import { describe, expect, it } from "vitest";
import { createCharacterSpawnPlan, resolveCharacter, resolveCharacterAction } from "../src/catalog/character-resolver";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";

describe("full character capability resolver", () => {
  it("resolves every StaffData record through one shared human profile", () => {
    const catalogs = loadRuntimeCatalogs();
    for (let sourceId = 0; sourceId < 141; sourceId += 1) {
      const resolved = resolveCharacter(catalogs, `staff:${sourceId}`);
      expect(resolved.catalogKind).toBe("staff");
      expect(resolved.profile.id).toBe("human-staff-v1");
      expect(resolved.imageSelector?.resolution_status).toBe("resolved");
      expect(resolveCharacterAction(catalogs, `staff:${sourceId}`, "wait", "left").selector?.selector_id).toBe(11);
      expect(resolveCharacterAction(catalogs, `actor:staff:${sourceId}`, "typing", "down").selector?.selector_id).toBe(26);
    }
  });

  it("keeps special staff, helpers, and explicit action gaps separate", () => {
    const catalogs = loadRuntimeCatalogs();
    const special = resolveCharacter(catalogs, "staff:114");
    expect(special.template.name.values.English).toBe("Bearington Bearington");
    expect(special.behaviorProfileId).toBe("staff-living-scene-v1");

    const helper = resolveCharacter(catalogs, "helper:2");
    expect(helper.catalogKind).toBe("helper");
    expect(helper.profile.id).toBe("helper-record-v1");
    expect(helper.behaviorProfileId).toBeNull();

    const deferred = resolveCharacterAction(catalogs, "staff:114", "fly_away");
    expect(deferred.status).toBe("deferred");
    expect(deferred.selector).toBeNull();

    const nativeBanzai = resolveCharacterAction(catalogs, "staff:114", "banzai", "right");
    expect(nativeBanzai.status).toBe("native_selector_ready");
    expect(nativeBanzai.selector?.selector_id).toBe(19);

    const unsupportedDirection = resolveCharacterAction(catalogs, "staff:114", "banzai", "left");
    expect(unsupportedDirection.status).toBe("no_selector_for_direction");
    expect(unsupportedDirection.selector).toBeNull();
  });

  it("returns a lazy spawn plan without creating mutable ActorState", () => {
    const catalogs = loadRuntimeCatalogs();
    const plan = createCharacterSpawnPlan(catalogs, "staff:114");
    expect(plan.instanceCreation).toBe("lazy_on_spawn_or_scene_use");
    expect(plan.profileId).toBe("human-staff-v1");
    expect(plan.sourceId).toBe(114);
    expect(plan.assetLoading).toBe("lazy_by_selector");
    expect(plan.availableActions).toContain("talk");
    expect(plan.availableActions).toContain("banzai");
  });
});
