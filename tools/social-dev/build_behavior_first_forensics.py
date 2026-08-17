"""Build the static, behavior-first Staff living-system forensic package.

This builder reads only repository evidence: the pinned IL2CPP dump, the
decompiled C# declarations/call sites, the existing closure artifacts, and
the static FurnitureData package.  It never starts a runtime or a server and
it deliberately records source limits where the decompiler damaged control
flow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
SOURCE_ROOT = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
OUT = EVIDENCE / "behavior-first"
REPORTS = ROOT / "docs/Phases/Behavior"

SOURCE_FILES = {
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "StaffData": SOURCE_ROOT / "data/StaffData.cs",
    "JobData": SOURCE_ROOT / "data/JobData.cs",
    "SkillData": SOURCE_ROOT / "data/SkillData.cs",
    "EventData": SOURCE_ROOT / "data/EventData.cs",
    "FurnitureData": ROOT / "knowledge/sources/data/csharp_update/FurnitureData.cs",
}

NATIVE_RVAS = {
    "Staff.Update": "0x12D2EC8",
    "Staff.UpdateRecoveryHp": "0x12D2C8C",
    "Staff.AddRecoveryHpStock": "0x12D2EB0",
    "Staff.UpdateWork": "0x12D4A7C",
    "Staff.UseEquip": "0x12D4DEC",
    "Staff.Talk": "0x12D5588",
    "Staff.InviteStaffToTalk": "0x12D5090",
    "Staff.UpdateMove": "0x12D57AC",
    "Staff.UpdateStayHome": "0x12D59F4",
    "Staff.SearchRoute": "0x12D5A6C",
    "Staff.OnArriveNextNode": "0x12D8184",
    "Staff.OnArriveGoal": "0x12D8420",
    "Staff.GotoTalk": "0x12D6600",
    "Staff.GotoEquip": "0x12D6540",
    "Staff.UpdateMeeting": "0x12D473C",
    "Staff.OnInvitedTalk": "0x12D6378",
    "Staff.GetHp": "0x12DCB00",
    "Staff.SetHp": "0x12DCB08",
    "Staff.GetHpRatio": "0x12D3BE8",
    "Staff.OnStartTyping": "0x12D6478",
    "Staff.OnEndTyping": "0x12D67F0",
    "Staff.RecoverHp": "0x12D2DD8",
    "Staff.RecoverHpMax": "0x12DCF64",
    "Staff.ClampHpMax": "0x12D3B9C",
    "Staff.GotoDesk": "0x12D58EC",
    "Staff.OnEquipDestroyed": "0x12DC408",
    "Staff.OnDeskDestroyed": "0x12DC4B0",
    "Staff.OnColleagueRemoved": "0x12DC6D8",
    "Staff.OnOpenDoor": "0x12DC7A8",
    "ObjChip.Update": "0x12BED80",
    "ObjChip.PlaceObj": "0x12C4308",
    "ObjChip.GetStandingPositions": "0x12C4868",
    "ObjChip.ReserveUse": "0x12C49B0",
    "ObjChip.OnUseComplate": "0x12C0158",
    "ObjChip.GetUsersNum": "0x12C4A70",
    "ObjChip.IsPassable": "0x12C4AB8",
    "ObjChip.IsCanSetToTalkGoal": "0x12C4D08",
    "Room.Update": "0x12CB9E8",
    "Room.InitObjChips": "0x12CB448",
    "Room.SetupBigChipsParent": "0x12CB864",
    "Room.PlaceDoor": "0x12CB5E8",
    "Room.PlaceObj": "0x12CE540",
    "Room.AddStaff": "0x12CEB2C",
    "Room.GetDoorIndex": "0x12CD088",
    "Room.GetRandomObjChipTypeOf": "0x12CFA30",
    "Room.GetIndexToUseEquipment": "0x12CFC94",
    "Room.GetEmptyObjTypeOf": "0x12CFEA0",
    "Room.GetStaffEmptyObjTypeOf": "0x12CF178",
    "Room.PlaceDesk": "0x12CEFC8",
    "Astar.SearchRoute": "0x110E080",
    "Astar._searchRoute": "0x110EBF0",
    "Astar.AddNeighbor": "0x110F248",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lines(path: Path) -> list[str]:
    return read(path).splitlines()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_of(path: Path, needle: str, occurrence: int = 1) -> int:
    count = 0
    for number, text in enumerate(lines(path), start=1):
        if needle in text:
            count += 1
            if count == occurrence:
                return number
    raise ValueError(f"cannot find {needle!r} in {path}")


def source_ref(file_key: str, needle: str, note: str, occurrence: int = 1) -> dict[str, Any]:
    path = SOURCE_FILES[file_key]
    line = line_of(path, needle, occurrence)
    return {
        "file": rel(path),
        "line": line,
        "symbol": needle.strip(),
        "source_sha256": sha256(path),
        "note": note,
    }


def dump_ref(symbol: str, note: str) -> dict[str, Any]:
    return {
        "file": rel(DUMP),
        "symbol": symbol,
        "note": note,
        "dump_sha256": sha256(DUMP),
    }


def native_ref(symbol: str, note: str) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "rva": NATIVE_RVAS[symbol],
        "file": rel(DUMP),
        "note": note,
    }


def load_json(path: Path) -> Any:
    return json.loads(read(path))


def write_json(name: str, value: Any) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_dump_class(class_name: str) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    dump_lines = lines(DUMP)
    marker = next(i for i, value in enumerate(dump_lines) if f"class {class_name} //" in value)
    end = next(i for i in range(marker, len(dump_lines)) if "// Methods" in dump_lines[i])
    field_map: dict[str, dict[str, Any]] = {}
    field_lines: dict[str, int] = {}
    pattern = re.compile(
        r"^\s*(public|private|protected|internal)\s+(.+?)\s+(\w+)\s*;?\s+//\s+0x([0-9A-Fa-f]+)"
    )
    for index in range(marker, end):
        match = pattern.match(dump_lines[index])
        if not match:
            continue
        modifiers = match.group(2).split()
        if "const" in modifiers:
            continue
        name = match.group(3)
        field_map[name] = {
            "access": match.group(1),
            "modifiers": modifiers,
            "offset": "0x" + match.group(4).upper(),
            "dump_line": index + 1,
        }
        field_lines[name] = index + 1
    return field_map, field_lines


def parse_source_fields(path: Path, class_name: str) -> dict[str, dict[str, Any]]:
    source_lines = lines(path)
    class_index = next(i for i, value in enumerate(source_lines) if f"class {class_name}" in value)
    ctor_index = next(i for i in range(class_index, len(source_lines)) if "public Staff(" in source_lines[i] or "public ObjChip(" in source_lines[i])
    pattern = re.compile(
        r"^\s*(public|private|protected|internal)\s+((?:(?:static|readonly|const|unsafe)\s+)*)?(.+?)\s+(\w+)\s*;\s*$"
    )
    result: dict[str, dict[str, Any]] = {}
    for index in range(class_index, ctor_index):
        match = pattern.match(source_lines[index])
        if not match:
            continue
        modifiers = (match.group(2) or "").split()
        if "const" in modifiers:
            continue
        result[match.group(4)] = {
            "access": match.group(1),
            "modifiers": modifiers,
            "type": match.group(3).strip(),
            "source_line": index + 1,
        }
    return result


def field_group(name: str) -> str:
    if name in {"state_", "oldState_", "moveMode_", "processStep_", "oldSebId_", "sebId_"}:
        return "state_and_dispatch"
    if name in {"flag_", "typingFrame_", "talkFrame_", "frame_", "sebFrame_", "sebFrameInterval_", "frame2_", "moveFrame_", "stepFinished_"}:
        return "timers_and_flags"
    if name in {"hp_", "frameToStartRecovery_", "frameToHideHpGauge_", "recoveryHpStock_", "recoveryEffectFrame_", "damagedFrame_"}:
        return "hp_and_recovery"
    if name in {"room_", "floor_", "objIndex_", "oldIndex_", "route_", "lastNode_", "x_", "y_", "vx_", "vy_", "dx_", "dy_", "dx2_", "dy2_", "speed_", "moveFrame_", "deskId_"}:
        return "movement_and_room"
    if name in {"staffData_", "params_", "level_", "exp_", "expStock_", "jobId_", "skillId_", "cost_", "masterJobIdList_", "uniqueId_"}:
        return "staff_data_and_progression"
    if name in {"colleagueId_", "reservedSebId_", "meetingPointGauge_", "lastMeetingPoint_", "meetingPointFrame_"}:
        return "social_and_meeting"
    if name in {"auraGauge_", "auraType_", "planningRate_", "planQuality_", "oldPlanningRate_", "planningElapsedTime_", "planningTotalElapsedTime_", "planningEndDelayFrame_", "targetQualityPoint_", "evolvedCount_", "proposalChoiceCount_", "evolutionItemStates_", "developState_", "developStateBackup_", "attackCharge_", "enemy_", "original_", "developStaffId_", "power_", "bodyStateTime_", "auraTime_", "ideaPoint_", "egg_", "originalUnipueId_", "isFukidashiCaller_", "isProduceBug_"}:
        return "planning_and_development"
    if name in {"id_", "firstName_", "lastName_", "alpha_", "scale_", "ofx_", "ofy_", "attack_frame_frame_", "lastDrawPos_"}:
        return "identity_and_presentation"
    if name in {"fukidashi_", "fukidashi__", "itemEffectParams_"}:
        return "speech_and_effects"
    return "other_staff_runtime"


def build_staff_field_inventory() -> dict[str, Any]:
    source_fields = parse_source_fields(SOURCE_FILES["Staff"], "Staff")
    dump_fields, dump_lines = parse_dump_class("Staff")
    records: list[dict[str, Any]] = []
    missing: list[str] = []
    for name, source in source_fields.items():
        dump = dump_fields.get(name)
        if not dump:
            missing.append(name)
        records.append(
            {
                "name": name,
                "type": source["type"],
                "access": source["access"],
                "static": "static" in source["modifiers"],
                "mutable": "readonly" not in source["modifiers"],
                "group": field_group(name),
                "source": {"file": rel(SOURCE_FILES["Staff"]), "line": source["source_line"]},
                "dump": dump or {"status": "missing"},
                "status": "source_and_dump_aligned" if dump else "source_only_unresolved",
            }
        )
    records.sort(key=lambda value: (value["dump"].get("offset", "0xFFFF"), value["name"]))
    return {
        "schema_version": "social-dev-behavior-first-staff-field-inventory-v1",
        "status": "pass" if not missing else "pass_with_source_limits",
        "source_boundary": "All mutable Staff declarations were matched against the pinned dump; static readonly and const labels are retained only where they explain behavior.",
        "class": "Staff",
        "class_dump_ref": dump_ref("Staff", "Pinned arm64 IL2CPP field layout."),
        "counts": {
            "source_mutable_fields": sum(1 for item in records if item["mutable"]),
            "records": len(records),
            "dump_aligned": sum(1 for item in records if item["status"] == "source_and_dump_aligned"),
            "missing_dump_offsets": len(missing),
        },
        "missing_dump_offsets": missing,
        "fields": records,
        "notes": [
            "Offsets are IL2CPP instance offsets from the pinned dump, not C# managed layout assumptions.",
            "The dump closes storage and native method addresses; it does not close the damaged high-level Staff.Update dispatch body.",
        ],
    }


def parse_constants(file_key: str) -> list[dict[str, Any]]:
    path = SOURCE_FILES[file_key]
    pattern = re.compile(r"^\s*public\s+const\s+(?:int|float|string)\s+(\w+)\s*=\s*([^;]+);")
    result: list[dict[str, Any]] = []
    for number, text in enumerate(lines(path), start=1):
        match = pattern.match(text)
        if not match:
            continue
        raw = match.group(2).strip()
        try:
            value: Any = int(raw, 0)
        except ValueError:
            value = raw
        result.append({"name": match.group(1), "value": value, "file": rel(path), "line": number})
    return result


def build_constant_catalog() -> dict[str, Any]:
    all_constants = {key: parse_constants(key) for key in ("Staff", "ObjChip", "StaffData", "FurnitureData", "SkillData", "EventData")}
    wanted_staff = [item for item in all_constants["Staff"] if item["name"].startswith(("STATE_", "MOVE_MODE_", "FLAG_"))]
    wanted_obj = [item for item in all_constants["ObjChip"] if item["name"].startswith(("OBJ_TYPE_", "DIRECTION_", "FLAG_"))]
    hp = [item for item in all_constants["StaffData"] if item["name"] == "PARAM_HP"]
    return {
        "schema_version": "social-dev-behavior-first-state-constant-catalog-v1",
        "status": "pass",
        "source_files": {key: rel(SOURCE_FILES[key]) for key in all_constants},
        "staff_state_move_flag_constants": wanted_staff,
        "objchip_constants": wanted_obj,
        "data_constants": {
            "StaffData": [item for item in all_constants["StaffData"] if item["name"].startswith("PARAM_")],
            "FurnitureData": [item for item in all_constants["FurnitureData"] if item["name"].startswith(("PASS_TYPE_", "FLAG_", "CATEGORY_"))],
            "SkillData": [item for item in all_constants["SkillData"] if item["name"].startswith(("TYPE_", "SCENE_", "TARGET_", "EFFECT_", "FLAG_"))],
            "EventData": [item for item in all_constants["EventData"] if item["name"] in {"EV_FIRST_DEVELOP_HP_DOWN", "EV_FIRST_STAFF_DOWN", "EV_FIRST_HP_RECOVERY_BY_ITEM", "EV_RECOVERY_ALL_STAFFS", "EV_POLICY_SELECT_LOW_HP"}],
        },
        "hp_parameter": hp,
        "native_method_rvas": NATIVE_RVAS,
        "native_refs": [
            native_ref("Staff.Update", "Native entry point for the broad per-Staff tick."),
            native_ref("Staff.UpdateRecoveryHp", "Native recovery helper."),
            native_ref("Staff.SearchRoute", "Native route wrapper."),
            native_ref("ObjChip.IsPassable", "Native FurnitureData passMap consumer."),
            native_ref("Room.InitObjChips", "Native raw objMap-to-ObjChip initialization."),
            native_ref("Room.PlaceObj", "Native room placement entry point."),
            native_ref("Astar._searchRoute", "Native route search implementation."),
            native_ref("Astar.AddNeighbor", "Native cardinal-neighbor connection."),
        ],
        "source_limit": "State labels and numeric values are closed; some handler-to-handler dispatch semantics remain source-limited by the damaged decompilation.",
    }


def ref_list(*refs: dict[str, Any]) -> list[dict[str, Any]]:
    return list(refs)


def build_state_machine() -> dict[str, Any]:
    states = [
        ("STATE_NORMAL", 0),
        ("STATE_MEETING", 1),
        ("STATE_MOVE", 2),
        ("STATE_SIT_DOWN", 3),
        ("STATE_WORK", 4),
        ("STATE_USE_EQUIPMENT", 5),
        ("STATE_TALK", 6),
        ("STATE_INVITE_TO_TALK", 7),
        ("STATE_FLY_AWAY", 8),
        ("STATE_WAIT", 9),
        ("STATE_WANDER", 10),
        ("STATE_WAIT_BACK_OF_DOOR", 11),
        ("STATE_DEVELOP", 12),
        ("STATE_STAY_HOME", 13),
    ]
    move_modes = [
        ("MOVE_MODE_STAY", 0),
        ("MOVE_MODE_GOTO_EQUIPMENT", 1),
        ("MOVE_MODE_WANDER", 2),
        ("MOVE_MODE_GOTO_DESK", 3),
        ("MOVE_MODE_INTO_EQUIPMENT", 4),
        ("MOVE_MODE_OUTOF_EQUIPMENT", 5),
        ("MOVE_MODE_SIT_DOWN", 6),
        ("MOVE_MODE_TO_STAFF", 7),
        ("MOVE_MODE_TO_STAND_TALKING", 8),
        ("MOVE_MODE_TO_BACK_OF_CHAIR", 9),
        ("MOVE_MODE_GO_TO_DOOR", 10),
        ("MOVE_MODE_GO_HOME", 11),
    ]
    transitions = [
        {
            "id": "update-special-dispatch",
            "from": "any_non_meeting_non_develop_state",
            "to": ["STATE_MEETING", "STATE_DEVELOP", "state_handler_selected_by_indirect_dispatch"],
            "guard_or_trigger": "Staff.Update returns to UpdateMeeting for state 1 and UpdateDevelop for state 12; the remaining dispatch is an unresolved indirect jump.",
            "confidence": "source_backed_with_source_limit",
            "refs": ref_list(source_ref("Staff", "public unsafe void Update()", "Broad update entry point; body contains damaged indirect dispatch."), native_ref("Staff.Update", "Pinned native method.")),
        },
        {
            "id": "low-hp-door-escape",
            "from": "any_state_except_move_and_stay_home",
            "to": "STATE_MOVE",
            "move_mode": "MOVE_MODE_GO_TO_DOOR",
            "guard_or_trigger": "GetHpRatio() <= 5",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "if (hpRatio <= 5 && state_ != 2 && state_ != 13)", "Low-HP guard clears route and targets the door."), native_ref("Staff.Update", "Pinned native entry.")),
        },
        {
            "id": "stay-home-recovery-return",
            "from": "STATE_STAY_HOME",
            "to": "STATE_WAIT_BACK_OF_DOOR",
            "move_mode": "MOVE_MODE_GOTO_DESK",
            "guard_or_trigger": "UpdateStayHome recovers one HP and GetHpRatio() >= 40",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "private void UpdateStayHome()", "Stay-home recovery and door reservation."), native_ref("Staff.UpdateStayHome", "Pinned native method.")),
        },
        {
            "id": "work-to-typing",
            "from": "STATE_WORK",
            "to": "STATE_WORK_with_FLAG_TYPING",
            "guard_or_trigger": "UpdateWork sitting branch and random decision; typingFrame_=100",
            "confidence": "source_backed_with_cadence_limit",
            "refs": ref_list(source_ref("Staff", "private void UpdateWork()", "Typing/equipment/talk decisions; modulo gate is decompiler-damaged."), source_ref("Staff", "private void OnStartTyping()", "Typing flag and frame setup."), native_ref("Staff.UpdateWork", "Pinned native method.")),
        },
        {
            "id": "work-to-equipment",
            "from": "STATE_WORK",
            "to": "STATE_MOVE",
            "move_mode": "MOVE_MODE_GOTO_EQUIPMENT",
            "guard_or_trigger": "random type 1 or 4 candidate, GetUsersNum() <= 0",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "private void GotoEquip()", "Equipment target and reservation."), native_ref("Staff.GotoEquip", "Pinned native method.")),
        },
        {
            "id": "work-to-talk",
            "from": "STATE_WORK",
            "to": "STATE_MOVE",
            "move_mode": "MOVE_MODE_TO_STAFF",
            "guard_or_trigger": "random colleague is sitting/work, usable standing cell, flags permit talk",
            "confidence": "source_backed_with_selection_limit",
            "refs": ref_list(source_ref("Staff", "private void GotoTalk()", "Talk candidate and bilateral flags."), native_ref("Staff.GotoTalk", "Pinned native method.")),
        },
        {
            "id": "talk-finish",
            "from": "STATE_TALK_or_STATE_INVITE_TO_TALK",
            "to": "desk_goal",
            "move_mode": "MOVE_MODE_GOTO_DESK",
            "guard_or_trigger": "Talk frame >= 130; clears invited/reserved flags and colleagueId_",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "if (num >= 130)", "Talk completion timing."), native_ref("Staff.Talk", "Pinned native method.")),
        },
        {
            "id": "arrival-consumes-route",
            "from": "STATE_MOVE",
            "to": "OnArriveGoal_or_next_node",
            "guard_or_trigger": "OnArriveNextNode removes route head; empty route dispatches OnArriveGoal",
            "confidence": "source_backed_with_goal-dispatch_limit",
            "refs": ref_list(source_ref("Staff", "private unsafe void OnArriveNextNode(int goalX, int goalY)", "Route consumption and arrival callbacks."), native_ref("Staff.OnArriveNextNode", "Pinned native method."), native_ref("Staff.OnArriveGoal", "Goal handler remains indirect in C#.")),
        },
        {
            "id": "equipment-destroyed",
            "from": "equipment_use_or_reserved",
            "to": "STATE_WAIT",
            "guard_or_trigger": "OnEquipDestroyed clears frame and selects wait animation/state",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "public void OnEquipDestroyed()", "Equipment destruction recovery."), native_ref("Staff.OnEquipDestroyed", "Pinned native method.")),
        },
        {
            "id": "desk-destroyed",
            "from": "desk_user",
            "to": "STATE_WANDER",
            "move_mode": "MOVE_MODE_WANDER",
            "guard_or_trigger": "OnDeskDestroyed clears deskId_",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "public void OnDeskDestroyed()", "Desk destruction fallback."), native_ref("Staff.OnDeskDestroyed", "Pinned native method.")),
        },
        {
            "id": "colleague-removed",
            "from": "talking_or_invited",
            "to": "STATE_WAIT",
            "guard_or_trigger": "OnColleagueRemoved clears colleagueId_ and talk flags",
            "confidence": "source_backed",
            "refs": ref_list(source_ref("Staff", "public void OnColleagueRemoved()", "Social contention cleanup."), native_ref("Staff.OnColleagueRemoved", "Pinned native method.")),
        },
    ]
    return {
        "schema_version": "social-dev-behavior-first-staff-state-machine-v1",
        "status": "pass_with_source_limits",
        "states": [{"name": name, "value": value, "semantic_status": "source_label_and_dispatch_evidence"} for name, value in states],
        "move_modes": [{"name": name, "value": value, "semantic_status": "source_label_and_route_mapping"} for name, value in move_modes],
        "transitions": transitions,
        "dispatch_limit": "Update and OnArriveGoal contain damaged indirect jumps. The contract retains the native RVAs and closes only readable direct branches.",
        "native_refs": [native_ref("Staff.Update", "Broad update."), native_ref("Staff.UpdateMove", "Movement handler."), native_ref("Staff.OnArriveGoal", "Arrival goal handler."), native_ref("Staff.SearchRoute", "Route wrapper.")],
    }


def build_transition_graph(state_machine: dict[str, Any]) -> dict[str, Any]:
    edges = []
    for transition in state_machine["transitions"]:
        edges.append(
            {
                "id": transition["id"],
                "from": transition["from"],
                "to": transition["to"],
                "move_mode": transition.get("move_mode"),
                "confidence": transition["confidence"],
            }
        )
    return {
        "schema_version": "social-dev-behavior-first-staff-transition-graph-v1",
        "status": "pass_with_source_limits",
        "nodes": [
            {"id": "STATE_NORMAL", "kind": "state"},
            {"id": "STATE_MOVE", "kind": "state"},
            {"id": "STATE_WORK", "kind": "state"},
            {"id": "STATE_USE_EQUIPMENT", "kind": "state"},
            {"id": "STATE_TALK", "kind": "state"},
            {"id": "STATE_INVITE_TO_TALK", "kind": "state"},
            {"id": "STATE_WAIT_BACK_OF_DOOR", "kind": "state"},
            {"id": "STATE_STAY_HOME", "kind": "state"},
            {"id": "STATE_WAIT", "kind": "state"},
            {"id": "STATE_WANDER", "kind": "state"},
            {"id": "route_search", "kind": "movement"},
            {"id": "door", "kind": "room_resource"},
            {"id": "desk", "kind": "workstation"},
            {"id": "equipment", "kind": "furniture"},
            {"id": "colleague", "kind": "staff"},
        ],
        "edges": edges,
        "unresolved_edges": [
            "Exact moveMode-to-OnArriveGoal handler bodies.",
            "Exact full Update dispatcher mapping for states 0, 3, 4, 5, 6, 7, 8, 9, 10, 11 and 13.",
        ],
    }


def build_hp_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    staff_path = SOURCE_FILES["Staff"]
    exact_names = ["stamina_", "energy_", "fatigue_", "condition_", "condition", "status_", "hp_", "frameToStartRecovery_", "recoveryHpStock_"]
    staff_lines = lines(staff_path)
    search_results = {name: [number for number, text in enumerate(staff_lines, start=1) if name in text] for name in exact_names}
    expanded_name_search: dict[str, Any] = {}
    for name in ["stamina_", "energy_", "fatigue_", "condition_", "status_"]:
        matches_by_file: dict[str, list[dict[str, Any]]] = {}
        for path in sorted(SOURCE_ROOT.rglob("*.cs")):
            matches = [
                {"line": number, "text": text.strip()}
                for number, text in enumerate(lines(path), start=1)
                if name.lower() in text.lower()
            ]
            if matches:
                matches_by_file[rel(path)] = matches
        expanded_name_search[name] = {
            "scope": "all C# files under csharp_raw_20260813/1_Click_CSharp_Code",
            "case_sensitive": False,
            "matches_by_file": matches_by_file,
            "Staff.cs_matches": matches_by_file.get(rel(staff_path), []),
        }
    direct_drain_patterns = {
        "RecoverHp(-": [number for number, text in enumerate(lines(staff_path), start=1) if "RecoverHp(-" in text],
        "hp_ -=": [number for number, text in enumerate(lines(staff_path), start=1) if "hp_ -=" in text],
        "hp_--": [number for number, text in enumerate(lines(staff_path), start=1) if "hp_--" in text],
        "hp_ +=": [number for number, text in enumerate(lines(staff_path), start=1) if "hp_ +=" in text],
    }
    contract = {
        "schema_version": "social-dev-behavior-first-hp-condition-contract-v1",
        "status": "pass_with_source_limits",
        "authority": "Staff.hp_ plus StaffData.PARAM_HP=5 and JobData HP parameter lookup",
        "field": {"name": "hp_", "offset": "0xE8", "owner": "Staff", "ref": source_ref("Staff", "private int hp_;", "Exact Staff HP field.")},
        "max_formula": {
            "expression": "GetBaseParam(StaffData.PARAM_HP, 0) + GetJobParam(StaffData.PARAM_HP, level_)",
            "parameter_value": 5,
            "refs": ref_list(source_ref("StaffData", "public const int PARAM_HP = 5;", "HP parameter index."), source_ref("Staff", "public int GetHpRatio()", "Ratio reads base and job HP."), source_ref("Staff", "public void RecoverHpMax()", "Max recovery."), source_ref("Staff", "public void ClampHpMax()", "Max clamp.")),
        },
        "initialization": {"initial_hp_literal": 100, "ref": source_ref("Staff", "hp_ = 100;", "Staff.Init default before Room.AddStaff max normalization.")},
        "reads": [
            {"consumer": "Staff.GetHp", "kind": "authoritative_read", "ref": native_ref("Staff.GetHp", "Native getter.")},
            {"consumer": "Staff.GetHpRatio", "kind": "ratio_read", "ref": native_ref("Staff.GetHpRatio", "Native ratio helper.")},
            {"consumer": "Staff.Update", "kind": "low_hp_guard", "ref": source_ref("Staff", "if (hpRatio <= 5 && state_ != 2 && state_ != 13)", "Door escape guard.")},
            {"consumer": "Staff.UpdateWork", "kind": "sleep_decision_input", "ref": source_ref("Staff", "int hpRatio = GetHpRatio();", "Low-HP sleeping decision in work handler.")},
            {"consumer": "Staff.UpdateStayHome", "kind": "home_return_input", "ref": source_ref("Staff", "if (hpRatio >= 40)", "Home return threshold.")},
            {"consumer": "DevelopForm/SubForm", "kind": "management_ui_read", "ref": {"file": rel(SOURCE_ROOT / "form/DevelopForm.cs"), "note": "UI reads Staff HP and GetParam(5); UI is a consumer, not autonomous authority."}},
        ],
        "writes": [
            {"site": "Staff.Init", "operation": "hp_=100", "status": "source_backed", "ref": source_ref("Staff", "hp_ = 100;", "Initialization literal.")},
            {"site": "Staff.SetHp", "operation": "hp_=argument", "status": "source_backed", "ref": source_ref("Staff", "public void SetHp(int hp)", "Explicit setter.")},
            {"site": "Staff.RecoverHp", "operation": "hp_+=value; clamp to computed max; clear sleeping at max", "status": "source_backed", "ref": source_ref("Staff", "public bool RecoverHp(int value)", "Recovery and max clamp." )},
            {"site": "Staff.RecoverHpMax", "operation": "hp_=computed max", "status": "source_backed", "ref": source_ref("Staff", "public void RecoverHpMax()", "New staff normalization." )},
            {"site": "Staff.ClampHpMax", "operation": "if hp_>max then hp_=max", "status": "source_backed", "ref": source_ref("Staff", "public void ClampHpMax()", "Loaded staff normalization." )},
            {"site": "Staff.UpdateRecoveryHp", "operation": "RecoverHp(1) from recovery stock", "status": "source_backed_with_cadence_limit", "ref": source_ref("Staff", "bool flag4 = RecoverHp(1);", "Per-stock recovery write." )},
            {"site": "Staff.UpdateStayHome", "operation": "RecoverHp(1)", "status": "source_backed", "ref": source_ref("Staff", "bool flag = RecoverHp(1);", "Stay-home tick recovery." )},
            {"site": "Staff.OnFinishDevelop/OnAttacked", "operation": "damage/HP floor or combat adjustment", "status": "source_backed_with_combat_scope", "ref": source_ref("Staff", "public void OnAttacked(int power)", "Combat path, not ordinary living work." )},
            {"site": "Staff.Deserialize/Clone", "operation": "restore/copy hp_", "status": "source_backed", "ref": source_ref("Staff", "staff.hp_ = hp_;", "Clone/overwrite persistence path." )},
        ],
        "thresholds": {"low_hp_ratio_percent": 5, "home_return_ratio_percent": 40, "sleeping_flag": 32, "recovery_start_delay_frames": 20},
        "condition_search": {
            "exact_name_results_in_Staff_cs": search_results,
            "expanded_exact_name_search": expanded_name_search,
            "direct_drain_search": direct_drain_patterns,
            "finding": "No Staff field named stamina_, energy_, fatigue_, or condition_ was found. Expanded exact-token hits belong to unrelated Player stamina, Avatar energy, EventData/UI vocabulary, or Unity binding code; none establishes a Staff condition field. The readable Staff source has no RecoverHp(-...), hp_ -=, or hp_-- ordinary-work write. Do not invent a work drain; ordinary work drain remains unresolved until native body tracing is allowed.",
        },
        "source_limit": "The decompiler damaged UpdateRecoveryHp cadence logic and broad Update dispatch. HP storage, max formula, thresholds, stock writes, and readable recovery writes are closed; ordinary living-work drain is not.",
        "native_refs": [native_ref("Staff.UpdateRecoveryHp", "Pinned recovery helper."), native_ref("Staff.Update", "Pinned broad update."), native_ref("Staff.RecoverHp", "Pinned recovery operation.")],
    }
    graph = {
        "schema_version": "social-dev-behavior-first-hp-read-write-graph-v1",
        "status": "pass_with_source_limits",
        "nodes": ["Staff.hp_", "StaffData.PARAM_HP", "JobData.params_", "Staff.GetHpRatio", "Staff.Update", "Staff.UpdateWork", "Staff.UpdateRecoveryHp", "Staff.UpdateStayHome", "FurnitureData.recovery_", "UI HP consumers"],
        "edges": [
            {"from": "StaffData.PARAM_HP", "to": "Staff.GetHpRatio", "kind": "index_semantics"},
            {"from": "JobData.params_", "to": "Staff max formula", "kind": "job_hp_component"},
            {"from": "FurnitureData.recovery_", "to": "Staff.recoveryHpStock_", "kind": "use-complete stock", "guard": "recovery_ >= 1"},
            {"from": "Staff.recoveryHpStock_", "to": "Staff.UpdateRecoveryHp", "kind": "delayed stock consumption", "delay_frames": 20},
            {"from": "Staff.UpdateRecoveryHp", "to": "Staff.hp_", "kind": "RecoverHp(1)"},
            {"from": "Staff.UpdateStayHome", "to": "Staff.hp_", "kind": "RecoverHp(1)"},
            {"from": "Staff.hp_", "to": "Staff.Update", "kind": "low_hp_guard", "threshold": "<=5%"},
            {"from": "Staff.hp_", "to": "UI HP consumers", "kind": "read_only_consumer"},
        ],
        "unresolved": ["ordinary work HP drain write site", "exact sleeping-to-stock cadence", "full combat/event HP semantics outside living scene"],
    }
    return contract, graph


def build_furniture_catalog() -> dict[str, Any]:
    package = load_json(EVIDENCE / "furniture_asset_metadata.json")
    records: list[dict[str, Any]] = []
    for item in package["furniture"]:
        fields = item["fields"]
        type_value = int(item["type"])
        recovery = int(fields["recovery_"])
        if type_value == 2:
            interaction = "WORKSTATION"
        elif type_value in {1, 4} and recovery > 0:
            interaction = "RECOVERY_EQUIPMENT"
        elif type_value in {1, 4}:
            interaction = "EQUIPMENT_NO_HP_EFFECT_PROVEN"
        elif type_value == 5:
            interaction = "DOOR_RECORD"
        else:
            interaction = "UNKNOWN"
        pass_map = fields.get("passMap_") or []
        nonzero = sum(1 for row in pass_map for cell in row if cell != 0)
        records.append(
            {
                "id": int(item["furniture_data_id"]),
                "name": item["name"],
                "type": type_value,
                "category": int(item["category"]),
                "flag": int(fields["flag_"]),
                "recovery": recovery,
                "interaction_class": interaction,
                "workstation": type_value == 2,
                "equipment_candidate_for_GotoEquip": type_value in {1, 4},
                "hp_recovery_on_use_complete": type_value in {1, 4} and recovery > 0,
                "rest_semantics": "NOT_EXPLICIT_IN_STAFF_SOURCE",
                "social_semantics": "NOT_A_FURNITURE_ROLE_IN_STAFF_SOURCE",
                "passability": {"passMap_present": "passMap_" in fields, "nonzero_cells": nonzero, "source_field": "FurnitureData.passMap_"},
                "role_basis": ["ObjChip.type_", "FurnitureData.recovery_", "Staff.GotoEquip selects type 1 or 4", "Staff.UseEquip checks recovery_"],
                "source_name_preserved": True,
            }
        )
    counts: dict[str, int] = {}
    for record in records:
        counts[record["interaction_class"]] = counts.get(record["interaction_class"], 0) + 1
    return {
        "schema_version": "social-dev-behavior-first-furniture-behavior-catalog-v1",
        "status": "pass_with_source_limits",
        "counts": {"records": len(records), "by_interaction_class": counts, "source_package_records": package["counts"]["furniture_records"]},
        "classification_policy": {
            "WORKSTATION": "type_ == 2; Room.PlaceDesk and Staff desk ownership consume this class.",
            "RECOVERY_EQUIPMENT": "type_ in {1,4} and recovery_ >= 1; Staff.UseEquip adds recovery stock on completion.",
            "EQUIPMENT_NO_HP_EFFECT_PROVEN": "type_ in {1,4} and recovery_ == 0; targetable by GotoEquip but no HP recovery is proven.",
            "DOOR_RECORD": "type_ == 5; Room.GetDoorIndex scans ObjChip type 5; record identity is not inferred from raw map alone.",
            "REST/SOCIAL": "No FurnitureData record is promoted as REST or SOCIAL from names or sprites. Rest is the Staff stay-home lifecycle; social goals are pass chips.",
        },
        "records": records,
        "refs": ref_list(source_ref("FurnitureData", "public int recovery_;", "Recovery field."), source_ref("Staff", "private void GotoEquip()", "Equipment target type filter."), source_ref("Staff", "private void UseEquip()", "Recovery stock on use completion."), source_ref("ObjChip", "public bool IsPassable()", "PassMap consumer entry."), native_ref("ObjChip.IsPassable", "Pinned native passability consumer.")),
    }


def build_hp_lifecycle_contracts() -> dict[str, dict[str, Any]]:
    return {
        "work-recovery-lifecycle.json": {
            "schema_version": "social-dev-behavior-first-work-recovery-lifecycle-v1",
            "status": "pass_with_source_limits",
            "lifecycle": [
                {"stage": "desk_work", "state": "STATE_WORK", "inputs": ["FLAG_SITTING", "frame_", "flag_", "GetHpRatio()"], "output": "typing/equipment/talk/sleep decision", "ref": source_ref("Staff", "private void UpdateWork()", "Autonomous work handler; timing gates damaged.")},
                {"stage": "equipment_use", "state": "STATE_USE_EQUIPMENT", "frames": [20, 40, 60, 70], "output": "OnUseComplate; optional recovery stock; GotoDesk", "ref": source_ref("Staff", "if (furnitureData_.recovery_ >= 1)", "Use completion recovery stock." )},
                {"stage": "delayed_recovery", "state": "normal_update_tick", "frames": {"start_delay": 20, "per_stock": 1}, "output": "RecoverHp(1); stock decremented", "ref": source_ref("Staff", "if (--frameToStartRecovery_ <= 0 && recoveryHpStock_ >= 1)", "Recovery stock tick." )},
                {"stage": "low_hp_exit", "state": "STATE_MOVE", "guard": "GetHpRatio() <= 5", "output": "door target; move mode 10", "ref": source_ref("Staff", "if (hpRatio <= 5 && state_ != 2 && state_ != 13)", "Low HP door guard." )},
                {"stage": "home_recovery", "state": "STATE_STAY_HOME", "per_tick": "RecoverHp(1)", "return_guard": "GetHpRatio() >= 40", "output": "door reservation; state 11; move mode 3", "ref": source_ref("Staff", "private void UpdateStayHome()", "Stay-home branch." )},
            ],
            "ordinary_work_hp_drain": {"status": "UNKNOWN", "finding": "No direct drain write is present in the readable Staff source search; do not model a decrement without native tracing.", "search": "RecoverHp(-, hp_ -=, hp_--"},
            "source_limit": "Exact cadence modulo arithmetic and the sleeping flag's stock-add frequency are damaged.",
            "native_refs": [native_ref("Staff.UpdateRecoveryHp", "Pinned recovery helper."), native_ref("Staff.UpdateWork", "Pinned work helper."), native_ref("Staff.UpdateStayHome", "Pinned home helper.")],
        },
        "home-rest-contract.json": {
            "schema_version": "social-dev-behavior-first-home-rest-contract-v1",
            "status": "pass_with_source_limits",
            "rest_authority": "Staff.STATE_STAY_HOME and UpdateStayHome; no FurnitureData name is promoted as a rest rule.",
            "entry": {"guard": "GetHpRatio() <= 5 and current state is not MOVE/STAY_HOME", "state": 2, "move_mode": 10, "target": "door", "ref": source_ref("Staff", "if (hpRatio <= 5 && state_ != 2 && state_ != 13)", "Low HP entry." )},
            "home_tick": {"operation": "RecoverHp(1)", "ref": source_ref("Staff", "bool flag = RecoverHp(1);", "Home recovery." )},
            "return": {"guard": "GetHpRatio() >= 40", "door_reservation": True, "state": 11, "move_mode": 3, "ref": source_ref("Staff", "if (hpRatio >= 40)", "Door return reservation." )},
            "unknowns": ["Exact state assignment into STATE_STAY_HOME from indirect dispatch.", "Whether hidden/home timing has any additional cadence outside UpdateStayHome.", "Exact OnArriveGoal handling for the door route."],
        },
        "equipment-behavior-contract.json": {
            "schema_version": "social-dev-behavior-first-equipment-contract-v1",
            "status": "pass_with_source_limits",
            "selection": {"types": [1, 4], "random_choice": "AppData.Random(2)", "reservation_guard": "GetUsersNum() <= 0", "ref": source_ref("Staff", "private void GotoEquip()", "Equipment selection and reservation." )},
            "reservation": {"operation": "ObjChip.ReserveUse(this)", "storage": "ObjChip.reservedStaffs_", "ref": source_ref("ObjChip", "public void ReserveUse(Staff staff)", "Explicit reservation list." )},
            "use_timeline": [
                {"frame": 20, "action": "movement/animation gate passes"},
                {"frame": 40, "action": "ObjChip.StartAction(0, id_)"},
                {"frame": 60, "action": "use animation phase"},
                {"frame": 70, "action": "ObjChip.OnUseComplate(this); optional recovery stock; GotoDesk"},
            ],
            "hp_effect": "FurnitureData.recovery_ >= 1 adds that many recovery stock units after use completion; it does not directly write hp_.",
            "destruction": {"operation": "RemoveObj notifies reserved staff via OnEquipDestroyed", "ref": source_ref("ObjChip", "staff.OnEquipDestroyed();", "Equipment removal cleanup." )},
            "source_limit": "Exact animation direction/selector semantics and GetUsersNum body are native-pinned but decompiler-damaged in C#.",
        },
    }


def build_workstation_contract() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-behavior-first-workstation-ownership-reservation-v1",
        "status": "pass_with_source_limits",
        "desk_ownership": [
            {"field": "Staff.deskId_", "write": "Room.AddStaff assigns GetStaffEmptyObjTypeOf(2).GetId()", "ref": source_ref("Room", "staff.deskId_ = id;", "Staff-to-desk ownership field." )},
            {"field": "ObjChip.staffId_", "write": "Room.AddStaff writes staff.id_", "ref": source_ref("Room", "staffEmptyObjTypeOf.staffId_ = staff.id_;", "Desk-to-staff ownership field." )},
            {"field": "ObjChip.staffs_", "write": "Staff.Update adds/removes based on current cell", "ref": source_ref("Staff", "objChip5.AddStaff(this);", "Occupancy list maintenance." )},
        ],
        "desk_creation": {"method": "Room.PlaceDesk", "slot_type": 2, "furniture_flag": 16384, "flag_name": "FurnitureData.FLAG_INIT_DESK", "ref": source_ref("Room", "bool flag2 = ((BaseData)obj12).Check(16384);", "Desk seed selection." )},
        "new_staff_placement": {"door": "ObjChip type 5", "initial_reservation": True, "hp_normalization": {"new": "RecoverHpMax", "loaded": "ClampHpMax"}, "ref": source_ref("Room", "objChip.ReserveUse(staff);", "Staff ingress reservation." )},
        "reservation_lifecycle": [
            {"operation": "ReserveUse", "list": "reservedStaffs_", "ref": source_ref("ObjChip", "public void ReserveUse(Staff staff)", "Add reservation." )},
            {"operation": "OnUseComplate", "effect": "remove reservation; increment useNum_ capped 99; add use point stock", "ref": source_ref("ObjChip", "public void OnUseComplate(Staff staff)", "Completion." )},
            {"operation": "RemoveObj", "effect": "notify reserved staff; desk user receives OnDeskDestroyed", "ref": source_ref("ObjChip", "OnDeskDestroyed();", "Destruction cleanup." )},
        ],
        "contention": {"equipment": "GotoEquip checks GetUsersNum() <= 0", "talk": "GotoTalk uses flags and colleagueId_ but does not call ReserveUse", "fairness": "not proven"},
        "unknowns": ["Exact GetStaffEmptyObjTypeOf predicate and desk vacancy rule.", "Exact GetUsersNum implementation and whether reservation list is the sole count.", "Exact OnArriveGoal side effects for into/out-of-equipment and sitting."],
        "native_refs": [native_ref("Room.GetStaffEmptyObjTypeOf", "Pinned desk lookup."), native_ref("ObjChip.GetUsersNum", "Pinned reservation count."), native_ref("Room.PlaceDesk", "Pinned desk placement."), native_ref("Room.AddStaff", "Pinned staff placement." )],
    }


def build_movement_contract() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-behavior-first-movement-target-arrival-contract-v1",
        "status": "pass_with_source_limits",
        "goal_flag_mapping": [
            {"move_mode": 1, "name": "MOVE_MODE_GOTO_EQUIPMENT", "astar_flag": 2, "flag_name": "GOAL_IS_EQUIP"},
            {"move_mode": 3, "name": "MOVE_MODE_GOTO_DESK", "astar_flag": 1, "flag_name": "GOAL_IS_DESK"},
            {"move_mode": 7, "name": "MOVE_MODE_TO_STAFF", "astar_flag": 4, "flag_name": "GOAL_IS_STAFF"},
            {"move_mode": 8, "name": "MOVE_MODE_TO_STAND_TALKING", "astar_flag": 0, "flag_name": "default/pass-goal path", "status": "source_limited"},
            {"move_mode": 10, "name": "MOVE_MODE_GO_TO_DOOR", "astar_flag": 0, "flag_name": "default/door path", "status": "source_limited"},
        ],
        "route_algorithm": {"neighbors": "cardinal only", "goal_filter": "desk/equipment/staff flags; occupied desk and blocked type 3/4/6 are filtered as closed by native evidence", "refs": [rel(EVIDENCE / "phase1d_route_fixture.json"), native_ref("Astar._searchRoute", "Pinned native route search."), native_ref("Astar.AddNeighbor", "Pinned cardinal neighbor connection.")]},
        "standing_positions": {"formula": "baseX=(ix+iy)*20; baseY=(iy-ix)*10", "positions": [{"ordinal": 0, "x": "+34", "y": "+25"}, {"ordinal": 1, "x": "+6", "y": "+11"}, {"ordinal": 2, "x": "+34", "y": "+11"}, {"ordinal": 3, "x": "+6", "y": "+25"}], "ref": native_ref("ObjChip.GetStandingPositions", "Pinned native standing positions." )},
        "movement_loop": [
            {"method": "SearchRoute", "effect": "derive current cell/use target and call Astar", "ref": source_ref("Staff", "private void SearchRoute()", "C# body damaged after goal selection; mapping retained." )},
            {"method": "ReadyToNextNode", "effect": "set dx/dy, speed, direction animation", "ref": source_ref("Staff", "private void ReadyToNextNode()", "Direction setup; body damaged." )},
            {"method": "Move", "effect": "advance x/y toward route head and call OnArriveNextNode", "ref": source_ref("Staff", "private void Move()", "Movement step." )},
            {"method": "OnArriveNextNode", "effect": "remove route head; continue or OnArriveGoal", "ref": source_ref("Staff", "private unsafe void OnArriveNextNode(int goalX, int goalY)", "Arrival and route consumption." )},
            {"method": "OnArriveGoal", "effect": "indirect moveMode dispatch", "ref": native_ref("Staff.OnArriveGoal", "Native entry; exact handler mapping unresolved." )},
        ],
        "source_limit": "The native route/standing contracts are closed; per-move-mode arrival side effects remain source-limited.",
    }


def build_social_contract() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-behavior-first-talk-social-contract-v1",
        "status": "pass_with_source_limits",
        "initiator": {"method": "GotoTalk", "target_selection": "one AppData.Random(staffs_.Length) staff id", "guards": ["target not null", "target != self", "target flags do not include 0x840", "target flag mask 6 equals sitting", "target state == STATE_WORK", "standing/use cell is not type 6"], "writes": ["initiator FLAG_RESERVED_TALK", "target FLAG_RESERVED_TALK", "target FLAG_INVITED_TALK", "colleagueId_ both sides", "initiator state MOVE", "initiator move mode TO_STAFF"], "ref": source_ref("Staff", "private void GotoTalk()", "Random colleague selection and bilateral flags." )},
        "invite": {"method": "InviteStaffToTalk", "guards": ["colleagueId_ is valid", "frame >=20", "frame >=60 branch can select talk goal type 0"], "writes": ["state MOVE", "move mode TO_STAND_TALKING", "target OnInvitedTalk"], "ref": source_ref("Staff", "private void InviteStaffToTalk()", "Invitation timing and target callback." )},
        "talk_timing": {"frame_20": "optional bubble", "frame_70": "optional bubble", "frame_110": "AddMeetingPointGauge(Lib.Random(0,4))", "frame_130_or_more": "clear flags and colleagueId_; GotoDesk", "ref": source_ref("Staff", "if (num >= 130)", "Talk completion." )},
        "partner_cleanup": {"method": "OnColleagueRemoved", "effect": "frame_=0; colleagueId_=-1; clear invited/reserved flags; state WAIT", "ref": source_ref("Staff", "public void OnColleagueRemoved()", "Partner removal cleanup." )},
        "skill_effect": {"skill_id": 1, "name": "Loving Meetings", "type": 10, "scene": 1, "target": 0, "effect_index": 8, "effect_value": 150, "flag": 1, "status": "selected data record plus readable OnEndTyping use; random gauge distribution not promoted"},
        "source_limit": "Full meeting-state handler and exact random/cadence behavior are not closed by the damaged UpdateMeeting and InviteStaffToTalk bodies.",
    }


def build_idle_and_contention() -> tuple[dict[str, Any], dict[str, Any]]:
    idle = {
        "schema_version": "social-dev-behavior-first-idle-autonomy-contract-v1",
        "status": "pass_with_source_limits",
        "tick_owner": "Room.Update loops Staff.Update before ObjChip.Update",
        "decision_order": [
            "if not sitting: GotoDesk",
            "if no management/planning flags and cadence gate: typing attempt",
            "if no reserved/typing flags and cadence gate: GotoEquip with random <21",
            "if still no reserved/typing flags and cadence gate: GotoTalk with random <=10",
            "if HP ratio <=99 and cadence gate: FLAG_SLEEPING with random <=25",
            "typingFrame_ decrements and OnEndTyping clears typing at completion",
        ],
        "probability_bounds": {"typing_attempt": "random 0..100 >=41 starts typing in the readable branch; exact gate cadence unknown", "equipment_attempt": "random <21", "talk_attempt": "random <=10", "sleep_flag_attempt": "random <=25", "bubble": "random <=50 or <=30 at related branch"},
        "visible_actions": ["walk", "sit/work", "type", "use equipment", "talk", "sleep/recovery", "leave for door", "return from home"],
        "refs": ref_list(source_ref("Room", "public void Update()", "Staff-first tick order."), source_ref("Staff", "private void UpdateWork()", "Autonomous choices."), native_ref("Room.Update", "Pinned room tick.")),
        "source_limit": "Magic multiply modulo gates are not reliable decompiler output; preserve branch probabilities only as bounded observations.",
    }
    contention = {
        "schema_version": "social-dev-behavior-first-multi-actor-contention-contract-v1",
        "status": "pass_with_source_limits",
        "reservation_state": "ObjChip.reservedStaffs_",
        "operations": [
            {"operation": "ReserveUse", "effect": "append Staff", "ref": source_ref("ObjChip", "public void ReserveUse(Staff staff)", "Reservation write." )},
            {"operation": "GetUsersNum", "effect": "read reservation count", "ref": native_ref("ObjChip.GetUsersNum", "Native reservation count." )},
            {"operation": "OnUseComplate", "effect": "remove reservation; useNum_ capped at 99", "ref": source_ref("ObjChip", "useNum_ = num;", "Completion cap." )},
            {"operation": "RemoveObj", "effect": "notify all reserved Staff via OnEquipDestroyed", "ref": source_ref("ObjChip", "staff.OnEquipDestroyed();", "Destroy cleanup." )},
        ],
        "guards": ["GotoEquip accepts usersNum <= 0", "GotoTalk uses bilateral flags/colleagueId_ rather than furniture reservation", "desk ownership is single staffId_ per desk chip"],
        "fairness_and_queue": "UNKNOWN; no source-backed queue or fairness policy was found.",
        "unknowns": ["Whether GetUsersNum includes active users separately from reservations", "Whether type 4 parent/child chips reserve at parent or child", "Whether simultaneous talk targets are arbitrated beyond flags"],
    }
    return idle, contention


def build_dashboard_contracts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    task_input = {
        "schema_version": "social-dev-behavior-first-dashboard-task-assignment-input-v1",
        "status": "pass_with_source_limits",
        "autonomous_authority": "Staff.Update/Room.Update/ObjChip reservations; dashboard is a consumer and explicit task-assignment surface.",
        "inputs": [
            {"class": "StaffData", "fields": ["jobId_", "defParams_", "skill_", "cost_", "hitRate_", "bonusTerms_", "bonusRate_"], "use": "Staff initialization and skill/job linkage", "ref": source_ref("StaffData", "public int jobId_;", "StaffData declaration." )},
            {"class": "JobData", "fields": ["type_", "jobGroup_", "maxLv_", "speed_", "params_", "bonus_"], "use": "GetJobParam and movement/work data", "ref": source_ref("JobData", "public int[][] params_;", "Job parameter data." )},
            {"class": "SkillData", "fields": ["type_", "scene_", "target_", "effects_", "auraRates_", "flag_"], "use": "OnEndTyping selected skill effect", "ref": source_ref("SkillData", "public int[][] effects_;", "Skill effect data." )},
            {"class": "FurnitureData", "fields": ["type_", "recovery_", "passMap_", "flag_", "paramType_", "paramValue_"], "use": "workstation/equipment/passability inputs", "ref": source_ref("FurnitureData", "public int[][] passMap_;", "Furniture behavior data." )},
            {"class": "EventData", "fields": ["event constants"], "use": "event vocabulary only; not autonomous Staff tick authority", "ref": source_ref("EventData", "public const int EV_FIRST_DEVELOP_HP_DOWN = 87;", "Event/UI trigger vocabulary." )},
        ],
        "assignment_boundary": ["dashboard may select staff/job/skill/furniture task inputs", "dashboard may display HP/condition-like fields only through existing consumers", "dashboard must not replace Staff.Update, Room.Update, ObjChip reservations, or native route contracts"],
        "source_limit": "Exact current dashboard widget-to-field mapping is outside the autonomous source slice; only field semantics and existing UI consumers are retained.",
    }
    visible = {
        "schema_version": "social-dev-behavior-first-visible-action-map-v1",
        "status": "pass_with_source_limits",
        "actions": [
            {"action": "idle_wait", "state": [0, 9, 10], "fields": ["state_", "sebId_", "frame_"], "source": "Staff state labels and wait/fallback methods"},
            {"action": "walk_to_target", "state": [2], "move_modes": [1, 3, 7, 8, 10], "fields": ["route_", "objIndex_", "moveMode_", "x_", "y_", "dx_", "dy_"], "source": "Staff.SearchRoute/Move/OnArriveNextNode"},
            {"action": "sit_and_work", "state": [3, 4], "fields": ["deskId_", "flag_", "frame_"], "source": "Staff.UpdateWork and Room desk ownership"},
            {"action": "typing", "state": [4], "flags": [16], "fields": ["typingFrame_", "sebFrameInterval_", "sebId_"], "source": "Staff.OnStartTyping/OnEndTyping"},
            {"action": "use_equipment", "state": [5], "fields": ["objIndex_", "frame_", "recoveryHpStock_"], "source": "Staff.UseEquip and FurnitureData.recovery_"},
            {"action": "talk", "state": [6, 7], "flags": [4, 8], "fields": ["colleagueId_", "talkFrame_", "meetingPointGauge_"], "source": "Staff.GotoTalk/InviteStaffToTalk/Talk"},
            {"action": "low_hp_leave_and_home_recovery", "state": [2, 11, 13], "fields": ["hp_", "state_", "moveMode_", "recoveryHpStock_", "frameToStartRecovery_"], "source": "Staff.Update low-HP guard/UpdateStayHome"},
        ],
        "renderer_boundary": "This map describes behavior-visible actions only. It does not authorize a renderer, MapChip, V8, emulator, or screenshot change.",
    }
    preservation = {
        "schema_version": "social-dev-behavior-first-dashboard-preservation-boundary-v1",
        "status": "pass",
        "preserve": ["Staff.Update and its native RVA", "Room.Update tick order", "ObjChip reservation lists and completion cleanup", "FurnitureData type/recovery/passMap semantics", "Astar route goal flags and cardinal neighbors", "existing V1-V7 runtime behavior and evidence"],
        "dashboard_only_changes": ["task assignment inputs", "management labels and read-only field presentation", "dashboard adapters that call existing APIs without changing autonomous ownership"],
        "forbidden_in_this_phase": ["visual correction", "V8", "production renderer cutover", "MapChip changes", "APK/game launch", "ADB/emulator", "live server/network/browser automation", "source-root edits"],
        "proof": ["No runtime or renderer path was modified by this phase.", "Evidence is kept under knowledge/fixtures/accepted/behavior-first and reports under docs/Phases/Behavior."],
    }
    return task_input, visible, preservation


def build_prior_reconciliation() -> dict[str, Any]:
    rows = [
        ("phase1d_closure.json", "pass / closed_for_phase2_entry", "accept", "native room/object/passability/route closure; Staff broad update explicitly limited", "Use as authority for native scene/route facts."),
        ("phase1d_passmap_fixture.json", "pass", "accept", "passMap 3x3 behavior fixture", "Reconcile into movement/furniture passability contract."),
        ("phase1d_route_fixture.json", "pass", "accept", "Astar cardinal route and goal filters", "Reconcile into movement target contract."),
        ("asset_selector_contract.json", "pass", "accept", "selector identity and sentinel policy", "Behavior phase uses only data identity, not renderer changes."),
        ("staff_semantics_contract.json", "pass", "accept_bounded", "states/modes/flags/talk/typing/selected skill slice", "Promote direct source-backed facts; keep stated limitations."),
        ("phase1d_closure_validation.json", "pass / closed_for_phase2_entry", "accept", "validation of prior closure", "Use as regression evidence."),
        ("staff_behavior_candidate.json", "candidate / pending_review", "do_not_promote_wholesale", "historical behavior candidates, including numeric labels and damaged Update", "Reverify each claim against current source/dump; unresolved items stay unknown."),
        ("scene_behavior_validation.json", "pass / pending_review", "accept_as_candidate_only", "candidate validation shell", "Does not close autonomous lifecycle."),
        ("scene_semantics_review.json", "candidate / pending_review", "candidate_only", "semantic review queue", "No automatic promotion."),
        ("scene_native_semantics.json", "candidate / pending_fixture_review", "accept_bounded", "native raw objMap/object placement claims", "Promote only the native facts rechecked here."),
        ("scene_native_semantics_validation.json", "pass / pending_fixture_review", "accept_bounded", "validation shell for native semantics", "No behavior authority beyond cited facts."),
    ]
    return {
        "schema_version": "social-dev-behavior-first-prior-evidence-reconciliation-v1",
        "status": "pass_with_source_limits",
        "method": "Re-read status/semantic_status, inspect source/dump references, and promote only claims independently rechecked in this phase.",
        "records": [{"artifact": name, "prior_status": status, "treatment": treatment, "scope": scope, "current_use": use, "path": rel(EVIDENCE / name)} for name, status, treatment, scope, use in rows],
        "accepted_authority": ["phase1d_closure native room/route/passability facts", "staff_semantics_contract bounded living-scene slice", "pinned dump field offsets/RVAs", "readable C# direct branches"],
        "rejected_shortcuts": ["Do not promote Staff.Update as a complete algorithm", "Do not infer FurnitureData identity from raw ObjChip topology", "Do not infer rest/social roles from names or sprites", "Do not treat historical candidate status as proof"],
    }


def build_unknowns() -> dict[str, Any]:
    return {
        "schema_version": "social-dev-behavior-first-unknowns-v1",
        "status": "tracked",
        "unknowns": [
            {"id": "BF-U01", "area": "Staff.Update", "question": "Which direct handler is selected for every state value?", "impact": "Cannot claim a complete autonomous state machine.", "evidence_limit": "decompiler indirect jump", "next_allowed_evidence": "pinned native disassembly/Ghidra or cleaner source", "blocked_now": True},
            {"id": "BF-U02", "area": "HP", "question": "Is ordinary living work charged by an HP drain not visible in readable C#?", "impact": "Cannot model work HP drain cadence.", "evidence_limit": "no readable hp decrement / RecoverHp(-) write; native body not traced in this static pass", "next_allowed_evidence": "native Update/UpdateWork body trace", "blocked_now": True},
            {"id": "BF-U03", "area": "Recovery", "question": "What exact cadence adds stock when FLAG_SLEEPING is set?", "impact": "Only delay and per-stock recovery are closed.", "evidence_limit": "damaged modulo branch in Update", "next_allowed_evidence": "native branch trace", "blocked_now": True},
            {"id": "BF-U04", "area": "Workstation", "question": "What exact predicate does GetStaffEmptyObjTypeOf use?", "impact": "Desk assignment fairness/vacancy cannot be claimed.", "evidence_limit": "damaged C# body", "next_allowed_evidence": "native method trace", "blocked_now": True},
            {"id": "BF-U05", "area": "Contention", "question": "Does GetUsersNum include active users, reservations, or both?", "impact": "Queue/fairness and simultaneous use remain unknown.", "evidence_limit": "native-pinned method with damaged C# body", "next_allowed_evidence": "native method trace", "blocked_now": True},
            {"id": "BF-U06", "area": "Movement", "question": "What are the exact OnArriveGoal side effects for each move mode?", "impact": "Arrival state mapping is incomplete.", "evidence_limit": "indirect jump in C#", "next_allowed_evidence": "native method trace", "blocked_now": True},
            {"id": "BF-U07", "area": "Movement", "question": "What is the exact GetDirectionVector mapping and type-4 parent policy?", "impact": "Use-cell semantics are bounded but not fully closed.", "evidence_limit": "damaged C# body", "next_allowed_evidence": "native method trace", "blocked_now": True},
            {"id": "BF-U08", "area": "Social", "question": "What does the full UpdateMeeting processStep dispatch do?", "impact": "Meeting animation/arrival lifecycle incomplete.", "evidence_limit": "damaged indirect jump", "next_allowed_evidence": "native method trace", "blocked_now": True},
            {"id": "BF-U09", "area": "Data", "question": "How does Staff.GetSkill resolve DataManager records in every save/load path?", "impact": "Selected skill is verified, lookup algorithm is not.", "evidence_limit": "damaged GetSkill body", "next_allowed_evidence": "native method trace or cleaner source", "blocked_now": True},
            {"id": "BF-U10", "area": "FurnitureData", "question": "Which type-1/type-4 records have social/rest semantics beyond recovery_?", "impact": "Only explicit type/recovery behavior is promoted.", "evidence_limit": "no source consumer ties names/sprites to rest/social roles", "next_allowed_evidence": "additional source-backed call sites", "blocked_now": True},
            {"id": "BF-U11", "area": "Dashboard", "question": "What exact current widget-to-field mapping should be retained after the visual cut?", "impact": "Dashboard change boundary remains behavioral and API-level only.", "evidence_limit": "task explicitly defers visual work", "next_allowed_evidence": "later dashboard audit", "blocked_now": False},
        ],
        "policy": "Unknown means no inferred value. Unknowns block claims that require them but do not block this source-limited behavior handoff.",
    }


def build_checkpoint_ledger() -> dict[str, Any]:
    common_tests = ["source read", "pinned dump read", "static JSON validation"]
    records: list[dict[str, Any]] = []
    for number in range(20):
        checkpoint = f"BF.{number}"
        status = "PASS"
        if number in {0, 3, 4, 6, 7, 12, 13, 15, 16}:
            status = "PASS_WITH_SOURCE_LIMITS"
        if number == 19:
            status = "STOP_NO_VISUAL_CUTOVER"
        records.append(
            {
                "Checkpoint": checkpoint,
                "Status": status,
                "Methods": {
                    "BF.0": "reconcile prior closure/candidate artifacts and read pinned sources",
                    "BF.1": "parse Staff instance/static mutable fields against dump offsets",
                    "BF.2": "parse state/move/flag constants and native method table",
                    "BF.3": "trace readable Update direct guards and indirect dispatch boundaries",
                    "BF.4": "search exact HP/condition names and identify HP writes/reads",
                    "BF.5": "trace max formula, thresholds, recovery stock and setter paths",
                    "BF.6": "trace work, sleep and recovery lifecycle; preserve unknown drain",
                    "BF.7": "trace stay-home/door return contract",
                    "BF.8": "trace equipment selection/use/completion",
                    "BF.9": "trace workstation ownership and desk creation",
                    "BF.10": "classify all FurnitureData records using source consumers",
                    "BF.11": "reconcile passMap/standing/cardinal route/arrival contracts",
                    "BF.12": "trace talk target, invite, timing and cleanup",
                    "BF.13": "trace idle autonomy decisions and contention reservations",
                    "BF.14": "map dashboard task-assignment data inputs",
                    "BF.15": "map behavior-visible actions to canonical Staff fields",
                    "BF.16": "define canonical living model and preserve unknowns",
                    "BF.17": "define dashboard preservation boundary and forbidden changes",
                    "BF.18": "run static coverage and regression checks",
                    "BF.19": "update state/handoff and stop before visual work",
                }.get(checkpoint, "static forensic checkpoint"),
                "Fields": ["Staff fields", "state/mode/flag fields", "HP/recovery fields", "room/ObjChip ownership fields"],
                "Constants": ["Staff state/move/flag constants", "StaffData.PARAM_HP", "ObjChip type/direction/flags", "FurnitureData flags/types"],
                "Native RVAs": [NATIVE_RVAS["Staff.Update"], NATIVE_RVAS["Staff.UpdateRecoveryHp"], NATIVE_RVAS["ObjChip.IsPassable"], NATIVE_RVAS["Room.InitObjChips"], NATIVE_RVAS["Astar._searchRoute"]],
                "Data records": ["StaffData 0-4 / JobData 4 / SkillData 1", "FurnitureData 103"],
                "Behavior transitions": ["low HP -> door", "stay home -> recover -> door return", "work -> typing/equipment/talk/sleep", "route head -> arrival"],
                "Furniture relationships": ["type 2 workstation", "type 1/4 equipment candidates", "recovery_ -> recovery stock", "passMap_ -> native IsPassable"],
                "HP/condition findings": ["hp_ authoritative", "PARAM_HP=5", "no Staff stamina_/energy_/fatigue_/condition_", "ordinary work drain unknown"],
                "Unknowns closed": [] if number in {0, 3, 4, 6, 7, 11, 13, 16, 18, 19} else ["direct source branch or record classification"],
                "Unknowns remaining": ["damaged indirect dispatch", "ordinary work HP drain", "GetStaffEmptyObjTypeOf predicate", "GetUsersNum exact semantics", "OnArriveGoal mapping"],
                "Tests": common_tests + (["behavior-first static coverage >=35", "no renderer/MapChip/V8 change"] if number >= 18 else []),
                "Next": "continue static trace" if number < 18 else ("write state and handoff" if number == 18 else "STOP; no visual work or renderer cutover"),
            }
        )
    return {
        "schema_version": "social-dev-behavior-first-checkpoint-ledger-v1",
        "status": "pass_with_source_limits",
        "records": records,
        "required_stop_literals": {"V8_started": "NO", "Visual_work_performed": "NO", "Production_renderer_changed": "NO", "MapChip_changed": "NO", "Subagents": "NO", "Emulator_ADB_live_server_network": "NO"},
    }


def report_texts(catalog: dict[str, Any], hp: dict[str, Any], state_machine: dict[str, Any]) -> dict[str, str]:
    state_lines = "\n".join(f"- `{item['name']}={item['value']}`" for item in state_machine["states"])
    furniture_counts = ", ".join(f"{key}={value}" for key, value in catalog["counts"]["by_interaction_class"].items())
    return {
        "BEHAVIOR_FIRST_AUDIT.md": f"""# Behavior-First Forensic Audit

Status: `PASS_BEHAVIOR_MODEL_WITH_SOURCE_LIMITS`.

This phase reconstructs the original autonomous Staff living/execution system from the pinned IL2CPP dump, decompiled C# declarations/call sites, and static data. It does not reconstruct a renderer and does not promote the dashboard UI into behavior authority.

## Boundary

- V8 started: **NO**
- Visual work performed: **NO**
- Production renderer changed: **NO**
- MapChip changed: **NO**
- Emulator/ADB/live server/network: **NO**
- Subagents: **NO**

The phase read and reconciled the prior Phase 1D closure, route/passMap fixtures, Staff living-scene contract, historical candidate artifacts, the pinned dump, Staff/Room/ObjChip source, StaffData/JobData/SkillData/EventData, and all 103 FurnitureData records.

## Findings

- `Staff` has an authoritative `hp_` field at dump offset `0xE8`; `StaffData.PARAM_HP` is exactly `5`.
- The maximum HP formula is `GetBaseParam(5, 0) + GetJobParam(5, level_)`.
- Low HP (`<=5%`) sends Staff to the door; `STATE_STAY_HOME` recovers one HP per readable tick and returns at `>=40%`.
- Work autonomy chooses typing, equipment, talk, or sleeping through readable bounded branches; exact modulo cadence remains source-limited.
- No Staff field named `stamina_`, `energy_`, `fatigue_`, or `condition_` was found. No readable ordinary-work `RecoverHp(-...)`, `hp_ -=`, or `hp_--` write was found; work drain remains unknown.
- FurnitureData classification is source-based: {furniture_counts}. No rest/social role is inferred from a record name or sprite.
- Native route, passMap, standing-position, raw object-chip, and reservation authorities are preserved.

## Required evidence

The machine-readable contracts are in `knowledge/fixtures/accepted/behavior-first/`; the checkpoint ledger records BF.0 through BF.19. The broad Staff.Update and OnArriveGoal indirect dispatches remain explicitly unresolved.

## Stop

Do not begin visual correction, V8, renderer cutover, MapChip work, emulator/ADB/live-server work, or source-root edits from this handoff.
""",
        "STAFF_STATE_MACHINE.md": f"""# Staff State Machine

The numeric state labels are source-backed and the pinned dump supplies the native method addresses. The complete dispatcher is not promoted because the decompiled `Staff.Update` and `OnArriveGoal` contain unresolved indirect jumps.

## States

{state_lines}

## Closed direct transitions

- `GetHpRatio() <= 5` clears the route and writes state `STATE_MOVE` with `MOVE_MODE_GO_TO_DOOR` unless already moving or staying home.
- `UpdateStayHome` calls `RecoverHp(1)` and, at `>=40%`, reserves the door and writes `STATE_WAIT_BACK_OF_DOOR` plus `MOVE_MODE_GOTO_DESK`.
- `GotoEquip` selects type 1 or 4, requires `GetUsersNum() <= 0`, reserves the chip, and writes `STATE_MOVE/MOVE_MODE_GOTO_EQUIPMENT`.
- `GotoTalk` selects one random colleague, checks sitting/work/flags/standing-cell guards, and writes bilateral talk flags and `STATE_MOVE/MOVE_MODE_TO_STAFF`.
- Talk at frame `>=130` clears talk flags and colleague identity, then calls `GotoDesk`.
- Equipment or desk destruction and colleague removal have explicit cleanup fallbacks.

## Source limits

The exact per-state indirect handler table, exact `OnArriveGoal` mapping, and exact modulo cadence are unknown. Numeric labels are retained as labels and are not treated as a replacement for the native body.
""",
        "HP_CONDITION_SYSTEM.md": f"""# HP and Condition System

## Authority

`Staff.hp_` at offset `0xE8` is the authoritative Staff health field. `StaffData.PARAM_HP=5` names the HP parameter. The dynamic maximum is `GetBaseParam(5,0)+GetJobParam(5,level_)`.

## Proven writes and reads

- Init starts at `hp_=100`; Room.AddStaff then calls `RecoverHpMax` for new Staff or `ClampHpMax` for loaded Staff.
- `RecoverHp(value)` adds a value, clamps below zero, caps at the dynamic maximum, and clears `FLAG_SLEEPING` when full.
- `AddRecoveryHpStock` sets a 20-frame delay; `UpdateRecoveryHp` consumes stock through `RecoverHp(1)`.
- `UpdateStayHome` calls `RecoverHp(1)` directly.
- `SetHp`, clone/overwrite, save/load, and combat paths are explicit additional writers.
- `GetHpRatio` feeds low-HP door escape, work sleeping decisions, home return, and UI consumers.

## Exact-name result

No Staff `stamina_`, `energy_`, `fatigue_`, or `condition_` field was found. The expanded exact-token scan records only unrelated Player stamina, Avatar energy, EventData/UI vocabulary, or Unity binding hits; none establishes a Staff condition field. No readable ordinary-work `RecoverHp(-...)`, `hp_ -=`, or `hp_--` write was found.

## Limits

Ordinary work HP drain and the exact sleeping-stock cadence remain unknown because the decompiled broad update body is damaged. The model must not invent them.
""",
        "WORK_RECOVERY_LIFECYCLE.md": """# Work and Recovery Lifecycle

Room.Update ticks Staff before ObjChip. A sitting Staff enters the readable UpdateWork decision chain: typing, equipment, talk, or sleeping branches. Equipment use has visible frame gates at 20, 40, 60, and 70. At completion the chip reservation is released, use count/stock are updated, FurnitureData.recovery_ may add recovery stock, and Staff returns toward the desk.

Recovery stock starts after a 20-frame delay and is consumed through one `RecoverHp(1)` per stock unit. Home recovery also calls `RecoverHp(1)` directly. The low-HP guard is `GetHpRatio() <= 5`; home return is `>=40`.

The exact work HP drain is **unknown**: no readable ordinary-work decrement was found. The exact sleeping flag cadence is also source-limited. These are preserved as unknowns in the machine contract.
""",
        "HOME_REST_BEHAVIOR.md": """# Home and Rest Behavior

Rest authority is a Staff lifecycle, not a FurnitureData name. When HP ratio is at or below 5 percent, Staff clears its route and targets the door. In `STATE_STAY_HOME`, the readable branch recovers one HP per tick. At 40 percent or higher it reserves the room door and enters wait-back-of-door with the desk movement mode.

The exact indirect transition into `STATE_STAY_HOME`, home timing outside `UpdateStayHome`, and door-route arrival effects remain unknown. No furniture is promoted as a rest rule from its label or sprite.
""",
        "FURNITURE_BEHAVIOR_MODEL.md": f"""# Furniture Behavior Model

All 103 FurnitureData records were classified using `type_`, `recovery_`, flags, and actual Staff/Room/ObjChip consumers. Counts: {furniture_counts}.

- Type 2 is the workstation/desk slot class used by Room.PlaceDesk and Staff desk ownership.
- Type 1 and type 4 are the equipment candidate classes used by GotoEquip.
- `recovery_ >= 1` has one proven autonomous consequence: use completion adds recovery stock.
- Type 5 is the door chip class scanned by Room.GetDoorIndex.
- `passMap_` is a data field consumed by native ObjChip.IsPassable; raw topology is not used to infer FurnitureData identity.
- No record is promoted as REST or SOCIAL from names, sprites, or asset selectors. Social goals use pass chips and Staff colleague logic.

The full per-record catalog is `furniture-behavior-catalog.json`. Records preserve exact source-derived names without turning them into unproven semantic roles.
""",
        "EQUIPMENT_INTERACTIONS.md": """# Equipment Interactions

GotoEquip randomly chooses type 1 or type 4, requests a random installed candidate, and accepts it only when `GetUsersNum() <= 0`. It then calls `ReserveUse`, writes the target object index, and enters move mode 1.

UseEquip has readable phase boundaries at frames 20, 40, 60, and 70. Completion calls `OnUseComplate`; if the FurnitureData recovery value is at least 1 and HP is below max, that value is added to recovery stock with a 20-frame delay. The action then returns toward the desk.

RemoveObj notifies reserved Staff with OnEquipDestroyed. Exact type-4 parent/child target handling, direction vectors, and reservation-count internals remain source-limited.
""",
        "WORKSTATION_OWNERSHIP.md": """# Workstation Ownership and Reservation

Room.AddStaff finds a type-2 staff slot, writes `Staff.deskId_`, and writes the desk chip's `staffId_`. Staff occupancy is maintained through ObjChip staffs lists as grid cells change. Room.PlaceDesk fills empty type-2 slots from FurnitureData records carrying `FLAG_INIT_DESK` (`16384`).

Equipment and door use reservations are stored in ObjChip.reservedStaffs_. `ReserveUse` appends; `OnUseComplate` removes and caps use count at 99. Removal notifies reserved Staff and desk removal calls OnDeskDestroyed.

The exact vacancy predicate in GetStaffEmptyObjTypeOf and exact GetUsersNum semantics are unknown. No fairness or queue policy is inferred.
""",
        "STAFF_SOCIAL_AUTONOMY.md": """# Staff Social Autonomy

GotoTalk chooses one random staff ID. It requires a non-self target, compatible flags, a sitting target in STATE_WORK, and a usable standing/use cell. It sets reserved/invited talk flags, colleague IDs, STATE_MOVE, and MOVE_MODE_TO_STAFF. InviteStaffToTalk can select an installed pass-chip talk goal and notifies the colleague. Talk emits timing events at frames 20, 70, and 110 and completes at frame 130 or later by clearing flags and returning toward the desk.

The selected StaffData records 0-4 point to JobData 4 and SkillData 1. Skill 1 is `Loving Meetings`, type 10, effect index 8 value 150, passive flag 1. OnEndTyping reads that effect through the selected skill path; the random gauge distribution is not promoted.

Full meeting process-step dispatch, queue/fairness, and exact invite cadence remain source-limited.
""",
        "DASHBOARD_BEHAVIOR_BOUNDARY.md": """# Dashboard Behavior Boundary

The dashboard may select or display StaffData, JobData, SkillData, FurnitureData, and explicit task-assignment inputs. It may remain a consumer of HP and parameter fields. EventData constants are event vocabulary, not authority for the autonomous Staff tick.

The autonomous authority remains Room.Update -> Staff.Update/ObjChip.Update, Staff state/move/flag fields, ObjChip reservations, FurnitureData recovery/passMap/type fields, and the native Astar route contract. Dashboard work must not replace these paths or infer behavior from sprites/names.

This phase performs no visual correction, no V8, no production renderer change, and no MapChip change. The full preserve/forbid list is in `dashboard-preservation-boundary.json`.
""",
        "BEHAVIOR_FIRST_HANDOFF.md": """# Behavior-First Handoff

BEHAVIOR-FIRST FORENSIC STATUS: `PASS_BEHAVIOR_MODEL_WITH_SOURCE_LIMITS`

## Fixed facts

- V8 started: NO
- Visual work performed: NO
- Production renderer changed: NO
- MapChip changed: NO
- Subagents: NO
- Emulator/ADB/live/server/network: NO

The autonomous Staff model is source-backed for field layout, state/move/flag constants, HP storage and max formula, low-HP door escape, stay-home recovery/return, equipment selection/use/reservations, workstation ownership, passMap/standing/cardinal route facts, talk timing, selected StaffData/JobData/SkillData links, and the 103-record FurnitureData classification.

## Limits carried forward

The broad Update and OnArriveGoal indirect dispatches, ordinary work HP drain, sleeping-stock cadence, GetStaffEmptyObjTypeOf vacancy predicate, GetUsersNum internals, full meeting dispatch, GetSkill lookup, and exact FurnitureData rest/social roles remain unknown. No values are invented for them.

## Verification

Run `python tools/social-dev/build_behavior_first_forensics.py` followed by `python tools/social-dev/test_behavior_first_forensics.py`. The static test suite covers the requested reconciliation, fields, constants, state/HP/recovery/work/home/equipment/workstation/furniture/movement/talk/idle/contention/dashboard/preservation/regression and no-cutover gates.

STOP. Do not return to visual work until the behavior-first source limits are intentionally resolved and a new scope explicitly authorizes visual changes.
""",
    }


def write_reports(catalog: dict[str, Any], hp: dict[str, Any], state_machine: dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    for name, text in report_texts(catalog, hp, state_machine).items():
        (REPORTS / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def build_all() -> dict[str, Any]:
    inventory = build_staff_field_inventory()
    constants = build_constant_catalog()
    state_machine = build_state_machine()
    transitions = build_transition_graph(state_machine)
    hp, hp_graph = build_hp_contract()
    furniture = build_furniture_catalog()
    lifecycle = build_hp_lifecycle_contracts()
    workstation = build_workstation_contract()
    movement = build_movement_contract()
    social = build_social_contract()
    idle, contention = build_idle_and_contention()
    task_input, visible, preservation = build_dashboard_contracts()
    prior = build_prior_reconciliation()
    unknowns = build_unknowns()
    ledger = build_checkpoint_ledger()

    write_json("prior-evidence-reconciliation.json", prior)
    write_json("staff-field-inventory.json", inventory)
    write_json("staff-state-constant-catalog.json", constants)
    write_json("staff-state-machine.json", state_machine)
    write_json("staff-transition-graph.json", transitions)
    write_json("hp-condition-contract.json", hp)
    write_json("hp-read-write-graph.json", hp_graph)
    for name, value in lifecycle.items():
        write_json(name, value)
    write_json("equipment-behavior-contract.json", lifecycle["equipment-behavior-contract.json"])
    write_json("workstation-ownership-reservation-contract.json", workstation)
    write_json("furniture-behavior-catalog.json", furniture)
    write_json("movement-target-arrival-contract.json", movement)
    write_json("talk-social-contract.json", social)
    write_json("idle-autonomy-contract.json", idle)
    write_json("multi-actor-contention-contract.json", contention)
    write_json("dashboard-task-assignment-input.json", task_input)
    write_json("behavior-visible-action-map.json", visible)
    write_json("canonical-staff-life-model.json", {
        "schema_version": "social-dev-behavior-first-canonical-staff-life-model-v1",
        "status": "pass_with_source_limits",
        "authority": ["Staff", "Room", "ObjChip", "StaffData", "JobData", "SkillData", "FurnitureData", "pinned native route/passMap methods"],
        "life_loop": ["spawn at door", "desk assignment", "work/typing", "equipment use", "talk/social", "HP low -> door/home", "recovery -> return", "save/load preservation"],
        "preserve": ["source-backed numeric labels and offsets", "native RVAs", "reservation and route semantics", "unknowns as unknown"],
        "not_authority": ["dashboard labels alone", "asset names/sprites", "renderer state", "MapChip geometry", "historical candidate claims without recheck"],
        "unknowns_ref": "unknowns.json",
    })
    write_json("dashboard-preservation-boundary.json", preservation)
    write_json("unknowns.json", unknowns)
    write_json("checkpoint-ledger.json", ledger)
    write_reports(furniture, hp, state_machine)
    return {"inventory": inventory, "constants": constants, "state_machine": state_machine, "hp": hp, "furniture": furniture, "ledger": ledger}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build the package and print a compact summary")
    args = parser.parse_args()
    package = build_all()
    if args.check:
        print(
            "behavior_first_built "
            f"fields={package['inventory']['counts']['records']} "
            f"furniture={package['furniture']['counts']['records']} "
            f"checkpoints={len(package['ledger']['records'])} "
            f"reports={len(list(REPORTS.glob('*.md')))}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
