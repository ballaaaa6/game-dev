import { describe, expect, it } from "vitest";
import traceJson from "../../../knowledge/fixtures/accepted/display_slice_01_behavior_trace.json";

describe("browser behavior-trace evidence", () => {
  it("records the required first vertical-slice milestones", () => {
    const trace = traceJson as {
      status: string;
      semantic_status: string;
      browser_fixture: { final_frame: number; auto_driver: boolean };
      observed_events: readonly { type: string; frame?: number }[];
      final_actor_states: readonly { id: string; lifecycle: string }[];
      gate: { console_errors: number; expected_talk_end_frame: number };
    };
    expect(trace.status).toBe("pass");
    expect(trace.semantic_status).toBe("deterministic_browser_trace");
    expect(trace.browser_fixture.final_frame).toBe(136);
    expect(trace.browser_fixture.auto_driver).toBe(false);
    expect(trace.observed_events.map((event) => event.type)).toEqual([
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
    expect(trace.observed_events.filter((event) => event.type === "talk_marker").map((event) => event.frame)).toEqual([20, 70, 110]);
    expect(trace.observed_events.at(-1)).toEqual({
      tick: 136,
      type: "talk_end",
      actorIds: ["actor:staff:0", "actor:staff:1"],
      frame: 130,
    });
    expect(trace.final_actor_states).toHaveLength(3);
    expect(trace.gate.console_errors).toBe(0);
    expect(trace.gate.expected_talk_end_frame).toBe(130);
  });
});
