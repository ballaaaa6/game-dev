# MapChip Tile Seam Gate

Status: `PASS`

The seam gate was executed in the required order: one tile, adjacent x/y pairs, 2x2, varied 5x5, then the complete MapChip-only fixture. The first failure occurred at the adjacent-pair gate and was classified as `FAIL_ALPHA`.

## First failure and correction

Under the pre-correction V7 raster behavior, a transparent fragment from a later image used `REPLACE` arithmetic that cleared an already-composited destination pixel. For both the x-adjacent and y-adjacent floor pairs:

- expected alpha pixels: 3,200;
- legacy output alpha pixels: 2,820;
- missing alpha pixels: 380;
- extra alpha pixels: 0.

The isolated correction in `runtime/social-dev/src/v7/raster.ts` preserves the existing destination when the incoming `REPLACE` source pixel has alpha zero. Explicit add/subtract behavior remains unchanged. This is a compatibility-raster correction, not a production-renderer change.

## Post-correction gates

| Fixture | Cells | Components | Unexpected transparent pixels | Result |
| --- | ---: | ---: | ---: | --- |
| adjacent x | 2 | — | 0 | PASS |
| adjacent y | 2 | — | 0 | PASS |
| 2x2 | 4 | — | 0 | PASS |
| varied 5x5 | 25 | 1 | 0 | PASS |
| complete 14x14 MapChip-only | 81 | 1 | 0 | PASS |

The complete fixture reports 752 source-transparent overlap pixels and five enclosed transparent pixels from the native source alpha topology. These are not unexplained full-tile gaps: the expected source-alpha union matches the rendered alpha mask, the alpha is connected, and the unexpected-transparent metric is zero.

The forensic canvas is 1200x700 with a diagnostic origin chosen to retain the full native projection. That canvas change prevents evidence clipping; it is not visual tuning or a change to the native MapChip coordinate contract.

Full machine evidence is in `knowledge/fixtures/accepted/visual-port/mapchip-forensic/two-tile-seam-results.json`, `mapchip-2x2-results.json`, `mapchip-5x5-results.json`, and `mapchip-14x14-results.json`.
