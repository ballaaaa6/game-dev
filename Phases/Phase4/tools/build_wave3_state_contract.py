#!/usr/bin/env python3
"""Build the Wave 3 C2 raw actor-state audit and neutral transition fixture."""

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
PHASE2_MAPPING = ROOT / "Phases" / "Phase2" / "artifacts" / "agent_state_mapping.json"

STATE_FIELDS = [
    "HumanMode",
    "HumanTime",
    "HumanStop",
    "HumanWalkLong",
    "HumanSitChair",
    "HumanReaction",
    "HumanWait",
    "HumanState",
    "HumanAnime",
    "HumanDegree",
    "HumanFukiIndex",
    "HumanFukiTime",
]


def field_rows(actor_map: dict[str, Any], identity: dict[str, Any]) -> list[dict[str, Any]]:
    field_map = actor_map["scope"]["field_map"]
    initial = {
        row["field"]: row
        for row in identity["actor_spawn_contract"]["initial_actor_fields"]
    }
    rows = []
    for name in STATE_FIELDS:
        field = field_map.get(name)
        if not field:
            raise RuntimeError(f"state field missing from W3-C0 map: {name}")
        seed = initial.get(name)
        rows.append(
            {
                "field": name,
                "offset": field["offset"],
                "declaration": {
                    "file": field["source"],
                    "line": field["line"],
                    "needle": f"{name}; // {field['offset']}",
                },
                "scoped_reference_count": field["offset_reference_count_in_scoped_functions"],
                "scoped_reference_functions": field["offset_reference_functions"],
                "reference_samples": field["offset_reference_samples"],
                "initial_seed": seed["initial_value_or_flow"] if seed else None,
                "initial_seed_status": seed["value_status"] if seed else "not_seeded_in_call_syain_slice",
                "access_kind": "offset_reference_only",
                "semantic_status": "raw_field_registered_semantic_label_not_closed",
                "policy": "do_not map raw field name or numeric seed directly to Agent state",
            }
        )
    return rows


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


def build_main_process_tick_slices(form_text: str) -> list[dict[str, Any]]:
    return [
        {
            "slice_id": "human_wait_decrement",
            "line_range": [7869, 7890],
            "guard": [
                "HumanEnabled[slot] >= 1",
                "HumanWait[slot] > 0",
            ],
            "raw_mutations": ["HumanWait[slot] = HumanWait[slot] - 1"],
            "agent_state": None,
            "timer_behavior": "decrement_by_one_raw_unit",
            "status": "verified_bounded_raw_tick",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "if (*(int *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) < 1) goto LAB_00f12e58;"),
                function_ref(form_text, "form_GameForm__MainProcess", "lVar24 = *(long *)(lVar24 + 0xea8);", 7869, 7890),
                function_ref(form_text, "form_GameForm__MainProcess", "*(int *)(lVar24 + 0x20) = *(int *)(lVar24 + 0x20) + -1;", 7869, 7890),
            ],
            "semantic_limits": [
                "HumanWait name is not promoted to an Agent wait state",
                "raw unit is not labelled milliseconds or frames",
            ],
        },
        {
            "slice_id": "raw_mode_stop_timer_reset",
            "line_range": [7945, 8020],
            "guard": [
                "raw field at offset 0xe58 equals 0",
                "raw field at offset 0xed0 equals 1",
                "raw relation values differ before the branch",
            ],
            "raw_mutations": [
                "HumanGoalPoint[slot] = bounded relation-derived value",
                "HumanMode[slot] = 0",
                "raw field at offset 0xed0 = 1",
                "HumanWalkLong[slot] = 0",
                "HumanTime[slot] = 0",
                "HumanStop[slot] = 0",
            ],
            "agent_state": None,
            "timer_behavior": "HumanTime_reset_to_zero; unit_unknown",
            "status": "verified_bounded_raw_transition_semantics_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "lVar27 = *(long *)(lVar24 + 0xe58);"),
                function_ref(form_text, "form_GameForm__MainProcess", "*(undefined4 *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) = 0;", 7990, 8020),
                function_ref(form_text, "form_GameForm__MainProcess", "*(undefined4 *)(lVar27 + (long)(int)uStack_64 * 4 + 0x20) = 1;", 7990, 8020),
            ],
            "semantic_limits": [
                "the decompiler aliases several arrays through local variables; only mapped offsets are named",
                "raw mode 0 is not labelled idle",
            ],
        },
        {
            "slice_id": "raw_state_2_to_mode_5",
            "line_range": [8219, 8264],
            "guard": [
                "HumanStop[slot] == 0",
                "HumanState[slot] == 2",
                "HumanSitChair[slot] >= 0",
            ],
            "raw_mutations": ["HumanMode[slot] = 5", "HumanState[slot] = 1"],
            "agent_state": None,
            "timer_behavior": "not_written_in_slice",
            "status": "verified_bounded_raw_transition_semantics_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "lVar27 = *(long *)(lVar24 + 0xf48);"),
                function_ref(form_text, "form_GameForm__MainProcess", "lVar27 = *(long *)(lVar24 + 0xe98);"),
                function_ref(form_text, "form_GameForm__MainProcess", "*(undefined4 *)(lVar24 + (long)(int)uStack_64 * 4 + 0x20) = 5;"),
                function_ref(form_text, "form_GameForm__MainProcess", "*(undefined4 *)(lVar24 + (long)(int)uStack_64 * 4 + 0x20) = 1;"),
            ],
            "semantic_limits": [
                "numeric mode/state values are raw IDs only",
                "HumanSitChair is not promoted to occupied-seat state from this branch alone",
            ],
        },
        {
            "slice_id": "human_anime_counter",
            "line_range": [8698, 8724],
            "guard": ["bVar14 is true or false after the preceding raw branch"],
            "raw_mutations": [
                "HumanAnime[slot] += 1 when bVar14 is true",
                "HumanAnime[slot] = 0 when bVar14 is false",
                "HumanAnime[slot] = 0 after the increment exceeds 15",
            ],
            "agent_state": None,
            "timer_behavior": "bounded_counter_threshold_15; unit_unknown",
            "status": "verified_bounded_raw_counter_semantics_open",
            "evidence": [
                function_ref(form_text, "form_GameForm__MainProcess", "lVar24 = *(long *)(lVar24 + 0xf40);"),
                function_ref(form_text, "form_GameForm__MainProcess", "*(int *)(lVar27 + 0x20) = *(int *)(lVar27 + 0x20) + 1, uVar41 <= uStack_64)"),
                function_ref(form_text, "form_GameForm__MainProcess", "if (0xf < *(int *)(lVar24 + (long)(int)uStack_64 * 4 + 0x20))"),
                function_ref(form_text, "form_GameForm__MainProcess", "*(undefined4 *)(lVar24 + 0x20) = 0;", 8698, 8725),
            ],
            "semantic_limits": [
                "HumanAnime is not assigned a specific animation meaning",
                "bVar14 provenance is outside this bounded slice",
            ],
        },
    ]


def build_transition_table(identity: dict[str, Any], phase2_mapping: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "transition_id": "raw_spawn_seed",
            "trigger": "CallSyain bounded success path",
            "guard": "free HumanEnabled slot and AddObjec result available",
            "raw_mutation": "initial Human* writes recorded in wave3_actor_identity_contract.json",
            "agent_state": None,
            "status": "verified_bounded_raw_seed",
            "legacy_equivalence": False,
            "evidence": [
                {"file": rel(FORM_C), "line": 27392, "needle": "// Function: form_GameForm__CallSyain"},
                {"file": rel(IDENTITY_CONTRACT), "line": None, "needle": "initial_actor_fields"},
            ],
        },
        {
            "transition_id": "adapter_move_requested",
            "trigger": "Wave 3 adapter receives a target and path",
            "guard": "path provider returns path",
            "raw_mutation": "raw HumanMode/HumanState writes not yet proven for this event",
            "agent_state": "walking",
            "status": "web_adapter_decision",
            "legacy_equivalence": False,
            "evidence": [
                {"file": "Phases/Phase4/artifacts/wave2_wave3_movement_interface.json", "line": None, "needle": "walk graph/grid as adapter data"},
            ],
        },
        {
            "transition_id": "adapter_move_arrived",
            "trigger": "adapter path is exhausted within arrival tolerance",
            "guard": "current position reaches target according to adapter contract",
            "raw_mutation": "raw arrival transition not closed in C0/C1 evidence",
            "agent_state": "idle",
            "status": "web_adapter_decision",
            "legacy_equivalence": False,
            "evidence": [
                {"file": "Phases/Phase4/artifacts/wave2_wave3_movement_interface.json", "line": None, "needle": "path | no_path | unavailable"},
            ],
        },
        {
            "transition_id": "dialogue_candidate_modes",
            "trigger": "Kaiwa-related DrawHuman callsite",
            "guard": "observed TMode expression is iVar % 2 + 8",
            "raw_mutation": "mode_08/mode_09 candidate only",
            "agent_state": "talking",
            "status": "probable_phase2_mapping",
            "legacy_equivalence": False,
            "evidence": [
                {"file": "Phases/Phase2/artifacts/agent_state_mapping.json", "line": None, "needle": "candidate TMode values 8 and 9"},
            ],
            "unknowns": ["timing", "loop behavior", "face-change timing", "whether 8/9 are talking loop"],
        },
    ]


def build_state_contract(
    actor_map: dict[str, Any], identity: dict[str, Any], phase2_mapping: dict[str, Any], form_text: str
) -> dict[str, Any]:
    fields = field_rows(actor_map, identity)
    transitions = build_transition_table(identity, phase2_mapping)
    tick_slices = build_main_process_tick_slices(form_text)
    return {
        "schema_version": "wave3-actor-state-contract-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C2-raw-state-audit",
        "source_roots_read_only": True,
        "state_namespaces": [
            {"name": "raw_legacy_field", "meaning": "Human* field/offset observed in dump/source", "status": "evidence_only"},
            {"name": "raw_mode_id", "meaning": "numeric HumanMode or TMode value", "status": "evidence_only"},
            {"name": "agent_state", "meaning": "Virtual office state used by adapter/runtime", "status": "must_be_verified_or_explicit_adapter_decision"},
            {"name": "animation_id", "meaning": "BodyFace/frame selection namespace", "status": "separate_from_agent_state"},
        ],
        "raw_state_fields": fields,
        "transition_table": transitions,
        "main_process_tick_slices": tick_slices,
        "phase2_mapping_baseline": {
            "source": "Phases/Phase2/artifacts/agent_state_mapping.json",
            "coverage": phase2_mapping["coverage"],
            "policy": phase2_mapping["policy"],
            "status": "retained_without_semantic_promotion",
        },
        "main_process_boundary": {
            "function": "form_GameForm__MainProcess",
            "source": rel(FORM_C),
            "line_start": 1,
            "line_end": 15354,
            "scope": "only actor field reads/writes and NextTarget callsites",
            "status": "bounded_slice_required",
        },
        "do_event_boundary": {
            "function": "form_GameForm__DoEvent",
            "source_status": "assembly_fallback_only",
            "input": "Phases/Phase4/artifacts/wave1_branch_index.json",
            "status": "semantic_trace_not_closed",
        },
        "summary": {
            "raw_state_field_count": len(fields),
            "transition_count": len(transitions),
            "verified_raw_transitions": sum(row["status"] == "verified_bounded_raw_seed" for row in transitions),
            "adapter_transitions": sum(row["status"] == "web_adapter_decision" for row in transitions),
            "probable_transitions": sum(row["status"] == "probable_phase2_mapping" for row in transitions),
            "main_process_tick_slice_count": len(tick_slices),
            "verified_raw_tick_slices": sum(row["status"].startswith("verified_bounded_raw") for row in tick_slices),
            "timer_semantics": "raw decrement/reset/counter evidence present; unit and Agent meaning open",
            "semantic_status": "raw_state_audit_ready_adapter_transitions_explicit_legacy_semantics_open",
        },
    }


def build_fixture(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "wave3-state-transition-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C2-neutral-state-transitions",
        "fixture_id": "actor_raw_seed_and_adapter_state_boundary",
        "clock": {"kind": "deterministic_adapter_clock", "frame_ms": 100, "legacy_timing_status": "unknown"},
        "scenarios": [
            {
                "id": "raw_spawn_seed",
                "input": {"transition_id": "raw_spawn_seed"},
                "expected": {"agent_state": None, "status": "verified_bounded_raw_seed"},
            },
            {
                "id": "adapter_walking",
                "input": {"transition_id": "adapter_move_requested", "path": [[0, 0], [1, 0], [2, 0]]},
                "expected": {"agent_state": "walking", "legacy_equivalence": False, "status": "web_adapter_decision"},
            },
            {
                "id": "adapter_idle_after_arrival",
                "input": {"transition_id": "adapter_move_arrived", "position": [2, 0]},
                "expected": {"agent_state": "idle", "legacy_equivalence": False, "status": "web_adapter_decision"},
            },
            {
                "id": "probable_talking_candidate",
                "input": {"transition_id": "dialogue_candidate_modes", "raw_modes": [8, 9]},
                "expected": {"agent_state": "talking", "status": "probable_phase2_mapping", "timing": None},
            },
            {
                "id": "raw_wait_decrement",
                "input": {"slice_id": "human_wait_decrement", "human_enabled": 1, "human_wait": 2},
                "expected": {"human_wait_after": 1, "agent_state": None, "status": "verified_bounded_raw_tick"},
            },
            {
                "id": "raw_state_mode_transition",
                "input": {"slice_id": "raw_state_2_to_mode_5", "human_stop": 0, "human_state": 2, "human_sit_chair": 0},
                "expected": {"raw_writes": {"HumanMode": 5, "HumanState": 1}, "agent_state": None},
            },
            {
                "id": "raw_anime_counter_boundary",
                "input": {"slice_id": "human_anime_counter", "human_anime": 15, "bVar14": True},
                "expected": {"human_anime_after": 0, "agent_state": None, "threshold": 15},
            },
        ],
        "not_claimed": [
            "HumanMode=0 is idle",
            "HumanState=0 is idle",
            "HumanAnime=0 is a specific animation",
            "adapter clock equals legacy HumanTime timing",
            "adapter walking/idle equals recovered legacy movement state",
        ],
        "source_contract": contract["schema_version"],
        "status": "neutral_state_fixture_ready_for_bounded_tick_trace",
    }


def build() -> dict[Path, Any]:
    required = [ACTOR_MAP, IDENTITY_CONTRACT, IDENTITY_MANIFEST, PHASE2_MAPPING, FORM_C, DUMP_CS]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C2 inputs: " + ", ".join(missing))
    actor_map = load_json(ACTOR_MAP)
    identity = load_json(IDENTITY_CONTRACT)
    phase2_mapping = load_json(PHASE2_MAPPING)
    form_text = read_text(FORM_C)
    contract = build_state_contract(actor_map, identity, phase2_mapping, form_text)
    fixture = build_fixture(contract)
    hashes = {
        rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in [FORM_C, DUMP_CS, ACTOR_MAP, IDENTITY_CONTRACT, IDENTITY_MANIFEST, PHASE2_MAPPING]
    }
    manifest = {
        "schema_version": "wave3-c2-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C2-raw-state-audit",
        "source_roots_read_only": True,
        "source_hashes": hashes,
        "artifact_inputs": [rel(ACTOR_MAP), rel(IDENTITY_CONTRACT), rel(IDENTITY_MANIFEST), rel(PHASE2_MAPPING)],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_actor_state_contract.json",
            "Phases/Phase4/artifacts/wave3_state_transition_fixture.json",
            "Phases/Phase4/artifacts/wave3_c2_build_manifest.json",
        ],
        "artifact_summary": {
            "raw_state_field_count": contract["summary"]["raw_state_field_count"],
            "transition_count": contract["summary"]["transition_count"],
            "verified_raw_transitions": contract["summary"]["verified_raw_transitions"],
            "adapter_transitions": contract["summary"]["adapter_transitions"],
            "probable_transitions": contract["summary"]["probable_transitions"],
            "main_process_tick_slice_count": contract["summary"]["main_process_tick_slice_count"],
            "verified_raw_tick_slices": contract["summary"]["verified_raw_tick_slices"],
            "timer_semantics": contract["summary"]["timer_semantics"],
            "semantic_status": contract["summary"]["semantic_status"],
        },
        "status": "W3-C2-built_raw_state_audit_with_semantic_gaps_open",
    }
    return {
        ARTIFACTS / "wave3_actor_state_contract.json": contract,
        ARTIFACTS / "wave3_state_transition_fixture.json": fixture,
        ARTIFACTS / "wave3_c2_build_manifest.json": manifest,
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
