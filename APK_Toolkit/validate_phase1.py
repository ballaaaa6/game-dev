#!/usr/bin/env python3
"""Validate the derived Phase 1 catalog without changing source assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from phase_paths import phase_artifacts_dir, phase_docs_dir


TARGET_GROUPS = ("office", "game", "com", "system")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_checksums(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) == 2 and len(parts[0]) == 64:
            values[parts[1].replace("\\", "/")] = parts[0].lower()
    return values


def add_check(checks: list[dict[str, Any]], check_id: str, status: str, details: str) -> None:
    checks.append({"id": check_id, "status": status, "details": details})


def validate(workspace: Path) -> dict[str, Any]:
    phase0_artifacts = phase_artifacts_dir(workspace, 0)
    phase1_artifacts = phase_artifacts_dir(workspace, 1)
    catalog_path = phase1_artifacts / "phase1_asset_catalog.json"
    seb_manifest_path = phase1_artifacts / "phase1_seb_manifest.json"
    trace_path = phase1_artifacts / "phase1_code_trace.json"
    office_manifest_path = phase1_artifacts / "office_manifest.json"
    preview_manifest_path = phase1_artifacts / "phase1_preview_manifest.json"
    legacy_path = phase1_artifacts / "phase1_legacy_asset_map.json"
    audit_path = phase1_artifacts / "phase1_input_audit.json"
    manifest_path = phase0_artifacts / "asset_manifest.json"
    checksum_path = phase0_artifacts / "phase0_checksums.sha256"

    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []
    required = (
        catalog_path,
        seb_manifest_path,
        trace_path,
        office_manifest_path,
        preview_manifest_path,
        legacy_path,
        audit_path,
        manifest_path,
        checksum_path,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        add_check(checks, "derived_artifacts_present", "fail", "; ".join(missing))
        return {
            "schema": 1,
            "generated_at_utc": utc_now(),
            "status": "fail",
            "checks": checks,
            "errors": [f"missing derived artifact: {path}" for path in missing],
            "warnings": [],
        }

    catalog = load_json(catalog_path)
    seb_manifest = load_json(seb_manifest_path)
    trace = load_json(trace_path)
    office_manifest = load_json(office_manifest_path)
    preview_manifest = load_json(preview_manifest_path)
    legacy = load_json(legacy_path)
    audit = load_json(audit_path)
    manifest = load_json(manifest_path)
    phase0 = parse_checksums(checksum_path)
    sprites_root = workspace / "game-dev-story-mod_Sprites"

    expected_count = sum(manifest.get("by_group", {}).get(group, 0) for group in TARGET_GROUPS)
    files = list(catalog.get("files", []))
    add_check(
        checks,
        "catalog_count",
        "pass" if len(files) == expected_count else "fail",
        f"catalog={len(files)} expected={expected_count}",
    )

    paths = [record.get("source", {}).get("relative_path") for record in files]
    duplicate_paths = sorted(path for path, count in Counter(paths).items() if path and count > 1)
    duplicate_ids = sorted(
        id_value for id_value, count in Counter(record.get("id") for record in files).items() if id_value and count > 1
    )
    if duplicate_paths:
        errors.append(f"duplicate catalog paths: {duplicate_paths}")
    if duplicate_ids:
        errors.append(f"duplicate catalog IDs: {duplicate_ids}")
    add_check(
        checks,
        "catalog_unique_keys",
        "pass" if not duplicate_paths and not duplicate_ids else "fail",
        f"duplicate_paths={len(duplicate_paths)} duplicate_ids={len(duplicate_ids)}",
    )

    actual_hash_mismatches: list[str] = []
    phase0_hash_mismatches: list[str] = []
    missing_files: list[str] = []
    png_failures: list[str] = []
    for record in files:
        rel = record.get("source", {}).get("relative_path")
        if not rel:
            errors.append("catalog record has no relative path")
            continue
        path = sprites_root / Path(rel)
        if not path.is_file():
            missing_files.append(rel)
            continue
        actual = sha256_file(path)
        if actual != record.get("source", {}).get("sha256"):
            actual_hash_mismatches.append(rel)
        phase0_key = f"game-dev-story-mod_Sprites/{rel}"
        if phase0.get(phase0_key) != actual:
            phase0_hash_mismatches.append(rel)
        if record.get("extension") == "png" and not record.get("png", {}).get("valid"):
            png_failures.append(rel)
    if missing_files:
        errors.append(f"missing source files: {missing_files}")
    if actual_hash_mismatches:
        errors.append(f"catalog hash mismatches: {actual_hash_mismatches}")
    if phase0_hash_mismatches:
        errors.append(f"Phase 0 hash mismatches: {phase0_hash_mismatches}")
    add_check(
        checks,
        "source_hash_integrity",
        "pass" if not missing_files and not actual_hash_mismatches and not phase0_hash_mismatches else "fail",
        f"missing={len(missing_files)} catalog_mismatch={len(actual_hash_mismatches)} phase0_mismatch={len(phase0_hash_mismatches)}",
    )
    add_check(
        checks,
        "png_metadata",
        "pass" if not png_failures else "fail",
        f"invalid_png_metadata={len(png_failures)}",
    )

    catalog_seb_paths = {
        record.get("source", {}).get("relative_path")
        for record in files
        if record.get("extension") == "seb"
    }
    seb_entries = list(seb_manifest.get("files", []))
    manifest_seb_paths = {entry.get("relative_path") for entry in seb_entries}
    missing_seb_manifest = sorted(catalog_seb_paths - manifest_seb_paths)
    extra_seb_manifest = sorted(manifest_seb_paths - catalog_seb_paths)
    seb_hash_mismatches: list[str] = []
    seb_parse_errors: list[str] = []
    seb_tail_shortfalls: list[dict[str, Any]] = []
    for entry in seb_entries:
        rel = entry.get("relative_path")
        if not rel:
            seb_parse_errors.append("manifest entry has no relative_path")
            continue
        source_path = sprites_root / Path(rel)
        if not source_path.is_file():
            seb_hash_mismatches.append(f"missing:{rel}")
            continue
        actual = sha256_file(source_path)
        if actual != entry.get("sha256"):
            seb_hash_mismatches.append(rel)
        if entry.get("errors"):
            seb_parse_errors.append(f"{rel}: {entry.get('errors')}")
        shortfall = int(entry.get("tail_shortfall_bytes") or 0)
        if shortfall:
            seb_tail_shortfalls.append(
                {
                    "path": rel,
                    "bytes": shortfall,
                    "status": entry.get("status"),
                }
            )
            if entry.get("status") != "truncated_final_record":
                seb_parse_errors.append(f"{rel}: unexpected shortfall status {entry.get('status')}")
    seb_manifest_bad = bool(
        missing_seb_manifest or extra_seb_manifest or seb_hash_mismatches or seb_parse_errors
    )
    if missing_seb_manifest:
        errors.append(f"SEB manifest missing catalog files: {missing_seb_manifest}")
    if extra_seb_manifest:
        errors.append(f"SEB manifest contains non-catalog files: {extra_seb_manifest}")
    if seb_hash_mismatches:
        errors.append(f"SEB manifest hash mismatches: {seb_hash_mismatches}")
    if seb_parse_errors:
        errors.extend(f"SEB manifest parse issue: {item}" for item in seb_parse_errors)
    if seb_tail_shortfalls:
        warnings.append(
            "SEB structural decoder recorded a four-byte final-record shortfall for "
            f"{len(seb_tail_shortfalls)} file(s); source bytes were not padded."
        )
    add_check(
        checks,
        "seb_manifest_integrity",
        "pass" if not seb_manifest_bad else "fail",
        f"catalog_seb={len(catalog_seb_paths)} manifest_seb={len(manifest_seb_paths)} hash_mismatch={len(seb_hash_mismatches)} parse_issues={len(seb_parse_errors)}",
    )
    add_check(
        checks,
        "seb_structural_decode",
        "attention" if seb_tail_shortfalls and not seb_manifest_bad else "pass" if not seb_manifest_bad else "fail",
        f"decoded={len(seb_entries) - len(seb_parse_errors)} tail_shortfall={len(seb_tail_shortfalls)}",
    )

    office_catalog_paths = {
        record.get("source", {}).get("relative_path")
        for record in files
        if record.get("source", {}).get("relative_path", "").startswith("office/")
        and record.get("extension") in {"png", "seb"}
    }
    office_manifest_paths = {item.get("path") for item in office_manifest.get("assets", [])}
    office_missing = sorted(office_catalog_paths - office_manifest_paths)
    office_extra = sorted(office_manifest_paths - office_catalog_paths)
    if office_missing:
        errors.append(f"office manifest missing catalog paths: {office_missing}")
    if office_extra:
        errors.append(f"office manifest contains non-catalog paths: {office_extra}")
    add_check(
        checks,
        "office_manifest_integrity",
        "pass" if not office_missing and not office_extra else "fail",
        f"catalog_office={len(office_catalog_paths)} manifest_office={len(office_manifest_paths)} missing={len(office_missing)} extra={len(office_extra)}",
    )

    trace_source_mismatches: list[str] = []
    for source in trace.get("source_files", []):
        rel = source.get("path")
        path = workspace / Path(rel) if rel else None
        if path is None or not path.is_file():
            trace_source_mismatches.append(f"missing:{rel}")
            continue
        if sha256_file(path) != source.get("sha256"):
            trace_source_mismatches.append(str(rel))
    trace_bad = not trace.get("functions") or bool(trace_source_mismatches)
    if trace_source_mismatches:
        errors.append(f"code trace source mismatches: {trace_source_mismatches}")
    add_check(
        checks,
        "code_trace_integrity",
        "fail" if trace_bad else "pass",
        f"functions={len(trace.get('functions', []))} evidence={len(trace.get('evidence', []))} source_mismatch={len(trace_source_mismatches)}",
    )

    preview_files = [item.get("path") for item in preview_manifest.get("previews", [])]
    missing_previews = [rel for rel in preview_files if not rel or not (workspace / Path(rel)).is_file()]
    if missing_previews:
        errors.append(f"missing preview files: {missing_previews}")
    add_check(
        checks,
        "preview_artifacts_present",
        "pass" if preview_files and not missing_previews else "fail",
        f"declared={len(preview_files)} missing={len(missing_previews)}",
    )

    # Every reference either resolves to a catalog path or is explicitly
    # unresolved.  The validator does not silently promote a basename guess.
    catalog_paths = set(paths)
    inf_unaccounted: list[str] = []
    inf_probable: list[str] = []
    inf_records = [
        (document.get("relative_path"), item)
        for document in legacy.get("inf_documents", [])
        for item in document.get("records", [])
    ]
    for source, item in inf_records:
        resolved = item.get("resolved_relative_path")
        if resolved and resolved not in catalog_paths:
            inf_unaccounted.append(f"{source}:{item.get('line')} -> {resolved}")
        if item.get("resolution") == "unique_basename_extension":
            inf_probable.append(f"{source}:{item.get('line')} {item.get('raw_name')}")
    if inf_unaccounted:
        errors.append(f"INF links outside catalog: {inf_unaccounted}")
    warnings.extend(f"INF adapter resolution remains probable: {item}" for item in inf_probable)
    add_check(
        checks,
        "inf_referential_integrity",
        "pass" if not inf_unaccounted else "fail",
        f"records={len(inf_records)} probable_suffix_recoveries={len(inf_probable)}",
    )

    bonus_rows = legacy.get("bonus_catalog", {}).get("rows", [])
    bonus_errors = list(legacy.get("bonus_catalog", {}).get("errors", []))
    bonus_unaccounted = [
        f"line {row.get('line')}: {row.get('asset_ref')}"
        for row in bonus_rows
        if row.get("asset_relative_path") and row.get("asset_relative_path") not in catalog_paths
    ]
    if bonus_errors:
        errors.extend(f"bonus mapping error: {error}" for error in bonus_errors)
    if bonus_unaccounted:
        errors.append(f"bonus links outside catalog: {bonus_unaccounted}")
    add_check(
        checks,
        "bonus_referential_integrity",
        "pass" if not bonus_errors and not bonus_unaccounted else "fail",
        f"rows={len(bonus_rows)} placeholders={sum(1 for row in bonus_rows if row.get('asset_ref') == '-1')} direct_links={sum(1 for row in bonus_rows if row.get('asset_relative_path'))}",
    )

    office_orphans = legacy.get("office_asset_audit", {}).get("unreferenced_pngs", [])
    floor_pair_gaps = legacy.get("office_asset_audit", {}).get("floor_png_without_same_name_seb", [])
    if office_orphans:
        warnings.append(f"Office PNGs without direct bonus reference: {office_orphans}")
    if floor_pair_gaps:
        warnings.append(f"Office floors without same-name SEB: {floor_pair_gaps}")
    if not audit.get("anomalies", {}).get("seb_tail_shortfall"):
        errors.append("SEB tail shortfall is not recorded in the input audit")
    add_check(
        checks,
        "known_anomalies_are_recorded",
        "pass" if "anomalies" in audit and audit.get("anomalies", {}).get("seb_tail_shortfall") else "fail",
        f"orphan_office_png={len(office_orphans)} floor_pair_gaps={len(floor_pair_gaps)} seb_tail_shortfall={len(audit.get('anomalies', {}).get('seb_tail_shortfall', []))}",
    )

    audit_failures = [check for check in audit.get("checks", []) if check.get("status") == "fail"]
    add_check(
        checks,
        "input_audit_status",
        "pass" if not audit_failures else "fail",
        f"audit_failures={len(audit_failures)}",
    )

    status = "fail" if errors else "pass_with_warnings" if warnings else "pass"
    return {
        "schema": 1,
        "generated_at_utc": utc_now(),
        "phase": "phase1",
        "status": status,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "catalog_files": len(files),
            "catalog_expected_files": expected_count,
            "inf_records": len(inf_records),
            "bonus_rows": len(bonus_rows),
            "phase0_hashes_checked": len(files),
            "seb_manifest_files": len(seb_entries),
            "seb_tail_shortfall_files": len(seb_tail_shortfalls),
        },
    }


def write_markdown(workspace: Path, report: dict[str, Any]) -> None:
    artifacts = phase_artifacts_dir(workspace, 1)
    audit = load_json(artifacts / "phase1_input_audit.json")
    catalog = load_json(artifacts / "phase1_asset_catalog.json")
    legacy = load_json(artifacts / "phase1_legacy_asset_map.json")
    seb_manifest = load_json(artifacts / "phase1_seb_manifest.json")
    trace = load_json(artifacts / "phase1_code_trace.json")
    office_manifest = load_json(artifacts / "office_manifest.json")
    lines = [
        "# Phase 1 Asset Inventory Report",
        "",
        f"Generated: `{report['generated_at_utc']}`",
        "",
        f"Status: **{report['status']}**",
        "",
        "This report is generated from the current extraction roots. Source assets remain read-only.",
        "",
        "## Coverage",
        "",
        f"- Target files: **{catalog['file_count']}**",
        f"- Target PNG: **{audit['counts']['target_png']}**",
        f"- Target SEB: **{audit['counts']['target_seb']}**",
        f"- SEB structurally decoded: **{seb_manifest['counts']['files']}**",
        f"- Target INF: **{audit['counts']['target_inf']}**",
        f"- Office PNG: **{audit['counts']['office_png']}**",
        f"- Bonus catalog rows: **{audit['counts']['bonus_rows']}**",
        f"- Verified code-trace claims: **{trace['summary']['evidence_verified']}**",
        f"- Office manifest assets: **{office_manifest['summary']['office_assets']}**",
        "",
        "## Checks",
        "",
        "| Check | Status | Details |",
        "|---|---|---|",
    ]
    for check in report["checks"]:
        lines.append(f"| `{check['id']}` | **{check['status']}** | {check['details']} |")

    lines.extend(["", "## Current known anomalies", ""])
    anomalies = audit.get("anomalies", {})
    lines.append(f"- INF missing-extension references: **{len(anomalies.get('inf_missing_extension', []))}**")
    lines.append(f"- Office floor PNGs without same-name SEB: **{len(anomalies.get('office_floor_without_same_name_seb', []))}**")
    lines.append(f"- Office PNGs without direct bonus reference: **{len(anomalies.get('office_png_not_directly_referenced_by_bonus', []))}**")
    lines.append(f"- SEB final-record tail shortfalls: **{len(anomalies.get('seb_tail_shortfall', []))}**")
    lines.append("")
    for title, values in (
        ("INF suffix recoveries", anomalies.get("inf_missing_extension", [])),
        ("Office floor/SEB gaps", anomalies.get("office_floor_without_same_name_seb", [])),
        ("Office bonus orphans", anomalies.get("office_png_not_directly_referenced_by_bonus", [])),
        ("SEB tail shortfalls", anomalies.get("seb_tail_shortfall", [])),
    ):
        lines.extend([f"### {title}", ""])
        if values:
            for value in values:
                lines.append(f"- `{json.dumps(value, ensure_ascii=False)}`")
        else:
            lines.append("- None")
        lines.append("")

    lines.extend([
        "## Renderer evidence and office map",
        "",
        f"- Renderer functions indexed: **{trace['summary']['functions_indexed']}**",
        f"- Verified renderer claims: **{trace['summary']['evidence_verified']}**",
        f"- Unresolved contracts retained: **{trace['summary']['unresolved_contracts']}**",
        f"- Office manifest assets: **{office_manifest['summary']['office_assets']}** ({office_manifest['summary']['office_png']} PNG + {office_manifest['summary']['office_seb']} SEB)",
        "",
        "| Evidence | Confidence | Source | Claim |",
        "|---|---|---|---|",
    ])
    for item in trace.get("evidence", []):
        source = item.get("source", {})
        source_label = f"{source.get('path')}:{source.get('line')}"
        lines.append(
            f"| `{item.get('id')}` | **{item.get('confidence')}** | `{source_label}` | {item.get('claim')} |"
        )
    lines.extend([
        "",
        "### Unresolved runtime contracts",
        "",
    ])
    for item in trace.get("unresolved", []):
        lines.append(f"- `{item.get('id')}`: {item.get('claim')} ({item.get('reason')})")
    lines.extend([
        "",
        "## Interpretation rules",
        "",
        "- A unique basename extension match is adapter metadata and remains `probable`; the INF source is unchanged.",
        "- Alpha bounds are visual diagnostics only. They do not establish pivot, seat, collision, or depth semantics.",
        "- SEB fields are structurally decoded from decompiled loader evidence; all current extracted files end four bytes before the declared final record is complete. This may be a legacy variant or an extraction/archive boundary issue and remains unresolved; runtime semantics are not trusted.",
        "- `reception_001` and `reception_002` remain unresolved until code evidence maps the two `-1` catalog rows.",
        "",
        "## Generated artifacts",
        "",
        "- `Phases/Phase1/artifacts/phase1_input_audit.json`",
        "- `Phases/Phase1/artifacts/phase1_asset_catalog.json`",
        "- `Phases/Phase1/artifacts/phase1_seb_manifest.json`",
        "- `Phases/Phase1/artifacts/phase1_code_trace.json`",
        "- `Phases/Phase1/artifacts/office_manifest.json`",
        "- `Phases/Phase1/artifacts/phase1_preview_manifest.json`",
        "- `Phases/Phase1/docs/phase1_office_preview.png`",
        "- `Phases/Phase1/docs/phase1_office_floor_contact_sheet.png`",
        "- `Phases/Phase1/artifacts/phase1_legacy_asset_map.json`",
        "- `Phases/Phase1/artifacts/phase1_validation_report.json`",
    ])
    report_path = phase_docs_dir(workspace, 1) / "phase1_asset_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing Phase 1 derived artifacts",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    try:
        report = validate(workspace)
        report_path = phase_artifacts_dir(workspace, 1) / "phase1_validation_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        write_markdown(workspace, report)
    except Exception as exc:
        print(f"[ERROR] Phase 1 validation failed to run: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Phase 1 validation status: {report['status']}")
    for check in report["checks"]:
        print(f"[{check['status'].upper()}] {check['id']}: {check['details']}")
    for warning in report["warnings"]:
        print(f"[WARN] {warning}")
    for error in report["errors"]:
        print(f"[ERROR] {error}", file=sys.stderr)
    return 0 if report["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
