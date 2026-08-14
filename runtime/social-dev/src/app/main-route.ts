import type { SceneProjectionMode } from "../scene/room-resolver";

export interface MainRuntimeRoute {
  readonly roomId: string;
  readonly rawOverlayEnabled: boolean;
  readonly initialTicks: number;
  readonly auto: boolean;
  readonly sceneOptions: {
    readonly nativeFloorValue: 0;
    readonly context: "main_display";
    readonly sceneMode: SceneProjectionMode;
  };
}

const MAIN_SCENE_OPTIONS = {
  nativeFloorValue: 0,
  context: "main_display",
  sceneMode: "floor00",
} as const satisfies MainRuntimeRoute["sceneOptions"];

function parseInitialTicks(rawValue: string | null): number {
  const value = Number(rawValue ?? "0");
  return Number.isInteger(value) && value > 0 ? value : 0;
}

export function parseMainRuntimeRoute(search: string): MainRuntimeRoute {
  const query = new URLSearchParams(search);

  return {
    roomId: query.get("room") ?? "room:0",
    rawOverlayEnabled: query.get("overlay") === "raw",
    initialTicks: parseInitialTicks(query.get("initialTicks")),
    auto: query.get("auto") !== "0",
    sceneOptions: MAIN_SCENE_OPTIONS,
  };
}
