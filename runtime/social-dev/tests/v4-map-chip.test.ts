import { describe, expect, it } from "vitest";
import { createV4Camera, createV4ResourceManager } from "../src/v4/fixture-loader";
import {
  drawMapChipBoundary,
  isMapFloorCellVisible,
  mapChipOrigin,
  renderMapChip,
} from "../src/v4/map-chip";
import type { V4CommandTrace } from "../src/v4/contracts";
import { GraphicsCompatibility } from "../src/v2/graphics";

describe("V4 MapChip compatibility", () => {
  it("keeps the native MapChip projection separate from ObjChip projection", () => {
    const camera = createV4Camera();
    expect(mapChipOrigin([2, 3], camera)).toEqual({ x: 200, y: 20 });
    expect(isMapFloorCellVisible([5, 5], 14, 14)).toBe(true);
    expect(isMapFloorCellVisible([9, 8], 14, 14)).toBe(true);
    expect(isMapFloorCellVisible([4, 5], 14, 14)).toBe(false);
    expect(isMapFloorCellVisible([9, 9], 14, 14)).toBe(false);
  });

  it("resolves the original resChip_ image/SEB IDs through V3", () => {
    const resources = createV4ResourceManager();
    expect(resources.groupId).toBe("resChip_");
    expect(resources.resolveImage(2).ref.id).toBe("resChip_:image:2");
    expect(resources.resolveImage(2).width).toBe(96);
    expect(resources.hasSeb(63)).toBe(true);
  });

  it("emits a floor image command at the native height anchor", () => {
    const result = renderMapChip(
      { cell: [5, 5], imageId: 85, roomFloor: 0, roomWidth: 14, roomHeight: 14 },
      createV4ResourceManager(),
      createV4Camera(),
    );
    expect(result.commands).toHaveLength(1);
    expect(result.commands[0].image.id).toBe("resChip_:image:85");
    expect(result.commands[0].destination).toEqual({ x: 400, y: 0, width: 80, height: 39 });
    expect(result.traces[0]).toMatchObject({ pass: "map-floor", resource: { id: 85 } });
  });

  it("expands a verified extension trigger into two native SEB calls", () => {
    const result = renderMapChip(
      { cell: [4, 5], imageId: -1, roomFloor: 0, roomWidth: 14, roomHeight: 14 },
      createV4ResourceManager(),
      createV4Camera(),
    );
    expect(result.traces).toHaveLength(2);
    expect(result.traces.every((trace) => trace.resource.id === 63 && trace.frame === 1)).toBe(true);
    expect(result.commands).toHaveLength(2);
  });

  it("keeps the verified horizontal extension on frame 0", () => {
    const result = renderMapChip(
      { cell: [2, 5], imageId: -1, roomFloor: 0, roomWidth: 14, roomHeight: 14 },
      createV4ResourceManager(),
      createV4Camera(),
    );
    expect(result.traces).toHaveLength(2);
    expect(result.traces.every((trace) => trace.resource.id === 63 && trace.frame === 0)).toBe(true);
    expect(result.commands).toHaveLength(2);
  });

  it("keeps the optional selector-7 boundary overlay safe when the selected V3 fixture lacks it", () => {
    const graphics = new GraphicsCompatibility();
    const traces: V4CommandTrace[] = [];
    drawMapChipBoundary(
      { cell: [0, 0], imageId: -1, roomFloor: 1, roomWidth: 14, roomHeight: 14 },
      createV4ResourceManager(),
      createV4Camera(),
      graphics,
      traces,
    );
    expect(graphics.commands.length).toBeGreaterThan(0);
    expect(traces.every((trace) => trace.resource.id !== 7)).toBe(true);
  });
});
