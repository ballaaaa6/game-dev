"""Pair source field assignments with reader calls as bounded load candidates."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "knowledge/fixtures/accepted/csharp_inventory"
OUTPUT = ROOT / "knowledge/fixtures/accepted/field_load_candidates.json"
REPORT = ROOT / "docs/reports/social-dev_field_load_candidates.md"
CALL_RE = re.compile(r"\bsas\.(Get[A-Za-z_][A-Za-z0-9_]*)\s*\(")
ASSIGN_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*_\w*)\s*=")


def body_for_load(source: str) -> str | None:
    marker = "public override void Load(StringArrayStream sas)"
    start = source.find(marker)
    if start < 0:
        return None
    brace = source.find("{", start)
    if brace < 0:
        return None
    depth = 0
    for index in range(brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1 : index]
    return None


def main() -> int:
    types = json.loads((INVENTORY / "type_catalog.json").read_text(encoding="utf-8"))["records"]
    fields = json.loads((INVENTORY / "field_catalog.json").read_text(encoding="utf-8"))["records"]
    data_types = {
        record["symbol"]: record
        for record in types
        if "/data/" in record["source"]["file"]
        and "." not in record["symbol"]
        and record["kind"] == "class"
    }
    fields_by_owner: dict[str, set[str]] = {name: set() for name in data_types}
    for record in fields:
        if record["owner"] in fields_by_owner:
            fields_by_owner[record["owner"]].add(record["symbol"])
    # BaseData owns id_/flag_, and derived loaders assign those inherited
    # fields before their own fields. Include them in the bounded sequence.
    base_fields = {
        record["symbol"]
        for record in fields
        if record["owner"] == "BaseData" and record["symbol"] in {"id_", "flag_"}
    }
    for field_names in fields_by_owner.values():
        field_names.update(base_fields)

    rows = []
    counts = {"candidate": 0, "load_missing": 0, "count_mismatch": 0}
    for type_name, type_record in sorted(data_types.items()):
        source_path = ROOT / type_record["source"]["file"]
        source = source_path.read_text(encoding="utf-8", errors="replace")
        body = body_for_load(source)
        if body is None:
            counts["load_missing"] += 1
            rows.append({"type": type_name, "status": "load_missing", "source": type_record["source"]})
            continue
        readers = CALL_RE.findall(body)
        field_names = fields_by_owner[type_name]
        assignments = [name for name in ASSIGN_RE.findall(body) if name in field_names]
        status = "candidate" if len(readers) == len(assignments) else "count_mismatch"
        counts[status] += 1
        pairs = []
        for index in range(min(len(readers), len(assignments))):
            pairs.append(
                {
                    "order": index,
                    "field": assignments[index],
                    "reader": readers[index],
                    "semantic_status": "unknown",
                    "mapping_status": "order_candidate",
                }
            )
        rows.append(
            {
                "type": type_name,
                "source": type_record["source"],
                "reader_sequence": readers,
                "field_assignment_sequence": assignments,
                "pairs": pairs,
                "reader_count": len(readers),
                "field_assignment_count": len(assignments),
                "status": status,
            }
        )

    payload = {
        "schema_version": "social-dev-field-load-candidates-v1",
        "policy": "Order-based field/reader pairs are bounded candidates only; no semantic column names are promoted.",
        "counts": counts,
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Social Dev field/load candidates",
        "",
        "This pass pairs field assignments and `StringArrayStream` reader calls in each data class `Load` body by source order. A pair is not a semantic proof.",
        "",
        "| Result | Classes |",
        "|---|---:|",
        f"| candidate | {counts['candidate']} |",
        f"| count mismatch | {counts['count_mismatch']} |",
        f"| Load missing | {counts['load_missing']} |",
        "",
        "## Count mismatches",
        "",
    ]
    mismatches = [row for row in rows if row["status"] == "count_mismatch"]
    if mismatches:
        lines.append("| Type | Reader calls | Field assignments |")
        lines.append("|---|---:|---:|")
        for row in mismatches:
            lines.append(f"| `{row['type']}` | {row['reader_count']} | {row['field_assignment_count']} |")
    else:
        lines.append("None.")
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "Use this artifact to guide manual semantic review and to compare English/Japanese row shapes. Do not generate production models directly from positional pairs.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
