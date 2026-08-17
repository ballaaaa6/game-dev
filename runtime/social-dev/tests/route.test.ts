import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { routeFromBehaviorContract } from "../src/core/route";

describe("closed route fixture", () => {
  it("keeps the verified cardinal route", () => {
    const route = routeFromBehaviorContract(loadRuntimeCatalogs().behavior);
    expect(route).toEqual([[8, 4], [7, 4], [6, 4]]);
    for (let index = 1; index < route.length; index += 1) {
      const previous = route[index - 1];
      const current = route[index];
      expect(Math.abs(current[0] - previous[0]) + Math.abs(current[1] - previous[1])).toBe(1);
    }
  });
});
