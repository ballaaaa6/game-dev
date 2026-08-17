import type { LivingSnapshot } from "../../core/living/types";
import type {
  AgentBinding,
  AssignmentCommand,
  AssignmentCommandResult,
  AssignmentEvent,
  DashboardLivingReadModel,
  DashboardReadModel,
  TaskRecord,
} from "../assignment/types";

export type DashboardRuntimeStatus = "READY" | "RUNNING" | "DISPOSED";

export interface DashboardStaffRosterEntry {
  readonly staffId: number;
  readonly staffDataId: number;
  readonly actorId: string;
  readonly name: string;
  readonly jobId: number;
  readonly jobName: string;
  readonly skillId: number;
  readonly skillName: string;
  readonly boundExternalAgentId: string | null;
  readonly living: DashboardLivingReadModel;
  readonly source: "I0_RUNTIME_CATALOG";
}

export interface DashboardRuntimeSnapshot {
  readonly frame: number;
  readonly bridgeMode: DashboardReadModel["bridgeMode"];
  readonly runtimeStatus: DashboardRuntimeStatus;
  readonly living: LivingSnapshot;
  readonly dashboard: DashboardReadModel;
  readonly staffRoster: readonly DashboardStaffRosterEntry[];
  readonly unboundStaff: readonly DashboardStaffRosterEntry[];
  readonly bindings: readonly AgentBinding[];
  readonly tasks: readonly TaskRecord[];
  readonly events: readonly AssignmentEvent[];
  readonly livingDigest: string;
  readonly assignmentDigest: string;
  readonly lastCommandResult: AssignmentCommandResult | null;
}

export type DashboardSnapshotListener = (snapshot: DashboardRuntimeSnapshot) => void;

export type DashboardRuntimeCommand = AssignmentCommand;
