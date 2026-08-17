"""Regression checks for the strict Phase 3C native closure package."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3c_strict_closure as builder


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    package, runtime_contract, validation = builder.build_package()
    stored_package = load(builder.OUTPUT_PATH)
    stored_runtime = load(builder.RUNTIME_OUTPUT_PATH)
    stored_validation = load(builder.VALIDATION_PATH)

    assert validation["status"] == "pass"
    assert validation["counts"] == {"checks": 10, "passed_checks": 10}
    assert validation["failed_checks"] == []
    assert package["status"] == "pass"
    assert package["semantic_status"] == "strict_evidence_closed_baseline_pending_approval"
    assert runtime_contract["status"] == "pass"
    assert runtime_contract["semantic_status"] == "approved_for_runtime_contract"

    assert package["scene_ref"]["door_cell"] == [8, 4]
    assert package["wall"]["cells_by_frame"] == {
        "vertical_frame_1": [[8, 1], [8, 2], [8, 3], [8, 5], [8, 6], [8, 7], [8, 8]],
        "horizontal_frame_0": [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]],
    }
    assert package["wall"]["sprite_records"]["vertical_frame_1"]["source_x"] == 72
    assert package["wall"]["sprite_records"]["horizontal_frame_0"]["source_x"] == 48
    assert [record["layer"] for record in package["wall"]["sprite_layers"]["vertical_frame_1"]] == [0, 1]
    assert [record["layer"] for record in package["wall"]["sprite_layers"]["horizontal_frame_0"]] == [0, 1]
    assert package["wall"]["sprite_layers"]["vertical_frame_1"][1]["source_x"] == 90
    assert package["wall"]["sprite_layers"]["vertical_frame_1"][1]["width"] == 2
    assert package["wall"]["sprite_layers"]["horizontal_frame_0"][1]["source_x"] == 52
    assert package["wall"]["sprite_layers"]["horizontal_frame_0"][1]["width"] == 2
    assert package["door"]["sprite_record"] == {
        "start_frame": 0,
        "image_id": 7,
        "source_x": 0,
        "source_y": 0,
        "width": 13,
        "height": 31,
        "destination_x": 0,
        "destination_y": -24,
        "flags": 0,
        "reserved": 0,
    }

    assert [item["furniture_data_id"] for item in package["native_initial_bindings"]] == [3, 3, 3, 12, 26, 56]
    assert [item["cell"] for item in package["native_initial_bindings"]] == [
        [2, 4],
        [3, 4],
        [6, 4],
        [8, 5],
        [8, 6],
        [2, 7],
    ]
    selected = {item["object_id"]: item for item in package["selected_display_binding_matrix"]}
    assert selected["furniture:2"]["native_status"] == "selector_defined_not_bound_in_room0_initial_path"
    assert selected["furniture:5"]["native_status"] == "selector_defined_not_bound_in_room0_initial_path"
    assert selected["furniture:1"]["cells"] == [[8, 4]]
    assert package["type4_geometry"]["anchors"] == [[4, 2], [7, 2]]

    assert package["closure_conclusion"]["missing_data_found"] is False
    assert package["baseline_policy"]["historical_baseline_preserved"] is True
    assert package["baseline_policy"]["replacement_persisted"] is False
    assert package["baseline_policy"]["comparison_policy_status"] == "pending_user_approval"

    def without_dynamic(value):
        return builder.without_dynamic(value)

    assert without_dynamic(stored_package) == without_dynamic(package)
    assert without_dynamic(stored_runtime) == without_dynamic(runtime_contract)
    assert without_dynamic(stored_validation) == without_dynamic(validation)

    print(
        "phase3c_strict_closure_test_passed "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"initial_bindings={len(package['native_initial_bindings'])} "
        f"baseline={package['baseline_policy']['comparison_policy_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
