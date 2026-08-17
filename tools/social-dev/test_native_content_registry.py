"""Deterministic checks for the native Social Dev content registry and graph."""

from __future__ import annotations

import json
from pathlib import Path

import build_native_content_registry as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    registry_path = EVIDENCE / "native_content_registry.json"
    graph_path = EVIDENCE / "native_content_connection_graph.json"
    contract_path = RUNTIME_EVIDENCE / "native_content_registry_contract.json"
    graph_contract_path = RUNTIME_EVIDENCE / "native_content_connection_contract.json"

    registry = load(registry_path)
    graph = load(graph_path)
    contract = load(contract_path)
    graph_contract = load(graph_contract_path)
    rebuilt = builder.build_payload()

    assert registry["schema_version"] == "social-dev-native-content-registry-v1"
    assert registry["status"] == "pass"
    assert registry["semantic_status"] == "evidence_registry_not_runtime_approved"
    assert registry["content_hash"] == rebuilt["content_hash"]
    assert contract["registry_content_hash"] == registry["content_hash"]
    assert contract["status"] == "pass"

    counts = registry["counts"]
    assert counts["data_manager_arrays"] == 43
    assert counts["data_types"] == 43
    assert counts["data_rows"] == 3693
    assert counts["assets"] == 3542
    assert counts["selectors"] == 3192
    assert counts["data_selector_relations"] > 0
    assert counts["consumer_edges"] == 250
    assert counts["lifecycle_edges"] > 0

    validation = registry["identity_validation"]
    assert validation["duplicate_asset_ids"] == []
    assert validation["duplicate_selector_keys"] == []
    assert validation["missing_archive_member_count"] == 0
    assert validation["unresolved_selector_count"] == 1
    assert validation["unresolved_selector_samples"][0]["raw_line"] == "bg.seb"

    data_types = {item["source_type"]: item for item in registry["data_types"]}
    assert data_types["RoomData"]["row_count"] == 18
    assert data_types["FurnitureData"]["row_count"] == 103
    assert data_types["StaffData"]["row_count"] == 141
    assert data_types["RoomData"]["rows"][17]["catalog_key"] == "data:room:17"
    assert data_types["RoomData"]["rows"][17]["decoded"]["status"] == "verified_reader_order"
    assert data_types["FurnitureData"]["rows"][3]["catalog_key"] == "data:furniture:3"
    assert data_types["FurnitureData"]["rows"][3]["decoded"]["status"] == "verified_reader_order"

    floor_table = registry["native_indirection_tables"]["Room.FLOOR_IMAGE_ID_ARRAY"]
    assert floor_table["values"] == [0, 19, 20, 21, 22, 23, 82, 83, 84, 85, 95]
    assert floor_table["source_status"] == "verified_native_static_array_contract"

    assets = {item["asset_id"]: item for item in registry["assets"]}
    assert assets["asset:01_GAME_PACKS/chip/desk_00.png"]["archive_member_present"] is True
    assert assets["asset:01_GAME_PACKS/chip/desk_00.png"]["sha256"]
    assert assets["asset:02_DERIVED_READY_IMAGES/opt_reconstructed/chip/desk_00.logical.png"]["source_status"] == "derived_or_catalog"

    selectors = {
        (item["resource_scope"], item["selector_kind"], item["selector_id"]): item
        for item in registry["selectors"]
    }
    assert selectors[("chip", "img", 23)]["target_filename"] == "floor_05.png"
    assert selectors[("chip", "seb", 1)]["target_filename"] == "desk_00.seb"
    assert selectors[("chip", "img", 3)]["target_filename"] == "desk_00.png"
    assert selectors[("com/English.lproj", "img", 5)]["resolution_mode"] == "locale_fallback"

    data_edges = registry["data_selector_relations"]
    assert any(
        edge["from"] == "data:furniture:3"
        and edge["field"] == "seb_"
        and edge["to"] == "ref:chip:seb:1"
        and edge["status"] == "resolved"
        for edge in data_edges
    )
    assert any(
        edge["from"] == "data:room:17"
        and edge["field"] == "doorImgId_"
        and edge["to"] == "ref:chip:img:93"
        for edge in data_edges
    )
    assert any(
        edge["from"] == "data:room:0"
        and edge["field"] == "floorImgId_"
        and edge["relation"] == "data_field_indirect_selector"
        and edge["native_value"] == 5
        and edge["native_selector_id"] == 23
        and edge["to"] == "ref:chip:img:23"
        and edge["status"] == "resolved"
        for edge in data_edges
    )
    assert any(
        edge["from"] == "data:room:17"
        and edge["field"] == "floorImgId_"
        and edge["native_value"] == 9
        and edge["native_selector_id"] == 85
        and edge["to"] == "ref:chip:img:85"
        and edge["status"] == "resolved"
        for edge in data_edges
    )

    consumer_edges = registry["consumer_graph"]["consumer_edges"]
    assert any(
        edge["from"] == "field:seb_" and edge["to"] == "consumer:ObjChip.Draw"
        for edge in consumer_edges
    )
    assert any(
        edge["from"] == "field:wallImgId_" and edge["to"] == "consumer:MapChip.DrawExtentionFloor"
        for edge in consumer_edges
    )
    assert any(
        edge["from"] == "registry:data_manager:furnitureData_" and edge["to"] == "consumer:AppData.NewGame"
        for edge in consumer_edges
    )

    assert graph["schema_version"] == "social-dev-native-content-connection-graph-v1"
    assert graph["registry_content_hash"] == registry["content_hash"]
    assert graph["content_hash"] == graph_contract["graph_content_hash"]
    assert graph_contract["registry_content_hash"] == registry["content_hash"]
    assert len(graph["nodes"]["data_records"]) == counts["data_rows"]
    assert len(graph["nodes"]["assets"]) == counts["assets"]
    assert len(graph["edges"]["consumer"]) == counts["consumer_edges"]

    print(
        "native_content_registry_test_passed "
        f"data_rows={counts['data_rows']} "
        f"assets={counts['assets']} "
        f"selectors={counts['selectors']} "
        f"consumer_edges={counts['consumer_edges']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
