"""Build a provenance-only runtime/entity candidate from Social Dev C# evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "knowledge/fixtures/accepted/csharp_inventory"
OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime_schema_candidate.json"
REPORT = ROOT / "docs/reports/social-dev_runtime_schema_candidate.md"
KEY_TYPES = [
    "Player",
    "Staff",
    "Room",
    "Company",
    "GameRecord",
    "Develop",
    "Proposal",
    "Meeting",
    "ObjChip",
    "MapChip",
    "Avatar",
    "Camera",
    "Enemy",
    "Fan",
]
LIFECYCLE = {"NewGame", "Load", "Serialize", "Deserialize", "Deserialized", "Update", "Move"}
TYPE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def load(name: str) -> dict:
    return json.loads((INVENTORY / name).read_text(encoding="utf-8"))


def main() -> int:
    types = load("type_catalog.json")["records"]
    fields = load("field_catalog.json")["records"]
    methods = load("method_catalog.json")["records"]
    fields_by_owner = {name: [] for name in KEY_TYPES}
    methods_by_owner = {name: [] for name in KEY_TYPES}
    for field in fields:
        if field["owner"] in fields_by_owner:
            fields_by_owner[field["owner"]].append(field)
    for method in methods:
        if method["owner"] in methods_by_owner and method["name"] in LIFECYCLE:
            methods_by_owner[method["owner"]].append(method)

    records = []
    relation_candidates = []
    for name in KEY_TYPES:
        type_records = [record for record in types if record["symbol"] == name]
        owner_fields = fields_by_owner[name]
        field_records = []
        for field in owner_fields:
            raw = field.get("raw_declaration", "")
            tokens = set(TYPE_RE.findall(raw))
            mentions = sorted((tokens & set(KEY_TYPES)) - {name})
            field_records.append(
                {
                    "symbol": field["symbol"],
                    "raw_declaration": raw,
                    "source": field["source"],
                    "mentions_key_types": mentions,
                    "semantic_status": "unknown",
                    "source_status": "raw_evidence",
                }
            )
            for target in mentions:
                relation_candidates.append(
                    {
                        "owner": name,
                        "field": field["symbol"],
                        "target_type_token": target,
                        "source": field["source"],
                        "relation_status": "candidate_only",
                    }
                )
        records.append(
            {
                "type": name,
                "type_sources": [record["source"] for record in type_records],
                "fields": field_records,
                "lifecycle_hooks": [
                    {
                        "symbol": method["symbol"],
                        "name": method["name"],
                        "source": method["source"],
                        "semantic_status": "unknown",
                    }
                    for method in methods_by_owner[name]
                ],
                "semantic_status": "unknown",
                "source_status": "raw_evidence",
            }
        )

    payload = {
        "schema_version": "social-dev-runtime-schema-candidate-v1",
        "source_inventory_fingerprint": load("inventory_manifest.json")["content_fingerprint"],
        "status": "candidate_only",
        "policy": "Field relations are evidence-backed tokens only; no runtime semantics are promoted here.",
        "entities": records,
        "relation_candidates": relation_candidates,
        "counts": {
            "entities": len(records),
            "fields": sum(len(record["fields"]) for record in records),
            "lifecycle_hooks": sum(len(record["lifecycle_hooks"]) for record in records),
            "relation_candidates": len(relation_candidates),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev runtime/entity schema candidate",
        "",
        "This is a source-backed candidate boundary for runtime entities. It is not executable runtime code and does not assign meanings to numeric states.",
        "",
        f"Inventory fingerprint: `{payload['source_inventory_fingerprint']}`",
        "",
        "| Item | Count |",
        "|---|---:|",
        f"| Key entity types | {payload['counts']['entities']} |",
        f"| Fields | {payload['counts']['fields']} |",
        f"| Lifecycle hooks | {payload['counts']['lifecycle_hooks']} |",
        f"| Relation candidates | {payload['counts']['relation_candidates']} |",
        "",
        "## Entity boundary",
        "",
        "| Entity | Fields | Lifecycle hooks | Status |",
        "|---|---:|---:|---|",
    ]
    for record in records:
        lines.append(
            f"| `{record['type']}` | {len(record['fields'])} | {len(record['lifecycle_hooks'])} | `unknown` |"
        )
    lines.extend(
        [
            "",
            "## Promotion rule",
            "",
            "The next semantic pass must confirm serialization ownership, collection identity, and state transitions from C# plus APK/assembly evidence. This candidate must not be replaced with fields from a human-authored scaffold by assumption.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
