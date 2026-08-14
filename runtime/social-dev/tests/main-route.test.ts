import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import { buildSceneProjection } from "../src/scene/projection";
import { parseMainRuntimeRoute } from "../src/app/main-route";

describe("unified main runtime route", () => {
  it("defaults to the approved floor00 main context", () => {
    const route = parseMainRuntimeRoute("");

    expect(route.roomId).toBe("room:0");
    expect(route.sceneOptions).toEqual({
      nativeFloorValue: 0,
      context: "main_display",
      sceneMode: "floor00",
    });
    expect(route.rawOverlayEnabled).toBe(false);
    expect(route.initialTicks).toBe(0);
    expect(route.auto).toBe(true);
  });

  it("keeps all room data on main while ignoring alternate route selectors", () => {
    const route = parseMainRuntimeRoute(
      "?room=room:17&scene=display-slice-01&nativeFloor=1&context=addition_floor_preview&overlay=raw&initialTicks=136&auto=0",
    );

    expect(route.roomId).toBe("room:17");
    expect(route.sceneOptions).toEqual({
      nativeFloorValue: 0,
      context: "main_display",
      sceneMode: "floor00",
    });
    expect(route.rawOverlayEnabled).toBe(true);
    expect(route.initialTicks).toBe(136);
    expect(route.auto).toBe(false);

    const projection = buildSceneProjection(loadRuntimeCatalogs(), route.roomId, route.sceneOptions);
    expect(projection.sceneMode).toBe("floor00");
    expect(projection.roomContext).toBe("main_display");
    expect(projection.nativeFloorValue).toBe(0);
  });

  it("does not create an alternate route from invalid tick input", () => {
    const route = parseMainRuntimeRoute("?initialTicks=not-a-number");

    expect(route.initialTicks).toBe(0);
    expect(route.sceneOptions.sceneMode).toBe("floor00");
  });

  it("uses floor00 for the main projection when no scene query is supplied", () => {
    const projection = buildSceneProjection(loadRuntimeCatalogs());

    expect(projection.sceneMode).toBe("floor00");
    expect(projection.roomContext).toBe("main_display");
    expect(projection.nativeFloorValue).toBe(0);
  });
});
