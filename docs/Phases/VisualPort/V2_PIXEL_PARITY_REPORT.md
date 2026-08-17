# V2 Pixel Parity Report

## V2 status

`V2 STATUS: PASS_STATIC; V2 ENTRY GATE FOR V3: PASS; PIXEL PARITY: DEFERRED_TO_V7`

The earlier `V2 STATUS: BLOCKED; PIXEL PARITY: DEFERRED` result is retained as a historical prior gate. The superseding static acceptance record separates the completed static/semantic gate from the unavailable native framebuffer proof.

The semantic Graphics, Seb, and ResourceManager contract is recovered for the selected static evidence. Exact raster parity is not complete because the pinned static sources do not expose the final `_drawBitmap` framebuffer pixels for the same fixture, source rectangle, destination rectangle, clip, filter, color, and blend state. Runtime/emulator/ADB/network evidence is excluded from this continuation.

## What is proven

- The current full repository regression after V2 changes is 35 test files and 132 tests; the historical V1 pre-change gate remains recorded in the earlier V1 report.
- Native DrawImage crop and DrawScaledImage source/destination mappings are disassembled and tested.
- Native state defaults, clip stack/intersection, AARRGGBB color packing, percent scale, render-mode defaults, blend mappings, and alpha-ratio rounding are recorded.
- Seb frame modulo, layer order, translation, positive ResourceManager image routing, `TEXID_NONE` skipping, and ReverseU reset are tested.
- Static native recovery additionally closes hidden SEB sentinel no-draw paths, synthetic primitive dispatch targets, CustomImages-before-`img[]` lookup order, center-based flip matrix branches, optimized-image block dispatch, and anchor/depth wrapper call flow.
- Source pixel hashes for the selected V1 logical fixtures remain recorded; they are input identities, not native output hashes.

## What is not proven

No native output hash or browser output hash is recorded. The missing static shader/framebuffer source prevents claims about Canvas image smoothing, shader sampling, premultiplied-alpha behavior, blend rounding, pixel-edge clipping, transformed backend coordinates, rotated output pixels, synthetic primitive pixels, depth output pixels, and anchor output pixels. The evidence file `pixel-parity-results.json` records `native_capture_hashes: null` and `browser_capture_hashes: null` for this reason.

The V2 runtime is an additive command/state layer under `runtime/social-dev/src/v2/`; it does not replace the production renderer. It does not flatten SEB records, bypass ResourceManager/Seb, or invent a Canvas default.

## Gate decision

The exact raster boundary remains a non-blocking V7 deferral. V2 is accepted for V3 static resource ownership/index recovery with no approximation and no live runtime or framebuffer capture. V3 must preserve the same evidence-only boundary.
