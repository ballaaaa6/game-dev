import { V3ContractError } from "./errors";

export class IndexedImage {
  public readonly imageAtlasId = -1;

  public readonly atlasRegion = null;

  private useCount = 0;

  public constructor(
    public readonly groupId: string,
    public readonly id: number,
    public readonly filename: string,
    public readonly sourceIndexMember: string,
    public readonly sourceMember: string,
    public readonly sourceSha256: string | null,
    public readonly sourceBytes: number | null,
    public readonly flags: readonly string[],
    public readonly aliasIds: readonly number[],
  ) {
    if (!Number.isSafeInteger(id) || id < 0 || sourceMember.length === 0) {
      throw new V3ContractError("IMAGE_INDEX_ENTRY_MALFORMED");
    }
  }

  public getUseCount(): number {
    return this.useCount;
  }

  public use(): void {
    this.useCount += 1;
  }

  public unuse(): void {
    if (this.useCount > 0) {
      this.useCount -= 1;
    }
  }
}
