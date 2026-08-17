import { V2ContractError } from "./errors";

export const GraphicsFlip = {
  NONE: 0,
  HORIZONTAL: 1,
  VERTICAL: 2,
  ROTATE: 3,
  ROTATE_LEFT: 4,
  ROTATE_RIGHT: 5,
} as const;

export const GraphicsAnchor = {
  LEFT: 1,
  CENTER: 2,
  RIGHT: 4,
  TOP: 16,
  MIDDLE: 32,
  BOTTOM: 64,
} as const;

export const GraphicsOperation = {
  REPLACE: 0,
  ADD: 1,
  SUBTRACT: 2,
} as const;

export const GraphicsBlend = {
  NONE: 0,
  COLOR: 1,
  LIGHT: 2,
  GRAYSCALE: 3,
} as const;

export interface GraphicsImageRef {
  readonly id: string | number;
  readonly width: number;
  readonly height: number;
}

export interface GraphicsRect {
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}

export interface GraphicsRenderMode {
  readonly operator: number;
  readonly sourceRatio: number;
  readonly destinationRatio: number;
  readonly isReplace: boolean;
}

export interface GraphicsStateSnapshot {
  readonly clip: GraphicsRect | null;
  readonly clipDepth: number;
  readonly flipMode: number;
  readonly linearFilter: boolean;
  readonly color: number;
  readonly scalePercent: number;
  readonly renderMode: GraphicsRenderMode;
  readonly renderModeDepth: number;
  readonly blendMode: number;
  readonly blendColor: number;
  readonly blendModeDepth: number;
}

export interface DrawImageCommand {
  readonly kind: "draw-image" | "draw-scaled-image";
  readonly image: GraphicsImageRef;
  readonly destination: GraphicsRect;
  readonly source: GraphicsRect;
  readonly state: GraphicsStateSnapshot;
}

export type GraphicsCommand = DrawImageCommand;

type MutableRect = { x: number; y: number; width: number; height: number };

interface MutableRenderMode {
  operator: number;
  sourceRatio: number;
  destinationRatio: number;
  isReplace: boolean;
}

const DEFAULT_COLOR = toSigned32(0xff000000);

export class GraphicsCompatibility {
  private clip: MutableRect | null = null;

  private readonly clipStack: (MutableRect | null)[] = [];

  private flipMode: number = GraphicsFlip.NONE;

  private linearFilter = false;

  private color = DEFAULT_COLOR;

  private scalePercent = 100;

  private renderMode: MutableRenderMode = makeRenderMode(
    GraphicsOperation.REPLACE,
    255,
    0,
  );

  private readonly renderModeStack: MutableRenderMode[] = [];

  private blendMode: number = GraphicsBlend.NONE;

  private blendColor = 0;

  private readonly blendModeStack: { mode: number; color: number }[] = [];

  private readonly recordedCommands: GraphicsCommand[] = [];

  public get commands(): readonly GraphicsCommand[] {
    return this.recordedCommands;
  }

  public getState(): GraphicsStateSnapshot {
    return {
      clip: cloneRect(this.clip),
      clipDepth: this.clipStack.length,
      flipMode: this.flipMode,
      linearFilter: this.linearFilter,
      color: this.color,
      scalePercent: this.scalePercent,
      renderMode: { ...this.renderMode },
      renderModeDepth: this.renderModeStack.length,
      blendMode: this.blendMode,
      blendColor: this.blendColor,
      blendModeDepth: this.blendModeStack.length,
    };
  }

  public clearCommands(): void {
    this.recordedCommands.length = 0;
  }

  public resetRender(): void {
    this.clip = null;
    this.clipStack.length = 0;
    this.flipMode = GraphicsFlip.NONE;
    this.color = DEFAULT_COLOR;
    this.scalePercent = 100;
    this.renderMode = makeRenderMode(GraphicsOperation.REPLACE, 255, 0);
    this.renderModeStack.length = 0;
    this.blendMode = GraphicsBlend.NONE;
    this.blendColor = 0;
    this.blendModeStack.length = 0;
  }

  public setFlipMode(flipMode: number): void {
    this.flipMode = requireInteger(flipMode, "GRAPHICS_FLIP_MODE_MALFORMED");
  }

  public getFlipMode(): number {
    return this.flipMode;
  }

  public scale(scalePercent: number): void {
    this.scalePercent = requireFinite(scalePercent, "GRAPHICS_SCALE_MALFORMED");
  }

  public getScale(): number {
    return this.scalePercent;
  }

  public linearFilterEnabled(enable: boolean): void {
    this.linearFilter = Boolean(enable);
  }

  public isLinearFilter(): boolean {
    return this.linearFilter;
  }

  public setColor(color: number): void;

  public setColor(red: number, green: number, blue: number, alpha?: number): void;

  public setColor(first: number, second?: number, third?: number, fourth = 255): void {
    if (second === undefined && third === undefined) {
      this.color = toSigned32(requireInteger(first, "GRAPHICS_COLOR_MALFORMED"));
      return;
    }
    if (second === undefined || third === undefined) {
      throw new V2ContractError("GRAPHICS_COLOR_MALFORMED");
    }
    this.color = packArgb(first, second, third, fourth);
  }

  public getColor(): number {
    return this.color;
  }

  public setRenderMode(): void;

  public setRenderMode(operator: number, sourceRatio: number): void;

  public setRenderMode(operator: number, sourceRatio: number, destinationRatio: number): void;

  public setRenderMode(
    operator: number = GraphicsOperation.REPLACE,
    sourceRatio: number = 255,
    destinationRatio?: number,
  ): void {
    const validOperator = requireInteger(operator, "GRAPHICS_RENDER_OPERATOR_MALFORMED");
    const validSource = requireInteger(sourceRatio, "GRAPHICS_RENDER_SOURCE_RATIO_MALFORMED");
    const validDestination = destinationRatio === undefined
      ? validOperator === GraphicsOperation.ADD ? 255 - validSource : 255
      : requireInteger(destinationRatio, "GRAPHICS_RENDER_DESTINATION_RATIO_MALFORMED");
    this.renderMode = makeRenderMode(validOperator, validSource, validDestination);
  }

  public getRenderModeOperator(): number {
    return this.renderMode.operator;
  }

  public getRenderModeSrcRatio(): number {
    return this.renderMode.sourceRatio;
  }

  public getRenderModeDstRatio(): number {
    return this.renderMode.destinationRatio;
  }

  public pushRenderMode(): void;

  public pushRenderMode(operator: number, sourceRatio: number, destinationRatio: number): void;

  public pushRenderMode(operator?: number, sourceRatio?: number, destinationRatio?: number): void {
    this.renderModeStack.push({ ...this.renderMode });
    if (operator !== undefined || sourceRatio !== undefined || destinationRatio !== undefined) {
      if (operator === undefined || sourceRatio === undefined || destinationRatio === undefined) {
        throw new V2ContractError("GRAPHICS_RENDER_MODE_MALFORMED");
      }
      this.setRenderMode(operator, sourceRatio, destinationRatio);
    }
  }

  public popRenderMode(): void {
    const previous = this.renderModeStack.pop();
    if (previous !== undefined) {
      this.renderMode = previous;
    }
  }

  public setBlendMode(mode: number, color?: number): void;

  public setBlendMode(mode: number, red: number, green: number, blue: number, alpha?: number): void;

  public setBlendMode(
    mode: number,
    colorOrRed = 0,
    green?: number,
    blue?: number,
    alpha = 255,
  ): void {
    const validMode = requireInteger(mode, "GRAPHICS_BLEND_MODE_MALFORMED");
    if (validMode < GraphicsBlend.NONE || validMode > GraphicsBlend.GRAYSCALE) {
      throw new V2ContractError("GRAPHICS_BLEND_MODE_UNSUPPORTED");
    }
    this.blendMode = validMode;
    this.blendColor = green === undefined || blue === undefined
      ? toSigned32(requireInteger(colorOrRed, "GRAPHICS_BLEND_COLOR_MALFORMED"))
      : packArgb(colorOrRed, green, blue, alpha);
  }

  public getBlendMode(): number {
    return this.blendMode;
  }

  public getBlendColor(): number {
    return this.blendColor;
  }

  public pushBlendMode(): void;

  public pushBlendMode(mode: number, color?: number): void;

  public pushBlendMode(mode?: number, color = 0): void {
    this.blendModeStack.push({ mode: this.blendMode, color: this.blendColor });
    if (mode !== undefined) {
      this.setBlendMode(mode, color);
    }
  }

  public popBlendMode(): void {
    const previous = this.blendModeStack.pop();
    if (previous !== undefined) {
      this.blendMode = previous.mode;
      this.blendColor = previous.color;
    }
  }

  public pushClip(): void {
    this.clipStack.push(cloneMutableRect(this.clip));
  }

  public popClip(): void {
    const previous = this.clipStack.pop();
    if (previous !== undefined) {
      this.clip = cloneMutableRect(previous);
    }
  }

  public setClip(x: number, y: number, width: number, height: number): void {
    this.clip = makeRect(x, y, width, height, "GRAPHICS_CLIP_MALFORMED");
  }

  public clipRect(x: number, y: number, width: number, height: number, push = true): void {
    if (push) {
      this.pushClip();
    }
    const incoming = makeRect(x, y, width, height, "GRAPHICS_CLIP_MALFORMED");
    this.clip = this.clip === null ? incoming : intersectRects(this.clip, incoming);
  }

  public clearClip(): void {
    this.clip = null;
  }

  public getClip(): readonly [number, number, number, number] | null {
    if (this.clip === null) {
      return null;
    }
    return [
      Math.trunc(this.clip.x),
      Math.trunc(this.clip.y),
      Math.trunc(this.clip.width),
      Math.trunc(this.clip.height),
    ];
  }

  public drawImage(image: GraphicsImageRef, dx: number, dy: number): void;

  public drawImage(
    image: GraphicsImageRef,
    dx: number,
    dy: number,
    sx: number,
    sy: number,
    width: number,
    height: number,
  ): void;

  public drawImage(
    image: GraphicsImageRef,
    dx: number,
    dy: number,
    sx = 0,
    sy = 0,
    width = image.width,
    height = image.height,
  ): void {
    this.recordedCommands.push(this.makeImageCommand(
      "draw-image",
      image,
      makeRect(dx, dy, width, height, "GRAPHICS_DESTINATION_MALFORMED"),
      makeRect(sx, sy, width, height, "GRAPHICS_SOURCE_MALFORMED"),
    ));
  }

  public drawScaledImage(
    image: GraphicsImageRef,
    dx: number,
    dy: number,
    width: number,
    height: number,
    sx: number,
    sy: number,
    sourceWidth: number,
    sourceHeight: number,
  ): void {
    this.recordedCommands.push(this.makeImageCommand(
      "draw-scaled-image",
      image,
      makeRect(dx, dy, width, height, "GRAPHICS_DESTINATION_MALFORMED"),
      makeRect(sx, sy, sourceWidth, sourceHeight, "GRAPHICS_SOURCE_MALFORMED"),
    ));
  }

  private makeImageCommand(
    kind: DrawImageCommand["kind"],
    image: GraphicsImageRef,
    destination: GraphicsRect,
    source: GraphicsRect,
  ): DrawImageCommand {
    validateImageRef(image);
    return {
      kind,
      image: { ...image },
      destination,
      source,
      state: this.getState(),
    };
  }
}

export function imageRef(id: string | number, width: number, height: number): GraphicsImageRef {
  validateImageRef({ id, width, height });
  return { id, width, height };
}

export function packArgb(red: number, green: number, blue: number, alpha = 255): number {
  const r = clampColorChannel(red);
  const g = clampColorChannel(green);
  const b = clampColorChannel(blue);
  const a = clampColorChannel(alpha);
  return toSigned32((a << 24) | (r << 16) | (g << 8) | b);
}

export function unpackArgb(color: number): { readonly red: number; readonly green: number; readonly blue: number; readonly alpha: number } {
  const value = color >>> 0;
  return {
    red: (value >>> 16) & 0xff,
    green: (value >>> 8) & 0xff,
    blue: value & 0xff,
    alpha: (value >>> 24) & 0xff,
  };
}

export function scaleAlphaByRatio(alpha: number, sourceRatio: number): number {
  const product = requireInteger(alpha, "GRAPHICS_ALPHA_MALFORMED") * requireInteger(
    sourceRatio,
    "GRAPHICS_RENDER_SOURCE_RATIO_MALFORMED",
  );
  if (product >= 0xff00) {
    return 0xff;
  }
  return Math.floor((product + 128) / 255);
}

function makeRenderMode(operator: number, sourceRatio: number, destinationRatio: number): MutableRenderMode {
  return {
    operator,
    sourceRatio,
    destinationRatio,
    isReplace: (operator === GraphicsOperation.REPLACE && sourceRatio > 0xfe)
      || (operator === GraphicsOperation.ADD
        && sourceRatio > 0xfe
        && sourceRatio + destinationRatio === 0x100
        && destinationRatio - 1 === 0),
  };
}

function makeRect(x: number, y: number, width: number, height: number, code: string): MutableRect {
  return {
    x: requireFinite(x, code),
    y: requireFinite(y, code),
    width: requireFinite(width, code),
    height: requireFinite(height, code),
  };
}

function intersectRects(left: MutableRect, right: MutableRect): MutableRect {
  const leftEdge = Math.max(left.x, right.x);
  const topEdge = Math.max(left.y, right.y);
  const rightEdge = Math.min(left.x + left.width, right.x + right.width);
  const bottomEdge = Math.min(left.y + left.height, right.y + right.height);
  return {
    x: leftEdge,
    y: topEdge,
    width: Math.max(0, rightEdge - leftEdge),
    height: Math.max(0, bottomEdge - topEdge),
  };
}

function cloneRect(rect: MutableRect | null): GraphicsRect | null {
  return rect === null ? null : { ...rect };
}

function cloneMutableRect(rect: MutableRect | null): MutableRect | null {
  return rect === null ? null : { ...rect };
}

function validateImageRef(image: GraphicsImageRef): void {
  if (image === null || typeof image !== "object" || (typeof image.id !== "string" && typeof image.id !== "number")) {
    throw new V2ContractError("GRAPHICS_IMAGE_MALFORMED");
  }
  requirePositiveFinite(image.width, "GRAPHICS_IMAGE_WIDTH_MALFORMED");
  requirePositiveFinite(image.height, "GRAPHICS_IMAGE_HEIGHT_MALFORMED");
}

function clampColorChannel(value: number): number {
  const valid = requireInteger(value, "GRAPHICS_COLOR_CHANNEL_MALFORMED");
  return Math.max(0, Math.min(0xff, valid));
}

function requireInteger(value: number, code: string): number {
  if (!Number.isInteger(value)) {
    throw new V2ContractError(code);
  }
  return value;
}

function requireFinite(value: number, code: string): number {
  if (!Number.isFinite(value)) {
    throw new V2ContractError(code);
  }
  return value;
}

function requirePositiveFinite(value: number, code: string): number {
  if (!Number.isFinite(value) || value <= 0) {
    throw new V2ContractError(code);
  }
  return value;
}

function toSigned32(value: number): number {
  return value | 0;
}
