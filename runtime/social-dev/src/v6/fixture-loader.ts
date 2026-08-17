import {
  actorSpawnJson,
  characterAssetManifestJson as assetManifestJson,
  characterCapabilityJson as capabilityJson,
  characterMetadataJson as metadataJson,
  floor00SceneJson as floor00Json,
  nativeDirectionJson as directionJson,
} from "../catalog/load-original-runtime-pack";
import type {
  CharacterAssetImage,
  CharacterAssetManifest,
  CharacterCapabilityContract,
  CharacterMetadataContract,
  Floor00SceneContract,
} from "../catalog/types";
import { createResourceManager } from "../v3/fixture-loader";
import { V4ResourceManager } from "../v4/resources";

export interface NativeDirectionFixture {
  readonly raw_domain: readonly number[];
  readonly raw_values: Readonly<Record<string, {
    readonly label: string;
    readonly vector: readonly [number, number];
    readonly reverse: number;
  }>>;
  readonly native_trace: {
    readonly reverse_table: readonly number[];
  };
}

export interface StaffActorSpawnRecord {
  readonly id: string;
  readonly source_staff_id: number;
  readonly insertion_index: number;
  readonly scene_ref: string;
  readonly spawn_cell: {
    readonly x: number;
    readonly y: number;
    readonly raw_map_value?: number;
  };
  readonly initial_position: { readonly x: number; readonly y: number };
  readonly initial_fields: Readonly<Record<string, { readonly value: unknown }>>;
}

export interface StaffActorSpawnContract {
  readonly actors: readonly StaffActorSpawnRecord[];
}

export interface StaffFixtureCatalog {
  readonly metadata: CharacterMetadataContract;
  readonly capability: CharacterCapabilityContract;
  readonly assets: CharacterAssetManifest;
  readonly actorSpawn: StaffActorSpawnContract;
  readonly floor00: Floor00SceneContract;
  readonly direction: NativeDirectionFixture;
  readonly human: V4ResourceManager;
}

const metadata = metadataJson as CharacterMetadataContract;
const capability = capabilityJson as unknown as CharacterCapabilityContract;
const assets = assetManifestJson as unknown as CharacterAssetManifest;
const actorSpawn = actorSpawnJson as unknown as StaffActorSpawnContract;
const floor00 = floor00Json as unknown as Floor00SceneContract;
const direction = directionJson as unknown as NativeDirectionFixture;

let cachedCatalog: StaffFixtureCatalog | undefined;

export function loadStaffFixtureCatalog(): StaffFixtureCatalog {
  if (cachedCatalog !== undefined) {
    return cachedCatalog;
  }
  const imageDimensions = assets.images.map((image: CharacterAssetImage) => ({
    id: image.selector_id,
    width: image.dimensions.width,
    height: image.dimensions.height,
    role: "resHuman_:staff-image",
  }));
  cachedCatalog = {
    metadata,
    capability,
    assets,
    actorSpawn,
    floor00,
    direction,
    human: new V4ResourceManager(createResourceManager("resHuman_"), imageDimensions),
  };
  return cachedCatalog;
}

export function getStaffMetadata(sourceStaffId: number, catalog = loadStaffFixtureCatalog()) {
  const record = catalog.metadata.staff.find((candidate) => candidate.source_identity.source_id === sourceStaffId);
  if (record === undefined) {
    throw new Error(`V6 StaffData record is missing source ID ${sourceStaffId}`);
  }
  return record;
}

export function getStaffAssetBinding(sourceStaffId: number, catalog = loadStaffFixtureCatalog()) {
  const binding = catalog.assets.staff_bindings.find((candidate) => candidate.source_id === sourceStaffId);
  if (binding === undefined) {
    throw new Error(`V6 Staff asset binding is missing source ID ${sourceStaffId}`);
  }
  return binding;
}

export function getStaffSpawnActor(sourceStaffId: number, catalog = loadStaffFixtureCatalog()): StaffActorSpawnRecord {
  const actor = catalog.actorSpawn.actors.find((candidate) => candidate.source_staff_id === sourceStaffId);
  if (actor === undefined) {
    throw new Error(`V6 actor spawn fixture is missing source ID ${sourceStaffId}`);
  }
  return actor;
}

export function getHumanImageDimension(selectorId: number, catalog = loadStaffFixtureCatalog()) {
  const image = catalog.assets.images.find((candidate) => candidate.selector_id === selectorId);
  if (image === undefined) {
    throw new Error(`V6 human image selector ${selectorId} is missing from the asset manifest`);
  }
  return { width: image.dimensions.width, height: image.dimensions.height };
}
