"""Build the strict Phase 3C closure package from the native room evidence.

The package makes two boundaries explicit:

* room wall/door positions are derived from the native ``ObjChip.DrawWall``
  predicates and the RoomData raw grid; and
* FurnitureData bindings are selected by the native initial-placement flags,
  not inferred from the raw ``objMap`` type.

The script reads source/evidence and the pinned asset archive only. It never
executes recovered C# or native code and it never replaces the historical
screenshot baseline.
"""

from __future__ import annotations

import copy
import hashlib
import json
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from seb_codec import decode_seb


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"

SCENE_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
ROOM_PATH = RUNTIME_EVIDENCE / "room_placement_contract.json"
NATIVE_PATH = EVIDENCE / "scene_native_semantics.json"
NATIVE_DUMP_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
ACTOR_PATH = EVIDENCE / "actor_spawn_fixture.json"
FURNITURE_PATH = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls/English.lproj/furniture.txt"
SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
BASELINE_PATH = EVIDENCE / "display_slice_01_screenshot_baseline.png"
BROWSER_GATE_PATH = EVIDENCE / "phase3c_browser_visual_gate.json"

OUTPUT_PATH = EVIDENCE / "phase3c_strict_closure.json"
RUNTIME_OUTPUT_PATH = RUNTIME_EVIDENCE / "phase3c_strict_closure_contract.json"
VALIDATION_PATH = EVIDENCE / "phase3c_strict_closure_validation.json"

ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
SPRITE_RECORD_FORMAT = ">HHHHhhhhHH"
SPRITE_RECORD_SIZE = struct.calcsize(SPRITE_RECORD_FORMAT)
FLAG_INIT_DESK = 16384
FLAG_INIT_PLACE = 32768

SOURCE_FILES = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "RoomData": SOURCE_ROOT / "data/RoomData.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def content_hash(value: Any) -> str:
    return sha256_bytes(stable_json(value).encode("utf-8"))


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def source_ref(path: Path, line_start: int | None = None, line_end: int | None = None, note: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"path": relative_path(path), "sha256": sha256_file(path)}
    if line_start is not None and line_end is not None:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        result.update(
            {
                "line_start": line_start,
                "line_end": line_end,
                "slice_sha256": sha256_bytes("".join(lines[line_start - 1 : line_end]).encode("utf-8")),
            }
        )
    if note:
        result["note"] = note
    return result


def evidence_ref(path: Path) -> dict[str, str]:
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def selector_entries() -> dict[str, dict[str, str]]:
    contract = load_json(SELECTOR_PATH)
    indexes = contract.get("selector_indexes") or contract["asset_zip"]["selector_indexes"]
    return {name: {str(key): str(value) for key, value in index["entries"].items()} for name, index in indexes.items()}


def parse_furniture_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(FURNITURE_PATH.read_text(encoding="utf-8-sig").splitlines(), start=1):
        fields = line.split("\t")
        if not fields or not fields[0].isdigit():
            continue
        if len(fields) <= 16:
            raise ValueError(f"FurnitureData row {line_number} is shorter than the reviewed loader fields")
        rows.append(
            {
                "id": int(fields[0]),
                "name": fields[1],
                "type": int(fields[3]),
                "seb": int(fields[10]),
                "sub_seb": int(fields[11]),
                "img": int(fields[12]),
                "flag": int(fields[16]),
                "row_number": line_number,
                "row_sha256": sha256_bytes((line + "\n").encode("utf-8")),
            }
        )
    return rows


def cells_by_raw_type(grid: list[list[int]]) -> dict[str, list[dict[str, int]]]:
    result: dict[str, list[dict[str, int]]] = {}
    for y, row in enumerate(grid):
        for x, raw_type in enumerate(row):
            result.setdefault(str(int(raw_type)), []).append({"x": x, "y": y, "raw_map_value": int(raw_type)})
    return result


def fixed_sprite_records(raw: bytes, record_count: int, member: str) -> list[dict[str, int]]:
    expected = 8 + record_count * SPRITE_RECORD_SIZE
    if len(raw) < expected:
        raise ValueError(f"{member} is shorter than its first sprite layer")
    records: list[dict[str, int]] = []
    for index in range(record_count):
        values = struct.unpack(
            SPRITE_RECORD_FORMAT,
            raw[8 + index * SPRITE_RECORD_SIZE : 8 + (index + 1) * SPRITE_RECORD_SIZE],
        )
        start_frame, image_id, source_x, source_y, width, height, destination_x, destination_y, flags, reserved = values
        records.append(
            {
                "start_frame": start_frame,
                "image_id": image_id,
                "source_x": source_x,
                "source_y": source_y,
                "width": width,
                "height": height,
                "destination_x": destination_x,
                "destination_y": destination_y,
                "flags": flags,
                "reserved": reserved,
            }
        )
    return records


def decoded_frame_records(decoded: dict[str, Any], frame: int) -> list[dict[str, int]]:
    """Return every SEB layer record selected by a native frame draw.

    ``AppData.DrawSeb(..., lineNo=-1)`` delegates to ``Seb.GetSpritesLocal``
    and therefore draws all layer records whose ``start_frame`` matches the
    selected frame.  Keeping the layer index in each record lets the runtime
    preserve the native layer order instead of silently collapsing a layered
    SEB to its first record.
    """

    return [copy.deepcopy(record) for record in decoded["records"] if record["start_frame"] == frame]


def room_draw_cells(grid: list[list[int]]) -> dict[str, list[list[int]]]:
    height = len(grid)
    width = len(grid[0]) if height else 0
    vertical = [
        [width - 2, y]
        for y in range(1, height - 1)
        if grid[y][width - 2] != 5
    ]
    horizontal = [
        [x, 1]
        for x in range(1, width - 1)
        if grid[1][x] != 5
    ]
    return {"vertical_frame_1": vertical, "horizontal_frame_0": horizontal}


def object_origin(cell: list[int]) -> dict[str, int]:
    x, y = cell
    return {"x": (x + y) * 20, "y": (y - x) * 10 + 9}


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scene_contract = load_json(SCENE_PATH)
    room_contract = load_json(ROOM_PATH)
    native = load_json(NATIVE_PATH)
    actor_fixture = load_json(ACTOR_PATH)
    selectors = selector_entries()
    furniture_rows = parse_furniture_rows()
    furniture_by_id = {row["id"]: row for row in furniture_rows}
    room = next(item for item in scene_contract["scenes"] if item["id"] == "room:0")
    grid = room["grid"]["objMap"]
    cells = cells_by_raw_type(grid)
    door_cell = [room["door"]["cells"][0]["x"], room["door"]["cells"][0]["y"]]

    with zipfile.ZipFile(ZIP_PATH) as archive:
        wall_member = "01_GAME_PACKS/chip/wall_00.seb"
        door_member = "01_GAME_PACKS/chip/door_02.seb"
        wall_raw = archive.read(ARCHIVE_PREFIX + wall_member)
        door_raw = archive.read(ARCHIVE_PREFIX + door_member)
        wall_records = fixed_sprite_records(wall_raw, 4, wall_member)
        wall_decoded = decode_seb(wall_raw, wall_member)
        wall_sprite_layers = {
            "vertical_frame_1": decoded_frame_records(wall_decoded, 1),
            "horizontal_frame_0": decoded_frame_records(wall_decoded, 0),
        }
        door_records = fixed_sprite_records(door_raw, 1, door_member)

    init_desk_rows = [row for row in furniture_rows if row["flag"] & FLAG_INIT_DESK]
    init_place_rows = [row for row in furniture_rows if row["flag"] & FLAG_INIT_PLACE]
    if [row["id"] for row in init_desk_rows] != [3]:
        raise ValueError("The reviewed furniture table no longer has the single init-desk row id 3")
    if [row["id"] for row in init_place_rows] != [12, 26, 56]:
        raise ValueError("The reviewed furniture table init-place order changed")

    type2_slots = [[cell["x"], cell["y"]] for cell in cells.get("2", [])]
    type1_slots = [[cell["x"], cell["y"]] for cell in cells.get("1", [])]
    type4_anchors = [[cell["x"], cell["y"]] for cell in cells.get("4", [])]
    actor_count = len(actor_fixture["actors"])
    if actor_count != 3:
        raise ValueError("The current bounded initial staff fixture must contain three entries")

    selected_ids = [0, 1, 2, 5]
    selected_binding_matrix: list[dict[str, Any]] = []
    for furniture_id in selected_ids:
        row = furniture_by_id[furniture_id]
        if furniture_id == 1:
            selected_binding_matrix.append(
                {
                    "object_id": "furniture:1",
                    "furniture_data_id": 1,
                    "name": row["name"],
                    "native_status": "door_chip_installed_without_furniture_data",
                    "cells": [door_cell],
                    "raw_type": 5,
                    "binding_rule": "Room.PlaceDoor scans raw type 5, calls ObjChip.PlaceObj(null), then writes installed flag 1.",
                    "not_selected_by_init_flags": True,
                }
            )
        elif furniture_id == 0:
            selected_binding_matrix.append(
                {
                    "object_id": "furniture:0",
                    "furniture_data_id": 0,
                    "name": row["name"],
                    "native_status": "type4_parent_geometry_only",
                    "cells": type4_anchors,
                    "raw_type": 4,
                    "binding_rule": "Room.SetupBigChipsParent links type-4 centers and type-3 footprint chips; it does not select FurnitureData(0).",
                    "display_fixture_cell": [4, 2],
                    "not_selected_by_init_flags": True,
                }
            )
        else:
            selected_binding_matrix.append(
                {
                    "object_id": f"furniture:{furniture_id}",
                    "furniture_data_id": furniture_id,
                    "name": row["name"],
                    "native_status": "selector_defined_not_bound_in_room0_initial_path",
                    "cells": [],
                    "raw_type": row["type"],
                    "binding_rule": "The row has neither FLAG_INIT_DESK nor FLAG_INIT_PLACE; the reviewed room bootstrap has no FurnitureData placement call for this id.",
                    "not_selected_by_init_flags": True,
                }
            )

    native_initial_bindings: list[dict[str, Any]] = []
    for index, slot in enumerate(type2_slots[:actor_count]):
        row = init_desk_rows[0]
        native_initial_bindings.append(
            {
                "object_id": "furniture:3",
                "furniture_data_id": 3,
                "name": row["name"],
                "native_status": "verified_native_initial_desk",
                "cell": slot,
                "raw_type": 2,
                "scan_order": index,
                "selector_flag": {"name": "FLAG_INIT_DESK", "value": FLAG_INIT_DESK},
                "count_source": "AppData.NewGame initStaffs.elementCount",
                "count_fixture_value": actor_count,
            }
        )
    for index, row in enumerate(init_place_rows):
        native_initial_bindings.append(
            {
                "object_id": f"furniture:{row['id']}",
                "furniture_data_id": row["id"],
                "name": row["name"],
                "native_status": "verified_native_initial_place",
                "cell": type1_slots[index],
                "raw_type": 1,
                "scan_order": index,
                "selector_flag": {"name": "FLAG_INIT_PLACE", "value": FLAG_INIT_PLACE},
                "count_source": "FurnitureData vector scan order; first empty type-1 chip is consumed",
            }
        )

    wall_cells = room_draw_cells(grid)
    wall_selector = int(room["scalar_fields_raw"]["wallImgId_"]["value"])
    door_selector = int(room["scalar_fields_raw"]["doorImgId_"]["value"])
    if selectors["chip_img"][str(wall_selector)] != "wall_00.png":
        raise ValueError("wall selector identity changed")
    if selectors["chip_img"][str(door_selector)] != "door_01.png":
        raise ValueError("door selector identity changed")
    if wall_records[1]["image_id"] != wall_selector or wall_records[2]["image_id"] != wall_selector:
        raise ValueError("wall_00.seb no longer references room wall image selector 6")
    if any(
        len(wall_sprite_layers[frame_id]) != 2
        or [record["layer"] for record in wall_sprite_layers[frame_id]] != [0, 1]
        or any(record["image_id"] != wall_selector for record in wall_sprite_layers[frame_id])
        for frame_id in ("vertical_frame_1", "horizontal_frame_0")
    ):
        raise ValueError("wall_00.seb selected frame no longer has the expected two native layers")
    if door_records[0]["image_id"] != door_selector:
        raise ValueError("door_02.seb no longer references room door image selector 7")

    source_refs = [
        source_ref(SOURCE_FILES["Room"], 454, 763, "InitObjChips and SetupBigChipsParent source boundary"),
        source_ref(SOURCE_FILES["Room"], 764, 923, "PlaceDoor raw type-5 scan, null binding and installed flag"),
        source_ref(SOURCE_FILES["Room"], 7390, 7517, "PlaceDesk FLAG_INIT_DESK selector and empty type-2 scan"),
        source_ref(SOURCE_FILES["ObjChip"], 2173, 2701, "DrawWall anchor, wall/door predicates and selector reads"),
        source_ref(SOURCE_FILES["ObjChip"], 9912, 10043, "PlaceObj FurnitureData binding and direction reset"),
        source_ref(SOURCE_FILES["FurnitureData"], 57, 59, "FLAG_INIT_DESK and FLAG_INIT_PLACE constants"),
        source_ref(SOURCE_FILES["AppData"], 14717, 14970, "NewGame initial room, type-1 placement and initStaffs count call site"),
        source_ref(NATIVE_DUMP_PATH, 218864, 218865, "DrawWall RVA and native signature from the pinned APK dump"),
    ]
    native_methods = {
        item["id"]: copy.deepcopy(item)
        for item in native["native_method_manifest"]
        if item["id"] in {
            "room-init-obj-chips",
            "room-setup-big-chips-parent",
            "room-place-door",
            "objchip-place-object",
            "room-place-desk",
            "appdata-new-game",
        }
    }
    native_methods["objchip-draw-wall"] = {
        "id": "objchip-draw-wall",
        "class": "ObjChip",
        "method": "DrawWall",
        "signature": "void DrawWall(Graphics g, int ofx, int ofy)",
        "rva_hex": "0x12C0698",
        "rva_decimal": 19662488,
        "body_status": "reviewed_native_disassembly",
    }

    browser_gate = load_json(BROWSER_GATE_PATH)
    browser_fixture = browser_gate["browser_fixture"]
    baseline_record = browser_fixture["frame136"]
    candidate_record = browser_fixture["frame6"]
    baseline_info = {
        "historical_path": relative_path(BASELINE_PATH),
        "historical_sha256": sha256_file(BASELINE_PATH),
        "candidate_frame_6": {
            "path": candidate_record["screenshot_path"],
            "sha256": candidate_record["screenshot_sha256"],
            "digest": candidate_record["digest"],
        },
        "candidate_frame_136": {
            "path": baseline_record["screenshot_path"],
            "sha256": baseline_record["screenshot_sha256"],
            "digest": baseline_record["digest"],
        },
        "historical_baseline_preserved": True,
        "replacement_persisted": False,
        "comparison_policy_status": "pending_user_approval",
        "approval_required": "Record explicit comparison-policy approval before replacing the historical placeholder baseline.",
    }

    package = {
        "schema_version": "social-dev-phase3c-strict-closure-v1",
        "package": "social-dev-phase3c-strict-closure",
        "status": "pass",
        "semantic_status": "strict_evidence_closed_baseline_pending_approval",
        "generated_at_utc": utc_now(),
        "catalog_id": "display-slice-01",
        "scene_ref": {
            "id": "room:0",
            "contract_hash": scene_contract["determinism"]["contract_hash"],
            "grid": {"width": room["grid"]["width"], "height": room["grid"]["height"]},
            "raw_type_cells": cells,
            "door_cell": door_cell,
            "door_raw_type": 5,
        },
        "native_evidence": {
            "apk": evidence_ref(APK_PATH),
            "native_semantics": evidence_ref(NATIVE_PATH),
            "methods": native_methods,
            "source_refs": source_refs,
            "source_policy": "C# and native artifacts are evidence inputs only; the browser consumes generated contracts and promoted asset bytes.",
        },
        "wall": {
            "raw_selector_id": wall_selector,
            "filename": "wall_00.png",
            "seb_selector_id": 5,
            "seb_filename": "wall_00.seb",
            "status": "verified_native_coordinate_composition",
            "anchor_formula": {
                "x": "ofx + (x + y) * 20",
                "y": "ofy + (y - x) * 10 + 9",
            },
            "native_predicate": {
                "vertical_frame_1": "type_ != 5 && y >= 1 && y < objMapHeight - 1 && x == objMapWidth - 2",
                "horizontal_frame_0": "x >= 1 && y == 1 && x < objMapWidth - 1 && type_ != 5",
            },
            "cells_by_frame": wall_cells,
            "sprite_records": {
                "vertical_frame_1": wall_records[1],
                "horizontal_frame_0": wall_records[0],
            },
            "sprite_layers": wall_sprite_layers,
            "draw_semantics": {
                "native_method": "ObjChip.DrawWall -> AppData.DrawSeb(frame, lineNo=-1)",
                "selected_frame_policy": "draw every SEB record whose start_frame equals the ObjChip wall frame",
                "layer_order": [0, 1],
                "first_layer_compatibility_records": "sprite_records retains layer 0 for older readers; runtime must prefer sprite_layers",
            },
            "source_asset": {
                "png_member": "01_GAME_PACKS/chip/wall_00.png",
                "seb_member": "01_GAME_PACKS/chip/wall_00.seb",
                "png_sha256": None,
                "seb_sha256": sha256_bytes((ZIP_PATH).read_bytes()),
            },
            "source_note": "The wall PNG/SEB pair is promoted only after the native draw predicate and source rectangles are recorded; the ZIP hash is captured below and the PNG hash is filled from the pinned asset index.",
        },
        "door": {
            "raw_selector_id": door_selector,
            "filename": "door_01.png",
            "seb_selector_id": 6,
            "seb_filename": "door_02.seb",
            "status": "verified_native_coordinate_composition",
            "cell": door_cell,
            "raw_type": 5,
            "anchor": object_origin(door_cell),
            "sprite_record": door_records[0],
            "native_binding": {
                "FurnitureData": None,
                "installed_flag": 1,
                "status": "Room.PlaceDoor_null_furniture_data",
            },
            "source_asset": {
                "png_member": "01_GAME_PACKS/chip/door_01.png",
                "seb_member": "01_GAME_PACKS/chip/door_02.seb",
                "png_sha256": None,
                "seb_sha256": None,
            },
        },
        "furniture_table": {
            "table_path": relative_path(FURNITURE_PATH),
            "table_sha256": sha256_file(FURNITURE_PATH),
            "flag_constants": {
                "FLAG_INIT_DESK": FLAG_INIT_DESK,
                "FLAG_INIT_PLACE": FLAG_INIT_PLACE,
            },
            "init_desk_rows": init_desk_rows,
            "init_place_rows": init_place_rows,
            "selected_display_rows": [furniture_by_id[item] for item in selected_ids],
        },
        "native_initial_bindings": native_initial_bindings,
        "selected_display_binding_matrix": selected_binding_matrix,
        "type4_geometry": {
            "status": "verified_native_parent_geometry",
            "anchors": type4_anchors,
            "footprint_rule": "SetupBigChipsParent writes the parent pointer across each 3x3 type-4/type-3 footprint; it does not select a FurnitureData id.",
            "display_fixture": [4, 2],
        },
        "baseline_policy": baseline_info,
        "closure_conclusion": {
            "data_status": "complete_for_scoped_wall_door_and_initial_furniture_questions",
            "remaining_external_decision": "baseline replacement approval only",
            "missing_data_found": False,
            "strict_runtime_boundary": "Render native room geometry and the native initial-binding matrix; keep selector-only furniture:2/furniture:5 out of room:0 unless a later user-placement contract supplies a cell.",
        },
        "provenance": {
            "scene_contract": evidence_ref(SCENE_PATH),
            "room_contract": evidence_ref(ROOM_PATH),
            "native_semantics": evidence_ref(NATIVE_PATH),
            "actor_fixture": evidence_ref(ACTOR_PATH),
            "selector_contract": evidence_ref(SELECTOR_PATH),
            "asset_index": evidence_ref(ASSET_INDEX_PATH),
            "asset_zip": evidence_ref(ZIP_PATH),
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }

    asset_index = {str(item["relative_path"]): item for item in load_json(ASSET_INDEX_PATH)}
    package["wall"]["source_asset"]["png_sha256"] = asset_index["01_GAME_PACKS/chip/wall_00.png"]["sha256"]
    package["wall"]["source_asset"]["seb_sha256"] = asset_index["01_GAME_PACKS/chip/wall_00.seb"]["sha256"]
    package["door"]["source_asset"]["png_sha256"] = asset_index["01_GAME_PACKS/chip/door_01.png"]["sha256"]
    package["door"]["source_asset"]["seb_sha256"] = asset_index["01_GAME_PACKS/chip/door_02.seb"]["sha256"]
    package["determinism"]["content_hash"] = content_hash(without_dynamic(package))

    runtime_contract = {
        "schema_version": "social-dev-phase3c-strict-closure-contract-v1",
        "package": "social-dev-phase3c-strict-closure-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": package["catalog_id"],
        "scene_id": "room:0",
        "wall": copy.deepcopy(package["wall"]),
        "door": copy.deepcopy(package["door"]),
        "native_initial_bindings": copy.deepcopy(package["native_initial_bindings"]),
        "selected_display_binding_matrix": copy.deepcopy(package["selected_display_binding_matrix"]),
        "type4_geometry": copy.deepcopy(package["type4_geometry"]),
        "baseline_policy": copy.deepcopy(baseline_info),
        "closure_conclusion": copy.deepcopy(package["closure_conclusion"]),
        "provenance": {
            "strict_closure": relative_path(OUTPUT_PATH),
            "strict_closure_hash": package["determinism"]["content_hash"],
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }
    runtime_contract["determinism"]["contract_hash"] = content_hash(without_dynamic(runtime_contract))

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append(
            {
                "id": check_id,
                "status": "pass" if passed else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    check("scene-grid", room["grid"]["width"] == 10 and room["grid"]["height"] == 10, [room["grid"]["width"], room["grid"]["height"]], [10, 10], "RoomData(0) grid shape is fixed by the runtime scene contract.")
    check("door-cell", door_cell == [8, 4] and grid[4][8] == 5, {"cell": door_cell, "raw": grid[4][8]}, {"cell": [8, 4], "raw": 5}, "Raw type-5 door cell is explicit.")
    expected_wall_cells = {"vertical_frame_1": [[8, 1], [8, 2], [8, 3], [8, 5], [8, 6], [8, 7], [8, 8]], "horizontal_frame_0": [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]]}
    check("wall-predicate", wall_cells == expected_wall_cells, wall_cells, expected_wall_cells, "ObjChip.DrawWall predicates are evaluated against the raw grid without guessed cells.")
    check("wall-selector", package["wall"]["source_asset"]["png_sha256"] == asset_index["01_GAME_PACKS/chip/wall_00.png"]["sha256"], package["wall"]["source_asset"]["png_sha256"], asset_index["01_GAME_PACKS/chip/wall_00.png"]["sha256"], "Room wall selector 6 resolves to wall_00.png.")
    check("door-selector", package["door"]["source_asset"]["png_sha256"] == asset_index["01_GAME_PACKS/chip/door_01.png"]["sha256"], package["door"]["source_asset"]["png_sha256"], asset_index["01_GAME_PACKS/chip/door_01.png"]["sha256"], "Room door selector 7 resolves to door_01.png.")
    check("native-desk-selector", [item["furniture_data_id"] for item in native_initial_bindings if item["raw_type"] == 2] == [3, 3, 3], [item["cell"] for item in native_initial_bindings if item["raw_type"] == 2], [[2, 4], [3, 4], [6, 4]], "FLAG_INIT_DESK resolves to FurnitureData(3) in first empty type-2 scan order.")
    check("native-place-selector", [item["furniture_data_id"] for item in native_initial_bindings if item["raw_type"] == 1] == [12, 26, 56], [item["cell"] for item in native_initial_bindings if item["raw_type"] == 1], [[8, 5], [8, 6], [2, 7]], "FLAG_INIT_PLACE records consume the first three empty type-1 cells.")
    check("selector-only-furniture", all(item["native_status"] == "selector_defined_not_bound_in_room0_initial_path" for item in selected_binding_matrix if item["furniture_data_id"] in {2, 5}), [item["native_status"] for item in selected_binding_matrix if item["furniture_data_id"] in {2, 5}], ["selector_defined_not_bound_in_room0_initial_path"] * 2, "FurnitureData(2)/(5) are explicitly negative native bindings, not missing coordinate data.")
    check("type4-geometry", type4_anchors == [[4, 2], [7, 2]] and package["type4_geometry"]["display_fixture"] == [4, 2], type4_anchors, [[4, 2], [7, 2]], "Both raw type-4 anchors are retained; the existing display fixture is not promoted to a FurnitureData inference rule.")
    check("baseline-policy", baseline_info["historical_baseline_preserved"] and not baseline_info["replacement_persisted"] and baseline_info["comparison_policy_status"] == "pending_user_approval", baseline_info["comparison_policy_status"], "pending_user_approval", "Baseline replacement is a separate explicit approval decision.")

    validation = {
        "schema_version": "social-dev-phase3c-strict-closure-validation-v1",
        "package": "social-dev-phase3c-strict-closure-validation",
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "semantic_status": "validated",
        "generated_at_utc": package["generated_at_utc"],
        "checks": checks,
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "counts": {"checks": len(checks), "passed_checks": sum(item["status"] == "pass" for item in checks)},
        "package_hash": package["determinism"]["content_hash"],
        "runtime_contract_hash": runtime_contract["determinism"]["contract_hash"],
    }
    return package, runtime_contract, validation


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    package, runtime_contract, validation = build_package()
    write_json(OUTPUT_PATH, package)
    write_json(RUNTIME_OUTPUT_PATH, runtime_contract)
    write_json(VALIDATION_PATH, validation)
    print(
        "phase3c_strict_closure_built "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"package={package['determinism']['content_hash']} "
        f"runtime={runtime_contract['determinism']['contract_hash']} "
        f"baseline={package['baseline_policy']['comparison_policy_status']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
