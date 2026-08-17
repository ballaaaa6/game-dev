import { fixtureManifestV4Json as v4FixtureJson } from "../catalog/load-original-runtime-pack";
import { createResourceManager } from "../v3/fixture-loader";
import { V4CameraBoundary } from "../v4/camera";
import type { V4FurnitureBinding, V4ImageDimension, V4CameraOffset } from "../v4/contracts";
import { createV4FurnitureBinding, getV4FixtureManifest } from "../v4/fixture-loader";
import { V4ResourceManager } from "../v4/resources";
import type { V5StructuralFacility } from "./contracts";
import { createV5MapCamera, createV5ObjectCamera } from "./coordinate-bridge";

interface V4FixtureShape {
  readonly resource_group: string;
  readonly image_dimensions: readonly V4ImageDimension[];
}

const v4Fixture = v4FixtureJson as unknown as V4FixtureShape;

export function createV5ResourceManager(): V4ResourceManager {
  const dimensions = new Map(v4Fixture.image_dimensions.map((dimension) => [dimension.id, dimension]));
  // The native room:0 facility fixture is a proven big_base00.seb → image 18
  // composition. Its source dimensions come from the same sprite record; V5
  // extends the V4 dimension boundary only for that explicit structural input.
  dimensions.set(18, { id: 18, width: 120, height: 61, role: "room:0 structural facility" });
  return new V4ResourceManager(createResourceManager(v4Fixture.resource_group), [...dimensions.values()]);
}

export function createV5Camera(offset: V4CameraOffset = { x: 0, y: 0 }): V4CameraBoundary {
  return createV5ObjectCamera(offset);
}

export function createV5MapDrawCamera(offset: V4CameraOffset = { x: 0, y: 0 }): V4CameraBoundary {
  return createV5MapCamera(offset);
}

export function createV5FurnitureBinding(objectId: string): V4FurnitureBinding {
  const binding = createV4FurnitureBinding(objectId);
  const fixture = getV4FixtureManifest().furniture_bindings.find((candidate) => candidate.object_id === objectId);
  if (fixture === undefined || binding.objectId !== objectId) {
    throw new Error(`V5 explicit FurnitureData binding is missing ${objectId}`);
  }
  return binding;
}

export function createV5StructuralBinding(facility: V5StructuralFacility): V4FurnitureBinding {
  return {
    objectId: facility.objectId,
    furnitureDataId: facility.furnitureDataId,
    rawType: facility.rawType,
    primarySeb: facility.primarySeb,
    secondarySeb: facility.secondarySeb,
    dataImage: facility.imageSelector,
    renderMode: "primary_seb_plus_secondary_seb",
    primaryFrame: 0,
  };
}
