#!/usr/bin/env python3
"""Create reproducible Phase 0 manifests without modifying extracted sources.

The script only reads the three current source roots and writes baseline
artifacts under ``Phases/Phase0/``. Source roots are never modified.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from phase_paths import phase_artifacts_dir, phase_docs_dir


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PLACEHOLDER_RE = re.compile(r"<\d+>")
FUNCTION_HEADER_RE = re.compile(r"^// Function:\s*.+$", re.MULTILINE)
C_FUNCTION_BLOCK_RE = re.compile(
    r"^// Function:\s*(?P<name>.+?)\r?\n"
    r"// Address:\s*(?P<address>[0-9A-Fa-f]+)\s*$",
    re.MULTILINE,
)

SOURCE_ROOTS = {
    "sprites": "game-dev-story-mod_Sprites",
    "dumped": "game-dev-story-mod_Dumped",
    "extracted": "game-dev-story-mod_Extracted",
}

KEY_FILES = [
    "game-dev-story-mod_Sprites/extraction_report.json",
    "game-dev-story-mod_Dumped/Exported_ALL.c",
    "game-dev-story-mod_Dumped/Exported_ALL.recovered.c",
    "game-dev-story-mod_Dumped/Exported_FAILED.c",
    "game-dev-story-mod_Dumped/Exported_ALL.report.json",
    "game-dev-story-mod_Dumped/Exported_FAILED.report.json",
    "game-dev-story-mod_Dumped/ghidra_symbols.report.json",
    "game-dev-story-mod_Dumped/Failed_Functions_Assembly/failed_functions.asm.txt",
    "game-dev-story-mod_Dumped/Failed_Functions_Assembly/failed_functions.asm.report.json",
    "game-dev-story-mod_Dumped/dump.cs",
    "game-dev-story-mod_Dumped/il2cpp.h",
    "game-dev-story-mod_Dumped/script.json",
    "game-dev-story-mod_Dumped/stringliteral.json",
    "game-dev-story-mod_Dumped/libil2cpp.so",
    "game-dev-story-mod_Extracted/AndroidManifest.xml",
    "game-dev-story-mod_Extracted/assets/bin/Data/Managed/Metadata/global-metadata.dat",
    "game-dev-story-mod_Extracted/lib/arm64-v8a/libil2cpp.so",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )


def rel_to_root(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def rel_to_workspace(path: Path, workspace: Path) -> str:
    return path.relative_to(workspace).as_posix()


def iter_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.as_posix().lower(),
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> dict[str, int] | None:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
        if len(header) < 24 or not header.startswith(PNG_SIGNATURE):
            return None
        width, height = struct.unpack(">II", header[16:24])
        return {"width": width, "height": height}
    except (OSError, struct.error):
        return None


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def summarize_root(root: Path, workspace: Path) -> dict[str, Any]:
    files = iter_files(root)
    extension_counts = Counter(
        (path.suffix.lower().lstrip(".") or "[no-extension]") for path in files
    )
    top_level_counts = Counter(
        (path.relative_to(root).parts[0] if path.relative_to(root).parts else "[root]")
        for path in files
    )
    total_bytes = sum(path.stat().st_size for path in files)
    newest = max((path.stat().st_mtime for path in files), default=None)
    return {
        "path": rel_to_workspace(root, workspace),
        "absolute_path": str(root),
        "exists": root.is_dir(),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "newest_file_mtime_utc": (
            datetime.fromtimestamp(newest, timezone.utc).isoformat().replace("+00:00", "Z")
            if newest is not None
            else None
        ),
        "by_extension": dict(sorted(extension_counts.items())),
        "by_top_level": dict(sorted(top_level_counts.items())),
    }


def build_asset_manifest(workspace: Path, generated_at: str) -> dict[str, Any]:
    root = workspace / SOURCE_ROOTS["sprites"]
    files = iter_files(root)
    entries: list[dict[str, Any]] = []
    extension_counts = Counter()
    top_level_counts = Counter()

    for path in files:
        relative = rel_to_root(path, root)
        extension = path.suffix.lower().lstrip(".") or "[no-extension]"
        top_level = Path(relative).parts[0] if Path(relative).parts else "[root]"
        extension_counts[extension] += 1
        top_level_counts[top_level] += 1

        entry: dict[str, Any] = {
            "path": f"{SOURCE_ROOTS['sprites']}/{relative}",
            "relative_path": relative,
            "group": top_level,
            "extension": extension,
            "size_bytes": path.stat().st_size,
            "modified_utc": iso_mtime(path),
            "sha256": sha256_file(path),
        }
        dimensions = png_dimensions(path) if extension == "png" else None
        if dimensions:
            entry["dimensions"] = dimensions
        entries.append(entry)

    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "source_root": SOURCE_ROOTS["sprites"],
        "source_policy": "Current extracted output; do not edit source files during analysis.",
        "file_count": len(entries),
        "total_bytes": sum(entry["size_bytes"] for entry in entries),
        "by_extension": dict(sorted(extension_counts.items())),
        "by_group": dict(sorted(top_level_counts.items())),
        "files": entries,
    }


def parse_language_file(path: Path, workspace: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    decode_error: str | None = None
    try:
        text = raw.decode("utf-8-sig")
        strict_utf8 = True
    except UnicodeDecodeError as exc:
        decode_error = str(exc)
        text = raw.decode("utf-8-sig", errors="replace")
        strict_utf8 = False

    metadata: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("@"):
            continue
        key, separator, value = line.partition(",")
        if not separator:
            key, separator, value = line.partition("=")
        metadata.setdefault(key, []).append(value if separator else "")

    ids: list[str] = []
    record_rows = 0
    continuation_row_count = 0
    nonstandard_id_rows: list[str] = []
    malformed_rows: list[str] = []
    csv_syntax_warnings: list[str] = []
    for row_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.startswith("@"):
            continue
        record_id = line.split(",", 1)[0].strip()
        if not record_id:
            # The source tables use leading-comma continuation rows for text
            # belonging to the previous language entry.
            continuation_row_count += 1
            continue
        record_rows += 1
        if re.fullmatch(r"#\d+", record_id):
            ids.append(record_id)
        elif re.fullmatch(r"\d+", record_id):
            nonstandard_id_rows.append(f"line {row_number}: {record_id}")
        else:
            malformed_rows.append(f"line {row_number}: {record_id[:80]}")
        try:
            list(csv.reader([line], strict=True))
        except csv.Error as exc:
            # Some original Kairosoft rows contain unescaped quotes inside a
            # quoted message. Keep the evidence, but do not rewrite source CSV.
            csv_syntax_warnings.append(f"line {row_number}: {exc}")

    duplicates = sorted(record_id for record_id, count in Counter(ids).items() if count > 1)
    numeric_ids = [int(record_id[1:]) for record_id in ids]
    placeholder_tokens = sorted(set(PLACEHOLDER_RE.findall(text)))
    locale_match = re.match(r"GameDevStory_(.+)\.csv$", path.name, re.IGNORECASE)
    locale = locale_match.group(1) if locale_match else path.stem

    return {
        "path": rel_to_workspace(path, workspace),
        "relative_path": rel_to_root(path, workspace / SOURCE_ROOTS["sprites"]),
        "locale": locale,
        "size_bytes": len(raw),
        "modified_utc": iso_mtime(path),
        "sha256": sha256_file(path),
        "has_utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
        "strict_utf8": strict_utf8,
        "decode_error": decode_error,
        "line_count": len(text.splitlines()),
        "metadata": metadata,
        "record_count": record_rows,
        "canonical_id_count": len(ids),
        "continuation_row_count": continuation_row_count,
        "first_id": ids[0] if ids else None,
        "last_id": ids[-1] if ids else None,
        "min_numeric_id": min(numeric_ids) if numeric_ids else None,
        "max_numeric_id": max(numeric_ids) if numeric_ids else None,
        "duplicate_ids": duplicates,
        "nonstandard_id_rows": nonstandard_id_rows,
        "malformed_rows": malformed_rows,
        "csv_syntax_warnings": csv_syntax_warnings,
        "placeholder_tokens": placeholder_tokens,
    }


def build_language_manifest(workspace: Path, generated_at: str) -> dict[str, Any]:
    root = workspace / SOURCE_ROOTS["sprites"]
    language_root = root / "language"
    entries = [
        parse_language_file(path, workspace)
        for path in sorted(language_root.glob("*.csv"), key=lambda item: item.name.lower())
    ]
    locales = [entry["locale"] for entry in entries]
    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "source_root": f"{SOURCE_ROOTS['sprites']}/language",
        "file_count": len(entries),
        "locales": locales,
        "files": entries,
    }


def hash_key_files(workspace: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for relative in KEY_FILES:
        path = workspace / Path(relative)
        if not path.is_file():
            results.append({"path": relative, "exists": False})
            continue
        results.append(
            {
                "path": relative,
                "exists": True,
                "size_bytes": path.stat().st_size,
                "modified_utc": iso_mtime(path),
                "sha256": sha256_file(path),
            }
        )
    return results


def function_header_count(path: Path) -> int | None:
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    return len(FUNCTION_HEADER_RE.findall(text))


def c_function_headers(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    return [
        {"name": match.group("name").strip(), "address": match.group("address").lower()}
        for match in C_FUNCTION_BLOCK_RE.finditer(text)
    ]


def collection_summary(root: Path, workspace: Path) -> dict[str, Any]:
    files = iter_files(root)
    return {
        "path": rel_to_workspace(root, workspace),
        "exists": root.is_dir(),
        "file_count": len(files),
        "total_bytes": sum(path.stat().st_size for path in files),
        "files": [rel_to_workspace(path, workspace) for path in files],
    }


def build_code_coverage(workspace: Path) -> dict[str, Any]:
    dumped_root = workspace / SOURCE_ROOTS["dumped"]
    main_report_path = dumped_root / "Exported_ALL.report.json"
    recovery_report_path = dumped_root / "Exported_FAILED.report.json"
    assembly_report_path = dumped_root / "Failed_Functions_Assembly" / "failed_functions.asm.report.json"
    main_report = load_json(main_report_path) or {}
    recovery_report = load_json(recovery_report_path) or {}
    assembly_report = load_json(assembly_report_path) or {}

    main_headers = c_function_headers(dumped_root / "Exported_ALL.c")
    recovered_headers = c_function_headers(dumped_root / "Exported_ALL.recovered.c")
    main_addresses = {entry["address"] for entry in main_headers}
    recovered_addresses = {entry["address"] for entry in recovered_headers}
    recovered_only_addresses = sorted(recovered_addresses - main_addresses)
    recovered_by_address = {entry["address"]: entry for entry in recovered_headers}

    assembly_functions: list[dict[str, Any]] = []
    for item in assembly_report.get("functions") or []:
        if not isinstance(item, dict):
            continue
        address = str(item.get("address", "")).lower()
        assembly_name = Path(str(item.get("file", ""))).name
        assembly_functions.append(
            {
                "address": address,
                "name": item.get("name"),
                "status": item.get("status"),
                "instructions": item.get("instructions"),
                "file": (
                    f"{SOURCE_ROOTS['dumped']}/Failed_Functions_Assembly/{assembly_name}"
                    if assembly_name
                    else None
                ),
                "c_status": (
                    "recovered_c"
                    if address in recovered_only_addresses
                    else "assembly_only"
                    if address not in recovered_addresses
                    else "main_c"
                ),
            }
        )

    remaining_without_c = [
        item for item in assembly_functions if item["address"] not in recovered_addresses
    ]
    main_failed_names = [
        item.get("name")
        for item in (main_report.get("failed_functions") or [])
        if isinstance(item, dict)
    ]
    effective_coverage_count = len(recovered_headers) + len(remaining_without_c)
    total_functions = int(main_report.get("total_functions", 0) or 0)
    return {
        "schema": 1,
        "source_root": SOURCE_ROOTS["dumped"],
        "main_export": {
            "report": rel_to_workspace(main_report_path, workspace),
            "c_file": rel_to_workspace(dumped_root / "Exported_ALL.c", workspace),
            "total_functions": total_functions,
            "successful_functions": int(main_report.get("successful_functions", 0) or 0),
            "failed_functions": int(main_report.get("failed_functions_count", 0) or 0),
            "failed_names": main_failed_names,
            "c_function_headers": len(main_headers),
        },
        "recovery_stage": {
            "report": rel_to_workspace(recovery_report_path, workspace),
            "c_file": rel_to_workspace(dumped_root / "Exported_FAILED.c", workspace),
            "selected_functions": int(recovery_report.get("total_functions", 0) or 0),
            "successful_functions": int(recovery_report.get("successful_functions", 0) or 0),
            "failed_functions": int(recovery_report.get("failed_functions_count", 0) or 0),
            "c_functions_added": len(recovered_only_addresses),
            "new_c_addresses": recovered_only_addresses,
        },
        "combined_c": {
            "canonical_file": rel_to_workspace(dumped_root / "Exported_ALL.recovered.c", workspace),
            "function_headers": len(recovered_headers),
            "total_functions": total_functions,
            "remaining_without_c": max(total_functions - len(recovered_headers), 0),
            "complete": total_functions > 0 and len(recovered_headers) == total_functions,
            "new_c_functions": [recovered_by_address[address] for address in recovered_only_addresses],
        },
        "assembly_fallback": {
            "report": rel_to_workspace(assembly_report_path, workspace),
            "function_count": len(assembly_functions),
            "status_ok_count": sum(1 for item in assembly_functions if item["status"] == "ok"),
            "complete_for_main_failures": len(assembly_functions) == len(main_failed_names)
            and all(item["status"] == "ok" for item in assembly_functions),
            "functions": assembly_functions,
        },
        "remaining_without_c": remaining_without_c,
        "effective_coverage": {
            "c_functions": len(recovered_headers),
            "assembly_only_functions": len(remaining_without_c),
            "covered_functions": effective_coverage_count,
            "total_functions": total_functions,
            "complete": total_functions > 0 and effective_coverage_count == total_functions,
        },
    }


def make_check(check_id: str, status: str, details: str) -> dict[str, str]:
    return {"id": check_id, "status": status, "details": details}


def build_baseline(
    workspace: Path,
    generated_at: str,
    asset_manifest: dict[str, Any],
    language_manifest: dict[str, Any],
    key_hashes: list[dict[str, Any]],
) -> dict[str, Any]:
    sprites_root = workspace / SOURCE_ROOTS["sprites"]
    dumped_root = workspace / SOURCE_ROOTS["dumped"]
    extracted_root = workspace / SOURCE_ROOTS["extracted"]
    extraction_report_path = sprites_root / "extraction_report.json"
    extraction_report = load_json(extraction_report_path) or {}
    export_report = load_json(dumped_root / "Exported_ALL.report.json") or {}
    failed_report = load_json(dumped_root / "Exported_FAILED.report.json") or {}
    symbols_report = load_json(dumped_root / "ghidra_symbols.report.json") or {}
    code_coverage = build_code_coverage(workspace)
    bodyface_path = dumped_root / "bodyface_records.reference.json"
    bodyface = load_json(bodyface_path)
    bodyface_count = len(bodyface) if isinstance(bodyface, list) else None

    actual_output = sprites_root.resolve()
    reported_output = extraction_report.get("output")
    reported_output_resolved: str | None = None
    if isinstance(reported_output, str):
        reported_output_resolved = str(Path(reported_output).resolve())

    actual_input = (extracted_root / "assets" / "bin" / "Data").resolve()
    reported_input = extraction_report.get("input")
    reported_input_resolved: str | None = None
    if isinstance(reported_input, str):
        reported_input_resolved = str(Path(reported_input).resolve())

    body_files = sorted((sprites_root / "game").glob("body*.png"))
    face_files = sorted((sprites_root / "game").glob("face_*.png"))
    png_files = [entry for entry in asset_manifest["files"] if entry["extension"] == "png"]
    csv_files = [entry for entry in asset_manifest["files"] if entry["extension"] == "csv"]

    checks: list[dict[str, str]] = []
    roots_present = all(
        (workspace / relative).is_dir() for relative in SOURCE_ROOTS.values()
    )
    checks.append(
        make_check(
            "source_roots_present",
            "pass" if roots_present else "fail",
            "All three current source roots exist." if roots_present else "At least one source root is missing.",
        )
    )

    report_errors = extraction_report.get("errors") or []
    checks.append(
        make_check(
            "asset_report_errors",
            "pass" if not report_errors else "attention",
            f"extraction_report.json errors={len(report_errors)}.",
        )
    )

    output_matches = reported_output_resolved == str(actual_output)
    checks.append(
        make_check(
            "asset_report_output_path",
            "pass" if output_matches else "attention",
            (
                "Report output path matches the current sprites root."
                if output_matches
                else f"Report says {reported_output!r}; current root is {str(actual_output)!r}."
            ),
        )
    )

    input_matches = reported_input_resolved == str(actual_input)
    checks.append(
        make_check(
            "asset_report_input_path",
            "pass" if input_matches else "attention",
            (
                "Report input path matches the current extracted root."
                if input_matches
                else f"Report says {reported_input!r}; current root is {str(actual_input)!r}."
            ),
        )
    )

    csv_strict_ok = all(
        entry["strict_utf8"] and entry["has_utf8_bom"] and not entry["decode_error"]
        for entry in language_manifest["files"]
    )
    checks.append(
        make_check(
            "language_files_valid",
            "pass" if csv_strict_ok else "attention",
            f"Validated {len(language_manifest['files'])} CSV files for BOM and strict UTF-8 bytes.",
        )
    )

    language_id_issues = sum(
        len(entry["duplicate_ids"])
        + len(entry["nonstandard_id_rows"])
        + len(entry["malformed_rows"])
        for entry in language_manifest["files"]
    )
    checks.append(
        make_check(
            "language_id_shape",
            "attention" if language_id_issues else "pass",
            f"Found {language_id_issues} non-canonical/duplicate language ID row issue(s); source CSV was not changed.",
        )
    )

    report_warning_count = len(extraction_report.get("warnings") or [])
    checks.append(
        make_check(
            "extractor_warning_provenance",
            "attention" if report_warning_count else "pass",
            f"Extractor report retains {report_warning_count} warning record(s); current CSV bytes are validated separately.",
        )
    )

    report_file_count = int(extraction_report.get("files_extracted", 0) or 0)
    raw_asset_count = int(extraction_report.get("raw_assets", 0) or 0)
    report_reconciles = report_file_count + raw_asset_count + 1 == asset_manifest["file_count"]
    checks.append(
        make_check(
            "asset_file_count_reconciles",
            "pass" if report_reconciles else "attention",
            f"Current files={asset_manifest['file_count']}; report extracted={report_file_count}, raw={raw_asset_count}, report-file=1.",
        )
    )

    code_total = code_coverage["main_export"]["total_functions"]
    code_success = code_coverage["main_export"]["successful_functions"]
    code_failed = code_coverage["main_export"]["failed_functions"]
    recovery_success = code_coverage["recovery_stage"]["c_functions_added"]
    combined_c = code_coverage["combined_c"]["function_headers"]
    remaining_c = code_coverage["combined_c"]["remaining_without_c"]
    c_headers = combined_c
    assembly_ok = code_coverage["assembly_fallback"]["complete_for_main_failures"]
    checks.append(
        make_check(
            "code_export_baseline",
            "pass" if combined_c + remaining_c == code_total else "attention",
            f"Main export={code_success}/{code_total}; recovery added={recovery_success}; combined C={combined_c}/{code_total}; C-only remaining={remaining_c}.",
        )
    )
    checks.append(
        make_check(
            "code_decompile_completeness",
            "pass" if remaining_c == 0 else "attention",
            f"Canonical recovered C has {combined_c}/{code_total} function headers; {remaining_c} function(s) remain assembly-only.",
        )
    )
    checks.append(
        make_check(
            "assembly_fallback_coverage",
            "pass" if assembly_ok else "attention",
            f"Assembly fallback covers {code_coverage['assembly_fallback']['function_count']} functions; status ok={code_coverage['assembly_fallback']['status_ok_count']}; C-only remaining={remaining_c}.",
        )
    )

    stale_tool_paths = []
    for log_name in ("ghidra_export.log", "ghidra_recovery.log", "ghidra_assembly.log"):
        log_path = dumped_root / log_name
        if log_path.is_file():
            text = log_path.read_text(encoding="utf-8", errors="ignore")
            if "APK_Toolkit" in text:
                stale_tool_paths.append(log_name)
    checks.append(
        make_check(
            "tool_log_provenance",
            "attention" if stale_tool_paths else "pass",
            (
                "Logs contain legacy APK_Toolkit absolute paths: " + ", ".join(stale_tool_paths)
                if stale_tool_paths
                else "Current logs do not contain legacy APK_Toolkit path references."
            ),
        )
    )

    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase0_status": "complete_with_known_limitations",
        "source_policy": "Data-first; current extraction roots are authoritative and source files remain untouched.",
        "source_roots": {
            name: summarize_root(workspace / relative, workspace)
            for name, relative in SOURCE_ROOTS.items()
        },
        "observed_counts": {
            "sprites_files": asset_manifest["file_count"],
            "sprites_total_bytes": asset_manifest["total_bytes"],
            "sprites_png": len(png_files),
            "sprites_csv": len(csv_files),
            "language_files": language_manifest["file_count"],
            "body_assets": len(body_files),
            "face_assets": len(face_files),
            "bodyface_records": bodyface_count,
            "code_total_functions": code_total,
            "code_main_successful_functions": code_success,
            "code_main_failed_functions": code_failed,
            "code_recovery_added_functions": recovery_success,
            "code_combined_c_functions": combined_c,
            "code_remaining_c_functions": remaining_c,
            "code_function_headers": c_headers,
            "assembly_fallback_functions": code_coverage["assembly_fallback"]["function_count"],
            "assembly_ok_functions": code_coverage["assembly_fallback"]["status_ok_count"],
            "categorized_code_files": len(iter_files(dumped_root / "Categorized_Code")),
            "assembly_files": len(iter_files(dumped_root / "Failed_Functions_Assembly")),
            "ghidra_address_count": symbols_report.get("address_count"),
            "ghidra_labels_created": symbols_report.get("labels_created"),
        },
        "analysis_collections": {
            "categorized_code": collection_summary(dumped_root / "Categorized_Code", workspace),
            "failed_functions_assembly": collection_summary(
                dumped_root / "Failed_Functions_Assembly", workspace
            ),
        },
        "extraction_report": {
            "path": rel_to_workspace(extraction_report_path, workspace),
            "reported_input": reported_input,
            "reported_output": reported_output,
            "actual_input": rel_to_workspace(actual_input, workspace),
            "actual_output": rel_to_workspace(sprites_root, workspace),
            "input_path_matches": input_matches,
            "output_path_matches": output_matches,
            "bundle_candidates": extraction_report.get("bundle_candidates"),
            "textassets": extraction_report.get("textassets"),
            "archives": extraction_report.get("archives"),
            "files_extracted": report_file_count,
            "raw_assets": raw_asset_count,
            "warnings": extraction_report.get("warnings") or [],
            "errors": report_errors,
        },
        "code_reports": {
            "coverage": code_coverage,
            "export_all": {
                "path": "game-dev-story-mod_Dumped/Exported_ALL.report.json",
                "total_functions": code_total,
                "successful_functions": code_success,
                "failed_functions": code_failed,
                "failed_names": [
                    item.get("name")
                    for item in (export_report.get("failed_functions") or [])
                    if isinstance(item, dict)
                ],
            },
            "export_failed_stage": {
                "path": "game-dev-story-mod_Dumped/Exported_FAILED.report.json",
                "total_functions": failed_report.get("total_functions"),
                "successful_functions": failed_report.get("successful_functions"),
                "failed_functions": failed_report.get("failed_functions_count"),
            },
            "ghidra_symbols": {
                "path": "game-dev-story-mod_Dumped/ghidra_symbols.report.json",
                "address_count": symbols_report.get("address_count"),
                "functions_existing": symbols_report.get("functions_existing"),
                "labels_created": symbols_report.get("labels_created"),
                "function_errors": symbols_report.get("function_errors") or [],
            },
        },
        "key_file_hashes": key_hashes,
        "checks": checks,
        "known_limitations": [
            "The extraction report output path points to game-dev-story-mod_Sprites_fixed while the current source root is game-dev-story-mod_Sprites.",
            "The extraction report retains three repaired trailing UTF-8 warning records; current CSV bytes pass strict UTF-8/BOM validation.",
            "The main C export originally had five failures; recovery added one function, leaving four functions without C decompile. All five failed-function assembly fallbacks are present and marked ok.",
            "Some Ghidra logs contain legacy absolute paths under APK_Toolkit; these are provenance notes, not current source roots.",
            "No semantic meaning is assigned to character modes or animation states in Phase 0.",
        ],
        "generated_artifacts": [
            "Phases/Phase0/artifacts/asset_manifest.json",
            "Phases/Phase0/artifacts/language_manifest.json",
            "Phases/Phase0/artifacts/phase0_baseline.json",
            "Phases/Phase0/artifacts/code_coverage_manifest.json",
            "Phases/Phase0/artifacts/phase0_checksums.sha256",
            "Phases/Phase0/docs/phase0_baseline_report.md",
        ],
    }


def write_checksums(
    workspace: Path,
    asset_manifest: dict[str, Any],
    language_manifest: dict[str, Any],
    key_hashes: list[dict[str, Any]],
    generated_at: str,
) -> None:
    lines = [
        "# SHA-256 baseline generated by APK_Toolkit/create_phase0_baseline.py",
        f"# generated_at_utc: {generated_at}",
        "# scope: every file under game-dev-story-mod_Sprites plus selected key files under Dumped/Extracted",
    ]
    seen: set[str] = set()
    for entry in asset_manifest["files"]:
        path = entry["path"]
        lines.append(f"{entry['sha256']}  {path}")
        seen.add(path)
    for entry in language_manifest["files"]:
        path = entry["path"]
        if path not in seen:
            lines.append(f"{entry['sha256']}  {path}")
            seen.add(path)
    for entry in key_hashes:
        if entry.get("exists") and entry["path"] not in seen:
            lines.append(f"{entry['sha256']}  {entry['path']}")
            seen.add(entry["path"])
    output = phase_artifacts_dir(workspace, 0) / "phase0_checksums.sha256"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_report(baseline: dict[str, Any]) -> str:
    counts = baseline["observed_counts"]
    extraction = baseline["extraction_report"]
    code = baseline["code_reports"]["coverage"]
    roots = baseline["source_roots"]
    checks = baseline["checks"]
    lines = [
        "# Phase 0 Baseline Report",
        "",
        f"Generated: `{baseline['generated_at_utc']}`",
        "",
        f"Status: **{baseline['phase0_status']}**",
        "",
        "Phase 0 freezes the current extraction set for later comparison. The source roots were read only; no extracted asset, dump, APK or Ghidra project was modified.",
        "",
        "## Source roots",
        "",
        "| Root | Exists | Files | Bytes | Newest file (UTC) |",
        "|---|---:|---:|---:|---|",
    ]
    for name in ("sprites", "dumped", "extracted"):
        root = roots[name]
        lines.append(
            f"| `{root['path']}` | {root['exists']} | {root['file_count']:,} | {root['total_bytes']:,} | `{root['newest_file_mtime_utc']}` |"
        )

    lines.extend(
        [
            "",
            "## Observed baseline",
            "",
            f"- Sprites output: **{counts['sprites_files']:,} files**, including {counts['sprites_png']} PNG and {counts['sprites_csv']} CSV files.",
            f"- Language tables: **{counts['language_files']} locales**.",
            f"- Character assets: **{counts['body_assets']} body** and **{counts['face_assets']} face** PNG files.",
            f"- Body-face records: **{counts['bodyface_records']}**.",
            f"- IL2CPP C export: main **{code['main_export']['successful_functions']:,}/{code['main_export']['total_functions']:,}**, recovery added **{code['recovery_stage']['c_functions_added']}**, canonical combined C **{code['combined_c']['function_headers']:,}/{code['combined_c']['total_functions']:,}**; C-only remaining: **{code['combined_c']['remaining_without_c']}**.",
            f"- Assembly fallback: **{code['assembly_fallback']['status_ok_count']}/{code['assembly_fallback']['function_count']}** functions marked `ok`; effective C/assembly coverage: **{code['effective_coverage']['covered_functions']:,}/{code['effective_coverage']['total_functions']:,}**.",
            f"- Ghidra symbols: `{counts['ghidra_address_count']}` addresses and `{counts['ghidra_labels_created']}` labels created.",
            "",
            "## Validation checks",
            "",
            "| Check | Status | Details |",
            "|---|---|---|",
        ]
    )
    for check in checks:
        lines.append(f"| `{check['id']}` | **{check['status']}** | {check['details']} |")

    lines.extend(
        [
            "",
            "## Extraction report reconciliation",
            "",
            f"- Report input: `{extraction['reported_input']}`",
            f"- Current input: `{extraction['actual_input']}`",
            f"- Report output: `{extraction['reported_output']}`",
            f"- Current output: `{extraction['actual_output']}`",
            f"- Reported extracted files: `{extraction['files_extracted']}`; raw assets: `{extraction['raw_assets']}`; report warnings: `{len(extraction['warnings'])}`; errors: `{len(extraction['errors'])}`.",
            "",
            "## Known limitations carried forward",
            "",
        ]
    )
    for limitation in baseline["known_limitations"]:
        lines.append(f"- {limitation}")

    lines.extend(
        [
            "",
            "## Generated artifacts",
            "",
            "- `Phases/Phase0/artifacts/asset_manifest.json` — every file under the current sprites root, dimensions for PNG files, modification time and SHA-256.",
            "- `Phases/Phase0/artifacts/language_manifest.json` — locale metadata, IDs, placeholder tokens, duplicate/malformed row checks and SHA-256 for each CSV.",
            "- `Phases/Phase0/artifacts/phase0_baseline.json` — source-root summary, report reconciliation, code baseline and validation checks.",
            "- `Phases/Phase0/artifacts/code_coverage_manifest.json` — separates the original five export failures, the one recovered C function, the four remaining C gaps and all assembly fallbacks.",
            "- `Phases/Phase0/artifacts/phase0_checksums.sha256` — reproducible checksum list for all sprite files and selected key dump/input files.",
            "",
            "## Next phase",
            "",
            "Phase 1 can now inventory the office/game/com/system assets and create the visual office map. The path mismatch and extractor warning records should remain visible until the extraction pipeline is either rerun or explicitly documented as historical provenance.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Workspace root (defaults to the parent of APK_Toolkit).",
    )
    args = parser.parse_args()
    workspace = args.root.resolve()
    generated_at = utc_now()

    asset_manifest = build_asset_manifest(workspace, generated_at)
    language_manifest = build_language_manifest(workspace, generated_at)
    key_hashes = hash_key_files(workspace)
    baseline = build_baseline(
        workspace,
        generated_at,
        asset_manifest,
        language_manifest,
        key_hashes,
    )

    artifacts = phase_artifacts_dir(workspace, 0)
    write_json(artifacts / "asset_manifest.json", asset_manifest)
    write_json(artifacts / "language_manifest.json", language_manifest)
    write_json(artifacts / "code_coverage_manifest.json", baseline["code_reports"]["coverage"])
    write_json(artifacts / "phase0_baseline.json", baseline)
    write_checksums(workspace, asset_manifest, language_manifest, key_hashes, generated_at)
    report_path = phase_docs_dir(workspace, 0) / "phase0_baseline_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(baseline), encoding="utf-8")

    print(f"[OK] Generated {asset_manifest['file_count']} asset entries.")
    print(f"[OK] Generated {language_manifest['file_count']} language entries.")
    print(f"[OK] Hashed {sum(1 for item in key_hashes if item.get('exists'))} selected key files.")
    print(
        "[INFO] C coverage: "
        f"main={baseline['observed_counts']['code_main_successful_functions']}/"
        f"{baseline['observed_counts']['code_total_functions']}, "
        f"recovery_added={baseline['observed_counts']['code_recovery_added_functions']}, "
        f"combined={baseline['observed_counts']['code_combined_c_functions']}, "
        f"remaining_c={baseline['observed_counts']['code_remaining_c_functions']}, "
        f"assembly={baseline['observed_counts']['assembly_ok_functions']}/"
        f"{baseline['observed_counts']['assembly_fallback_functions']}."
    )
    print(f"[INFO] Phase 0 status: {baseline['phase0_status']}.")
    for check in baseline["checks"]:
        print(f"[{check['status'].upper()}] {check['id']}: {check['details']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
