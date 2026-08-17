export type V4ErrorCode =
  | "V4_INPUT_MALFORMED"
  | "V4_RESOURCE_GROUP_MISMATCH"
  | "V4_IMAGE_DIMENSIONS_UNPROVEN"
  | "V4_UNSUPPORTED_SELECTOR"
  | "V4_UNSUPPORTED_BRANCH"
  | "V4_DIRECTION_OUT_OF_RANGE"
  | "V4_CELL_OUT_OF_RANGE"
  | "V4_CAMERA_VALUE_MALFORMED";

export class V4ContractError extends Error {
  public constructor(
    public readonly code: V4ErrorCode,
    message?: string,
  ) {
    super(message ?? code);
    this.name = "V4ContractError";
  }
}
