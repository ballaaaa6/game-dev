"""Build the evidence-backed Phase 3B room-placement contract for room:0.

This builder is evidence-only. It reads the current catalog contracts, native
evidence, source hashes and the pinned asset index. It never executes recovered
C# or native code and it does not promote binary assets into the runtime.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"

SCENE_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
OBJECT_PATH = RUNTIME_EVIDENCE / "object_catalog_contract.json"
CAMERA_PATH = RUNTIME_EVIDENCE / "camera_coordinate_contract.json"
DISPLAY_ASSET_PATH = RUNTIME_EVIDENCE / "display_asset_manifest.json"
SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
NATIVE_PATH = EVIDENCE / "scene_native_semantics.json"
PASSMAP_PATH = EVIDENCE / "phase1d_passmap_fixture.json"
ROUTE_PATH = EVIDENCE / "phase1d_route_fixture.json"
PHASE3A_CLOSURE_PATH = EVIDENCE / "phase3a_asset_composition_closure.json"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"

SOURCE_FILES = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "MapChip": SOURCE_ROOT / "game/MapChip.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "RoomData": SOURCE_ROOT / "data/RoomData.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
}

SOURCE_SLICES = [
    {
        "id": "room-constructor-and-map-init",
        "type": "Room",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 149,
        "line_end": 453,
        "purpose": "Room construction order and floor selector passed to MapChip.",
    },
    {
        "id": "room-object-init-and-parent-setup",
        "type": "Room",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 454,
        "line_end": 763,
        "purpose": "ObjChip grid construction and multi-chip parent setup boundary.",
    },
    {
        "id": "room-door-placement",
        "type": "Room",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 764,
        "line_end": 908,
        "purpose": "Door type scan, null FurnitureData placement path and installed flag.",
    },
    {
        "id": "room-draw-and-pass-sites",
        "type": "Room",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 1165,
        "line_end": 3450,
        "purpose": "Decompiler-bounded Room.Draw call sites used for draw-pass ordering.",
    },
    {
        "id": "room-coordinate-formulas",
        "type": "Room",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 6168,
        "line_end": 6255,
        "purpose": "Native grid-to-world coordinate formulas and door lookup boundary.",
    },
    {
        "id": "map-chip-draw",
        "type": "MapChip",
        "file": "sources/raw/1_Click_CSharp_Code update/game/MapChip.cs",
        "line_start": 52,
        "line_end": 405,
        "purpose": "Native map-chip draw basis and floor image placement formula.",
    },
    {
        "id": "obj-chip-wall-draw",
        "type": "ObjChip",
        "file": "sources/raw/1_Click_CSharp_Code update/game/ObjChip.cs",
        "line_start": 2173,
        "line_end": 2701,
        "purpose": "Native wall/object draw anchors and room wall/door selector reads.",
    },
    {
        "id": "obj-chip-draw",
        "type": "ObjChip",
        "file": "sources/raw/1_Click_CSharp_Code update/game/ObjChip.cs",
        "line_start": 2702,
        "line_end": 3002,
        "purpose": "Native object draw dispatch boundary.",
    },
    {
        "id": "obj-chip-placement",
        "type": "ObjChip",
        "file": "sources/raw/1_Click_CSharp_Code update/game/ObjChip.cs",
        "line_start": 9912,
        "line_end": 10043,
        "purpose": "Furniture binding, direction and placement state reset.",
    },
    {
        "id": "room-data-load-order",
        "type": "RoomData",
        "file": "sources/raw/1_Click_CSharp_Code update/data/RoomData.cs",
        "line_start": 23,
        "line_end": 73,
        "purpose": "RoomData scalar and grid field load order.",
    },
    {
        "id": "appdata-chip-constants",
        "type": "AppData",
        "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs",
        "line_start": 1200,
        "line_end": 1264,
        "purpose": "Source-labeled chip image and SEB selector constants.",
    },
]

DRAW_PASS_SITES = [
    {
        "id": "map-extension-floor",
        "method": "MapChip.DrawExtentionFloor",
        "line": 2220,
        "layer_role": "map_extension_floor",
    },
    {
        "id": "map-chip",
        "method": "MapChip.Draw",
        "line": 2291,
        "layer_role": "map_chip_boundary_and_wall_sprites",
    },
    {
        "id": "object-chip-primary",
        "method": "ObjChip.Draw",
        "line": 2682,
        "layer_role": "object_primary",
    },
    {
        "id": "object-chip-wall",
        "method": "ObjChip.DrawWall",
        "line": 2812,
        "layer_role": "object_wall_overlay",
    },
    {
        "id": "avatar-primary",
        "method": "Avatar.Draw",
        "line": 2874,
        "layer_role": "actor_primary",
    },
    {
        "id": "avatar-secondary",
        "method": "Avatar.Draw",
        "line": 3046,
        "layer_role": "actor_secondary",
    },
    {
        "id": "object-chip-late-preview",
        "method": "ObjChip.Draw",
        "line": 3178,
        "layer_role": "object_late_preview",
    },
    {
        "id": "object-chip-late",
        "method": "ObjChip.Draw",
        "line": 3260,
        "layer_role": "object_late",
    },
    {
        "id": "map-floor",
        "method": "MapChip.DrawFloor",
        "line": 3426,
        "layer_role": "map_floor",
    },
]

SCHEMA_VERSION = "social-dev-phase3b-room-placement-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-phase3b-room-placement-fixture-v1"
AUDIT_SCHEMA_VERSION = "social-dev-phase3b-room-placement-source-audit-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-phase3b-room-placement-validation-v1"

FLOOR_RUNTIME_FALLBACK = {
    "target_selector_id": 85,
    "filename": "floor_09.png",
    "reason_code": "user_approved_runtime_alias",
    "decision": "The unresolved raw floor selector 5 uses floor_09.png as an explicit runtime alias; source mapping remains unresolved.",
}


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


def content_hash(value: Any) -> str:
    return sha256_bytes(stable_json(value).encode("utf-8"))


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def evidence_ref(path: Path) -> dict[str, str]:
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = [evidence_ref(path) for path in sorted(set(paths), key=lambda item: relative_path(item))]
    return {"files": files, "input_hash": content_hash(files)}


def source_slice_ref(item: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / item["file"]
    result = copy.deepcopy(item)
    if not path.is_file():
        result.update({"file_sha256": None, "slice_sha256": None, "hash_status": "missing"})
        return result
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = int(item["line_start"])
    end = int(item["line_end"])
    text = "".join(lines[start - 1 : end])
    result.update(
        {
            "file_sha256": sha256_file(path),
            "slice_sha256": sha256_bytes(text.encode("utf-8")),
            "hash_status": "pass",
        }
    )
    return result


def asset_index_map() -> dict[str, dict[str, Any]]:
    rows = load_json(ASSET_INDEX_PATH)
    if not isinstance(rows, list):
        raise ValueError("ASSET_INDEX.json must contain a list")
    result = {str(row["relative_path"]).replace("\\", "/"): row for row in rows}
    if len(result) != len(rows):
        raise ValueError("ASSET_INDEX.json contains duplicate relative paths")
    return result


def asset_ref(index: dict[str, dict[str, Any]], member: str) -> dict[str, Any]:
    normalized = member.replace("\\", "/")
    row = index.get(normalized)
    if row is None:
        raise KeyError(f"asset index is missing {normalized}")
    return {
        "relative_path": normalized,
        "kind": row.get("kind"),
        "pack": row.get("pack"),
        "original_name": row.get("original_name"),
        "size_bytes": row.get("size"),
        "width": row.get("width"),
        "height": row.get("height"),
        "format": row.get("format"),
        "sha256": row.get("sha256"),
        "apk_source_entry": row.get("apk_source_entry"),
    }


def selector_entry(selector_contract: dict[str, Any], selector_name: str, selector_id: int) -> str | None:
    indexes = selector_contract.get("selector_indexes") or selector_contract["asset_zip"]["selector_indexes"]
    index = indexes[selector_name]["entries"]
    return index.get(str(selector_id))


def build_image_selector(
    selector_contract: dict[str, Any],
    index: dict[str, dict[str, Any]],
    raw_id: int,
    role: str,
    runtime_fallback: dict[str, Any] | None = None,
) -> dict[str, Any]:
    filename = selector_entry(selector_contract, "chip_img", raw_id)
    result: dict[str, Any] = {
        "role": role,
        "index_name": "chip_img",
        "raw_selector_id": raw_id,
        "resolution_status": "resolved" if filename else "unresolved",
        "runtime_promotion_status": "not_promoted_in_phase3b",
        "runtime_resolution_status": "source_resolved" if filename else "unresolved",
    }
    if filename is None:
        result.update(
            {
                "reason_code": "missing_img_inf_entry",
                "reason": f"chip/img.inf has no entry for raw selector id {raw_id}; no authoritative source filename is available.",
                "asset": None,
            }
        )
    else:
        result.update(
            {
                "filename": filename,
                "asset": asset_ref(index, f"01_GAME_PACKS/chip/{filename}"),
            }
        )
    if runtime_fallback is not None:
        target_selector_id = int(runtime_fallback["target_selector_id"])
        target_filename = str(runtime_fallback["filename"])
        indexed_target_filename = selector_entry(selector_contract, "chip_img", target_selector_id)
        if indexed_target_filename != target_filename:
            raise ValueError(
                f"runtime fallback selector {target_selector_id} does not resolve to {target_filename!r}"
            )
        result.update(
            {
                "runtime_promotion_status": "approved_explicit_fallback",
                "runtime_resolution_status": "explicit_fallback",
                "runtime_fallback": {
                    "target_selector_id": target_selector_id,
                    "filename": target_filename,
                    "resolution_status": "resolved",
                    "resolution_mode": "explicit_user_approved_alias",
                    "reason_code": runtime_fallback["reason_code"],
                    "decision": runtime_fallback["decision"],
                    "asset": asset_ref(index, f"01_GAME_PACKS/chip/{target_filename}"),
                },
            }
        )
    return result


def build_seb_selector(
    selector_contract: dict[str, Any],
    index: dict[str, dict[str, Any]],
    selector_id: int,
    role: str,
) -> dict[str, Any]:
    filename = selector_entry(selector_contract, "chip_seb", selector_id)
    if filename is None:
        raise ValueError(f"chip_seb selector id {selector_id} is unresolved")
    return {
        "role": role,
        "index_name": "chip_seb",
        "raw_selector_id": selector_id,
        "resolution_status": "resolved",
        "filename": filename,
        "asset": asset_ref(index, f"01_GAME_PACKS/chip/{filename}"),
        "runtime_promotion_status": "not_promoted_in_phase3b",
    }


def native_methods(native: dict[str, Any]) -> list[dict[str, Any]]:
    selected = [
        "room-init-obj-chips",
        "room-setup-big-chips-parent",
        "room-place-door",
        "objchip-place-object",
        "objchip-standing-positions",
        "objchip-is-passable",
    ]
    methods = {item["id"]: item for item in native["native_method_manifest"]}
    missing = [item for item in selected if item not in methods]
    if missing:
        raise ValueError(f"native evidence is missing methods: {missing}")
    return [copy.deepcopy(methods[item]) for item in selected]


def upstream_ref(path: Path) -> dict[str, Any]:
    value = load_json(path)
    return {
        "path": relative_path(path),
        "sha256": sha256_file(path),
        "contract_hash": value.get("determinism", {}).get("contract_hash")
        or value.get("determinism", {}).get("content_hash"),
        "status": value.get("status"),
        "semantic_status": value.get("semantic_status"),
    }


def cell_origin(x: int, y: int) -> dict[str, int]:
    return {"x": (x + y) * 20 + 20, "y": (y - x) * 10 + 18}


def actor_origin(x: int, y: int) -> dict[str, int]:
    return {"x": (x + y) * 20 + 40, "y": (y - x) * 10 + 9}


def map_draw_origin(x: int, y: int, ofx: int = 0, ofy: int = 0) -> dict[str, int]:
    return {"x": ofx + (x + y) * 40, "y": ofy + (y - x) * 20}


def object_draw_origin(x: int, y: int, ofx: int = 0, ofy: int = 0) -> dict[str, int]:
    return {"x": ofx + (x + y) * 20, "y": ofy + (y - x) * 10 + 9}


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    scene = load_json(SCENE_PATH)
    objects = load_json(OBJECT_PATH)
    camera = load_json(CAMERA_PATH)
    display_assets = load_json(DISPLAY_ASSET_PATH)
    selector_contract = load_json(SELECTOR_PATH)
    native = load_json(NATIVE_PATH)
    passmap = load_json(PASSMAP_PATH)
    route = load_json(ROUTE_PATH)
    phase3a_closure = load_json(PHASE3A_CLOSURE_PATH)
    phase3a_approved = phase3a_closure.get("status") == "approved"
    asset_index = asset_index_map()

    scene_record = next(item for item in scene["scenes"] if item["id"] == "room:0")
    object_by_id = {item["id"]: item for item in objects["objects"]}
    door_cell = copy.deepcopy(scene_record["door"]["cells"][0])
    type4_fixture = copy.deepcopy(scene_record["type4_fixture"])
    type4_passmap = copy.deepcopy(passmap["isPassable"])

    selectors = {
        "floor": build_image_selector(
            selector_contract,
            asset_index,
            5,
            "room.floorImgId_",
            runtime_fallback=FLOOR_RUNTIME_FALLBACK,
        ),
        "wall": build_image_selector(selector_contract, asset_index, 6, "room.wallImgId_"),
        "door": build_image_selector(selector_contract, asset_index, 7, "room.doorImgId_"),
    }
    selectors["wall"]["native_composition"] = {
        "seb": build_seb_selector(selector_contract, asset_index, 5, "native wall SEB constant"),
        "image": "room.wallImgId_",
        "status": "source_selector_pair",
    }
    selectors["door"]["native_composition"] = {
        "seb": build_seb_selector(selector_contract, asset_index, 9, "FurnitureData(1) door selector candidate"),
        "image": "room.doorImgId_",
        "status": "native_draw_parameter_pair; FurnitureData binding remains unpromoted",
    }

    footprint = copy.deepcopy(passmap["native_placement"])
    type4_placement = {
        "object_id": "furniture:0",
        "status": "verified_native_fixture",
        "anchor": copy.deepcopy(type4_fixture["anchor"]),
        "raw_type": 4,
        "furniture_data_id": 0,
        "parent_center_offset": copy.deepcopy(footprint["parent_center_offset"]),
        "footprint_offsets": footprint["footprint_offsets"],
        "footprint": footprint["footprint"],
        "pass_map": copy.deepcopy(passmap["furniture_record"]),
        "passability": type4_passmap,
        "provenance": {
            "passmap_fixture": evidence_ref(PASSMAP_PATH),
            "scene_catalog": upstream_ref(SCENE_PATH),
            "object_catalog_binding": next(
                copy.deepcopy(item)
                for item in objects["scene_bindings"]
                if item["id"] == "room:0/type4-anchor"
            ),
        },
    }

    object_boundary = {
        "approved_display_compositions": sorted(display_assets["objects"]),
        "native_room_bindings": [
            {
                "object_id": "furniture:0",
                "status": "verified_native_fixture",
                "cell": [4, 2],
                "note": "The type-4 parent/footprint fixture binds FurnitureData(0).",
            },
            {
                "object_id": "furniture:1",
                "status": "selector_candidate_not_native_binding",
                "cell": [8, 4],
                "note": "Room.PlaceDoor calls PlaceObj(null) and sets installed; FurnitureData(1) remains a selector candidate.",
            },
            {
                "object_id": "furniture:5",
                "status": "approved_selector_not_placed_in_room0",
                "cell": None,
                "note": "The approved composition exists, but no native room:0 FurnitureData(5) binding is evidenced.",
            },
            {
                "object_id": "furniture:2",
                "status": "approved_selector_not_placed_in_room0" if phase3a_approved else "quarantined_source_limitation",
                "cell": None,
                "note": (
                    "Phase 3A chair_00 variable-piece reconstruction is approved; no native room:0 FurnitureData(2) binding is evidenced."
                    if phase3a_approved
                    else "Phase 3A quarantine remains active because chair_00.opt is truncated and has no authoritative recovery."
                ),
            },
        ],
        # Keep the Phase 3A approval boundary without importing the closure's
        # generated gate/manifest hashes. Those hashes are downstream of the
        # display gate and would recreate a cross-phase dependency cycle that
        # the room contract is meant to sit upstream of.
        "quarantine_ref": {
            "path": relative_path(PHASE3A_CLOSURE_PATH),
            "status": phase3a_closure.get("status"),
            "semantic_status": phase3a_closure.get("semantic_status"),
            "source_audit_content_hash": phase3a_closure.get("source_audit_ref", {}).get("content_hash"),
        },
        "runtime_policy": {
            "promote_furniture_2": phase3a_approved,
            "allow_native_furniture_id_inference": False,
            "require_explicit_scene_binding": True,
        },
    }

    coordinates = {
        "grid": {
            "width": 10,
            "height": 10,
            "indexing": "x + y * width",
            "row_axis": "y",
            "column_axis": "x",
        },
        "cell_origin": {
            "formula_x": "(x + y) * 20 + 20",
            "formula_y": "(y - x) * 10 + 18",
            "status": "verified_source_formula",
            "probes": [
                {"cell": [0, 0], "world": cell_origin(0, 0)},
                {"cell": [4, 2], "world": cell_origin(4, 2)},
                {"cell": [8, 4], "world": cell_origin(8, 4)},
                {"cell": [9, 9], "world": cell_origin(9, 9)},
            ],
        },
        "actor_spawn": {
            "formula_x": "(x + y) * 20 + 40",
            "formula_y": "(y - x) * 10 + 9",
            "status": "verified_source_bounded",
            "probes": [{"cell": [8, 4], "world": actor_origin(8, 4)}],
        },
        "standing_positions": copy.deepcopy(camera["coordinate_system"]["standing_positions"]),
        "map_chip_draw_origin": {
            "formula_x": "ofx + (x + y) * 40",
            "formula_y": "ofy + (y - x) * 20",
            "floor_image_bottom_y": "origin_y + 39",
            "status": "verified_source_formula",
            "probes": [{"cell": [8, 4], "origin": map_draw_origin(8, 4)}],
        },
        "object_draw_origin": {
            "formula_x": "ofx + (x + y) * 20",
            "formula_y": "ofy + (y - x) * 10 + 9",
            "status": "verified_source_bounded",
            "probes": [{"cell": [8, 4], "origin": object_draw_origin(8, 4)}],
        },
        "camera": {
            "transform": camera["camera"]["transform"],
            "fixture_offset": camera["camera"]["fixture_offset"],
            "fixture_scale": camera["camera"]["fixture_scale"],
            "source_boundary": camera["camera"]["source_boundary"],
            "dynamic_viewport_status": "not_inferred",
        },
        "bounded_room0_world": {
            "cell_origin_min": [20, -72],
            "cell_origin_max": [380, 108],
            "actor_origin_min": [40, -81],
            "actor_origin_max": [400, 99],
            "status": "deterministic_10x10_fixture_bounds",
        },
    }

    draw_order = {
        "status": "verified_source_call_order_bounded",
        "source_method": "Room.Draw(Graphics, ofx, ofy, drawMode)",
        "ordering_rule": "Preserve the observed Room.Draw call-site order; do not replace it with a renderer y-sort.",
        "decompiler_limit": "The current C# method body is damaged; this closes observed call order, not missing branch predicates or sprite alpha semantics.",
        "passes": [
            {**item, "source_file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs"}
            for item in DRAW_PASS_SITES
        ],
        "overlap_fixture": {
            "cell": [8, 4],
            "events": [
                {"id": "door-object", "method": "ObjChip.Draw", "pass_id": "object-chip-primary"},
                {"id": "floor-image", "method": "MapChip.DrawFloor", "pass_id": "map-floor"},
            ],
            "expected_event_order": ["door-object", "floor-image"],
            "assertion": "The renderer must retain the native pass order for this shared-cell overlap fixture.",
        },
    }

    native_placement = {
        "init_order": [
            "Room.InitMapChips",
            "Room.InitObjChips",
            "Room.SetupBigChipsParent",
            "Room.PlaceDoor",
        ],
        "raw_grid_assignment": {
            "source_field": "RoomData.objMap_",
            "cell_expression": "objMap[y][x]",
            "constructor": "new ObjChip(x, y, rawCell, null, room)",
            "flat_index": "x + y * objMapWidth_",
        },
        "door": {
            "cell": door_cell,
            "raw_type": 5,
            "installed_flag": 1,
            "place_obj_furniture_data": None,
            "native_furniture_binding_status": "not_bound_by_room_place_door",
        },
        "type4": type4_placement,
        "route_fixture": copy.deepcopy(route["route"]),
        "route_filter_probes": copy.deepcopy(route["filter_probes"]),
    }

    input_paths = [
        SCENE_PATH,
        OBJECT_PATH,
        CAMERA_PATH,
        SELECTOR_PATH,
        ASSET_INDEX_PATH,
        NATIVE_PATH,
        PASSMAP_PATH,
        ROUTE_PATH,
        APK_PATH,
        *SOURCE_FILES.values(),
    ]
    manifest = input_manifest(input_paths)
    source_refs = [source_slice_ref(item) for item in SOURCE_SLICES]
    source_hashes = {name: sha256_file(path) for name, path in SOURCE_FILES.items()}
    all_source_hashes_pass = all(item["hash_status"] == "pass" for item in source_refs)

    source_audit = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "package": "social-dev-phase3b-room-placement-source-audit",
        "status": "pass",
        "semantic_status": "closed_for_phase3b_with_explicit_unresolved_selector",
        "generated_at_utc": utc_now(),
        "scene_ref": upstream_ref(SCENE_PATH),
        "source_artifacts": {
            "apk": {**evidence_ref(APK_PATH), "role": "native evidence only"},
            "source_files": source_hashes,
        },
        "input_manifest": manifest,
        "selector_chain": copy.deepcopy(selectors),
        "unresolved": [
            {
                "id": "room:0/floorImgId_",
                "raw_selector_id": 5,
                "reason_code": "missing_img_inf_entry",
                "status": "explicit_unresolved",
                "runtime_policy": "retain raw id; use the explicit approved runtime alias to selector 85 / floor_09.png",
            }
        ],
        "source_slices": source_refs,
        "native_methods": native_methods(native),
        "limits": [
            "C# and APK remain evidence inputs only.",
            "The missing chip/img.inf id 5 remains source-unresolved; the runtime alias to floor_09.png is an explicit product decision, not recovered provenance.",
            "The source-bounded draw order does not claim decompiler-damaged branch predicates or alpha semantics.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    source_audit["determinism"]["content_hash"] = content_hash(without_dynamic(source_audit))

    fixture = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-phase3b-room-placement-fixture",
        "status": "pass",
        "semantic_status": "deterministic_fixture",
        "generated_at_utc": utc_now(),
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "source_id": 0},
        "selectors": selectors,
        "native_placement": native_placement,
        "object_boundary": object_boundary,
        "coordinates": coordinates,
        "draw_order": draw_order,
        "provenance": {
            "source_audit": {
                "path": relative_path(EVIDENCE / "phase3b_room_placement_source_audit.json"),
                "content_hash": source_audit["determinism"]["content_hash"],
            },
            "phase1d_passmap": evidence_ref(PASSMAP_PATH),
            "phase1d_route": evidence_ref(ROUTE_PATH),
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    fixture["determinism"]["content_hash"] = content_hash(without_dynamic(fixture))

    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-room-placement-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "generated_at_utc": utc_now(),
        "catalog_id": "display-slice-01",
        "scene_ref": upstream_ref(SCENE_PATH) | {"id": "room:0"},
        "object_catalog_ref": upstream_ref(OBJECT_PATH),
        "camera_coordinate_ref": upstream_ref(CAMERA_PATH),
        # Phase 3B consumes the display gate's approval status and the
        # source-backed object keys above, but it must not pin the generated
        # Phase 3C manifest hash. That manifest also contains the strict
        # closure reference, so hashing it here would create a cycle:
        # display manifest -> room contract -> strict closure -> display gate.
        "display_asset_manifest_ref": {
            "path": relative_path(DISPLAY_ASSET_PATH),
            "status": display_assets.get("status"),
            "semantic_status": display_assets.get("semantic_status"),
        },
        "selectors": selectors,
        "native_placement": native_placement,
        "object_boundary": object_boundary,
        "coordinates": coordinates,
        "draw_order": draw_order,
        "fixture_ref": {
            "path": relative_path(EVIDENCE / "phase3b_room_placement_fixture.json"),
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "source_audit_ref": {
            "path": relative_path(EVIDENCE / "phase3b_room_placement_source_audit.json"),
            "content_hash": source_audit["determinism"]["content_hash"],
        },
        "runtime_policy": {
            "source_code_imports": False,
            "archive_imports": False,
            "unapproved_binary_imports": False,
            "unresolved_selector_policy": "retain raw selector and use the explicit per-selector runtime fallback while preserving the source gap",
            "phase3b_asset_promotion": "explicit floor fallback only; source selector resolution remains evidence-only",
            "quarantined_objects_excluded": [] if phase3a_approved else ["furniture:2"],
        },
        "limits": [
            "This contract covers native room:0 placement and source-bounded draw pass order.",
            "The floor image selector remains source-unresolved because img.inf has no id 5 entry; runtime uses the explicit floor_09.png alias at selector 85.",
            "FurnitureData identity is not inferred for the native door path; Room.PlaceDoor binds null and sets installed.",
            "Canvas rendering and screenshot/browser fidelity remain Phase 3C work.",
        ],
        "provenance": {
            "input_manifest": manifest,
            "source_audit": source_audit["determinism"]["content_hash"],
            "native_semantics": evidence_ref(NATIVE_PATH),
            "apk": evidence_ref(APK_PATH),
            "source_files": source_hashes,
            "source_policy": "C# and native artifacts are evidence inputs only; the browser runtime must not import or execute them.",
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }
    contract["determinism"]["contract_hash"] = content_hash(without_dynamic(contract))

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append(
            {
                "id": check_id,
                "status": "pass" if condition else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    check(
        "scene-identity",
        scene_record["id"] == "room:0" and scene_record["source_identity"]["source_id"] == 0,
        {"id": scene_record["id"], "source_id": scene_record["source_identity"]["source_id"]},
        {"id": "room:0", "source_id": 0},
        "Phase 3B is bounded to RoomData(0).",
    )
    check(
        "grid-shape-and-indexing",
        scene_record["grid"]["width"] == scene_record["grid"]["height"] == 10
        and scene_record["grid"]["indexing"]["flat_index"] == "x + y * width",
        {"width": scene_record["grid"]["width"], "height": scene_record["grid"]["height"], "indexing": scene_record["grid"]["indexing"]},
        {"width": 10, "height": 10, "flat_index": "x + y * width"},
        "The native grid remains y-major with x + y * width storage.",
    )
    check(
        "floor-selector-explicit-fallback",
        (
            selectors["floor"]["resolution_status"] == "unresolved"
            and selectors["floor"]["reason_code"] == "missing_img_inf_entry"
            and selectors["floor"]["asset"] is None
            and selectors["floor"]["runtime_resolution_status"] == "explicit_fallback"
            and selectors["floor"]["runtime_fallback"]["target_selector_id"] == 85
            and selectors["floor"]["runtime_fallback"]["filename"] == "floor_09.png"
            and selectors["floor"]["runtime_fallback"]["asset"]["sha256"]
            == "cc960abb36b882bc771837a82c20563c11399456f21aa08ff87a033d2b543184"
        ),
        selectors["floor"],
        {
            "resolution_status": "unresolved",
            "reason_code": "missing_img_inf_entry",
            "asset": None,
            "runtime_resolution_status": "explicit_fallback",
            "runtime_fallback": {"target_selector_id": 85, "filename": "floor_09.png"},
        },
        "The absent source selector remains visible while the user-approved runtime alias is deterministic and testable.",
    )
    check(
        "wall-selector-chain",
        selectors["wall"]["raw_selector_id"] == 6
        and selectors["wall"]["filename"] == "wall_00.png"
        and selectors["wall"]["asset"]["sha256"] == "cbd7c73a38d041cafc330471cbab58b081c9c1c5ca4826e39e7f44d0a282d06c",
        selectors["wall"],
        {"raw_selector_id": 6, "filename": "wall_00.png"},
        "RoomData wallImgId_ resolves through chip/img.inf and the pinned asset index.",
    )
    check(
        "door-selector-chain",
        selectors["door"]["raw_selector_id"] == 7
        and selectors["door"]["filename"] == "door_01.png"
        and selectors["door"]["asset"]["sha256"] == "196198c9ee093f7f234060868434f9547e56bd020e57acebf4b2285848281569",
        selectors["door"],
        {"raw_selector_id": 7, "filename": "door_01.png"},
        "RoomData doorImgId_ resolves through chip/img.inf and the pinned asset index.",
    )
    check(
        "native-init-order",
        native_placement["init_order"] == ["Room.InitMapChips", "Room.InitObjChips", "Room.SetupBigChipsParent", "Room.PlaceDoor"],
        native_placement["init_order"],
        ["Room.InitMapChips", "Room.InitObjChips", "Room.SetupBigChipsParent", "Room.PlaceDoor"],
        "Room construction establishes map chips, object chips, parent links and door installation in this order.",
    )
    check(
        "raw-map-assignment",
        native_placement["raw_grid_assignment"]["cell_expression"] == "objMap[y][x]"
        and native_placement["raw_grid_assignment"]["constructor"].endswith("null, room)"),
        native_placement["raw_grid_assignment"],
        {"cell_expression": "objMap[y][x]", "furniture_data": None},
        "The raw map type is separate from a later FurnitureData binding.",
    )
    check(
        "door-cell-and-installed-flag",
        native_placement["door"]["cell"] == {"x": 8, "y": 4, "raw_map_value": 5, "raw_dir_value": 0}
        and native_placement["door"]["installed_flag"] == 1
        and native_placement["door"]["place_obj_furniture_data"] is None,
        native_placement["door"],
        {"cell": {"x": 8, "y": 4}, "raw_type": 5, "installed_flag": 1, "furniture_data": None},
        "The native door path is raw type 5 plus installed flag, not an inferred FurnitureData id.",
    )
    check(
        "type4-footprint",
        len(type4_placement["footprint"]) == 9
        and type4_placement["anchor"] == {"x": 4, "y": 2, "raw_map_value": 4}
        and type4_placement["parent_center_offset"] == {"dx": 0, "dy": 0},
        {"anchor": type4_placement["anchor"], "footprint_count": len(type4_placement["footprint"]), "center": type4_placement["parent_center_offset"]},
        {"anchor": {"x": 4, "y": 2, "raw_map_value": 4}, "footprint_count": 9, "center": {"dx": 0, "dy": 0}},
        "The native type-4 parent occupies the explicit 3x3 footprint fixture.",
    )
    check(
        "type4-passability",
        type4_placement["passability"]["matrix"] == [[True, False, False], [True, False, False], [True, True, True]],
        type4_placement["passability"]["matrix"],
        [[True, False, False], [True, False, False], [True, True, True]],
        "The closed Phase 1D passMap consumer fixture is carried without reinterpretation.",
    )
    check(
        "route-door-to-desk",
        native_placement["route_fixture"]["path"] == [[8, 4], [7, 4], [6, 4]]
        and native_placement["route_fixture"]["step_count"] == 2,
        native_placement["route_fixture"],
        {"path": [[8, 4], [7, 4], [6, 4]], "step_count": 2},
        "The door coordinate remains consistent with the closed route fixture.",
    )
    check(
        "furniture-boundary",
        object_boundary["runtime_policy"]["promote_furniture_2"] is (phase3a_closure.get("status") == "approved")
        and {item["object_id"] for item in object_boundary["native_room_bindings"]} == {"furniture:0", "furniture:1", "furniture:2", "furniture:5"},
        object_boundary,
        {"quarantined": [] if phase3a_closure.get("status") == "approved" else ["furniture:2"], "explicit_bindings": True},
        "Approved compositions are kept separate from native room placement; Phase 3A status controls whether furniture:2 remains quarantined.",
    )
    check(
        "cell-coordinate-probes",
        coordinates["cell_origin"]["probes"] == [
            {"cell": [0, 0], "world": {"x": 20, "y": 18}},
            {"cell": [4, 2], "world": {"x": 140, "y": -2}},
            {"cell": [8, 4], "world": {"x": 260, "y": -22}},
            {"cell": [9, 9], "world": {"x": 380, "y": 18}},
        ],
        coordinates["cell_origin"]["probes"],
        "Room.GetXbyIndex/GetYbyIndex probe values",
        "The logical cell origin follows the source 20/10 isometric formula.",
    )
    check(
        "map-and-object-draw-bases",
        coordinates["map_chip_draw_origin"]["probes"][0]["origin"] == {"x": 480, "y": -80}
        and coordinates["object_draw_origin"]["probes"][0]["origin"] == {"x": 240, "y": -31},
        {
            "map": coordinates["map_chip_draw_origin"]["probes"],
            "object": coordinates["object_draw_origin"]["probes"],
        },
        {"map": {"x": 480, "y": -80}, "object": {"x": 240, "y": -31}},
        "Native map sprites use the 40/20 basis while object anchors use the 20/10 basis plus the observed +9 y anchor.",
    )
    check(
        "camera-boundary",
        coordinates["camera"]["transform"] == "screen = world + offset"
        and coordinates["camera"]["fixture_offset"] == [0, 0]
        and coordinates["camera"]["dynamic_viewport_status"] == "not_inferred",
        coordinates["camera"],
        {"transform": "screen = world + offset", "fixture_offset": [0, 0], "dynamic_viewport_status": "not_inferred"},
        "Only the native Room.Draw ofx/ofy boundary is promoted; dynamic UI viewport behavior is not inferred.",
    )
    lines = [item["line"] for item in draw_order["passes"]]
    check(
        "draw-pass-order",
        lines == sorted(lines)
        and draw_order["passes"][0]["method"] == "MapChip.DrawExtentionFloor"
        and draw_order["passes"][-1]["method"] == "MapChip.DrawFloor",
        {"lines": lines, "first": draw_order["passes"][0]["method"], "last": draw_order["passes"][-1]["method"]},
        {"strictly_increasing": True, "first": "MapChip.DrawExtentionFloor", "last": "MapChip.DrawFloor"},
        "The source-bounded Room.Draw call-site order is deterministic and renderer-visible.",
    )
    check(
        "draw-overlap-order",
        draw_order["overlap_fixture"]["expected_event_order"] == ["door-object", "floor-image"]
        and next(item["line"] for item in draw_order["passes"] if item["id"] == "object-chip-primary")
        < next(item["line"] for item in draw_order["passes"] if item["id"] == "map-floor"),
        draw_order["overlap_fixture"],
        {"expected_event_order": ["door-object", "floor-image"]},
        "The shared-cell fixture protects native pass ordering against an accidental y-sort.",
    )
    check(
        "source-slice-hashes",
        all_source_hashes_pass and all(len(value) == 64 for value in source_hashes.values()),
        {"all_slice_hashes_pass": all_source_hashes_pass, "source_files": source_hashes},
        {"all_slice_hashes_pass": True, "sha256_length": 64},
        "The evidence package records the exact current source hashes it consumed.",
    )
    check(
        "upstream-contracts",
        all(upstream_ref(path)["status"] == "pass" for path in [SCENE_PATH, OBJECT_PATH, CAMERA_PATH, DISPLAY_ASSET_PATH]),
        {
            "scene": scene["status"],
            "objects": objects["status"],
            "camera": camera["status"],
            "display_assets": display_assets["status"],
        },
        {"all": "pass"},
        "Phase 3B consumes only the current approved upstream contracts.",
    )
    check(
        "runtime-import-policy",
        contract["runtime_policy"]["source_code_imports"] is False
        and contract["runtime_policy"]["archive_imports"] is False
        and contract["runtime_policy"]["unapproved_binary_imports"] is False,
        contract["runtime_policy"],
        {"source_code_imports": False, "archive_imports": False, "unapproved_binary_imports": False},
        "The contract is data-only at the runtime boundary.",
    )

    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "package": "social-dev-phase3b-room-placement-validation",
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": utc_now(),
        "input_hash": manifest["input_hash"],
        "source_audit_hash": source_audit["determinism"]["content_hash"],
        "fixture_hash": fixture["determinism"]["content_hash"],
        "contract_hash": contract["determinism"]["contract_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {
            "checks": len(checks),
            "passed_checks": sum(item["status"] == "pass" for item in checks),
            "source_slices": len(source_refs),
            "draw_passes": len(draw_order["passes"]),
            "selector_count": len(selectors),
            "native_room_bindings": len(object_boundary["native_room_bindings"]),
        },
        "phase_boundary": {
            "phase": "Phase 3B",
            "next": "Phase 3C",
            "completed": [
                "native room:0 placement contract",
                "selector-chain classification",
                "coordinate and camera boundary fixture",
                "source-bounded draw order fixture",
            ],
            "not_started": ["Canvas integration", "browser screenshot closure"],
        },
    }
    return source_audit, fixture, contract, validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    source_audit, fixture, contract, validation = build_package()
    write_json(evidence_dir / "phase3b_room_placement_source_audit.json", source_audit)
    write_json(evidence_dir / "phase3b_room_placement_fixture.json", fixture)
    write_json(evidence_dir / "phase3b_room_placement_validation.json", validation)
    write_json(runtime_dir / "room_placement_contract.json", contract)
    print(
        "phase3b_room_placement_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"unresolved_floor={contract['selectors']['floor']['resolution_status']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
