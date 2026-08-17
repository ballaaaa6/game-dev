"""Deterministic checks for the authoritative Phase 1D closure evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"


def load(name: str) -> dict:
    with (EVIDENCE / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    closure = load("phase1d_closure.json")
    validation = load("phase1d_closure_validation.json")
    passmap = load("phase1d_passmap_fixture.json")
    route = load("phase1d_route_fixture.json")
    asset = load("asset_selector_contract.json")
    staff = load("staff_semantics_contract.json")

    assert closure["status"] == "pass"
    assert closure["semantic_status"] == "closed_for_phase2_entry"
    assert closure["phase2_status"] == "not_started"
    assert validation["status"] == "pass"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"] == 18

    assert passmap["fixture_kind"].startswith("real_room_type4")
    assert passmap["scene_record"]["anchor"] == {"x": 4, "y": 2, "raw_map_value": 4}
    assert passmap["furniture_record"]["id"] == 0
    assert passmap["furniture_record"]["type"] == 4
    assert passmap["furniture_record"]["passMap_shape"] == [9, 9]
    assert len(passmap["native_placement"]["footprint"]) == 9
    assert passmap["isPassable"]["matrix"] == [[True, False, False], [True, False, False], [True, True, True]]
    assert all(item["isPassable"] for item in passmap["isPassable"]["synthetic_zero_probes"])
    assert passmap["isPassable"]["all_nonzero_probe"]["isPassable"] is False
    assert passmap["null_furniture_branch"]["status"] == "closed_for_fixture_scope"

    assert route["status"] == "pass"
    assert route["route"]["path"] == [[8, 4], [7, 4], [6, 4]]
    assert route["route"]["step_count"] == 2
    assert all(probe["path"] is None for probe in route["filter_probes"])
    assert route["goal_filter"]["public_postprocess_probes"]["equip_flag_on_type1"]["direction"] == 7
    assert {item["move_mode"]: item["astar_flag"] for item in route["goal_filter"]["staff_move_mode_mapping"]} == {
        "MOVE_MODE_GOTO_EQUIPMENT": 2,
        "MOVE_MODE_TO_STAFF": 4,
        "MOVE_MODE_GOTO_DESK": 1,
    }
    assert len(route["provenance"]["apk_sha256"]) == 64
    assert route["provenance"]["room_data"]["row_sha256"]

    assert asset["status"] == "pass"
    assert asset["unresolved"] == []
    assert all(item["locale_sets_match"] for item in asset["selector_contracts"].values())
    assert asset["selector_contracts"]["FurnitureData.seb_"]["rows_checked"] == 206
    assert asset["selector_contracts"]["FurnitureData.subSeb_"]["negative_value_count"] == 160
    assert asset["selector_contracts"]["StaffData.img_"]["used_ids"] == list(range(105))
    assert asset["selected_furniture"][0]["selectors"]["seb_"]["filename"] == "big_base00.seb"
    assert asset["selected_furniture"][2]["selectors"]["subSeb_"]["filename"] == "chair_00.seb"
    assert asset["selected_furniture"][3]["selectors"]["img_"]["filename"] == "desk_06.png"

    assert staff["status"] == "pass"
    assert staff["skill_reference"]["selected_staff_skill_ids"] == [1]
    assert staff["skill_reference"]["selected_staff_skill_ids_japanese"] == [1]
    assert staff["skill_reference"]["staff_skill_ids_locale_aligned"] is True
    assert staff["skill_reference"]["skill_core_locale_aligned"] is True
    assert staff["skill_reference"]["skill"]["effects_8"] == [150]
    assert staff["skill_reference"]["effect_contract"]["type_value"] == 10
    assert staff["skill_reference"]["effect_contract"]["flag_value"] == 1
    assert staff["route_mapping"]["entries"] == [
        {"move_mode": "MOVE_MODE_GOTO_EQUIPMENT", "move_mode_value": 1, "astar_flag": 2},
        {"move_mode": "MOVE_MODE_TO_STAFF", "move_mode_value": 7, "astar_flag": 4},
        {"move_mode": "MOVE_MODE_GOTO_DESK", "move_mode_value": 3, "astar_flag": 1},
    ]
    assert [item["typing"]["seb_id"] for item in staff["typing_animation"]["selector_pairs"]] == [23, 24, 25, 26]
    assert [item["wait"]["seb_id"] for item in staff["typing_animation"]["selector_pairs"]] == [10, 11, 12, 13]
    assert all(item["typing"]["asset"]["status"] == "resolved" for item in staff["typing_animation"]["selector_pairs"])
    assert all(item["wait"]["asset"]["status"] == "resolved" for item in staff["typing_animation"]["selector_pairs"])

    print(
        "phase1d_closure_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"route_steps={route['route']['step_count']} "
        f"furniture_rows={asset['scope']['furniture_rows']} "
        f"staff_rows={asset['scope']['staff_rows']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
