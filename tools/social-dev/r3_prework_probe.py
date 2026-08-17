#!/usr/bin/env python3
"""Canonical R3 prework profiler and identity recovery.

This tool is deliberately evidence-only.  It reads the corrected R1.5 catalog,
the final R2 Twin queue, the isolated Twin source, and the already-produced
ISIL files.  It never edits the original source roots or the Twin.  Source
identity is accepted from an exact R1.5 line span plus body hash; short-name
matching is retained only as a diagnostic field.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


OWNED = {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
R3_CFG_STATUS = "DEFER_R3_CFG"
R2_BLOCKED_STATUS = "BLOCKED_IDENTITY"

PINNED_INPUTS = {
    "apk": (
        "sources/raw/Social_Dev_Story_v2.5.1.apk",
        "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    ),
    "rar": (
        "sources/raw/1_Click_CSharp_Code.rar",
        "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903",
    ),
    "libil2cpp": (
        "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so",
        "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    ),
    "global_metadata": (
        "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat",
        "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
    ),
}

ROOT_CAUSES = [
    "SOURCE_FILE_MISSING",
    "SOURCE_METHOD_NOT_LOCATED",
    "OVERLOAD_OR_SOURCE_AMBIGUITY",
    "CONSTRUCTOR_REPRESENTATION",
    "ACCESSOR_EVENT_REPRESENTATION",
    "NESTED_OR_COMPILER_GENERATED_TYPE_IDENTITY",
    "GENERIC_IDENTITY_NORMALIZATION",
    "BYREF_REF_OUT_NORMALIZATION",
    "BODY_HASH_DRIFT",
    "ROSLYN_SYMBOL_AMBIGUITY",
    "METADATA_SOURCE_SIGNATURE_DISAGREEMENT",
    "SOURCE_LIMITED",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def normalize_relative(value: str | None) -> str:
    return (value or "").replace("\\", "/").lstrip("/")


def normalize_type(value: str) -> str:
    value = value.strip().replace("global::", "").replace(" ", "").replace("?", "")
    aliases = {
        "object": "System.Object",
        "string": "System.String",
        "bool": "System.Boolean",
        "byte": "System.Byte",
        "short": "System.Int16",
        "int": "System.Int32",
        "long": "System.Int64",
        "float": "System.Single",
        "double": "System.Double",
        "void": "System.Void",
    }
    for source, target in aliases.items():
        value = re.sub(rf"(?<![\w.]){re.escape(source)}(?![\w])", target, value)
    return value


def split_type_list(value: str) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    depth = 0
    for char in value:
        if char in "<[(":
            depth += 1
        elif char in ">])":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    tail = "".join(current).strip()
    if tail:
        result.append(tail)
    return result


def parse_isil_signature(header: str) -> tuple[str, str, list[str]] | None:
    left, separator, right = header.partition("(")
    if not separator or not right.endswith(")"):
        return None
    tokens = left.strip().split()
    if len(tokens) < 2:
        return None
    name = tokens[-1]
    return_type = normalize_type(" ".join(tokens[:-1]))
    parameters: list[str] = []
    for parameter in split_type_list(right[:-1]):
        parameter = re.sub(r"\s*=.*$", "", parameter).strip()
        parameter = re.sub(r"\b(?:ref|out|in|this)\s+", "", parameter)
        tokens = parameter.split()
        if len(tokens) > 1 and re.fullmatch(r"[A-Za-z_]\w*", tokens[-1]):
            parameter = " ".join(tokens[:-1])
        parameters.append(normalize_type(parameter))
    return name, return_type, parameters


def isil_method_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^Method:\s*(.+)$", text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1).strip(), text[match.end():end]))
    return blocks


def parse_isil_facts(text: str, method: dict[str, Any]) -> dict[str, Any]:
    candidates: list[tuple[str, str]] = []
    for header, block in isil_method_blocks(text):
        signature = parse_isil_signature(header)
        if signature is None or signature[0] != method.get("method_name"):
            continue
        candidates.append((header, block))

    exact: list[tuple[str, str]] = []
    expected_return = normalize_type(str(method.get("return_type") or ""))
    expected_parameters = [normalize_type(str(value)) for value in method.get("parameter_types", [])]
    for header, block in candidates:
        signature = parse_isil_signature(header)
        if signature and signature[1] == expected_return and signature[2] == expected_parameters:
            exact.append((header, block))

    selected = exact[0] if len(exact) == 1 else None
    block = selected[1] if selected else ""
    instruction_rows: list[dict[str, Any]] = []
    in_isil = False
    for line in block.splitlines():
        if line.strip() == "ISIL:":
            in_isil = True
            continue
        if not in_isil:
            continue
        match = re.match(r"^\s*(\d+)\s+(.+)$", line)
        if match:
            instruction_rows.append({"index": int(match.group(1)), "text": match.group(2).strip()})

    transfers = [
        row
        for row in instruction_rows
        if re.search(r"\b(?:Jump|ConditionalJump|Switch|Return|Throw)\b", row["text"])
    ]
    calls = [row for row in instruction_rows if re.search(r"\bCall\b", row["text"])]
    branch_targets = sorted({target for row in transfers for target in re.findall(r"@b(\d+)", row["text"])})
    blocks: list[dict[str, Any]] = []
    start = instruction_rows[0]["index"] if instruction_rows else None
    for row in instruction_rows:
        if re.search(r"\b(?:Jump|ConditionalJump|Switch|Return|Throw)\b", row["text"]):
            if start is not None:
                blocks.append({"start": start, "end": row["index"], "terminator": row["text"]})
            start = row["index"] + 1
    if start is not None and instruction_rows:
        last = instruction_rows[-1]["index"]
        if start <= last:
            blocks.append({"start": start, "end": last, "terminator": "FALLTHROUGH"})

    return {
        "file_exists": True,
        "type_header": re.search(r"(?m)^Type:\s*(.+)$", text).group(1).strip() if re.search(r"(?m)^Type:\s*(.+)$", text) else None,
        "method_candidate_count": len(candidates),
        "exact_signature_candidate_count": len(exact),
        "selected_header": selected[0] if selected else None,
        "instruction_count": len(instruction_rows),
        "call_count": len(calls),
        "control_transfer_count": len(transfers),
        "branch_targets": branch_targets,
        "basic_blocks": blocks,
        "instructions": instruction_rows,
        "selection_status": "EXACT_SIGNATURE_UNIQUE" if selected else ("SIGNATURE_AMBIGUOUS" if len(exact) > 1 else "SIGNATURE_NOT_MATCHED"),
    }


def extract_body(text: str, start_line: int | None, end_line: int | None) -> dict[str, Any]:
    if not isinstance(start_line, int) or not isinstance(end_line, int) or start_line < 1 or end_line < start_line:
        return {"status": "NO_LINE_SPAN"}
    lines = text.splitlines(keepends=True)
    if end_line > len(lines):
        return {"status": "LINE_SPAN_OUT_OF_RANGE", "line_count": len(lines)}
    region = "".join(lines[start_line - 1 : end_line])
    open_index = find_code_brace(region)
    if open_index is None:
        arrow = region.find("=>")
        semicolon = region.find(";", arrow + 2) if arrow >= 0 else -1
        if arrow >= 0 and semicolon >= 0:
            body = region[arrow + 2 : semicolon]
            return {"status": "EXPRESSION_BODY", "body": body, "body_sha256": sha256_text(body)}
        return {"status": "METHOD_BODY_NOT_LOCATED"}
    close_index = matching_brace(region, open_index)
    if close_index is None:
        return {"status": "UNBALANCED_BODY"}
    body = region[open_index + 1 : close_index]
    return {
        "status": "EXACT_LINE_SPAN",
        "body": body,
        "body_sha256": sha256_text(body),
        "method_text": region[: close_index + 1],
        "open_index": open_index,
        "close_index": close_index,
    }


def find_code_brace(text: str) -> int | None:
    quote: str | None = None
    escape = False
    line_comment = False
    block_comment = False
    for index, char in enumerate(text):
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
            continue
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue
        if char == "/" and next_char == "/":
            line_comment = True
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            continue
        if char in ('"', "'"):
            quote = char
            continue
        if char == "{":
            return index
    return None


def matching_brace(text: str, open_index: int) -> int | None:
    depth = 0
    quote: str | None = None
    escape = False
    line_comment = False
    block_comment = False
    index = open_index
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
                continue
            index += 1
            continue
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char == "/" and next_char == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in ('"', "'"):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def body_features(body: str) -> dict[str, int]:
    return {
        "body_lines": body.count("\n") + 1,
        "goto_il": len(re.findall(r"\bgoto\s+IL_[0-9A-Fa-f]+", body)),
        "labels": len(re.findall(r"(?m)^\s*IL_[0-9A-Fa-f]+\s*:", body)),
        "while_true": len(re.findall(r"\bwhile\s*\(\s*true\s*\)", body)),
        "switch": len(re.findall(r"\bswitch\s*\(", body)),
        "try": len(re.findall(r"\btry\s*\{", body)),
        "finally": len(re.findall(r"\bfinally\s*\{", body)),
        "catch": len(re.findall(r"\bcatch\b", body)),
        "foreach": len(re.findall(r"\bforeach\s*\(", body)),
        "if": len(re.findall(r"\bif\s*\(", body)),
        "return": len(re.findall(r"\breturn\b", body)),
        "throw": len(re.findall(r"\bthrow\b", body)),
        "note": body.count("Cpp2ILHelpers.NoteDecompilerIssue"),
        "expected": len(re.findall(r"Expected\s+[A-Z0-9]", body)),
        "indirect_jump": len(re.findall(r"Indirect jump|jump table", body, re.IGNORECASE)),
        "object_temp": len(re.findall(r"\bobject\s+(?:obj|num|result|value)\w*\s*=", body)),
        "throw_array": body.count("throw array;"),
        "unsafe_as": body.count("Unsafe.As"),
    }


def classify_family(features: dict[str, int], isil: dict[str, Any]) -> str:
    transfers = isil.get("control_transfer_count", 0)
    branch_targets = len(isil.get("branch_targets", []))
    if features["indirect_jump"] or (features["switch"] and (features["goto_il"] or features["labels"])) or branch_targets >= 4:
        return "SWITCH_OR_JUMP_TABLE_COLLAPSE"
    if features["finally"] and (features["goto_il"] or features["labels"]):
        return "TRY_FINALLY_CFG_COLLAPSE"
    if features["while_true"] and (features["goto_il"] or features["labels"]):
        return "LOOP_CFG_COLLAPSE"
    if features["goto_il"] >= 4 and features["object_temp"] and (features["expected"] or features["note"]):
        return "TYPE_EROSION_PLUS_HEAVY_GOTO"
    if features["goto_il"] >= 1 or (transfers >= 2 and features["labels"] >= 1):
        return "LOCAL_GOTO_BRANCH_CFG"
    if features["switch"]:
        return "SWITCH_STRUCTURAL_DAMAGE"
    if features["note"] and (features["expected"] or features["object_temp"]):
        return "DECOMPILER_TYPE_CFG_DAMAGE"
    if features["while_true"] or features["try"] or features["finally"]:
        return "STRUCTURED_CONTROL_SUSPECT"
    return "OTHER_CFG"


def structural_risk(features: dict[str, int], isil: dict[str, Any]) -> str:
    score = (
        features["goto_il"] * 2
        + features["labels"]
        + features["while_true"] * 4
        + features["switch"] * 4
        + features["finally"] * 4
        + features["indirect_jump"] * 8
        + min(features["note"], 10)
        + min(features["expected"], 10)
        + min(isil.get("control_transfer_count", 0), 10)
    )
    if score <= 5 and features["body_lines"] <= 30:
        return "LOW_STRUCTURAL_COMPLEXITY"
    if score <= 20 and features["body_lines"] <= 100:
        return "MEDIUM_STRUCTURAL_COMPLEXITY"
    return "HIGH_STRUCTURAL_COMPLEXITY"


def source_path(source_root: Path, twin_root: Path, relative: str | None) -> tuple[Path | None, str]:
    relative = normalize_relative(relative)
    if not relative:
        return None, "NO_SOURCE_FILE"
    twin = twin_root / "source" / Path(relative)
    if twin.exists():
        return twin, "R2_TWIN"
    original = source_root / Path(relative)
    if original.exists():
        return original, "ORIGINAL_READ_ONLY"
    return original, "SOURCE_FILE_MISSING"


def identity_root_cause(row: dict[str, Any], body: dict[str, Any], r2_status: dict[str, Any]) -> str:
    if row.get("repair_disposition") == "SOURCE_LIMITED":
        return "SOURCE_LIMITED"
    if body.get("status") in {"NO_LINE_SPAN", "LINE_SPAN_OUT_OF_RANGE", "METHOD_BODY_NOT_LOCATED", "UNBALANCED_BODY"}:
        return "SOURCE_FILE_MISSING" if body.get("status") == "NO_LINE_SPAN" and not row.get("source_file") else "SOURCE_METHOD_NOT_LOCATED"
    if body.get("body_sha256") and row.get("body_sha256") and body["body_sha256"].lower() != str(row["body_sha256"]).lower():
        return "BODY_HASH_DRIFT"
    reason = str(r2_status.get("reason") or "").lower()
    source_match = str(row.get("source_match_status") or "")
    if source_match == "AMBIGUOUS_SOURCE_KEY":
        return "OVERLOAD_OR_SOURCE_AMBIGUITY"
    if "multiple overload" in reason or "multiple" in reason:
        return "ROSLYN_SYMBOL_AMBIGUITY"
    method_name = str(row.get("method_name") or "")
    declaring_type = str(row.get("declaring_type") or "")
    signature = str(row.get("normalized_signature") or "")
    if method_name in {".ctor", ".cctor"}:
        return "CONSTRUCTOR_REPRESENTATION"
    if method_name.startswith(("get_", "set_", "add_", "remove_")):
        return "ACCESSOR_EVENT_REPRESENTATION"
    if "+" in declaring_type or "<" in declaring_type or ">" in declaring_type:
        return "NESTED_OR_COMPILER_GENERATED_TYPE_IDENTITY"
    if "`" in declaring_type or "`" in signature or "!0" in signature or "!!" in signature:
        return "GENERIC_IDENTITY_NORMALIZATION"
    if "&" in signature:
        return "BYREF_REF_OUT_NORMALIZATION"
    if source_match in {"MISSING", "SHORT_TYPE"}:
        return "METADATA_SOURCE_SIGNATURE_DISAGREEMENT"
    return "METADATA_SOURCE_SIGNATURE_DISAGREEMENT"


def r3_status_from_r2(row: dict[str, Any], identity: dict[str, Any]) -> str:
    r2 = identity.get("r2_final_status")
    if r2 == "REPAIRED_CSHARP":
        return "REPAIRED_CSHARP_R2"
    if r2 == "BASELINE_READABLE":
        return "BASELINE_READABLE"
    if r2 == "DEFER_R3_CFG":
        return "DEFER_CFG_UNPROVEN"
    if r2 == "DEFER_R4_NATIVE":
        return "DEFER_R4_NATIVE"
    if r2 == "DEFER_R2_UNPROVEN_MECHANICAL":
        return "DEFER_MECHANICAL_UNPROVEN"
    if r2 == "SOURCE_LIMITED":
        return "SOURCE_LIMITED"
    if r2 != R2_BLOCKED_STATUS:
        return r2 or "UNKNOWN_R2_STATUS"
    if identity.get("source_body_identity_recovered"):
        disposition = row.get("repair_disposition")
        return {
            "VERIFY_ONLY": "BASELINE_READABLE",
            "CFG_REPAIR": "DEFER_CFG_UNPROVEN",
            "ISIL_ASSISTED_REPAIR": "DEFER_R4_NATIVE",
            "AUTO_TYPE_REPAIR": "DEFER_MECHANICAL_UNPROVEN",
            "SOURCE_LIMITED": "SOURCE_LIMITED",
        }.get(disposition, "DEFER_MECHANICAL_UNPROVEN")
    if identity.get("isil_identity_recovered") and row.get("repair_disposition") == "ISIL_ASSISTED_REPAIR":
        return "DEFER_R4_NATIVE"
    return "BLOCKED_IDENTITY"


def source_gate(root: Path, source_root: Path, twin_root: Path) -> dict[str, Any]:
    expected_root = root
    rows: dict[str, Any] = {}
    mismatches: list[str] = []
    repo_root = root.parent.parent
    for name, (relative, expected) in PINNED_INPUTS.items():
        path = repo_root / Path(relative)
        actual = sha256_file(path) if path.exists() else None
        rows[name] = {"path": str(path), "expected_sha256": expected, "actual_sha256": actual, "match": actual == expected}
        if actual != expected:
            mismatches.append(f"{name}:{actual or 'MISSING'}")

    manifest_path = root / "source-file-manifest.json"
    manifest = read_json(manifest_path)
    source_mismatches: list[str] = []
    csharp_files = 0
    csharp_bytes = 0
    zero_byte: list[str] = []
    for item in manifest:
        relative = normalize_relative(item.get("relative_path"))
        path = source_root / Path(relative)
        if not path.exists():
            source_mismatches.append(f"missing:{relative}")
            continue
        if str(item.get("extension", "")).lower() == ".cs":
            csharp_files += 1
            csharp_bytes += path.stat().st_size
            if path.stat().st_size == 0:
                zero_byte.append(relative)
            actual = sha256_file(path)
            if actual.lower() != str(item.get("sha256", "")).lower():
                source_mismatches.append(f"hash:{relative}")

    twin_manifest_path = twin_root / "baseline" / "source-manifest.json"
    twin_manifest = read_json(twin_manifest_path) if twin_manifest_path.exists() else []
    provenance_path = twin_root / "provenance" / "r2-type-canary-001.jsonl"
    provenance = read_jsonl(provenance_path) if provenance_path.exists() else []
    approved_twin_after_hashes: dict[str, set[str]] = defaultdict(set)
    for record in provenance:
        relative = normalize_relative(record.get("source_file"))
        after_hash = str(record.get("after_file_sha256") or "").lower()
        if relative and after_hash:
            approved_twin_after_hashes[relative].add(after_hash)
    twin_mismatches: list[str] = []
    approved_twin_repairs: list[dict[str, Any]] = []
    for item in twin_manifest:
        twin_path = Path(item.get("twin_path", ""))
        original_path = Path(item.get("original_path", ""))
        if not twin_path.exists():
            twin_mismatches.append(f"twin_missing:{item.get('relative_path')}")
            continue
        relative = normalize_relative(item.get("relative_path"))
        actual_twin_hash = sha256_file(twin_path).lower()
        baseline_hash = str(item.get("baseline_sha256", "")).lower()
        if actual_twin_hash != baseline_hash:
            if actual_twin_hash in approved_twin_after_hashes.get(relative, set()):
                approved_twin_repairs.append({
                    "relative_path": relative,
                    "baseline_sha256": baseline_hash,
                    "after_file_sha256": actual_twin_hash,
                })
            else:
                twin_mismatches.append(f"twin_unapproved_hash:{relative}")
        if original_path.exists() and sha256_file(original_path).lower() != str(item.get("original_sha256", "")).lower():
            twin_mismatches.append(f"original_hash:{item.get('relative_path')}")
    return {
        "schema_version": "r3-source-gate-v1",
        "status": "PASS" if not mismatches and not source_mismatches and not twin_mismatches and len(provenance) == 4 else "FAIL",
        "pinned_inputs": rows,
        "source_root": {
            "manifest_file_count": len(manifest),
            "csharp_files": csharp_files,
            "csharp_bytes": csharp_bytes,
            "zero_byte_csharp_files": sorted(zero_byte),
            "mismatches": sorted(source_mismatches),
        },
        "r2_twin": {
            "baseline_manifest_file_count": len(twin_manifest),
            "provenance_count": len(provenance),
            "baseline_mismatches": sorted(twin_mismatches),
            "approved_r2_repair_files": sorted(approved_twin_repairs, key=lambda row: row["relative_path"]),
            "provenance_file": str(provenance_path),
        },
        "identity_mismatches": sorted(mismatches),
        "original_source_read_only": True,
        "source_root_path": str(source_root),
        "twin_root_path": str(twin_root),
    }


def edge_indexes(artifact_root: Path) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    callers: dict[str, list[dict[str, Any]]] = defaultdict(list)
    fields: dict[str, list[dict[str, Any]]] = defaultdict(list)
    static_refs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(artifact_root / "call-edges.jsonl"):
        callers[row.get("caller_method_id", "")].append({"direction": "callee", **row})
        callers[row.get("callee_method_id", "")].append({"direction": "caller", **row})
    for row in read_jsonl(artifact_root / "field-edges.jsonl"):
        fields[row.get("source_method_id", "")].append(row)
    for row in read_jsonl(artifact_root / "static-data-edges.jsonl"):
        static_refs[row.get("source_method_id", "")].append(row)
    return callers, fields, static_refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Canonical R3 prework profiler")
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--twin-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact_root = Path(args.artifact_root).resolve()
    twin_root = Path(args.twin_root).resolve()
    source_root = Path(args.source_root).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    methods = read_jsonl(artifact_root / "method-catalog.jsonl")
    methods_by_id = {row["method_id"]: row for row in methods}
    queue = read_jsonl(artifact_root / "repair-queue.jsonl")
    r2_statuses = read_jsonl(twin_root / "queue" / "r2-method-status-after.jsonl")
    status_by_id = {row["method_id"]: row for row in r2_statuses}
    if len(methods) != 10827 or len(queue) != 10827 or len(status_by_id) != 10827:
        raise SystemExit("R3_PREWORK_FAIL: canonical method/queue/status coverage is not 10,827")

    gate = source_gate(artifact_root, source_root, twin_root)
    write_json(out / "r3-source-gate.json", gate)
    if gate["status"] != "PASS":
        raise SystemExit("R3_PREWORK_FAIL: source or R2 Twin identity gate failed")

    callers, field_edges, static_refs = edge_indexes(artifact_root)
    source_cache: dict[Path, str] = {}
    isil_cache: dict[Path, str] = {}
    mapping_counts = Counter()
    identity_counts = Counter()
    family_counts = Counter()
    risk_counts = Counter()
    family_risk = Counter()
    core_counts: dict[str, Counter[str]] = defaultdict(Counter)
    representative_samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    blocked_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    final_status_counts = Counter()
    identity_resolved = Counter()
    identity_by_id: dict[str, dict[str, Any]] = {}

    def load_source(path: Path) -> str:
        if path not in source_cache:
            source_cache[path] = path.read_text(encoding="utf-8", errors="replace")
        return source_cache[path]

    def load_isil(path: Path) -> str:
        if path not in isil_cache:
            isil_cache[path] = path.read_text(encoding="utf-8", errors="replace")
        return isil_cache[path]

    for status_row in sorted(r2_statuses, key=lambda row: row["method_id"]):
        method = methods_by_id[status_row["method_id"]]
        r2_final = status_row.get("final_status")
        path, source_origin = source_path(source_root, twin_root, method.get("source_file"))
        source_text = load_source(path) if path and path.exists() else ""
        body = extract_body(source_text, method.get("source_line"), method.get("source_line_end")) if source_text else {
            "status": "SOURCE_FILE_MISSING" if method.get("source_file") else "NO_LINE_SPAN"
        }
        body_hash_matches = bool(body.get("body_sha256") and method.get("body_sha256") and body["body_sha256"].lower() == str(method["body_sha256"]).lower())
        if body.get("status") == "EXACT_LINE_SPAN" and body_hash_matches:
            mapping = "EXACT_R1_5_LINE_SPAN_BODY_HASH"
        elif body.get("status") == "EXPRESSION_BODY" and body_hash_matches:
            mapping = "EXACT_R1_5_EXPRESSION_BODY_HASH"
        elif body.get("status") == "SOURCE_FILE_MISSING":
            mapping = "SOURCE_FILE_MISSING"
        elif body.get("status") == "NO_LINE_SPAN":
            mapping = "NO_CANONICAL_LINE_SPAN"
        elif body.get("status") == "METHOD_BODY_NOT_LOCATED":
            mapping = "METHOD_BODY_NOT_LOCATED"
        elif body_hash_matches:
            mapping = "BODY_HASH_MATCH_WITH_NONSTANDARD_SPAN"
        else:
            mapping = "BODY_HASH_DRIFT_OR_UNAVAILABLE"
        mapping_counts[mapping] += 1

        isil_facts: dict[str, Any] = {"file_exists": False, "selection_status": "NO_ISIL_FILE"}
        isil_path = Path(str(method.get("isil_evidence_file") or ""))
        if isil_path.exists():
            isil_facts = parse_isil_facts(load_isil(isil_path), method)
        source_body_identity_recovered = mapping in {"EXACT_R1_5_LINE_SPAN_BODY_HASH", "EXACT_R1_5_EXPRESSION_BODY_HASH", "BODY_HASH_MATCH_WITH_NONSTANDARD_SPAN"}
        isil_identity_recovered = isil_facts.get("selection_status") == "EXACT_SIGNATURE_UNIQUE"
        identity = {
            "r2_final_status": r2_final,
            "source_origin": source_origin,
            "mapping": mapping,
            "body_hash_matches": body_hash_matches,
            "source_body_identity_recovered": source_body_identity_recovered,
            "isil_identity_recovered": isil_identity_recovered,
        }
        identity_by_id[method["method_id"]] = identity
        r3_status = r3_status_from_r2(method, identity)
        final_status_counts[r3_status] += 1

        if r2_final == R2_BLOCKED_STATUS:
            root_cause = identity_root_cause(method, body, status_row)
            identity_counts[root_cause] += 1
            if source_body_identity_recovered:
                identity_resolved["SOURCE_BODY_IDENTITY_RECOVERED"] += 1
            elif isil_identity_recovered:
                identity_resolved["ISIL_IDENTITY_RECOVERED"] += 1
            else:
                identity_resolved["UNRESOLVED"] += 1
            blocked_rows.append({
                **method,
                "r2_status": status_row,
                "r3_identity_root_cause": root_cause,
                "r3_identity": identity,
                "r3_status": r3_status,
                "isil_facts_summary": {
                    key: value
                    for key, value in isil_facts.items()
                    if key not in {"instructions", "basic_blocks"}
                },
            })

        if r3_status == "DEFER_CFG_UNPROVEN":
            if not source_body_identity_recovered:
                continue
            body_text = body.get("body", "")
            features = body_features(body_text)
            family = classify_family(features, isil_facts)
            risk = structural_risk(features, isil_facts)
            family_counts[family] += 1
            risk_counts[risk] += 1
            family_risk[(family, risk)] += 1
            core = str(method.get("declaring_type", "")).split(".")[-1].split("+")[-1].split("`")[0]
            core_counts[core][family] += 1
            if len(representative_samples[family]) < 12:
                representative_samples[family].append({
                    "method_id": method["method_id"],
                    "assembly": method.get("assembly"),
                    "declaring_type": method.get("declaring_type"),
                    "method_name": method.get("method_name"),
                    "source_file": method.get("source_file"),
                    "structural_risk": risk,
                    "features": features,
                    "isil_control_transfer_count": isil_facts.get("control_transfer_count", 0),
                })
            profile_row = {
                **method,
                "r2_status": status_row,
                "r3_status": r3_status,
                "source_origin": source_origin,
                "source_mapping": mapping,
                "source_body": body_text,
                "source_body_sha256": body.get("body_sha256"),
                "cfg_family": family,
                "structural_risk": risk,
                "features": features,
                "isil_path": str(isil_path) if isil_path else None,
                "isil_facts": isil_facts,
                "roslyn": {
                    "syntax_diagnostics_before": status_row.get("syntax_diagnostics_before"),
                    "semantic_diagnostics_available": False,
                    "semantic_diagnostics_note": "R2 Roslyn plan evidence is syntax-only; full semantic compilation is unavailable for the external-reference corpus.",
                },
                "callers_callees": callers.get(method["method_id"], []),
                "field_edges": field_edges.get(method["method_id"], []),
                "static_data_refs": static_refs.get(method["method_id"], []),
                "accepted_evidence_refs": method.get("evidence_refs", []),
            }
            profile_rows.append(profile_row)
            bundle_path = out / "bundles" / f"{method['method_id']}.json"
            write_json(bundle_path, {
                "schema_version": "r3-cfg-evidence-bundle-v1",
                "method_id": method["method_id"],
                "assembly": method.get("assembly"),
                "declaring_type": method.get("declaring_type"),
                "exact_signature": method.get("normalized_signature"),
                "metadata_token": method.get("metadata_token"),
                "rva": method.get("rva"),
                "source_file": method.get("source_file"),
                "source_origin": source_origin,
                "source_line": method.get("source_line"),
                "source_line_end": method.get("source_line_end"),
                "source_body": body_text,
                "before_body_sha256": method.get("body_sha256"),
                "r0_quality_signals": method.get("r0_signals", {}),
                "r1_5_source_match": {
                    "source_match_status": method.get("source_match_status"),
                    "source_present": method.get("source_present"),
                    "source_body_present": method.get("source_body_present"),
                    "body_sha256": method.get("body_sha256"),
                },
                "isil": {
                    "evidence_file": str(isil_path) if isil_path else None,
                    "facts": isil_facts,
                },
                "callers_callees": callers.get(method["method_id"], []),
                "field_reads_writes": field_edges.get(method["method_id"], []),
                "static_data_refs": static_refs.get(method["method_id"], []),
                "accepted_brain_native_evidence_refs": method.get("evidence_refs", []),
                "roslyn": {
                    "syntax_diagnostics_before": status_row.get("syntax_diagnostics_before"),
                    "semantic_diagnostics_available": False,
                    "semantic_diagnostics_note": "Full semantic compilation is unavailable; parse-only evidence is not treated as equivalence proof.",
                },
                "classification": {
                    "cfg_family": family,
                    "structural_risk": risk,
                    "features": features,
                },
            })

    for root_cause in ROOT_CAUSES:
        identity_counts.setdefault(root_cause, 0)
    write_jsonl(out / "r3-cfg-profile.jsonl", profile_rows)
    write_jsonl(out / "r3-blocked-identity.jsonl", blocked_rows)
    write_jsonl(out / "r3-method-status.jsonl", [
        {
            "method_id": method["method_id"],
            "r2_status": status_by_id[method["method_id"]].get("final_status"),
            "r3_status": r3_status_from_r2(method, identity_by_id[method["method_id"]]),
            "identity": identity_by_id[method["method_id"]],
        }
        for method in sorted(methods, key=lambda row: row["method_id"])
    ])
    write_json(out / "r3-cfg-family-summary.json", {
        "schema_version": "r3-cfg-family-summary-v1",
        "active_cfg_count": len(profile_rows),
        "mapping_counts": dict(sorted(mapping_counts.items())),
        "family_counts": dict(sorted(family_counts.items())),
        "risk_counts": dict(sorted(risk_counts.items())),
        "family_risk_matrix": [
            {"family": family, "risk": risk, "count": count}
            for (family, risk), count in sorted(family_risk.items())
        ],
        "per_core_class": {
            core: dict(sorted(counter.items())) for core, counter in sorted(core_counts.items())
        },
        "representatives": {family: rows for family, rows in sorted(representative_samples.items())},
    })
    write_json(out / "r3-identity-recovery-summary.json", {
        "schema_version": "r3-identity-recovery-summary-v1",
        "blocked_identity_start": sum(1 for row in r2_statuses if row.get("final_status") == R2_BLOCKED_STATUS),
        "root_cause_counts": dict(sorted(identity_counts.items())),
        "recovery_counts": dict(sorted(identity_resolved.items())),
        "resolved_total": sum(value for key, value in identity_resolved.items() if key != "UNRESOLVED"),
        "unresolved_total": identity_resolved.get("UNRESOLVED", 0),
        "routing": [
            {
                "mapping": mapping,
                "r3_status": r3_status,
                "count": count,
            }
            for (mapping, r3_status), count in sorted(Counter(
                (row["r3_identity"]["mapping"], row["r3_status"])
                for row in blocked_rows
            ).items())
        ],
        "minimum_root_cause_vocabulary": ROOT_CAUSES,
        "source_bodies_changed": False,
    })
    write_json(out / "r3-canonical-prework.json", {
        "schema_version": "r3-canonical-prework-v1",
        "status": "PASS",
        "r2_status_counts": dict(sorted(Counter(row.get("final_status") for row in r2_statuses).items())),
        "r3_status_counts": dict(sorted(final_status_counts.items())),
        "canonical_target_types": 641,
        "canonical_method_count": len(methods),
        "canonical_queue_count": len(queue),
        "r2_direct_cfg_count": sum(1 for row in r2_statuses if row.get("final_status") == R3_CFG_STATUS),
        "r3_active_cfg_count": len(profile_rows),
        "blocked_identity_count": sum(1 for row in r2_statuses if row.get("final_status") == R2_BLOCKED_STATUS),
        "source_gate": str(out / "r3-source-gate.json"),
        "identity_summary": str(out / "r3-identity-recovery-summary.json"),
        "cfg_family_summary": str(out / "r3-cfg-family-summary.json"),
        "evidence_bundle_count": len(profile_rows),
        "exact_mapping_required": True,
        "fallback_mapping_is_diagnostic_only": True,
        "native_body_lift_started": False,
    })
    print(json.dumps({
        "status": "PASS",
        "canonical_methods": len(methods),
        "r2_direct_cfg": sum(1 for row in r2_statuses if row.get("final_status") == R3_CFG_STATUS),
        "active_cfg": len(profile_rows),
        "blocked_identity": sum(1 for row in r2_statuses if row.get("final_status") == R2_BLOCKED_STATUS),
        "identity_recovery": dict(sorted(identity_resolved.items())),
        "families": dict(sorted(family_counts.items())),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
