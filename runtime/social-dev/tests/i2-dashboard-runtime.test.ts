import { describe, expect, it, vi } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { StaffFlag, StaffState } from "../src/core/living/constants";
import { createLivingRuntime } from "../src/core/living/runtime";
import { createDashboardRuntime } from "../src/product/dashboard";
import { stableStringify } from "../src/product/assignment/snapshot";

const catalogs = loadRuntimeCatalogs();

function fixture(staffDataIds: readonly number[] = [0], scenarioEquipment = false) {
  const living = createLivingRuntime(catalogs, {
    initialStaffDataIds: staffDataIds,
    scenarioEquipment,
    appDataReplay: [0, 0, 0, 0, 0, 0],
    libReplay: [0, 0, 0, 0],
  });
  return { living, dashboard: createDashboardRuntime(living) };
}

describe("I2 DashboardRuntime and in-process control surface", () => {
  it("D1 boots with source-backed Staff, no bindings, no tasks, and an unbound roster", () => {
    const { dashboard } = fixture([0, 1, 2]);
    const snapshot = dashboard.getSnapshot();
    expect(snapshot.frame).toBe(0);
    expect(snapshot.bindings).toEqual([]);
    expect(snapshot.tasks).toEqual([]);
    expect(snapshot.events).toEqual([]);
    expect(snapshot.unboundStaff.map((staff) => staff.staffId)).toEqual([0, 1, 2]);
    expect(snapshot.unboundStaff.every((staff) => staff.source === "I0_RUNTIME_CATALOG")).toBe(true);
  });

  it("D2 binds only through an explicit externalAgentId and staffId pair", () => {
    const { dashboard } = fixture([0, 1, 2]);
    const result = dashboard.bindAgent("agent-alpha", 1);
    expect(result).toMatchObject({ accepted: true, code: "OK", agent: { externalAgentId: "agent-alpha", staffId: 1 } });
    expect(dashboard.getSnapshot().bindings).toEqual([{ externalAgentId: "agent-alpha", staffId: 1, boundSequence: 1 }]);
    expect(dashboard.getSnapshot().unboundStaff.map((staff) => staff.staffId)).toEqual([0, 2]);
  });

  it("D3 assigns a product task without ticking or mutating living state", () => {
    const { living, dashboard } = fixture();
    dashboard.bindAgent("agent-alpha", 0);
    const before = living.snapshot();
    const tick = vi.spyOn(living, "tick");
    const result = dashboard.assignTask("task-alpha", "agent-alpha", "Prepare brief");
    expect(result.task?.status).toBe("ASSIGNED");
    expect(tick).not.toHaveBeenCalled();
    expect(living.snapshot()).toEqual(before);
    expect(dashboard.getSnapshot().frame).toBe(0);
  });

  it("D4 starts product RUNNING state without claiming original living context", () => {
    const { living, dashboard } = fixture();
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.assignTask("task-alpha", "agent-alpha");
    const before = living.snapshot();
    const result = dashboard.startTask("task-alpha");
    expect(result).toMatchObject({ accepted: true, task: { status: "RUNNING", bridgeContextOwned: false } });
    expect(living.snapshot()).toEqual(before);
    expect(dashboard.getDashboardReadModel().agents[0]?.task.status).toBe("RUNNING");
  });

  it("D5 performs exactly one living tick, one observe, and one publication per scheduler step", () => {
    const { living, dashboard } = fixture();
    const tick = vi.spyOn(living, "tick");
    const observe = vi.spyOn(dashboard.assignmentAdapter, "observeLiving");
    let publications = 0;
    const dispose = dashboard.subscribe(() => { publications += 1; });
    dashboard.step(10);
    expect(living.frame).toBe(10);
    expect(tick).toHaveBeenCalledTimes(10);
    expect(observe).toHaveBeenCalledTimes(10);
    expect(publications).toBe(10);
    expect(dashboard.getSnapshot().living.frame).toBe(10);
    dispose();
  });

  it("D6 observes an autonomous living transition while the product task remains RUNNING", () => {
    const { living, dashboard } = fixture([0], true);
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.assignTask("task-alpha", "agent-alpha");
    dashboard.startTask("task-alpha");
    living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
    expect(living.gotoEquip(0)).toBe(true);
    dashboard.step(1);
    expect(dashboard.getDashboardReadModel().agents[0]?.task.status).toBe("RUNNING");
    expect(dashboard.getEvents().some((event) => event.type === "living_interruption_observed")).toBe(true);
    expect(dashboard.getDashboardReadModel().agents[0]?.living.livingFrame).toBe(1);
  });

  it("D7 updates Task progress only and keeps the living snapshot byte-identical", () => {
    const { living, dashboard } = fixture();
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.assignTask("task-alpha", "agent-alpha");
    dashboard.startTask("task-alpha");
    const before = living.snapshot();
    const result = dashboard.updateTaskProgress("task-alpha", 42);
    expect(result).toMatchObject({ accepted: true, task: { externalProgress: 42, status: "RUNNING" } });
    expect(living.snapshot()).toEqual(before);
    expect(dashboard.getSnapshot().dashboard.agents[0]?.living.livingFrame).toBe(0);
  });

  it("D8 completes a product task and keeps the scheduler moving baseline living", () => {
    const { living, dashboard } = fixture();
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.assignTask("task-alpha", "agent-alpha");
    dashboard.startTask("task-alpha");
    expect(dashboard.completeTask("task-alpha").task?.status).toBe("COMPLETED");
    expect(dashboard.getSnapshot().frame).toBe(0);
    dashboard.step(1);
    expect(living.frame).toBe(1);
    expect(dashboard.getDashboardReadModel().agents[0]?.task.status).toBe("COMPLETED");
  });

  it("D9 and D10 preserve terminal FAILED and CANCELLED history", () => {
    const failed = fixture();
    failed.dashboard.bindAgent("agent-alpha", 0);
    failed.dashboard.assignTask("task-failed", "agent-alpha");
    failed.dashboard.startTask("task-failed");
    expect(failed.dashboard.failTask("task-failed", "execution_error").task?.status).toBe("FAILED");
    expect(failed.dashboard.getTasks()[0]?.terminalReason).toBe("execution_error");

    const cancelled = fixture();
    cancelled.dashboard.bindAgent("agent-alpha", 0);
    cancelled.dashboard.assignTask("task-cancelled", "agent-alpha");
    expect(cancelled.dashboard.cancelTask("task-cancelled", "operator_cancelled").task?.status).toBe("CANCELLED");
    expect(cancelled.dashboard.getTasks()[0]?.terminalReason).toBe("operator_cancelled");
  });

  it("D11 isolates two agents and their product task histories", () => {
    const { dashboard } = fixture([0, 1]);
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.bindAgent("agent-beta", 1);
    dashboard.assignTask("task-alpha", "agent-alpha");
    dashboard.assignTask("task-beta", "agent-beta");
    dashboard.startTask("task-alpha");
    dashboard.updateTaskProgress("task-beta", 42);
    const agents = dashboard.getDashboardReadModel().agents;
    expect(agents.map((agent) => agent.externalAgentId)).toEqual(["agent-alpha", "agent-beta"]);
    expect(agents.find((agent) => agent.externalAgentId === "agent-alpha")?.task.status).toBe("RUNNING");
    expect(agents.find((agent) => agent.externalAgentId === "agent-beta")?.task.externalProgress).toBe(42);
  });

  it("D12 returns normal I1 conflict and invalid-transition codes through the typed facade", () => {
    const { dashboard } = fixture([0, 1]);
    expect(dashboard.assignTask("unbound-task", "agent-missing").code).toBe("AGENT_NOT_BOUND");
    expect(dashboard.bindAgent("agent-alpha", 0).accepted).toBe(true);
    expect(dashboard.bindAgent("agent-beta", 0).code).toBe("AGENT_BINDING_CONFLICT");
    expect(dashboard.assignTask("task-alpha", "agent-alpha").accepted).toBe(true);
    expect(dashboard.assignTask("task-alpha-2", "agent-alpha").code).toBe("ACTIVE_TASK_CONFLICT");
    expect(dashboard.unbindAgent("agent-alpha").code).toBe("ACTIVE_TASK_PREVENTS_UNBIND");
    expect(dashboard.startTask("task-alpha").accepted).toBe(true);
    expect(dashboard.startTask("task-alpha").code).toBe("INVALID_TASK_TRANSITION");
    expect(dashboard.getSnapshot().lastCommandResult).toMatchObject({ accepted: false, code: "INVALID_TASK_TRANSITION" });
  });

  it("D13 resets product state on a fresh runtime and exposes no persistence boundary", () => {
    const first = fixture();
    first.dashboard.bindAgent("agent-alpha", 0);
    first.dashboard.assignTask("task-alpha", "agent-alpha");
    expect(first.dashboard.getTasks()).toHaveLength(1);
    const second = fixture();
    expect(second.dashboard.getBindings()).toEqual([]);
    expect(second.dashboard.getTasks()).toEqual([]);
    expect(second.dashboard.getSnapshot().unboundStaff).toHaveLength(1);
  });

  it("D14 produces the same deterministic replay digest for the same command and tick sequence", () => {
    const build = () => {
      const { dashboard } = fixture([0, 1]);
      dashboard.bindAgent("agent-alpha", 0, "bind-alpha");
      dashboard.bindAgent("agent-beta", 1, "bind-beta");
      dashboard.assignTask("task-alpha", "agent-alpha", "A", "assign-alpha");
      dashboard.startTask("task-alpha", "start-alpha");
      dashboard.updateTaskProgress("task-alpha", 42, "progress-alpha");
      dashboard.step(10);
      dashboard.completeTask("task-alpha", "done", "complete-alpha");
      return { digest: dashboard.replayDigest(), snapshot: dashboard.getSnapshot() };
    };
    const left = build();
    const right = build();
    expect(left.digest).toBe(right.digest);
    expect(stableStringify(left.snapshot)).toBe(stableStringify(right.snapshot));
  });
});
