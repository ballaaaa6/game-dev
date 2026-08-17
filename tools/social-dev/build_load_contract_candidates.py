"""Extract Load(StringArrayStream) reader sequences beside xls row shapes."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "knowledge/fixtures/accepted/data_schema_candidate.json"
CROSSCHECK = ROOT / "knowledge/fixtures/accepted/data_text_crosscheck.json"
OUTPUT = ROOT / "knowledge/fixtures/accepted/load_contract_candidates.json"
REPORT = ROOT / "docs/reports/social-dev_load_contract_candidates.md"
CALL_RE = re.compile(r"\bsas\.(Get[A-Za-z_][A-Za-z0-9_]*)\s*\(")


def method_body(source: str, marker: str) -> str | None:
    start = source.find(marker)
    if start < 0:
        return None
    brace = source.find("{", start)
    if brace < 0:
        return None
    depth = 0
    for index in range(brace, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1 : index]
    return None


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    crosscheck = json.loads(CROSSCHECK.read_text(encoding="utf-8"))
    types = {item["symbol"]: item for item in schema["data_types"]}
    tables = {item["registry_field"]: item for item in crosscheck["records"]}
    rows = []
    statuses = Counter()
    for registry in schema["data_manager_registry"]:
        element_type = registry["type"].removesuffix("[]")
        type_record = types.get(element_type)
        source_path = ROOT / type_record["source"]["file"] if type_record else None
        source = source_path.read_text(encoding="utf-8", errors="replace") if source_path and source_path.is_file() else ""
        body = method_body(source, "public override void Load(StringArrayStream sas)")
        calls = CALL_RE.findall(body or "")
        table = tables.get(registry["name"], {})
        english = table.get("languages", {}).get("English.lproj", {})
        table_path = Path(english["path"]) if english.get("path") else None
        column_counts = Counter()
        row_count = 0
        if table_path and table_path.is_file():
            for line in table_path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                if line.strip():
                    row_count += 1
                    column_counts[len(line.split("\t"))] += 1
        if body is None:
            status = "load_method_missing"
        elif not table_path or not table_path.is_file():
            status = "table_missing"
        else:
            status = "candidate"
        statuses[status] += 1
        rows.append(
            {
                "registry_field": registry["name"],
                "element_type": element_type,
                "source_file": type_record["source"]["file"] if type_record else None,
                "load_method_status": "present" if body is not None else "missing",
                "reader_sequence": calls,
                "reader_call_count": len(calls),
                "english_table": str(table_path) if table_path else None,
                "english_row_count": row_count,
                "english_column_count_distribution": dict(sorted(column_counts.items())),
                "status": status,
                "semantic_status": "unknown",
            }
        )

    payload = {
        "schema_version": "social-dev-load-contract-candidates-v1",
        "source_schema_fingerprint": schema["source_inventory_fingerprint"],
        "policy": "Reader sequence and row shape are evidence candidates; they do not yet define semantic columns.",
        "status_counts": dict(sorted(statuses.items())),
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev Load contract candidates",
        "",
        "This report pairs each DataManager registry entry with the C# `Load(StringArrayStream)` reader sequence and English table row shape. It does not label columns.",
        "",
        "| Status | Files |",
        "|---|---:|",
    ]
    for status, count in payload["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "| Registry | Type | Reader calls | English rows | Column counts |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['registry_field']}` | `{row['element_type']}` | {row['reader_call_count']} | {row['english_row_count']} | `{row['english_column_count_distribution']}` |"
        )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "Column meanings remain unknown until the loader sequence, table bytes, language variants, and assembly-guide rules are reconciled. These candidates are not runtime data yet.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload["status_counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
