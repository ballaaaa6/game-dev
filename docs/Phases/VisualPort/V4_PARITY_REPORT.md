# V4 Static Parity Report

## Result

Phase V4 reaches `PASS_STATIC_COMMAND_PARITY` for the selected MapChip, ObjChip, FurnitureData binding, Camera, and local ordering scope. The proof is static native/source/call-flow evidence plus deterministic command recording against real V3 `resChip_` fixtures.

The focused run passed:

```text
npm exec vitest -- run tests/v4-map-chip.test.ts tests/v4-obj-chip.test.ts tests/v4-furniture-camera-ordering.test.ts tests/v4-regression.test.ts
4 files, 20 tests passed
```

The observed matrix is recorded in `knowledge/fixtures/accepted/visual-port/v4/command-parity-results.json`.

The final repository gate also passed: `npm test` reported `40` files and `160` tests, `npm run typecheck` completed cleanly, `npm run build` completed successfully, and the V1/V3/asset/closure Python gates remained green.

## Regression boundary

V4 uses the existing V1 SEB contract, V2 GraphicsCompatibility command recorder, and V3 numeric ResourceManagerV3. Regression checks preserve the `resChip_` group, sparse numeric slots, selector `85` floor alias, V3 ready state, raw type-5 door separation, and the no-raw-type-to-FurnitureData rule. V4 code is isolated under `runtime/social-dev/src/v4/` and is not imported by the production renderer.

## Deferred proof

Exact native framebuffer pixels, shader/sample/filter/alpha/compositor parity, live viewport behavior, emulator/ADB observation, and full Room orchestration are outside this static V4 gate. Pixel parity remains `DEFERRED_TO_V7`; generic and catalogue branches are listed as nonblocking V5 unknowns. No server, live app, emulator, ADB, or network evidence was used.
