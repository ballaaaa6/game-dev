"""Deterministic checks for the complete RoomData catalog."""

from __future__ import annotations

import json
from pathlib import Path

import build_room_catalog as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    catalog_path = EVIDENCE / "room_catalog_full.json"
    contract_path = RUNTIME_EVIDENCE / "room_catalog_contract.json"
    catalog = load(catalog_path)
    contract = load(contract_path)
    rebuilt = builder.build_payload()

    assert catalog["schema_version"] == "social-dev-room-catalog-full-v1"
    assert catalog["status"] == "pass"
    assert catalog["semantic_status"] == "roomdata_complete_mapchip_shared_contract"
    assert catalog["content_hash"] == rebuilt["content_hash"]
    assert contract["catalog_content_hash"] == catalog["content_hash"]
    assert contract["registry_content_hash"] == catalog["registry_content_hash"]

    rooms = {room["room_key"]: room for room in catalog["rooms"]}
    assert list(rooms) == [f"room:{index}" for index in range(18)]
    assert len(rooms) == 18
    assert catalog["validation"]["total_objchip_cells"] == 1800
    assert catalog["validation"]["all_obj_grids_rectangular"] is True
    assert catalog["map_chip_scope"]["linked_rooms"] == [f"room:{index}" for index in range(18)]
    assert catalog["map_chip_scope"]["unlinked_room_count"] == 0
    assert catalog["native_floor_image_table"]["values"] == [0, 19, 20, 21, 22, 23, 82, 83, 84, 85, 95]
    assert catalog["native_floor_image_table"]["unresolved_entry_count"] == 0

    room_a = rooms["room:0"]
    assert room_a["native"]["name"] == "Floor A"
    assert room_a["obj_chip"]["width"] == room_a["obj_chip"]["height"] == 10
    assert room_a["obj_chip"]["door_cells"] == ["cell:room:0:obj:8:4"]
    assert room_a["obj_chip"]["raw_type_counts"] == {
        "0": 31,
        "1": 8,
        "2": 6,
        "3": 16,
        "4": 2,
        "5": 1,
        "6": 36,
    }
    assert room_a["selectors"]["floor"]["status"] == "resolved_by_native_floor_image_table"
    assert room_a["selectors"]["floor"]["native_selector_id"] == 23
    assert room_a["selectors"]["floor"]["runtime_alias"]["selector_id"] == 85
    assert room_a["selectors"]["floor"]["target_filename"] == "floor_05.png"
    assert room_a["selectors"]["wall"]["target_filename"] == "wall_00.png"
    assert room_a["selectors"]["door"]["target_filename"] == "door_01.png"
    assert room_a["map_chip"]["status"] == "linked_shared_native_contract"
    assert room_a["map_chip"]["width"] == room_a["map_chip"]["height"] == 14

    room_b = rooms["room:1"]
    assert room_b["selectors"]["floor"]["native_id"] == 0
    assert room_b["selectors"]["floor"]["native_selector_id"] == 0
    assert room_b["selectors"]["floor"]["target_filename"] == "floor_00.png"
    assert room_b["map_chip"]["status"] == "linked_shared_native_contract"

    room_r = rooms["room:17"]
    assert room_r["native"]["name"] == "Floor R"
    assert room_r["native"]["desk_num"] == 12
    assert room_r["native"]["equip_small_num"] == 30
    assert room_r["native"]["floor_img_id"] == 9
    assert room_r["native"]["wall_img_id"] == 94
    assert room_r["native"]["door_img_id"] == 93
    assert room_r["obj_chip"]["door_cells"] == ["cell:room:17:obj:8:3"]
    assert room_r["obj_chip"]["raw_type_counts"] == {
        "0": 21,
        "1": 30,
        "2": 12,
        "5": 1,
        "6": 36,
    }
    assert room_r["selectors"]["floor"]["status"] == "resolved_by_native_floor_image_table"
    assert room_r["selectors"]["floor"]["native_domain"] == "Room.FLOOR_IMAGE_ID_ARRAY"
    assert room_r["selectors"]["floor"]["native_selector_id"] == 85
    assert room_r["selectors"]["floor"]["target_filename"] == "floor_09.png"
    assert room_r["selectors"]["wall"]["target_filename"] == "wall_06.png"
    assert room_r["selectors"]["door"]["target_filename"] == "door_06.png"
    assert room_r["map_chip"]["status"] == "linked_shared_native_contract"

    assert catalog["validation"]["unresolved_selector_count"] == 0
    assert all(
        room["selectors"]["wall"]["status"] == "resolved"
        and room["selectors"]["door"]["status"] == "resolved"
        for room in rooms.values()
    )

    print(
        "room_catalog_test_passed "
        f"rooms={len(rooms)} "
        f"objchip_cells={catalog['validation']['total_objchip_cells']} "
        f"mapchip_linked={len(catalog['map_chip_scope']['linked_rooms'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
