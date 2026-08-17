import { V4ContractError } from "./errors";
import type { V4CameraOffset, V4Point } from "./contracts";

/** Minimum V4 camera boundary: integer draw-space translation only. */
export class V4CameraBoundary {
  private offsetValue: V4CameraOffset;

  public constructor(offset: V4CameraOffset = { x: 0, y: 0 }) {
    this.offsetValue = validateOffset(offset);
  }

  public get offset(): V4CameraOffset {
    return { ...this.offsetValue };
  }

  public setPosition(x: number, y: number): void {
    this.offsetValue = validateOffset({ x, y });
  }

  public getX(): number {
    return this.offsetValue.x;
  }

  public getY(): number {
    return this.offsetValue.y;
  }

  public getBaseX(): number {
    return 0;
  }

  public getBaseY(): number {
    return 0;
  }

  public transform(world: V4Point): V4Point {
    if (!Number.isFinite(world.x) || !Number.isFinite(world.y)) {
      throw new V4ContractError("V4_CAMERA_VALUE_MALFORMED", "V4 world point is malformed");
    }
    return {
      x: world.x + this.offsetValue.x,
      y: world.y + this.offsetValue.y,
    };
  }
}

function validateOffset(offset: V4CameraOffset): V4CameraOffset {
  if (!Number.isSafeInteger(offset.x) || !Number.isSafeInteger(offset.y)) {
    throw new V4ContractError("V4_CAMERA_VALUE_MALFORMED", "V4 camera offset must be integer draw-space pixels");
  }
  return { x: offset.x, y: offset.y };
}
