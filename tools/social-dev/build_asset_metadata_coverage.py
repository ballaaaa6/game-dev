"""Build the AM-1 asset metadata coverage and orphan matrix.

This pass answers whether every current asset, selector, data-field relation,
and runtime manifest entry can be traced to an indexed/native identity. It
keeps "not referenced yet" separate from "missing" so gaps are visible
without inventing usage.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

BASELINE_PATH = EVIDENCE / "asset_metadata_baseline.json"
COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_metadata_coverage_contract.json"
ORPHAN_PATH = EVIDENCE / "asset_metadata_orphan_report.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_metadata_coverage.md"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.csv"
NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
NATIVE_REGISTRY_PATH = EVIDENCE / "native_content_registry.json"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def asset_id_for_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    return f"asset:{normalized}"


def maybe_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def load_asset_index() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    with ASSET_INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    rows = []
    for raw in raw_rows:
        path = raw["relative_path"].replace("\\", "/")
        rows.append(
            {
                "asset_id": asset_id_for_path(path),
                "relative_path": path,
                "kind": raw["kind"],
                "pack": raw["pack"] or "__ungrouped__",
                "original_name": raw["original_name"],
                "extension": raw["extension"],
                "size_bytes": maybe_int(raw["size"]),
                "width": maybe_int(raw["width"]),
                "height": maybe_int(raw["height"]),
                "format": raw["format"] or None,
                "has_alpha": None if raw["has_alpha"] == "" else raw["has_alpha"] == "True",
                "sha256": raw["sha256"].lower(),
                "apk_source_entry": raw["apk_source_entry"],
                "semantic_role": raw["semantic_role"],
            }
        )
    return rows, {row["asset_id"]: row for row in rows}


def canonical_asset_id(value: Any, *, asset_index: dict[str, Any], native_assets: dict[str, Any], asset_member: Any = None, source_asset_id: Any = None) -> str | None:
    candidates = []
    if isinstance(value, str) and value:
        normalized = value.replace("\\", "/")
        candidates.append(normalized)
        if normalized.startswith("asset:derived/"):
            candidates.append(asset_id_for_path(normalized[len("asset:derived/") :]))
        elif not normalized.startswith("asset:"):
            candidates.append(asset_id_for_path(normalized))
    if isinstance(asset_member, str) and asset_member:
        candidates.append(asset_id_for_path(asset_member))
    if isinstance(source_asset_id, str) and source_asset_id:
        normalized_source = source_asset_id.replace("\\", "/")
        candidates.append(normalized_source)
        if not normalized_source.startswith("asset:"):
            candidates.append(asset_id_for_path(normalized_source))
    for candidate in candidates:
        if candidate in asset_index or candidate in native_assets:
            return candidate
    return candidates[0] if candidates else None


def count_nested_asset_refs(value: Any) -> int:
    if isinstance(value, dict):
        return sum(
            (1 if key.endswith("asset_id") and value.get(key) else 0) + count_nested_asset_refs(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return sum(count_nested_asset_refs(item) for item in value)
    return 0


def load_runtime_entries(*, asset_index: dict[str, Any], native_assets: dict[str, Any]):
    entries = []
    refs_by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add_entries(path: Path, key: str, family: str, entry_kind: str) -> None:
        source = load_json(path)
        for index, item in enumerate(source.get(key, [])):
            raw_id = item.get("asset_id")
            provenance = item.get("provenance") or {}
            source_asset_id = item.get("source_asset_id") or provenance.get("source_asset_id")
            canonical = canonical_asset_id(
                raw_id,
                asset_index=asset_index,
                native_assets=native_assets,
                asset_member=item.get("asset_member"),
                source_asset_id=source_asset_id,
            )
            record = {
                "entry_id": f"{family}:{index}",
                "family": family,
                "entry_kind": entry_kind,
                "manifest_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "asset_id": raw_id,
                "canonical_asset_id": canonical,
                "source_asset_id": source_asset_id,
                "asset_member": item.get("asset_member"),
                "runtime_path": item.get("runtime_path"),
                "status": item.get("status") or item.get("runtime_status") or "manifest_entry",
                "source_status": item.get("source_status"),
                "semantic_role": item.get("semantic_role"),
                "selector_id": item.get("selector_id"),
            }
            entries.append(record)
            if canonical:
                refs_by_asset[canonical].append(
                    {
                        "entry_id": record["entry_id"],
                        "family": family,
                        "entry_kind": entry_kind,
                        "manifest_path": record["manifest_path"],
                        "status": record["status"],
                    }
                )

    add_entries(RUNTIME_EVIDENCE / "display_asset_manifest.json", "assets", "display_slice", "direct_asset")
    add_entries(RUNTIME_EVIDENCE / "room_scene_asset_manifest.json", "assets", "room_scene", "direct_asset")
    add_entries(RUNTIME_EVIDENCE / "character_asset_manifest.json", "images", "character", "image")
    add_entries(RUNTIME_EVIDENCE / "character_asset_manifest.json", "animations", "character", "animation")

    gate = load_json(EVIDENCE / "display_asset_gate.json")
    gate_entries = [
        {
            "entry_id": item.get("id") or f"display_gate:{index}",
            "kind": item.get("kind"),
            "status": item.get("status"),
            "asset_ref_count": count_nested_asset_refs(item),
        }
        for index, item in enumerate(gate.get("entries", []))
    ]
    return entries, dict(refs_by_asset), gate_entries


def build_data_field_inventory(registry: dict[str, Any], data_relations: list[dict[str, Any]], consumer_edges: list[dict[str, Any]]):
    relation_by_type_field: Counter[tuple[str, str]] = Counter()
    for relation in data_relations:
        source_id = relation.get("from", "")
        namespace = source_id.split(":", 2)[1] if source_id.startswith("data:") else "unknown"
        relation_by_type_field[(namespace, relation.get("field", ""))] += 1
    consumer_by_field: Counter[str] = Counter()
    for edge in consumer_edges:
        source = edge.get("from", "")
        if source.startswith("field:"):
            consumer_by_field[source[len("field:") :]] += 1

    rows = []
    for data_type in registry.get("data_types", []):
        namespace = data_type.get("native_namespace", "").removeprefix("data:")
        for field in data_type.get("fields", []):
            name = field.get("name")
            relation_count = relation_by_type_field[(namespace, name)]
            rows.append(
                {
                    "source_type": data_type.get("element_type"),
                    "native_namespace": data_type.get("native_namespace"),
                    "field": name,
                    "field_type": field.get("type"),
                    "selector_relation_count": relation_count,
                    "consumer_edge_count": consumer_by_field[name],
                    "asset_disposition": "selector_or_asset_reference" if relation_count else "no_direct_selector_relation_in_current_graph",
                    "semantic_status": "relation_present" if relation_count else "needs_semantic_classification",
                }
            )
    return sorted(rows, key=lambda item: (item["source_type"] or "", item["field"] or ""))


def build_payload() -> tuple[dict[str, Any], dict[str, Any]]:
    baseline = load_json(BASELINE_PATH)
    index_rows, asset_index = load_asset_index()
    catalog = load_json(NATIVE_CATALOG_PATH)
    registry = load_json(NATIVE_REGISTRY_PATH)
    native_assets = {item["asset_id"]: item for item in catalog["assets"]}
    selectors = catalog["selectors"]
    data_relations = registry["data_selector_relations"]
    consumer_edges = catalog["connections"]["consumer"]
    lifecycle_edges = catalog["connections"]["lifecycle"]
    selector_asset_relations = catalog["connections"]["selector_asset_and_companion"]
    runtime_entries, refs_by_asset, gate_entries = load_runtime_entries(asset_index=asset_index, native_assets=native_assets)

    relation_by_asset: Counter[str] = Counter()
    data_relation_by_asset: Counter[str] = Counter()
    selector_relation_by_asset: Counter[str] = Counter()
    for relation in selector_asset_relations:
        target = relation.get("target_asset_id")
        if target:
            relation_by_asset[target] += 1
            selector_relation_by_asset[target] += 1
    for relation in data_relations:
        target = relation.get("target_asset_id")
        if target:
            relation_by_asset[target] += 1
            data_relation_by_asset[target] += 1

    runtime_asset_ids = set(refs_by_asset)
    asset_rows = []
    asset_status_counts: Counter[str] = Counter()
    for row in index_rows:
        asset_id = row["asset_id"]
        native = native_assets.get(asset_id)
        relation_count = relation_by_asset[asset_id]
        runtime_refs = refs_by_asset.get(asset_id, [])
        if not native:
            status = "indexed_not_in_native_catalog"
        elif runtime_refs:
            status = "runtime_manifest_referenced"
        elif relation_count:
            status = "cataloged_with_native_relation"
        else:
            status = "cataloged_without_current_relation"
        asset_status_counts[status] += 1
        asset_rows.append(
            {
                **row,
                "native_catalog_present": native is not None,
                "native_source_status": native.get("source_status") if native else None,
                "archive_member_present": native.get("archive_member_present") if native else None,
                "native_kind": native.get("kind") if native else None,
                "selector_or_companion_relation_count": selector_relation_by_asset[asset_id],
                "data_selector_relation_count": data_relation_by_asset[asset_id],
                "native_relation_count": relation_count,
                "runtime_reference_count": len(runtime_refs),
                "runtime_families": sorted({item["family"] for item in runtime_refs}),
                "coverage_status": status,
                "semantic_status": "indexed_identity_closed" if native else "native_identity_gap",
                "geometry_status": "dimensions_indexed" if row["width"] is not None and row["height"] is not None else "dimensions_not_indexed",
            }
        )

    selector_rows = []
    selector_status_counts: Counter[str] = Counter()
    for selector in selectors:
        target = selector.get("target_asset_id")
        if selector.get("status") != "resolved":
            status = "unresolved_selector"
        elif not target or target not in asset_index:
            status = "resolved_target_missing_from_index"
        elif target in runtime_asset_ids:
            status = "resolved_target_runtime_referenced"
        else:
            status = "resolved_target_not_runtime_referenced"
        selector_status_counts[status] += 1
        selector_rows.append(
            {
                "selector_key": selector.get("selector_key"),
                "resource_scope": selector.get("resource_scope"),
                "selector_kind": selector.get("selector_kind"),
                "selector_id": selector.get("selector_id"),
                "source_file": selector.get("source_file"),
                "source_row": selector.get("source_row"),
                "raw_line": selector.get("raw_line"),
                "status": selector.get("status"),
                "resolution_mode": selector.get("resolution_mode"),
                "target_asset_id": target,
                "target_filename": selector.get("target_filename"),
                "target_present_in_index": bool(target and target in asset_index),
                "data_relation_count": sum(1 for item in data_relations if item.get("to") == selector.get("selector_key")),
                "coverage_status": status,
            }
        )

    data_field_rows = build_data_field_inventory(registry, data_relations, consumer_edges)
    data_relation_rows = []
    relation_status_counts: Counter[str] = Counter()
    for relation in data_relations:
        target = relation.get("target_asset_id")
        if relation.get("status") == "absent_by_sentinel":
            coverage_status = "explicit_absent_sentinel"
        elif relation.get("status") != "resolved":
            coverage_status = "selector_scope_unresolved"
        elif target in asset_index:
            coverage_status = "resolved_to_indexed_asset"
        else:
            coverage_status = "resolved_selector_without_index_asset"
        relation_status_counts[coverage_status] += 1
        data_relation_rows.append({**relation, "target_present_in_index": bool(target and target in asset_index), "coverage_status": coverage_status})

    consumer_rows = []
    relation_fields = {item["field"] for item in data_field_rows if item["selector_relation_count"]}
    for edge in consumer_edges:
        field = edge.get("from", "").removeprefix("field:")
        consumer_rows.append(
            {
                **edge,
                "field_asset_relation_status": "field_has_selector_relations" if field in relation_fields else "field_has_no_selector_relation_in_current_graph",
            }
        )

    orphan_report = {
        "schema_version": "social-dev-asset-metadata-orphan-report-v1",
        "status": "pass",
        "semantic_status": "coverage_gaps_explicit_not_runtime_approval",
        "baseline_content_hash": baseline["determinism"]["content_hash"],
        "summary": {
            "indexed_assets": len(index_rows),
            "native_assets": len(native_assets),
            "selectors": len(selectors),
            "data_selector_relations": len(data_relations),
            "data_fields": len(data_field_rows),
            "runtime_manifest_entries": len(runtime_entries),
            "assets_without_current_relation": sum(1 for row in asset_rows if row["coverage_status"] == "cataloged_without_current_relation"),
            "selectors_unresolved": sum(1 for row in selector_rows if row["coverage_status"] == "unresolved_selector"),
            "fields_needing_semantic_classification": sum(1 for row in data_field_rows if row["semantic_status"] == "needs_semantic_classification"),
            "relations_explicit_absent_sentinel": sum(1 for row in data_relation_rows if row["coverage_status"] == "explicit_absent_sentinel"),
            "relations_selector_scope_unresolved": sum(1 for row in data_relation_rows if row["coverage_status"] == "selector_scope_unresolved"),
        },
        "asset_gaps": {
            "indexed_not_in_native_catalog": [row["asset_id"] for row in asset_rows if row["coverage_status"] == "indexed_not_in_native_catalog"],
            "cataloged_without_current_relation": [row["asset_id"] for row in asset_rows if row["coverage_status"] == "cataloged_without_current_relation"],
        },
        "selector_gaps": {
            "unresolved": [
                {"selector_key": row["selector_key"], "resource_scope": row["resource_scope"], "selector_kind": row["selector_kind"], "raw_line": row["raw_line"], "source_file": row["source_file"]}
                for row in selector_rows if row["coverage_status"] == "unresolved_selector"
            ],
            "resolved_target_missing_from_index": [row["selector_key"] for row in selector_rows if row["coverage_status"] == "resolved_target_missing_from_index"],
        },
        "field_gaps": [
            {"source_type": row["source_type"], "field": row["field"], "field_type": row["field_type"], "consumer_edge_count": row["consumer_edge_count"]}
            for row in data_field_rows if row["semantic_status"] == "needs_semantic_classification"
        ],
        "runtime_reference_gaps": [item for item in runtime_entries if not item["canonical_asset_id"] or item["canonical_asset_id"] not in asset_index],
        "interpretation": {
            "cataloged_without_current_relation": "Not automatically an error; it can be a companion, source definition, localization, unused variant, or a family whose consumer relation is not yet modeled.",
            "fields_needing_semantic_classification": "Not automatically an asset reference; AM-3 must classify these as asset-bearing, data-only, control, relation, or intentionally non-visual.",
            "unresolved_selector": "A real identity gap that must remain explicit until an authoritative selector id/target is found or permanently marked source-limited.",
        },
    }
    orphan_report["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(orphan_report).encode("utf-8"))}

    payload = {
        "schema_version": "social-dev-asset-metadata-coverage-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "coverage_matrix_not_runtime_approval",
        "baseline_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_baseline.json", "content_hash": baseline["determinism"]["content_hash"]},
        "policy": {"source_roots_read_only": True, "missing_and_unreferenced_are_distinct": True, "runtime_promotion_is_not_inferred_from_index_presence": True},
        "counts": {
            "indexed_assets": len(index_rows),
            "native_assets": len(native_assets),
            "selectors": len(selectors),
            "data_selector_relations": len(data_relations),
            "data_fields": len(data_field_rows),
            "consumer_edges": len(consumer_edges),
            "lifecycle_edges": len(lifecycle_edges),
            "runtime_manifest_entries": len(runtime_entries),
            "display_gate_entries": len(gate_entries),
            "runtime_referenced_assets": len(runtime_asset_ids),
            "relations_explicit_absent_sentinel": sum(1 for row in data_relation_rows if row["coverage_status"] == "explicit_absent_sentinel"),
            "relations_selector_scope_unresolved": sum(1 for row in data_relation_rows if row["coverage_status"] == "selector_scope_unresolved"),
            "asset_statuses": dict(sorted(asset_status_counts.items())),
            "selector_coverage_statuses": dict(sorted(selector_status_counts.items())),
            "relation_coverage_statuses": dict(sorted(relation_status_counts.items())),
        },
        "assets": asset_rows,
        "selectors": selector_rows,
        "data_fields": data_field_rows,
        "data_selector_relations": data_relation_rows,
        "consumer_edges": consumer_rows,
        "runtime_manifest_entries": runtime_entries,
        "runtime_gate_entries": gate_entries,
        "orphan_report_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_orphan_report.json", "summary": orphan_report["summary"]},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload, orphan_report


def build_contract_payload(coverage: dict[str, Any], orphan_report: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-metadata-coverage-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "coverage_contract_not_runtime_approval",
        "coverage_path": "knowledge/fixtures/accepted/asset_metadata_coverage.json",
        "coverage_content_hash": coverage["determinism"]["content_hash"],
        "baseline_content_hash": coverage["baseline_ref"]["content_hash"],
        "counts": coverage["counts"],
        "orphan_summary": orphan_report["summary"],
        "runtime_policy": {"may_be_used_for_lookup": False, "may_be_used_to_promote_assets": False, "required_before_runtime_family_expansion": True, "next_gate": "asset_family_taxonomy_contract"},
        "acceptance": {
            "indexed_assets_are_traceable": coverage["counts"]["indexed_assets"] == coverage["counts"]["native_assets"],
            "all_resolved_data_relations_target_indexed_assets": coverage["counts"]["relation_coverage_statuses"].get("resolved_to_indexed_asset", 0) == coverage["counts"]["data_selector_relations"] - coverage["counts"].get("relations_explicit_absent_sentinel", 0) - coverage["counts"].get("relations_selector_scope_unresolved", 0),
            "unresolved_selector_count_is_explicit": True,
            "field_semantics_are_not_overclaimed": True,
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(coverage: dict[str, Any], orphan: dict[str, Any], contract: dict[str, Any]) -> str:
    counts = coverage["counts"]
    meanings = {
        "runtime_manifest_referenced": "Referenced by a runtime manifest; family semantics still have their own gates.",
        "cataloged_with_native_relation": "Present in the native catalog and reached by a relation, but not currently in a runtime manifest.",
        "cataloged_without_current_relation": "Indexed/native-present but not reached by the current graph; may be companion/unused/under-modeled.",
        "indexed_not_in_native_catalog": "Real identity mismatch requiring correction.",
    }
    lines = [
        "# Social Dev asset metadata coverage matrix",
        "",
        "AM-1 compares every indexed asset, native selector, data-selector relation, field inventory, and runtime manifest entry. Index presence is not treated as runtime approval.",
        "",
        "## Identity",
        "",
        f"- Coverage content hash: `{coverage['determinism']['content_hash']}`",
        f"- Baseline content hash: `{coverage['baseline_ref']['content_hash']}`",
        f"- Contract content hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Matrix counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Indexed assets | {counts['indexed_assets']:,} |",
        f"| Native catalog assets | {counts['native_assets']:,} |",
        f"| Selectors | {counts['selectors']:,} |",
        f"| Data-selector relations | {counts['data_selector_relations']:,} |",
        f"| Data fields | {counts['data_fields']:,} |",
        f"| Consumer edges | {counts['consumer_edges']:,} |",
        f"| Lifecycle edges | {counts['lifecycle_edges']:,} |",
        f"| Runtime manifest asset entries | {counts['runtime_manifest_entries']:,} |",
        f"| Display gate entries | {counts['display_gate_entries']:,} |",
        "",
        "## Asset coverage status",
        "",
        "| Status | Count | Meaning |",
        "|---|---:|---|",
    ]
    for status, count in counts["asset_statuses"].items():
        lines.append(f"| `{status}` | {count:,} | {meanings.get(status, 'Explicit coverage status.')} |")
    lines.extend(
        [
            "",
            "## Selector coverage",
            "",
            f"- Current selector statuses: `{counts['selector_coverage_statuses']}`.",
            f"- Unresolved selector records: **{len(orphan['selector_gaps']['unresolved']):,}**.",
            "- The unresolved selector remains explicit and is not replaced with a guessed id.",
            "",
            "## Data-field coverage",
            "",
            f"- Fields requiring semantic classification: **{orphan['summary']['fields_needing_semantic_classification']:,}**.",
            "- These fields are not automatically asset fields. AM-3 must classify them as selector-bearing, data-only, control, relation, or intentionally non-visual.",
            "",
            "## Runtime reference gaps",
            "",
            f"- Runtime manifest entries: **{counts['runtime_manifest_entries']:,}**.",
            f"- Entries without an index/native identity: **{len(orphan['runtime_reference_gaps']):,}**.",
            "- A manifest entry can use a derived runtime path; the matrix records both its raw manifest id and canonical source identity when available.",
            "",
            "## Orphan interpretation",
            "",
            "The orphan report is a work queue, not a deletion list. Unreferenced assets remain in evidence until a later family/consumer pass proves they are unused or classifies them as companion, localization, control, or runtime content.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_metadata_coverage.py",
            "python -B tools/social-dev/test_asset_metadata_coverage.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    coverage, orphan_report = build_payload()
    contract = build_contract_payload(coverage, orphan_report)
    write_json(COVERAGE_PATH, coverage)
    write_json(ORPHAN_PATH, orphan_report)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(coverage, orphan_report, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"coverage_content_hash": coverage["determinism"]["content_hash"], "indexed_assets": coverage["counts"]["indexed_assets"], "selectors": coverage["counts"]["selectors"], "data_fields": coverage["counts"]["data_fields"], "runtime_manifest_entries": coverage["counts"]["runtime_manifest_entries"], "runtime_reference_gaps": len(orphan_report["runtime_reference_gaps"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
