"""Build a provenance-preserving first-slice data candidate.

The output is evidence only. It keeps raw table rows and loader candidates
without promoting array columns to semantic runtime fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
CATALOG = EVIDENCE / "csharp_update_inventory"
ASSET_XLS = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
DEFAULT_OUTPUT = EVIDENCE

TABLE_NAMES = {
    "RoomData": "room.txt",
    "FurnitureData": "furniture.txt",
    "StaffData": "staff.txt",
    "JobData": "job.txt",
    "SkillData": "skill.txt",
}
SELECTED_IDS = {
    "RoomData": [0],
    "FurnitureData": [1, 2, 5],
    "StaffData": [0, 1, 2, 3, 4],
    "JobData": [4],
    # Phase 1B loader-aware framing derives StaffData.skill_ = 1 for the
    # selected staff rows. It remains an order candidate, not a semantic link.
    "SkillData": [1],
}
VARIABLE_READERS = {
    "GetIntArray",
    "GetIntIntArray",
    "GetTripleIntArray",
    "GetStringArray",
}
SCHEMA_VERSION = "social-dev-first-slice-data-candidate-v1"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalise_path(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def relative_path(path: Path) -> str:
    try:
        return normalise_path(path.relative_to(ROOT))
    except ValueError:
        return normalise_path(path)


def table_path(type_name: str, locale: str) -> Path:
    path = ASSET_XLS / f"{locale}.lproj" / TABLE_NAMES[type_name]
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path


def read_table(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            raw_line = raw_line.rstrip("\r\n")
            if not raw_line:
                continue
            columns = raw_line.split("\t")
            parsed_id: int | None = None
            try:
                parsed_id = int(columns[0])
            except (ValueError, IndexError):
                pass
            rows.append(
                {
                    "row_number": line_number,
                    "raw_line": raw_line,
                    "columns": columns,
                    "id": parsed_id,
                    "row_sha256": hashlib.sha256(raw_line.encode("utf-8")).hexdigest(),
                }
            )
    return rows


def scalar_value(value: str) -> int | str:
    try:
        return int(value)
    except ValueError:
        return value


def prefix_candidate(
    columns: list[str],
    fields: list[str],
    readers: list[str],
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    stopped_at: dict[str, Any] | None = None
    for index, (field, reader) in enumerate(zip(fields, readers)):
        if reader in VARIABLE_READERS:
            stopped_at = {
                "column_index": index,
                "field": field,
                "reader": reader,
                "reason": "array_reader_boundary",
            }
            break
        if index >= len(columns):
            break
        values[field] = {
            "column_index": index,
            "reader": reader,
            "raw": columns[index],
            "parsed_candidate": scalar_value(columns[index]),
            "mapping_status": "order_candidate",
            "semantic_status": "unknown",
        }
    return {
        "fields": values,
        "stopped_at": stopped_at,
        "mapping_status": "scalar_prefix_only",
        "semantic_status": "unknown",
    }


def find_loader_row(rows: list[dict[str, Any]], type_name: str) -> dict[str, Any]:
    for row in rows:
        if row.get("type") == type_name or row.get("element_type") == type_name:
            return row
    raise KeyError(f"missing load contract row: {type_name}")


def find_field_load_row(rows: list[dict[str, Any]], type_name: str) -> dict[str, Any]:
    for row in rows:
        if row.get("type") == type_name:
            return row
    raise KeyError(f"missing field-load row: {type_name}")


def find_type_source(type_rows: list[dict[str, Any]], type_name: str) -> dict[str, Any]:
    for row in type_rows:
        if row.get("name") == type_name:
            return row
    raise KeyError(f"missing type catalog row: {type_name}")


def candidate_name(records: list[dict[str, Any]], type_name: str, locale: str, selected_ids: list[int]) -> list[str]:
    values: list[str] = []
    for record in records:
        if record.get("type") != type_name or record.get("locale") != locale or record.get("id") not in selected_ids:
            continue
        name_field = record.get("scalar_prefix_candidate", {}).get("fields", {}).get("name_")
        if name_field is not None:
            values.append(str(name_field.get("raw", "")))
    return values


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = []
    for path in sorted(set(paths), key=lambda item: str(item)):
        if not path.is_file():
            raise FileNotFoundError(str(path))
        payload: dict[str, Any] = {
            "path": relative_path(path),
            "sha256": sha256_file(path),
        }
        files.append(payload)
    digest = hashlib.sha256(stable_json(files).encode("utf-8")).hexdigest()
    return {"files": files, "input_hash": digest}


def selected_record(
    type_name: str,
    locale: str,
    selected_id: int,
    rows: list[dict[str, Any]],
    load_row: dict[str, Any],
    field_load_row: dict[str, Any],
    type_source: dict[str, Any],
    table_file: Path,
) -> dict[str, Any]:
    matches = [row for row in rows if row["id"] == selected_id]
    if not matches:
        return {
            "type": type_name,
            "locale": locale,
            "id": selected_id,
            "status": "missing",
            "semantic_status": "unknown",
            "table_path": relative_path(table_file),
        }
    row = matches[0]
    fields = field_load_row.get("field_assignment_sequence") or []
    readers = field_load_row.get("reader_sequence") or []
    return {
        "type": type_name,
        "locale": locale,
        "id": selected_id,
        "status": "candidate",
        "semantic_status": "unknown",
        "mapping_status": "raw_row_with_scalar_prefix_candidate",
        "table_path": relative_path(table_file),
        "row_number": row["row_number"],
        "row_sha256": row["row_sha256"],
        "column_count": len(row["columns"]),
        "raw_columns": row["columns"],
        "loader_candidate": {
            "reader_sequence": load_row.get("reader_sequence", []),
            "reader_call_count": load_row.get("reader_call_count"),
            "field_assignment_sequence": fields,
            "field_assignment_count": field_load_row.get("field_assignment_count"),
            "load_status": load_row.get("status"),
            "field_load_status": field_load_row.get("status"),
        },
        "scalar_prefix_candidate": prefix_candidate(row["columns"], fields, readers),
        "csharp_source_ref": {
            "file": normalise_path(type_source["source"]["file"]),
            "line_start": type_source["source"].get("line_start"),
            "line_end": type_source["source"].get("line_end"),
            "source_hash": type_source.get("source_hash"),
        },
    }


def table_summary(
    type_name: str,
    english_path: Path,
    japanese_path: Path,
    english_rows: list[dict[str, Any]],
    japanese_rows: list[dict[str, Any]],
    load_row: dict[str, Any],
    field_load_row: dict[str, Any],
) -> dict[str, Any]:
    english_ids = [row["id"] for row in english_rows]
    japanese_ids = [row["id"] for row in japanese_rows]
    english_counts = Counter(str(len(row["columns"])) for row in english_rows)
    japanese_counts = Counter(str(len(row["columns"])) for row in japanese_rows)
    return {
        "type": type_name,
        "english": {
            "path": relative_path(english_path),
            "sha256": sha256_file(english_path),
            "row_count": len(english_rows),
            "column_count_distribution": dict(sorted(english_counts.items())),
            "id_sequence": english_ids,
        },
        "japanese": {
            "path": relative_path(japanese_path),
            "sha256": sha256_file(japanese_path),
            "row_count": len(japanese_rows),
            "column_count_distribution": dict(sorted(japanese_counts.items())),
            "id_sequence": japanese_ids,
        },
        "locale_alignment": {
            "row_count_equal": len(english_rows) == len(japanese_rows),
            "id_sequence_equal": english_ids == japanese_ids,
            "duplicate_english_ids": sorted({item for item, count in Counter(english_ids).items() if count > 1}),
            "duplicate_japanese_ids": sorted({item for item, count in Counter(japanese_ids).items() if count > 1}),
            "status": "candidate",
        },
        "loader_candidate": {
            "reader_sequence": load_row.get("reader_sequence", []),
            "reader_call_count": load_row.get("reader_call_count"),
            "english_row_count_reported": load_row.get("english_row_count"),
            "english_column_count_distribution_reported": load_row.get("english_column_count_distribution"),
            "field_assignment_sequence": field_load_row.get("field_assignment_sequence", []),
            "field_assignment_count": field_load_row.get("field_assignment_count"),
            "load_status": load_row.get("status"),
            "field_load_status": field_load_row.get("status"),
        },
    }


def build_candidate(output_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    type_catalog = load_json(CATALOG / "type_catalog.json")
    data_schema = load_json(EVIDENCE / "data_schema_candidate.json")
    load_contracts = load_json(EVIDENCE / "load_contract_candidates.json")
    field_load = load_json(EVIDENCE / "field_load_candidates.json")
    asset_validation = load_json(EVIDENCE / "asset_validation_gate.json")
    type_rows = type_catalog["records"]

    input_paths = [
        CATALOG / "type_catalog.json",
        EVIDENCE / "data_schema_candidate.json",
        EVIDENCE / "load_contract_candidates.json",
        EVIDENCE / "field_load_candidates.json",
        EVIDENCE / "asset_validation_gate.json",
    ]
    all_summaries: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    missing_records: list[dict[str, Any]] = []
    selected_by_type = dict(SELECTED_IDS)
    table_cache: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for type_name in SELECTED_IDS:
        english_path = table_path(type_name, "English")
        japanese_path = table_path(type_name, "Japanese")
        input_paths.extend([english_path, japanese_path])
        english_rows = read_table(english_path)
        japanese_rows = read_table(japanese_path)
        table_cache[(type_name, "English")] = english_rows
        table_cache[(type_name, "Japanese")] = japanese_rows
        load_row = find_loader_row(load_contracts["rows"], type_name)
        field_load_row = find_field_load_row(field_load["rows"], type_name)
        type_source = find_type_source(type_rows, type_name)
        all_summaries.append(
            table_summary(
                type_name,
                english_path,
                japanese_path,
                english_rows,
                japanese_rows,
                load_row,
                field_load_row,
            )
        )
        for locale, rows, path in (
            ("English", english_rows, english_path),
            ("Japanese", japanese_rows, japanese_path),
        ):
            for selected_id in selected_by_type[type_name]:
                record = selected_record(
                    type_name,
                    locale,
                    selected_id,
                    rows,
                    load_row,
                    field_load_row,
                    type_source,
                    path,
                )
                records.append(record)
                if record["status"] == "missing":
                    missing_records.append(
                        {"type": type_name, "locale": locale, "id": selected_id}
                    )

    staff_english = [
        record for record in records
        if record["type"] == "StaffData" and record["locale"] == "English" and record["status"] == "candidate"
    ]
    job_ids: list[int] = []
    for record in staff_english:
        candidate = record["scalar_prefix_candidate"]["fields"].get("jobId_")
        if candidate and isinstance(candidate.get("parsed_candidate"), int):
            job_ids.append(candidate["parsed_candidate"])
    job_ids = sorted(set(job_ids))
    selected_by_type["JobData"] = job_ids
    job_records = [
        record for record in records
        if record["type"] == "JobData" and record["locale"] == "English"
    ]
    if job_ids != SELECTED_IDS["JobData"]:
        selected_by_type["JobData"] = job_ids
        for locale in ("English", "Japanese"):
            path = table_path("JobData", locale)
            rows = table_cache[("JobData", locale)]
            load_row = find_loader_row(load_contracts["rows"], "JobData")
            field_load_row = find_field_load_row(field_load["rows"], "JobData")
            type_source = find_type_source(type_rows, "JobData")
            for selected_id in job_ids:
                records.append(
                    selected_record(
                        "JobData",
                        locale,
                        selected_id,
                        rows,
                        load_row,
                        field_load_row,
                        type_source,
                        path,
                    )
                )

    selection = {
        "status": "derived_candidate",
        "reason": "lowest/base records plus bounded scalar-prefix linkage from StaffData.jobId_",
        "room": {"type": "RoomData", "ids": SELECTED_IDS["RoomData"], "name_evidence": {locale: candidate_name(records, "RoomData", locale, SELECTED_IDS["RoomData"])[0] for locale in ("English", "Japanese")}},
        "furniture": {"type": "FurnitureData", "ids": SELECTED_IDS["FurnitureData"], "name_evidence": {locale: candidate_name(records, "FurnitureData", locale, SELECTED_IDS["FurnitureData"]) for locale in ("English", "Japanese")}},
        "staff": {"type": "StaffData", "ids": SELECTED_IDS["StaffData"]},
        "job": {"type": "JobData", "ids": job_ids, "link_status": "order_candidate"},
        "skill": {"type": "SkillData", "ids": SELECTED_IDS["SkillData"], "link_status": "loader_aware_order_candidate"},
        "room_state_status": "unverified",
    }

    links = [
        {
            "id": f"staff-{staff_id}-job",
            "from": {"type": "StaffData", "id": staff_id, "field": "jobId_"},
            "to": {"type": "JobData", "id": job_ids[0] if len(job_ids) == 1 else None},
            "relation": "job_reference",
            "status": "order_candidate",
            "confidence": "medium",
            "evidence_refs": [
                "knowledge/fixtures/accepted/field_load_candidates.json",
                "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls/English.lproj/staff.txt",
            ],
            "note": "jobId_ is in the scalar prefix before StaffData.defParams_ array reader.",
        }
        for staff_id in SELECTED_IDS["StaffData"]
    ]
    links.append(
        {
            "id": "staff-skill-supporting",
            "from": {"type": "StaffData", "ids": SELECTED_IDS["StaffData"], "field": "skill_"},
            "to": {"type": "SkillData", "ids": SELECTED_IDS["SkillData"]},
            "relation": "skill_reference",
            "status": "order_candidate",
            "confidence": "medium",
            "evidence_refs": [
                "knowledge/fixtures/accepted/field_load_candidates.json",
                "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls/English.lproj/staff.txt",
            ],
            "note": "Phase 1B loader-aware framing reads skill_ = 1 after variable arrays; this is still not a promoted product relation.",
        }
    )
    review_items = [
        {
            "id": "room-state-placement-unverified",
            "status": "unknown",
            "blocking": True,
            "action": "Find persisted/generated room placement evidence before claiming selected furniture belongs to RoomData id 0.",
        },
        {
            "id": "array-column-semantic-unverified",
            "status": "unknown",
            "blocking": True,
            "action": "Resolve variable-length array boundaries using loader/table evidence before creating typed records.",
        },
        {
            "id": "staff-skill-link-unverified",
            "status": "unknown",
            "blocking": True,
            "action": "Trace StaffData.skill_ consumer or bounded assembly evidence.",
        },
        {
            "id": "asset-selector-not-promoted",
            "status": "quarantine",
            "blocking": True,
            "action": "Resolve furniture/character selector relationships before runtime promotion.",
        },
        {
            "id": "locale-name-is-evidence-not-semantic",
            "status": "derived",
            "blocking": False,
            "action": "Use English/Japanese text for locale fixtures only; do not infer field meanings from translations.",
        },
    ]

    input_hashes = input_manifest(input_paths)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidate = {
        "schema_version": SCHEMA_VERSION,
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": generated_at,
        "input_manifest": input_hashes,
        "selection": selection,
        "table_summaries": all_summaries,
        "records": records,
        "links": links,
        "review_items": review_items,
        "asset_validation_status": asset_validation.get("status"),
        "policy": {
            "english_primary_japanese_crosscheck": True,
            "raw_columns_retained": True,
            "array_fields_not_positionally_promoted": True,
            "runtime_promotion": "blocked_until_phase1_contract_gate",
        },
    }
    validation_checks = []
    def check(check_id: str, passed: bool, observed: Any, expected: Any, note: str) -> None:
        validation_checks.append(
            {
                "id": check_id,
                "status": "pass" if passed else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    selected_types = set(SELECTED_IDS)
    check("selected-types", selected_types == set(TABLE_NAMES), sorted(selected_types), sorted(TABLE_NAMES), "All first-slice data types are included.")
    check("selected-records-present", not missing_records, missing_records, "empty", "Every selected id exists in English and Japanese.")
    alignments = {summary["type"]: summary["locale_alignment"] for summary in all_summaries}
    check("locale-row-alignment", all(item["row_count_equal"] and item["id_sequence_equal"] for item in alignments.values()), alignments, "all equal", "English/Japanese IDs and row counts align.")
    check("no-duplicate-ids", all(not item["duplicate_english_ids"] and not item["duplicate_japanese_ids"] for item in alignments.values()), alignments, "no duplicates", "Selected tables have unique IDs.")
    check("raw-columns-retained", all(record.get("raw_columns") for record in records if record["status"] == "candidate"), len(records), "all candidate rows", "No raw row is discarded.")
    check("semantic-not-promoted", candidate["semantic_status"] == "pending_review", candidate["semantic_status"], "pending_review", "Candidate package must not become runtime contract.")
    validation = {
        "schema_version": "social-dev-first-slice-data-validation-v1",
        "status": "pass" if all(item["status"] == "pass" for item in validation_checks) else "fail",
        "semantic_status": "pending_review",
        "generated_at_utc": generated_at,
        "input_hash": input_hashes["input_hash"],
        "failed_checks": [item["id"] for item in validation_checks if item["status"] == "fail"],
        "checks": validation_checks,
        "counts": {
            "types": len(selected_types),
            "selected_records": len([record for record in records if record["status"] == "candidate"]),
            "missing_records": len(missing_records),
            "links": len(links),
            "review_items": len(review_items),
        },
        "blocking_review_items": [item["id"] for item in review_items if item["blocking"]],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in (
        ("first_slice_data_candidate.json", candidate),
        ("first_slice_data_validation.json", validation),
    ):
        with (output_dir / name).open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    return candidate, validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    _, validation = build_candidate(output_dir)
    print(
        "first_slice_data_complete "
        f"status={validation['status']} "
        f"types={validation['counts']['types']} "
        f"records={validation['counts']['selected_records']} "
        f"missing={validation['counts']['missing_records']} "
        f"review_items={validation['counts']['review_items']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
