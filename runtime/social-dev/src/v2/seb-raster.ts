import { rasterFixtureManifestV2Json as rasterFixtureManifestJson } from "../catalog/load-original-runtime-pack";

import type { Image } from "../v1/image";
import type { ResourceManager } from "../v1/resource-manager";
import type { Seb } from "../v1/seb";
import type { Sprite } from "../v1/sprite";
import { V1LookupError } from "../v1/errors";
import { V2DeferredError } from "./errors";
import {
  GraphicsBlend,
  GraphicsCompatibility,
  GraphicsImageRef,
  GraphicsOperation,
  imageRef,
  scaleAlphaByRatio,
  unpackArgb,
} from "./graphics";

interface RasterFixtureImageSource {
  readonly source_member: string;
  readonly width: number | null;
  readonly height: number | null;
  readonly status: string;
}

interface RasterFixtureManifest {
  readonly image_sources: readonly RasterFixtureImageSource[];
}

const rasterFixtureManifest = rasterFixtureManifestJson as RasterFixtureManifest;

export interface SebDrawOptions {
  readonly frame?: number;
  readonly layer?: number;
}

export interface SebDrawResult {
  readonly sebId: number;
  readonly frame: number;
  readonly layer: number | null;
  readonly commandCount: number;
}

export function drawSeb(
  manager: ResourceManager,
  graphics: GraphicsCompatibility,
  x: number,
  y: number,
  sebId: number,
  options: SebDrawOptions = {},
): SebDrawResult {
  const seb = manager.getSeb(sebId);
  const frame = normalizeManagerFrame(options.frame ?? seb.getCurFrame(), seb);
  const before = graphics.commands.length;
  const sprites = options.layer === undefined
    ? seb.getSprites(frame)
    : [requireSprite(seb, frame, options.layer)];

  for (const sprite of sprites) {
    drawSprite(manager, graphics, sprite, x, y);
  }

  return {
    sebId,
    frame,
    layer: options.layer ?? null,
    commandCount: graphics.commands.length - before,
  };
}

export function renderSeb(): never {
  throw new V2DeferredError(
    "V2_SEB_DEPTH_UNPROVEN",
    "Seb.Render remains deferred because the selected SEB fixtures do not carry proven native depth-line payloads.",
  );
}

function drawSprite(
  manager: ResourceManager,
  graphics: GraphicsCompatibility,
  sprite: Sprite,
  x: number,
  y: number,
): void {
  if (sprite.TexId < 0) {
    if (sprite.TexId === -1 || sprite.TexId === -8 || sprite.TexId === -9) {
      return;
    }
    throw new V2DeferredError(
      "V2_SEB_SYNTHETIC_SPRITE_UNPROVEN",
      `Synthetic SEB texture id ${sprite.TexId} needs the native primitive path before raster implementation.`,
    );
  }

  const ref = resolveImageRef(manager, sprite.TexId);
  const flipMode = sprite.ReverseU | (sprite.ReverseV << 1);
  if (flipMode !== 0) {
    graphics.setFlipMode(flipMode);
  }

  const blendPushed = sprite.Blend !== GraphicsBlend.NONE;
  if (blendPushed) {
    applySebBlendMode(graphics, sprite.Blend, sprite.Color);
  }

  graphics.drawImage(
    ref,
    x + sprite.TransX,
    y + sprite.TransY,
    sprite.U,
    sprite.V,
    sprite.W,
    sprite.H,
  );

  if (blendPushed) {
    graphics.popRenderMode();
  }
  if (flipMode !== 0) {
    graphics.setFlipMode(0);
  }
}

export function applySebBlendMode(graphics: GraphicsCompatibility, blend: number, color: number): void {
  const alpha = unpackArgb(color).alpha;
  const sourceRatio = graphics.getRenderModeOperator() === GraphicsOperation.REPLACE
    && graphics.getRenderModeSrcRatio() !== 0xff
    ? scaleAlphaByRatio(alpha, graphics.getRenderModeSrcRatio())
    : alpha;
  if (blend === GraphicsBlend.COLOR) {
    graphics.pushRenderMode(GraphicsOperation.ADD, sourceRatio, 0xff - sourceRatio);
    return;
  }
  if (blend === GraphicsBlend.LIGHT) {
    graphics.pushRenderMode(GraphicsOperation.ADD, sourceRatio, 0xff);
    return;
  }
  if (blend === GraphicsBlend.GRAYSCALE) {
    graphics.pushRenderMode(GraphicsOperation.SUBTRACT, sourceRatio, 0xff);
    return;
  }
  throw new V2DeferredError(
    "V2_SEB_BLEND_UNSUPPORTED",
    `SEB blend mode ${blend} is outside the native Graphics blend surface 0..3.`,
  );
}

function normalizeManagerFrame(frame: number, seb: Seb): number {
  if (!Number.isInteger(frame) || frame < 0) {
    throw new V2DeferredError(
      "V2_FRAME_NORMALIZATION_UNPROVEN",
      "The native manager wrapper uses signed remainder semantics for negative frames; selected call sites are non-negative only.",
    );
  }
  return frame % seb.getMaxFrame();
}

function requireSprite(seb: Seb, frame: number, layer: number): Sprite {
  const sprite = seb.getSprite(frame, layer);
  if (sprite === null) {
    throw new V2DeferredError("V2_SEB_FRAME_RECORD_NOT_FOUND", "The selected SEB layer has no active frame record.");
  }
  return sprite;
}

function resolveImageRef(manager: ResourceManager, imageId: number): GraphicsImageRef {
  try {
    return toImageRef(manager.getImage(imageId));
  } catch (error) {
    if (!(error instanceof V1LookupError)) {
      throw error;
    }
    const fixture = manager.fixtures.find(
      (candidate) => candidate.image_id === imageId && candidate.image_member !== null,
    );
    const sourceMember = fixture?.image_member;
    const source = sourceMember === undefined || sourceMember === null
      ? undefined
      : rasterFixtureManifest.image_sources.find((candidate) => candidate.source_member === sourceMember);
    if (source === undefined || source.status !== "proven" || source.width === null || source.height === null) {
      throw new V2DeferredError(
        "V2_RESOURCE_IMAGE_SOURCE_UNPROVEN",
        `ResourceManager image slot ${imageId} has no proven source image contract for raster composition.`,
      );
    }
    return imageRef(source.source_member, source.width, source.height);
  }
}

function toImageRef(image: Image): GraphicsImageRef {
  return imageRef(image.sourceMember, image.width, image.height);
}
