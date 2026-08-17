import type { LivingPlayer, LivingStaff } from "./types";
import { StaffFlag } from "./constants";

export function startPlanning(player: LivingPlayer, staffs: readonly LivingStaff[]): void {
  const mutablePlayer = player as { planning: boolean; completed: boolean; elapsedPlanning: number };
  mutablePlayer.planning = true;
  mutablePlayer.completed = false;
  mutablePlayer.elapsedPlanning = 0;
  for (const staff of staffs) {
    const mutableStaff = staff as { flags: number };
    mutableStaff.flags |= StaffFlag.PLANNING;
    mutableStaff.flags &= ~StaffFlag.PLANNING_COMPLETED;
  }
}

export function updatePlanning(player: LivingPlayer, staffs: readonly LivingStaff[], elapsed: number): void {
  const mutablePlayer = player as { planning: boolean; completed: boolean; elapsedPlanning: number };
  mutablePlayer.elapsedPlanning += Math.max(0, elapsed);
  for (const staff of staffs) {
    const mutableStaff = staff as { flags: number };
    if (mutablePlayer.planning) mutableStaff.flags |= StaffFlag.PLANNING;
  }
}

export function endPlanning(player: LivingPlayer, staffs: readonly LivingStaff[]): void {
  const mutablePlayer = player as { planning: boolean; completed: boolean; elapsedPlanning: number };
  mutablePlayer.planning = false;
  mutablePlayer.completed = true;
  for (const staff of staffs) {
    const mutableStaff = staff as { flags: number };
    mutableStaff.flags &= ~StaffFlag.PLANNING;
    mutableStaff.flags |= StaffFlag.PLANNING_COMPLETED;
  }
}
