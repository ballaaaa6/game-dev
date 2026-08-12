#!/usr/bin/env python3
"""Reconcile carried Phase 4 gaps against later bounded evidence.

Historical gap registers are intentionally immutable.  This artifact is the
current view: it records which old questions were answered by later waves,
which remain open, and which are product boundaries rather than extraction
gaps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"
PHASE5_ARTIFACTS = ROOT / "Phases" / "Phase5" / "artifacts"
PHASE6_ARTIFACTS = ROOT / "Phases" / "Phase6" / "artifacts"
OUTPUT = ARTIFACTS / "cross_wave_gap_reconciliation.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_ref(relative: str, role: str) -> dict[str, Any]:
    path = ROOT / relative
    if not path.is_file():
        raise RuntimeError(f"missing evidence artifact: {relative}")
    return {
        "file": relative,
        "role": role,
        "exists": True,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def historical_register_summary() -> dict[str, Any]:
    register_paths = [
        "Phases/Phase4/artifacts/wave1_gap_register.json",
        "Phases/Phase4/artifacts/wave2_gap_register.json",
        "Phases/Phase4/artifacts/wave3_gap_register.json",
        "Phases/Phase4/artifacts/wave4_gap_register.json",
        "Phases/Phase5/artifacts/wave5_gap_register.json",
        "Phases/Phase6/artifacts/wave6_gap_register.json",
    ]
    registers = []
    for relative in register_paths:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"missing gap register: {relative}")
        value = read_json(path)
        rows = value.get("gaps", [])
        registers.append(
            {
                "file": relative,
                "wave": path.stem.split("_")[0].title(),
                "top_status": value.get("status"),
                "gap_count": len(rows),
                "gap_ids": [row.get("gap_id") or row.get("id") for row in rows],
                "statuses": sorted({row.get("status") for row in rows if row.get("status")}),
            }
        )
    return {"registers": registers, "register_count": len(registers)}


def resolved_later() -> list[dict[str, Any]]:
    return [
        {
            "gap_key": "selector_base_values",
            "origin_gap_ids": [
                "G-W1-C1-DDBody",
                "G-W1-C1-DDPC",
                "G-W1-C1-DDChair-DDDesk",
            ],
            "status": "verified_later",
            "resolution_wave": "Wave5",
            "facts": {"DDBody": 0, "DDChair": 25, "DDDesk": 26, "DDPC": 77},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_3_numeric_crop_placement_contract.json",
                    "numeric selector decode",
                ),
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_5_img_list_alignment.json",
                    "exact selector-to-filename join",
                ),
            ],
            "scope_note": "The numeric values and observed joins are closed; universal resource namespace is not inferred beyond the verified joins.",
        },
        {
            "gap_key": "imgface_prefix_suffix",
            "origin_gap_ids": ["G-W1-C2-imgFace-prefix"],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"prefix": "face_", "suffix": ".png", "join_rule": "one-based native literal label corrected to zero-based table index"},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_5_img_list_alignment.json",
                    "corrected native/script metadata alignment",
                )
            ],
            "scope_note": "This resolves the prefix conflict, not the separate TFace=40/41 index-space problem.",
        },
        {
            "gap_key": "bihin_filename_metadata_join",
            "origin_gap_ids": ["G-W2-C1-selector-namespace"],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"join": "IMG_LIST[selector] + .png -> AppData.GetImage -> manifest filename/metadata"},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_5_img_list_alignment.json",
                    "exact bihin filename and metadata join",
                ),
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_4_img_list_loader_bridge.json",
                    "loader bridge",
                ),
            ],
            "scope_note": "The observed selector joins are closed; this does not establish every selector namespace used by the legacy runtime.",
        },
        {
            "gap_key": "floorparts_selector_join",
            "origin_gap_ids": ["G-W2-C1-selector-namespace"],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"mode": 1, "selector_source": "IndexImgFloorParts", "image_slot": "imgFloorParts"},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json",
                    "IndexImgFloorParts and floor-main selector flow",
                )
            ],
            "scope_note": "Observed floor-part joins are closed; full room reconstruction remains open.",
        },
        {
            "gap_key": "seb_consumer_local_placement",
            "origin_gap_ids": ["G-W2-C4-coordinate-spaces", "G-W2-C7-placement-trace"],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"placement": "base + trans", "crop": "U/V/W/H", "space": "local SEB consumer space"},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_7_seb_consumer_contract.json",
                    "SEB crop and local placement",
                )
            ],
            "scope_note": "The local consumer arithmetic is verified; producer world/isometric transform is not.",
        },
        {
            "gap_key": "png_room_screen_placement",
            "origin_gap_ids": ["G-W2-C4-coordinate-spaces", "G-W2-C7-placement-trace"],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"path": "ObjecX/Y + ObjecZX/ZY + image dimensions -> screen draw placement"},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_8_room_caller_contract.json",
                    "bounded GameForm PNG room screen path",
                )
            ],
            "scope_note": "This is a bounded PNG path, not a universal camera/world/isometric transform.",
        },
        {
            "gap_key": "object_producer_field_provenance",
            "origin_gap_ids": [
                "G-W2-C2-object-record-semantics",
                "G-W2-C6-furniture-relations",
                "G-W2-C7-placement-trace",
            ],
            "status": "verified_later_bounded",
            "resolution_wave": "Wave5",
            "facts": {"producer_scope": ["AddObjec", "MainProcess", "CallPCChange", "CallDeskChange", "CallChairChange"]},
            "evidence": [
                artifact_ref(
                    "Phases/Phase5/artifacts/wave5_9_object_producer_contract.json",
                    "object producer field provenance",
                )
            ],
            "scope_note": "Field writes/reads are bounded; semantic names, nonzero ObjecZX/ZY producers and full placement remain open.",
        },
    ]


def open_recoverable() -> list[dict[str, Any]]:
    return [
        {
            "gap_key": "newgamepara_branch_semantics",
            "origin_gap_ids": ["G-W1-C4-NewGamePara-semantics"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave1_branch_index.json", "structural branch index"),
                artifact_ref("Phases/Phase4/artifacts/wave1_slices.json", "bounded assembly slices"),
            ],
            "next_action": "cluster high-value initialization/reset/exit blocks and validate each cluster against recovered callers",
        },
        {
            "gap_key": "doevent_dispatch_lifecycle",
            "origin_gap_ids": ["G-W1-C4-DoEvent-semantics", "W4-GAP-005"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave1_branch_index.json", "structural branch index"),
                artifact_ref("Phases/Phase4/artifacts/wave4_event_mode_candidates.json", "target clusters without mode names"),
            ],
            "next_action": "trace only event clusters that reach AddKaiwa/AddMessage/EventGChange before attempting semantic mode names",
        },
        {
            "gap_key": "tface_40_41_namespace",
            "origin_gap_ids": ["G-W1-C3-face-selector-40-41", "W5-GAP-005"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave1_asset_gap_audit.json", "asset/index audit"),
                artifact_ref("Phases/Phase4/artifacts/wave3_actor_animation_contract.json", "DrawHuman selector contract"),
                artifact_ref("Phases/Phase5/artifacts/wave5_5_img_list_alignment.json", "face prefix/suffix only"),
            ],
            "next_action": "trace callers and producer values; keep 40/41 unresolved unless an alternate namespace or asset source is proven",
        },
        {
            "gap_key": "universal_room_transform",
            "origin_gap_ids": ["G-W2-C4-coordinate-spaces", "W5-GAP-002"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave2_coordinate_contract.json", "coordinate-space evidence"),
                artifact_ref("Phases/Phase5/artifacts/wave5_8_room_caller_contract.json", "bounded PNG caller"),
                artifact_ref("Phases/Phase5/artifacts/wave5_9_object_producer_contract.json", "producer-side boundary"),
            ],
            "next_action": "find producer-side camera/isometric/pivot inputs or explicitly close the question as extraction-unavailable",
        },
        {
            "gap_key": "seb_room_caller_mapping",
            "origin_gap_ids": ["G-W2-C7-placement-trace", "W5-GAP-001", "W5-GAP-009"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json", "SEB structural decode"),
                artifact_ref("Phases/Phase5/artifacts/wave5_7_seb_consumer_contract.json", "local SEB consumer"),
                artifact_ref("Phases/Phase5/artifacts/wave5_8_room_caller_contract.json", "scoped caller inventory"),
            ],
            "next_action": "resolve the direct room caller and four-byte tail only if an alternate asset/extraction source exists",
        },
        {
            "gap_key": "actor_state_and_animation",
            "origin_gap_ids": ["W3-GAP-004", "W3-GAP-005", "W5-GAP-004"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave3_actor_state_contract.json", "raw state/timer contract"),
                artifact_ref("Phases/Phase4/artifacts/wave3_actor_animation_contract.json", "selector/draw boundary"),
                artifact_ref("Phases/Phase5/artifacts/wave5_1_animation_policy.json", "adapter policy boundary"),
            ],
            "next_action": "trace MainProcess/DoEvent transitions only where they feed DrawHuman; do not promote adapter animation profiles to legacy semantics",
        },
        {
            "gap_key": "talk_token_semantics",
            "origin_gap_ids": ["W4-GAP-002"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave4_talk_speaker_trace.json", "bounded split/replace/parse trace"),
            ],
            "next_action": "validate delimiter and token meaning against raw talk records; keep actor binding separate",
        },
        {
            "gap_key": "bubble_timer_unit",
            "origin_gap_ids": ["W4-GAP-004", "W5-GAP-006"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave4_timer_fuki_trace.json", "timer/fukidashi trace"),
                artifact_ref("Phases/Phase5/artifacts/wave5_1_timer_contract.json", "logical-tick adapter boundary"),
            ],
            "next_action": "look for speed/delta-time conversion outside the current MainProcess scope; otherwise retain logical tick",
        },
        {
            "gap_key": "message_graph_labels_audio",
            "origin_gap_ids": ["W4-GAP-007"],
            "status": "open_recoverable",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave4_message_graph_trace.json", "render/audio threshold trace"),
            ],
            "next_action": "join graph IDs and SoundPlay arguments to raw assets/labels before naming product semantics",
        },
    ]


def open_not_found_scoped() -> list[dict[str, Any]]:
    return [
        {
            "gap_key": "speaker_to_actor_binding",
            "origin_gap_ids": ["W4-GAP-003", "W5-GAP-007"],
            "status": "not_found_in_scoped_sources",
            "evidence": [artifact_ref("Phases/Phase4/artifacts/wave4_talk_speaker_trace.json", "scoped caller search")],
            "next_action": "require explicit actor_id at adapter boundary unless a new caller/source is found",
        },
        {
            "gap_key": "semantic_talking_state",
            "origin_gap_ids": ["W3-GAP-006", "W4-GAP-006", "W5-GAP-004"],
            "status": "not_found_in_scoped_sources",
            "evidence": [artifact_ref("Phases/Phase4/artifacts/wave3_actor_animation_contract.json", "semantic animation audit")],
            "next_action": "keep talking as adapter-only; do not infer it from mode 8/9",
        },
        {
            "gap_key": "legacy_seat_collision_walkable",
            "origin_gap_ids": ["G-W2-C6-seat-collision-walkable", "W3-GAP-006", "W3-GAP-007"],
            "status": "not_found_in_scoped_sources",
            "evidence": [
                artifact_ref("Phases/Phase4/artifacts/wave3_legacy_occupancy_decision.json", "occupancy producer decision"),
                artifact_ref("Phases/Phase5/artifacts/wave5_9_object_producer_contract.json", "scoped producer scan"),
            ],
            "next_action": "only reopen with a wider source/assembly scope; web runtime may keep explicit provider boundary",
        },
    ]


def product_boundaries() -> list[dict[str, Any]]:
    return [
        {
            "gap_key": "phase6_persistence_backend",
            "status": "product_boundary",
            "wave": "Wave6",
            "evidence": [artifact_ref("Phases/Phase6/artifacts/wave6_gap_register.json", "Wave6 known limitations")],
            "note": "Local repository adapter is implemented; server/auth/multi-user persistence is outside Phase4 extraction evidence.",
        },
        {
            "gap_key": "phase6_permissions_and_assignment",
            "status": "product_boundary",
            "wave": "Wave6",
            "evidence": [artifact_ref("Phases/Phase6/artifacts/wave6_gap_register.json", "Wave6 known limitations")],
            "note": "Explicit local permission and assignment policies are product decisions, not legacy data gaps.",
        },
        {
            "gap_key": "phase6_ai_and_navigation",
            "status": "product_boundary",
            "wave": "Wave6",
            "evidence": [artifact_ref("Phases/Phase6/artifacts/wave6_gap_register.json", "Wave6 known limitations")],
            "note": "AI auto-assignment and cross-view navigation are out of the Phase4 source-recovery scope.",
        },
    ]


def build() -> dict[str, Any]:
    resolved = resolved_later()
    open_items = open_recoverable()
    not_found = open_not_found_scoped()
    products = product_boundaries()
    return {
        "schema_version": "phase4-cross-wave-gap-reconciliation-v1",
        "phase": "Phase4",
        "waves": ["Wave0", "Wave1", "Wave2", "Wave3", "Wave4", "Wave5", "Wave6"],
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "reconciled_with_open_gaps",
        "historical_registers": historical_register_summary(),
        "resolved_later": resolved,
        "open_recoverable": open_items,
        "open_not_found_scoped": not_found,
        "product_boundaries": products,
        "decision_rule": {
            "historical_registers": "preserve immutable historical statuses",
            "current_status": "use this reconciliation as the current cross-wave view",
            "closure_policy": "only verified source/artifact evidence can close a gap; adapter behavior is not legacy equivalence",
        },
        "summary": {
            "historical_register_count": 6,
            "resolved_later_count": len(resolved),
            "open_recoverable_count": len(open_items),
            "open_not_found_scoped_count": len(not_found),
            "product_boundary_count": len(products),
            "stale_statuses_superseded_by_later_evidence": len(resolved),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare generated output with the checked-in artifact")
    args = parser.parse_args()
    value = build()
    if args.check:
        if not OUTPUT.is_file():
            raise SystemExit(f"missing generated artifact: {rel(OUTPUT)}")
        actual = read_json(OUTPUT)
        if actual != value:
            raise SystemExit(f"artifact mismatch: {rel(OUTPUT)}")
        print(json.dumps({"status": "check_pass", "output": rel(OUTPUT)}, ensure_ascii=False))
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "built", "output": rel(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
