"""Build the Social Dev Phase 0 system extraction evidence.

This tool only reads structural/evidence catalogs. It does not compile or
execute decompiled C# and it does not create runtime code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "knowledge/fixtures/accepted"
CATALOG_DIR = DEFAULT_OUTPUT / "csharp_update_inventory"

CATALOG_FILES = {
    "types": CATALOG_DIR / "type_catalog.json",
    "fields": CATALOG_DIR / "field_catalog.json",
    "methods": CATALOG_DIR / "method_catalog.json",
    "inventory_manifest": CATALOG_DIR / "inventory_manifest.json",
    "data_schema": DEFAULT_OUTPUT / "data_schema_candidate.json",
    "runtime_schema": DEFAULT_OUTPUT / "runtime_schema_candidate.json",
    "load_contracts": DEFAULT_OUTPUT / "load_contract_candidates.json",
    "field_load": DEFAULT_OUTPUT / "field_load_candidates.json",
    "asset_validation": DEFAULT_OUTPUT / "asset_validation_gate.json",
}

SCHEMA_VERSION = "social-dev-csharp-system-extraction-v1"
ALLOWED_STATUSES = {
    "verified",
    "raw_only",
    "derived",
    "unknown",
    "conflict",
    "quarantine",
}
ALLOWED_SCOPES = {"keep", "adapt", "defer", "cut"}

CORE_KEEP = {
    "Room",
    "MapChip",
    "ObjChip",
    "Staff",
    "Astar",
    "Node",
    "DelayEvent",
}
ADAPT_TYPES = {"DataManager", "Main", "AppData", "Player"}
OPTIONAL_TYPES = {"Avatar", "Meeting", "ScheduleData"}
CUT_TYPES = {
    "Company",
    "Develop",
    "Enemy",
    "Fan",
    "FestivalManager",
    "GameRecord",
    "Outsourcing",
    "Proposal",
    "Reinforce",
    "Treasure",
}
FIRST_SLICE_DATA = {
    "RoomData",
    "FurnitureData",
    "StaffData",
    "JobData",
    "SkillData",
    "TalkData",
    "EventData",
    "AvatarEventData",
    "AvatarTalkData",
    "EventMessageData",
    "TodayEventData",
    "ScheduleData",
}
VISIBLE_EVENT_TYPES = {
    "DelayEvent",
    "EventData",
    "AvatarEventData",
    "TalkData",
    "AvatarTalkData",
    "EventMessageData",
    "TodayEventData",
}
MANAGEMENT_DATA_HINTS = {
    "AwardData",
    "CompanyData",
    "ContentMatchListData",
    "DownloadEventData",
    "EnemySkillData",
    "FavoriteData",
    "FestivalData",
    "GameDexData",
    "HardwareData",
    "HelperData",
    "HistoryData",
    "IdeaData",
    "Install",
    "ItemData",
    "LoginBonusData",
    "MailData",
    "MailWordData",
    "ManagementData",
    "ManagementEventData",
    "MethodMatchListData",
    "NewsData",
    "PlatformContentData",
    "PlatformData",
    "PrizeData",
    "ProfileData",
    "ReleaseEventData",
    "RouletteData",
    "SaleTaskData",
    "TrophyData",
}

SYSTEM_SPECS = [
    {
        "id": "data_registry",
        "name": "Data registry and catalog input",
        "role": "data_source",
        "scope": "adapt",
        "phase": "P0",
        "types": ["DataManager"],
        "include_data_types": True,
        "required_for_display_slice": True,
        "reason": "The browser needs normalized records, but the original singleton/loader body is not portable.",
        "evidence_basis": ["typed DataManager registry", "data schema candidate", "load contract candidate"],
    },
    {
        "id": "bootstrap_world",
        "name": "Bootstrap, world ownership and clock boundary",
        "role": "state_owner_boundary",
        "scope": "adapt",
        "phase": "P0",
        "types": ["Main", "AppData", "Player"],
        "required_for_display_slice": True,
        "reason": "Split lifecycle, world ownership, time and presentation effects instead of porting god objects.",
        "evidence_basis": ["application lifecycle", "Player room/staff/time fields", "AppData facade fields"],
    },
    {
        "id": "scene_room",
        "name": "Scene, room, map and camera",
        "role": "scene_state",
        "scope": "keep",
        "phase": "P0",
        "types": ["Room", "RoomData", "MapChip", "Camera"],
        "required_for_display_slice": True,
        "reason": "Defines the visible room grid, coordinate system, camera and draw/update ordering.",
        "evidence_basis": ["Room fields and lifecycle methods", "RoomData loader", "Camera state methods"],
    },
    {
        "id": "object_occupancy",
        "name": "Object, furniture and occupancy",
        "role": "world_service",
        "scope": "keep",
        "phase": "P0",
        "types": ["ObjChip", "FurnitureData"],
        "required_for_display_slice": True,
        "reason": "ObjChip combines visual object, passability, standing positions and use lifecycle.",
        "evidence_basis": ["ObjChip placement/use methods", "FurnitureData registry/load candidate"],
    },
    {
        "id": "actor_living",
        "name": "Staff actor and living state",
        "role": "actor_state_machine",
        "scope": "keep",
        "phase": "P0",
        "types": ["Staff", "StaffData", "JobData", "SkillData"],
        "required_for_display_slice": True,
        "reason": "Contains visible actor state, movement, work, talk, bubble and animation facts.",
        "evidence_basis": ["Staff state/movement constants", "Staff lifecycle methods", "StaffData/JobData/SkillData"],
    },
    {
        "id": "route_service",
        "name": "Route search and collision",
        "role": "world_service",
        "scope": "keep",
        "phase": "P0",
        "types": ["Astar", "Node"],
        "required_for_display_slice": True,
        "reason": "Provides room-grid neighbors and routes to desk/equipment/staff.",
        "evidence_basis": ["Astar goal flags", "Node fields", "Staff route consumers"],
    },
    {
        "id": "visible_event_text",
        "name": "Visible event, delay and text",
        "role": "event_service",
        "scope": "keep",
        "phase": "P1",
        "types": sorted(VISIBLE_EVENT_TYPES),
        "required_for_display_slice": True,
        "reason": "Only the event/text subset that produces visible talk, bubble, form or notification is needed first.",
        "evidence_basis": ["EventData scripts/terms", "DelayEvent fields", "TalkData speaker/text fields"],
    },
    {
        "id": "schedule_interaction",
        "name": "Schedule and visible interaction",
        "role": "interaction_service",
        "scope": "defer",
        "phase": "P1",
        "types": ["ScheduleData"],
        "required_for_display_slice": False,
        "reason": "Include only when the first living loop requires schedule-driven work behavior.",
        "evidence_basis": ["ScheduleData Start/Update/CheckTerms/DecideResult"],
    },
    {
        "id": "optional_avatar",
        "name": "Avatar interaction",
        "role": "optional_actor",
        "scope": "defer",
        "phase": "P2",
        "types": ["Avatar"],
        "required_for_display_slice": False,
        "reason": "Avatar is not the same entity as office Staff and is only needed for an avatar-visible slice.",
        "evidence_basis": ["Avatar identity/frame/draw/talk methods"],
    },
    {
        "id": "optional_meeting",
        "name": "Meeting sequence",
        "role": "optional_behavior",
        "scope": "defer",
        "phase": "P2",
        "types": ["Meeting"],
        "required_for_display_slice": False,
        "reason": "Defer until the basic office life loop is replayable.",
        "evidence_basis": ["Meeting state/update/draw methods"],
    },
    {
        "id": "management_gameplay",
        "name": "Management and player-facing gameplay",
        "role": "deferred_gameplay",
        "scope": "cut",
        "phase": "P2",
        "types": sorted(CUT_TYPES),
        "required_for_display_slice": False,
        "reason": "Not required to reproduce the visible scene and living loop.",
        "evidence_basis": ["structural inventory only; no display requirement in current target"],
    },
]

SOURCE_SLICES = [
    {
        "id": "data_loading",
        "name": "Data loading and first-slice records",
        "purpose": "Extract typed registry, loader order and row-shape candidates without assigning column semantics.",
        "scope": "adapt",
        "required_for_display_slice": True,
        "types": ["DataManager"] + sorted(FIRST_SLICE_DATA),
        "methods": [
            ("DataManager", "Load"),
            ("RoomData", "Load"),
            ("FurnitureData", "Load"),
            ("StaffData", "Load"),
            ("JobData", "Load"),
            ("SkillData", "Load"),
            ("TalkData", "Load"),
            ("EventData", "Load"),
            ("AvatarEventData", "Load"),
            ("ScheduleData", "Load"),
            ("TodayEventData", "Load"),
        ],
        "fields": [],
        "constants": [],
        "artifact_risk": "DataManager.Load and several decompiled loaders contain IL artifacts; retain reader sequence as candidate only.",
    },
    {
        "id": "bootstrap_clock",
        "name": "Application bootstrap, world ownership and clock",
        "purpose": "Separate browser host lifecycle from world state, time and presentation effects.",
        "scope": "adapt",
        "required_for_display_slice": True,
        "types": ["Main", "AppData", "Player"],
        "methods": [
            ("Main", "OnCreate"),
            ("Main", "OnUpdate"),
            ("Main", "OnDraw"),
            ("Main", "OnSuspend"),
            ("Main", "OnDestroy"),
            ("AppData", "Init"),
            ("AppData", "InitGameData"),
            ("AppData", "NewGame"),
            ("AppData", "LoadGame"),
            ("AppData", "ExeEvent"),
            ("AppData", "UpdatePopup"),
            ("AppData", "UpdateAnnounce"),
            ("Player", "NewGame"),
            ("Player", "UpdateCurrentTime"),
            ("Player", "RealTimeProcess"),
            ("Player", "UpdateRealTimeData"),
            ("Player", "Update"),
            ("Player", "Frame"),
        ],
        "fields": [
            ("AppData", "player_"),
            ("AppData", "MAPCHIP_WIDTH"),
            ("AppData", "MAPCHIP_HEIGHT"),
            ("Player", "dataMan_"),
            ("Player", "rooms_"),
            ("Player", "staffs_"),
            ("Player", "currentTime_"),
            ("Player", "realTime_"),
            ("Player", "frame_"),
        ],
        "constants": [],
        "artifact_risk": "AppData and Player mix save, gameplay and UI; only bounded lifecycle facts are retained.",
    },
    {
        "id": "scene_room",
        "name": "Room scene construction and update order",
        "purpose": "Extract room/grid/map/object/staff ownership and visible update/draw boundaries.",
        "scope": "keep",
        "required_for_display_slice": True,
        "types": ["Room", "RoomData", "MapChip", "Camera"],
        "methods": [
            ("Room", "InitMapChips"),
            ("Room", "InitObjChips"),
            ("Room", "InitStaffs"),
            ("Room", "Update"),
            ("Room", "UpdateFukidashi"),
            ("Room", "UpdatePlanning"),
            ("Room", "Draw"),
            ("Room", "PlaceObj"),
            ("Room", "PlaceDesk"),
            ("Room", "AddStaff"),
            ("Room", "RemoveStaff"),
            ("Room", "GetXbyIndex"),
            ("Room", "GetYbyIndex"),
            ("MapChip", "Init"),
            ("MapChip", "Draw"),
            ("Camera", "Init"),
            ("Camera", "Update"),
            ("Camera", "SetTargetPos"),
        ],
        "fields": [
            ("Room", "roomData_"),
            ("Room", "mapChips_"),
            ("Room", "objChips_"),
            ("Room", "staffs_"),
            ("Room", "objMapWidth_"),
            ("Room", "objMapHeight_"),
            ("Room", "routeNodeArrayId_"),
            ("Room", "width_"),
            ("Room", "height_"),
            ("Camera", "currentFloor_"),
            ("Camera", "targetPos_"),
            ("Camera", "state_"),
        ],
        "constants": [
            ("Room", "MAPCHIP_ARRAY"),
            ("Room", "MAPCHIP_IMAGE_ID_ARRAY"),
            ("Room", "FLOOR_IMAGE_ID_ARRAY"),
        ],
        "artifact_risk": "Room body is heavily decompiled; update ordering is retained as a candidate and must receive a bounded trace.",
    },
    {
        "id": "object_occupancy",
        "name": "Object placement, passability and use lifecycle",
        "purpose": "Extract the non-renderer parts of furniture/object behavior.",
        "scope": "keep",
        "required_for_display_slice": True,
        "types": ["ObjChip", "FurnitureData"],
        "methods": [
            ("ObjChip", "Init"),
            ("ObjChip", "Update"),
            ("ObjChip", "IsPassable"),
            ("ObjChip", "GetStandingPositions"),
            ("ObjChip", "ReserveUse"),
            ("ObjChip", "StartAction"),
            ("ObjChip", "OnUseComplate"),
            ("ObjChip", "AddStaff"),
            ("ObjChip", "RemoveStaff"),
            ("ObjChip", "PlaceObj"),
            ("ObjChip", "RemoveObj"),
            ("ObjChip", "Draw"),
        ],
        "fields": [
            ("ObjChip", "index_"),
            ("ObjChip", "room_"),
            ("ObjChip", "furnitureData_"),
            ("ObjChip", "floor_"),
            ("ObjChip", "type_"),
            ("ObjChip", "direction_"),
            ("ObjChip", "active_"),
            ("ObjChip", "frame_"),
            ("ObjChip", "staffId_"),
            ("ObjChip", "staffs_"),
            ("ObjChip", "useNum_"),
            ("ObjChip", "usePoint_"),
        ],
        "constants": [
            ("ObjChip", "OBJ_TYPE_PASS"),
            ("ObjChip", "OBJ_TYPE_EQUIP"),
            ("ObjChip", "OBJ_TYPE_DESK"),
            ("ObjChip", "DIRECTION_UP"),
            ("ObjChip", "DIRECTION_RIGHT"),
            ("ObjChip", "DIRECTION_DOWN"),
            ("ObjChip", "DIRECTION_LEFT"),
        ],
        "artifact_risk": "Use completion name is preserved exactly as cataloged; semantic completion timing remains a review item.",
    },
    {
        "id": "actor_living",
        "name": "Staff state, movement, work, talk and animation",
        "purpose": "Extract the visible actor state machine and its inputs/outputs.",
        "scope": "keep",
        "required_for_display_slice": True,
        "types": ["Staff", "StaffData", "JobData", "SkillData"],
        "methods": [
            ("Staff", "Init"),
            ("Staff", "Update"),
            ("Staff", "UpdateMove"),
            ("Staff", "UpdateWork"),
            ("Staff", "UpdateMeeting"),
            ("Staff", "SearchRoute"),
            ("Staff", "Move"),
            ("Staff", "OnArriveNextNode"),
            ("Staff", "OnArriveGoal"),
            ("Staff", "ChangeState"),
            ("Staff", "GotoDesk"),
            ("Staff", "GotoEquip"),
            ("Staff", "GotoTalk"),
            ("Staff", "ReserveTalk"),
            ("Staff", "InviteStaffToTalk"),
            ("Staff", "Talk"),
            ("Staff", "OnFinishTalk"),
            ("Staff", "OnStartTyping"),
            ("Staff", "OnEndTyping"),
            ("Staff", "AdvanceSebFrame"),
            ("Staff", "ChangeSeb"),
            ("Staff", "DrawStaff"),
        ],
        "fields": [
            ("Staff", "staffData_"),
            ("Staff", "x_"),
            ("Staff", "y_"),
            ("Staff", "vx_"),
            ("Staff", "vy_"),
            ("Staff", "speed_"),
            ("Staff", "state_"),
            ("Staff", "moveMode_"),
            ("Staff", "route_"),
            ("Staff", "room_"),
            ("Staff", "floor_"),
            ("Staff", "objIndex_"),
            ("Staff", "deskId_"),
            ("Staff", "sebId_"),
            ("Staff", "sebFrame_"),
            ("Staff", "sebFrameInterval_"),
            ("Staff", "typingFrame_"),
            ("Staff", "talkFrame_"),
            ("Staff", "fukidashi_"),
        ],
        "constants": [
            ("Staff", "STATE_NORMAL"),
            ("Staff", "STATE_MOVE"),
            ("Staff", "STATE_SIT_DOWN"),
            ("Staff", "STATE_WORK"),
            ("Staff", "STATE_USE_EQUIPMENT"),
            ("Staff", "STATE_TALK"),
            ("Staff", "STATE_WAIT"),
            ("Staff", "STATE_WANDER"),
            ("Staff", "MOVE_MODE_STAY"),
            ("Staff", "MOVE_MODE_GOTO_EQUIPMENT"),
            ("Staff", "MOVE_MODE_GOTO_DESK"),
            ("Staff", "MOVE_MODE_SIT_DOWN"),
            ("Staff", "MOVE_MODE_TO_STAFF"),
            ("Staff", "MOVE_MODE_TO_STAND_TALKING"),
            ("Staff", "MOVE_MODE_GO_TO_DOOR"),
            ("Staff", "MOVE_MODE_GO_HOME"),
            ("Staff", "MOVE_MODE_WANDER"),
        ],
        "artifact_risk": "Staff.Update and movement bodies contain decompiler artifacts; state names/constants and method boundaries are evidence, not a direct implementation.",
    },
    {
        "id": "route_service",
        "name": "Astar grid and route search",
        "purpose": "Extract grid/node/goal contracts for a fresh bounded route implementation.",
        "scope": "keep",
        "required_for_display_slice": True,
        "types": ["Astar", "Node", "Room"],
        "methods": [
            ("Astar", "AddNodeArray"),
            ("Astar", "ConnectNeighbors"),
            ("Astar", "SearchRoute"),
            ("Astar", "GetNode"),
            ("Astar", "RemoveNodeArray"),
            ("Node", "CalculateCost"),
            ("Node", "SetPosition"),
        ],
        "fields": [
            ("Astar", "nodes_"),
            ("Astar", "openList_"),
            ("Astar", "closeList_"),
            ("Astar", "current_"),
            ("Astar", "NODE_DIRECTIONS"),
            ("Node", "position_"),
            ("Room", "objMapWidth_"),
            ("Room", "objMapHeight_"),
        ],
        "constants": [
            ("Astar", "FLAG_GOAL_IS_DESK"),
            ("Astar", "FLAG_GOAL_IS_EQUIP"),
            ("Astar", "FLAG_GOAL_IS_STAFF"),
        ],
        "artifact_risk": "Implement a new bounded Astar from grid/goal facts and fixtures; do not port the damaged body.",
    },
    {
        "id": "visible_event_text",
        "name": "Visible event, delay and text",
        "purpose": "Extract only the event/text subset that produces visible talks, bubbles, forms or notifications.",
        "scope": "keep",
        "required_for_display_slice": True,
        "types": sorted(VISIBLE_EVENT_TYPES),
        "methods": [
            ("DelayEvent", "Serialize"),
            ("EventData", "Load"),
            ("EventData", "NewGame"),
            ("EventData", "ExeAutoEvent"),
            ("EventData", "StartEvent"),
            ("EventData", "ExeEvent"),
            ("AvatarEventData", "Load"),
            ("AvatarEventData", "NewGame"),
            ("AvatarEventData", "ExeAutoEvent"),
            ("AvatarEventData", "StartEvent"),
            ("AvatarEventData", "ExeEvent"),
            ("TalkData", "Load"),
            ("TodayEventData", "Load"),
            ("TodayEventData", "CheckTerms"),
        ],
        "fields": [
            ("DelayEvent", "eventID_"),
            ("DelayEvent", "exeLine_"),
            ("DelayEvent", "active_"),
            ("DelayEvent", "delayFrame_"),
            ("DelayEvent", "charType_"),
            ("DelayEvent", "charIndex_"),
            ("DelayEvent", "repParam_"),
            ("DelayEvent", "value_"),
            ("EventData", "oneLimit_"),
            ("EventData", "termScript_"),
            ("EventData", "execScript_"),
            ("EventData", "exeNum_"),
            ("AvatarEventData", "limitTimes_"),
            ("AvatarEventData", "termScript_"),
            ("AvatarEventData", "execScript_"),
            ("AvatarEventData", "exeNum_"),
            ("TalkData", "charIndex_"),
            ("TalkData", "strDat_"),
            ("TodayEventData", "name_"),
            ("TodayEventData", "text_"),
            ("TodayEventData", "terms_"),
        ],
        "constants": [
            ("EventData", "SCR_TALK"),
            ("EventData", "SCR_DELAY"),
            ("AvatarEventData", "SCR_TALK"),
            ("AvatarEventData", "SCR_DELAY"),
        ],
        "artifact_risk": "Script opcodes and term meanings remain unknown until bounded event traces are reviewed.",
    },
]

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalise_path(value: str) -> str:
    return value.replace("\\", "/")


def source_ref(record: dict[str, Any], source_kind: str) -> dict[str, Any]:
    source = record.get("source") or {}
    return {
        "source_kind": source_kind,
        "file": normalise_path(str(source.get("file", ""))),
        "line_start": source.get("line_start"),
        "line_end": source.get("line_end"),
        "symbol": record.get("symbol") or record.get("name"),
    }


def dedupe_refs(refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for ref in refs:
        unique[stable_json(ref)] = ref
    return [unique[key] for key in sorted(unique)]


def build_indexes(
    type_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    method_rows: list[dict[str, Any]],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    types: dict[str, list[dict[str, Any]]] = {}
    fields: dict[str, list[dict[str, Any]]] = {}
    methods: dict[str, list[dict[str, Any]]] = {}
    for row in type_rows:
        for key in {str(row.get("name", "")), str(row.get("symbol", ""))}:
            if key:
                types.setdefault(key, []).append(row)
    for row in field_rows:
        owner = str(row.get("owner", ""))
        if owner:
            fields.setdefault(owner, []).append(row)
    for row in method_rows:
        owner = str(row.get("owner", ""))
        if owner:
            methods.setdefault(owner, []).append(row)
    return types, fields, methods


def first_type_ref(
    name: str,
    type_index: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    rows = type_index.get(name, [])
    if not rows:
        return None, []
    row = sorted(rows, key=lambda item: (str(item.get("source", {}).get("file", "")), int(item.get("source", {}).get("line_start") or 0)))[0]
    return row, [source_ref(row, "csharp_update_inventory")]


def method_refs(
    owner: str,
    name: str,
    method_index: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows = [row for row in method_index.get(owner, []) if row.get("name") == name]
    return [
        source_ref(row, "csharp_update_inventory")
        for row in sorted(rows, key=lambda item: int(item.get("source", {}).get("line_start") or 0))
    ]


def field_refs(
    owner: str,
    name: str,
    field_index: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows = [row for row in field_index.get(owner, []) if row.get("name") == name]
    return [
        source_ref(row, "csharp_update_inventory")
        for row in sorted(rows, key=lambda item: int(item.get("source", {}).get("line_start") or 0))
    ]


def classify_type(name: str, data_types: set[str]) -> tuple[str, str]:
    if name in ADAPT_TYPES:
        return "adapt", "god-object or application-boundary responsibilities must be split"
    if name in CORE_KEEP:
        return "keep", "directly drives the visible scene or living loop"
    if name in FIRST_SLICE_DATA:
        return "keep", "first display slice data dependency"
    if name in OPTIONAL_TYPES:
        return "defer", "optional visible feature after first living loop"
    if name in CUT_TYPES:
        return "cut", "management/gameplay outside the display/living target"
    if name in VISIBLE_EVENT_TYPES:
        return "keep", "visible event/text dependency"
    if name in data_types:
        if name in MANAGEMENT_DATA_HINTS:
            return "defer", "data registry member not required by first display slice"
        return "defer", "data record requires slice-specific review"
    if name.endswith("Manager") or name.endswith("Record") or name.endswith("Type"):
        return "defer", "supporting or nested type outside the first slice"
    return "defer", "not yet assigned to a first-slice system; review required"


def make_input_manifest(root: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for label, path in CATALOG_FILES.items():
        if not path.is_file():
            raise FileNotFoundError(str(path))
        payload = load_json(path)
        records = payload.get("records")
        record_count = len(records) if isinstance(records, list) else None
        files.append(
            {
                "label": label,
                "path": normalise_path(str(path.relative_to(root))),
                "sha256": sha256_file(path),
                "schema_version": payload.get("schema_version"),
                "content_fingerprint": payload.get("content_fingerprint")
                or payload.get("source_inventory_fingerprint")
                or payload.get("source_schema_fingerprint"),
                "record_count": record_count,
            }
        )
    input_hash = hashlib.sha256(stable_json(files).encode("utf-8")).hexdigest()
    return {"files": files, "input_hash": input_hash}


def build_type_rollup(
    type_rows: list[dict[str, Any]],
    field_index: dict[str, list[dict[str, Any]]],
    method_index: dict[str, list[dict[str, Any]]],
    data_types: set[str],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in sorted(type_rows, key=lambda item: str(item.get("name", ""))):
        name = str(row.get("name", ""))
        scope, reason = classify_type(name, data_types)
        fields = field_index.get(name, [])
        methods = method_index.get(name, [])
        output.append(
            {
                "type": name,
                "symbol": row.get("symbol"),
                "kind": row.get("kind"),
                "scope": scope,
                "scope_status": "derived",
                "scope_reason": reason,
                "semantic_status": "unknown",
                "structural_facts": {
                    "field_count": len(fields),
                    "method_count": len(methods),
                    "source": source_ref(row, "csharp_update_inventory"),
                    "source_hash": row.get("source_hash"),
                    "raw_declaration": row.get("raw_declaration"),
                },
            }
        )
    return output


def system_refs(
    names: list[str],
    type_index: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[str]]:
    refs: list[dict[str, Any]] = []
    missing: list[str] = []
    for name in names:
        row, row_refs = first_type_ref(name, type_index)
        refs.extend(row_refs)
        if row is None:
            missing.append(name)
    return dedupe_refs(refs), missing


def build_systems(
    specs: list[dict[str, Any]],
    type_index: dict[str, list[dict[str, Any]]],
    data_types: set[str],
) -> list[dict[str, Any]]:
    systems: list[dict[str, Any]] = []
    for spec in specs:
        names = list(spec["types"])
        if spec.get("include_data_types"):
            names.extend(sorted(data_types))
        names = sorted(set(names))
        refs, missing = system_refs(names, type_index)
        systems.append(
            {
                "id": spec["id"],
                "name": spec["name"],
                "role": spec["role"],
                "scope": spec["scope"],
                "scope_status": "derived",
                "phase": spec["phase"],
                "types": names,
                "type_source_refs": refs,
                "missing_types": missing,
                "required_for_display_slice": bool(spec["required_for_display_slice"]),
                "semantic_status": "unknown",
                "confidence": "medium",
                "reason": spec["reason"],
                "evidence_basis": spec["evidence_basis"],
            }
        )
    return systems


def edge(
    edge_id: str,
    source_system: str,
    target_system: str,
    relation: str,
    owner_method: tuple[str, str],
    type_index: dict[str, list[dict[str, Any]]],
    method_index: dict[str, list[dict[str, Any]]],
    note: str,
) -> dict[str, Any]:
    owner, method = owner_method
    refs = method_refs(owner, method, method_index)
    if not refs:
        _, refs = first_type_ref(owner, type_index)
    return {
        "id": edge_id,
        "from": source_system,
        "to": target_system,
        "relation": relation,
        "status": "candidate",
        "confidence": "medium" if refs else "low",
        "source_refs": dedupe_refs(refs),
        "review_note": note,
    }


def build_dependency_graph(
    type_index: dict[str, list[dict[str, Any]]],
    method_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    edges = [
        edge("data-manager-registry", "data_registry", "scene_room", "typed_registry", ("DataManager", "Load"), type_index, method_index, "DataManager owns typed arrays; record consumers need slice review."),
        edge("main-bootstrap", "bootstrap_world", "data_registry", "bootstrap_load", ("Main", "OnCreate"), type_index, method_index, "Main lifecycle initializes application/data boundary."),
        edge("bootstrap-room-owner", "bootstrap_world", "scene_room", "world_ownership", ("Player", "NewGame"), type_index, method_index, "Player creates/owns room collections in the original boundary."),
        edge("room-map", "scene_room", "scene_room", "map_initialization", ("Room", "InitMapChips"), type_index, method_index, "Room initializes map chips from room data."),
        edge("room-objects", "scene_room", "object_occupancy", "object_initialization", ("Room", "InitObjChips"), type_index, method_index, "Room initializes object chips and placement."),
        edge("room-actors", "scene_room", "actor_living", "actor_initialization", ("Room", "InitStaffs"), type_index, method_index, "Room initializes staff collection."),
        edge("room-route", "scene_room", "route_service", "route_node_registration", ("Astar", "AddNodeArray"), type_index, method_index, "Room/grid dimensions feed the route node array."),
        edge("actor-route", "actor_living", "route_service", "route_search", ("Staff", "SearchRoute"), type_index, method_index, "Staff requests routes to visible goals."),
        edge("actor-object", "actor_living", "object_occupancy", "occupancy_and_action", ("ObjChip", "ReserveUse"), type_index, method_index, "Object use/reservation is part of actor interaction."),
        edge("room-update-actor", "scene_room", "actor_living", "tick_update", ("Room", "Update"), type_index, method_index, "Room update loop contains staff update pass."),
        edge("room-update-object", "scene_room", "object_occupancy", "tick_update", ("Room", "Update"), type_index, method_index, "Room update loop contains object update pass."),
        edge("actor-event", "actor_living", "visible_event_text", "talk_and_bubble", ("Staff", "Talk"), type_index, method_index, "Talk/bubble output is a visible event boundary."),
        edge("event-delay", "visible_event_text", "bootstrap_world", "delayed_dispatch", ("EventData", "ExeEvent"), type_index, method_index, "Event data dispatches visible event actions into the world boundary."),
        edge("camera-scene", "scene_room", "bootstrap_world", "viewport_target", ("Camera", "SetTargetPos"), type_index, method_index, "Camera follows scene/world target state."),
    ]
    return {
        "schema_version": "social-dev-csharp-dependency-graph-v1",
        "status": "candidate",
        "policy": "Edges are bounded candidates with source refs; no edge is an approved runtime API.",
        "nodes": [spec["id"] for spec in SYSTEM_SPECS],
        "edges": edges,
    }


def resolve_items(
    items: list[tuple[str, str]],
    resolver,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    refs: list[dict[str, Any]] = []
    unresolved: list[dict[str, str]] = []
    for owner, name in items:
        found = resolver(owner, name)
        if found:
            refs.extend(found)
        else:
            unresolved.append({"owner": owner, "name": name})
    return dedupe_refs(refs), unresolved


def build_source_slices(
    type_index: dict[str, list[dict[str, Any]]],
    field_index: dict[str, list[dict[str, Any]]],
    method_index: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    slices: list[dict[str, Any]] = []
    for spec in SOURCE_SLICES:
        type_refs, missing_types = system_refs(spec["types"], type_index)
        method_refs_found, missing_methods = resolve_items(
            spec["methods"],
            lambda owner, name: method_refs(owner, name, method_index),
        )
        field_refs_found, missing_fields = resolve_items(
            spec["fields"],
            lambda owner, name: field_refs(owner, name, field_index),
        )
        constant_refs_found, missing_constants = resolve_items(
            spec["constants"],
            lambda owner, name: field_refs(owner, name, field_index),
        )
        slices.append(
            {
                "id": spec["id"],
                "name": spec["name"],
                "purpose": spec["purpose"],
                "scope": spec["scope"],
                "required_for_display_slice": spec["required_for_display_slice"],
                "types": spec["types"],
                "type_source_refs": type_refs,
                "missing_types": missing_types,
                "methods": [{"owner": owner, "name": name} for owner, name in spec["methods"]],
                "method_source_refs": method_refs_found,
                "missing_methods": missing_methods,
                "fields": [{"owner": owner, "name": name} for owner, name in spec["fields"]],
                "field_source_refs": field_refs_found,
                "missing_fields": missing_fields,
                "constants": [{"owner": owner, "name": name} for owner, name in spec["constants"]],
                "constant_source_refs": constant_refs_found,
                "missing_constants": missing_constants,
                "artifact_risk": spec["artifact_risk"],
                "semantic_status": "unknown",
                "confidence": "medium",
            }
        )
    return slices


def build_review_queue(
    data_schema: dict[str, Any],
    runtime_schema: dict[str, Any],
    load_contracts: dict[str, Any],
    field_load: dict[str, Any],
) -> list[dict[str, Any]]:
    load_counts = load_contracts.get("status_counts") or {}
    field_counts = field_load.get("counts") or {}
    return [
        {
            "id": "loader-column-semantic",
            "category": "data_loader",
            "status": "unknown",
            "blocking": True,
            "scope": "keep",
            "evidence_refs": [
                "knowledge/fixtures/accepted/load_contract_candidates.json",
                "knowledge/fixtures/accepted/field_load_candidates.json",
            ],
            "observed": {
                "loader_status_counts": load_counts,
                "field_load_counts": field_counts,
            },
            "action": "Resolve first-slice reader/field mappings using source, table bytes and language evidence; do not promote column order alone.",
        },
        {
            "id": "decompiler-body-repair",
            "category": "control_flow",
            "status": "quarantine",
            "blocking": True,
            "scope": "keep",
            "evidence_refs": [
                "knowledge/fixtures/accepted/candidate_diff.json",
                "knowledge/fixtures/accepted/cleanup_equivalence.json",
            ],
            "observed": {
                "candidate_policy": "marker cleanup is not semantic repair",
                "target_bodies": ["DataManager.Load", "Room.Update", "Staff.Update", "Astar.SearchRoute"],
            },
            "action": "Use bounded source/assembly traces and write fresh implementations from contracts.",
        },
        {
            "id": "player-appdata-split",
            "category": "architecture",
            "status": "derived",
            "blocking": True,
            "scope": "adapt",
            "evidence_refs": [
                "knowledge/fixtures/accepted/runtime_schema_candidate.json",
                "knowledge/fixtures/accepted/csharp_update_inventory/type_catalog.json",
            ],
            "observed": {
                "player_fields": 227,
                "appdata_fields": 1238,
                "rule": "do not port either type wholesale",
            },
            "action": "Assign bounded responsibilities to WorldContext, Clock, EventQueue and PresentationEffects.",
        },
        {
            "id": "asset-selector-promotion",
            "category": "assets",
            "status": "quarantine",
            "blocking": True,
            "scope": "keep",
            "evidence_refs": [
                "knowledge/fixtures/accepted/asset_validation_gate.json",
            ],
            "observed": {
                "selector_promotion": "blocked_selector_unverified",
            },
            "action": "Resolve selector-to-source relationships before promoting assets into runtime catalog.",
        },
        {
            "id": "semantic-state-labels",
            "category": "state_machine",
            "status": "unknown",
            "blocking": True,
            "scope": "keep",
            "evidence_refs": [
                "knowledge/fixtures/accepted/runtime_schema_candidate.json",
                "knowledge/fixtures/accepted/csharp_update_inventory/field_catalog.json",
            ],
            "observed": {
                "rule": "keep numeric constants and source labels; do not invent meanings",
            },
            "action": "Build bounded transition fixtures for idle/move/work/talk and retain unresolved states outside first slice.",
        },
        {
            "id": "first-slice-selection",
            "category": "scope",
            "status": "derived",
            "blocking": False,
            "scope": "keep",
            "evidence_refs": [
                "docs/roadmap/Roadmap_SocialDev_Data_Readiness.md",
                "docs/reports/social-dev_csharp_system_survey.md",
            ],
            "observed": {
                "target": "one room, 3-5 staff, 2-3 objects, one route, idle-move-work-talk",
            },
            "action": "Select concrete room/actor/object IDs after the first data extraction pass.",
        },
    ]


def validate_artifacts(
    type_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    method_rows: list[dict[str, Any]],
    systems: list[dict[str, Any]],
    graph: dict[str, Any],
    slices: list[dict[str, Any]],
    review_queue: list[dict[str, Any]],
    input_manifest: dict[str, Any],
) -> dict[str, Any]:
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

    check("type-catalog-nonempty", bool(type_rows), len(type_rows), ">0", "Structural type catalog loaded.")
    check("field-catalog-nonempty", bool(field_rows), len(field_rows), ">0", "Structural field catalog loaded.")
    check("method-catalog-nonempty", bool(method_rows), len(method_rows), ">0", "Structural method catalog loaded.")
    check("expected-structural-counts", (len(type_rows), len(field_rows), len(method_rows)) == (82, 3430, 1685), [len(type_rows), len(field_rows), len(method_rows)], [82, 3430, 1685], "Known current update inventory boundary.")
    check("system-ids-unique", len({item["id"] for item in systems}) == len(systems), len(systems), "unique", "System IDs must be unique.")
    check("graph-edge-shape", all({"id", "from", "to", "relation", "status", "source_refs", "review_note"} <= set(edge_row) for edge_row in graph["edges"]), len(graph["edges"]), "all edges shaped", "Dependency edges have required fields.")
    check("slice-ids-unique", len({item["id"] for item in slices}) == len(slices), len(slices), "unique", "Source slice IDs must be unique.")
    check("slice-types-resolved", all(not item["missing_types"] for item in slices), {item["id"]: item["missing_types"] for item in slices if item["missing_types"]}, "empty", "Every slice type must exist in the structural catalog.")
    check("review-queue-shaped", all({"id", "category", "status", "blocking", "scope", "evidence_refs", "action"} <= set(item) for item in review_queue), len(review_queue), "all entries shaped", "Review items must be actionable.")
    check("input-hash-present", bool(input_manifest.get("input_hash")), input_manifest.get("input_hash"), "non-empty", "Generated artifacts must identify their input boundary.")
    failed = [item["id"] for item in checks if item["status"] == "fail"]
    return {
        "schema_version": "social-dev-csharp-extraction-validation-v1",
        "status": "pass" if not failed else "fail",
        "structural_status": "pass" if not failed else "fail",
        "semantic_status": "pending_review",
        "failed_checks": failed,
        "checks": checks,
        "blocking_review_items": [item["id"] for item in review_queue if item["blocking"]],
        "counts": {
            "types": len(type_rows),
            "fields": len(field_rows),
            "methods": len(method_rows),
            "systems": len(systems),
            "dependency_edges": len(graph["edges"]),
            "source_slices": len(slices),
            "review_items": len(review_queue),
        },
    }


def build_artifacts(output_dir: Path) -> dict[str, Any]:
    catalogs = {label: load_json(path) for label, path in CATALOG_FILES.items()}
    type_rows = catalogs["types"]["records"]
    field_rows = catalogs["fields"]["records"]
    method_rows = catalogs["methods"]["records"]
    data_schema = catalogs["data_schema"]
    runtime_schema = catalogs["runtime_schema"]
    data_types = {str(row["symbol"]) for row in data_schema.get("data_types", [])}
    type_index, field_index, method_index = build_indexes(type_rows, field_rows, method_rows)
    input_manifest = make_input_manifest(ROOT)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    systems = build_systems(SYSTEM_SPECS, type_index, data_types)
    graph = build_dependency_graph(type_index, method_index)
    slices = build_source_slices(type_index, field_index, method_index)
    review_queue = build_review_queue(
        data_schema,
        runtime_schema,
        catalogs["load_contracts"],
        catalogs["field_load"],
    )
    validation = validate_artifacts(
        type_rows,
        field_rows,
        method_rows,
        systems,
        graph,
        slices,
        review_queue,
        input_manifest,
    )

    inventory = {
        "schema_version": SCHEMA_VERSION,
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": generated_at,
        "input_manifest": input_manifest,
        "counts": {
            "catalog_types": len(type_rows),
            "catalog_fields": len(field_rows),
            "catalog_methods": len(method_rows),
            "data_manager_registry": len(data_schema.get("data_manager_registry", [])),
            "data_types": len(data_types),
            "runtime_entities": len(runtime_schema.get("entities", [])),
        },
        "policy": {
            "source_roots_read_only": True,
            "decompiled_csharp_executable": False,
            "runtime_promotion": "blocked_until_canonical_contract_gate",
            "semantic_default": "unknown",
        },
        "systems": systems,
        "type_rollup": build_type_rollup(type_rows, field_index, method_index, data_types),
    }
    graph["generated_at_utc"] = generated_at
    graph["input_hash"] = input_manifest["input_hash"]
    graph["source_system_inventory"] = "csharp_system_inventory.json"

    source_slices = {
        "schema_version": "social-dev-csharp-source-slice-v1",
        "status": "candidate",
        "semantic_status": "pending_review",
        "generated_at_utc": generated_at,
        "input_hash": input_manifest["input_hash"],
        "slices": slices,
    }
    review = {
        "schema_version": "social-dev-csharp-semantic-review-queue-v1",
        "status": "open",
        "generated_at_utc": generated_at,
        "input_hash": input_manifest["input_hash"],
        "items": review_queue,
    }
    validation["generated_at_utc"] = generated_at
    validation["input_hash"] = input_manifest["input_hash"]

    artifacts = {
        "csharp_system_inventory.json": inventory,
        "csharp_dependency_graph.json": graph,
        "csharp_source_slice_manifest.json": source_slices,
        "csharp_semantic_review_queue.json": review,
        "csharp_extraction_validation.json": validation,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in artifacts.items():
        path = output_dir / name
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    artifacts = build_artifacts(output_dir)
    validation = artifacts["csharp_extraction_validation.json"]
    print(
        "phase0_extraction_complete "
        f"status={validation['status']} "
        f"types={validation['counts']['types']} "
        f"fields={validation['counts']['fields']} "
        f"methods={validation['counts']['methods']} "
        f"systems={validation['counts']['systems']} "
        f"edges={validation['counts']['dependency_edges']} "
        f"slices={validation['counts']['source_slices']} "
        f"review_items={validation['counts']['review_items']}"
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
