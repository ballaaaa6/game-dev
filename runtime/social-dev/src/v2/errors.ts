export class V2ContractError extends Error {
  public readonly code: string;

  public constructor(code: string, message = code) {
    super(message);
    this.name = "V2ContractError";
    this.code = code;
  }
}

export class V2DeferredError extends Error {
  public readonly code: string;

  public constructor(code: string, message: string) {
    super(message);
    this.name = "V2DeferredError";
    this.code = code;
  }
}
