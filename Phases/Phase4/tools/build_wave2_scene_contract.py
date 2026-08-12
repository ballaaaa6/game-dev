#!/usr/bin/env python3
"""Build Wave 2 scene, selector-adapter, and object-contract artifacts.

Wave 2 starts with contracts rather than a web renderer implementation.  This
builder reads the existing Wave 0/Wave 1 artifacts plus the recovered source
roots and records only evidence that can be traced to ``dump.cs``, recovered C,
assembly metadata, or the audited assets.  It never mutates source/extraction
roots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DUMP = ROOT / "game-dev-story-mod_Dumped"
FORM_C = DUMP / "Categorized_Code" / "Global" / "form.c"
METHOD_C = DUMP / "Categorized_Code" / "Global" / "Method.c"
KAIRO_C = DUMP / "Categorized_Code" / "Global" / "kairo.c"
MAIN_C = DUMP / "Categorized_Code" / "Global" / "main.c"
DUMP_CS = DUMP / "dump.cs"
SCRIPT_JSON = DUMP / "script.json"
STRINGLITERAL = DUMP / "stringliteral.json"
PHASE1_TRACE = ROOT / "Phases" / "Phase1" / "artifacts" / "phase1_code_trace.json"
PHASE1_MANIFEST = ROOT / "Phases" / "Phase1" / "artifacts" / "office_manifest.json"
PHASE1_SEB = ROOT / "Phases" / "Phase1" / "artifacts" / "phase1_seb_manifest.json"
PHASE2_TRACE = ROOT / "Phases" / "Phase2" / "artifacts" / "phase2_code_trace.json"
RESOURCE_MAP = ARTIFACTS / "resource_selector_map.json"
WAVE1_SELECTOR = ARTIFACTS / "wave1_selector_resolution.json"
WAVE1_AUDIT = ARTIFACTS / "wave1_asset_gap_audit.json"
WAVE1_GAPS = ARTIFACTS / "wave1_gap_register.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def line_of(text: str, needle: str, occurrence: int = 1) -> int | None:
    matches = list(re.finditer(re.escape(needle), text))
    if not matches:
        return None
    index = min(max(occurrence - 1, 0), len(matches) - 1)
    return text.count("\n", 0, matches[index].start()) + 1


def source_ref(path: Path, text: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    return {
        "file": rel(path),
        "line": line_of(text, needle, occurrence),
        "needle": needle,
    }


def function_span(text: str, symbol: str) -> dict[str, Any]:
    lines = text.splitlines()
    header = f"// Function: {symbol}"
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        return {"symbol": symbol, "status": "not_found"}
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("// Function:"):
            end = index
            break
    address = None
    for line in lines[start : min(start + 4, end)]:
        match = re.search(r"// Address:\s*(0x[0-9a-fA-F]+)", line)
        if match:
            address = match.group(1)
            break
    return {
        "symbol": symbol,
        "status": "recovered_c_function",
        "line_start": start + 1,
        "line_end": end,
        "address": address,
        "source": rel(FORM_C),
    }


def source_ref_in_function(path: Path, text: str, symbol: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    """Return a source reference for a needle constrained to one function."""

    span = function_span(text, symbol)
    if span.get("status") == "not_found":
        return {"file": rel(path), "line": None, "needle": needle, "function": symbol, "status": "function_not_found"}
    lines = text.splitlines()
    local_text = "\n".join(lines[span["line_start"] - 1 : span["line_end"]])
    local_line = line_of(local_text, needle, occurrence)
    return {
        "file": rel(path),
        "line": span["line_start"] + local_line - 1 if local_line is not None else None,
        "needle": needle,
        "function": symbol,
    }


def parse_gameform_fields(names: set[str]) -> dict[str, dict[str, Any]]:
    fields: dict[str, dict[str, Any]] = {}
    lines = DUMP_CS.read_text(encoding="utf-8", errors="replace").splitlines()
    for line_number, line in enumerate(lines, 1):
        if "// 0x" not in line:
            continue
        for name in names:
            pattern = rf"\b{re.escape(name)}\s*;\s*//\s*(0x[0-9A-Fa-f]+)\b"
            match = re.search(pattern, line)
            if not match or name in fields:
                continue
            declaration = line.strip().split("//", 1)[0].strip()
            fields[name] = {
                "name": name,
                "declaration": declaration,
                "offset": match.group(1),
                "source": rel(DUMP_CS),
                "line": line_number,
                "status": "verified_dump_field",
            }
    return fields


def parse_constants() -> list[dict[str, Any]]:
    wanted = {
        "OBJ_TYPE_PARTS",
        "OBJ_TYPE_HUMAN",
        "OBJ_TYPE_DISPLAY",
        "OBJ_TYPE_CHAIR",
        "OBJ_TYPE_DESK",
        "OBJ_TYPE_DESK_CEO",
        "OBJ_TYPE_RECEPTION",
    }
    constants: list[dict[str, Any]] = []
    for line_number, line in enumerate(DUMP_CS.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = re.search(r"\b(public|private|internal)\s+const\s+int\s+(OBJ_TYPE_[A-Z_]+)\s*=\s*(-?\d+)\s*;", line)
        if match and match.group(2) in wanted:
            constants.append(
                {
                    "name": match.group(2),
                    "value": int(match.group(3)),
                    "source": rel(DUMP_CS),
                    "line": line_number,
                    "status": "verified_dump_constant",
                }
            )
    return sorted(constants, key=lambda row: row["value"])


def build_selector_adapter(resource_map: dict[str, Any], selector_resolution: dict[str, Any], audit: dict[str, Any], phase2_trace: dict[str, Any]) -> dict[str, Any]:
    functions = Counter(row["function"] for row in phase2_trace["draw_human_calls"])
    literal_40_41 = [
        {
            "function": row["function"],
            "line": row["line"],
            "source": row["source"],
            "TFace": row["selectors"]["TFace"]["literal"],
            "TBody": row["selectors"]["TBody"]["literal"],
            "status": "index_space_mismatch",
        }
        for row in phase2_trace["draw_human_calls"]
        if row["selectors"]["TFace"]["literal"] in {40, 41}
    ]
    namespaces = [
        {
            "name": "selector_index",
            "meaning": "Runtime selector expression such as TFace, TBody, or a static DD* field.",
            "must_not_be_joined_by": "filename numeric suffix",
        },
        {
            "name": "resource_index",
            "meaning": "Index assigned by img.inf/seb.inf loader order or explicit manifest index.",
            "evidence": rel(RESOURCE_MAP),
        },
        {
            "name": "img_array_slot",
            "meaning": "Slot in GameForm.imgFace/imgBody/imgBihin_ after initializer population.",
            "evidence": rel(DUMP_CS),
        },
        {
            "name": "filename_numeric_id",
            "meaning": "Number embedded in a filename such as body10 or face_10.",
            "status": "not_a_resource_index_without_direct_evidence",
        },
    ]
    selectors: list[dict[str, Any]] = []
    for row in selector_resolution["selectors"]:
        selectors.append(
            {
                "name": row["name"],
                "field_offset": row["field_offset"],
                "uses": row["uses"],
                "write_site": row["write_site"],
                "data_source": row["data_source"],
                "resolution_status": row["resolution_status"],
                "value_status": row["value_status"],
                "adapter_policy": "symbolic_only_until_direct_numeric_value_is_recovered",
                "next_action": row["next_action"],
                "evidence": row["evidence"],
            }
        )
    face_contract = next(row for row in resource_map["selector_contracts"] if row["family"] == "face")
    body_contract = next(row for row in resource_map["selector_contracts"] if row["family"] == "body")
    return {
        "schema_version": "wave2-selector-adapter-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C1-symbolic-selector-adapter",
        "source_roots_read_only": True,
        "policy": {
            "numeric_value_policy": "do_not_hardcode_runtime_or_GOT-backed selector values",
            "imgface_conflict_policy": "retain StringLiteral_7514=false and face asset evidence as conflicting_evidence",
            "tface_40_41_policy": "retain as index_space_mismatch until caller/branch evidence resolves the namespace",
        },
        "namespaces": namespaces,
        "static_selectors": selectors,
        "asset_selector_contracts": {
            "face": {
                "expression": face_contract["selector_expression"],
                "array": face_contract["destination_field"],
                "count": face_contract["count"],
                "mapping_status": face_contract["mapping_status"],
                "evidence": face_contract["source"],
            },
            "body": {
                "expression": body_contract["selector_expression"],
                "array": body_contract["destination_field"],
                "count": body_contract["count"],
                "mapping_status": body_contract["mapping_status"],
                "evidence": body_contract["source"],
            },
        },
        "drawhuman_audit": {
            "total_calls": phase2_trace["draw_human_call_count"],
            "dynamic_selector_calls": phase2_trace["literal_selector_coverage"]["dynamic_selector_calls"],
            "caller_counts": dict(sorted(functions.items())),
            "literal_tface_values": phase2_trace["literal_selector_coverage"]["TFace_values"],
            "tface_40_41_calls": literal_40_41,
            "tface_40_41_audit": audit["tface_40_41"],
        },
        "summary": {
            "static_selector_count": len(selectors),
            "numeric_static_values_decoded": selector_resolution["summary"]["numeric_selector_values_decoded"],
            "drawhuman_call_count": phase2_trace["draw_human_call_count"],
            "tface_40_41_call_count": len(literal_40_41),
            "status": "symbolic_adapter_ready_with_known_selector_gaps",
        },
    }


def build_scene_contract(form_text: str, fields: dict[str, dict[str, Any]], constants: list[dict[str, Any]]) -> dict[str, Any]:
    spans = {
        symbol: function_span(form_text, symbol)
        for symbol in (
            "form_GameForm__AddObjec",
            "form_GameForm__CallHikkosi",
            "form_GameForm__AddTarget",
            "form_GameForm__DrawObj",
            "form_GameForm__DrawFloorCover",
            "form_GameForm__EventGChange",
            "form_GameForm__LoadBihinImage",
            "form_GameForm__GetPcImgData",
            "form_GameForm__GetDeskImgData",
            "form_GameForm__GetChairImgData",
            "form_GameForm__CallPCChange",
            "form_GameForm__CallDeskChange",
            "form_GameForm__CallChairChange",
        )
    }
    add_objec = {
        "function": spans["form_GameForm__AddObjec"],
        "argument_to_field": [
            {"argument": "param_2", "field": "ObjecSyurui", "evidence": source_ref(FORM_C, form_text, "*(uint *)(lVar6 + (long)(int)uVar1 * 4 + 0x20) = param_2;")},
            {"argument": "param_3", "field": "ObjecX", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_3;")},
            {"argument": "param_4", "field": "ObjecY", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_4;")},
            {"argument": "param_5", "field": "ObjecCX", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_5;")},
            {"argument": "param_6", "field": "ObjecCY", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_6;")},
            {"argument": "param_7", "field": "ObjecWX", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_7;")},
            {"argument": "param_8", "field": "ObjecWY", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_8;")},
            {"argument": "param_9", "field": "ObjecSY", "evidence": source_ref(FORM_C, form_text, "*(undefined4 *)(lVar6 + (long)(int)*puVar7 * 4 + 0x20) = param_9;")},
        ],
        "default_writes": [
            {"field": "ObjecEnabled", "value": 1, "status": "verified_from_recovered_c"},
            {"field": "ObjecVisible", "value": 1, "status": "verified_from_recovered_c"},
            {"field": "ObjecZX", "value": 0, "status": "verified_from_recovered_c"},
            {"field": "ObjecZY", "value": 0, "status": "verified_from_recovered_c"},
        ],
        "slot_policy": {
            "free_slot_source": "ObjecEnabled",
            "returned_value": "selected object slot/index",
            "capacity_field": "ObjecMax",
            "refresh_on_failure": "ObjecRefresh=1",
            "status": "verified_for_control_flow_and_field_offsets",
        },
    }
    field_roles = {
        name: {
            **fields[name],
            "role": "source_field_name_only_until_semantic_trace_closes",
        }
        for name in sorted(fields)
    }
    return {
        "schema_version": "wave2-scene-contract-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C2-object-contract",
        "source_roots_read_only": True,
        "address_namespace": {
            "export_to_raw_delta": "-0x100000",
            "status": "verified_from_wave1",
        },
        "object_type_constants": constants,
        "field_map": field_roles,
        "function_spans": spans,
        "add_objec_contract": add_objec,
        "scene_dependencies": {
            "room_initialization": {
                "functions": ["form_GameForm__CallHikkosi", "form_GameForm__AddTarget", "form_GameForm__AddObjec"],
                "status": "recoverable_bounded_trace",
                "next_action": "validate the minimum scene fixture, then expand the bounded branch until its room object type and numeric placement are producer-backed",
            },
            "furniture_image_data": {
                "functions": ["form.GameForm.GetPcImgData", "form.GameForm.GetDeskImgData", "form.GameForm.GetChairImgData", "form.GameForm.LoadBihinImage"],
                "status": "recoverable_bounded_trace",
                "next_action": "use the relation contract as Wave 3 furniture input without treating asset presence as seat occupancy",
            },
            "draw_dispatch": {
                "function": "form_GameForm__DrawObj",
                "status": "verified_dispatch_and_sort_pattern",
                "next_action": "validate the neutral fixture against assembly/runtime behavior before assigning depth semantics",
            },
        },
        "semantic_policy": {
            "verified": "direct field/call/constant evidence",
            "recoverable": "bounded trace has a concrete next action",
            "web_adapter_decision": "web behavior explicitly chosen when legacy behavior is not recovered",
            "out_of_scope": "not required for scene truth or not present in audited source",
        },
        "summary": {
            "field_count": len(field_roles),
            "object_type_constant_count": len(constants),
            "function_count": len(spans),
            "stage_status": "object_contract_ready_for_minimum_scene_fixture",
        },
    }


def build_room_contract(resource_map: dict[str, Any], phase1_manifest: dict[str, Any], phase1_seb: dict[str, Any]) -> dict[str, Any]:
    floor = next(row for row in phase1_manifest["scene_families"] if row["asset"] == "office/floor0.png")
    floor_asset = next(row for row in phase1_manifest["assets"] if row["path"] == "office/floor0.png")
    seb = next(row for row in phase1_seb["files"] if row["relative_path"] == "office/floor0.seb")
    fixtures = []
    for family in ("chair", "desk", "pc", "reception"):
        candidates = [
            row for row in resource_map["fixtures"]
            if row["family"] == family and row["manifest"].endswith("office/img.inf")
        ]
        if candidates:
            fixtures.append(candidates[0])
    return {
        "schema_version": "wave2-room-contract-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C3-room-and-seb-asset-contract",
        "source_roots_read_only": True,
        "room_fixture": {
            "fixture_id": "room_asset_fixture_floor0",
            "floor": {
                "path": floor["asset"],
                "asset_id": floor["asset_id"],
                "sha256": floor_asset["sha256"],
                "dimensions": floor["dimensions"],
                "status": "asset_verified",
            },
            "seb": {
                "path": seb["relative_path"],
                "sha256": seb["sha256"],
                "format": seb["format_name"],
                "group_count": seb["header"]["group_count"],
                "tail_shortfall_bytes": seb["tail_shortfall_bytes"],
                "status": seb["status"],
                "confidence": seb["confidence"],
            },
            "furniture_asset_fixtures": fixtures,
            "placement_status": "not_yet_resolved",
            "fixture_scope": "verified room and furniture assets; no guessed runtime positions",
        },
        "index_contract": {
            "floor_indices": ["IndexImgFloorMain", "IndexImgFloorParts"],
            "event_index": "IndexImgEvent",
            "resource_join": "resource manifest index/name -> GameForm image slot",
            "status": "expression_verified_asset_join_pending",
            "evidence": [
                {"file": rel(FORM_C), "needle": "// Function: form_GameForm__EventGChange", "line": line_of(FORM_C.read_text(encoding="utf-8", errors="replace"), "// Function: form_GameForm__EventGChange")},
                {"file": rel(DUMP_CS), "needle": "public static Image imgFloorMain; // 0x1120", "line": line_of(DUMP_CS.read_text(encoding="utf-8", errors="replace"), "public static Image imgFloorMain; // 0x1120")},
            ],
        },
        "known_limitations": [
            "Four office floor PNGs have no same-name SEB in the current extraction.",
            "SEB records retain the verified four-byte final-record shortfall.",
            "Room placement values are not inferred from the preview image.",
        ],
        "summary": {
            "selected_room": "office/floor0.png",
            "selected_seb": "office/floor0.seb",
            "furniture_fixture_count": len(fixtures),
            "placement_status": "not_yet_resolved",
            "status": "room_asset_contract_ready_for_coordinate_slice",
        },
    }


def build_coordinate_contract(form_text: str, scene_contract: dict[str, Any]) -> dict[str, Any]:
    field = scene_contract["field_map"]
    return {
        "schema_version": "wave2-coordinate-contract-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C4-coordinate-contract-start",
        "source_roots_read_only": True,
        "coordinate_spaces": [
            {"name": "resource_crop", "status": "verified_shape_neutral_semantics"},
            {"name": "seb_local", "status": "partial_due_to_seb_tail_shortfall"},
            {"name": "object_record", "status": "field_names_verified; placement_values_pending"},
            {"name": "world_or_form", "status": "field_names_verified; transform_pending"},
            {"name": "graphics_origin_and_screen", "status": "callsite_evidence_present_transform_pending"},
        ],
        "evidence": [
            {
                "contract": "floor_cover_draw",
                "function": "form_GameForm__DrawFloorCover",
                "source": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawFloorCover", "kairo_unity_ui_Graphics__DrawImage", 1),
                "observed_arguments": {
                    "destination_x": "record + 0x20 + param_3",
                    "destination_y": "record + 0x24 + param_4",
                    "image_slot": "GameForm.imgFloorCover (+0x1130)",
                    "source_rect": ["record + 0x28", "record + 0x2c", "record + 0x30", "record + 0x34"],
                },
                "semantic_status": "verified_for_argument_flow_only",
            },
            {
                "contract": "object_draw_coordinates",
                "function": "form_GameForm__DrawObj",
                "source": source_ref(FORM_C, form_text, "kairo_unity_ui_Graphics__GetOriginX", 1),
                "observed_fields": [
                    {"field": name, "offset": field[name]["offset"]}
                    for name in ("ObjecX", "ObjecY", "ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY", "ObjecSY")
                ],
                "semantic_status": "verified_field_access_neutral_transform",
            },
            {
                "contract": "observed_object_draw_anchor",
                "function": "form_GameForm__DrawObj",
                "source": [
                    source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawHuman", 1),
                    source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawReception", 1),
                ],
                "observed_formula": {
                    "draw_x": "ObjecX + ObjecZX",
                    "draw_y": "ObjecY + ObjecZY",
                    "crop": ["ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY"],
                    "space": "graphics-local coordinates while Graphics origin is active",
                },
                "semantic_status": "verified_for_observed_human_and_reception_callsites_not_universal_renderer_claim",
            },
            {
                "contract": "camera_and_surface",
                "functions": ["form.GameForm.GameScreenLayout", "form.GameForm.RenderGameScreen", "form.GameForm.Draw"],
                "fields": [
                    {"field": name, "offset": field[name]["offset"]}
                    for name in ("CameraX", "CameraY", "GameWidth", "GameHeight", "FormX", "FormY")
                ],
                "semantic_status": "field_names_verified_transform_trace_pending",
            },
        ],
        "policy": {
            "isometric_label": "do_not_assign_without direct transform evidence",
            "anchor_baseline_pivot": "keep unresolved until direct read/write or renderer contract evidence",
            "placement": "do_not derive from image alpha bounds or preview composition",
        },
        "summary": {
            "space_count": 5,
            "transform_status": "not_closed",
            "status": "coordinate_evidence_index_ready_for_followup_slice",
        },
    }


def build_coordinate_fixture(form_text: str) -> dict[str, Any]:
    """Build a deterministic fixture for the recovered centered-origin math.

    This deliberately exercises only arithmetic that is visible in recovered C.
    It is not an isometric projection fixture and does not invent object
    placement, pivot, or tile semantics.
    """

    def origin_for_view(view_size: int) -> dict[str, int]:
        initial_candidate = view_size - 0xEF
        selected_candidate = view_size - 0xF0 if view_size - 0xF0 >= 0 else initial_candidate
        return {
            "view_size": view_size,
            "initial_candidate": initial_candidate,
            "selected_candidate": selected_candidate,
            "origin": selected_candidate >> 1,
        }

    width = origin_for_view(800)
    height = origin_for_view(600)
    return {
        "schema_version": "wave2-coordinate-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C4-coordinate-transform-fixture",
        "fixture_id": "coordinate_center_origin_800x600",
        "semantic_scope": "centered Graphics origin arithmetic only",
        "not_claimed": [
            "isometric projection",
            "tile/grid dimensions",
            "object pivot or anchor",
            "world-to-object placement",
        ],
        "formula": {
            "viewport_constant_hex": "0xF0",
            "viewport_constant_decimal": 240,
            "non_negative_fallback_hex": "0xEF",
            "non_negative_fallback_decimal": 239,
            "selection": "candidate = size - 0xF0 when size - 0xF0 >= 0, otherwise size - 0xEF",
            "origin": "candidate >> 1",
        },
        "input": {"game_width": 800, "game_height": 600},
        "expected": {
            "width": width,
            "height": height,
            "graphics_origin": {"x": width["origin"], "y": height["origin"]},
        },
        "evidence": [
            source_ref(FORM_C, form_text, "iVar12 = iVar10 + -0xef;"),
            source_ref(FORM_C, form_text, "iVar12 = iVar10 + -0xf0;"),
            source_ref(FORM_C, form_text, "iVar10 = iVar11 + -0xef;"),
            source_ref(FORM_C, form_text, "iVar10 = iVar11 + -0xf0;"),
            source_ref(FORM_C, form_text, "kairo_unity_ui_Graphics__SetOrigin((float)(iVar12 >> 1),(float)(iVar10 >> 1),param_2,0);"),
            source_ref(FORM_C, form_text, "form_GameForm__DrawFloorCover(uVar15,param_2,iVar10 >> 1,iVar12);"),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "kairo_unity_ui_Graphics__GetOriginX", 1),
        ],
        "status": "verified_formula_fixture_transform_semantics_still_open",
    }


def build_draw_order_contract(form_text: str, scene_contract: dict[str, Any]) -> dict[str, Any]:
    dispatch = {
        "OBJ_TYPE_PARTS": "form.GameForm.DrawImage/direct parts branch",
        "OBJ_TYPE_HUMAN": "form.GameForm.DrawHuman",
        "OBJ_TYPE_DISPLAY": "form.GameForm.DrawDisplay",
        "OBJ_TYPE_CHAIR": "form.GameForm.DrawChair",
        "OBJ_TYPE_DESK": "form.GameForm.DrawDesk",
        "OBJ_TYPE_DESK_CEO": "form.GameForm.DrawCeoDesk",
        "OBJ_TYPE_RECEPTION": "form.GameForm.DrawReception",
    }
    dispatch_evidence = {
        "OBJ_TYPE_HUMAN": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawHuman", 1),
        "OBJ_TYPE_CHAIR": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawChair", 1),
        "OBJ_TYPE_DESK": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawDesk", 1),
        "OBJ_TYPE_DESK_CEO": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawCeoDesk", 1),
        "OBJ_TYPE_RECEPTION": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawReception", 1),
    }
    return {
        "schema_version": "wave2-draw-order-contract-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C5-draw-dispatch-and-sort-index",
        "source_roots_read_only": True,
        "dispatch": [
            {
                "object_type": name,
                "renderer": renderer,
                "status": "verified_dispatch_name" if name != "OBJ_TYPE_PARTS" else "verified_direct_branch_pending_named_renderer",
                "evidence": dispatch_evidence.get(name),
            }
            for name, renderer in dispatch.items()
        ],
        "sort_evidence": {
            "function": "form.GameForm__DrawObj",
            "comparison": source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "if (*(int *)(lVar27 + (long)(int)uVar10 * 4 + 0x20) +", 1),
            "order_array": {"field": "ObjecUpDown", "offset": scene_contract["field_map"]["ObjecUpDown"]["offset"], "status": "field_access_verified"},
            "candidate_components": [
                {"raw_offset": "0x2D8", "field": "ObjecSY", "status": "field_offset_join_verified_neutral_semantics"},
                {"raw_offset": "0x2A0", "field": "ObjecY", "status": "field_offset_join_verified_neutral_semantics"},
            ],
            "semantic_status": "comparison_verified_depth_label_not_yet_verified",
        },
        "fixture_policy": {
            "minimum_objects": 2,
            "expected_output": "ordered draw command records, not a guessed pixel snapshot",
            "status": "neutral_fixture_created_semantics_pending",
        },
        "summary": {
            "dispatch_count": len(dispatch),
            "sort_pattern": "compare_and_swap_verified",
            "depth_semantics": "not_closed",
            "status": "draw_dispatch_contract_ready_for_fixture",
        },
    }


def build_draw_order_fixture(form_text: str, scene_contract: dict[str, Any]) -> dict[str, Any]:
    """Build a neutral compare-and-swap probe from the recovered sort fields."""

    records = [
        {"slot": 0, "object_type": "OBJ_TYPE_DESK", "ObjecY": 300, "ObjecSY": 20},
        {"slot": 1, "object_type": "OBJ_TYPE_CHAIR", "ObjecY": 120, "ObjecSY": 10},
        {"slot": 2, "object_type": "OBJ_TYPE_RECEPTION", "ObjecY": 200, "ObjecSY": 15},
    ]
    for record in records:
        record["candidate_sort_key"] = record["ObjecSY"] + record["ObjecY"]
    ordered = sorted(records, key=lambda row: (row["candidate_sort_key"], row["slot"]))
    return {
        "schema_version": "wave2-draw-order-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C5-draw-order-fixture",
        "fixture_id": "draw_order_compare_and_swap_3_objects",
        "semantic_status": "neutral_sort_probe_depth_meaning_not_closed",
        "sort_policy": {
            "candidate_key": "ObjecSY + ObjecY",
            "comparison": "swap when left candidate key > right candidate key",
            "tie_break": "original slot for deterministic fixture output",
            "legacy_verification_scope": "recovered comparison and swap pattern; not a semantic depth claim",
        },
        "input_records": records,
        "expected_draw_order": [row["slot"] for row in ordered],
        "expected_sorted_records": ordered,
        "evidence": [
            source_ref_in_function(
                FORM_C,
                form_text,
                "form_GameForm__DrawObj",
                "if (*(int *)(lVar27 + (long)(int)uVar10 * 4 + 0x20) +",
                1,
            ),
            {
                "file": rel(DUMP_CS),
                "line": scene_contract["field_map"]["ObjecSY"]["line"],
                "needle": "ObjecSY; // 0x2D8",
            },
            {
                "file": rel(DUMP_CS),
                "line": scene_contract["field_map"]["ObjecY"]["line"],
                "needle": "ObjecY; // 0x2A0",
            },
        ],
        "status": "fixture_ready_for_assembly_or_pixel_regression",
    }


def build_furniture_contract(form_text: str, scene_contract: dict[str, Any]) -> dict[str, Any]:
    field_map = scene_contract["field_map"]
    accessor_specs = [
        ("pc", "form_GameForm__GetPcImgData", "PCImgData", "lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x480);"),
        ("desk", "form_GameForm__GetDeskImgData", "DeskImgData", "lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x488);"),
        ("chair", "form_GameForm__GetChairImgData", "ChairImgData", "lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x490);"),
    ]
    accessors = []
    for family, function, field, array_needle in accessor_specs:
        accessors.append(
            {
                "family": family,
                "function": function,
                "array_field": field,
                "array_offset": field_map[field]["offset"],
                "normalization": "param_1 modulo array length",
                "evidence": [
                    source_ref_in_function(FORM_C, form_text, function, array_needle, 1),
                    source_ref_in_function(FORM_C, form_text, function, "uVar2 = param_1 - iVar3 * uVar1;", 1),
                    source_ref_in_function(FORM_C, form_text, function, "return *(undefined8 *)(lVar5 + (long)(int)uVar2 * 8 + 0x20);", 1),
                ],
                "status": "verified_accessor_and_slot_normalization",
            }
        )

    relation_specs = [
        {
            "function": "form_GameForm__CallPCChange",
            "relations": ["PCImgData", "PCObjec", "DeskZahyou", "ObjecX", "ObjecY", "ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY", "ObjecSY", "ObjecZX"],
            "evidence": [
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallPCChange", "form_GameForm__GetPcImgData(param_3);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallPCChange", "lVar7 = *(long *)(lVar8 + 0x470);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallPCChange", "lVar9 = *(long *)(lVar8 + 0x478);", 1),
            ],
        },
        {
            "function": "form_GameForm__CallDeskChange",
            "relations": ["DeskImgData", "DeskObjec", "DeskZahyou", "ObjecSyurui", "ObjecX", "ObjecY", "ObjecSY"],
            "evidence": [
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallDeskChange", "form_GameForm__GetDeskImgData(param_3);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallDeskChange", "lVar10 = *(long *)(lVar7 + 0x458);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallDeskChange", "lVar12 = *(long *)(lVar7 + 0x2f8);", 1),
            ],
        },
        {
            "function": "form_GameForm__CallChairChange",
            "relations": ["ChairImgData", "ChairMainObjec", "ChairSubObjec", "DeskZahyou", "ObjecX", "ObjecY", "ObjecSY"],
            "evidence": [
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallChairChange", "form_GameForm__GetChairImgData(param_3);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallChairChange", "lVar9 = *(long *)(lVar12 + 0x460);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__CallChairChange", "lVar17 = *(long *)(lVar12 + 0x478);", 1),
            ],
        },
        {
            "function": "form_GameForm__LoadBihinImage",
            "relations": ["imgBihin_"],
            "evidence": [
                source_ref_in_function(FORM_C, form_text, "form_GameForm__LoadBihinImage", "plVar6 = *(long **)(lVar3 + 0x1110);", 1),
                source_ref_in_function(FORM_C, form_text, "form_GameForm__LoadBihinImage", "main_AppData__GetImage(param_1,uVar4,0)", 1),
            ],
        },
    ]

    placement_trace = {
        "function": "form_GameForm__CallHikkosi",
        "branch": "param_2 == 0, first bounded DeskImgData-backed object",
        "source_array": "DeskImgData",
        "source_array_offset": field_map["DeskImgData"]["offset"],
        "office_index_field": "KaishaOffice",
        "office_index_offset": field_map["KaishaOffice"]["offset"],
        "record_guard": "selected desk record length >= 14",
        "add_objec_arguments": {
            "param_2": "selected desk record + 0x54 + 5",
            "param_3": 0x2E,
            "param_4": 0x3D,
            "param_5": 100,
            "param_6": 0,
            "param_7": 0x21,
            "param_8": 0x2E,
            "param_9": 0x20,
        },
        "object_list_field": "OfficeObjecList",
        "object_list_offset": field_map["OfficeObjecList"]["offset"],
        "status": "verified_bounded_add_objec_trace_without_full_room_placement_semantics",
        "evidence": [
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "lVar15 = *(long *)(lVar16 + 0x488);", 1),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "*(uint *)(lVar16 + 0x734)", 1),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "form_GameForm__AddObjec", 1),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "*(int *)(lVar21 + (long)(int)uVar22 * 4 + 0x20) = (int)uVar9;", 1),
        ],
    }

    return {
        "schema_version": "wave2-furniture-contract-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C6-furniture-seat-placement-trace",
        "source_roots_read_only": True,
        "image_data_accessors": accessors,
        "relation_traces": relation_specs,
        "placement_trace": placement_trace,
        "seat_contract": {
            "legacy_fields": ["ChairMainObjec", "ChairSubObjec", "DeskZahyou"],
            "status": "not_closed",
            "evidence_scope": "chair change and desk coordinate arrays are traced, but no direct occupancy-to-seat assignment is established",
            "web_adapter_policy": "do_not_mark_a_seat_occupied_from_chair_asset_or_array_presence_alone",
            "next_action": "trace the caller that writes employee/seat occupancy before implementing interaction behavior",
        },
        "collision_contract": {
            "status": "not_found_in_scoped_scene_functions",
            "scope": ["CallHikkosi", "CallPCChange", "CallDeskChange", "CallChairChange", "DrawObj"],
            "evidence": rel(PHASE1_TRACE),
            "next_action": "search the movement/interaction producer path before adding web collision geometry",
        },
        "walkable_contract": {
            "status": "not_found_in_scoped_scene_functions",
            "scope": ["CallHikkosi", "CallPCChange", "CallDeskChange", "CallChairChange", "DrawObj"],
            "evidence": rel(PHASE1_TRACE),
            "next_action": "trace movement/path graph consumers or explicitly mark web walkability as adapter behavior",
        },
        "summary": {
            "accessor_count": len(accessors),
            "relation_trace_count": len(relation_specs),
            "placement_status": placement_trace["status"],
            "seat_status": "not_closed",
            "collision_status": "not_found_in_scoped_scene_functions",
            "walkable_status": "not_found_in_scoped_scene_functions",
            "status": "furniture_relations_and_bounded_placement_trace_ready; seat_collision_walkable_open",
        },
    }


def build_placement_fixture(furniture_contract: dict[str, Any]) -> dict[str, Any]:
    trace = furniture_contract["placement_trace"]
    return {
        "schema_version": "wave2-placement-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C6-placement-trace-fixture",
        "fixture_id": "callhikkosi_param2_0_first_desk_object",
        "fixture_scope": "bounded legacy call trace; not a rendered room snapshot",
        "input": {"CallHikkosi_param_2": 0, "office_index_source": "KaishaOffice"},
        "expected": {
            "source_array": trace["source_array"],
            "record_guard": trace["record_guard"],
            "add_objec_arguments": trace["add_objec_arguments"],
            "result_written_to": trace["object_list_field"],
        },
        "unresolved": [
            "selected office record numeric value",
            "complete room object list",
            "seat occupancy state",
            "collision and walkable zones",
        ],
        "status": "relation_contract_fixture_only",
        "evidence": trace["evidence"],
    }


def build_minimum_scene_fixture(
    form_text: str,
    room_contract: dict[str, Any],
    coordinate_fixture: dict[str, Any],
    draw_order_fixture: dict[str, Any],
    furniture_contract: dict[str, Any],
    scene_contract: dict[str, Any],
) -> dict[str, Any]:
    placement = furniture_contract["placement_trace"]
    bounded_record = {
        "record_id": "callhikkosi_param2_0_office_object_0",
        "origin": "form_GameForm__CallHikkosi bounded first DeskImgData-backed AddObjec call",
        "ObjecSyurui": "selected_desk_record_plus_5",
        "ObjecX": placement["add_objec_arguments"]["param_3"],
        "ObjecY": placement["add_objec_arguments"]["param_4"],
        "ObjecCX": placement["add_objec_arguments"]["param_5"],
        "ObjecCY": placement["add_objec_arguments"]["param_6"],
        "ObjecWX": placement["add_objec_arguments"]["param_7"],
        "ObjecWY": placement["add_objec_arguments"]["param_8"],
        "ObjecSY": placement["add_objec_arguments"]["param_9"],
        "ObjecZX": 0,
        "ObjecZY": 0,
        "ObjecEnabled": 1,
        "ObjecVisible": 1,
        "candidate_sort_key": 0x20 + 0x3D,
        "object_type_status": "symbolic_only_selected_desk_record_plus_5",
    }
    dispatch_probe = {
        "record_id": "known_reception_dispatch_probe",
        "purpose": "exercise a verified renderer dispatch and anchor/crop argument flow without claiming CallHikkosi creates reception",
        "ObjecSyurui": 7,
        "ObjecX": 46,
        "ObjecY": 61,
        "ObjecCX": 100,
        "ObjecCY": 0,
        "ObjecWX": 33,
        "ObjecWY": 46,
        "ObjecZX": 0,
        "ObjecZY": 0,
        "renderer": "form.GameForm.DrawReception",
        "draw_command": {
            "space": "graphics-local-with-current-origin",
            "x": 46,
            "y": 61,
            "crop": [100, 0, 33, 46],
            "origin_reference": coordinate_fixture["expected"]["graphics_origin"],
        },
        "status": "verified_dispatch_probe_not_room_object_claim",
    }
    return {
        "schema_version": "wave2-minimum-scene-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C7-minimum-scene-gate",
        "fixture_id": "office_floor0_bounded_object_and_dispatch_probe",
        "scope": "minimum Wave 2 scene contract; not a final pixel snapshot or full room reconstruction",
        "room": {
            "floor": room_contract["room_fixture"]["floor"],
            "seb": room_contract["room_fixture"]["seb"],
            "placement_source": placement["source_array"],
            "placement_index_field": placement["office_index_field"],
        },
        "coordinate": {
            "fixture_id": coordinate_fixture["fixture_id"],
            "graphics_origin": coordinate_fixture["expected"]["graphics_origin"],
            "object_anchor_formula": {
                "x": "ObjecX + ObjecZX",
                "y": "ObjecY + ObjecZY",
                "crop": ["ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY"],
                "status": "verified_for_observed_human_and_reception_callsites",
            },
        },
        "objects": {
            "bounded_placement_record": bounded_record,
            "known_dispatch_probe": dispatch_probe,
        },
        "draw_order": {
            "neutral_fixture_id": draw_order_fixture["fixture_id"],
            "bounded_record_candidate_key": bounded_record["candidate_sort_key"],
            "semantic_status": "sort_probe_only_depth_not_closed",
        },
        "asset_and_object_contracts": {
            "room_contract": "wave2_room_contract.json",
            "scene_contract": "scene_contract.json",
            "furniture_contract": "wave2_furniture_contract.json",
        },
        "evidence": [
            source_ref_in_function(FORM_C, form_text, "form_GameForm__DrawObj", "form_GameForm__DrawReception", 1),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "form_GameForm__AddObjec", 1),
            source_ref_in_function(FORM_C, form_text, "form_GameForm__CallHikkosi", "*(int *)(lVar21 + (long)(int)uVar22 * 4 + 0x20) = (int)uVar9;", 1),
            {"file": rel(DUMP_CS), "line": scene_contract["field_map"]["ObjecX"]["line"], "needle": "ObjecX; // 0x298"},
            {"file": rel(DUMP_CS), "line": scene_contract["field_map"]["ObjecZX"]["line"], "needle": "ObjecZX; // 0x2C8"},
        ],
        "status": "minimum_scene_contract_ready_with_symbolic_room_object_type",
    }


def build_wave3_movement_interface(furniture_contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "wave2-wave3-movement-interface-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C7-wave3-interface-boundary",
        "purpose": "Define the input boundary Wave 3 may consume without promoting unresolved legacy semantics.",
        "seat": {
            "legacy_status": furniture_contract["seat_contract"]["status"],
            "web_adapter_decision": "seat occupancy must be an explicit relation/state owned by Wave 3; do not infer it from chair image or ChairMainObjec presence",
            "inputs": ["agent_id", "seat_id", "optional_furniture_object_id"],
            "output": "seat_occupancy_state",
        },
        "collision": {
            "legacy_status": furniture_contract["collision_contract"]["status"],
            "web_adapter_decision": "require an explicit collision provider; no legacy-equivalent geometry is supplied by Wave 2",
            "inputs": ["object_id", "candidate_position"],
            "output": "blocked | clear | unavailable",
        },
        "walkable": {
            "legacy_status": furniture_contract["walkable_contract"]["status"],
            "web_adapter_decision": "allow Wave 3 to inject a walk graph/grid as adapter data, labelled non-legacy until producer evidence is found",
            "inputs": ["from_position", "to_position", "movement_context"],
            "output": "path | no_path | unavailable",
        },
        "non_goals": [
            "derive seat state from pixels or alpha bounds",
            "derive collision rectangles from furniture image dimensions",
            "call adapter walkability a recovered legacy grid",
        ],
        "status": "wave3_interface_ready_with_legacy_semantics_open",
    }


def carry_forward_gaps(wave1_gaps: dict[str, Any]) -> list[dict[str, Any]]:
    carried = []
    for row in wave1_gaps["gaps"]:
        carried.append(
            {
                "gap_id": row["gap_id"],
                "question": row["question"],
                "status": row["status"],
                "impact": row["impact"],
                "evidence": row["evidence"],
                "next_action": row["next_action"],
                "confidence": row["confidence"],
                "carried_from": "Wave1",
            }
        )
    return carried


def build_gap_register(wave1_gaps: dict[str, Any], selector_adapter: dict[str, Any], scene_contract: dict[str, Any]) -> dict[str, Any]:
    gaps = carry_forward_gaps(wave1_gaps)
    additions = [
        {
            "gap_id": "G-W2-C1-selector-namespace",
            "question": "Selector, resource index, image-array slot และ filename numeric id จะ join กันที่จุดใดของ runtime",
            "status": "recoverable",
            "impact": "risk",
            "evidence": [rel(WAVE1_SELECTOR), rel(RESOURCE_MAP), rel(WAVE1_AUDIT)],
            "next_action": "ใช้ symbolic adapter และ trace เฉพาะ caller ที่อยู่ใน room/DrawObj path ก่อน decode numeric value",
            "confidence": "high",
        },
        {
            "gap_id": "G-W2-C2-object-record-semantics",
            "question": "Object record fields ที่ AddObjec เขียนจะ map เป็น scene schema ได้ครบเพียงใด",
            "status": "recoverable",
            "impact": "risk",
            "evidence": [
                f"{rel(FORM_C)}:{scene_contract['function_spans']['form_GameForm__AddObjec']['line_start']}",
                rel(DUMP_CS),
            ],
            "next_action": "สร้าง fixture จาก CallHikkosi หนึ่ง branch แล้วตรวจ producer/consumer ของทุก field ที่ใช้จริง",
            "confidence": "high",
        },
        {
            "gap_id": "G-W2-C4-coordinate-spaces",
            "question": "world/object/crop/screen coordinate transforms ที่ DrawFloorCover และ DrawObj ใช้คืออะไร",
            "status": "recoverable",
            "impact": "blocker",
            "evidence": [rel(FORM_C), rel(PHASE1_TRACE)],
            "next_action": "ตรวจ coordinate formula fixture กับ assembly/pixel evidence ก่อนปิด transform semantics",
            "confidence": "medium",
        },
        {
            "gap_id": "G-W2-C5-depth-field-semantics",
            "question": "sort comparison ใน DrawObj ใช้ field ใดเป็นลำดับวาดและมีความหมาย depth หรือไม่",
            "status": "recoverable",
            "impact": "blocker",
            "evidence": [f"{rel(PHASE1_TRACE)}:drawobj_sort_comparison", rel(FORM_C), rel(DUMP_CS)],
            "next_action": "ใช้ neutral compare-and-swap fixture เป็น regression probe แล้วตรวจ semantic depth จาก assembly/pixel behavior",
            "confidence": "medium",
        },
        {
            "gap_id": "G-W2-C6-seat-collision-walkable",
            "question": "seat, collision, walkable และ interaction zone เป็น legacy fact หรือ web adapter behavior",
            "status": "recoverable",
            "impact": "risk",
            "evidence": [f"{rel(PHASE1_TRACE)}:collision_contract", rel(FORM_C), rel(DUMP_CS)],
            "next_action": "trace direct occupancy/seat reads; ถ้าไม่พบให้ปิด legacy claim และบันทึก web_adapter_decision หรือ out_of_scope",
            "confidence": "medium",
        },
        {
            "gap_id": "G-W2-C6-furniture-relations",
            "question": "PC/desk/chair image data และ object arrays เชื่อมกันอย่างไรใน change functions",
            "status": "recoverable",
            "impact": "risk",
            "evidence": [rel(FORM_C), rel(DUMP_CS)],
            "next_action": "ใช้ furniture relation contract ตรวจ caller ที่สร้าง object และเชื่อมกับ room fixture",
            "confidence": "high",
        },
        {
            "gap_id": "G-W2-C7-placement-trace",
            "question": "CallHikkosi สร้าง object placement ของ office/furniture อย่างไรโดยไม่เดาจากภาพ",
            "status": "recoverable",
            "impact": "blocker",
            "evidence": [rel(FORM_C), rel(DUMP_CS)],
            "next_action": "ขยาย bounded branch ไปเป็น end-to-end room fixture และคง numeric placement เป็น unresolved จนกว่าจะมี producer evidence",
            "confidence": "medium",
        },
    ]
    gaps.extend(additions)
    status_counts = Counter(row["status"] for row in gaps)
    return {
        "schema_version": "wave2-gap-register-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C7-minimum-gate",
        "source_roots_read_only": True,
        "controlled_statuses": wave1_gaps["controlled_statuses"],
        "gaps": gaps,
        "summary": {
            "gap_count": len(gaps),
            "status_counts": dict(sorted(status_counts.items())),
            "unclassified_unknown_count": sum(1 for row in gaps if row["status"] == "unknown"),
            "current_wave2_gate": "not_ready_for_wave2_scene_closure",
            "selector_adapter_status": selector_adapter["summary"]["status"],
            "scene_contract_status": scene_contract["summary"]["stage_status"],
        },
    }


def build_manifest(selector_adapter: dict[str, Any], scene_contract: dict[str, Any], room_contract: dict[str, Any], coordinate_contract: dict[str, Any], coordinate_fixture: dict[str, Any], draw_order_contract: dict[str, Any], draw_order_fixture: dict[str, Any], furniture_contract: dict[str, Any], placement_fixture: dict[str, Any], minimum_scene_fixture: dict[str, Any], movement_interface: dict[str, Any], gap_register: dict[str, Any]) -> dict[str, Any]:
    source_files = [
        FORM_C,
        METHOD_C,
        KAIRO_C,
        MAIN_C,
        DUMP_CS,
        SCRIPT_JSON,
        STRINGLITERAL,
        RESOURCE_MAP,
        WAVE1_SELECTOR,
        WAVE1_AUDIT,
        WAVE1_GAPS,
        PHASE1_TRACE,
        PHASE1_MANIFEST,
        PHASE1_SEB,
        PHASE2_TRACE,
    ]
    return {
        "schema_version": "wave2-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave2",
        "stage": "W2-C7-minimum-gate",
        "source_roots_read_only": True,
        "address_namespace": {"export_to_raw_delta": "-0x100000", "status": "verified"},
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_files},
        "artifact_summary": {
            "selector_count": selector_adapter["summary"]["static_selector_count"],
            "scene_field_count": scene_contract["summary"]["field_count"],
            "room_fixture_count": room_contract["summary"]["furniture_fixture_count"],
            "coordinate_space_count": coordinate_contract["summary"]["space_count"],
            "coordinate_fixture_status": coordinate_fixture["status"],
            "draw_dispatch_count": draw_order_contract["summary"]["dispatch_count"],
            "draw_order_fixture_status": draw_order_fixture["status"],
            "furniture_relation_count": furniture_contract["summary"]["relation_trace_count"],
            "placement_fixture_status": placement_fixture["status"],
            "minimum_scene_fixture_status": minimum_scene_fixture["status"],
            "movement_interface_status": movement_interface["status"],
            "gap_count": gap_register["summary"]["gap_count"],
        },
        "status": "W2-C0-baseline-through-W2-C7-minimum-gate-built_with_open_semantics",
    }


def build() -> dict[Path, Any]:
    form_text = FORM_C.read_text(encoding="utf-8", errors="replace")
    resource_map = load_json(RESOURCE_MAP)
    selector_resolution = load_json(WAVE1_SELECTOR)
    audit = load_json(WAVE1_AUDIT)
    wave1_gaps = load_json(WAVE1_GAPS)
    phase2_trace = load_json(PHASE2_TRACE)
    field_names = {
        "CameraX", "CameraY", "GameWidth", "GameHeight", "FormX", "FormY",
        "ObjecMax", "ObjecRefresh", "ObjecIndex", "ObjecX", "ObjecY", "ObjecCX", "ObjecCY",
        "ObjecWX", "ObjecWY", "ObjecZX", "ObjecZY", "ObjecSY", "ObjecEnabled", "ObjecVisible",
        "ObjecUpDown", "ObjecSyurui", "ObjecAnime", "ObjecPoint", "TargetX", "TargetY",
        "OfficeObjecMax", "OfficeObjecList", "DeskSyain", "DeskObjec", "ChairMainObjec",
        "ChairSubObjec", "PCObjec", "DeskZahyou", "PCImgData", "DeskImgData", "ChairImgData",
        "KaishaOffice", "imgBihin_", "imgFloorMain", "imgFloorParts", "imgFloorCover", "imgFace",
        "imgBody", "imgEvent", "IndexImgFloorMain", "IndexImgEvent", "IndexImgFloorParts",
    }
    fields = parse_gameform_fields(field_names)
    missing = sorted(field_names - set(fields))
    if missing:
        raise RuntimeError("missing expected GameForm fields: " + ", ".join(missing))
    constants = parse_constants()
    if len(constants) != 7:
        raise RuntimeError(f"expected 7 object type constants, found {len(constants)}")
    selector_adapter = build_selector_adapter(resource_map, selector_resolution, audit, phase2_trace)
    scene_contract = build_scene_contract(form_text, fields, constants)
    phase1_manifest = load_json(PHASE1_MANIFEST)
    phase1_seb = load_json(PHASE1_SEB)
    room_contract = build_room_contract(resource_map, phase1_manifest, phase1_seb)
    coordinate_contract = build_coordinate_contract(form_text, scene_contract)
    coordinate_fixture = build_coordinate_fixture(form_text)
    draw_order_contract = build_draw_order_contract(form_text, scene_contract)
    draw_order_fixture = build_draw_order_fixture(form_text, scene_contract)
    furniture_contract = build_furniture_contract(form_text, scene_contract)
    placement_fixture = build_placement_fixture(furniture_contract)
    minimum_scene_fixture = build_minimum_scene_fixture(
        form_text,
        room_contract,
        coordinate_fixture,
        draw_order_fixture,
        furniture_contract,
        scene_contract,
    )
    movement_interface = build_wave3_movement_interface(furniture_contract)
    gap_register = build_gap_register(wave1_gaps, selector_adapter, scene_contract)
    manifest = build_manifest(
        selector_adapter,
        scene_contract,
        room_contract,
        coordinate_contract,
        coordinate_fixture,
        draw_order_contract,
        draw_order_fixture,
        furniture_contract,
        placement_fixture,
        minimum_scene_fixture,
        movement_interface,
        gap_register,
    )
    return {
        ARTIFACTS / "wave2_selector_adapter.json": selector_adapter,
        ARTIFACTS / "scene_contract.json": scene_contract,
        ARTIFACTS / "wave2_room_contract.json": room_contract,
        ARTIFACTS / "wave2_coordinate_contract.json": coordinate_contract,
        ARTIFACTS / "wave2_coordinate_fixture.json": coordinate_fixture,
        ARTIFACTS / "wave2_draw_order_contract.json": draw_order_contract,
        ARTIFACTS / "wave2_draw_order_fixture.json": draw_order_fixture,
        ARTIFACTS / "wave2_furniture_contract.json": furniture_contract,
        ARTIFACTS / "wave2_placement_fixture.json": placement_fixture,
        ARTIFACTS / "wave2_minimum_scene_fixture.json": minimum_scene_fixture,
        ARTIFACTS / "wave2_wave3_movement_interface.json": movement_interface,
        ARTIFACTS / "wave2_gap_register.json": gap_register,
        ARTIFACTS / "wave2_build_manifest.json": manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare with existing artifacts")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            if not path.exists() or load_json(path) != expected:
                mismatches.append(rel(path))
        if mismatches:
            raise SystemExit("artifact mismatch: " + ", ".join(mismatches))
        return
    for path, value in outputs.items():
        write_json(path, value)
    print(json.dumps({"outputs": [rel(path) for path in outputs], "status": "built"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
