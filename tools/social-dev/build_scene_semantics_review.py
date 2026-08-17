"""Build bounded scene-semantics evidence for the Social Dev display slice.

This tool consumes the Phase 1B candidate package and re-reads the current
read-only C# source/table evidence. It records what is source-observed versus
what remains blocked by decompiler damage; it never creates a runtime catalog
and never executes the recovered C#.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_behavior_candidates as base
import scene_native_semantics_facts as native_facts


ROOT = base.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
SOURCE_ROOT = base.SOURCE_ROOT

INPUT_SCENE = EVIDENCE / "scene_data_candidate.json"
INPUT_FIRST_SLICE = EVIDENCE / "first_slice_data_candidate.json"
FIELD_LOAD = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG = EVIDENCE / "csharp_update_inventory/type_catalog.json"

SOURCE_FILES = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "MapChip": SOURCE_ROOT / "game/MapChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
    "Node": SOURCE_ROOT / "game.routeSearch/Node.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
}

SELECTED_FURNITURE_IDS = [1, 2, 5]
SCHEMA_VERSION = "social-dev-scene-semantics-review-v1"
VALIDATION_VERSION = "social-dev-scene-semantics-validation-v1"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def find_marker(lines: list[str], marker: str, start_index: int = 0) -> int:
    for index in range(start_index, len(lines)):
        if marker in lines[index]:
            return index
    raise ValueError(f"marker not found: {marker}")


def source_span(
    key: str,
    start_marker: str,
    end_marker: str,
    purpose: str,
    status: str = "evidence_only",
) -> dict[str, Any]:
    path = SOURCE_FILES[key]
    lines = source_lines(path)
    start_index = find_marker(lines, start_marker)
    end_index = find_marker(lines, end_marker, start_index + 1)
    text = "".join(lines[start_index:end_index])
    return {
        "id": purpose.replace(" ", "-"),
        "type": key,
        "file": relative_path(path),
        "line_start": start_index + 1,
        "line_end": end_index,
        "purpose": purpose,
        "slice_sha256": sha256_bytes(text.encode("utf-8")),
        "file_sha256": sha256_file(path),
        "il_marker_count": text.count("//IL_"),
        "status": status,
    }


def source_line_ref(key: str, needle: str, note: str) -> dict[str, Any]:
    path = SOURCE_FILES[key]
    lines = source_lines(path)
    line_index = find_marker(lines, needle)
    return {
        "file": relative_path(path),
        "line_start": line_index + 1,
        "line_end": line_index + 1,
        "source_hash": sha256_file(path),
        "needle": needle,
        "note": note,
    }


def value(record: dict[str, Any], field: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(field, {}).get("value", default)


def shape(value_: Any) -> list[int] | None:
    if value_ is None:
        return None
    if not isinstance(value_, list):
        return []
    return [len(row) if isinstance(row, list) else -1 for row in value_]


def furniture_profiles() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    field_load = load_json(FIELD_LOAD)
    type_catalog = load_json(TYPE_CATALOG)
    field_load_row = base.find_field_load(field_load["rows"], "FurnitureData")
    type_source = base.find_type_source(type_catalog["records"], "FurnitureData")
    parsed_by_locale: dict[str, list[dict[str, Any]]] = {}
    for locale in ("English", "Japanese"):
        table = base.table_path("FurnitureData", locale)
        parsed_by_locale[locale] = [
            base.parse_row(
                "FurnitureData",
                locale,
                row,
                field_load_row,
                type_source,
                table,
            )
            for row in base.read_table(table)
        ]

    english = {record["id"]: record for record in parsed_by_locale["English"]}
    japanese = {record["id"]: record for record in parsed_by_locale["Japanese"]}
    ids = sorted(set(english) | set(japanese))
    profiles: list[dict[str, Any]] = []
    parse_errors: list[dict[str, Any]] = []
    non_empty_pass_map: list[dict[str, Any]] = []
    for row_id in ids:
        en = english.get(row_id)
        ja = japanese.get(row_id)
        if en is None or ja is None:
            profiles.append(
                {
                    "id": row_id,
                    "locale_alignment": "missing_locale_row",
                    "english_present": en is not None,
                    "japanese_present": ja is not None,
                }
            )
            continue
        if en["parse"]["status"] != "pass" or ja["parse"]["status"] != "pass":
            parse_errors.extend(
                record
                for record in (en, ja)
                if record["parse"]["status"] != "pass"
            )
        pass_map = value(en, "passMap_")
        profile = {
            "id": row_id,
            "name_english": value(en, "name_"),
            "name_japanese": value(ja, "name_"),
            "type_candidate": value(en, "type_"),
            "passMap_candidate": pass_map,
            "passMap_shape": shape(pass_map),
            "passMap_non_empty": bool(pass_map),
            "locale_alignment": {
                "english_row": en["row_number"],
                "japanese_row": ja["row_number"],
                "english_columns": en["column_count"],
                "japanese_columns": ja["column_count"],
                "same_column_count": en["column_count"] == ja["column_count"],
            },
            "provenance": {
                "english": {
                    "table_path": en["table_path"],
                    "row_number": en["row_number"],
                    "row_sha256": en["row_sha256"],
                },
                "japanese": {
                    "table_path": ja["table_path"],
                    "row_number": ja["row_number"],
                    "row_sha256": ja["row_sha256"],
                },
            },
        }
        profiles.append(profile)
        if profile["passMap_non_empty"]:
            non_empty_pass_map.append(profile)

    return profiles, {
        "total_ids": len(ids),
        "english_rows": len(parsed_by_locale["English"]),
        "japanese_rows": len(parsed_by_locale["Japanese"]),
        "parse_error_count": len(parse_errors),
        "missing_locale_count": sum(1 for profile in profiles if profile["locale_alignment"] == "missing_locale_row"),
        "non_empty_pass_map_count": len(non_empty_pass_map),
        "non_empty_pass_map_records": non_empty_pass_map,
        "selected_profiles": [
            profile for profile in profiles if profile.get("id") in SELECTED_FURNITURE_IDS
        ],
        "parse_errors": [
            {
                "locale": record["locale"],
                "id": record["id"],
                "row_number": record["row_number"],
                "errors": record["parse"]["errors"],
            }
            for record in parse_errors
        ],
    }


def build_source_slices() -> list[dict[str, Any]]:
    return [
        source_span(
            "Room",
            "private void InitObjChips(RoomData roomData)",
            "private void SetupBigChipsParent()",
            "room object-grid construction",
            "decompiler_bounded",
        ),
        source_span(
            "Room",
            "private void PlaceDoor()",
            "private void InitStaffs(RoomData roomData)",
            "door scan and installation flag",
            "decompiler_bounded",
        ),
        source_span(
            "Room",
            "public static int GetXbyIndex(int ix, int iy)",
            "public Vector2D GetDoorIndex()",
            "index-to-screen coordinate formulas",
        ),
        source_span(
            "ObjChip",
            "public const int OBJ_TYPE_PASS = 0;",
            "public const int OBJ_TYPE_OUTDOOR = 6;",
            "object type constant domain",
        ),
        source_span(
            "ObjChip",
            "public Vector2D[] GetStandingPositions()",
            "public bool HasInstalled()",
            "standing-position method",
            "decompiler_damaged",
        ),
        source_span(
            "ObjChip",
            "public bool IsPassable()",
            "public int GetDeskDir()",
            "passability method",
            "decompiler_damaged",
        ),
        source_span(
            "Astar",
            "public unsafe void AddNodeArray(Room room)",
            "public void RemoveNodeArray(int routeNodeArrayId)",
            "route node-grid construction",
            "decompiler_bounded",
        ),
        source_span(
            "Astar",
            "private void ConnectNeighbors(Room room)",
            "private void AddNeighbor(int nodeX, int nodeY, Room room)",
            "neighbor sweep",
            "decompiler_bounded",
        ),
        source_span(
            "Astar",
            "private void AddNeighbor(int nodeX, int nodeY, Room room)",
            "public Node GetNode(int x, int y, Room room)",
            "neighbor candidate construction",
            "decompiler_damaged",
        ),
        source_span(
            "Astar",
            "private bool _searchRoute(int startX, int startY, int goalX, int goalY, Room room, FastVector route)",
            "private void ConnectNeighbors(Room room)",
            "route search and passability hook",
            "decompiler_damaged",
        ),
        source_span(
            "Node",
            "public void CalculateCost(Node goal)",
            "public void SetPosition(int x, int y)",
            "Manhattan g/h cost",
        ),
        source_span(
            "FurnitureData",
            "public class FurnitureData : BaseData",
            "public override void NewGame()",
            "furniture field/load boundary",
            "decompiler_bounded",
        ),
    ]


def build_observations(scene: dict[str, Any], source_slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_purpose = {item["purpose"]: item for item in source_slices}
    return [
        {
            "id": "room-grid-shape",
            "status": "native_observed",
            "claim": "Room.InitObjChips derives objMapWidth_/objMapHeight_ from RoomData.objMap_, passes each raw objMap[y][x] cell as ObjChip.type_, and stores one ObjChip per grid cell at x + y * width.",
            "limits": "The current C# body remains decompiler-damaged; the native method body closes the raw-cell assignment.",
            "source_refs": [by_purpose["room object-grid construction"]],
            "superseding_evidence": "scene_native_semantics.json#objmap-to-objchip-type",
        },
        {
            "id": "door-scan-type-five",
            "status": "contract_ready",
            "claim": "Room.PlaceDoor scans ObjChip.type_ for literal 5, calls PlaceObj for the matching chip, and sets the installed flag; native InitObjChips proves raw RoomData.objMap_ value 5 becomes type 5.",
            "limits": "The exact FurnitureData record selected for the door asset remains an asset-selector review item.",
            "source_refs": [
                by_purpose["door scan and installation flag"],
                source_line_ref("Room", "if (objChip.type_ != 5)", "door scan predicate"),
                source_line_ref("Room", "objChip.flag_ = num2;", "door installation flag write"),
            ],
            "superseding_evidence": "scene_native_semantics.json#door-binding",
        },
        {
            "id": "object-code-domain",
            "status": "source_observed",
            "claim": "ObjChip declares source-labeled constants for values 0 through 6, including door value 5 and outdoor value 6.",
            "limits": "Constant names are retained as source labels and are not treated as a complete map-code contract.",
            "source_refs": [by_purpose["object type constant domain"]],
        },
        {
            "id": "coordinate-projection",
            "status": "source_observed",
            "claim": "Room.GetXbyIndex/GetYbyIndex use the isometric projection formulas already captured in Phase 1B.",
            "limits": "Camera offset, draw depth and asset anchor are separate contracts.",
            "source_refs": [by_purpose["index-to-screen coordinate formulas"]],
        },
        {
            "id": "route-node-grid",
            "status": "bounded_candidate",
            "claim": "Astar.AddNodeArray uses room grid dimensions, assigns node grid indices/positions and calls ConnectNeighbors.",
            "limits": "The construction body contains decompiler damage, so node field orientation and all initialization details remain bounded observations.",
            "source_refs": [by_purpose["route node-grid construction"]],
        },
        {
            "id": "neighbor-topology",
            "status": "native_observed",
            "claim": "ConnectNeighbors sweeps the room grid and native AddNeighbor connects only west/east/north/south; center and all four corners are excluded.",
            "limits": "Out-of-bounds handling is represented as GetNode skip behavior; passability remains a separate route gate.",
            "source_refs": [
                by_purpose["neighbor sweep"],
                by_purpose["neighbor candidate construction"],
            ],
            "superseding_evidence": "scene_native_semantics.json#neighbor-policy",
        },
        {
            "id": "manhattan-cost",
            "status": "source_observed",
            "claim": "Node.MANHATTAN is true and CalculateCost computes absolute row/column deltas for g/h costs.",
            "limits": "The heuristic/cost rule does not by itself establish passability or route correctness.",
            "source_refs": [
                by_purpose["Manhattan g/h cost"],
                source_line_ref("Node", "public const bool MANHATTAN = true;", "Manhattan source constant"),
            ],
        },
        {
            "id": "passability-gate",
            "status": "native_observed_bounded",
            "claim": "Astar._searchRoute invokes ObjChip.IsPassable while evaluating neighboring cells, and native IsPassable consumes a FurnitureData.passMap_ 3x3 window derived from dx_/dy_.",
            "limits": "The final boolean meaning of the passMap branch and the type 3/4 null-furniture fallback still require a normalized fixture.",
            "source_refs": [
                by_purpose["route search and passability hook"],
                source_line_ref("Astar", "bool flag20 = objChip.IsPassable();", "route passability call"),
                by_purpose["passability method"],
            ],
            "superseding_evidence": "scene_native_semantics.json#passmap-consumer",
        },
        {
            "id": "furniture-pass-map",
            "status": "native_observed_bounded",
            "claim": "FurnitureData exposes passMap_ through the loader; native ObjChip.IsPassable is the consumer, and a type-4 non-empty passMap fixture is available for normalization.",
            "limits": "An empty or non-empty passMap still does not define walkability until the consumer return predicate is fixture-tested.",
            "source_refs": [by_purpose["furniture field/load boundary"]],
            "superseding_evidence": "scene_native_semantics.json#passmap-consumer",
        },
    ]


def build_review() -> tuple[dict[str, Any], dict[str, Any]]:
    scene = load_json(INPUT_SCENE)
    first_slice = load_json(INPUT_FIRST_SLICE)
    room = scene["room"]
    obj_map = room["objMap"]
    obj_dir = room["objDir"]
    object_constants = {
        item["value"]: item["name"] for item in scene["object_type_constants"]
    }
    map_values = [value_ for row in obj_map for value_ in row]
    dir_values = [value_ for row in obj_dir for value_ in row]
    furniture_records, pass_map_summary = furniture_profiles()
    source_slices = build_source_slices()
    observations = build_observations(scene, source_slices)

    source_inputs = [
        INPUT_SCENE,
        INPUT_FIRST_SLICE,
        FIELD_LOAD,
        TYPE_CATALOG,
        *SOURCE_FILES.values(),
    ]
    input_manifest = [
        {"file": relative_path(path), "sha256": sha256_file(path)} for path in source_inputs
    ]

    map_histogram = dict(sorted(Counter(map_values).items()))
    dir_histogram = dict(sorted(Counter(dir_values).items()))
    door_cells = [
        {"x": x, "y": y, "raw_map_value": value_}
        for y, row in enumerate(obj_map)
        for x, value_ in enumerate(row)
        if value_ == 5
    ]
    goal_candidates = [
        {"x": x, "y": y, "raw_map_value": value_}
        for y, row in enumerate(obj_map)
        for x, value_ in enumerate(row)
        if value_ == 2
    ]
    route_candidate = {
        "status": "blocked_on_fixture_semantics",
        "start_candidates": door_cells,
        "goal_candidates": goal_candidates,
        "node_grid_candidate": {
            "width": room["grid_shape"]["objMap_width"],
            "height": room["grid_shape"]["objMap_height"],
            "node_count_candidate": room["grid_shape"]["objMap_width"] * room["grid_shape"]["objMap_height"],
        },
        "neighbor_policy_candidate": {
            "shape": "3x3 centered neighborhood",
            "connectivity": native_facts.NEIGHBOR_POLICY["connectivity"],
            "offsets": native_facts.NEIGHBOR_POLICY["offsets"],
            "status": native_facts.NEIGHBOR_POLICY["status"],
        },
        "required_before_path_assertion": [
            "passability_and_passMap_fixture_normalization",
            "goal_filter_confirmation",
        ],
        "cleared_gates": [
            "objMap_to_objChip_type_assignment",
            "room_placement_and_furniture_binding_model",
            "standing_positions",
            "neighbor_policy_confirmation",
        ],
        "note": "No path is emitted from raw map values alone.",
    }

    review = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-scene-semantics-review",
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "input_manifest": input_manifest,
        "scene": {
            "room_type": room["type"],
            "room_id": room["id"],
            "room_name": room["name"],
            "grid_shape": room["grid_shape"],
            "raw_map_value_histogram": map_histogram,
            "raw_dir_value_histogram": dir_histogram,
            "raw_map_domain": sorted(set(map_values)),
            "object_constant_domain": sorted(object_constants),
            "domain_overlap": sorted(set(map_values) & set(object_constants)),
            "domain_gap": sorted(set(map_values) - set(object_constants)),
            "door_cells_by_raw_code": door_cells,
            "direction_values_are_raw": True,
            "semantic_status": "pending_review",
        },
        "object_constants": scene["object_type_constants"],
        "furniture_pass_map_inventory": pass_map_summary,
        "route": route_candidate,
        "observations": observations,
        "promotion_matrix": [
            {
                "id": "room-grid",
                "current_status": "source_observed",
                "can_promote_to_contract": True,
                "required_next_evidence": "none for dimensions/raw grid; retain raw field provenance",
            },
            {
                "id": "map-code-to-object-type",
                "current_status": "native_observed",
                "can_promote_to_contract": True,
                "required_next_evidence": "none for raw assignment; retain APK hash and method RVA provenance",
            },
            {
                "id": "door-location",
                "current_status": "contract_ready",
                "can_promote_to_contract": True,
                "required_next_evidence": "resolve the visual FurnitureData selector separately",
            },
            {
                "id": "coordinate-transform",
                "current_status": "source_observed",
                "can_promote_to_contract": True,
                "required_next_evidence": "separate camera/depth/asset anchor review",
            },
            {
                "id": "passability",
                "current_status": "native_observed_bounded",
                "can_promote_to_contract": False,
                "required_next_evidence": "normalize passMap boolean return and null-furniture fallback with type-4 fixture",
            },
            {
                "id": "route-fixture",
                "current_status": "blocked_on_fixture_semantics",
                "can_promote_to_contract": False,
                "required_next_evidence": "passMap fixture normalization and goal filter confirmation",
            },
        ],
        "source_slices": source_slices,
        "review_items": [
            {
                "id": "objmap-assignment-gap",
                "status": "closed",
                "blocking": False,
                "action": "Use native InitObjChips contract: ObjChip.type_ = objMap[y][x].",
            },
            {
                "id": "room-furniture-placement-gap",
                "status": "bounded_contract",
                "blocking": False,
                "action": "Implement placement as a second layer: PlaceObj binds FurnitureData; initial records use FLAG_INIT_DESK/FLAG_INIT_PLACE.",
            },
            {
                "id": "passmap-and-standing-semantics",
                "status": "bounded_candidate",
                "blocking": True,
                "action": "Use native standing-position formulas; normalize the IsPassable passMap branch with type-4 fixture.",
            },
            {
                "id": "neighbor-policy",
                "status": "closed",
                "blocking": False,
                "action": "Use native AddNeighbor contract: cardinal 4-neighbor only; do not use diagonal edges.",
            },
            {
                "id": "route-goal-filter",
                "status": "unknown",
                "blocking": True,
                "action": "Resolve goal flags and raw-code/object relations before selecting a route goal.",
            },
            {
                "id": "asset-selector-carryover",
                "status": "quarantine",
                "blocking": True,
                "action": "Keep seb/img/subSeb selectors outside runtime until the asset relationship review closes.",
            },
        ],
        "first_slice_reference": {
            "file": relative_path(INPUT_FIRST_SLICE),
            "sha256": sha256_file(INPUT_FIRST_SLICE),
            "selected_furniture_ids": SELECTED_FURNITURE_IDS,
        },
    }

    checks = [
        {
            "id": "room-grid-shape",
            "status": "pass" if room["grid_shape"] == {"objMap_width": 10, "objMap_height": 10, "objDir_width": 10, "objDir_height": 10} else "fail",
            "observed": room["grid_shape"],
            "expected": "10x10 for objMap and objDir",
        },
        {
            "id": "raw-map-domain",
            "status": "pass" if not set(map_values) - set(object_constants) else "fail",
            "observed": sorted(set(map_values)),
            "expected": sorted(object_constants),
            "note": "Domain overlap is structural evidence, not semantic assignment proof.",
        },
        {
            "id": "door-code-count",
            "status": "pass" if len(door_cells) == 1 and door_cells[0] == {"x": 8, "y": 4, "raw_map_value": 5} else "fail",
            "observed": door_cells,
            "expected": [{"x": 8, "y": 4, "raw_map_value": 5}],
        },
        {
            "id": "furniture-locale-parse",
            "status": "pass" if pass_map_summary["parse_error_count"] == 0 and pass_map_summary["missing_locale_count"] == 0 else "fail",
            "observed": {
                "english_rows": pass_map_summary["english_rows"],
                "japanese_rows": pass_map_summary["japanese_rows"],
                "parse_errors": pass_map_summary["parse_error_count"],
                "missing_locale": pass_map_summary["missing_locale_count"],
            },
            "expected": "aligned rows with zero parse errors",
        },
        {
            "id": "source-anchors",
            "status": "pass" if all(slice_["status"] in {"evidence_only", "decompiler_bounded", "decompiler_damaged"} for slice_ in source_slices) else "fail",
            "observed": len(source_slices),
            "expected": "all source spans resolve",
        },
        {
            "id": "route-not-promoted",
            "status": "pass" if route_candidate["status"] == "blocked_on_fixture_semantics" else "fail",
            "observed": route_candidate["status"],
            "expected": "blocked only on passMap fixture and goal semantics",
        },
        {
            "id": "semantic-not-promoted",
            "status": "pass" if review["semantic_status"] == "pending_review" else "fail",
            "observed": review["semantic_status"],
            "expected": "pending_review",
        },
    ]
    validation = {
        "schema_version": VALIDATION_VERSION,
        "status": "pass" if all(check["status"] == "pass" for check in checks) else "fail",
        "semantic_status": "pending_review",
        "generated_at_utc": review["generated_at_utc"],
        "input_hash": sha256_bytes(stable_json(input_manifest).encode("utf-8")),
        "failed_checks": [check["id"] for check in checks if check["status"] != "pass"],
        "checks": checks,
        "counts": {
            "source_slices": len(source_slices),
            "observations": len(observations),
            "furniture_ids": pass_map_summary["total_ids"],
            "non_empty_pass_map_records": pass_map_summary["non_empty_pass_map_count"],
            "review_items": len(review["review_items"]),
            "route_goal_candidates": len(goal_candidates),
        },
        "blocking_review_items": [
            item["id"] for item in review["review_items"] if item["blocking"]
        ],
    }
    return review, validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=EVIDENCE)
    args = parser.parse_args()
    review, validation = build_review()
    write_json(args.output_dir / "scene_semantics_review.json", review)
    write_json(args.output_dir / "scene_semantics_validation.json", validation)
    print(
        "scene_semantics_review_complete "
        f"status={validation['status']} "
        f"slices={validation['counts']['source_slices']} "
        f"furniture={validation['counts']['furniture_ids']} "
        f"non_empty_pass_map={validation['counts']['non_empty_pass_map_records']} "
        f"review_items={validation['counts']['review_items']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
