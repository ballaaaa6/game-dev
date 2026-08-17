import { loadRuntimeCatalogs, type RuntimeCatalogs } from "../../catalog/load-contracts";
import { stableStringify } from "../digest";
import { StaffFlag, StaffState } from "./constants";
import { createLivingRuntime, type LivingRuntime } from "./runtime";
import { i0Catalog, type I0RuntimeCatalog } from "./catalog";
import type { LivingSnapshot } from "./types";

export type I0ScenarioFixture = I0RuntimeCatalog["scenario_fixtures"][number];

export interface ScenarioAssertion {
  readonly name: string;
  readonly status: "PASS" | "FAIL";
  readonly detail: string;
}

export interface ScenarioResult {
  readonly id: string;
  readonly name: string;
  readonly status: "PASS" | "FAIL";
  readonly fixture: I0ScenarioFixture;
  readonly initial: LivingSnapshot;
  readonly final: LivingSnapshot;
  readonly replayFinal?: LivingSnapshot;
  readonly assertions: readonly ScenarioAssertion[];
}

function runUntil(runtime: LivingRuntime, predicate: () => boolean, limit = 600): void {
  for (let index = 0; index < limit && !predicate(); index += 1) runtime.tick();
}

function assertion(name: string, condition: boolean, detail: string): ScenarioAssertion {
  return { name, status: condition ? "PASS" : "FAIL", detail };
}

function staff(runtime: LivingRuntime, id: number) {
  const found = runtime.staffs.find((candidate) => candidate.id === id);
  if (!found) throw new Error(`Scenario runtime is missing Staff:${id}`);
  return found;
}

function scenarioS1(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
  runUntil(runtime, () => staff(runtime, 0).state === StaffState.WORK && (staff(runtime, 0).flags & StaffFlag.SITTING) !== 0, 120);
  const current = staff(runtime, 0);
  return {
    runtime,
    assertions: [
      assertion("desk-owner", runtime.room.furniture.find((item) => item.instanceId === current.deskId)?.ownerStaffId === 0, "Staff:0 owns the first raw-order installed desk"),
      assertion("work-entry", current.state === StaffState.WORK && (current.flags & StaffFlag.SITTING) !== 0, "Staff reaches STATE_WORK with FLAG_SITTING"),
      assertion("arrival-modes", runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-3") && runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-6"), "GOTO_DESK and SIT_DOWN arrival dispatches are present"),
      assertion("ordinary-work-hp", current.hp === 100, "ordinary work does not drain HP"),
    ],
  };
}

function scenarioS2(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0], scenarioEquipment: true, appDataReplay: [0, 0] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
  const selected = runtime.gotoEquip(0);
  const equipment = runtime.room.furniture.find((item) => item.furnitureDataId === 18);
  runUntil(runtime, () => {
    const current = staff(runtime, 0);
    return current.state === StaffState.WORK && current.equipmentId === -1 && (equipment?.reservedUserIds.length ?? 1) === 0;
  }, 300);
  const current = staff(runtime, 0);
  return {
    runtime,
    assertions: [
      assertion("selected", selected && equipment?.rawType === 1, "AppData.Random(2)=0 selects type 1 FurnitureData:18"),
      assertion("released", (equipment?.reservedUserIds.length ?? 1) === 0, "OnUseComplate releases reservedUserIds"),
      assertion("recovery-stock", current.recoveryStock <= 10, "completion supplies recovery stock without immediate HP write"),
      assertion("return-work", current.state === StaffState.WORK, "equipment loop returns through GotoDesk to work"),
    ],
  };
}

function scenarioS3(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], appDataReplay: [1], libReplay: [0] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
  runtime.configureStaff(1, { state: StaffState.WORK, flags: StaffFlag.SITTING });
  const selected = runtime.gotoTalk(0);
  runUntil(runtime, () => staff(runtime, 0).colleagueId === -1 && staff(runtime, 1).colleagueId === -1, 500);
  const first = staff(runtime, 0);
  const second = staff(runtime, 1);
  return {
    runtime,
    assertions: [
      assertion("candidate", selected, "Staff:1 is selected by the injected AppData candidate draw"),
      assertion("bilateral-relation", runtime.traces.some((trace) => trace.event === "talk-reserved-bilateral") && runtime.traces.some((trace) => trace.event === "on-invited-talk"), "reserved and invited talk relation is bilateral"),
      assertion("mode-chain", runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-7") && runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-9") && runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-8"), "TO_STAFF -> TO_BACK_OF_CHAIR -> TO_STAND_TALKING is observed"),
      assertion("cleanup", first.colleagueId === -1 && second.colleagueId === -1 && (first.flags & (StaffFlag.RESERVED_TALK | StaffFlag.INVITED)) === 0, "talk flags and colleague IDs are cleared"),
      assertion("hp-unchanged", first.hp === 100 && second.hp === 100, "talk does not change HP"),
    ],
  };
}

function scenarioS4(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 5 });
  runUntil(runtime, () => {
    const current = staff(runtime, 0);
    return current.hp * 100 >= current.maxHp * 40 && current.state === StaffState.WORK;
  }, 800);
  const current = staff(runtime, 0);
  return {
    runtime,
    assertions: [
      assertion("derived-max-hp", current.maxHp === 108, "Staff:0/Job:4 neutral formula yields maxHp 108"),
      assertion("low-hp-route", runtime.traces.some((trace) => trace.event === "low-hp-go-to-door") && runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-10"), "low HP enters the GO_TO_DOOR/GO_HOME path"),
      assertion("home-recovery", runtime.traces.some((trace) => trace.event === "stay-home-recover"), "UpdateStayHome calls RecoverHp(1)"),
      assertion("return", current.hp * 100 >= current.maxHp * 40 && current.deskId === 0, "return threshold reacquires the valid desk path"),
    ],
  };
}

function scenarioS5(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1] });
  const first = staff(runtime, 0);
  const second = staff(runtime, 1);
  return {
    runtime,
    assertions: [
      assertion("raw-order-first", first.deskId === 0, "first AddStaff receives raw-order desk 0"),
      assertion("raw-order-second", second.deskId === 1, "second AddStaff receives raw-order desk 1"),
      assertion("no-fairness-queue", !runtime.traces.some((trace) => trace.event.includes("fairness")), "no fairness queue or rotation is created"),
    ],
  };
}

function scenarioS6(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 0, 0, 0] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
  runtime.configureStaff(1, { state: StaffState.WORK, flags: StaffFlag.SITTING });
  const first = runtime.gotoEquip(0);
  const second = runtime.gotoEquip(1);
  const equipment = runtime.room.furniture.find((item) => item.furnitureDataId === 18);
  return {
    runtime,
    assertions: [
      assertion("first-reserve", first && equipment?.reservedUserIds.join(",") === "0", "first sequential GotoEquip reserves the target"),
      assertion("second-reject", second === false && equipment?.reservedUserIds.length === 1, "second sequential GotoEquip is rejected by reserved count"),
      assertion("active-owner-separate", equipment?.activeUserIds.length === 0 && equipment.ownerStaffId === -1, "active users and owner do not override reserved contention"),
    ],
  };
}

function scenarioS7(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
  const removed = runtime.removeFurniture(0);
  const current = staff(runtime, 0);
  return {
    runtime,
    assertions: [
      assertion("removed", removed, "desk ObjChip is removed"),
      assertion("owner-cleared", runtime.room.furniture.find((item) => item.instanceId === 0)?.ownerStaffId === -1, "removed desk owner is cleared"),
      assertion("staff-cleared", current.deskId !== 0 && current.flags % 4 < 2, "Staff has no stale desk dependency or sitting bit"),
      assertion("fallback", current.state === StaffState.MOVE || current.state === StaffState.WANDER, "fallback uses current GotoDesk/Wander policy"),
    ],
  };
}

function scenarioS8(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1] });
  runtime.startPlanning();
  return {
    runtime,
    assertions: [
      assertion("player", runtime.player.planning, "Player.StartPlanning is active"),
      assertion("room-staff-chain", runtime.staffs.every((candidate) => (candidate.flags & StaffFlag.PLANNING) !== 0), "Room and every Staff receive planning state"),
      assertion("work-boundary", runtime.traces.some((trace) => trace.event === "planning-start-room") && runtime.traces.some((trace) => trace.event === "planning-start-staff"), "planning boundary is trace-visible"),
    ],
  };
}

function scenarioS9(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[] } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1] });
  runtime.startPlanning();
  runtime.endPlanning(true);
  return {
    runtime,
    assertions: [
      assertion("completion-predicate", runtime.player.completed && !runtime.player.planning, "Player completion predicate clears planning"),
      assertion("staff-end-chain", runtime.staffs.every((candidate) => (candidate.flags & StaffFlag.PLANNING) === 0), "Room.OnEndPlanning clears Staff planning flags"),
      assertion("work-resume-boundary", runtime.traces.some((trace) => trace.event === "planning-end-staff"), "end chain is trace-visible without a product task queue"),
    ],
  };
}

function replaySnapshot(catalogs: RuntimeCatalogs): LivingSnapshot {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 1, 40, 20, 10, 25, 0, 4] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
  runtime.runTicks(100);
  return runtime.snapshot();
}

function scenarioS10(catalogs: RuntimeCatalogs): { runtime: LivingRuntime; assertions: ScenarioAssertion[]; replayFinal: LivingSnapshot } {
  const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 1, 40, 20, 10, 25, 0, 4] });
  runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
  runtime.runTicks(100);
  const replayFinal = replaySnapshot(catalogs);
  return {
    runtime,
    replayFinal,
    assertions: [
      assertion("byte-identical-log", stableStringify(runtime.snapshot()) === stableStringify(replayFinal), "same canonical state and replay stream produce identical output"),
      assertion("same-draw-log", stableStringify(runtime.snapshot().rngDraws) === stableStringify(replayFinal.rngDraws), "same RNG draw order is preserved"),
    ],
  };
}

const SCENARIO_RUNNERS: Readonly<Record<string, (catalogs: RuntimeCatalogs) => { runtime: LivingRuntime; assertions: ScenarioAssertion[]; replayFinal?: LivingSnapshot }>> = {
  S1: scenarioS1,
  S2: scenarioS2,
  S3: scenarioS3,
  S4: scenarioS4,
  S5: scenarioS5,
  S6: scenarioS6,
  S7: scenarioS7,
  S8: scenarioS8,
  S9: scenarioS9,
  S10: scenarioS10,
};

export function runI0ScenarioSuite(catalogs: RuntimeCatalogs = loadRuntimeCatalogs()): readonly ScenarioResult[] {
  return i0Catalog(catalogs).scenario_fixtures.map((fixture) => {
    const runner = SCENARIO_RUNNERS[fixture.id];
    if (!runner) throw new Error(`No I0 runner exists for ${fixture.id}`);
    const execution = runner(catalogs);
    const assertions = execution.assertions;
    return {
      id: fixture.id,
      name: fixture.name,
      status: assertions.every((check) => check.status === "PASS") ? "PASS" : "FAIL",
      fixture,
      initial: execution.runtime.initialSnapshot(),
      final: execution.runtime.snapshot(),
      ...(execution.replayFinal ? { replayFinal: execution.replayFinal } : {}),
      assertions,
    };
  });
}
