import { defaultMapChipJson } from "./load-original-runtime-pack";
import type { DefaultMapChipContract } from "./types";

// Raw floor id 5 has no authoritative img.inf mapping in the supplied pack.
// Runtime therefore has one explicit composition: retain selector/data identity
// 85/floor_09.png while rendering the valid floor_05.png pixels. This is an
// approved synthetic composition, not native mapping recovery.
export interface FloorRenderResolution {
  readonly selectorId: number;
  readonly filename: string;
  readonly assetId: `map:chip/${string}`;
  readonly metadataSelectorId: number;
  readonly metadataFilename: string;
  readonly resolutionStatus: string;
  readonly resolutionMode: string;
  readonly sourceStatus: string;
  readonly synthetic: true;
}

const defaultMap = defaultMapChipJson as unknown as DefaultMapChipContract;

export function resolveFloorRender(): FloorRenderResolution {
  const remap = defaultMap.floor_selector_remap;
  return {
    selectorId: remap.runtime_selector_id,
    filename: remap.runtime_render_filename,
    assetId: `map:chip/${remap.runtime_render_filename}`,
    metadataSelectorId: remap.runtime_selector_id,
    metadataFilename: remap.runtime_filename,
    resolutionStatus: remap.runtime_resolution_status,
    resolutionMode: remap.runtime_render_resolution_mode,
    sourceStatus: remap.runtime_render_source_status,
    synthetic: true,
  };
}

// Keep filename lookup identity-preserving: floor_05.png stays floor_05.png,
// while its selector/data metadata is supplied by resolveFloorRender().
export function resolveRuntimeMapFilename(filename: string): string {
  return filename;
}
