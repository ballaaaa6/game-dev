import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { buildSceneProjection } from "../src/scene/projection";

describe("Room R raw scene overlay", () => {
  it("cross-checks the fixture against the runtime resolver and keeps every cell raw-only", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:17");
    expect(projection.rawOverlay).toMatchObject({
      roomId: "room:17",
      gridWidth: 10,
      gridHeight: 10,
      status: "pass",
      diagnosticOnly: true,
    });
    expect(projection.rawOverlay?.cells).toHaveLength(100);
    expect(projection.rawOverlay?.doorCells).toEqual([[8, 3]]);
    expect(projection.rawOverlay?.cells.every((cell) => cell.instanceId === null)).toBe(true);
    expect(projection.rawOverlay?.cells.every((cell) => cell.identityStatus === "raw_only_no_furniture_data_inference")).toBe(true);
    expect(projection.rawOverlay?.cells.find((cell) => cell.cell[0] === 8 && cell.cell[1] === 3)).toMatchObject({
      rawType: 5,
      rawDirection: 0,
    });
  });

  it("does not attach a Room R overlay to another room", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(buildSceneProjection(catalogs, "room:0").rawOverlay).toBeNull();
  });
});
