# V7 raster compatibility

## Status

`PASS_STATIC`

The additive implementation is under `runtime/social-dev/src/v7/` and is not imported by the production route. It provides `RasterSurfaceCompatibilityV7`, `RasterCompatibilityV7`, deterministic PNG encoding, and pixel-diff metrics.

## Implemented rules

- Crop rectangles and independent destination rectangles are sampled from the selected source PNGs.
- Nearest and linear filtering are deterministic and tested with source-pixel-center semantics.
- Negative and out-of-bounds destinations are clipped to the surface; out-of-bounds source samples are transparent.
- Clip rectangles intersect through state snapshots; transformed fixture clips use an explicit convex polygon.
- Scale, horizontal/vertical/both flips, and isolated rotations are supported around a pivot.
- Replace, add, subtract, color modulation, alpha ratios, and the selected blend modes are covered by focused tests.
- PNGs use filter-zero scanlines and stored DEFLATE blocks, so repeated generation has stable bytes.

The detailed contracts are [sampling-contract.json](../../../knowledge/fixtures/accepted/visual-port/v7/sampling-contract.json), [transform-raster-contract.json](../../../knowledge/fixtures/accepted/visual-port/v7/transform-raster-contract.json), and [blend-alpha-contract.json](../../../knowledge/fixtures/accepted/visual-port/v7/blend-alpha-contract.json).

## Test surface

The focused V7 suite covers default state, crop/destination, clipping, filtering, transforms, flips, color/alpha, blend equations, transparent/OOB samples, PNG determinism, and V5/V6 render stability. The static Python gate additionally decodes every emitted RGBA PNG and verifies its byte hash, dimensions, fixture hash, room hash, diff hash, proof flags, and checkpoint ledger.

The backend is a compatibility reimplementation, not a claim of native GPU pixel parity. The missing shader/framebuffer evidence is explicitly nonblocking in [unknowns.json](../../../knowledge/fixtures/accepted/visual-port/v7/unknowns.json).

## Boundary

V7 does not replace `runtime/social-dev/src/production/` or alter the active route. It produces evidence and isolated previews only. V8 must make a separate cutover decision if native-compatible pixels become available.
