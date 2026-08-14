import type { CameraCoordinateContract } from "../catalog/types";
import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { SimulationState } from "../core/types";
import { actorDisplayFrame, furnitureFrameForScene, type LoadedDisplayAssets } from "../assets/display-assets";
import {
  characterDisplayFrame,
  characterFrameRecordAssetId,
  getCachedCharacterImage,
} from "../assets/character-assets";
import { actorToCanvas, cellToCanvas, mapChipToCanvas, objectToCanvas, structuralFacilityToCanvas } from "../scene/coordinates";
import type { SceneProjection } from "../scene/projection";
import type { RoomRawOverlay } from "../scene/room-overlay";
import { createRenderPassPlan } from "./render-plan";
import { classifyNativeWallLayer, compareNativeCells, sortNativeDrawables } from "./native-render-order";
import {
  createVisibilityTracker,
  emptyFinalVisibilityDiagnostics,
  type VisibilityTracker,
} from "./visibility";

const ACTOR_COLORS = ["#66c4ff", "#ff9e76", "#a78bfa", "#72dfae", "#f7d26d"] as const;

function actorColor(sourceId: number): string {
  return ACTOR_COLORS[sourceId % ACTOR_COLORS.length];
}

function roundedRect(
  context: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  radius: number,
): void {
  context.beginPath();
  context.roundRect(x, y, width, height, radius);
}

function drawWorldBackground(context: CanvasRenderingContext2D, canvas: HTMLCanvasElement, assets: LoadedDisplayAssets | null): void {
  const background = assets?.ambientImages.get("day_back_00.png");
  if (!background) {
    return;
  }
  // The supplied 60x720 strip is a complete backdrop.  Anchor its bottom to
  // the canvas instead of inventing a second brown fill below a cropped strip.
  const nativeBackgroundY = canvas.height - (background.naturalHeight || background.height);
  context.save();
  context.imageSmoothingEnabled = false;
  for (let x = 0; x < canvas.width; x += 60) {
    context.drawImage(background, x, nativeBackgroundY, 60, background.naturalHeight || background.height);
  }
  context.restore();
}

function drawFloor00AssetLifecycleState(context: CanvasRenderingContext2D, canvas: HTMLCanvasElement): void {
  context.save();
  context.fillStyle = "rgba(13, 24, 37, 0.92)";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#dceeff";
  context.font = "600 22px sans-serif";
  context.textAlign = "center";
  context.fillText("Loading approved floor00 assets…", canvas.width / 2, canvas.height / 2 - 8);
  context.fillStyle = "#8ea8bf";
  context.font = "14px sans-serif";
  context.fillText("The native room is held until its SEB/PNG crops are ready.", canvas.width / 2, canvas.height / 2 + 22);
  context.restore();
}

function drawMapImages(
  context: CanvasRenderingContext2D,
  projection: SceneProjection,
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null,
  nativeFloorPass: boolean,
  diagnostics: MutableRenderDiagnostics,
  passId: "map-chip" | "map-floor",
  visibility?: VisibilityTracker | null,
): void {
  // Room.Draw walks native map rows from the far row toward the near row and
  // scans each row from right to left.  A generic x+y depth sort reverses
  // several same-depth cells and is the reason tree/edge pixels were unstable.
  const orderedCells = [...projection.mapCells].sort((left, right) => compareNativeCells(left, right));
  for (const cell of orderedCells) {
    if (cell.nativeFloorPass !== nativeFloorPass) {
      continue;
    }
    const image = cell.assetId ? assets?.mapImages.get(cell.assetId) : undefined;
    if (!image) {
      continue;
    }
    const point = mapChipToCanvas(cell.cell, camera);
    const imageHeight = image.naturalHeight || image.height;
    const imageWidth = image.naturalWidth || image.width;
    const sourceId = `mapcell:${projection.sceneId}:${cell.cell[0]}:${cell.cell[1]}`;
    context.save();
    context.imageSmoothingEnabled = false;
    context.drawImage(image, point.x, point.y + 39 - imageHeight);
    context.restore();
    visibility?.drawImage(sourceId, image, {
      destination_x: point.x,
      destination_y: point.y + 39 - imageHeight,
      width: imageWidth,
      height: imageHeight,
    });
    diagnostics.render_trace.push({
      pass_id: passId,
      native_method: passId === "map-chip" ? "MapChip.Draw" : "MapChip.DrawFloor",
      source_id: sourceId,
      asset_id: cell.assetId,
      cell: [cell.cell[0], cell.cell[1]],
      status: "approved_asset_draw",
    });
  }
}

interface NativeSpriteRecord {
  readonly layer?: number;
  readonly source_x: number;
  readonly source_y: number;
  readonly width: number;
  readonly height: number;
  readonly destination_x: number;
  readonly destination_y: number;
}

function nativeSpriteRecord(value: Record<string, unknown> | undefined): NativeSpriteRecord | null {
  if (!value) {
    return null;
  }
  const numeric = (key: keyof NativeSpriteRecord): number | null => {
    const candidate = value[key];
    return typeof candidate === "number" ? candidate : null;
  };
  const sourceX = numeric("source_x");
  const sourceY = numeric("source_y");
  const width = numeric("width");
  const height = numeric("height");
  const destinationX = numeric("destination_x");
  const destinationY = numeric("destination_y");
  if (sourceX === null || sourceY === null || width === null || height === null || destinationX === null || destinationY === null) {
    return null;
  }
  return {
    layer: typeof value.layer === "number" ? value.layer : undefined,
    source_x: sourceX,
    source_y: sourceY,
    width,
    height,
    destination_x: destinationX,
    destination_y: destinationY,
  };
}

function drawNativeSprite(
  context: CanvasRenderingContext2D,
  image: HTMLImageElement,
  point: { readonly x: number; readonly y: number },
  record: NativeSpriteRecord,
  visibility: VisibilityTracker | null | undefined,
  visibilityId: string,
): void {
  context.save();
  context.imageSmoothingEnabled = false;
  context.drawImage(
    image,
    record.source_x,
    record.source_y,
    record.width,
    record.height,
    point.x + record.destination_x,
    point.y + record.destination_y,
    record.width,
    record.height,
  );
  context.restore();
  visibility?.drawImage(visibilityId, image, {
    source_x: record.source_x,
    source_y: record.source_y,
    source_width: record.width,
    source_height: record.height,
    destination_x: point.x + record.destination_x,
    destination_y: point.y + record.destination_y,
    width: record.width,
    height: record.height,
  });
}

interface WorldDrawable {
  readonly depth: number;
  readonly layer: number;
  readonly key: string;
  readonly cell?: readonly [number, number];
  readonly draw: () => void;
}

export interface RenderDiagnostics {
  readonly furniture_draw_attempts: number;
  readonly furniture_asset_draws: number;
  readonly furniture_subframe_draws: number;
  readonly furniture_fallbacks: number;
  readonly structural_facility_draws: number;
  readonly structural_facility_draw_ids: string[];
  readonly furniture_draw_attempt_ids: string[];
  readonly furniture_asset_draw_ids: string[];
  readonly furniture_fallback_ids: string[];
  readonly final_visibility: import("./visibility").FinalVisibilityDiagnostics;
  readonly render_trace: readonly RenderTraceEntry[];
}

export interface RenderTraceEntry {
  readonly pass_id: string;
  readonly native_method: string;
  readonly source_id: string;
  readonly asset_id: string | null;
  readonly cell: readonly [number, number] | null;
  readonly status: string;
}

type MutableRenderDiagnostics = {
  furniture_draw_attempts: number;
  furniture_asset_draws: number;
  furniture_subframe_draws: number;
  furniture_fallbacks: number;
  structural_facility_draws: number;
  structural_facility_draw_ids: string[];
  furniture_draw_attempt_ids: string[];
  furniture_asset_draw_ids: string[];
  furniture_fallback_ids: string[];
  final_visibility: import("./visibility").FinalVisibilityDiagnostics;
  render_trace: RenderTraceEntry[];
};

function cellDepth(cell: readonly [number, number]): number {
  return cell[0] + cell[1];
}

function mapExtensionWallDrawables(
  context: CanvasRenderingContext2D,
  projection: SceneProjection,
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null,
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): WorldDrawable[] {
  const drawables: WorldDrawable[] = [];
  for (const wall of projection.extensionWalls) {
    const image = assets?.mapImages.get(wall.sourceAssetId);
    const record = nativeSpriteRecord(wall.spriteRecord);
    if (!image || !record) {
      continue;
    }
    drawables.push({
      depth: cellDepth(wall.cell),
      layer: wall.pieceIndex,
      key: `map-wall:${wall.compositionGroup}:${wall.cell[0]}:${wall.cell[1]}:${wall.pieceIndex}`,
      cell: wall.cell,
      draw: () => {
        const sourceId = `mapwall:${projection.sceneId}:${wall.cell[0]}:${wall.cell[1]}:${wall.compositionGroup}:${wall.pieceIndex}`;
        const origin = mapChipToCanvas(wall.cell, camera);
        drawNativeSprite(context, image, {
          x: origin.x + wall.pieceOffset.x,
          y: origin.y + wall.pieceOffset.y,
        }, record, visibility, sourceId);
        diagnostics.render_trace.push({
          pass_id: "map-extension-floor",
          native_method: "MapChip.DrawExtentionFloor",
          source_id: sourceId,
      asset_id: wall.sourceAssetId,
      cell: [wall.cell[0], wall.cell[1]],
      status: "approved_native_two_piece_extension_draw",
        });
      },
    });
  }
  return drawables;
}

function nativeSceneDrawables(
  context: CanvasRenderingContext2D,
  projection: SceneProjection,
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null,
  pass: "object-chip-primary" | "object-chip-wall" | "object-chip-late",
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
  foregroundWallCells: readonly (readonly [number, number])[] = [[8, 7], [8, 8]],
): WorldDrawable[] {
  const drawables: WorldDrawable[] = [];
  for (const asset of projection.sceneAssets) {
    if (asset.status !== "approved_native_coordinate_composition" || !asset.runtimeAssetId) {
      continue;
    }
    const image = assets?.images.get(asset.runtimeAssetId) ?? assets?.mapImages.get(asset.runtimeAssetId);
    if (!image) {
      continue;
    }
    if ((pass === "object-chip-wall" || pass === "object-chip-late") && asset.role === "wall") {
      const cellsByFrame = asset.cellScope?.cells;
      const compatibilityRecords = asset.cellScope?.spriteRecords;
      const layerRecords = asset.cellScope?.spriteLayers;
      if (!cellsByFrame || (!compatibilityRecords && !layerRecords)) {
        continue;
      }
      for (const [frameId, cells] of Object.entries(cellsByFrame)) {
        const rawRecords = layerRecords?.[frameId]
          ?? (compatibilityRecords?.[frameId] ? [compatibilityRecords[frameId]] : []);
        const records = rawRecords
          .map((rawRecord, index) => ({
            layer: typeof rawRecord.layer === "number" ? rawRecord.layer : index,
            record: nativeSpriteRecord(rawRecord),
          }))
          .filter((entry): entry is { readonly layer: number; readonly record: NativeSpriteRecord } => entry.record !== null)
          .sort((left, right) => left.layer - right.layer);
        if (records.length === 0) {
          continue;
        }
        for (const cell of cells) {
          const wallCell = [cell[0], cell[1]] as const;
          const foregroundWall = classifyNativeWallLayer(wallCell, foregroundWallCells) === "foreground";
          if (pass === "object-chip-wall" && foregroundWall) {
            continue;
          }
          if (pass === "object-chip-late" && !foregroundWall) {
            continue;
          }
          drawables.push({
            depth: cellDepth(wallCell),
            layer: foregroundWall ? 6 : 1,
            key: `wall:${frameId}:${wallCell[0]}:${wallCell[1]}:${records.map((entry) => entry.layer).join("-")}`,
            cell: wallCell,
            draw: () => {
              const origin = objectToCanvas(wallCell, camera);
              for (const entry of records) {
                const sourceId = `${asset.id}@${frameId}:${wallCell[0]}:${wallCell[1]}:layer:${entry.layer}`;
                drawNativeSprite(context, image, origin, entry.record, visibility, sourceId);
                diagnostics.render_trace.push({
                  pass_id: pass,
                  native_method: "ObjChip.DrawWall",
                  source_id: sourceId,
                  asset_id: asset.runtimeAssetId ?? null,
                  cell: [wallCell[0], wallCell[1]],
                  status: "approved_native_coordinate_composition",
                });
              }
            },
          });
        }
      }
    } else if (pass === "object-chip-wall" && asset.role === "door" && asset.cell) {
      const record = nativeSpriteRecord(asset.nativeCoordinate?.spriteRecord);
      if (record) {
        const doorCell = [asset.cell[0], asset.cell[1]] as const;
        drawables.push({
          depth: cellDepth(doorCell),
          layer: 6,
          key: `door:${doorCell[0]}:${doorCell[1]}`,
          cell: doorCell,
          draw: () => {
            drawNativeSprite(context, image, objectToCanvas(doorCell, camera), record, visibility, asset.id);
            diagnostics.render_trace.push({
              pass_id: "object-chip-wall",
              native_method: "ObjChip.DrawWall / Door",
              source_id: asset.id,
              asset_id: asset.runtimeAssetId ?? null,
              cell: [doorCell[0], doorCell[1]],
              status: "approved_native_coordinate_composition",
            });
          },
        });
      }
    }
  }
  return drawables;
}

function drawObjectFallback(
  context: CanvasRenderingContext2D,
  object: { readonly id: string },
  point: { readonly x: number; readonly y: number },
): void {
  const isDoor = object.id === "furniture:1";
  context.fillStyle = isDoor ? "rgba(238, 113, 147, 0.32)" : "rgba(237, 171, 88, 0.25)";
  context.strokeStyle = isDoor ? "#f0839d" : "#e7ad5f";
  context.lineWidth = 2;
  context.fillRect(point.x - (isDoor ? 11 : 30), point.y - (isDoor ? 22 : 35), isDoor ? 22 : 60, isDoor ? 28 : 40);
  context.strokeRect(point.x - (isDoor ? 11 : 30), point.y - (isDoor ? 22 : 35), isDoor ? 22 : 60, isDoor ? 28 : 40);
}

function drawStructuralFacilityAtAnchor(
  context: CanvasRenderingContext2D,
  item: SceneProjection["structuralFacilities"][number],
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null,
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): void {
  const image = assets?.images.get(item.imageAssetId);
  const record = nativeSpriteRecord(item.frame);
  if (!image || !record) {
    diagnostics.render_trace.push({
      pass_id: "object-chip-primary",
      native_method: "ObjChip.Draw",
      source_id: item.id,
      asset_id: item.imageAssetId,
      cell: [item.anchor[0], item.anchor[1]],
      status: "blocked_structural_facility_draw",
    });
    return;
  }
  drawNativeSprite(context, image, structuralFacilityToCanvas(item.mapAnchor, camera), record, visibility, item.id);
  diagnostics.structural_facility_draws += 1;
  diagnostics.structural_facility_draw_ids.push(item.id);
  diagnostics.render_trace.push({
    pass_id: "object-chip-primary",
    native_method: "ObjChip.Draw",
    source_id: item.id,
    asset_id: item.imageAssetId,
    cell: [item.anchor[0], item.anchor[1]],
    status: "approved_static_structural_facility_draw",
  });
}

function drawFurnitureAtCell(
  context: CanvasRenderingContext2D,
  item: {
    readonly id: string;
    readonly label: string;
    readonly cell: readonly [number, number];
  },
  sceneMode: SceneProjection["sceneMode"],
  camera: CameraCoordinateContract,
  frameNumber: number,
  assets: LoadedDisplayAssets | null,
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): void {
  const point = objectToCanvas(item.cell, camera);
  diagnostics.furniture_draw_attempts += 1;
  diagnostics.furniture_draw_attempt_ids.push(item.id);
  const furnitureFrame = furnitureFrameForScene(item.id, frameNumber, sceneMode);
  const furnitureImage = furnitureFrame?.imageAssetId ? assets?.images.get(furnitureFrame.imageAssetId) : undefined;
  const subImage = furnitureFrame?.subImageAssetId ? assets?.images.get(furnitureFrame.subImageAssetId) : undefined;
  const frameFitsImage = (frame: { readonly source_x: number; readonly source_y: number; readonly width: number; readonly height: number }, image: HTMLImageElement | undefined): boolean =>
    Boolean(image && frame.source_x >= 0 && frame.source_y >= 0 && frame.width > 0 && frame.height > 0
      && frame.source_x + frame.width <= (image.naturalWidth || image.width)
      && frame.source_y + frame.height <= (image.naturalHeight || image.height));
  const mainFrameReady = Boolean(
      furnitureFrame
      && furnitureImage
      && (furnitureFrame.frame.runtime_status ?? furnitureFrame.frame.source_status)?.startsWith("pass")
      && frameFitsImage(furnitureFrame.frame, furnitureImage),
  );
  const subFrameReady = Boolean(
    furnitureFrame?.subFrame
      && subImage
      && (furnitureFrame.subFrame.runtime_status ?? furnitureFrame.subFrame.source_status)?.startsWith("pass")
      && frameFitsImage(furnitureFrame.subFrame, subImage),
  );

  if (furnitureFrame && mainFrameReady && furnitureImage) {
    const frame = furnitureFrame.frame;
    const visibilityId = `${item.id}@${item.cell[0]}:${item.cell[1]}`;
    context.save();
    context.imageSmoothingEnabled = false;
    context.drawImage(
      furnitureImage,
      frame.source_x,
      frame.source_y,
      frame.width,
      frame.height,
      point.x + frame.destination_x,
      point.y + frame.destination_y,
      frame.width,
      frame.height,
    );
    diagnostics.furniture_asset_draws += 1;
    diagnostics.furniture_asset_draw_ids.push(item.id);
    visibility?.drawImage(visibilityId, furnitureImage, {
      source_x: frame.source_x,
      source_y: frame.source_y,
      source_width: frame.width,
      source_height: frame.height,
      destination_x: point.x + frame.destination_x,
      destination_y: point.y + frame.destination_y,
      width: frame.width,
      height: frame.height,
    });
    diagnostics.render_trace.push({
      pass_id: "object-chip-primary",
      native_method: "ObjChip.Draw",
      source_id: item.id,
      asset_id: furnitureFrame.imageAssetId ?? null,
      cell: [item.cell[0], item.cell[1]],
      status: "approved_furniture_asset_draw",
    });
    if (furnitureFrame.subFrame && subFrameReady && subImage) {
      const subFrame = furnitureFrame.subFrame;
      context.drawImage(
        subImage,
        subFrame.source_x,
        subFrame.source_y,
        subFrame.width,
        subFrame.height,
        point.x + subFrame.destination_x,
        point.y + subFrame.destination_y,
        subFrame.width,
        subFrame.height,
      );
      visibility?.drawImage(visibilityId, subImage, {
        source_x: subFrame.source_x,
        source_y: subFrame.source_y,
        source_width: subFrame.width,
        source_height: subFrame.height,
        destination_x: point.x + subFrame.destination_x,
        destination_y: point.y + subFrame.destination_y,
        width: subFrame.width,
        height: subFrame.height,
      });
      diagnostics.furniture_subframe_draws += 1;
    }
    context.restore();
  } else {
    diagnostics.furniture_fallbacks += 1;
    diagnostics.furniture_fallback_ids.push(item.id);
    diagnostics.render_trace.push({
      pass_id: "object-chip-primary",
      native_method: "ObjChip.Draw",
      source_id: item.id,
      asset_id: furnitureFrame?.imageAssetId ?? null,
      cell: [item.cell[0], item.cell[1]],
      status: "fallback_marker_draw",
    });
    drawObjectFallback(context, item, point);
    visibility?.markRect(
      `${item.id}@${item.cell[0]}:${item.cell[1]}`,
      point.x - (item.id === "furniture:1" ? 11 : 30),
      point.y - (item.id === "furniture:1" ? 22 : 35),
      item.id === "furniture:1" ? 22 : 60,
      item.id === "furniture:1" ? 28 : 40,
    );
  }
}

function sortedDrawables(drawables: readonly WorldDrawable[]): WorldDrawable[] {
  const withCells = drawables.every((drawable) => Boolean(drawable.cell));
  if (withCells) {
    return sortNativeDrawables(drawables as (WorldDrawable & { readonly cell: readonly [number, number] })[]);
  }
  return [...drawables].sort((left, right) => {
    if (left.cell && right.cell) {
      return compareNativeCells({ cell: left.cell }, { cell: right.cell })
        || left.layer - right.layer
        || left.key.localeCompare(right.key);
    }
    return left.depth - right.depth || left.layer - right.layer || left.key.localeCompare(right.key);
  });
}

function objectChipPrimaryDrawables(
  context: CanvasRenderingContext2D,
  projection: SceneProjection,
  camera: CameraCoordinateContract,
  frameNumber: number,
  assets: LoadedDisplayAssets | null,
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): WorldDrawable[] {
  const drawables: WorldDrawable[] = [];
  for (const facility of projection.structuralFacilities) {
    const cell = [facility.anchor[0], facility.anchor[1]] as const;
    drawables.push({
      depth: cellDepth(cell),
      layer: 2,
      key: `structural:${facility.id}`,
      cell,
      draw: () => drawStructuralFacilityAtAnchor(context, facility, camera, assets, diagnostics, visibility),
    });
  }

  for (const object of projection.nativeInitialObjects) {
    const cell = [object.cell[0], object.cell[1]] as const;
    drawables.push({
      depth: cellDepth(cell),
      layer: 2,
      key: `native:${object.id}`,
      cell,
      draw: () => drawFurnitureAtCell(
        context,
        { id: object.objectId, label: object.label, cell },
        projection.sceneMode,
        camera,
        frameNumber,
        assets,
        diagnostics,
        visibility,
      ),
    });
  }

  return sortedDrawables(drawables);
}

function objectChipWallDrawables(
  context: CanvasRenderingContext2D,
  projection: SceneProjection,
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null,
  diagnostics: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
  foregroundWallCells: readonly (readonly [number, number])[] = [[8, 7], [8, 8]],
): WorldDrawable[] {
  return sortedDrawables(nativeSceneDrawables(
    context,
    projection,
    camera,
    assets,
    "object-chip-wall",
    diagnostics,
    visibility,
    foregroundWallCells,
  ));
}

export function resolveForegroundWallCells(
  projection: SceneProjection,
  catalogs?: RuntimeCatalogs,
): readonly (readonly [number, number])[] {
  const nativeForegroundCells = catalogs?.floor00.render_composition.foreground_wall_cells ?? [[8, 7], [8, 8]] as const;
  if (projection.sceneMode !== "floor00" || projection.sceneId !== "room:0" || !projection.presentationLayout) {
    return nativeForegroundCells.map(([x, y]) => [x, y] as const);
  }
  const [offsetX, offsetY] = projection.presentationLayout.backwardOffset;
  return nativeForegroundCells.map(([x, y]) => [x + offsetX, y + offsetY] as const);
}

function avatarDrawables(
  context: CanvasRenderingContext2D,
  camera: CameraCoordinateContract,
  state: SimulationState,
  assets: LoadedDisplayAssets | null,
  catalogs?: RuntimeCatalogs,
  diagnostics?: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): WorldDrawable[] {
  return sortedDrawables(Object.values(state.actors).sort((left, right) => left.id.localeCompare(right.id)).map((actor) => ({
    depth: cellDepth([actor.cell[0], actor.cell[1]]),
    layer: 0,
    key: `actor:${actor.id}`,
    cell: [actor.cell[0], actor.cell[1]] as const,
    draw: () => drawActor(context, actor, camera, state.selectedActorId === actor.id, assets, catalogs, diagnostics, visibility),
  })));
}

function drawRoute(context: CanvasRenderingContext2D, state: SimulationState, camera: CameraCoordinateContract): void {
  const movingActor = Object.values(state.actors).find((actor) => actor.lifecycle === "move" || actor.route.length > 0);
  if (!movingActor || movingActor.route.length < 2) {
    return;
  }
  context.save();
  context.setLineDash([4, 5]);
  context.lineWidth = 2;
  context.strokeStyle = "rgba(115, 204, 255, 0.72)";
  context.beginPath();
  movingActor.route.forEach((cell, index) => {
    const point = cellToCanvas(cell, camera);
    if (index === 0) {
      context.moveTo(point.x, point.y);
    } else {
      context.lineTo(point.x, point.y);
    }
  });
  context.stroke();
  context.restore();
}

function drawActor(
  context: CanvasRenderingContext2D,
  actor: SimulationState["actors"][string],
  camera: CameraCoordinateContract,
  selected: boolean,
  assets: LoadedDisplayAssets | null,
  catalogs?: RuntimeCatalogs,
  diagnostics?: MutableRenderDiagnostics,
  visibility?: VisibilityTracker | null,
): void {
  const point = actorToCanvas(actor.position, camera);
  const x = point.x;
  const y = point.y;
  const color = actorColor(actor.sourceId);

  context.fillStyle = "rgba(0, 0, 0, 0.34)";
  context.beginPath();
  context.ellipse(x, y + 16, 15, 5, 0, 0, Math.PI * 2);
  context.fill();

  const displayFrame = actorDisplayFrame(actor.sourceId, actor.animation.mode, actor.animation.selectorId, actor.animation.frame);
  const actorImage = displayFrame ? assets?.images.get(displayFrame.imageAssetId) : undefined;
  const genericFrame = !displayFrame || !actorImage
    ? catalogs && characterDisplayFrame(catalogs, actor.id, actor.animation.mode, actor.facing, actor.animation.frame)
    : null;
  const genericImage = genericFrame ? getCachedCharacterImage(genericFrame.imageAssetId) : undefined;

  if (selected) {
    context.strokeStyle = "#ffffff";
    context.lineWidth = 2;
    context.beginPath();
    context.arc(x, y - 14, 18, 0, Math.PI * 2);
    context.stroke();
  }

  let actorStatus = "fallback_actor_marker";
  let actorAssetId: string | null = null;
  if (displayFrame && actorImage && displayFrame.frame.source_status === "pass") {
    const frame = displayFrame.frame;
    context.save();
    context.imageSmoothingEnabled = false;
    context.drawImage(
      actorImage,
      frame.source_x,
      frame.source_y,
      frame.width,
      frame.height,
      x + frame.destination_x,
      y + frame.destination_y,
      frame.width,
      frame.height,
    );
    context.restore();
    actorAssetId = displayFrame.imageAssetId;
    actorStatus = "approved_actor_asset_draw";
    visibility?.drawImage(actor.id, actorImage, {
      source_x: frame.source_x,
      source_y: frame.source_y,
      source_width: frame.width,
      source_height: frame.height,
      destination_x: x + frame.destination_x,
      destination_y: y + frame.destination_y,
      width: frame.width,
      height: frame.height,
    });
  } else if (genericFrame && genericImage) {
    context.save();
    context.imageSmoothingEnabled = false;
    for (const frame of genericFrame.records) {
      const assetId = characterFrameRecordAssetId(frame, genericFrame.imageAssetId);
      const image = assetId ? getCachedCharacterImage(assetId) : undefined;
      if (!image) {
        continue;
      }
      context.drawImage(
        image,
        frame.source_x,
        frame.source_y,
        frame.width,
        frame.height,
        x + frame.destination_x,
        y + frame.destination_y,
        frame.width,
        frame.height,
      );
      visibility?.drawImage(actor.id, image, {
        source_x: frame.source_x,
        source_y: frame.source_y,
        source_width: frame.width,
        source_height: frame.height,
        destination_x: x + frame.destination_x,
        destination_y: y + frame.destination_y,
        width: frame.width,
        height: frame.height,
      });
    }
    context.restore();
    actorAssetId = genericFrame.imageAssetId;
    actorStatus = "approved_character_asset_draw";
  } else {
    context.fillStyle = color;
    context.beginPath();
    context.arc(x, y, 12, 0, Math.PI * 2);
    context.fill();
    context.fillStyle = "rgba(255, 255, 255, 0.56)";
    context.beginPath();
    context.arc(x - 4, y - 4, 4, 0, Math.PI * 2);
    context.fill();
    visibility?.markRect(actor.id, x - 12, y - 12, 24, 24);
  }

  diagnostics?.render_trace.push({
    pass_id: "avatar-primary",
    native_method: "Avatar.Draw",
    source_id: actor.id,
    asset_id: actorAssetId,
    cell: [actor.cell[0], actor.cell[1]],
    status: actorStatus,
  });

  if (diagnostics && actorStatus === "fallback_actor_marker") {
    diagnostics.render_trace.push({
      pass_id: "avatar-primary",
      native_method: "Avatar.Draw",
      source_id: `${actor.id}:fallback`,
      asset_id: null,
      cell: [actor.cell[0], actor.cell[1]],
      status: "fallback_marker_draw",
    });
  }

  if (actor.lifecycle === "talk") {
    const bubbleWidth = 122;
    const bubbleX = x + 20;
    const bubbleY = y - 60;
    roundedRect(context, bubbleX, bubbleY, bubbleWidth, 28, 8);
    context.fillStyle = "rgba(245, 250, 255, 0.95)";
    context.fill();
    context.fillStyle = "#1a2738";
    context.font = "10px ui-sans-serif, system-ui, sans-serif";
    context.textAlign = "left";
    context.textBaseline = "middle";
    context.fillText(`talk frame ${actor.talkFrame ?? 0}`, bubbleX + 10, bubbleY + 14);
  }
}

function rawOverlayColor(rawType: number): string {
  switch (rawType) {
    case 1:
      return "rgba(104, 194, 255, 0.18)";
    case 2:
      return "rgba(255, 190, 87, 0.24)";
    case 5:
      return "rgba(244, 115, 158, 0.34)";
    case 6:
      return "rgba(164, 177, 199, 0.2)";
    default:
      return "rgba(129, 150, 176, 0.12)";
  }
}

function drawRawRoomOverlay(
  context: CanvasRenderingContext2D,
  overlay: RoomRawOverlay,
  camera: CameraCoordinateContract,
): void {
  context.save();
  context.lineWidth = 1;
  context.font = "8px ui-monospace, SFMono-Regular, Consolas, monospace";
  context.textAlign = "center";
  context.textBaseline = "middle";
  for (const cell of overlay.cells) {
    const point = objectToCanvas(cell.cell, camera);
    const halfWidth = 19;
    const halfHeight = 10;
    context.beginPath();
    context.moveTo(point.x, point.y - halfHeight);
    context.lineTo(point.x + halfWidth, point.y);
    context.lineTo(point.x, point.y + halfHeight);
    context.lineTo(point.x - halfWidth, point.y);
    context.closePath();
    context.fillStyle = rawOverlayColor(cell.rawType);
    context.fill();
    context.strokeStyle = cell.rawType === 5 ? "#ffb2c7" : "rgba(201, 225, 255, 0.62)";
    context.stroke();
    context.fillStyle = "#f5f8fd";
    context.fillText(`${cell.cell[0]},${cell.cell[1]} t${cell.rawType} d${cell.rawDirection}`, point.x, point.y - 16);
  }
  context.fillStyle = "rgba(9, 14, 24, 0.84)";
  context.fillRect(18, 18, 216, 22);
  context.fillStyle = "#ffcf72";
  context.textAlign = "left";
  context.fillText("ROOM R RAW OVERLAY · 10×10 · diagnostic only", 26, 29);
  context.restore();
}

function floor00RequiredVisibilityIds(projection: SceneProjection, state: SimulationState): string[] {
  if (projection.sceneMode !== "floor00" || projection.sceneId !== "room:0") {
    return [];
  }
  const required: string[] = [];
  for (const facility of projection.structuralFacilities) {
    required.push(facility.id);
  }
  for (const object of projection.nativeInitialObjects) {
    required.push(`${object.objectId}@${object.cell[0]}:${object.cell[1]}`);
  }
  required.push(...Object.keys(state.actors).sort());
  const tree = projection.mapCells.find((cell) => cell.cell[0] === 3 && cell.cell[1] === 8);
  if (tree) {
    required.push(`mapcell:${projection.sceneId}:3:8`);
  }
  for (const wall of projection.extensionWalls) {
    required.push(`mapwall:${projection.sceneId}:${wall.cell[0]}:${wall.cell[1]}:${wall.compositionGroup}:${wall.pieceIndex}`);
  }
  const wallAsset = projection.sceneAssets.find((asset) => asset.role === "wall");
  for (const [frameId, cells] of Object.entries(wallAsset?.cellScope?.cells ?? {})) {
    const rawLayers = wallAsset?.cellScope?.spriteLayers?.[frameId]
      ?? (wallAsset?.cellScope?.spriteRecords?.[frameId] ? [wallAsset.cellScope.spriteRecords[frameId]] : []);
    for (const cell of cells) {
      for (const [layerIndex, rawLayer] of rawLayers.entries()) {
        const layer = typeof rawLayer.layer === "number" ? rawLayer.layer : layerIndex;
        required.push(`${wallAsset?.id ?? "scene:room:0/wall"}@${frameId}:${cell[0]}:${cell[1]}:layer:${layer}`);
      }
    }
  }
  const door = projection.sceneAssets.find((asset) => asset.role === "door");
  if (door) {
    required.push(door.id);
  }
  return [...new Set(required)];
}

export function renderScene(
  canvas: HTMLCanvasElement,
  projection: SceneProjection,
  state: SimulationState,
  camera: CameraCoordinateContract,
  assets: LoadedDisplayAssets | null = null,
  rawOverlayEnabled = false,
  catalogs?: RuntimeCatalogs,
): RenderDiagnostics {
  const context = canvas.getContext("2d");
  if (!context) {
    throw new Error("Canvas 2D context is unavailable");
  }
  context.clearRect(0, 0, canvas.width, canvas.height);
  const diagnostics: MutableRenderDiagnostics = {
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
  };
  const visibility = createVisibilityTracker(canvas);
  const foregroundWallCells = resolveForegroundWallCells(projection, catalogs);
  const gradient = context.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#0e1825");
  gradient.addColorStop(1, "#0a111b");
  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);

  if (projection.sceneMode === "floor00" && assets === null) {
    drawFloor00AssetLifecycleState(context, canvas);
    diagnostics.render_trace.push({
      pass_id: "asset-lifecycle",
      native_method: "approved_runtime_asset_loader",
      source_id: `lifecycle:${projection.sceneId}`,
      asset_id: null,
      cell: null,
      status: "waiting_for_approved_assets",
    });
    canvas.dataset.renderDiagnostics = JSON.stringify(diagnostics);
    return diagnostics;
  }

  drawWorldBackground(context, canvas, assets);
  const passPlan = createRenderPassPlan(projection);
  for (const pass of passPlan) {
    diagnostics.render_trace.push({
      pass_id: pass.id,
      native_method: pass.layerRole,
      source_id: `pass:${projection.sceneId}:${pass.id}`,
      asset_id: null,
      cell: null,
      status: "pass_enter",
    });
    let drawables: readonly WorldDrawable[] = [];
    switch (pass.id) {
      case "map-extension-floor":
        // The native scene contract treats MapChip/floor pixels as one opaque
        // underlay for this comparison view. Commit both map layers before
        // extension/object pixels so the floor cannot erase the room content.
        drawMapImages(context, projection, camera, assets, false, diagnostics, "map-chip", visibility);
        drawMapImages(context, projection, camera, assets, true, diagnostics, "map-floor", visibility);
        // Extension walls sit above the underlay but below room objects.
        drawables = sortedDrawables(mapExtensionWallDrawables(context, projection, camera, assets, diagnostics, visibility));
        break;
      case "map-chip":
        break;
      case "object-chip-primary":
        // ObjChip.DrawWall is a per-cell rear layer.  Compose it with the
        // primary object list here so a wall at [8,5]/[8,6] stays behind the
        // native garbage can/printer instead of erasing their pixels later.
        drawables = sortedDrawables([
          ...objectChipWallDrawables(context, projection, camera, assets, diagnostics, visibility, foregroundWallCells),
          ...objectChipPrimaryDrawables(context, projection, camera, state.frame, assets, diagnostics, visibility),
        ]);
        break;
      case "object-chip-wall":
        break;
      case "avatar-primary":
        drawRoute(context, state, camera);
        drawables = avatarDrawables(context, camera, state, assets, catalogs, diagnostics, visibility);
        break;
      case "avatar-secondary":
      case "object-chip-late-preview":
        break;
      case "object-chip-late":
        drawables = sortedDrawables(nativeSceneDrawables(
          context,
          projection,
          camera,
          assets,
          "object-chip-late",
          diagnostics,
          visibility,
          foregroundWallCells,
        ));
        break;
      case "map-floor":
        break;
    }
    for (const drawable of drawables) {
      drawable.draw();
    }
  }
  if (rawOverlayEnabled && projection.rawOverlay) {
    drawRawRoomOverlay(context, projection.rawOverlay, camera);
  }
  diagnostics.final_visibility = visibility?.finish(floor00RequiredVisibilityIds(projection, state))
    ?? emptyFinalVisibilityDiagnostics();
  canvas.dataset.renderDiagnostics = JSON.stringify(diagnostics);
  return diagnostics;
}
