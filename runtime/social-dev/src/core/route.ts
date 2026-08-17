import type { BehaviorContract } from "../catalog/types";
import type { Cell } from "./types";

function isCell(value: unknown): value is readonly [number, number] {
  return Array.isArray(value) && value.length === 2 && value.every((item) => typeof item === "number");
}

export function routeFromBehaviorContract(contract: BehaviorContract): readonly Cell[] {
  const milestone = contract.trace.milestones.find((candidate) => candidate.event === "move");
  if (!milestone?.route || milestone.route.length < 2 || !milestone.route.every(isCell)) {
    throw new Error("Behavior contract does not contain a closed movement route");
  }
  const route = milestone.route.map(([x, y]) => [x, y] as const);
  for (let index = 1; index < route.length; index += 1) {
    const [previousX, previousY] = route[index - 1];
    const [currentX, currentY] = route[index];
    if (Math.abs(currentX - previousX) + Math.abs(currentY - previousY) !== 1) {
      throw new Error("Movement route is not cardinal-adjacent");
    }
  }
  return route;
}
