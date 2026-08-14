import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs, validateFloor00VisualLayoutContract } from "../src/catalog/load-contracts";
import { createInitialState } from "../src/core/simulation";
import { resolveForegroundWallCells } from "../src/renderer/canvas-renderer";
import { buildSceneProjection } from "../src/scene/projection";
import { buildVisualGateSnapshot } from "../src/renderer/visual-gate";

describe("floor00 visual layout contract", () => {
  it("loads the approved floor00 presentation policy", () => {
    const catalogs = loadRuntimeCatalogs();
    const layout = catalogs.floor00VisualLayout;

    expect(layout.catalog_id).toBe("floor00-visual-layout");
    expect(layout.scene_ref).toEqual({ id: "room:0", scene_mode: "floor00" });
    expect(layout.glass.source_asset_id).toBe("map:chip/wall_01.png");
    expect(layout.wood_wall.source_asset_id).toBe("asset:01_GAME_PACKS/chip/wall_00.png");
    expect(layout.wood_wall.layer_order).toEqual([0, 1]);
    expect(layout.glass.removed_trigger_cells.length).toBeGreaterThan(0);
    expect(Object.keys(layout.glass.final_trigger_cells_by_group).sort()).toEqual([
      "horizontal_frame_0",
      "vertical_frame_1",
    ]);

    const removed = new Set(layout.glass.removed_trigger_cells.map((cell) => cell.join(",")));
    const final = Object.values(layout.glass.final_trigger_cells_by_group)
      .flat()
      .map((cell) => cell.join(","));
    expect(final.some((cell) => removed.has(cell))).toBe(false);
    expect(layout.wood_wall.final_cells_by_frame).not.toEqual(layout.wood_wall.native_cells_by_frame);
  });

  it("rejects a glass strip whose declared endpoint is not rendered", () => {
    const catalogs = loadRuntimeCatalogs();
    const invalid = JSON.parse(JSON.stringify(catalogs.floor00VisualLayout)) as any;
    invalid.glass.final_trigger_cells_by_group.vertical_frame_1 = invalid.glass.final_trigger_cells_by_group.vertical_frame_1.slice(0, -1);

    expect(() => validateFloor00VisualLayoutContract(
      invalid,
      catalogs.defaultMap,
      catalogs.floor00,
      catalogs.nativeAssembly,
    )).toThrow("glass strip");
  });

  it("rejects a visual layout for a different scene mode", () => {
    const catalogs = loadRuntimeCatalogs();
    const invalid = JSON.parse(JSON.stringify(catalogs.floor00VisualLayout)) as any;
    invalid.scene_ref.scene_mode = "display-slice-01";

    expect(() => validateFloor00VisualLayoutContract(
      invalid,
      catalogs.defaultMap,
      catalogs.floor00,
      catalogs.nativeAssembly,
    )).toThrow("scene mode");
  });

  it("rejects overlapping removed and final glass cells", () => {
    const catalogs = loadRuntimeCatalogs();
    const invalid = JSON.parse(JSON.stringify(catalogs.floor00VisualLayout)) as any;
    invalid.glass.final_trigger_cells_by_group.horizontal_frame_0[0] = [2, 5];

    expect(() => validateFloor00VisualLayoutContract(
      invalid,
      catalogs.defaultMap,
      catalogs.floor00,
      catalogs.nativeAssembly,
    )).toThrow("overlaps removed");
  });

  it("rejects a wall offset larger than one cell", () => {
    const catalogs = loadRuntimeCatalogs();
    const invalid = JSON.parse(JSON.stringify(catalogs.floor00VisualLayout)) as any;
    invalid.wood_wall.backward_offset = [2, 0];

    expect(() => validateFloor00VisualLayoutContract(
      invalid,
      catalogs.defaultMap,
      catalogs.floor00,
      catalogs.nativeAssembly,
    )).toThrow("exactly one cell");
  });

  it("rejects a final wood wall cell outside the ObjChip grid", () => {
    const catalogs = loadRuntimeCatalogs();
    const invalid = JSON.parse(JSON.stringify(catalogs.floor00VisualLayout)) as any;
    invalid.wood_wall.final_cells_by_frame.vertical_frame_1[0] = [10, 1];

    expect(() => validateFloor00VisualLayoutContract(
      invalid,
      catalogs.defaultMap,
      catalogs.floor00,
      catalogs.nativeAssembly,
    )).toThrow("out-of-bounds");
  });

  it("projects only the approved floor00 glass and wood scopes", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });

    expect(projection.presentationLayout?.status).toBe("approved_floor00_visual_layout");
    expect(projection.presentationLayout?.removedGlassCells).toEqual(
      catalogs.floor00VisualLayout.glass.removed_trigger_cells,
    );
    expect(projection.presentationLayout?.finalGlassCellsByGroup).toEqual(
      catalogs.floor00VisualLayout.glass.final_trigger_cells_by_group,
    );
    expect(projection.presentationLayout?.backwardOffset).toEqual(
      catalogs.floor00VisualLayout.wood_wall.backward_offset,
    );

    const main = buildSceneProjection(catalogs);
    expect(main.sceneMode).toBe("floor00");
    expect(main.presentationLayout?.status).toBe("approved_floor00_visual_layout");
  });

  it("passes dedicated visual checks for the approved floor00 layout", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });
    const snapshot = buildVisualGateSnapshot(projection, createInitialState(catalogs), catalogs, null);

    expect(snapshot.checks.floor00_visual_layout.status).toBe("pass");
    expect(snapshot.checks.floor00_glass_continuity.status).toBe("pass");
    expect(snapshot.checks.floor00_wall_alignment.status).toBe("pass");
  });

  it("moves the foreground wall split with the approved floor00 wall offset", () => {
    const catalogs = loadRuntimeCatalogs();
    const main = buildSceneProjection(catalogs);

    expect(resolveForegroundWallCells(main, catalogs)).toEqual([[9, 7], [9, 8]]);
  });
});
