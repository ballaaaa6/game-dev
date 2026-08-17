import { describe, expect, it } from "vitest";
import { GraphicsCompatibility } from "../src/v2/graphics";
import {
  createV4Camera,
  createV4FurnitureBinding,
  createV4ResourceManager,
  getV4FixtureManifest,
} from "../src/v4/fixture-loader";
import type { V4CommandTrace } from "../src/v4/contracts";
import { drawFurnitureBinding } from "../src/v4/furniture";
import { renderMapChip } from "../src/v4/map-chip";
import { objChipOrigin, renderObjChip } from "../src/v4/obj-chip";

describe("V4 regression boundaries", () => {
  it("preserves V3 resource-group identity and numeric slots after V4 drawing", () => {
    const resources = createV4ResourceManager();
    const image85 = resources.manager.getImage(85);
    const seb63 = resources.manager.getSeb(63);

    const result = renderMapChip(
      { cell: [5, 5], imageId: 85, roomFloor: 0, roomWidth: 14, roomHeight: 14 },
      resources,
      createV4Camera(),
    );

    expect(result.commands).toHaveLength(1);
    expect(resources.groupId).toBe("resChip_");
    expect(resources.manager.loadState).toBe("ready_static_fixture");
    expect(resources.manager.getImage(85)).toBe(image85);
    expect(resources.manager.getSeb(63)).toBe(seb63);
    expect(resources.manager.img[5] ?? null).toBeNull();
  });

  it("keeps the explicit floor alias at selector 85 instead of rewriting it to 5", () => {
    const manifest = getV4FixtureManifest();
    const resources = createV4ResourceManager();
    expect(manifest.map.floor_image_selector).toBe(85);
    expect(resources.resolveImage(manifest.map.floor_image_selector).ref.id).toBe("resChip_:image:85");
  });

  it("retains exact native furniture 3 primary and secondary destinations", () => {
    const result = renderObjChip(
      {
        cell: [2, 4],
        rawType: 2,
        rawDirection: 0,
        roomWidth: 10,
        roomHeight: 10,
        wallImageId: 6,
        doorImageId: 7,
        furnitureBinding: createV4FurnitureBinding("furniture:3"),
      },
      createV4ResourceManager(),
      createV4Camera(),
    );

    expect(result.commands).toHaveLength(2);
    expect(result.commands.map((command) => command.image.id)).toEqual([
      "resChip_:image:3",
      "resChip_:image:4",
    ]);
    expect(result.commands.map((command) => command.destination)).toEqual([
      { x: 111, y: 16, width: 60, height: 32 },
      { x: 120, y: 14, width: 60, height: 32 },
    ]);
  });

  it("keeps direct-image fixtures distinct from FurnitureData catalogue sentinels", () => {
    const manifest = getV4FixtureManifest();
    const resources = createV4ResourceManager();
    const catalogue = manifest.catalog_selector_fixtures.find((fixture) => fixture.furniture_data_id === 0);
    expect(catalogue?.selectors.img).toBe(-1);

    const directFixtures = [
      { objectId: "furniture:12", cell: [8, 5] as const, destination: { x: 248, y: -40, width: 24, height: 22 } },
      { objectId: "furniture:26", cell: [8, 6] as const, destination: { x: 269, y: -34, width: 23, height: 26 } },
      { objectId: "furniture:56", cell: [2, 7] as const, destination: { x: 168, y: 34, width: 24, height: 28 } },
    ];
    for (const fixture of directFixtures) {
      const binding = createV4FurnitureBinding(fixture.objectId);
      const graphics = new GraphicsCompatibility();
      const traces: V4CommandTrace[] = [];
      drawFurnitureBinding(binding, objChipOrigin(fixture.cell, createV4Camera()), resources, graphics, traces);
      expect(graphics.commands).toHaveLength(1);
      expect(graphics.commands[0].image.id).toBe(`resChip_:image:${binding.imageSelector}`);
      expect(graphics.commands[0].destination).toEqual(fixture.destination);
      expect(traces[0].resource.id).toBe(binding.imageSelector);
      expect(binding.dataImage).toBe(binding.imageSelector);
    }
  });
});
