import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { resolveRoomScene, roomKeys } from "../src/scene/room-resolver";
import { buildSceneProjection } from "../src/scene/projection";
import { createRenderPassPlan } from "../src/renderer/render-plan";

describe("all-room runtime resolver", () => {
  it("connects every RoomData row to the shared MapChip topology", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(roomKeys(catalogs)).toHaveLength(18);
    for (const roomId of roomKeys(catalogs)) {
      const room = resolveRoomScene(catalogs, roomId);
      expect(room.status).toBe("pass");
      expect(room.mapVariant).toBe("floor_0");
      expect(room.mapCells).toHaveLength(196);
      expect(room.placements).toHaveLength(100);
      expect(room.nativeBindings.every((binding) => binding.source_status === "verified_strict_native_initial_binding")).toBe(true);
    }
  });

  it("keeps room:0's native instances explicit and never treats raw types as FurnitureData ids", () => {
    const room = resolveRoomScene(loadRuntimeCatalogs(), "room:0");
    expect(room.assets.floor).toMatchObject({
      rawSelectorId: 5,
      runtimeSelectorId: 85,
      filename: "floor_05.png",
      metadataFilename: "floor_09.png",
      runtimeAssetId: "map:chip/floor_05.png",
    });
    expect(room.nativeBindings.map((binding) => `${binding.object_id}@${binding.cell[0]}:${binding.cell[1]}`)).toEqual([
      "furniture:3@2:4",
      "furniture:3@3:4",
      "furniture:3@6:4",
      "furniture:12@8:5",
      "furniture:26@8:6",
      "furniture:56@2:7",
    ]);
    expect(room.placements.filter((placement) => placement.kind === "native_instance")).toHaveLength(6);
    expect(room.placements.filter((placement) => placement.kind !== "native_instance").some((placement) => placement.furnitureDataId !== undefined)).toBe(false);
    expect(room.placements.every((placement) => placement.directionLabel.length > 0)).toBe(true);
    expect(room.placements.every((placement) => placement.directionVector.length === 2)).toBe(true);
    expect(room.placements.find((placement) => placement.cell.join(",") === "8,1")).toMatchObject({
      passable: false,
      collisionKind: "footprint_wall",
    });
    expect(room.placements.find((placement) => placement.cell.join(",") === "9,1")).toMatchObject({
      passable: false,
      collisionKind: "boundary_wall",
    });
    expect(room.placements.find((placement) => placement.cell.join(",") === "8,4")).toMatchObject({
      passable: true,
      collisionKind: "entry_door",
    });
    expect(room.placements.find((placement) => placement.cell.join(",") === "8,5")).toMatchObject({
      passable: false,
      collisionKind: "installed_furniture",
    });
  });

  it("resolves room:R metadata and native wall/door composition without guessing furniture", () => {
    const room = resolveRoomScene(loadRuntimeCatalogs(), "room:17");
    expect(room.name).toBe("Floor R");
    expect(room.assets.floor).toMatchObject({
      rawSelectorId: 9,
      runtimeSelectorId: 85,
      filename: "floor_09.png",
      runtimeAssetId: "map:chip/floor_09.png",
    });
    expect(room.assets.wall.runtimeAssetId).toBe("asset:01_GAME_PACKS/chip/wall_06.png");
    expect(room.assets.door.runtimeAssetId).toBe("asset:01_GAME_PACKS/chip/door_06.png");
    expect(room.assets.wall.runtimeStatus).toBe("pass_promoted_room_selector_asset");
    expect(room.assets.wall.compositionStatus).toBe("approved_native_coordinate_composition");
    expect(room.assets.door.compositionStatus).toBe("approved_native_coordinate_composition");
    expect(room.assets.door.cell).toEqual([8, 3]);
    expect(room.nativeBindings).toHaveLength(0);
    const door = room.placements.find((placement) => placement.cell[0] === 8 && placement.cell[1] === 3);
    expect(door).toMatchObject({ kind: "door_fixture", rawType: 5 });
    expect(door?.furnitureDataId).toBeUndefined();
    expect(door?.objectId).toBeUndefined();
  });

  it("executes the native pass contract as explicit render stages", () => {
    const projection = buildSceneProjection(loadRuntimeCatalogs());
    expect(createRenderPassPlan(projection).map((pass) => pass.id)).toEqual(projection.drawPasses);
    expect(createRenderPassPlan(projection).map((pass) => pass.layerRole)).toEqual([
      "MapChip.DrawExtentionFloor",
      "MapChip.Draw",
      "ObjChip.Draw",
      "ObjChip.DrawWall",
      "Avatar.Draw",
      "Avatar.DrawSecondary",
      "ObjChip.DrawLatePreview",
      "ObjChip.DrawLate",
      "MapChip.DrawFloor",
    ]);
  });
});
