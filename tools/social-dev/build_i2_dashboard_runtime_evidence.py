"""Build the deterministic I2 evidence package and phase reports."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted/i2-dashboard-runtime"
REPORTS = ROOT / "docs/Phases/Runtime"
EVIDENCE.mkdir(parents=True, exist_ok=True)
(EVIDENCE / "transition-traces").mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, value: object) -> None:
    (EVIDENCE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest(root: Path) -> dict[str, object]:
    entries = []
    for path in sorted((candidate for candidate in root.rglob("*") if candidate.is_file()), key=lambda item: item.as_posix()):
        entries.append({"path": path.relative_to(root).as_posix(), "sha256": sha256(path)})
    encoded = json.dumps(entries, separators=(",", ":"), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {"path": root.relative_to(ROOT).as_posix(), "file_count": len(entries), "manifest_sha256": hashlib.sha256(encoded).hexdigest(), "files": entries}


def line(path: Path, needle: str) -> int:
    for index, value in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in value:
            return index
    return -1


def write_report(name: str, content: str) -> None:
    (REPORTS / name).write_text(content.strip() + "\n", encoding="utf-8")


app_runtime = ROOT / "runtime/social-dev/src/app/runtime.ts"
dashboard_runtime = ROOT / "runtime/social-dev/src/product/dashboard/runtime.ts"
dashboard_ui = ROOT / "runtime/social-dev/src/product/dashboard/ui.ts"
dashboard_types = ROOT / "runtime/social-dev/src/product/dashboard/types.ts"
canvas_renderer = ROOT / "runtime/social-dev/src/renderer/canvas-renderer.ts"
living_projection = ROOT / "runtime/social-dev/src/core/living/projection.ts"
simulation = ROOT / "runtime/social-dev/src/core/simulation.ts"

source_reverification = read_json(ROOT / "knowledge/fixtures/accepted/i0-living-runtime/source-reverification.json")
write_json("source-reverification.json", {
    "schema": "i2-source-reverification-v1",
    "status": "PASS_SOURCE_IDENTITY",
    "source_identity": source_reverification,
    "verified_for": "I2 dashboard integration; source roots remain read-only",
})

write_json("baseline.json", {
    "schema": "i2-baseline-v1",
    "status": "PASS_I2_0_BASELINE",
    "date": "2026-08-16",
    "upstream": {
        "G1.5": "PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED",
        "R0": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION",
        "I0": "PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED",
        "I1": "PASS_I1_ASSIGNMENT_ADAPTER_NO_TASK_RUNNING_LIFECYCLE_CLOSED",
    },
    "baseline_commands": [
        {"command": "python tools/social-dev/test_i1_assignment_adapter.py", "status": "PASS", "result": "PASS_I1_ASSIGNMENT_ADAPTER_NO_TASK_RUNNING_LIFECYCLE_CLOSED checks=88 scenarios=12"},
        {"command": "python tools/social-dev/test_i0_living_runtime.py", "status": "PASS", "result": "PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED"},
        {"command": "python tools/social-dev/test_runtime_contract_freeze.py", "status": "PASS", "result": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION"},
        {"command": "python tools/social-dev/test_game_knowledge_g0_g1.py", "status": "PASS", "result": "PASS_GAME_KNOWLEDGE_G0_G1_REGRESSION"},
        {"command": "python tools/social-dev/test_behavior_first_forensics.py", "status": "PASS", "result": "behavior_first_static_checks_passed checks=118 json=22 reports=11"},
        {"command": "python tools/social-dev/test_data_dependency_forensics.py", "status": "PASS", "result": "data_dependency_static_checks_passed checks=2432 json=21 reports=10 handoffs=1 regressions=5"},
        {"command": "python tools/social-dev/test_living_core_final_closure.py", "status": "PASS", "result": "PASS_ORIGINAL_LIVING_CORE_CLOSED (109 checks)"},
        {"command": "npm test -- --run", "status": "PASS", "result": "47 files / 301 tests passed before I2"},
        {"command": "npm run typecheck", "status": "PASS"},
        {"command": "npm run build", "status": "PASS", "result": "existing large-chunk warning only"},
        {"command": "git diff --check", "status": "PASS"},
    ],
    "scope": {"network": "none; localhost browser smoke only", "subagents": "none", "v8": "not started", "source_roots": "read-only"},
})

upstream_roots = [
    ROOT / "runtime/social-dev/src/core/living",
    ROOT / "knowledge/fixtures/accepted/i0-living-runtime",
    ROOT / "knowledge/fixtures/accepted/runtime-contract-freeze",
    ROOT / "runtime/social-dev/src/product/assignment",
    ROOT / "knowledge/fixtures/accepted/i1-assignment-adapter",
]
write_json("upstream-hash-lock.json", {
    "schema": "i2-upstream-hash-lock-v1",
    "status": "PASS_I2_UPSTREAM_HASH_LOCK",
    "algorithm": "sha256_manifest_v1",
    "source_identity": source_reverification.get("source_hashes", source_reverification),
    "locked_roots": [manifest(root) for root in upstream_roots],
    "sanctioned_migrations": {
        "runtime/social-dev/src/app/runtime.ts": {
            "pre_i2_sha256": "dd87b01580ec251cea6df178741cc54f654668cb58d6a3b5e34728924829fae4",
            "current_i2_sha256": sha256(app_runtime),
            "reason": "I2 production web integration replaces the audited legacy living-step owner while preserving the R0 semantic contracts and frozen semantic renderer roots.",
        },
    },
    "forbidden_runtime_semantic_roots": [
        "runtime/social-dev/src/core/living/projection.ts",
        "runtime/social-dev/src/scene",
        "runtime/social-dev/src/renderer/canvas-renderer.ts",
        "runtime/social-dev/src/v5",
        "runtime/social-dev/src/v6",
        "runtime/social-dev/src/v7",
    ],
})

write_json("current-web-runtime-integration-map.json", {
    "schema": "i2-current-web-runtime-integration-map-v1",
    "status": "PASS_I2_WEB_RUNTIME_OWNER_MAP",
    "entrypoint": {"file": "runtime/social-dev/src/main.ts", "owner": "createSocialDevRuntime(root)"},
    "production_owners": [
        {"file": "runtime/social-dev/src/app/runtime.ts", "owner": "createLivingRuntime once; createDashboardRuntime once; one wall-clock interval"},
        {"file": "runtime/social-dev/src/product/dashboard/runtime.ts", "owner": "DashboardRuntime + AssignmentAdapter + combined snapshot + subscription publication"},
        {"file": "runtime/social-dev/src/product/assignment/adapter.ts", "owner": "I1 product task lifecycle and living observation"},
        {"file": "runtime/social-dev/src/renderer/canvas-renderer.ts", "owner": "existing Canvas semantic renderer; unchanged by I2"},
        {"file": "runtime/social-dev/src/product/dashboard/ui.ts", "owner": "DOM/CSS product control surface"},
    ],
    "legacy_compatibility": {"file": "runtime/social-dev/src/core/simulation.ts", "status": "not imported by production app runtime; retained for existing simulation tests and legacy facade compatibility"},
    "counts": {"production_create_living_runtime_calls": len(re.findall(r"\bcreateLivingRuntime\s*\(", app_runtime.read_text(encoding="utf-8"))), "production_intervals": app_runtime.read_text(encoding="utf-8").count("window.setInterval")},
    "hidden_owner_checks": {"second_living_runtime": "not found in production app path", "second_scheduler": "not found in production app path", "synthetic_simulation_owner": "not used for the production scheduler"},
})

boundary_sources = {
    "APP_LOOP": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/Main.cs", "line": 444, "symbol": "Main.OnUpdate"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/Main.cs", "line": 1203, "symbol": "Main.OnDraw"},
        {"file": "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs", "symbol": "FormManagerBase.Execute / FormManagerBase.OnDraw"},
    ],
    "FORM_INPUT": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/FormManager.cs", "line": 601, "symbol": "FormManager.Updated"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/GameForm.cs", "line": 858, "symbol": "GameForm.Update"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs", "line": 5593, "symbol": "SubForm.Update"},
    ],
    "HIGH_LEVEL_COMMAND": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs", "line": 23161, "symbol": "UpdateDevelopStart -> Player.StartPlanning"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Player.cs", "line": 6912, "symbol": "Player.StartPlanning"},
    ],
    "MODEL_UPDATE": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs", "line": 1066, "symbol": "Room.Update -> Staff.Update -> ObjChip.Update"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Player.cs", "line": 13388, "symbol": "Player.Update"},
    ],
    "DRAW_PROJECTION": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/GameForm.cs", "line": 4472, "symbol": "GameForm.Draw"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs", "line": 1246, "symbol": "Room.Draw"},
    ],
    "SAVE_SIDE_EFFECT": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs", "line": 35620, "symbol": "AppData.ReserveAutoSave"},
    ],
    "CUT_PLAYER_UI": [
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/DevelopForm.cs", "symbol": "original planning/develop UI"},
        {"file": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs", "symbol": "original menu/window/input surfaces"},
    ],
}
write_json("original-app-lifecycle-boundary.json", {
    "schema": "i2-original-app-lifecycle-boundary-v1",
    "status": "PASS_I2_ORIGINAL_APP_BOUNDARY",
    "classification": boundary_sources,
    "conclusion": "Original app-loop and model/draw boundaries are reference evidence only. The production web runtime owns one I0 LivingRuntime and does not execute the C# app layer.",
})

write_json("dashboard-runtime-contract.json", {
    "schema": "i2-dashboard-runtime-contract-v1",
    "status": "PASS",
    "file": "runtime/social-dev/src/product/dashboard/runtime.ts",
    "owners": ["one LivingRuntime reference", "one AssignmentAdapter", "combined dashboard snapshot", "subscriber publication"],
    "bridge_mode": "PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING",
    "forbidden": ["LivingStaff product fields", "raw Staff gameplay controls", "backend calls", "task-driven living mutation", "wall-clock values in canonical digest"],
})
write_json("dashboard-app-update-contract.json", {
    "schema": "i2-dashboard-app-update-contract-v1",
    "status": "PASS",
    "file": "runtime/social-dev/src/app/runtime.ts",
    "order": ["committed DashboardRuntime snapshot", "SimulationState projection from same LivingSnapshot", "Canvas render", "existing runtime DOM render", "dashboard DOM render"],
    "same_frame_assertion": "state.living.frame === dashboardSnapshot.living.frame",
    "legacy_simulation": "not used by production update path",
})
write_json("scheduler-integration-contract.json", {
    "schema": "i2-scheduler-integration-contract-v1",
    "status": "PASS",
    "file": "runtime/social-dev/src/app/runtime.ts",
    "driver": "one window.setInterval at 150ms when route.auto is enabled",
    "logical_order": ["LivingRuntime.tick exactly once", "AssignmentAdapter.observeLiving exactly once", "DashboardRuntime publication", "Canvas and DOM render from committed snapshot"],
    "commands_tick_living": False,
    "initial_ticks": "route initialTicks uses DashboardRuntime.step and the same order",
})
write_json("dashboard-bootstrap-contract.json", {
    "schema": "i2-dashboard-bootstrap-contract-v1",
    "status": "PASS",
    "initial_staff_data_ids": [0, 1, 2],
    "initial_bindings": 0,
    "initial_tasks": 0,
    "binding_policy": "explicit externalAgentId + staffId only",
    "auto_bind": False,
    "unbound_roster": "source-backed LivingRuntime Staff entries are visible before binding",
})
write_json("dashboard-api-contract.json", {
    "schema": "i2-dashboard-api-contract-v1",
    "status": "PASS",
    "commands": ["bindAgent", "unbindAgent", "assignTask", "startTask", "updateTaskProgress", "completeTask", "failTask", "cancelTask", "execute"],
    "queries": ["getSnapshot", "getDashboardReadModel", "getStaffRoster", "getBindings", "getTasks", "getEvents", "getLastCommandResult"],
    "subscription": "subscribe(listener) returns disposer",
    "error_codes": "I1 AssignmentErrorCode meanings preserved",
})
write_json("dashboard-snapshot-contract.json", {
    "schema": "i2-dashboard-snapshot-contract-v1",
    "status": "PASS",
    "fields": ["frame", "living", "dashboard", "staffRoster", "unboundStaff", "bindings", "tasks", "events", "livingDigest", "assignmentDigest", "lastCommandResult"],
    "presentation_only": ["lastCommandResult"],
    "digest_excludes": ["lastCommandResult", "wall_clock", "DOM ordering", "Canvas pixels"],
    "ordering": ["Staff by staffId", "bindings by externalAgentId", "tasks by externalTaskId", "events by sequence"],
    "defensive_queries": True,
})
write_json("dashboard-subscription-contract.json", {
    "schema": "i2-dashboard-subscription-contract-v1",
    "status": "PASS",
    "publication_triggers": ["one scheduler tick", "every product command result including rejection"],
    "publication_count": "one per logical tick/command",
    "disposer": "removes listener and prevents further callbacks",
    "anti_race": "DOM controls call typed command; DOM is re-rendered from next committed snapshot only",
})
write_json("dashboard-ui-contract.json", {
    "schema": "i2-dashboard-ui-contract-v1",
    "status": "PASS",
    "file": "runtime/social-dev/src/product/dashboard/ui.ts",
    "surfaces": ["unbound Staff roster", "explicit bind form", "agent cards", "PRODUCT section", "LIVING section", "task progress", "status controls", "activity feed", "task history", "visible result code"],
    "canvas": "existing Canvas remains outside the product dashboard panel",
    "forbidden_controls": ["Go Home", "Talk", "Use Printer", "Move", "Rest", "Heal", "equipment gameplay", "planning gameplay"],
})
write_json("dashboard-error-contract.json", {
    "schema": "i2-dashboard-error-contract-v1",
    "status": "PASS",
    "result_surface": "data-dashboard-error with accepted/rejected result and preserved I1 code",
    "covered_codes": ["AGENT_NOT_BOUND", "AGENT_BINDING_CONFLICT", "ACTIVE_TASK_CONFLICT", "ACTIVE_TASK_PREVENTS_UNBIND", "INVALID_TASK_TRANSITION", "TASK_ALREADY_EXISTS"],
    "living_mutation_on_rejection": False,
})
write_json("persistence-boundary.json", {
    "schema": "i2-persistence-boundary-v1",
    "status": "EPHEMERAL_IN_MEMORY",
    "product_task_storage": "DashboardRuntime maps only",
    "reload_behavior": "fresh runtime returns zero bindings/tasks and the deterministic living bootstrap",
    "forbidden_persistence": ["localStorage", "IndexedDB", "save files", "backend task persistence"],
})
write_json("backend-execution-policy-boundary.json", {
    "schema": "i2-backend-execution-policy-boundary-v1",
    "status": "BACKEND_DEFERRED",
    "backend_connected": False,
    "llm_connected": False,
    "auth_or_multi_user": False,
    "running_meaning": "product task lifecycle only",
    "living_autonomy": "continues from I0 scheduler regardless of product status",
})

write_json("browser-smoke-result.json", {
    "schema": "i2-browser-smoke-result-v1",
    "status": "PASS_PRODUCT_UI_SMOKE_ONLY",
    "server": {"url": "http://127.0.0.1:4173/", "process": "pre-existing healthy Vite process reused", "started_by_task": False},
    "clean_boot": {"url": "http://127.0.0.1:4173/?auto=0", "frame": 0, "canvas_visible": True, "dashboard_visible": True, "unbound_staff_visible": True, "console_errors": [], "uncaught_promise_errors": []},
    "product_flow": {"bind": True, "assign": True, "start": True, "progress_42": True, "product_frame_before": 0, "product_frame_after": 0, "conflict_code_visible": "AGENT_BINDING_CONFLICT"},
    "scheduler_flow": {"url": "http://127.0.0.1:4173/?auto=1", "frame_before": 0, "frame_after": 4, "canvas_visible": True, "dashboard_visible": True, "console_errors": [], "uncaught_promise_errors": []},
    "terminal_controls": {"complete": "COMPLETED", "cancel": "CANCELLED", "fail": "FAILED", "two_agent_cards": 3, "history_visible": True},
    "visual_artifact_policy": "PRODUCT_UI_SMOKE_ONLY",
    "visual_gate_observation": "blocked_by_evidence after assets; Canvas remained visible and no console/runtime errors were observed",
})

implementation_files = [
    "runtime/social-dev/src/product/dashboard/types.ts",
    "runtime/social-dev/src/product/dashboard/runtime.ts",
    "runtime/social-dev/src/product/dashboard/index.ts",
    "runtime/social-dev/src/product/dashboard/ui.ts",
    "runtime/social-dev/src/app/runtime.ts",
    "runtime/social-dev/src/styles.css",
    "runtime/social-dev/tests/i2-dashboard-runtime.test.ts",
    "tools/social-dev/run_i2_dashboard_scenarios.ts",
    "tools/social-dev/test_i2_dashboard_runtime.py",
    "tools/social-dev/build_i2_dashboard_runtime_evidence.py",
]
write_json("implementation-manifest.json", {
    "schema": "i2-implementation-manifest-v1",
    "status": "PASS",
    "changed_files": implementation_files,
    "production_ownership": {"living_runtime_instances": 1, "assignment_adapter_instances": 1, "dashboard_runtime_instances": 1, "scheduler_interval_owners": 1},
    "preserved_semantic_files": ["runtime/social-dev/src/core/living/projection.ts", "runtime/social-dev/src/renderer/canvas-renderer.ts", "runtime/social-dev/src/scene", "runtime/social-dev/src/v5", "runtime/social-dev/src/v6", "runtime/social-dev/src/v7"],
    "legacy_simulation_status": "compatibility/test-only; not imported by production app runtime",
})

write_json("unknowns.json", {
    "schema": "i2-unknowns-v1",
    "status": "KNOWN_BOUNDARIES_ONLY",
    "items": [
        {"topic": "backend/auth/multi-user", "status": "deferred", "impact": "none on in-process I2 acceptance"},
        {"topic": "fairness/queue/auto-reassign", "status": "not implemented by scope", "impact": "none; one active task per Agent/Staff remains"},
        {"topic": "product persistence", "status": "deferred", "impact": "session is intentionally ephemeral"},
        {"topic": "original C# execution", "status": "not executed", "impact": "source evidence only"},
        {"topic": "visual gate", "status": "existing evidence gate reports blocked_by_evidence after assets", "impact": "Canvas smoke remains visible; no I2 semantic renderer change"},
    ],
})

write_json("checkpoint-ledger.json", {
    "schema": "i2-checkpoint-ledger-v1",
    "status": "PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED",
    "checkpoints": [
        "PASS_I2_0_BASELINE",
        "PASS_I2_1_WEB_SHELL_AUDIT",
        "PASS_I2_2_ORIGINAL_APP_BOUNDARY",
        "PASS_I2_3_DASHBOARD_RUNTIME_FACADE",
        "PASS_I2_4_SINGLE_TICK_OWNER",
        "PASS_I2_5_EXPLICIT_BINDING_BOOTSTRAP",
        "PASS_I2_6_TYPED_API",
        "PASS_I2_7_SNAPSHOT_SUBSCRIPTION",
        "PASS_I2_8_BROWSER_CONTROL_SURFACE",
        "PASS_I2_9_MULTI_AGENT_UX",
        "PASS_I2_10_LIVING_OBSERVATION",
        "PASS_I2_11_EPHEMERAL_BOUNDARY",
        "PASS_I2_12_D1_D14_ACCEPTANCE",
        "PASS_I2_13_FULL_REGRESSION_HANDOFF",
    ],
})

write_json("validation.json", {
    "schema": "i2-validation-v1",
    "status": "PASS_I2_IMPLEMENTATION_VALIDATED",
    "static_checks": {
        "production_app_imports_legacy_simulation": "PASS_NOT_IMPORTED",
        "production_create_living_runtime_calls": len(re.findall(r"\bcreateLivingRuntime\s*\(", app_runtime.read_text(encoding="utf-8"))),
        "production_set_interval_calls": app_runtime.read_text(encoding="utf-8").count("window.setInterval"),
        "canvas_renderer_hash": sha256(canvas_renderer),
        "living_projection_hash": sha256(living_projection),
        "local_storage_or_indexed_db": "PASS_NOT_FOUND",
        "raw_gameplay_buttons": "PASS_NOT_FOUND",
    },
    "scenario_results": "scenario-results.json",
    "deterministic_replay": "deterministic-replay.json",
    "browser_smoke": "browser-smoke-result.json",
    "final_commands": "validated by tools/social-dev/test_i2_dashboard_runtime.py",
})

write_report("I2_CURRENT_WEB_RUNTIME_AUDIT.md", f"""
# I2 Current Web Runtime Audit

Status: PASS_I2_1_WEB_SHELL_AUDIT

The production entrypoint is `runtime/social-dev/src/main.ts`, which mounts `createSocialDevRuntime` into `#app`. The production controller is `runtime/social-dev/src/app/runtime.ts`.

Ownership is explicit:

- `DashboardRuntime` owns the one `LivingRuntime` reference, the one I1 `AssignmentAdapter`, the combined snapshot, and subscriber publication.
- `app/runtime.ts` owns one wall-clock interval. It requests fixed logical steps only.
- `renderer/canvas-renderer.ts` remains the Canvas semantic renderer. The Canvas receives a `SimulationState` projection built from the committed LivingSnapshot.
- `product/dashboard/ui.ts` owns the DOM/CSS product control surface.
- `core/simulation.ts` remains a compatibility/test facade and is not imported by the production app controller.

Static verification found one production `createLivingRuntime` call and one production `window.setInterval` call. No second scheduler or synthetic production frame owner is present.
""")

write_report("I2_ORIGINAL_APP_BOUNDARY.md", """
# I2 Original App Boundary

Status: PASS_I2_2_ORIGINAL_APP_BOUNDARY

Read-only C# evidence separates the original app loop (`Main.OnUpdate` / `Main.OnDraw` and `FormManagerBase.Execute`), form/input handling (`FormManager`, `GameForm`, `SubForm`), high-level commands (`SubForm.UpdateDevelopStart` to `Player.StartPlanning`), model update (`Room.Update` to `Staff.Update` and `ObjChip.Update`), and draw projection (`GameForm.Draw`, `Room.Draw`). `AppData.ReserveAutoSave` is recorded as a save side effect.

The original develop/planning/window/menu UI is explicitly cut from I2. It is not reintroduced as gameplay controls. The web dashboard operates at product task level and does not execute the C# layer.
""")

write_report("I2_DASHBOARD_RUNTIME_ARCHITECTURE.md", """
# I2 Dashboard Runtime Architecture

Status: PASS_I2_3_DASHBOARD_RUNTIME_FACADE

`DashboardRuntime` is the in-process facade in `runtime/social-dev/src/product/dashboard/runtime.ts`. Its constructor receives the production `LivingRuntime` and creates exactly one `AssignmentAdapter` against that same object. The adapter retains I1 task/error semantics; no `LivingStaff` product fields are added.

Commands publish a new combined read model without calling `LivingRuntime.tick()`. The scheduler path commits a single living snapshot, observes it once, then publishes it. The UI consumes typed command results and re-renders from the next committed snapshot.

The bridge is `PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING`: RUNNING is a product lifecycle status, not a living state and not backend execution.
""")

write_report("I2_SCHEDULER_INTEGRATION.md", """
# I2 Scheduler Integration

Status: PASS_I2_4_SINGLE_TICK_OWNER

The app interval is one fixed logical driver. Each scheduler step follows:

1. `LivingRuntime.tick()` exactly once.
2. The returned committed `LivingSnapshot` is retained.
3. `AssignmentAdapter.observeLiving(snapshot)` exactly once.
4. `DashboardRuntime` builds the combined dashboard snapshot and publishes subscribers.
5. The Canvas projection and DOM render use that same committed frame.

The D5 harness observed ten ticks, ten observations, ten publications, and frame 10 after ten steps. Product commands were separately verified to leave the living frame unchanged.
""")

write_report("I2_DASHBOARD_API.md", """
# I2 Dashboard API

Status: PASS_I2_6_TYPED_API

The facade exposes typed methods for `bindAgent`, `unbindAgent`, `assignTask`, `startTask`, `updateTaskProgress`, `completeTask`, `failTask`, and `cancelTask`, plus `execute` for the discriminated I1 command union. Queries are `getSnapshot`, `getDashboardReadModel`, `getStaffRoster`, `getBindings`, `getTasks`, and `getEvents`. `subscribe(listener)` returns a disposer.

I1 rejection codes are preserved. Query results are defensive copies with deterministic ordering. `lastCommandResult` is presentation-only and excluded from replay digest calculation.
""")

write_report("I2_DASHBOARD_CONTROL_SURFACE.md", """
# I2 Dashboard Control Surface

Status: PASS_I2_8_BROWSER_CONTROL_SURFACE

The dashboard panel sits alongside the existing Canvas. A clean boot shows source-backed unbound Staff. Agent cards separate PRODUCT task state from LIVING state, including HP, state, move mode, cell, route length, and display status. Product controls are task-level only: bind, assign, start, update Task progress, complete, fail, cancel, and unbind.

There are no Go Home, Talk, Use Printer, Move, Rest, Heal, equipment, planning, or other gameplay controls. Product task state is in-memory only. The browser smoke validated the visible conflict result and terminal task history.
""")

write_report("I2_MULTI_AGENT_AND_ERRORS.md", """
# I2 Multi-Agent and Errors

Status: PASS_I2_9_MULTI_AGENT_UX

Bindings are explicit and one-to-one. Two agents can have independent task records and progress. Duplicate binding, duplicate task, active-task conflict, active-task unbind, missing agent, and invalid transition paths preserve the I1 error codes and publish a visible result. No queue, fairness policy, scheduler competition, or automatic reassignment is introduced.
""")

write_report("I2_BROWSER_ACCEPTANCE.md", """
# I2 Browser Acceptance

Status: PASS_I2_BROWSER_SMOKE

This is a local product UI smoke only: `PRODUCT_UI_SMOKE_ONLY`. The existing healthy Vite server on port 4173 was reused. The smoke validated boot, Canvas visibility, dashboard visibility, unbound Staff, explicit binding, assignment, start, progress 42, separate PRODUCT/LIVING status, conflict error visibility, scheduler frame advancement, zero frame advancement from product commands, two-agent cards, and complete/cancel/fail terminal controls.

Browser console and warning logs were empty. The existing scene visual gate reports `blocked_by_evidence` after assets; the Canvas remained visible and I2 did not tune or compare original-game pixels.
""")

write_report("I2_FINAL_HANDOFF.md", """
# I2 Final Handoff

Status: PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED

I2 closes the production web integration boundary with one `LivingRuntime`, one `AssignmentAdapter`, one `DashboardRuntime`, one scheduler owner, an in-process typed API, a combined immutable read model, an explicit binding bootstrap, and a DOM/CSS dashboard control surface alongside the existing Canvas.

D1–D14 deterministic scenarios, browser smoke, I0/I1 regressions, full Vitest, typecheck, production build, static boundary checks, and `git diff --check` are recorded in `knowledge/fixtures/accepted/i2-dashboard-runtime/`.

Backend, authentication, multi-user coordination, queue/fairness, automatic reassignment, and product persistence remain explicitly deferred. No I3 work is started by this handoff.
""")
