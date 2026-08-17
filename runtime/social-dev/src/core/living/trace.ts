import type { LivingStaff, LivingTrace, LivingCell } from "./types";

export class TraceRecorder {
  private readonly entries: LivingTrace[] = [];
  private sequence = 0;

  public constructor(existing: readonly LivingTrace[] = []) {
    this.entries.push(...existing.map((entry) => ({ ...entry, route: entry.route.map((cell) => [cell[0], cell[1]] as const) })));
    this.sequence = this.entries.length;
  }

  public record(
    tick: number,
    event: string,
    staff: LivingStaff | null,
    before: Partial<Pick<LivingStaff, "state" | "moveMode" | "flags" | "cell" | "route" | "deskId" | "equipmentId" | "colleagueId" | "hp" | "recoveryStock">> = {},
    rngSequence: number | null = null,
    evidenceContractId = "LC-6",
  ): void {
    const current = staff;
    const cell = current?.cell ?? (before.cell as LivingCell | undefined) ?? null;
    this.entries.push({
      sequence: this.sequence++,
      tick,
      staffId: current?.id ?? null,
      event,
      beforeState: before.state ?? current?.state ?? null,
      afterState: current?.state ?? null,
      beforeMoveMode: before.moveMode ?? current?.moveMode ?? null,
      afterMoveMode: current?.moveMode ?? null,
      flags: current?.flags ?? before.flags ?? null,
      cell: cell ? [cell[0], cell[1]] as const : null,
      route: (current?.route ?? before.route ?? []).map((routeCell) => [routeCell[0], routeCell[1]] as const),
      deskId: current?.deskId ?? before.deskId ?? null,
      equipmentId: current?.equipmentId ?? before.equipmentId ?? null,
      colleagueId: current?.colleagueId ?? before.colleagueId ?? null,
      hp: current?.hp ?? before.hp ?? null,
      recoveryStock: current?.recoveryStock ?? before.recoveryStock ?? null,
      rngSequence,
      evidenceContractId,
    });
  }

  public all(): readonly LivingTrace[] {
    return this.entries.map((entry) => ({ ...entry, route: entry.route.map((cell) => [cell[0], cell[1]] as const) }));
  }
}
