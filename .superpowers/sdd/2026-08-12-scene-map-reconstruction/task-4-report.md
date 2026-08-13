# Task 4 Report — SEB consumer-boundary semantics

Completed on 2026-08-13.

## What changed

- Added `tools/scene_reconstruction/csharp_trace.py` with a deterministic literal text tracer for C#/C/assembly evidence.
- Added `tools/scene_reconstruction/build_seb_semantics_contract.py` to publish the semantics contract artifact.
- Added `tools/scene_reconstruction/test_csharp_trace.py` with:
  - a negative `unknown` case for a missing consumer,
  - a bounded/sorted trace assertion,
  - field-category separation checks.
- Published `knowledge/world-assets/evidence/scene_reconstruction/seb_semantics_contract.json`.

## Evidence summary

The contract keeps these groups separate:

- SEB local crop: `u`, `v`, `w`, `h`
- local translation: `trans_x`, `trans_y`
- texture/selector: `frame`, `texture_id`
- external object/base coordinates: `ObjecX`, `ObjecY`, `ObjecZX`, `ObjecZY`
- screen/camera coordinates: `camX_`, `camY_`
- sort/depth: `ObjecSY`, `ObjecUpDown`

The trace set covers:

- `GetSprites` and `DrawSeb` variants
- `SP_*` field constants
- `RenderGameScreen`, `DrawObj`, and `AddObjec`
- `ObjecX/Y`, `ObjecZX/ZY`
- `floorparts0` and `LoadSeb`

## Results

- Missing symbol trace stays `unknown` and returns no source refs.
- Existing symbols return deterministic source refs with:
  - workspace-relative source path,
  - line number,
  - byte offset,
  - SHA-256 of the source file,
  - bounded excerpt,
  - explicit status.
- The generated contract keeps `ObjecZX/ObjecZY` as bounded contributions only; it does not collapse them into a universal world transform.
- Special texture IDs remain `candidate` unless the consumer switch and asset identity agree.

## Tests

- `python -m unittest discover -s tools/scene_reconstruction -p 'test_csharp_trace.py' -v`
- `python tools/scene_reconstruction/build_seb_semantics_contract.py`
- `python -m unittest discover -s tools/scene_reconstruction -p 'test_*.py' -v`

## Self-review

I checked the generated JSON and the status split is consistent:

- verified: crop, translation, frame selector, object/base coordinates, camera coordinates, depth boundary
- candidate: special texture IDs, reverse flags, `ObjecZX/ObjecZY`, `ObjecUpDown`
- unknown: `blend`, `color`, `end`

The main limitation is scope, not implementation: the contract is still intentionally bounded to literal text evidence and does not claim a universal world/camera transform.
