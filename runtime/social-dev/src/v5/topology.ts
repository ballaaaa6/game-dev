import { nativeRoomFloorUsageJson as floorUsageJson } from "../catalog/load-original-runtime-pack";
import type { NativeRoomFloorUsageContract } from "../catalog/types";
import type { V5RoomContext, V5RoomOptions, V5RoomTopology } from "./contracts";

const floorUsage = floorUsageJson as unknown as NativeRoomFloorUsageContract;

export function resolveRoomTopologyV5(
  roomFloor: number,
  options: Pick<V5RoomOptions, "context" | "dimensions"> = {},
): V5RoomTopology {
  if (!Number.isSafeInteger(roomFloor)) {
    throw new Error(`Room.floor_ must be an integer, received ${String(roomFloor)}`);
  }
  const variantId = roomFloor === 0 ? "floor_0" : "floor_nonzero";
  const variant = floorUsage.topology_selection.variants[variantId];
  if (variant === undefined) {
    throw new Error(`Native Room floor topology ${variantId} is unavailable`);
  }
  const context = options.context ?? defaultContext(roomFloor, options.dimensions);
  const dimensions = options.dimensions ?? defaultDimensions(context, variant.width, variant.height);
  validateDimensions(roomFloor, context, dimensions.width, dimensions.height, variant.width, variant.height);
  const values = variant.rows.flat();
  const rows = Array.from({ length: dimensions.height }, (_, y) =>
    values.slice(y * dimensions.width, (y + 1) * dimensions.width));
  if (rows.some((row) => row.length !== dimensions.width)) {
    throw new Error(`Native Room topology ${variantId} cannot materialize ${dimensions.width}x${dimensions.height}`);
  }
  return {
    roomFloor,
    variantId,
    width: dimensions.width,
    height: dimensions.height,
    rows,
    context,
    environmentScope: context === "main_display"
      ? "native_main_14x14_outer_map"
      : "native_room_topology_only",
    proof: "NATIVE-CODE-PROVEN",
  };
}

export function nativeFloorTopologyContract(): NativeRoomFloorUsageContract {
  return floorUsage;
}

function defaultContext(
  roomFloor: number,
  dimensions: V5RoomOptions["dimensions"],
): V5RoomContext {
  if (roomFloor !== 0) {
    return "addition_floor_preview";
  }
  return dimensions?.width === 4 && dimensions.height === 4 ? "persistent_room" : "main_display";
}

function defaultDimensions(
  context: V5RoomContext,
  variantWidth: number,
  variantHeight: number,
): { readonly width: number; readonly height: number } {
  if (context === "main_display") {
    return { width: 14, height: 14 };
  }
  return context === "persistent_room"
    ? { width: 4, height: 4 }
    : { width: variantWidth, height: variantHeight };
}

function validateDimensions(
  roomFloor: number,
  context: V5RoomContext,
  width: number,
  height: number,
  variantWidth: number,
  variantHeight: number,
): void {
  if (!Number.isSafeInteger(width) || !Number.isSafeInteger(height) || width < 1 || height < 1) {
    throw new Error(`Room topology dimensions must be positive integers, received ${width}x${height}`);
  }
  if (roomFloor !== 0 && (width !== 4 || height !== 4)) {
    throw new Error(`Native Room rejects floor=${roomFloor} at ${width}x${height}; MAPCHIP_ARRAY[1] is 4x4 only`);
  }
  if (roomFloor === 0 && !((width === 4 && height === 4) || (width === 14 && height === 14))) {
    throw new Error(`Native Room rejects floor=0 at ${width}x${height}; approved constructor dimensions are 4x4 or 14x14`);
  }
  if (width > variantWidth || height > variantHeight) {
    throw new Error(`Native Room topology ${width}x${height} exceeds ${variantWidth}x${variantHeight}`);
  }
  if (context === "main_display" && (roomFloor !== 0 || width !== 14 || height !== 14)) {
    throw new Error("main_display requires floor=0 at 14x14");
  }
  if (context === "persistent_room" && (roomFloor !== 0 || width !== 4 || height !== 4)) {
    throw new Error("persistent_room requires floor=0 at 4x4");
  }
  if (context === "addition_floor_preview" && (roomFloor === 0 || width !== 4 || height !== 4)) {
    throw new Error("addition_floor_preview requires floor!=0 at 4x4");
  }
}
