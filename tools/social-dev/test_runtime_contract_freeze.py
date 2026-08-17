"""Independent acceptance checks for the R0 runtime-contract freeze package."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge/fixtures/accepted/runtime-contract-freeze"
I0_EVIDENCE = ROOT / "knowledge/fixtures/accepted/i0-living-runtime"
REPORTS = ROOT / "docs/Phases/Runtime"
I2_EVIDENCE = ROOT / "knowledge/fixtures/accepted/i2-dashboard-runtime"

CONTRACT_FILES = [
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
SUPPORTING_FILES = [
    "runtime-contract-validation.json",
    "checkpoint-ledger.json",
    "runtime-contract-manifest.json",
]
REPORT_FILES = [
    "R0_EXISTING_RUNTIME_DELTA_AUDIT.md",
    "R0_ACTOR_ROOM_FURNITURE_CONTRACT.md",
    "R0_MOVEMENT_STATE_TICK_RNG_CONTRACT.md",
    "R0_HP_WORK_INTERRUPTION_CONTRACT.md",
    "R0_VISUAL_PRODUCT_SAVE_BOUNDARY.md",
    "R0_SCENARIO_FIXTURES.md",
    "R0_RUNTIME_CONTRACT_FREEZE.md",
]
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
FINAL_STATUS = "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION"
K2_5_CANONICAL_PATH_REWRITE_PATHS = {
    "runtime/social-dev/src/catalog/load-contracts.ts",
    "runtime/social-dev/src/scene/room-resolver.ts",
}


def i0_implementation_active() -> bool:
    manifest = I0_EVIDENCE / "implementation-manifest.json"
    if not manifest.is_file():
        return False
    try:
        return str(load_json_file(manifest).get("status", "")).startswith("PASS_I0_")
    except (OSError, json.JSONDecodeError):
        return False


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load(name: str) -> dict[str, Any]:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def i2_sanctioned_runtime_paths() -> dict[str, dict[str, Any]]:
    """Allow only the explicit I2 app-shell migration while keeping R0 files immutable."""
    lock_path = I2_EVIDENCE / "upstream-hash-lock.json"
    if not lock_path.is_file():
        return {}
    try:
        lock = load_json_file(lock_path)
    except (OSError, json.JSONDecodeError):
        return {}
    if not str(lock.get("status", "")).startswith("PASS_I2_"):
        return {}
    migrations = lock.get("sanctioned_migrations", {})
    return migrations if isinstance(migrations, dict) else {}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def names(rows: list[dict[str, Any]]) -> set[str]:
    return {row["name"] for row in rows}


def main() -> int:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(f"check {checks} failed: {message}")

    check(OUT.is_dir(), "R0 evidence directory exists")
    check(REPORTS.is_dir(), "runtime reports directory exists")
    required_json = set(CONTRACT_FILES + SUPPORTING_FILES)
    check({path.name for path in OUT.glob("*.json")} == required_json, "exact R0 JSON artifact set")
    check({path.name for path in REPORTS.glob("R0_*.md")} == set(REPORT_FILES), "exact R0 report set")
    for name in CONTRACT_FILES + SUPPORTING_FILES:
        payload = load(name)
        check(isinstance(payload, dict), f"JSON object: {name}")
    for name in REPORT_FILES:
        check((REPORTS / name).read_text(encoding="utf-8").strip() != "", f"non-empty report: {name}")

    payloads = {name: load(name) for name in CONTRACT_FILES + SUPPORTING_FILES}
    for name in CONTRACT_FILES:
        check(payloads[name]["status"] == "FROZEN_FOR_IMPLEMENTATION", f"frozen contract status: {name}")
    check(payloads["runtime-contract-manifest.json"]["status"] == FINAL_STATUS, "manifest status")
    check(payloads["runtime-contract-validation.json"]["status"] == FINAL_STATUS, "validation status")
    check(payloads["checkpoint-ledger.json"]["status"] == FINAL_STATUS, "ledger status")

    identity = payloads["runtime-contract-manifest.json"]["source_identity"]
    identity_paths = {
        "apk": ROOT / identity["apk_path"],
        "libil2cpp": ROOT / identity["native_path"],
        "global_metadata": ROOT / identity["metadata_path"],
        "dump": ROOT / identity["dump_path"],
    }
    for key, path in identity_paths.items():
        check(path.is_file(), f"pinned source exists: {key}")
        observed = sha256(path)
        check(observed == EXPECTED_HASHES[key], f"pinned source hash: {key}")
        check(identity["observed_hashes"][key] == observed, f"manifest observed hash: {key}")
        check(identity["expected_hashes"][key] == EXPECTED_HASHES[key], f"manifest expected hash: {key}")
    check(identity["status"] == "PASS_SOURCE_IDENTITY", "source identity status")

    manifest = payloads["runtime-contract-manifest.json"]
    check(set(manifest["contract_files"]) == set(CONTRACT_FILES), "manifest contract coverage")
    check(set(manifest["reports"]) == set(REPORT_FILES), "manifest report coverage")
    for name in CONTRACT_FILES:
        descriptor = manifest["contract_files"][name]
        path = ROOT / descriptor["path"]
        check(path == OUT / name, f"manifest contract path: {name}")
        check(sha256(path) == descriptor["sha256"], f"manifest contract hash: {name}")
    for name in REPORT_FILES:
        descriptor = manifest["reports"][name]
        path = ROOT / descriptor["path"]
        check(path == REPORTS / name, f"manifest report path: {name}")
        check(sha256(path) == descriptor["sha256"], f"manifest report hash: {name}")
    ledger_path = ROOT / manifest["supporting_artifacts"]["checkpoint_ledger"]["path"]
    check(sha256(ledger_path) == manifest["supporting_artifacts"]["checkpoint_ledger"]["sha256"], "ledger hash")
    check(manifest["supporting_artifacts"]["validation"]["sha256"] is None, "validation circular hash excluded")
    validation = payloads["runtime-contract-validation.json"]
    check(validation["manifest_sha256"] == sha256(OUT / "runtime-contract-manifest.json"), "final manifest hash in validation")

    def walk_provenance(value: Any) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        if isinstance(value, dict):
            if "provenance" in value:
                found.append(value["provenance"])
            for child in value.values():
                found.extend(walk_provenance(child))
        elif isinstance(value, list):
            for child in value:
                found.extend(walk_provenance(child))
        return found

    provenance_rows = []
    for name, payload in payloads.items():
        for row in walk_provenance(payload):
            provenance_rows.append((name, row))
            check(row.get("authority_type") in ALLOWED_AUTHORITY, f"allowed provenance authority in {name}")
            check(isinstance(row.get("source_evidence_path"), str) and row["source_evidence_path"], f"provenance path in {name}")
            check(isinstance(row.get("status"), str) and row["status"], f"provenance status in {name}")
    check(len(provenance_rows) >= 100, "provenance coverage is substantial")

    delta = payloads["runtime-delta-matrix.json"]
    expected_dispositions = {
        "KEEP": 2,
        "KEEP_VISUAL_ONLY": 112,
        "EXTEND": 3,
        "REPLACE": 3,
        "SUPERSEDED": 3,
        "PRODUCT_LAYER_ONLY": 0,
        "OUT_OF_SCOPE": 11,
        "UNKNOWN_REVIEW_REQUIRED": 0,
    }
    check(delta["summary"]["by_disposition"] == expected_dispositions, "delta disposition counts")
    check(delta["summary"]["total_entries"] == 134, "delta entry count")
    check(delta["summary"]["implementation_blockers"] == 0, "delta blockers")
    check(delta["summary"]["unknown_review_required_living_runtime"] == 0, "no living unknown review entries")
    i0_active = i0_implementation_active()
    i2_sanctioned_paths = i2_sanctioned_runtime_paths()
    # The I0 preflight adapter is a generated projection of the R0 lock.  It
    # necessarily changes whenever the frozen R0 manifest is regenerated, so
    # its own wildcard-audit digest cannot be checked without a hash cycle.
    # Validate the projection's referenced contract digests instead.
    generated_i0_projection = "knowledge/fixtures/accepted/runtime/i0-r0-runtime-adapter.json"
    i0_projection = json.loads((ROOT / generated_i0_projection).read_text(encoding="utf-8"))
    for contract in i0_projection.get("contracts", {}).values():
        contract_path = ROOT / contract["source"]
        check(contract_path.is_file(), f"I0 projection source exists: {contract['source']}")
        check(sha256(contract_path) == contract["sha256"], f"I0 projection source hash: {contract['source']}")
    generated_i0_catalog = "knowledge/fixtures/accepted/runtime/i0-runtime-catalog.json"
    i0_catalog = json.loads((ROOT / generated_i0_catalog).read_text(encoding="utf-8"))
    i0_catalog_manifest = json.loads(
        (I0_EVIDENCE / "canonical-runtime-catalog-manifest.json").read_text(encoding="utf-8")
    )
    check(i0_catalog_manifest.get("catalog_path") == generated_i0_catalog, "I0 catalog path")
    check(i0_catalog.get("counts") == i0_catalog_manifest.get("counts"), "I0 catalog counts")
    check(i0_catalog.get("source_hashes") == i0_catalog_manifest.get("source_hashes"), "I0 catalog source hashes")
    check(i0_catalog_manifest.get("fabricated_rows") == 0, "I0 catalog fabricated rows")
    for row in delta["entries"]:
        path = ROOT / row["path"]
        check(path.is_file(), f"audited path exists: {row['path']}")
        # R0 records the pre-I0 source snapshot. Once the I0 implementation
        # manifest is PASS, the R0 contract files remain immutable while the
        # explicitly superseded core owner is allowed to migrate.
        sanctioned = i2_sanctioned_paths.get(row["path"])
        if sanctioned:
            check(sha256(path) == sanctioned.get("current_i2_sha256"), f"I2 sanctioned path hash: {row['path']}")
        elif row["path"] == generated_i0_projection:
            check(i0_projection.get("status") == "PASS_R0_CONTRACTS_ADAPTED_READ_ONLY", "I0 projection status")
        elif row["path"] == generated_i0_catalog:
            check(i0_catalog.get("status") == "pass", "I0 catalog status")
        elif not i0_active or not row["path"].startswith("runtime/social-dev/src/core/"):
            check(sha256(path) == row["file_sha256"], f"audited path hash: {row['path']}")
    if not i0_active:
        check(delta["runtime_source_hash_guard"]["git_diff_status"] == {
            "runtime/social-dev/src/catalog": "clean",
            "runtime/social-dev/src/core": "clean",
            "runtime/social-dev/src/renderer": "clean",
            "runtime/social-dev/src/scene": "clean",
        }, "runtime source hash guard status")
    for source_root in ["runtime/social-dev/src/core", "runtime/social-dev/src/catalog", "runtime/social-dev/src/scene", "runtime/social-dev/src/renderer"]:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", source_root],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if i0_active and source_root == "runtime/social-dev/src/core":
            continue
        # K2.10 is an import-only repackaging cutover.  The exact files are
        # hash-locked in the I2 sanctioned migration map; permit those files
        # in their owning catalog/scene roots while keeping every other dirty
        # path and the renderer root subject to the original R0 cleanliness
        # gate.
        if source_root in {"runtime/social-dev/src/catalog", "runtime/social-dev/src/scene"} and i2_sanctioned_paths:
            changed_paths = []
            for line in result.stdout.splitlines():
                changed = line[3:].strip() if len(line) >= 3 else ""
                changed_paths.append(changed.replace("\\", "/"))
            allowed_paths = set(i2_sanctioned_paths)
            if changed_paths and all(path in allowed_paths for path in changed_paths):
                continue
        # K2.5 canonicalizes the two import-only consumers that used the
        # retired runtime/evidence namespace.  Keep this exception explicit;
        # every other catalog/scene change remains subject to the original
        # R0 cleanliness gate.
        if source_root in {"runtime/social-dev/src/catalog", "runtime/social-dev/src/scene"}:
            changed_paths = []
            for line in result.stdout.splitlines():
                changed = line[3:].strip() if len(line) >= 3 else ""
                changed_paths.append(changed.replace("\\", "/"))
            if changed_paths and all(path in K2_5_CANONICAL_PATH_REWRITE_PATHS for path in changed_paths):
                continue
        check(result.returncode == 0 and result.stdout.strip() == "", f"no runtime source changes: {source_root}")

    actor = payloads["actor-runtime-contract.json"]
    actor_original = actor["original_static_identity"] + actor["original_mutable_runtime_state"]
    original_names = names(actor_original)
    product_names = names(actor["product_only_state"])
    check(original_names.isdisjoint(product_names), "product-only actor fields are separate")
    check({"externalAgentId", "externalTaskId", "backendTaskState", "dashboardDisplayState"} == product_names, "product actor field set")
    check({field["name"] for field in actor["original_mutable_runtime_state"]} >= {"hp", "state", "moveMode", "flags", "roomRef", "floor", "deskId", "recoveryStock"}, "actor mutable state coverage")
    actor_offsets = {field["name"]: field.get("native_offset") for field in actor_original}
    check(actor_offsets["hp"] == "0xE8" and actor_offsets["state"] == "0x70" and actor_offsets["moveMode"] == "0xA8", "actor native offsets")
    check(actor_offsets["deskId"] == "0xB8" and actor_offsets["roomRef"] == "0x90", "actor room/desk offsets")
    check("taskAssignment" not in original_names and "externalTaskId" not in original_names, "no dashboard task state in original actor")

    room = payloads["room-runtime-contract.json"]
    topology = {row["name"]: row["value"] for row in room["topology"]}
    check(topology["mapChipMainDisplay"] == {"width": 14, "height": 14, "cellCount": 196, "variant": "floor_0"}, "main MapChip topology")
    check(topology["objChipOccupancy"]["width"] == 10 and topology["objChipOccupancy"]["height"] == 10 and topology["objChipOccupancy"]["cellCount"] == 100, "ObjChip topology")
    check("coordinateSeparation" in topology and "MapChip 14x14" in topology["coordinateSeparation"], "MapChip/ObjChip separation")
    check(any(row["name"] == "rawChipTraversal" for row in room["membership_and_order"]), "raw ObjChip order preserved")

    furniture = payloads["furniture-instance-contract.json"]
    furniture_fields = {field["name"]: field for field in furniture["fields"]}
    check(furniture_fields["ownerStaffId"]["native_offset"] == "0x78", "owner offset")
    check(furniture_fields["activeUserIds"]["native_offset"] == "0x68", "active users offset")
    check(furniture_fields["reservedUserIds"]["native_offset"] == "0x70", "reserved users offset")
    check(furniture_fields["useCount"]["native_offset"] == "0x8C", "use count offset")
    check(len({furniture_fields[name]["native_offset"] for name in ["ownerStaffId", "activeUserIds", "reservedUserIds"]}) == 3, "owner/active/reserved are distinct")
    role_counts = {row["name"]: row["value"] for row in furniture["role_counts"]}
    check(role_counts == {"WORKSTATION": 10, "RECOVERY_EQUIPMENT": 49, "EQUIPMENT_NO_HP_EFFECT_PROVEN": 43, "DOOR": 1}, "FurnitureData role counts")
    check("REST" not in role_counts and "SOCIAL" not in role_counts, "no inferred REST/SOCIAL furniture roles")

    movement = payloads["movement-route-contract.json"]
    neighbors = next(row["value"] for row in movement["pathfinding"] if row["name"] == "neighborPolicy")
    check(neighbors["connectivity"] == 4 and neighbors["diagonal"] is False and set(map(tuple, neighbors["neighbors"])) == {(-1, 0), (1, 0), (0, -1), (0, 1)}, "cardinal four-neighbor movement")
    arrivals = {row["value"]["moveMode"]: row["value"]["label"] for row in movement["arrival_dispatch"]}
    check(set(arrivals) == set(range(1, 12)), "all eleven arrival modes")
    check(arrivals[10] == "GO_TO_DOOR" and arrivals[11] == "GO_HOME", "door/home arrival modes")
    state_machine = payloads["staff-state-machine-contract.json"]
    check({row["state_id"] for row in state_machine["states"]} == set(range(14)), "fourteen Staff states")
    check({row["value"] for row in state_machine["move_modes"]} == set(range(12)), "twelve move modes")
    check(state_machine["invariants"][0]["value"] == 14, "state count invariant")

    tick = payloads["tick-order-contract-v2.json"]
    check([row["name"] for row in tick["staff_update_order"]] == ["staffEntry", "recoveryFirst", "lowHpGuard", "stateDispatch", "stateHandler", "routeArrival", "handlerTimers", "cleanup", "projection"], "canonical Staff tick order")
    check([row["name"] for row in tick["player_room_order"]] == ["playerFrame", "planningChain", "roomStaffThenObj", "visualAfterCommit"], "Player/Room tick order")
    check(tick["legacy_contract_audit"]["disposition"] == "REPLACE", "legacy tick contract superseded")

    rng = payloads["rng-autonomy-contract.json"]
    random_n = next(row for row in rng["decisions"] if row["managed_method"] == "AppData.Random(int n)")
    random_min_max = next(row for row in rng["decisions"] if row["managed_method"] == "AppData.Random(int min, int max)")
    check(random_n["range_semantics"] == "[0,n) when n > 0", "exclusive native RNG range")
    check(random_min_max["range_semantics"] == "[min,max] inclusive", "inclusive native RNG range")
    check(any(row["managed_method"] == "Staff.GotoEquip" and row["comparison_or_threshold"].startswith("0 -> type 1") for row in rng["decisions"]), "equipment RNG branch")
    check({row["name"] for row in rng["old_deterministic_fixtures_to_replace"]} >= {"fixedRouteTrace", "scriptedTalkTiming"}, "fixed legacy traces marked for replacement")

    hp = payloads["hp-recovery-home-runtime-contract.json"]
    hp_invariants = {row["name"]: row["value"] for row in hp["invariants"]}
    check(hp_invariants["thresholds"] == {"low": 5, "return": 40}, "HP thresholds")
    recovery = {row["name"]: row["value"] for row in hp["recovery_stock"]}
    check(recovery["startDelay"] == 20 and recovery["stockUnit"] == 1, "recovery delay and stock unit")
    check("frame_%3 == 0" in recovery["cadence"] and "RecoverHp(1)" in recovery["cadence"], "recovery cadence")
    check(recovery["exhaustion"]["frameToHideHpGauge_"] == 40, "recovery gauge timer")
    check(hp["ordinary_work"]["value"].startswith("FALSE:"), "ordinary work has no HP drain")
    check(any("<= 5" in row["value"] for row in hp["home"]), "low HP home guard")
    check(any(">= 40" in row["value"] for row in hp["home"]), "home return threshold")

    work = payloads["work-planning-runtime-contract.json"]
    chains = {row["name"]: row["value"] for row in work["original_command_chain"]}
    check(chains["startChain"] == ["Player.StartPlanning", "Room.OnStartPlanning", "Staff.OnStartPlanning"], "planning start chain")
    check(chains["updateChain"] == ["Player.UpdatePlanning", "Room.UpdatePlanning", "Staff.UpdatePlanning2"], "planning update chain")
    check(chains["endChain"] == ["Player.IsCompletedPlanning", "Room.OnEndPlanning", "Staff.OnEndPlanning"], "planning end chain")
    check(work["product_policy"]["value"].startswith("PRODUCT_POLICY_PENDING"), "planning product boundary")
    interruptions = {row["id"] for row in payloads["interruption-resume-contract.json"]["paths"]}
    check(interruptions == {"work-to-equipment", "work-to-talk", "low-hp-home", "desk-destroyed"}, "interruption/resume path coverage")
    check(payloads["interruption-resume-contract.json"]["no_fairness_queue"]["value"].startswith("No queue"), "no fairness queue invented")

    visual = payloads["visual-projection-boundary.json"]
    check({row["name"] for row in visual["frozen_layers"]} >= {"V8", "MapChip"}, "visual layers remain frozen")
    no_behavior_mutation = next(row for row in visual["visual_must_not"] if row["name"] == "noBehaviorMutation")
    check(set(no_behavior_mutation["value"]) >= {"decide movement", "mutate HP", "assign desk"}, "visual mutation boundary")
    product = payloads["product-policy-boundary.json"]
    check(product["preservation_rule"]["value"].startswith("Do not encode"), "product policy preservation rule")
    check("externalTaskId" in {row["name"] for row in product["product_policy_state"]}, "external task state is product-only")
    save = payloads["save-boundary-contract.json"]
    check(save["serialization_status"] == "CONTRACT_ONLY_NO_SAVE_IMPLEMENTATION", "save implementation boundary")
    check(set(save["critical_saved_fields"]["value"]) >= {"hp_", "jobId_", "skillId_", "deskId_", "state_", "moveMode_"}, "critical original save fields")
    check({field["category"] for field in save["fields"]} >= {"ORIGINAL_SAVED", "ORIGINAL_TRANSIENT", "DERIVED"}, "save field classifications")

    scenarios = payloads["runtime-scenario-fixtures.json"]
    check(scenarios["required_fixture_ids"] == [f"S{number}" for number in range(1, 11)], "ten required scenarios")
    check([row["id"] for row in scenarios["fixtures"]] == [f"S{number}" for number in range(1, 11)], "ten scenario fixture rows")
    ledger = payloads["checkpoint-ledger.json"]
    check(ledger["required_stop_literals"] == {
        "I0_started": False,
        "MapChip_changed": False,
        "Renderer_changed": False,
        "V8_started": False,
        "emulator_or_adb": False,
        "inline_only": True,
        "network": False,
        "runtime_implementation_changed": False,
        "static_contract_only": True,
        "subagents": False,
    }, "R0 stop literals")
    check(ledger["records"][-1]["status"] == FINAL_STATUS, "final checkpoint")
    check(validation["implementation_blocker_count"] == 0, "validation blocker count")
    if not i0_active:
        check(validation["runtime_implementation_changed"] is False, "pre-I0 runtime implementation flag")

    print(
        "runtime_contract_freeze_validated "
        f"checks={checks} contracts={len(CONTRACT_FILES)} scenarios=10 blockers=0 "
        f"status={FINAL_STATUS}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"runtime_contract_freeze_validation_failed: {error}")
        raise SystemExit(1)
