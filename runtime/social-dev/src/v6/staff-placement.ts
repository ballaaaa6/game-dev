import type { V4CameraBoundary, V4Cell, V4Point } from "../v4";
import type { StaffPlacementV6 } from "./contracts";

export interface StaffSpawnFixtureLike {
  readonly id: string;
  readonly source_staff_id: number;
  readonly scene_ref: string;
  readonly spawn_cell: { readonly x: number; readonly y: number };
  readonly initial_position: { readonly x: number; readonly y: number };
}

export function createStaffPlacement(
  actor: StaffSpawnFixtureLike,
  camera: V4CameraBoundary,
): StaffPlacementV6 {
  const cell: V4Cell = [actor.spawn_cell.x, actor.spawn_cell.y];
  const world: V4Point = {
    x: actor.initial_position.x,
    y: actor.initial_position.y,
  };
  return {
    sceneId: actor.scene_ref,
    actorId: actor.id,
    sourceStaffId: actor.source_staff_id,
    cell,
    world,
    screen: camera.transform(world),
    cameraOffset: camera.offset,
    coordinateFormula: {
      x: "(door_x + door_y) * 20 + 40",
      y: "(door_y - door_x) * 10 + 9",
    },
    proof: "SOURCE-DATA-PROVEN",
  };
}
