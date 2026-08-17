import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";

describe("runtime contract boundary", () => {
  it("loads only approved contracts and the display slice", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(catalogs.preRuntime.status).toBe("pass");
    expect(catalogs.scene.status).toBe("pass");
    expect(catalogs.objects.status).toBe("pass");
    expect(catalogs.actors.status).toBe("pass");
    expect(catalogs.characterCapabilities.status).toBe("pass");
    expect(catalogs.characterAssets.status).toBe("pass");
    expect(catalogs.characterMetadata.status).toBe("pass");
    expect(catalogs.spawn.status).toBe("pass");
    expect(catalogs.camera.status).toBe("pass");
    expect(catalogs.behavior.status).toBe("pass");
    expect(catalogs.tickOrder.status).toBe("pass");
    expect(catalogs.displayScene.grid.width).toBe(10);
    expect(catalogs.displayScene.grid.height).toBe(10);
    expect(catalogs.objects.objects).toHaveLength(4);
    expect(catalogs.actors.actors).toHaveLength(5);
    expect(catalogs.characterCapabilities.profiles).toHaveLength(4);
    expect(catalogs.characterCapabilities.bindings.staff).toHaveLength(141);
    expect(catalogs.characterCapabilities.bindings.helpers).toHaveLength(19);
    expect(catalogs.characterAssets.images).toHaveLength(105);
    expect(catalogs.characterAssets.animations).toHaveLength(35);
    expect(catalogs.characterAssets.staff_bindings).toHaveLength(141);
    expect(catalogs.characterMetadata.staff).toHaveLength(141);
    expect(catalogs.characterMetadata.helpers).toHaveLength(19);
    expect(catalogs.characterMetadata.jobs).toHaveLength(30);
    expect(catalogs.characterMetadata.skills).toHaveLength(36);
    expect(catalogs.characterMetadata.staff[114].source_identity.source_id).toBe(114);
    expect(catalogs.characterMetadata.staff[114].render?.image_selector?.resolution_status).toBe("resolved");
    expect(catalogs.characterMetadata.runtime_readiness?.instance_creation).toBe("lazy_on_spawn_or_scene_use");
    expect(catalogs.activeActors).toHaveLength(3);
    expect(catalogs.activeActors.every((actor) => actor.desk_assignment.status === "deferred")).toBe(true);
    expect(catalogs.defaultMap.room.native_floor_img_selector).toBe(23);
    expect(catalogs.defaultMap.room.native_floor_filename).toBe("floor_05.png");
    expect(catalogs.defaultMap.room.resolved_floor_img_selector).toBe(85);
    expect(catalogs.defaultMap.room.resolved_floor_filename).toBe("floor_05.png");
    expect(catalogs.defaultMap.room.resolved_floor_metadata_filename).toBe("floor_09.png");
    expect(catalogs.defaultMap.floor_selector_remap.runtime_resolution_mode).toBe("explicit_user_approved_alias");
    expect(catalogs.defaultMap.floor_selector_remap.runtime_render_filename).toBe("floor_05.png");
    expect(catalogs.defaultMap.floor_selector_remap.runtime_render_resolution_mode).toBe("explicit_user_approved_visual_asset_with_runtime_selector_alias");
  });

  it("keeps source provenance separate from runtime readiness", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(catalogs.actors.runtime_readiness?.status).toBe("ready_for_vite_typescript_core");
    expect(catalogs.tickOrder.mutation_policy.source_code_imports).toBe(false);
    expect(catalogs.tickOrder.mutation_policy.renderer_may_mutate).toBe(false);
  });
});
