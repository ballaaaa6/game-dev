import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { LivingSnapshot } from "./living/types";
import type { V8LiveSnapshot } from "../v8/contracts";

export type Cell = readonly [number, number];
export type Lifecycle = "spawned" | "idle" | "move" | "work" | "talk";
export type AnimationMode = "wait" | "typing";

export interface WorldPosition {
  readonly x: number;
  readonly y: number;
}

export interface ActorState {
  readonly id: string;
  readonly sourceId: number;
  readonly name: string;
  readonly cell: Cell;
  readonly position: WorldPosition;
  readonly alpha: number;
  readonly speed: number;
  readonly lifecycle: Lifecycle;
  readonly facing: "left" | "right" | "up" | "down";
  readonly route: readonly Cell[];
  readonly routeCursor: number;
  readonly talkFrame: number | null;
  readonly animation: {
    readonly mode: AnimationMode;
    readonly frame: number;
    readonly selectorId: number;
  };
}

export interface RuntimeEvent {
  readonly tick: number;
  readonly type: string;
  readonly actorIds: readonly string[];
  readonly frame?: number;
}

export interface SimulationState {
  readonly frame: number;
  readonly sceneId: string;
  readonly actors: Readonly<Record<string, ActorState>>;
  readonly events: readonly RuntimeEvent[];
  readonly eventLog: readonly RuntimeEvent[];
  readonly selectedActorId: string | null;
  readonly tickOperations: readonly string[];
  readonly living: LivingSnapshot;
  /** Present only for the authorized V8 live Room0 route. */
  readonly v8?: V8LiveSnapshot;
  readonly digest: string;
}

export interface SimulationInput {
  readonly selectedActorId?: string | null;
}

export interface RuntimeSnapshot {
  readonly state: SimulationState;
  readonly catalogs: RuntimeCatalogs;
}
