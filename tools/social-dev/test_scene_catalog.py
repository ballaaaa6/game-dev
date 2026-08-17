"""Deterministic checks for the canonical Social Dev SceneCatalog."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import build_scene_catalog as builder


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
    fixture_path = EVIDENCE / "scene_catalog_fixture.json"
    validation_path = EVIDENCE / "scene_catalog_validation.json"
    contract_path = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
    fixture = load(fixture_path)
    validation = load(validation_path)
    contract = load(contract_path)

    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-scene-catalog-fixture-v1"
    assert contract["schema_version"] == "social-dev-scene-catalog-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"]
    assert validation["counts"]["checks"] >= 20
    assert contract["catalog_id"] == "display-slice-01"
    assert len(contract["scenes"]) == 1

    scene = contract["scenes"][0]
    assert scene["id"] == "room:0"
    assert scene["name"] == {"English": "Floor A", "Japanese": "フロアA"}
    assert scene["source_identity"] == {"type": "RoomData", "id_field": "id_", "source_id": 0}
    assert scene["grid"]["width"] == scene["grid"]["height"] == 10
    assert scene["grid"]["objMap"] == [
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 0, 0, 3, 3, 3, 3, 3, 3, 6],
        [6, 0, 0, 3, 4, 3, 3, 4, 3, 6],
        [6, 0, 0, 3, 3, 3, 3, 3, 3, 6],
        [6, 0, 2, 2, 0, 0, 2, 0, 5, 6],
        [6, 0, 2, 2, 0, 0, 2, 0, 1, 6],
        [6, 0, 0, 0, 0, 0, 0, 0, 1, 6],
        [6, 0, 1, 0, 1, 0, 1, 0, 0, 6],
        [6, 0, 1, 0, 1, 0, 1, 0, 0, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    ]
    assert len(scene["grid"]["objDir"]) == len(scene["grid"]["objMap"]) == 10
    assert all(len(row) == 10 for row in scene["grid"]["objDir"])
    assert scene["grid"]["indexing"]["flat_index"] == "x + y * width"
    assert scene["grid"]["native_assignment"]["raw_cell"] == "objMap[y][x]"

    assert scene["door"]["type"] == 5
    assert scene["door"]["cells"] == [{"x": 8, "y": 4, "raw_map_value": 5, "raw_dir_value": 0}]
    assert scene["door"]["installed_flag"] == 1
    assert scene["door"]["image_id_raw"] == 7
    assert scene["door"]["image_id_status"] == "raw_only"

    type4 = scene["type4_fixture"]
    assert type4["anchor"] == {"x": 4, "y": 2, "raw_map_value": 4}
    assert type4["furniture_binding"]["id"] == 0
    assert type4["furniture_binding"]["type"] == 4
    assert type4["furniture_binding"]["passMap_shape"] == [9, 9]
    assert len(type4["footprint"]["footprint"]) == 9
    assert type4["footprint"]["parent_center_offset"] == {"dx": 0, "dy": 0}
    assert type4["passability"]["matrix"] == [[True, False, False], [True, False, False], [True, True, True]]
    assert all(item["isPassable"] for item in type4["passability"]["synthetic_zero_probes"])
    assert type4["passability"]["all_nonzero_probe"]["isPassable"] is False

    route = scene["route_fixtures"][0]
    assert route["id"] == "room:0/door-to-desk-6"
    assert route["path"] == [[8, 4], [7, 4], [6, 4]]
    assert route["step_count"] == 2
    assert route["neighbor_policy"]["connectivity"] == 4
    assert route["neighbor_policy"]["corners_included"] is False
    assert route["goal_filter"]["equip_flag_on_type1"]["direction"] == 7
    assert {item["id"] for item in route["filter_probes"]} == {
        "occupied-type2",
        "type4-ispassable-false",
        "type6-outdoor",
    }
    assert all(item["path"] is None and item["admission"]["admitted"] is False for item in route["filter_probes"])

    provenance = contract["provenance"]
    assert provenance["status"] == "verified"
    assert provenance["apk"]["hash_status"] == "pass"
    assert len(provenance["apk"]["sha256"]) == 64
    assert provenance["data_rows"]["RoomData"]["English"]["row_sha256"]
    assert provenance["data_rows"]["FurnitureData_type4"]["Japanese"]["row_sha256"]
    assert provenance["source_slices"]
    assert all(item["hash_status"] == "pass" for item in provenance["source_slices"])
    assert len(provenance["native_methods"]) == 9
    assert "ObjectCatalog" in scene["deferred"]
    assert "renderer" in scene["deferred"]
    assert "runtime_behavior" in scene["deferred"]

    assert fixture["determinism"]["content_hash"] == validation["fixture_hash"]
    assert contract["determinism"]["contract_hash"] == validation["contract_hash"]
    assert contract["fixture_ref"]["content_hash"] == fixture["determinism"]["content_hash"]

    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "scene_catalog_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"scenes={validation['counts']['scenes']} "
        f"grid_cells={validation['counts']['grid_cells']} "
        f"route_steps={validation['counts']['route_steps']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
