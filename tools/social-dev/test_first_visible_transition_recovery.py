"""Static contract checks for the first-visible transition recovery package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted/visual-port/first-visible-transition"
DOCS = ROOT / "docs/Phases/VisualPort"

JSON_NAMES = [
    "checkpoint-ledger.json",
    "fs-unknown-inventory.json",
    "newgame-caller-contract.json",
    "startgame-control-flow.json",
    "starter-event-selection.json",
    "starter-event-command-map.json",
    "starter-room-mutation-timeline.json",
    "starter-wall-door-transition.json",
    "starter-staff-transition.json",
    "first-stable-boundary-contract.json",
    "first-visible-transition-timeline.json",
    "first-visible-stable-manifest.json",
    "fs-unknown-closure.json",
    "unknowns.json",
]

DOC_NAMES = [
    "FIRST_VISIBLE_TRANSITION_RECOVERY.md",
    "START_GAME_CALL_FLOW.md",
    "STARTER_EVENT_INTERPRETER.md",
    "STARTER_ROOM_MUTATIONS.md",
    "STARTER_STAFF_TRANSITION.md",
    "FIRST_STABLE_BOUNDARY.md",
]


def load(name: str) -> dict:
    with (EVIDENCE / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    assert EVIDENCE.is_dir()
    assert (EVIDENCE / "previews/README.md").is_file()
    records = {name: load(name) for name in JSON_NAMES}
    assert all((DOCS / name).is_file() for name in DOC_NAMES)

    ledger = records["checkpoint-ledger.json"]
    assert ledger["status"] == "BLOCKED_SOURCE_LIMITED"
    assert ledger["static_only"] is True
    assert ledger["required_static_test_topics"] == list(range(1, 25))
    constraints = ledger["execution_constraints"]
    assert all(
        constraints[key] is False
        for key in (
            "subagents_used",
            "v8_started",
            "emulator_used",
            "adb_used",
            "live_apk_used",
            "server_started",
            "network_used",
            "browser_used",
            "new_screenshots_taken",
            "full_starter_room_rendered",
        )
    )
    frozen = ledger["frozen_invariants"]
    assert all(value is False for value in frozen.values())

    caller = records["newgame-caller-contract.json"]
    assert caller["method"] == "form.TitleForm.Update"
    assert caller["native"]["direct_call_site"] == "0x01208248"
    assert caller["native"]["direct_call_count_found"] == 1
    assert caller["contract"]["callee_rva"] == "0x1263A70"
    assert caller["contract"]["immediate_post_call"][-1].startswith("No direct EventData.StartEvent")

    start_flow = records["startgame-control-flow.json"]
    assert start_flow["form_type"] == 73
    assert start_flow["native"]["init_start_game_rva"] == "0x112A27C"
    assert start_flow["native"]["update_start_game_rva"] == "0x119EF6C"
    assert all(not step["direct_newgame_or_event_call"] for step in start_flow["flow"][:3])
    assert start_flow["terminal_selection_contract"]["terminal_owner"] == "TitleForm.Update"

    selection = records["starter-event-selection.json"]
    assert selection["selection_contract"]["selected_starter_event_ids"] == [0]
    assert selection["asset_row"]["term_script"] == [[3, 1, 4]]
    assert selection["asset_row"]["exec_script"] == [[0, 0], [1, 10]]
    assert selection["event_zero_execution"]["commands"] == [
        {"line": 0, "opcode": 0, "name": "SCR_TALK", "parameters": [0, 0]},
        {"line": 1, "opcode": 1, "name": "SCR_DELAY", "parameters": [10]},
    ]

    command_map = records["starter-event-command-map.json"]
    assert len(command_map["opcode_jump_table"]) == 16
    assert [row["opcode"] for row in command_map["opcode_jump_table"]] == list(range(16))
    assert command_map["event_zero_handlers"]["SCR_TALK"]["room_mutation"] is False
    assert command_map["event_zero_handlers"]["SCR_TALK"]["staff_pose_write"] is False
    assert command_map["event_zero_handlers"]["SCR_DELAY"]["furniture_mutation"] is False
    assert command_map["interpreter_completion"]["explicit_end_opcode_in_event_0"] is False

    timeline = records["starter-room-mutation-timeline.json"]
    assert [step["id"] for step in timeline["timeline"]] == [
        "T0",
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7",
        "T8",
        "T9",
        "T10",
    ]
    assert timeline["event_zero_mutation_summary"] == {
        "room": False,
        "furniture": False,
        "wall": False,
        "door": False,
        "staff_pose": False,
        "workstations": "bootstrap values remain the only source-backed values",
        "equipment": "bootstrap values remain the only source-backed values",
    }

    wall_door = records["starter-wall-door-transition.json"]
    assert wall_door["bootstrap_source"]["wall"]["wall_asset"] == "wall_00.png"
    assert wall_door["bootstrap_source"]["door"]["cell"] == [8, 4]
    assert wall_door["transition_proof"]["event_zero_wall_write"] is False
    assert wall_door["transition_proof"]["event_zero_door_write"] is False

    manifest = records["first-visible-stable-manifest.json"]
    assert manifest["status"] == "PARTIAL_SOURCE_LIMITED"
    assert manifest["room"]["width"] == 14 and manifest["room"]["height"] == 14
    assert [item["raw_furniture"] for item in manifest["workstations"]] == [3, 3, 3]
    assert [item["raw_furniture"] for item in manifest["equipment"]] == [12, 26, 56]
    assert len(manifest["staff"]) == 3
    assert all(item["direction"] == "unknown" for item in manifest["staff"])
    assert manifest["render"]["full_starter_room_rendered"] is False
    assert manifest["render"]["isolated_previews_generated"] is False

    staff = records["starter-staff-transition.json"]
    assert len(staff["bootstrap_staff"]) == 3
    assert staff["event_zero_effect"]["direction_write"] is False
    assert all(value == "unknown" for pose in staff["stable_pose"].values() for value in pose.values())

    boundary = records["first-stable-boundary-contract.json"]
    assert boundary["predicate"]["game_form_state"] == "GameForm.state_ == STATE_NORMAL == 2"
    assert "AppData.ExeEvent(2)" in boundary["predicate"]["event_work"]
    assert boundary["predicate"]["menu"] == "AppData.frmMenu_ is non-null and isSliding_ is false."
    assert boundary["preview_eligibility"]["isolated_preview_allowed"] is False

    closure = records["fs-unknown-closure.json"]
    assert {item["id"] for item in closure["closures"]} == {f"FS-U0{i}" for i in range(1, 7)}
    assert set(closure["blocking_ids"]) == {"FS-U02", "FS-U03", "FS-U04", "FS-U05", "FS-U06"}
    assert records["unknowns.json"]["status"] == "SOURCE_LIMITED"

    preview_files = [path for path in (EVIDENCE / "previews").rglob("*") if path.is_file() and path.suffix.lower() == ".png"]
    assert preview_files == []

    print(
        "first_visible_transition_recovery_test_passed "
        f"artifacts={len(JSON_NAMES)} docs={len(DOC_NAMES)} topics=24 status={ledger['status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
