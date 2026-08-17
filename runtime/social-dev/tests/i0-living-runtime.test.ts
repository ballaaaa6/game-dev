import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { searchRoute } from "../src/core/living/astar";
import { i0Catalog } from "../src/core/living/catalog";
import { MoveMode, ObjChipType, StaffFlag, StaffState } from "../src/core/living/constants";
import { createLivingRuntime } from "../src/core/living/runtime";
import { runI0ScenarioSuite } from "../src/core/living/scenario-runner";
import { applyBasicArrival, mutableStaff } from "../src/core/living/movement";
import { stableStringify } from "../src/core/digest";

const catalogs = loadRuntimeCatalogs();

describe("I0 original living core", () => {
  it("loads the canonical data boundary and exact numeric vocabulary", () => {
    expect(i0Catalog(catalogs).counts).toMatchObject({ StaffData: 141, JobData: 30, SkillData: 36, FurnitureData: 103, RoomData: 18 });
    expect(Object.values(StaffState)).toEqual(Array.from({ length: 14 }, (_, index) => index));
    expect(Object.values(MoveMode)).toEqual(Array.from({ length: 12 }, (_, index) => index));
    expect(StaffFlag.SITTING).toBe(2);
    expect(StaffFlag.RESERVED_TALK).toBe(4);
    expect(StaffFlag.INVITED).toBe(8);
    expect(StaffFlag.TYPING).toBe(16);
    expect(StaffFlag.SLEEPING).toBe(32);
    expect(StaffFlag.PLANNING).toBe(64);
    expect(StaffFlag.PLANNING_COMPLETED).toBe(512);
    expect(ObjChipType.DOOR).toBe(5);
    expect(ObjChipType.OUTDOOR).toBe(6);
  });

  it("uses the source-backed four-neighbor route and target filters", () => {
    const route = searchRoute(catalogs, [8, 4], [6, 4], { goal: { cell: [6, 4], allowOccupiedTarget: true } });
    expect(route).toEqual([[8, 4], [7, 4], [6, 4]]);
    expect(() => searchRoute(catalogs, [8, 4], [0, 0])).toThrow(/goal is rejected/);
    expect(() => searchRoute(catalogs, [8, 4], [6, 4], { goal: { cell: [6, 4], allowOccupiedTarget: false } })).toThrow(/goal is rejected/);
  });

  it("represents every explicit OnArriveGoal mode without collapsing arrival to a boolean", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
    const staff = runtime.staffs[0]!;
    const mutable = mutableStaff(staff);
    for (let mode = 1; mode <= 11; mode += 1) {
      mutable.state = StaffState.MOVE;
      mutable.moveMode = mode as typeof mutable.moveMode;
      mutable.route = [];
      applyBasicArrival(staff, mode);
      expect([StaffState.WORK, StaffState.USE_EQUIPMENT, StaffState.TALK, StaffState.STAY_HOME, StaffState.INVITE_TO_TALK, StaffState.WANDER, StaffState.MOVE]).toContain(staff.state);
    }
  });

  it("runs S1 through generic normal startup, raw-order desk ownership, sit, and work", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
    const initial = runtime.staffs[0]!;
    expect(initial.jobId).toBe(4);
    expect(initial.skillId).toBe(1);
    expect(initial.maxHp).toBe(108);
    expect(initial.deskId).toBe(0);
    runtime.runTicks(20);
    const staff = runtime.staffs[0]!;
    expect(staff.state).toBe(StaffState.WORK);
    expect(staff.moveMode).toBe(MoveMode.STAY);
    expect(staff.flags & StaffFlag.SITTING).toBe(StaffFlag.SITTING);
    expect(runtime.room.furniture.find((item) => item.instanceId === 0)?.ownerStaffId).toBe(0);
    expect(runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-3")).toBe(true);
    expect(runtime.traces.some((trace) => trace.event === "on-arrive-goal-mode-6")).toBe(true);
    const pair = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1, 2] });
    expect(pair.staffs.map((candidate) => candidate.maxHp)).toEqual([108, 108, 108]);
  });

  it("reserves and releases the canonical recovery equipment without using active users for contention", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0], scenarioEquipment: true, appDataReplay: [0, 0] });
    runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
    expect(runtime.gotoEquip(0)).toBe(true);
    const equipment = runtime.room.furniture.find((item) => item.furnitureDataId === 18)!;
    expect(equipment.reservedUserIds).toEqual([0]);
    runtime.runTicks(80);
    expect(equipment.reservedUserIds).toEqual([]);
    expect(runtime.staffs[0]!.recoveryStock).toBe(10);
    expect(runtime.staffs[0]!.state).toBe(StaffState.MOVE);
    runtime.runTicks(20);
    expect(runtime.staffs[0]!.recoveryStock).toBeLessThan(10);
  });

  it("keeps equipment reservation contention separate from owner and active users", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 0, 0, 0] });
    const equipment = runtime.room.furniture.find((item) => item.furnitureDataId === 18)! as unknown as { activeUserIds: number[]; ownerStaffId: number; reservedUserIds: readonly number[] };
    equipment.activeUserIds.push(99);
    equipment.ownerStaffId = 99;
    expect(runtime.gotoEquip(0)).toBe(true);
    expect(runtime.gotoEquip(1)).toBe(false);
    expect(equipment.reservedUserIds).toEqual([0]);
  });

  it("runs talk reservation, invitation, timeline, cleanup, and desk return", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], appDataReplay: [1], libReplay: [0] });
    runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    runtime.configureStaff(1, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    expect(runtime.gotoTalk(0)).toBe(true);
    expect(runtime.staffs[0]!.flags & StaffFlag.RESERVED_TALK).toBe(StaffFlag.RESERVED_TALK);
    expect(runtime.staffs[1]!.flags & StaffFlag.INVITED).toBe(StaffFlag.INVITED);
    runtime.runTicks(220);
    expect(runtime.staffs[0]!.colleagueId).toBe(-1);
    expect(runtime.staffs[1]!.colleagueId).toBe(-1);
    expect(runtime.staffs[0]!.flags & (StaffFlag.RESERVED_TALK | StaffFlag.INVITED)).toBe(0);
    expect(runtime.traces.some((trace) => trace.event === "talk-frame-110-meeting-point")).toBe(true);
  });

  it("takes low HP Staff through door, home recovery, and desk return", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
    runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 5 });
    runtime.runTicks(260);
    const staff = runtime.staffs[0]!;
    expect(staff.maxHp).toBe(108);
    expect(staff.hp).toBeGreaterThanOrEqual(44);
    expect(staff.deskId).toBe(0);
    expect(runtime.traces.some((trace) => trace.event === "low-hp-go-to-door")).toBe(true);
    expect(runtime.traces.some((trace) => trace.event === "stay-home-recover")).toBe(true);
  });

  it("cleans a destroyed desk without stale owner/desk state", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0] });
    runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    expect(runtime.removeFurniture(0)).toBe(true);
    expect(runtime.staffs[0]!.deskId).not.toBe(0);
    expect(runtime.room.furniture.find((item) => item.instanceId === 0)?.ownerStaffId).toBe(-1);
    expect(runtime.traces.some((trace) => trace.event === "furniture-destroy-cleanup")).toBe(true);
  });

  it("preserves the Player to Room to Staff planning boundary", () => {
    const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1] });
    runtime.startPlanning();
    expect(runtime.player.planning).toBe(true);
    expect(runtime.staffs.every((staff) => (staff.flags & StaffFlag.PLANNING) !== 0)).toBe(true);
    runtime.endPlanning(true);
    expect(runtime.player.completed).toBe(true);
    expect(runtime.staffs.every((staff) => (staff.flags & StaffFlag.PLANNING) === 0)).toBe(true);
  });

  it("replays the same canonical transition log byte-identically", () => {
    const build = () => {
      const runtime = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 0, 0, 0] });
      runtime.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
      runtime.gotoEquip(0);
      runtime.runTicks(80);
      return runtime.snapshot();
    };
    expect(stableStringify(build())).toBe(stableStringify(build()));
  });

  it("closes all ten frozen acceptance scenarios through the runtime harness", () => {
    const results = runI0ScenarioSuite(catalogs);
    expect(results.map((result) => result.id)).toEqual(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]);
    expect(results.every((result) => result.status === "PASS")).toBe(true);
    expect(results.flatMap((result) => result.assertions.filter((check) => check.status === "FAIL"))).toEqual([]);
  });
});
