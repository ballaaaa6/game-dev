import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { withDigest } from "../src/core/digest";
import { createInitialState } from "../src/core/simulation";
import { buildSceneProjection } from "../src/scene/projection";
import { buildVisualGateSnapshot } from "../src/renderer/visual-gate";

describe("deterministic visual gate snapshot", () => {
  it("records the explicit pass order, metadata cards, and pending asset state", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:0");
    const snapshot = buildVisualGateSnapshot(projection, createInitialState(catalogs), catalogs, null);
    expect(snapshot.gate_status).toBe("pending_assets");
    expect(snapshot.render_passes).toEqual([
      "map-extension-floor",
      "map-chip",
      "object-chip-primary",
      "object-chip-wall",
      "avatar-primary",
      "avatar-secondary",
      "object-chip-late-preview",
      "object-chip-late",
      "map-floor",
    ]);
    expect(snapshot.checks.render_pass_order.status).toBe("pass");
    expect(snapshot.checks.drawable_metadata.status).toBe("pass");
    expect(snapshot.metadata_missing).toHaveLength(0);
    expect(snapshot.checks.native_placement.status).toBe("pass");
    expect(snapshot.checks.native_composition.status).toBe("pass");
    expect(snapshot.checks.floor00_bootstrap.details).not.toContain("legacy render objects");
  });

  it("marks Room R raw overlay as diagnostic evidence while keeping native composition approved", () => {
    const catalogs = loadRuntimeCatalogs();
    const projection = buildSceneProjection(catalogs, "room:17");
    const base = createInitialState(catalogs);
    const { digest: _digest, ...withoutDigest } = base;
    const state = withDigest({
      ...withoutDigest,
      sceneId: "room:17",
      actors: {},
      events: [],
      eventLog: [],
      selectedActorId: null,
    });
    const snapshot = buildVisualGateSnapshot(
      projection,
      state,
      catalogs,
      null,
      true,
    );
    expect(snapshot.gate_status).toBe("pending_assets");
    expect(snapshot.raw_overlay_enabled).toBe(true);
    expect(snapshot.checks.raw_room_overlay).toMatchObject({ status: "pass" });
    expect(snapshot.checks.native_composition).toMatchObject({ status: "pass" });
    expect(snapshot.checks.native_placement).toMatchObject({ status: "pass" });
    expect(snapshot.drawable_cards.filter((card) => card.kind === "raw_overlay_cell")).toHaveLength(100);
    expect(snapshot.unresolved).toEqual([]);
  });
});
