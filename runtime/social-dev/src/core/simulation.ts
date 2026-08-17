import { loadRuntimeCatalogs, type RuntimeCatalogs } from "../catalog/load-contracts";
import { cellToActorWorld } from "../scene/coordinates";
import { digestState, withDigest } from "./digest";
import { createLivingRuntime, LivingRuntime } from "./living/runtime";
import { projectLivingStaffs } from "./living/projection";
import type { ActorState, Cell, RuntimeEvent, SimulationInput, SimulationState } from "./types";

function eventFromTrace(catalogs: RuntimeCatalogs, trace: SimulationState["living"]["traces"][number]): RuntimeEvent {
  const actorIds = trace.staffId === null ? [] : [`actor:staff:${trace.staffId}`];
  return {
    tick: trace.tick,
    type: trace.event,
    actorIds,
    ...(trace.rngSequence === null ? {} : { frame: trace.rngSequence }),
  };
}

function staticActor(actor: ActorState, cell: Cell, catalogs: RuntimeCatalogs): ActorState {
  return {
    ...actor,
    cell,
    position: cellToActorWorld(cell, catalogs.camera),
    lifecycle: "idle",
    route: [],
    routeCursor: 0,
    talkFrame: null,
    animation: {
      ...actor.animation,
      mode: "wait",
      frame: 0,
    },
  };
}

function baseLivingRuntime(catalogs: RuntimeCatalogs): LivingRuntime {
  return createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1, 2] });
}

export function createInitialState(catalogs: RuntimeCatalogs = loadRuntimeCatalogs()): SimulationState {
  const living = baseLivingRuntime(catalogs).snapshot();
  const actors = projectLivingStaffs(catalogs, living.staffs);
  const stateWithoutDigest = {
    frame: living.frame,
    sceneId: catalogs.displayScene.id,
    actors,
    living,
    events: [],
    eventLog: [],
    selectedActorId: catalogs.activeActors[0]?.id ?? null,
    tickOperations: catalogs.tickOrder.order.map((entry) => entry.operation),
  } as const;
  return withDigest(stateWithoutDigest);
}

export function applyFloor00DisplayPolicy(
  state: SimulationState,
  catalogs: RuntimeCatalogs,
): SimulationState {
  const actors = Object.fromEntries(Object.entries(state.actors).map(([id, actor]) => {
    const placement = catalogs.floor00DisplayPolicy.actors.find((candidate) => candidate.id === id);
    if (!placement) throw new Error(`Floor00 display policy is missing ${id}`);
    const cell = [placement.reserved_cell[0], placement.reserved_cell[1]] as const;
    return [id, staticActor(actor, cell, catalogs)];
  }));
  const { digest: _digest, ...stateWithoutDigest } = state;
  return withDigest({
    ...stateWithoutDigest,
    frame: 0,
    actors,
    events: [],
    eventLog: [],
  });
}

export function stepSimulation(
  state: SimulationState,
  catalogs: RuntimeCatalogs = loadRuntimeCatalogs(),
  input: SimulationInput = {},
): SimulationState {
  const runtime = LivingRuntime.fromSnapshot(catalogs, state.living);
  const living = runtime.tick();
  const actors = projectLivingStaffs(catalogs, living.staffs);
  const previousTraceCount = state.living.traces.length;
  const events = living.traces.slice(previousTraceCount).map((trace) => eventFromTrace(catalogs, trace));
  const selectedActorId = input.selectedActorId === undefined ? state.selectedActorId : input.selectedActorId;
  const eventLog = [...state.eventLog, ...events].slice(-80);
  const stateWithoutDigest = {
    frame: living.frame,
    sceneId: state.sceneId,
    actors,
    living,
    events,
    eventLog,
    selectedActorId,
    tickOperations: [...state.tickOperations],
  } as const;
  return withDigest(stateWithoutDigest);
}

export function runTicks(
  count: number,
  catalogs: RuntimeCatalogs = loadRuntimeCatalogs(),
  input: SimulationInput = {},
): SimulationState {
  let state = createInitialState(catalogs);
  for (let index = 0; index < count; index += 1) state = stepSimulation(state, catalogs, input);
  return state;
}

export function digestSequence(count: number, catalogs: RuntimeCatalogs = loadRuntimeCatalogs()): readonly string[] {
  const digests: string[] = [];
  let state = createInitialState(catalogs);
  digests.push(state.digest);
  for (let index = 0; index < count; index += 1) {
    state = stepSimulation(state, catalogs);
    digests.push(state.digest);
  }
  return digests;
}

export function stateDigestWithoutMutation(state: SimulationState): string {
  const { digest: _digest, ...stateWithoutDigest } = state;
  return digestState(stateWithoutDigest);
}
