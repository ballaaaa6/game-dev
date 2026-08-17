import { describe, expect, it } from "vitest";
import { classifyNativeCollision } from "../src/scene/native-collision";

describe("native ObjChip collision classification", () => {
  it("keeps verified empty cells and the entry door traversable", () => {
    expect(classifyNativeCollision(0, false)).toEqual({ passable: true, kind: "empty_walkable" });
    expect(classifyNativeCollision(5, false)).toEqual({ passable: true, kind: "entry_door" });
    expect(classifyNativeCollision(1, false)).toEqual({ passable: true, kind: "unbound_place_slot" });
  });

  it("blocks native boundary, footprint, and explicitly installed furniture cells", () => {
    expect(classifyNativeCollision(6, false)).toEqual({ passable: false, kind: "boundary_wall" });
    expect(classifyNativeCollision(3, false)).toEqual({ passable: false, kind: "footprint_wall" });
    expect(classifyNativeCollision(4, false)).toEqual({ passable: false, kind: "footprint_anchor" });
    expect(classifyNativeCollision(2, true)).toEqual({ passable: false, kind: "installed_furniture" });
  });
});
