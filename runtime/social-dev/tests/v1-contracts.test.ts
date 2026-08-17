import { describe, expect, it } from "vitest";

import { SPRITE_INDEX } from "../src/v1/contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "../src/v1/errors";

describe("V1 contract primitives", () => {
  it("exposes the native twelve-slot Sprite index contract", () => {
    expect(SPRITE_INDEX).toEqual({
      FrameNo: 0,
      TexId: 1,
      U: 2,
      V: 3,
      W: 4,
      H: 5,
      TransX: 6,
      TransY: 7,
      ReverseU: 8,
      ReverseV: 9,
      Blend: 10,
      Color: 11,
    });
  });

  it("keeps malformed, missing, and deferred V1 failures distinguishable", () => {
    expect(new V1ContractError("MALFORMED_EVIDENCE").code).toBe("MALFORMED_EVIDENCE");
    expect(new V1LookupError("MISSING_RESOURCE").code).toBe("MISSING_RESOURCE");
    expect(new V1DeferredError("INTENTIONALLY_UNCLOSED").code).toBe("INTENTIONALLY_UNCLOSED");
  });
});
