import { GraphicsCompatibility } from "../v2/graphics";
import type { GraphicsCommand } from "../v2/graphics";
import type { V4CommandTrace } from "../v4";
import type { V5CommandEvent, V5PassResult } from "../v5/contracts";
import type { RoomV5 } from "../v5/room";
import type { StaffDrawResult, V6IntegratedPassResult, V6IntegratedRenderResult } from "./contracts";
import { StaffV6 } from "./staff";

export function integrateStaffIntoRoomV6(
  room: RoomV5,
  staff: readonly StaffV6[],
): V6IntegratedRenderResult {
  const base = room.draw();
  const avatarPassIndex = base.passes.findIndex((pass) => pass.passId === "avatar-primary");
  if (avatarPassIndex < 0) {
    throw new Error("V6 native avatar-primary pass is missing from the V5 room schedule");
  }

  const staffGraphics = new GraphicsCompatibility();
  const staffDraws: StaffDrawResult[] = [];
  for (const actor of staff) {
    staffDraws.push(actor.draw(staffGraphics, room.camera));
  }

  const commands: GraphicsCommand[] = [];
  const traces: V4CommandTrace[] = [];
  const events: V5CommandEvent[] = [];
  const passes: V6IntegratedPassResult[] = [];

  for (const [index, basePass] of base.passes.entries()) {
    const passCommandStart = commands.length;
    const passTraceStart = traces.length;
    const commandShift = passCommandStart - basePass.commandStart;
    const traceShift = passTraceStart - basePass.traceStart;
    commands.push(...base.commands.slice(basePass.commandStart, basePass.commandEnd));
    traces.push(...base.traces.slice(basePass.traceStart, basePass.traceEnd));
    for (const event of base.events.filter((candidate) => candidate.passId === basePass.passId)) {
      events.push(shiftEvent(event, commandShift, traceShift));
    }

    let inputCount = basePass.inputCount;
    if (index === avatarPassIndex) {
      inputCount += staff.length;
      appendStaffDraws(staffDraws, commands, traces, events, basePass.passId);
    }
    passes.push({
      ...basePass,
      inputCount,
      commandStart: passCommandStart,
      commandEnd: commands.length,
      traceStart: passTraceStart,
      traceEnd: traces.length,
    });
  }

  return {
    base,
    commands,
    traces,
    events,
    passes,
    camera: room.camera,
    resources: room.resources,
    staff: staff.map((actor) => actor.snapshot(room.camera)),
    staffDraws,
    integration: {
      passId: "avatar-primary",
      index: avatarPassIndex,
      nativeRelation: "SOURCE-LIMITED",
      ordering: "object-chip-wall < avatar-primary StaffV6 < avatar-secondary < object-chip-late-preview < object-chip-late",
      occlusion: "foreground object-chip-late and map-floor remain after StaffV6 commands",
    },
  };
}

function appendStaffDraws(
  staffDraws: readonly StaffDrawResult[],
  commands: GraphicsCommand[],
  traces: V4CommandTrace[],
  events: V5CommandEvent[],
  passId: string,
): void {
  for (const draw of staffDraws) {
    const commandStart = commands.length;
    const traceStart = traces.length;
    commands.push(...draw.commands);
    traces.push(...draw.traces);
    events.push({
      passId,
      cell: draw.placement.cell,
      role: "static StaffV6 actor",
      commandStart,
      commandEnd: commands.length,
      traceStart,
      traceEnd: traces.length,
      proof: "CALL-FLOW-PROVEN",
    });
  }
}

function shiftEvent(event: V5CommandEvent, commandShift: number, traceShift: number): V5CommandEvent {
  return {
    ...event,
    commandStart: event.commandStart + commandShift,
    commandEnd: event.commandEnd + commandShift,
    traceStart: event.traceStart + traceShift,
    traceEnd: event.traceEnd + traceShift,
  };
}
