import type { SebContract } from "../v1/contracts";
import { V1ContractError } from "../v1/errors";
import { Seb } from "../v1/seb";
import type { V3DecodedSebEntry, V3ImageIndexEntry, V3IndexGroup, V3SebIndexEntry, V3SebResolution } from "./contracts";
import { V3ContractError, V3DeferredError, V3LookupError } from "./errors";
import { IndexedImage } from "./image";

export interface ResourceManagerV3Input {
  readonly groupId: string;
  readonly pack: string | null;
  readonly imageIndex: V3IndexGroup<V3ImageIndexEntry> | null;
  readonly sebIndex: V3IndexGroup<V3DecodedSebEntry | V3SebIndexEntry> | null;
  readonly decodedSebByMember?: ReadonlyMap<string, SebContract>;
}

export type V3LoadState = "ready_static_fixture" | "disposed";

export class ResourceManagerV3 {
  public readonly img: readonly (IndexedImage | null)[];

  public readonly seb: readonly (Seb | null)[];

  public readonly groupId: string;

  public readonly pack: string | null;

  public readonly atlasStatus = "deferred" as const;

  public readonly customImages: ReadonlyMap<number, IndexedImage>;

  public readonly loadState: V3LoadState = "ready_static_fixture";

  private disposed = false;

  private constructor(input: ResourceManagerV3Input) {
    validateInput(input);
    this.groupId = input.groupId;
    this.pack = input.pack;
    this.img = Object.freeze(loadImages(input.groupId, input.imageIndex));
    this.seb = Object.freeze(loadSebs(input.sebIndex, input.decodedSebByMember));
    this.customImages = new Map<number, IndexedImage>();
  }

  public static fromEvidence(input: ResourceManagerV3Input): ResourceManagerV3 {
    return new ResourceManagerV3(input);
  }

  public getImage(id: number): IndexedImage {
    this.ensureLive();
    const validId = requireLookupId(id);
    const custom = this.customImages.get(validId);
    if (custom !== undefined) {
      return custom;
    }
    const image = this.img[validId];
    if (image === undefined || image === null) {
      throw new V3LookupError("RESOURCE_IMAGE_NOT_FOUND", `${this.groupId}: image ID ${validId} is missing`);
    }
    return image;
  }

  public getSeb(id: number): Seb {
    this.ensureLive();
    const validId = requireLookupId(id);
    const seb = this.seb[validId];
    if (seb === undefined || seb === null) {
      throw new V3LookupError("RESOURCE_SEB_NOT_FOUND", `${this.groupId}: SEB ID ${validId} is missing or source-limited`);
    }
    return seb;
  }

  public loadImage(id: number): IndexedImage {
    return this.getImage(id);
  }

  public loadSeb(id: number): Seb {
    return this.getSeb(id);
  }

  public getCustomImage(id: number): IndexedImage | null {
    this.ensureLive();
    const validId = requireLookupId(id);
    return this.customImages.get(validId) ?? null;
  }

  public resolveSebImage(sebId: number, frame = 0, layer = 0): V3SebResolution {
    const seb = this.getSeb(sebId);
    const sprite = seb.getSprite(frame, layer);
    if (sprite === null) {
      throw new V3LookupError("SEB_FRAME_RECORD_NOT_FOUND", `${this.groupId}: SEB ${sebId} has no frame ${frame}`);
    }
    const texId = sprite.TexId;
    if (texId < 0) {
      return { status: "sentinel", groupId: this.groupId, sebId, frame, layer, texId, image: null };
    }
    return { status: "resolved", groupId: this.groupId, sebId, frame, layer, texId, image: this.getImage(texId) };
  }

  public loadReady(): this {
    this.ensureLive();
    return this;
  }

  public loadStart(): this {
    this.ensureLive();
    return this;
  }

  public getAtlas(_id: number): never {
    throw new V3DeferredError(
      "RESOURCE_ATLAS_DEFERRED",
      "Atlas population and GPU lifetime are not statically proven for V3 fixtures.",
    );
  }

  public dispose(): void {
    this.disposed = true;
  }

  private ensureLive(): void {
    if (this.disposed) {
      throw new V3LookupError("RESOURCE_MANAGER_DISPOSED");
    }
  }
}

function loadImages(groupId: string, index: V3IndexGroup<V3ImageIndexEntry> | null): (IndexedImage | null)[] {
  if (index === null) {
    return [];
  }
  const images: (IndexedImage | null)[] = new Array((index.max_id ?? -1) + 1).fill(null);
  for (const entry of index.entries) {
    if (images[entry.id] !== null) {
      throw new V3ContractError("IMAGE_INDEX_DUPLICATE_ID");
    }
    images[entry.id] = new IndexedImage(
      groupId,
      entry.id,
      entry.filename,
      entry.source_index_member,
      entry.source_member,
      entry.source_sha256,
      entry.source_bytes,
      entry.flags,
      entry.alias_ids,
    );
  }
  return images;
}

function loadSebs(
  index: V3IndexGroup<V3DecodedSebEntry | V3SebIndexEntry> | null,
  decodedSebByMember: ReadonlyMap<string, SebContract> | undefined,
): (Seb | null)[] {
  if (index === null) {
    return [];
  }
  const sebs: (Seb | null)[] = new Array((index.max_id ?? -1) + 1).fill(null);
  for (const entry of index.entries) {
    if (sebs[entry.id] !== null) {
      throw new V3ContractError("SEB_INDEX_DUPLICATE_ID");
    }
    const decoded = ("decoded" in entry ? entry.decoded : undefined) ?? decodedSebByMember?.get(entry.source_member);
    if (decoded === undefined) {
      continue;
    }
    try {
      sebs[entry.id] = Seb.fromContract(decoded);
    } catch (error) {
      // The catalog intentionally retains source-limited SEBs whose decoded
      // header is not accepted by the existing V1 contract parser. Preserve
      // the original slot as null instead of inventing a repaired grammar.
      if (error instanceof V1ContractError) {
        continue;
      }
      throw error;
    }
  }
  return sebs;
}

function validateInput(input: ResourceManagerV3Input): void {
  if (input === null || typeof input !== "object" || input.groupId.length === 0) {
    throw new V3ContractError("RESOURCE_GROUP_INPUT_MALFORMED");
  }
  if (input.imageIndex !== null && input.imageIndex.group_id !== input.groupId) {
    throw new V3ContractError("IMAGE_INDEX_GROUP_MISMATCH");
  }
  if (input.sebIndex !== null && input.sebIndex.group_id !== input.groupId) {
    throw new V3ContractError("SEB_INDEX_GROUP_MISMATCH");
  }
}

function requireLookupId(id: number): number {
  if (!Number.isSafeInteger(id) || id < 0) {
    throw new V3LookupError("RESOURCE_ID_MALFORMED");
  }
  return id;
}
