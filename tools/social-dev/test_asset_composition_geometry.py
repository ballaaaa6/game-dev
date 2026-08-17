"""Deterministic checks for AM-4 composition and geometry catalogs."""

from __future__ import annotations

import json

import build_asset_composition_geometry as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    composition = load(builder.COMPOSITION_PATH)
    geometry = load(builder.GEOMETRY_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt_composition, compositions, direct_entries = builder.build_compositions()
    rebuilt_geometry = builder.build_geometry(rebuilt_composition, compositions, direct_entries)
    rebuilt_contract = builder.build_contract_payload(rebuilt_composition, rebuilt_geometry)

    assert composition["schema_version"] == "social-dev-asset-composition-catalog-v1"
    assert geometry["schema_version"] == "social-dev-asset-geometry-catalog-v1"
    assert composition["status"] == "pass"
    assert geometry["status"] == "pass"
    assert composition["determinism"]["content_hash"] == rebuilt_composition["determinism"]["content_hash"]
    assert geometry["determinism"]["content_hash"] == rebuilt_geometry["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]

    assert composition["counts"]["character_seb_compositions"] == 35
    assert composition["counts"]["logical_reconstructions"] == 4
    assert composition["counts"]["furniture_object_compositions"] == 4
    assert composition["counts"]["native_initial_object_compositions"] == 4
    assert geometry["counts"]["indexed_asset_rows"] == 3542
    assert geometry["counts"]["runtime_geometry_gaps"] == 0
    assert len(geometry["assets"]) == geometry["counts"]["geometry_rows"]
    assert contract["acceptance"]["runtime_geometry_gaps_closed"] is True
    assert contract["acceptance"]["character_animation_compositions_closed"] is True
    assert contract["acceptance"]["logical_reconstructions_closed"] is True

    composition_by_id = {item["composition_id"]: item for item in composition["compositions"]}
    assert composition_by_id["character_animation:walk_right.seb"]["record_summary"]["record_count"] > 0
    assert composition_by_id["display_object:furniture:2"]["record_summary"]["destination_bounds"]
    assert composition_by_id["native_initial_object:furniture:12"]["record_summary"]["destination_bounds"]

    geometry_by_id = {item["asset_id"]: item for item in geometry["assets"]}
    assert geometry_by_id["asset:01_GAME_PACKS/human/chara86.png"]["geometry_status"] in {"physical_dimensions_closed", "composition_and_geometry_closed"}
    assert geometry_by_id["asset:01_GAME_PACKS/chip/chair_00.opt"]["runtime_relevant"] is True
    assert geometry_by_id["asset:01_GAME_PACKS/chip/chair_00.opt"]["composition_ids"]
    assert geometry_by_id["asset:derived/02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_00.png"]["geometry_status"] == "derived_runtime_geometry_closed"

    print(f"asset_composition_geometry_test_passed compositions={composition['counts']['composition_entries']} geometry_rows={geometry['counts']['geometry_rows']} runtime_gaps={geometry['counts']['runtime_geometry_gaps']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
