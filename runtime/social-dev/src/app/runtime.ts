import { loadRuntimeCatalogs, type RuntimeCatalogs } from "../catalog/load-contracts";
import { loadDisplayAssets, type DisplayAssetStatus, type LoadedDisplayAssets } from "../assets/display-assets";
import { characterDisplayFrame, preloadCharacterFrameImages } from "../assets/character-assets";
import { resolveCharacter } from "../catalog/character-resolver";
import { applyFloor00DisplayPolicy, createInitialState, stepSimulation } from "../core/simulation";
import { withDigest } from "../core/digest";
import type { SimulationState } from "../core/types";
import { renderScene } from "../renderer/canvas-renderer";
import { createRuntimeUi, renderRuntimeUi, type RuntimeUiElements } from "../renderer/dom-ui";
import { buildVisualGateSnapshot, type VisualGateSnapshot } from "../renderer/visual-gate";
import { buildSceneProjection, type SceneProjection } from "../scene/projection";
import { parseMainRuntimeRoute } from "./main-route";
import type { RoomSceneContext, SceneProjectionMode } from "../scene/room-resolver";

export interface SocialDevRuntimeController {
  readonly catalogs: RuntimeCatalogs;
  readonly projection: SceneProjection;
  readonly selectRoom: (roomId: string) => SceneProjection;
  readonly getState: () => SimulationState;
  readonly step: (count?: number) => SimulationState;
  readonly selectActor: (actorId: string | null) => SimulationState;
  readonly getVisualGateSnapshot: () => VisualGateSnapshot;
  readonly stop: () => void;
}

function render(
  canvas: HTMLCanvasElement,
  ui: RuntimeUiElements,
  catalogs: RuntimeCatalogs,
  projection: SceneProjection,
  state: SimulationState,
  selectActor: (actorId: string | null) => SimulationState,
  assets: LoadedDisplayAssets | null,
  assetStatus: DisplayAssetStatus,
  rawOverlayEnabled: boolean,
): VisualGateSnapshot {
  if (assets) {
    for (const actor of Object.values(state.actors)) {
      try {
        const resolved = resolveCharacter(catalogs, actor.id);
        const imageAssetId = resolved.imageSelector?.asset?.asset_id;
        if (imageAssetId && !assets.images.has(imageAssetId) && !assets.mapImages.has(imageAssetId)) {
          const genericFrame = characterDisplayFrame(catalogs, actor.id, actor.animation.mode, actor.facing, actor.animation.frame);
          if (genericFrame) {
            void preloadCharacterFrameImages(genericFrame).catch(() => undefined);
          }
        }
      } catch {
        // The bounded scene may contain only approved ActorCatalog records;
        // missing full-catalog metadata must remain a renderer fallback.
      }
    }
  }
  const renderDiagnostics = renderScene(canvas, projection, state, catalogs.camera, assets, rawOverlayEnabled, catalogs);
  const visualGate = buildVisualGateSnapshot(projection, state, catalogs, assets, rawOverlayEnabled, renderDiagnostics);
  renderRuntimeUi(ui, state, catalogs, (actorId) => selectActor(actorId), assetStatus, visualGate, projection.sceneMode, rawOverlayEnabled);
  return visualGate;
}

export function createSocialDevRuntime(root: HTMLElement): SocialDevRuntimeController {
  const catalogs = loadRuntimeCatalogs();
  const route = parseMainRuntimeRoute(window.location.search);
  const requestedRoomId = route.roomId;
  const sceneOptions = route.sceneOptions;
  const rawOverlayEnabled = route.rawOverlayEnabled;
  if (!catalogs.roomSceneRuntime.rooms.some((room) => room.room_key === requestedRoomId)) {
    throw new Error(`Unknown RoomData room ${requestedRoomId}`);
  }
  let activeRoomId = requestedRoomId;
  let projection = buildSceneProjection(catalogs, activeRoomId, sceneOptions);
  let state = createRoomState(catalogs, activeRoomId, projection.roomContext, projection.sceneMode);
  let displayAssets: LoadedDisplayAssets | null = null;
  let assetStatus: DisplayAssetStatus = "loading";
  let visualGateSnapshot: VisualGateSnapshot;
  let handleSelection: (actorId: string) => void = () => undefined;
  let handleRoomSelection: (roomId: string) => void = () => undefined;
  const ui = createRuntimeUi(
    root,
    (actorId) => handleSelection(actorId),
    (roomId) => handleRoomSelection(roomId),
    catalogs.roomSceneRuntime.rooms.map((room) => ({ id: room.room_key, name: room.native.name })),
  );
  const canvas = root.querySelector<HTMLCanvasElement>("#scene-canvas");
  if (!canvas) {
    throw new Error("Runtime canvas is missing");
  }

  handleSelection = (actorId) => {
    state = selectActor(actorId);
  };

  handleRoomSelection = (roomId) => {
    state = selectRoomState(roomId);
  };

  const selectRoom = (roomId: string): SceneProjection => {
    if (!catalogs.roomSceneRuntime.rooms.some((room) => room.room_key === roomId)) {
      throw new Error(`Unknown RoomData room ${roomId}`);
    }
    activeRoomId = roomId;
    projection = buildSceneProjection(catalogs, activeRoomId, sceneOptions);
    state = createRoomState(catalogs, activeRoomId, projection.roomContext, projection.sceneMode);
    visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
    return projection;
  };

  const selectRoomState = (roomId: string): SimulationState => {
    selectRoom(roomId);
    return state;
  };

  const selectActor = (actorId: string | null): SimulationState => {
    state = selectActorState(state, actorId);
    visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
    return state;
  };

  const step = (count = 1): SimulationState => {
    if (!Number.isInteger(count) || count < 0) {
      throw new Error("Runtime step count must be a non-negative integer");
    }
    for (let index = 0; index < count; index += 1) {
      if (projection.sceneMode !== "floor00" && state.sceneId === "room:0" && projection.roomContext === "main_display") {
        state = stepSimulation(state, catalogs);
      }
    }
    visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
    return state;
  };

  const initialTicks = route.initialTicks;
  if (projection.sceneMode !== "floor00" && activeRoomId === "room:0" && projection.roomContext === "main_display" && Number.isInteger(initialTicks) && initialTicks > 0) {
    for (let index = 0; index < initialTicks; index += 1) {
      state = stepSimulation(state, catalogs);
    }
  }
  visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
  // The wall-clock driver only requests fixed logical steps. The core itself
  // never reads time, uses randomness, or mutates from the renderer/UI.
  const timer = !route.auto || projection.sceneMode === "floor00" ? undefined : window.setInterval(() => step(1), 150);

  const controller: SocialDevRuntimeController = {
    catalogs,
    get projection() {
      return projection;
    },
    selectRoom,
    getState: () => state,
    step,
    selectActor,
    getVisualGateSnapshot: () => visualGateSnapshot,
    stop: () => {
      if (timer !== undefined) {
        window.clearInterval(timer);
      }
    },
  };
  (window as Window & { __SOCIAL_DEV_RUNTIME__?: SocialDevRuntimeController }).__SOCIAL_DEV_RUNTIME__ = controller;
  void loadDisplayAssets()
    .then((loaded) => {
      displayAssets = loaded;
      assetStatus = loaded.status;
      visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
    })
    .catch(() => {
      assetStatus = "fallback";
      visualGateSnapshot = render(canvas, ui, catalogs, projection, state, selectActor, displayAssets, assetStatus, rawOverlayEnabled);
    });
  return controller;
}

function createRoomState(
  catalogs: RuntimeCatalogs,
  roomId: string,
  context: RoomSceneContext = "main_display",
  sceneMode: SceneProjectionMode = "floor00",
): SimulationState {
  const base = createInitialState(catalogs);
  if (roomId === "room:0" && context === "main_display") {
    return sceneMode === "floor00" ? applyFloor00DisplayPolicy(base, catalogs) : base;
  }
  const { digest: _digest, ...withoutDigest } = base;
  return withDigest({
    ...withoutDigest,
    sceneId: roomId,
    actors: {},
    events: [],
    eventLog: [],
    selectedActorId: null,
  });
}

function selectActorState(
  state: SimulationState,
  actorId: string | null,
): SimulationState {
  if (actorId !== null && !state.actors[actorId]) {
    throw new Error(`Cannot select unknown actor ${actorId}`);
  }
  // Selection is a UI command, not a simulation tick. Restore the current
  // frame/event stream while preserving the deterministic selected id.
  const { digest: _digest, ...stateWithoutDigest } = state;
  const selectedState = withDigest({ ...stateWithoutDigest, selectedActorId: actorId });
  return selectedState;
}
