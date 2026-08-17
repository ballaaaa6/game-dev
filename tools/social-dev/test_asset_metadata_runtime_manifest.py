"""Deterministic checks for the runtime asset metadata manifest."""

from __future__ import annotations

import json

import build_asset_metadata_runtime_manifest as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    manifest = load(builder.MANIFEST_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert manifest["schema_version"] == "social-dev-asset-metadata-runtime-manifest-v1"
    assert manifest["status"] == "pass"
    assert manifest["semantic_status"] == "approved_for_runtime_query_contract"
    assert manifest["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    assert manifest["counts"]["runtime_assets"] == 186
    assert manifest["counts"]["native_catalog_assets"] == 3542
    assert manifest["counts"]["native_catalog_selectors"] == 3192
    assert manifest["counts"]["families"] == 27
    assert len(manifest["runtime_assets"]) == 186
    assert len({item["asset_id"] for item in manifest["runtime_assets"]}) == 186
    assert manifest["lazy_loading"]["eager_load_full_catalog"] is False
    assert manifest["lazy_loading"]["source_archive_imports"] is False
    assert manifest["runtime_policy"]["placement_inference_disabled"] is True
    assert contract["acceptance"]["runtime_assets_are_lazy"] is True
    assert contract["acceptance"]["runtime_asset_ids_are_unique"] is True

    by_id = {item["asset_id"]: item for item in manifest["runtime_assets"]}
    assert by_id["asset:01_GAME_PACKS/human/chara86.png"]["family_id"] == "character.staff.human"
    assert by_id["asset:01_GAME_PACKS/chip/desk_00.seb"]["composition_ids"]
    assert by_id["asset:derived/02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_00.png"]["lineage"] == "derived_runtime_output"
    assert any(item["family_id"] == "world.chip" for item in manifest["runtime_assets"])

    print(f"asset_metadata_runtime_manifest_test_passed runtime_assets={manifest['counts']['runtime_assets']} families={manifest['counts']['families']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
