export class V3Error extends Error {
  public constructor(public readonly code: string, message = code) {
    super(message);
    this.name = "V3Error";
  }
}

export class V3LookupError extends V3Error {
  public constructor(code: string, message = code) {
    super(code, message);
    this.name = "V3LookupError";
  }
}

export class V3ContractError extends V3Error {
  public constructor(code: string, message = code) {
    super(code, message);
    this.name = "V3ContractError";
  }
}

export class V3DeferredError extends V3Error {
  public constructor(code: string, message = code) {
    super(code, message);
    this.name = "V3DeferredError";
  }
}
