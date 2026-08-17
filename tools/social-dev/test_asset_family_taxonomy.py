"""Deterministic checks for the AM-2 asset-family taxonomy."""

from __future__ import annotations

import json

import build_asset_family_taxonomy as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    taxonomy = load(builder.TAXONOMY_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert taxonomy["schema_version"] == "social-dev-asset-family-taxonomy-v1"
    assert taxonomy["status"] == "pass"
    assert taxonomy["semantic_status"] == "structural_taxonomy_not_runtime_approval"
    assert taxonomy["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]

    counts = taxonomy["counts"]
    assert counts["assets"] == 3542
    assert counts["families"] == 27
    assert counts["taxonomy_statuses"]["classified_structural_family"] == 3542
    assert sum(counts["lineages"].values()) == 3542
    assert len(taxonomy["assets"]) == 3542
    assert len({row["asset_id"] for row in taxonomy["assets"]}) == 3542
    assert all(row["family_id"] and row["subfamily_id"] and row["lineage"] for row in taxonomy["assets"])
    assert contract["acceptance"]["every_asset_has_family"] is True
    assert contract["acceptance"]["every_asset_has_subfamily"] is True
    assert contract["acceptance"]["every_asset_has_lineage"] is True
    assert contract["acceptance"]["unknown_taxonomy_rows"] == 0

    families = {item["family_id"] for item in taxonomy["families"]}
    assert "world.chip" in families
    assert "character.staff.human" in families
    assert "character.helper" in families
    assert "platform.android" in families
    assert "data.unity_textasset" in families
    assert any(row["subfamily"] == "selector_index" for row in taxonomy["assets"])
    assert any(row["subfamily"] == "animation_timeline" for row in taxonomy["assets"])
    assert any(row["lineage"] == "derived_reconstruction" for row in taxonomy["assets"])

    print(f"asset_family_taxonomy_test_passed assets={counts['assets']} families={counts['families']} subfamilies={counts['subfamilies']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
