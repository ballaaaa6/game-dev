"""Cross-check DataManager registry names against extracted xls text tables."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "knowledge/fixtures/accepted/data_schema_candidate.json"
TEXT_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
OUTPUT = ROOT / "knowledge/fixtures/accepted/data_text_crosscheck.json"
REPORT = ROOT / "docs/reports/social-dev_data_text_crosscheck.md"


def file_info(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": str(path),
        "bytes": len(data),
        "lines": len(data.decode("utf-8-sig", errors="replace").splitlines()),
        "sha256": hashlib.sha256(data).hexdigest().upper(),
    }


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    registry = schema["data_manager_registry"]
    records = []
    mapped_stems = set()
    for item in registry:
        field_name = item["name"].rstrip("_")
        if field_name == "helpTexts":
            stem = "help"
        elif field_name.endswith("Data"):
            stem = field_name[:-4]
        else:
            stem = field_name
        mapped_stems.add(stem.casefold())
        languages = {}
        for language in ("English.lproj", "Japanese.lproj"):
            folder = TEXT_ROOT / language
            matches = [path for path in folder.glob("*.txt") if path.stem.casefold() == stem.casefold()]
            if matches:
                languages[language] = {"status": "matched_by_name", **file_info(matches[0])}
            else:
                languages[language] = {"status": "missing"}
        records.append(
            {
                "registry_field": item["name"],
                "element_type": item["type"],
                "expected_stem": stem,
                "languages": languages,
                "semantic_status": "unknown",
            }
        )

    extras = {}
    for language in ("English.lproj", "Japanese.lproj"):
        folder = TEXT_ROOT / language
        extras[language] = [
            file_info(path)
            for path in sorted(folder.glob("*.txt"))
            if path.stem.casefold() not in mapped_stems
        ]
    payload = {
        "schema_version": "social-dev-data-text-crosscheck-v1",
        "source_schema_fingerprint": schema["source_inventory_fingerprint"],
        "status": "evidence_crosscheck",
        "records": records,
        "extra_text_files": extras,
        "counts": {
            "registry_records": len(records),
            "english_matches": sum(record["languages"]["English.lproj"]["status"] == "matched_by_name" for record in records),
            "japanese_matches": sum(record["languages"]["Japanese.lproj"]["status"] == "matched_by_name" for record in records),
            "english_extras": len(extras["English.lproj"]),
            "japanese_extras": len(extras["Japanese.lproj"]),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev data text cross-check",
        "",
        "This pass checks the source-backed DataManager registry against the extracted English/Japanese xls text-table names. It does not assign column semantics.",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Registry records | {payload['counts']['registry_records']} |",
        f"| English name matches | {payload['counts']['english_matches']} |",
        f"| Japanese name matches | {payload['counts']['japanese_matches']} |",
        f"| English extra text files | {payload['counts']['english_extras']} |",
        f"| Japanese extra text files | {payload['counts']['japanese_extras']} |",
        "",
        "## Missing matches",
        "",
    ]
    missing = [
        record["registry_field"]
        for record in records
        if any(value["status"] == "missing" for value in record["languages"].values())
    ]
    lines.append("None." if not missing else "\n".join(f"- `{item}`" for item in missing))
    lines.extend(["", "## Extra text files", ""])
    for language, entries in extras.items():
        lines.append(f"### {language}")
        lines.extend(f"- `{Path(item['path']).name}`" for item in entries)
        if not entries:
            lines.append("- None")
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "Name coverage is a structural match only. Column order, row meaning, language fallback, and loader behavior still require cross-checking against each `Load(StringArrayStream)` method and the assembly guide.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
