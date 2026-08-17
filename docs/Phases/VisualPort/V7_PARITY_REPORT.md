# V7 parity report

## Status

`PASS_STATIC_FIDELITY`

V7 parity is accepted for the selected static command contracts and compatibility raster output. It is not a claim of exact native GPU pixels because the original shader/framebuffer path is not available in the static evidence.

## Baseline identity

| Baseline | Result | Stable identity |
| --- | --- | --- |
| V5 room:0 | pass | 74 commands / 59 traces / 788 events; command `51f69c307338fa7fe89a3d9785bc9e76e20a8863ce3f79bb74b2b8d4fc458fd6`; manifest `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788` |
| V6 room:0 + Staff | pass | 77 commands / 62 traces / 791 events; manifest `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142` |
| V7 structural raster | pass | PNG `574492baa161e195fabe16bb7848da2c392f5ad4102d8806a828e67648471b3d` |
| V7 Staff raster | pass | PNG `3793515941d6dc6c10079cf20e1d0908f9c1b55619c9c0a97019908ebed9e6ff` |

## Proof classes

- `PROVEN`: source image dimensions/hashes, selected command identity, room pass order, Staff selectors/action/direction/frame inputs, and repeat determinism.
- `INFERRED_STRONG`: bounded relationships that combine recovered call flow with selected command output.
- `COMPATIBILITY_REIMPLEMENTATION`: V7 raster bytes, filtering, blend equations, transform fixture pixels, and deterministic PNG bytes.
- `PRODUCT_POLICY`: the floor selector alias.
- `SOURCE_LIMITED`: native shader rounding, premultiplication, exact modes 4/5 pixels, complete live Staff cadence, and unused atlas/custom/depth branches.

## Gate result

The V7 Python evidence gate verifies all 14 fixture pixel/PNG hashes, both room render hashes, the diff PNG hash, proof flags, nonblocking unknowns, static-only flags, and V7 checkpoint ledger. Full Vitest, typecheck, build, JSON, Python compilation, and diff checks are recorded in [V7_PROGRESS.md](V7_PROGRESS.md).
