import type { LivingCell } from "../core/living/types";

export type V8Direction = "right" | "left" | "up" | "down";
export type V8VisualAction = "move" | "wait" | "typing" | "talk" | "equipment";

export const V8_RENDER_PASSES = [
  "map-extension-floor",
  "map-chip",
  "object-chip-primary",
  "object-chip-wall",
  "avatar-primary",
  "avatar-secondary",
  "object-chip-late-preview",
  "object-chip-late",
  "map-floor",
] as const;

export type V8RenderPass = (typeof V8_RENDER_PASSES)[number];

export const V8_RAW_DIRECTIONS = {
  left: 0,
  right: 1,
  down: 2,
  up: 3,
} as const satisfies Record<V8Direction, number>;

export const V8_DIRECTION_BY_RAW: readonly V8Direction[] = ["left", "right", "down", "up"];

export const V8_WAIT_SELECTORS: readonly number[] = [11, 10, 13, 12];
export const V8_TYPING_SELECTORS: readonly number[] = [24, 23, 26, 25];
export const V8_MOVE_SELECTORS: readonly number[] = [2, 1, 4, 3];

export const V8_EQUIPMENT_SELECTORS = {
  frame20: { leftOfTarget: 8, rightOfTarget: 7 },
  frame40: { leftOfTarget: 16, rightOfTarget: 15 },
  frame60: { leftOfTarget: 12, rightOfTarget: 11 },
} as const;

export const V8_TALK_POOLS = {
  invitationOpening: [25, 26, 27, 28, 29, 68],
  invitationResponse: [22, 23, 24],
  invitationBusy: [44, 45, 46],
  autonomousInitiator: [30, 31, 32, 33, 34],
  autonomousTarget: [35, 36, 37, 38, 39, 40, 41, 42, 43],
} as const;

export const V8_FUKIDASHI_LIFETIME = 40;
export const V8_FUKIDASHI_OFFSET_Y = 0;

/** The accepted English localization slice used by the live Room0 renderer. */
export const V8_ENGLISH_FUKIDASHI: Readonly<Record<number, string>> = {
  22: "Yeees",
  23: "What could it be?",
  24: "Yes, yes...",
  25: "Hey, listen...",
  26: "Umm...",
  27: "Is now a good time?",
  28: "Sorry",
  29: "Hey you",
  30: "About this...",
  31: "In that case...",
  32: "And then...",
  33: "...",
  34: "By the way...",
  35: "Hmm",
  36: "Yep yep",
  37: "Of course!",
  38: "Huh?",
  39: "Amazing!",
  40: "As expected!",
  41: "Wow!",
  42: "Hmm...",
  43: "I dunno...",
  44: "I’m busy",
  45: "Sorry...",
  46: "Later!",
  68: "...",
};

export interface V8FukidashiPayload {
  readonly id: number;
  readonly lifetime: number;
  readonly delay: number;
  readonly offsetY: number;
  readonly text: string;
  readonly source: "invitation" | "autonomous";
}

export interface V8VisualStaff {
  readonly id: number;
  readonly actorId: string;
  readonly staffDataId: number;
  readonly cell: LivingCell;
  readonly world: { readonly x: number; readonly y: number };
  readonly rawDirection: number;
  readonly direction: V8Direction;
  readonly action: V8VisualAction;
  readonly selectorId: number;
  readonly frame: number;
  readonly alpha: number;
  readonly visible: boolean;
  readonly lifecycle: "spawned" | "idle" | "move" | "work" | "talk" | "home";
  readonly state: number;
  readonly moveMode: number;
  readonly flags: number;
  readonly deskId: number;
  readonly equipmentId: number;
  readonly colleagueId: number;
  readonly route: readonly LivingCell[];
  readonly fukidashi: V8FukidashiPayload | null;
}

export interface V8VisualRngDraw {
  readonly sequence: number;
  readonly stream: "AppData";
  readonly method: "Random";
  readonly min: number;
  readonly max: number;
  readonly exclusiveMax: true;
  readonly value: number;
}

export interface V8InvitationVisual {
  readonly initiatorId: number;
  readonly targetId: number;
  readonly frame: number;
  readonly outcome: "pending" | "accepted" | "busy";
}

export interface V8LiveSnapshot {
  readonly schema_version: "social-dev-v8-live-room0-v1";
  readonly frame: number;
  readonly roomId: "room:0";
  readonly staffs: readonly V8VisualStaff[];
  readonly invitations: readonly V8InvitationVisual[];
  readonly fukidashi: readonly V8FukidashiPayload[];
  readonly rngDraws: readonly V8VisualRngDraw[];
  readonly rngState: { readonly state: number; readonly sequence: number };
  readonly diagnostics: {
    readonly fallbackMarkers: number;
    readonly unresolvedSelectors: readonly string[];
    readonly renderPasses: readonly V8RenderPass[];
  };
}
