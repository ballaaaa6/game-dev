"""Build the runtime-facing native content catalog.

The evidence registry is intentionally not imported by the browser because it
contains the complete extraction graph and is large.  This catalog keeps the
same native identities, selector IDs, source hashes, decoded values, and
connection edges at the runtime boundary so later systems can query an object
without inventing a second ID space.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/native_content_catalog.json"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def build_payload() -> dict[str, Any]:
    registry = json.loads(SOURCE.read_text(encoding="utf-8"))
    data_types = registry["data_types"]

    data_records: list[dict[str, Any]] = []
    for data_type in data_types:
        for row in data_type.get("rows", []):
            decoded = row.get("decoded", {})
            locales = row.get("locales", {})
            data_records.append(
                {
                    "record_id": row["catalog_key"],
                    "native_id": row.get("native_id"),
                    "data_type": data_type["source_type"],
                    "native_namespace": data_type["native_namespace"],
                    "row_index": row.get("row_index"),
                    "id_status": row.get("id_status"),
                    "source_status": decoded.get("status", "not_mapped"),
                    "source_file": data_type.get("source_file"),
                    "source_type_sha256": data_type.get("source_sha256"),
                    "locale_rows": {
                        locale: {
                            "row": value.get("row"),
                            "raw_row_sha256": value.get("raw_row_sha256"),
                        }
                        for locale, value in sorted(locales.items())
                    },
                    "decoded": decoded,
                }
            )

    body: dict[str, Any] = {
        "schema_version": "social-dev-native-content-catalog-v1",
        "package": "social-dev-native-content-catalog",
        "status": "pass",
        "semantic_status": "approved_for_runtime_catalog",
        "catalog_id": "display-slice-01",
        "source_registry": {
            "path": "knowledge/fixtures/accepted/native_content_registry.json",
            "schema_version": registry["schema_version"],
            "content_hash": registry["content_hash"],
            "policy": "Native values and source statuses are preserved; this catalog does not rename unknown fields or infer visual placement.",
        },
        "data_types": [
            {
                "element_type": item["source_type"],
                "native_namespace": item["native_namespace"],
                "field": item["field"],
                "row_count": item["row_count"],
                "source_file": item["source_file"],
                "source_sha256": item["source_sha256"],
                "fields": item["fields"],
            }
            for item in data_types
        ],
        "data_records": data_records,
        "selectors": registry["selectors"],
        "assets": registry["assets"],
        "connections": {
            "data_selector": registry["data_selector_relations"],
            "selector_asset_and_companion": registry["relations"],
            "consumer": registry["consumer_graph"]["consumer_edges"],
            "lifecycle": registry["consumer_graph"]["lifecycle_edges"],
        },
        "identity_policy": {
            "data_record_id_format": "data:<native_namespace>:<native_id>",
            "selector_id_format": "ref:<resource_scope>:<selector_kind>:<selector_id>",
            "asset_id_format": "asset:<archive_relative_path>",
            "negative_selector_values_are_explicit_sentinels": True,
            "raw_types_are_not_asset_ids": True,
            "consumer_composition_is_required_before_draw": True,
        },
        "counts": {
            "data_manager_arrays": registry["counts"]["data_manager_arrays"],
            "data_types": registry["counts"]["data_types"],
            "data_records": len(data_records),
            "assets": len(registry["assets"]),
            "selectors": len(registry["selectors"]),
            "data_selector_connections": len(registry["data_selector_relations"]),
            "selector_asset_and_companion_connections": len(registry["relations"]),
            "consumer_connections": len(registry["consumer_graph"]["consumer_edges"]),
            "lifecycle_connections": len(registry["consumer_graph"]["lifecycle_edges"]),
        },
    }
    return {**body, "determinism": {"algorithm": "stable-json-sha256", "content_hash": content_hash(body)}}


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        "native_content_catalog_built "
        f"records={payload['counts']['data_records']} "
        f"assets={payload['counts']['assets']} "
        f"selectors={payload['counts']['selectors']}"
    )


if __name__ == "__main__":
    main()
