#!/usr/bin/env python3
"""Build the Wave 3 C4 raw furniture relation audit and seat adapter fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_wave3_actor_contract import (
    ARTIFACTS,
    DUMP_CS,
    FORM_C,
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
STATE_CONTRACT = ARTIFACTS / "wave3_actor_state_contract.json"
STATE_MANIFEST = ARTIFACTS / "wave3_c2_build_manifest.json"
MOVEMENT_CONTRACT = ARTIFACTS / "wave3_movement_contract.json"
WAVE2_FURNITURE = ARTIFACTS / "wave2_furniture_contract.json"
WAVE2_MOVEMENT = ARTIFACTS / "wave2_wave3_movement_interface.json"

RELATION_FIELDS = [
    "HumanSitChair",
    "DeskSyain",
    "DeskObjec",
    "ChairMainObjec",
    "ChairSubObjec",
    "PCObjec",
    "DeskZahyou",
]


def function_ref(
    text: str,
    symbol: str,
    needle: str,
    start_line: int | None = None,
    end_line: int | None = None,
) -> dict[str, Any]:
    spans = all_function_spans(text, symbol)
    if not spans:
        raise RuntimeError(f"function not found: {symbol}")
    span = spans[0]
    lines = text.splitlines()
    start = max(span["line_start"], start_line or span["line_start"])
    end = min(span["line_end"], end_line or span["line_end"])
    hits = [index for index in range(start - 1, end) if needle in lines[index]]
    if not hits:
        return {
            "file": rel(FORM_C),
            "line": None,
            "function": symbol,
            "needle": needle,
            "status": "needle_not_found_in_function",
        }
    return {"file": rel(FORM_C), "line": hits[0] + 1, "function": symbol, "needle": needle}


def field_snapshot(actor_map: dict[str, Any]) -> dict[str, Any]:
    fields = parse_gameform_fields(set(RELATION_FIELDS))
    mapped_fields = actor_map["scope"]["field_map"]
    return {
        name: {
            "offset": fields[name]["offset"],
            "declaration": {
                "file": fields[name]["source"],
                "line": fields[name]["line"],
                "needle": f"{name}; // {fields[name]['offset']}",
            },
            "scoped_reference_count": mapped_fields[name]["offset_reference_count_in_scoped_functions"],
            "scoped_reference_functions": mapped_fields[name]["offset_reference_functions"],
            "status": "verified_dump_field_declaration_raw_relation_role_open",
        }
        for name in RELATION_FIELDS
    }


def build_raw_relation_traces(form_text: str) -> list[dict[str, Any]]:
    return [
        {
            "trace_id": "actor_seat_index_consumed_by_main_process",
            "function": "form_GameForm__MainProcess",
            "line_range": [12883, 12991],
            "raw_inputs": ["HumanMode[slot]", "HumanTime[slot]", "HumanSitChair[slot]", "ChairMainObjec[chair]"],
            "raw_mutations": [
                "HumanTime[slot] += 1 when HumanMode[slot] == 5",
                "raw relation array at offset 0x2c8[ChairMainObjec[HumanSitChair[slot]]] = -3 when HumanTime == 1",
                "raw relation array at offset 0x2d0[ChairMainObjec[HumanSitChair[slot]]] = -1 when HumanTime == 1",
            ],
            "occupancy_state": None,
            "status": "verified_raw_index_and_relation_flow_occupancy_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "if (*(int *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) == 5)", 12881, 12890),
                function_ref(form_text, "form_GameForm__MainProcess", "*(int *)(lVar27 + 0x20) = *(int *)(lVar27 + 0x20) + 1;", 12890, 12900),
                function_ref(form_text, "form_GameForm__MainProcess", "lVar24 = *(long *)(lVar24 + 0xe98);", 12890, 12910),
                function_ref(form_text, "form_GameForm__MainProcess", "= 0xfffffffd;", 12960, 12995),
            ],
            "semantic_limits": [
                "HumanSitChair is an observed index/reference flow, not proof of seat ownership",
                "0x2c8/0x2d0 fields are outside the named actor relation map",
            ],
        },
        {
            "trace_id": "actor_seat_stage_2_and_3_relation_updates",
            "function": "form_GameForm__MainProcess",
            "line_range": [12997, 13355],
            "raw_inputs": ["HumanTime[slot]", "HumanSitChair[slot]", "ChairMainObjec[chair]", "ChairSubObjec[chair]"],
            "raw_mutations": [
                "raw relation array values 2/1/3 are written for HumanTime 2 and 3 branches",
                "raw relation array values 0/0 are written for HumanTime 4 branch",
                "bVar14 is set by the branch and is not resolved here",
            ],
            "occupancy_state": None,
            "status": "verified_raw_stage_branches_occupancy_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "if (*(int *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) == 2)", 12997, 13010),
                function_ref(form_text, "form_GameForm__MainProcess", "if (*(int *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) == 3)", 13030, 13045),
                function_ref(form_text, "form_GameForm__MainProcess", "lVar24 = *(long *)(lVar24 + 0x468);", 13230, 13245),
                function_ref(form_text, "form_GameForm__MainProcess", "bVar14 = true;", 13340, 13360),
            ],
            "semantic_limits": [
                "numeric HumanTime values are raw branch guards, not named seat lifecycle states",
                "ChairMainObjec/ChairSubObjec presence does not prove occupancy",
            ],
        },
        {
            "trace_id": "desk_slot_scan_and_assignment",
            "function": "form_GameForm__CallHikkosi",
            "line_range": [25509, 25534],
            "raw_inputs": ["DeskSyain", "relation array at offset 0x6c8", "relation array at offset 0x610"],
            "raw_mutations": [
                "scan DeskSyain for -1 slot",
                "DeskSyain[free_slot] = source relation value",
                "relation array at offset 0x610[source] = free_slot",
            ],
            "occupancy_state": None,
            "status": "verified_bounded_desk_relation_flow_occupancy_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__CallHikkosi", "lVar15 = *(long *)(*(long *)(lVar8 + 0xb8) + 0x450);", 25505, 25515),
                function_ref(form_text, "form_GameForm__CallHikkosi", "if (*(int *)(lVar15 + (long)(int)uVar18 * 4 + 0x20) == -1)", 25505, 25515),
                function_ref(form_text, "form_GameForm__CallHikkosi", "*(undefined4 *)(lVar21 + (long)(int)uVar18 * 4 + 0x20)", 25520, 25530),
                function_ref(form_text, "form_GameForm__CallHikkosi", "*(uint *)(lVar16 + (long)(int)uVar22 * 4 + 0x20) = uVar18;", 25529, 25536),
            ],
            "semantic_limits": [
                "the source proves a slot scan/assignment relation, not a seat occupancy API",
                "source relation arrays are not exposed as stable web identity",
            ],
        },
        {
            "trace_id": "actor_desk_relation_reset_on_call_syain",
            "function": "form_GameForm__CallSyain",
            "line_range": [27850, 27875],
            "raw_inputs": ["SyainIndex", "relation array at offset 0x610", "DeskSyain"],
            "raw_mutations": [
                "DeskSyain[relation] = -1",
                "raw array at offset 0x2e0[employee] = 0",
                "raw array at offset 0xe30[employee] = 0",
            ],
            "occupancy_state": None,
            "status": "verified_bounded_relation_clear_occupancy_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__CallSyain", "lVar7 = *(long *)(lVar5 + 0x610);", 27848, 27855),
                function_ref(form_text, "form_GameForm__CallSyain", "lVar3 = *(long *)(lVar5 + 0x450);", 27854, 27862),
                function_ref(form_text, "form_GameForm__CallSyain", "= 0xffffffff;", 27854, 27862),
                function_ref(form_text, "form_GameForm__CallSyain", "= 0;", 27860, 27875),
            ],
            "semantic_limits": [
                "clearing a raw relation is not mapped to adapter release without an owner contract",
                "no seat_id/public actor_id is present in this source slice",
            ],
        },
        {
            "trace_id": "draw_object_furniture_relations",
            "function": "form_GameForm__DrawObj",
            "line_range": [16860, 17020],
            "raw_inputs": ["HumanSyurui", "PCObjec", "DeskZahyou", "object coordinate arrays"],
            "raw_mutations": [],
            "occupancy_state": None,
            "status": "verified_render_relation_not_occupancy",
            "evidence": [
                function_ref(form_text, "form_GameForm__DrawObj", "lVar23 = *(long *)(lVar22 + 0x470);", 16860, 16875),
                function_ref(form_text, "form_GameForm__DrawObj", "lVar22 = *(long *)(lVar35 + 0x478);", 17000, 17015),
            ],
            "semantic_limits": [
                "PCObjec and DeskZahyou are used in a draw path here, not as occupancy proof",
                "sprite presence and coordinate lookup are not seat ownership",
            ],
        },
    ]


def build_relation_roles(furniture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "field": "HumanSitChair",
            "role": "actor_to_chair_index_or_relation_candidate",
            "status": "raw_index_flow_verified_occupancy_not_closed",
            "legacy_equivalence": False,
        },
        {
            "field": "DeskSyain",
            "role": "desk_slot_to_source_relation_array",
            "status": "bounded_scan_assignment_clear_verified",
            "legacy_equivalence": False,
        },
        {
            "field": "DeskObjec",
            "role": "desk_to_object_relation_candidate",
            "status": "wave2_accessor_relation_only",
            "legacy_equivalence": False,
        },
        {
            "field": "ChairMainObjec",
            "role": "chair_main_object_relation_indexed_by_HumanSitChair",
            "status": "raw_consumer_verified_occupancy_not_closed",
            "legacy_equivalence": False,
        },
        {
            "field": "ChairSubObjec",
            "role": "chair_sub_object_relation_indexed_by_HumanSitChair",
            "status": "raw_consumer_verified_occupancy_not_closed",
            "legacy_equivalence": False,
        },
        {
            "field": "PCObjec",
            "role": "pc_object_relation_used_by_draw_path",
            "status": "render_relation_verified_occupancy_not_closed",
            "legacy_equivalence": False,
        },
        {
            "field": "DeskZahyou",
            "role": "desk_coordinate_data_used_by_draw_path",
            "status": "coordinate_relation_verified_occupancy_not_closed",
            "legacy_equivalence": False,
        },
        {
            "field": "seat_occupancy_state",
            "role": "explicit_web_adapter_relation",
            "status": "web_adapter_decision",
            "legacy_equivalence": False,
            "source_boundary": furniture["seat_contract"]["web_adapter_policy"],
        },
    ]


def build_adapter_contract(movement: dict[str, Any], movement_interface: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "web_adapter_decision",
        "legacy_equivalence": False,
        "operations": {
            "occupy": {
                "inputs": ["agent_id", "seat_id", "optional_furniture_object_id"],
                "outputs": ["occupied", "conflict", "unavailable"],
                "rule": "one owner per seat; conflict does not mutate existing owner",
            },
            "release": {
                "inputs": ["agent_id", "seat_id"],
                "outputs": ["released", "not_owner", "unavailable"],
                "rule": "only current owner may release; unavailable preserves known state",
            },
            "query": {
                "inputs": ["seat_id"],
                "outputs": ["free", "occupied", "unavailable"],
                "rule": "query is explicit state and never derived from chair image presence",
            },
        },
        "movement_dependencies": {
            "path": movement["provider_contract"]["path"],
            "collision": movement["provider_contract"]["collision"],
            "seat_boundary": movement_interface["seat"],
        },
        "conflict_policy": [
            "occupied seat returns conflict and preserves owner",
            "disabled actor cannot newly occupy; existing ownership requires explicit release policy",
            "cancelled path does not implicitly occupy or release",
            "legacy raw relation clear does not implicitly call adapter release",
        ],
    }


def build_contract(
    actor_map: dict[str, Any],
    furniture: dict[str, Any],
    movement: dict[str, Any],
    movement_interface: dict[str, Any],
    form_text: str,
) -> dict[str, Any]:
    return {
        "schema_version": "wave3-interaction-contract-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C4-furniture-seat-interaction-boundary",
        "source_roots_read_only": True,
        "inputs": {
            "actor_function_map": rel(ACTOR_MAP),
            "wave2_furniture_contract": rel(WAVE2_FURNITURE),
            "wave2_movement_interface": rel(WAVE2_MOVEMENT),
            "movement_contract": rel(MOVEMENT_CONTRACT),
        },
        "raw_field_snapshot": field_snapshot(actor_map),
        "relation_roles": build_relation_roles(furniture),
        "raw_relation_traces": build_raw_relation_traces(form_text),
        "adapter_contract": build_adapter_contract(movement, movement_interface),
        "not_claimed": [
            "HumanSitChair is not automatically an occupied seat",
            "ChairMainObjec/ChairSubObjec presence is not occupancy proof",
            "DeskSyain raw slot relation is not a public actor/seat identity",
            "PCObjec/DeskZahyou draw relations are not seat state",
            "raw relation clear is not implicit adapter release",
            "collision/walkable remain provider inputs and are not inferred from furniture pixels",
        ],
        "summary": {
            "relation_field_count": len(RELATION_FIELDS),
            "raw_trace_count": 5,
            "adapter_operation_count": 3,
            "legacy_occupancy_status": "not_closed",
            "collision_status": movement_interface["collision"]["legacy_status"],
            "walkable_status": movement_interface["walkable"]["legacy_status"],
            "status": "raw_furniture_relation_audit_adapter_seat_contract_ready_legacy_occupancy_open",
        },
    }


def build_fixture(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "wave3-seat-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C4-explicit-seat-occupancy",
        "fixture_id": "single_actor_seat_occupancy_boundary",
        "fixture_scope": "adapter contract fixture; no claim of legacy runtime equivalence",
        "initial": {
            "actor_id": "adapter.actor.0",
            "employee_id": "adapter.employee.0",
            "seat_id": "adapter.seat.0",
            "furniture_object_id": "adapter.chair.0",
            "raw_relation_snapshot": {"HumanSitChair": None, "ChairMainObjec": None, "ChairSubObjec": None},
        },
        "scenarios": [
            {
                "id": "occupy_free_seat",
                "input": {"operation": "occupy", "agent_id": "adapter.actor.0", "seat_id": "adapter.seat.0"},
                "expected": {"result": "occupied", "owner": "adapter.actor.0", "legacy_equivalence": False},
            },
            {
                "id": "occupied_seat_conflict",
                "input": {"operation": "occupy", "agent_id": "adapter.actor.1", "seat_id": "adapter.seat.0"},
                "precondition": {"owner": "adapter.actor.0"},
                "expected": {"result": "conflict", "owner_after": "adapter.actor.0", "legacy_equivalence": False},
            },
            {
                "id": "release_by_owner",
                "input": {"operation": "release", "agent_id": "adapter.actor.0", "seat_id": "adapter.seat.0"},
                "precondition": {"owner": "adapter.actor.0"},
                "expected": {"result": "released", "state_after": "free", "legacy_equivalence": False},
            },
            {
                "id": "release_by_non_owner",
                "input": {"operation": "release", "agent_id": "adapter.actor.1", "seat_id": "adapter.seat.0"},
                "precondition": {"owner": "adapter.actor.0"},
                "expected": {"result": "not_owner", "owner_after": "adapter.actor.0", "legacy_equivalence": False},
            },
            {
                "id": "seat_provider_unavailable",
                "input": {"operation": "occupy", "agent_id": "adapter.actor.0", "seat_id": "adapter.seat.0", "provider": "unavailable"},
                "expected": {"result": "unavailable", "state_mutation": None, "legacy_equivalence": False},
            },
            {
                "id": "raw_human_sit_chair_is_not_occupancy",
                "input": {"raw_field": "HumanSitChair", "raw_value": 0},
                "expected": {"occupancy_state": None, "status": "raw_relation_only", "adapter_operation": None},
            },
        ],
        "status": "seat_fixture_ready_explicit_occupancy_legacy_producer_open",
        "source_contract": contract["schema_version"],
    }


def build() -> dict[Path, Any]:
    required = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        IDENTITY_CONTRACT,
        STATE_CONTRACT,
        STATE_MANIFEST,
        MOVEMENT_CONTRACT,
        WAVE2_FURNITURE,
        WAVE2_MOVEMENT,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C4 inputs: " + ", ".join(missing))
    form_text = read_text(FORM_C)
    actor_map = load_json(ACTOR_MAP)
    furniture = load_json(WAVE2_FURNITURE)
    movement = load_json(MOVEMENT_CONTRACT)
    movement_interface = load_json(WAVE2_MOVEMENT)
    contract = build_contract(actor_map, furniture, movement, movement_interface, form_text)
    fixture = build_fixture(contract)
    source_paths = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        IDENTITY_CONTRACT,
        STATE_CONTRACT,
        STATE_MANIFEST,
        MOVEMENT_CONTRACT,
        WAVE2_FURNITURE,
        WAVE2_MOVEMENT,
    ]
    manifest = {
        "schema_version": "wave3-c4-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C4-furniture-seat-interaction-boundary",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_paths},
        "artifact_inputs": [rel(ACTOR_MAP), rel(WAVE2_FURNITURE), rel(WAVE2_MOVEMENT), rel(MOVEMENT_CONTRACT)],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_interaction_contract.json",
            "Phases/Phase4/artifacts/wave3_seat_fixture.json",
            "Phases/Phase4/artifacts/wave3_c4_build_manifest.json",
        ],
        "artifact_summary": {
            "relation_field_count": contract["summary"]["relation_field_count"],
            "raw_trace_count": contract["summary"]["raw_trace_count"],
            "adapter_operation_count": contract["summary"]["adapter_operation_count"],
            "scenario_count": len(fixture["scenarios"]),
            "legacy_occupancy_status": contract["summary"]["legacy_occupancy_status"],
            "semantic_status": contract["summary"]["status"],
        },
        "status": "W3-C4-built_relation_audit_and_explicit_seat_fixture_legacy_occupancy_open",
    }
    return {
        ARTIFACTS / "wave3_interaction_contract.json": contract,
        ARTIFACTS / "wave3_seat_fixture.json": fixture,
        ARTIFACTS / "wave3_c4_build_manifest.json": manifest,
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
