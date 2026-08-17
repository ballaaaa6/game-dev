import { describe, expect, it } from "vitest";

import sebEvidenceJson from "../../../knowledge/fixtures/accepted/visual-port/v1/seb-contract.json";

import type { SebEvidenceContract } from "../src/v1/contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "../src/v1/errors";
import { loadSebFixture } from "../src/v1/fixture-loader";
import { Seb } from "../src/v1/seb";

interface GeometryFrameContract {
  readonly layer_rects: readonly (readonly number[])[];
  readonly bounding_rect: readonly number[];
  readonly pixel_rect: readonly number[];
  readonly proof_class: string;
}

interface GeometryContract {
  readonly status: string;
  readonly fixture_results: Readonly<Record<string, {
    readonly category_refs: readonly string[];
    readonly frames: Readonly<Record<string, GeometryFrameContract>>;
  }>>;
  readonly depth_contract: {
    readonly status: string;
    readonly native_rvas: readonly string[];
  };
}

const evidence = sebEvidenceJson as SebEvidenceContract & { readonly geometry_contract: GeometryContract };

describe("Seb geometry and depth boundary", () => {
  it("matches format-proven layer and union rectangles for every selected frame", () => {
    for (const result of Object.entries(evidence.geometry_contract.fixture_results)) {
      const [member, expected] = result;
      const category = expected.category_refs[0];
      const { seb } = loadSebFixture(category);

      for (const [frame, frameExpected] of Object.entries(expected.frames)) {
        const frameNumber = Number(frame);
        expect(expected.category_refs.length).toBeGreaterThan(0);
        expect(frameExpected.proof_class).toBe("FORMAT-PROVEN_FALLBACK_NO_PIXEL_BOUNDING_METADATA");
        expect(rectTuple(seb.getBRect(frameNumber, 0))).toEqual(frameExpected.layer_rects[0]);
        expect(rectTuple(seb.getBoundingRect(frameNumber))).toEqual(frameExpected.bounding_rect);
        expect(rectTuple(seb.getPixelRect(frameNumber))).toEqual(frameExpected.pixel_rect);
      }

      expect(member).toMatch(/^01_GAME_PACKS\//);
    }
  });

  it("retains negative translations and multi-layer unions", () => {
    const { seb: wall } = loadSebFixture("multi_layer");
    expect(rectTuple(wall.getBRect(0, 1))).toEqual([20, -34, 2, 43]);
    expect(rectTuple(wall.getBoundingRect(0))).toEqual([-4, -34, 26, 53]);

    const { seb: desk } = loadSebFixture("translation");
    expect(rectTuple(desk.getBRect(2))).toEqual([-26, -6, 60, 32]);
  });

  it("makes invalid frame/layer and malformed contract behavior explicit", () => {
    const { seb } = loadSebFixture("simple_one_layer");
    expect(() => seb.getBRect(-1)).toThrowError(V1LookupError);
    expect(() => seb.getBRect(0, 1)).toThrowError(V1LookupError);

    const contract = JSON.parse(JSON.stringify(
      (sebEvidenceJson as SebEvidenceContract).records.find(
        (record) => record.source_member === "01_GAME_PACKS/chip/door_02.seb",
      )?.decoded,
    ));
    contract.layers[0].records = [];
    expect(() => Seb.fromContract(contract)).toThrowError(V1ContractError);
  });

  it("does not fabricate depth values when native depth metadata is absent", () => {
    expect(evidence.geometry_contract.depth_contract.status).toBe("deferred");
    expect(evidence.geometry_contract.depth_contract.native_rvas).toEqual([
      "0x1C5D5EC",
      "0x1C52994",
      "0x1C61CE0",
    ]);

    const { seb } = loadSebFixture("multi_layer");
    expect(() => seb.getDepthInfo(0, 1)).toThrowError(V1DeferredError);
    try {
      seb.getDepthInfo(0, 1, 100, 6);
    } catch (error) {
      expect(error).toBeInstanceOf(V1DeferredError);
      expect((error as V1DeferredError).code).toBe("SEB_DEPTH_UNPROVEN");
    }
  });
});

function rectTuple(rect: { readonly x: number; readonly y: number; readonly width: number; readonly height: number }): [number, number, number, number] {
  return [rect.x, rect.y, rect.width, rect.height];
}
