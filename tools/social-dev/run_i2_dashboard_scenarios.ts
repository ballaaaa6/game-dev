import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { loadRuntimeCatalogs } from "../../runtime/social-dev/src/catalog/load-contracts";
import { StaffFlag, StaffState } from "../../runtime/social-dev/src/core/living/constants";
import { createLivingRuntime, type LivingRuntime } from "../../runtime/social-dev/src/core/living/runtime";
import { createDashboardRuntime, type DashboardRuntime, type DashboardRuntimeSnapshot } from "../../runtime/social-dev/src/product/dashboard";
import { stableStringify } from "../../runtime/social-dev/src/product/assignment/snapshot";

const catalogs = loadRuntimeCatalogs();
const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const evidenceDirectory = resolve(scriptDirectory, "../../knowledge/fixtures/accepted/i2-dashboard-runtime");
const traceDirectory = resolve(evidenceDirectory, "transition-traces");
mkdirSync(traceDirectory, { recursive: true });

interface ScenarioCheck {
  readonly name: string;
  readonly status: "PASS" | "FAIL";
  readonly observed: unknown;
}

interface TraceLine {
  readonly scenario: string;
  readonly sequence: number;
  readonly operation: string;
  readonly frame: number;
  readonly livingDigest: string;
  readonly assignmentDigest: string;
  readonly bindings: readonly string[];
  readonly tasks: readonly { readonly id: string; readonly agent: string; readonly status: string; readonly progress: number }[];
  readonly eventTypes: readonly string[];
  readonly details?: Record<string, unknown>;
}

interface ScenarioResult {
  readonly id: string;
  readonly status: "PASS" | "FAIL";
  readonly checks: readonly ScenarioCheck[];
  readonly trace_lines: number;
  readonly error: string | null;
}

function fixture(staffDataIds: readonly number[] = [0], scenarioEquipment = false): { readonly living: LivingRuntime; readonly dashboard: DashboardRuntime } {
  const living = createLivingRuntime(catalogs, {
    initialStaffDataIds: staffDataIds,
    scenarioEquipment,
    appDataReplay: [0, 0, 0, 0, 0, 0],
    libReplay: [0, 0, 0, 0],
  });
  return { living, dashboard: createDashboardRuntime(living) };
}

function traceLine(scenario: string, sequence: number, operation: string, snapshot: DashboardRuntimeSnapshot, details?: Record<string, unknown>): TraceLine {
  return {
    scenario,
    sequence,
    operation,
    frame: snapshot.frame,
    livingDigest: snapshot.livingDigest,
    assignmentDigest: snapshot.assignmentDigest,
    bindings: snapshot.bindings.map((binding) => `${binding.externalAgentId}->${binding.staffId}`),
    tasks: snapshot.tasks.map((task) => ({ id: task.externalTaskId, agent: task.externalAgentId, status: task.status, progress: task.externalProgress })),
    eventTypes: snapshot.events.slice(-8).map((event) => event.type),
    details,
  };
}

function runScenario(id: string, run: (checks: ScenarioCheck[], traces: TraceLine[]) => void): ScenarioResult {
  const checks: ScenarioCheck[] = [];
  const traces: TraceLine[] = [];
  let error: string | null = null;
  try {
    run(checks, traces);
  } catch (caught) {
    error = caught instanceof Error ? caught.message : String(caught);
  }
  const result: ScenarioResult = {
    id,
    status: error === null && checks.every((check) => check.status === "PASS") ? "PASS" : "FAIL",
    checks,
    trace_lines: traces.length,
    error,
  };
  writeFileSync(resolve(traceDirectory, `${id}.jsonl`), traces.map((line) => JSON.stringify(line)).join("\n") + "\n", "utf8");
  return result;
}

function check(checks: ScenarioCheck[], name: string, condition: boolean, observed: unknown): void {
  checks.push({ name, status: condition ? "PASS" : "FAIL", observed });
  if (!condition) throw new Error(`${name} failed: ${JSON.stringify(observed)}`);
}

function record(traces: TraceLine[], id: string, sequence: number, operation: string, dashboard: DashboardRuntime, details?: Record<string, unknown>): void {
  traces.push(traceLine(id, sequence, operation, dashboard.getSnapshot(), details));
}

function prepareTask(dashboard: DashboardRuntime, agent = "agent-alpha", task = "task-alpha"): void {
  dashboard.bindAgent(agent, 0);
  dashboard.assignTask(task, agent, "Prepare scene brief");
  dashboard.startTask(task);
}

const scenarios: ScenarioResult[] = [];

scenarios.push(runScenario("D1", (checks, traces) => {
  const { dashboard } = fixture([0, 1, 2]);
  record(traces, "D1", 0, "boot", dashboard);
  const snapshot = dashboard.getSnapshot();
  check(checks, "zero bindings", snapshot.bindings.length === 0, snapshot.bindings);
  check(checks, "zero tasks", snapshot.tasks.length === 0, snapshot.tasks);
  check(checks, "unbound roster", snapshot.unboundStaff.length === 3, snapshot.unboundStaff.map((staff) => staff.staffId));
}));

scenarios.push(runScenario("D2", (checks, traces) => {
  const { dashboard } = fixture([0, 1, 2]);
  const result = dashboard.bindAgent("agent-alpha", 1);
  record(traces, "D2", 0, "bind agent-alpha to Staff 1", dashboard, { code: result.code });
  check(checks, "explicit bind accepted", result.accepted, result);
  check(checks, "remaining unbound Staff visible", dashboard.getSnapshot().unboundStaff.length === 2, dashboard.getSnapshot().unboundStaff.map((staff) => staff.staffId));
}));

scenarios.push(runScenario("D3", (checks, traces) => {
  const { living, dashboard } = fixture();
  dashboard.bindAgent("agent-alpha", 0);
  const before = living.snapshot();
  const result = dashboard.assignTask("task-alpha", "agent-alpha", "Prepare brief");
  record(traces, "D3", 0, "assign task", dashboard, { code: result.code });
  check(checks, "task assigned", result.task?.status === "ASSIGNED", result.task);
  check(checks, "living unchanged", stableStringify(living.snapshot()) === stableStringify(before), { frame: living.frame });
}));

scenarios.push(runScenario("D4", (checks, traces) => {
  const { living, dashboard } = fixture();
  prepareTask(dashboard);
  const before = living.snapshot();
  const result = dashboard.getTasks()[0];
  record(traces, "D4", 0, "start task", dashboard, { status: result?.status, bridgeContextOwned: result?.bridgeContextOwned });
  check(checks, "task running", result?.status === "RUNNING", result);
  check(checks, "living unchanged", stableStringify(living.snapshot()) === stableStringify(before), { frame: living.frame });
}));

scenarios.push(runScenario("D5", (checks, traces) => {
  const { living, dashboard } = fixture();
  let publications = 0;
  const dispose = dashboard.subscribe(() => { publications += 1; });
  let ticks = 0;
  let observations = 0;
  const originalTick = living.tick.bind(living);
  const originalObserve = dashboard.assignmentAdapter.observeLiving.bind(dashboard.assignmentAdapter);
  (living as unknown as { tick: () => DashboardRuntimeSnapshot["living"] }).tick = () => { ticks += 1; return originalTick(); };
  (dashboard.assignmentAdapter as unknown as { observeLiving: (snapshot: DashboardRuntimeSnapshot["living"]) => unknown }).observeLiving = (snapshot) => { observations += 1; return originalObserve(snapshot); };
  dashboard.step(10);
  record(traces, "D5", 0, "scheduler step x10", dashboard, { ticks, observations, publications });
  check(checks, "ten living frames", living.frame === 10, living.frame);
  check(checks, "ten living ticks", ticks === 10, ticks);
  check(checks, "ten living observations", observations === 10, observations);
  check(checks, "ten publications", publications === 10, publications);
  dispose();
}));

scenarios.push(runScenario("D6", (checks, traces) => {
  const { living, dashboard } = fixture([0], true);
  prepareTask(dashboard);
  living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
  living.gotoEquip(0);
  dashboard.step(1);
  record(traces, "D6", 0, "autonomous equipment transition", dashboard);
  check(checks, "task remains running", dashboard.getDashboardReadModel().agents[0]?.task.status === "RUNNING", dashboard.getDashboardReadModel().agents[0]?.task.status);
  check(checks, "interruption observed", dashboard.getEvents().some((event) => event.type === "living_interruption_observed"), dashboard.getEvents().map((event) => event.type));
}));

scenarios.push(runScenario("D7", (checks, traces) => {
  const { living, dashboard } = fixture();
  prepareTask(dashboard);
  const before = living.snapshot();
  const result = dashboard.updateTaskProgress("task-alpha", 42);
  record(traces, "D7", 0, "progress 42", dashboard, { code: result.code });
  check(checks, "progress accepted", result.task?.externalProgress === 42, result.task);
  check(checks, "living unchanged", stableStringify(living.snapshot()) === stableStringify(before), { frame: living.frame });
}));

scenarios.push(runScenario("D8", (checks, traces) => {
  const { living, dashboard } = fixture();
  prepareTask(dashboard);
  const result = dashboard.completeTask("task-alpha");
  record(traces, "D8", 0, "complete task", dashboard, { code: result.code });
  dashboard.step(1);
  record(traces, "D8", 1, "scheduler continues after completion", dashboard);
  check(checks, "task completed", dashboard.getTasks()[0]?.status === "COMPLETED", dashboard.getTasks()[0]);
  check(checks, "living continued", living.frame === 1, living.frame);
}));

scenarios.push(runScenario("D9", (checks, traces) => {
  const { dashboard } = fixture();
  prepareTask(dashboard);
  const result = dashboard.failTask("task-alpha", "execution_error");
  record(traces, "D9", 0, "fail task", dashboard, { code: result.code });
  check(checks, "task failed", result.task?.status === "FAILED", result.task);
}));

scenarios.push(runScenario("D10", (checks, traces) => {
  const { dashboard } = fixture();
  dashboard.bindAgent("agent-alpha", 0);
  dashboard.assignTask("task-alpha", "agent-alpha");
  const result = dashboard.cancelTask("task-alpha", "operator_cancelled");
  record(traces, "D10", 0, "cancel task", dashboard, { code: result.code });
  check(checks, "task cancelled", result.task?.status === "CANCELLED", result.task);
}));

scenarios.push(runScenario("D11", (checks, traces) => {
  const { dashboard } = fixture([0, 1]);
  dashboard.bindAgent("agent-alpha", 0);
  dashboard.bindAgent("agent-beta", 1);
  dashboard.assignTask("task-alpha", "agent-alpha");
  dashboard.assignTask("task-beta", "agent-beta");
  dashboard.startTask("task-alpha");
  dashboard.updateTaskProgress("task-beta", 42);
  record(traces, "D11", 0, "two-agent isolation", dashboard);
  check(checks, "two bindings", dashboard.getBindings().length === 2, dashboard.getBindings());
  check(checks, "two tasks isolated", dashboard.getTasks().length === 2 && dashboard.getTasks().every((task) => task.staffId !== undefined), dashboard.getTasks());
  check(checks, "task state isolated", dashboard.getDashboardReadModel().agents.find((agent) => agent.externalAgentId === "agent-alpha")?.task.status === "RUNNING" && dashboard.getDashboardReadModel().agents.find((agent) => agent.externalAgentId === "agent-beta")?.task.externalProgress === 42, dashboard.getDashboardReadModel().agents);
}));

scenarios.push(runScenario("D12", (checks, traces) => {
  const { dashboard } = fixture([0, 1]);
  const missing = dashboard.assignTask("task-missing", "agent-missing");
  dashboard.bindAgent("agent-alpha", 0);
  const duplicateBinding = dashboard.bindAgent("agent-beta", 0);
  dashboard.assignTask("task-alpha", "agent-alpha");
  const activeConflict = dashboard.assignTask("task-alpha-2", "agent-alpha");
  const unbindConflict = dashboard.unbindAgent("agent-alpha");
  const start = dashboard.startTask("task-alpha");
  const invalidTransition = dashboard.startTask("task-alpha");
  record(traces, "D12", 0, "conflict and error commands", dashboard, { missing: missing.code, duplicateBinding: duplicateBinding.code, activeConflict: activeConflict.code, unbindConflict: unbindConflict.code, start: start.code, invalidTransition: invalidTransition.code });
  check(checks, "unbound rejection", missing.code === "AGENT_NOT_BOUND", missing.code);
  check(checks, "binding conflict", duplicateBinding.code === "AGENT_BINDING_CONFLICT", duplicateBinding.code);
  check(checks, "active task conflict", activeConflict.code === "ACTIVE_TASK_CONFLICT", activeConflict.code);
  check(checks, "active unbind conflict", unbindConflict.code === "ACTIVE_TASK_PREVENTS_UNBIND", unbindConflict.code);
  check(checks, "invalid transition", invalidTransition.code === "INVALID_TASK_TRANSITION", invalidTransition.code);
}));

scenarios.push(runScenario("D13", (checks, traces) => {
  const first = fixture();
  first.dashboard.bindAgent("agent-alpha", 0);
  first.dashboard.assignTask("task-alpha", "agent-alpha");
  record(traces, "D13", 0, "ephemeral session before reset", first.dashboard);
  const second = fixture();
  record(traces, "D13", 1, "fresh runtime reset", second.dashboard);
  check(checks, "fresh bindings empty", second.dashboard.getBindings().length === 0, second.dashboard.getBindings());
  check(checks, "fresh tasks empty", second.dashboard.getTasks().length === 0, second.dashboard.getTasks());
}));

scenarios.push(runScenario("D14", (checks, traces) => {
  const build = () => {
    const { dashboard } = fixture([0, 1]);
    dashboard.bindAgent("agent-alpha", 0, "bind-alpha");
    dashboard.bindAgent("agent-beta", 1, "bind-beta");
    dashboard.assignTask("task-alpha", "agent-alpha", "A", "assign-alpha");
    dashboard.startTask("task-alpha", "start-alpha");
    dashboard.updateTaskProgress("task-alpha", 42, "progress-alpha");
    dashboard.step(10);
    dashboard.completeTask("task-alpha", "done", "complete-alpha");
    return dashboard;
  };
  const left = build();
  const right = build();
  record(traces, "D14", 0, "deterministic replay", left, { leftDigest: left.replayDigest(), rightDigest: right.replayDigest() });
  check(checks, "replay digest stable", left.replayDigest() === right.replayDigest(), { left: left.replayDigest(), right: right.replayDigest() });
  check(checks, "snapshot stable", stableStringify(left.getSnapshot()) === stableStringify(right.getSnapshot()), true);
}));

const failed = scenarios.filter((scenario) => scenario.status === "FAIL");
writeFileSync(resolve(evidenceDirectory, "scenario-results.json"), JSON.stringify({ schema: "i2-dashboard-scenario-results-v1", status: failed.length === 0 ? "PASS" : "FAIL", scenarios }, null, 2) + "\n", "utf8");

const replay = (() => {
  const build = () => {
    const { dashboard } = fixture([0, 1]);
    dashboard.bindAgent("agent-alpha", 0, "bind-alpha");
    dashboard.bindAgent("agent-beta", 1, "bind-beta");
    dashboard.assignTask("task-alpha", "agent-alpha", "A", "assign-alpha");
    dashboard.startTask("task-alpha", "start-alpha");
    dashboard.updateTaskProgress("task-alpha", 42, "progress-alpha");
    dashboard.step(10);
    dashboard.completeTask("task-alpha", "done", "complete-alpha");
    return dashboard;
  };
  const left = build();
  const right = build();
  return {
    schema: "i2-dashboard-deterministic-replay-v1",
    status: left.replayDigest() === right.replayDigest() && stableStringify(left.getSnapshot()) === stableStringify(right.getSnapshot()) ? "PASS" : "FAIL",
    left_digest: left.replayDigest(),
    right_digest: right.replayDigest(),
    wall_clock_fields: [],
  };
})();
writeFileSync(resolve(evidenceDirectory, "deterministic-replay.json"), JSON.stringify(replay, null, 2) + "\n", "utf8");

if (failed.length > 0) {
  process.exitCode = 1;
}
