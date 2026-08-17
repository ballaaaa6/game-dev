"""Build the runtime-approved lazy asset metadata query manifest."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

USAGE_PATH = EVIDENCE / "asset_usage_lifecycle_placement_matrix.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
FURNITURE_PATH = EVIDENCE / "furniture_asset_metadata.json"
CHARACTER_PATH = EVIDENCE / "character_visual_asset_metadata.json"
NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
ROOM_MANIFEST_PATH = RUNTIME_EVIDENCE / "room_scene_asset_manifest.json"
DISPLAY_MANIFEST_PATH = RUNTIME_EVIDENCE / "display_asset_manifest.json"

MANIFEST_PATH = RUNTIME_EVIDENCE / "asset_metadata_runtime_manifest.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_metadata_runtime_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_metadata_runtime_manifest.md"


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
    usage = load_json(USAGE_PATH)
    geometry = load_json(GEOMETRY_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    furniture = load_json(FURNITURE_PATH)
    character = load_json(CHARACTER_PATH)
    native_catalog = load_json(NATIVE_CATALOG_PATH)
    room_manifest = load_json(ROOM_MANIFEST_PATH)
    display_manifest = load_json(DISPLAY_MANIFEST_PATH)
    geometry_by_asset = {item["asset_id"]: item for item in geometry["assets"]}
    taxonomy_by_asset = {item["asset_id"]: item for item in taxonomy["assets"]}

    runtime_assets = []
    for item in usage["assets"]:
        if item["runtime_query_status"] != "queryable_by_runtime_manifest_and_asset_id":
            continue
        geo = geometry_by_asset.get(item["asset_id"], {})
        tax = taxonomy_by_asset[item["asset_id"]]
        runtime_assets.append(
            {
                "asset_id": item["asset_id"],
                "relative_path": item["relative_path"],
                "family_id": item["family_id"],
                "subfamily_id": item["subfamily_id"],
                "lineage": item["lineage"],
                "runtime_manifest_families": item["runtime_manifest_families"],
                "usage_status": item["usage_status"],
                "lifecycle_status": item["lifecycle_status"],
                "placement_status": item["placement_status"],
                "composition_ids": geo.get("composition_ids", []),
                "geometry_status": geo.get("geometry_status"),
                "physical_dimensions": geo.get("physical_dimensions", []),
                "runtime_reference_count": item["runtime_manifest_families"].count("display_slice") + item["runtime_manifest_families"].count("room_scene") + item["runtime_manifest_families"].count("character"),
                "runtime_policy": "lazy_by_asset_id",
            }
        )

    # Derived runtime outputs are intentionally not native catalog rows, but
    # they are queryable by their explicit runtime asset IDs and source refs.
    for item in geometry["assets"]:
        if item["asset_id"] in {asset["asset_id"] for asset in runtime_assets}:
            continue
        if item.get("geometry_status") != "derived_runtime_geometry_closed":
            continue
        tax = taxonomy_by_asset.get(item.get("source_asset_id"), {})
        runtime_assets.append(
            {
                "asset_id": item["asset_id"],
                "relative_path": item.get("relative_path"),
                "family_id": tax.get("family_id", "derived.runtime_output"),
                "subfamily_id": tax.get("subfamily_id", "derived.runtime_output.raster"),
                "lineage": "derived_runtime_output",
                "runtime_manifest_families": ["display_slice"],
                "usage_status": "runtime_manifest_referenced",
                "lifecycle_status": "runtime_manifest_without_native_phase_edge",
                "placement_status": "explicit_binding",
                "composition_ids": item.get("composition_ids", []),
                "geometry_status": item.get("geometry_status"),
                "physical_dimensions": item.get("physical_dimensions", []),
                "source_asset_id": item.get("source_asset_id"),
                "runtime_policy": "lazy_by_runtime_asset_id",
            }
        )
    runtime_assets = sorted(runtime_assets, key=lambda item: item["asset_id"])

    family_manifests = []
    for family_id in sorted({item["family_id"] for item in taxonomy["assets"]}):
        rows = [item for item in taxonomy["assets"] if item["family_id"] == family_id]
        runtime_ids = [item["asset_id"] for item in runtime_assets if item["family_id"] == family_id]
        family_manifests.append(
            {
                "family_id": family_id,
                "asset_count": len(rows),
                "runtime_asset_count": len(runtime_ids),
                "runtime_asset_ids": sorted(runtime_ids),
                "evidence_path": "knowledge/fixtures/accepted/asset_family_taxonomy.json",
                "load_policy": "lazy_manifest_then_family_contract",
            }
        )

    payload = {
        "schema_version": "social-dev-asset-metadata-runtime-manifest-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "approved_for_runtime_query_contract",
        "refs": {
            "usage_matrix": {"path": "knowledge/fixtures/accepted/asset_usage_lifecycle_placement_matrix.json", "content_hash": usage["determinism"]["content_hash"]},
            "geometry": {"path": "knowledge/fixtures/accepted/asset_geometry_catalog.json", "content_hash": geometry["determinism"]["content_hash"]},
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
            "furniture": {"path": "knowledge/fixtures/accepted/furniture_asset_metadata.json", "content_hash": furniture["determinism"]["content_hash"]},
            "character": {"path": "knowledge/fixtures/accepted/character_visual_asset_metadata.json", "content_hash": character["determinism"]["content_hash"]},
            "native_catalog": {"path": "knowledge/fixtures/accepted/runtime/native_content_catalog.json", "content_hash": native_catalog["determinism"]["content_hash"]},
        },
        "counts": {
            "runtime_assets": len(runtime_assets),
            "native_catalog_assets": native_catalog["counts"]["assets"],
            "native_catalog_selectors": native_catalog["counts"]["selectors"],
            "families": len(family_manifests),
            "furniture_records": furniture["counts"]["furniture_records"],
            "staff_records": character["counts"]["staff_records"],
            "helper_records": character["counts"]["helper_records"],
            "rooms": room_manifest["counts"]["rooms"],
            "display_assets": len(display_manifest["assets"]),
            "runtime_asset_lineages": dict(sorted(Counter(item["lineage"] for item in runtime_assets).items())),
        },
        "runtime_assets": runtime_assets,
        "family_manifests": family_manifests,
        "lazy_loading": {
            "asset_lookup": "findRuntimeAssetMetadata(asset_id)",
            "selector_lookup": "findNativeSelector(resource_scope, selector_kind, selector_id)",
            "furniture_lookup": "findFurnitureMetadata(native_id)",
            "character_lookup": "resolveCharacter(record_id)",
            "eager_load_full_catalog": False,
            "source_archive_imports": False,
            "source_code_imports": False,
        },
        "runtime_policy": {
            "approved_scope": "metadata lookup and routing for explicitly cataloged runtime assets",
            "unapproved_assets_are_not_loaded": True,
            "family_composition_gate_required": True,
            "placement_inference_disabled": True,
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-metadata-runtime-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "approved_for_runtime_query_contract",
        "manifest_path": "knowledge/fixtures/accepted/runtime/asset_metadata_runtime_manifest.json",
        "manifest_content_hash": manifest["determinism"]["content_hash"],
        "counts": manifest["counts"],
        "acceptance": {
            "runtime_assets_are_lazy": manifest["lazy_loading"]["eager_load_full_catalog"] is False,
            "source_imports_are_disabled": manifest["lazy_loading"]["source_archive_imports"] is False and manifest["lazy_loading"]["source_code_imports"] is False,
            "runtime_asset_ids_are_unique": len({item["asset_id"] for item in manifest["runtime_assets"]}) == manifest["counts"]["runtime_assets"],
            "native_catalog_boundary_is_preserved": manifest["counts"]["native_catalog_assets"] == 3542 and manifest["counts"]["native_catalog_selectors"] == 3192,
            "family_gate_required": manifest["runtime_policy"]["family_composition_gate_required"] is True,
        },
        "query_surface": ["asset_id", "selector_key", "furniture_data_id", "staff_record_id", "helper_record_id", "room_key"],
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(manifest: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev runtime asset metadata manifest",
        "",
        "This is the runtime query boundary for explicit asset metadata. It is lazy: the browser loads the native catalog and this small runtime-relevant manifest, then resolves by stable IDs without importing source archives or C#.",
        "",
        "## Identity",
        "",
        f"- Manifest hash: `{manifest['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Runtime asset metadata rows | {manifest['counts']['runtime_assets']:,} |",
        f"| Native catalog assets | {manifest['counts']['native_catalog_assets']:,} |",
        f"| Native selectors | {manifest['counts']['native_catalog_selectors']:,} |",
        f"| Family manifests | {manifest['counts']['families']:,} |",
        f"| Furniture records | {manifest['counts']['furniture_records']:,} |",
        f"| Staff records | {manifest['counts']['staff_records']:,} |",
        f"| Helper records | {manifest['counts']['helper_records']:,} |",
        f"| Rooms | {manifest['counts']['rooms']:,} |",
        "",
        "## Query rules",
        "",
        "- Asset: `asset_id` → lazy runtime metadata row.",
        "- Selector: `(resource_scope, selector_kind, selector_id)` → native selector → target asset ID.",
        "- Furniture: `data:furniture:<id>` → selector fields → target assets/composition.",
        "- Character: `staff:<id>` or `helper:<id>` → existing character resolver and capability contract.",
        "- Missing/unresolved records return explicit status; no filename or selector guessing is permitted.",
        "",
        "```powershell",
        "python -B tools/social-dev/build_asset_metadata_runtime_manifest.py",
        "python -B tools/social-dev/test_asset_metadata_runtime_manifest.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    manifest = build_payload()
    contract = build_contract_payload(manifest)
    write_json(MANIFEST_PATH, manifest)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(manifest, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"manifest_hash": manifest["determinism"]["content_hash"], "runtime_assets": manifest["counts"]["runtime_assets"], "families": manifest["counts"]["families"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
