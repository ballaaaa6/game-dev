"""Validate the all-room native scene assembly contract."""

from __future__ import annotations

import json
from pathlib import Path

import build_native_scene_assembly_contract as builder


ROOT = builder.ROOT
CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    rebuilt = builder.build_payload()
    assert contract["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert contract["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["counts"] == {
        "rooms": 18,
        "objchip_cells": 1800,
        "wall_compositions_closed": 18,
        "door_compositions_closed": 18,
        "room_selector_connections": 54,
        "explicit_native_furniture_instances": 6,
        "direction_values_closed": 4,
        "render_passes": 9,
    }
    assert [step["phase"] for step in contract["native_lifecycle"]] == [
        "load", "bootstrap", "construct", "map", "objects", "parenting", "door",
        "initial_objects", "draw", "update", "persist",
    ]
    assert contract["direction"]["values"]["0"] == {"label": "DIRECTION_RIGHT", "vector": [0, 1], "reverse": 1}
    assert contract["direction"]["values"]["1"]["reverse"] == 0
    assert contract["direction"]["values"]["2"]["vector"] == [1, 0]
    assert contract["direction"]["values"]["3"]["reverse"] == 2
    assert contract["native_trace"]["direction"]["reverse_table"] == [1, 0, 3, 2]
    assert contract["native_trace"]["direction"]["static_vectors"] == [[0, 1], [0, -1], [1, 0], [-1, 0]]
    assert contract["wall_door_composition"]["status"] == "closed_for_all_rooms"
    assert contract["coordinates"]["object_to_canvas"]["x"] == "ofx + (x + y) * 20"
    assert contract["coordinates"]["object_to_canvas"]["y"] == "ofy + (y - x) * 10 + 9"

    rooms = contract["rooms"]
    assert [room["room_key"] for room in rooms] == [f"room:{index}" for index in range(18)]
    assert all(room["map_chip"]["selected_variant"] == "floor_0" for room in rooms)
    assert all(room["map_chip"]["native_floor_value"] == 0 for room in rooms)
    assert all(room["objchip_grid"]["cell_count"] == 100 for room in rooms)
    assert all(room["wall"]["status"] == "approved_native_coordinate_composition" for room in rooms)
    assert all(room["door"]["status"] == "approved_native_coordinate_composition" for room in rooms)
    assert all(len(room["door"]["cells"]) == 1 for room in rooms)
    assert all(room["door"]["furniture_data"] is None for room in rooms)
    assert all(room["door"]["installed_flag"] == 1 for room in rooms)
    assert len(rooms[0]["native_furniture_bindings"]) == 6
    assert all(len(room["native_furniture_bindings"]) == 0 for room in rooms[1:])
    assert all(len(room["object_cells"]) == 100 for room in rooms)
    assert all(
        cell["instance_id"].startswith(f"objchip:{room['room_key']}:")
        for room in rooms
        for cell in room["object_cells"]
    )
    assert any(cell["identity_status"] == "explicit_native_furniture_binding" for cell in rooms[0]["object_cells"])
    assert all(
        role_ref["runtime_path"].startswith("assets/room-scene/")
        for room in rooms
        for role_ref in room["selectors"].values()
    )
    assert all(len(room["draw_commands"]) == 9 for room in rooms)
    assert not contract.get("open_items")
    assert not contract.get("blockers")

    print(
        "native_scene_assembly_contract_test_passed "
        f"rooms={contract['counts']['rooms']} cells={contract['counts']['objchip_cells']} passes={contract['counts']['render_passes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
