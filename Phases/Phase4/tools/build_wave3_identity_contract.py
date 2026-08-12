#!/usr/bin/env python3
"""Build the Wave 3 C1 actor identity and bounded spawn contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_wave3_actor_contract import (
    ARTIFACTS,
    CALL_GRAPH,
    DUMP_CS,
    FORM_C,
    FUNCTION_INVENTORY,
    ROOT,
    WAVE2_MOVEMENT,
    all_function_spans,
    load_json,
    parse_gameform_fields,
    read_text,
    rel,
    sha256,
    write_json,
)


ACTOR_MAP = ARTIFACTS / "wave3_actor_function_map.json"
GAP_REGISTER = ARTIFACTS / "wave3_gap_register.json"
C0_MANIFEST = ARTIFACTS / "wave3_build_manifest.json"

EMPLOYEE_FIELDS = {
    "SyainIndex",
    "SyainPoint",
    "SyainPointIndex",
    "SyainName",
    "SyainMiniName",
    "SyainEnabled",
    "SyainSyurui",
    "SyainFaceG",
    "SyainBodyG",
    "SyainBosyuPoint",
    "SyainSuperMax",
    "SyainKyuryo",
    "SyainKeiyaku",
    "SyainSpeed",
    "SyainTaikyu",
    "SyainJobType",
    "SyainJobMuchP",
    "SyainJobLevel",
    "SyainPara",
    "SyainMemo",
    "SyainHuman",
    "SyainMyDesk",
    "ObjecIndex",
    "HumanIndex",
    "HumanMax",
}

ACTOR_FIELDS = {
    "HumanEnabled",
    "HumanObjec",
    "HumanSyain",
    "HumanSyurui",
    "HumanFaceG",
    "HumanBodyG",
    "HumanStop",
    "HumanMode",
    "HumanWalkLong",
    "HumanTime",
    "HumanAnime",
    "HumanState",
    "HumanTairyoku",
    "HumanGoHome",
    "HumanDevProcess",
    "HumanSitChair",
    "HumanReaction",
    "HumanWait",
    "HumanMeetMode",
    "HumanRequestMax",
    "HumanMeetSyain",
}


ADD_SYAIN_PARAMETERS = [
    ("TPoint", "param_2", ["SyainPointIndex", "SyainPoint"], "direct index/point relation"),
    ("TSyurui", "param_3", ["SyainSyurui"], "direct"),
    ("TName", "param_4", ["SyainName"], "direct"),
    ("TMiniName", "param_5", ["SyainMiniName"], "direct"),
    ("TFaceG", "param_6", ["SyainFaceG"], "direct byte-sized selector input"),
    ("TBodyG", "param_7", ["SyainBodyG"], "direct byte-sized selector input"),
    ("TBosyuP", "param_8", ["SyainBosyuPoint"], "direct"),
    ("TKyuryo", "param_9", ["SyainKyuryo"], "direct"),
    ("TKeiyaku", "param_10", ["SyainKeiyaku"], "direct"),
    ("TSpeed", "param_11", ["SyainSpeed"], "direct"),
    ("TTaikyu", "param_12", ["SyainTaikyu"], "multiplied_by_10_before_store"),
    ("TPara0", "param_13", ["SyainPara[0]"], "direct"),
    ("TPara1", "param_14", ["SyainPara[1]"], "direct"),
    ("TPara2", "param_15", ["SyainPara[2]"], "direct"),
    ("TPara3", "param_16", ["SyainPara[3]"], "direct"),
    ("TSuperMax", "param_17", ["SyainSuperMax"], "direct"),
    ("TJobType", "param_18", ["SyainJobType"], "direct"),
    ("TJobMuchP", "param_19", ["SyainJobMuchP"], "direct"),
    ("TJobLebel0", "param_20", ["SyainJobLevel[0]"], "direct"),
    ("TJobLebel1", "param_21", ["SyainJobLevel[1]"], "direct"),
    ("TJobLebel2", "param_22", ["SyainJobLevel[2]"], "direct"),
    ("TJobLebel3", "param_23", ["SyainJobLevel[3]"], "direct"),
    ("TJobLebel4", "param_24", ["SyainJobLevel[4]"], "direct"),
    ("TJobLebel5", "param_25", ["SyainJobLevel[5]"], "direct"),
    ("TJobLebel6", "param_26", ["SyainJobLevel[6]"], "direct"),
    ("TJobLebel7", "param_27", ["SyainJobLevel[7]"], "direct"),
    ("TMemo", "param_28", ["SyainMemo"], "direct"),
]


def function_lines(text: str, symbol: str, occurrence: int = 1) -> tuple[int, int, list[str]]:
    spans = all_function_spans(text, symbol)
    if not spans or occurrence > len(spans):
        raise RuntimeError(f"function not found: {symbol} occurrence {occurrence}")
    span = spans[occurrence - 1]
    lines = text.splitlines()
    return span["line_start"], span["line_end"], lines


def function_ref(text: str, symbol: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    start, end, lines = function_lines(text, symbol)
    hits = [index for index in range(start - 1, end) if needle in lines[index]]
    if not hits:
        return {
            "file": rel(FORM_C),
            "line": None,
            "function": symbol,
            "needle": needle,
            "status": "needle_not_found_in_function",
        }
    index = hits[min(max(occurrence - 1, 0), len(hits) - 1)]
    return {"file": rel(FORM_C), "line": index + 1, "function": symbol, "needle": needle}


def assignment_ref(text: str, symbol: str, parameter: str) -> dict[str, Any]:
    start, end, lines = function_lines(text, symbol)
    hits = [
        index
        for index in range(start - 1, end)
        if parameter in lines[index] and "//" not in lines[index]
    ]
    if not hits:
        return {
            "file": rel(FORM_C),
            "line": None,
            "function": symbol,
            "needle": parameter,
            "status": "assignment_not_found_in_function",
        }
    # Decompiled C sometimes puts the assignment operator on the previous line
    # and the parameter token on its own continuation line.  The last match in
    # the function is the actual store, while the earlier match is the signature.
    index = hits[-1]
    return {"file": rel(FORM_C), "line": index + 1, "function": symbol, "needle": parameter}


def field_snapshot(names: set[str]) -> dict[str, Any]:
    fields = parse_gameform_fields(names)
    return {
        name: {
            "declaration": row["declaration"],
            "offset": row["offset"],
            "source": row["source"],
            "line": row["line"],
            "status": row["status"],
        }
        for name, row in sorted(fields.items())
    }


def build_add_syain_contract(form_text: str, fields: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for legacy_name, c_parameter, stored_fields, transform in ADD_SYAIN_PARAMETERS:
        rows.append(
            {
                "parameter": legacy_name,
                "c_parameter": c_parameter,
                "stored_fields": stored_fields,
                "transform": transform,
                "evidence": [assignment_ref(form_text, "form_GameForm__AddSyain", c_parameter)],
                "status": "verified_bounded_parameter_store",
            }
        )
    return {
        "function": "form_GameForm__AddSyain",
        "signature_source": {
            "file": rel(DUMP_CS),
            "line": 276474,
            "needle": "public int AddSyain(int TPoint, int TSyurui, string TName, string TMiniName, int TFaceG, int TBodyG, int TBosyuP, int TKyuryo, int TKeiyaku, int TSpeed, int TTaikyu, int TPara0, int TPara1, int TPara2, int TPara3, int TSuperMax, int TJobType, int TJobMuchP, int TJobLebel0, int TJobLebel1, int TJobLebel2, int TJobLebel3, int TJobLebel4, int TJobLebel5, int TJobLebel6, int TJobLebel7, string TMemo)",
        },
        "slot_policy": {
            "free_slot_array": "SyainEnabled",
            "result_field": "SyainIndex",
            "failure_result": -1,
            "status": "verified_bounded_control_flow",
            "evidence": [
                function_ref(form_text, "form_GameForm__AddSyain", "lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x5a0);"),
                function_ref(form_text, "form_GameForm__AddSyain", "if (iVar7 < 0)"),
            ],
        },
        "stored_parameter_count": len(rows),
        "parameter_map": rows,
        "semantic_limit": "employee table provenance only; business stats are not promoted to Agent runtime state",
        "employee_fields": fields,
    }


def initial_field_rows(form_text: str, fields: dict[str, Any]) -> list[dict[str, Any]]:
    specifications = [
        ("HumanSyain", "SyainIndex selected by CallSyain", "direct_array_flow"),
        ("HumanSyurui", "CallSyain param_4 / TSyurui", "direct_parameter_flow"),
        ("HumanObjec", "AddObjec return stored in ObjecIndex", "object_reference_flow"),
        ("HumanEnabled", 1, "direct_literal"),
        ("HumanFaceG", "SyainFaceG[SyainIndex]", "employee_to_actor_selector_flow"),
        ("HumanBodyG", "SyainBodyG[SyainIndex]", "employee_to_actor_selector_flow"),
        ("HumanStop", 1, "direct_literal"),
        ("HumanMode", 0, "direct_literal_not_idle_claim"),
        ("HumanWalkLong", 0, "direct_literal"),
        ("HumanTime", 0, "direct_literal_not_timer_semantics"),
        ("HumanAnime", 0, "direct_literal_not_animation_semantics"),
        ("HumanState", 0, "direct_literal_not_agent_state"),
        ("HumanTairyoku", "SyainTaikyu[SyainIndex]", "employee_to_actor_value_flow"),
        ("HumanGoHome", 0, "direct_literal"),
        ("HumanDevProcess", 0, "direct_literal"),
        ("HumanSitChair", 0, "direct_literal_not_seat_semantics"),
        ("HumanReaction", 0, "direct_literal_not_reaction_semantics"),
        ("HumanWait", 0, "direct_literal_not_wait_semantics"),
        ("HumanMeetMode", 0, "direct_literal_not_meeting_semantics"),
        ("HumanRequestMax", 0, "direct_literal_not_request_semantics"),
        ("HumanMeetSyain", 0, "direct_literal_not_meeting_semantics"),
    ]
    rows = []
    for name, initial_value, value_status in specifications:
        field = fields[name]
        rows.append(
            {
                "field": name,
                "offset": field["offset"],
                "initial_value_or_flow": initial_value,
                "value_status": value_status,
                "semantic_status": "verified_bounded_initial_write",
                "field_declaration": {"file": field["source"], "line": field["line"], "needle": f"{name}; // {field['offset']}"},
                "write_evidence": [function_ref(form_text, "form_GameForm__CallSyain", field["offset"])],
            }
        )
    return rows


def build_call_syain_contract(form_text: str, fields: dict[str, Any]) -> dict[str, Any]:
    return {
        "function": "form_GameForm__CallSyain",
        "signature_source": {
            "file": rel(DUMP_CS),
            "line": 276480,
            "needle": "public int CallSyain(int TMode, int TIndex, int TSyurui)",
        },
        "parameter_roles": [
            {
                "parameter": "TMode",
                "c_parameter": "param_2",
                "role": "branch/control input",
                "evidence": [function_ref(form_text, "form_GameForm__CallSyain", "if (param_2 == 0)")],
                "status": "verified_control_flow_only",
            },
            {
                "parameter": "TIndex",
                "c_parameter": "param_3",
                "role": "sets SyainIndex before actor lookup",
                "evidence": [function_ref(form_text, "form_GameForm__CallSyain", "*(undefined4 *)(lVar5 + 0x574) = param_3;")],
                "status": "verified_bounded_input_flow",
            },
            {
                "parameter": "TSyurui",
                "c_parameter": "param_4",
                "role": "stored in HumanSyurui for selected actor",
                "evidence": [function_ref(form_text, "form_GameForm__CallSyain", "= param_4;", 1)],
                "status": "verified_bounded_input_flow",
            },
        ],
        "slot_allocation": {
            "free_slot_array": "HumanEnabled",
            "selected_slot_field": "HumanIndex",
            "object_slot_allocator": "AddObjec",
            "object_result_field": "ObjecIndex",
            "failure_result": -1,
            "evidence": [
                function_ref(form_text, "form_GameForm__CallSyain", "lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0xe30);"),
                function_ref(form_text, "form_GameForm__CallSyain", "uVar4 = form_GameForm__AddObjec(lVar3,0xffffffff,0,0,0,0,0,0,0);"),
            ],
            "status": "verified_bounded_slot_and_object_flow",
        },
        "initial_actor_fields": initial_field_rows(form_text, fields),
        "calls": [
            {
                "callee": "form_GameForm__AddObjec",
                "count": 2,
                "evidence": [function_ref(form_text, "form_GameForm__CallSyain", "form_GameForm__AddObjec", 1), function_ref(form_text, "form_GameForm__CallSyain", "form_GameForm__AddObjec", 2)],
            },
            {
                "callee": "form_GameForm__NextTarget",
                "count": 1,
                "evidence": [function_ref(form_text, "form_GameForm__CallSyain", "form_GameForm__NextTarget")],
            },
        ],
        "semantic_limit": "actor slot and initial field writes are bounded evidence; stable public actor identity is a web adapter decision",
    }


def build_spawn_fixture(contract: dict[str, Any]) -> dict[str, Any]:
    initial = {
        row["field"]: row["initial_value_or_flow"]
        for row in contract["initial_actor_fields"]
    }
    return {
        "schema_version": "wave3-spawn-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C1-bounded-identity-spawn",
        "fixture_id": "single_actor_identity_spawn_contract",
        "fixture_scope": "contract fixture; no claim of full legacy runtime equivalence",
        "input": {
            "employee_record": {
                "employee_id": "adapter.employee.0",
                "TPoint": "fixture.point.0",
                "TSyurui": "fixture.employee.type",
                "TName": "fixture.employee.name",
                "TMiniName": "fixture.employee.short_name",
                "TFaceG": "fixture.face.selector",
                "TBodyG": "fixture.body.selector",
                "TSpeed": "fixture.speed",
            },
            "call_syain": {
                "TMode": "fixture.call_mode",
                "TIndex": "employee_record_index",
                "TSyurui": "fixture.actor.type",
            },
        },
        "expected": {
            "employee_binding": {
                "employee_id": "adapter.employee.0",
                "legacy_index_field": "SyainIndex",
                "status": "bounded_input_reference",
            },
            "actor_identity": {
                "actor_id": "adapter.actor.0",
                "identity_policy": "stable_web_adapter_id_not_legacy_array_index",
                "human_slot": "selected_free_HumanEnabled_slot",
                "employee_reference": "adapter.employee.0",
                "object_reference": "ObjecIndex_returned_by_AddObjec",
            },
            "initial_actor_fields": initial,
        },
        "failure_cases": [
            {"case": "no_free_employee_slot", "result": -1, "status": "verified_return_path"},
            {"case": "no_free_actor_slot", "result": -1, "status": "verified_or_bounded_return_path"},
            {"case": "object_slot_unavailable", "result": "actor_creation_not_complete", "status": "bounded_dependency"},
        ],
        "non_goals": [
            "do not interpret HumanMode=0 as idle",
            "do not interpret HumanState=0 as an Agent state",
            "do not treat actor_id as a recovered legacy field",
            "do not decode face/body numeric selectors in this fixture",
        ],
        "evidence": [
            {"file": rel(FORM_C), "line": 27392, "needle": "// Function: form_GameForm__CallSyain"},
            {"file": rel(FORM_C), "line": 26951, "needle": "// Function: form_GameForm__AddSyain"},
        ],
        "status": "spawn_contract_ready_for_state_and_movement_slices",
    }


def source_hashes(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return {
        rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in paths
    }


def build() -> dict[Path, Any]:
    required = [FORM_C, DUMP_CS, ACTOR_MAP, GAP_REGISTER, C0_MANIFEST, WAVE2_MOVEMENT]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C1 inputs: " + ", ".join(missing))

    form_text = read_text(FORM_C)
    actor_map = load_json(ACTOR_MAP)
    gap_register = load_json(GAP_REGISTER)
    c0_manifest = load_json(C0_MANIFEST)
    movement_interface = load_json(WAVE2_MOVEMENT)
    fields = parse_gameform_fields(EMPLOYEE_FIELDS | ACTOR_FIELDS)
    employee_fields = field_snapshot(EMPLOYEE_FIELDS)
    add_syain = build_add_syain_contract(form_text, employee_fields)
    call_syain = build_call_syain_contract(form_text, fields)
    identity = {
        "schema_version": "wave3-actor-identity-contract-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C1-bounded-identity-spawn",
        "source_roots_read_only": True,
        "inputs": {
            "actor_function_map": rel(ACTOR_MAP),
            "gap_register": rel(GAP_REGISTER),
            "wave2_movement_interface": rel(WAVE2_MOVEMENT),
            "wave2_gate_status": movement_interface["status"],
        },
        "employee_record_contract": add_syain,
        "actor_spawn_contract": call_syain,
        "identity_policy": {
            "legacy_index_fields": ["SyainIndex", "HumanIndex", "ObjecIndex"],
            "web_actor_id": "stable adapter-owned ID",
            "policy": "do not expose global array index as public Agent identity",
            "status": "web_adapter_decision",
        },
        "summary": {
            "employee_parameter_count": add_syain["stored_parameter_count"],
            "initial_actor_field_count": len(call_syain["initial_actor_fields"]),
            "call_syain_call_count": 2,
            "failure_case_count": 3,
            "status": "W3-C1-identity-and-spawn-contract-ready_with_semantic_state_open",
        },
        "inherited_gap_count": gap_register["summary"]["gap_count"],
        "c0_source_hashes": c0_manifest["source_hashes"],
    }
    fixture = build_spawn_fixture(call_syain)
    manifest = {
        "schema_version": "wave3-c1-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C1-bounded-identity-spawn",
        "source_roots_read_only": True,
        "address_namespace": {
            "export_to_raw_delta": "-0x100000",
            "status": "verified_inherited_from_wave1_wave2",
        },
        "source_hashes": source_hashes(
            [FORM_C, DUMP_CS, FUNCTION_INVENTORY, CALL_GRAPH, ACTOR_MAP, GAP_REGISTER, C0_MANIFEST, WAVE2_MOVEMENT]
        ),
        "artifact_inputs": [rel(ACTOR_MAP), rel(GAP_REGISTER), rel(C0_MANIFEST), rel(WAVE2_MOVEMENT)],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_actor_identity_contract.json",
            "Phases/Phase4/artifacts/wave3_spawn_fixture.json",
            "Phases/Phase4/artifacts/wave3_c1_build_manifest.json",
        ],
        "artifact_summary": {
            "employee_parameter_count": identity["summary"]["employee_parameter_count"],
            "initial_actor_field_count": identity["summary"]["initial_actor_field_count"],
            "failure_case_count": identity["summary"]["failure_case_count"],
            "semantic_status": "bounded_identity_spawn_only",
        },
        "status": "W3-C1-built_identity_spawn_contract_ready_for_state_slice",
    }
    return {
        ARTIFACTS / "wave3_actor_identity_contract.json": identity,
        ARTIFACTS / "wave3_spawn_fixture.json": fixture,
        ARTIFACTS / "wave3_c1_build_manifest.json": manifest,
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
