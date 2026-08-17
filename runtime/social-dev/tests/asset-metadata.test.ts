import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import {
  findFurnitureMetadata,
  findRuntimeAssetMetadata,
  findRuntimeFamilyAssets,
  resolveNativeSelectorAsset,
  resolveNativeSelectorAssetByKey,
} from "../src/catalog/asset-metadata";

describe("runtime asset metadata query surface", () => {
  const catalogs = loadRuntimeCatalogs();

  it("loads the lazy runtime manifest without source imports", () => {
    expect(catalogs.assetMetadataRuntime.counts.runtime_assets).toBe(186);
    expect(catalogs.assetMetadataRuntime.lazy_loading.eager_load_full_catalog).toBe(false);
    expect(catalogs.assetMetadataRuntime.runtime_policy.placement_inference_disabled).toBe(true);
  });

  it("resolves runtime and catalog-only selector targets by stable identity", () => {
    const runtime = resolveNativeSelectorAsset(catalogs, "chip", "seb", 1);
    expect(runtime.status).toBe("runtime_ready");
    expect(runtime.asset_id).toBe("asset:01_GAME_PACKS/chip/desk_00.seb");
    expect(runtime.runtime_metadata?.family_id).toBe("world.chip");

    const catalogOnly = resolveNativeSelectorAsset(catalogs, "chip", "img", 100);
    expect(catalogOnly.status).toBe("catalog_only");
    expect(catalogOnly.asset_id).toBe("asset:01_GAME_PACKS/chip/drawing.png");
  });

  it("keeps unresolved selectors explicit", () => {
    const unresolved = resolveNativeSelectorAssetByKey(catalogs, "ref:lineup_layout:seb:0");
    expect(unresolved.status).toBe("missing_selector");
    expect(unresolved.asset_id).toBeUndefined();
  });

  it("queries family and furniture metadata lazily", () => {
    expect(findRuntimeAssetMetadata(catalogs, "asset:01_GAME_PACKS/human/chara86.png")?.family_id).toBe("character.staff.human");
    expect(findRuntimeFamilyAssets(catalogs, "world.chip").length).toBeGreaterThan(0);
    const furniture = findFurnitureMetadata(catalogs, 3);
    expect(furniture.status).toBe("resolved");
    expect(furniture.selector_references.length).toBeGreaterThan(0);
    expect(findFurnitureMetadata(catalogs, 999).status).toBe("missing");
  });
});
