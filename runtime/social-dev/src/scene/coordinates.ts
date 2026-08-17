import type { CameraCoordinateContract } from "../catalog/types";
import type { Cell, WorldPosition } from "../core/types";

export interface CanvasPoint {
  readonly x: number;
  readonly y: number;
}

// The browser fixture is a 980x600 canvas. Room.Draw derives its horizontal
// draw offsets from the game width and room width; keep those native offsets
// explicit so MapChip (40/20 lattice) and ObjChip/Staff (20/10 lattice) share
// the same room instead of being composited as one grid.
const ROOM_WIDTH = 14;
const CANVAS_WIDTH = 980;
const FLOOR_WIDTH_OFFSET = (CANVAS_WIDTH >> 1) - ((ROOM_WIDTH * 2) << 4) + 40;
// Room.Draw forwards the floor-width offset directly to MapChip, then derives
// the object-grid offset from half of (room.width * 80 - 320).  The two grids
// are intentionally different resolutions, but these offsets put their
// native room boundary on the same screen-space edge.
const NATIVE_MAP_DRAW_OFFSET_X = FLOOR_WIDTH_OFFSET;
const NATIVE_OBJECT_DRAW_OFFSET_X = FLOOR_WIDTH_OFFSET + (((ROOM_WIDTH * 5) << 4) - 320) / 2 - 40;
const VIEWPORT_ORIGIN = { x: 0, y: 260 } as const;

export function cellToWorld(cell: Cell): CanvasPoint {
  const [x, y] = cell;
  return {
    x: (x + y) * 20 + 20,
    y: (y - x) * 10 + 18,
  };
}

export function mapChipWorldOrigin(cell: Cell): CanvasPoint {
  const [x, y] = cell;
  return {
    x: (x + y) * 40,
    y: (y - x) * 20,
  };
}

export function objectWorldOrigin(cell: Cell): CanvasPoint {
  const [x, y] = cell;
  return {
    x: (x + y) * 20,
    y: (y - x) * 10 + 9,
  };
}

export function cellToActorWorld(cell: Cell, contract: CameraCoordinateContract): WorldPosition {
  const [x, y] = cell;
  const expected = contract.coordinate_system.actor_spawn_position;
  if (typeof expected.formula !== "string" || !expected.formula.includes("(x + y) * 20 + 40")) {
    throw new Error("Actor coordinate formula is not the verified runtime formula");
  }
  return {
    x: (x + y) * 20 + 40,
    y: (y - x) * 10 + 9,
  };
}

export function worldToCanvas(point: CanvasPoint, contract: CameraCoordinateContract): CanvasPoint {
  const [offsetX, offsetY] = contract.camera.fixture_offset;
  return {
    x: point.x + VIEWPORT_ORIGIN.x + offsetX,
    y: point.y + VIEWPORT_ORIGIN.y + offsetY,
  };
}

export function cellToCanvas(cell: Cell, contract: CameraCoordinateContract): CanvasPoint {
  const world = cellToWorld(cell);
  return worldToCanvas(
    {
      x: world.x + NATIVE_OBJECT_DRAW_OFFSET_X + 20,
      y: world.y - 9,
    },
    contract,
  );
}

export function mapChipToCanvas(cell: Cell, contract: CameraCoordinateContract): CanvasPoint {
  const origin = mapChipWorldOrigin(cell);
  return worldToCanvas({ x: origin.x + NATIVE_MAP_DRAW_OFFSET_X, y: origin.y }, contract);
}

// The native furniture:0 big_base00 composition is a 120x61 sprite for a
// verified 3x3 structural footprint. The raw type-4 centers are recorded in
// the separate 10x10 ObjChip grid, while the visual pad is a 3x3 MapChip-sized
// composition. The closed floor00 raster alignment maps the object anchor to
// the room's MapChip floor band by preserving x and applying the verified
// room-band y offset.
const FLOOR00_STRUCTURAL_MAP_Y_OFFSET = 3;

export function structuralFacilityMapCell(cell: Cell): Cell {
  return [cell[0], cell[1] + FLOOR00_STRUCTURAL_MAP_Y_OFFSET] as const;
}

export function structuralFacilityToCanvas(mapAnchor: Cell, contract: CameraCoordinateContract): CanvasPoint {
  return mapChipToCanvas(mapAnchor, contract);
}

export function objectToCanvas(cell: Cell, contract: CameraCoordinateContract): CanvasPoint {
  const origin = objectWorldOrigin(cell);
  return worldToCanvas({ x: origin.x + NATIVE_OBJECT_DRAW_OFFSET_X, y: origin.y }, contract);
}

export function actorToCanvas(position: WorldPosition, contract: CameraCoordinateContract): CanvasPoint {
  return worldToCanvas({ x: position.x + NATIVE_OBJECT_DRAW_OFFSET_X, y: position.y }, contract);
}

export function viewportOrigin(): CanvasPoint {
  return VIEWPORT_ORIGIN;
}
