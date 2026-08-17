"""Build loader-aware scene and staff-behavior evidence for Social Dev.

This tool parses only the selected first-slice rows using the reader order
already observed in the C# evidence. The output remains a candidate package;
it is not a runtime catalog and does not execute decompiled C#.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
CATALOG = EVIDENCE / "csharp_update_inventory"
TABLE_ROOT = ROOT / "knowledge/sources/asset_guide_20260813/01_GAME_PACKS/xls"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"
DEFAULT_OUTPUT = EVIDENCE

TABLE_NAMES = {
    "RoomData": "room.txt",
    "FurnitureData": "furniture.txt",
    "StaffData": "staff.txt",
    "JobData": "job.txt",
    "SkillData": "skill.txt",
}
BASE_IDS = {
    "RoomData": [0],
    "FurnitureData": [1, 2, 5],
    "StaffData": [0, 1, 2, 3, 4],
}

SOURCE_FILES = {
    "RoomData": "data/RoomData.cs",
    "FurnitureData": "data/FurnitureData.cs",
    "StaffData": "data/StaffData.cs",
    "JobData": "data/JobData.cs",
    "SkillData": "data/SkillData.cs",
    "Room": "game/Room.cs",
    "MapChip": "game/MapChip.cs",
    "ObjChip": "game/ObjChip.cs",
    "Staff": "game/Staff.cs",
    "Astar": "game.routeSearch/Astar.cs",
    "Node": "game.routeSearch/Node.cs",
}
STRING_ARRAY_STREAM = SOURCE_ROOT / "ext.util/StringArrayStream.cs"

SCENE_SLICES = [
    ("Room", 20, 104, "room constants and fields"),
    ("Room", 208, 453, "map-chip grid initialization"),
    ("Room", 454, 763, "object-chip grid initialization and big-chip parent setup"),
    ("Room", 764, 923, "door scan and placement"),
    ("Room", 6168, 6227, "index-to-screen coordinate formulas"),
    ("MapChip", 12, 235, "map-chip dimensions and draw path"),
    ("ObjChip", 18, 116, "object types, directions and dimensions"),
    ("ObjChip", 10397, 10859, "standing positions, occupancy and passability hooks"),
    ("Astar", 11, 230, "node-array construction and goal flags"),
    ("Astar", 1521, 1716, "neighbor connection and node lookup"),
    ("Node", 7, 75, "node position and Manhattan cost candidate"),
    ("RoomData", 10, 62, "room data fields and loader"),
    ("FurnitureData", 11, 178, "furniture data fields and loader"),
]

BEHAVIOR_SLICES = [
    ("Staff", 22, 396, "staff constants and visible state fields"),
    ("Staff", 421, 884, "staff initialization defaults and data links"),
    ("Staff", 1216, 1940, "staff update dispatcher and health/movement branch"),
    ("Staff", 1941, 2058, "stay-home and move update"),
    ("Staff", 2059, 2175, "talk timing branch"),
    ("Staff", 2703, 2993, "work decisions and typing/equipment/talk branches"),
    ("Staff", 2994, 3059, "talk/equipment destination selection"),
    ("Staff", 4714, 5243, "route search, node movement and arrival callbacks"),
    ("Staff", 7705, 7713, "state mutation boundary"),
    ("Staff", 9404, 9526, "position and route API boundary"),
    ("Staff", 10309, 10406, "typing animation boundary"),
    ("Staff", 10599, 10608, "state/move read boundary"),
    ("StaffData", 11, 116, "staff data fields and loader"),
    ("JobData", 7, 71, "job fields and loader"),
    ("SkillData", 10, 140, "skill fields, constants and loader"),
]

SCHEMA_VERSION = "social-dev-scene-behavior-candidates-v1"
VALIDATION_VERSION = "social-dev-scene-behavior-validation-v1"


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


def normalise_path(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def relative_path(path: Path | str) -> str:
    path = Path(path)
    try:
        return normalise_path(path.relative_to(ROOT))
    except ValueError:
        return normalise_path(path)


def table_path(type_name: str, locale: str) -> Path:
    path = TABLE_ROOT / f"{locale}.lproj" / TABLE_NAMES[type_name]
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path


def read_table(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            raw_line = raw_line.rstrip("\r\n")
            if not raw_line:
                continue
            columns = raw_line.split("\t")
            try:
                row_id: int | None = int(columns[0])
            except (ValueError, IndexError):
                row_id = None
            rows.append(
                {
                    "row_number": line_number,
                    "raw_line": raw_line,
                    "columns": columns,
                    "id": row_id,
                    "row_sha256": sha256_bytes(raw_line.encode("utf-8")),
                }
            )
    return rows


class LoaderCursor:
    """Parse the small reader subset used by the selected data classes."""

    def __init__(self, columns: list[str]) -> None:
        self.columns = columns
        self.pos = 0
        self.errors: list[str] = []

    def take(self, reader: str) -> tuple[Any, int, int]:
        start = self.pos
        if reader in {"GetInt", "GetByte", "GetShort", "GetLong"}:
            if self.pos >= len(self.columns):
                raise IndexError(f"{reader} at end of row")
            value = int(self.columns[self.pos])
            self.pos += 1
            return value, start, self.pos
        if reader == "GetString":
            if self.pos >= len(self.columns):
                raise IndexError("GetString at end of row")
            value = self.columns[self.pos]
            self.pos += 1
            return value, start, self.pos
        if reader == "GetIntArray":
            count = self._take_int("GetIntArray length")
            if count < 0:
                return None, start, self.pos
            values = [self._take_int("GetIntArray value") for _ in range(count)]
            return values, start, self.pos
        if reader == "GetIntIntArray":
            row_count = self._take_int("GetIntIntArray row count")
            if row_count < 0:
                return None, start, self.pos
            rows: list[list[int]] = []
            for row_index in range(row_count):
                row_length = self._take_int(f"GetIntIntArray row {row_index} length")
                if row_length < 0:
                    self.errors.append(f"negative nested row length at {row_index}")
                    rows.append([])
                    continue
                rows.append(
                    [self._take_int(f"GetIntIntArray row {row_index} value") for _ in range(row_length)]
                )
            return rows, start, self.pos
        raise ValueError(f"unsupported reader: {reader}")

    def _take_int(self, context: str) -> int:
        if self.pos >= len(self.columns):
            raise IndexError(f"{context} at end of row")
        try:
            value = int(self.columns[self.pos])
        except ValueError as exc:
            raise ValueError(f"{context} is not an integer: {self.columns[self.pos]!r}") from exc
        self.pos += 1
        return value


def find_field_load(rows: list[dict[str, Any]], type_name: str) -> dict[str, Any]:
    for row in rows:
        if row.get("type") == type_name:
            return row
    raise KeyError(f"missing field-load evidence for {type_name}")


def find_type_source(rows: list[dict[str, Any]], type_name: str) -> dict[str, Any]:
    for row in rows:
        if row.get("name") == type_name:
            return row
    raise KeyError(f"missing type catalog evidence for {type_name}")


def parse_row(
    type_name: str,
    locale: str,
    row: dict[str, Any],
    field_load: dict[str, Any],
    type_source: dict[str, Any],
    table_file: Path,
) -> dict[str, Any]:
    pairs = field_load.get("pairs") or []
    cursor = LoaderCursor(row["columns"])
    parsed_fields: dict[str, Any] = {}
    errors: list[str] = []
    for pair in pairs:
        field = str(pair["field"])
        reader = str(pair["reader"])
        try:
            value, start, end = cursor.take(reader)
        except (IndexError, ValueError) as exc:
            errors.append(f"{field}/{reader}: {exc}")
            break
        parsed_fields[field] = {
            "reader": reader,
            "token_start": start,
            "token_end_exclusive": end,
            "value": value,
            "mapping_status": "order_candidate",
            "semantic_status": "unknown",
        }
    errors.extend(cursor.errors)
    if cursor.pos != len(row["columns"]):
        errors.append(f"unconsumed_columns={len(row['columns']) - cursor.pos}")
    return {
        "type": type_name,
        "locale": locale,
        "id": row["id"],
        "status": "candidate" if not errors else "parse_error",
        "semantic_status": "pending_review",
        "table_path": relative_path(table_file),
        "row_number": row["row_number"],
        "row_sha256": row["row_sha256"],
        "column_count": len(row["columns"]),
        "raw_columns": row["columns"],
        "parsed_fields": parsed_fields,
        "parse": {
            "reader_sequence": [pair["reader"] for pair in pairs],
            "field_sequence": [pair["field"] for pair in pairs],
            "consumed_columns": cursor.pos,
            "remaining_columns": len(row["columns"]) - cursor.pos,
            "errors": errors,
            "status": "pass" if not errors else "fail",
        },
        "csharp_source_ref": {
            "file": normalise_path(type_source["source"]["file"]),
            "line_start": type_source["source"].get("line_start"),
            "line_end": type_source["source"].get("line_end"),
            "source_hash": type_source.get("source_hash"),
        },
    }


def value(record: dict[str, Any], field: str, default: Any = None) -> Any:
    return record.get("parsed_fields", {}).get(field, {}).get("value", default)


def find_record(records: list[dict[str, Any]], type_name: str, locale: str, row_id: int) -> dict[str, Any]:
    for record in records:
        if record["type"] == type_name and record["locale"] == locale and record["id"] == row_id:
            return record
    raise KeyError(f"missing parsed record {type_name}/{locale}/{row_id}")


def source_file(type_name: str) -> Path:
    path = SOURCE_ROOT / SOURCE_FILES[type_name]
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path


def source_slice(type_name: str, start: int, end: int, purpose: str) -> dict[str, Any]:
    path = source_file(type_name)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if start < 1 or end > len(lines) or start > end:
        raise ValueError(f"invalid source slice {type_name}:{start}-{end}")
    text = "".join(lines[start - 1 : end])
    return {
        "type": type_name,
        "file": relative_path(path),
        "line_start": start,
        "line_end": end,
        "purpose": purpose,
        "slice_sha256": sha256_bytes(text.encode("utf-8")),
        "file_sha256": sha256_file(path),
        "il_marker_count": text.count("//IL_"),
        "status": "evidence_only",
    }


def build_slices(specs: list[tuple[str, int, int, str]]) -> list[dict[str, Any]]:
    return [source_slice(*spec) for spec in specs]


def extract_constants(type_name: str, names: list[str]) -> list[dict[str, Any]]:
    path = source_file(type_name)
    lines = path.read_text(encoding="utf-8").splitlines()
    wanted = set(names)
    result: list[dict[str, Any]] = []
    pattern = re.compile(r"^\s*public const (?:int|bool) (?P<name>[A-Za-z0-9_]+) = (?P<value>-?[0-9]+|true|false);")
    for line_number, line in enumerate(lines, start=1):
        match = pattern.match(line)
        if not match or match.group("name") not in wanted:
            continue
        raw_value = match.group("value")
        if raw_value in {"true", "false"}:
            parsed_value: int | bool = raw_value == "true"
        else:
            parsed_value = int(raw_value)
        result.append(
            {
                "name": match.group("name"),
                "value": parsed_value,
                "source_ref": {
                    "file": relative_path(path),
                    "line_start": line_number,
                    "line_end": line_number,
                    "source_hash": sha256_file(path),
                },
                "semantic_status": "source_label_only",
            }
        )
    missing = wanted - {item["name"] for item in result}
    if missing:
        raise KeyError(f"missing constants in {type_name}: {sorted(missing)}")
    return result


def input_manifest(paths: list[Path]) -> dict[str, Any]:
    files = []
    for path in sorted(set(paths), key=lambda item: str(item)):
        if not path.is_file():
            raise FileNotFoundError(str(path))
        files.append({"path": relative_path(path), "sha256": sha256_file(path)})
    return {
        "files": files,
        "input_hash": sha256_bytes(stable_json(files).encode("utf-8")),
    }


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_candidates(output_dir: Path | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Build candidate payloads without mutating evidence files.

    ``output_dir`` remains an optional compatibility argument for callers that
    used the old signature.  Artifact writes belong to the CLI entry point so
    tests and downstream builders cannot change provenance hashes merely by
    rebuilding an in-memory candidate package.
    """
    candidate = load_json(EVIDENCE / "first_slice_data_candidate.json")
    field_load = load_json(EVIDENCE / "field_load_candidates.json")
    load_contract = load_json(EVIDENCE / "load_contract_candidates.json")
    type_catalog = load_json(CATALOG / "type_catalog.json")
    asset_validation = load_json(EVIDENCE / "asset_validation_gate.json")

    selected_ids = dict(BASE_IDS)
    table_cache: dict[tuple[str, str], list[dict[str, Any]]] = {}
    parsed_records: list[dict[str, Any]] = []
    input_paths: list[Path] = [
        EVIDENCE / "first_slice_data_candidate.json",
        EVIDENCE / "field_load_candidates.json",
        EVIDENCE / "load_contract_candidates.json",
        CATALOG / "type_catalog.json",
        EVIDENCE / "asset_validation_gate.json",
        STRING_ARRAY_STREAM,
    ]
    type_rows = type_catalog["records"]

    def parse_selected(type_name: str, ids: list[int]) -> None:
        field_row = find_field_load(field_load["rows"], type_name)
        type_source = find_type_source(type_rows, type_name)
        for locale in ("English", "Japanese"):
            path = table_path(type_name, locale)
            input_paths.append(path)
            rows = read_table(path)
            table_cache[(type_name, locale)] = rows
            for row_id in ids:
                matches = [row for row in rows if row["id"] == row_id]
                if not matches:
                    parsed_records.append(
                        {
                            "type": type_name,
                            "locale": locale,
                            "id": row_id,
                            "status": "missing",
                            "semantic_status": "unknown",
                            "table_path": relative_path(path),
                        }
                    )
                    continue
                parsed_records.append(parse_row(type_name, locale, matches[0], field_row, type_source, path))

    for type_name, ids in BASE_IDS.items():
        parse_selected(type_name, ids)

    staff_english = [
        find_record(parsed_records, "StaffData", "English", staff_id)
        for staff_id in BASE_IDS["StaffData"]
    ]
    job_ids = sorted({int(value(record, "jobId_")) for record in staff_english})
    skill_ids = sorted({int(value(record, "skill_")) for record in staff_english})
    selected_ids["JobData"] = job_ids
    selected_ids["SkillData"] = skill_ids
    parse_selected("JobData", job_ids)
    parse_selected("SkillData", skill_ids)

    room = find_record(parsed_records, "RoomData", "English", 0)
    obj_map = value(room, "objMap_", [])
    obj_dir = value(room, "objDir_", [])
    room_width = len(obj_map[0]) if obj_map else 0
    room_height = len(obj_map)
    direction_width = len(obj_dir[0]) if obj_dir else 0
    direction_height = len(obj_dir)
    value_histogram = Counter(str(cell) for row in obj_map for cell in row)

    obj_type_constants = extract_constants(
        "ObjChip",
        [
            "OBJ_TYPE_PASS",
            "OBJ_TYPE_EQUIP",
            "OBJ_TYPE_DESK",
            "OBJ_TYPE_BIG",
            "OBJ_TYPE_BIG_CENTER",
            "OBJ_TYPE_DOOR",
            "OBJ_TYPE_OUTDOOR",
        ],
    )
    obj_type_values = {item["name"]: item["value"] for item in obj_type_constants}
    door_value = obj_type_values["OBJ_TYPE_DOOR"]
    door_cells = [
        {"x": x, "y": y, "raw_map_value": cell}
        for y, row in enumerate(obj_map)
        for x, cell in enumerate(row)
        if cell == door_value
    ]

    furniture_records = [
        find_record(parsed_records, "FurnitureData", "English", furniture_id)
        for furniture_id in BASE_IDS["FurnitureData"]
    ]
    furniture_projection = []
    for record in furniture_records:
        furniture_projection.append(
            {
                "id": record["id"],
                "name": value(record, "name_"),
                "category": value(record, "category_"),
                "type": value(record, "type_"),
                "seb": value(record, "seb_"),
                "subSeb": value(record, "subSeb_"),
                "img": value(record, "img_"),
                "flag": value(record, "flag_"),
                "terms": value(record, "terms_"),
                "useBonus": value(record, "useBonus_"),
                "passMap": value(record, "passMap_"),
                "selector_status": "unverified",
                "source_record_ref": {
                    "table_path": record["table_path"],
                    "row_number": record["row_number"],
                    "row_sha256": record["row_sha256"],
                },
            }
        )

    scene_input_paths = list(input_paths)
    for type_name, _, _, _ in SCENE_SLICES:
        scene_input_paths.append(source_file(type_name))
    scene_input_paths.extend(
        [
            ROOT / "knowledge/sources/asset_guide_20260813/05_ASSEMBLY_GUIDE/09_WORLD_CHIP_ASSEMBLY.md",
            ROOT / "knowledge/sources/asset_guide_20260813/05_ASSEMBLY_GUIDE/10_COORDINATE_AND_LAYER_RULES.md",
        ]
    )
    behavior_input_paths = list(input_paths)
    for type_name, _, _, _ in BEHAVIOR_SLICES:
        behavior_input_paths.append(source_file(type_name))
    behavior_input_paths.append(ROOT / "knowledge/sources/asset_guide_20260813/05_ASSEMBLY_GUIDE/07_CHARACTER_ASSEMBLY.md")

    timestamp = now_utc()
    scene = {
        "schema_version": SCHEMA_VERSION,
        "package": "scene",
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": timestamp,
        "input_manifest": input_manifest(scene_input_paths),
        "loader_parser": {
            "status": "candidate",
            "source": "ext.util/StringArrayStream.cs reader behavior plus field-load pairs",
            "source_ref": {
                "file": relative_path(STRING_ARRAY_STREAM),
                "sha256": sha256_file(STRING_ARRAY_STREAM),
            },
            "supported_readers": ["GetInt", "GetString", "GetIntArray", "GetIntIntArray"],
            "negative_array_length": "candidate_null_sentinel",
            "row_exhaustion_required": True,
            "semantic_status": "pending_review",
        },
        "room": {
            "type": "RoomData",
            "id": 0,
            "name": value(room, "name_"),
            "scalar_fields": {
                field: room["parsed_fields"][field]
                for field in [
                    "id_",
                    "name_",
                    "costMoney_",
                    "costCoin_",
                    "deskNum_",
                    "equipSmallNum_",
                    "equipBigNum_",
                    "floorImgId_",
                    "wallImgId_",
                    "doorImgId_",
                    "flag_",
                    "costMax_",
                ]
            },
            "objMap": obj_map,
            "objDir": obj_dir,
            "grid_shape": {
                "objMap_width": room_width,
                "objMap_height": room_height,
                "objDir_width": direction_width,
                "objDir_height": direction_height,
            },
            "raw_map_value_histogram": dict(sorted(value_histogram.items(), key=lambda item: int(item[0]))),
            "cells": [
                {
                    "x": x,
                    "y": y,
                    "raw_map_value": cell,
                    "raw_dir_value": obj_dir[y][x] if y < len(obj_dir) and x < len(obj_dir[y]) else None,
                    "semantic_status": "unknown",
                }
                for y, row in enumerate(obj_map)
                for x, cell in enumerate(row)
            ],
            "door_cells_by_code_candidate": {
                "raw_code": door_value,
                "cells": door_cells,
                "relation_status": "order_candidate",
                "note": "Room.PlaceDoor scans ObjChip type 5; objMap-to-type assignment remains a bounded candidate.",
            },
            "source_record_ref": {
                "table_path": room["table_path"],
                "row_number": room["row_number"],
                "row_sha256": room["row_sha256"],
            },
        },
        "furniture": {
            "type": "FurnitureData",
            "records": furniture_projection,
            "placement_status": "unverified",
        },
        "coordinate_contract_candidate": {
            "room_index_to_world": {
                "x": "(index.x + index.y) * 20 + 20",
                "y": "(index.y - index.x) * 10 + 18",
                "source_status": "source_observed",
                "semantic_status": "pending_review",
            },
            "map_chip": {
                "width": 80,
                "height": 39,
                "source_status": "source_constant",
            },
            "obj_chip": {
                "width": 40,
                "height": 19,
                "source_status": "source_constant",
            },
            "floor_height": 180,
            "source_status": "source_constant",
        },
        "object_type_constants": obj_type_constants,
        "route_fixture_candidate": {
            "status": "unverified",
            "start": door_cells[0] if door_cells else None,
            "goal_candidates": [
                {"x": x, "y": y, "raw_map_value": cell}
                for y, row in enumerate(obj_map)
                for x, cell in enumerate(row)
                if cell == obj_type_values["OBJ_TYPE_DESK"]
            ],
            "required_before_path_assertion": ["passability_semantics", "neighbor_policy", "goal_filter"],
            "note": "A route path is intentionally not generated from raw codes alone.",
        },
        "source_slices": build_slices(SCENE_SLICES),
        "review_items": [
            {
                "id": "room-map-code-semantic",
                "status": "unknown",
                "blocking": True,
                "action": "Confirm objMap cell values become ObjChip type values in the runtime construction path.",
            },
            {
                "id": "room-placement-missing",
                "status": "unknown",
                "blocking": True,
                "action": "Find persisted/generated furniture placement that binds FurnitureData ids to RoomData(0) cells.",
            },
            {
                "id": "passability-unresolved",
                "status": "unknown",
                "blocking": True,
                "action": "Resolve ObjChip.IsPassable and FurnitureData.passMap_ semantics before route fixture promotion.",
            },
            {
                "id": "asset-selector-unverified",
                "status": "quarantine",
                "blocking": True,
                "action": "Resolve seb/subSeb/img to asset source relationships before runtime promotion.",
            },
        ],
        "asset_validation_status": asset_validation.get("status"),
    }

    staff_records = [
        find_record(parsed_records, "StaffData", "English", staff_id)
        for staff_id in BASE_IDS["StaffData"]
    ]
    staff_projection = []
    for record in staff_records:
        staff_projection.append(
            {
                "id": record["id"],
                "lastName": value(record, "lastName_"),
                "firstName": value(record, "firstName_"),
                "img": value(record, "img_"),
                "rank": value(record, "rank_"),
                "jobId": value(record, "jobId_"),
                "favorite": value(record, "favorite_"),
                "hobby": value(record, "hobby_"),
                "defParams": value(record, "defParams_"),
                "area": value(record, "area_"),
                "flag": value(record, "flag_"),
                "evolveMaxNum": value(record, "evolveMaxNum_"),
                "cost": value(record, "cost_"),
                "skillId": value(record, "skill_"),
                "hitRate": value(record, "hitRate_"),
                "bonusTerms": value(record, "bonusTerms_"),
                "bonusRate": value(record, "bonusRate_"),
                "record_parse_status": record["parse"]["status"],
                "source_record_ref": {
                    "table_path": record["table_path"],
                    "row_number": record["row_number"],
                    "row_sha256": record["row_sha256"],
                },
            }
        )

    state_names = [
        "STATE_NORMAL",
        "STATE_MEETING",
        "STATE_MOVE",
        "STATE_SIT_DOWN",
        "STATE_WORK",
        "STATE_USE_EQUIPMENT",
        "STATE_TALK",
        "STATE_INVITE_TO_TALK",
        "STATE_FLY_AWAY",
        "STATE_WAIT",
        "STATE_WANDER",
        "STATE_WAIT_BACK_OF_DOOR",
        "STATE_DEVELOP",
        "STATE_STAY_HOME",
    ]
    move_names = [
        "MOVE_MODE_STAY",
        "MOVE_MODE_GOTO_EQUIPMENT",
        "MOVE_MODE_WANDER",
        "MOVE_MODE_GOTO_DESK",
        "MOVE_MODE_INTO_EQUIPMENT",
        "MOVE_MODE_OUTOF_EQUIPMENT",
        "MOVE_MODE_SIT_DOWN",
        "MOVE_MODE_TO_STAFF",
        "MOVE_MODE_TO_STAND_TALKING",
        "MOVE_MODE_TO_BACK_OF_CHAIR",
        "MOVE_MODE_GO_TO_DOOR",
        "MOVE_MODE_GO_HOME",
    ]
    flag_names = [
        "FLAG_SITTING",
        "FLAG_RESERVED_TALK",
        "FLAG_INVITED_TALK",
        "FLAG_TYPING",
        "FLAG_SLEEPING",
        "FLAG_PLANNING",
        "FLAG_PLANNING_COMPLETED",
        "FLAG_WAITING_ROOM",
        "FLAG_LEADER",
    ]
    staff_constants = extract_constants("Staff", state_names + move_names + flag_names)
    staff_constant_values = {item["name"]: item["value"] for item in staff_constants}
    astar_constants = extract_constants("Astar", ["FLAG_GOAL_IS_DESK", "FLAG_GOAL_IS_EQUIP", "FLAG_GOAL_IS_STAFF"])

    transition_candidates = [
        {
            "id": "stay-home-to-door",
            "kind": "bounded_branch_observation",
            "when": "UpdateStayHome hpRatio >= 40",
            "writes": {"state_": staff_constant_values["STATE_WAIT_BACK_OF_DOOR"], "moveMode_": staff_constant_values["MOVE_MODE_GOTO_DESK"]},
            "side_effect": "reserve room door use",
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 1941, "line_end": 1954},
            "semantic_status": "pending_review",
        },
        {
            "id": "work-to-equipment",
            "kind": "bounded_branch_observation",
            "when": "GotoEquip selects an available equipment object",
            "writes": {"state_": staff_constant_values["STATE_MOVE"], "moveMode_": staff_constant_values["MOVE_MODE_GOTO_EQUIPMENT"]},
            "side_effect": "reserve object use",
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 3038, "line_end": 3059},
            "semantic_status": "pending_review",
        },
        {
            "id": "work-to-talk",
            "kind": "bounded_branch_observation",
            "when": "GotoTalk finds a staff at a usable desk",
            "writes": {"state_": staff_constant_values["STATE_MOVE"], "moveMode_": staff_constant_values["MOVE_MODE_TO_STAFF"]},
            "side_effect": "set colleague ids and talk flags on both staff",
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 2994, "line_end": 3037},
            "semantic_status": "pending_review",
        },
        {
            "id": "move-route-dispatch",
            "kind": "goal-flag-mapping",
            "mapping": {
                "MOVE_MODE_GOTO_EQUIPMENT": {"value": staff_constant_values["MOVE_MODE_GOTO_EQUIPMENT"], "astar_flag": astar_constants[1]["value"]},
                "MOVE_MODE_TO_STAFF": {"value": staff_constant_values["MOVE_MODE_TO_STAFF"], "astar_flag": astar_constants[2]["value"]},
                "MOVE_MODE_GOTO_DESK": {"value": staff_constant_values["MOVE_MODE_GOTO_DESK"], "astar_flag": astar_constants[0]["value"]},
            },
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 9474, "line_end": 9519},
            "semantic_status": "pending_review",
        },
        {
            "id": "route-consumption",
            "kind": "bounded_lifecycle_observation",
            "sequence": ["route node selected", "Move", "OnArriveNextNode", "ReadyToNextNode or OnArriveGoal"],
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 4817, "line_end": 5243},
            "semantic_status": "pending_review",
        },
        {
            "id": "talk-timing",
            "kind": "visible-timer-observation",
            "frame_markers": [20, 70, 110, 130],
            "terminal_effect": "clear talk flags and GotoDesk at frame >= 130",
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 2059, "line_end": 2175},
            "semantic_status": "pending_review",
        },
        {
            "id": "typing-animation",
            "kind": "animation-selector-observation",
            "start": {"flag": staff_constant_values["FLAG_TYPING"], "typingFrame": 100, "sebFrameInterval": 3, "seb_formula": "reverseDirection + 23"},
            "end": {"flag_cleared": staff_constant_values["FLAG_TYPING"], "sebFrameInterval": 1, "seb_formula": "reverseDirection + 10"},
            "source_ref": {"file": "sources/raw/1_Click_CSharp_Code update/game/Staff.cs", "line_start": 10309, "line_end": 10406},
            "semantic_status": "pending_review",
        },
    ]

    behavior = {
        "schema_version": SCHEMA_VERSION,
        "package": "staff_behavior",
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": timestamp,
        "input_manifest": input_manifest(behavior_input_paths),
        "loader_parser_source_ref": {
            "file": relative_path(STRING_ARRAY_STREAM),
            "sha256": sha256_file(STRING_ARRAY_STREAM),
        },
        "selection": {
            "staff_ids": BASE_IDS["StaffData"],
            "job_ids": job_ids,
            "skill_ids": skill_ids,
            "skill_link_status": "order_candidate",
            "note": "skill_ is parsed after defParams_/hitRate_/bonusTerms_ framing and assigned to Staff.skillId_ in Staff.Init; product relation remains pending review.",
        },
        "records": {
            "staff": staff_projection,
            "job": [find_record(parsed_records, "JobData", "English", job_id) for job_id in job_ids],
            "skill": [find_record(parsed_records, "SkillData", "English", skill_id) for skill_id in skill_ids],
        },
        "visible_field_contract_candidate": [
            {"field": field, "owner": "Staff", "semantic_status": "source_field_only"}
            for field in ["id_", "x_", "y_", "sebId_", "sebFrame_", "sebFrameInterval_", "route_", "room_", "objIndex_", "moveMode_", "deskId_", "colleagueId_", "flag_", "oldState_", "oldSebId_"]
        ],
        "state_constants": staff_constants,
        "route_goal_constants": astar_constants,
        "transition_candidates": transition_candidates,
        "animation_contract_candidate": {
            "selector_fields": ["sebId_", "sebFrame_", "sebFrameInterval_", "scale_", "alpha_"],
            "asset_selector_status": "unverified",
            "source_status": "bounded source observations only",
        },
        "source_slices": build_slices(BEHAVIOR_SLICES),
        "review_items": [
            {
                "id": "numeric-state-labels",
                "status": "unknown",
                "blocking": True,
                "action": "Keep source labels and numeric values until transition traces or assembly evidence confirm product semantics.",
            },
            {
                "id": "decompiler-update-body",
                "status": "quarantine",
                "blocking": True,
                "action": "Use these observations as rewrite inputs; do not port Staff.Update or Astar.SearchRoute body.",
            },
            {
                "id": "skill-reference-promotion",
                "status": "unknown",
                "blocking": True,
                "action": "Confirm DataManager skill lookup and skill id semantics before canonical ActorCatalog promotion.",
            },
            {
                "id": "animation-selector-promotion",
                "status": "quarantine",
                "blocking": True,
                "action": "Resolve seb id to human asset source and frame contract.",
            },
        ],
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

    required_types = set(BASE_IDS) | {"JobData", "SkillData"}
    parsed_type_ids = {(record["type"], record["id"]) for record in parsed_records if record["status"] == "candidate"}
    required_type_ids = {
        (type_name, row_id)
        for type_name, ids in selected_ids.items()
        for row_id in ids
    }
    check("selected-records-present", required_type_ids.issubset(parsed_type_ids), sorted(required_type_ids - parsed_type_ids), "empty", "All derived first-slice records exist in both locales.")
    check("loader-row-exhaustion", all(record["parse"]["status"] == "pass" for record in parsed_records if record["status"] == "candidate"), [record for record in parsed_records if record.get("parse", {}).get("status") != "pass"], "all pass", "Every selected row is consumed exactly by the reader sequence.")
    check("locale-shape", all(find_record(parsed_records, type_name, "English", row_id)["column_count"] == find_record(parsed_records, type_name, "Japanese", row_id)["column_count"] for type_name, ids in selected_ids.items() for row_id in ids), "English/Japanese column counts", "equal", "Locale rows retain aligned framing.")
    check("room-grid-shape", room_height == 10 and room_width == 10 and direction_height == 10 and direction_width == 10, {"objMap": [room_width, room_height], "objDir": [direction_width, direction_height]}, "10x10 for both", "RoomData(0) arrays decode to a rectangular first-slice grid.")
    check("door-code-candidate", len(door_cells) == 1, door_cells, "one candidate cell", "Exactly one raw map cell carries ObjChip door code 5.")
    check("derived-job-skill-links", job_ids == [4] and skill_ids == [1], {"job_ids": job_ids, "skill_ids": skill_ids}, {"job_ids": [4], "skill_ids": [1]}, "StaffData derived links are present rows, not promoted relations.")
    check("source-slices", all(item["status"] == "evidence_only" for item in scene["source_slices"] + behavior["source_slices"]), "all anchors", "evidence_only", "All source anchors resolve to current read-only C# files.")
    check("semantic-not-promoted", scene["semantic_status"] == "pending_review" and behavior["semantic_status"] == "pending_review", {"scene": scene["semantic_status"], "behavior": behavior["semantic_status"]}, "pending_review", "Candidate packages cannot become runtime catalogs.")

    validation = {
        "schema_version": VALIDATION_VERSION,
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "semantic_status": "pending_review",
        "generated_at_utc": timestamp,
        "input_hash": sha256_bytes(stable_json({"scene": scene["input_manifest"], "behavior": behavior["input_manifest"]}).encode("utf-8")),
        "failed_checks": [item["id"] for item in checks if item["status"] == "fail"],
        "checks": checks,
        "counts": {
            "parsed_records": len([record for record in parsed_records if record["status"] == "candidate"]),
            "scene_source_slices": len(scene["source_slices"]),
            "behavior_source_slices": len(behavior["source_slices"]),
            "transition_candidates": len(transition_candidates),
            "review_items": len(scene["review_items"]) + len(behavior["review_items"]),
        },
        "blocking_review_items": [
            item["id"]
            for item in scene["review_items"] + behavior["review_items"]
            if item["blocking"]
        ],
    }
    return scene, behavior, validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    scene, behavior, validation = build_candidates()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "scene_data_candidate.json": scene,
        "staff_behavior_candidate.json": behavior,
        "scene_behavior_validation.json": validation,
    }
    for name, payload in outputs.items():
        with (output_dir / name).open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    print(
        "scene_behavior_candidates_complete "
        f"status={validation['status']} "
        f"records={validation['counts']['parsed_records']} "
        f"transitions={validation['counts']['transition_candidates']} "
        f"review_items={validation['counts']['review_items']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
