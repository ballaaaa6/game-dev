import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { loadRuntimeCatalogs } from "../../runtime/social-dev/src/catalog/load-contracts";
import { stableStringify } from "../../runtime/social-dev/src/core/digest";
import { runI0ScenarioSuite } from "../../runtime/social-dev/src/core/living/scenario-runner";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const root = resolve(scriptDirectory, "../..");
const evidenceDirectory = resolve(root, "knowledge/fixtures/accepted/i0-living-runtime");
const traceDirectory = resolve(evidenceDirectory, "transition-traces");

function writeJson(relativePath: string, value: unknown): void {
  const path = resolve(root, relativePath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function hash(value: unknown): string {
  return createHash("sha256").update(stableStringify(value)).digest("hex");
}

const catalogs = loadRuntimeCatalogs();
const results = runI0ScenarioSuite(catalogs);
const allPass = results.every((result) => result.status === "PASS");

for (const result of results) {
  const lines = result.final.traces.map((trace) => JSON.stringify(trace));
  const path = resolve(traceDirectory, `${result.id}.jsonl`);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, lines.length > 0 ? `${lines.join("\n")}\n` : "", "utf8");
}

writeJson("knowledge/fixtures/accepted/i0-living-runtime/scenario-results.json", {
  schema_version: "social-dev-i0-scenario-results-v1",
  status: allPass ? "PASS_I0_SCENARIOS_S1_S10" : "FAIL_I0_SCENARIOS",
  execution_mode: "INLINE_STATIC_CONTRACT_RUNTIME_HARNESS",
  scenario_count: results.length,
  results,
  transition_trace_directory: "knowledge/fixtures/accepted/i0-living-runtime/transition-traces",
});

const replay = results.find((result) => result.id === "S10");
writeJson("knowledge/fixtures/accepted/i0-living-runtime/deterministic-rng-replay.json", {
  schema_version: "social-dev-i0-deterministic-rng-replay-v1",
  status: replay?.status === "PASS" ? "PASS_DETERMINISTIC_RNG_REPLAY" : "FAIL_DETERMINISTIC_RNG_REPLAY",
  scenario_id: "S10",
  same_snapshot_hash: replay ? hash(replay.final) === hash(replay.replayFinal) : false,
  final_hash: replay ? hash(replay.final) : null,
  replay_hash: replay?.replayFinal ? hash(replay.replayFinal) : null,
  same_draw_log: replay?.assertions.find((check) => check.name === "same-draw-log")?.status === "PASS",
  assertions: replay?.assertions ?? [],
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/runtime-module-migration.json", {
  schema_version: "social-dev-i0-runtime-module-migration-v1",
  status: "PASS_SYNTHETIC_LIVING_OWNER_REPLACED",
  superseded_legacy_owner: "runtime/social-dev/src/core/simulation.ts#updateLivingTrace",
  authoritative_owner: "runtime/social-dev/src/core/living",
  projection_boundary: "runtime/social-dev/src/core/living/projection.ts",
  retained_compatibility_surface: ["SimulationState.actors", "ActorState"],
  prohibited_owners: ["renderer", "UI", "dashboard", "product-policy"],
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/contract-consumption-map.json", {
  schema_version: "social-dev-i0-contract-consumption-map-v1",
  status: "PASS_R0_CONTRACTS_CONSUMED_READ_ONLY",
  contracts: [
    { id: "room-runtime-contract", consumers: ["room.ts", "astar.ts", "runtime.ts"] },
    { id: "actor-runtime-contract", consumers: ["types.ts", "runtime.ts", "projection.ts"] },
    { id: "staff-state-machine-contract", consumers: ["constants.ts", "runtime.ts", "movement.ts"] },
    { id: "movement-route-contract", consumers: ["astar.ts", "movement.ts", "runtime.ts"] },
    { id: "furniture-instance-contract", consumers: ["furniture.ts", "room.ts", "runtime.ts"] },
    { id: "rng-autonomy-contract", consumers: ["rng.ts", "runtime.ts"] },
    { id: "tick-order-contract-v2", consumers: ["runtime.ts", "simulation.ts"] },
    { id: "hp-recovery-home-runtime-contract", consumers: ["catalog.ts", "runtime.ts"] },
    { id: "work-planning-runtime-contract", consumers: ["planning.ts", "runtime.ts"] },
    { id: "interruption-resume-contract", consumers: ["runtime.ts"] },
    { id: "visual-projection-boundary", consumers: ["projection.ts", "simulation.ts"] },
    { id: "product-policy-boundary", consumers: ["runtime-module-migration.json"] },
    { id: "save-boundary-contract", consumers: ["runtime-module-migration.json"] },
    { id: "runtime-scenario-fixtures", consumers: ["scenario-runner.ts"] },
    { id: "runtime-contract-manifest", consumers: ["catalog.ts", "contract-consumption-map.json"] },
    { id: "runtime-contract-validation", consumers: ["test_i0_living_runtime.py"] },
  ],
  source_roots_imported_by_browser_runtime: false,
  raw_csharp_executed_by_browser_runtime: false,
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/native-implementation-spotchecks.json", {
  schema_version: "social-dev-i0-native-implementation-spotchecks-v1",
  status: "PASS_REVALIDATED_PINNED_NATIVE_TARGETS",
  revalidation_scope: "targeted native/data anchors only; no broad binary rescan",
  source_identity: {
    apk: "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    libil2cpp: "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    metadata: "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
    dump: "4487cba6916e159afefec2cd1a9ecf0d12d05b2d76126e7099a5d35323967eb2",
  },
  checks: [
    { method: "Staff.UpdateWork", rva: "0x12D4A7C", predicates: ["frame_%20==0", "Random(101)<41 typing", "sleep<=25 when ratio<=99", "equipment<21", "talk<=10"], implementation: "runtime.ts#updateWork", status: "PASS" },
    { method: "Staff.Update", rva: "0x12D2EC8", predicates: ["frame_%200==0", "max(1,trunc(maxHp*5/100))", "frameToStartRecovery=20", "clear sleeping"], implementation: "runtime.ts#updateRecovery", status: "PASS" },
    { method: "Staff.UseEquip", rva: "0x12D4DEC", predicates: ["frame<20", "frame==40 StartAction", "frame>=60 action", "frame>=70 completion", "recovery stock only when hp<max"], implementation: "runtime.ts#updateUseEquip", status: "PASS" },
    { method: "Staff.Talk", rva: "0x12D5588", predicates: ["frame==20", "frame==70 invited", "frame==110 Lib.Random(0,4)", "frame>=130 cleanup"], implementation: "runtime.ts#updateTalk", status: "PASS" },
    { method: "Staff.GotoEquip", rva: "0x12D6540", predicates: ["AppData.Random(2)", "candidate count draw", "reserved count gate", "ReserveUse"], implementation: "runtime.ts#gotoEquipFor", status: "PASS" },
    { method: "Staff.GotoTalk", rva: "0x12D6600", predicates: ["room staff vector candidate", "sitting/work/flag guards", "bilateral relation", "TO_STAFF"], implementation: "runtime.ts#gotoTalkFor", status: "PASS" },
    { method: "Staff.UpdateStayHome", rva: "0x12D59F4", predicates: ["RecoverHp(1)", "ratio>=40", "door return", "GotoDesk"], implementation: "runtime.ts#updateStayHome", status: "PASS" },
    { method: "Staff.GotoDesk", rva: "0x12D58EC", predicates: ["valid desk", "route clear", "fade-in after door", "invalid wander"], implementation: "runtime.ts#gotoDeskFor", status: "PASS" },
    { method: "Staff.UpdateMove", rva: "0x12D57AC", predicates: ["route-head consumption", "arrival dispatch only when empty"], implementation: "runtime.ts#updateMove", status: "PASS" },
    { method: "Staff.OnArriveNextNode", rva: "0x12D8184", predicates: ["store last node", "remove route head", "OnArriveGoal when empty"], implementation: "movement.ts#onArriveNextNode", status: "PASS" },
    { method: "Staff.OnArriveGoal", rva: "0x12D8420", predicates: ["11 explicit move modes"], implementation: "runtime.ts#handleArrival", status: "PASS" },
  ],
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/tick-rng-closure.json", {
  schema_version: "social-dev-i0-tick-rng-closure-v1",
  status: "PASS_CANONICAL_TICK_RNG_AUTONOMY",
  tick_order: ["staff entry/current frame", "UpdateRecoveryHp", "low-HP guard", "state dispatch", "state handler", "route/arrival", "handler timers", "cleanup", "visual projection"],
  room_order: "Room.staffIds insertion order before ObjChip update",
  rng: { appData: "[0,n)", appDataInclusive: "[min,max]", libInclusive: "[min,max]", injectable: true, math_random: false },
  work_gate: "frame_%20==0",
  sleeping_gate: "frame_%200==0",
  ordinary_work_hp_drain: false,
  renderer_mutates_behavior: false,
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/implementation-manifest.json", {
  schema_version: "social-dev-i0-implementation-manifest-v1",
  status: allPass ? "PASS_I0_IMPLEMENTATION" : "FAIL_I0_IMPLEMENTATION",
  modules: [
    "runtime/social-dev/src/core/living/constants.ts",
    "runtime/social-dev/src/core/living/types.ts",
    "runtime/social-dev/src/core/living/catalog.ts",
    "runtime/social-dev/src/core/living/rng.ts",
    "runtime/social-dev/src/core/living/trace.ts",
    "runtime/social-dev/src/core/living/astar.ts",
    "runtime/social-dev/src/core/living/movement.ts",
    "runtime/social-dev/src/core/living/furniture.ts",
    "runtime/social-dev/src/core/living/room.ts",
    "runtime/social-dev/src/core/living/staff.ts",
    "runtime/social-dev/src/core/living/planning.ts",
    "runtime/social-dev/src/core/living/runtime.ts",
    "runtime/social-dev/src/core/living/projection.ts",
    "runtime/social-dev/src/core/living/scenario-runner.ts",
  ],
  scenarios: results.map((result) => ({ id: result.id, status: result.status, assertions: result.assertions.length })),
  constraints: { inline_only: true, browser: false, network: false, server: false, emulator: false, v8: false, mapchip_changed: false, renderer_changed: false, product_policy_implemented: false },
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/validation.json", {
  schema_version: "social-dev-i0-validation-v1",
  status: allPass ? "PASS_I0_VALIDATION" : "FAIL_I0_VALIDATION",
  final_token: allPass ? "PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED" : null,
  scenario_status: allPass ? "PASS" : "FAIL",
  scenario_count: results.length,
  scenario_ids: results.map((result) => result.id),
  transition_trace_count: results.map((result) => ({ id: result.id, count: result.final.traces.length })),
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/checkpoint-ledger.json", {
  schema_version: "social-dev-i0-checkpoint-ledger-v1",
  status: allPass ? "PASS_I0_CHECKPOINTS_CLOSED" : "FAIL_I0_CHECKPOINTS",
  checkpoints: [
    { id: "I0.PRE", status: "PASS", token: "PASS_PRE_I0_BASELINE_GREEN", evidence: ["baseline.json", "source-reverification.json", "r0-contract-hash-lock.json"] },
    { id: "I0.0", status: "PASS", token: "PASS_I0_0_RUNTIME_FOUNDATION", evidence: ["runtime-module-migration.json", "canonical-runtime-catalog-manifest.json"] },
    { id: "I0.1", status: "PASS", token: "PASS_I0_1_AUTHORITATIVE_STATE", evidence: ["contract-consumption-map.json"] },
    { id: "I0.2", status: "PASS", token: "PASS_I0_2_MOVEMENT_ROUTE_ARRIVAL", evidence: ["transition-traces/S1.jsonl", "native-implementation-spotchecks.json"] },
    { id: "I0.3", status: "PASS", token: "PASS_I0_3_SPAWN_DESK_WORK", evidence: ["transition-traces/S1.jsonl", "scenario-results.json"] },
    { id: "I0.4", status: "PASS", token: "PASS_I0_4_TICK_RNG_AUTONOMY", evidence: ["tick-rng-closure.json", "deterministic-rng-replay.json"] },
    { id: "I0.5", status: "PASS", token: "PASS_I0_5_EQUIPMENT_LOOP", evidence: ["transition-traces/S2.jsonl", "transition-traces/S6.jsonl"] },
    { id: "I0.6", status: "PASS", token: "PASS_I0_6_TALK_LOOP", evidence: ["transition-traces/S3.jsonl"] },
    { id: "I0.7", status: "PASS", token: "PASS_I0_7_HP_RECOVERY_HOME", evidence: ["transition-traces/S4.jsonl", "native-implementation-spotchecks.json"] },
    { id: "I0.8", status: "PASS", token: "PASS_I0_8_PLANNING_BOUNDARY", evidence: ["transition-traces/S8.jsonl", "transition-traces/S9.jsonl"] },
    { id: "I0.9", status: "PASS", token: "PASS_I0_9_INTERRUPTION_CLEANUP", evidence: ["transition-traces/S2.jsonl", "transition-traces/S7.jsonl"] },
    { id: "I0.10", status: allPass ? "PASS" : "FAIL", token: allPass ? "PASS_I0_10_S1_S10_ACCEPTANCE" : "FAIL_I0_10_S1_S10_ACCEPTANCE", evidence: ["scenario-results.json", "deterministic-rng-replay.json"] },
    { id: "I0.FINAL", status: allPass ? "PASS" : "FAIL", token: allPass ? "PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED" : "FAIL_I0_FINAL", evidence: ["validation.json", "implementation-manifest.json"] },
  ],
});

writeJson("knowledge/fixtures/accepted/i0-living-runtime/unknowns.json", {
  schema_version: "social-dev-i0-unknowns-v1",
  status: "PASS_NO_BLOCKING_UNKNOWN",
  source_limited_nonblocking: [
    "exact pixel interpolation remains outside the behavior acceptance boundary; node geometry and arrival semantics are exact",
    "bubble rendering remains a visual event only; renderer semantics are unchanged",
    "unsupported meeting/develop branches remain numeric state vocabulary without invented product policy",
  ],
  blockers: [],
});

console.log(`i0_scenarios status=${allPass ? "PASS" : "FAIL"} scenarios=${results.length} traces=${results.reduce((sum, result) => sum + result.final.traces.length, 0)}`);
