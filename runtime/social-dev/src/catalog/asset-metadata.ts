import type {
  AssetMetadataRuntimeAsset,
  NativeContentCatalogContract,
} from "./types";
import type { RuntimeCatalogs } from "./load-contracts";

export type AssetMetadataLookupStatus =
  | "runtime_ready"
  | "catalog_only"
  | "missing_selector"
  | "unresolved_selector_target"
  | "missing_asset";

export interface RuntimeAssetMetadataResolution {
  readonly status: AssetMetadataLookupStatus;
  readonly selector_key?: string;
  readonly asset_id?: string;
  readonly selector?: Readonly<Record<string, unknown>>;
  readonly asset?: Readonly<Record<string, unknown>>;
  readonly runtime_metadata?: AssetMetadataRuntimeAsset;
}

export interface FurnitureMetadataResolution {
  readonly status: "resolved" | "missing";
  readonly record_id: string;
  readonly record?: NativeContentCatalogContract["data_records"][number];
  readonly selector_references: readonly Readonly<Record<string, unknown>>[];
}

function selectorKey(resourceScope: string, selectorKind: string, selectorId: number): string {
  return `ref:${resourceScope}:${selectorKind}:${selectorId}`;
}

function runtimeAsset(catalogs: RuntimeCatalogs, assetId: string): AssetMetadataRuntimeAsset | undefined {
  return catalogs.assetMetadataRuntime.runtime_assets.find((asset) => asset.asset_id === assetId);
}

export function findRuntimeAssetMetadata(catalogs: RuntimeCatalogs, assetId: string): AssetMetadataRuntimeAsset | undefined {
  return runtimeAsset(catalogs, assetId);
}

export function findRuntimeFamilyAssets(catalogs: RuntimeCatalogs, familyId: string): readonly AssetMetadataRuntimeAsset[] {
  const family = catalogs.assetMetadataRuntime.family_manifests.find((item) => item.family_id === familyId);
  if (!family) {
    return [];
  }
  return family.runtime_asset_ids
    .map((assetId) => runtimeAsset(catalogs, assetId))
    .filter((asset): asset is AssetMetadataRuntimeAsset => Boolean(asset));
}

export function resolveNativeSelectorAsset(
  catalogs: RuntimeCatalogs,
  resourceScope: string,
  selectorKind: string,
  selectorId: number,
): RuntimeAssetMetadataResolution {
  return resolveNativeSelectorAssetByKey(catalogs, selectorKey(resourceScope, selectorKind, selectorId));
}

export function resolveNativeSelectorAssetByKey(catalogs: RuntimeCatalogs, key: string): RuntimeAssetMetadataResolution {
  const selector = catalogs.nativeContent.selectors.find((candidate) => candidate.selector_key === key);
  if (!selector) {
    return { status: "missing_selector", selector_key: key };
  }
  const selectorRecord = selector as Readonly<Record<string, unknown>>;
  const assetId = typeof selectorRecord.target_asset_id === "string" ? selectorRecord.target_asset_id : undefined;
  if (!assetId) {
    return { status: "unresolved_selector_target", selector_key: key, selector: selectorRecord };
  }
  const asset = catalogs.nativeContent.assets.find((candidate) => candidate.asset_id === assetId) as Readonly<Record<string, unknown>> | undefined;
  if (!asset) {
    return { status: "missing_asset", selector_key: key, asset_id: assetId, selector: selectorRecord };
  }
  return {
    status: runtimeAsset(catalogs, assetId) ? "runtime_ready" : "catalog_only",
    selector_key: key,
    asset_id: assetId,
    selector: selectorRecord,
    asset,
    runtime_metadata: runtimeAsset(catalogs, assetId),
  };
}

export function findFurnitureMetadata(catalogs: RuntimeCatalogs, furnitureId: number): FurnitureMetadataResolution {
  const recordId = `data:furniture:${furnitureId}`;
  const record = catalogs.nativeContent.data_records.find((candidate) => candidate.record_id === recordId);
  if (!record) {
    return { status: "missing", record_id: recordId, selector_references: [] };
  }
  const selectorReferences = catalogs.nativeContent.connections.data_selector.filter(
    (connection) => connection.from === recordId,
  );
  return { status: "resolved", record_id: recordId, record, selector_references: selectorReferences };
}
