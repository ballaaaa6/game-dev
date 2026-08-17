import type { RuntimeCatalogs } from "../catalog/load-contracts";
import { getCharacterAnimation } from "../assets/character-assets";
import { StaffFlag, StaffState } from "../core/living/constants";
import type { LivingCell, LivingSnapshot, LivingStaff } from "../core/living/types";
import {
  V8_DIRECTION_BY_RAW,
  V8_EQUIPMENT_SELECTORS,
  V8_FUKIDASHI_OFFSET_Y,
  V8_MOVE_SELECTORS,
  V8_RENDER_PASSES,
  V8_TALK_POOLS,
  V8_TYPING_SELECTORS,
  V8_WAIT_SELECTORS,
  type V8Direction,
  type V8FukidashiPayload,
  type V8InvitationVisual,
  type V8LiveSnapshot,
  type V8VisualAction,
  type V8VisualRngDraw,
  type V8VisualStaff,
} from "./contracts";
import { directionForRaw, rawDirectionForStep, selectorForDirection } from "./direction";
import {
  createFukidashi,
  isDrawableFukidashi,
  selectFukidashiId,
  updateFukidashi,
  type V8RandomSource,
} from "./fukidashi";

interface V8ReplayRandomOptions {
  readonly replay?: readonly number[];
  readonly seed?: number;
}

class V8ReplayRandom implements V8RandomSource {
  private readonly replay: readonly number[];
  private readonly recorded: V8VisualRngDraw[] = [];
  private replayIndex = 0;
  private stateValue: number;

  public constructor(options: V8ReplayRandomOptions = {}) {
    this.replay = options.replay ?? [];
    this.stateValue = (options.seed ?? 0x51c0de) >>> 0;
  }

  public get draws(): readonly V8VisualRngDraw[] {
    return this.recorded;
  }

  public get state(): number {
    return this.stateValue >>> 0;
  }

  public random(maxExclusive: number): number {
    if (!Number.isInteger(maxExclusive) || maxExclusive <= 0) {
      throw new Error(`V8 AppData.Random requires a positive exclusive bound, got ${maxExclusive}`);
    }
    let value: number;
    const replayValue = this.replay[this.replayIndex];
    if (replayValue !== undefined) {
      this.replayIndex += 1;
      value = ((Math.trunc(replayValue) % maxExclusive) + maxExclusive) % maxExclusive;
    } else {
      let x = this.stateValue >>> 0;
      x ^= x << 13;
      x ^= x >>> 17;
      x ^= x << 5;
      this.stateValue = x >>> 0;
      value = this.stateValue % maxExclusive;
    }
    this.recorded.push({
      sequence: this.recorded.length,
      stream: "AppData",
      method: "Random",
      min: 0,
      max: maxExclusive,
      exclusiveMax: true,
      value,
    });
    return value;
  }
}

interface MutableV8StaffVisual {
  rawDirection: number;
  alpha: number;
  bootstrapFadeIn: boolean;
  fukidashi: V8FukidashiPayload | null;
  previousCell: LivingCell;
}

interface MutableV8Invitation {
  initiatorId: number;
  targetId: number;
  startedAt: number;
  outcome: V8InvitationVisual["outcome"];
}

function cloneCell(cell: LivingCell): LivingCell {
  return [cell[0], cell[1]];
}

function clonePayload(payload: V8FukidashiPayload | null): V8FukidashiPayload | null {
  return payload ? { ...payload } : null;
}

function lifecycle(staff: LivingStaff): V8VisualStaff["lifecycle"] {
  switch (staff.state) {
    case StaffState.MOVE:
      return "move";
    case StaffState.WORK:
    case StaffState.USE_EQUIPMENT:
    case StaffState.INVITE_TO_TALK:
      return "work";
    case StaffState.TALK:
      return "talk";
    case StaffState.STAY_HOME:
    case StaffState.WAIT_BACK_OF_DOOR:
      return "home";
    case StaffState.NORMAL:
      return staff.frame === 0 ? "spawned" : "idle";
    default:
      return "idle";
  }
}

function actionForStaff(staff: LivingStaff): V8VisualAction {
  if (staff.state === StaffState.MOVE) return "move";
  if (staff.state === StaffState.TALK) return "talk";
  if (staff.state === StaffState.USE_EQUIPMENT) return "equipment";
  if ((staff.flags & StaffFlag.TYPING) !== 0) return "typing";
  return "wait";
}

function equipmentCell(snapshot: LivingSnapshot, staff: LivingStaff): LivingCell | null {
  const furniture = snapshot.room.furniture.find((item) => item.instanceId === staff.equipmentId);
  return furniture ? furniture.cell : null;
}

function selectorForStaff(snapshot: LivingSnapshot, staff: LivingStaff, rawDirection: number): number {
  const action = actionForStaff(staff);
  switch (action) {
    case "move":
      return V8_MOVE_SELECTORS[rawDirection] ?? V8_MOVE_SELECTORS[0]!;
    case "typing":
    case "talk":
      return V8_TYPING_SELECTORS[rawDirection] ?? V8_TYPING_SELECTORS[0]!;
    case "equipment": {
      const target = equipmentCell(snapshot, staff);
      const rightOfTarget = Boolean(target && staff.cell[0] > target[0]);
      if (staff.frame < 40) return rightOfTarget ? V8_EQUIPMENT_SELECTORS.frame20.rightOfTarget : V8_EQUIPMENT_SELECTORS.frame20.leftOfTarget;
      if (staff.frame < 60) return rightOfTarget ? V8_EQUIPMENT_SELECTORS.frame40.rightOfTarget : V8_EQUIPMENT_SELECTORS.frame40.leftOfTarget;
      return rightOfTarget ? V8_EQUIPMENT_SELECTORS.frame60.rightOfTarget : V8_EQUIPMENT_SELECTORS.frame60.leftOfTarget;
    }
    case "wait":
      return V8_WAIT_SELECTORS[rawDirection] ?? V8_WAIT_SELECTORS[0]!;
  }
}

function frameForStaff(staff: LivingStaff, action: V8VisualAction): number {
  if (action === "talk") return staff.talkFrame;
  if (action === "move") return staff.moveFrame;
  if (action === "equipment") return staff.frame;
  return staff.frame;
}

function findTraceSequence(snapshot: LivingSnapshot): number {
  const last = snapshot.traces.at(-1);
  return last?.sequence ?? -1;
}

export interface V8LiveRuntimeOptions {
  readonly appDataReplay?: readonly number[];
  readonly seed?: number;
}

/**
 * Deterministic visual state compiled from the authoritative I0 living
 * snapshot. It owns only display state (direction, alpha, full selectors and
 * Fukidashi payloads); product tasks never enter this runtime.
 */
export class V8LiveRuntime {
  private readonly catalogs: RuntimeCatalogs;
  private readonly random: V8ReplayRandom;
  private readonly staffs = new Map<number, MutableV8StaffVisual>();
  private readonly invitations = new Map<string, MutableV8Invitation>();
  private lastTraceSequence: number;
  private currentSnapshot: V8LiveSnapshot;

  public constructor(catalogs: RuntimeCatalogs, initial: LivingSnapshot, options: V8LiveRuntimeOptions = {}) {
    this.catalogs = catalogs;
    this.random = new V8ReplayRandom({ replay: options.appDataReplay, seed: options.seed });
    for (const staff of initial.staffs) {
      this.staffs.set(staff.id, {
        rawDirection: 0,
        alpha: staff.alpha,
        bootstrapFadeIn: staff.alpha < 255,
        fukidashi: null,
        previousCell: cloneCell(staff.cell),
      });
    }
    this.lastTraceSequence = findTraceSequence(initial);
    this.currentSnapshot = this.compile(initial);
  }

  public snapshot(): V8LiveSnapshot {
    return this.currentSnapshot;
  }

  public advance(snapshot: LivingSnapshot): V8LiveSnapshot {
    for (const staff of snapshot.staffs) {
      const visual = this.staffs.get(staff.id) ?? {
        rawDirection: 0,
        alpha: staff.alpha,
        bootstrapFadeIn: staff.alpha < 255,
        fukidashi: null,
        previousCell: cloneCell(staff.cell),
      };
      this.staffs.set(staff.id, visual);
      const nextCell = staff.route[0];
      const stepDirection = nextCell ? rawDirectionForStep(staff.cell, nextCell) : rawDirectionForStep(visual.previousCell, staff.cell);
      if (stepDirection !== null) visual.rawDirection = stepDirection;
      visual.previousCell = cloneCell(staff.cell);
      visual.fukidashi = updateFukidashi(visual.fukidashi);
      this.updateAlpha(visual, staff);
    }
    this.processNewTraces(snapshot);
    this.advanceInvitations(snapshot);
    this.currentSnapshot = this.compile(snapshot);
    return this.currentSnapshot;
  }

  private updateAlpha(visual: MutableV8StaffVisual, staff: LivingStaff): void {
    if ((staff.flags & StaffFlag.FADE_IN) !== 0) {
      visual.alpha = Math.min(255, visual.alpha + 25);
      if (visual.alpha >= 255) visual.bootstrapFadeIn = false;
      return;
    }
    if ((staff.flags & StaffFlag.FADE_OUT) !== 0) {
      visual.alpha = Math.max(0, visual.alpha - 25);
      return;
    }
    // Room.AddStaff is source-bounded at alpha=0. The live entry path then
    // exposes the same native +25 cadence so the freshly spawned staff can
    // actually enter the room before any home/door fade is requested.
    if (visual.bootstrapFadeIn && staff.state !== StaffState.WAIT_BACK_OF_DOOR) {
      visual.alpha = Math.min(255, visual.alpha + 25);
      if (visual.alpha >= 255) visual.bootstrapFadeIn = false;
    }
  }

  private processNewTraces(snapshot: LivingSnapshot): void {
    for (const trace of snapshot.traces) {
      if (trace.sequence <= this.lastTraceSequence) continue;
      if (trace.event === "talk-reserved-bilateral" && trace.staffId !== null && trace.colleagueId !== null) {
        const key = `${trace.staffId}:${trace.colleagueId}`;
        if (!this.invitations.has(key)) {
          this.invitations.set(key, {
            initiatorId: trace.staffId,
            targetId: trace.colleagueId,
            startedAt: trace.tick,
            outcome: "pending",
          });
        }
      }
      if (trace.event === "talk-frame-20-bubble" && trace.staffId !== null) {
        this.setBubble(trace.staffId, V8_TALK_POOLS.autonomousInitiator, "autonomous");
      }
      if (trace.event === "talk-frame-70-bubble" && trace.staffId !== null) {
        this.setBubble(trace.staffId, V8_TALK_POOLS.autonomousTarget, "autonomous");
      }
      this.lastTraceSequence = Math.max(this.lastTraceSequence, trace.sequence);
    }
  }

  private advanceInvitations(snapshot: LivingSnapshot): void {
    for (const invitation of this.invitations.values()) {
      if (invitation.outcome !== "pending") continue;
      const invitationFrame = snapshot.frame - invitation.startedAt;
      if (invitationFrame >= 20 && invitationFrame < 21) {
        this.setBubble(invitation.initiatorId, V8_TALK_POOLS.invitationOpening, "invitation");
      }
      if (invitationFrame >= 60) {
        const responseDraw = this.random.random(101);
        const busy = responseDraw <= 10;
        invitation.outcome = busy ? "busy" : "accepted";
        this.setBubble(
          invitation.targetId,
          busy ? V8_TALK_POOLS.invitationBusy : V8_TALK_POOLS.invitationResponse,
          "invitation",
        );
      }
    }
  }

  private setBubble(staffId: number, pool: readonly number[], source: V8FukidashiPayload["source"]): void {
    const visual = this.staffs.get(staffId);
    if (!visual || isDrawableFukidashi(visual.fukidashi)) return;
    const id = selectFukidashiId(pool, this.random);
    visual.fukidashi = createFukidashi(id, source, 0, V8_FUKIDASHI_OFFSET_Y);
  }

  private compile(snapshot: LivingSnapshot): V8LiveSnapshot {
    const unresolvedSelectors = new Set<string>();
    const staffs = snapshot.staffs.map((staff) => {
      const visual = this.staffs.get(staff.id)!;
      const rawDirection = visual.rawDirection;
      const direction = directionForRaw(rawDirection);
      const action = actionForStaff(staff);
      const selectorId = selectorForStaff(snapshot, staff, rawDirection);
      if (!getCharacterAnimation(selectorId)) unresolvedSelectors.add(`${staff.actorId}:${selectorId}`);
      const fukidashi = clonePayload(visual.fukidashi);
      return {
        id: staff.id,
        actorId: staff.actorId,
        staffDataId: staff.staffDataId,
        cell: cloneCell(staff.cell),
        world: { ...staff.world },
        rawDirection,
        direction,
        action,
        selectorId,
        frame: frameForStaff(staff, action),
        alpha: visual.alpha,
        visible: visual.alpha > 0 && staff.state !== StaffState.WAIT_BACK_OF_DOOR,
        lifecycle: lifecycle(staff),
        state: staff.state,
        moveMode: staff.moveMode,
        flags: staff.flags,
        deskId: staff.deskId,
        equipmentId: staff.equipmentId,
        colleagueId: staff.colleagueId,
        route: staff.route.map(cloneCell),
        fukidashi,
      } satisfies V8VisualStaff;
    });
    const invitations = [...this.invitations.values()]
      .map((invitation) => ({
        initiatorId: invitation.initiatorId,
        targetId: invitation.targetId,
        frame: Math.max(0, snapshot.frame - invitation.startedAt),
        outcome: invitation.outcome,
      } satisfies V8InvitationVisual))
      .sort((left, right) => left.initiatorId - right.initiatorId || left.targetId - right.targetId);
    const fukidashi = staffs
      .map((staff) => staff.fukidashi)
      .filter((payload): payload is V8FukidashiPayload => isDrawableFukidashi(payload));
    return {
      schema_version: "social-dev-v8-live-room0-v1",
      frame: snapshot.frame,
      roomId: "room:0",
      staffs,
      invitations,
      fukidashi,
      rngDraws: this.random.draws.map((draw) => ({ ...draw })),
      rngState: { state: this.random.state, sequence: this.random.draws.length },
      diagnostics: {
        fallbackMarkers: 0,
        unresolvedSelectors: [...unresolvedSelectors].sort(),
        renderPasses: V8_RENDER_PASSES,
      },
    };
  }
}

export function createV8LiveRuntime(
  catalogs: RuntimeCatalogs,
  initial: LivingSnapshot,
  options: V8LiveRuntimeOptions = {},
): V8LiveRuntime {
  return new V8LiveRuntime(catalogs, initial, options);
}
