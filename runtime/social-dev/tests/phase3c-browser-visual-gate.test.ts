import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import gateJson from "../../../knowledge/fixtures/accepted/phase3c_browser_visual_gate.json";

describe("Phase 3C browser visual gate evidence", () => {
  it("keeps the deterministic browser gate aligned with the runtime trace", () => {
    const gate = gateJson as {
      status: string;
      semantic_status: string;
      browser_fixture: {
        url: string;
        auto_driver: boolean;
        canvas: { width: number; height: number };
        frame6: { frame: number; digest: string; screenshot_path: string; screenshot_sha256: string };
        frame136: { frame: number; digest: string; actors: number; asset_status: string; screenshot_path: string; screenshot_sha256: string };
      };
      observed_events: readonly { type: string; frame?: number }[];
      expected: { final_frame: number; final_digest: string; talk_marker_frames: readonly number[]; talk_end_frame: number };
      gate: { console_errors: number; console_warnings: number; historical_baseline_preserved: boolean; baseline_replacement: string };
      render_boundary: { rendered_objects: readonly string[]; not_placed_objects: readonly string[]; blocked_scene_assets: readonly string[] };
    };

    expect(gate.status).toBe("pass");
    expect(gate.semantic_status).toBe("deterministic_browser_visual_gate");
    expect(gate.browser_fixture.url).toBe("http://127.0.0.1:4173/?initialTicks=136&auto=0");
    expect(gate.browser_fixture.auto_driver).toBe(false);
    expect(gate.browser_fixture.canvas).toEqual({ width: 980, height: 600 });
    expect(gate.browser_fixture.frame6).toMatchObject({ frame: 6, digest: "47bf1dfa3d2fbc59" });
    expect(gate.browser_fixture.frame136).toMatchObject({ frame: 136, digest: "1fe49b91bd27c5fa", actors: 3, asset_status: "display assets ready" });
    expect(gate.observed_events.map((event) => event.type)).toEqual([
      "idle",
      "move",
      "arrive",
      "work_or_equipment",
      "talk",
      "talk_marker",
      "talk_marker",
      "talk_marker",
      "talk_end",
    ]);
    expect(gate.observed_events.filter((event) => event.type === "talk_marker").map((event) => event.frame)).toEqual([20, 70, 110]);
    expect(gate.expected).toEqual({
      final_frame: 136,
      final_digest: "1fe49b91bd27c5fa",
      talk_marker_frames: [20, 70, 110],
      talk_end_frame: 130,
      required_event_types: ["idle", "move", "arrive", "work_or_equipment", "talk", "talk_marker", "talk_end"],
    });
    expect(gate.gate).toMatchObject({
      console_errors: 0,
      console_warnings: 0,
      historical_baseline_preserved: true,
      baseline_replacement: "not_persisted",
    });
    expect(gate.render_boundary).toEqual({
      rendered_objects: ["furniture:0", "furniture:1"],
      not_placed_objects: ["furniture:2", "furniture:5"],
      blocked_scene_assets: ["wall", "door"],
      floor_resolution: "raw selector 5 -> selector/data 85/floor_09.png -> render floor_05.png",
    });
  });

  it("keeps both candidate screenshots present and content-addressed", () => {
    const gate = gateJson as {
      browser_fixture: {
        frame6: { screenshot_path: string; screenshot_sha256: string };
        frame136: { screenshot_path: string; screenshot_sha256: string };
      };
    };
    const workspaceRoot = resolve(process.cwd(), "../..");
    for (const screenshot of [gate.browser_fixture.frame6, gate.browser_fixture.frame136]) {
      const screenshotPath = resolve(workspaceRoot, screenshot.screenshot_path);
      expect(existsSync(screenshotPath)).toBe(true);
      const digest = createHash("sha256").update(readFileSync(screenshotPath)).digest("hex");
      expect(digest).toBe(screenshot.screenshot_sha256);
    }
  });
});
