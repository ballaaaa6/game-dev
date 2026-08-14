import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { buildSceneProjection } from "../src/scene/projection";

describe("Phase 3C integrated render plan", () => {
  it("contains the unified native room placements", () => {
    const projection = buildSceneProjection(loadRuntimeCatalogs());
    expect(projection.sceneMode).toBe("floor00");
    expect(projection.renderObjects).toEqual([]);
    expect(projection.structuralFacilities.map((facility) => facility.objectId)).toEqual(["furniture:0", "furniture:0"]);
    expect(projection.nativeInitialObjects.map((object) => `${object.objectId}@${object.cell[0]}:${object.cell[1]}`)).toEqual([
      "furniture:3@2:4",
      "furniture:3@3:4",
      "furniture:3@6:4",
      "furniture:12@8:5",
      "furniture:26@8:6",
      "furniture:56@2:7",
    ]);
    expect(projection.sceneAssets.find((asset) => asset.role === "floor")).toMatchObject({
      status: "approved_room_selector_asset",
      rawSelectorId: 5,
      runtimeResolutionStatus: "pass_runtime_map_asset",
      runtimeAssetId: "map:chip/floor_05.png",
      filename: "floor_05.png",
      floorResolutionMode: "explicit_runtime_alias",
      metadataFilename: "floor_09.png",
    });
    expect(projection.sceneAssets.filter((asset) => asset.status === "approved_native_coordinate_composition").map((asset) => asset.role)).toEqual(["wall", "door"]);

    const roomFloorCells = projection.mapCells.filter((cell) => cell.rawIndex === 1);
    expect(roomFloorCells.length).toBeGreaterThan(0);
    expect(roomFloorCells.every((cell) => cell.selectorId === 85)).toBe(true);
    expect(roomFloorCells.every((cell) => cell.filename === "floor_05.png")).toBe(true);
    expect(projection.mapCells.some((cell) => cell.filename === "floor_05.png")).toBe(true);
  });

  it("retains native pass order and overlap policy", () => {
    const projection = buildSceneProjection(loadRuntimeCatalogs());
    expect(projection.drawPasses).toEqual([
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
});
