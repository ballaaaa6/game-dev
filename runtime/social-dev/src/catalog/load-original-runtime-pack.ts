import runtimePackJson from "../../generated/original-runtime-pack.json";

// K2 makes the generated original runtime pack the only JSON data entry point
// for production code.  The named aliases keep the pre-K2 module contracts
// stable while moving provenance and packaging behind one facade.
export const k2RuntimePack = runtimePackJson.runtime_catalogs;

export const actorCatalogJson = k2RuntimePack.actorCatalogJson;
export const actorBehaviorJson = k2RuntimePack.actorBehaviorJson;
export const actorSpawnJson = k2RuntimePack.actorSpawnJson;
export const cameraCoordinateJson = k2RuntimePack.cameraCoordinateJson;
export const characterCapabilityJson = k2RuntimePack.characterCapabilityJson;
export const characterAssetManifestJson = k2RuntimePack.characterAssetManifestJson;
export const characterMetadataJson = k2RuntimePack.characterMetadataJson;
export const displayAssetManifestJson = k2RuntimePack.displayAssetManifestJson;
export const objectCatalogJson = k2RuntimePack.objectCatalogJson;
export const preRuntimeClosureJson = k2RuntimePack.preRuntimeClosureJson;
export const phase3cRenderJson = k2RuntimePack.phase3cRenderJson;
export const roomPlacementJson = k2RuntimePack.roomPlacementJson;
export const sceneCatalogJson = k2RuntimePack.sceneCatalogJson;
export const strictClosureJson = k2RuntimePack.strictClosureJson;
export const tickOrderJson = k2RuntimePack.tickOrderJson;
export const defaultMapChipJson = k2RuntimePack.defaultMapChipJson;
export const roomSceneRuntimeJson = k2RuntimePack.roomSceneRuntimeJson;
export const nativeDirectionJson = k2RuntimePack.nativeDirectionJson;
export const roomSceneAssetManifestJson = k2RuntimePack.roomSceneAssetManifestJson;
export const roomRSceneJson = k2RuntimePack.roomRSceneJson;
export const nativeContentCatalogJson = k2RuntimePack.nativeContentCatalogJson;
export const nativeSceneAssemblyJson = k2RuntimePack.nativeSceneAssemblyJson;
export const nativeRoomFloorUsageJson = k2RuntimePack.nativeRoomFloorUsageJson;
export const assetMetadataRuntimeManifestJson = k2RuntimePack.assetMetadataRuntimeManifestJson;
export const i0RuntimeCatalogJson = k2RuntimePack.i0RuntimeCatalogJson;
export const floor00SceneJson = k2RuntimePack.floor00SceneJson;
export const floor00DisplayPolicyJson = k2RuntimePack.floor00DisplayPolicyJson;
export const floor00VisualLayoutJson = k2RuntimePack.floor00VisualLayoutJson;

export const fixtureManifestV1Json = k2RuntimePack.fixtureManifestV1Json;
export const imageOptContractV1Json = k2RuntimePack.imageOptContractV1Json;
export const resourceLookupContractV1Json = k2RuntimePack.resourceLookupContractV1Json;
export const sebContractV1Json = k2RuntimePack.sebContractV1Json;
export const rasterFixtureManifestV2Json = k2RuntimePack.rasterFixtureManifestV2Json;
export const fixtureManifestV3Json = k2RuntimePack.fixtureManifestV3Json;
export const groupMapV3Json = k2RuntimePack.groupMapV3Json;
export const imgIndexV3Json = k2RuntimePack.imgIndexV3Json;
export const sebIndexV3Json = k2RuntimePack.sebIndexV3Json;
export const packInventoryV3Json = k2RuntimePack.packInventoryV3Json;
export const sebCatalogJson = k2RuntimePack.sebCatalogJson;
export const fixtureManifestV4Json = k2RuntimePack.fixtureManifestV4Json;
