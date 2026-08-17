import type { MoveMode, StaffState } from "../../core/living/constants";

export type BridgeMode = "PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING";

export type TaskStatus = "ASSIGNED" | "RUNNING" | "COMPLETED" | "FAILED" | "CANCELLED";

export type ProductTaskStatus = TaskStatus | "IDLE_NO_TASK";

export type AssignmentErrorCode =
  | "AGENT_NOT_BOUND"
  | "STAFF_NOT_FOUND"
  | "TASK_NOT_FOUND"
  | "TASK_ALREADY_EXISTS"
  | "ACTIVE_TASK_CONFLICT"
  | "INVALID_TASK_TRANSITION"
  | "AGENT_BINDING_CONFLICT"
  | "ORIGINAL_BRIDGE_UNAVAILABLE"
  | "ACTIVE_TASK_PREVENTS_UNBIND"
  | "INVALID_ARGUMENT";

export interface AgentBinding {
  readonly externalAgentId: string;
  readonly staffId: number;
  readonly boundSequence: number;
}

export interface TaskRecord {
  readonly externalTaskId: string;
  readonly externalAgentId: string;
  readonly staffId: number;
  readonly status: TaskStatus;
  readonly label: string | null;
  readonly externalProgress: number;
  readonly bridgeMode: BridgeMode;
  readonly bridgeContextOwned: boolean;
  readonly createdSequence: number;
  readonly assignedSequence: number;
  readonly startedSequence: number | null;
  readonly terminalSequence: number | null;
  readonly terminalReason: string | null;
}

export type AssignmentCommand =
  | {
      readonly type: "bind_agent";
      readonly commandId?: string;
      readonly externalAgentId: string;
      readonly staffId: number;
    }
  | {
      readonly type: "unbind_agent";
      readonly commandId?: string;
      readonly externalAgentId: string;
    }
  | {
      readonly type: "assign_task";
      readonly commandId?: string;
      readonly externalTaskId: string;
      readonly externalAgentId: string;
      readonly label?: string;
    }
  | {
      readonly type: "start_task";
      readonly commandId?: string;
      readonly externalTaskId: string;
    }
  | {
      readonly type: "complete_task";
      readonly commandId?: string;
      readonly externalTaskId: string;
      readonly reason?: string;
    }
  | {
      readonly type: "fail_task";
      readonly commandId?: string;
      readonly externalTaskId: string;
      readonly reason?: string;
    }
  | {
      readonly type: "cancel_task";
      readonly commandId?: string;
      readonly externalTaskId: string;
      readonly reason?: string;
    }
  | {
      readonly type: "update_task_progress";
      readonly commandId?: string;
      readonly externalTaskId: string;
      readonly externalProgress: number;
    };

export type AssignmentEventType =
  | "agent_bound"
  | "agent_unbound"
  | "task_assigned"
  | "task_started"
  | "task_progressed"
  | "task_completed"
  | "task_failed"
  | "task_cancelled"
  | "original_context_enter"
  | "original_context_exit"
  | "living_interruption_observed"
  | "living_resumed_observed"
  | "command_rejected";

export interface AssignmentEvent {
  readonly sequence: number;
  readonly commandId: string;
  readonly type: AssignmentEventType;
  readonly externalAgentId: string | null;
  readonly externalTaskId: string | null;
  readonly staffId: number | null;
  readonly productStatusBefore: TaskStatus | "IDLE_NO_TASK" | null;
  readonly productStatusAfter: TaskStatus | "IDLE_NO_TASK" | null;
  readonly livingStateAtEvent: StaffState | null;
  readonly livingMoveModeAtEvent: MoveMode | null;
  readonly livingFrame: number;
  readonly bridgeMode: BridgeMode;
  readonly reason: string | null;
  readonly code: "OK" | AssignmentErrorCode | null;
  readonly originalContextOwned: boolean;
}

export interface AssignmentAdapterState {
  readonly bridgeMode: BridgeMode;
  readonly bindings: readonly AgentBinding[];
  readonly tasks: readonly TaskRecord[];
  readonly activeBridgeTaskIds: readonly string[];
  readonly events: readonly AssignmentEvent[];
}

export type AssignmentAdapterSnapshot = AssignmentAdapterState;

export type LivingDisplayStatus =
  | "AT_DESK"
  | "MOVING"
  | "TALKING"
  | "USING_EQUIPMENT"
  | "HOME"
  | "RETURNING"
  | "WANDERING"
  | "WAITING"
  | "PLANNING"
  | "DEVELOPING";

export interface DashboardLivingReadModel {
  readonly state: StaffState;
  readonly stateName: string;
  readonly moveMode: MoveMode;
  readonly moveModeName: string;
  readonly flags: number;
  readonly hp: number;
  readonly maxHp: number;
  readonly hpRatio: number;
  readonly deskId: number;
  readonly equipmentId: number;
  readonly colleagueId: number;
  readonly atHome: boolean;
  readonly planning: boolean;
  readonly developing: boolean;
  readonly livingDisplayStatus: LivingDisplayStatus;
  readonly cell: readonly [number, number];
  readonly world: { readonly x: number; readonly y: number };
  readonly routeLength: number;
  readonly livingFrame: number;
}

export interface DashboardTaskReadModel {
  readonly externalTaskId: string | null;
  readonly status: ProductTaskStatus;
  readonly label: string | null;
  readonly externalProgress: number | null;
  readonly bridgeMode: BridgeMode;
  readonly terminalReason: string | null;
}

export interface DashboardAgentReadModel {
  readonly externalAgentId: string;
  readonly staffId: number;
  readonly staffDataId: number;
  readonly task: DashboardTaskReadModel;
  readonly living: DashboardLivingReadModel;
  readonly availability: "AVAILABLE" | "BOUND" | "TASK_ACTIVE" | "TASK_TERMINAL";
}

export interface DashboardReadModel {
  readonly bridgeMode: BridgeMode;
  readonly frame: number;
  readonly agents: readonly DashboardAgentReadModel[];
}

export interface AssignmentCommandResult {
  readonly accepted: boolean;
  readonly code: "OK" | AssignmentErrorCode;
  readonly eventSequence: number | null;
  readonly agent: AgentBinding | null;
  readonly task: TaskRecord | null;
}
