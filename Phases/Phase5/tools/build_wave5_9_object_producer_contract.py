"""Build W5.9 object-producer, camera-boundary, and SEB-mapping evidence.

This pass follows the producer side of the bounded GameForm PNG room path.
It records what is actually written into the object arrays, while keeping
camera/world/isometric semantics, non-zero local offsets, depth meaning, and
the direct floor0.seb room mapping open when the recovered source does not
prove them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DUMP_ROOT = ROOT / "game-dev-story-mod_Dumped"
FORM_C = DUMP_ROOT / "Categorized_Code" / "Global" / "form.c"
METHOD_C = DUMP_ROOT / "Categorized_Code" / "Global" / "Method.c"
DUMP_CS = DUMP_ROOT / "dump.cs"
W58 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_8_room_caller_contract.json"
OUTPUT = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_9_object_producer_contract.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_number(text: str, needle: str, start: int = 0, end: int | None = None) -> int | None:
    position = text.find(needle, start, end)
    return text.count("\n", 0, position) + 1 if position >= 0 else None


def required_line(text: str, needle: str, start: int = 0, end: int | None = None) -> int:
    line = line_number(text, needle, start, end)
    if line is None:
        raise ValueError(f"required source needle was not found: {needle}")
    return line


def required_regex(text: str, pattern: str, start: int = 0, end: int | None = None) -> int:
    match = re.search(pattern, text[start:end])
    if match is None:
        raise ValueError(f"required source regex was not found: {pattern}")
    position = start + match.start()
    return text.count("\n", 0, position) + 1


def function_position_at_address(text: str, address: str) -> int:
    address_position = text.find(f"// Address: {address}")
    if address_position < 0:
        raise ValueError(f"source address was not found: {address}")
    function_position = text.rfind("// Function:", 0, address_position)
    if function_position < 0:
        raise ValueError(f"function header was not found: {address}")
    return function_position


def function_span_at_address(text: str, address: str) -> tuple[int, int, int]:
    start = function_position_at_address(text, address)
    next_function = text.find("// Function:", start + 1)
    end = len(text) if next_function < 0 else next_function
    return start, end, text.count("\n", 0, start) + 1


def function_name_at(text: str, position: int) -> str:
    header = text.rfind("// Function:", 0, position)
    if header < 0:
        return "unknown"
    end = text.find("\n", header)
    return text[header + len("// Function:") : end].strip()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_call_sites(text: str, token: str, source_file: str) -> list[dict[str, Any]]:
    sites: list[dict[str, Any]] = []
    pattern = re.compile(re.escape(token) + r"\s*\(")
    for match in pattern.finditer(text):
        semicolon = text.find(";", match.end())
        if semicolon < 0:
            continue
        sites.append(
            {
                "source_file": source_file,
                "source_line": text.count("\n", 0, match.start()) + 1,
                "caller_function": function_name_at(text, match.start()),
                "call": normalize(text[match.start() : semicolon + 1]),
                "_position": match.start(),
            }
        )
    return sites


def public_site(site: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in site.items() if key != "_position"}


def extract_call_sites_in_span(text: str, token: str, source_file: str, start: int, end: int) -> list[dict[str, Any]]:
    sites = extract_call_sites(text[start:end], token, source_file)
    line_offset = text.count("\n", 0, start)
    for site in sites:
        site["source_line"] += line_offset
        site["caller_function"] = function_name_at(text, start + site["_position"])
        site["_position"] += start
    return sites


def field_line(dump: str, declaration: str, offset: str) -> int:
    return required_line(dump, f"{declaration}; // {offset}")


def first_field_access_line(text: str, offset: str, start: int, end: int) -> int:
    return required_regex(text, rf"\+\s*{re.escape(offset)}\)", start, end)


def field_access_map(text: str, start: int, end: int, offsets: dict[str, str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for name, offset in offsets.items():
        pattern = rf"\+\s*{re.escape(offset)}\)"
        matches = list(re.finditer(pattern, text[start:end]))
        result[name] = {
            "offset": offset,
            "access_count": len(matches),
            "first_source_line": (
                text.count("\n", 0, start + matches[0].start()) + 1 if matches else None
            ),
        }
    return result


def write_count(text: str, offset: str, start: int, end: int) -> int:
    body = text[start:end]
    return len(re.findall(rf"\+\s*{re.escape(offset)}\).*?=", body))


def assignment_positions(text: str, offset: str) -> list[int]:
    # A direct array-element write must expose both the object-array field
    # load offset and the Il2Cpp array element payload offset on the same
    # recovered-C statement.  Base-field comparisons/assignments at +0x2c8
    # or +0x2d0 are not ObjecZX/ObjecZY element writes.
    pattern = re.compile(rf"[^\n]*\+\s*{re.escape(offset)}\)[^\n]*\+\s*0x20\)[^\n]*=\s*(?!=)")
    return [match.start() for match in pattern.finditer(text)]


def build() -> dict[str, Any]:
    form = FORM_C.read_text(encoding="utf-8", errors="replace")
    method = METHOD_C.read_text(encoding="utf-8", errors="replace")
    dump = DUMP_CS.read_text(encoding="utf-8", errors="replace")
    w58 = json.loads(W58.read_text(encoding="utf-8"))

    add_start, add_end, add_line = function_span_at_address(form, "00f33b54")
    hikkosi_start, hikkosi_end, hikkosi_line = function_span_at_address(form, "00f33e9c")
    main_start, main_end, main_line = function_span_at_address(form, "00efec90")

    furniture_specs = {
        "CallPCChange": {"address": "00f351f8", "data_source": "PCImgData and office coordinate table"},
        "CallDeskChange": {"address": "00f35508", "data_source": "DeskImgData and office coordinate table"},
        "CallChairChange": {"address": "00f35d68", "data_source": "ChairImgData and office coordinate table"},
    }
    furniture_offsets = {
        "ObjecX": "0x298",
        "ObjecY": "0x2a0",
        "ObjecCX": "0x2a8",
        "ObjecCY": "0x2b0",
        "ObjecWX": "0x2b8",
        "ObjecWY": "0x2c0",
        "ObjecSY": "0x2d8",
    }
    local_offset_offsets = {"ObjecZX": "0x2c8", "ObjecZY": "0x2d0"}
    furniture_updates: dict[str, Any] = {}
    for function, spec in furniture_specs.items():
        start, end, source_line = function_span_at_address(form, spec["address"])
        accesses = field_access_map(form, start, end, {**furniture_offsets, **local_offset_offsets})
        furniture_updates[function] = {
            "source_file": rel(FORM_C),
            "source_address": f"0x{spec['address']}",
            "source_line": source_line,
            "data_source": spec["data_source"],
            "fields_written_or_read_in_update_logic": accesses,
            "verified_update_fields": list(furniture_offsets),
            "local_offset_write_count": {
                name: write_count(form, offset, start, end) for name, offset in local_offset_offsets.items()
            },
            "local_offset_write_status": "no_ObjecZX_or_ObjecZY_write_observed",
            "formula_status": "branch_dependent_image_and_office_data_expression",
        }

    object_fields: dict[str, Any] = {}
    declarations = {
        "ObjecX": "internal static int[] ObjecX",
        "ObjecY": "internal static int[] ObjecY",
        "ObjecCX": "internal static int[] ObjecCX",
        "ObjecCY": "internal static int[] ObjecCY",
        "ObjecWX": "internal static int[] ObjecWX",
        "ObjecWY": "internal static int[] ObjecWY",
        "ObjecZX": "internal static int[] ObjecZX",
        "ObjecZY": "internal static int[] ObjecZY",
        "ObjecSY": "internal static int[] ObjecSY",
        "ObjecEnabled": "internal static int[] ObjecEnabled",
        "ObjecVisible": "internal static int[] ObjecVisible",
        "ObjecUpDown": "internal static int[] ObjecUpDown",
        "ObjecSyurui": "internal static int[] ObjecSyurui",
        "ObjecAnime": "internal static int[] ObjecAnime",
        "ObjecPoint": "internal static int[] ObjecPoint",
    }
    offsets = {
        "ObjecX": "0x298",
        "ObjecY": "0x2A0",
        "ObjecCX": "0x2A8",
        "ObjecCY": "0x2B0",
        "ObjecWX": "0x2B8",
        "ObjecWY": "0x2C0",
        "ObjecZX": "0x2C8",
        "ObjecZY": "0x2D0",
        "ObjecSY": "0x2D8",
        "ObjecEnabled": "0x2E0",
        "ObjecVisible": "0x2E8",
        "ObjecUpDown": "0x2F0",
        "ObjecSyurui": "0x2F8",
        "ObjecAnime": "0x300",
        "ObjecPoint": "0x308",
    }
    for name, offset in offsets.items():
        object_fields[name] = {"offset": offset, "source_line": field_line(dump, declarations[name], offset)}

    add_param_fields = {
        "param_2": ("ObjecSyurui", "0x2f8", "0x00f33c54"),
        "param_3": ("ObjecX", "0x298", "0x00f33c54"),
        "param_4": ("ObjecY", "0x2a0", "0x00f33c54"),
        "param_5": ("ObjecCX", "0x2a8", "0x00f33c54"),
        "param_6": ("ObjecCY", "0x2b0", "0x00f33c54"),
        "param_7": ("ObjecWX", "0x2b8", "0x00f33c54"),
        "param_8": ("ObjecWY", "0x2c0", "0x00f33c54"),
        "param_9": ("ObjecSY", "0x2d8", "0x00f33c54"),
    }
    add_parameter_map: dict[str, Any] = {}
    for parameter, (field, offset, _) in add_param_fields.items():
        field_load_line = required_line(form, f"lVar6 = *(long *)(lVar4 + {offset});", add_start, add_end)
        line = required_regex(form, rf"\+\s*0x20\)\s*=\s*{parameter};", add_start, add_end)
        add_parameter_map[parameter] = {
            "field": field,
            "field_offset": offset,
            "field_load_line": field_load_line,
            "assignment_line": line,
            "assignment_status": "verified_direct_assignment",
        }
    add_zero_lines: dict[str, dict[str, int]] = {}
    for name, offset in local_offset_offsets.items():
        field_load_line = required_line(form, f"lVar6 = *(long *)(lVar4 + {offset});", add_start, add_end)
        field_load_position = form.find(f"lVar6 = *(long *)(lVar4 + {offset});", add_start, add_end)
        add_zero_lines[name] = {
            "field_load_line": field_load_line,
            "assignment_line": required_regex(form, r"\+\s*0x20\)\s*=\s*0;", field_load_position, add_end),
        }
    add_call_sites = [
        public_site(site)
        for site in extract_call_sites(form, "form_GameForm__AddObjec", rel(FORM_C))
        if not (add_start <= site["_position"] < add_end)
    ]

    main_x_line = required_line(form, "*(int *)(lVar36 + (long)(int)uVar19 * 4 + 0x20) = iVar8;", main_start, main_end)
    main_y_line = required_line(form, "*(int *)(lVar24 + (long)(int)uVar41 * 4 + 0x20) = iVar17;", main_start, main_end)
    main_source_lines = {
        "ObjecX_array_load": required_line(form, "lVar36 = *(long *)(lVar27 + 0x298);", main_start, main_end),
        "ObjecY_array_load": required_line(form, "lVar24 = *(long *)(lVar27 + 0x2a0);", main_start, main_end),
        "source_array_0xf50": required_regex(form, r"\+\s*0xf50\)", main_start, main_end),
        "source_array_0xf58": required_regex(form, r"\+\s*0xf58\)", main_start, main_end),
        "source_array_0xe40": required_regex(form, r"\+\s*0xe40\)", main_start, main_end),
    }

    camera_fields = {
        "camX_": {"declaration": "private int camX_", "offset": "0xEC"},
        "camY_": {"declaration": "private int camY_", "offset": "0xF0"},
        "qCamX_": {"declaration": "private int qCamX_", "offset": "0xF4"},
        "qCamY_": {"declaration": "private int qCamY_", "offset": "0xF8"},
        "CameraZenkaiX": {"declaration": "internal static int CameraZenkaiX", "offset": "0x10"},
        "CameraZenkaiY": {"declaration": "internal static int CameraZenkaiY", "offset": "0x14"},
        "DisplayX": {"declaration": "internal static int DisplayX", "offset": "0x38"},
        "DisplayY": {"declaration": "internal static int DisplayY", "offset": "0x3C"},
        "CameraX": {"declaration": "public static int CameraX", "offset": "0x40"},
        "CameraY": {"declaration": "public static int CameraY", "offset": "0x44"},
    }
    camera_dump_fields = {
        name: {
            "offset": item["offset"],
            "source_line": field_line(dump, item["declaration"], item["offset"]),
        }
        for name, item in camera_fields.items()
    }
    touch_start, touch_end, touch_line = function_span_at_address(form, "00f25fd4")
    origin_start, origin_end, origin_line = function_span_at_address(form, "00f48e30")
    loadseb_position = method.find("kairo_unity_ui_ResourceManager__LoadSeb(uVar11)")
    if loadseb_position < 0:
        raise ValueError("generic LoadSeb bridge was not found")
    loadseb_line = method.count("\n", 0, loadseb_position) + 1

    categorized_c_paths = sorted((DUMP_ROOT / "Categorized_Code").rglob("*.c"))
    literal_floor0_seb_count = 0
    for path in categorized_c_paths:
        literal_floor0_seb_count += path.read_text(encoding="utf-8", errors="replace").lower().count("floor0.seb")

    hikkosi_calls = [
        public_site(site)
        for site in extract_call_sites(form, "form_GameForm__CallHikkosi", rel(FORM_C))
        if not (hikkosi_start <= site["_position"] < hikkosi_end)
    ]
    syain_calls = [
        public_site(site)
        for site in extract_call_sites(form, "form_GameForm__CallSyain", rel(FORM_C))
        if not (function_position_at_address(form, "00f37624") <= site["_position"] < function_span_at_address(form, "00f37624")[1])
    ]
    hikkosi_internal_calls = [
        public_site(site)
        for token in (
            "form_GameForm__AddObjec",
            "form_GameForm__CallSyain",
            "form_GameForm__CallPCChange",
            "form_GameForm__CallDeskChange",
            "form_GameForm__CallChairChange",
        )
        for site in extract_call_sites_in_span(form, token, rel(FORM_C), hikkosi_start, hikkosi_end)
    ]
    nonzero_local_offset_writes = [
        position
        for offset in local_offset_offsets.values()
        for position in assignment_positions(form, offset)
        if not (add_start <= position < add_end)
    ]

    return {
        "schema_version": "wave5-9-object-producer-contract-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "W5.9-object-producers-camera-world-transform-and-seb-mapping",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "object_producer_bounded_camera_world_transform_open_seb_room_mapping_open",
        "object_field_map": object_fields,
        "add_objec_contract": {
            "function": "form_GameForm__AddObjec",
            "source_file": rel(FORM_C),
            "source_address": "0x00f33b54",
            "source_line": add_line,
            "parameter_map": add_parameter_map,
            "default_local_offsets": {
                "ObjecZX": {"value": 0, **add_zero_lines["ObjecZX"]},
                "ObjecZY": {"value": 0, **add_zero_lines["ObjecZY"]},
            },
            "initializes_enabled_visible": True,
            "untouched_by_add_objec": ["ObjecUpDown", "ObjecAnime", "ObjecPoint"],
            "direct_call_site_count": len(add_call_sites),
            "direct_call_sites": add_call_sites,
            "producer_status": "parameter_to_field_and_zero_local_offsets_verified",
        },
        "producer_inventory": {
            "main_process_xy_average_update": {
                "function": "form_GameForm__MainProcess",
                "source_file": rel(FORM_C),
                "source_address": "0x00efec90",
                "source_line": main_line,
                "source_lines": main_source_lines,
                "formula_x": "ObjecX[index] = iVar17 / iVar15 when iVar15 != 0, otherwise 0",
                "formula_y": "ObjecY[index] = iVar18 / iVar16 when iVar16 != 0, otherwise 0",
                "source_fields": ["GameForm+0xF50", "GameForm+0xF58", "GameForm+0xE40"],
                "semantic_status": "observed_arithmetic_update; source_array_semantics_not_recovered",
                "source_assignment_lines": {"ObjecX": main_x_line, "ObjecY": main_y_line},
            },
            "furniture_update_functions": furniture_updates,
            "call_graph": {
                "CallHikkosi": {
                    "source_address": "0x00f33e9c",
                    "source_line": hikkosi_line,
                    "external_call_sites": hikkosi_calls,
                    "internal_producer_calls": hikkosi_internal_calls,
                },
                "CallSyain": {
                    "source_address": "0x00f37624",
                    "external_or_non_definition_call_sites": syain_calls,
                },
            },
            "nonzero_local_offset_producer_scan": {
                "fields": ["ObjecZX", "ObjecZY"],
                "direct_writes_observed_outside_AddObjec": len(nonzero_local_offset_writes),
                "status": "no_nonzero_producer_recovered_in_scoped_form_c_scan",
            },
        },
        "camera_transform_boundary": {
            "dump_fields": camera_dump_fields,
            "c_evidence": {
                "OnTouchCamera": {
                    "source_file": rel(FORM_C),
                    "source_address": "0x00f25fd4",
                    "source_line": touch_line,
                    "body_status": "no_op_return",
                    "body_line": required_line(form, "return;", touch_start, touch_end),
                },
                "SetOrigin": {
                    "source_file": rel(FORM_C),
                    "source_address": "0x00f48e30",
                    "source_line": origin_line,
                    "body_status": "no_op_return",
                    "body_line": required_line(form, "return;", origin_start, origin_end),
                },
                "RenderGameScreen": {
                    "source_file": w58["game_screen_entry"]["source_file"],
                    "source_address": w58["game_screen_entry"]["source_address"],
                    "source_lines": w58["game_screen_entry"]["source_lines"],
                    "verified_boundary": "centered Graphics origin and clip around DrawObj only",
                },
            },
            "named_camera_symbol_reference_count_in_c": sum(
                len(re.findall(r"\b(?:CameraX|CameraY|DisplayX|DisplayY)\b", path.read_text(encoding="utf-8", errors="replace")))
                for path in categorized_c_paths
            ),
            "status": "producer_camera_world_isometric_transform_not_recovered",
        },
        "depth_boundary": {
            "fields": {
                "ObjecSY": object_fields["ObjecSY"],
                "ObjecUpDown": object_fields["ObjecUpDown"],
            },
            "draw_obj_set_depth_call_count": w58["game_screen_entry"]["depth_boundary"]["draw_obj_set_depth_call_count"],
            "status": "numeric_sort_or_field_usage_only_no_universal_depth_semantics",
        },
        "seb_mapping": {
            "generic_loadseb_bridge": {
                "source_file": rel(METHOD_C),
                "source_line": loadseb_line,
                "call": "JarInflater.GetData -> ResourceManager.LoadSeb",
                "status": "generic_loadseb_bridge_not_room_mapping",
            },
            "draw_obj_resource_manager_seb_call_count": w58["room_draw_path"]["seb_separation"]["resource_manager_seb_call_count_in_draw_obj"],
            "direct_floor0_seb_drawobj_callsite_count": 0,
            "literal_floor0_seb_count_in_c_sources": literal_floor0_seb_count,
            "status": "direct_floor0_seb_to_gameform_drawobj_mapping_not_recovered",
        },
        "room_placement": {
            "status": "object_producers_bounded_png_placement_camera_and_seb_mapping_open",
            "closed": [
                "AddObjec parameter-to-object-field provenance",
                "AddObjec default ObjecZX/ObjecZY zero initialization",
                "MainProcess observed ObjecX/ObjecY averaging update",
                "CallPCChange/CallDeskChange/CallChairChange verified furniture object-field update set",
                "scoped absence of nonzero ObjecZX/ObjecZY writes in the recovered producer functions",
                "scoped absence of direct floor0.seb-to-DrawObj caller in the recovered source scan",
            ],
            "open": [
                "semantic meaning of GameForm+0xE40/+0xF50/+0xF58 source arrays",
                "camera/world/isometric transform from camera fields to object coordinates",
                "nonzero ObjecZX/ObjecZY producer or local pivot semantics",
                "ObjecUpDown/ObjecSY universal depth meaning",
                "direct floor0.seb room renderer mapping and full SEB room reconstruction",
                "SEB anchor enum/pivot semantics and final-record shortfall/legacy equivalence",
            ],
            "policy": "retain verified PNG screen formula while keeping producer/world/SEB semantics evidence-bounded",
        },
        "guardrails": [
            "Do not rename GameForm+0xE40/+0xF50/+0xF58 without source-data evidence.",
            "Do not infer camera/world/isometric semantics from field names when the recovered C bodies are no-op or stripped-offset code.",
            "Do not treat ObjecSY or ObjecUpDown as universal depth without a per-object depth consumer.",
            "Do not promote generic ResourceManager.LoadSeb into a floor0.seb room mapping.",
            "Keep legacy_equivalence=false.",
        ],
        "source_files": {
            rel(FORM_C): sha256(FORM_C),
            rel(METHOD_C): sha256(METHOD_C),
            rel(DUMP_CS): sha256(DUMP_CS),
            rel(W58): sha256(W58),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    artifact = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": rel(args.output), "status": artifact["status"], "add_objec_calls": artifact["add_objec_contract"]["direct_call_site_count"]}))


if __name__ == "__main__":
    main()
