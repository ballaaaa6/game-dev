#!/usr/bin/env python3
"""Build the Wave 3 C3 target/position flow and adapter movement fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_wave3_actor_contract import (
    ARTIFACTS,
    DUMP_CS,
    FORM_C,
    ROOT,
    all_function_spans,
    load_json,
    parse_gameform_fields,
    read_text,
    rel,
    sha256,
    write_json,
)


ACTOR_MAP = ARTIFACTS / "wave3_actor_function_map.json"
IDENTITY_CONTRACT = ARTIFACTS / "wave3_actor_identity_contract.json"
IDENTITY_MANIFEST = ARTIFACTS / "wave3_c1_build_manifest.json"
STATE_CONTRACT = ARTIFACTS / "wave3_actor_state_contract.json"
STATE_MANIFEST = ARTIFACTS / "wave3_c2_build_manifest.json"
WAVE2_MOVEMENT = ARTIFACTS / "wave2_wave3_movement_interface.json"
WAVE2_SCENE = ARTIFACTS / "wave2_minimum_scene_fixture.json"

TARGET_FIELDS = ["TargetX", "TargetY"]
POSITION_FIELDS = ["HumanX", "HumanY", "HumanPX", "HumanPY"]


def function_ref(text: str, symbol: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    spans = all_function_spans(text, symbol)
    if not spans:
        raise RuntimeError(f"function not found: {symbol}")
    span = spans[occurrence - 1]
    lines = text.splitlines()
    hits = [index for index in range(span["line_start"] - 1, span["line_end"]) if needle in lines[index]]
    if not hits:
        return {
            "file": rel(FORM_C),
            "line": None,
            "function": symbol,
            "needle": needle,
            "status": "needle_not_found_in_function",
        }
    return {"file": rel(FORM_C), "line": hits[0] + 1, "function": symbol, "needle": needle}


def field_snapshot(names: list[str]) -> dict[str, Any]:
    fields = parse_gameform_fields(set(names))
    return {
        name: {
            "offset": fields[name]["offset"],
            "declaration": {
                "file": fields[name]["source"],
                "line": fields[name]["line"],
                "needle": f"{name}; // {fields[name]['offset']}",
            },
            "status": "verified_dump_field_declaration",
        }
        for name in names
    }


def build_raw_trace(form_text: str) -> dict[str, Any]:
    add_target = [
        {
            "step": 1,
            "operation": "write",
            "raw_array": "TargetX",
            "index": "TIndex / param_2",
            "value": "TX / param_3",
            "evidence": [function_ref(form_text, "form_GameForm__AddTarget", "0x310")],
        },
        {
            "step": 2,
            "operation": "write",
            "raw_array": "TargetY",
            "index": "TIndex / param_2",
            "value": "TY / param_4",
            "evidence": [function_ref(form_text, "form_GameForm__AddTarget", "0x318")],
        },
    ]
    next_target = [
        {
            "step": 3,
            "condition": "TMode == 0",
            "operation": "copy",
            "from": "TargetX[TPos]",
            "to": "HumanX[THumanIndex]",
            "evidence": [
                function_ref(form_text, "form_GameForm__NextTarget", "lVar4 = *(long *)(lVar3 + 0x310);"),
                function_ref(form_text, "form_GameForm__NextTarget", "lVar5 = *(long *)(lVar3 + 0xf10);"),
            ],
        },
        {
            "step": 4,
            "condition": "TMode == 0",
            "operation": "copy",
            "from": "TargetY[TPos]",
            "to": "HumanY[THumanIndex]",
            "evidence": [
                function_ref(form_text, "form_GameForm__NextTarget", "lVar4 = *(long *)(lVar3 + 0x318);"),
                function_ref(form_text, "form_GameForm__NextTarget", "lVar3 = *(long *)(lVar3 + 0xf18);"),
            ],
        },
        {
            "step": 5,
            "condition": "all modes after bounds checks",
            "operation": "copy",
            "from": "TargetX[TPos]",
            "to": "HumanPX[THumanIndex]",
            "evidence": [
                function_ref(form_text, "form_GameForm__NextTarget", "lVar4 = *(long *)(lVar2 + 0xf20);"),
            ],
        },
        {
            "step": 6,
            "condition": "all modes after bounds checks",
            "operation": "copy",
            "from": "TargetY[TPos]",
            "to": "HumanPY[THumanIndex]",
            "evidence": [
                function_ref(form_text, "form_GameForm__NextTarget", "lVar2 = *(long *)(lVar2 + 0xf28);"),
            ],
        },
    ]
    return {
        "producer": {
            "function": "form_GameForm__AddTarget",
            "signature": "AddTarget(TIndex, TX, TY)",
            "steps": add_target,
            "status": "verified_bounded_raw_writes",
        },
        "consumer": {
            "function": "form_GameForm__NextTarget",
            "signature": "NextTarget(TPos, THumanIndex, TMode)",
            "steps": next_target,
            "status": "verified_bounded_array_copies",
        },
        "callers": [
            {
                "function": "form_GameForm__CallHikkosi",
                "relationship": "calls AddTarget and NextTarget in room/actor setup slice",
                "evidence": [{"file": rel(FORM_C), "line": 25013, "needle": "form_GameForm__CallHikkosi"}],
                "status": "call_graph_observed_semantics_not_closed",
            },
            {
                "function": "form_GameForm__CallSyain",
                "relationship": "calls NextTarget during actor setup",
                "evidence": [{"file": rel(FORM_C), "line": 27392, "needle": "form_GameForm__CallSyain"}],
                "status": "call_graph_observed_semantics_not_closed",
            },
        ],
    }


def build_coordinate_spaces(scene: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "space_id": "legacy_target_array",
            "raw_fields": TARGET_FIELDS,
            "meaning": "array values written by AddTarget and read by NextTarget",
            "status": "verified_raw_storage_flow",
            "legacy_equivalence": True,
        },
        {
            "space_id": "legacy_actor_position_arrays",
            "raw_fields": POSITION_FIELDS,
            "meaning": "array values written by NextTarget; HumanX/Y vs HumanPX/PY role is not named by source evidence",
            "status": "verified_writes_role_open",
            "legacy_equivalence": False,
        },
        {
            "space_id": "adapter_world_position",
            "raw_fields": [],
            "meaning": "stable [x, y] position consumed by the Wave 3 adapter movement fixture",
            "status": "web_adapter_decision",
            "legacy_equivalence": False,
        },
        {
            "space_id": "graphics_local_position",
            "raw_fields": [],
            "meaning": "rendering coordinate space with Wave 2 origin/anchor rules",
            "origin": scene["coordinate"]["graphics_origin"],
            "status": "wave2_coordinate_fixture_inherited",
            "legacy_equivalence": False,
        },
    ]


def build_provider_contract(movement_interface: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": rel(WAVE2_MOVEMENT),
        "status": movement_interface["status"],
        "path": {
            "inputs": movement_interface["walkable"]["inputs"],
            "outputs": movement_interface["walkable"]["output"],
            "adapter_policy": "path data is injected and remains explicitly non-legacy",
        },
        "collision": {
            "inputs": movement_interface["collision"]["inputs"],
            "outputs": movement_interface["collision"]["output"],
            "adapter_policy": "blocked means no position mutation for that tick",
        },
        "seat": {
            "inputs": movement_interface["seat"]["inputs"],
            "output": movement_interface["seat"]["output"],
            "adapter_policy": "seat occupancy is an explicit relation, not inferred from chair pixels",
        },
    }


def build_movement_contract(
    actor_map: dict[str, Any],
    identity: dict[str, Any],
    state: dict[str, Any],
    movement_interface: dict[str, Any],
    scene: dict[str, Any],
    form_text: str,
) -> dict[str, Any]:
    fields = field_snapshot(TARGET_FIELDS + POSITION_FIELDS)
    raw_trace = build_raw_trace(form_text)
    return {
        "schema_version": "wave3-actor-movement-contract-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C3-target-position-and-adapter-movement",
        "source_roots_read_only": True,
        "inputs": {
            "actor_function_map": rel(ACTOR_MAP),
            "identity_contract": rel(IDENTITY_CONTRACT),
            "state_contract": rel(STATE_CONTRACT),
            "wave2_movement_interface": rel(WAVE2_MOVEMENT),
            "wave2_scene_fixture": rel(WAVE2_SCENE),
        },
        "raw_field_snapshot": fields,
        "raw_field_flow": raw_trace,
        "coordinate_spaces": build_coordinate_spaces(scene),
        "provider_contract": build_provider_contract(movement_interface),
        "adapter_tick_policy": {
            "clock": "deterministic fixture clock",
            "step_rule": "advance at most one supplied waypoint per tick",
            "arrival_rule": "arrived only when supplied path is exhausted or explicit target tolerance is met",
            "blocked_rule": "do not teleport and do not mutate adapter position when collision returns blocked",
            "unavailable_rule": "preserve position and return provider_unavailable",
            "legacy_timing_equivalence": False,
            "status": "web_adapter_decision",
        },
        "semantic_limits": [
            "HumanX/HumanY are not promoted to a generic world position without a runtime adapter boundary",
            "HumanPX/HumanPY are not labelled previous position solely from field names or offsets",
            "TargetX/TargetY are not treated as a path graph or walkable grid",
            "collision and seat state remain provider inputs, not recovered legacy semantics",
            "adapter movement state is not claimed equivalent to HumanMode or HumanState",
        ],
        "summary": {
            "target_field_count": len(TARGET_FIELDS),
            "position_field_count": len(POSITION_FIELDS),
            "raw_flow_step_count": sum(len(row["steps"]) for row in [raw_trace["producer"], raw_trace["consumer"]]),
            "provider_count": 3,
            "coordinate_space_count": 4,
            "verified_raw_flow": True,
            "legacy_movement_semantics": "open",
            "status": "target_position_flow_verified_adapter_movement_fixture_only",
        },
    }


def build_fixture(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "wave3-movement-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C3-deterministic-adapter-movement",
        "fixture_id": "target_position_provider_boundary",
        "clock": {"kind": "deterministic_adapter_clock", "tick_ms": 100, "legacy_timing_status": "unknown"},
        "initial": {
            "actor_id": "adapter.actor.0",
            "adapter_world_position": [0, 0],
            "raw_target": [3, 0],
            "raw_position_arrays": {"HumanX": [0, 0], "HumanY": [0, 0], "HumanPX": [0, 0], "HumanPY": [0, 0]},
        },
        "scenarios": [
            {
                "id": "raw_target_to_position_trace",
                "input": {"target": [3, 0], "path_provider": [[0, 0], [1, 0], [2, 0], [3, 0]], "collision": "clear"},
                "expected": {
                    "positions_by_tick": [[1, 0], [2, 0], [3, 0]],
                    "final_status": "arrived",
                    "legacy_equivalence": False,
                },
            },
            {
                "id": "blocked_target_does_not_teleport",
                "input": {"target": [3, 0], "path_provider": [[1, 0]], "collision": "blocked"},
                "expected": {"positions_by_tick": [[0, 0]], "final_status": "blocked", "legacy_equivalence": False},
            },
            {
                "id": "no_path_preserves_position",
                "input": {"target": [3, 0], "path_provider": "no_path", "collision": "clear"},
                "expected": {"positions_by_tick": [[0, 0]], "final_status": "no_path", "legacy_equivalence": False},
            },
            {
                "id": "provider_unavailable_preserves_position",
                "input": {"target": [3, 0], "path_provider": "unavailable", "collision": "unavailable"},
                "expected": {"positions_by_tick": [[0, 0]], "final_status": "provider_unavailable", "legacy_equivalence": False},
            },
            {
                "id": "raw_tmode_zero_copy_is_not_adapter_tick",
                "input": {"raw_trace": "NextTarget", "TMode": 0},
                "expected": {
                    "raw_writes": ["HumanX", "HumanY", "HumanPX", "HumanPY"],
                    "adapter_position_mutation": None,
                    "status": "verified_raw_flow_not_runtime_movement_equivalence",
                },
            },
        ],
        "not_claimed": [
            "HumanX/HumanY are current position in every call context",
            "HumanPX/HumanPY are previous position",
            "TargetX/TargetY contain a complete path",
            "path provider is recovered legacy walkability",
            "blocked/no_path/unavailable statuses match the legacy binary",
        ],
        "source_contract": contract["schema_version"],
        "status": "adapter_movement_fixture_ready_legacy_semantics_open",
    }


def build() -> dict[Path, Any]:
    required = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        IDENTITY_CONTRACT,
        IDENTITY_MANIFEST,
        STATE_CONTRACT,
        STATE_MANIFEST,
        WAVE2_MOVEMENT,
        WAVE2_SCENE,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C3 inputs: " + ", ".join(missing))
    form_text = read_text(FORM_C)
    actor_map = load_json(ACTOR_MAP)
    identity = load_json(IDENTITY_CONTRACT)
    state = load_json(STATE_CONTRACT)
    movement_interface = load_json(WAVE2_MOVEMENT)
    scene = load_json(WAVE2_SCENE)
    contract = build_movement_contract(actor_map, identity, state, movement_interface, scene, form_text)
    fixture = build_fixture(contract)
    source_paths = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        IDENTITY_CONTRACT,
        IDENTITY_MANIFEST,
        STATE_CONTRACT,
        STATE_MANIFEST,
        WAVE2_MOVEMENT,
        WAVE2_SCENE,
    ]
    manifest = {
        "schema_version": "wave3-c3-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C3-target-position-and-adapter-movement",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_paths},
        "artifact_inputs": [rel(ACTOR_MAP), rel(IDENTITY_CONTRACT), rel(STATE_CONTRACT), rel(WAVE2_MOVEMENT), rel(WAVE2_SCENE)],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_movement_contract.json",
            "Phases/Phase4/artifacts/wave3_movement_fixture.json",
            "Phases/Phase4/artifacts/wave3_c3_build_manifest.json",
        ],
        "artifact_summary": {
            "target_field_count": contract["summary"]["target_field_count"],
            "position_field_count": contract["summary"]["position_field_count"],
            "raw_flow_step_count": contract["summary"]["raw_flow_step_count"],
            "scenario_count": len(fixture["scenarios"]),
            "legacy_movement_semantics": contract["summary"]["legacy_movement_semantics"],
            "semantic_status": contract["summary"]["status"],
        },
        "status": "W3-C3-built_raw_target_flow_and_adapter_fixture_legacy_semantics_open",
    }
    return {
        ARTIFACTS / "wave3_movement_contract.json": contract,
        ARTIFACTS / "wave3_movement_fixture.json": fixture,
        ARTIFACTS / "wave3_c3_build_manifest.json": manifest,
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
