import { V4CameraBoundary } from "../v4/camera";
import type { V4CameraOffset, V4Point } from "../v4/contracts";

// Room.Draw uses two native lattices for the same room. The source-backed
// canvas bases are 82 for MapChip and 442 for ObjChip/Staff.
// V5 command previews already carry the shared viewport normalization, so the
// smallest equivalent bridge keeps MapChip at the established preview origin
// and carries only the proven 360-pixel difference into object/actor space.
export const V5_SOURCE_MAP_DRAW_OFFSET_X = 82;
export const V5_SOURCE_OBJECT_DRAW_OFFSET_X = 442;
export const V5_NATIVE_MAP_DRAW_OFFSET_X = 0;
export const V5_NATIVE_OBJECT_DRAW_OFFSET_X = V5_SOURCE_OBJECT_DRAW_OFFSET_X - V5_SOURCE_MAP_DRAW_OFFSET_X;

class V5DrawSpaceCamera extends V4CameraBoundary {
  public constructor(
    private readonly baseX: number,
    offset: V4CameraOffset = { x: 0, y: 0 },
  ) {
    super(offset);
  }

  public override getBaseX(): number {
    return this.baseX;
  }

  public override transform(world: V4Point): V4Point {
    const logical = super.transform(world);
    return { x: logical.x + this.baseX, y: logical.y };
  }
}

export function createV5MapCamera(offset: V4CameraOffset = { x: 0, y: 0 }): V4CameraBoundary {
  return new V5DrawSpaceCamera(V5_NATIVE_MAP_DRAW_OFFSET_X, offset);
}

export function createV5ObjectCamera(offset: V4CameraOffset = { x: 0, y: 0 }): V4CameraBoundary {
  return new V5DrawSpaceCamera(V5_NATIVE_OBJECT_DRAW_OFFSET_X, offset);
}
