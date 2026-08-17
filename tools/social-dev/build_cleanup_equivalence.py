"""Check whether the C# update differs from raw evidence only by issue-marker lines."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
UPDATE = ROOT / "sources/raw/1_Click_CSharp_Code update"
OUTPUT = ROOT / "knowledge/fixtures/accepted/cleanup_equivalence.json"
REPORT = ROOT / "docs/reports/social-dev_cleanup_equivalence.md"
PREFIXES = ("data/", "game/", "game.routeSearch/", "main/")
MARKER_LINE = re.compile(r"^\s*Cpp2ILHelpers\.NoteDecompilerIssue\(.*\);\s*$\r?\n?", re.MULTILINE)


def canonical(relative: str, corpus: str) -> str:
    if corpus == "update" and relative.startswith("KairoEngine/"):
        return relative[len("KairoEngine/") :]
    return relative


def index(root: Path, corpus: str) -> dict[str, Path]:
    result = {}
    for path in root.rglob("*.cs"):
        relative = path.relative_to(root).as_posix()
        name = canonical(relative, corpus)
        if name.startswith(PREFIXES):
            result[name] = path
    return result


def normalized_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = MARKER_LINE.sub("", text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def main() -> int:
    raw = index(RAW, "raw")
    update = index(UPDATE, "update")
    rows = []
    counts = {"normalized_exact": 0, "normalized_different": 0, "exact": 0, "missing": 0}
    for name in sorted(set(raw) | set(update)):
        a = raw.get(name)
        b = update.get(name)
        if not a or not b:
            counts["missing"] += 1
            rows.append({"path": name, "status": "missing"})
            continue
        raw_hash = hashlib.sha256(a.read_bytes()).hexdigest().upper()
        update_hash = hashlib.sha256(b.read_bytes()).hexdigest().upper()
        if raw_hash == update_hash:
            counts["exact"] += 1
            status = "exact"
        elif normalized_hash(a) == normalized_hash(b):
            counts["normalized_exact"] += 1
            status = "marker_cleanup_only"
        else:
            counts["normalized_different"] += 1
            status = "content_change_beyond_markers"
        rows.append(
            {
                "path": name,
                "status": status,
                "raw_sha256": raw_hash,
                "update_sha256": update_hash,
                "raw_normalized_sha256": normalized_hash(a),
                "update_normalized_sha256": normalized_hash(b),
            }
        )
    payload = {
        "schema_version": "social-dev-cleanup-equivalence-v1",
        "scope": list(PREFIXES),
        "policy": "Marker normalization is a diagnostic only; it does not make decompiled C# executable.",
        "counts": counts,
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Social Dev C# cleanup equivalence",
        "",
        "This pass removes only standalone `Cpp2ILHelpers.NoteDecompilerIssue(...)` lines in memory, then compares hashes. It never changes source files.",
        "",
        "| Result | Files | Meaning |",
        "|---|---:|---|",
        f"| exact | {counts['exact']} | raw/update bytes already equal |",
        f"| marker cleanup only | {counts['normalized_exact']} | equal after removing marker lines |",
        f"| content change beyond markers | {counts['normalized_different']} | requires semantic review |",
        f"| missing | {counts['missing']} | not comparable in both corpora |",
        "",
        "## Gate",
        "",
        "If all candidate files are exact or marker-cleanup-only, the update is a cleaner evidence presentation rather than a new semantic implementation. The raw baseline remains the provenance anchor.",
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
