import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import { GraphicsCompatibility, imageRef, packArgb } from "../src/v2/graphics";
import { createV6RoomStaffPreview } from "../src/v6";
import { createRoomV5 } from "../src/v5";
import {
  createDefaultRasterState,
  diffRasterV7,
  encodePngRgbaV7,
  makeDiffSurfaceV7,
  RasterCompatibilityV7,
  RasterSurfaceCompatibilityV7,
  renderV7Commands,
} from "../src/v7";
import type { GraphicsCommand, GraphicsImageRef, GraphicsStateSnapshot } from "../src/v2/graphics";
import type { V7RasterImage } from "../src/v7";

const QUADRANT_IMAGE: V7RasterImage = {
  id: "quadrant",
  width: 2,
  height: 2,
  pixels: new Uint8Array([
    255, 0, 0, 255,
    0, 255, 0, 255,
    0, 0, 255, 255,
    255, 255, 255, 255,
  ]),
};

function commandFor(
  image: GraphicsImageRef,
  destination: [number, number, number, number],
  source: [number, number, number, number] = [0, 0, image.width, image.height],
  configure?: (graphics: GraphicsCompatibility) => void,
): GraphicsCommand {
  const graphics = new GraphicsCompatibility();
  configure?.(graphics);
  if (destination[2] === source[2] && destination[3] === source[3]) {
    graphics.drawImage(image, destination[0], destination[1], source[0], source[1], source[2], source[3]);
  } else {
    graphics.drawScaledImage(
      image,
      destination[0],
      destination[1],
      destination[2],
      destination[3],
      source[0],
      source[1],
      source[2],
      source[3],
    );
  }
  const command = graphics.commands[0];
  if (command === undefined) {
    throw new Error("test command was not recorded");
  }
  return command;
}

function renderCommand(command: GraphicsCommand, image = QUADRANT_IMAGE): RasterSurfaceCompatibilityV7 {
  const map = new Map([[String(command.image.id), image]]);
  return renderV7Commands([command], map, { width: 8, height: 8 }).surface as RasterSurfaceCompatibilityV7;
}

function pixel(surface: RasterSurfaceCompatibilityV7, x: number, y: number): readonly [number, number, number, number] {
  return surface.getPixel(x, y);
}

describe("V7 RasterCompatibility selected contract", () => {
  it("keeps the recovered default state identity-compatible", () => {
    const state = createDefaultRasterState();
    expect(state.flipMode).toBe(0);
    expect(state.scalePercent).toBe(100);
    expect(state.linearFilter).toBe(false);
    expect(state.renderMode).toMatchObject({ operator: 0, sourceRatio: 255, destinationRatio: 0 });
  });

  it("copies a source crop to an equal destination with stable nearest sampling", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2]);
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([255, 0, 0, 255]);
    expect(pixel(surface, 1, 0)).toEqual([0, 255, 0, 255]);
    expect(pixel(surface, 0, 1)).toEqual([0, 0, 255, 255]);
    expect(pixel(surface, 1, 1)).toEqual([255, 255, 255, 255]);
  });

  it("preserves crop and destination dimensions independently", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [1, 1, 4, 2], [0, 0, 2, 1]);
    const surface = renderCommand(command);
    expect(pixel(surface, 1, 1)).toEqual([255, 0, 0, 255]);
    expect(pixel(surface, 4, 1)).toEqual([0, 255, 0, 255]);
    expect(pixel(surface, 1, 2)).toEqual([255, 0, 0, 255]);
    expect(pixel(surface, 1, 3)).toEqual([0, 0, 0, 0]);
  });

  it("clips negative destination geometry at the surface boundary", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [-1, -1, 2, 2]);
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([255, 255, 255, 255]);
    expect(surface.nonTransparentBounds()).toEqual({ x: 0, y: 0, width: 1, height: 1 });
  });

  it("applies an explicit axis-aligned clip", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], undefined, (graphics) => {
      graphics.setClip(1, 0, 1, 2);
    });
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([0, 0, 0, 0]);
    expect(pixel(surface, 1, 0)).toEqual([0, 255, 0, 255]);
  });

  it("keeps clip intersection state deterministic", () => {
    const graphics = new GraphicsCompatibility();
    graphics.clipRect(0, 0, 3, 3);
    graphics.clipRect(1, 1, 3, 3, false);
    expect(graphics.getClip()).toEqual([1, 1, 2, 2]);
    graphics.popClip();
    expect(graphics.getClip()).toBeNull();
  });

  it("applies transformed clipping as a polygon, not a browser default", () => {
    const raster = new RasterCompatibilityV7({ width: 8, height: 8 });
    const state = createDefaultRasterState();
    raster.draw({
      image: QUADRANT_IMAGE,
      destination: { x: 0, y: 0, width: 4, height: 4 },
      source: { x: 0, y: 0, width: 2, height: 2 },
      state,
      clip: {
        rect: { x: 1, y: 1, width: 2, height: 2 },
        transformed: { scaleX: 2, scaleY: 1, pivot: { x: 2, y: 2 } },
      },
    });
    expect(raster.output.nonTransparentBounds()).toEqual({ x: 0, y: 1, width: 4, height: 2 });
  });

  it("flips horizontally around the destination center", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], undefined, (graphics) => graphics.setFlipMode(1));
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([0, 255, 0, 255]);
    expect(pixel(surface, 1, 0)).toEqual([255, 0, 0, 255]);
  });

  it("flips vertically around the destination center", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], undefined, (graphics) => graphics.setFlipMode(2));
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([0, 0, 255, 255]);
    expect(pixel(surface, 0, 1)).toEqual([255, 0, 0, 255]);
  });

  it("flips both axes without inventing a filename or alternate image", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], undefined, (graphics) => graphics.setFlipMode(3));
    const surface = renderCommand(command);
    expect(pixel(surface, 0, 0)).toEqual([255, 255, 255, 255]);
    expect(pixel(surface, 1, 1)).toEqual([255, 0, 0, 255]);
  });

  it("supports the two recovered rotate branches with explicit compatibility orientation", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [1, 1, 2, 2], undefined, (graphics) => graphics.setFlipMode(4));
    const surface = renderCommand(command);
    expect(surface.nonTransparentBounds()).toEqual({ x: 1, y: 1, width: 2, height: 2 });
  });

  it("applies percent scale around the destination pivot", () => {
    const raster = new RasterCompatibilityV7({ width: 8, height: 8 });
    const graphics = new GraphicsCompatibility();
    graphics.scale(200);
    graphics.drawImage(imageRef("quadrant", 2, 2), 2, 2, 0, 0, 2, 2);
    raster.render(graphics.commands, new Map([["quadrant", QUADRANT_IMAGE]]));
    expect(raster.output.nonTransparentBounds()).toEqual({ x: 1, y: 1, width: 4, height: 4 });
  });

  it("keeps linear filtering explicit and deterministic", () => {
    const nearest = renderCommand(commandFor(imageRef("quadrant", 2, 2), [0, 0, 5, 5]));
    const linear = renderCommand(commandFor(imageRef("quadrant", 2, 2), [0, 0, 5, 5], undefined, (graphics) => graphics.linearFilterEnabled(true)));
    expect(linear.getPixel(2, 2)).not.toEqual(nearest.getPixel(2, 2));
    expect(linear.getPixel(2, 2)[3]).toBeGreaterThan(0);
  });

  it("packs explicit color channels and alpha without changing the command geometry", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], undefined, (graphics) => graphics.setColor(255, 0, 0, 128));
    const surface = renderCommand(command);
    expect(surface.getPixel(0, 0)).toEqual([255, 0, 0, 128]);
    expect(command.destination).toEqual({ x: 0, y: 0, width: 2, height: 2 });
  });

  it("applies alpha through the recovered source/destination render ratios", () => {
    const base = new RasterSurfaceCompatibilityV7(2, 2, [0, 0, 255, 255]);
    const raster = new RasterCompatibilityV7({ width: 2, height: 2 });
    raster.output.pixels.set(base.pixels);
    const graphics = new GraphicsCompatibility();
    graphics.setRenderMode(1, 128, 127);
    graphics.drawImage(imageRef("quadrant", 2, 2), 0, 0);
    raster.render(graphics.commands, new Map([["quadrant", QUADRANT_IMAGE]]));
    expect(raster.output.getPixel(0, 0)[0]).toBeGreaterThan(100);
    expect(raster.output.getPixel(0, 0)[2]).toBeGreaterThan(100);
  });

  it("supports subtract render mode with clamped channels", () => {
    const raster = new RasterCompatibilityV7({ width: 2, height: 2, background: [10, 10, 10, 255] });
    const graphics = new GraphicsCompatibility();
    graphics.setRenderMode(2, 255, 255);
    graphics.drawImage(imageRef("quadrant", 2, 2), 0, 0);
    raster.render(graphics.commands, new Map([["quadrant", QUADRANT_IMAGE]]));
    expect(raster.output.getPixel(0, 0)).toEqual([245, 0, 0, 0]);
  });

  it("supports color, light, and grayscale blend states", () => {
    const color = new GraphicsCompatibility();
    color.setBlendMode(1, packArgb(0, 255, 0, 255));
    color.drawImage(imageRef("quadrant", 2, 2), 0, 0);
    expect(renderCommand(color.commands[0]!).getPixel(0, 0)).toEqual([0, 0, 0, 255]);

    const light = new GraphicsCompatibility();
    light.setBlendMode(2, packArgb(10, 20, 30, 255));
    light.drawImage(imageRef("quadrant", 2, 2), 0, 0);
    expect(renderCommand(light.commands[0]!).getPixel(0, 0)).toEqual([255, 20, 30, 255]);

    const grayscale = new GraphicsCompatibility();
    grayscale.setBlendMode(3, 0);
    grayscale.drawImage(imageRef("quadrant", 2, 2), 0, 0);
    expect(renderCommand(grayscale.commands[0]!).getPixel(0, 0)[0]).toBe(76);
  });

  it("keeps fully transparent source pixels transparent under replace", () => {
    const image: V7RasterImage = { ...QUADRANT_IMAGE, pixels: new Uint8Array(16) };
    const surface = renderCommand(commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2]), image);
    expect(surface.nonTransparentBounds()).toBeNull();
  });

  it("preserves an existing destination under a transparent replace fragment", () => {
    const raster = new RasterCompatibilityV7({ width: 1, height: 1 });
    raster.output.setPixel(0, 0, [12, 34, 56, 255]);
    const transparent: V7RasterImage = {
      id: "transparent",
      width: 1,
      height: 1,
      pixels: new Uint8Array([0, 0, 0, 0]),
    };
    raster.render([commandFor(imageRef("transparent", 1, 1), [0, 0, 1, 1])], new Map([["transparent", transparent]]));
    expect(raster.output.getPixel(0, 0)).toEqual([12, 34, 56, 255]);
  });

  it("treats out-of-bounds source samples as transparent compatibility pixels", () => {
    const command = commandFor(imageRef("quadrant", 2, 2), [0, 0, 2, 2], [-1, -1, 2, 2]);
    const surface = renderCommand(command);
    expect(surface.getPixel(0, 0)).toEqual([0, 0, 0, 0]);
    expect(surface.getPixel(1, 1)).toEqual([255, 0, 0, 255]);
  });

  it("encodes deterministic PNG bytes without timestamps or ancillary chunks", () => {
    const surface = new RasterSurfaceCompatibilityV7(2, 1);
    surface.setPixel(0, 0, [255, 0, 0, 255]);
    surface.setPixel(1, 0, [0, 0, 0, 0]);
    const first = encodePngRgbaV7(surface);
    const second = encodePngRgbaV7(surface);
    expect(Buffer.from(first).equals(Buffer.from(second))).toBe(true);
    expect(createHash("sha256").update(first).digest("hex")).toBe(createHash("sha256").update(second).digest("hex"));
    expect(Buffer.from(first).subarray(0, 8)).toEqual(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  });

  it("reports changed pixels, maximum channel error, and changed bounds", () => {
    const left = new RasterSurfaceCompatibilityV7(3, 2);
    const right = left.clone();
    right.setPixel(1, 0, [255, 0, 0, 255]);
    const diff = diffRasterV7(left, right);
    expect(diff).toMatchObject({ changedPixelCount: 1, maxChannelError: 255, changedRegion: { x: 1, y: 0, width: 1, height: 1 }, identical: false });
    expect(makeDiffSurfaceV7(left, right).getPixel(1, 0)).toEqual([255, 0, 0, 255]);
  });

  it("renders the complete V5 structural command stream byte-stably", () => {
    const room = createRoomV5("room:0", { visualScope: "full_static" }).draw();
    const imageMap = new Map<string, V7RasterImage>();
    for (const command of room.commands) {
      const key = String(command.image.id);
      if (!imageMap.has(key)) {
        imageMap.set(key, proceduralImage(command.image));
      }
    }
    const first = renderV7Commands(room.commands, imageMap);
    const second = renderV7Commands(room.commands, imageMap);
    expect(Buffer.from(encodePngRgbaV7(first.surface)).equals(Buffer.from(encodePngRgbaV7(second.surface)))).toBe(true);
    expect(first.drawCount).toBeGreaterThan(0);
  });

  it("renders the integrated V6 room plus three Staff commands without changing V6 counts", () => {
    const manifest = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "right", frame: 0, alpha: 255 });
    const imageMap = new Map<string, V7RasterImage>();
    for (const command of manifest.commands) {
      const key = String(command.image.id);
      if (!imageMap.has(key)) {
        imageMap.set(key, proceduralImage(command.image));
      }
    }
    const raster = renderV7Commands(manifest.commands, imageMap);
    expect(manifest.commands).toHaveLength(142);
    expect(manifest.traces).toHaveLength(127);
    expect(manifest.events).toHaveLength(791);
    expect(raster.nonTransparentBounds).not.toBeNull();
  });

  it("uses source dimensions and command identities rather than filenames in the raster map", () => {
    const image = proceduralImage({ id: "same-id", width: 3, height: 4 });
    expect(image.id).toBe("same-id");
    expect(image.width).toBe(3);
    expect(image.height).toBe(4);
    expect(image.sourceRef).toBeUndefined();
  });
});

function proceduralImage(ref: GraphicsImageRef): V7RasterImage {
  const pixels = new Uint8Array(ref.width * ref.height * 4);
  for (let y = 0; y < ref.height; y += 1) {
    for (let x = 0; x < ref.width; x += 1) {
      const offset = (y * ref.width + x) * 4;
      pixels[offset] = (x * 17 + y * 3) % 256;
      pixels[offset + 1] = (x * 5 + y * 19) % 256;
      pixels[offset + 2] = (x * 11 + y * 7) % 256;
      pixels[offset + 3] = 255;
    }
  }
  return { id: ref.id, width: ref.width, height: ref.height, pixels };
}
