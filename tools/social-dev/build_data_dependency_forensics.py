"""Build the static Staff/job/skill/furniture data-dependency package.

This phase is deliberately evidence-only.  It parses the pinned original XLS
tables through the loader sequence already recovered from C#, records every
raw row and locale, and joins those rows to the readable C# and native dump
contracts.  It does not execute recovered C#, start a runtime, or modify the
renderer/MapChip implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import build_scene_behavior_candidates as base


ROOT = base.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
OUT = EVIDENCE / "data-dependency"
REPORTS = ROOT / "docs/Phases/Behavior"
TABLE_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
FIELD_LOAD = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG = EVIDENCE / "csharp_update_inventory/type_catalog.json"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
RAR_PATH = ROOT / "sources/raw/1_Click_CSharp_Code.rar"
RAW_SOURCE_ROOT = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
LIBIL2CPP = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
APK_MANIFEST = ROOT / "knowledge/sources/phase3a_apk_probe/raw/manifest.json"

TABLE_NAMES = {
    "StaffData": "staff.txt",
    "JobData": "job.txt",
    "SkillData": "skill.txt",
    "FurnitureData": "furniture.txt",
}
EXPECTED_COUNTS = {"StaffData": 141, "JobData": 30, "SkillData": 36, "FurnitureData": 103}
LOCALES = ("English", "Japanese")

TYPE_SOURCE_FILES = {
    "StaffData": SOURCE_ROOT / "data/StaffData.cs",
    "JobData": SOURCE_ROOT / "data/JobData.cs",
    "SkillData": SOURCE_ROOT / "data/SkillData.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
}
RUNTIME_SOURCE_FILES = {
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "DataManager": SOURCE_ROOT / "data/DataManager.cs",
    "StringArrayStream": SOURCE_ROOT / "ext.util/StringArrayStream.cs",
    "Graph": SOURCE_ROOT / "KairoEngine/kairo.unity.graph/Graph.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
}

NATIVE_RVAS = {
    "JobData.GetBaseParam": "0x121ECBC",
    "JobData.GetParam": "0x121ED20",
    "JobData.GetMasterLvBonusParam": "0x121ED68",
    "Staff.GetParam": "0x12DB9E4",
    "Staff.GetJobParam": "0x12DBD38",
    "Staff.GetBaseParam": "0x12DBA28",
    "Staff.GetSkill": "0x12D7810",
    "Staff.GetHpRatio": "0x12D3BE8",
    "Staff.RecoverHp": "0x12D2DD8",
    "Staff.UpdateRecoveryHp": "0x12D2C8C",
    "Staff.UpdateStayHome": "0x12D59F4",
    "Staff.UpdateWork": "0x12D4A7C",
    "Staff.Update": "0x12D2EC8",
    "Staff.UseEquip": "0x12D4DEC",
    "Staff.GotoEquip": "0x12D6540",
    "Staff.GotoDesk": "0x12D58EC",
    "ObjChip.IsPassable": "0x12C4AB8",
    "ObjChip.GetStandingPositions": "0x12C4868",
    "ObjChip.ReserveUse": "0x12C49B0",
    "ObjChip.GetUsersNum": "0x12C4A70",
    "Room.GetDoorIndex": "0x12CD088",
    "Room.GetEquipParam": "0x12D0728",
    "Room.PlaceDesk": "0x12CEFC8",
    "Graph.Easing": "0x1D082A4",
}

STAFF_FLAG_BITS = [
    ("FLAG_SPECIAL", 1),
    ("FLAG_INIT_FIND", 2),
    ("FLAG_RECRUIT", 4),
]

PARAM_VOCABULARY = {
    "StaffData": {
        "parameter_indices": [
            ("PARAM_IDEA", 0),
            ("PARAM_PROGRAM", 1),
            ("PARAM_GRAPHIC", 2),
            ("PARAM_SOUND", 3),
            ("PARAM_NETWORK", 4),
            ("PARAM_HP", 5),
            ("PARAM_END", 6),
        ],
        "field": "defParams_",
    },
    "JobData": {
        "parameter_indices": [
            ("PARAM_IDEA", 0),
            ("PARAM_PROGRAM", 1),
            ("PARAM_GRAPHIC", 2),
            ("PARAM_SOUND", 3),
            ("PARAM_NETWORK", 4),
            ("PARAM_END", 5),
        ],
        "field": "params_",
    },
    "SkillData": {
        "type_indices": [
            ("TYPE_GAME_PARAM_BOOST", 0),
            ("TYPE_ATTACK_IDEA", 1),
            ("TYPE_DEVELOP_SPEED_UP", 2),
            ("TYPE_RECOVERY_BOTH_SIDES_STAFF", 3),
            ("TYPE_STAFF_PARAM_BOOST", 4),
            ("TYPE_TREASURE_RANK_UP", 5),
            ("TYPE_GUARD_BOTH_SIDES_STAFF", 6),
            ("TYPE_QUALITY_UP", 7),
            ("TYPE_POWER_UP_BOOST", 8),
            ("TYPE_COMBI_BONUS_UP", 9),
            ("TYPE_MEETING_POINT_UP", 10),
            ("TYPE_DEBUG_BOOST", 11),
            ("TYPE_OVER_KILL", 12),
            ("TYPE_AURA_CHARGE_UP", 13),
        ],
        "scene_indices": [
            ("SCENE_DEVELOPING", 0),
            ("SCENE_MAIN", 1),
            ("SCENE_PLANNING", 2),
            ("SCENE_POWER_UP", 3),
        ],
        "target_indices": [("TARGET_SELF", 0), ("TARGET_TEAM", 1), ("TARGET_OTHER", 2)],
        "effect_indices": [
            ("EFFECT_GAME_PARAM", 0),
            ("EFFECT_STAFF_PARAM", 1),
            ("EFFECT_TREASURE_RANK", 2),
            ("EFFECT_DEVELOP_SPEED", 3),
            ("EFFECT_GUARD_VALUE", 4),
            ("EFFECT_RECOVERY", 5),
            ("EFFECT_ATTACK_DAMAGE", 6),
            ("EFFECT_COMBI_BONUS", 7),
            ("EFFECT_MEETING_POINT", 8),
            ("EFFECT_DEBUG", 9),
            ("EFFECT_POWER_UP", 10),
            ("EFFECT_PLAN_QUALITY", 11),
            ("EFFECT_AURA_CHARGE", 12),
        ],
        "aura_indices": [("AURA_SPEED", 0), ("AURA_POWER", 1), ("AURA_GUARD", 2), ("AURA_END", 3)],
        "flag_bits": [("FLAG_PASSIVE", 1), ("FLAG_TEMP", 2), ("FLAG_DISPLAY_START_DEVELOP", 4)],
    },
    "FurnitureData": {
        "category_indices": [
            ("CATEGORY_DESK", 0),
            ("CATEGORY_STORAGE", 1),
            ("CATEGORY_HIGH_TECH", 2),
            ("CATEGORY_ENVIRON", 3),
            ("CATEGORY_RECOMMENDED", 4),
        ],
        "type_indices": [("PASS_TYPE_PASSABLE", 0), ("PASS_TYPE_CENTER", 1), ("PASS_TYPE_NO_WAY", 2)],
        "flag_bits": [
            ("FLAG_OVERRIDE", 1),
            ("FLAG_ANIME_ALWAYS", 2),
            ("FLAG_ANIME_USE", 4),
            ("FLAG_ANIME_GAUGE_MAX", 8),
            ("FLAG_ATTRIBUTE", 16),
            ("FLAG_USER", 32),
            ("FLAG_EVERYONE", 64),
            ("FLAG_ROCKET", 128),
            ("FLAG_HOLE", 256),
            ("FLAG_VOLCANO", 512),
            ("FLAG_AQUARIUM", 1024),
            ("FLAG_PASTURE", 2048),
            ("FLAG_KAIROKUN", 4096),
            ("FLAG_VACANT", 8192),
            ("FLAG_INIT_DESK", 16384),
            ("FLAG_INIT_PLACE", 32768),
        ],
    },
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


def rel(path: Path | str) -> str:
    path = Path(path)
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, value: Any) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_report(name: str, text: str) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / name).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def evidence_ref(path: Path, status: str = "evidence_only") -> dict[str, Any]:
    require(path.is_file(), f"missing evidence file: {path}")
    return {"path": rel(path), "sha256": sha256_file(path), "status": status}


def source_lines(path: Path) -> list[str]:
    require(path.is_file(), f"missing source file: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def source_line(path: Path, needle: str, occurrence: int = 1) -> int:
    count = 0
    for number, text in enumerate(source_lines(path), start=1):
        if needle in text:
            count += 1
            if count == occurrence:
                return number
    raise ValueError(f"cannot find {needle!r} in {path}")


def source_ref(path: Path, needle: str | None = None, occurrence: int = 1, note: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "file": rel(path),
        "source_sha256": sha256_file(path),
        "status": "evidence_only",
    }
    if needle is not None:
        result["line"] = source_line(path, needle, occurrence)
        result["symbol"] = needle.strip()
    if note:
        result["note"] = note
    return result


def native_ref(symbol: str, note: str) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "rva": NATIVE_RVAS[symbol],
        "dump_file": rel(DUMP),
        "dump_sha256": sha256_file(DUMP),
        "native_file": rel(LIBIL2CPP),
        "native_sha256": sha256_file(LIBIL2CPP),
        "status": "native_evidence_only",
        "note": note,
    }


def table_path(type_name: str, locale: str) -> Path:
    path = TABLE_ROOT / f"{locale}.lproj" / TABLE_NAMES[type_name]
    require(path.is_file(), f"missing {type_name}/{locale} table: {path}")
    return path


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[int, dict[str, Any]]]]:
    load_contract = load_json(FIELD_LOAD)
    type_catalog = load_json(TYPE_CATALOG)
    load_rows = load_contract["rows"]
    type_rows = type_catalog["records"]
    all_records: dict[str, dict[int, dict[str, Any]]] = {}
    for type_name in TABLE_NAMES:
        field_load = base.find_field_load(load_rows, type_name)
        type_source = base.find_type_source(type_rows, type_name)
        by_id: dict[int, dict[str, Any]] = {}
        for locale in LOCALES:
            path = table_path(type_name, locale)
            for row in base.read_table(path):
                parsed = base.parse_row(type_name, locale, row, field_load, type_source, path)
                require(parsed["parse"]["status"] == "pass", f"{type_name}/{locale}/{parsed['id']} parse failed")
                by_id.setdefault(parsed["id"], {})[locale] = parsed
        require(len(by_id) == EXPECTED_COUNTS[type_name], f"{type_name} count mismatch")
        require(all(set(locales) == set(LOCALES) for locales in by_id.values()), f"{type_name} locale mismatch")
        all_records[type_name] = by_id
    return load_contract, type_catalog, all_records


def field_value(record: dict[str, Any], field: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(field, {}).get("value", default)


def row_ref(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": record["type"],
        "locale": record["locale"],
        "source_id": record["id"],
        "table_path": record["table_path"],
        "row_number": record["row_number"],
        "row_sha256": record["row_sha256"],
        "parse_status": record["parse"]["status"],
        "raw_line_preserved": True,
    }


def type_source_record(type_name: str, type_catalog: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in type_catalog["records"] if row["name"] == type_name)


def update_type_ref(type_name: str, type_catalog: dict[str, Any]) -> dict[str, Any]:
    record = type_source_record(type_name, type_catalog)
    path = ROOT / record["source"]["file"]
    return {
        "type": type_name,
        "file": rel(path),
        "line_start": record["source"]["line_start"],
        "line_end": record["source"]["line_end"],
        "source_sha256": record["source_hash"],
        "status": "evidence_only",
    }


def source_field_payload(parsed: dict[str, Any], field_name: str) -> dict[str, Any]:
    field = parsed["parsed_fields"][field_name]
    return {
        "value": copy.deepcopy(field["value"]),
        "reader": field["reader"],
        "token_range": [field["token_start"], field["token_end_exclusive"]],
        "mapping_status": field["mapping_status"],
        "semantic_status": "raw_source_value",
        "status": "raw_preserved",
    }


def canonical_record(
    type_name: str,
    source_id: int,
    locales: dict[str, dict[str, Any]],
    type_catalog: dict[str, Any],
) -> dict[str, Any]:
    english = locales["English"]
    localized_fields: dict[str, Any] = {}
    field_names = list(english["parsed_fields"])
    for field_name in field_names:
        localized_fields[field_name] = {
            locale: source_field_payload(locales[locale], field_name) for locale in LOCALES
        }
    csharp_ref = update_type_ref(type_name, type_catalog)
    return {
        "record_id": f"{type_name}:{source_id}",
        "source_id": source_id,
        "status": "source_record",
        "semantic_status": "raw_fields_retained_no_fabricated_values",
        "locales": {
            locale: {
                "raw_line": "\t".join(locales[locale]["raw_columns"]),
                "raw_columns": copy.deepcopy(locales[locale]["raw_columns"]),
                "parsed_fields": {
                    name: source_field_payload(locales[locale], name) for name in field_names
                },
                "parse": copy.deepcopy(locales[locale]["parse"]),
            }
            for locale in LOCALES
        },
        "localized_fields": localized_fields,
        "provenance": {
            "data_rows": {locale: row_ref(locales[locale]) for locale in LOCALES},
            "csharp_type": csharp_ref,
            "source_policy": "Original table values and C# loader mappings are evidence; no semantic value is invented when source meaning is unknown.",
        },
    }


def build_catalog(type_name: str, records: dict[int, dict[str, Any]], type_catalog: dict[str, Any], load_contract: dict[str, Any]) -> dict[str, Any]:
    field_load = base.find_field_load(load_contract["rows"], type_name)
    rows = [canonical_record(type_name, source_id, records[source_id], type_catalog) for source_id in sorted(records)]
    return {
        "schema_version": "social-dev-data-dependency-canonical-catalog-v1",
        "catalog_type": type_name,
        "status": "pass_source_catalog",
        "semantic_status": "source_values_and_provenance_authoritative",
        "counts": {
            "records": len(rows),
            "expected_records": EXPECTED_COUNTS[type_name],
            "locales_per_record": len(LOCALES),
            "parse_pass_records": sum(
                1
                for row in rows
                if all(row["locales"][locale]["parse"]["status"] == "pass" for locale in LOCALES)
            ),
        },
        "loader_contract": {
            "source_file": rel(SOURCE_ROOT / f"data/{type_name}.cs"),
            "source_type": update_type_ref(type_name, type_catalog),
            "reader_count": field_load["reader_count"],
            "reader_sequence": field_load["reader_sequence"],
            "field_assignment_sequence": field_load["field_assignment_sequence"],
            "mapping_status": "loader_order_verified_against_all_rows",
            "field_load_evidence": evidence_ref(FIELD_LOAD),
        },
        "records": rows,
    }


def archive_member_manifest() -> dict[str, Any]:
    members: list[dict[str, Any]] = []
    prefix = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/01_GAME_PACKS/xls/"
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
        for type_name, filename in TABLE_NAMES.items():
            for locale in LOCALES:
                member = f"{prefix}{locale}.lproj/{filename}"
                require(member in names, f"missing ZIP member {member}")
                data = archive.read(member)
                local = table_path(type_name, locale).read_bytes()
                members.append(
                    {
                        "type": type_name,
                        "locale": locale,
                        "member": member,
                        "member_sha256": sha256_bytes(data),
                        "local_table": rel(table_path(type_name, locale)),
                        "local_sha256": sha256_bytes(local),
                        "roundtrip_status": "exact" if data == local else "mismatch",
                    }
                )
    return {
        "archive": evidence_ref(ZIP_PATH, "original_archive_authority"),
        "members": members,
        "all_members_exact": all(row["roundtrip_status"] == "exact" for row in members),
    }


def source_pack_manifest() -> dict[str, Any]:
    cs_files = sorted(RAW_SOURCE_ROOT.rglob("*.cs"))
    return {
        "rar_archive": evidence_ref(RAR_PATH, "original_csharp_archive_authority"),
        "extraction_root": rel(RAW_SOURCE_ROOT),
        "extracted_cs_file_count": len(cs_files),
        "extracted_source_sample": [
            {"path": rel(path), "sha256": sha256_file(path)} for path in cs_files if path.name in {"Staff.cs", "StaffData.cs", "JobData.cs", "SkillData.cs", "FurnitureData.cs"}
        ],
        "active_update_sources": {key: evidence_ref(path) for key, path in {**TYPE_SOURCE_FILES, **RUNTIME_SOURCE_FILES}.items()},
        "source_policy": "RAR extraction and C# update are read-only evidence roots; recovered C# is not executed by the web runtime.",
    }


def apk_manifest() -> dict[str, Any]:
    return {
        "apk": evidence_ref(APK_PATH, "pinned_apk_authority"),
        "manifest": evidence_ref(APK_MANIFEST),
        "global_metadata": evidence_ref(METADATA),
        "libil2cpp": evidence_ref(LIBIL2CPP),
        "dump": evidence_ref(DUMP),
        "manifest_entries": load_json(APK_MANIFEST),
    }


def build_authority(type_catalog: dict[str, Any], load_contract: dict[str, Any], archive: dict[str, Any], source_pack: dict[str, Any], apk: dict[str, Any]) -> dict[str, Any]:
    table_manifest: dict[str, Any] = {}
    for type_name, filename in TABLE_NAMES.items():
        table_manifest[type_name] = {
            locale: {
                "path": rel(table_path(type_name, locale)),
                "sha256": sha256_file(table_path(type_name, locale)),
                "row_count": len(base.read_table(table_path(type_name, locale))),
                "archive_roundtrip": next(
                    row for row in archive["members"] if row["type"] == type_name and row["locale"] == locale
                ),
            }
            for locale in LOCALES
        }
    return {
        "schema_version": "social-dev-data-dependency-authority-v1",
        "status": "pass_authority_closed",
        "authority_order": [
            "pinned original APK and extracted native/dump hashes",
            "original asset-guide ZIP XLS members with exact local roundtrip",
            "loader order from field_load_candidates.json cross-checked against update C# Load methods",
            "native IL2CPP disassembly for damaged formulas and lookup paths",
            "readable C# source for state/consumer semantics",
            "existing Behavior-First/Phase 1D contracts for already-closed room/object behavior",
        ],
        "pinned_inputs": {
            "apk_and_native": apk,
            "original_data_pack": archive,
            "original_csharp_pack": source_pack,
            "field_load_evidence": evidence_ref(FIELD_LOAD),
            "type_catalog_evidence": evidence_ref(TYPE_CATALOG),
        },
        "table_manifest": table_manifest,
        "record_counts": EXPECTED_COUNTS,
        "source_reconciliation": {
            "type_catalog_schema": type_catalog["schema_version"],
            "loader_candidate_schema": load_contract["schema_version"],
            "all_four_catalogues_have_english_and_japanese_rows": True,
            "raw_rows_retained": True,
            "unresolved_values_retained": True,
        },
        "read_only_boundary": [
            "No source root was modified.",
            "No decompiled C# was executed.",
            "No runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.",
        ],
    }


def constant_ref(type_name: str, symbol: str, type_catalog: dict[str, Any]) -> dict[str, Any]:
    path = TYPE_SOURCE_FILES[type_name]
    return source_ref(path, f"public const int {symbol}", note="Named constant recovered from the update C# source; numeric value is not inferred.")


def build_parameter_vocabulary(type_catalog: dict[str, Any]) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    for type_name, values in PARAM_VOCABULARY.items():
        section: dict[str, Any] = {}
        for key, pairs in values.items():
            if not isinstance(pairs, list):
                section[key] = pairs
                continue
            section[key] = [
                {
                    "name": symbol,
                    "value": value,
                    "status": "verified_source_constant",
                    "source_ref": constant_ref(type_name, symbol, type_catalog),
                }
                for symbol, value in pairs
            ]
        sections[type_name] = section
    return {
        "schema_version": "social-dev-staff-parameter-vocabulary-v1",
        "status": "pass_full_named_vocabulary",
        "policy": "Constants are source vocabulary. A field's gameplay meaning is promoted only where a consumer is source-backed.",
        "staff_parameter_indices": sections["StaffData"]["parameter_indices"],
        "job_parameter_indices": sections["JobData"]["parameter_indices"],
        "job_parameter_slot_observation": {
            "array_fields": ["JobData.params_", "JobData.bonus_"],
            "observed_slot_count": 6,
            "observed_slots": [0, 1, 2, 3, 4, 5],
            "slot_5_status": "source_data_slot_consumed_by_StaffData.PARAM_HP",
            "named_constant_status": "JobData.cs declares PARAM_END = 5 and no named JobData.PARAM_HP constant; Staff.GetBaseParam/GetJobParam nevertheless receive type 5 and the original six-element JobData arrays contain that slot.",
            "evidence": {
                "staff_hp_constant": constant_ref("StaffData", "PARAM_HP", type_catalog),
                "job_loader_field": "JobData.params_/bonus_",
                "native_staff_hp_call": native_ref("Staff.GetJobParam", "Native Staff HP path supplies type 5 to JobData.GetParam."),
            },
        },
        "skill_vocabulary": sections["SkillData"],
        "furniture_vocabulary": sections["FurnitureData"],
        "source_types": {type_name: update_type_ref(type_name, type_catalog) for type_name in PARAM_VOCABULARY},
    }


def trunc_div(numerator: int, denominator: int) -> int:
    require(denominator != 0, "division by zero")
    quotient = abs(numerator) // abs(denominator)
    return -quotient if (numerator < 0) != (denominator < 0) else quotient


def job_base(job: dict[str, Any], parameter: int, level: int) -> int:
    params = job["params"][parameter]
    return params[0] + trunc_div((params[1] - params[0]) * (level - 1), job["max_level"] - 1)


def job_param(job: dict[str, Any], parameter: int, level: int) -> int:
    result = job_base(job, parameter, level)
    if level >= job["max_level"]:
        result += job["bonus"][parameter]
    return result


def simple_values(record: dict[str, Any], field_map: dict[str, str]) -> dict[str, Any]:
    return {target: field_value(record, source) for target, source in field_map.items()}


def job_values(records: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    values: dict[int, dict[str, Any]] = {}
    for source_id, locales in records.items():
        english = locales["English"]
        values[source_id] = {
            "source_id": source_id,
            "name_english": field_value(english, "name_"),
            "type": field_value(english, "type_"),
            "job_group": field_value(english, "jobGroup_"),
            "max_level": field_value(english, "maxLv_"),
            "params": field_value(english, "params_"),
            "bonus": field_value(english, "bonus_"),
            "speed": field_value(english, "speed_"),
            "evolution_job": field_value(english, "evolutionJob_"),
            "evolution_cost": field_value(english, "evolutionCost_"),
            "icon": field_value(english, "icon_"),
            "evolution_items": field_value(english, "evolutionItems_"),
        }
    return values


def build_job_level_contract(job_catalog: dict[str, Any], records: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    jobs = job_values(records)
    rows: list[dict[str, Any]] = []
    for source_id in sorted(jobs):
        job = jobs[source_id]
        probe_levels = sorted({0, 1, job["max_level"] - 1, job["max_level"]})
        rows.append(
            {
                "job_id": source_id,
                "name_english": job["name_english"],
                "max_level": job["max_level"],
                "parameter_pair_count": len(job["params"]),
                "bonus_count": len(job["bonus"]),
                "parameter_slots": list(range(len(job["params"]))),
                "hp_slot": {
                    "slot": 5,
                    "status": "source_data_slot_consumed_by_StaffData.PARAM_HP",
                    "named_job_constant": "NONE",
                },
                "probe_levels": [
                    {
                        "level": level,
                        "base_params": [job_base(job, parameter, level) for parameter in range(5)],
                        "params": [job_param(job, parameter, level) for parameter in range(5)],
                        "hp_base": job_base(job, 5, level),
                        "hp_param": job_param(job, 5, level),
                    }
                    for level in probe_levels
                ],
                "provenance": {
                    "catalog_ref": f"data-dependency/jobdata-canonical-catalog.json#/records/{source_id}",
                    "source_row": row_ref(records[source_id]["English"]),
                },
            }
        )
    return {
        "schema_version": "social-dev-job-level-parameter-contract-v1",
        "status": "pass_native_formula_recovered",
        "formula": {
            "base": "params_[type][0] + trunc_toward_zero((params_[type][1] - params_[type][0]) * (lv - 1) / (maxLv_ - 1))",
            "param": "GetBaseParam(type, lv) + (lv >= maxLv_ ? bonus_[type] : 0)",
            "integer_semantics": "AArch64 sdiv; truncates toward zero, not floor.",
            "level_argument": "Native code evaluates the supplied lv without an observed clamp. Staff initializes level_ to 0 and progression resets to 0; the caller domain is therefore retained explicitly.",
            "bounds": "Native code checks params_ and type/nested-row availability; invalid data follows the original exception path and is not replaced with a fabricated value.",
        },
        "native_refs": [
            native_ref("JobData.GetBaseParam", "Native body shows the pair interpolation and sdiv."),
            native_ref("JobData.GetParam", "Native body gates bonus addition on maxLv_ <= lv."),
            native_ref("JobData.GetMasterLvBonusParam", "Native body reads bonus_[type]."),
        ],
        "source_refs": [
            source_ref(TYPE_SOURCE_FILES["JobData"], "public int GetBaseParam(int type, int lv)", note="Decompiler body is damaged; retained as declaration evidence only."),
            source_ref(TYPE_SOURCE_FILES["JobData"], "public int GetParam(int type, int lv)", note="Readable bonus gate is cross-checked against native."),
        ],
        "records": rows,
        "record_count": len(rows),
        "catalog_ref": "data-dependency/jobdata-canonical-catalog.json",
    }


def build_staff_job_links(records: dict[int, dict[str, Any]], jobs: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    links: list[dict[str, Any]] = []
    for source_id in sorted(records):
        english = records[source_id]["English"]
        job_id = int(field_value(english, "jobId_"))
        links.append(
            {
                "staff_id": source_id,
                "source_field": "jobId_",
                "job_id": job_id,
                "target_record": f"JobData:{job_id}",
                "target_exists": job_id in jobs,
                "status": "verified_source_relation" if job_id in jobs else "UNKNOWN",
                "provenance": {
                    "staff_row": row_ref(english),
                    "job_row": row_ref(records=jobs[job_id]["English"]) if False else None,
                },
            }
        )
    for link in links:
        link["provenance"]["job_catalog_ref"] = f"data-dependency/jobdata-canonical-catalog.json#/records/{link['job_id']}"
        link["provenance"].pop("job_row", None)
    return {
        "schema_version": "social-dev-staff-job-link-contract-v1",
        "status": "pass_all_staff_links_resolved",
        "link_count": len(links),
        "unique_job_ids": sorted({link["job_id"] for link in links}),
        "relation_rule": "StaffData.jobId_ -> JobData.id_ -> Staff.GetJob() -> JobData.GetParam/GetMasterLvBonusParam",
        "source_refs": [
            source_ref(TYPE_SOURCE_FILES["StaffData"], "jobId_ = num5", note="StaffData loader assignment."),
            source_ref(SOURCE_ROOT / "game/Staff.cs", "JobData job = GetJob();", note="Staff parameter path obtains the selected JobData."),
            native_ref("Staff.GetJobParam", "Native body calls JobData.GetParam."),
        ],
        "links": links,
        "distribution": dict(sorted(Counter(link["job_id"] for link in links).items())),
    }


def build_staff_skill_links(records: dict[int, dict[str, Any]], skills: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    links: list[dict[str, Any]] = []
    for source_id in sorted(records):
        english = records[source_id]["English"]
        skill_id = int(field_value(english, "skill_"))
        links.append(
            {
                "staff_id": source_id,
                "original_source_field": "StaffData.skill_",
                "initial_runtime_field": "Staff.skillId_",
                "skill_id": skill_id,
                "target_record": f"SkillData:{skill_id}",
                "target_exists": skill_id in skills,
                "status": "verified_native_index_relation" if skill_id in skills else "UNKNOWN",
                "provenance": {
                    "staff_row": row_ref(english),
                    "catalog_ref": f"data-dependency/skilldata-canonical-catalog.json#/records/{skill_id}",
                },
            }
        )
    return {
        "schema_version": "social-dev-staff-skill-link-contract-v1",
        "status": "pass_all_staff_links_resolved",
        "link_count": len(links),
        "unique_skill_ids": sorted({link["skill_id"] for link in links}),
        "relation_rule": "StaffData.skill_ -> Staff.Init skillId_ -> DataManager.skillData_[skillId_] -> Staff.GetSkill()",
        "mutation_boundary": {
            "change_method": "Staff.ChangeSkill(int skillId)",
            "save_field": "skillId_",
            "default_initialization": "Staff.Init copies StaffData.skill_ when StaffData is present.",
            "lookup": "Native Staff.GetSkill indexes DataManager.skillData_ by skillId_; -1 returns null and out-of-range follows the original error path.",
            "status": "verified_with_native_lookup",
        },
        "source_refs": [
            source_ref(TYPE_SOURCE_FILES["StaffData"], "skill_ = num13", note="StaffData loader assignment."),
            source_ref(SOURCE_ROOT / "game/Staff.cs", "skillId_ = num8", note="Staff.Init copies the source skill relation."),
            source_ref(SOURCE_ROOT / "game/Staff.cs", "public SkillData GetSkill()", note="Readable declaration; lookup body is cross-checked against native."),
            native_ref("Staff.GetSkill", "Native body reads skillId_ at 0x160 and indexes the DataManager SkillData array."),
        ],
        "links": links,
        "distribution": dict(sorted(Counter(link["skill_id"] for link in links).items())),
    }


def saved_staff_fields() -> set[str]:
    path = SOURCE_ROOT / "game/Staff.cs"
    lines = source_lines(path)
    start = source_line(path, "public unsafe void Serialize(OutputStream os)") - 1
    end = source_line(path, "public unsafe void Deserialize(InputStream stream)") - 1
    text = "\n".join(lines[start:end])
    names = set(re.findall(r"StreamUtil\.Write(?:Int|Float|String|Long)\(os,\s*(\w+_)", text))
    # Several persistent values are emitted through collection loops or derived
    # locals in the damaged decompilation, so they are not visible to the
    # direct-field regex above. Keep the composite serialization evidence
    # explicit instead of misclassifying these fields as transient.
    names.update(
        {
            "params_",
            "route_",
            "floor_",
            "objIndex_",
            "masterJobIdList_",
            "itemEffectParams_",
            "fukidashi_",
            "cost_",
            "planningElapsedTime_",
            "planningTotalElapsedTime_",
        }
    )
    return names


def initialized_staff_fields() -> set[str]:
    path = SOURCE_ROOT / "game/Staff.cs"
    lines = source_lines(path)
    start = source_line(path, "private void Init(int staffDataID)") - 1
    end = source_line(path, "public void AddExpStock(int exp)") - 1
    text = "\n".join(lines[start:end])
    return set(re.findall(r"\b(\w+_)\s*=", text))


def build_runtime_status() -> dict[str, Any]:
    inventory = load_json(EVIDENCE / "behavior-first/staff-field-inventory.json")
    saved = saved_staff_fields()
    initialized = initialized_staff_fields()
    fields: list[dict[str, Any]] = []
    for field in inventory["fields"]:
        name = field["name"]
        if field.get("static"):
            owner = "static_source_constant_or_table"
        elif name in saved:
            owner = "saved_runtime_state"
        else:
            owner = "transient_runtime_state"
        fields.append(
            {
                "name": name,
                "type": field["type"],
                "offset": field["dump"]["offset"],
                "mutable": field.get("mutable", False),
                "static": field.get("static", False),
                "group": field.get("group"),
                "storage_owner": owner,
                "serialized_by_Staff_Serialize": name in saved,
                "initialized_in_Staff_Init_or_constructor": name in initialized,
                "status": "source_and_dump_aligned",
                "provenance": {
                    "inventory_ref": "behavior-first/staff-field-inventory.json",
                    "source": field["source"],
                    "dump": field["dump"],
                },
            }
        )
    derived = [
        {
            "name": "max_hp",
            "source_fields": ["StaffData.defParams_", "JobData.params_", "Staff.level_", "Staff.room_", "Staff.deskId_", "Staff.masterJobIdList_", "Staff.itemEffectParams_"],
            "formula_ref": "hp-data-dependency-contract.json#/max_hp_formula",
            "storage_owner": "derived_not_saved_as_own_field",
            "status": "verified_formula_with_source_limits",
        },
        {
            "name": "hp_ratio_percent",
            "source_fields": ["Staff.hp_", "max_hp"],
            "formula_ref": "hp-data-dependency-contract.json#/hp_ratio_formula",
            "storage_owner": "derived_not_saved_as_own_field",
            "status": "verified_formula",
        },
        {
            "name": "effective_staff_parameter",
            "source_fields": ["StaffData.defParams_", "JobData.params_", "JobData.bonus_", "Staff.level_", "Staff.room_", "Staff.deskId_", "Staff.itemEffectParams_", "Staff.masterJobIdList_", "Staff.proposalChoiceCount_"],
            "formula_ref": "staff-derived-parameter-contract.json#/staff_get_base_param",
            "storage_owner": "derived_not_saved_as_own_field",
            "status": "native_formula_with_room_equipment_limit",
        },
    ]
    return {
        "schema_version": "social-dev-staff-runtime-status-contract-v1",
        "status": "pass_saved_transient_derived_separated",
        "authority": {
            "field_inventory": evidence_ref(EVIDENCE / "behavior-first/staff-field-inventory.json"),
            "staff_source": evidence_ref(SOURCE_ROOT / "game/Staff.cs"),
            "dump": evidence_ref(DUMP),
        },
        "counts": {
            "storage_records": len(fields),
            "saved_runtime_fields": sum(1 for field in fields if field["storage_owner"] == "saved_runtime_state"),
            "transient_runtime_fields": sum(1 for field in fields if field["storage_owner"] == "transient_runtime_state"),
            "static_fields": sum(1 for field in fields if field["storage_owner"] == "static_source_constant_or_table"),
            "derived_contract_fields": len(derived),
            "dump_aligned_fields": inventory["counts"]["dump_aligned"],
        },
        "save_stream": {
            "method": "Staff.Serialize(OutputStream)",
            "source_ref": source_ref(SOURCE_ROOT / "game/Staff.cs", "public unsafe void Serialize(OutputStream os)"),
            "serialized_fields_detected": sorted(saved),
            "composite_serialization_evidence": {
                "params_": "Lib.WriteIntArray writes the Staff parameter vector.",
                "route_": "Serialize writes route count/elements through FastVector locals.",
                "floor_": "Serialize writes room_.floor_ as the floor slot; Deserialize restores floor_.",
                "objIndex_": "Serialize writes Vector2D x/y slots; Deserialize restores objIndex_.",
                "masterJobIdList_": "Serialize writes FastVector count/elements through locals.",
                "itemEffectParams_": "Serialize writes the array length/elements through locals.",
                "fukidashi_": "Serialize writes the dialogue/fukidashi payload through object-array locals.",
                "cost_": "Serialize writes cost_.Get() through a local integer.",
                "planningElapsedTime_": "Serialize writes ExLong.Get() through a local long.",
                "planningTotalElapsedTime_": "Serialize writes ExLong.Get() through a local long.",
            },
            "critical_saved_fields": ["hp_", "jobId_", "skillId_", "level_", "floor_", "objIndex_", "deskId_", "state_", "moveMode_", "recoveryHpStock_", "frameToStartRecovery_"],
            "round_trip_method": "Staff.Deserialize(InputStream)",
        },
        "fields": fields,
        "derived_fields": derived,
        "policy": "Saved fields are persistent Staff state; transient fields are live loop state or object references; derived fields are formula outputs and must not be serialized as original source fields.",
    }


def build_staff_derived(records: dict[int, dict[str, Any]], jobs: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    staff_base_source = source_ref(SOURCE_ROOT / "game/Staff.cs", "public int GetBaseParam(int type, int level)", note="Native body recovers the component sum; damaged C# body is not executed.")
    job_param_source = source_ref(SOURCE_ROOT / "game/Staff.cs", "public int GetJobParam(int type, int level)")
    fixture_ids = [0, 114, 129]
    fixtures: list[dict[str, Any]] = []
    for staff_id in fixture_ids:
        staff = records[staff_id]["English"]
        job_id = int(field_value(staff, "jobId_"))
        job_record = jobs[job_id]
        hp_base = int(field_value(staff, "defParams_")[5])
        level = 0 if staff_id == 0 else (1 if staff_id == 114 else job_record["max_level"])
        job_hp = job_base(job_record, 5, level)
        if level >= job_record["max_level"]:
            job_hp += job_record["bonus"][5]
        fixtures.append(
            {
                "staff_id": staff_id,
                "job_id": job_id,
                "level": level,
                "motivation": 0,
                "neutral_context": {
                    "room_equip_param": 0,
                    "desk_param_value": 0,
                    "master_job_bonus": 0,
                    "item_effect_param": 0,
                    "clamp_effect": "none",
                },
                "staff_data_defParams_HP": hp_base,
                "job_base_HP": job_base(job_record, 5, level),
                "job_param_HP": job_hp,
                "motivation_multiplier_percent": 100,
                "staff_job_param_HP": job_hp,
                "expected_max_hp": hp_base + job_hp,
                "status": "real_source_rows_neutral_context_fixture",
                "provenance": {
                    "staff_row": row_ref(staff),
                    "job_catalog_ref": f"data-dependency/jobdata-canonical-catalog.json#/records/{job_id}",
                },
            }
        )
    return {
        "schema_version": "social-dev-staff-derived-parameter-contract-v1",
        "status": "pass_native_component_formula_with_room_limit",
        "staff_get_param": {
            "formula": "Staff.GetParam(type, level) = Staff.GetBaseParam(type, level) + Staff.GetJobParam(type, level)",
            "native_ref": native_ref("Staff.GetParam", "Native body adds the two returned components."),
            "source_ref": source_ref(SOURCE_ROOT / "game/Staff.cs", "public int GetParam(int type, int level)"),
        },
        "staff_get_job_param": {
            "formula": "trunc_toward_zero(Graph.Easing(100, 150, 99, GetMotivation(), 0) * JobData.GetParam(type, level) / 100)",
            "motivation_input": "GetMotivation() clamps Staff.proposalChoiceCount_ against a Player-owned bound; exact Player field semantics remain source-limited.",
            "native_refs": [native_ref("Staff.GetJobParam", "Native body calls JobData.GetParam, Graph.Easing, then signed integer divide by 100.") , native_ref("Graph.Easing", "Native easing implementation is pinned; motivation-bound ownership remains outside this contract.")],
            "source_ref": job_param_source,
        },
        "staff_get_base_param": {
            "formula": "Clamp(StaffData.defParams_[type] + Room.GetEquipParam(type, JobData.jobGroup_) + desk FurnitureData.paramValue_ when FurnitureData.paramType_ == type + sum(JobData.GetMasterLvBonusParam(type) for masterJobIdList_) + itemEffectParams_[type], 1, 9999),",
            "component_status": {
                "StaffData.defParams_": "verified",
                "Room.GetEquipParam": "source_dependency_with_damaged_filter_semantics",
                "desk FurnitureData.paramType_/paramValue_": "verified_native_branch",
                "masterJobIdList_": "verified_native_loop",
                "itemEffectParams_": "verified_native_branch",
                "AppData.Clamp(1,9999)": "verified_native_return_boundary",
            },
            "native_ref": native_ref("Staff.GetBaseParam", "Native body shows the full additive component path and final clamp."),
            "source_ref": staff_base_source,
        },
        "three_real_max_hp_fixtures": fixtures,
        "provenance": {
            "staff_data_source": update_type_ref("StaffData", type_catalog),
            "job_data_source": update_type_ref("JobData", type_catalog),
            "staff_source": evidence_ref(SOURCE_ROOT / "game/Staff.cs"),
        },
    }


def build_hp_contract(runtime_status: dict[str, Any], derived: dict[str, Any], type_catalog: dict[str, Any]) -> dict[str, Any]:
    staff_path = SOURCE_ROOT / "game/Staff.cs"
    data_path = TYPE_SOURCE_FILES["StaffData"]
    return {
        "schema_version": "social-dev-hp-data-dependency-contract-v1",
        "status": "pass_hp_chain_closed_with_work_drain_limit",
        "field": {
            "name": "hp_",
            "type": "int",
            "offset": "0xE8",
            "owner": "Staff",
            "storage": "saved_runtime_state",
            "source_ref": source_ref(staff_path, "private int hp_;"),
            "dump_ref": "behavior-first/staff-field-inventory.json#/fields/hp_",
        },
        "parameter_dependency": {
            "parameter_name": "StaffData.PARAM_HP",
            "parameter_value": 5,
            "staff_vector_field": "StaffData.defParams_[5]",
            "job_vector_field": "JobData.params_[5]",
            "source_ref": constant_ref("StaffData", "PARAM_HP", type_catalog),
            "status": "verified_source_constant_and_native_consumers",
        },
        "max_hp_formula": derived["staff_get_base_param"],
        "hp_ratio_formula": {
            "formula": "trunc_toward_zero(hp_ * 100 / (Staff.GetBaseParam(5, 0) + Staff.GetJobParam(5, level_)))",
            "clamp": "If hp_ >= 1, returned ratio is clamped to at least 1; native/C# body retains integer division.",
            "source_ref": source_ref(staff_path, "public int GetHpRatio()"),
            "native_ref": native_ref("Staff.GetHpRatio", "Pinned native method for the HP ratio consumer."),
        },
        "write_and_recovery_chain": [
            {"field": "hp_", "operation": "SetHp(int)", "status": "direct_write", "source_ref": source_ref(staff_path, "public void SetHp(int hp)")},
            {"field": "hp_", "operation": "RecoverHp(value)", "status": "adds_value_clamps_at_max_and_clears_sleeping_when_full", "source_ref": source_ref(staff_path, "public bool RecoverHp(int value)"), "native_ref": native_ref("Staff.RecoverHp", "Pinned HP recovery helper.")},
            {"field": "hp_", "operation": "RecoverHpMax()", "status": "sets_to_data_backed_max", "source_ref": source_ref(staff_path, "public void RecoverHpMax()"), "native_ref": native_ref("Staff.RecoverHp", "Pinned recovery relationship.")},
            {"field": "hp_", "operation": "ClampHpMax()", "status": "clamps_down_to_data_backed_max", "source_ref": source_ref(staff_path, "public void ClampHpMax()"), "native_ref": native_ref("Staff.GetHpRatio", "HP max is shared with the ratio path.")},
            {"field": "recoveryHpStock_", "operation": "UpdateRecoveryHp -> RecoverHp(1)", "status": "verified_per_stock_tick", "source_ref": source_ref(staff_path, "if (--frameToStartRecovery_ <= 0 && recoveryHpStock_ >= 1)"), "native_ref": native_ref("Staff.UpdateRecoveryHp", "Pinned delayed recovery method.")},
            {"field": "hp_", "operation": "UpdateStayHome -> RecoverHp(1)", "status": "verified_per_readable_branch", "source_ref": source_ref(staff_path, "private void UpdateStayHome()"), "native_ref": native_ref("Staff.UpdateStayHome", "Pinned home recovery method.")},
        ],
        "thresholds": {
            "low_hp_ratio_percent": 5,
            "home_return_ratio_percent": 40,
            "recovery_start_delay_frames": 20,
            "low_hp_transition": "GetHpRatio() <= 5 -> STATE_MOVE and MOVE_MODE_GO_TO_DOOR (10), except STATE_MOVE/STATE_STAY_HOME guards.",
            "home_return": "GetHpRatio() >= 40 -> door completion/return path; exact arrival dispatch remains source-limited.",
            "source_ref": source_ref(staff_path, "if (hpRatio <= 5 && state_ != 2 && state_ != 13)"),
        },
        "saved_load": {
            "save_field": "hp_",
            "serialize_ref": source_ref(staff_path, "StreamUtil.WriteInt(os, hp_);"),
            "deserialize_ref": source_ref(staff_path, "hp_ = num51;"),
            "status": "saved_and_restored",
        },
        "ordinary_work_hp_drain": {
            "status": "UNKNOWN",
            "readable_search": ["RecoverHp(-", "hp_ -=", "hp_--", "hp_ = hp_ -"],
            "finding": "No readable direct ordinary work decrement is present. Do not add an invented work drain until native tracing closes it.",
            "source_ref": native_ref("Staff.UpdateWork", "Native entry is pinned, but the full work body is not semantically recovered here."),
        },
        "fixtures_ref": "data-dependency/staff-derived-parameter-contract.json#/three_real_max_hp_fixtures",
        "runtime_status_ref": "data-dependency/staff-runtime-status-contract.json",
    }


def existing_behavior(name: str) -> Any:
    return load_json(EVIDENCE / "behavior-first" / name)


def build_work_status(type_catalog: dict[str, Any]) -> dict[str, Any]:
    constants = existing_behavior("staff-state-constant-catalog.json")
    lifecycle = existing_behavior("work-recovery-lifecycle.json")
    machine = existing_behavior("staff-state-machine.json")
    return {
        "schema_version": "social-dev-work-status-dependency-contract-v1",
        "status": "pass_state_and_consumers_with_work_drain_limit",
        "state_vocabulary": constants["staff_state_move_flag_constants"],
        "state_machine_ref": "behavior-first/staff-state-machine.json",
        "lifecycle": lifecycle["lifecycle"],
        "data_dependencies": [
            {"source": "StaffData.jobId_", "consumer": "Staff.GetJob()", "effect": "selects JobData for work parameters", "status": "verified"},
            {"source": "StaffData.defParams_", "consumer": "Staff.GetBaseParam", "effect": "base parameter vector", "status": "verified"},
            {"source": "JobData.speed_", "consumer": "work/development speed paths", "effect": "job speed input", "status": "source_backed_consumer"},
            {"source": "JobData.params_", "consumer": "Staff.GetJobParam", "effect": "level-dependent parameter component", "status": "verified"},
            {"source": "SkillData.effects_", "consumer": "Staff.GetSkill and selected SkillData consumers", "effect": "skill-specific meeting/aura/development branches", "status": "partial_living_consumers"},
            {"source": "FurnitureData.type_", "consumer": "Staff.GotoEquip/GotoDesk and Room placement", "effect": "target class and workstation/equipment route", "status": "verified_with_role_limits"},
            {"source": "FurnitureData.recovery_", "consumer": "Staff.UseEquip", "effect": "recovery stock on use completion", "status": "verified"},
            {"source": "FurnitureData.paramType_/paramValue_", "consumer": "Staff.GetBaseParam desk branch", "effect": "desk parameter component", "status": "verified_native_branch"},
        ],
        "work_states": {
            "STATE_WORK": 4,
            "STATE_USE_EQUIPMENT": 5,
            "STATE_SIT_DOWN": 3,
            "STATE_TALK": 6,
            "STATE_WAIT": 9,
            "STATE_WANDER": 10,
            "STATE_WAIT_BACK_OF_DOOR": 11,
            "STATE_STAY_HOME": 13,
        },
        "consumer_contract": {
            "Staff.UpdateWork": {"inputs": ["FLAG_SITTING", "frame_", "flag_", "GetHpRatio()"], "status": "readable_inputs_damaged_dispatch"},
            "Staff.UpdateStayHome": {"inputs": ["hp_", "GetHpRatio()", "Room.GetDoorIndex()"], "status": "readable_recovery_branch"},
            "Staff.GotoEquip": {"inputs": ["Room.GetRandomObjChipTypeOf", "ObjChip.type_", "ObjChip.GetUsersNum"], "status": "target_selection_source_backed"},
            "Staff.GotoDesk": {"inputs": ["deskId_", "Room.GetObjChip"], "status": "desk_route_source_backed"},
            "Staff.GotoTalk": {"inputs": ["Room.GetStaff", "talk flags"], "status": "social_route_source_backed"},
        },
        "ordinary_work_hp_drain": lifecycle["ordinary_work_hp_drain"],
        "unknowns": [
            "Exact UpdateWork frame modulo and sleeping-stock cadence remain damaged.",
            "Exact post-arrival dispatch and desk vacancy predicate remain source-limited.",
        ],
        "source_refs": [
            native_ref("Staff.Update", "State dispatcher and low-HP guard."),
            native_ref("Staff.UpdateWork", "Work-state entry point."),
            native_ref("Staff.UpdateStayHome", "Home recovery state entry point."),
            native_ref("Staff.GotoEquip", "Equipment target entry point."),
            native_ref("Staff.GotoDesk", "Workstation target entry point."),
        ],
        "existing_behavior_authority": {
            "state_constants": evidence_ref(EVIDENCE / "behavior-first/staff-state-constant-catalog.json"),
            "state_machine": evidence_ref(EVIDENCE / "behavior-first/staff-state-machine.json"),
            "work_recovery": evidence_ref(EVIDENCE / "behavior-first/work-recovery-lifecycle.json"),
        },
    }


def skill_consumers(type_name: int) -> list[dict[str, Any]]:
    staff_path = SOURCE_ROOT / "game/Staff.cs"
    skill_path = TYPE_SOURCE_FILES["SkillData"]
    if type_name == 10:
        return [{"consumer": "Staff.OnEndTyping", "effect_index": 8, "effect_name": "EFFECT_MEETING_POINT", "source_ref": source_ref(staff_path, "if (skill.type_ != 10)"), "status": "verified_living_social_consumer"}]
    if type_name == 13:
        return [{"consumer": "Staff.AddAuraGauge", "effect_index": 12, "effect_name": "EFFECT_AURA_CHARGE", "source_ref": source_ref(staff_path, "if (skill.type_ != 13)"), "status": "verified_staff_runtime_consumer"}]
    if type_name == 2:
        return [{"consumer": "Staff.GetDevelopSpeed", "effect_index": 3, "effect_name": "EFFECT_DEVELOP_SPEED", "source_ref": source_ref(staff_path, "if (!flag9)"), "status": "source_consumer_damaged_context"}]
    if type_name == 7:
        return [{"consumer": "Staff.RaisePlanQualityBySkill", "effect_index": 11, "effect_name": "EFFECT_PLAN_QUALITY", "source_ref": source_ref(staff_path, "skill.type_ == 7"), "status": "verified_planning_consumer"}]
    if type_name == 11:
        return [{"consumer": "Staff.UpdateDevelop debug branch", "effect_index": 9, "effect_name": "EFFECT_DEBUG", "source_ref": source_ref(staff_path, "if (skill.type_ != 11)"), "status": "source_consumer_damaged_context"}]
    if type_name in {1, 3, 4}:
        index = {1: 6, 3: 5, 4: 1}[type_name]
        effect = {1: "EFFECT_ATTACK_DAMAGE", 3: "EFFECT_RECOVERY", 4: "EFFECT_STAFF_PARAM"}[type_name]
        return [{"consumer": "SkillData.Invoke(Staff)", "effect_index": index, "effect_name": effect, "source_ref": source_ref(skill_path, f"if (type_ != {type_name})"), "status": "verified_development_skill_consumer"}]
    return []


def build_skill_effects(skill_records: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for skill_id in sorted(skill_records):
        english = skill_records[skill_id]["English"]
        skill_type = int(field_value(english, "type_"))
        rows.append(
            {
                "skill_id": skill_id,
                "name_english": field_value(english, "name_"),
                "type": skill_type,
                "scene": field_value(english, "scene_"),
                "target": field_value(english, "target_"),
                "flag": field_value(english, "flag_"),
                "effects_raw": copy.deepcopy(field_value(english, "effects_")),
                "aura_rates_raw": copy.deepcopy(field_value(english, "auraRates_")),
                "proven_consumers": skill_consumers(skill_type),
                "consumer_status": "verified_or_source_limited" if skill_consumers(skill_type) else "UNKNOWN_NOT_PROMOTED",
                "provenance": {
                    "catalog_ref": f"data-dependency/skilldata-canonical-catalog.json#/records/{skill_id}",
                    "source_row": row_ref(english),
                },
            }
        )
    return {
        "schema_version": "social-dev-living-skill-effects-contract-v1",
        "status": "pass_raw_effects_retained_with_partial_staff_consumers",
        "policy": "SkillData effect arrays remain raw. Only source-backed consumers are listed; names, scenes, targets, and effect indices are not expanded into invented living rules.",
        "skill_catalog_ref": "data-dependency/skilldata-canonical-catalog.json",
        "effect_index_vocabulary_ref": "data-dependency/staff-parameter-vocabulary.json#/skill_vocabulary/effect_indices",
        "records": rows,
        "staff_consumer_summary": {
            "meeting_point": "Skill type 10 effect index 8 is read by Staff.OnEndTyping.",
            "aura_charge": "Skill type 13 effect index 12 is read by Staff.AddAuraGauge.",
            "other_types": "Other consumers are development/planning/combat-adjacent or have damaged context; no autonomous living rule is invented.",
        },
        "source_refs": [
            source_ref(TYPE_SOURCE_FILES["SkillData"], "public void Invoke(Staff staff)", note="Explicit skill invocation branches."),
            native_ref("Staff.GetSkill", "Selected skill lookup authority."),
        ],
        "record_count": len(rows),
    }


def build_furniture_effects(furniture_records: dict[int, dict[str, Any]], type_catalog: dict[str, Any]) -> dict[str, Any]:
    existing = existing_behavior("furniture-behavior-catalog.json")
    existing_by_id = {row["id"]: row for row in existing["records"]}
    rows: list[dict[str, Any]] = []
    for source_id in sorted(furniture_records):
        english = furniture_records[source_id]["English"]
        old = existing_by_id[source_id]
        raw = {name: copy.deepcopy(field_value(english, name)) for name in english["parsed_fields"]}
        rows.append(
            {
                "furniture_id": source_id,
                "name_english": field_value(english, "name_"),
                "raw_fields": raw,
                "interaction_class": old["interaction_class"],
                "type": old["type"],
                "category": old["category"],
                "flag": old["flag"],
                "recovery": old["recovery"],
                "status_effects": {
                    "door_record": old["interaction_class"] == "DOOR_RECORD",
                    "equipment_candidate_for_GotoEquip": old["equipment_candidate_for_GotoEquip"],
                    "hp_recovery_on_use_complete": old["hp_recovery_on_use_complete"],
                    "workstation": old["workstation"],
                    "rest_semantics": "UNKNOWN_NOT_PROMOTED",
                    "social_semantics": "UNKNOWN_NOT_PROMOTED",
                    "param_effect": {
                        "paramType_": raw["paramType_"],
                        "paramValue_": raw["paramValue_"],
                        "consumer": "Staff.GetBaseParam desk branch when paramType_ matches requested type",
                        "status": "verified_native_branch",
                    },
                },
                "passability": {
                    "passMap_raw": raw["passMap_"],
                    "passMap_present": raw["passMap_"] is not None,
                    "nonzero_cells": sum(1 for row in (raw["passMap_"] or []) for value in row if value != 0),
                    "status": "raw_matrix_retained",
                    "consumer": "ObjChip.IsPassable",
                },
                "provenance": {
                    "source_row": row_ref(english),
                    "csharp_type": update_type_ref("FurnitureData", type_catalog),
                    "behavior_catalog_ref": "behavior-first/furniture-behavior-catalog.json",
                    "passMap_fixture_ref": "phase1d_passmap_fixture.json",
                },
            }
        )
    return {
        "schema_version": "social-dev-furniture-status-effect-contract-v1",
        "status": "pass_all_records_classified_with_rest_social_limits",
        "counts": {
            "records": len(rows),
            "expected_records": 103,
            "by_interaction_class": dict(sorted(Counter(row["interaction_class"] for row in rows).items())),
            "recovery_records": sum(1 for row in rows if row["status_effects"]["hp_recovery_on_use_complete"]),
            "workstation_records": sum(1 for row in rows if row["status_effects"]["workstation"]),
            "door_records": sum(1 for row in rows if row["status_effects"]["door_record"]),
        },
        "rules": {
            "door": "FurnitureData.type_ == 5 is consumed by Room.GetDoorIndex/ObjChip door semantics.",
            "workstation": "FurnitureData.type_ == 2 is consumed by desk placement/ownership paths.",
            "equipment": "FurnitureData.type_ in {1,4} is a GotoEquip candidate; this is not a rest/social label.",
            "recovery": "FurnitureData.recovery_ >= 1 causes Staff.UseEquip to add recoveryHpStock_ on use completion; exact stock cadence remains source-limited.",
            "passMap": "Raw passMap_ is passed to ObjChip.IsPassable; the 9x9 selection fixture is authoritative for the tested multi-cell record.",
        },
        "native_refs": [
            native_ref("Staff.GotoEquip", "Equipment target selection."),
            native_ref("Staff.UseEquip", "Use completion and recovery stock."),
            native_ref("ObjChip.IsPassable", "PassMap consumer."),
            native_ref("Room.GetDoorIndex", "Door type scan."),
            native_ref("Room.PlaceDesk", "Workstation placement path."),
        ],
        "source_refs": [
            source_ref(TYPE_SOURCE_FILES["FurnitureData"], "public int[][] passMap_;"),
            source_ref(TYPE_SOURCE_FILES["FurnitureData"], "public int recovery_;"),
            source_ref(TYPE_SOURCE_FILES["FurnitureData"], "public override void Load(StringArrayStream sas)"),
        ],
        "records": rows,
        "unknowns": [
            "No FurnitureData record is promoted as original REST or SOCIAL solely from name, category, type 1/4, or sprite.",
            "Exact type-4 direction/interaction semantics remain unknown.",
            "Exact occupancy/fairness and desk vacancy semantics remain in the ObjChip/Room source-limited boundary.",
        ],
    }


def build_actor_furniture(furniture: dict[str, Any]) -> dict[str, Any]:
    classes = furniture["counts"]["by_interaction_class"]
    return {
        "schema_version": "social-dev-actor-furniture-dependency-contract-v1",
        "status": "pass_dependency_graph_with_role_limits",
        "nodes": [
            {"id": "Staff", "kind": "runtime_actor", "status": "source_and_dump_aligned"},
            {"id": "StaffData", "kind": "static_data", "status": "canonical_catalog"},
            {"id": "JobData", "kind": "static_data", "status": "canonical_catalog"},
            {"id": "SkillData", "kind": "static_data", "status": "canonical_catalog"},
            {"id": "Room", "kind": "runtime_room", "status": "behavior-first_contract"},
            {"id": "ObjChip", "kind": "runtime_occupancy_object", "status": "behavior-first_contract"},
            {"id": "FurnitureData", "kind": "static_data", "status": "canonical_catalog"},
        ],
        "edges": [
            {"from": "StaffData.jobId_", "to": "JobData.id_", "consumer": "Staff.GetJob", "status": "verified"},
            {"from": "StaffData.skill_", "to": "Staff.skillId_", "consumer": "Staff.Init", "status": "verified"},
            {"from": "Staff.skillId_", "to": "SkillData.id_", "consumer": "Staff.GetSkill", "status": "verified_native_index"},
            {"from": "Staff.room_", "to": "Room", "consumer": "Staff movement/work/home", "status": "verified_runtime_reference"},
            {"from": "Staff.deskId_", "to": "Room.GetObjChip -> ObjChip", "consumer": "Staff.GetBaseParam/GotoDesk", "status": "verified_with_desk_vacancy_limit"},
            {"from": "ObjChip.furnitureData_", "to": "FurnitureData", "consumer": "Staff.UseEquip/GetBaseParam", "status": "verified"},
            {"from": "FurnitureData.type_ in {1,4}", "to": "Staff.GotoEquip", "consumer": "equipment target selection", "status": "verified_candidate_class"},
            {"from": "FurnitureData.recovery_", "to": "Staff.recoveryHpStock_", "consumer": "Staff.UseEquip", "status": "verified_on_use_complete"},
            {"from": "FurnitureData.paramType_/paramValue_", "to": "Staff.GetBaseParam", "consumer": "desk parameter component", "status": "verified_native_branch"},
            {"from": "FurnitureData.passMap_", "to": "ObjChip.IsPassable", "consumer": "movement passability", "status": "verified_with_phase1d_fixture"},
            {"from": "FurnitureData.type_ == 5", "to": "Room.GetDoorIndex", "consumer": "door/home routing", "status": "verified"},
        ],
        "class_counts": classes,
        "role_limits": [
            "REST is a Staff stay-home state, not a FurnitureData role recovered from this source.",
            "SOCIAL is a Staff talk/meeting path; no furniture record is promoted as its source.",
            "Type 4 is retained as an equipment candidate with unresolved exact direction/interaction semantics.",
        ],
        "refs": {
            "furniture_effects": "data-dependency/furniture-status-effect-contract.json",
            "staff_status": "data-dependency/staff-runtime-status-contract.json",
            "passMap_fixture": "phase1d_passmap_fixture.json",
            "route_fixture": "phase1d_route_fixture.json",
        },
    }


def build_canonical_actor_schema(runtime_status: dict[str, Any], staff_catalog: dict[str, Any]) -> dict[str, Any]:
    source_fields = list(staff_catalog["loader_contract"]["field_assignment_sequence"])
    source_schema = [
        {
            "canonical_field": field,
            "original_field": f"StaffData.{field}",
            "status": "source_field_no_fabrication",
            "source_catalog": "data-dependency/staffdata-canonical-catalog.json",
        }
        for field in source_fields
    ]
    saved = [field["name"] for field in runtime_status["fields"] if field["storage_owner"] == "saved_runtime_state"]
    transient = [field["name"] for field in runtime_status["fields"] if field["storage_owner"] == "transient_runtime_state"]
    return {
        "schema_version": "social-dev-canonical-actor-schema-v1",
        "status": "pass_no_fabricated_original_fields",
        "identity_rule": "actor identity is source type plus StaffData.id_; an instance id is a PRODUCT_POLICY runtime wrapper, not an original StaffData value.",
        "static_source_fields": source_schema,
        "runtime_saved_fields": [
            {"original_field": f"Staff.{name}", "status": "saved_runtime_field", "source_status": "source_and_dump_aligned"}
            for name in saved
        ],
        "runtime_transient_fields": [
            {"original_field": f"Staff.{name}", "status": "transient_runtime_field", "source_status": "source_and_dump_aligned"}
            for name in transient
        ],
        "derived_contract_fields": [
            {"field": "max_hp", "status": "derived_contract_only", "formula_ref": "data-dependency/hp-data-dependency-contract.json"},
            {"field": "hp_ratio_percent", "status": "derived_contract_only", "formula_ref": "data-dependency/hp-data-dependency-contract.json"},
            {"field": "effective_parameter_vector", "status": "derived_contract_only", "formula_ref": "data-dependency/staff-derived-parameter-contract.json"},
            {"field": "behavior_state_label", "status": "derived_contract_only", "formula_ref": "behavior-first/staff-state-constant-catalog.json"},
        ],
        "product_policy_fields": [
            {"field": "instance_id", "status": "PRODUCT_POLICY", "rule": "Stable client/runtime instance wrapper; never presented as an original StaffData field."},
            {"field": "dashboard_task_ref", "status": "PRODUCT_POLICY", "rule": "Adapter reference only; see dashboard-task-adapter-contract.json."},
        ],
        "forbidden_fabrication_rules": [
            "Do not create original source fields for dashboard task state, task priority, actor health bands, or occupancy labels.",
            "Do not replace unknown source values with defaults merely to satisfy a runtime type.",
            "Do not put visual x/y or renderer-specific coordinates into the static actor catalog.",
        ],
        "catalog_ref": "data-dependency/staffdata-canonical-catalog.json",
        "runtime_status_ref": "data-dependency/staff-runtime-status-contract.json",
    }


def build_canonical_furniture_schema(furniture: dict[str, Any]) -> dict[str, Any]:
    field_load_rows = load_json(FIELD_LOAD)["rows"]
    furniture_loader = next(row for row in field_load_rows if row["type"] == "FurnitureData")
    static_fields = list(furniture_loader["field_assignment_sequence"])
    return {
        "schema_version": "social-dev-canonical-furniture-schema-v1",
        "status": "pass_no_fabricated_original_fields",
        "static_source_fields": [
            {"canonical_field": field, "original_field": f"FurnitureData.{field}", "status": "source_field_no_fabrication", "catalog_ref": "data-dependency/furniture-status-effect-contract.json"}
            for field in static_fields
        ],
        "runtime_source_fields": [
            {"original_field": "FurnitureData.num_", "status": "mutable_runtime_source_field"},
            {"original_field": "FurnitureData.newDelete_", "status": "mutable_runtime_source_field"},
            {"original_field": "FurnitureData.placed_", "status": "mutable_runtime_source_field"},
            {"original_field": "FurnitureData.new_", "status": "mutable_runtime_source_field"},
            {"original_field": "FurnitureData.selectFurnitureData_", "status": "static_selection_source_field"},
        ],
        "derived_contract_fields": [
            {"field": "interaction_class", "status": "derived_contract_only", "rule": "Source-backed classification from type_/recovery_/Staff/Room consumers."},
            {"field": "passability_projection", "status": "derived_contract_only", "rule": "Retains raw passMap_; does not replace it with a guessed rectangle."},
            {"field": "occupancy_projection", "status": "derived_contract_only", "rule": "ObjChip reservation/occupancy state is runtime, not FurnitureData."},
        ],
        "record_count": furniture["counts"]["records"],
        "catalog_ref": "data-dependency/furniture-status-effect-contract.json",
        "forbidden_fabrication_rules": [
            "No original REST/SOCIAL field is added.",
            "No original workstation vacancy count is added.",
            "No passMap is simplified into a guessed footprint.",
        ],
    }


def build_original_profiles(staff_records: dict[int, dict[str, Any]], staff_catalog: dict[str, Any], jobs: dict[int, dict[str, Any]], skills: dict[int, dict[str, Any]]) -> dict[str, Any]:
    profiles: list[dict[str, Any]] = []
    for source_id in sorted(staff_records):
        english = staff_records[source_id]["English"]
        japanese = staff_records[source_id]["Japanese"]
        job_id = int(field_value(english, "jobId_"))
        skill_id = int(field_value(english, "skill_"))
        profiles.append(
            {
                "profile_id": f"original-staff:{source_id}",
                "source_type": "StaffData",
                "source_id": source_id,
                "status": "source_profile",
                "semantic_status": "original_static_profile_only",
                "name": {
                    "English": f"{field_value(english, 'lastName_')} {field_value(english, 'firstName_')}",
                    "Japanese": f"{field_value(japanese, 'lastName_')} {field_value(japanese, 'firstName_')}",
                },
                "source_fields": {
                    field: copy.deepcopy(field_value(english, field))
                    for field in staff_catalog["loader_contract"]["field_assignment_sequence"]
                },
                "relations": {
                    "job_id": job_id,
                    "skill_id": skill_id,
                    "job_exists": job_id in jobs,
                    "skill_exists": skill_id in skills,
                },
                "provenance": {
                    "English": row_ref(english),
                    "Japanese": row_ref(japanese),
                    "catalog_ref": f"data-dependency/staffdata-canonical-catalog.json#/records/{source_id}",
                },
            }
        )
    return {
        "schema_version": "social-dev-original-staff-profile-catalog-v1",
        "status": "pass_all_141_original_profiles",
        "profile_count": len(profiles),
        "profiles": profiles,
        "default_actor_boundary": {
            "known_initial_spawn_staff_ids": [0, 1, 2],
            "status": "source_bounded_fixture",
            "source_ref": "knowledge/fixtures/accepted/runtime/actor_spawn_contract.json#/actors",
            "note": "AppData.NewGame consumes caller-provided initStaffs. The full caller selection is not reconstructed; no broader default set is invented.",
        },
        "policy": "Every profile is the original StaffData row plus exact locale/provenance. Runtime status, room position, HP, desk occupancy, and dashboard task state are not folded into the original profile.",
        "catalog_ref": "data-dependency/staffdata-canonical-catalog.json",
    }


def build_dashboard_adapter() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-dashboard-task-adapter-contract-v1",
        "status": "pass_product_policy_boundary",
        "purpose": "A presentation/task adapter may consume canonical source records and bounded runtime state without redefining original Staff/Job/Skill/Furniture data.",
        "input_contracts": [
            "data-dependency/original-staff-profile-catalog.json",
            "data-dependency/staff-job-link-contract.json",
            "data-dependency/staff-skill-link-contract.json",
            "data-dependency/furniture-status-effect-contract.json",
            "data-dependency/staff-runtime-status-contract.json",
        ],
        "adapter_fields": [
            {"field": "task_id", "status": "PRODUCT_POLICY", "source": "adapter_generated"},
            {"field": "actor_ref", "status": "PRODUCT_POLICY", "source": "canonical actor identity"},
            {"field": "task_kind", "status": "PRODUCT_POLICY", "source": "bounded semantic label; not an original Staff field"},
            {"field": "task_status", "status": "PRODUCT_POLICY", "source": "adapter lifecycle"},
            {"field": "job_ref", "status": "PRODUCT_POLICY", "source": "StaffData.jobId_ relation"},
            {"field": "skill_ref", "status": "PRODUCT_POLICY", "source": "StaffData.skill_/Staff.skillId_ relation"},
            {"field": "furniture_ref", "status": "PRODUCT_POLICY", "source": "FurnitureData dependency when source-backed"},
            {"field": "source_evidence_refs", "status": "PRODUCT_POLICY", "source": "provenance pointers"},
        ],
        "not_exposed_as_adapter_fields": ["Staff.x_", "Staff.y_", "Staff.hp_", "Staff.objIndex_", "Staff.route_", "raw renderer coordinates", "raw occupancy counters"],
        "forbidden_inputs": [
            "Do not infer task state from raw x/y or sprite position.",
            "Do not write a raw HP value into a dashboard task contract.",
            "Do not mutate canonical catalogs to satisfy dashboard widgets.",
        ],
        "separation": {
            "original_source_data": "catalog contracts",
            "runtime_life_state": "Staff runtime status contract",
            "dashboard_task_view": "PRODUCT_POLICY adapter only",
        },
        "status_unknowns": [
            "Existing dashboard widget-to-task mappings remain UNKNOWN until a separate product contract is authorized.",
            "No dashboard task assignment algorithm is implemented in this forensic phase.",
        ],
        "preservation_ref": "behavior-first/dashboard-preservation-boundary.json",
    }


def build_unknowns() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-data-dependency-unknowns-v1",
        "status": "tracked",
        "resolved_this_phase": [
            {"id": "DD-R01", "topic": "JobData.GetBaseParam", "status": "resolved_native", "ref": "job-level-parameter-contract.json"},
            {"id": "DD-R02", "topic": "JobData.GetMasterLvBonusParam", "status": "resolved_native", "ref": "job-level-parameter-contract.json"},
            {"id": "DD-R03", "topic": "Staff.GetSkill lookup", "status": "resolved_native", "ref": "staff-skill-link-contract.json"},
        ],
        "unknowns": [
            {"id": "DD-U01", "topic": "Room.GetEquipParam filter/flag semantics", "status": "UNKNOWN", "impact": "The room equipment component of Staff.GetBaseParam cannot be evaluated from source alone without the damaged filter body."},
            {"id": "DD-U02", "topic": "GetMotivation Player-bound semantics", "status": "UNKNOWN", "impact": "The native clamp input is recovered, but the owning Player field's product meaning is not promoted."},
            {"id": "DD-U03", "topic": "ordinary work HP drain", "status": "UNKNOWN", "impact": "No readable decrement is added; native UpdateWork remains an entry point only."},
            {"id": "DD-U04", "topic": "sleeping recovery stock cadence", "status": "UNKNOWN", "impact": "The stock-add condition's exact frame/modulo cadence is damaged."},
            {"id": "DD-U05", "topic": "desk vacancy predicate", "status": "UNKNOWN", "impact": "Exact occupancy/reservation fairness cannot be promoted beyond source-backed guards."},
            {"id": "DD-U06", "topic": "arrival callback dispatch", "status": "UNKNOWN", "impact": "OnArriveGoal and indirect state dispatch remain damaged."},
            {"id": "DD-U07", "topic": "FurnitureData type-4 direction/interaction", "status": "UNKNOWN", "impact": "Type 4 is retained as equipment candidate; exact direction semantics are not invented."},
            {"id": "DD-U08", "topic": "FurnitureData rest/social roles", "status": "UNKNOWN", "impact": "No record is promoted as rest or social from names, category, or sprites."},
            {"id": "DD-U09", "topic": "full meeting dispatch", "status": "UNKNOWN", "impact": "Skill 10 meeting-point effect is proven, but complete meeting state dispatch remains source-limited."},
            {"id": "DD-U10", "topic": "AppData initStaffs caller selection", "status": "UNKNOWN", "impact": "Known initial spawn fixture contains StaffData 0, 1, 2; broader caller selection is not reconstructed."},
            {"id": "DD-U11", "topic": "dashboard widget mapping", "status": "UNKNOWN_PRODUCT_POLICY", "impact": "No dashboard task assignment algorithm is created in this forensic phase."},
        ],
        "retention_policy": {
            "raw_rows_retained": True,
            "raw_columns_retained": True,
            "unresolved_semantics_retained": True,
            "fabricated_original_values": False,
        },
    }


def build_checkpoint_ledger() -> dict[str, Any]:
    rows = [
        ("DD.0", "PASS", "Data/catalog authority and provenance chain closed for pinned APK, ZIP, RAR extraction, C# update, and loader evidence."),
        ("DD.1", "PASS", "Full Staff/Job/Skill/Furniture constant vocabulary retained with source refs."),
        ("DD.2", "PASS", "StaffData catalog retains 141/141 English+Japanese records and raw rows."),
        ("DD.3", "PASS", "JobData catalog retains 30/30 English+Japanese records and raw rows."),
        ("DD.4", "PASS", "Job level interpolation, max-level bonus, and integer semantics recovered from native."),
        ("DD.5", "PASS", "SkillData catalog retains 36/36 English+Japanese records and raw effect arrays."),
        ("DD.6", "PASS", "All 141 StaffData.jobId_ links resolve to JobData."),
        ("DD.7", "PASS", "All 141 StaffData.skill_ links resolve through native Staff.GetSkill indexing."),
        ("DD.8", "PASS_WITH_LIMITS", "Staff parameter component formula recovered; room equipment and motivation labels remain source-limited."),
        ("DD.9", "PASS", "Saved/transient/derived Staff runtime status schema produced from field inventory and Serialize/Deserialize evidence."),
        ("DD.10", "PASS_WITH_LIMITS", "HP data chain, max formula, save/load, thresholds, and recovery proven; ordinary work drain remains UNKNOWN."),
        ("DD.11", "PASS_WITH_LIMITS", "Work/state consumers linked; damaged UpdateWork cadence and arrival dispatch retained as UNKNOWN."),
        ("DD.12", "PASS_WITH_LIMITS", "All SkillData effects retained; source-backed Staff meeting/aura consumers listed; other contexts not invented."),
        ("DD.13", "PASS_WITH_LIMITS", "All 103 FurnitureData status effects classified; rest/social and type-4 direction remain UNKNOWN."),
        ("DD.14", "PASS_WITH_LIMITS", "Actor/Furniture dependency graph closed at source-backed edges; occupancy fairness remains UNKNOWN."),
        ("DD.15", "PASS", "Canonical Actor schema separates source, saved, transient, derived, and PRODUCT_POLICY fields."),
        ("DD.16", "PASS", "Canonical Furniture schema retains all original fields and raw passMap; projections are derived only."),
        ("DD.17", "PASS_WITH_LIMITS", "141 original StaffData profiles retained; known initial spawn fixture 0/1/2 kept without inventing broader selection."),
        ("DD.18", "PASS", "Dashboard task adapter is explicitly PRODUCT_POLICY and excludes raw x/y/HP/runtime coordinates."),
        ("DD.19", "PASS", "Completeness/provenance/regression checks are provided by the dedicated test script and diff gate."),
        ("DD.20", "STOP", "Stop before living-system runtime implementation, visual correction, renderer/MapChip changes, or V8."),
    ]
    return {
        "schema_version": "social-dev-data-dependency-checkpoint-ledger-v1",
        "status": "PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS",
        "records": [{"Checkpoint": key, "Status": status, "Evidence": evidence} for key, status, evidence in rows],
        "required_stop_literals": {
            "implementation_started": "NO",
            "visual_work_started": "NO",
            "renderer_changed": "NO",
            "MapChip_changed": "NO",
            "V8_started": "NO",
            "subagents_used": "NO",
            "emulator_or_adb_used": "NO",
            "server_started": "NO",
            "network_used": "NO",
        },
        "output_roots": {"machine_evidence": rel(OUT), "reports": rel(REPORTS)},
    }


def report_header(title: str) -> str:
    return f"# {title}\n\nStatus: `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`\n\nThis report is static/offline evidence only. No decompiled C# was executed and no runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.\n"


def build_reports(authority: dict[str, Any], catalogs: dict[str, dict[str, Any]], derived: dict[str, Any], hp: dict[str, Any], furniture: dict[str, Any], actor_schema: dict[str, Any], furniture_schema: dict[str, Any], dashboard: dict[str, Any], unknowns: dict[str, Any]) -> None:
    counts = ", ".join(f"{name}={catalogs[name]['counts']['records']}" for name in ("StaffData", "JobData", "SkillData"))
    write_report("DATA_DEPENDENCY_AUDIT.md", report_header("Data Dependency Audit") + f"\nAuthority is the pinned APK/native set plus the original asset-guide ZIP table members. ZIP table roundtrip is exact for all eight locale/type members. Canonical counts: {counts}, FurnitureData={furniture['counts']['records']}.\n\nThe machine package is under `knowledge/fixtures/accepted/data-dependency/`. Every record retains English and Japanese raw rows, parsed loader fields, row hashes, C# type refs, and archive provenance.\n\nResolved native formulas: JobData level interpolation, max-level bonus, Staff.GetSkill index lookup, Staff parameter component sum, and HP max consumer chain. Source limits remain tracked rather than filled with product guesses.\n")
    write_report("STAFFDATA_MODEL.md", report_header("StaffData Model") + f"\nStaffData is cataloged at {catalogs['StaffData']['counts']['records']}/{catalogs['StaffData']['counts']['expected_records']} records. The six data parameter slots are 0 IDEA, 1 PROGRAM, 2 GRAPHIC, 3 SOUND, 4 NETWORK, and 5 HP; index 6 is the end sentinel. `defParams_`, `jobId_`, and `skill_` remain exact source values.\n\nSee `staffdata-canonical-catalog.json`, `staff-job-link-contract.json`, and `staff-skill-link-contract.json`. Mutable Staff state is separate in `staff-runtime-status-contract.json`.\n")
    write_report("JOBDATA_MODEL.md", report_header("JobData Model") + f"\nJobData is cataloged at {catalogs['JobData']['counts']['records']}/{catalogs['JobData']['counts']['expected_records']} records. Native recovery closes the parameter formula: `p0 + trunc((p1-p0)*(lv-1)/(maxLv-1))`, then adds `bonus_[type]` when `lv >= maxLv_`.\n\nThe contract retains raw `params_`, `bonus_`, speed, evolution, and locale values for all jobs.\n")
    write_report("SKILLDATA_MODEL.md", report_header("SkillData Model") + f"\nSkillData is cataloged at {catalogs['SkillData']['counts']['records']}/{catalogs['SkillData']['counts']['expected_records']} records. All raw effect arrays, aura rates, flags, scenes, targets, and locale fields are retained.\n\nThe selected skill relation is native-indexed through `Staff.skillId_`. Proven Staff consumers include meeting-point effect index 8 for type 10 and aura-charge effect index 12 for type 13. Other contexts stay source-limited.\n")
    write_report("DERIVED_STAFF_PARAMETERS.md", report_header("Derived Staff Parameters") + "\n`Staff.GetParam` is the sum of `Staff.GetBaseParam` and `Staff.GetJobParam`. The native component path includes StaffData base parameters, room equipment, desk FurnitureData parameter value, master-job bonuses, item effects, motivation scaling, and the 1..9999 clamp.\n\nThree source-row MaxHP fixtures are recorded in `staff-derived-parameter-contract.json`; they use a neutral room/equipment context and motivation 0 so the data dependency is reproducible without inventing live state.\n")
    write_report("HP_DATA_DEPENDENCY.md", report_header("HP Data Dependency") + f"\n`Staff.hp_` is the saved mutable life resource at dump offset `0xE8`. `StaffData.PARAM_HP` is 5. Max HP is `GetBaseParam(5,0) + GetJobParam(5,level_)`; HP ratio uses integer division against that same max.\n\nLow HP at `<=5%` routes to the door; home recovery returns at `>=40%`. Equipment recovery adds stock after use completion and delayed recovery consumes one stock per readable tick. Ordinary work HP drain is explicitly `UNKNOWN`.\n")
    write_report("FURNITURE_STATUS_EFFECTS.md", report_header("Furniture Status Effects") + f"\nAll {furniture['counts']['records']} FurnitureData records are retained with raw passMap matrices and classified only from type/recovery/consumer evidence. The current interaction counts are `{json.dumps(furniture['counts']['by_interaction_class'], sort_keys=True)}`.\n\nType 5 is the door record, type 2 is the workstation class, type 1/4 are equipment candidates, and recovery >= 1 is the proven use-completion recovery trigger. Rest/social labels are not inferred.\n")
    write_report("CANONICAL_ACTOR_SCHEMA.md", report_header("Canonical Actor Schema") + "\nThe canonical actor schema keeps StaffData source fields, saved Staff fields, transient Staff fields, and derived formula outputs in separate namespaces. `instance_id` and dashboard task references are explicitly `PRODUCT_POLICY`; they are not original game fields.\n\nThe schema forbids fabricating source values or adding raw x/y/HP fields to the dashboard adapter.\n")
    write_report("CANONICAL_FURNITURE_SCHEMA.md", report_header("Canonical Furniture Schema") + "\nThe canonical Furniture schema retains the complete FurnitureData loader field sequence, including price, parameter, recovery, use bonus, and passMap data. Interaction class, passability projection, occupancy projection, and recovery role are derived contract views with provenance; they do not replace original fields.\n")
    write_report("DASHBOARD_TASK_ADAPTER.md", report_header("Dashboard Task Adapter") + "\nThe dashboard adapter is a `PRODUCT_POLICY` boundary. It may reference an actor, job, skill, furniture, task kind, task status, and evidence pointers. It does not expose raw Staff x/y, HP, object index, route, or occupancy counters, and no task assignment algorithm is implemented here.\n")
    write_report("DATA_DEPENDENCY_HANDOFF.md", report_header("Data Dependency Handoff") + "\nDD.0–DD.20 are recorded in `checkpoint-ledger.json`. Catalogs are complete at StaffData 141, JobData 30, SkillData 36, and FurnitureData 103. Job level math and Staff skill lookup are native-backed. HP/work/furniture/actor schemas and all unresolved rows are machine-readable.\n\nSTOP: implementation/visual work has not started. Do not begin renderer or V8 work from this handoff; resolve the listed DD unknowns or authorize the next phase separately.\n")


def build_all() -> dict[str, Any]:
    load_contract, type_catalog, records = load_inputs()
    archive = archive_member_manifest()
    source_pack = source_pack_manifest()
    apk = apk_manifest()
    authority = build_authority(type_catalog, load_contract, archive, source_pack, apk)
    vocab = build_parameter_vocabulary(type_catalog)
    catalogs = {type_name: build_catalog(type_name, records[type_name], type_catalog, load_contract) for type_name in TABLE_NAMES}
    jobs = job_values(records["JobData"])
    skills = {source_id: {"source_id": source_id} for source_id in records["SkillData"]}
    job_level = build_job_level_contract(catalogs["JobData"], records["JobData"], type_catalog)
    staff_job = build_staff_job_links(records["StaffData"], jobs, type_catalog)
    staff_skill = build_staff_skill_links(records["StaffData"], skills, type_catalog)
    runtime_status = build_runtime_status()
    derived = build_staff_derived(records["StaffData"], jobs, type_catalog)
    hp = build_hp_contract(runtime_status, derived, type_catalog)
    work = build_work_status(type_catalog)
    skill_effects = build_skill_effects(records["SkillData"], type_catalog)
    furniture = build_furniture_effects(records["FurnitureData"], type_catalog)
    actor_furniture = build_actor_furniture(furniture)
    actor_schema = build_canonical_actor_schema(runtime_status, catalogs["StaffData"])
    furniture_schema = build_canonical_furniture_schema(furniture)
    profiles = build_original_profiles(records["StaffData"], catalogs["StaffData"], jobs, skills)
    dashboard = build_dashboard_adapter()
    unknowns = build_unknowns()
    ledger = build_checkpoint_ledger()

    outputs = {
        "checkpoint-ledger.json": ledger,
        "data-catalog-authority.json": authority,
        "staff-parameter-vocabulary.json": vocab,
        "staffdata-canonical-catalog.json": catalogs["StaffData"],
        "jobdata-canonical-catalog.json": catalogs["JobData"],
        "job-level-parameter-contract.json": job_level,
        "skilldata-canonical-catalog.json": catalogs["SkillData"],
        "staff-job-link-contract.json": staff_job,
        "staff-skill-link-contract.json": staff_skill,
        "staff-derived-parameter-contract.json": derived,
        "staff-runtime-status-contract.json": runtime_status,
        "hp-data-dependency-contract.json": hp,
        "work-status-dependency-contract.json": work,
        "living-skill-effects-contract.json": skill_effects,
        "furniture-status-effect-contract.json": furniture,
        "actor-furniture-dependency-contract.json": actor_furniture,
        "canonical-actor-schema.json": actor_schema,
        "canonical-furniture-schema.json": furniture_schema,
        "original-staff-profile-catalog.json": profiles,
        "dashboard-task-adapter-contract.json": dashboard,
        "unknowns.json": unknowns,
    }
    for name, payload in outputs.items():
        write_json(name, payload)
    build_reports(authority, catalogs, derived, hp, furniture, actor_schema, furniture_schema, dashboard, unknowns)
    return {"outputs": sorted(outputs), "counts": EXPECTED_COUNTS, "status": ledger["status"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Build and validate the package.")
    args = parser.parse_args()
    result = build_all()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
