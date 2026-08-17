import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import {
  findNativeAsset,
  findNativeConnections,
  findNativeDataRecord,
  findNativeSelector,
  resolveNativeId,
} from "../src/catalog/native-content";

describe("native content ID bridge", () => {
  it("resolves data, selector, asset, and connection records by their native IDs", () => {
    const catalogs = loadRuntimeCatalogs();
    const room = findNativeDataRecord(catalogs, "data:room:0");
    const selector = findNativeSelector(catalogs, "ref:chip:img:23");
    const asset = findNativeAsset(catalogs, "asset:01_GAME_PACKS/chip/floor_05.png");

    expect(room?.data_type).toBe("RoomData");
    expect((room?.decoded as { fields?: { floorImgId_?: number } }).fields?.floorImgId_).toBe(5);
    expect(selector).toMatchObject({ selector_id: 23, target_filename: "floor_05.png", status: "resolved" });
    expect(asset).toMatchObject({ extension: ".png", width: 80, height: 39, source_status: "native_source" });

    const roomConnections = findNativeConnections(catalogs, "data:room:0");
    expect(roomConnections.some((connection) => connection.to === "ref:chip:img:23")).toBe(true);
    expect(findNativeConnections(catalogs, "asset:missing")).toHaveLength(0);
  });

  it("returns the complete traversable identity slice for one ID", () => {
    const resolution = resolveNativeId(loadRuntimeCatalogs(), "ref:chip:img:23");
    expect(resolution.selector).toMatchObject({ selector_key: "ref:chip:img:23" });
    expect(resolution.asset).toBeUndefined();
    expect(resolution.connections.some((connection) => connection.to === "asset:01_GAME_PACKS/chip/floor_05.png")).toBe(true);
  });
});
