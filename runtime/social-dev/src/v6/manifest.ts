import { V4NativePassOrder } from "../v4/ordering";
import type { RoomV5 } from "../v5/room";
import type { V6IntegratedRenderResult, V6RoomStaffManifest } from "./contracts";

export function createV6RoomStaffManifest(
  room: RoomV5,
  render: V6IntegratedRenderResult,
): V6RoomStaffManifest {
  return {
    schemaVersion: 1,
    phase: "V6",
    roomKey: room.roomData.roomKey,
    dataKey: room.roomData.dataKey,
    cameraOffset: render.camera.offset,
    passOrder: [...V4NativePassOrder],
    passes: render.passes,
    events: render.events,
    traces: render.traces,
    commands: render.commands,
    staff: render.staff,
    integration: render.integration,
    baseline: {
      phase: "V5",
      commandCount: render.base.commands.length,
      traceCount: render.base.traces.length,
      eventCount: render.base.events.length,
      passCount: render.base.passes.length,
    },
    policy: {
      productionCutover: false,
      gameplay: false,
      serverProof: false,
      exactPixels: "DEFERRED_TO_V7",
    },
  };
}
