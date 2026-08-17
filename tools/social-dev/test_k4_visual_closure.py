"""Validate the deterministic K4 visual assembly brain-closure artifacts."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
K4 = ROOT / "knowledge/brain/acceptance/k4"
DB = ROOT / "knowledge/brain/sqlite/social_dev_brain.sqlite"
MANIFEST = ROOT / "knowledge/brain/MANIFEST.json"
FINAL_TOKEN = "PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8"
REVISION = "k4-visual-assembly-r2"
ALLOWED_STATUSES = {
    "PROVEN_CANONICAL",
    "PROVEN_NOT_CANONICAL",
    "SOURCE_MISSING",
    "SOURCE_LIMITED",
    "NO_DISTINCT_VISUAL",
    "NOT_REACHABLE",
}
REQUIRED_FILES = [
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
    "K4_CLOSURE_REPORT.md",
]


def load(name: str):
    return json.loads((K4 / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def metrics(records: list[dict]) -> dict[str, int]:
    counts = Counter(record["status"] for record in records)
    return {
        "reachable_consumer_count": sum(
            record["status"] != "NOT_REACHABLE" for record in records
        ),
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


def validate_files(errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        if not (K4 / name).exists():
            fail(errors, f"missing required K4 artifact: {name}")


def validate_coverage(errors: list[str]) -> None:
    consumers = load("reachable-visual-consumers.json")
    matrix = load("visual-assembly-coverage-matrix.json")
    records = consumers["records"]
    matrix_records = matrix["records"]
    if [r["consumer_id"] for r in records] != [
        r["consumer_id"] for r in matrix_records
    ]:
        fail(errors, "coverage matrix records do not match reachable consumer records")
    if len({r["consumer_id"] for r in records}) != len(records):
        fail(errors, "coverage consumer IDs are not unique")
    for record in records:
        if record["status"] not in ALLOWED_STATUSES:
            fail(errors, f"invalid status for {record['consumer_id']}")
        if record["heuristic_or_assumed"] is not False:
            fail(errors, f"heuristic/assumed record: {record['consumer_id']}")
        if not record["evidence"]:
            fail(errors, f"missing evidence for {record['consumer_id']}")
    computed = metrics(records)
    if consumers["metrics"] != computed:
        fail(errors, "reachable consumer metrics are not deterministic")
    if matrix["metrics"] != computed:
        fail(errors, "coverage matrix metrics are not deterministic")
    if computed["source_missing_count"] != 0:
        fail(errors, "K4 contains SOURCE_MISSING coverage records")
    if computed["heuristic_or_assumed_count"] != 0:
        fail(errors, "K4 contains heuristic/assumed coverage records")
    expected_blockers = set()
    actual_blockers = {
        r["consumer_id"]
        for r in records
        if r["status"] == "SOURCE_LIMITED" and r["blocking"]
    }
    if actual_blockers != expected_blockers:
        fail(errors, f"unexpected K4 blockers: {sorted(actual_blockers)}")
    if consumers["status"] != "closed" or matrix["status"] != "closed":
        fail(errors, "K4 coverage is not marked closed")
    required_domains = {
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
    }
    if not required_domains.issubset(set(matrix["required_domains"])):
        fail(errors, "coverage matrix is missing a mandatory K4 domain")


def validate_room0(errors: list[str]) -> None:
    bootstrap = load("room0-bootstrap-visual-recipe.json")
    room = bootstrap["room"]
    topology = room["map_topology"]
    if room["room_key"] != "room:0" or room["room_data_key"] != "data:room:0":
        fail(errors, "Room0 recipe identity is wrong")
    if topology["map_chip_width"] != 14 or topology["map_chip_height"] != 14:
        fail(errors, "Room0 MapChip topology is not 14x14")
    if topology["obj_chip_width"] != 10 or topology["obj_chip_height"] != 10:
        fail(errors, "Room0 ObjChip topology is not 10x10")
    chain = room["floor_selector_chain"]
    if (
        chain["raw_roomdata_floor_image_index"] != 5
        or chain["native_image_selector"] != 23
        or chain["asset"] != "floor_05.png"
    ):
        fail(errors, "Room0 floor selector chain is not 5 -> 23 -> floor_05.png")
    if chain["runtime_alias_is_separate"] is not True:
        fail(errors, "Room0 runtime floor alias was collapsed into native identity")
    if len(bootstrap["initial_furniture"]) != 6:
        fail(errors, "Room0 initial furniture instance count is not six")
    expected_cells = {
        (3, (2, 4)),
        (3, (3, 4)),
        (3, (6, 4)),
        (12, (8, 5)),
        (26, (8, 6)),
        (56, (2, 7)),
    }
    actual_cells = {
        (item["furniture_data_id"], tuple(item["cell"]))
        for item in bootstrap["initial_furniture"]
    }
    if actual_cells != expected_cells:
        fail(errors, f"Room0 initial furniture cells differ: {actual_cells}")
    if bootstrap["door"]["cell"] != [8, 4]:
        fail(errors, "Room0 door cell is not [8,4]")
    if len(bootstrap["actors"]) != 3:
        fail(errors, "Room0 initial actor count is not three")

    wall_door = load("wall-door-assembly-recipe.json")
    if wall_door["wall"]["logical_application_count"] != 15:
        fail(errors, "Room0 wall logical application count is not 15")
    if wall_door["wall"]["layer_application_count"] != 30:
        fail(errors, "Room0 wall layer application count is not 30")
    if wall_door["door_closed_baseline"]["cell"] != [8, 4]:
        fail(errors, "Room0 door baseline cell is wrong")
    if wall_door["door_action"]["status"] != "NO_DISTINCT_VISUAL":
        fail(errors, "door action-vs-visual conclusion is not canonical")
    if wall_door["door_action"]["blocking"]:
        fail(errors, "door action-vs-visual conclusion remains blocking")


def validate_recipes(errors: list[str]) -> None:
    furniture = load("furniture-execution-model.json")
    ids = {
        item["furniture_data_id"] for item in furniture["native_room0_instances"]
    }
    if ids != {3, 12, 26, 56}:
        fail(errors, "furniture execution model does not cover all Room0 bindings")
    if furniture["generic_native_model"]["type_policy"]["raw_type_without_explicit_binding"] != "never infer FurnitureData identity":
        fail(errors, "raw ObjChip identity policy is not explicit")

    workstation = load("workstation-sitting-composition.json")
    if workstation["status"] != "PROVEN_CANONICAL" or workstation["blocking"]:
        fail(errors, "workstation interleave is not canonical")
    if workstation["desk_cells"] != [[2, 4], [3, 4], [6, 4]]:
        fail(errors, "workstation desk cells are wrong")

    talk = load("talk-composition-recipe.json")
    if talk["status"] != "PROVEN_CANONICAL" or talk["fukidashi"]["blocking"]:
        fail(errors, "talk Fukidashi payload is not canonical")
    if talk["fukidashi"]["known"]["invocation_frames"] != [20, 70]:
        fail(errors, "talk Fukidashi frame gates are wrong")
    if len(talk["fukidashi"]["known"]["native_static_field_handles"]) != 5:
        fail(errors, "talk field-handle evidence is not the exact autonomous pool set")

    equipment = load("equipment-composition-recipe.json")
    gates = equipment["native_execution"]["frame_gates"]
    if [item["frame"] for item in gates] != [20, 40, 60, 70]:
        fail(errors, "equipment frame gates are not 20/40/60/70")

    draw = load("room-draw-pass-recipe.json")
    expected_passes = [
        "map-extension-floor",
        "map-chip",
        "object-chip-primary",
        "object-chip-wall",
        "avatar-primary",
        "avatar-secondary",
        "object-chip-late-preview",
        "object-chip-late",
        "map-floor",
    ]
    if [item["pass_id"] for item in draw["passes"]] != expected_passes:
        fail(errors, "Room.Draw pass graph is not the exact nine-pass sequence")
    if not draw["occlusion"]["avatar_primary_between_object_primary_and_object_late"]:
        fail(errors, "Room.Draw avatar/late-object occlusion seam is missing")

    opt = load("opt-seb-execution-model.json")
    if opt["logical_execution"]["composition_count"]["composition_entries"] != 47:
        fail(errors, "OPT/SEB composition count is not 47")
    if opt["native_call_boundary"]["pixel_backend"]["blocking"]:
        fail(errors, "V7 pixel backend was incorrectly made a K4 blocker")


def validate_queries(errors: list[str]) -> None:
    queries = load("deterministic-query-results.json")["queries"]
    expected = {
        "A_room0_complete_bootstrap": "pass",
        "B_one_wall_cell": "pass",
        "C_workstation_sitting": "pass",
        "D_talk": "pass",
        "E_equipment": "pass",
        "F_staff_state_visual_matrix": "pass",
        "G_global_room_draw_pass": "pass",
    }
    if {key: value["status"] for key, value in queries.items()} != expected:
        fail(errors, "deterministic K4 query statuses differ from the closure result")


def validate_brain_and_boundaries(errors: list[str]) -> None:
    final = load("final-validation.json")
    if final["final_token"] != FINAL_TOKEN:
        fail(errors, "K4.1 final token is missing")
    if final["coverage"]["blocking_source_limited_count"] != 0:
        fail(errors, "K4 blocking source-limited count is not zero")
    if final["coverage"]["heuristic_or_assumed_count"] != 0:
        fail(errors, "K4 heuristic/assumed count is not zero")
    if final["coverage"]["source_missing_count"] != 0:
        fail(errors, "K4 source-missing count is not zero")
    if final["boundary"]["v8"] != "NOT_STARTED" or final["status"] != "complete":
        fail(errors, "K4 final boundary/status is wrong")
    if any(item["status"] != "PASS" for item in final["regressions"]):
        fail(errors, "a K4 regression command did not pass")

    readiness = load("v8-readiness.json")
    if readiness["ready_for_v8"] is not True or readiness["status"] != "READY":
        fail(errors, "V8 readiness does not report ready")
    if readiness["blocking_source_limited"] != []:
        fail(errors, "V8 readiness still has blocking source-limited records")

    delta = load("semantic-delta.json")
    if len(delta["canonical_facts_added"]) < 10 or len(delta["verified_edges_added"]) < 9:
        fail(errors, "K4.1 semantic delta does not contain the promoted exact facts/edges")
    if delta["heuristic_or_assumed_added"] != 0:
        fail(errors, "K4 semantic delta contains heuristic additions")

    pack_delta = load("generated-pack-delta.json")
    if any(
        pack_delta[key]
        for key in (
            "runtime_pack_changed",
            "visual_pack_changed",
            "data_pack_changed",
            "runtime_mirror_changed",
        )
    ):
        fail(errors, "K4 changed an original generated pack")

    source_evidence = load("source-native-evidence-manifest.json")
    if source_evidence["source_roots_read_only"] is not True:
        fail(errors, "source roots are not recorded read-only")
    if source_evidence["source_hashes_unchanged"] is not True:
        fail(errors, "source hashes changed during K4")

    connection = sqlite3.connect(DB)
    try:
        metadata = dict(connection.execute("select key,value_json from brain_metadata"))
        if json.loads(metadata["brain_revision"]) != REVISION:
            fail(errors, "canonical brain revision is not K4")
        if json.loads(metadata["status"]) != "K4_CLOSED_VISUAL_ASSEMBLY":
            fail(errors, "canonical brain status is not K4 closed")
        fact_count = connection.execute(
            "select count(*) from canonical_facts where fact_id like 'fact:k4:%'"
        ).fetchone()[0]
        edge_count = connection.execute(
            "select count(*) from semantic_edges where edge_id like 'edge-k4:%' or edge_id like 'edge-k4-1:%'"
        ).fetchone()[0]
        if fact_count < 10 or edge_count < 9:
            fail(errors, "canonical brain K4 fact/edge counts are wrong")
    finally:
        connection.close()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["scope"]["v8"] != "NOT_STARTED":
        fail(errors, "MANIFEST v8 scope was changed")
    if manifest["scope"]["k4"] != "CLOSED":
        fail(errors, "MANIFEST K4 scope is not CLOSED")
    if manifest["status"] != "K4_CLOSED_VISUAL_ASSEMBLY":
        fail(errors, "MANIFEST status is not K4 closed")
    after = final["canonical_brain"]["after"]
    if after["sha256"] != sha256(DB):
        fail(errors, "final validation canonical brain hash is stale")
    if manifest["canonical_semantic_db"]["sha256"] != sha256(DB):
        fail(errors, "MANIFEST canonical brain hash is stale")

    preflight = load("preflight-current-state.json")
    expected_tokens = {
        "k2": "PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED",
        "k2_5": "PASS_K2_5_CANONICAL_KNOWLEDGE_PROMOTION_AND_LEGACY_DISTILLATION_CLOSED",
        "k3": "PASS_K3_TARGETED_MISSING_LINK_CLOSURE_CLOSED",
    }
    if preflight["upstream_tokens"] != expected_tokens:
        fail(errors, "upstream K2/K2.5/K3 tokens are not preserved")
    if any(preflight["boundary"].get(key) for key in ("network_used", "subagents_used", "server_started", "emulator_or_adb_used", "live_app_used", "mapchip_pixels_changed")):
        fail(errors, "K4 preflight boundary records an out-of-scope action")


def validate_report_and_layout(errors: list[str]) -> None:
    report = (K4 / "K4_CLOSURE_REPORT.md").read_text(encoding="utf-8")
    for marker in (
        FINAL_TOKEN,
        "room0.door.action-timeline",
        "staff.talk.fukidashi-payload",
        "workstation.live-interleave",
        "No blocking source-limited relations remain",
        "V8 remains NOT_STARTED",
    ):
        if marker not in report:
            fail(errors, f"closure report is missing marker: {marker}")
    final = load("final-validation.json")
    for path in final["artifacts"]:
        if not path.startswith(("knowledge/brain/acceptance/k4/", "knowledge/brain/acceptance/k4-1/")):
            fail(errors, f"K4 artifact escapes the acceptance directory: {path}")


def main() -> int:
    errors: list[str] = []
    validate_files(errors)
    if not errors:
        validate_coverage(errors)
        validate_room0(errors)
        validate_recipes(errors)
        validate_queries(errors)
        validate_brain_and_boundaries(errors)
        validate_report_and_layout(errors)
    if errors:
        print("FAIL_K4_ARTIFACT_VALIDATION")
        for error in errors:
            print(f"- {error}")
        return 1
    final = load("final-validation.json")
    coverage = final["coverage"]
    print(
        "PASS_K4_ARTIFACT_VALIDATION_SOURCE_LIMITED "
        f"reachable={coverage['reachable_consumer_count']} "
        f"visible={coverage['visible_consumer_count']} "
        f"blocking_source_limited={coverage['blocking_source_limited_count']} "
        f"heuristic_or_assumed={coverage['heuristic_or_assumed_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
