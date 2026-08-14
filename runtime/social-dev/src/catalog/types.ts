export type Locale = "English" | "Japanese";

export interface ContractHeader {
  readonly schema_version: string;
  readonly package: string;
  readonly status: string;
  readonly semantic_status?: string;
  readonly determinism?: {
    readonly contract_hash?: string;
    readonly content_hash?: string;
  };
}

export interface GridContract {
  readonly width: number;
  readonly height: number;
  readonly objMap: readonly (readonly number[])[];
  readonly objDir: readonly (readonly number[])[];
}

export interface SceneRecord {
  readonly id: string;
  readonly name: Readonly<Record<Locale, string>>;
  readonly grid: GridContract;
  readonly door?: {
    readonly cells: readonly { readonly x: number; readonly y: number }[];
  };
  readonly type4_fixture?: {
    readonly anchor: { readonly x: number; readonly y: number };
  };
}

export interface SceneCatalogContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scenes: readonly SceneRecord[];
}

export interface SelectorRecord {
  readonly id: number;
  readonly status: string;
  readonly resolution_status: string;
  readonly filename?: string;
  readonly asset_member?: string;
  readonly asset_index?: {
    readonly relative_path?: string;
    readonly width?: string;
    readonly height?: string;
    readonly format?: string;
  };
}

export interface ObjectRecord {
  readonly id: string;
  readonly source_identity: {
    readonly source_id: number;
  };
  readonly name: {
    readonly values: Readonly<Record<Locale, string>>;
  };
  readonly selectors: Readonly<Record<string, SelectorRecord>>;
  readonly status: string;
}

export interface ObjectBinding {
  readonly id: string;
  readonly cell?:
    | { readonly x: number; readonly y: number; readonly raw_map_value?: number; readonly raw_dir_value?: number }
    | readonly number[];
  readonly status: string;
  readonly [key: string]: unknown;
}

export interface RawObjectType {
  readonly id: string;
  readonly raw_type: number;
  readonly source_constant?: {
    readonly name: string;
    readonly value: number;
  };
  readonly scene_cell_count?: number;
}

export interface ObjectCatalogContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: { readonly id: string };
  readonly objects: readonly ObjectRecord[];
  readonly raw_object_types: readonly RawObjectType[];
  readonly scene_bindings: readonly ObjectBinding[];
}

export interface ActorRecord {
  readonly id: string;
  readonly source_identity: {
    readonly source_id: number;
  };
  readonly name: {
    readonly values: Readonly<Record<Locale, string>>;
  };
  readonly portrait_selector: SelectorRecord;
  readonly animation_profile_ref: { readonly id: string };
  readonly behavior_profile_ref: { readonly id: string };
  readonly status: string;
}

export interface AnimationDirection {
  readonly wait: {
    readonly seb_id: number;
    readonly status: string;
    readonly filename?: string;
  };
  readonly typing: {
    readonly seb_id: number;
    readonly status: string;
    readonly filename?: string;
  };
  readonly [key: string]: unknown;
}

export interface AnimationProfile {
  readonly id: string;
  readonly directions: readonly AnimationDirection[];
  readonly typing_rules?: {
    readonly start?: Record<string, unknown>;
    readonly end?: Record<string, unknown>;
  };
}

export interface BehaviorProfile {
  readonly id: string;
  readonly route_mapping?: Record<string, unknown>;
  readonly transitions?: readonly Record<string, unknown>[];
  readonly animation_timing?: Record<string, unknown>;
  readonly talk_timing?: {
    readonly frame_markers: readonly number[];
    readonly terminal_effect?: string;
  };
}

export interface ActorCatalogContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: { readonly id: string };
  readonly actors: readonly ActorRecord[];
  readonly animation_profiles: readonly AnimationProfile[];
  readonly behavior_profiles: readonly BehaviorProfile[];
  readonly fixture_ref: {
    readonly path: string;
    readonly content_hash: string;
  };
  readonly runtime_readiness?: {
    readonly status: string;
    readonly required_before_runtime?: readonly string[];
  };
}

export interface CharacterMetadataField {
  readonly value: unknown;
  readonly status: string;
  readonly semantic_status: string;
  readonly runtime_usage: string;
  readonly source_field: string;
  readonly reader: string;
  readonly token_range: readonly number[];
  readonly mapping_status: string;
  readonly confidence: string;
  readonly review_note: string;
}

export interface CharacterMetadataSelector {
  readonly id: number;
  readonly field: string;
  readonly status: string;
  readonly resolution_status: string;
  readonly reference?: string;
  readonly connection_status?: string;
  readonly asset?: {
    readonly asset_id: string;
    readonly member: string;
    readonly filename?: string;
    readonly sha256?: string;
    readonly width?: number;
    readonly height?: number;
    readonly [key: string]: unknown;
  };
  readonly [key: string]: unknown;
}

export interface CharacterMetadataRecord {
  readonly id: string;
  readonly record_kind?: string;
  readonly status: string;
  readonly semantic_status: string;
  readonly source_identity: {
    readonly type: string;
    readonly source_id: number;
  };
  readonly name: {
    readonly values: Readonly<Record<Locale, string>>;
  };
  readonly source_fields: Readonly<Record<string, unknown>>;
  readonly render?: {
    readonly family: string;
    readonly image_selector?: CharacterMetadataSelector;
    readonly big_image_selector?: CharacterMetadataSelector;
    readonly animation_profile_ref?: string;
    readonly capability_profile_ref?: string;
    readonly behavior_profile_ref?: string;
    readonly [key: string]: unknown;
  };
  readonly relations?: Readonly<Record<string, {
    readonly id: string;
    readonly source_id: number;
    readonly status: string;
    readonly semantic_status: string;
  }>>;
  readonly [key: string]: unknown;
}

export interface CharacterMetadataContract extends ContractHeader {
  readonly catalog_id: string;
  readonly staff: readonly CharacterMetadataRecord[];
  readonly helpers: readonly CharacterMetadataRecord[];
  readonly jobs: readonly CharacterMetadataRecord[];
  readonly skills: readonly CharacterMetadataRecord[];
  readonly counts: Readonly<Record<string, number>>;
  readonly runtime_state_boundary: {
    readonly mutable_actor_state_owner: string;
    readonly mutable_actor_state_fields: readonly string[];
    readonly [key: string]: unknown;
  };
  readonly runtime_readiness?: {
    readonly status: string;
    readonly instance_creation: string;
    readonly asset_loading: string;
    readonly [key: string]: unknown;
  };
}

export interface CharacterCapabilitySelector {
  readonly selector_id: number;
  readonly selector_key: string;
  readonly filename: string;
  readonly asset_id: string;
  readonly asset_member: string;
  readonly status: string;
  readonly resolution_status: string;
  readonly source_file: string;
  readonly source_row: number;
}

export interface CharacterActionCapability {
  readonly status: string;
  readonly semantic_status: string;
  readonly source_action?: string;
  readonly fallback_action?: string;
  readonly selector?: CharacterCapabilitySelector | null;
  readonly selector_by_direction?: Readonly<Record<string, CharacterCapabilitySelector>> | null;
  readonly asset_loading?: string;
  readonly frame_resolution_status?: string;
  readonly note?: string;
  readonly [key: string]: unknown;
}

export interface CharacterCapabilityProfile {
  readonly id: string;
  readonly family: string;
  readonly role: string;
  readonly status: string;
  readonly semantic_status: string;
  readonly record_kinds: readonly string[];
  readonly behavior: {
    readonly profile_ref: string | null;
    readonly status: string;
    readonly contract_ref?: {
      readonly path: string;
      readonly sha256: string;
    };
    readonly [key: string]: unknown;
  };
  readonly directions: readonly string[];
  readonly actions: Readonly<Record<string, CharacterActionCapability>>;
  readonly native_actions?: Readonly<Record<string, CharacterActionCapability>>;
  readonly [key: string]: unknown;
}

export interface CharacterCapabilityBinding {
  readonly record_id: string;
  readonly source_id: number;
  readonly record_kind: string;
  readonly profile_ref: string;
  readonly behavior_profile_ref: string | null;
  readonly status: string;
  readonly image_resolution_status: string;
  readonly optional_override: Record<string, unknown> | null;
}

export interface CharacterCapabilityContract extends ContractHeader {
  readonly catalog_id: string;
  readonly profiles: readonly CharacterCapabilityProfile[];
  readonly bindings: {
    readonly staff: readonly CharacterCapabilityBinding[];
    readonly helpers: readonly CharacterCapabilityBinding[];
  };
  readonly native_selector_inventory: readonly CharacterCapabilitySelector[];
  readonly runtime_policy: {
    readonly template_lookup: string;
    readonly instance_creation: string;
    readonly animation_resolution: string;
    readonly per_character_customization: string;
    readonly unsupported_action_policy: string;
    readonly asset_loading: string;
    readonly source_code_imports: boolean;
    readonly [key: string]: unknown;
  };
  readonly counts: Readonly<Record<string, number>>;
  readonly fixture_ref: {
    readonly path: string;
    readonly content_hash: string;
  };
  readonly [key: string]: unknown;
}

export interface CharacterAssetImage {
  readonly selector_id: number;
  readonly filename: string;
  readonly asset_id: string;
  readonly asset_member: string;
  readonly runtime_path: string;
  readonly source_sha256: string;
  readonly runtime_sha256: string;
  readonly bytes: number;
  readonly status: string;
  readonly source_status: string;
  readonly dimensions: {
    readonly width: number;
    readonly height: number;
    readonly mode: string;
  };
}

export interface CharacterAssetFrameRecord {
  readonly layer: number;
  readonly layer_record_index: number;
  readonly start_frame: number;
  readonly image_id: number;
  readonly image_id_raw: number;
  readonly source_x: number;
  readonly source_y: number;
  readonly width: number;
  readonly height: number;
  readonly destination_x: number;
  readonly destination_y: number;
  readonly flags: number;
  readonly reserved: number;
  readonly texture_status: string;
  readonly source_asset_member: string | null;
  readonly source_asset_id: string | null;
  readonly source_size?: {
    readonly width: number;
    readonly height: number;
  };
}

export interface CharacterAssetLayer {
  readonly index: number;
  readonly record_count: number;
  readonly frame_bound: number;
  readonly marker: {
    readonly record_count: number;
    readonly raw_value: number;
  } | null;
  readonly records: readonly CharacterAssetFrameRecord[];
}

export interface CharacterAssetAnimation {
  readonly selector_id: number;
  readonly filename: string;
  readonly asset_id: string;
  readonly asset_member: string;
  readonly runtime_path: string;
  readonly source_sha256: string;
  readonly runtime_sha256: string;
  readonly bytes: number;
  readonly header: {
    readonly layer_count: number;
    readonly global_frame_count: number;
    readonly record_count: number;
    readonly frame_bound: number;
  };
  readonly layers: readonly CharacterAssetLayer[];
  readonly records: readonly CharacterAssetFrameRecord[];
  readonly control_record_count: number;
  readonly status: string;
  readonly composition_policy: string;
}

export interface CharacterAssetStaffBinding {
  readonly record_id: string;
  readonly source_id: number;
  readonly record_kind: string;
  readonly capability_profile_ref: string;
  readonly image_selector_id: number;
  readonly image_asset_id: string;
  readonly image_asset_member: string;
  readonly runtime_path: string;
  readonly status: string;
}

export interface CharacterAssetManifest extends ContractHeader {
  readonly catalog_id: string;
  readonly images: readonly CharacterAssetImage[];
  readonly animations: readonly CharacterAssetAnimation[];
  readonly staff_bindings: readonly CharacterAssetStaffBinding[];
  readonly runtime_policy: {
    readonly asset_namespace: string;
    readonly image_loading: string;
    readonly frame_resolution: string;
    readonly raw_seb_retained: boolean;
    readonly eager_load_full_catalog: boolean;
    readonly source_archive_imports: boolean;
    readonly source_code_imports: boolean;
    readonly [key: string]: unknown;
  };
  readonly counts: Readonly<Record<string, number>>;
  readonly fixture_ref: {
    readonly path: string;
    readonly content_hash: string;
  };
  readonly [key: string]: unknown;
}

export interface SpawnActorFixture {
  readonly id: string;
  readonly spawn_cell: {
    readonly x: number;
    readonly y: number;
    readonly raw_map_value?: number;
  };
  readonly initial_position: { readonly x: number; readonly y: number };
  readonly initial_fields: Readonly<Record<string, { readonly value: number }>>;
  readonly desk_assignment: { readonly status: string };
}

export interface ActorSpawnFixture extends ContractHeader {
  readonly catalog_id: string;
  readonly actors: readonly SpawnActorFixture[];
  readonly determinism: {
    readonly content_hash: string;
  };
}

export interface ActorSpawnContract extends ContractHeader {
  readonly fixture_ref: { readonly path: string; readonly content_hash: string };
  readonly actors: readonly SpawnActorFixture[];
  readonly spawn_rule: Record<string, unknown>;
}

export interface Floor00FurnitureInstance {
  readonly object_id: string;
  readonly furniture_data_id: number;
  readonly cell: readonly [number, number];
  readonly raw_type: number;
  readonly selector_flag: string;
  readonly scan_order: number;
}

export interface Floor00StructuralFacility {
  readonly object_id: string;
  readonly anchor: readonly [number, number];
  readonly map_anchor: readonly [number, number];
  readonly raw_type: 4;
  readonly footprint_cells: readonly (readonly [number, number])[];
  readonly seb_selector_id: number;
  readonly seb_filename: string;
  readonly image_asset_id: string;
  readonly sprite_record: Record<string, unknown>;
  readonly render_policy: string;
}

export interface Floor00ActorInstance {
  readonly id: string;
  readonly source_staff_id: number;
  readonly spawn_cell: readonly [number, number];
  readonly initial_position: readonly [number, number];
}

export interface Floor00DisplayActor {
  readonly id: string;
  readonly reserved_cell: readonly [number, number];
  readonly raw_type: number;
  readonly cell_status: string;
}

export interface Floor00DisplayPolicyContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: { readonly id: string };
  readonly policy: {
    readonly placement_mode: string;
    readonly simulation_mode: "static_idle";
    readonly native_spawn_contract_preserved: boolean;
    readonly reason: string;
  };
  readonly actors: readonly Floor00DisplayActor[];
  readonly refs: Readonly<Record<string, string>>;
  readonly determinism: {
    readonly algorithm: string;
    readonly hash_basis: string;
    readonly content_hash: string;
  };
}

export interface Floor00SceneContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: { readonly id: string };
  readonly bootstrap: {
    readonly entrypoint: string;
    readonly room_data_key: string;
    readonly room_constructor: {
      readonly width: number;
      readonly height: number;
      readonly floor: number;
      readonly is_preview: boolean;
    };
    readonly place_desk_argument: number;
    readonly initial_staff_count: number;
  };
  readonly map: {
    readonly map_chip_variant: string;
    readonly map_chip_width: number;
    readonly map_chip_height: number;
    readonly map_chip_cells: number;
    readonly obj_chip_width: number;
    readonly obj_chip_height: number;
    readonly obj_chip_cells: number;
    readonly raw_type_counts: Readonly<Record<string, number>>;
  };
  readonly native_initial_furniture: readonly Floor00FurnitureInstance[];
  readonly structural_facilities: readonly Floor00StructuralFacility[];
  readonly door: {
    readonly cell: readonly [number, number];
    readonly raw_type: number;
    readonly installed_flag: number;
    readonly furniture_data: null;
  };
  readonly render_composition: {
    readonly status: string;
    readonly native_pass_slots_preserved: boolean;
    readonly native_cell_order: string;
    readonly logical_order: readonly string[];
    readonly rear_wall_cells: readonly (readonly [number, number])[];
    readonly door_cell: readonly [number, number];
    readonly foreground_wall_cells: readonly (readonly [number, number])[];
    readonly underlay_committed_before_objects: boolean;
    readonly wall_boundary_asset: string;
    readonly wall_boundary_collision: string;
    readonly source_basis: readonly string[];
  };
  readonly actors: readonly Floor00ActorInstance[];
  readonly exclusions: readonly string[];
  readonly refs: Readonly<Record<string, string>>;
  readonly determinism: {
    readonly algorithm: string;
    readonly hash_basis: string;
    readonly content_hash: string;
  };
}

export interface Floor00VisualLayoutContract extends ContractHeader {
  readonly catalog_id: "floor00-visual-layout";
  readonly scene_ref: { readonly id: "room:0"; readonly scene_mode: "floor00" };
  readonly refs: Readonly<Record<string, string>>;
  readonly glass: {
    readonly source_asset_id: "map:chip/wall_01.png";
    readonly frame_ids_by_group: Readonly<Record<string, string>>;
    readonly native_trigger_cells_by_group: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly removed_trigger_cells: readonly (readonly [number, number])[];
    readonly final_trigger_cells_by_group: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly strip_axis: "map_x" | "map_y";
    readonly strip_start: readonly [number, number];
    readonly strip_end: readonly [number, number];
  };
  readonly wood_wall: {
    readonly source_asset_id: "asset:01_GAME_PACKS/chip/wall_00.png";
    readonly source_seb_asset_id: "asset:01_GAME_PACKS/chip/wall_00.seb";
    readonly native_cells_by_frame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly final_cells_by_frame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly moved_group: "green_circled_side";
    readonly backward_offset: readonly [number, number];
    readonly layer_order: readonly [0, 1];
  };
  readonly alignment: {
    readonly upper_edge_cells: readonly (readonly [number, number])[];
    readonly left_edge_cells: readonly (readonly [number, number])[];
    readonly expected_screen_delta: { readonly x: number; readonly y: number };
  };
  readonly determinism: { readonly algorithm: string; readonly content_hash: string };
}

export interface CameraCoordinateContract extends ContractHeader {
  readonly coordinate_system: {
    readonly grid: { readonly width: number; readonly height: number };
    readonly cell_origin: Record<string, unknown>;
    readonly actor_spawn_position: Record<string, unknown>;
  };
  readonly camera: {
    readonly fixture_offset: readonly [number, number];
    readonly fixture_scale: number;
    readonly transform: string;
  };
  readonly draw_offset_contract: Record<string, unknown>;
}

export interface RoomPlacementAssetRef {
  readonly relative_path: string;
  readonly sha256: string;
  readonly size_bytes?: number;
  readonly width?: string;
  readonly height?: string;
  readonly format?: string;
}

export interface RoomPlacementSelector {
  readonly role: string;
  readonly index_name: string;
  readonly raw_selector_id: number;
  readonly resolution_status: string;
  readonly runtime_promotion_status: string;
  readonly runtime_resolution_status?: string;
  readonly filename?: string;
  readonly reason_code?: string;
  readonly reason?: string;
  readonly asset: RoomPlacementAssetRef | null;
  readonly runtime_fallback?: {
    readonly target_selector_id: number;
    readonly filename: string;
    readonly resolution_status: string;
    readonly resolution_mode: string;
    readonly reason_code: string;
    readonly decision: string;
    readonly asset: RoomPlacementAssetRef;
  };
  readonly native_composition?: {
    readonly seb: {
      readonly raw_selector_id: number;
      readonly filename: string;
      readonly asset: RoomPlacementAssetRef;
    };
    readonly image: string;
    readonly status: string;
  };
}

export interface RoomPlacementContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: {
    readonly id: string;
    readonly contract_hash: string;
    readonly status: string;
  };
  readonly object_catalog_ref: {
    readonly contract_hash: string;
    readonly status: string;
  };
  readonly camera_coordinate_ref: {
    readonly contract_hash: string;
    readonly status: string;
  };
  readonly display_asset_manifest_ref: {
    readonly contract_hash?: string;
    readonly status: string;
    readonly semantic_status?: string;
  };
  readonly selectors: Readonly<Record<"floor" | "wall" | "door", RoomPlacementSelector>>;
  readonly native_placement: {
    readonly init_order: readonly string[];
    readonly raw_grid_assignment: {
      readonly source_field: string;
      readonly cell_expression: string;
      readonly constructor: string;
      readonly flat_index: string;
    };
    readonly door: {
      readonly cell: { readonly x: number; readonly y: number; readonly raw_map_value: number; readonly raw_dir_value: number };
      readonly raw_type: number;
      readonly installed_flag: number;
      readonly place_obj_furniture_data: null;
      readonly native_furniture_binding_status: string;
    };
    readonly type4: {
      readonly object_id: string;
      readonly anchor: { readonly x: number; readonly y: number; readonly raw_map_value: number };
      readonly raw_type: number;
      readonly furniture_data_id: number;
      readonly footprint: readonly Record<string, number>[];
      readonly passability: {
        readonly matrix: readonly (readonly boolean[])[];
      };
    };
    readonly route_fixture: {
      readonly path: readonly (readonly number[])[];
      readonly step_count: number;
    };
    readonly route_filter_probes: readonly Record<string, unknown>[];
  };
  readonly object_boundary: {
    readonly approved_display_compositions: readonly string[];
    readonly native_room_bindings: readonly {
      readonly object_id: string;
      readonly status: string;
      readonly cell: readonly number[] | null;
      readonly note: string;
    }[];
    readonly runtime_policy: {
      readonly promote_furniture_2: boolean;
      readonly allow_native_furniture_id_inference: boolean;
      readonly require_explicit_scene_binding: boolean;
    };
  };
  readonly coordinates: {
    readonly cell_origin: {
      readonly formula_x: string;
      readonly formula_y: string;
      readonly probes: readonly { readonly cell: readonly number[]; readonly world: { readonly x: number; readonly y: number } }[];
    };
    readonly actor_spawn: {
      readonly formula_x: string;
      readonly formula_y: string;
      readonly probes: readonly { readonly cell: readonly number[]; readonly world: { readonly x: number; readonly y: number } }[];
    };
    readonly map_chip_draw_origin: {
      readonly formula_x: string;
      readonly formula_y: string;
      readonly probes: readonly { readonly cell: readonly number[]; readonly origin: { readonly x: number; readonly y: number } }[];
    };
    readonly object_draw_origin: {
      readonly formula_x: string;
      readonly formula_y: string;
      readonly probes: readonly { readonly cell: readonly number[]; readonly origin: { readonly x: number; readonly y: number } }[];
    };
    readonly camera: {
      readonly transform: string;
      readonly fixture_offset: readonly [number, number];
      readonly fixture_scale: number;
      readonly dynamic_viewport_status: string;
    };
  };
  readonly draw_order: {
    readonly status: string;
    readonly passes: readonly { readonly id: string; readonly method: string; readonly line: number; readonly layer_role: string }[];
    readonly overlap_fixture: {
      readonly cell: readonly number[];
      readonly expected_event_order: readonly string[];
    };
  };
  readonly runtime_policy: {
    readonly source_code_imports: boolean;
    readonly archive_imports: boolean;
    readonly unapproved_binary_imports: boolean;
    readonly unresolved_selector_policy: string;
    readonly phase3b_asset_promotion: string;
    readonly quarantined_objects_excluded: readonly string[];
  };
}

export interface DefaultMapChipContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: string;
  readonly room: {
    readonly width: number;
    readonly height: number;
    readonly floor: number;
    readonly room_data_floor_img_id: number;
    readonly native_floor_img_selector: number;
    readonly native_floor_filename: string;
    readonly resolved_floor_img_selector: number;
    readonly resolved_floor_filename: string;
    readonly resolved_floor_metadata_filename: string;
    readonly floor_resolution_status: string;
    readonly wall_img_selector: number;
    readonly wall_filename: string;
    readonly door_img_selector: number;
    readonly door_filename: string;
    readonly door_cell: readonly [number, number];
  };
  readonly native_static_arrays: {
    readonly map_chip_image_id_array: { readonly values: readonly number[] };
    readonly floor_image_id_array: { readonly values: readonly number[] };
    readonly map_chip_array_by_floor: {
      readonly floor_0: { readonly length: number; readonly rows: readonly (readonly number[])[] };
      readonly floor_nonzero: { readonly length: number; readonly rows: readonly (readonly number[])[] };
    };
  };
  readonly raw_index_to_selector: Readonly<Record<string, {
    readonly selector_id: number;
    readonly filename: string | null;
    readonly asset_id: string | null;
    readonly meaning: string;
  }>>;
  readonly floor_selector_remap: {
    readonly raw_room_data_floor_id: number;
    readonly native_table_index: number;
    readonly native_image_selector: number;
    readonly native_filename: string;
    readonly source_status: string;
    readonly runtime_selector_id: number;
    readonly runtime_filename: string;
    readonly runtime_resolution_status: string;
    readonly runtime_resolution_mode: string;
    readonly runtime_reason_code: string;
    readonly runtime_decision: string;
    readonly runtime_render_filename: string;
    readonly runtime_render_asset_sha256: string;
    readonly runtime_render_resolution_mode: string;
    readonly runtime_render_source_status: string;
    readonly runtime_render_reason_code: string;
    readonly runtime_render_decision: string;
  };
  readonly extension_wall: {
    readonly seb_selector_id: number;
    readonly seb_filename: string;
    readonly source_image_selector_id: number;
    readonly source_image_filename: string;
    readonly frame_records: Readonly<Record<string, {
      readonly source_x: number;
      readonly source_y: number;
      readonly width: number;
      readonly height: number;
      readonly destination_x: number;
      readonly destination_y: number;
    }>>;
    readonly native_predicates: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly frame_usage: Readonly<Record<string, {
      readonly floor00_status: string;
      readonly native_method: string;
    }>>;
    readonly composition_groups: Readonly<Record<string, {
      readonly frame_id: string;
      readonly trigger_cells: readonly (readonly [number, number])[];
      readonly native_method: string;
      readonly draw_call_count: number;
      readonly piece_offsets: readonly { readonly x: number; readonly y: number }[];
      readonly offset_basis: string;
      readonly continuity: string;
    }>>;
  };
  readonly draw_contract: {
    readonly map_chip_origin: { readonly x: string; readonly y: string };
    readonly map_image_anchor: string;
    readonly native_pass_order: readonly string[];
    readonly floor_image_culling: {
      readonly native_method: string;
      readonly room_dimensions: readonly [number, number];
      readonly x_inclusive: readonly [number, number];
      readonly y_inclusive: readonly [number, number];
      readonly predicate: string;
      readonly source_status: string;
    };
    readonly object_grid_is_separate: boolean;
    readonly object_grid_size: readonly [number, number];
  };
  readonly source_assets: {
    readonly asset_root: string;
    readonly asset_zip_sha256: string;
    readonly files: Readonly<Record<string, { readonly runtime_path: string; readonly width: number; readonly height: number; readonly sha256: string }>>;
    readonly ambient_assets?: Readonly<Record<string, { readonly runtime_path: string; readonly width: number; readonly height: number; readonly sha256: string }>>;
  };
}

export type NativeRoomFloorTopologyVariantId = "floor_0" | "floor_nonzero";

export interface NativeRoomFloorTopologyVariant {
  readonly native_index: number;
  readonly floor_predicate: string;
  readonly width: number;
  readonly height: number;
  readonly length: number;
  readonly rows: readonly (readonly number[])[];
  readonly status: string;
}

export interface NativeRoomFloorUsageRecord {
  readonly usage_id: string;
  readonly roomdata_ids: readonly string[];
  readonly roomdata_id_status: string;
  readonly room_floor_value: number;
  readonly topology_variant: NativeRoomFloorTopologyVariantId;
  readonly width: number;
  readonly height: number;
  readonly is_preview: boolean;
  readonly callers: readonly Record<string, unknown>[];
  readonly status: string;
}

export interface NativeRoomFloorUsageContract extends ContractHeader {
  readonly catalog_id: string;
  readonly content_hash: string;
  readonly native_artifact_ref: {
    readonly apk_sha256: string;
    readonly binary_sha256: string;
    readonly metadata_sha256: string;
    readonly method_ids: readonly string[];
  };
  readonly topology_selection: {
    readonly native_field: string;
    readonly predicate: string;
    readonly variants: Readonly<Record<NativeRoomFloorTopologyVariantId, NativeRoomFloorTopologyVariant>>;
  };
  readonly usage: readonly NativeRoomFloorUsageRecord[];
  readonly roomdata_catalog: {
    readonly room_keys: readonly string[];
    readonly room_count: number;
    readonly floor_image_links: string;
    readonly objchip_grid: string;
  };
  readonly runtime_policy: Readonly<Record<string, unknown>> & {
    readonly roomdata_is_interior_catalog_key: boolean;
    readonly room_floor_is_constructor_key: boolean;
    readonly mapchip_never_inferred_from_objchip: boolean;
    readonly floor_image_table_is_independent_from_mapchip_topology: boolean;
    readonly nonzero_topology_requires_4x4_native_dimensions: boolean;
    readonly unsupported_dimension_combinations_are_rejected: boolean;
    readonly raw_native_floor_value_is_preserved: boolean;
    readonly environment_scope: {
      readonly main_display: {
        readonly topology: string;
        readonly dimensions: string;
        readonly outer_mapchip: string;
      };
      readonly persistent_room: {
        readonly topology: string;
        readonly dimensions: string;
        readonly outer_mapchip: string;
      };
      readonly addition_floor_preview: {
        readonly topology: string;
        readonly dimensions: string;
        readonly outer_mapchip: string;
      };
      readonly non_main_outer_mapchip_policy: string;
    };
  };
  readonly source_evidence: {
    readonly knowledge_catalog: string;
    readonly source_policy: string;
  };
  readonly contract_hash: string;
}

export interface Phase3CRenderPlacement {
  readonly id: string;
  readonly role: "floor" | "wall" | "door" | "object";
  readonly object_id?: string;
  readonly raw_selector_id?: number;
  readonly runtime_asset_id?: string;
  readonly filename?: string;
  readonly status: string;
  readonly binding_status?: string;
  readonly evidence_binding: string;
  readonly cell?: readonly [number, number] | null;
  readonly source_resolution_status?: string;
  readonly runtime_resolution_status?: string;
  readonly runtime_fallback?: {
    readonly target_selector_id: number;
    readonly filename: string;
    readonly resolution_status: string;
    readonly resolution_mode: string;
    readonly reason_code: string;
    readonly decision: string;
    readonly asset: Record<string, unknown>;
  };
  readonly cell_scope?: {
    readonly width: number;
    readonly height: number;
    readonly mode: string;
    readonly cells?: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly anchor_formula?: Readonly<Record<string, string>>;
    readonly sprite_records?: Readonly<Record<string, Record<string, unknown>>>;
    readonly sprite_layers?: Readonly<Record<string, readonly Record<string, unknown>[]>>;
  };
  readonly native_binding_status?: string;
  readonly native_coordinate?: {
    readonly anchor: { readonly x: number; readonly y: number };
    readonly sprite_record: Record<string, unknown>;
  };
}

export interface Phase3CNativeInitialBinding {
  readonly object_id: string;
  readonly furniture_data_id: number;
  readonly name: string;
  readonly native_status: string;
  readonly cell: readonly [number, number];
  readonly raw_type: number;
  readonly scan_order: number;
  readonly selector_flag: {
    readonly name: string;
    readonly value: number;
  };
  readonly count_source: string;
  readonly count_fixture_value?: number;
}

export interface Phase3CStrictClosureContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_id: string;
  readonly native_initial_bindings: readonly Phase3CNativeInitialBinding[];
  readonly determinism: {
    readonly contract_hash: string;
  };
}

export interface Phase3CRenderContract extends ContractHeader {
  readonly catalog_id: string;
  readonly scene_ref: {
    readonly id: string;
    readonly contract_hash?: string;
  };
  readonly room_placement_ref: {
    readonly path: string;
    readonly contract_hash?: string;
    readonly status: string;
  };
  readonly object_catalog_ref: {
    readonly path: string;
    readonly contract_hash?: string;
    readonly status: string;
  };
  readonly camera_coordinate_ref: {
    readonly path: string;
    readonly contract_hash?: string;
    readonly status: string;
  };
  readonly display_asset_manifest_ref: {
    readonly path: string;
    readonly content_hash?: string;
    readonly status: string;
  };
  readonly canvas: {
    readonly width: number;
    readonly height: number;
    readonly presentation_origin: { readonly x: number; readonly y: number };
    readonly presentation_origin_status: string;
  };
  readonly coordinates: {
    readonly cell_origin: Record<string, unknown>;
    readonly actor_spawn: Record<string, unknown>;
    readonly map_chip_draw_origin: Record<string, unknown>;
    readonly object_draw_origin: Record<string, unknown>;
    readonly camera: Record<string, unknown>;
  };
  readonly draw_passes: readonly {
    readonly id: string;
    readonly method: string;
    readonly layer_role: string;
  }[];
  readonly placements: readonly Phase3CRenderPlacement[];
  readonly native_initial_bindings: readonly Phase3CNativeInitialBinding[];
  readonly overlap_fixture: {
    readonly cell: readonly number[];
    readonly events: readonly Record<string, unknown>[];
    readonly expected_event_order: readonly string[];
    readonly assertion: string;
  };
  readonly runtime_policy: {
    readonly source_code_imports: boolean;
    readonly archive_imports: boolean;
    readonly unapproved_binary_imports: boolean;
    readonly allow_native_furniture_id_inference: boolean;
    readonly require_explicit_scene_binding: boolean;
    readonly unresolved_selector_policy: string;
    readonly approved_not_placed_objects_are_not_drawn: boolean;
  };
  readonly fixture_ref: {
    readonly path: string;
    readonly content_hash: string;
  };
  readonly provenance: Record<string, string>;
}

export interface BehaviorTraceMilestone {
  readonly tick: number;
  readonly event: string;
  readonly actor?: string;
  readonly actors?: readonly string[];
  readonly route?: readonly (readonly [number, number])[];
  readonly frame?: number;
  readonly expected?: string;
  readonly expected_state_label?: string;
  readonly expected_move_label?: string;
}

export interface BehaviorContract extends ContractHeader {
  readonly state_labels: unknown;
  readonly route_mapping: Record<string, unknown>;
  readonly transitions: readonly Record<string, unknown>[];
  readonly animation_timing: Record<string, unknown>;
  readonly talk_timing: {
    readonly frame_markers: readonly number[];
    readonly terminal_effect: string;
  };
  readonly trace: {
    readonly actors: readonly string[];
    readonly milestones: readonly BehaviorTraceMilestone[];
  };
}

export interface RoomRuntimeSelector {
  readonly field: string;
  readonly native_id: number;
  readonly native_selector_id?: number;
  readonly table_index?: number;
  readonly target_filename?: string;
  readonly target_asset_id?: string;
  readonly status: string;
  readonly runtime_alias?: {
    readonly selector_id: number;
    readonly metadata_filename: string;
    readonly render_filename: string;
    readonly status: string;
    readonly note: string;
  };
}

export interface RoomRuntimeRawCell {
  readonly cell_id: string;
  readonly cell: readonly [number, number];
  readonly x: number;
  readonly y: number;
  readonly raw_type: number;
  readonly raw_type_label: string;
  readonly raw_direction: number;
  readonly direction_status: string;
  readonly source_status: string;
}

export interface RoomRuntimeRawCellGroup {
  readonly raw_type: number;
  readonly label: string;
  readonly cells: readonly (readonly [number, number])[];
  readonly count: number;
  readonly identity_status: string;
}

export interface RoomRuntimeNativeBinding {
  readonly object_id: string;
  readonly furniture_data_id: number;
  readonly cell: readonly [number, number];
  readonly raw_type: number;
  readonly scan_order: number;
  readonly selector_flag: { readonly name: string; readonly value: number };
  readonly native_status: string;
  readonly source_status: string;
}

export interface RoomSceneRuntimeRecord {
  readonly room_key: string;
  readonly data_key: string;
  readonly native: Readonly<Record<string, unknown>> & {
    readonly id: number;
    readonly name: string;
    readonly floor_img_id: number;
    readonly wall_img_id: number;
    readonly door_img_id: number;
  };
  readonly selectors: {
    readonly floor: RoomRuntimeSelector;
    readonly wall: RoomRuntimeSelector;
    readonly door: RoomRuntimeSelector;
  };
  readonly grid: {
    readonly width: number;
    readonly height: number;
    readonly obj_map: readonly (readonly number[])[];
    readonly obj_dir: readonly (readonly number[])[];
  };
  readonly raw_cell_groups: readonly RoomRuntimeRawCellGroup[];
  readonly raw_cells: readonly RoomRuntimeRawCell[];
  readonly native_bindings: readonly RoomRuntimeNativeBinding[];
  readonly native_binding_status: string;
  readonly map_chip: {
    readonly status: string;
    readonly contract_path: string;
    readonly topology_selection: {
      readonly native_field: string;
      readonly roomdata_row_does_not_select_topology: boolean;
      readonly default_variant: string;
      readonly native_floor_value?: number;
      readonly selected_variant?: string;
      readonly selection_status?: string;
      readonly available_variants: readonly string[];
      readonly status: string;
    };
    readonly floor_image_table: Readonly<Record<string, unknown>>;
    readonly source_status: string;
  };
  readonly source: Readonly<Record<string, unknown>>;
}

export interface RoomSceneRuntimeContract extends ContractHeader {
  readonly catalog_id: string;
  readonly room_catalog_ref: {
    readonly path: string;
    readonly catalog_content_hash: string;
    readonly registry_content_hash: string;
    readonly status: string;
  };
  readonly map_chip_ref: {
    readonly path: string;
    readonly contract_hash?: string;
    readonly scene_ref: string;
    readonly shared_topology: boolean;
    readonly selection_field: string;
    readonly selection_status: string;
  };
  readonly native_identity_policy: {
    readonly objchip_never_infers_furniture_data_id: boolean;
    readonly raw_types_are_not_asset_ids: boolean;
    readonly native_bindings_must_be_explicit: boolean;
    readonly unresolved_direction_keeps_raw_value: boolean;
    readonly raw_type_semantics: Readonly<Record<string, string>>;
  };
  readonly rooms: readonly RoomSceneRuntimeRecord[];
  readonly counts: Readonly<Record<string, number>>;
}

export interface RoomRFixtureCell {
  readonly cell_id: string;
  readonly source_cell_id: string;
  readonly room_id: string;
  readonly grid: string;
  readonly x: number;
  readonly y: number;
  readonly flat_index: number;
  readonly raw_type: number;
  readonly raw_type_label: string;
  readonly raw_direction: number;
  readonly direction_status: string;
  readonly identity_status: string;
  readonly instance_id: null;
  readonly render_status: string;
  readonly source_status: string;
}

export interface RoomRSceneContract extends ContractHeader {
  readonly fixture_semantic_status: string;
  readonly catalog_id: string;
  readonly room_id: string;
  readonly data_key: string;
  readonly native: Readonly<Record<string, unknown>> & {
    readonly id: number;
    readonly name: string;
    readonly floor_img_id: number;
    readonly wall_img_id: number;
    readonly door_img_id: number;
  };
  readonly source: Readonly<Record<string, unknown>> & {
    readonly english_raw_row_sha256: string;
    readonly room_runtime_contract_hash: string;
  };
  readonly grid: {
    readonly width: number;
    readonly height: number;
    readonly obj_map: readonly (readonly number[])[];
    readonly obj_dir: readonly (readonly number[])[];
  };
  readonly raw_cells: readonly RoomRFixtureCell[];
  readonly raw_type_groups: readonly {
    readonly raw_type: number;
    readonly label: string;
    readonly count: number;
    readonly cells: readonly (readonly [number, number])[];
    readonly identity_status: string;
  }[];
  readonly door_cells: readonly { readonly cell_id: string; readonly x: number; readonly y: number }[];
  readonly selectors: {
    readonly floor: RoomRuntimeSelector;
    readonly wall: RoomRuntimeSelector;
    readonly door: RoomRuntimeSelector;
  };
  readonly map_chip: {
    readonly contract_path: string;
    readonly status: string;
    readonly shared_topology: boolean;
    readonly width: number;
    readonly height: number;
    readonly topology_selection: Readonly<Record<string, unknown>>;
    readonly default_variant: {
      readonly length: number;
      readonly rows: readonly (readonly number[])[];
      readonly metadata_offset: string;
      readonly metadata_hash: string;
    };
  };
  readonly native_bindings: readonly RoomRuntimeNativeBinding[];
  readonly runtime_policy: {
    readonly raw_overlay_is_diagnostic_only: boolean;
    readonly raw_types_are_not_furniture_data_ids: boolean;
    readonly direction_labels_are_not_invented: boolean;
    readonly native_wall_door_coordinate_composition_not_implied: boolean;
    readonly unbound_slots_are_not_drawn_as_native_objects: boolean;
  };
  readonly unresolved: readonly string[];
  readonly counts: Readonly<Record<string, number | Readonly<Record<string, number>>>>;
}

export interface NativeDirectionContract extends ContractHeader {
  readonly direction_semantics_status: string;
  readonly native_field: string;
  readonly raw_domain: readonly number[];
  readonly raw_values: Readonly<Record<string, {
    readonly label: string | null;
    readonly vector: readonly number[] | null;
    readonly reverse?: number;
  }>>;
  readonly native_trace?: {
    readonly vector_rva?: string;
    readonly reverse_rva?: string;
    readonly static_constructor_rva?: string;
    readonly direction_field_offset?: string;
    readonly reverse_table_rodata_rva?: string;
    readonly reverse_table?: readonly number[];
    readonly static_vectors?: readonly (readonly number[])[];
    readonly binary?: string;
    readonly binary_evidence_status?: string;
    readonly source_status?: string;
    readonly [key: string]: unknown;
  };
  readonly runtime_policy: {
    readonly preserve_raw_direction: boolean;
    readonly expose_native_label_and_vector?: boolean;
    readonly rotation_is_allowed: boolean;
    readonly directional_asset_selection_is_allowed: boolean;
    readonly unresolved_status: string;
  };
}

export interface NativeContentCatalogContract extends ContractHeader {
  readonly catalog_id: string;
  readonly source_registry: {
    readonly path: string;
    readonly schema_version: string;
    readonly content_hash: string;
    readonly policy: string;
  };
  readonly data_types: readonly Record<string, unknown>[];
  readonly data_records: readonly {
    readonly record_id: string;
    readonly native_id: number | null;
    readonly data_type: string;
    readonly native_namespace: string;
    readonly source_status: string;
    readonly decoded: Record<string, unknown>;
    readonly [key: string]: unknown;
  }[];
  readonly selectors: readonly Record<string, unknown>[];
  readonly assets: readonly Record<string, unknown>[];
  readonly connections: {
    readonly data_selector: readonly Record<string, unknown>[];
    readonly selector_asset_and_companion: readonly Record<string, unknown>[];
    readonly consumer: readonly Record<string, unknown>[];
    readonly lifecycle: readonly Record<string, unknown>[];
  };
  readonly identity_policy: Record<string, unknown>;
  readonly counts: Readonly<Record<string, number>>;
  readonly determinism: {
    readonly algorithm: string;
    readonly content_hash: string;
  };
}

export interface AssetMetadataRuntimeAsset {
  readonly asset_id: string;
  readonly relative_path: string;
  readonly family_id: string;
  readonly subfamily_id: string;
  readonly lineage: string;
  readonly runtime_manifest_families: readonly string[];
  readonly usage_status: string;
  readonly lifecycle_status: string;
  readonly placement_status: string;
  readonly composition_ids: readonly string[];
  readonly geometry_status?: string;
  readonly physical_dimensions?: readonly Record<string, unknown>[];
  readonly source_asset_id?: string;
  readonly runtime_policy: string;
}

export interface AssetMetadataRuntimeManifest extends ContractHeader {
  readonly refs: Readonly<Record<string, Record<string, string>>>;
  readonly counts: Readonly<Record<string, number>>;
  readonly runtime_assets: readonly AssetMetadataRuntimeAsset[];
  readonly family_manifests: readonly {
    readonly family_id: string;
    readonly asset_count: number;
    readonly runtime_asset_count: number;
    readonly runtime_asset_ids: readonly string[];
    readonly evidence_path: string;
    readonly load_policy: string;
  }[];
  readonly lazy_loading: {
    readonly asset_lookup: string;
    readonly selector_lookup: string;
    readonly furniture_lookup: string;
    readonly character_lookup: string;
    readonly eager_load_full_catalog: boolean;
    readonly source_archive_imports: boolean;
    readonly source_code_imports: boolean;
  };
  readonly runtime_policy: {
    readonly approved_scope: string;
    readonly unapproved_assets_are_not_loaded: boolean;
    readonly family_composition_gate_required: boolean;
    readonly placement_inference_disabled: boolean;
  };
}

export interface NativeSceneDirectionValue {
  readonly label: string;
  readonly vector: readonly [number, number];
  readonly reverse: number;
}

export interface NativeSceneSelectorConnection {
  readonly role: "floor" | "wall" | "door";
  readonly raw_selector_id: number;
  readonly native_selector_id?: number | null;
  readonly filename?: string;
  readonly asset_id: string;
  readonly runtime_path: string;
  readonly sha256: string;
  readonly source_status: string;
  readonly runtime_status: string;
}

export interface NativeSceneWallComposition {
  readonly status: string;
  readonly predicate: Readonly<Record<string, string>>;
  readonly cells_by_frame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
  readonly seb: { readonly selector_id: number; readonly filename: string };
  /** Layer 0 compatibility records are retained separately; native DrawSeb lineNo=-1 draws every selected layer. */
  readonly sprite_records: Readonly<Record<string, Record<string, unknown>>>;
  readonly sprite_layers: Readonly<Record<string, readonly Record<string, unknown>[]>>;
  readonly draw_semantics: Readonly<Record<string, unknown>>;
  readonly image_selector: NativeSceneSelectorConnection;
}

export interface NativeSceneDoorComposition {
  readonly status: string;
  readonly predicate: string;
  readonly cells: readonly (readonly [number, number])[];
  readonly raw_type: number;
  readonly installed_flag: number;
  readonly furniture_data: null;
  readonly seb: { readonly selector_id: number; readonly filename: string };
  readonly sprite_record: Record<string, unknown>;
  readonly image_selector: NativeSceneSelectorConnection;
}

export interface NativeSceneAssemblyRoom {
  readonly room_key: string;
  readonly data_key: string;
  readonly native: Readonly<Record<string, unknown>>;
  readonly map_chip: {
    readonly native_field: string;
    readonly native_floor_value: number;
    readonly selected_variant: string;
    readonly variant_rows: readonly (readonly number[])[];
    readonly selection_status: string;
    readonly source_status: string;
  };
  readonly selectors: Readonly<Record<"floor" | "wall" | "door", NativeSceneSelectorConnection>>;
  readonly objchip_grid: {
    readonly width: number;
    readonly height: number;
    readonly cell_count: number;
    readonly source_map_field: string;
    readonly source_direction_field: string;
    readonly constructor: string;
    readonly parent_setup: string;
    readonly raw_cell_identity: string;
    readonly native_furniture_identity_policy: string;
  };
  readonly object_cells: readonly {
    readonly instance_id: string;
    readonly cell: readonly [number, number];
    readonly raw_type: number;
    readonly raw_direction: number;
    readonly direction: NativeSceneDirectionValue;
    readonly furniture_data_id: number | null;
    readonly object_id: string | null;
    readonly identity_status: string;
  }[];
  readonly native_furniture_bindings: readonly RoomRuntimeNativeBinding[];
  readonly native_furniture_binding_status: string;
  readonly wall: NativeSceneWallComposition;
  readonly door: NativeSceneDoorComposition;
  readonly draw_commands: readonly {
    readonly pass_id: string;
    readonly native_method: string;
    readonly source: string;
  }[];
  readonly source: Record<string, unknown>;
}

export interface NativeSceneAssemblyContract extends ContractHeader {
  readonly catalog_id: string;
  readonly refs: Record<string, unknown>;
  readonly native_lifecycle: readonly {
    readonly order: number;
    readonly phase: string;
    readonly native_method: string;
    readonly input: string;
    readonly output: string;
  }[];
  readonly native_trace: Record<string, unknown>;
  readonly direction: {
    readonly native_field: string;
    readonly raw_domain: readonly number[];
    readonly values: Readonly<Record<string, NativeSceneDirectionValue>>;
    readonly status: string;
    readonly runtime_policy: Record<string, unknown>;
  };
  readonly coordinates: Record<string, unknown>;
  readonly wall_door_composition: Record<string, unknown>;
  readonly rooms: readonly NativeSceneAssemblyRoom[];
  readonly render_passes: readonly {
    readonly pass_id: string;
    readonly native_method: string;
    readonly source: string;
  }[];
  readonly closure_decisions: readonly string[];
  readonly counts: Readonly<Record<string, number>>;
  readonly determinism: {
    readonly algorithm: string;
    readonly content_hash: string;
  };
}

export interface RoomSceneAssetManifest extends ContractHeader {
  readonly scope: string;
  readonly assets: readonly {
    readonly asset_id: string;
    readonly asset_member: string;
    readonly runtime_path: string;
    readonly kind: string;
    readonly width: number;
    readonly height: number;
    readonly sha256: string;
  }[];
  readonly rooms: readonly {
    readonly room_key: string;
    readonly assets: Readonly<Record<"floor" | "wall" | "door", {
      readonly raw_selector_id: number;
      readonly native_selector_id?: number;
      readonly filename: string;
      readonly asset_id: string;
      readonly runtime_status: string;
      readonly source_status: string;
    }>>;
  }[];
  readonly counts: Readonly<Record<string, number>>;
  readonly runtime_policy: {
    readonly source_code_imports: boolean;
    readonly archive_imports: boolean;
    readonly exact_selector_identity_preserved: boolean;
    readonly native_coordinate_composition_not_implied: boolean;
  };
}

export type ActorBehaviorContract = BehaviorContract;

export interface TickOrderContract extends ContractHeader {
  readonly tick: {
    readonly unit: string;
    readonly step: number;
    readonly wall_clock: string;
  };
  readonly order: readonly {
    readonly index: number;
    readonly operation: string;
  }[];
  readonly mutation_policy: {
    readonly core_only: boolean;
    readonly renderer_may_mutate: boolean;
    readonly ui_may_mutate: boolean;
    readonly source_code_imports: boolean;
  };
}

export interface PreRuntimeClosureContract extends ContractHeader {
  readonly counts: Record<string, number>;
}
