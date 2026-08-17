import type { LivingRuntime } from "../../core/living/runtime";
import { MoveMode, StaffState } from "../../core/living/constants";
import type { LivingSnapshot, LivingStaff } from "../../core/living/types";
import { createAssignmentEvent, snapshotStaff } from "./events";
import { buildDashboardReadModel } from "./read-model";
import { assignmentReplayDigest } from "./snapshot";
import { createProductTaskOverlayBridge, type AssignmentBridge } from "./bridge";
import type {
  AgentBinding,
  AssignmentAdapterSnapshot,
  AssignmentCommand,
  AssignmentCommandResult,
  AssignmentErrorCode,
  AssignmentEvent,
  DashboardReadModel,
  TaskRecord,
  TaskStatus,
} from "./types";

const terminalStatuses = new Set<TaskStatus>(["COMPLETED", "FAILED", "CANCELLED"]);
const activeStatuses = new Set<TaskStatus>(["ASSIGNED", "RUNNING"]);

function cloneBinding(binding: AgentBinding): AgentBinding {
  return { ...binding };
}

function cloneTask(task: TaskRecord): TaskRecord {
  return { ...task };
}

function cloneSnapshot(snapshot: AssignmentAdapterSnapshot): AssignmentAdapterSnapshot {
  return {
    bridgeMode: snapshot.bridgeMode,
    bindings: snapshot.bindings.map(cloneBinding),
    tasks: snapshot.tasks.map(cloneTask),
    activeBridgeTaskIds: [...snapshot.activeBridgeTaskIds],
    events: snapshot.events.map((event) => ({ ...event })),
  };
}

function nonEmpty(value: string): boolean {
  return value.trim().length > 0;
}

function statusOrNull(task: TaskRecord | null): TaskStatus | null {
  return task?.status ?? null;
}

function sameLivingState(left: LivingStaff, right: LivingStaff): boolean {
  return left.state === right.state
    && left.moveMode === right.moveMode
    && left.hp === right.hp
    && left.deskId === right.deskId
    && left.equipmentId === right.equipmentId
    && left.colleagueId === right.colleagueId
    && left.cell[0] === right.cell[0]
    && left.cell[1] === right.cell[1];
}

function interruptionReason(previous: LivingStaff, current: LivingStaff): string | null {
  if (current.state === StaffState.USE_EQUIPMENT || current.equipmentId >= 0) return "equipment_detour";
  if (current.state === StaffState.TALK || current.state === StaffState.INVITE_TO_TALK || current.colleagueId >= 0 || current.moveMode === MoveMode.TO_STAFF || current.moveMode === MoveMode.TO_STAND_TALKING || current.moveMode === MoveMode.TO_BACK_OF_CHAIR) return "talk_detour";
  if (current.state === StaffState.STAY_HOME || current.moveMode === MoveMode.GO_TO_DOOR || current.moveMode === MoveMode.GO_HOME) return "low_hp_home_path";
  if (previous.deskId >= 0 && current.deskId < 0) return "desk_destroyed";
  if (previous.deskId < 0 && current.deskId >= 0) return "desk_reacquired";
  if (current.state === StaffState.MOVE || previous.state === StaffState.MOVE) return "living_route_transition";
  return null;
}

function isResumeState(staff: LivingStaff): boolean {
  return staff.state === StaffState.WORK || staff.state === StaffState.NORMAL || staff.state === StaffState.WAIT_BACK_OF_DOOR;
}

export class AssignmentAdapter {
  public readonly living: LivingRuntime;
  public readonly bridge: AssignmentBridge;
  private readonly bindingByAgent = new Map<string, AgentBinding>();
  private readonly agentByStaff = new Map<number, string>();
  private readonly taskById = new Map<string, TaskRecord>();
  private readonly eventLog: AssignmentEvent[] = [];
  private readonly activeBridgeTasks = new Set<string>();
  private readonly interruptedAgents = new Set<string>();
  private commandSequence = 0;
  private eventSequence = 0;
  private lastLivingSnapshot: LivingSnapshot;

  public constructor(living: LivingRuntime, bridge: AssignmentBridge = createProductTaskOverlayBridge()) {
    this.living = living;
    this.bridge = bridge;
    this.lastLivingSnapshot = living.snapshot();
  }

  public bindAgent(externalAgentId: string, staffId: number, commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    if (!nonEmpty(externalAgentId)) return this.reject(command, "INVALID_ARGUMENT", externalAgentId, null, staffId);
    if (this.bindingByAgent.has(externalAgentId) || this.agentByStaff.has(staffId)) return this.reject(command, "AGENT_BINDING_CONFLICT", externalAgentId, null, staffId);
    const staff = this.livingStaff(staffId);
    if (!staff) return this.reject(command, "STAFF_NOT_FOUND", externalAgentId, null, staffId);
    const binding: AgentBinding = { externalAgentId, staffId, boundSequence: command.sequence };
    this.bindingByAgent.set(externalAgentId, binding);
    this.agentByStaff.set(staffId, externalAgentId);
    const event = this.emit(command, "agent_bound", { externalAgentId, staffId, living: staff, productStatusAfter: "IDLE_NO_TASK" });
    return this.accept(event.sequence, binding, null);
  }

  public unbindAgent(externalAgentId: string, commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    const binding = this.bindingByAgent.get(externalAgentId);
    if (!binding) return this.reject(command, "AGENT_NOT_BOUND", externalAgentId, null, null);
    const active = this.activeTaskFor(externalAgentId);
    if (active) return this.reject(command, "ACTIVE_TASK_PREVENTS_UNBIND", externalAgentId, active, binding.staffId);
    this.bindingByAgent.delete(externalAgentId);
    this.agentByStaff.delete(binding.staffId);
    const event = this.emit(command, "agent_unbound", { externalAgentId, staffId: binding.staffId, living: this.livingStaff(binding.staffId), productStatusBefore: "IDLE_NO_TASK", productStatusAfter: "IDLE_NO_TASK" });
    return this.accept(event.sequence, null, null);
  }

  public assignTask(externalTaskId: string, externalAgentId: string, label?: string, commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    const binding = this.bindingByAgent.get(externalAgentId);
    if (!binding) return this.reject(command, "AGENT_NOT_BOUND", externalAgentId, null, null);
    if (!nonEmpty(externalTaskId)) return this.reject(command, "INVALID_ARGUMENT", externalAgentId, null, binding.staffId);
    if (this.taskById.has(externalTaskId)) return this.reject(command, "TASK_ALREADY_EXISTS", externalAgentId, this.taskById.get(externalTaskId) ?? null, binding.staffId);
    const active = this.activeTaskFor(externalAgentId);
    if (active) return this.reject(command, "ACTIVE_TASK_CONFLICT", externalAgentId, active, binding.staffId);
    const task: TaskRecord = {
      externalTaskId,
      externalAgentId,
      staffId: binding.staffId,
      status: "ASSIGNED",
      label: label?.trim() || null,
      externalProgress: 0,
      bridgeMode: this.bridge.mode,
      bridgeContextOwned: false,
      createdSequence: command.sequence,
      assignedSequence: command.sequence,
      startedSequence: null,
      terminalSequence: null,
      terminalReason: null,
    };
    this.taskById.set(externalTaskId, task);
    const event = this.emit(command, "task_assigned", { externalAgentId, externalTaskId, staffId: binding.staffId, living: this.livingStaff(binding.staffId), productStatusBefore: "IDLE_NO_TASK", productStatusAfter: "ASSIGNED" });
    return this.accept(event.sequence, binding, task);
  }

  public startTask(externalTaskId: string, commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    const task = this.taskById.get(externalTaskId);
    if (!task) return this.reject(command, "TASK_NOT_FOUND", null, null, null, externalTaskId);
    const binding = this.bindingByAgent.get(task.externalAgentId) ?? null;
    if (!binding) return this.reject(command, "AGENT_NOT_BOUND", task.externalAgentId, task, task.staffId, externalTaskId);
    if (task.status !== "ASSIGNED") return this.reject(command, "INVALID_TASK_TRANSITION", task.externalAgentId, task, task.staffId, externalTaskId);
    try {
      this.bridge.enter(task);
    } catch {
      return this.reject(command, "ORIGINAL_BRIDGE_UNAVAILABLE", task.externalAgentId, task, task.staffId, externalTaskId);
    }
    this.activeBridgeTasks.add(externalTaskId);
    const started: TaskRecord = { ...task, status: "RUNNING", startedSequence: command.sequence, bridgeContextOwned: false };
    this.taskById.set(externalTaskId, started);
    const contextEvent = this.emit(command, "original_context_enter", { externalAgentId: task.externalAgentId, externalTaskId, staffId: task.staffId, living: this.livingStaff(task.staffId), productStatusBefore: "ASSIGNED", productStatusAfter: "ASSIGNED", reason: "product_overlay_entered_without_native_living_mutation", originalContextOwned: false });
    const event = this.emit(command, "task_started", { externalAgentId: task.externalAgentId, externalTaskId, staffId: task.staffId, living: this.livingStaff(task.staffId), productStatusBefore: "ASSIGNED", productStatusAfter: "RUNNING", originalContextOwned: false });
    return this.accept(event.sequence, binding, this.taskById.get(externalTaskId) ?? started, contextEvent.sequence);
  }

  public completeTask(externalTaskId: string, reason = "completed_by_command", commandId?: string): AssignmentCommandResult {
    return this.terminalTask(externalTaskId, "COMPLETED", reason, "task_completed", commandId);
  }

  public failTask(externalTaskId: string, reason = "failed_by_command", commandId?: string): AssignmentCommandResult {
    return this.terminalTask(externalTaskId, "FAILED", reason, "task_failed", commandId);
  }

  public cancelTask(externalTaskId: string, reason = "cancelled_by_command", commandId?: string): AssignmentCommandResult {
    return this.terminalTask(externalTaskId, "CANCELLED", reason, "task_cancelled", commandId);
  }

  public updateTaskProgress(externalTaskId: string, externalProgress: number, commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    const task = this.taskById.get(externalTaskId);
    if (!task) return this.reject(command, "TASK_NOT_FOUND", null, null, null, externalTaskId);
    const binding = this.bindingByAgent.get(task.externalAgentId) ?? null;
    if (!binding) return this.reject(command, "AGENT_NOT_BOUND", task.externalAgentId, task, task.staffId, externalTaskId);
    if (!activeStatuses.has(task.status) || !Number.isFinite(externalProgress)) return this.reject(command, "INVALID_TASK_TRANSITION", task.externalAgentId, task, task.staffId, externalTaskId);
    const next = { ...task, externalProgress: Math.max(0, Math.min(100, externalProgress)) };
    this.taskById.set(externalTaskId, next);
    const event = this.emit(command, "task_progressed", { externalAgentId: task.externalAgentId, externalTaskId, staffId: task.staffId, living: this.livingStaff(task.staffId), productStatusBefore: task.status, productStatusAfter: next.status, reason: `external_progress:${next.externalProgress}` });
    return this.accept(event.sequence, binding, next);
  }

  public execute(command: AssignmentCommand): AssignmentCommandResult {
    switch (command.type) {
      case "bind_agent": return this.bindAgent(command.externalAgentId, command.staffId, command.commandId);
      case "unbind_agent": return this.unbindAgent(command.externalAgentId, command.commandId);
      case "assign_task": return this.assignTask(command.externalTaskId, command.externalAgentId, command.label, command.commandId);
      case "start_task": return this.startTask(command.externalTaskId, command.commandId);
      case "complete_task": return this.completeTask(command.externalTaskId, command.reason, command.commandId);
      case "fail_task": return this.failTask(command.externalTaskId, command.reason, command.commandId);
      case "cancel_task": return this.cancelTask(command.externalTaskId, command.reason, command.commandId);
      case "update_task_progress": return this.updateTaskProgress(command.externalTaskId, command.externalProgress, command.commandId);
    }
  }

  /** Observe I0 transitions without writing any product or living field. */
  public observeLiving(snapshot: LivingSnapshot = this.living.snapshot()): DashboardReadModel {
    for (const binding of this.bindingByAgent.values()) {
      const previous = this.lastLivingSnapshot.staffs.find((staff) => staff.id === binding.staffId);
      const current = snapshot.staffs.find((staff) => staff.id === binding.staffId);
      const task = this.activeTaskFor(binding.externalAgentId);
      if (!previous || !current || !task || sameLivingState(previous, current)) continue;
      const reason = interruptionReason(previous, current);
      if (reason && !this.interruptedAgents.has(binding.externalAgentId)) {
        this.interruptedAgents.add(binding.externalAgentId);
        this.emit({ sequence: this.nextCommandSequence(), commandId: `observe:${snapshot.frame}:${binding.externalAgentId}` }, "living_interruption_observed", { externalAgentId: binding.externalAgentId, externalTaskId: task.externalTaskId, staffId: binding.staffId, living: current, livingFrame: snapshot.frame, productStatusBefore: task.status, productStatusAfter: task.status, reason });
      } else if (!reason && this.interruptedAgents.has(binding.externalAgentId) && isResumeState(current)) {
        this.interruptedAgents.delete(binding.externalAgentId);
        this.emit({ sequence: this.nextCommandSequence(), commandId: `observe:${snapshot.frame}:${binding.externalAgentId}` }, "living_resumed_observed", { externalAgentId: binding.externalAgentId, externalTaskId: task.externalTaskId, staffId: binding.staffId, living: current, livingFrame: snapshot.frame, productStatusBefore: task.status, productStatusAfter: task.status, reason: "baseline_living_resumed" });
      }
    }
    this.lastLivingSnapshot = snapshot;
    return this.readModel(snapshot);
  }

  public readModel(snapshot: LivingSnapshot = this.living.snapshot()): DashboardReadModel {
    return buildDashboardReadModel([...this.bindingByAgent.values()], [...this.taskById.values()], snapshot, this.bridge);
  }

  public snapshot(): AssignmentAdapterSnapshot {
    return cloneSnapshot({
      bridgeMode: this.bridge.mode,
      bindings: [...this.bindingByAgent.values()].sort((left, right) => left.externalAgentId.localeCompare(right.externalAgentId)),
      tasks: [...this.taskById.values()],
      activeBridgeTaskIds: this.bridge.activeTaskIds(),
      events: this.eventLog,
    });
  }

  public events(): readonly AssignmentEvent[] {
    return this.snapshot().events;
  }

  public replayDigest(): string {
    return assignmentReplayDigest(this.snapshot(), this.readModel(), this.living.snapshot());
  }

  private terminalTask(externalTaskId: string, status: Extract<TaskStatus, "COMPLETED" | "FAILED" | "CANCELLED">, reason: string, eventType: "task_completed" | "task_failed" | "task_cancelled", commandId?: string): AssignmentCommandResult {
    const command = this.beginCommand(commandId);
    const task = this.taskById.get(externalTaskId);
    if (!task) return this.reject(command, "TASK_NOT_FOUND", null, null, null, externalTaskId);
    const binding = this.bindingByAgent.get(task.externalAgentId) ?? null;
    if (!binding) return this.reject(command, "AGENT_NOT_BOUND", task.externalAgentId, task, task.staffId, externalTaskId);
    if (!activeStatuses.has(task.status)) return this.reject(command, "INVALID_TASK_TRANSITION", task.externalAgentId, task, task.staffId, externalTaskId);
    if (this.activeBridgeTasks.has(externalTaskId)) {
      try {
        this.bridge.exit(task, reason);
      } catch {
        return this.reject(command, "ORIGINAL_BRIDGE_UNAVAILABLE", task.externalAgentId, task, task.staffId, externalTaskId);
      }
      this.activeBridgeTasks.delete(externalTaskId);
      this.emit(command, "original_context_exit", { externalAgentId: task.externalAgentId, externalTaskId, staffId: task.staffId, living: this.livingStaff(task.staffId), productStatusBefore: task.status, productStatusAfter: task.status, reason, originalContextOwned: false });
    }
    const terminal: TaskRecord = { ...task, status, terminalSequence: command.sequence, terminalReason: reason };
    this.taskById.set(externalTaskId, terminal);
    const event = this.emit(command, eventType, { externalAgentId: task.externalAgentId, externalTaskId, staffId: task.staffId, living: this.livingStaff(task.staffId), productStatusBefore: task.status, productStatusAfter: status, reason, originalContextOwned: false });
    return this.accept(event.sequence, binding, terminal);
  }

  private beginCommand(commandId?: string): { readonly sequence: number; readonly commandId: string } {
    const sequence = this.nextCommandSequence();
    return { sequence, commandId: commandId ?? `command:${sequence}` };
  }

  private nextCommandSequence(): number {
    this.commandSequence += 1;
    return this.commandSequence;
  }

  private accept(eventSequence: number, agent: AgentBinding | null, task: TaskRecord | null, _firstEventSequence?: number): AssignmentCommandResult {
    return { accepted: true, code: "OK", eventSequence, agent: agent ? cloneBinding(agent) : null, task: task ? cloneTask(task) : null };
  }

  private reject(command: { readonly sequence: number; readonly commandId: string }, code: AssignmentErrorCode, externalAgentId: string | null, task: TaskRecord | null, staffId: number | null, externalTaskId: string | null = null): AssignmentCommandResult {
    const event = this.emit(command, "command_rejected", { externalAgentId, externalTaskId, staffId, living: this.livingStaff(staffId), productStatusBefore: statusOrNull(task), productStatusAfter: statusOrNull(task), reason: code, code });
    const binding = externalAgentId ? this.bindingByAgent.get(externalAgentId) ?? null : null;
    return { accepted: false, code, eventSequence: event.sequence, agent: binding ? cloneBinding(binding) : null, task: task ? cloneTask(task) : null };
  }

  private emit(command: { readonly sequence: number; readonly commandId: string }, type: Parameters<typeof createAssignmentEvent>[1]["type"], context: Omit<Parameters<typeof createAssignmentEvent>[1], "type" | "commandId" | "livingFrame" | "bridgeMode"> & { readonly livingFrame?: number }): AssignmentEvent {
    const event = createAssignmentEvent(this.eventSequence++, {
      ...context,
      commandId: command.commandId,
      type,
      livingFrame: context.livingFrame ?? this.living.frame,
      bridgeMode: this.bridge.mode,
    });
    this.eventLog.push(event);
    return event;
  }

  private livingStaff(staffId: number | null): LivingStaff | null {
    return staffId === null ? null : snapshotStaff(this.living.snapshot(), staffId);
  }

  private activeTaskFor(externalAgentId: string): TaskRecord | null {
    const tasks = [...this.taskById.values()].filter((task) => task.externalAgentId === externalAgentId && activeStatuses.has(task.status));
    return tasks[tasks.length - 1] ?? null;
  }
}

export function createAssignmentAdapter(living: LivingRuntime, bridge?: AssignmentBridge): AssignmentAdapter {
  return new AssignmentAdapter(living, bridge);
}
