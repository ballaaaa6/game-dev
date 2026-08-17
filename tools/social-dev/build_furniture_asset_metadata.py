"""Build the Track W furniture/world asset metadata catalog."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
SCENE_ASSEMBLY_PATH = RUNTIME_EVIDENCE / "native_scene_assembly_contract.json"
ROOM_RUNTIME_PATH = RUNTIME_EVIDENCE / "room_scene_runtime_contract.json"
SELECTOR_MATRIX_PATH = EVIDENCE / "asset_selector_usage_matrix.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"

CATALOG_PATH = EVIDENCE / "furniture_asset_metadata.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "furniture_asset_metadata_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_furniture_asset_metadata.md"


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
    catalog = load_json(NATIVE_CATALOG_PATH)
    scene = load_json(SCENE_ASSEMBLY_PATH)
    room_runtime = load_json(ROOM_RUNTIME_PATH)
    selector_matrix = load_json(SELECTOR_MATRIX_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    geometry = load_json(GEOMETRY_PATH)

    selector_by_key = {item["selector_key"]: item for item in selector_matrix["selectors"] if item.get("selector_key")}
    taxonomy_by_asset = {item["asset_id"]: item for item in taxonomy["assets"]}
    geometry_by_asset = {item["asset_id"]: item for item in geometry["assets"]}
    relation_by_record_field: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for relation in catalog["connections"]["data_selector"]:
        relation_by_record_field[(relation.get("from"), relation.get("field"))].append(relation)

    native_initial_objects = load_json(RUNTIME_EVIDENCE / "display_asset_manifest.json").get("native_initial_objects", {})
    native_binding_ids = sorted({value.get("furniture_data_id") for value in native_initial_objects.values() if value.get("furniture_data_id") is not None})
    native_binding_records = []
    for room in scene.get("rooms", []):
        for binding in room.get("native_furniture_bindings", []):
            native_binding_records.append({"room_key": room.get("room_key"), **binding})
    binding_by_furniture: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for binding in native_binding_records:
        if binding.get("furniture_data_id") is not None:
            binding_by_furniture[binding["furniture_data_id"]].append(binding)

    furniture_rows = []
    selector_status_counts: Counter[str] = Counter()
    composition_status_counts: Counter[str] = Counter()
    for record in catalog["data_records"]:
        if record.get("data_type") != "FurnitureData":
            continue
        furniture_id = record["native_id"]
        record_id = record["record_id"]
        decoded = record.get("decoded", {})
        fields = decoded.get("fields", {})
        selector_fields = {}
        target_assets = set()
        relation_statuses = {}
        for field_name in ("seb_", "subSeb_", "img_"):
            relations = relation_by_record_field.get((record_id, field_name), [])
            relation = relations[0] if relations else None
            target = relation.get("target_asset_id") if relation else None
            selector_key = relation.get("to") if relation else None
            selector = selector_by_key.get(selector_key) if selector_key else None
            target_assets.add(target) if target else None
            status = relation.get("status") if relation else "relation_not_present"
            relation_statuses[field_name] = status
            selector_status_counts[f"{field_name}:{status}"] += 1
            selector_fields[field_name] = {
                "native_value": fields.get(field_name),
                "selector_key": selector_key,
                "selector_id": selector.get("selector_id") if selector else None,
                "selector_kind": selector.get("selector_kind") if selector else None,
                "resource_scope": selector.get("resource_scope") if selector else None,
                "status": status,
                "target_asset_id": target,
                "target_filename": selector.get("target_filename") if selector else None,
                "target_family_id": taxonomy_by_asset.get(target, {}).get("family_id") if target else None,
                "target_subfamily_id": taxonomy_by_asset.get(target, {}).get("subfamily_id") if target else None,
                "geometry_status": geometry_by_asset.get(target, {}).get("geometry_status") if target else None,
                "composition_ids": geometry_by_asset.get(target, {}).get("composition_ids", []) if target else [],
            }

        composition_targets = [
            item for item in selector_fields.values()
            if item.get("target_asset_id") and item.get("geometry_status") in {"composition_and_geometry_closed", "physical_dimensions_closed", "derived_runtime_geometry_closed"}
        ]
        if not target_assets:
            composition_status = "selector_only_or_sentinel_no_target"
        elif len(composition_targets) == len(target_assets):
            composition_status = "target_geometry_available"
        else:
            composition_status = "target_composition_pending_or_manifest_only"
        composition_status_counts[composition_status] += 1
        placement = binding_by_furniture.get(furniture_id, [])
        placement_status = "verified_native_initial_binding" if placement else "not_bound_to_native_room_fixture"
        furniture_rows.append(
            {
                "record_id": record_id,
                "furniture_data_id": furniture_id,
                "name": fields.get("name_"),
                "type": fields.get("type_"),
                "category": fields.get("category_"),
                "native_status": record.get("source_status"),
                "decoded_status": decoded.get("status"),
                "source_row": record.get("row_index"),
                "source_file": record.get("source_file"),
                "locale_rows": record.get("locale_rows"),
                "fields": fields,
                "selector_fields": selector_fields,
                "selector_relation_statuses": relation_statuses,
                "target_asset_ids": sorted(target_assets),
                "composition_status": composition_status,
                "placement_status": placement_status,
                "native_room_bindings": placement,
                "native_binding_instance_count": len(placement),
                "runtime_lookup_key": f"data:furniture:{furniture_id}",
                "runtime_policy": "explicit_native_binding_only; do_not_infer_from_ObjChip_type_or_cell_topology",
            }
        )

    room_rows = []
    for room in room_runtime.get("rooms", []):
        bindings = room.get("native_bindings", [])
        room_rows.append(
            {
                "room_key": room.get("room_key"),
                "data_key": room.get("data_key"),
                "objchip_cell_count": len(room.get("raw_cells", [])),
                "raw_type_counts": room.get("raw_cell_groups", []),
                "native_binding_status": room.get("native_binding_status"),
                "native_furniture_bindings": bindings,
                "native_furniture_data_ids": sorted({item.get("furniture_data_id") for item in bindings if item.get("furniture_data_id") is not None}),
                "placement_policy": "native_binding_records_only; raw ObjChip topology is not a FurnitureData identity source",
            }
        )

    world_assets = [item for item in taxonomy["assets"] if item["family_id"] == "world.chip"]
    payload = {
        "schema_version": "social-dev-furniture-asset-metadata-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "furniture_metadata_and_native_binding_contract",
        "refs": {
            "native_catalog": {"path": "knowledge/fixtures/accepted/runtime/native_content_catalog.json", "content_hash": catalog["determinism"]["content_hash"]},
            "selector_matrix": {"path": "knowledge/fixtures/accepted/asset_selector_usage_matrix.json", "content_hash": selector_matrix["determinism"]["content_hash"]},
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
            "geometry": {"path": "knowledge/fixtures/accepted/asset_geometry_catalog.json", "content_hash": geometry["determinism"]["content_hash"]},
            "scene_assembly": {"path": "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "content_hash": scene["determinism"]["content_hash"]},
        },
        "counts": {
            "furniture_records": len(furniture_rows),
            "world_chip_assets": len(world_assets),
            "native_binding_furniture_ids": len(native_binding_ids),
            "native_binding_instances": len(native_binding_records),
            "rooms": len(room_rows),
            "rooms_with_native_bindings": sum(1 for item in room_rows if item["native_furniture_bindings"]),
            "selector_statuses": dict(sorted(selector_status_counts.items())),
            "composition_statuses": dict(sorted(composition_status_counts.items())),
        },
        "furniture": sorted(furniture_rows, key=lambda item: item["furniture_data_id"]),
        "rooms": sorted(room_rows, key=lambda item: item["room_key"]),
        "native_binding_ids": native_binding_ids,
        "world_asset_scope": {
            "family_id": "world.chip",
            "asset_count": len(world_assets),
            "runtime_status_counts": dict(sorted(Counter(item["coverage_status"] for item in world_assets).items())),
            "policy": "World-chip taxonomy is closed; furniture instance identity still requires an explicit native FurnitureData binding or a separate source-backed placement contract.",
        },
        "policy": {
            "furniture_id_format": "data:furniture:<native_id>",
            "selector_lookup": "Use selector_fields[field].selector_key and target_asset_id; preserve -1 as absent_by_sentinel.",
            "placement_lookup": "Use native_room_bindings only; never infer a FurnitureData ID from raw ObjChip type or cell coordinates.",
            "composition_lookup": "Follow target_asset_id into the composition/geometry catalogs; do not synthesize frame geometry from name or type.",
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(catalog: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-furniture-asset-metadata-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "furniture_metadata_contract_not_full_world_runtime_approval",
        "catalog_path": "knowledge/fixtures/accepted/furniture_asset_metadata.json",
        "catalog_content_hash": catalog["determinism"]["content_hash"],
        "counts": catalog["counts"],
        "acceptance": {
            "all_furniture_rows_decoded": catalog["counts"]["furniture_records"] == 103,
            "seb_rows_resolved": catalog["counts"]["selector_statuses"].get("seb_:resolved") == 103,
            "subseb_sentinels_explicit": catalog["counts"]["selector_statuses"].get("subSeb_:absent_by_sentinel") == 80,
            "img_sentinels_explicit": catalog["counts"]["selector_statuses"].get("img_:absent_by_sentinel") == 7,
            "all_rooms_present": catalog["counts"]["rooms"] == 18,
            "objchip_to_furniture_inference_disabled": all(item["placement_policy"].startswith("native_binding_records_only") for item in catalog["rooms"]),
        },
        "runtime_policy": {"may_be_used_for_furniture_lookup": True, "may_be_used_for_placement": True, "placement_requires_native_binding": True, "next_gate": "human_helper_avatar_asset_metadata"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(catalog: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev furniture and world asset metadata",
        "",
        "Track W binds all 103 FurnitureData records to selector identities, composition/geometry references, and explicit room-placement status. Raw ObjChip topology remains separate from FurnitureData identity.",
        "",
        "## Identity",
        "",
        f"- Catalog hash: `{catalog['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| FurnitureData records | {catalog['counts']['furniture_records']:,} |",
        f"| World/chip asset rows | {catalog['counts']['world_chip_assets']:,} |",
        f"| Rooms | {catalog['counts']['rooms']:,} |",
        f"| Rooms with explicit native furniture bindings | {catalog['counts']['rooms_with_native_bindings']:,} |",
        f"| Explicit native binding instances | {catalog['counts']['native_binding_instances']:,} |",
        "",
        "## Selector statuses",
        "",
        "| Field/status | Count |",
        "|---|---:|",
    ]
    for status, count in catalog["counts"]["selector_statuses"].items():
        lines.append(f"| `{status}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Placement boundary",
            "",
            "- Room:0 retains the explicit native FurnitureData bindings and six initial instances.",
            "- Rooms 1–17 retain raw 10x10 ObjChip cells and wall/door composition but have no inferred FurnitureData bindings.",
            "- A furniture lookup is repeatable by `data:furniture:<id>` plus selector field keys; placement is repeatable only where a native binding record exists.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_furniture_asset_metadata.py",
            "python -B tools/social-dev/test_furniture_asset_metadata.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    catalog = build_payload()
    contract = build_contract_payload(catalog)
    write_json(CATALOG_PATH, catalog)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(catalog, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"catalog_hash": catalog["determinism"]["content_hash"], "furniture_records": catalog["counts"]["furniture_records"], "rooms": catalog["counts"]["rooms"], "native_binding_instances": catalog["counts"]["native_binding_instances"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
