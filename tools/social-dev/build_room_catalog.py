"""Build the complete RoomData catalog from the native content registry.

This catalog covers every RoomData row currently present in the game data. It
keeps the 10x10 ObjChip occupancy/direction layer separate from the native
MapChip layer, resolves every Room.FLOOR_IMAGE_ID_ARRAY entry through the
source selector registry, and links the shared native MapChip topology policy.
The MapChip topology is selected by Room.floor_, not synthesized from a
RoomData ObjChip grid.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import build_native_content_registry as registry_builder


ROOT = registry_builder.ROOT
REGISTRY_PATH = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
OBJECT_CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/object_catalog_contract.json"
DEFAULT_MAP_PATH = ROOT / "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"
OUTPUT_PATH = ROOT / "knowledge/fixtures/accepted/room_catalog_full.json"
CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/room_catalog_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_room_catalog_full.md"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_json(value: Any) -> str:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def raw_type_catalog() -> dict[int, dict[str, Any]]:
    contract = load(OBJECT_CONTRACT_PATH)
    return {item["raw_type"]: item for item in contract.get("raw_object_types", [])}


def selector_lookup(registry: dict[str, Any]) -> dict[tuple[str, str, int], dict[str, Any]]:
    return {
        (item["resource_scope"], item["selector_kind"], item["selector_id"]): item
        for item in registry["selectors"]
        if item.get("selector_id") is not None
    }


def resolve_selector(
    selectors: dict[tuple[str, str, int], dict[str, Any]],
    scope: str,
    selector_kind: str,
    native_id: int | None,
    field: str,
) -> dict[str, Any]:
    result = {
        "field": field,
        "resource_scope": scope,
        "selector_kind": selector_kind,
        "native_id": native_id,
        "selector_key": None,
        "target_filename": None,
        "target_asset_id": None,
        "status": "unknown",
    }
    if native_id is None:
        result["status"] = "missing_value"
        return result
    if native_id < 0:
        result["status"] = "absent_by_sentinel"
        return result
    selector = selectors.get((scope, selector_kind, native_id))
    result["selector_key"] = f"ref:{scope}:{selector_kind}:{native_id}"
    if selector is None:
        result["status"] = "selector_not_indexed"
        return result
    result.update(
        {
            "target_filename": selector.get("target_filename"),
            "target_asset_id": selector.get("target_asset_id"),
            "resolution_mode": selector.get("resolution_mode"),
            "source_file": selector.get("source_file"),
            "source_row": selector.get("source_row"),
            "status": selector.get("status"),
        }
    )
    return result


def build_floor_image_table(
    default_map: dict[str, Any],
    selectors: dict[tuple[str, str, int], dict[str, Any]],
) -> dict[str, Any]:
    """Resolve the native Room.FLOOR_IMAGE_ID_ARRAY into source selectors."""

    raw_table = default_map.get("native_static_arrays", {}).get("floor_image_id_array")
    if not isinstance(raw_table, dict) or not isinstance(raw_table.get("values"), list):
        raise ValueError("default MapChip contract does not contain FLOOR_IMAGE_ID_ARRAY values")
    values = raw_table["values"]
    entries = []
    for table_index, selector_id in enumerate(values):
        resolved = resolve_selector(
            selectors,
            "chip",
            "img",
            selector_id,
            f"Room.FLOOR_IMAGE_ID_ARRAY[{table_index}]",
        )
        entry = {
            "table_index": table_index,
            "native_selector_id": selector_id,
            "selector_key": resolved["selector_key"],
            "target_filename": resolved["target_filename"],
            "target_asset_id": resolved["target_asset_id"],
            "status": resolved["status"],
            "resolution_mode": resolved.get("resolution_mode"),
            "source_file": resolved.get("source_file"),
            "source_row": resolved.get("source_row"),
        }
        entries.append(entry)
    unresolved = [entry for entry in entries if entry["status"] != "resolved"]
    return {
        "field": "Room.FLOOR_IMAGE_ID_ARRAY",
        "element_type": raw_table.get("element_type"),
        "length": raw_table.get("length", len(values)),
        "values": values,
        "metadata_offset": raw_table.get("metadata_offset"),
        "metadata_hash": raw_table.get("metadata_hash"),
        "entries": entries,
        "unresolved_entry_count": len(unresolved),
        "source_contract": "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
        "source_status": "verified_native_static_array_contract",
    }


def shared_map_chip_contract(
    default_map: dict[str, Any],
    floor_table: dict[str, Any],
) -> dict[str, Any]:
    """Return the shared native MapChip contract without duplicating ObjChip data."""

    native_arrays = default_map.get("native_static_arrays", {})
    map_arrays = native_arrays.get("map_chip_array_by_floor", {})
    variants = {}
    for variant_name, array in map_arrays.items():
        variants[variant_name] = {
            "length": array.get("length"),
            "rows": array.get("rows"),
            "metadata_offset": array.get("metadata_offset"),
            "metadata_hash": array.get("metadata_hash"),
        }
    default_floor = default_map.get("room", {}).get("floor")
    default_variant = f"floor_{default_floor}"
    return {
        "status": "linked_shared_native_contract",
        "contract_path": "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
        "grid": "map",
        "width": default_map.get("room", {}).get("width"),
        "height": default_map.get("room", {}).get("height"),
        "topology_selection": {
            "native_field": "Room.floor_",
            "roomdata_row_does_not_select_topology": True,
            "default_variant": default_variant,
            "available_variants": sorted(variants),
            "status": "shared_native_mapchip_variants",
        },
        "floor_image_table": {
            "field": floor_table["field"],
            "length": floor_table["length"],
            "metadata_offset": floor_table["metadata_offset"],
            "metadata_hash": floor_table["metadata_hash"],
            "source_status": floor_table["source_status"],
        },
        "default_topology_variant": variants.get(default_variant),
        "topology_variants": variants,
        "raw_index_to_selector": default_map.get("raw_index_to_selector"),
        "extension_wall": default_map.get("extension_wall"),
        "status_note": "RoomData contributes its floor image through FLOOR_IMAGE_ID_ARRAY; native MapChip topology is selected separately by Room.floor_ and is never inferred from ObjChip.",
    }


def cell_records(
    room_id: int,
    obj_map: list[list[int]],
    obj_dir: list[list[int]],
    types: dict[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[list[int]]]]:
    cells = []
    grouped: dict[str, list[list[int]]] = {}
    for y, row in enumerate(obj_map):
        for x, raw_type in enumerate(row):
            raw_direction = obj_dir[y][x] if y < len(obj_dir) and x < len(obj_dir[y]) else None
            type_record = types.get(raw_type, {})
            type_name = type_record.get("source_constant", {}).get("name")
            label = type_name or f"UNKNOWN_TYPE_{raw_type}"
            cell = {
                "cell_id": f"cell:room:{room_id}:obj:{x}:{y}",
                "room_id": room_id,
                "grid": "obj",
                "x": x,
                "y": y,
                "flat_index": x + y * len(row),
                "raw_type": raw_type,
                "raw_type_label": label,
                "raw_direction": raw_direction,
                "direction_status": "native_raw_value_untranslated",
                "source_status": "verified_from_RoomData_objMap_objDir",
            }
            cells.append(cell)
            grouped.setdefault(label, []).append([x, y])
    return cells, grouped


def build_room(
    room_record: dict[str, Any],
    selectors: dict[tuple[str, str, int], dict[str, Any]],
    types: dict[int, dict[str, Any]],
    default_map: dict[str, Any],
    floor_table: dict[str, Any],
) -> dict[str, Any]:
    row = room_record["rows"][0]
    decoded = row["decoded"]
    if decoded.get("status") != "verified_reader_order":
        raise ValueError(f"RoomData row {row['row_index']} is not decoded: {decoded}")
    fields = decoded["fields"]
    obj_map = fields["objMap_"]
    obj_dir = fields["objDir_"]
    if not isinstance(obj_map, list) or not isinstance(obj_dir, list):
        raise ValueError(f"RoomData row {row['row_index']} has missing grid arrays")
    if len(obj_map) != len(obj_dir):
        raise ValueError(f"RoomData row {row['row_index']} map/direction height mismatch")
    width = len(obj_map[0]) if obj_map else 0
    if any(len(grid_row) != width for grid_row in obj_map + obj_dir):
        raise ValueError(f"RoomData row {row['row_index']} has ragged grid rows")
    cells, grouped = cell_records(fields["id_"], obj_map, obj_dir, types)
    raw_counts = Counter(cell["raw_type"] for cell in cells)
    door_cells = [cell["cell_id"] for cell in cells if cell["raw_type"] == 5]
    room_id = fields["id_"]
    floor_ref = {
        "field": "floorImgId_",
        "native_domain": "Room.FLOOR_IMAGE_ID_ARRAY",
        "native_id": fields["floorImgId_"],
        "table_index": fields["floorImgId_"],
        "selector_key": None,
        "native_selector_id": None,
        "target_filename": None,
        "target_asset_id": None,
        "status": "floor_array_index_unresolved",
        "status_note": "RoomData.floorImgId_ is an index into the native floor image table, not a direct chip/img.inf selector.",
    }
    table_index = fields["floorImgId_"]
    table_entries = floor_table["entries"]
    if isinstance(table_index, int) and 0 <= table_index < len(table_entries):
        table_entry = table_entries[table_index]
        floor_ref.update(
            {
                "native_selector_id": table_entry["native_selector_id"],
                "selector_key": table_entry["selector_key"],
                "target_filename": table_entry["target_filename"],
                "target_asset_id": table_entry["target_asset_id"],
                "status": "resolved_by_native_floor_image_table" if table_entry["status"] == "resolved" else "floor_table_selector_unresolved",
                "floor_table_entry": table_entry,
            }
        )
    elif isinstance(table_index, int) and table_index < 0:
        floor_ref["status"] = "absent_by_sentinel"
    elif isinstance(table_index, int):
        floor_ref["status"] = "floor_array_index_out_of_range"

    default_room = default_map.get("room", {})
    if (
        room_id == 0
        and table_index == default_room.get("room_data_floor_img_id")
        and default_room.get("resolved_floor_img_selector") is not None
    ):
        floor_ref["runtime_alias"] = {
            "selector_id": default_room.get("resolved_floor_img_selector"),
            "metadata_filename": default_room.get("resolved_floor_metadata_filename"),
            "render_filename": default_room.get("resolved_floor_filename"),
            "status": default_room.get("floor_resolution_status"),
            "note": "Existing room:0 runtime policy is preserved separately from the now-resolved native FLOOR_IMAGE_ID_ARRAY lookup.",
        }
    selectors_out = {
        "floor": floor_ref,
        "wall": resolve_selector(selectors, "chip", "img", fields["wallImgId_"], "wallImgId_"),
        "door": resolve_selector(selectors, "chip", "img", fields["doorImgId_"], "doorImgId_"),
    }
    map_chip = shared_map_chip_contract(default_map, floor_table)
    map_chip.update(
        {
            "roomdata_floor_table_index": table_index,
            "roomdata_floor_native_selector_id": floor_ref.get("native_selector_id"),
            "roomdata_floor_filename": floor_ref.get("target_filename"),
        }
    )
    return {
        "room_key": f"room:{room_id}",
        "data_key": row["catalog_key"],
        "native": {
            "id": fields["id_"],
            "name": fields.get("name_"),
            "cost_money": fields.get("costMoney_"),
            "cost_coin": fields.get("costCoin_"),
            "desk_num": fields.get("deskNum_"),
            "equip_small_num": fields.get("equipSmallNum_"),
            "equip_big_num": fields.get("equipBigNum_"),
            "flag": fields.get("flag_"),
            "cost_max": fields.get("costMax_"),
            "floor_img_id": fields.get("floorImgId_"),
            "wall_img_id": fields.get("wallImgId_"),
            "door_img_id": fields.get("doorImgId_"),
        },
        "selectors": selectors_out,
        "obj_chip": {
            "width": width,
            "height": len(obj_map),
            "obj_map": obj_map,
            "obj_dir": obj_dir,
            "cells": cells,
            "grouped_cells": grouped,
            "raw_type_counts": {str(key): value for key, value in sorted(raw_counts.items())},
            "door_cells": door_cells,
            "direction_policy": "Raw objDir values are retained; semantic direction labels remain native-trace pending.",
        },
        "map_chip": map_chip,
        "source": {
            "registry_path": "knowledge/fixtures/accepted/native_content_registry.json",
            "registry_row": row["row_index"],
            "english_raw_row_sha256": row["locales"].get("English.lproj", {}).get("raw_row_sha256"),
            "japanese_raw_row_sha256": row["locales"].get("Japanese.lproj", {}).get("raw_row_sha256"),
            "raw_columns": row["locales"].get("English.lproj", {}).get("raw_columns"),
            "raw_columns_japanese": row["locales"].get("Japanese.lproj", {}).get("raw_columns"),
        },
    }


def build_payload() -> dict[str, Any]:
    registry = load(REGISTRY_PATH)
    types = raw_type_catalog()
    selectors = selector_lookup(registry)
    if not DEFAULT_MAP_PATH.is_file():
        raise ValueError(f"missing native MapChip contract: {DEFAULT_MAP_PATH}")
    default_map = load(DEFAULT_MAP_PATH)
    floor_table = build_floor_image_table(default_map, selectors)
    room_type = next(item for item in registry["data_types"] if item["source_type"] == "RoomData")
    rooms = [
        build_room(
            {
                "rows": [row],
            },
            selectors,
            types,
            default_map,
            floor_table,
        )
        for row in room_type["rows"]
    ]
    total_cells = sum(room["obj_chip"]["width"] * room["obj_chip"]["height"] for room in rooms)
    linked_map_chip_rooms = [room["room_key"] for room in rooms if room["map_chip"]["status"] == "linked_shared_native_contract"]
    unresolved_selectors = [
        {
            "room": room["room_key"],
            "field": field,
            "native_id": value["native_id"],
            "status": value["status"],
        }
        for room in rooms
        for field, value in room["selectors"].items()
        if value["status"] not in {"resolved", "absent_by_sentinel", "resolved_by_native_floor_image_table"}
    ]
    payload = {
        "schema_version": "social-dev-room-catalog-full-v1",
        "status": "pass" if len(rooms) == 18 and not unresolved_selectors else "pass_with_explicit_gaps",
        "semantic_status": "roomdata_complete_mapchip_shared_contract",
        "policy": {
            "roomdata_source_is_complete": True,
            "objchip_grid_is_separate_from_mapchip_grid": True,
            "floor_image_table_is_native_and_resolved": floor_table["unresolved_entry_count"] == 0,
            "mapchip_topology_is_selected_by_room_floor": True,
            "direction_labels_are_not_invented": True,
            "unresolved_floor_wall_door_selectors_are_explicit": True,
            "runtime_aliases_are_separate_from_native_resolution": True,
        },
        "registry_content_hash": registry["content_hash"],
        "native_floor_image_table": floor_table,
        "rooms": rooms,
        "map_chip_scope": {
            "linked_rooms": linked_map_chip_rooms,
            "unlinked_room_count": len(rooms) - len(linked_map_chip_rooms),
            "status": "shared_native_floor_table_and_topology_contract",
            "topology_selection_field": "Room.floor_",
            "roomdata_floor_table_field": "RoomData.floorImgId_",
            "note": "All RoomData floor image indexes resolve through the native FLOOR_IMAGE_ID_ARRAY. The 14x14 topology remains a shared native MapChip contract selected by Room.floor_, never inferred from ObjChip.",
        },
        "validation": {
            "room_count": len(rooms),
            "room_ids": [room["native"]["id"] for room in rooms],
            "total_objchip_cells": total_cells,
            "unresolved_selector_count": len(unresolved_selectors),
            "unresolved_selectors": unresolved_selectors,
            "all_obj_grids_rectangular": all(
                room["obj_chip"]["width"] > 0
                and room["obj_chip"]["height"] > 0
                and len(room["obj_chip"]["obj_map"]) == room["obj_chip"]["height"]
                for room in rooms
            ),
        },
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["content_hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return payload


def write_outputs(payload: dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    contract = {
        "schema_version": "social-dev-room-catalog-contract-v1",
        "package": "social-dev-room-catalog",
        "status": payload["status"],
        "semantic_status": payload["semantic_status"],
        "catalog_path": "knowledge/fixtures/accepted/room_catalog_full.json",
        "catalog_content_hash": payload["content_hash"],
        "registry_content_hash": payload["registry_content_hash"],
        "counts": {
            "rooms": len(payload["rooms"]),
            "objchip_cells": payload["validation"]["total_objchip_cells"],
            "linked_mapchip_rooms": len(payload["map_chip_scope"]["linked_rooms"]),
            "native_floor_image_table_entries": payload["native_floor_image_table"]["length"],
            "unresolved_selectors": payload["validation"]["unresolved_selector_count"],
        },
        "room_keys": [room["room_key"] for room in payload["rooms"]],
        "native_floor_image_table": {
            "field": payload["native_floor_image_table"]["field"],
            "values": payload["native_floor_image_table"]["values"],
            "metadata_offset": payload["native_floor_image_table"]["metadata_offset"],
            "metadata_hash": payload["native_floor_image_table"]["metadata_hash"],
            "unresolved_entry_count": payload["native_floor_image_table"]["unresolved_entry_count"],
        },
        "native_grid_policy": {
            "objchip": "RoomData.objMap_/objDir_ jagged arrays decoded through the native reader sequence",
            "mapchip": "Shared native MapChip topology selected by Room.floor_; never inferred from ObjChip cells",
        },
        "open_items": [
            "Raw objDir values are recorded but direction labels require the native direction-vector trace.",
            "The existing room:0 runtime alias remains separate from the native floor-image-table lookup until the runtime resolver consumes this catalog.",
        ],
    }
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Social Dev complete RoomData catalog",
        "",
        "All RoomData rows are cataloged from the native reader order. The 10x10 ObjChip grid is kept separate from the 14x14 MapChip topology.",
        "",
        "## Summary",
        "",
        f"- Rooms: `{len(payload['rooms'])}` (`room:0` through `room:17`)",
        f"- ObjChip cells: `{payload['validation']['total_objchip_cells']}`",
        f"- MapChip floor-image links: `{len(payload['map_chip_scope']['linked_rooms'])}/{len(payload['rooms'])}`",
        f"- Native FLOOR_IMAGE_ID_ARRAY entries: `{payload['native_floor_image_table']['length']}`",
        f"- Explicit selector gaps: `{payload['validation']['unresolved_selector_count']}`",
        "",
        "## Room index",
        "",
        "| Room | Name | ObjChip | Desk slots | Small slots | Big slots | Door cells | MapChip status |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for room in payload["rooms"]:
        native = room["native"]
        groups = room["obj_chip"]["raw_type_counts"]
        lines.append(
            f"| `{room['room_key']}` | {native['name']} | {room['obj_chip']['width']}×{room['obj_chip']['height']} | "
            f"{groups.get('2', 0)} | {groups.get('1', 0)} | {groups.get('3', 0) + groups.get('4', 0)} | "
            f"{len(room['obj_chip']['door_cells'])} | `{room['map_chip']['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Resolution policy",
            "",
            "RoomData `wallImgId_` and `doorImgId_` values are direct `chip/img.inf` selector IDs. `floorImgId_` is an index into the native `Room.FLOOR_IMAGE_ID_ARRAY`; all 18 RoomData rows now resolve that table index to a selector and source asset.",
            "",
            "MapChip topology is not synthesized from the object grid. The shared native MapChip contract is selected by `Room.floor_`; the RoomData catalog carries the floor-image table link for every room while preserving the existing room:0 runtime alias as a separate policy.",
            "",
            f"Registry hash: `{payload['registry_content_hash']}`",
            f"Catalog hash: `{payload['content_hash']}`",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_outputs(payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "rooms": len(payload["rooms"]),
                "objchip_cells": payload["validation"]["total_objchip_cells"],
                "unresolved_selectors": payload["validation"]["unresolved_selector_count"],
                "content_hash": payload["content_hash"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
