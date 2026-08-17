import { describe, expect, it } from "vitest";
import { compareNativeCells, classifyNativeWallLayer, sortNativeDrawables } from "../src/renderer/native-render-order";

describe("native room render ordering", () => {
  it("walks each native row from right to left", () => {
    const cells = [
      { cell: [1, 1] as const, key: "left" },
      { cell: [8, 1] as const, key: "right" },
      { cell: [4, 0] as const, key: "far" },
      { cell: [3, 1] as const, key: "middle" },
    ];

    expect(sortNativeDrawables(cells).map((item) => item.key)).toEqual(["far", "right", "middle", "left"]);
    expect(compareNativeCells({ cell: [8, 1] }, { cell: [1, 1] })).toBeLessThan(0);
  });

  it("keeps the front boundary and door in the late occlusion layer", () => {
    expect(classifyNativeWallLayer([8, 3])).toBe("rear");
    expect(classifyNativeWallLayer([8, 4])).toBe("rear");
    expect(classifyNativeWallLayer([8, 6])).toBe("rear");
    expect(classifyNativeWallLayer([8, 7])).toBe("foreground");
    expect(classifyNativeWallLayer([8, 8])).toBe("foreground");
    expect(classifyNativeWallLayer([4, 1])).toBe("rear");
  });

  it("accepts the foreground wall cells from the floor00 composition contract", () => {
    expect(classifyNativeWallLayer([8, 7], [[8, 8]])).toBe("rear");
    expect(classifyNativeWallLayer([8, 8], [[8, 8]])).toBe("foreground");
  });
});
