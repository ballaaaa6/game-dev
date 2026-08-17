# V2 Graphics Recovery

## Status

`V2 STATUS: PASS_STATIC`; `V2 ENTRY GATE FOR V3: PASS`; `PIXEL PARITY: DEFERRED_TO_V7`. Static/native Graphics, Seb, and ResourceManager call flow is recovered for the proven surface, and the additive runtime adapter records those semantics. Exact framebuffer pixels are not claimed because the pinned static sources do not expose the final `_drawBitmap` shader/sample output. Runtime, emulator, ADB, network, and live-app proof are explicitly out of scope for this continuation. The prior `BLOCKED/DEFERRED` raster-gate record is preserved as historical evidence in the superseding acceptance record.

Execution was inline-only and sequential. No subagents or delegated agents were used. V1 was not replaced and the production renderer was not cut over.

## Checkpoint ledger

| Checkpoint | Result | Evidence |
| --- | --- | --- |
| V2.0 native Graphics surface audit | `PASS` | `graphics-method-contract.json` |
| V2.1 state/default/stack model | `PASS WITH UNKNOWNS` | `graphics-state-contract.json` |
| V2.2 DrawImage source/destination mapping | `PASS WITH UNKNOWNS` | `draw-image-contract.json` |
| V2.3 flip and percent-scale state | `PASS WITH UNKNOWNS` | `draw-image-contract.json`, `graphics-state-contract.json` |
| V2.4 clip stack/intersection | `PASS WITH UNKNOWNS` | `clip-contract.json` |
| V2.5 color/alpha/render/blend state | `PASS WITH UNKNOWNS` | `color-blend-contract.json` |
| V2.6 Seb command composition | `PASS WITH RASTER BACKEND DEFERRED` | `seb-raster-contract.json` |
| V2.7 ResourceManager draw wrappers | `PASS WITH DEFERRED PATHS` | `resource-draw-wrapper-contract.json` |
| V2.8 native raster fixture matrix | `DEFERRED` | `native-raster-map.json`, `raster-fixture-manifest.json` |
| V2.9 static parity report and handoff | `PASS_STATIC; V3 ENTRY PASS; PIXEL PARITY DEFERRED_TO_V7` | `v2-static-acceptance.json`, `pixel-parity-results.json`, `graphics-static-recovery.json`, `unknowns.json` |

## Runtime boundary

The new code is isolated under `runtime/social-dev/src/v2/`. `GraphicsCompatibility` is a deterministic command/state adapter, not a Canvas implementation. It records the recovered crop/scaled image command, clip state, color, scale, filter, render mode, blend mode, and flip state. This preserves a semantic boundary for a future backend without allowing Canvas defaults to become native truth.

`drawSeb` routes frame selection and positive texture IDs through the existing V1 `Seb` and `ResourceManager` records. It uses validated source-slot evidence for selected metadata-only images whose source membership and dimensions are proven. `TEXID_NONE`, `TEXID_HIDELINE`, and `TEXID_HIDERECT` are skipped as native does; synthetic `TEXID_FRECT`, `TEXID_RECT`, and `TEXID_LINE` are statically mapped to native primitive calls but remain deferred in the command adapter. Depth-aware `RenderSeb` and anchor wrappers are statically traced but remain deferred at the runtime command boundary.

## Recovered semantics

- Crop `DrawImage` records destination `(dx, dy, width, height)` and source `(sx, sy, width, height)`.
- `DrawScaledImage` keeps independent source and destination sizes.
- Flip bits 1 and 2 select horizontal and vertical reversal in the native `_drawImage` path.
- Native mode 3 uses a two-axis center scale; modes 4 and 5 both select a `-90 degree` center rotation branch in the pinned binary. Final pixels remain deferred.
- Full-image `DrawImage` can enumerate Image optimization blocks before reaching `_drawImage`; atlas/custom-image dispatch is also visible before `_drawBitmap`.
- Graphics scale is percent-based and resets to 100; general origin/matrix transforms are pinned but remain deferred without a controlled transform fixture.
- Color is signed AARRGGBB; channels clamp to 0..255.
- Render operators are Replace, Add, and Subtract, with the native two-argument destination-ratio defaults.
- Seb blend flags 1, 2, and 3 push the recovered Add/Add/Subtract render modes using the native alpha-ratio formula.
- Clip intersection uses max left/top, min right/bottom, and non-negative width/height; active `GetClip` values use truncation toward zero in the proven no-transform path.

## Stop condition

The pinned IL2CPP binary and dump recover the `_drawBitmap` entry boundary, but static code/data sources do not expose its final shader/sample/compositor pixels. Therefore filtering, shader sampling, premultiplied-alpha behavior, pixel-edge clipping, and final blend rounding remain unknown and are deferred to V7. The V2 implementation records the boundary, accepts V3 for static resource ownership/index recovery, and does not use runtime proof under the current task scope.

V3 is safe to start for its static-only resource ownership/index scope; exact raster parity is not part of the V3 gate.
