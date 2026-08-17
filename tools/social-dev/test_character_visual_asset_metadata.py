"""Deterministic checks for Track H character visual metadata."""

from __future__ import annotations

import json

import build_character_visual_asset_metadata as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    catalog = load(builder.CATALOG_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert catalog["schema_version"] == "social-dev-character-visual-asset-metadata-v1"
    assert catalog["status"] == "pass"
    assert catalog["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    counts = catalog["counts"]
    assert counts["staff_records"] == 141
    assert counts["staff_image_bindings"] == 141
    assert counts["unique_human_images"] == 105
    assert counts["human_animations"] == 35
    assert counts["helper_records"] == 19
    assert counts["helper_image_statuses"]["resolved"] == 7
    assert counts["helper_image_statuses"]["deferred"] == 11
    assert counts["helper_image_statuses"]["absent_by_sentinel"] == 1
    assert counts["avatar_body_assets"] == 284
    assert counts["avatar_head_assets"] == 509
    assert len(catalog["staff"]) == 141
    assert len(catalog["helpers"]) == 19
    assert len(catalog["human_visuals"]["images"]) == 105
    assert len(catalog["human_visuals"]["animations"]) == 35

    staff = {item["record_id"]: item for item in catalog["staff"]}
    assert staff["staff:0"]["image_selector"]["asset_id"] == "asset:01_GAME_PACKS/human/chara86.png"
    helper = {item["record_id"]: item for item in catalog["helpers"]}
    assert helper["helper:0"]["image_selector"]["resolution_status"] == "absent_by_sentinel"
    assert helper["helper:8"]["image_selector"]["resolution_status"] == "deferred"
    assert contract["acceptance"]["all_staff_records_bound"] is True
    assert contract["acceptance"]["human_images_closed"] is True
    assert contract["acceptance"]["human_animations_closed"] is True
    assert contract["acceptance"]["helper_visual_gap_explicit"] is True
    assert contract["acceptance"]["avatar_boundary_explicit"] is True

    print(f"character_visual_asset_metadata_test_passed staff={counts['staff_records']} helpers={counts['helper_records']} human_images={counts['unique_human_images']} human_animations={counts['human_animations']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
