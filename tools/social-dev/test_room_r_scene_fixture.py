"""Regression checks for the Room R raw scene fixture."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "knowledge/fixtures/accepted/room_r_scene_fixture.json"
RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime/room_r_scene_contract.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    fixture = load(FIXTURE)
    runtime = load(RUNTIME)
    assert fixture == runtime, "knowledge fixture and runtime contract drifted"
    assert fixture["status"] == "pass"
    assert fixture["semantic_status"] == "approved_for_runtime_contract"
    assert fixture["fixture_semantic_status"] == "raw_scene_fixture"
    assert fixture["room_id"] == "room:17"
    assert fixture["grid"]["width"] == 10
    assert fixture["grid"]["height"] == 10
    assert len(fixture["raw_cells"]) == 100
    assert fixture["counts"]["raw_type_counts"] == {"0": 21, "1": 30, "2": 12, "5": 1, "6": 36}
    assert fixture["counts"]["door_cells"] == 1
    assert fixture["counts"]["native_bindings"] == 0
    assert fixture["native"]["floor_img_id"] == 9
    assert fixture["native"]["wall_img_id"] == 94
    assert fixture["native"]["door_img_id"] == 93
    assert fixture["door_cells"] == [{"cell_id": "mapcell:room:17:obj:8:3", "x": 8, "y": 3}]
    assert fixture["map_chip"]["shared_topology"] is True
    assert fixture["map_chip"]["width"] == 14
    assert fixture["map_chip"]["height"] == 14
    assert fixture["runtime_policy"]["raw_overlay_is_diagnostic_only"] is True
    assert fixture["runtime_policy"]["raw_types_are_not_furniture_data_ids"] is True
    assert fixture["runtime_policy"]["native_wall_door_coordinate_composition_not_implied"] is True
    assert all(cell["instance_id"] is None for cell in fixture["raw_cells"])
    assert all(cell["identity_status"] == "raw_only_no_furniture_data_inference" for cell in fixture["raw_cells"])
    assert all(cell["render_status"] == "diagnostic_raw_overlay_only" for cell in fixture["raw_cells"])
    assert fixture["determinism"]["content_hash"]
    print("room_r_scene_fixture_test_passed room=room:17 raw_cells=100 door=8,3 native_bindings=0")


if __name__ == "__main__":
    main()
