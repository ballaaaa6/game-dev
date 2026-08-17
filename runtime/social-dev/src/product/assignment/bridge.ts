import type { TaskRecord } from "./types";
import type { BridgeMode } from "./types";

export interface BridgeLease {
  readonly bridgeMode: BridgeMode;
  readonly contextKind: "product_overlay";
  readonly originalContextOwned: false;
}

export interface AssignmentBridge {
  readonly mode: BridgeMode;
  enter(task: TaskRecord): BridgeLease;
  exit(task: TaskRecord, reason: string): BridgeLease;
  isActive(externalTaskId: string): boolean;
  activeTaskIds(): readonly string[];
}

/**
 * Bridge C deliberately has no LivingRuntime mutator. It gives the product
 * lifecycle a named, testable bridge boundary while I0 continues to own all
 * movement, autonomy, equipment, talk, HP, and home behavior.
 */
export class ProductTaskOverlayBridge implements AssignmentBridge {
  public readonly mode = "PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING" as const;
  private readonly active = new Set<string>();

  public enter(task: TaskRecord): BridgeLease {
    if (this.active.has(task.externalTaskId)) throw new Error(`Task bridge is already active:${task.externalTaskId}`);
    this.active.add(task.externalTaskId);
    return { bridgeMode: this.mode, contextKind: "product_overlay", originalContextOwned: false };
  }

  public exit(task: TaskRecord, _reason: string): BridgeLease {
    if (!this.active.has(task.externalTaskId)) throw new Error(`Task bridge is not active:${task.externalTaskId}`);
    this.active.delete(task.externalTaskId);
    return { bridgeMode: this.mode, contextKind: "product_overlay", originalContextOwned: false };
  }

  public isActive(externalTaskId: string): boolean {
    return this.active.has(externalTaskId);
  }

  public activeTaskIds(): readonly string[] {
    return [...this.active].sort();
  }
}

export function createProductTaskOverlayBridge(): ProductTaskOverlayBridge {
  return new ProductTaskOverlayBridge();
}
