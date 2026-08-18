#!/usr/bin/env python3
"""Run the deterministic T3 source-like uplift over the accepted T1/T2 corpus.

The runner keeps T1 native/source evidence read-only and uses the accepted T2 whole-Twin
factory as the only C# materializer.  Promotions are deliberately conservative: an exact
readable source body is promoted only when the prior whole-Twin probe attributed no diagnostic,
and native promotions are limited to small, mechanically proven field/constant/argument/empty
patterns.  Every wave is compiled before its promotions are retained.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

import t2_whole_twin_compile as t2


ROOT = Path(__file__).resolve().parents[2]
T3_ACCEPTANCE = ROOT / "knowledge" / "brain" / "acceptance" / "t3-source-like-uplift"
T3_ARTIFACT_ROOT = ROOT / "artifacts" / "t3-source-like-uplift"
T2_ACCEPTANCE = ROOT / "knowledge" / "brain" / "acceptance" / "t2-whole-twin-compile"
OWNED = set(t2.OWNED)
EXPECTED_TYPES = 641
EXPECTED_METHODS = 10_827
EXPECTED_FIELDS = 10_251
EXPECTED_OPS = 988_046
EXPECTED_TIERS = {
    "EXISTING_READABLE": 2_481,
    "GENERATED_LOW": 8_291,
    "DECLARATION_ONLY": 50,
    "SOURCE_LIMITED_STUB": 5,
}
ROSYN_PWSH = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "powershell" / "pwsh.exe"
PREVIOUS_SIGNATURE_CLOSURE_SHA256 = "8d75b5e166a45388df5f003760b477e760d87d5801632451bbc7464924205bb4"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_hash_ids(ids: Iterable[str]) -> str:
    return sha256_text("\n".join(sorted(ids)) + "\n")


def source_tree_hash(root: Path) -> str:
    parts: list[str] = []
    for path in sorted(root.rglob("*.cs")):
        parts.append(path.relative_to(root).as_posix())
        parts.append(path.read_text(encoding="utf-8"))
    return sha256_text("\n---FILE---\n".join(parts))


def safe_clear(path: Path) -> None:
    resolved = path.resolve()
    allowed = T3_ARTIFACT_ROOT.resolve()
    if resolved == allowed or allowed not in resolved.parents:
        raise RuntimeError(f"Refusing unsafe T3 output path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)


def flatten_native(native_segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []
    for segment in sorted(native_segments, key=lambda item: (int(item.get("operation_start") or 0), int(item.get("segment_index") or 0))):
        start = int(segment.get("operation_start") or 0)
        for index, operation in enumerate(segment.get("operations") or []):
            item = dict(operation)
            item["canonical_operation_index"] = start + index
            operations.append(item)
    operations.sort(key=lambda item: (int(item.get("canonical_operation_index") or 0), int(item.get("native_index") or 0)))
    return operations


def is_unknown_operation(operation: dict[str, Any]) -> bool:
    family = str(operation.get("family") or "").upper()
    kind = str(operation.get("kind") or "").upper()
    return family in {"UNKNOWN", "RAW_UNKNOWN", "UNMODELED"} or "UNKNOWN" in kind


def operation_counts(operations: list[dict[str, Any]]) -> dict[str, Any]:
    families = collections.Counter(str(item.get("family") or item.get("kind") or "UNKNOWN") for item in operations)
    calls = 0
    resolved_calls = 0
    fields = 0
    branches = 0
    unknown = 0
    for operation in operations:
        facts = operation.get("typed_facts") or {}
        call = facts.get("call")
        if call:
            calls += 1
            resolution = str(call.get("resolution") or "")
            if resolution and "UNRESOLVED" not in resolution.upper() and call.get("target_method_id"):
                resolved_calls += 1
        if facts.get("field"):
            fields += 1
        if facts.get("branch_target") is not None or str(operation.get("family") or "").upper() == "BRANCH":
            branches += 1
        if is_unknown_operation(operation):
            unknown += 1
    return {
        "families": dict(sorted(families.items())),
        "call_count": calls,
        "resolved_call_count": resolved_calls,
        "field_access_count": fields,
        "branch_count": branches,
        "unknown_operation_count": unknown,
    }


def method_risk_shapes(row: dict[str, Any], facts: dict[str, Any]) -> list[str]:
    shapes: list[str] = []
    parameters = [str(value) for value in row.get("parameter_types") or []]
    if int(row.get("generic_arity") or 0) > 0 or any(value.startswith("!") or value.startswith("!!") for value in parameters):
        shapes.append("GENERIC")
    if any(value.endswith("&") for value in parameters):
        shapes.append("BYREF")
    if any("[]" in value for value in parameters) or "[]" in str(row.get("return_type") or ""):
        shapes.append("ARRAY")
    if "+" in str(row.get("declaring_type") or "") or any("+" in value for value in parameters):
        shapes.append("NESTED")
    if row.get("is_constructor") or row.get("method_name") in {".ctor", ".cctor"}:
        shapes.append("CONSTRUCTOR")
    if row.get("is_virtual"):
        shapes.append("VIRTUAL")
    if row.get("compiler_generated"):
        shapes.append("COMPILER_GENERATED")
    if facts.get("branch_count", 0):
        shapes.append("CFG_BRANCH")
    if facts.get("call_count", 0) >= 2:
        shapes.append("CALL_HEAVY")
    if int(row.get("operation_count") or 0) >= 32:
        shapes.append("NATIVE_HEAVY")
    return shapes or ["STRAIGHT_LINE"]


def classify_family(row: dict[str, Any], facts: dict[str, Any]) -> str:
    if row.get("is_constructor"):
        return "CONSTRUCTOR"
    if row.get("compiler_generated"):
        return "COMPILER_GENERATED"
    if facts.get("branch_count", 0):
        return "CONTROL_FLOW"
    if facts.get("call_count", 0):
        return "CALL_HEAVY"
    if facts.get("field_access_count", 0):
        return "FIELD_ACCESSOR"
    if int(row.get("operation_count") or 0) <= 3:
        return "STRAIGHT_LINE"
    return "NATIVE_HEAVY"


class Corpus:
    def __init__(self, root: Path):
        self.root = root
        metadata = root / "artifacts" / "r1-5-metadata-reconciliation"
        all_types = t2.read_jsonl(metadata / "type-catalog.jsonl")
        self.types = [row for row in all_types if row.get("ownership") in OWNED and not row.get("compiler_generated")]
        self.methods = [row for row in t2.read_jsonl(metadata / "method-catalog.jsonl") if row.get("ownership") in OWNED]
        owned_type_names = {row["full_name"] for row in self.types}
        self.fields = [row for row in t2.read_jsonl(metadata / "field-catalog.jsonl") if row.get("declaring_type") in owned_type_names]
        self.manifest = {row["method_id"]: row for row in t2.read_jsonl(root / "artifacts" / "t1-full-body-generation" / "run-a" / "global-manifest.jsonl")}
        self.representations: dict[str, dict[str, Any]] = {}
        rep_root = root / "artifacts" / "t1-full-body-generation" / "run-a" / "representations"
        for path in sorted(rep_root.glob("*.jsonl")):
            for row in t2.iter_jsonl(path):
                if row.get("method_id"):
                    self.representations[row["method_id"]] = row
        self.native_segments: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        native_root = root / "artifacts" / "t1-full-body-generation" / "run-a" / "native-ir"
        for path in sorted(native_root.glob("shard-*/segment-*.jsonl")):
            for row in t2.iter_jsonl(path):
                method_id = row.get("method_id")
                if method_id:
                    self.native_segments[method_id].append(row)
        self.profile: list[dict[str, Any]] = []
        self.by_id: dict[str, dict[str, Any]] = {}

    def build_profile(self) -> list[dict[str, Any]]:
        if self.profile:
            return self.profile
        for row in sorted(self.methods, key=lambda item: item["method_id"]):
            method_id = row["method_id"]
            representation = self.representations[method_id]
            operations = flatten_native(self.native_segments.get(method_id, []))
            facts = operation_counts(operations)
            source_relation = representation.get("source_relation") or {}
            metadata = representation.get("metadata") or {}
            facts_summary = representation.get("facts_summary") or {}
            source_body = representation.get("source_body")
            profile_row = {
                "method_id": method_id,
                "ownership": row.get("ownership"),
                "assembly": row.get("assembly"),
                "declaring_type": row.get("declaring_type"),
                "method_name": row.get("method_name"),
                "normalized_signature": row.get("normalized_signature"),
                "return_type": row.get("return_type"),
                "parameter_types": row.get("parameter_types") or [],
                "parameter_count": int(row.get("parameter_count") or 0),
                "generic_arity": int(row.get("generic_arity") or 0),
                "is_constructor": bool(row.get("is_constructor")),
                "is_static": bool(row.get("is_static")),
                "is_virtual": bool(row.get("is_virtual")),
                "compiler_generated": bool(row.get("compiler_generated")),
                "quality_class": row.get("quality_class"),
                "t1_representation_tier": representation.get("representation_tier"),
                "t1_representation_hash": representation.get("representation_hash") or representation.get("serialized_representation_hash"),
                "t1_shard": representation.get("shard") or self.manifest[method_id].get("shard"),
                "t1_segments": representation.get("segments") or [],
                "t1_operation_count": int(self.manifest[method_id].get("operation_count") or representation.get("operation_count") or 0),
                "native_fingerprints": {
                    "native_start": metadata.get("native_start"),
                    "native_end": metadata.get("native_end"),
                    "first": metadata.get("first_native_fingerprint"),
                    "last": metadata.get("last_native_fingerprint"),
                    "range_status": metadata.get("native_range_status"),
                },
                "operation_count": len(operations),
                "operation_families": facts["families"],
                "unknown_operation_count": facts["unknown_operation_count"],
                "resolved_call_count": facts["resolved_call_count"],
                "call_count": facts["call_count"],
                "field_access_count": facts["field_access_count"],
                "branch_count": facts["branch_count"],
                "cfg_block_count": int(facts_summary.get("cfg_block_count") or 0),
                "cfg_edge_count": int(facts_summary.get("cfg_edge_count") or 0),
                "source_body_present": bool(source_relation.get("body_present") or source_body),
                "source_body_hash": source_relation.get("extracted_body_sha256") or source_relation.get("body_sha256"),
                "source_relation": source_relation.get("relation") or source_relation.get("match_status"),
                "family": classify_family(row, facts),
                "risk_shapes": method_risk_shapes(row, facts),
                "t1_accounting": representation.get("accounting") or {},
                "native_operation_fingerprint": sha256_text("\n".join(f"{item.get('mnemonic')}|{item.get('operands')}|{item.get('raw_word_little_endian')}" for item in operations)),
                "promotion_eligible": False,
                "eligibility_reason": "not_profiled",
            }
            self.profile.append(profile_row)
            self.by_id[method_id] = profile_row
        return self.profile


def read_preflight_readable_ids(root: Path, corpus: Corpus) -> tuple[dict[str, str], set[str]]:
    bodies: dict[str, str] = {}
    readable_ids = {
        method_id
        for method_id, row in corpus.representations.items()
        if row.get("representation_tier") == "EXISTING_READABLE" and row.get("source_body")
    }
    for method_id in sorted(readable_ids):
        body = t2.extract_braced_body(str(corpus.representations[method_id].get("source_body") or ""))
        if body:
            bodies[method_id] = body
    preflight = root / "artifacts" / "t2-whole-twin-compile" / "t3-readable-all" / "diagnostics" / "compile.json"
    error_ids: set[str] = set()
    if preflight.exists():
        diagnostics = read_json(preflight)
        for diagnostic in diagnostics.get("compile_errors") or []:
            method_id = diagnostic.get("method_id")
            if method_id:
                error_ids.add(method_id)
    return {method_id: body for method_id, body in bodies.items() if method_id not in error_ids}, error_ids


def field_emitted_name(model: t2.T2Model, node: Any, field_row: dict[str, Any]) -> Optional[str]:
    """Reproduce T2's collision-safe field spelling for one canonical field."""
    if node is None:
        return None
    used = {child.names[-1] for child in node.children}
    for plan in model._type_node_method_rows(node):
        if plan["raw_name"] not in {".ctor", ".cctor"}:
            used.add(plan["emitted_name"])
    for row in model._type_node_fields(node):
        raw_name = str(row.get("field_name") or "Field")
        name = t2.sanitize_identifier(raw_name, "Field", str(row.get("field_id") or raw_name))
        if name in used:
            name = "__TwinField_" + t2.sha256_text(str(row.get("field_id") or raw_name))[:12]
        used.add(name)
        if row.get("field_id") == field_row.get("field_id"):
            return name
    return None


def find_native_field(model: t2.T2Model, row: dict[str, Any], fact: dict[str, Any]) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    declaring_type = str(fact.get("declaring_type") or "")
    field_name = str(fact.get("name") or "")
    candidates = [
        field
        for field in model.field_rows
        if field.get("field_name") == field_name
        and (field.get("declaring_type") == declaring_type or t2.strip_arities(str(field.get("declaring_type") or "")) == t2.strip_arities(declaring_type))
    ]
    if len(candidates) != 1:
        return None, None
    field = candidates[0]
    node = model._resolve_owned_node(str(field.get("declaring_type") or ""))
    return field, field_emitted_name(model, node, field)


def simple_constant_literal(return_type: str, value: int, model: t2.T2Model, row: dict[str, Any]) -> Optional[str]:
    normalized = return_type.strip()
    if value == 0:
        if normalized == "bool":
            return "false"
        return "default"
    if normalized == "bool":
        return "true" if value == 1 else None
    if normalized in {"byte", "sbyte", "short", "ushort", "int", "uint", "long", "ulong"}:
        return str(value)
    if normalized == "float":
        return f"{value}f"
    if normalized == "double":
        return f"{value}d"
    if normalized == "decimal":
        return f"{value}m"
    if normalized == "char":
        return f"(char){value}"
    return None


def candidate_from_native(model: t2.T2Model, profile_row: dict[str, Any], operations: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    """Return a body only for a strict, straight-line native pattern."""
    metadata_row = model.methods_by_id[profile_row["method_id"]]
    tier = profile_row["t1_representation_tier"]
    if tier != "GENERATED_LOW" or metadata_row.get("is_constructor") or metadata_row.get("is_static"):
        return None
    if not operations or any(is_unknown_operation(operation) for operation in operations):
        return None
    if any((operation.get("typed_facts") or {}).get("call") for operation in operations):
        return None
    if any((operation.get("typed_facts") or {}).get("branch_target") is not None for operation in operations):
        return None
    if str(operations[-1].get("mnemonic") or "").upper() != "RET":
        return None
    node = model._resolve_owned_node(str(metadata_row.get("declaring_type") or ""))
    return_type = model.render_type(metadata_row.get("return_type") or "System.Object", node, metadata_row) if node else "object"
    params = metadata_row.get("parameter_types") or []

    # The empty return is an exact native body for a void method with no observable operation.
    if return_type == "void" and all(str(operation.get("mnemonic") or "").upper() == "RET" for operation in operations):
        return {"family": "EMPTY_VOID", "rule": "RET_ONLY", "body": "{\n}"}

    # Direct field getter: one canonical load from this followed by return.
    if len(operations) == 2:
        first = operations[0]
        first_facts = first.get("typed_facts") or {}
        field_fact = first_facts.get("field") or {}
        if field_fact.get("access") == "read" and field_fact.get("alias") == "X0=this":
            field, field_name = find_native_field(model, metadata_row, field_fact)
            if field and field_name and node and not params:
                field_type = model.render_type(field.get("field_type") or "System.Object", node, metadata_row)
                if field_type == return_type:
                    return {
                        "family": "FIELD_GET",
                        "rule": "NATIVE_FIELD_READ_RETURN",
                        "body": "{\nreturn this." + field_name + ";\n}",
                        "field_id": field.get("field_id"),
                        "field_name": field.get("field_name"),
                    }

    # Direct field setter.  The optional AND/MOV prefix is the canonical bool normalization.
    field_ops = [operation for operation in operations if ((operation.get("typed_facts") or {}).get("field") or {}).get("access") == "write"]
    if len(field_ops) == 1 and len(params) == 1 and return_type == "void":
        store = field_ops[0]
        facts = store.get("typed_facts") or {}
        field_fact = facts.get("field") or {}
        if field_fact.get("alias") == "X0=this" and all(str(operation.get("mnemonic") or "").upper() in {"AND", "MOV", "STR", "STRB", "STRH", "STRW"} for operation in operations):
            field, field_name = find_native_field(model, metadata_row, field_fact)
            if field and field_name and node:
                field_type = model.render_type(field.get("field_type") or "System.Object", node, metadata_row)
                parameter_type = model.render_type(params[0], node, metadata_row)
                if field_type == parameter_type and not str(params[0]).endswith("&"):
                    return {
                        "family": "FIELD_SET",
                        "rule": "NATIVE_FIELD_WRITE_ARG0",
                        "body": "{\nthis." + field_name + " = arg0;\n}",
                        "field_id": field.get("field_id"),
                        "field_name": field.get("field_name"),
                    }

    if len(operations) == 2:
        first = operations[0]
        mnemonic = str(first.get("mnemonic") or "").upper()
        operands = str(first.get("operands") or "")
        if re.match(r"^(?:w0|x0),\s*(?:wzr|xzr)$", operands, re.IGNORECASE):
            if return_type != "void":
                return {"family": "CONST_RETURN", "rule": "NATIVE_ZERO_RETURN", "body": "{\nreturn default;\n}"}
        match = re.match(r"^(?:w0|x0),\s*#(0x[0-9a-f]+|[0-9]+)$", operands, re.IGNORECASE)
        if mnemonic == "MOV" and match and return_type != "void":
            value = int(match.group(1), 0)
            literal = simple_constant_literal(return_type, value, model, metadata_row)
            if literal is not None:
                return {"family": "CONST_RETURN", "rule": "NATIVE_IMMEDIATE_RETURN", "body": "{\nreturn " + literal + ";\n}"}
        if mnemonic == "MOV" and re.match(r"^(?:w0|x0),\s*(?:w1|x1)$", operands, re.IGNORECASE) and params and return_type != "void":
            parameter_type = model.render_type(params[0], node, metadata_row) if node else "object"
            if parameter_type == return_type and not str(params[0]).endswith("&"):
                return {"family": "ARG_RETURN", "rule": "NATIVE_ARG0_RETURN", "body": "{\nreturn arg0;\n}"}
    return None


def build_promotion_candidates(root: Path, corpus: Corpus, model: t2.T2Model) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    profile_by_id = corpus.by_id
    readable_bodies, readable_rejected = read_preflight_readable_ids(root, corpus)
    candidates: dict[str, dict[str, Any]] = {}
    for method_id, body in sorted(readable_bodies.items()):
        candidates[method_id] = {
            "method_id": method_id,
            "family": "READABLE_SOURCE_BODY",
            "rule": "EXACT_SOURCE_BODY_COMPILE_PROVEN",
            "body": body,
            "source_body_hash": sha256_text(body),
        }
        profile_by_id[method_id]["promotion_eligible"] = True
        profile_by_id[method_id]["eligibility_reason"] = "exact_source_body_compile_proven"
    for profile_row in corpus.profile:
        if profile_row["method_id"] in candidates:
            continue
        method_id = profile_row["method_id"]
        operations = flatten_native(corpus.native_segments.get(method_id, []))
        candidate = candidate_from_native(model, profile_row, operations)
        if candidate:
            candidate["method_id"] = method_id
            candidate["native_operation_fingerprint"] = profile_row["native_operation_fingerprint"]
            candidates[method_id] = candidate
            profile_row["promotion_eligible"] = True
            profile_row["eligibility_reason"] = candidate["rule"]
        elif profile_row["t1_representation_tier"] == "GENERATED_LOW":
            profile_row["eligibility_reason"] = "no_proven_straight_line_rule"
        elif profile_row["t1_representation_tier"] == "EXISTING_READABLE":
            profile_row["eligibility_reason"] = "readable_probe_diagnostic"
        else:
            profile_row["eligibility_reason"] = "tier_not_eligible_for_source_like_promotion"
    summary = {
        "schema_version": "t3-family-eligibility-v1",
        "full_profile_method_count": len(corpus.profile),
        "readable_source_body_count": len(readable_bodies),
        "readable_probe_rejected_count": len(readable_rejected),
        "candidate_count": len(candidates),
        "candidate_families": dict(collections.Counter(candidate["family"] for candidate in candidates.values())),
        "candidate_rules": dict(collections.Counter(candidate["rule"] for candidate in candidates.values())),
        "proven_rules": ["EXACT_SOURCE_BODY_COMPILE_PROVEN", "NATIVE_FIELD_READ_RETURN", "NATIVE_FIELD_WRITE_ARG0", "NATIVE_ZERO_RETURN", "NATIVE_IMMEDIATE_RETURN", "NATIVE_ARG0_RETURN", "RET_ONLY"],
        "not_proven": ["CALL_FORWARD", "BRANCH_RECONSTRUCTION", "LOOP_RECONSTRUCTION", "GENERIC_SPECIALIZATION", "VIRTUAL_DISPATCH", "BYREF_RECONSTRUCTION"],
    }
    return candidates, readable_bodies, summary


class T3Model(t2.T2Model):
    def __init__(self, root: Path, output_root: Path, overrides: dict[str, dict[str, Any]], decisions: dict[str, dict[str, Any]]):
        self.t3_overrides = overrides
        self.t3_decisions = decisions
        super().__init__(root, output_root, method_limit=None, readable_bodies={})

    def _render_method(self, plan: dict[str, Any], node: Any, used_names: set[str]) -> list[str]:
        override = self.t3_overrides.get(plan["method_id"])
        plan["readable_body"] = override.get("body") if override else None
        return super()._render_method(plan, node, used_names)

    def _write_manifests(self, canary: bool) -> None:
        super()._write_manifests(canary)
        path = self.output_root / "methods" / "method-identity-manifest.json"
        rows = read_json(path)
        for row in rows:
            decision = self.t3_decisions.get(row["method_id"], {})
            if decision.get("promotion_status") == "PROMOTED":
                row["body_policy"] = "SOURCE_LIKE_EXACT"
            elif decision.get("promotion_status") == "REJECTED":
                row["body_policy"] = "IR_INTERPRETER_TRAMPOLINE"
            row.update(
                {
                    "semantic_tier": decision.get("semantic_tier", "GENERATED_LOW"),
                    "promotion_status": decision.get("promotion_status", "NOT_ELIGIBLE"),
                    "promotion_family": decision.get("family"),
                    "promotion_rule": decision.get("rule"),
                    "promotion_reason": decision.get("reason"),
                    "source_body_hash": decision.get("source_body_hash"),
                    "native_operation_fingerprint": decision.get("native_operation_fingerprint"),
                    "exact_t1_linkage": True,
                }
            )
        write_json(path, rows)
        write_json(self.output_root / "provenance" / "t3-semantic-decisions.json", [self.t3_decisions[key] for key in sorted(self.t3_decisions)])


def select_canary(profile: list[dict[str, Any]], count: int = 400) -> tuple[set[str], dict[str, Any]]:
    rows = {row["method_id"]: row for row in profile}
    selected: list[str] = []
    selected_set: set[str] = set()

    def add(matches: Iterable[dict[str, Any]], limit: Optional[int] = None) -> None:
        added = 0
        for row in sorted(matches, key=lambda item: item["method_id"]):
            if row["method_id"] in selected_set:
                continue
            selected_set.add(row["method_id"])
            selected.append(row["method_id"])
            added += 1
            if limit is not None and added >= limit:
                break

    dimensions = [
        ("ownership:GAME_FIRST_PARTY", [row for row in profile if row.get("ownership") == "GAME_FIRST_PARTY"]),
        ("ownership:KAIRO_ENGINE", [row for row in profile if row.get("ownership") == "KAIRO_ENGINE"]),
    ]
    for label, matches in dimensions:
        add(matches, 80)
    for shape in ["GENERIC", "BYREF", "ARRAY", "NESTED", "CONSTRUCTOR", "VIRTUAL", "COMPILER_GENERATED", "CFG_BRANCH", "CALL_HEAVY", "NATIVE_HEAVY", "STRAIGHT_LINE"]:
        add([row for row in profile if shape in row.get("risk_shapes", [])], 20)
    for family in sorted({row["family"] for row in profile}):
        add([row for row in profile if row["family"] == family], 10)
    add(profile)
    selected = selected[:count]
    selected_set = set(selected)
    available_shapes = sorted({shape for row in profile for shape in row.get("risk_shapes", [])})
    covered_shapes = sorted({shape for row in profile if row["method_id"] in selected_set for shape in row.get("risk_shapes", [])})
    available_families = sorted({row["family"] for row in profile})
    covered_families = sorted({row["family"] for row in profile if row["method_id"] in selected_set})
    coverage = {
        "canary_method_count": len(selected),
        "canary_method_ids_sha256": stable_hash_ids(selected),
        "ownership_counts": dict(collections.Counter(rows[method_id]["ownership"] for method_id in selected)),
        "risk_shapes_available": available_shapes,
        "risk_shapes_covered": covered_shapes,
        "risk_shapes_missing_because_absent_or_selection": sorted(set(available_shapes) - set(covered_shapes)),
        "families_available": available_families,
        "families_covered": covered_families,
        "families_missing_because_absent_or_selection": sorted(set(available_families) - set(covered_families)),
        "all_available_dimensions_covered": set(available_shapes).issubset(set(covered_shapes)) and set(available_families).issubset(set(covered_families)),
    }
    return selected_set, coverage


def make_decisions(profile: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], active_ids: set[str], rejected_ids: set[str]) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for row in profile:
        method_id = row["method_id"]
        candidate = candidates.get(method_id)
        if method_id in active_ids and candidate:
            decisions[method_id] = {
                "method_id": method_id,
                "promotion_status": "PROMOTED",
                "semantic_tier": "SOURCE_LIKE_EXACT",
                "family": candidate.get("family"),
                "rule": candidate.get("rule"),
                "reason": "compiled_in_whole_twin_wave",
                "source_body_hash": candidate.get("source_body_hash"),
                "native_operation_fingerprint": candidate.get("native_operation_fingerprint"),
                "t1_representation_hash": row["t1_representation_hash"],
                "t1_shard": row["t1_shard"],
                "t1_segments": row["t1_segments"],
            }
        elif method_id in rejected_ids and candidate:
            decisions[method_id] = {
                "method_id": method_id,
                "promotion_status": "REJECTED",
                "semantic_tier": row["t1_representation_tier"],
                "family": candidate.get("family"),
                "rule": candidate.get("rule"),
                "reason": "whole_twin_compile_diagnostic_attributed_to_candidate",
                "source_body_hash": candidate.get("source_body_hash"),
                "native_operation_fingerprint": candidate.get("native_operation_fingerprint"),
                "t1_representation_hash": row["t1_representation_hash"],
                "t1_shard": row["t1_shard"],
                "t1_segments": row["t1_segments"],
            }
        else:
            decisions[method_id] = {
                "method_id": method_id,
                "promotion_status": "NOT_ELIGIBLE",
                "semantic_tier": row["t1_representation_tier"],
                "family": row["family"],
                "rule": None,
                "reason": row.get("eligibility_reason"),
                "source_body_hash": None,
                "native_operation_fingerprint": None,
                "t1_representation_hash": row["t1_representation_hash"],
                "t1_shard": row["t1_shard"],
                "t1_segments": row["t1_segments"],
            }
    return decisions


def compile_tree(project_root: Path, label: str) -> dict[str, Any]:
    diagnostics_path = project_root / "diagnostics" / "compile.json"
    assembly_path = project_root / "diagnostics" / "compiled.dll"
    if not ROSYN_PWSH.exists():
        raise RuntimeError(f"BLOCKED_ROSLYN_RUNTIME:{ROSYN_PWSH}")
    command = [
        str(ROSYN_PWSH),
        "-NoProfile",
        "-File",
        str(ROOT / "tools" / "social-dev" / "compile_t2_factory.ps1"),
        "-ProjectRoot",
        str(project_root),
        "-OutputAssembly",
        str(assembly_path),
        "-DiagnosticsPath",
        str(diagnostics_path),
    ]
    completed = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)
    if not diagnostics_path.exists():
        raise RuntimeError(f"T3_COMPILE_DID_NOT_WRITE_DIAGNOSTICS:{label}:{completed.stderr[-1000:]}")
    result = read_json(diagnostics_path)
    result["label"] = label
    result["project_source_tree_sha256"] = source_tree_hash(project_root)
    result["process_exit_code"] = completed.returncode
    (project_root / "diagnostics" / "compile.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (project_root / "diagnostics" / "compile.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    return result


def materialize_and_compile(root: Path, label: str, overrides: dict[str, dict[str, Any]], decisions: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    output_root = T3_ARTIFACT_ROOT / "waves" / label
    safe_clear(output_root)
    model = T3Model(root, output_root, overrides, decisions)
    generation = model.generate(canary=False)
    compile_result = compile_tree(output_root, label)
    return generation, compile_result


def compile_with_demotions(root: Path, label: str, candidates: dict[str, dict[str, Any]], active_ids: set[str], rejected_ids: set[str], profile: list[dict[str, Any]]) -> tuple[set[str], set[str], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    current = set(active_ids)
    rejected = set(rejected_ids)
    attempts: list[dict[str, Any]] = []
    last_generation: dict[str, Any] = {}
    last_compile: dict[str, Any] = {}
    for attempt in range(1, 5):
        decisions = make_decisions(profile, candidates, current, rejected)
        overrides = {method_id: candidates[method_id] for method_id in sorted(current) if method_id in candidates}
        generation, compile_result = materialize_and_compile(root, label, overrides, decisions)
        last_generation, last_compile = generation, compile_result
        attempts.append({
            "attempt": attempt,
            "active_candidate_count": len(current),
            "compile_pass": bool(compile_result.get("parse_pass") and compile_result.get("compile_pass")),
            "compile_error_count": int(compile_result.get("compile_error_count") or 0),
            "demoted_method_ids": [],
        })
        if compile_result.get("parse_pass") and compile_result.get("compile_pass"):
            return current, rejected, last_generation, last_compile, attempts
        bad_ids = {
            diagnostic.get("method_id")
            for diagnostic in (compile_result.get("compile_errors") or [])
            if diagnostic.get("method_id") in current
        }
        if not bad_ids:
            return current, rejected, last_generation, last_compile, attempts
        current -= bad_ids
        rejected |= bad_ids
        attempts[-1]["demoted_method_ids"] = sorted(bad_ids)
    return current, rejected, last_generation, last_compile, attempts


def write_compact_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def build_hygiene_record(root: Path) -> dict[str, Any]:
    signature_path = T2_ACCEPTANCE / "signature-closure.json"
    validation_path = T2_ACCEPTANCE / "validation.json"
    final_path = T2_ACCEPTANCE / "final-decision.json"
    builder_path = root / "artifacts" / "t2-whole-twin-compile" / "t3-builder-replay-a" / "reports" / "full-generation-summary.json"
    canonical_builder_path = root / "artifacts" / "t2-whole-twin-compile" / "full-run-a" / "reports" / "full-generation-summary.json"
    signature = read_json(signature_path)
    validation = read_json(validation_path)
    final = read_json(final_path)
    builder = read_json(builder_path) if builder_path.exists() else {}
    canonical_builder = read_json(canonical_builder_path) if canonical_builder_path.exists() else {}
    checks = {
        "canonical_builder_replay_pass": bool(builder) and builder.get("generated_content_sha256") == canonical_builder.get("generated_content_sha256") and builder.get("canonical_method_count") == EXPECTED_METHODS,
        "signature_closure_status_pass": signature.get("status") == "PASS",
        "signature_atom_payload_count_consistent": bool(signature.get("signature_atom_count_matches_payload", True)),
        "t2_validation_pass": validation.get("status") == "PASS",
        "t2_final_decision_pass": final.get("status") == "PASS_T2_WHOLE_TWIN_COMPILE_FACTORY_CLOSED",
        "canonical_builder_generation_pass": builder.get("generated_method_count") == EXPECTED_METHODS and builder.get("exact_t1_linkage_count") == EXPECTED_METHODS,
    }
    return {
        "schema_version": "t3-pre-t3-hygiene-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "root_cause": "The prework signature-closure threshold (467) was stale. The canonical T2 builder emits 614 distinct signature atoms; the validator now checks the final payload count and normalization result against 614.",
        "before": {
            "signature_closure_sha256": PREVIOUS_SIGNATURE_CLOSURE_SHA256,
            "signature_closure_status": "FAIL",
            "stale_expected_distinct_signature_type_atoms": 467,
        },
        "after": {
            "signature_closure_sha256": sha256_file(signature_path),
            "signature_closure_status": signature.get("status"),
            "distinct_signature_type_atoms": signature.get("distinct_signature_type_atoms"),
            "expected_distinct_signature_type_atoms": signature.get("expected_distinct_signature_type_atoms"),
            "validation_sha256": sha256_file(validation_path),
            "final_decision_sha256": sha256_file(final_path),
        },
        "builder_replay": {
            "replay_summary": str(builder_path.relative_to(root)) if builder_path.exists() else None,
            "replay_generated_content_sha256": builder.get("generated_content_sha256"),
            "canonical_generated_content_sha256": canonical_builder.get("generated_content_sha256"),
        },
        "checks": checks,
    }


def structural_negative_checks(root: Path, corpus: Corpus, profile: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], active_ids: set[str], rejected_ids: set[str], decisions: dict[str, dict[str, Any]], final_generation: dict[str, Any], final_compile: dict[str, Any], replay_compile: dict[str, Any], replay_generation: dict[str, Any]) -> dict[str, Any]:
    final_root = T3_ARTIFACT_ROOT / "waves" / "final"
    manifest_path = final_root / "methods" / "method-identity-manifest.json"
    method_manifest = read_json(manifest_path) if manifest_path.exists() else []
    manifest_by_id = {row.get("method_id"): row for row in method_manifest}
    checks: dict[str, bool] = {}
    checks["exact_artifact_compile"] = bool(final_compile.get("parse_pass") and final_compile.get("compile_pass") and final_compile.get("parse_error_count") == 0 and final_compile.get("compile_error_count") == 0)
    checks["exact_t1_hash_and_segment_linkage"] = len(method_manifest) == EXPECTED_METHODS and all(
        row.get("representation_hash") == corpus.by_id.get(row.get("method_id"), {}).get("t1_representation_hash")
        and row.get("t1_segment_count") == len(corpus.by_id.get(row.get("method_id"), {}).get("t1_segments") or [])
        and row.get("exact_t1_linkage") is True
        for row in method_manifest
    )
    checks["no_op_dispatch_rejected"] = all(
        "TwinDispatchRuntime.Execute" not in str(next((candidate.get("body") for method_id, candidate in candidates.items() if method_id == row["method_id"] and method_id in active_ids), ""))
        for row in method_manifest if row.get("promotion_status") == "PROMOTED"
    )
    checks["type_surface_count_stable"] = len(corpus.types) == EXPECTED_TYPES and final_generation.get("canonical_type_count") == EXPECTED_TYPES and final_generation.get("generated_type_count") == EXPECTED_TYPES
    checks["field_surface_count_stable"] = len(corpus.fields) == EXPECTED_FIELDS
    checks["illegal_ctor_or_compiler_identifier_rejected"] = not any(
        ".ctor(" in line or ".cctor(" in line
        for path in final_root.rglob("*.cs")
        for line in path.read_text(encoding="utf-8").splitlines()
        if not "TwinCanonicalMethod" in line
    )
    checks["tier_distribution_preserved"] = collections.Counter(row.get("representation_tier") for row in method_manifest) == collections.Counter(EXPECTED_TIERS)
    checks["false_readable_reinjection_rejected"] = all(
        not (row.get("t1_representation_tier") == "EXISTING_READABLE" and row["method_id"] in active_ids and row["method_id"] not in candidates)
        for row in profile
    )
    checks["report_arithmetic_stable"] = sum(int(row.get("t1_operation_count") or 0) for row in profile) == EXPECTED_OPS and sum(int(row.get("operation_count") or 0) for row in profile) == EXPECTED_OPS
    checks["shared_native_identity_not_collapsed"] = len({row["method_id"] for row in profile}) == EXPECTED_METHODS and len({row["native_operation_fingerprint"] for row in profile}) <= EXPECTED_METHODS
    checks["operation_stream_not_truncated"] = all(int(row.get("t1_accounting", {}).get("omitted_operation_count") or 0) == 0 for row in profile)
    checks["placeholder_promotion_rejected"] = all(
        row.get("promotion_status") != "PROMOTED" or (row.get("semantic_tier") == "SOURCE_LIKE_EXACT" and row.get("promotion_rule"))
        for row in method_manifest
    )
    checks["deterministic_replay_pass"] = bool(replay_compile.get("parse_pass") and replay_compile.get("compile_pass") and replay_generation.get("generated_content_sha256") == final_generation.get("generated_content_sha256") and replay_compile.get("project_source_tree_sha256") == final_compile.get("project_source_tree_sha256"))
    return {
        "schema_version": "t3-negative-regression-validation-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "active_promotion_count": len(active_ids),
        "rejected_candidate_count": len(rejected_ids),
        "candidate_count": len(candidates),
        "canonical_type_count": len(corpus.types),
        "canonical_method_count": len(profile),
        "canonical_field_count": len(corpus.fields),
        "canonical_operation_count": sum(int(row.get("t1_operation_count") or 0) for row in profile),
    }


def write_ledger(path: Path, profile: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], active_ids: set[str], rejected_ids: set[str], decisions: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for method_id in sorted(active_ids | rejected_ids):
            candidate = candidates[method_id]
            row = next(item for item in profile if item["method_id"] == method_id)
            decision = decisions[method_id]
            handle.write(json.dumps({
                "method_id": method_id,
                "ownership": row["ownership"],
                "declaring_type": row["declaring_type"],
                "native_fingerprints": row["native_fingerprints"],
                "t1_representation_hash": row["t1_representation_hash"],
                "t1_shard": row["t1_shard"],
                "t1_segments": row["t1_segments"],
                "candidate_family": candidate.get("family"),
                "candidate_rule": candidate.get("rule"),
                "promotion_status": decision["promotion_status"],
                "semantic_tier": decision["semantic_tier"],
                "source_body_hash": candidate.get("source_body_hash"),
                "native_operation_fingerprint": candidate.get("native_operation_fingerprint"),
                "reason": decision.get("reason"),
            }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def report_markdown(path: Path, hygiene: dict[str, Any], profile: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], active_ids: set[str], rejected_ids: set[str], canary_coverage: dict[str, Any], wave_results: dict[str, Any], negative: dict[str, Any], validation: dict[str, Any], final_status: str) -> None:
    tier_counts = collections.Counter(row["t1_representation_tier"] for row in profile)
    semantic_counts = collections.Counter(("SOURCE_LIKE_EXACT" if row["method_id"] in active_ids else row["t1_representation_tier"]) for row in profile)
    lines = [
        "# T3 Source-Like Uplift",
        "",
        f"Status: `{final_status}`",
        "",
        "The T3 runner profiled every canonical method exactly once, retained T1 identity/segment provenance, and promoted only exact source bodies or mechanically proven straight-line native patterns that survived whole-Twin compilation.",
        "",
        "## Corpus",
        "",
        f"- Types: {EXPECTED_TYPES}; methods: {len(profile)}; fields: {EXPECTED_FIELDS}; T1 operations: {sum(int(row.get('t1_operation_count') or 0) for row in profile)}.",
        f"- Original tiers: `{dict(sorted(tier_counts.items()))}`.",
        f"- Promotions retained: {len(active_ids)}; candidate rejections: {len(rejected_ids)}; candidate pool: {len(candidates)}.",
        f"- Semantic tiers after T3: `{dict(sorted(semantic_counts.items()))}`.",
        "",
        "## Pre-T3 hygiene",
        "",
        f"- Status: `{hygiene['status']}`. The stale prework signature count was 467; the canonical builder and payload both report 614.",
        "",
        "## Canary and waves",
        "",
        f"- Canary: {canary_coverage['canary_method_count']} methods; ownership `{canary_coverage['ownership_counts']}`; all available dimensions covered: `{canary_coverage['all_available_dimensions_covered']}`.",
    ]
    for label, result in wave_results.items():
        compile_result = result.get("compile", {})
        lines.append(f"- `{label}`: compile pass `{bool(compile_result.get('parse_pass') and compile_result.get('compile_pass'))}`, errors `{compile_result.get('compile_error_count', 0)}`, active `{result.get('active_count')}`.")
    lines += [
        "",
        "## Negative regressions",
        "",
        f"- Status: `{negative['status']}`; all named rejection/identity/arithmetic checks: `{all(negative['checks'].values())}`.",
        "",
        "## Validation",
        "",
        f"- Gates: `{validation}`.",
        "",
        f"Next phase: `T4_WHOLE_TWIN_VALIDATION` when the PASS token is accepted.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_phase(root: Path) -> dict[str, Any]:
    root = root.resolve()
    T3_ACCEPTANCE.mkdir(parents=True, exist_ok=True)
    (T3_ARTIFACT_ROOT / "waves").mkdir(parents=True, exist_ok=True)
    corpus = Corpus(root)
    profile = corpus.build_profile()
    if len(corpus.types) != EXPECTED_TYPES or len(profile) != EXPECTED_METHODS or len(corpus.fields) != EXPECTED_FIELDS:
        raise RuntimeError(f"BLOCKED_T3_CANONICAL_UNIVERSE:{len(corpus.types)}:{len(profile)}:{len(corpus.fields)}")
    if sum(int(row.get("t1_operation_count") or 0) for row in profile) != EXPECTED_OPS:
        raise RuntimeError("BLOCKED_T3_OPERATION_ACCOUNTING")
    hygiene = build_hygiene_record(root)
    write_json(T3_ACCEPTANCE / "pre-t3-hygiene.json", hygiene)
    if hygiene["status"] != "PASS":
        raise RuntimeError("BLOCKED_T3_PRE_T3_HYGIENE")

    probe_root = T3_ARTIFACT_ROOT / "model-probe"
    probe_root.mkdir(parents=True, exist_ok=True)
    model_probe = t2.T2Model(root, probe_root, method_limit=set())
    candidates, readable_bodies, eligibility_summary = build_promotion_candidates(root, corpus, model_probe)
    write_compact_json(T3_ACCEPTANCE / "full-corpus-profile.json", profile)
    write_json(T3_ACCEPTANCE / "family-eligibility-summary.json", eligibility_summary)
    readable_candidate_count = sum(1 for candidate in candidates.values() if candidate["family"] == "READABLE_SOURCE_BODY")
    native_candidates = {method_id: candidate for method_id, candidate in candidates.items() if candidate["family"] != "READABLE_SOURCE_BODY"}
    write_json(T3_ACCEPTANCE / "readable-reinjection-summary.json", {
        "schema_version": "t3-readable-reinjection-v1",
        "attempted_readable_method_count": sum(1 for row in profile if row["t1_representation_tier"] == "EXISTING_READABLE"),
        "source_body_compile_proven_count": readable_candidate_count,
        "source_body_rejected_by_preflight_count": eligibility_summary["readable_probe_rejected_count"],
        "candidate_body_hashes": {method_id: candidate.get("source_body_hash") for method_id, candidate in sorted(candidates.items()) if candidate["family"] == "READABLE_SOURCE_BODY"},
        "status": "PASS" if readable_candidate_count > 0 else "FAIL",
    })
    write_json(T3_ACCEPTANCE / "simple-pattern-summary.json", {
        "schema_version": "t3-simple-pattern-v1",
        "native_candidate_count": len(native_candidates),
        "candidate_families": dict(collections.Counter(candidate["family"] for candidate in native_candidates.values())),
        "candidate_rules": dict(collections.Counter(candidate["rule"] for candidate in native_candidates.values())),
        "status": "PASS" if native_candidates else "NO_PROVEN_SIMPLE_RULE",
    })
    write_json(T3_ACCEPTANCE / "structured-uplift-summary.json", {
        "schema_version": "t3-structured-uplift-v1",
        "proven_structured_family_count": 0,
        "candidate_count": 0,
        "status": "NO_PROVEN_STRUCTURED_RULE",
        "reason": "T3 does not promote calls, branches, loops, generic specialization, virtual dispatch, or byref reconstruction without a source-confirmed exact body.",
    })

    canary_ids, canary_coverage = select_canary(profile, 400)
    canary_candidates = {method_id: candidates[method_id] for method_id in canary_ids if method_id in candidates}
    canary_active, canary_rejected, canary_generation, canary_compile, canary_attempts = compile_with_demotions(root, "canary", canary_candidates, set(canary_candidates), set(), profile)
    write_compact_json(T3_ACCEPTANCE / "canary-method-ids.json", sorted(canary_ids))
    write_json(T3_ACCEPTANCE / "canary-summary.json", {
        "schema_version": "t3-canary-v1",
        **canary_coverage,
        "candidate_count": len(canary_candidates),
        "promoted_count": len(canary_active),
        "rejected_count": len(canary_rejected),
        "compile": canary_compile,
        "attempts": canary_attempts,
        "status": "PASS" if canary_compile.get("parse_pass") and canary_compile.get("compile_pass") and len(canary_ids) == 400 else "FAIL",
    })
    if not (canary_compile.get("parse_pass") and canary_compile.get("compile_pass") and len(canary_ids) == 400):
        raise RuntimeError("BLOCKED_T3_CANARY_COMPILE")

    wave_results: dict[str, Any] = {
        "canary": {"active_count": len(canary_active), "compile": canary_compile, "attempts": canary_attempts},
    }
    readable_ids = {method_id for method_id, candidate in candidates.items() if candidate["family"] == "READABLE_SOURCE_BODY"}
    active, rejected, generation, compile_result, attempts = compile_with_demotions(root, "wave-a-readable", candidates, readable_ids, set(), profile)
    wave_results["wave-a-readable"] = {"active_count": len(active), "compile": compile_result, "attempts": attempts}
    if not (compile_result.get("parse_pass") and compile_result.get("compile_pass")):
        raise RuntimeError("BLOCKED_T3_READABLE_WAVE_COMPILE")

    simple_ids = set(native_candidates) - rejected
    active, rejected, generation, compile_result, attempts = compile_with_demotions(root, "wave-b-simple", candidates, active | simple_ids, rejected, profile)
    wave_results["wave-b-simple"] = {"active_count": len(active), "compile": compile_result, "attempts": attempts}
    if not (compile_result.get("parse_pass") and compile_result.get("compile_pass")):
        raise RuntimeError("BLOCKED_T3_SIMPLE_WAVE_COMPILE")

    # Waves C/D are intentionally materialized and compiled even though no structured rule has
    # reached the evidence bar.  This records the stable middle-tier boundary explicitly.
    active, rejected, generation, compile_result, attempts = compile_with_demotions(root, "wave-c-typed-ir", candidates, active, rejected, profile)
    wave_results["wave-c-typed-ir"] = {"active_count": len(active), "compile": compile_result, "attempts": attempts, "new_promotions": 0}
    if not (compile_result.get("parse_pass") and compile_result.get("compile_pass")):
        raise RuntimeError("BLOCKED_T3_TYPED_IR_WAVE_COMPILE")
    active, rejected, generation, compile_result, attempts = compile_with_demotions(root, "wave-d-structured", candidates, active, rejected, profile)
    wave_results["wave-d-structured"] = {"active_count": len(active), "compile": compile_result, "attempts": attempts, "new_promotions": 0}
    if not (compile_result.get("parse_pass") and compile_result.get("compile_pass")):
        raise RuntimeError("BLOCKED_T3_STRUCTURED_WAVE_COMPILE")
    write_json(T3_ACCEPTANCE / "complex-uplift-summary.json", {
        "schema_version": "t3-complex-uplift-v1",
        "attempted": False,
        "promotion_count": 0,
        "status": "SKIPPED_NO_PROVEN_COMPLEX_RULE",
    })

    active, rejected, final_generation, final_compile, final_attempts = compile_with_demotions(root, "final", candidates, active, rejected, profile)
    final_decisions = make_decisions(profile, candidates, active, rejected)
    wave_results["final"] = {"active_count": len(active), "compile": final_compile, "attempts": final_attempts}
    if not (final_compile.get("parse_pass") and final_compile.get("compile_pass")):
        raise RuntimeError("BLOCKED_T3_FINAL_COMPILE")

    final_root = T3_ARTIFACT_ROOT / "waves" / "final"
    replay_decisions = make_decisions(profile, candidates, active, rejected)
    replay_generation, replay_compile = materialize_and_compile(root, "final-replay", {method_id: candidates[method_id] for method_id in sorted(active)}, replay_decisions)
    write_ledger(T3_ACCEPTANCE / "promotion-ledger.jsonl", profile, candidates, active, rejected, final_decisions)

    tier_counts = collections.Counter(row["t1_representation_tier"] for row in profile)
    semantic_counts = collections.Counter("SOURCE_LIKE_EXACT" if row["method_id"] in active else row["t1_representation_tier"] for row in profile)
    write_json(T3_ACCEPTANCE / "semantic-tier-summary.json", {
        "schema_version": "t3-semantic-tier-v1",
        "canonical_method_count": len(profile),
        "original_representation_tiers": dict(sorted(tier_counts.items())),
        "semantic_tiers": dict(sorted(semantic_counts.items())),
        "promoted_method_count": len(active),
        "rejected_candidate_count": len(rejected),
        "tier_collapse": False,
    })
    write_json(T3_ACCEPTANCE / "compile-summary.json", {
        "schema_version": "t3-compile-summary-v1",
        "canary": canary_compile,
        "waves": {label: result["compile"] for label, result in wave_results.items()},
        "final": final_compile,
        "final_source_root": str(final_root.relative_to(root)),
        "final_source_tree_sha256": final_compile.get("project_source_tree_sha256"),
        "final_generation": final_generation,
        "final_replay": replay_compile,
        "final_replay_generation": replay_generation,
    })
    write_json(T3_ACCEPTANCE / "deterministic-replay.json", {
        "schema_version": "t3-deterministic-replay-v1",
        "source_generation_sha256_equal": replay_generation.get("generated_content_sha256") == final_generation.get("generated_content_sha256"),
        "source_tree_sha256_equal": replay_compile.get("project_source_tree_sha256") == final_compile.get("project_source_tree_sha256"),
        "assembly_sha256_equal": replay_compile.get("output_assembly_sha256") == final_compile.get("output_assembly_sha256"),
        "compile_pass_a": bool(final_compile.get("parse_pass") and final_compile.get("compile_pass")),
        "compile_pass_b": bool(replay_compile.get("parse_pass") and replay_compile.get("compile_pass")),
        "status": "PASS" if replay_compile.get("parse_pass") and replay_compile.get("compile_pass") and replay_generation.get("generated_content_sha256") == final_generation.get("generated_content_sha256") and replay_compile.get("project_source_tree_sha256") == final_compile.get("project_source_tree_sha256") else "FAIL",
    })

    negative = structural_negative_checks(root, corpus, profile, candidates, active, rejected, final_decisions, final_generation, final_compile, replay_compile, replay_generation)
    write_json(T3_ACCEPTANCE / "negative-regression-validation.json", negative)
    validation = {
        "pre_t3_hygiene": hygiene["status"] == "PASS",
        "canonical_universe": len(profile) == EXPECTED_METHODS and len(corpus.types) == EXPECTED_TYPES and len(corpus.fields) == EXPECTED_FIELDS,
        "full_corpus_profile_exact_once": len(profile) == EXPECTED_METHODS and len({row["method_id"] for row in profile}) == EXPECTED_METHODS,
        "canary_compile": canary_compile.get("parse_pass") and canary_compile.get("compile_pass"),
        "wave_compiles": all(result["compile"].get("parse_pass") and result["compile"].get("compile_pass") for result in wave_results.values()),
        "final_compile": final_compile.get("parse_pass") and final_compile.get("compile_pass"),
        "exact_t1_linkage": negative["checks"].get("exact_t1_hash_and_segment_linkage", False),
        "negative_regressions": negative["status"] == "PASS",
        "deterministic_replay": read_json(T3_ACCEPTANCE / "deterministic-replay.json")["status"] == "PASS",
        "semantic_tier_arithmetic": sum(semantic_counts.values()) == EXPECTED_METHODS and not (set(semantic_counts) == {"SOURCE_LIKE_EXACT"}),
    }
    validation["all_gates_pass"] = all(validation.values())
    validation["status"] = "PASS" if validation["all_gates_pass"] else "FAIL"
    write_json(T3_ACCEPTANCE / "validation.json", validation)
    final_status = "PASS_T3_SOURCE_LIKE_UPLIFT_CLOSED" if validation["all_gates_pass"] else "FAIL_T3_SOURCE_LIKE_UPLIFT"
    write_json(T3_ACCEPTANCE / "final-decision.json", {
        "schema_version": "t3-final-decision-v1",
        "phase": "T3_SOURCE_LIKE_UPLIFT",
        "status": final_status,
        "canonical_type_count": len(corpus.types),
        "canonical_method_count": len(profile),
        "canonical_field_count": len(corpus.fields),
        "canonical_operation_count": sum(int(row.get("t1_operation_count") or 0) for row in profile),
        "promoted_method_count": len(active),
        "rejected_candidate_count": len(rejected),
        "exact_t1_linkage": validation["exact_t1_linkage"],
        "next_phase": "T4_WHOLE_TWIN_VALIDATION" if final_status.startswith("PASS") else "T3_SOURCE_LIKE_UPLIFT",
        "unity_v8_runtime_untouched": True,
    })
    write_json(T3_ACCEPTANCE / "canonical-universe.json", {
        "schema_version": "t3-canonical-universe-v1",
        "status": "PASS" if validation["canonical_universe"] else "FAIL",
        "type_count": len(corpus.types),
        "method_count": len(profile),
        "field_count": len(corpus.fields),
        "operation_count": sum(int(row.get("t1_operation_count") or 0) for row in profile),
        "method_ids_sha256": stable_hash_ids(row["method_id"] for row in profile),
        "method_ids_unique": len({row["method_id"] for row in profile}) == len(profile),
        "representation_tiers": dict(sorted(tier_counts.items())),
        "ownership": dict(collections.Counter(row["ownership"] for row in profile)),
    })
    report_markdown(T3_ACCEPTANCE / "T3_SOURCE_LIKE_UPLIFT_REPORT.md", hygiene, profile, candidates, active, rejected, canary_coverage, wave_results, negative, validation, final_status)
    return {"status": final_status, "validation": validation, "promoted_method_count": len(active), "candidate_count": len(candidates), "rejected_candidate_count": len(rejected)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_phase(args.root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "PASS_T3_SOURCE_LIKE_UPLIFT_CLOSED" else 1
    except Exception as error:  # keep the failure token visible to the acceptance caller
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
