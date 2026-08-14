import { describe, expect, it } from "vitest";
import {
  actorDisplayFrame,
  displayAssetManifest,
  furnitureFrameForScene,
  furnitureDisplayFrame,
  resolveRuntimeMapFilename,
  selectDisplayFrame,
} from "../src/assets/display-assets";
import { resolveFloorRender } from "../src/catalog/floor-resolution";

describe("approved display asset adapter", () => {
  it("loads only the approved subset manifest", () => {
    expect(displayAssetManifest.status).toBe("pass");
    expect(displayAssetManifest.semantic_status).toBe("approved_for_runtime_subset");
    expect(displayAssetManifest.assets).toHaveLength(34);
    expect(displayAssetManifest.actors).toHaveLength(5);
    expect(displayAssetManifest.scope).toBe("actor-frame-subset-proven-chip-compositions-native-wall-door-composition-and-explicit-floor-fallback");
    expect(displayAssetManifest.assets.some((asset) => asset.asset_member === "01_GAME_PACKS/chip/floor_09.png")).toBe(true);
    expect(displayAssetManifest.assets.some((asset) => asset.asset_member === "01_GAME_PACKS/chip/wall_00.png")).toBe(true);
    expect(displayAssetManifest.assets.some((asset) => asset.asset_member === "01_GAME_PACKS/chip/door_01.png")).toBe(true);
    expect(displayAssetManifest.assets.filter((asset) => asset.kind === "derived_opt_reconstruction")).toHaveLength(4);
    expect(Object.keys(displayAssetManifest.objects).sort()).toEqual(["furniture:0", "furniture:1", "furniture:2", "furniture:5"]);
    expect(Object.keys(displayAssetManifest.native_initial_objects).sort()).toEqual([
      "furniture:12",
      "furniture:26",
      "furniture:3",
      "furniture:56",
    ]);
    expect(displayAssetManifest.native_initial_objects["furniture:3"].img_selector_id).toBe(148);
    expect(displayAssetManifest.native_initial_objects["furniture:12"].records[0].source_asset_member).toContain("garbage_can.png");
    expect(displayAssetManifest.phase3a.status).toBe("approved");
    expect(displayAssetManifest.phase3a.target).toBe("furniture:2");
    expect(displayAssetManifest.phase3a.runtime_promotion).toBe("approved");
    expect(displayAssetManifest.runtime_policy.unapproved_assets_are_not_loaded).toBe(true);
  });

  it("selects the bounded wait and typing SEB records deterministically", () => {
    const wait = displayAssetManifest.actors[0].animations.wait;
    const typing = displayAssetManifest.actors[0].animations.typing;
    expect(selectDisplayFrame(wait, 0).source_x).toBe(0);
    expect(selectDisplayFrame(wait, 9).source_x).toBe(0);
    expect(selectDisplayFrame(wait, 10).source_x).toBe(30);
    expect(selectDisplayFrame(wait, 19).source_x).toBe(30);
    expect(selectDisplayFrame(wait, 20).source_x).toBe(0);
    expect(selectDisplayFrame(typing, 0).source_x).toBe(120);
    expect(selectDisplayFrame(typing, 10).source_x).toBe(240);
    expect(selectDisplayFrame(typing, 20).source_x).toBe(120);
  });

  it("keeps the complete floor05 pixels under the floor05 lookup", () => {
    expect(resolveRuntimeMapFilename("floor_05.png")).toBe("floor_05.png");
    expect(resolveRuntimeMapFilename("floor_09.png")).toBe("floor_09.png");
  });

  it("uses floor09 selector metadata with floor05 render pixels", () => {
    const floor = resolveFloorRender();
    expect(floor.selectorId).toBe(85);
    expect(floor.metadataSelectorId).toBe(85);
    expect(floor.metadataFilename).toBe("floor_09.png");
    expect(floor.filename).toBe("floor_05.png");
    expect(floor.assetId).toBe("map:chip/floor_05.png");
    expect(floor.synthetic).toBe(true);
  });

  it("keeps actor selector identity and furniture composition explicit", () => {
    const actorFrame = actorDisplayFrame(0, "wait", 10, 10);
    expect(actorFrame?.imageAssetId).toBe("asset:01_GAME_PACKS/human/chara86.png");
    expect(actorFrame?.frame.destination_x).toBe(-14);
    expect(actorDisplayFrame(0, "wait", 11, 0)).toBeNull();

    const furniture = furnitureDisplayFrame();
    expect(furniture?.object.object_id).toBe("furniture:0");
    expect(furniture?.frame.source_asset_member).toBe("big_base00.png");
    expect(furniture?.frame.source_status).toBe("pass");

    const door = furnitureDisplayFrame("furniture:1");
    expect(door?.frame.source_asset_member).toBe("door_02.png");
    expect(door?.frame.source_status).toBe("pass_opt_logical");
    expect(door?.object.source_compositions?.[0].opt_status).toBe("pass");

    const workstation = furnitureDisplayFrame("furniture:5");
    expect(workstation?.frame.source_asset_member).toBe("desk_00.png");
    expect(workstation?.object.sub_composition?.filename).toBe("chair_02.seb");

    const recoveredDesk = furnitureDisplayFrame("furniture:2");
    expect(recoveredDesk?.object.phase3a_closure?.status).toBe("approved");
    expect(recoveredDesk?.object.sub_composition?.filename).toBe("chair_00.seb");
    expect(recoveredDesk?.object.sub_composition?.source_compositions?.[0].opt_status).toBe("pass");

    const nativeDesk = furnitureDisplayFrame("furniture:3");
    expect(nativeDesk?.object.name).toBe("Wooden Desk");
    expect(nativeDesk?.object.furniture_data_id).toBe(3);
    expect(nativeDesk?.object.display_mode).toBe("native_selector_composition");

    const nativeEquipment = furnitureDisplayFrame("furniture:12");
    expect(nativeEquipment?.object.name).toBe("Trash Can");
    expect(nativeEquipment?.frame.source_status).toBe("pass_native_img_asset");
  });

  it("selects composed object frames without mutating the manifest", () => {
    const doorFrame = furnitureDisplayFrame("furniture:1", 1);
    expect(doorFrame?.frame.source_x).toBe(13);
    expect(doorFrame?.frame.destination_x).toBe(23);

    const workstationFrame = furnitureDisplayFrame("furniture:5", 2);
    expect(workstationFrame?.frame.source_x).toBe(60);
    expect(workstationFrame?.subFrame?.source_x).toBe(120);
    expect(workstationFrame?.subImageAssetId).toBe("asset:derived/02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_02.png");
    expect(workstationFrame?.frame.runtime_size).toEqual({ width: 120, height: 32 });
    expect(workstationFrame?.frame.runtime_status).toBe("pass_derived_opt_png");
  });

  it("keeps the native computer composition on frame zero in every scene mode", () => {
    const floor00Desk = furnitureFrameForScene("furniture:3", 2, "floor00");

    expect(floor00Desk?.frame.start_frame).toBe(0);
    expect(floor00Desk?.subFrame?.start_frame).toBe(0);
  });
});
