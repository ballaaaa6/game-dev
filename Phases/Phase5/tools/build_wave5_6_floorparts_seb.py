"""Build the W5.6 floor-parts selector and SEB structural evidence artifact.

This pass closes the selector-to-IMG_LIST join that was still dynamic in W5.3,
then records the SEB loader's structural contract without inventing room,
pivot, or transform semantics for the truncated legacy files.
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
KAIRO_C = DUMP / "Categorized_Code" / "Global" / "kairo.c"
SCRIPT_JSON = DUMP / "script.json"
W53 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_3_numeric_crop_placement_contract.json"
W55 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_5_img_list_alignment.json"
SEB_MANIFEST = ROOT / "Phases" / "Phase1" / "artifacts" / "phase1_seb_manifest.json"
SEB_PATH = ROOT / "game-dev-story-mod_Sprites" / "office" / "floor0.seb"
OUTPUT = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_6_floorparts_seb_contract.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_number(text: str, needle: str, start: int = 0) -> int | None:
    position = text.find(needle, start)
    return text.count("\n", 0, position) + 1 if position >= 0 else None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_expression(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_mode_one_calls(form_text: str) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    needle = "form_GameForm__EventGChange"
    search_start = 0
    while True:
        function_start = form_text.find(needle, search_start)
        if function_start < 0:
            break
        open_paren = form_text.find("(", function_start + len(needle))
        if open_paren < 0:
            break
        depth = 0
        close_paren = None
        for position in range(open_paren, len(form_text)):
            char = form_text[position]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    close_paren = position
                    break
        if close_paren is None:
            break
        arguments: list[str] = []
        argument_start = open_paren + 1
        depth = 0
        for position in range(open_paren + 1, close_paren):
            char = form_text[position]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                arguments.append(form_text[argument_start:position].strip())
                argument_start = position + 1
        arguments.append(form_text[argument_start:close_paren].strip())
        search_start = close_paren + 1
        if len(arguments) < 3 or arguments[1] != "1":
            continue
        expression = normalize_expression(arguments[2])
        line = form_text.count("\n", 0, function_start) + 1
        resolved_selector = None
        resolution = "dynamic_selector_expression"
        if "0xbc" in expression and re.search(r"\+ 3$", expression):
            resolved_selector = "DDFloor + 3"
            resolution = "initial_floor_parts_call_expression"
        calls.append(
            {
                "source_line": line,
                "receiver_expression": normalize_expression(arguments[0]),
                "selector_expression": expression,
                "resolution": resolution,
                "resolved_selector_expression": resolved_selector,
            }
        )
    return calls


def decode_seb(data: bytes) -> dict[str, Any]:
    if len(data) < 8:
        raise ValueError("SEB sample is shorter than the structural header")

    format_selector = data[0]
    if format_selector & 0x80:
        raise ValueError("W5.6 sample is not the local_104=0 SEB variant")
    group_count = data[1]
    max_frame = struct.unpack_from(">h", data, 2)[0]
    cursor = 4
    groups: list[dict[str, Any]] = []
    field_names = [
        "frame",
        "texture_id",
        "u",
        "v",
        "w",
        "h",
        "trans_x",
        "trans_y",
        "reverse_u",
        "reverse_v",
    ]
    for group_index in range(group_count):
        if cursor + 4 > len(data):
            raise ValueError("SEB sample ends before group header")
        group_offset = cursor
        group_id, record_count = struct.unpack_from(">hh", data, cursor)
        cursor += 4
        records: list[dict[str, Any]] = []
        for record_index in range(record_count):
            record_offset = cursor
            expected_bytes = 20
            available_bytes = min(expected_bytes, max(0, len(data) - cursor))
            raw = data[cursor : cursor + available_bytes]
            available_short_count = len(raw) // 2
            decoded = [struct.unpack_from(">h", raw, index * 2)[0] for index in range(available_short_count)]
            fields = {name: decoded[index] for index, name in enumerate(field_names[:available_short_count])}
            missing_fields = field_names[available_short_count:]
            records.append(
                {
                    "index": record_index,
                    "offset": record_offset,
                    "expected_bytes": expected_bytes,
                    "available_bytes": available_bytes,
                    "fields": fields,
                    "missing_fields": missing_fields,
                    "complete": available_bytes == expected_bytes,
                    "status": "complete" if available_bytes == expected_bytes else "partial_final_record",
                    "raw_hex": raw.hex(),
                }
            )
            cursor += available_bytes
        groups.append(
            {
                "index": group_index,
                "offset": group_offset,
                "record_count": record_count,
                "group_id": group_id,
                "header_bytes": 4,
                "records": records,
                "status": "complete" if all(record["complete"] for record in records) else "truncated_record",
            }
        )

    expected_bytes = 4 + sum(4 + sum(record["expected_bytes"] for record in group["records"]) for group in groups)
    return {
        "format_selector_byte": format_selector,
        "format_code": 0,
        "group_count": group_count,
        "max_frame": max_frame,
        "header_bytes": 4,
        "groups": groups,
        "bytes_consumed": cursor,
        "expected_bytes": expected_bytes,
        "trailing_bytes": max(0, len(data) - cursor),
        "tail_shortfall_bytes": max(0, expected_bytes - len(data)),
        "raw_hex": data.hex(),
        "status": "complete" if cursor == expected_bytes else "truncated_final_record",
    }


def build() -> dict[str, Any]:
    form_text = FORM_C.read_text(encoding="utf-8", errors="replace")
    kairo_text = KAIRO_C.read_text(encoding="utf-8", errors="replace")
    w53 = load_json(W53)
    w55 = load_json(W55)
    phase1_seb = load_json(SEB_MANIFEST)
    script = load_json(SCRIPT_JSON)["ScriptString"]

    event_line = line_number(form_text, "// Function: form_GameForm__EventGChange")
    event_start = form_text.find("// Function: form_GameForm__EventGChange")
    mode1_position = form_text.find("if (param_2 == 1) {", event_start)
    mode0_position = form_text.find("else if (param_2 == 0) {", event_start)
    mode1_start = line_number(form_text, "if (param_2 == 1) {", event_start)
    mode0_start = line_number(form_text, "else if (param_2 == 0) {", event_start)
    mode1_store = line_number(form_text, "0x1188) = param_3;", event_start)
    mode1_load = line_number(form_text, "main_AppData__GetImage(lVar4,uVar5,0)", mode1_position)
    mode0_add = line_number(form_text, "param_3 = iVar1 + param_3;", event_start)
    mode1_calls = extract_mode_one_calls(form_text)

    selector_fields = {item["name"]: item["value"] for item in w53["selector_decode"]["fields"]}
    dd_floor = w53["selector_decode"]["neighbor_values_decoded_for_audit"]["DDFloor"]
    img_entries = {item["selector_index"]: item for item in w55["img_list"]["entries"]}
    floor_parts_entry = img_entries[dd_floor + 3]
    floor_main_rows = []
    for input_selector in range(3):
        final_selector = dd_floor + input_selector
        entry = img_entries[final_selector]
        floor_main_rows.append(
            {
                "caller_input_selector": input_selector,
                "base_field": "DDFloor",
                "base_value": dd_floor,
                "resolved_img_list_selector": final_selector,
                "native_value": entry["native_value"],
                "requested_filename": entry["requested_filename"],
                "manifest_resource_index": entry["manifest_resource_index"],
                "manifest_asset_path": entry["manifest_asset_path"],
                "status": "exact_img_list_metadata_manifest_join",
            }
        )

    seb_bytes = SEB_PATH.read_bytes()
    seb_decoded = decode_seb(seb_bytes)
    seb_entry = next(item for item in phase1_seb["files"] if item["relative_path"] == "office/floor0.seb")
    if seb_entry["sha256"] != sha256(SEB_PATH):
        raise ValueError("floor0.seb does not match the Phase1 SEB manifest")
    if seb_entry["size_bytes"] != len(seb_bytes):
        raise ValueError("floor0.seb size does not match the Phase1 SEB manifest")
    if seb_decoded["tail_shortfall_bytes"] != seb_entry["tail_shortfall_bytes"]:
        raise ValueError("independent SEB decode disagrees with the Phase1 tail shortfall")

    rect_label = 4798
    rect_literal = script[rect_label - 1]
    loader_start = line_number(kairo_text, "// Function: kairo_unity_ui_Seb___load")
    loader_read_header = line_number(kairo_text, "uVar24 = java_io_DataInputStream__ReadByte(plVar31,0);", kairo_text.find("// Function: kairo_unity_ui_Seb___load"))
    loader_record = line_number(kairo_text, "if (local_104 == 0) {", kairo_text.find("// Function: kairo_unity_ui_Seb___load"))
    loader_rect = line_number(kairo_text, "System_String__op_Equality", kairo_text.find("// Function: kairo_unity_ui_Seb___load"))

    phase1_summary = {
        "manifest_file_count": phase1_seb["counts"]["files"],
        "legacy_ten_short_record_count": phase1_seb["counts"]["by_format"].get("legacy_ten_short_record"),
        "tail_shortfall_file_count": phase1_seb["counts"]["tail_shortfall_files"],
        "policy": "preserve truncated records; do not synthesize missing bytes",
    }

    return {
        "schema_version": "wave5-6-floorparts-seb-contract-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "W5.6-IndexImgFloorParts-and-SEB-structural-trace",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "floorparts_selector_exact_seb_structure_verified_room_placement_open",
        "index_img_floor_parts": {
            "field": "IndexImgFloorParts",
            "offset": "0x1188",
            "initial_value": w53["floor_parts_selector"]["initial_value"],
            "initializer_provenance": w53["floor_parts_selector"]["initializer_provenance"],
            "event_g_change": {
                "function": "form_GameForm__EventGChange",
                "source_file": rel(FORM_C),
                "function_line": event_line,
                "mode_1_branch_lines": [mode1_start, (mode0_start - 1) if mode0_start else None],
                "mode_1_branch": {
                    "condition": "param_2 == 1",
                    "compare": "GameForm+0x1188 != param_3",
                    "clear_image_slot": "GameForm+0x1128 (imgFloorParts)",
                    "store_selector": "GameForm+0x1188 = param_3",
                    "request": "IMG_LIST[param_3] + StringLiteral_833",
                    "load_suffix": ".png",
                    "image_loader": "AppData.GetImage",
                    "store_image_slot": "GameForm+0x1128 (imgFloorParts)",
                    "source_lines": {
                        "store_selector": mode1_store,
                        "load_request": mode1_load,
                    },
                    "fixed_runtime_selector": False,
                },
            },
            "initial_callsite_resolution": {
                "field": "DDFloor",
                "field_offset": "0xBC",
                "field_value": dd_floor,
                "expression": "DDFloor + 3",
                "resolved_selector": dd_floor + 3,
                "img_list_value": floor_parts_entry["native_value"],
                "requested_filename": floor_parts_entry["requested_filename"],
                "manifest_resource_index": floor_parts_entry["manifest_resource_index"],
                "manifest_asset_path": floor_parts_entry["manifest_asset_path"],
                "callsite_count_resolved": sum(item["resolution"] == "initial_floor_parts_call_expression" for item in mode1_calls),
                "status": "exact_value_join_verified",
            },
            "mode_1_callsites": mode1_calls,
        },
        "index_img_floor_main": {
            "field": "IndexImgFloorMain",
            "offset": "0x1180",
            "branch_formula": "resolved_selector = DDFloor + param_3",
            "branch_source_line": mode0_add,
            "verified_input_range_probe": floor_main_rows,
            "status": "bounded_floor0_floor1_floor2_selector_join_verified",
        },
        "seb_loader": {
            "function": "kairo_unity_ui_Seb___load",
            "source_file": rel(KAIRO_C),
            "source_lines": {
                "function": loader_start,
                "header_read": loader_read_header,
                "legacy_record_decode": loader_record,
                "optional_rect_marker": loader_rect,
            },
            "format_selector": {
                "sample_value": 0,
                "local_104": 0,
                "header_rule": "read first byte and second byte as group-count selector, then ReadShort max_frame",
            },
            "record_contract": {
                "group_header": ["group_id", "record_count"],
                "record_expected_bytes": 20,
                "structural_field_names": [
                    "frame",
                    "texture_id",
                    "u",
                    "v",
                    "w",
                    "h",
                    "trans_x",
                    "trans_y",
                    "reverse_u",
                    "reverse_v",
                ],
                "field_semantics": "unknown; names remain parser-level labels only",
            },
            "optional_tail": {
                "ascii_marker_literal_label": rect_label,
                "ascii_marker_value": rect_literal["Value"],
                "behavior": "when a trailing chunk is present, compare its first four ASCII bytes with RECT and decode Rect shorts",
                "floor0_present": False,
                "floor0_reason": "the sample ends inside the final record and has no trailing bytes",
            },
        },
        "seb_sample": {
            "source_file": rel(SEB_PATH),
            "manifest_entry": seb_entry,
            "independent_decode": seb_decoded,
            "phase1_summary": phase1_summary,
            "asset_pair": {
                "floor_png": "game-dev-story-mod_Sprites/office/floor0.png",
                "seb": "game-dev-story-mod_Sprites/office/floor0.seb",
                "same_name_pair": True,
            },
        },
        "room_placement": {
            "status": "not_closed",
            "verified": [
                "floor-parts selector and filename join for the observed initial call",
                "SEB group/record framing and available raw shorts for office/floor0.seb",
                "bounded CallHikkosi object coordinates remain in the W5.3 artifact",
            ],
            "open_semantics": [
                "SEB record field meaning and pivot/anchor interpretation",
                "how SEB records are consumed to place a complete room scene",
                "universal world/object/crop/screen transform",
                "four-byte final-record tail shortfall in all audited SEB files",
                "floor-to-SEB mapping for office floor PNGs without same-name SEB files",
            ],
            "policy": "do not pad or synthesize the missing SEB bytes; keep placement non-equivalent",
        },
        "remaining_gap": {
            "id": "W5-GAP-009",
            "status": "partially_closed_floorparts_selector_seb_structure",
            "closed": [
                "IndexImgFloorParts initial sentinel and mode-1 update branch",
                "DDFloor + 3 initial selector resolves to floorparts0.png/index79",
                "DDFloor + input selector resolves floor0/floor1/floor2 for the bounded 0..2 probe",
            ],
            "open": [
                "full SEB room reconstruction",
                "room placement/pivot/transform semantics",
                "legacy-equivalent renderer",
            ],
        },
        "guardrails": [
            "Use StringLiteral_N as one-based labels and W5.5 value-aligned IMG_LIST rows as the current namespace source of truth.",
            "Keep floorparts0.png in the game/img.inf resource namespace; do not confuse it with office/floor0.png.",
            "Treat SEB field names as structural labels only until a consumer proves their semantics.",
            "Do not infer room placement from the 600x600 record values or from the bounded CallHikkosi fixture.",
            "Keep legacy_equivalence=false.",
        ],
        "source_files": {
            rel(FORM_C): sha256(FORM_C),
            rel(KAIRO_C): sha256(KAIRO_C),
            rel(SCRIPT_JSON): sha256(SCRIPT_JSON),
            rel(W53): sha256(W53),
            rel(W55): sha256(W55),
            rel(SEB_MANIFEST): sha256(SEB_MANIFEST),
            rel(SEB_PATH): sha256(SEB_PATH),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    artifact = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    print(json.dumps({"output": rel(output_path.resolve()), "status": artifact["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
