import type { CameraCoordinateContract } from "../catalog/types";
import type { Cell } from "../core/types";
import { actorToCanvas, cellToActorWorld, mapChipToCanvas, type CanvasPoint } from "./coordinates";
import type { SceneCellProjection, SceneMapCellProjection, SceneProjection } from "./projection";

export interface ActorFloorContainmentResult {
  readonly status: "pass" | "blocked";
  readonly cell: Cell;
  readonly foot: CanvasPoint;
  readonly containingCells: readonly Cell[];
  readonly reason: string;
}

const FLOOR_TILE_WIDTH = 80;
const FLOOR_TILE_HEIGHT = 39;
const FLOOR_TILE_CENTER_Y = FLOOR_TILE_HEIGHT / 2;
const CONTAINMENT_EPSILON = 0.06;

function sameCell(left: Cell, right: Cell): boolean {
  return left[0] === right[0] && left[1] === right[1];
}

function placementForCell(cells: readonly SceneCellProjection[], cell: Cell): SceneCellProjection | undefined {
  return cells.find((candidate) => sameCell(candidate.cell, cell));
}

function pointInsideFloorTile(point: CanvasPoint, origin: CanvasPoint): boolean {
  const normalized = Math.abs(point.x - (origin.x + FLOOR_TILE_WIDTH / 2)) / (FLOOR_TILE_WIDTH / 2)
    + Math.abs(point.y - (origin.y + FLOOR_TILE_CENTER_Y)) / FLOOR_TILE_CENTER_Y;
  return normalized <= 1 + CONTAINMENT_EPSILON;
}

function floorCells(projection: Pick<SceneProjection, "mapCells">): readonly SceneMapCellProjection[] {
  return projection.mapCells.filter((cell) => cell.nativeFloorPass && cell.rawIndex === 1 && Boolean(cell.assetId));
}

/**
 * Verifies both native ObjChip occupancy and screen-space containment in a
 * visible floor MapChip diamond. The two tests are intentionally separate:
 * an empty ObjChip cell can still project outside the rendered floor if the
 * camera/grid transform is wrong.
 */
export function evaluateActorFloorContainment(
  cell: Cell,
  projection: Pick<SceneProjection, "cells" | "mapCells">,
  camera: CameraCoordinateContract,
  options: {
    readonly allowEntryDoor?: boolean;
    readonly allowInstalledFurniture?: boolean;
  } = {},
): ActorFloorContainmentResult {
  const foot = actorToCanvas(cellToActorWorld(cell, camera), camera);
  const placement = placementForCell(projection.cells, cell);
  if (!placement) {
    return {
      status: "blocked",
      cell,
      foot,
      containingCells: [],
      reason: "actor_cell_missing_from_objchip_projection",
    };
  }
  const occupiedByInstalledFurniture = options.allowInstalledFurniture === true
    && placement.collisionKind === "installed_furniture";
  const occupiedByEntryDoor = options.allowEntryDoor === true
    && placement.collisionKind === "entry_door";
  if ((!placement.passable || placement.collisionKind !== "empty_walkable") && !occupiedByInstalledFurniture && !occupiedByEntryDoor) {
    return {
      status: "blocked",
      cell,
      foot,
      containingCells: [],
      reason: `actor_cell_not_empty_walkable:${placement.collisionKind}`,
    };
  }
  if (occupiedByEntryDoor) {
    return {
      status: "pass",
      cell,
      foot,
      containingCells: [],
      reason: "actor_at_native_entry_door",
    };
  }
  const containingCells = floorCells(projection)
    .filter((floor) => pointInsideFloorTile(foot, mapChipToCanvas(floor.cell, camera)))
    .map((floor) => floor.cell);
  return {
    status: containingCells.length > 0 ? "pass" : "blocked",
    cell,
    foot,
    containingCells,
    reason: containingCells.length > 0
      ? "actor_foot_inside_native_floor_mapchip"
      : "actor_foot_outside_visible_native_floor_mapchips",
  };
}
