import type { DepthInfo, Rect, SebContract, SebLayerContract, SebRecordContract, SpriteValues } from "./contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "./errors";
import { Sprite } from "./sprite";

const EXPLICIT_FRAME_MODULUS = 10000;

interface SourceRecord {
  readonly startFrame: number;
  readonly imageId: number;
  readonly imageIdRaw: number;
  readonly sourceX: number;
  readonly sourceY: number;
  readonly width: number;
  readonly height: number;
  readonly destinationX: number;
  readonly destinationY: number;
  readonly flags: number;
  readonly reserved: number;
  readonly layerRecordIndex: number;
}

interface SourceLayer {
  readonly layer: number;
  readonly markerRawValue: number | null;
  readonly records: readonly SourceRecord[];
}

export class Seb {
  private currentFrame = 0;

  private constructor(
    private readonly maxFrame: number,
    private readonly layers: readonly SourceLayer[],
  ) {}

  public static fromContract(contract: SebContract): Seb {
    validateSebContract(contract);
    return new Seb(
      contract.header.frame_bound,
      contract.layers.map((layer) => ({
        layer: layer.layer,
        markerRawValue: layer.marker?.raw_value ?? null,
        records: layer.records.map(copySourceRecord),
      })),
    );
  }

  public getMaxFrame(): number {
    return this.maxFrame;
  }

  public getCurFrame(): number {
    return this.currentFrame;
  }

  public setCurFrame(frame: number): void {
    this.currentFrame = requireInteger(frame, "SEB_FRAME_MALFORMED");
  }

  public Frame(): void {
    this.currentFrame = (this.currentFrame + 1) % this.maxFrame;
  }

  public getSprites(frame: number): Sprite[] {
    return this.layers.map((_, layer) => {
      const sprite = this.getSprite(frame, layer);
      if (sprite === null) {
        throw new V1LookupError("SEB_FRAME_RECORD_NOT_FOUND");
      }
      return sprite;
    });
  }

  public getSprite(frame: number, layer: number): Sprite | null {
    const sourceLayer = this.layers[requireLayer(layer, this.layers.length)];
    const explicitFrame = requireInteger(frame, "SEB_FRAME_MALFORMED") % EXPLICIT_FRAME_MODULUS;
    const record = selectActiveRecord(sourceLayer.records, explicitFrame);
    return record === null ? null : new Sprite(toSpriteValues(record));
  }

  public getBRect(frame = this.currentFrame, layer?: number): Rect {
    if (layer !== undefined) {
      const sprite = this.getSprite(frame, layer);
      if (sprite === null) {
        throw new V1LookupError("SEB_FRAME_RECORD_NOT_FOUND");
      }
      return rectFromSprite(sprite);
    }
    return unionRects(this.getSprites(frame).map(rectFromSprite));
  }

  public getBoundingRect(frame = this.currentFrame): Rect {
    return this.getBRect(frame);
  }

  public getPixelRect(frame = this.currentFrame): Rect {
    // The selected decoded SEB grammar has no pixelBoundingRects_ payload. The
    // native GetPixelRect(frame) path falls back to GetBRect(frame) when that
    // optional cache is absent; do not substitute PNG dimensions here.
    return this.getBRect(frame);
  }

  public getDepthInfo(
    frame: number,
    scale: number,
    defaultDepth = 0,
    ignoreDepth = Number.MAX_SAFE_INTEGER,
  ): DepthInfo {
    requireInteger(frame, "SEB_FRAME_MALFORMED");
    requireInteger(scale, "SEB_DEPTH_SCALE_MALFORMED");
    requireInteger(defaultDepth, "SEB_DEFAULT_DEPTH_MALFORMED");
    requireInteger(ignoreDepth, "SEB_IGNORE_DEPTH_MALFORMED");
    throw new V1DeferredError(
      "SEB_DEPTH_UNPROVEN",
      "DepthInfo remains deferred because the selected SEB contracts retain no native depth-line metadata.",
    );
  }
}

function rectFromSprite(sprite: Sprite): Rect {
  return {
    x: sprite.TransX,
    y: sprite.TransY,
    width: sprite.W,
    height: sprite.H,
  };
}

function unionRects(rects: readonly Rect[]): Rect {
  if (rects.length === 0) {
    throw new V1LookupError("SEB_NO_SPRITES");
  }
  const left = Math.min(...rects.map((rect) => rect.x));
  const top = Math.min(...rects.map((rect) => rect.y));
  const right = Math.max(...rects.map((rect) => rect.x + rect.width));
  const bottom = Math.max(...rects.map((rect) => rect.y + rect.height));
  return { x: left, y: top, width: right - left, height: bottom - top };
}

function validateSebContract(contract: SebContract): void {
  if (contract.status !== "pass" || contract.grammar !== "seb-layered-v1") {
    throw new V1ContractError("SEB_DECODER_STATUS_UNSUPPORTED");
  }
  if (contract.trailing_bytes !== 0 || contract.metadata_warnings.length !== 0) {
    throw new V1ContractError("SEB_DECODER_OUTPUT_UNSUPPORTED");
  }

  const header = contract.header;
  const layerCount = requirePositiveInteger(header.layer_count, "SEB_LAYER_COUNT_MALFORMED");
  const globalFrameCount = requirePositiveInteger(header.global_frame_count, "SEB_FRAME_COUNT_MALFORMED");
  const frameBound = requirePositiveInteger(header.frame_bound, "SEB_FRAME_BOUND_MALFORMED");
  const firstRecordCount = requirePositiveInteger(header.record_count, "SEB_RECORD_COUNT_MALFORMED");

  if (contract.layers.length !== layerCount || globalFrameCount !== frameBound) {
    throw new V1ContractError("SEB_HEADER_MISMATCH");
  }
  if (contract.records.length !== contract.layers.reduce((count, layer) => count + layer.records.length, 0)) {
    throw new V1ContractError("SEB_RECORD_TOTAL_MISMATCH");
  }
  const sourceOrderRecords = contract.layers.flatMap((layer) => layer.records);
  if (sourceOrderRecords.some((record, index) => !sameRecord(record, contract.records[index]))) {
    throw new V1ContractError("SEB_TOP_LEVEL_RECORD_ORDER_MISMATCH");
  }

  for (const [index, layer] of contract.layers.entries()) {
    validateLayer(layer, index, frameBound, index === 0 ? firstRecordCount : undefined);
  }
}

function validateLayer(
  layer: SebLayerContract,
  index: number,
  frameBound: number,
  expectedFirstRecordCount: number | undefined,
): void {
  if (layer.index !== index || layer.layer !== index || layer.frame_bound !== frameBound) {
    throw new V1ContractError("SEB_LAYER_ORDER_MALFORMED");
  }
  if (requirePositiveInteger(layer.record_count, "SEB_RECORD_COUNT_MALFORMED") !== layer.records.length) {
    throw new V1ContractError("SEB_LAYER_RECORD_COUNT_MISMATCH");
  }
  if (expectedFirstRecordCount !== undefined && layer.record_count !== expectedFirstRecordCount) {
    throw new V1ContractError("SEB_HEADER_RECORD_COUNT_MISMATCH");
  }
  if ((index === 0 && layer.marker !== null) || (index > 0 && layer.marker === null)) {
    throw new V1ContractError("SEB_LAYER_MARKER_MALFORMED");
  }
  if (layer.marker !== null) {
    requireUnsigned16(layer.marker.record_count, "SEB_LAYER_MARKER_MALFORMED");
    requireUnsigned16(layer.marker.raw_value, "SEB_LAYER_MARKER_MALFORMED");
    if (layer.marker.record_count !== layer.record_count) {
      throw new V1ContractError("SEB_LAYER_MARKER_COUNT_MISMATCH");
    }
  }
  for (const [recordIndex, record] of layer.records.entries()) {
    validateRecord(record, index, recordIndex, frameBound);
  }
}

function validateRecord(record: SebRecordContract, layer: number, recordIndex: number, frameBound: number): void {
  if (record.layer !== layer || record.layer_record_index !== recordIndex) {
    throw new V1ContractError("SEB_RECORD_ORDER_MALFORMED");
  }
  if (record.frame_status !== "in_header_frame_bound" || record.start_frame < 0 || record.start_frame >= frameBound) {
    throw new V1ContractError("SEB_RECORD_FRAME_STATUS_UNSUPPORTED");
  }
  for (const value of [
    record.start_frame,
    record.source_x,
    record.source_y,
    record.width,
    record.height,
    record.destination_x,
    record.destination_y,
    record.flags,
    record.reserved,
  ]) {
    requireInteger(value, "SEB_RECORD_VALUE_MALFORMED");
  }
  requireUnsigned16(record.image_id_raw, "SEB_IMAGE_ID_RAW_MALFORMED");
  const expectedImageId = record.image_id_raw >= 0x8000 ? record.image_id_raw - 0x10000 : record.image_id_raw;
  if (record.image_id !== expectedImageId) {
    throw new V1ContractError("SEB_IMAGE_ID_SIGN_MISMATCH");
  }
}

function copySourceRecord(record: SebRecordContract): SourceRecord {
  return {
    startFrame: record.start_frame,
    imageId: record.image_id,
    imageIdRaw: record.image_id_raw,
    sourceX: record.source_x,
    sourceY: record.source_y,
    width: record.width,
    height: record.height,
    destinationX: record.destination_x,
    destinationY: record.destination_y,
    flags: record.flags,
    reserved: record.reserved,
    layerRecordIndex: record.layer_record_index,
  };
}

function sameRecord(left: SebRecordContract, right: SebRecordContract | undefined): boolean {
  return right !== undefined
    && left.layer === right.layer
    && left.layer_record_index === right.layer_record_index
    && left.start_frame === right.start_frame
    && left.image_id === right.image_id
    && left.image_id_raw === right.image_id_raw
    && left.source_x === right.source_x
    && left.source_y === right.source_y
    && left.width === right.width
    && left.height === right.height
    && left.destination_x === right.destination_x
    && left.destination_y === right.destination_y
    && left.flags === right.flags
    && left.reserved === right.reserved
    && left.frame_status === right.frame_status;
}

function selectActiveRecord(records: readonly SourceRecord[], frame: number): SourceRecord | null {
  let selected: SourceRecord | null = null;
  for (const record of records) {
    if (record.startFrame <= frame) {
      selected = record;
    }
  }
  return selected;
}

function toSpriteValues(record: SourceRecord): SpriteValues {
  return [
    record.startFrame,
    record.imageId,
    record.sourceX,
    record.sourceY,
    record.width,
    record.height,
    record.destinationX,
    record.destinationY,
    record.flags & 1,
    (record.flags >> 1) & 1,
    (record.flags >> 2) & 0xF,
    record.reserved,
  ];
}

function requireLayer(layer: number, layerCount: number): number {
  const value = requireInteger(layer, "SEB_LAYER_MALFORMED");
  if (value < 0 || value >= layerCount) {
    throw new V1LookupError("SEB_LAYER_OUT_OF_RANGE");
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

function requireUnsigned16(value: number, code: string): number {
  const integer = requireInteger(value, code);
  if (integer < 0 || integer > 0xFFFF) {
    throw new V1ContractError(code);
  }
  return integer;
}

function requireInteger(value: number, code: string): number {
  if (!Number.isSafeInteger(value)) {
    throw new V1ContractError(code);
  }
  return value;
}
