import { describe, expect, it } from "vitest";
import { furnitureFrameForScene } from "../src/assets/display-assets";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { applyFloor00DisplayPolicy, createInitialState } from "../src/core/simulation";
import { buildSceneProjection } from "../src/scene/projection";
import { buildVisualGateSnapshot } from "../src/renderer/visual-gate";

describe("floor00 native bootstrap scene", () => {
  it("loads the deterministic bootstrap contract against the closed catalogs", () => {
    const catalogs = loadRuntimeCatalogs();

    expect(catalogs.floor00.catalog_id).toBe("floor00-native-bootstrap");
    expect(catalogs.floor00.scene_ref.id).toBe("room:0");
    expect(catalogs.floor00.bootstrap.initial_staff_count).toBe(3);
    expect(catalogs.floor00.map.map_chip_cells).toBe(196);
    expect(catalogs.floor00.map.obj_chip_cells).toBe(100);
    expect(catalogs.floor00.native_initial_furniture).toHaveLength(6);
    expect(catalogs.floor00.actors).toHaveLength(3);
    expect(catalogs.floor00.render_composition.logical_order).toEqual([
      "background",
      "map-chip-and-map-floor-underlay",
      "map-extension-floor-pale-boundary",
      "object-chip-wall-rear-door-and-wall",
      "object-chip-primary-native-furniture",
      "avatar-primary-static-floor00-display-actors",
      "object-chip-late-foreground-wall",
      "diagnostic-overlay",
    ]);
    expect(catalogs.floor00.render_composition.foreground_wall_cells).toEqual([[8, 7], [8, 8]]);
  });

  it("projects only native initial furniture and the exact three entry actors", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });

    expect(projection.sceneMode).toBe("floor00");
    expect(projection.mapWidth).toBe(14);
    expect(projection.mapHeight).toBe(14);
    expect(projection.mapCells).toHaveLength(196);
    expect(projection.cells).toHaveLength(100);
    expect(projection.nativeInitialObjects.map((object) => `${object.objectId}@${object.cell[0]}:${object.cell[1]}`)).toEqual([
      "furniture:3@2:4",
      "furniture:3@3:4",
      "furniture:3@6:4",
      "furniture:12@8:5",
      "furniture:26@8:6",
      "furniture:56@2:7",
    ]);
    expect(projection.sceneAssets.find((asset) => asset.role === "floor")?.filename).toBe("floor_05.png");
    expect(projection.floorMetadataFilename).toBe("floor_09.png");
    expect(projection.sceneAssets.find((asset) => asset.role === "door")?.cell).toEqual([8, 4]);
    const wall = projection.sceneAssets.find((asset) => asset.role === "wall");
    expect(wall?.cellScope?.spriteLayers?.horizontal_frame_0).toHaveLength(2);
    expect(wall?.cellScope?.spriteLayers?.vertical_frame_1).toHaveLength(2);
    expect(wall?.cellScope?.spriteLayers?.vertical_frame_1?.map((record) => record.layer)).toEqual([0, 1]);
  });

  it("projects both raw type-4 facility pads as static SEB compositions without promoting them to FurnitureData", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });

    expect(catalogs.floor00.structural_facilities).toHaveLength(2);
    expect(catalogs.floor00.structural_facilities.map((facility) => `${facility.object_id}@${facility.anchor[0]}:${facility.anchor[1]}`)).toEqual([
      "furniture:0@4:2",
      "furniture:0@7:2",
    ]);
    expect(projection.structuralFacilities.map((facility) => `${facility.objectId}@${facility.anchor[0]}:${facility.anchor[1]}`)).toEqual([
      "furniture:0@4:2",
      "furniture:0@7:2",
    ]);
    expect(projection.structuralFacilities.map((facility) => facility.mapAnchor)).toEqual([[4, 5], [7, 5]]);
    expect(projection.structuralFacilities.every((facility) => facility.rawType === 4)).toBe(true);
    expect(projection.structuralFacilities.every((facility) => facility.renderStatus === "approved_static_structural_facility")).toBe(true);
    expect(projection.structuralFacilities[0]?.footprintCells).toEqual([
      [3, 1], [4, 1], [5, 1],
      [3, 2], [4, 2], [5, 2],
      [3, 3], [4, 3], [5, 3],
    ]);
    expect(projection.structuralFacilities[1]?.footprintCells).toEqual([
      [6, 1], [7, 1], [8, 1],
      [6, 2], [7, 2], [8, 2],
      [6, 3], [7, 3], [8, 3],
    ]);
    expect(projection.structuralFacilities[0]?.imageAssetId).toBe("asset:01_GAME_PACKS/chip/big_base00.png");
    expect(projection.structuralFacilities[0]?.frame).toMatchObject({
      start_frame: 0,
      source_x: 0,
      source_y: 0,
      width: 120,
      height: 61,
      destination_x: -40,
      destination_y: -21,
    });
    expect(projection.nativeInitialObjects).toHaveLength(6);
    expect(projection.nativeInitialObjects.some((object) => object.objectId === "furniture:0")).toBe(false);
  });

  it("keeps the bootstrap actors co-located at the native door entry", () => {
    const catalogs = loadRuntimeCatalogs();
    const state = createInitialState(catalogs);

    expect(Object.keys(state.actors).sort()).toEqual([
      "actor:staff:0",
      "actor:staff:1",
      "actor:staff:2",
    ]);
    for (const actor of Object.values(state.actors)) {
      expect(actor.cell).toEqual([8, 4]);
      expect(actor.position).toEqual({ x: 280, y: -31 });
      expect(actor.speed).toBe(3);
    }
  });

  it("reserves distinct empty walkable display cells and keeps the scene static", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });
    const state = applyFloor00DisplayPolicy(createInitialState(catalogs), catalogs);

    const snapshot = buildVisualGateSnapshot(projection, state, catalogs, null);

    expect(snapshot.checks.floor00_bootstrap.status).toBe("pass");
    expect(snapshot.checks.furniture_render.status).toBe("pending");
    expect(snapshot.checks.floor00_asset_lifecycle.status).toBe("pending");
    expect(snapshot.checks.floor00_furniture_composition.status).toBe("pending");
    expect(snapshot.checks.floor00_extension_wall_composition.status).toBe("pending");
    expect(snapshot.checks.floor00_fallback_usage.status).toBe("pending");
    expect(Object.values(state.actors).map((actor) => actor.cell)).toEqual([[4, 6], [5, 6], [7, 6]]);
    expect(Object.values(state.actors).every((actor) => actor.lifecycle === "idle")).toBe(true);
    expect(state.eventLog).toHaveLength(0);
  });

  it("pins every native floor00 furniture composition to frame 0", () => {
    for (const objectId of ["furniture:3", "furniture:12", "furniture:26", "furniture:56"]) {
      const frameZero = furnitureFrameForScene(objectId, 0, "floor00");
      const laterFrame = furnitureFrameForScene(objectId, 9, "floor00");

      expect(frameZero).not.toBeNull();
      expect(laterFrame).toEqual(frameZero);
      expect(laterFrame?.frame.start_frame).toBe(0);
      expect(laterFrame?.subFrame?.start_frame ?? 0).toBe(0);
    }
  });
});
