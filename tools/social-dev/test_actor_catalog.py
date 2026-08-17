"""Deterministic checks for the canonical Social Dev ActorCatalog."""

from __future__ import annotations

import json
from pathlib import Path

import build_actor_catalog as builder


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
    fixture_path = EVIDENCE / "actor_catalog_fixture.json"
    validation_path = EVIDENCE / "actor_catalog_validation.json"
    contract_path = RUNTIME_EVIDENCE / "actor_catalog_contract.json"
    fixture = load(fixture_path)
    validation = load(validation_path)
    contract = load(contract_path)

    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-actor-catalog-fixture-v1"
    assert contract["schema_version"] == "social-dev-actor-catalog-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert fixture["semantic_status"] == "deterministic_fixture"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["semantic_status"] == "validated"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"]
    assert validation["counts"]["actors"] == 5
    assert validation["counts"]["job_records"] == 1
    assert validation["counts"]["skill_records"] == 1
    assert validation["counts"]["resolved_portrait_selectors"] == 5
    assert validation["counts"]["resolved_animation_selectors"] == 8
    assert validation["counts"]["deferred_spawn_boundaries"] == 5

    actors = contract["actors"]
    assert [item["id"] for item in actors] == [f"actor:staff:{item}" for item in range(5)]
    assert [item["source_identity"]["source_id"] for item in actors] == list(range(5))
    assert [item["name"]["values"]["English"] for item in actors] == [
        "10s Female",
        "10s Male",
        "20s Female",
        "20s Male",
        "30s Female",
    ]
    assert [item["portrait_selector"]["id"] for item in actors] == [86, 87, 88, 89, 90]
    assert [item["portrait_selector"]["filename"] for item in actors] == [
        "chara86.png",
        "chara87.png",
        "chara88.png",
        "chara89.png",
        "chara90.png",
    ]
    assert all(item["portrait_selector"]["resolution_status"] == "resolved" for item in actors)
    assert all(item["job_ref"]["id"] == "job:4" for item in actors)
    assert all(item["skill_ref"]["id"] == "skill:1" for item in actors)
    assert all(item["spawn_boundary"]["status"] == "deferred" for item in actors)
    assert all(item["status"] == "verified" for item in actors)
    assert "unknown" not in builder.stable_json(actors).lower()

    animation = contract["animation_profiles"][0]
    assert animation["id"] == "human-living-scene-v1"
    assert [item["wait"]["seb_id"] for item in animation["directions"]] == [10, 11, 12, 13]
    assert [item["typing"]["seb_id"] for item in animation["directions"]] == [23, 24, 25, 26]
    assert animation["typing_rules"]["start"]["typingFrame"] == 100
    assert animation["typing_rules"]["start"]["sebFrameInterval"] == 3
    assert animation["typing_rules"]["end"]["typingFrame"] == 0
    assert animation["typing_rules"]["end"]["sebFrameInterval"] == 1

    behavior = contract["behavior_profiles"][0]
    assert behavior["id"] == "staff-living-scene-v1"
    assert len(behavior["source_constants"]) == 35
    route_mapping = {
        item["move_mode"]: {"value": item["move_mode_value"], "astar_flag": item["astar_flag"]}
        for item in behavior["route_mapping"]["entries"]
    }
    assert route_mapping == {
        "MOVE_MODE_GOTO_EQUIPMENT": {"value": 1, "astar_flag": 2},
        "MOVE_MODE_TO_STAFF": {"value": 7, "astar_flag": 4},
        "MOVE_MODE_GOTO_DESK": {"value": 3, "astar_flag": 1},
    }
    assert behavior["talk_timing"]["frame_markers"] == [20, 70, 110, 130]
    assert behavior["skill_effect"]["type_value"] == 10
    assert behavior["skill_effect"]["effect_index"] == 8
    assert behavior["skill_effect"]["effect_value"] == 150
    assert behavior["skill_effect"]["flag_value"] == 1

    assert contract["runtime_readiness"]["status"] == "ready_for_vite_typescript_core"
    assert contract["runtime_readiness"]["required_before_runtime"] == ["screenshot baseline", "browser behavior trace"]
    assert contract["fixture_ref"]["content_hash"] == fixture["determinism"]["content_hash"]
    assert validation["contract_hash"] == contract["determinism"]["contract_hash"]
    assert validation["fixture_hash"] == fixture["determinism"]["content_hash"]

    provenance = contract["provenance"]
    assert provenance["status"] == "verified"
    assert provenance["assets"]["asset_zip"]["hash_status"] == "pass"
    assert len(provenance["source_slices"]) == 15
    assert all(item["hash_status"] == "pass" for item in provenance["source_slices"])
    assert all((ROOT / item["path"]).is_file() for item in provenance["input_manifest"]["files"])
    assert all((ROOT / item["path"]).is_file() for item in provenance["source_files"])

    assert not (ROOT / "runtime/social-dev/core").exists()
    assert not (ROOT / "runtime/social-dev/actors").exists()
    assert not (ROOT / "runtime/social-dev/renderer").exists()
    assert not list((ROOT / "runtime/social-dev").rglob("*.cs"))

    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "actor_catalog_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"actors={validation['counts']['actors']} "
        f"portraits={validation['counts']['resolved_portrait_selectors']} "
        f"animations={validation['counts']['resolved_animation_selectors']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
