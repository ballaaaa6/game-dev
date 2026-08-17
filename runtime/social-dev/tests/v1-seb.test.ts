import { describe, expect, it } from "vitest";

import sebEvidenceJson from "../../../knowledge/fixtures/accepted/visual-port/v1/seb-contract.json";

import type { SebContract, SebEvidenceContract } from "../src/v1/contracts";
import { V1ContractError } from "../src/v1/errors";
import { loadSebFixture } from "../src/v1/fixture-loader";
import { Seb } from "../src/v1/seb";

describe("Seb", () => {
  it("projects the one-frame door_02 fixture without changing its source record", () => {
    const { seb, fixture } = loadSebFixture("simple_one_layer");

    expect(seb.getMaxFrame()).toBe(1);
    expect(seb.getSprites(0)).toHaveLength(1);
    expect(seb.getSprites(0)[0]?.TexId).toBe(fixture.frames["0"].sprites[0]?.TexId);
    expect(seb.getSprites(0)[0]?.FrameNo).toBe(fixture.frames["0"].sprites[0]?.FrameNo);
    expect(fixture.frames["0"].sourceLayerOrder).toEqual([0]);
    expect(fixture.frames["0"].sourceRecordIndices).toEqual([0]);
  });

  it("preserves wall_00 layer order, source indices, signed texture ids, and marker values", () => {
    const { seb, fixture } = loadSebFixture("multi_layer");

    expect(seb.getMaxFrame()).toBe(4);
    expect(seb.getSprites(0)).toHaveLength(2);
    expect(seb.getSprites(0).map((sprite) => sprite.TexId)).toEqual(
      fixture.frames["0"].sprites.map((sprite) => sprite.TexId),
    );
    expect(seb.getSprite(0, 0)?.W).toBe(fixture.frames["0"].sprites[0]?.W);
    expect(seb.getSprite(0, 1)?.TransX).toBe(fixture.frames["0"].sprites[1]?.TransX);
    expect(fixture.frames["2"].sourceLayerOrder).toEqual([0, 1]);
    expect(fixture.frames["2"].sourceRecordIndices).toEqual([2, 2]);
    expect(fixture.frames["2"].sprites.map((sprite) => [sprite.TexId, sprite.TexIdRaw])).toEqual([
      [6, 6],
      [-1, 65535],
    ]);
    expect(fixture.markerRawValues).toEqual([null, 3]);
  });

  it("selects chair_00 records by the last source start frame at or before the explicit frame", () => {
    const { seb, fixture } = loadSebFixture("multi_frame");

    for (const frame of [0, 1, 2]) {
      expect(seb.getSprite(frame, 0)?.U).toBe(fixture.frames[String(frame)].sprites[0]?.U);
      expect(seb.getSprite(frame, 0)?.TransX).toBe(fixture.frames[String(frame)].sprites[0]?.TransX);
      expect(fixture.frames[String(frame)].sourceRecordIndices).toEqual([frame]);
    }
  });

  it("retains the wait_left flip flags through the selected source records", () => {
    const { seb, fixture } = loadSebFixture("flip");

    for (const frame of [0, 10, 19]) {
      const sprite = seb.getSprite(frame, 0);
      const expected = fixture.frames[String(frame)].sprites[0];

      expect([sprite?.FrameNo, sprite?.ReverseU, sprite?.ReverseV, sprite?.Blend]).toEqual([
        expected?.FrameNo,
        expected?.ReverseU,
        expected?.ReverseV,
        expected?.Blend,
      ]);
      expect(fixture.frames[String(frame)].sourceRecordIndices).toEqual([
        expected?.layerRecordIndex,
      ]);
    }
  });

  it("projects avatar-body wait_right as ordered multi-layer source records", () => {
    const { seb, fixture } = loadSebFixture("character");

    for (const frame of [0, 9, 10, 19]) {
      const expected = fixture.frames[String(frame)];

      expect(seb.getSprites(frame).map((sprite) => [sprite.TexId, sprite.TransY])).toEqual(
        expected.sprites.map((sprite) => [sprite.TexId, sprite.TransY]),
      );
      expect(expected.sourceLayerOrder).toEqual([0, 1]);
      expect(expected.sourceRecordIndices).toEqual([expected.sprites[0]?.layerRecordIndex, expected.sprites[1]?.layerRecordIndex]);
    }
  });

  it("keeps explicit GetSprite frame selection separate from Frame state wrapping", () => {
    const { seb, fixture } = loadSebFixture("multi_layer");

    expect(seb.getSprite(4, 0)?.U).toBe(fixture.frames["3"].sprites[0]?.U);
    expect(seb.getSprite(4, 0)?.U).not.toBe(fixture.frames["0"].sprites[0]?.U);

    expect(seb.getCurFrame()).toBe(0);
    seb.setCurFrame(3);
    seb.Frame();
    expect(seb.getCurFrame()).toBe(0);
    seb.setCurFrame(4);
    seb.Frame();
    expect(seb.getCurFrame()).toBe(1);
  });

  it("rejects a top-level record list that no longer preserves decoded source order", () => {
    const contract = cloneFixtureContract("01_GAME_PACKS/chip/wall_00.seb");
    (contract.records as unknown as { reverse(): void }).reverse();

    expect(() => Seb.fromContract(contract)).toThrowError(V1ContractError);
    try {
      Seb.fromContract(contract);
    } catch (error) {
      expect((error as V1ContractError).code).toBe("SEB_TOP_LEVEL_RECORD_ORDER_MISMATCH");
    }
  });

  it("copies decoded source records and rejects unsupported decoder output", () => {
    const copiedContract = cloneFixtureContract("01_GAME_PACKS/chip/chair_00.seb");
    const seb = Seb.fromContract(copiedContract);
    (copiedContract.layers[0].records[0] as unknown as { source_x: number }).source_x = 999;
    expect(seb.getSprite(0, 0)?.U).toBe(60);

    const trailingContract = cloneFixtureContract("01_GAME_PACKS/chip/door_02.seb");
    (trailingContract as unknown as { trailing_bytes: number }).trailing_bytes = 1;
    expect(() => Seb.fromContract(trailingContract)).toThrowError(V1ContractError);
    try {
      Seb.fromContract(trailingContract);
    } catch (error) {
      expect((error as V1ContractError).code).toBe("SEB_DECODER_OUTPUT_UNSUPPORTED");
    }
  });
});

function cloneFixtureContract(member: string): SebContract {
  const evidence = sebEvidenceJson as SebEvidenceContract;
  const record = evidence.records.find((candidate) => candidate.source_member === member);
  if (!record) {
    throw new Error(`missing fixture contract ${member}`);
  }
  return JSON.parse(JSON.stringify(record.decoded)) as SebContract;
}
