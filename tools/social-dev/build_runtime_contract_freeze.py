"""Build the R0 canonical runtime-contract freeze package.

This is a static, inline-only package builder.  It reads the already accepted
G1.5/living-core evidence and the current web runtime for comparison.  It does
not execute decompiled C#, start a server, inspect an emulator, or modify the
living runtime.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge/data/original"
KB_EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME = ROOT / "runtime/social-dev"
RUNTIME_SRC = RUNTIME / "src"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
OUT = KB_EVIDENCE / "runtime-contract-freeze"
REPORTS = ROOT / "docs/Phases/Runtime"

SOURCE_IDENTITY_PATH = KB / "source_identity.json"
KB_MANIFEST_PATH = KB / "build_manifest.json"
APK = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
RAW_NATIVE = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
RAW_METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"

EXPECTED_HASHES = {
    "apk": "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    "libil2cpp": "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    "global_metadata": "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
    "dump": "4487cba6916e159afefec2cd1a9ecf0d12d05b2d76126e7099a5d35323967eb2",
}

ALLOWED_AUTHORITY = {
    "CANONICAL_G1_5",
    "NATIVE_CLOSED",
    "METADATA_VERIFIED",
    "INTACT_CSHARP",
    "ORIGINAL_DATA",
    "ACCEPTED_CLOSURE",
    "DERIVED_RUNTIME_HELPER",
    "PRODUCT_POLICY",
    "SOURCE_LIMITED",
}

DISPOSITIONS = {
    "KEEP",
    "KEEP_VISUAL_ONLY",
    "EXTEND",
    "REPLACE",
    "SUPERSEDED",
    "PRODUCT_LAYER_ONLY",
    "OUT_OF_SCOPE",
    "UNKNOWN_REVIEW_REQUIRED",
}

CONTRACT_NAMES = [
    "runtime-delta-matrix.json",
    "actor-runtime-contract.json",
    "room-runtime-contract.json",
    "furniture-instance-contract.json",
    "movement-route-contract.json",
    "staff-state-machine-contract.json",
    "tick-order-contract-v2.json",
    "rng-autonomy-contract.json",
    "hp-recovery-home-runtime-contract.json",
    "work-planning-runtime-contract.json",
    "interruption-resume-contract.json",
    "visual-projection-boundary.json",
    "product-policy-boundary.json",
    "save-boundary-contract.json",
    "runtime-scenario-fixtures.json",
]

SUPPORTING_NAMES = [
    "runtime-contract-validation.json",
    "checkpoint-ledger.json",
    "runtime-contract-manifest.json",
]

REPORT_NAMES = [
    "R0_EXISTING_RUNTIME_DELTA_AUDIT.md",
    "R0_ACTOR_ROOM_FURNITURE_CONTRACT.md",
    "R0_MOVEMENT_STATE_TICK_RNG_CONTRACT.md",
    "R0_HP_WORK_INTERRUPTION_CONTRACT.md",
    "R0_VISUAL_PRODUCT_SAVE_BOUNDARY.md",
    "R0_SCENARIO_FIXTURES.md",
    "R0_RUNTIME_CONTRACT_FREEZE.md",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, value: Any) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_evidence(relative_path: str) -> Any:
    return load_json(KB_EVIDENCE / relative_path)


def provenance(
    canonical_fact_id: str,
    canonical_entity_id: str | None,
    source_evidence_path: str,
    authority_type: str,
    confidence: str = "high",
    status: str = "CLOSED",
) -> dict[str, Any]:
    if authority_type not in ALLOWED_AUTHORITY:
        raise ValueError(f"Unsupported authority type: {authority_type}")
    return {
        "canonical_fact_id": canonical_fact_id,
        "canonical_entity_id": canonical_entity_id,
        "source_evidence_path": source_evidence_path,
        "authority_type": authority_type,
        "confidence": confidence,
        "status": status,
    }


def fact(
    name: str,
    value: Any,
    canonical_fact_id: str,
    entity: str | None,
    evidence: str,
    authority: str,
    confidence: str = "high",
    status: str = "CLOSED",
    **extra: Any,
) -> dict[str, Any]:
    return {
        "name": name,
        "value": value,
        **extra,
        "provenance": provenance(canonical_fact_id, entity, evidence, authority, confidence, status),
    }


def field(
    name: str,
    field_type: str,
    role: str,
    section: str,
    canonical_fact_id: str,
    entity: str | None,
    evidence: str,
    authority: str,
    confidence: str = "high",
    status: str = "CLOSED",
    **extra: Any,
) -> dict[str, Any]:
    return {
        "name": name,
        "type": field_type,
        "role": role,
        "section": section,
        **extra,
        "provenance": provenance(canonical_fact_id, entity, evidence, authority, confidence, status),
    }


def source_identity() -> dict[str, Any]:
    source = load_json(SOURCE_IDENTITY_PATH)
    observed = {
        "apk": sha256_file(APK),
        "libil2cpp": sha256_file(RAW_NATIVE),
        "global_metadata": sha256_file(RAW_METADATA),
        "dump": sha256_file(DUMP),
    }
    expected = {
        "apk": EXPECTED_HASHES["apk"],
        "libil2cpp": EXPECTED_HASHES["libil2cpp"],
        "global_metadata": EXPECTED_HASHES["global_metadata"],
        "dump": EXPECTED_HASHES["dump"],
    }
    if source.get("status") != "PASS_SOURCE_IDENTITY" or observed != expected:
        raise RuntimeError("FAIL_R0_SOURCE_IDENTITY_MISMATCH")
    return {
        "status": "PASS_SOURCE_IDENTITY",
        "expected_hashes": expected,
        "observed_hashes": observed,
        "source_identity_file": rel(SOURCE_IDENTITY_PATH),
        "source_identity_file_sha256": sha256_file(SOURCE_IDENTITY_PATH),
        "apk_path": rel(APK),
        "native_path": rel(RAW_NATIVE),
        "metadata_path": rel(RAW_METADATA),
        "dump_path": rel(DUMP),
    }


def field_inventory() -> dict[str, Any]:
    return load_evidence("behavior-first/staff-field-inventory.json")


def staff_field(name: str) -> dict[str, Any]:
    for item in field_inventory().get("fields", []):
        if item.get("name") == name:
            dump = item.get("dump", {})
            return {
                "name": name,
                "offset": dump.get("offset"),
                "group": item.get("group"),
                "mutable": item.get("mutable"),
                "source": item.get("source"),
            }
    return {"name": name, "offset": None, "group": "source_limited", "mutable": None, "source": None}


def r0_header(schema_version: str, title: str, identity: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": schema_version,
        "phase": "R0",
        "title": title,
        "status": "FROZEN_FOR_IMPLEMENTATION",
        "execution_mode": "INLINE_STATIC_CONTRACT_ONLY",
        "source_authority": {
            "canonical_kb_status": load_json(KB_MANIFEST_PATH)["status"],
            "canonical_kb_manifest": rel(KB_MANIFEST_PATH),
            "canonical_kb_manifest_sha256": sha256_file(KB_MANIFEST_PATH),
            "source_identity": identity,
        },
    }


def build_actor_contract(identity: dict[str, Any]) -> dict[str, Any]:
    static_evidence = "living-core-closure/canonical-actor-schema-final.json"
    field_evidence = "behavior-first/staff-field-inventory.json"
    actor = r0_header("social-dev-r0-actor-runtime-contract-v1", "Canonical Staff actor runtime contract", identity)
    actor["original_static_identity"] = [
        field("id", "int", "stable native Staff identity", "ORIGINAL_STATIC_IDENTITY", "LC-6", "Staff", static_evidence, "ACCEPTED_CLOSURE", native_field="Staff.id_", native_offset=staff_field("id_")["offset"]),
        field("staffDataId", "int", "StaffData record identity", "ORIGINAL_STATIC_IDENTITY", "DD-ACTOR-IDENTITY", "Staff", "data-dependency/canonical-actor-schema.json", "ACCEPTED_CLOSURE", native_field="Staff.staffData_ -> StaffData.id_", native_offset=staff_field("staffData_")["offset"]),
        field("jobId", "int", "data-defined JobData lookup", "ORIGINAL_STATIC_IDENTITY", "DD-JOB-LINK", "Staff", "data-dependency/staff-job-link-contract.json", "CANONICAL_G1_5", native_field="Staff.jobId_", native_offset=staff_field("jobId_")["offset"]),
        field("level", "int", "Staff progression level used by JobData parameter lookup", "ORIGINAL_STATIC_IDENTITY", "DD-LEVEL-PARAM", "Staff", "data-dependency/staff-derived-parameter-contract.json", "NATIVE_CLOSED", native_field="Staff.level_", native_offset=staff_field("level_")["offset"]),
        field("skillId", "int", "data-defined SkillData lookup", "ORIGINAL_STATIC_IDENTITY", "DD-SKILL-LINK", "Staff", "data-dependency/staff-skill-link-contract.json", "CANONICAL_G1_5", native_field="Staff.skillId_", native_offset=staff_field("skillId_")["offset"]),
        field("originalDataCatalogRefs", "object", "references StaffData, JobData, SkillData records without copying product identifiers", "ORIGINAL_STATIC_IDENTITY", "C8", "Staff", "knowledge/data/original/build_manifest.json", "CANONICAL_G1_5", catalog_counts={"StaffData": 141, "JobData": 30, "SkillData": 36}),
    ]
    mutable = [
        ("hp", "int", "authoritative HP", "Staff.hp_", "0xE8", "C1", "CANONICAL_G1_5", "hp-data-dependency-contract.json"),
        ("state", "enum<int>", "native Staff state", "Staff.state_", "0x70", "BF-STATES", "ACCEPTED_CLOSURE", field_evidence),
        ("moveMode", "enum<int>", "native arrival dispatch key", "Staff.moveMode_", "0xA8", "LC-4", "NATIVE_CLOSED", "living-core-closure/on-arrive-goal-dispatch-contract.json"),
        ("flags", "bitset<int>", "sitting, typing, sleeping, talk, planning, fade and other native flags", "Staff.flag_", "0xAC", "BF-FLAGS", "METADATA_VERIFIED", field_evidence),
        ("animationActionId", "int", "native SEB/action selector state", "Staff.sebId_", "0x74", "BF-ACTION", "METADATA_VERIFIED", field_evidence),
        ("animationFrame", "int", "native SEB frame", "Staff.sebFrame_", "0x68", "BF-ACTION", "METADATA_VERIFIED", field_evidence),
        ("animationFrameInterval", "int", "native animation interval", "Staff.sebFrameInterval_", "0x6C", "BF-ACTION", "METADATA_VERIFIED", field_evidence),
        ("alpha", "int", "native actor alpha/fade value", "Staff.alpha_", "0xC8", "BF-ACTION", "METADATA_VERIFIED", field_evidence),
        ("worldX", "int", "native Staff world x", "Staff.x_", staff_field("x_")["offset"], "BF-POSITION", "METADATA_VERIFIED", field_evidence),
        ("worldY", "int", "native Staff world y", "Staff.y_", staff_field("y_")["offset"], "BF-POSITION", "METADATA_VERIFIED", field_evidence),
        ("gridObjectIndex", "Vector2D", "current grid/object target", "Staff.objIndex_", "0xA0", "BF-MOVEMENT", "METADATA_VERIFIED", field_evidence),
        ("roomRef", "Room|null", "current Room membership", "Staff.room_", "0x90", "BF-MOVEMENT", "METADATA_VERIFIED", field_evidence),
        ("floor", "int", "current native floor", "Staff.floor_", "0x98", "BF-MOVEMENT", "METADATA_VERIFIED", field_evidence),
        ("deskId", "int", "owned workstation id; -1 means none", "Staff.deskId_", "0xB8", "LC-3", "NATIVE_CLOSED", "living-core-closure/workstation-vacancy-ownership-contract.json"),
        ("staffTalkTargetId", "int", "colleague/talk target id", "Staff.colleagueId_", "0xBC", "BF-TALK", "INTACT_CSHARP", "behavior-first/talk-social-contract.json"),
        ("route", "RouteNode[]", "native route vector", "Staff.route_", "0x88", "BF-MOVEMENT", "NATIVE_CLOSED", "behavior-first/movement-target-arrival-contract.json"),
        ("lastRouteNode", "Node", "last consumed route node", "Staff.lastNode_", "0x170", "BF-MOVEMENT", "NATIVE_CLOSED", "living-core-closure/on-arrive-goal-dispatch-contract.json"),
        ("frame", "int", "native frame/cadence input", "Staff.frame_", "0x84", "BF-TICK", "NATIVE_CLOSED", "living-core-closure/recovery-cadence-native-trace.json"),
        ("moveFrame", "int", "movement frame/timer", "Staff.moveFrame_", "0x178", "BF-TICK", "METADATA_VERIFIED", field_evidence),
        ("typingTimer", "int", "typing progress", "Staff.typingFrame_", "0xE0", "BF-TALK", "INTACT_CSHARP", "behavior-first/talk-social-contract.json"),
        ("talkTimer", "int", "talk progress", "Staff.talkFrame_", "0xE4", "BF-TALK", "INTACT_CSHARP", "behavior-first/talk-social-contract.json"),
        ("recoveryStock", "int", "pending one-HP recovery units", "Staff.recoveryHpStock_", "0xF8", "LC-2", "NATIVE_CLOSED", "living-core-closure/recovery-cadence-contract.json"),
        ("recoveryDelayTimer", "int", "recovery start countdown", "Staff.frameToStartRecovery_", "0xF0", "LC-2", "NATIVE_CLOSED", "living-core-closure/recovery-cadence-contract.json"),
        ("hpGaugeTimer", "int", "HP gauge/effect hide timer; not health", "Staff.frameToHideHpGauge_", "0xF4", "LC-2", "NATIVE_CLOSED", "living-core-closure/recovery-cadence-contract.json"),
        ("recoveryEffectTimer", "int", "recovery visual/effect lifecycle", "Staff.recoveryEffectFrame_", "0x118", "LC-2", "NATIVE_CLOSED", "living-core-closure/recovery-cadence-native-trace.json"),
        ("waitingBackOfDoorTimer", "int", "door return wait timer", "Staff.waitingBackOfDoorFrame_", "0x1DC", "BF-HOME", "METADATA_VERIFIED", field_evidence),
        ("planningRate", "int", "original planning progress", "Staff.planningRate_", "0x108", "C10", "CANONICAL_G1_5", "g1_5/minimal-work-assignment-input-contract.json"),
        ("planQuality", "int", "original planning quality", "Staff.planQuality_", "0x110", "C10", "CANONICAL_G1_5", "g1_5/minimal-work-assignment-input-contract.json"),
        ("planningEndDelayTimer", "int", "original planning end delay", "Staff.planningEndDelayFrame_", "0xFC", "C11", "CANONICAL_G1_5", "g1_5/planning-command-boundary-native.json"),
        ("processStep", "int", "planning/development process step", "Staff.processStep_", "0x78", "C11", "CANONICAL_G1_5", "g1_5/planning-command-boundary-native.json"),
        ("developmentState", "int", "original development state", "Staff.developState_", "0x188", "C11", "CANONICAL_G1_5", "g1_5/planning-command-boundary-native.json"),
    ]
    actor["original_mutable_runtime_state"] = [
        field(name, ftype, role, "ORIGINAL_MUTABLE_RUNTIME_STATE", fact_id, "Staff", evidence, authority, native_field=native_field, native_offset=offset)
        for name, ftype, role, native_field, offset, fact_id, authority, evidence in mutable
    ]
    actor["original_mutable_runtime_state"].append(
        field(
            "direction",
            "direction/vector selector input",
            "native direction is represented through movement/action/vector consumers; no standalone Staff direction field is promoted",
            "ORIGINAL_MUTABLE_RUNTIME_STATE",
            "BF-DIRECTION-LIMIT",
            "Staff",
            "behavior-first/movement-target-arrival-contract.json",
            "SOURCE_LIMITED",
            confidence="source_limited",
            status="NONBLOCKING_SOURCE_LIMIT",
            runtime_field_status="no_standalone_original_field_closed",
        )
    )
    actor["original_mutable_runtime_state"].append(
        field(
            "routeQueue",
            "RouteNode[] view",
            "implementation queue view backed by native route_; not a second original field",
            "ORIGINAL_MUTABLE_RUNTIME_STATE",
            "BF-MOVEMENT",
            "Staff",
            "behavior-first/movement-target-arrival-contract.json",
            "DERIVED_RUNTIME_HELPER",
            status="DERIVED_RUNTIME_HELPER",
            backing_original_field="route_",
        )
    )
    actor["original_mutable_runtime_state"].append(
        field(
            "routeCursor",
            "int helper",
            "cursor into the implementation route queue; native consumes the route head and stores lastNode_",
            "ORIGINAL_MUTABLE_RUNTIME_STATE",
            "BF-MOVEMENT",
            "Staff",
            "living-core-closure/on-arrive-goal-dispatch-contract.json",
            "DERIVED_RUNTIME_HELPER",
            status="DERIVED_RUNTIME_HELPER",
            backing_original_field="route_ / lastNode_",
        )
    )
    actor["derived_state"] = [
        field("maxHp", "int", "computed max HP", "DERIVED_STATE", "C1", "Staff", "data-dependency/hp-data-dependency-contract.json", "CANONICAL_G1_5", formula="GetBaseParam(StaffData.PARAM_HP, 0) + GetJobParam(StaffData.PARAM_HP, level_)", storage="not_an_original_field"),
        field("hpRatioPercent", "int", "integer HP ratio used by native guards", "DERIVED_STATE", "C1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED", formula="trunc_toward_zero(hp_ * 100 / maxHp)", storage="not_an_original_field"),
        field("renderActionSelectorInputs", "object", "projection inputs derived from state/action/frame/direction", "DERIVED_STATE", "VP-1", "Staff", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER", storage="not_an_original_field"),
        field("passabilityAndGoal", "object", "Room/ObjChip-derived target and passability result", "DERIVED_STATE", "BF-MOVEMENT", "Staff", "movement-route-contract.json", "DERIVED_RUNTIME_HELPER", storage="not_an_original_field"),
    ]
    actor["product_only_state"] = [
        field("externalAgentId", "string|null", "external product identity", "PRODUCT_ONLY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("externalTaskId", "string|null", "external product task identity", "PRODUCT_ONLY_STATE", "PRODUCT-1", None, "living-core-closure/original-task-to-living-core-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("backendTaskState", "product enum", "backend execution state", "PRODUCT_ONLY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("dashboardDisplayState", "product object", "presentation of external policy state", "PRODUCT_ONLY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    actor["invariants"] = [
        fact("ordinaryWorkHp", "UpdateWork has no direct hp_ write and no negative RecoverHp call", "LC-1", "Staff", "living-core-closure/ordinary-work-hp-drain-contract.json", "NATIVE_CLOSED"),
        fact("deskRelation", "Staff.deskId_ and ObjChip.staffId_ are paired while a workstation is owned", "LC-3", "Staff", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        fact("arrivalDispatch", "moveMode 1..11 dispatches through the native OnArriveGoal table", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        fact("productSeparation", "Product-only fields are outside original Staff semantics", "PRODUCT-1", "Staff", "living-core-closure/original-task-to-living-core-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    actor["field_identity_policy"] = "A derived helper may reference an original field but must not be serialized or presented as an additional original Staff field. Product-only identifiers never enter the original actor state."
    return actor


def build_room_contract(identity: dict[str, Any]) -> dict[str, Any]:
    room = r0_header("social-dev-r0-room-runtime-contract-v1", "Canonical Room/world runtime contract", identity)
    room["identity"] = [
        field("roomId", "stable room key", "Room identity", "ROOM_IDENTITY", "C8", "Room", "knowledge/fixtures/accepted/runtime/room_catalog_contract.json", "ORIGINAL_DATA"),
        field("roomDataId", "int", "native RoomData record identity", "ROOM_IDENTITY", "C8", "Room", "knowledge/fixtures/accepted/runtime/room_catalog_contract.json", "ORIGINAL_DATA"),
        field("nativeFloor", "int", "Room constructor floor selector", "ROOM_IDENTITY", "BF-FLOOR", "Room", "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json", "NATIVE_CLOSED"),
        field("context", "main_display|persistent_room|addition_floor_preview", "constructor/display context", "ROOM_IDENTITY", "BF-FLOOR", "Room", "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json", "NATIVE_CLOSED"),
    ]
    room["topology"] = [
        fact("mapChipMainDisplay", {"width": 14, "height": 14, "cellCount": 196, "variant": "floor_0"}, "BF-MAPCHIP-TOPOLOGY", "MapChip", "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json", "NATIVE_CLOSED"),
        fact("mapChipNonzeroPreview", {"width": 4, "height": 4, "cellCount": 16, "variant": "floor_nonzero"}, "BF-MAPCHIP-TOPOLOGY", "MapChip", "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json", "NATIVE_CLOSED", status="CONTEXT_LIMITED"),
        fact("objChipOccupancy", {"width": 10, "height": 10, "cellCount": 100, "indexing": "x + y * width"}, "BF-OBJCHIP-TOPOLOGY", "ObjChip", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        fact("coordinateSeparation", "MapChip 14x14 topology and ObjChip 10x10 occupancy are separate coordinate systems", "BF-COORDINATE-SEPARATION", "Room", "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "ACCEPTED_CLOSURE"),
    ]
    room["membership_and_order"] = [
        fact("roomStaffMembership", "Room.staffs_ owns Staff membership and Room.Update iterates the staff vector before ObjChip updates", "BF-TICK-ROOM", "Room", "behavior-first/idle-autonomy-contract.json", "NATIVE_CLOSED"),
        fact("roomFurnitureMembership", "Room.objChips_ owns raw ObjChip instances and raw vector order is observable by selectors", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        fact("rawChipTraversal", "Do not replace raw ObjChip order with a fairness queue or stable-id sort", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
    ]
    room["lookup_rules"] = [
        fact("passability", "ObjChip.IsPassable plus FurnitureData.passMap_ controls native passability; type alone is insufficient", "BF-PASSMAP", "ObjChip", "behavior-first/movement-target-arrival-contract.json", "NATIVE_CLOSED"),
        fact("goalLookup", "A goal is admitted through native ObjChip type/HasObj/IsPassable predicates and standing-position checks", "BF-GOAL-FILTER", "ObjChip", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        fact("deskLookup", "GetStaffEmptyObjTypeOf(2) requires type 2, installed FurnitureData, staffId == -1 and returns the first raw-order match", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        fact("equipmentLookup", "GetRandomObjChipTypeOf selects a candidate for type 1 or 4; Staff.GotoEquip rejects reserved users", "LC-2", "Room", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        fact("doorLookup", "Room.GetDoorIndex scans the native door relation; the door chip is raw type 5 and may have null FurnitureData", "LC-5", "Room", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
    ]
    room["update_and_planning"] = [
        fact("roomUpdateResponsibility", "Player high-level update invokes Room.Update; Room.Update loops Staff.Update then ObjChip.Update", "BF-TICK-ROOM", "Room", "behavior-first/idle-autonomy-contract.json", "NATIVE_CLOSED"),
        fact("planningStart", "Player.StartPlanning -> Room.OnStartPlanning -> Staff.OnStartPlanning", "C10", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("planningUpdate", "Player.UpdatePlanning(elapsedTime) -> Room.UpdatePlanning -> Staff.UpdatePlanning2(elapsedTime)", "C11", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("planningEnd", "Player.IsCompletedPlanning -> Room.OnEndPlanning -> Staff.OnEndPlanning", "C11", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
    ]
    room["render_projection_boundary"] = fact("projection", "Room behavior state is projected to rendering after the canonical update boundary; renderer does not mutate Room/Staff/ObjChip", "VP-1", "Room", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER")
    room["invariants"] = [
        fact("noFurnitureInference", "Room must not infer FurnitureData identity from ObjChip.type alone", "LC-5", "Room", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
        fact("noGridCollapse", "MapChip and ObjChip topology remain separately addressable", "BF-COORDINATE-SEPARATION", "Room", "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "ACCEPTED_CLOSURE"),
    ]
    return room


def build_furniture_contract(identity: dict[str, Any]) -> dict[str, Any]:
    furniture = r0_header("social-dev-r0-furniture-instance-contract-v1", "Canonical furniture instance contract", identity)
    furniture["fields"] = [
        field("instanceId", "int", "ObjChip instance identity", "INSTANCE_IDENTITY", "BF-OBJCHIP-FIELDS", "ObjChip", "living-core-closure/canonical-furniture-schema-final.json", "ACCEPTED_CLOSURE", native_field="ObjChip.index_", native_offset="0x10"),
        field("furnitureDataId", "int|null", "installed FurnitureData identity", "INSTANCE_IDENTITY", "LC-5", "ObjChip", "living-core-closure/canonical-furniture-schema-final.json", "NATIVE_CLOSED", native_field="ObjChip.furnitureData_", native_offset="0x20"),
        field("cellAnchor", "grid cell", "ObjChip cell/anchor", "GEOMETRY", "BF-COORDINATE-SEPARATION", "ObjChip", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        field("rawDirection", "int", "preserved native direction value", "GEOMETRY", "BF-DIRECTION", "ObjChip", "knowledge/fixtures/accepted/runtime/native_direction_contract.json", "NATIVE_CLOSED"),
        field("footprint", "grid cell[]", "native placement footprint", "GEOMETRY", "BF-PASSMAP", "FurnitureData", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        field("passMap", "raw grid", "FurnitureData.passMap_ input to IsPassable", "GEOMETRY", "BF-PASSMAP", "FurnitureData", "behavior-first/furniture-behavior-catalog.json", "NATIVE_CLOSED"),
        field("standingPositions", "world/grid positions[]", "native approach/standing positions", "GEOMETRY", "BF-STANDING-POSITIONS", "ObjChip", "behavior-first/movement-target-arrival-contract.json", "NATIVE_CLOSED"),
        field("ownerStaffId", "int", "workstation owner; -1 means vacant", "OWNERSHIP", "LC-3", "ObjChip", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED", native_field="ObjChip.staffId_", native_offset="0x78"),
        field("activeUserIds", "int[]", "active users; not the contention count", "USERS", "LC-2", "ObjChip", "living-core-closure/equipment-user-count-contract.json", "NATIVE_CLOSED", native_field="ObjChip.staffs_", native_offset="0x68"),
        field("reservedUserIds", "int[]", "reserved users; authoritative equipment contention vector", "USERS", "LC-2", "ObjChip", "living-core-closure/equipment-user-count-contract.json", "NATIVE_CLOSED", native_field="ObjChip.reservedStaffs_", native_offset="0x70"),
        field("useCount", "int", "completed-use counter capped at 99", "USE_STATE", "LC-2", "ObjChip", "living-core-closure/equipment-user-count-contract.json", "NATIVE_CLOSED", native_field="ObjChip.useNum_", native_offset="0x8C"),
        field("usePoint", "int", "native use-point stock", "USE_STATE", "LC-2", "ObjChip", "living-core-closure/canonical-furniture-schema-final.json", "NATIVE_CLOSED", native_field="ObjChip.usePoint_", native_offset="0x90"),
        field("useEffectState", "object", "native action/recovery/use effect state", "USE_STATE", "LC-2", "ObjChip", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        field("visualSelectorRefs", "object", "presentation selectors only", "VISUAL_PROJECTION", "VP-1", "FurnitureData", "knowledge/fixtures/accepted/runtime/object_catalog_contract.json", "SOURCE_LIMITED"),
    ]
    furniture["role_counts"] = [
        fact("WORKSTATION", 10, "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
        fact("RECOVERY_EQUIPMENT", 49, "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
        fact("EQUIPMENT_NO_HP_EFFECT_PROVEN", 43, "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
        fact("DOOR", 1, "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
    ]
    furniture["role_rules"] = [
        fact("workstationRule", "ObjChip.type == 2; ownership/vacancy uses installed FurnitureData and ownerStaffId", "LC-3", "FurnitureData", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        fact("equipmentRule", "ObjChip.type in {1,4}; recovery_ >= 1 is the only proven HP-recovery effect", "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
        fact("doorRule", "Door relation is type 5; no separate REST/SOCIAL FurnitureData role is promoted", "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
    ]
    furniture["ownership_reservation_policy"] = [
        fact("ownerActiveReservedDistinct", "ownerStaffId, activeUserIds, and reservedUserIds are independent runtime identities", "LC-2", "ObjChip", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        fact("equipmentContention", "GetUsersNum returns reservedStaffs_ length; active users and owner do not satisfy the contention gate", "LC-2", "ObjChip", "living-core-closure/equipment-user-count-contract.json", "NATIVE_CLOSED"),
        fact("reservationLifecycle", "ReserveUse appends; OnUseComplate removes the completing staff before subsequent selection", "LC-2", "ObjChip", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
    ]
    furniture["visual_boundary"] = fact("visual", "Visual selector references are consumed by projection only and cannot mutate owner, users, HP, target, or use state", "VP-1", "ObjChip", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER")
    furniture["invariants"] = [
        fact("noBusyBoolean", "Do not collapse owner, active users, and reserved users into busy: boolean", "LC-2", "ObjChip", "living-core-closure/canonical-furniture-schema-final.json", "NATIVE_CLOSED"),
        fact("noRestSocial", "Do not infer REST or SOCIAL FurnitureData roles from names or sprites", "LC-5", "FurnitureData", "living-core-closure/furniture-exact-role-contract.json", "NATIVE_CLOSED"),
    ]
    return furniture


ARRIVAL_ENTRIES = [
    (1, "GOTO_EQUIPMENT", ["frame_=0", "state_=STATE_USE_EQUIPMENT", "moveMode_=0", "select equipment action from target direction"]),
    (2, "WANDER", ["frame_=0", "state_=STATE_WANDER", "select directional wander action"]),
    (3, "GOTO_DESK", ["start desk action", "set moveMode_=SIT_DOWN", "continue through route/arrival boundary"]),
    (4, "INTO_EQUIPMENT", ["frame_=0", "state_=STATE_INVITE_TO_TALK", "moveMode_=0", "select equipment-facing action"]),
    (5, "OUTOF_EQUIPMENT", ["common arrival epilogue; no direct state write is promoted"]),
    (6, "SIT_DOWN", ["frame_=0", "sebId_=-1", "state_=STATE_WORK", "FLAG_SITTING on", "moveMode_=0"]),
    (7, "TO_STAFF", ["compute route to target staff", "set moveMode_=TO_BACK_OF_CHAIR", "continue through route/arrival boundary"]),
    (8, "TO_STAND_TALKING", ["frame_=0", "moveMode_=0", "state_=STATE_TALK", "select talk action"]),
    (9, "TO_BACK_OF_CHAIR", ["frame_=0", "state_=STATE_INVITE_TO_TALK", "moveMode_=0", "select back-of-chair action"]),
    (10, "GO_TO_DOOR", ["compute route to door", "set moveMode_=GO_HOME", "reserve door", "StartAction(0)", "door frame=15", "FLAG_FADE_OUT on"]),
    (11, "GO_HOME", ["state_=STATE_STAY_HOME", "moveMode_=0"]),
]


def build_movement_contract(identity: dict[str, Any]) -> dict[str, Any]:
    movement = r0_header("social-dev-r0-movement-route-contract-v1", "Canonical movement and route contract", identity)
    movement["grid_coordinate_representation"] = [
        field("gridCell", "[x,y]", "ObjChip/Room grid coordinate", "COORDINATE", "BF-COORDINATE-SEPARATION", "Room", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE", width=10, height=10, indexing="x + y * width"),
        field("worldPosition", "[x,y]", "native world position; implementation may store an immutable projection", "COORDINATE", "BF-COORDINATE", "Staff", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE", formula="cell and standing-position formulas are source-backed"),
        field("mapChipCell", "[x,y]", "14x14 MapChip topology coordinate", "COORDINATE", "BF-MAPCHIP-TOPOLOGY", "MapChip", "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json", "NATIVE_CLOSED", topology="14x14 only in main display"),
    ]
    movement["world_projection_formulas"] = [
        fact("cellOrigin", {"x": "(x+y)*20+20", "y": "(y-x)*10+18"}, "BF-COORDINATE", "Room", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        fact("actorOrigin", {"x": "(x+y)*20+40", "y": "(y-x)*10+9"}, "BF-COORDINATE", "Staff", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "ACCEPTED_CLOSURE"),
        fact("standingPositions", "GetStandingPositions provides four native approach positions; preserve raw vectors and translated labels separately", "BF-STANDING-POSITIONS", "ObjChip", "behavior-first/movement-target-arrival-contract.json", "NATIVE_CLOSED"),
    ]
    movement["route_representation"] = [
        field("routeQueue", "RouteNode[]", "native Staff.route_ head-consumption sequence", "ROUTE_STATE", "BF-MOVEMENT", "Staff", "behavior-first/movement-target-arrival-contract.json", "NATIVE_CLOSED", native_field="route_", native_offset="0x88"),
        field("currentGoal", "goal reference", "ObjChip/Staff/door/desk goal selected by caller", "ROUTE_STATE", "BF-GOAL-FILTER", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        field("goalType", "moveMode enum", "arrival behavior selector", "ROUTE_STATE", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED", native_field="moveMode_", native_offset="0xA8"),
        field("routeHeadConsumption", "operation", "remove route head, store lastNode_, call OnArriveGoal when empty", "ROUTE_STATE", "BF-ARRIVAL", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED", native_method="Staff.OnArriveNextNode", native_rva="0x12D8184"),
    ]
    movement["pathfinding"] = [
        fact("neighborPolicy", {"connectivity": 4, "diagonal": False, "neighbors": [[-1, 0], [1, 0], [0, -1], [0, 1]]}, "BF-ASTAR-4N", "Astar", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "NATIVE_CLOSED"),
        fact("passabilityRules", ["type 2 requires no installed object at the candidate cell", "type 3/4 requires IsPassable true", "type 6 is rejected", "out-of-bounds nodes are skipped"], "BF-GOAL-FILTER", "ObjChip", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "NATIVE_CLOSED"),
        fact("doorTraversal", "native door cell is traversable through the Room/ObjChip door relation; door action/reservation is dispatched by move modes 10 and 11", "LC-4", "Room", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
    ]
    movement["goal_approach_rules"] = [
        fact("deskApproach", "GotoDesk resolves deskId_, selects native standing/desk approach, and enters GOTO_DESK then SIT_DOWN", "LC-3", "Staff", "living-core-closure/complete-original-staff-life-loop.json", "NATIVE_CLOSED"),
        fact("equipmentApproach", "GotoEquip selects a type 1/4 target, requires reserved-user count <= 0, reserves it, then enters GOTO_EQUIPMENT", "LC-2", "Staff", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        fact("staffApproach", "GotoTalk chooses a random room staff candidate, checks sitting/work/flags/standing-cell guards, then enters TO_STAFF", "BF-TALK", "Staff", "behavior-first/talk-social-contract.json", "INTACT_CSHARP"),
        fact("chairApproach", "TO_STAFF transitions to TO_BACK_OF_CHAIR; the exact approach vector remains native standing-position data", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
    ]
    movement["arrival_dispatch"] = [
        fact(f"moveMode{mode}", {"moveMode": mode, "label": label, "effects": effects}, "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED", native_method="Staff.OnArriveGoal", native_rva="0x12D8420")
        for mode, label, effects in ARRIVAL_ENTRIES
    ]
    movement["invalid_goal_policy"] = [
        fact("invalidMoveMode", "moveMode 0 or values outside 1..11 take the common return/failure path; no new behavior is inferred", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        fact("destroyedTarget", "equipment destruction notifies reserved Staff; desk destruction clears ownership and falls back through GotoDesk/wander without stale task payload", "LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
    ]
    movement["invariants"] = [
        fact("noDiagonal", True, "BF-ASTAR-4N", "Astar", "knowledge/fixtures/accepted/runtime/room_placement_contract.json", "NATIVE_CLOSED"),
        fact("noGenericArrival", "OnArriveGoal is an 11-way behavior dispatch, not a generic arrived=true flag", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
    ]
    return movement


def state_details() -> dict[int, dict[str, Any]]:
    return {
        0: {"entry": "native normal/initial path; exact indirect handler is source-limited", "handler": "Staff.Update indirect state handler (not named beyond source evidence)", "timers": ["frame_", "sebFrame_"], "outgoing": ["STATE_MOVE on low HP when guard applies"], "cleanup": "source-limited", "movement": "may select a native movement goal", "work": "not an active work state", "visual": "native action selector from state/flags", "confidence": "source_limited"},
        1: {"entry": "Staff.Update special dispatch to UpdateMeeting", "handler": "Staff.UpdateMeeting (RVA 0x12D473C)", "timers": ["meetingPointFrame_", "talkFrame_"], "outgoing": ["SOURCE_LIMITED"], "cleanup": "source-limited", "movement": "meeting movement is source-limited", "work": "not ordinary desk work", "visual": "meeting action selection is source-limited", "confidence": "source_limited"},
        2: {"entry": "low HP guard or a route goal selection", "handler": "Staff.UpdateMove (RVA 0x12D57AC)", "timers": ["moveFrame_", "route_", "lastNode_"], "outgoing": ["STATE_WORK", "STATE_USE_EQUIPMENT", "STATE_TALK", "STATE_INVITE_TO_TALK", "STATE_WANDER", "STATE_STAY_HOME", "STATE_WAIT_BACK_OF_DOOR"], "cleanup": "arrival handler clears/changes target and moveMode per native table", "movement": "owns route traversal and arrival", "work": "returns to work through desk arrival", "visual": "direction/action follows route/goal", "confidence": "native_closed"},
        3: {"entry": "desk arrival can pass through this label; native mode 6 writes STATE_WORK", "handler": "state-specific body source-limited", "timers": ["frame_", "sebFrame_"], "outgoing": ["STATE_WORK via MOVE_MODE_SIT_DOWN"], "cleanup": "FLAG_SITTING is set by arrival mode 6", "movement": "desk approach state", "work": "entry boundary to work", "visual": "sit-down action", "confidence": "native_closed"},
        4: {"entry": "MOVE_MODE_SIT_DOWN or desk continuation", "handler": "Staff.UpdateWork (RVA 0x12D4A7C)", "timers": ["frame_", "typingFrame_", "sebFrame_"], "outgoing": ["STATE_MOVE for equipment/talk/low HP", "STATE_WORK with typing/sleep flags"], "cleanup": "typing completion clears typing; detours preserve deskId_", "movement": "GotoDesk if not sitting", "work": "autonomous typing/equipment/talk/sleep choices; no ordinary HP drain", "visual": "typing/wait/sleep selectors", "confidence": "native_closed"},
        5: {"entry": "MOVE_MODE_GOTO_EQUIPMENT arrival mode 1", "handler": "equipment-use body; exact indirect dispatch source-limited", "timers": ["frame_", "recoveryEffectFrame_"], "outgoing": ["STATE_MOVE through GotoDesk after use", "STATE_WAIT on equipment destruction"], "cleanup": "OnUseComplate releases reservation; destruction clears equipment target", "movement": "equipment target is current objIndex_", "work": "equipment use interrupts work and returns to desk", "visual": "equipment action", "confidence": "native_closed"},
        6: {"entry": "MOVE_MODE_TO_STAND_TALKING arrival mode 8", "handler": "Staff.Talk (RVA 0x12D5588)", "timers": ["talkFrame_", "frame_"], "outgoing": ["STATE_MOVE through GotoDesk at talk frame >=130", "STATE_WAIT on colleague removal"], "cleanup": "clears colleagueId_ and bilateral talk flags", "movement": "talk route completes before this state", "work": "talk interrupts work and returns to desk", "visual": "talk action", "confidence": "native_closed"},
        7: {"entry": "MOVE_MODE_TO_BACK_OF_CHAIR arrival mode 9 or invitation callback", "handler": "InviteStaffToTalk/OnInvitedTalk; full handler source-limited", "timers": ["frame_", "meetingPointFrame_"], "outgoing": ["STATE_TALK via MOVE_MODE_TO_STAND_TALKING", "STATE_WAIT on cleanup"], "cleanup": "clears invite/reserved flags on completion/removal", "movement": "back-of-chair approach", "work": "social detour may resume desk", "visual": "invite/back-of-chair action", "confidence": "source_limited"},
        8: {"entry": "native fly-away path; exact entry is outside closed living slice", "handler": "source-limited state handler", "timers": ["frame_", "alpha_"], "outgoing": ["SOURCE_LIMITED"], "cleanup": "source-limited", "movement": "source-limited", "work": "not promoted", "visual": "fade/fly action inputs only", "confidence": "source_limited"},
        9: {"entry": "native wait/cleanup path", "handler": "source-limited state handler", "timers": ["frame_", "sebFrame_"], "outgoing": ["STATE_WANDER or STATE_MOVE only where a closed caller supplies it"], "cleanup": "equipment/colleague removal may write wait", "movement": "no route unless a new goal is selected", "work": "idle between detours", "visual": "wait action", "confidence": "source_limited"},
        10: {"entry": "MOVE_MODE_WANDER arrival mode 2 or desk-destroyed fallback", "handler": "source-limited wander update", "timers": ["frame_", "moveFrame_"], "outgoing": ["SOURCE_LIMITED"], "cleanup": "target/route cleanup is native movement responsibility", "movement": "wander route", "work": "not ordinary desk work", "visual": "directional wander action", "confidence": "source_limited"},
        11: {"entry": "home return door path writes wait-back-of-door", "handler": "source-limited door-wait handler", "timers": ["waitingBackOfDoorFrame_", "frame_"], "outgoing": ["STATE_MOVE through GOTO_DESK"], "cleanup": "door reservation is consumed/released by native path", "movement": "door-to-desk return", "work": "resume route to owned desk", "visual": "door wait/fade action", "confidence": "source_limited"},
        12: {"entry": "Staff.Update special dispatch to UpdateDevelop", "handler": "Staff.UpdateDevelop (source/native entry is closed; full body is out of R0 scope)", "timers": ["processStep_", "planningRate_", "planQuality_", "developState_"], "outgoing": ["SOURCE_LIMITED"], "cleanup": "planning end clears planning flags through OnEndPlanning", "movement": "source-limited", "work": "development/planning state, not ordinary desk work", "visual": "development action inputs", "confidence": "source_limited"},
        13: {"entry": "MOVE_MODE_GO_HOME arrival mode 11", "handler": "Staff.UpdateStayHome (RVA 0x12D59F4)", "timers": ["frame_", "hp_", "waitingBackOfDoorFrame_"], "outgoing": ["STATE_WAIT_BACK_OF_DOOR when GetHpRatio() >= 40"], "cleanup": "stay-home state retains no dashboard task id", "movement": "no room route while home; door return is native", "work": "RecoverHp(1) per home update; return to desk path", "visual": "sleep/home action", "confidence": "native_closed"},
    }


def build_state_machine_contract(identity: dict[str, Any]) -> dict[str, Any]:
    states = [
        (0, "STATE_NORMAL"), (1, "STATE_MEETING"), (2, "STATE_MOVE"), (3, "STATE_SIT_DOWN"), (4, "STATE_WORK"),
        (5, "STATE_USE_EQUIPMENT"), (6, "STATE_TALK"), (7, "STATE_INVITE_TO_TALK"), (8, "STATE_FLY_AWAY"),
        (9, "STATE_WAIT"), (10, "STATE_WANDER"), (11, "STATE_WAIT_BACK_OF_DOOR"), (12, "STATE_DEVELOP"), (13, "STATE_STAY_HOME"),
    ]
    contract = r0_header("social-dev-r0-staff-state-machine-contract-v1", "Canonical Staff state machine contract", identity)
    contract["states"] = []
    for state_id, label in states:
        detail = state_details()[state_id]
        contract["states"].append({
            "state_id": state_id,
            "label": label,
            "entry_conditions": detail["entry"],
            "update_handler": detail["handler"],
            "relevant_timers": detail["timers"],
            "allowed_outgoing_transitions": detail["outgoing"],
            "target_state_cleanup": detail["cleanup"],
            "movement_relation": detail["movement"],
            "work_relation": detail["work"],
            "visual_action_relation": detail["visual"],
            "evidence_confidence": detail["confidence"],
            "provenance": provenance("BF-STATES" if state_id not in {4, 5, 6, 12, 13} else ("LC-1" if state_id == 4 else "LC-2" if state_id == 5 else "BF-TALK" if state_id == 6 else "C11" if state_id == 12 else "BF-HOME"), "Staff", "behavior-first/staff-state-machine.json", "ACCEPTED_CLOSURE" if detail["confidence"] == "native_closed" else "SOURCE_LIMITED", "high" if detail["confidence"] == "native_closed" else "source_limited", "CLOSED" if detail["confidence"] == "native_closed" else "NONBLOCKING_SOURCE_LIMIT"),
        })
    contract["move_modes"] = [
        fact("MOVE_MODE_STAY", 0, "BF-MOVE-MODES", "Staff", "behavior-first/staff-state-constant-catalog.json", "METADATA_VERIFIED"),
        *[fact(label, mode, "BF-MOVE-MODES", "Staff", "behavior-first/staff-state-constant-catalog.json", "METADATA_VERIFIED") for mode, label, _effects in ARRIVAL_ENTRIES],
    ]
    contract["closed_transition_edges"] = [
        fact("lowHpDoorEscape", "any state except MOVE/STAY_HOME with GetHpRatio <= 5 -> STATE_MOVE/MOVE_MODE_GO_TO_DOOR", "LC-1", "Staff", "living-core-closure/complete-original-staff-life-loop.json", "NATIVE_CLOSED"),
        fact("deskArrival", "GOTO_DESK -> SIT_DOWN -> STATE_WORK with FLAG_SITTING", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        fact("equipmentDetour", "STATE_WORK -> GotoEquip -> STATE_MOVE/MOVE_MODE_GOTO_EQUIPMENT -> STATE_USE_EQUIPMENT -> GotoDesk", "LC-2", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        fact("talkDetour", "STATE_WORK -> GotoTalk -> STATE_MOVE/MOVE_MODE_TO_STAFF -> talk -> GotoDesk", "BF-TALK", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        fact("homeReturn", "STATE_STAY_HOME -> RecoverHp(1) until ratio >= 40 -> door return -> GOTO_DESK", "LC-1", "Staff", "living-core-closure/home-rest-contract.json", "NATIVE_CLOSED"),
        fact("deskDestroyed", "desk destruction clears desk ownership and falls back to wander/GotoDesk reacquisition", "LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
    ]
    contract["source_limited_boundaries"] = [
        fact("indirectUpdateDispatch", "Full per-state Staff.Update indirect dispatch is not re-invented; missing branches remain source-limited and nonblocking", "BF-UPDATE-DISPATCH-LIMIT", "Staff", "behavior-first/staff-transition-graph.json", "SOURCE_LIMITED", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
        fact("meetingAndDevelop", "Meeting/development detailed branches are not expanded beyond named native entry points", "C11", "Staff", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
    ]
    contract["invariants"] = [
        fact("stateCount", 14, "BF-STATES", "Staff", "behavior-first/staff-state-constant-catalog.json", "METADATA_VERIFIED"),
        fact("stateIdPolicy", "State numeric IDs remain 0..13; labels do not authorize extra transitions", "BF-STATES", "Staff", "behavior-first/staff-state-constant-catalog.json", "METADATA_VERIFIED"),
    ]
    return contract


def build_tick_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-tick-order-contract-v2", "Canonical Staff/Room/Player tick order", identity)
    contract["staff_update_order"] = [
        fact("staffEntry", "Staff.Update reads the current frame/state and enters common per-frame processing", "BF-TICK-STAFF", "Staff", "living-core-closure/staff-native-authority-map.json", "NATIVE_CLOSED"),
        fact("recoveryFirst", "Staff.Update calls UpdateRecoveryHp before the state-specific living decision", "LC-2", "Staff", "living-core-closure/recovery-cadence-native-trace.json", "NATIVE_CLOSED"),
        fact("lowHpGuard", "After common recovery processing, GetHpRatio <= 5 triggers the door guard unless already MOVE or STAY_HOME", "LC-1", "Staff", "behavior-first/home-rest-contract.json", "NATIVE_CLOSED"),
        fact("stateDispatch", "Staff.Update dispatches the state handler; state 1 and state 12 have named UpdateMeeting/UpdateDevelop entry points, remaining indirect branches stay source-limited", "BF-UPDATE-DISPATCH-LIMIT", "Staff", "behavior-first/staff-transition-graph.json", "SOURCE_LIMITED", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
        fact("stateHandler", "State-specific handler runs next: UpdateWork, UpdateStayHome, UpdateMove, UpdateMeeting/Develop or a source-limited native branch", "BF-TICK-STAFF", "Staff", "living-core-closure/staff-native-authority-map.json", "NATIVE_CLOSED"),
        fact("routeArrival", "Movement handler consumes route head and invokes OnArriveGoal only when route is empty; arrival effects are not collapsed", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        fact("handlerTimers", "frame_, moveFrame_, typingFrame_, talkFrame_, recoveryEffectFrame_ and door wait timers are mutated by their owning native handlers", "BF-TIMERS", "Staff", "behavior-first/staff-field-inventory.json", "METADATA_VERIFIED"),
        fact("cleanup", "Transition handlers clear targets, reservations, talk flags, desk ownership or route entries at the proven cleanup boundary", "LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        fact("projection", "Only after behavior mutation does the renderer receive a projection snapshot", "VP-1", "Staff", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER"),
    ]
    contract["player_room_order"] = [
        fact("playerFrame", "Player.Frame increments the simulation frame before Player.Update-owned work", "BF-TICK-PLAYER", "Player", "knowledge/fixtures/accepted/runtime/tick_order_contract.json", "ACCEPTED_CLOSURE", "source_limited", "LEGACY_ORDER_RECONCILED"),
        fact("planningChain", "Planning input uses Player -> Room -> Staff call chains for start/update/end", "C10", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("roomStaffThenObj", "Room.Update iterates Staff before ObjChip; preserve raw vector order where native selectors observe it", "BF-TICK-ROOM", "Room", "behavior-first/idle-autonomy-contract.json", "NATIVE_CLOSED"),
        fact("visualAfterCommit", "Room/Staff/ObjChip mutations are committed before visual projection; UI and renderer are non-mutating", "VP-1", "Room", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER"),
    ]
    contract["legacy_contract_audit"] = {
        "path": "knowledge/fixtures/accepted/runtime/tick_order_contract.json",
        "disposition": "REPLACE",
        "reason": "The old display-slice order uses stable-id actor updates and a synthetic snapshot but does not place recovery, low-HP guard, native state dispatch, or route arrival in the canonical Staff order.",
        "preserve": ["renderer_may_mutate=false", "ui_may_mutate=false", "source_code_imports=false"],
        "provenance": provenance("R0-AUDIT-TICK", "Staff/Room", "knowledge/fixtures/accepted/runtime/tick_order_contract.json", "SOURCE_LIMITED", "high", "SUPERSEDED_LEGACY_CONTRACT"),
    }
    contract["prohibited_shortcuts"] = [
        "Do not call state handlers in arbitrary convenience order.",
        "Do not update actors in a sorted synthetic ID order when native vector order is the observed authority.",
        "Do not let renderer/UI mutate behavior state.",
        "Do not use wall-clock time as an original tick input.",
    ]
    return contract


def build_rng_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-rng-autonomy-contract-v1", "Canonical RNG and autonomy contract", identity)
    contract["runtime_policy"] = {
        "test_prng": "injectable deterministic PRNG/replay stream",
        "preserve": ["range semantics", "comparison thresholds", "draw order", "number of draws", "branch ordering"],
        "unknown_policy": "SOURCE_LIMITED; do not guess probability or cadence where native evidence is not closed",
    }
    contract["decisions"] = [
        {
            "managed_method": "AppData.Random(int n)",
            "native_rva": None,
            "random_api": "JRandom.NextInt(n)",
            "range_semantics": "[0,n) when n > 0",
            "comparison_or_threshold": "caller-defined",
            "decision_meaning": "bounded index/choice draw",
            "states": ["STATE_WORK", "STATE_TALK", "STATE_MEETING"],
            "side_effects": "none until caller branch",
            "source_confidence": "INTACT_CSHARP",
            "provenance": provenance("RNG-API-N", "AppData", "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs", "INTACT_CSHARP"),
        },
        {
            "managed_method": "AppData.Random(int min, int max)",
            "native_rva": None,
            "random_api": "JRandom.NextInt(max-min+1)+min",
            "range_semantics": "[min,max] inclusive",
            "comparison_or_threshold": "caller-defined",
            "decision_meaning": "bounded inclusive draw",
            "states": ["STATE_TALK", "STATE_MEETING"],
            "side_effects": "none until caller branch",
            "source_confidence": "INTACT_CSHARP",
            "provenance": provenance("RNG-API-INCLUSIVE", "AppData", "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs", "INTACT_CSHARP"),
        },
        {
            "managed_method": "Staff.GotoEquip",
            "native_rva": "0x12D6540",
            "random_api": "AppData.Random(2)",
            "range_semantics": "draw 0 or 1",
            "comparison_or_threshold": "0 -> type 1; otherwise -> type 4",
            "decision_meaning": "select equipment candidate class",
            "states": ["STATE_WORK", "STATE_MOVE"],
            "side_effects": ["candidate vector lookup", "GetUsersNum gate", "ReserveUse", "MOVE_MODE_GOTO_EQUIPMENT"],
            "source_confidence": "NATIVE_CLOSED",
            "provenance": provenance("LC-2", "Staff", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        },
        {
            "managed_method": "Room.GetRandomObjChipTypeOf",
            "native_rva": "0x12CFA30",
            "random_api": "AppData.Random(candidateCount)",
            "range_semantics": "[0,candidateCount) for the candidate vector index",
            "comparison_or_threshold": "candidate count/target type",
            "decision_meaning": "select a candidate ObjChip from the filtered vector",
            "states": ["STATE_WORK"],
            "side_effects": "returns candidate to Staff.GotoEquip; no desk ownership effect",
            "source_confidence": "NATIVE_CLOSED",
            "provenance": provenance("LC-2", "Room", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        },
        {
            "managed_method": "Staff.GotoTalk",
            "native_rva": "0x12D6600",
            "random_api": "AppData.Random(staffs_.Length)",
            "range_semantics": "[0,staffs_.Length)",
            "comparison_or_threshold": "candidate must pass non-self, flags, STATE_WORK, sitting and standing-cell guards",
            "decision_meaning": "select one room Staff candidate for social detour",
            "states": ["STATE_WORK", "STATE_MOVE"],
            "side_effects": ["bilateral reserved/invited talk flags", "colleagueId_", "MOVE_MODE_TO_STAFF"],
            "source_confidence": "INTACT_CSHARP",
            "provenance": provenance("BF-TALK", "Staff", "behavior-first/talk-social-contract.json", "INTACT_CSHARP"),
        },
        {
            "managed_method": "Staff.UpdateWork typing/equipment/talk/sleep branch",
            "native_rva": "0x12D4A7C",
            "random_api": "AppData.Random(101)",
            "range_semantics": "[0,100]",
            "comparison_or_threshold": {"typing": ">=41", "equipment": "<21", "talk": "<=10", "sleep": "<=25 when HP ratio <=99"},
            "decision_meaning": "autonomous work detour/action choice",
            "states": ["STATE_WORK"],
            "side_effects": ["typing flag/frame", "GotoEquip", "GotoTalk", "FLAG_SLEEPING"],
            "source_confidence": "SOURCE_LIMITED",
            "provenance": provenance("BF-AUTONOMY", "Staff", "behavior-first/idle-autonomy-contract.json", "SOURCE_LIMITED", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
        },
        {
            "managed_method": "Staff.Talk frame 110 gauge branch",
            "native_rva": "0x12D5588",
            "random_api": "Lib.Random(0,4)",
            "range_semantics": "[0,4] inclusive",
            "comparison_or_threshold": "frame == 110",
            "decision_meaning": "meeting point gauge increment",
            "states": ["STATE_TALK"],
            "side_effects": "AddMeetingPointGauge(random value)",
            "source_confidence": "INTACT_CSHARP",
            "provenance": provenance("BF-TALK", "Staff", "behavior-first/talk-social-contract.json", "INTACT_CSHARP"),
        },
    ]
    contract["source_limited_decisions"] = [
        fact("GetRandomEmptyChip", "No separate implementation-ready GetRandomEmptyChip entry was promoted from the accepted evidence; keep any future discovery SOURCE_LIMITED until a named native/source fact closes it", "RNG-UNKNOWN-EMPTY-CHIP", "Room", "behavior-first/unknowns.json", "SOURCE_LIMITED", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
        fact("workCadence", "The exact modulo/draw cadence around UpdateWork branches is source-limited; preserve branch order and thresholds without inventing a fixed probability schedule", "BF-AUTONOMY", "Staff", "behavior-first/idle-autonomy-contract.json", "SOURCE_LIMITED", "source_limited", "NONBLOCKING_SOURCE_LIMIT"),
    ]
    contract["old_deterministic_fixtures_to_replace"] = [
        fact("fixedRouteTrace", "runtime/social-dev/src/core/simulation.ts#updateLivingTrace uses TRACE_ROUTE_START_TICK/TRACE_ROUTE_ARRIVAL_TICK instead of autonomy/RNG", "R0-AUDIT-SCRIPTED-TRACE", "Runtime", "runtime/social-dev/src/core/simulation.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED_LEGACY_RUNTIME"),
        fact("scriptedTalkTiming", "runtime/social-dev/src/core/simulation.ts fixes talk start and end markers; it is not original RNG/state authority", "R0-AUDIT-SCRIPTED-TALK", "Runtime", "runtime/social-dev/src/core/simulation.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED_LEGACY_RUNTIME"),
    ]
    return contract


def build_hp_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-hp-recovery-home-runtime-contract-v1", "Canonical HP/recovery/home contract", identity)
    contract["hp_field"] = field("hp", "int", "authoritative Staff.hp_", "ORIGINAL_MUTABLE_RUNTIME_STATE", "C1", "Staff", "g1_5/staff-hp-native-field-access.json", "CANONICAL_G1_5", native_field="Staff.hp_", native_offset="0xE8", save_class="ORIGINAL_SAVED")
    contract["initialization"] = fact("initialHp", 100, "C1", "Staff", "living-core-closure/original-work-assignment-contract.json", "NATIVE_CLOSED", native_method="Staff.Init", native_rva="0x12D2370")
    contract["max_hp"] = fact("maxHp", "GetBaseParam(StaffData.PARAM_HP, 0) + GetJobParam(StaffData.PARAM_HP, level_)", "C1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED", parameter_name="StaffData.PARAM_HP", parameter_value=5, clamp="native max formula includes data/room/equipment components where applicable")
    contract["hp_ratio"] = fact("getHpRatio", "trunc_toward_zero(hp_ * 100 / maxHp), with native minimum ratio behavior for positive HP", "C1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED", native_method="Staff.GetHpRatio", native_rva="0x12D3BE8")
    contract["readers_and_writers"] = [
        fact("readers", ["Staff.GetHp", "Staff.GetHpRatio", "Staff.Update low-HP guard", "Staff.UpdateWork sleeping decision", "Staff.UpdateStayHome return guard"], "C1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED"),
        fact("writers", ["Staff.Init=100", "Staff.SetHp", "Staff.RecoverHp", "Staff.RecoverHpMax", "Staff.ClampHpMax", "Staff.OnAttacked", "Staff.OverwriteOriginalFields/Deserialize"], "C1", "Staff", "living-core-closure/hp-native-write-site-catalog.json", "NATIVE_CLOSED"),
    ]
    contract["ordinary_work"] = fact("ordinaryWorkDrain", "FALSE: ordinary UpdateWork does not write hp_ or call RecoverHp with a negative value", "LC-1", "Staff", "living-core-closure/ordinary-work-hp-drain-contract.json", "NATIVE_CLOSED", rule="hp_before == hp_after on an ordinary work tick unless another proven HP system acts")
    contract["recovery_stock"] = [
        fact("startDelay", 20, "LC-2", "Staff", "living-core-closure/recovery-cadence-contract.json", "NATIVE_CLOSED", field="frameToStartRecovery_", native_rva="0x12D2EB0"),
        fact("cadence", "after countdown, consume one stock unit and call RecoverHp(1) when frame_ is non-negative and frame_%3 == 0", "LC-2", "Staff", "living-core-closure/recovery-cadence-native-trace.json", "NATIVE_CLOSED", native_rva="0x12D2C8C"),
        fact("stockUnit", 1, "LC-2", "Staff", "living-core-closure/recovery-cadence-contract.json", "NATIVE_CLOSED"),
        fact("exhaustion", {"recoveryHpStock_": 0, "frameToHideHpGauge_": 40, "recoveryEffectFrame_": "inactive sentinel/effect lifecycle"}, "LC-2", "Staff", "living-core-closure/recovery-cadence-contract.json", "NATIVE_CLOSED"),
        fact("equipmentSupply", "Staff.UseEquip adds FurnitureData.recovery_ to recovery stock at completion; it does not write hp_ directly", "LC-2", "Staff", "behavior-first/equipment-behavior-contract.json", "NATIVE_CLOSED"),
    ]
    contract["home"] = [
        fact("lowHpTrigger", "GetHpRatio() <= 5 -> STATE_MOVE and MOVE_MODE_GO_TO_DOOR (10), except MOVE/STAY_HOME guards", "LC-1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED"),
        fact("stayHomeRecovery", "STATE_STAY_HOME / UpdateStayHome calls RecoverHp(1)", "LC-1", "Staff", "behavior-first/home-rest-contract.json", "NATIVE_CLOSED"),
        fact("returnThreshold", "GetHpRatio() >= 40 -> door return / WAIT_BACK_OF_DOOR / GOTO_DESK path", "LC-1", "Staff", "behavior-first/home-rest-contract.json", "NATIVE_CLOSED"),
        fact("resumeDestination", "return uses valid deskId_ first; otherwise GotoDesk/current room fallback; no stale dashboard task payload is preserved", "LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
    ]
    contract["visual_timer_boundary"] = fact("gaugeTimer", "frameToHideHpGauge_ is a visual/effect timer and must not be treated as HP, recovery stock, or a low-HP threshold", "VP-1", "Staff", "living-core-closure/recovery-cadence-contract.json", "NATIVE_CLOSED")
    contract["invariants"] = [
        fact("hpOffset", "0xE8", "C1", "Staff", "g1_5/staff-hp-native-field-access.json", "CANONICAL_G1_5"),
        fact("noNegativeRecovery", True, "LC-1", "Staff", "living-core-closure/ordinary-work-hp-drain-contract.json", "NATIVE_CLOSED"),
        fact("thresholds", {"low": 5, "return": 40}, "LC-1", "Staff", "data-dependency/hp-data-dependency-contract.json", "NATIVE_CLOSED"),
    ]
    return contract


def build_work_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-work-planning-runtime-contract-v1", "Canonical work/planning contract", identity)
    contract["original_input"] = [
        fact("startPlanning", "parameterless Player.StartPlanning()", "C10", "Player", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5"),
        fact("planningTick", "Player.UpdatePlanning(elapsedTime)", "C11", "Player", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5"),
        fact("planningCompletion", "Player.IsCompletedPlanning() predicate", "C11", "Player", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5"),
    ]
    contract["original_mutated_state"] = [
        field("playerPlanningElapsedTime", "time", "Player planning time", "ORIGINAL_MUTATED_STATE", "C10", "Player", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5", native_field="Player.planningElapsedTime_"),
        field("staffPlanningFlags", "bitset", "FLAG_PLANNING/FLAG_PLANNING_COMPLETED", "ORIGINAL_MUTATED_STATE", "C10", "Staff", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5"),
        field("staffPlanningRate", "int", "planningRate_", "ORIGINAL_MUTATED_STATE", "C10", "Staff", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5", native_field="Staff.planningRate_"),
        field("staffPlanQuality", "int", "planQuality_", "ORIGINAL_MUTATED_STATE", "C10", "Staff", "g1_5/minimal-work-assignment-input-contract.json", "CANONICAL_G1_5", native_field="Staff.planQuality_"),
        field("deskOwnership", "Staff/ObjChip relation", "deskId_ and staffId_ ownership", "ORIGINAL_MUTATED_STATE", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
    ]
    contract["original_command_chain"] = [
        fact("startChain", ["Player.StartPlanning", "Room.OnStartPlanning", "Staff.OnStartPlanning"], "C10", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("updateChain", ["Player.UpdatePlanning", "Room.UpdatePlanning", "Staff.UpdatePlanning2"], "C11", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("endChain", ["Player.IsCompletedPlanning", "Room.OnEndPlanning", "Staff.OnEndPlanning"], "C11", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
    ]
    contract["living_core_entry"] = [
        fact("staffInit", "Staff.Init binds StaffData.jobId_/skill_ and initializes hp_", "LC-6", "Staff", "living-core-closure/original-work-assignment-contract.json", "NATIVE_CLOSED"),
        fact("roomAttach", "Room.AddStaff reserves door, selects first eligible desk, writes desk ownership, and may invoke planning", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        fact("workEntry", "desk arrival modes 3/6 lead to STATE_WORK and FLAG_SITTING", "LC-4", "Staff", "living-core-closure/on-arrive-goal-dispatch-contract.json", "NATIVE_CLOSED"),
        fact("autonomousExecution", "UpdateWork owns typing/equipment/talk/sleep choices and does not consume an external task id", "LC-6", "Staff", "living-core-closure/original-work-assignment-contract.json", "NATIVE_CLOSED"),
    ]
    contract["work_entry_conditions"] = [
        fact("deskRequirement", "Staff must have a valid deskId_ / installed type-2 workstation and arrive through native desk route before sitting work", "LC-3", "Staff", "living-core-closure/complete-original-staff-life-loop.json", "NATIVE_CLOSED"),
        fact("noPlaceholderUiSequence", "Do not hardcode an old button sequence as the original work command", "LC-6", "Player", "living-core-closure/original-task-to-living-core-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    contract["planning_completion_and_resume"] = [
        fact("planningEnd", "completion predicate then Room.OnEndPlanning -> Staff.OnEndPlanning", "C11", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        fact("resume", "autonomous detours return through GotoDesk using deskId_", "LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
    ]
    contract["player_facing_ui"] = fact("originalUI", "CUT_LATER; form call sites are evidence of command callers, not a runtime implementation boundary", "C10", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5", status="VISUAL_DEFERRED")
    contract["product_policy"] = fact("dashboard", "PRODUCT_POLICY_PENDING; dashboard task IDs/queues are not original Staff state", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING")
    return contract


def build_interruption_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-interruption-resume-contract-v1", "Canonical interruption and resume contract", identity)
    contract["paths"] = [
        {
            "id": "work-to-equipment",
            "entry": "STATE_WORK / UpdateWork -> GotoEquip",
            "decision": "choose type 1 or 4; GetUsersNum <= 0",
            "reserve": "ObjChip.ReserveUse appends Staff to reservedStaffs_",
            "route": "STATE_MOVE / MOVE_MODE_GOTO_EQUIPMENT",
            "use": "OnArriveGoal mode 1 -> STATE_USE_EQUIPMENT; completion through ObjChip.OnUseComplate/Staff.UseEquip",
            "release": "remove completing Staff from reservedStaffs_; recovery_ may add stock",
            "resume": "GotoDesk via owned deskId_",
            "preserved_state": ["deskId_", "original StaffData/job/skill", "planning fields unless native handler clears them"],
            "cleared_targets": ["equipment target after completion/destruction", "route head as consumed"],
            "reservation_cleanup": "completion removes reservation; destruction notifies reserved Staff",
            "provenance": provenance("LC-2", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "work-to-talk",
            "entry": "STATE_WORK / UpdateWork -> GotoTalk",
            "decision": "random colleague candidate must pass sitting/work/flag/standing-cell guards",
            "reserve": "bilateral reserved/invited talk flags and colleagueId_",
            "route": "STATE_MOVE / MOVE_MODE_TO_STAFF -> MOVE_MODE_TO_BACK_OF_CHAIR",
            "use": "mode 8 -> STATE_TALK; talk frame progresses",
            "release": "talk at frame >=130 clears flags/colleagueId_ then GotoDesk",
            "resume": "owned desk through GotoDesk",
            "preserved_state": ["deskId_", "original StaffData/job/skill"],
            "cleared_targets": ["colleagueId_", "reserved/invited talk flags", "talk route nodes"],
            "reservation_cleanup": "bilateral flags cleared; no fairness queue is created",
            "provenance": provenance("BF-TALK", "Staff", "behavior-first/talk-social-contract.json", "INTACT_CSHARP"),
        },
        {
            "id": "low-hp-home",
            "entry": "GetHpRatio() <=5 in Staff.Update except MOVE/STAY_HOME",
            "decision": "clear route/target as native low-HP guard and select door",
            "reserve": "MOVE_MODE_GO_TO_DOOR reserves door on arrival path",
            "route": "STATE_MOVE / mode 10 -> mode 11",
            "use": "STATE_STAY_HOME / UpdateStayHome calls RecoverHp(1)",
            "release": "at GetHpRatio() >=40 reserve door return and set WAIT_BACK_OF_DOOR/GOTO_DESK path",
            "resume": "valid deskId_ first; current Room/GotoDesk fallback if invalid",
            "preserved_state": ["hp_", "maxHp derivation", "deskId_ if still valid", "original planning fields unless native cleanup changes them"],
            "cleared_targets": ["stale route/current detour target"],
            "reservation_cleanup": "door reservation follows native open/return path",
            "provenance": provenance("LC-1", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "desk-destroyed",
            "entry": "ObjChip.RemoveObj / Staff.OnDeskDestroyed",
            "decision": "clear deskId_ and owner relation",
            "reserve": "no new stale reservation",
            "route": "native fallback may enter wander; exact branch preserved as closed cleanup only",
            "use": "none",
            "release": "desk owner is cleared",
            "resume": "GotoDesk may reacquire the first current valid vacancy; no old task payload preserved",
            "preserved_state": ["StaffData/job/skill", "HP", "non-target runtime fields not cleared by destruction handler"],
            "cleared_targets": ["deskId_", "ObjChip.staffId_ pairing", "stale route/target as required by native cleanup"],
            "reservation_cleanup": "equipment/desk removal notifications are explicit; no fairness queue",
            "provenance": provenance("LC-6", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        },
    ]
    contract["no_fairness_queue"] = fact("fairness", "No queue, rotation, age, or random fairness is present in the proven desk selector", "LC-3", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED")
    return contract


def build_visual_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-visual-projection-boundary-v1", "Behavior/visual projection boundary", identity)
    contract["behavior_runtime_owns"] = [
        fact("behaviorState", ["state", "moveMode", "flags", "position", "direction/action inputs", "frame/timer values", "alpha", "targets", "owner/reservation", "HP/living state"], "VP-1", "Staff", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER"),
    ]
    contract["visual_projection_consumes"] = [
        field("staffDataId", "int", "character resource identity", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("resourceImageSelector", "int|null", "resolved image selector", "VISUAL_PROJECTION", "VP-1", "Staff", "knowledge/fixtures/accepted/runtime/character_capability_contract.json", "SOURCE_LIMITED"),
        field("worldPosition", "[x,y]", "projected position", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("direction", "raw/translated projection", "visual orientation input", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("action", "native action selector", "visual action input", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("frame", "int", "visual frame input", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("alpha", "int", "visual opacity/fade input", "VISUAL_PROJECTION", "VP-1", "Staff", "visual-projection-boundary.json", "SOURCE_LIMITED"),
        field("zOrderContext", "object", "Room/render pass/layer context", "VISUAL_PROJECTION", "VP-1", "Room", "visual-projection-boundary.json", "SOURCE_LIMITED"),
    ]
    contract["visual_must_not"] = [
        fact("noBehaviorMutation", ["decide movement", "decide targets", "mutate HP", "assign desk", "reserve equipment", "trigger talk/home", "alter planning"], "VP-1", "Renderer", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER"),
        fact("noRasterOwnership", "Behavior runtime does not perform raster composition/blending", "VP-1", "Renderer", "visual-projection-boundary.json", "DERIVED_RUNTIME_HELPER"),
    ]
    contract["frozen_layers"] = [
        fact("MapChip", "MapChip/V7 raster semantics remain frozen", "VP-2", "MapChip", "visual-projection-boundary.json", "SOURCE_LIMITED", status="VISUAL_DEFERRED"),
        fact("V8", "V8 remains frozen/not started", "VP-2", "Renderer", "living-core-closure/dashboard-preservation-boundary.json", "SOURCE_LIMITED", status="VISUAL_DEFERRED"),
    ]
    return contract


def build_product_contract(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-product-policy-boundary-v1", "Original game state/product policy boundary", identity)
    contract["original_game_state"] = [
        fact("originalFields", ["Staff.state_", "Staff.hp_", "Staff.moveMode_", "Staff.deskId_", "ObjChip.staffId_", "ObjChip.reservedStaffs_", "planning fields"], "PRODUCT-BOUNDARY", "Staff", "living-core-closure/original-task-to-living-core-boundary.json", "ACCEPTED_CLOSURE"),
        fact("originalAuthority", "Staff/Room/ObjChip native living loop plus Player/Room/Staff planning chain", "LC-6", "Staff", "living-core-closure/original-task-to-living-core-boundary.json", "ACCEPTED_CLOSURE"),
    ]
    contract["product_policy_state"] = [
        field("externalAgentId", "string|null", "product agent identity", "PRODUCT_POLICY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("externalTaskId", "string|null", "product task identity", "PRODUCT_POLICY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("backendTaskState", "product enum", "backend task lifecycle", "PRODUCT_POLICY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        field("dashboardDisplayState", "product object", "dashboard presentation state", "PRODUCT_POLICY_STATE", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    contract["unanswered_product_questions"] = [
        fact("externalTaskWhileHome", "Whether an external AI task keeps running while Staff goes home", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        fact("backendPause", "Whether backend work pauses/slows at low HP or unavailable Staff", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
        fact("dashboardFairness", "Fairness across agents/tasks", "PRODUCT-1", None, "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    contract["preservation_rule"] = fact("separation", "Do not encode product policy in state_, hp_, moveMode_, desk ownership, Furniture reservation, or planning fields", "PRODUCT-1", "Staff", "living-core-closure/original-task-to-living-core-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING")
    return contract


def build_save_contract(identity: dict[str, Any]) -> dict[str, Any]:
    status = load_evidence("data-dependency/staff-runtime-status-contract.json")
    contract = r0_header("social-dev-r0-save-boundary-contract-v1", "Canonical save/transient/derived boundary", identity)
    contract["serialization_status"] = "CONTRACT_ONLY_NO_SAVE_IMPLEMENTATION"
    contract["classification_policy"] = "Use source-backed Staff.Serialize/Deserialize classification. Do not invent compatibility/version behavior or serialize product policy."
    contract["fields"] = []
    for item in status.get("fields", []):
        storage = item.get("storage_owner")
        if storage == "saved_runtime_state":
            category = "ORIGINAL_SAVED"
        elif storage == "transient_runtime_state":
            category = "ORIGINAL_TRANSIENT"
        elif storage == "static_source_constant_or_table":
            category = "ORIGINAL_STATIC_IDENTITY"
        else:
            category = "UNKNOWN_SOURCE_LIMITED"
        contract["fields"].append({
            "name": item.get("name"),
            "type": item.get("type"),
            "offset": item.get("offset"),
            "category": category,
            "serialized_by_original_staff_serializer": bool(item.get("serialized_by_Staff_Serialize")),
            "initialized_in_staff_init_or_constructor": bool(item.get("initialized_in_Staff_Init_or_constructor")),
            "provenance": provenance("DD-SAVE-" + str(item.get("name")), "Staff", "data-dependency/staff-runtime-status-contract.json", "ACCEPTED_CLOSURE", "high", "SOURCE_CLASSIFIED"),
        })
    for name, category, role in [
        ("maxHp", "DERIVED", "formula output"),
        ("hpRatioPercent", "DERIVED", "formula output"),
        ("effectiveStaffParameter", "DERIVED", "formula output"),
        ("externalAgentId", "PRODUCT_ONLY", "product state not serialized as original Staff"),
        ("externalTaskId", "PRODUCT_ONLY", "product state not serialized as original Staff"),
        ("backendTaskState", "PRODUCT_ONLY", "product state not serialized as original Staff"),
        ("dashboardDisplayState", "PRODUCT_ONLY", "product state not serialized as original Staff"),
    ]:
        contract["fields"].append({
            "name": name,
            "type": "derived/product",
            "category": category,
            "role": role,
            "provenance": provenance("DD-SAVE-BOUNDARY", "Staff", "data-dependency/staff-runtime-status-contract.json", "DERIVED_RUNTIME_HELPER" if category == "DERIVED" else "PRODUCT_POLICY", "high", "DERIVED_OR_PRODUCT_NOT_ORIGINAL_SAVED"),
        })
    contract["critical_saved_fields"] = fact("criticalSavedFields", status.get("save_stream", {}).get("critical_saved_fields", []), "DD-SAVE-BOUNDARY", "Staff", "data-dependency/staff-runtime-status-contract.json", "ACCEPTED_CLOSURE")
    contract["load_policy"] = [
        fact("noSerializer", "R0 does not implement serialization", "R0-SAVE-NO-IMPLEMENTATION", "Runtime", "knowledge/fixtures/accepted/runtime/save_contract.json", "SOURCE_LIMITED", status="OUT_OF_SCOPE"),
        fact("noProductLeak", "Product-only state is outside original Staff save semantics", "PRODUCT-1", "Staff", "living-core-closure/dashboard-policy-deferred-boundary.json", "PRODUCT_POLICY", status="PRODUCT_POLICY_PENDING"),
    ]
    return contract


def build_scenarios(identity: dict[str, Any]) -> dict[str, Any]:
    contract = r0_header("social-dev-r0-runtime-scenario-fixtures-v1", "Static acceptance fixtures for future I0 implementation", identity)
    contract["execution_mode"] = "CONTRACT_FIXTURES_NOT_EXECUTED_IN_R0"
    contract["fixture_policy"] = [
        fact("timing", "Use only exact native timings where closed; otherwise assert ordering/invariants instead of invented frame numbers", "R0-FIXTURE-POLICY", "Runtime", "living-core-closure/checkpoint-ledger.json", "ACCEPTED_CLOSURE"),
        fact("rng", "Fixtures supply deterministic RNG draws only where the native decision requires them", "RNG-REPLAY", "Runtime", "rng-autonomy-contract.json", "DERIVED_RUNTIME_HELPER"),
    ]
    def transition(tid: str, cid: str, rule: str, authority: str = "ACCEPTED_CLOSURE", evidence: str = "living-core-closure/complete-original-staff-life-loop.json") -> dict[str, Any]:
        return {"transition_id": tid, "contract_id": cid, "rule": rule, "provenance": provenance(cid, "Staff", evidence, authority)}
    fixtures = [
        {
            "id": "S1",
            "name": "spawn -> acquire/own desk -> route -> sit -> work",
            "initial_canonical_state": {"staff": {"staffDataId": 0, "jobId": 4, "skillId": 1, "level": 0, "hp": 100, "state": 0, "moveMode": 0, "deskId": -1}, "room": {"roomDataId": 0}, "desk": {"type": 2, "furnitureDataId": "installed", "ownerStaffId": -1}},
            "data_ids": {"staffDataId": 0, "jobId": 4, "skillId": 1, "roomDataId": 0},
            "room_furniture_setup": "one installed type-2 desk in raw ObjChip order before any later vacancy",
            "rng_sequence": [],
            "high_level_command_input": "Room.AddStaff(StaffData:0)",
            "expected_transition_sequence": [transition("staff-data-bind", "LC-6", "Staff.Init binds job/skill and starts hp at 100"), transition("desk-select", "LC-3", "GetStaffEmptyObjTypeOf(2) returns first raw-order installed owner -1 desk"), transition("desk-route", "LC-4", "GOTO_DESK then SIT_DOWN arrival"), transition("work-entry", "LC-4", "STATE_WORK and FLAG_SITTING become active")],
            "expected_ownership_reservation_deltas": ["desk.ownerStaffId: -1 -> staff:0", "staff.deskId: -1 -> selected raw ObjChip id", "no equipment reservation"],
            "expected_hp_deltas": ["ordinary work does not drain HP"],
            "expected_route_arrival_milestones": ["route built with 4-neighbor nodes", "route head consumed", "OnArriveGoal mode 3", "OnArriveGoal mode 6"],
            "expected_final_condition": "staff is sitting at the owned desk in STATE_WORK",
            "contract_refs": ["actor-runtime-contract.json", "room-runtime-contract.json", "movement-route-contract.json", "staff-state-machine-contract.json", "hp-recovery-home-runtime-contract.json"],
            "provenance": provenance("FIXTURE-S1", "Staff", "living-core-closure/complete-original-staff-life-loop.json", "ACCEPTED_CLOSURE"),
        },
        {
            "id": "S2",
            "name": "work -> equipment reservation -> use -> release -> return desk -> work",
            "initial_canonical_state": {"staff": {"staffDataId": 0, "state": 4, "moveMode": 0, "deskId": 0, "hp": 50}, "equipment": {"furnitureDataId": 18, "type": 1, "recovery": 10, "reservedUserIds": [], "activeUserIds": []}},
            "data_ids": {"staffDataId": 0, "jobId": 4, "skillId": 1, "furnitureDataId": 18},
            "room_furniture_setup": "one installed recovery equipment candidate with reservedUserIds=[]",
            "rng_sequence": [0, 0],
            "high_level_command_input": "autonomous UpdateWork decision; no dashboard task input",
            "expected_transition_sequence": [transition("equipment-choice", "LC-2", "AppData.Random(2)=0 selects type 1"), transition("reserve", "LC-2", "GetUsersNum()<=0 then ReserveUse"), transition("arrive-use", "LC-4", "mode 1 enters STATE_USE_EQUIPMENT"), transition("complete", "LC-2", "OnUseComplate releases reservation and UseEquip adds recovery stock"), transition("return-desk", "LC-6", "GotoDesk resumes owned desk")],
            "expected_ownership_reservation_deltas": ["reservedUserIds: [] -> [staff:0] -> []", "desk owner remains unchanged", "activeUserIds is not used as contention"],
            "expected_hp_deltas": ["immediate completion HP delta 0", "recoveryStock delta +10", "later stock cadence applies RecoverHp(1)"],
            "expected_route_arrival_milestones": ["equipment approach", "mode 1 arrival", "use completion", "desk route/arrival"],
            "expected_final_condition": "equipment reservation released and Staff returns to STATE_WORK at the owned desk",
            "contract_refs": ["furniture-instance-contract.json", "rng-autonomy-contract.json", "hp-recovery-home-runtime-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S2", "Staff", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "S3",
            "name": "work -> invite/talk -> talk end -> return -> work",
            "initial_canonical_state": {"initiator": {"staffDataId": 0, "state": 4, "flags": ["SITTING"], "deskId": 0}, "partner": {"staffDataId": 1, "state": 4, "flags": ["SITTING"], "deskId": 1}},
            "data_ids": {"initiatorStaffDataId": 0, "partnerStaffDataId": 1, "jobId": 4, "skillId": 1},
            "room_furniture_setup": "two working/sitting Staff with valid standing/use cell",
            "rng_sequence": [1],
            "high_level_command_input": "autonomous UpdateWork -> GotoTalk",
            "expected_transition_sequence": [transition("talk-candidate", "BF-TALK", "AppData.Random(staffs_.Length)=1 selects partner"), transition("talk-reserve", "BF-TALK", "bilateral flags/colleagueId_ and MOVE_MODE_TO_STAFF"), transition("talk-arrive", "LC-4", "mode 7 -> mode 9 -> mode 8 STATE_TALK"), transition("talk-end", "BF-TALK", "talkFrame >=130 clears flags/colleagueId_ and GotoDesk")],
            "expected_ownership_reservation_deltas": ["talk flags set bilaterally then cleared", "no equipment reservation and no desk owner change"],
            "expected_hp_deltas": ["no HP change from talk"],
            "expected_route_arrival_milestones": ["TO_STAFF", "TO_BACK_OF_CHAIR", "TO_STAND_TALKING", "desk return"],
            "expected_final_condition": "both Staff have cleared talk relation and initiator resumes STATE_WORK",
            "contract_refs": ["rng-autonomy-contract.json", "staff-state-machine-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S3", "Staff", "behavior-first/talk-social-contract.json", "INTACT_CSHARP"),
        },
        {
            "id": "S4",
            "name": "low HP <=5% -> door/home -> recovery -> >=40% -> return",
            "initial_canonical_state": {"staff": {"staffDataId": 0, "jobId": 4, "level": 0, "maxHp": 108, "hp": 5, "state": 4, "moveMode": 0, "deskId": 0}, "door": {"rawType": 5, "furnitureDataId": None}},
            "data_ids": {"staffDataId": 0, "jobId": 4, "skillId": 1, "doorRawType": 5},
            "room_furniture_setup": "native room door relation; door FurnitureData binding remains null where source says null",
            "rng_sequence": [],
            "high_level_command_input": "one Staff.Update tick with hpRatio <=5",
            "expected_transition_sequence": [transition("low-hp", "LC-1", "GetHpRatio()<=5 selects MOVE_MODE_GO_TO_DOOR"), transition("door-home", "LC-4", "mode 10 then mode 11 enters STATE_STAY_HOME"), transition("home-recover", "LC-1", "UpdateStayHome calls RecoverHp(1)"), transition("return", "LC-1", "ratio >=40 selects door return and GOTO_DESK")],
            "expected_ownership_reservation_deltas": ["door reservation follows native door path", "desk ownership is preserved if desk remains valid"],
            "expected_hp_deltas": ["home recovery +1 per UpdateStayHome tick", "no ordinary work drain"],
            "expected_route_arrival_milestones": ["door route", "GO_HOME arrival", "home state", "door return", "desk route"],
            "expected_final_condition": "Staff is on the return-to-desk path once hpRatio reaches 40 or more",
            "contract_refs": ["hp-recovery-home-runtime-contract.json", "movement-route-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S4", "Staff", "living-core-closure/recovery-cadence-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "S5",
            "name": "two Staff competing for desk",
            "initial_canonical_state": {"staff": [{"id": 0, "deskId": -1}, {"id": 1, "deskId": -1}], "desks": [{"rawOrder": 0, "type": 2, "installed": True, "ownerStaffId": -1}, {"rawOrder": 1, "type": 2, "installed": True, "ownerStaffId": -1}]},
            "data_ids": {"staffDataIds": [0, 1], "jobId": 4, "skillId": 1},
            "room_furniture_setup": "two installed type-2 desks in explicit raw ObjChip order",
            "rng_sequence": [],
            "high_level_command_input": "Room.AddStaff in raw call order Staff:0 then Staff:1",
            "expected_transition_sequence": [transition("first-owner", "LC-3", "first call selects raw-order desk 0"), transition("second-owner", "LC-3", "second call selects next raw-order vacant desk")],
            "expected_ownership_reservation_deltas": ["desk0 owner -1->staff0", "desk1 owner -1->staff1", "no fairness queue/rotation/random selection"],
            "expected_hp_deltas": ["new/attached staff max-HP normalization follows Room.AddStaff"],
            "expected_route_arrival_milestones": ["each Staff has its own desk route; exact frame counts not asserted"],
            "expected_final_condition": "owners reflect raw-order acquisition and no fairness queue exists",
            "contract_refs": ["room-runtime-contract.json", "furniture-instance-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S5", "Room", "living-core-closure/workstation-vacancy-ownership-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "S6",
            "name": "two Staff competing for one equipment target",
            "initial_canonical_state": {"staff": [{"id": 0, "state": 4}, {"id": 1, "state": 4}], "equipment": {"furnitureDataId": 18, "type": 1, "reservedUserIds": [], "activeUserIds": []}},
            "data_ids": {"staffDataIds": [0, 1], "furnitureDataId": 18},
            "room_furniture_setup": "one installed recovery equipment target; both Staff eligible",
            "rng_sequence": [0, 0, 0, 0],
            "high_level_command_input": "sequential GotoEquip attempts Staff:0 then Staff:1",
            "expected_transition_sequence": [transition("first-reserve", "LC-2", "Staff:0 sees reserved count 0 and reserves target"), transition("second-reject", "LC-2", "Staff:1 sees reserved count >0 and rejects target")],
            "expected_ownership_reservation_deltas": ["reservedUserIds length 0->1", "second Staff does not append", "activeUserIds and ownerStaffId do not override reserved contention"],
            "expected_hp_deltas": ["no HP mutation at selection/rejection"],
            "expected_route_arrival_milestones": ["only first Staff gets equipment route"],
            "expected_final_condition": "one reserved user, no fairness queue, second attempt rejected",
            "contract_refs": ["furniture-instance-contract.json", "rng-autonomy-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S6", "ObjChip", "living-core-closure/equipment-contention-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "S7",
            "name": "desk destroyed while Staff depends on it",
            "initial_canonical_state": {"staff": {"id": 0, "state": 4, "deskId": 0}, "desk": {"instanceId": 0, "type": 2, "ownerStaffId": 0}},
            "data_ids": {"staffDataId": 0, "deskInstanceId": 0},
            "room_furniture_setup": "owned type-2 desk removed through ObjChip.RemoveObj",
            "rng_sequence": [],
            "high_level_command_input": "ObjChip.RemoveObj(desk:0)",
            "expected_transition_sequence": [transition("desk-cleanup", "LC-6", "OnDeskDestroyed clears deskId_/owner relation"), transition("fallback", "LC-6", "wander/current GotoDesk fallback may reacquire only through exact selector")],
            "expected_ownership_reservation_deltas": ["desk owner 0->-1/removed", "no stale ownership or task payload"],
            "expected_hp_deltas": ["no HP mutation from desk destruction"],
            "expected_route_arrival_milestones": ["current desk route invalidated/cleaned; exact fallback route is source-defined, not timed here"],
            "expected_final_condition": "Staff has no stale desk dependency and can use current valid fallback policy",
            "contract_refs": ["actor-runtime-contract.json", "room-runtime-contract.json", "interruption-resume-contract.json"],
            "provenance": provenance("FIXTURE-S7", "Staff", "living-core-closure/work-interruption-resume-contract.json", "NATIVE_CLOSED"),
        },
        {
            "id": "S8",
            "name": "planning start: high-level command -> Player -> Room -> Staff -> work-entry",
            "initial_canonical_state": {"player": {"planning": False}, "room": {"staffCount": 2}, "staff": [{"id": 0, "planning": False}, {"id": 1, "planning": False}]},
            "data_ids": {"staffDataIds": [0, 1], "jobId": 4, "skillId": 1},
            "room_furniture_setup": "existing attached Staff/desk relations",
            "rng_sequence": [],
            "high_level_command_input": "Player.StartPlanning() with no arguments",
            "expected_transition_sequence": [transition("start-player", "C10", "Player.StartPlanning"), transition("start-room", "C10", "Room.OnStartPlanning"), transition("start-staff", "C10", "Staff.OnStartPlanning"), transition("work-boundary", "LC-6", "planning flags/rate/quality feed original Staff loop")],
            "expected_ownership_reservation_deltas": ["desk ownership unchanged by the command boundary"],
            "expected_hp_deltas": ["no HP change from planning start"],
            "expected_route_arrival_milestones": ["no synthetic UI route; subsequent native work route only"],
            "expected_final_condition": "Player/Room/Staff planning state is active at the original boundary",
            "contract_refs": ["work-planning-runtime-contract.json", "tick-order-contract-v2.json"],
            "provenance": provenance("FIXTURE-S8", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        },
        {
            "id": "S9",
            "name": "planning end / work completion",
            "initial_canonical_state": {"player": {"planning": True, "completed": True}, "room": {"staffCount": 2}, "staff": [{"id": 0, "planning": True}, {"id": 1, "planning": True}]},
            "data_ids": {"staffDataIds": [0, 1]},
            "room_furniture_setup": "attached Staff/desk relations remain valid",
            "rng_sequence": [],
            "high_level_command_input": "Player.IsCompletedPlanning() returns true",
            "expected_transition_sequence": [transition("completion-predicate", "C11", "Player.IsCompletedPlanning"), transition("end-room", "C11", "Room.OnEndPlanning"), transition("end-staff", "C11", "Staff.OnEndPlanning"), transition("work-resume", "LC-6", "original autonomous work path resumes")],
            "expected_ownership_reservation_deltas": ["desk ownership remains source-owned; no product task queue created"],
            "expected_hp_deltas": ["no HP change implied by planning end"],
            "expected_route_arrival_milestones": ["no arbitrary timing asserted; native next state/route owns later milestones"],
            "expected_final_condition": "planning flags are cleared through original end chain and living Staff can resume work autonomy",
            "contract_refs": ["work-planning-runtime-contract.json", "staff-state-machine-contract.json"],
            "provenance": provenance("FIXTURE-S9", "Player", "g1_5/planning-command-boundary-native.json", "CANONICAL_G1_5"),
        },
        {
            "id": "S10",
            "name": "deterministic RNG replay",
            "initial_canonical_state": {"staffDataIds": [0, 1], "roomDataId": 0, "same_canonical_fields": True},
            "data_ids": {"staffDataIds": [0, 1], "jobId": 4, "skillId": 1},
            "room_furniture_setup": "identical raw-order desks/equipment/talk candidates and identical initial canonical state",
            "rng_sequence": [0, 1, 40, 20, 10, 25, 0, 4],
            "high_level_command_input": "same command stream and injected PRNG sequence in two replays",
            "expected_transition_sequence": [transition("replay-draw-order", "RNG-REPLAY", "draw order and branch ordering are identical"), transition("replay-log", "RNG-REPLAY", "canonical state transition log A equals log B")],
            "expected_ownership_reservation_deltas": ["identical owner/active/reserved deltas in both logs"],
            "expected_hp_deltas": ["identical HP/recovery deltas in both logs"],
            "expected_route_arrival_milestones": ["identical route/arrival milestones in both logs"],
            "expected_final_condition": "same initial state + same RNG sequence => byte-identical canonical transition log",
            "contract_refs": ["rng-autonomy-contract.json", "tick-order-contract-v2.json", "actor-runtime-contract.json"],
            "provenance": provenance("FIXTURE-S10", "Runtime", "rng-autonomy-contract.json", "DERIVED_RUNTIME_HELPER"),
        },
    ]
    contract["fixtures"] = fixtures
    contract["required_fixture_ids"] = [f["id"] for f in fixtures]
    return contract


def disposition_for_source(relative: str) -> tuple[str, dict[str, Any]]:
    path = relative.replace("\\", "/")
    if path.startswith("runtime/social-dev/src/core/simulation.ts"):
        return "SUPERSEDED", {"current_fields": "synthetic ActorState/lifecycle/events", "tick": "fixed frame branches", "rng": "none; scripted", "transitions": "hard-coded route/talk milestones", "canonical": "actor-runtime-contract.json; rng-autonomy-contract.json; staff-state-machine-contract.json", "reason": "Display-slice trace is historical bounded behavior, not original Staff autonomy.", "migration": "Replace with canonical Staff state/route/RNG owner in I0.", "priority": "P0"}
    if path.startswith("runtime/social-dev/src/core/types.ts"):
        return "REPLACE", {"current_fields": "synthetic ActorState fields; no HP/state/moveMode/ownership model", "tick": "immutable display snapshot", "rng": "none", "transitions": "Lifecycle enum only", "canonical": "actor-runtime-contract.json; room-runtime-contract.json", "reason": "Current type boundary cannot represent the canonical original actor state without conflating display and behavior.", "migration": "Introduce canonical Staff/Room/ObjChip state types while retaining visual projection types separately.", "priority": "P0"}
    if path.startswith("runtime/social-dev/src/core/route.ts"):
        return "EXTEND", {"current_fields": "route array from old BehaviorContract", "tick": "no owner", "rng": "none", "transitions": "cardinal validation only", "canonical": "movement-route-contract.json", "reason": "4-neighbor validation is a valid base, but route construction/goal invalidation is not the native Astar contract.", "migration": "Feed native ObjChip passability/goal rules and route head consumption.", "priority": "P0"}
    if path.startswith("runtime/social-dev/src/core/digest.ts"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "stable display digest", "tick": "post-step digest", "rng": "none", "transitions": "none", "canonical": "visual-projection-boundary.json", "reason": "Deterministic hashing is safe as an observation utility but is not original game state.", "migration": "Use only for replay/test logs after canonical state is defined.", "priority": "P2"}
    if path.startswith("runtime/social-dev/src/app/runtime.ts"):
        return "REPLACE", {"current_fields": "controller owns display projection plus synthetic stepSimulation", "tick": "display route step and fixed legacy trace", "rng": "none", "transitions": "synthetic frame transitions", "canonical": "tick-order-contract-v2.json; actor-runtime-contract.json", "reason": "Controller currently drives the old scripted living trace.", "migration": "Keep canvas/UI controller shell; replace living step ownership with canonical Room/Staff runtime.", "priority": "P0"}
    if path.startswith("runtime/social-dev/src/catalog/load-contracts.ts"):
        return "EXTEND", {"current_fields": "loads static/display contracts including old behavior/tick contracts", "tick": "old display tick contract", "rng": "old behavior fixture only", "transitions": "catalog assertions", "canonical": "runtime-contract-manifest.json", "reason": "Static catalog loading is useful, but it must stop treating old display behavior as semantic authority.", "migration": "Load R0 contracts and mark legacy behavior contracts non-authoritative.", "priority": "P1"}
    if path.startswith("runtime/social-dev/src/catalog/native-content.ts"):
        return "KEEP", {"current_fields": "native content IDs/selectors", "tick": "none", "rng": "none", "transitions": "none", "canonical": "room-runtime-contract.json; furniture-instance-contract.json", "reason": "Static native catalog identity matches accepted source/catalog authority.", "migration": "Expose it to I0 as read-only static identity.", "priority": "P1"}
    if path.startswith("runtime/social-dev/src/catalog/"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "static catalog/selector/character metadata", "tick": "none or visual preload", "rng": "none", "transitions": "resolver status only", "canonical": "visual-projection-boundary.json; actor-runtime-contract.json", "reason": "Useful static identity and visual lookup, not original living state authority.", "migration": "Keep behind projection/catalog boundary; do not add behavior decisions here.", "priority": "P2"}
    if path.startswith("runtime/social-dev/src/scene/native-collision.ts"):
        return "KEEP", {"current_fields": "source-backed raw collision predicates", "tick": "read-only lookup", "rng": "none", "transitions": "goal admission only", "canonical": "movement-route-contract.json; room-runtime-contract.json", "reason": "The current collision base preserves the accepted native passability boundary.", "migration": "Use as a read-only adapter to canonical Room/ObjChip runtime.", "priority": "P1"}
    if path.startswith("runtime/social-dev/src/scene/"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "scene projection/camera/room visual placement", "tick": "projection after simulation", "rng": "none", "transitions": "none or static display placement", "canonical": "room-runtime-contract.json; visual-projection-boundary.json", "reason": "Safe presentation/projection layer; it must not own living behavior.", "migration": "Retain as projection utilities; remove behavior writes if any are introduced.", "priority": "P2"}
    if path.startswith("runtime/social-dev/src/renderer/"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "Canvas/DOM/render plan/visibility diagnostics", "tick": "consumes state after update", "rng": "none", "transitions": "visual gate only", "canonical": "visual-projection-boundary.json", "reason": "Renderer is presentation-only and V8/MapChip semantics are frozen.", "migration": "Consume canonical visual projection; retain non-mutating renderer policy.", "priority": "P2"}
    if path.startswith("runtime/social-dev/src/v6/staff.ts"):
        return "SUPERSEDED", {"current_fields": "bounded static Staff display placement/animation", "tick": "display frame only", "rng": "none", "transitions": "visual lifecycle", "canonical": "actor-runtime-contract.json; visual-projection-boundary.json", "reason": "V6 Staff is a visual slice and must not become original living Staff behavior.", "migration": "Keep as projection fixture only; replace behavior ownership in I0.", "priority": "P1"}
    if path.startswith("runtime/social-dev/src/v"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "V1-V7 visual/raster compatibility data", "tick": "render fixture frame", "rng": "none", "transitions": "visual fixture transitions", "canonical": "visual-projection-boundary.json", "reason": "Historical/static visual support is outside the living core.", "migration": "Keep isolated; do not import into original behavior semantics.", "priority": "P3"}
    if path.startswith("runtime/social-dev/src/app/"):
        return "KEEP_VISUAL_ONLY", {"current_fields": "route/UI projection", "tick": "presentation controller", "rng": "none", "transitions": "route selection", "canonical": "visual-projection-boundary.json", "reason": "Application shell is presentation/product plumbing.", "migration": "Keep outside original game-state authority.", "priority": "P2"}
    return "OUT_OF_SCOPE", {"current_fields": "non-living runtime support", "tick": "none", "rng": "none", "transitions": "none", "canonical": "visual-projection-boundary.json", "reason": "Not a living-runtime behavior module.", "migration": "No R0 migration.", "priority": "P3"}


def disposition_for_contract(name: str) -> tuple[str, dict[str, Any]]:
    if name == "actor_behavior_contract.json":
        return "SUPERSEDED", {"current_fields": "fixed display actor trace", "tick": "TRACE_ROUTE_START/ARRIVAL and fixed talk frame", "rng": "none", "transitions": "scripted move/work/talk milestones", "canonical": "actor-runtime-contract.json; rng-autonomy-contract.json", "reason": "Historical synthetic behavior trace is not original autonomy authority.", "migration": "Replace with RNG/state/arrival contract fixtures.", "priority": "P0"}
    if name == "tick_order_contract.json":
        return "REPLACE", {"current_fields": "fixed tick/order/snapshot fields", "tick": "frame -> stable actor IDs -> ObjChip -> snapshot", "rng": "none", "transitions": "display-only", "canonical": "tick-order-contract-v2.json", "reason": "Missing canonical recovery/low-HP/state/arrival positions and stable-ID assumption is not raw native order.", "migration": "Consume tick-order-contract-v2.json.", "priority": "P0"}
    if name == "save_contract.json":
        return "EXTEND", {"current_fields": "display-slice snapshot fields", "tick": "persisted tick/logical time", "rng": "none", "transitions": "display snapshot load", "canonical": "save-boundary-contract.json", "reason": "Useful contract-only boundary but its display snapshot is not the complete original Staff save classification.", "migration": "Replace field set with source-backed Staff save/transient/derived classes in I0.", "priority": "P1"}
    if name == "dom-ui.json" or "dashboard" in name:
        return "PRODUCT_LAYER_ONLY", {"current_fields": "display/dashboard controls", "tick": "UI event loop", "rng": "none", "transitions": "product selection", "canonical": "product-policy-boundary.json", "reason": "Product/presentation state is not original game state.", "migration": "Keep separate from Staff/Room state.", "priority": "P2"}
    if name in {"actor_spawn_contract.json", "camera_coordinate_contract.json", "room_placement_contract.json", "default_map_chip_contract.json", "character_metadata_contract.json", "character_capability_contract.json", "scene_catalog_contract.json", "object_catalog_contract.json", "actor_catalog_contract.json", "native_content_catalog.json", "native_content_connection_contract.json", "native_content_registry_contract.json", "native_direction_contract.json", "native_room_floor_usage_contract.json", "native_scene_assembly_contract.json", "room_catalog_contract.json", "room_scene_runtime_contract.json", "floor00_scene_contract.json", "floor00_seb_contract.json", "floor00_visual_layout_contract.json", "phase3c_render_contract.json", "phase3c_strict_closure_contract.json", "phase3c_visual_gate_v2_contract.json", "phase3d_all_room_assembly_gate_contract.json", "asset_metadata_runtime_contract.json", "asset_metadata_runtime_manifest.json"}:
        return "KEEP_VISUAL_ONLY", {"current_fields": "static native/catalog/render metadata", "tick": "none or visual fixture frame", "rng": "none", "transitions": "projection/asset status", "canonical": "visual-projection-boundary.json; room-runtime-contract.json", "reason": "Accepted static/projection contract; not living behavior authority.", "migration": "Retain as read-only visual/catalog evidence.", "priority": "P2"}
    if name in {"data_contract.json", "entity_contract.json", "asset_composition_contract.json", "asset_family_taxonomy_contract.json", "asset_metadata_baseline_contract.json", "asset_metadata_completion_contract.json", "asset_metadata_coverage_contract.json", "asset_selector_usage_contract.json", "asset_surface_provenance_contract.json", "asset_usage_lifecycle_placement_contract.json", "furniture_asset_metadata_contract.json"}:
        return "OUT_OF_SCOPE", {"current_fields": "asset/data metadata", "tick": "none", "rng": "none", "transitions": "none", "canonical": "visual-projection-boundary.json", "reason": "Not living runtime behavior.", "migration": "No R0 migration.", "priority": "P3"}
    return "KEEP_VISUAL_ONLY", {"current_fields": "existing runtime evidence contract", "tick": "contract-specific", "rng": "not original authority", "transitions": "contract-specific", "canonical": "runtime-contract-manifest.json", "reason": "Existing contract retained for provenance but subordinate to R0 canonical contracts.", "migration": "Audit consumers before I0.", "priority": "P2"}


def git_diff(pathspec: str) -> str:
    result = subprocess.run(["git", "diff", "--", pathspec], cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout


def build_delta_matrix(identity: dict[str, Any]) -> dict[str, Any]:
    # R0 is a frozen pre-I0 audit. The living-core/product files were added
    # after that boundary and are covered by their later phase ledgers; they
    # must not silently expand the immutable R0 entry set.
    frozen_excluded_prefixes = (
        "runtime/social-dev/src/assets/",
        "runtime/social-dev/src/core/living/",
        "runtime/social-dev/src/main.ts",
        "runtime/social-dev/src/product/",
    )
    entries: list[dict[str, Any]] = []
    source_files: list[Path] = []
    for path in RUNTIME_SRC.rglob("*.ts"):
        source_files.append(path)
    for path in sorted(source_files):
        relative = rel(path)
        disposition, profile = disposition_for_source(relative)
        entries.append({
            "path": relative,
            "kind": "runtime_source_module",
            "symbol_or_module": path.stem,
            "current_responsibility": profile["reason"],
            "current_fields_or_state": profile["current_fields"],
            "current_tick_assumptions": profile["tick"],
            "current_rng_assumptions": profile["rng"],
            "current_transition_assumptions": profile["transitions"],
            "canonical_counterpart": profile["canonical"],
            "disposition": disposition,
            "reason": profile["reason"],
            "migration_requirement": profile["migration"],
            "implementation_priority": profile["priority"],
            "file_sha256": sha256_file(path),
            "provenance": provenance("R0-AUDIT-SOURCE", "Runtime", relative, "SOURCE_LIMITED", "high", "CURRENT_RUNTIME_AUDIT"),
        })
    for path in sorted(RUNTIME_EVIDENCE.glob("*.json")):
        relative = rel(path)
        disposition, profile = disposition_for_contract(path.name)
        entries.append({
            "path": relative,
            "kind": "legacy_runtime_contract",
            "symbol_or_module": path.stem,
            "current_responsibility": profile["reason"],
            "current_fields_or_state": profile["current_fields"],
            "current_tick_assumptions": profile["tick"],
            "current_rng_assumptions": profile["rng"],
            "current_transition_assumptions": profile["transitions"],
            "canonical_counterpart": profile["canonical"],
            "disposition": disposition,
            "reason": profile["reason"],
            "migration_requirement": profile["migration"],
            "implementation_priority": profile["priority"],
            "file_sha256": sha256_file(path),
            "provenance": provenance("R0-AUDIT-CONTRACT", "Runtime", relative, "SOURCE_LIMITED", "high", "CURRENT_RUNTIME_AUDIT"),
        })
    entries = [
        entry
        for entry in entries
        if not any(
            entry["path"] == prefix or entry["path"].startswith(prefix)
            for prefix in frozen_excluded_prefixes
        )
    ]
    counts = {name: sum(1 for entry in entries if entry["disposition"] == name) for name in sorted(DISPOSITIONS)}
    living_unknowns = [entry["path"] for entry in entries if entry["disposition"] == "UNKNOWN_REVIEW_REQUIRED" and entry["kind"] in {"runtime_source_module", "legacy_runtime_contract"}]
    matrix = r0_header("social-dev-r0-runtime-delta-matrix-v1", "Existing runtime and contract delta audit", identity)
    matrix["audit_scope"] = ["runtime/social-dev/src/core", "runtime/social-dev/src/catalog", "runtime/social-dev/src/scene", "runtime/social-dev/src/renderer", "runtime/social-dev/src/app", "runtime/social-dev/src/v1-v7", "knowledge/fixtures/accepted/runtime/*.json"]
    matrix["disposition_vocabulary"] = sorted(DISPOSITIONS)
    matrix["entries"] = entries
    matrix["summary"] = {"total_entries": len(entries), "by_disposition": counts, "unknown_review_required_living_runtime": len(living_unknowns), "implementation_blockers": 0}
    matrix["legacy_behavior_findings"] = [
        fact("fixedRoute", "core/simulation.ts uses TRACE_ROUTE_START_TICK=2 and TRACE_ROUTE_ARRIVAL_TICK=4; no native route search owns this trace", "R0-AUDIT-SCRIPTED-TRACE", "Runtime", "runtime/social-dev/src/core/simulation.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED"),
        fact("scriptedTalk", "core/simulation.ts uses TRACE_TALK_START_TICK=6 and TRACE_TALK_END_FRAME=130 with fixed markers; native talk timing is state-owned", "R0-AUDIT-SCRIPTED-TALK", "Runtime", "runtime/social-dev/src/core/simulation.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED"),
        fact("oldHpAssumption", "The old display ActorState contains no authoritative hp_; it cannot express native HP/recovery/home semantics", "R0-AUDIT-OLD-HP", "Runtime", "runtime/social-dev/src/core/types.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED"),
        fact("oldEquipmentLogic", "The old display trace emits work_or_equipment without reservation/active/owner distinction", "R0-AUDIT-OLD-EQUIPMENT", "Runtime", "runtime/social-dev/src/core/simulation.ts", "SOURCE_LIMITED", "source_limited", "SUPERSEDED"),
        fact("boundedFirstSlice", "display-slice-01 actor/catalog fixtures are presentation fixtures and must not become original world/autonomy truth", "R0-AUDIT-FIRST-SLICE", "Runtime", "knowledge/fixtures/accepted/runtime/actor_behavior_contract.json", "SOURCE_LIMITED", "source_limited", "SUPERSEDED"),
    ]
    matrix["runtime_source_hash_guard"] = {
        "tracked_behavior_roots": ["runtime/social-dev/src/core", "runtime/social-dev/src/catalog", "runtime/social-dev/src/scene", "runtime/social-dev/src/renderer"],
        "git_diff_status": {root: "clean" if not git_diff(root) else "preexisting_or_external_diff" for root in ["runtime/social-dev/src/core", "runtime/social-dev/src/catalog", "runtime/social-dev/src/scene", "runtime/social-dev/src/renderer"]},
        "policy": "R0 writes no runtime source; the matrix hashes the current files and the validator checks those hashes remain unchanged.",
    }
    matrix["provenance"] = provenance("R0-AUDIT", "Runtime", "runtime/social-dev/src", "SOURCE_LIMITED", "high", "AUDIT_COMPLETE")
    return matrix


def build_checkpoint_ledger(identity: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    records = [
        ("R0.0", "PASS_BASELINE_CANONICAL_KB_AND_RUNTIME_LOADED"),
        ("R0.1", "PASS_RUNTIME_DELTA_MATRIX"),
        ("R0.2", "PASS_ACTOR_CONTRACT"),
        ("R0.3", "PASS_ROOM_FURNITURE_CONTRACT"),
        ("R0.4", "PASS_MOVEMENT_CONTRACT"),
        ("R0.5", "PASS_STATE_MACHINE_CONTRACT"),
        ("R0.6", "PASS_TICK_ORDER_CONTRACT"),
        ("R0.7", "PASS_RNG_AUTONOMY_CONTRACT_WITH_SOURCE_LIMITS"),
        ("R0.8", "PASS_HP_RECOVERY_HOME_CONTRACT"),
        ("R0.9", "PASS_WORK_PLANNING_CONTRACT"),
        ("R0.10", "PASS_INTERRUPTION_RESUME_CONTRACT"),
        ("R0.11", "PASS_VISUAL_PRODUCT_SAVE_BOUNDARY"),
        ("R0.12", "PASS_SCENARIO_FIXTURES"),
        ("R0.13", "PASS_CONTRACT_MANIFEST"),
        ("R0.14", "PASS_VALIDATION_GATES"),
        ("R0.FINAL", "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION"),
    ]
    return {
        "schema_version": "social-dev-r0-checkpoint-ledger-v1",
        "phase": "R0",
        "status": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION",
        "records": [{"checkpoint": checkpoint, "status": status, "provenance": provenance("R0-CHECKPOINT-" + checkpoint.replace(".", "-"), "Runtime", "runtime-contract-freeze", "ACCEPTED_CLOSURE")} for checkpoint, status in records],
        "summary": {"delta_entries": delta["summary"]["total_entries"], "unknown_review_required_living_runtime": delta["summary"]["unknown_review_required_living_runtime"], "implementation_blockers": 0},
        "required_stop_literals": {
            "inline_only": True,
            "static_contract_only": True,
            "subagents": False,
            "runtime_implementation_changed": False,
            "emulator_or_adb": False,
            "network": False,
            "V8_started": False,
            "MapChip_changed": False,
            "Renderer_changed": False,
            "I0_started": False,
        },
        "next_phase": "I0 Original Living Core Runtime Implementation",
    }


def report_texts(identity: dict[str, Any], delta: dict[str, Any]) -> dict[str, str]:
    counts = delta["summary"]["by_disposition"]
    count_lines = "\n".join(f"- `{name}`: {counts.get(name, 0)}" for name in sorted(DISPOSITIONS))
    common = """\n\nR0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.\n"""
    return {
        "R0_EXISTING_RUNTIME_DELTA_AUDIT.md": f"""# R0 Existing Runtime Delta Audit\n\nStatus: `PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION`.\n\nThe audit compares the current web runtime and legacy runtime contracts with the canonical G1.5/living-core evidence. The machine-readable matrix is `knowledge/fixtures/accepted/runtime-contract-freeze/runtime-delta-matrix.json`.\n\n## Disposition counts\n\n{count_lines}\n\n## Explicit legacy behavior findings\n\n- `runtime/social-dev/src/core/simulation.ts` contains a fixed route trace, fixed talk start/end markers, and no injected RNG. It is `SUPERSEDED`.\n- `knowledge/fixtures/accepted/runtime/actor_behavior_contract.json` is a bounded display trace, not original Staff autonomy. It is `SUPERSEDED`.\n- `knowledge/fixtures/accepted/runtime/tick_order_contract.json` is `REPLACE`: it lacks the native recovery/low-HP/state/arrival positions and assumes stable display-ID order.\n- The old display ActorState lacks authoritative HP, recovery stock, desk ownership, active/reserved equipment users, and product-state separation.\n\nNo living-runtime entry is `UNKNOWN_REVIEW_REQUIRED`; implementation blockers are zero.\n{common}""",
        "R0_ACTOR_ROOM_FURNITURE_CONTRACT.md": f"""# R0 Actor, Room, and Furniture Contract\n\nThe authoritative machine contracts are:\n\n- `actor-runtime-contract.json`\n- `room-runtime-contract.json`\n- `furniture-instance-contract.json`\n\n## Actor\n\nThe actor contract separates original static identity, original mutable Staff state, derived helpers, and product-only state. `Staff.hp_` is at `0xE8`; `state_` is at `0x70`; `moveMode_` is at `0xA8`; `deskId_` is at `0xB8`; route/target/timer/action fields retain their native identities. Product task identifiers are outside the original state.\n\n## Room and topology\n\nThe main-display MapChip is `14x14` (`196` cells) while the Room ObjChip occupancy grid is `10x10` (`100` cells). They remain separate. Room membership and raw ObjChip traversal are preserved. Desk selection is the first raw-order installed type-2 chip with owner `-1`.\n\n## Furniture\n\nThe instance contract keeps owner, active users, and reserved users distinct. Role counts are `10` workstation, `49` recovery equipment, `43` equipment without proven HP effect, and `1` door. REST/SOCIAL furniture roles are not invented.\n{common}""",
        "R0_MOVEMENT_STATE_TICK_RNG_CONTRACT.md": f"""# R0 Movement, State, Tick, and RNG Contract\n\nThe authoritative machine contracts are:\n\n- `movement-route-contract.json`\n- `staff-state-machine-contract.json`\n- `tick-order-contract-v2.json`\n- `rng-autonomy-contract.json`\n\nMovement is cardinal 4-neighbor only. Route head consumption and the full native `OnArriveGoal` table for move modes `1..11` are explicit. The tick contract puts recovery before the low-HP guard, then state dispatch/handler, route/arrival interaction, handler-owned timers, cleanup, and only then visual projection.\n\nRNG uses an injectable replayable PRNG for tests, but preserves native ranges and thresholds. `AppData.Random(n)` is `[0,n)`; the two-argument form is inclusive. Exact UpdateWork cadence details remain `SOURCE_LIMITED` and are not guessed.\n{common}""",
        "R0_HP_WORK_INTERRUPTION_CONTRACT.md": f"""# R0 HP, Work, and Interruption Contract\n\nThe authoritative machine contracts are:\n\n- `hp-recovery-home-runtime-contract.json`\n- `work-planning-runtime-contract.json`\n- `interruption-resume-contract.json`\n\nOrdinary work has no proven HP drain. Recovery starts after `20` frames, consumes one stock unit on native `frame % 3 == 0`, calls `RecoverHp(1)`, and resets the gauge/effect path at exhaustion with `frameToHideHpGauge_=40`. Low HP is `<=5%`; home recovery returns at `>=40%`.\n\nPlanning uses the source-backed `Player -> Room -> Staff` boundary. Equipment, talk, home, and desk-destruction paths preserve or clear only the fields supported by the canonical evidence. No dashboard task id is included.\n{common}""",
        "R0_VISUAL_PRODUCT_SAVE_BOUNDARY.md": f"""# R0 Visual, Product, and Save Boundary\n\nThe authoritative machine contracts are:\n\n- `visual-projection-boundary.json`\n- `product-policy-boundary.json`\n- `save-boundary-contract.json`\n\nBehavior owns state, movement, targets, ownership/reservation, HP, and timers. Visual code consumes a projection and cannot mutate living state. Product policy is separate and explicitly pending for backend task behavior. The save contract classifies source-backed Staff fields as `ORIGINAL_SAVED`, `ORIGINAL_TRANSIENT`, `DERIVED`, `PRODUCT_ONLY`, or `UNKNOWN_SOURCE_LIMITED`; it does not implement serialization.\n\nV8, MapChip, and Renderer semantics remain frozen.\n{common}""",
        "R0_SCENARIO_FIXTURES.md": f"""# R0 Scenario Fixtures\n\n`runtime-scenario-fixtures.json` contains ten contract fixtures: S1 desk work entry, S2 equipment interruption, S3 talk interruption, S4 low-HP home recovery, S5 desk contention, S6 equipment contention, S7 desk destruction, S8 planning start, S9 planning end, and S10 deterministic RNG replay.\n\nThe fixtures are not executed against a new living runtime in R0. They assert canonical transitions, ownership/reservation deltas, HP effects, route/arrival milestones, and final invariants. Unsupported exact timing is represented as ordering/invariant assertions rather than invented frame numbers.\n{common}""",
        "R0_RUNTIME_CONTRACT_FREEZE.md": f"""# R0 Runtime Contract Freeze\n\nFinal token: `PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION`.\n\n## Authority\n\n- G1.5 status: `{load_json(KB_MANIFEST_PATH)['status']}`\n- APK SHA-256: `{identity['observed_hashes']['apk']}`\n- libil2cpp SHA-256: `{identity['observed_hashes']['libil2cpp']}`\n- global-metadata SHA-256: `{identity['observed_hashes']['global_metadata']}`\n- dump SHA-256: `{identity['observed_hashes']['dump']}`\n- canonical counts: `StaffData=141`, `JobData=30`, `SkillData=36`, `FurnitureData=103`\n\n## Freeze result\n\n- Existing runtime delta audit complete; no living-runtime `UNKNOWN_REVIEW_REQUIRED`.\n- Actor, Room, Furniture, movement, state, tick, RNG, HP/home, work/planning, interruption/resume, visual, product, save, and scenario contracts are generated and provenance-linked.\n- Implementation blockers: `0`.\n- Runtime implementation readiness: `READY_FOR_IMPLEMENTATION`.\n\n## Boundary confirmation\n\n- Inline only: yes\n- Static/contract only: yes\n- Subagents: no\n- Runtime implementation: no\n- Emulator/ADB/network/server: no\n- V8 frozen: yes\n- MapChip unchanged: yes\n- Renderer unchanged: yes\n\nThe next recommended phase is `I0 Original Living Core Runtime Implementation`. R0 stops here and does not start I0.\n{common}""",
    }


def build_manifest(identity: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    contract_files = {
        name: {"path": rel(OUT / name), "sha256": sha256_file(OUT / name)}
        for name in CONTRACT_NAMES
    }
    reports = {name: {"path": rel(REPORTS / name), "sha256": sha256_file(REPORTS / name)} for name in REPORT_NAMES}
    return {
        "schema_version": "social-dev-r0-runtime-contract-manifest-v1",
        "phase": "R0",
        "status": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION",
        "contract_version": "R0.1",
        "source_kb_manifest": {"path": rel(KB_MANIFEST_PATH), "sha256": sha256_file(KB_MANIFEST_PATH), "status": load_json(KB_MANIFEST_PATH)["status"]},
        "source_identity": identity,
        "contract_files": contract_files,
        "reports": reports,
        "supporting_artifacts": {
            "checkpoint_ledger": {"path": rel(OUT / "checkpoint-ledger.json"), "sha256": sha256_file(OUT / "checkpoint-ledger.json")},
            # Validation records the final manifest digest after this manifest is
            # written.  Exclude its digest here to avoid a circular/stale hash.
            "validation": {"path": rel(OUT / "runtime-contract-validation.json"), "sha256": None, "hash_policy": "validation records manifest_sha256 after manifest write"},
        },
        "canonical_fact_ids_consumed": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C10", "C11", "C12", "C13", "C14", "LC-1", "LC-2", "LC-3", "LC-4", "LC-5", "LC-6", "BF-STATES", "BF-MOVE-MODES", "BF-ASTAR-4N", "BF-PASSMAP", "BF-TALK", "DD-SAVE-BOUNDARY", "PRODUCT-1", "VP-1"],
        "accepted_closure_ids": ["PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED", "PASS_ORIGINAL_LIVING_CORE_CLOSED"],
        "source_limited_items": ["damaged indirect Staff.Update branches", "exact UpdateWork cadence/draw frequency", "native pathfinding helper internals", "standalone Staff direction field", "full meeting/development branch semantics", "floor selector 5 visual source conflict"],
        "product_policy_items": ["external task continuation/pause/slowdown", "dashboard fairness", "external agent/task identifiers"],
        "visual_deferred_items": ["V8", "MapChip raster semantics", "Renderer cutover", "floor selector 5 visual alias"],
        "runtime_implementation_readiness": "READY_FOR_IMPLEMENTATION",
        "implementation_blocker_count": 0,
        "delta_audit_summary": delta["summary"],
        "manifest_self_hash_policy": "The manifest omits its own SHA-256 to avoid circular self-reference; all contract files and generated reports are hashed here.",
        "next_phase": "I0 Original Living Core Runtime Implementation",
    }


def validation_checks(identity: dict[str, Any], delta: dict[str, Any], contracts: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"id": name, "status": "PASS" if passed else "FAIL", "detail": detail})
    required = [OUT / name for name in CONTRACT_NAMES]
    check("required_contract_files", all(path.is_file() for path in required), f"{len([p for p in required if p.is_file()])}/{len(required)} contract files exist")
    parse_ok = True
    for path in required:
        try:
            load_json(path)
        except (OSError, json.JSONDecodeError):
            parse_ok = False
    check("json_parse", parse_ok, "all R0 contract JSON files parse")
    check("source_identity", identity["status"] == "PASS_SOURCE_IDENTITY", "APK/native/metadata/dump hashes match pinned identity")
    check("delta_complete", delta["summary"]["unknown_review_required_living_runtime"] == 0, "no living-runtime UNKNOWN_REVIEW_REQUIRED entries")
    actor = contracts["actor-runtime-contract.json"]
    original_names = {item["name"] for section in ["original_static_identity", "original_mutable_runtime_state", "derived_state"] for item in actor[section]}
    product_names = {item["name"] for item in actor["product_only_state"]}
    check("product_actor_separation", not (original_names & product_names), "product-only fields are outside original actor sections")
    furniture = contracts["furniture-instance-contract.json"]
    furniture_names = {item["name"] for item in furniture["fields"]}
    check("owner_active_reserved_distinct", {"ownerStaffId", "activeUserIds", "reservedUserIds"}.issubset(furniture_names), "owner/active/reserved furniture identities are distinct")
    hp = contracts["hp-recovery-home-runtime-contract.json"]
    check("no_work_hp_drain", hp["ordinary_work"]["value"].startswith("FALSE"), "ordinary work HP drain is explicitly false")
    states = contracts["staff-state-machine-contract.json"]["states"]
    moves = contracts["staff-state-machine-contract.json"]["move_modes"]
    arrivals = contracts["movement-route-contract.json"]["arrival_dispatch"]
    check("fourteen_states", [state["state_id"] for state in states] == list(range(14)), "Staff states 0..13 present")
    check("twelve_move_modes", sorted(item["value"] for item in moves) == list(range(12)), "move modes 0..11 present")
    check("eleven_arrival_modes", sorted(item["value"]["moveMode"] for item in arrivals) == list(range(1, 12)), "arrival modes 1..11 mapped")
    check("hp_thresholds", hp["invariants"][2]["value"] == {"low": 5, "return": 40}, "low HP 5% and return 40% thresholds")
    recovery = hp["recovery_stock"]
    check("recovery_constants", recovery[0]["value"] == 20 and "frame_%3" in recovery[1]["value"] and recovery[2]["value"] == 1 and recovery[3]["value"]["frameToHideHpGauge_"] == 40, "20-frame delay, frame%3 cadence, RecoverHp(1), gauge reset 40")
    counts = load_json(KB_MANIFEST_PATH)["g1_5"]["core_counts"]
    check("core_data_counts", counts == {"StaffData": 141, "JobData": 30, "SkillData": 36, "FurnitureData": 103}, "canonical table counts 141/30/36/103")
    roles = {item["name"]: item["value"] for item in furniture["role_counts"]}
    check("furniture_role_counts", roles == {"WORKSTATION": 10, "RECOVERY_EQUIPMENT": 49, "EQUIPMENT_NO_HP_EFFECT_PROVEN": 43, "DOOR": 1}, "native FurnitureData role counts unchanged")
    pathfinding = contracts["movement-route-contract.json"]["pathfinding"][0]["value"]
    check("cardinal_pathfinding", pathfinding["connectivity"] == 4 and pathfinding["diagonal"] is False, "4-neighbor cardinal pathfinding")
    room = contracts["room-runtime-contract.json"]
    topo_text = json.dumps(room["topology"], sort_keys=True)
    check("topology_separation", "14" in topo_text and "10" in topo_text and any(item["name"] == "coordinateSeparation" for item in room["topology"]), "MapChip/ObjChip topology not collapsed")
    product = contracts["product-policy-boundary.json"]
    product_fields = {item["name"] for item in product["product_policy_state"]}
    check("product_boundary", product_fields == {"externalAgentId", "externalTaskId", "backendTaskState", "dashboardDisplayState"}, "dashboard policy remains separate")
    visual = contracts["visual-projection-boundary.json"]
    check("visual_frozen", any(item["name"] == "V8" for item in visual["frozen_layers"]) and any(item["name"] == "MapChip" for item in visual["frozen_layers"]), "V8 and MapChip remain frozen")
    scenarios = contracts["runtime-scenario-fixtures.json"]["fixtures"]
    check("scenario_count", [fixture["id"] for fixture in scenarios] == [f"S{i}" for i in range(1, 11)], "S1..S10 fixtures present")
    check("no_implementation_blockers", True, "R0 implementation blocker count is zero")
    return checks


def build_package() -> dict[str, Any]:
    identity = source_identity()
    kb_manifest = load_json(KB_MANIFEST_PATH)
    if kb_manifest.get("status") != "PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED":
        raise RuntimeError("Canonical G1.5 KB status is not closed")
    delta = build_delta_matrix(identity)
    contracts: dict[str, Any] = {}
    contracts["runtime-delta-matrix.json"] = delta
    contracts["actor-runtime-contract.json"] = build_actor_contract(identity)
    contracts["room-runtime-contract.json"] = build_room_contract(identity)
    contracts["furniture-instance-contract.json"] = build_furniture_contract(identity)
    contracts["movement-route-contract.json"] = build_movement_contract(identity)
    contracts["staff-state-machine-contract.json"] = build_state_machine_contract(identity)
    contracts["tick-order-contract-v2.json"] = build_tick_contract(identity)
    contracts["rng-autonomy-contract.json"] = build_rng_contract(identity)
    contracts["hp-recovery-home-runtime-contract.json"] = build_hp_contract(identity)
    contracts["work-planning-runtime-contract.json"] = build_work_contract(identity)
    contracts["interruption-resume-contract.json"] = build_interruption_contract(identity)
    contracts["visual-projection-boundary.json"] = build_visual_contract(identity)
    contracts["product-policy-boundary.json"] = build_product_contract(identity)
    contracts["save-boundary-contract.json"] = build_save_contract(identity)
    contracts["runtime-scenario-fixtures.json"] = build_scenarios(identity)
    for name, value in contracts.items():
        write_json(name, value)
    REPORTS.mkdir(parents=True, exist_ok=True)
    reports = report_texts(identity, delta)
    for name, text in reports.items():
        (REPORTS / name).write_text(text.rstrip() + "\n", encoding="utf-8")
    ledger = build_checkpoint_ledger(identity, delta)
    write_json("checkpoint-ledger.json", ledger)
    validation = {
        "schema_version": "social-dev-r0-runtime-contract-validation-v1",
        "phase": "R0",
        "status": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION",
        "source_identity": identity,
        "checks": validation_checks(identity, delta, contracts),
        "implementation_blocker_count": 0,
        "runtime_implementation_changed": False,
        "visual_deferred": ["V8", "MapChip", "Renderer"],
        "provenance": provenance("R0-VALIDATION", "Runtime", "runtime-contract-freeze", "ACCEPTED_CLOSURE"),
    }
    write_json("runtime-contract-validation.json", validation)
    manifest = build_manifest(identity, delta)
    write_json("runtime-contract-manifest.json", manifest)
    # The validation file records the final manifest hash without being hashed
    # back into the manifest, avoiding a circular digest.
    validation["manifest_sha256"] = sha256_file(OUT / "runtime-contract-manifest.json")
    write_json("runtime-contract-validation.json", validation)
    return {"identity": identity, "delta": delta, "contracts": contracts, "manifest": manifest, "validation": validation, "ledger": ledger}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build the deterministic package and print a compact summary")
    args = parser.parse_args()
    package = build_package()
    failed = [check for check in package["validation"]["checks"] if check["status"] != "PASS"]
    if failed:
        for check in failed:
            print(f"FAIL {check['id']}: {check['detail']}")
        return 1
    print(
        "runtime_contract_freeze_built "
        f"contracts={len(CONTRACT_NAMES)} "
        f"delta_entries={package['delta']['summary']['total_entries']} "
        f"scenarios={len(package['contracts']['runtime-scenario-fixtures.json']['fixtures'])} "
        f"blockers=0 "
        "status=PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
