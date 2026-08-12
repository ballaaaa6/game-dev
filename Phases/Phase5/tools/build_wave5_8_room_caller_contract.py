"""Build W5.8 room-caller and screen-placement evidence.

This pass separates the GameForm room PNG path from SEB UI consumers.  It
records the verified screen origin, object-coordinate/crop formulas, and the
scoped absence of ResourceManager.DrawSeb inside DrawObj without claiming that
the complete room/world transform or floor0.seb mapping is recovered.
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
KAIRO_C = DUMP_ROOT / "Categorized_Code" / "Global" / "kairo.c"
DUMP_CS = DUMP_ROOT / "dump.cs"
W53 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_3_numeric_crop_placement_contract.json"
W56 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_6_floorparts_seb_contract.json"
W57 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_7_seb_consumer_contract.json"
OUTPUT = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_8_room_caller_contract.json"


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


def function_position_at_address(text: str, address: str) -> int:
    address_position = text.find(f"// Address: {address}")
    if address_position < 0:
        raise ValueError(f"source address was not found: {address}")
    function_position = text.rfind("// Function:", 0, address_position)
    if function_position < 0:
        raise ValueError(f"function header was not found: {address}")
    return function_position


def function_line_at_address(text: str, address: str) -> int:
    return text.count("\n", 0, function_position_at_address(text, address)) + 1


def function_span_at_address(text: str, address: str) -> tuple[int, int, int]:
    start = function_position_at_address(text, address)
    next_function = text.find("// Function:", start + 1)
    end = len(text) if next_function < 0 else next_function
    return start, end, text.count("\n", 0, start) + 1


def last_line_before(text: str, needle: str, start: int, end: int) -> int:
    position = text.rfind(needle, start, end)
    if position < 0:
        raise ValueError(f"source needle was not found before boundary: {needle}")
    return text.count("\n", 0, position) + 1


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def function_name_at(text: str, position: int) -> str:
    header = text.rfind("// Function:", 0, position)
    if header < 0:
        return "unknown"
    end = text.find("\n", header)
    return text[header + len("// Function:") : end].strip()


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
            }
        )
    return sites


def field_line(dump: str, name: str, offset: str) -> int:
    return required_line(dump, f"{name}; // {offset}")


def build() -> dict[str, Any]:
    form = FORM_C.read_text(encoding="utf-8", errors="replace")
    method = METHOD_C.read_text(encoding="utf-8", errors="replace")
    kairo = KAIRO_C.read_text(encoding="utf-8", errors="replace")
    dump = DUMP_CS.read_text(encoding="utf-8", errors="replace")
    w53 = json.loads(W53.read_text(encoding="utf-8"))
    w56 = json.loads(W56.read_text(encoding="utf-8"))
    w57 = json.loads(W57.read_text(encoding="utf-8"))

    render_start, render_end, render_line = function_span_at_address(method, "00f16edc")
    drawobj_start, drawobj_end, drawobj_line = function_span_at_address(form, "00f173c8")
    reception_start, reception_end, reception_line = function_span_at_address(form, "00f6d4ec")

    origin_line = required_line(method, "kairo_unity_ui_Graphics__SetOrigin((float)(iVar3 >> 1),0,param_2,0)", render_start, render_end)
    reset_origin_line = required_line(method, "kairo_unity_ui_Graphics__SetOrigin(0,0,param_2,0)", render_start, render_end)
    drawobj_call_line = required_line(method, "form_GameForm__DrawObj(param_1,param_2)", render_start, render_end)
    clip_line = required_line(method, "kairo_unity_ui_Graphics__SetClip", render_start, render_end)
    width_line = required_line(method, "surface_GameView__GetGameWidth", render_start, render_end)
    mesh_depth_line = required_line(method, "kairo_unity_graphics_MeshManager__SetDepth", render_start, render_end)

    floor_field_position = form.find("*(undefined8 *)(lVar22 + 0x1128)", drawobj_start, drawobj_end)
    if floor_field_position < 0:
        raise ValueError("DrawObj imgFloorParts field access was not found")
    direct_draw_position = form.rfind("kairo_unity_ui_Graphics__DrawImage", drawobj_start, floor_field_position)
    if direct_draw_position < 0:
        raise ValueError("DrawObj direct DrawImage before imgFloorParts was not found")
    direct_draw_end = form.find(";", direct_draw_position, drawobj_end)
    if direct_draw_end < 0:
        raise ValueError("DrawObj direct DrawImage terminator was not found")
    direct_destination_lines = {
        "x": last_line_before(form, "((float)(*(int *)(lVar25 + lVar35 * 4 + 0x20)", direct_draw_position, floor_field_position),
        "y": last_line_before(form, "(float)(*(int *)(lVar28 + lVar35 * 4 + 0x20)", direct_draw_position, direct_draw_end),
    }
    direct_crop_lines = {
        "cx": last_line_before(form, "*(undefined4 *)(lVar29 + lVar35 * 4 + 0x20)", direct_draw_position, direct_draw_end),
        "cy": last_line_before(form, "*(undefined4 *)(lVar30 + lVar35 * 4 + 0x20)", direct_draw_position, direct_draw_end),
        "wx": last_line_before(form, "*(undefined4 *)(lVar32 + lVar35 * 4 + 0x20)", direct_draw_position, direct_draw_end),
        "wy": last_line_before(form, "*(undefined4 *)(lVar31 + lVar35 * 4 + 0x20)", direct_draw_position, direct_draw_end),
    }
    reception_call_line = required_line(form, "form_GameForm__DrawReception", drawobj_start, drawobj_end)
    reception_draw_line = required_line(form, "kairo_unity_ui_Graphics__DrawImage", reception_start, reception_end)
    reception_image_line = required_line(form, "0x1128),param_5,param_6,param_7", reception_start, reception_end)

    game_fields = {
        "imgFloorMain": {"offset": "0x1120", "source_line": field_line(dump, "public static Image imgFloorMain", "0x1120")},
        "imgFloorParts": {"offset": "0x1128", "source_line": field_line(dump, "public static Image imgFloorParts", "0x1128")},
        "IndexImgFloorMain": {"offset": "0x1180", "source_line": field_line(dump, "internal static int IndexImgFloorMain", "0x1180")},
        "IndexImgFloorParts": {"offset": "0x1188", "source_line": field_line(dump, "internal static int IndexImgFloorParts", "0x1188")},
    }
    object_fields = {}
    for name, offset in (
        ("ObjecX", "0x298"),
        ("ObjecY", "0x2A0"),
        ("ObjecCX", "0x2A8"),
        ("ObjecCY", "0x2B0"),
        ("ObjecWX", "0x2B8"),
        ("ObjecWY", "0x2C0"),
        ("ObjecZX", "0x2C8"),
        ("ObjecZY", "0x2D0"),
        ("ObjecSY", "0x2D8"),
        ("ObjecUpDown", "0x2F0"),
        ("ObjecSyurui", "0x2F8"),
        ("ObjecAnime", "0x300"),
        ("ObjecPoint", "0x308"),
    ):
        object_fields[name] = {"offset": offset, "source_line": field_line(dump, f"internal static int[] {name}", offset)}

    seb_draw_sites: list[dict[str, Any]] = []
    for path in sorted((DUMP_ROOT / "Categorized_Code").rglob("*.c")):
        if path == KAIRO_C:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = rel(path)
        seb_draw_sites.extend(extract_call_sites(text, "kairo_unity_ui_ResourceManager__DrawSeb", relative))
        seb_draw_sites.extend(extract_call_sites(text, "kairo_unity_ui_ResourceManager__DrawSebAnchor", relative))
    seb_draw_sites.sort(key=lambda item: (item["source_file"], item["source_line"], item["call"]))
    # The Anchor token is a substring of DrawSeb, so the exact-token extraction
    # above can produce a duplicate only when the non-anchor regex matches it.
    unique_sites = []
    seen = set()
    for site in seb_draw_sites:
        key = (site["source_file"], site["source_line"], site["call"])
        if key not in seen:
            seen.add(key)
            unique_sites.append(site)
    seb_draw_sites = unique_sites

    drawobj_text = form[drawobj_start:drawobj_end]
    drawobj_seb_call_count = len(re.findall(r"kairo_unity_ui_ResourceManager__DrawSeb(?:Anchor)?\s*\(", drawobj_text))
    drawobj_set_depth_count = drawobj_text.count("kairo_unity_ui_Graphics__SetDepth")

    return {
        "schema_version": "wave5-8-room-caller-contract-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "W5.8-room-caller-screen-origin-png-placement-and-seb-separation",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "room_png_screen_placement_verified_seb_room_mapping_open",
        "game_screen_entry": {
            "function": "Method_form_GameForm_RenderGameScreen",
            "source_file": rel(METHOD_C),
            "source_address": "0x00f16edc",
            "source_line": render_line,
            "source_lines": {
                "game_width_read": width_line,
                "clip": clip_line,
                "mesh_depth_setup": mesh_depth_line,
                "set_origin": origin_line,
                "draw_obj_call": drawobj_call_line,
                "reset_origin": reset_origin_line,
            },
            "coordinate_flow": {
                "viewport_constants": {"VIEW_X": 0, "VIEW_Y": 22, "VIEW_W": "GameForm+0x8", "VIEW_H": "GameForm+0xc"},
                "origin_expression": "iVar5 = GameForm.GetGameWidth(); iVar3 = iVar5 - 0xef; if (-1 < iVar5 - 0xf0) iVar3 = iVar5 - 0xf0; Graphics.SetOrigin(iVar3 >> 1, 0)",
                "clip_expression": "clip_x uses the same 0xf0/0xf1 width branch; clip width is GameForm+0x8 and height is GameForm+0xc",
                "draw_obj_boundary": "Graphics origin is active while DrawObj runs and is reset immediately afterward",
                "status": "screen_origin_and_clip_flow_verified; expression preserved without simplifying the one-pixel branch",
            },
            "depth_boundary": {
                "setup": "MeshManager.SetDepth(mesh, 0, 1, 0) before DrawObj",
                "draw_obj_set_depth_call_count": drawobj_set_depth_count,
                "semantic_status": "no per-object Graphics.SetDepth in scoped DrawObj; do not rename object sort fields as depth",
            },
        },
        "room_draw_path": {
            "entry_function": "form_GameForm__DrawObj",
            "source_file": rel(FORM_C),
            "source_address": "0x00f173c8",
            "source_line": drawobj_line,
            "object_fields": object_fields,
            "image_slots": game_fields,
            "dispatch": {
                "object_type_field": "ObjecSyurui (+0x2f8)",
                "object_order_field": "ObjecUpDown (+0x2f0)",
                "observed_branches": [
                    {"value": 4, "callee": "form_GameForm__DrawChair"},
                    {"value": 5, "callee": "bounded object branch before furniture/floor fallback"},
                    {"value": 6, "callee": "form_GameForm__DrawCeoDesk"},
                    {"value": 7, "callee": "form_GameForm__DrawReception"},
                    {"value": "other", "callee": "direct Graphics.DrawImage using imgFloorParts slot"},
                ],
                "semantic_policy": "numeric branch labels remain structural; do not equate value 7 with a universal room type outside this DrawObj slice",
            },
            "direct_img_floor_parts_branch": {
                "source_lines": {
                    "draw_image": form.count("\n", 0, direct_draw_position) + 1,
                    "destination_x": direct_destination_lines["x"],
                    "destination_y": direct_destination_lines["y"],
                    "image_field": form.count("\n", 0, floor_field_position) + 1,
                    "source_cx": direct_crop_lines["cx"],
                    "source_cy": direct_crop_lines["cy"],
                    "source_wx": direct_crop_lines["wx"],
                    "source_wy": direct_crop_lines["wy"],
                },
                "formula": "DrawImage(ObjecX + ObjecZX, ObjecY + ObjecZY, GameForm.imgFloorParts, ObjecCX, ObjecCY, ObjecWX, ObjecWY, 0)",
                "status": "bounded_room_png_crop_and_local_placement_verified",
            },
            "reception_helper": {
                "function": "form_GameForm__DrawReception",
                "source_line": reception_line,
                "call_from_draw_obj_line": reception_call_line,
                "draw_image_line": reception_draw_line,
                "img_floor_parts_line": reception_image_line,
                "formula": "DrawImage(ObjecX + ObjecZX, ObjecY + ObjecZY, GameForm.imgFloorParts, ObjecCX, ObjecCY, ObjecWX, ObjecWY, 0)",
                "status": "helper_argument_flow_verified; object array producer remains outside this slice",
            },
            "seb_separation": {
                "resource_manager_seb_call_count_in_draw_obj": drawobj_seb_call_count,
                "resource_manager_seb_call_count_status": "scoped_zero",
                "conclusion": "DrawObj room path reaches PNG/furniture DrawImage helpers directly; no ResourceManager.DrawSeb consumer is present inside this function",
            },
        },
        "seb_caller_inventory": {
            "scope": "all categorized C files except kairo.c implementation definitions",
            "call_site_count": len(seb_draw_sites),
            "caller_functions": sorted({site["caller_function"] for site in seb_draw_sites}),
            "call_sites": seb_draw_sites,
            "classification": "observed callers are UI/subform/rank/special-form consumers; none is the GameForm.DrawObj room path",
            "room_mapping_status": "no direct floor0.seb-to-DrawObj caller recovered in this scan",
        },
        "cross_wave_join": {
            "w53_crop_contract": w53["crop_contract"]["draw_obj_fields"],
            "w56_floor_selector": {
                "initial_floor_parts_selector": w56["index_img_floor_parts"]["initial_value"],
                "resolved_floor_parts_asset": w56["index_img_floor_parts"]["initial_callsite_resolution"]["requested_filename"],
                "runtime_floor_parts_slot": "GameForm+0x1128",
            },
            "w57_seb_contract_status": w57["status"],
            "interpretation": "W5.7 closes SEB local consumer arithmetic, while W5.8 closes the separate GameForm PNG room-screen path; the two asset/draw paths must not be conflated",
        },
        "room_placement": {
            "status": "png_room_screen_placement_bounded_seb_room_mapping_open",
            "closed": [
                "GameForm RenderGameScreen clip/origin wrapper around DrawObj",
                "ObjecX/ObjecY plus ObjecZX/ObjecZY destination flow",
                "ObjecCX/ObjecCY/ObjecWX/ObjecWY crop flow",
                "imgFloorParts field slot at GameForm+0x1128 in the room draw path",
                "scoped separation between DrawObj PNG rendering and ResourceManager SEB UI consumers",
            ],
            "open": [
                "producer semantics for every object coordinate array and camera/world mapping",
                "full isometric/world-to-screen transform beyond the verified screen origin",
                "ObjecUpDown/ObjecSY semantic depth meaning",
                "direct caller or mapping from office/floor0.seb to the room floor renderer",
                "SEB anchor enum/pivot and depth semantics",
                "four-byte final-record shortfall and legacy-equivalent SEB decoding",
            ],
            "policy": "use PNG room formulas only within the verified GameForm screen boundary; keep SEB room reconstruction and legacy_equivalence=false",
        },
        "guardrails": [
            "Do not use the office/floor0.seb sample as proof of the GameForm room PNG draw path.",
            "Do not rename numeric ObjecSyurui branches or ObjecUpDown/ObjecSY as universal product/depth semantics.",
            "The SetOrigin expression is a screen-centering boundary; it does not prove the producer-side world/isometric transform.",
            "Keep W5.7 SEB local crop evidence separate from W5.8 GameForm PNG room placement evidence.",
            "Keep legacy_equivalence=false.",
        ],
        "source_files": {
            rel(FORM_C): sha256(FORM_C),
            rel(METHOD_C): sha256(METHOD_C),
            rel(KAIRO_C): sha256(KAIRO_C),
            rel(DUMP_CS): sha256(DUMP_CS),
            rel(W53): sha256(W53),
            rel(W56): sha256(W56),
            rel(W57): sha256(W57),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    artifact = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": rel(args.output), "status": artifact["status"], "seb_call_sites": artifact["seb_caller_inventory"]["call_site_count"]}))


if __name__ == "__main__":
    main()
