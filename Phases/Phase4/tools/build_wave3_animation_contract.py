#!/usr/bin/env python3
"""Build the Wave 3 C5 selector/draw contract and deterministic draw fixture."""

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
    read_text,
    rel,
    sha256,
    write_json,
)


ACTOR_MAP = ARTIFACTS / "wave3_actor_function_map.json"
STATE_CONTRACT = ARTIFACTS / "wave3_actor_state_contract.json"
MOVEMENT_CONTRACT = ARTIFACTS / "wave3_movement_contract.json"
INTERACTION_CONTRACT = ARTIFACTS / "wave3_interaction_contract.json"
PHASE2_CODE_TRACE = ROOT / "Phases" / "Phase2" / "artifacts" / "phase2_code_trace.json"
PHASE2_ANALYSIS = ROOT / "Phases" / "Phase2" / "artifacts" / "bodyface_analysis.json"
PHASE2_ANIMATION = ROOT / "Phases" / "Phase2" / "artifacts" / "animation_manifest.json"
PHASE2_ASSETS = ROOT / "Phases" / "Phase2" / "artifacts" / "character_asset_catalog.json"
PHASE2_MAPPING = ROOT / "Phases" / "Phase2" / "artifacts" / "agent_state_mapping.json"
BODYFACE_REFERENCE = ROOT / "game-dev-story-mod_Dumped" / "bodyface_records.reference.json"


def function_ref(
    text: str,
    symbol: str,
    needle: str,
    occurrence: int = 1,
    start_line: int | None = None,
    end_line: int | None = None,
) -> dict[str, Any]:
    spans = all_function_spans(text, symbol)
    if not spans or occurrence > len(spans):
        raise RuntimeError(f"function not found: {symbol} occurrence {occurrence}")
    span = spans[occurrence - 1]
    lines = text.splitlines()
    start = max(span["line_start"], start_line or span["line_start"])
    end = min(span["line_end"], end_line or span["line_end"])
    hits = [index for index in range(start - 1, end) if needle in lines[index]]
    if not hits:
        return {
            "file": rel(FORM_C),
            "line": None,
            "function": symbol,
            "occurrence": occurrence,
            "needle": needle,
            "status": "needle_not_found_in_function",
        }
    return {
        "file": rel(FORM_C),
        "line": hits[0] + 1,
        "function": symbol,
        "occurrence": occurrence,
        "needle": needle,
    }


def asset_lookup(catalog: dict[str, Any], asset_id: str) -> dict[str, Any] | None:
    for asset in catalog["assets"]:
        if asset["asset_id"] == asset_id:
            return {
                "asset_id": asset["asset_id"],
                "source_path": asset["source_path"],
                "filename": asset["filename"],
                "dimensions": asset["dimensions"],
                "mapping_status": asset["mapping_status"],
                "confidence": asset["confidence"],
            }
    return None


def build_selector_namespaces(actor_map: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    field_map = actor_map["scope"]["field_map"]
    return [
        {
            "namespace": "legacy_draw_selector",
            "fields": ["TFace", "TBody", "TMode", "TKage"],
            "meaning": "DrawHuman call parameters",
            "status": "verified_signature_contract",
            "agent_semantics": None,
        },
        {
            "namespace": "actor_selector_source",
            "fields": ["HumanFaceG", "HumanBodyG", "HumanAnime"],
            "offsets": {name: field_map[name]["offset"] for name in ["HumanFaceG", "HumanBodyG", "HumanAnime"]},
            "meaning": "raw actor/preview selector sources observed in bounded paths",
            "status": "raw_source_only",
            "agent_semantics": None,
        },
        {
            "namespace": "raw_actor_state",
            "fields": ["HumanState", "HumanMode", "HumanDegree"],
            "offsets": {name: field_map[name]["offset"] for name in ["HumanState", "HumanMode", "HumanDegree"]},
            "meaning": "raw fields kept separate from draw selectors",
            "status": "raw_state_not_selector_mapping",
            "agent_semantics": None,
        },
        {
            "namespace": "bodyface_record",
            "fields": ["BodyFace[TMode][0..13]"],
            "meaning": "mode-indexed crop/destination/shadow record",
            "status": "verified_record_only",
            "agent_semantics": None,
        },
        {
            "namespace": "agent_state",
            "fields": [row["agent_state"] for row in state["transition_table"] if row["agent_state"]],
            "meaning": "adapter/runtime state namespace",
            "status": "separate_from_numeric_selector_and_raw_mode",
            "agent_semantics": "requires_verified_or_explicit_adapter_boundary",
        },
    ]


def build_selector_flows(form_text: str, code_trace: dict[str, Any]) -> list[dict[str, Any]]:
    human_dex = code_trace["dynamic_selector_trace"]["human_dex_draw_call"]
    return [
        {
            "flow_id": "office_drawobj_actor",
            "caller": "form_GameForm__DrawObj",
            "callee": "form_GameForm__DrawHuman",
            "selectors": {
                "TFace": "HumanFaceG[actor_or_object_index] / raw offset 0xf30",
                "TBody": "HumanBodyG[actor_or_object_index] / raw offset 0xf38",
                "TMode": "raw selector array at offset 0x300 in this callsite; not promoted to HumanMode/HumanAnime",
                "TKage": 1,
            },
            "position": "graphics/object relation arrays at the callsite; destination transform remains Wave 2 boundary",
            "status": "verified_bounded_actor_draw_callsite_selector_sources_partial",
            "evidence": [
                function_ref(form_text, "form_GameForm__DrawObj", "lVar29 = *(long *)(lVar22 + 0xf30);", 1, 16300, 16325),
                function_ref(form_text, "form_GameForm__DrawObj", "lVar30 = *(long *)(lVar22 + 0xf38);", 1, 16310, 16325),
                function_ref(form_text, "form_GameForm__DrawObj", "lVar22 = *(long *)(lVar22 + 0x300);", 1, 16315, 16325),
                function_ref(form_text, "form_GameForm__DrawObj", "form_GameForm__DrawHuman", 1, 16320, 16335),
            ],
            "semantic_limits": [
                "DrawObj callsite does not prove that the 0x300 selector is HumanMode or HumanAnime",
                "HumanState/HumanDegree are not silently mapped to TMode or direction",
            ],
        },
        {
            "flow_id": "human_dex_preview_draw",
            "caller": human_dex["callsite"]["function"],
            "callee": "form_GameForm__DrawHuman",
            "selectors": {
                "TFace": human_dex["argument_mapping"]["TFace"],
                "TBody": human_dex["argument_mapping"]["TBody"],
                "TMode": human_dex["argument_mapping"]["TMode"],
                "TKage": 1,
            },
            "position": {"X": human_dex["argument_mapping"]["X"], "Y": human_dex["argument_mapping"]["Y"]},
            "status": "verified_dynamic_selector_flow_not_agent_semantic_mapping",
            "evidence": human_dex["evidence"],
            "semantic_limits": [
                "HumanDex path is a preview/debug/catalog path in Phase 2 evidence",
                "dynamic selector flow does not establish office Agent state semantics",
            ],
        },
    ]


def build_composition_contract(
    form_text: str,
    code_trace: dict[str, Any],
    analysis: dict[str, Any],
    catalog: dict[str, Any],
) -> dict[str, Any]:
    phase2_contract = code_trace["composition_contract"]
    record = analysis["records"][0]
    raw = record["raw_record"]
    body_asset = asset_lookup(catalog, "body_3")
    face_asset = asset_lookup(catalog, "face_2")
    return {
        "status": phase2_contract["status"],
        "selector_to_image_array": phase2_contract["selector_to_image_array"],
        "drawhuman_signature": {
            "source": rel(DUMP_CS),
            "overloads": [
                {"line": 276585, "signature": "DrawHuman(Graphics g, int X, int Y, int TFace, int TBody, int TMode)"},
                {"line": 276588, "signature": "DrawHuman(Graphics g, int X, int Y, int TFace, int TBody, int TMode, int TKage)"},
            ],
            "status": "verified_dump_signature",
        },
        "bodyface_record_contract": {
            "selector": "TMode",
            "record_index": 0,
            "record_source": rel(PHASE2_ANALYSIS),
            "body": {
                "selector": "TBody",
                "image_array": "imgBody",
                "source_rect_fields": ["BodyFace[TMode][2]", "BodyFace[TMode][3]", "BodyFace[TMode][4]", "BodyFace[TMode][5]"],
                "destination_offset_fields": ["BodyFace[TMode][0]", "BodyFace[TMode][1]"],
                "record_values": {
                    "source_rect": [raw["body_src_x"], raw["body_src_y"], raw["body_width"], raw["body_height"]],
                    "destination_offset": [raw["body_dst_x"], raw["body_dst_y"]],
                },
                "asset_fixture": body_asset,
            },
            "face": {
                "selector": "TFace",
                "image_array": "imgFace",
                "source_rect_fields": ["BodyFace[TMode][8]", "BodyFace[TMode][9]", "BodyFace[TMode][10]", "BodyFace[TMode][11]"],
                "destination_offset_fields": ["BodyFace[TMode][6]", "BodyFace[TMode][7]"],
                "record_values": {
                    "source_rect": [raw["face_src_x"], raw["face_src_y"], raw["face_width"], raw["face_height"]],
                    "destination_offset": [raw["face_dst_x"], raw["face_dst_y"]],
                },
                "asset_fixture": face_asset,
            },
            "shadow": {
                "record_fields": ["BodyFace[TMode][12]", "BodyFace[TMode][13]"],
                "record_values": [raw["shadow_dst_x"], raw["shadow_dst_y"]],
                "status": "record_verified_render_rule_branch_dependent",
            },
        },
        "drawhuman_evidence": [
            function_ref(form_text, "form_GameForm__DrawHuman", "kairo_unity_ui_Graphics__DrawImage", 2, 41130, 41150),
            function_ref(form_text, "form_GameForm__DrawHuman", "kairo_unity_ui_Graphics__DrawImage", 2, 41290, 41310),
            function_ref(form_text, "form_GameForm__DrawHuman", "kairo_unity_ui_Graphics__DrawImage", 2, 41370, 41420),
        ],
        "semantic_limits": [
            "BodyFace mode records are not named idle/walking/working/sitting states",
            "direction, frame timing, loop, mirroring and universal shadow behavior remain unknown",
            "mode-dependent offset branches must remain separate from the base record offsets",
        ],
    }


def build_literal_selector_cases(code_trace: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    for call in code_trace["draw_human_calls"]:
        literal = call.get("selectors", {}).get("TFace", {}).get("literal")
        if literal not in (40, 41):
            continue
        mode_raw = call.get("selectors", {}).get("TMode", {}).get("raw")
        cases.append(
            {
                "callsite": {
                    "source": call["source"],
                    "line": call["line"],
                    "function": call["function"],
                },
                "TFace": literal,
                "TBody": call.get("selectors", {}).get("TBody", {}).get("literal"),
                "TMode_expression": mode_raw,
                "TKage": call.get("selectors", {}).get("TKage", {}).get("literal"),
                "asset_resolution_status": "extraction_missing_or_index_space_gap",
                "runtime_policy": "preserve_raw_selector_and_return_unresolved_draw_asset; do_not substitute another face",
                "semantic_status": "unknown",
            }
        )
    return cases


def build_animation_semantics(animation: dict[str, Any], mapping: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    return {
        "verified_semantic_animations": animation["coverage"]["verified_semantic_animations"],
        "probable_semantic_animations": animation["coverage"]["probable_semantic_animations"],
        "unknown_semantic_animations": animation["coverage"]["unknown_semantic_animations"],
        "talking_candidate": {
            "status": next(row["status"] for row in mapping["states"] if row["agent_state"] == "talking"),
            "raw_modes": [8, 9],
            "timing": None,
            "loop": None,
            "direction": None,
            "evidence_policy": "probable mapping only; not a verified DrawHuman animation",
        },
        "raw_anime_tick_boundary": {
            "source_contract": rel(STATE_CONTRACT),
            "threshold": 15,
            "status": "raw_counter_only",
            "meaning": None,
        },
        "unknowns": ["semantic state", "direction", "frame timing", "loop behavior", "mirroring", "face-change timing"],
    }


def build_fixture(contract: dict[str, Any], analysis: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    raw = analysis["records"][0]["raw_record"]
    body_asset = asset_lookup(catalog, "body_3")
    face_asset = asset_lookup(catalog, "face_2")
    x, y = 100, 200
    return {
        "schema_version": "wave3-draw-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C5-deterministic-selector-draw",
        "fixture_id": "single_actor_body_face_composition_boundary",
        "fixture_scope": "renderer contract fixture; no semantic animation claim",
        "scenarios": [
            {
                "id": "actor_draw_mode_0",
                "input": {"actor_id": "adapter.actor.0", "X": x, "Y": y, "TFace": 2, "TBody": 3, "TMode": 0, "TKage": 1},
                "expected": {
                    "status": "draw_command_ready",
                    "semantic_state": None,
                    "commands": [
                        {
                            "layer": "body",
                            "image_array": "imgBody",
                            "asset": body_asset,
                            "source_rect": [raw["body_src_x"], raw["body_src_y"], raw["body_width"], raw["body_height"]],
                            "destination": [x + raw["body_dst_x"], y + raw["body_dst_y"]],
                        },
                        {
                            "layer": "face",
                            "image_array": "imgFace",
                            "asset": face_asset,
                            "source_rect": [raw["face_src_x"], raw["face_src_y"], raw["face_width"], raw["face_height"]],
                            "destination": [x + raw["face_dst_x"], y + raw["face_dst_y"]],
                        },
                    ],
                    "shadow": {"record_values": [raw["shadow_dst_x"], raw["shadow_dst_y"]], "rendered": None},
                    "legacy_equivalence": False,
                },
            },
            {
                "id": "talking_candidate_draw",
                "input": {"actor_id": "adapter.actor.0", "X": x, "Y": y, "TFace": 2, "TBody": 3, "TMode": 8, "TKage": 1, "agent_state": "talking"},
                "expected": {"status": "draw_command_ready", "semantic_state": "probable_talking_candidate_only", "timing": None, "loop": None, "legacy_equivalence": False},
            },
            {
                "id": "tface_40_unresolved",
                "input": {"TFace": 40, "TBody": 23, "TMode": "raw_expression", "TKage": 1},
                "expected": {"status": "unresolved_face_asset", "raw_selector_preserved": 40, "fallback_face": None, "semantic_state": None, "legacy_equivalence": False},
            },
            {
                "id": "tface_41_unresolved",
                "input": {"TFace": 41, "TBody": 4, "TMode": "raw_expression", "TKage": 0},
                "expected": {"status": "unresolved_face_asset", "raw_selector_preserved": 41, "fallback_face": None, "semantic_state": None, "legacy_equivalence": False},
            },
            {
                "id": "raw_state_does_not_choose_mode",
                "input": {"HumanState": 2, "HumanMode": 5, "HumanAnime": 15, "TFace": 2, "TBody": 3, "TMode": 0},
                "expected": {"status": "use_explicit_draw_selectors", "state_to_selector_mapping": None, "semantic_state": None},
            },
        ],
        "not_claimed": [
            "TMode 0 is idle",
            "TMode 8/9 is verified talking animation",
            "HumanAnime is a frame index for DrawHuman",
            "TFace 40/41 maps to face_40/face_41",
            "TFace 40/41 should silently fall back to another face",
            "record order proves direction, timing or loop",
        ],
        "source_contract": contract["schema_version"],
        "status": "deterministic_draw_fixture_ready_semantic_animation_open",
    }


def build() -> dict[Path, Any]:
    required = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        STATE_CONTRACT,
        MOVEMENT_CONTRACT,
        INTERACTION_CONTRACT,
        PHASE2_CODE_TRACE,
        PHASE2_ANALYSIS,
        PHASE2_ANIMATION,
        PHASE2_ASSETS,
        PHASE2_MAPPING,
        BODYFACE_REFERENCE,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C5 inputs: " + ", ".join(missing))
    form_text = read_text(FORM_C)
    actor_map = load_json(ACTOR_MAP)
    state = load_json(STATE_CONTRACT)
    code_trace = load_json(PHASE2_CODE_TRACE)
    analysis = load_json(PHASE2_ANALYSIS)
    animation = load_json(PHASE2_ANIMATION)
    catalog = load_json(PHASE2_ASSETS)
    mapping = load_json(PHASE2_MAPPING)
    contract = {
        "schema_version": "wave3-actor-animation-contract-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C5-selector-draw-contract",
        "source_roots_read_only": True,
        "inputs": {
            "actor_function_map": rel(ACTOR_MAP),
            "state_contract": rel(STATE_CONTRACT),
            "movement_contract": rel(MOVEMENT_CONTRACT),
            "interaction_contract": rel(INTERACTION_CONTRACT),
            "phase2_code_trace": rel(PHASE2_CODE_TRACE),
            "bodyface_analysis": rel(PHASE2_ANALYSIS),
            "animation_manifest": rel(PHASE2_ANIMATION),
            "character_asset_catalog": rel(PHASE2_ASSETS),
            "agent_state_mapping": rel(PHASE2_MAPPING),
        },
        "selector_namespaces": build_selector_namespaces(actor_map, state),
        "selector_flows": build_selector_flows(form_text, code_trace),
        "composition_contract": build_composition_contract(form_text, code_trace, analysis, catalog),
        "literal_selector_cases": build_literal_selector_cases(code_trace),
        "animation_semantics": build_animation_semantics(animation, mapping, state),
        "phase2_mapping_update": {
            "updated": False,
            "reason": "C5 adds selector/render evidence but no new verified Agent semantic state, timing, loop or direction",
            "source": rel(PHASE2_MAPPING),
        },
        "summary": {
            "selector_flow_count": 2,
            "bodyface_record_count": analysis["record_count"],
            "verified_semantic_animations": animation["coverage"]["verified_semantic_animations"],
            "probable_semantic_animations": animation["coverage"]["probable_semantic_animations"],
            "tface_40_41_case_count": len(build_literal_selector_cases(code_trace)),
            "timing": None,
            "loop": None,
            "direction": None,
            "status": "selector_and_composition_verified_semantic_animation_open",
        },
    }
    fixture = build_fixture(contract, analysis, catalog)
    source_paths = [
        FORM_C,
        DUMP_CS,
        ACTOR_MAP,
        STATE_CONTRACT,
        MOVEMENT_CONTRACT,
        INTERACTION_CONTRACT,
        PHASE2_CODE_TRACE,
        PHASE2_ANALYSIS,
        PHASE2_ANIMATION,
        PHASE2_ASSETS,
        PHASE2_MAPPING,
        BODYFACE_REFERENCE,
    ]
    manifest = {
        "schema_version": "wave3-c5-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C5-selector-draw-contract",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_paths},
        "artifact_inputs": [rel(ACTOR_MAP), rel(STATE_CONTRACT), rel(MOVEMENT_CONTRACT), rel(INTERACTION_CONTRACT), rel(PHASE2_CODE_TRACE), rel(PHASE2_ANALYSIS), rel(PHASE2_ANIMATION), rel(PHASE2_ASSETS), rel(PHASE2_MAPPING)],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_actor_animation_contract.json",
            "Phases/Phase4/artifacts/wave3_draw_fixture.json",
            "Phases/Phase4/artifacts/wave3_c5_build_manifest.json",
        ],
        "artifact_summary": {
            "selector_flow_count": contract["summary"]["selector_flow_count"],
            "bodyface_record_count": contract["summary"]["bodyface_record_count"],
            "verified_semantic_animations": contract["summary"]["verified_semantic_animations"],
            "probable_semantic_animations": contract["summary"]["probable_semantic_animations"],
            "tface_40_41_case_count": contract["summary"]["tface_40_41_case_count"],
            "scenario_count": len(fixture["scenarios"]),
            "semantic_status": contract["summary"]["status"],
        },
        "status": "W3-C5-built_selector_draw_fixture_semantic_animation_open",
    }
    return {
        ARTIFACTS / "wave3_actor_animation_contract.json": contract,
        ARTIFACTS / "wave3_draw_fixture.json": fixture,
        ARTIFACTS / "wave3_c5_build_manifest.json": manifest,
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
