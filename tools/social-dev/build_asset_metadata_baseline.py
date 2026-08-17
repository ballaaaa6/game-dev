"""Build a deterministic baseline for the Social Dev asset-metadata program.

The baseline is an evidence snapshot, not a runtime asset bundle.  It records
the authoritative input files, their hashes, the current catalog counts, and
the known closure exceptions so later coverage work can be compared without
guessing which version of an index or contract was used.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

BASELINE_PATH = EVIDENCE / "asset_metadata_baseline.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_metadata_baseline_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_metadata_baseline.md"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.csv"

INPUT_PATHS = [
    EVIDENCE / "asset_binary_inventory.json",
    ASSET_INDEX_PATH,
    EVIDENCE / "asset_selector_contract.json",
    EVIDENCE / "source_inventory.json",
    EVIDENCE / "object_catalog_fixture.json",
    EVIDENCE / "object_catalog_validation.json",
    EVIDENCE / "display_asset_gate.json",
    EVIDENCE / "phase3d_all_room_assembly_gate.json",
    EVIDENCE / "native_content_registry.json",
    EVIDENCE / "native_content_connection_graph.json",
    RUNTIME_EVIDENCE / "native_content_registry_contract.json",
    RUNTIME_EVIDENCE / "native_content_connection_contract.json",
    RUNTIME_EVIDENCE / "native_content_catalog.json",
    RUNTIME_EVIDENCE / "native_scene_assembly_contract.json",
    RUNTIME_EVIDENCE / "native_direction_contract.json",
    RUNTIME_EVIDENCE / "room_catalog_contract.json",
    RUNTIME_EVIDENCE / "room_scene_asset_manifest.json",
    RUNTIME_EVIDENCE / "room_scene_runtime_contract.json",
    RUNTIME_EVIDENCE / "default_map_chip_contract.json",
    RUNTIME_EVIDENCE / "character_metadata_contract.json",
    RUNTIME_EVIDENCE / "character_capability_contract.json",
    RUNTIME_EVIDENCE / "character_asset_manifest.json",
    RUNTIME_EVIDENCE / "display_asset_manifest.json",
    RUNTIME_EVIDENCE / "phase3d_all_room_assembly_gate_contract.json",
    RUNTIME_EVIDENCE / "pre_runtime_closure_contract.json",
]

EXPECTED_VERIFICATION_COMMANDS = [
    "python -B tools/social-dev/test_native_content_registry.py",
    "python -B tools/social-dev/test_native_content_catalog.py",
    "python -B tools/social-dev/test_character_metadata.py",
    "python -B tools/social-dev/test_character_capabilities.py",
    "python -B tools/social-dev/test_room_catalog.py",
    "python -B tools/social-dev/test_room_scene_asset_manifest.py",
    "python -B tools/social-dev/test_native_direction_contract.py",
    "python -B tools/social-dev/test_native_scene_assembly_contract.py",
    "python -B tools/social-dev/test_phase3d_all_room_assembly_gate.py",
    "python -B tools/social-dev/test_display_asset_gate.py",
]


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def input_manifest() -> dict[str, Any]:
    files = []
    for path in sorted(INPUT_PATHS, key=lambda item: relative_path(item)):
        require(path.is_file(), f"missing baseline input: {path}")
        files.append(
            {
                "path": relative_path(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return {
        "files": files,
        "input_hash": sha256_bytes(stable_json(files).encode("utf-8")),
    }


def summarize_asset_index() -> dict[str, Any]:
    with ASSET_INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(rows, "asset index is empty")

    def count(field: str, blank_key: str | None = None) -> dict[str, int]:
        values = []
        for row in rows:
            value = row.get(field, "") or (blank_key if blank_key is not None else "")
            values.append(value)
        return dict(sorted(Counter(values).items()))

    paths = [row["relative_path"] for row in rows]
    hashes = [row["sha256"] for row in rows]
    return {
        "row_count": len(rows),
        "unique_relative_paths": len(set(paths)),
        "duplicate_relative_paths": sorted(
            path for path, total in Counter(paths).items() if total > 1
        ),
        "rows_with_sha256": sum(bool(value) for value in hashes),
        "rows_with_dimensions": sum(bool(row["width"]) and bool(row["height"]) for row in rows),
        "by_kind": count("kind"),
        "by_pack": count("pack", blank_key="__ungrouped__"),
        "by_extension": count("extension"),
        "by_format": count("format", blank_key="__unknown__"),
    }


def summarize_binary_inventory() -> dict[str, Any]:
    source = load_json(EVIDENCE / "asset_binary_inventory.json")
    archives = {}
    for name, item in sorted(source["archives"].items()):
        archives[name] = {
            "bytes": item["bytes"],
            "members": item["members"],
            "total_uncompressed_bytes": item["total_uncompressed_bytes"],
            "sha256": item["sha256"],
            "top_level_groups": item["top_level_groups"],
            "index_summaries": item.get("index_summaries", {}),
        }
    return {
        "schema_version": source["schema_version"],
        "archives": archives,
    }


def summarize_native_catalog() -> dict[str, Any]:
    catalog = load_json(RUNTIME_EVIDENCE / "native_content_catalog.json")
    data_records = catalog["data_records"]
    selectors = catalog["selectors"]
    return {
        "status": catalog["status"],
        "semantic_status": catalog["semantic_status"],
        "schema_version": catalog["schema_version"],
        "catalog_id": catalog["catalog_id"],
        "counts": catalog["counts"],
        "data_record_status": dict(
            sorted(Counter(item.get("decoded", {}).get("status", "unknown") for item in data_records).items())
        ),
        "data_record_source_status": dict(
            sorted(Counter(item.get("source_status", "unknown") for item in data_records).items())
        ),
        "selector_status": dict(sorted(Counter(item.get("status", "unknown") for item in selectors).items())),
        "selector_resolution_mode": dict(
            sorted(
                Counter(item.get("resolution_mode") or "unknown" for item in selectors).items()
            )
        ),
        "unresolved_selector_samples": [
            {
                "selector_key": item.get("selector_key"),
                "raw_line": item.get("raw_line"),
                "source_file": item.get("source_file"),
            }
            for item in selectors
            if item.get("status") != "resolved"
        ][:10],
    }


def summarize_contracts() -> dict[str, Any]:
    paths = {
        "native_scene_assembly": RUNTIME_EVIDENCE / "native_scene_assembly_contract.json",
        "room_catalog": RUNTIME_EVIDENCE / "room_catalog_contract.json",
        "room_scene_assets": RUNTIME_EVIDENCE / "room_scene_asset_manifest.json",
        "room_scene_runtime": RUNTIME_EVIDENCE / "room_scene_runtime_contract.json",
        "character_metadata": RUNTIME_EVIDENCE / "character_metadata_contract.json",
        "character_capabilities": RUNTIME_EVIDENCE / "character_capability_contract.json",
        "display_assets": RUNTIME_EVIDENCE / "display_asset_manifest.json",
        "display_gate": EVIDENCE / "display_asset_gate.json",
        "all_room_gate": EVIDENCE / "phase3d_all_room_assembly_gate.json",
        "pre_runtime_closure": RUNTIME_EVIDENCE / "pre_runtime_closure_contract.json",
    }
    result = {}
    for name, path in paths.items():
        value = load_json(path)
        item = {
            "path": relative_path(path),
            "schema_version": value.get("schema_version"),
            "status": value.get("status"),
            "semantic_status": value.get("semantic_status"),
        }
        for key in ("counts", "runtime_readiness", "open_items", "determinism"):
            if key in value:
                item[key] = value[key]
        for key in ("rooms", "assets", "promoted_assets", "actors", "objects", "native_initial_objects"):
            if key in value and isinstance(value[key], list):
                item[f"{key}_count"] = len(value[key])
        result[name] = item
    return result


def summarize_relationships() -> dict[str, Any]:
    registry = load_json(EVIDENCE / "native_content_registry.json")
    graph = load_json(EVIDENCE / "native_content_connection_graph.json")
    return {
        "registry_status": registry.get("status"),
        "registry_semantic_status": registry.get("semantic_status"),
        "registry_counts": registry.get("counts"),
        "registry_identity_validation": registry.get("identity_validation"),
        "graph_counts": {
            name: len(items) if isinstance(items, list) else len(items)
            for name, items in graph.get("edges", {}).items()
        },
        "graph_content_hash": graph.get("content_hash"),
    }


def build_payload() -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-metadata-baseline-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "evidence_baseline_not_runtime_approval",
        "purpose": "Freeze the current asset, selector, data, composition, and runtime-contract counts before coverage closure work.",
        "policy": {
            "source_roots_read_only": True,
            "decompiled_csharp_executed": False,
            "baseline_promotes_assets": False,
            "runtime_approval_requires_family_composition_and_usage_validation": True,
        },
        "inputs": input_manifest(),
        "inventory": {
            "asset_index": summarize_asset_index(),
            "binary_sources": summarize_binary_inventory(),
        },
        "native_catalog": summarize_native_catalog(),
        "relationships": summarize_relationships(),
        "contracts": summarize_contracts(),
        "verification_commands": EXPECTED_VERIFICATION_COMMANDS,
        "known_exceptions": [
            {
                "id": "selector.unresolved.lineup_layout.bg_seb",
                "status": "open",
                "scope": "selector_resolution",
                "detail": "lineup_layout/seb.inf contains raw bg.seb without a resolved selector id/file target.",
            },
            {
                "id": "room.room0.floor_alias",
                "status": "explicit_runtime_alias",
                "scope": "room_floor_selection",
                "detail": "room:0 raw floorImgId_=5 resolves through FLOOR_IMAGE_ID_ARRAY to selector 23/floor_05.png; the runtime default alias for metadata remains separate.",
            },
            {
                "id": "native_catalog.data_records.not_mapped",
                "status": "coverage_gap",
                "scope": "data_field_semantics",
                "detail": "The native catalog retains all data rows, but rows outside the verified reader-order slices remain source-backed and not_mapped until field semantics are classified.",
            },
            {
                "id": "room.rooms_without_native_furniture_bindings",
                "status": "composition_gap",
                "scope": "room_furniture_placement",
                "detail": "Raw ObjChip topology is available for all rooms; explicit native FurnitureData instance bindings are currently closed only for the existing initial-object slice.",
            },
            {
                "id": "character.helper_image_resolution",
                "status": "partial",
                "scope": "helper_visuals",
                "detail": "Helper metadata is complete, while helper image usage is resolved for 7 records, deferred for 11, and absent for 1.",
            },
            {
                "id": "asset.runtime_promotion_scope",
                "status": "partial",
                "scope": "runtime_assets",
                "detail": "The full 3,542-row index is cataloged; runtime-approved display and room slices are smaller and must not be treated as full-family closure.",
            },
        ],
    }
    body_hash = sha256_bytes(stable_json(payload).encode("utf-8"))
    payload["determinism"] = {
        "algorithm": "stable-json-sha256 excluding determinism.content_hash",
        "content_hash": body_hash,
    }
    return payload


def build_contract_payload(baseline: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-metadata-baseline-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "baseline_contract_not_runtime_catalog",
        "baseline_path": "knowledge/fixtures/accepted/asset_metadata_baseline.json",
        "baseline_content_hash": baseline["determinism"]["content_hash"],
        "input_hash": baseline["inputs"]["input_hash"],
        "counts": {
            "indexed_assets": baseline["inventory"]["asset_index"]["row_count"],
            "native_data_rows": baseline["native_catalog"]["counts"]["data_records"],
            "native_selectors": baseline["native_catalog"]["counts"]["selectors"],
            "native_assets": baseline["native_catalog"]["counts"]["assets"],
            "native_data_selector_relations": baseline["native_catalog"]["counts"]["data_selector_connections"],
            "runtime_approved_display_assets": baseline["contracts"]["display_gate"]["promoted_assets_count"],
            "room_count": baseline["contracts"]["room_catalog"]["counts"]["rooms"],
            "staff_count": baseline["contracts"]["character_metadata"]["counts"]["staff_records"],
            "helper_count": baseline["contracts"]["character_metadata"]["counts"]["helper_records"],
            "furniture_count": baseline["native_catalog"]["counts"]["data_records"],
        },
        "runtime_policy": {
            "may_be_used_for_lookup": False,
            "may_be_used_to_promote_assets": False,
            "next_gate": "asset_metadata_coverage_contract",
        },
    }
    payload["determinism"] = {
        "algorithm": "stable-json-sha256 excluding determinism.content_hash",
        "content_hash": sha256_bytes(stable_json(payload).encode("utf-8")),
    }
    return payload


def markdown_report(baseline: dict[str, Any], contract: dict[str, Any]) -> str:
    index = baseline["inventory"]["asset_index"]
    native = baseline["native_catalog"]
    counts = native["counts"]
    exceptions = baseline["known_exceptions"]
    lines = [
        "# Social Dev asset metadata baseline",
        "",
        "This is the frozen AM-0 evidence baseline for the asset-metadata completion program. It is a reproducible snapshot, not a claim that every asset is runtime-ready.",
        "",
        "## Baseline identity",
        "",
        f"- Baseline content hash: `{baseline['determinism']['content_hash']}`",
        f"- Input manifest hash: `{baseline['inputs']['input_hash']}`",
        f"- Indexed asset rows: **{index['row_count']:,}** ({index['unique_relative_paths']:,} unique paths)",
        f"- Native catalog: **{counts['assets']:,} assets**, **{counts['selectors']:,} selectors**, **{counts['data_records']:,} data rows**",
        "",
        "## Current inventory",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Original packed assets | {index['by_kind'].get('original_pack_asset', 0):,} |",
        f"| Reconstructed/derived image rows | {sum(value for key, value in index['by_kind'].items() if key != 'original_pack_asset'): ,} |".replace(" ,", ","),
        f"| Named packs | {sum(1 for key in index['by_pack'] if key != '__ungrouped__')} |",
        f"| Ungrouped rows | {index['by_pack'].get('__ungrouped__', 0):,} |",
        f"| Rows with SHA-256 | {index['rows_with_sha256']:,} |",
        f"| Rows with dimensions | {index['rows_with_dimensions']:,} |",
        f"| Native data-selector relations | {counts['data_selector_connections']:,} |",
        f"| Selector/asset/companion relations | {counts['selector_asset_and_companion_connections']:,} |",
        "",
        "### Pack counts",
        "",
        "| Pack | Rows |",
        "|---|---:|",
    ]
    for pack, count in index["by_pack"].items():
        lines.append(f"| `{pack}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Resolution and readiness snapshot",
            "",
            "| Area | Current evidence |",
            "|---|---|",
            f"| Selector resolution | {native['selector_status']} |",
            f"| Data-row semantic status | {native['data_record_status']} |",
            f"| Staff metadata | {baseline['contracts']['character_metadata']['counts']['staff_records']:,} records; {baseline['contracts']['character_metadata']['counts']['unique_staff_image_selectors']:,} unique human image selectors |",
            f"| Helpers | {baseline['contracts']['character_metadata']['counts']['helper_records']:,} records; image resolution is partial |",
            f"| Rooms | {baseline['contracts']['room_catalog']['counts']['rooms']:,} rooms; {baseline['contracts']['room_catalog']['counts']['objchip_cells']:,} ObjChip cells |",
            f"| Furniture metadata | {counts['data_records']:,} total data rows in catalog; FurnitureData is a verified reader-order slice inside that catalog |",
            f"| Runtime display subset | {baseline['contracts']['display_gate']['promoted_assets_count']:,} promoted binary assets across {baseline['contracts']['display_gate']['counts']['entries']:,} approved entries |",
            "",
            "## Known exceptions carried into AM-1",
            "",
        ]
    )
    for item in exceptions:
        lines.append(f"- `{item['id']}` — **{item['status']}**: {item['detail']}")
    lines.extend(
        [
            "",
            "## Rebuild and verification",
            "",
            "The builder hashes every input by workspace-relative path and computes a stable content hash. If an upstream catalog changes, the baseline test fails until the snapshot is intentionally regenerated.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_metadata_baseline.py",
            "python -B tools/social-dev/test_asset_metadata_baseline.py",
            "```",
            "",
            "The ten pre-existing targeted contract tests are recorded in the JSON baseline and remain the minimum AM-0 verification set.",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    baseline = build_payload()
    contract = build_contract_payload(baseline)
    write_json(BASELINE_PATH, baseline)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(baseline, contract), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "baseline_content_hash": baseline["determinism"]["content_hash"],
                "input_hash": baseline["inputs"]["input_hash"],
                "indexed_assets": baseline["inventory"]["asset_index"]["row_count"],
                "native_assets": baseline["native_catalog"]["counts"]["assets"],
                "native_selectors": baseline["native_catalog"]["counts"]["selectors"],
                "native_data_rows": baseline["native_catalog"]["counts"]["data_records"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
