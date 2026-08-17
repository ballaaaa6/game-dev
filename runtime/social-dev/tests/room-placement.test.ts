import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";

describe("native room placement contract", () => {
  it("loads the bounded room:0 placement fixture at the runtime boundary", () => {
    const catalogs = loadRuntimeCatalogs();
    const placement = catalogs.roomPlacement;

    expect(placement.status).toBe("pass");
    expect(placement.semantic_status).toBe("approved_for_runtime_contract");
    expect(placement.scene_ref.id).toBe("room:0");
    expect(placement.native_placement.door.cell).toEqual({
      x: 8,
      y: 4,
      raw_map_value: 5,
      raw_dir_value: 0,
    });
    expect(placement.native_placement.door.installed_flag).toBe(1);
    expect(placement.native_placement.door.place_obj_furniture_data).toBeNull();
    expect(placement.native_placement.type4.footprint).toHaveLength(9);
    expect(placement.native_placement.route_fixture.path).toEqual([[8, 4], [7, 4], [6, 4]]);
  });

  it("keeps selector gaps, pass order, and room-placement exclusion explicit", () => {
    const placement = loadRuntimeCatalogs().roomPlacement;

    expect(placement.selectors.floor.resolution_status).toBe("unresolved");
    expect(placement.selectors.floor.reason_code).toBe("missing_img_inf_entry");
    expect(placement.selectors.floor.runtime_resolution_status).toBe("explicit_fallback");
    expect(placement.selectors.floor.runtime_fallback?.target_selector_id).toBe(85);
    expect(placement.selectors.floor.runtime_fallback?.filename).toBe("floor_09.png");
    expect(placement.selectors.floor.runtime_fallback?.resolution_mode).toBe("explicit_user_approved_alias");
    expect(placement.selectors.wall.filename).toBe("wall_00.png");
    expect(placement.selectors.door.filename).toBe("door_01.png");
    expect(placement.object_boundary.runtime_policy.promote_furniture_2).toBe(true);
    expect(placement.runtime_policy.quarantined_objects_excluded).toEqual([]);
    expect(placement.draw_order.overlap_fixture.expected_event_order).toEqual(["door-object", "floor-image"]);
  });
});
