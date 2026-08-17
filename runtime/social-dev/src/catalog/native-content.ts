import type { RuntimeCatalogs } from "./load-contracts";
import type { NativeContentCatalogContract } from "./types";

type NativeCatalogRecord = Readonly<Record<string, unknown>>;
type NativeDataRecord = NativeContentCatalogContract["data_records"][number];

export interface NativeIdResolution {
  readonly id: string;
  readonly dataRecord?: NativeDataRecord;
  readonly selector?: NativeCatalogRecord;
  readonly asset?: NativeCatalogRecord;
  readonly connections: readonly NativeCatalogRecord[];
}

function connectionRows(catalogs: RuntimeCatalogs): readonly NativeCatalogRecord[] {
  const groups = catalogs.nativeContent.connections;
  return [
    ...groups.data_selector,
    ...groups.selector_asset_and_companion,
    ...groups.consumer,
    ...groups.lifecycle,
  ];
}

export function findNativeDataRecord(catalogs: RuntimeCatalogs, recordId: string): NativeDataRecord | undefined {
  return catalogs.nativeContent.data_records.find((record) => record.record_id === recordId);
}

export function findNativeSelector(catalogs: RuntimeCatalogs, selectorKey: string): NativeCatalogRecord | undefined {
  return catalogs.nativeContent.selectors.find((selector) => selector.selector_key === selectorKey);
}

export function findNativeAsset(catalogs: RuntimeCatalogs, assetId: string): NativeCatalogRecord | undefined {
  return catalogs.nativeContent.assets.find((asset) => asset.asset_id === assetId);
}

export function findNativeConnections(catalogs: RuntimeCatalogs, id: string): readonly NativeCatalogRecord[] {
  return connectionRows(catalogs).filter((connection) => connection.from === id || connection.to === id);
}

export function resolveNativeId(catalogs: RuntimeCatalogs, id: string): NativeIdResolution {
  return {
    id,
    dataRecord: findNativeDataRecord(catalogs, id),
    selector: findNativeSelector(catalogs, id),
    asset: findNativeAsset(catalogs, id),
    connections: findNativeConnections(catalogs, id),
  };
}
