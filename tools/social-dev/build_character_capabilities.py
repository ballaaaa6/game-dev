"""Build the shared character-family and animation capability contract.

The character metadata catalog owns source identity. This package owns the
reusable runtime capability profiles that turn that identity into a lazy spawn
plan. It records selector readiness explicitly and never invents a distinct
animation set for every source character.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_character_metadata as metadata_builder


ROOT = metadata_builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
METADATA_PATH = RUNTIME_EVIDENCE / "character_metadata_contract.json"
NATIVE_CONTENT_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
ACTOR_BEHAVIOR_PATH = RUNTIME_EVIDENCE / "actor_behavior_contract.json"
AVATAR_SOURCE_PATH = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs"

SCHEMA_VERSION = "social-dev-character-capability-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-character-capability-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-character-capability-validation-v1"

DIRECTIONS = ("right", "left", "up", "down")
NATIVE_DIRECTION_SUFFIXES = tuple(f"_{direction}" for direction in DIRECTIONS)
BASIC_ACTION_FILES = {
    "move": ("walk_right.seb", "walk_left.seb", "walk_up.seb", "walk_down.seb"),
    "wait": ("wait_right.seb", "wait_left.seb", "wait_up.seb", "wait_down.seb"),
    "typing": ("typing_right.seb", "typing_left.seb", "typing_up.seb", "typing_down.seb"),
}


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


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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


def evidence_ref(path: Path) -> dict[str, str]:
    require(path.is_file(), f"missing evidence file: {path}")
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def selector_row(native_content: dict[str, Any], filename: str) -> dict[str, Any]:
    matches = [
        row
        for row in native_content["selectors"]
        if row.get("resource_scope") == "human"
        and row.get("selector_kind") == "seb"
        and row.get("target_filename") == filename
    ]
    require(len(matches) == 1, f"expected one human SEB selector for {filename}, got {len(matches)}")
    row = matches[0]
    require(row.get("status") == "resolved", f"human SEB selector is not resolved: {filename}")
    return row


def compact_selector(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "selector_id": row["selector_id"],
        "selector_key": row["selector_key"],
        "filename": row["target_filename"],
        "asset_id": row["target_asset_id"],
        "asset_member": row["target_relative_path"],
        "status": "selector_ready",
        "resolution_status": row["status"],
        "source_file": row["source_file"],
        "source_row": row["source_row"],
    }


def direction_selector_map(native_content: dict[str, Any], filenames: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    return {
        direction: compact_selector(selector_row(native_content, filename))
        for direction, filename in zip(DIRECTIONS, filenames)
    }


def build_basic_actions(native_content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    actions: dict[str, dict[str, Any]] = {}
    for action, filenames in BASIC_ACTION_FILES.items():
        actions[action] = {
            "status": "selector_ready",
            "semantic_status": "shared_native_selector_mapping",
            "selector_by_direction": direction_selector_map(native_content, filenames),
            "asset_loading": "lazy_by_selector",
            "frame_resolution_status": "native_frame_contract_ready",
        }

    # The display slice already uses typing while an actor is in talk state.
    # Keep that mapping explicit instead of pretending that a distinct talk
    # SEB exists in the current source selector table.
    actions["talk"] = {
        "status": "display_ready_via_shared_profile",
        "semantic_status": "runtime_talk_to_typing_mapping",
        "source_action": "typing",
        "selector_by_direction": copy.deepcopy(actions["typing"]["selector_by_direction"]),
        "asset_loading": "lazy_by_selector",
        "note": "No distinct talk selector is promoted by the current human/seb.inf; the bounded display runtime maps talk to typing.",
    }

    for action in ("work", "equipment", "sit_down", "meeting", "invite_to_talk", "wander", "stay_home"):
        source_action = "move" if action == "wander" else "wait"
        actions[action] = {
            "status": "fallback_ready",
            "semantic_status": "shared_profile_fallback",
            "source_action": source_action,
            "fallback_action": source_action,
            "selector_by_direction": copy.deepcopy(actions[source_action]["selector_by_direction"]),
            "asset_loading": "lazy_by_selector",
            "note": "The action interface is ready, but the current evidence does not close a distinct action-specific human selector.",
        }
    actions["fly_away"] = {
        "status": "deferred",
        "semantic_status": "no_promoted_native_selector",
        "selector_by_direction": None,
        "asset_loading": "on_demand_when_source_closes",
        "note": "Keep the capability explicit so callers can handle the missing native selector without silently substituting a new animation.",
    }
    return actions


def build_native_selector_inventory(native_content: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in native_content["selectors"]
        if row.get("resource_scope") == "human" and row.get("selector_kind") == "seb"
    ]
    return [compact_selector(row) for row in sorted(rows, key=lambda item: item["selector_id"])]


def split_native_action_name(filename: str) -> tuple[str, str | None]:
    stem = Path(filename).stem
    for suffix in NATIVE_DIRECTION_SUFFIXES:
        if stem.endswith(suffix):
            return stem[: -len(suffix)], suffix[1:]
    return stem, None


def build_native_actions(native_content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Expose every native human SEB filename as a callable shared action.

    The source selector table is authoritative for which directions actually
    exist. A caller asking for an unsupported direction receives an explicit
    no-selector result instead of an invented mirrored animation.
    """
    actions: dict[str, dict[str, Any]] = {}
    rows = [
        row
        for row in native_content["selectors"]
        if row.get("resource_scope") == "human" and row.get("selector_kind") == "seb"
    ]
    for row in sorted(rows, key=lambda item: item["selector_id"]):
        action_name, direction = split_native_action_name(row["target_filename"])
        action = actions.setdefault(
            action_name,
            {
                "status": "native_selector_ready",
                "semantic_status": "native_filename_selector_mapping",
                "selector_by_direction": {},
                "selector": None,
                "asset_loading": "lazy_by_selector",
                "frame_resolution_status": "native_frame_contract_ready",
                "source_filename_stems": [],
            },
        )
        action["source_filename_stems"].append(row["target_filename"])
        selector = compact_selector(row)
        if direction is None:
            action["selector"] = selector
        else:
            action["selector_by_direction"][direction] = selector

    for action in actions.values():
        if not action["selector_by_direction"]:
            action["selector_by_direction"] = None
    return actions


def build_profiles(
    native_content: dict[str, Any],
    behavior_ref: dict[str, Any],
    avatar_ref: dict[str, Any],
    native_actions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    basic_actions = build_basic_actions(native_content)
    return [
        {
            "id": "human-staff-v1",
            "family": "human",
            "role": "staff",
            "status": "ready_for_lazy_character_resolution",
            "semantic_status": "shared_human_profile",
            "record_kinds": ["staff_data_template", "internal_assistant_template"],
            "behavior": {
                "profile_ref": "staff-living-scene-v1",
                "status": "bounded_display_behavior",
                "contract_ref": behavior_ref,
            },
            "directions": list(DIRECTIONS),
            "actions": basic_actions,
            "native_actions": native_actions,
            "native_selector_inventory_status": "all_human_seb_selectors_resolved",
            "native_selector_count": 35,
            "render_identity": {
                "character_image": "template.render.image_selector",
                "animation_selector": "profile.actions[action].selector_by_direction or profile.native_actions[action]",
                "per_character_override": "optional_template.render.animation_override; absent by default",
            },
            "asset_loading": {
                "policy": "lazy_by_selector",
                "eager_load_all_character_pngs": False,
                "eager_load_all_seb_assets": False,
                "cache_key": "asset_id",
            },
            "frame_composition": {
                "status": "native_frame_contract_ready",
                "binary_decoder": "multilayer_seb_decoder_v1",
                "frame_contract_ref": "knowledge/fixtures/accepted/runtime/character_asset_manifest.json",
                "note": "Native selectors resolve through the promoted character asset manifest and its decoded multilayer frame contract.",
            },
        },
        {
            "id": "helper-record-v1",
            "family": "helper_record",
            "role": "helper",
            "status": "ready_for_metadata_resolution",
            "semantic_status": "separate_helper_record_profile",
            "record_kinds": ["helper_data_template"],
            "behavior": {
                "profile_ref": None,
                "status": "not_promoted_as_staff_lifecycle",
                "note": "HelperData records carry effects/dialogue/image references; they are not automatically Staff ActorState instances.",
            },
            "directions": [],
            "actions": {
                "portrait": {
                    "status": "selector_conditional",
                    "source_selector": "template.render.image_selector",
                    "resolution_policy": "preserve_resolved_deferred_and_absent_states",
                },
                "dialogue": {
                    "status": "metadata_reference_only",
                    "source_fields": ["helloTalk_", "goodbyeTalk_", "execTalk_"],
                },
                "effect": {
                    "status": "metadata_reference_only",
                    "source_fields": ["effectType_", "effect_"],
                },
            },
            "asset_loading": {
                "policy": "lazy_by_record_use",
                "eager_load_all_helper_assets": False,
            },
        },
        {
            "id": "avatar-v1",
            "family": "avatar",
            "role": "avatar",
            "status": "profile_reserved_source_catalog_deferred",
            "semantic_status": "body_head_composition_boundary",
            "record_kinds": ["avatar_template"],
            "behavior": {
                "profile_ref": None,
                "status": "deferred_until_avatar_catalog",
            },
            "directions": list(DIRECTIONS),
            "actions": {},
            "composition": {
                "parts": ["body", "head"],
                "source_resource_ref": avatar_ref,
                "status": "resource_boundary_known_selector_catalog_not_promoted",
            },
            "asset_loading": {
                "policy": "lazy_by_part_selector",
                "eager_load_all_avatar_parts": False,
            },
        },
        {
            "id": "event-only-v1",
            "family": "event_only",
            "role": "event_only",
            "status": "profile_reserved",
            "semantic_status": "non_staff_scene_entity_boundary",
            "record_kinds": ["event_only_template"],
            "behavior": {
                "profile_ref": None,
                "status": "caller_owned_timeline",
            },
            "directions": [],
            "actions": {
                "event_pose": {
                    "status": "deferred_until_event_asset_catalog",
                    "selector_by_direction": None,
                }
            },
            "asset_loading": {
                "policy": "lazy_by_event_use",
                "eager_load_all_event_assets": False,
            },
        },
    ]


def build_bindings(metadata: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    staff = []
    for record in metadata["staff"]:
        staff.append(
            {
                "record_id": record["id"],
                "source_id": record["source_identity"]["source_id"],
                "record_kind": record.get("record_kind", "staff_data_template"),
                "profile_ref": record["render"]["capability_profile_ref"],
                "behavior_profile_ref": record["render"]["behavior_profile_ref"],
                "status": "ready_for_lazy_resolution",
                "image_resolution_status": record["render"]["image_selector"]["resolution_status"],
                "optional_override": None,
            }
        )
    helpers = []
    for record in metadata["helpers"]:
        helpers.append(
            {
                "record_id": record["id"],
                "source_id": record["source_identity"]["source_id"],
                "record_kind": "helper_data_template",
                "profile_ref": record["render"]["capability_profile_ref"],
                "behavior_profile_ref": None,
                "status": "ready_for_metadata_resolution",
                "image_resolution_status": record["render"]["image_selector"]["resolution_status"],
                "optional_override": None,
            }
        )
    return {"staff": staff, "helpers": helpers}


def build_checks(
    metadata: dict[str, Any],
    profiles: list[dict[str, Any]],
    bindings: dict[str, list[dict[str, Any]]],
    selector_inventory: list[dict[str, Any]],
    native_actions: dict[str, dict[str, Any]],
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

    profile_by_id = {profile["id"]: profile for profile in profiles}
    human = profile_by_id["human-staff-v1"]
    action_map = human["actions"]
    check("profile-set", set(profile_by_id) == {"human-staff-v1", "helper-record-v1", "avatar-v1", "event-only-v1"}, sorted(profile_by_id), "four shared profiles", "Family profile set is stable and explicit.")
    check("human-selector-coverage", len(selector_inventory) == 35 and all(item["resolution_status"] == "resolved" for item in selector_inventory), len(selector_inventory), 35, "Every human SEB selector is represented as a resolved native selector identity.")
    check("human-wait-directions", set(action_map["wait"]["selector_by_direction"]) == set(DIRECTIONS), sorted(action_map["wait"]["selector_by_direction"]), list(DIRECTIONS), "Wait uses one shared four-direction selector map.")
    check("human-move-directions", set(action_map["move"]["selector_by_direction"]) == set(DIRECTIONS), sorted(action_map["move"]["selector_by_direction"]), list(DIRECTIONS), "Move uses one shared four-direction selector map.")
    check("human-typing-directions", set(action_map["typing"]["selector_by_direction"]) == set(DIRECTIONS), sorted(action_map["typing"]["selector_by_direction"]), list(DIRECTIONS), "Typing uses one shared four-direction selector map.")
    represented_native_selector_ids = {
        selector["selector_id"]
        for action in native_actions.values()
        for selector in [action.get("selector")]
        if selector is not None
    }
    represented_native_selector_ids.update(
        selector["selector_id"]
        for action in native_actions.values()
        for selector in (action.get("selector_by_direction") or {}).values()
    )
    check(
        "native-action-coverage",
        len(native_actions) > 0 and represented_native_selector_ids == {item["selector_id"] for item in selector_inventory},
        {"actions": len(native_actions), "selectors": len(represented_native_selector_ids)},
        {"actions": len(native_actions), "selectors": len(selector_inventory)},
        "Every native human SEB selector is reachable through a filename-derived action identity.",
    )
    check("staff-binding-coverage", [item["source_id"] for item in bindings["staff"]] == list(range(141)), len(bindings["staff"]), 141, "All StaffData records, including special and assistant templates, bind to a shared human profile.")
    check("staff-profile-uniformity", {item["profile_ref"] for item in bindings["staff"]} == {"human-staff-v1"}, sorted({item["profile_ref"] for item in bindings["staff"]}), ["human-staff-v1"], "Per-character animation code is not duplicated across StaffData records.")
    check("special-staff-binding", all(item["profile_ref"] == "human-staff-v1" for item in bindings["staff"] if 114 <= item["source_id"] <= 129), True, True, "The named special StaffData range uses the same human capability profile unless an explicit override is added.")
    check("helper-binding-coverage", [item["source_id"] for item in bindings["helpers"]] == list(range(19)), len(bindings["helpers"]), 19, "All HelperData records remain addressable through the separate helper profile.")
    check("helper-not-staff", {item["profile_ref"] for item in bindings["helpers"]}.isdisjoint({"human-staff-v1"}), sorted({item["profile_ref"] for item in bindings["helpers"]}), ["helper-record-v1"], "Helpers are not silently promoted to Staff ActorState behavior.")
    check("lazy-assets", human["asset_loading"]["eager_load_all_character_pngs"] is False and human["asset_loading"]["eager_load_all_seb_assets"] is False, False, False, "Character PNG/SEB assets remain selector references and are loaded on demand.")
    check("explicit-action-gaps", action_map["fly_away"]["status"] == "deferred" and action_map["work"]["status"] == "fallback_ready", {"fly_away": action_map["fly_away"]["status"], "work": action_map["work"]["status"]}, "explicit status", "Unsupported native action semantics are visible to callers instead of being silently invented.")
    check("metadata-ref-integrity", all(record["render"]["capability_profile_ref"] == "human-staff-v1" for record in metadata["staff"]) and all(record["render"]["capability_profile_ref"] == "helper-record-v1" for record in metadata["helpers"]), True, True, "Metadata records point to the shared profile layer.")
    return checks


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    metadata = load_json(METADATA_PATH)
    native_content = load_json(NATIVE_CONTENT_PATH)
    behavior_ref = evidence_ref(ACTOR_BEHAVIOR_PATH)
    avatar_ref = evidence_ref(AVATAR_SOURCE_PATH)
    selector_inventory = build_native_selector_inventory(native_content)
    native_actions = build_native_actions(native_content)
    profiles = build_profiles(native_content, behavior_ref, avatar_ref, native_actions)
    bindings = build_bindings(metadata)
    checks = build_checks(metadata, profiles, bindings, selector_inventory, native_actions)
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    counts = {
        "profiles": len(profiles),
        "human_seb_selectors": len(selector_inventory),
        "staff_bindings": len(bindings["staff"]),
        "helper_bindings": len(bindings["helpers"]),
        "human_selector_ready_actions": 3,
        "human_native_actions": len(native_actions),
        "human_native_action_selectors": len(selector_inventory),
        "human_fallback_actions": sum(item["status"] == "fallback_ready" for item in profiles[0]["actions"].values()),
        "human_deferred_actions": sum(item["status"] == "deferred" for item in profiles[0]["actions"].values()),
    }
    limits = [
        "This contract defines shared capability profiles, filename-derived native actions, and selector identities; decoded frame composition is supplied by the character asset manifest.",
        "All StaffData records use the human profile by default; a future per-record override is explicit and optional.",
        "The shared state actions close wait, move, and typing selectors in four directions; talk/work/equipment mappings remain explicit fallbacks where no distinct native selector is closed.",
        "Every native human SEB filename is callable through human-staff-v1.native_actions, while unsupported directions remain explicit no-selector results.",
        "HelperData, avatar body/head composition, and event-only entities remain separate families and are not silently treated as Staff ActorState instances.",
        "Mutable position, lifecycle, route, animation frame, and gameplay values belong to runtime instances, not this contract.",
    ]
    provenance = {
        "status": "verified",
        "authorities": {
            "character_metadata": evidence_ref(METADATA_PATH),
            "native_content_catalog": evidence_ref(NATIVE_CONTENT_PATH),
            "actor_behavior_contract": behavior_ref,
            "avatar_resource_source": avatar_ref,
        },
        "source_policy": "Native/C# evidence is used to build contracts only; the browser runtime imports generated JSON, never recovered source code.",
    }
    shared = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-character-capability-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "character-capabilities-full",
        "profiles": profiles,
        "bindings": bindings,
        "native_selector_inventory": selector_inventory,
        "runtime_policy": {
            "template_lookup": "by_record_kind_and_source_id",
            "instance_creation": "lazy_on_spawn_or_scene_use",
            "animation_resolution": "character_template_to_shared_profile_to_action_or_native_filename_selector_to_decoded_frame_contract",
            "per_character_customization": "optional_override_only",
            "unsupported_action_policy": "explicit_fallback_or_deferred_status",
            "asset_loading": "lazy_selector_cache_not_eager_full_catalog",
            "source_code_imports": False,
        },
        "provenance": provenance,
        "counts": counts,
        "limits": limits,
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    shared["determinism"]["content_hash"] = sha256_bytes(stable_json(without_dynamic(shared)).encode("utf-8"))
    fixture = shared
    contract = copy.deepcopy(shared)
    contract["schema_version"] = SCHEMA_VERSION
    contract["package"] = "social-dev-character-capability"
    contract["semantic_status"] = "approved_for_runtime_contract" if status == "pass" else "invalid"
    contract["fixture_ref"] = {"path": "knowledge/fixtures/accepted/character_capability_fixture.json", "content_hash": fixture["determinism"]["content_hash"]}
    contract["determinism"] = {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""}
    contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(without_dynamic(contract)).encode("utf-8"))
    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "contract_hash": contract["determinism"]["contract_hash"],
        "fixture_hash": fixture["determinism"]["content_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {"checks": len(checks), "passed_checks": sum(item["status"] == "pass" for item in checks), **counts},
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
    write_json(evidence_dir / "character_capability_fixture.json", fixture)
    write_json(evidence_dir / "character_capability_validation.json", validation)
    write_json(runtime_dir / "character_capability_contract.json", contract)
    print(
        "character_capability_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"profiles={validation['counts']['profiles']} "
        f"staff={validation['counts']['staff_bindings']} "
        f"helpers={validation['counts']['helper_bindings']} "
        f"selectors={validation['counts']['human_seb_selectors']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
