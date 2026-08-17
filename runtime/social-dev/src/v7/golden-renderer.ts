import type { GraphicsCommand } from "../v2/graphics";
import { createV6RoomStaffPreview } from "../v6";
import { createRoomV5 } from "../v5";
import type {
  V7RasterImage,
  V7RasterOptions,
  V7RenderResult,
} from "./contracts";
import { RasterCompatibilityV7 } from "./raster";

export const V7_ROOM_RASTER_OPTIONS: V7RasterOptions = {
  width: 980,
  height: 600,
  origin: { x: 82, y: 260 },
  background: [0, 0, 0, 0],
};

export interface V7SceneCommandSource {
  readonly phase: "V5" | "V6";
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly unknown[];
  readonly events: readonly unknown[];
  readonly sourceManifest: string;
}

export interface V7SceneRasterResult {
  readonly source: V7SceneCommandSource;
  readonly raster: V7RenderResult;
}

export function renderV7Commands(
  commands: readonly GraphicsCommand[],
  images: ReadonlyMap<string, V7RasterImage>,
  options: V7RasterOptions = V7_ROOM_RASTER_OPTIONS,
): V7RenderResult {
  return new RasterCompatibilityV7(options).render(commands, images);
}

export function renderV7Room00Structural(
  images: ReadonlyMap<string, V7RasterImage>,
  options: V7RasterOptions = V7_ROOM_RASTER_OPTIONS,
): V7SceneRasterResult {
  const room = createRoomV5("room:0", {
    context: "main_display",
    visualScope: "full_static",
  });
  const render = room.draw();
  return {
    source: {
      phase: "V5",
      commands: render.commands,
      traces: render.traces,
      events: render.events,
      sourceManifest: "runtime/social-dev/src/v5/manifest.ts",
    },
    raster: renderV7Commands(render.commands, images, options),
  };
}

export function renderV7Room00WithStaff(
  images: ReadonlyMap<string, V7RasterImage>,
  options: V7RasterOptions = V7_ROOM_RASTER_OPTIONS,
): V7SceneRasterResult {
  const manifest = createV6RoomStaffPreview({
    roomKey: "room:0",
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
  });
  return {
    source: {
      phase: "V6",
      commands: manifest.commands,
      traces: manifest.traces,
      events: manifest.events,
      sourceManifest: "runtime/social-dev/src/v6/manifest.ts",
    },
    raster: renderV7Commands(manifest.commands, images, options),
  };
}
