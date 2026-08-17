import { describe, expect, it } from "vitest";

import groupCoverage from "../../../knowledge/fixtures/accepted/visual-port/v3/group-coverage.json";
import checkpointLedger from "../../../knowledge/fixtures/accepted/visual-port/v3/checkpoint-ledger.json";
import fixtureManifest from "../../../knowledge/fixtures/accepted/visual-port/v3/fixture-manifest.json";
import imageSebAssociation from "../../../knowledge/fixtures/accepted/visual-port/v3/image-seb-association.json";
import imgIndex from "../../../knowledge/fixtures/accepted/visual-port/v3/img-index-contract.json";
import resourceGroupMap from "../../../knowledge/fixtures/accepted/visual-port/v3/resource-group-map.json";
import sebIndex from "../../../knowledge/fixtures/accepted/visual-port/v3/seb-index-contract.json";
import v2Acceptance from "../../../knowledge/fixtures/accepted/visual-port/v2/v2-static-acceptance.json";
import v1Lookup from "../../../knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json";
import { createAdditionalResourceManager, createResourceManager, createVisualAppData } from "../src/v3/fixture-loader";
import { V3DeferredError, V3LookupError } from "../src/v3/errors";

describe("V3 original resource groups", () => {
  it("keeps all declared AppData group fields and independent namespaces", () => {
    expect(resourceGroupMap.declared_group_ids).toEqual([
      "resChip_",
      "resInterface_",
      "resHuman_",
      "resCom_",
      "resGame_",
      "resEffect_",
      "resMeeting_",
      "resAvatarBody_",
      "resAvatarHead_",
      "resDevelop_",
      "resWindow_",
    ]);
    const appData = createVisualAppData();
    expect(appData.resChip_.groupId).toBe("resChip_");
    expect(appData.resHuman_.groupId).toBe("resHuman_");
    expect(appData.resChip_.img).not.toBe(appData.resHuman_.img);
    expect(appData.resInterface_.img).toHaveLength(0);
    expect(appData.getResourceManager("resAvatarHead_").groupId).toBe("resAvatarHead_");
  });

  it("resolves furniture and preserves source-index IDs and TexId", () => {
    const manager = createResourceManager("resChip_");
    expect(manager.getImage(4).sourceMember).toBe("01_GAME_PACKS/chip/chair_00.png");
    expect(manager.getSeb(3).getMaxFrame()).toBeGreaterThan(0);
    expect(manager.resolveSebImage(3, 0, 0)).toMatchObject({ status: "resolved", texId: 4 });
    expect(manager.getImage(3).sourceMember).toBe("01_GAME_PACKS/chip/desk_00.png");
    expect(manager.getImage(7).sourceMember).toBe("01_GAME_PACKS/chip/door_01.png");
  });

  it("resolves human, avatar, game, effect, meeting, develop, and window fixtures", () => {
    const cases = [
      ["resHuman_", 0, 11, "01_GAME_PACKS/human/chara00.png"],
      ["resAvatarBody_", 0, 0, "01_GAME_PACKS/avatar_body/m_00.png"],
      ["resGame_", 5, 1, "01_GAME_PACKS/game/cloud_day.png"],
      ["resEffect_", 0, 0, "01_GAME_PACKS/effect/effect00.png"],
      ["resMeeting_", 2, 0, "01_GAME_PACKS/meeting/hit_effect.png"],
      ["resDevelop_", 0, 0, "01_GAME_PACKS/develop/enemy_attack_timing.png"],
      ["resWindow_", 0, 0, "01_GAME_PACKS/window/install_bonus.png"],
    ] as const;
    for (const [groupId, imageId, sebId, sourceMember] of cases) {
      const manager = createResourceManager(groupId);
      expect(manager.getImage(imageId).sourceMember).toBe(sourceMember);
      expect(manager.getSeb(sebId).getMaxFrame()).toBeGreaterThan(0);
      const frame = groupId === "resEffect_" ? 2 : 0;
      const layer = groupId === "resEffect_" ? 2 : 0;
      expect(manager.resolveSebImage(sebId, frame, layer).status).toBe("resolved");
    }
    expect(createResourceManager("resAvatarHead_").getImage(0).sourceMember)
      .toBe("01_GAME_PACKS/avatar_head/face_m_00.png");
  });

  it("keeps the common-window alias and negative SEB sentinel explicit", () => {
    const common = createResourceManager("resCom_");
    expect(common.getImage(5).sourceMember).toBe("01_GAME_PACKS/com/wnd_conner.png");
    expect(common.getImage(19).sourceMember).toBe("01_GAME_PACKS/com/wnd_conner.png");
    expect(common.getImage(5)).not.toBe(common.getImage(19));
    expect(common.resolveSebImage(0, 0, 0)).toMatchObject({ status: "resolved", texId: 19 });

    const chip = createResourceManager("resChip_");
    expect(chip.resolveSebImage(5, 2, 1)).toMatchObject({ status: "sentinel", texId: -1, image: null });
    expect(chip.resolveSebImage(5, 1, 0)).toMatchObject({ status: "resolved", texId: 6 });
  });

  it("preserves sparse gaps and rejects invalid or missing IDs", () => {
    const game = createResourceManager("resGame_");
    expect(game.img).toHaveLength(72);
    expect(game.img[1]).toBeNull();
    expect(() => game.getImage(1)).toThrowError(V3LookupError);
    expect(() => game.getImage(72)).toThrowError(V3LookupError);
    expect(() => game.getImage(-1)).toThrowError(V3LookupError);
    expect(() => game.getImage(1.5)).toThrowError(V3LookupError);

    const interfaceManager = createResourceManager("resInterface_");
    expect(() => interfaceManager.getImage(0)).toThrowError(V3LookupError);
    expect(() => createResourceManager("resAvatarHead_").getSeb(0)).toThrowError(V3LookupError);
  });

  it("keeps load aliases, custom-image emptiness, atlas deferral, and lifetime bounded", () => {
    const manager = createResourceManager("resHuman_");
    expect(manager.loadImage(0)).toBe(manager.getImage(0));
    expect(manager.loadSeb(11)).toBe(manager.getSeb(11));
    expect(manager.loadReady()).toBe(manager);
    expect(manager.loadStart()).toBe(manager);
    expect(manager.customImages.size).toBe(0);
    expect(manager.getCustomImage(0)).toBeNull();
    expect(() => manager.getAtlas(0)).toThrowError(V3DeferredError);
    const image = manager.getImage(0);
    image.use();
    image.use();
    expect(image.getUseCount()).toBe(2);
    image.unuse();
    image.unuse();
    image.unuse();
    expect(image.getUseCount()).toBe(0);
    expect(manager.atlasStatus).toBe("deferred");
  });

  it("covers real source hashes, deterministic contracts, and the V1/V2 regression boundary", () => {
    expect(fixtureManifest.status).toBe("PASS_REAL_SOURCE_INDEXED_MULTI_GROUP_FIXTURES");
    expect(fixtureManifest.fixtures.length).toBeGreaterThanOrEqual(13);
    expect(imgIndex.groups).toHaveLength(10);
    expect(sebIndex.groups).toHaveLength(9);
    expect(imgIndex.determinism.content_hash).toMatch(/^[a-f0-9]{64}$/);
    expect(sebIndex.determinism.content_hash).toMatch(/^[a-f0-9]{64}$/);
    expect(imageSebAssociation.cross_group_exceptions).toEqual([]);
    expect(imageSebAssociation.associations).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ fixture_id: "resChip_:chair_00", status: "PROVEN_SAME_PACK_INDEX_NAMESPACE" }),
        expect.objectContaining({ fixture_id: "resCom_:wnd_conner", tex_ids: [19] }),
      ]),
    );
    expect(groupCoverage.coverage_categories).toEqual(
      expect.arrayContaining(["PROVEN_BOTH", "PROVEN_SOURCE_INDEXED", "DECLARED_ONLY", "SENTINEL", "DEFERRED"]),
    );
    expect(v1Lookup.group_ids).toHaveLength(11);
    expect(v2Acceptance.status).toBe("PASS_STATIC");
    expect(v2Acceptance.v2_entry_gate_for_v3).toBe("PASS");
    expect(v2Acceptance.pixel_parity).toBe("DEFERRED_TO_V7");
    expect(checkpointLedger.status).toBe("PASS_STATIC_V3_STOP_BEFORE_V4");
    expect(checkpointLedger.checkpoints).toHaveLength(11);
    expect(checkpointLedger.checkpoints.at(-1)?.status).toBe("PASS");
  });

  it("keeps additional title and recruit owners separate from AppData visual groups", () => {
    const title = createAdditionalResourceManager("resTitle_");
    const recruit = createAdditionalResourceManager("resRecruit_");
    expect(title.getImage(2).sourceMember).toBe("01_GAME_PACKS/title/title_menu.png");
    expect(title.resolveSebImage(0, 0, 0).texId).toBe(2);
    expect(recruit.getImage(0).sourceMember).toBe("01_GAME_PACKS/recruit/hope_join_back.png");
    expect(recruit.resolveSebImage(0, 0, 0).texId).toBe(0);
  });
});
