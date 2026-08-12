"""Build the W5.7 SEB consumer, crop, and bounded placement evidence artifact.

This pass follows the recovered SEB data from the loader through sprite-buffer
conversion into DrawImage consumers.  It records the local crop/base-offset
contract and the bounding/anchor helpers, while keeping room/world transform
semantics explicitly open.
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
KAIRO_C = DUMP_ROOT / "Categorized_Code" / "Global" / "kairo.c"
MAIN_C = DUMP_ROOT / "Categorized_Code" / "Global" / "main.c"
METHOD_C = DUMP_ROOT / "Categorized_Code" / "Global" / "Method.c"
DUMP_CS = DUMP_ROOT / "dump.cs"
W53 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_3_numeric_crop_placement_contract.json"
W56 = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_6_floorparts_seb_contract.json"
OUTPUT = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_7_seb_consumer_contract.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def line_number(text: str, needle: str, start: int = 0) -> int | None:
    position = text.find(needle, start)
    return text.count("\n", 0, position) + 1 if position >= 0 else None


def required_line(text: str, needle: str, start: int = 0) -> int:
    line = line_number(text, needle, start)
    if line is None:
        raise ValueError(f"required source needle was not found: {needle}")
    return line


def function_line_at_address(text: str, address: str) -> int:
    address_position = text.find(f"// Address: {address}")
    if address_position < 0:
        raise ValueError(f"source address was not found: {address}")
    function_position = text.rfind("// Function:", 0, address_position)
    if function_position < 0:
        raise ValueError(f"function header for address was not found: {address}")
    return text.count("\n", 0, function_position) + 1


def function_position_at_address(text: str, address: str) -> int:
    address_position = text.find(f"// Address: {address}")
    if address_position < 0:
        raise ValueError(f"source address was not found: {address}")
    function_position = text.rfind("// Function:", 0, address_position)
    if function_position < 0:
        raise ValueError(f"function header for address was not found: {address}")
    return function_position


def constant_value(dump_text: str, name: str) -> int:
    match = re.search(rf"public const int {re.escape(name)} = (-?\d+);", dump_text)
    if not match:
        raise ValueError(f"Seb constant was not found in dump.cs: {name}")
    return int(match.group(1))


def build() -> dict[str, Any]:
    kairo = KAIRO_C.read_text(encoding="utf-8", errors="replace")
    main = MAIN_C.read_text(encoding="utf-8", errors="replace")
    method = METHOD_C.read_text(encoding="utf-8", errors="replace")
    dump = DUMP_CS.read_text(encoding="utf-8", errors="replace")
    w53 = load_json(W53)
    w56 = load_json(W56)

    expected_constants = {
        "SP_FRAME_NO": 0,
        "SP_TEX_ID": 1,
        "SP_U": 2,
        "SP_V": 3,
        "SP_W": 4,
        "SP_H": 5,
        "SP_TRANS_X": 6,
        "SP_TRANS_Y": 7,
        "SP_REVERS_U": 8,
        "SP_REVERS_V": 9,
        "SP_BLEND": 10,
        "SP_COLOR": 11,
        "SP_END": 12,
    }
    constants = {name: constant_value(dump, name) for name in expected_constants}
    if constants != expected_constants:
        raise ValueError(f"unexpected SEB constants: {constants}")

    get_sprites_local = function_line_at_address(kairo, "01884a04")
    get_brect_frame = function_line_at_address(kairo, "01884b78")
    get_bounding_rect = function_line_at_address(kairo, "01884dfc")
    get_brect = function_line_at_address(kairo, "01884eb4")
    get_pixel_rect = function_line_at_address(kairo, "01885110")
    get_sprites = function_line_at_address(kairo, "01885610")
    get_sprite_local = function_line_at_address(kairo, "01886104")
    conv_start = kairo.find("// Address: 018869d0")
    conv_buffer_to_sprite = function_line_at_address(kairo, "018869d0")
    seb_core_draw = function_line_at_address(kairo, "0188b280")
    seb_core_draw_start = function_position_at_address(kairo, "0188b280")
    seb_set_offset = function_line_at_address(kairo, "0187cdb8")
    seb_clear_offset = function_line_at_address(kairo, "0188be94")
    seb_get_anchor = function_line_at_address(kairo, "01888298")
    seb_draw_anchor = function_line_at_address(kairo, "018883a8")
    resource_load_seb = function_line_at_address(kairo, "01879a70")
    seb_ctor = function_line_at_address(kairo, "01879ac8")

    main_horizontal = function_line_at_address(main, "00f79fe4")
    main_horizontal_start = function_position_at_address(main, "00f79fe4")
    main_vertical = function_line_at_address(main, "00f7a0f4")
    main_vertical_start = function_position_at_address(main, "00f7a0f4")
    main_normal = function_line_at_address(main, "00f7a204")
    main_normal_start = function_position_at_address(main, "00f7a204")
    main_reverse = function_line_at_address(main, "00f7a2e4")
    main_reverse_start = function_position_at_address(main, "00f7a2e4")
    main_brect = function_line_at_address(main, "00f7a5c8")
    main_brect_start = function_position_at_address(main, "00f7a5c8")

    field_source_lines = {
        "texture_id": required_line(kairo, "*(int *)(param_3 + 0x24) =", conv_start),
        "local_x": required_line(kairo, "*(int *)(param_3 + 0x38) =", conv_start),
        "local_y": required_line(kairo, "*(int *)(param_3 + 0x3c) =", conv_start),
        "u": required_line(kairo, "*(uint *)(param_3 + 0x28) =", conv_start),
        "v": required_line(kairo, "*(uint *)(param_3 + 0x2c) =", conv_start),
        "w": required_line(kairo, "*(uint *)(param_3 + 0x30) =", conv_start),
        "h": required_line(kairo, "*(uint *)(param_3 + 0x34) =", conv_start),
        "blend_flags": required_line(kairo, "*(uint *)(param_3 + 0x48) =", conv_start),
        "reverse_u_flag": required_line(kairo, "*(uint *)(param_3 + 0x40) =", conv_start),
        "reverse_v_flag": required_line(kairo, "*(uint *)(param_3 + 0x44) =", conv_start),
        "color": required_line(kairo, "*(uint *)(param_3 + 0x4c) =", conv_start),
    }

    core_draw_lines = {
        "offset_x": required_line(kairo, "fVar12 = *(float *)(lVar10 + 0x20)", seb_core_draw_start),
        "offset_y": required_line(kairo, "fVar11 = *(float *)(lVar10 + 0x24)", seb_core_draw_start),
        "destination_matrix_or_add": required_line(kairo, "kairo_unity_ui_Graphics__CheckLocalMatrix", seb_core_draw_start),
        "source_rect": required_line(kairo, "uVar5 = *(undefined4 *)(param_7 + 0x28)", seb_core_draw_start),
        "texture_lookup": required_line(kairo, "kairo_unity_ui_Seb__GetImage", seb_core_draw_start),
        "draw_image": required_line(kairo, "kairo_unity_ui_Graphics__DrawImage(param_1,param_2,param_4,local_88", seb_core_draw_start),
    }

    main_horizontal_lines = {
        "destination_x": required_line(main, "((float)(*(int *)(lVar4 + 0x38) + param_3)", main_horizontal_start),
        "destination_y": required_line(main, "(float)(*(int *)(lVar4 + 0x3c) + param_4)", main_horizontal_start),
        "source_u_with_repeat": required_line(main, "*(int *)(lVar4 + 0x28) + *(int *)(lVar4 + 0x30) * param_8", main_horizontal_start),
        "draw_image": required_line(main, "kairo_unity_ui_Graphics__DrawImage", main_horizontal_start),
    }
    main_vertical_lines = {
        "source_v_with_repeat": required_line(main, "*(int *)(lVar4 + 0x2c) + *(int *)(lVar4 + 0x34) * param_8", main_vertical_start),
        "draw_image": required_line(main, "kairo_unity_ui_Graphics__DrawImage", main_vertical_start),
    }
    main_normal_lines = {
        "destination_x": required_line(main, "((float)(*(int *)(lVar3 + 0x38) + param_3)", main_normal_start),
        "destination_y": required_line(main, "(float)(*(int *)(lVar3 + 0x3c) + param_4)", main_normal_start),
        "source_rect": required_line(main, "*(undefined4 *)(lVar3 + 0x28),*(undefined4 *)(lVar3 + 0x2c)", main_normal_start),
        "draw_image": required_line(main, "kairo_unity_ui_Graphics__DrawImage", main_normal_start),
    }
    main_reverse_lines = {
        "destination_x": required_line(main, "((float)((param_3 - *(int *)(lVar4 + 0x38)) - *(int *)(lVar4 + 0x30))", main_reverse_start),
        "destination_y": required_line(main, "(float)(*(int *)(lVar4 + 0x3c) + param_4)", main_reverse_start),
        "draw_image": required_line(main, "kairo_unity_ui_Graphics__DrawImage", main_reverse_start),
    }
    main_brect_lines = {
        "get_bounding_rect": required_line(main, "kairo_unity_ui_Seb__GetBoundingRect", main_brect_start),
        "add_base_x": required_line(main, "*(int *)(lVar4 + 0x20) = *(int *)(lVar3 + 0x20) + param_3", main_brect_start),
        "add_base_y": required_line(main, "*(int *)(lVar4 + 0x24) = *(int *)(lVar3 + 0x24) + param_4", main_brect_start),
        "copy_width": required_line(main, "*(undefined4 *)(lVar4 + 0x28) =", main_brect_start),
        "copy_height": required_line(main, "*(undefined4 *)(lVar4 + 0x2c) =", main_brect_start),
    }

    method_load_line = required_line(method, "kairo_unity_ui_ResourceManager__LoadSeb(uVar11)")
    dump_seb = required_line(dump, "public class Seb // TypeDefIndex: 1988")
    dump_resource_manager = required_line(dump, "public class ResourceManager // TypeDefIndex: 1974")
    dump_load_seb = required_line(dump, "public static Seb LoadSeb(byte[] src)")

    sample_record = w56["seb_sample"]["independent_decode"]["groups"][0]["records"][0]
    fields = sample_record["fields"]
    sample_effective_local_draw = {
        "status": "structural_probe_only_partial_record",
        "texture_id": fields["texture_id"],
        "source_rect_u_v_w_h": [fields["u"], fields["v"], fields["w"], fields["h"]],
        "local_destination_offset_x_y": [fields["trans_x"], fields["trans_y"]],
        "external_base_x_y": "caller supplied; not present in floor0.seb record",
        "missing_record_fields": sample_record["missing_fields"],
        "policy": "do not claim a successful render from the truncated sample",
    }

    return {
        "schema_version": "wave5-7-seb-consumer-contract-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "W5.7-SEB-consumer-crop-local-placement-and-anchor-trace",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "seb_local_crop_and_external_base_placement_verified_room_world_transform_open",
        "resource_chain": {
            "dump_api": {
                "class": "kairo.unity.ui.ResourceManager",
                "seb_array_field": "seb",
                "seb_array_offset": "0x18",
                "load_method": "LoadSeb(byte[] src)",
                "source_file": rel(DUMP_CS),
                "source_lines": {"class": dump_resource_manager, "load_method": dump_load_seb},
            },
            "native_loader": {
                "load_seb_function": "kairo_unity_ui_ResourceManager__LoadSeb",
                "constructor": "kairo_unity_ui_Seb___ctor",
                "source_file": rel(KAIRO_C),
                "source_lines": {"load_seb": resource_load_seb, "constructor": seb_ctor},
            },
            "resource_consumer_call": {
                "source_file": rel(METHOD_C),
                "source_line": method_load_line,
                "observed_flow": "JarInflater.GetData -> ResourceManager.LoadSeb -> resource array slot",
                "name_to_file_and_list_namespace": "not fully closed in this pass",
            },
        },
        "seb_record_contract": {
            "source_file": rel(DUMP_CS),
            "source_line": dump_seb,
            "constants": constants,
            "loader_and_conversion": {
                "get_sprites_local": get_sprites_local,
                "get_sprites": get_sprites,
                "get_sprite_local": get_sprite_local,
                "conv_buffer_to_sprite": conv_buffer_to_sprite,
                "record_flow": "GetSprites/GetSpritesLocal -> GetSpriteLocal -> ConvBufferToSprite -> sprite object",
                "field_semantics": "verified by Seb SP_* constants plus consumer field reads",
            },
            "sprite_object_offsets": {
                "texture_id": {"offset": "0x24", "field": "SP_TEX_ID", "source_line": field_source_lines["texture_id"]},
                "local_x": {"offset": "0x38", "field": "SP_TRANS_X", "source_line": field_source_lines["local_x"]},
                "local_y": {"offset": "0x3c", "field": "SP_TRANS_Y", "source_line": field_source_lines["local_y"]},
                "u": {"offset": "0x28", "field": "SP_U", "source_line": field_source_lines["u"]},
                "v": {"offset": "0x2c", "field": "SP_V", "source_line": field_source_lines["v"]},
                "w": {"offset": "0x30", "field": "SP_W", "source_line": field_source_lines["w"]},
                "h": {"offset": "0x34", "field": "SP_H", "source_line": field_source_lines["h"]},
                "blend_mode_low_nibble": {"offset": "0x48", "field": "SP_BLEND", "source_line": field_source_lines["blend_flags"]},
                "reverse_u_flag": {"offset": "0x40", "field": "SP_REVERS_U", "source_line": field_source_lines["reverse_u_flag"]},
                "reverse_v_flag": {"offset": "0x44", "field": "SP_REVERS_V", "source_line": field_source_lines["reverse_v_flag"]},
                "color": {"offset": "0x4c", "field": "SP_COLOR", "source_line": field_source_lines["color"]},
            },
            "special_texture_ids": {
                "TEXID_NONE": -1,
                "TEXID_FRECT": -2,
                "TEXID_RECT": -3,
                "TEXID_LINE": -4,
                "TEXID_HIDELINE": -8,
                "TEXID_HIDERECT": -9,
                "policy": "keep special primitive behavior separate from normal image crop",
            },
        },
        "seb_draw_contract": {
            "draw_image_shape": "DrawImage(destination_x, destination_y, image, source_u, source_v, source_w, source_h, alpha)",
            "core_consumer": {
                "function": "kairo_unity_ui_Seb__Draw",
                "source_line": seb_core_draw,
                "source_lines": core_draw_lines,
                "destination_formula": "(caller_x + offset_x + local_x, caller_y + offset_y + local_y), or the same values applied through a temporary local matrix",
                "source_formula": "(u, v, w, h)",
                "image_formula": "Seb.GetImage(texture_id), with optional custom image dictionary lookup",
                "status": "verified_local_crop_and_offset_flow",
            },
            "appdata_consumers": {
                "horizontal_repeat": {
                    "function": "main_AppData__DrawSeb",
                    "source_address": "0x00f79fe4",
                    "source_line": main_horizontal,
                    "source_lines": main_horizontal_lines,
                    "destination_formula": "(base_x + local_x, base_y + local_y)",
                    "source_formula": "(u + w * repeat_index, v, w, h)",
                },
                "vertical_repeat": {
                    "function": "main_AppData__DrawSebV",
                    "source_address": "0x00f7a0f4",
                    "source_line": main_vertical,
                    "source_lines": main_vertical_lines,
                    "destination_formula": "(base_x + local_x, base_y + local_y)",
                    "source_formula": "(u, v + h * repeat_index, w, h)",
                },
                "normal": {
                    "function": "main_AppData__DrawSeb",
                    "source_address": "0x00f7a204",
                    "source_line": main_normal,
                    "source_lines": main_normal_lines,
                    "destination_formula": "(base_x + local_x, base_y + local_y)",
                    "source_formula": "(u, v, w, h)",
                },
                "reverse_horizontal": {
                    "function": "main_AppData__DrawSebReverse",
                    "source_address": "0x00f7a2e4",
                    "source_line": main_reverse,
                    "source_lines": main_reverse_lines,
                    "destination_formula": "(base_x - local_x - w, base_y + local_y)",
                    "source_formula": "(u, v, w, h)",
                },
            },
            "decompiler_guardrail": "The first scaled DrawSeb overload prints sprite+0x38 for both x and y; the normal, horizontal, vertical, reverse, and core consumers use +0x38 for x and +0x3c for y, so the latter is the trusted y contract.",
        },
        "bounding_anchor_contract": {
            "bounding_rect": {
                "get_brect_frame_layer": get_brect_frame,
                "get_bounding_rect": get_bounding_rect,
                "get_brect": get_brect,
                "get_pixel_rect": get_pixel_rect,
                "pixel_rect_policy": "use optional pixelBoundingRects_ tail when present; otherwise fall back to BRect",
                "flip_policy": "BRect and PixelRect apply the SEB flip bits when selecting x/y extents",
            },
            "external_base": {
                "function": "main_AppData__GetBRectSeb",
                "source_file": rel(MAIN_C),
                "source_line": main_brect,
                "source_lines": main_brect_lines,
                "formula": "output_rect.x = seb_bounding_rect.x + base_x; output_rect.y = seb_bounding_rect.y + base_y; width/height copied",
                "status": "bounded_external_base_placement_verified",
            },
            "anchor_offset": {
                "get_anchor_position": seb_get_anchor,
                "draw_anchor": seb_draw_anchor,
                "set_offset": seb_set_offset,
                "clear_offset": seb_clear_offset,
                "observed_flow": "GetBoundingRect -> anchor adjustment -> SetOffset -> draw -> ClearOffset",
                "status": "anchor_adjustment_path_verified; anchor-bit naming remains open",
            },
        },
        "cross_renderer_comparison": {
            "legacy_object_draw": {
                "source": "Phases/Phase5/artifacts/wave5_3_numeric_crop_placement_contract.json",
                "destination": w53["crop_contract"]["draw_obj_fields"]["destination_x"] + ", " + w53["crop_contract"]["draw_obj_fields"]["destination_y"],
                "source_rect": w53["crop_contract"]["draw_obj_fields"]["source_rect"],
            },
            "seb_draw": {
                "destination": "base_x + SP_TRANS_X, base_y + SP_TRANS_Y",
                "source_rect": ["SP_U", "SP_V", "SP_W", "SP_H"],
            },
            "comparison_status": "same DrawImage argument shape; object and SEB field namespaces remain separate",
            "transform_policy": "do not infer a universal room/object/crop/screen transform from this shared call shape",
        },
        "floor0_probe": {
            "source_artifact": rel(W56),
            "record_status": sample_record["status"],
            "effective_local_draw": sample_effective_local_draw,
            "interpretation": "the available bytes are consistent with a 600x600 local crop at zero local offset, but reverse fields are absent and the file is truncated",
        },
        "room_placement": {
            "status": "bounded_local_placement_verified_room_world_transform_open",
            "closed": [
                "SEB texture id to image lookup at the draw consumer",
                "SEB U/V/W/H source crop flow",
                "SEB local trans_x/trans_y plus external base x/y destination flow",
                "bounded GetBRectSeb external base addition",
                "anchor helper offset lifecycle at the SEB API boundary",
            ],
            "open": [
                "which room/floor caller supplies the complete external base x/y",
                "floor PNG to complete room SEB mapping",
                "universal world/object/crop/screen or isometric transform",
                "exact anchor bit enum meaning and pivot policy",
                "depth/z semantics and DepthMethod coordinate conversion",
                "legacy-equivalent handling of the four-byte final-record shortfall",
            ],
            "policy": "use the verified local contract in adapters, but keep full room reconstruction and legacy_equivalence=false",
        },
        "remaining_gap": {
            "id": "W5-GAP-009",
            "status": "partially_closed_seb_local_crop_and_base_placement",
            "closed": [
                "IndexImgFloorParts selector and SEB structural framing from W5.6",
                "SEB consumer crop fields and local destination offsets",
                "bounded external base and anchor offset paths",
            ],
            "open": [
                "full SEB room reconstruction",
                "room/world/isometric transform and pivot semantics",
                "depth semantics",
                "complete legacy-equivalent renderer",
            ],
        },
        "guardrails": [
            "Keep office/floor0.seb separate from game/floorparts0.png and game/floor0.png selector namespaces.",
            "Treat the local SEB draw formula as verified only at the consumer boundary; do not infer its caller's room/world coordinates.",
            "Do not pad or synthesize missing reverse fields in the 24-byte floor0.seb sample.",
            "Keep the first scaled DrawSeb y expression as a decompiler discrepancy, not a second placement contract.",
            "Keep legacy_equivalence=false.",
        ],
        "source_files": {
            rel(KAIRO_C): sha256(KAIRO_C),
            rel(MAIN_C): sha256(MAIN_C),
            rel(METHOD_C): sha256(METHOD_C),
            rel(DUMP_CS): sha256(DUMP_CS),
            rel(W53): sha256(W53),
            rel(W56): sha256(W56),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    artifact = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": rel(args.output), "status": artifact["status"]}))


if __name__ == "__main__":
    main()
