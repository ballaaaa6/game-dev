import { MoveMode, StaffFlag, StaffState } from "../../core/living/constants";
import type { LivingSnapshot, LivingStaff } from "../../core/living/types";
import type { AssignmentBridge } from "./bridge";
import type { AgentBinding, DashboardAgentReadModel, DashboardLivingReadModel, DashboardReadModel, DashboardTaskReadModel, TaskRecord } from "./types";

const stateNames: Record<number, string> = {
  [StaffState.NORMAL]: "STATE_NORMAL",
  [StaffState.MEETING]: "STATE_MEETING",
  [StaffState.MOVE]: "STATE_MOVE",
  [StaffState.SIT_DOWN]: "STATE_SIT_DOWN",
  [StaffState.WORK]: "STATE_WORK",
  [StaffState.USE_EQUIPMENT]: "STATE_USE_EQUIPMENT",
  [StaffState.TALK]: "STATE_TALK",
  [StaffState.INVITE_TO_TALK]: "STATE_INVITE_TO_TALK",
  [StaffState.FLY_AWAY]: "STATE_FLY_AWAY",
  [StaffState.WAIT]: "STATE_WAIT",
  [StaffState.WANDER]: "STATE_WANDER",
  [StaffState.WAIT_BACK_OF_DOOR]: "STATE_WAIT_BACK_OF_DOOR",
  [StaffState.DEVELOP]: "STATE_DEVELOP",
  [StaffState.STAY_HOME]: "STATE_STAY_HOME",
};

const moveModeNames: Record<number, string> = {
  [MoveMode.STAY]: "MOVE_MODE_STAY",
  [MoveMode.GOTO_EQUIPMENT]: "MOVE_MODE_GOTO_EQUIPMENT",
  [MoveMode.WANDER]: "MOVE_MODE_WANDER",
  [MoveMode.GOTO_DESK]: "MOVE_MODE_GOTO_DESK",
  [MoveMode.INTO_EQUIPMENT]: "MOVE_MODE_INTO_EQUIPMENT",
  [MoveMode.OUTOF_EQUIPMENT]: "MOVE_MODE_OUTOF_EQUIPMENT",
  [MoveMode.SIT_DOWN]: "MOVE_MODE_SIT_DOWN",
  [MoveMode.TO_STAFF]: "MOVE_MODE_TO_STAFF",
  [MoveMode.TO_STAND_TALKING]: "MOVE_MODE_TO_STAND_TALKING",
  [MoveMode.TO_BACK_OF_CHAIR]: "MOVE_MODE_TO_BACK_OF_CHAIR",
  [MoveMode.GO_TO_DOOR]: "MOVE_MODE_GO_TO_DOOR",
  [MoveMode.GO_HOME]: "MOVE_MODE_GO_HOME",
};

function livingDisplayStatus(staff: LivingStaff, planning: boolean): DashboardLivingReadModel["livingDisplayStatus"] {
  if (planning) return "PLANNING";
  if (staff.state === StaffState.DEVELOP) return "DEVELOPING";
  if (staff.state === StaffState.TALK || staff.state === StaffState.INVITE_TO_TALK || staff.moveMode === MoveMode.TO_STAND_TALKING || staff.moveMode === MoveMode.TO_BACK_OF_CHAIR) return "TALKING";
  if (staff.state === StaffState.USE_EQUIPMENT || staff.moveMode === MoveMode.GOTO_EQUIPMENT || staff.moveMode === MoveMode.INTO_EQUIPMENT || staff.moveMode === MoveMode.OUTOF_EQUIPMENT) return "USING_EQUIPMENT";
  if (staff.state === StaffState.STAY_HOME || staff.moveMode === MoveMode.GO_HOME || staff.moveMode === MoveMode.GO_TO_DOOR) return staff.state === StaffState.STAY_HOME ? "HOME" : "RETURNING";
  if (staff.moveMode !== MoveMode.STAY || staff.state === StaffState.MOVE) return "MOVING";
  if (staff.state === StaffState.WORK && (staff.flags & StaffFlag.SITTING) !== 0) return "AT_DESK";
  if (staff.state === StaffState.WANDER) return "WANDERING";
  return "WAITING";
}

export function projectLiving(staff: LivingStaff, snapshot: LivingSnapshot): DashboardLivingReadModel {
  return {
    state: staff.state,
    stateName: stateNames[staff.state] ?? `STATE_${staff.state}`,
    moveMode: staff.moveMode,
    moveModeName: moveModeNames[staff.moveMode] ?? `MOVE_MODE_${staff.moveMode}`,
    flags: staff.flags,
    hp: staff.hp,
    maxHp: staff.maxHp,
    hpRatio: Math.trunc((staff.hp * 100) / Math.max(1, staff.maxHp)),
    deskId: staff.deskId,
    equipmentId: staff.equipmentId,
    colleagueId: staff.colleagueId,
    atHome: staff.state === StaffState.STAY_HOME || staff.moveMode === MoveMode.GO_HOME,
    planning: snapshot.player.planning,
    developing: staff.state === StaffState.DEVELOP,
    livingDisplayStatus: livingDisplayStatus(staff, snapshot.player.planning),
    cell: [staff.cell[0], staff.cell[1]],
    world: { ...staff.world },
    routeLength: staff.route.length,
    livingFrame: snapshot.frame,
  };
}

function latestTask(tasks: readonly TaskRecord[], externalAgentId: string): TaskRecord | null {
  const matches = tasks.filter((task) => task.externalAgentId === externalAgentId);
  return matches.length === 0 ? null : matches[matches.length - 1] ?? null;
}

function taskModel(task: TaskRecord | null, bridge: AssignmentBridge): DashboardTaskReadModel {
  if (!task) return { externalTaskId: null, status: "IDLE_NO_TASK", label: null, externalProgress: null, bridgeMode: bridge.mode, terminalReason: null };
  return {
    externalTaskId: task.externalTaskId,
    status: task.status,
    label: task.label,
    externalProgress: task.externalProgress,
    bridgeMode: task.bridgeMode,
    terminalReason: task.terminalReason,
  };
}

function availability(task: TaskRecord | null): DashboardAgentReadModel["availability"] {
  if (!task) return "BOUND";
  if (task.status === "ASSIGNED" || task.status === "RUNNING") return "TASK_ACTIVE";
  return "TASK_TERMINAL";
}

export function buildDashboardReadModel(
  bindings: readonly AgentBinding[],
  tasks: readonly TaskRecord[],
  snapshot: LivingSnapshot,
  bridge: AssignmentBridge,
): DashboardReadModel {
  const agents = bindings.map((binding) => {
    const staff = snapshot.staffs.find((candidate) => candidate.id === binding.staffId);
    if (!staff) return null;
    const task = latestTask(tasks, binding.externalAgentId);
    return {
      externalAgentId: binding.externalAgentId,
      staffId: staff.id,
      staffDataId: staff.staffDataId,
      task: taskModel(task, bridge),
      living: projectLiving(staff, snapshot),
      availability: availability(task),
    } satisfies DashboardAgentReadModel;
  }).filter((agent): agent is DashboardAgentReadModel => agent !== null);
  return { bridgeMode: bridge.mode, frame: snapshot.frame, agents };
}

export function stateName(state: StaffState): string {
  return stateNames[state] ?? `STATE_${state}`;
}

export function moveModeName(moveMode: MoveMode): string {
  return moveModeNames[moveMode] ?? `MOVE_MODE_${moveMode}`;
}
