import { fixtureManifestV4Json as fixtureManifestJson } from "../catalog/load-original-runtime-pack";
import { createResourceManager } from "../v3/fixture-loader";
import { V4CameraBoundary } from "./camera";
import type { V4FurnitureBinding, V4ImageDimension } from "./contracts";
import { V4ResourceManager } from "./resources";

interface V4FixtureManifest {
  readonly resource_group: string;
  readonly image_dimensions: readonly V4ImageDimension[];
  readonly camera: { readonly offset: readonly [number, number] };
  readonly map: { readonly floor_image_selector: number };
  readonly catalog_selector_fixtures: readonly {
    readonly furniture_data_id: number;
    readonly selectors: { readonly seb: number; readonly sub_seb: number; readonly img: number };
  }[];
  readonly furniture_bindings: readonly V4RawFurnitureBinding[];
}

interface V4RawFurnitureBinding {
  readonly object_id: string;
  readonly furniture_data_id: number;
  readonly raw_type: number;
  readonly seb_selector: number;
  readonly sub_seb_selector: number;
  readonly data_img_selector: number;
  readonly render_mode: V4FurnitureBinding["renderMode"];
  readonly image_selector?: number;
  readonly image_source?: readonly [number, number, number, number];
  readonly destination_offset?: readonly [number, number];
  readonly primary_frame?: number;
  readonly secondary_frame?: number;
  readonly cells: readonly (readonly [number, number])[];
}

interface V4FixtureManifestView extends V4FixtureManifest {
  readonly furniture_bindings: readonly (V4RawFurnitureBinding & {
    readonly cells: readonly (readonly [number, number])[];
  })[];
}

const fixtureManifest = fixtureManifestJson as unknown as V4FixtureManifest;

export function createV4ResourceManager(groupId = fixtureManifest.resource_group): V4ResourceManager {
  return new V4ResourceManager(createResourceManager(groupId), fixtureManifest.image_dimensions);
}

export function createV4Camera(): V4CameraBoundary {
  return new V4CameraBoundary({
    x: fixtureManifest.camera.offset[0],
    y: fixtureManifest.camera.offset[1],
  });
}

export function getV4FurnitureBinding(objectId: string): V4FurnitureBinding {
  const binding = fixtureManifest.furniture_bindings.find((candidate) => candidate.object_id === objectId);
  if (binding === undefined) {
    throw new Error(`Unknown V4 furniture fixture ${objectId}`);
  }
  return {
    objectId: binding.object_id,
    furnitureDataId: binding.furniture_data_id,
    rawType: binding.raw_type,
    primarySeb: binding.seb_selector,
    secondarySeb: binding.sub_seb_selector,
    dataImage: binding.data_img_selector,
    renderMode: binding.render_mode,
    imageSelector: binding.image_selector,
    imageSource: binding.image_source === undefined
      ? undefined
      : {
        x: binding.image_source[0],
        y: binding.image_source[1],
        width: binding.image_source[2],
        height: binding.image_source[3],
      },
    destinationOffset: binding.destination_offset === undefined
      ? undefined
      : { x: binding.destination_offset[0], y: binding.destination_offset[1] },
    primaryFrame: binding.primary_frame,
    secondaryFrame: binding.secondary_frame,
  };
}

export function createV4FurnitureBinding(objectId: string): V4FurnitureBinding {
  return getV4FurnitureBinding(objectId);
}

export function getV4FixtureManifest(): V4FixtureManifestView {
  return fixtureManifest;
}
