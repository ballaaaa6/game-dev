import type { LivingStaff } from "./types";

/** Derived Staff helpers kept separate from the mutable runtime owner. */
export function getHpRatio(staff: LivingStaff): number {
  return Math.trunc((staff.hp * 100) / Math.max(1, staff.maxHp));
}

export function clampHp(staff: LivingStaff, value: number): number {
  return Math.max(0, Math.min(staff.maxHp, Math.trunc(value)));
}

export function isSitting(staff: LivingStaff): boolean {
  return (staff.flags & 2) !== 0;
}
