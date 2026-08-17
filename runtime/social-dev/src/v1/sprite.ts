import { SPRITE_INDEX, assertSpriteValues, type SpriteValues } from "./contracts";
import { V1ContractError } from "./errors";

export class Sprite {
  private values: number[] | undefined;

  public constructor(values?: SpriteValues) {
    if (values !== undefined) {
      assertSpriteValues(values);
      this.values = [...values];
    }
  }

  public static empty(): Sprite {
    return new Sprite();
  }

  public get IsEmpty(): boolean {
    return this.values === undefined;
  }

  public get FrameNo(): number { return this.getItem(SPRITE_INDEX.FrameNo); }
  public get TexId(): number { return this.getItem(SPRITE_INDEX.TexId); }
  public get U(): number { return this.getItem(SPRITE_INDEX.U); }
  public get V(): number { return this.getItem(SPRITE_INDEX.V); }
  public get W(): number { return this.getItem(SPRITE_INDEX.W); }
  public get H(): number { return this.getItem(SPRITE_INDEX.H); }
  public get X(): number { return this.getItem(SPRITE_INDEX.TransX); }
  public get Y(): number { return this.getItem(SPRITE_INDEX.TransY); }
  public get TransX(): number { return this.getItem(SPRITE_INDEX.TransX); }
  public get TransY(): number { return this.getItem(SPRITE_INDEX.TransY); }
  public get ReverseU(): number { return this.getItem(SPRITE_INDEX.ReverseU); }
  public get ReverseV(): number { return this.getItem(SPRITE_INDEX.ReverseV); }
  public get Blend(): number { return this.getItem(SPRITE_INDEX.Blend); }
  public get Color(): number { return this.getItem(SPRITE_INDEX.Color); }

  public getItem(index: number): number {
    return this.requireValues()[this.validateIndex(index)];
  }

  public setItem(index: number, value: number): void {
    const values = this.requireValues();
    const validIndex = this.validateIndex(index);
    this.validateValue(value);
    values[validIndex] = value;
  }

  private requireValues(): number[] {
    if (this.values === undefined) {
      throw new V1ContractError("SPRITE_EMPTY");
    }
    return this.values;
  }

  private validateIndex(index: number): number {
    if (!Number.isInteger(index) || index < 0 || index >= 12) {
      throw new V1ContractError("SPRITE_INDEX_OUT_OF_RANGE");
    }
    return index;
  }

  private validateValue(value: number): void {
    if (!Number.isFinite(value)) {
      throw new V1ContractError("SPRITE_VALUE_MALFORMED");
    }
  }
}
