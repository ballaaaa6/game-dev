import type { Cell } from "../core/types";

export interface NativeCellDrawable {
  readonly cell: Cell;
  readonly key?: string;
  readonly layer?: number;
}

/** Native Room.Draw scans increasing rows and descending columns. */
export function compareNativeCells(
  left: Pick<NativeCellDrawable, "cell">,
  right: Pick<NativeCellDrawable, "cell">,
): number {
  return left.cell[1] - right.cell[1] || right.cell[0] - left.cell[0];
}

export function sortNativeDrawables<T extends NativeCellDrawable>(drawables: readonly T[]): T[] {
  return [...drawables].sort((left, right) =>
    compareNativeCells(left, right)
      || (left.layer ?? 0) - (right.layer ?? 0)
      || (left.key ?? "").localeCompare(right.key ?? ""),
  );
}

export type NativeWallLayer = "rear" | "foreground";

/** The floor00 contract supplies the late wall occluder cells. */
export function classifyNativeWallLayer(
  cell: Cell,
  foregroundCells: readonly Cell[] = [[8, 7], [8, 8]],
): NativeWallLayer {
  return foregroundCells.some((candidate) => candidate[0] === cell[0] && candidate[1] === cell[1])
    ? "foreground"
    : "rear";
}
