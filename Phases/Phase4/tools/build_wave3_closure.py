#!/usr/bin/env python3
"""Build the Wave 3 C7 closure decision and handoff manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_wave3_actor_contract import ARTIFACTS, ROOT, load_json, rel, sha256, write_json


GAP_REGISTER = ARTIFACTS / "wave3_gap_register.json"
STATE_CONTRACT = ARTIFACTS / "wave3_actor_state_contract.json"
INTERACTION_CONTRACT = ARTIFACTS / "wave3_interaction_contract.json"
ANIMATION_CONTRACT = ARTIFACTS / "wave3_actor_animation_contract.json"
E2E_FIXTURE = ARTIFACTS / "wave3_actor_e2e_fixture.json"
E2E_TRACE = ARTIFACTS / "wave3_actor_trace.json"
C0_MANIFEST = ARTIFACTS / "wave3_build_manifest.json"
C1_MANIFEST = ARTIFACTS / "wave3_c1_build_manifest.json"
C2_MANIFEST = ARTIFACTS / "wave3_c2_build_manifest.json"
C3_MANIFEST = ARTIFACTS / "wave3_c3_build_manifest.json"
C4_MANIFEST = ARTIFACTS / "wave3_c4_build_manifest.json"
C5_MANIFEST = ARTIFACTS / "wave3_c5_build_manifest.json"
C6_MANIFEST = ARTIFACTS / "wave3_c6_build_manifest.json"
PHASE2_MAPPING = ROOT / "Phases" / "Phase2" / "artifacts" / "agent_state_mapping.json"
REPORT = ROOT / "Phases" / "Phase4" / "docs" / "wave3_closure_report.md"
DECISION = ARTIFACTS / "wave3_legacy_occupancy_decision.json"
MANIFEST = ARTIFACTS / "wave3_c7_build_manifest.json"


def build_decision(
    gaps: dict[str, Any],
    state: dict[str, Any],
    interaction: dict[str, Any],
    animation: dict[str, Any],
    e2e: dict[str, Any],
) -> dict[str, Any]:
    gap_rows = {row["id"]: row for row in gaps["gaps"]}
    occupancy_gap = gap_rows["W3-GAP-006"]
    mapping = load_json(PHASE2_MAPPING)
    return {
        "schema_version": "wave3-closure-decision-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C7-closure-and-handoff",
        "source_roots_read_only": True,
        "closure_status": "complete_with_known_limitations",
        "scope": "C0-C6 contract/fixture handoff; not recovered full legacy runtime equivalence",
        "legacy_occupancy_decision": {
            "status": "adapter_only_for_current_wave3_scope_legacy_producer_not_closed",
            "decision": "Use explicit occupy/release/query seat adapter; do not derive ownership from raw relations or rendering",
            "scoped_functions": ["form_GameForm__MainProcess", "form_GameForm__CallHikkosi", "form_GameForm__CallSyain", "form_GameForm__DrawObj"],
            "raw_findings": [
                "HumanSitChair is consumed as an index/reference in MainProcess raw relation branches",
                "DeskSyain has bounded scan/assignment and clear flows without public actor_id/seat_id ownership",
                "PCObjec and DeskZahyou are observed in render/object relation paths",
                "No bounded source path establishes one-owner seat occupancy or an occupancy API",
            ],
            "evidence": occupancy_gap["evidence"],
            "next_action": occupancy_gap["next_action"],
            "reopen_condition": "Reopen only when a new producer connects raw chair/desk relations to stable actor and seat ownership",
        },
        "c2_semantic_mapping_decision": {
            "status": "not_closed_no_phase2_mapping_update",
            "verified_raw_tick_slices": state["summary"]["verified_raw_tick_slices"],
            "verified_semantic_agent_states": 0,
            "phase2_mapping_updated": False,
            "mapping_source": rel(PHASE2_MAPPING),
            "state_statuses": [
                {"agent_state": row["agent_state"], "status": row["status"], "legacy_state_or_mode": row["legacy_state_or_mode"]}
                for row in mapping["states"]
            ],
            "reason": "C2/C5/C6 contain raw transitions, explicit adapter transitions and renderer composition but no new evidence connecting raw IDs to verified Agent semantics",
            "next_action": "Trace a dependency-specific consumer/timing path only if Phase 5 requires a particular state or animation",
        },
        "animation_decision": {
            "status": animation["summary"]["status"],
            "verified_semantic_animations": animation["summary"]["verified_semantic_animations"],
            "tface_40_41_cases": animation["summary"]["tface_40_41_case_count"],
            "timing": animation["summary"]["timing"],
            "loop": animation["summary"]["loop"],
            "direction": animation["summary"]["direction"],
        },
        "e2e_boundary": {
            "fixture_status": e2e["status"],
            "required_scenarios": e2e["required_scenarios"],
            "legacy_equivalence": e2e["adapter_contract"]["legacy_equivalence"],
        },
        "open_gap_ids": [row["id"] for row in gaps["gaps"] if row["status"] != "out_of_scope"],
        "controlled_out_of_scope": [row["id"] for row in gaps["gaps"] if row["status"] == "out_of_scope"],
        "handoff_rules": [
            "Keep raw legacy fields, adapter states and draw selectors in separate namespaces",
            "Keep legacy_equivalence=false for adapter-generated traces",
            "Do not substitute TFace=40/41 or infer occupancy/collision/walkable from pixels",
        ],
    }


def build() -> dict[Path, Any]:
    required = [
        GAP_REGISTER,
        STATE_CONTRACT,
        INTERACTION_CONTRACT,
        ANIMATION_CONTRACT,
        E2E_FIXTURE,
        E2E_TRACE,
        C0_MANIFEST,
        C1_MANIFEST,
        C2_MANIFEST,
        C3_MANIFEST,
        C4_MANIFEST,
        C5_MANIFEST,
        C6_MANIFEST,
        PHASE2_MAPPING,
        REPORT,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C7 inputs: " + ", ".join(missing))

    gaps = load_json(GAP_REGISTER)
    state = load_json(STATE_CONTRACT)
    interaction = load_json(INTERACTION_CONTRACT)
    animation = load_json(ANIMATION_CONTRACT)
    e2e = load_json(E2E_FIXTURE)
    decision = build_decision(gaps, state, interaction, animation, e2e)
    source_paths = required
    manifest = {
        "schema_version": "wave3-c7-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C7-closure-and-handoff",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in source_paths},
        "artifact_inputs": [rel(path) for path in required],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_legacy_occupancy_decision.json",
            "Phases/Phase4/artifacts/wave3_c7_build_manifest.json",
            "Phases/Phase4/docs/wave3_closure_report.md",
        ],
        "artifact_summary": {
            "contract_packages_ready": ["W3-C0", "W3-C1", "W3-C2", "W3-C3", "W3-C4", "W3-C5", "W3-C6"],
            "open_gap_count": len(decision["open_gap_ids"]),
            "out_of_scope_gap_count": len(decision["controlled_out_of_scope"]),
            "legacy_occupancy_status": decision["legacy_occupancy_decision"]["status"],
            "phase2_mapping_updated": decision["c2_semantic_mapping_decision"]["phase2_mapping_updated"],
            "legacy_equivalence": decision["e2e_boundary"]["legacy_equivalence"],
            "status": decision["closure_status"],
        },
        "status": "W3-C7-closure_ready_for_phase5_with_known_limitations",
    }
    return {DECISION: decision, MANIFEST: manifest}


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
