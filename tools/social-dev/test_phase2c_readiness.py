"""Deterministic checks for the complete Phase 2C readiness package."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase2c_readiness as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    fixture = load(EVIDENCE / "actor_spawn_fixture.json")
    validation = load(EVIDENCE / "actor_spawn_validation.json")
    spawn_contract = load(RUNTIME_EVIDENCE / "actor_spawn_contract.json")
    camera_contract = load(RUNTIME_EVIDENCE / "camera_coordinate_contract.json")
    behavior_contract = load(RUNTIME_EVIDENCE / "actor_behavior_contract.json")
    tick_contract = load(RUNTIME_EVIDENCE / "tick_order_contract.json")

    rebuilt = builder.finalize_package(builder.build_package())

    assert fixture["schema_version"] == "social-dev-actor-spawn-fixture-v1"
    assert fixture["status"] == validation["status"] == spawn_contract["status"] == "pass"
    assert fixture["semantic_status"] == "deterministic_fixture"
    assert validation["semantic_status"] == "validated"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"] == 12
    assert validation["counts"]["spawned_actors"] == 3

    assert [item["id"] for item in fixture["actors"]] == [
        "actor:staff:0",
        "actor:staff:1",
        "actor:staff:2",
    ]
    assert all(item["spawn_cell"] == fixture["actors"][0]["spawn_cell"] for item in fixture["actors"])
    assert all(item["initial_position"] ["x"] == 280 and item["initial_position"]["y"] == -31 for item in fixture["actors"])
    assert all(item["initial_fields"]["alpha_"]["value"] == 0 for item in fixture["actors"])
    assert all(item["initial_fields"]["speed_"]["value"] == 3 for item in fixture["actors"])
    assert all(item["desk_assignment"]["status"] == "deferred" for item in fixture["actors"])

    assert camera_contract["status"] == "pass"
    assert camera_contract["semantic_status"] == "approved_for_runtime_contract"
    assert camera_contract["coordinate_system"]["actor_spawn_position"]["door_fixture_values"] == [280, -31]
    assert camera_contract["coordinate_system"]["standing_positions"]["door_fixture_values"] == [
        [274, -15],
        [246, -29],
        [274, -29],
        [246, -15],
    ]
    assert camera_contract["camera"]["fixture_offset"] == [0, 0]

    assert behavior_contract["status"] == "pass"
    assert len(behavior_contract["transitions"]) == 4
    assert behavior_contract["route_mapping"]["entries"]
    assert behavior_contract["trace"]["actors"] == [
        "actor:staff:0",
        "actor:staff:1",
        "actor:staff:2",
    ]
    assert behavior_contract["trace"]["milestones"][-1]["event"] == "talk_end"

    assert tick_contract["status"] == "pass"
    assert tick_contract["tick"]["step"] == 1
    assert [item["index"] for item in tick_contract["order"]] == [0, 1, 2, 3]
    assert tick_contract["mutation_policy"]["renderer_may_mutate"] is False

    assert spawn_contract["fixture_ref"]["content_hash"] == fixture["determinism"]["content_hash"]
    assert validation["artifact_hashes"]["spawn_contract"] == spawn_contract["determinism"]["contract_hash"]
    assert builder.without_dynamic(fixture) == builder.without_dynamic(rebuilt["spawn_fixture"])
    assert builder.without_dynamic(validation) == builder.without_dynamic(rebuilt["validation"])
    assert builder.without_dynamic(spawn_contract) == builder.without_dynamic(rebuilt["spawn_contract"])
    assert builder.without_dynamic(camera_contract) == builder.without_dynamic(rebuilt["camera_contract"])
    assert builder.without_dynamic(behavior_contract) == builder.without_dynamic(rebuilt["behavior_contract"])
    assert builder.without_dynamic(tick_contract) == builder.without_dynamic(rebuilt["tick_contract"])

    assert not (ROOT / "runtime/social-dev/core").exists()
    assert not (ROOT / "runtime/social-dev/renderer").exists()

    print(
        "phase2c_readiness_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"actors={validation['counts']['spawned_actors']} "
        f"source_slices={validation['counts']['source_slices']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
