import type { ActorRecord } from "../../catalog/types";
import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { resolveCharacterAction } from "../../catalog/character-resolver";
import type { ActorState, Cell } from "../types";
import { StaffFlag, StaffState } from "./constants";
import type { LivingStaff } from "./types";

function actorRecord(catalogs: RuntimeCatalogs, actorId: string): ActorRecord {
  const record = catalogs.actors.actors.find((candidate) => candidate.id === actorId);
  if (!record) throw new Error(`ActorCatalog is missing ${actorId}`);
  return record;
}

function selectorId(catalogs: RuntimeCatalogs, actor: ActorRecord, mode: "wait" | "typing"): number {
  const resolved = resolveCharacterAction(catalogs, actor.id, mode, "right");
  if (!resolved.selector || resolved.selector.status !== "selector_ready") {
    throw new Error(`Shared animation selector for ${actor.id} is not resolved`);
  }
  return resolved.selector.selector_id;
}

function lifecycle(staff: LivingStaff): ActorState["lifecycle"] {
  switch (staff.state) {
    case StaffState.MOVE:
      return "move";
    case StaffState.WORK:
    case StaffState.USE_EQUIPMENT:
    case StaffState.INVITE_TO_TALK:
      return "work";
    case StaffState.TALK:
      return "talk";
    case StaffState.NORMAL:
      return staff.frame === 0 ? "spawned" : "idle";
    default:
      return "idle";
  }
}

export function projectLivingStaff(catalogs: RuntimeCatalogs, staff: LivingStaff): ActorState {
  const record = actorRecord(catalogs, staff.actorId);
  const mode = (staff.flags & StaffFlag.TYPING) !== 0 || staff.state === StaffState.TALK ? "typing" : "wait";
  const cell: Cell = [staff.cell[0], staff.cell[1]];
  return {
    id: staff.actorId,
    sourceId: staff.staffDataId,
    name: `${String((record.name.values as Record<string, unknown>).English ?? staff.staffDataId)}`,
    cell,
    position: { ...staff.world },
    alpha: staff.alpha,
    speed: staff.speed,
    lifecycle: lifecycle(staff),
    facing: "right",
    route: staff.route.map((routeCell) => [routeCell[0], routeCell[1]] as const),
    routeCursor: 0,
    talkFrame: staff.state === StaffState.TALK ? staff.talkFrame : null,
    animation: {
      mode,
      frame: staff.state === StaffState.TALK ? staff.talkFrame : staff.frame,
      selectorId: selectorId(catalogs, record, mode),
    },
  };
}

export function projectLivingStaffs(catalogs: RuntimeCatalogs, staffs: readonly LivingStaff[]): Readonly<Record<string, ActorState>> {
  return Object.fromEntries(staffs.map((staff) => [staff.actorId, projectLivingStaff(catalogs, staff)]));
}
