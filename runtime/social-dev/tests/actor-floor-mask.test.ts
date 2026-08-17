import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { buildSceneProjection } from "../src/scene/projection";
import { evaluateActorFloorContainment } from "../src/scene/actor-floor-mask";

describe("floor00 actor floor containment", () => {
  it("keeps all reserved display actors inside rendered floor diamonds", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });

    for (const actor of catalogs.floor00DisplayPolicy.actors) {
      const result = evaluateActorFloorContainment(actor.reserved_cell, projection, catalogs.camera);
      expect(result.status, `${actor.id}: ${result.reason}`).toBe("pass");
      expect(result.containingCells.length).toBeGreaterThan(0);
    }
  });

  it("rejects boundary and installed-furniture cells", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });

    const boundary = evaluateActorFloorContainment([0, 0], projection, catalogs.camera);
    const furniture = evaluateActorFloorContainment([2, 4], projection, catalogs.camera);

    expect(boundary.status).toBe("blocked");
    expect(boundary.reason).toContain("not_empty_walkable");
    expect(furniture.status).toBe("blocked");
    expect(furniture.reason).toContain("installed_furniture");
  });
});
