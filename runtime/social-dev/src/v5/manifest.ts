import type { V5RoomCommandManifest, V5RoomRenderResult } from "./contracts";
import type { RoomV5 } from "./room";

export function createV5CommandManifest(room: RoomV5, render: V5RoomRenderResult): V5RoomCommandManifest {
  const floorPolicy = room.roomData.runtimeRecord.selectors.floor;
  const alias = floorPolicy.runtime_alias;
  return {
    schemaVersion: 1,
    phase: "V5",
    roomKey: room.roomData.roomKey,
    dataKey: room.roomData.dataKey,
    roomFloor: room.floor,
    floorImgId: room.roomData.floorImgId,
    topology: {
      variantId: room.topology.variantId,
      width: room.topology.width,
      height: room.topology.height,
      context: room.topology.context,
    },
    cameraOffset: render.camera.offset,
    visualScope: room.visualScope,
    passes: render.passes,
    events: render.events,
    traces: render.traces,
    commands: render.commands,
    nativeBindings: room.roomData.nativeBindings,
    structuralFacilities: room.roomData.structuralFacilities,
    floorSelectorPolicy: {
      rawRoomDataSelector: room.roomData.floorImgId,
      nativeTableSelector: floorPolicy.native_selector_id ?? null,
      runtimeSelector: alias?.selector_id ?? floorPolicy.native_selector_id ?? room.roomData.floorImgId,
      renderedFilename: alias?.render_filename ?? floorPolicy.target_filename ?? `selector_${alias?.selector_id ?? floorPolicy.native_selector_id ?? room.roomData.floorImgId}`,
      status: alias === undefined ? "NATIVE-CODE-PROVEN" : "COMPATIBILITY-POLICY",
    },
  };
}

export function stableJson(value: unknown): string {
  if (value === undefined) {
    return "null";
  }
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value) ?? "null";
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableJson(item)).join(",")}]`;
  }
  const record = value as Record<string, unknown>;
  return `{${Object.keys(record)
    .filter((key) => record[key] !== undefined)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableJson(record[key])}`)
    .join(",")}}`;
}
