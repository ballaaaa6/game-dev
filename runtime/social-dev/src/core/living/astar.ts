import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { furniturePassMap, i0Catalog } from "./catalog";
import { ObjChipType } from "./constants";
import type { LivingCell } from "./types";

export interface AstarGoal {
  readonly cell: LivingCell;
  readonly allowOccupiedTarget?: boolean;
  readonly goalType?: number;
}

export interface AstarOptions {
  readonly goal?: AstarGoal;
}

const NEIGHBORS: readonly LivingCell[] = [[-1, 0], [1, 0], [0, -1], [0, 1]];

function key(cell: LivingCell): string {
  return `${cell[0]},${cell[1]}`;
}

function manhattan(a: LivingCell, b: LivingCell): number {
  return Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
}

function sameCell(a: LivingCell, b: LivingCell): boolean {
  return a[0] === b[0] && a[1] === b[1];
}

function rawTypeAt(catalogs: RuntimeCatalogs, cell: LivingCell): number {
  const room = i0Catalog(catalogs).rooms.find((candidate) => candidate.room_key === "room:0");
  return room?.obj_map[cell[1]]?.[cell[0]] ?? ObjChipType.OUTDOOR;
}

function furnitureAt(catalogs: RuntimeCatalogs, cell: LivingCell): { readonly type: number; readonly dataId: number | null } | null {
  const room = i0Catalog(catalogs).rooms.find((candidate) => candidate.room_key === "room:0");
  const rawType = room?.obj_map[cell[1]]?.[cell[0]];
  if (rawType === undefined) return null;
  const bootstrap = i0Catalog(catalogs).bootstrap;
  const explicit = [...bootstrap.desks, ...bootstrap.equipment].find((candidate) => candidate.cell[0] === cell[0] && candidate.cell[1] === cell[1]);
  return explicit ? { type: rawType, dataId: explicit.furniture_data_id } : null;
}

export function isPassableCell(catalogs: RuntimeCatalogs, cell: LivingCell, goal?: AstarGoal): boolean {
  const room = i0Catalog(catalogs).rooms.find((candidate) => candidate.room_key === "room:0");
  if (!room || cell[0] < 0 || cell[1] < 0 || cell[0] >= room.width || cell[1] >= room.height) return false;
  const rawType = rawTypeAt(catalogs, cell);
  if (rawType === ObjChipType.OUTDOOR) return false;
  const isGoal = goal ? sameCell(goal.cell, cell) : false;
  if (rawType === ObjChipType.BIG || rawType === ObjChipType.BIG_CENTER) {
    const furniture = furnitureAt(catalogs, cell);
    if (furniture?.dataId !== null && furniture?.dataId !== undefined) {
      const passMap = furniturePassMap(catalogs, furniture.dataId);
      if (passMap.length > 0 && passMap.every((value) => value === 0)) return false;
    }
    return isGoal && goal?.allowOccupiedTarget === true;
  }
  if (rawType === ObjChipType.DESK || rawType === ObjChipType.EQUIPMENT) {
    return isGoal && goal?.allowOccupiedTarget === true;
  }
  if (rawType === ObjChipType.DOOR || rawType === ObjChipType.PASS) return true;
  return false;
}

export function searchRoute(
  catalogs: RuntimeCatalogs,
  start: LivingCell,
  goal: LivingCell,
  options: AstarOptions = {},
): readonly LivingCell[] {
  const resolvedGoal: AstarGoal = options.goal ?? { cell: goal, allowOccupiedTarget: true };
  if (!isPassableCell(catalogs, start, { cell: start, allowOccupiedTarget: true })) {
    throw new Error(`Astar start is not passable: ${key(start)}`);
  }
  if (!isPassableCell(catalogs, goal, resolvedGoal)) {
    throw new Error(`Astar goal is rejected: ${key(goal)}`);
  }
  const open: LivingCell[] = [[start[0], start[1]]];
  const cameFrom = new Map<string, LivingCell>();
  const gScore = new Map<string, number>([[key(start), 0]]);
  const fScore = new Map<string, number>([[key(start), manhattan(start, goal)]]);
  const closed = new Set<string>();
  while (open.length > 0) {
    open.sort((left, right) => {
      const fDelta = (fScore.get(key(left)) ?? Number.MAX_SAFE_INTEGER) - (fScore.get(key(right)) ?? Number.MAX_SAFE_INTEGER);
      return fDelta || key(left).localeCompare(key(right));
    });
    const current = open.shift();
    if (!current) break;
    const currentKey = key(current);
    if (sameCell(current, goal)) {
      const path: LivingCell[] = [current];
      let cursor = currentKey;
      while (cameFrom.has(cursor)) {
        const previous = cameFrom.get(cursor)!;
        path.unshift(previous);
        cursor = key(previous);
      }
      return path;
    }
    closed.add(currentKey);
    for (const delta of NEIGHBORS) {
      const next: LivingCell = [current[0] + delta[0], current[1] + delta[1]];
      const nextKey = key(next);
      if (closed.has(nextKey) || !isPassableCell(catalogs, next, resolvedGoal)) continue;
      const tentative = (gScore.get(currentKey) ?? Number.MAX_SAFE_INTEGER) + 1;
      if (tentative < (gScore.get(nextKey) ?? Number.MAX_SAFE_INTEGER)) {
        cameFrom.set(nextKey, current);
        gScore.set(nextKey, tentative);
        fScore.set(nextKey, tentative + manhattan(next, goal));
        if (!open.some((candidate) => sameCell(candidate, next))) open.push(next);
      }
    }
  }
  throw new Error(`Astar route not found: ${key(start)} -> ${key(goal)}`);
}

export { manhattan, sameCell };
