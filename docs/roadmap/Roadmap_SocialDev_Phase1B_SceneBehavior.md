# Social Dev Phase 1B — Scene and staff-behavior extraction

Status: **closed by the Pre-runtime Closure Sweep for display-slice-01**

The candidate package remains historical evidence. Scene and behavior claims
are reconciled to the Phase 1D and Phase 2 contracts by
`knowledge/fixtures/accepted/semantic_review_closure.json`.

Start date: 2026-08-13

## Goal

Continue from the first-slice raw-data candidate and produce an evidence package that explains which inputs the room grid, object layer, coordinate transform, passability, and staff living loop require, without creating the web runtime or executing decompiled C#.

## First-slice scope

- Room: `RoomData(0)` — `Floor A`
- Grid: loader-parsed `objMap_` and `objDir_`, size `10×10`
- Furniture: `FurnitureData(1, 2, 5)` — Door, Desk, Graphics Workstation
- Staff: `StaffData(0–4)`
- Job: `JobData(4)` from `StaffData.jobId_`
- Skill: derived from `StaffData.skill_` after array framing; status remains `order_candidate`
- Route: retain grid/door/goal candidates first; do not create a path that is not supported by verified passability semantics

## Extraction method

1. Use the C# `StringArrayStream` reader sequence as the initial framing contract: scalar, `GetIntArray`, `GetIntIntArray`, and strings in source order.
2. Verify that the parser consumes the complete raw row and produces the same shape in English/Japanese before storing typed candidates.
3. Retain raw columns, parsed fields, row hashes, source line/hash references, and parser warnings.
4. Separate values explicitly stated by the source, such as field order, constants, and coordinate formulas, from inferred values such as map-value semantics, passability, placement, and asset selectors.
5. Build bounded transition observations from `Staff` only for branches that clearly write state/move-mode/flag values; do not create new semantic names for numeric states.

## Source evidence

### Scene/object

- `data/RoomData.cs`: field/load order for costs, map, direction, and image IDs
- `game/Room.cs`: map/object initialization, door scan, grid dimensions, and index-to-screen formulas
- `game/MapChip.cs`: tile dimensions and draw transform
- `game/ObjChip.cs`: object type/direction constants, occupancy/passability hooks, and standing/use positions
- `game.routeSearch/Astar.cs` and `Node.cs`: node grid, goal flags, neighbor search, and Manhattan-cost candidate

### Staff/living behavior

- `data/StaffData.cs`, `data/JobData.cs`, `data/SkillData.cs`: loader-aware actor/job/skill records
- `game/Staff.cs`: initialization defaults, state/move constants, route calls, work/talk/equipment branches, animation-selector fields, and visible transition hooks

## Required outputs

- `knowledge/fixtures/accepted/scene_data_candidate.json`
- `knowledge/fixtures/accepted/staff_behavior_candidate.json`
- `knowledge/fixtures/accepted/scene_behavior_validation.json`
- `docs/reports/social-dev_phase1b_scene_behavior_report.md`
- `tools/social-dev/build_scene_behavior_candidates.py`
- `tools/social-dev/test_scene_behavior_candidates.py`

## Validation gates

- Selected English/Japanese rows have matching IDs and column framing.
- RoomData arrays parse completely, have matching shapes, and consume each raw row to the end.
- Selected furniture/staff/job/skill rows parse completely according to the loader sequence.
- StaffData `jobId_` and `skill_` links point to existing rows but remain `order_candidate`.
- The transform fixture is deterministic for grid corners and the door candidate.
- Behavior observations have source references and do not promote numeric labels to product semantics.
- Output semantic status must be `pending_review`; do not write under `runtime/social-dev/catalog/`.

## Not done in Phase 1B

- Do not create a route path that relies on unverified passability.
- Do not create actual room placement from the furniture catalog alone.
- Do not promote `seb_`, `img_`, or `subSeb_` as runtime asset selectors.
- Do not create the TypeScript/Vite scaffold until the scene/behavior candidate passes its review gate.

## Definition of done

Machine-readable scene/behavior candidates exist, parser/fixture tests pass, provenance is complete, unresolved semantics are recorded in the review queue, and state/TODO match the actual files.
