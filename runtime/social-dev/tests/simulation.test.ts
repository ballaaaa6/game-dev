import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { digestSequence, createInitialState, runTicks, stateDigestWithoutMutation, stepSimulation } from "../src/core/simulation";

describe("deterministic living-scene core", () => {
  it("creates the source-bounded spawn fixture without inventing cells", () => {
    const catalogs = loadRuntimeCatalogs();
    const state = createInitialState(catalogs);
    expect(Object.keys(state.actors)).toEqual(["actor:staff:0", "actor:staff:1", "actor:staff:2"]);
    expect(Object.values(state.actors).map((actor) => actor.cell)).toEqual([[8, 4], [8, 4], [8, 4]]);
    expect(Object.values(state.actors).map((actor) => actor.position)).toEqual([
      { x: 280, y: -31 },
      { x: 280, y: -31 },
      { x: 280, y: -31 },
    ]);
    expect(state.frame).toBe(0);
    expect(stateDigestWithoutMutation(state)).toBe(state.digest);
  });

  it("advances the authoritative living core and projects it to actors", () => {
    const catalogs = loadRuntimeCatalogs();
    let state = createInitialState(catalogs);
    for (let index = 0; index < 20; index += 1) {
      state = stepSimulation(state, catalogs);
    }
    expect(state.living.staffs[0]?.state).toBe(4);
    expect(state.living.traces.some((trace) => trace.event === "on-arrive-goal-mode-3")).toBe(true);
    expect(state.living.traces.some((trace) => trace.event === "on-arrive-goal-mode-6")).toBe(true);
    expect(state.actors["actor:staff:0"]?.cell).toEqual(state.living.staffs[0]?.cell);
  });

  it("produces the same digest sequence for the same tick input", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(digestSequence(140, catalogs)).toEqual(digestSequence(140, catalogs));
    expect(runTicks(6, catalogs).living.traces.length).toBeGreaterThan(0);
  });
});
