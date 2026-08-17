import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { StaffFlag, StaffState } from "../src/core/living/constants";
import { createLivingRuntime } from "../src/core/living/runtime";
import { createDashboardRuntime } from "../src/product/dashboard";
import { createV8LiveRuntime } from "../src/v8/live-runtime";
import { directionForRaw, rawDirectionForStep } from "../src/v8/direction";
import { createFukidashi, isDrawableFukidashi, updateFukidashi } from "../src/v8/fukidashi";
import { compileV8Room0Commands } from "../src/v8/command-compiler";
import { compileWorkstationComposition } from "../src/v8/workstation";
import { buildSceneProjection } from "../src/scene/projection";

const catalogs = loadRuntimeCatalogs();

describe("V8 live Room0 visual contract", () => {
  it("keeps the source-backed raw direction and selector authority exact", () => {
    expect([0, 1, 2, 3].map(directionForRaw)).toEqual(["left", "right", "down", "up"]);
    expect(rawDirectionForStep([8, 4], [7, 4])).toBe(0);
    expect(rawDirectionForStep([8, 4], [9, 4])).toBe(1);
    expect(rawDirectionForStep([8, 4], [8, 5])).toBe(2);
    expect(rawDirectionForStep([8, 4], [8, 3])).toBe(3);
  });

  it("implements the native Fukidashi payload and lifetime guards", () => {
    const payload = createFukidashi(25, "invitation", 2, 0);
    expect(payload).toMatchObject({ id: 25, lifetime: 40, delay: 2, offsetY: 0, text: "Hey, listen..." });
    expect(isDrawableFukidashi(payload)).toBe(false);
    const afterDelay = updateFukidashi(payload)!;
    expect(afterDelay).toMatchObject({ lifetime: 40, delay: 1 });
    const drawable = updateFukidashi(afterDelay)!;
    expect(drawable).toMatchObject({ lifetime: 39, delay: 0 });
    expect(isDrawableFukidashi(drawable)).toBe(true);
  });

  it("projects three live Staff actors from the canonical door into desks", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1, 2] });
    const v8 = createV8LiveRuntime(catalogs, living.snapshot());
    expect(v8.snapshot().staffs.map((staff) => staff.cell)).toEqual([[8, 4], [8, 4], [8, 4]]);
    let visual = v8.snapshot();
    for (let index = 0; index < 35; index += 1) visual = v8.advance(living.tick());
    expect(visual.staffs.every((staff) => staff.alpha > 0)).toBe(true);
    expect(visual.staffs.some((staff) => staff.lifecycle === "move" || staff.lifecycle === "work")).toBe(true);
    expect(visual.staffs.every((staff) => staff.selectorId > 0)).toBe(true);
    expect(visual.diagnostics.unresolvedSelectors).toEqual([]);
    expect(visual.rngState.sequence).toBeGreaterThanOrEqual(0);
  });

  it("compiles all nine native passes with live nested workstation ownership", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1, 2] });
    const v8 = createV8LiveRuntime(catalogs, living.snapshot());
    let visual = v8.snapshot();
    for (let index = 0; index < 45; index += 1) visual = v8.advance(living.tick());
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });
    const plan = compileV8Room0Commands(catalogs, projection, visual);
    expect(plan.passes.map((pass) => pass.id)).toEqual([
      "map-extension-floor",
      "map-chip",
      "object-chip-primary",
      "object-chip-wall",
      "avatar-primary",
      "avatar-secondary",
      "object-chip-late-preview",
      "object-chip-late",
      "map-floor",
    ]);
    expect(plan.underlayFirst).toBe(true);
    expect(plan.rowOrder).toBe("y_ascending_x_descending");
    expect(plan.passes.find((pass) => pass.id === "object-chip-primary")?.commands.filter((command) => command.kind === "furniture")).toHaveLength(6);
    const nested = plan.passes.find((pass) => pass.id === "object-chip-primary")?.commands.filter((command) => command.kind === "workstation") ?? [];
    expect(nested.length).toBeGreaterThanOrEqual(1);
    expect(nested.every((command) => command.workstation?.commands.map((item) => item.kind))).toBeTruthy();
  });

  it("keeps both native FurnitureData(3) directional interleaves exact", () => {
    const down = compileWorkstationComposition(1, [3, 4], 1, [3, 4], 23, 0, 2);
    expect(down.commands.map((command) => [command.kind, command.frame ?? null])).toEqual([
      ["furniture", null],
      ["chair", 1],
      ["staff", 0],
      ["chair", 2],
    ]);

    const up = compileWorkstationComposition(0, [2, 4], 0, [2, 4], 11, 0, 3);
    expect(up.commands.map((command) => [command.kind, command.frame ?? null])).toEqual([
      ["chair", 0],
      ["staff", 0],
      ["furniture", null],
    ]);
  });

  it("keeps invitation and equipment visual states separate from product task state", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true, appDataReplay: [0, 0] });
    living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING, hp: 50 });
    expect(living.gotoEquip(0)).toBe(true);
    const v8 = createV8LiveRuntime(catalogs, living.snapshot());
    let visual = v8.snapshot();
    for (let index = 0; index < 61; index += 1) visual = v8.advance(living.tick());
    const equipmentStaff = visual.staffs.find((staff) => staff.id === 0)!;
    expect([7, 8, 11, 12, 15, 16]).toContain(equipmentStaff.selectorId);
    expect(visual.rngDraws.every((draw) => draw.stream === "AppData" && draw.exclusiveMax)).toBe(true);
  });

  it("projects the exact even-direction equipment selector cadence", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0], scenarioEquipment: true });
    const equipment = living.room.furniture.find((item) => item.furnitureDataId === 18)!;
    living.configureStaff(0, {
      state: StaffState.USE_EQUIPMENT,
      equipmentId: equipment.instanceId,
      cell: [equipment.cell[0], equipment.cell[1]],
      frame: 20,
    });
    const v8 = createV8LiveRuntime(catalogs, living.snapshot());
    expect(v8.snapshot().staffs[0]?.selectorId).toBe(8);

    living.configureStaff(0, { frame: 40 });
    expect(v8.advance(living.snapshot()).staffs[0]?.selectorId).toBe(16);
    living.configureStaff(0, { frame: 60 });
    expect(v8.advance(living.snapshot()).staffs[0]?.selectorId).toBe(12);
  });

  it("projects source-backed invitation timing, pools, and deterministic payloads", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], appDataReplay: [1, 0, 0, 0], libReplay: [0] });
    living.configureStaff(0, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    living.configureStaff(1, { state: StaffState.WORK, flags: StaffFlag.SITTING });
    const v8 = createV8LiveRuntime(catalogs, living.snapshot(), { seed: 1234 });
    expect(living.gotoTalk(0)).toBe(true);

    let visual = v8.advance(living.snapshot());
    const payloads: typeof visual.fukidashi[number][] = [];
    for (let index = 0; index < 300; index += 1) {
      visual = v8.advance(living.tick());
      payloads.push(...visual.fukidashi);
    }

    expect(visual.invitations).toMatchObject([{ initiatorId: 0, targetId: 1, outcome: expect.stringMatching(/accepted|busy/) }]);
    expect(payloads.some((payload) => [25, 26, 27, 28, 29, 68].includes(payload.id) && payload.source === "invitation")).toBe(true);
    expect(payloads.every((payload) => payload.lifetime >= 1 && payload.delay <= 0 && payload.offsetY === 0 && payload.text.length > 0)).toBe(true);
    expect(visual.rngDraws.every((draw) => draw.stream === "AppData" && draw.method === "Random" && draw.exclusiveMax)).toBe(true);
  });

  it("keeps RUNNING product state independent across live Talk, equipment, and home", () => {
    const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1], scenarioEquipment: true });
    const dashboard = createDashboardRuntime(living);
    dashboard.bindAgent("agent-alpha", 0);
    dashboard.assignTask("task-alpha", "agent-alpha");
    dashboard.startTask("task-alpha");
    for (const state of [StaffState.TALK, StaffState.USE_EQUIPMENT, StaffState.STAY_HOME]) {
      living.configureStaff(0, { state });
      dashboard.step(1);
      expect(dashboard.getDashboardReadModel().agents[0]?.task.status).toBe("RUNNING");
    }
  });
});
