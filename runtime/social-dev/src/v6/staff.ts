import { GraphicsOperation, type GraphicsCompatibility } from "../v2/graphics";
import { applySebBlendMode } from "../v2/seb-raster";
import type { V4CameraBoundary, V4CommandTrace } from "../v4";
import type { CharacterMetadataRecord } from "../catalog/types";
import {
  getStaffAssetBinding,
  getStaffMetadata,
  getStaffSpawnActor,
  loadStaffFixtureCatalog,
  type StaffFixtureCatalog,
} from "./fixture-loader";
import { resolveHumanAction, type HumanDirectionInput } from "./human-action-resolver";
import type {
  HumanDirection,
  StaffAction,
  StaffDrawResult,
  StaffFrameState,
  StaffSelectorResolution,
  StaffV6Snapshot,
} from "./contracts";
import { frameIntervalForStaffAction, StaffAnimationV6 } from "./staff-animation";
import { createStaffPlacement, type StaffSpawnFixtureLike } from "./staff-placement";

export interface StaffV6Options {
  readonly sourceStaffId: number;
  readonly catalog?: StaffFixtureCatalog;
  readonly actorId?: string;
  readonly action?: StaffAction | string;
  readonly direction?: HumanDirection;
  readonly rawDirection?: number;
  readonly frame?: number;
  readonly alpha?: number;
  readonly scalePercent?: number;
}

export class StaffV6 {
  public readonly catalog: StaffFixtureCatalog;
  public readonly sourceStaffId: number;
  public readonly actor: StaffSpawnFixtureLike;
  public readonly metadata: CharacterMetadataRecord;
  public readonly imageSelectorId: number;
  public readonly assetBinding: ReturnType<typeof getStaffAssetBinding>;

  private actionValue: string;
  private directionValue: HumanDirection | null;
  private rawDirectionValue: number | null;
  private alphaValue: number;
  private scaleValue: number;
  private selectorValue: StaffSelectorResolution;
  private readonly animation: StaffAnimationV6;

  public constructor(options: StaffV6Options) {
    this.catalog = options.catalog ?? loadStaffFixtureCatalog();
    this.sourceStaffId = options.sourceStaffId;
    this.metadata = getStaffMetadata(options.sourceStaffId, this.catalog);
    this.assetBinding = getStaffAssetBinding(options.sourceStaffId, this.catalog);
    this.imageSelectorId = requireImageSelector(this.metadata, this.assetBinding.image_selector_id);
    const actor = getStaffSpawnActor(options.sourceStaffId, this.catalog);
    this.actor = toSpawnFixtureLike(actor, options.actorId);
    this.actionValue = options.action ?? "wait";
    this.rawDirectionValue = options.rawDirection ?? null;
    this.directionValue = options.direction ?? null;
    this.alphaValue = options.alpha ?? readInitialAlpha(actor);
    this.scaleValue = options.scalePercent ?? 100;
    validateAlpha(this.alphaValue);
    validateScale(this.scaleValue);
    this.selectorValue = resolveHumanAction(
      this.actionValue,
      { direction: this.directionValue ?? undefined, rawDirection: this.rawDirectionValue ?? undefined },
      this.catalog,
    );
    this.directionValue = this.selectorValue.direction;
    this.rawDirectionValue = this.selectorValue.rawDirection;
    this.animation = new StaffAnimationV6(this.catalog.human, this.selectorValue, options.frame ?? 0);
  }

  public get action(): string {
    return this.actionValue;
  }

  public get direction(): HumanDirection | null {
    return this.directionValue;
  }

  public get rawDirection(): number | null {
    return this.rawDirectionValue;
  }

  public get alpha(): number {
    return this.alphaValue;
  }

  public get scalePercent(): number {
    return this.scaleValue;
  }

  public get selector(): StaffSelectorResolution {
    return this.selectorValue;
  }

  public setAction(
    action: StaffAction | string,
    direction: HumanDirection = this.directionValue ?? "right",
    rawDirection?: number,
  ): StaffSelectorResolution {
    this.actionValue = action;
    this.directionValue = direction;
    this.rawDirectionValue = rawDirection ?? null;
    this.selectorValue = resolveHumanAction(
      action,
      { direction, rawDirection },
      this.catalog,
    );
    this.directionValue = this.selectorValue.direction;
    this.rawDirectionValue = this.selectorValue.rawDirection;
    this.animation.setSelector(this.selectorValue, 0);
    return this.selectorValue;
  }

  public setAlpha(alpha: number): void {
    validateAlpha(alpha);
    this.alphaValue = alpha;
  }

  public advanceAlpha(steps = 1): void {
    if (!Number.isSafeInteger(steps) || steps < 0) {
      throw new Error("V6 Staff alpha steps must be a non-negative integer");
    }
    this.alphaValue = Math.min(255, this.alphaValue + (steps * 25));
  }

  public advanceFrame(ticks = 1): void {
    if (!Number.isSafeInteger(ticks) || ticks < 0) {
      throw new Error("V6 Staff animation ticks must be a non-negative integer");
    }
    this.animation.advance(frameIntervalForStaffAction(this.actionValue) * ticks);
  }

  public getFrameState(): StaffFrameState | null {
    return this.animation.state(
      this.actionValue,
      this.selectorValue.sourceAction,
      frameIntervalForStaffAction(this.actionValue),
    );
  }

  public placement(camera: V4CameraBoundary): ReturnType<typeof createStaffPlacement> {
    return createStaffPlacement(this.actor, camera);
  }

  public draw(graphics: GraphicsCompatibility, camera: V4CameraBoundary): StaffDrawResult {
    const placement = this.placement(camera);
    const frame = this.getFrameState();
    const before = graphics.commands.length;
    if (this.alphaValue < 1) {
      return {
        commands: graphics.commands.slice(before),
        traces: [],
        placement,
        selector: this.selectorValue,
        frame,
        commandCount: 0,
        skipped: true,
        skipReason: "alpha_zero_at_native_spawn",
      };
    }
    if (this.selectorValue.selectorId === null || frame === null) {
      return {
        commands: graphics.commands.slice(before),
        traces: [],
        placement,
        selector: this.selectorValue,
        frame,
        commandCount: 0,
        skipped: true,
        skipReason: this.selectorValue.note ?? "selector_deferred",
      };
    }

    const alphaMode = this.alphaValue < 255;
    if (alphaMode) {
      graphics.pushRenderMode(GraphicsOperation.ADD, this.alphaValue, 255 - this.alphaValue);
    }
    const seb = this.catalog.human.getSeb(frame.selectorId);
    for (const sprite of seb.getSprites(frame.frame)) {
      if (sprite.TexId < 0) {
        continue;
      }
      const imageSelectorId = sprite.TexId === 0 ? this.imageSelectorId : sprite.TexId;
      const image = this.catalog.human.resolveImage(imageSelectorId);
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
        placement.screen.x + sprite.TransX,
        placement.screen.y + sprite.TransY,
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
    if (alphaMode) {
      graphics.popRenderMode();
    }
    const commandCount = graphics.commands.length - before;
    const trace: V4CommandTrace = {
      pass: "avatar-primary",
      kind: "seb",
      resource: { groupId: this.catalog.human.groupId, id: frame.selectorId },
      frame: frame.frame,
      layer: null,
      cell: placement.cell,
      destination: placement.screen,
      selectorRole: `staff:${this.sourceStaffId}:${this.actionValue}`,
      commandCount,
      proof: "CALL-FLOW-PROVEN",
    };
    return {
      commands: graphics.commands.slice(before),
      traces: [trace],
      placement,
      selector: this.selectorValue,
      frame,
      commandCount,
      skipped: false,
      skipReason: null,
    };
  }

  public snapshot(camera: V4CameraBoundary): StaffV6Snapshot {
    return {
      actorId: this.actor.id,
      sourceStaffId: this.sourceStaffId,
      imageSelectorId: this.imageSelectorId,
      action: this.actionValue,
      direction: this.directionValue,
      rawDirection: this.rawDirectionValue,
      selector: this.selectorValue,
      frame: this.getFrameState(),
      placement: this.placement(camera),
      alpha: this.alphaValue,
      scalePercent: this.scaleValue,
    };
  }
}

function requireImageSelector(metadata: CharacterMetadataRecord, bindingImageSelector: number): number {
  const metadataSelector = metadata.render?.image_selector?.id;
  if (metadataSelector === undefined || metadataSelector !== bindingImageSelector) {
    throw new Error(`V6 StaffData image selector mismatch for ${metadata.id}`);
  }
  return metadataSelector;
}

function readInitialAlpha(actor: { readonly initial_fields?: Readonly<Record<string, { readonly value: unknown }>> }): number {
  const value = actor.initial_fields?.alpha_?.value;
  return typeof value === "number" ? value : 0;
}

function validateAlpha(alpha: number): void {
  if (!Number.isSafeInteger(alpha) || alpha < 0 || alpha > 255) {
    throw new Error("V6 Staff alpha must be an integer in 0..255");
  }
}

function validateScale(scale: number): void {
  if (!Number.isSafeInteger(scale) || scale <= 0) {
    throw new Error("V6 Staff scale must be a positive integer percentage");
  }
}

function toSpawnFixtureLike(actor: unknown, actorId?: string): StaffSpawnFixtureLike {
  const raw = actor as {
    readonly id: string;
    readonly source_staff_id: number;
    readonly scene_ref: string;
    readonly spawn_cell: { readonly x: number; readonly y: number };
    readonly initial_position: { readonly x: number; readonly y: number };
  };
  return {
    id: actorId ?? raw.id,
    source_staff_id: raw.source_staff_id,
    scene_ref: raw.scene_ref,
    spawn_cell: { ...raw.spawn_cell },
    initial_position: { ...raw.initial_position },
  };
}
