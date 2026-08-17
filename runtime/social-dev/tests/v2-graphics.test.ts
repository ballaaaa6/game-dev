import { describe, expect, it } from "vitest";

import {
  GraphicsBlend,
  GraphicsCompatibility,
  GraphicsFlip,
  GraphicsOperation,
  imageRef,
  packArgb,
  scaleAlphaByRatio,
  unpackArgb,
} from "../src/v2/graphics";

describe("V2 Graphics compatibility contract", () => {
  it("starts with the native ResetRender state", () => {
    const graphics = new GraphicsCompatibility();

    expect(graphics.getState()).toMatchObject({
      clip: null,
      clipDepth: 0,
      flipMode: GraphicsFlip.NONE,
      linearFilter: false,
      color: packArgb(0, 0, 0, 255),
      scalePercent: 100,
      renderMode: {
        operator: GraphicsOperation.REPLACE,
        sourceRatio: 255,
        destinationRatio: 0,
        isReplace: true,
      },
      blendMode: GraphicsBlend.NONE,
      blendColor: 0,
    });
  });

  it("preserves crop and scaled DrawImage source/destination geometry, including negatives", () => {
    const graphics = new GraphicsCompatibility();
    const image = imageRef("fixture-image", 64, 32);

    graphics.setFlipMode(GraphicsFlip.HORIZONTAL);
    graphics.drawImage(image, 1, 2);
    graphics.drawImage(image, -3.5, 4.5, -2, -1, 7, 8);
    graphics.drawScaledImage(image, 10, 11, 20, 21, 1, 2, 3, 4);

    expect(graphics.commands).toHaveLength(3);
    expect(graphics.commands[0]).toMatchObject({
      kind: "draw-image",
      destination: { x: 1, y: 2, width: 64, height: 32 },
      source: { x: 0, y: 0, width: 64, height: 32 },
    });
    expect(graphics.commands[1]).toMatchObject({
      kind: "draw-image",
      destination: { x: -3.5, y: 4.5, width: 7, height: 8 },
      source: { x: -2, y: -1, width: 7, height: 8 },
      state: { flipMode: GraphicsFlip.HORIZONTAL },
    });
    expect(graphics.commands[2]).toMatchObject({
      kind: "draw-scaled-image",
      destination: { x: 10, y: 11, width: 20, height: 21 },
      source: { x: 1, y: 2, width: 3, height: 4 },
      state: { flipMode: GraphicsFlip.HORIZONTAL },
    });
  });

  it("intersects and stacks clips with native integer GetClip conversion", () => {
    const graphics = new GraphicsCompatibility();

    graphics.setClip(1.9, 2.8, 10.9, 20.1);
    graphics.clipRect(4, 5, 20, 20, false);
    expect(graphics.getClip()).toEqual([4, 5, 8, 17]);

    graphics.pushClip();
    graphics.setClip(0, 0, 2, 3);
    graphics.popClip();
    expect(graphics.getClip()).toEqual([4, 5, 8, 17]);

    graphics.clearClip();
    expect(graphics.getClip()).toBeNull();
  });

  it("recovers packed color, scale, filter, render, blend, and alpha-ratio state", () => {
    const graphics = new GraphicsCompatibility();

    graphics.setColor(-4, 20, 300, 128);
    expect(unpackArgb(graphics.getColor())).toEqual({ red: 0, green: 20, blue: 255, alpha: 128 });
    graphics.scale(75);
    graphics.linearFilterEnabled(true);
    graphics.setRenderMode(GraphicsOperation.ADD, 120);
    expect([graphics.getRenderModeOperator(), graphics.getRenderModeSrcRatio(), graphics.getRenderModeDstRatio()])
      .toEqual([GraphicsOperation.ADD, 120, 135]);

    graphics.pushRenderMode(GraphicsOperation.SUBTRACT, 80, 255);
    graphics.popRenderMode();
    expect(graphics.getRenderModeOperator()).toBe(GraphicsOperation.ADD);

    graphics.setBlendMode(GraphicsBlend.COLOR, packArgb(1, 2, 3, 4));
    expect(graphics.getBlendMode()).toBe(GraphicsBlend.COLOR);
    expect(unpackArgb(graphics.getBlendColor())).toEqual({ red: 1, green: 2, blue: 3, alpha: 4 });
    expect(scaleAlphaByRatio(128, 255)).toBe(128);
    expect(scaleAlphaByRatio(128, 120)).toBe(60);
    expect(graphics.getScale()).toBe(75);
    expect(graphics.isLinearFilter()).toBe(true);
  });

  it("preserves native LinearFilter state across ResetRender", () => {
    const graphics = new GraphicsCompatibility();

    graphics.linearFilterEnabled(true);
    graphics.setColor(1, 2, 3, 4);
    graphics.setFlipMode(GraphicsFlip.VERTICAL);
    graphics.resetRender();

    expect(graphics.isLinearFilter()).toBe(true);
    expect(graphics.getFlipMode()).toBe(GraphicsFlip.NONE);
    expect(graphics.getColor()).toBe(packArgb(0, 0, 0, 255));
  });
});
