"""Deterministic checks for AM-3 selector and field semantics artifacts."""

from __future__ import annotations

import json

import build_asset_selector_usage_matrix as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    selector = load(builder.SELECTOR_MATRIX_PATH)
    fields = load(builder.FIELD_MATRIX_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt_selector, rebuilt_fields = builder.build_usage_and_fields()
    rebuilt_contract = builder.build_contract_payload(rebuilt_selector, rebuilt_fields)

    assert selector["schema_version"] == "social-dev-asset-selector-usage-matrix-v1"
    assert fields["schema_version"] == "social-dev-data-field-semantics-matrix-v1"
    assert selector["status"] == "pass"
    assert fields["status"] == "pass"
    assert selector["determinism"]["content_hash"] == rebuilt_selector["determinism"]["content_hash"]
    assert fields["determinism"]["content_hash"] == rebuilt_fields["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]

    assert selector["counts"]["selectors"] == 3192
    assert selector["counts"]["unresolved_selectors"] == 1
    assert selector["counts"]["selectors_with_data_relations"] == 267
    assert fields["counts"]["fields"] == 1063
    assert fields["counts"]["selector_bearing_fields"] == 8
    assert len(selector["selectors"]) == 3192
    assert len(fields["field_semantics"]) == 1063
    assert len(fields["selector_field_contracts"]) == 8

    selector_by_key = {item["selector_key"]: item for item in selector["selectors"]}
    assert selector_by_key["ref:chip:seb:1"]["data_relation_count"] > 0
    assert selector_by_key["ref:chip:seb:1"]["target_asset_id"] == "asset:01_GAME_PACKS/chip/desk_00.seb"
    assert selector_by_key["ref:chip:img:23"]["target_asset_id"] == "asset:01_GAME_PACKS/chip/floor_05.png"
    assert selector["selectors"][-1]["selector_call_contract"]

    fields_by_key = {item["field_key"]: item for item in fields["field_semantics"]}
    assert fields_by_key["FurnitureData.seb_"]["asset_disposition"] == "direct_selector"
    assert fields_by_key["FurnitureData.subSeb_"]["sentinel_value_count"] == 80
    assert fields_by_key["FurnitureData.img_"]["sentinel_value_count"] == 7
    assert fields_by_key["RoomData.floorImgId_"]["asset_disposition"] == "indirect_selector"
    assert fields_by_key["RoomData.objMap_"]["asset_disposition"] == "non_asset_control"
    assert fields_by_key["HelperData.img_"]["semantic_status"] == "closed_selector_field_contract"
    assert contract["acceptance"]["every_field_has_explicit_disposition"] is True
    assert contract["acceptance"]["sentinel_policy_is_preserved"] is True

    print(f"asset_selector_usage_matrix_test_passed selectors={selector['counts']['selectors']} fields={fields['counts']['fields']} selector_fields={fields['counts']['selector_bearing_fields']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
