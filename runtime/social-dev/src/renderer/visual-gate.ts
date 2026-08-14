import {
  actorDisplayFrame,
  displayAssetManifest,
  furnitureFrameForScene,
  type DisplayFrameRecord,
  type LoadedDisplayAssets,
} from "../assets/display-assets";
import {
  characterDisplayFrame,
  characterFrameAssetIds,
  characterFrameRecordAssetId,
  getCachedCharacterImage,
  type CharacterDisplayFrame,
} from "../assets/character-assets";
import type { CharacterAssetFrameRecord } from "../catalog/types";
import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { SimulationState } from "../core/types";
import type { RenderDiagnostics } from "./canvas-renderer";
import { createRenderPassPlan } from "./render-plan";
import type { SceneProjection } from "../scene/projection";
import { evaluateActorFloorContainment } from "../scene/actor-floor-mask";
import { emptyFinalVisibilityDiagnostics } from "./visibility";

export type VisualGateCheckStatus = "pass" | "pending" | "blocked_by_evidence" | "not_applicable";

export interface VisualGateCheck {
  readonly status: VisualGateCheckStatus;
  readonly details: string;
}

export interface VisualDrawableCard {
  readonly id: string;
  readonly kind: string;
  readonly roomId: string;
  readonly cell: readonly [number, number] | null;
  readonly assetId: string | null;
  readonly renderPass: string;
  readonly status: string;
}

export interface VisualGateSnapshot {
  readonly schema_version: "social-dev-visual-gate-snapshot-v1";
  readonly semantic_status: "deterministic_visual_gate_snapshot";
  readonly gate_status: "pass" | "pending_assets" | "blocked_by_evidence";
  readonly scene_id: string;
  readonly frame: number;
  readonly digest: string;
  readonly raw_overlay_enabled: boolean;
  readonly asset_status: string;
  readonly render_passes: readonly string[];
  readonly frame_checks: {
    readonly total: number;
    readonly checked_against_loaded_images: number;
    readonly missing_assets: readonly string[];
    readonly out_of_bounds: readonly string[];
  };
  readonly render_diagnostics: RenderDiagnostics;
  readonly drawable_cards: readonly VisualDrawableCard[];
  readonly metadata_missing: readonly string[];
  readonly unresolved: readonly string[];
  readonly checks: Readonly<Record<string, VisualGateCheck>>;
}

function imageSize(image: HTMLImageElement): { readonly width: number; readonly height: number } {
  return {
    width: image.naturalWidth || image.width,
    height: image.naturalHeight || image.height,
  };
}

function loadedImage(assets: LoadedDisplayAssets | null, assetId: string): HTMLImageElement | undefined {
  return assets?.images.get(assetId) ?? assets?.mapImages.get(assetId) ?? getCachedCharacterImage(assetId);
}

function checkFrameRecords(
  owner: string,
  records: readonly DisplayFrameRecord[],
  assets: LoadedDisplayAssets | null,
  missingAssets: Set<string>,
  outOfBounds: string[],
  defaultAssetId?: string,
): number {
  let checked = 0;
  for (const [index, record] of records.entries()) {
    const assetId = record.runtime_asset_id ?? record.source_asset_id ?? defaultAssetId;
    if (!assetId) {
      outOfBounds.push(`${owner}[${index}]:missing_asset_id`);
      continue;
    }
    const image = loadedImage(assets, assetId);
    if (assets?.status === "ready" && !image) {
      missingAssets.add(assetId);
      continue;
    }
    const fallbackSize = record.runtime_size ?? record.source_size;
    const size = image ? imageSize(image) : fallbackSize;
    if (!size) {
      outOfBounds.push(`${owner}[${index}]:missing_runtime_size`);
      continue;
    }
    checked += 1;
    if (
      record.source_x < 0
      || record.source_y < 0
      || record.width <= 0
      || record.height <= 0
      || record.source_x + record.width > size.width
      || record.source_y + record.height > size.height
    ) {
      outOfBounds.push(`${owner}[${index}]:${assetId}`);
    }
  }
  return checked;
}

function checkCharacterFrameRecords(
  owner: string,
  records: readonly CharacterAssetFrameRecord[],
  assets: LoadedDisplayAssets | null,
  missingAssets: Set<string>,
  outOfBounds: string[],
  defaultAssetId: string,
): number {
  let checked = 0;
  for (const [index, record] of records.entries()) {
    if (record.texture_status === "control_no_texture") {
      checked += 1;
      continue;
    }
    const assetId = characterFrameRecordAssetId(record, defaultAssetId);
    if (!assetId) {
      checked += 1;
      continue;
    }
    const image = loadedImage(assets, assetId);
    if (assets?.status === "ready" && !image) {
      missingAssets.add(assetId);
      continue;
    }
    const size = image ? imageSize(image) : record.source_size;
    if (!size) {
      outOfBounds.push(`${owner}[${index}]:missing_runtime_size`);
      continue;
    }
    checked += 1;
    if (
      record.source_x < 0
      || record.source_y < 0
      || record.width <= 0
      || record.height <= 0
      || record.source_x + record.width > size.width
      || record.source_y + record.height > size.height
    ) {
      outOfBounds.push(`${owner}[${index}]:${assetId}`);
    }
  }
  return checked;
}

function resolveGenericCharacterFrame(catalogs: RuntimeCatalogs, actor: SimulationState["actors"][string]): CharacterDisplayFrame | null {
  try {
    return characterDisplayFrame(catalogs, actor.id, actor.animation.mode, actor.facing, actor.animation.frame);
  } catch {
    return null;
  }
}

function drawableCards(
  projection: SceneProjection,
  state: SimulationState,
  rawOverlayEnabled: boolean,
  catalogs: RuntimeCatalogs,
): VisualDrawableCard[] {
  const cards: VisualDrawableCard[] = [];
  for (const cell of projection.mapCells) {
    if (cell.assetId) {
      cards.push({
        id: `mapcell:${projection.sceneId}:map:${cell.cell[0]}:${cell.cell[1]}`,
        kind: "map_chip",
        roomId: projection.sceneId,
        cell: cell.cell,
        assetId: cell.assetId,
        renderPass: cell.nativeFloorPass ? "map-floor" : "map-chip",
        status: cell.meaning,
      });
    }
  }
  for (const wall of projection.extensionWalls) {
    cards.push({
      id: `mapwall:${projection.sceneId}:${wall.cell[0]}:${wall.cell[1]}:${wall.compositionGroup}:${wall.pieceIndex}`,
      kind: "map_extension_wall",
      roomId: projection.sceneId,
      cell: wall.cell,
      assetId: wall.sourceAssetId,
      renderPass: "map-extension-floor",
      status: "resolved_native_two_piece_map_extension_wall",
    });
  }
  for (const asset of projection.sceneAssets) {
    cards.push({
      id: asset.id,
      kind: asset.role,
      roomId: projection.sceneId,
      cell: asset.cell ?? null,
      assetId: asset.runtimeAssetId ?? null,
      renderPass: asset.role === "floor" ? "map-floor" : asset.role === "object" ? "object-chip-primary" : "object-chip-wall",
      status: asset.status,
    });
  }
  for (const facility of projection.structuralFacilities) {
    cards.push({
      id: facility.id,
      kind: "structural_facility",
      roomId: projection.sceneId,
      cell: facility.anchor,
      assetId: facility.imageAssetId,
      renderPass: "object-chip-primary",
      status: facility.renderStatus,
    });
  }
  for (const object of projection.nativeInitialObjects) {
    cards.push({
      id: object.id,
      kind: "native_initial_object",
      roomId: projection.sceneId,
      cell: object.cell,
      assetId: null,
      renderPass: "object-chip-primary",
      status: object.nativeStatus,
    });
  }
  for (const actor of Object.values(state.actors)) {
    const display = actorDisplayFrame(actor.sourceId, actor.animation.mode, actor.animation.selectorId, actor.animation.frame);
    const generic = display ? null : resolveGenericCharacterFrame(catalogs, actor);
    cards.push({
      id: actor.id,
      kind: "actor",
      roomId: projection.sceneId,
      cell: actor.cell,
      assetId: display?.imageAssetId ?? generic?.imageAssetId ?? null,
      renderPass: "avatar-primary",
      status: display?.frame.source_status ?? (generic ? "character_frame_contract_ready" : "fallback_actor_marker"),
    });
  }
  if (rawOverlayEnabled && projection.rawOverlay) {
    for (const cell of projection.rawOverlay.cells) {
      cards.push({
        id: cell.id,
        kind: "raw_overlay_cell",
        roomId: projection.sceneId,
        cell: cell.cell,
        assetId: null,
        renderPass: "diagnostic-overlay",
        status: cell.renderStatus,
      });
    }
  }
  return cards;
}

function checkMetadata(cards: readonly VisualDrawableCard[]): string[] {
  return cards
    .filter((card) => !card.id || !card.kind || !card.roomId || !card.renderPass || !card.status)
    .map((card) => card.id || "missing-id");
}

function cellKey(cell: readonly [number, number]): string {
  return `${cell[0]},${cell[1]}`;
}

function sameCellSet(
  left: readonly (readonly [number, number])[],
  right: readonly (readonly [number, number])[],
): boolean {
  const leftKeys = left.map(cellKey).sort();
  const rightKeys = right.map(cellKey).sort();
  return JSON.stringify(leftKeys) === JSON.stringify(rightKeys);
}

function sameCellScope(
  left: Readonly<Record<string, readonly (readonly [number, number])[]>> | undefined,
  right: Readonly<Record<string, readonly (readonly [number, number])[]>> | undefined,
): boolean {
  if (!left || !right) return false;
  const leftFrames = Object.keys(left).sort();
  const rightFrames = Object.keys(right).sort();
  return JSON.stringify(leftFrames) === JSON.stringify(rightFrames)
    && rightFrames.every((frameId) => sameCellSet(left[frameId] ?? [], right[frameId] ?? []));
}

function screenAnchor(cell: readonly [number, number]): { readonly x: number; readonly y: number } {
  return {
    x: (cell[0] + cell[1]) * 20,
    y: (cell[1] - cell[0]) * 10,
  };
}

function screenDelta(
  from: readonly [number, number],
  to: readonly [number, number],
): { readonly x: number; readonly y: number } {
  const fromAnchor = screenAnchor(from);
  const toAnchor = screenAnchor(to);
  return { x: toAnchor.x - fromAnchor.x, y: toAnchor.y - fromAnchor.y };
}

function orderedStripCells(
  axis: "map_x" | "map_y",
  start: readonly [number, number],
  end: readonly [number, number],
): readonly (readonly [number, number])[] {
  const cells: [number, number][] = [];
  if (axis === "map_x") {
    for (let x = start[0]; x <= end[0]; x += 1) cells.push([x, start[1]]);
  } else {
    for (let y = start[1]; y <= end[1]; y += 1) cells.push([start[0], y]);
  }
  return cells;
}

export function buildVisualGateSnapshot(
  projection: SceneProjection,
  state: SimulationState,
  catalogs: RuntimeCatalogs,
  assets: LoadedDisplayAssets | null,
  rawOverlayEnabled = false,
  renderDiagnostics: RenderDiagnostics = {
    furniture_draw_attempts: 0,
    furniture_asset_draws: 0,
    furniture_subframe_draws: 0,
    furniture_fallbacks: 0,
    structural_facility_draws: 0,
    structural_facility_draw_ids: [],
    furniture_draw_attempt_ids: [],
    furniture_asset_draw_ids: [],
    furniture_fallback_ids: [],
    final_visibility: emptyFinalVisibilityDiagnostics(),
    render_trace: [],
  },
): VisualGateSnapshot {
  const missingAssets = new Set<string>();
  const outOfBounds: string[] = [];
  let totalFrames = 0;
  let checkedFrames = 0;
  const checkManifestRecords = (owner: string, records: readonly DisplayFrameRecord[], defaultAssetId?: string): void => {
    totalFrames += records.length;
    checkedFrames += checkFrameRecords(owner, records, assets, missingAssets, outOfBounds, defaultAssetId);
  };
  for (const [objectId, object] of Object.entries(displayAssetManifest.objects)) {
    checkManifestRecords(`${objectId}.records`, object.records);
    if (object.sub_composition) {
      checkManifestRecords(`${objectId}.sub_composition.records`, object.sub_composition.records);
    }
  }
  for (const [objectId, object] of Object.entries(displayAssetManifest.native_initial_objects)) {
    checkManifestRecords(`${objectId}.records`, object.records);
  }
  for (const actor of displayAssetManifest.actors) {
    for (const [mode, animation] of Object.entries(actor.animations)) {
      checkManifestRecords(`actor:${actor.actor_source_id}.${mode}`, animation.records, actor.image_asset_id);
    }
  }
  for (const actor of Object.values(state.actors)) {
    const bounded = actorDisplayFrame(actor.sourceId, actor.animation.mode, actor.animation.selectorId, actor.animation.frame);
    const generic = bounded ? null : resolveGenericCharacterFrame(catalogs, actor);
    if (generic) {
      totalFrames += generic.records.length;
      checkedFrames += checkCharacterFrameRecords(
        `character:${actor.id}.${generic.action}.${generic.direction}`,
        generic.records,
        assets,
        missingAssets,
        outOfBounds,
        generic.imageAssetId,
      );
    }
  }

  const requiredRuntimeAssets = new Set<string>();
  for (const cell of projection.mapCells) {
    if (cell.assetId) requiredRuntimeAssets.add(cell.assetId);
  }
  for (const wall of projection.extensionWalls) requiredRuntimeAssets.add(wall.sourceAssetId);
  for (const asset of projection.sceneAssets) {
    if (asset.runtimeAssetId) requiredRuntimeAssets.add(asset.runtimeAssetId);
  }
  for (const object of projection.nativeInitialObjects) {
    const display = furnitureFrameForScene(object.objectId, state.frame, projection.sceneMode);
    if (display?.imageAssetId) requiredRuntimeAssets.add(display.imageAssetId);
    if (display?.subImageAssetId) requiredRuntimeAssets.add(display.subImageAssetId);
  }
  for (const facility of projection.structuralFacilities) {
    requiredRuntimeAssets.add(facility.imageAssetId);
  }
  for (const actor of Object.values(state.actors)) {
    const display = actorDisplayFrame(actor.sourceId, actor.animation.mode, actor.animation.selectorId, actor.animation.frame);
    const generic = display ? null : resolveGenericCharacterFrame(catalogs, actor);
    if (display?.imageAssetId) requiredRuntimeAssets.add(display.imageAssetId);
    if (generic) {
      for (const assetId of characterFrameAssetIds(generic)) {
        requiredRuntimeAssets.add(assetId);
      }
    }
  }
  if (assets?.status === "ready") {
    for (const assetId of requiredRuntimeAssets) {
      if (!loadedImage(assets, assetId)) missingAssets.add(assetId);
    }
  }

  const passes = createRenderPassPlan(projection);
  const cards = drawableCards(projection, state, rawOverlayEnabled, catalogs);
  const metadataMissing = checkMetadata(cards);
  const nativePlacementPass = projection.sceneId === "room:0"
    ? projection.nativeInitialObjects.length === catalogs.strictClosure.native_initial_bindings.length
      && projection.nativeInitialObjects.every((object) => object.nativeStatus.length > 0)
    : projection.nativeInitialObjects.length === projection.runtimeRoom.nativeBindings.length;
  const nativeCompositionReady = projection.sceneAssets
    .filter((asset) => asset.role === "wall" || asset.role === "door")
    .every((asset) => asset.status === "approved_native_coordinate_composition" && Boolean(asset.runtimeAssetId));
  const nativeCompositionStatus: VisualGateCheckStatus = nativeCompositionReady ? "pass" : "blocked_by_evidence";
  const floor00ExpectedFurniture = catalogs.floor00.native_initial_furniture.map((item) => `${item.object_id}@${item.cell[0]}:${item.cell[1]}`);
  const floor00ActualFurniture = projection.nativeInitialObjects.map((item) => `${item.objectId}@${item.cell[0]}:${item.cell[1]}`);
  const floor00ExpectedActors = catalogs.floor00DisplayPolicy.actors.map((actor) => actor.id).sort();
  const floor00ActualActors = Object.keys(state.actors).sort();
  const floor00DisplayActorPositionsPass = catalogs.floor00DisplayPolicy.actors.every((expected) => {
    const actor = state.actors[expected.id];
    return Boolean(actor)
      && actor.cell[0] === expected.reserved_cell[0]
      && actor.cell[1] === expected.reserved_cell[1]
      && actor.lifecycle === "idle"
      && actor.route.length === 0;
  });
  const floor00ActorFloorResults = projection.sceneMode === "floor00" && projection.sceneId === "room:0"
    ? catalogs.floor00DisplayPolicy.actors.map((expected) => ({
        actorId: expected.id,
        result: evaluateActorFloorContainment(expected.reserved_cell, projection, catalogs.camera),
      }))
    : [];
  const floor00ActorFloorPass = floor00ActorFloorResults.length === catalogs.floor00DisplayPolicy.actors.length
    && floor00ActorFloorResults.every(({ result }) => result.status === "pass");
  const floor00Layout = projection.presentationLayout;
  const floor00ExpectedGlassCellsByGroup = floor00Layout?.finalGlassCellsByGroup ?? {};
  const floor00ActualGlassCellsByGroup: Record<string, [number, number][]> = {};
  for (const wall of projection.extensionWalls) {
    const cells = floor00ActualGlassCellsByGroup[wall.compositionGroup] ?? [];
    if (!cells.some((cell) => cellKey(cell) === cellKey(wall.triggerCell))) {
      cells.push([wall.triggerCell[0], wall.triggerCell[1]]);
    }
    floor00ActualGlassCellsByGroup[wall.compositionGroup] = cells;
  }
  const floor00GlassGroupsPass = floor00Layout !== null
    && JSON.stringify(Object.keys(floor00ActualGlassCellsByGroup).sort()) === JSON.stringify(Object.keys(floor00ExpectedGlassCellsByGroup).sort())
    && Object.keys(floor00ExpectedGlassCellsByGroup).every((groupId) =>
      sameCellSet(floor00ActualGlassCellsByGroup[groupId] ?? [], floor00ExpectedGlassCellsByGroup[groupId] ?? []))
    && projection.extensionWalls.every((wall) =>
      wall.sourceAssetId === catalogs.floor00VisualLayout.glass.source_asset_id
      && (wall.compositionGroup === "horizontal_frame_0" || wall.compositionGroup === "vertical_frame_1")
      && wall.pieceIndex >= 0
      && wall.pieceIndex < 2);
  const floor00RemovedGlassKeys = new Set((floor00Layout?.removedGlassCells ?? []).map(cellKey));
  const floor00RemovedGlassPass = floor00Layout !== null
    && projection.extensionWalls.every((wall) => !floor00RemovedGlassKeys.has(cellKey(wall.triggerCell)));
  const floor00GlassStripPass = floor00Layout !== null
    && orderedStripCells(
      catalogs.floor00VisualLayout.glass.strip_axis,
      catalogs.floor00VisualLayout.glass.strip_start,
      catalogs.floor00VisualLayout.glass.strip_end,
    ).every((cell) => {
      const key = cellKey(cell);
      return Object.values(floor00ActualGlassCellsByGroup).some((cells) => cells.some((candidate) => cellKey(candidate) === key));
    });
  const floor00WallAsset = projection.sceneAssets.find((asset) => asset.role === "wall");
  const floor00WallScopePass = floor00Layout !== null
    && sameCellScope(floor00WallAsset?.cellScope?.cells, floor00Layout.wallCellsByFrame);
  const floor00Alignment = catalogs.floor00VisualLayout.alignment;
  const floor00UpperEdge = floor00Alignment.upper_edge_cells;
  const floor00LeftEdge = floor00Alignment.left_edge_cells;
  const floor00SharedAlignmentCell = floor00UpperEdge[1] && floor00LeftEdge[0]
    && cellKey(floor00UpperEdge[1]) === cellKey(floor00LeftEdge[0])
    ? floor00UpperEdge[1]
    : null;
  const floor00FinalWallCells = Object.values(floor00Layout?.wallCellsByFrame ?? {}).flat();
  const floor00WallLayerOrderPass = floor00WallAsset?.cellScope?.spriteLayers !== undefined
    && Object.values(floor00WallAsset.cellScope.spriteLayers).every((layers) =>
      layers.map((layer) => layer.layer).join(",") === "0,1");
  const floor00WallAlignmentPass = floor00Layout !== null
    && floor00WallScopePass
    && Boolean(floor00SharedAlignmentCell)
    && floor00FinalWallCells.some((cell) => cellKey(cell) === cellKey(floor00SharedAlignmentCell!))
    && floor00WallLayerOrderPass
    && JSON.stringify(screenDelta(floor00UpperEdge[1] ?? [-1, -1], floor00LeftEdge[0] ?? [-2, -2]))
      === JSON.stringify(floor00Alignment.expected_screen_delta);
  const floor00VisualLayoutPass = projection.sceneMode === "floor00"
    && projection.sceneId === "room:0"
    && floor00Layout?.status === "approved_floor00_visual_layout"
    && floor00Layout.contractId === catalogs.floor00VisualLayout.catalog_id
    && floor00GlassGroupsPass
    && floor00RemovedGlassPass
    && floor00WallScopePass;
  const floor00ExtensionContractPass = projection.sceneMode !== "floor00"
    || projection.sceneId === "room:0"
      && floor00VisualLayoutPass
      && projection.extensionWalls.every((wall) => {
        const record = wall.spriteRecord;
        const width = record.width;
        const height = record.height;
        const sourceX = record.source_x;
        const sourceY = record.source_y;
        return (wall.compositionGroup === "vertical_frame_1" || wall.compositionGroup === "horizontal_frame_0")
          && wall.pieceIndex >= 0
          && wall.pieceIndex < 2
          && typeof width === "number"
          && typeof height === "number"
          && typeof sourceX === "number"
          && typeof sourceY === "number"
          && width > 0
          && width <= 24
          && height === 43
          && sourceX >= 0
          && sourceY === 0
          && sourceX + width <= 96;
      });
  const floor00ExtensionTraceCount = renderDiagnostics.render_trace.filter((entry) =>
    entry.pass_id === "map-extension-floor" && entry.status === "approved_native_two_piece_extension_draw",
  ).length;
  const floor00FurnitureExpectedDrawIds = catalogs.floor00.native_initial_furniture.map((item) => item.object_id).sort();
  const floor00FurnitureActualDrawIds = [...renderDiagnostics.furniture_draw_attempt_ids].sort();
  const floor00FurnitureAssetDrawIds = [...renderDiagnostics.furniture_asset_draw_ids].sort();
  const floor00FurnitureCompositionPass = projection.sceneMode !== "floor00"
    || projection.sceneId === "room:0"
      && renderDiagnostics.furniture_draw_attempts === catalogs.floor00.native_initial_furniture.length
      && renderDiagnostics.furniture_asset_draws === catalogs.floor00.native_initial_furniture.length
      && renderDiagnostics.furniture_subframe_draws === 3
      && renderDiagnostics.furniture_fallbacks === 0
      && JSON.stringify(floor00FurnitureActualDrawIds) === JSON.stringify(floor00FurnitureExpectedDrawIds)
      && JSON.stringify(floor00FurnitureAssetDrawIds) === JSON.stringify(floor00FurnitureExpectedDrawIds);
  const floor00StructuralExpectedDrawIds = catalogs.floor00.structural_facilities.map((facility) => `${facility.object_id}@${facility.anchor[0]}:${facility.anchor[1]}`).sort();
  const floor00StructuralActualDrawIds = [...renderDiagnostics.structural_facility_draw_ids].sort();
  const floor00StructuralTraceCount = renderDiagnostics.render_trace.filter((entry) =>
    entry.pass_id === "object-chip-primary" && entry.status === "approved_static_structural_facility_draw",
  ).length;
  const floor00StructuralPass = projection.sceneMode !== "floor00"
    || projection.sceneId === "room:0"
      && projection.structuralFacilities.length === catalogs.floor00.structural_facilities.length
      && renderDiagnostics.structural_facility_draws === catalogs.floor00.structural_facilities.length
      && floor00StructuralTraceCount === catalogs.floor00.structural_facilities.length
      && JSON.stringify(floor00StructuralActualDrawIds) === JSON.stringify(floor00StructuralExpectedDrawIds);
  const floor00FallbackTrace = renderDiagnostics.render_trace.filter((entry) => entry.status === "fallback_marker_draw");
  const floor00ActorAssetDrawCount = renderDiagnostics.render_trace.filter((entry) =>
    entry.pass_id === "avatar-primary"
      && (entry.status === "approved_actor_asset_draw" || entry.status === "approved_character_asset_draw"),
  ).length;
  const floor00Trace = renderDiagnostics.render_trace;
  const floor00TraceIndex = (predicate: (entry: RenderDiagnostics["render_trace"][number]) => boolean): number =>
    floor00Trace.findIndex(predicate);
  const floor00WallEntries = floor00Trace.filter((entry) =>
    entry.source_id.startsWith("scene:room:0/wall@") && entry.status === "approved_native_coordinate_composition",
  );
  const floor00DoorEntries = floor00Trace.filter((entry) =>
    entry.source_id === "scene:room:0/door" && entry.status === "approved_native_coordinate_composition",
  );
  const floor00ExpectedWallLayerIds = Object.entries(floor00WallAsset?.cellScope?.cells ?? {})
    .flatMap(([frameId, cells]) => cells.flatMap((cell) => {
      const layers = floor00WallAsset?.cellScope?.spriteLayers?.[frameId]
        ?? (floor00WallAsset?.cellScope?.spriteRecords?.[frameId] ? [floor00WallAsset.cellScope.spriteRecords[frameId]] : []);
      return layers.map((rawLayer, layerIndex) => {
        const layer = typeof rawLayer.layer === "number" ? rawLayer.layer : layerIndex;
        return `${floor00WallAsset?.id ?? "scene:room:0/wall"}@${frameId}:${cell[0]}:${cell[1]}:layer:${layer}`;
      });
    }))
    .sort();
  const floor00ActualWallLayerIds = floor00WallEntries.map((entry) => entry.source_id).sort();
  const floor00WallDoorOrderPass = projection.sceneMode !== "floor00"
    || projection.sceneId === "room:0"
      && floor00WallEntries.length === floor00ExpectedWallLayerIds.length
      && JSON.stringify(floor00ActualWallLayerIds) === JSON.stringify(floor00ExpectedWallLayerIds)
      && floor00DoorEntries.length === 1
      && floor00TraceIndex((entry) => entry.source_id.startsWith("scene:room:0/wall@") && entry.cell?.[1] === 7) > floor00TraceIndex((entry) => entry.source_id === "actor:staff:0" && entry.status === "approved_actor_asset_draw")
      && floor00TraceIndex((entry) => entry.source_id === "scene:room:0/door") < floor00TraceIndex((entry) => entry.source_id === "furniture:3" && entry.status === "approved_furniture_asset_draw")
      && floor00TraceIndex((entry) => entry.source_id === "furniture:3" && entry.status === "approved_furniture_asset_draw") < floor00TraceIndex((entry) => entry.source_id === "actor:staff:0" && entry.status === "approved_actor_asset_draw");
  const floor00TreeCell = projection.mapCells.find((cell) => cell.cell[0] === 3 && cell.cell[1] === 8);
  const floor00TreeId = floor00TreeCell?.assetId ? `mapcell:${projection.sceneId}:3:8` : null;
  const floor00TreePixels = floor00TreeId ? renderDiagnostics.final_visibility.pixel_counts[floor00TreeId] ?? 0 : 0;
  const floor00TreeVisibilityPass = projection.sceneMode !== "floor00"
    || projection.sceneId === "room:0" && Boolean(floor00TreeId) && floor00TreePixels > 0;
  const floor00BootstrapStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0"
      ? "blocked_by_evidence"
      : JSON.stringify(floor00ActualFurniture) === JSON.stringify(floor00ExpectedFurniture)
        && JSON.stringify(floor00ActualActors) === JSON.stringify(floor00ExpectedActors)
        && floor00DisplayActorPositionsPass
        ? "pass"
        : "blocked_by_evidence";
  const rawOverlayStatus: VisualGateCheckStatus = projection.sceneId !== "room:17" || !rawOverlayEnabled
    ? "not_applicable"
    : projection.rawOverlay?.status === "pass" && projection.rawOverlay.cells.length === 100
      ? "pass"
      : "blocked_by_evidence";
  const floor00CollisionPass = projection.sceneMode !== "floor00"
    ? true
    : projection.sceneId === "room:0"
      && catalogs.floor00DisplayPolicy.actors.every((actor) => {
        const placement = projection.cells.find((cell) => cell.cell[0] === actor.reserved_cell[0] && cell.cell[1] === actor.reserved_cell[1]);
        return placement?.passable === true && placement.collisionKind === "empty_walkable";
      })
      && projection.cells.find((cell) => cell.cell[0] === 9 && cell.cell[1] === 1)?.passable === false
      && projection.cells.find((cell) => cell.cell[0] === 8 && cell.cell[1] === 4)?.collisionKind === "entry_door";
  const floor00ActorFloorStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0"
      ? "blocked_by_evidence"
      : floor00ActorFloorPass
        ? "pass"
        : "blocked_by_evidence";
  const floor00ExtensionStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00ExtensionContractPass
      ? "blocked_by_evidence"
      : assets === null
        ? "pending"
        : floor00ExtensionTraceCount === projection.extensionWalls.length
          ? "pass"
          : "blocked_by_evidence";
  const floor00FurnitureStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00FurnitureCompositionPass
      ? assets === null ? "pending" : "blocked_by_evidence"
      : "pass";
  const floor00LifecycleStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : assets === null
      ? "pending"
      : floor00FallbackTrace.length === 0
        && floor00ActorAssetDrawCount === catalogs.floor00DisplayPolicy.actors.length
        ? "pass"
        : "blocked_by_evidence";
  const floor00VisualLayoutStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00VisualLayoutPass
      ? "blocked_by_evidence"
      : "pass";
  const floor00GlassContinuityStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00GlassGroupsPass || !floor00RemovedGlassPass || !floor00GlassStripPass
      ? "blocked_by_evidence"
      : "pass";
  const floor00WallAlignmentStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00WallAlignmentPass
      ? "blocked_by_evidence"
      : "pass";
  const floor00WallDoorStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00WallDoorOrderPass
      ? assets === null ? "pending" : "blocked_by_evidence"
      : "pass";
  const floor00TreeStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : projection.sceneId !== "room:0" || !floor00TreeVisibilityPass
      ? assets === null ? "pending" : "blocked_by_evidence"
      : "pass";
  const floor00FinalVisibilityStatus: VisualGateCheckStatus = projection.sceneMode !== "floor00"
    ? "not_applicable"
    : renderDiagnostics.final_visibility.status === "pass"
      ? "pass"
      : renderDiagnostics.final_visibility.status === "blocked"
        ? "blocked_by_evidence"
        : "pending";
  const checks: Record<string, VisualGateCheck> = {
    asset_bounds: {
      status: assets?.status === "ready" && outOfBounds.length === 0 ? "pass" : assets ? "pending" : "pending",
      details: `${checkedFrames}/${totalFrames} frame records checked against loaded/declared image bounds`,
    },
    required_assets_loaded: {
      status: assets?.status === "ready" && missingAssets.size === 0 ? "pass" : "pending",
      details: `${requiredRuntimeAssets.size - missingAssets.size}/${requiredRuntimeAssets.size} required runtime assets available`,
    },
    render_pass_order: {
      status: passes.length === 9 ? "pass" : "blocked_by_evidence",
      details: passes.map((pass) => pass.id).join(" → "),
    },
    drawable_metadata: {
      status: metadataMissing.length === 0 ? "pass" : "blocked_by_evidence",
      details: `${cards.length} drawable cards; missing=${metadataMissing.length}`,
    },
    furniture_render: {
      status: projection.sceneMode === "floor00" && assets === null
        ? "pending"
        : renderDiagnostics.furniture_fallbacks === 0
        && renderDiagnostics.furniture_asset_draws === renderDiagnostics.furniture_draw_attempts
        ? "pass"
        : "blocked_by_evidence",
      details: `${renderDiagnostics.furniture_asset_draws}/${renderDiagnostics.furniture_draw_attempts} furniture draws used approved assets; fallback=${renderDiagnostics.furniture_fallbacks}`,
    },
    floor00_extension_wall_composition: {
      status: floor00ExtensionStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 extension-wall projection"
        : `${projection.extensionWalls.length} approved floor00 paired extension pieces; trace=${floor00ExtensionTraceCount}; source crops are bounded to wall_01.png subframes`,
    },
    floor00_visual_layout: {
      status: floor00VisualLayoutStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 visual layout projection"
        : floor00VisualLayoutStatus === "pass"
          ? `approved ${floor00Layout?.contractId ?? "unknown"}; removed glass=${floor00Layout?.removedGlassCells.length ?? 0}; shifted wall=${floor00Layout?.backwardOffset.join(",") ?? "unknown"}`
          : "floor00 projection does not match the approved visual layout contract",
    },
    floor00_glass_continuity: {
      status: floor00GlassContinuityStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 glass continuity projection"
        : `${Object.values(floor00ActualGlassCellsByGroup).flat().length} final glass trigger cells; strip=${floor00GlassStripPass ? "continuous" : "not continuous"}; removed-zone overlap=${floor00RemovedGlassPass ? "none" : "present"}`,
    },
    floor00_wall_alignment: {
      status: floor00WallAlignmentStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 wall alignment projection"
        : `upper/left shared cell=${floor00SharedAlignmentCell?.join(",") ?? "missing"}; screen delta=${JSON.stringify(screenDelta(floor00UpperEdge[1] ?? [-1, -1], floor00LeftEdge[0] ?? [-2, -2]))}; layers=${floor00WallLayerOrderPass ? "0,1" : "invalid"}`,
    },
    floor00_furniture_composition: {
      status: floor00FurnitureStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 furniture projection"
        : `${renderDiagnostics.furniture_asset_draws}/${catalogs.floor00.native_initial_furniture.length} native furniture assets; subframes=${renderDiagnostics.furniture_subframe_draws}; fallback=${renderDiagnostics.furniture_fallbacks}`,
    },
    floor00_structural_facilities: {
      status: projection.sceneMode !== "floor00"
        ? "not_applicable"
        : assets === null
          ? "pending"
          : floor00StructuralPass ? "pass" : "blocked_by_evidence",
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 structural facility projection"
        : `${renderDiagnostics.structural_facility_draws}/${catalogs.floor00.structural_facilities.length} static furniture:0 facility pads; trace=${floor00StructuralTraceCount}`,
    },
    floor00_asset_lifecycle: {
      status: floor00LifecycleStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 asset lifecycle projection"
        : assets === null
          ? "floor00 scene held until approved PNG/SEB-derived assets are ready; no fallback room is drawn"
          : `fallback trace records=${floor00FallbackTrace.length}; approved actor asset draws=${floor00ActorAssetDrawCount}/${catalogs.floor00DisplayPolicy.actors.length}`,
    },
    native_placement: {
      status: nativePlacementPass ? "pass" : "blocked_by_evidence",
      details: `${projection.nativeInitialObjects.length} explicit native instances; raw slots remain non-native`,
    },
    native_composition: {
      status: nativeCompositionStatus,
      details: nativeCompositionReady ? "native wall/door coordinate composition is closed for this room" : "native wall/door composition is missing an approved asset or contract",
    },
    native_collision: {
      status: floor00CollisionPass ? "pass" : "blocked_by_evidence",
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 collision projection"
        : "empty reserved cells and entry door are traversable; native footprint/boundary cells are blocked",
    },
    floor00_actor_floor_containment: {
      status: floor00ActorFloorStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 actor placement projection"
        : floor00ActorFloorResults.map(({ actorId, result }) => `${actorId}:${result.status}:${result.reason}`).join("; "),
    },
    floor00_fallback_usage: {
      status: floor00LifecycleStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 fallback projection"
        : `${floor00FallbackTrace.length} fallback marker trace records; fallback ids=${renderDiagnostics.furniture_fallback_ids.join(",") || "none"}`,
    },
    floor00_wall_door_order: {
      status: floor00WallDoorStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 wall/door order projection"
        : `${floor00WallEntries.length} wall draws + ${floor00DoorEntries.length} door draw; rear wall/door precede furniture, foreground wall follows actors`,
    },
    floor00_tree_visibility: {
      status: floor00TreeStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 tree visibility projection"
        : `tree cell [3,8] retained ${floor00TreePixels} owner pixels after the underlay and object passes`,
    },
    floor00_final_pixel_visibility: {
      status: floor00FinalVisibilityStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 final-pixel visibility projection"
        : `${renderDiagnostics.final_visibility.visible_ids.length}/${renderDiagnostics.final_visibility.required_ids.length} required Floor00 drawables retain final canvas pixels; occluded=${renderDiagnostics.final_visibility.occluded_ids.length}`,
    },
    floor00_bootstrap: {
      status: floor00BootstrapStatus,
      details: projection.sceneMode !== "floor00"
        ? "not a Floor00 bootstrap projection"
        : `${floor00ActualFurniture.length}/${floor00ExpectedFurniture.length} native furniture instances; ${floor00ActualActors.length}/${floor00ExpectedActors.length} static display actors`,
    },
    raw_room_overlay: {
      status: rawOverlayStatus,
      details: projection.sceneId === "room:17" ? `${projection.rawOverlay?.cells.length ?? 0}/100 raw cells cross-checked` : "not a Room R diagnostic view",
    },
  };
  const hasPendingAssets = checks.asset_bounds.status === "pending"
    || checks.required_assets_loaded.status === "pending"
    || checks.floor00_asset_lifecycle.status === "pending"
    || checks.floor00_extension_wall_composition.status === "pending"
    || checks.floor00_furniture_composition.status === "pending"
    || checks.floor00_structural_facilities.status === "pending";
  const hasBlockedCheck = Object.values(checks).some((check) => check.status === "blocked_by_evidence");
  const gateStatus = hasPendingAssets
    ? "pending_assets"
    : hasBlockedCheck
      ? "blocked_by_evidence"
      : "pass";
  return {
    schema_version: "social-dev-visual-gate-snapshot-v1",
    semantic_status: "deterministic_visual_gate_snapshot",
    gate_status: gateStatus,
    scene_id: projection.sceneId,
    frame: state.frame,
    digest: state.digest,
    raw_overlay_enabled: rawOverlayEnabled,
    asset_status: assets?.status ?? "loading",
    render_passes: passes.map((pass) => pass.id),
    frame_checks: {
      total: totalFrames,
      checked_against_loaded_images: checkedFrames,
      missing_assets: [...missingAssets].sort(),
      out_of_bounds: outOfBounds,
    },
    render_diagnostics: renderDiagnostics,
    drawable_cards: cards,
    metadata_missing: metadataMissing,
    unresolved: projection.runtimeRoom.unresolved,
    checks,
  };
}
