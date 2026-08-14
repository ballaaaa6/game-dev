import type { DefaultMapChipContract } from "../catalog/types";
import type { Cell } from "../core/types";

export interface ExtensionWallPiece {
  readonly triggerCell: Cell;
  /** Alias retained for render-order and visibility consumers. */
  readonly cell: Cell;
  readonly compositionGroup: string;
  readonly frameId: string;
  readonly pieceIndex: number;
  /** Native DrawSeb call offset before the SEB destination offset is applied. */
  readonly pieceOffset: { readonly x: number; readonly y: number };
  readonly sourceAssetId: string;
  readonly spriteRecord: DefaultMapChipContract["extension_wall"]["frame_records"][string];
}

type ExtensionWallContract = DefaultMapChipContract["extension_wall"];

function sameCells(
  left: readonly (readonly [number, number])[],
  right: readonly (readonly [number, number])[],
): boolean {
  return left.length === right.length && left.every((cell, index) => cell[0] === right[index]?.[0] && cell[1] === right[index]?.[1]);
}

function nativeCellOrder(left: readonly [number, number], right: readonly [number, number]): number {
  return left[1] - right[1] || right[0] - left[0];
}

function assertContinuousPair(
  groupId: string,
  record: ExtensionWallContract["frame_records"][string],
  offsets: readonly { readonly x: number; readonly y: number }[],
): void {
  const intervals = offsets
    .map((offset) => ({
      start: offset.x + record.destination_x,
      end: offset.x + record.destination_x + record.width,
    }))
    .sort((left, right) => left.start - right.start);
  for (let index = 1; index < intervals.length; index += 1) {
    if (intervals[index].start > intervals[index - 1].end) {
      throw new Error(`Extension wall group ${groupId} has a gap between paired crops`);
    }
  }
}

function resolveExtensionWallPiecesInternal(
  contract: ExtensionWallContract,
  sourceAssetId: string,
  triggerCellsByGroup: Readonly<Record<string, readonly (readonly [number, number])[]>>,
  requireNativePredicates: boolean,
): readonly ExtensionWallPiece[] {
  const pieces: ExtensionWallPiece[] = [];
  for (const [groupId, group] of Object.entries(contract.composition_groups)) {
    const record = contract.frame_records[group.frame_id];
    if (!record) {
      throw new Error(`Extension wall group ${groupId} references missing frame ${group.frame_id}`);
    }
    const predicateCells = contract.native_predicates[groupId];
    const triggerCells = triggerCellsByGroup[groupId];
    if (!predicateCells || !triggerCells) {
      throw new Error(`Extension wall group ${groupId} has no trigger cells`);
    }
    if (requireNativePredicates && !sameCells(predicateCells, triggerCells)) {
      throw new Error(`Extension wall group ${groupId} does not match its native predicate cells`);
    }
    if (group.draw_call_count !== group.piece_offsets.length || group.draw_call_count !== 2) {
      throw new Error(`Extension wall group ${groupId} does not contain the native two-piece draw count`);
    }
    if (record.source_x < 0 || record.source_y < 0 || record.width <= 0 || record.height <= 0 || record.source_x + record.width > 96) {
      throw new Error(`Extension wall group ${groupId} contains an invalid wall_01 crop`);
    }
    assertContinuousPair(groupId, record, group.piece_offsets);
    const sortedCells = [...triggerCells].sort(nativeCellOrder);
    for (const triggerCell of sortedCells) {
      for (const [pieceIndex, pieceOffset] of group.piece_offsets.entries()) {
        const cell: Cell = [triggerCell[0], triggerCell[1]];
        pieces.push({
          triggerCell: cell,
          cell,
          compositionGroup: groupId,
          frameId: group.frame_id,
          pieceIndex,
          pieceOffset,
          sourceAssetId,
          spriteRecord: record,
        });
      }
    }
  }
  return pieces;
}

export function resolveExtensionWallPieces(
  contract: ExtensionWallContract,
  sourceAssetId: string,
): readonly ExtensionWallPiece[] {
  return resolveExtensionWallPiecesInternal(contract, sourceAssetId, contract.native_predicates, true);
}

export function resolveExtensionWallPiecesForTriggerCells(
  contract: ExtensionWallContract,
  sourceAssetId: string,
  triggerCellsByGroup: Readonly<Record<string, readonly (readonly [number, number])[]>>,
): readonly ExtensionWallPiece[] {
  return resolveExtensionWallPiecesInternal(contract, sourceAssetId, triggerCellsByGroup, false);
}
