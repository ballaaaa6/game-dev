"""Validate the runtime-facing native content catalog."""

from __future__ import annotations

import json
from pathlib import Path

import build_native_content_catalog as builder


ROOT = builder.ROOT
CATALOG_PATH = ROOT / "knowledge/fixtures/accepted/runtime/native_content_catalog.json"


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    rebuilt = builder.build_payload()
    assert catalog["status"] == "pass"
    assert catalog["semantic_status"] == "approved_for_runtime_catalog"
    assert catalog["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert catalog["source_registry"]["content_hash"]
    counts = catalog["counts"]
    assert counts == {
        "data_manager_arrays": 43,
        "data_types": 43,
        "data_records": 3693,
        "assets": 3542,
        "selectors": 3192,
        "data_selector_connections": 523,
        "selector_asset_and_companion_connections": 4596,
        "consumer_connections": 250,
        "lifecycle_connections": 43,
    }

    data_records = catalog["data_records"]
    assert len({record["record_id"] for record in data_records}) == 3693
    furniture = [record for record in data_records if record["data_type"] == "FurnitureData"]
    assert len(furniture) == 103
    furniture_by_id = {record["native_id"]: record for record in furniture}
    assert furniture_by_id[3]["decoded"]["fields"]["name_"] == "Wooden Desk"
    assert furniture_by_id[3]["decoded"]["fields"]["seb_"] == 1
    assert furniture_by_id[12]["decoded"]["fields"]["img_"] == 109
    assert furniture_by_id[12]["locale_rows"]["English.lproj"]["raw_row_sha256"]

    assets = catalog["assets"]
    selectors = catalog["selectors"]
    assert len({asset["asset_id"] for asset in assets}) == 3542
    assert len({selector["selector_key"] for selector in selectors}) == 3192
    assets_by_id = {asset["asset_id"]: asset for asset in assets}
    selector_by_key = {selector["selector_key"]: selector for selector in selectors}
    assert assets_by_id["asset:01_GAME_PACKS/chip/floor_05.png"]["sha256"]
    assert selector_by_key["ref:chip:img:23"]["target_filename"] == "floor_05.png"

    data_edges = catalog["connections"]["data_selector"]
    assert any(
        edge["from"] == "data:furniture:3"
        and edge["field"] == "seb_"
        and edge["to"] == "ref:chip:seb:1"
        and edge["target_asset_id"] in assets_by_id
        for edge in data_edges
    )
    assert any(
        edge["from"] == "data:room:17"
        and edge["field"] == "doorImgId_"
        and edge["to"] == "ref:chip:img:93"
        for edge in data_edges
    )
    assert all(
        edge.get("target_asset_id") is None or edge.get("target_asset_id") in assets_by_id
        for edge in data_edges
    )
    assert any(
        edge["from"] == "field:floorImgId_" and edge["to"] == "consumer:Room.InitMapChips"
        for edge in catalog["connections"]["consumer"]
    )
    assert any(
        edge["from"] == "registry:data_manager:furnitureData_" and edge["to"] == "consumer:AppData.NewGame"
        for edge in catalog["connections"]["consumer"]
    )

    print(
        "native_content_catalog_test_passed "
        f"records={counts['data_records']} assets={counts['assets']} selectors={counts['selectors']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
