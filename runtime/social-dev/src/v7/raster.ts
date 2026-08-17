import type {
  GraphicsCommand,
  GraphicsRect,
  GraphicsStateSnapshot,
} from "../v2/graphics";
import {
  GraphicsBlend,
  GraphicsFlip,
  GraphicsOperation,
} from "../v2/graphics";
import type {
  V7Bounds,
  V7DrawRequest,
  V7FlipMode,
  V7RasterClip,
  V7RasterImage,
  V7RasterOptions,
  V7RasterSurface,
  V7RasterTransform,
  V7RenderResult,
  V7SurfaceOrigin,
} from "./contracts";

const IDENTITY_COLOR = -16777216;
const EPSILON = 1e-9;

export class RasterSurfaceCompatibilityV7 implements V7RasterSurface {
  public readonly pixels: Uint8Array;

  public constructor(
    public readonly width: number,
    public readonly height: number,
    background: readonly [number, number, number, number] = [0, 0, 0, 0],
  ) {
    requirePositiveInteger(width, "V7 surface width");
    requirePositiveInteger(height, "V7 surface height");
    this.pixels = new Uint8Array(width * height * 4);
    this.clear(background);
  }

  public clear(color: readonly [number, number, number, number] = [0, 0, 0, 0]): void {
    const rgba = color.map((channel) => clampByte(channel)) as [number, number, number, number];
    for (let offset = 0; offset < this.pixels.length; offset += 4) {
      this.pixels[offset] = rgba[0];
      this.pixels[offset + 1] = rgba[1];
      this.pixels[offset + 2] = rgba[2];
      this.pixels[offset + 3] = rgba[3];
    }
  }

  public getPixel(x: number, y: number): readonly [number, number, number, number] {
    const offset = this.offsetAt(x, y);
    return [
      this.pixels[offset],
      this.pixels[offset + 1],
      this.pixels[offset + 2],
      this.pixels[offset + 3],
    ];
  }

  public setPixel(x: number, y: number, rgba: readonly [number, number, number, number]): void {
    const offset = this.offsetAt(x, y);
    this.pixels[offset] = clampByte(rgba[0]);
    this.pixels[offset + 1] = clampByte(rgba[1]);
    this.pixels[offset + 2] = clampByte(rgba[2]);
    this.pixels[offset + 3] = clampByte(rgba[3]);
  }

  public nonTransparentBounds(): V7Bounds | null {
    let left = this.width;
    let top = this.height;
    let right = -1;
    let bottom = -1;
    for (let y = 0; y < this.height; y += 1) {
      for (let x = 0; x < this.width; x += 1) {
        if (this.pixels[(y * this.width + x) * 4 + 3] === 0) {
          continue;
        }
        left = Math.min(left, x);
        top = Math.min(top, y);
        right = Math.max(right, x);
        bottom = Math.max(bottom, y);
      }
    }
    return right < left || bottom < top
      ? null
      : { x: left, y: top, width: right - left + 1, height: bottom - top + 1 };
  }

  public clone(): RasterSurfaceCompatibilityV7 {
    const copy = new RasterSurfaceCompatibilityV7(this.width, this.height);
    copy.pixels.set(this.pixels);
    return copy;
  }

  private offsetAt(x: number, y: number): number {
    if (!Number.isSafeInteger(x) || !Number.isSafeInteger(y) || x < 0 || y < 0 || x >= this.width || y >= this.height) {
      throw new Error(`V7 surface coordinate out of range (${x},${y})`);
    }
    return (y * this.width + x) * 4;
  }
}

export class RasterCompatibilityV7 {
  private readonly origin: V7SurfaceOrigin;

  private readonly surface: RasterSurfaceCompatibilityV7;

  public constructor(options: V7RasterOptions) {
    this.origin = options.origin ?? { x: 0, y: 0 };
    this.surface = new RasterSurfaceCompatibilityV7(
      options.width,
      options.height,
      options.background ?? [0, 0, 0, 0],
    );
  }

  public get output(): RasterSurfaceCompatibilityV7 {
    return this.surface;
  }

  public draw(request: V7DrawRequest): number {
    validateImage(request.image);
    validateRect(request.destination, "V7 destination");
    validateRect(request.source, "V7 source");
    const transform = resolveTransform(request);
    const flipMode = request.flipMode ?? normalizeFlipMode(request.state.flipMode);
    const bounds = transformedBounds(request.destination, transform);
    const minX = Math.max(0, Math.floor(bounds.x + this.origin.x));
    const minY = Math.max(0, Math.floor(bounds.y + this.origin.y));
    const maxX = Math.min(this.surface.width, Math.ceil(bounds.x + bounds.width + this.origin.x));
    const maxY = Math.min(this.surface.height, Math.ceil(bounds.y + bounds.height + this.origin.y));
    let written = 0;

    for (let surfaceY = minY; surfaceY < maxY; surfaceY += 1) {
      for (let surfaceX = minX; surfaceX < maxX; surfaceX += 1) {
        const worldPoint = {
          x: surfaceX + 0.5 - this.origin.x,
          y: surfaceY + 0.5 - this.origin.y,
        };
        if (!pointInClip(worldPoint, request.clip ?? null)) {
          continue;
        }
        const localPoint = inverseTransform(worldPoint, transform);
        if (!insideRect(localPoint, request.destination)) {
          continue;
        }
        const sourcePoint = sourcePointFor(localPoint, request.destination, request.source, flipMode);
        const sample = request.state.linearFilter
          ? sampleLinear(request.image, sourcePoint.x, sourcePoint.y)
          : sampleNearest(request.image, sourcePoint.x, sourcePoint.y);
        const filtered = applyStateColorAndBlend(sample, request.state);
        const destination = this.surface.getPixel(surfaceX, surfaceY);
        this.surface.setPixel(surfaceX, surfaceY, composite(destination, filtered, request.state));
        written += 1;
      }
    }
    return written;
  }

  public render(
    commands: readonly GraphicsCommand[],
    images: ReadonlyMap<string, V7RasterImage>,
  ): V7RenderResult {
    let drawCount = 0;
    let skippedDrawCount = 0;
    for (const command of commands) {
      const image = images.get(String(command.image.id));
      if (image === undefined) {
        throw new Error(`V7 raster image is missing for ${String(command.image.id)}`);
      }
      const written = this.draw({
        image,
        destination: command.destination,
        source: command.source,
        state: command.state,
        clip: command.state.clip === null ? null : { rect: command.state.clip },
      });
      if (written > 0) {
        drawCount += 1;
      } else {
        skippedDrawCount += 1;
      }
    }
    return {
      surface: this.surface,
      commands,
      drawCount,
      skippedDrawCount,
      nonTransparentBounds: this.surface.nonTransparentBounds(),
    };
  }
}

export function createDefaultRasterState(): GraphicsStateSnapshot {
  return {
    clip: null,
    clipDepth: 0,
    flipMode: GraphicsFlip.NONE,
    linearFilter: false,
    color: IDENTITY_COLOR,
    scalePercent: 100,
    renderMode: {
      operator: GraphicsOperation.REPLACE,
      sourceRatio: 255,
      destinationRatio: 0,
      isReplace: true,
    },
    renderModeDepth: 0,
    blendMode: GraphicsBlend.NONE,
    blendColor: 0,
    blendModeDepth: 0,
  };
}

function resolveTransform(request: V7DrawRequest): Required<V7RasterTransform> {
  const stateScale = request.state.scalePercent / 100;
  if (!Number.isFinite(stateScale) || stateScale <= 0) {
    throw new Error("V7 scale must be positive");
  }
  const flipMode = request.flipMode ?? normalizeFlipMode(request.state.flipMode);
  const rotationDegrees = request.transform?.rotationDegrees
    ?? (flipMode === GraphicsFlip.ROTATE_LEFT ? -90 : flipMode === GraphicsFlip.ROTATE_RIGHT ? 90 : 0);
  return {
    scaleX: request.transform?.scaleX ?? stateScale,
    scaleY: request.transform?.scaleY ?? stateScale,
    rotationDegrees,
    pivot: request.transform?.pivot ?? {
      x: request.destination.x + request.destination.width / 2,
      y: request.destination.y + request.destination.height / 2,
    },
  };
}

function transformedBounds(rect: GraphicsRect, transform: Required<V7RasterTransform>): V7Bounds {
  const corners = [
    { x: rect.x, y: rect.y },
    { x: rect.x + rect.width, y: rect.y },
    { x: rect.x, y: rect.y + rect.height },
    { x: rect.x + rect.width, y: rect.y + rect.height },
  ].map((point) => forwardTransform(point, transform));
  const left = Math.min(...corners.map((point) => point.x));
  const top = Math.min(...corners.map((point) => point.y));
  const right = Math.max(...corners.map((point) => point.x));
  const bottom = Math.max(...corners.map((point) => point.y));
  return { x: left, y: top, width: right - left, height: bottom - top };
}

function forwardTransform(point: { x: number; y: number }, transform: Required<V7RasterTransform>): { x: number; y: number } {
  const scaledX = transform.pivot.x + (point.x - transform.pivot.x) * transform.scaleX;
  const scaledY = transform.pivot.y + (point.y - transform.pivot.y) * transform.scaleY;
  const radians = transform.rotationDegrees * Math.PI / 180;
  const cos = Math.cos(radians);
  const sin = Math.sin(radians);
  const dx = scaledX - transform.pivot.x;
  const dy = scaledY - transform.pivot.y;
  return {
    x: transform.pivot.x + dx * cos - dy * sin,
    y: transform.pivot.y + dx * sin + dy * cos,
  };
}

function inverseTransform(point: { x: number; y: number }, transform: Required<V7RasterTransform>): { x: number; y: number } {
  const radians = transform.rotationDegrees * Math.PI / 180;
  const cos = Math.cos(radians);
  const sin = Math.sin(radians);
  const dx = point.x - transform.pivot.x;
  const dy = point.y - transform.pivot.y;
  const unrotatedX = dx * cos + dy * sin;
  const unrotatedY = -dx * sin + dy * cos;
  return {
    x: transform.pivot.x + unrotatedX / transform.scaleX,
    y: transform.pivot.y + unrotatedY / transform.scaleY,
  };
}

function sourcePointFor(
  point: { x: number; y: number },
  destination: GraphicsRect,
  source: GraphicsRect,
  flipMode: V7FlipMode,
): { x: number; y: number } {
  let u = (point.x - destination.x) / destination.width;
  let v = (point.y - destination.y) / destination.height;
  if (flipMode === GraphicsFlip.HORIZONTAL || flipMode === GraphicsFlip.ROTATE) {
    u = 1 - u;
  }
  if (flipMode === GraphicsFlip.VERTICAL || flipMode === GraphicsFlip.ROTATE) {
    v = 1 - v;
  }
  return {
    x: source.x + u * source.width - 0.5,
    y: source.y + v * source.height - 0.5,
  };
}

function pointInClip(point: { x: number; y: number }, clip: V7RasterClip | null): boolean {
  if (clip === null) {
    return true;
  }
  if (clip.transformed === undefined) {
    return insideRect(point, clip.rect);
  }
  const transform = {
    scaleX: clip.transformed.scaleX ?? 1,
    scaleY: clip.transformed.scaleY ?? 1,
    rotationDegrees: clip.transformed.rotationDegrees ?? 0,
    pivot: clip.transformed.pivot ?? {
      x: clip.rect.x + clip.rect.width / 2,
      y: clip.rect.y + clip.rect.height / 2,
    },
  };
  const corners = [
    { x: clip.rect.x, y: clip.rect.y },
    { x: clip.rect.x + clip.rect.width, y: clip.rect.y },
    { x: clip.rect.x + clip.rect.width, y: clip.rect.y + clip.rect.height },
    { x: clip.rect.x, y: clip.rect.y + clip.rect.height },
  ].map((corner) => forwardTransform(corner, transform));
  let sign = 0;
  for (let index = 0; index < corners.length; index += 1) {
    const current = corners[index];
    const next = corners[(index + 1) % corners.length];
    const cross = (next.x - current.x) * (point.y - current.y)
      - (next.y - current.y) * (point.x - current.x);
    if (Math.abs(cross) <= EPSILON) {
      continue;
    }
    const currentSign = cross > 0 ? 1 : -1;
    if (sign === 0) {
      sign = currentSign;
    } else if (sign !== currentSign) {
      return false;
    }
  }
  return true;
}

function insideRect(point: { x: number; y: number }, rect: GraphicsRect): boolean {
  return point.x >= rect.x - EPSILON
    && point.y >= rect.y - EPSILON
    && point.x < rect.x + rect.width - EPSILON
    && point.y < rect.y + rect.height - EPSILON;
}

function sampleNearest(image: V7RasterImage, x: number, y: number): [number, number, number, number] {
  const sampleX = Math.floor(x + 0.5);
  const sampleY = Math.floor(y + 0.5);
  return readImagePixel(image, sampleX, sampleY);
}

function sampleLinear(image: V7RasterImage, x: number, y: number): [number, number, number, number] {
  const x0 = Math.floor(x);
  const y0 = Math.floor(y);
  const fx = x - x0;
  const fy = y - y0;
  const topLeft = readImagePixel(image, x0, y0);
  const topRight = readImagePixel(image, x0 + 1, y0);
  const bottomLeft = readImagePixel(image, x0, y0 + 1);
  const bottomRight = readImagePixel(image, x0 + 1, y0 + 1);
  return [0, 1, 2, 3].map((channel) => Math.round(
    lerp(lerp(topLeft[channel], topRight[channel], fx), lerp(bottomLeft[channel], bottomRight[channel], fx), fy),
  )) as [number, number, number, number];
}

function lerp(left: number, right: number, amount: number): number {
  return left + (right - left) * amount;
}

function readImagePixel(image: V7RasterImage, x: number, y: number): [number, number, number, number] {
  if (x < 0 || y < 0 || x >= image.width || y >= image.height) {
    return [0, 0, 0, 0];
  }
  const offset = (y * image.width + x) * 4;
  return [image.pixels[offset], image.pixels[offset + 1], image.pixels[offset + 2], image.pixels[offset + 3]];
}

function applyStateColorAndBlend(
  source: readonly [number, number, number, number],
  state: GraphicsStateSnapshot,
): [number, number, number, number] {
  const color = unpackSignedArgb(state.color);
  const identityColor = state.color === IDENTITY_COLOR;
  let red = source[0];
  let green = source[1];
  let blue = source[2];
  let alpha = source[3];
  if (!identityColor) {
    red = Math.round(red * color.red / 255);
    green = Math.round(green * color.green / 255);
    blue = Math.round(blue * color.blue / 255);
    alpha = Math.round(alpha * color.alpha / 255);
  }
  if (state.blendMode === GraphicsBlend.COLOR) {
    const blend = unpackSignedArgb(state.blendColor);
    red = Math.round(red * blend.red / 255);
    green = Math.round(green * blend.green / 255);
    blue = Math.round(blue * blend.blue / 255);
  } else if (state.blendMode === GraphicsBlend.LIGHT) {
    const blend = unpackSignedArgb(state.blendColor);
    red = clampByte(red + blend.red);
    green = clampByte(green + blend.green);
    blue = clampByte(blue + blend.blue);
  } else if (state.blendMode === GraphicsBlend.GRAYSCALE) {
    const gray = Math.round(red * 0.299 + green * 0.587 + blue * 0.114);
    red = gray;
    green = gray;
    blue = gray;
  }
  return [red, green, blue, alpha];
}

function composite(
  destination: readonly [number, number, number, number],
  source: readonly [number, number, number, number],
  state: GraphicsStateSnapshot,
): [number, number, number, number] {
  const sourceRatio = state.renderMode.sourceRatio / 255;
  const destinationRatio = state.renderMode.destinationRatio / 255;
  // Native image textures carry meaningful transparent pixels.  In the
  // default replace path a transparent source fragment must leave the
  // already-composed destination intact; otherwise an isometric tile drawn
  // later in native traversal order erases the neighboring tile's overlap.
  // Keep this narrow to the identity replace state so explicit subtract/add
  // render modes retain their recovered arithmetic semantics.
  if (
    state.renderMode.operator === GraphicsOperation.REPLACE
    && sourceRatio === 1
    && destinationRatio === 0
    && source[3] === 0
  ) {
    return [destination[0], destination[1], destination[2], destination[3]];
  }
  const result = [0, 1, 2, 3].map((channel) => {
    const sourceValue = source[channel] * sourceRatio;
    const destinationValue = destination[channel] * destinationRatio;
    if (state.renderMode.operator === GraphicsOperation.SUBTRACT) {
      return clampByte(Math.round(sourceValue - destinationValue));
    }
    return clampByte(Math.round(sourceValue + destinationValue));
  }) as [number, number, number, number];
  return result;
}

function unpackSignedArgb(value: number): { red: number; green: number; blue: number; alpha: number } {
  const unsigned = value >>> 0;
  return {
    red: (unsigned >>> 16) & 0xff,
    green: (unsigned >>> 8) & 0xff,
    blue: unsigned & 0xff,
    alpha: (unsigned >>> 24) & 0xff,
  };
}

function normalizeFlipMode(mode: number): V7FlipMode {
  if (!Number.isSafeInteger(mode) || mode < 0 || mode > 5) {
    throw new Error(`V7 unsupported flip mode ${mode}`);
  }
  return mode as V7FlipMode;
}

function validateImage(image: V7RasterImage): void {
  requirePositiveInteger(image.width, "V7 image width");
  requirePositiveInteger(image.height, "V7 image height");
  if (image.pixels.length !== image.width * image.height * 4) {
    throw new Error(`V7 image ${String(image.id)} has inconsistent RGBA length`);
  }
}

function validateRect(rect: GraphicsRect, label: string): void {
  for (const value of [rect.x, rect.y, rect.width, rect.height]) {
    if (!Number.isFinite(value)) {
      throw new Error(`${label} contains non-finite geometry`);
    }
  }
  if (rect.width <= 0 || rect.height <= 0) {
    throw new Error(`${label} must be positive`);
  }
}

function requirePositiveInteger(value: number, label: string): void {
  if (!Number.isSafeInteger(value) || value <= 0) {
    throw new Error(`${label} must be a positive integer`);
  }
}

function clampByte(value: number): number {
  return Math.max(0, Math.min(255, Math.round(value)));
}
