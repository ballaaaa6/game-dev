import type { GraphicsCommand } from "../v2/graphics";
import type { V4CameraBoundary, V4Cell, V4CommandTrace, V4Point, V4ResourceManager } from "../v4";
import type {
  V5CommandEvent,
  V5PassResult,
  V5Proof,
  V5RoomRenderResult,
} from "../v5/contracts";

export type V6Proof = V5Proof;

export type HumanDirection = "right" | "left" | "up" | "down";

export type StaffAction =
  | "move"
  | "wait"
  | "typing"
  | "talk"
  | "work"
  | "equipment"
  | "sit_down"
  | "meeting"
  | "invite_to_talk"
  | "wander"
  | "stay_home"
  | "fly_away"
  | "chara_sample00"
  | "walk"
  | "native";

export type StaffResolutionStatus = "resolved" | "fallback" | "deferred" | "unsupported";

export interface StaffSelectorResolution {
  readonly action: string;
  readonly sourceAction: string | null;
  readonly fallbackAction: string | null;
  readonly direction: HumanDirection | null;
  readonly rawDirection: number | null;
  readonly reverseDirection: number | null;
  readonly selectorId: number | null;
  readonly selectorFilename: string | null;
  readonly status: StaffResolutionStatus;
  readonly proof: V6Proof;
  readonly note: string | null;
}

export interface StaffPlacementV6 {
  readonly sceneId: string;
  readonly actorId: string;
  readonly sourceStaffId: number;
  readonly cell: V4Cell;
  readonly world: V4Point;
  readonly screen: V4Point;
  readonly cameraOffset: { readonly x: number; readonly y: number };
  readonly coordinateFormula: { readonly x: string; readonly y: string };
  readonly proof: V6Proof;
}

export interface StaffFrameState {
  readonly selectorId: number;
  readonly frame: number;
  readonly frameBound: number;
  readonly frameInterval: number;
  readonly action: string;
  readonly sourceAction: string | null;
  readonly proof: V6Proof;
}

export interface StaffDrawResult {
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly V4CommandTrace[];
  readonly placement: StaffPlacementV6;
  readonly selector: StaffSelectorResolution;
  readonly frame: StaffFrameState | null;
  readonly commandCount: number;
  readonly skipped: boolean;
  readonly skipReason: string | null;
}

export interface StaffV6Snapshot {
  readonly actorId: string;
  readonly sourceStaffId: number;
  readonly imageSelectorId: number;
  readonly action: string;
  readonly direction: HumanDirection | null;
  readonly rawDirection: number | null;
  readonly selector: StaffSelectorResolution;
  readonly frame: StaffFrameState | null;
  readonly placement: StaffPlacementV6;
  readonly alpha: number;
  readonly scalePercent: number;
}

export interface V6IntegratedPassResult extends V5PassResult {
  readonly inputCount: number;
}

export interface V6IntegratedRenderResult {
  readonly base: V5RoomRenderResult;
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly V4CommandTrace[];
  readonly events: readonly V5CommandEvent[];
  readonly passes: readonly V6IntegratedPassResult[];
  readonly camera: V4CameraBoundary;
  readonly resources: V4ResourceManager;
  readonly staff: readonly StaffV6Snapshot[];
  readonly staffDraws: readonly StaffDrawResult[];
  readonly integration: {
    readonly passId: "avatar-primary";
    readonly index: number;
    readonly nativeRelation: "SOURCE-LIMITED";
    readonly ordering: string;
    readonly occlusion: string;
  };
}

export interface V6RoomStaffManifest {
  readonly schemaVersion: 1;
  readonly phase: "V6";
  readonly roomKey: string;
  readonly dataKey: string;
  readonly cameraOffset: { readonly x: number; readonly y: number };
  readonly passOrder: readonly string[];
  readonly passes: readonly V6IntegratedPassResult[];
  readonly events: readonly V5CommandEvent[];
  readonly traces: readonly V4CommandTrace[];
  readonly commands: readonly GraphicsCommand[];
  readonly staff: readonly StaffV6Snapshot[];
  readonly integration: V6IntegratedRenderResult["integration"];
  readonly baseline: {
    readonly phase: "V5";
    readonly commandCount: number;
    readonly traceCount: number;
    readonly eventCount: number;
    readonly passCount: number;
  };
  readonly policy: {
    readonly productionCutover: false;
    readonly gameplay: false;
    readonly serverProof: false;
    readonly exactPixels: "DEFERRED_TO_V7";
  };
}
