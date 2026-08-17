import type { LivingFurniture } from "./types";

export type MutableFurniture = {
  -readonly [Key in keyof LivingFurniture]: LivingFurniture[Key] extends readonly (infer Item)[] ? Item[] : LivingFurniture[Key];
};

export function asMutableFurniture(furniture: LivingFurniture): MutableFurniture {
  return furniture as unknown as MutableFurniture;
}

export function getUsersNum(furniture: LivingFurniture): number {
  return furniture.reservedUserIds.length;
}

export function reserveUse(furniture: LivingFurniture, staffId: number): boolean {
  const mutable = asMutableFurniture(furniture);
  if (mutable.removed || !mutable.installed || mutable.reservedUserIds.includes(staffId) || getUsersNum(furniture) > 0) return false;
  mutable.reservedUserIds.push(staffId);
  return true;
}

export function releaseReservation(furniture: LivingFurniture, staffId: number): void {
  const mutable = asMutableFurniture(furniture);
  mutable.reservedUserIds = mutable.reservedUserIds.filter((id) => id !== staffId);
}

export function startAction(furniture: LivingFurniture, actionId: number): void {
  const mutable = asMutableFurniture(furniture);
  mutable.actionStarted = true;
  mutable.actionId = actionId;
  mutable.useFrame = 0;
  if (!mutable.activeUserIds.includes(actionId)) mutable.activeUserIds.push(actionId);
}

export function completeAction(furniture: LivingFurniture, staffId: number): void {
  const mutable = asMutableFurniture(furniture);
  mutable.useFrame = 0;
  mutable.actionStarted = false;
  mutable.activeUserIds = mutable.activeUserIds.filter((id) => id !== staffId);
  mutable.reservedUserIds = mutable.reservedUserIds.filter((id) => id !== staffId);
}

export function removeFurniture(furniture: LivingFurniture): void {
  const mutable = asMutableFurniture(furniture);
  mutable.removed = true;
  mutable.installed = false;
  mutable.ownerStaffId = -1;
  mutable.activeUserIds = [];
  mutable.reservedUserIds = [];
  mutable.actionStarted = false;
  mutable.useFrame = 0;
}

export function cloneFurniture(furniture: LivingFurniture): LivingFurniture {
  return {
    ...furniture,
    cell: [furniture.cell[0], furniture.cell[1]],
    activeUserIds: [...furniture.activeUserIds],
    reservedUserIds: [...furniture.reservedUserIds],
  };
}
