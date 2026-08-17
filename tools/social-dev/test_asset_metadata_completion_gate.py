"""Deterministic checks for the final asset metadata completion gate."""

from __future__ import annotations

import json

import build_asset_metadata_completion_gate as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    gate = load(builder.GATE_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert gate["schema_version"] == "social-dev-asset-metadata-completion-gate-v1"
    assert gate["status"] == "pass"
    assert gate["semantic_status"] == "asset_metadata_catalog_complete_with_runtime_subset_and_explicit_boundaries"
    assert gate["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    assert all(item["passed"] for item in gate["checks"])
    assert gate["counts"]["indexed_assets"] == 3542
    assert gate["counts"]["native_data_records"] == 3693
    assert gate["counts"]["native_selectors"] == 3192
    assert gate["counts"]["runtime_query_assets"] == 186
    assert gate["counts"]["unresolved_selector_identities"] == 1
    assert gate["counts"]["helper_scope_gaps"] == 9
    assert gate["counts"]["unity_textasset_apk_gaps"] == 34
    assert gate["counts"]["non_actor_families_without_screen_event_contract"] == 21
    assert gate["counts"]["runtime_geometry_gaps"] == 0
    assert contract["acceptance"]["all_checks_pass"] is True
    assert contract["acceptance"]["catalog_metadata_complete"] is True
    assert contract["acceptance"]["runtime_query_surface_explicit"] is True
    assert contract["acceptance"]["full_runtime_promotion_not_overclaimed"] is True

    print(f"asset_metadata_completion_gate_test_passed checks={len(gate['checks'])} assets={gate['counts']['indexed_assets']} runtime_query_assets={gate['counts']['runtime_query_assets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
