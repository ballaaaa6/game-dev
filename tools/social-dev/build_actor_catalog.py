"""Build the canonical Social Dev ActorCatalog for display-slice-01.

This builder projects static StaffData identity, human selector identity, and
bounded living-scene evidence into a runtime contract. It never executes
recovered C# or native code, never treats a decompiler body as an algorithm,
and never copies PNG/SEB binaries into the runtime boundary.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_catalog as scene_builder


ROOT = scene_builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = scene_builder.SOURCE_ROOT

SCENE_CATALOG_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
OBJECT_CATALOG_PATH = RUNTIME_EVIDENCE / "object_catalog_contract.json"
ASSET_SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_VALIDATION_PATH = EVIDENCE / "asset_validation_gate.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
STAFF_SEMANTICS_PATH = EVIDENCE / "staff_semantics_contract.json"
STAFF_BEHAVIOR_PATH = EVIDENCE / "staff_behavior_candidate.json"
PHASE1D_CLOSURE_PATH = EVIDENCE / "phase1d_closure.json"
PHASE1D_VALIDATION_PATH = EVIDENCE / "phase1d_closure_validation.json"
READINESS_CONTRACT_PATHS = {
    "spawn": RUNTIME_EVIDENCE / "actor_spawn_contract.json",
    "camera_coordinate": RUNTIME_EVIDENCE / "camera_coordinate_contract.json",
    "behavior": RUNTIME_EVIDENCE / "actor_behavior_contract.json",
    "tick": RUNTIME_EVIDENCE / "tick_order_contract.json",
}
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"

FIELD_LOAD_PATH = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG_PATH = EVIDENCE / "csharp_update_inventory/type_catalog.json"

SOURCE_FILES = {
    "StaffData": SOURCE_ROOT / "data/StaffData.cs",
    "JobData": SOURCE_ROOT / "data/JobData.cs",
    "SkillData": SOURCE_ROOT / "data/SkillData.cs",
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "StringArrayStream": SOURCE_ROOT / "ext.util/StringArrayStream.cs",
}

SELECTED_STAFF_IDS = [0, 1, 2, 3, 4]
SELECTED_JOB_ID = 4
SELECTED_SKILL_ID = 1
EXPECTED_IMAGE_IDS = {0: 86, 1: 87, 2: 88, 3: 89, 4: 90}
EXPECTED_WAIT_IDS = [10, 11, 12, 13]
EXPECTED_TYPING_IDS = [23, 24, 25, 26]
EXPECTED_ROUTE_MAPPING = {
    "MOVE_MODE_GOTO_EQUIPMENT": {"value": 1, "astar_flag": 2},
    "MOVE_MODE_TO_STAFF": {"value": 7, "astar_flag": 4},
    "MOVE_MODE_GOTO_DESK": {"value": 3, "astar_flag": 1},
}
EXPECTED_TALK_FRAMES = [20, 70, 110, 130]
ALLOWED_STATUSES = {"verified", "derived", "raw_only", "deferred", "quarantine"}

SCHEMA_VERSION = "social-dev-actor-catalog-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-actor-catalog-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-actor-catalog-validation-v1"


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
        return str(candidate).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def field(record: dict[str, Any], name: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(name, {}).get("value", default)


def row_ref(record: dict[str, Any]) -> dict[str, Any]:
    return scene_builder.row_ref(record)


def evidence_ref(path: Path) -> dict[str, str]:
    require(path.is_file(), f"missing evidence file: {path}")
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = [evidence_ref(path) for path in sorted(set(paths), key=lambda item: str(item))]
    return {"files": files, "input_hash": sha256_bytes(stable_json(files).encode("utf-8"))}


def read_record(type_name: str, locale: str, row_id: int) -> dict[str, Any]:
    record = scene_builder.read_table_record(type_name, locale, row_id)
    require(record["parse"]["status"] == "pass", f"{type_name}/{locale}/{row_id} did not parse")
    return record


def normalize_asset_member(member: str) -> str:
    prefix = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
    return member[len(prefix) :] if member.startswith(prefix) else member


def asset_index_map(asset_index: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["relative_path"]): item for item in asset_index}


def source_slice_refs(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for item in candidate.get("source_slices", []):
        path = ROOT / item["file"]
        expected_file_hash = item.get("file_sha256")
        expected_slice_hash = item.get("slice_sha256")
        if not path.is_file():
            refs.append(
                {
                    "type": item.get("type"),
                    "file": item.get("file"),
                    "line_start": item.get("line_start"),
                    "line_end": item.get("line_end"),
                    "purpose": item.get("purpose"),
                    "expected_file_sha256": expected_file_hash,
                    "expected_slice_sha256": expected_slice_hash,
                    "actual_file_sha256": None,
                    "actual_slice_sha256": None,
                    "hash_status": "missing",
                }
            )
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        start = int(item["line_start"])
        end = int(item["line_end"])
        slice_text = "".join(lines[start - 1 : end])
        actual_file_hash = sha256_file(path)
        actual_slice_hash = sha256_bytes(slice_text.encode("utf-8"))
        refs.append(
            {
                "type": item.get("type"),
                "file": item.get("file"),
                "line_start": start,
                "line_end": end,
                "purpose": item.get("purpose"),
                "expected_file_sha256": expected_file_hash,
                "expected_slice_sha256": expected_slice_hash,
                "actual_file_sha256": actual_file_hash,
                "actual_slice_sha256": actual_slice_hash,
                "il_marker_count": item.get("il_marker_count"),
                "hash_status": "pass"
                if actual_file_hash == expected_file_hash and actual_slice_hash == expected_slice_hash
                else "drift",
            }
        )
    return refs


def status_field(
    value: Any,
    status: str,
    semantic_status: str,
    source_field: str,
    review_note: str,
    confidence: str = "high",
    evidence_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    require(status in ALLOWED_STATUSES, f"invalid field status: {status}")
    result: dict[str, Any] = {
        "value": copy.deepcopy(value),
        "status": status,
        "semantic_status": semantic_status,
        "source_field": source_field,
        "confidence": confidence,
        "review_note": review_note,
    }
    if evidence_refs:
        result["evidence_refs"] = copy.deepcopy(evidence_refs)
    return result


def load_authority() -> dict[str, Any]:
    scene = load_json(SCENE_CATALOG_PATH)
    objects = load_json(OBJECT_CATALOG_PATH)
    selectors = load_json(ASSET_SELECTOR_PATH)
    asset_validation = load_json(ASSET_VALIDATION_PATH)
    asset_index = load_json(ASSET_INDEX_PATH)
    semantics = load_json(STAFF_SEMANTICS_PATH)
    behavior_candidate = load_json(STAFF_BEHAVIOR_PATH)
    closure = load_json(PHASE1D_CLOSURE_PATH)
    closure_validation = load_json(PHASE1D_VALIDATION_PATH)
    readiness_contracts = {name: load_json(path) for name, path in READINESS_CONTRACT_PATHS.items()}

    require(
        scene.get("status") == "pass"
        and scene.get("semantic_status") == "approved_for_runtime_contract",
        "SceneCatalog is not approved_for_runtime_contract",
    )
    require(
        objects.get("status") == "pass"
        and objects.get("semantic_status") == "approved_for_runtime_contract",
        "ObjectCatalog is not approved_for_runtime_contract",
    )
    require(selectors.get("status") == "pass" and selectors.get("unresolved") == [], "asset selector contract is not closed")
    require(semantics.get("status") == "pass", "staff semantics contract is not pass")
    require(
        closure.get("status") == "pass"
        and closure.get("semantic_status") == "closed_for_phase2_entry",
        "Phase 1D closure is not closed_for_phase2_entry",
    )
    require(closure_validation.get("status") == "pass" and closure_validation.get("failed_checks") == [], "Phase 1D validation failed")
    require(asset_validation.get("status") == "evidence_gate_only", "unexpected asset validation status")
    require(isinstance(asset_index, list) and len(asset_index) == asset_validation.get("asset_index_count"), "asset index count drift")
    require(behavior_candidate.get("status") == "candidate", "staff behavior candidate status changed unexpectedly")
    require(
        all(
            contract.get("status") == "pass"
            and contract.get("semantic_status") == "approved_for_runtime_contract"
            for contract in readiness_contracts.values()
        ),
        "Phase 2C readiness contracts are not approved",
    )
    return {
        "scene": scene,
        "objects": objects,
        "selectors": selectors,
        "asset_validation": asset_validation,
        "asset_index": asset_index,
        "semantics": semantics,
        "behavior_candidate": behavior_candidate,
        "closure": closure,
        "closure_validation": closure_validation,
    }


def build_portrait_selector(
    staff_id: int,
    staff_record: dict[str, Any],
    selector_record: dict[str, Any],
    asset_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    selector = selector_record["img_"]
    raw_id = field(staff_record, "img_")
    require(raw_id == selector["id"], f"StaffData({staff_id}) img_ drift")
    require(raw_id == EXPECTED_IMAGE_IDS[staff_id], f"StaffData({staff_id}) unexpected img_ id")
    require(selector.get("status") == "resolved", f"StaffData({staff_id}) image selector unresolved")
    inf_member = normalize_asset_member(selector["inf_member"])
    inf_entry = asset_map.get(inf_member)
    require(inf_entry is not None, f"human image index missing {inf_member}")
    require(inf_entry.get("sha256") == selector.get("inf_sha256"), f"human image index hash drift for {staff_id}")
    asset_member = f"01_GAME_PACKS/human/{selector['filename']}"
    asset_entry = asset_map.get(asset_member)
    require(asset_entry is not None, f"human image asset missing {asset_member}")
    return {
        "id": raw_id,
        "status": "verified",
        "resolution_status": "resolved",
        "filename": selector["filename"],
        "asset_member": asset_member,
        "asset_index": copy.deepcopy(asset_entry),
        "selector_index": {
            "member": selector["inf_member"],
            "sha256": selector["inf_sha256"],
            "status": "verified",
        },
        "confidence": "high",
        "review_note": "StaffData.img_ resolves to the indexed human image identity; frame composition remains deferred.",
    }


def build_animation_profile(semantics: dict[str, Any], asset_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    human_inf = semantics["asset_animation_provenance"]["human_seb_inf"]
    human_inf_member = normalize_asset_member(human_inf["member"])
    human_inf_entry = asset_map.get(human_inf_member)
    require(human_inf_entry is not None, f"human animation index missing {human_inf_member}")
    require(human_inf_entry.get("sha256") == human_inf["sha256"], "human animation selector-index hash drift")

    directions: list[dict[str, Any]] = []
    for pair in semantics["typing_animation"]["selector_pairs"]:
        direction: dict[str, Any] = {"reverse_direction": pair["reverse_direction"]}
        for kind in ("wait", "typing"):
            spec = pair[kind]
            asset = spec["asset"]
            require(spec["seb_id"] == asset["id"], f"{kind} selector id drift")
            expected_filename = human_inf["entries"][str(spec["seb_id"])]
            require(expected_filename == asset["filename"], f"{kind} filename drift for {spec['seb_id']}")
            asset_member = f"01_GAME_PACKS/human/{asset['filename']}"
            asset_entry = asset_map.get(asset_member)
            require(asset_entry is not None, f"human animation asset missing {asset_member}")
            require(asset["inf_sha256"] == human_inf["sha256"], f"{kind} selector index drift")
            direction[kind] = {
                "seb_id": spec["seb_id"],
                "filename": asset["filename"],
                "asset_member": asset_member,
                "asset_index": copy.deepcopy(asset_entry),
                "status": "verified",
                "confidence": "high",
                "review_note": "Selector identity is closed; binary frame composition remains outside ActorCatalog.",
            }
        directions.append(direction)

    return {
        "id": "human-living-scene-v1",
        "status": "verified",
        "semantic_status": "bounded_animation_selector_contract",
        "selector_index": {
            "member": human_inf["member"],
            "sha256": human_inf["sha256"],
            "entry_count": human_inf["entry_count"],
            "status": "verified",
        },
        "directions": directions,
        "typing_rules": {
            "start": copy.deepcopy(semantics["typing_animation"]["start"]),
            "end": copy.deepcopy(semantics["typing_animation"]["end"]),
            "status": "verified",
            "confidence": "high",
            "review_note": "Typing/wait frame selection is bounded to the approved living-scene evidence.",
        },
        "limits": [
            "Walk selectors are retained in human/seb.inf evidence but are not promoted by this contract.",
            "SEB frame composition, crop, scale, alpha, and binary promotion remain deferred.",
        ],
    }


def build_behavior_profile(semantics: dict[str, Any]) -> dict[str, Any]:
    constants = []
    for item in semantics["state_constants"]:
        constants.append(
            {
                "name": item["name"],
                "value": item["value"],
                "status": "verified",
                "semantic_status": item.get("semantic_status", "source_label_only"),
                "confidence": "high",
                "source_ref": copy.deepcopy(item["source_ref"]),
                "review_note": "Numeric source label is retained without expanding product semantics.",
            }
        )

    route_entries = []
    for item in semantics["route_mapping"]["entries"]:
        route_entries.append(
            {
                "move_mode": item["move_mode"],
                "move_mode_value": item["move_mode_value"],
                "astar_flag": item["astar_flag"],
                "status": "verified",
                "semantic_status": "source_access_policy",
                "confidence": "high",
                "review_note": "Bounded Staff-to-Astar dispatch mapping; route search implementation remains outside the catalog.",
            }
        )

    transitions = []
    for item in semantics["state_transition_contracts"]:
        transition = copy.deepcopy(item)
        transition["confidence"] = "high"
        transition["review_note"] = "Closed bounded living-scene observation; not a port of Staff.Update."
        transitions.append(transition)

    talk_transition = next(item for item in transitions if item["id"] == "talk-timing")
    skill = semantics["skill_reference"]
    effect = copy.deepcopy(skill["effect_contract"])
    effect.update(
        {
            "status": "verified",
            "semantic_status": "bounded_skill_effect",
            "confidence": "high",
            "review_note": "The selected effect identity is closed; random gauge distribution is intentionally not ported.",
        }
    )

    return {
        "id": "staff-living-scene-v1",
        "status": "verified",
        "semantic_status": "bounded_living_scene_contract",
        "source_constants": constants,
        "route_mapping": {
            "entries": route_entries,
            "status": "verified",
            "confidence": "high",
            "source_ref": copy.deepcopy(semantics["route_mapping"]["source_ref"]),
            "astar_constants": copy.deepcopy(semantics["route_mapping"]["astar_constants"]),
            "review_note": "Only the closed dispatch mapping is promoted.",
        },
        "transitions": transitions,
        "talk_timing": {
            "frame_markers": copy.deepcopy(talk_transition["frame_markers"]),
            "terminal_effect": talk_transition["terminal_effect"],
            "status": "verified",
            "confidence": "high",
            "source_ref": copy.deepcopy(talk_transition["source_ref"]),
        },
        "skill_effect": effect,
        "limits": [
            "Staff.Update and the damaged GetSkill body are not promoted as runtime algorithms.",
            "HumanMode, HumanState, and broader numeric labels remain source-labelled evidence.",
        ],
    }


def build_data_record(
    type_name: str,
    row_id: int,
    records: dict[str, dict[str, Any]],
    field_names: list[str],
    verified_fields: set[str],
) -> dict[str, Any]:
    english = records["English"]
    japanese = records["Japanese"]
    raw_fields: dict[str, Any] = {}
    for name in field_names:
        raw_fields[name] = status_field(
            field(english, name),
            "verified" if name in verified_fields else "raw_only",
            "source_value" if name not in verified_fields else "loader_field",
            name,
            "Source field retained for the selected relation; no broader gameplay meaning is inferred."
            if name not in verified_fields
            else "Loader-aware source field is cross-checked against the selected locale rows.",
        )
    return {
        "id": f"{type_name.lower().replace('data', '')}:{row_id}",
        "status": "verified",
        "semantic_status": "approved_for_runtime_contract",
        "source_identity": {
            "type": type_name,
            "id_field": "id_",
            "source_id": row_id,
            "status": "verified",
            "confidence": "high",
            "review_note": "Stable identity is type plus source id, not array position alone.",
        },
        "name": {
            "values": {"English": field(english, "name_"), "Japanese": field(japanese, "name_")},
            "status": "verified",
            "semantic_status": "locale_value",
            "confidence": "high",
            "review_note": "Names are retained as exact locale source values.",
        },
        "raw_fields": raw_fields,
        "provenance_ref": {
            "data_rows": {"English": row_ref(english), "Japanese": row_ref(japanese)},
            "source_policy": "C# is evidence-only and is not a runtime import.",
        },
    }


def build_actor_record(
    staff_id: int,
    staff_records: dict[str, dict[str, Any]],
    semantic_record: dict[str, Any],
    selector_record: dict[str, Any],
    asset_map: dict[str, dict[str, Any]],
    behavior_profile: dict[str, Any],
    animation_profile: dict[str, Any],
    job_id: int,
    skill_id: int,
) -> dict[str, Any]:
    english = staff_records["English"]
    japanese = staff_records["Japanese"]
    require(field(english, "id_") == staff_id and field(japanese, "id_") == staff_id, f"StaffData({staff_id}) locale id drift")
    require(field(english, "jobId_") == job_id, f"StaffData({staff_id}) job relation drift")
    require(field(english, "skill_") == skill_id, f"StaffData({staff_id}) skill relation drift")
    expected_name = f"{field(english, 'lastName_')} {field(english, 'firstName_')}"
    require(expected_name == semantic_record["name"], f"StaffData({staff_id}) semantic name drift")
    portrait = build_portrait_selector(staff_id, english, selector_record, asset_map)

    raw_fields = {
        "rank_": status_field(field(english, "rank_"), "raw_only", "source_value", "rank_", "Rank is retained as a source value; progression semantics are outside this catalog."),
        "area_": status_field(field(english, "area_"), "raw_only", "source_value", "area_", "Area is retained as a source value; world placement is not inferred from it."),
        "flag_": status_field(field(english, "flag_"), "raw_only", "source_value", "flag_", "StaffData flags are retained as source values; runtime flags are separate mutable state."),
    }

    return {
        "id": f"actor:staff:{staff_id}",
        "status": "verified",
        "semantic_status": "approved_for_runtime_contract",
        "source_identity": {
            "type": "StaffData",
            "id_field": "id_",
            "source_id": staff_id,
            "status": "verified",
            "confidence": "high",
            "review_note": "Stable actor identity is type plus source id.",
        },
        "name": {
            "values": {
                "English": f"{field(english, 'lastName_')} {field(english, 'firstName_')}",
                "Japanese": f"{field(japanese, 'lastName_')} {field(japanese, 'firstName_')}",
            },
            "status": "verified",
            "semantic_status": "locale_value",
            "confidence": "high",
            "review_note": "Names are retained as exact locale source values.",
        },
        "source_fields": {
            "lastName_": status_field(field(english, "lastName_"), "verified", "loader_field", "lastName_", "Loader-aware identity field cross-checked in both locales."),
            "firstName_": status_field(field(english, "firstName_"), "verified", "loader_field", "firstName_", "Loader-aware identity field cross-checked in both locales."),
            "img_": status_field(field(english, "img_"), "verified", "loader_field", "img_", "Image selector identity is closed by the asset selector contract."),
            "jobId_": status_field(field(english, "jobId_"), "verified", "relation_key", "jobId_", "StaffData.jobId_ matches JobData.id_ for the selected row."),
            "skill_": status_field(field(english, "skill_"), "verified", "relation_key", "skill_", "Skill relation is closed by the approved staff semantics contract."),
            **raw_fields,
        },
        "portrait_selector": portrait,
        "job_ref": {
            "id": f"job:{job_id}",
            "source_id": job_id,
            "status": "verified",
            "semantic_status": "source_relation",
            "confidence": "high",
            "review_note": "Reference is based on StaffData.jobId_ matching JobData.id_; no role expansion is required here.",
        },
        "skill_ref": {
            "id": f"skill:{skill_id}",
            "source_id": skill_id,
            "status": "verified",
            "semantic_status": "closed_staff_skill_relation",
            "confidence": "high",
            "review_note": "Reference is closed by Staff.Init/OnEndTyping evidence and locale-aligned SkillData rows.",
        },
        "animation_profile_ref": {
            "id": animation_profile["id"],
            "status": "verified",
            "semantic_status": "bounded_profile_reference",
            "confidence": "high",
            "review_note": "Actor references the shared human selector profile; live frame state remains in runtime state.",
        },
        "behavior_profile_ref": {
            "id": behavior_profile["id"],
            "status": "verified",
            "semantic_status": "bounded_profile_reference",
            "confidence": "high",
            "review_note": "Actor references bounded living-scene behavior evidence; Staff.Update is not ported.",
        },
        "spawn_boundary": {
            "status": "deferred",
            "semantic_status": "not_promoted",
            "confidence": "not_promoted",
            "review_note": "Initial room cell, camera coordinate, and mutable state are not closed by the current native authority package.",
        },
        "provenance_ref": {
            "data_rows": {"English": row_ref(english), "Japanese": row_ref(japanese)},
            "staff_semantics_contract": evidence_ref(STAFF_SEMANTICS_PATH),
            "asset_selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
            "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports.",
        },
    }


def build_provenance(
    authority: dict[str, Any],
    manifest: dict[str, Any],
    records: dict[int, dict[str, dict[str, Any]]],
    jobs: dict[str, dict[str, Any]],
    skills: dict[str, dict[str, Any]],
    source_slices: list[dict[str, Any]],
) -> dict[str, Any]:
    asset_selector = authority["selectors"]
    human_img = asset_selector["selected_staff"][0]["img_"]
    human_inf = authority["semantics"]["asset_animation_provenance"]["human_seb_inf"]
    return {
        "status": "verified",
        "authority": {
            "scene_catalog": evidence_ref(SCENE_CATALOG_PATH),
            "object_catalog": evidence_ref(OBJECT_CATALOG_PATH),
            "staff_semantics_contract": evidence_ref(STAFF_SEMANTICS_PATH),
            "asset_selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
            "phase1d_closure": evidence_ref(PHASE1D_CLOSURE_PATH),
            "phase1d_closure_validation": evidence_ref(PHASE1D_VALIDATION_PATH),
        },
        "input_manifest": manifest,
        "data_rows": {
            "StaffData": {
                str(staff_id): {"English": row_ref(records[staff_id]["English"]), "Japanese": row_ref(records[staff_id]["Japanese"])}
                for staff_id in SELECTED_STAFF_IDS
            },
            "JobData": {"English": row_ref(jobs["English"]), "Japanese": row_ref(jobs["Japanese"])},
            "SkillData": {"English": row_ref(skills["English"]), "Japanese": row_ref(skills["Japanese"])},
        },
        "source_slices": source_slices,
        "source_files": [
            {"type": key, **evidence_ref(path), "status": "evidence_only"}
            for key, path in SOURCE_FILES.items()
        ],
        "assets": {
            "asset_zip": {
                "path": asset_selector["asset_zip"]["path"],
                "expected_sha256": asset_selector["asset_zip"]["sha256"],
                "actual_sha256": sha256_file(ZIP_PATH),
                "hash_status": "pass" if sha256_file(ZIP_PATH) == asset_selector["asset_zip"]["sha256"] else "drift",
            },
            "asset_index": evidence_ref(ASSET_INDEX_PATH),
            "human_img_selector_index": {
                "member": human_img["inf_member"],
                "sha256": human_img["inf_sha256"],
                "status": "verified",
            },
            "human_seb_selector_index": {
                "member": human_inf["member"],
                "sha256": human_inf["sha256"],
                "entry_count": human_inf["entry_count"],
                "status": "verified",
            },
            "runtime_binary_policy": "selector identity only; no PNG/SEB binary promotion in Phase 2C",
        },
        "spawn_boundary": {
            "status": "deferred",
            "evidence_files": [evidence_ref(SOURCE_FILES["Room"]), evidence_ref(SOURCE_FILES["Staff"])],
            "reason": "Room.AddStaff and Staff initialization remain decompiler evidence; no native initial-spawn fixture is closed in this phase.",
        },
        "source_policy": "C# and native artifacts are evidence inputs only; the browser runtime must not import or execute them.",
    }


def build_checks(
    authority: dict[str, Any],
    records: dict[int, dict[str, dict[str, Any]]],
    jobs: dict[str, dict[str, Any]],
    skills: dict[str, dict[str, Any]],
    actors: list[dict[str, Any]],
    job_records: list[dict[str, Any]],
    skill_records: list[dict[str, Any]],
    animation_profile: dict[str, Any],
    behavior_profile: dict[str, Any],
    provenance: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append(
            {
                "id": check_id,
                "status": "pass" if condition else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    semantics = authority["semantics"]
    selectors = authority["selectors"]
    scene = authority["scene"]
    objects = authority["objects"]
    check(
        "scene-entry-gate",
        scene.get("status") == "pass" and scene.get("semantic_status") == "approved_for_runtime_contract",
        {"status": scene.get("status"), "semantic_status": scene.get("semantic_status")},
        {"status": "pass", "semantic_status": "approved_for_runtime_contract"},
        "ActorCatalog consumes only the approved SceneCatalog contract.",
    )
    check(
        "object-entry-gate",
        objects.get("status") == "pass" and objects.get("semantic_status") == "approved_for_runtime_contract",
        {"status": objects.get("status"), "semantic_status": objects.get("semantic_status")},
        {"status": "pass", "semantic_status": "approved_for_runtime_contract"},
        "The actor slice is anchored to the approved ObjectCatalog boundary.",
    )
    check(
        "staff-semantics-entry-gate",
        semantics.get("status") == "pass",
        {"status": semantics.get("status")},
        {"status": "pass"},
        "Bounded living-scene evidence is closed before actor projection.",
    )
    check(
        "selector-entry-gate",
        selectors.get("status") == "pass" and selectors.get("unresolved") == [],
        {"status": selectors.get("status"), "unresolved": len(selectors.get("unresolved", []))},
        {"status": "pass", "unresolved": 0},
        "Human selector identity has no unresolved entries.",
    )
    check(
        "scene-identity",
        scene["catalog_id"] == "display-slice-01" and scene["scenes"][0]["id"] == "room:0",
        {"catalog_id": scene["catalog_id"], "scene_id": scene["scenes"][0]["id"]},
        {"catalog_id": "display-slice-01", "scene_id": "room:0"},
        "ActorCatalog uses the same first scene as SceneCatalog/ObjectCatalog.",
    )
    check(
        "object-identity",
        objects["catalog_id"] == "display-slice-01" and len(objects["objects"]) == 4,
        {"catalog_id": objects["catalog_id"], "objects": len(objects["objects"])},
        {"catalog_id": "display-slice-01", "objects": 4},
        "The object authority remains the locked four-record display slice.",
    )
    check(
        "staff-selection",
        sorted(records) == SELECTED_STAFF_IDS and len(actors) == len(SELECTED_STAFF_IDS),
        {"staff_ids": sorted(records), "actors": len(actors)},
        {"staff_ids": SELECTED_STAFF_IDS, "actors": 5},
        "Exactly five selected StaffData records are projected.",
    )
    check(
        "stable-actor-ids",
        [item["id"] for item in actors] == [f"actor:staff:{item}" for item in SELECTED_STAFF_IDS],
        [item["id"] for item in actors],
        [f"actor:staff:{item}" for item in SELECTED_STAFF_IDS],
        "Actor IDs are explicit type-plus-source-id identities.",
    )
    check(
        "locale-row-parse",
        all(records[item][locale]["parse"]["status"] == "pass" for item in records for locale in ("English", "Japanese")),
        {"rows": len(records) * 2},
        {"rows": 10, "parse_status": "pass"},
        "Both locale rows parse through the loader-aware evidence path.",
    )
    check(
        "locale-id-alignment",
        all(field(records[item]["English"], "id_") == field(records[item]["Japanese"], "id_") == item for item in records),
        [field(records[item]["English"], "id_") for item in records],
        SELECTED_STAFF_IDS,
        "English/Japanese rows preserve the same source IDs.",
    )
    check(
        "locale-row-provenance",
        all(records[item][locale]["row_sha256"] for item in records for locale in ("English", "Japanese")),
        {"rows_with_hash": len(records) * 2},
        {"rows_with_hash": 10},
        "Every promoted actor row has a source row hash.",
    )
    check(
        "staff-semantic-record-alignment",
        all(
            semantics["staff_records"][item]["id"] == item
            and semantics["staff_records"][item]["img_"] == EXPECTED_IMAGE_IDS[item]
            for item in range(len(semantics["staff_records"]))
        ),
        {"records": len(semantics["staff_records"])},
        {"records": 5, "image_ids": list(EXPECTED_IMAGE_IDS.values())},
        "Approved staff semantics records align with the selected source IDs and image selectors.",
    )
    check(
        "portrait-selector-count",
        all(item["portrait_selector"]["resolution_status"] == "resolved" for item in actors),
        {"resolved": sum(item["portrait_selector"]["resolution_status"] == "resolved" for item in actors)},
        {"resolved": 5},
        "Every promoted actor image selector resolves.",
    )
    check(
        "portrait-index-members",
        all(item["portrait_selector"]["asset_member"].endswith(f"chara{EXPECTED_IMAGE_IDS[index]}.png") for index, item in enumerate(actors)),
        [item["portrait_selector"]["asset_member"] for item in actors],
        [f"01_GAME_PACKS/human/chara{value}.png" for value in EXPECTED_IMAGE_IDS.values()],
        "Human image selector identities match the indexed asset members.",
    )
    check(
        "animation-direction-count",
        len(animation_profile["directions"]) == 4,
        len(animation_profile["directions"]),
        4,
        "The approved typing/wait profile contains four direction pairs.",
    )
    check(
        "wait-selector-domain",
        [item["wait"]["seb_id"] for item in animation_profile["directions"]] == EXPECTED_WAIT_IDS,
        [item["wait"]["seb_id"] for item in animation_profile["directions"]],
        EXPECTED_WAIT_IDS,
        "Wait selectors preserve the closed human/seb.inf IDs.",
    )
    check(
        "typing-selector-domain",
        [item["typing"]["seb_id"] for item in animation_profile["directions"]] == EXPECTED_TYPING_IDS,
        [item["typing"]["seb_id"] for item in animation_profile["directions"]],
        EXPECTED_TYPING_IDS,
        "Typing selectors preserve the closed human/seb.inf IDs.",
    )
    check(
        "animation-index-members",
        all(
            item[kind]["asset_index"]["relative_path"] == item[kind]["asset_member"]
            for item in animation_profile["directions"]
            for kind in ("wait", "typing")
        ),
        {"indexed_pairs": 8},
        {"indexed_pairs": 8},
        "Every promoted wait/typing selector has an indexed asset member.",
    )
    check(
        "typing-rule-boundary",
        animation_profile["typing_rules"]["start"]["typingFrame"] == 100
        and animation_profile["typing_rules"]["start"]["sebFrameInterval"] == 3
        and animation_profile["typing_rules"]["end"]["typingFrame"] == 0
        and animation_profile["typing_rules"]["end"]["sebFrameInterval"] == 1,
        animation_profile["typing_rules"],
        {"start_frame": 100, "start_interval": 3, "end_frame": 0, "end_interval": 1},
        "Typing frame and interval transitions remain bounded evidence.",
    )
    check(
        "job-record-identity",
        len(job_records) == 1 and job_records[0]["source_identity"]["source_id"] == SELECTED_JOB_ID,
        {"records": len(job_records), "id": job_records[0]["source_identity"]["source_id"]},
        {"records": 1, "id": SELECTED_JOB_ID},
        "JobData(4) is the only selected job record.",
    )
    check(
        "skill-record-identity",
        len(skill_records) == 1 and skill_records[0]["source_identity"]["source_id"] == SELECTED_SKILL_ID,
        {"records": len(skill_records), "id": skill_records[0]["source_identity"]["source_id"]},
        {"records": 1, "id": SELECTED_SKILL_ID},
        "SkillData(1) is the only selected skill record.",
    )
    check(
        "job-relation-alignment",
        all(item["job_ref"]["source_id"] == SELECTED_JOB_ID for item in actors),
        sorted({item["job_ref"]["source_id"] for item in actors}),
        [SELECTED_JOB_ID],
        "All selected staff rows point to JobData(4).",
    )
    check(
        "skill-relation-alignment",
        all(item["skill_ref"]["source_id"] == SELECTED_SKILL_ID for item in actors)
        and semantics["skill_reference"]["staff_skill_ids_uniform"]
        and semantics["skill_reference"]["staff_skill_ids_locale_aligned"],
        {"skill_ids": sorted({item["skill_ref"]["source_id"] for item in actors}), "uniform": semantics["skill_reference"]["staff_skill_ids_uniform"]},
        {"skill_ids": [SELECTED_SKILL_ID], "uniform": True},
        "The selected skill relation is closed and locale-aligned.",
    )
    check(
        "route-mapping",
        {item["move_mode"]: {"value": item["move_mode_value"], "astar_flag": item["astar_flag"]} for item in behavior_profile["route_mapping"]["entries"]} == EXPECTED_ROUTE_MAPPING,
        {item["move_mode"]: {"value": item["move_mode_value"], "astar_flag": item["astar_flag"]} for item in behavior_profile["route_mapping"]["entries"]},
        EXPECTED_ROUTE_MAPPING,
        "Staff route dispatch preserves the three closed Astar flag mappings.",
    )
    check(
        "transition-count",
        len(behavior_profile["transitions"]) == 4,
        len(behavior_profile["transitions"]),
        4,
        "Only the four closed living-scene transitions are promoted.",
    )
    check(
        "talk-timing",
        behavior_profile["talk_timing"]["frame_markers"] == EXPECTED_TALK_FRAMES,
        behavior_profile["talk_timing"]["frame_markers"],
        EXPECTED_TALK_FRAMES,
        "Talk timing markers preserve the bounded source observation.",
    )
    check(
        "skill-effect",
        behavior_profile["skill_effect"]["type_value"] == 10
        and behavior_profile["skill_effect"]["effect_index"] == 8
        and behavior_profile["skill_effect"]["effect_value"] == 150
        and behavior_profile["skill_effect"]["flag_value"] == 1,
        behavior_profile["skill_effect"],
        {"type_value": 10, "effect_index": 8, "effect_value": 150, "flag_value": 1},
        "Selected SkillData effect identity is closed without porting its random path.",
    )
    actor_payload = stable_json(actors)
    check(
        "field-statuses",
        all(
            item.get("status") in ALLOWED_STATUSES and item.get("confidence")
            for actor in actors
            for item in [
                actor["source_identity"],
                actor["name"],
                *actor["source_fields"].values(),
                actor["portrait_selector"],
                actor["job_ref"],
                actor["skill_ref"],
                actor["animation_profile_ref"],
                actor["behavior_profile_ref"],
                actor["spawn_boundary"],
            ]
        ),
        {"actors": len(actors)},
        "Every actor field wrapper has a controlled status and confidence.",
        "Promoted actor values must not omit evidence status.",
    )
    check(
        "no-unresolved-promoted-actors",
        "unknown" not in actor_payload.lower() and all(item["status"] == "verified" for item in actors),
        {"contains_unresolved_label": "unknown" in actor_payload.lower()},
        {"contains_unresolved_label": False},
        "Unresolved semantic labels remain outside promoted actor records.",
    )
    check(
        "spawn-boundary",
        all(item["spawn_boundary"]["status"] == "deferred" for item in actors)
        and provenance["spawn_boundary"]["status"] == "deferred",
        {"actor_spawn_statuses": sorted({item["spawn_boundary"]["status"] for item in actors}), "provenance_status": provenance["spawn_boundary"]["status"]},
        {"actor_spawn_statuses": ["deferred"], "provenance_status": "deferred"},
        "Spawn is explicit and deferred; no room cell is guessed.",
    )
    check(
        "source-slice-hashes",
        len(provenance["source_slices"]) == 15 and all(item["hash_status"] == "pass" for item in provenance["source_slices"]),
        {"slices": len(provenance["source_slices"]), "hash_statuses": sorted({item["hash_status"] for item in provenance["source_slices"]})},
        {"slices": 15, "hash_status": "pass"},
        "All selected staff behavior source slices match the read-only source files.",
    )
    check(
        "input-file-provenance",
        all((ROOT / item["path"]).is_file() for item in provenance["input_manifest"]["files"]),
        {"files": len(provenance["input_manifest"]["files"])},
        "Every input manifest path exists at build time.",
        "Provenance must be complete before promotion.",
    )
    check(
        "asset-zip-hash",
        provenance["assets"]["asset_zip"]["hash_status"] == "pass",
        provenance["assets"]["asset_zip"],
        {"hash_status": "pass"},
        "Selector identity remains tied to the pinned asset ZIP.",
    )
    check(
        "source-policy",
        "runtime" not in provenance["source_policy"].lower() or "import" in provenance["source_policy"].lower(),
        provenance["source_policy"],
        "C# and native artifacts are evidence inputs only.",
        "The browser runtime must not depend on recovered source.",
    )
    check(
        "phase-boundary",
        len(actors) == 5 and animation_profile["id"] == "human-living-scene-v1" and behavior_profile["id"] == "staff-living-scene-v1",
        {"actors": len(actors), "animation_profile": animation_profile["id"], "behavior_profile": behavior_profile["id"]},
        {"actors": 5, "animation_profile": "human-living-scene-v1", "behavior_profile": "staff-living-scene-v1"},
        "Phase 2C creates contracts only; runtime core and renderer remain absent.",
    )
    return checks


def _without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [_without_dynamic(item) for item in value]
    return value


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    authority = load_authority()
    selectors = authority["selectors"]
    asset_map = asset_index_map(authority["asset_index"])
    semantic_staff = {int(item["id"]): item for item in authority["semantics"]["staff_records"]}
    selector_staff = {int(item["id"]): item for item in selectors["selected_staff"]}
    require(sorted(semantic_staff) == SELECTED_STAFF_IDS, "staff semantics IDs drift")
    require(sorted(selector_staff) == SELECTED_STAFF_IDS, "staff selector IDs drift")

    staff_records: dict[int, dict[str, dict[str, Any]]] = {
        staff_id: {
            "English": read_record("StaffData", "English", staff_id),
            "Japanese": read_record("StaffData", "Japanese", staff_id),
        }
        for staff_id in SELECTED_STAFF_IDS
    }
    jobs = {"English": read_record("JobData", "English", SELECTED_JOB_ID), "Japanese": read_record("JobData", "Japanese", SELECTED_JOB_ID)}
    skills = {"English": read_record("SkillData", "English", SELECTED_SKILL_ID), "Japanese": read_record("SkillData", "Japanese", SELECTED_SKILL_ID)}

    require(sha256_file(ZIP_PATH) == selectors["asset_zip"]["sha256"], "asset ZIP hash drift")
    animation_profile = build_animation_profile(authority["semantics"], asset_map)
    behavior_profile = build_behavior_profile(authority["semantics"])
    actor_records = [
        build_actor_record(
            staff_id,
            staff_records[staff_id],
            semantic_staff[staff_id],
            selector_staff[staff_id],
            asset_map,
            behavior_profile,
            animation_profile,
            SELECTED_JOB_ID,
            SELECTED_SKILL_ID,
        )
        for staff_id in SELECTED_STAFF_IDS
    ]
    job_record = build_data_record("JobData", SELECTED_JOB_ID, jobs, ["type_", "jobGroup_", "evolutionJob_", "speed_"], {"type_", "jobGroup_", "evolutionJob_", "speed_"})
    skill_record = build_data_record("SkillData", SELECTED_SKILL_ID, skills, ["type_", "scene_", "target_", "attribute_", "effects_", "auraRates_", "flag_"], {"type_", "scene_", "target_", "attribute_", "effects_", "auraRates_", "flag_"})

    source_paths = [
        SCENE_CATALOG_PATH,
        OBJECT_CATALOG_PATH,
        ASSET_SELECTOR_PATH,
        ASSET_VALIDATION_PATH,
        ASSET_INDEX_PATH,
        STAFF_SEMANTICS_PATH,
        STAFF_BEHAVIOR_PATH,
        PHASE1D_CLOSURE_PATH,
        PHASE1D_VALIDATION_PATH,
        FIELD_LOAD_PATH,
        TYPE_CATALOG_PATH,
        APK_PATH,
        ZIP_PATH,
        *[scene_builder.base.table_path("StaffData", locale) for locale in ("English", "Japanese")],
        *[scene_builder.base.table_path("JobData", locale) for locale in ("English", "Japanese")],
        *[scene_builder.base.table_path("SkillData", locale) for locale in ("English", "Japanese")],
        *SOURCE_FILES.values(),
    ]
    manifest = input_manifest(source_paths)
    source_slices = source_slice_refs(authority["behavior_candidate"])
    provenance = build_provenance(authority, manifest, staff_records, jobs, skills, source_slices)
    job_records = [job_record]
    skill_records = [skill_record]
    checks = build_checks(
        authority,
        staff_records,
        jobs,
        skills,
        actor_records,
        job_records,
        skill_records,
        animation_profile,
        behavior_profile,
        provenance,
    )
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    limits = [
        "This contract covers five StaffData records for display-slice-01 only.",
        "ActorCatalog contains static actor definitions; mutable ActorState is deferred to the TypeScript core.",
        "Mutable actor state remains outside ActorCatalog; the Phase 2C readiness package closes the source-bounded spawn and scene/runtime contract boundary.",
        "Wait and typing selector identity is promoted; SEB frame composition and binary promotion remain deferred.",
        "C# and native artifacts remain evidence and are not runtime imports.",
    ]
    fixture = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-actor-catalog-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "source_catalog": evidence_ref(SCENE_CATALOG_PATH)},
        "object_ref": {"catalog_id": "display-slice-01", "source_catalog": evidence_ref(OBJECT_CATALOG_PATH)},
        "actors": copy.deepcopy(actor_records),
        "job_records": copy.deepcopy(job_records),
        "skill_records": copy.deepcopy(skill_records),
        "animation_profiles": [copy.deepcopy(animation_profile)],
        "behavior_profiles": [copy.deepcopy(behavior_profile)],
        "provenance": provenance,
        "limits": limits,
        "determinism": {
            "algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash",
            "content_hash": "",
        },
    }
    fixture["determinism"]["content_hash"] = sha256_bytes(stable_json(_without_dynamic(fixture)).encode("utf-8"))

    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-actor-catalog",
        "status": status,
        "semantic_status": "approved_for_runtime_contract" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "source_catalog": evidence_ref(SCENE_CATALOG_PATH)},
        "object_ref": {"catalog_id": "display-slice-01", "source_catalog": evidence_ref(OBJECT_CATALOG_PATH)},
        "actors": copy.deepcopy(actor_records),
        "job_records": copy.deepcopy(job_records),
        "skill_records": copy.deepcopy(skill_records),
        "animation_profiles": [copy.deepcopy(animation_profile)],
        "behavior_profiles": [copy.deepcopy(behavior_profile)],
        "fixture_ref": {
            "path": "knowledge/fixtures/accepted/actor_catalog_fixture.json",
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "provenance": provenance,
        "limits": limits,
        "runtime_readiness": {
            "status": "ready_for_vite_typescript_core",
            "required_before_runtime": ["screenshot baseline", "browser behavior trace"],
            "readiness_contract_paths": [relative_path(path) for path in READINESS_CONTRACT_PATHS.values()],
            "note": "Static ActorCatalog remains separate from mutable ActorState; the Phase 2C readiness package is approved and the Vite/TypeScript core may now start.",
        },
        "determinism": {
            "algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash",
            "contract_hash": "",
        },
    }
    contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(_without_dynamic(contract)).encode("utf-8"))

    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "input_hash": manifest["input_hash"],
        "contract_hash": contract["determinism"]["contract_hash"],
        "fixture_hash": fixture["determinism"]["content_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {
            "checks": len(checks),
            "passed_checks": sum(item["status"] == "pass" for item in checks),
            "actors": len(actor_records),
            "job_records": len(job_records),
            "skill_records": len(skill_records),
            "animation_profiles": 1,
            "behavior_profiles": 1,
            "resolved_portrait_selectors": sum(item["portrait_selector"]["resolution_status"] == "resolved" for item in actor_records),
            "resolved_animation_selectors": sum(1 for item in animation_profile["directions"] for kind in ("wait", "typing") if item[kind]["status"] == "verified"),
            "deferred_spawn_boundaries": sum(item["spawn_boundary"]["status"] == "deferred" for item in actor_records),
        },
        "phase_boundary": {
            "phase": "Phase 2C",
            "next": "display-slice-contract",
            "not_started": ["deterministic ActorState core", "renderer", "Vite scaffold", "screenshot baseline", "browser behavior trace"],
        },
    }
    return fixture, contract, validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    fixture, contract, validation = build_package()
    write_json(evidence_dir / "actor_catalog_fixture.json", fixture)
    write_json(evidence_dir / "actor_catalog_validation.json", validation)
    write_json(runtime_dir / "actor_catalog_contract.json", contract)
    print(
        "actor_catalog_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"actors={validation['counts']['actors']} "
        f"portraits={validation['counts']['resolved_portrait_selectors']} "
        f"animations={validation['counts']['resolved_animation_selectors']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
