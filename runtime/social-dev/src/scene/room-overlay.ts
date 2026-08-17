import type { RoomRSceneContract, RoomSceneRuntimeRecord } from "../catalog/types";
import type { Cell } from "../core/types";

export interface RoomRawOverlayCell {
  readonly id: string;
  readonly cell: Cell;
  readonly rawType: number;
  readonly rawTypeLabel: string;
  readonly rawDirection: number;
  readonly directionStatus: string;
  readonly identityStatus: string;
  readonly instanceId: null;
  readonly renderStatus: string;
}

export interface RoomRawOverlay {
  readonly roomId: "room:17";
  readonly gridWidth: 10;
  readonly gridHeight: 10;
  readonly cells: readonly RoomRawOverlayCell[];
  readonly doorCells: readonly Cell[];
  readonly status: "pass";
  readonly diagnosticOnly: true;
  readonly unresolved: readonly string[];
}

function cellKey(x: number, y: number): string {
  return `${x}:${y}`;
}

/**
 * Build the Room R diagnostic overlay from the independently generated fixture.
 * The runtime catalog is cross-checked before the overlay is accepted so the
 * debug view cannot silently drift away from the resolver's raw cells.
 */
export function buildRoomRawOverlay(
  fixture: RoomRSceneContract,
  runtimeRoom: RoomSceneRuntimeRecord,
): RoomRawOverlay {
  if (fixture.room_id !== "room:17" || runtimeRoom.room_key !== "room:17") {
    throw new Error("Room R overlay requires room:17 fixture and runtime record");
  }
  if (fixture.raw_cells.length !== runtimeRoom.raw_cells.length || fixture.raw_cells.length !== 100) {
    throw new Error("Room R overlay raw cell count drifted");
  }
  const runtimeByCell = new Map(runtimeRoom.raw_cells.map((cell) => [cellKey(cell.x, cell.y), cell]));
  const cells: RoomRawOverlayCell[] = fixture.raw_cells.map((fixtureCell) => {
    const runtimeCell = runtimeByCell.get(cellKey(fixtureCell.x, fixtureCell.y));
    if (!runtimeCell) {
      throw new Error(`Room R overlay is missing runtime cell ${fixtureCell.cell_id}`);
    }
    if (runtimeCell.raw_type !== fixtureCell.raw_type || runtimeCell.raw_direction !== fixtureCell.raw_direction) {
      throw new Error(`Room R overlay drift at ${fixtureCell.cell_id}`);
    }
    return {
      id: fixtureCell.cell_id,
      cell: [fixtureCell.x, fixtureCell.y],
      rawType: fixtureCell.raw_type,
      rawTypeLabel: fixtureCell.raw_type_label,
      rawDirection: fixtureCell.raw_direction,
      directionStatus: fixtureCell.direction_status,
      identityStatus: fixtureCell.identity_status,
      instanceId: null,
      renderStatus: fixtureCell.render_status,
    };
  });
  return {
    roomId: "room:17",
    gridWidth: 10,
    gridHeight: 10,
    cells,
    doorCells: fixture.door_cells.map((cell) => [cell.x, cell.y]),
    status: "pass",
    diagnosticOnly: true,
    unresolved: fixture.unresolved,
  };
}
