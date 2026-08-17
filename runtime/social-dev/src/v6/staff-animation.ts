import type { V4ResourceManager } from "../v4";
import type { StaffAction, StaffFrameState, StaffSelectorResolution } from "./contracts";

export function frameIntervalForStaffAction(action: string): number {
  return action === "typing" || action === "talk" ? 3 : 1;
}

export class StaffAnimationV6 {
  public constructor(
    private readonly resources: V4ResourceManager,
    private selector: StaffSelectorResolution,
    private frame = 0,
  ) {}

  public get currentSelector(): StaffSelectorResolution {
    return this.selector;
  }

  public get currentFrame(): number {
    return this.frame;
  }

  public get frameBound(): number | null {
    if (this.selector.selectorId === null) {
      return null;
    }
    return this.resources.getSeb(this.selector.selectorId).getMaxFrame();
  }

  public setSelector(selector: StaffSelectorResolution, frame = 0): void {
    this.selector = selector;
    this.frame = selector.selectorId === null ? 0 : normalizeFrame(frame, this.resources.getSeb(selector.selectorId).getMaxFrame());
  }

  public setFrame(frame: number): void {
    const bound = this.frameBound;
    if (bound === null) {
      this.frame = 0;
      return;
    }
    this.frame = normalizeFrame(frame, bound);
  }

  public advance(interval = 1, reservedSelector: StaffSelectorResolution | null = null): void {
    if (!Number.isSafeInteger(interval) || interval < 0) {
      throw new Error("V6 Staff frame interval must be a non-negative integer");
    }
    const bound = this.frameBound;
    if (bound === null) {
      return;
    }
    const next = this.frame + interval;
    const wrapped = next >= bound;
    this.frame = next % bound;
    if (wrapped && reservedSelector?.selectorId !== null && reservedSelector !== null) {
      this.setSelector(reservedSelector, this.frame);
    }
  }

  public state(action: string, sourceAction: string | null, frameInterval: number): StaffFrameState | null {
    const selectorId = this.selector.selectorId;
    const frameBound = this.frameBound;
    if (selectorId === null || frameBound === null) {
      return null;
    }
    return {
      selectorId,
      frame: this.frame,
      frameBound,
      frameInterval,
      action,
      sourceAction,
      proof: "CALL-FLOW-PROVEN",
    };
  }
}

function normalizeFrame(frame: number, bound: number): number {
  if (!Number.isSafeInteger(frame) || frame < 0 || !Number.isSafeInteger(bound) || bound <= 0) {
    throw new Error("V6 Staff frame is malformed");
  }
  return frame % bound;
}

export function isAnimationAction(action: string): action is StaffAction {
  return action.length > 0;
}
