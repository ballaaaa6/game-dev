import { describe, expect, it } from "vitest";

import imageOptEvidenceJson from "../../../knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json";

import type { ImageContract, ImageOptEvidenceContract } from "../src/v1/contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "../src/v1/errors";
import { loadImageFixture } from "../src/v1/fixture-loader";
import { Image, ImageResult } from "../src/v1/image";

const evidence = imageOptEvidenceJson as unknown as ImageOptEvidenceContract;

describe("Image and OPT", () => {
  it.each(["chair_00", "chair_02", "desk_00", "door_02"])(
    "projects the validated %s logical image and OPT access contract",
    (stem) => {
      const { image, contract } = loadImageFixture(stem);

      expect(image.width).toBe(contract.logical_size.width);
      expect(image.height).toBe(contract.logical_size.height);
      expect(image.sourcePixelSha256).toBe(contract.pixel_sha256);
      expect(image.getOptimize(0, 0, 0)).toEqual(contract.optimize_access["0,0,0"]);
      expect(image.getOptimizeSeb(0)).toEqual(contract.seb_associations[0]);
      expect(image.sourcePngRawSha256).toBe(contract.source_png.raw_sha256);
      expect(image.sourceOptRawSha256).toBe(contract.source_opt.raw_sha256);
    },
  );

  it("preserves chair_00 variable-piece cells and source-region boundaries", () => {
    const { image, contract } = loadImageFixture("chair_00");
    const cell = contract.opt.cells.find((candidate) => candidate.index === 1);

    expect(cell?.piece_count).toBe(2);
    expect(image.getOptimize(1, 0, 0)).toEqual(contract.optimize_access["1,0,0"]);
    expect(image.getOptimize(1, 0, 1)).toEqual(contract.optimize_access["1,0,1"]);
    expect(image.getOptimize(1, 0, 2)).toBeNull();

    for (const record of contract.opt.records) {
      const region = image.getSourceRegion(record.index, record.part_index);
      expect([region.x, region.y, region.width, region.height]).toEqual([
        record.source_x,
        record.source_y,
        record.width,
        record.height,
      ]);
      expect(region.x + region.width).toBeLessThanOrEqual(contract.source_size.width);
      expect(region.y + region.height).toBeLessThanOrEqual(contract.source_size.height);
    }
  });

  it("keeps source and promoted runtime hashes identical", () => {
    for (const contract of evidence.records) {
      expect(contract.source_png.raw_sha256).toBe(
        contract.source_png.runtime_promotion.runtime_sha256,
      );
      expect(contract.source_opt.raw_sha256).toBe(
        contract.source_opt.runtime_promotion.runtime_sha256,
      );
      expect(contract.pixel_sha256).toBe(contract.logical_runtime_promotion.pixel_sha256);

      const { image } = loadImageFixture(contract.fixture_stem.split("/").pop() ?? contract.fixture_stem);
      expect(image.sourcePngRawSha256).toBe(contract.source_png.raw_sha256);
      expect(image.sourceOptRawSha256).toBe(contract.source_opt.raw_sha256);
      expect(image.pixelSha256).toBe(contract.pixel_sha256);
    }
  });

  it("tracks contract-only lifetime, resize metadata, and atlas identity", () => {
    const { image } = loadImageFixture("desk_00");

    expect(image.useCount).toBe(0);
    image.use();
    image.use();
    expect(image.useCount).toBe(2);
    expect(image.isUsed).toBe(true);
    image.unuse();
    image.unuse();
    image.unuse();
    expect(image.useCount).toBe(0);
    expect(image.isUsed).toBe(false);

    image.resize(240, 64);
    expect([image.width, image.height]).toEqual([240, 64]);
    expect([image.sourceWidth, image.sourceHeight]).toEqual([24, 51]);
    expect(image.resizeMetadata).toEqual({
      width: 240,
      height: 64,
      srcX: 0,
      srcY: 0,
      srcWidth: 120,
      srcHeight: 32,
      rasterParity: "deferred",
    });

    expect(image.imageAtlasId).toBe(-1);
    expect(image.setImageAtlasId(7)).toBe(ImageResult.Success);
    expect(image.imageAtlasId).toBe(7);
  });

  it("rejects raw OPT bytes instead of decoding a second runtime format", () => {
    expect(() => Image.fromContract(new Uint8Array([0x3c, 0x20, 0x03, 0x01]) as never)).toThrowError(
      V1DeferredError,
    );
    try {
      Image.fromContract(new Uint8Array([0x3c, 0x20, 0x03, 0x01]) as never);
    } catch (error) {
      expect((error as V1DeferredError).code).toBe("IMAGE_RAW_OPT_DEFERRED");
    }
  });

  it("rejects malformed image contracts and invalid access keys", () => {
    const { contract } = loadImageFixture("door_02");
    const malformed = JSON.parse(JSON.stringify(contract)) as ImageContract;
    (malformed as unknown as { logical_reconstruction: { opt: { status: string } } }).logical_reconstruction.opt.status = "candidate";
    expect(() => Image.fromContract(malformed)).toThrowError(V1ContractError);

    const { image } = loadImageFixture("door_02");
    expect(() => image.getOptimize(-1, 0, 0)).toThrowError(V1LookupError);
    expect(() => image.getOptimize(0, 1, 0)).toThrowError(V1LookupError);
    expect(() => image.getSourceRegion(9, 0)).toThrowError(V1LookupError);
  });
});
