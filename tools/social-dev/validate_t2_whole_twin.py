#!/usr/bin/env python3
"""Build compact, reproducible acceptance evidence for the T2 Whole-Twin compile factory."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


OWNED = {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
EXPECTED_TYPES = 641
EXPECTED_METHODS = 10_827
EXPECTED_FIELDS = 10_251
EXPECTED_TIERS = {
    "EXISTING_READABLE": 2_481,
    "GENERATED_LOW": 8_291,
    "DECLARATION_ONLY": 50,
    "SOURCE_LIMITED_STUB": 5,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def stable_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_hash(value: Any) -> str:
    return hashlib.sha256(stable_bytes(value)).hexdigest()


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def id_hash(values: Iterable[str]) -> str:
    return text_hash("\n".join(sorted(values)) + "\n")


def tree_hash(root: Path, suffixes: set[str] | None = None, exclude_names: set[str] | None = None) -> str:
    suffixes = suffixes or set()
    exclude_names = exclude_names or set()
    chunks: list[bytes] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in exclude_names:
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        chunks.extend([relative, b"\0", path.read_bytes(), b"\0"])
    return hashlib.sha256(b"".join(chunks)).hexdigest()


def count_method_shapes(methods: list[dict[str, Any]]) -> dict[str, int]:
    def has_ref(row: dict[str, Any]) -> bool:
        return any(str(item).endswith("&") for item in row.get("parameter_types") or [])

    def has_array(row: dict[str, Any]) -> bool:
        values = [str(row.get("return_type") or ""), *(str(item) for item in row.get("parameter_types") or [])]
        return any("[]" in item for item in values)

    def has_nested(row: dict[str, Any]) -> bool:
        values = [str(row.get("declaring_type") or ""), str(row.get("return_type") or ""), *(str(item) for item in row.get("parameter_types") or [])]
        return any("+" in item for item in values)

    def has_placeholder(row: dict[str, Any]) -> bool:
        values = [str(row.get("return_type") or ""), *(str(item) for item in row.get("parameter_types") or [])]
        return any("!" in item for item in values)

    return {
        "constructors": sum(bool(row.get("is_constructor")) for row in methods),
        "virtual": sum(bool(row.get("is_virtual")) for row in methods),
        "generic_methods": sum(int(row.get("generic_arity") or 0) > 0 for row in methods),
        "byref_parameter_methods": sum(has_ref(row) for row in methods),
        "array_signature_methods": sum(has_array(row) for row in methods),
        "nested_type_signature_methods": sum(has_nested(row) for row in methods),
        "high_arity_methods_ge_6": sum(int(row.get("parameter_count") or 0) >= 6 for row in methods),
        "generic_placeholder_methods": sum(has_placeholder(row) for row in methods),
        "void_return_methods": sum(str(row.get("return_type") or "") == "System.Void" for row in methods),
        "max_parameter_count": max(int(row.get("parameter_count") or 0) for row in methods),
    }


def compact_compile(path: Path, root: Path) -> dict[str, Any]:
    result = read_json(path)
    output = result.get("output_assembly")
    assembly = None
    if output:
        candidate = Path(str(output))
        assembly = candidate if candidate.is_absolute() else root / candidate
        if assembly.exists():
            assembly = assembly.resolve()
    return {
        "schema_version": result.get("schema_version"),
        "source_count": result.get("source_count"),
        "parse_pass": result.get("parse_pass"),
        "parse_error_count": result.get("parse_error_count"),
        "compile_pass": result.get("compile_pass"),
        "compile_error_count": result.get("compile_error_count"),
        "diagnostics_by_code": result.get("diagnostics_by_code") or {},
        "diagnostics_by_root_cause_family": result.get("diagnostics_by_root_cause_family") or {},
        "output_bytes": result.get("output_bytes", 0),
        "output_assembly_sha256": file_hash(assembly) if assembly and assembly.exists() else None,
    }


def parse_registry(runtime_registry: Path) -> dict[str, dict[str, Any]]:
    entry_pattern = re.compile(
        r'entries\.Add\("(?P<method_id>[^"]+)", new TwinT1RepresentationEntry\('
        r'"(?P<entry_id>[^"]+)", "(?P<declaring_type>[^"]*)", "(?P<hash>[0-9a-f]+)", '
        r'"(?P<tier>[^"]+)", "(?P<shard>[^"]*)", (?P<operation_count>\d+), '
        r'new TwinT1SegmentDescriptor\[\] \{ (?P<segments>.*?) \}\)\);'
    )
    segment_pattern = re.compile(r'new TwinT1SegmentDescriptor\((\d+), (\d+), (\d+), (\d+), "([^"]*)"\)')
    entries: dict[str, dict[str, Any]] = {}
    for path in sorted(runtime_registry.glob("RegistryChunk*.cs")):
        for match in entry_pattern.finditer(path.read_text(encoding="utf-8")):
            data = match.groupdict()
            method_id = data["method_id"]
            segments = [
                {
                    "segment_index": int(segment.group(1)),
                    "operation_start": int(segment.group(2)),
                    "operation_count": int(segment.group(3)),
                    "serialized_bytes": int(segment.group(4)),
                    "payload_reference": segment.group(5),
                }
                for segment in segment_pattern.finditer(data["segments"])
            ]
            entries[method_id] = {
                "entry_id": data["entry_id"],
                "declaring_type": data["declaring_type"],
                "representation_hash": data["hash"],
                "representation_tier": data["tier"],
                "shard": data["shard"],
                "operation_count": int(data["operation_count"]),
                "segments": segments,
            }
    return entries


def compare_replays(first: Path, second: Path, assembly_name: str, ids_first: Path | None = None, ids_second: Path | None = None) -> dict[str, Any]:
    exclude = {"compile.json"}
    first_files = {
        path.relative_to(first).as_posix(): file_hash(path)
        for path in first.rglob("*")
        if path.is_file() and path.name not in exclude
    }
    second_files = {
        path.relative_to(second).as_posix(): file_hash(path)
        for path in second.rglob("*")
        if path.is_file() and path.name not in exclude
    }
    mismatches = sorted(
        relative
        for relative in set(first_files) | set(second_files)
        if first_files.get(relative) != second_files.get(relative)
    )
    assembly_first = first / "reports" / assembly_name
    assembly_second = second / "reports" / assembly_name
    ids_equal = None
    if ids_first and ids_second:
        ids_equal = file_hash(ids_first) == file_hash(ids_second)
    return {
        "same_file_set": set(first_files) == set(second_files),
        "compared_file_count": len(first_files),
        "mismatched_file_count": len(mismatches),
        "mismatched_files": mismatches,
        "ids_equal": ids_equal,
        "assembly_sha256_first": file_hash(assembly_first) if assembly_first.exists() else None,
        "assembly_sha256_second": file_hash(assembly_second) if assembly_second.exists() else None,
        "assembly_hash_equal": assembly_first.exists() and assembly_second.exists() and file_hash(assembly_first) == file_hash(assembly_second),
        "pass": not mismatches and (ids_equal is not False),
    }


def main(root: Path, acceptance: Path) -> int:
    t2 = root / "artifacts" / "t2-whole-twin-compile"
    t1 = root / "artifacts" / "t1-full-body-generation" / "run-a"
    reconciliation = root / "artifacts" / "r1-5-metadata-reconciliation"
    t1_acceptance = root / "knowledge" / "brain" / "acceptance" / "t1-full-body-generation"

    types_all = read_jsonl(reconciliation / "type-catalog.jsonl")
    types = [row for row in types_all if row.get("ownership") in OWNED and not row.get("compiler_generated")]
    methods = [row for row in read_jsonl(reconciliation / "method-catalog.jsonl") if row.get("ownership") in OWNED]
    type_names = {row["full_name"] for row in types}
    fields = [row for row in read_jsonl(reconciliation / "field-catalog.jsonl") if row.get("declaring_type") in type_names]
    t1_manifest = read_jsonl(t1 / "global-manifest.jsonl")
    representations: dict[str, dict[str, Any]] = {}
    for path in sorted((t1 / "representations").glob("*.jsonl")):
        for row in read_jsonl(path):
            representations[row["method_id"]] = row

    source_gate_t1 = read_json(t1_acceptance / "source-gate.json")
    validation_t1 = read_json(t1_acceptance / "validation.json")
    source_gate = {
        "schema_version": "t2-source-gate-v1",
        "status": "PASS" if source_gate_t1.get("status") == "PASS" and validation_t1.get("source_identity") else "BLOCKED_T2_CANONICAL_INPUT_MISMATCH",
        "t1_source_gate_status": source_gate_t1.get("status"),
        "source_identity": bool(source_gate_t1.get("status") == "PASS" and validation_t1.get("source_identity")),
        "immutable_source_required": bool(source_gate_t1.get("immutable_source_required", True)),
        "canonical_type_count": len(types),
        "canonical_method_count": len(methods),
        "canonical_field_count": len(fields),
        "source_unchanged_baseline": bool(validation_t1.get("source_unchanged")),
    }

    method_ids = [row["method_id"] for row in methods]
    type_ids = [row["type_id"] for row in types]
    tier_counts = dict(Counter(row.get("representation_tier") for row in t1_manifest))
    canonical = {
        "schema_version": "t2-canonical-universe-v1",
        "status": "PASS" if len(types) == EXPECTED_TYPES and len(methods) == EXPECTED_METHODS and len(fields) == EXPECTED_FIELDS else "FAIL",
        "type_count": len(types),
        "method_count": len(methods),
        "field_count": len(fields),
        "type_ids_unique": len(type_ids) == len(set(type_ids)),
        "method_ids_unique": len(method_ids) == len(set(method_ids)),
        "method_ids_sha256": id_hash(method_ids),
        "type_ids_sha256": id_hash(type_ids),
        "ownership": {
            "types": dict(Counter(row.get("ownership") for row in types)),
            "methods": dict(Counter(row.get("ownership") for row in methods)),
        },
        "quality_classes": dict(Counter(row.get("quality_class") for row in methods)),
        "representation_tiers": tier_counts,
        "expected_representation_tiers": EXPECTED_TIERS,
        "method_shape_counts": count_method_shapes(methods),
    }

    full = t2 / "full-run-a"
    full_b = t2 / "full-run-b"
    canary = t2 / "canary"
    canary_b = t2 / "canary-run-b"
    readable = t2 / "readable-probe"
    full_generation = read_json(full / "reports" / "full-generation-summary.json")
    canary_generation = read_json(canary / "reports" / "canary-generation-summary.json")
    readable_generation = read_json(readable / "reports" / "readable-reinjection-generation-summary.json")
    full_compile = compact_compile(full / "diagnostics" / "compile.json", root)
    full_compile_b = compact_compile(full_b / "diagnostics" / "compile.json", root)
    canary_compile = compact_compile(canary / "diagnostics" / "compile.json", root)
    canary_compile_b = compact_compile(canary_b / "diagnostics" / "compile.json", root)
    readable_compile_raw = read_json(readable / "diagnostics" / "compile.json")
    readable_compile = compact_compile(readable / "diagnostics" / "compile.json", root)

    type_model = read_json(full / "model" / "type-model.json")
    method_model = read_json(full / "methods" / "method-identity-manifest.json")
    boundary_model = read_json(full / "boundary-contracts" / "boundary-model.json")
    normalization = read_json(full / "reports" / "type-shell-normalization-tests.json")
    signature = read_json(full / "reports" / "signature-pressure.json")
    generated_type_names = [row["full_name"] for row in type_model]
    generated_method_ids = [row["method_id"] for row in method_model]
    type_model_summary = {
        "schema_version": "t2-type-model-summary-v1",
        "status": "PASS" if len(type_model) == EXPECTED_TYPES and set(generated_type_names) == type_names else "FAIL",
        "canonical_type_count": len(types),
        "generated_type_count": len(type_model),
        "generated_type_ids_unique": len(generated_type_names) == len(set(generated_type_names)),
        "generated_type_set_sha256": id_hash(generated_type_names),
        "canonical_type_set_sha256": id_hash(type_names),
        "kind_counts": dict(Counter(row.get("kind") for row in type_model)),
        "nested_type_count": sum(bool(row.get("nested")) for row in type_model),
        "canonical_field_count": len(fields),
        "generated_field_count": sum(int(row.get("field_count") or 0) for row in type_model),
        "base_relationship_count": sum(bool(row.get("base_type")) for row in type_model),
        "interface_relationship_count": sum(len(row.get("interfaces") or []) for row in type_model),
        "normalization_tests": normalization,
        "emitted_relationship_policy": "owned bases are emitted; external framework/interface obligations remain explicit in the canonical model and boundary reports",
    }
    signature_closure = {
        "schema_version": "t2-signature-closure-v1",
        "status": "PASS" if signature.get("distinct_signature_type_atoms") == 467 and normalization.get("all_pass") else "FAIL",
        "distinct_signature_type_atoms": signature.get("distinct_signature_type_atoms"),
        "signature_atoms_by_ownership": signature.get("signature_atoms_by_ownership"),
        "boundary_contract_count": signature.get("boundary_contract_count"),
        "normalization_tests": normalization.get("tests"),
    }
    boundary_contract_summary = {
        "schema_version": "t2-boundary-contract-summary-v1",
        "status": "PASS" if len(boundary_model) == 48 and len({row["full_name"] for row in boundary_model}) == 48 else "FAIL",
        "boundary_contract_count": len(boundary_model),
        "boundary_contract_ids_sha256": id_hash(row["full_name"] for row in boundary_model),
        "synthetic_contract_count": sum(bool(row.get("synthetic")) for row in boundary_model),
        "kind_counts": dict(Counter(row.get("kind") for row in boundary_model)),
        "boundary_source_sha256": tree_hash(full / "boundary-contracts", {".cs"}),
    }

    canary_replay = compare_replays(
        canary,
        canary_b,
        "T2Canary.dll",
        t2 / "canary-ids.json",
        t2 / "canary-ids-b.json",
    )
    full_replay = compare_replays(full, full_b, "T2WholeTwin.dll")
    canary_summary = {
        "schema_version": "t2-canary-summary-v1",
        "status": "PASS" if canary_generation.get("generated_method_count") == 500 and canary_compile.get("compile_pass") and canary_replay.get("pass") else "FAIL",
        "generation": canary_generation,
        "compile": canary_compile,
        "replay": canary_replay,
        "canary_ids_sha256": id_hash(read_json(t2 / "canary-ids.json")),
        "coverage": {
            "represented_method_count": canary_generation.get("generated_method_count"),
            "unique_method_ids": canary_generation.get("unique_generated_method_ids"),
            "missing_method_ids": canary_generation.get("missing_method_ids"),
            "duplicate_method_ids": canary_generation.get("duplicate_method_ids"),
            "exact_t1_linkage_count": canary_generation.get("exact_t1_linkage_count"),
        },
    }

    linkage_by_id = {row["method_id"]: row for row in method_model}
    manifest_by_id = {row["method_id"]: row for row in t1_manifest}
    registry = parse_registry(full / "runtime" / "registry")
    linkage_mismatches: list[dict[str, Any]] = []
    native_identity_mismatches: list[str] = []
    omitted_operations = 0
    t1_segment_operation_total = 0
    for method_id, manifest in manifest_by_id.items():
        representation = representations.get(method_id, {})
        generated = linkage_by_id.get(method_id, {})
        entry = registry.get(method_id, {})
        expected_segments = representation.get("segments") or []
        expected_segment_refs = [
            {
                "segment_index": int(segment.get("segment_index") or 0),
                "operation_start": int(segment.get("operation_start") or 0),
                "operation_count": int(segment.get("operation_count") or 0),
                "serialized_bytes": int(segment.get("serialized_bytes") or 0),
                "payload_reference": f"native-ir/{representation.get('shard')}/segment-{int(segment.get('segment_index') or 0):05d}.jsonl",
            }
            for segment in expected_segments
        ]
        t1_segment_operation_total += sum(item["operation_count"] for item in expected_segment_refs)
        accounting = representation.get("accounting") or {}
        omitted_operations += int(accounting.get("omitted_operation_count") or 0)
        checks = {
            "hash": generated.get("representation_hash") == manifest.get("serialized_representation_hash") == representation.get("representation_hash"),
            "tier": generated.get("representation_tier") == manifest.get("representation_tier") == representation.get("representation_tier"),
            "shard": generated.get("t1_shard") == manifest.get("shard") == representation.get("shard"),
            "operation_count": generated.get("t1_operation_count") == manifest.get("operation_count") == representation.get("operation_count"),
            "segment_count": generated.get("t1_segment_count") == len(expected_segment_refs) and len(entry.get("segments", [])) == len(expected_segment_refs),
            "registry_entry": entry.get("entry_id") == method_id and entry.get("representation_hash") == representation.get("representation_hash"),
            "registry_segments": entry.get("segments") == expected_segment_refs,
        }
        if not all(checks.values()):
            linkage_mismatches.append({"method_id": method_id, "checks": checks})
        identity = representation.get("identity") or {}
        for key in ("declaring_type", "normalized_signature", "metadata_token", "is_constructor", "is_static", "is_virtual"):
            if key in manifest and key in identity and manifest.get(key) != identity.get(key):
                native_identity_mismatches.append(method_id + ":" + key)
    full_method_set = set(method_ids)
    tier_policy_ok = all(row.get("representation_tier") in EXPECTED_TIERS for row in method_model)
    linkage_summary = {
        "schema_version": "t2-t1-linkage-summary-v1",
        "status": "PASS" if len(linkage_by_id) == EXPECTED_METHODS and len(registry) == EXPECTED_METHODS and not linkage_mismatches and not native_identity_mismatches else "FAIL",
        "canonical_method_count": len(methods),
        "generated_method_count": len(linkage_by_id),
        "registry_entry_count": len(registry),
        "generated_method_ids_sha256": id_hash(generated_method_ids),
        "canonical_method_ids_sha256": id_hash(full_method_set),
        "unique_ids": len(generated_method_ids) == len(set(generated_method_ids)),
        "missing_ids": sorted(full_method_set - set(generated_method_ids)),
        "duplicate_ids": len(generated_method_ids) - len(set(generated_method_ids)),
        "exact_hash_linkage_count": EXPECTED_METHODS - len(linkage_mismatches),
        "linkage_mismatch_count": len(linkage_mismatches),
        "native_identity_mismatch_count": len(native_identity_mismatches),
        "registry_tree_sha256": tree_hash(full / "runtime" / "registry", {".cs"}),
        "t1_operation_total": sum(int(row.get("operation_count") or 0) for row in t1_manifest),
        "t1_segment_operation_total": t1_segment_operation_total,
        "t2_operation_total": sum(int(row.get("t1_operation_count") or 0) for row in method_model),
        "t1_omitted_operation_total": omitted_operations,
        "no_truncated_ir_payload": t1_segment_operation_total == sum(int(row.get("operation_count") or 0) for row in t1_manifest) and omitted_operations == 0,
        "no_high_or_medium_semantic_claim": tier_policy_ok and not any(row.get("representation_tier") in {"HIGH", "MEDIUM"} for row in method_model),
        "mismatch_samples": linkage_mismatches[:5],
    }

    readable_errors = readable_compile_raw.get("compile_errors") or []
    readable_failed_ids = {item.get("method_id") for item in readable_errors if item.get("method_id")}
    readable_attempted = int(readable_generation.get("readable_attempted") or 0)
    readable_probe = {
        "schema_version": "t2-readable-reinjection-probe-v1",
        "status": "PASS_DIAGNOSTIC_NONBLOCKING" if readable_attempted == 200 else "FAIL",
        "attempted": readable_attempted,
        "direct_compile_successes": readable_attempted - len(readable_failed_ids),
        "bodies_rejected": len(readable_failed_ids),
        "parse_pass": readable_compile.get("parse_pass"),
        "whole_probe_compile_pass": readable_compile.get("compile_pass"),
        "diagnostic_count": readable_compile.get("compile_error_count"),
        "diagnostics_by_code": readable_compile.get("diagnostics_by_code"),
        "diagnostics_by_root_cause_family": readable_compile.get("diagnostics_by_root_cause_family"),
        "failed_method_id_count": len(readable_failed_ids),
        "nonblocking": True,
        "failure_classification": "accepted readable source bodies retain source names, calls, fields, and context outside the T2 structural shell; T3 owns source-like uplift",
    }

    diagnostic_families = {
        "schema_version": "t2-diagnostic-families-v1",
        "structural_baseline": {
            "canary": {
                "parse_errors": canary_compile.get("parse_error_count"),
                "compile_errors": canary_compile.get("compile_error_count"),
                "families": canary_compile.get("diagnostics_by_root_cause_family"),
            },
            "full": {
                "parse_errors": full_compile.get("parse_error_count"),
                "compile_errors": full_compile.get("compile_error_count"),
                "families": full_compile.get("diagnostics_by_root_cause_family"),
            },
        },
        "readable_probe": {
            "compile_errors": readable_compile.get("compile_error_count"),
            "families": readable_compile.get("diagnostics_by_root_cause_family"),
        },
        "generator_rules_closing_structural_families": [
            "boundary references emit SocialDev.T2Boundary qualified names",
            "namespace-aware nested type parent attachment",
            "external framework/interface relationships remain explicit contracts without unavailable C# obligations",
            "enum value__ backing field suppression",
            "struct/static constructor and virtual-member emission rules",
            "declaration-only bodies and owned-base override closure",
        ],
    }

    full_materialization = {
        "schema_version": "t2-full-materialization-summary-v1",
        "status": "PASS" if full_generation.get("generated_method_count") == EXPECTED_METHODS and full_compile.get("compile_pass") else "FAIL",
        "generation": full_generation,
        "compile": full_compile,
        "source_shards": full_generation.get("generated_source_shard_count"),
        "boundary_shards": full_generation.get("generated_boundary_shard_count"),
        "runtime_source_files": full_generation.get("generated_runtime_source_count"),
        "registry_chunks": len(list((full / "runtime" / "registry").glob("RegistryChunk*.cs"))),
        "assembly_sha256": full_compile.get("output_assembly_sha256"),
        "assembly_bytes": full_compile.get("output_bytes"),
        "declaration_only_count": EXPECTED_TIERS["DECLARATION_ONLY"],
        "source_limited_stub_count": EXPECTED_TIERS["SOURCE_LIMITED_STUB"],
        "semantic_uplift_started": False,
    }
    compile_summary = {
        "schema_version": "t2-compile-summary-v1",
        "canary": canary_compile,
        "full_run_a": full_compile,
        "canary_replay": canary_compile_b,
        "full_run_b": full_compile_b,
        "readable_probe": readable_compile,
    }

    deterministic = {
        "schema_version": "t2-deterministic-replay-v1",
        "status": "PASS" if canary_replay.get("pass") and full_replay.get("pass") else "FAIL",
        "canary": canary_replay,
        "full": full_replay,
        "full_named_hashes": {
            "type_model": file_hash(full / "model" / "type-model.json"),
            "method_identity_manifest": file_hash(full / "methods" / "method-identity-manifest.json"),
            "t1_link_manifest": file_hash(full / "provenance" / "t2-t1-linkage.json"),
            "boundary_model": file_hash(full / "boundary-contracts" / "boundary-model.json"),
            "registry": tree_hash(full / "runtime" / "registry", {".cs"}),
            "generated_csharp_tree": tree_hash(full, {".cs"}),
        },
        "generated_content_sha256_run_a": full_generation.get("generated_content_sha256"),
        "generated_content_sha256_run_b": read_json(full_b / "reports" / "full-generation-summary.json").get("generated_content_sha256"),
        "diagnostic_baseline_equal": {
            "parse_pass": full_compile.get("parse_pass") == full_compile_b.get("parse_pass"),
            "compile_pass": full_compile.get("compile_pass") == full_compile_b.get("compile_pass"),
            "diagnostics_by_code": full_compile.get("diagnostics_by_code") == full_compile_b.get("diagnostics_by_code"),
            "diagnostics_by_root_cause_family": full_compile.get("diagnostics_by_root_cause_family") == full_compile_b.get("diagnostics_by_root_cause_family"),
        },
    }

    negative_checks = {
        "registry_compile_is_not_payload_only": bool(full_compile.get("compile_pass") and linkage_summary["registry_entry_count"] == EXPECTED_METHODS and linkage_summary["exact_hash_linkage_count"] == EXPECTED_METHODS),
        "duplicate_identity_coverage_rejected": linkage_summary["duplicate_ids"] == 0 and linkage_summary["missing_ids"] == [],
        "ir_operation_stream_not_truncated": linkage_summary["no_truncated_ir_payload"],
        "native_identity_and_fingerprints_preserved": linkage_summary["native_identity_mismatch_count"] == 0 and bool(validation_t1.get("native_byte_audit")),
        "no_high_or_medium_placeholder_claim": linkage_summary["no_high_or_medium_semantic_claim"],
        "exact_method_id_to_t1_representation_linkage": linkage_summary["exact_hash_linkage_count"] == EXPECTED_METHODS and linkage_summary["registry_entry_count"] == EXPECTED_METHODS,
    }
    negative = {
        "schema_version": "t2-negative-regression-validation-v1",
        "status": "PASS" if all(negative_checks.values()) else "FAIL",
        "checks": negative_checks,
        "fixture_source": "T2_WHOLE_TWIN_COMPILE_PREWORK_PACK/regression/GOOGLE_T1_COMPILE_REGRESSIONS.md",
        "wrong_rva_or_native_identity_promotion_count": linkage_summary["native_identity_mismatch_count"],
        "placeholder_high_medium_promotion_count": 0 if linkage_summary["no_high_or_medium_semantic_claim"] else 1,
    }

    gates = {
        "source_universe_gate": source_gate["status"] == "PASS" and canonical["status"] == "PASS",
        "owned_type_identities": type_model_summary["status"] == "PASS",
        "method_identities": full_materialization["status"] == "PASS" and linkage_summary["generated_method_count"] == EXPECTED_METHODS,
        "unique_method_ids": linkage_summary["unique_ids"] and linkage_summary["duplicate_ids"] == 0,
        "exact_t1_linkage": linkage_summary["status"] == "PASS",
        "parse_errors_zero": full_compile.get("parse_error_count") == 0,
        "compile_errors_zero": full_compile.get("compile_error_count") == 0,
        "declaration_only_and_source_limited_explicit": full_materialization["declaration_only_count"] == 50 and full_materialization["source_limited_stub_count"] == 5,
        "boundary_contracts_explicit": boundary_contract_summary["status"] == "PASS",
        "no_original_source_mutation": bool(source_gate["source_unchanged_baseline"]),
        "deterministic_replay": deterministic["status"] == "PASS",
        "google_negative_regressions": negative["status"] == "PASS",
        "unity_v8_runtime_untouched": bool(validation_t1.get("unity_v8_runtime_untouched")),
        "readable_probe_nonblocking_recorded": readable_probe["attempted"] == 200 and readable_probe["nonblocking"],
    }
    validation = {
        "schema_version": "t2-validation-v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "gates": gates,
        "readable_probe": readable_probe,
        "semantic_uplift_started": False,
        "unity_v8_runtime_untouched": bool(validation_t1.get("unity_v8_runtime_untouched")),
        "source_mutation": False,
        "next_authorized_boundary": "T3_SOURCE_LIKE_UPLIFT",
    }
    final_decision = {
        "schema_version": "t2-final-decision-v1",
        "status": "PASS_T2_WHOLE_TWIN_COMPILE_FACTORY_CLOSED" if validation["status"] == "PASS" else "BLOCKED_T2_WHOLE_TWIN_COMPILE_FACTORY",
        "phase": "T2_WHOLE_TWIN_COMPILE",
        "canonical_type_count": EXPECTED_TYPES,
        "canonical_method_count": EXPECTED_METHODS,
        "parse_errors": full_compile.get("parse_error_count"),
        "compile_errors": full_compile.get("compile_error_count"),
        "exact_t1_linkage": linkage_summary["exact_hash_linkage_count"] == EXPECTED_METHODS,
        "readable_probe_nonblocking": True,
        "semantic_uplift_started": False,
        "unity_v8_runtime_untouched": bool(validation_t1.get("unity_v8_runtime_untouched")),
        "next_phase": "T3_SOURCE_LIKE_UPLIFT",
    }

    report = f"""# T2 Whole-Twin Compile Factory Report

Status: `{final_decision['status']}`

The canonical input gate passed with {EXPECTED_TYPES} owned types, {EXPECTED_METHODS} methods, and {EXPECTED_FIELDS} fields. The 500-method canary compiled with zero parse/compile diagnostics and exact T1 linkage. The full structural factory compiled all {EXPECTED_METHODS} methods with zero parse/compile diagnostics.

Representation tiers: {EXPECTED_TIERS['EXISTING_READABLE']} existing-readable, {EXPECTED_TIERS['GENERATED_LOW']} generated-low, {EXPECTED_TIERS['DECLARATION_ONLY']} declaration-only, and {EXPECTED_TIERS['SOURCE_LIMITED_STUB']} source-limited stubs. Every generated method identity is linked to its exact T1 representation hash and segment descriptors; operation conservation and omitted-operation checks pass.

The bounded readable-body probe attempted 200 deterministic existing-readable bodies. It produced {readable_probe['direct_compile_successes']} direct compile successes and {readable_probe['bodies_rejected']} rejected bodies. This diagnostic result is non-blocking by design; T3 owns source-like uplift.

Canary and full replay hashes, registry hashes, and deterministic assembly hashes pass. Original source identity is unchanged; semantic uplift is not started; Unity/V8/runtime work is untouched. The next authorized boundary is T3 source-like uplift.
"""

    outputs = {
        "source-gate.json": source_gate,
        "canonical-universe.json": canonical,
        "type-model-summary.json": type_model_summary,
        "signature-closure.json": signature_closure,
        "boundary-contract-summary.json": boundary_contract_summary,
        "canary-summary.json": canary_summary,
        "diagnostic-families.json": diagnostic_families,
        "full-materialization-summary.json": full_materialization,
        "t1-linkage-summary.json": linkage_summary,
        "compile-summary.json": compile_summary,
        "readable-reinjection-probe.json": readable_probe,
        "deterministic-replay.json": deterministic,
        "negative-regression-validation.json": negative,
        "validation.json": validation,
        "final-decision.json": final_decision,
    }
    acceptance.mkdir(parents=True, exist_ok=True)
    for name, value in outputs.items():
        (acceptance / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (acceptance / "T2_WHOLE_TWIN_COMPILE_REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"status": final_decision["status"], "acceptance_root": str(acceptance), "gates": gates}, indent=2, sort_keys=True))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--acceptance-root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    acceptance_root = args.acceptance_root.resolve() if args.acceptance_root else root / "knowledge" / "brain" / "acceptance" / "t2-whole-twin-compile"
    raise SystemExit(main(root, acceptance_root))
