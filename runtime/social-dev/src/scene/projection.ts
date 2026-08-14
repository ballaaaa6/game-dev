import type { RuntimeCatalogs } from "../catalog/load-contracts";
import { resolveFloorRender, type FloorRenderResolution } from "../catalog/floor-resolution";
import type { ObjectRecord, Phase3CRenderPlacement, RawObjectType } from "../catalog/types";
import type { Cell } from "../core/types";
import type { NativeCollisionKind } from "./native-collision";
import type { ExtensionWallPiece } from "./extension-wall";
import { resolveRoomScene, type ResolvedRoomScene, type RoomSceneResolveOptions, type SceneProjectionMode } from "./room-resolver";
import { buildRoomRawOverlay, type RoomRawOverlay } from "./room-overlay";

export interface SceneCellProjection {
  readonly cell: Cell;
  readonly rawType: number;
  readonly rawDirection: number;
  readonly directionLabel: string;
  readonly directionVector: readonly [number, number];
  readonly reverseDirection: number;
  readonly passable: boolean;
  readonly collisionKind: NativeCollisionKind;
  readonly rawTypeLabel: string;
}

export interface SceneMapCellProjection {
  readonly cell: Cell;
  readonly rawIndex: number;
  readonly selectorId: number;
  readonly filename: string | null;
  readonly assetId: string | null;
  readonly meaning: string;
  readonly nativeFloorPass: boolean;
}

export type SceneMapWallProjection = ExtensionWallPiece;

export interface VerifiedNativeInitialObjectProjection {
  readonly id: string;
  readonly objectId: string;
  readonly furnitureDataId: number;
  readonly cell: Cell;
  readonly label: string;
  readonly rawType: number;
  readonly nativeStatus: string;
  readonly selectorFlag: string;
  readonly scanOrder: number;
}

export interface VerifiedStructuralFacilityProjection {
  readonly id: string;
  readonly objectId: string;
  readonly label: string;
  readonly anchor: Cell;
  readonly mapAnchor: Cell;
  readonly rawType: number;
  readonly footprintCells: readonly Cell[];
  readonly sebSelectorId: number;
  readonly imageAssetId: string;
  readonly frame: Record<string, unknown>;
  readonly renderStatus: string;
}

export interface SceneAssetProjection {
  readonly id: string;
  readonly role: Phase3CRenderPlacement["role"];
  readonly cell?: Cell;
  readonly rawSelectorId?: number;
  readonly runtimeAssetId?: string;
  readonly filename?: string;
  readonly status: string;
  readonly sourceResolutionStatus?: string;
  readonly runtimeResolutionStatus?: string;
  readonly floorResolutionMode?: string;
  readonly metadataFilename?: string;
  readonly cellScope?: {
    readonly width: number;
    readonly height: number;
    readonly mode: string;
    readonly cells?: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly anchorFormula?: Readonly<Record<string, string>>;
    readonly spriteRecords?: Readonly<Record<string, Record<string, unknown>>>;
    readonly spriteLayers?: Readonly<Record<string, readonly Record<string, unknown>[]>>;
  };
  readonly nativeCoordinate?: {
    readonly anchor: { readonly x: number; readonly y: number };
    readonly spriteRecord: Record<string, unknown>;
  };
}

export interface SceneProjection {
  readonly sceneId: string;
  readonly sceneMode: SceneProjectionMode;
  readonly name: string;
  readonly gridWidth: number;
  readonly gridHeight: number;
  readonly cells: readonly SceneCellProjection[];
  readonly mapWidth: number;
  readonly mapHeight: number;
  readonly nativeFloorValue: number;
  readonly roomContext: ResolvedRoomScene["context"];
  readonly environmentScope: ResolvedRoomScene["environmentScope"];
  readonly topologyStatus: string;
  readonly extensionWallStatus: string;
  readonly mapCells: readonly SceneMapCellProjection[];
  readonly floorResolutionMode: string;
  readonly floorMetadataFilename: string;
  readonly extensionWalls: readonly SceneMapWallProjection[];
  readonly structuralFacilities: readonly VerifiedStructuralFacilityProjection[];
  readonly nativeInitialObjects: readonly VerifiedNativeInitialObjectProjection[];
  readonly sceneAssets: readonly SceneAssetProjection[];
  readonly presentationLayout: ResolvedRoomScene["presentationLayout"];
  readonly drawPasses: readonly string[];
  readonly catalogObjectNames: readonly string[];
  readonly runtimeRoom: ResolvedRoomScene;
  readonly rawOverlay: RoomRawOverlay | null;
}

function rawTypeLabel(rawTypes: readonly RawObjectType[], rawType: number): string {
  return rawTypes.find((candidate) => candidate.raw_type === rawType)?.source_constant?.name ?? `RAW_TYPE_${rawType}`;
}

function objectById(catalogs: RuntimeCatalogs, id: string): ObjectRecord {
  const object = catalogs.objects.objects.find((candidate) => candidate.id === id);
  if (!object) {
    throw new Error(`ObjectCatalog is missing ${id}`);
  }
  return object;
}

function verifiedStructuralFacility(
  catalogs: RuntimeCatalogs,
  facility: RuntimeCatalogs["floor00"]["structural_facilities"][number],
): VerifiedStructuralFacilityProjection {
  const object = objectById(catalogs, facility.object_id);
  if (facility.seb_selector_id !== object.selectors.seb_?.id) {
    throw new Error(`Structural facility ${facility.object_id} has a selector drift`);
  }
  return {
    id: `${facility.object_id}@${facility.anchor[0]}:${facility.anchor[1]}`,
    objectId: facility.object_id,
    label: object.name.values.English,
    anchor: [facility.anchor[0], facility.anchor[1]],
    mapAnchor: [facility.map_anchor[0], facility.map_anchor[1]],
    rawType: facility.raw_type,
    footprintCells: facility.footprint_cells.map((cell) => [cell[0], cell[1]]),
    sebSelectorId: facility.seb_selector_id,
    imageAssetId: facility.image_asset_id,
    frame: { ...facility.sprite_record },
    renderStatus: "approved_static_structural_facility",
  };
}

function placementCell(placement: Phase3CRenderPlacement): Cell | null {
  if (!Array.isArray(placement.cell) || placement.cell.length !== 2) {
    return null;
  }
  if (!placement.cell.every((value) => typeof value === "number")) {
    return null;
  }
  return [placement.cell[0], placement.cell[1]] as const;
}

function sceneAssetProjection(
  placement: Phase3CRenderPlacement,
  floorRender?: FloorRenderResolution,
): SceneAssetProjection {
  const isFloor = placement.role === "floor" && floorRender !== undefined;
  return {
    id: placement.id,
    role: placement.role,
    cell: placementCell(placement) ?? undefined,
    rawSelectorId: placement.raw_selector_id,
    runtimeAssetId: isFloor ? floorRender.assetId : placement.runtime_asset_id,
    filename: isFloor ? floorRender.filename : placement.filename,
    status: isFloor ? "approved_explicit_floor05_render_with_floor09_selector_data" : placement.status,
    sourceResolutionStatus: placement.source_resolution_status,
    runtimeResolutionStatus: isFloor ? floorRender.resolutionStatus : placement.runtime_resolution_status,
    floorResolutionMode: isFloor ? floorRender.resolutionMode : undefined,
    metadataFilename: isFloor ? floorRender.metadataFilename : undefined,
    cellScope: placement.cell_scope
      ? {
          width: placement.cell_scope.width,
          height: placement.cell_scope.height,
          mode: placement.cell_scope.mode,
          cells: placement.cell_scope.cells,
          anchorFormula: placement.cell_scope.anchor_formula,
          spriteRecords: placement.cell_scope.sprite_records,
          spriteLayers: placement.cell_scope.sprite_layers,
        }
      : undefined,
    nativeCoordinate: placement.native_coordinate
      ? {
          anchor: placement.native_coordinate.anchor,
          spriteRecord: placement.native_coordinate.sprite_record,
        }
      : undefined,
  };
}

export function buildSceneProjection(
  catalogs: RuntimeCatalogs,
  roomId = "room:0",
  options?: RoomSceneResolveOptions,
): SceneProjection {
  const runtimeRoom = resolveRoomScene(catalogs, roomId, options);
  const sceneMode = options?.sceneMode ?? "floor00";
  const scene = catalogs.scene.scenes.find((candidate) => candidate.id === roomId);
  const sourceRoom = catalogs.roomSceneRuntime.rooms.find((candidate) => candidate.room_key === roomId);
  if (!sourceRoom) {
    throw new Error(`RoomSceneRuntime source record is missing ${roomId}`);
  }
  const isMainDisplay = roomId === "room:0" && runtimeRoom.context === "main_display";
  const rawOverlay = roomId === "room:17" && runtimeRoom.context === "main_display"
    ? buildRoomRawOverlay(catalogs.roomRScene, sourceRoom)
    : null;
  const floorRender = isMainDisplay ? resolveFloorRender() : undefined;
  const cells: SceneCellProjection[] = runtimeRoom.placements.map((placement) => ({
    cell: placement.cell,
    rawType: placement.rawType,
    rawDirection: placement.rawDirection,
    directionLabel: placement.directionLabel,
    directionVector: placement.directionVector,
    reverseDirection: placement.reverseDirection,
    passable: placement.passable,
    collisionKind: placement.collisionKind,
    rawTypeLabel: placement.rawTypeLabel || rawTypeLabel(catalogs.objects.raw_object_types, placement.rawType),
  }));
  const mapCells: SceneMapCellProjection[] = runtimeRoom.mapCells.map((cell) => ({
    cell: cell.cell,
    rawIndex: cell.rawIndex,
    selectorId: cell.selectorId,
    filename: cell.filename,
    assetId: cell.assetId,
    meaning: cell.meaning,
    nativeFloorPass: cell.nativeFloorPass,
  }));
  const extensionWalls: SceneMapWallProjection[] = runtimeRoom.extensionWalls.map((wall) => ({ ...wall }));

  const structuralFacilities: VerifiedStructuralFacilityProjection[] = [];
  const nativeInitialObjects: VerifiedNativeInitialObjectProjection[] = [];
  const sceneAssets: SceneAssetProjection[] = [];
  if (roomId === "room:0" && sceneMode === "floor00") {
    for (const facility of catalogs.floor00.structural_facilities) {
      structuralFacilities.push(verifiedStructuralFacility(catalogs, facility));
    }
  }
  for (const binding of runtimeRoom.nativeBindings) {
    nativeInitialObjects.push({
      id: `${binding.object_id}@${binding.cell[0]}:${binding.cell[1]}`,
      objectId: binding.object_id,
      furnitureDataId: binding.furniture_data_id,
      cell: [binding.cell[0], binding.cell[1]],
      label: binding.object_id,
      rawType: binding.raw_type,
      nativeStatus: binding.native_status,
      selectorFlag: binding.selector_flag.name,
      scanOrder: binding.scan_order,
    });
  }
  for (const asset of Object.values(runtimeRoom.assets)) {
    sceneAssets.push({
      id: `scene:${roomId}/${asset.role}`,
      role: asset.role,
      cell: asset.cell,
      rawSelectorId: asset.rawSelectorId,
      runtimeAssetId: asset.runtimeAssetId,
      filename: asset.filename,
      status: asset.runtimeAssetId
        ? asset.role === "floor" ? "approved_room_selector_asset" : asset.compositionStatus
        : "blocked_runtime_asset_not_promoted",
      sourceResolutionStatus: asset.sourceStatus,
      runtimeResolutionStatus: asset.runtimeStatus,
      floorResolutionMode: asset.resolutionMode,
      metadataFilename: asset.metadataFilename,
      cellScope: asset.cellScope,
      nativeCoordinate: asset.nativeCoordinate,
    });
  }

  return {
    sceneId: roomId,
    sceneMode,
    name: scene?.name.English ?? runtimeRoom.name,
    gridWidth: runtimeRoom.gridWidth,
    gridHeight: runtimeRoom.gridHeight,
    cells,
    mapWidth: runtimeRoom.mapWidth,
    mapHeight: runtimeRoom.mapHeight,
    nativeFloorValue: runtimeRoom.nativeFloorValue,
    roomContext: runtimeRoom.context,
    environmentScope: runtimeRoom.environmentScope,
    topologyStatus: runtimeRoom.topologyStatus,
    extensionWallStatus: runtimeRoom.extensionWallStatus,
    mapCells,
    floorResolutionMode: floorRender?.resolutionMode ?? runtimeRoom.assets.floor.resolutionMode ?? "exact_native_floor_table_resolution",
    floorMetadataFilename: floorRender?.metadataFilename ?? runtimeRoom.assets.floor.metadataFilename ?? runtimeRoom.assets.floor.filename ?? "",
    extensionWalls,
    structuralFacilities,
    nativeInitialObjects,
    sceneAssets,
    presentationLayout: runtimeRoom.presentationLayout,
    drawPasses: catalogs.render3c.draw_passes.map((pass) => pass.id),
    catalogObjectNames: catalogs.objects.objects.map((object) => object.name.values.English),
    runtimeRoom,
    rawOverlay,
  };
}
