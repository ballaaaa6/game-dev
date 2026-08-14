import actorCatalogJson from "../../evidence/actor_catalog_contract.json";
import actorBehaviorJson from "../../evidence/actor_behavior_contract.json";
import actorSpawnJson from "../../evidence/actor_spawn_contract.json";
import cameraCoordinateJson from "../../evidence/camera_coordinate_contract.json";
import characterCapabilityJson from "../../evidence/character_capability_contract.json";
import characterAssetManifestJson from "../../evidence/character_asset_manifest.json";
import characterMetadataJson from "../../evidence/character_metadata_contract.json";
import displayAssetManifestJson from "../../evidence/display_asset_manifest.json";
import objectCatalogJson from "../../evidence/object_catalog_contract.json";
import preRuntimeClosureJson from "../../evidence/pre_runtime_closure_contract.json";
import phase3cRenderJson from "../../evidence/phase3c_render_contract.json";
import roomPlacementJson from "../../evidence/room_placement_contract.json";
import sceneCatalogJson from "../../evidence/scene_catalog_contract.json";
import strictClosureJson from "../../evidence/phase3c_strict_closure_contract.json";
import tickOrderJson from "../../evidence/tick_order_contract.json";
import defaultMapChipJson from "../../evidence/default_map_chip_contract.json";
import roomSceneRuntimeJson from "../../evidence/room_scene_runtime_contract.json";
import nativeDirectionJson from "../../evidence/native_direction_contract.json";
import roomSceneAssetManifestJson from "../../evidence/room_scene_asset_manifest.json";
import roomRSceneJson from "../../evidence/room_r_scene_contract.json";
import nativeContentCatalogJson from "../../evidence/native_content_catalog.json";
import nativeSceneAssemblyJson from "../../evidence/native_scene_assembly_contract.json";
import nativeRoomFloorUsageJson from "../../evidence/native_room_floor_usage_contract.json";
import assetMetadataRuntimeManifestJson from "../../evidence/asset_metadata_runtime_manifest.json";
import floor00SceneJson from "../../evidence/floor00_scene_contract.json";
import floor00DisplayPolicyJson from "../../evidence/floor00_display_policy.json";
import floor00VisualLayoutJson from "../../evidence/floor00_visual_layout_contract.json";
import type {
  ActorBehaviorContract,
  ActorCatalogContract,
  ActorSpawnContract,
  CharacterMetadataContract,
  CharacterCapabilityContract,
  CharacterAssetManifest,
  ActorSpawnFixture,
  CameraCoordinateContract,
  DefaultMapChipContract,
  Phase3CRenderContract,
  ObjectCatalogContract,
  PreRuntimeClosureContract,
  RoomPlacementContract,
  SceneCatalogContract,
  Phase3CStrictClosureContract,
  TickOrderContract,
  NativeDirectionContract,
  RoomSceneRuntimeContract,
  RoomSceneAssetManifest,
  RoomRSceneContract,
  NativeContentCatalogContract,
  AssetMetadataRuntimeManifest,
  NativeSceneAssemblyContract,
  NativeRoomFloorUsageContract,
  Floor00SceneContract,
  Floor00DisplayPolicyContract,
  Floor00VisualLayoutContract,
} from "./types";

// The imported JSON files are the only data entry point for the browser runtime.
// Raw C# and source/extraction roots are deliberately absent from this module.
export interface RuntimeCatalogs {
  readonly scene: SceneCatalogContract;
  readonly objects: ObjectCatalogContract;
  readonly actors: ActorCatalogContract;
  readonly characterMetadata: CharacterMetadataContract;
  readonly characterCapabilities: CharacterCapabilityContract;
  readonly characterAssets: CharacterAssetManifest;
  readonly spawn: ActorSpawnContract;
  readonly spawnFixture: ActorSpawnFixture;
  readonly camera: CameraCoordinateContract;
  readonly defaultMap: DefaultMapChipContract;
  readonly roomPlacement: RoomPlacementContract;
  readonly render3c: Phase3CRenderContract;
  readonly strictClosure: Phase3CStrictClosureContract;
  readonly behavior: ActorBehaviorContract;
  readonly tickOrder: TickOrderContract;
  readonly preRuntime: PreRuntimeClosureContract;
  readonly roomSceneRuntime: RoomSceneRuntimeContract;
  readonly nativeDirection: NativeDirectionContract;
  readonly roomSceneAssets: RoomSceneAssetManifest;
  readonly roomRScene: RoomRSceneContract;
  readonly nativeContent: NativeContentCatalogContract;
  readonly nativeAssembly: NativeSceneAssemblyContract;
  readonly nativeRoomFloorUsage: NativeRoomFloorUsageContract;
  readonly floor00: Floor00SceneContract;
  readonly floor00DisplayPolicy: Floor00DisplayPolicyContract;
  readonly floor00VisualLayout: Floor00VisualLayoutContract;
  readonly assetMetadataRuntime: AssetMetadataRuntimeManifest;
  readonly displayScene: SceneCatalogContract["scenes"][number];
  readonly activeActors: readonly ActorSpawnFixture["actors"][number][];
}

type ContractCandidate = {
  readonly status?: unknown;
  readonly semantic_status?: unknown;
};

function requireApproved<T extends ContractCandidate>(value: unknown, label: string): T {
  if (typeof value !== "object" || value === null) {
    throw new Error(`${label} is not an object contract`);
  }
  const candidate = value as ContractCandidate;
  if (candidate.status !== "pass") {
    throw new Error(`${label} status is ${String(candidate.status)}; expected pass`);
  }
  if (candidate.semantic_status !== "approved_for_runtime_contract") {
    throw new Error(`${label} semantic status is ${String(candidate.semantic_status)}; expected approved_for_runtime_contract`);
  }
  return value as T;
}

function requirePass<T extends ContractCandidate>(value: unknown, label: string): T {
  if (typeof value !== "object" || value === null || (value as ContractCandidate).status !== "pass") {
    throw new Error(`${label} must have status pass`);
  }
  return value as T;
}

function requireRuntimeCatalog<T extends ContractCandidate>(value: unknown, label: string): T {
  if (typeof value !== "object" || value === null) {
    throw new Error(`${label} is not an object contract`);
  }
  const candidate = value as ContractCandidate;
  if (candidate.status !== "pass" || candidate.semantic_status !== "approved_for_runtime_catalog") {
    throw new Error(`${label} is not an approved runtime catalog`);
  }
  return value as T;
}

function requireRuntimeQueryManifest(value: unknown, label: string): AssetMetadataRuntimeManifest {
  if (typeof value !== "object" || value === null) {
    throw new Error(`${label} is not an object contract`);
  }
  const candidate = value as ContractCandidate;
  if (candidate.status !== "pass" || candidate.semantic_status !== "approved_for_runtime_query_contract") {
    throw new Error(`${label} is not an approved runtime query manifest`);
  }
  return value as AssetMetadataRuntimeManifest;
}

function requireEqual(left: unknown, right: unknown, label: string): void {
  if (left !== right) {
    throw new Error(`${label} mismatch: ${String(left)} !== ${String(right)}`);
  }
}

function cellKey(cell: readonly [number, number]): string {
  return `${cell[0]},${cell[1]}`;
}

function sortedCellKeys(cells: readonly (readonly [number, number])[]): string[] {
  return cells.map(cellKey).sort();
}

function requireCellSetEqual(
  left: readonly (readonly [number, number])[],
  right: readonly (readonly [number, number])[],
  label: string,
): void {
  requireEqual(JSON.stringify(sortedCellKeys(left)), JSON.stringify(sortedCellKeys(right)), label);
}

function requireCellsInBounds(
  cells: readonly (readonly [number, number])[],
  width: number,
  height: number,
  label: string,
): void {
  for (const cell of cells) {
    if (cell.length !== 2 || cell[0] < 0 || cell[0] >= width || cell[1] < 0 || cell[1] >= height) {
      throw new Error(`${label} contains out-of-bounds cell ${cell.join(",")}`);
    }
  }
}

export function validateFloor00VisualLayoutContract(
  layout: Floor00VisualLayoutContract,
  defaultMap: DefaultMapChipContract,
  floor00: Floor00SceneContract,
  nativeAssembly: NativeSceneAssemblyContract,
): Floor00VisualLayoutContract {
  requireApproved<Floor00VisualLayoutContract>(layout, "Floor00VisualLayout");
  requireEqual(layout.catalog_id, "floor00-visual-layout", "Floor00VisualLayout catalog id");
  requireEqual(layout.scene_ref.id, floor00.scene_ref.id, "Floor00VisualLayout scene id");
  requireEqual(layout.scene_ref.scene_mode, "floor00", "Floor00VisualLayout scene mode");
  requireEqual(layout.glass.source_asset_id, `map:chip/${defaultMap.extension_wall.source_image_filename}`, "Floor00VisualLayout glass asset");
  requireEqual(layout.wood_wall.source_asset_id, "asset:01_GAME_PACKS/chip/wall_00.png", "Floor00VisualLayout wood asset");
  requireEqual(layout.wood_wall.source_seb_asset_id, "asset:01_GAME_PACKS/chip/wall_00.seb", "Floor00VisualLayout wood SEB asset");
  requireEqual(JSON.stringify(layout.wood_wall.layer_order), JSON.stringify([0, 1]), "Floor00VisualLayout wall layer order");
  requireEqual(floor00.render_composition.wall_boundary_asset, "wall_01.png", "Floor00VisualLayout boundary asset");

  const nativeAssemblyRoom = nativeAssembly.rooms.find((room) => room.room_key === floor00.scene_ref.id);
  if (!nativeAssemblyRoom) {
    throw new Error(`Floor00VisualLayout is missing native assembly room ${floor00.scene_ref.id}`);
  }

  const extensionGroups = Object.keys(defaultMap.extension_wall.composition_groups).sort();
  requireEqual(
    JSON.stringify(Object.keys(layout.glass.native_trigger_cells_by_group).sort()),
    JSON.stringify(extensionGroups),
    "Floor00VisualLayout native glass groups",
  );
  requireEqual(
    JSON.stringify(Object.keys(layout.glass.final_trigger_cells_by_group).sort()),
    JSON.stringify(extensionGroups),
    "Floor00VisualLayout final glass groups",
  );
  const nativeGlassCells: (readonly [number, number])[] = [];
  for (const groupId of extensionGroups) {
    const group = defaultMap.extension_wall.composition_groups[groupId];
    const nativeCells = defaultMap.extension_wall.native_predicates[groupId];
    if (!group || !nativeCells) {
      throw new Error(`DefaultMapChip is missing extension group ${groupId}`);
    }
    requireCellSetEqual(
      layout.glass.native_trigger_cells_by_group[groupId] ?? [],
      nativeCells,
      `Floor00VisualLayout native trigger cells ${groupId}`,
    );
    requireEqual(
      layout.glass.frame_ids_by_group[groupId],
      group.frame_id,
      `Floor00VisualLayout frame id ${groupId}`,
    );
    nativeGlassCells.push(...nativeCells);
  }

  const removedKeys = layout.glass.removed_trigger_cells.map(cellKey);
  if (new Set(removedKeys).size !== removedKeys.length) {
    throw new Error("Floor00VisualLayout removed glass cells contain duplicates");
  }
  const nativeGlassKeys = new Set(nativeGlassCells.map(cellKey));
  if (removedKeys.some((key) => !nativeGlassKeys.has(key))) {
    throw new Error("Floor00VisualLayout removes a glass cell that is not in the native extension scope");
  }
  const finalGlassCells = Object.values(layout.glass.final_trigger_cells_by_group).flat();
  const finalGlassKeys = finalGlassCells.map(cellKey);
  if (new Set(finalGlassKeys).size !== finalGlassKeys.length) {
    throw new Error("Floor00VisualLayout final glass cells contain duplicates");
  }
  if (finalGlassKeys.some((key) => removedKeys.includes(key))) {
    throw new Error("Floor00VisualLayout final glass scope overlaps removed glass cells");
  }
  requireCellsInBounds(finalGlassCells, defaultMap.room.width, defaultMap.room.height, "Floor00VisualLayout final glass scope");
  const finalGlassSet = new Set(finalGlassKeys);
  const [stripStartX, stripStartY] = layout.glass.strip_start;
  const [stripEndX, stripEndY] = layout.glass.strip_end;
  if (!finalGlassSet.has(cellKey(layout.glass.strip_start)) || !finalGlassSet.has(cellKey(layout.glass.strip_end))) {
    throw new Error("Floor00VisualLayout glass strip endpoint is not rendered");
  }
  if (layout.glass.strip_axis === "map_x") {
    if (stripStartY !== stripEndY || stripEndX <= stripStartX) {
      throw new Error("Floor00VisualLayout map_x glass strip endpoints are invalid");
    }
    for (let x = stripStartX; x <= stripEndX; x += 1) {
      if (!finalGlassSet.has(`${x},${stripStartY}`)) {
        throw new Error("Floor00VisualLayout glass strip is not continuous");
      }
    }
  } else {
    if (stripStartX !== stripEndX || stripEndY <= stripStartY) {
      throw new Error("Floor00VisualLayout map_y glass strip endpoints are invalid");
    }
    for (let y = stripStartY; y <= stripEndY; y += 1) {
      if (!finalGlassSet.has(`${stripStartX},${y}`)) {
        throw new Error("Floor00VisualLayout glass strip is not continuous");
      }
    }
  }

  const [offsetX, offsetY] = layout.wood_wall.backward_offset;
  if (Math.abs(offsetX) + Math.abs(offsetY) !== 1) {
    throw new Error("Floor00VisualLayout backward offset must move exactly one cell");
  }
  requireEqual(
    JSON.stringify(Object.keys(layout.wood_wall.native_cells_by_frame).sort()),
    JSON.stringify(Object.keys(nativeAssemblyRoom.wall.cells_by_frame).sort()),
    "Floor00VisualLayout native wall frames",
  );
  for (const frameId of Object.keys(nativeAssemblyRoom.wall.cells_by_frame)) {
    requireCellSetEqual(
      layout.wood_wall.native_cells_by_frame[frameId] ?? [],
      nativeAssemblyRoom.wall.cells_by_frame[frameId] ?? [],
      `Floor00VisualLayout native wall cells ${frameId}`,
    );
    const finalCells = layout.wood_wall.final_cells_by_frame[frameId] ?? [];
    requireCellsInBounds(finalCells, floor00.map.obj_chip_width, floor00.map.obj_chip_height, `Floor00VisualLayout final wall cells ${frameId}`);
  }
  const nativeMovedCells = layout.wood_wall.native_cells_by_frame.vertical_frame_1 ?? [];
  const expectedMovedCells = nativeMovedCells.map(([x, y]) => [x + offsetX, y + offsetY] as const);
  requireCellSetEqual(
    layout.wood_wall.final_cells_by_frame.vertical_frame_1 ?? [],
    expectedMovedCells,
    "Floor00VisualLayout moved wall cells",
  );
  const finalUpperCells = layout.wood_wall.final_cells_by_frame.horizontal_frame_0 ?? [];
  if (finalUpperCells.length <= (layout.wood_wall.native_cells_by_frame.horizontal_frame_0?.length ?? 0)) {
    throw new Error("Floor00VisualLayout upper wall was not extended");
  }
  requireEqual(
    cellKey(layout.alignment.upper_edge_cells[1] ?? [-1, -1]),
    cellKey(layout.alignment.left_edge_cells[0] ?? [-2, -2]),
    "Floor00VisualLayout wall edge alignment cell",
  );
  requireEqual(layout.alignment.expected_screen_delta.x, 0, "Floor00VisualLayout alignment x delta");
  requireEqual(layout.alignment.expected_screen_delta.y, 0, "Floor00VisualLayout alignment y delta");
  return layout;
}

export function loadRuntimeCatalogs(): RuntimeCatalogs {
  const scene = requireApproved<SceneCatalogContract>(sceneCatalogJson, "SceneCatalog");
  const objects = requireApproved<ObjectCatalogContract>(objectCatalogJson, "ObjectCatalog");
  const actors = requireApproved<ActorCatalogContract>(actorCatalogJson, "ActorCatalog");
  const characterCapabilities = requireApproved<CharacterCapabilityContract>(characterCapabilityJson, "CharacterCapability");
  const characterAssets = requireRuntimeCatalog<CharacterAssetManifest>(characterAssetManifestJson, "CharacterAssetManifest");
  const characterMetadata = requireApproved<CharacterMetadataContract>(characterMetadataJson, "CharacterMetadata");
  const spawn = requireApproved<ActorSpawnContract>(actorSpawnJson, "ActorSpawn");
  const camera = requireApproved<CameraCoordinateContract>(cameraCoordinateJson, "CameraCoordinate");
  const defaultMap = requireApproved<DefaultMapChipContract>(defaultMapChipJson, "DefaultMapChip");
  const roomPlacement = requireApproved<RoomPlacementContract>(roomPlacementJson, "RoomPlacement");
  const render3c = requireApproved<Phase3CRenderContract>(phase3cRenderJson, "Phase3CRender");
  const strictClosure = requireApproved<Phase3CStrictClosureContract>(strictClosureJson, "Phase3CStrictClosure");
  const behavior = requireApproved<ActorBehaviorContract>(actorBehaviorJson, "ActorBehavior");
  const tickOrder = requireApproved<TickOrderContract>(tickOrderJson, "TickOrder");
  const preRuntime = requirePass<PreRuntimeClosureContract>(preRuntimeClosureJson, "PreRuntimeClosure");
  const roomSceneRuntime = requireApproved<RoomSceneRuntimeContract>(roomSceneRuntimeJson, "RoomSceneRuntime");
  const nativeDirection = requireApproved<NativeDirectionContract>(nativeDirectionJson, "NativeDirection");
  const roomSceneAssets = requireApproved<RoomSceneAssetManifest>(roomSceneAssetManifestJson, "RoomSceneAssetManifest");
  const roomRScene = requireApproved<RoomRSceneContract>(roomRSceneJson, "RoomRScene");
  const nativeContent = requireRuntimeCatalog<NativeContentCatalogContract>(nativeContentCatalogJson, "NativeContentCatalog");
  const nativeAssembly = requireApproved<NativeSceneAssemblyContract>(nativeSceneAssemblyJson, "NativeSceneAssembly");
  const nativeRoomFloorUsage = requireApproved<NativeRoomFloorUsageContract>(nativeRoomFloorUsageJson, "NativeRoomFloorUsage");
  const assetMetadataRuntime = requireRuntimeQueryManifest(assetMetadataRuntimeManifestJson, "AssetMetadataRuntimeManifest");
  const floor00 = requireApproved<Floor00SceneContract>(floor00SceneJson, "Floor00Scene");
  const floor00DisplayPolicy = requireApproved<Floor00DisplayPolicyContract>(floor00DisplayPolicyJson, "Floor00DisplayPolicy");
  const floor00VisualLayout = requireApproved<Floor00VisualLayoutContract>(floor00VisualLayoutJson, "Floor00VisualLayout");
  validateFloor00VisualLayoutContract(floor00VisualLayout, defaultMap, floor00, nativeAssembly);
  // ActorSpawnContract already contains the exact three-actor fixture rows and
  // pins the source fixture hash. Project only that runtime-owned subset so
  // the browser does not import knowledge evidence directly.
  const spawnFixture: ActorSpawnFixture = {
    schema_version: "social-dev-actor-spawn-fixture-v1",
    package: "social-dev-actor-spawn-fixture",
    status: spawn.status,
    semantic_status: "deterministic_fixture",
    catalog_id: "display-slice-01",
    actors: spawn.actors,
    determinism: { content_hash: spawn.fixture_ref.content_hash },
  };

  requirePass(spawnFixture, "ActorSpawnFixture");
  requireEqual(actors.catalog_id, "display-slice-01", "ActorCatalog id");
  requireEqual(characterCapabilities.catalog_id, "character-capabilities-full", "CharacterCapability id");
  requireEqual(characterCapabilities.counts.profiles, 4, "CharacterCapability profile count");
  requireEqual(characterCapabilities.counts.staff_bindings, 141, "CharacterCapability staff binding count");
  requireEqual(characterCapabilities.counts.helper_bindings, 19, "CharacterCapability helper binding count");
  requireEqual(characterCapabilities.counts.human_native_actions, 16, "CharacterCapability native action count");
  requireEqual(characterCapabilities.counts.human_native_action_selectors, 35, "CharacterCapability native selector count");
  requireEqual(characterCapabilities.runtime_policy.instance_creation, "lazy_on_spawn_or_scene_use", "CharacterCapability instance policy");
  requireEqual(characterCapabilities.runtime_policy.source_code_imports, false, "CharacterCapability source import policy");
  requireEqual(characterAssets.catalog_id, "character-assets-full", "CharacterAssetManifest id");
  requireEqual(characterAssets.counts.images, 105, "CharacterAssetManifest image count");
  requireEqual(characterAssets.counts.animations, 35, "CharacterAssetManifest animation count");
  requireEqual(characterAssets.counts.staff_bindings, 141, "CharacterAssetManifest staff binding count");
  requireEqual(characterAssets.counts.decoded_layers, 48, "CharacterAssetManifest decoded layer count");
  requireEqual(characterAssets.counts.decoded_records, 334, "CharacterAssetManifest decoded record count");
  requireEqual(characterAssets.runtime_policy.eager_load_full_catalog, false, "CharacterAssetManifest eager load policy");
  requireEqual(characterAssets.runtime_policy.frame_resolution, "decoded_seb_contract", "CharacterAssetManifest frame resolution policy");
  requireEqual(characterAssets.runtime_policy.source_code_imports, false, "CharacterAssetManifest source import policy");
  requireEqual(characterMetadata.catalog_id, "character-metadata-full", "CharacterMetadata id");
  requireEqual(characterMetadata.counts.staff_records, 141, "CharacterMetadata staff count");
  requireEqual(characterMetadata.counts.helper_records, 19, "CharacterMetadata helper count");
  requireEqual(characterMetadata.counts.job_records, 30, "CharacterMetadata job count");
  requireEqual(characterMetadata.counts.skill_records, 36, "CharacterMetadata skill count");
  requireEqual(characterMetadata.runtime_state_boundary.mutable_actor_state_owner, "ActorState", "CharacterMetadata state owner");
  const capabilityProfiles = new Set(characterCapabilities.profiles.map((profile) => profile.id));
  for (const record of characterMetadata.staff) {
    const profileRef = record.render?.capability_profile_ref;
    if (!profileRef || !capabilityProfiles.has(profileRef)) {
      throw new Error(`CharacterMetadata staff record ${record.id} has no capability profile`);
    }
  }
  for (const record of characterMetadata.helpers) {
    const profileRef = record.render?.capability_profile_ref;
    if (!profileRef || !capabilityProfiles.has(profileRef)) {
      throw new Error(`CharacterMetadata helper record ${record.id} has no capability profile`);
    }
  }
  requireEqual(objects.scene_ref.id, "room:0", "ObjectCatalog scene ref");
  requireEqual(actors.scene_ref.id, "room:0", "ActorCatalog scene ref");
  requireEqual(roomPlacement.scene_ref.id, "room:0", "RoomPlacement scene ref");
  requireEqual(render3c.catalog_id, "display-slice-01", "Phase3C render catalog id");
  requireEqual(strictClosure.catalog_id, "display-slice-01", "Phase3C strict closure catalog id");
  requireEqual(strictClosure.scene_id, "room:0", "Phase3C strict closure scene id");
  requireEqual(defaultMap.catalog_id, "display-slice-01", "DefaultMapChip catalog id");
  requireEqual(nativeRoomFloorUsage.catalog_id, "display-slice-01", "NativeRoomFloorUsage catalog id");
  requireEqual(nativeRoomFloorUsage.topology_selection.native_field, "Room.floor_", "NativeRoomFloorUsage native field");
  requireEqual(
    nativeRoomFloorUsage.topology_selection.predicate,
    "floor == 0 ? MAPCHIP_ARRAY[0] : MAPCHIP_ARRAY[1]",
    "NativeRoomFloorUsage selector predicate",
  );
  for (const variantId of ["floor_0", "floor_nonzero"] as const) {
    const variant = nativeRoomFloorUsage.topology_selection.variants[variantId];
    const legacyVariant = defaultMap.native_static_arrays.map_chip_array_by_floor[variantId];
    requireEqual(variant.length, variant.width * variant.height, `NativeRoomFloorUsage ${variantId} dimensions`);
    requireEqual(variant.rows.length, variant.height, `NativeRoomFloorUsage ${variantId} row count`);
    requireEqual(legacyVariant.length, variant.length, `DefaultMapChip ${variantId} length connection`);
    requireEqual(JSON.stringify(legacyVariant.rows), JSON.stringify(variant.rows), `DefaultMapChip ${variantId} rows connection`);
    for (const row of variant.rows) {
      requireEqual(row.length, variant.width, `NativeRoomFloorUsage ${variantId} row width`);
    }
  }
  requireEqual(nativeRoomFloorUsage.roomdata_catalog.room_count, 18, "NativeRoomFloorUsage RoomData count");
  requireEqual(nativeRoomFloorUsage.roomdata_catalog.room_keys.length, 18, "NativeRoomFloorUsage RoomData key coverage");
  requireEqual(nativeRoomFloorUsage.runtime_policy.mapchip_never_inferred_from_objchip, true, "NativeRoomFloorUsage ObjChip policy");
  requireEqual(nativeRoomFloorUsage.runtime_policy.floor_image_table_is_independent_from_mapchip_topology, true, "NativeRoomFloorUsage floor-image policy");
  requireEqual(
    nativeRoomFloorUsage.runtime_policy.environment_scope?.non_main_outer_mapchip_policy,
    "no_synthetic_14x14_promotion",
    "NativeRoomFloorUsage non-main outer MapChip policy",
  );
  requireEqual(
    nativeRoomFloorUsage.runtime_policy.environment_scope?.main_display?.outer_mapchip,
    "native",
    "NativeRoomFloorUsage main-display outer MapChip scope",
  );
  requireEqual(
    nativeRoomFloorUsage.runtime_policy.environment_scope?.persistent_room?.outer_mapchip,
    "not_present",
    "NativeRoomFloorUsage persistent-room outer MapChip scope",
  );
  requireEqual(
    nativeRoomFloorUsage.runtime_policy.environment_scope?.addition_floor_preview?.outer_mapchip,
    "not_present",
    "NativeRoomFloorUsage addition-floor outer MapChip scope",
  );
  requireEqual(
    nativeRoomFloorUsage.usage.some((usage) => usage.usage_id === "main-display-map" && usage.width === 14 && usage.height === 14),
    true,
    "NativeRoomFloorUsage main display path",
  );
  requireEqual(
    nativeRoomFloorUsage.usage.some((usage) => usage.usage_id === "addition-floor-preview" && usage.topology_variant === "floor_nonzero" && usage.width === 4 && usage.height === 4),
    true,
    "NativeRoomFloorUsage nonzero preview path",
  );
  requireEqual(roomSceneRuntime.catalog_id, "display-slice-01", "RoomSceneRuntime catalog id");
  requireEqual(roomSceneRuntime.counts.rooms, 18, "RoomSceneRuntime room count");
  requireEqual(roomSceneRuntime.counts.rooms_with_shared_mapchip_contract, 18, "RoomSceneRuntime shared MapChip room count");
  requireEqual(roomSceneRuntime.map_chip_ref.shared_topology, true, "RoomSceneRuntime shared MapChip policy");
  requireEqual(roomSceneRuntime.native_identity_policy.objchip_never_infers_furniture_data_id, true, "RoomSceneRuntime ObjChip identity policy");
  requireEqual(nativeDirection.direction_semantics_status, "closed_native_vector_mapping", "NativeDirection semantic status");
  requireEqual(nativeDirection.runtime_policy.preserve_raw_direction, true, "NativeDirection raw policy");
  requireEqual(nativeDirection.runtime_policy.rotation_is_allowed, false, "NativeDirection rotation policy");
  requireEqual(nativeDirection.runtime_policy.expose_native_label_and_vector, true, "NativeDirection exposed mapping policy");
  requireEqual(roomSceneAssets.counts.rooms, 18, "RoomSceneAssetManifest room count");
  requireEqual(roomSceneAssets.counts.unique_selector_pngs, 23, "RoomSceneAssetManifest selector asset count");
  requireEqual(roomSceneAssets.runtime_policy.exact_selector_identity_preserved, true, "RoomSceneAssetManifest identity policy");
  requireEqual(roomSceneAssets.runtime_policy.native_coordinate_composition_not_implied, true, "RoomSceneAssetManifest composition policy");
  requireEqual(roomRScene.catalog_id, "display-slice-01", "RoomR fixture catalog id");
  requireEqual(roomRScene.room_id, "room:17", "RoomR fixture room id");
  requireEqual(roomRScene.fixture_semantic_status, "raw_scene_fixture", "RoomR fixture semantic status");
  requireEqual(roomRScene.grid.width, 10, "RoomR fixture grid width");
  requireEqual(roomRScene.grid.height, 10, "RoomR fixture grid height");
  requireEqual(roomRScene.raw_cells.length, 100, "RoomR fixture raw cell count");
  requireEqual(roomRScene.map_chip.shared_topology, true, "RoomR fixture shared MapChip topology");
  requireEqual(roomRScene.map_chip.width, 14, "RoomR fixture MapChip width");
  requireEqual(roomRScene.map_chip.height, 14, "RoomR fixture MapChip height");
  requireEqual(roomRScene.native_bindings.length, 0, "RoomR fixture native binding count");
  requireEqual(roomRScene.runtime_policy.raw_overlay_is_diagnostic_only, true, "RoomR fixture overlay policy");
  requireEqual(roomRScene.runtime_policy.raw_types_are_not_furniture_data_ids, true, "RoomR fixture identity policy");
  requireEqual(roomRScene.runtime_policy.native_wall_door_coordinate_composition_not_implied, true, "RoomR fixture raw-overlay policy");
  requireEqual(roomRScene.door_cells.map((cell) => `${cell.x},${cell.y}`).join(","), "8,3", "RoomR fixture door cell");
  requireEqual(defaultMap.scene_ref, "room:0", "DefaultMapChip scene ref");
  requireEqual(defaultMap.room.width, 14, "DefaultMapChip room width");
  requireEqual(defaultMap.room.height, 14, "DefaultMapChip room height");
  requireEqual(defaultMap.room.floor, 0, "DefaultMapChip default floor");
  requireEqual(defaultMap.room.native_floor_img_selector, 23, "DefaultMapChip native floor selector");
  requireEqual(defaultMap.room.native_floor_filename, "floor_05.png", "DefaultMapChip native floor filename");
  requireEqual(defaultMap.room.resolved_floor_img_selector, 85, "DefaultMapChip runtime floor selector");
  requireEqual(defaultMap.room.resolved_floor_filename, "floor_05.png", "DefaultMapChip runtime render floor filename");
  requireEqual(defaultMap.room.resolved_floor_metadata_filename, "floor_09.png", "DefaultMapChip runtime metadata floor filename");
  requireEqual(defaultMap.room.floor_resolution_status, "explicit_fallback_with_floor05_render_asset", "DefaultMapChip floor resolution status");
  const floorFallback = roomPlacement.selectors.floor.runtime_fallback;
  if (!floorFallback) {
    throw new Error("RoomPlacement floor fallback is required");
  }
  requireEqual(defaultMap.floor_selector_remap.raw_room_data_floor_id, roomPlacement.selectors.floor.raw_selector_id, "DefaultMapChip raw floor selector");
  requireEqual(defaultMap.floor_selector_remap.native_image_selector, 23, "DefaultMapChip native floor lookup selector");
  requireEqual(defaultMap.floor_selector_remap.native_filename, "floor_05.png", "DefaultMapChip native floor lookup filename");
  requireEqual(defaultMap.floor_selector_remap.runtime_selector_id, floorFallback.target_selector_id, "DefaultMapChip runtime floor fallback selector");
  requireEqual(defaultMap.floor_selector_remap.runtime_filename, floorFallback.filename, "DefaultMapChip runtime floor fallback filename");
  requireEqual(defaultMap.floor_selector_remap.runtime_resolution_status, roomPlacement.selectors.floor.runtime_resolution_status, "DefaultMapChip runtime floor fallback status");
  requireEqual(defaultMap.floor_selector_remap.runtime_resolution_mode, floorFallback.resolution_mode, "DefaultMapChip runtime floor fallback mode");
  requireEqual(defaultMap.floor_selector_remap.runtime_reason_code, floorFallback.reason_code, "DefaultMapChip runtime floor fallback reason");
  requireEqual(defaultMap.floor_selector_remap.runtime_decision, floorFallback.decision, "DefaultMapChip runtime floor fallback decision");
  requireEqual(defaultMap.raw_index_to_selector["1"]?.selector_id, floorFallback.target_selector_id, "DefaultMapChip raw floor-cell selector");
  requireEqual(defaultMap.raw_index_to_selector["1"]?.filename, defaultMap.floor_selector_remap.runtime_render_filename, "DefaultMapChip raw floor-cell render filename");
  requireEqual(defaultMap.raw_index_to_selector["1"]?.asset_id, "map:chip/floor_05.png", "DefaultMapChip raw floor-cell render asset");
  const floorAsset = defaultMap.source_assets.files[defaultMap.floor_selector_remap.runtime_render_filename];
  if (!floorAsset) {
    throw new Error(`DefaultMapChip is missing runtime render floor asset ${defaultMap.floor_selector_remap.runtime_render_filename}`);
  }
  requireEqual(floorAsset.sha256, defaultMap.floor_selector_remap.runtime_render_asset_sha256, "DefaultMapChip runtime render floor asset hash");
  requireEqual(defaultMap.floor_selector_remap.runtime_render_filename, "floor_05.png", "DefaultMapChip runtime render floor filename");
  requireEqual(defaultMap.floor_selector_remap.runtime_render_resolution_mode, "explicit_user_approved_visual_asset_with_runtime_selector_alias", "DefaultMapChip runtime render resolution mode");
  requireEqual(defaultMap.floor_selector_remap.runtime_render_source_status, "synthetic_not_native_recovery", "DefaultMapChip runtime render source status");
  requireEqual(defaultMap.native_static_arrays.map_chip_array_by_floor.floor_0.length, 196, "DefaultMapChip floor-0 array length");
  requireEqual(defaultMap.native_static_arrays.map_chip_array_by_floor.floor_0.rows.length, 14, "DefaultMapChip floor-0 row count");
  requireEqual(
    Object.keys(defaultMap.extension_wall.frame_records).sort().join(","),
    "0,1,2,3",
    "DefaultMapChip extension wall SEB frame coverage",
  );
  for (const [groupId, group] of Object.entries(defaultMap.extension_wall.composition_groups)) {
    requireEqual(group.draw_call_count, 2, `DefaultMapChip extension group ${groupId} draw count`);
    requireEqual(group.piece_offsets.length, 2, `DefaultMapChip extension group ${groupId} piece offsets`);
    requireEqual(
      JSON.stringify(group.trigger_cells),
      JSON.stringify(defaultMap.extension_wall.native_predicates[groupId]),
      `DefaultMapChip extension group ${groupId} native predicate cells`,
    );
    const frameUsage = defaultMap.extension_wall.frame_usage[group.frame_id];
    if (!frameUsage) {
      throw new Error(`DefaultMapChip extension group ${groupId} has no frame usage record`);
    }
    requireEqual(
      frameUsage.floor00_status,
      group.frame_id === "0" || group.frame_id === "1"
        ? group.frame_id === "0" ? "selected_horizontal_extension_triggers" : "selected_vertical_extension_triggers"
        : "retained_not_selected_by_floor00_extension_path",
      `DefaultMapChip extension frame ${group.frame_id} usage status`,
    );
  }
  for (const frameId of ["2", "3"]) {
    requireEqual(
      defaultMap.extension_wall.frame_usage[frameId]?.floor00_status,
      "retained_not_selected_by_floor00_extension_path",
      `DefaultMapChip extension retained frame ${frameId} status`,
    );
  }
  requireEqual(defaultMap.draw_contract.floor_image_culling.native_method, "MapChip.DrawFloor@0x12A1F38", "DefaultMapChip floor culling method");
  requireEqual(defaultMap.draw_contract.floor_image_culling.x_inclusive.join(","), "5,9", "DefaultMapChip floor culling x bounds");
  requireEqual(defaultMap.draw_contract.floor_image_culling.y_inclusive.join(","), "5,8", "DefaultMapChip floor culling y bounds");
  requireEqual(defaultMap.draw_contract.object_grid_is_separate, true, "DefaultMapChip object/map grid separation");
  requireEqual(nativeContent.catalog_id, "display-slice-01", "NativeContentCatalog id");
  requireEqual(nativeContent.counts.data_records, 3693, "NativeContentCatalog data record count");
  requireEqual(nativeContent.counts.assets, 3542, "NativeContentCatalog asset count");
  requireEqual(nativeContent.counts.selectors, 3192, "NativeContentCatalog selector count");
  requireEqual(assetMetadataRuntime.counts.runtime_assets, 186, "AssetMetadataRuntime runtime asset count");
  requireEqual(assetMetadataRuntime.counts.families, 27, "AssetMetadataRuntime family count");
  requireEqual(assetMetadataRuntime.lazy_loading.eager_load_full_catalog, false, "AssetMetadataRuntime lazy policy");
  requireEqual(assetMetadataRuntime.lazy_loading.source_archive_imports, false, "AssetMetadataRuntime archive import policy");
  requireEqual(assetMetadataRuntime.lazy_loading.source_code_imports, false, "AssetMetadataRuntime source import policy");
  requireEqual(nativeAssembly.catalog_id, "display-slice-01", "NativeSceneAssembly catalog id");
  requireEqual(nativeAssembly.counts.rooms, 18, "NativeSceneAssembly room count");
  requireEqual(nativeAssembly.counts.objchip_cells, 1800, "NativeSceneAssembly ObjChip count");
  requireEqual(nativeAssembly.counts.wall_compositions_closed, 18, "NativeSceneAssembly wall count");
  requireEqual(nativeAssembly.counts.door_compositions_closed, 18, "NativeSceneAssembly door count");
  requireEqual(nativeAssembly.direction.status, "closed_native_vector_and_reverse_mapping", "NativeSceneAssembly direction status");
  requireEqual(nativeAssembly.rooms.length, roomSceneRuntime.rooms.length, "NativeSceneAssembly room coverage");
  for (const room of nativeAssembly.rooms) {
    requireEqual(room.objchip_grid.cell_count, 100, `NativeSceneAssembly ${room.room_key} ObjChip cell count`);
    requireEqual(room.map_chip.selected_variant, "floor_0", `NativeSceneAssembly ${room.room_key} MapChip variant`);
    requireEqual(room.wall.status, "approved_native_coordinate_composition", `NativeSceneAssembly ${room.room_key} wall status`);
    requireEqual(room.door.status, "approved_native_coordinate_composition", `NativeSceneAssembly ${room.room_key} door status`);
    for (const frameId of ["vertical_frame_1", "horizontal_frame_0"] as const) {
      const layers = room.wall.sprite_layers[frameId];
      if (!layers || layers.length !== 2 || layers.map((record) => record.layer).join(",") !== "0,1") {
        throw new Error(`NativeSceneAssembly ${room.room_key} wall ${frameId} must retain both SEB layers in native order`);
      }
      const thinLayer = layers[1];
      if (thinLayer.width !== 2 || thinLayer.height !== 43 || thinLayer.destination_y !== -34) {
        throw new Error(`NativeSceneAssembly ${room.room_key} wall ${frameId} thin layer crop/offset is not the decoded wall_00 contract`);
      }
      const compatibility = room.wall.sprite_records[frameId];
      for (const key of ["start_frame", "image_id", "source_x", "source_y", "width", "height", "destination_x", "destination_y", "flags", "reserved"] as const) {
        if (compatibility[key] !== layers[0][key]) {
          throw new Error(`NativeSceneAssembly ${room.room_key} wall ${frameId} compatibility record diverges from layer 0 at ${key}`);
        }
      }
    }
    requireEqual(
      room.wall.draw_semantics.native_method,
      "ObjChip.DrawWall -> AppData.DrawSeb(frame, lineNo=-1)",
      `NativeSceneAssembly ${room.room_key} wall DrawSeb semantics`,
    );
    if (room.door.cells.length !== 1 || room.door.furniture_data !== null) {
      throw new Error(`NativeSceneAssembly ${room.room_key} door binding is invalid`);
    }
    if (room.selectors.wall.runtime_path.length === 0 || room.selectors.door.runtime_path.length === 0) {
      throw new Error(`NativeSceneAssembly ${room.room_key} selector asset connection is missing`);
    }
  }
  requireEqual(floor00.catalog_id, "floor00-native-bootstrap", "Floor00 catalog id");
  requireEqual(floor00.scene_ref.id, "room:0", "Floor00 scene ref");
  requireEqual(floor00.bootstrap.entrypoint, "AppData.NewGame", "Floor00 bootstrap entrypoint");
  requireEqual(floor00.bootstrap.room_data_key, "data:room:0", "Floor00 RoomData key");
  requireEqual(floor00.bootstrap.room_constructor.width, 14, "Floor00 room constructor width");
  requireEqual(floor00.bootstrap.room_constructor.height, 14, "Floor00 room constructor height");
  requireEqual(floor00.bootstrap.room_constructor.floor, 0, "Floor00 room constructor floor");
  requireEqual(floor00.bootstrap.room_constructor.is_preview, false, "Floor00 room constructor preview flag");
  requireEqual(floor00.bootstrap.initial_staff_count, spawn.actors.length, "Floor00 initial staff count");
  const floor00Room = nativeAssembly.rooms.find((room) => room.room_key === "room:0");
  if (!floor00Room) {
    throw new Error("NativeSceneAssembly does not contain room:0 for Floor00");
  }
  requireEqual(floor00.map.map_chip_variant, floor00Room.map_chip.selected_variant, "Floor00 MapChip variant");
  requireEqual(floor00.map.map_chip_cells, defaultMap.native_static_arrays.map_chip_array_by_floor.floor_0.length, "Floor00 MapChip cell count");
  requireEqual(floor00.map.obj_chip_cells, floor00Room.objchip_grid.cell_count, "Floor00 ObjChip cell count");
  const rawTypeCounts: Record<string, number> = {};
  for (const cell of floor00Room.object_cells) {
    const key = String(cell.raw_type);
    rawTypeCounts[key] = (rawTypeCounts[key] ?? 0) + 1;
  }
  requireEqual(JSON.stringify(floor00.map.raw_type_counts), JSON.stringify(rawTypeCounts), "Floor00 raw ObjChip type counts");
  const type4Cells = floor00Room.object_cells.filter((cell) => cell.raw_type === 4);
  requireEqual(floor00.structural_facilities.length, type4Cells.length, "Floor00 structural facility count");
  const displayObjects = (displayAssetManifestJson as unknown as {
    readonly objects: Readonly<Record<string, {
      readonly seb_selector_id: number;
      readonly seb_asset_member: string;
      readonly records: readonly Record<string, unknown>[];
    }>>;
  }).objects;
  const structuralObject = displayObjects["furniture:0"];
  if (!structuralObject || !structuralObject.records[0]) {
    throw new Error("DisplayAssetManifest is missing the approved furniture:0 structural composition");
  }
  const structuralFrame = structuralObject.records[0];
  for (const facility of floor00.structural_facilities) {
    const type4Cell = type4Cells.find((cell) => cell.cell[0] === facility.anchor[0] && cell.cell[1] === facility.anchor[1]);
    if (!type4Cell || facility.raw_type !== 4 || facility.object_id !== "furniture:0") {
      throw new Error(`Floor00 structural facility ${facility.object_id}@${facility.anchor.join(",")} is not a raw type-4 anchor`);
    }
    requireEqual(
      JSON.stringify(facility.map_anchor),
      JSON.stringify([facility.anchor[0], facility.anchor[1] + 3]),
      `Floor00 structural MapChip anchor ${facility.anchor.join(",")}`,
    );
    if (facility.map_anchor[0] < 0 || facility.map_anchor[0] >= floor00Room.map_chip.variant_rows[0].length
      || facility.map_anchor[1] < 0 || facility.map_anchor[1] >= floor00Room.map_chip.variant_rows.length) {
      throw new Error(`Floor00 structural MapChip anchor ${facility.map_anchor.join(",")} is outside the 14x14 map`);
    }
    const expectedFootprint = [-1, 0, 1].flatMap((dy) => [-1, 0, 1].map((dx) => [facility.anchor[0] + dx, facility.anchor[1] + dy]));
    requireEqual(JSON.stringify(facility.footprint_cells), JSON.stringify(expectedFootprint), `Floor00 structural footprint ${facility.anchor.join(",")}`);
    for (const cell of facility.footprint_cells) {
      const footprintCell = floor00Room.object_cells.find((candidate) => candidate.cell[0] === cell[0] && candidate.cell[1] === cell[1]);
      if (!footprintCell || (cell[0] === facility.anchor[0] && cell[1] === facility.anchor[1] ? footprintCell.raw_type !== 4 : footprintCell.raw_type !== 3)) {
        throw new Error(`Floor00 structural footprint cell ${cell.join(",")} is not the verified type-4/type-3 parent footprint`);
      }
    }
    requireEqual(facility.seb_selector_id, structuralObject.seb_selector_id, `Floor00 structural SEB selector ${facility.anchor.join(",")}`);
    requireEqual(facility.seb_filename, structuralObject.seb_asset_member.split("/").pop(), `Floor00 structural SEB filename ${facility.anchor.join(",")}`);
    requireEqual(facility.image_asset_id, structuralFrame.runtime_asset_id ?? structuralFrame.source_asset_id, `Floor00 structural PNG asset ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.start_frame, structuralFrame.start_frame, `Floor00 structural frame ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.source_x, structuralFrame.source_x, `Floor00 structural source x ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.source_y, structuralFrame.source_y, `Floor00 structural source y ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.width, structuralFrame.width, `Floor00 structural source width ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.height, structuralFrame.height, `Floor00 structural source height ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.destination_x, structuralFrame.destination_x, `Floor00 structural destination x ${facility.anchor.join(",")}`);
    requireEqual(facility.sprite_record.destination_y, structuralFrame.destination_y, `Floor00 structural destination y ${facility.anchor.join(",")}`);
    requireEqual(facility.render_policy, "static_single_frame_structural_composition", `Floor00 structural render policy ${facility.anchor.join(",")}`);
  }
  requireEqual(
    JSON.stringify(floor00.native_initial_furniture.map((item) => `${item.object_id}@${item.cell[0]}:${item.cell[1]}`)),
    JSON.stringify(strictClosure.native_initial_bindings.map((item) => `${item.object_id}@${item.cell[0]}:${item.cell[1]}`)),
    "Floor00 native furniture matrix",
  );
  requireEqual(floor00.native_initial_furniture.length, strictClosure.native_initial_bindings.length, "Floor00 native furniture count");
  requireEqual(JSON.stringify(floor00.door.cell), JSON.stringify([8, 4]), "Floor00 door cell");
  requireEqual(floor00.door.raw_type, 5, "Floor00 door raw type");
  requireEqual(floor00.door.installed_flag, 1, "Floor00 door installed flag");
  requireEqual(floor00.door.furniture_data, null, "Floor00 door FurnitureData binding");
  requireEqual(floor00.render_composition.status, "approved_native_runtime_composition", "Floor00 render composition status");
  requireEqual(floor00.render_composition.native_pass_slots_preserved, true, "Floor00 native pass slots");
  requireEqual(floor00.render_composition.native_cell_order, "row_y_ascending_then_x_descending", "Floor00 native cell order");
  requireEqual(
    floor00.render_composition.logical_order.join(","),
    "background,map-chip-and-map-floor-underlay,map-extension-floor-pale-boundary,object-chip-wall-rear-door-and-wall,object-chip-primary-native-furniture,avatar-primary-static-floor00-display-actors,object-chip-late-foreground-wall,diagnostic-overlay",
    "Floor00 logical render order",
  );
  requireEqual(JSON.stringify(floor00.render_composition.door_cell), JSON.stringify(floor00.door.cell), "Floor00 composition door cell");
  requireEqual(JSON.stringify(floor00.render_composition.foreground_wall_cells), JSON.stringify([[8, 7], [8, 8]]), "Floor00 foreground wall cells");
  requireEqual(floor00.render_composition.underlay_committed_before_objects, true, "Floor00 underlay ordering");
  requireEqual(floor00.render_composition.wall_boundary_asset, "wall_01.png", "Floor00 boundary wall asset");
  requireEqual(floor00.render_composition.wall_boundary_collision, "boundary_wall_not_passable", "Floor00 boundary wall collision");
  requireEqual(
    JSON.stringify(floor00.actors.map((actor) => actor.id)),
    JSON.stringify(spawn.actors.map((actor) => actor.id)),
    "Floor00 actor spawn ids",
  );
  requireEqual(floor00.actors.length, 3, "Floor00 actor spawn count");
  requireEqual(floor00DisplayPolicy.catalog_id, "floor00-static-display-policy", "Floor00 display policy id");
  requireEqual(floor00DisplayPolicy.scene_ref.id, "room:0", "Floor00 display policy scene ref");
  requireEqual(floor00DisplayPolicy.policy.placement_mode, "reserved_empty_walkable_cells", "Floor00 display placement mode");
  requireEqual(floor00DisplayPolicy.policy.simulation_mode, "static_idle", "Floor00 display simulation mode");
  requireEqual(floor00DisplayPolicy.policy.native_spawn_contract_preserved, true, "Floor00 native spawn preservation");
  requireEqual(floor00DisplayPolicy.actors.length, floor00.actors.length, "Floor00 display actor count");
  const floor00ReservedCells = new Set<string>();
  const floor00FurnitureCells = new Set(floor00.native_initial_furniture.map((item) => item.cell.join(",")));
  const floor00RoomDoorCell = floor00.door.cell.join(",");
  for (const displayActor of floor00DisplayPolicy.actors) {
    if (!floor00.actors.some((actor) => actor.id === displayActor.id)) {
      throw new Error(`Floor00 display policy references unknown actor ${displayActor.id}`);
    }
    const cellKey = displayActor.reserved_cell.join(",");
    if (floor00ReservedCells.has(cellKey)) {
      throw new Error(`Floor00 display policy reuses reserved cell ${cellKey}`);
    }
    floor00ReservedCells.add(cellKey);
    if (floor00FurnitureCells.has(cellKey) || cellKey === floor00RoomDoorCell) {
      throw new Error(`Floor00 display policy reserves occupied cell ${cellKey}`);
    }
    const rawCell = floor00Room.object_cells.find((cell) => cell.cell[0] === displayActor.reserved_cell[0] && cell.cell[1] === displayActor.reserved_cell[1]);
    if (!rawCell || rawCell.raw_type !== 0 || displayActor.raw_type !== 0 || displayActor.cell_status !== "verified_empty_walkable") {
      throw new Error(`Floor00 display policy cell ${cellKey} is not a verified empty walkable cell`);
    }
  }
  requireEqual(strictClosure.native_initial_bindings.length, 6, "Phase3C strict native initial binding count");
  requireEqual(
    strictClosure.native_initial_bindings.map((binding) => binding.object_id).join(","),
    "furniture:3,furniture:3,furniture:3,furniture:12,furniture:26,furniture:56",
    "Phase3C strict native initial binding order",
  );
  requireEqual(
    render3c.native_initial_bindings.map((binding) => `${binding.object_id}@${binding.cell[0]}:${binding.cell[1]}`).join(","),
    strictClosure.native_initial_bindings.map((binding) => `${binding.object_id}@${binding.cell[0]}:${binding.cell[1]}`).join(","),
    "Phase3C render/native initial binding matrix",
  );
  requireEqual(render3c.scene_ref.id, "room:0", "Phase3C render scene ref");
  requireEqual(render3c.scene_ref.contract_hash, scene.determinism?.contract_hash, "Phase3C render scene contract hash");
  requireEqual(render3c.room_placement_ref.contract_hash, roomPlacement.determinism?.contract_hash, "Phase3C render room contract hash");
  requireEqual(render3c.object_catalog_ref.contract_hash, objects.determinism?.contract_hash, "Phase3C render object contract hash");
  requireEqual(render3c.camera_coordinate_ref.contract_hash, camera.determinism?.contract_hash, "Phase3C render camera contract hash");
  requireEqual(render3c.display_asset_manifest_ref.content_hash, (displayAssetManifestJson as { determinism?: { content_hash?: string } }).determinism?.content_hash, "Phase3C render display manifest hash");
  requireEqual(render3c.overlap_fixture.expected_event_order.join(","), "door-object,floor-image", "Phase3C render overlap order");
  requireEqual(render3c.runtime_policy.allow_native_furniture_id_inference, false, "Phase3C native furniture inference");
  requireEqual(render3c.runtime_policy.approved_not_placed_objects_are_not_drawn, true, "Phase3C unplaced object policy");
  requireEqual(roomPlacement.scene_ref.contract_hash, scene.determinism?.contract_hash, "RoomPlacement scene contract hash");
  requireEqual(roomPlacement.object_catalog_ref.contract_hash, objects.determinism?.contract_hash, "RoomPlacement object contract hash");
  requireEqual(roomPlacement.camera_coordinate_ref.contract_hash, camera.determinism?.contract_hash, "RoomPlacement camera contract hash");
  requireEqual(
    roomPlacement.display_asset_manifest_ref.status,
    "pass",
    "RoomPlacement display asset manifest status",
  );
  requireEqual(roomPlacement.native_placement.door.cell.x, 8, "RoomPlacement door x");
  requireEqual(roomPlacement.native_placement.door.cell.y, 4, "RoomPlacement door y");
  requireEqual(roomPlacement.native_placement.door.raw_type, 5, "RoomPlacement door raw type");
  requireEqual(roomPlacement.native_placement.door.place_obj_furniture_data, null, "RoomPlacement native door FurnitureData");
  requireEqual(roomPlacement.selectors.floor.resolution_status, "unresolved", "RoomPlacement source floor selector");
  requireEqual(roomPlacement.selectors.floor.runtime_resolution_status, "explicit_fallback", "RoomPlacement floor fallback status");
  requireEqual(roomPlacement.selectors.floor.runtime_fallback?.target_selector_id, 85, "RoomPlacement floor fallback selector");
  requireEqual(roomPlacement.selectors.floor.runtime_fallback?.filename, "floor_09.png", "RoomPlacement floor fallback asset");
  requireEqual(roomPlacement.object_boundary.runtime_policy.promote_furniture_2, true, "RoomPlacement furniture:2 display approval");
  requireEqual(roomPlacement.runtime_policy.source_code_imports, false, "RoomPlacement source imports");
  requireEqual(roomPlacement.runtime_policy.archive_imports, false, "RoomPlacement archive imports");
  requireEqual(roomPlacement.runtime_policy.unapproved_binary_imports, false, "RoomPlacement binary imports");
  requireEqual(spawn.fixture_ref.content_hash, spawnFixture.determinism.content_hash, "ActorSpawn fixture hash");
  requireEqual(
    actors.fixture_ref.content_hash,
    actorCatalogJson.fixture_ref.content_hash,
    "ActorCatalog fixture hash",
  );
  requireEqual(camera.coordinate_system.grid.width, 10, "Camera grid width");
  requireEqual(camera.coordinate_system.grid.height, 10, "Camera grid height");
  requireEqual(tickOrder.mutation_policy.renderer_may_mutate, false, "Renderer mutation policy");
  requireEqual(tickOrder.mutation_policy.ui_may_mutate, false, "UI mutation policy");

  const displayScene = scene.scenes.find((candidate) => candidate.id === "room:0");
  if (!displayScene) {
    throw new Error("SceneCatalog does not contain room:0");
  }

  const actorIds = new Set(actors.actors.map((actor) => actor.id));
  const activeActors = spawnFixture.actors.filter((actor) => actorIds.has(actor.id));
  if (activeActors.length !== spawnFixture.actors.length || activeActors.length < 3) {
    throw new Error("ActorSpawn fixture contains an actor outside ActorCatalog");
  }

  return {
    scene,
    objects,
    actors,
    characterCapabilities,
    characterAssets,
    characterMetadata,
    spawn,
    spawnFixture,
    camera,
    defaultMap,
    roomPlacement,
    render3c,
    strictClosure,
    behavior,
    tickOrder,
    preRuntime,
    roomSceneRuntime,
    nativeDirection,
    roomSceneAssets,
    roomRScene,
    nativeContent,
    nativeAssembly,
    nativeRoomFloorUsage,
    floor00,
    floor00DisplayPolicy,
    floor00VisualLayout,
    assetMetadataRuntime,
    displayScene,
    activeActors,
  };
}
