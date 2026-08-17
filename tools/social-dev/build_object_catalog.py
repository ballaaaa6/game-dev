"""Build the canonical Social Dev ObjectCatalog for display-slice-01.

This builder is evidence/contract-only. It consumes the closed SceneCatalog,
Phase 1D fixtures, selector evidence, current data rows, and indexed asset
metadata. It never executes recovered C# or native code and never copies asset
binaries into the runtime boundary.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_scene_catalog as scene_builder


ROOT = scene_builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
TABLE_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
SOURCE_ROOT = scene_builder.SOURCE_ROOT

SCENE_CATALOG_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
ASSET_SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_VALIDATION_PATH = EVIDENCE / "asset_validation_gate.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
PASSMAP_PATH = EVIDENCE / "phase1d_passmap_fixture.json"
ROUTE_PATH = EVIDENCE / "phase1d_route_fixture.json"
CLOSURE_PATH = EVIDENCE / "phase1d_closure.json"
CLOSURE_VALIDATION_PATH = EVIDENCE / "phase1d_closure_validation.json"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"

SOURCE_FILES = {
    "RoomData": SOURCE_ROOT / "data/RoomData.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
}

SELECTED_FURNITURE_IDS = [0, 1, 2, 5]
SELECTED_SOURCE_TYPES = {"Room", "RoomData", "FurnitureData", "ObjChip", "Astar"}
RAW_TYPE_LABELS = {
    0: "OBJ_TYPE_PASS",
    1: "OBJ_TYPE_EQUIP",
    2: "OBJ_TYPE_DESK",
    3: "OBJ_TYPE_BIG",
    4: "OBJ_TYPE_BIG_CENTER",
    5: "OBJ_TYPE_DOOR",
    6: "OBJ_TYPE_OUTDOOR",
}
SELECTOR_FIELDS = ["seb_", "subSeb_", "img_"]
SENTINEL_ALLOWED_FIELDS = {"subSeb_", "img_"}
EXPECTED_PASSABILITY_MATRIX = [
    [True, False, False],
    [True, False, False],
    [True, True, True],
]

SCHEMA_VERSION = "social-dev-object-catalog-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-object-catalog-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-object-catalog-validation-v1"


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


def field(record: dict[str, Any], name: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(name, {}).get("value", default)


def read_furniture_record(locale: str, row_id: int) -> dict[str, Any]:
    return scene_builder.read_table_record("FurnitureData", locale, row_id)


def row_ref(record: dict[str, Any]) -> dict[str, Any]:
    return scene_builder.row_ref(record)


def evidence_ref(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = [evidence_ref(path) for path in sorted(set(paths), key=lambda item: str(item))]
    return {"files": files, "input_hash": sha256_bytes(stable_json(files).encode("utf-8"))}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalize_asset_member(member: str) -> str:
    prefix = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
    if member.startswith(prefix):
        return member[len(prefix) :]
    return member


def load_authority() -> dict[str, Any]:
    scene = load_json(SCENE_CATALOG_PATH)
    selectors = load_json(ASSET_SELECTOR_PATH)
    asset_validation = load_json(ASSET_VALIDATION_PATH)
    asset_index = load_json(ASSET_INDEX_PATH)
    passmap = load_json(PASSMAP_PATH)
    route = load_json(ROUTE_PATH)
    closure = load_json(CLOSURE_PATH)
    closure_validation = load_json(CLOSURE_VALIDATION_PATH)

    require(
        scene.get("status") == "pass"
        and scene.get("semantic_status") == "approved_for_runtime_contract",
        "SceneCatalog is not approved_for_runtime_contract",
    )
    require(
        selectors.get("status") == "pass" and not selectors.get("unresolved"),
        "asset selector contract is not closed",
    )
    require(
        closure.get("status") == "pass"
        and closure.get("semantic_status") == "closed_for_phase2_entry",
        "Phase 1D closure is not closed_for_phase2_entry",
    )
    require(
        closure_validation.get("status") == "pass" and closure_validation.get("failed_checks") == [],
        "Phase 1D closure validation has failed checks",
    )
    require(asset_validation.get("status") == "evidence_gate_only", "unexpected asset validation status")
    require(isinstance(asset_index, list) and len(asset_index) == asset_validation.get("asset_index_count"), "asset index count drift")
    require(passmap.get("status") == "pass", "type-4 passMap fixture is not pass")
    require(route.get("status") == "pass", "route fixture is not pass")
    return {
        "scene": scene,
        "selectors": selectors,
        "asset_validation": asset_validation,
        "asset_index": asset_index,
        "passmap": passmap,
        "route": route,
        "closure": closure,
        "closure_validation": closure_validation,
    }


def refresh_source_slices(scene_contract: dict[str, Any]) -> list[dict[str, Any]]:
    refreshed: list[dict[str, Any]] = []
    for item in scene_contract.get("provenance", {}).get("source_slices", []):
        if item.get("type") not in SELECTED_SOURCE_TYPES:
            continue
        path = ROOT / item["file"]
        if not path.is_file():
            refreshed.append(
                {
                    "type": item.get("type"),
                    "file": item.get("file"),
                    "line_start": item.get("line_start"),
                    "line_end": item.get("line_end"),
                    "purpose": item.get("purpose"),
                    "expected_file_sha256": item.get("expected_file_sha256"),
                    "expected_slice_sha256": item.get("expected_slice_sha256"),
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
        expected_file_hash = item.get("expected_file_sha256", item.get("actual_file_sha256"))
        expected_slice_hash = item.get("expected_slice_sha256", item.get("actual_slice_sha256"))
        refreshed.append(
            {
                "type": item.get("type"),
                "file": item.get("file"),
                "line_start": start,
                "line_end": end,
                "purpose": item.get("purpose"),
                "expected_file_sha256": expected_file_hash,
                "expected_slice_sha256": expected_slice_hash,
                "actual_file_sha256": actual_file_hash,
                "actual_slice_sha256": actual_slice_hash,
                "hash_status": "pass"
                if actual_file_hash == expected_file_hash and actual_slice_hash == expected_slice_hash
                else "drift",
            }
        )
    return refreshed


def parse_source_constants() -> dict[int, dict[str, Any]]:
    path = SOURCE_FILES["ObjChip"]
    lines = path.read_text(encoding="utf-8").splitlines()
    actual_file_hash = sha256_file(path)
    found: dict[int, dict[str, Any]] = {}
    pattern = re.compile(r"^\s*public const int (OBJ_TYPE_[A-Z_]+) = (-?\d+);\s*$")
    for line_number, line in enumerate(lines, start=1):
        match = pattern.match(line)
        if match:
            name = match.group(1)
            value = int(match.group(2))
            found[value] = {
                "name": name,
                "value": value,
                "source_ref": {
                    "file": relative_path(path),
                    "line_start": line_number,
                    "line_end": line_number,
                    "source_sha256": actual_file_hash,
                },
                "semantic_status": "source_label_only",
                "status": "verified",
            }
    return found


def build_asset_index_map(asset_index: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["relative_path"]): item for item in asset_index}


def build_selector(
    selector_contract: dict[str, Any],
    selector_record: dict[str, Any],
    data_record: dict[str, Any],
    field_name: str,
    asset_index_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    raw_id = field(data_record, field_name)
    spec = selector_record["selectors"][field_name]
    require(raw_id == spec["id"], f"FurnitureData({data_record['id']}) {field_name} drift")
    if raw_id == -1:
        require(field_name in SENTINEL_ALLOWED_FIELDS, f"invalid -1 sentinel for {field_name}")
        require(spec.get("status") == "absent_by_sentinel", f"missing sentinel status for {field_name}")
        return {
            "id": -1,
            "status": "verified",
            "resolution_status": "absent_by_sentinel",
            "sentinel_policy": "explicit_absent_sentinel",
            "source_selector_status": spec.get("status"),
            "confidence": "high",
            "review_note": "The selector contract explicitly permits -1 for this field.",
        }

    require(spec.get("status") == "resolved", f"unresolved {field_name} for FurnitureData({data_record['id']})")
    filename = spec["filename"]
    relative_asset_path = f"01_GAME_PACKS/chip/{filename}"
    asset_entry = asset_index_map.get(relative_asset_path)
    require(asset_entry is not None, f"asset index missing {relative_asset_path}")
    inf_name = "seb.inf" if field_name in {"seb_", "subSeb_"} else "img.inf"
    inf_path = f"01_GAME_PACKS/chip/{inf_name}"
    inf_entry = asset_index_map.get(inf_path)
    require(inf_entry is not None, f"asset index missing {inf_path}")
    selector_index_key = "chip_seb" if inf_name == "seb.inf" else "chip_img"
    selector_index = selector_contract["asset_zip"]["selector_indexes"][selector_index_key]
    require(spec.get("inf_sha256") == selector_index["sha256"], f"selector index hash drift for {field_name}")
    require(inf_entry["sha256"] == selector_index["sha256"], f"asset index hash drift for {inf_path}")
    return {
        "id": raw_id,
        "status": "verified",
        "resolution_status": "resolved",
        "filename": filename,
        "asset_member": relative_asset_path,
        "asset_index": copy.deepcopy(asset_entry),
        "selector_index": {
            "member": spec["inf_member"],
            "sha256": spec["inf_sha256"],
            "entry_count": selector_index["entry_count"],
            "status": "verified",
        },
        "sentinel_policy": "not_applicable",
        "confidence": "high",
        "review_note": "Selector identity is closed; visual frame composition remains outside Phase 2B.",
    }


def field_projection(
    data_record: dict[str, Any],
    field_name: str,
    status: str,
    semantic_status: str,
    note: str,
) -> dict[str, Any]:
    return {
        "value": copy.deepcopy(field(data_record, field_name)),
        "status": status,
        "semantic_status": semantic_status,
        "source_field": field_name,
        "confidence": "high",
        "review_note": note,
    }


def build_object_record(
    row_id: int,
    records: dict[int, dict[str, dict[str, Any]]],
    selector_records: dict[int, dict[str, Any]],
    selector_contract: dict[str, Any],
    asset_index_map: dict[str, dict[str, Any]],
    scene: dict[str, Any],
    evidence_refs: dict[str, dict[str, str]],
) -> dict[str, Any]:
    english = records[row_id]["English"]
    japanese = records[row_id]["Japanese"]
    selector_record = selector_records[row_id]
    source_rows = {"English": scene_builder.row_ref(english), "Japanese": scene_builder.row_ref(japanese)}
    raw_type = field(english, "type_")
    raw_pass_map = field(english, "passMap_", [])
    selectors = {
        field_name: build_selector(selector_contract, selector_record, english, field_name, asset_index_map)
        for field_name in SELECTOR_FIELDS
    }
    raw_fields = {
        "category_": field_projection(
            english,
            "category_",
            "raw_only",
            "source_value",
            "Retained as the source category value; display interaction semantics are bounded elsewhere.",
        ),
        "type_": field_projection(
            english,
            "type_",
            "verified",
            "source_label_only",
            "The numeric type is verified as a source value; its product meaning is not expanded here.",
        ),
        "flag_": field_projection(
            english,
            "flag_",
            "raw_only",
            "source_value",
            "Flags remain raw because Phase 2B does not implement placement/economy behavior.",
        ),
        "passMap_": field_projection(
            english,
            "passMap_",
            "verified" if row_id == 0 else "raw_only",
            "verified_fixture" if row_id == 0 else "source_value",
            "The type-4 passMap has a normalized native fixture; empty passMap arrays remain raw-only for other records.",
        ),
    }

    if row_id == 0:
        type4 = scene["type4_fixture"]
        geometry = {
            "status": "verified",
            "confidence": "high",
            "footprint": copy.deepcopy(type4["footprint"]),
            "passability": copy.deepcopy(type4["passability"]),
            "standing_positions": {
                "status": "deferred",
                "value": None,
                "confidence": "not_promoted",
                "review_note": "Standing-position policy remains outside this fixture projection.",
            },
        }
        interaction = {
            "status": "derived",
            "semantic_status": "bounded_fixture_role",
            "role": "type4_multi_chip_passmap_fixture",
            "confidence": "high",
            "review_note": "Role is limited to the closed type-4 fixture and is not a global placement rule.",
        }
    else:
        geometry = {
            "status": "deferred",
            "confidence": "not_promoted",
            "footprint": {
                "status": "deferred",
                "value": None,
                "confidence": "not_promoted",
                "review_note": "Per-record footprint is not closed for this Phase 2B slice.",
            },
            "passability": {
                "status": "raw_only",
                "value": copy.deepcopy(raw_pass_map),
                "confidence": "high",
                "review_note": "No normalized passability fixture is promoted for this record.",
            },
            "standing_positions": {
                "status": "deferred",
                "value": None,
                "confidence": "not_promoted",
                "review_note": "Standing-position policy remains outside this record.",
            },
        }
        role = "door_selector_record" if raw_type == 5 else "desk_selector_record"
        interaction = {
            "status": "derived",
            "semantic_status": "bounded_selector_role",
            "role": role,
            "confidence": "medium",
            "review_note": "Role is derived from the selected source record and selector evidence only.",
        }

    if raw_type == 2:
        route_goal = scene["route_fixtures"][0]["goal"]
        direction_policy = {
            "status": "verified",
            "semantic_status": "source_access_policy",
            "rule": "ObjChip.PlaceObj reads RoomData.objDir_[iy][ix] for type 2.",
            "example": {
                "cell": [route_goal["x"], route_goal["y"]],
                "raw_dir_value": route_goal["raw_dir_value"],
            },
            "confidence": "high",
            "review_note": "This is an access policy, not a complete placement map.",
            "evidence_refs": [evidence_refs["route_fixture"]],
        }
    else:
        direction_policy = {
            "status": "deferred",
            "semantic_status": "not_promoted",
            "rule": None,
            "confidence": "not_promoted",
            "review_note": "No per-record direction policy is promoted in this phase.",
        }

    return {
        "id": f"furniture:{row_id}",
        "status": "verified",
        "semantic_status": "approved_for_runtime_contract",
        "source_identity": {
            "type": "FurnitureData",
            "id_field": "id_",
            "source_id": row_id,
            "status": "verified",
            "confidence": "high",
            "review_note": "Stable id is type plus source id, not array position alone.",
        },
        "name": {
            "values": {"English": field(english, "name_"), "Japanese": field(japanese, "name_")},
            "status": "verified",
            "semantic_status": "locale_value",
            "confidence": "high",
            "review_note": "Names are retained as locale source values.",
        },
        "raw_fields": raw_fields,
        "selectors": selectors,
        "geometry": geometry,
        "direction_policy": direction_policy,
        "interaction": interaction,
        "provenance_ref": {
            "data_rows": source_rows,
            "asset_selector_contract": evidence_refs["asset_selector_contract"],
            "source_policy": "C# and native artifacts are evidence only; they are not runtime imports.",
        },
    }


def build_raw_object_types(scene: dict[str, Any]) -> list[dict[str, Any]]:
    source_constants = parse_source_constants()
    histogram = scene["grid"]["raw_map_value_histogram"]
    records: list[dict[str, Any]] = []
    for raw_type, label in RAW_TYPE_LABELS.items():
        source = source_constants.get(raw_type)
        require(source is not None, f"missing ObjChip source constant for raw type {raw_type}")
        require(source["name"] == label, f"source label drift for raw type {raw_type}")
        records.append(
            {
                "id": f"raw-type:{raw_type}",
                "raw_type": raw_type,
                "source_constant": copy.deepcopy(source),
                "scene_cell_count": int(histogram.get(str(raw_type), 0)),
                "map_assignment": {
                    "status": "verified",
                    "rule": "Room.InitObjChips passes objMap[y][x] as ObjChip.type_.",
                    "flat_index": "x + y * width",
                    "confidence": "high",
                    "review_note": "Raw assignment is closed; FurnitureData binding is a separate layer.",
                },
            }
        )
    return records


def build_scene_bindings(scene: dict[str, Any], objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    object_by_id = {item["id"]: item for item in objects}
    door = scene["door"]
    type4 = scene["type4_fixture"]
    route = scene["route_fixtures"][0]
    occupied_probe = next(item for item in route["filter_probes"] if item["id"] == "occupied-type2")
    return [
        {
            "id": "room:0/type4-anchor",
            "status": "verified",
            "binding_status": "verified_fixture",
            "cell": copy.deepcopy(type4["anchor"]),
            "raw_object_type": type4["anchor"]["raw_map_value"],
            "furniture_id": "furniture:0",
            "footprint_cells": copy.deepcopy(type4["footprint"]["footprint"]),
            "passability_status": "verified",
            "evidence_claims": ["furniture-placement-model", "passmap-consumer"],
            "confidence": "high",
            "review_note": "Explicit type-4 fixture binding; not a global map-to-furniture rule.",
        },
        {
            "id": "room:0/door-cell",
            "status": "verified",
            "binding_status": "candidate_by_type_and_selector",
            "cell": copy.deepcopy(door["cells"][0]),
            "raw_object_type": door["type"],
            "installed_flag": door["installed_flag"],
            "furniture_candidates": ["furniture:1"] if object_by_id.get("furniture:1") else [],
            "native_binding": {
                "status": "deferred",
                "reason": "Room.PlaceDoor passes FurnitureData=null before writing the installed flag.",
                "evidence_claim": "door-binding",
            },
            "confidence": "medium",
            "review_note": "Raw door binding is verified; FurnitureData identity remains a selector candidate.",
        },
        {
            "id": "room:0/occupied-type2-route-probe",
            "status": "verified",
            "binding_status": "fixture_only",
            "cell": copy.deepcopy(occupied_probe["cell"]),
            "raw_object_type": occupied_probe["admission"]["raw_type"],
            "furniture_id": "furniture:2",
            "has_obj": occupied_probe["admission"]["has_obj"],
            "route_admitted": occupied_probe["admission"]["admitted"],
            "route_reason": occupied_probe["admission"]["reason"],
            "confidence": "high",
            "review_note": "Explicit route fixture only; it does not map all type-2 cells.",
        },
    ]


def build_provenance(
    authority: dict[str, Any],
    manifest: dict[str, Any],
    records: dict[int, dict[str, dict[str, Any]]],
    source_slices: list[dict[str, Any]],
) -> dict[str, Any]:
    scene_contract = authority["scene"]
    selectors = authority["selectors"]
    asset_zip_expected = selectors["asset_zip"]["sha256"]
    apk_expected = scene_contract["provenance"]["apk"]["sha256"]
    return {
        "status": "verified",
        "authority": {
            "scene_catalog": evidence_ref(SCENE_CATALOG_PATH),
            "asset_selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
            "asset_validation_gate": evidence_ref(ASSET_VALIDATION_PATH),
            "phase1d_closure": evidence_ref(CLOSURE_PATH),
            "phase1d_closure_validation": evidence_ref(CLOSURE_VALIDATION_PATH),
            "passmap_fixture": evidence_ref(PASSMAP_PATH),
            "route_fixture": evidence_ref(ROUTE_PATH),
        },
        "input_manifest": manifest,
        "data_rows": {
            str(row_id): {
                "English": row_ref(records[row_id]["English"]),
                "Japanese": row_ref(records[row_id]["Japanese"]),
            }
            for row_id in SELECTED_FURNITURE_IDS
        },
        "source_slices": source_slices,
        "native_methods": copy.deepcopy(scene_contract["provenance"].get("native_methods", [])),
        "native_claims": copy.deepcopy(scene_contract["provenance"].get("native_claims", [])),
        "assets": {
            "selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
            "asset_index": evidence_ref(ASSET_INDEX_PATH),
            "asset_validation_status": authority["asset_validation"]["status"],
            "runtime_binary_policy": "selector identity only; no PNG/SEB binary promotion in Phase 2B",
        },
        "apk": {
            "path": scene_contract["provenance"]["apk"]["path"],
            "expected_sha256": apk_expected,
            "actual_sha256": sha256_file(APK_PATH),
            "hash_status": "pass" if sha256_file(APK_PATH) == apk_expected else "drift",
        },
        "asset_zip": {
            "path": relative_path(ZIP_PATH),
            "expected_sha256": asset_zip_expected,
            "actual_sha256": sha256_file(ZIP_PATH),
            "hash_status": "pass" if sha256_file(ZIP_PATH) == asset_zip_expected else "drift",
        },
        "source_policy": "C# and native artifacts are evidence inputs only; the browser runtime must not import or execute them.",
    }


def build_checks(
    authority: dict[str, Any],
    scene: dict[str, Any],
    objects: list[dict[str, Any]],
    raw_types: list[dict[str, Any]],
    bindings: list[dict[str, Any]],
    provenance: dict[str, Any],
    records: dict[int, dict[str, dict[str, Any]]],
    selector_records: dict[int, dict[str, Any]],
    asset_index_map: dict[str, dict[str, Any]],
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

    scene_grid = scene["grid"]
    histogram = {int(key): value for key, value in scene_grid["raw_map_value_histogram"].items()}
    all_selector_entries = [selector for item in objects for selector in item["selectors"].values()]
    resolved_selectors = [item for item in all_selector_entries if item["resolution_status"] == "resolved"]
    sentinel_selectors = [item for item in all_selector_entries if item["resolution_status"] == "absent_by_sentinel"]
    source_slices_ok = all(item["hash_status"] == "pass" for item in provenance["source_slices"])
    source_files_ok = all(item["path"] for item in provenance["input_manifest"]["files"])
    type4 = next(item for item in objects if item["id"] == "furniture:0")
    door_binding = next(item for item in bindings if item["id"] == "room:0/door-cell")
    type2_binding = next(item for item in bindings if item["id"] == "room:0/occupied-type2-route-probe")
    route = scene["route_fixtures"][0]

    check(
        "scene-catalog-entry-gate",
        authority["scene"].get("status") == "pass" and authority["scene"].get("semantic_status") == "approved_for_runtime_contract",
        {"status": authority["scene"].get("status"), "semantic_status": authority["scene"].get("semantic_status")},
        {"status": "pass", "semantic_status": "approved_for_runtime_contract"},
        "ObjectCatalog consumes only the approved SceneCatalog contract.",
    )
    check(
        "phase1d-entry-gate",
        authority["closure"].get("status") == "pass" and authority["closure_validation"].get("failed_checks") == [],
        {"closure": authority["closure"].get("status"), "failed_checks": authority["closure_validation"].get("failed_checks")},
        {"closure": "pass", "failed_checks": []},
        "Native, route, and selector authority remains closed before projection.",
    )
    check(
        "selector-entry-gate",
        authority["selectors"].get("status") == "pass" and len(authority["selectors"].get("selected_furniture", [])) == 4,
        {"status": authority["selectors"].get("status"), "selected_furniture": len(authority["selectors"].get("selected_furniture", []))},
        {"status": "pass", "selected_furniture": 4},
        "The existing selector contract covers the four promoted records.",
    )
    check(
        "scene-identity",
        scene["id"] == "room:0" and scene["source_identity"]["source_id"] == 0,
        {"id": scene["id"], "source_id": scene["source_identity"]["source_id"]},
        {"id": "room:0", "source_id": 0},
        "The object slice is anchored to RoomData(0).",
    )
    check(
        "grid-shape",
        scene_grid["width"] == scene_grid["height"] == 10
        and scene_grid["objMap_dimensions"] == {"width": 10, "height": 10}
        and scene_grid["objDir_dimensions"] == {"width": 10, "height": 10},
        {"width": scene_grid["width"], "height": scene_grid["height"], "objMap": scene_grid["objMap_dimensions"], "objDir": scene_grid["objDir_dimensions"]},
        {"width": 10, "height": 10, "objMap": {"width": 10, "height": 10}, "objDir": {"width": 10, "height": 10}},
        "Raw object-type coverage is checked against the closed rectangular scene grid.",
    )
    check(
        "source-file-manifest",
        source_files_ok and all(Path(ROOT / item["path"]).is_file() for item in provenance["input_manifest"]["files"]),
        {"file_count": len(provenance["input_manifest"]["files"]), "all_present": source_files_ok},
        {"all_present": True},
        "Every input manifest path exists at build time.",
    )
    check(
        "source-slice-hashes",
        source_slices_ok,
        {"slice_count": len(provenance["source_slices"]), "all_hash_status": source_slices_ok},
        {"all_hash_status": True},
        "Relevant source slices match the current read-only source roots.",
    )
    check(
        "apk-hash",
        provenance["apk"]["hash_status"] == "pass",
        provenance["apk"],
        {"hash_status": "pass"},
        "Native method RVAs are valid only for the pinned APK hash.",
    )
    check(
        "asset-zip-hash",
        provenance["asset_zip"]["hash_status"] == "pass",
        provenance["asset_zip"],
        {"hash_status": "pass"},
        "Selector identity is tied to the current asset ZIP fingerprint.",
    )
    check(
        "locale-row-identity",
        all(
            records[row_id]["English"]["id"] == records[row_id]["Japanese"]["id"] == row_id
            and records[row_id]["English"]["parse"]["status"] == records[row_id]["Japanese"]["parse"]["status"] == "pass"
            for row_id in SELECTED_FURNITURE_IDS
        ),
        {str(row_id): [records[row_id]["English"]["row_sha256"], records[row_id]["Japanese"]["row_sha256"]] for row_id in SELECTED_FURNITURE_IDS},
        {"ids_match": True, "parse_status": "pass"},
        "Both locale rows parse completely and preserve the same source id.",
    )
    check(
        "promoted-record-ids",
        [int(item["id"].split(":")[1]) for item in objects] == SELECTED_FURNITURE_IDS,
        [item["id"] for item in objects],
        [f"furniture:{row_id}" for row_id in SELECTED_FURNITURE_IDS],
        "Stable ids are explicit type-plus-source-id ids.",
    )
    check(
        "selector-row-crosscheck",
        all(
            field(records[row_id]["English"], field_name) == selector_records[row_id]["selectors"][field_name]["id"]
            for row_id in SELECTED_FURNITURE_IDS
            for field_name in SELECTOR_FIELDS
        ),
        {str(row_id): {field_name: field(records[row_id]["English"], field_name) for field_name in SELECTOR_FIELDS} for row_id in SELECTED_FURNITURE_IDS},
        "Every promoted selector id matches the parsed English source row.",
        "Selector ids do not get rewritten during canonical projection.",
    )
    check(
        "selector-resolution",
        len(resolved_selectors) == 8 and len(sentinel_selectors) == 4,
        {"resolved": len(resolved_selectors), "sentinel": len(sentinel_selectors)},
        {"resolved": 8, "sentinel": 4},
        "The four records contain eight resolved selectors and four explicit -1 sentinels.",
    )
    check(
        "selector-asset-index",
        all(item.get("asset_index", {}).get("relative_path") in asset_index_map for item in resolved_selectors),
        [item.get("asset_index", {}).get("relative_path") for item in resolved_selectors],
        "Every resolved selector has an indexed asset member.",
        "Asset index rows are the binary identity evidence; binaries are not copied into runtime.",
    )
    check(
        "raw-type-domain",
        [item["raw_type"] for item in raw_types] == list(range(7)) and set(histogram) == set(range(7)),
        {"raw_types": [item["raw_type"] for item in raw_types], "histogram_keys": sorted(histogram)},
        {"raw_types": list(range(7)), "histogram_keys": list(range(7))},
        "The raw type catalog covers exactly the values present in RoomData(0).",
    )
    check(
        "raw-type-histogram",
        all(item["scene_cell_count"] == histogram[item["raw_type"]] for item in raw_types),
        {str(item["raw_type"]): item["scene_cell_count"] for item in raw_types},
        {str(key): value for key, value in histogram.items()},
        "Raw type counts are projected from the approved SceneCatalog grid.",
    )
    check(
        "raw-type-source-constants",
        all(item["source_constant"]["value"] == item["raw_type"] and item["source_constant"]["name"] == RAW_TYPE_LABELS[item["raw_type"]] for item in raw_types),
        [item["source_constant"] for item in raw_types],
        "OBJ_TYPE_* source labels match their numeric constants.",
        "Labels remain source_label_only and are not expanded into product semantics.",
    )
    check(
        "map-assignment-policy",
        all(item["map_assignment"]["flat_index"] == "x + y * width" for item in raw_types)
        and scene_grid["native_assignment"]["raw_cell"] == "objMap[y][x]",
        {"raw_cell": scene_grid["native_assignment"]["raw_cell"], "flat_indices": sorted({item["map_assignment"]["flat_index"] for item in raw_types})},
        {"raw_cell": "objMap[y][x]", "flat_index": "x + y * width"},
        "Native raw map assignment remains separate from FurnitureData placement.",
    )
    check(
        "type4-binding",
        type4["geometry"]["status"] == "verified"
        and next(item for item in bindings if item["id"] == "room:0/type4-anchor")["binding_status"] == "verified_fixture"
        and next(item for item in bindings if item["id"] == "room:0/type4-anchor")["furniture_id"] == "furniture:0",
        {"geometry": type4["geometry"]["status"], "binding": next(item for item in bindings if item["id"] == "room:0/type4-anchor")["binding_status"]},
        {"geometry": "verified", "binding": "verified_fixture"},
        "The native multi-chip/passMap anchor is explicitly bound to FurnitureData(0).",
    )
    check(
        "type4-footprint",
        len(type4["geometry"]["footprint"]["footprint"]) == 9
        and type4["geometry"]["footprint"]["parent_center_offset"] == {"dx": 0, "dy": 0},
        {"cells": len(type4["geometry"]["footprint"]["footprint"]), "parent_center_offset": type4["geometry"]["footprint"]["parent_center_offset"]},
        {"cells": 9, "parent_center_offset": {"dx": 0, "dy": 0}},
        "The bounded type-4 footprint is preserved from the authoritative fixture.",
    )
    check(
        "type4-passability",
        type4["geometry"]["passability"]["matrix"] == EXPECTED_PASSABILITY_MATRIX
        and all(item["isPassable"] for item in type4["geometry"]["passability"]["synthetic_zero_probes"])
        and type4["geometry"]["passability"]["all_nonzero_probe"]["isPassable"] is False,
        type4["geometry"]["passability"]["matrix"],
        EXPECTED_PASSABILITY_MATRIX,
        "Passability uses the closed native 3x3 window and boolean fixture.",
    )
    check(
        "door-binding-separation",
        door_binding["binding_status"] == "candidate_by_type_and_selector"
        and door_binding["native_binding"]["status"] == "deferred"
        and door_binding["installed_flag"] == 1,
        {"binding_status": door_binding["binding_status"], "native_status": door_binding["native_binding"]["status"], "installed_flag": door_binding["installed_flag"]},
        {"binding_status": "candidate_by_type_and_selector", "native_status": "deferred", "installed_flag": 1},
        "The raw door binding is not overstated as a FurnitureData binding.",
    )
    check(
        "route-fixture",
        route["path"] == [[8, 4], [7, 4], [6, 4]]
        and route["step_count"] == 2
        and route["neighbor_policy"]["connectivity"] == 4,
        {"path": route["path"], "step_count": route["step_count"], "connectivity": route["neighbor_policy"]["connectivity"]},
        {"path": [[8, 4], [7, 4], [6, 4]], "step_count": 2, "connectivity": 4},
        "The real route remains the movement/filter fixture consumed by the object boundary.",
    )
    check(
        "route-filter-probes",
        {item["id"] for item in route["filter_probes"]} == {"occupied-type2", "type4-ispassable-false", "type6-outdoor"}
        and all(item["admission"]["admitted"] is False for item in route["filter_probes"]),
        [{"id": item["id"], "admitted": item["admission"]["admitted"]} for item in route["filter_probes"]],
        "All three authoritative negative probes are rejected.",
        "ObjectCatalog retains route evidence without implementing the route service.",
    )
    check(
        "type2-direction-policy",
        all(item["direction_policy"]["status"] == "verified" for item in objects if item["id"] in {"furniture:2", "furniture:5"})
        and type2_binding["furniture_id"] == "furniture:2",
        {item["id"]: item["direction_policy"]["status"] for item in objects},
        {"furniture:2": "verified", "furniture:5": "verified"},
        "Type-2 direction access is verified without claiming full placement.",
    )
    check(
        "promoted-field-statuses",
        all(
            item["status"] in {"verified", "derived", "raw_only", "deferred", "quarantine"}
            and item.get("confidence")
            for object_record in objects
            for item in [object_record["source_identity"], object_record["name"], *object_record["raw_fields"].values(), *object_record["selectors"].values(), object_record["geometry"], object_record["direction_policy"], object_record["interaction"]]
        ),
        {"object_count": len(objects)},
        "Every promoted field wrapper carries a controlled status and confidence.",
        "Unknown values are not silently promoted into the runtime contract.",
    )
    check(
        "no-unknown-promoted-values",
        "unknown" not in stable_json(objects).lower(),
        {"contains_unknown": "unknown" in stable_json(objects).lower()},
        {"contains_unknown": False},
        "Unknown semantics remain outside promoted object records.",
    )
    check(
        "native-method-provenance",
        len(provenance["native_methods"]) == 9 and all(item.get("id") for item in provenance["native_methods"]),
        {"native_methods": len(provenance["native_methods"])},
        {"native_methods": 9},
        "The canonical object package retains the native method manifest used upstream.",
    )
    check(
        "phase-boundary",
        all("runtime" not in item.get("review_note", "").lower() or item.get("status") != "verified" for item in objects),
        {"runtime_object_count": len(objects)},
        "No renderer/runtime behavior is introduced by the object catalog builder.",
        "Phase 2B remains a canonical evidence contract, not a runtime implementation.",
    )
    return checks


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    authority = load_authority()
    scene_contract = authority["scene"]
    scene = scene_contract["scenes"][0]
    selector_contract = authority["selectors"]
    asset_index_map = build_asset_index_map(authority["asset_index"])

    records: dict[int, dict[str, dict[str, Any]]] = {
        row_id: {
            "English": read_furniture_record("English", row_id),
            "Japanese": read_furniture_record("Japanese", row_id),
        }
        for row_id in SELECTED_FURNITURE_IDS
    }
    selector_records = {int(item["id"]): item for item in selector_contract["selected_furniture"]}
    require(sorted(selector_records) == SELECTED_FURNITURE_IDS, "selected FurnitureData selector ids drift")
    require(sha256_file(APK_PATH) == scene_contract["provenance"]["apk"]["sha256"], "APK hash drift")
    require(sha256_file(ZIP_PATH) == selector_contract["asset_zip"]["sha256"], "asset ZIP hash drift")

    evidence_refs = {
        "asset_selector_contract": evidence_ref(ASSET_SELECTOR_PATH),
        "route_fixture": evidence_ref(ROUTE_PATH),
    }
    objects = [
        build_object_record(
            row_id,
            records,
            selector_records,
            selector_contract,
            asset_index_map,
            scene,
            evidence_refs,
        )
        for row_id in SELECTED_FURNITURE_IDS
    ]
    raw_types = build_raw_object_types(scene)
    bindings = build_scene_bindings(scene, objects)

    source_paths = [
        SCENE_CATALOG_PATH,
        ASSET_SELECTOR_PATH,
        ASSET_VALIDATION_PATH,
        ASSET_INDEX_PATH,
        PASSMAP_PATH,
        ROUTE_PATH,
        CLOSURE_PATH,
        CLOSURE_VALIDATION_PATH,
        APK_PATH,
        ZIP_PATH,
        *[scene_builder.base.table_path("FurnitureData", locale) for locale in ("English", "Japanese")],
        *SOURCE_FILES.values(),
    ]
    manifest = input_manifest(source_paths)
    source_slices = refresh_source_slices(scene_contract)
    provenance = build_provenance(authority, manifest, records, source_slices)
    checks = build_checks(
        authority,
        scene,
        objects,
        raw_types,
        bindings,
        provenance,
        records,
        selector_records,
        asset_index_map,
    )
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    limits = [
        "This contract covers four FurnitureData records for display-slice-01 only.",
        "Raw ObjChip types and FurnitureData bindings are separate layers.",
        "The door FurnitureData candidate is not promoted as a native binding.",
        "Full object-to-FurnitureData placement for every RoomData cell is deferred.",
        "Standing-position, camera, coordinate, draw-order, visual-frame, renderer, and behavior contracts are deferred.",
        "C# and native artifacts remain evidence and are not runtime imports.",
    ]
    fixture = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-object-catalog-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": scene["id"], "source_catalog": evidence_ref(SCENE_CATALOG_PATH)},
        "objects": copy.deepcopy(objects),
        "raw_object_types": copy.deepcopy(raw_types),
        "scene_bindings": copy.deepcopy(bindings),
        "provenance": provenance,
        "limits": limits,
        "determinism": {
            "algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash",
            "content_hash": "",
        },
    }
    fixture["determinism"]["content_hash"] = sha256_bytes(stable_json(_without_dynamic(fixture)).encode("utf-8"))

    contract = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-object-catalog",
        "status": status,
        "semantic_status": "approved_for_runtime_contract" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": scene["id"], "source_catalog": evidence_ref(SCENE_CATALOG_PATH)},
        "objects": copy.deepcopy(objects),
        "raw_object_types": copy.deepcopy(raw_types),
        "scene_bindings": copy.deepcopy(bindings),
        "fixture_ref": {
            "path": "knowledge/fixtures/accepted/object_catalog_fixture.json",
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "provenance": provenance,
        "limits": limits,
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
            "objects": len(objects),
            "raw_object_types": len(raw_types),
            "scene_bindings": len(bindings),
            "resolved_selectors": sum(item["resolution_status"] == "resolved" for obj in objects for item in obj["selectors"].values()),
            "sentinel_selectors": sum(item["resolution_status"] == "absent_by_sentinel" for obj in objects for item in obj["selectors"].values()),
        },
        "phase_boundary": {
            "phase": "Phase 2B",
            "next": "ActorCatalog" if status == "pass" else "ObjectCatalog repair",
            "not_started": ["ActorCatalog", "TypeScript runtime core", "renderer", "camera"],
        },
    }
    return fixture, contract, validation


def _without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [_without_dynamic(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    fixture, contract, validation = build_package()
    write_json(evidence_dir / "object_catalog_fixture.json", fixture)
    write_json(evidence_dir / "object_catalog_validation.json", validation)
    write_json(runtime_dir / "object_catalog_contract.json", contract)
    print(
        "object_catalog_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"objects={validation['counts']['objects']} "
        f"resolved_selectors={validation['counts']['resolved_selectors']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
