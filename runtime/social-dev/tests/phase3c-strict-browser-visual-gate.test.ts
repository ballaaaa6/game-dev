import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import visualGateJson from "../../../knowledge/fixtures/accepted/phase3c_visual_fidelity_gate.json";

describe("Phase 3C superseded image-level browser gate evidence", () => {
  it("records why the previous default-entry claim is no longer accepted", () => {
    const gate = visualGateJson as any;
    expect(gate.status).toBe("superseded");
    expect(gate.semantic_status).toBe("superseded_image_level_gate_wrong_room_topology");
    expect(gate.superseded_reason).toMatch(/10x10 ObjChip grid/);
    expect(gate.source_reconciliation.verified_sequence).toHaveLength(4);
    expect(gate.source_reconciliation.correction).toMatch(/TryPlace/);
    expect(gate.default_entry_fixture).toMatchObject({
      frame: 0,
      digest: "ceb7009453ac8858",
      actors: 3,
    });
    expect(gate.frame136_fixture).toMatchObject({
      frame: 136,
      digest: "1fe49b91bd27c5fa",
      actors: 3,
    });
    expect(gate.native_initial_bindings).toEqual({
      "furniture:3": [[2, 4], [3, 4], [6, 4]],
      "furniture:12": [[8, 5]],
      "furniture:26": [[8, 6]],
      "furniture:56": [[2, 7]],
    });
    expect(gate.selector_only_bindings).toEqual(["furniture:2", "furniture:5"]);
    expect(gate.visual_observation).toMatchObject({
      floor_runtime_asset_visible: true,
      floor_source_status: "explicit_runtime_fallback_5_to_85_floor_09",
      debug_raw_map_overlay: false,
      native_initial_furniture_visible: true,
      wall_cells_visible: true,
      door_cell_visible: [8, 4],
      foreground_occlusion: "native_wall_and_door_draw_after_actor_at_verified_depth",
      contracts_approved: true,
      display_assets_ready: true,
      console_errors: 0,
      console_warnings: 0,
      historical_baseline_preserved: true,
      replacement_persisted: false,
    });
  });

  it("keeps both default-entry screenshots content-addressed", () => {
    const gate = visualGateJson as any;
    const workspaceRoot = resolve(process.cwd(), "../..");
    for (const fixture of [gate.default_entry_fixture, gate.frame136_fixture]) {
      const screenshotPath = resolve(workspaceRoot, fixture.screenshot.path);
      expect(existsSync(screenshotPath)).toBe(true);
      expect(createHash("sha256").update(readFileSync(screenshotPath)).digest("hex")).toBe(fixture.screenshot.sha256);
    }
  });
});
