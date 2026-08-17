import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { furnitureRecovery, furnitureType, i0Catalog, roomRecord } from "./catalog";
import { ObjChipType } from "./constants";
import { cloneFurniture, type MutableFurniture } from "./furniture";
import type { LivingFurniture, LivingRoom, LivingCell } from "./types";

export interface RoomBuildOptions {
  readonly scenarioEquipment?: boolean;
}

function toCell(cell: readonly number[]): LivingCell {
  return [cell[0] ?? 0, cell[1] ?? 0];
}

function explicitFurniture(
  catalogs: RuntimeCatalogs,
  item: {
    readonly instance_id: number;
    readonly furniture_data_id: number;
    readonly cell: readonly number[];
    readonly raw_type?: number;
    readonly direction: number;
    readonly raw_order: number;
  },
): LivingFurniture {
  const rawType = item.raw_type ?? furnitureType(catalogs, item.furniture_data_id);
  return {
    instanceId: item.instance_id,
    rawIndex: item.raw_order,
    rawType,
    rawDirection: item.direction,
    cell: toCell(item.cell),
    furnitureDataId: item.furniture_data_id,
    installed: true,
    ownerStaffId: -1,
    activeUserIds: [],
    reservedUserIds: [],
    useFrame: 0,
    actionStarted: false,
    actionId: -1,
    recovery: furnitureRecovery(catalogs, item.furniture_data_id),
    removed: false,
  };
}

export function buildRoom(catalogs: RuntimeCatalogs, options: RoomBuildOptions = {}): LivingRoom {
  const source = roomRecord(catalogs, "room:0");
  const bootstrap = i0Catalog(catalogs).bootstrap;
  const equipment = options.scenarioEquipment ? bootstrap.scenario_equipment : bootstrap.equipment;
  const door: LivingFurniture = {
    instanceId: -1,
    rawIndex: -1,
    rawType: ObjChipType.DOOR,
    rawDirection: bootstrap.door.raw_direction,
    cell: toCell(bootstrap.door.cell),
    furnitureDataId: null,
    installed: true,
    ownerStaffId: -1,
    activeUserIds: [],
    reservedUserIds: [],
    useFrame: 0,
    actionStarted: false,
    actionId: -1,
    recovery: 0,
    removed: false,
  };
  const furniture = [
    door,
    ...bootstrap.desks.map((item) => explicitFurniture(catalogs, item)),
    ...equipment.map((item) => explicitFurniture(catalogs, item)),
  ];
  return {
    roomDataId: source.native.id,
    roomKey: source.room_key,
    width: source.width,
    height: source.height,
    objMap: source.obj_map.map((row) => [...row]),
    objDir: source.obj_dir.map((row) => [...row]),
    furniture,
    staffIds: [],
  };
}

export function cloneRoom(room: LivingRoom): LivingRoom {
  return {
    ...room,
    objMap: room.objMap.map((row) => [...row]),
    objDir: room.objDir.map((row) => [...row]),
    furniture: room.furniture.map(cloneFurniture),
    staffIds: [...room.staffIds],
  };
}

export function mutableRoom(room: LivingRoom): {
  roomDataId: number;
  roomKey: string;
  width: number;
  height: number;
  objMap: number[][];
  objDir: number[][];
  furniture: MutableFurniture[];
  staffIds: number[];
} {
  return room as unknown as {
    roomDataId: number;
    roomKey: string;
    width: number;
    height: number;
    objMap: number[][];
    objDir: number[][];
    furniture: MutableFurniture[];
    staffIds: number[];
  };
}

export function findFurniture(room: LivingRoom, instanceId: number): LivingFurniture | null {
  return room.furniture.find((item) => item.instanceId === instanceId && !item.removed) ?? null;
}

export function findDesk(room: LivingRoom, preferredId = -1): LivingFurniture | null {
  if (preferredId >= 0) {
    const preferred = findFurniture(room, preferredId);
    if (preferred && preferred.rawType === ObjChipType.DESK && preferred.installed) return preferred;
  }
  return [...room.furniture]
    .filter((item) => item.rawType === ObjChipType.DESK && item.installed && item.furnitureDataId !== null && item.ownerStaffId < 0)
    .sort((left, right) => left.rawIndex - right.rawIndex)[0] ?? null;
}

export function findEquipment(room: LivingRoom, rawType: number): LivingFurniture[] {
  return room.furniture
    .filter((item) => item.installed && !item.removed && (item.rawType === rawType || (rawType === ObjChipType.EQUIPMENT && item.rawType === ObjChipType.BIG_CENTER)))
    .sort((left, right) => left.rawIndex - right.rawIndex);
}

export function setCellRawType(room: LivingRoom, cell: LivingCell, rawType: number): void {
  const mutable = mutableRoom(room);
  if (mutable.objMap[cell[1]]) mutable.objMap[cell[1]][cell[0]] = rawType;
}

export function removeRoomFurniture(room: LivingRoom, instanceId: number): LivingFurniture | null {
  const furniture = findFurniture(room, instanceId);
  if (!furniture) return null;
  const mutable = furniture as unknown as MutableFurniture;
  mutable.removed = true;
  mutable.installed = false;
  mutable.ownerStaffId = -1;
  mutable.activeUserIds = [];
  mutable.reservedUserIds = [];
  mutable.actionStarted = false;
  mutable.useFrame = 0;
  setCellRawType(room, furniture.cell, ObjChipType.PASS);
  return furniture;
}
