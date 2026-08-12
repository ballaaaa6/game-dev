#!/usr/bin/env python3
"""Build and verify the P0-A0 corpus baseline manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "p0-a0.corpus-baseline.v1"
CHUNK_SIZE = 1024 * 1024
SOURCE_ROOTS = {
    "sprites": "game-dev-story-mod_Sprites",
    "dumped": "game-dev-story-mod_Dumped",
    "extracted": "game-dev-story-mod_Extracted",
}
ARTIFACT_ROOTS = {
    "phase0_artifacts": "Phases/Phase0/artifacts",
    "phase4_artifacts": "Phases/Phase4/artifacts",
    "phase5_artifacts": "Phases/Phase5/artifacts",
    "phase6_artifacts": "Phases/Phase6/artifacts",
}
EXCLUDED_GENERATED_ROOT = "Phases/Phase4/artifacts/corpus"
TEXT_SUFFIXES = {
    ".asm",
    ".bat",
    ".c",
    ".cfg",
    ".conf",
    ".cpp",
    ".cs",
    ".css",
    ".csv",
    ".h",
    ".html",
    ".inf",
    ".ini",
    ".js",
    ".json",
    ".log",
    ".md",
    ".py",
    ".report",
    ".sha256",
    ".sh",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def normalize_relative_path(path: Path, root: Path) -> str:
    """Return a workspace-relative POSIX path and reject paths outside root."""

    root_resolved = root.resolve()
    path_resolved = path.resolve()
    try:
        relative = path_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"Path escapes workspace root: {path}") from exc
    return relative.as_posix()


def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest of one file read as binary chunks."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_metadata(path: Path) -> tuple[str, int, int | None, str, bool]:
    digest = hashlib.sha256()
    total_bytes = 0
    newline_count = 0
    has_nul = False
    sample = bytearray()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
            total_bytes += len(chunk)
            newline_count += chunk.count(b"\n")
            if b"\x00" in chunk:
                has_nul = True
            if len(sample) < 8192:
                sample.extend(chunk[: 8192 - len(sample)])

    suffix = path.suffix.lower()
    looks_like_text = suffix in TEXT_SUFFIXES and not has_nul
    if looks_like_text:
        try:
            bytes(sample).decode("utf-8")
        except UnicodeDecodeError:
            looks_like_text = False

    return (
        digest.hexdigest(),
        total_bytes,
        newline_count if looks_like_text else None,
        "utf-8" if looks_like_text else None,
        not looks_like_text,
    )


def _record_file(path: Path, workspace_root: Path, root_id: str, role: str) -> dict[str, Any]:
    digest, total_bytes, line_count, text_encoding, is_binary = _file_metadata(path)
    return {
        "path": normalize_relative_path(path, workspace_root),
        "root_id": root_id,
        "role": role,
        "exists": True,
        "bytes": total_bytes,
        "sha256": digest,
        "line_count": line_count,
        "text_encoding": text_encoding,
        "is_binary": is_binary,
    }


def _scan_root(workspace_root: Path, relative_root: str, root_id: str, role: str) -> list[dict[str, Any]]:
    root = workspace_root / relative_root
    if not root.is_dir():
        raise FileNotFoundError(f"Required input root is missing: {relative_root}")
    records: list[dict[str, Any]] = []
    excluded = Path(EXCLUDED_GENERATED_ROOT).parts
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative_parts = Path(normalize_relative_path(path, workspace_root)).parts
        if role == "artifact" and relative_parts[: len(excluded)] == excluded:
            continue
        records.append(_record_file(path, workspace_root, root_id, role))
    return records


def scan_inputs(root: Path) -> dict[str, list[dict[str, Any]]]:
    """Return sorted source_files and artifact_files for the declared input boundary."""

    workspace_root = root.resolve()
    source_files: list[dict[str, Any]] = []
    artifact_files: list[dict[str, Any]] = []
    for root_id, relative_root in SOURCE_ROOTS.items():
        source_files.extend(_scan_root(workspace_root, relative_root, root_id, "source"))
    for root_id, relative_root in ARTIFACT_ROOTS.items():
        artifact_files.extend(_scan_root(workspace_root, relative_root, root_id, "artifact"))
    source_files.sort(key=lambda row: row["path"])
    artifact_files.sort(key=lambda row: row["path"])
    return {"source_files": source_files, "artifact_files": artifact_files}


def tree_fingerprint(records: list[dict[str, Any]]) -> str:
    """Return the canonical digest of sorted namespace/path/size/hash records."""

    rows = []
    for record in sorted(
        records,
        key=lambda item: (
            str(item.get("role", "")),
            str(item.get("root_id", "")),
            str(item["path"]),
        ),
    ):
        rows.append(
            f'{record.get("role", "")}{chr(0)}{record.get("root_id", "")}{chr(0)}'
            f'{record["path"]}{chr(0)}{record["bytes"]}{chr(0)}{record["sha256"]}{chr(10)}'.encode(
                "utf-8"
            )
        )
    return hashlib.sha256(b"".join(rows)).hexdigest()


def _root_summary(
    records: list[dict[str, Any]], root_id: str, relative_path: str
) -> dict[str, Any]:
    selected = [row for row in records if row["root_id"] == root_id]
    by_extension: dict[str, int] = {}
    for row in selected:
        suffix = Path(row["path"]).suffix.lower() or "[no-extension]"
        by_extension[suffix] = by_extension.get(suffix, 0) + 1
    return {
        "id": root_id,
        "path": relative_path,
        "exists": True,
        "file_count": len(selected),
        "total_bytes": sum(row["bytes"] for row in selected),
        "total_lines": sum(
            row["line_count"] for row in selected if row["line_count"] is not None
        ),
        "by_extension": dict(sorted(by_extension.items())),
        "tree_sha256": tree_fingerprint(selected),
        "status": "pass",
    }


def _read_json_object(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _artifact_input(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    value = _read_json_object(root / record["path"])
    schema: Any = None
    status: Any = "unknown"
    metadata: dict[str, Any] = {}
    if value is not None:
        schema = value.get("schema", value.get("schema_version"))
        status = value.get("phase0_status", value.get("status", "unknown"))
        for key in ("schema_version", "phase", "wave", "stage"):
            if key in value:
                metadata[key] = value[key]
    return {
        "path": record["path"],
        "exists": True,
        "bytes": record["bytes"],
        "sha256": record["sha256"],
        "schema": schema,
        "status": status,
        "role": "phase_artifact",
        "supersedes": [],
        **metadata,
    }


def _derived_counts(root: Path, records: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    counts: dict[str, Any] = {
        "source_file_count": {"value": len(records["source_files"]), "basis": "current_scan"},
        "artifact_file_count": {"value": len(records["artifact_files"]), "basis": "current_scan"},
    }
    phase0_path = root / "Phases/Phase0/artifacts/phase0_baseline.json"
    phase0 = _read_json_object(phase0_path)
    if phase0 and isinstance(phase0.get("observed_counts"), dict):
        for key, value in sorted(phase0["observed_counts"].items()):
            counts[key] = {
                "value": value,
                "basis": "observed_counts",
                "source": "Phases/Phase0/artifacts/phase0_baseline.json",
            }
    function_inventory = _read_json_object(root / "Phases/Phase4/artifacts/function_inventory.json")
    if function_inventory and isinstance(function_inventory.get("shortlist"), list):
        counts["phase4_shortlist_units"] = {
            "value": len(function_inventory["shortlist"]),
            "basis": "function_inventory.shortlist",
            "source": "Phases/Phase4/artifacts/function_inventory.json",
        }
    coverage = _read_json_object(root / "Phases/Phase4/artifacts/translation_coverage.json")
    if coverage and isinstance(coverage.get("summary"), dict):
        for key in ("unit_count", "evidence_ready_units"):
            if key in coverage["summary"]:
                counts[f"phase4_{key}"] = {
                    "value": coverage["summary"][key],
                    "basis": f"translation_coverage.summary.{key}",
                    "source": "Phases/Phase4/artifacts/translation_coverage.json",
                }
    return counts


def _external_tools(root: Path) -> list[dict[str, Any]]:
    script_tools = (
        ("ghidra_headless_script", "game-dev-story-mod_Dumped/ghidra_headless.py"),
        ("ghidra_export_c_script", "game-dev-story-mod_Dumped/ghidra_export_c.py"),
    )
    result: list[dict[str, Any]] = []
    for tool_id, relative in script_tools:
        available = (root / relative).is_file()
        result.append(
            {
                "id": tool_id,
                "path": relative,
                "status": "available" if available else "not_available",
                "required": False,
            }
        )
    for command in ("Cpp2IL", "Cpp2IL.exe"):
        result.append(
            {
                "id": command,
                "command": command,
                "status": "available" if shutil.which(command) else "not_available",
                "required": False,
            }
        )
    return result


def _checks(root: Path, records: dict[str, list[dict[str, Any]]], derived: dict[str, Any]) -> list[dict[str, str]]:
    required_manifests = (
        "Phases/Phase0/artifacts/phase0_baseline.json",
        "Phases/Phase4/artifacts/wave0_build_manifest.json",
        "Phases/Phase5/artifacts/wave5_build_manifest.json",
        "Phases/Phase6/artifacts/wave6_build_manifest.json",
    )
    missing = [relative for relative in required_manifests if not (root / relative).is_file()]
    return [
        {
            "id": "source_roots_present",
            "status": "pass",
            "details": "All declared source roots were scanned.",
        },
        {
            "id": "artifact_inputs_present",
            "status": "pass",
            "details": "All declared artifact roots were scanned.",
        },
        {
            "id": "source_roots_read_only",
            "status": "pass",
            "details": "The builder only reads source roots.",
        },
        {
            "id": "output_excluded",
            "status": "pass"
            if not any(row["path"].startswith(EXCLUDED_GENERATED_ROOT + "/") for row in records["artifact_files"])
            else "attention",
            "details": "Corpus output is excluded from artifact input records.",
        },
        {
            "id": "historical_manifest_inputs_present",
            "status": "pass" if not missing else "attention",
            "details": "Missing: " + ", ".join(missing) if missing else "Phase 0/4/5/6 manifests are present.",
        },
        {
            "id": "function_count_provenance",
            "status": "pass" if "code_total_functions" in derived else "attention",
            "details": "Function counts are sourced from the Phase 0 observed-count baseline."
            if "code_total_functions" in derived
            else "Phase 0 observed function counts are unavailable.",
        },
    ]


def _known_limitations(root: Path) -> list[str]:
    limitations = [
        "Baseline records current filesystem facts; it does not assign semantic meaning.",
    ]
    phase0 = _read_json_object(root / "Phases/Phase0/artifacts/phase0_baseline.json")
    if phase0 and isinstance(phase0.get("known_limitations"), list):
        limitations.extend(str(item) for item in phase0["known_limitations"])
    return list(dict.fromkeys(limitations))


def build_manifest(root: Path, generated_at_utc: str | None = None) -> dict[str, Any]:
    """Return one p0-a0.corpus-baseline.v1 manifest without writing input files."""

    records = scan_inputs(root)
    all_records = records["source_files"] + records["artifact_files"]
    derived = _derived_counts(root, records)
    return {
        "schema": SCHEMA,
        "generated_at_utc": generated_at_utc or datetime.now(timezone.utc).isoformat(),
        "workspace_policy": {
            "source_roots_read_only": True,
            "path_format": "workspace-relative-posix",
            "hash_algorithm": "sha256",
            "fingerprint_basis": "sorted(role, root_id, path, size_bytes, sha256)",
            "excluded_generated_roots": [EXCLUDED_GENERATED_ROOT],
        },
        "source_files": records["source_files"],
        "artifact_files": records["artifact_files"],
        "source_roots": [
            _root_summary(records["source_files"], root_id, relative_root)
            for root_id, relative_root in SOURCE_ROOTS.items()
        ],
        "artifact_inputs": [
            _artifact_input(root, record) for record in records["artifact_files"]
        ],
        "derived_counts": derived,
        "external_tools": _external_tools(root),
        "checks": _checks(root, records, derived),
        "known_limitations": _known_limitations(root),
        "snapshot_fingerprint": tree_fingerprint(all_records),
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Write JSON atomically without touching any input file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def write_report(path: Path, manifest: dict[str, Any]) -> None:
    """Write a concise Markdown summary derived solely from the manifest."""

    lines = [
        "# P0-A0 Corpus Baseline Report",
        "",
        f"- Schema: `{manifest['schema']}`",
        f"- Snapshot fingerprint: `{manifest['snapshot_fingerprint']}`",
        f"- Generated at UTC: `{manifest['generated_at_utc']}`",
        "",
        "## Source roots",
        "",
        "| Root | Files | Bytes | Lines | Tree SHA-256 | Status |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in manifest["source_roots"]:
        lines.append(
            f"| `{row['path']}` | {row['file_count']} | {row['total_bytes']} | "
            f"{row['total_lines']} | `{row['tree_sha256']}` | {row['status']} |"
        )
    lines.extend(["", "## Derived counts", ""])
    for key, value in sorted(manifest["derived_counts"].items()):
        lines.append(f"- `{key}`: `{value.get('value')}` ({value.get('basis')})")
    lines.extend(["", "## External tools", ""])
    for tool in manifest["external_tools"]:
        lines.append(f"- `{tool['id']}`: `{tool['status']}`")
    lines.extend(["", "## Checks", ""])
    for check in manifest["checks"]:
        lines.append(f"- `{check['id']}`: `{check['status']}` — {check['details']}")
    lines.extend(["", "## Known limitations", ""])
    lines.extend(f"- {item}" for item in manifest["known_limitations"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _resolve_cli_path(path: Path, workspace_root: Path) -> Path:
    return (workspace_root / path).resolve() if not path.is_absolute() else path.resolve()


def _validate_output_paths(workspace_root: Path, output_dir: Path, report_path: Path) -> str | None:
    corpus_root = (workspace_root / EXCLUDED_GENERATED_ROOT).resolve()
    docs_root = (workspace_root / "Phases/Phase4/docs").resolve()
    if not output_dir.is_relative_to(corpus_root):
        return f"Output directory must be under {EXCLUDED_GENERATED_ROOT}: {output_dir}"
    if not report_path.is_relative_to(docs_root):
        return f"Report path must be under Phases/Phase4/docs: {report_path}"
    for relative_root in SOURCE_ROOTS.values():
        source_root = (workspace_root / relative_root).resolve()
        if output_dir == source_root or output_dir.is_relative_to(source_root):
            return f"Output directory cannot be inside source root: {output_dir}"
        if report_path == source_root or report_path.is_relative_to(source_root):
            return f"Report path cannot be inside source root: {report_path}"
    return None


def compare_snapshot(root: Path, baseline: dict[str, Any]) -> dict[str, Any]:
    """Return pass or drift plus added, removed, changed and count-delta details."""

    current = scan_inputs(root)
    current_records = current["source_files"] + current["artifact_files"]
    baseline_records = baseline.get("source_files", []) + baseline.get("artifact_files", [])
    current_by_path = {row["path"]: row for row in current_records}
    baseline_by_path = {row["path"]: row for row in baseline_records}
    added = sorted(set(current_by_path) - set(baseline_by_path))
    removed = sorted(set(baseline_by_path) - set(current_by_path))
    changed = []
    for path in sorted(set(current_by_path) & set(baseline_by_path)):
        before = baseline_by_path[path]
        after = current_by_path[path]
        if (before.get("bytes"), before.get("sha256")) != (
            after.get("bytes"),
            after.get("sha256"),
        ):
            changed.append(
                {
                    "path": path,
                    "baseline": {"bytes": before.get("bytes"), "sha256": before.get("sha256")},
                    "current": {"bytes": after.get("bytes"), "sha256": after.get("sha256")},
                }
            )
    current_fingerprint = tree_fingerprint(current_records)
    baseline_fingerprint = baseline.get("snapshot_fingerprint")
    status = "pass" if not added and not removed and not changed and current_fingerprint == baseline_fingerprint else "drift"
    count_deltas = []
    for label, before_rows, after_rows in (
        ("source_files", baseline.get("source_files", []), current["source_files"]),
        ("artifact_files", baseline.get("artifact_files", []), current["artifact_files"]),
    ):
        if len(before_rows) != len(after_rows):
            count_deltas.append({"scope": label, "baseline": len(before_rows), "current": len(after_rows)})
    return {
        "status": status,
        "baseline_fingerprint": baseline_fingerprint,
        "current_fingerprint": current_fingerprint,
        "added": added,
        "removed": removed,
        "changed": changed,
        "count_deltas": count_deltas,
    }


def main(argv: list[str] | None = None) -> int:
    """Parse build/check arguments, write only declared outputs, and return the CLI code."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("Phases/Phase4/artifacts/corpus"))
    parser.add_argument("--report", type=Path, default=Path("Phases/Phase4/docs/corpus_baseline_report.md"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"Workspace root does not exist: {root}", file=sys.stderr)
        return 3
    output_dir = _resolve_cli_path(args.output, root)
    report_path = _resolve_cli_path(args.report, root)
    unsafe_output = _validate_output_paths(root, output_dir, report_path)
    if unsafe_output is not None:
        print(unsafe_output, file=sys.stderr)
        return 4
    if args.check:
        manifest_path = output_dir / "manifest.json"
        if not manifest_path.is_file():
            print(f"Baseline manifest is missing: {manifest_path}", file=sys.stderr)
            return 3
        try:
            baseline = json.loads(manifest_path.read_text(encoding="utf-8"))
            result = compare_snapshot(root, baseline)
        except (OSError, UnicodeError, json.JSONDecodeError, FileNotFoundError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 3
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "pass" else 2
    try:
        manifest = build_manifest(root)
        write_manifest(output_dir / "manifest.json", manifest)
        write_report(report_path, manifest)
    except (OSError, UnicodeError, FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 3
    print(
        json.dumps(
            {
                "status": "built",
                "manifest": (output_dir / "manifest.json").as_posix(),
                "report": report_path.as_posix(),
                "snapshot_fingerprint": manifest["snapshot_fingerprint"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
