"""Build the runtime room/placement bridge from the verified RoomData catalog.

This is a contract builder only.  It reads the extracted evidence, records raw
ObjChip values without assigning FurnitureData identities, and carries the
shared MapChip topology reference into a compact browser-facing contract.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FULL_CATALOG = ROOT / "knowledge/fixtures/accepted/room_catalog_full.json"
ROOM_CATALOG_CONTRACT = ROOT / "knowledge/fixtures/accepted/runtime/room_catalog_contract.json"
DEFAULT_MAP = ROOT / "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"
STRICT_CLOSURE = ROOT / "knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json"
OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def raw_cell_groups(obj_map: list[list[int]], obj_dir: list[list[int]], cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    labels = {
        0: "empty_walkable",
        1: "place_slot_or_fixture",
        2: "desk_slot_or_fixture",
        3: "footprint_fixture",
        4: "anchor_fixture",
        5: "door_fixture",
        6: "boundary_fixture",
    }
    for raw_type in sorted({value for row in obj_map for value in row}):
        matching = [cell for cell in cells if cell["raw_type"] == raw_type]
        groups.append(
            {
                "raw_type": raw_type,
                "label": labels.get(raw_type, f"raw_type_{raw_type}"),
                "cells": [[cell["x"], cell["y"]] for cell in matching],
                "count": len(matching),
                "identity_status": "raw_only_no_furniture_data_inference",
            }
        )
    return groups


def build() -> dict[str, Any]:
    full = load(FULL_CATALOG)
    room_contract = load(ROOM_CATALOG_CONTRACT)
    default_map = load(DEFAULT_MAP)
    strict = load(STRICT_CLOSURE)
    strict_by_room: dict[str, list[dict[str, Any]]] = {}
    if strict.get("status") == "pass":
        strict_by_room[str(strict["scene_id"])] = [
            {
                "object_id": binding["object_id"],
                "furniture_data_id": binding["furniture_data_id"],
                "cell": binding["cell"],
                "raw_type": binding["raw_type"],
                "scan_order": binding["scan_order"],
                "selector_flag": binding["selector_flag"],
                "native_status": binding["native_status"],
                "source_status": "verified_strict_native_initial_binding",
            }
            for binding in strict.get("native_initial_bindings", [])
        ]

    rooms: list[dict[str, Any]] = []
    for room in full["rooms"]:
        room_key = str(room["room_key"])
        obj_chip = room["obj_chip"]
        obj_map = obj_chip["obj_map"]
        obj_dir = obj_chip["obj_dir"]
        raw_cells = [
            {
                "cell_id": cell["cell_id"],
                "cell": [cell["x"], cell["y"]],
                "x": cell["x"],
                "y": cell["y"],
                "raw_type": cell["raw_type"],
                "raw_type_label": cell["raw_type_label"],
                "raw_direction": cell["raw_direction"],
                "direction_status": cell["direction_status"],
                "source_status": cell["source_status"],
            }
            for cell in obj_chip["cells"]
        ]
        rooms.append(
            {
                "room_key": room_key,
                "data_key": room["data_key"],
                "native": room["native"],
                "selectors": room["selectors"],
                "grid": {
                    "width": obj_chip["width"],
                    "height": obj_chip["height"],
                    "obj_map": obj_map,
                    "obj_dir": obj_dir,
                },
                "raw_cell_groups": raw_cell_groups(obj_map, obj_dir, raw_cells),
                "raw_cells": raw_cells,
                "native_bindings": strict_by_room.get(room_key, []),
                "native_binding_status": "verified_strict_native_initial_binding"
                if room_key in strict_by_room
                else "not_available_no_native_instance_binding_in_evidence",
                "map_chip": {
                    "status": room["map_chip"]["status"],
                    "contract_path": room["map_chip"]["contract_path"],
                    "topology_selection": {
                        **room["map_chip"]["topology_selection"],
                        "native_floor_value": 0,
                        "selected_variant": "floor_0",
                        "selection_status": "explicit_current_runtime_fixture_floor_value",
                    },
                    "floor_image_table": room["map_chip"]["floor_image_table"],
                    "source_status": "linked_shared_native_mapchip_contract",
                },
                "source": room["source"],
            }
        )

    body = {
        "schema_version": "social-dev-room-scene-runtime-v1",
        "package": "social-dev-room-scene-runtime",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "room_catalog_ref": {
            "path": "knowledge/fixtures/accepted/runtime/room_catalog_contract.json",
            "catalog_content_hash": room_contract["catalog_content_hash"],
            "registry_content_hash": room_contract["registry_content_hash"],
            "status": room_contract["status"],
        },
        "map_chip_ref": {
            "path": "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
            "contract_hash": default_map["determinism"]["contract_hash"],
            "scene_ref": default_map["scene_ref"],
            "shared_topology": True,
            "selection_field": "Room.floor_",
            "selection_status": "verified_shared_native_mapchip_variant_contract",
        },
        "native_identity_policy": {
            "objchip_never_infers_furniture_data_id": True,
            "raw_types_are_not_asset_ids": True,
            "native_bindings_must_be_explicit": True,
            "unresolved_direction_keeps_raw_value": True,
            "raw_type_semantics": {
                "0": "empty_walkable",
                "1": "place_slot_or_fixture",
                "2": "desk_slot_or_fixture",
                "3": "footprint_fixture",
                "4": "anchor_fixture",
                "5": "door_fixture",
                "6": "boundary_fixture",
            },
        },
        "rooms": rooms,
        "counts": {
            "rooms": len(rooms),
            "raw_objchip_cells": sum(len(room["raw_cells"]) for room in rooms),
            "rooms_with_explicit_native_bindings": sum(bool(room["native_bindings"]) for room in rooms),
            "rooms_with_shared_mapchip_contract": sum(room["map_chip"]["status"] == "linked_shared_native_contract" for room in rooms),
        },
    }
    result = {**body, "determinism": {"algorithm": "stable-json-sha256", "content_hash": content_hash(body)}}
    return result


def main() -> None:
    result = build()
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "rooms": result["counts"]["rooms"], "content_hash": result["determinism"]["content_hash"]}))


if __name__ == "__main__":
    main()
