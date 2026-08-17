import type { GraphicsCompatibility, GraphicsImageRef } from "../v2/graphics";
import { applySebBlendMode } from "../v2/seb-raster";
import type { Sprite } from "../v1/sprite";
import type { IndexedImage } from "../v3/image";
import { ResourceManagerV3 } from "../v3/resource-manager";
import { V4ContractError } from "./errors";
import type {
  V4ImageDimension,
  V4ResolvedImage,
  V4ResourceAddress,
  V4SebDrawResult,
} from "./contracts";

/**
 * Thin V4 bridge over the already-proven V3 numeric resource manager.
 * It adds only the dimensions required by the V2 command recorder; it does
 * not parse source files or replace V1/V2 SEB/image semantics.
 */
export class V4ResourceManager {
  private readonly dimensions = new Map<number, V4ImageDimension>();

  public constructor(
    public readonly manager: ResourceManagerV3,
    imageDimensions: readonly V4ImageDimension[],
  ) {
    for (const dimension of imageDimensions) {
      if (
        !Number.isSafeInteger(dimension.id)
        || dimension.id < 0
        || !Number.isSafeInteger(dimension.width)
        || dimension.width <= 0
        || !Number.isSafeInteger(dimension.height)
        || dimension.height <= 0
      ) {
        throw new V4ContractError("V4_INPUT_MALFORMED", "V4 image dimension record is malformed");
      }
      if (this.dimensions.has(dimension.id)) {
        throw new V4ContractError("V4_INPUT_MALFORMED", `Duplicate V4 image dimension ${dimension.id}`);
      }
      this.dimensions.set(dimension.id, dimension);
    }
  }

  public get groupId(): string {
    return this.manager.groupId;
  }

  public hasImage(id: number): boolean {
    return Number.isSafeInteger(id) && id >= 0 && this.manager.img[id] !== undefined && this.manager.img[id] !== null;
  }

  public hasSeb(id: number): boolean {
    return Number.isSafeInteger(id) && id >= 0 && this.manager.seb[id] !== undefined && this.manager.seb[id] !== null;
  }

  public getImage(id: number): IndexedImage {
    return this.manager.getImage(id);
  }

  public getSeb(id: number) {
    return this.manager.getSeb(id);
  }

  public resolveImage(id: number): V4ResolvedImage {
    const image = this.getImage(id);
    const dimension = this.dimensions.get(id);
    if (dimension === undefined) {
      throw new V4ContractError(
        "V4_IMAGE_DIMENSIONS_UNPROVEN",
        `${this.groupId}: image ID ${id} has no selected V4 dimension contract`,
      );
    }
    return {
      address: this.address(id),
      ref: this.imageRef(image, dimension),
      width: dimension.width,
      height: dimension.height,
      sourceMember: image.sourceMember,
    };
  }

  public drawImage(
    graphics: GraphicsCompatibility,
    imageId: number,
    x: number,
    y: number,
    source: { readonly x: number; readonly y: number; readonly width: number; readonly height: number },
  ): number {
    const image = this.resolveImage(imageId);
    if (
      source.x < 0
      || source.y < 0
      || source.width <= 0
      || source.height <= 0
      || source.x + source.width > image.width
      || source.y + source.height > image.height
    ) {
      throw new V4ContractError("V4_INPUT_MALFORMED", `Image crop is outside image ${imageId}`);
    }
    graphics.drawImage(image.ref, x, y, source.x, source.y, source.width, source.height);
    return 1;
  }

  public drawSeb(
    graphics: GraphicsCompatibility,
    x: number,
    y: number,
    sebId: number,
    options: { readonly frame?: number; readonly layer?: number } = {},
  ): V4SebDrawResult {
    const seb = this.getSeb(sebId);
    const frame = normalizeFrame(options.frame ?? seb.getCurFrame(), seb.getMaxFrame());
    const before = graphics.commands.length;
    const sprites = options.layer === undefined
      ? seb.getSprites(frame)
      : [requireSprite(seb, frame, options.layer)];
    const resolvedTextureIds: number[] = [];
    for (const sprite of sprites) {
      if (sprite.TexId < 0) {
        continue;
      }
      resolvedTextureIds.push(sprite.TexId);
      this.drawSprite(graphics, sprite, x, y);
    }
    return {
      address: this.address(sebId),
      frame,
      layer: options.layer ?? null,
      commandCount: graphics.commands.length - before,
      resolvedTextureIds,
    };
  }

  private drawSprite(graphics: GraphicsCompatibility, sprite: Sprite, x: number, y: number): void {
    const image = this.resolveImage(sprite.TexId);
    const flipMode = sprite.ReverseU | (sprite.ReverseV << 1);
    if (flipMode !== 0) {
      graphics.setFlipMode(flipMode);
    }
    const blendPushed = sprite.Blend !== 0;
    if (blendPushed) {
      applySebBlendMode(graphics, sprite.Blend, sprite.Color);
    }
    graphics.drawImage(
      image.ref,
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

  private imageRef(image: IndexedImage, dimension: V4ImageDimension): GraphicsImageRef {
    return {
      id: `${this.groupId}:image:${image.id}`,
      width: dimension.width,
      height: dimension.height,
    };
  }

  private address(id: number): V4ResourceAddress {
    return { groupId: this.groupId, id };
  }
}

function normalizeFrame(frame: number, maxFrame: number): number {
  if (!Number.isSafeInteger(frame) || frame < 0 || !Number.isSafeInteger(maxFrame) || maxFrame <= 0) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "V4 SEB frame is malformed");
  }
  return frame % maxFrame;
}

function requireSprite(seb: ReturnType<ResourceManagerV3["getSeb"]>, frame: number, layer: number): Sprite {
  const sprite = seb.getSprite(frame, layer);
  if (sprite === null) {
    throw new V4ContractError("V4_UNSUPPORTED_SELECTOR", `SEB layer ${layer} has no active frame ${frame}`);
  }
  return sprite;
}
