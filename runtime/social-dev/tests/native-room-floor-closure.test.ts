import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { buildSceneProjection } from "../src/scene/projection";
import { resolveRoomScene } from "../src/scene/room-resolver";

describe("native Room.floor_ topology closure", () => {
  it("loads the native selector contract and connects both topology rows", () => {
    const catalogs = loadRuntimeCatalogs();
    const usage = catalogs.nativeRoomFloorUsage;
    expect(usage.topology_selection.native_field).toBe("Room.floor_");
    expect(usage.topology_selection.predicate).toBe("floor == 0 ? MAPCHIP_ARRAY[0] : MAPCHIP_ARRAY[1]");
    expect(usage.topology_selection.variants.floor_0).toMatchObject({ width: 14, height: 14, length: 196 });
    expect(usage.topology_selection.variants.floor_nonzero).toMatchObject({ width: 4, height: 4, length: 16 });
    expect(usage.topology_selection.variants.floor_nonzero.rows).toEqual([
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
    ]);
    expect(usage.usage.map((record) => record.usage_id)).toEqual([
      "player-add-room",
      "addition-floor-preview",
      "main-display-map",
    ]);
  });

  it("resolves the current full display without changing the approved floor alias", () => {
    const room = resolveRoomScene(loadRuntimeCatalogs(), "room:0");
    expect(room).toMatchObject({
      mapWidth: 14,
      mapHeight: 14,
      mapVariant: "floor_0",
      nativeFloorValue: 0,
      context: "main_display",
      environmentScope: "native_main_14x14_outer_map",
      topologyStatus: "verified_native_floor_selector_and_dimensions",
      extensionWallStatus: "approved_native_14x14_extension_predicates",
    });
    expect(room.mapCells).toHaveLength(196);
    expect(room.assets.floor).toMatchObject({
      rawSelectorId: 5,
      runtimeSelectorId: 85,
      filename: "floor_05.png",
      metadataFilename: "floor_09.png",
    });
  });

  it("resolves the native 4x4 persistent path and never borrows a 14x14 row", () => {
    const room = resolveRoomScene(loadRuntimeCatalogs(), "room:17", {
      nativeFloorValue: 0,
      context: "persistent_room",
    });
    expect(room).toMatchObject({
      mapWidth: 4,
      mapHeight: 4,
      mapVariant: "floor_0",
      nativeFloorValue: 0,
      context: "persistent_room",
      environmentScope: "native_room_topology_only",
      extensionWallStatus: "explicitly_not_promoted_for_native_4x4_topology",
    });
    expect(room.mapCells).toHaveLength(16);
    expect(room.mapCells.every((cell) => cell.rawIndex === 0)).toBe(true);
    expect(room.mapCells.every((cell) => cell.nativeFloorPass)).toBe(true);
  });

  it("resolves the native nonzero preview path and preserves the raw floor value", () => {
    const catalogs = loadRuntimeCatalogs();
    const room = resolveRoomScene(catalogs, "room:17", {
      nativeFloorValue: 1,
      context: "addition_floor_preview",
    });
    expect(room).toMatchObject({
      mapWidth: 4,
      mapHeight: 4,
      mapVariant: "floor_nonzero",
      nativeFloorValue: 1,
      context: "addition_floor_preview",
      environmentScope: "native_room_topology_only",
    });
    expect(room.mapCells).toHaveLength(16);
    expect(room.mapCells.every((cell) => cell.rawIndex === 1 && cell.nativeFloorPass)).toBe(true);
    expect(room.extensionWalls).toHaveLength(0);

    const alternateNonzero = resolveRoomScene(catalogs, "room:17", {
      nativeFloorValue: 5,
      context: "addition_floor_preview",
    });
    expect(alternateNonzero.nativeFloorValue).toBe(5);
    expect(alternateNonzero.mapVariant).toBe("floor_nonzero");
  });

  it("rejects the invalid combination that caused upper-floor data to be faked", () => {
    expect(() => resolveRoomScene(loadRuntimeCatalogs(), "room:17", {
      nativeFloorValue: 1,
      context: "addition_floor_preview",
      dimensions: { width: 14, height: 14 },
    })).toThrow("native 4x4 only");
  });

  it("passes the same topology options through the projection boundary", () => {
    const projection = buildSceneProjection(loadRuntimeCatalogs(), "room:17", {
      nativeFloorValue: 1,
      context: "addition_floor_preview",
    });
    expect(projection).toMatchObject({
      mapWidth: 4,
      mapHeight: 4,
      nativeFloorValue: 1,
      roomContext: "addition_floor_preview",
      environmentScope: "native_room_topology_only",
      extensionWallStatus: "explicitly_not_promoted_for_native_4x4_topology",
    });
    expect(projection.mapCells).toHaveLength(16);
    expect(projection.rawOverlay).toBeNull();
  });
});
