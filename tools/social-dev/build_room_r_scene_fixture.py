"""Build the evidence-backed Room R raw scene fixture.

The fixture is a diagnostic/runtime contract for room:17. It preserves the
native 10x10 ObjChip grid and the shared 14x14 MapChip link, but does not
promote raw slots into FurnitureData instances or invent wall/door coordinates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FULL_CATALOG = ROOT / "knowledge/fixtures/accepted/room_catalog_full.json"
ROOM_RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json"
KNOWLEDGE_OUTPUT = ROOT / "knowledge/fixtures/accepted/room_r_scene_fixture.json"
RUNTIME_OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/room_r_scene_contract.json"

RAW_LABELS = {
    0: "empty_walkable",
    1: "place_slot_or_fixture",
    2: "desk_slot_or_fixture",
    3: "footprint_fixture",
    4: "anchor_fixture",
    5: "door_fixture",
    6: "boundary_fixture",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def room_record(full: dict[str, Any]) -> dict[str, Any]:
    for room in full["rooms"]:
        if room["room_key"] == "room:17":
            return room
    raise ValueError("room:17 is missing from the full RoomData catalog")


def runtime_record(runtime: dict[str, Any]) -> dict[str, Any]:
    for room in runtime["rooms"]:
        if room["room_key"] == "room:17":
            return room
    raise ValueError("room:17 is missing from the room runtime contract")


def build() -> dict[str, Any]:
    full = load(FULL_CATALOG)
    runtime = load(ROOM_RUNTIME)
    room = room_record(full)
    runtime_room = runtime_record(runtime)
    obj_chip = room["obj_chip"]

    raw_cells = []
    for cell in obj_chip["cells"]:
        raw_type = int(cell["raw_type"])
        x = int(cell["x"])
        y = int(cell["y"])
        raw_cells.append(
            {
                "cell_id": f"mapcell:room:17:obj:{x}:{y}",
                "source_cell_id": cell["cell_id"],
                "room_id": "room:17",
                "grid": "obj",
                "x": x,
                "y": y,
                "flat_index": int(cell["flat_index"]),
                "raw_type": raw_type,
                "raw_type_label": cell["raw_type_label"],
                "raw_direction": int(cell["raw_direction"]),
                "direction_status": cell["direction_status"],
                "identity_status": "raw_only_no_furniture_data_inference",
                "instance_id": None,
                "render_status": "diagnostic_raw_overlay_only",
                "source_status": cell["source_status"],
            }
        )

    groups = []
    for raw_type in sorted({cell["raw_type"] for cell in raw_cells}):
        cells = [cell for cell in raw_cells if cell["raw_type"] == raw_type]
        groups.append(
            {
                "raw_type": raw_type,
                "label": RAW_LABELS.get(raw_type, f"raw_type_{raw_type}"),
                "count": len(cells),
                "cells": [[cell["x"], cell["y"]] for cell in cells],
                "identity_status": "raw_only_no_furniture_data_inference",
            }
        )

    map_chip = room["map_chip"]
    topology = map_chip["default_topology_variant"]
    door_cells = [
        {"cell_id": cell["cell_id"], "x": cell["x"], "y": cell["y"]}
        for cell in raw_cells
        if cell["raw_type"] == 5
    ]

    body = {
        "schema_version": "social-dev-room-r-scene-fixture-v1",
        "package": "social-dev-room-r-scene-fixture",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "fixture_semantic_status": "raw_scene_fixture",
        "catalog_id": "display-slice-01",
        "room_id": "room:17",
        "data_key": room["data_key"],
        "native": room["native"],
        "source": {
            **room["source"],
            "full_catalog_path": "knowledge/fixtures/accepted/room_catalog_full.json",
            "room_runtime_path": "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json",
            "room_runtime_contract_hash": runtime["determinism"]["content_hash"],
        },
        "grid": {
            "width": obj_chip["width"],
            "height": obj_chip["height"],
            "obj_map": obj_chip["obj_map"],
            "obj_dir": obj_chip["obj_dir"],
        },
        "raw_cells": raw_cells,
        "raw_type_groups": groups,
        "door_cells": door_cells,
        "selectors": room["selectors"],
        "map_chip": {
            "contract_path": map_chip["contract_path"],
            "status": map_chip["status"],
            "shared_topology": True,
            "width": 14,
            "height": 14,
            "topology_selection": map_chip["topology_selection"],
            "default_variant": {
                "length": topology["length"],
                "rows": topology["rows"],
                "metadata_offset": topology["metadata_offset"],
                "metadata_hash": topology["metadata_hash"],
            },
        },
        "native_bindings": runtime_room["native_bindings"],
        "runtime_policy": {
            "raw_overlay_is_diagnostic_only": True,
            "raw_types_are_not_furniture_data_ids": True,
            "direction_labels_are_not_invented": True,
            "native_wall_door_coordinate_composition_not_implied": True,
            "unbound_slots_are_not_drawn_as_native_objects": True,
        },
        "unresolved": [
            "direction:raw_values_preserved_until_native_vector_trace_closes",
            "wall:native_coordinate_composition_not_closed_for:room:17",
            "door:native_coordinate_composition_not_closed_for:room:17",
        ],
        "counts": {
            "raw_cells": len(raw_cells),
            "raw_type_groups": len(groups),
            "raw_type_counts": {str(key): value for key, value in obj_chip["raw_type_counts"].items()},
            "door_cells": len(obj_chip["door_cells"]),
            "native_bindings": len(runtime_room["native_bindings"]),
            "map_cells": 14 * 14,
        },
    }
    return {**body, "determinism": {"algorithm": "stable-json-sha256", "content_hash": content_hash(body)}}


def main() -> None:
    result = build()
    KNOWLEDGE_OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    RUNTIME_OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "room": result["room_id"], "raw_cells": result["counts"]["raw_cells"], "content_hash": result["determinism"]["content_hash"]}))


if __name__ == "__main__":
    main()
