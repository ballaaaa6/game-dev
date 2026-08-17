import { loadRuntimeCatalogs, type RuntimeCatalogs } from "../catalog/load-contracts";
import { loadDisplayAssets, type DisplayAssetStatus, type LoadedDisplayAssets } from "../assets/display-assets";
import {
  characterDisplayFrame,
  characterDisplayFrameForSelector,
  characterFrameAssetIds,
  getCachedCharacterImage,
  preloadCharacterFrameImages,
} from "../assets/character-assets";
import { resolveCharacter } from "../catalog/character-resolver";
import { createLivingRuntime } from "../core/living/runtime";
import { projectLivingStaffs } from "../core/living/projection";
import type { LivingSnapshot } from "../core/living/types";
import { withDigest } from "../core/digest";
import type { RuntimeEvent, SimulationState } from "../core/types";
import { createDashboardRuntime, createDashboardUi, renderDashboardUi, type DashboardRuntime, type DashboardRuntimeSnapshot, type DashboardUiElements } from "../product/dashboard";
import { renderScene } from "../renderer/canvas-renderer";
import { createRuntimeUi, renderRuntimeUi, type RuntimeUiElements } from "../renderer/dom-ui";
import { buildVisualGateSnapshot, type VisualGateSnapshot } from "../renderer/visual-gate";
import { buildSceneProjection, type SceneProjection } from "../scene/projection";
import { parseMainRuntimeRoute } from "./main-route";
import { createV8LiveRuntime, type V8LiveRuntime } from "../v8/live-runtime";
import type { V8LiveSnapshot } from "../v8/contracts";

export interface SocialDevRuntimeController {
  readonly catalogs: RuntimeCatalogs;
  readonly projection: SceneProjection;
  readonly dashboard: DashboardRuntime;
  readonly selectRoom: (roomId: string) => SceneProjection;
  readonly getState: () => SimulationState;
  readonly getDashboardSnapshot: () => DashboardRuntimeSnapshot;
  readonly step: (count?: number) => SimulationState;
  readonly selectActor: (actorId: string | null) => SimulationState;
  readonly getVisualGateSnapshot: () => VisualGateSnapshot;
  readonly getV8Snapshot: () => V8LiveSnapshot;
  readonly stop: () => void;
}

function runtimeEventFromTrace(trace: LivingSnapshot["traces"][number]): RuntimeEvent {
  return {
    tick: trace.tick,
    type: trace.event,
    actorIds: trace.staffId === null ? [] : [`actor:staff:${trace.staffId}`],
    frame: trace.tick,
  };
}

function stateFromLiving(
  catalogs: RuntimeCatalogs,
  living: LivingSnapshot,
  sceneId: string,
  activeMainDisplay: boolean,
  selectedActorId: string | null,
  v8: V8LiveSnapshot | undefined,
): SimulationState {
  const eventLog = living.traces.slice(-96).map(runtimeEventFromTrace);
  const events = living.traces.slice(-24).map(runtimeEventFromTrace);
  const baseActors = activeMainDisplay ? projectLivingStaffs(catalogs, living.staffs) : {};
  const actors = Object.fromEntries(Object.values(baseActors).map((actor) => {
    const visual = v8?.staffs.find((candidate) => candidate.actorId === actor.id);
    if (!visual) return [actor.id, actor] as const;
    return [actor.id, {
      ...actor,
      cell: [visual.cell[0], visual.cell[1]] as const,
      position: { ...visual.world },
      alpha: visual.alpha,
      lifecycle: visual.lifecycle === "home" ? "idle" : visual.lifecycle,
      facing: visual.direction,
      route: visual.route.map((cell) => [cell[0], cell[1]] as const),
      talkFrame: visual.action === "talk" ? visual.frame : null,
      animation: {
        mode: visual.action === "typing" || visual.action === "talk" ? "typing" as const : "wait" as const,
        frame: visual.frame,
        selectorId: visual.selectorId,
      },
    }] as const;
  }));
  const { digest: _digest, ...withoutDigest } = {
    frame: living.frame,
    sceneId,
    actors,
    events,
    eventLog,
    selectedActorId,
    tickOperations: living.frame === 0
      ? ["LivingRuntime.snapshot", "DashboardRuntime.publish"]
      : ["LivingRuntime.tick", "AssignmentAdapter.observeLiving", "DashboardRuntime.publish"],
    living,
    v8,
    digest: "",
  };
  return withDigest(withoutDigest);
}

function render(
  canvas: HTMLCanvasElement,
  ui: RuntimeUiElements,
  dashboardUi: DashboardUiElements,
  catalogs: RuntimeCatalogs,
  projection: SceneProjection,
  state: SimulationState,
  dashboard: DashboardRuntime,
  dashboardSnapshot: DashboardRuntimeSnapshot,
  selectActor: (actorId: string | null) => SimulationState,
  assets: LoadedDisplayAssets | null,
  assetStatus: DisplayAssetStatus,
  rawOverlayEnabled: boolean,
  onAsyncAssetsReady?: () => void,
): VisualGateSnapshot {
  const pendingCharacterPreloads: Promise<unknown>[] = [];
  const preloadCharacterFrame = (frame: ReturnType<typeof characterDisplayFrame>): void => {
    if (!frame) return;
    const hasUncachedAsset = characterFrameAssetIds(frame).some((assetId) => !getCachedCharacterImage(assetId));
    if (!hasUncachedAsset) return;
    pendingCharacterPreloads.push(preloadCharacterFrameImages(frame).catch(() => undefined));
  };
  if (assets) {
    for (const actor of Object.values(state.actors)) {
      try {
        const resolved = resolveCharacter(catalogs, actor.id);
        const imageAssetId = resolved.imageSelector?.asset?.asset_id;
        if (imageAssetId && !assets.images.has(imageAssetId) && !assets.mapImages.has(imageAssetId)) {
          const genericFrame = characterDisplayFrame(catalogs, actor.id, actor.animation.mode, actor.facing, actor.animation.frame);
          preloadCharacterFrame(genericFrame);
        }
      } catch {
        // The bounded scene may contain only approved ActorCatalog records;
        // missing full-catalog metadata must remain a renderer fallback.
      }
    }
    if (state.v8) {
      for (const staff of state.v8.staffs) {
        try {
          const frame = characterDisplayFrameForSelector(catalogs, staff.actorId, staff.action, staff.direction, staff.selectorId, staff.frame);
          preloadCharacterFrame(frame);
        } catch {
          // The visual gate records selector/asset evidence; rendering never
          // invents a fallback marker for a missing full-catalog character.
        }
      }
    }
  }
  if (pendingCharacterPreloads.length > 0 && onAsyncAssetsReady) {
    void Promise.all(pendingCharacterPreloads).then(onAsyncAssetsReady);
  }
  const renderDiagnostics = renderScene(canvas, projection, state, catalogs.camera, assets, rawOverlayEnabled, catalogs);
  const visualGate = buildVisualGateSnapshot(projection, state, catalogs, assets, rawOverlayEnabled, renderDiagnostics);
  renderRuntimeUi(ui, state, catalogs, (actorId) => selectActor(actorId), assetStatus, visualGate, projection.sceneMode, rawOverlayEnabled);
  renderDashboardUi(dashboardUi, dashboardSnapshot, { execute: (command) => dashboard.execute(command) });
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
  const living = createLivingRuntime(catalogs, { initialStaffDataIds: [0, 1, 2] });
  const v8Runtime: V8LiveRuntime = createV8LiveRuntime(catalogs, living.snapshot());
  const dashboard = createDashboardRuntime(living);
  let activeRoomId = requestedRoomId;
  let projection = buildSceneProjection(catalogs, activeRoomId, sceneOptions);
  let dashboardSnapshot = dashboard.getSnapshot();
  let v8Snapshot = v8Runtime.snapshot();
  let state = stateFromLiving(catalogs, dashboardSnapshot.living, activeRoomId, activeRoomId === "room:0" && projection.roomContext === "main_display", null, v8Snapshot);
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
  const dashboardUi = createDashboardUi(root, { execute: (command) => dashboard.execute(command) });
  const canvas = root.querySelector<HTMLCanvasElement>("#scene-canvas");
  if (!canvas) {
    throw new Error("Runtime canvas is missing");
  }

  const activeMainDisplay = (): boolean => activeRoomId === "room:0" && projection.roomContext === "main_display";
  const renderCurrent = (): VisualGateSnapshot => {
    visualGateSnapshot = render(
      canvas,
      ui,
      dashboardUi,
      catalogs,
      projection,
      state,
      dashboard,
      dashboardSnapshot,
      selectActor,
      displayAssets,
      assetStatus,
      rawOverlayEnabled,
      () => renderCurrent(),
    );
    return visualGateSnapshot;
  };

  dashboard.subscribe((nextSnapshot) => {
    dashboardSnapshot = nextSnapshot;
    v8Snapshot = v8Runtime.advance(nextSnapshot.living);
    state = stateFromLiving(catalogs, nextSnapshot.living, activeRoomId, activeMainDisplay(), state.selectedActorId, v8Snapshot);
    if (state.selectedActorId && !state.actors[state.selectedActorId]) {
      state = selectActorState(state, null);
    }
    renderCurrent();
  });

  handleSelection = (actorId) => {
    selectActor(actorId);
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
    state = stateFromLiving(catalogs, dashboardSnapshot.living, activeRoomId, activeMainDisplay(), null, v8Snapshot);
    renderCurrent();
    return projection;
  };

  const selectRoomState = (roomId: string): SimulationState => {
    selectRoom(roomId);
    return state;
  };

  const selectActor = (actorId: string | null): SimulationState => {
    state = selectActorState(state, actorId);
    renderCurrent();
    return state;
  };

  const step = (count = 1): SimulationState => {
    if (!Number.isInteger(count) || count < 0) {
      throw new Error("Runtime step count must be a non-negative integer");
    }
    if (count === 0) renderCurrent();
    else dashboard.step(count);
    return state;
  };

  const initialTicks = route.initialTicks;
  if (Number.isInteger(initialTicks) && initialTicks > 0) {
    dashboard.step(initialTicks);
  }
  if (initialTicks === 0) renderCurrent();
  // The wall-clock driver only requests fixed logical steps. The core itself
  // never reads time, uses randomness, or mutates from the renderer/UI.
  const timer = !route.auto ? undefined : window.setInterval(() => step(1), 150);

  const controller: SocialDevRuntimeController = {
    catalogs,
    get projection() {
      return projection;
    },
    dashboard,
    selectRoom,
    getState: () => state,
    getDashboardSnapshot: () => dashboard.getSnapshot(),
    step,
    selectActor,
    getVisualGateSnapshot: () => visualGateSnapshot,
    getV8Snapshot: () => v8Snapshot,
    stop: () => {
      if (timer !== undefined) {
        window.clearInterval(timer);
      }
      dashboard.dispose();
    },
  };
  (window as Window & { __SOCIAL_DEV_RUNTIME__?: SocialDevRuntimeController }).__SOCIAL_DEV_RUNTIME__ = controller;
  void loadDisplayAssets()
    .then((loaded) => {
      displayAssets = loaded;
      assetStatus = loaded.status;
      renderCurrent();
    })
    .catch(() => {
      assetStatus = "fallback";
      renderCurrent();
    });
  return controller;
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
