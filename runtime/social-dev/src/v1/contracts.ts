import { V1ContractError } from "./errors";

export const SPRITE_INDEX = {
  FrameNo: 0,
  TexId: 1,
  U: 2,
  V: 3,
  W: 4,
  H: 5,
  TransX: 6,
  TransY: 7,
  ReverseU: 8,
  ReverseV: 9,
  Blend: 10,
  Color: 11,
} as const;

export type SpriteValues = readonly [
  number, number, number, number, number, number,
  number, number, number, number, number, number,
];

export interface Rect {
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}

export interface DepthInfo {
  readonly depth: number;
  readonly scale: number;
  readonly isDefaultDepth: boolean;
  readonly layers: readonly number[];
}

export interface SebRecordContract {
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
  readonly frame_status: string;
}

export interface SebLayerContract {
  readonly index: number;
  readonly layer: number;
  readonly record_count: number;
  readonly frame_bound: number;
  readonly marker: { readonly record_count: number; readonly raw_value: number } | null;
  readonly records: readonly SebRecordContract[];
}

export interface SebContract {
  readonly status: string;
  readonly grammar: string;
  readonly header: {
    readonly layer_count: number;
    readonly global_frame_count: number;
    readonly record_count: number;
    readonly frame_bound: number;
  };
  readonly layers: readonly SebLayerContract[];
  readonly records: readonly SebRecordContract[];
  readonly trailing_bytes: number;
  readonly metadata_warnings: readonly string[];
}

export interface SebEvidenceRecord {
  readonly source_member: string;
  readonly source_sha256: string;
  readonly decoded: SebContract;
}

export interface SebEvidenceContract {
  readonly status: string;
  readonly records: readonly SebEvidenceRecord[];
}

export type OptimizeValues = readonly [
  number,
  number,
  number,
  number,
  number,
  number,
  number,
];

export interface OptHeaderContract {
  readonly cell_width: number;
  readonly cell_height: number;
  readonly columns: number;
  readonly rows: number;
  readonly logical_width: number;
  readonly logical_height: number;
}

export interface OptRecordContract {
  readonly index: number;
  readonly record_prefix: number;
  readonly source_reference: number;
  readonly offset_x: number;
  readonly offset_y: number;
  readonly source_x: number;
  readonly source_y: number;
  readonly width: number;
  readonly height: number;
  readonly part_index: number;
  readonly part_count: number;
  readonly cell_column: number;
  readonly cell_row: number;
  readonly destination_x: number;
  readonly destination_y: number;
}

export interface OptCellContract {
  readonly index: number;
  readonly piece_count: number;
  readonly records: readonly OptRecordContract[];
}

export interface OptPayloadContract {
  readonly source_ref: string;
  readonly size_bytes: number;
  readonly sha256: string;
  readonly header: OptHeaderContract;
  readonly expected_record_count: number;
  readonly partial_tail_bytes: number;
  readonly status: string;
  readonly errors: readonly string[];
  readonly records: readonly OptRecordContract[];
  readonly cells: readonly OptCellContract[];
}

export interface ImageAssetHashContract {
  readonly member: string;
  readonly raw_sha256: string;
  readonly bytes: number;
  readonly runtime_promotion: {
    readonly status: string;
    readonly runtime_path?: string;
    readonly runtime_sha256?: string;
  };
}

export interface ImageRuntimePromotionContract {
  readonly status: string;
  readonly runtime_path: string;
  readonly raw_sha256: string;
  readonly pixel_sha256: string;
}

export interface ImageSebAssociationContract {
  readonly seb_member: string;
  readonly seb_sha256: string;
  readonly image_id: number;
  readonly source_index_member: string;
  readonly status: string;
}

export interface ImageNativeContract {
  readonly load_optimize_rvas: readonly string[];
  readonly get_optimize_rvas: readonly string[];
  readonly get_optimize_seb_rva: string;
  readonly use_unuse_rvas: readonly string[];
  readonly resize_rvas: readonly string[];
  readonly set_image_atlas_id_rva: string;
  readonly proof_class: string;
  readonly source_ref: string;
}

export interface ImageContract {
  readonly fixture_stem: string;
  readonly source_png: ImageAssetHashContract;
  readonly source_opt: ImageAssetHashContract;
  readonly logical_reconstruction: {
    readonly status: string;
    readonly pixel_sha256: string;
    readonly source_size: { readonly width: number; readonly height: number };
    readonly logical_size: { readonly width: number; readonly height: number };
    readonly opt: OptPayloadContract;
  };
  readonly logical_runtime_promotion: ImageRuntimePromotionContract;
  readonly opt: OptPayloadContract;
  readonly source_size: { readonly width: number; readonly height: number };
  readonly logical_size: { readonly width: number; readonly height: number };
  readonly pixel_sha256: string;
  readonly source_png_pixel_sha256: string;
  readonly optimize_access: Readonly<Record<string, OptimizeValues>>;
  readonly optimize_type_index: Readonly<Record<string, OptimizeValues>>;
  readonly optimize_grid: {
    readonly columns: number;
    readonly rows: number;
    readonly max_pass: number;
  };
  readonly seb_associations: readonly (OptimizeValues | null)[];
  readonly optimize_seb_contract: {
    readonly status: string;
    readonly proof_class: string;
    readonly source_ref: string;
  };
  readonly associated_seb_ids: readonly ImageSebAssociationContract[];
  readonly image_atlas_id: number;
  readonly atlas_region: unknown;
  readonly native_contract: ImageNativeContract;
  readonly lifetime_contract: {
    readonly status: string;
    readonly use: string;
    readonly unuse: string;
    readonly raster_loading: string;
  };
  readonly resize_contract: {
    readonly status: string;
    readonly raster_parity: string;
    readonly source_ref: string;
  };
}

export interface ImageOptEvidenceContract {
  readonly schema_version: string;
  readonly status: string;
  readonly source: Readonly<Record<string, string>>;
  readonly codec: {
    readonly parse_opt: string;
    readonly reconstruct_opt: string;
  };
  readonly records: readonly ImageContract[];
}

export interface ResourceLookupImageBinding {
  readonly id: number;
  readonly source_index_member: string;
  readonly source_member: string;
  readonly source_sha256: string;
  readonly image_contract_stem: string | null;
  readonly runtime_promotion: { readonly status: string; readonly runtime_path?: string; readonly runtime_sha256?: string };
  readonly status: string;
}

export interface ResourceLookupSebBinding {
  readonly id: number;
  readonly source_index_member: string;
  readonly source_member: string;
  readonly source_sha256: string;
  readonly seb_contract_member: string | null;
  readonly status: string;
}

export interface ResourceLookupFixture {
  readonly fixture_id: string;
  readonly group_id: string;
  readonly fixture_stem: string;
  readonly image_id: number | null;
  readonly seb_id: number;
  readonly image_member: string | null;
  readonly seb_member: string;
  readonly image_contract_stem: string | null;
  readonly seb_contract_member: string | null;
  readonly status: string;
}

export interface ResourceLookupGroupContract {
  readonly group_id: string;
  readonly source_declaration: string;
  readonly source_ref: string;
  readonly group_kind: string;
  readonly status: string;
  readonly membership_status: string;
  readonly ownership: Readonly<Record<string, string>>;
  readonly image_bindings: readonly ResourceLookupImageBinding[];
  readonly seb_bindings: readonly ResourceLookupSebBinding[];
  readonly fixtures: readonly ResourceLookupFixture[];
}

export interface ResourceLookupEvidenceContract {
  readonly schema_version: string;
  readonly status: string;
  readonly source: Readonly<Record<string, string>>;
  readonly group_ids: readonly string[];
  readonly groups: readonly ResourceLookupGroupContract[];
  readonly fixtures: readonly ResourceLookupFixture[];
  readonly atlas_contract: {
    readonly status: string;
    readonly reason: string;
    readonly affected_fixtures: readonly string[];
  };
  readonly native_contract: Readonly<Record<string, unknown>>;
}

export function assertSpriteValues(values: readonly number[]): asserts values is SpriteValues {
  if (values.length !== 12 || values.some((value) => !Number.isFinite(value))) {
    throw new V1ContractError("SPRITE_VALUES_MALFORMED");
  }
}
