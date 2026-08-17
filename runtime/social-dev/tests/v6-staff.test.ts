import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import { GraphicsCompatibility } from "../src/v2/graphics";
import { createRoomV5, stableJson } from "../src/v5";
import {
  createV6RoomStaffPreview,
  getStaffMetadata,
  loadStaffFixtureCatalog,
  resolveHumanAction,
  StaffVisualResolverV6,
  StaffV6,
  integrateStaffIntoRoomV6,
} from "../src/v6";

describe("V6 Staff / StaffData / human animation static integration", () => {
  it.each([
    ["wait", "right", 10], ["wait", "left", 11], ["wait", "up", 12], ["wait", "down", 13],
    ["move", "right", 1], ["move", "left", 2], ["move", "up", 3], ["move", "down", 4],
    ["typing", "right", 23], ["typing", "left", 24], ["typing", "up", 25], ["typing", "down", 26],
  ] as const)("closes %s_%s through the original human selector ID", (action, direction, selectorId) => {
    const result = resolveHumanAction(action, { direction }, loadStaffFixtureCatalog());
    expect(result).toMatchObject({ action, direction, selectorId, status: "resolved" });
  });

  it("keeps all 141 StaffData image selectors aligned with the promoted Staff bindings", () => {
    const catalog = loadStaffFixtureCatalog();
    expect(catalog.metadata.staff).toHaveLength(141);
    expect(catalog.assets.staff_bindings).toHaveLength(141);
    for (const record of catalog.metadata.staff) {
      const binding = catalog.assets.staff_bindings.find((candidate) => candidate.source_id === record.source_identity.source_id);
      expect(binding?.image_selector_id).toBe(record.render?.image_selector?.id);
    }
  });

  it("resolves raw ObjChip direction through the native reverse table before selecting typing SEB", () => {
    const catalog = loadStaffFixtureCatalog();
    const typingFromRightRaw = resolveHumanAction("typing", { rawDirection: 0 }, catalog);
    expect(typingFromRightRaw).toMatchObject({
      rawDirection: 0,
      reverseDirection: 1,
      direction: "left",
      selectorId: 24,
      selectorFilename: "typing_left.seb",
      status: "resolved",
    });
    const talk = resolveHumanAction("talk", { direction: "down" }, catalog);
    expect(talk).toMatchObject({ action: "talk", sourceAction: "typing", selectorId: 26 });
  });

  it("keeps unsupported human actions explicit instead of inventing a filename", () => {
    const result = resolveHumanAction("fly_away", { direction: "right" }, loadStaffFixtureCatalog());
    expect(result).toMatchObject({ status: "deferred", selectorId: null, selectorFilename: null });
  });

  it("binds StaffData img_ to the selected human image while SEB TexId 0 remains a slot", () => {
    const staff = new StaffV6({ sourceStaffId: 0, action: "wait", direction: "right", alpha: 255 });
    const graphics = new GraphicsCompatibility();
    const draw = staff.draw(graphics, createRoomV5("room:0").camera);
    expect(staff.imageSelectorId).toBe(86);
    expect(draw.skipped).toBe(false);
    expect(draw.commandCount).toBeGreaterThan(0);
    expect(draw.commands[0]?.image.id).toBe("resHuman_:image:86");
    expect(draw.commands[0]?.destination).toMatchObject({ x: 626, y: -61 });
  });

  it("retains native alpha-zero spawn and deterministic source-bounded fade-in", () => {
    const staff = new StaffV6({ sourceStaffId: 0, action: "wait", direction: "right" });
    const graphics = new GraphicsCompatibility();
    const camera = createRoomV5("room:0").camera;
    expect(staff.alpha).toBe(0);
    expect(staff.draw(graphics, camera).skipped).toBe(true);
    staff.advanceAlpha(11);
    expect(staff.alpha).toBe(255);
    expect(staff.draw(graphics, camera).skipped).toBe(false);
  });

  it("uses the native frame bound and typing interval without browser timing", () => {
    const staff = new StaffV6({ sourceStaffId: 0, action: "typing", direction: "right", alpha: 255 });
    expect(staff.getFrameState()).toMatchObject({ selectorId: 23, frame: 0, frameBound: 20, frameInterval: 3 });
    staff.advanceFrame();
    expect(staff.getFrameState()?.frame).toBe(3);
    staff.advanceFrame(6);
    expect(staff.getFrameState()?.frame).toBe(1);
  });

  it("keeps Room.AddStaff door placement and integer camera forwarding exact", () => {
    const room = createRoomV5("room:0", { cameraOffset: { x: 7, y: -4 } });
    const staff = new StaffV6({ sourceStaffId: 0, action: "wait", direction: "right", alpha: 255 });
    const placement = staff.placement(room.camera);
    expect(placement).toMatchObject({
      cell: [8, 4],
      world: { x: 280, y: -31 },
      screen: { x: 647, y: -35 },
      cameraOffset: { x: 7, y: -4 },
    });
  });

  it("inserts StaffV6 after rear walls and before late foreground passes", () => {
    const room = createRoomV5("room:0", { visualScope: "full_static" });
    const catalog = loadStaffFixtureCatalog();
    const staff = catalog.actorSpawn.actors.slice(0, 3).map((actor) => new StaffV6({
      sourceStaffId: actor.source_staff_id,
      catalog,
      action: "wait",
      direction: "right",
      alpha: 255,
    }));
    const render = integrateStaffIntoRoomV6(room, staff);
    const avatarPass = render.passes.find((pass) => pass.passId === "avatar-primary");
    const latePass = render.passes.find((pass) => pass.passId === "object-chip-late");
    expect(avatarPass?.inputCount).toBe(3);
    expect(avatarPass?.commandEnd).toBeGreaterThan(avatarPass?.commandStart ?? 0);
    expect(latePass?.commandStart).toBeGreaterThanOrEqual(avatarPass?.commandEnd ?? 0);
    expect(render.staff.every((snapshot) => snapshot.placement.cell[0] === 8 && snapshot.placement.cell[1] === 4)).toBe(true);
    expect(render.integration.nativeRelation).toBe("SOURCE-LIMITED");
    expect(render.traces.filter((trace) => trace.pass === "avatar-primary")).toHaveLength(3);
  });

  it("produces a deterministic room:0 V6 manifest without changing the V5 baseline", () => {
    const manifest = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "right", alpha: 255 });
    expect(manifest.phase).toBe("V6");
    expect(manifest.staff).toHaveLength(3);
    expect(manifest.baseline).toMatchObject({ phase: "V5", commandCount: 139, traceCount: 124, eventCount: 788, passCount: 9 });
    expect(manifest.passes.map((pass) => pass.passId)).toEqual([
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
    expect(manifest.policy.exactPixels).toBe("DEFERRED_TO_V7");
    expect(manifest.commands).toHaveLength(142);
    expect(manifest.traces).toHaveLength(127);
    expect(manifest.events).toHaveLength(791);
    const hash = createHash("sha256").update(stableJson(manifest)).digest("hex");
    console.log(`V6_ROOM00_MANIFEST_SHA256=${hash}`);
  });

  it("does not import the production renderer from the V6 fixture surface", () => {
    const record = getStaffMetadata(0);
    expect(record.render?.family).toBe("human");
    expect(loadStaffFixtureCatalog().human.groupId).toBe("resHuman_");
  });

  it("exposes the combined Staff visual surface without duplicating parser logic", () => {
    const surface = new StaffVisualResolverV6().resolve(0, "wait", { direction: "right" });
    expect(surface).toMatchObject({ imageSelectorId: 86, selector: { selectorId: 10 } });
  });
});
