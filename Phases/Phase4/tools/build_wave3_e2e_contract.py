#!/usr/bin/env python3
"""Build the Wave 3 C6 single-actor end-to-end fixture and golden trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_wave3_actor_contract import ARTIFACTS, ROOT, load_json, rel, sha256, write_json


WAVE2_SCENE = ARTIFACTS / "wave2_minimum_scene_fixture.json"
IDENTITY_CONTRACT = ARTIFACTS / "wave3_actor_identity_contract.json"
SPAWN_FIXTURE = ARTIFACTS / "wave3_spawn_fixture.json"
STATE_CONTRACT = ARTIFACTS / "wave3_actor_state_contract.json"
STATE_FIXTURE = ARTIFACTS / "wave3_state_transition_fixture.json"
MOVEMENT_CONTRACT = ARTIFACTS / "wave3_movement_contract.json"
MOVEMENT_FIXTURE = ARTIFACTS / "wave3_movement_fixture.json"
INTERACTION_CONTRACT = ARTIFACTS / "wave3_interaction_contract.json"
SEAT_FIXTURE = ARTIFACTS / "wave3_seat_fixture.json"
ANIMATION_CONTRACT = ARTIFACTS / "wave3_actor_animation_contract.json"
DRAW_FIXTURE = ARTIFACTS / "wave3_draw_fixture.json"


def scenario_by_id(fixture: dict[str, Any], scenario_id: str) -> dict[str, Any]:
    for scenario in fixture.get("scenarios", []):
        if scenario.get("id") == scenario_id:
            return scenario
    raise RuntimeError(f"fixture scenario not found: {scenario_id}")


def build_inputs() -> dict[str, str]:
    return {
        "wave2_minimum_scene_fixture": rel(WAVE2_SCENE),
        "identity_contract": rel(IDENTITY_CONTRACT),
        "spawn_fixture": rel(SPAWN_FIXTURE),
        "state_contract": rel(STATE_CONTRACT),
        "state_fixture": rel(STATE_FIXTURE),
        "movement_contract": rel(MOVEMENT_CONTRACT),
        "movement_fixture": rel(MOVEMENT_FIXTURE),
        "interaction_contract": rel(INTERACTION_CONTRACT),
        "seat_fixture": rel(SEAT_FIXTURE),
        "animation_contract": rel(ANIMATION_CONTRACT),
        "draw_fixture": rel(DRAW_FIXTURE),
    }


def build_adapter_contract(
    scene: dict[str, Any],
    state: dict[str, Any],
    movement: dict[str, Any],
    interaction: dict[str, Any],
    animation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "clock": {
            "kind": "deterministic_adapter_clock",
            "frame_ms": 100,
            "legacy_timing_status": "unknown",
        },
        "scene_boundary": {
            "fixture": rel(WAVE2_SCENE),
            "room_status": scene["status"],
            "coordinate_status": scene["coordinate"]["object_anchor_formula"]["status"],
            "draw_order_status": scene["draw_order"]["semantic_status"],
            "status": "wave2_contract_boundary_not_full_room_runtime",
        },
        "state_boundary": {
            "fixture": rel(STATE_CONTRACT),
            "raw_state_status": state["summary"]["semantic_status"],
            "adapter_state_policy": "walking/idle/sitting are explicit web adapter states; raw HumanState/HumanMode are not silently mapped",
            "status": "raw_and_adapter_state_namespaces_separate",
        },
        "movement_boundary": {
            "fixture": rel(MOVEMENT_CONTRACT),
            "position_space": "adapter_world_position",
            "arrival_tolerance": "fixture_exact_point",
            "blocked_policy": movement["adapter_tick_policy"]["blocked_rule"],
            "status": "web_adapter_decision",
        },
        "seat_boundary": {
            "fixture": rel(INTERACTION_CONTRACT),
            "operations": ["occupy", "release", "query"],
            "legacy_occupancy_status": interaction["summary"]["legacy_occupancy_status"],
            "status": "explicit_adapter_relation_not_derived_from_raw_HumanSitChair",
        },
        "draw_boundary": {
            "fixture": rel(ANIMATION_CONTRACT),
            "composition_status": animation["composition_contract"]["status"],
            "selector_policy": "draw uses explicit TFace/TBody/TMode; semantic Agent state does not choose selectors",
            "unknown_animation_policy": "static verified frame may be used by adapter; unresolved face selectors are never substituted",
            "status": "deterministic_composition_semantic_animation_open",
        },
        "legacy_equivalence": False,
    }


def spawn_event(spawn: dict[str, Any], tick: int = 0) -> dict[str, Any]:
    expected = spawn["expected"]
    initial = expected["initial_actor_fields"]
    return {
        "tick": tick,
        "event": "spawn",
        "actor_id": expected["actor_identity"]["actor_id"],
        "employee_id": expected["employee_binding"]["employee_id"],
        "status": "spawned",
        "raw_state": {
            "HumanEnabled": initial["HumanEnabled"],
            "HumanMode": initial["HumanMode"],
            "HumanState": initial["HumanState"],
            "HumanAnime": initial["HumanAnime"],
            "HumanWait": initial["HumanWait"],
        },
        "selector_sources": {
            "TFace": initial["HumanFaceG"],
            "TBody": initial["HumanBodyG"],
            "TMode": "explicit_draw_selector_required",
        },
        "provenance": rel(SPAWN_FIXTURE),
        "legacy_equivalence": False,
    }


def draw_event(draw: dict[str, Any], scenario_id: str, tick: int) -> dict[str, Any]:
    source = scenario_by_id(draw, scenario_id)
    return {
        "tick": tick,
        "event": "draw",
        "source_scenario": scenario_id,
        "input": source["input"],
        "expected": source["expected"],
        "provenance": rel(DRAW_FIXTURE),
        "legacy_equivalence": source["expected"].get("legacy_equivalence", False),
    }


def build_scenarios(
    spawn: dict[str, Any],
    state_fixture: dict[str, Any],
    movement_fixture: dict[str, Any],
    seat_fixture: dict[str, Any],
    draw_fixture: dict[str, Any],
) -> list[dict[str, Any]]:
    spawn_step = spawn_event(spawn)
    movement = scenario_by_id(movement_fixture, "raw_target_to_position_trace")
    blocked = scenario_by_id(movement_fixture, "blocked_target_does_not_teleport")
    occupy = scenario_by_id(seat_fixture, "occupy_free_seat")
    conflict = scenario_by_id(seat_fixture, "occupied_seat_conflict")
    release = scenario_by_id(seat_fixture, "release_by_owner")
    raw_seed = scenario_by_id(state_fixture, "raw_spawn_seed")
    adapter_walking = scenario_by_id(state_fixture, "adapter_walking")
    adapter_idle = scenario_by_id(state_fixture, "adapter_idle_after_arrival")

    walk_events = [spawn_step]
    walk_events.extend(
        [
            {
                "tick": 0,
                "event": "state",
                "transition": adapter_walking["input"],
                "expected": adapter_walking["expected"],
                "provenance": rel(STATE_FIXTURE),
            },
            {
                "tick": 1,
                "event": "move",
                "position": movement["expected"]["positions_by_tick"][0],
                "movement_status": "moving",
                "provenance": rel(MOVEMENT_FIXTURE),
            },
            {
                "tick": 2,
                "event": "move",
                "position": movement["expected"]["positions_by_tick"][1],
                "movement_status": "moving",
                "provenance": rel(MOVEMENT_FIXTURE),
            },
            {
                "tick": 3,
                "event": "move",
                "position": movement["expected"]["positions_by_tick"][2],
                "movement_status": movement["expected"]["final_status"],
                "provenance": rel(MOVEMENT_FIXTURE),
            },
            {
                "tick": 3,
                "event": "state",
                "transition": adapter_idle["input"],
                "expected": adapter_idle["expected"],
                "provenance": rel(STATE_FIXTURE),
            },
        ]
    )
    walk_events.append(draw_event(draw_fixture, "actor_draw_mode_0", 3))

    blocked_events = [
        spawn_step,
        {
            "tick": 0,
            "event": "state",
            "transition": adapter_walking["input"],
            "expected": adapter_walking["expected"],
            "provenance": rel(STATE_FIXTURE),
        },
        {
            "tick": 1,
            "event": "move",
            "position": blocked["expected"]["positions_by_tick"][0],
            "movement_status": blocked["expected"]["final_status"],
            "provenance": rel(MOVEMENT_FIXTURE),
        },
    ]

    return [
        {
            "id": "spawn_idle_draw",
            "purpose": "spawn one actor, retain raw seed, and issue a verified explicit draw command",
            "trace": [spawn_step, scenario_by_id(state_fixture, "raw_spawn_seed") | {"tick": 0, "event": "state", "provenance": rel(STATE_FIXTURE)}, draw_event(draw_fixture, "actor_draw_mode_0", 0)],
            "expected": {
                "status": "passed",
                "final_adapter_state": "idle",
                "position": [0, 0],
                "draw_status": "draw_command_ready",
                "legacy_equivalence": False,
            },
        },
        {
            "id": "walk_to_target_arrive",
            "purpose": "golden path from spawn through deterministic adapter movement to arrival and draw",
            "trace": walk_events,
            "expected": {
                "status": "passed",
                "positions_by_tick": [[0, 0], [1, 0], [2, 0], [3, 0]],
                "final_adapter_state": "idle",
                "movement_status": "arrived",
                "draw_status": "draw_command_ready",
                "legacy_equivalence": False,
            },
        },
        {
            "id": "blocked_target",
            "purpose": "collision provider blocks movement without teleporting actor",
            "trace": blocked_events,
            "expected": {
                "status": "blocked",
                "position_after_block": [0, 0],
                "movement_status": "blocked",
                "draw_dispatched": False,
                "legacy_equivalence": False,
            },
        },
        {
            "id": "seat_occupied",
            "purpose": "explicit seat conflict prevents actor 1 from acquiring a seat owned by actor 0",
            "trace": [
                spawn_step,
                {"tick": 0, "event": "seat", "operation": occupy["input"]["operation"], "actor_id": occupy["input"]["agent_id"], "seat_id": occupy["input"]["seat_id"], "result": occupy["expected"]["result"], "owner": occupy["expected"]["owner"], "provenance": rel(SEAT_FIXTURE)},
                {"tick": 1, "event": "seat", "operation": conflict["input"]["operation"], "actor_id": conflict["input"]["agent_id"], "seat_id": conflict["input"]["seat_id"], "result": conflict["expected"]["result"], "owner_after": conflict["expected"]["owner_after"], "provenance": rel(SEAT_FIXTURE)},
            ],
            "expected": {
                "status": "seat_conflict",
                "seat_owner": "adapter.actor.0",
                "actor_state": "actor.1_not_seated",
                "legacy_occupancy_equivalence": False,
            },
        },
        {
            "id": "seat_release_then_sit",
            "purpose": "owner release followed by explicit re-acquisition for the same actor",
            "trace": [
                spawn_step,
                {"tick": 0, "event": "seat", "operation": occupy["input"]["operation"], "actor_id": occupy["input"]["agent_id"], "seat_id": occupy["input"]["seat_id"], "result": occupy["expected"]["result"], "owner": occupy["expected"]["owner"], "provenance": rel(SEAT_FIXTURE)},
                {"tick": 1, "event": "seat", "operation": release["input"]["operation"], "actor_id": release["input"]["agent_id"], "seat_id": release["input"]["seat_id"], "result": release["expected"]["result"], "state_after": release["expected"]["state_after"], "provenance": rel(SEAT_FIXTURE)},
                {"tick": 2, "event": "seat", "operation": occupy["input"]["operation"], "actor_id": occupy["input"]["agent_id"], "seat_id": occupy["input"]["seat_id"], "result": occupy["expected"]["result"], "owner": occupy["expected"]["owner"], "adapter_state": "sitting", "provenance": rel(SEAT_FIXTURE)},
                draw_event(draw_fixture, "actor_draw_mode_0", 2),
            ],
            "expected": {
                "status": "passed",
                "final_adapter_state": "sitting",
                "seat_owner": "adapter.actor.0",
                "draw_status": "draw_command_ready",
                "legacy_occupancy_equivalence": False,
            },
        },
        {
            "id": "animation_unknown_fallback",
            "purpose": "unknown raw animation state uses an explicit verified static frame policy without asset substitution",
            "trace": [
                spawn_step,
                {
                    "tick": 0,
                    "event": "animation_resolve",
                    "raw_state": {"HumanState": 2, "HumanMode": 5, "HumanAnime": 15},
                    "status": "semantic_animation_unknown",
                    "policy": "static_verified_frame_only_no_asset_substitution",
                    "provenance": rel(ANIMATION_CONTRACT),
                },
                draw_event(draw_fixture, "raw_state_does_not_choose_mode", 0),
            ],
            "expected": {
                "status": "passed",
                "fallback_type": "adapter_static_frame_only",
                "draw_status": "use_explicit_draw_selectors",
                "asset_substitution": False,
                "semantic_state": None,
                "legacy_equivalence": False,
            },
        },
    ]


def build_trace(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    golden = next(row for row in scenarios if row["id"] == "walk_to_target_arrive")
    return {
        "schema_version": "wave3-actor-trace-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C6-single-actor-golden-trace",
        "trace_id": "spawn_move_arrive_draw",
        "source_fixture": "Phases/Phase4/artifacts/wave3_actor_e2e_fixture.json",
        "event_order": ["spawn", "state(adapter_walking)", "move", "state(adapter_idle_after_arrival)", "draw"],
        "events": golden["trace"],
        "expected": golden["expected"],
        "trace_policy": {
            "clock": "deterministic_adapter_clock/frame_ms=100",
            "position_space": "adapter_world_position",
            "draw_selector_policy": "explicit TFace/TBody/TMode; raw state does not silently choose TMode",
            "legacy_equivalence": False,
        },
        "status": "golden_trace_ready_adapter_boundary_legacy_semantics_open",
    }


def build() -> dict[Path, Any]:
    required = [
        WAVE2_SCENE,
        IDENTITY_CONTRACT,
        SPAWN_FIXTURE,
        STATE_CONTRACT,
        STATE_FIXTURE,
        MOVEMENT_CONTRACT,
        MOVEMENT_FIXTURE,
        INTERACTION_CONTRACT,
        SEAT_FIXTURE,
        ANIMATION_CONTRACT,
        DRAW_FIXTURE,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C6 inputs: " + ", ".join(missing))

    scene = load_json(WAVE2_SCENE)
    identity = load_json(IDENTITY_CONTRACT)
    spawn = load_json(SPAWN_FIXTURE)
    state = load_json(STATE_CONTRACT)
    state_fixture = load_json(STATE_FIXTURE)
    movement = load_json(MOVEMENT_CONTRACT)
    movement_fixture = load_json(MOVEMENT_FIXTURE)
    interaction = load_json(INTERACTION_CONTRACT)
    seat_fixture = load_json(SEAT_FIXTURE)
    animation = load_json(ANIMATION_CONTRACT)
    draw_fixture = load_json(DRAW_FIXTURE)

    scenarios = build_scenarios(spawn, state_fixture, movement_fixture, seat_fixture, draw_fixture)
    fixture = {
        "schema_version": "wave3-actor-e2e-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C6-single-actor-end-to-end",
        "source_roots_read_only": True,
        "fixture_id": "single_actor_end_to_end_boundary",
        "fixture_scope": "deterministic contract composition; no claim of full legacy runtime equivalence",
        "inputs": build_inputs(),
        "adapter_contract": build_adapter_contract(scene, state, movement, interaction, animation),
        "scenarios": scenarios,
        "required_scenarios": [
            "spawn_idle_draw",
            "walk_to_target_arrive",
            "blocked_target",
            "seat_occupied",
            "seat_release_then_sit",
            "animation_unknown_fallback",
        ],
        "not_claimed": [
            "adapter state names are recovered HumanState/HumanMode semantics",
            "adapter movement position equals legacy world/pixel/isometric position",
            "seat occupancy is produced by HumanSitChair or chair arrays",
            "raw HumanMode/HumanAnime selects DrawHuman TMode",
            "static frame policy substitutes missing TFace=40/41 assets",
            "Wave2 minimum scene fixture is a complete room reconstruction",
        ],
        "status": "deterministic_e2e_fixture_ready_legacy_semantics_open",
    }
    trace = build_trace(scenarios)
    source_paths = required
    manifest = {
        "schema_version": "wave3-c6-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C6-single-actor-end-to-end",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_paths},
        "artifact_inputs": [rel(path) for path in required],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_actor_e2e_fixture.json",
            "Phases/Phase4/artifacts/wave3_actor_trace.json",
            "Phases/Phase4/artifacts/wave3_c6_build_manifest.json",
        ],
        "artifact_summary": {
            "scenario_count": len(scenarios),
            "required_scenario_count": len(fixture["required_scenarios"]),
            "golden_trace_event_count": len(trace["events"]),
            "legacy_equivalence": False,
            "status": fixture["status"],
        },
        "status": "W3-C6-built_single_actor_e2e_fixture_and_golden_trace_legacy_semantics_open",
    }
    return {
        ARTIFACTS / "wave3_actor_e2e_fixture.json": fixture,
        ARTIFACTS / "wave3_actor_trace.json": trace,
        ARTIFACTS / "wave3_c6_build_manifest.json": manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare with existing artifacts")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            if not path.is_file() or json.loads(path.read_text(encoding="utf-8")) != expected:
                mismatches.append(rel(path))
        if mismatches:
            raise SystemExit("artifact mismatch: " + ", ".join(mismatches))
        return
    for path, value in outputs.items():
        write_json(path, value)
    print(json.dumps({"outputs": [rel(path) for path in outputs], "status": "built"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
