import type { V4Cell } from "./contracts";

export const V4NativePassOrder = [
  "map-extension-floor",
  "map-chip",
  "object-chip-primary",
  "object-chip-wall",
  "avatar-primary",
  "avatar-secondary",
  "object-chip-late-preview",
  "object-chip-late",
  "map-floor",
] as const;

export type V4NativePassId = typeof V4NativePassOrder[number];

export interface V4SortableDrawable {
  readonly cell: V4Cell;
  readonly layer?: number;
  readonly key?: string;
}

export function compareV4Cells(left: Pick<V4SortableDrawable, "cell">, right: Pick<V4SortableDrawable, "cell">): number {
  return left.cell[1] - right.cell[1] || right.cell[0] - left.cell[0];
}

export function sortV4Drawables<T extends V4SortableDrawable>(drawables: readonly T[]): T[] {
  return [...drawables].sort((left, right) =>
    compareV4Cells(left, right)
      || (left.layer ?? 0) - (right.layer ?? 0)
      || (left.key ?? "").localeCompare(right.key ?? ""),
  );
}
