import { describe, expect, it } from "vitest";
import checkpointLedger from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/checkpoint-ledger.json";
import coordinateBridge from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/coordinate-bridge-audit.json";
import finalScene from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/final-scene-manifest.json";
import passMembership from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/pass-membership-audit.json";
import stage0 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage0-mapchip.json";
import stage1 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage1-room-floor.json";
import stage2 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage2-walls-corners.json";
import stage3 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage3-door.json";
import stage4 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage4-structural.json";
import stage5 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage5-furniture.json";
import stage6 from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage6-staff.json";
import unknowns from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/unknowns.json";
import visualAcceptance from "../../../knowledge/fixtures/accepted/visual-port/starter-room-reintegration/visual-acceptance.json";
import { createV6RoomStaffPreview } from "../src/v6";
import { createRoomV5 } from "../src/v5";
import { selectReintegrationLayer } from "../src/v7/starter-room-reintegration";

describe("starter-room layered reintegration gate", () => {
  it("keeps V8 explicitly unstarted", () => {
    expect(finalScene.v8_started).toBe(false);
    expect(checkpointLedger.v8_started).toBe(false);
    expect(finalScene.status).toBe("PASS_STARTER_ROOM_REINTEGRATION");
  });

  it("records the required static-only execution envelope", () => {
    expect(checkpointLedger.execution_mode).toBe("INLINE_STATIC_ONLY");
    expect(checkpointLedger.subagents).toBe(false);
    expect(checkpointLedger.external_state).toEqual({
      emulator: false,
      adb: false,
      live_app: false,
      server: false,
      network: false,
      screenshots: false,
    });
  });

  it("passes the baseline checkpoint", () => {
    const baseline = checkpointLedger.checkpoints.find((checkpoint) => checkpoint.checkpoint === "RI.0");
    expect(baseline?.status).toBe("PASS");
    expect(baseline?.owner_class).toBe("BASELINE_GATE");
  });

  it("freezes the accepted 14 by 14 MapChip topology", () => {
    expect(stage0.topology).toMatchObject({
      width: 14,
      height: 14,
      cell_count: 196,
      nonempty_count: 81,
      empty_sentinel_count: 115,
    });
  });

  it("preserves the accepted MapChip selector histogram", () => {
    expect(stage0.topology.selector_histogram).toEqual({
      "10": 33,
      "11": 2,
      "12": 1,
      "13": 4,
      "14": 4,
      "15": 3,
      "85": 28,
      "105": 2,
      "154": 1,
      "155": 1,
      "156": 2,
    });
  });

  it("matches the forensic MapChip render exactly", () => {
    expect(stage0.commands.count).toBe(81);
    expect(stage0.commands.trace_count).toBe(81);
    expect(stage0.commands.only_pass).toBe("main-display-map-underlay");
    expect(stage0.accepted_forensic_match.matched_pixel_sha256).toBe(true);
    expect(stage0.accepted_forensic_match.matched_png_sha256).toBe(true);
    expect(stage0.png.pixel_sha256).toBe("3ea05bd9edcc5168a14ee1b0e79256e460072be75c018f11f2009d01c215d293");
    expect(stage0.png.png_sha256).toBe("fb40142389fe963bba46a93a122f961dc21fe8a85d0abac75b1a68fd3d4ecaed");
  });

  it("keeps the MapChip foundation deterministic and gap-free", () => {
    expect(stage0.png.deterministic_repeat).toMatchObject({ identical: true, changed_pixel_count: 0 });
    expect(stage0.alpha_component_count).toBe(1);
    expect(stage0.unexpected_transparent_pixels).toBe(0);
  });

  it("assigns the room floor to the existing MapChip foundation", () => {
    expect(stage1.owner_class).toBe("ROOM_FLOOR_OWNER");
    expect(stage1.ownership.decision).toBe("A_MAPCHIP_FOUNDATION_ALREADY_CONTAINS_ROOM_FLOOR");
    expect(stage1.ownership.room_floor_cell_count).toBe(28);
    expect(stage1.ownership.added_command_count).toBe(0);
    expect(stage1.ownership.duplicated_floor_plane).toBe(false);
  });

  it("keeps Stage 1 byte-identical to Stage 0 while exposing floor-only evidence", () => {
    expect(stage1.commands.stage1_mapchip_plus_room_floor.command_count).toBe(81);
    expect(stage1.commands.stage1_mapchip_plus_room_floor.pixel_sha256).toBe(stage0.png.pixel_sha256);
    expect(stage1.commands.stage1_mapchip_plus_room_floor.png_sha256).toBe(stage0.png.png_sha256);
    expect(stage1.commands.stage1_floor_only.command_count).toBe(28);
  });

  it("selects the MapChip layer from the real V5 draw stream", () => {
    const source = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" }).draw();
    const selection = selectReintegrationLayer(source, { trace: (trace) => trace.pass === "main-display-map-underlay" });
    expect(selection.commands).toHaveLength(81);
    expect(selection.traces).toHaveLength(81);
    expect(selection.selectedCommandIndices[0]).toBe(0);
  });

  it("keeps walls and corners isolated from the door", () => {
    expect(stage2.owner_class).toBe("OBJCHIP_WALL");
    expect(stage2.commands.command_count).toBe(46);
    expect(stage2.commands.trace_count).toBe(31);
    expect(stage2.connectivity.door_excluded).toBe(true);
    expect(stage2.connectivity.wall_cell_count).toBe(14);
    expect(stage2.corners.fixtures.every((fixture) => fixture.proof === "NATIVE-CODE-PROVEN")).toBe(true);
  });

  it("proves wall connectivity and the coordinate bridge", () => {
    expect(visualAcceptance.structural_visual_sanity.walls_connect).toBe(true);
    expect(stage2.coordinate_bridge.no_screenshot_tuning).toBe(true);
    expect(stage2.coordinate_bridge.source_canvas_bases.normalized_delta_x).toBe(360);
    expect(coordinateBridge.samples.map_cell_5_5).toEqual({ x: 400, y: 0 });
    expect(coordinateBridge.samples.door_cell_8_4).toEqual({ x: 600, y: -31 });
    expect(coordinateBridge.samples.staff_cell_8_4).toMatchObject({ cell: [8, 4], world: { x: 280, y: -31 } });
  });

  it("keeps the door as a single source-backed layer", () => {
    expect(stage3.owner_class).toBe("DOOR");
    expect(stage3.commands.command_count).toBe(1);
    expect(stage3.door).toMatchObject({
      cell: [8, 4],
      raw_type: 5,
      seb_selector: 6,
      image_selector: 7,
      pass: "object-chip-wall",
      proof: "NATIVE-CODE-PROVEN",
    });
  });

  it("keeps structural facilities on explicit native anchors", () => {
    expect(stage4.owner_class).toBe("STRUCTURAL");
    expect(stage4.commands.command_count).toBe(2);
    expect(stage4.no_invented_props).toBe(true);
    expect(stage4.objects.map((object) => object.anchor_cell)).toEqual([[4, 2], [7, 2]]);
    expect(stage4.objects.every((object) => object.raw_type === 4 && object.pass === "object-chip-primary")).toBe(true);
  });

  it("keeps the six explicit FurnitureData instances and their counts", () => {
    expect(stage5.owner_class).toBe("FURNITURE_BOOTSTRAP");
    expect(stage5.counts).toEqual({ furniture_3: 3, furniture_12: 1, furniture_26: 1, furniture_56: 1, total: 6 });
    expect(stage5.instances).toHaveLength(6);
    expect(stage5.instances.map((instance) => instance.object_id)).toEqual([
      "furniture:3",
      "furniture:3",
      "furniture:3",
      "furniture:12",
      "furniture:26",
      "furniture:56",
    ]);
  });

  it("does not infer furniture from raw ObjChip types", () => {
    expect(stage5.no_raw_type_inference).toBe(true);
    expect(stage5.compound_policy).toContain("furniture:3");
    expect(stage5.instances.every((instance) => instance.proof === "verified_strict_native_initial_binding")).toBe(true);
  });

  it("uses the unchanged three-actor Staff bootstrap fixture", () => {
    expect(stage6.owner_class).toBe("STAFF_INTEGRATION");
    expect(stage6.semantics_changed).toBe(false);
    expect(stage6.actors.map((actor) => actor.staff_data_id)).toEqual([0, 1, 2]);
    expect(stage6.actors.every((actor) => actor.cell[0] === 8 && actor.cell[1] === 4)).toBe(true);
    expect(stage6.actors.every((actor) => actor.action === "wait" && actor.direction === "right" && actor.frame === 0)).toBe(true);
  });

  it("keeps Staff isolated to the avatar-primary pass", () => {
    expect(stage6.commands.staff_only.command_count).toBe(3);
    expect(stage6.commands.staff_only.trace_count).toBe(3);
    expect(stage6.commands.complete_room_with_staff.command_count).toBe(142);
    expect(stage6.commands.staff_only.deterministic_repeat.identical).toBe(true);
    expect(stage6.occlusion).toContain("Staff avatar-primary");
  });

  it("preserves the native pass schedule and stream counts", () => {
    expect(passMembership.source_streams).toEqual({
      structural: { commands: 139, traces: 124, events: 788 },
      with_staff: { commands: 142, traces: 127, events: 791 },
    });
    expect(passMembership.production_renderer_changed).toBe(false);
    expect(passMembership.native_pass_schedule.map((pass) => pass.pass_id)).toEqual([
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
  });

  it("records the complete staged command partition", () => {
    expect(finalScene.per_layer_command_counts).toEqual({
      mapchip_foundation: 81,
      room_floor_added: 0,
      walls_corners: 46,
      door: 1,
      structural: 2,
      furniture: 9,
      staff: 3,
    });
    expect(finalScene.complete_command_count).toBe(142);
  });

  it("repeats the final structural and Staff renders identically", () => {
    expect(finalScene.final_structural.deterministic_repeat).toMatchObject({ identical: true, changed_pixel_count: 0 });
    expect(finalScene.final_with_staff.deterministic_repeat).toMatchObject({ identical: true, changed_pixel_count: 0 });
    expect(finalScene.final_structural.pixel_sha256).toBe("f139c65b2b4357b972fbdbca37308060091607d3907593e6893df77803e67288");
    expect(finalScene.final_with_staff.pixel_sha256).toBe("c3d82b29a78b827e682b623c94789e34701bd4cfa0369a14ea81fcf2fe2a30b6");
  });

  it("passes all static visual sanity checks", () => {
    expect(visualAcceptance.status).toBe("PASS");
    expect(visualAcceptance.evidence_acceptance).toEqual({
      correct_owners: true,
      selectors: true,
      topology: true,
      coordinates: true,
      passes: true,
      command_determinism: true,
    });
    expect(visualAcceptance.structural_visual_sanity).toMatchObject({
      floor_continuous: true,
      walls_connect: true,
      corners_close: true,
      door_sits_in_wall: true,
      exterior_front_scene_coherent: true,
      furniture_inside_room: true,
      staff_spatially_coherent: true,
      no_unexplained_holes_or_floating_pieces: true,
    });
  });

  it("includes the required ten-panel human QA contact sheet", () => {
    expect(visualAcceptance.contact_sheet_panels).toHaveLength(10);
    expect(visualAcceptance.contact_sheet_panels).toContain("Previous broken-room comparison");
    expect(visualAcceptance.contact_sheet.path).toContain("STARTER_ROOM_LAYERED_REINTEGRATION_CONTACT_SHEET.png");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("floor");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("walls");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("door");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("structural");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("furniture");
    expect(visualAcceptance.layer_isolation_strips).toHaveProperty("Staff");
  });

  it("keeps production and accepted foundations unchanged", () => {
    expect(finalScene.production_renderer_changed).toBe(false);
    expect(finalScene.mapchip_foundation_changed).toBe(false);
    expect(finalScene.staff_semantics_changed).toBe(false);
    expect(stage0.proof).toContain("runtime/social-dev/src/v7/raster.ts");
  });

  it("keeps remaining unknowns explicit and non-blocking", () => {
    expect(unknowns.items).toHaveLength(3);
    expect(unknowns.items.every((item) => item.blocking === false)).toBe(true);
    expect(unknowns.status).toBe("PASS_WITH_EXPLICIT_NONBLOCKING_UNKNOWNs");
  });

  it("classifies the target as the starter main-display static environment", () => {
    expect(finalScene.first_launch_state_classification.value).toContain("ROOM_0_AFTER_NEWGAME_BOOTSTRAP");
    expect(finalScene.first_launch_state_classification.target).toBe("source-backed first-launch / starter main-display static environment");
    expect(finalScene.first_launch_state_classification.excludes).toEqual(["UI overlays", "tutorial overlays", "gameplay simulation"]);
  });

  it("advances through RI.11 and stops before V8", () => {
    expect(checkpointLedger.checkpoints.map((checkpoint) => checkpoint.checkpoint)).toEqual([
      "RI.0",
      "RI.1",
      "RI.2",
      "RI.3",
      "RI.4",
      "RI.5",
      "RI.6",
      "RI.7",
      "RI.8",
      "RI.9",
      "RI.10",
      "RI.11",
    ]);
    expect(checkpointLedger.checkpoints.at(-1)?.status).toBe("PASS_STOP_BEFORE_V8");
  });

  it("renders the Staff source fixture with the same placement contract", () => {
    const source = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "right", frame: 0, alpha: 255 });
    expect(source.staff).toHaveLength(3);
    expect(source.staff.every((actor) => actor.placement.cell[0] === 8 && actor.placement.cell[1] === 4)).toBe(true);
    expect(source.staff.every((actor) => actor.placement.world.x === 280 && actor.placement.world.y === -31)).toBe(true);
  });
});
