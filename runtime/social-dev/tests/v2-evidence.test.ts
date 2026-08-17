import { describe, expect, it } from "vitest";

import clipContract from "../../../knowledge/fixtures/accepted/visual-port/v2/clip-contract.json";
import colorBlendContract from "../../../knowledge/fixtures/accepted/visual-port/v2/color-blend-contract.json";
import drawImageContract from "../../../knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json";
import graphicsStaticRecovery from "../../../knowledge/fixtures/accepted/visual-port/v2/graphics-static-recovery.json";
import graphicsMethodContract from "../../../knowledge/fixtures/accepted/visual-port/v2/graphics-method-contract.json";
import graphicsStateContract from "../../../knowledge/fixtures/accepted/visual-port/v2/graphics-state-contract.json";
import nativeRasterMap from "../../../knowledge/fixtures/accepted/visual-port/v2/native-raster-map.json";
import pixelParityResults from "../../../knowledge/fixtures/accepted/visual-port/v2/pixel-parity-results.json";
import rasterFixtureManifest from "../../../knowledge/fixtures/accepted/visual-port/v2/raster-fixture-manifest.json";
import resourceDrawWrapperContract from "../../../knowledge/fixtures/accepted/visual-port/v2/resource-draw-wrapper-contract.json";
import sebRasterContract from "../../../knowledge/fixtures/accepted/visual-port/v2/seb-raster-contract.json";
import unknowns from "../../../knowledge/fixtures/accepted/visual-port/v2/unknowns.json";
import v2StaticAcceptance from "../../../knowledge/fixtures/accepted/visual-port/v2/v2-static-acceptance.json";

describe("V2 evidence closure", () => {
  it("keeps the native source and recovered method surface pinned", () => {
    expect(graphicsMethodContract.source.apk_sha256).toBe(
      "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    );
    expect(graphicsMethodContract.methods).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ method: "SetClip", native_rva: "0x1C0812C" }),
        expect.objectContaining({ method: "DrawImage", native_rva: "0x1C0EF98" }),
        expect.objectContaining({ method: "SetColor", native_rva: "0x1C09D60" }),
        expect.objectContaining({ method: "Scale", native_rva: "0x1C07C6C" }),
      ]),
    );
    expect(graphicsStateContract.field_offsets.flip_mode).toBe("0x40");
    expect(drawImageContract.overloads).toHaveLength(3);
    expect(clipContract.operations).toHaveLength(7);
    expect(colorBlendContract.seb_sprite_blend).toHaveLength(4);
  });

  it("records static native call-flow recovery without promoting framebuffer behavior", () => {
    expect(graphicsStaticRecovery.execution_policy.runtime_execution_used_for_this_record).toBe(false);
    expect(graphicsStaticRecovery.execution_policy.adb_or_emulator_used_for_this_record).toBe(false);
    expect(graphicsStaticRecovery.graphics.draw_image_dispatch.flip_matrix.mode_4)
      .toContain("RotateTemporary(-90 degrees");
    expect(graphicsStaticRecovery.graphics.draw_image_dispatch.flip_matrix.mode_5)
      .toContain("RotateTemporary(-90 degrees");
    expect(graphicsStaticRecovery.seb.sentinel_dispatch.hide_line.native_behavior).toContain("no draw");
    expect(graphicsStaticRecovery.resource_manager.get_image.lookup_order).toContain("CustomImages");
    expect(graphicsStaticRecovery.pixel_boundary.status).toBe("deferred");
  });

  it("keeps SEB/resource routing additive and fixture-backed", () => {
    expect(sebRasterContract.runtime_surface).toBe("runtime/social-dev/src/v2/seb-raster.ts");
    expect(sebRasterContract.native_methods).toMatchObject({
      draw_anchor: "0x1C5E5F8",
      draw_ratio: "0x1C5E97C",
      draw_repeat: "0x1C5EF00",
    });
    expect(resourceDrawWrapperContract.resource_manager_fields).toMatchObject({ img: "this+0x10", seb: "this+0x18" });
    expect(rasterFixtureManifest.fixtures).toHaveLength(6);
    expect(rasterFixtureManifest.image_sources).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ source_member: "01_GAME_PACKS/chip/wall_00.png", status: "proven" }),
        expect.objectContaining({ source_member: "01_GAME_PACKS/human/chara00.png", status: "proven" }),
      ]),
    );
  });

  it("normalizes the static V2 gate without claiming pixel parity", () => {
    expect(nativeRasterMap.status).toBe("pass_static");
    expect(nativeRasterMap.pixel_proof_status).toBe("deferred");
    expect(nativeRasterMap.native_capture.available).toBe(false);
    expect(pixelParityResults.overall).toBe(
      "V2 STATUS: PASS_STATIC; V2 ENTRY GATE FOR V3: PASS; PIXEL PARITY: DEFERRED_TO_V7",
    );
    expect(pixelParityResults.pixel_parity.status).toBe("deferred");
    expect(pixelParityResults.pixel_parity.native_capture_hashes).toBeNull();
    expect(pixelParityResults.v3_safe).toBe(true);
    expect(pixelParityResults.accepted_for_v3).toBe(true);
    expect(pixelParityResults.historical_prior_gate.overall).toBe(
      "V2 STATUS: BLOCKED; PIXEL PARITY: DEFERRED",
    );
    expect(v2StaticAcceptance.status).toBe("PASS_STATIC");
    expect(v2StaticAcceptance.v2_entry_gate_for_v3).toBe("PASS");
    expect(v2StaticAcceptance.accepted_for_v3).toBe(true);
    expect(v2StaticAcceptance.pixel_parity).toBe("DEFERRED_TO_V7");
    expect(unknowns.v3_entry_blocking).toBe(false);
    expect(unknowns.unknowns).toEqual(
      expect.arrayContaining([expect.objectContaining({ id: "v2-native-raster-capture", impact: "critical" })]),
    );
  });
});
