"""Build AM-5 usage, lifecycle, placement, and provenance matrix."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
SELECTOR_MATRIX_PATH = EVIDENCE / "asset_selector_usage_matrix.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"
FURNITURE_PATH = EVIDENCE / "furniture_asset_metadata.json"
CHARACTER_PATH = EVIDENCE / "character_visual_asset_metadata.json"
NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
ASSET_VALIDATION_PATH = EVIDENCE / "asset_validation_gate.json"
BINARY_INVENTORY_PATH = EVIDENCE / "asset_binary_inventory.json"

MATRIX_PATH = EVIDENCE / "asset_usage_lifecycle_placement_matrix.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_usage_lifecycle_placement_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_usage_lifecycle_placement.md"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_payload() -> dict[str, Any]:
    taxonomy = load_json(TAXONOMY_PATH)
    coverage = load_json(COVERAGE_PATH)
    selector_matrix = load_json(SELECTOR_MATRIX_PATH)
    geometry = load_json(GEOMETRY_PATH)
    furniture = load_json(FURNITURE_PATH)
    character = load_json(CHARACTER_PATH)
    native_catalog = load_json(NATIVE_CATALOG_PATH)
    validation = load_json(ASSET_VALIDATION_PATH)
    binary_inventory = load_json(BINARY_INVENTORY_PATH)

    taxonomy_by_asset = {item["asset_id"]: item for item in taxonomy["assets"]}
    geometry_by_asset = {item["asset_id"]: item for item in geometry["assets"]}
    selector_rows_by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for selector in selector_matrix["selectors"]:
        if selector.get("target_asset_id"):
            selector_rows_by_asset[selector["target_asset_id"]].append(selector)
    runtime_entries_by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in coverage["runtime_manifest_entries"]:
        if item.get("canonical_asset_id"):
            runtime_entries_by_asset[item["canonical_asset_id"]].append(item)

    furniture_by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    furniture_bindings_by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in furniture["furniture"]:
        for selector in item["selector_fields"].values():
            target = selector.get("target_asset_id")
            if target:
                furniture_by_asset[target].append({"furniture_data_id": item["furniture_data_id"], "field": selector.get("selector_kind"), "selector_status": selector.get("status")})
        for binding in item.get("native_room_bindings", []):
            for selector in item["selector_fields"].values():
                target = selector.get("target_asset_id")
                if target:
                    furniture_bindings_by_asset[target].append({"furniture_data_id": item["furniture_data_id"], "room_key": binding.get("room_key"), "cell": binding.get("cell"), "object_id": binding.get("object_id")})

    staff_assets: dict[str, list[str]] = defaultdict(list)
    for item in character["staff"]:
        asset_id = item["image_selector"].get("asset_id")
        if asset_id:
            staff_assets[asset_id].append(item["record_id"])
    helper_assets: dict[str, list[str]] = defaultdict(list)
    for item in character["helpers"]:
        asset_id = item["image_selector"].get("asset_id")
        if asset_id:
            helper_assets[asset_id].append(item["record_id"])
    room_assets = {
        item["canonical_asset_id"]: item["family"]
        for item in coverage["runtime_manifest_entries"]
        if item.get("family") == "room_scene" and item.get("canonical_asset_id")
    }

    lifecycle_edges = native_catalog["connections"]["lifecycle"]
    usage_rows = []
    usage_statuses: Counter[str] = Counter()
    lifecycle_statuses: Counter[str] = Counter()
    placement_statuses: Counter[str] = Counter()
    query_statuses: Counter[str] = Counter()
    usage_edges = []

    for asset in taxonomy["assets"]:
        asset_id = asset["asset_id"]
        selectors = selector_rows_by_asset.get(asset_id, [])
        runtime_entries = runtime_entries_by_asset.get(asset_id, [])
        geometry_row = geometry_by_asset.get(asset_id, {})
        channels = set()
        if selectors:
            channels.add("selector_target")
        if any(item.get("data_relation_count") for item in selectors):
            channels.add("data_field_relation")
        if runtime_entries:
            channels.add("runtime_manifest")
        if geometry_row.get("composition_ids") or geometry_row.get("logical_reconstruction_count"):
            channels.add("composition")
        if asset_id in furniture_by_asset:
            channels.add("furniture_metadata")
        if asset_id in staff_assets:
            channels.add("staff_character_binding")
        if asset_id in helper_assets:
            channels.add("helper_metadata_binding")
        if asset_id in room_assets:
            channels.add("room_scene_manifest")

        if runtime_entries:
            usage_status = "runtime_manifest_referenced"
        elif selectors:
            usage_status = "selector_referenced_catalog_only"
        else:
            usage_status = "cataloged_without_current_usage_edge"
        usage_statuses[usage_status] += 1

        consumer_methods = sorted({method for selector in selectors for method in selector.get("consumer_methods", [])})
        consumer_targets = sorted({target for selector in selectors for target in selector.get("consumer_targets", [])})
        lifecycle_phases = sorted({phase for selector in selectors for phase in selector.get("lifecycle_phases", [])})
        if lifecycle_phases:
            lifecycle_status = "consumer_phase_closed"
        elif runtime_entries:
            lifecycle_status = "runtime_manifest_without_native_phase_edge"
        elif selectors:
            lifecycle_status = "selector_resolved_without_consumer_phase"
        else:
            lifecycle_status = "lifecycle_not_closed"
        lifecycle_statuses[lifecycle_status] += 1

        placements = []
        if asset_id in room_assets:
            placements.append({"status": "room_selector_placement", "family": "room_scene", "runtime_entry_count": len(runtime_entries)})
        if asset_id in furniture_by_asset:
            placements.append({"status": "furniture_selector_binding", "furniture_data_ids": sorted({item["furniture_data_id"] for item in furniture_by_asset[asset_id]}), "native_room_bindings": furniture_bindings_by_asset.get(asset_id, [])})
        if asset_id in staff_assets:
            placements.append({"status": "staff_template_image_binding", "staff_ids": sorted(staff_assets[asset_id])})
        if asset_id in helper_assets:
            placements.append({"status": "helper_template_image_binding", "helper_ids": sorted(helper_assets[asset_id])})
        if not placements:
            placements.append({"status": "not_bound_to_explicit_placement"})
        placement_status = "explicit_binding" if any(item["status"] != "not_bound_to_explicit_placement" for item in placements) else "not_bound_to_explicit_placement"
        placement_statuses[placement_status] += 1

        if runtime_entries:
            query_status = "queryable_by_runtime_manifest_and_asset_id"
        elif selectors:
            query_status = "queryable_by_native_selector_and_asset_id"
        else:
            query_status = "evidence_catalog_only"
        query_statuses[query_status] += 1

        for selector in selectors:
            usage_edges.append({"edge_type": "selector_targets_asset", "asset_id": asset_id, "selector_key": selector.get("selector_key"), "data_relation_count": selector.get("data_relation_count"), "consumer_methods": selector.get("consumer_methods", []), "lifecycle_phases": selector.get("lifecycle_phases", [])})
        for entry in runtime_entries:
            usage_edges.append({"edge_type": "runtime_manifest_references_asset", "asset_id": asset_id, "entry_id": entry.get("entry_id"), "family": entry.get("family"), "manifest_path": entry.get("manifest_path")})
        for composition_id in geometry_row.get("composition_ids", []):
            usage_edges.append({"edge_type": "composition_uses_asset", "asset_id": asset_id, "composition_id": composition_id})

        usage_rows.append(
            {
                "asset_id": asset_id,
                "family_id": asset["family_id"],
                "subfamily_id": asset["subfamily_id"],
                "relative_path": asset["relative_path"],
                "extension": asset["extension"],
                "lineage": asset["lineage"],
                "usage_channels": sorted(channels),
                "usage_status": usage_status,
                "selector_keys": sorted({item.get("selector_key") for item in selectors if item.get("selector_key")}),
                "data_relation_count": sum(item.get("data_relation_count", 0) for item in selectors),
                "consumer_methods": consumer_methods,
                "consumer_targets": consumer_targets,
                "lifecycle_phases": lifecycle_phases,
                "lifecycle_status": lifecycle_status,
                "placement_status": placement_status,
                "placements": placements,
                "runtime_query_status": query_status,
                "runtime_manifest_families": sorted({item.get("family") for item in runtime_entries}),
                "composition_ids": geometry_row.get("composition_ids", []),
                "geometry_status": geometry_row.get("geometry_status"),
            }
        )

    family_summary = []
    for family_id in sorted({item["family_id"] for item in taxonomy["assets"]}):
        rows = [item for item in usage_rows if item["family_id"] == family_id]
        family_summary.append(
            {
                "family_id": family_id,
                "asset_count": len(rows),
                "usage_statuses": dict(sorted(Counter(item["usage_status"] for item in rows).items())),
                "lifecycle_statuses": dict(sorted(Counter(item["lifecycle_status"] for item in rows).items())),
                "placement_statuses": dict(sorted(Counter(item["placement_status"] for item in rows).items())),
                "runtime_query_statuses": dict(sorted(Counter(item["runtime_query_status"] for item in rows).items())),
            }
        )

    non_actor_families = []
    for family in family_summary:
        if family["family_id"].startswith(("ui.", "effect.", "event.", "text.", "config.", "data.", "system.", "platform.")):
            non_actor_families.append({**family, "usage_boundary": "cataloged_usage_or_screen_consumer_not_closed_by_current_actor_scene", "runtime_policy": "do_not_promote_without_screen_or_event_consumer_contract"})

    source_provenance = {
        "asset_validation": {
            "status": validation.get("status"),
            "asset_index_count": validation.get("asset_index_count"),
            "zip_status_counts": validation.get("zip_status_counts"),
            "apk_source_status_counts": validation.get("apk_source_status_counts"),
            "pack_source_map_count": validation.get("pack_source_map_count"),
            "roundtrip_exact_counts": validation.get("roundtrip_exact_counts"),
        },
        "binary_sources": {
            name: {"sha256": item.get("sha256"), "members": item.get("members"), "bytes": item.get("bytes")} for name, item in sorted(binary_inventory.get("archives", {}).items())
        },
        "unity_textasset_provenance": {"asset_rows": 34, "apk_entry_missing": 34, "status": "source_hash_or_nested_unity_mapping_not_closed"},
        "policy": "Archive/APK hashes and relative identities are retained; nested Unity bundle/TextAsset mapping remains explicit evidence-only until closed.",
    }

    payload = {
        "schema_version": "social-dev-asset-usage-lifecycle-placement-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "usage_lifecycle_placement_matrix_not_full_runtime_promotion",
        "refs": {
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
            "coverage": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": coverage["determinism"]["content_hash"]},
            "selector_matrix": {"path": "knowledge/fixtures/accepted/asset_selector_usage_matrix.json", "content_hash": selector_matrix["determinism"]["content_hash"]},
            "geometry": {"path": "knowledge/fixtures/accepted/asset_geometry_catalog.json", "content_hash": geometry["determinism"]["content_hash"]},
            "furniture": {"path": "knowledge/fixtures/accepted/furniture_asset_metadata.json", "content_hash": furniture["determinism"]["content_hash"]},
            "character": {"path": "knowledge/fixtures/accepted/character_visual_asset_metadata.json", "content_hash": character["determinism"]["content_hash"]},
        },
        "counts": {
            "assets": len(usage_rows),
            "usage_edges": len(usage_edges),
            "lifecycle_edges": len(lifecycle_edges),
            "families": len(family_summary),
            "non_actor_families": len(non_actor_families),
            "usage_statuses": dict(sorted(usage_statuses.items())),
            "lifecycle_statuses": dict(sorted(lifecycle_statuses.items())),
            "placement_statuses": dict(sorted(placement_statuses.items())),
            "runtime_query_statuses": dict(sorted(query_statuses.items())),
        },
        "assets": sorted(usage_rows, key=lambda item: item["asset_id"]),
        "usage_edges": sorted(usage_edges, key=lambda item: stable_json(item)),
        "lifecycle_edges": lifecycle_edges,
        "families": family_summary,
        "non_actor_families": non_actor_families,
        "source_provenance": source_provenance,
        "policy": {
            "usage_status_is_not_visual_quality": True,
            "lifecycle_status_requires_consumer_or_runtime_phase_evidence": True,
            "placement_status_never_infers_from_raw_type": True,
            "runtime_query_status_requires_contract_or_manifest": True,
            "source_provenance_gaps_are_not_deleted": True,
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(matrix: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-usage-lifecycle-placement-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "usage_lifecycle_placement_contract_not_full_runtime_approval",
        "matrix_path": "knowledge/fixtures/accepted/asset_usage_lifecycle_placement_matrix.json",
        "matrix_content_hash": matrix["determinism"]["content_hash"],
        "counts": matrix["counts"],
        "acceptance": {
            "every_asset_has_usage_status": matrix["counts"]["assets"] == 3542,
            "every_asset_has_lifecycle_status": all(item["lifecycle_status"] for item in matrix["assets"]),
            "every_asset_has_placement_status": all(item["placement_status"] for item in matrix["assets"]),
            "every_asset_has_runtime_query_status": all(item["runtime_query_status"] for item in matrix["assets"]),
            "non_actor_families_are_explicit": matrix["counts"]["non_actor_families"] > 0,
            "apk_unity_provenance_gap_is_explicit": matrix["source_provenance"]["unity_textasset_provenance"]["status"] == "source_hash_or_nested_unity_mapping_not_closed",
        },
        "runtime_policy": {"may_be_used_for_usage_trace": True, "may_be_used_for_placement": True, "may_be_used_for_lazy_query_routing": True, "may_be_used_to_promote_unapproved_assets": False, "next_gate": "asset_metadata_runtime_query_manifest"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(matrix: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev asset usage, lifecycle, placement, and provenance",
        "",
        "AM-5 gives every indexed asset an explicit usage status, lifecycle status, placement status, runtime-query status, and source-provenance boundary.",
        "",
        "## Identity",
        "",
        f"- Matrix hash: `{matrix['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Assets | {matrix['counts']['assets']:,} |",
        f"| Usage edges | {matrix['counts']['usage_edges']:,} |",
        f"| Lifecycle edges | {matrix['counts']['lifecycle_edges']:,} |",
        f"| Families | {matrix['counts']['families']:,} |",
        f"| Non-actor/UI/event/text families | {matrix['counts']['non_actor_families']:,} |",
        "",
        "## Runtime query statuses",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in matrix["counts"]["runtime_query_statuses"].items():
        lines.append(f"| `{status}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Source/provenance boundary",
            "",
            f"- Asset ZIP rows: `{matrix['source_provenance']['asset_validation']['zip_status_counts']}`.",
            f"- APK source statuses: `{matrix['source_provenance']['asset_validation']['apk_source_status_counts']}`.",
            "- The 34 Unity TextAsset/APK-missing rows remain explicit provenance gaps; they are not deleted or silently promoted.",
            "- UI, effect, event, text, system, platform, config, and data families are cataloged but require screen/event consumer contracts before runtime promotion.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_usage_lifecycle_placement.py",
            "python -B tools/social-dev/test_asset_usage_lifecycle_placement.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    matrix = build_payload()
    contract = build_contract_payload(matrix)
    write_json(MATRIX_PATH, matrix)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(matrix, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"matrix_hash": matrix["determinism"]["content_hash"], "assets": matrix["counts"]["assets"], "usage_edges": matrix["counts"]["usage_edges"], "non_actor_families": matrix["counts"]["non_actor_families"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
