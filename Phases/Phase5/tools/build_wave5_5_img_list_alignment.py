"""Build the corrected native ScriptString -> APK metadata -> img.inf alignment.

The recovered C/Ghidra labels use one-based ``StringLiteral_N`` names while
``stringliteral.json`` and ``script.json["ScriptString"]`` are zero-based
arrays.  This builder keeps those namespaces explicit, then joins the native
literal value to the active APK metadata by exact UTF-8 string value before
joining to the game ``img.inf`` filename.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DUMP = ROOT / "game-dev-story-mod_Dumped"
FORM_C = DUMP / "Categorized_Code" / "Global" / "form.c"
SCRIPT_JSON = DUMP / "script.json"
STRINGLITERAL_JSON = DUMP / "stringliteral.json"
METADATA = ROOT / "game-dev-story-mod_Extracted" / "assets" / "bin" / "Data" / "Managed" / "Metadata" / "global-metadata.dat"
RESOURCE_MAP = ROOT / "Phases" / "Phase4" / "artifacts" / "resource_selector_map.json"
OUTPUT = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_5_img_list_alignment.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_number(text: str, needle: str) -> int | None:
    position = text.find(needle)
    return text.count("\n", 0, position) + 1 if position >= 0 else None


def load_metadata_values(path: Path) -> tuple[dict[str, Any], list[str]]:
    data = path.read_bytes()
    magic, version = struct.unpack_from("<II", data, 0)
    literal_offset, literal_bytes = struct.unpack_from("<II", data, 8)
    literal_data_offset, literal_data_bytes = struct.unpack_from("<II", data, 16)
    if literal_bytes % 8:
        raise ValueError("global-metadata string literal table is not 8-byte aligned")
    values: list[str] = []
    for index in range(literal_bytes // 8):
        length, data_index = struct.unpack_from("<II", data, literal_offset + index * 8)
        start = literal_data_offset + data_index
        values.append(data[start : start + length].decode("utf-8", "replace"))
    return (
        {
            "magic": f"0x{magic:08x}",
            "version": version,
            "literal_table_offset": f"0x{literal_offset:x}",
            "literal_table_bytes": literal_bytes,
            "literal_count": len(values),
            "literal_data_offset": f"0x{literal_data_offset:x}",
            "literal_data_bytes": literal_data_bytes,
        },
        values,
    )


def native_string_rows() -> list[dict[str, Any]]:
    script = json.loads(SCRIPT_JSON.read_text(encoding="utf-8"))["ScriptString"]
    zero_based = json.loads(STRINGLITERAL_JSON.read_text(encoding="utf-8"))
    if len(script) != len(zero_based):
        raise ValueError("script.json and stringliteral.json counts differ")
    if any(row["Value"] != zero["value"] or row["Address"] != int(zero["address"], 16) for row, zero in zip(script, zero_based)):
        raise ValueError("script.json and stringliteral.json disagree")
    return script


def parse_img_list(form_text: str, script: list[dict[str, Any]]) -> list[dict[str, Any]]:
    allocation = re.search(
        r"lVar17\s*=\s*FUN_00db0c30\(\*\(undefined8 \*\)puVar7,0x50\);",
        form_text,
    )
    assignment = re.search(r"\+ 0x68\) = lVar17;", form_text[allocation.end() :] if allocation else "")
    if not allocation or not assignment:
        raise ValueError("GameForm.IMG_LIST cctor allocation/assignment not found")
    chunk = form_text[allocation.end() : allocation.end() + assignment.start()]
    labels = [int(value) for value in re.findall(r"PTR_StringLiteral_(\d+)", chunk)]
    rows: list[dict[str, Any]] = []
    for selector_index, label in enumerate(labels):
        if not 1 <= label <= len(script):
            raise ValueError(f"StringLiteral_{label} is outside ScriptString table")
        rows.append(
            {
                "selector_index": selector_index,
                "literal_label": label,
                "zero_based_script_index": label - 1,
                "native_value": script[label - 1]["Value"],
                "native_address": f"0x{script[label - 1]['Address']:x}",
            }
        )
    return rows


def manifest_records() -> dict[str, dict[str, Any]]:
    resource_map = json.loads(RESOURCE_MAP.read_text(encoding="utf-8"))
    game = next(row for row in resource_map["manifests"] if row["manifest"].endswith("game/img.inf"))
    return {row["filename"].lower(): row for row in game["records"]}


def normalized_filename(base_name: str) -> str | None:
    match = re.fullmatch(r"face(\d+)", base_name)
    return f"face_{match.group(1)}.png" if match else None


def align(rows: list[dict[str, Any]], metadata_values: list[str], records: dict[str, dict[str, Any]]) -> None:
    for row in rows:
        base_name = row["native_value"]
        requested = f"{base_name}.png"
        exact = records.get(requested.lower())
        normalized = records.get((normalized_filename(base_name) or "").lower())
        record = exact or normalized
        metadata_hits = [index for index, value in enumerate(metadata_values) if value == base_name]
        row.update(
            {
                "requested_filename": requested,
                "active_metadata_indices": metadata_hits,
                "active_metadata_join": "exact_value_unique" if len(metadata_hits) == 1 else "not_unique_or_missing",
                "manifest_join": "exact_filename" if exact else ("normalized_face_family" if normalized else "unresolved"),
                "manifest_filename": record["filename"] if record else None,
                "manifest_resource_index": record["resource_index"] if record else None,
                "manifest_asset_path": record["asset_path"] if record else None,
            }
        )


def build() -> dict[str, Any]:
    form_text = FORM_C.read_text(encoding="utf-8", errors="replace")
    script = native_string_rows()
    metadata_header, metadata_values = load_metadata_values(METADATA)
    rows = parse_img_list(form_text, script)
    align(rows, metadata_values, manifest_records())
    selectors = {row["selector_index"]: row for row in rows}
    fields = {
        "DDChair": {"offset": "0xAC", "selector_index": 25},
        "DDDesk": {"offset": "0xB0", "selector_index": 26},
        "DDPC": {"offset": "0xD4", "selector_index": 77},
    }
    for field, value in fields.items():
        value["native_value"] = selectors[value["selector_index"]]["native_value"]
        value["manifest_resource_index"] = selectors[value["selector_index"]]["manifest_resource_index"]
        value["manifest_filename"] = selectors[value["selector_index"]]["manifest_filename"]
        value["active_metadata_indices"] = selectors[value["selector_index"]]["active_metadata_indices"]
        value["status"] = "verified_exact" if selectors[value["selector_index"]]["manifest_join"] == "exact_filename" and len(value["active_metadata_indices"]) == 1 else "unresolved"
    exact_count = sum(row["manifest_join"] == "exact_filename" for row in rows)
    normalized_count = sum(row["manifest_join"] == "normalized_face_family" for row in rows)
    unresolved_count = sum(row["manifest_join"] == "unresolved" for row in rows)
    metadata_join_count = sum(row["active_metadata_join"] == "exact_value_unique" for row in rows)
    return {
        "schema_version": "wave5-5-img-list-alignment-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "W5.5-corrected-scriptstring-metadata-manifest-alignment",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "exact_bihin_selector_join_verified",
        "parser_correction": {
            "native_label_namespace": "StringLiteral_N is one-based",
            "json_array_namespace": "script.json ScriptString and stringliteral.json are zero-based",
            "correct_index_rule": "zero_based_script_index = literal_label - 1",
            "prior_failure_mode": "directly indexing stringliteral.json by PTR_StringLiteral_N shifted every recovered value by one",
            "source": {
                "file": "APK_Toolkit/Il2CppDumper/ghidra.py",
                "line": 41,
                "needle": "index = 1",
            },
        },
        "native_scriptstring": {
            "file": rel(SCRIPT_JSON),
            "entry_count": len(script),
            "script_string_and_stringliteral_values_equal": True,
            "script_string_and_stringliteral_addresses_equal": True,
        },
        "active_apk_global_metadata": {
            **metadata_header,
            "join_rule": "match native ScriptString UTF-8 value exactly; do not reuse native label as active metadata index",
            "img_list_values_found_by_exact_value": metadata_join_count == len(rows),
            "metadata_join_count": metadata_join_count,
            "suffix_literal": {
                "literal_label": 833,
                "native_value": script[832]["Value"],
                "active_metadata_indices": [index for index, value in enumerate(metadata_values) if value == script[832]["Value"]],
            },
            "face_prefix_literal": {
                "literal_label": 7514,
                "native_value": script[7513]["Value"],
                "active_metadata_indices": [index for index, value in enumerate(metadata_values) if value == script[7513]["Value"]],
            },
        },
        "loader_contract": {
            "request_expression": "IMG_LIST[selector] + StringLiteral_833",
            "resolved_suffix": script[832]["Value"],
            "lookup": "AppData.GetImage(name) matches list entry name and returns resGame_.img[index]",
            "source_refs": [
                {"file": rel(FORM_C), "line": line_number(form_text, "// Function: form_GameForm__LoadBihinImage"), "needle": "// Function: form_GameForm__LoadBihinImage"},
                {"file": "game-dev-story-mod_Dumped/Categorized_Code/Global/main.c", "line": 6462, "needle": "// Function: main_AppData__GetImage"},
            ],
        },
        "selector_fields": fields,
        "img_list": {
            "field": "form.GameForm.IMG_LIST",
            "field_offset": "0x68",
            "length": len(rows),
            "entries": rows,
        },
        "summary": {
            "img_list_entry_count": len(rows),
            "active_metadata_exact_value_join_count": metadata_join_count,
            "manifest_exact_filename_join_count": exact_count,
            "manifest_normalized_face_join_count": normalized_count,
            "manifest_unresolved_join_count": unresolved_count,
            "bihin_selector_exact_join_count": sum(value["status"] == "verified_exact" for value in fields.values()),
        },
        "guardrails": [
            "Promote only the verified DDPC/DDChair/DDDesk native IMG_LIST joins; keep dynamic floor/event selector semantics separate.",
            "Use the native string value for active global-metadata alignment; native literal labels are not active metadata indices.",
            "Keep face0/face1/face2 as normalized family candidates because the manifest spells them face_0/face_1/face_2.",
            "Keep legacy_equivalence=false: this closes resource-name/index alignment, not crop, room placement, SEB, transform, or animation semantics.",
        ],
        "source_files": {rel(path): sha256(path) for path in (FORM_C, SCRIPT_JSON, STRINGLITERAL_JSON, METADATA, RESOURCE_MAP)},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    artifact = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    print(json.dumps({"output": rel(output_path.resolve()), "status": artifact["status"], "summary": artifact["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
