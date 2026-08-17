from __future__ import annotations

import json
from pathlib import Path

import build_character_asset_manifest as builder


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
    fixture = load(EVIDENCE / "character_asset_fixture.json")
    validation = load(EVIDENCE / "character_asset_validation.json")
    contract = load(RUNTIME_EVIDENCE / "character_asset_manifest.json")
    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-character-asset-fixture-v1"
    assert contract["schema_version"] == "social-dev-character-asset-manifest-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_catalog"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"]
    assert validation["counts"]["images"] == 105
    assert validation["counts"]["animations"] == 35
    assert validation["counts"]["staff_bindings"] == 141
    assert validation["counts"]["multilayer_animations"] == 8
    assert validation["counts"]["decoded_layers"] == 48
    assert validation["counts"]["decoded_records"] == 334
    assert validation["counts"]["promoted_bytes"] == 201347

    assert [item["selector_id"] for item in contract["images"]] == list(range(105))
    assert [item["selector_id"] for item in contract["animations"]] == [*range(34), 100]
    assert [item["source_id"] for item in contract["staff_bindings"]] == list(range(141))
    assert all(item["source_sha256"] == item["runtime_sha256"] for item in contract["images"])
    assert all(item["source_sha256"] == item["runtime_sha256"] for item in contract["animations"])
    assert all(item["header"]["layer_count"] == len(item["layers"]) for item in contract["animations"])
    assert any(item["header"]["layer_count"] == 3 for item in contract["animations"])
    assert any(record["texture_status"] == "control_no_texture" for item in contract["animations"] for record in item["records"])
    assert all(
        record["texture_status"] == "control_no_texture"
        or record["source_x"] + record["width"] <= record["source_size"]["width"]
        and record["source_y"] + record["height"] <= record["source_size"]["height"]
        for item in contract["animations"]
        for record in item["records"]
    )
    assert contract["runtime_policy"]["image_loading"] == "lazy_by_character_and_asset_id"
    assert contract["runtime_policy"]["eager_load_full_catalog"] is False

    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "character_asset_manifest_test_passed "
        f"images={validation['counts']['images']} "
        f"animations={validation['counts']['animations']} "
        f"layers={validation['counts']['decoded_layers']} "
        f"records={validation['counts']['decoded_records']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
