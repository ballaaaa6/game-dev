"""Regression checks for the evidence-bounded Phase 3C render contract."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3c_render_contract as builder


ROOT = builder.ROOT


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def without_dynamic(value):
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    fixture, contract, validation = builder.build_package()
    stored_fixture = load(builder.FIXTURE_PATH)
    stored_contract = load(builder.CONTRACT_PATH)
    stored_validation = load(builder.VALIDATION_PATH)

    assert validation["status"] == "pass"
    assert validation["counts"] == {"checks": 12, "passed_checks": 12}
    assert validation["failed_checks"] == []
    assert contract["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert contract["canvas"] == {
        "width": 980,
        "height": 600,
        "presentation_origin": {"x": 240, "y": 260},
        "presentation_origin_status": "explicit_runtime_fixture",
    }
    assert [item["id"] for item in contract["draw_passes"]] == [
        "map-extension-floor",
        "map-chip",
        "object-chip-primary",
        "object-chip-wall",
        "avatar-primary",
        "avatar-secondary",
        "object-chip-late-preview",
        "object-chip-late",
        "map-floor",
    ]
    placements = {item["id"]: item for item in contract["placements"]}
    assert [f"{item['object_id']}@{item['cell'][0]}:{item['cell'][1]}" for item in contract["native_initial_bindings"]] == [
        "furniture:3@2:4",
        "furniture:3@3:4",
        "furniture:3@6:4",
        "furniture:12@8:5",
        "furniture:26@8:6",
        "furniture:56@2:7",
    ]
    assert placements["scene:room:0/floor"]["status"] == "approved_explicit_fallback"
    assert placements["scene:room:0/floor"]["raw_selector_id"] == 5
    assert placements["scene:room:0/floor"]["runtime_fallback"]["target_selector_id"] == 85
    assert placements["furniture:0"]["cell"] == [4, 2]
    assert placements["furniture:0"]["status"] == "approved_native_geometry_fixture"
    assert placements["furniture:1"]["cell"] == [8, 4]
    assert placements["furniture:1"]["status"] == "approved_native_door_coordinate"
    assert placements["furniture:2"]["cell"] is None
    assert placements["furniture:5"]["cell"] is None
    assert placements["scene:room:0/wall"]["status"] == "approved_native_coordinate_composition"
    assert placements["scene:room:0/wall"]["cell_scope"]["cells"]["vertical_frame_1"] == [[8, 1], [8, 2], [8, 3], [8, 5], [8, 6], [8, 7], [8, 8]]
    assert placements["scene:room:0/door"]["status"] == "approved_native_coordinate_composition"
    assert placements["scene:room:0/door"]["cell"] == [8, 4]
    assert without_dynamic(stored_fixture) == without_dynamic(fixture)
    assert without_dynamic(stored_contract) == without_dynamic(contract)
    assert without_dynamic(stored_validation) == without_dynamic(validation)
    print(
        "phase3c_render_contract_test_passed "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
