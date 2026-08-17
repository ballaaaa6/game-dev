import { describe, expect, it } from "vitest";
import {
  characterDisplayFrame,
  characterFrameAssetIds,
  getCharacterAnimation,
  getCharacterAssetManifest,
  getCharacterImageAsset,
  selectCharacterAnimationRecords,
} from "../src/assets/character-assets";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";

describe("full character asset catalog", () => {
  it("resolves frames for every StaffData image through the promoted asset set", () => {
    const catalogs = loadRuntimeCatalogs();
    const manifest = getCharacterAssetManifest();
    expect(manifest.images).toHaveLength(105);
    expect(manifest.animations).toHaveLength(35);

    for (let sourceId = 0; sourceId < 141; sourceId += 1) {
      const wait = characterDisplayFrame(catalogs, `staff:${sourceId}`, "wait", "left", 10);
      expect(wait?.selectorId).toBe(11);
      expect(wait?.imageAssetId).toMatch(/^asset:01_GAME_PACKS\/human\/chara\d+\.png$/);
      expect(wait?.records.length).toBeGreaterThan(0);
      expect(wait?.records.every((record) => record.texture_status === "resolved")).toBe(true);

      const move = characterDisplayFrame(catalogs, `staff:${sourceId}`, "move", "up", 5);
      expect(move?.selectorId).toBe(3);
      expect(move?.records.length).toBeGreaterThan(0);
    }
  });

  it("keeps talk aliases and multilayer control records explicit", () => {
    const catalogs = loadRuntimeCatalogs();
    const talk = characterDisplayFrame(catalogs, "staff:114", "talk", "right", 0);
    expect(talk?.selectorId).toBe(23);
    expect(talk?.animation.filename).toBe("typing_right.seb");

    const nativeGesture = characterDisplayFrame(catalogs, "staff:114", "banzai", "right", 0);
    expect(nativeGesture?.selectorId).toBe(19);
    expect(nativeGesture?.records.length).toBe(3);

    const head = characterDisplayFrame(catalogs, "staff:114", "head", "right", 0);
    expect(head?.selectorId).toBe(100);
    expect(head ? characterFrameAssetIds(head) : []).toEqual([
      "asset:01_GAME_PACKS/human/chara81.png",
      "asset:01_GAME_PACKS/human/chara01.png",
    ]);

    const multilayer = getCharacterAnimation(19);
    if (!multilayer) {
      throw new Error("Expected human banzai selector 19");
    }
    expect(multilayer.header.layer_count).toBe(3);
    expect(selectCharacterAnimationRecords(multilayer, 0).length).toBe(3);
    expect(multilayer.records.some((record) => record.texture_status === "control_no_texture")).toBe(true);
  });

  it("exposes exact lazy asset identities without loading the full catalog", () => {
    const manifest = getCharacterAssetManifest();
    expect(manifest.runtime_policy.image_loading).toBe("lazy_by_character_and_asset_id");
    expect(manifest.runtime_policy.eager_load_full_catalog).toBe(false);
    const image = getCharacterImageAsset("asset:01_GAME_PACKS/human/chara00.png");
    expect(image?.runtime_path).toBe("assets/character-catalog/01_GAME_PACKS/human/chara00.png");
  });
});
