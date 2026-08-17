import { characterAssetManifestJson } from "../catalog/load-original-runtime-pack";
import { resolveCharacter, resolveCharacterAction } from "../catalog/character-resolver";
import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type {
  CharacterAssetAnimation,
  CharacterAssetFrameRecord,
  CharacterAssetImage,
  CharacterAssetManifest,
} from "../catalog/types";

export interface CharacterDisplayFrame {
  readonly characterId: string;
  readonly action: string;
  readonly direction: string;
  readonly selectorId: number;
  readonly imageAssetId: string;
  readonly imageRuntimePath: string;
  readonly animation: CharacterAssetAnimation;
  readonly records: readonly CharacterAssetFrameRecord[];
}

const characterAssetManifest = characterAssetManifestJson as unknown as CharacterAssetManifest;
const imageByAssetId = new Map(characterAssetManifest.images.map((image) => [image.asset_id, image]));
const animationBySelectorId = new Map(characterAssetManifest.animations.map((animation) => [animation.selector_id, animation]));
const imagePromises = new Map<string, Promise<HTMLImageElement>>();
const loadedImages = new Map<string, HTMLImageElement>();

if (
  characterAssetManifest.catalog_id !== "character-assets-full" ||
  characterAssetManifest.status !== "pass" ||
  characterAssetManifest.semantic_status !== "approved_for_runtime_catalog" ||
  characterAssetManifest.runtime_policy.eager_load_full_catalog !== false
) {
  throw new Error("Character asset manifest is not an approved lazy runtime catalog");
}

export function getCharacterAssetManifest(): CharacterAssetManifest {
  return characterAssetManifest;
}

export function getCharacterImageAsset(assetId: string): CharacterAssetImage | null {
  return imageByAssetId.get(assetId) ?? null;
}

export function getCharacterAnimation(selectorId: number): CharacterAssetAnimation | null {
  return animationBySelectorId.get(selectorId) ?? null;
}

export function getCachedCharacterImage(assetId: string): HTMLImageElement | undefined {
  return loadedImages.get(assetId);
}

export function loadCharacterImage(assetId: string): Promise<HTMLImageElement> {
  const existing = imagePromises.get(assetId);
  if (existing) {
    return existing;
  }
  const asset = getCharacterImageAsset(assetId);
  if (!asset) {
    return Promise.reject(new Error(`Character image asset is missing from manifest: ${assetId}`));
  }
  const promise = new Promise<HTMLImageElement>((resolve, reject) => {
    const image = new Image();
    image.decoding = "async";
    image.onload = () => {
      loadedImages.set(assetId, image);
      resolve(image);
    };
    image.onerror = () => reject(new Error(`Character image failed to load: ${asset.runtime_path}`));
    image.src = new URL(`./${asset.runtime_path}`, document.baseURI).toString();
  });
  imagePromises.set(assetId, promise);
  return promise;
}

export function preloadCharacterImage(catalogs: RuntimeCatalogs, characterId: string): Promise<HTMLImageElement> {
  const resolved = resolveCharacter(catalogs, characterId);
  const assetId = resolved.imageSelector?.asset?.asset_id;
  if (!assetId) {
    return Promise.reject(new Error(`Character ${characterId} has no resolved image asset`));
  }
  return loadCharacterImage(assetId);
}

/**
 * Resolve a decoded frame's image slot to the physical runtime image.
 *
 * Native human SEBs use image_id 0 as the current character image slot. The
 * manifest retains chara00.png as the source slot reference for provenance,
 * but runtime StaffData bindings replace that slot with the character's own
 * selected image. Other image IDs remain direct promoted asset references.
 */
export function characterFrameRecordAssetId(
  record: CharacterAssetFrameRecord,
  defaultAssetId: string,
): string | null {
  if (record.texture_status !== "resolved") {
    return null;
  }
  return record.image_id === 0 ? defaultAssetId : record.source_asset_id ?? defaultAssetId;
}

export function characterFrameAssetIds(frame: CharacterDisplayFrame): readonly string[] {
  const assetIds = new Set<string>([frame.imageAssetId]);
  for (const record of frame.records) {
    const assetId = characterFrameRecordAssetId(record, frame.imageAssetId);
    if (assetId) {
      assetIds.add(assetId);
    }
  }
  return [...assetIds];
}

export function preloadCharacterFrameImages(frame: CharacterDisplayFrame): Promise<readonly string[]> {
  const assetIds = characterFrameAssetIds(frame);
  return Promise.all(assetIds.map((assetId) => loadCharacterImage(assetId))).then(() => assetIds);
}

function normalizeFrame(frame: number, frameBound: number): number {
  if (!Number.isFinite(frameBound) || frameBound <= 0) {
    return 0;
  }
  const normalized = Math.floor(frame) % frameBound;
  return normalized < 0 ? normalized + frameBound : normalized;
}

function selectLayerRecord(layer: CharacterAssetAnimation["layers"][number], frame: number): CharacterAssetFrameRecord | null {
  const normalized = normalizeFrame(frame, layer.frame_bound);
  let selected: CharacterAssetFrameRecord | null = null;
  for (const record of layer.records) {
    if (record.start_frame <= normalized) {
      selected = record;
    } else {
      break;
    }
  }
  return selected;
}

export function selectCharacterAnimationRecords(
  animation: CharacterAssetAnimation,
  frame: number,
): readonly CharacterAssetFrameRecord[] {
  return animation.layers
    .map((layer) => selectLayerRecord(layer, frame))
    .filter((record): record is CharacterAssetFrameRecord => record !== null)
    .sort((left, right) => left.layer - right.layer || left.layer_record_index - right.layer_record_index);
}

export function characterDisplayFrame(
  catalogs: RuntimeCatalogs,
  characterId: string,
  action: string,
  direction: "right" | "left" | "up" | "down" = "right",
  frame = 0,
): CharacterDisplayFrame | null {
  const actionResolution = resolveCharacterAction(catalogs, characterId, action, direction);
  const selectorId = actionResolution.selector?.selector_id;
  if (selectorId === undefined) {
    return null;
  }
  const resolved = resolveCharacter(catalogs, characterId);
  const imageAssetId = resolved.imageSelector?.asset?.asset_id;
  const image = imageAssetId ? getCharacterImageAsset(imageAssetId) : null;
  const animation = getCharacterAnimation(selectorId);
  if (!imageAssetId || !image || !animation) {
    return null;
  }
  return {
    characterId,
    action,
    direction,
    selectorId,
    imageAssetId,
    imageRuntimePath: image.runtime_path,
    animation,
    records: selectCharacterAnimationRecords(animation, frame),
  };
}

/** Resolve a source-backed selector directly for native phase poses. */
export function characterDisplayFrameForSelector(
  catalogs: RuntimeCatalogs,
  characterId: string,
  action: string,
  direction: "right" | "left" | "up" | "down",
  selectorId: number,
  frame = 0,
): CharacterDisplayFrame | null {
  const resolved = resolveCharacter(catalogs, characterId);
  const imageAssetId = resolved.imageSelector?.asset?.asset_id;
  const image = imageAssetId ? getCharacterImageAsset(imageAssetId) : null;
  const animation = getCharacterAnimation(selectorId);
  if (!imageAssetId || !image || !animation) return null;
  return {
    characterId,
    action,
    direction,
    selectorId,
    imageAssetId,
    imageRuntimePath: image.runtime_path,
    animation,
    records: selectCharacterAnimationRecords(animation, frame),
  };
}
