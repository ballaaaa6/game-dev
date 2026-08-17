import type { GraphicsCommand } from "../v2/graphics";
import type { V4CommandTrace } from "../v4/contracts";
import type { V5CommandEvent, V5PassResult, V5RoomRenderResult } from "../v5/contracts";
import type { V6IntegratedPassResult, V6IntegratedRenderResult } from "../v6/contracts";

export type ReintegrationSource = V5RoomRenderResult | V6IntegratedRenderResult;

export interface ReintegrationTraceRange {
  readonly trace: V4CommandTrace;
  readonly commandStart: number;
  readonly commandEnd: number;
}

export interface ReintegrationSelection {
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly V4CommandTrace[];
  readonly selectedCommandIndices: readonly number[];
  readonly sourceCommandCount: number;
  readonly sourceTraceCount: number;
}

export interface ReintegrationSelectionPredicate {
  readonly trace?: (trace: V4CommandTrace) => boolean;
  readonly event?: (event: V5CommandEvent) => boolean;
}

/**
 * Selects a visual layer from an already-recovered RoomV5/V6 command stream.
 * The source stream remains authoritative for ordering and every selected
 * command retains its original Graphics state snapshot.
 */
export function selectReintegrationLayer(
  source: ReintegrationSource,
  predicate: ReintegrationSelectionPredicate,
): ReintegrationSelection {
  const selected = new Set<number>();
  const ranges = traceRanges(source.commands, source.traces, source.passes);

  for (const range of ranges) {
    if (predicate.trace?.(range.trace) !== true) continue;
    addRange(selected, range.commandStart, range.commandEnd);
  }
  for (const event of source.events) {
    if (predicate.event?.(event) !== true) continue;
    addRange(selected, event.commandStart, event.commandEnd);
  }

  const selectedCommandIndices = [...selected].sort((left, right) => left - right);
  const selectedIndexSet = new Set(selectedCommandIndices);
  return {
    commands: selectedCommandIndices.map((index) => source.commands[index]!).filter(Boolean),
    traces: ranges
      .filter((range) => hasSelectedCommand(selectedIndexSet, range.commandStart, range.commandEnd))
      .map((range) => range.trace),
    selectedCommandIndices,
    sourceCommandCount: source.commands.length,
    sourceTraceCount: source.traces.length,
  };
}

export function traceRanges(
  commands: readonly GraphicsCommand[],
  traces: readonly V4CommandTrace[],
  passes: readonly (V5PassResult | V6IntegratedPassResult)[],
): readonly ReintegrationTraceRange[] {
  const ranges: ReintegrationTraceRange[] = [];
  for (const pass of passes) {
    let commandCursor = pass.commandStart;
    for (const trace of traces.slice(pass.traceStart, pass.traceEnd)) {
      const commandEnd = commandCursor + trace.commandCount;
      if (commandCursor < 0 || commandEnd > commands.length) {
        throw new Error(`Reintegration trace range is outside the command stream for ${trace.selectorRole}`);
      }
      ranges.push({ trace, commandStart: commandCursor, commandEnd });
      commandCursor = commandEnd;
    }
    if (commandCursor !== pass.commandEnd) {
      throw new Error(`Reintegration trace accounting drift in pass ${pass.passId}: ${commandCursor} !== ${pass.commandEnd}`);
    }
  }
  return ranges;
}

function addRange(selected: Set<number>, commandStart: number, commandEnd: number): void {
  for (let index = commandStart; index < commandEnd; index += 1) selected.add(index);
}

function hasSelectedCommand(selected: ReadonlySet<number>, commandStart: number, commandEnd: number): boolean {
  for (let index = commandStart; index < commandEnd; index += 1) {
    if (selected.has(index)) return true;
  }
  return false;
}
