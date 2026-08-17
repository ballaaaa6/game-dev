"""Build a source-backed candidate registry for Social Dev static data."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "knowledge/fixtures/accepted/csharp_inventory"
OUTPUT = ROOT / "knowledge/fixtures/accepted/data_schema_candidate.json"
REPORT = ROOT / "docs/reports/social-dev_data_schema_candidate.md"
FIELD_RE = re.compile(
    r"(?P<type>[A-Za-z_][A-Za-z0-9_.]*(?:<[^;{}=]+>)?(?:\[\s*,?\s*\])*)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:=|;)"
)


def load(name: str) -> dict:
    return json.loads((INVENTORY / name).read_text(encoding="utf-8"))


def parse_field(record: dict) -> dict:
    declaration = record.get("raw_declaration", "")
    match = FIELD_RE.search(declaration)
    type_name = match.group("type") if match else None
    name = match.group("name") if match else record.get("symbol")
    return {
        "symbol": record.get("symbol"),
        "name": name,
        "type": type_name,
        "is_array": bool(type_name and "[" in type_name),
        "raw_declaration": declaration,
        "source": record.get("source"),
        "semantic_status": "unknown",
        "source_status": "raw_evidence",
    }


def main() -> int:
    manifest = load("inventory_manifest.json")
    types = load("type_catalog.json")["records"]
    fields = load("field_catalog.json")["records"]
    methods = load("method_catalog.json")["records"]

    data_types = [
        {
            "symbol": record["symbol"],
            "kind": record["kind"],
            "source": record["source"],
            "semantic_status": "unknown",
            "source_status": "raw_evidence",
        }
        for record in types
        if "/data/" in record["source"]["file"]
        and "." not in record["symbol"]
        and record["kind"] == "class"
    ]
    data_type_names = {record["symbol"] for record in data_types}

    data_fields = [parse_field(record) for record in fields if record["owner"] in data_type_names]
    data_manager_fields = [
        parse_field(record)
        for record in fields
        if record["owner"] == "DataManager" and "[]" in record.get("raw_declaration", "")
    ]
    lifecycle_names = {"Load", "NewGame", "Serialize", "Deserialize", "Deserialized"}
    lifecycle = [
        {
            "symbol": record["symbol"],
            "owner": record["owner"],
            "name": record["name"],
            "kind": record["kind"],
            "source": record["source"],
            "semantic_status": "unknown",
            "source_status": "raw_evidence",
        }
        for record in methods
        if record["owner"] in data_type_names | {"DataManager"}
        and record["name"] in lifecycle_names
    ]

    payload = {
        "schema_version": "social-dev-data-schema-candidate-v1",
        "source_inventory_fingerprint": manifest["content_fingerprint"],
        "status": "candidate_only",
        "policy": "Names and types are preserved from evidence; semantic meaning remains unknown until cross-source review.",
        "data_manager_registry": data_manager_fields,
        "data_types": data_types,
        "data_fields": data_fields,
        "lifecycle_hooks": lifecycle,
        "counts": {
            "registry_arrays": len(data_manager_fields),
            "data_types": len(data_types),
            "data_fields": len(data_fields),
            "lifecycle_hooks": len(lifecycle),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev data schema candidate",
        "",
        "This is a source-backed candidate, not an approved runtime schema. Field names/types are copied from the structural inventory; semantic meaning remains `unknown`.",
        "",
        f"Inventory fingerprint: `{manifest['content_fingerprint']}`",
        "",
        "## Counts",
        "",
        "| Item | Count |",
        "|---|---:|",
        f"| DataManager typed arrays | {len(data_manager_fields)} |",
        f"| Data record classes | {len(data_types)} |",
        f"| Data fields | {len(data_fields)} |",
        f"| Lifecycle hooks | {len(lifecycle)} |",
        "",
        "## DataManager registry",
        "",
        "| Field | Element type | Source | Semantic status |",
        "|---|---|---|---|",
    ]
    for record in data_manager_fields:
        lines.append(
            f"| `{record['name']}` | `{record['type']}` | `{record['source']['file']}:{record['source']['line_start']}` | `{record['semantic_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Promotion rule",
            "",
            "This registry is the first canonical boundary candidate. It must be reconciled with the update corpus, ZIP data/guide, and APK provenance before any data is copied into `runtime/social-dev`.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
