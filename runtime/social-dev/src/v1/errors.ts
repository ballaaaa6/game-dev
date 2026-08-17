export class V1ContractError extends Error {
  public readonly code: string;

  public constructor(code: string, message = code) {
    super(message);
    this.name = "V1ContractError";
    this.code = code;
  }
}

export class V1LookupError extends Error {
  public readonly code: string;

  public constructor(code: string, message = code) {
    super(message);
    this.name = "V1LookupError";
    this.code = code;
  }
}

export class V1DeferredError extends Error {
  public readonly code: string;

  public constructor(code: string, message = code) {
    super(message);
    this.name = "V1DeferredError";
    this.code = code;
  }
}
