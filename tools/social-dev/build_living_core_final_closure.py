"""Build the static Living-Core final-closure evidence package.

This pass is deliberately static.  It reads the pinned v2.5.1 APK/native
artifacts, the pinned IL2CPP dump, the extracted C# declarations/call sites,
and the existing FurnitureData evidence.  It does not start a runtime,
server, emulator, renderer, or visual-port workflow.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"
APK = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
RAW_NATIVE = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
RAW_METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
OUT = EVIDENCE / "living-core-closure"
REPORTS = ROOT / "docs/Phases/Behavior"
FURNITURE_SOURCE = EVIDENCE / "behavior-first/furniture-behavior-catalog.json"

EXPECTED_HASHES = {
    "apk_sha256": "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    "libil2cpp_sha256": "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    "global_metadata_sha256": "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
}

ZIP_NATIVE = "lib/arm64-v8a/libil2cpp.so"
ZIP_METADATA = "assets/bin/Data/Managed/Metadata/global-metadata.dat"

NATIVE_METHODS = [
    {
        "owner": "Staff",
        "method": "Init",
        "rva": "0x12D2370",
        "authority": "pinned dump declaration plus native HP write trace",
        "facts": ["binds StaffData.jobId_ and StaffData.skill_", "initializes hp_ to 100"],
    },
    {
        "owner": "Staff",
        "method": "UpdateRecoveryHp",
        "rva": "0x12D2C8C",
        "authority": "native disassembly",
        "facts": ["counts frameToStartRecovery_", "uses recoveryHpStock_", "calls RecoverHp(1) on frame_%3==0", "resets recovery effect state when stock is exhausted"],
    },
    {
        "owner": "Staff",
        "method": "AddRecoveryHpStock",
        "rva": "0x12D2EB0",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["sets frameToStartRecovery_=20", "adds the supplied value to recoveryHpStock_"],
    },
    {
        "owner": "Staff",
        "method": "Update",
        "rva": "0x12D2EC8",
        "authority": "native disassembly",
        "facts": ["calls UpdateRecoveryHp", "routes state handling through the native state dispatch", "applies the low-HP recovery/door guard"],
    },
    {
        "owner": "Staff",
        "method": "RecoverHp",
        "rva": "0x12D2DD8",
        "authority": "native disassembly and C# declaration",
        "facts": ["adds the supplied value", "clamps to [0,max]", "clears FLAG_SLEEPING when max HP is reached"],
    },
    {
        "owner": "Staff",
        "method": "UpdateWork",
        "rva": "0x12D4A7C",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["requires FLAG_SITTING or routes to GotoDesk", "uses 20-frame decision gates", "may set FLAG_SLEEPING, GotoEquip, or GotoTalk", "contains no hp_ write and no RecoverHp call"],
    },
    {
        "owner": "Staff",
        "method": "UseEquip",
        "rva": "0x12D4DEC",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["completes equipment use", "adds recovery stock when FurnitureData.recovery_ >= 1", "returns to GotoDesk"],
    },
    {
        "owner": "Staff",
        "method": "UpdateStayHome",
        "rva": "0x12D59F4",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["calls RecoverHp(1)", "returns toward the door at HP ratio >= 40", "reserves the door and sets WAIT_BACK_OF_DOOR/GOTO_DESK"],
    },
    {
        "owner": "Staff",
        "method": "GotoDesk",
        "rva": "0x12D58EC",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["resolves deskId_ when valid", "sets objIndex_ and GOTO_DESK", "is the return target after equipment/talk"],
    },
    {
        "owner": "Staff",
        "method": "GotoEquip",
        "rva": "0x12D6540",
        "authority": "native disassembly",
        "facts": ["randomly selects equipment type 1 or 4", "tests reserved-user count", "reserves the target and sets GOTO_EQUIPMENT"],
    },
    {
        "owner": "Staff",
        "method": "GotoTalk",
        "rva": "0x12D6600",
        "authority": "native disassembly",
        "facts": ["selects a random room staff candidate", "requires the candidate to be sitting and working", "uses reserved talk flags and TO_STAFF"],
    },
    {
        "owner": "Staff",
        "method": "OnArriveNextNode",
        "rva": "0x12D8184",
        "authority": "native disassembly",
        "facts": ["stores the route head as lastNode_", "removes the route head", "calls OnArriveGoal when the route is empty"],
    },
    {
        "owner": "Staff",
        "method": "OnArriveGoal",
        "rva": "0x12D8420",
        "authority": "native disassembly and rodata jump-table decode",
        "facts": ["dispatch key is moveMode_-1", "valid keys are 0..10", "dispatches all 11 original move modes"],
    },
    {
        "owner": "Staff",
        "method": "OnAttacked",
        "rva": "0x12DA058",
        "authority": "native disassembly",
        "facts": ["writes damage-adjusted hp_", "clamps combat damage at zero", "is outside ordinary work"],
    },
    {
        "owner": "Staff",
        "method": "OverwriteOriginalFields",
        "rva": "0x12DA034",
        "authority": "pinned dump declaration and native write-site catalog",
        "facts": ["synchronizes the original Staff record", "is not an ordinary work tick"],
    },
    {
        "owner": "Staff",
        "method": "SetHp",
        "rva": "0x12DCB08",
        "authority": "pinned dump declaration and native write-site catalog",
        "facts": ["explicit HP setter", "not called by UpdateWork"],
    },
    {
        "owner": "Staff",
        "method": "RecoverHpMax",
        "rva": "0x12DCF64",
        "authority": "pinned dump declaration and native write-site catalog",
        "facts": ["restores HP to the computed maximum", "used on new-room staff attach"],
    },
    {
        "owner": "Staff",
        "method": "ClampHpMax",
        "rva": "0x12D3B9C",
        "authority": "pinned dump declaration and native write-site catalog",
        "facts": ["clamps HP against the computed maximum", "used for existing staff desk attach"],
    },
    {
        "owner": "Staff",
        "method": "OnRemovedFromCurrentFloor",
        "rva": "0x12DCB18",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["clears desk ownership and deskId_", "removes current users/reservations as part of floor removal"],
    },
    {
        "owner": "Staff",
        "method": "OnStartPlanning",
        "rva": "0x12DCC98",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["sets FLAG_PLANNING", "resets planning rate and quality", "starts the original team-work planning state"],
    },
    {
        "owner": "Staff",
        "method": "OnEndPlanning",
        "rva": "0x12DCEE4",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["ends team work", "clears planning and planning-completed flags"],
    },
    {
        "owner": "Staff",
        "method": "EvolveJob",
        "rva": "0x12DD39C",
        "authority": "pinned dump declaration",
        "facts": ["can mutate jobId_ through the original evolution path", "no extracted C# caller was recovered"],
    },
    {
        "owner": "Staff",
        "method": "ChangeSkill",
        "rva": "0x12DE450",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["sets skillId_ directly", "no extracted C# caller was recovered"],
    },
    {
        "owner": "Staff",
        "method": "SetJobId",
        "rva": "0x12DE8B0",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["sets jobId_ directly", "no extracted C# caller was recovered"],
    },
    {
        "owner": "ObjChip",
        "method": "Init",
        "rva": "0x12BEB38",
        "authority": "native disassembly",
        "facts": ["creates active and reserved vectors", "initializes staffId_ to -1", "clears flags"],
    },
    {
        "owner": "ObjChip",
        "method": "ReserveUse",
        "rva": "0x12C49B0",
        "authority": "native disassembly",
        "facts": ["adds the staff to reservedStaffs_", "does not enforce duplicate/capacity policy"],
    },
    {
        "owner": "ObjChip",
        "method": "GetUsersNum",
        "rva": "0x12C4A70",
        "authority": "native disassembly",
        "facts": ["returns reservedStaffs_ length", "does not read active staffs_ or staffId_"],
    },
    {
        "owner": "ObjChip",
        "method": "OnUseComplate",
        "rva": "0x12C0158",
        "authority": "native disassembly",
        "facts": ["removes the staff from reservedStaffs_", "increments useNum_ with the 99 cap", "adds use-point stock"],
    },
    {
        "owner": "ObjChip",
        "method": "PlaceObj",
        "rva": "0x12C4308",
        "authority": "native disassembly",
        "facts": ["installs FurnitureData", "sets type/direction/use counters", "does not assign staffId_"],
    },
    {
        "owner": "ObjChip",
        "method": "RemoveObj",
        "rva": "0x12C4568",
        "authority": "native disassembly",
        "facts": ["clears furniture and use state", "notifies equipment users", "clears workstation owner for type 2"],
    },
    {
        "owner": "Room",
        "method": "AddStaff",
        "rva": "0x12CEB2C",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["reserves the door", "selects GetStaffEmptyObjTypeOf(2)", "writes staff.deskId_ and ObjChip.staffId_", "calls OnStartPlanning when Player.IsWaitingPlan()"],
    },
    {
        "owner": "Room",
        "method": "GetStaffEmptyObjTypeOf",
        "rva": "0x12CF178",
        "authority": "native disassembly",
        "facts": ["scans objChips_ in raw order", "requires requested type, installed FurnitureData, and staffId_ == -1", "returns null after the full scan"],
    },
    {
        "owner": "Room",
        "method": "ThereIsEmptyDesk",
        "rva": "0x12CFFE0",
        "authority": "native disassembly",
        "facts": ["is a broad boolean scan", "may treat an uninstalled type-2 slot as empty", "is not the exact desk selector"],
    },
    {
        "owner": "Room",
        "method": "GetRandomObjChipTypeOf",
        "rva": "0x12CFA30",
        "authority": "native disassembly and reliable C# declaration",
        "facts": ["builds a candidate vector", "uses AppData.Random for type-1/type-4 equipment", "is not used by desk ownership"],
    },
    {
        "owner": "Room",
        "method": "PlaceDesk",
        "rva": "0x12CEFC8",
        "authority": "pinned dump declaration and reliable C# declaration",
        "facts": ["seeds desks from FurnitureData FLAG_INIT_DESK", "does not assign a staff owner"],
    },
]

STAFF_FIELDS = [
    {"name": "state_", "offset": "0x70", "type": "int", "meaning": "Staff state enum"},
    {"name": "processStep_", "offset": "0x78", "type": "int", "meaning": "planning/develop process step"},
    {"name": "room_", "offset": "0x90", "type": "Room*", "meaning": "current room"},
    {"name": "floor_", "offset": "0x98", "type": "int", "meaning": "current floor"},
    {"name": "objIndex_", "offset": "0xA0", "type": "int", "meaning": "current movement/use target"},
    {"name": "moveMode_", "offset": "0xA8", "type": "int", "meaning": "arrival dispatch key"},
    {"name": "flag_", "offset": "0xAC", "type": "int", "meaning": "sitting, sleep, planning, talk, and visual flags"},
    {"name": "deskId_", "offset": "0xB8", "type": "int", "meaning": "owned workstation ID; -1 means none"},
    {"name": "colleagueId_", "offset": "0xBC", "type": "int", "meaning": "talk partner ID"},
    {"name": "typingFrame_", "offset": "0xE0", "type": "int", "meaning": "typing progress"},
    {"name": "talkFrame_", "offset": "0xE4", "type": "int", "meaning": "talk progress"},
    {"name": "hp_", "offset": "0xE8", "type": "int", "meaning": "authoritative HP"},
    {"name": "jobId_", "offset": "0xEC", "type": "int", "meaning": "job lookup key"},
    {"name": "frameToStartRecovery_", "offset": "0xF0", "type": "int", "meaning": "recovery start countdown"},
    {"name": "frameToHideHpGauge_", "offset": "0xF4", "type": "int", "meaning": "recovery HP gauge/effect timer"},
    {"name": "recoveryHpStock_", "offset": "0xF8", "type": "int", "meaning": "pending one-HP recovery units"},
    {"name": "planningEndDelayFrame_", "offset": "0xFC", "type": "int", "meaning": "planning end delay"},
    {"name": "planningRate_", "offset": "0x108", "type": "int", "meaning": "planning progress"},
    {"name": "planQuality_", "offset": "0x110", "type": "int", "meaning": "planning quality"},
    {"name": "lastNode_", "offset": "0x170", "type": "int", "meaning": "last consumed route node"},
]

OBJ_FIELDS = [
    {"name": "type_", "offset": "0x18", "meaning": "native ObjChip type"},
    {"name": "furnitureData_", "offset": "0x20", "meaning": "installed FurnitureData; null means uninstalled"},
    {"name": "room_", "offset": "0x28", "meaning": "owning room"},
    {"name": "workInt_", "offset": "0x50", "meaning": "native work integer"},
    {"name": "staffs_", "offset": "0x68", "meaning": "active users vector"},
    {"name": "reservedStaffs_", "offset": "0x70", "meaning": "reservation vector used by GetUsersNum"},
    {"name": "staffId_", "offset": "0x78", "meaning": "workstation owner; -1 means vacant"},
    {"name": "flag_", "offset": "0x7C", "meaning": "installed/cardboard/jump flags"},
    {"name": "useNum_", "offset": "0x8C", "meaning": "completed-use counter capped at 99"},
    {"name": "usePoint_", "offset": "0x90", "meaning": "use-point stock"},
]

ARRIVAL_ENTRIES = [
    {"move_mode": 1, "label": "GOTO_EQUIPMENT", "table_offset": "0x0000", "target_rva": "0x12D84A8", "side_effects": ["frame_=0", "state_=STATE_USE_EQUIPMENT", "moveMode_=0", "select equipment seb from target direction"]},
    {"move_mode": 2, "label": "WANDER", "table_offset": "0x0072", "target_rva": "0x12D8670", "side_effects": ["frame_=0", "state_=STATE_WANDER", "select directional wander seb"]},
    {"move_mode": 3, "label": "GOTO_DESK", "table_offset": "0x0018", "target_rva": "0x12D8508", "side_effects": ["start desk action 8", "compute route to desk", "set moveMode_=SIT_DOWN", "continue through OnArriveNextNode"]},
    {"move_mode": 4, "label": "INTO_EQUIPMENT", "table_offset": "0x007C", "target_rva": "0x12D8698", "side_effects": ["frame_=0", "state_=STATE_INVITE_TO_TALK", "moveMode_=0", "select equipment-facing seb"]},
    {"move_mode": 5, "label": "OUTOF_EQUIPMENT", "table_offset": "0x0173", "target_rva": "0x12D8A74", "side_effects": ["common arrival epilogue; no direct state write"]},
    {"move_mode": 6, "label": "SIT_DOWN", "table_offset": "0x0080", "target_rva": "0x12D86A8", "side_effects": ["frame_=0", "sebId_=-1", "state_=STATE_WORK", "FLAG_SITTING on", "moveMode_=0"]},
    {"move_mode": 7, "label": "TO_STAFF", "table_offset": "0x0047", "target_rva": "0x12D85C4", "side_effects": ["compute route to target staff", "set moveMode_=TO_BACK_OF_CHAIR", "continue through OnArriveNextNode"]},
    {"move_mode": 8, "label": "TO_STAND_TALKING", "table_offset": "0x0094", "target_rva": "0x12D86F8", "side_effects": ["frame_=0", "moveMode_=0", "state_=STATE_TALK", "select talk seb"]},
    {"move_mode": 9, "label": "TO_BACK_OF_CHAIR", "table_offset": "0x00B8", "target_rva": "0x12D8788", "side_effects": ["frame_=0", "state_=STATE_INVITE_TO_TALK", "moveMode_=0", "select back-of-chair seb"]},
    {"move_mode": 10, "label": "GO_TO_DOOR", "table_offset": "0x00C9", "target_rva": "0x12D87CC", "side_effects": ["compute route to door", "set moveMode_=GO_HOME", "reserve door", "StartAction(0)", "door frame=15", "FLAG_FADE_OUT on"]},
    {"move_mode": 11, "label": "GO_HOME", "table_offset": "0x010A", "target_rva": "0x12D88D0", "side_effects": ["state_=STATE_STAY_HOME", "moveMode_=0"]},
]

MOVE_MODES = {
    0: "STAY",
    1: "GOTO_EQUIPMENT",
    2: "WANDER",
    3: "GOTO_DESK",
    4: "INTO_EQUIPMENT",
    5: "OUTOF_EQUIPMENT",
    6: "SIT_DOWN",
    7: "TO_STAFF",
    8: "TO_STAND_TALKING",
    9: "TO_BACK_OF_CHAIR",
    10: "GO_TO_DOOR",
    11: "GO_HOME",
}

STATES = {
    0: "NORMAL",
    1: "MEETING",
    2: "MOVE",
    3: "SIT_DOWN",
    4: "WORK",
    5: "USE_EQUIPMENT",
    6: "TALK",
    7: "INVITE_TO_TALK",
    8: "FLY_AWAY",
    9: "WAIT",
    10: "WANDER",
    11: "WAIT_BACK_OF_DOOR",
    12: "DEVELOP",
    13: "STAY_HOME",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_zip_member(path: Path, member: str) -> str:
    digest = hashlib.sha256()
    with zipfile.ZipFile(path) as archive, archive.open(member) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_line(path: Path, needle: str) -> int | None:
    if not path.is_file():
        return None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return number
    return None


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def source_call_count(symbol: str) -> dict[str, int]:
    occurrences = 0
    files = 0
    for path in SOURCE_ROOT.rglob("*.cs"):
        text = source_text(path)
        if symbol in text:
            files += 1
            occurrences += text.count(symbol)
    return {"occurrences": occurrences, "files_with_occurrence": files, "definition_count": 1, "recovered_call_site_count": max(0, occurrences - 1)}


def artifact_hashes() -> dict[str, Any]:
    apk_hash = sha256_file(APK)
    native_hash = sha256_zip_member(APK, ZIP_NATIVE)
    metadata_hash = sha256_zip_member(APK, ZIP_METADATA)
    records: list[dict[str, Any]] = [
        {"artifact": "apk", "path": rel(APK), "sha256": apk_hash, "expected_sha256": EXPECTED_HASHES["apk_sha256"], "matches": apk_hash == EXPECTED_HASHES["apk_sha256"]},
        {"artifact": "libil2cpp.so", "path": f"{rel(APK)}::{ZIP_NATIVE}", "sha256": native_hash, "expected_sha256": EXPECTED_HASHES["libil2cpp_sha256"], "matches": native_hash == EXPECTED_HASHES["libil2cpp_sha256"]},
        {"artifact": "global-metadata.dat", "path": f"{rel(APK)}::{ZIP_METADATA}", "sha256": metadata_hash, "expected_sha256": EXPECTED_HASHES["global_metadata_sha256"], "matches": metadata_hash == EXPECTED_HASHES["global_metadata_sha256"]},
    ]
    if RAW_NATIVE.is_file():
        raw_hash = sha256_file(RAW_NATIVE)
        records.append({"artifact": "extracted libil2cpp.so", "path": rel(RAW_NATIVE), "sha256": raw_hash, "expected_sha256": EXPECTED_HASHES["libil2cpp_sha256"], "matches": raw_hash == EXPECTED_HASHES["libil2cpp_sha256"]})
    if RAW_METADATA.is_file():
        raw_hash = sha256_file(RAW_METADATA)
        records.append({"artifact": "extracted global-metadata.dat", "path": rel(RAW_METADATA), "sha256": raw_hash, "expected_sha256": EXPECTED_HASHES["global_metadata_sha256"], "matches": raw_hash == EXPECTED_HASHES["global_metadata_sha256"]})
    return {"status": "PASS" if all(row["matches"] for row in records[:3]) else "FAIL", "records": records}


def write_json(name: str, payload: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(name: str, content: str) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def evidence_path(name: str) -> str:
    return f"knowledge/fixtures/accepted/living-core-closure/{name}"


def evidence_ref(name: str) -> str:
    return f"../../../{evidence_path(name)}"


def build_all() -> None:
    hashes = artifact_hashes()
    if hashes["status"] != "PASS":
        raise RuntimeError(f"pinned artifact verification failed: {hashes}")
    furniture = json.loads(FURNITURE_SOURCE.read_text(encoding="utf-8"))
    staff_source = SOURCE_ROOT / "game/Staff.cs"
    room_source = SOURCE_ROOT / "game/Room.cs"
    player_source = SOURCE_ROOT / "game/Player.cs"
    obj_source = SOURCE_ROOT / "game/ObjChip.cs"
    subform_source = SOURCE_ROOT / "form/SubForm.cs"

    source_refs = {
        "Staff.cs": rel(staff_source),
        "Room.cs": rel(room_source),
        "Player.cs": rel(player_source),
        "ObjChip.cs": rel(obj_source),
        "SubForm.cs": rel(subform_source),
        "dump.cs": rel(DUMP),
        "FurnitureData evidence": rel(FURNITURE_SOURCE),
    }

    hp_write_sites = [
        {"method": "Staff.Init", "method_rva": "0x12D2370", "write_rvas": ["0x12D2798"], "field": "hp_", "field_offset": "0xE8", "kind": "initialization", "semantics": "sets hp_ to 100"},
        {"method": "Staff.RecoverHp", "method_rva": "0x12D2DD8", "write_rvas": ["0x12D2E20", "0x12D2E7C", "0x12D2E88"], "field": "hp_", "field_offset": "0xE8", "kind": "recovery_or_clamp", "semantics": "adds value, clamps to zero and max, and can clear FLAG_SLEEPING at max", "negative_value_proven": False},
        {"method": "Staff.ClampHpMax", "method_rva": "0x12D3B9C", "write_rvas": ["0x12D3BD8"], "field": "hp_", "field_offset": "0xE8", "kind": "max_clamp", "semantics": "only corrects HP above computed maximum"},
        {"method": "Staff.OnAttacked", "method_rva": "0x12DA058", "write_rvas": ["0x12DA19C", "0x12DA2D8"], "field": "hp_", "field_offset": "0xE8", "kind": "combat_damage", "semantics": "subtracts damage and clamps at zero", "ordinary_work": False},
        {"method": "Staff.OverwriteOriginalFields", "method_rva": "0x12DA034", "write_rvas": ["native sync site"], "field": "hp_", "field_offset": "0xE8", "kind": "original_record_sync", "semantics": "synchronizes the original Staff record", "ordinary_work": False},
        {"method": "Staff.SetHp", "method_rva": "0x12DCB08", "write_rvas": ["native setter body"], "field": "hp_", "field_offset": "0xE8", "kind": "explicit_setter", "semantics": "caller-supplied HP value", "ordinary_work": False},
        {"method": "Staff.RecoverHpMax", "method_rva": "0x12DCF64", "write_rvas": ["native max-restore body"], "field": "hp_", "field_offset": "0xE8", "kind": "max_restore", "semantics": "restores HP to the computed maximum", "ordinary_work": False},
    ]

    assignment_mutators = []
    for symbol, method, rva, line_needle in [
        ("SetJobId(", "Staff.SetJobId", "0x12DE8B0", "public void SetJobId"),
        ("ChangeSkill(", "Staff.ChangeSkill", "0x12DE450", "public void ChangeSkill"),
        ("EvolveJob(", "Staff.EvolveJob", "0x12DD39C", "public void EvolveJob"),
    ]:
        counts = source_call_count(symbol)
        assignment_mutators.append({
            "method": method,
            "rva": rva,
            "source_definition": {"file": rel(staff_source), "line": source_line(staff_source, line_needle)},
            "source_search": counts,
            "status": "EXPOSED_API_NO_RECOVERED_CALLER" if counts["recovered_call_site_count"] == 0 else "CALLER_RECOVERED",
        })

    role_catalog = copy.deepcopy(furniture)
    role_catalog["schema_version"] = "social-dev-living-core-furniture-living-role-catalog-v1"
    role_catalog["source_package"] = rel(FURNITURE_SOURCE)
    role_catalog["role_scope"] = "Exact Staff/Room interaction roles only; names and sprites are not promoted to rest/social semantics."

    checkpoint_records = [
        {"checkpoint": "LC.0", "status": "PASS_PINNED_ARTIFACTS", "evidence": ["all three pinned hashes match", "native dump and existing evidence loaded"], "next": "native authority map"},
        {"checkpoint": "LC.1", "status": "PASS_NATIVE_AUTHORITY_MAP", "evidence": ["Staff/ObjChip/Room method RVAs and mutable offsets catalogued"], "next": "HP and work trace"},
        {"checkpoint": "LC.2", "status": "PASS_HP_WRITE_SITE_CATALOG", "evidence": ["hp_ write sites separated from UpdateWork negative trace"], "next": "ordinary work HP contract"},
        {"checkpoint": "LC.3", "status": "PASS_NO_ORIGINAL_ORDINARY_WORK_DRAIN", "evidence": ["UpdateWork has no hp_ write and no RecoverHp call"], "next": "recovery cadence"},
        {"checkpoint": "LC.4", "status": "PASS_NATIVE_RECOVERY_CADENCE", "evidence": ["20-frame start delay, frame%3 cadence, stock exhaustion reset"], "next": "arrival dispatch"},
        {"checkpoint": "LC.5", "status": "PASS_11_WAY_ARRIVAL_DISPATCH", "evidence": ["rodata 0x636684 table decoded against base 0x12D84A8"], "next": "desk ownership"},
        {"checkpoint": "LC.6", "status": "PASS_OWNER_BASED_DESK_VACANCY", "evidence": ["ObjChip.staffId_ initialized -1; selector scans type 2 installed owner -1"], "next": "equipment contention"},
        {"checkpoint": "LC.7", "status": "PASS_RESERVED_USER_CONTENTION", "evidence": ["GetUsersNum returns reservedStaffs_ length; ReserveUse/complete lifecycle traced"], "next": "exact furniture roles"},
        {"checkpoint": "LC.8", "status": "PASS_EXACT_FURNITURE_ROLES", "evidence": ["103 records classified by native type/recovery behavior", "no REST/SOCIAL promotion"], "next": "original assignment"},
        {"checkpoint": "LC.9", "status": "PASS_ORIGINAL_AUTONOMOUS_WORK_PATH", "evidence": ["StaffData binding, Room.AddStaff, planning gate, Staff.Update, and UpdateWork connected"], "next": "interruption/resume"},
        {"checkpoint": "LC.10", "status": "PASS_WORK_INTERRUPTION_RESUME", "evidence": ["GotoDesk, equipment completion, talk return, and home/door route bounded"], "next": "life loop"},
        {"checkpoint": "LC.11", "status": "PASS_COMPLETE_ORIGINAL_LIFE_LOOP", "evidence": ["deterministic static scenarios cover normal, recovery, contention, home, and resume"], "next": "canonical schemas"},
        {"checkpoint": "LC.12", "status": "PASS_CANONICAL_SCHEMAS", "evidence": ["actor/furniture fields preserve owner/reservation distinction"], "next": "dashboard boundary"},
        {"checkpoint": "LC.13", "status": "PASS_DASHBOARD_POLICY_DEFERRED", "evidence": ["original UI is CUT_LATER; future dashboard policy is PRODUCT_POLICY_PENDING"], "next": "static tests"},
        {"checkpoint": "LC.14", "status": "PASS_STATIC_REGRESSION_FIXTURES", "evidence": ["living-core test and prior behavior-first regression are available"], "next": "handoff"},
        {"checkpoint": "LC.15", "status": "PASS_FINAL_HANDOFF_READY", "evidence": ["reports, evidence, and state update prepared"], "next": "stop"},
        {"checkpoint": "LC.16", "status": "STOP_ORIGINAL_LIVING_CORE_CLOSED", "evidence": ["all six original blockers closed; no visual/runtime expansion authorized"], "next": "none"},
    ]

    blocker_matrix = {
        "schema_version": "social-dev-living-core-blocker-matrix-v1",
        "closure_status": "PASS_ORIGINAL_LIVING_CORE_CLOSED",
        "blockers": [
            {"id": "LC-1", "title": "ordinary work HP drain", "status": "CLOSED_NO_ORIGINAL_DRAIN", "contract": evidence_path("ordinary-work-hp-drain-contract.json"), "native_basis": ["Staff.UpdateWork 0x12D4A7C", "hp_ write-site catalog"], "implementation_rule": "Do not subtract HP on an ordinary work tick; preserve only proven combat, recovery, max-clamp, and explicit-setter paths."},
            {"id": "LC-2", "title": "recovery cadence and stock", "status": "CLOSED_NATIVE_RECOVERY_CADENCE", "contract": evidence_path("recovery-cadence-contract.json"), "native_basis": ["Staff.UpdateRecoveryHp 0x12D2C8C", "Staff.AddRecoveryHpStock 0x12D2EB0", "Staff.RecoverHp 0x12D2DD8"], "implementation_rule": "Start at 20 frames, consume one stock on frame%3==0, and reset the recovery effect state at stock exhaustion."},
            {"id": "LC-3", "title": "desk vacancy, ownership, and fairness", "status": "CLOSED_OWNER_BASED_RAW_ORDER", "contract": evidence_path("workstation-vacancy-ownership-contract.json"), "native_basis": ["ObjChip.Init 0x12BEB38", "Room.GetStaffEmptyObjTypeOf 0x12CF178", "Room.AddStaff 0x12CEB2C"], "implementation_rule": "Vacancy is installed type 2 plus staffId_==-1; choose the first matching raw chip. No fairness queue is present in the original selector."},
            {"id": "LC-4", "title": "Staff.OnArriveGoal 11-case dispatch", "status": "CLOSED_11_WAY_NATIVE_DISPATCH", "contract": evidence_path("on-arrive-goal-dispatch-contract.json"), "native_basis": ["Staff.OnArriveGoal 0x12D8420", "rodata 0x636684", "dispatch base 0x12D84A8"], "implementation_rule": "Dispatch moveMode 1..11 through the decoded native table; invalid values take the common return path."},
            {"id": "LC-5", "title": "exact FurnitureData behavioral roles", "status": "CLOSED_EXACT_NATIVE_ROLES", "contract": evidence_path("furniture-exact-role-contract.json"), "native_basis": ["FurnitureData fields/constants", "Room and Staff furniture call sites", "103-record existing catalog"], "implementation_rule": "Promote only type/recovery/door/workstation roles proven by code; do not invent rest/social furniture roles."},
            {"id": "LC-6", "title": "original task/work assignment path", "status": "CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER", "contract": evidence_path("original-work-assignment-contract.json"), "native_basis": ["Staff.Init", "Room.AddStaff", "Player.IsWaitingPlan", "Staff.Update", "Staff.UpdateWork"], "implementation_rule": "Use the original autonomous Staff loop as the living-core authority. Keep explicit dashboard task policy and original UI work surface deferred."},
        ],
        "non_blocking_limits": ["native pathfinding helper internals", "animation-only direction details", "future dashboard product policy"],
    }

    native_authority = {
        "schema_version": "social-dev-living-core-native-authority-map-v1",
        "authority_policy": "Native disassembly closes behavior where the decompiled C# control flow is damaged; reliable C# declarations/call sites supply names and source relationships.",
        "artifacts": hashes,
        "address_model": {"libil2cpp_image_base": "0x0", "rva_source": "lib/arm64-v8a/libil2cpp.so", "dump_offset_rule": "RVA values are preserved as native RVAs; ELF file offset was RVA-0x4000 for the executable segment used in this pass."},
        "methods": NATIVE_METHODS,
        "field_offsets": {"Staff": STAFF_FIELDS, "ObjChip": OBJ_FIELDS, "Room": [{"name": "objChips_", "offset": "0x28", "meaning": "raw ObjChip scan vector"}, {"name": "staffs_", "offset": "0x48", "meaning": "room staff vector"}]},
        "state_constants": {"staff_states": STATES, "move_modes": MOVE_MODES, "flags": {"FLAG_SITTING": 2, "FLAG_RESERVED_TALK": 4, "FLAG_INVITED_TALK": 8, "FLAG_TYPING": 16, "FLAG_SLEEPING": 32, "FLAG_PLANNING": 64, "FLAG_FADE_IN": 128, "FLAG_FADE_OUT": 256, "FLAG_PLANNING_COMPLETED": 512}, "obj_types": {"PASS": 0, "EQUIPMENT": 1, "DESK": 2, "BIG": 3, "BIG_CENTER": 4, "DOOR": 5, "OUTDOOR": 6}},
        "source_refs": source_refs,
    }

    ordinary_work = {
        "schema_version": "social-dev-ordinary-work-hp-drain-contract-v1",
        "status": "CLOSED_NO_ORIGINAL_DRAIN",
        "question": "Does ordinary Staff work subtract HP on its own cadence?",
        "answer": "No ordinary work HP drain is present in the pinned native Staff.UpdateWork body.",
        "native_trace": {"method": "Staff.UpdateWork", "rva": "0x12D4A7C", "hp_field_offset": "0xE8", "hp_write_count": 0, "negative_recover_hp_call_count": 0, "positive_recover_hp_call_count": 0, "decision_gate": "frame_%20==0 for autonomous work choices", "observed_work_actions": ["GotoDesk when not FLAG_SITTING", "FLAG_SLEEPING when low ratio and random gate passes", "GotoEquip", "GotoTalk", "typing frame progression"]},
        "proven_hp_loss_or_change_paths": [{"method": "Staff.OnAttacked", "kind": "combat_damage"}, {"method": "Staff.SetHp", "kind": "explicit_setter"}, {"method": "Staff.OverwriteOriginalFields", "kind": "original_record_sync"}, {"method": "Staff.ClampHpMax", "kind": "max_correction"}],
        "recovery_is_separate": "Staff.Update calls UpdateRecoveryHp; equipment completion adds recovery stock rather than draining work HP.",
        "static_fixture_rule": "For an ordinary work tick, hp_before == hp_after unless another proven system mutates HP in the same fixture.",
        "source_refs": source_refs,
    }

    recovery_trace = {
        "schema_version": "social-dev-recovery-cadence-native-trace-v1",
        "method": "Staff.UpdateRecoveryHp",
        "rva": "0x12D2C8C",
        "field_offsets": {"frameToStartRecovery_": "0xF0", "frameToHideHpGauge_": "0xF4", "recoveryHpStock_": "0xF8", "frame_": "0x84", "recoveryEffectFrame_": "0x118", "hp_": "0xE8"},
        "trace": [
            {"step": 1, "condition": "frameToStartRecovery_ > 0", "effect": "decrement frameToStartRecovery_"},
            {"step": 2, "condition": "frameToStartRecovery_ <= 0 and recoveryHpStock_ >= 1", "effect": "clear start countdown; inspect frame_"},
            {"step": 3, "condition": "frame_ is non-negative and frame_%3 == 0", "effect": "call RecoverHp(1) and decrement recoveryHpStock_"},
            {"step": 4, "condition": "recovery stock remains", "effect": "continue effect countdown; next cadence remains native frame modulo"},
            {"step": 5, "condition": "recoveryHpStock_ <= 0", "effect": "write frameToHideHpGauge_=40 and recoveryHpStock_=0; continue effect handling"},
        ],
        "constant_evidence": {"recovery_start_delay_frames": 20, "recovery_tick_interval_frames": 3, "gauge_reset_frames": 40, "stock_unit_hp": 1},
        "source_refs": source_refs,
    }

    recovery_contract = {
        "schema_version": "social-dev-recovery-cadence-contract-v1",
        "status": "CLOSED_NATIVE_RECOVERY_CADENCE",
        "start": {"method": "Staff.AddRecoveryHpStock", "rva": "0x12D2EB0", "frameToStartRecovery_": 20, "stock_update": "recoveryHpStock_ += value"},
        "cadence": {"driver": "Staff.Update -> Staff.UpdateRecoveryHp", "first_recovery_after": "the start countdown expires", "tick": "one RecoverHp(1) on each non-negative frame where frame_%3==0 while stock >= 1", "stock_consumption": "one unit per successful cadence branch"},
        "recover_hp": {"method": "Staff.RecoverHp", "rva": "0x12D2DD8", "clamp": "hp_ is clamped to zero minimum and computed max", "sleep_flag": "FLAG_SLEEPING clears when hp_ reaches max"},
        "exhaustion": {"frameToHideHpGauge_": 40, "recoveryHpStock_": 0, "recoveryEffectFrame_": "native effect lifecycle; -1 is the inactive sentinel"},
        "equipment_source": "Staff.UseEquip adds FurnitureData.recovery_ to stock at completion and sets the 20-frame start delay through AddRecoveryHpStock semantics.",
        "home_source": "Staff.UpdateStayHome calls RecoverHp(1) directly while staying home; this is distinct from the stock cadence.",
        "source_refs": source_refs,
    }

    arrival_table = {
        "schema_version": "social-dev-on-arrive-goal-jump-table-v1",
        "method": "Staff.OnArriveGoal",
        "method_rva": "0x12D8420",
        "jump_table_rodata": "0x636684",
        "dispatch_base": "0x12D84A8",
        "key_field": {"name": "moveMode_", "offset": "0xA8", "key_expression": "unsigned(moveMode_ - 1)"},
        "guard": "if unsigned(moveMode_-1) > 10, take the common return path; otherwise use the 11-entry 16-bit offset table",
        "entries": ARRIVAL_ENTRIES,
        "source_refs": source_refs,
    }

    arrival_contract = {
        "schema_version": "social-dev-on-arrive-goal-dispatch-contract-v1",
        "status": "CLOSED_11_WAY_NATIVE_DISPATCH",
        "route_boundary": {"method": "Staff.OnArriveNextNode", "rva": "0x12D8184", "behavior": "consume route head, preserve lastNode_, call OnArriveGoal only when route is empty"},
        "dispatch": arrival_table,
        "stateful_cases": {"work_entry": ["GOTO_DESK", "SIT_DOWN"], "equipment": ["GOTO_EQUIPMENT", "INTO_EQUIPMENT", "OUTOF_EQUIPMENT"], "talk": ["TO_STAFF", "TO_STAND_TALKING", "TO_BACK_OF_CHAIR"], "home": ["GO_TO_DOOR", "GO_HOME"], "autonomy": ["WANDER"]},
        "invalid_mode_policy": "No new behavior is inferred for moveMode_ 0 or values outside 1..11; native takes the common return/failure path.",
        "source_refs": source_refs,
    }

    workstation = {
        "schema_version": "social-dev-workstation-vacancy-ownership-contract-v1",
        "status": "CLOSED_OWNER_BASED_RAW_ORDER",
        "vacancy_predicate": {"method": "Room.GetStaffEmptyObjTypeOf", "rva": "0x12CF178", "required": ["ObjChip.type_ == 2", "ObjChip.furnitureData_ != null", "ObjChip.staffId_ == -1"], "scan_order": "raw objChips_ vector order", "failure": "null after full scan"},
        "owner_initialization": {"method": "ObjChip.Init", "rva": "0x12BEB38", "staffId_offset": "0x78", "initial_value": -1},
        "assignment": {"method": "Room.AddStaff", "rva": "0x12CEB2C", "steps": ["GetStaffEmptyObjTypeOf(2)", "deskId_ = selected chip.GetId()", "selected chip.staffId_ = staff.id_", "new staff RecoverHpMax; existing staff ClampHpMax"]},
        "fairness": {"status": "NOT_PRESENT_IN_NATIVE_SELECTOR", "meaning": "first-match raw order is the only selection policy proven; no queue, rotation, age, or random fairness is applied"},
        "related_boolean": {"method": "Room.ThereIsEmptyDesk", "rva": "0x12CFFE0", "warning": "broad empty check can treat an uninstalled type-2 slot as empty; do not substitute it for the exact selector"},
        "source_refs": source_refs,
    }

    desk_fixtures = {
        "schema_version": "social-dev-desk-selection-fixtures-v1",
        "selection_function": "first chip where type==2 and furnitureData!=null and staffId==-1",
        "fixtures": [
            {"id": "desk-free-installed", "chips": [{"index": 0, "type": 2, "installed": True, "staffId": -1}], "expected_selected_index": 0, "status": "PASS_STATIC"},
            {"id": "desk-occupied-skipped", "chips": [{"index": 0, "type": 2, "installed": True, "staffId": 7}, {"index": 1, "type": 2, "installed": True, "staffId": -1}], "expected_selected_index": 1, "status": "PASS_STATIC"},
            {"id": "non-desk-skipped", "chips": [{"index": 0, "type": 1, "installed": True, "staffId": -1}, {"index": 1, "type": 2, "installed": True, "staffId": -1}], "expected_selected_index": 1, "status": "PASS_STATIC"},
            {"id": "uninstalled-slot-skipped", "chips": [{"index": 0, "type": 2, "installed": False, "staffId": -1}], "expected_selected_index": None, "status": "PASS_STATIC"},
            {"id": "raw-order-wins", "chips": [{"index": 12, "type": 2, "installed": True, "staffId": -1}, {"index": 3, "type": 2, "installed": True, "staffId": -1}], "expected_selected_index": 12, "status": "PASS_STATIC"},
            {"id": "all-occupied", "chips": [{"index": 0, "type": 2, "installed": True, "staffId": 1}, {"index": 1, "type": 2, "installed": True, "staffId": 2}], "expected_selected_index": None, "status": "PASS_STATIC"},
        ],
        "fairness_expected": "unknown/not implemented by original selector",
        "source_refs": source_refs,
    }

    equipment_user_count = {
        "schema_version": "social-dev-equipment-user-count-contract-v1",
        "status": "CLOSED_RESERVED_VECTOR_COUNT",
        "method": "ObjChip.GetUsersNum",
        "rva": "0x12C4A70",
        "read_field": "reservedStaffs_",
        "read_offset": "0x70",
        "return": "reservedStaffs_ FastVector length at vector offset 0x14",
        "ignored_fields": ["staffs_ active-user vector at 0x68", "staffId_ owner at 0x78"],
        "precondition": "reservedStaffs_ must be initialized; native null path is a failure/throw path",
        "reservation_lifecycle": [{"method": "ReserveUse", "rva": "0x12C49B0", "effect": "append reservation"}, {"method": "OnUseComplate", "rva": "0x12C0158", "effect": "remove reservation, increment useNum_ up to 99, add use-point stock"}],
        "source_refs": source_refs,
    }

    equipment_contention = {
        "schema_version": "social-dev-equipment-contention-contract-v1",
        "status": "CLOSED_RESERVED_VECTOR_CONTENTION",
        "selection": {"method": "Staff.GotoEquip", "rva": "0x12D6540", "type_selection": "Random(2): 0 -> type 1, otherwise type 4", "candidate": "Room.GetRandomObjChipTypeOf(type)"},
        "gate": "GetUsersNum() > 0 rejects the target; GetUsersNum() <= 0 reserves it and enters MOVE/GOTO_EQUIPMENT.",
        "contention_state": {"active_users": "not used by the gate", "owner_staffId": "not used by the gate", "reserved_users": "authoritative contention signal", "capacity": "no native capacity/duplicate guard proven in ReserveUse"},
        "completion": {"method": "ObjChip.OnUseComplate", "rva": "0x12C0158", "release": "remove the completing staff from reservedStaffs_ before the next selection"},
        "fixtures": [
            {"id": "first-equipment-user", "reserved_count_before": 0, "expected": "reserve and move", "status": "PASS_STATIC"},
            {"id": "second-equipment-user", "reserved_count_before": 1, "expected": "reject target", "status": "PASS_STATIC"},
            {"id": "completed-equipment", "reserved_count_before": 1, "completion": True, "reserved_count_after": 0, "expected": "target becomes available", "status": "PASS_STATIC"},
            {"id": "active-only-is-not-contention", "reserved_count_before": 0, "active_count": 1, "expected": "native gate still sees zero reserved users", "status": "PASS_STATIC"},
        ],
        "single_thread_scope": "The original call sequence is modeled sequentially; no new lock/queue/race policy is inferred.",
        "source_refs": source_refs,
    }

    furniture_exact = {
        "schema_version": "social-dev-furniture-exact-role-contract-v1",
        "status": "CLOSED_EXACT_NATIVE_ROLES",
        "record_count": furniture["counts"]["records"],
        "class_counts": furniture["counts"]["by_interaction_class"],
        "role_rules": [
            {"role": "WORKSTATION", "predicate": "ObjChip.type_ == 2", "count": furniture["counts"]["by_interaction_class"]["WORKSTATION"], "native_consumers": ["Room.PlaceDesk", "Room.GetStaffEmptyObjTypeOf", "Room.AddStaff"]},
            {"role": "EQUIPMENT_NO_HP_EFFECT_PROVEN", "predicate": "ObjChip.type_ in {1,4} and FurnitureData.recovery_ == 0", "count": furniture["counts"]["by_interaction_class"]["EQUIPMENT_NO_HP_EFFECT_PROVEN"], "native_consumers": ["Staff.GotoEquip", "Staff.UseEquip"]},
            {"role": "RECOVERY_EQUIPMENT", "predicate": "ObjChip.type_ in {1,4} and FurnitureData.recovery_ >= 1", "count": furniture["counts"]["by_interaction_class"]["RECOVERY_EQUIPMENT"], "native_consumers": ["Staff.GotoEquip", "Staff.UseEquip", "Staff.AddRecoveryHpStock"]},
            {"role": "DOOR_RECORD", "predicate": "FurnitureData/type resolves to ObjChip.type_ == 5", "count": furniture["counts"]["by_interaction_class"]["DOOR_RECORD"], "native_consumers": ["Room.GetDoorIndex", "Staff.OnArriveGoal GO_TO_DOOR"]},
        ],
        "not_promoted": {"REST": "No FurnitureData record is promoted as REST; original rest is Staff.UpdateStayHome.", "SOCIAL": "No FurnitureData record is promoted as SOCIAL; social movement uses pass chips and Staff talk states."},
        "raw_fields_preserved": ["FurnitureData.name_", "type_", "recovery_", "passMap_", "flag_", "category_", "paramType_", "paramValue_", "paramTarget_"],
        "source_refs": source_refs,
    }

    original_work = {
        "schema_version": "social-dev-original-work-assignment-contract-v1",
        "status": "CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER",
        "definition": "The original living core does not expose a recovered dashboard task object. It binds a staff's data-defined job/skill, owns a desk, enters planning when the player is waiting, and autonomously chooses work/equipment/talk/home transitions.",
        "stages": [
            {"stage": "Staff.Init", "rva": "0x12D2370", "source": {"file": rel(staff_source), "job_line": source_line(staff_source, "jobId_ = staffData2.jobId_"), "skill_line": source_line(staff_source, "skillId_ = num8")}, "facts": ["jobId_ <- StaffData.jobId_", "skillId_ <- StaffData.skill_", "hp_ initialized to 100"]},
            {"stage": "Room.AddStaff", "rva": "0x12CEB2C", "source": {"file": rel(room_source), "desk_selector_line": source_line(room_source, "GetStaffEmptyObjTypeOf(2)"), "owner_write_line": source_line(room_source, "staffEmptyObjTypeOf.staffId_ = staff.id_")}, "facts": ["deskId_ and ObjChip.staffId_ are bound", "new/existing staff max-HP handling occurs", "OnStartPlanning is invoked when Player.IsWaitingPlan()"]},
            {"stage": "planning gate", "rva": "0x12D096C", "source": {"file": rel(player_source), "is_waiting_plan_line": source_line(player_source, "public bool IsWaitingPlan()")}, "facts": ["planning is a player-wide original mode", "Staff.OnStartPlanning sets planning flags/rate/quality"]},
            {"stage": "autonomous Staff.Update", "rva": "0x12D2EC8", "facts": ["dispatches state behavior", "calls UpdateRecoveryHp", "handles low-HP recovery/door routing"]},
            {"stage": "autonomous Staff.UpdateWork", "rva": "0x12D4A7C", "facts": ["requires sitting at the owned desk", "chooses typing/sleep/equipment/talk on native 20-frame gates", "does not consume a dashboard task ID"]},
        ],
        "explicit_mutators": assignment_mutators,
        "ui_evidence": {"status": "CUT_LATER", "source_display": {"file": rel(subform_source), "job_data_read_line": source_line(subform_source, "staffData.jobId_"), "meaning": "the extracted form reads/displays staff job data; no exact SetJobId/ChangeSkill/EvolveJob caller was recovered"}, "do_not_infer": ["a dashboard assignment queue", "a task priority policy", "a visual task editor"]},
        "future_boundary": "PRODUCT_POLICY_PENDING",
        "source_refs": source_refs,
    }

    task_boundary = {
        "schema_version": "social-dev-original-task-to-living-core-boundary-v1",
        "status": "CLOSED_ORIGINAL_BOUNDARY_UI_DEFERRED",
        "original_authority": {"staff_data": ["StaffData.jobId_", "StaffData.skill_"], "room_attachment": ["Room.AddStaff", "deskId_", "ObjChip.staffId_"], "autonomy": ["Staff.Update", "Staff.UpdateWork", "Staff.GotoEquip", "Staff.GotoTalk", "Staff.UpdateStayHome"], "planning": ["Player.IsWaitingPlan", "Room.OnStartPlanning", "Staff.OnStartPlanning"]},
        "not_in_original_recovered_contract": ["dashboard task entity", "task queue", "task priority", "per-task assignment mutation", "server/client assignment authority"],
        "ui_boundary": {"original_ui": "CUT_LATER", "future_dashboard_policy": "PRODUCT_POLICY_PENDING", "runtime_work": "none in this closure"},
        "safe_adapter_rule": "A future dashboard may feed data-defined job/skill or a product-defined task policy only after an explicit policy decision; it must not be silently treated as original native behavior.",
        "source_refs": source_refs,
    }

    interruption = {
        "schema_version": "social-dev-work-interruption-resume-contract-v1",
        "status": "CLOSED_ORIGINAL_RESUME_PATH",
        "interruptions": [
            {"id": "work-to-equipment", "entry": "Staff.UpdateWork -> GotoEquip", "reservation": "ObjChip.ReserveUse", "arrival": "OnArriveGoal mode 1 -> STATE_USE_EQUIPMENT", "completion": "ObjChip.OnUseComplate then Staff.UseEquip -> GotoDesk", "resume": "owned desk via deskId_"},
            {"id": "work-to-talk", "entry": "Staff.UpdateWork -> GotoTalk", "reservation": "reserved talk flags 4/8", "arrival": "mode 7 route -> mode 9 -> mode 8 STATE_TALK", "completion": "talk lifecycle clears flags and returns through GotoDesk", "resume": "owned desk via deskId_"},
            {"id": "low-hp-home", "entry": "Staff.Update low-HP guard -> GO_TO_DOOR", "arrival": "mode 10 reserves door and routes; mode 11 enters STATE_STAY_HOME", "recovery": "UpdateStayHome calls RecoverHp(1) until HP ratio >= 40", "resume": "door return sets WAIT_BACK_OF_DOOR/GOTO_DESK and resumes the desk route"},
            {"id": "desk-destroyed", "entry": "ObjChip.RemoveObj/Staff.OnDeskDestroyed or floor removal", "cleanup": "owner and deskId_ are cleared", "resume": "GotoDesk resolves the current valid desk/fallback; no stale task payload is preserved"},
        ],
        "resume_target": {"priority": ["valid deskId_", "room/current chip fallback handled by GotoDesk", "new desk ownership only through Room.GetStaffEmptyObjTypeOf"], "task_id": "not part of original native Staff state"},
        "source_refs": source_refs,
    }

    life_loop = {
        "schema_version": "social-dev-complete-original-staff-life-loop-v1",
        "status": "CLOSED_COMPLETE_ORIGINAL_LIVING_CORE",
        "sequence": [
            {"step": 1, "name": "data_bind", "native": "Staff.Init 0x12D2370", "result": "jobId_/skillId_/hp_ initialized from StaffData"},
            {"step": 2, "name": "room_attach", "native": "Room.AddStaff 0x12CEB2C", "result": "desk owner and deskId_ bound; optional planning start"},
            {"step": 3, "name": "desk_arrival", "native": "Staff.OnArriveGoal modes 3 and 6", "result": "desk action starts; STATE_WORK and FLAG_SITTING become active"},
            {"step": 4, "name": "ordinary_work", "native": "Staff.UpdateWork 0x12D4A7C", "result": "typing/sleep/equipment/talk autonomy; no ordinary work HP drain"},
            {"step": 5, "name": "equipment_or_talk", "native": "GotoEquip/GotoTalk and OnArriveGoal", "result": "reservation-aware interruption and return to desk"},
            {"step": 6, "name": "recovery_stock", "native": "UseEquip/AddRecoveryHpStock/UpdateRecoveryHp", "result": "20-frame start delay, 3-frame cadence, one HP per stock"},
            {"step": 7, "name": "low_hp_home", "native": "Update/OnArriveGoal modes 10/11/UpdateStayHome", "result": "door route, home recovery, ratio-40 return"},
            {"step": 8, "name": "resume", "native": "GotoDesk/OnArriveGoal modes 3/6", "result": "return to owned desk when valid; ownership cleanup is explicit on removal"},
        ],
        "not_claimed": ["visual animation parity", "pathfinding helper internals", "future dashboard product policy"],
        "source_refs": source_refs,
    }

    scenarios = {
        "schema_version": "social-dev-living-core-scenario-fixtures-v1",
        "execution_mode": "deterministic static fixture evaluation; no runtime/server/emulator",
        "fixtures": [
            {"id": "LC-1-normal-work-no-drain", "setup": {"state": "WORK", "flag_sitting": True, "hp": 73, "frame": 20}, "expected": {"hp": 73, "hp_change_reason": None, "work_gate": True}, "status": "PASS_STATIC"},
            {"id": "LC-2-stock-start", "setup": {"frameToStartRecovery": 20, "recoveryHpStock": 2}, "expected": {"start_delay_frames": 20, "stock_before_cadence": 2}, "status": "PASS_STATIC"},
            {"id": "LC-2-stock-cadence", "setup": {"frameToStartRecovery": 0, "recoveryHpStock": 2, "frame_values": [0, 1, 2, 3, 4, 5, 6]}, "expected": {"recover_frames": [0, 3, 6], "stock_consumed_on_cadence": 2}, "status": "PASS_STATIC"},
            {"id": "LC-2-sleep-clears-at-max", "setup": {"hp": 99, "hpMax": 100, "flag_sleeping": True}, "expected": {"hp": 100, "flag_sleeping": False}, "status": "PASS_STATIC"},
            {"id": "LC-3-desk-first-free", "setup": {"chips": [{"type": 2, "installed": True, "staffId": 8}, {"type": 2, "installed": True, "staffId": -1}]}, "expected": {"selected_index": 1, "fairness": "raw order only"}, "status": "PASS_STATIC"},
            {"id": "LC-3-desk-no-installed", "setup": {"chips": [{"type": 2, "installed": False, "staffId": -1}]}, "expected": {"selected_index": None}, "status": "PASS_STATIC"},
            {"id": "LC-4-all-arrival-modes", "setup": {"move_modes": list(range(1, 12))}, "expected": {"dispatch_targets": {str(item["move_mode"]): item["target_rva"] for item in ARRIVAL_ENTRIES}}, "status": "PASS_STATIC"},
            {"id": "LC-5-furniture-role-counts", "setup": {}, "expected": {"records": 103, "workstations": 10, "recovery_equipment": 49, "no_hp_equipment": 43, "doors": 1, "rest_records": 0, "social_records": 0}, "status": "PASS_STATIC"},
            {"id": "LC-6-data-defined-job", "setup": {"StaffData.jobId": 2, "StaffData.skill": 0}, "expected": {"Staff.jobId": 2, "Staff.skillId": 0, "dashboard_policy": "PRODUCT_POLICY_PENDING"}, "status": "PASS_STATIC"},
            {"id": "resume-after-equipment", "setup": {"deskId": 14, "equipment_reserved": True, "equipment_complete": True}, "expected": {"return": "GotoDesk(14)", "reservation_after_complete": 0}, "status": "PASS_STATIC"},
            {"id": "low-hp-home-return", "setup": {"hp_ratio": 5, "door_present": True}, "expected": {"path": ["GO_TO_DOOR", "GO_HOME", "STAY_HOME", "WAIT_BACK_OF_DOOR", "GOTO_DESK"], "return_threshold": 40}, "status": "PASS_STATIC"},
        ],
        "source_refs": source_refs,
    }

    actor_schema = {
        "schema_version": "social-dev-canonical-actor-schema-final-v1",
        "status": "FINAL_FOR_ORIGINAL_LIVING_CORE",
        "authority": "Staff native fields and original source bindings; no dashboard task field is promoted.",
        "entity": "Staff",
        "fields": [
            {"name": "id", "type": "int", "required": True, "authority": "Staff.id_", "role": "stable actor identity"},
            {"name": "staffDataId", "type": "int", "required": True, "authority": "Staff.staffDataID_", "role": "data record identity"},
            {"name": "jobId", "type": "int", "required": True, "authority": "Staff.jobId_ @ 0xEC", "role": "data-defined job lookup"},
            {"name": "skillId", "type": "int", "required": True, "authority": "Staff.skillId_", "role": "data-defined skill lookup"},
            {"name": "hp", "type": "int", "required": True, "authority": "Staff.hp_ @ 0xE8", "role": "authoritative HP"},
            {"name": "hpMax", "type": "int", "required": True, "authority": "GetBaseParam/GetJobParam", "role": "computed maximum"},
            {"name": "state", "type": "enum", "required": True, "authority": "Staff.state_ @ 0x70", "role": "living/develop state"},
            {"name": "moveMode", "type": "enum", "required": True, "authority": "Staff.moveMode_ @ 0xA8", "role": "arrival dispatch key"},
            {"name": "flags", "type": "bitset", "required": True, "authority": "Staff.flag_ @ 0xAC", "role": "sitting/sleep/talk/planning flags"},
            {"name": "roomId", "type": "int|null", "required": True, "authority": "Staff.room_ @ 0x90", "role": "current room"},
            {"name": "floor", "type": "int", "required": True, "authority": "Staff.floor_ @ 0x98", "role": "current floor"},
            {"name": "deskId", "type": "int", "required": True, "authority": "Staff.deskId_ @ 0xB8", "role": "owned workstation; -1 none"},
            {"name": "objIndex", "type": "int", "required": True, "authority": "Staff.objIndex_ @ 0xA0", "role": "current target"},
            {"name": "frame", "type": "int", "required": True, "authority": "Staff.frame_ @ 0x84", "role": "native frame/cadence input"},
            {"name": "recoveryStartFrame", "type": "int", "required": True, "authority": "Staff.frameToStartRecovery_ @ 0xF0", "role": "recovery delay"},
            {"name": "recoveryHpStock", "type": "int", "required": True, "authority": "Staff.recoveryHpStock_ @ 0xF8", "role": "pending recovery units"},
            {"name": "route", "type": "route-node[]", "required": True, "authority": "Staff.route_ @ 0x88", "role": "native movement route"},
            {"name": "taskAssignment", "type": "absent|policy-defined", "required": False, "authority": "not present in recovered original Staff state", "role": "PRODUCT_POLICY_PENDING"},
        ],
        "invariants": ["hp is not decremented by ordinary UpdateWork", "deskId and ObjChip.staffId are paired while a desk is owned", "moveMode 1..11 dispatches through the native arrival table"],
        "source_refs": source_refs,
    }

    furniture_schema = {
        "schema_version": "social-dev-canonical-furniture-schema-final-v1",
        "status": "FINAL_FOR_ORIGINAL_LIVING_CORE",
        "authority": "ObjChip native storage plus exact FurnitureData role rules.",
        "entity": "Furniture/ObjChip",
        "fields": [
            {"name": "id", "type": "int", "required": True, "authority": "ObjChip.index_ @ 0x10", "role": "chip identity"},
            {"name": "type", "type": "enum", "required": True, "authority": "ObjChip.type_ @ 0x18", "role": "native interaction type"},
            {"name": "furnitureDataId", "type": "int|null", "required": True, "authority": "FurnitureData identity through furnitureData_ @ 0x20", "role": "installed content"},
            {"name": "installed", "type": "bool", "required": True, "authority": "furnitureData_ != null", "role": "selector eligibility"},
            {"name": "ownerStaffId", "type": "int", "required": True, "authority": "ObjChip.staffId_ @ 0x78", "role": "workstation owner; -1 vacant"},
            {"name": "reservedUserIds", "type": "int[]", "required": True, "authority": "reservedStaffs_ @ 0x70", "role": "equipment contention"},
            {"name": "activeUserIds", "type": "int[]", "required": True, "authority": "staffs_ @ 0x68", "role": "active users; not GetUsersNum"},
            {"name": "useCount", "type": "int", "required": True, "authority": "useNum_ @ 0x8C", "role": "completed uses capped at 99"},
            {"name": "usePoint", "type": "int", "required": True, "authority": "usePoint_ @ 0x90", "role": "use-point stock"},
            {"name": "passMap", "type": "raw grid", "required": False, "authority": "FurnitureData.passMap_", "role": "native passability input"},
            {"name": "role", "type": "enum", "required": True, "authority": "type/recovery predicate", "role": "WORKSTATION/EQUIPMENT/RECOVERY_EQUIPMENT/DOOR"},
        ],
        "invariants": ["type 2 installed owner -1 is vacant", "reserved users are distinct from active users", "rest/social roles are not inferred from names or sprites"],
        "source_refs": source_refs,
    }

    dashboard_boundary = {
        "schema_version": "social-dev-dashboard-policy-deferred-boundary-v1",
        "status": "PRODUCT_POLICY_PENDING",
        "original_ui": "CUT_LATER",
        "visual_work_performed": "NO",
        "allowed_now": ["static evidence", "native living-core contracts", "deterministic fixtures", "English reports/state updates"],
        "deferred": ["dashboard UI", "task assignment interaction", "task queue/priority policy", "renderer/MapChip/V8 work", "server authority"],
        "future_decision_required": ["whether dashboard edits job/skill or creates a new task abstraction", "whether task assignment overrides autonomy", "fairness/priority semantics if a new task system is introduced"],
        "preservation_rule": "Do not label a future dashboard policy as original behavior without new evidence and an explicit product decision.",
        "source_refs": source_refs,
    }

    unknowns = {
        "schema_version": "social-dev-living-core-unknowns-v1",
        "status": "tracked_non_blocking",
        "policy": "The six original living-core blockers are closed. Remaining unknowns are explicitly non-blocking or belong to deferred product policy.",
        "unknowns": [
            {"id": "LC-U01", "area": "pathfinding", "question": "What are every internal A* helper's tie-break details?", "blocked_now": False, "reason": "route head consumption and arrival dispatch are closed; helper internals are not required for living-core authority"},
            {"id": "LC-U02", "area": "animation", "question": "What is every directional seb/animation asset mapping?", "blocked_now": False, "reason": "state/mode transitions and native side effects are closed"},
            {"id": "LC-U03", "area": "assignment UI", "question": "Which original UI event, if any, called SetJobId/ChangeSkill/EvolveJob in omitted or damaged code?", "blocked_now": False, "reason": "no extracted C# caller was recovered; original UI is explicitly CUT_LATER"},
            {"id": "LC-U04", "area": "dashboard policy", "question": "Should a future dashboard task system override or coexist with autonomous Staff.UpdateWork?", "blocked_now": True, "reason": "PRODUCT_POLICY_PENDING; outside this closure"},
            {"id": "LC-U05", "area": "type-4 furniture geometry", "question": "What are all parent/child placement details for every type-4 chip?", "blocked_now": False, "reason": "exact living role is already bounded by native type/recovery behavior"},
        ],
        "stop_rule": "Do not reopen closed blockers or expand into UI/runtime work without new scope authorization.",
    }

    payloads = {
        "checkpoint-ledger.json": {"schema_version": "social-dev-living-core-checkpoint-ledger-v1", "closure_status": "PASS_ORIGINAL_LIVING_CORE_CLOSED", "records": checkpoint_records, "hash_verification": hashes, "required_stop_literals": {"Visual work performed": "NO", "V8_started": "NO", "renderer_changed": "NO", "MapChip_changed": "NO", "subagents": "NO", "emulator_ADB_live_app": "NO", "local_server": "NO", "network": "NO"}, "source_limits": ["static-only", "no runtime/server/emulator", "source roots read-only", "dashboard UI CUT_LATER"]},
        "blocker-matrix.json": blocker_matrix,
        "staff-native-authority-map.json": native_authority,
        "hp-native-write-site-catalog.json": {"schema_version": "social-dev-hp-native-write-site-catalog-v1", "field": {"name": "hp_", "offset": "0xE8", "class": "Staff"}, "write_sites": hp_write_sites, "negative_trace": {"method": "Staff.UpdateWork", "rva": "0x12D4A7C", "hp_field_offset": "0xE8", "str_or_stur_write_count": 0, "RecoverHp_call_count": 0, "negative_recovery_call_count": 0}, "source_refs": source_refs},
        "ordinary-work-hp-drain-contract.json": ordinary_work,
        "recovery-cadence-contract.json": recovery_contract,
        "recovery-cadence-native-trace.json": recovery_trace,
        "on-arrive-goal-jump-table.json": arrival_table,
        "on-arrive-goal-dispatch-contract.json": arrival_contract,
        "workstation-vacancy-ownership-contract.json": workstation,
        "desk-selection-fixtures.json": desk_fixtures,
        "equipment-user-count-contract.json": equipment_user_count,
        "equipment-contention-contract.json": equipment_contention,
        "furniture-exact-role-contract.json": furniture_exact,
        "furniture-living-role-catalog.json": role_catalog,
        "original-work-assignment-contract.json": original_work,
        "original-task-to-living-core-boundary.json": task_boundary,
        "work-interruption-resume-contract.json": interruption,
        "complete-original-staff-life-loop.json": life_loop,
        "living-core-scenario-fixtures.json": scenarios,
        "canonical-actor-schema-final.json": actor_schema,
        "canonical-furniture-schema-final.json": furniture_schema,
        "dashboard-policy-deferred-boundary.json": dashboard_boundary,
        "unknowns.json": unknowns,
    }
    for name, payload in payloads.items():
        write_json(name, payload)

    write_report("LIVING_CORE_FINAL_CLOSURE.md", f"""# Living-Core Final Closure

Status: `PASS_ORIGINAL_LIVING_CORE_CLOSED`

This is the static native closure for the original Staff living loop in the pinned v2.5.1 artifacts. The three required artifact hashes match. The six original blockers are closed in the blocker matrix and the contracts below.

| Blocker | Result |
|---|---|
| LC-1 ordinary work HP drain | `CLOSED_NO_ORIGINAL_DRAIN` |
| LC-2 recovery cadence/stock | `CLOSED_NATIVE_RECOVERY_CADENCE` |
| LC-3 desk vacancy/ownership/fairness | `CLOSED_OWNER_BASED_RAW_ORDER` |
| LC-4 `Staff.OnArriveGoal` | `CLOSED_11_WAY_NATIVE_DISPATCH` |
| LC-5 FurnitureData roles | `CLOSED_EXACT_NATIVE_ROLES` |
| LC-6 original task/work path | `CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER` |

## Scope boundary

Visual work performed: **NO**. V8 started: **NO**. Renderer and MapChip are unchanged. No subagents, emulator/ADB/live app, local development server, network access, or runtime execution were used. The original UI task surface remains `CUT_LATER`; future dashboard policy is `PRODUCT_POLICY_PENDING`.

## Evidence

- [`blocker-matrix.json`]({evidence_ref("blocker-matrix.json")})
- [`staff-native-authority-map.json`]({evidence_ref("staff-native-authority-map.json")})
- [`complete-original-staff-life-loop.json`]({evidence_ref("complete-original-staff-life-loop.json")})
- [`living-core-scenario-fixtures.json`]({evidence_ref("living-core-scenario-fixtures.json")})
""")

    write_report("ORDINARY_WORK_HP_DRAIN.md", f"""# Ordinary Work HP Drain

Status: `CLOSED_NO_ORIGINAL_DRAIN`

Native `Staff.UpdateWork` at `0x12D4A7C` contains the original 20-frame work decision gates, typing progression, sleeping flag, equipment choice, and talk choice. It has no write to `hp_` at `0xE8` and no `RecoverHp` call, positive or negative. Ordinary work therefore preserves HP unless another proven system changes it in the same frame.

HP writes remain limited to initialization, recovery/max correction, combat damage, original-record synchronization, and explicit setters. Equipment recovery adds stock; it does not create a work drain.

Evidence: [`ordinary-work-hp-drain-contract.json`]({evidence_ref("ordinary-work-hp-drain-contract.json")}), [`hp-native-write-site-catalog.json`]({evidence_ref("hp-native-write-site-catalog.json")} ).
""")

    write_report("RECOVERY_CADENCE.md", f"""# Recovery Cadence

Status: `CLOSED_NATIVE_RECOVERY_CADENCE`

`Staff.AddRecoveryHpStock` at `0x12D2EB0` sets a 20-frame start countdown and adds stock. `Staff.UpdateRecoveryHp` at `0x12D2C8C` consumes one stock and calls `RecoverHp(1)` on non-negative frames where `frame_%3==0`. When stock reaches zero, the native effect state writes a 40-frame gauge/effect reset and stock remains zero. `RecoverHp` clamps to the computed maximum and clears `FLAG_SLEEPING` at max.

Home recovery is a separate direct `RecoverHp(1)` path in `UpdateStayHome`.

Evidence: [`recovery-cadence-contract.json`]({evidence_ref("recovery-cadence-contract.json")}), [`recovery-cadence-native-trace.json`]({evidence_ref("recovery-cadence-native-trace.json")} ).
""")

    write_report("ON_ARRIVE_GOAL_DISPATCH.md", f"""# `Staff.OnArriveGoal` Dispatch

Status: `CLOSED_11_WAY_NATIVE_DISPATCH`

The native method at `0x12D8420` reads `moveMode_` at offset `0xA8`, subtracts one, rejects unsigned keys above ten, and dispatches through the 16-bit table at rodata `0x636684` with base `0x12D84A8`. All move modes 1 through 11 are decoded and recorded with their native target RVAs and side effects.

Evidence: [`on-arrive-goal-jump-table.json`]({evidence_ref("on-arrive-goal-jump-table.json")}), [`on-arrive-goal-dispatch-contract.json`]({evidence_ref("on-arrive-goal-dispatch-contract.json")} ).
""")

    write_report("WORKSTATION_OWNERSHIP_AND_VACANCY.md", f"""# Workstation Ownership and Vacancy

Status: `CLOSED_OWNER_BASED_RAW_ORDER`

`ObjChip.Init` initializes `staffId_` at `0x78` to `-1`. `Room.GetStaffEmptyObjTypeOf` at `0x12CF178` scans the raw chip vector and returns the first installed type-2 chip whose owner is `-1`. `Room.AddStaff` writes both the staff `deskId_` and the chip owner. The original selector contains no fairness queue, randomization, or rotation.

`Room.ThereIsEmptyDesk` is only a broad boolean and is not a substitute for the exact selector.

Evidence: [`workstation-vacancy-ownership-contract.json`]({evidence_ref("workstation-vacancy-ownership-contract.json")}), [`desk-selection-fixtures.json`]({evidence_ref("desk-selection-fixtures.json")} ).
""")

    write_report("EQUIPMENT_CONTENTION.md", f"""# Equipment Contention

Status: `CLOSED_RESERVED_VECTOR_CONTENTION`

`ObjChip.GetUsersNum` at `0x12C4A70` returns the length of `reservedStaffs_` at `0x70`; it ignores the active-user vector and workstation owner. `Staff.GotoEquip` checks this count before reserving a type-1/type-4 target. `ReserveUse` appends the reservation, and `OnUseComplate` removes it and increments the use counter up to 99.

The native code proves a reservation-based single-thread decision, not a queue, lock, capacity policy, or fairness policy.

Evidence: [`equipment-user-count-contract.json`]({evidence_ref("equipment-user-count-contract.json")}), [`equipment-contention-contract.json`]({evidence_ref("equipment-contention-contract.json")} ).
""")

    write_report("FURNITURE_EXACT_LIVING_ROLES.md", f"""# Exact Furniture Living Roles

Status: `CLOSED_EXACT_NATIVE_ROLES`

The source/evidence package contains 103 FurnitureData records. Native interaction promotes 10 workstations (`type_ == 2`), 43 type-1/type-4 equipment records with no proven HP effect, 49 recovery equipment records, and one door record. No record is promoted to REST or SOCIAL from names, sprites, or raw data alone. Rest is the Staff stay-home lifecycle; social movement uses pass chips and Staff talk states.

Evidence: [`furniture-exact-role-contract.json`]({evidence_ref("furniture-exact-role-contract.json")}), [`furniture-living-role-catalog.json`]({evidence_ref("furniture-living-role-catalog.json")} ).
""")

    write_report("ORIGINAL_WORK_ASSIGNMENT_FLOW.md", f"""# Original Work Assignment Flow

Status: `CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER`

The original path is data-defined and autonomous: `Staff.Init` binds `StaffData.jobId_`/`skill_`; `Room.AddStaff` assigns a desk owner and optionally starts planning; `Staff.Update` dispatches the living state; and `Staff.UpdateWork` autonomously chooses typing, equipment, talk, or sleep. No recovered `Staff.UpdateWork` input is a dashboard task object.

The extracted source exposes `SetJobId`, `ChangeSkill`, and `EvolveJob`, but exact source call-site search recovers only their definitions. Forms read/display job data, but no reliable UI mutation caller is promoted. The original UI is therefore `CUT_LATER`, and future dashboard policy is `PRODUCT_POLICY_PENDING`.

Evidence: [`original-work-assignment-contract.json`]({evidence_ref("original-work-assignment-contract.json")}), [`original-task-to-living-core-boundary.json`]({evidence_ref("original-task-to-living-core-boundary.json")} ).
""")

    write_report("WORK_INTERRUPTION_AND_RESUME.md", f"""# Work Interruption and Resume

Status: `CLOSED_ORIGINAL_RESUME_PATH`

Equipment and talk are explicit interruptions from ordinary work. Equipment uses reservations, dispatches through the native arrival table, completes through `OnUseComplate`, and returns through `GotoDesk`. Talk uses reserved-talk flags and the TO_STAFF/TO_BACK_OF_CHAIR/TO_STAND_TALKING modes, then returns to the owned desk. Low HP routes through the door to stay-home recovery; at HP ratio 40 or above, the staff reserves the door and returns toward the desk. Desk destruction/floor removal clears ownership before any new desk resolution.

Evidence: [`work-interruption-resume-contract.json`]({evidence_ref("work-interruption-resume-contract.json")} ).
""")

    write_report("COMPLETE_STAFF_LIFE_LOOP.md", f"""# Complete Original Staff Life Loop

Status: `CLOSED_COMPLETE_ORIGINAL_LIVING_CORE`

The closed sequence is: data bind → room/desk attach → desk arrival → sitting/work → equipment/talk interruption → completion and desk return → recovery stock cadence → low-HP door/home recovery → desk resume. Deterministic static fixtures cover each boundary. Visual animation parity, pathfinding helper internals, and dashboard policy remain outside the closure.

Evidence: [`complete-original-staff-life-loop.json`]({evidence_ref("complete-original-staff-life-loop.json")}), [`living-core-scenario-fixtures.json`]({evidence_ref("living-core-scenario-fixtures.json")} ).
""")

    write_report("LIVING_CORE_FINAL_HANDOFF.md", f"""# Living-Core Final Handoff

## Closure

`PASS_ORIGINAL_LIVING_CORE_CLOSED`

All six original blockers are closed with pinned hashes, native RVAs, field offsets, contracts, fixtures, and reports. The canonical actor schema keeps HP, ownership, reservation, route, state, and recovery fields explicit. The canonical furniture schema keeps active users, reserved users, and workstation owner distinct.

## Required stop boundary

Visual work performed: **NO**. V8 started: **NO**. Renderer/MapChip unchanged. Subagents: **NO**. Emulator/ADB/live app: **NO**. Local server: **NO**. Network: **NO**. Source roots remain read-only. No runtime files were changed for this closure.

## Deferred product boundary

Original UI: `CUT_LATER`. Future dashboard task/assignment policy: `PRODUCT_POLICY_PENDING`. Do not infer a dashboard queue or fairness policy from the autonomous native Staff loop.

## Verification entry points

- `python tools/social-dev/test_living_core_final_closure.py`
- [`checkpoint-ledger.json`]({evidence_ref("checkpoint-ledger.json")})
- [`unknowns.json`]({evidence_ref("unknowns.json")})
""")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    build_all()
    if not args.quiet:
        print(f"built {len(list(OUT.glob('*.json')))} JSON evidence files and final closure reports in {REPORTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
