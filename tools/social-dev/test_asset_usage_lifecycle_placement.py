"""Deterministic checks for AM-5 usage/lifecycle/placement metadata."""

from __future__ import annotations

import json

import build_asset_usage_lifecycle_placement as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    matrix = load(builder.MATRIX_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert matrix["schema_version"] == "social-dev-asset-usage-lifecycle-placement-v1"
    assert matrix["status"] == "pass"
    assert matrix["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    counts = matrix["counts"]
    assert counts["assets"] == 3542
    assert counts["lifecycle_edges"] == 43
    assert counts["families"] == 27
    assert counts["non_actor_families"] > 0
    assert len(matrix["assets"]) == 3542
    assert all(item["usage_status"] and item["lifecycle_status"] and item["placement_status"] and item["runtime_query_status"] for item in matrix["assets"])
    assert counts["runtime_query_statuses"]["queryable_by_runtime_manifest_and_asset_id"] == 182
    assert matrix["source_provenance"]["unity_textasset_provenance"]["apk_entry_missing"] == 34
    assert contract["acceptance"]["every_asset_has_usage_status"] is True
    assert contract["acceptance"]["every_asset_has_lifecycle_status"] is True
    assert contract["acceptance"]["every_asset_has_placement_status"] is True
    assert contract["acceptance"]["apk_unity_provenance_gap_is_explicit"] is True

    by_id = {item["asset_id"]: item for item in matrix["assets"]}
    assert "selector_target" in by_id["asset:01_GAME_PACKS/chip/desk_00.seb"]["usage_channels"]
    assert by_id["asset:01_GAME_PACKS/chip/desk_00.seb"]["lifecycle_phases"]
    assert by_id["asset:01_GAME_PACKS/human/chara86.png"]["placement_status"] == "explicit_binding"
    assert by_id["asset:01_GAME_PACKS/avatar_body/m_00.png"]["runtime_query_status"] == "queryable_by_native_selector_and_asset_id"
    assert by_id["asset:01_GAME_PACKS/com/add_alpha.png"]["usage_status"] in {"selector_referenced_catalog_only", "cataloged_without_current_usage_edge", "runtime_manifest_referenced"}

    print(f"asset_usage_lifecycle_placement_test_passed assets={counts['assets']} usage_edges={counts['usage_edges']} non_actor_families={counts['non_actor_families']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
