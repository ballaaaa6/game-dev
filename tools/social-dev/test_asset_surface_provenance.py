"""Deterministic checks for the Track X/A surface provenance package."""

from __future__ import annotations

import json

import build_asset_surface_provenance as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    surface = load(builder.SURFACE_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert surface["schema_version"] == "social-dev-asset-surface-provenance-v1"
    assert surface["status"] == "pass"
    assert surface["semantic_status"] == "surface_provenance_boundary_closed_with_explicit_runtime_promotion_gates"
    assert surface["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]

    counts = surface["counts"]
    assert counts["indexed_assets"] == 3542
    assert counts["families"] == 27
    assert counts["non_actor_families"] == 21
    assert counts["zip_exact_assets"] == 3542
    assert counts["apk_entry_present_assets"] == 3508
    assert counts["apk_entry_missing_assets"] == 34
    assert counts["pack_roundtrip_exact_rows"] == 25
    assert counts["unity_textasset_assets"] == 34
    assert counts["unity_textasset_apk_missing_assets"] == 34
    assert counts["unresolved_selectors"] == 1
    assert len(surface["families"]) == 27
    assert len({row["family_id"] for row in surface["families"]}) == 27
    assert len([row for row in surface["families"] if row["non_actor_surface"]]) == 21
    assert all(row["boundary_status"] for row in surface["families"])
    assert all(row["runtime_policy"] == "do_not_promote_without_screen_or_event_consumer_contract" for row in surface["families"] if row["non_actor_surface"])

    gap = surface["source_provenance"]["unity_textasset_boundary"]
    assert gap["asset_count"] == 34
    assert gap["apk_entry_missing_count"] == 34
    assert gap["status"] == "source_hash_or_nested_unity_mapping_not_closed"
    assert surface["source_provenance"]["selector_identity_boundary"]["rows"][0]["raw_line"] == "bg.seb"
    assert all(surface["closure"].values())
    assert contract["acceptance"]["all_non_actor_families_have_explicit_boundary"] is True
    assert contract["runtime_policy"]["screen_event_usage_inference"] is False

    print(f"asset_surface_provenance_test_passed assets={counts['indexed_assets']} non_actor_families={counts['non_actor_families']} apk_missing={counts['apk_entry_missing_assets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
