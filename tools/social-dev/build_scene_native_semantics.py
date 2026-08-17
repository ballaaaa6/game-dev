"""Build normalized native semantics evidence for the Social Dev scene slice.

The facts in ``scene_native_semantics_facts.py`` were reviewed against the
current APK's IL2CPP method bodies.  This builder adds current-artifact hashes,
source anchors and the FurnitureData fixture inventory.  It creates evidence
only; it does not execute decompiled C# or native code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_semantics_review as semantics
import scene_native_semantics_facts as facts


ROOT = semantics.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
SOURCE_ROOT = semantics.SOURCE_ROOT
APK_PATH = ROOT / facts.APK_RELATIVE_PATH
SCENE_INPUT = EVIDENCE / "scene_data_candidate.json"
SCHEMA_VERSION = "social-dev-scene-native-semantics-v1"
VALIDATION_VERSION = "social-dev-scene-native-semantics-validation-v1"

SOURCE_FILES = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_line(path: Path, needle: str, note: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            return {
                "file": relative_path(path),
                "line_start": index + 1,
                "line_end": index + 1,
                "source_sha256": sha256_file(path),
                "needle": needle,
                "note": note,
            }
    raise ValueError(f"source marker not found: {relative_path(path)}::{needle}")


def source_lines(path: Path, start_needle: str, end_needle: str, note: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next(index for index, line in enumerate(lines) if start_needle in line)
    end = next(index for index in range(start + 1, len(lines)) if end_needle in lines[index])
    return {
        "file": relative_path(path),
        "line_start": start + 1,
        "line_end": end,
        "source_sha256": sha256_file(path),
        "start_needle": start_needle,
        "end_needle": end_needle,
        "note": note,
    }


def native_ref(method_id: str) -> dict[str, Any]:
    for method in facts.NATIVE_METHODS:
        if method["id"] == method_id:
            return dict(method)
    raise KeyError(method_id)


def source_ref(key: str, needle: str, note: str) -> dict[str, Any]:
    return source_line(SOURCE_FILES[key], needle, note)


def source_span(key: str, start_needle: str, end_needle: str, note: str) -> dict[str, Any]:
    return source_lines(SOURCE_FILES[key], start_needle, end_needle, note)


def furniture_fixture() -> dict[str, Any]:
    _, summary = semantics.furniture_profiles()
    candidates = [
        profile
        for profile in summary["non_empty_pass_map_records"]
        if profile.get("type_candidate") == 4
    ]
    if not candidates:
        raise ValueError("no non-empty type-4 FurnitureData passMap candidate")
    candidate = candidates[0]
    return {
        "status": "candidate_ready_for_normalized_fixture",
        "reason": "type 4 is the native multi-chip/passMap consumer path",
        "record": candidate,
        "remaining_normalization": [
            "derive the exact dx_/dy_ anchor for one placed 3x3 object",
            "resolve the loop-dependent boolean return with a fixture",
        ],
        "inventory_summary": {
            "total_ids": summary["total_ids"],
            "non_empty_pass_map_count": summary["non_empty_pass_map_count"],
            "parse_error_count": summary["parse_error_count"],
            "missing_locale_count": summary["missing_locale_count"],
        },
    }


def build_claims() -> list[dict[str, Any]]:
    return [
        {
            "id": "objmap-to-objchip-type",
            "status": "native_observed",
            "promotable_to_contract": True,
            "claim": "Room.InitObjChips reads RoomData.objMap_[y][x], passes that raw integer as the ObjChip constructor type argument, supplies furnitureData=null and the Room reference, then stores the chip at flat index x + y * width.",
            "contract": {
                "raw_cell": "objMap[y][x]",
                "constructor": "new ObjChip(x, y, rawCell, null, room)",
                "flat_index": "x + y * objMapWidth_",
            },
            "native_refs": [native_ref("room-init-obj-chips"), native_ref("objchip-constructor")],
            "source_refs": [source_span("Room", "private void InitObjChips(RoomData roomData)", "private void SetupBigChipsParent()", "decompiler-bounded source counterpart")],
            "limits": "The current C# decompiler rendering is damaged; the native body is the assignment evidence.",
        },
        {
            "id": "door-binding",
            "status": "contract_ready",
            "promotable_to_contract": True,
            "claim": "The raw map value 5 becomes ObjChip type 5; Room.PlaceDoor scans that type, calls the door placement path and sets the installed flag.",
            "contract": {"door_type": 5, "door_cells_source": "RoomData.objMap", "installed_flag": 1},
            "native_refs": [native_ref("room-init-obj-chips"), native_ref("room-place-door")],
            "source_refs": [
                source_ref("Room", "if (objChip.type_ != 5)", "door scan predicate"),
                source_ref("Room", "objChip.flag_ = num2;", "door installation flag write"),
            ],
            "limits": "The exact FurnitureData record selected for the door asset remains an asset-selector review item.",
        },
        {
            "id": "standing-positions",
            "status": "contract_ready",
            "promotable_to_contract": True,
            "claim": "ObjChip.GetStandingPositions returns four deterministic screen positions from the chip index using the native formulas and fixed order.",
            "contract": facts.STANDING_POSITIONS,
            "native_refs": [native_ref("objchip-standing-positions")],
            "source_refs": [source_span("ObjChip", "public Vector2D[] GetStandingPositions()", "public bool HasInstalled()", "decompiler-damaged source counterpart")],
            "limits": "Camera offset, draw depth and sprite anchor are separate renderer contracts.",
        },
        {
            "id": "furniture-placement-model",
            "status": "native_observed_bounded",
            "promotable_to_contract": True,
            "promotable_to_canonical_catalog": False,
            "claim": "Furniture placement is a second layer over the objMap type grid: ObjChip.PlaceObj binds FurnitureData, while Room.PlaceDesk and AppData.NewGame select initial records by furniture flags and consume empty chips.",
            "contract": facts.FURNITURE_PLACEMENT_MODEL,
            "native_refs": [
                native_ref("objchip-place-object"),
                native_ref("room-place-desk"),
                native_ref("appdata-new-game"),
            ],
            "source_refs": [
                source_span("ObjChip", "public void PlaceObj(FurnitureData furnitureData)", "public void DecideDirection()", "ObjChip binding and orientation source"),
                source_span("Room", "public void PlaceDesk(int num)", "public int GetDesksNum()", "initial desk placement source"),
                source_ref("AppData", "player.rooms_.AddElement(room);", "initial room and type-1 chip setup"),
                source_ref("AppData", "bool flag115 = ((BaseData)(object)text).Check(32768);", "initial-place furniture flag"),
                source_ref("FurnitureData", "public const int FLAG_INIT_DESK = 16384;", "desk selector flag"),
                source_ref("FurnitureData", "public const int FLAG_INIT_PLACE = 32768;", "initial-place selector flag"),
            ],
            "limits": "This closes the placement model, not the final asset/catalog mapping for every selected FurnitureData id.",
        },
        {
            "id": "passmap-consumer",
            "status": "native_observed_bounded",
            "promotable_to_contract": False,
            "claim": "ObjChip.IsPassable consumes FurnitureData.passMap_ through a native 3x3 window derived from dx_/dy_; zero-cell handling and the null-furniture fallback are visible, but the final boolean meaning still needs a normalized fixture.",
            "contract": facts.PASSMAP_CONSUMER,
            "native_refs": [native_ref("objchip-is-passable")],
            "source_refs": [
                source_span("ObjChip", "public bool IsPassable()", "public int GetDeskDir()", "passability source counterpart"),
                source_ref("FurnitureData", "public int[][] passMap_;", "passMap field"),
            ],
            "limits": "Do not infer passable/blocked from passMap values alone until the loop-dependent return and type 3/4 fallback are exercised by a fixture.",
        },
        {
            "id": "neighbor-policy",
            "status": "contract_ready",
            "promotable_to_contract": True,
            "claim": "Astar.AddNeighbor connects only the four cardinal neighbors; the four corners and center of the 3x3 candidate window are excluded.",
            "contract": facts.NEIGHBOR_POLICY,
            "native_refs": [native_ref("astar-connect-neighbors"), native_ref("astar-add-neighbor")],
            "source_refs": [
                source_span("Astar", "private void ConnectNeighbors(Room room)", "public Node GetNode(int x, int y, Room room)", "neighbor construction source counterpart"),
            ],
            "limits": "This is connectivity policy only; route goal selection and passability remain separate gates.",
        },
        {
            "id": "route-filter",
            "status": "bounded_candidate",
            "promotable_to_contract": False,
            "claim": "The readable Astar source filters occupied type-2 chips, non-passable type-3/4 chips and type-6 outdoor chips while evaluating neighbors.",
            "contract": facts.ROUTE_FILTER,
            "native_refs": [native_ref("astar-search-route")],
            "source_refs": [
                source_ref("Astar", "bool flag20 = objChip.IsPassable();", "route passability call"),
                source_span("Astar", "private bool _searchRoute(int startX, int startY, int goalX, int goalY, Room room, FastVector route)", "private void ConnectNeighbors(Room room)", "route filter source counterpart"),
            ],
            "limits": "The native _searchRoute function boundary was noisy in Ghidra, so this remains bounded source evidence until the route fixture confirms it.",
        },
    ]


def build_package() -> tuple[dict[str, Any], dict[str, Any]]:
    scene = load_json(SCENE_INPUT)
    room = scene["room"]
    fixture = furniture_fixture()
    source_inputs = [SCENE_INPUT, APK_PATH, *SOURCE_FILES.values()]
    input_manifest = [
        {"file": relative_path(path), "sha256": sha256_file(path)}
        for path in source_inputs
    ]
    claims = build_claims()
    closed = [
        claim["id"]
        for claim in claims
        if claim.get("promotable_to_contract") is True
    ]
    remaining = [
        {
            "id": "passmap-boolean-normalization",
            "status": "blocking",
            "reason": "Resolve native loop-dependent return and null-furniture fallback with a type-4 9x9 fixture.",
            "fixture_candidate": fixture["record"]["id"],
        },
        {
            "id": "route-goal-filter",
            "status": "blocking",
            "reason": "Prove the actual goal predicate/selection; raw objMap value 2 remains only a candidate.",
        },
        {
            "id": "furniture-canonical-selector",
            "status": "non_blocking_for_model",
            "reason": "Resolve seb_/img_/subSeb_ mapping before promoting a final visual catalog.",
        },
    ]
    package = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-scene-native-semantics",
        "status": "candidate",
        "semantic_status": "pending_fixture_review",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_artifact": {
            "apk": relative_path(APK_PATH),
            "apk_sha256": sha256_file(APK_PATH),
            "il2cpp_metadata_version": facts.IL2CPP_METADATA_VERSION,
            "architecture": facts.NATIVE_EXTRACTION_RECIPE["architecture"],
            "extraction_recipe": facts.NATIVE_EXTRACTION_RECIPE,
        },
        "input_manifest": input_manifest,
        "native_method_manifest": facts.NATIVE_METHODS,
        "scene_reference": {
            "room_type": room["type"],
            "room_id": room["id"],
            "grid_shape": room["grid_shape"],
            "door_cells": [
                {"x": x, "y": y, "raw_map_value": raw}
                for y, row in enumerate(room["objMap"])
                for x, raw in enumerate(row)
                if raw == 5
            ],
            "raw_map_domain": sorted({raw for row in room["objMap"] for raw in row}),
        },
        "claims": claims,
        "closed_contract_gates": closed,
        "fixture": fixture,
        "route": {
            "status": "blocked_on_fixture_semantics",
            "cleared_gates": [
                "objMap_to_ObjChip.type_",
                "standing_positions",
                "neighbor_policy",
                "bounded_furniture_placement_model",
            ],
            "remaining_gates": ["passmap_boolean_normalization", "route_goal_filter"],
            "node_grid": {
                "width": room["grid_shape"]["objMap_width"],
                "height": room["grid_shape"]["objMap_height"],
                "connectivity": facts.NEIGHBOR_POLICY["connectivity"],
            },
            "no_path_emitted": True,
        },
        "remaining_review": remaining,
        "evidence_limits": [
            "Native evidence is used to build contracts; it is not executed in the web runtime.",
            "A method RVA is valid only for the recorded APK hash.",
            "C# source remains useful as a readable cross-check but does not override native evidence when decompiler output is damaged.",
        ],
    }
    checks = [
        {"id": "apk-present", "status": "pass" if APK_PATH.is_file() else "fail", "observed": relative_path(APK_PATH)},
        {"id": "apk-hash", "status": "pass" if len(package["source_artifact"]["apk_sha256"]) == 64 else "fail", "observed": package["source_artifact"]["apk_sha256"]},
        {"id": "method-refs-unique", "status": "pass" if len({item["id"] for item in facts.NATIVE_METHODS}) == len(facts.NATIVE_METHODS) else "fail", "observed": len(facts.NATIVE_METHODS)},
        {"id": "objmap-contract", "status": "pass" if "objMap[y][x]" in claims[0]["contract"]["raw_cell"] and claims[0]["promotable_to_contract"] else "fail", "observed": claims[0]["contract"]},
        {"id": "standing-contract", "status": "pass" if len(facts.STANDING_POSITIONS["order"]) == 4 else "fail", "observed": facts.STANDING_POSITIONS},
        {"id": "cardinal-neighbors", "status": "pass" if facts.NEIGHBOR_POLICY["connectivity"] == 4 and not facts.NEIGHBOR_POLICY["corners_included"] else "fail", "observed": facts.NEIGHBOR_POLICY},
        {"id": "passmap-fixture", "status": "pass" if fixture["record"]["type_candidate"] == 4 and fixture["record"]["passMap_non_empty"] else "fail", "observed": fixture["record"]["id"]},
        {"id": "route-not-promoted", "status": "pass" if package["route"]["status"] == "blocked_on_fixture_semantics" and package["route"]["no_path_emitted"] else "fail", "observed": package["route"]},
    ]
    validation = {
        "schema_version": VALIDATION_VERSION,
        "status": "pass" if all(check["status"] == "pass" for check in checks) else "fail",
        "semantic_status": package["semantic_status"],
        "generated_at_utc": package["generated_at_utc"],
        "input_hash": hashlib.sha256(stable_json(input_manifest).encode("utf-8")).hexdigest(),
        "failed_checks": [check["id"] for check in checks if check["status"] != "pass"],
        "checks": checks,
        "counts": {
            "native_methods": len(facts.NATIVE_METHODS),
            "claims": len(claims),
            "closed_contract_gates": len(closed),
            "remaining_review_items": len(remaining),
            "pass_map_fixture_id": fixture["record"]["id"],
        },
    }
    return package, validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=EVIDENCE)
    args = parser.parse_args()
    package, validation = build_package()
    write_json(args.output_dir / "scene_native_semantics.json", package)
    write_json(args.output_dir / "scene_native_semantics_validation.json", validation)
    print(
        "scene_native_semantics_complete "
        f"status={validation['status']} "
        f"methods={validation['counts']['native_methods']} "
        f"claims={validation['counts']['claims']} "
        f"closed={validation['counts']['closed_contract_gates']} "
        f"fixture={validation['counts']['pass_map_fixture_id']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
