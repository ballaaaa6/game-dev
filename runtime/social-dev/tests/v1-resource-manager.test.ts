import { describe, expect, it } from "vitest";

import resourceEvidenceJson from "../../../knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json";

import type { ResourceLookupEvidenceContract } from "../src/v1/contracts";
import { V1DeferredError, V1LookupError } from "../src/v1/errors";
import { loadResourceGroup } from "../src/v1/fixture-loader";
import { Image } from "../src/v1/image";
import { ResourceManager } from "../src/v1/resource-manager";
import { Seb } from "../src/v1/seb";

const evidence = resourceEvidenceJson as unknown as ResourceLookupEvidenceContract;

describe("ResourceManager group lookup", () => {
  it("preserves the exact eleven visual AppData group IDs", () => {
    expect(evidence.group_ids).toEqual([
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
    expect(evidence.group_ids).toHaveLength(11);
  });

  it("resolves the proven resChip_ image and SEB IDs through sparse arrays", () => {
    const { manager, fixture } = loadResourceGroup("resChip_");

    expect(manager.groupId).toBe("resChip_");
    expect(fixture?.fixture_id).toBe("resChip_:chair_00");
    expect(manager.seb[fixture?.seb_id ?? -1]).toBeInstanceOf(Seb);
    expect(manager.img[fixture?.image_id ?? -1]).toBeInstanceOf(Image);
    expect(manager.getSeb(fixture?.seb_id ?? -1)).toBe(manager.seb[fixture?.seb_id ?? -1]);
    expect(manager.getImage(fixture?.image_id ?? -1)).toBe(manager.img[fixture?.image_id ?? -1]);
    expect(manager.getImage(4)?.sourceMember).toBe("01_GAME_PACKS/chip/chair_00.png");
    expect(manager.getSeb(3)?.getMaxFrame()).toBe(3);
  });

  it("keeps missing IDs and cross-group fallback explicit", () => {
    const { manager } = loadResourceGroup("resChip_");

    expect(() => manager.getImage(999)).toThrowError(V1LookupError);
    expect(() => manager.getSeb(999)).toThrowError(V1LookupError);
    expectCode(() => manager.getImage(1), "RESOURCE_IMAGE_NOT_FOUND");
    expectCode(() => manager.getSeb(11), "RESOURCE_SEB_NOT_FOUND");
  });

  it("keeps atlas behavior deferred because selected fixtures have no atlas region", () => {
    const { manager } = loadResourceGroup("resChip_");

    expect(evidence.atlas_contract.status).toBe("deferred");
    expect(manager.atlasStatus).toBe("deferred");
    expect(() => manager.getAtlas(0)).toThrowError(V1DeferredError);
    try {
      manager.getAtlas(0);
    } catch (error) {
      expect((error as V1DeferredError).code).toBe("RESOURCE_ATLAS_DEFERRED");
    }
  });

  it("constructs an empty declared group without borrowing another group", () => {
    const group = evidence.groups.find((candidate) => candidate.group_id === "resInterface_");
    expect(group).toBeDefined();
    const manager = ResourceManager.fromContract(group!);
    expect(manager.groupId).toBe("resInterface_");
    expect(manager.img).toEqual([]);
    expect(manager.seb).toEqual([]);
    expectCode(() => manager.getImage(0), "RESOURCE_IMAGE_NOT_FOUND");
    expectCode(() => manager.getSeb(0), "RESOURCE_SEB_NOT_FOUND");
  });
});

function expectCode(action: () => unknown, code: string): void {
  try {
    action();
    throw new Error(`expected ${code}`);
  } catch (error) {
    expect((error as { readonly code?: string }).code).toBe(code);
  }
}
