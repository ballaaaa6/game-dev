import type { LivingCell } from "../core/living/types";

export interface V8WorkstationDrawCommand {
  readonly kind: "furniture" | "staff" | "chair";
  readonly id: string;
  readonly cell: LivingCell;
  readonly selectorId?: number;
  readonly frame?: number;
  readonly layer: "primary" | "staff" | "foreground";
}

export interface V8WorkstationComposition {
  readonly deskId: number;
  readonly deskCell: LivingCell;
  readonly chairCell: LivingCell;
  readonly rawDirection: number;
  readonly commands: readonly V8WorkstationDrawCommand[];
}

/**
 * Native ObjChip.Draw(FurnitureData, preview:false) interleave for both
 * accepted directional workstation paths. The generic Staff loop must not
 * add a second copy of an installed staff.
 */
export function compileWorkstationComposition(
  deskId: number,
  deskCell: LivingCell,
  staffId: number,
  staffCell: LivingCell,
  staffSelectorId: number,
  staffFrame: number,
  rawDirection: number,
): V8WorkstationComposition {
  // FurnitureData(3)'s chair is the installed sub-SEB at the desk origin;
  // raw direction 3 uses frame 0 before Staff and the desk after Staff,
  // while raw direction 2 uses the desk/frame 1/Staff/frame 2 sequence.
  const chairCell: LivingCell = [deskCell[0], deskCell[1]];
  const commands: V8WorkstationDrawCommand[] = rawDirection === 3
    ? [
        { kind: "chair", id: `chair:${deskId}:sub`, cell: chairCell, selectorId: 1, frame: 0, layer: "primary" },
        { kind: "staff", id: `actor:staff:${staffId}`, cell: staffCell, selectorId: staffSelectorId, frame: staffFrame, layer: "staff" },
        { kind: "furniture", id: `furniture:${deskId}`, cell: deskCell, layer: "foreground" },
      ]
    : [
        { kind: "furniture", id: `furniture:${deskId}`, cell: deskCell, layer: "primary" },
        { kind: "chair", id: `chair:${deskId}:sub`, cell: chairCell, selectorId: 1, frame: 1, layer: "primary" },
        { kind: "staff", id: `actor:staff:${staffId}`, cell: staffCell, selectorId: staffSelectorId, frame: staffFrame, layer: "staff" },
        { kind: "chair", id: `chair:${deskId}:front`, cell: chairCell, selectorId: 1, frame: 2, layer: "foreground" },
      ];
  return { deskId, deskCell: [deskCell[0], deskCell[1]], chairCell, rawDirection, commands };
}

export function dedupeInstalledStaff(
  staffIds: readonly number[],
  nestedStaffIds: readonly number[],
): readonly number[] {
  const nested = new Set(nestedStaffIds);
  return staffIds.filter((staffId) => !nested.has(staffId));
}
