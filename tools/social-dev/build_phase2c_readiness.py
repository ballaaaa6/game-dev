"""Build the remaining Phase 2C readiness contracts for display-slice-01.

The package closes the source-bounded actor spawn fixture, the coordinate/camera
boundary, and the deterministic behavior/tick contracts. It does not execute
decompiled C# or native code and it does not create the Vite/TypeScript runtime.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"

SCENE_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
OBJECT_PATH = RUNTIME_EVIDENCE / "object_catalog_contract.json"
ACTOR_PATH = RUNTIME_EVIDENCE / "actor_catalog_contract.json"
STAFF_SEMANTICS_PATH = EVIDENCE / "staff_semantics_contract.json"
ROUTE_PATH = EVIDENCE / "phase1d_route_fixture.json"

SOURCE_FILES = {
    "Room": SOURCE_ROOT / "game/Room.cs",
    "Staff": SOURCE_ROOT / "game/Staff.cs",
    "ObjChip": SOURCE_ROOT / "game/ObjChip.cs",
    "Player": SOURCE_ROOT / "game/Player.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
}

EXPECTED_SOURCE_HASHES = {
    "Room": "e8c8916c12f2902898c0de6ce8aa59f8ca0c738dd5c482aa64919b775d90662f",
    "Staff": "9eaf34d6fad6265f69d6b10ca9b3c5baa60f1ad932e4ca7059c7c131292f9d37",
    "ObjChip": "49ed2d780cddcc6cfda40de07206da59b54d5be5d0bfcb6ff03f479877d13947",
    "Player": "4e42c7f40ac6c984c729fdea21ae1048ecfb2120538d03bf4501e53a55f3289e",
    "AppData": "04b0ae97383e0c345b87ac9a18d73fd40fb5592434443f27921fb99394d81bd4",
}

SCHEMA_VERSION = "social-dev-phase2c-readiness-v1"
SPAWN_FIXTURE_SCHEMA_VERSION = "social-dev-actor-spawn-fixture-v1"
SPAWN_VALIDATION_SCHEMA_VERSION = "social-dev-actor-spawn-validation-v1"
CAMERA_SCHEMA_VERSION = "social-dev-camera-coordinate-contract-v1"
BEHAVIOR_SCHEMA_VERSION = "social-dev-actor-behavior-contract-v1"
TICK_SCHEMA_VERSION = "social-dev-tick-order-contract-v1"


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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_ref(path: Path, expected_hash: str | None = None) -> dict[str, Any]:
    require(path.is_file(), f"missing source or evidence file: {path}")
    actual = sha256_file(path)
    return {
        "path": relative_path(path),
        "expected_sha256": expected_hash,
        "actual_sha256": actual,
        "hash_status": "pass" if expected_hash is None or actual == expected_hash else "drift",
    }


def source_slice(name: str, start: int, end: int, purpose: str) -> dict[str, Any]:
    path = SOURCE_FILES[name]
    require(path.is_file(), f"missing source file for {name}")
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    require(1 <= start <= end <= len(lines), f"invalid {name} source range {start}-{end}")
    slice_hash = sha256_bytes("".join(lines[start - 1 : end]).encode("utf-8"))
    actual_file_hash = sha256_file(path)
    expected_file_hash = EXPECTED_SOURCE_HASHES[name]
    return {
        "type": name,
        "file": relative_path(path),
        "line_start": start,
        "line_end": end,
        "purpose": purpose,
        "file_sha256": actual_file_hash,
        "slice_sha256": slice_hash,
        "expected_file_sha256": expected_file_hash,
        "hash_status": "pass" if actual_file_hash == expected_file_hash else "drift",
        "status": "evidence_only",
    }


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def contract_ref(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    return {
        "path": relative_path(path),
        "sha256": sha256_file(path),
        "status": payload.get("status"),
        "semantic_status": payload.get("semantic_status"),
    }


def build_package() -> dict[str, Any]:
    scene = load_json(SCENE_PATH)
    objects = load_json(OBJECT_PATH)
    actors = load_json(ACTOR_PATH)
    semantics = load_json(STAFF_SEMANTICS_PATH)
    route = load_json(ROUTE_PATH)

    require(scene["status"] == "pass" and scene["semantic_status"] == "approved_for_runtime_contract", "SceneCatalog gate failed")
    require(objects["status"] == "pass" and objects["semantic_status"] == "approved_for_runtime_contract", "ObjectCatalog gate failed")
    require(actors["status"] == "pass" and actors["semantic_status"] == "approved_for_runtime_contract", "ActorCatalog gate failed")
    require(semantics["status"] == "pass", "staff semantics gate failed")

    scene_record = scene["scenes"][0]
    require(scene_record["id"] == "room:0", "unexpected scene identity")
    door_cells = scene_record["door"]["cells"]
    require(len(door_cells) == 1 and door_cells[0]["raw_map_value"] == 5, "door fixture is not closed")
    door = door_cells[0]
    door_x = int(door["x"])
    door_y = int(door["y"])

    base_x = (door_x + door_y) * 20
    base_y = (door_y - door_x) * 10
    cell_origin = [base_x + 20, base_y + 18]
    spawn_position = [base_x + 40, base_y + 9]
    standing_positions = [
        [base_x + 34, base_y + 25],
        [base_x + 6, base_y + 11],
        [base_x + 34, base_y + 11],
        [base_x + 6, base_y + 25],
    ]

    selected_actor_ids = ["actor:staff:0", "actor:staff:1", "actor:staff:2"]
    actor_by_id = {item["id"]: item for item in actors["actors"]}
    require(all(item in actor_by_id for item in selected_actor_ids), "three actor spawn fixture records are required")

    spawn_slices = [
        source_slice("AppData", 13898, 13938, "NewGame creates Staff instances and calls Room.AddStaff for the initial staff vector"),
        source_slice("Room", 5594, 5764, "Room.AddStaff assigns the room door index, position, alpha, speed and room reference"),
        source_slice("Room", 6228, 6277, "Room.GetDoorIndex boundary used by AddStaff"),
    ]
    coordinate_slices = [
        source_slice("Room", 6168, 6227, "Room grid-index to screen-coordinate formulas"),
        source_slice("Room", 1165, 1215, "Room.Draw consumes explicit camera offsets"),
        source_slice("Staff", 7051, 7084, "Staff.Draw forwards the camera offsets to the actor draw path"),
        source_slice("ObjChip", 10419, 10578, "ObjChip.GetStandingPositions deterministic four-point formula"),
    ]
    behavior_slices = [
        source_slice("Room", 993, 1071, "Room.Update iterates staff before object chips"),
        source_slice("Staff", 1216, 1940, "Staff.Update lifecycle and route/state boundary; body remains evidence-only"),
        source_slice("Staff", 7705, 7709, "Staff.ChangeState state mutation boundary"),
        source_slice("Staff", 9410, 9468, "Staff animation advance and room/route API boundary"),
        source_slice("Player", 12082, 12605, "Player.Update lifecycle boundary"),
        source_slice("Player", 12606, 12623, "Player.Frame increments the frame counter"),
    ]
    all_slices = spawn_slices + coordinate_slices + behavior_slices

    spawn_actors: list[dict[str, Any]] = []
    for insertion_index, actor_id in enumerate(selected_actor_ids):
        actor = actor_by_id[actor_id]
        staff_id = actor["source_identity"]["source_id"]
        spawn_actors.append(
            {
                "id": actor_id,
                "status": "verified",
                "semantic_status": "source_bounded_spawn_fixture",
                "source_staff_id": staff_id,
                "insertion_index": insertion_index,
                "scene_ref": "room:0",
                "spawn_cell": {
                    "x": door_x,
                    "y": door_y,
                    "raw_map_value": door["raw_map_value"],
                    "status": "verified",
                    "source_ref": "knowledge/fixtures/accepted/runtime/scene_catalog_contract.json#/scenes/0/door/cells/0",
                },
                "initial_position": {
                    "x": spawn_position[0],
                    "y": spawn_position[1],
                    "formula": {
                        "x": "(door_x + door_y) * 20 + 40",
                        "y": "(door_y - door_x) * 10 + 9",
                    },
                    "status": "derived",
                    "confidence": "high",
                    "source_ref": "sources/raw/1_Click_CSharp_Code update/game/Room.cs:5594-5764",
                    "review_note": "The position is calculated from the verified room door cell and the readable AddStaff assignments; it is not a selected free cell.",
                },
                "initial_fields": {
                    "id_": {"value": insertion_index, "status": "verified", "source_ref": "Room.AddStaff:staff.id_ = index"},
                    "objIndex_": {"value": [door_x, door_y], "status": "verified", "source_ref": "Room.AddStaff:staff.objIndex_ = doorIndex"},
                    "alpha_": {"value": 0, "status": "verified", "source_ref": "Room.AddStaff:staff.alpha_ = 0"},
                    "speed_": {"value": 3, "status": "verified", "source_ref": "Room.AddStaff:staff.speed_ = 3f"},
                    "room_ref": {"value": "room:0", "status": "verified", "source_ref": "Room.AddStaff:staff.room_ = this"},
                },
                "initial_state_boundary": {
                    "state_": {"value": 0, "label": "STATE_NORMAL", "status": "derived", "source_ref": "Staff.cs:28 and C# field default"},
                    "moveMode_": {"value": 0, "label": "MOVE_MODE_STAY", "status": "derived", "source_ref": "Staff.cs:82 and Staff.Init default boundary"},
                    "flag_": {"value": 0, "status": "derived", "source_ref": "Staff.cs:224 field declaration and C# field default"},
                    "note": "Zero defaults are retained as derived initialization facts; no decompiler body is executed.",
                },
                "desk_assignment": {
                    "status": "deferred",
                    "reason": "GetStaffEmptyObjTypeOf body is not sufficiently readable; desk binding is outside the spawn cell fixture.",
                },
            }
        )

    spawn_fixture = {
        "schema_version": SPAWN_FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-actor-spawn-fixture",
        "status": "pass",
        "semantic_status": "deterministic_fixture",
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "contract": contract_ref(SCENE_PATH)},
        "actor_ref": {"catalog_id": "display-slice-01", "contract": contract_ref(ACTOR_PATH)},
        "spawn_rule": {
            "owner": "Room.AddStaff",
            "input": "verified RoomData(0) door cell type 5 at (8,4)",
            "cell_policy": "all selected actors enter through the verified door cell; no free-cell placement is invented",
            "position_policy": "source-bounded AddStaff position formula",
            "status": "verified_source_bounded",
        },
        "door": {
            "cell": [door_x, door_y],
            "raw_type": door["raw_map_value"],
            "screen_base": [base_x, base_y],
            "status": "verified",
        },
        "actors": spawn_actors,
        "minimum_actor_count": 3,
        "collision_policy": "co_located_at_source_spawn_until_behavior_tick_moves_or_hides_actor",
        "provenance": {
            "upstream": [contract_ref(SCENE_PATH), contract_ref(OBJECT_PATH), contract_ref(ACTOR_PATH), file_ref(STAFF_SEMANTICS_PATH)],
            "source_slices": spawn_slices,
            "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports.",
        },
        "limits": [
            "The fixture closes initial entry through the verified door and the fields written by Room.AddStaff.",
            "Desk selection and post-spawn visibility remain behavior concerns and are not guessed here.",
            "The fixture intentionally preserves source co-location; a renderer must not silently fan actors out.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    spawn_fixture["determinism"]["content_hash"] = sha256_bytes(stable_json(without_dynamic(spawn_fixture)).encode("utf-8"))

    camera_contract = {
        "schema_version": CAMERA_SCHEMA_VERSION,
        "package": "social-dev-camera-coordinate-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "contract": contract_ref(SCENE_PATH)},
        "coordinate_system": {
            "grid": {"width": scene_record["grid"]["width"], "height": scene_record["grid"]["height"], "row_axis": "y", "column_axis": "x", "flat_index": "x + y * width", "status": "verified"},
            "cell_origin": {"x": "(x + y) * 20 + 20", "y": "(y - x) * 10 + 18", "status": "verified_source_formula"},
            "standing_positions": {
                "base": {"x": "(x + y) * 20", "y": "(y - x) * 10"},
                "offsets": [[34, 25], [6, 11], [34, 11], [6, 25]],
                "door_fixture_values": standing_positions,
                "status": "verified_native_formula",
            },
            "actor_spawn_position": {"formula": "(x + y) * 20 + 40, (y - x) * 10 + 9", "door_fixture_values": spawn_position, "status": "verified_source_bounded"},
        },
        "camera": {
            "transform": "screen = world + offset",
            "offset_units": "screen pixels in the original integer draw coordinate space",
            "fixture_offset": [0, 0],
            "fixture_scale": 1,
            "fixture_status": "explicit_runtime_fixture_input",
            "source_boundary": "Room.Draw(Graphics, ofx, ofy, drawMode) forwards ofx/ofy to scene draw calls; the original UI's dynamic viewport policy is not inferred.",
        },
        "draw_offset_contract": {"room_draw_parameters": ["ofx", "ofy"], "actor_draw_parameters": ["ofx", "ofy"], "status": "verified_boundary"},
        "provenance": {"source_slices": coordinate_slices, "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports."},
        "limits": [
            "This contract closes coordinate formulas and the camera-offset interface, not a claim about an original default viewport size.",
            "Sprite crop, scale, alpha composition and draw ordering remain renderer contracts.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }

    behavior_profile = actors["behavior_profiles"][0]
    transition_contracts = copy.deepcopy(semantics["state_transition_contracts"])
    behavior_contract = {
        "schema_version": BEHAVIOR_SCHEMA_VERSION,
        "package": "social-dev-actor-behavior-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "scene_ref": {"id": "room:0", "contract": contract_ref(SCENE_PATH)},
        "spawn_ref": {"path": "knowledge/fixtures/accepted/actor_spawn_fixture.json", "content_hash": spawn_fixture["determinism"]["content_hash"]},
        "actor_ref": {"path": relative_path(ACTOR_PATH), "sha256": sha256_file(ACTOR_PATH)},
        "state_labels": copy.deepcopy(semantics["state_constants"]),
        "route_mapping": copy.deepcopy(behavior_profile["route_mapping"]),
        "transitions": transition_contracts,
        "animation_timing": copy.deepcopy(actors["animation_profiles"][0]["typing_rules"]),
        "talk_timing": copy.deepcopy(behavior_profile["talk_timing"]),
        "skill_effect": copy.deepcopy(behavior_profile["skill_effect"]),
        "replay_policy": {
            "route": "use the approved route fixture only; no random route selection in the readiness trace",
            "actor_order": "ascending stable actor id",
            "randomness": "disabled for the fixture",
            "wall_clock": "forbidden; tick count is the only time input",
        },
        "trace": {
            "id": "living-trace-01",
            "actors": selected_actor_ids,
            "route_ref": {"path": relative_path(ROUTE_PATH), "sha256": sha256_file(ROUTE_PATH)},
            "milestones": [
                {"tick": 0, "event": "spawn", "expected": "three actors are created from the source-bounded spawn fixture"},
                {"tick": 1, "event": "idle", "expected_state_label": "STATE_NORMAL", "expected_move_label": "MOVE_MODE_STAY"},
                {"tick": 2, "event": "move", "actor": "actor:staff:0", "route": [[8, 4], [7, 4], [6, 4]], "expected_state_label": "STATE_MOVE"},
                {"tick": 4, "event": "arrive", "actor": "actor:staff:0", "expected": "route is consumed at the verified goal cell"},
                {"tick": 5, "event": "work_or_equipment", "actor": "actor:staff:0", "expected": "only a closed bounded destination transition may be applied"},
                {"tick": 6, "event": "talk", "actors": ["actor:staff:0", "actor:staff:1"], "expected": "talk flags and colleague relation are driven by the closed talk transition"},
                {"tick": 26, "event": "talk_marker", "frame": 20, "expected": "talk timing marker is emitted"},
                {"tick": 76, "event": "talk_marker", "frame": 70, "expected": "talk timing marker is emitted"},
                {"tick": 116, "event": "talk_marker", "frame": 110, "expected": "talk timing marker is emitted"},
                {"tick": 136, "event": "talk_end", "frame": 130, "expected": "talk flags clear and bounded return transition is emitted"},
            ],
            "status": "deterministic_contract_trace",
        },
        "provenance": {"source_slices": behavior_slices, "staff_semantics": file_ref(STAFF_SEMANTICS_PATH), "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports."},
        "limits": [
            "Staff.Update and GetSkill are not ported as whole algorithms; only the approved bounded transitions are exposed.",
            "Desk selection, random gauge distribution and UI event text remain outside this contract.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }

    tick_contract = {
        "schema_version": TICK_SCHEMA_VERSION,
        "package": "social-dev-fixed-tick-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "tick": {"unit": "frame", "step": 1, "source_boundary": "Player.Frame increments frame_ by one", "wall_clock": "not allowed"},
        "owner": "deterministic core state owner",
        "order": [
            {"index": 0, "operation": "increment_frame", "source_ref": "Player.Frame"},
            {"index": 1, "operation": "update_actors_in_stable_id_order", "source_ref": "Room.Update staff loop"},
            {"index": 2, "operation": "update_object_bindings_and_reservations", "source_ref": "Room.Update ObjChip loop"},
            {"index": 3, "operation": "commit_immutable_snapshot", "source_ref": "runtime contract boundary"},
        ],
        "mutation_policy": {"core_only": True, "renderer_may_mutate": False, "ui_may_mutate": False, "source_code_imports": False},
        "trace_ref": {"path": "knowledge/fixtures/accepted/runtime/actor_behavior_contract.json#/trace", "status": "required"},
        "provenance": {"source_slices": behavior_slices, "source_policy": "C# and native artifacts are evidence inputs only; they are not runtime imports."},
        "limits": ["This contract fixes replay order for the display slice; it does not claim that every original gameplay subsystem is reproduced."],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""},
    }

    for payload in (camera_contract, behavior_contract, tick_contract):
        payload["determinism"]["contract_hash"] = sha256_bytes(stable_json(without_dynamic(payload)).encode("utf-8"))

    checks = []

    def check(check_id: str, condition: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append({"id": check_id, "status": "pass" if condition else "fail", "observed": observed, "expected": expected, "note": note})

    check("upstream-catalogs", True, {"scene": scene["status"], "objects": objects["status"], "actors": actors["status"]}, {"all": "pass"}, "All canonical catalogs are approved inputs.")
    check("door-cell", [door_x, door_y] == [8, 4] and door["raw_map_value"] == 5, [door_x, door_y, door["raw_map_value"]], [8, 4, 5], "Spawn uses the verified RoomData door cell.")
    check("minimum-actors", len(spawn_actors) >= 3, len(spawn_actors), ">= 3", "The fixture explicitly contains at least three stable actor IDs.")
    check("spawn-positions", spawn_position == [280, -31], spawn_position, [280, -31], "Room.AddStaff formula is evaluated without selecting a free cell.")
    check("spawn-writes", all(item["initial_fields"]["alpha_"]["value"] == 0 and item["initial_fields"]["speed_"]["value"] == 3 for item in spawn_actors), "alpha=0,speed=3", "alpha=0,speed=3", "The fields explicitly written by AddStaff are retained.")
    check("coordinate-formulas", cell_origin == [260, -22] and standing_positions == [[274, -15], [246, -29], [274, -29], [246, -15]], {"cell_origin": cell_origin, "standing": standing_positions}, {"cell_origin": [260, -22], "standing": [[274, -15], [246, -29], [274, -29], [246, -15]]}, "Coordinate formulas match the closed source/native boundaries.")
    check("camera-boundary", camera_contract["camera"]["transform"] == "screen = world + offset" and camera_contract["camera"]["fixture_offset"] == [0, 0], camera_contract["camera"], {"transform": "screen = world + offset", "fixture_offset": [0, 0]}, "Camera is an explicit offset adapter, not an inferred hidden global.")
    check("behavior-transitions", len(transition_contracts) == 4 and len(behavior_profile["route_mapping"]["entries"]) == 3, {"transitions": len(transition_contracts), "routes": len(behavior_profile["route_mapping"]["entries"])}, {"transitions": 4, "routes": 3}, "Only bounded living-scene transitions are promoted.")
    check("talk-markers", behavior_contract["talk_timing"]["frame_markers"] == [20, 70, 110, 130], behavior_contract["talk_timing"]["frame_markers"], [20, 70, 110, 130], "Talk timing remains source-labelled and deterministic.")
    check("fixed-tick", tick_contract["tick"]["step"] == 1 and [item["index"] for item in tick_contract["order"]] == [0, 1, 2, 3], tick_contract["order"], "frame step 1 and order 0..3", "The runtime contract has one owner and a stable update order.")
    check("source-hashes", all(item["hash_status"] == "pass" for item in all_slices), {"slices": len(all_slices), "statuses": sorted({item["hash_status"] for item in all_slices})}, {"hash_status": "pass"}, "Read-only source slices match their pinned file hashes.")
    check("no-runtime-core", not (ROOT / "runtime/social-dev/core").exists() and not (ROOT / "runtime/social-dev/renderer").exists(), True, True, "Vite/TypeScript core is not started before readiness gates.")

    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    validation = {
        "schema_version": SPAWN_VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {"checks": len(checks), "passed_checks": sum(item["status"] == "pass" for item in checks), "spawned_actors": len(spawn_actors), "source_slices": len(all_slices)},
        "artifact_hashes": {"spawn_fixture": spawn_fixture["determinism"]["content_hash"], "camera_contract": camera_contract["determinism"]["contract_hash"], "behavior_contract": behavior_contract["determinism"]["contract_hash"], "tick_contract": tick_contract["determinism"]["contract_hash"]},
        "phase_boundary": {"phase": "Phase 2C", "runtime_status": "ready_for_vite_typescript_core" if status == "pass" else "blocked", "required_before_core": ["spawn fixture", "camera/coordinate contract", "runtime behavior contract", "fixed tick contract"]},
    }
    return {"spawn_fixture": spawn_fixture, "validation": validation, "spawn_contract": {"schema_version": SCHEMA_VERSION, "package": "social-dev-actor-spawn-contract", "status": status, "semantic_status": "approved_for_runtime_contract" if status == "pass" else "invalid", "fixture_ref": {"path": "knowledge/fixtures/accepted/actor_spawn_fixture.json", "content_hash": spawn_fixture["determinism"]["content_hash"]}, "actors": copy.deepcopy(spawn_actors), "spawn_rule": copy.deepcopy(spawn_fixture["spawn_rule"]), "provenance": copy.deepcopy(spawn_fixture["provenance"]), "limits": copy.deepcopy(spawn_fixture["limits"]), "runtime_readiness": {"status": "ready_for_camera_behavior_contracts" if status == "pass" else "blocked"}, "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""}}, "camera_contract": camera_contract, "behavior_contract": behavior_contract, "tick_contract": tick_contract}


def finalize_package(package: dict[str, Any]) -> dict[str, Any]:
    spawn_contract = package["spawn_contract"]
    spawn_contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(without_dynamic(spawn_contract)).encode("utf-8"))
    package["validation"]["artifact_hashes"]["spawn_contract"] = spawn_contract["determinism"]["contract_hash"]
    return package


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    package = finalize_package(build_package())
    spawn_contract = package["spawn_contract"]
    write_json(evidence_dir / "actor_spawn_fixture.json", package["spawn_fixture"])
    write_json(evidence_dir / "actor_spawn_validation.json", package["validation"])
    write_json(runtime_dir / "actor_spawn_contract.json", spawn_contract)
    write_json(runtime_dir / "camera_coordinate_contract.json", package["camera_contract"])
    write_json(runtime_dir / "actor_behavior_contract.json", package["behavior_contract"])
    write_json(runtime_dir / "tick_order_contract.json", package["tick_contract"])
    print(f"phase2c_readiness_complete status={package['validation']['status']} checks={package['validation']['counts']['passed_checks']}/{package['validation']['counts']['checks']} actors={package['validation']['counts']['spawned_actors']} spawn_contract_hash={spawn_contract['determinism']['contract_hash']}")
    return 0 if package["validation"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
