"""Measure the Social Dev candidate C# slice without assigning semantics."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/social-dev"))
from build_source_inventory import comparable_path  # noqa: E402


RAW = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
UPDATE = ROOT / "sources/raw/1_Click_CSharp_Code update"
OUTPUT = ROOT / "knowledge/fixtures/accepted/candidate_diff.json"
REPORT = ROOT / "docs/reports/social-dev_candidate_diff.md"
PREFIXES = ("data/", "game/", "game.routeSearch/", "main/")
MARKER_RE = re.compile(r"Cpp2ILHelpers\.NoteDecompilerIssue")
IL_RE = re.compile(r"//\s*IL_[0-9A-Fa-f]+")
ARRAY_FIELD_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_<>.?]*\s*(?:\[\s*,?\s*\])\s+[A-Za-z_][A-Za-z0-9_]*\s*(?:=|;)")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def index(root: Path, corpus: str) -> dict[str, Path]:
    output = {}
    for path in sorted(root.rglob("*.cs")):
        relative = path.relative_to(root).as_posix()
        canonical = comparable_path(relative, corpus)
        if not canonical.startswith(PREFIXES):
            continue
        if canonical in output:
            raise RuntimeError(f"candidate path collision: {canonical}")
        output[canonical] = path
    return output


def metrics(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "lines": len(lines),
        "decompiler_issue_markers": len(MARKER_RE.findall(text)),
        "il_markers": len(IL_RE.findall(text)),
        "rough_array_field_lines": sum(1 for line in lines if ARRAY_FIELD_RE.search(line)),
    }


def main() -> int:
    raw = index(RAW, "raw")
    update = index(UPDATE, "update")
    rows = []
    statuses = Counter()
    for canonical in sorted(set(raw) | set(update)):
        raw_path = raw.get(canonical)
        update_path = update.get(canonical)
        raw_metrics = metrics(raw_path) if raw_path else None
        update_metrics = metrics(update_path) if update_path else None
        if raw_metrics and update_metrics:
            status = "exact_match" if raw_metrics["sha256"] == update_metrics["sha256"] else "modified"
        elif update_metrics:
            status = "update_only"
        else:
            status = "raw_only"
        statuses[status] += 1
        row = {
            "canonical_path": canonical,
            "status": status,
            "raw": raw_metrics,
            "update": update_metrics,
        }
        if raw_metrics and update_metrics:
            row["delta"] = {
                key: update_metrics[key] - raw_metrics[key]
                for key in (
                    "bytes",
                    "lines",
                    "decompiler_issue_markers",
                    "il_markers",
                    "rough_array_field_lines",
                )
            }
            row["marker_direction"] = (
                "reduced"
                if row["delta"]["decompiler_issue_markers"] < 0
                else "increased"
                if row["delta"]["decompiler_issue_markers"] > 0
                else "same"
            )
        rows.append(row)

    payload = {
        "schema_version": "social-dev-candidate-diff-v1",
        "raw_root": str(RAW),
        "update_root": str(UPDATE),
        "scope": list(PREFIXES),
        "status_counts": dict(sorted(statuses.items())),
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    modified = [row for row in rows if row["status"] == "modified"]
    marker_counts = Counter(row["marker_direction"] for row in modified)
    lines = [
        "# Social Dev candidate C# diff",
        "",
        "This report measures the gameplay/lifecycle slice only: `data`, `game`, `game.routeSearch`, and `main`. It does not promote semantics or treat a marker reduction as proof of correctness.",
        "",
        "## Result",
        "",
        "| Status | Files |",
        "|---|---:|",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Modified-file marker direction",
            "",
            "| Update marker direction | Files | Interpretation |",
            "|---|---:|---|",
            f"| reduced | {marker_counts.get('reduced', 0)} | possible cleanup; still needs semantic review |",
            f"| same | {marker_counts.get('same', 0)} | layout/content changed without marker-count change |",
            f"| increased | {marker_counts.get('increased', 0)} | possible added decompiler damage or expanded extraction |",
            "",
            "## Largest changed files by absolute byte delta",
            "",
            "| File | Bytes Δ | Lines Δ | Issue markers Δ | Array-field lines Δ |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in sorted(modified, key=lambda item: abs(item["delta"]["bytes"]), reverse=True)[:30]:
        delta = row["delta"]
        lines.append(
            f"| `{row['canonical_path']}` | {delta['bytes']:+,} | {delta['lines']:+,} | {delta['decompiler_issue_markers']:+,} | {delta['rough_array_field_lines']:+,} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The update corpus is not promoted wholesale. Only the candidate slice is measured here; form/UI splits and dependency rewrites remain separate evidence. A reduced decompiler-marker count is a review signal, not a correctness verdict.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status_counts": payload["status_counts"], "marker_direction": dict(marker_counts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
