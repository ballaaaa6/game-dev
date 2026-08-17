# V7 graphics fidelity

## Status

`PASS_STATIC_FIDELITY`

V7 closes the selected graphics contract for the room:0 and room:0 + Staff static scenes. The work is inline-only and static-only. No emulator, ADB, live APK/game, server, network, live browser, or runtime screenshot was used as evidence. The production renderer was not changed or cut over.

## Closed contract

The V7 backend consumes the V2 `GraphicsCommand` stream without changing command identity. The selected paths are `DrawImage` crop, `DrawScaledImage`, direct FurnitureData image selection, SEB source-slot resolution, clip intersection, state push/pop, and the selected Staff image draws. The command stream remains the authoritative geometry and ordering input.

The recovered/native boundaries are retained in `knowledge/fixtures/accepted/visual-port/v7/graphics-raster-contract.json`. Relevant static native anchors include `DrawImage` `0x1C0EF98`, `DrawScaledImage` `0x1C0F0C8`, `_drawBitmap` `0x1C10388`, clip operations around `0x1C08694`, `SetColor` `0x1C09D60`, `SetFlip` `0x1C1B54C`, `Scale` `0x1C07C6C`, and `GetTransRect` `0x1C085E8`.

## Proof classification

| Surface | Classification | Boundary |
| --- | --- | --- |
| selected source image dimensions and hashes | `PROVEN` | Source PNG/derived logical PNG manifests and command image dimensions agree. |
| V5/V6 command identity and ordering | `PROVEN` | V5 remains 74 commands / 59 traces / 788 events; V6 remains 77 / 62 / 791. |
| floor selector `5 -> 85 -> floor_05.png` | `PRODUCT_POLICY` | The compatibility alias is explicit; it is not claimed as native numeric identity. |
| V7 byte raster output | `COMPATIBILITY_REIMPLEMENTATION` | Native shader/framebuffer bytes are unavailable; deterministic rules are isolated under `src/v7`. |
| complete Staff timing | `SOURCE_LIMITED` | Selected action/direction/frame fixtures are closed; live cadence is not claimed. |

The full contract is recorded in [graphics-raster-contract.json](../../../knowledge/fixtures/accepted/visual-port/v7/graphics-raster-contract.json), [selected-path-closure.json](../../../knowledge/fixtures/accepted/visual-port/v7/selected-path-closure.json), and [unknowns.json](../../../knowledge/fixtures/accepted/visual-port/v7/unknowns.json).

## Compatibility assumptions

- The default V2 signed color `0xFF000000` is treated as an identity sentinel because selected V5/V6 commands do not set a tint color.
- Output is straight-alpha RGBA bytes; native premultiplication and shader rounding remain unknown.
- Nearest sampling uses source pixel centers; linear sampling uses four-neighbor bilinear interpolation.
- Out-of-bounds source samples are transparent.
- Axis clips and the isolated transformed polygon clip are evaluated against transformed world pixel centers.
- Flip modes 1–3 are center flips. Modes 4–5 have explicit compatibility rotations but remain source-limited for final native pixels.

## Evidence result

The selected room renders and all 14 golden fixtures are deterministic. Exact hashes and residual classifications are in [fidelity-manifest.json](../../../knowledge/fixtures/accepted/visual-port/v7/fidelity-manifest.json) and [pixel-diff-results.json](../../../knowledge/fixtures/accepted/visual-port/v7/pixel-diff-results.json).
