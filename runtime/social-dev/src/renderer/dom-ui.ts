import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { SimulationState } from "../core/types";
import type { DisplayAssetStatus } from "../assets/display-assets";
import type { VisualGateSnapshot } from "./visual-gate";

export interface RuntimeUiElements {
  readonly frame: HTMLElement;
  readonly actorCount: HTMLElement;
  readonly sceneValue: HTMLElement;
  readonly sceneMode: HTMLElement;
  readonly digest: HTMLElement;
  readonly selected: HTMLElement;
  readonly actorList: HTMLElement;
  readonly eventLog: HTMLElement;
  readonly contractList: HTMLElement;
  readonly machineState: HTMLElement;
  readonly assetStatus: HTMLElement;
  readonly visualGateStatus: HTMLElement;
  readonly roomSelect: HTMLSelectElement;
  readonly notice: HTMLElement;
}

const ACTOR_COLORS = ["#66c4ff", "#ff9e76", "#a78bfa", "#72dfae", "#f7d26d"] as const;

function element<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  return node;
}

function clear(node: HTMLElement): void {
  node.replaceChildren();
}

export function createRuntimeUi(
  root: HTMLElement,
  onSelect: (actorId: string) => void,
  onRoomSelect: (roomId: string) => void,
  rooms: readonly { readonly id: string; readonly name: string }[],
): RuntimeUiElements {
  root.innerHTML = `
    <div class="app-shell">
      <header class="app-header">
        <div>
          <p class="eyebrow">Social Dev · native scene runtime</p>
          <h1>Living Scene Runtime</h1>
        </div>
        <div class="header-meta">
          <span class="status-pill">source contracts loaded</span>
            <span id="asset-status" class="status-pill" data-assets-status="loading">display assets loading</span>
            <span id="visual-gate-status" class="status-pill" data-visual-gate-status="loading">visual gate loading</span>
        </div>
      </header>
      <div class="runtime-layout">
        <section class="panel scene-panel">
          <div class="scene-toolbar">
            <div><h2 id="scene-title">RoomData scene</h2><p>RoomData → shared MapChip → raw ObjChip resolver</p></div>
            <label class="room-picker">Room <select id="room-select" aria-label="Select RoomData room"></select></label>
            <div id="selected-actor" class="status-pill">selected: —</div>
          </div>
          <div class="scene-frame"><canvas id="scene-canvas" width="980" height="600" aria-label="Social Dev room display"></canvas></div>
        </section>
        <aside class="side-column">
          <section class="panel side-panel">
            <h2>Runtime snapshot</h2>
            <div class="metrics">
              <div class="metric"><span class="metric-label">Fixed frame</span><span id="frame-value" class="metric-value">0</span></div>
              <div class="metric"><span class="metric-label">Actors</span><span id="actor-count" class="metric-value">0</span></div>
              <div class="metric"><span class="metric-label">Scene</span><span id="scene-value" class="metric-value">room:0</span></div>
              <div class="metric"><span class="metric-label">Mode</span><span id="scene-mode" class="metric-value">floor00</span></div>
              <div class="metric"><span class="metric-label">Digest</span><span id="digest-value" class="metric-value">—</span></div>
            </div>
          </section>
          <section class="panel side-panel"><h2>Actors</h2><div id="actor-list" class="actor-list"></div></section>
          <section class="panel side-panel"><h2>Event trace</h2><div id="event-log" class="event-log"></div></section>
          <section class="panel side-panel">
            <h2>Evidence boundary</h2>
            <dl id="contract-list" class="contract-list"></dl>
            <p id="runtime-notice" class="notice"></p>
          </section>
          <output id="runtime-state" hidden></output>
        </aside>
      </div>
    </div>
  `;

  const canvas = root.querySelector<HTMLCanvasElement>("#scene-canvas");
  if (!canvas) {
    throw new Error("Scene canvas was not created");
  }
  const frame = root.querySelector<HTMLElement>("#frame-value");
  const actorCount = root.querySelector<HTMLElement>("#actor-count");
  const sceneValue = root.querySelector<HTMLElement>("#scene-value");
  const sceneMode = root.querySelector<HTMLElement>("#scene-mode");
  const digest = root.querySelector<HTMLElement>("#digest-value");
  const selected = root.querySelector<HTMLElement>("#selected-actor");
  const actorList = root.querySelector<HTMLElement>("#actor-list");
  const eventLog = root.querySelector<HTMLElement>("#event-log");
  const contractList = root.querySelector<HTMLElement>("#contract-list");
  const machineState = root.querySelector<HTMLElement>("#runtime-state");
  const assetStatus = root.querySelector<HTMLElement>("#asset-status");
  const visualGateStatus = root.querySelector<HTMLElement>("#visual-gate-status");
  const roomSelect = root.querySelector<HTMLSelectElement>("#room-select");
  const notice = root.querySelector<HTMLElement>("#runtime-notice");
  if (!frame || !actorCount || !sceneValue || !sceneMode || !digest || !selected || !actorList || !eventLog || !contractList || !machineState || !assetStatus || !visualGateStatus || !roomSelect || !notice) {
    throw new Error("Runtime UI elements were not created");
  }
  for (const room of rooms) {
    const option = document.createElement("option");
    option.value = room.id;
    option.textContent = `${room.name} · ${room.id}`;
    roomSelect.append(option);
  }
  roomSelect.addEventListener("change", () => onRoomSelect(roomSelect.value));
  return { frame, actorCount, sceneValue, sceneMode, digest, selected, actorList, eventLog, contractList, machineState, assetStatus, visualGateStatus, roomSelect, notice };
}

export function renderRuntimeUi(
  elements: RuntimeUiElements,
  state: SimulationState,
  catalogs: RuntimeCatalogs,
  onSelect: (actorId: string) => void,
  assetStatus: DisplayAssetStatus,
  visualGate: VisualGateSnapshot,
  sceneMode: string,
  rawOverlayEnabled: boolean,
): void {
  elements.frame.textContent = String(state.frame);
  elements.actorCount.textContent = String(Object.keys(state.actors).length);
  elements.sceneValue.textContent = state.sceneId;
  elements.sceneMode.textContent = sceneMode;
  elements.digest.textContent = state.digest;
  elements.selected.textContent = `selected: ${state.selectedActorId ?? "—"}`;
  elements.machineState.dataset.frame = String(state.frame);
  elements.machineState.dataset.digest = state.digest;
  elements.machineState.dataset.visualGateStatus = visualGate.gate_status;
  elements.machineState.dataset.rawOverlay = String(rawOverlayEnabled);
  elements.machineState.dataset.renderTrace = String(visualGate.render_diagnostics.render_trace.length);
  elements.assetStatus.dataset.assetsStatus = assetStatus;
  elements.assetStatus.textContent = `display assets ${assetStatus}`;
  elements.visualGateStatus.dataset.visualGateStatus = visualGate.gate_status;
  elements.visualGateStatus.textContent = `visual gate ${visualGate.gate_status.replaceAll("_", " ")}`;
  elements.roomSelect.value = state.sceneId;
  const room = catalogs.roomSceneRuntime.rooms.find((candidate) => candidate.room_key === state.sceneId);
  const title = elements.roomSelect.closest(".scene-toolbar")?.querySelector("h2");
  if (title) {
    title.textContent = `${room?.native.name ?? state.sceneId} · ${state.sceneId} · ${sceneMode}`;
  }
  elements.machineState.textContent = JSON.stringify({
    frame: state.frame,
    digest: state.digest,
    events: state.eventLog,
    actors: Object.values(state.actors).map((actor) => ({
      id: actor.id,
      cell: actor.cell,
      lifecycle: actor.lifecycle,
      talkFrame: actor.talkFrame,
      animationMode: actor.animation.mode,
      selectorId: actor.animation.selectorId,
    })),
    visualGate: {
      status: visualGate.gate_status,
      frameChecks: visualGate.frame_checks,
      renderDiagnostics: visualGate.render_diagnostics,
      checks: visualGate.checks,
      metadataMissing: visualGate.metadata_missing,
      unresolved: visualGate.unresolved,
    },
  });

  clear(elements.actorList);
  Object.values(state.actors).sort((left, right) => left.id.localeCompare(right.id)).forEach((actor) => {
    const button = element("button", `actor-button${state.selectedActorId === actor.id ? " is-selected" : ""}`);
    button.type = "button";
    button.dataset.actorId = actor.id;
    button.addEventListener("click", () => onSelect(actor.id));
    const swatch = element("span", "actor-swatch");
    swatch.style.background = ACTOR_COLORS[actor.sourceId % ACTOR_COLORS.length];
    const copy = element("span");
    const name = element("span", "actor-name");
    name.textContent = actor.name;
    const detail = element("span", "actor-detail");
    detail.textContent = `${actor.id} · cell ${actor.cell.join(",")}`;
    copy.append(name, detail);
    const status = element("span", "actor-state");
    status.textContent = actor.lifecycle;
    button.append(swatch, copy, status);
    elements.actorList.append(button);
  });

  clear(elements.eventLog);
  [...state.eventLog].slice(-12).reverse().forEach((event) => {
    const row = element("div", "event-row");
    const tick = element("span", "event-tick");
    tick.textContent = `F${event.tick}`;
    const text = element("span");
    text.textContent = `${event.type}${event.frame === undefined ? "" : ` · marker ${event.frame}`} · ${event.actorIds.join(", ")}`;
    row.append(tick, text);
    elements.eventLog.append(row);
  });
  if (state.eventLog.length === 0) {
    const empty = element("div", "event-row");
    empty.textContent = "No events yet";
    elements.eventLog.append(empty);
  }

  const activeRoom = catalogs.roomSceneRuntime.rooms.find((candidate) => candidate.room_key === state.sceneId);
  const floorSelector = activeRoom?.selectors.floor;
  const floorRender = floorSelector?.runtime_alias?.render_filename ?? floorSelector?.target_filename ?? "unresolved";
  const floorSelectorLabel = floorSelector?.runtime_alias
    ? `${floorRender} · selector ${floorSelector.runtime_alias.selector_id}/${floorSelector.runtime_alias.metadata_filename}`
    : `${floorRender} · selector ${floorSelector?.native_selector_id ?? floorSelector?.native_id ?? "?"}`;
  const roomBlockers = activeRoom
    ? (["floor", "wall", "door"] as const)
        .map((role) => activeRoom.selectors[role])
        .filter((selector) => !selector.status.includes("resolved"))
        .map((selector) => selector.field)
        .join(", ") || "none"
    : "unknown room";
  const roomNotice = activeRoom?.selectors.floor.runtime_alias
    ? `Explicit floor alias: render ${floorRender} pixels; retain source selector ${activeRoom.selectors.floor.native_id} and metadata ${activeRoom.selectors.floor.runtime_alias.metadata_filename}.`
    : `Native floor selector ${activeRoom?.selectors.floor.native_selector_id ?? activeRoom?.selectors.floor.native_id ?? "?"} resolves to ${floorRender}; wall/door runtime promotion remains asset-specific.`;
  const overlayNotice = rawOverlayEnabled && state.sceneId === "room:17"
    ? " Room R raw overlay is diagnostic-only; raw cells are not FurnitureData instances."
    : "";
  const floor00Notice = sceneMode === "floor00"
    ? " Floor00 uses the native NewGame bootstrap: 14×14 MapChip, 10×10 ObjChip, six native furniture instances, and three static actors reserved in verified empty cells for map inspection."
    : "";
  const floor00Furniture = sceneMode === "floor00"
    ? catalogs.floor00.native_initial_furniture
        .map((item) => `${item.object_id}@${item.cell.join(",")}`)
        .join(" · ")
    : "unavailable in main";
  const floor00Door = sceneMode === "floor00"
    ? `${catalogs.floor00.door.cell.join(",")} · FurnitureData=null`
    : "unavailable in main";
  elements.notice.textContent = `${roomNotice}${floor00Notice}${overlayNotice}`;
  const contractEntries: [string, string][] = [
    ["SceneCatalog", catalogs.scene.status],
    ["ObjectCatalog", catalogs.objects.status],
    ["ActorCatalog", catalogs.actors.status],
    ["Room placement", catalogs.roomPlacement.status],
    ["Phase 3C render", catalogs.render3c.status],
    ["Native initial furniture", `${catalogs.strictClosure.native_initial_bindings.length} bindings`],
    ["Depth occlusion", "rear wall → furniture/actors → lower front wall"],
    ["Tick order", catalogs.tickOrder.status],
    ["Pre-runtime", catalogs.preRuntime.status],
    ["Native content", `${catalogs.nativeContent.counts.data_records} records · ${catalogs.nativeContent.counts.assets} assets · ${catalogs.nativeContent.counts.selectors} selectors`],
    ["Scene assembly", `${catalogs.nativeAssembly.counts.rooms} rooms · ${catalogs.nativeAssembly.counts.wall_compositions_closed}/${catalogs.nativeAssembly.counts.door_compositions_closed} wall/door`],
    ["Room resolver", `${catalogs.roomSceneRuntime.counts.rooms} rooms · ${catalogs.nativeAssembly.counts.objchip_cells} ObjChip cells`],
    ["Scene mode", sceneMode],
    ["Floor00 bootstrap", `${catalogs.floor00.map.map_chip_cells} MapChip · ${catalogs.floor00.map.obj_chip_cells} ObjChip · ${catalogs.floor00.native_initial_furniture.length} furniture · ${catalogs.floor00.actors.length} actors`],
    ["Floor00 furniture", floor00Furniture],
    ["Floor00 door", floor00Door],
    ["Native furniture cards", String(visualGate.drawable_cards.filter((card) => card.kind === "native_initial_object").length)],
    ["Direction", catalogs.nativeAssembly.direction.status],
    ["Visual gate", visualGate.gate_status],
    ["Furniture render", visualGate.checks.furniture_render.details],
    ["Native collision", visualGate.checks.native_collision.details],
    ["Final pixel visibility", visualGate.checks.floor00_final_pixel_visibility.details],
    ["Raw overlay", rawOverlayEnabled && state.sceneId === "room:17" ? "room:17 diagnostic" : "off"],
    ["Drawable cards", String(visualGate.drawable_cards.length)],
    ["Render trace", `${visualGate.render_diagnostics.render_trace.length} records`],
    ["Display assets", assetStatus],
    ["Floor selector", floorSelectorLabel],
    ["Scene blockers", roomBlockers],
  ];
  clear(elements.contractList);
  for (const [label, value] of contractEntries) {
    const row = element("div");
    const term = element("dt");
    term.textContent = label;
    const description = element("dd");
    description.textContent = value;
    row.append(term, description);
    elements.contractList.append(row);
  }
}
