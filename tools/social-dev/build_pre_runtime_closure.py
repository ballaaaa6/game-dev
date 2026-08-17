"""Build the pre-runtime closure package for Social Dev.

This package closes the historical Phase 0 through Phase 1C review boundary
without erasing the original candidate evidence.  The current authority is a
closure matrix that maps every old blocking item to verified evidence or an
explicit deferred/quarantine decision.  It does not execute or import
decompiled C# and it does not create the TypeScript runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"

SCHEMA_VERSION = "social-dev-pre-runtime-closure-v1"
MATRIX_SCHEMA_VERSION = "social-dev-semantic-review-closure-v1"
LOAD_SCHEMA_VERSION = "social-dev-load-contract-closure-v1"
DATA_SCHEMA_VERSION = "social-dev-data-contract-v1"
ENTITY_SCHEMA_VERSION = "social-dev-entity-contract-v1"
SAVE_SCHEMA_VERSION = "social-dev-save-contract-v1"
SUPERSESSION_SCHEMA_VERSION = "social-dev-phase1-supersession-v1"

ALLOWED_FINAL_STATUSES = {"verified", "derived", "deferred", "quarantine", "conflict"}

PATHS = {
    "review_queue": EVIDENCE / "csharp_semantic_review_queue.json",
    "extraction_validation": EVIDENCE / "csharp_extraction_validation.json",
    "system_inventory": EVIDENCE / "csharp_system_inventory.json",
    "load_candidates": EVIDENCE / "load_contract_candidates.json",
    "field_load_candidates": EVIDENCE / "field_load_candidates.json",
    "first_slice_candidate": EVIDENCE / "first_slice_data_candidate.json",
    "first_slice_validation": EVIDENCE / "first_slice_data_validation.json",
    "scene_behavior_validation": EVIDENCE / "scene_behavior_validation.json",
    "scene_semantics_validation": EVIDENCE / "scene_semantics_validation.json",
    "phase1d_closure": EVIDENCE / "phase1d_closure.json",
    "phase1d_validation": EVIDENCE / "phase1d_closure_validation.json",
    "asset_selectors": EVIDENCE / "asset_selector_contract.json",
    "staff_semantics": EVIDENCE / "staff_semantics_contract.json",
    "scene_catalog": RUNTIME_EVIDENCE / "scene_catalog_contract.json",
    "object_catalog": RUNTIME_EVIDENCE / "object_catalog_contract.json",
    "actor_catalog": RUNTIME_EVIDENCE / "actor_catalog_contract.json",
    "actor_behavior": RUNTIME_EVIDENCE / "actor_behavior_contract.json",
    "camera": RUNTIME_EVIDENCE / "camera_coordinate_contract.json",
    "tick": RUNTIME_EVIDENCE / "tick_order_contract.json",
}

SOURCE_FILES = {
    "DataManager": SOURCE_ROOT / "data/DataManager.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
    "Node": SOURCE_ROOT / "game.routeSearch/Node.cs",
    "Player": SOURCE_ROOT / "game/Player.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
    "Camera": SOURCE_ROOT / "game/Camera.cs",
}

FIRST_SLICE_TYPES = ["RoomData", "FurnitureData", "StaffData", "JobData", "SkillData"]


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return str(candidate.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        text = str(candidate).replace("\\", "/")
        marker = "/knowledge/"
        if marker in text:
            return text[text.index("knowledge/") :]
        return text


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing evidence file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "artifact_hashes"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def content_hash(payload: Any) -> str:
    return sha256_bytes(stable_json(without_dynamic(payload)).encode("utf-8"))


def evidence_ref(path: Path, payload: Any | None = None) -> dict[str, Any]:
    require(path.is_file(), f"missing evidence reference: {path}")
    return {
        "path": relative_path(path),
        "sha256": sha256_file(path),
        "content_hash": content_hash(payload) if payload is not None else None,
    }


def source_ref(name: str, purpose: str) -> dict[str, Any]:
    path = SOURCE_FILES[name]
    require(path.is_file(), f"missing source reference: {path}")
    return {
        "type": name,
        "path": relative_path(path),
        "sha256": sha256_file(path),
        "purpose": purpose,
        "status": "evidence_only",
    }


def finalise(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    payload = dict(payload)
    payload["generated_at_utc"] = utc_now()
    payload["content_hash"] = ""
    payload["content_hash"] = content_hash(payload)
    return payload


def require_upstream_gates() -> dict[str, dict[str, Any]]:
    upstream: dict[str, dict[str, Any]] = {}
    for key in (
        "phase1d_closure",
        "phase1d_validation",
        "asset_selectors",
        "staff_semantics",
        "scene_catalog",
        "object_catalog",
        "actor_catalog",
        "actor_behavior",
        "camera",
        "tick",
    ):
        payload = load_json(PATHS[key])
        upstream[key] = payload

    require(upstream["phase1d_closure"]["status"] == "pass", "Phase 1D closure status is not pass")
    require(upstream["phase1d_closure"]["semantic_status"] == "closed_for_phase2_entry", "Phase 1D closure is not authoritative")
    require(upstream["phase1d_validation"]["status"] == "pass", "Phase 1D validation is not pass")
    require(upstream["phase1d_validation"]["semantic_status"] == "closed_for_phase2_entry", "Phase 1D validation is not closed")
    require(upstream["asset_selectors"]["status"] == "pass", "asset selector contract is not pass")
    require(not upstream["asset_selectors"].get("unresolved"), "asset selector contract has unresolved selectors")
    require(upstream["staff_semantics"]["status"] == "pass", "staff semantics contract is not pass")
    for key in ("scene_catalog", "object_catalog", "actor_catalog"):
        require(upstream[key]["status"] == "pass", f"{key} status is not pass")
        require(
            upstream[key]["semantic_status"] == "approved_for_runtime_contract",
            f"{key} is not approved for runtime contract",
        )
    for key in ("actor_behavior", "camera", "tick"):
        require(upstream[key]["status"] == "pass", f"{key} readiness contract is not pass")
        require(
            upstream[key]["semantic_status"] == "approved_for_runtime_contract",
            f"{key} readiness contract is not approved",
        )
    return upstream


def build_load_closure() -> dict[str, Any]:
    loads = load_json(PATHS["load_candidates"])
    fields = load_json(PATHS["field_load_candidates"])
    load_by_type = {row["element_type"]: row for row in loads["rows"]}
    field_by_type = {row["type"]: row for row in fields["rows"]}

    mappings: list[dict[str, Any]] = []
    for type_name in FIRST_SLICE_TYPES:
        load_row = load_by_type.get(type_name)
        field_row = field_by_type.get(type_name)
        require(load_row is not None, f"missing loader row for {type_name}")
        require(field_row is not None, f"missing field loader row for {type_name}")
        require(load_row["load_method_status"] == "present", f"{type_name} loader method is missing")
        require(load_row["reader_call_count"] == len(load_row["reader_sequence"]), f"{type_name} reader count drift")
        require(field_row["reader_count"] == len(field_row["reader_sequence"]), f"{type_name} field reader count drift")
        require(field_row["reader_count"] == field_row["field_assignment_count"], f"{type_name} field assignment count mismatch")
        require(load_row["reader_sequence"] == field_row["reader_sequence"], f"{type_name} loader sequence disagreement")
        mappings.append(
            {
                "type": type_name,
                "table": {
                    "english": relative_path(load_row["english_table"]),
                    "english_row_count": load_row["english_row_count"],
                    "english_column_count_distribution": load_row["english_column_count_distribution"],
                },
                "source_file": load_row["source_file"],
                "reader_sequence": load_row["reader_sequence"],
                "field_assignment_sequence": field_row["field_assignment_sequence"],
                "field_mapping_status": "verified_source_order_with_raw_array_retention",
                "array_policy": "Array values retain complete raw framing; no semantic zip is inferred after an array reader.",
                "status": "verified",
                "evidence_refs": [relative_path(PATHS["load_candidates"]), relative_path(PATHS["field_load_candidates"])],
            }
        )

    missing_loaders = [
        {
            "registry_field": "helpTexts_",
            "type": "HelpText",
            "status": "deferred",
            "reason": "No matching data class/loader body is required by display-slice-01; preserve as raw evidence until a visible text slice requires it.",
        },
        {
            "registry_field": "installData_",
            "type": "Install",
            "status": "deferred",
            "reason": "Install is bootstrap/gameplay data outside the living-scene display slice; no runtime field is promoted.",
        },
    ]
    count_mismatches = [
        {
            "type": "CompanyData",
            "status": "deferred",
            "reason": "Reader/field count mismatch remains outside the display slice; raw table and source references remain retained.",
        },
        {
            "type": "DownloadEventData",
            "status": "deferred",
            "reason": "Reader/field count mismatch remains outside the display slice; no typed contract is promoted.",
        },
        {
            "type": "ProfileData",
            "status": "deferred",
            "reason": "Reader/field count mismatch remains outside the display slice; duplicated choices assignment is not guessed.",
        },
    ]

    payload = {
        "schema_version": LOAD_SCHEMA_VERSION,
        "package": "social-dev-load-contract-closure",
        "status": "pass",
        "semantic_status": "closed_for_display_slice",
        "scope": "display-slice-01 plus explicit non-promoted exceptions",
        "policy": {
            "selected_types": "All five display-slice data types have matching loader and field-assignment sequences.",
            "array_framing": "Retain raw arrays and assign only fields explicitly consumed by the source loader sequence.",
            "non_slice_policy": "Missing loaders and count mismatches are closed as deferred exceptions, never silently promoted.",
        },
        "coverage": {
            "registry_arrays": len(loads.get("rows", [])),
            "data_types": 44,
            "field_candidates": fields.get("counts", {}),
            "first_slice_types": len(mappings),
        },
        "first_slice_mappings": mappings,
        "exceptions": {
            "missing_loaders": missing_loaders,
            "count_mismatches": count_mismatches,
        },
        "open_blocking_items": [],
        "provenance": [evidence_ref(PATHS["load_candidates"]), evidence_ref(PATHS["field_load_candidates"])],
    }
    return finalise("load_contract_closure.json", payload)


def build_data_contract(load_closure: dict[str, Any], upstream: dict[str, dict[str, Any]]) -> dict[str, Any]:
    records = [
        {"type": "RoomData", "ids": [0], "status": "verified", "role": "scene identity/grid input"},
        {"type": "FurnitureData", "ids": [0, 1, 2, 5], "status": "verified", "role": "object/passability/selector input"},
        {"type": "StaffData", "ids": [0, 1, 2, 3, 4], "status": "verified", "role": "visible actor identity input"},
        {"type": "JobData", "ids": [4], "status": "verified", "role": "selected staff job relation"},
        {"type": "SkillData", "ids": [1], "status": "verified", "role": "selected staff skill/effect relation"},
    ]
    payload = {
        "schema_version": DATA_SCHEMA_VERSION,
        "package": "social-dev-data-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "scope": "Canonical normalized data required by the visible room/staff slice.",
        "records": records,
        "relations": [
            {"from": "StaffData.jobId_", "to": "JobData.id_", "value": 4, "status": "verified", "source": "Staff constructor/init"},
            {"from": "StaffData.skill_", "to": "SkillData.id_", "value": 1, "status": "verified", "source": "Staff.skillId_ and Staff.GetSkill consumer"},
        ],
        "loader_contract": {
            "path": relative_path(EVIDENCE / "load_contract_closure.json"),
            "content_hash": load_closure["content_hash"],
            "status": load_closure["status"],
            "semantic_status": load_closure["semantic_status"],
        },
        "upstream_contracts": [
            evidence_ref(PATHS["scene_catalog"], upstream["scene_catalog"]),
            evidence_ref(PATHS["object_catalog"], upstream["object_catalog"]),
            evidence_ref(PATHS["actor_catalog"], upstream["actor_catalog"]),
        ],
        "raw_retention": {
            "required": True,
            "policy": "Every selected row retains locale, row number, row hash, source path and raw columns in evidence.",
            "array_policy": "Variable-length arrays are not re-zipped into invented product semantics.",
        },
        "non_promoted": [
            {
                "scope": "data types outside the five selected types",
                "status": "deferred",
                "reason": "No visible display-slice consumer is currently authorized.",
            },
            {
                "scope": "unmapped array columns outside the selected contracts",
                "status": "quarantine",
                "reason": "Column position alone is insufficient semantic evidence.",
            },
        ],
        "open_blocking_items": [],
    }
    return finalise("data_contract.json", payload)


def build_entity_contract(upstream: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entities = [
        {
            "id": "WorldContext",
            "status": "derived",
            "responsibility": "Own the mutable scene, actor/object collections, deterministic clock and event queue.",
            "source_boundary": ["AppData", "Player", "Main"],
            "fields": ["scene_ref", "actors", "objects", "clock", "event_queue", "presentation_effects"],
        },
        {
            "id": "SceneState",
            "status": "verified",
            "responsibility": "Room grid, raw object type layer, object bindings and camera input.",
            "source_boundary": ["Room", "RoomData", "Camera"],
            "fields": ["scene_ref", "grid", "object_layer", "actor_layer", "camera_offset"],
        },
        {
            "id": "ObjectState",
            "status": "verified",
            "responsibility": "Occupancy, footprint, passability, standing positions and bounded interaction state.",
            "source_boundary": ["ObjChip", "FurnitureData"],
            "fields": ["object_id", "raw_type", "furniture_ref", "position", "direction", "passability", "occupancy"],
        },
        {
            "id": "ActorState",
            "status": "verified",
            "responsibility": "Mutable visible Staff state, position, route, animation and talk/bubble effects.",
            "source_boundary": ["Staff", "StaffData", "JobData", "SkillData"],
            "fields": ["actor_id", "staff_ref", "position", "state", "move_mode", "route", "animation", "talk"],
        },
        {
            "id": "RouteService",
            "status": "verified",
            "responsibility": "Cardinal grid neighbors, goal filters and deterministic route output.",
            "source_boundary": ["Astar", "Node", "Room"],
            "fields": ["grid", "neighbor_policy", "goal_filter", "route_fixture"],
        },
        {
            "id": "Clock",
            "status": "derived",
            "responsibility": "Logical tick/frame progression and timer inputs; wall-clock access stays outside the core.",
            "source_boundary": ["Player", "Room", "Staff"],
            "fields": ["tick_index", "frame", "logical_time"],
        },
        {
            "id": "EventQueue",
            "status": "deferred",
            "responsibility": "Visible delayed events only; no gameplay/management event graph is promoted.",
            "source_boundary": ["DelayEvent", "EventData", "TalkData"],
            "fields": ["sequence", "due_tick", "event_type", "payload"],
        },
        {
            "id": "PresentationEffects",
            "status": "derived",
            "responsibility": "Render-facing alpha, animation, bubble and camera effects without mutating simulation state.",
            "source_boundary": ["Room", "Staff", "ObjChip", "Main"],
            "fields": ["alpha", "sprite_selector", "frame", "bubble", "camera_offset"],
        },
    ]
    payload = {
        "schema_version": ENTITY_SCHEMA_VERSION,
        "package": "social-dev-entity-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "ownership_rule": "Simulation owns state; renderer consumes snapshots/effects and cannot mutate state.",
        "entities": entities,
        "player_appdata_decision": {
            "status": "derived",
            "decision": "Do not port Player or AppData wholesale. Split only the bounded responsibilities listed above.",
            "evidence": [source_ref("Player", "lifecycle/time/room/staff evidence"), source_ref("AppData", "world/bootstrap facade evidence")],
        },
        "decompiler_body_policy": [
            {
                "method": "DataManager.Load",
                "status": "quarantine",
                "policy": "Use registry/reader evidence; write a fresh loader from the closed data contract.",
                "source": source_ref("DataManager", "loader body contains decompiler artifacts"),
            },
            {
                "method": "Room.Update",
                "status": "quarantine",
                "policy": "Use the verified update-order observation; implement a new deterministic loop.",
                "source": source_ref("Room", "update-order and lifecycle evidence"),
            },
            {
                "method": "Staff.Update",
                "status": "quarantine",
                "policy": "Use bounded transition/tick contracts; do not copy the damaged body.",
                "source": source_ref("Staff", "state/movement/animation evidence"),
            },
            {
                "method": "Astar.SearchRoute",
                "status": "quarantine",
                "policy": "Implement a new route service from the native cardinal-neighbor and goal-filter contract.",
                "source": source_ref("Astar", "route constants and native policy evidence"),
            },
        ],
        "upstream_contracts": [
            evidence_ref(PATHS["actor_behavior"], upstream["actor_behavior"]),
            evidence_ref(PATHS["camera"], upstream["camera"]),
            evidence_ref(PATHS["tick"], upstream["tick"]),
        ],
        "open_blocking_items": [],
    }
    return finalise("entity_contract.json", payload)


def build_save_contract(data_contract: dict[str, Any], entity_contract: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": SAVE_SCHEMA_VERSION,
        "package": "social-dev-save-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "implementation_status": "contract_only_until_runtime_core",
        "snapshot": {
            "schema_version": "display-slice-snapshot-v1",
            "required": [
                "catalog_id",
                "scene_ref",
                "tick_index",
                "logical_time",
                "actors",
                "objects",
                "event_queue",
            ],
            "stable_id_policy": "Persist canonical IDs (room:, actor:, object:) rather than array positions.",
            "actor_fields": ["actor_id", "staff_ref", "position", "state", "move_mode", "route", "animation", "talk"],
            "object_fields": ["object_id", "raw_type", "furniture_ref", "position", "direction", "occupancy"],
            "event_fields": ["sequence", "due_tick", "event_type", "payload"],
        },
        "load_policy": {
            "validate_catalog_id": True,
            "validate_contract_hashes": True,
            "reject_unknown_schema": True,
            "do_not_restore_presentation": True,
        },
        "excluded_from_display_slice": [
            "Player wholesale fields",
            "AppData wholesale fields",
            "management/economy/progression state",
            "binary image/SEB payloads",
            "unverified raw array semantics",
        ],
        "provenance": {
            "data_contract": {"path": relative_path(RUNTIME_EVIDENCE / "data_contract.json"), "content_hash": data_contract["content_hash"]},
            "entity_contract": {"path": relative_path(RUNTIME_EVIDENCE / "entity_contract.json"), "content_hash": entity_contract["content_hash"]},
        },
        "open_blocking_items": [],
    }
    return finalise("save_contract.json", payload)


def build_supersession(upstream: dict[str, dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "schema_version": SUPERSESSION_SCHEMA_VERSION,
        "package": "social-dev-phase1-supersession",
        "status": "pass",
        "semantic_status": "closed_by_authority",
        "historical_package": "Phase 1C scene-semantics review",
        "authority": {
            "phase1d": evidence_ref(PATHS["phase1d_closure"], upstream["phase1d_closure"]),
            "phase1d_validation": evidence_ref(PATHS["phase1d_validation"], upstream["phase1d_validation"]),
            "scene_catalog": evidence_ref(PATHS["scene_catalog"], upstream["scene_catalog"]),
            "object_catalog": evidence_ref(PATHS["object_catalog"], upstream["object_catalog"]),
        },
        "replacement_matrix": [
            {
                "old_id": "passmap-and-standing-semantics",
                "old_status": "pending_review",
                "final_status": "verified",
                "replacement": "Phase 1D passmap fixture and standing-position contract",
                "reason": "Native bounded fixture closes the 3x3 passMap window and four standing positions.",
            },
            {
                "old_id": "route-goal-filter",
                "old_status": "pending_review",
                "final_status": "verified",
                "replacement": "Phase 1D route fixture and cardinal-neighbor/goal-filter contract",
                "reason": "Current-APK native evidence closes neighbor admission and goal filters.",
            },
            {
                "old_id": "asset-selector-carryover",
                "old_status": "pending_review",
                "final_status": "verified",
                "replacement": "asset_selector_contract.json plus Scene/Object/Actor catalogs",
                "reason": "All parsed selectors used by the display slice resolve with zero unresolved selectors.",
            },
        ],
        "preservation_policy": "The original Phase 1C evidence remains historical; this record is the active lifecycle decision.",
        "open_blocking_items": [],
    }
    return finalise("phase1_supersession.json", payload)


def closure_item(
    item_id: str,
    phase: str,
    package: str,
    old_status: str,
    old_blocking: bool,
    final_status: str,
    resolution: str,
    evidence: list[str],
    authority: list[str],
    promotion: str,
) -> dict[str, Any]:
    require(final_status in ALLOWED_FINAL_STATUSES, f"invalid final status for {item_id}: {final_status}")
    return {
        "id": item_id,
        "phase": phase,
        "package": package,
        "historical_status": old_status,
        "historical_blocking": old_blocking,
        "final_status": final_status,
        "resolution": resolution,
        "evidence_refs": evidence,
        "authority_refs": authority,
        "runtime_promotion": promotion,
        "closure_status": "closed",
    }


def build_matrix(
    load_closure: dict[str, Any],
    data_contract: dict[str, Any],
    entity_contract: dict[str, Any],
    save_contract: dict[str, Any],
    supersession: dict[str, Any],
    upstream: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    authority_refs = [
        relative_path(PATHS["phase1d_closure"]),
        relative_path(PATHS["phase1d_validation"]),
        relative_path(PATHS["asset_selectors"]),
        relative_path(PATHS["staff_semantics"]),
        relative_path(PATHS["scene_catalog"]),
        relative_path(PATHS["object_catalog"]),
        relative_path(PATHS["actor_catalog"]),
    ]
    items = [
        closure_item(
            "loader-column-semantic",
            "Phase 0",
            "csharp_system_extraction",
            "unknown",
            True,
            "verified",
            "All five display-slice loader/field sequences match source order and retain raw array framing; non-slice missing/mismatch rows are explicit deferred exceptions.",
            [relative_path(PATHS["load_candidates"]), relative_path(PATHS["field_load_candidates"])],
            [relative_path(EVIDENCE / "load_contract_closure.json"), relative_path(RUNTIME_EVIDENCE / "data_contract.json")],
            "display-slice-only",
        ),
        closure_item(
            "decompiler-body-repair",
            "Phase 0",
            "csharp_system_extraction",
            "quarantine",
            True,
            "quarantine",
            "Decompiler bodies are not repaired or copied. Fresh runtime implementations must consume the closed contracts and bounded source/native observations.",
            [relative_path(EVIDENCE / "candidate_diff.json"), relative_path(EVIDENCE / "cleanup_equivalence.json")],
            [relative_path(RUNTIME_EVIDENCE / "entity_contract.json")],
            "never-promote-body",
        ),
        closure_item(
            "player-appdata-split",
            "Phase 0",
            "csharp_system_extraction",
            "derived",
            True,
            "derived",
            "Player/AppData are split into bounded world, clock, event and presentation responsibilities; wholesale porting is prohibited.",
            [relative_path(EVIDENCE / "runtime_schema_candidate.json"), relative_path(EVIDENCE / "csharp_system_inventory.json")],
            [relative_path(RUNTIME_EVIDENCE / "entity_contract.json"), relative_path(RUNTIME_EVIDENCE / "save_contract.json")],
            "bounded-contract-only",
        ),
        closure_item(
            "asset-selector-promotion",
            "Phase 0",
            "csharp_system_extraction",
            "quarantine",
            True,
            "verified",
            "Display-slice furniture/staff selectors and parsed animation selectors resolve in the indexed asset package; unrelated derived assets remain non-promoted.",
            [relative_path(PATHS["asset_selectors"]), relative_path(PATHS["staff_semantics"])],
            authority_refs,
            "display-slice-only",
        ),
        closure_item(
            "semantic-state-labels",
            "Phase 0",
            "csharp_system_extraction",
            "unknown",
            True,
            "derived",
            "Numeric state/move labels are retained exactly from source; only the bounded living-scene transition/timing fixture is promoted. Other state families are explicitly out of scope.",
            [relative_path(PATHS["staff_semantics"]), relative_path(PATHS["actor_behavior"])],
            [relative_path(RUNTIME_EVIDENCE / "entity_contract.json"), relative_path(PATHS["tick"])],
            "bounded-living-scene-only",
        ),
        closure_item(
            "first-slice-selection",
            "Phase 0",
            "csharp_system_extraction",
            "derived",
            False,
            "derived",
            "The room/staff/object scope is fixed as display-slice-01 and is traceable to the data-readiness plan and canonical catalogs.",
            ["docs/roadmap/Roadmap_SocialDev_Data_Readiness.md", "docs/reports/social-dev_csharp_system_survey.md"],
            authority_refs,
            "scope-locked",
        ),
        closure_item(
            "room-state-placement-unverified",
            "Phase 1",
            "first_slice_data_candidate",
            "unknown",
            True,
            "derived",
            "Room 0 identity/grid/door and the bounded actor entry fixture are closed; arbitrary furniture placement and free-cell selection remain explicitly deferred.",
            [relative_path(PATHS["first_slice_candidate"]), relative_path(PATHS["scene_catalog"])],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["object_catalog"]), relative_path(EVIDENCE / "actor_spawn_fixture.json")],
            "bounded-fixture-only",
        ),
        closure_item(
            "array-column-semantic-unverified",
            "Phase 1",
            "first_slice_data_candidate",
            "unknown",
            True,
            "verified",
            "Selected first-slice field assignment sequences are source-verified; raw array framing is preserved and no post-array semantic zip is promoted.",
            [relative_path(PATHS["field_load_candidates"]), relative_path(PATHS["first_slice_candidate"])],
            [relative_path(EVIDENCE / "load_contract_closure.json"), relative_path(RUNTIME_EVIDENCE / "data_contract.json")],
            "selected-fields-only",
        ),
        closure_item(
            "staff-skill-link-unverified",
            "Phase 1",
            "first_slice_data_candidate",
            "unknown",
            True,
            "verified",
            "StaffData.skill_ is consumed into Staff.skillId_ and resolved through Staff.GetSkill; selected rows and both locales agree on SkillData(1).",
            [relative_path(PATHS["first_slice_candidate"]), relative_path(PATHS["staff_semantics"])],
            [relative_path(PATHS["actor_catalog"]), relative_path(PATHS["actor_behavior"])],
            "display-slice-only",
        ),
        closure_item(
            "asset-selector-not-promoted",
            "Phase 1",
            "first_slice_data_candidate",
            "quarantine",
            True,
            "verified",
            "Selected furniture/staff/animation selectors are resolved by the asset selector and actor contracts; unselected assets remain non-promoted.",
            [relative_path(PATHS["asset_selectors"]), relative_path(PATHS["staff_semantics"])],
            authority_refs,
            "display-slice-only",
        ),
        closure_item(
            "room-map-code-semantic",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "verified",
            "Current-APK native evidence closes Room.InitObjChips objMap[y][x] to ObjChip.type_ and preserves flat indexing x + y * width.",
            [relative_path(EVIDENCE / "scene_data_candidate.json")],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["scene_catalog"])],
            "display-slice-only",
        ),
        closure_item(
            "room-placement-missing",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "derived",
            "The bounded furniture placement model and three-actor door entry fixture are closed; full automatic placement is deferred rather than guessed.",
            [relative_path(EVIDENCE / "scene_data_candidate.json")],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["object_catalog"]), relative_path(EVIDENCE / "actor_spawn_fixture.json")],
            "bounded-fixture-only",
        ),
        closure_item(
            "passability-unresolved",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "verified",
            "The type-4 passMap window, zero-cell/all-nonzero probes and Astar passability filters are closed by the Phase 1D fixture.",
            [relative_path(EVIDENCE / "scene_data_candidate.json")],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["object_catalog"])],
            "display-slice-only",
        ),
        closure_item(
            "asset-selector-unverified",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "verified",
            "Selector identity is closed for the parsed furniture/staff rows and selected animation selectors; no asset binary is copied into runtime.",
            [relative_path(PATHS["asset_selectors"]), relative_path(PATHS["staff_semantics"])],
            authority_refs,
            "display-slice-only",
        ),
        closure_item(
            "numeric-state-labels",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "derived",
            "Source labels and numeric values are closed as labels; only bounded idle/move/work/talk behavior is runtime-authorized.",
            [relative_path(PATHS["staff_semantics"])],
            [relative_path(PATHS["actor_behavior"]), relative_path(RUNTIME_EVIDENCE / "entity_contract.json")],
            "bounded-living-scene-only",
        ),
        closure_item(
            "decompiler-update-body",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "quarantine",
            "The Staff/Room update bodies remain evidence-only; deterministic runtime code must be written from the bounded transition and tick contracts.",
            [relative_path(EVIDENCE / "staff_behavior_candidate.json"), relative_path(EVIDENCE / "candidate_diff.json")],
            [relative_path(RUNTIME_EVIDENCE / "entity_contract.json"), relative_path(PATHS["tick"])],
            "never-promote-body",
        ),
        closure_item(
            "skill-reference-promotion",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "verified",
            "Staff.skillId_ and the selected SkillData effect contract are source- and locale-backed.",
            [relative_path(PATHS["staff_semantics"])],
            [relative_path(PATHS["actor_catalog"]), relative_path(PATHS["actor_behavior"])],
            "display-slice-only",
        ),
        closure_item(
            "animation-selector-promotion",
            "Phase 1B",
            "scene_behavior_candidate",
            "pending_review",
            True,
            "verified",
            "Human wait/typing selectors 10–13 and 23–26 resolve in the indexed human SEB package and are bounded by the staff animation contract.",
            [relative_path(PATHS["staff_semantics"]), relative_path(PATHS["asset_selectors"])],
            [relative_path(PATHS["actor_catalog"]), relative_path(PATHS["actor_behavior"])],
            "display-slice-only",
        ),
        closure_item(
            "passmap-and-standing-semantics",
            "Phase 1C",
            "scene_semantics_review",
            "pending_review",
            True,
            "verified",
            "Superseded by the authoritative Phase 1D native passMap and standing-position fixtures.",
            [relative_path(PATHS["scene_semantics_validation"])],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["object_catalog"])],
            "display-slice-only",
        ),
        closure_item(
            "route-goal-filter",
            "Phase 1C",
            "scene_semantics_review",
            "pending_review",
            True,
            "verified",
            "Superseded by the authoritative Phase 1D cardinal-neighbor and goal-filter route fixture.",
            [relative_path(PATHS["scene_semantics_validation"])],
            [relative_path(PATHS["phase1d_closure"]), relative_path(PATHS["scene_catalog"])],
            "display-slice-only",
        ),
        closure_item(
            "asset-selector-carryover",
            "Phase 1C",
            "scene_semantics_review",
            "pending_review",
            True,
            "verified",
            "Superseded by the zero-unresolved asset selector contract and the approved Scene/Object/Actor catalogs.",
            [relative_path(PATHS["scene_semantics_validation"]), relative_path(PATHS["asset_selectors"])],
            authority_refs,
            "display-slice-only",
        ),
    ]

    expected_ids = {
        item["id"] for item in load_json(PATHS["review_queue"])["items"]
    }
    actual_phase0_ids = {item["id"] for item in items if item["phase"] == "Phase 0"}
    require(expected_ids == actual_phase0_ids, f"Phase 0 closure matrix does not cover queue: {expected_ids ^ actual_phase0_ids}")

    expected_first_slice = {
        item["id"] for item in load_json(PATHS["first_slice_candidate"])["review_items"] if item.get("blocking")
    }
    actual_first_slice_ids = {
        item["id"] for item in items if item["phase"] == "Phase 1"
    }
    require(expected_first_slice == actual_first_slice_ids, f"Phase 1 closure matrix mismatch: {expected_first_slice ^ actual_first_slice_ids}")

    expected_scene_behavior = set(load_json(PATHS["scene_behavior_validation"])["blocking_review_items"])
    actual_scene_behavior = {item["id"] for item in items if item["phase"] == "Phase 1B"}
    require(expected_scene_behavior == actual_scene_behavior, f"Phase 1B closure matrix mismatch: {expected_scene_behavior ^ actual_scene_behavior}")

    expected_scene_semantics = set(load_json(PATHS["scene_semantics_validation"])["blocking_review_items"])
    actual_scene_semantics = {item["id"] for item in items if item["phase"] == "Phase 1C"}
    require(expected_scene_semantics == actual_scene_semantics, f"Phase 1C closure matrix mismatch: {expected_scene_semantics ^ actual_scene_semantics}")

    require(all(item["closure_status"] == "closed" for item in items), "not every closure item is closed")
    require(not [item for item in items if item["historical_blocking"] and item["final_status"] not in ALLOWED_FINAL_STATUSES], "invalid blocking final status")

    counts = {status: sum(item["final_status"] == status for item in items) for status in sorted(ALLOWED_FINAL_STATUSES)}
    payload = {
        "schema_version": MATRIX_SCHEMA_VERSION,
        "package": "social-dev-semantic-review-closure",
        "status": "pass",
        "semantic_status": "closed_before_runtime",
        "scope": "Phase 0 through Phase 1C historical review boundary",
        "policy": {
            "raw_evidence": "Original candidate artifacts retain their historical status and are not rewritten to erase provenance.",
            "active_authority": "This matrix and the contracts it references determine current closure status.",
            "runtime_rule": "Only verified/derived display-slice facts enter canonical contracts; deferred/quarantine facts do not.",
        },
        "items": items,
        "counts": {
            "total_items": len(items),
            "closed_items": len(items),
            "open_items": 0,
            "pending_review_items": 0,
            "blocking_items_remaining": 0,
            "final_statuses": counts,
        },
        "contract_refs": [
            {"path": relative_path(EVIDENCE / "load_contract_closure.json"), "content_hash": load_closure["content_hash"]},
            {"path": relative_path(RUNTIME_EVIDENCE / "data_contract.json"), "content_hash": data_contract["content_hash"]},
            {"path": relative_path(RUNTIME_EVIDENCE / "entity_contract.json"), "content_hash": entity_contract["content_hash"]},
            {"path": relative_path(RUNTIME_EVIDENCE / "save_contract.json"), "content_hash": save_contract["content_hash"]},
            {"path": relative_path(EVIDENCE / "phase1_supersession.json"), "content_hash": supersession["content_hash"]},
        ],
        "authority_contracts": authority_refs,
        "open_blocking_items": [],
    }
    return finalise("semantic_review_closure.json", payload)


def build_package() -> dict[str, dict[str, Any]]:
    upstream = require_upstream_gates()
    load_closure = build_load_closure()
    data_contract = build_data_contract(load_closure, upstream)
    entity_contract = build_entity_contract(upstream)
    save_contract = build_save_contract(data_contract, entity_contract)
    supersession = build_supersession(upstream)
    matrix = build_matrix(load_closure, data_contract, entity_contract, save_contract, supersession, upstream)

    package = {
        "knowledge/fixtures/accepted/load_contract_closure.json": load_closure,
        "knowledge/fixtures/accepted/semantic_review_closure.json": matrix,
        "knowledge/fixtures/accepted/phase1_supersession.json": supersession,
        "knowledge/fixtures/accepted/runtime/data_contract.json": data_contract,
        "knowledge/fixtures/accepted/runtime/entity_contract.json": entity_contract,
        "knowledge/fixtures/accepted/runtime/save_contract.json": save_contract,
    }
    artifact_hashes = {path: payload["content_hash"] for path, payload in package.items()}
    closure_payload = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-pre-runtime-closure",
        "status": "pass",
        "semantic_status": "closed_before_runtime",
        "scope": "Phase 0, Phase 1, Phase 1B and historical Phase 1C",
        "definition_of_done": [
            "Every historical blocking review item has a closed final status.",
            "No active closure matrix item remains open, pending_review or unknown.",
            "Only evidence-backed display-slice facts are runtime-approved.",
            "Deferred and quarantine decisions include explicit non-promotion reasons.",
            "Phase 1C is formally superseded by Phase 1D without reinterpreting old evidence.",
            "Raw C# and decompiler bodies remain evidence-only and are never runtime imports.",
        ],
        "counts": matrix["counts"],
        "blocking_review_items": [],
        "open_items": [],
        "authority": {
            "matrix": {"path": "knowledge/fixtures/accepted/semantic_review_closure.json", "content_hash": matrix["content_hash"]},
            "load_contract": {"path": "knowledge/fixtures/accepted/load_contract_closure.json", "content_hash": load_closure["content_hash"]},
            "data_contract": {"path": "knowledge/fixtures/accepted/runtime/data_contract.json", "content_hash": data_contract["content_hash"]},
            "entity_contract": {"path": "knowledge/fixtures/accepted/runtime/entity_contract.json", "content_hash": entity_contract["content_hash"]},
            "save_contract": {"path": "knowledge/fixtures/accepted/runtime/save_contract.json", "content_hash": save_contract["content_hash"]},
            "phase1_supersession": {"path": "knowledge/fixtures/accepted/phase1_supersession.json", "content_hash": supersession["content_hash"]},
        },
        "upstream_gates": [
            evidence_ref(PATHS["phase1d_closure"], upstream["phase1d_closure"]),
            evidence_ref(PATHS["scene_catalog"], upstream["scene_catalog"]),
            evidence_ref(PATHS["object_catalog"], upstream["object_catalog"]),
            evidence_ref(PATHS["actor_catalog"], upstream["actor_catalog"]),
        ],
        "artifact_hashes": artifact_hashes,
    }
    package["knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json"] = finalise("pre_runtime_closure_contract.json", closure_payload)
    return package


def write_package(package: dict[str, dict[str, Any]]) -> None:
    for relative, payload in package.items():
        write_json(ROOT / relative, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the closure artifacts")
    args = parser.parse_args()
    package = build_package()
    if args.write:
        write_package(package)
    matrix = package["knowledge/fixtures/accepted/semantic_review_closure.json"]
    contract = package["knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json"]
    print(
        "pre_runtime_closure_built "
        f"items={matrix['counts']['total_items']} "
        f"blocking_remaining={matrix['counts']['blocking_items_remaining']} "
        f"status={contract['semantic_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
