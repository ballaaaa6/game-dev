import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { staffJobAndSkill, staffRecord, jobRecord, skillRecord } from "../../core/living/catalog";
import type { LivingRuntime } from "../../core/living/runtime";
import type { LivingSnapshot, LivingStaff } from "../../core/living/types";
import type { AssignmentBridge } from "../assignment/bridge";
import {
  AssignmentAdapter,
  assignmentDigest,
  assignmentReplayDigest,
  createAssignmentAdapter,
  projectLiving,
  type AgentBinding,
  type AssignmentCommand,
  type AssignmentCommandResult,
  type AssignmentEvent,
  type DashboardReadModel,
  type TaskRecord,
} from "../assignment";
import type {
  DashboardRuntimeCommand,
  DashboardRuntimeSnapshot,
  DashboardRuntimeStatus,
  DashboardSnapshotListener,
  DashboardStaffRosterEntry,
} from "./types";

function cloneLivingSnapshot(snapshot: LivingSnapshot): LivingSnapshot {
  return {
    frame: snapshot.frame,
    room: {
      ...snapshot.room,
      objMap: snapshot.room.objMap.map((row) => [...row]),
      objDir: snapshot.room.objDir.map((row) => [...row]),
      furniture: snapshot.room.furniture.map((furniture) => ({
        ...furniture,
        cell: [furniture.cell[0], furniture.cell[1]],
        activeUserIds: [...furniture.activeUserIds],
        reservedUserIds: [...furniture.reservedUserIds],
      })),
      staffIds: [...snapshot.room.staffIds],
    },
    staffs: snapshot.staffs.map((staff) => ({
      ...staff,
      cell: [staff.cell[0], staff.cell[1]],
      world: { ...staff.world },
      route: staff.route.map((cell) => [cell[0], cell[1]]),
      lastNode: staff.lastNode ? [staff.lastNode[0], staff.lastNode[1]] : null,
      goalCell: staff.goalCell ? [staff.goalCell[0], staff.goalCell[1]] : null,
    })),
    player: { ...snapshot.player },
    traces: snapshot.traces.map((trace) => ({
      ...trace,
      cell: trace.cell ? [trace.cell[0], trace.cell[1]] : null,
      route: trace.route.map((cell) => [cell[0], cell[1]]),
    })),
    rngDraws: snapshot.rngDraws.map((draw) => ({ ...draw })),
    rngState: { ...snapshot.rngState },
    rngReplay: { appData: [...snapshot.rngReplay.appData], lib: [...snapshot.rngReplay.lib] },
    meetingPointGauge: snapshot.meetingPointGauge,
  };
}

function cloneBinding(binding: AgentBinding): AgentBinding {
  return { ...binding };
}

function cloneTask(task: TaskRecord): TaskRecord {
  return { ...task };
}

function cloneEvent(event: AssignmentEvent): AssignmentEvent {
  return { ...event };
}

function cloneResult(result: AssignmentCommandResult | null): AssignmentCommandResult | null {
  if (!result) return null;
  return {
    ...result,
    agent: result.agent ? cloneBinding(result.agent) : null,
    task: result.task ? cloneTask(result.task) : null,
  };
}

function nameField(record: { readonly fields: Record<string, unknown> }, key: string, fallback: string): string {
  const value = record.fields[key];
  return typeof value === "string" && value.trim().length > 0 ? value : fallback;
}

function staffRosterEntry(
  catalogs: RuntimeCatalogs,
  snapshot: LivingSnapshot,
  staff: LivingStaff,
  bindingByStaff: ReadonlyMap<number, AgentBinding>,
): DashboardStaffRosterEntry {
  const staffData = staffRecord(catalogs, staff.staffDataId);
  const { jobId, skillId } = staffJobAndSkill(catalogs, staff.staffDataId);
  const job = jobRecord(catalogs, jobId);
  const skill = skillRecord(catalogs, skillId);
  return {
    staffId: staff.id,
    staffDataId: staff.staffDataId,
    actorId: staff.actorId,
    name: `${nameField(staffData, "firstName_", "Staff")} ${nameField(staffData, "lastName_", String(staff.staffDataId))}`,
    jobId,
    jobName: nameField(job, "name_", `Job ${jobId}`),
    skillId,
    skillName: nameField(skill, "name_", `Skill ${skillId}`),
    boundExternalAgentId: bindingByStaff.get(staff.id)?.externalAgentId ?? null,
    living: projectLiving(staff, snapshot),
    source: "I0_RUNTIME_CATALOG",
  };
}

export class DashboardRuntime {
  public readonly living: LivingRuntime;
  public readonly assignmentAdapter: AssignmentAdapter;
  private readonly catalogs: RuntimeCatalogs;
  private readonly subscribers = new Set<DashboardSnapshotListener>();
  private committedLivingSnapshot: LivingSnapshot;
  private runtimeStatus: DashboardRuntimeStatus = "READY";
  private lastCommandResult: AssignmentCommandResult | null = null;
  private lastSnapshot: DashboardRuntimeSnapshot;

  public constructor(living: LivingRuntime, bridge?: AssignmentBridge) {
    this.living = living;
    this.catalogs = living.catalogs;
    this.assignmentAdapter = createAssignmentAdapter(living, bridge);
    this.committedLivingSnapshot = living.snapshot();
    this.lastSnapshot = this.buildSnapshot();
  }

  public get status(): DashboardRuntimeStatus {
    return this.runtimeStatus;
  }

  public getSnapshot(): DashboardRuntimeSnapshot {
    return this.buildSnapshot();
  }

  public getDashboardReadModel(): DashboardReadModel {
    return this.assignmentAdapter.readModel(this.committedLivingSnapshot);
  }

  public getStaffRoster(): readonly DashboardStaffRosterEntry[] {
    return this.buildStaffRoster();
  }

  public getBindings(): readonly AgentBinding[] {
    return this.assignmentAdapter.snapshot().bindings.map(cloneBinding);
  }

  public getTasks(): readonly TaskRecord[] {
    return this.sortedTasks();
  }

  public getEvents(): readonly AssignmentEvent[] {
    return this.assignmentAdapter.events().map(cloneEvent);
  }

  public getLastCommandResult(): AssignmentCommandResult | null {
    return cloneResult(this.lastCommandResult);
  }

  public subscribe(listener: DashboardSnapshotListener): () => void {
    this.subscribers.add(listener);
    return () => {
      this.subscribers.delete(listener);
    };
  }

  /** The single scheduled living step for the production dashboard runtime. */
  public tick(): DashboardRuntimeSnapshot {
    this.assertUsable();
    const committed = this.living.tick();
    this.committedLivingSnapshot = cloneLivingSnapshot(committed);
    this.assignmentAdapter.observeLiving(this.committedLivingSnapshot);
    this.lastCommandResult = null;
    return this.publish();
  }

  public step(count = 1): DashboardRuntimeSnapshot {
    if (!Number.isInteger(count) || count < 0) {
      throw new Error("Dashboard scheduler step count must be a non-negative integer");
    }
    let snapshot = this.getSnapshot();
    for (let index = 0; index < count; index += 1) snapshot = this.tick();
    return snapshot;
  }

  public execute(command: DashboardRuntimeCommand): AssignmentCommandResult {
    this.assertUsable();
    const result = this.assignmentAdapter.execute(command);
    this.committedLivingSnapshot = cloneLivingSnapshot(this.living.snapshot());
    this.lastCommandResult = cloneResult(result);
    this.publish();
    return cloneResult(result) as AssignmentCommandResult;
  }

  public bindAgent(externalAgentId: string, staffId: number, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "bind_agent", externalAgentId, staffId, commandId });
  }

  public unbindAgent(externalAgentId: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "unbind_agent", externalAgentId, commandId });
  }

  public assignTask(externalTaskId: string, externalAgentId: string, label?: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "assign_task", externalTaskId, externalAgentId, label, commandId });
  }

  public startTask(externalTaskId: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "start_task", externalTaskId, commandId });
  }

  public updateTaskProgress(externalTaskId: string, externalProgress: number, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "update_task_progress", externalTaskId, externalProgress, commandId });
  }

  public completeTask(externalTaskId: string, reason?: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "complete_task", externalTaskId, reason, commandId });
  }

  public failTask(externalTaskId: string, reason?: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "fail_task", externalTaskId, reason, commandId });
  }

  public cancelTask(externalTaskId: string, reason?: string, commandId?: string): AssignmentCommandResult {
    return this.execute({ type: "cancel_task", externalTaskId, reason, commandId });
  }

  public replayDigest(): string {
    const adapter = this.assignmentAdapter.snapshot();
    return assignmentReplayDigest(adapter, this.getDashboardReadModel(), this.committedLivingSnapshot);
  }

  public dispose(): void {
    if (this.runtimeStatus === "DISPOSED") return;
    this.runtimeStatus = "DISPOSED";
    this.subscribers.clear();
    this.lastSnapshot = this.buildSnapshot();
  }

  private assertUsable(): void {
    if (this.runtimeStatus === "DISPOSED") throw new Error("DashboardRuntime is disposed");
  }

  private publish(): DashboardRuntimeSnapshot {
    this.lastSnapshot = this.buildSnapshot();
    for (const subscriber of this.subscribers) subscriber(this.buildSnapshot());
    return this.getSnapshot();
  }

  private buildSnapshot(): DashboardRuntimeSnapshot {
    const adapterSnapshot = this.assignmentAdapter.snapshot();
    const bindings = adapterSnapshot.bindings.map(cloneBinding);
    const bindingByStaff = new Map(bindings.map((binding) => [binding.staffId, binding]));
    const dashboard = this.assignmentAdapter.readModel(this.committedLivingSnapshot);
    const staffRoster = this.buildStaffRoster(bindingByStaff);
    const tasks = this.sortedTasks();
    const events = adapterSnapshot.events.slice().sort((left, right) => left.sequence - right.sequence).map(cloneEvent);
    const living = cloneLivingSnapshot(this.committedLivingSnapshot);
    return {
      frame: living.frame,
      bridgeMode: dashboard.bridgeMode,
      runtimeStatus: this.runtimeStatus,
      living,
      dashboard,
      staffRoster,
      unboundStaff: staffRoster.filter((staff) => staff.boundExternalAgentId === null),
      bindings,
      tasks,
      events,
      livingDigest: assignmentDigest(living),
      assignmentDigest: assignmentReplayDigest(adapterSnapshot, dashboard, living),
      lastCommandResult: cloneResult(this.lastCommandResult),
    };
  }

  private buildStaffRoster(bindingByStaff = new Map<number, AgentBinding>()): readonly DashboardStaffRosterEntry[] {
    return this.committedLivingSnapshot.staffs
      .slice()
      .sort((left, right) => left.id - right.id)
      .map((staff) => staffRosterEntry(this.catalogs, this.committedLivingSnapshot, staff, bindingByStaff));
  }

  private sortedTasks(): readonly TaskRecord[] {
    return this.assignmentAdapter.snapshot().tasks
      .slice()
      .sort((left, right) => left.externalTaskId.localeCompare(right.externalTaskId))
      .map(cloneTask);
  }
}

export function createDashboardRuntime(living: LivingRuntime, bridge?: AssignmentBridge): DashboardRuntime {
  return new DashboardRuntime(living, bridge);
}
