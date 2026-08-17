"""Deterministic checks for Track W furniture/world metadata."""

from __future__ import annotations

import json

import build_furniture_asset_metadata as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    catalog = load(builder.CATALOG_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert catalog["schema_version"] == "social-dev-furniture-asset-metadata-v1"
    assert catalog["status"] == "pass"
    assert catalog["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    assert catalog["counts"]["furniture_records"] == 103
    assert catalog["counts"]["rooms"] == 18
    assert catalog["counts"]["rooms_with_native_bindings"] == 1
    assert catalog["counts"]["native_binding_instances"] == 6
    assert catalog["counts"]["selector_statuses"]["seb_:resolved"] == 103
    assert catalog["counts"]["selector_statuses"]["subSeb_:resolved"] == 23
    assert catalog["counts"]["selector_statuses"]["subSeb_:absent_by_sentinel"] == 80
    assert catalog["counts"]["selector_statuses"]["img_:resolved"] == 96
    assert catalog["counts"]["selector_statuses"]["img_:absent_by_sentinel"] == 7
    assert len(catalog["furniture"]) == 103
    assert len({item["furniture_data_id"] for item in catalog["furniture"]}) == 103
    assert catalog["native_binding_ids"] == [3, 12, 26, 56]

    furniture = {item["furniture_data_id"]: item for item in catalog["furniture"]}
    assert furniture[0]["runtime_lookup_key"] == "data:furniture:0"
    assert furniture[0]["selector_fields"]["seb_"]["selector_key"] == "ref:chip:seb:11"
    assert furniture[0]["selector_fields"]["img_"]["status"] == "absent_by_sentinel"
    assert furniture[3]["native_binding_instance_count"] == 3
    assert furniture[12]["native_binding_instance_count"] == 1
    assert furniture[26]["native_binding_instance_count"] == 1
    assert furniture[56]["native_binding_instance_count"] == 1
    assert furniture[1]["placement_status"] == "not_bound_to_native_room_fixture"
    assert contract["acceptance"]["all_furniture_rows_decoded"] is True
    assert contract["acceptance"]["objchip_to_furniture_inference_disabled"] is True

    print(f"furniture_asset_metadata_test_passed furniture={catalog['counts']['furniture_records']} rooms={catalog['counts']['rooms']} bindings={catalog['counts']['native_binding_instances']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
