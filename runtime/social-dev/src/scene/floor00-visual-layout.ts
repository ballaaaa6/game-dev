import type { DefaultMapChipContract, Floor00VisualLayoutContract } from "../catalog/types";
import type { Cell } from "../core/types";
import {
  resolveExtensionWallPiecesForTriggerCells,
  type ExtensionWallPiece,
} from "./extension-wall";

export interface Floor00VisualLayoutProjection {
  readonly status: "approved_floor00_visual_layout";
  readonly contractId: string;
  readonly extensionWalls: readonly ExtensionWallPiece[];
  readonly wallCellsByFrame: Readonly<Record<string, readonly Cell[]>>;
  readonly removedGlassCells: readonly Cell[];
  readonly finalGlassCellsByGroup: Readonly<Record<string, readonly Cell[]>>;
  readonly backwardOffset: Cell;
}

function cellKey(cell: Cell): string {
  return `${cell[0]},${cell[1]}`;
}

function sortedCellKeys(cells: readonly Cell[]): string[] {
  return cells.map(cellKey).sort();
}

function requireSameCells(
  actual: readonly Cell[],
  expected: readonly Cell[],
  label: string,
): void {
  if (JSON.stringify(sortedCellKeys(actual)) !== JSON.stringify(sortedCellKeys(expected))) {
    throw new Error(`${label} does not match the floor00 visual layout contract`);
  }
}

export function resolveFloor00VisualLayout(
  layout: Floor00VisualLayoutContract,
  defaultMap: DefaultMapChipContract,
  nativeWallCellsByFrame: Readonly<Record<string, readonly Cell[]>>,
): Floor00VisualLayoutProjection {
  if (layout.scene_ref.id !== "room:0" || layout.scene_ref.scene_mode !== "floor00") {
    throw new Error("Floor00 visual layout is not scoped to room:0 floor00");
  }

  const extensionWalls = resolveExtensionWallPiecesForTriggerCells(
    defaultMap.extension_wall,
    layout.glass.source_asset_id,
    layout.glass.final_trigger_cells_by_group,
  );
  const actualCellsByGroup: Record<string, Cell[]> = {};
  for (const piece of extensionWalls) {
    const cells = actualCellsByGroup[piece.compositionGroup] ?? [];
    if (!cells.some((cell) => cellKey(cell) === cellKey(piece.triggerCell))) {
      cells.push([piece.triggerCell[0], piece.triggerCell[1]]);
    }
    actualCellsByGroup[piece.compositionGroup] = cells;
  }
  for (const [groupId, expectedCells] of Object.entries(layout.glass.final_trigger_cells_by_group)) {
    requireSameCells(actualCellsByGroup[groupId] ?? [], expectedCells, `Glass group ${groupId}`);
  }
  const removedKeys = new Set(layout.glass.removed_trigger_cells.map(cellKey));
  if (extensionWalls.some((piece) => removedKeys.has(cellKey(piece.triggerCell)))) {
    throw new Error("Floor00 visual layout resolved a removed glass cell");
  }

  for (const [frameId, nativeCells] of Object.entries(nativeWallCellsByFrame)) {
    requireSameCells(
      layout.wood_wall.native_cells_by_frame[frameId] ?? [],
      nativeCells,
      `Native wall frame ${frameId}`,
    );
  }

  return {
    status: "approved_floor00_visual_layout",
    contractId: layout.catalog_id,
    extensionWalls,
    wallCellsByFrame: Object.fromEntries(
      Object.entries(layout.wood_wall.final_cells_by_frame).map(([frameId, cells]) => [
        frameId,
        cells.map((cell) => [cell[0], cell[1]] as Cell),
      ]),
    ),
    removedGlassCells: layout.glass.removed_trigger_cells.map((cell) => [cell[0], cell[1]] as Cell),
    finalGlassCellsByGroup: Object.fromEntries(
      Object.entries(layout.glass.final_trigger_cells_by_group).map(([groupId, cells]) => [
        groupId,
        cells.map((cell) => [cell[0], cell[1]] as Cell),
      ]),
    ),
    backwardOffset: [layout.wood_wall.backward_offset[0], layout.wood_wall.backward_offset[1]],
  };
}
