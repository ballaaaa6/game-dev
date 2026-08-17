import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { cellToActorWorld } from "../../scene/coordinates";
import { MoveMode, StaffFlag, StaffState } from "./constants";
import { searchRoute } from "./astar";
import type { LivingCell, LivingStaff } from "./types";

type MutableStaffBase = { -readonly [Key in keyof LivingStaff]: LivingStaff[Key] };

export type MutableStaff = Omit<MutableStaffBase, "cell" | "world" | "route" | "lastNode" | "goalCell"> & {
  cell: LivingCell;
  world: { x: number; y: number };
  route: LivingCell[];
  lastNode: LivingCell | null;
  goalCell: LivingCell | null;
};

export function mutableStaff(staff: LivingStaff): MutableStaff {
  return staff as unknown as MutableStaff;
}

export interface RouteBuildResult {
  readonly path: readonly LivingCell[];
  readonly goalFlags: number;
}

export function buildStaffRoute(
  catalogs: RuntimeCatalogs,
  staff: LivingStaff,
  target: LivingCell,
  goalFlags: number,
): RouteBuildResult {
  const path = searchRoute(catalogs, staff.cell, target, { goal: { cell: target, allowOccupiedTarget: true, goalType: goalFlags } });
  return { path, goalFlags };
}

export function installRoute(
  catalogs: RuntimeCatalogs,
  staff: LivingStaff,
  target: LivingCell,
  goalFlags: number,
): RouteBuildResult {
  const mutable = mutableStaff(staff);
  const result = buildStaffRoute(catalogs, staff, target, goalFlags);
  mutable.route = result.path.slice(1).map((cell) => [cell[0], cell[1]] as const);
  mutable.goalCell = [target[0], target[1]];
  mutable.goalFlags = goalFlags;
  return result;
}

export function clearRoute(staff: LivingStaff): void {
  const mutable = mutableStaff(staff);
  mutable.route = [];
  mutable.goalCell = null;
  mutable.goalFlags = 0;
}

export function onArriveNextNode(staff: LivingStaff, catalogs: RuntimeCatalogs): boolean {
  const mutable = mutableStaff(staff);
  if (mutable.route.length === 0) return true;
  const next = mutable.route.shift()!;
  mutable.lastNode = [mutable.cell[0], mutable.cell[1]];
  mutable.cell = [next[0], next[1]];
  mutable.world = cellToActorWorld(mutable.cell, catalogs.camera);
  return mutable.route.length === 0;
}

export function applyBasicArrival(staff: LivingStaff, moveMode: number): void {
  const mutable = mutableStaff(staff);
  mutable.frame = 0;
  switch (moveMode) {
    case MoveMode.GOTO_EQUIPMENT:
      mutable.state = StaffState.USE_EQUIPMENT;
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.WANDER:
      mutable.state = StaffState.WANDER;
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.GOTO_DESK:
      mutable.moveMode = MoveMode.SIT_DOWN;
      break;
    case MoveMode.INTO_EQUIPMENT:
      mutable.state = StaffState.INVITE_TO_TALK;
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.OUTOF_EQUIPMENT:
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.SIT_DOWN:
      mutable.state = StaffState.WORK;
      mutable.flags |= StaffFlag.SITTING;
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.TO_STAND_TALKING:
      mutable.state = StaffState.TALK;
      mutable.moveMode = MoveMode.STAY;
      mutable.talkFrame = 0;
      break;
    case MoveMode.TO_BACK_OF_CHAIR:
      mutable.state = StaffState.INVITE_TO_TALK;
      mutable.moveMode = MoveMode.STAY;
      break;
    case MoveMode.GO_HOME:
      mutable.state = StaffState.STAY_HOME;
      mutable.moveMode = MoveMode.STAY;
      break;
    default:
      mutable.moveMode = MoveMode.STAY;
      break;
  }
}
