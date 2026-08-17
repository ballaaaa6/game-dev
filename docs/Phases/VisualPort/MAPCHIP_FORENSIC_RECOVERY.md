# MapChip Forensic Recovery

Status: `PASS_MAPCHIP_FOUNDATION`

This report records the static-only MapChip recovery gate requested after the earlier starter-room correction PASS was revoked. The earlier PASS is superseded because its full-room output contained black triangular/checkerboard gaps, discontinuous floor coverage, disconnected grass/pavement diamonds, and spatially inconsistent wall context.

## Scope and freeze

- Execution was inline and static-only.
- No emulator, ADB, APK install or launch, live game, network, browser smoke test, or local development server was used.
- Historical screenshots and the corrupt starter-room output were secondary context only. No coordinate or selector was inferred from them.
- V8 was not started. Full-room integration remains frozen until a separately authorized gate.
- The production renderer was not changed. The only implementation correction is the isolated V7 compatibility-raster alpha rule recorded in `runtime/social-dev/src/v7/raster.ts`.

## Finding

The first staged failure was not a MapChip selector, OPT, dimension, anchor, projection, or source-alpha failure. At MC.6, legacy V7 `REPLACE` arithmetic cleared existing destination pixels when a later native image contributed transparent pixels over an adjacent tile. Each x- and y-adjacent pair lost 380 expected alpha pixels before the correction. Preserving the destination under an incoming alpha-zero `REPLACE` fragment fixed the failure without changing explicit additive/subtractive operations or the production renderer.

After that isolated correction, MC.6 through MC.15 passed. The complete MapChip-only fixture contains 81 nonempty commands from the native 14x14 topology, one connected alpha component, zero unexpected transparent pixels, and a repeat-identical pixel digest.

## Gate result

| Checkpoint | Result | Evidence |
| --- | --- | --- |
| MC.0 baseline and revoked-pass classification | PASS | `checkpoint-ledger.json` |
| MC.1 selector inventory and topology | PASS | `mapchip-selector-inventory.json`, `mapchip-selector-map.json` |
| MC.2 OPT path | PASS | `mapchip-opt-audit.json` |
| MC.3 source alpha | PASS | `mapchip-alpha-audit.json` |
| MC.4 dimensions and anchors | PASS | `mapchip-dimension-anchor-audit.json` |
| MC.5 single tile | PASS | `single-tile-results.json` |
| MC.6 adjacent x/y tiles | PASS after isolated V7 correction | `two-tile-seam-results.json` |
| MC.7 2x2 | PASS | `mapchip-2x2-results.json` |
| MC.8 selector overlay | PASS | `mapchip-selector-map.json` |
| MC.9 varied 5x5 | PASS | `mapchip-5x5-results.json` |
| MC.10 complete 14x14 MapChip-only | PASS | `mapchip-14x14-results.json` |
| MC.11 ownership split | PASS | `outer-vs-room-floor-ownership.json` |
| MC.12 root-cause correction | PASS | `root-cause.json`, `two-tile-seam-results.json`, V7 raster correction |
| MC.13 visual evidence package | PASS | `contact-sheet.json`, forensic contact sheet |
| MC.14 stop before full room | PASS | `unknowns.json`, ownership matrix |
| MC.15 STOP | PASS | `checkpoint-ledger.json` |

## Remaining boundary

The floor selector/data identity remains `85/floor_09.png` as an explicit compatibility-policy alias, while the rendered pixels remain the source-backed `floor_05.png` candidate. Native provenance and full-room layer interaction remain open or deferred in `unknowns.json`; neither is a reason to start V8 or rebuild the full room in this task.

The machine-readable ledger and previews are under `knowledge/fixtures/accepted/visual-port/mapchip-forensic/`. The staged forensic test is `runtime/social-dev/tests/mapchip-forensic.test.ts`.
