import {
  defaultMapChipJson as defaultMapJson,
  floor00SceneJson,
  nativeSceneAssemblyJson as nativeAssemblyJson,
  roomSceneRuntimeJson as roomRuntimeJson,
} from "../catalog/load-original-runtime-pack";
import type {
  DefaultMapChipContract,
  Floor00SceneContract,
  NativeSceneAssemblyContract,
  RoomSceneRuntimeContract,
} from "../catalog/types";
import type {
  V5RawObjChip,
  V5RoomData,
  V5StructuralFacility,
} from "./contracts";
import type { V4Cell } from "../v4";

const defaultMap = defaultMapJson as unknown as DefaultMapChipContract;
const floor00Scene = floor00SceneJson as unknown as Floor00SceneContract;
const nativeAssembly = nativeAssemblyJson as unknown as NativeSceneAssemblyContract;
const roomRuntime = roomRuntimeJson as unknown as RoomSceneRuntimeContract;

const RUNTIME_CONTRACT_REF = "knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json";
const NATIVE_ASSEMBLY_REF = "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json";

export function roomDataV5Keys(): readonly string[] {
  return roomRuntime.rooms.map((room) => room.room_key);
}

export function loadRoomDataV5(roomKey = "room:0"): V5RoomData {
  const runtimeRecord = roomRuntime.rooms.find((room) => room.room_key === roomKey);
  const assembly = nativeAssembly.rooms.find((room) => room.room_key === roomKey);
  if (runtimeRecord === undefined || assembly === undefined) {
    throw new Error(`V5 RoomData is missing ${roomKey}`);
  }
  const objMap = runtimeRecord.grid.obj_map;
  const objDir = runtimeRecord.grid.obj_dir;
  validateGrid(objMap, objDir, runtimeRecord.grid.width, runtimeRecord.grid.height, roomKey);
  const rawObjChips: V5RawObjChip[] = [];
  for (let y = 0; y < objMap.length; y += 1) {
    const mapRow = objMap[y];
    const dirRow = objDir[y];
    if (mapRow === undefined || dirRow === undefined) {
      throw new Error(`V5 RoomData ${roomKey} has a missing row at ${y}`);
    }
    for (let x = 0; x < mapRow.length; x += 1) {
      const rawType = mapRow[x];
      const rawDirection = dirRow[x];
      if (rawType === undefined || rawDirection === undefined) {
        throw new Error(`V5 RoomData ${roomKey} has a missing cell at ${x},${y}`);
      }
      rawObjChips.push({
        instanceId: `objchip:${roomKey}:${x}:${y}`,
        cell: [x, y],
        rawType,
        rawDirection,
      });
    }
  }
  return {
    roomKey,
    dataKey: runtimeRecord.data_key,
    roomId: runtimeRecord.native.id,
    name: runtimeRecord.native.name,
    floorImgId: runtimeRecord.native.floor_img_id,
    wallImgId: runtimeRecord.native.wall_img_id,
    doorImgId: runtimeRecord.native.door_img_id,
    objMap,
    objDir,
    objMapWidth: runtimeRecord.grid.width,
    objMapHeight: runtimeRecord.grid.height,
    rawObjChips,
    nativeBindings: assembly.native_furniture_bindings,
    structuralFacilities: structuralFacilitiesFor(roomKey),
    assembly,
    runtimeRecord,
    source: {
      englishRawRowSha256: String(runtimeRecord.source.english_raw_row_sha256),
      runtimeContract: RUNTIME_CONTRACT_REF,
      nativeAssemblyContract: NATIVE_ASSEMBLY_REF,
    },
  };
}

export function loadAllRoomDataV5(): readonly V5RoomData[] {
  return roomDataV5Keys().map((roomKey) => loadRoomDataV5(roomKey));
}

export function mapImageSelectorForRawIndex(rawIndex: number): number {
  const record = defaultMap.raw_index_to_selector[String(rawIndex)];
  if (record === undefined) {
    throw new Error(`V5 MapChip has no selector mapping for raw index ${rawIndex}`);
  }
  return record.selector_id;
}

export function mapMeaningForRawIndex(rawIndex: number): string {
  const record = defaultMap.raw_index_to_selector[String(rawIndex)];
  if (record === undefined) {
    throw new Error(`V5 MapChip has no meaning mapping for raw index ${rawIndex}`);
  }
  return record.meaning;
}

export function nativeWallCells(roomData: V5RoomData): Readonly<Record<string, readonly V4Cell[]>> {
  return roomData.assembly.wall.cells_by_frame;
}

export function nativeDoorCells(roomData: V5RoomData): readonly V4Cell[] {
  return roomData.assembly.door.cells;
}

export function explicitBindingAt(
  roomData: V5RoomData,
  cell: V4Cell,
): (typeof roomData.nativeBindings)[number] | undefined {
  return roomData.nativeBindings.find((binding) => binding.cell[0] === cell[0] && binding.cell[1] === cell[1]);
}

function structuralFacilitiesFor(roomKey: string): readonly V5StructuralFacility[] {
  if (roomKey !== "room:0") {
    return [];
  }
  return floor00Scene.structural_facilities.map((facility) => ({
    objectId: facility.object_id,
    furnitureDataId: 0,
    anchor: facility.anchor,
    mapAnchor: facility.map_anchor,
    rawType: 4,
    footprintCells: facility.footprint_cells,
    primarySeb: facility.seb_selector_id,
    secondarySeb: -1,
    imageSelector: facility.sprite_record.image_id as number,
    spriteRecord: facility.sprite_record,
    sourceStatus: "verified_native_fixture",
  }));
}

function validateGrid(
  objMap: readonly (readonly number[])[],
  objDir: readonly (readonly number[])[],
  width: number,
  height: number,
  roomKey: string,
): void {
  if (objMap.length !== height || objDir.length !== height || width !== 10 || height !== 10) {
    throw new Error(`V5 RoomData ${roomKey} requires the native 10x10 ObjChip grids`);
  }
  for (let y = 0; y < height; y += 1) {
    if (objMap[y]?.length !== width || objDir[y]?.length !== width) {
      throw new Error(`V5 RoomData ${roomKey} has a non-rectangular ObjChip row ${y}`);
    }
  }
}
