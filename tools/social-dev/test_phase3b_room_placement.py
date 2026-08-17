"""Deterministic regression checks for the Phase 3B room-placement package."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3b_room_placement as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    audit_path = EVIDENCE / "phase3b_room_placement_source_audit.json"
    fixture_path = EVIDENCE / "phase3b_room_placement_fixture.json"
    validation_path = EVIDENCE / "phase3b_room_placement_validation.json"
    contract_path = RUNTIME_EVIDENCE / "room_placement_contract.json"
    audit = load(audit_path)
    fixture = load(fixture_path)
    validation = load(validation_path)
    contract = load(contract_path)
    rebuilt_audit, rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert audit["schema_version"] == "social-dev-phase3b-room-placement-source-audit-v1"
    assert fixture["schema_version"] == "social-dev-phase3b-room-placement-fixture-v1"
    assert validation["schema_version"] == "social-dev-phase3b-room-placement-validation-v1"
    assert contract["schema_version"] == "social-dev-phase3b-room-placement-v1"
    assert audit["status"] == fixture["status"] == validation["status"] == contract["status"] == "pass"
    assert audit["semantic_status"] == "closed_for_phase3b_with_explicit_unresolved_selector"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"] == 20

    assert contract["scene_ref"]["id"] == "room:0"
    assert contract["selectors"]["floor"]["raw_selector_id"] == 5
    assert contract["selectors"]["floor"]["resolution_status"] == "unresolved"
    assert contract["selectors"]["floor"]["reason_code"] == "missing_img_inf_entry"
    assert contract["selectors"]["floor"]["asset"] is None
    assert contract["selectors"]["floor"]["runtime_resolution_status"] == "explicit_fallback"
    assert contract["selectors"]["floor"]["runtime_fallback"] == {
        "target_selector_id": 85,
        "filename": "floor_09.png",
        "resolution_status": "resolved",
        "resolution_mode": "explicit_user_approved_alias",
        "reason_code": "user_approved_runtime_alias",
        "decision": "The unresolved raw floor selector 5 uses floor_09.png as an explicit runtime alias; source mapping remains unresolved.",
        "asset": contract["selectors"]["floor"]["runtime_fallback"]["asset"],
    }
    assert contract["selectors"]["floor"]["runtime_fallback"]["asset"]["sha256"] == "cc960abb36b882bc771837a82c20563c11399456f21aa08ff87a033d2b543184"
    assert contract["selectors"]["wall"]["filename"] == "wall_00.png"
    assert contract["selectors"]["wall"]["asset"]["sha256"] == "cbd7c73a38d041cafc330471cbab58b081c9c1c5ca4826e39e7f44d0a282d06c"
    assert contract["selectors"]["door"]["filename"] == "door_01.png"
    assert contract["selectors"]["door"]["asset"]["sha256"] == "196198c9ee093f7f234060868434f9547e56bd020e57acebf4b2285848281569"

    placement = contract["native_placement"]
    assert placement["init_order"] == [
        "Room.InitMapChips",
        "Room.InitObjChips",
        "Room.SetupBigChipsParent",
        "Room.PlaceDoor",
    ]
    assert placement["door"]["cell"] == {"x": 8, "y": 4, "raw_map_value": 5, "raw_dir_value": 0}
    assert placement["door"]["installed_flag"] == 1
    assert placement["door"]["place_obj_furniture_data"] is None
    assert placement["type4"]["anchor"] == {"x": 4, "y": 2, "raw_map_value": 4}
    assert len(placement["type4"]["footprint"]) == 9
    assert placement["type4"]["passability"]["matrix"] == [[True, False, False], [True, False, False], [True, True, True]]
    assert placement["route_fixture"]["path"] == [[8, 4], [7, 4], [6, 4]]

    bindings = {item["object_id"]: item for item in contract["object_boundary"]["native_room_bindings"]}
    assert bindings["furniture:0"]["status"] == "verified_native_fixture"
    assert bindings["furniture:1"]["status"] == "selector_candidate_not_native_binding"
    assert bindings["furniture:5"]["status"] == "approved_selector_not_placed_in_room0"
    assert bindings["furniture:2"]["status"] == "approved_selector_not_placed_in_room0"
    assert contract["object_boundary"]["runtime_policy"]["promote_furniture_2"] is True

    coordinates = contract["coordinates"]
    assert coordinates["cell_origin"]["probes"][2] == {"cell": [8, 4], "world": {"x": 260, "y": -22}}
    assert coordinates["actor_spawn"]["probes"][0] == {"cell": [8, 4], "world": {"x": 280, "y": -31}}
    assert coordinates["map_chip_draw_origin"]["probes"][0] == {"cell": [8, 4], "origin": {"x": 480, "y": -80}}
    assert coordinates["object_draw_origin"]["probes"][0] == {"cell": [8, 4], "origin": {"x": 240, "y": -31}}
    assert coordinates["camera"]["fixture_offset"] == [0, 0]

    draw_passes = contract["draw_order"]["passes"]
    assert [item["line"] for item in draw_passes] == sorted(item["line"] for item in draw_passes)
    assert contract["draw_order"]["overlap_fixture"]["expected_event_order"] == ["door-object", "floor-image"]

    assert all(item["hash_status"] == "pass" for item in audit["source_slices"])
    assert contract["runtime_policy"] == {
        "source_code_imports": False,
        "archive_imports": False,
        "unapproved_binary_imports": False,
        "unresolved_selector_policy": "retain raw selector and use the explicit per-selector runtime fallback while preserving the source gap",
        "phase3b_asset_promotion": "explicit floor fallback only; source selector resolution remains evidence-only",
        "quarantined_objects_excluded": [],
    }

    assert builder.without_dynamic(audit) == builder.without_dynamic(rebuilt_audit)
    assert builder.without_dynamic(fixture) == builder.without_dynamic(rebuilt_fixture)
    assert builder.without_dynamic(contract) == builder.without_dynamic(rebuilt_contract)
    assert builder.without_dynamic(validation) == builder.without_dynamic(rebuilt_validation)
    assert not list((ROOT / "runtime/social-dev").rglob("*.cs"))

    print(
        "phase3b_room_placement_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"contract_hash={contract['determinism']['contract_hash']} "
        f"floor={contract['selectors']['floor']['resolution_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
