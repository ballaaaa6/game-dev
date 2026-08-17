import type { V4CameraOffset } from "../v4";
import { createRoomV5 } from "../v5/room";
import type { StaffAction, HumanDirection, V6RoomStaffManifest } from "./contracts";
import { loadStaffFixtureCatalog } from "./fixture-loader";
import { createV6RoomStaffManifest } from "./manifest";
import { StaffV6 } from "./staff";
import { integrateStaffIntoRoomV6 } from "./staff-room-integrator";

export interface V6PreviewOptions {
  readonly roomKey?: string;
  readonly cameraOffset?: V4CameraOffset;
  readonly sourceStaffIds?: readonly number[];
  readonly action?: StaffAction | string;
  readonly direction?: HumanDirection;
  readonly frame?: number;
  readonly alpha?: number;
}

export function createV6RoomStaffPreview(options: V6PreviewOptions = {}): V6RoomStaffManifest {
  const catalog = loadStaffFixtureCatalog();
  const room = createRoomV5(options.roomKey ?? "room:0", {
    context: "main_display",
    visualScope: "full_static",
    cameraOffset: options.cameraOffset ?? { x: 0, y: 0 },
  });
  const sourceStaffIds = options.sourceStaffIds ?? catalog.actorSpawn.actors.slice(0, 3).map((actor) => actor.source_staff_id);
  const staff = sourceStaffIds.map((sourceStaffId) => new StaffV6({
    sourceStaffId,
    catalog,
    action: options.action ?? "wait",
    direction: options.direction ?? "right",
    frame: options.frame ?? 0,
    alpha: options.alpha ?? 255,
  }));
  const render = integrateStaffIntoRoomV6(room, staff);
  return createV6RoomStaffManifest(room, render);
}
