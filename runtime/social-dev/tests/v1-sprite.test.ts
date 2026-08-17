import { describe, expect, it } from "vitest";

import { V1ContractError } from "../src/v1/errors";
import { Sprite } from "../src/v1/sprite";

const values = [101, 202, 303, 404, 505, 606, -707, -808, 909, 1001, 1102, 1203] as const;

describe("Sprite", () => {
  it("maps every native field and the translation aliases to its non-symmetric slot", () => {
    const sprite = new Sprite(values);

    expect(sprite.FrameNo).toBe(101);
    expect(sprite.TexId).toBe(202);
    expect([sprite.U, sprite.V, sprite.W, sprite.H]).toEqual([303, 404, 505, 606]);
    expect(sprite.X).toBe(-707);
    expect(sprite.TransX).toBe(-707);
    expect(sprite.Y).toBe(-808);
    expect(sprite.TransY).toBe(-808);
    expect([sprite.ReverseU, sprite.ReverseV, sprite.Blend, sprite.Color]).toEqual([909, 1001, 1102, 1203]);
    expect(sprite.getItem(6)).toBe(-707);

    sprite.setItem(6, -1707);

    expect(sprite.X).toBe(-1707);
    expect(sprite.TransX).toBe(-1707);
  });

  it("accepts every native slot index and rejects values outside the twelve-slot contract", () => {
    const sprite = new Sprite(values);

    expect(Array.from({ length: 12 }, (_, index) => sprite.getItem(index))).toEqual(values);

    for (const index of [-1, 12, 1.5]) {
      const getItem = () => sprite.getItem(index);

      expect(getItem).toThrowError(V1ContractError);
      try {
        getItem();
      } catch (error) {
        expect(error).toBeInstanceOf(V1ContractError);
        expect((error as V1ContractError).code).toBe("SPRITE_INDEX_OUT_OF_RANGE");
      }

      try {
        sprite.setItem(index, 0);
      } catch (error) {
        expect(error).toBeInstanceOf(V1ContractError);
        expect((error as V1ContractError).code).toBe("SPRITE_INDEX_OUT_OF_RANGE");
      }
    }
  });

  it("rejects non-finite item values without mutating the Sprite", () => {
    for (const value of [Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY]) {
      const sprite = new Sprite(values);
      const setItem = () => sprite.setItem(0, value);

      expect(setItem).toThrowError(V1ContractError);
      try {
        setItem();
      } catch (error) {
        expect(error).toBeInstanceOf(V1ContractError);
        expect((error as V1ContractError).code).toBe("SPRITE_VALUE_MALFORMED");
      }
      expect(sprite.FrameNo).toBe(101);
    }
  });

  it("copies exactly twelve finite values and rejects a malformed Sprite vector", () => {
    const input = [...values] as unknown as number[];
    const sprite = new Sprite(input as unknown as typeof values);

    input[0] = -1;

    expect(sprite.FrameNo).toBe(101);
    expect(() => new Sprite([1, 2, 3] as unknown as typeof values)).toThrowError(V1ContractError);
    try {
      new Sprite([1, 2, 3] as unknown as typeof values);
    } catch (error) {
      expect((error as V1ContractError).code).toBe("SPRITE_VALUES_MALFORMED");
    }
  });

  it("preserves an explicit empty Sprite state", () => {
    const sprite = Sprite.empty();

    expect(sprite.IsEmpty).toBe(true);
    expect(() => sprite.getItem(0)).toThrowError(V1ContractError);
    try {
      sprite.getItem(0);
    } catch (error) {
      expect((error as V1ContractError).code).toBe("SPRITE_EMPTY");
    }
  });
});
