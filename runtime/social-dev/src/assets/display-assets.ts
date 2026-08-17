import {
  displayAssetManifestJson as manifestJson,
  defaultMapChipJson,
  roomSceneAssetManifestJson,
} from "../catalog/load-original-runtime-pack";
import { resolveFloorRender, type FloorRenderResolution } from "../catalog/floor-resolution";

export { resolveRuntimeMapFilename } from "../catalog/floor-resolution";

export type DisplayAnimationMode = "wait" | "typing";
export type DisplayAssetStatus = "loading" | "ready" | "fallback";

export interface DisplayFrameRecord {
  readonly start_frame: number;
  readonly image_id: number;
  readonly source_x: number;
  readonly source_y: number;
  readonly width: number;
  readonly height: number;
  readonly destination_x: number;
  readonly destination_y: number;
  readonly flags: number;
  readonly reserved: number;
  readonly source_asset_slot?: string;
  readonly source_asset_member?: string;
  readonly source_asset_id?: string;
  readonly source_size?: { readonly width: number; readonly height: number };
  readonly source_status?: string;
  /** Physical image used by the browser after any offline OPT reconstruction. */
  readonly runtime_asset_member?: string;
  readonly runtime_asset_id?: string;
  readonly runtime_size?: { readonly width: number; readonly height: number };
  readonly runtime_status?: string;
}

export interface DisplayAnimation {
  readonly selector_id: number;
  readonly filename: string;
  readonly asset_id: string;
  readonly frame_bound: number;
  readonly global_frame_count: number;
  readonly records: readonly DisplayFrameRecord[];
  readonly binding: string;
  readonly status: string;
}

export interface DisplayAssetRecord {
  readonly asset_id: string;
  readonly asset_member: string;
  readonly runtime_path: string;
  readonly extension: string;
  readonly sha256: string;
  readonly kind?: string;
  readonly width?: number;
  readonly height?: number;
  readonly provenance?: Readonly<Record<string, unknown>>;
}

export interface DisplayActorBinding {
  readonly actor_source_id: number;
  readonly image_selector_id: number;
  readonly image_asset_id: string;
  readonly image_asset_member: string;
  readonly image_size: { readonly width: number; readonly height: number };
  readonly animations: Readonly<Record<DisplayAnimationMode, DisplayAnimation>>;
  readonly status: string;
}

export interface DisplaySourceComposition {
  readonly image_id: number;
  readonly source_asset_member: string;
  readonly source_asset_id: string;
  readonly source_size: { readonly width: number; readonly height: number };
  readonly opt_asset_member?: string;
  readonly opt_asset_id?: string;
  readonly opt_status: string;
  readonly logical_size?: { readonly width: number; readonly height: number } | null;
  readonly logical_pixel_sha256?: string | null;
  readonly opt_issues?: readonly string[];
  readonly runtime_asset_member?: string;
  readonly runtime_asset_id?: string;
  readonly runtime_size?: { readonly width: number; readonly height: number };
  readonly runtime_status?: string;
}

export interface DisplaySubComposition {
  readonly selector_id: number;
  readonly filename: string;
  readonly asset_id: string;
  readonly asset_member: string;
  readonly header: {
    readonly layer_count: number;
    readonly global_frame_count: number;
    readonly record_count: number;
    readonly frame_bound: number;
  };
  readonly records: readonly DisplayFrameRecord[];
  readonly composition_issues: readonly string[];
  readonly source_compositions: readonly DisplaySourceComposition[];
  readonly status: string;
}

export interface DisplayObjectBinding {
  readonly object_id: string;
  readonly name: string;
  readonly seb_selector_id: number;
  readonly seb_asset_member: string;
  readonly seb_asset_id: string;
  readonly header: {
    readonly layer_count: number;
    readonly global_frame_count: number;
    readonly record_count: number;
    readonly frame_bound: number;
  };
  readonly records: readonly DisplayFrameRecord[];
  readonly composition_issues: readonly string[];
  readonly source_compositions?: readonly DisplaySourceComposition[];
  readonly sub_composition?: DisplaySubComposition | null;
  readonly phase3a_closure?: {
    readonly status: string;
    readonly reason_code?: string | null;
  };
  readonly status: string;
}

export interface DisplayNativeInitialObjectBinding extends DisplayObjectBinding {
  readonly furniture_data_id: number;
  readonly raw_type: number;
  readonly seb_selector_id: number;
  readonly sub_seb_selector_id: number;
  readonly img_selector_id: number;
  readonly img_filename?: string | null;
  readonly selector_flag: "FLAG_INIT_DESK" | "FLAG_INIT_PLACE";
  readonly native_status: string;
  readonly display_mode: "native_selector_composition" | "native_type1_direct_img";
}

export interface DisplayPhase3AStatus {
  readonly target: "furniture:2";
  readonly status: "approved" | "quarantined_source_limitation" | "pending";
  readonly reason_code?: string | null;
  readonly runtime_promotion: "approved" | "not_promoted";
  readonly closure_path: string;
}

export interface DisplayAssetManifest {
  readonly schema_version: string;
  readonly package: string;
  readonly status: string;
  readonly semantic_status: string;
  readonly scope: string;
  readonly phase3a: DisplayPhase3AStatus;
  readonly assets: readonly DisplayAssetRecord[];
  readonly actors: readonly DisplayActorBinding[];
  readonly objects: Readonly<Record<string, DisplayObjectBinding>>;
  readonly native_initial_objects: Readonly<Record<string, DisplayNativeInitialObjectBinding>>;
  readonly runtime_policy: {
    readonly fallback: string;
    readonly unapproved_assets_are_not_loaded: boolean;
    readonly source_code_imports: boolean;
  };
}

export interface LoadedDisplayAssets {
  readonly status: "ready";
  readonly manifest: DisplayAssetManifest;
  readonly floorRender: FloorRenderResolution;
  readonly images: ReadonlyMap<string, HTMLImageElement>;
  readonly mapImages: ReadonlyMap<string, HTMLImageElement>;
  readonly ambientImages: ReadonlyMap<string, HTMLImageElement>;
}

export type NativeInitialObjectId = "furniture:3" | "furniture:12" | "furniture:26" | "furniture:56";

export interface FurnitureDisplayFrame<TObject extends DisplayObjectBinding = DisplayObjectBinding> {
  readonly object: TObject;
  readonly frame: DisplayFrameRecord;
  readonly imageAssetId?: string;
  readonly subFrame?: DisplayFrameRecord;
  readonly subImageAssetId?: string;
}

/**
 * The native computer is a static room prop in the unified main scene. The
 * approved floor00 presentation freezes the other native compositions too.
 */
export function furnitureFrameForScene(
  objectId: string,
  frame: number,
  sceneMode: "floor00",
): FurnitureDisplayFrame<DisplayObjectBinding | DisplayNativeInitialObjectBinding> | null {
  return furnitureDisplayFrame(objectId, sceneMode === "floor00" ? 0 : frame);
}

export const displayAssetManifest = validateManifest(manifestJson as unknown as DisplayAssetManifest);

function validateManifest(candidate: DisplayAssetManifest): DisplayAssetManifest {
  if (
    candidate.schema_version !== "social-dev-display-asset-manifest-v1" ||
    candidate.package !== "display-slice-01" ||
    candidate.status !== "pass" ||
    candidate.semantic_status !== "approved_for_runtime_subset" ||
    !candidate.phase3a ||
    candidate.phase3a.target !== "furniture:2" ||
    !["approved", "quarantined_source_limitation", "pending"].includes(candidate.phase3a.status) ||
    !["approved", "not_promoted"].includes(candidate.phase3a.runtime_promotion) ||
    candidate.runtime_policy.unapproved_assets_are_not_loaded !== true ||
    candidate.runtime_policy.source_code_imports !== false
  ) {
    throw new Error("Display asset manifest is not an approved runtime subset");
  }
  if (
    candidate.actors.length !== 5 ||
    !candidate.objects["furniture:0"] ||
    !candidate.native_initial_objects ||
    Object.keys(candidate.native_initial_objects).sort().join(",") !==
      ["furniture:12", "furniture:26", "furniture:3", "furniture:56"].join(",")
  ) {
    throw new Error("Display asset manifest does not contain the required bounded slice");
  }
  const nativeDesk = candidate.native_initial_objects["furniture:3"];
  if (
    nativeDesk.furniture_data_id !== 3 ||
    nativeDesk.selector_flag !== "FLAG_INIT_DESK" ||
    nativeDesk.display_mode !== "native_selector_composition" ||
    nativeDesk.seb_selector_id !== 1 ||
    nativeDesk.sub_seb_selector_id !== 3
  ) {
    throw new Error("Native FurnitureData(3) binding is not source-backed");
  }
  for (const objectId of ["furniture:12", "furniture:26", "furniture:56"] as const) {
    const nativeObject = candidate.native_initial_objects[objectId];
    if (
      nativeObject.selector_flag !== "FLAG_INIT_PLACE" ||
      nativeObject.display_mode !== "native_type1_direct_img" ||
      nativeObject.seb_selector_id !== 21 ||
      nativeObject.sub_seb_selector_id !== -1 ||
      nativeObject.records[0]?.source_status !== "pass_native_img_asset"
    ) {
      throw new Error(`Native ${objectId} binding is not source-backed`);
    }
  }
  if (candidate.phase3a.status === "quarantined_source_limitation" && candidate.objects["furniture:2"]) {
    throw new Error("Quarantined furniture:2 must not be present in the runtime manifest");
  }
  if (candidate.phase3a.status === "approved" && !candidate.objects["furniture:2"]) {
    throw new Error("Approved furniture:2 must be present in the runtime manifest");
  }
  if (candidate.assets.some((asset) => !asset.runtime_path.startsWith("assets/display-slice-01/"))) {
    throw new Error("Display asset manifest contains an asset outside the runtime asset boundary");
  }
  const assetsById = new Map(candidate.assets.map((asset) => [asset.asset_id, asset]));
  const validateObjectFrames = (label: string, records: readonly DisplayFrameRecord[]): void => {
    for (const [index, record] of records.entries()) {
      const runtimeAssetId = record.runtime_asset_id ?? record.source_asset_id;
      if (!runtimeAssetId) {
        throw new Error(`${label}[${index}] has no runtime asset identity`);
      }
      const asset = assetsById.get(runtimeAssetId);
      if (!asset || typeof asset.width !== "number" || typeof asset.height !== "number") {
        throw new Error(`${label}[${index}] runtime asset ${runtimeAssetId} is not a bounded PNG asset`);
      }
      const size = record.runtime_size ?? { width: asset.width, height: asset.height };
      if (
        record.source_x < 0 ||
        record.source_y < 0 ||
        record.width <= 0 ||
        record.height <= 0 ||
        record.source_x + record.width > size.width ||
        record.source_y + record.height > size.height
      ) {
        throw new Error(`${label}[${index}] frame rectangle exceeds runtime asset ${runtimeAssetId}`);
      }
      if (record.runtime_status && !record.runtime_status.startsWith("pass")) {
        throw new Error(`${label}[${index}] runtime status is ${record.runtime_status}`);
      }
    }
  };
  for (const [objectId, object] of Object.entries(candidate.objects)) {
    validateObjectFrames(`${objectId}.records`, object.records);
    if (object.sub_composition) {
      validateObjectFrames(`${objectId}.sub_composition.records`, object.sub_composition.records);
    }
  }
  for (const [objectId, object] of Object.entries(candidate.native_initial_objects)) {
    validateObjectFrames(`${objectId}.records`, object.records);
  }
  for (const actor of candidate.actors) {
    const asset = assetsById.get(actor.image_asset_id);
    if (!asset || typeof asset.width !== "number" || typeof asset.height !== "number") {
      throw new Error(`Actor ${actor.actor_source_id} image asset is not bounded`);
    }
    for (const [mode, animation] of Object.entries(actor.animations)) {
      for (const [index, record] of animation.records.entries()) {
        const size = record.source_size ?? { width: asset.width, height: asset.height };
        if (record.source_x < 0 || record.source_y < 0 || record.source_x + record.width > size.width || record.source_y + record.height > size.height) {
          throw new Error(`Actor ${actor.actor_source_id} ${mode}[${index}] frame exceeds source bounds`);
        }
      }
    }
  }
  return candidate;
}

function normalizeFrame(frame: number, frameBound: number): number {
  if (!Number.isInteger(frame) || frameBound <= 0) {
    return 0;
  }
  return ((frame % frameBound) + frameBound) % frameBound;
}

export function selectDisplayFrame(animation: DisplayAnimation, frame: number): DisplayFrameRecord {
  return selectFrameRecord(animation.records, animation.frame_bound, frame);
}

function selectFrameRecord(records: readonly DisplayFrameRecord[], frameBound: number, frame: number): DisplayFrameRecord {
  const normalized = normalizeFrame(frame, frameBound);
  const sortedRecords = [...records].sort((left, right) => left.start_frame - right.start_frame);
  const first = sortedRecords[0];
  if (!first) {
    throw new Error("Display composition has no frame records");
  }
  let selected = first;
  for (const record of sortedRecords) {
    if (record.start_frame <= normalized) {
      selected = record;
    } else {
      break;
    }
  }
  return selected;
}

export function actorDisplayFrame(
  sourceId: number,
  mode: DisplayAnimationMode,
  selectorId: number,
  frame: number,
): { readonly actor: DisplayActorBinding; readonly imageAssetId: string; readonly frame: DisplayFrameRecord } | null {
  const actor = displayAssetManifest.actors.find((candidate) => candidate.actor_source_id === sourceId);
  if (!actor) {
    return null;
  }
  const animation = actor.animations[mode];
  if (!animation || animation.selector_id !== selectorId) {
    return null;
  }
  return {
    actor,
    imageAssetId: actor.image_asset_id,
    frame: selectDisplayFrame(animation, frame),
  };
}

export function furnitureDisplayFrame(
  objectId: NativeInitialObjectId,
  frame?: number,
): FurnitureDisplayFrame<DisplayNativeInitialObjectBinding> | null;
export function furnitureDisplayFrame(
  objectId?: string,
  frame?: number,
): FurnitureDisplayFrame<DisplayObjectBinding | DisplayNativeInitialObjectBinding> | null;
export function furnitureDisplayFrame(
  objectId = "furniture:0",
  frame = 0,
): FurnitureDisplayFrame<DisplayObjectBinding | DisplayNativeInitialObjectBinding> | null {
  const object = displayAssetManifest.objects[objectId] ?? displayAssetManifest.native_initial_objects[objectId];
  if (!object || object.records.length === 0) {
    return null;
  }
  const mainFrame = selectFrameRecord(object.records, object.header.frame_bound, frame);
  const subComposition = object.sub_composition;
  const subFrame = subComposition && subComposition.records.length > 0
    ? selectFrameRecord(subComposition.records, subComposition.header.frame_bound, frame)
    : undefined;
  return {
    object,
    frame: mainFrame,
    imageAssetId: mainFrame.runtime_asset_id ?? mainFrame.source_asset_id,
    subFrame,
    subImageAssetId: subFrame?.runtime_asset_id ?? subFrame?.source_asset_id,
  };
}

function resolveAssetUrl(asset: DisplayAssetRecord): string {
  return new URL(`./${asset.runtime_path}`, document.baseURI).toString();
}

function resolveMapAssetUrl(runtimePath: string): string {
  return new URL(`./${runtimePath}`, document.baseURI).toString();
}

function loadImage(asset: DisplayAssetRecord): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.decoding = "async";
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error(`Display asset failed to load: ${asset.asset_member}`));
    image.src = resolveAssetUrl(asset);
  });
}

export async function loadDisplayAssets(): Promise<LoadedDisplayAssets> {
  const imageAssets = displayAssetManifest.assets.filter((asset) => asset.extension.toLowerCase() === ".png");
  const loaded = await Promise.all(imageAssets.map(async (asset) => [asset.asset_id, await loadImage(asset)] as const));
  const mapContract = defaultMapChipJson as {
    readonly source_assets: {
      readonly files: Readonly<Record<string, { readonly runtime_path: string }>>;
      readonly ambient_assets?: Readonly<Record<string, { readonly runtime_path: string }>>;
    };
  };
  const floorRender = resolveFloorRender();
  const mapFiles = mapContract.source_assets.files;
  const loadedMap = await Promise.all(
    Object.entries(mapFiles).map(async ([filename, asset]) => {
        const image = await new Promise<HTMLImageElement>((resolve, reject) => {
          const candidate = new Image();
          candidate.decoding = "async";
          candidate.onload = () => resolve(candidate);
          candidate.onerror = () => reject(new Error(`Map asset failed to load: ${filename}`));
          candidate.src = resolveMapAssetUrl(asset.runtime_path);
        });
        return [`map:chip/${filename}`, image] as const;
      }),
  );
  const roomAssets = roomSceneAssetManifestJson as { readonly assets: readonly DisplayAssetRecord[] };
  const loadedRoomAssets = await Promise.all(
    roomAssets.assets.map(async (asset) => [asset.asset_id, await loadImage(asset)] as const),
  );
  const mapImages = new Map([...loadedMap, ...loadedRoomAssets]);
  const runtimeFloorKey = floorRender.assetId;
  const runtimeFloorImage = mapImages.get(runtimeFloorKey);
  if (!runtimeFloorImage) {
    throw new Error(`Map asset failed to load: ${floorRender.filename}`);
  }
  const ambientFiles = (defaultMapChipJson as {
    readonly source_assets: {
      readonly ambient_assets?: Readonly<Record<string, { readonly runtime_path: string }>>;
    };
  }).source_assets.ambient_assets ?? {};
  const loadedAmbient = await Promise.all(
    Object.entries(ambientFiles).map(async ([filename, asset]) => {
      const image = await new Promise<HTMLImageElement>((resolve, reject) => {
        const candidate = new Image();
        candidate.decoding = "async";
        candidate.onload = () => resolve(candidate);
        candidate.onerror = () => reject(new Error(`Ambient asset failed to load: ${filename}`));
        candidate.src = resolveMapAssetUrl(asset.runtime_path);
      });
      return [filename, image] as const;
    }),
  );
  return {
    status: "ready",
    manifest: displayAssetManifest,
    floorRender,
    images: new Map(loaded),
    mapImages,
    ambientImages: new Map(loadedAmbient),
  };
}
