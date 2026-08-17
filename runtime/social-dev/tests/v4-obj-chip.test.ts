import { describe, expect, it } from "vitest";
import { GraphicsCompatibility } from "../src/v2/graphics";
import { createV4Camera, createV4FurnitureBinding, createV4ResourceManager } from "../src/v4/fixture-loader";
import type { V4CommandTrace } from "../src/v4/contracts";
import {
  drawObjChipPrimary,
  drawObjChipWall,
  getDirectionInfo,
  objChipOrigin,
  renderObjChip,
  wallFramesFor,
} from "../src/v4/obj-chip";

describe("V4 ObjChip compatibility", () => {
  it("uses the native object projection and preserves all four direction values", () => {
    const camera = createV4Camera();
    expect(objChipOrigin([2, 3], camera)).toEqual({ x: 100, y: 19 });
    expect(getDirectionInfo(0)).toMatchObject({ label: "DIRECTION_RIGHT", vector: [0, 1], reverse: 1 });
    expect(getDirectionInfo(1)).toMatchObject({ label: "DIRECTION_LEFT", vector: [0, -1], reverse: 0 });
    expect(getDirectionInfo(2)).toMatchObject({ label: "DIRECTION_UP", vector: [1, 0], reverse: 3 });
    expect(getDirectionInfo(3)).toMatchObject({ label: "DIRECTION_DOWN", vector: [-1, 0], reverse: 2 });
  });

  it("keeps wall and door frame predicates separate", () => {
    expect(wallFramesFor({ cell: [8, 1], rawType: 0, roomWidth: 10, roomHeight: 10 })).toEqual([1, 0]);
    expect(wallFramesFor({ cell: [7, 1], rawType: 0, roomWidth: 10, roomHeight: 10 })).toEqual([0]);
    expect(wallFramesFor({ cell: [8, 4], rawType: 5, roomWidth: 10, roomHeight: 10 })).toEqual([0]);
    expect(wallFramesFor({ cell: [4, 4], rawType: 0, roomWidth: 10, roomHeight: 10 })).toEqual([]);
  });

  it("emits both active wall SEB layers for an intersection cell", () => {
    const graphics = new GraphicsCompatibility();
    const traces: V4CommandTrace[] = [];
    drawObjChipWall(
      { cell: [8, 1], rawType: 0, rawDirection: 0, roomWidth: 10, roomHeight: 10, wallImageId: 6, doorImageId: 7 },
      createV4ResourceManager(),
      createV4Camera(),
      graphics,
      traces,
    );
    expect(graphics.commands).toHaveLength(4);
    expect(traces.map((trace) => trace.frame)).toEqual([1, 0]);
  });

  it("emits the native raw type-5 door record without FurnitureData", () => {
    const result = renderObjChip(
      { cell: [8, 4], rawType: 5, rawDirection: 0, roomWidth: 10, roomHeight: 10, wallImageId: 6, doorImageId: 7 },
      createV4ResourceManager(),
      createV4Camera(),
    );
    expect(result.commands).toHaveLength(1);
    expect(result.commands[0].image.id).toBe("resChip_:image:7");
    expect(result.traces[0]).toMatchObject({ resource: { id: 6 }, selectorRole: "ObjChip.DrawWall:raw_type_5_door" });
  });

  it("draws only an explicitly supplied native furniture binding", () => {
    const binding = createV4FurnitureBinding("furniture:3");
    const result = renderObjChip(
      {
        cell: [2, 4],
        rawType: 2,
        rawDirection: 0,
        roomWidth: 10,
        roomHeight: 10,
        wallImageId: 6,
        doorImageId: 7,
        furnitureBinding: binding,
      },
      createV4ResourceManager(),
      createV4Camera(),
    );
    expect(result.commands).toHaveLength(2);
    expect(result.commands.map((command) => command.image.id)).toEqual([
      "resChip_:image:3",
      "resChip_:image:4",
    ]);
    expect(result.traces.map((trace) => trace.resource.id)).toEqual([1, 3]);
  });

  it("does not infer furniture identity from a raw object type", () => {
    const graphics = new GraphicsCompatibility();
    const traces: V4CommandTrace[] = [];
    drawObjChipPrimary(
      { cell: [8, 5], rawType: 1, rawDirection: 0, roomWidth: 10, roomHeight: 10, wallImageId: 6, doorImageId: 7 },
      createV4ResourceManager(),
      createV4Camera(),
      graphics,
      traces,
    );
    expect(graphics.commands).toHaveLength(0);
    expect(traces).toHaveLength(0);
  });
});
