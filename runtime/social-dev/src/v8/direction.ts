import {
  V8_DIRECTION_BY_RAW,
  V8_RAW_DIRECTIONS,
  type V8Direction,
} from "./contracts";
import type { LivingCell } from "../core/living/types";

export function directionForRaw(rawDirection: number): V8Direction {
  return V8_DIRECTION_BY_RAW[rawDirection] ?? "left";
}

export function rawDirectionForStep(from: LivingCell, to: LivingCell): number | null {
  const dx = to[0] - from[0];
  const dy = to[1] - from[1];
  if (dx < 0) return V8_RAW_DIRECTIONS.left;
  if (dx > 0) return V8_RAW_DIRECTIONS.right;
  if (dy < 0) return V8_RAW_DIRECTIONS.up;
  if (dy > 0) return V8_RAW_DIRECTIONS.down;
  return null;
}

export function selectorForDirection(
  direction: V8Direction,
  selectors: readonly number[],
): number {
  const raw = V8_RAW_DIRECTIONS[direction];
  const selector = selectors[raw];
  if (selector === undefined) {
    throw new Error(`V8 selector catalog is missing direction ${direction}`);
  }
  return selector;
}

export function directionFromSelector(selectorId: number): V8Direction | null {
  const maps: readonly [readonly number[], V8Direction][] = [
    [[11, 10, 13, 12], "right"],
    [[24, 23, 26, 25], "right"],
    [[2, 1, 4, 3], "right"],
  ];
  for (const [selectors] of maps) {
    const raw = selectors.indexOf(selectorId);
    if (raw >= 0) return V8_DIRECTION_BY_RAW[raw] ?? null;
  }
  return null;
}

export function directionVector(direction: V8Direction): readonly [number, number] {
  switch (direction) {
    case "left": return [-1, 0];
    case "right": return [1, 0];
    case "up": return [0, -1];
    case "down": return [0, 1];
  }
}
