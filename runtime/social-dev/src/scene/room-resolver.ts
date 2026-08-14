import displayAssetManifestJson from "../../evidence/display_asset_manifest.json";
import type {
  DefaultMapChipContract,
  NativeRoomFloorTopologyVariant,
  NativeRoomFloorTopologyVariantId,
  NativeSceneAssemblyRoom,
  RoomRuntimeNativeBinding,
  RoomSceneRuntimeRecord,
} from "../catalog/types";
import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { Cell } from "../core/types";
import { classifyNativeCollision, type NativeCollisionKind } from "./native-collision";
import { resolveExtensionWallPieces, type ExtensionWallPiece } from "./extension-wall";
import {
  resolveFloor00VisualLayout,
  type Floor00VisualLayoutProjection,
} from "./floor00-visual-layout";

export type RoomPlacementKind =
  | "empty_walkable"
  | "place_slot_or_fixture"
  | "desk_slot_or_fixture"
  | "footprint_fixture"
  | "anchor_fixture"
  | "door_fixture"
  | "boundary_fixture"
  | "native_instance";

export type RoomSceneContext = "main_display" | "persistent_room" | "addition_floor_preview";
export type SceneProjectionMode = "display-slice-01" | "floor00";
export type RoomEnvironmentScope = "native_main_14x14_outer_map" | "native_room_topology_only";

export interface RoomSceneResolveOptions {
  readonly nativeFloorValue?: number;
  readonly context?: RoomSceneContext;
  readonly sceneMode?: SceneProjectionMode;
  readonly dimensions?: {
    readonly width: number;
    readonly height: number;
  };
}

export interface ResolvedRoomAsset {
  readonly role: "floor" | "wall" | "door";
  readonly cell?: Cell;
  readonly rawSelectorId: number;
  readonly nativeSelectorId?: number;
  readonly runtimeSelectorId?: number;
  readonly metadataFilename?: string;
  readonly filename?: string;
  readonly sourceAssetId?: string;
  readonly runtimeAssetId?: string;
  readonly sourceStatus: string;
  readonly resolutionStatus: string;
  readonly runtimeStatus: string;
  readonly resolutionMode?: string;
  readonly compositionStatus: string;
  readonly cellScope?: {
    readonly width: number;
    readonly height: number;
    readonly mode: string;
    readonly cells: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly anchorFormula: Readonly<Record<string, string>>;
    readonly spriteRecords: Readonly<Record<string, Record<string, unknown>>>;
    readonly spriteLayers: Readonly<Record<string, readonly Record<string, unknown>[]>>;
  };
  readonly nativeCoordinate?: {
    readonly anchor: { readonly x: number; readonly y: number };
    readonly spriteRecord: Record<string, unknown>;
  };
}

export interface ResolvedRoomMapCell {
  readonly cell: Cell;
  readonly rawIndex: number;
  readonly selectorId: number;
  readonly filename: string | null;
  readonly assetId: string | null;
  readonly meaning: string;
  readonly nativeFloorPass: boolean;
  readonly resolutionStatus: string;
}

export interface ResolvedRoomPlacement {
  readonly id: string;
  readonly cell: Cell;
  readonly kind: RoomPlacementKind;
  readonly rawType: number;
  readonly rawTypeLabel: string;
  readonly rawDirection: number;
  readonly directionStatus: string;
  readonly directionLabel: string;
  readonly directionVector: readonly [number, number];
  readonly reverseDirection: number;
  readonly passable: boolean;
  readonly collisionKind: NativeCollisionKind;
  readonly furnitureDataId?: number;
  readonly objectId?: string;
  readonly bindingStatus: string;
  readonly sourceStatus: string;
}

export interface ResolvedRoomScene {
  readonly roomId: string;
  readonly dataKey: string;
  readonly name: string;
  readonly gridWidth: number;
  readonly gridHeight: number;
  readonly mapWidth: number;
  readonly mapHeight: number;
  readonly mapVariant: string;
  readonly nativeFloorValue: number;
  readonly context: RoomSceneContext;
  readonly environmentScope: RoomEnvironmentScope;
  readonly topologyStatus: string;
  readonly extensionWallStatus: string;
  readonly mapCells: readonly ResolvedRoomMapCell[];
  readonly assets: Readonly<Record<"floor" | "wall" | "door", ResolvedRoomAsset>>;
  readonly placements: readonly ResolvedRoomPlacement[];
  readonly nativeBindings: readonly RoomRuntimeNativeBinding[];
  readonly extensionWalls: readonly ExtensionWallPiece[];
  readonly presentationLayout: Floor00VisualLayoutProjection | null;
  readonly unresolved: readonly string[];
  readonly status: "pass";
}

const RAW_KIND_BY_TYPE: Readonly<Record<number, RoomPlacementKind>> = {
  0: "empty_walkable",
  1: "place_slot_or_fixture",
  2: "desk_slot_or_fixture",
  3: "footprint_fixture",
  4: "anchor_fixture",
  5: "door_fixture",
  6: "boundary_fixture",
};

function displayAssetIds(): ReadonlySet<string> {
  const manifest = displayAssetManifestJson as { readonly assets: readonly { readonly asset_id: string }[] };
  return new Set(manifest.assets.map((asset) => asset.asset_id));
}

function roomRecord(catalogs: RuntimeCatalogs, roomId: string): RoomSceneRuntimeRecord {
  const room = catalogs.roomSceneRuntime.rooms.find((candidate) => candidate.room_key === roomId);
  if (!room) {
    throw new Error(`RoomSceneRuntime is missing ${roomId}`);
  }
  return room;
}

function assemblyRoom(catalogs: RuntimeCatalogs, roomId: string): NativeSceneAssemblyRoom {
  const room = catalogs.nativeAssembly.rooms.find((candidate) => candidate.room_key === roomId);
  if (!room) {
    throw new Error(`NativeSceneAssembly is missing ${roomId}`);
  }
  return room;
}

interface ResolvedNativeTopology {
  readonly nativeFloorValue: number;
  readonly variantId: NativeRoomFloorTopologyVariantId;
  readonly variant: NativeRoomFloorTopologyVariant;
  readonly width: number;
  readonly height: number;
  readonly rows: readonly (readonly number[])[];
  readonly context: RoomSceneContext;
  readonly environmentScope: RoomEnvironmentScope;
}

function resolveNativeTopology(
  catalogs: RuntimeCatalogs,
  assembly: NativeSceneAssemblyRoom,
  options?: RoomSceneResolveOptions,
): ResolvedNativeTopology {
  const nativeFloorValue = options?.nativeFloorValue ?? assembly.map_chip.native_floor_value;
  if (!Number.isInteger(nativeFloorValue)) {
    throw new Error(`Room.floor_ must be an integer, received ${String(nativeFloorValue)}`);
  }
  const variantId: NativeRoomFloorTopologyVariantId = nativeFloorValue === 0 ? "floor_0" : "floor_nonzero";
  const variant = catalogs.nativeRoomFloorUsage.topology_selection.variants[variantId];
  if (!variant) {
    throw new Error(`NativeRoomFloorUsage is missing topology variant ${variantId}`);
  }
  const context = options?.context ?? (
    nativeFloorValue !== 0
      ? "addition_floor_preview"
      : options?.dimensions?.width === 4 && options?.dimensions?.height === 4
        ? "persistent_room"
        : "main_display"
  );
  const dimensions = options?.dimensions ?? (
    context === "main_display"
      ? { width: catalogs.defaultMap.room.width, height: catalogs.defaultMap.room.height }
      : context === "persistent_room"
        ? { width: 4, height: 4 }
        : { width: variant.width, height: variant.height }
  );
  const { width, height } = dimensions;
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1) {
    throw new Error(`Room topology dimensions must be positive integers, received ${width}x${height}`);
  }
  if (variantId === "floor_nonzero" && (width !== 4 || height !== 4)) {
    throw new Error(`NativeRoomFloorUsage rejects floor=${nativeFloorValue} at ${width}x${height}; MAPCHIP_ARRAY[1] is native 4x4 only`);
  }
  if (variantId === "floor_0" && !((width === 4 && height === 4) || (width === 14 && height === 14))) {
    throw new Error(`NativeRoomFloorUsage rejects floor=0 at ${width}x${height}; approved Room constructor dimensions are 4x4 or 14x14`);
  }
  if (width * height > variant.length) {
    throw new Error(`NativeRoomFloorUsage rejects ${width}x${height}; ${variantId} contains only ${variant.length} native cells`);
  }
  if (context === "main_display" && (nativeFloorValue !== 0 || width !== 14 || height !== 14)) {
    throw new Error("RoomSceneContext main_display requires floor=0 at 14x14");
  }
  if (context === "persistent_room" && (nativeFloorValue !== 0 || width !== 4 || height !== 4)) {
    throw new Error("RoomSceneContext persistent_room requires floor=0 at 4x4");
  }
  if (context === "addition_floor_preview" && (nativeFloorValue === 0 || width !== 4 || height !== 4)) {
    throw new Error("RoomSceneContext addition_floor_preview requires floor!=0 at 4x4");
  }
  const environmentScope: RoomEnvironmentScope = context === "main_display"
    ? "native_main_14x14_outer_map"
    : "native_room_topology_only";
  const flatValues = variant.rows.flat();
  const rows = Array.from({ length: height }, (_, y) => flatValues.slice(y * width, (y + 1) * width));
  if (rows.some((row) => row.length !== width)) {
    throw new Error(`NativeRoomFloorUsage ${variantId} cannot materialize ${width}x${height} rows`);
  }
  const topologyStatus = variant.status === "verified_native_topology"
    ? "verified_native_floor_selector_and_dimensions"
    : `blocked_native_topology_status:${variant.status}`;
  if (topologyStatus.startsWith("blocked_")) {
    throw new Error(topologyStatus);
  }
  return { nativeFloorValue, variantId, variant, width, height, rows, context, environmentScope };
}

function resolveAsset(
  catalogs: RuntimeCatalogs,
  room: RoomSceneRuntimeRecord,
  role: "floor" | "wall" | "door",
  displayIds: ReadonlySet<string>,
): ResolvedRoomAsset {
  const selector = room.selectors[role];
  const roomAsset = catalogs.roomSceneAssets.rooms.find((candidate) => candidate.room_key === room.room_key)?.assets[role];
  const rawSelectorId = selector.native_id;
  const nativeSelectorId = selector.native_selector_id;
  const sourceAssetId = selector.target_asset_id;
  const sourceStatus = selector.status;
  if (role === "floor") {
    const alias = selector.runtime_alias;
    const filename = alias?.render_filename ?? selector.target_filename;
    const metadataFilename = alias?.metadata_filename ?? selector.target_filename;
    const runtimeAssetId = filename && catalogs.defaultMap.source_assets.files[filename]
      ? `map:chip/${filename}`
      : roomAsset?.asset_id;
    return {
      role,
      rawSelectorId,
      nativeSelectorId,
      runtimeSelectorId: alias?.selector_id ?? nativeSelectorId ?? rawSelectorId,
      metadataFilename,
      filename,
      sourceAssetId: sourceAssetId ?? (filename ? `asset:01_GAME_PACKS/chip/${filename}` : undefined),
      runtimeAssetId,
      sourceStatus,
      resolutionStatus: alias?.status ?? (selector.status === "resolved" ? "resolved" : "unresolved"),
      runtimeStatus: runtimeAssetId ? "pass_runtime_map_asset" : "not_promoted_runtime_asset",
      resolutionMode: alias ? "explicit_runtime_alias" : "exact_native_floor_table_resolution",
      compositionStatus: "native_map_chip_floor_composition",
    };
  }

  const filename = selector.target_filename;
  const assetId = sourceAssetId ?? (filename ? `asset:01_GAME_PACKS/chip/${filename}` : undefined);
  const runtimeAssetId = assetId && displayIds.has(assetId) ? assetId : roomAsset?.asset_id;
  return {
    role,
    rawSelectorId,
    nativeSelectorId,
    runtimeSelectorId: nativeSelectorId ?? rawSelectorId,
    filename,
    sourceAssetId: assetId,
    runtimeAssetId,
    sourceStatus,
    resolutionStatus: selector.status === "resolved" ? "resolved" : "unresolved",
    runtimeStatus: runtimeAssetId
      ? displayIds.has(runtimeAssetId) ? "pass_runtime_display_asset" : "pass_promoted_room_selector_asset"
      : "not_promoted_runtime_asset",
    resolutionMode: "exact_native_img_selector_resolution",
    compositionStatus: "awaiting_native_scene_assembly",
  };
}

function buildPlacements(catalogs: RuntimeCatalogs, room: RoomSceneRuntimeRecord): ResolvedRoomPlacement[] {
  const bindingByCell = new Map(room.native_bindings.map((binding) => [`${binding.cell[0]}:${binding.cell[1]}`, binding]));
  const directionByRaw = catalogs.nativeAssembly.direction.values;
  return room.raw_cells.map((raw) => {
    const binding = bindingByCell.get(`${raw.x}:${raw.y}`);
    const kind = binding ? "native_instance" : RAW_KIND_BY_TYPE[raw.raw_type] ?? "empty_walkable";
    const direction = directionByRaw[String(raw.raw_direction)];
    if (!direction) {
      throw new Error(`NativeSceneAssembly is missing direction ${raw.raw_direction}`);
    }
    const collision = classifyNativeCollision(raw.raw_type, Boolean(binding));
    return {
      id: `placement:${room.room_key}:${raw.x}:${raw.y}`,
      cell: [raw.x, raw.y],
      kind,
      rawType: raw.raw_type,
      rawTypeLabel: raw.raw_type_label,
      rawDirection: raw.raw_direction,
      directionStatus: "closed_native_direction_trace",
      directionLabel: direction.label,
      directionVector: [direction.vector[0], direction.vector[1]],
      reverseDirection: direction.reverse,
      passable: collision.passable,
      collisionKind: collision.kind,
      ...(binding
        ? {
            furnitureDataId: binding.furniture_data_id,
            objectId: binding.object_id,
            bindingStatus: "verified_explicit_native_binding",
          }
        : { bindingStatus: "raw_cell_without_furniture_data_binding" }),
      sourceStatus: raw.source_status,
    };
  });
}

function buildMapCells(
  catalogs: RuntimeCatalogs,
  topology: ResolvedNativeTopology,
  floor: ResolvedRoomAsset,
): ResolvedRoomMapCell[] {
  const culling = catalogs.defaultMap.draw_contract.floor_image_culling;
  const cells: ResolvedRoomMapCell[] = [];
  const usesFullMapCulling = topology.width === catalogs.defaultMap.room.width && topology.height === catalogs.defaultMap.room.height;
  for (let y = 0; y < topology.height; y += 1) {
    const row = topology.rows[y];
    if (!row) {
      throw new Error(`NativeRoomFloorUsage ${topology.variantId} is missing row ${y}`);
    }
    for (let x = 0; x < topology.width; x += 1) {
      const rawIndex = row[x];
      const nativeFloorPass = usesFullMapCulling
        ? x >= culling.x_inclusive[0]
          && x <= culling.x_inclusive[1]
          && y >= culling.y_inclusive[0]
          && y <= culling.y_inclusive[1]
        : true;
      if (rawIndex === 1) {
        cells.push({
          cell: [x, y],
          rawIndex,
          selectorId: floor.runtimeSelectorId ?? floor.nativeSelectorId ?? floor.rawSelectorId,
          filename: floor.filename ?? null,
          assetId: floor.runtimeAssetId ?? null,
          meaning: floor.runtimeAssetId ? "room_floor_resolved_from_roomdata_floor_image_table" : "room_floor_source_resolved_runtime_asset_pending",
          nativeFloorPass,
          resolutionStatus: floor.runtimeStatus,
        });
        continue;
      }
      const mapping = catalogs.defaultMap.raw_index_to_selector[String(rawIndex)];
      if (!mapping) {
        throw new Error(`DefaultMapChip is missing raw map selector ${rawIndex}`);
      }
      cells.push({
        cell: [x, y],
        rawIndex,
        selectorId: mapping.selector_id,
        filename: mapping.filename,
        assetId: mapping.asset_id,
        meaning: mapping.meaning,
        nativeFloorPass,
        resolutionStatus: mapping.asset_id ? "resolved_shared_map_asset" : "empty_map_cell",
      });
    }
  }
  return cells;
}

function buildExtensionWalls(catalogs: RuntimeCatalogs, topology: ResolvedNativeTopology): readonly ExtensionWallPiece[] {
  if (topology.width !== catalogs.defaultMap.room.width || topology.height !== catalogs.defaultMap.room.height) {
    return [];
  }
  return resolveExtensionWallPieces(
    catalogs.defaultMap.extension_wall,
    `map:chip/${catalogs.defaultMap.extension_wall.source_image_filename}`,
  );
}

export function resolveRoomScene(
  catalogs: RuntimeCatalogs,
  roomId = "room:0",
  options?: RoomSceneResolveOptions,
): ResolvedRoomScene {
  const room = roomRecord(catalogs, roomId);
  const assembly = assemblyRoom(catalogs, roomId);
  const topology = resolveNativeTopology(catalogs, assembly, options);
  const displayIds = displayAssetIds();
  const resolvedAssets = {
    floor: resolveAsset(catalogs, room, "floor", displayIds),
    wall: resolveAsset(catalogs, room, "wall", displayIds),
    door: resolveAsset(catalogs, room, "door", displayIds),
  } as const;
  const presentationLayout = roomId === "room:0" && options?.sceneMode === "floor00"
    ? resolveFloor00VisualLayout(
      catalogs.floor00VisualLayout,
      catalogs.defaultMap,
      assembly.wall.cells_by_frame,
    )
    : null;
  const assets: Readonly<Record<"floor" | "wall" | "door", ResolvedRoomAsset>> = {
    floor: resolvedAssets.floor,
    wall: {
      ...resolvedAssets.wall,
      compositionStatus: assembly.wall.status,
      cellScope: {
        width: room.grid.width,
        height: room.grid.height,
        mode: "native_objchip_wall_predicates",
        cells: presentationLayout?.wallCellsByFrame ?? assembly.wall.cells_by_frame,
        anchorFormula: {
          x: "ofx + (x + y) * 20",
          y: "ofy + (y - x) * 10 + 9",
        },
        spriteRecords: assembly.wall.sprite_records,
        spriteLayers: assembly.wall.sprite_layers,
      },
    },
    door: {
      ...resolvedAssets.door,
      cell: assembly.door.cells[0] ? [assembly.door.cells[0][0], assembly.door.cells[0][1]] : undefined,
      compositionStatus: assembly.door.status,
      nativeCoordinate: {
        anchor: {
          x: (assembly.door.cells[0]?.[0] ?? 0) * 20 + (assembly.door.cells[0]?.[1] ?? 0) * 20,
          y: ((assembly.door.cells[0]?.[1] ?? 0) - (assembly.door.cells[0]?.[0] ?? 0)) * 10 + 9,
        },
        spriteRecord: assembly.door.sprite_record,
      },
    },
  };
  const mapCells = buildMapCells(catalogs, topology, assets.floor);
  const placements = buildPlacements(catalogs, room);
  const unresolved: string[] = [];
  for (const asset of Object.values(assets)) {
    if (!asset.runtimeAssetId) {
      unresolved.push(`${asset.role}:runtime_asset_not_promoted:${asset.filename ?? asset.rawSelectorId}`);
    }
  }
  if (assembly.wall.status !== "approved_native_coordinate_composition") {
    unresolved.push(`wall:assembly_status:${assembly.wall.status}`);
  }
  if (assembly.door.status !== "approved_native_coordinate_composition") {
    unresolved.push(`door:assembly_status:${assembly.door.status}`);
  }
  return {
    roomId,
    dataKey: room.data_key,
    name: room.native.name,
    gridWidth: room.grid.width,
    gridHeight: room.grid.height,
    mapWidth: topology.width,
    mapHeight: topology.height,
    mapVariant: topology.variantId,
    nativeFloorValue: topology.nativeFloorValue,
    context: topology.context,
    environmentScope: topology.environmentScope,
    topologyStatus: "verified_native_floor_selector_and_dimensions",
    extensionWallStatus: topology.width === catalogs.defaultMap.room.width && topology.height === catalogs.defaultMap.room.height
      ? "approved_native_14x14_extension_predicates"
      : "explicitly_not_promoted_for_native_4x4_topology",
    mapCells,
    assets,
    placements,
    nativeBindings: room.native_bindings,
    extensionWalls: presentationLayout?.extensionWalls ?? buildExtensionWalls(catalogs, topology),
    presentationLayout,
    unresolved,
    status: "pass",
  };
}

export function roomKeys(catalogs: RuntimeCatalogs): readonly string[] {
  return catalogs.roomSceneRuntime.rooms.map((room) => room.room_key);
}
