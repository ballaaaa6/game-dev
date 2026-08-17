import { describe, expect, it } from "vitest";
import { GraphicsCompatibility } from "../src/v2/graphics";
import { createV4Camera, createV4FurnitureBinding, createV4ResourceManager } from "../src/v4/fixture-loader";
import { resolveFurnitureSelectors, drawFurnitureBinding } from "../src/v4/furniture";
import { sortV4Drawables } from "../src/v4/ordering";

describe("V4 FurnitureData, Camera, and ordering boundaries", () => {
  it("resolves primary/secondary/image selectors and preserves sentinels", () => {
    const resources = createV4ResourceManager();
    expect(resolveFurnitureSelectors(resources, {
      furnitureDataId: 3,
      rawType: 2,
      primarySeb: 1,
      secondarySeb: 3,
      dataImage: 148,
    }).map((item) => item.status)).toEqual(["resolved", "resolved", "resolved"]);
    expect(resolveFurnitureSelectors(resources, {
      furnitureDataId: 0,
      rawType: 4,
      primarySeb: 11,
      secondarySeb: -1,
      dataImage: -1,
    }).map((item) => item.status)).toEqual(["resolved", "sentinel", "sentinel"]);
  });

  it("draws the selected native direct-image fixture at its proven offset", () => {
    const graphics = new GraphicsCompatibility();
    const traces: never[] = [];
    drawFurnitureBinding(
      createV4FurnitureBinding("furniture:12"),
      { x: 260, y: -21 },
      createV4ResourceManager(),
      graphics,
      traces,
    );
    expect(graphics.commands).toHaveLength(1);
    expect(graphics.commands[0].image.id).toBe("resChip_:image:109");
    expect(graphics.commands[0].destination).toEqual({ x: 248, y: -40, width: 24, height: 22 });
    expect(traces[0]).toMatchObject({ kind: "image", resource: { id: 109 } });
  });

  it("applies only integer camera translation", () => {
    const camera = createV4Camera();
    expect(camera.transform({ x: 10, y: -4 })).toEqual({ x: 10, y: -4 });
    camera.setPosition(7, -9);
    expect(camera.offset).toEqual({ x: 7, y: -9 });
    expect(camera.transform({ x: 10, y: -4 })).toEqual({ x: 17, y: -13 });
    expect(camera.getBaseX()).toBe(0);
    expect(camera.getBaseY()).toBe(0);
  });

  it("keeps the native row/column ordering stable", () => {
    const cells = [
      { cell: [1, 1] as const, key: "left" },
      { cell: [8, 1] as const, key: "right" },
      { cell: [4, 0] as const, key: "far" },
      { cell: [3, 1] as const, key: "middle" },
    ];
    expect(sortV4Drawables(cells).map((item) => item.key)).toEqual(["far", "right", "middle", "left"]);
  });
});
