"""Static BF.18 coverage for the behavior-first forensic package."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from build_behavior_first_forensics import EVIDENCE, OUT, REPORTS, ROOT, build_all


REQUIRED_JSON = [
    "checkpoint-ledger.json",
    "prior-evidence-reconciliation.json",
    "staff-field-inventory.json",
    "staff-state-constant-catalog.json",
    "staff-state-machine.json",
    "staff-transition-graph.json",
    "hp-condition-contract.json",
    "hp-read-write-graph.json",
    "work-recovery-lifecycle.json",
    "home-rest-contract.json",
    "equipment-behavior-contract.json",
    "workstation-ownership-reservation-contract.json",
    "furniture-behavior-catalog.json",
    "movement-target-arrival-contract.json",
    "talk-social-contract.json",
    "idle-autonomy-contract.json",
    "multi-actor-contention-contract.json",
    "dashboard-task-assignment-input.json",
    "behavior-visible-action-map.json",
    "canonical-staff-life-model.json",
    "dashboard-preservation-boundary.json",
    "unknowns.json",
]

REQUIRED_REPORTS = [
    "BEHAVIOR_FIRST_AUDIT.md",
    "STAFF_STATE_MACHINE.md",
    "HP_CONDITION_SYSTEM.md",
    "WORK_RECOVERY_LIFECYCLE.md",
    "HOME_REST_BEHAVIOR.md",
    "FURNITURE_BEHAVIOR_MODEL.md",
    "EQUIPMENT_INTERACTIONS.md",
    "WORKSTATION_OWNERSHIP.md",
    "STAFF_SOCIAL_AUTONOMY.md",
    "DASHBOARD_BEHAVIOR_BOUNDARY.md",
    "BEHAVIOR_FIRST_HANDOFF.md",
]


def main() -> int:
    build_all()
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(f"check {checks} failed: {message}")

    check(OUT.is_dir(), "behavior-first evidence directory exists")
    check(REPORTS.is_dir(), "Behavior reports directory exists")

    docs: dict[str, object] = {}
    for name in REQUIRED_JSON:
        path = OUT / name
        check(path.is_file(), f"required JSON exists: {name}")
        docs[name] = json.loads(path.read_text(encoding="utf-8"))
    for name in REQUIRED_REPORTS:
        path = REPORTS / name
        check(path.is_file(), f"required report exists: {name}")
        check(path.read_text(encoding="utf-8").strip(), f"required report is non-empty: {name}")

    ledger = docs["checkpoint-ledger.json"]  # type: ignore[assignment]
    check(len(ledger["records"]) == 20, "BF.0-BF.19 checkpoint coverage")
    check({row["Checkpoint"] for row in ledger["records"]} == {f"BF.{n}" for n in range(20)}, "checkpoint IDs are complete")
    check(ledger["records"][-1]["Status"] == "STOP_NO_VISUAL_CUTOVER", "BF.19 is the stop checkpoint")
    check(ledger["required_stop_literals"]["V8_started"] == "NO", "V8 stop literal")

    inventory = docs["staff-field-inventory.json"]  # type: ignore[assignment]
    check(inventory["counts"]["records"] >= 100, "Staff mutable/storage field inventory is broad")
    check(inventory["counts"]["dump_aligned"] == inventory["counts"]["records"], "every inventory field has a pinned dump offset")
    hp_field = next(item for item in inventory["fields"] if item["name"] == "hp_")
    check(hp_field["dump"]["offset"] == "0xE8", "Staff.hp_ offset")
    check(any(item["name"] == "recoveryHpStock_" for item in inventory["fields"]), "recovery stock field inventory")

    constants = docs["staff-state-constant-catalog.json"]  # type: ignore[assignment]
    state_values = {item["name"]: item["value"] for item in constants["staff_state_move_flag_constants"]}
    check(state_values["STATE_NORMAL"] == 0 and state_values["STATE_STAY_HOME"] == 13, "state constants")
    check(state_values["MOVE_MODE_GOTO_EQUIPMENT"] == 1 and state_values["MOVE_MODE_GO_TO_DOOR"] == 10, "move mode constants")
    check(state_values["FLAG_SITTING"] == 2 and state_values["FLAG_SLEEPING"] == 32, "sitting/sleeping flags")
    check(state_values["FLAG_RESERVED_TALK"] == 4 and state_values["FLAG_INVITED_TALK"] == 8, "talk flags")
    check(constants["native_method_rvas"]["Staff.Update"] == "0x12D2EC8", "Staff.Update native RVA")
    check(constants["native_method_rvas"]["ObjChip.IsPassable"] == "0x12C4AB8", "ObjChip.IsPassable native RVA")

    machine = docs["staff-state-machine.json"]  # type: ignore[assignment]
    check(len(machine["states"]) == 14, "all Staff living/develop state labels")
    check(any(item["id"] == "low-hp-door-escape" for item in machine["transitions"]), "low HP transition")
    check(any(item["id"] == "stay-home-recovery-return" for item in machine["transitions"]), "stay-home return transition")
    check(any(item["id"] == "arrival-consumes-route" for item in machine["transitions"]), "arrival transition")

    hp = docs["hp-condition-contract.json"]  # type: ignore[assignment]
    check(hp["field"]["name"] == "hp_" and hp["field"]["offset"] == "0xE8", "HP authority contract")
    check(hp["max_formula"]["parameter_value"] == 5, "HP max uses PARAM_HP=5")
    check(hp["thresholds"]["low_hp_ratio_percent"] == 5 and hp["thresholds"]["home_return_ratio_percent"] == 40, "HP thresholds")
    check(hp["thresholds"]["recovery_start_delay_frames"] == 20, "recovery delay")
    check(hp["condition_search"]["direct_drain_search"]["RecoverHp(-"] == [], "no readable negative RecoverHp write")
    check(hp["condition_search"]["direct_drain_search"]["hp_ -="] == [], "no readable hp subtraction write")
    check(not hp["condition_search"]["exact_name_results_in_Staff_cs"]["condition_"], "no Staff condition_ field")
    expanded = hp["condition_search"]["expanded_exact_name_search"]
    check(set(expanded) == {"stamina_", "energy_", "fatigue_", "condition_", "status_"}, "expanded HP/condition name search")
    check(all(not expanded[name]["Staff.cs_matches"] for name in ("stamina_", "energy_", "fatigue_", "condition_")), "expanded search has no Staff condition fields")
    check(any("game/Player.cs" in path for path in expanded["stamina_"]["matches_by_file"]), "expanded search distinguishes Player stamina")
    check(any("game/Avatar.cs" in path for path in expanded["energy_"]["matches_by_file"]), "expanded search distinguishes Avatar energy")

    lifecycle = docs["work-recovery-lifecycle.json"]  # type: ignore[assignment]
    check(len(lifecycle["lifecycle"]) == 5, "work/recovery lifecycle stages")
    check(lifecycle["ordinary_work_hp_drain"]["status"] == "UNKNOWN", "work drain remains unknown")
    home = docs["home-rest-contract.json"]  # type: ignore[assignment]
    check(home["return"]["guard"] == "GetHpRatio() >= 40", "home return guard")
    check(home["return"]["door_reservation"], "home return reserves the door")

    equipment = docs["equipment-behavior-contract.json"]  # type: ignore[assignment]
    check(equipment["selection"]["types"] == [1, 4], "equipment target types")
    check(equipment["selection"]["reservation_guard"] == "GetUsersNum() <= 0", "equipment contention guard")
    check([item["frame"] for item in equipment["use_timeline"]] == [20, 40, 60, 70], "equipment visible timeline")

    workstation = docs["workstation-ownership-reservation-contract.json"]  # type: ignore[assignment]
    check(workstation["desk_creation"]["furniture_flag"] == 16384, "desk seed flag")
    check(any(item["field"] == "Staff.deskId_" for item in workstation["desk_ownership"]), "Staff desk ownership")
    check(any(item["operation"] == "ReserveUse" for item in workstation["reservation_lifecycle"]), "reservation lifecycle")

    furniture = docs["furniture-behavior-catalog.json"]  # type: ignore[assignment]
    check(furniture["counts"]["records"] == 103, "all FurnitureData records")
    check(furniture["counts"]["source_package_records"] == 103, "metadata package count")
    check(furniture["counts"]["by_interaction_class"]["WORKSTATION"] == 10, "type-2 workstation count")
    check(furniture["counts"]["by_interaction_class"]["RECOVERY_EQUIPMENT"] == 49, "recovery equipment count")
    check(all(item["passability"]["passMap_present"] for item in furniture["records"]), "all records preserve passMap presence")
    check(all(item["rest_semantics"] == "NOT_EXPLICIT_IN_STAFF_SOURCE" for item in furniture["records"]), "no inferred furniture rest role")
    check(all(item["social_semantics"] == "NOT_A_FURNITURE_ROLE_IN_STAFF_SOURCE" for item in furniture["records"]), "no inferred furniture social role")

    movement = docs["movement-target-arrival-contract.json"]  # type: ignore[assignment]
    mapping = {item["move_mode"]: item["astar_flag"] for item in movement["goal_flag_mapping"] if "astar_flag" in item}
    check(mapping[1] == 2 and mapping[3] == 1 and mapping[7] == 4, "Astar goal flag mapping")
    check(movement["route_algorithm"]["neighbors"] == "cardinal only", "cardinal route contract")
    check(len(movement["standing_positions"]["positions"]) == 4, "four standing positions")
    check(any(item["method"] == "OnArriveNextNode" for item in movement["movement_loop"]), "arrival consumer")

    social = docs["talk-social-contract.json"]  # type: ignore[assignment]
    check("target state == STATE_WORK" in social["initiator"]["guards"], "talk target work guard")
    check(social["talk_timing"]["frame_130_or_more"].startswith("clear"), "talk completion timing")
    check(social["skill_effect"]["skill_id"] == 1 and social["skill_effect"]["effect_value"] == 150, "selected meeting skill")

    idle = docs["idle-autonomy-contract.json"]  # type: ignore[assignment]
    check(len(idle["decision_order"]) >= 5, "idle autonomy decision order")
    check("equipment_attempt" in idle["probability_bounds"], "equipment probability bound")
    contention = docs["multi-actor-contention-contract.json"]  # type: ignore[assignment]
    check(contention["reservation_state"] == "ObjChip.reservedStaffs_", "contention reservation authority")
    check(contention["fairness_and_queue"] == "UNKNOWN; no source-backed queue or fairness policy was found.", "no invented fairness policy")

    task_input = docs["dashboard-task-assignment-input.json"]  # type: ignore[assignment]
    check({item["class"] for item in task_input["inputs"]} >= {"StaffData", "JobData", "SkillData", "FurnitureData", "EventData"}, "dashboard input data classes")
    visible = docs["behavior-visible-action-map.json"]  # type: ignore[assignment]
    check(len(visible["actions"]) >= 7, "visible action map")
    preservation = docs["dashboard-preservation-boundary.json"]  # type: ignore[assignment]
    check("V8" in " ".join(preservation["forbidden_in_this_phase"]), "V8 forbidden")
    check("MapChip changes" in preservation["forbidden_in_this_phase"], "MapChip forbidden")
    canonical = docs["canonical-staff-life-model.json"]  # type: ignore[assignment]
    check(canonical["status"] == "pass_with_source_limits", "canonical model source-limited status")
    check(docs["unknowns.json"]["status"] == "tracked", "unknowns are tracked, not guessed")

    prior = docs["prior-evidence-reconciliation.json"]  # type: ignore[assignment]
    candidate_row = next(row for row in prior["records"] if row["artifact"] == "staff_behavior_candidate.json")
    check(candidate_row["treatment"] == "do_not_promote_wholesale", "historical candidate is not promoted wholesale")
    check(load_status("phase1d_closure.json") == "pass", "Phase 1D closure regression")
    check(load_status("phase1d_passmap_fixture.json") == "pass", "passMap regression")
    check(load_status("phase1d_route_fixture.json") == "pass", "route regression")

    generated_suffixes = {path.suffix.lower() for path in OUT.iterdir() if path.is_file()}
    check(not generated_suffixes.intersection({".png", ".jpg", ".jpeg", ".apk", ".aab"}), "no screenshots or binaries generated")
    check(not any("MapChip.cs" in path.name or "renderer" in path.name.lower() for path in OUT.iterdir()), "no renderer/MapChip artifact emitted")
    check(not any("v8" in path.name.lower() for path in OUT.iterdir()), "no V8 artifact emitted")
    check(no_source_root_diff(), "read-only source roots untouched")
    check(checks >= 35, "static coverage is at least 35 checks")

    print(f"behavior_first_static_checks_passed checks={checks} json={len(REQUIRED_JSON)} reports={len(REQUIRED_REPORTS)}")
    return 0


def load_status(name: str) -> str:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))["status"]


def no_source_root_diff() -> bool:
    paths = [
        "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs",
        "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs",
        "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/ObjChip.cs",
        "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/StaffData.cs",
        "knowledge/sources/data/csharp_update/FurnitureData.cs",
    ]
    result = subprocess.run(["git", "diff", "--name-only", "--", *paths], cwd=ROOT, check=True, capture_output=True, text=True)
    return not result.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
