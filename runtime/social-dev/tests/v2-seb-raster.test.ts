import { describe, expect, it } from "vitest";

import { loadResourceGroup } from "../src/v1/fixture-loader";
import type { ResourceManager } from "../src/v1/resource-manager";
import { Seb } from "../src/v1/seb";
import { V2DeferredError } from "../src/v2/errors";
import { GraphicsBlend, GraphicsCompatibility, GraphicsOperation, packArgb } from "../src/v2/graphics";
import { applySebBlendMode, drawSeb, renderSeb } from "../src/v2/seb-raster";

describe("V2 SEB raster composition contract", () => {
  it("routes a wrapped manager frame through the V1 Seb and Image records", () => {
    const { manager } = loadResourceGroup("resChip_");
    const graphics = new GraphicsCompatibility();
    const result = drawSeb(manager, graphics, 10, 20, 3, { frame: 4 });
    const sprite = manager.getSeb(3).getSprite(1, 0);

    expect(sprite).not.toBeNull();
    expect(result).toEqual({ sebId: 3, frame: 1, layer: null, commandCount: 1 });
    expect(graphics.commands[0]).toMatchObject({
      image: { id: manager.getImage(sprite!.TexId).sourceMember },
      destination: {
        x: 10 + sprite!.TransX,
        y: 20 + sprite!.TransY,
        width: sprite!.W,
        height: sprite!.H,
      },
      source: { x: sprite!.U, y: sprite!.V, width: sprite!.W, height: sprite!.H },
    });
  });

  it("keeps multi-layer source order while skipping native TEXID_NONE records", () => {
    const { manager } = loadResourceGroup("resChip_");
    const graphics = new GraphicsCompatibility();
    const result = drawSeb(manager, graphics, 0, 0, 5, { frame: 2 });

    expect(result).toEqual({ sebId: 5, frame: 2, layer: null, commandCount: 1 });
    expect(graphics.commands[0]?.image.id).toBe("01_GAME_PACKS/chip/wall_00.png");

    graphics.clearCommands();
    expect(drawSeb(manager, graphics, 0, 0, 5, { frame: 2, layer: 1 }).commandCount).toBe(0);
  });

  it.each([
    [1, "01_GAME_PACKS/chip/desk_00.png"],
    [6, "01_GAME_PACKS/chip/door_01.png"],
  ] as const)("resolves furniture source slot %s through the ResourceManager contract", (sebId, imageMember) => {
    const { manager } = loadResourceGroup("resChip_");
    const graphics = new GraphicsCompatibility();

    expect(drawSeb(manager, graphics, 0, 0, sebId, { frame: 0 }).commandCount).toBe(1);
    expect(graphics.commands[0]?.image.id).toBe(imageMember);
  });

  it("records ReverseU on the draw and restores flip state for the next sprite", () => {
    const { manager } = loadResourceGroup("resHuman_");
    const graphics = new GraphicsCompatibility();
    const result = drawSeb(manager, graphics, 3, 4, 11, { frame: 0 });

    expect(result.commandCount).toBe(1);
    expect(graphics.commands[0]?.state.flipMode).toBe(1);
    expect(graphics.getFlipMode()).toBe(0);
  });

  it("skips the native hidden SEB sentinels", () => {
    const hiddenSeb = Seb.fromContract({
      status: "pass",
      grammar: "seb-layered-v1",
      header: { layer_count: 1, global_frame_count: 1, record_count: 1, frame_bound: 1 },
      layers: [{
        index: 0,
        layer: 0,
        record_count: 1,
        frame_bound: 1,
        marker: null,
        records: [{
          layer: 0,
          layer_record_index: 0,
          start_frame: 0,
          image_id: -8,
          image_id_raw: 0xfff8,
          source_x: 0,
          source_y: 0,
          width: 1,
          height: 1,
          destination_x: 0,
          destination_y: 0,
          flags: 0,
          reserved: 0,
          frame_status: "in_header_frame_bound",
        }],
      }],
      records: [{
        layer: 0,
        layer_record_index: 0,
        start_frame: 0,
        image_id: -8,
        image_id_raw: 0xfff8,
        source_x: 0,
        source_y: 0,
        width: 1,
        height: 1,
        destination_x: 0,
        destination_y: 0,
        flags: 0,
        reserved: 0,
        frame_status: "in_header_frame_bound",
      }],
      trailing_bytes: 0,
      metadata_warnings: [],
    });
    const manager = {
      getSeb: () => hiddenSeb,
      getImage: () => { throw new Error("hidden sentinel must not resolve an image"); },
      fixtures: [],
    } as unknown as ResourceManager;
    const graphics = new GraphicsCompatibility();

    expect(drawSeb(manager, graphics, 0, 0, 0, { frame: 0 }).commandCount).toBe(0);
  });

  it("maps all proven Seb blend flags to native render-mode pushes", () => {
    const cases = [
      [GraphicsBlend.COLOR, GraphicsOperation.ADD, 120, 135],
      [GraphicsBlend.LIGHT, GraphicsOperation.ADD, 120, 255],
      [GraphicsBlend.GRAYSCALE, GraphicsOperation.SUBTRACT, 120, 255],
    ] as const;

    for (const [blend, operator, sourceRatio, destinationRatio] of cases) {
      const graphics = new GraphicsCompatibility();
      applySebBlendMode(graphics, blend, packArgb(0, 0, 0, 120));
      expect([graphics.getRenderModeOperator(), graphics.getRenderModeSrcRatio(), graphics.getRenderModeDstRatio()])
        .toEqual([operator, sourceRatio, destinationRatio]);
      graphics.popRenderMode();
      expect(graphics.getRenderModeOperator()).toBe(GraphicsOperation.REPLACE);
    }
  });

  it("defers depth-aware RenderSeb until native depth payload is available", () => {
    expect(() => renderSeb()).toThrowError(V2DeferredError);
    try {
      renderSeb();
    } catch (error) {
      expect((error as V2DeferredError).code).toBe("V2_SEB_DEPTH_UNPROVEN");
    }
  });
});
