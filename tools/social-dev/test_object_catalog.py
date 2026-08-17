"""Deterministic checks for the canonical Social Dev ObjectCatalog."""

from __future__ import annotations

import json
from pathlib import Path

import build_object_catalog as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def without_dynamic(value):
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    fixture_path = EVIDENCE / "object_catalog_fixture.json"
    validation_path = EVIDENCE / "object_catalog_validation.json"
    contract_path = RUNTIME_EVIDENCE / "object_catalog_contract.json"
    fixture = load(fixture_path)
    validation = load(validation_path)
    contract = load(contract_path)

    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-object-catalog-fixture-v1"
    assert contract["schema_version"] == "social-dev-object-catalog-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert fixture["semantic_status"] == "deterministic_fixture"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["semantic_status"] == "validated"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"] == 29
    assert validation["counts"] == {
        "checks": 29,
        "passed_checks": 29,
        "objects": 4,
        "raw_object_types": 7,
        "scene_bindings": 3,
        "resolved_selectors": 8,
        "sentinel_selectors": 4,
    }

    objects = {item["id"]: item for item in contract["objects"]}
    assert list(objects) == ["furniture:0", "furniture:1", "furniture:2", "furniture:5"]
    assert all(item["status"] == "verified" for item in objects.values())
    assert all(item["semantic_status"] == "approved_for_runtime_contract" for item in objects.values())

    expected_selectors = {
        "furniture:0": {
            "seb_": ("resolved", "big_base00.seb"),
            "subSeb_": ("absent_by_sentinel", None),
            "img_": ("absent_by_sentinel", None),
        },
        "furniture:1": {
            "seb_": ("resolved", "door_03.seb"),
            "subSeb_": ("absent_by_sentinel", None),
            "img_": ("absent_by_sentinel", None),
        },
        "furniture:2": {
            "seb_": ("resolved", "desk_00.seb"),
            "subSeb_": ("resolved", "chair_00.seb"),
            "img_": ("resolved", "desk_00.png"),
        },
        "furniture:5": {
            "seb_": ("resolved", "desk_00.seb"),
            "subSeb_": ("resolved", "chair_02.seb"),
            "img_": ("resolved", "desk_06.png"),
        },
    }
    for object_id, selector_expectations in expected_selectors.items():
        for field_name, (resolution_status, filename) in selector_expectations.items():
            selector = objects[object_id]["selectors"][field_name]
            assert selector["resolution_status"] == resolution_status
            assert selector.get("filename") == filename
            assert selector["status"] == "verified"
            assert selector["confidence"] == "high"
            if resolution_status == "resolved":
                assert selector["asset_index"]["relative_path"].endswith(filename)
                assert selector["selector_index"]["status"] == "verified"
            else:
                assert selector["id"] == -1

    type4 = objects["furniture:0"]
    assert type4["geometry"]["status"] == "verified"
    assert type4["geometry"]["confidence"] == "high"
    assert len(type4["geometry"]["footprint"]["footprint"]) == 9
    assert type4["geometry"]["footprint"]["parent_center_offset"] == {"dx": 0, "dy": 0}
    assert type4["geometry"]["passability"]["matrix"] == [
        [True, False, False],
        [True, False, False],
        [True, True, True],
    ]
    assert all(item["isPassable"] for item in type4["geometry"]["passability"]["synthetic_zero_probes"])
    assert type4["geometry"]["passability"]["all_nonzero_probe"]["isPassable"] is False

    assert all(objects[item_id]["direction_policy"]["status"] == "verified" for item_id in ["furniture:2", "furniture:5"])
    assert objects["furniture:1"]["direction_policy"]["status"] == "deferred"
    assert "unknown" not in builder.stable_json(contract["objects"]).lower()

    raw_types = contract["raw_object_types"]
    assert [item["raw_type"] for item in raw_types] == list(range(7))
    assert [item["source_constant"]["name"] for item in raw_types] == [
        "OBJ_TYPE_PASS",
        "OBJ_TYPE_EQUIP",
        "OBJ_TYPE_DESK",
        "OBJ_TYPE_BIG",
        "OBJ_TYPE_BIG_CENTER",
        "OBJ_TYPE_DOOR",
        "OBJ_TYPE_OUTDOOR",
    ]

    bindings = {item["id"]: item for item in contract["scene_bindings"]}
    assert bindings["room:0/type4-anchor"]["binding_status"] == "verified_fixture"
    assert bindings["room:0/type4-anchor"]["furniture_id"] == "furniture:0"
    assert bindings["room:0/door-cell"]["binding_status"] == "candidate_by_type_and_selector"
    assert bindings["room:0/door-cell"]["native_binding"]["status"] == "deferred"
    assert bindings["room:0/door-cell"]["installed_flag"] == 1
    assert bindings["room:0/door-cell"]["furniture_candidates"] == ["furniture:1"]
    assert bindings["room:0/occupied-type2-route-probe"]["binding_status"] == "fixture_only"
    assert bindings["room:0/occupied-type2-route-probe"]["furniture_id"] == "furniture:2"
    assert bindings["room:0/occupied-type2-route-probe"]["route_admitted"] is False

    provenance = contract["provenance"]
    assert provenance["status"] == "verified"
    assert provenance["apk"]["hash_status"] == "pass"
    assert provenance["apk"]["expected_sha256"] == provenance["apk"]["actual_sha256"]
    assert provenance["asset_zip"]["hash_status"] == "pass"
    assert provenance["asset_zip"]["expected_sha256"] == provenance["asset_zip"]["actual_sha256"]
    assert len(provenance["source_slices"]) == 11
    assert all(item["hash_status"] == "pass" for item in provenance["source_slices"])
    assert len(provenance["native_methods"]) == 9
    assert all((ROOT / item["path"]).is_file() for item in provenance["input_manifest"]["files"])
    assert all("binary" not in item for item in provenance["input_manifest"]["files"])

    assert fixture["determinism"]["content_hash"] == validation["fixture_hash"]
    assert contract["determinism"]["contract_hash"] == validation["contract_hash"]
    assert contract["fixture_ref"]["content_hash"] == fixture["determinism"]["content_hash"]
    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "object_catalog_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"objects={validation['counts']['objects']} "
        f"raw_types={validation['counts']['raw_object_types']} "
        f"resolved_selectors={validation['counts']['resolved_selectors']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
