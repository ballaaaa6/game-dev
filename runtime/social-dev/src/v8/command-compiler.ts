import type { RuntimeCatalogs } from "../catalog/load-contracts";
import type { LivingFurniture } from "../core/living/types";
import type { SceneProjection } from "../scene/projection";
import { compareNativeCells } from "../renderer/native-render-order";
import {
  V8_RENDER_PASSES,
  type V8LiveSnapshot,
  type V8RenderPass,
  type V8VisualStaff,
} from "./contracts";
import { compileWorkstationComposition, type V8WorkstationComposition } from "./workstation";

export type V8RoomCommandKind =
  | "map"
  | "extension_wall"
  | "rear_wall"
  | "door"
  | "structural_facility"
  | "furniture"
  | "workstation"
  | "staff"
  | "foreground_wall";

export interface V8RoomCommand {
  readonly pass: V8RenderPass;
  readonly kind: V8RoomCommandKind;
  readonly id: string;
  readonly cell: readonly [number, number] | null;
  readonly layer: number;
  readonly source: string;
  readonly furniture?: LivingFurniture;
  readonly staff?: V8VisualStaff;
  readonly workstation?: V8WorkstationComposition;
  readonly objectId?: string;
}

export interface V8RoomCommandPlan {
  readonly schema_version: "social-dev-v8-room0-command-plan-v1";
  readonly passes: readonly {
    readonly id: V8RenderPass;
    readonly commands: readonly V8RoomCommand[];
  }[];
  readonly nestedStaffIds: readonly number[];
  readonly underlayFirst: true;
  readonly rowOrder: "y_ascending_x_descending";
}

function cellCompare(left: V8RoomCommand, right: V8RoomCommand): number {
  if (left.cell && right.cell) {
    return compareNativeCells({ cell: left.cell }, { cell: right.cell })
      || left.layer - right.layer
      || left.id.localeCompare(right.id);
  }
  return left.layer - right.layer || left.id.localeCompare(right.id);
}

function installedStaffForDesk(
  snapshot: V8LiveSnapshot,
  desk: LivingFurniture,
): readonly V8VisualStaff[] {
  return snapshot.staffs.filter((staff) =>
    staff.deskId === desk.instanceId
    && (staff.flags & 2) !== 0
    && staff.visible,
  );
}

function workstationForStaff(
  snapshot: V8LiveSnapshot,
  staff: V8VisualStaff,
  desk: LivingFurniture,
  rawDirection: number,
): V8WorkstationComposition {
  return compileWorkstationComposition(
    desk.instanceId,
    desk.cell,
    staff.id,
    staff.cell,
    staff.selectorId,
    staff.frame,
    rawDirection,
  );
}

/**
 * Compile the native nine-slot Room0 order into deterministic commands. The
 * underlay is committed in the first slot, and rear wall/furniture/installed
 * staff are explicitly composed before the foreground wall slot.
 */
export function compileV8Room0Commands(
  catalogs: RuntimeCatalogs,
  projection: SceneProjection,
  snapshot: V8LiveSnapshot,
): V8RoomCommandPlan {
  if (projection.sceneId !== "room:0" || projection.sceneMode !== "floor00") {
    throw new Error("V8 Room0 compositor requires the floor00 room:0 projection");
  }
  const byPass = new Map<V8RenderPass, V8RoomCommand[]>();
  for (const pass of V8_RENDER_PASSES) byPass.set(pass, []);
  const push = (command: V8RoomCommand): void => { byPass.get(command.pass)!.push(command); };

  for (const cell of projection.mapCells) {
    push({
      pass: "map-extension-floor",
      kind: "map",
      id: `map:${cell.cell[0]}:${cell.cell[1]}`,
      cell: [cell.cell[0], cell.cell[1]],
      layer: cell.nativeFloorPass ? 1 : 0,
      source: "MapChip.Draw / DrawFloor underlay",
    });
  }
  for (const wall of projection.extensionWalls) {
    push({
      pass: "map-extension-floor",
      kind: "extension_wall",
      id: `extension:${wall.cell[0]}:${wall.cell[1]}:${wall.compositionGroup}:${wall.pieceIndex}`,
      cell: [wall.cell[0], wall.cell[1]],
      layer: 2 + wall.pieceIndex,
      source: "MapChip.DrawExtentionFloor",
    });
  }

  for (const facility of projection.structuralFacilities) {
    push({
      pass: "object-chip-primary",
      kind: "structural_facility",
      id: facility.id,
      cell: [facility.anchor[0], facility.anchor[1]],
      layer: 2,
      source: "ObjChip.Draw structural FurnitureData(0) composition",
      objectId: facility.objectId,
    });
  }

  const foreground = new Set((catalogs.floor00.render_composition.foreground_wall_cells ?? [[8, 7], [8, 8]])
    .map((cell) => `${cell[0]},${cell[1]}`));
  const wallAsset = projection.sceneAssets.find((asset) => asset.role === "wall");
  for (const [frameId, cells] of Object.entries(wallAsset?.cellScope?.cells ?? {})) {
    const records = wallAsset?.cellScope?.spriteLayers?.[frameId]
      ?? (wallAsset?.cellScope?.spriteRecords?.[frameId] ? [wallAsset.cellScope.spriteRecords[frameId]] : []);
    for (const cell of cells) {
      const key = `${cell[0]},${cell[1]}`;
      for (const [index, record] of records.entries()) {
        const layer = typeof record.layer === "number" ? record.layer : index;
        push({
          pass: foreground.has(key) ? "object-chip-late" : "object-chip-primary",
          kind: foreground.has(key) ? "foreground_wall" : "rear_wall",
          id: `${wallAsset?.id ?? "wall"}@${frameId}:${cell[0]}:${cell[1]}:layer:${layer}`,
          cell: [cell[0], cell[1]],
          layer: foreground.has(key) ? 8 + layer : layer,
          source: "ObjChip.DrawWall",
        });
      }
    }
  }
  const door = projection.sceneAssets.find((asset) => asset.role === "door");
  if (door?.cell) {
    push({
      pass: "object-chip-primary",
      kind: "door",
      id: door.id,
      cell: [door.cell[0], door.cell[1]],
      layer: 6,
      source: "ObjChip.DrawWall door type 5",
    });
  }

  const nestedStaffIds: number[] = [];
  let deskInstanceIndex = 0;
  const workstationStaffByDesk = new Map<number, { readonly staff: V8VisualStaff; readonly object: typeof projection.nativeInitialObjects[number] }>();
  for (const object of projection.nativeInitialObjects) {
    const isDesk = object.objectId === "furniture:3";
    const instanceId = isDesk ? deskInstanceIndex++ : -1;
    const instance = isDesk
      ? snapshot.staffs.find((staff) => staff.deskId === instanceId && (staff.flags & 2) !== 0 && staff.visible)
      : undefined;
    push({
      pass: "object-chip-primary",
      kind: "furniture",
      id: `${object.objectId}@${object.cell[0]}:${object.cell[1]}`,
      cell: [object.cell[0], object.cell[1]],
      layer: 4,
      source: "ObjChip.Draw FurnitureData native binding",
      objectId: object.objectId,
    });
    if (instance && isDesk) {
      nestedStaffIds.push(instance.id);
      workstationStaffByDesk.set(instanceId, { staff: instance, object });
    }
  }

  for (const staff of snapshot.staffs) {
    if (nestedStaffIds.includes(staff.id)) continue;
    push({
      pass: "avatar-primary",
      kind: "staff",
      id: staff.actorId,
      cell: [staff.cell[0], staff.cell[1]],
      layer: 0,
      source: "Staff.Draw",
      staff,
    });
  }

  for (const [deskId, { staff, object }] of workstationStaffByDesk) {
    const desk: LivingFurniture = {
      instanceId: deskId,
      rawIndex: -1,
      rawType: 2,
      rawDirection: 0,
      cell: [object.cell[0], object.cell[1]],
      furnitureDataId: 3,
      installed: true,
      ownerStaffId: staff.id,
      activeUserIds: [staff.id],
      reservedUserIds: [],
      useFrame: 0,
      actionStarted: false,
      actionId: -1,
      recovery: 0,
      removed: false,
    };
    const rawDirection = projection.cells.find((cell) =>
      cell.cell[0] === object.cell[0] && cell.cell[1] === object.cell[1]
    )?.rawDirection ?? 0;
    const workstation = workstationForStaff(snapshot, staff, { ...desk, rawDirection }, rawDirection);
    push({
      pass: "object-chip-primary",
      kind: "workstation",
      id: `workstation:${staff.id}:${deskId}`,
      cell: [object.cell[0], object.cell[1]],
      layer: 5,
      source: "ObjChip.Draw FurnitureData preview=false workstation interleave",
      workstation,
    });
  }

  return {
    schema_version: "social-dev-v8-room0-command-plan-v1",
    passes: V8_RENDER_PASSES.map((id) => ({
      id,
      commands: [...(byPass.get(id) ?? [])].sort(cellCompare),
    })),
    nestedStaffIds: [...new Set(nestedStaffIds)].sort((left, right) => left - right),
    underlayFirst: true,
    rowOrder: "y_ascending_x_descending",
  };
}
