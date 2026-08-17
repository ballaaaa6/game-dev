import type { ActorState, SimulationState } from "./types";

type JsonValue = null | boolean | number | string | readonly JsonValue[] | { readonly [key: string]: JsonValue };

function toJsonValue(value: unknown): JsonValue {
  if (value === null || typeof value === "boolean" || typeof value === "number" || typeof value === "string") {
    return value;
  }
  if (Array.isArray(value)) {
    return value.map(toJsonValue);
  }
  if (typeof value === "object" && value !== null) {
    const record = value as Record<string, unknown>;
    return Object.fromEntries(Object.keys(record).sort().map((key) => [key, toJsonValue(record[key])])) as {
      readonly [key: string]: JsonValue;
    };
  }
  return String(value);
}

export function stableStringify(value: unknown): string {
  return JSON.stringify(toJsonValue(value));
}

function hash64(input: string): string {
  let hash = 1469598103934665603n;
  for (let index = 0; index < input.length; index += 1) {
    hash ^= BigInt(input.charCodeAt(index));
    hash = BigInt.asUintN(64, hash * 1099511628211n);
  }
  return hash.toString(16).padStart(16, "0");
}

function actorDigest(actor: ActorState): unknown {
  return {
    id: actor.id,
    sourceId: actor.sourceId,
    cell: actor.cell,
    position: actor.position,
    lifecycle: actor.lifecycle,
    facing: actor.facing,
    route: actor.route,
    routeCursor: actor.routeCursor,
    talkFrame: actor.talkFrame,
    animation: actor.animation,
  };
}

export function digestState(state: Omit<SimulationState, "digest">): string {
  return hash64(stableStringify({
    frame: state.frame,
    sceneId: state.sceneId,
    actors: Object.fromEntries(Object.keys(state.actors).sort().map((id) => [id, actorDigest(state.actors[id])])),
    events: state.events,
    selectedActorId: state.selectedActorId,
    tickOperations: state.tickOperations,
    living: state.living,
  }));
}

export function withDigest(state: Omit<SimulationState, "digest">): SimulationState {
  return { ...state, digest: digestState(state) };
}
