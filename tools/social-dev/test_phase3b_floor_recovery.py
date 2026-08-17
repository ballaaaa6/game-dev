"""Deterministic regression checks for the Phase 3B floor recovery gate."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3b_floor_recovery as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    audit_path = EVIDENCE / "phase3b_floor_recovery_source_audit.json"
    fixture_path = EVIDENCE / "phase3b_floor_recovery_fixture.json"
    validation_path = EVIDENCE / "phase3b_floor_recovery_validation.json"
    audit = load(audit_path)
    fixture = load(fixture_path)
    validation = load(validation_path)
    rebuilt_audit, rebuilt_fixture, rebuilt_validation, rebuilt_report = builder.build_package()

    assert audit["schema_version"] == "social-dev-phase3b-floor-recovery-source-audit-v1"
    assert fixture["schema_version"] == "social-dev-phase3b-floor-recovery-fixture-v1"
    assert validation["schema_version"] == "social-dev-phase3b-floor-recovery-validation-v1"
    assert audit["status"] == fixture["status"] == validation["status"] == "pass"
    assert audit["semantic_status"] == "source_limited_unresolved_recovery_complete"
    assert fixture["semantic_status"] == audit["semantic_status"]
    assert validation["semantic_status"] == "recovery_gate_pass_source_limited_unresolved"
    assert validation["summary"]["failed"] == 0
    assert validation["summary"]["passed"] == validation["summary"]["total"] == 22

    assert audit["raw_selector"] == {
        "scene_id": "room:0",
        "field": "floorImgId_",
        "value": 5,
        "scene_contract_ref": audit["raw_selector"]["scene_contract_ref"],
    }
    selector_probe = fixture["selector_probe"]
    assert selector_probe["selector_id"] == 5
    assert selector_probe["img_inf_filename_zip"] is None
    assert selector_probe["img_inf_filename_apk"] is None
    assert selector_probe["asset_selector_contract_filename"] is None
    assert selector_probe["resolution_status"] == "unresolved"

    zip_img = audit["zip_pack"]["img_inf"]
    apk_img = audit["apk_pack"]["img_inf"]
    assert zip_img["sha256"] == "5f37934c43bc86c3139d7415f1ae2c9315b4aef7bc81746b95db558a077e5310"
    assert apk_img["sha256"] == zip_img["sha256"]
    assert zip_img["entries"].get("5") is None
    assert apk_img["entries"].get("5") is None
    assert audit["selector_cross_check"]["zip_and_apk_img_inf_byte_equal"] is True
    assert audit["selector_cross_check"]["zip_and_apk_seb_inf_byte_equal"] is True
    assert [item["filename"] for item in audit["selector_cross_check"]["floor_image_records_in_img_inf"]] == [
        "floor_00.png",
        "floor_01.png",
        "floor_02.png",
        "floor_03.png",
        "floor_04.png",
        "floor_05.png",
        "floor_06.png",
        "floor_07.png",
        "floor_08.png",
        "floor_09.png",
        "floor_10.png",
    ]
    floor_05 = next(item for item in audit["selector_cross_check"]["floor_05_asset_index_rows"] if item["original_name"] == "floor_05.png")
    assert floor_05["kind"] == "original_pack_asset"
    assert floor_05["sha256"] == "be6572af9df60f5ed00eb0ab0e7d4dd95ba08749d7ec88b027a8ae5b3896c08c"
    assert audit["apk_pack"]["scan"]["match_count"] == 1
    assert audit["apk_pack"]["scan"]["scanned_count"] == 1147
    assert audit["apk_pack"]["pack_header"]["file_count"] == 333
    assert audit["apk_pack"]["key"]["key_hash_matches_dump_field"] is True

    native = audit["native_trace"]
    assert native["negative_sentinel"]["is_negative"] is False
    assert native["fallback_or_alias"]["status"] == "not_proven"
    assert [item["step"] for item in native["selector_flow"]] == [
        "RoomData load",
        "Room.InitMapChips",
        "MapChip storage and draw",
        "ResourceManager pack load",
        "List parsing",
    ]
    assert audit["source_search"]["source_labeled_image_constant_id_5"] == []

    versions = {item["label"]: item for item in audit["version_and_provenance"]["available_candidates"]}
    assert versions["2.4.9"]["status"] == "missing_in_workspace"
    assert versions["2.5.0"]["status"] == "missing_in_workspace"
    assert versions["2.5.1_current"]["status"] == "matching_current_chip_boundary"
    assert versions["archive_game_dev_story_mod"]["status"] == "removed_with_legacy_archive"
    assert versions["archive_game_dev_story_mod"]["exists"] is False
    assert versions["archive_game_dev_story_mod"]["chip_scan"]["match_count"] == 0

    final = audit["final_classification"]
    assert final == {
        "classification": "source_limited_unresolved",
        "status": "recovery_complete",
        "data_availability": "id_5_mapping_absent_from_supplied_current_chip_pack",
        "extraction_loss_proven": False,
        "authoritative_filename": None,
        "authoritative_asset": None,
        "intentional_reservation_proven": False,
        "runtime_action": "retain raw selector 5; use explicit runtime alias 5 -> 85 -> floor_09.png; source mapping remains unresolved",
        "phase3b_closure": "closed_as_source_limit_with_explicit_runtime_fallback",
    }
    assert audit["runtime_decision"]["fallback"]["target_selector_id"] == 85
    assert audit["runtime_decision"]["fallback"]["filename"] == "floor_09.png"
    assert audit["runtime_decision"]["fallback"]["resolution_mode"] == "explicit_user_approved_alias"
    assert validation["summary"]["runtime_contract_changed"] is False
    contract = load(ROOT / "knowledge/fixtures/accepted/runtime/room_placement_contract.json")
    assert audit["baseline"]["contract_hash"] == contract["determinism"]["contract_hash"]
    assert all(item["hash_status"] == "pass" for item in audit["source_slices"])

    assert builder.without_dynamic(audit) == builder.without_dynamic(rebuilt_audit)
    assert builder.without_dynamic(fixture) == builder.without_dynamic(rebuilt_fixture)
    assert builder.without_dynamic(validation) == builder.without_dynamic(rebuilt_validation)
    assert "source_limited_unresolved" in rebuilt_report
    assert not list((ROOT / "runtime/social-dev").rglob("*.cs"))

    print(
        "phase3b_floor_recovery_test_passed "
        f"checks={validation['summary']['passed']} "
        f"classification={final['classification']} "
        f"img_inf_sha256={zip_img['sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
