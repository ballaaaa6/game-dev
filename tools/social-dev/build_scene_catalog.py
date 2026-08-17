"""Build the canonical Social Dev SceneCatalog for RoomData(0).

This builder is contract/evidence-only. It reads the current RoomData and
FurnitureData rows, verifies the Phase 1D authority package, and projects the
closed scene facts into a stable catalog fixture. It never executes recovered
C# or native code and it does not create renderer/runtime behavior.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_behavior_candidates as base


ROOT = base.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
TABLE_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
CATALOG = EVIDENCE / "csharp_update_inventory"
SOURCE_ROOT = base.SOURCE_ROOT

SCENE_CANDIDATE_PATH = EVIDENCE / "scene_data_candidate.json"
NATIVE_SEMANTICS_PATH = EVIDENCE / "scene_native_semantics.json"
NATIVE_VALIDATION_PATH = EVIDENCE / "scene_native_semantics_validation.json"
PASSMAP_PATH = EVIDENCE / "phase1d_passmap_fixture.json"
ROUTE_PATH = EVIDENCE / "phase1d_route_fixture.json"
CLOSURE_PATH = EVIDENCE / "phase1d_closure.json"
CLOSURE_VALIDATION_PATH = EVIDENCE / "phase1d_closure_validation.json"
FIELD_LOAD_PATH = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG_PATH = CATALOG / "type_catalog.json"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"

SOURCE_FILES = {
    "RoomData": SOURCE_ROOT / "data/RoomData.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
}

SCHEMA_VERSION = "social-dev-scene-catalog-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-scene-catalog-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-scene-catalog-validation-v1"

EXPECTED_MAP_DOMAIN = [0, 1, 2, 3, 4, 5, 6]
EXPECTED_PASSABILITY_MATRIX = [
    [True, False, False],
    [True, False, False],
    [True, True, True],
]
EXPECTED_ROUTE_PATH = [[8, 4], [7, 4], [6, 4]]
EXPECTED_FOOTPRINT_CELLS = {(x, y) for y in range(1, 4) for x in range(3, 6)}
SELECTED_NATIVE_METHOD_IDS = [
    "room-init-obj-chips",
    "room-place-door",
    "room-setup-big-chips-parent",
    "objchip-place-object",
    "objchip-is-passable",
    "astar-connect-neighbors",
    "astar-add-neighbor",
    "astar-search-route",
    "astar-search-route-public",
]
EVIDENCE_INPUTS = [
    SCENE_CANDIDATE_PATH,
    NATIVE_SEMANTICS_PATH,
    NATIVE_VALIDATION_PATH,
    PASSMAP_PATH,
    ROUTE_PATH,
    CLOSURE_PATH,
    CLOSURE_VALIDATION_PATH,
    FIELD_LOAD_PATH,
    TYPE_CATALOG_PATH,
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


def relative_path(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return str(candidate.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(candidate).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_table_record(type_name: str, locale: str, row_id: int) -> dict[str, Any]:
    path = base.table_path(type_name, locale)
    rows = base.read_table(path)
    matches = [row for row in rows if row["id"] == row_id]
    if len(matches) != 1:
        raise ValueError(f"expected one {type_name} row for {locale}/{row_id}, found {len(matches)}")
    field_load = base.find_field_load(load_json(FIELD_LOAD_PATH)["rows"], type_name)
    type_source = base.find_type_source(load_json(TYPE_CATALOG_PATH)["records"], type_name)
    parsed = base.parse_row(type_name, locale, matches[0], field_load, type_source, path)
    if parsed["parse"]["status"] != "pass":
        raise ValueError(f"{type_name}/{locale}/{row_id} failed parsing: {parsed['parse']['errors']}")
    return parsed


def field(record: dict[str, Any], name: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(name, {}).get("value", default)


def row_ref(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": record["type"],
        "locale": record["locale"],
        "id": record["id"],
        "table_path": record["table_path"],
        "row_number": record["row_number"],
        "row_sha256": record["row_sha256"],
        "parse_status": record["parse"]["status"],
    }


def source_slice_ref(candidate: dict[str, Any], selected_types: set[str]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for item in candidate.get("source_slices", []):
        if item.get("type") not in selected_types:
            continue
        path = ROOT / item["file"]
        if not path.is_file():
            refs.append(
                {
                    "type": item.get("type"),
                    "file": item.get("file"),
                    "line_start": item.get("line_start"),
                    "line_end": item.get("line_end"),
                    "purpose": item.get("purpose"),
                    "expected_file_sha256": item.get("file_sha256"),
                    "expected_slice_sha256": item.get("slice_sha256"),
                    "actual_file_sha256": None,
                    "actual_slice_sha256": None,
                    "hash_status": "missing",
                }
            )
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        start = int(item["line_start"])
        end = int(item["line_end"])
        text = "".join(lines[start - 1 : end])
        actual_file_hash = sha256_file(path)
        actual_slice_hash = sha256_bytes(text.encode("utf-8"))
        refs.append(
            {
                "type": item.get("type"),
                "file": item["file"],
                "line_start": start,
                "line_end": end,
                "purpose": item.get("purpose"),
                "expected_file_sha256": item.get("file_sha256"),
                "expected_slice_sha256": item.get("slice_sha256"),
                "actual_file_sha256": actual_file_hash,
                "actual_slice_sha256": actual_slice_hash,
                "hash_status": "pass"
                if actual_file_hash == item.get("file_sha256") and actual_slice_hash == item.get("slice_sha256")
                else "drift",
            }
        )
    return refs


def evidence_ref(path: Path) -> dict[str, str]:
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = [evidence_ref(path) for path in sorted(set(paths), key=lambda item: str(item))]
    return {"files": files, "input_hash": sha256_bytes(stable_json(files).encode("utf-8"))}


def native_claim(native: dict[str, Any], claim_id: str) -> dict[str, Any]:
    for claim in native.get("claims", []):
        if claim.get("id") == claim_id:
            return claim
    raise KeyError(f"missing native claim: {claim_id}")


def native_methods(native: dict[str, Any]) -> list[dict[str, Any]]:
    methods = {item["id"]: item for item in native.get("native_method_manifest", [])}
    missing = [item for item in SELECTED_NATIVE_METHOD_IDS if item not in methods]
    if missing:
        raise KeyError(f"missing native methods: {missing}")
    return [copy.deepcopy(methods[item]) for item in SELECTED_NATIVE_METHOD_IDS]


def cardinal_path(path: list[list[int]]) -> bool:
    return all(
        len(a) == 2
        and len(b) == 2
        and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        for a, b in zip(path, path[1:])
    )


def build_provenance(
    scene_candidate: dict[str, Any],
    native: dict[str, Any],
    room_en: dict[str, Any],
    room_ja: dict[str, Any],
    furniture_en: dict[str, Any],
    furniture_ja: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    selected_types = {"Room", "RoomData", "ObjChip", "Astar", "FurnitureData"}
    native_refs: list[dict[str, Any]] = []
    for claim_id in ["objmap-to-objchip-type", "door-binding", "furniture-placement-model", "passmap-consumer", "neighbor-policy", "route-filter"]:
        claim = native_claim(native, claim_id)
        native_refs.append(
            {
                "claim_id": claim_id,
                "status": claim.get("status"),
                "promotable_to_contract": claim.get("promotable_to_contract"),
                "promotable_to_canonical_catalog": claim.get("promotable_to_canonical_catalog", True),
                "native_refs": copy.deepcopy(claim.get("native_refs", [])),
                "source_refs": copy.deepcopy(claim.get("source_refs", [])),
            }
        )
    return {
        "status": "verified",
        "authority": {
            "phase1d_closure": evidence_ref(CLOSURE_PATH),
            "phase1d_closure_validation": evidence_ref(CLOSURE_VALIDATION_PATH),
            "native_semantics": evidence_ref(NATIVE_SEMANTICS_PATH),
            "passmap_fixture": evidence_ref(PASSMAP_PATH),
            "route_fixture": evidence_ref(ROUTE_PATH),
        },
        "input_manifest": manifest,
        "data_rows": {
            "RoomData": {"English": row_ref(room_en), "Japanese": row_ref(room_ja)},
            "FurnitureData_type4": {"English": row_ref(furniture_en), "Japanese": row_ref(furniture_ja)},
        },
        "source_slices": source_slice_ref(scene_candidate, selected_types),
        "native_claims": native_refs,
        "native_methods": native_methods(native),
        "apk": {
            "path": native["source_artifact"]["apk"],
            "sha256": native["source_artifact"]["apk_sha256"],
            "hash_status": "pass" if sha256_file(APK_PATH) == native["source_artifact"]["apk_sha256"] else "drift",
        },
        "source_policy": "C# and native artifacts are evidence inputs only; the browser runtime must not import or execute them.",
    }


def build_checks(
    scene_candidate: dict[str, Any],
    closure: dict[str, Any],
    closure_validation: dict[str, Any],
    native: dict[str, Any],
    room_en: dict[str, Any],
    room_ja: dict[str, Any],
    furniture_en: dict[str, Any],
    furniture_ja: dict[str, Any],
    scene: dict[str, Any],
    passmap: dict[str, Any],
    route: dict[str, Any],
    provenance: dict[str, Any],
) -> list[dict[str, Any]]:
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

    room_map = field(room_en, "objMap_", [])
    room_dir = field(room_en, "objDir_", [])
    room_map_ja = field(room_ja, "objMap_", [])
    room_dir_ja = field(room_ja, "objDir_", [])
    width = len(room_map[0]) if room_map else 0
    height = len(room_map)
    all_values = {cell for row in room_map for cell in row}
    door_cells = scene["door"]["cells"]
    path = scene["route_fixtures"][0]["path"]
    footprint = {(item["x"], item["y"]) for item in scene["type4_fixture"]["footprint"]["footprint"]}
    source_hashes_ok = all(item["hash_status"] == "pass" for item in provenance["source_slices"])

    check(
        "phase1d-entry-gate",
        closure.get("status") == "pass"
        and closure.get("semantic_status") == "closed_for_phase2_entry"
        and closure_validation.get("failed_checks") == [],
        {"closure": closure.get("status"), "semantic_status": closure.get("semantic_status"), "failed_checks": closure_validation.get("failed_checks")},
        {"closure": "pass", "semantic_status": "closed_for_phase2_entry", "failed_checks": []},
        "Phase 2A consumes only the closed Phase 1D authority package.",
    )
    check(
        "room-identity",
        scene["id"] == "room:0"
        and scene["source_identity"] == {"type": "RoomData", "id_field": "id_", "source_id": 0}
        and scene["name"]["English"] == "Floor A",
        {"id": scene["id"], "source_identity": scene["source_identity"], "name": scene["name"]["English"]},
        {"id": "room:0", "source_id": 0, "name": "Floor A"},
        "The canonical id is type plus source id, not an array position alone.",
    )
    check(
        "room-locale-rows",
        room_en["id"] == room_ja["id"] == 0
        and scene["name"] == {"English": "Floor A", "Japanese": "フロアA"}
        and room_map == room_map_ja
        and room_dir == room_dir_ja,
        {"english_row": room_en["row_sha256"], "japanese_row": room_ja["row_sha256"], "grid_equal": room_map == room_map_ja and room_dir == room_dir_ja},
        {"same_id": 0, "grid_equal": True},
        "English/Japanese rows agree on identity and scene grid; names remain locale values.",
    )
    check(
        "grid-dimensions",
        width == 10 and height == 10 and len(room_dir) == 10 and len(room_dir[0]) == 10,
        {"objMap": [width, height], "objDir": [len(room_dir[0]) if room_dir else 0, len(room_dir)]},
        {"objMap": [10, 10], "objDir": [10, 10]},
        "RoomData(0) has two rectangular 10x10 arrays.",
    )
    check(
        "grid-rectangular",
        all(len(row) == width for row in room_map) and all(len(row) == width for row in room_dir),
        {"objMap_row_lengths": sorted({len(row) for row in room_map}), "objDir_row_lengths": sorted({len(row) for row in room_dir})},
        {"row_length": [10]},
        "All rows use the same x width and preserve y-major source order.",
    )
    check(
        "map-domain",
        sorted(all_values) == EXPECTED_MAP_DOMAIN,
        sorted(all_values),
        EXPECTED_MAP_DOMAIN,
        "Raw map values are preserved in the native type domain 0..6.",
    )
    check(
        "native-map-assignment",
        scene["grid"]["native_assignment"]["raw_cell"] == "objMap[y][x]"
        and scene["grid"]["native_assignment"]["flat_index"] == "x + y * width",
        scene["grid"]["native_assignment"],
        {"raw_cell": "objMap[y][x]", "flat_index": "x + y * width"},
        "Native Room.InitObjChips passes the raw cell to ObjChip.type_.",
    )
    check(
        "door-cell",
        scene["door"]["type"] == 5
        and [(item["x"], item["y"]) for item in door_cells] == [(8, 4)]
        and door_cells[0]["raw_map_value"] == 5
        and scene["door"]["installed_flag"] == 1,
        {"type": scene["door"]["type"], "cells": [[item["x"], item["y"]] for item in door_cells], "installed_flag": scene["door"]["installed_flag"]},
        {"type": 5, "cells": [[8, 4]], "installed_flag": 1},
        "Room.PlaceDoor scans ObjChip type 5 and writes the installed flag.",
    )
    check(
        "type4-anchor",
        scene["type4_fixture"]["anchor"] == {"x": 4, "y": 2, "raw_map_value": 4}
        and scene["type4_fixture"]["furniture_binding"]["id"] == 0
        and scene["type4_fixture"]["furniture_binding"]["type"] == 4,
        {"anchor": scene["type4_fixture"]["anchor"], "furniture": scene["type4_fixture"]["furniture_binding"]["id"], "type": scene["type4_fixture"]["furniture_binding"]["type"]},
        {"anchor": {"x": 4, "y": 2, "raw_map_value": 4}, "furniture": 0, "type": 4},
        "The type-4 fixture binds the real RoomData anchor to FurnitureData(0).",
    )
    check(
        "type4-furniture-row",
        field(furniture_en, "passMap_") == field(furniture_ja, "passMap_")
        and field(furniture_en, "passMap_") == passmap["furniture_record"]["passMap"]
        and field(furniture_en, "type_") == 4,
        {"english_type": field(furniture_en, "type_"), "passMap_shape": [len(field(furniture_en, "passMap_")), len(field(furniture_en, "passMap_")[0])]},
        {"type": 4, "passMap_shape": [9, 9]},
        "FurnitureData(0) is cross-checked from both locale rows and the Phase 1D fixture.",
    )
    check(
        "type4-footprint",
        len(scene["type4_fixture"]["footprint"]["footprint"]) == 9
        and scene["type4_fixture"]["footprint"]["parent_center_offset"] == {"dx": 0, "dy": 0}
        and footprint == EXPECTED_FOOTPRINT_CELLS,
        {"count": len(footprint), "cells": sorted([[x, y] for x, y in footprint]), "center": scene["type4_fixture"]["footprint"]["parent_center_offset"]},
        {"count": 9, "cells": sorted([[x, y] for x, y in EXPECTED_FOOTPRINT_CELLS]), "center": {"dx": 0, "dy": 0}},
        "The native type-4 placement produces the bounded 3x3 footprint.",
    )
    check(
        "type4-passability-matrix",
        scene["type4_fixture"]["passability"]["matrix"] == EXPECTED_PASSABILITY_MATRIX,
        scene["type4_fixture"]["passability"]["matrix"],
        EXPECTED_PASSABILITY_MATRIX,
        "IsPassable normalization is the reviewed 3x3 matrix.",
    )
    check(
        "type4-passability-probes",
        all(item["isPassable"] for item in scene["type4_fixture"]["passability"]["synthetic_zero_probes"])
        and scene["type4_fixture"]["passability"]["all_nonzero_probe"]["isPassable"] is False,
        {"zero_probe_count": len(scene["type4_fixture"]["passability"]["synthetic_zero_probes"]), "all_nonzero": scene["type4_fixture"]["passability"]["all_nonzero_probe"]["isPassable"]},
        {"zero_probe_count": 9, "all_nonzero": False},
        "Zero-cell and all-nonzero probes exercise both native boolean branches.",
    )
    check(
        "route-path",
        path == EXPECTED_ROUTE_PATH
        and scene["route_fixtures"][0]["step_count"] == 2
        and route["route"]["path"] == route["route"]["expected_path"],
        {"path": path, "step_count": scene["route_fixtures"][0]["step_count"]},
        {"path": EXPECTED_ROUTE_PATH, "step_count": 2},
        "The route is projected from the real RoomData fixture, not generated from raw codes alone.",
    )
    check(
        "route-cardinal-neighbors",
        cardinal_path(path)
        and scene["route_fixtures"][0]["neighbor_policy"]["connectivity"] == 4
        and scene["route_fixtures"][0]["neighbor_policy"]["corners_included"] is False,
        {"cardinal": cardinal_path(path), "connectivity": scene["route_fixtures"][0]["neighbor_policy"]["connectivity"]},
        {"cardinal": True, "connectivity": 4},
        "Astar connects four cardinal neighbors only.",
    )
    check(
        "route-filter-probes",
        all(item["path"] is None and item["admission"]["admitted"] is False for item in scene["route_fixtures"][0]["filter_probes"]),
        [{"id": item["id"], "path": item["path"], "admitted": item["admission"]["admitted"]} for item in scene["route_fixtures"][0]["filter_probes"]],
        "occupied-type2, type4-ispassable-false, type6-outdoor all rejected",
        "The route fixture retains negative admission probes.",
    )
    check(
        "route-goal-filter",
        scene["route_fixtures"][0]["goal_filter"]["equip_flag_on_type1"]["direction"] == 7,
        scene["route_fixtures"][0]["goal_filter"]["equip_flag_on_type1"],
        {"raw_objDir": 0, "direction": 7},
        "The public equipment goal postprocess keeps the reviewed objDir mapping.",
    )
    check(
        "provenance-source-hashes",
        source_hashes_ok and all(item["hash_status"] == "pass" for item in provenance["source_slices"]),
        {"source_slices": len(provenance["source_slices"]), "drift": [item["file"] for item in provenance["source_slices"] if item["hash_status"] != "pass"]},
        "all selected source slices pass hash verification",
        "Canonical fields must remain anchored to current source slices.",
    )
    check(
        "provenance-apk",
        provenance["apk"]["hash_status"] == "pass" and len(provenance["apk"]["sha256"]) == 64,
        provenance["apk"],
        "current APK hash matches native evidence",
        "Native method RVAs are valid only for the pinned APK hash.",
    )
    check(
        "provenance-rows",
        room_en["row_sha256"] == scene["provenance_row_refs"]["RoomData"]["English"]["row_sha256"]
        and room_ja["row_sha256"] == scene["provenance_row_refs"]["RoomData"]["Japanese"]["row_sha256"]
        and furniture_en["row_sha256"] == scene["provenance_row_refs"]["FurnitureData_type4"]["English"]["row_sha256"]
        and furniture_ja["row_sha256"] == scene["provenance_row_refs"]["FurnitureData_type4"]["Japanese"]["row_sha256"],
        {"room_en": room_en["row_sha256"], "room_ja": room_ja["row_sha256"], "furniture_en": furniture_en["row_sha256"], "furniture_ja": furniture_ja["row_sha256"]},
        "current source row hashes are retained for both locales",
        "Every promoted row has a direct table provenance reference.",
    )
    check(
        "contract-boundary",
        scene["deferred"]
        and "ObjectCatalog" in scene["deferred"]
        and "renderer" in scene["deferred"]
        and "runtime_behavior" in scene["deferred"],
        scene["deferred"],
        "ObjectCatalog, renderer and runtime behavior remain deferred",
        "Phase 2A must not silently expand into implementation work.",
    )
    check(
        "candidate-cross-check",
        scene_candidate["room"]["id"] == 0
        and scene_candidate["room"]["objMap"] == room_map
        and scene_candidate["room"]["objDir"] == room_dir
        and scene_candidate["room"]["grid_shape"] == {"objMap_width": 10, "objMap_height": 10, "objDir_width": 10, "objDir_height": 10},
        {"candidate_room_id": scene_candidate["room"]["id"], "candidate_grid": scene_candidate["room"]["grid_shape"]},
        {"candidate_room_id": 0, "candidate_grid": {"objMap_width": 10, "objMap_height": 10, "objDir_width": 10, "objDir_height": 10}},
        "The new contract is a checked projection of the existing scene candidate, not an independent rewrite.",
    )
    return checks


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scene_candidate = load_json(SCENE_CANDIDATE_PATH)
    native = load_json(NATIVE_SEMANTICS_PATH)
    native_validation = load_json(NATIVE_VALIDATION_PATH)
    passmap = load_json(PASSMAP_PATH)
    route = load_json(ROUTE_PATH)
    closure = load_json(CLOSURE_PATH)
    closure_validation = load_json(CLOSURE_VALIDATION_PATH)

    room_en = read_table_record("RoomData", "English", 0)
    room_ja = read_table_record("RoomData", "Japanese", 0)
    furniture_en = read_table_record("FurnitureData", "English", 0)
    furniture_ja = read_table_record("FurnitureData", "Japanese", 0)
    room_map = copy.deepcopy(field(room_en, "objMap_", []))
    room_dir = copy.deepcopy(field(room_en, "objDir_", []))
    if not room_map or not room_dir:
        raise ValueError("RoomData(0) objMap_/objDir_ must be non-empty")
    if len(room_map) != len(room_dir) or any(len(a) != len(b) for a, b in zip(room_map, room_dir)):
        raise ValueError("RoomData(0) objMap_/objDir_ shape mismatch")

    room_width = len(room_map[0])
    room_height = len(room_map)
    door_type = 5
    door_cells = [
        {
            "x": x,
            "y": y,
            "raw_map_value": room_map[y][x],
            "raw_dir_value": room_dir[y][x],
        }
        for y in range(room_height)
        for x in range(room_width)
        if room_map[y][x] == door_type
    ]
    passmap_record = passmap["furniture_record"]
    passability = copy.deepcopy(passmap["isPassable"])
    native_map_claim = native_claim(native, "objmap-to-objchip-type")
    door_claim = native_claim(native, "door-binding")
    route_filter_claim = native_claim(native, "route-filter")

    source_paths = [
        *EVIDENCE_INPUTS,
        APK_PATH,
        base.table_path("RoomData", "English"),
        base.table_path("RoomData", "Japanese"),
        base.table_path("FurnitureData", "English"),
        base.table_path("FurnitureData", "Japanese"),
        *SOURCE_FILES.values(),
    ]
    manifest = input_manifest(source_paths)
    provenance = build_provenance(
        scene_candidate,
        native,
        room_en,
        room_ja,
        furniture_en,
        furniture_ja,
        manifest,
    )
    provenance_row_refs = {
        "RoomData": {"English": row_ref(room_en), "Japanese": row_ref(room_ja)},
        "FurnitureData_type4": {"English": row_ref(furniture_en), "Japanese": row_ref(furniture_ja)},
    }

    scene = {
        "id": "room:0",
        "status": "verified",
        "source_identity": {"type": "RoomData", "id_field": "id_", "source_id": 0},
        "name": {"English": field(room_en, "name_"), "Japanese": field(room_ja, "name_")},
        "default_locale": "English",
        "scalar_fields_raw": {
            name: {
                "value": field(room_en, name),
                "status": "raw_only",
                "source_field": name,
                "note": "Retained for provenance; visual asset semantics are deferred to ObjectCatalog.",
            }
            for name in ["floorImgId_", "wallImgId_", "doorImgId_", "flag_", "costMax_"]
        },
        "grid": {
            "width": room_width,
            "height": room_height,
            "objMap": room_map,
            "objDir": room_dir,
            "objMap_dimensions": {"width": room_width, "height": room_height},
            "objDir_dimensions": {"width": len(room_dir[0]), "height": len(room_dir)},
            "indexing": {
                "row_axis": "y",
                "column_axis": "x",
                "flat_index": "x + y * width",
                "source_order": "objMap[y][x] and objDir[y][x]",
                "status": "verified",
            },
            "native_assignment": {
                "raw_cell": "objMap[y][x]",
                "constructor": "new ObjChip(x, y, rawCell, null, room)",
                "flat_index": "x + y * width",
                "status": "verified",
                "evidence_claim": native_map_claim["id"],
            },
            "raw_map_domain": sorted({cell for row in room_map for cell in row}),
            "raw_map_value_histogram": {
                str(value): sum(cell == value for row in room_map for cell in row)
                for value in sorted({cell for row in room_map for cell in row})
            },
        },
        "door": {
            "status": "verified",
            "source_field": "objMap_",
            "type": door_type,
            "cells": door_cells,
            "installed_flag": door_claim["contract"]["installed_flag"],
            "image_id_raw": field(room_en, "doorImgId_"),
            "image_id_status": "raw_only",
            "asset_selector_status": "deferred_to_object_catalog",
            "evidence_claims": ["objmap-to-objchip-type", "door-binding"],
        },
        "type4_fixture": {
            "status": "verified",
            "anchor": copy.deepcopy(passmap["scene_record"]["anchor"]),
            "furniture_binding": {
                "id": field(furniture_en, "id_"),
                "name": field(furniture_en, "name_"),
                "name_locales": {"English": field(furniture_en, "name_"), "Japanese": field(furniture_ja, "name_")},
                "type": field(furniture_en, "type_"),
                "passMap_shape": [len(field(furniture_en, "passMap_")), len(field(furniture_en, "passMap_")[0])],
                "passMap": copy.deepcopy(field(furniture_en, "passMap_")),
                "asset_selector_status": "deferred_to_object_catalog",
            },
            "footprint": copy.deepcopy(passmap["native_placement"]),
            "passability": passability,
            "evidence_claims": ["furniture-placement-model", "passmap-consumer"],
        },
        "route_fixtures": [],
        "provenance_row_refs": provenance_row_refs,
        "deferred": [
            "ObjectCatalog",
            "object-to-FurnitureData placement for every occupied RoomData cell",
            "camera",
            "coordinate_transform",
            "renderer",
            "runtime_behavior",
            "visual asset promotion",
        ],
    }

    route_core = route["route"]
    start_x, start_y = route_core["start"]
    goal_x, goal_y = route_core["goal"]
    route_fixture = {
        "id": "room:0/door-to-desk-6",
        "status": "verified",
        "start": {
            "x": start_x,
            "y": start_y,
            "raw_map_value": room_map[start_y][start_x],
            "raw_dir_value": room_dir[start_y][start_x],
        },
        "goal": {
            "x": goal_x,
            "y": goal_y,
            "raw_map_value": room_map[goal_y][goal_x],
            "raw_dir_value": room_dir[goal_y][goal_x],
        },
        "path": copy.deepcopy(route_core["path"]),
        "step_count": route_core["step_count"],
        "expected_path": copy.deepcopy(route_core["expected_path"]),
        "neighbor_policy": copy.deepcopy(route_core["neighbor_policy"]),
        "cell_trace": copy.deepcopy(route_core["cell_trace"]),
        "filter_probes": copy.deepcopy(route["filter_probes"]),
        "goal_filter": {
            "flag_values": copy.deepcopy(route["goal_filter"]["native_contract"]["goal_filter"]["flag_values"]),
            "equip_flag_on_type1": copy.deepcopy(route["goal_filter"]["public_postprocess_probes"]["equip_flag_on_type1"]),
            "move_mode_mapping": copy.deepcopy(route["goal_filter"]["staff_move_mode_mapping"]),
            "status": route_filter_claim["contract"]["status"],
        },
        "secondary_real_goal": copy.deepcopy(route["secondary_real_goal"]),
        "provenance_ref": "phase1d_route_fixture.json",
    }
    scene["route_fixtures"].append(route_fixture)

    checks = build_checks(
        scene_candidate,
        closure,
        closure_validation,
        native,
        room_en,
        room_ja,
        furniture_en,
        furniture_ja,
        scene,
        passmap,
        route,
        provenance,
    )
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()

    fixture = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-scene-catalog-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scenes": [scene],
        "provenance": provenance,
        "determinism": {
            "algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash",
            "content_hash": "",
        },
    }
    fixture["determinism"]["content_hash"] = sha256_bytes(stable_json(_without_dynamic(fixture)).encode("utf-8"))

    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-scene-catalog",
        "status": status,
        "semantic_status": "approved_for_runtime_contract" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scenes": [scene],
        "fixture_ref": {
            "path": "knowledge/fixtures/accepted/scene_catalog_fixture.json",
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "provenance": provenance,
        "limits": [
            "This contract covers one RoomData(0) scene only.",
            "Native/C# artifacts remain provenance evidence and are not runtime imports.",
            "Door/furniture visual selectors and full object placement are deferred to ObjectCatalog.",
            "Camera, draw order and coordinate transform are not promoted in Phase 2A.",
        ],
        "determinism": {
            "algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash",
            "contract_hash": "",
        },
    }
    contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(_without_dynamic(contract)).encode("utf-8"))

    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "input_hash": manifest["input_hash"],
        "contract_hash": contract["determinism"]["contract_hash"],
        "fixture_hash": fixture["determinism"]["content_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {
            "checks": len(checks),
            "passed_checks": sum(item["status"] == "pass" for item in checks),
            "scenes": len(contract["scenes"]),
            "grid_cells": room_width * room_height,
            "door_cells": len(door_cells),
            "type4_footprint_cells": len(scene["type4_fixture"]["footprint"]["footprint"]),
            "route_steps": route_fixture["step_count"],
            "route_filter_probes": len(route_fixture["filter_probes"]),
        },
        "phase_boundary": {
            "phase": "Phase 2A",
            "next": "ObjectCatalog",
            "not_started": ["ObjectCatalog", "ActorCatalog", "TypeScript runtime core", "renderer"],
        },
        "native_validation_ref": {
            "path": relative_path(NATIVE_VALIDATION_PATH),
            "status": native_validation.get("status"),
        },
    }
    return fixture, contract, validation


def _without_dynamic(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: _without_dynamic(value)
            for key, value in payload.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(payload, list):
        return [_without_dynamic(item) for item in payload]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    fixture, contract, validation = build_package()
    write_json(evidence_dir / "scene_catalog_fixture.json", fixture)
    write_json(evidence_dir / "scene_catalog_validation.json", validation)
    write_json(runtime_dir / "scene_catalog_contract.json", contract)
    print(
        "scene_catalog_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"scene_count={validation['counts']['scenes']} "
        f"route_steps={validation['counts']['route_steps']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
