"""Validate the loader-aware scene and behavior candidate package."""

from __future__ import annotations

import json

from build_scene_behavior_candidates import DEFAULT_OUTPUT, build_candidates


def main() -> int:
    scene, behavior, validation = build_candidates(DEFAULT_OUTPUT)
    if validation["status"] != "pass":
        raise AssertionError(f"validation failed: {validation['failed_checks']}")
    if scene["semantic_status"] != "pending_review" or behavior["semantic_status"] != "pending_review":
        raise AssertionError("candidate packages must remain pending_review")
    if scene["room"]["grid_shape"] != {
        "objMap_width": 10,
        "objMap_height": 10,
        "objDir_width": 10,
        "objDir_height": 10,
    }:
        raise AssertionError(f"unexpected room shape: {scene['room']['grid_shape']}")
    if scene["room"]["door_cells_by_code_candidate"]["cells"] != [
        {"x": 8, "y": 4, "raw_map_value": 5}
    ]:
        raise AssertionError("door candidate must remain tied to raw map code 5")
    if behavior["selection"]["job_ids"] != [4] or behavior["selection"]["skill_ids"] != [1]:
        raise AssertionError(f"unexpected derived links: {behavior['selection']}")
    if validation["counts"] != {
        "parsed_records": 22,
        "scene_source_slices": 13,
        "behavior_source_slices": 15,
        "transition_candidates": 7,
        "review_items": 8,
    }:
        raise AssertionError(f"unexpected counts: {validation['counts']}")
    route = next(item for item in behavior["transition_candidates"] if item["id"] == "move-route-dispatch")
    if route["mapping"]["MOVE_MODE_GOTO_EQUIPMENT"]["astar_flag"] != 2:
        raise AssertionError("equipment goal flag mapping changed")
    if route["mapping"]["MOVE_MODE_TO_STAFF"]["astar_flag"] != 4:
        raise AssertionError("staff goal flag mapping changed")
    if route["mapping"]["MOVE_MODE_GOTO_DESK"]["astar_flag"] != 1:
        raise AssertionError("desk goal flag mapping changed")

    for name in (
        "scene_data_candidate.json",
        "staff_behavior_candidate.json",
        "scene_behavior_validation.json",
    ):
        with (DEFAULT_OUTPUT / name).open("r", encoding="utf-8") as handle:
            json.load(handle)

    print(
        "scene_behavior_test_passed "
        f"records={validation['counts']['parsed_records']} "
        f"room=10x10 "
        f"transitions={validation['counts']['transition_candidates']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
