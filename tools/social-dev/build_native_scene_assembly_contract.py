"""Build the end-to-end native scene assembly contract for all 18 rooms.

This contract is the bridge between the evidence catalogs and the renderer. It
keeps the native lifecycle order, the two independent grids, the exact native
direction mapping, the generic wall/door predicates, and every room selector
asset in one queryable record. No FurnitureData identity is inferred from a
raw ObjChip type.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ROOM_RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json"
ROOM_ASSETS = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json"
DEFAULT_MAP = ROOT / "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"
STRICT = ROOT / "knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json"
NATIVE_CONTENT = ROOT / "knowledge/fixtures/accepted/runtime/native_content_catalog.json"
OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def cells_for_wall(room: dict[str, Any]) -> dict[str, list[list[int]]]:
    width = room["grid"]["width"]
    height = room["grid"]["height"]
    raw_cells = room["raw_cells"]
    vertical = [
        [cell["x"], cell["y"]]
        for cell in raw_cells
        if cell["raw_type"] != 5 and cell["y"] >= 1 and cell["y"] < height - 1 and cell["x"] == width - 2
    ]
    horizontal = [
        [cell["x"], cell["y"]]
        for cell in raw_cells
        if cell["x"] >= 1 and cell["y"] == 1 and cell["x"] < width - 1 and cell["raw_type"] != 5
    ]
    return {"vertical_frame_1": vertical, "horizontal_frame_0": horizontal}


def selector_ref(room: dict[str, Any], asset_manifest: dict[str, Any], role: str, assets_by_id: dict[str, Any]) -> dict[str, Any]:
    selector = room["selectors"][role]
    manifest_selector = asset_manifest[role]
    asset_id = manifest_selector["asset_id"]
    asset = assets_by_id[asset_id]
    return {
        "role": role,
        "raw_selector_id": selector["native_id"],
        "native_selector_id": selector.get("native_selector_id"),
        "filename": selector.get("target_filename"),
        "asset_id": asset_id,
        "runtime_path": asset["runtime_path"],
        "sha256": asset["sha256"],
        "source_status": selector["status"],
        "runtime_status": manifest_selector["runtime_status"],
    }


def build_payload() -> dict[str, Any]:
    room_runtime = load(ROOM_RUNTIME)
    room_assets = load(ROOM_ASSETS)
    default_map = load(DEFAULT_MAP)
    strict = load(STRICT)
    native_content = load(NATIVE_CONTENT)
    assets_by_id = {asset["asset_id"]: asset for asset in room_assets["assets"]}
    manifest_by_room = {room["room_key"]: room["assets"] for room in room_assets["rooms"]}
    strict_wall = strict["wall"]
    strict_door = strict["door"]

    direction_values = {
        "0": {"label": "DIRECTION_RIGHT", "vector": [0, 1], "reverse": 1},
        "1": {"label": "DIRECTION_LEFT", "vector": [0, -1], "reverse": 0},
        "2": {"label": "DIRECTION_UP", "vector": [1, 0], "reverse": 3},
        "3": {"label": "DIRECTION_DOWN", "vector": [-1, 0], "reverse": 2},
    }

    rooms: list[dict[str, Any]] = []
    for room in room_runtime["rooms"]:
        room_key = room["room_key"]
        manifest_assets = manifest_by_room[room_key]
        wall_cells = cells_for_wall(room)
        door_cells = [
            [cell["x"], cell["y"]]
            for cell in room["raw_cells"]
            if cell["raw_type"] == 5
        ]
        native_bindings = room["native_bindings"]
        binding_status = (
            "native_initial_instances_verified"
            if native_bindings
            else "no_native_furniture_instance_emitted_by_constructor_evidence"
        )
        rooms.append(
            {
                "room_key": room_key,
                "data_key": room["data_key"],
                "native": room["native"],
                "map_chip": {
                    "native_field": "Room.floor_",
                    "native_floor_value": 0,
                    "selected_variant": "floor_0",
                    "variant_rows": default_map["native_static_arrays"]["map_chip_array_by_floor"]["floor_0"]["rows"],
                    "selection_status": "explicit_current_runtime_fixture_floor_value",
                    "source_status": "AppData.NewGame constructs the active display Room with floor argument 0; RoomData does not select MapChip topology.",
                },
                "selectors": {
                    role: selector_ref(room, manifest_assets, role, assets_by_id)
                    for role in ("floor", "wall", "door")
                },
                "objchip_grid": {
                    "width": room["grid"]["width"],
                    "height": room["grid"]["height"],
                    "cell_count": len(room["raw_cells"]),
                    "source_map_field": "RoomData.objMap_",
                    "source_direction_field": "RoomData.objDir_",
                    "constructor": "new ObjChip(ix, iy, 0, null, this)",
                    "parent_setup": "Room.SetupBigChipsParent",
                    "raw_cell_identity": "objchip:<room_key>:<x>:<y>",
                    "native_furniture_identity_policy": "Only explicit Room.PlaceDesk/PlaceObj bindings receive FurnitureData IDs; raw_type remains a structural slot/type value.",
                },
                "object_cells": [
                    {
                        "instance_id": f"objchip:{room_key}:{cell['x']}:{cell['y']}",
                        "cell": [cell["x"], cell["y"]],
                        "raw_type": cell["raw_type"],
                        "raw_direction": cell["raw_direction"],
                        "direction": direction_values[str(cell["raw_direction"])],
                        "furniture_data_id": next(
                            (binding["furniture_data_id"] for binding in native_bindings if binding["cell"] == [cell["x"], cell["y"]]),
                            None,
                        ),
                        "object_id": next(
                            (binding["object_id"] for binding in native_bindings if binding["cell"] == [cell["x"], cell["y"]]),
                            None,
                        ),
                        "identity_status": "explicit_native_furniture_binding"
                        if any(binding["cell"] == [cell["x"], cell["y"]] for binding in native_bindings)
                        else "raw_objchip_instance_without_furniture_data_identity",
                    }
                    for cell in room["raw_cells"]
                ],
                "native_furniture_bindings": native_bindings,
                "native_furniture_binding_status": binding_status,
                "wall": {
                    "status": "approved_native_coordinate_composition",
                    "predicate": strict_wall["native_predicate"],
                    "cells_by_frame": wall_cells,
                    "seb": {
                        "selector_id": strict_wall["seb_selector_id"],
                        "filename": strict_wall["seb_filename"],
                    },
                    "sprite_records": strict_wall["sprite_records"],
                    "sprite_layers": strict_wall["sprite_layers"],
                    "draw_semantics": strict_wall["draw_semantics"],
                    "image_selector": selector_ref(room, manifest_assets, "wall", assets_by_id),
                },
                "door": {
                    "status": "approved_native_coordinate_composition",
                    "predicate": "raw_type == 5",
                    "cells": door_cells,
                    "raw_type": 5,
                    "installed_flag": strict_door["native_binding"]["installed_flag"],
                    "furniture_data": None,
                    "seb": {
                        "selector_id": strict_door["seb_selector_id"],
                        "filename": strict_door["seb_filename"],
                    },
                    "sprite_record": strict_door["sprite_record"],
                    "image_selector": selector_ref(room, manifest_assets, "door", assets_by_id),
                },
                "draw_commands": [
                    {
                        "pass_id": "map-extension-floor",
                        "native_method": "MapChip.DrawExtentionFloor",
                        "source": "shared MapChip extension wall contract",
                    },
                    {"pass_id": "map-chip", "native_method": "MapChip.Draw", "source": "selected Room.floor_ topology"},
                    {"pass_id": "object-chip-primary", "native_method": "ObjChip.Draw", "source": "explicit FurnitureData instances only"},
                    {"pass_id": "object-chip-wall", "native_method": "ObjChip.DrawWall", "source": "wall predicate and raw door type 5"},
                    {"pass_id": "avatar-primary", "native_method": "Avatar.Draw", "source": "actor catalog"},
                    {"pass_id": "avatar-secondary", "native_method": "Avatar.DrawSecondary", "source": "actor catalog"},
                    {"pass_id": "object-chip-late-preview", "native_method": "ObjChip.DrawLatePreview", "source": "native pass slot"},
                    {"pass_id": "object-chip-late", "native_method": "ObjChip.DrawLate", "source": "native pass slot"},
                    {"pass_id": "map-floor", "native_method": "MapChip.DrawFloor", "source": "floor culling contract"},
                ],
                "source": {
                    "room_runtime_contract": "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json",
                    "room_asset_manifest": "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json",
                    "raw_cell_count": len(room["raw_cells"]),
                },
            }
        )

    body: dict[str, Any] = {
        "schema_version": "social-dev-native-scene-assembly-v1",
        "package": "social-dev-native-scene-assembly",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "refs": {
            "native_content_catalog": {
                "path": "knowledge/fixtures/accepted/runtime/native_content_catalog.json",
                "content_hash": native_content["determinism"]["content_hash"],
                "source_registry_hash": native_content["source_registry"]["content_hash"],
            },
            "room_runtime": "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json",
            "room_assets": "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json",
            "map_chip": "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
            "strict_closure": "knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json",
        },
        "native_lifecycle": [
            {"order": 0, "phase": "load", "native_method": "DataManager.Load", "input": "DataManager arrays and resource selector tables", "output": "native content catalog IDs"},
            {"order": 1, "phase": "bootstrap", "native_method": "AppData.NewGame", "input": "roomData_[0], constructor floor=0, initStaffs", "output": "active Room instance"},
            {"order": 2, "phase": "construct", "native_method": "Room::.ctor", "input": "width=14,height=14,floor,RoomData", "output": "MapChip grid + ObjChip grid"},
            {"order": 3, "phase": "map", "native_method": "Room.InitMapChips", "input": "Room.floor_ and RoomData.floorImgId_", "output": "14x14 MapChip topology and floor selector"},
            {"order": 4, "phase": "objects", "native_method": "Room.InitObjChips", "input": "RoomData.objMap_ and objDir_", "output": "10x10 ObjChip instances with raw type/direction"},
            {"order": 5, "phase": "parenting", "native_method": "Room.SetupBigChipsParent", "input": "ObjChip structural footprint/anchor types", "output": "parent-linked object chips"},
            {"order": 6, "phase": "door", "native_method": "Room.PlaceDoor", "input": "ObjChip.type_ == 5", "output": "installed door with FurnitureData=null"},
            {"order": 7, "phase": "initial_objects", "native_method": "Room.PlaceDesk", "input": "FLAG_INIT_DESK / FLAG_INIT_PLACE and empty raw slots", "output": "explicit native FurnitureData bindings"},
            {"order": 8, "phase": "draw", "native_method": "Room.Draw", "input": "MapChip, ObjChip, Avatar passes", "output": "nine ordered render passes"},
            {"order": 9, "phase": "update", "native_method": "Room.Update", "input": "runtime state", "output": "updated ObjChip/actor state"},
            {"order": 10, "phase": "persist", "native_method": "Room.Serialize", "input": "room instance state", "output": "saved room state"},
        ],
        "native_trace": {
            "binary": "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so",
            "direction": {
                "get_direction_vector_rva": "0x12C4754",
                "get_reverse_direction_rva": "0x12C47D4",
                "direction_field_offset": "0x48",
                "reverse_table_rodata_rva": "0x617F70",
                "reverse_table": [1, 0, 3, 2],
                "static_vector_constructor_rva": "0x12C59DC",
                "static_vectors": [[0, 1], [0, -1], [1, 0], [-1, 0]],
                "status": "reviewed_native_disassembly",
            },
            "draw_wall": {
                "rva": "0x12C0698",
                "coordinate_formula": {
                    "x": "ofx + (x + y) * 20",
                    "y": "ofy + (y - x) * 10 + 9",
                },
                "type_field_offset": "0x18",
                "index_field_offset": "0x10",
                "status": "reviewed_native_disassembly",
            },
            "source_refs": [
                "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs",
                "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/ObjChip.cs",
                "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs",
                "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/KairoEngine/main/AppData.cs",
            ],
        },
        "direction": {
            "native_field": "ObjChip.direction_",
            "raw_domain": [0, 1, 2, 3],
            "values": direction_values,
            "status": "closed_native_vector_and_reverse_mapping",
            "runtime_policy": {
                "preserve_raw_value": True,
                "expose_label_and_vector": True,
                "allow_rotation": False,
                "allow_directional_asset_selection": False,
            },
        },
        "coordinates": {
            "object_to_canvas": {
                "x": "ofx + (x + y) * 20",
                "y": "ofy + (y - x) * 10 + 9",
            },
            "wall_and_door_anchor": "object_to_canvas(raw ObjChip index)",
            "sprite_destination_is_applied_from_SEB_record": True,
        },
        "wall_door_composition": {
            "status": "closed_for_all_rooms",
            "wall": {
                "vertical_predicate": strict_wall["native_predicate"]["vertical_frame_1"],
                "horizontal_predicate": strict_wall["native_predicate"]["horizontal_frame_0"],
                "frame_records": strict_wall["sprite_records"],
                "seb_selector_id": strict_wall["seb_selector_id"],
                "seb_filename": strict_wall["seb_filename"],
                "image_is_room_selector": True,
            },
            "door": {
                "predicate": "ObjChip.type_ == 5",
                "frame_record": strict_door["sprite_record"],
                "seb_selector_id": strict_door["seb_selector_id"],
                "seb_filename": strict_door["seb_filename"],
                "installed_flag": strict_door["native_binding"]["installed_flag"],
                "FurnitureData": None,
                "image_is_room_selector": True,
            },
        },
        "rooms": rooms,
        "render_passes": rooms[0]["draw_commands"],
        "closure_decisions": [
            "Every room's raw ObjChip cell is represented as an ObjChip instance identity; raw type is never promoted to FurnitureData ID.",
            "The current runtime fixture explicitly supplies Room.floor_=0, selecting the verified floor_0 MapChip table for all catalog rooms; RoomData.floorImgId_ remains the independent floor image selector.",
            "Room.PlaceDoor is represented for every raw type-5 cell with FurnitureData=null and installed flag=1.",
            "Room.PlaceDesk/PlaceObj bindings are emitted only where the strict native initial-binding evidence provides a FurnitureData ID; empty rooms are a closed no-instance result, not an inferred identity.",
            "Wall and door sprite records are universal native SEB frame records; each room supplies its own authoritative wall/door PNG selector asset.",
            "The floor selector 5 policy remains explicit: selector/data identity 85/floor_09 is the runtime alias while floor_05.png supplies the approved render pixels.",
        ],
        "counts": {
            "rooms": len(rooms),
            "objchip_cells": sum(room["objchip_grid"]["cell_count"] for room in rooms),
            "wall_compositions_closed": sum(room["wall"]["status"] == "approved_native_coordinate_composition" for room in rooms),
            "door_compositions_closed": sum(room["door"]["status"] == "approved_native_coordinate_composition" for room in rooms),
            "room_selector_connections": sum(len(room["selectors"]) for room in rooms),
            "explicit_native_furniture_instances": sum(len(room["native_furniture_bindings"]) for room in rooms),
            "direction_values_closed": len(direction_values),
            "render_passes": len(rooms[0]["draw_commands"]),
        },
    }
    return {**body, "determinism": {"algorithm": "stable-json-sha256", "content_hash": content_hash(body)}}


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        "native_scene_assembly_built "
        f"rooms={payload['counts']['rooms']} "
        f"objchip_cells={payload['counts']['objchip_cells']} "
        f"wall={payload['counts']['wall_compositions_closed']} "
        f"door={payload['counts']['door_compositions_closed']}"
    )


if __name__ == "__main__":
    main()
