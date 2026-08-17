import type { LivingSnapshot, LivingStaff } from "../../core/living/types";
import type {
  AssignmentEvent,
  AssignmentEventType,
  AssignmentErrorCode,
  BridgeMode,
  ProductTaskStatus,
  TaskStatus,
} from "./types";

export interface EventContext {
  readonly commandId: string;
  readonly type: AssignmentEventType;
  readonly externalAgentId?: string | null;
  readonly externalTaskId?: string | null;
  readonly staffId?: number | null;
  readonly productStatusBefore?: ProductTaskStatus | null;
  readonly productStatusAfter?: ProductTaskStatus | null;
  readonly living?: LivingStaff | null;
  readonly livingFrame: number;
  readonly bridgeMode: BridgeMode;
  readonly reason?: string | null;
  readonly code?: "OK" | AssignmentErrorCode | null;
  readonly originalContextOwned?: boolean;
}

export function createAssignmentEvent(sequence: number, context: EventContext): AssignmentEvent {
  return {
    sequence,
    commandId: context.commandId,
    type: context.type,
    externalAgentId: context.externalAgentId ?? null,
    externalTaskId: context.externalTaskId ?? null,
    staffId: context.staffId ?? null,
    productStatusBefore: context.productStatusBefore ?? null,
    productStatusAfter: context.productStatusAfter ?? null,
    livingStateAtEvent: context.living?.state ?? null,
    livingMoveModeAtEvent: context.living?.moveMode ?? null,
    livingFrame: context.livingFrame,
    bridgeMode: context.bridgeMode,
    reason: context.reason ?? null,
    code: context.code ?? null,
    originalContextOwned: context.originalContextOwned ?? false,
  };
}

export function currentProductStatus(status: TaskStatus | null): ProductTaskStatus | null {
  return status;
}

export function cloneAssignmentEvent(event: AssignmentEvent): AssignmentEvent {
  return { ...event };
}

export function snapshotStaff(snapshot: LivingSnapshot, staffId: number | null | undefined): LivingStaff | null {
  if (staffId === null || staffId === undefined) return null;
  return snapshot.staffs.find((staff) => staff.id === staffId) ?? null;
}
