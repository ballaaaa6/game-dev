"""Build the full source-derived Social Dev character metadata catalog.

This package keeps static source data available for lookup while keeping live
actor state outside the catalog. It reads evidence tables and approved
connection contracts only; it never executes recovered C# or copies binaries
into the browser runtime.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_behavior_candidates as base


ROOT = base.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
TABLE_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
FIELD_LOAD_PATH = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG_PATH = EVIDENCE / "csharp_update_inventory/type_catalog.json"
ASSET_SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
NATIVE_CONTENT_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"

TABLE_NAMES = {
    "StaffData": "staff.txt",
    "HelperData": "helper.txt",
    "JobData": "job.txt",
    "SkillData": "skill.txt",
}

SOURCE_FILES = {
    "DataManager": base.SOURCE_ROOT / "data/DataManager.cs",
    "StaffData": base.SOURCE_ROOT / "data/StaffData.cs",
    "HelperData": base.SOURCE_ROOT / "data/HelperData.cs",
    "JobData": base.SOURCE_ROOT / "data/JobData.cs",
    "SkillData": base.SOURCE_ROOT / "data/SkillData.cs",
    "Staff": base.SOURCE_ROOT / "game/Staff.cs",
}

SCHEMA_VERSION = "social-dev-character-metadata-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-character-metadata-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-character-metadata-validation-v1"

STAFF_FIELD_ROLES = {
    "id_": "identity",
    "lastName_": "display_name",
    "firstName_": "display_name",
    "sortId_": "catalog_sort_key",
    "img_": "human_image_selector",
    "rank_": "base_rank_value",
    "jobId_": "job_relation",
    "favorite_": "favorite_relation",
    "hobby_": "hobby_relation",
    "defParams_": "base_stat_vector",
    "employmentFukidashi_": "employment_dialogue",
    "dismissalFukidashi_": "dismissal_dialogue",
    "area_": "area_value",
    "extraRate_": "extra_rate_value",
    "flag_": "source_flag_value",
    "evolveMaxNum_": "evolution_limit_value",
    "cost_": "recruitment_cost_value",
    "skill_": "skill_relation",
    "hitRate_": "encounter_rate_values",
    "bonusTerms_": "bonus_condition_values",
    "bonusRate_": "bonus_rate_value",
}

HELPER_FIELD_ROLES = {
    "id_": "identity",
    "name_": "display_name",
    "explain_": "description",
    "term_": "duration_value",
    "rate_": "rate_value",
    "rank_": "helper_rank_value",
    "costType_": "cost_type_value",
    "cost_": "cost_value",
    "img_": "helper_image_selector",
    "bigImg_": "helper_big_image_selector",
    "helloTalk_": "hello_dialogue_reference",
    "goodbyeTalk_": "goodbye_dialogue_reference",
    "execTalk_": "execution_dialogue_reference",
    "effectType_": "effect_type_value",
    "effect_": "effect_values",
    "flag_": "source_flag_value",
}

JOB_FIELD_ROLES = {
    "id_": "identity",
    "name_": "display_name",
    "type_": "job_type_value",
    "jobGroup_": "job_group_value",
    "evolutionJob_": "evolution_job_relation",
    "evolutionCost_": "evolution_cost_value",
    "maxLv_": "max_level_value",
    "speed_": "speed_value",
    "params_": "job_stat_modifier_values",
    "bonus_": "job_bonus_values",
    "icon_": "job_icon_selector",
    "evolutionItems_": "evolution_item_values",
}

SKILL_FIELD_ROLES = {
    "id_": "identity",
    "name_": "display_name",
    "type_": "skill_type_value",
    "scene_": "skill_scene_value",
    "target_": "skill_target_value",
    "attribute_": "skill_attribute_value",
    "effects_": "effect_values",
    "auraRates_": "aura_rate_values",
    "flag_": "source_flag_value",
    "explain_": "description",
}

VERIFIED_FIELD_NAMES = {
    "StaffData": {"id_", "lastName_", "firstName_", "img_", "jobId_", "skill_"},
    "HelperData": {"id_", "name_", "explain_"},
    "JobData": {"id_", "name_"},
    "SkillData": {"id_", "name_", "explain_"},
}

STAFF_FLAG_BITS = [
    {"name": "FLAG_SPECIAL", "value": 1},
    {"name": "FLAG_INIT_FIND", "value": 2},
    {"name": "FLAG_RECRUIT", "value": 4},
]

RUNTIME_STATE_BOUNDARY = {
    "catalog_owns": [
        "source identity",
        "localized names and source dialogue",
        "static numeric fields and relations",
        "selector references and asset provenance",
    ],
    "mutable_actor_state_owner": "ActorState",
    "mutable_actor_state_fields": [
        "instance_id",
        "level",
        "exp",
        "current_params",
        "current_job_id",
        "room_id",
        "desk_id",
        "position",
        "lifecycle",
        "facing",
        "route",
        "animation_frame",
    ],
    "policy": "Retain all loaded static source fields; do not copy live gameplay state into the metadata catalog.",
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


def evidence_ref(path: Path) -> dict[str, str]:
    require(path.is_file(), f"missing evidence file: {path}")
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = [evidence_ref(path) for path in sorted(set(paths), key=lambda item: str(item))]
    return {"files": files, "input_hash": sha256_bytes(stable_json(files).encode("utf-8"))}


def table_path(type_name: str, locale: str) -> Path:
    path = TABLE_ROOT / f"{locale}.lproj" / TABLE_NAMES[type_name]
    require(path.is_file(), f"missing {type_name}/{locale} table: {path}")
    return path


def read_locale_records(
    type_name: str,
    locale: str,
    field_loads: list[dict[str, Any]],
    type_sources: list[dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    path = table_path(type_name, locale)
    rows = base.read_table(path)
    field_load = base.find_field_load(field_loads, type_name)
    type_source = base.find_type_source(type_sources, type_name)
    records: dict[int, dict[str, Any]] = {}
    for row in rows:
        parsed = base.parse_row(type_name, locale, row, field_load, type_source, path)
        require(parsed["parse"]["status"] == "pass", f"{type_name}/{locale}/{row['id']} did not parse")
        require(parsed["id"] not in records, f"duplicate {type_name}/{locale}/{parsed['id']}")
        records[parsed["id"]] = parsed
    return records


def field_value(record: dict[str, Any], name: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(name, {}).get("value", default)


def row_ref(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": record["type"],
        "locale": record["locale"],
        "id": record["id"],
        "table_path": record["table_path"],
        "row_number": record["row_number"],
        "row_sha256": record["row_sha256"],
        "parse_status": record["parse"]["status"],
    }


def build_source_fields(
    type_name: str,
    record: dict[str, Any],
    roles: dict[str, str],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for name, parsed in record["parsed_fields"].items():
        verified = name in VERIFIED_FIELD_NAMES[type_name]
        result[name] = {
            "value": copy.deepcopy(parsed["value"]),
            "status": "verified" if verified else "raw_only",
            "semantic_status": "loader_field" if verified else "source_value",
            "runtime_usage": roles.get(name, "source_metadata"),
            "source_field": name,
            "reader": parsed["reader"],
            "token_range": [parsed["token_start"], parsed["token_end_exclusive"]],
            "mapping_status": parsed["mapping_status"],
            "confidence": "high" if verified else "source_only",
            "review_note": (
                "Loader-aware identity or relation field is retained for runtime lookup."
                if verified
                else "Exact source value is retained; broader gameplay semantics are not promoted."
            ),
        }
    return result


def localized_name(
    type_name: str,
    english: dict[str, Any],
    japanese: dict[str, Any],
) -> dict[str, Any]:
    if type_name == "StaffData":
        values = {
            "English": f"{field_value(english, 'lastName_')} {field_value(english, 'firstName_')}",
            "Japanese": f"{field_value(japanese, 'lastName_')} {field_value(japanese, 'firstName_')}",
        }
    else:
        values = {"English": field_value(english, "name_"), "Japanese": field_value(japanese, "name_")}
    return {
        "values": values,
        "status": "verified",
        "semantic_status": "locale_value",
        "confidence": "high",
        "review_note": "Names are retained as exact locale source values.",
    }


def localized_field(
    english: dict[str, Any],
    japanese: dict[str, Any],
    name: str,
    semantic_status: str,
) -> dict[str, Any]:
    return {
        "values": {"English": field_value(english, name), "Japanese": field_value(japanese, name)},
        "status": "verified",
        "semantic_status": semantic_status,
        "confidence": "high",
        "source_field": name,
        "review_note": "Locale values are retained without translation or semantic rewriting.",
    }


def build_flag_bits(raw_value: Any) -> dict[str, Any]:
    value = int(raw_value)
    return {
        "raw_value": value,
        "known_bits": [
            {"name": item["name"], "value": item["value"], "enabled": (value & item["value"]) != 0, "status": "raw_only"}
            for item in STAFF_FLAG_BITS
        ],
        "status": "raw_only",
        "semantic_status": "source_flag_labels",
        "confidence": "source_only",
        "review_note": "Named bits are preserved from StaffData.cs; product-level availability is not inferred.",
    }


def build_asset_ref(asset: dict[str, Any]) -> dict[str, Any]:
    return {
        "asset_id": asset["asset_id"],
        "member": asset["relative_path"],
        "filename": asset.get("original_name"),
        "kind": asset.get("kind"),
        "pack": asset.get("pack"),
        "size_bytes": asset.get("size_bytes", asset.get("size")),
        "width": asset.get("width"),
        "height": asset.get("height"),
        "format": asset.get("format"),
        "sha256": asset.get("sha256"),
        "source_status": asset.get("source_status", "native_source"),
        "status": "verified",
    }


def build_selector_ref(
    connection: dict[str, Any] | None,
    raw_value: Any,
    asset_by_id: dict[str, dict[str, Any]],
    selector_field: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": raw_value,
        "field": selector_field,
        "status": "raw_only",
        "resolution_status": "not_promoted",
        "confidence": "source_only",
        "review_note": "Selector value is preserved; no approved runtime asset binding is available for this field.",
    }
    if raw_value is None or int(raw_value) < 0:
        result.update(
            {
                "status": "verified",
                "resolution_status": "absent_by_sentinel",
                "confidence": "high",
                "review_note": "Negative selector is an explicit absent sentinel in the source row.",
            }
        )
        return result
    if connection is None:
        return result
    connection_status = connection.get("status")
    if connection_status == "resolved" and connection.get("target_asset_id"):
        asset = asset_by_id.get(connection["target_asset_id"])
        require(asset is not None, f"missing asset for selector connection {connection}")
        result.update(
            {
                "status": "verified",
                "resolution_status": "resolved",
                "reference": connection.get("to"),
                "asset": build_asset_ref(asset),
                "confidence": "high",
                "review_note": "Selector-to-asset identity is closed by the native content connection graph.",
            }
        )
    elif connection_status == "absent_by_sentinel":
        result.update({"status": "verified", "resolution_status": "absent_by_sentinel", "confidence": "high"})
    else:
        result.update(
            {
                "resolution_status": "deferred",
                "reference": connection.get("to"),
                "connection_status": connection_status,
                "review_note": "The source selector is retained, but its asset scope is not closed by current evidence.",
            }
        )
    return result


def build_staff_record(
    staff_id: int,
    english: dict[str, Any],
    japanese: dict[str, Any],
    connection_map: dict[tuple[str, str], dict[str, Any]],
    asset_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source_fields = build_source_fields("StaffData", english, STAFF_FIELD_ROLES)
    image_connection = connection_map.get((f"data:staff:{staff_id}", "img_"))
    require(image_connection is not None, f"missing StaffData({staff_id}) image connection")
    image_ref = build_selector_ref(image_connection, field_value(english, "img_"), asset_by_id, "img_")
    require(image_ref["resolution_status"] == "resolved", f"StaffData({staff_id}) image selector is not resolved")
    sort_id = int(field_value(english, "sortId_"))
    is_internal_assistant = sort_id == -1 and field_value(english, "lastName_") == "Assistant"
    return {
        "id": f"staff:{staff_id}",
        "record_kind": "internal_assistant_template" if is_internal_assistant else "staff_data_template",
        "record_kind_status": "derived_from_source_shape" if is_internal_assistant else "source_record",
        "status": "verified",
        "semantic_status": "approved_for_runtime_metadata",
        "source_identity": {
            "type": "StaffData",
            "id_field": "id_",
            "source_id": staff_id,
            "status": "verified",
            "confidence": "high",
            "review_note": "Stable identity is StaffData plus source id, not array position alone.",
        },
        "name": localized_name("StaffData", english, japanese),
        "source_fields": source_fields,
        "relations": {
            "job_ref": {
                "id": f"job:{field_value(english, 'jobId_')}",
                "source_id": field_value(english, "jobId_"),
                "status": "verified",
                "semantic_status": "source_relation",
            },
            "skill_ref": {
                "id": f"skill:{field_value(english, 'skill_')}",
                "source_id": field_value(english, "skill_"),
                "status": "verified",
                "semantic_status": "source_relation",
            },
        },
        "render": {
            "family": "human",
            "image_selector": image_ref,
            "animation_profile_ref": "human-living-scene-v1",
            "capability_profile_ref": "human-staff-v1",
            "behavior_profile_ref": "staff-living-scene-v1",
            "status": "selector_ready",
            "review_note": "Static visual identity is ready; live animation state remains outside this catalog.",
        },
        "source_flags": build_flag_bits(field_value(english, "flag_")),
        "provenance_ref": {
            "data_rows": {"English": row_ref(english), "Japanese": row_ref(japanese)},
            "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports.",
        },
    }


def build_generic_record(
    type_name: str,
    record_id: int,
    english: dict[str, Any],
    japanese: dict[str, Any],
    roles: dict[str, str],
    record_prefix: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "id": f"{record_prefix}:{record_id}",
        "status": "verified",
        "semantic_status": "approved_for_runtime_metadata",
        "source_identity": {
            "type": type_name,
            "id_field": "id_",
            "source_id": record_id,
            "status": "verified",
            "confidence": "high",
            "review_note": "Stable identity is the source type plus source id.",
        },
        "name": localized_name(type_name, english, japanese),
        "source_fields": build_source_fields(type_name, english, roles),
        "provenance_ref": {
            "data_rows": {"English": row_ref(english), "Japanese": row_ref(japanese)},
            "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports.",
        },
    }
    if type_name == "HelperData":
        record["description"] = localized_field(english, japanese, "explain_", "locale_description")
    return record


def build_helper_record(
    helper_id: int,
    english: dict[str, Any],
    japanese: dict[str, Any],
    connection_map: dict[tuple[str, str], dict[str, Any]],
    asset_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    record = build_generic_record("HelperData", helper_id, english, japanese, HELPER_FIELD_ROLES, "helper")
    record["render"] = {
        "family": "helper_record",
        "capability_profile_ref": "helper-record-v1",
        "image_selector": build_selector_ref(
            connection_map.get((f"data:helper:{helper_id}", "img_")),
            field_value(english, "img_"),
            asset_by_id,
            "img_",
        ),
        "big_image_selector": build_selector_ref(None, field_value(english, "bigImg_"), asset_by_id, "bigImg_"),
        "status": "selector_references_preserved",
        "review_note": "Helper selectors remain separate from StaffData/Human actor instances.",
    }
    return record


def connection_index(native_content: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for connection in native_content["connections"]["data_selector"]:
        key = (connection["from"], connection["field"])
        if key in result:
            raise ValueError(f"duplicate selector connection: {key}")
        result[key] = connection
    return result


def build_provenance(
    input_paths: list[Path],
    staff_locales: dict[str, dict[int, dict[str, Any]]],
    helper_locales: dict[str, dict[int, dict[str, Any]]],
    job_locales: dict[str, dict[int, dict[str, Any]]],
    skill_locales: dict[str, dict[int, dict[str, Any]]],
) -> dict[str, Any]:
    return {
        "status": "verified",
        "input_manifest": input_manifest(input_paths),
        "source_files": [{"type": key, **evidence_ref(path), "status": "evidence_only"} for key, path in SOURCE_FILES.items()],
        "data_tables": {
            "StaffData": {locale: evidence_ref(table_path("StaffData", locale)) for locale in staff_locales},
            "HelperData": {locale: evidence_ref(table_path("HelperData", locale)) for locale in helper_locales},
            "JobData": {locale: evidence_ref(table_path("JobData", locale)) for locale in job_locales},
            "SkillData": {locale: evidence_ref(table_path("SkillData", locale)) for locale in skill_locales},
        },
        "authorities": {
            "asset_selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
            "native_content_catalog": evidence_ref(NATIVE_CONTENT_PATH),
            "asset_index": evidence_ref(ASSET_INDEX_PATH),
        },
        "source_policy": "Source tables and native/C# evidence are extracted inputs; the browser runtime imports only this JSON contract.",
    }


def build_checks(
    staff: list[dict[str, Any]],
    helpers: list[dict[str, Any]],
    jobs: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    source_locales: dict[str, dict[str, dict[int, dict[str, Any]]]],
    connection_map: dict[tuple[str, str], dict[str, Any]],
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

    staff_ids = [item["source_identity"]["source_id"] for item in staff]
    helper_ids = [item["source_identity"]["source_id"] for item in helpers]
    job_ids = [item["source_identity"]["source_id"] for item in jobs]
    skill_ids = [item["source_identity"]["source_id"] for item in skills]
    internal_assistant_ids = list(range(20, 27)) + list(range(130, 141))
    check("staff-coverage", staff_ids == list(range(141)), staff_ids, list(range(141)), "All StaffData source ids are retained.")
    check("helper-coverage", helper_ids == list(range(19)), helper_ids, list(range(19)), "All HelperData source ids are retained separately.")
    check("job-coverage", job_ids == list(range(30)), job_ids, list(range(30)), "All referenced JobData records are retained.")
    check("skill-coverage", skill_ids == list(range(36)), skill_ids, list(range(36)), "All referenced SkillData records are retained.")
    check(
        "special-staff-coverage",
        all(staff_ids.count(item) == 1 for item in range(114, 130)),
        [item for item in range(114, 130) if item not in staff_ids],
        [],
        "The named special StaffData range remains in the full catalog.",
    )
    check(
        "internal-assistant-coverage",
        [item["source_identity"]["source_id"] for item in staff if item["record_kind"] == "internal_assistant_template"] == internal_assistant_ids,
        [item["source_identity"]["source_id"] for item in staff if item["record_kind"] == "internal_assistant_template"],
        internal_assistant_ids,
        "Assistant placeholder records are retained and explicitly marked instead of being confused with ordinary staff.",
    )
    check(
        "locale-parse",
        all(record["parse"]["status"] == "pass" for table in source_locales.values() for locales in table.values() for record in locales.values()),
        "all parsed rows",
        "pass",
        "Every English/Japanese source row used by the catalog parses through the loader-aware evidence path.",
    )
    check(
        "staff-image-resolution",
        all(item["render"]["image_selector"]["resolution_status"] == "resolved" for item in staff),
        sum(item["render"]["image_selector"]["resolution_status"] == "resolved" for item in staff),
        141,
        "Every StaffData.img_ selector resolves to a human asset identity.",
    )
    helper_render_statuses = [item["render"]["image_selector"]["resolution_status"] for item in helpers]
    check(
        "helper-selector-boundary",
        sorted(helper_render_statuses) == ["absent_by_sentinel"] + ["deferred"] * 11 + ["resolved"] * 7,
        {status: helper_render_statuses.count(status) for status in sorted(set(helper_render_statuses))},
        {"absent_by_sentinel": 1, "deferred": 11, "resolved": 7},
        "Helper image selectors preserve resolved, absent, and scope-unresolved states without inventing assets.",
    )
    check(
        "staff-relations",
        all(
            item["relations"]["job_ref"]["source_id"] in job_ids and item["relations"]["skill_ref"]["source_id"] in skill_ids
            for item in staff
        ),
        "all StaffData job/skill references",
        "resolved in catalog",
        "Every StaffData jobId_/skill_ relation points to a retained related record.",
    )
    check(
        "field-retention",
        all(
            set(item["source_fields"]) == set(source_locales["StaffData"]["English"][item["source_identity"]["source_id"]]["parsed_fields"])
            for item in staff
        ),
        "all StaffData source fields",
        "retained",
        "Static StaffData fields are not deleted merely because gameplay does not use them yet.",
    )
    dynamic_names = set(RUNTIME_STATE_BOUNDARY["mutable_actor_state_fields"])
    check(
        "runtime-state-separation",
        not any(dynamic_name in item["source_fields"] for item in staff for dynamic_name in dynamic_names),
        "no mutable runtime fields in StaffData source_fields",
        "true",
        "Mutable instance state remains outside the static metadata catalog.",
    )
    check(
        "input-provenance",
        all((ROOT / item["path"]).is_file() for item in provenance["input_manifest"]["files"]),
        len(provenance["input_manifest"]["files"]),
        "all input files exist",
        "Every catalog input is present and hashed.",
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


def compact_selector(selector: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": selector["id"],
        "field": selector["field"],
        "status": selector["status"],
        "resolution_status": selector["resolution_status"],
    }
    for key in ("reference", "connection_status"):
        if key in selector:
            result[key] = selector[key]
    if selector.get("asset"):
        asset = selector["asset"]
        result["asset"] = {
            key: asset[key]
            for key in ("asset_id", "member", "filename", "sha256", "width", "height", "format")
            if key in asset
        }
    return result


def compact_record(record: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": record["id"],
        "status": record["status"],
        "semantic_status": record["semantic_status"],
        "source_identity": {
            "type": record["source_identity"]["type"],
            "source_id": record["source_identity"]["source_id"],
        },
        "name": {"values": copy.deepcopy(record["name"]["values"])},
        "source_fields": {
            name: copy.deepcopy(field["value"])
            for name, field in record["source_fields"].items()
        },
    }
    if "record_kind" in record:
        result["record_kind"] = record["record_kind"]
    if "relations" in record:
        result["relations"] = {
            name: {
                "id": relation["id"],
                "source_id": relation["source_id"],
                "status": relation["status"],
                "semantic_status": relation["semantic_status"],
            }
            for name, relation in record["relations"].items()
        }
    if "description" in record:
        result["description"] = {"values": copy.deepcopy(record["description"]["values"])}
    if "render" in record:
        render = record["render"]
        compact_render: dict[str, Any] = {
            "family": render["family"],
            "status": render["status"],
        }
        for key in ("image_selector", "big_image_selector"):
            if key in render:
                compact_render[key] = compact_selector(render[key])
        for key in ("animation_profile_ref", "capability_profile_ref", "behavior_profile_ref"):
            if key in render:
                compact_render[key] = render[key]
        result["render"] = compact_render
    if "source_flags" in record:
        result["source_flags"] = {
            "raw_value": record["source_flags"]["raw_value"],
            "known_bits": [
                {"name": bit["name"], "value": bit["value"], "enabled": bit["enabled"]}
                for bit in record["source_flags"]["known_bits"]
            ],
        }
    return result


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    field_loads = load_json(FIELD_LOAD_PATH)["rows"]
    type_sources = load_json(TYPE_CATALOG_PATH)["records"]
    source_locales: dict[str, dict[str, dict[int, dict[str, Any]]]] = {}
    for type_name in TABLE_NAMES:
        source_locales[type_name] = {
            locale: read_locale_records(type_name, locale, field_loads, type_sources)
            for locale in ("English", "Japanese")
        }
    for type_name, locale_records in source_locales.items():
        require(set(locale_records["English"]) == set(locale_records["Japanese"]), f"{type_name} locale id sets differ")

    asset_selector = load_json(ASSET_SELECTOR_PATH)
    require(asset_selector["status"] == "pass", "asset selector contract is not pass")
    require(asset_selector["scope"]["staff_rows"] == 141, "asset selector StaffData row scope drift")
    native_content = load_json(NATIVE_CONTENT_PATH)
    require(native_content["status"] == "pass", "native content catalog is not pass")
    asset_by_id = {asset["asset_id"]: asset for asset in native_content["assets"]}
    connection_map = connection_index(native_content)

    staff = [
        build_staff_record(
            staff_id,
            source_locales["StaffData"]["English"][staff_id],
            source_locales["StaffData"]["Japanese"][staff_id],
            connection_map,
            asset_by_id,
        )
        for staff_id in sorted(source_locales["StaffData"]["English"])
    ]
    helpers = [
        build_helper_record(
            helper_id,
            source_locales["HelperData"]["English"][helper_id],
            source_locales["HelperData"]["Japanese"][helper_id],
            connection_map,
            asset_by_id,
        )
        for helper_id in sorted(source_locales["HelperData"]["English"])
    ]
    jobs = [
        build_generic_record(
            "JobData",
            job_id,
            source_locales["JobData"]["English"][job_id],
            source_locales["JobData"]["Japanese"][job_id],
            JOB_FIELD_ROLES,
            "job",
        )
        for job_id in sorted(source_locales["JobData"]["English"])
    ]
    skills = [
        build_generic_record(
            "SkillData",
            skill_id,
            source_locales["SkillData"]["English"][skill_id],
            source_locales["SkillData"]["Japanese"][skill_id],
            SKILL_FIELD_ROLES,
            "skill",
        )
        for skill_id in sorted(source_locales["SkillData"]["English"])
    ]

    input_paths = [
        FIELD_LOAD_PATH,
        TYPE_CATALOG_PATH,
        ASSET_SELECTOR_PATH,
        ASSET_INDEX_PATH,
        NATIVE_CONTENT_PATH,
        ZIP_PATH,
        *SOURCE_FILES.values(),
        *[table_path(type_name, locale) for type_name in TABLE_NAMES for locale in ("English", "Japanese")],
    ]
    provenance = build_provenance(input_paths, source_locales["StaffData"], source_locales["HelperData"], source_locales["JobData"], source_locales["SkillData"])
    checks = build_checks(staff, helpers, jobs, skills, source_locales, connection_map, provenance)
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    counts = {
        "staff_records": len(staff),
        "helper_records": len(helpers),
        "job_records": len(jobs),
        "skill_records": len(skills),
        "staff_image_selectors_resolved": sum(item["render"]["image_selector"]["resolution_status"] == "resolved" for item in staff),
        "unique_staff_image_selectors": len({item["render"]["image_selector"]["id"] for item in staff}),
        "helper_image_selectors_resolved": sum(item["render"]["image_selector"]["resolution_status"] == "resolved" for item in helpers),
        "helper_image_selectors_deferred": sum(item["render"]["image_selector"]["resolution_status"] == "deferred" for item in helpers),
        "helper_image_selectors_absent": sum(item["render"]["image_selector"]["resolution_status"] == "absent_by_sentinel" for item in helpers),
    }
    limits = [
        "This catalog contains static StaffData, HelperData, JobData, and SkillData metadata only.",
        "All source fields are retained with explicit runtime-usage labels; unused fields are not silently deleted.",
        "Mutable Staff/Actor instance state is intentionally excluded and belongs to ActorState/save state.",
        "StaffData.img_ selector identity is resolved; unresolved helper selector scopes remain deferred/raw-only.",
        "Named special StaffData records and assistant source records remain in the catalog; HelperData remains a separate role.",
        "The catalog contains references and provenance, not decoded image objects or live renderers.",
    ]
    base_payload = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-character-metadata-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "character-metadata-full",
        "staff": staff,
        "helpers": helpers,
        "jobs": jobs,
        "skills": skills,
        "runtime_state_boundary": copy.deepcopy(RUNTIME_STATE_BOUNDARY),
        "provenance": provenance,
        "counts": counts,
        "limits": limits,
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    base_payload["determinism"]["content_hash"] = sha256_bytes(stable_json(_without_dynamic(base_payload)).encode("utf-8"))

    fixture = base_payload
    compact_staff = [compact_record(item) for item in staff]
    compact_helpers = [compact_record(item) for item in helpers]
    compact_jobs = [compact_record(item) for item in jobs]
    compact_skills = [compact_record(item) for item in skills]
    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-character-metadata",
        "status": status,
        "semantic_status": "approved_for_runtime_contract" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "character-metadata-full",
        "staff": compact_staff,
        "helpers": compact_helpers,
        "jobs": compact_jobs,
        "skills": compact_skills,
        "runtime_state_boundary": copy.deepcopy(RUNTIME_STATE_BOUNDARY),
        "fixture_ref": {
            "path": "knowledge/fixtures/accepted/character_metadata_fixture.json",
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "provenance": provenance,
        "counts": counts,
        "limits": limits,
        "runtime_readiness": {
            "status": "ready_for_metadata_lookup",
            "instance_creation": "lazy_on_spawn_or_scene_use",
            "asset_loading": "selector_reference_and_cache_on_demand",
            "active_actor_state_source": "knowledge/fixtures/accepted/runtime/actor_spawn_contract.json",
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }
    contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(_without_dynamic(contract)).encode("utf-8"))
    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "input_hash": provenance["input_manifest"]["input_hash"],
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
    write_json(evidence_dir / "character_metadata_fixture.json", fixture)
    write_json(evidence_dir / "character_metadata_validation.json", validation)
    write_json(runtime_dir / "character_metadata_contract.json", contract)
    print(
        "character_metadata_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"staff={validation['counts']['staff_records']} "
        f"helpers={validation['counts']['helper_records']} "
        f"jobs={validation['counts']['job_records']} "
        f"skills={validation['counts']['skill_records']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
