# Social Dev Phase 1B — Scene and staff-behavior extraction

Date: 2026-08-13

Status: historical candidate extraction passed structural validation; all
display-slice review items are now closed by the Pre-runtime Closure Sweep.
The candidate evidence is not rewritten and remains separate from the active
runtime contracts.

## Results

Phase 1B continues from the first-slice package by extracting the scene grid, object-code candidate, and staff living observations from real loader/source evidence. Results are machine-readable evidence separate from runtime, and decompiled C# is not executed in the web application.

Latest checks:

- Parsed records: `22` from English/Japanese; every row was fully consumed according to the loader sequence.
- RoomData(0): `objMap_` and `objDir_` are rectangular `10×10` grids.
- Raw door-code candidate: `(x=8, y=4, raw_map_value=5)`; value `5` matches the `ObjChip` door constant only at the source-label level.
- Derived links: `StaffData.jobId_ → JobData(4)` and loader-aware `StaffData.skill_ → SkillData(1)`; both remain candidate links.
- Scene source slices: `13`; behavior source slices: `15`.
- Staff transition candidates: `7`.
- Historical blocking review items: `8`.
- Validation status: `pass`.
- Active closure status: `closed_before_runtime`.

## Primary machine-readable files

- `knowledge/fixtures/accepted/scene_data_candidate.json`
- `knowledge/fixtures/accepted/staff_behavior_candidate.json`
- `knowledge/fixtures/accepted/scene_behavior_validation.json`

## Plan and builders

- `docs/roadmap/Roadmap_SocialDev_Phase1B_SceneBehavior.md`
- `tools/social-dev/build_scene_behavior_candidates.py`
- `tools/social-dev/test_scene_behavior_candidates.py`

## Parsing method

Field/load order from `RoomData`, `FurnitureData`, `StaffData`, `JobData`, and `SkillData` was combined with `StringArrayStream` framing for `GetIntArray` and `GetIntIntArray`. This verifies scalar prefixes, array shapes, row exhaustion, and locale alignment.

The important point is that `StaffData.skill_` appears after an array reader, so selecting `SkillData(0)` from an approximate position was unsafe. After complete framing, all five selected staff records yielded `skill_ = 1`, so the supporting candidate was corrected to `SkillData(1)`; lookup semantics are still not verified.

## Scene candidate

Retain raw `objMap_` and `objDir_` with cell lists, grid dimensions, furniture projection, and coordinate formulas from `Room.cs`:

- `GetXbyIndex(ix, iy) = (iy + ix) * 20 + 20`
- `GetYbyIndex(ix, iy) = (iy - ix) * 10 + 18`

This is sufficient for deterministic fixtures and data-assembly checks, but not for actual room placement or routing because map-code meaning, footprint, standing positions, and passability still require method-body/assembly evidence.

## Staff behavior candidate

Retain state/move/flag constants as `source_label_only` and transition observations where `Staff.cs` clearly writes values, such as stay-home, go to equipment, go to talk, route-goal mapping, and typing/talk frame hooks. Do not create new semantic product labels for numeric states.

Runtime behavior not yet created includes route paths, complete movement timing, animation selectors, asset lookup, and skill relationships to jobs/actors.

## Historical review queue and current disposition

The eight historical items are mapped one-for-one in
`knowledge/fixtures/accepted/semantic_review_closure.json`. Map-code,
passability, skill, selector, and animation claims are verified from the
Phase 1D/Phase 2 authorities. Room placement is closed only for the bounded
display fixtures. Numeric labels remain source labels, and decompiler update
bodies remain quarantined.

## Active closure artifacts

- `knowledge/fixtures/accepted/semantic_review_closure.json`
- `knowledge/fixtures/accepted/phase1_supersession.json`
- `knowledge/fixtures/accepted/runtime/entity_contract.json`
- `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json`

Re-run with:

```powershell
python -B tools/social-dev/build_first_slice_data_candidate.py
python -B tools/social-dev/test_first_slice_data_candidate.py
python -B tools/social-dev/build_scene_behavior_candidates.py
python -B tools/social-dev/test_scene_behavior_candidates.py
```
