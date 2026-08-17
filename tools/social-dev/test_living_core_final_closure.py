"""Static acceptance and regression checks for the Living-Core final closure."""

from __future__ import annotations

import json
import sys
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))

from build_living_core_final_closure import (  # noqa: E402
    EXPECTED_HASHES,
    OUT,
    REPORTS,
    artifact_hashes,
    build_all,
)


REQUIRED_JSON = [
    "checkpoint-ledger.json",
    "blocker-matrix.json",
    "staff-native-authority-map.json",
    "hp-native-write-site-catalog.json",
    "ordinary-work-hp-drain-contract.json",
    "recovery-cadence-contract.json",
    "recovery-cadence-native-trace.json",
    "on-arrive-goal-jump-table.json",
    "on-arrive-goal-dispatch-contract.json",
    "workstation-vacancy-ownership-contract.json",
    "desk-selection-fixtures.json",
    "equipment-user-count-contract.json",
    "equipment-contention-contract.json",
    "furniture-exact-role-contract.json",
    "furniture-living-role-catalog.json",
    "original-work-assignment-contract.json",
    "original-task-to-living-core-boundary.json",
    "work-interruption-resume-contract.json",
    "complete-original-staff-life-loop.json",
    "living-core-scenario-fixtures.json",
    "canonical-actor-schema-final.json",
    "canonical-furniture-schema-final.json",
    "dashboard-policy-deferred-boundary.json",
    "unknowns.json",
]

REQUIRED_REPORTS = [
    "LIVING_CORE_FINAL_CLOSURE.md",
    "ORDINARY_WORK_HP_DRAIN.md",
    "RECOVERY_CADENCE.md",
    "ON_ARRIVE_GOAL_DISPATCH.md",
    "WORKSTATION_OWNERSHIP_AND_VACANCY.md",
    "EQUIPMENT_CONTENTION.md",
    "FURNITURE_EXACT_LIVING_ROLES.md",
    "ORIGINAL_WORK_ASSIGNMENT_FLOW.md",
    "WORK_INTERRUPTION_AND_RESUME.md",
    "COMPLETE_STAFF_LIFE_LOOP.md",
    "LIVING_CORE_FINAL_HANDOFF.md",
]


def load(name: str) -> dict:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def main() -> int:
    build_all()
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(f"check {checks} failed: {message}")

    check(OUT.is_dir(), "living-core evidence directory exists")
    check(REPORTS.is_dir(), "Behavior reports directory exists")
    check(set(path.name for path in OUT.glob("*.json")) == set(REQUIRED_JSON), "exact requested evidence JSON set")
    check(set(path.name for path in REPORTS.glob("LIVING_CORE*.md")) == {"LIVING_CORE_FINAL_CLOSURE.md", "LIVING_CORE_FINAL_HANDOFF.md"}, "living-core closure/handoff reports exist")
    for name in REQUIRED_REPORTS:
        path = REPORTS / name
        check(path.is_file(), f"required report exists: {name}")
        check(path.read_text(encoding="utf-8").strip(), f"required report is non-empty: {name}")

    ledger = load("checkpoint-ledger.json")
    check(ledger["closure_status"] == "PASS_ORIGINAL_LIVING_CORE_CLOSED", "final closure status")
    check([item["checkpoint"] for item in ledger["records"]] == [f"LC.{number}" for number in range(17)], "LC.0-LC.16 checkpoint coverage")
    check(ledger["records"][-1]["status"] == "STOP_ORIGINAL_LIVING_CORE_CLOSED", "stop checkpoint")
    stop = ledger["required_stop_literals"]
    check(stop["Visual work performed"] == "NO", "visual stop literal")
    check(stop["V8_started"] == "NO", "V8 stop literal")
    check(stop["renderer_changed"] == "NO" and stop["MapChip_changed"] == "NO", "renderer/MapChip stop literals")
    check(stop["subagents"] == "NO" and stop["emulator_ADB_live_app"] == "NO", "agent/live-app stop literals")
    check(stop["local_server"] == "NO" and stop["network"] == "NO", "server/network stop literals")

    hashes = artifact_hashes()
    check(hashes["status"] == "PASS", "pinned artifact hash status")
    for row in hashes["records"][:3]:
        check(row["matches"], f"pinned hash matches: {row['artifact']}")
    check(hashes["records"][0]["sha256"] == EXPECTED_HASHES["apk_sha256"], "APK SHA-256 exact")
    check(hashes["records"][1]["sha256"] == EXPECTED_HASHES["libil2cpp_sha256"], "libil2cpp SHA-256 exact")
    check(hashes["records"][2]["sha256"] == EXPECTED_HASHES["global_metadata_sha256"], "metadata SHA-256 exact")

    matrix = load("blocker-matrix.json")
    check({item["id"] for item in matrix["blockers"]} == {f"LC-{number}" for number in range(1, 7)}, "six blocker IDs")
    check(all(item["status"].startswith("CLOSED_") for item in matrix["blockers"]), "all six blockers closed")

    native = load("staff-native-authority-map.json")
    methods = {(item["owner"], item["method"]): item for item in native["methods"]}
    for key, rva in {
        ("Staff", "Update"): "0x12D2EC8",
        ("Staff", "UpdateRecoveryHp"): "0x12D2C8C",
        ("Staff", "UpdateWork"): "0x12D4A7C",
        ("Staff", "OnArriveGoal"): "0x12D8420",
        ("Room", "GetStaffEmptyObjTypeOf"): "0x12CF178",
        ("ObjChip", "GetUsersNum"): "0x12C4A70",
    }.items():
        check(methods[key]["rva"] == rva, f"native RVA {key}")
    staff_fields = {item["name"]: item for item in native["field_offsets"]["Staff"]}
    check(staff_fields["hp_"]["offset"] == "0xE8", "Staff.hp_ offset")
    check(staff_fields["moveMode_"]["offset"] == "0xA8", "Staff.moveMode_ offset")

    hp = load("hp-native-write-site-catalog.json")
    check(hp["field"]["offset"] == "0xE8", "HP write catalog field offset")
    negative = hp["negative_trace"]
    check(negative["method"] == "Staff.UpdateWork" and negative["str_or_stur_write_count"] == 0, "UpdateWork has no HP write")
    check(negative["RecoverHp_call_count"] == 0 and negative["negative_recovery_call_count"] == 0, "UpdateWork has no recovery call")
    check(all(item["method"] != "Staff.UpdateWork" for item in hp["write_sites"]), "UpdateWork absent from HP write sites")

    work = load("ordinary-work-hp-drain-contract.json")
    check(work["status"] == "CLOSED_NO_ORIGINAL_DRAIN", "ordinary work closure")
    check(work["native_trace"]["hp_write_count"] == 0, "ordinary work HP write count")
    check(work["native_trace"]["negative_recover_hp_call_count"] == 0, "ordinary work negative recovery call count")
    check(work["static_fixture_rule"] == "For an ordinary work tick, hp_before == hp_after unless another proven system mutates HP in the same fixture.", "ordinary work fixture rule")

    recovery = load("recovery-cadence-contract.json")
    check(recovery["start"]["frameToStartRecovery_"] == 20, "recovery start delay")
    check("frame_%3==0" in recovery["cadence"]["tick"], "recovery cadence modulo")
    check(recovery["exhaustion"]["frameToHideHpGauge_"] == 40, "recovery gauge reset")
    check(recovery["exhaustion"]["recoveryHpStock_"] == 0, "recovery stock exhaustion")
    trace = load("recovery-cadence-native-trace.json")
    check(trace["constant_evidence"]["stock_unit_hp"] == 1, "recovery stock unit")
    check(trace["constant_evidence"]["recovery_tick_interval_frames"] == 3, "recovery interval")

    arrivals = load("on-arrive-goal-jump-table.json")
    check(len(arrivals["entries"]) == 11, "11 arrival cases")
    check(arrivals["jump_table_rodata"] == "0x636684" and arrivals["dispatch_base"] == "0x12D84A8", "arrival table locations")
    check({entry["move_mode"] for entry in arrivals["entries"]} == set(range(1, 12)), "arrival move modes 1..11")
    check(arrivals["key_field"]["offset"] == "0xA8", "arrival key field")
    arrival_contract = load("on-arrive-goal-dispatch-contract.json")
    check(arrival_contract["status"] == "CLOSED_11_WAY_NATIVE_DISPATCH", "arrival closure")
    check(arrival_contract["dispatch"]["entries"] == arrivals["entries"], "arrival contract/table agreement")

    desks = load("desk-selection-fixtures.json")

    def select(chips: list[dict]) -> int | None:
        for chip in chips:
            if chip["type"] == 2 and chip["installed"] and chip["staffId"] == -1:
                return chip["index"]
        return None

    for fixture in desks["fixtures"]:
        check(select(fixture["chips"]) == fixture["expected_selected_index"], f"desk fixture {fixture['id']}")
    workstation = load("workstation-vacancy-ownership-contract.json")
    check(workstation["vacancy_predicate"]["required"] == ["ObjChip.type_ == 2", "ObjChip.furnitureData_ != null", "ObjChip.staffId_ == -1"], "desk predicate exactness")
    check(workstation["fairness"]["status"] == "NOT_PRESENT_IN_NATIVE_SELECTOR", "desk fairness boundary")

    users = load("equipment-user-count-contract.json")
    check(users["return"] == "reservedStaffs_ FastVector length at vector offset 0x14", "equipment user count semantics")
    check("staffs_ active-user vector at 0x68" in users["ignored_fields"], "active users excluded from count")
    contention = load("equipment-contention-contract.json")
    check(contention["gate"] == "GetUsersNum() > 0 rejects the target; GetUsersNum() <= 0 reserves it and enters MOVE/GOTO_EQUIPMENT.", "equipment contention gate")
    check(len(contention["fixtures"]) == 4, "equipment contention fixtures")

    furniture = load("furniture-exact-role-contract.json")
    check(furniture["record_count"] == 103, "FurnitureData record count")
    check(furniture["class_counts"] == {"DOOR_RECORD": 1, "EQUIPMENT_NO_HP_EFFECT_PROVEN": 43, "RECOVERY_EQUIPMENT": 49, "WORKSTATION": 10}, "FurnitureData class counts")
    check(furniture["not_promoted"]["REST"].startswith("No FurnitureData record"), "no invented rest role")
    check(furniture["not_promoted"]["SOCIAL"].startswith("No FurnitureData record"), "no invented social role")
    catalog = load("furniture-living-role-catalog.json")
    check(len(catalog["records"]) == 103, "full FurnitureData role catalog")

    assignment = load("original-work-assignment-contract.json")
    check(assignment["status"] == "CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER", "assignment closure")
    check(len(assignment["stages"]) == 5, "assignment stages")
    check(len(assignment["explicit_mutators"]) == 3, "explicit mutator catalog")
    check(all(item["status"] == "EXPOSED_API_NO_RECOVERED_CALLER" for item in assignment["explicit_mutators"]), "no unsupported assignment caller")
    check(assignment["ui_evidence"]["status"] == "CUT_LATER", "original UI boundary")
    boundary = load("original-task-to-living-core-boundary.json")
    check(boundary["ui_boundary"]["future_dashboard_policy"] == "PRODUCT_POLICY_PENDING", "dashboard policy pending")

    interruption = load("work-interruption-resume-contract.json")
    check(interruption["status"] == "CLOSED_ORIGINAL_RESUME_PATH", "interruption closure")
    check({item["id"] for item in interruption["interruptions"]} == {"work-to-equipment", "work-to-talk", "low-hp-home", "desk-destroyed"}, "interruption cases")
    life_loop = load("complete-original-staff-life-loop.json")
    check(life_loop["status"] == "CLOSED_COMPLETE_ORIGINAL_LIVING_CORE", "life loop closure")
    check(len(life_loop["sequence"]) == 8, "complete life-loop stages")
    scenarios = load("living-core-scenario-fixtures.json")
    check(len(scenarios["fixtures"]) >= 10, "living-core scenario coverage")
    check(all(item["status"] == "PASS_STATIC" for item in scenarios["fixtures"]), "living-core scenario status")

    actor = load("canonical-actor-schema-final.json")
    actor_fields = {item["name"]: item for item in actor["fields"]}
    check(actor_fields["hp"]["authority"] == "Staff.hp_ @ 0xE8", "actor HP authority")
    check(actor_fields["deskId"]["authority"] == "Staff.deskId_ @ 0xB8", "actor desk authority")
    check(actor_fields["taskAssignment"]["role"] == "PRODUCT_POLICY_PENDING", "actor task boundary")
    furniture_schema = load("canonical-furniture-schema-final.json")
    furniture_fields = {item["name"]: item for item in furniture_schema["fields"]}
    check(furniture_fields["ownerStaffId"]["authority"] == "ObjChip.staffId_ @ 0x78", "furniture owner authority")
    check(furniture_fields["reservedUserIds"]["authority"] == "reservedStaffs_ @ 0x70", "furniture reservation authority")
    dashboard = load("dashboard-policy-deferred-boundary.json")
    check(dashboard["status"] == "PRODUCT_POLICY_PENDING", "dashboard policy boundary")
    check(dashboard["original_ui"] == "CUT_LATER" and dashboard["visual_work_performed"] == "NO", "dashboard/UI stop boundary")

    unknowns = load("unknowns.json")
    check(unknowns["status"] == "tracked_non_blocking", "unknowns are non-blocking except deferred policy")
    check(any(item["id"] == "LC-U04" and item["blocked_now"] for item in unknowns["unknowns"]), "future dashboard policy remains explicit")

    print(f"PASS_ORIGINAL_LIVING_CORE_CLOSED ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
