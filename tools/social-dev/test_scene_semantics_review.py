"""Contract checks for Phase 1C scene-semantics evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"


def load(name: str) -> dict:
    with (EVIDENCE / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    review = load("scene_semantics_review.json")
    validation = load("scene_semantics_validation.json")

    assert validation["status"] == "pass"
    assert validation["semantic_status"] == "pending_review"
    assert validation["failed_checks"] == []
    assert validation["counts"]["source_slices"] == 12
    assert validation["counts"]["observations"] == 9
    assert validation["counts"]["furniture_ids"] == 103
    assert validation["counts"]["non_empty_pass_map_records"] == 13
    assert validation["counts"]["route_goal_candidates"] == 6

    scene = review["scene"]
    assert scene["grid_shape"] == {
        "objMap_width": 10,
        "objMap_height": 10,
        "objDir_width": 10,
        "objDir_height": 10,
    }
    assert scene["raw_map_domain"] == [0, 1, 2, 3, 4, 5, 6]
    assert scene["door_cells_by_raw_code"] == [{"x": 8, "y": 4, "raw_map_value": 5}]
    assert review["route"]["status"] == "blocked_on_fixture_semantics"
    assert review["route"]["node_grid_candidate"]["node_count_candidate"] == 100
    assert review["route"]["neighbor_policy_candidate"]["connectivity"] == 4
    assert review["furniture_pass_map_inventory"]["selected_profiles"]
    assert all(
        profile["passMap_non_empty"] is False
        for profile in review["furniture_pass_map_inventory"]["selected_profiles"]
    )
    assert any(item["id"] == "manhattan-cost" and item["status"] == "source_observed" for item in review["observations"])
    assert any(item["id"] == "passability-gate" and item["status"] == "native_observed_bounded" for item in review["observations"])
    assert any(item["id"] == "room-grid-shape" and item["status"] == "native_observed" for item in review["observations"])
    assert any(item["id"] == "neighbor-topology" and item["status"] == "native_observed" for item in review["observations"])
    assert any(item["id"] == "objmap-assignment-gap" and item["status"] == "closed" and not item["blocking"] for item in review["review_items"])
    assert any(item["id"] == "neighbor-policy" and item["status"] == "closed" and not item["blocking"] for item in review["review_items"])
    assert len(review["review_items"]) == 6
    print(
        "scene_semantics_test_passed "
        f"grid={scene['grid_shape']['objMap_width']}x{scene['grid_shape']['objMap_height']} "
        f"furniture={validation['counts']['furniture_ids']} "
        f"non_empty_pass_map={validation['counts']['non_empty_pass_map_records']} "
        f"route={review['route']['status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
