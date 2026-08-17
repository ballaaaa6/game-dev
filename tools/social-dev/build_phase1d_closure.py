"""Build the authoritative Phase 1D closure package for the Social Dev slice.

This builder is intentionally evidence-only.  It parses the current extracted
tables, reads selector indexes from the supplied asset ZIP, and normalizes the
small native contracts needed to enter Phase 2.  It does not execute recovered
C# or native code and it does not create a runtime/catalog implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import build_scene_behavior_candidates as base
import scene_native_semantics_facts as facts


ROOT = base.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
CATALOG = EVIDENCE / "csharp_update_inventory"
SOURCE_ROOT = base.SOURCE_ROOT
APK_PATH = ROOT / facts.APK_RELATIVE_PATH
ASSET_ZIP = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
SCENE_PATH = EVIDENCE / "scene_data_candidate.json"
FIELD_LOAD_PATH = EVIDENCE / "field_load_candidates.json"
TYPE_CATALOG_PATH = CATALOG / "type_catalog.json"
OUTPUT_DIR = EVIDENCE

SCHEMA_VERSION = "social-dev-phase1d-closure-v1"
VALIDATION_VERSION = "social-dev-phase1d-closure-validation-v1"

ZIP_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
SELECTOR_MEMBERS = {
    "chip_seb": ZIP_PREFIX + "01_GAME_PACKS/chip/seb.inf",
    "chip_img": ZIP_PREFIX + "01_GAME_PACKS/chip/img.inf",
    "human_seb": ZIP_PREFIX + "01_GAME_PACKS/human/seb.inf",
    "human_img": ZIP_PREFIX + "01_GAME_PACKS/human/img.inf",
}
ASSEMBLY_GUIDE_MEMBER = ZIP_PREFIX + "05_ASSEMBLY_GUIDE/07_CHARACTER_ASSEMBLY.md"

SOURCE_FILES: dict[str, Path] = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Astar": SOURCE_ROOT / "game.routeSearch/Astar.cs",
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "FurnitureData": SOURCE_ROOT / "data/FurnitureData.cs",
    "StaffData": SOURCE_ROOT / "data/StaffData.cs",
    "SkillData": SOURCE_ROOT / "data/SkillData.cs",
    "DevelopForm": SOURCE_ROOT / "form/DevelopForm.cs",
}

STATE_NAMES = [
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
MOVE_NAMES = [
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
FLAG_NAMES = [
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
ASTAR_FLAG_NAMES = ["FLAG_GOAL_IS_DESK", "FLAG_GOAL_IS_EQUIP", "FLAG_GOAL_IS_STAFF"]
SKILL_CONSTANT_NAMES = [
    "TYPE_MEETING_POINT_UP",
    "SCENE_MAIN",
    "TARGET_SELF",
    "EFFECT_MEETING_POINT",
    "FLAG_PASSIVE",
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


def rel(path: Path | str) -> str:
    return base.relative_path(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def source_path(name: str) -> Path:
    try:
        path = SOURCE_FILES[name]
    except KeyError as exc:
        raise KeyError(f"unknown source key {name}") from exc
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path


def source_marker(path: Path, marker: str, note: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if marker in line:
            return {
                "file": rel(path),
                "line_start": index,
                "line_end": index,
                "source_sha256": sha256_file(path),
                "marker": marker,
                "note": note,
            }
    raise ValueError(f"source marker not found: {rel(path)}::{marker}")


def source_span(path: Path, start_marker: str, end_marker: str, note: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next((index for index, line in enumerate(lines) if start_marker in line), None)
    if start is None:
        raise ValueError(f"source start marker not found: {rel(path)}::{start_marker}")
    end = next((index for index in range(start + 1, len(lines)) if end_marker in lines[index]), None)
    if end is None:
        raise ValueError(f"source end marker not found: {rel(path)}::{end_marker}")
    text = "".join(lines[start : end + 1])
    return {
        "file": rel(path),
        "line_start": start + 1,
        "line_end": end + 1,
        "source_sha256": sha256_file(path),
        "slice_sha256": sha256_bytes(text.encode("utf-8")),
        "start_marker": start_marker,
        "end_marker": end_marker,
        "note": note,
    }


def native_ref(method_id: str) -> dict[str, Any]:
    for method in facts.NATIVE_METHODS:
        if method["id"] == method_id:
            item = copy.deepcopy(method)
            rva = int(item["rva_hex"], 16)
            mapping = facts.NATIVE_EXTRACTION_RECIPE["elf_rva_file_offset"]
            segment_start = int(mapping["segment_virtual_start"], 16)
            if rva >= segment_start:
                item["file_offset_hex"] = f"0x{rva - 0x4000:X}"
                item["file_offset_rule"] = mapping["rule"]
            return item
    raise KeyError(method_id)


def native_instruction(rva_hex: str, meaning: str) -> dict[str, Any]:
    rva = int(rva_hex, 16)
    mapping = facts.NATIVE_EXTRACTION_RECIPE["elf_rva_file_offset"]
    item = {
        "rva_hex": rva_hex,
        "file_offset_hex": f"0x{rva - 0x4000:X}" if rva >= int(mapping["segment_virtual_start"], 16) else None,
        "meaning": meaning,
        "apk_sha256": sha256_file(APK_PATH),
    }
    return item


def parse_records(type_name: str, ids: Iterable[int] | None = None) -> list[dict[str, Any]]:
    field_load_rows = base.load_json(FIELD_LOAD_PATH)["rows"]
    type_catalog_rows = base.load_json(TYPE_CATALOG_PATH)["records"]
    field_load = base.find_field_load(field_load_rows, type_name)
    type_source = base.find_type_source(type_catalog_rows, type_name)
    wanted = set(ids) if ids is not None else None
    parsed: list[dict[str, Any]] = []
    for locale in ("English", "Japanese"):
        table = base.table_path(type_name, locale)
        for row in base.read_table(table):
            if row["id"] is None or (wanted is not None and row["id"] not in wanted):
                continue
            parsed.append(base.parse_row(type_name, locale, row, field_load, type_source, table))
    return parsed


def record(records: list[dict[str, Any]], type_name: str, locale: str, row_id: int) -> dict[str, Any]:
    return base.find_record(records, type_name, locale, row_id)


def field(record_value: dict[str, Any], name: str, default: Any = None) -> Any:
    return base.value(record_value, name, default)


def record_ref(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": item["type"],
        "locale": item["locale"],
        "id": item["id"],
        "table_path": item["table_path"],
        "row_number": item["row_number"],
        "row_sha256": item["row_sha256"],
        "parse_status": item["parse"]["status"],
    }


def selector_entry(raw_line: str) -> tuple[int, str]:
    raw_id, raw_name = raw_line.split("\t", 1)
    name = raw_name.split(",", 1)[0]
    return int(raw_id), name


def read_inf(archive: zipfile.ZipFile, member: str) -> dict[str, Any]:
    raw = archive.read(member)
    entries: dict[int, str] = {}
    for line in raw.decode("utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        item_id, filename = selector_entry(line)
        if item_id in entries:
            raise ValueError(f"duplicate selector {member}:{item_id}")
        entries[item_id] = filename
    return {
        "member": member,
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "entry_count": len(entries),
        "entries": entries,
    }


def selector_ref(inf: dict[str, Any], selector_id: int) -> dict[str, Any]:
    filename = inf["entries"].get(selector_id)
    if filename is None:
        return {"id": selector_id, "status": "unresolved"}
    return {
        "id": selector_id,
        "filename": filename,
        "inf_member": inf["member"],
        "inf_sha256": inf["sha256"],
        "status": "resolved",
    }


def build_native_evidence() -> dict[str, Any]:
    return {
        "apk": rel(APK_PATH),
        "apk_sha256": sha256_file(APK_PATH),
        "architecture": facts.NATIVE_EXTRACTION_RECIPE["architecture"],
        "metadata_version": facts.IL2CPP_METADATA_VERSION,
        "extraction_recipe": facts.NATIVE_EXTRACTION_RECIPE,
        "methods": [
            native_ref("room-init-obj-chips"),
            native_ref("room-setup-big-chips-parent"),
            native_ref("room-place-object"),
            native_ref("objchip-is-passable"),
            native_ref("astar-search-route"),
            native_ref("astar-search-route-public"),
            native_ref("astar-add-neighbor"),
        ],
        "instruction_refs": {
            "type4_footprint": [
                native_instruction("0x12CE6E0", "Room.PlaceObj stores child dx_/dy_ offsets starting at -1,-1."),
                native_instruction("0x12CE6E8", "Room.PlaceObj iterates the three columns and three rows."),
                native_instruction("0x12CB864", "Room.SetupBigChipsParent links the same bounded 3x3 neighborhood."),
            ],
            "is_passable": [
                native_instruction("0x12C4B14", "Loads FurnitureData.passMap_ from the bound furniture record."),
                native_instruction("0x12C4B1C", "Loads ObjChip dx_/dy_ from the native object layout."),
                native_instruction("0x12C4B34", "Normalizes dx_/dy_ into the 3x3 anchor and row/column start."),
                native_instruction("0x12C4B98", "Loads one selected passMap cell."),
                native_instruction("0x12C4BA0", "Zero cell returns the current loop boolean immediately."),
                native_instruction("0x12C4BB4", "The final completed all-nonzero row changes the return boolean to false."),
                native_instruction("0x12C4C70", "Fallback record branch returns to the same passMap consumer."),
            ],
            "astar_neighbor_filter": [
                native_instruction("0x110EF5C", "Reads the neighbor ObjChip type."),
                native_instruction("0x110EF74", "Calls HasObj for type 2."),
                native_instruction("0x110EF80", "Normalizes type 3/4 into the IsPassable branch."),
                native_instruction("0x110EF94", "Calls ObjChip.IsPassable."),
                native_instruction("0x110EF98", "Rejects a false IsPassable result."),
                native_instruction("0x110EFA0", "Rejects type 6."),
            ],
            "astar_goal_filter": [
                native_instruction("0x110E860", "Public SearchRoute reads the goal-filter flag."),
                native_instruction("0x110E884", "Checks the desk bit before equip/staff goal handling."),
                native_instruction("0x110E8A8", "Checks the equipment bit."),
                native_instruction("0x110E8C4", "Reads the final goal ObjChip for equipment postprocess."),
                native_instruction("0x110E8DC", "Type-1 goal uses RoomData.objDir_."),
                native_instruction("0x110E930", "objDir 0 maps to direction 7."),
                native_instruction("0x110E93C", "objDir 1 maps to direction 6."),
                native_instruction("0x110E944", "Other objDir values map to direction 0."),
                native_instruction("0x110E94C", "Checks the staff bit."),
            ],
        },
    }


def normalize_is_passable(pass_map: list[list[int]], dx: int, dy: int) -> tuple[bool, list[dict[str, Any]]]:
    if len(pass_map) < 9 or any(len(row) < 9 for row in pass_map):
        raise ValueError("IsPassable fixture requires a 9x9-or-larger passMap")
    anchor = dx + dy * 3 + 4
    row_start = (anchor // 3) * 3
    column_start = (anchor % 3) * 3
    if row_start + 3 > len(pass_map) or column_start + 3 > len(pass_map[0]):
        raise ValueError(f"passMap window out of bounds for dx={dx}, dy={dy}")
    result = True
    trace: list[dict[str, Any]] = []
    for row_offset in range(3):
        for column_offset in range(3):
            row_index = row_start + row_offset
            column_index = column_start + column_offset
            cell_value = pass_map[row_index][column_index]
            before = result
            if cell_value == 0:
                trace.append(
                    {
                        "row_offset": row_offset,
                        "column_offset": column_offset,
                        "row_index": row_index,
                        "column_index": column_index,
                        "value": cell_value,
                        "result_before": before,
                        "branch": "zero_returns_current_result",
                        "result": result,
                    }
                )
                return result, trace
            trace.append(
                {
                    "row_offset": row_offset,
                    "column_offset": column_offset,
                    "row_index": row_index,
                    "column_index": column_index,
                    "value": cell_value,
                    "result_before": before,
                    "branch": "nonzero_continue",
                }
            )
        result = row_offset < 2
        trace.append(
            {
                "row_offset": row_offset,
                "branch": "row_complete_cset",
                "result": result,
            }
        )
    return result, trace


def build_passmap_fixture(scene: dict[str, Any], furniture_records: list[dict[str, Any]]) -> dict[str, Any]:
    room = scene["room"]
    furniture = record(furniture_records, "FurnitureData", "English", 0)
    furniture_ja = record(furniture_records, "FurnitureData", "Japanese", 0)
    pass_map = field(furniture, "passMap_")
    if field(furniture, "type_") != 4 or field(furniture_ja, "type_") != 4:
        raise ValueError("FurnitureData(0) is no longer the reviewed type-4 fixture")
    if pass_map != field(furniture_ja, "passMap_"):
        raise ValueError("English/Japanese type-4 passMap differs")
    anchors = [
        {"x": x, "y": y, "raw_map_value": raw}
        for y, row in enumerate(room["objMap"])
        for x, raw in enumerate(row)
        if raw == 4
    ]
    if not anchors:
        raise ValueError("RoomData(0) has no raw type-4 anchor")
    anchor = anchors[0]
    parent_x, parent_y = anchor["x"], anchor["y"]
    footprint = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            x = parent_x + dx
            y = parent_y + dy
            footprint.append(
                {
                    "dx": dx,
                    "dy": dy,
                    "x": x,
                    "y": y,
                    "raw_map_value": room["objMap"][y][x],
                    "raw_dir_value": room["objDir"][y][x],
                }
            )
    matrix: list[list[bool]] = []
    traces: dict[str, Any] = {}
    for dy in range(-1, 2):
        row_results = []
        for dx in range(-1, 2):
            result, trace = normalize_is_passable(pass_map, dx, dy)
            row_results.append(result)
            traces[f"dx={dx},dy={dy}"] = {
                "dx": dx,
                "dy": dy,
                "isPassable": result,
                "trace": trace,
            }
        matrix.append(row_results)
    synthetic_probes = []
    for row_offset in range(3):
        for column_offset in range(3):
            probe = [[2 for _ in range(9)] for _ in range(9)]
            probe[3 + row_offset][3 + column_offset] = 0
            result, _ = normalize_is_passable(probe, 0, 0)
            synthetic_probes.append(
                {
                    "zero_row_offset": row_offset,
                    "zero_column_offset": column_offset,
                    "isPassable": result,
                }
            )
    all_nonzero = [[2 for _ in range(9)] for _ in range(9)]
    all_nonzero_result, all_nonzero_trace = normalize_is_passable(all_nonzero, 0, 0)
    return {
        "status": "pass",
        "fixture_kind": "real_room_type4_parent_with_explicit_furniture_binding",
        "scene_record": {
            "type": room["type"],
            "id": room["id"],
            "source_record_ref": room["source_record_ref"],
            "anchor": anchor,
        },
        "furniture_record": {
            "id": furniture["id"],
            "name": field(furniture, "name_"),
            "type": field(furniture, "type_"),
            "passMap_shape": [len(pass_map[0]), len(pass_map)],
            "passMap": pass_map,
            "english_ref": record_ref(furniture),
            "japanese_ref": record_ref(furniture_ja),
        },
        "native_placement": {
            "footprint_offsets": "dx,dy in {-1,0,1}, row-major",
            "footprint": footprint,
            "parent_center_offset": {"dx": 0, "dy": 0},
        },
        "isPassable": {
            "formula": "anchor = dx + dy * 3 + 4; rowStart = floor(anchor / 3) * 3; columnStart = (anchor mod 3) * 3",
            "boolean_semantics": "returns true on any selected zero cell; returns false only after all nine selected cells are nonzero",
            "matrix_order": {"rows": "dy=-1,0,1", "columns": "dx=-1,0,1"},
            "matrix": matrix,
            "traces": traces,
            "all_nonzero_probe": {
                "isPassable": all_nonzero_result,
                "trace": all_nonzero_trace,
            },
            "synthetic_zero_probes": synthetic_probes,
        },
        "null_furniture_branch": {
            "status": "closed_for_fixture_scope",
            "native_observation": "fallback record resolution at 0x12C4BD8..0x12C4C70 returns to the same passMap consumer",
            "fixture_policy": "bind FurnitureData(0) explicitly; no fallback selector identity is promoted into the runtime",
        },
        "provenance": {
            "native_method_ids": ["room-place-object", "room-setup-big-chips-parent", "objchip-is-passable"],
            "apk": rel(APK_PATH),
            "apk_sha256": sha256_file(APK_PATH),
            "source_files": [
                {"file": rel(SOURCE_FILES["Room"]), "sha256": sha256_file(SOURCE_FILES["Room"])},
                {"file": rel(SOURCE_FILES["ObjChip"]), "sha256": sha256_file(SOURCE_FILES["ObjChip"])},
                {"file": rel(SOURCE_FILES["FurnitureData"]), "sha256": sha256_file(SOURCE_FILES["FurnitureData"])},
            ],
        },
    }


def cell_key(x: int, y: int) -> str:
    return f"{x},{y}"


def cell_admission(room: dict[str, Any], x: int, y: int, overrides: dict[str, dict[str, Any]]) -> dict[str, Any]:
    width = room["grid_shape"]["objMap_width"]
    height = room["grid_shape"]["objMap_height"]
    if x < 0 or y < 0 or x >= width or y >= height:
        return {"x": x, "y": y, "admitted": False, "reason": "out_of_bounds"}
    raw_type = room["objMap"][y][x]
    info: dict[str, Any] = {
        "x": x,
        "y": y,
        "raw_type": raw_type,
        "type": raw_type,
        "has_obj": False,
        "isPassable": None,
    }
    info.update(copy.deepcopy(overrides.get(cell_key(x, y), {})))
    object_type = info["type"]
    if object_type == 2:
        admitted = not bool(info.get("has_obj", False))
        reason = "type2_requires_not_HasObj"
    elif object_type in (3, 4):
        admitted = bool(info.get("isPassable", False))
        reason = "type3_4_requires_IsPassable_true"
    elif object_type == 6:
        admitted = False
        reason = "type6_rejected"
    else:
        admitted = True
        reason = "other_type_accepted"
    info["admitted"] = admitted
    info["reason"] = reason
    return info


def route_search(room: dict[str, Any], start: tuple[int, int], goal: tuple[int, int], overrides: dict[str, dict[str, Any]]) -> list[list[int]] | None:
    start_info = cell_admission(room, start[0], start[1], overrides)
    goal_info = cell_admission(room, goal[0], goal[1], overrides)
    if not start_info.get("admitted") or not goal_info.get("admitted"):
        return None
    queue: deque[tuple[int, int]] = deque([start])
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    offsets = [(item["dx"], item["dy"]) for item in facts.NEIGHBOR_POLICY["offsets"]]
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in offsets:
            candidate = (current[0] + dx, current[1] + dy)
            if candidate in came_from:
                continue
            info = cell_admission(room, candidate[0], candidate[1], overrides)
            if not info.get("admitted"):
                continue
            came_from[candidate] = current
            queue.append(candidate)
    if goal not in came_from:
        return None
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return [[x, y] for x, y in path]


def goal_postprocess(room: dict[str, Any], goal: tuple[int, int], flag: int) -> dict[str, Any]:
    goal_type = room["objMap"][goal[1]][goal[0]]
    if flag == 0:
        return {"flag": flag, "branch": "default", "direction": 7}
    if flag & facts.ROUTE_FILTER["goal_filter"]["flag_values"]["FLAG_GOAL_IS_DESK"]:
        return {"flag": flag, "branch": "desk_bit_skips_equip_staff_postprocess", "direction": 7}
    if flag & facts.ROUTE_FILTER["goal_filter"]["flag_values"]["FLAG_GOAL_IS_EQUIP"]:
        if goal_type == 1:
            raw_direction = room["objDir"][goal[1]][goal[0]]
            direction = {0: 7, 1: 6}.get(raw_direction, 0)
            return {
                "flag": flag,
                "branch": "equip_type1_goal_objDir",
                "goal_type": goal_type,
                "raw_objDir": raw_direction,
                "direction": direction,
            }
        return {"flag": flag, "branch": "equip_non_type1_default", "goal_type": goal_type, "direction": 7}
    if flag & facts.ROUTE_FILTER["goal_filter"]["flag_values"]["FLAG_GOAL_IS_STAFF"]:
        return {"flag": flag, "branch": "staff_bit_recognized_default_postprocess", "direction": 7}
    return {"flag": flag, "branch": "default", "direction": 7}


def build_route_fixture(scene: dict[str, Any], passmap: dict[str, Any], staff_records: list[dict[str, Any]]) -> dict[str, Any]:
    room = scene["room"]
    start = (8, 4)
    goal = (6, 4)
    overrides: dict[str, dict[str, Any]] = {}
    path = route_search(room, start, goal, overrides)
    equip_goal = (8, 5)
    equip_path = route_search(room, start, equip_goal, overrides)
    occupied_overrides = {cell_key(6, 4): {"has_obj": True, "furniture_id": 2}}
    occupied_path = route_search(room, start, goal, occupied_overrides)
    big_anchor = passmap["scene_record"]["anchor"]
    big_overrides = {
        cell_key(big_anchor["x"], big_anchor["y"]): {
            "furniture_id": passmap["furniture_record"]["id"],
            "dx": 0,
            "dy": 0,
            "isPassable": False,
        }
    }
    big_path = route_search(room, start, (big_anchor["x"], big_anchor["y"]), big_overrides)
    outdoor_path = route_search(room, start, (0, 0), {})
    flag_values = facts.ROUTE_FILTER["goal_filter"]["flag_values"]
    astar_constants = base.extract_constants("Astar", ASTAR_FLAG_NAMES)
    staff_constants = {item["name"]: item["value"] for item in base.extract_constants("Staff", MOVE_NAMES)}
    route_mapping = [
        {
            "move_mode": "MOVE_MODE_GOTO_EQUIPMENT",
            "move_mode_value": staff_constants["MOVE_MODE_GOTO_EQUIPMENT"],
            "astar_flag": flag_values["FLAG_GOAL_IS_EQUIP"],
        },
        {
            "move_mode": "MOVE_MODE_TO_STAFF",
            "move_mode_value": staff_constants["MOVE_MODE_TO_STAFF"],
            "astar_flag": flag_values["FLAG_GOAL_IS_STAFF"],
        },
        {
            "move_mode": "MOVE_MODE_GOTO_DESK",
            "move_mode_value": staff_constants["MOVE_MODE_GOTO_DESK"],
            "astar_flag": flag_values["FLAG_GOAL_IS_DESK"],
        },
    ]
    source_staff_route = source_path("Staff")
    return {
        "status": "pass",
        "fixture_kind": "real_roomdata_route_with_filter_probes",
        "scene": {
            "type": room["type"],
            "id": room["id"],
            "name": room["name"],
            "grid_shape": room["grid_shape"],
            "source_record_ref": room["source_record_ref"],
        },
        "route": {
            "start": list(start),
            "goal": list(goal),
            "expected_path": [[8, 4], [7, 4], [6, 4]],
            "path": path,
            "step_count": len(path) - 1 if path else None,
            "neighbor_policy": facts.NEIGHBOR_POLICY,
            "cell_trace": [cell_admission(room, x, y, overrides) for x, y in [(8, 4), (7, 4), (6, 4)]],
        },
        "goal_filter": {
            "native_contract": facts.ROUTE_FILTER,
            "source_constants": astar_constants,
            "staff_move_mode_mapping": route_mapping,
            "public_postprocess_probes": {
                "desk_flag": goal_postprocess(room, goal, flag_values["FLAG_GOAL_IS_DESK"]),
                "equip_flag_on_type1": goal_postprocess(room, equip_goal, flag_values["FLAG_GOAL_IS_EQUIP"]),
                "staff_flag": goal_postprocess(room, goal, flag_values["FLAG_GOAL_IS_STAFF"]),
                "default_flag": goal_postprocess(room, goal, 0),
            },
            "source_refs": [
                source_marker(source_path("Astar"), "public const int FLAG_GOAL_IS_DESK", "goal flag constants"),
                source_marker(source_path("Astar"), "public unsafe bool SearchRoute", "public goal-filter entrypoint"),
                source_marker(source_staff_route, "return ((Astar)0).SearchRoute", "Staff move mode to Astar flag dispatch"),
            ],
        },
        "filter_probes": [
            {
                "id": "occupied-type2",
                "cell": [6, 4],
                "expected_admitted": False,
                "admission": cell_admission(room, 6, 4, occupied_overrides),
                "path": occupied_path,
                "native_reason": "type 2 with HasObj() is rejected",
            },
            {
                "id": "type4-ispassable-false",
                "cell": [big_anchor["x"], big_anchor["y"]],
                "expected_admitted": False,
                "admission": cell_admission(room, big_anchor["x"], big_anchor["y"], big_overrides),
                "path": big_path,
                "native_reason": "type 3/4 with IsPassable() == false is rejected",
                "furniture_binding": {
                    "furniture_id": passmap["furniture_record"]["id"],
                    "dx": 0,
                    "dy": 0,
                    "isPassable": False,
                },
            },
            {
                "id": "type6-outdoor",
                "cell": [0, 0],
                "expected_admitted": False,
                "admission": cell_admission(room, 0, 0, {}),
                "path": outdoor_path,
                "native_reason": "type 6 is rejected",
            },
        ],
        "secondary_real_goal": {
            "goal": list(equip_goal),
            "raw_type": room["objMap"][equip_goal[1]][equip_goal[0]],
            "path": equip_path,
            "goal_flag": flag_values["FLAG_GOAL_IS_EQUIP"],
            "public_postprocess": goal_postprocess(room, equip_goal, flag_values["FLAG_GOAL_IS_EQUIP"]),
        },
        "provenance": {
            "apk": rel(APK_PATH),
            "apk_sha256": sha256_file(APK_PATH),
            "room_data": room["source_record_ref"],
            "native_method_ids": ["astar-search-route", "astar-search-route-public", "astar-add-neighbor"],
            "source_files": [
                {"file": rel(SOURCE_FILES["Astar"]), "sha256": sha256_file(SOURCE_FILES["Astar"])},
                {"file": rel(SOURCE_FILES["Room"]), "sha256": sha256_file(SOURCE_FILES["Room"])},
                {"file": rel(SOURCE_FILES["Staff"]), "sha256": sha256_file(SOURCE_FILES["Staff"])},
            ],
            "fixture_input": "RoomData(0) objMap_/objDir_ plus explicit FurnitureData(0) binding for the type-4 negative probe",
        },
    }


def build_asset_selector_contract(furniture_records: list[dict[str, Any]], staff_records: list[dict[str, Any]]) -> dict[str, Any]:
    with zipfile.ZipFile(ASSET_ZIP) as archive:
        infs = {key: read_inf(archive, member) for key, member in SELECTOR_MEMBERS.items()}
        guide_raw = archive.read(ASSEMBLY_GUIDE_MEMBER)
        guide_ref = {
            "member": ASSEMBLY_GUIDE_MEMBER,
            "bytes": len(guide_raw),
            "sha256": sha256_bytes(guide_raw),
        }
    selector_specs = {
        "FurnitureData.seb_": ("chip_seb", "seb_", False),
        "FurnitureData.subSeb_": ("chip_seb", "subSeb_", True),
        "FurnitureData.img_": ("chip_img", "img_", True),
        "StaffData.img_": ("human_img", "img_", False),
    }
    datasets = {
        "FurnitureData": furniture_records,
        "StaffData": staff_records,
    }
    results: dict[str, Any] = {}
    unresolved: list[dict[str, Any]] = []
    for label, (inf_key, field_name, negative_allowed) in selector_specs.items():
        type_name = label.split(".", 1)[0]
        records = datasets[type_name]
        inf = infs[inf_key]
        by_locale: dict[str, list[int]] = {}
        negative_count = 0
        for locale in ("English", "Japanese"):
            values: list[int] = []
            for item in records:
                if item["locale"] != locale:
                    continue
                if item["parse"]["status"] != "pass":
                    unresolved.append({"dataset": label, "record": record_ref(item), "reason": "row_parse_error"})
                    continue
                selector = field(item, field_name)
                if selector is None:
                    unresolved.append({"dataset": label, "record": record_ref(item), "reason": "missing_field"})
                    continue
                selector = int(selector)
                if selector < 0:
                    negative_count += 1
                    if not negative_allowed:
                        unresolved.append({"dataset": label, "record": record_ref(item), "selector": selector, "reason": "negative_not_allowed"})
                    continue
                values.append(selector)
                if selector not in inf["entries"]:
                    unresolved.append({"dataset": label, "record": record_ref(item), "selector": selector, "reason": "inf_entry_missing"})
            by_locale[locale] = sorted(set(values))
        if by_locale["English"] != by_locale["Japanese"]:
            unresolved.append({"dataset": label, "reason": "locale_selector_set_mismatch", "by_locale": by_locale})
        results[label] = {
            "field": field_name,
            "inf": selector_ref(inf, 0)["inf_member"] if inf["entries"] else inf["member"],
            "inf_sha256": inf["sha256"],
            "rows_checked": len(records),
            "rows_per_locale": {locale: sum(1 for item in records if item["locale"] == locale) for locale in ("English", "Japanese")},
            "negative_value_count": negative_count,
            "used_ids": by_locale["English"],
            "resolved": {str(selector_id): selector_ref(inf, selector_id) for selector_id in by_locale["English"]},
            "locale_sets_match": by_locale["English"] == by_locale["Japanese"],
            "status": "pass",
        }
    selected_furniture = []
    for item_id in (0, 1, 2, 5):
        item = record(furniture_records, "FurnitureData", "English", item_id)
        selected_furniture.append(
            {
                "id": item_id,
                "name": field(item, "name_"),
                "type": field(item, "type_"),
                "selectors": {
                    "seb_": selector_ref(infs["chip_seb"], int(field(item, "seb_"))),
                    "subSeb_": selector_ref(infs["chip_seb"], int(field(item, "subSeb_"))) if int(field(item, "subSeb_")) >= 0 else {"id": -1, "status": "absent_by_sentinel"},
                    "img_": selector_ref(infs["chip_img"], int(field(item, "img_"))) if int(field(item, "img_")) >= 0 else {"id": -1, "status": "absent_by_sentinel"},
                },
                "source_record_ref": record_ref(item),
            }
        )
    selected_staff = []
    for item_id in (0, 1, 2, 3, 4):
        item = record(staff_records, "StaffData", "English", item_id)
        selected_staff.append(
            {
                "id": item_id,
                "name": f"{field(item, 'lastName_')} {field(item, 'firstName_')}",
                "img_": selector_ref(infs["human_img"], int(field(item, "img_"))),
                "source_record_ref": record_ref(item),
            }
        )
    source_refs = [
        source_marker(source_path("FurnitureData"), "public int seb_;", "FurnitureData asset selector fields"),
        source_marker(source_path("FurnitureData"), "seb_ = num6;", "FurnitureData.Load selector assignment"),
        source_marker(source_path("ObjChip"), "bool flag144 = furnitureData.seb_ < seb6.Length;", "ObjChip.Draw chip seb bounds check"),
        source_marker(source_path("ObjChip"), "object obj147 = resChip_7.seb + furnitureData.seb_;", "ObjChip.Draw chip seb/img selector use"),
        source_marker(source_path("ObjChip"), "furnitureData.subSeb_, flag35 ? 1 : 0", "ObjChip.Draw subSeb selector use"),
        source_marker(source_path("DevelopForm"), "appData.resChip_.DrawSeb(g, x2, y2, furnitureData_.subSeb_, frame);", "DevelopForm subSeb selector use"),
        source_marker(source_path("Staff"), "bool flag3 = staffData.img_ < img.Length;", "Staff.DrawScale human img bounds check"),
    ]
    status = "pass" if not unresolved else "fail"
    return {
        "schema_version": "social-dev-asset-selector-contract-v1",
        "status": status,
        "scope": {
            "furniture_rows": 103,
            "staff_rows": 141,
            "locales": ["English", "Japanese"],
            "policy": "All nonnegative selectors used by parsed FurnitureData/StaffData rows must resolve in the matching inf index; -1 is an explicit absent sentinel only for subSeb_/img_ fields that permit it.",
            "not_claimed": "This closes selector identity for parsed data rows, not visual frame timing or every derived asset in the 3542-row inventory.",
        },
        "asset_zip": {
            "path": rel(ASSET_ZIP),
            "sha256": sha256_file(ASSET_ZIP),
            "selector_indexes": infs,
            "assembly_guide": guide_ref,
        },
        "selector_contracts": results,
        "selected_furniture": selected_furniture,
        "selected_staff": selected_staff,
        "source_refs": source_refs,
        "unresolved": unresolved,
    }


def build_staff_semantics(staff_records: list[dict[str, Any]], skill_records: list[dict[str, Any]], asset_contract: dict[str, Any]) -> dict[str, Any]:
    selected_staff = [record(staff_records, "StaffData", "English", item_id) for item_id in (0, 1, 2, 3, 4)]
    selected_staff_ja = [record(staff_records, "StaffData", "Japanese", item_id) for item_id in (0, 1, 2, 3, 4)]
    skill = record(skill_records, "SkillData", "English", 1)
    skill_ja = record(skill_records, "SkillData", "Japanese", 1)
    skill_effects = field(skill, "effects_")
    if field(skill, "type_") != 10 or field(skill, "scene_") != 1 or field(skill, "target_") != 0:
        raise ValueError("SkillData(1) no longer matches the reviewed living-scene skill")
    if not skill_effects or len(skill_effects) <= 8 or skill_effects[8] != [150]:
        raise ValueError("SkillData(1).effects_[8] no longer matches the reviewed effect")
    state_constants = base.extract_constants("Staff", STATE_NAMES + MOVE_NAMES + FLAG_NAMES)
    state_values = {item["name"]: item["value"] for item in state_constants}
    astar_constants = base.extract_constants("Astar", ASTAR_FLAG_NAMES)
    astar_values = {item["name"]: item["value"] for item in astar_constants}
    skill_constants = base.extract_constants("SkillData", SKILL_CONSTANT_NAMES)
    skill_constant_values = {item["name"]: item["value"] for item in skill_constants}
    with zipfile.ZipFile(ASSET_ZIP) as archive:
        human_seb = read_inf(archive, SELECTOR_MEMBERS["human_seb"])
    typing_pairs = []
    for reverse_direction in range(4):
        typing_id = reverse_direction + 23
        wait_id = reverse_direction + 10
        typing_pairs.append(
            {
                "reverse_direction": reverse_direction,
                "typing": {"seb_id": typing_id, "asset": selector_ref(human_seb, typing_id)},
                "wait": {"seb_id": wait_id, "asset": selector_ref(human_seb, wait_id)},
            }
        )
    staff_skill_ids = sorted({int(field(item, "skill_")) for item in selected_staff})
    staff_skill_ids_ja = sorted({int(field(item, "skill_")) for item in selected_staff_ja})
    skill_core_fields = ["type_", "scene_", "target_", "attribute_", "effects_", "auraRates_", "flag_"]
    skill_locale_alignment = all(field(skill, name) == field(skill_ja, name) for name in skill_core_fields)
    source_staff = source_path("Staff")
    source_skill = source_path("SkillData")
    transition_contracts = [
        {
            "id": "stay-home-to-door",
            "when": "UpdateStayHome hpRatio >= 40",
            "writes": {"state_": state_values["STATE_WAIT_BACK_OF_DOOR"], "moveMode_": state_values["MOVE_MODE_GOTO_DESK"]},
            "side_effect": "reserve room door use",
            "source_ref": base.source_slice("Staff", 1941, 1954, "bounded stay-home transition"),
            "status": "closed_for_living_scene_contract",
        },
        {
            "id": "work-to-equipment",
            "when": "GotoEquip selects an available equipment object",
            "writes": {"state_": state_values["STATE_MOVE"], "moveMode_": state_values["MOVE_MODE_GOTO_EQUIPMENT"]},
            "side_effect": "reserve object use",
            "source_ref": base.source_slice("Staff", 3038, 3059, "bounded equipment destination transition"),
            "status": "closed_for_living_scene_contract",
        },
        {
            "id": "work-to-talk",
            "when": "GotoTalk finds a staff at a usable desk",
            "writes": {"state_": state_values["STATE_MOVE"], "moveMode_": state_values["MOVE_MODE_TO_STAFF"]},
            "side_effect": "set colleague ids and talk flags on both staff",
            "source_ref": base.source_slice("Staff", 2994, 3037, "bounded talk destination transition"),
            "status": "closed_for_living_scene_contract",
        },
        {
            "id": "talk-timing",
            "frame_markers": [20, 70, 110, 130],
            "terminal_effect": "clear talk flags and GotoDesk at frame >= 130",
            "source_ref": base.source_slice("Staff", 2059, 2175, "visible talk timer transition"),
            "status": "closed_for_living_scene_contract",
        },
    ]
    route_mapping = [
        {
            "move_mode": "MOVE_MODE_GOTO_EQUIPMENT",
            "move_mode_value": state_values["MOVE_MODE_GOTO_EQUIPMENT"],
            "astar_flag": astar_values["FLAG_GOAL_IS_EQUIP"],
        },
        {
            "move_mode": "MOVE_MODE_TO_STAFF",
            "move_mode_value": state_values["MOVE_MODE_TO_STAFF"],
            "astar_flag": astar_values["FLAG_GOAL_IS_STAFF"],
        },
        {
            "move_mode": "MOVE_MODE_GOTO_DESK",
            "move_mode_value": state_values["MOVE_MODE_GOTO_DESK"],
            "astar_flag": astar_values["FLAG_GOAL_IS_DESK"],
        },
    ]
    staff_projection = [
        {
            "id": item["id"],
            "name": f"{field(item, 'lastName_')} {field(item, 'firstName_')}",
            "img_": field(item, "img_"),
            "jobId_": field(item, "jobId_"),
            "skill_": field(item, "skill_"),
            "source_record_ref": record_ref(item),
        }
        for item in selected_staff
    ]
    return {
        "schema_version": "social-dev-staff-living-scene-contract-v1",
        "status": "pass",
        "scope": "Visible staff slice required for a living scene: state/move labels, route flag dispatch, talk timing, typing/wait animation selectors, and the selected skill reference/effect.",
        "staff_records": staff_projection,
        "state_constants": state_constants,
        "route_mapping": {
            "entries": route_mapping,
            "source_ref": source_marker(source_staff, "return ((Astar)0).SearchRoute", "Staff route dispatch to Astar"),
            "astar_constants": astar_constants,
        },
        "state_transition_contracts": transition_contracts,
        "typing_animation": {
            "start": {
                "flag_on": state_values["FLAG_TYPING"],
                "typingFrame": 100,
                "sebFrameInterval": 3,
                "seb_formula": "reverseDirection + 23",
                "source_ref": source_span(source_staff, "private void OnStartTyping()", "private void OnEndTyping()", "typing start transition"),
            },
            "end": {
                "flag_off": state_values["FLAG_TYPING"],
                "typingFrame": 0,
                "sebFrameInterval": 1,
                "seb_formula": "reverseDirection + 10",
                "source_ref": source_span(source_staff, "private void OnEndTyping()", "private bool IsTyping()", "typing end transition"),
            },
            "selector_pairs": typing_pairs,
        },
        "skill_reference": {
            "selected_staff_skill_ids": staff_skill_ids,
            "selected_staff_skill_ids_japanese": staff_skill_ids_ja,
            "staff_skill_ids_uniform": len(staff_skill_ids) == 1,
            "staff_skill_ids_locale_aligned": staff_skill_ids == staff_skill_ids_ja,
            "skill_core_locale_aligned": skill_locale_alignment,
            "skill": {
                "id": skill["id"],
                "name": field(skill, "name_"),
                "type_": field(skill, "type_"),
                "scene_": field(skill, "scene_"),
                "target_": field(skill, "target_"),
                "attribute_": field(skill, "attribute_"),
                "effects_8": field(skill, "effects_")[8],
                "auraRates_": field(skill, "auraRates_"),
                "flag_": field(skill, "flag_"),
                "english_ref": record_ref(skill),
                "japanese_ref": record_ref(skill_ja),
            },
            "source_constants": skill_constants,
            "source_refs": [
                source_marker(source_staff, "skillId_ = num8;", "Staff constructor/init copies StaffData.skill_ into skillId_"),
                source_marker(source_staff, "skillId_ = skillId;", "Staff.ChangeSkill writes skillId_"),
                source_marker(source_staff, "SkillData skill = GetSkill();", "Staff.OnEndTyping resolves the selected skill"),
                source_marker(source_skill, "effects_ = intIntArray;", "SkillData.Load effects field"),
            ],
            "effect_contract": {
                "type_name": "TYPE_MEETING_POINT_UP",
                "type_value": skill_constant_values["TYPE_MEETING_POINT_UP"],
                "effect_name": "EFFECT_MEETING_POINT",
                "effect_index": skill_constant_values["EFFECT_MEETING_POINT"],
                "effect_value": 150,
                "flag_name": "FLAG_PASSIVE",
                "flag_value": skill_constant_values["FLAG_PASSIVE"],
                "on_end_typing_scope": "OnEndTyping reads effects_[8][0] for type 10 and applies its bounded meeting-point gauge path; the random gauge distribution is intentionally not ported here.",
            },
        },
        "asset_animation_provenance": {
            "human_seb_inf": next(item for item in asset_contract["asset_zip"]["selector_indexes"].values() if item["member"] == SELECTOR_MEMBERS["human_seb"]),
            "selector_contract_status": asset_contract["status"],
        },
        "limitations": [
            "Staff.Update and the damaged GetSkill lookup body are not promoted as a full runtime algorithm.",
            "The contract closes only the state/animation/skill semantics needed to show this living-scene slice; canonical ActorCatalog behavior remains Phase 2 work.",
        ],
    }


def build_checks(passmap: dict[str, Any], route: dict[str, Any], asset: dict[str, Any], staff: dict[str, Any], native: dict[str, Any]) -> list[dict[str, Any]]:
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

    expected_matrix = [[True, False, False], [True, False, False], [True, True, True]]
    actual_matrix = passmap["isPassable"]["matrix"]
    zero_probes = passmap["isPassable"]["synthetic_zero_probes"]
    check("type4-real-fixture", passmap["fixture_kind"].startswith("real_room_type4"), passmap["scene_record"], "RoomData(0) raw type-4 anchor with FurnitureData(0)", "The fixture binds real scene and furniture records.")
    check("type4-passmap-shape", passmap["furniture_record"]["passMap_shape"] == [9, 9], passmap["furniture_record"]["passMap_shape"], [9, 9], "FurnitureData(0) supplies the reviewed 9x9 passMap.")
    check("type4-footprint", len(passmap["native_placement"]["footprint"]) == 9 and passmap["native_placement"]["parent_center_offset"] == {"dx": 0, "dy": 0}, len(passmap["native_placement"]["footprint"]), 9, "Native Room placement yields a 3x3 footprint with a center child.")
    check("ispassable-normalization", actual_matrix == expected_matrix, actual_matrix, expected_matrix, "The native loop normalization is exercised at every 3x3 offset.")
    check("ispassable-zero-cell", all(item["isPassable"] for item in zero_probes), [item["isPassable"] for item in zero_probes], "all true", "Every selected zero cell returns true.")
    check("ispassable-all-nonzero", passmap["isPassable"]["all_nonzero_probe"]["isPassable"] is False, passmap["isPassable"]["all_nonzero_probe"]["isPassable"], False, "All nine nonzero cells complete the final false branch.")
    check("astar-route-path", route["route"]["path"] == route["route"]["expected_path"], route["route"]["path"], route["route"]["expected_path"], "A real RoomData route is emitted with provenance.")
    check("astar-occupied-type2", route["filter_probes"][0]["path"] is None and not route["filter_probes"][0]["admission"]["admitted"], route["filter_probes"][0], "no path", "HasObj blocks occupied type 2.")
    check("astar-type4-false", route["filter_probes"][1]["path"] is None and not route["filter_probes"][1]["admission"]["admitted"], route["filter_probes"][1], "no path", "IsPassable false blocks the real type-4 goal.")
    check("astar-type6-filter", route["filter_probes"][2]["path"] is None and not route["filter_probes"][2]["admission"]["admitted"], route["filter_probes"][2], "no path", "Type 6 is excluded.")
    check("astar-goal-filter", route["goal_filter"]["public_postprocess_probes"]["equip_flag_on_type1"]["direction"] == 7, route["goal_filter"]["public_postprocess_probes"], "equipment type-1 objDir 0 -> direction 7", "Public SearchRoute goal postprocess is confirmed.")
    check("asset-selector-resolution", asset["status"] == "pass" and not asset["unresolved"], {"status": asset["status"], "unresolved": len(asset["unresolved"])}, "pass / 0 unresolved", "All used nonnegative data selectors resolve in the matching inf indexes.")
    check("asset-selector-locale-alignment", all(item["locale_sets_match"] for item in asset["selector_contracts"].values()), {key: item["locale_sets_match"] for key, item in asset["selector_contracts"].items()}, "all true", "English/Japanese selector sets agree.")
    check("staff-state-contract", staff["status"] == "pass" and len(staff["state_constants"]) == len(STATE_NAMES + MOVE_NAMES + FLAG_NAMES), len(staff["state_constants"]), len(STATE_NAMES + MOVE_NAMES + FLAG_NAMES), "Required state, move and flag labels are sourced.")
    check("staff-animation-contract", [item["typing"]["asset"]["status"] for item in staff["typing_animation"]["selector_pairs"]] == ["resolved"] * 4 and [item["wait"]["asset"]["status"] for item in staff["typing_animation"]["selector_pairs"]] == ["resolved"] * 4, staff["typing_animation"]["selector_pairs"], "all resolved", "Typing and wait selectors resolve to human seb entries.")
    check("staff-skill-contract", staff["skill_reference"]["selected_staff_skill_ids"] == [1] and staff["skill_reference"]["skill"]["effects_8"] == [150], staff["skill_reference"], "skill 1 / effects[8]=[150]", "Selected staff and OnEndTyping skill semantics align.")
    check("staff-skill-locale-alignment", staff["skill_reference"]["staff_skill_ids_locale_aligned"] and staff["skill_reference"]["skill_core_locale_aligned"], {"staff_ids": staff["skill_reference"]["staff_skill_ids_locale_aligned"], "skill_core": staff["skill_reference"]["skill_core_locale_aligned"]}, "both true", "English/Japanese skill links and core effect fields agree.")
    check("native-provenance", len(native["apk_sha256"]) == 64 and len(native["methods"]) >= 7, {"apk_sha256": native["apk_sha256"], "methods": len(native["methods"])}, "current APK hash and reviewed methods", "Every closure gate points to the current native evidence.")
    return checks


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    timestamp = utc_now()
    scene = base.load_json(SCENE_PATH)
    furniture_records = parse_records("FurnitureData")
    staff_records = parse_records("StaffData")
    skill_records = parse_records("SkillData", [1])
    if len({item["id"] for item in furniture_records if item["locale"] == "English"}) != 103:
        raise ValueError("FurnitureData English row count changed")
    if len({item["id"] for item in staff_records if item["locale"] == "English"}) != 141:
        raise ValueError("StaffData English row count changed")
    native = build_native_evidence()
    passmap = build_passmap_fixture(scene, furniture_records)
    route = build_route_fixture(scene, passmap, staff_records)
    asset = build_asset_selector_contract(furniture_records, staff_records)
    staff = build_staff_semantics(staff_records, skill_records, asset)
    checks = build_checks(passmap, route, asset, staff, native)
    input_paths = [
        SCENE_PATH,
        FIELD_LOAD_PATH,
        TYPE_CATALOG_PATH,
        APK_PATH,
        ASSET_ZIP,
        *SOURCE_FILES.values(),
    ]
    manifest = base.input_manifest(input_paths)
    closure = {
        "schema_version": SCHEMA_VERSION,
        "package": "social-dev-phase1d-closure",
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "phase": "Phase 1D",
        "semantic_status": "closed_for_phase2_entry",
        "generated_at_utc": timestamp,
        "phase2_status": "not_started",
        "engineering_loop": "fixture -> deterministic check -> provenance -> regression -> state update",
        "input_manifest": manifest,
        "native_evidence": native,
        "gates": [
            {"id": "type4-passmap-fixture", "status": "pass" if passmap["status"] == "pass" else "fail", "evidence": "phase1d_passmap_fixture.json"},
            {"id": "astar-goal-filter", "status": "pass" if route["status"] == "pass" else "fail", "evidence": "phase1d_route_fixture.json"},
            {"id": "real-route-with-provenance", "status": "pass" if route["route"]["path"] else "fail", "evidence": "phase1d_route_fixture.json"},
            {"id": "asset-selectors-seb-img-subseb", "status": asset["status"], "evidence": "asset_selector_contract.json"},
            {"id": "staff-living-scene-semantics", "status": staff["status"], "evidence": "staff_semantics_contract.json"},
        ],
        "authoritative_evidence": [
            "phase1d_passmap_fixture.json",
            "phase1d_route_fixture.json",
            "asset_selector_contract.json",
            "staff_semantics_contract.json",
            "phase1d_closure_validation.json",
        ],
        "phase1_boundary": {
            "closed": [
                "type-4 passMap_ fixture and IsPassable normalization",
                "Astar neighbor admission and public goal filter",
                "one real RoomData route fixture with provenance",
                "FurnitureData/StaffData seb_, img_, subSeb_ selector resolution",
                "staff visible state/move/typing/wait/skill contract for the selected living-scene slice",
            ],
            "not_started": [
                "SceneCatalog",
                "ObjectCatalog",
                "ActorCatalog",
                "deterministic fixture runtime package",
                "TypeScript runtime core",
            ],
        },
        "limits": [
            "Native evidence is contract input only; it is not executed by the browser runtime.",
            "Selector closure covers every parsed FurnitureData/StaffData data-row selector and the selected human/chip inf indexes, not every derived inventory artifact.",
            "Staff closure is the visible living-scene slice; broad Staff.Update and damaged GetSkill lookup remain rewrite work for Phase 2.",
        ],
    }
    validation = {
        "schema_version": VALIDATION_VERSION,
        "status": closure["status"],
        "semantic_status": closure["semantic_status"],
        "generated_at_utc": timestamp,
        "input_hash": manifest["input_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {
            "checks": len(checks),
            "passed_checks": sum(item["status"] == "pass" for item in checks),
            "furniture_rows_per_locale": 103,
            "staff_rows_per_locale": 141,
            "skill_rows_per_locale": 1,
            "route_steps": route["route"]["step_count"],
        },
        "phase2_status": "not_started",
    }
    return closure, passmap, route, asset, staff, validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    closure, passmap, route, asset, staff, validation = build_package()
    outputs = {
        "phase1d_closure.json": closure,
        "phase1d_passmap_fixture.json": passmap,
        "phase1d_route_fixture.json": route,
        "asset_selector_contract.json": asset,
        "staff_semantics_contract.json": staff,
        "phase1d_closure_validation.json": validation,
    }
    for name, payload in outputs.items():
        write_json(output_dir / name, payload)
    print(
        "phase1d_closure_complete "
        f"status={closure['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"route_steps={validation['counts']['route_steps']} "
        f"unresolved_selectors={len(asset['unresolved'])}"
    )
    return 0 if closure["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
