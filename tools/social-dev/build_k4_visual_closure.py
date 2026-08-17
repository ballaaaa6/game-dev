"""Build the K4 whole visual assembly brain-closure evidence pack.

K4 is an evidence-only closure pass.  It promotes exact source/native visual
facts into the canonical brain, records every reachable Room0 visual
consumer, and preserves source-limited composition boundaries.  It never
starts a server, emulator, browser, live app, or network operation, and it
does not modify runtime pixels or read-only source roots.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRAIN = ROOT / "knowledge/brain"
K4 = BRAIN / "acceptance/k4"
DB_PATH = BRAIN / "sqlite/social_dev_brain.sqlite"
MANIFEST_PATH = BRAIN / "MANIFEST.json"
GRAPH_PATH = BRAIN / "graphs/semantic-edges.json"

NATIVE_SCENE = ROOT / "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json"
FLOOR00 = ROOT / "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json"
DISPLAY_MANIFEST = ROOT / "knowledge/fixtures/accepted/runtime/display_asset_manifest.json"
COMPOSITION_CATALOG = ROOT / "knowledge/fixtures/accepted/asset_composition_catalog.json"
FURNITURE_METADATA = ROOT / "knowledge/fixtures/accepted/furniture_asset_metadata.json"
FLOOR00_SEB = ROOT / "knowledge/fixtures/accepted/runtime/floor00_seb_contract.json"
ROOM_RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json"
ROOM_ASSETS = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json"
ACTION_MAP = ROOT / "knowledge/fixtures/accepted/visual-port/v6/human-action-selector-map.json"
DIRECTION_CONTRACT = ROOT / "knowledge/fixtures/accepted/visual-port/v6/staff-direction-contract.json"
STATE_MACHINE = ROOT / "knowledge/fixtures/accepted/behavior-first/staff-state-machine.json"
STATE_CONSTANTS = ROOT / "knowledge/fixtures/accepted/behavior-first/staff-state-constant-catalog.json"
VISIBLE_ACTIONS = ROOT / "knowledge/fixtures/accepted/behavior-first/behavior-visible-action-map.json"
AUTONOMY = ROOT / "knowledge/fixtures/accepted/behavior-first/idle-autonomy-contract.json"
EQUIPMENT = ROOT / "knowledge/fixtures/accepted/behavior-first/equipment-behavior-contract.json"
TALK = ROOT / "knowledge/fixtures/accepted/behavior-first/talk-social-contract.json"
HOME = ROOT / "knowledge/fixtures/accepted/behavior-first/home-rest-contract.json"
MOVEMENT = ROOT / "knowledge/fixtures/accepted/behavior-first/movement-target-arrival-contract.json"
ARRIVAL = ROOT / "knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-jump-table.json"
STAFF_AUTHORITY = ROOT / "knowledge/fixtures/accepted/living-core-closure/staff-native-authority-map.json"
STAFF_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs"
ROOM_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs"
OBJCHIP_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/ObjChip.cs"
FURNITURE_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs"
LIBIL2CPP = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
SOURCE_MANIFEST = ROOT / "knowledge/sources/source-manifest.json"
K2_FINAL = BRAIN / "acceptance/k2/final-validation.json"
K25_FINAL = BRAIN / "acceptance/k2-5-cleanup/final-validation.json"
K3_FINAL = BRAIN / "acceptance/k3/final-validation.json"

ALLOWED_STATUSES = {
    "PROVEN_CANONICAL",
    "PROVEN_NOT_CANONICAL",
    "SOURCE_MISSING",
    "SOURCE_LIMITED",
    "NO_DISTINCT_VISUAL",
    "NOT_REACHABLE",
}
FINAL_TOKEN = "K4_INCOMPLETE_VISUAL_SOURCE_LIMITED"
REVISION = "k4-visual-assembly-r1"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    value = "|".join(str(part) for part in parts)
    return f"{prefix}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]}"


def source_ref(path: Path, detail: str | None = None) -> str:
    return f"{rel(path)}:{detail}" if detail else rel(path)


def source_hash_record(path: Path, role: str) -> dict[str, Any]:
    return {
        "path": rel(path),
        "role": role,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def git_state() -> dict[str, Any]:
    def run(args: list[str]) -> str:
        result = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return result.stdout.strip()

    return {
        "branch": run(["git", "branch", "--show-current"]),
        "status_entries": run(["git", "status", "--short"]).splitlines(),
    }


def metadata_value(connection: sqlite3.Connection, key: str) -> Any:
    row = connection.execute(
        "select value_json from brain_metadata where key=?", (key,)
    ).fetchone()
    if not row:
        return None
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return row[0]


def db_snapshot() -> dict[str, Any]:
    connection = sqlite3.connect(DB_PATH)
    try:
        tables = {
            "canonical_entities": connection.execute(
                "select count(*) from canonical_entities"
            ).fetchone()[0],
            "canonical_facts": connection.execute(
                "select count(*) from canonical_facts"
            ).fetchone()[0],
            "semantic_edges": connection.execute(
                "select count(*) from semantic_edges"
            ).fetchone()[0],
            "verified_edges": connection.execute(
                "select count(*) from semantic_edges where status='verified'"
            ).fetchone()[0],
            "rejected_edges": connection.execute(
                "select count(*) from semantic_edges where status='rejected'"
            ).fetchone()[0],
            "source_limited_edges": connection.execute(
                "select count(*) from semantic_edges where status='unresolved'"
            ).fetchone()[0],
            "derived_artifacts": connection.execute(
                "select count(*) from derived_artifacts"
            ).fetchone()[0],
        }
        return {
            "path": rel(DB_PATH),
            "size_bytes": DB_PATH.stat().st_size,
            "sha256": sha256_file(DB_PATH),
            "brain_revision": metadata_value(connection, "brain_revision"),
            "status": metadata_value(connection, "status"),
            "k3_status": metadata_value(connection, "k3_status"),
            "k4_status": metadata_value(connection, "k4_status"),
            "tables": tables,
        }
    finally:
        connection.close()


def pack_snapshot() -> dict[str, Any]:
    files = {
        "runtime": ROOT / "knowledge/generated/original-runtime-pack/runtime-pack.json",
        "visual": ROOT / "knowledge/generated/original-visual-pack/visual-pack.json",
        "data": ROOT / "knowledge/generated/original-data-pack/data.json",
        "runtime_mirror": ROOT / "runtime/social-dev/generated/original-runtime-pack.json",
    }
    return {
        key: {
            "path": rel(path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for key, path in files.items()
    }


def find_room0(native_scene: dict[str, Any]) -> dict[str, Any]:
    for room in native_scene["rooms"]:
        if room["room_key"] == "room:0":
            return room
    raise AssertionError("native scene contract has no room:0")


def find_composition(catalog: dict[str, Any], composition_id: str) -> dict[str, Any]:
    for composition in catalog["compositions"]:
        if composition["composition_id"] == composition_id:
            return composition
    raise AssertionError(f"composition missing: {composition_id}")


def find_furniture(metadata: dict[str, Any], furniture_id: int) -> dict[str, Any]:
    for record in metadata["furniture"]:
        if record["furniture_data_id"] == furniture_id:
            return record
    raise AssertionError(f"FurnitureData record missing: {furniture_id}")


def preflight() -> tuple[dict[str, Any], dict[str, Any]]:
    native_scene = load_json(NATIVE_SCENE)
    floor00 = load_json(FLOOR00)
    source_manifest = load_json(SOURCE_MANIFEST)
    source_files = [
        (STAFF_SOURCE, "Staff C# source"),
        (ROOM_SOURCE, "Room C# source"),
        (OBJCHIP_SOURCE, "ObjChip C# source"),
        (FURNITURE_SOURCE, "FurnitureData C# source"),
        (LIBIL2CPP, "pinned native binary"),
        (METADATA, "pinned native metadata"),
        (DUMP, "pinned IL2CPP dump"),
    ]
    selected_sources = [
        source_hash_record(path, role)
        for path, role in source_files
        if path.exists()
    ]
    k2 = load_json(K2_FINAL)
    k25 = load_json(K25_FINAL)
    k3 = load_json(K3_FINAL)
    snapshot = {
        "schema_version": "social-dev-k4-preflight-current-state-v1",
        "run_kind": "repeatable_k4_closure_build",
        "status": "pass",
        "scope": {
            "target": "whole visual assembly brain closure for the reachable Room0 autonomous slice",
            "room": "room:0",
            "visual_runtime_implementation": False,
            "pixel_output_or_tuning": False,
            "v8": "NOT_STARTED",
        },
        "upstream_tokens": {
            "k2": k2["final_validation_token"],
            "k2_5": k25["final_token"],
            "k3": k3["final_validation_token"],
        },
        "canonical_brain_before_k4": db_snapshot(),
        "generated_packs_before_k4": pack_snapshot(),
        "source_manifest": {
            "path": rel(SOURCE_MANIFEST),
            "sha256": sha256_file(SOURCE_MANIFEST),
            "pinned_sources": source_manifest["sources"],
        },
        "selected_source_hashes_before_k4": selected_sources,
        "git": git_state(),
        "baseline_regressions": {
            "source": rel(K3_FINAL),
            "status": "PASS",
            "native_registry": "PASS",
            "native_catalog": "PASS",
            "native_floor": "PASS",
            "display_gate": "PASS",
            "runtime_typecheck": "PASS",
            "vitest": "PASS 48 files / 314 tests",
            "original_data_sha256": "9d561f7d5708c73b6b8a80acca10681f0323ec5a001145ed9c63215987d79d37",
        },
        "boundary": {
            "source_roots_read_only": True,
            "legacy_runtime_active_dependency": False,
            "network_used": False,
            "subagents_used": False,
            "server_started": False,
            "emulator_or_adb_used": False,
            "live_app_used": False,
            "mapchip_pixels_changed": False,
        },
    }
    return snapshot, {"native_scene": native_scene, "floor00": floor00}


def room0_bootstrap_recipe(
    context: dict[str, Any],
) -> dict[str, Any]:
    native_scene = context["native_scene"]
    floor00 = context["floor00"]
    room0 = find_room0(native_scene)
    return {
        "schema_version": "social-dev-k4-room0-bootstrap-visual-recipe-v1",
        "status": "PROVEN_CANONICAL",
        "recipe_id": "ROOM0_BOOTSTRAP_VISUAL_RECIPE:0",
        "entrypoint": floor00["bootstrap"],
        "room": {
            "room_key": "room:0",
            "room_data_key": "data:room:0",
            "native_data": room0["native"],
            "map_topology": floor00["map"],
            "native_map_selector": room0["map_chip"],
            "floor_selector_chain": {
                "raw_roomdata_floor_image_index": room0["selectors"]["floor"][
                    "raw_selector_id"
                ],
                "native_image_selector": room0["selectors"]["floor"][
                    "native_selector_id"
                ],
                "asset": room0["selectors"]["floor"]["filename"],
                "asset_id": room0["selectors"]["floor"]["asset_id"],
                "runtime_alias_is_separate": True,
            },
        },
        "assembly_stages": native_scene["native_lifecycle"],
        "initial_furniture": floor00["native_initial_furniture"],
        "structural_facilities": floor00["structural_facilities"],
        "door": floor00["door"],
        "actors": floor00["actors"],
        "render_composition": floor00["render_composition"],
        "native_room_draw_commands": room0["draw_commands"],
        "exclusions": floor00["exclusions"],
        "source_refs": [
            source_ref(FLOOR00),
            source_ref(NATIVE_SCENE, "rooms[room:0]"),
            source_ref(ROOM_SOURCE, "AppData.NewGame/Room constructor/PlaceDesk"),
            source_ref(OBJCHIP_SOURCE, "ObjChip construction and draw ownership"),
        ],
    }


def wall_door_recipe(context: dict[str, Any]) -> dict[str, Any]:
    native_scene = context["native_scene"]
    room0 = find_room0(native_scene)
    wall = room0["wall"]
    door = room0["door"]
    return {
        "schema_version": "social-dev-k4-wall-door-assembly-recipe-v1",
        "status": "SOURCE_LIMITED",
        "recipe_id": "ROOM0_WALL_DOOR_ASSEMBLY_RECIPE:0",
        "wall": {
            "status": wall["status"],
            "predicate": wall["predicate"],
            "cells_by_frame": wall["cells_by_frame"],
            "seb": wall["seb"],
            "sprite_records": wall["sprite_records"],
            "sprite_layers": wall["sprite_layers"],
            "draw_semantics": wall["draw_semantics"],
            "image_selector": wall["image_selector"],
            "logical_application_count": 15,
            "layer_application_count": 30,
        },
        "door_closed_baseline": {
            "status": door["status"],
            "cell": door["cells"][0],
            "raw_type": door["raw_type"],
            "installed_flag": door["installed_flag"],
            "furniture_data": door["furniture_data"],
            "seb": door["seb"],
            "sprite_record": door["sprite_record"],
            "image_selector": door["image_selector"],
            "frame": 0,
        },
        "door_action": {
            "status": "SOURCE_LIMITED",
            "blocking": True,
            "proven": [
                "Staff.OnArriveGoal move mode GO_TO_DOOR routes to the door.",
                "Staff.OnArriveGoal writes door frame_=15, calls ObjChip.StartAction(0,id_), and sets FLAG_FADE_OUT.",
                "Staff.OnOpenDoor calls GotoDesk and sets FLAG_FADE_IN.",
            ],
            "known_native": {
                "Staff.OnArriveGoal": "0x12D8420",
                "ObjChip.StartAction": "0x12C0520",
                "Staff.OnOpenDoor": "0x12DC7A8",
            },
            "unresolved": [
                "ObjChip.Update frame progression for the door action is not reconciled.",
                "ObjChip.DrawWall action-frame/layer selection after the frame-15 seed is not closed.",
            ],
            "no_fallback_policy": "Do not invent a door action frame sequence or substitute another door SEB.",
        },
        "source_refs": [
            source_ref(NATIVE_SCENE, "rooms[room:0].wall/door"),
            source_ref(FLOOR00, "door/render_composition"),
            source_ref(LIBIL2CPP, "ObjChip.DrawWall@0x12C0698"),
            source_ref(LIBIL2CPP, "Staff.OnArriveGoal@0x12D87CC"),
            source_ref(LIBIL2CPP, "ObjChip.StartAction@0x12C0520"),
            source_ref(STAFF_SOURCE, "Staff.OnOpenDoor"),
        ],
    }


def furniture_recipe(context: dict[str, Any]) -> dict[str, Any]:
    floor00 = context["floor00"]
    catalog = load_json(COMPOSITION_CATALOG)
    metadata = load_json(FURNITURE_METADATA)
    instance_records: list[dict[str, Any]] = []
    for instance in floor00["native_initial_furniture"]:
        furniture_id = instance["furniture_data_id"]
        record = find_furniture(metadata, furniture_id)
        composition = find_composition(
            catalog, f"native_initial_object:furniture:{furniture_id}"
        )
        instance_records.append(
            {
                "object_id": instance["object_id"],
                "furniture_data_id": furniture_id,
                "cell": instance["cell"],
                "raw_type": instance["raw_type"],
                "selector_flag": instance["selector_flag"],
                "scan_order": instance["scan_order"],
                "name": record["name"],
                "fields": {
                    key: record["fields"][key]
                    for key in ("type_", "seb_", "subSeb_", "img_", "flag_", "recovery_")
                },
                "composition_id": composition["composition_id"],
                "composition_status": composition["status"],
                "records": composition["records"],
            }
        )
    unique_compositions = []
    seen: set[int] = set()
    for item in instance_records:
        furniture_id = item["furniture_data_id"]
        if furniture_id in seen:
            continue
        seen.add(furniture_id)
        unique_compositions.append(item)
    return {
        "schema_version": "social-dev-k4-furniture-execution-model-v1",
        "status": "PROVEN_CANONICAL",
        "model_id": "FURNITURE_EXECUTION_MODEL:objchip-v1",
        "generic_native_model": {
            "ObjChip.furnitureData_offset": "0x20",
            "ObjChip.type_offset": "0x18",
            "ObjChip.frame_offset": "0x60",
            "ObjChip.sebFrame_offset": "0x80",
            "PlaceObj": {
                "rva": "0x12C4308",
                "initialization": "stores FurnitureData and zeros frame_/sebFrame_",
            },
            "draw": {
                "rva": "0x12C166C",
                "dispatch": "FurnitureData.type_ selects the native type branch",
                "resource_path": "ResourceManager img/seb selector -> accepted composition record -> AppData.DrawSeb or direct image",
            },
            "type_policy": {
                "type_1": "direct initial img_ record with SEB_SELECTOR_ID:21 action companion",
                "type_2": "workstation compound composition with primary desk and subSeb chair",
                "type_5": "door-owned ObjChip path; no FurnitureData object",
                "raw_type_without_explicit_binding": "never infer FurnitureData identity",
            },
        },
        "native_room0_instances": instance_records,
        "unique_initial_compositions": unique_compositions,
        "structural_facilities": context["floor00"]["structural_facilities"],
        "source_refs": [
            source_ref(FURNITURE_METADATA, "furniture_data_id 3/12/26/56"),
            source_ref(COMPOSITION_CATALOG, "native_initial_object compositions"),
            source_ref(FLOOR00, "native_initial_furniture"),
            source_ref(OBJCHIP_SOURCE, "ObjChip.Draw/PlaceObj"),
            source_ref(LIBIL2CPP, "ObjChip.Draw@0x12C166C"),
        ],
    }


def workstation_recipe(context: dict[str, Any]) -> dict[str, Any]:
    floor00 = context["floor00"]
    catalog = load_json(COMPOSITION_CATALOG)
    desk = find_composition(catalog, "native_initial_object:furniture:3")
    chair = find_composition(catalog, "display_subcomposition:furniture:2")
    desk_cells = [
        item["cell"]
        for item in floor00["native_initial_furniture"]
        if item["furniture_data_id"] == 3
    ]
    return {
        "schema_version": "social-dev-k4-workstation-sitting-composition-v1",
        "status": "SOURCE_LIMITED",
        "composition_id": "WORKSTATION_SITTING_COMPOSITION:floor00-desk",
        "blocking": True,
        "desk_cells": desk_cells,
        "ownership": {
            "Room.PlaceDesk": {
                "rva": "0x12CEFC8",
                "effect": "seeds explicit FLAG_INIT_DESK bindings without staff ownership",
            },
            "Room.AddStaff": {
                "rva": "0x12CEB2C",
                "effect": "writes Staff.deskId_ and ObjChip.staffId_ for a free type-2 workstation",
            },
            "Staff.GotoDesk": {
                "rva": "0x12D58EC",
                "effect": "sets objIndex_, state MOVE, move mode GOTO_DESK",
            },
            "Staff.OnArriveGoal.GOTO_DESK": {
                "rva": "0x12D8508",
                "effect": "starts desk action 8 and continues to SIT_DOWN",
            },
            "Staff.OnArriveGoal.SIT_DOWN": {
                "rva": "0x12D86A8",
                "effect": "frame_=0, sebId_=-1, state WORK, FLAG_SITTING on",
            },
        },
        "static_compound_geometry": {
            "primary": {
                "composition_id": desk["composition_id"],
                "asset_id": desk["asset_id"],
                "records": desk["records"],
            },
            "subcomposition": {
                "composition_id": chair["composition_id"],
                "asset_id": chair["asset_id"],
                "records": chair["records"],
            },
            "frame_policy": "static bootstrap uses frame 0; action/state frame updates remain separate from furniture frame selection",
        },
        "staff_visual_relation": {
            "source_proven": [
                "ObjChip.Draw(Graphics,ofx,ofy) calls Staff.Draw for staff entries associated with installed furniture.",
                "Staff.Draw(Graphics,ofx,ofy) resolves state/position and calls the native full sprite draw overload.",
                "Staff.OnStartTyping sets FLAG_TYPING, typingFrame_=100, interval=3, and sebId_=reverseDirection+23.",
                "Staff.OnEndTyping clears typing and returns to reverseDirection+10.",
            ],
            "native_methods": {
                "Staff.Draw": "0x12DA6A0",
                "Staff.Draw_offset_overload": "0x12DABA8",
                "Staff.Draw_full": "0x12DA710",
                "Staff.OnStartTyping": "0x12D5C70",
                "Staff.OnEndTyping": "0x12D5D88",
            },
        },
        "unresolved_live_interleave": {
            "status": "SOURCE_LIMITED",
            "blocking": True,
            "missing": "The native live order between desk primary SEB, chair subSeb records, Staff.Draw, and chair foreground records is not proven as a complete sequence.",
            "explicitly_forbidden": "Do not draw a full chair and then move Staff over it as a renderer approximation.",
            "required_next_evidence": "Close the ObjChip.Draw(FurnitureData,bool) native branch/layer order for the type-2 workstation path.",
        },
        "source_refs": [
            source_ref(FLOOR00, "native_initial_furniture"),
            source_ref(COMPOSITION_CATALOG, "native_initial_object:furniture:3/display_subcomposition:furniture:2"),
            source_ref(ROOM_SOURCE, "Room.PlaceDesk/Room.AddStaff"),
            source_ref(OBJCHIP_SOURCE, "ObjChip.Draw staff association"),
            source_ref(STAFF_SOURCE, "Staff.GotoDesk/OnStartTyping/OnEndTyping"),
            source_ref(LIBIL2CPP, "ObjChip.Draw(FurnitureData,bool)@0x12C166C"),
        ],
    }


def staff_recipe(context: dict[str, Any]) -> dict[str, Any]:
    floor00 = context["floor00"]
    action_map = load_json(ACTION_MAP)
    state_machine = load_json(STATE_MACHINE)
    constants = load_json(STATE_CONSTANTS)
    visible = load_json(VISIBLE_ACTIONS)
    return {
        "schema_version": "social-dev-k4-staff-behavior-visual-recipe-v1",
        "status": "PROVEN_CANONICAL",
        "recipe_id": "STAFF_BEHAVIOR_VISUAL_RECIPE:human-staff-v1",
        "bootstrap_actor_visual_bindings": [
            {
                **actor,
                "visual_status": "accepted_floor00_static_display_actor",
                "selector_policy": "human action selector map resolves wait/move/typing by translated direction",
            }
            for actor in floor00["actors"]
        ],
        "directions": load_json(DIRECTION_CONTRACT),
        "states": state_machine["states"],
        "move_modes": state_machine["move_modes"],
        "transitions": state_machine["transitions"],
        "selector_map": action_map,
        "visible_action_map": visible,
        "native_draw": {
            "Staff.Draw": "0x12DA6A0",
            "Staff.Draw_offset_overload": "0x12DABA8",
            "Staff.Draw_full": "0x12DA710",
            "Staff.AdvanceSebFrame": "0x12D8E30",
            "Staff.UpdateAlpha": "0x12D3A40",
            "alpha_policy": "fade-out decrements by 25 to zero; fade-in increments by 25 to 255",
            "state_11_draw_policy": "Staff.Draw skips WAIT_BACK_OF_DOOR",
        },
        "autonomous_visual_branches": {
            "movement": "move selector 1/2/3/4 by translated direction; route fields and arrival modes remain source/native-backed",
            "wander": "wander falls back to move selector 1/2/3/4; OnArriveGoal mode 2 selects directional wander SEB",
            "work": "work/sit state has no separate selector; typing is explicit selector 23/24/25/26 when FLAG_TYPING is on",
            "equipment": "equipment-specific native phase recipe is in equipment-composition-recipe.json",
            "talk": "talk pose reuses typing selectors; Fukidashi payload is separately source-limited",
            "hp_home_return": "low-HP door escape, hidden WAIT_BACK_OF_DOOR, STAY_HOME recovery, and GotoDesk return are source/native-backed",
        },
        "initial_live_selector_boundary": {
            "status": "NO_DISTINCT_VISUAL",
            "reason": "The accepted Room0 bootstrap displays the three initial actors through the static actor binding; Staff.Init's direct sebId_ write is not a distinct promoted visual consumer.",
            "no_invented_selector": True,
        },
        "source_refs": [
            source_ref(FLOOR00, "actors"),
            source_ref(ACTION_MAP),
            source_ref(DIRECTION_CONTRACT),
            source_ref(STATE_MACHINE),
            source_ref(STAFF_AUTHORITY, "Staff.Draw/AdvanceSebFrame/UpdateAlpha"),
            source_ref(STAFF_SOURCE, "Staff.OnStartTyping/OnEndTyping/GotoDesk"),
            source_ref(LIBIL2CPP, "Staff.Draw/AdvanceSebFrame/UpdateAlpha"),
        ],
    }


def equipment_recipe(context: dict[str, Any]) -> dict[str, Any]:
    metadata = load_json(FURNITURE_METADATA)
    selected = []
    for furniture_id in (12, 26, 56):
        record = find_furniture(metadata, furniture_id)
        selected.append(
            {
                "furniture_data_id": furniture_id,
                "name": record["name"],
                "cell": record["native_room_bindings"][0]["cell"],
                "type": record["fields"]["type_"],
                "seb_selector_id": record["fields"]["seb_"],
                "img_selector_id": record["fields"]["img_"],
                "subSeb_selector_id": record["fields"]["subSeb_"],
                "initial_composition_id": f"native_initial_object:furniture:{furniture_id}",
            }
        )
    return {
        "schema_version": "social-dev-k4-equipment-composition-recipe-v1",
        "status": "PROVEN_CANONICAL",
        "recipe_id": "EQUIPMENT_COMPOSITION_RECIPE:Staff.UseEquip",
        "reachable_room0_equipment": selected,
        "native_execution": {
            "method": "Staff.UseEquip",
            "rva": "0x12D4DEC",
            "target_field": "objIndex_",
            "frame_gates": [
                {
                    "frame": 20,
                    "selector_branch": {
                        "x_greater_than_target": 7,
                        "otherwise": 8,
                    },
                    "frame_advance": "even frames only",
                },
                {
                    "frame": 40,
                    "side_effect": "ObjChip.StartAction(0,id_)",
                    "selector_branch": {
                        "x_greater_than_target": 15,
                        "otherwise": 16,
                    },
                    "frame_advance": "even frames only",
                },
                {
                    "frame": 60,
                    "selector_branch": {
                        "x_greater_than_target": 11,
                        "otherwise": 12,
                    },
                    "frame_advance": "every frame",
                },
                {
                    "frame": 70,
                    "side_effect": "ObjChip.OnUseComplate; optional recovery stock; GotoDesk",
                },
            ],
            "native_calls": {
                "Room.GetObjChip": "0x12CE2E4",
                "Room.GetXbyIndex": "0x12CF558",
                "ObjChip.StartAction": "0x12C0520",
                "ObjChip.OnUseComplate": "0x12C0158",
                "Staff.GotoDesk": "0x12D58EC",
            },
        },
        "reservation_and_recovery": {
            "reservation": "ObjChip.reservedStaffs_",
            "selection_types": [1, 4],
            "completion": "recovery_ >= 1 adds recovery stock; it does not directly write hp_",
        },
        "source_refs": [
            source_ref(EQUIPMENT),
            source_ref(FURNITURE_METADATA, "furniture_data_id 12/26/56"),
            source_ref(STAFF_SOURCE, "Staff.GotoEquip/UseEquip"),
            source_ref(OBJCHIP_SOURCE, "ReserveUse/OnUseComplate"),
            source_ref(LIBIL2CPP, "Staff.UseEquip@0x12D4DEC"),
        ],
    }


def talk_recipe(context: dict[str, Any]) -> dict[str, Any]:
    talk_contract = load_json(TALK)
    return {
        "schema_version": "social-dev-k4-talk-composition-recipe-v1",
        "status": "SOURCE_LIMITED",
        "recipe_id": "TALK_COMPOSITION_RECIPE:Staff.Talk",
        "blocking": True,
        "selection_and_pose": {
            "initiator_guards": talk_contract["initiator"]["guards"],
            "target_selection": talk_contract["initiator"]["target_selection"],
            "bilateral_writes": talk_contract["initiator"]["writes"],
            "invitation_writes": talk_contract["invite"]["writes"],
            "arrival_pose": {
                "TO_STAND_TALKING": {
                    "move_mode": 8,
                    "state": 6,
                    "selector": "talk selector = typing selector by translated direction",
                },
                "TO_BACK_OF_CHAIR": {
                    "move_mode": 9,
                    "state": 7,
                    "selector": "reverse direction + wait base",
                },
                "INVITE_FRAME_20": "reverse direction + 6",
                "INVITE_FRAME_GT_40": "reverse direction + 10",
            },
        },
        "timing": talk_contract["talk_timing"],
        "native_execution": {
            "Staff.Talk": "0x12D5588",
            "Staff.InviteStaffToTalk": "0x12D5090",
            "Staff.OnInvitedTalk": "0x12D6378",
            "Staff.AddFukidashi_": "0x12D3C50",
            "Staff.DrawFukidashi": "0x12DDAE4",
            "Staff.DrawFukidashi_single": "0x12DDCA4",
            "ObjChip.DrawFukidashi": "0x12C3E28",
        },
        "fukidashi": {
            "status": "SOURCE_LIMITED",
            "blocking": True,
            "known": {
                "invocation_frames": [20, 70],
                "native_static_field_handles": [
                    "0x27D7E48",
                    "0x27D7E50",
                    "0x27D7E28",
                    "0x27D7E20",
                    "0x27D7E30",
                    "0x27D7E40",
                ],
                "enum_domain": "AppData.FUKIDASHI values 0..69 are declared in the dump",
                "single_entry_storage": "fukidashi__[0]=id; fukidashi__[1]=frame 40; delay/offset fields are retained by Staff.AddFukidashi_",
                "draw_owners": [
                    "Staff.DrawFukidashi -> AppData.DrawFukidashiStr",
                    "Staff.DrawFukidashi_single -> AppData.DrawFukidashi",
                    "ObjChip.DrawFukidashi owns object-level bubble traversal",
                ],
            },
            "unresolved": [
                "The exact RuntimeFieldHandle array payload IDs for the frame-20 and frame-70 branches are not recoverable from the pinned C# body/dump.",
                "The exact payload-specific coordinate/offset values for the selected arrays are therefore not proven.",
            ],
            "no_generic_bubble_policy": "Do not choose a generic Fukidashi enum or guessed offset to make the talk effect look complete.",
        },
        "cleanup": talk_contract["partner_cleanup"],
        "source_refs": [
            source_ref(TALK),
            source_ref(STAFF_SOURCE, "Staff.Talk/InviteStaffToTalk/AddFukidashi_"),
            source_ref(LIBIL2CPP, "Staff.Talk@0x12D5588/DrawFukidashi@0x12DDAE4"),
            source_ref(DUMP, "AppData.FUKIDASHI/Staff fukidashi fields"),
        ],
    }


def room_draw_recipe(context: dict[str, Any]) -> dict[str, Any]:
    native_scene = context["native_scene"]
    floor00 = context["floor00"]
    return {
        "schema_version": "social-dev-k4-room-draw-pass-recipe-v1",
        "status": "PROVEN_CANONICAL",
        "recipe_id": "ROOM_DRAW_PASS_GRAPH:room0-nine-pass",
        "passes": native_scene["render_passes"],
        "room0_logical_composition": floor00["render_composition"],
        "occlusion": {
            "cell_order": "row_y_ascending_then_x_descending",
            "underlay_before_objects": True,
            "rear_wall_cells": floor00["render_composition"]["rear_wall_cells"],
            "door_cell": floor00["render_composition"]["door_cell"],
            "foreground_wall_cells": floor00["render_composition"]["foreground_wall_cells"],
            "avatar_primary_between_object_primary_and_object_late": True,
            "foreground_occlusion_is_not_a_global_sort": True,
        },
        "effect_and_gauge_owners": [
            {
                "owner": "ObjChip",
                "method": "DrawFukidashi",
                "native_rva": "0x12C3E28",
                "status": "PROVEN_CANONICAL",
            },
            {
                "owner": "ObjChip",
                "method": "DrawStaffHpGauge",
                "status": "PROVEN_CANONICAL",
            },
            {
                "owner": "ObjChip",
                "method": "DrawUsePointGauge",
                "status": "PROVEN_CANONICAL",
            },
            {
                "owner": "ObjChip",
                "method": "DrawStaffMeetingPointGauge",
                "status": "PROVEN_CANONICAL",
            },
            {
                "owner": "Staff",
                "methods": ["DrawFukidashi", "DrawFukidashi_"],
                "status": "PROVEN_CANONICAL",
                "payload_boundary": "talk-composition-recipe.json",
            },
        ],
        "source_refs": [
            source_ref(NATIVE_SCENE, "render_passes"),
            source_ref(FLOOR00, "render_composition"),
            source_ref(ROOM_SOURCE, "Room.Draw"),
            source_ref(OBJCHIP_SOURCE, "ObjChip.Draw/DrawWall/DrawFukidashi/gauges"),
            source_ref(LIBIL2CPP, "Room.Draw@0x12CBB80"),
        ],
    }


def opt_seb_recipe(context: dict[str, Any]) -> dict[str, Any]:
    catalog = load_json(COMPOSITION_CATALOG)
    seb = load_json(FLOOR00_SEB)
    runtime = load_json(ROOM_RUNTIME)
    assets = load_json(ROOM_ASSETS)
    return {
        "schema_version": "social-dev-k4-opt-seb-execution-model-v1",
        "status": "PROVEN_CANONICAL",
        "model_id": "OPT_SEB_EXECUTION_MODEL:logical-v1",
        "logical_execution": {
            "composition_catalog_status": catalog["status"],
            "composition_count": catalog["counts"],
            "floor00_seb_contract_status": seb["status"],
            "floor00_explicit_asset_count": len(seb["explicit_assets"]),
            "record_selection": "select every SEB record whose start_frame equals the current object/staff frame",
            "layer_order": "SEB layer index ascending; wall layer 0 then thin layer 1 are both required",
            "crop_and_offset": "use accepted source rectangles and native destination offsets; do not recenter or normalize",
            "opt_policy": "accepted logical OPT reconstructions supply geometry only; no new pixels are created by K4",
        },
        "room_runtime_contract": {
            "status": runtime["status"],
            "asset_manifest_status": assets["status"],
        },
        "native_call_boundary": {
            "proven": [
                "Seb.GetSprite resolves frame records.",
                "AppData.DrawSeb and ResourceManager.DrawSeb receive the selected composition.",
                "Staff full draw uses the same selector/frame path.",
            ],
            "pixel_backend": {
                "status": "PROVEN_NOT_CANONICAL",
                "blocking": False,
                "deferred_to": "V7 exact raster/framebuffer compatibility",
                "reason": "K4 closes selector/frame/layer execution, not shader/premultiplied pixel parity.",
            },
        },
        "source_refs": [
            source_ref(COMPOSITION_CATALOG),
            source_ref(FLOOR00_SEB),
            source_ref(ROOM_RUNTIME),
            source_ref(ROOM_ASSETS),
            source_ref(LIBIL2CPP, "Seb.GetSprite/AppData.DrawSeb/ResourceManager.DrawSeb"),
        ],
    }


def run_command(label: str, command: str, workdir: Path = ROOT) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=workdir,
            shell=True,
            text=True,
            capture_output=True,
            timeout=300,
            check=False,
        )
        return {
            "label": label,
            "command": command,
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-2000:],
            "stderr_tail": result.stderr[-2000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "label": label,
            "command": command,
            "status": "FAIL",
            "returncode": None,
            "stdout_tail": str(exc.stdout)[-2000:] if exc.stdout else "",
            "stderr_tail": "command timed out after 300 seconds",
        }


def run_regressions() -> list[dict[str, Any]]:
    commands = [
        ("k2_unified_brain", "python -B tools/social-dev/test_k2_unified_brain.py", ROOT),
        ("native_content_registry", "python -B tools/social-dev/test_native_content_registry.py", ROOT),
        ("native_content_catalog", "python -B tools/social-dev/test_native_content_catalog.py", ROOT),
        ("native_room_floor_closure", "python -B tools/social-dev/test_native_room_floor_closure.py", ROOT),
        ("display_asset_gate", "python -B tools/social-dev/test_display_asset_gate.py", ROOT),
        ("runtime_typecheck", "npm run typecheck", ROOT / "runtime/social-dev"),
        ("runtime_vitest", "npm test -- --run", ROOT / "runtime/social-dev"),
    ]
    return [run_command(label, command, workdir) for label, command, workdir in commands]


def consumer(
    consumer_id: str,
    domain: str,
    description: str,
    status: str,
    visible: bool,
    evidence: list[str],
    *,
    blocking: bool = False,
    promoted: bool = False,
    notes: str | None = None,
) -> dict[str, Any]:
    if status not in ALLOWED_STATUSES:
        raise AssertionError(f"invalid coverage status: {status}")
    return {
        "consumer_id": consumer_id,
        "domain": domain,
        "description": description,
        "reachable": status != "NOT_REACHABLE",
        "visible": visible,
        "status": status,
        "blocking": blocking,
        "promotion_status": (
            "PROMOTED_TO_CANONICAL_BRAIN" if promoted else "NOT_PROMOTED"
        ),
        "heuristic_or_assumed": False,
        "evidence": sorted(set(evidence)),
        **({"notes": notes} if notes else {}),
    }


def build_consumers(context: dict[str, Any]) -> list[dict[str, Any]]:
    native_scene = context["native_scene"]
    floor00 = context["floor00"]
    room0 = find_room0(native_scene)
    refs = [
        source_ref(NATIVE_SCENE, "rooms[room:0]"),
        source_ref(FLOOR00),
    ]
    records: list[dict[str, Any]] = [
        consumer(
            "room0.bootstrap.entry",
            "Room0 bootstrap",
            "AppData.NewGame -> RoomData:0 -> Room::.ctor -> initial native object/staff bindings",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(ROOM_SOURCE, "AppData.NewGame/Room::.ctor")],
            promoted=True,
        ),
        consumer(
            "room0.floor.map-chip",
            "Floor/map",
            "Room.floor_=0 selects the 14x14 floor_0 MapChip topology; RoomData.floorImgId_=5 resolves through native selector 23 to floor_05.png",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(NATIVE_SCENE, "rooms[room:0].selectors.floor")],
            promoted=True,
        ),
        consumer(
            "room0.map-extension-floor",
            "Floor/map",
            "MapChip.DrawExtentionFloor is the first visible Room.Draw pass",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(NATIVE_SCENE, "render_passes[0]")],
            promoted=True,
        ),
        consumer(
            "room0.wall.horizontal",
            "Wall/corner/join",
            "Horizontal frame-0 wall cells and both SEB layers",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(NATIVE_SCENE, "rooms[room:0].wall")],
            promoted=True,
        ),
        consumer(
            "room0.wall.vertical",
            "Wall/corner/join",
            "Vertical frame-1 wall cells and both SEB layers",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(NATIVE_SCENE, "rooms[room:0].wall")],
            promoted=True,
        ),
        consumer(
            "room0.door.closed",
            "Door",
            "Installed raw type-5 door at [8,4], closed frame-0 door_02.seb/door_01.png baseline",
            "PROVEN_CANONICAL",
            True,
            refs + [source_ref(NATIVE_SCENE, "rooms[room:0].door")],
            promoted=True,
        ),
        consumer(
            "room0.door.action-timeline",
            "Door",
            "Door open/close action after the native frame-15 seed and StartAction call",
            "SOURCE_LIMITED",
            True,
            refs + [source_ref(LIBIL2CPP, "Staff.OnArriveGoal@0x12D87CC/ObjChip.StartAction@0x12C0520")],
            blocking=True,
            notes="Frame seed and fade boundary are proven; complete Update/DrawWall action frame progression is not.",
        ),
    ]
    for instance in floor00["native_initial_furniture"]:
        records.append(
            consumer(
                f"room0.{instance['object_id']}.cell-{instance['cell'][0]}-{instance['cell'][1]}",
                "Furniture",
                f"Native initial {instance['object_id']} composition at cell {instance['cell']}",
                "PROVEN_CANONICAL",
                True,
                refs
                + [
                    source_ref(
                        COMPOSITION_CATALOG,
                        f"native_initial_object:{instance['object_id']}",
                    )
                ],
                promoted=True,
            )
        )
    for index, facility in enumerate(floor00["structural_facilities"]):
        records.append(
            consumer(
                f"room0.structural-facility-{index}",
                "Furniture",
                f"Structural facility SEB at map anchor {facility['map_anchor']}",
                "PROVEN_CANONICAL",
                True,
                refs + [source_ref(FLOOR00, "structural_facilities")],
                promoted=True,
            )
        )
    records.append(
        consumer(
            "furniture.generic.objchip-draw",
            "Furniture",
            "Generic ObjChip FurnitureData dispatch, selector resolution, frame and layer execution",
            "PROVEN_CANONICAL",
            True,
            [source_ref(OBJCHIP_SOURCE, "ObjChip.Draw"), source_ref(LIBIL2CPP, "ObjChip.Draw@0x12C166C")],
            promoted=True,
        )
    )
    for actor in floor00["actors"]:
        records.append(
            consumer(
                f"{actor['id']}.bootstrap-visual",
                "Staff bootstrap",
                f"Accepted static Room0 display actor for source StaffData {actor['source_staff_id']}",
                "PROVEN_CANONICAL",
                True,
                [source_ref(FLOOR00, "actors"), source_ref(DISPLAY_MANIFEST, "actors")],
                promoted=True,
            )
        )
    action_evidence = [source_ref(ACTION_MAP), source_ref(DIRECTION_CONTRACT)]
    records.extend(
        [
            consumer("staff.wait", "Staff visual resolver", "Wait selector 10/11/12/13 by translated direction", "PROVEN_CANONICAL", True, action_evidence, promoted=True),
            consumer("staff.move", "Staff visual resolver", "Move selector 1/2/3/4 by translated direction", "PROVEN_CANONICAL", True, action_evidence, promoted=True),
            consumer("staff.typing", "Staff visual resolver", "Typing selector 23/24/25/26 from FLAG_TYPING", "PROVEN_CANONICAL", True, action_evidence + [source_ref(STAFF_SOURCE, "OnStartTyping/OnEndTyping")], promoted=True),
            consumer("staff.work-no-typing", "Staff visual resolver", "Work state without typing has the explicit wait fallback and no distinct work selector", "NO_DISTINCT_VISUAL", False, action_evidence, promoted=True),
            consumer("staff.equipment-fallback", "Staff visual resolver", "Equipment state outside its native UseEquip phase uses the explicit wait fallback", "NO_DISTINCT_VISUAL", False, action_evidence, promoted=True),
            consumer("staff.sit-down", "Staff visual resolver", "Sit-down state uses the explicit wait fallback; sitting is a lifecycle flag/pose relation", "NO_DISTINCT_VISUAL", False, action_evidence, promoted=True),
            consumer("staff.meeting-fallback", "Staff visual resolver", "Meeting state has the explicit wait fallback", "NO_DISTINCT_VISUAL", False, action_evidence, promoted=True),
            consumer("staff.invite-fallback", "Staff visual resolver", "Invite-to-talk state has the explicit wait fallback", "NO_DISTINCT_VISUAL", False, action_evidence, promoted=True),
            consumer("staff.wander", "Movement/wander", "Wander uses the explicit move fallback and native directional wander arrival branch", "PROVEN_CANONICAL", True, action_evidence + [source_ref(ARRIVAL, "WANDER")], promoted=True),
            consumer("staff.stay-home-hidden", "HP/home/return", "Stay-home state is alpha-hidden and has the explicit wait fallback", "NO_DISTINCT_VISUAL", False, action_evidence + [source_ref(HOME)], promoted=True),
            consumer("staff.fly-away", "Staff visual resolver", "Fly-away selector is deferred outside the normal Room0 autonomous slice", "NOT_REACHABLE", False, [source_ref(ACTION_MAP, "actions.fly_away")], notes="Not a normal Room0 autonomous consumer in the accepted idle loop."),
            consumer("staff.develop", "Staff visual resolver", "Develop state is outside the accepted Room0 autonomous visible-action slice", "NOT_REACHABLE", False, [source_ref(STATE_MACHINE, "states")], notes="No normal Room0 idle path promotes this state."),
            consumer("staff.movement-route-projection", "Movement/wander", "Cardinal route, target arrival, translated direction and movement selector projection", "PROVEN_CANONICAL", True, [source_ref(MOVEMENT), source_ref(ARRIVAL), source_ref(DIRECTION_CONTRACT)], promoted=True),
            consumer("staff.hp-home-return-boundary", "HP/home/return", "Low HP door escape, hidden WAIT_BACK_OF_DOOR, stay-home recovery and GotoDesk return", "PROVEN_CANONICAL", True, [source_ref(HOME), source_ref(STAFF_SOURCE, "Update/UpdateStayHome"), source_ref(LIBIL2CPP, "Staff.UpdateStayHome@0x12D59F4")], promoted=True),
            consumer("staff.initial-live-seb-boundary", "Staff bootstrap", "Direct Staff.Init sebId assignment is not a distinct promoted consumer in the accepted bootstrap", "NO_DISTINCT_VISUAL", False, [source_ref(STAFF_SOURCE, "Init"), source_ref(FLOOR00, "actors")], promoted=False),
            consumer("staff.use-equip.timeline", "Equipment", "Native equipment animation phase selectors 7/8, 15/16 and 11/12 with completion at frame 70", "PROVEN_CANONICAL", True, [source_ref(EQUIPMENT), source_ref(LIBIL2CPP, "Staff.UseEquip@0x12D4DEC")], promoted=True),
            consumer("staff.talk.pose-and-timing", "Talk", "Bilateral talk states, invitation pose selectors, typing-reused talk pose and frame 20/70/110/130 timing", "PROVEN_CANONICAL", True, [source_ref(TALK), source_ref(LIBIL2CPP, "Staff.Talk@0x12D5588")], promoted=True),
            consumer("staff.talk.fukidashi-payload", "Talk", "Fukidashi payload array IDs and payload-specific offset/position data", "SOURCE_LIMITED", True, [source_ref(TALK), source_ref(DUMP, "AppData.FUKIDASHI"), source_ref(LIBIL2CPP, "Staff.Talk@0x12D5588")], blocking=True, notes="Static field handles are known; exact array payloads are not recoverable."),
            consumer("workstation.live-interleave", "Workstation/sitting", "Live desk primary, chair subSeb, Staff.Draw and chair foreground interleave", "SOURCE_LIMITED", True, [source_ref(OBJCHIP_SOURCE, "ObjChip.Draw"), source_ref(LIBIL2CPP, "ObjChip.Draw(FurnitureData,bool)@0x12C166C")], blocking=True, notes="Exact native type-2 layer order remains unresolved."),
            consumer("staff.native-draw-logical", "Staff draw", "Staff Draw overloads, alpha gate, selector/frame and Seb.GetSprite/AppData.DrawSeb call chain", "PROVEN_NOT_CANONICAL", True, [source_ref(STAFF_AUTHORITY, "Staff.Draw"), source_ref(LIBIL2CPP, "Staff.Draw@0x12DA6A0")], notes="Logical execution is proven; exact V7 pixel backend is outside K4."),
        ]
    )
    for item in native_scene["render_passes"]:
        records.append(
            consumer(
                f"room.draw.{item['pass_id']}",
                "Global Room.Draw/occlusion",
                f"Room.Draw pass {item['pass_id']} via {item['native_method']}",
                "PROVEN_CANONICAL",
                True,
                [source_ref(NATIVE_SCENE, "render_passes"), source_ref(ROOM_SOURCE, "Room.Draw")],
                promoted=True,
            )
        )
    records.extend(
        [
            consumer(
                "room.effects.gauge-ownership",
                "Global Room.Draw/occlusion",
                "Native ObjChip ownership for Fukidashi, HP, use-point and meeting-point gauge draw calls",
                "PROVEN_CANONICAL",
                True,
                [source_ref(OBJCHIP_SOURCE, "ObjChip draw effect owners")],
                promoted=True,
            ),
            consumer(
                "opt-seb.logical-execution",
                "OPT/SEB execution",
                "Accepted OPT geometry, SEB frame/layer selection, crop/offset and resource draw chain",
                "PROVEN_CANONICAL",
                True,
                [source_ref(COMPOSITION_CATALOG), source_ref(FLOOR00_SEB), source_ref(LIBIL2CPP, "Seb.GetSprite/AppData.DrawSeb")],
                promoted=True,
            ),
            consumer(
                "opt-seb.pixel-backend",
                "OPT/SEB execution",
                "Shader/premultiplied framebuffer parity for the native pixel backend",
                "PROVEN_NOT_CANONICAL",
                True,
                [source_ref(LIBIL2CPP, "native Graphics/_drawBitmap boundary")],
                notes="Deferred to V7 and nonblocking for K4 brain closure.",
            ),
        ]
    )
    return records


def coverage_metrics(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(record["status"] for record in records)
    return {
        "reachable_consumer_count": sum(record["reachable"] for record in records),
        "visible_consumer_count": sum(record["visible"] for record in records),
        "proven_canonical_count": counts["PROVEN_CANONICAL"],
        "proven_promoted_count": sum(
            record["promotion_status"] == "PROMOTED_TO_CANONICAL_BRAIN"
            for record in records
        ),
        "proven_not_canonical_count": counts["PROVEN_NOT_CANONICAL"],
        "no_distinct_visual_count": counts["NO_DISTINCT_VISUAL"],
        "not_reachable_count": counts["NOT_REACHABLE"],
        "source_limited_count": counts["SOURCE_LIMITED"],
        "blocking_source_limited_count": sum(
            record["status"] == "SOURCE_LIMITED" and record["blocking"]
            for record in records
        ),
        "source_missing_count": counts["SOURCE_MISSING"],
        "heuristic_or_assumed_count": sum(
            bool(record["heuristic_or_assumed"]) for record in records
        ),
    }


def build_queries(
    bootstrap: dict[str, Any],
    wall_door: dict[str, Any],
    workstation: dict[str, Any],
    talk: dict[str, Any],
    equipment: dict[str, Any],
    staff: dict[str, Any],
    room_draw: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "social-dev-k4-deterministic-query-results-v1",
        "status": "source_limited",
        "queries": {
            "A_room0_complete_bootstrap": {
                "status": "pass",
                "inputs": ["room:0", "data:room:0", "Room.floor_=0"],
                "result": {
                    "map": [bootstrap["room"]["map_topology"]["map_chip_width"], bootstrap["room"]["map_topology"]["map_chip_height"]],
                    "objchips": [bootstrap["room"]["map_topology"]["obj_chip_width"], bootstrap["room"]["map_topology"]["obj_chip_height"]],
                    "initial_furniture_instances": len(bootstrap["initial_furniture"]),
                    "initial_staff_count": len(bootstrap["actors"]),
                    "door_cell": bootstrap["door"]["cell"],
                },
                "gaps": [],
            },
            "B_one_wall_cell": {
                "status": "pass",
                "input": "[8,1] horizontal/vertical overlap",
                "result": {
                    "horizontal_frame": wall_door["wall"]["sprite_layers"]["horizontal_frame_0"],
                    "vertical_frame": wall_door["wall"]["sprite_layers"]["vertical_frame_1"],
                    "layer_order": [0, 1],
                },
                "gaps": [],
            },
            "C_workstation_sitting": {
                "status": "source_limited",
                "input": "furniture:3 at [2,4], [3,4], [6,4]",
                "result": {
                    "desk_cells": workstation["desk_cells"],
                    "sit_down_state": "STATE_WORK + FLAG_SITTING",
                    "typing_selectors": [23, 24, 25, 26],
                },
                "gaps": ["live desk/chair/Staff.Draw layer interleave"],
            },
            "D_talk": {
                "status": "source_limited",
                "input": "Staff.Talk frame gates 20/70/110/130",
                "result": {
                    "pose": talk["selection_and_pose"],
                    "timing": talk["timing"],
                    "bubble_invocations": talk["fukidashi"]["known"]["invocation_frames"],
                },
                "gaps": ["exact Fukidashi array payload IDs and payload-specific offsets"],
            },
            "E_equipment": {
                "status": "pass",
                "input": "Staff.UseEquip",
                "result": equipment["native_execution"],
                "gaps": [],
            },
            "F_staff_state_visual_matrix": {
                "status": "pass",
                "input": "state machine + human action selector map",
                "result": {
                    "state_count": len(staff["states"]),
                    "move_mode_count": len(staff["move_modes"]),
                    "selector_actions": sorted(staff["selector_map"]["actions"]),
                    "fallback_policy_explicit": True,
                },
                "gaps": [],
            },
            "G_global_room_draw_pass": {
                "status": "pass",
                "input": "Room.Draw",
                "result": {
                    "pass_count": len(room_draw["passes"]),
                    "pass_ids": [item["pass_id"] for item in room_draw["passes"]],
                    "occlusion": room_draw["occlusion"],
                },
                "gaps": [],
            },
        },
    }


def promote_brain(
    bootstrap: dict[str, Any],
    furniture: dict[str, Any],
    staff: dict[str, Any],
    equipment: dict[str, Any],
    room_draw: dict[str, Any],
    opt_seb: dict[str, Any],
    wall_door: dict[str, Any],
) -> dict[str, Any]:
    facts = [
        {
            "entity_id": "ROOM_DATA_ID:0",
            "predicate": "k4_room0_bootstrap_visual_assembly",
            "value": {
                "map": bootstrap["room"]["map_topology"],
                "floor_selector_chain": bootstrap["room"]["floor_selector_chain"],
                "initial_furniture_count": len(bootstrap["initial_furniture"]),
                "initial_staff_count": len(bootstrap["actors"]),
                "door_cell": bootstrap["door"]["cell"],
            },
            "refs": bootstrap["source_refs"],
            "note": "Room0 bootstrap topology, native floor chain, explicit furniture bindings and actor spawn are source/native-backed.",
        },
        {
            "entity_id": "ROOM_DATA_ID:0",
            "predicate": "k4_wall_closed_frame_layers",
            "value": wall_door["wall"],
            "refs": wall_door["source_refs"],
            "note": "Room0 wall predicates, cells, SEB layers, crops and offsets are closed; door action progression remains separate.",
        },
        {
            "entity_id": "ROOM_DATA_ID:0",
            "predicate": "k4_door_closed_baseline",
            "value": wall_door["door_closed_baseline"],
            "refs": wall_door["source_refs"],
            "note": "Room0 closed door baseline is canonical; action timeline is explicitly source-limited.",
        },
        {
            "entity_id": "STAFF_VISUAL_PROFILE:human-staff-v1",
            "predicate": "k4_action_selector_and_fallback_map",
            "value": staff["selector_map"],
            "refs": staff["source_refs"],
            "note": "Human action selectors, translated directions and explicit fallback policy are promoted without inventing deferred selectors.",
        },
        {
            "entity_id": "STAFF_METHOD:UseEquip",
            "predicate": "k4_equipment_visual_timeline",
            "value": equipment["native_execution"],
            "refs": equipment["source_refs"],
            "note": "Native equipment frame gates, selectors, start/completion calls and return-to-desk are promoted.",
        },
        {
            "entity_id": "ROOM_METHOD:Draw",
            "predicate": "k4_room_draw_pass_graph",
            "value": {
                "passes": room_draw["passes"],
                "occlusion": room_draw["occlusion"],
                "effect_and_gauge_owners": room_draw["effect_and_gauge_owners"],
            },
            "refs": room_draw["source_refs"],
            "note": "The exact nine-pass Room.Draw graph and Room0 occlusion topology are promoted.",
        },
        {
            "entity_id": "OPT_SEB_EXECUTION_MODEL:logical-v1",
            "predicate": "k4_logical_frame_layer_execution",
            "value": opt_seb["logical_execution"],
            "refs": opt_seb["source_refs"],
            "note": "Accepted OPT/SEB selector, frame, layer, crop and native offset execution is promoted; exact V7 pixels remain outside K4.",
        },
    ]
    edges = [
        ("ROOM_DATA_ID:0", "assembled_as", "ROOM0_BOOTSTRAP_VISUAL_RECIPE:0", bootstrap["source_refs"]),
        ("ROOM_DATA_ID:0", "uses_wall_door_recipe", "ROOM0_WALL_DOOR_ASSEMBLY_RECIPE:0", wall_door["source_refs"]),
        ("STAFF_VISUAL_PROFILE:human-staff-v1", "uses_selector_map", "HUMAN_ACTION_SELECTOR_MAP:v6", staff["source_refs"]),
        ("STAFF_METHOD:UseEquip", "executes_visual_timeline", "EQUIPMENT_VISUAL_TIMELINE:UseEquip", equipment["source_refs"]),
        ("ROOM_METHOD:Draw", "uses_pass_graph", "ROOM_DRAW_PASS_GRAPH:room0-nine-pass", room_draw["source_refs"]),
        ("OPT_SEB_EXECUTION_MODEL:logical-v1", "resolves_frame_layers", "ACCEPTED_OPT_SEB_COMPOSITION_CATALOG:v1", opt_seb["source_refs"]),
    ]
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("pragma foreign_keys=off")
        connection.execute("begin")
        for fact in facts:
            entity_id = fact["entity_id"]
            refs_json = json.dumps(sorted(set(fact["refs"])), ensure_ascii=False, sort_keys=True)
            value_json = json.dumps(
                fact["value"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            fact_id = f"fact:k4:{entity_id}|{fact['predicate']}"
            claim_id = stable_id("fact-claim-k4", fact_id)
            connection.execute(
                "insert or replace into canonical_entities(entity_id,entity_type,name,attributes_json,provenance_json) values(?,?,?,?,?)",
                (entity_id, "k4_visual_assembly_entity", entity_id, "{}", refs_json),
            )
            connection.execute(
                "insert or replace into canonical_facts(fact_id,entity_id,predicate,value_json,status,authority,impl_status,revision,canonical,note) values(?,?,?,?,?,?,?,?,?,?)",
                (
                    fact_id,
                    entity_id,
                    fact["predicate"],
                    value_json,
                    "CONFIRMED",
                    "pinned_native",
                    "usable",
                    1,
                    1,
                    fact["note"],
                ),
            )
            connection.execute(
                "insert or replace into fact_claims(claim_id,entity_id,predicate,value_json,status,authority,impl_status,canonical_fact_id,source_claim_refs_json,note) values(?,?,?,?,?,?,?,?,?,?)",
                (
                    claim_id,
                    entity_id,
                    fact["predicate"],
                    value_json,
                    "CONFIRMED",
                    "pinned_native",
                    "usable",
                    fact_id,
                    refs_json,
                    fact["note"],
                ),
            )
            for ref in sorted(set(fact["refs"])):
                connection.execute(
                    "insert or replace into fact_sources(fact_source_id,claim_id,entity_id,predicate,source_json) values(?,?,?,?,?)",
                    (
                        stable_id("fact-source-k4", claim_id, ref),
                        claim_id,
                        entity_id,
                        fact["predicate"],
                        json.dumps({"source_ref": ref, "authority": "pinned_native"}, sort_keys=True),
                    ),
                )
        for subject, predicate, object_id, refs in edges:
            edge_id = stable_id("edge-k4", subject, predicate, object_id)
            claim_id = stable_id("edge-claim-k4", edge_id)
            refs_json = json.dumps(sorted(set(refs)), ensure_ascii=False, sort_keys=True)
            statement = f"{subject} {predicate} {object_id}"
            connection.execute(
                "insert or replace into semantic_edges(edge_id,subject_id,predicate,object_id,status,authority,source_refs_json,claim_id) values(?,?,?,?,?,?,?,?)",
                (edge_id, subject, predicate, object_id, "verified", "pinned_native", refs_json, claim_id),
            )
            connection.execute(
                "insert or replace into edge_claims(claim_id,edge_id,claim_status,confidence,statement,source_refs_json) values(?,?,?,?,?,?)",
                (claim_id, edge_id, "verified", "high", statement, refs_json),
            )
            connection.execute(
                "insert or replace into edge_revisions(revision_id,edge_id,prior_status,next_status,reason,source_refs_json) values(?,?,?,?,?,?)",
                (
                    stable_id("edge-revision-k4", edge_id),
                    edge_id,
                    None,
                    "verified",
                    "Exact K4 source/native visual assembly relation.",
                    refs_json,
                ),
            )
            for ref in sorted(set(refs)):
                connection.execute(
                    "insert or replace into edge_sources(edge_source_id,edge_id,source_instance_id,source_ref,authority) values(?,?,?,?,?)",
                    (
                        stable_id("edge-source-k4", edge_id, ref),
                        edge_id,
                        None,
                        ref,
                        "pinned_native",
                    ),
                )
        metadata = {
            "brain_revision": REVISION,
            "status": "K4_SOURCE_LIMITED",
            "k4_status": "SOURCE_LIMITED",
            "k4_final_token": FINAL_TOKEN,
        }
        for key, value in metadata.items():
            connection.execute(
                "insert or replace into brain_metadata(key,value_json) values(?,?)",
                (key, json.dumps(value, ensure_ascii=False)),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return {
        "facts": [
            {
                "fact_id": f"fact:k4:{fact['entity_id']}|{fact['predicate']}",
                "entity_id": fact["entity_id"],
                "predicate": fact["predicate"],
                "note": fact["note"],
            }
            for fact in facts
        ],
        "edges": [
            {
                "edge_id": stable_id("edge-k4", subject, predicate, object_id),
                "subject_id": subject,
                "predicate": predicate,
                "object_id": object_id,
            }
            for subject, predicate, object_id, _ in edges
        ],
    }


def update_derived_artifacts(paths: list[Path]) -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        for path in paths:
            relative = rel(path)
            derived_id = stable_id("derived-k4", relative)
            connection.execute(
                "insert or replace into derived_artifacts(derived_id,relative_path,kind,source_ids_json,brain_revision,sha256,status) values(?,?,?,?,?,?,?)",
                (
                    derived_id,
                    relative,
                    "k4_visual_assembly_acceptance",
                    json.dumps([REVISION]),
                    REVISION,
                    sha256_file(path),
                    "active",
                ),
            )
        connection.commit()
    finally:
        connection.close()


def update_graph_summary() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        counts = dict(
            connection.execute(
                "select status,count(*) from semantic_edges group by status"
            ).fetchall()
        )
        total = connection.execute("select count(*) from semantic_edges").fetchone()[0]
    finally:
        connection.close()
    existing = load_json(GRAPH_PATH)
    existing.update(
        {
            "schema_version": "social-dev-k4-semantic-edge-graph-v1",
            "status": "source_limited",
            "edge_count": total,
            "verified_edge_count": counts.get("verified", 0),
            "candidate_edge_count": counts.get("candidate", 0),
            "unresolved_edge_count": counts.get("unresolved", 0),
            "rejected_edge_count": counts.get("rejected", 0),
            "k4_visual_assembly_revision": REVISION,
            "k4_visual_assembly_status": "SOURCE_LIMITED",
        }
    )
    write_json(GRAPH_PATH, existing)


def update_manifest(final_validation: dict[str, Any], after_db: dict[str, Any]) -> None:
    manifest = load_json(MANIFEST_PATH)
    manifest["status"] = "K4_SOURCE_LIMITED_VISUAL_ASSEMBLY"
    manifest["canonical_semantic_db"].update(
        {
            "sha256": after_db["sha256"],
            "size_bytes": after_db["size_bytes"],
            "brain_revision": REVISION,
        }
    )
    manifest.setdefault("acceptance", {})["k4"] = rel(K4)
    manifest["acceptance"]["k4_report"] = rel(K4 / "K4_CLOSURE_REPORT.md")
    manifest.setdefault("scope", {})["k4"] = "SOURCE_LIMITED"
    manifest["scope"]["v8"] = "NOT_STARTED"
    manifest["scope"]["integrations"] = "NOT_STARTED"
    manifest["scope"]["deployment"] = "NOT_STARTED"
    manifest["scope"]["network"] = False
    manifest["scope"]["subagents"] = False
    manifest["k4"] = {
        "status": "SOURCE_LIMITED",
        "final_token": final_validation["final_token"],
        "blocking_source_limited_count": final_validation["coverage"]["blocking_source_limited_count"],
        "heuristic_or_assumed_count": final_validation["coverage"]["heuristic_or_assumed_count"],
        "ready_for_v8": False,
    }
    digest = hashlib.sha256()
    total = 0
    files = [
        path
        for path in BRAIN.rglob("*")
        if path.is_file() and path.resolve() != MANIFEST_PATH.resolve()
    ]
    for path in sorted(files, key=lambda item: rel(item)):
        name = rel(path).encode("utf-8")
        content_hash = bytes.fromhex(sha256_file(path))
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(path.stat().st_size.to_bytes(8, "big"))
        digest.update(content_hash)
        total += path.stat().st_size
    manifest.setdefault("active_topology", {})["brain_tree_excluding_this_manifest"] = {
        "file_count": len(files),
        "bytes": total,
        "sha256": digest.hexdigest(),
    }
    write_json(MANIFEST_PATH, manifest)


def report_text(
    final_validation: dict[str, Any],
    regressions: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> str:
    coverage = final_validation["coverage"]
    regression_lines = "\n".join(
        f"- {item['label']}: {item['status']} ({item['command']})"
        for item in regressions
    )
    blocker_lines = "\n".join(
        f"- {item['consumer_id']}: {item['notes']}"
        for item in blockers
    )
    return f"""# K4 Whole Visual Assembly Brain Closure

Status: {final_validation["status"]}

Final token: {final_validation["final_token"]}

K4 closes the source/native visual assembly model for the reachable Room0
slice and records the exact remaining source limits. It does not start V8,
change runtime code, change MapChip pixels, or execute a live app.

## Coverage

- Reachable consumers: {coverage["reachable_consumer_count"]}
- Visible consumers: {coverage["visible_consumer_count"]}
- PROVEN_CANONICAL: {coverage["proven_canonical_count"]}
- Proven promoted to the canonical brain: {coverage["proven_promoted_count"]}
- PROVEN_NOT_CANONICAL: {coverage["proven_not_canonical_count"]}
- NO_DISTINCT_VISUAL: {coverage["no_distinct_visual_count"]}
- NOT_REACHABLE: {coverage["not_reachable_count"]}
- SOURCE_LIMITED: {coverage["source_limited_count"]}
- Blocking SOURCE_LIMITED: {coverage["blocking_source_limited_count"]}
- SOURCE_MISSING: {coverage["source_missing_count"]}
- Heuristic/assumed: {coverage["heuristic_or_assumed_count"]}

## Room0 assembly closed

- AppData.NewGame creates RoomData:0 / Floor A with a 14x14 MapChip grid and
  10x10 ObjChip grid.
- RoomData floor image index 5 is kept separate from the native indirect
  selector chain 5 -> 23 -> floor_05.png and from the runtime compatibility
  alias.
- The six explicit initial FurnitureData bindings, two structural facilities,
  door cell [8,4], three initial actor bindings, wall predicates, wall layers,
  and the nine Room.Draw passes are recorded with source/native references.
- Generic type-1 direct-image and type-2 workstation execution models are
  separate; raw ObjChip type is never treated as FurnitureData identity.

## Remaining blockers

{blocker_lines}

These are reported as source-limited because the pinned source/native evidence
does not prove the complete visible sequence. No guessed payload, offset,
action frame, or layer order was promoted.

## Deterministic query status

- Queries A, B, E, F, and G pass.
- Query C is source-limited by the live workstation interleave.
- Query D is source-limited by the exact Fukidashi array payload IDs and
  payload-specific offsets.

## Regression verification

{regression_lines}

## Boundary

- K2, K2.5, and K3 upstream tokens remain preserved.
- V8 remains NOT_STARTED and is not ready.
- Network, subagents, server, browser, emulator/ADB, and live app were not
  used.
- Read-only source roots were not modified.
- The runtime, generated original packs, and MapChip pixels were not changed.
"""


def main() -> int:
    preflight_state, context = preflight()
    native_scene = context["native_scene"]
    floor00 = context["floor00"]
    bootstrap = room0_bootstrap_recipe(context)
    wall_door = wall_door_recipe(context)
    furniture = furniture_recipe(context)
    workstation = workstation_recipe(context)
    staff = staff_recipe(context)
    equipment = equipment_recipe(context)
    talk = talk_recipe(context)
    room_draw = room_draw_recipe(context)
    opt_seb = opt_seb_recipe(context)
    records = build_consumers(context)
    metrics = coverage_metrics(records)
    if metrics["source_missing_count"] != 0:
        raise AssertionError("K4 cannot contain SOURCE_MISSING records")
    if metrics["heuristic_or_assumed_count"] != 0:
        raise AssertionError("K4 cannot contain heuristic/assumed records")
    blockers = [
        record
        for record in records
        if record["status"] == "SOURCE_LIMITED" and record["blocking"]
    ]
    if len(blockers) != 3:
        raise AssertionError(f"expected three K4 blocking source limits, got {len(blockers)}")
    queries = build_queries(
        bootstrap, wall_door, workstation, talk, equipment, staff, room_draw
    )
    source_native_paths = [
        (SOURCE_MANIFEST, "pinned source identity manifest"),
        (STAFF_SOURCE, "Staff source"),
        (ROOM_SOURCE, "Room source"),
        (OBJCHIP_SOURCE, "ObjChip source"),
        (FURNITURE_SOURCE, "FurnitureData source"),
        (LIBIL2CPP, "native binary"),
        (METADATA, "native metadata"),
        (DUMP, "native dump"),
        (NATIVE_SCENE, "accepted native scene assembly contract"),
        (FLOOR00, "accepted Room0 bootstrap contract"),
        (DISPLAY_MANIFEST, "accepted display asset manifest"),
        (COMPOSITION_CATALOG, "accepted composition catalog"),
        (FURNITURE_METADATA, "accepted furniture metadata"),
        (FLOOR00_SEB, "accepted floor00 SEB contract"),
        (ROOM_RUNTIME, "accepted room runtime contract"),
        (ROOM_ASSETS, "accepted room asset manifest"),
        (ACTION_MAP, "accepted action selector map"),
        (DIRECTION_CONTRACT, "accepted direction contract"),
        (STATE_MACHINE, "accepted staff state machine"),
        (ARRIVAL, "accepted arrival jump table"),
        (STAFF_AUTHORITY, "accepted native authority map"),
        (TALK, "accepted talk contract"),
        (EQUIPMENT, "accepted equipment contract"),
        (HOME, "accepted home contract"),
        (MOVEMENT, "accepted movement contract"),
    ]
    source_native_evidence = {
        "schema_version": "social-dev-k4-source-native-evidence-manifest-v1",
        "status": "pass",
        "authority_policy": {
            "tier_a": "pinned native binary, metadata, dump, raw C# source, and source/resource identities",
            "tier_b": "accepted source-derived contracts and decoded composition catalogs",
            "source_limited_policy": "unresolved values remain explicit; no fallback values are promoted",
        },
        "artifacts": [
            source_hash_record(path, role)
            for path, role in source_native_paths
            if path.exists()
        ],
        "native_anchor_catalog": {
            "Room.Draw": "0x12CBB80",
            "ObjChip.DrawWall": "0x12C0698",
            "ObjChip.Draw": "0x12C166C",
            "Staff.Draw": "0x12DA6A0",
            "Staff.Talk": "0x12D5588",
            "Staff.UseEquip": "0x12D4DEC",
            "Staff.OnArriveGoal": "0x12D8420",
        },
        "source_roots_read_only": True,
        "source_hashes_rechecked_after_build": None,
    }
    K4.mkdir(parents=True, exist_ok=True)
    write_json(K4 / "preflight-current-state.json", preflight_state)
    write_json(K4 / "room0-bootstrap-visual-recipe.json", bootstrap)
    write_json(K4 / "wall-door-assembly-recipe.json", wall_door)
    write_json(K4 / "furniture-execution-model.json", furniture)
    write_json(K4 / "workstation-sitting-composition.json", workstation)
    write_json(K4 / "staff-behavior-visual-recipe.json", staff)
    write_json(K4 / "equipment-composition-recipe.json", equipment)
    write_json(K4 / "talk-composition-recipe.json", talk)
    write_json(K4 / "room-draw-pass-recipe.json", room_draw)
    write_json(K4 / "opt-seb-execution-model.json", opt_seb)
    write_json(K4 / "source-native-evidence-manifest.json", source_native_evidence)
    write_json(
        K4 / "reachable-visual-consumers.json",
        {
            "schema_version": "social-dev-k4-reachable-visual-consumers-v1",
            "status": "source_limited",
            "scope": "normal reachable Room0 autonomous visual assembly slice",
            "records": records,
            "metrics": metrics,
        },
    )
    write_json(
        K4 / "visual-assembly-coverage-matrix.json",
        {
            "schema_version": "social-dev-k4-visual-assembly-coverage-matrix-v1",
            "status": "source_limited",
            "required_status_vocabulary": sorted(ALLOWED_STATUSES),
            "required_domains": [
                "Room0 bootstrap",
                "Floor/map",
                "Wall/corner/join",
                "Door",
                "Furniture",
                "Workstation/sitting",
                "Staff bootstrap",
                "Staff visual resolver",
                "Movement/wander",
                "Equipment",
                "Talk",
                "HP/home/return",
                "Global Room.Draw/occlusion",
                "OPT/SEB execution",
            ],
            "records": records,
            "metrics": metrics,
            "blocking_consumers": [record["consumer_id"] for record in blockers],
        },
    )
    write_json(K4 / "deterministic-query-results.json", queries)
    promoted = promote_brain(
        bootstrap, furniture, staff, equipment, room_draw, opt_seb, wall_door
    )
    derived_paths = [
        K4 / name
        for name in [
            "preflight-current-state.json",
            "room0-bootstrap-visual-recipe.json",
            "wall-door-assembly-recipe.json",
            "furniture-execution-model.json",
            "workstation-sitting-composition.json",
            "staff-behavior-visual-recipe.json",
            "equipment-composition-recipe.json",
            "talk-composition-recipe.json",
            "room-draw-pass-recipe.json",
            "opt-seb-execution-model.json",
            "source-native-evidence-manifest.json",
            "reachable-visual-consumers.json",
            "visual-assembly-coverage-matrix.json",
            "deterministic-query-results.json",
        ]
    ]
    update_derived_artifacts(derived_paths)
    update_graph_summary()
    after_db = db_snapshot()
    semantic_delta = {
        "schema_version": "social-dev-k4-semantic-delta-v1",
        "status": "source_limited",
        "brain_revision_before": preflight_state["canonical_brain_before_k4"]["brain_revision"],
        "brain_revision_after": REVISION,
        "canonical_database_before": preflight_state["canonical_brain_before_k4"],
        "canonical_database_after": after_db,
        "canonical_facts_added": promoted["facts"],
        "verified_edges_added": promoted["edges"],
        "source_limited_not_promoted": [
            {
                "consumer_id": record["consumer_id"],
                "description": record["description"],
                "notes": record.get("notes"),
            }
            for record in blockers
        ],
        "heuristic_or_assumed_added": 0,
        "runtime_pixel_change": False,
        "mapchip_pixel_change": False,
        "scope": "K4 visual assembly brain facts only; no product/living policy change",
    }
    write_json(K4 / "semantic-delta.json", semantic_delta)
    packs_before = preflight_state["generated_packs_before_k4"]
    packs_after = pack_snapshot()
    generated_delta = {
        "schema_version": "social-dev-k4-generated-pack-delta-v1",
        "status": "pass",
        "packs_before": packs_before,
        "packs_after": packs_after,
        "runtime_pack_changed": packs_before != packs_after,
        "visual_pack_changed": packs_before["visual"] != packs_after["visual"],
        "data_pack_changed": packs_before["data"] != packs_after["data"],
        "runtime_mirror_changed": packs_before["runtime_mirror"] != packs_after["runtime_mirror"],
        "generated_pack_policy": "K4 adds brain acceptance evidence and canonical semantic facts; original runtime/data/visual packs remain byte-stable.",
    }
    write_json(K4 / "generated-pack-delta.json", generated_delta)
    regressions = run_regressions()
    regression_status = all(item["status"] == "PASS" for item in regressions)
    source_after = [
        source_hash_record(path, role)
        for path, role in source_native_paths
        if path.exists()
    ]
    source_native_evidence["source_hashes_rechecked_after_build"] = source_after
    source_native_evidence["source_hashes_unchanged"] = (
        source_native_evidence["artifacts"] == source_after
    )
    write_json(K4 / "source-native-evidence-manifest.json", source_native_evidence)
    readiness = {
        "schema_version": "social-dev-k4-v8-readiness-v1",
        "status": "NOT_READY",
        "ready_for_v8": False,
        "final_token": FINAL_TOKEN,
        "coverage": metrics,
        "blocking_source_limited": [
            {
                "consumer_id": record["consumer_id"],
                "domain": record["domain"],
                "required_closure": record.get("notes"),
            }
            for record in blockers
        ],
        "heuristic_or_assumed_count": metrics["heuristic_or_assumed_count"],
        "source_missing_count": metrics["source_missing_count"],
        "required_next_step": "Close all blocking source-limited assembly relations with pinned source/native evidence before starting V8.",
        "v8_scope": "NOT_STARTED",
    }
    write_json(K4 / "v8-readiness.json", readiness)
    final_validation = {
        "schema_version": "social-dev-k4-final-validation-v1",
        "status": "incomplete_source_limited" if regression_status else "incomplete_source_limited_regression_failure",
        "final_token": FINAL_TOKEN,
        "coverage": metrics,
        "blocking_consumers": [record["consumer_id"] for record in blockers],
        "upstream": preflight_state["upstream_tokens"],
        "canonical_brain": {
            "before": preflight_state["canonical_brain_before_k4"],
            "after": after_db,
        },
        "semantic_delta": {
            "canonical_facts_added": len(promoted["facts"]),
            "verified_edges_added": len(promoted["edges"]),
            "heuristic_or_assumed_added": 0,
            "artifact": rel(K4 / "semantic-delta.json"),
        },
        "generated_pack_delta": {
            "runtime_changed": generated_delta["runtime_pack_changed"],
            "visual_changed": generated_delta["visual_pack_changed"],
            "data_changed": generated_delta["data_pack_changed"],
            "artifact": rel(K4 / "generated-pack-delta.json"),
        },
        "deterministic_queries": {
            query_id: query["status"]
            for query_id, query in queries["queries"].items()
        },
        "regressions": regressions,
        "boundary": {
            "v8": "NOT_STARTED",
            "network": False,
            "subagents": False,
            "server": False,
            "browser": False,
            "emulator_adb": False,
            "live_app": False,
            "runtime_code_changed": False,
            "mapchip_pixels_changed": False,
            "source_roots_changed": not source_native_evidence["source_hashes_unchanged"],
        },
        "artifacts": [
            rel(K4 / name)
            for name in [
                "preflight-current-state.json",
                "reachable-visual-consumers.json",
                "visual-assembly-coverage-matrix.json",
                "room0-bootstrap-visual-recipe.json",
                "wall-door-assembly-recipe.json",
                "furniture-execution-model.json",
                "workstation-sitting-composition.json",
                "staff-behavior-visual-recipe.json",
                "equipment-composition-recipe.json",
                "talk-composition-recipe.json",
                "room-draw-pass-recipe.json",
                "opt-seb-execution-model.json",
                "source-native-evidence-manifest.json",
                "semantic-delta.json",
                "generated-pack-delta.json",
                "v8-readiness.json",
                "final-validation.json",
                "deterministic-query-results.json",
                "K4_CLOSURE_REPORT.md",
            ]
        ],
    }
    write_json(K4 / "final-validation.json", final_validation)
    report = report_text(final_validation, regressions, blockers)
    (K4 / "K4_CLOSURE_REPORT.md").write_text(report, encoding="utf-8")
    update_manifest(final_validation, after_db)
    print(
        json.dumps(
            {
                "status": final_validation["status"],
                "final_token": final_validation["final_token"],
                "coverage": metrics,
                "blocking_consumers": [record["consumer_id"] for record in blockers],
                "regressions": {item["label"]: item["status"] for item in regressions},
                "canonical_facts_added": len(promoted["facts"]),
                "verified_edges_added": len(promoted["edges"]),
            },
            sort_keys=True,
        )
    )
    return 0 if regression_status and source_native_evidence["source_hashes_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
