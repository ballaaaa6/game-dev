import { describe, expect, it } from "vitest";
import defaultMapChipJson from "../../../knowledge/fixtures/accepted/runtime/default_map_chip_contract.json";
import { resolveExtensionWallPieces, resolveExtensionWallPiecesForTriggerCells } from "../src/scene/extension-wall";
import type { DefaultMapChipContract } from "../src/catalog/types";

const contract = defaultMapChipJson as unknown as DefaultMapChipContract;

describe("native wall extension composition", () => {
  it("expands each verified MapChip trigger into the two native DrawSeb pieces", () => {
    const pieces = resolveExtensionWallPieces(contract.extension_wall, "map:chip/wall_01.png");

    expect(pieces).toHaveLength(20);
    expect(pieces.filter((piece) => piece.compositionGroup === "horizontal_frame_0")).toHaveLength(10);
    expect(pieces.filter((piece) => piece.compositionGroup === "vertical_frame_1")).toHaveLength(10);
    expect(pieces.every((piece) => piece.pieceIndex === 0 || piece.pieceIndex === 1)).toBe(true);
    expect(pieces.every((piece) => piece.spriteRecord.width <= 24 && piece.spriteRecord.source_x + piece.spriteRecord.width <= 96)).toBe(true);
  });

  it("keeps pair spans continuous and preserves the unused alternate SEB frames", () => {
    const pieces = resolveExtensionWallPieces(contract.extension_wall, "map:chip/wall_01.png");
    const firstHorizontal = pieces.filter((piece) => piece.triggerCell.join(",") === "2,5");
    const firstVertical = pieces.filter((piece) => piece.triggerCell.join(",") === "4,5");

    const intervals = (group: typeof firstHorizontal) => group
      .map((piece) => ({
        start: piece.pieceOffset.x + piece.spriteRecord.destination_x,
        end: piece.pieceOffset.x + piece.spriteRecord.destination_x + piece.spriteRecord.width,
      }))
      .sort((left, right) => left.start - right.start);

    const horizontal = intervals(firstHorizontal);
    const vertical = intervals(firstVertical);
    expect(horizontal[1].start).toBeLessThanOrEqual(horizontal[0].end);
    expect(vertical[1].start).toBeLessThanOrEqual(vertical[0].end);
    expect(Object.keys(contract.extension_wall.frame_records).sort()).toEqual(["0", "1", "2", "3"]);
    expect(contract.extension_wall.frame_usage["2"].floor00_status).toBe("retained_not_selected_by_floor00_extension_path");
    expect(contract.extension_wall.frame_usage["3"].floor00_status).toBe("retained_not_selected_by_floor00_extension_path");
  });

  it("resolves a concrete trigger-cell override with the same native two-piece records", () => {
    const pieces = resolveExtensionWallPiecesForTriggerCells(
      contract.extension_wall,
      "map:chip/wall_01.png",
      {
        horizontal_frame_0: [[5, 5], [6, 5], [7, 5], [8, 5]],
        vertical_frame_1: [[4, 7], [4, 8], [4, 9], [4, 10], [4, 11]],
      },
    );

    expect(pieces).toHaveLength(18);
    expect(pieces.filter((piece) => piece.compositionGroup === "horizontal_frame_0")).toHaveLength(8);
    expect(pieces.filter((piece) => piece.compositionGroup === "vertical_frame_1")).toHaveLength(10);
    expect(pieces.some((piece) => piece.triggerCell.join(",") === "2,5")).toBe(false);
    expect(pieces.some((piece) => piece.triggerCell.join(",") === "4,11")).toBe(true);
  });
});
