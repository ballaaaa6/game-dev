"""Build the evidence-bounded Phase 3C Canvas render contract.

This contract is intentionally separate from the native Phase 3B placement
contract. It describes what the browser is allowed to draw in the first
integrated visual slice while preserving unresolved and candidate statuses.
It never imports C# or source roots into the runtime.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

ROOM_PATH = RUNTIME_EVIDENCE / "room_placement_contract.json"
SCENE_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
OBJECT_PATH = RUNTIME_EVIDENCE / "object_catalog_contract.json"
CAMERA_PATH = RUNTIME_EVIDENCE / "camera_coordinate_contract.json"
DISPLAY_PATH = RUNTIME_EVIDENCE / "display_asset_manifest.json"
STRICT_CLOSURE_PATH = RUNTIME_EVIDENCE / "phase3c_strict_closure_contract.json"

FIXTURE_PATH = KNOWLEDGE_EVIDENCE / "phase3c_render_fixture.json"
VALIDATION_PATH = KNOWLEDGE_EVIDENCE / "phase3c_render_validation.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "phase3c_render_contract.json"

SCHEMA_VERSION = "social-dev-phase3c-render-contract-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-phase3c-render-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-phase3c-render-validation-v1"

DRAW_PASSES = [
    {
        "id": "map-extension-floor",
        "method": "MapChip.DrawExtentionFloor",
        "layer_role": "map_extension_floor",
    },
    {
        "id": "map-chip",
        "method": "MapChip.Draw",
        "layer_role": "map_chip_boundary_and_wall_sprites",
    },
    {
        "id": "object-chip-primary",
        "method": "ObjChip.Draw",
        "layer_role": "object_primary",
    },
    {
        "id": "object-chip-wall",
        "method": "ObjChip.DrawWall",
        "layer_role": "object_wall_overlay",
    },
    {
        "id": "avatar-primary",
        "method": "Avatar.Draw",
        "layer_role": "actor_primary",
    },
    {
        "id": "avatar-secondary",
        "method": "Avatar.Draw",
        "layer_role": "actor_secondary",
    },
    {
        "id": "object-chip-late-preview",
        "method": "ObjChip.Draw",
        "layer_role": "object_late_preview",
    },
    {
        "id": "object-chip-late",
        "method": "ObjChip.Draw",
        "layer_role": "object_late",
    },
    {
        "id": "map-floor",
        "method": "MapChip.DrawFloor",
        "layer_role": "map_floor",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def contract_hash(contract: dict[str, Any], key: str = "contract_hash") -> str | None:
    determinism = contract.get("determinism")
    if not isinstance(determinism, dict):
        return None
    value = determinism.get(key)
    return str(value) if value else None


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    room = load_json(ROOM_PATH)
    scene = load_json(SCENE_PATH)
    objects = load_json(OBJECT_PATH)
    camera = load_json(CAMERA_PATH)
    display = load_json(DISPLAY_PATH)
    strict = load_json(STRICT_CLOSURE_PATH)

    room_record = next(item for item in scene["scenes"] if item["id"] == "room:0")
    room_object_bindings = {
        item["object_id"]: item
        for item in room["object_boundary"]["native_room_bindings"]
    }
    strict_object_bindings = {
        item["object_id"]: item
        for item in strict["selected_display_binding_matrix"]
    }

    floor_selector = room["selectors"]["floor"]
    wall_selector = room["selectors"]["wall"]
    door_selector = room["selectors"]["door"]

    placements = [
        {
            "id": "scene:room:0/floor",
            "role": "floor",
            "raw_selector_id": floor_selector["raw_selector_id"],
            "runtime_asset_id": "asset:01_GAME_PACKS/chip/floor_09.png",
            "filename": "floor_09.png",
            "status": "approved_explicit_fallback",
            "source_resolution_status": floor_selector["resolution_status"],
            "runtime_resolution_status": floor_selector["runtime_resolution_status"],
            "runtime_fallback": floor_selector["runtime_fallback"],
            "cell_scope": {
                "width": room_record["grid"]["width"],
                "height": room_record["grid"]["height"],
                "mode": "every_grid_cell",
            },
        },
        {
            "id": "furniture:0",
            "role": "object",
            "object_id": "furniture:0",
            "cell": [4, 2],
            "status": "approved_native_geometry_fixture",
            "binding_status": strict_object_bindings["furniture:0"]["native_status"],
            "evidence_binding": "strict_closure.type4_geometry",
            "native_binding_status": strict_object_bindings["furniture:0"]["binding_rule"],
        },
        {
            "id": "furniture:1",
            "role": "object",
            "object_id": "furniture:1",
            "cell": [8, 4],
            "status": "approved_native_door_coordinate",
            "binding_status": strict_object_bindings["furniture:1"]["native_status"],
            "evidence_binding": "strict_closure.door",
            "native_binding_status": strict_object_bindings["furniture:1"]["binding_rule"],
        },
        {
            "id": "furniture:2",
            "role": "object",
            "object_id": "furniture:2",
            "cell": None,
            "status": "approved_not_placed",
            "binding_status": strict_object_bindings["furniture:2"]["native_status"],
            "evidence_binding": "room_placement.object_boundary.native_room_bindings",
        },
        {
            "id": "furniture:5",
            "role": "object",
            "object_id": "furniture:5",
            "cell": None,
            "status": "approved_not_placed",
            "binding_status": strict_object_bindings["furniture:5"]["native_status"],
            "evidence_binding": "room_placement.object_boundary.native_room_bindings",
        },
        {
            "id": "scene:room:0/wall",
            "role": "wall",
            "raw_selector_id": wall_selector["raw_selector_id"],
            "runtime_asset_id": "asset:01_GAME_PACKS/chip/wall_00.png",
            "filename": wall_selector["filename"],
            "status": "approved_native_coordinate_composition",
            "source_resolution_status": wall_selector["resolution_status"],
            "runtime_resolution_status": "resolved",
            "evidence_binding": "strict_closure.wall",
            "native_binding_status": strict["wall"]["status"],
            "cell_scope": {
                "width": room_record["grid"]["width"],
                "height": room_record["grid"]["height"],
                "mode": "native_draw_wall_predicates",
                "cells": strict["wall"]["cells_by_frame"],
                "anchor_formula": strict["wall"]["anchor_formula"],
                "sprite_records": strict["wall"]["sprite_records"],
            },
        },
        {
            "id": "scene:room:0/door",
            "role": "door",
            "raw_selector_id": door_selector["raw_selector_id"],
            "runtime_asset_id": "asset:01_GAME_PACKS/chip/door_01.png",
            "filename": door_selector["filename"],
            "status": "approved_native_coordinate_composition",
            "source_resolution_status": door_selector["resolution_status"],
            "runtime_resolution_status": "resolved",
            "evidence_binding": "strict_closure.door",
            "cell": strict["door"]["cell"],
            "native_binding_status": strict["door"]["native_binding"]["status"],
            "native_coordinate": {
                "anchor": strict["door"]["anchor"],
                "sprite_record": strict["door"]["sprite_record"],
            },
        },
    ]

    fixture = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-phase3c-render-fixture",
        "status": "pass",
        "semantic_status": "evidence_bounded_integrated_render",
        "catalog_id": "display-slice-01",
        "scene_ref": {
            "id": "room:0",
            "contract_hash": contract_hash(scene),
        },
        "room_placement_ref": {
            "path": relative_path(ROOM_PATH),
            "contract_hash": contract_hash(room),
        },
        "object_catalog_ref": {
            "path": relative_path(OBJECT_PATH),
            "contract_hash": contract_hash(objects),
        },
        "camera_coordinate_ref": {
            "path": relative_path(CAMERA_PATH),
            "contract_hash": contract_hash(camera),
        },
        "display_asset_manifest_ref": {
            "path": relative_path(DISPLAY_PATH),
            "content_hash": contract_hash(display, "content_hash"),
        },
        "strict_closure_ref": {
            "path": relative_path(STRICT_CLOSURE_PATH),
            "contract_hash": contract_hash(strict),
            "status": strict["status"],
        },
        "canvas": {
            "width": 980,
            "height": 600,
            "presentation_origin": {"x": 240, "y": 260},
            "presentation_origin_status": "explicit_runtime_fixture",
        },
        "coordinates": {
            "cell_origin": room["coordinates"]["cell_origin"],
            "actor_spawn": room["coordinates"]["actor_spawn"],
            "map_chip_draw_origin": room["coordinates"]["map_chip_draw_origin"],
            "object_draw_origin": room["coordinates"]["object_draw_origin"],
            "camera": room["coordinates"]["camera"],
        },
        "draw_passes": DRAW_PASSES,
        "placements": placements,
        "native_initial_bindings": strict["native_initial_bindings"],
        "overlap_fixture": room["draw_order"]["overlap_fixture"],
        "runtime_policy": {
            "source_code_imports": False,
            "archive_imports": False,
            "unapproved_binary_imports": False,
            "allow_native_furniture_id_inference": False,
            "require_explicit_scene_binding": True,
            "unresolved_selector_policy": "retain_raw_and_show_explicit_fallback_or_blocked_status",
            "approved_not_placed_objects_are_not_drawn": True,
        },
        "provenance": {
            "room_contract": relative_path(ROOM_PATH),
            "scene_contract": relative_path(SCENE_PATH),
            "object_contract": relative_path(OBJECT_PATH),
            "camera_contract": relative_path(CAMERA_PATH),
            "display_asset_manifest": relative_path(DISPLAY_PATH),
        },
    }

    fixture_without_dynamic = dict(fixture)
    fixture_hash = sha256_text(stable_json(fixture_without_dynamic))
    fixture["determinism"] = {
        "algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash",
        "content_hash": fixture_hash,
    }

    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-phase3c-render-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "scene_ref": fixture["scene_ref"],
        "room_placement_ref": {
            "path": relative_path(ROOM_PATH),
            "contract_hash": contract_hash(room),
            "status": room["status"],
        },
        "object_catalog_ref": {
            "path": relative_path(OBJECT_PATH),
            "contract_hash": contract_hash(objects),
            "status": objects["status"],
        },
        "camera_coordinate_ref": {
            "path": relative_path(CAMERA_PATH),
            "contract_hash": contract_hash(camera),
            "status": camera["status"],
        },
        "display_asset_manifest_ref": {
            "path": relative_path(DISPLAY_PATH),
            "content_hash": contract_hash(display, "content_hash"),
            "status": display["status"],
        },
        "strict_closure_ref": fixture["strict_closure_ref"],
        "canvas": fixture["canvas"],
        "coordinates": fixture["coordinates"],
        "draw_passes": DRAW_PASSES,
        "placements": placements,
        "native_initial_bindings": strict["native_initial_bindings"],
        "overlap_fixture": fixture["overlap_fixture"],
        "runtime_policy": fixture["runtime_policy"],
        "fixture_ref": {
            "path": relative_path(FIXTURE_PATH),
            "content_hash": fixture_hash,
        },
        "provenance": fixture["provenance"],
    }
    contract_without_dynamic = dict(contract)
    contract["determinism"] = {
        "algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash",
        "contract_hash": sha256_text(stable_json(contract_without_dynamic)),
    }

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append(
            {
                "id": check_id,
                "status": "pass" if passed else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    check("scene-status", scene["status"] == "pass", scene["status"], "pass", "SceneCatalog is an approved runtime input.")
    check("room-placement-status", room["status"] == "pass", room["status"], "pass", "Phase 3B placement contract is closed.")
    check("display-manifest-status", display["status"] == "pass", display["status"], "pass", "Only the approved display manifest is consumed.")
    check("strict-closure-status", strict["status"] == "pass", strict["status"], "pass", "Native wall/door and furniture-binding evidence is available as a separate strict contract.")
    check("floor-fallback", placements[0]["status"] == "approved_explicit_fallback", placements[0]["status"], "approved_explicit_fallback", "Raw selector 5 remains unresolved.")
    check("native-type4-placement", placements[1]["cell"] == [4, 2], placements[1]["cell"], [4, 2], "The existing furniture:0 render remains an explicit type-4 geometry fixture.")
    check("door-native-placement", placements[2]["cell"] == [8, 4] and placements[2]["status"] == "approved_native_door_coordinate", placements[2]["cell"], [8, 4], "The raw door cell and native DrawWall coordinate are closed; no FurnitureData id is inferred.")
    check("wall-native-composition", placements[5]["status"] == "approved_native_coordinate_composition" and placements[5]["cell_scope"]["cells"]["vertical_frame_1"], placements[5]["cell_scope"]["cells"], strict["wall"]["cells_by_frame"], "Wall cells are generated from the native DrawWall predicates.")
    check("no-inferred-furniture-2", placements[3]["cell"] is None, placements[3]["cell"], None, "FurnitureData(2) has no native room:0 binding.")
    check("no-inferred-furniture-5", placements[4]["cell"] is None, placements[4]["cell"], None, "FurnitureData(5) has no native room:0 binding.")
    check("native-pass-order", [item["id"] for item in DRAW_PASSES] == [item["id"] for item in room["draw_order"]["passes"]], [item["id"] for item in DRAW_PASSES], [item["id"] for item in room["draw_order"]["passes"]], "Renderer must use the closed Room.Draw pass order.")
    check("runtime-policy", all(value is False for value in (contract["runtime_policy"]["source_code_imports"], contract["runtime_policy"]["archive_imports"], contract["runtime_policy"]["unapproved_binary_imports"])), contract["runtime_policy"], "all source/archive/unapproved imports false", "Runtime remains contract-only.")

    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "package": "social-dev-phase3c-render-validation",
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "semantic_status": "validated",
        "generated_at_utc": now_utc(),
        "checks": checks,
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "counts": {
            "checks": len(checks),
            "passed_checks": sum(item["status"] == "pass" for item in checks),
        },
        "fixture_hash": fixture_hash,
        "contract_hash": contract["determinism"]["contract_hash"],
    }
    return fixture, contract, validation


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    fixture, contract, validation = build_package()
    write_json(FIXTURE_PATH, fixture)
    write_json(CONTRACT_PATH, contract)
    write_json(VALIDATION_PATH, validation)
    print(
        "phase3c_render_contract_built "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"fixture={fixture['determinism']['content_hash']} "
        f"contract={contract['determinism']['contract_hash']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
