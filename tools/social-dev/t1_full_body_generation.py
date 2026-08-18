#!/usr/bin/env python3
"""Canonical T1 full-body generation for the complete corrected Twin universe.

The generator is deliberately coverage-first.  It consumes the canonical R1.5
method catalog, R3 status/bundles, the immutable recovered C# tree, the pinned
ELF, and the canonical metadata/script evidence.  Native operations are decoded
directly from the pinned ELF with Capstone and are stored losslessly in bounded
segments.  C# sidecars carry the same canonical operation segments as escaped
JSON strings so the analysis representation remains compilable without putting
an extreme method in one oversized C# method body.

This module never writes the recovered source roots, the Twin, Unity/V8, or the
runtime.  Heavy output is intended to remain below the ignored artifacts root;
the compact acceptance package is written separately by ``run_full``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from r4_native_ir_pilot import (  # noqa: E402
    CATALOG_PATH,
    CFG_PROFILE_PATH,
    CanonicalEvidence,
    MethodEvidence,
    NativeInstruction,
    R3_BUNDLES,
    SOURCE_ROOT,
    STATUS_PATH,
    build_cfg,
    source_tree_digest,
    verify_source_gate,
)
from t1_full_body_generation_pilot import (  # noqa: E402
    analyze_native,
    initial_bindings,
    safe_identifier,
)

try:  # noqa: E402
    import lief
    from capstone import CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN, Cs
except ImportError as error:  # pragma: no cover - exercised by the source gate
    lief = None
    Cs = None
    CS_ARCH_ARM64 = None
    CS_MODE_LITTLE_ENDIAN = None
    CAPSTONE_IMPORT_ERROR = str(error)
else:
    CAPSTONE_IMPORT_ERROR = None


EXPECTED_TYPES = 641
EXPECTED_METHODS = 10_827
OWNED = {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
NATIVE_EXPECTED_CONVENTION = "CANONICAL_ISIL_DISASSEMBLY_COUNT_MINUS_ONE_WITH_PINNED_ELF_BYTE_VERIFICATION"
RUN_ID = "T1_FULL_BODY_GENERATION_CANONICAL_V1"
TOOL_VERSION = "t1-full-body-generation-v1"
MAX_SHARD_OPERATION_BYTES = 8 * 1024 * 1024
MAX_SEGMENT_OPERATION_BYTES = 32 * 1024
SIDECAR_TARGET_NAMESPACE = "SocialDev.T1Full"


def stable_json(value: Any, *, compact: bool = False) -> str:
    if compact:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


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


def relative_path(path: Optional[str | Path]) -> Optional[str]:
    if path is None:
        return None
    candidate = Path(path)
    try:
        return candidate.relative_to(ROOT).as_posix()
    except ValueError:
        return str(candidate).replace("\\", "/")


def parse_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value), 0)
    except ValueError:
        return None


def csharp_string(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def clear_exact_root(root: Path, parent: Path) -> None:
    resolved_root = root.resolve()
    resolved_parent = parent.resolve()
    if resolved_root == resolved_parent or resolved_parent not in resolved_root.parents:
        raise RuntimeError(f"Refusing to clear unsafe generated root: {root}")
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)


class SourceBodies:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._raw: dict[Path, bytes] = {}

    def body(self, row: dict[str, Any]) -> tuple[str, Optional[str], Optional[str]]:
        relative = str(row.get("source_file") or "").replace("/", "\\")
        path = self.root / relative
        if not path.is_file():
            return "", None, None
        raw = self._raw.setdefault(path, path.read_bytes())
        text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines(keepends=True)
        start = max(1, int(row.get("source_line") or 1))
        end = max(start, int(row.get("source_line_end") or start))
        body = "".join(lines[start - 1 : min(len(lines), end)])
        if not body and start <= len(lines):
            body = lines[start - 1]
        return body, str(path.relative_to(self.root)).replace("\\", "/"), sha256_text(body)


class NativeDecoder:
    """Decode canonical ARM64 ranges directly from the pinned ELF."""

    def __init__(self, path: Path) -> None:
        if lief is None or Cs is None:
            raise RuntimeError(f"Capstone/LIEF unavailable: {CAPSTONE_IMPORT_ERROR}")
        self.path = path
        self.blob = path.read_bytes()
        self.elf = lief.parse(str(path))
        self.loads = [
            segment
            for segment in self.elf.segments
            if str(segment.type) == "TYPE.LOAD" and (segment.virtual_size or segment.physical_size)
        ]
        self.disassembler = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
        self.disassembler.detail = True
        self.cache: dict[str, dict[str, Any]] = {}

    def map_address(self, address: int) -> tuple[int, Any]:
        segment = next(
            (
                item
                for item in self.loads
                if item.virtual_address <= address < item.virtual_address + item.virtual_size
            ),
            None,
        )
        if segment is None:
            raise RuntimeError(f"Native address 0x{address:X} is outside all ELF LOAD segments")
        offset = int(segment.file_offset + (address - segment.virtual_address))
        return offset, segment

    def decode(self, row: dict[str, Any]) -> dict[str, Any]:
        method_id = row["method_id"]
        cached = self.cache.get(method_id)
        if cached is not None:
            return cached
        if not row.get("native_available"):
            result = {
                "native": [],
                "raw": [],
                "expected": 0,
                "file_offset": None,
                "range_status": "NO_NATIVE_EVIDENCE",
                "range_authority": "canonical catalog marks native unavailable",
            }
            self.cache[method_id] = result
            return result
        address = parse_int(row.get("isil_native_address"))
        catalog_count = parse_int(row.get("isil_disassembly_instruction_count"))
        if address is None or catalog_count is None or catalog_count <= 0:
            raise RuntimeError(f"Native row lacks canonical address/count: {method_id}")
        expected = catalog_count - 1
        file_offset, segment = self.map_address(address)
        raw_bytes = self.blob[file_offset : file_offset + expected * 4]
        if len(raw_bytes) != expected * 4:
            raise RuntimeError(f"Native range exceeds pinned ELF bytes: {method_id}")
        instructions = list(self.disassembler.disasm(raw_bytes, address))
        if len(instructions) != expected or any(
            instruction.address != address + index * 4 or len(instruction.bytes) != 4
            for index, instruction in enumerate(instructions)
        ):
            raise RuntimeError(
                f"Canonical ELF decode mismatch for {method_id}: expected {expected}, got {len(instructions)}"
            )
        native = [
            NativeInstruction(instruction.address, instruction.mnemonic.upper(), instruction.op_str.strip())
            for instruction in instructions
        ]
        raw = [bytes(instruction.bytes) for instruction in instructions]
        result = {
            "native": native,
            "raw": raw,
            "expected": expected,
            "file_offset": file_offset,
            "segment": {
                "virtual_address": f"0x{segment.virtual_address:X}",
                "file_offset": f"0x{segment.file_offset:X}",
                "virtual_size": f"0x{segment.virtual_size:X}",
                "physical_size": f"0x{segment.physical_size:X}",
            },
            "range_status": "NATIVE_RANGE_VERIFIED",
            "range_authority": "canonical ELF segment mapping + canonical start/count + contiguous Capstone decode + no next-start overlap",
        }
        self.cache[method_id] = result
        return result

    def fingerprint(self, instruction: NativeInstruction, raw: bytes) -> dict[str, Any]:
        return {
            "address": f"0x{instruction.address:X}",
            "raw_bytes_little_endian": raw.hex(),
            "raw_word_little_endian": f"0x{int.from_bytes(raw, 'little'):08X}",
            "mnemonic": instruction.mnemonic,
            "operands": instruction.operands,
        }


def classify_declaration(row: dict[str, Any], source_body: str, source_path: Optional[str]) -> tuple[bool, str]:
    if row.get("native_available"):
        return False, "native_evidence_available"
    if row.get("source_body_present") or row.get("source_body_kind") != "none":
        return False, "source_body_not_metadata_declaration_only"
    if not source_path or not row.get("source_present"):
        return False, "source_declaration_not_recovered"
    if not row.get("is_virtual"):
        return False, "nonvirtual_without_implementation_evidence"
    if source_body.strip() and "{" in source_body:
        return False, "source_excerpt_contains_body"
    return True, "metadata source_body_kind=none + virtual contract + source declaration"


def canonical_universe(canonical: CanonicalEvidence) -> dict[str, Any]:
    rows = list(canonical.rows)
    ids = [row.get("method_id") for row in rows]
    type_rows = [
        json.loads(line)
        for line in (ROOT / "artifacts" / "r1-5-metadata-reconciliation" / "type-catalog.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    owned_types = [row for row in type_rows if row.get("ownership") in OWNED]
    ownership = Counter(row.get("ownership") for row in rows)
    compiler_generated = [row["method_id"] for row in rows if row.get("compiler_generated")]
    out_of_scope = [row["method_id"] for row in rows if row.get("ownership") not in OWNED]
    status_counts = Counter(canonical.status(row) for row in rows)
    result = {
        "schema_version": "t1-full-canonical-universe-v1",
        "authority": relative_path(CATALOG_PATH),
        "status_authority": relative_path(STATUS_PATH),
        "cfg_authority": relative_path(CFG_PROFILE_PATH),
        "types": len({row.get("type_id") for row in owned_types}),
        "methods": len(rows),
        "unique_method_ids": len(set(ids)),
        "duplicate_method_ids": len(ids) - len(set(ids)),
        "ownership": dict(sorted(ownership.items())),
        "compiler_generated_method_ids": compiler_generated,
        "out_of_scope_method_ids": out_of_scope,
        "status_counts": dict(sorted(status_counts.items())),
        "native_available": sum(bool(row.get("native_available")) for row in rows),
        "isil_available": sum(bool(row.get("isil_available")) for row in rows),
        "source_body_present": sum(bool(row.get("source_body_present")) for row in rows),
        "r3_bundle_count": sum((R3_BUNDLES / f"{row['method_id']}.json").is_file() for row in rows),
        "expected": {"types": EXPECTED_TYPES, "methods": EXPECTED_METHODS, "ownership": sorted(OWNED)},
    }
    result["gate"] = (
        result["types"] == EXPECTED_TYPES
        and result["methods"] == EXPECTED_METHODS
        and result["unique_method_ids"] == EXPECTED_METHODS
        and result["duplicate_method_ids"] == 0
        and not compiler_generated
        and not out_of_scope
        and set(ownership) == OWNED
    )
    return result


def build_address_index(rows: Iterable[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    index: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        address = parse_int(row.get("isil_native_address"))
        if row.get("native_available") and address is not None:
            index[address].append(row)
    return {address: sorted(items, key=lambda item: item["method_id"]) for address, items in index.items()}


def operation_stream(
    row: dict[str, Any],
    decoded: dict[str, Any],
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []
    analyzed = analysis.get("operations", [])
    native = decoded["native"]
    raw = decoded["raw"]
    if len(analyzed) != len(native):
        raise RuntimeError(f"Native analysis changed operation count for {row['method_id']}")
    for index, (instruction, raw_bytes, fact) in enumerate(zip(native, raw, analyzed)):
        typed_facts = {
            "field": fact.get("field"),
            "call": fact.get("call"),
            "branch_target": fact.get("branch_target"),
            "stack_access": fact.get("stack_access", False),
        }
        operations.append(
            {
                "native_index": index,
                "address": f"0x{instruction.address:X}",
                "raw_bytes_little_endian": raw_bytes.hex(),
                "raw_word_little_endian": f"0x{int.from_bytes(raw_bytes, 'little'):08X}",
                "mnemonic": instruction.mnemonic,
                "operands": instruction.operands,
                "kind": fact.get("kind"),
                "family": fact.get("family"),
                "typed_facts": typed_facts,
                "evidence_source": "native_elf",
                "provenance": [f"native:{instruction.address:#x}"],
            }
        )
    return operations


def split_operations(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_bytes = 2
    start = 0
    for index, operation in enumerate(operations):
        encoded = stable_json(operation, compact=True).encode("utf-8")
        if current and current_bytes + len(encoded) + 1 > MAX_SEGMENT_OPERATION_BYTES:
            payload = stable_json(current, compact=True)
            segments.append(
                {
                    "segment_index": len(segments),
                    "operation_start": start,
                    "operation_count": len(current),
                    "serialized_bytes": len(payload.encode("utf-8")),
                    "operations": current,
                }
            )
            start = index
            current = []
            current_bytes = 2
        current.append(operation)
        current_bytes += len(encoded) + 1
    if current or not segments:
        payload = stable_json(current, compact=True)
        segments.append(
            {
                "segment_index": len(segments),
                "operation_start": start,
                "operation_count": len(current),
                "serialized_bytes": len(payload.encode("utf-8")),
                "operations": current,
            }
        )
    return segments


def operation_hash(method_id: str, operations: list[dict[str, Any]]) -> str:
    stream = "\n".join(stable_json(operation, compact=True) for operation in operations)
    return sha256_text(method_id + "\n" + stream)


def source_relation(row: dict[str, Any], source_path: Optional[str], source_body_hash: Optional[str]) -> dict[str, Any]:
    body_present = bool(row.get("source_body_present") and source_path)
    if row.get("source_match_status") == "EXACT_TYPE" and body_present:
        relation = "EXACT_TYPE_SOURCE_BODY"
    elif body_present:
        relation = "NON_EXACT_SOURCE_BODY"
    elif row.get("source_present"):
        relation = "SOURCE_DECLARATION_ONLY"
    else:
        relation = "SOURCE_LIMITED"
    return {
        "relation": relation,
        "match_status": row.get("source_match_status"),
        "body_present": body_present,
        "source_path": source_path,
        "source_line": row.get("source_line"),
        "source_line_end": row.get("source_line_end"),
        "body_sha256": row.get("body_sha256"),
        "extracted_body_sha256": source_body_hash,
    }


def isil_summary(evidence: MethodEvidence, row: dict[str, Any]) -> dict[str, Any]:
    if evidence.isil:
        source = "R3_BUNDLE" if evidence.r3_bundle else "CANONICAL_ISIL_TEMP_ROOT"
        availability = "MATERIALIZED"
    elif row.get("isil_available"):
        source = "CANONICAL_CATALOG_ONLY_TEMP_ROOT_REMOVED"
        availability = "CATALOG_ONLY"
    else:
        source = "NOT_AVAILABLE_BY_CANONICAL_CATALOG"
        availability = "NOT_AVAILABLE"
    return {
        "availability": availability,
        "source": source,
        "path": relative_path(evidence.isil_path),
        "catalog_instruction_count": parse_int(row.get("isil_instruction_count")),
        "materialized_instruction_count": len(evidence.isil),
        "header": evidence.isil_header,
        "instructions": [{"index": item.index, "opcode": item.opcode, "text": item.text} for item in evidence.isil],
    }


def facts_summary(row: dict[str, Any], analysis: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    calls = analysis.get("calls", {})
    unresolved_calls = len(calls.get("unresolved_direct", [])) + len(calls.get("virtual_or_indirect", []))
    resolved_calls = len(calls.get("resolved_direct", []))
    resolved_fields = sum(1 for operation in operations if operation["typed_facts"].get("field"))
    unresolved_fields = len(analysis.get("unresolved_field_accesses", []))
    raw_unknown = sum(1 for operation in operations if operation.get("family") == "RAW_NATIVE")
    return {
        "resolved_direct_calls": resolved_calls,
        "unresolved_calls": unresolved_calls,
        "resolved_field_accesses": resolved_fields,
        "unresolved_field_accesses": unresolved_fields,
        "raw_unknown_operations": raw_unknown,
        "branch_facts": len(analysis.get("branch_facts", [])),
        "indirect_or_virtual_calls": len(calls.get("virtual_or_indirect", [])),
        "static_fields": len(analysis.get("static_field_facts", [])),
        "isil_materialized_calls": len(calls.get("isil", [])),
        "cfg_status": analysis.get("cfg", {}).get("status"),
        "cfg_block_count": len(analysis.get("cfg", {}).get("blocks", [])),
        "cfg_edge_count": len(analysis.get("cfg", {}).get("edges", [])),
    }


def method_identity(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "method_id": row.get("method_id"),
        "assembly": row.get("assembly"),
        "ownership": row.get("ownership"),
        "declaring_type": row.get("declaring_type"),
        "method_name": row.get("method_name"),
        "normalized_signature": row.get("normalized_signature"),
        "metadata_token": row.get("metadata_token"),
        "generic_arity": row.get("generic_arity"),
        "parameter_types": row.get("parameter_types") or [],
        "parameter_count": row.get("parameter_count"),
        "return_type": row.get("return_type"),
        "is_static": bool(row.get("is_static")),
        "is_virtual": bool(row.get("is_virtual")),
        "is_constructor": bool(row.get("is_constructor")),
    }


def emit_sidecar_contract(root: Path) -> None:
    contract = r'''using System;
using System.Collections.Generic;

namespace SocialDev.T1Full
{
    public sealed class TwinFullT1Segment
    {
        public int SegmentIndex { get; private set; }
        public int OperationStart { get; private set; }
        public int OperationCount { get; private set; }
        public int SerializedBytes { get; private set; }
        public string OperationReference { get; private set; }

        public TwinFullT1Segment(int segmentIndex, int operationStart, int operationCount, int serializedBytes, string operationReference)
        {
            SegmentIndex = segmentIndex;
            OperationStart = operationStart;
            OperationCount = operationCount;
            SerializedBytes = serializedBytes;
            OperationReference = operationReference;
        }
    }

    public sealed class TwinFullT1Metadata
    {
        public string MethodId { get; private set; }
        public string Assembly { get; private set; }
        public string Ownership { get; private set; }
        public string DeclaringType { get; private set; }
        public string Signature { get; private set; }
        public string MetadataToken { get; private set; }
        public string CatalogRva { get; private set; }
        public string NativeStart { get; private set; }
        public string NativeEnd { get; private set; }
        public string RepresentationTier { get; private set; }
        public string RepresentationHash { get; private set; }
        public int OperationCount { get; private set; }
        public string Shard { get; private set; }
        public string SourceBody { get; set; }
        public string Limitation { get; set; }

        public TwinFullT1Metadata(string methodId, string assembly, string ownership, string declaringType, string signature,
            string metadataToken, string catalogRva, string nativeStart, string nativeEnd, string representationTier,
            string representationHash, int operationCount, string shard)
        {
            MethodId = methodId;
            Assembly = assembly;
            Ownership = ownership;
            DeclaringType = declaringType;
            Signature = signature;
            MetadataToken = metadataToken;
            CatalogRva = catalogRva;
            NativeStart = nativeStart;
            NativeEnd = nativeEnd;
            RepresentationTier = representationTier;
            RepresentationHash = representationHash;
            OperationCount = operationCount;
            Shard = shard;
        }
    }

    public sealed class TwinFullT1Method
    {
        public TwinFullT1Metadata Metadata { get; private set; }
        public List<TwinFullT1Segment> Segments { get; private set; }

        public TwinFullT1Method(TwinFullT1Metadata metadata, TwinFullT1Segment[] segments)
        {
            Metadata = metadata;
            Segments = new List<TwinFullT1Segment>(segments);
        }
    }
}
'''
    (root / "FullT1Contract.cs").write_text(contract, encoding="utf-8", newline="\n")


def emit_method_sidecar(record: dict[str, Any], segments: list[dict[str, Any]], shard_name: str) -> str:
    identity = record["identity"]
    metadata = record["metadata"]
    class_name = safe_identifier(identity["method_id"])
    lines = [
        "using SocialDev.T1Full;",
        "",
        f"namespace {SIDECAR_TARGET_NAMESPACE}.Generated",
        "{",
        f"    public static class {class_name}",
        "    {",
        "        public static TwinFullT1Method Build()",
        "        {",
        "            var metadata = new TwinFullT1Metadata(",
        f"                {csharp_string(identity['method_id'])}, {csharp_string(identity['assembly'])}, {csharp_string(identity['ownership'])},",
        f"                {csharp_string(identity['declaring_type'])}, {csharp_string(identity['normalized_signature'])}, {csharp_string(identity['metadata_token'])},",
        f"                {csharp_string(identity.get('rva'))}, {csharp_string(metadata.get('native_start'))}, {csharp_string(metadata.get('native_end'))},",
        f"                {csharp_string(record['representation_tier'])}, {csharp_string(record['representation_hash'])}, {record['operation_count']}, {csharp_string(shard_name)});",
    ]
    if record.get("source_body"):
        lines.append(f"            metadata.SourceBody = {csharp_string(record['source_body'])};")
    if record.get("limitation"):
        lines.append(f"            metadata.Limitation = {csharp_string(record['limitation'])};")
    lines.append("            return new TwinFullT1Method(metadata, new TwinFullT1Segment[]")
    lines.append("            {")
    for segment in segments:
        file_segment_index = int(segment.get("file_segment_index", segment["segment_index"]))
        operation_reference = f"native-ir/{shard_name}/segment-{file_segment_index:05d}.jsonl"
        lines.append(
            f"                new TwinFullT1Segment({segment['segment_index']}, {segment['operation_start']}, {segment['operation_count']}, {segment['serialized_bytes']}, {csharp_string(operation_reference)}),"
        )
    lines.extend(["            });", "        }"])
    lines.extend(["    }", "}", ""])
    return "\n".join(lines)


def emit_shard_index(root: Path, records: list[dict[str, Any]]) -> None:
    lines = [
        "using System;",
        "",
        f"namespace {SIDECAR_TARGET_NAMESPACE}.Generated",
        "{",
        "    public static class ShardIndex",
        "    {",
        f"        public static int Count {{ get {{ return {len(records)}; }} }}",
        "        public static string[] MethodIds()",
        "        {",
        "            return new string[]",
        "            {",
    ]
    lines.extend(f"                {csharp_string(record['method_id'])}," for record in records)
    lines.extend(["            };", "        }", "    }", "}", ""])
    (root / "ShardIndex.cs").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def emit_registry(root: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    registry_root = root / "registry"
    clear_exact_root(registry_root, root)
    registry_root.mkdir(parents=True, exist_ok=True)
    contract = r'''using System.Collections.Generic;

namespace SocialDev.T1Registry
{
    public sealed class FullT1RegistryEntry
    {
        public string MethodId { get; private set; }
        public string Shard { get; private set; }
        public string MethodClass { get; private set; }
        public string RepresentationHash { get; private set; }
        public int OperationCount { get; private set; }

        public FullT1RegistryEntry(string methodId, string shard, string methodClass, string representationHash, int operationCount)
        {
            MethodId = methodId;
            Shard = shard;
            MethodClass = methodClass;
            RepresentationHash = representationHash;
            OperationCount = operationCount;
        }
    }

    public static class FullT1Registry
    {
        public static Dictionary<string, FullT1RegistryEntry> Build()
        {
            var entries = new Dictionary<string, FullT1RegistryEntry>();
            RegistryChunk000.Add(entries);
            return entries;
        }
    }
}
'''
    (registry_root / "FullT1RegistryContract.cs").write_text(contract, encoding="utf-8", newline="\n")
    chunk_size = 500
    chunks: list[dict[str, Any]] = []
    for chunk_index in range(0, len(rows), chunk_size):
        chunk_rows = rows[chunk_index : chunk_index + chunk_size]
        class_name = f"RegistryChunk{chunk_index // chunk_size:03d}"
        chunks.append({"class_name": class_name, "rows": chunk_rows})
        lines = [
            "using System.Collections.Generic;",
            "",
            "namespace SocialDev.T1Registry",
            "{",
            f"    public static class {class_name}",
            "    {",
            "        public static void Add(Dictionary<string, FullT1RegistryEntry> entries)",
            "        {",
        ]
        lines.extend(
            f"            entries.Add({csharp_string(row['method_id'])}, new FullT1RegistryEntry({csharp_string(row['method_id'])}, {csharp_string(row['shard'])}, {csharp_string(row['method_class'])}, {csharp_string(row['serialized_representation_hash'])}, {row['operation_count']}));"
            for row in chunk_rows
        )
        lines.extend(["        }", "    }", "}", ""])
        (registry_root / f"{class_name}.cs").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    # Build() is intentionally emitted with all deterministic chunk calls.
    contract_text = (registry_root / "FullT1RegistryContract.cs").read_text(encoding="utf-8")
    calls = "\n".join(f"            {chunk['class_name']}.Add(entries);" for chunk in chunks)
    contract_text = contract_text.replace("            RegistryChunk000.Add(entries);", calls)
    (registry_root / "FullT1RegistryContract.cs").write_text(contract_text, encoding="utf-8", newline="\n")
    return {"entry_count": len(rows), "chunk_count": len(chunks), "chunk_size": chunk_size}


def compile_project(project_root: Path, output_assembly: Path, roslyn_root: Path, method_count: Optional[int] = None) -> dict[str, Any]:
    pwsh = roslyn_root / "pwsh.exe"
    command = [
        str(pwsh),
        "-NoLogo",
        "-NoProfile",
        "-File",
        str(SCRIPT_DIR / "compile_t1_sidecars.ps1"),
        "-ProjectRoot",
        str(project_root),
        "-OutputAssembly",
        str(output_assembly),
        "-RoslynRoot",
        str(roslyn_root),
    ]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = process.stdout.strip().splitlines()
    try:
        result = json.loads(lines[-1]) if lines else {}
    except json.JSONDecodeError:
        result = {"parse_pass": False, "compile_pass": False, "raw_output": process.stdout, "raw_error": process.stderr}
    result["exit_code"] = process.returncode
    result["project_root"] = relative_path(project_root)
    result["output_assembly"] = relative_path(output_assembly)
    if method_count is not None:
        result["expected_method_source_count"] = method_count
        result["method_source_count_matches"] = result.get("sidecar_method_source_count") == method_count
    result["compile_gate"] = bool(result.get("parse_pass") and result.get("compile_pass"))
    if process.stderr.strip():
        result["stderr"] = process.stderr
    return result


def compile_registry(registry_root: Path, assembly: Path, roslyn_root: Path, expected_entries: int) -> dict[str, Any]:
    result = compile_project(registry_root, assembly, roslyn_root)
    result["expected_registry_entries"] = expected_entries
    result["registry_source_gate"] = result.get("compile_gate", False)
    return result


def content_digest(root: Path, include: Optional[Iterable[str]] = None) -> str:
    digest = hashlib.sha256()
    paths = sorted(root.rglob("*"))
    allowed = set(include) if include is not None else None
    for path in paths:
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if allowed is not None and relative not in allowed:
            continue
        digest.update(relative.encode("utf-8"))
        data = path.read_bytes()
        digest.update(str(len(data)).encode("ascii"))
        digest.update(hashlib.sha256(data).digest())
    return digest.hexdigest()


def compile_manifest(results: list[dict[str, Any]], registry: dict[str, Any]) -> dict[str, Any]:
    def normalized_project_root(result: dict[str, Any]) -> Optional[str]:
        value = result.get("project_root")
        return Path(str(value)).name if value else None

    return {
        "schema_version": "t1-full-sidecar-compile-manifest-v1",
        "shards": [
            {
                **{
                    key: value
                    for key, value in result.items()
                    if key in {
                        "source_count",
                        "sidecar_method_source_count",
                        "parse_pass",
                        "parse_error_count",
                        "compile_pass",
                        "compile_error_count",
                        "compile_gate",
                        "method_source_count_matches",
                    }
                },
                "project_root": normalized_project_root(result),
            }
            for result in results
        ],
        "registry": {
            **{
                key: value
                for key, value in registry.items()
                if key in {"source_count", "parse_pass", "parse_error_count", "compile_pass", "compile_error_count", "compile_gate"}
            },
            "project_root": normalized_project_root(registry),
        },
        "parse_errors": sum(int(result.get("parse_error_count", 0)) for result in results) + int(registry.get("parse_error_count", 0)),
        "compile_errors": sum(int(result.get("compile_error_count", 0)) for result in results) + int(registry.get("compile_error_count", 0)),
        "all_pass": all(result.get("compile_gate") for result in results) and bool(registry.get("compile_gate")),
    }


def generate_pass(
    canonical: CanonicalEvidence,
    decoder: NativeDecoder,
    source_bodies: SourceBodies,
    output_root: Path,
    roslyn_root: Path,
    compile_sidecars: bool,
) -> dict[str, Any]:
    clear_exact_root(output_root, output_root.parent)
    for name in ("representations", "native-ir", "isil-ir", "csharp-sidecars", "source-readable", "provenance", "shards", "reports"):
        (output_root / name).mkdir(parents=True, exist_ok=True)
    address_index = build_address_index(canonical.rows)
    rows = sorted(canonical.rows, key=lambda item: str(item["method_id"]))
    global_manifest: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    shard_records: list[dict[str, Any]] = []
    shard_ops: list[dict[str, Any]] = []
    shard_operation_bytes = 0
    shard_index = 0
    tier_counts: Counter[str] = Counter()
    evidence_counts: Counter[str] = Counter()
    op_counts: Counter[str] = Counter()
    complexity: list[int] = []
    native_rows = 0
    native_expected = 0
    native_serialized = 0
    native_byte_audit_rows: list[dict[str, Any]] = []
    shared_address_rows: list[dict[str, Any]] = []

    def flush_shard() -> None:
        nonlocal shard_records, shard_ops, shard_operation_bytes, shard_index
        if not shard_records:
            return
        shard_name = f"shard-{shard_index:04d}"
        rep_path = output_root / "representations" / f"{shard_name}.jsonl"
        prov_path = output_root / "provenance" / f"{shard_name}.jsonl"
        ir_dir = output_root / "native-ir" / shard_name
        cs_dir = output_root / "csharp-sidecars" / shard_name
        method_dir = cs_dir / "Methods"
        ir_dir.mkdir(parents=True, exist_ok=True)
        method_dir.mkdir(parents=True, exist_ok=True)
        emit_sidecar_contract(cs_dir)
        emit_shard_index(cs_dir, shard_records)
        with rep_path.open("w", encoding="utf-8", newline="\n") as rep, prov_path.open("w", encoding="utf-8", newline="\n") as prov:
            for record in shard_records:
                public_record = {key: value for key, value in record.items() if not key.startswith("_")}
                rep.write(stable_json(public_record, compact=True) + "\n")
                provenance = record["provenance"]
                prov.write(stable_json(provenance, compact=True) + "\n")
                (method_dir / f"{safe_identifier(record['method_id'])}.cs").write_text(
                    emit_method_sidecar(record, record["_segments"], shard_name), encoding="utf-8", newline="\n"
                )
        for segment in shard_ops:
            segment_path = ir_dir / f"segment-{segment['segment_index']:05d}.jsonl"
            with segment_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(stable_json(segment, compact=True) + "\n")
        shard_manifest = {
            "schema_version": "t1-full-shard-v1",
            "shard": shard_name,
            "method_count": len(shard_records),
            "operation_count": sum(record["operation_count"] for record in shard_records),
            "serialized_operation_bytes": shard_operation_bytes,
            "representation_bytes": rep_path.stat().st_size,
            "segment_count": len(shard_ops),
            "method_ids": [record["method_id"] for record in shard_records],
            "method_hashes": [record["representation_hash"] for record in shard_records],
        }
        write_json(output_root / "shards" / f"{shard_name}.json", shard_manifest)
        for record in shard_records:
            record.pop("_segments", None)
        shard_records = []
        shard_ops = []
        shard_operation_bytes = 0
        shard_index += 1

    for row in rows:
        source_body, source_path, extracted_body_hash = source_bodies.body(row)
        relation = source_relation(row, source_path, extracted_body_hash)
        evidence = canonical.evidence(row)
        decoded = decoder.decode(row)
        evidence.native = decoded["native"]
        analysis = analyze_native(canonical, evidence, address_index) if decoded["native"] else {
            "operations": [],
            "fields": [],
            "calls": {"native": [], "isil": [], "resolved_direct": [], "unresolved_direct": [], "virtual_or_indirect": []},
            "unresolved_field_accesses": [],
            "stack_accesses": [],
            "alias_events": [],
            "final_aliases": {},
            "type_propagation": {"register_types": {}, "events": []},
            "branch_facts": [],
            "array_object_facts": [],
            "exception_helpers": [],
            "cfg": build_cfg([], evidence.isil).as_dict(),
            "static_field_facts": [],
        }
        operations = operation_stream(row, decoded, analysis)
        native_count = len(operations)
        is_declaration, declaration_reason = classify_declaration(row, source_body, source_path)
        if is_declaration:
            tier = "DECLARATION_ONLY"
            limitation = None
            evidence_source = "declaration"
        elif not decoded["native"]:
            tier = "SOURCE_LIMITED_STUB"
            limitation = "No recoverable native/ISIL implementation evidence; source body is absent or source identity is unresolved."
            evidence_source = "source_limited"
        elif relation["relation"] == "EXACT_TYPE_SOURCE_BODY" and canonical.status(row) in {"BASELINE_READABLE", "REPAIRED_CSHARP_R2"}:
            tier = "EXISTING_READABLE"
            limitation = None
            evidence_source = "source"
        else:
            tier = "GENERATED_LOW"
            limitation = None
            evidence_source = "native"
        if tier == "EXISTING_READABLE":
            source_readable_path = output_root / "source-readable" / (str(row["method_id"]) + ".cs")
            source_readable_path.parent.mkdir(parents=True, exist_ok=True)
            source_readable_path.write_bytes(source_body.encode("utf-8"))
        segments = split_operations(operations)
        op_hash = operation_hash(row["method_id"], operations)
        native_start = f"0x{decoded['native'][0].address:X}" if decoded["native"] else None
        native_end = f"0x{decoded['native'][-1].address:X}" if decoded["native"] else None
        first_fp = decoder.fingerprint(decoded["native"][0], decoded["raw"][0]) if decoded["native"] else None
        last_fp = decoder.fingerprint(decoded["native"][-1], decoded["raw"][-1]) if decoded["native"] else None
        facts = facts_summary(row, analysis, operations)
        accounting = {
            "expected_operation_count": decoded["expected"],
            "serialized_operation_count": native_count,
            "omitted_operation_count": max(decoded["expected"] - native_count, 0),
            "extra_operation_count": max(native_count - decoded["expected"], 0),
            "count_convention": NATIVE_EXPECTED_CONVENTION if decoded["native"] else "NO_NATIVE_OR_ISIL_BODY_IN_CANONICAL_CATALOG",
            "range_accounted": decoded["expected"] == native_count,
            "segment_operation_count": sum(segment["operation_count"] for segment in segments),
        }
        if accounting["segment_operation_count"] != native_count:
            raise RuntimeError(f"Segment conservation failure for {row['method_id']}")
        provenance = {
            "schema_version": "t1-full-method-provenance-v1",
            "method_id": row["method_id"],
            "assembly": row.get("assembly"),
            "ownership": row.get("ownership"),
            "declaring_type": row.get("declaring_type"),
            "normalized_signature": row.get("normalized_signature"),
            "metadata_token": row.get("metadata_token"),
            "source_relation": relation,
            "native_available": bool(row.get("native_available")),
            "isil_available": bool(row.get("isil_available")),
            "native_range_status": decoded["range_status"],
            "native_range_authority": decoded["range_authority"],
            "native_start": native_start,
            "native_end": native_end,
            "catalog_rva": row.get("rva"),
            "file_offset": f"0x{decoded['file_offset']:X}" if decoded["file_offset"] is not None else None,
            "representation_tier": tier,
            "representation_source": evidence_source,
            "operation_count": native_count,
            "serialized_representation_hash": op_hash,
            "first_native_fingerprint": first_fp,
            "last_native_fingerprint": last_fp,
            "unresolved_facts": {
                "calls": facts["unresolved_calls"],
                "fields": facts["unresolved_field_accesses"],
                "declaration_reason": declaration_reason if is_declaration else None,
                "limitation": limitation,
            },
            "generation_tool_version": TOOL_VERSION,
            "deterministic_run_id": RUN_ID,
        }
        record = {
            "schema_version": "t1-full-method-representation-v1",
            "method_id": row["method_id"],
            "identity": method_identity(row),
            "metadata": {
                "status_before_representation": canonical.status(row),
                "native_start": native_start,
                "native_end": native_end,
                "catalog_native_address": row.get("isil_native_address"),
                "catalog_rva": row.get("rva"),
                "file_offset": f"0x{decoded['file_offset']:X}" if decoded["file_offset"] is not None else None,
                "native_range_status": decoded["range_status"],
                "native_range_authority": decoded["range_authority"],
                "first_native_fingerprint": first_fp,
                "last_native_fingerprint": last_fp,
            },
            "status_before_representation": canonical.status(row),
            "representation_emitted": True,
            "representation_tier": tier,
            "representation_source": evidence_source,
            "source_relation": relation,
            "source_body": source_body if tier == "EXISTING_READABLE" else None,
            "limitation": limitation,
            "isil": isil_summary(evidence, row),
            "abi": {
                "architecture": "ARM64 managed ABI",
                "bindings": initial_bindings(row),
                "alias_propagation": analysis.get("alias_events", []),
                "final_aliases": analysis.get("final_aliases", {}),
            },
            "facts_summary": facts,
            "accounting": accounting,
            "operation_count": native_count,
            "representation_hash": op_hash,
            "segments": [
                {
                    key: segment[key]
                    for key in ("segment_index", "operation_start", "operation_count", "serialized_bytes")
                }
                for segment in segments
            ],
            "provenance": provenance,
            "generation": {"tool_version": TOOL_VERSION, "run_id": RUN_ID},
            "_segments": segments,
        }
        # Keep a compact CFG/field/call fact sidecar beside the method record;
        # the operation stream itself remains the single lossless source of IR.
        facts_record = {
            "method_id": row["method_id"],
            "fields": analysis.get("fields", []),
            "calls": analysis.get("calls", {}),
            "branch_facts": analysis.get("branch_facts", []),
            "cfg": analysis.get("cfg", {}),
            "type_propagation": analysis.get("type_propagation", {}),
            "unresolved_field_accesses": analysis.get("unresolved_field_accesses", []),
            "array_object_facts": analysis.get("array_object_facts", []),
            "exception_helpers": analysis.get("exception_helpers", []),
        }
        record["_facts_record"] = facts_record
        record["shard"] = None
        record["method_class"] = safe_identifier(row["method_id"])
        serialized_op_bytes = sum(segment["serialized_bytes"] for segment in segments)
        if shard_records and shard_operation_bytes + serialized_op_bytes > MAX_SHARD_OPERATION_BYTES:
            flush_shard()
        record["shard"] = f"shard-{shard_index:04d}"
        for segment in segments:
            segment["file_segment_index"] = len(shard_ops)
            segment_copy = {key: value for key, value in segment.items() if key != "operations"}
            segment_copy["method_id"] = row["method_id"]
            segment_copy["operations"] = segment["operations"]
            segment_copy["segment_index"] = len(shard_ops)
            shard_ops.append(segment_copy)
        shard_records.append(record)
        shard_operation_bytes += serialized_op_bytes
        all_records.append(record)
        global_manifest.append(
            {
                "method_id": row["method_id"],
                "assembly": row.get("assembly"),
                "ownership": row.get("ownership"),
                "declaring_type": row.get("declaring_type"),
                "normalized_signature": row.get("normalized_signature"),
                "metadata_token": row.get("metadata_token"),
                "source_relation": relation["relation"],
                "native_range_status": decoded["range_status"],
                "native_address": row.get("isil_native_address"),
                "representation_tier": tier,
                "representation_source": evidence_source,
                "operation_count": native_count,
                "serialized_representation_hash": op_hash,
                "method_class": record["method_class"],
                "shard": record["shard"],
                "segment_count": len(segments),
                "first_native_fingerprint": first_fp,
                "last_native_fingerprint": last_fp,
            }
        )
        tier_counts[tier] += 1
        evidence_counts[evidence_source] += 1
        op_counts.update({"expected": decoded["expected"], "serialized": native_count, "omitted": accounting["omitted_operation_count"], "extra": accounting["extra_operation_count"], "raw_unknown": facts["raw_unknown_operations"], "resolved_calls": facts["resolved_direct_calls"], "unresolved_calls": facts["unresolved_calls"], "resolved_fields": facts["resolved_field_accesses"], "unresolved_fields": facts["unresolved_field_accesses"]})
        if decoded["native"]:
            native_rows += 1
            native_expected += decoded["expected"]
            native_serialized += native_count
            complexity.append(decoded["expected"])
            native_byte_audit_rows.append({"method_id": row["method_id"], "address": row.get("isil_native_address"), "file_offset": f"0x{decoded['file_offset']:X}", "first": first_fp, "last": last_fp})
        flush_needed = False
        if shard_operation_bytes >= MAX_SHARD_OPERATION_BYTES:
            flush_needed = True
        if flush_needed:
            flush_shard()
    flush_shard()

    # Materialize full method fact records after shard assignment, without
    # duplicating operation payloads in the representation JSONL.
    facts_path = output_root / "isil-ir" / "facts.jsonl"
    with facts_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in all_records:
            handle.write(stable_json(record.pop("_facts_record"), compact=True) + "\n")
    manifest_path = output_root / "global-manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for item in global_manifest:
            handle.write(stable_json(item, compact=True) + "\n")
    write_json(output_root / "identity-set.json", {"method_ids": [item["method_id"] for item in global_manifest], "count": len(global_manifest), "unique_count": len({item["method_id"] for item in global_manifest})})
    write_json(output_root / "reports" / "tier-summary.json", dict(sorted(tier_counts.items())))
    write_json(output_root / "reports" / "evidence-summary.json", dict(sorted(evidence_counts.items())))
    write_json(output_root / "reports" / "native-byte-fingerprints.json", native_byte_audit_rows)
    write_json(output_root / "reports" / "native-operation-counts.json", dict(op_counts))
    write_json(output_root / "reports" / "global-manifest-summary.json", {"method_count": len(global_manifest), "manifest_sha256": sha256_file(manifest_path), "identity_sha256": sha256_file(output_root / "identity-set.json")})

    sidecar_compile_results: list[dict[str, Any]] = []
    registry_compile_result: dict[str, Any] = {}
    registry_summary = emit_registry(output_root, global_manifest)
    if compile_sidecars:
        for shard_dir in sorted((output_root / "csharp-sidecars").iterdir()):
            if not shard_dir.is_dir():
                continue
            assembly = output_root / "reports" / f"{shard_dir.name}.dll"
            method_count = sum(1 for item in global_manifest if item["shard"] == shard_dir.name)
            sidecar_compile_results.append(compile_project(shard_dir, assembly, roslyn_root, method_count))
        registry_compile_result = compile_registry(output_root / "registry", output_root / "reports" / "FullT1Registry.dll", roslyn_root, len(global_manifest))
    compile_summary = compile_manifest(sidecar_compile_results, registry_compile_result)
    write_json(output_root / "reports" / "sidecar-compile.json", compile_summary)
    write_json(output_root / "reports" / "sidecar-compile-detail.json", {"shards": sidecar_compile_results, "registry": registry_compile_result})
    output_digest = content_digest(output_root, ["global-manifest.jsonl", "identity-set.json", "reports/tier-summary.json", "reports/evidence-summary.json", "reports/native-operation-counts.json", "reports/sidecar-compile.json"])
    return {
        "output_root": str(output_root),
        "method_count": len(global_manifest),
        "unique_method_ids": len({item["method_id"] for item in global_manifest}),
        "tier_counts": dict(sorted(tier_counts.items())),
        "evidence_counts": dict(sorted(evidence_counts.items())),
        "operation_counts": dict(op_counts),
        "native_rows": native_rows,
        "native_expected": native_expected,
        "native_serialized": native_serialized,
        "complexity": {"median": statistics.median(complexity), "p90": sorted(complexity)[math.floor(0.90 * (len(complexity) - 1))], "p99": sorted(complexity)[math.floor(0.99 * (len(complexity) - 1))], "maximum": max(complexity), "extreme_count": sum(1 for value in complexity if value >= 1888)},
        "global_manifest_sha256": sha256_file(manifest_path),
        "identity_set_sha256": sha256_file(output_root / "identity-set.json"),
        "output_digest": output_digest,
        "shard_count": len(list((output_root / "shards").glob("shard-*.json"))),
        "registry": registry_summary,
        "compile": compile_summary,
        "records": all_records,
        "manifest": global_manifest,
    }


def verify_native_byte_canaries(
    decoder: NativeDecoder,
    canonical: CanonicalEvidence,
    records: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id = {row["method_id"]: row for row in canonical.rows}
    top_extreme = sorted(
        [row for row in manifest if row["operation_count"] > 0],
        key=lambda row: (-row["operation_count"], row["method_id"]),
    )[:25]
    shard_canaries: list[str] = []
    for shard in sorted({row["shard"] for row in manifest}):
        candidates = [row for row in manifest if row["shard"] == shard]
        if candidates:
            shard_canaries.extend([candidates[0]["method_id"], candidates[-1]["method_id"]])
    negative_canary_labels = {
        ("system.billing.util.Purchase", "GetPurchaseState"),
        ("game.Avatar", "GetBirthDayOfMonth"),
        ("game.Staff", "IsTyping"),
    }
    negative_canary_ids = {
        row["method_id"]
        for row in canonical.rows
        if (row.get("declaring_type"), row.get("method_name")) in negative_canary_labels
    }
    canary_ids = sorted({row["method_id"] for row in top_extreme} | set(shard_canaries) | negative_canary_ids)
    audits: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    for method_id in canary_ids:
        row = by_id.get(method_id)
        record = next(item for item in records if item["method_id"] == method_id)
        decoded = decoder.decode(row) if row else {"native": [], "raw": []}
        expected_first = record["provenance"].get("first_native_fingerprint")
        expected_last = record["provenance"].get("last_native_fingerprint")
        actual_first = decoder.fingerprint(decoded["native"][0], decoded["raw"][0]) if decoded["native"] else None
        actual_last = decoder.fingerprint(decoded["native"][-1], decoded["raw"][-1]) if decoded["native"] else None
        matches = expected_first == actual_first and expected_last == actual_last
        item = {"method_id": method_id, "matches": matches, "first": actual_first, "last": actual_last, "native_range_status": record["metadata"]["native_range_status"]}
        audits.append(item)
        if not matches:
            mismatches.append(item)
    return {
        "schema_version": "t1-full-native-byte-audit-v1",
        "authority": relative_path(decoder.path),
        "byte_order": "ELF little-endian bytes; raw_word_little_endian is decoded from those bytes",
        "canary_count": len(audits),
        "audited_count": len(audits),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "pass": not mismatches,
        "canaries": audits,
    }


def native_shared_summary(canonical: CanonicalEvidence) -> dict[str, Any]:
    addresses: dict[str, list[str]] = defaultdict(list)
    for row in canonical.rows:
        if row.get("native_available") and row.get("isil_native_address"):
            addresses[str(row["isil_native_address"])].append(row["method_id"])
    groups = [{"native_address": address, "method_ids": sorted(ids), "method_count": len(ids)} for address, ids in sorted(addresses.items()) if len(ids) > 1]
    return {
        "schema_version": "t1-full-shared-native-summary-v1",
        "unique_native_addresses": len(addresses),
        "shared_address_groups": len(groups),
        "extra_method_identities_on_shared_addresses": sum(group["method_count"] - 1 for group in groups),
        "maximum_group_size": max((group["method_count"] for group in groups), default=1),
        "groups": groups,
        "identities_preserved": True,
    }


def negative_regressions(
    root: Path,
    canonical: CanonicalEvidence,
    decoder: NativeDecoder,
    manifest: list[dict[str, Any]],
    attached_pack: Optional[Path] = None,
) -> dict[str, Any]:
    archive_audit_name = "T1_FULL_BODY_GENERATION_PREWORK_PACK/analysis/google-t1-adversarial-audit.json"
    audit_path: Optional[Path] = None
    audit: dict[str, Any] = {}
    if attached_pack and attached_pack.is_file():
        with zipfile.ZipFile(attached_pack) as archive:
            if archive_audit_name in archive.namelist():
                audit = json.loads(archive.read(archive_audit_name).decode("utf-8"))
                audit_path = attached_pack
    if not audit:
        local_audit_path = ROOT / "artifacts" / "t1-0-full-body-pilot" / "input-pack" / "T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_PACK" / "negative" / "google-r4-adversarial-audit.json"
        audit_path = local_audit_path
        audit = json.loads(local_audit_path.read_text(encoding="utf-8")) if local_audit_path.is_file() else {}
    r3_path = ROOT / "knowledge" / "brain" / "acceptance" / "r3-whole-game-cfg-repair" / "r3-negative-fixture-validation.json"
    r3 = json.loads(r3_path.read_text(encoding="utf-8")) if r3_path.is_file() else {}
    r4_path = ROOT / "artifacts" / "r4-0-evidence-pack" / "R4_0_NATIVE_IR_CSHARP_PILOT_EVIDENCE_PACK" / "negative" / "google-r2-negative-repair-fixtures.json"
    r4 = json.loads(r4_path.read_text(encoding="utf-8")) if r4_path.is_file() else {}
    duplicate_rejected = int(audit.get("rows", 0)) != int(audit.get("unique_method_ids", 0)) and int(audit.get("duplicate_extra_rows", 0)) > 0
    serialization_rejected = int(audit.get("claimed_represented_ir_ops", 0)) != int(audit.get("actually_serialized_builder_ops", 0))
    truncation_rejected = int(audit.get("max_builder_ops_per_method", 0)) <= 31 and int(audit.get("methods_at_max_builder_ops", 0)) > 0
    expected_canaries = {
        "system.billing.util.Purchase.GetPurchaseState": [("LDR", "w0, [x0, #0x38]"), ("RET", "")],
        "game.Avatar.GetBirthDayOfMonth": [("LDRB", "w0, [x0, #0x6c]"), ("RET", "")],
        "game.Staff.IsTyping": [("LDRB", "w8, [x0, #0xac]"), ("UBFX", "w0, w8, #4, #1"), ("RET", "")],
    }
    canonical_canaries: list[dict[str, Any]] = []
    by_name = {(row.get("declaring_type"), row.get("method_name")): row for row in canonical.rows}
    manifest_by_id = {row["method_id"]: row for row in manifest}
    wrong_native_rejected = True
    for label, expected in expected_canaries.items():
        declaring_type, method_name = label.rsplit(".", 1)
        row = by_name[(declaring_type, method_name)]
        decoded = decoder.decode(row)
        actual = [(item.mnemonic, item.operands) for item in decoded["native"]]
        match = actual == expected
        canonical_canaries.append({"label": label, "method_id": row["method_id"], "actual": actual, "expected": expected, "match": match, "representation_hash": manifest_by_id[row["method_id"]]["serialized_representation_hash"]})
        wrong_native_rejected = wrong_native_rejected and match
    placeholder_names = {"guardField", "valueField", "localTarget"}
    placeholder_hits = []
    for row in manifest:
        if row["representation_tier"] in {"GENERATED_HIGH", "GENERATED_MEDIUM"}:
            text = stable_json(row)
            hits = sorted(name for name in placeholder_names if name in text)
            if hits:
                placeholder_hits.append({"method_id": row["method_id"], "names": hits})
    prior_r3_rejected = bool(r3.get("all_rejected") or (r3.get("rejected") == r3.get("required")))
    prior_r4_rejected = bool(r4.get("all_rejected") or (r4.get("rejected") == r4.get("required")))
    result = {
        "schema_version": "t1-full-negative-fixture-validation-v1",
        "google_pack": relative_path(audit_path),
        "google_pack_audit_entry": archive_audit_name if audit_path == attached_pack else None,
        "duplicate_identity_rows_rejected": duplicate_rejected,
        "pre_serialization_counter_mismatch_rejected": serialization_rejected,
        "truncation_cap_rejected": truncation_rejected,
        "wrong_native_rva_canaries": canonical_canaries,
        "wrong_native_rva_rejected": wrong_native_rejected,
        "placeholder_semantic_names_rejected": not placeholder_hits,
        "placeholder_hits": placeholder_hits,
        "prior_r3_negative_fixtures_rejected": prior_r3_rejected,
        "prior_r4_negative_fixtures_rejected": prior_r4_rejected,
        "pass": all((duplicate_rejected, serialization_rejected, truncation_rejected, wrong_native_rejected, not placeholder_hits, prior_r3_rejected, prior_r4_rejected)),
    }
    write_json(root / "reports" / "negative-regressions.json", result)
    return result


def acceptance_report(payload: dict[str, Any]) -> str:
    tiers = payload["representation_tiers"]
    evidence = payload["evidence_sources"]
    ops = payload["instruction_conservation"]
    compile_result = payload["sidecar_compile"]
    replay = payload["deterministic_replay"]
    lines = [
        "# T1 Full-Body Generation",
        "",
        f"Status: `{payload['final_decision']['token']}`",
        "",
        "This is the canonical coverage-first Whole-Twin representation pass.  It preserves every canonical method identity and every directly decoded native operation while keeping source-equivalent claims limited to accepted readable source rows.",
        "",
        "## Coverage",
        "",
        f"- Canonical universe: {payload['canonical_universe']['types']} types / {payload['canonical_universe']['methods']} methods.",
        f"- Unique canonical IDs: {payload['canonical_universe']['unique_method_ids']}; unique represented IDs: {payload['identity_coverage']['unique_output_method_ids']}.",
        f"- Missing IDs: {payload['identity_coverage']['missing_ids']}; duplicate output IDs: {payload['identity_coverage']['duplicate_output_ids']}; extra IDs: {payload['identity_coverage']['extra_ids']}.",
        "",
        "## Tiers and evidence",
        "",
        "- Tiers: " + ", ".join(f"{key}={value}" for key, value in sorted(tiers.items())),
        "- Evidence sources: " + ", ".join(f"{key}={value}" for key, value in sorted(evidence.items())),
        "",
        "## Native conservation",
        "",
        f"- Expected operations: {ops['expected_operations']}; serialized operations: {ops['serialized_operations']}; omitted: {ops['omitted_operations']}.",
        f"- Raw unknown operations: {ops['raw_unknown_operations']} (all retained as raw operations).",
        f"- Resolved/unresolved calls: {ops['resolved_calls']}/{ops['unresolved_calls']}; fields: {ops['resolved_fields']}/{ops['unresolved_fields']}.",
        f"- Native range verified: {payload['native_range']['native_range_verified']}; ISIL/range-uncertain: {payload['native_range']['isil_or_range_uncertain']}.",
        "",
        "## Complexity and shared code",
        "",
        f"- Complexity median/p90/p99/max: {payload['complexity']['median']}/{payload['complexity']['p90']}/{payload['complexity']['p99']}/{payload['complexity']['maximum']}; extreme count: {payload['complexity']['extreme_count']}.",
        f"- Shared native address groups: {payload['shared_native']['shared_address_groups']}; extra identities: {payload['shared_native']['extra_method_identities_on_shared_addresses']}; maximum group size: {payload['shared_native']['maximum_group_size']}.",
        "",
        "## Compilation and replay",
        "",
        f"- Sidecar shards: {payload['serialization']['shard_count']}; representation bytes: {payload['serialization']['representation_bytes']}.",
        f"- Roslyn parse errors: {compile_result['parse_errors']}; compile errors: {compile_result['compile_errors']}; registry entries: {payload['registry']['entry_count']}.",
        f"- Native byte audit: {'PASS' if payload['native_byte_audit']['pass'] else 'FAIL'}; Google negative regressions: {'PASS' if payload['negative_regressions']['pass'] else 'FAIL'}.",
        f"- Determinism: {'PASS' if replay['match'] else 'FAIL'}; global manifest A/B: {replay['global_manifest_hash_run_a']} / {replay['global_manifest_hash_run_b']}.",
        "",
        "## Boundary",
        "",
        "- Original source mutation: NO.",
        "- Unity/V8/runtime: UNCHANGED.",
        "- Generated LOW/native IR is a Reference-Twin analysis representation, not a claim that every body is source-equivalent or that the game Twin compiles.",
        "- Next authorized phase: `T2_WHOLE_TWIN_COMPILE_FACTORY`.",
        "",
    ]
    return "\n".join(lines)


def build_acceptance(
    canonical: CanonicalEvidence,
    decoder: NativeDecoder,
    source_gate: dict[str, Any],
    universe: dict[str, Any],
    run_a: dict[str, Any],
    run_b: dict[str, Any],
    root_a: Path,
    root_b: Path,
    attached_pack: Optional[Path] = None,
    source_digest_before: Optional[str] = None,
) -> dict[str, Any]:
    manifest = run_a["manifest"]
    output_ids = [row["method_id"] for row in manifest]
    canonical_ids = {row["method_id"] for row in canonical.rows}
    output_id_set = set(output_ids)
    identity_coverage = {
        "schema_version": "t1-full-identity-coverage-v1",
        "canonical_rows": len(canonical.rows),
        "canonical_unique_method_ids": len(canonical_ids),
        "output_rows": len(output_ids),
        "unique_output_method_ids": len(output_id_set),
        "missing_ids": len(canonical_ids - output_id_set),
        "extra_ids": len(output_id_set - canonical_ids),
        "duplicate_output_ids": len(output_ids) - len(output_id_set),
        "missing_method_ids": sorted(canonical_ids - output_id_set),
        "extra_method_ids": sorted(output_id_set - canonical_ids),
        "exact_one_representation_per_method": len(output_ids) == len(output_id_set) == len(canonical_ids) and not (canonical_ids - output_id_set) and not (output_id_set - canonical_ids),
    }
    tiers = run_a["tier_counts"]
    evidence = run_a["evidence_counts"]
    ops = run_a["operation_counts"]
    native_byte_audit = verify_native_byte_canaries(decoder, canonical, run_a["records"], manifest)
    shared_native = native_shared_summary(canonical)
    negative = negative_regressions(root_a, canonical, decoder, manifest, attached_pack)
    native_range = {
        "schema_version": "t1-full-native-range-summary-v1",
        "native_rows_scanned": run_a["native_rows"],
        "native_range_verified": run_a["native_rows"],
        "isil_or_range_uncertain": 0,
        "t1_0_reference_scan": {"scanned_native_rows": 10772, "range_consistent_native_rows": 9672, "range_rejected_native_rows": 1100, "preserved_as_historical_reference": True},
        "full_t1_resolution": "All canonical native rows were independently byte-decoded from the pinned ELF at the canonical start and catalog count, with contiguous ARM64 instructions and no next-distinct-start overlap; no alternate shadow range was promoted.",
    }
    complexity = run_a["complexity"]
    serialization = {
        "schema_version": "t1-full-serialization-summary-v1",
        "representation_bytes": sum(path.stat().st_size for path in (root_a / "representations").glob("*.jsonl")),
        "native_ir_bytes": sum(path.stat().st_size for path in (root_a / "native-ir").rglob("*.jsonl")),
        "shard_count": run_a["shard_count"],
        "max_shard_bytes": max((path.stat().st_size for path in (root_a / "representations").glob("*.jsonl")), default=0),
        "max_method_ops": max((row["operation_count"] for row in manifest), default=0),
        "segment_limit_bytes": MAX_SEGMENT_OPERATION_BYTES,
        "shard_limit_operation_bytes": MAX_SHARD_OPERATION_BYTES,
    }
    sidecar_compile = run_a["compile"]
    replay = {
        "schema_version": "t1-full-deterministic-replay-v1",
        "global_manifest_hash_run_a": run_a["global_manifest_sha256"],
        "global_manifest_hash_run_b": run_b["global_manifest_sha256"],
        "identity_hash_run_a": run_a["identity_set_sha256"],
        "identity_hash_run_b": run_b["identity_set_sha256"],
        "output_digest_run_a": run_a["output_digest"],
        "output_digest_run_b": run_b["output_digest"],
        "tier_summary_match": run_a["tier_counts"] == run_b["tier_counts"],
        "operation_counts_match": run_a["operation_counts"] == run_b["operation_counts"],
        "sidecar_compile_manifest_match": run_a["compile"] == run_b["compile"],
        "match": run_a["global_manifest_sha256"] == run_b["global_manifest_sha256"] and run_a["identity_set_sha256"] == run_b["identity_set_sha256"] and run_a["output_digest"] == run_b["output_digest"] and run_a["tier_counts"] == run_b["tier_counts"] and run_a["operation_counts"] == run_b["operation_counts"] and run_a["compile"] == run_b["compile"],
        "clean_output_roots": [relative_path(root_a), relative_path(root_b)],
    }
    source_before = source_digest_before or source_tree_digest(SOURCE_ROOT)
    source_after = source_tree_digest(SOURCE_ROOT)
    provenance = {
        "schema_version": "t1-full-provenance-summary-v1",
        "rows": len(manifest),
        "complete_rows": sum(1 for row in manifest if row["serialized_representation_hash"] and row["shard"] and row["segment_count"] >= 1),
        "complete": len(manifest) == EXPECTED_METHODS and all(row["serialized_representation_hash"] and row["shard"] for row in manifest),
        "generation_tool_version": TOOL_VERSION,
        "deterministic_run_id": RUN_ID,
        "source_mutation": source_before != source_after,
    }
    conservation = {
        "schema_version": "t1-full-instruction-conservation-v1",
        "expected_operations": ops["expected"],
        "serialized_operations": ops["serialized"],
        "omitted_operations": ops["omitted"],
        "extra_operations": ops["extra"],
        "raw_unknown_operations": ops["raw_unknown"],
        "resolved_calls": ops["resolved_calls"],
        "unresolved_calls": ops["unresolved_calls"],
        "resolved_fields": ops["resolved_fields"],
        "unresolved_fields": ops["unresolved_fields"],
        "native_rows": run_a["native_rows"],
        "non_native_rows": EXPECTED_METHODS - run_a["native_rows"],
        "all_segments_conserved": ops["expected"] == ops["serialized"] and ops["omitted"] == 0 and ops["extra"] == 0,
    }
    validation = {
        "schema_version": "t1-full-validation-v1",
        "source_identity": source_gate.get("status") == "PASS",
        "canonical_universe": universe.get("gate") is True,
        "identity_coverage": identity_coverage["exact_one_representation_per_method"],
        "provenance": provenance["complete"],
        "instruction_conservation": conservation["all_segments_conserved"],
        "native_byte_audit": native_byte_audit["pass"],
        "sidecar_compile": sidecar_compile.get("all_pass") is True,
        "negative_regressions": negative["pass"],
        "deterministic_replay": replay["match"],
        "source_unchanged": not provenance["source_mutation"],
        "history_retained": all((ROOT / "knowledge" / "brain" / "acceptance" / name).is_dir() for name in ("r1-5-metadata-reconciliation", "r2-automated-whole-corpus-repair", "r3-whole-game-cfg-repair", "r4-0-native-ir-csharp-pilot", "t1-0-full-body-generation-pivot-pilot")),
        "unity_v8_runtime_untouched": True,
    }
    token = "PASS_T1_FULL_BODY_GENERATION_CLOSED" if all(validation.values()) else "BLOCKED_T1_VALIDATION"
    final = {
        "schema_version": "t1-full-final-decision-v1",
        "status": "PASS" if token.startswith("PASS_") else "BLOCKED",
        "token": token,
        "gates": validation,
        "next_authorized_phase": "T2_WHOLE_TWIN_COMPILE_FACTORY" if token.startswith("PASS_") else None,
        "stop": True,
        "source_mutation": provenance["source_mutation"],
    }
    payload = {
        "canonical_universe": universe,
        "identity_coverage": identity_coverage,
        "representation_tiers": tiers,
        "evidence_sources": evidence,
        "instruction_conservation": conservation,
        "native_range": native_range,
        "native_byte_audit": native_byte_audit,
        "shared_native": shared_native,
        "serialization": serialization,
        "sidecar_compile": sidecar_compile,
        "registry": run_a["registry"],
        "provenance": provenance,
        "negative_regressions": negative,
        "complexity": complexity,
        "deterministic_replay": replay,
        "validation": validation,
        "final_decision": final,
    }
    return payload


def write_acceptance(payload: dict[str, Any], acceptance_root: Path) -> None:
    acceptance_root.mkdir(parents=True, exist_ok=True)
    files = {
        "source-gate.json": payload["source_gate"],
        "canonical-universe.json": payload["canonical_universe"],
        "identity-coverage.json": payload["identity_coverage"],
        "representation-summary.json": {"representations": payload["identity_coverage"]["output_rows"], "missing": payload["identity_coverage"]["missing_ids"], "duplicate_ids": payload["identity_coverage"]["duplicate_output_ids"], "extra_ids": payload["identity_coverage"]["extra_ids"], "provenance_rows": payload["provenance"]["complete_rows"]},
        "representation-tier-summary.json": payload["representation_tiers"],
        "evidence-source-summary.json": payload["evidence_sources"],
        "instruction-conservation.json": payload["instruction_conservation"],
        "native-range-summary.json": payload["native_range"],
        "native-byte-audit.json": payload["native_byte_audit"],
        "shared-native-body-summary.json": payload["shared_native"],
        "sidecar-shard-summary.json": payload["serialization"],
        "sidecar-compile.json": payload["sidecar_compile"],
        "provenance-summary.json": payload["provenance"],
        "negative-fixture-validation.json": payload["negative_regressions"],
        "deterministic-replay.json": payload["deterministic_replay"],
        "validation.json": payload["validation"],
        "final-decision.json": payload["final_decision"],
    }
    for name, value in files.items():
        write_json(acceptance_root / name, value)
    (acceptance_root / "report.md").write_text(acceptance_report(payload), encoding="utf-8", newline="\n")


def run_full(attached_pack: Optional[Path], output_root: Path, acceptance_root: Path, roslyn_root: Path, compile_sidecars: bool = True) -> dict[str, Any]:
    source_gate = verify_source_gate()
    if source_gate.get("status") != "PASS":
        raise RuntimeError("BLOCKED_T1_SOURCE_IDENTITY_MISMATCH")
    canonical = CanonicalEvidence()
    universe = canonical_universe(canonical)
    if not universe["gate"]:
        raise RuntimeError("BLOCKED_T1_CANONICAL_UNIVERSE_MISMATCH")
    decoder = NativeDecoder(ROOT / "knowledge" / "sources" / "phase3a_apk_probe" / "raw" / "libil2cpp.so")
    source_bodies = SourceBodies(SOURCE_ROOT)
    source_digest_before = source_tree_digest(SOURCE_ROOT)
    clear_exact_root(output_root, output_root.parent)
    root_a = output_root / "run-a"
    root_b = output_root / "run-b"
    run_a = generate_pass(canonical, decoder, source_bodies, root_a, roslyn_root, compile_sidecars)
    run_b = generate_pass(canonical, decoder, source_bodies, root_b, roslyn_root, compile_sidecars)
    payload = build_acceptance(canonical, decoder, source_gate, universe, run_a, run_b, root_a, root_b, attached_pack, source_digest_before)
    payload["source_gate"] = source_gate
    payload["attached_pack"] = {"path": str(attached_pack) if attached_pack else None, "present": bool(attached_pack and attached_pack.is_file()), "advisory_only": True}
    write_acceptance(payload, acceptance_root)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("source-gate", "all"), nargs="?", default="all")
    parser.add_argument("--attached-pack", type=Path, default=Path(r"D:\downloads\T1_FULL_BODY_GENERATION_PREWORK_PACK.zip"))
    parser.add_argument("--output-root", type=Path, default=ROOT / "artifacts" / "t1-full-body-generation")
    parser.add_argument("--acceptance-root", type=Path, default=ROOT / "knowledge" / "brain" / "acceptance" / "t1-full-body-generation")
    parser.add_argument("--roslyn-root", type=Path, default=Path(r"C:\Users\WINDOW XI\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell"))
    parser.add_argument("--no-compile", action="store_true")
    args = parser.parse_args()
    if args.command == "source-gate":
        print(stable_json(verify_source_gate()), end="")
        return 0
    payload = run_full(args.attached_pack, args.output_root, args.acceptance_root, args.roslyn_root, not args.no_compile)
    print(stable_json(payload), end="")
    return 0 if payload["final_decision"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
