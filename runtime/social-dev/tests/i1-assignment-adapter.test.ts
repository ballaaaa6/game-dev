import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { MoveMode, StaffFlag, StaffState } from "../src/core/living/constants";
import { createLivingRuntime } from "../src/core/living/runtime";
import { createAssignmentAdapter } from "../src/product/assignment";
import { stableStringify } from "../src/product/assignment/snapshot";

const catalogs = loadRuntimeCatalogs();

function fixture(staffDataIds: readonly number[] = [0]) {
  return createAssignmentAdapter(createLivingRuntime(catalogs, { initialStaffDataIds: staffDataIds, scenarioEquipment: true, appDataReplay: [0, 0, 0, 0, 0, 0], libReplay: [0, 0, 0] }));
}

function observedTicks(adapter: ReturnType<typeof fixture>, count: number): void {
  for (let index = 0; index < count; index += 1) {
    adapter.living.tick();
    adapter.observeLiving();
  }
}

describe("I1 product task overlay with baseline living", () => {
  it("keeps no-task, assignment, and running separate from STATE_WORK", () => {
    const adapter = fixture();
    expect(adapter.bindAgent("agent-a", 0).accepted).toBe(true);
    adapter.living.runTicks(20);
    expect(adapter.readModel().agents[0]?.task.status).toBe("IDLE_NO_TASK");
    const livingBefore = adapter.living.snapshot();
    expect(adapter.assignTask("task-a", "agent-a", "Fix login").task?.status).toBe("ASSIGNED");
    expect(adapter.living.snapshot().staffs[0]).toEqual(livingBefore.staffs[0]);
    expect(adapter.startTask("task-a").task?.status).toBe("RUNNING");
    expect(adapter.living.snapshot().staffs[0]).toEqual(livingBefore.staffs[0]);
    expect(adapter.readModel().agents[0]?.task.status).toBe("RUNNING");
    expect(adapter.readModel().agents[0]?.living.stateName).toBe("STATE_WORK");
  });

  it("preserves product identity across equipment, talk, home, and desk observations", () => {
    const adapter = fixture([0, 1]);
    adapter.bindAgent("agent-a", 0);
    adapter.bindAgent("agent-b", 1);
    adapter.assignTask("task-a", "agent-a");
    adapter.startTask("task-a");
    adapter.living.configureStaff(0, { state: StaffState.USE_EQUIPMENT, moveMode: MoveMode.STAY, equipmentId: 18 });
    adapter.observeLiving();
    adapter.living.configureStaff(0, { state: StaffState.TALK, moveMode: MoveMode.STAY, equipmentId: -1, colleagueId: 1 });
    adapter.observeLiving();
    adapter.living.configureStaff(0, { state: StaffState.STAY_HOME, moveMode: MoveMode.STAY, colleagueId: -1, hp: 20 });
    adapter.observeLiving();
    adapter.living.configureStaff(0, { state: StaffState.WORK, moveMode: MoveMode.STAY, flags: StaffFlag.SITTING, deskId: 0, hp: 50 });
    adapter.observeLiving();
    expect(adapter.readModel().agents[0]?.task).toMatchObject({ externalTaskId: "task-a", status: "RUNNING" });
    expect(adapter.events().filter((event) => event.type === "living_interruption_observed").length).toBeGreaterThanOrEqual(1);
  });

  it("enforces one active task, one agent per Staff, and explicit terminal cleanup", () => {
    const adapter = fixture([0, 1]);
    expect(adapter.bindAgent("agent-a", 0).accepted).toBe(true);
    expect(adapter.bindAgent("agent-b", 0).code).toBe("AGENT_BINDING_CONFLICT");
    expect(adapter.bindAgent("agent-b", 1).accepted).toBe(true);
    expect(adapter.assignTask("task-a", "agent-a").accepted).toBe(true);
    expect(adapter.assignTask("task-b", "agent-a").code).toBe("ACTIVE_TASK_CONFLICT");
    expect(adapter.unbindAgent("agent-a").code).toBe("ACTIVE_TASK_PREVENTS_UNBIND");
    expect(adapter.completeTask("task-a").task?.status).toBe("COMPLETED");
    expect(adapter.assignTask("task-a2", "agent-a").accepted).toBe(true);
    expect(adapter.startTask("task-a2").accepted).toBe(true);
    expect(adapter.completeTask("task-a2").task?.status).toBe("COMPLETED");
    expect(adapter.unbindAgent("agent-a").accepted).toBe(true);
    expect(adapter.events().filter((event) => event.type === "task_started")).toHaveLength(1);
  });

  it("isolates two agents and produces byte-stable replay state", () => {
    const build = () => {
      const adapter = fixture([0, 1]);
      adapter.bindAgent("agent-a", 0);
      adapter.bindAgent("agent-b", 1);
      adapter.assignTask("task-a", "agent-a", "A");
      adapter.assignTask("task-b", "agent-b", "B");
      adapter.startTask("task-a");
      adapter.updateTaskProgress("task-a", 25);
      adapter.cancelTask("task-a");
      return { adapter: adapter.snapshot(), dashboard: adapter.readModel(), digest: adapter.replayDigest() };
    };
    expect(build()).toEqual(build());
  });

  it("closes deterministic acceptance scenarios A1 through A12", () => {
    const a1 = fixture();
    a1.bindAgent("agent-a", 0);
    observedTicks(a1, 20);
    expect(a1.readModel().agents[0]?.task.status).toBe("IDLE_NO_TASK");

    const a2 = fixture();
    a2.bindAgent("agent-a", 0);
    const beforeA2 = a2.living.snapshot();
    expect(a2.assignTask("task-a", "agent-a").task?.status).toBe("ASSIGNED");
    expect(a2.living.snapshot().staffs[0]).toEqual(beforeA2.staffs[0]);

    const a3 = fixture();
    a3.bindAgent("agent-a", 0);
    a3.assignTask("task-a", "agent-a");
    expect(a3.startTask("task-a").task?.status).toBe("RUNNING");
    expect(a3.events().filter((event) => event.type === "task_started")).toHaveLength(1);

    const a4 = fixture();
    a4.bindAgent("agent-a", 0);
    a4.assignTask("task-a", "agent-a");
    a4.startTask("task-a");
    a4.living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
    expect(a4.living.gotoEquip(0)).toBe(true);
    observedTicks(a4, 80);
    expect(a4.readModel().agents[0]?.task.status).toBe("RUNNING");

    const a5 = createAssignmentAdapter(createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], appDataReplay: [1], libReplay: [0] }));
    a5.bindAgent("agent-a", 0);
    a5.assignTask("task-a", "agent-a");
    a5.startTask("task-a");
    a5.living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    a5.living.configureStaff(1, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    expect(a5.living.gotoTalk(0)).toBe(true);
    observedTicks(a5, 220);
    expect(a5.readModel().agents[0]?.task.status).toBe("RUNNING");

    const a6 = fixture();
    a6.bindAgent("agent-a", 0);
    a6.assignTask("task-a", "agent-a");
    a6.startTask("task-a");
    a6.living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 5 });
    observedTicks(a6, 260);
    expect(a6.readModel().agents[0]?.task.status).toBe("RUNNING");

    const a7 = fixture();
    a7.bindAgent("agent-a", 0);
    a7.assignTask("task-a", "agent-a");
    a7.startTask("task-a");
    const beforeA7 = a7.living.snapshot().staffs[0]!;
    expect(a7.completeTask("task-a").task?.status).toBe("COMPLETED");
    expect(a7.living.snapshot().staffs[0]).toEqual(beforeA7);

    const a8 = fixture();
    a8.bindAgent("agent-a", 0);
    a8.assignTask("task-a", "agent-a");
    expect(a8.cancelTask("task-a").task?.status).toBe("CANCELLED");

    const a9 = fixture();
    a9.bindAgent("agent-a", 0);
    a9.assignTask("task-a", "agent-a");
    a9.startTask("task-a");
    const beforeA9 = a9.living.snapshot().staffs[0]!;
    expect(a9.failTask("task-a", "backend_error").task?.status).toBe("FAILED");
    expect(a9.living.snapshot().staffs[0]?.hp).toBe(beforeA9.hp);

    const a10 = fixture([0, 1]);
    a10.bindAgent("agent-a", 0);
    a10.bindAgent("agent-b", 1);
    expect(a10.assignTask("task-a", "agent-a").accepted).toBe(true);
    expect(a10.assignTask("task-b", "agent-b").accepted).toBe(true);
    expect(a10.startTask("task-a").task?.staffId).toBe(0);
    expect(a10.startTask("task-b").task?.staffId).toBe(1);
    expect(a10.snapshot().tasks.map((task) => task.staffId)).toEqual([0, 1]);

    const a11 = fixture();
    a11.bindAgent("agent-a", 0);
    a11.assignTask("task-a", "agent-a");
    expect(a11.assignTask("task-b", "agent-a").code).toBe("ACTIVE_TASK_CONFLICT");
    expect(a11.snapshot().tasks).toHaveLength(1);

    const buildA12 = () => {
      const adapter = fixture([0, 1]);
      adapter.bindAgent("agent-a", 0, "bind-a");
      adapter.bindAgent("agent-b", 1, "bind-b");
      adapter.assignTask("task-a", "agent-a", "A", "assign-a");
      adapter.startTask("task-a", "start-a");
      adapter.updateTaskProgress("task-a", 25, "progress-a");
      adapter.living.tick();
      adapter.observeLiving();
      return { adapter: adapter.snapshot(), dashboard: adapter.readModel(), living: adapter.living.snapshot(), digest: adapter.replayDigest() };
    };
    const replayA12 = buildA12();
    expect(stableStringify(replayA12)).toBe(stableStringify(buildA12()));
  });
});
