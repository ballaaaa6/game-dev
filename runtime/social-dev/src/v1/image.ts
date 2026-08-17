import type {
  ImageContract,
  ImageOptEvidenceContract,
  ImageSebAssociationContract,
  OptRecordContract,
  OptimizeValues,
} from "./contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "./errors";

export const ImageResult = {
  Success: 0,
  Failure: 1,
  Over: 2,
} as const;

export type ImageResult = (typeof ImageResult)[keyof typeof ImageResult];

export interface ImageSourceRegion {
  readonly index: number;
  readonly partIndex: number;
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
  readonly destinationX: number;
  readonly destinationY: number;
}

export interface ImageResizeMetadata {
  readonly width: number;
  readonly height: number;
  readonly srcX: number;
  readonly srcY: number;
  readonly srcWidth: number;
  readonly srcHeight: number;
  readonly rasterParity: "deferred";
}

export class Image {
  private readonly contract: ImageContract;

  private readonly optimizeAccess: ReadonlyMap<string, OptimizeValues>;

  private readonly optimizeTypeIndex: ReadonlyMap<string, OptimizeValues>;

  private currentWidth: number;

  private currentHeight: number;

  private currentUseCount = 0;

  private currentImageAtlasId: number;

  private currentResizeMetadata: ImageResizeMetadata | null = null;

  private constructor(contract: ImageContract, images: readonly Image[] = []) {
    this.contract = cloneContract(contract);
    this.optimizeAccess = new Map(
      Object.entries(this.contract.optimize_access).map(([key, values]) => [key, [...values] as OptimizeValues]),
    );
    this.optimizeTypeIndex = new Map(
      Object.entries(this.contract.optimize_type_index).map(([key, values]) => [key, [...values] as OptimizeValues]),
    );
    this.currentWidth = this.contract.logical_size.width;
    this.currentHeight = this.contract.logical_size.height;
    this.currentImageAtlasId = this.contract.image_atlas_id;

    // The native loader accepts an optional Image[] source set. The selected
    // contracts use only source_reference=-1, so retain the argument boundary
    // without making a second image decoder or inventing cross-image links.
    void images;
  }

  public static fromContract(contract: ImageContract): Image {
    if (isRawBytes(contract)) {
      throw new V1DeferredError(
        "IMAGE_RAW_OPT_DEFERRED",
        "Image consumes the validated Python OPT contract; raw OPT decoding remains outside the TypeScript boundary.",
      );
    }
    validateImageContract(contract);
    return new Image(contract);
  }

  public static loadOptimize(contract: ImageContract, images: readonly Image[] = []): Image {
    if (isRawBytes(contract)) {
      throw new V1DeferredError(
        "IMAGE_RAW_OPT_DEFERRED",
        "Image.LoadOptimize consumes a validated OPT contract rather than raw bytes in V1.",
      );
    }
    validateImageContract(contract);
    return new Image(contract, images);
  }

  public loadOptimize(contract: ImageContract, images: readonly Image[] = []): Image {
    return Image.loadOptimize(contract, images);
  }

  public get fixtureStem(): string {
    return this.contract.fixture_stem;
  }

  public get sourceMember(): string {
    return this.contract.source_png.member;
  }

  public get sourceOptMember(): string {
    return this.contract.source_opt.member;
  }

  public get width(): number {
    return this.currentWidth;
  }

  public get height(): number {
    return this.currentHeight;
  }

  public get logicalWidth(): number {
    return this.currentWidth;
  }

  public get logicalHeight(): number {
    return this.currentHeight;
  }

  public get sourceWidth(): number {
    return this.contract.source_size.width;
  }

  public get sourceHeight(): number {
    return this.contract.source_size.height;
  }

  public get sourcePixelSha256(): string {
    // The V1 contract names the validated logical pixel identity pixel_sha256;
    // it is the identity asserted by the existing source/runtime reconstruction.
    return this.contract.pixel_sha256;
  }

  public get pixelSha256(): string {
    return this.contract.pixel_sha256;
  }

  public get sourcePngPixelSha256(): string {
    return this.contract.source_png_pixel_sha256;
  }

  public get sourcePngRawSha256(): string {
    return this.contract.source_png.raw_sha256;
  }

  public get sourceOptRawSha256(): string {
    return this.contract.source_opt.raw_sha256;
  }

  public get runtimeRawSha256(): string {
    return this.contract.logical_runtime_promotion.raw_sha256;
  }

  public get runtimePixelSha256(): string {
    return this.contract.logical_runtime_promotion.pixel_sha256;
  }

  public get hasOptimize(): boolean {
    return this.contract.logical_reconstruction.opt.status === "pass";
  }

  public get optimizeHeader(): ImageContract["logical_reconstruction"]["opt"]["header"] {
    return this.contract.logical_reconstruction.opt.header;
  }

  public get optimizeCells(): ImageContract["logical_reconstruction"]["opt"]["cells"] {
    return this.contract.logical_reconstruction.opt.cells;
  }

  public get sourceRegions(): readonly ImageSourceRegion[] {
    return this.contract.logical_reconstruction.opt.records.map((record) => toSourceRegion(record));
  }

  public get associatedSebIds(): readonly ImageSebAssociationContract[] {
    return this.contract.associated_seb_ids;
  }

  public get imageAtlasId(): number {
    return this.currentImageAtlasId;
  }

  public get ImageAtlasId(): number {
    return this.currentImageAtlasId;
  }

  public get atlasRegion(): unknown {
    return this.contract.atlas_region;
  }

  public get useCount(): number {
    return this.currentUseCount;
  }

  public get isUsed(): boolean {
    return this.currentUseCount > 0;
  }

  public get resizeMetadata(): ImageResizeMetadata | null {
    return this.currentResizeMetadata;
  }

  public getOptimize(bx: number, by: number, passIndex: number): readonly number[] | null;

  public getOptimize(access: number): readonly number[] | null;

  public getOptimize(type: number, index: number): readonly number[] | null;

  public getOptimize(first: number, second?: number, third?: number): readonly number[] | null {
    if (third !== undefined) {
      if (second === undefined) {
        throw new V1ContractError("IMAGE_OPT_ACCESS_MALFORMED");
      }
      const bx = requireInteger(first, "IMAGE_OPT_ACCESS_MALFORMED");
      const by = requireInteger(second, "IMAGE_OPT_ACCESS_MALFORMED");
      const passIndex = requireInteger(third, "IMAGE_OPT_ACCESS_MALFORMED");
      if (
        bx < 0
        || by < 0
        || passIndex < 0
        || bx >= this.optimizeHeader.columns
        || by >= this.optimizeHeader.rows
      ) {
        throw new V1LookupError("IMAGE_OPT_ACCESS_OUT_OF_RANGE");
      }
      const values = this.optimizeAccess.get(`${bx},${by},${passIndex}`);
      return values === undefined ? null : [...values];
    }

    if (second !== undefined) {
      return this.getOptimizeByTypeIndex(first, second);
    }

    const access = requireInteger(first, "IMAGE_OPT_ACCESS_MALFORMED");
    const shift = access >= -128 && access <= 127 ? 7 : 15;
    const type = (access >> shift) & 1;
    const index = access & ((1 << shift) - 1);
    return this.getOptimizeByTypeIndex(type, index);
  }

  public getOptimizeByTypeIndex(type: number, index: number): readonly number[] | null {
    const validType = requireInteger(type, "IMAGE_OPT_TYPE_MALFORMED");
    const validIndex = requireInteger(index, "IMAGE_OPT_INDEX_MALFORMED");
    if (validType < 0 || validIndex < 0) {
      throw new V1LookupError("IMAGE_OPT_TYPE_INDEX_OUT_OF_RANGE");
    }
    const values = this.optimizeTypeIndex.get(`${validType},${validIndex}`);
    return values === undefined ? null : [...values];
  }

  public getOptimizeSeb(index: number): readonly number[] | null {
    const validIndex = requireInteger(index, "IMAGE_OPT_SEB_INDEX_MALFORMED");
    if (validIndex < 0) {
      throw new V1LookupError("IMAGE_OPT_SEB_INDEX_OUT_OF_RANGE");
    }
    const association = this.contract.seb_associations[validIndex];
    return association === undefined || association === null ? null : [...association];
  }

  public getSourceRegion(index: number, partIndex = 0): ImageSourceRegion {
    const validIndex = requireInteger(index, "IMAGE_SOURCE_REGION_INDEX_MALFORMED");
    const validPartIndex = requireInteger(partIndex, "IMAGE_SOURCE_REGION_PART_MALFORMED");
    if (validIndex < 0 || validPartIndex < 0) {
      throw new V1LookupError("IMAGE_SOURCE_REGION_OUT_OF_RANGE");
    }
    const record = this.contract.logical_reconstruction.opt.records.find(
      (candidate) => candidate.index === validIndex && candidate.part_index === validPartIndex,
    );
    if (record === undefined) {
      throw new V1LookupError("IMAGE_SOURCE_REGION_NOT_FOUND");
    }
    return toSourceRegion(record);
  }

  public use(): void {
    this.currentUseCount += 1;
  }

  public unuse(): void {
    if (this.currentUseCount > 0) {
      this.currentUseCount -= 1;
    }
  }

  public resize(width: number, height: number): void;

  public resize(scaleRatio: number): void;

  public resize(width: number, height: number, srcX: number, srcY: number, srcWidth: number, srcHeight: number): void;

  public resize(first: number, second?: number, srcX?: number, srcY?: number, srcWidth?: number, srcHeight?: number): void {
    const previousWidth = this.currentWidth;
    const previousHeight = this.currentHeight;
    let width: number;
    let height: number;
    let sourceX: number;
    let sourceY: number;
    let sourceWidth: number;
    let sourceHeight: number;

    if (second === undefined) {
      if (!Number.isFinite(first) || first <= 0) {
        throw new V1ContractError("IMAGE_RESIZE_SCALE_MALFORMED");
      }
      width = Math.floor(previousWidth * first);
      height = Math.floor(previousHeight * first);
      sourceX = 0;
      sourceY = 0;
      sourceWidth = previousWidth;
      sourceHeight = previousHeight;
    } else {
      width = requirePositiveInteger(first, "IMAGE_RESIZE_WIDTH_MALFORMED");
      height = requirePositiveInteger(second, "IMAGE_RESIZE_HEIGHT_MALFORMED");
      sourceX = requireNonnegativeInteger(srcX ?? 0, "IMAGE_RESIZE_SOURCE_MALFORMED");
      sourceY = requireNonnegativeInteger(srcY ?? 0, "IMAGE_RESIZE_SOURCE_MALFORMED");
      sourceWidth = requirePositiveInteger(srcWidth ?? previousWidth, "IMAGE_RESIZE_SOURCE_MALFORMED");
      sourceHeight = requirePositiveInteger(srcHeight ?? previousHeight, "IMAGE_RESIZE_SOURCE_MALFORMED");
    }

    this.currentWidth = width;
    this.currentHeight = height;
    this.currentResizeMetadata = {
      width,
      height,
      srcX: sourceX,
      srcY: sourceY,
      srcWidth: sourceWidth,
      srcHeight: sourceHeight,
      rasterParity: "deferred",
    };
  }

  public setImageAtlasId(id: number): ImageResult {
    const validId = requireInteger(id, "IMAGE_ATLAS_ID_MALFORMED");
    if (validId < -1) {
      throw new V1ContractError("IMAGE_ATLAS_ID_MALFORMED");
    }
    this.currentImageAtlasId = validId;
    return ImageResult.Success;
  }
}

export function loadOptimize(contract: ImageContract, images: readonly Image[] = []): Image {
  return Image.loadOptimize(contract, images);
}

export function loadImageContractFromEvidence(
  evidence: ImageOptEvidenceContract,
  fixtureStem: string,
): Image {
  const record = evidence.records.find((candidate) => candidate.fixture_stem === fixtureStem);
  if (record === undefined) {
    throw new V1LookupError("IMAGE_FIXTURE_CONTRACT_NOT_FOUND");
  }
  return Image.fromContract(record);
}

function validateImageContract(contract: ImageContract): void {
  if (contract === null || typeof contract !== "object") {
    throw new V1ContractError("IMAGE_CONTRACT_MALFORMED");
  }
  if (contract.logical_reconstruction.status !== "pass") {
    throw new V1ContractError("IMAGE_RECONSTRUCTION_UNSUPPORTED");
  }
  const opt = contract.logical_reconstruction.opt;
  if (
    opt.status !== "pass"
    || contract.opt.status !== opt.status
    || contract.opt.sha256 !== opt.sha256
    || opt.errors.length !== 0
    || opt.partial_tail_bytes !== 0
  ) {
    throw new V1ContractError("IMAGE_OPT_CONTRACT_UNSUPPORTED");
  }
  requirePositiveInteger(contract.source_size.width, "IMAGE_SOURCE_WIDTH_MALFORMED");
  requirePositiveInteger(contract.source_size.height, "IMAGE_SOURCE_HEIGHT_MALFORMED");
  requirePositiveInteger(contract.logical_size.width, "IMAGE_LOGICAL_WIDTH_MALFORMED");
  requirePositiveInteger(contract.logical_size.height, "IMAGE_LOGICAL_HEIGHT_MALFORMED");
  if (
    contract.logical_size.width !== opt.header.logical_width
    || contract.logical_size.height !== opt.header.logical_height
    || contract.logical_reconstruction.logical_size.width !== contract.logical_size.width
    || contract.logical_reconstruction.logical_size.height !== contract.logical_size.height
  ) {
    throw new V1ContractError("IMAGE_LOGICAL_SIZE_MISMATCH");
  }
  if (contract.pixel_sha256 !== contract.logical_reconstruction.pixel_sha256) {
    throw new V1ContractError("IMAGE_PIXEL_HASH_MISMATCH");
  }
  if (contract.pixel_sha256 !== contract.logical_runtime_promotion.pixel_sha256) {
    throw new V1ContractError("IMAGE_RUNTIME_PIXEL_HASH_MISMATCH");
  }
  if (contract.source_png.raw_sha256 !== contract.source_png.runtime_promotion.runtime_sha256) {
    throw new V1ContractError("IMAGE_SOURCE_PNG_HASH_MISMATCH");
  }
  if (contract.source_opt.raw_sha256 !== contract.source_opt.runtime_promotion.runtime_sha256) {
    throw new V1ContractError("IMAGE_SOURCE_OPT_HASH_MISMATCH");
  }
  if (contract.optimize_grid.columns !== opt.header.columns || contract.optimize_grid.rows !== opt.header.rows) {
    throw new V1ContractError("IMAGE_OPT_GRID_MISMATCH");
  }
  for (const record of opt.records) {
    validateOptRecord(record, contract.source_size.width, contract.source_size.height);
  }
  for (const [key, values] of Object.entries(contract.optimize_access)) {
    if (!/^\d+,\d+,\d+$/.test(key) || !isOptimizeValues(values)) {
      throw new V1ContractError("IMAGE_OPT_ACCESS_MALFORMED");
    }
  }
  if (contract.seb_associations.length === 0) {
    throw new V1ContractError("IMAGE_OPT_SEB_CONTRACT_MALFORMED");
  }
}

function validateOptRecord(record: OptRecordContract, sourceWidth: number, sourceHeight: number): void {
  for (const value of [
    record.index,
    record.record_prefix,
    record.source_reference,
    record.offset_x,
    record.offset_y,
    record.source_x,
    record.source_y,
    record.width,
    record.height,
    record.part_index,
    record.part_count,
    record.cell_column,
    record.cell_row,
    record.destination_x,
    record.destination_y,
  ]) {
    requireInteger(value, "IMAGE_OPT_RECORD_MALFORMED");
  }
  if (
    record.source_x < 0
    || record.source_y < 0
    || record.width <= 0
    || record.height <= 0
    || record.source_x + record.width > sourceWidth
    || record.source_y + record.height > sourceHeight
  ) {
    throw new V1ContractError("IMAGE_OPT_SOURCE_RECT_OUT_OF_BOUNDS");
  }
}

function isOptimizeValues(value: readonly number[]): value is OptimizeValues {
  return Array.isArray(value) && value.length === 7 && value.every((item) => Number.isSafeInteger(item));
}

function toSourceRegion(record: OptRecordContract): ImageSourceRegion {
  return {
    index: record.index,
    partIndex: record.part_index,
    x: record.source_x,
    y: record.source_y,
    width: record.width,
    height: record.height,
    destinationX: record.destination_x,
    destinationY: record.destination_y,
  };
}

function cloneContract(contract: ImageContract): ImageContract {
  return JSON.parse(JSON.stringify(contract)) as ImageContract;
}

function isRawBytes(value: unknown): value is Uint8Array {
  return value instanceof Uint8Array || value instanceof ArrayBuffer;
}

function requireInteger(value: number, code: string): number {
  if (!Number.isSafeInteger(value)) {
    throw new V1ContractError(code);
  }
  return value;
}

function requirePositiveInteger(value: number, code: string): number {
  const integer = requireInteger(value, code);
  if (integer <= 0) {
    throw new V1ContractError(code);
  }
  return integer;
}

function requireNonnegativeInteger(value: number, code: string): number {
  const integer = requireInteger(value, code);
  if (integer < 0) {
    throw new V1ContractError(code);
  }
  return integer;
}
