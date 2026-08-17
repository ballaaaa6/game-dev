# Social Dev Display Runtime — Implementation Plan

## Current status — Phase 3A, Phase 3B, and Phase 3C strict evidence/runtime closure complete

The exact `chair_00` composition is approved. The validated OPT grammar is
`header + per-cell piece_count + 14-byte crop descriptors`; `chair_00` uses
cell pattern `[1,2,1]`, reconstructs to a 180×32 logical atlas, and requires no
borrowed or generated pixels. The display gate now has `14` approved entries,
`0` room-coordinate blockers, and `26` promoted source binaries. The strict
Phase 3C package closes native wall/door coordinates and sprite records plus
the native initial FurnitureData matrix. Selector-only `furniture:2` and
`furniture:5` remain explicit negatives, and baseline replacement still needs
comparison-policy approval.

This document is the destination runtime plan, not the first task. The preceding work is `Roadmap_SocialDev_CSharp_Rewrite.md`, which starts with C# system survey and data extraction into contracts.

## Goal

Reproduce the observable Social Dev experience:

- original scene, room layout, camera, draw order, and asset selectors;
- original characters and their visible animation/state;
- the original sense of life: tick, idle, work, movement, routing, talking, bubbles, and visible events;
- without rebuilding player-facing management gameplay that is not needed for display.

“Same as the game” is split into two testable targets:

1. **Visual fidelity** — scene composition, sprites, animation, camera, layers, and UI presentation.
2. **Observable behavior fidelity** — actor lifecycle, movement, route decisions, timers, interactions, and visible event transitions.

Economy, progression, recruitment screens, win/loss, backend, auth, multiplayer, and LLM are deferred unless they directly drive something visible in the scene.

## Non-negotiable boundaries

- Original C#/APK/asset inputs remain read-only evidence.
- Decompiled C# is never executed as the browser runtime.
- Every ported behavior needs a source reference and a deterministic fixture.
- `unknown`, `raw_only`, `derived`, and `conflict` values remain explicit; they are not silently renamed.
- An asset enters runtime only after selector, identity, and source-relationship validation passes.
- The deleted GameDev/Office runtime is not imported into the Social Dev state owner.

## Runtime shape

Use a small TypeScript/ES-module runtime with no game-framework dependency initially:

```text
runtime/social-dev/
  evidence/       machine-readable contracts and provenance
  catalog/        promoted data and asset manifests
  core/           canonical state, fixed tick, transitions, events
  scene/          room grid, coordinate transform, camera, draw order
  actors/         Staff/Player visible state and behavior adapters
  renderer/       Canvas scene renderer
  ui/             DOM panels, bubbles, and menus
  tests/          contract, deterministic, and visual smoke tests
```

The core owns state. The renderer reads a snapshot and never mutates simulation state. Canvas handles the pixel scene; DOM handles panels and text overlays.

## Phases

### Phase 0 — C# system extraction

- Group `DataManager`, `Room`, `ObjChip`, `Staff`, `Astar`, the `Player/AppData` subset, and visible event/text.
- Separate `keep`, `adapt`, `defer`, and `cut` with dependency/owner/consumer evidence.
- Record decompiler uncertainty as evidence status; do not port broken bodies.

### Phase 1 — Data extraction and scope lock

- Write the display contract and explicit gameplay cut list.
- Select one known room/floor, a small character set, and a small furniture set.
- Define screenshot and behavior acceptance criteria before implementing.
- Extract the data/loader/selector/transition subset required by that slice.

### Phase 2 — Canonical evidence slice

- Trace only the first slice: `DataManager`, `Room`, `Staff`, `ObjChip`, `Camera`, route search, and bounded lifecycle code.
- Resolve which fields control identity, position, facing, animation, occupancy, timers, and visible events.
- Keep data-loader mismatches in the review queue; do not generate production models from column position alone.
- Promote only versioned contracts with provenance and deterministic fixtures.

### Phase 3 — Scene and asset contract

- Confirm room grid, floor/wall/door selectors, object map, object direction, coordinate transform, camera, and draw order.
- Validate selectors against the assembly guide, ZIP index, and APK metadata.
- Use placeholders only for blocked compositions; promote an asset only through the selector/hash/SEB frame gate.
- Execute the remaining first-slice closure as three sequential rounds: Phase 3A asset composition, Phase 3B native room placement, and Phase 3C integrated visual fidelity.

#### Phase 3A — Asset composition closure

The implementation-ready Phase 3A work breakdown, recovery/quarantine decision
flow, evidence matrix, and regression checklist are recorded in
`docs/roadmap/Roadmap_SocialDev_Phase3A_AssetComposition.md`.

Objective: close the remaining `furniture:2` composition without inventing OPT bytes or silently treating a damaged payload as complete.

Scope:

- Reconcile `chair_00.opt` against the read-only asset ZIP, assembly guide index, APK metadata, and the existing selector/SEB relationship.
- Extend the OPT parser/reconstructor only when a field or payload rule is supported by source evidence and an exact pixel fixture.
- Rebuild the `furniture:2` main/sub composition, including source rectangles, logical atlas dimensions, selector identity, and provenance.
- Validate the apparent `chair_00` tail as the second crop descriptor in the variable-piece cell grammar; never pad, infer, or rewrite the source payload.

Deliverables:

- `opt_codec.py` and focused regression fixtures updated only for evidence-backed behavior;
- display gate entry and runtime manifest updated if every `furniture:2` record passes;
- deterministic asset promotion report, state update, and a clear source-limitation record if closure is impossible.

Acceptance criteria:

1. `chair_00.opt` has a complete, source-supported payload or a documented, reproducible source limitation; no speculative bytes are introduced.
2. Every promoted `furniture:2` record has a passing source rectangle and complete selector/PNG/OPT/SEB provenance.
3. The gate and manifest rebuild deterministically, with exact hashes and no unapproved asset promotion.
4. OPT, display-gate, TypeScript, and runtime regression checks remain green.

Exit boundary: Phase 3A is complete only when `furniture:2` is approved or its unrecoverable source limitation is formally recorded and the runtime keeps it gated.

#### Phase 3B — Native room-placement closure

Objective: close the native evidence needed to place floor, wall, door, and approved furniture compositions into `room:0`.

Scope:

- Resolve the room floor/wall/door selector chain from `chip/img.inf`, APK metadata, assembly-guide evidence, and native `Room`/`ObjChip` consumers; retain unresolved IDs as explicit evidence when no authoritative filename exists.
- Prove the room-to-screen coordinate transform, object anchor/origin, direction, footprint, door cell `(8,4)`, and draw/depth ordering for the bounded `10×10` room.
- Produce a native placement contract and deterministic fixture for the existing `furniture:0`, `furniture:1`, and `furniture:5` bindings, with `furniture:2` included only if Phase 3A passes.
- Keep the runtime asset boundary separate from evidence: derived previews may support comparison but are not promoted as original runtime assets.

Deliverables:

- native room-placement contract and validation fixture under the approved evidence boundary;
- source-backed floor/wall/door composition records with selector, coordinate, and layer provenance;
- scene-projection inputs ready for renderer integration, without changing the historical screenshot baseline.

Acceptance criteria:

1. The room floor/wall/door identities are resolved from evidence or each unresolved slot has an explicit, testable reason.
2. Placement, coordinate, footprint, camera, and draw-order assertions match the native evidence for `room:0`.
3. Door placement remains consistent with raw type `5` at `(8,4)` and the existing closed route/coordinate contracts.
4. The placement contract and all upstream catalog/asset gates pass without importing C#, archives, or unapproved binaries into the browser runtime.

Exit boundary: Phase 3B is complete when the renderer has a deterministic, evidence-backed room-placement contract for the bounded scene.

#### Phase 3C — Integrated visual fidelity closure

Objective: place the proven compositions into the Canvas scene and close the first-slice visual/browser gate.

Scope:

- Bind the Phase 3B room placement contract and strict native-closure contract to the Canvas renderer; draw native wall/door source records at the proven cells and retain the explicit floor fallback.
- Encode the native initial FurnitureData scan: Wooden Desk (`furniture:3`) on the first three empty type-2 cells, then `furniture:12`, `furniture:26`, and `furniture:56` on the first three empty type-1 cells.
- Keep selector-only `furniture:2`/`furniture:5` outside the room projection unless a later explicit user-placement contract supplies a cell.
- Verify selector-backed frame selection, camera/coordinate projection, actor occlusion/depth, and the existing living-state event trace together in the browser.
- Compare the new rendered scene with the historical placeholder baseline; persist a replacement baseline only after the comparison policy is recorded and accepted.

Deliverables:

- integrated scene renderer and display manifest updates;
- deterministic screenshot/behavior evidence for the completed `display-slice-01` room;
- final Phase 3 closure report and synchronized state/TODO entries.

Acceptance criteria:

1. Native wall/door compositions and native initial furniture bindings are visible at evidence-backed room positions with no guessed placement.
2. The browser reaches frame `136`, preserves the expected event sequence and digest contract, and reports zero console errors.
3. Typecheck, unit tests, production build, asset gates, and browser smoke checks pass together.
4. The historical placeholder baseline is retained unless a documented comparison decision authorizes a new persisted baseline.

Exit boundary: strict evidence/runtime closure completes the bounded `display-slice-01`; comparison-policy approval is the remaining external decision before any baseline replacement or expansion.

### Phase 4 — Living-logic core

- Implement a deterministic fixed-tick state owner.
- Port actor spawn, idle/work state, movement, route, arrival, facing, animation, interaction, dialogue bubble, and visible-event timing.
- Keep formulas as pure functions where possible and test each against evidence fixtures.

### Phase 5 — Presentation

- Render the scene with the original visual coordinate system and layering.
- Add the minimum UI needed to feel like the game: camera, character selection, status/bubble overlays, and scene panels.
- Do not let UI code become a second state owner.

### Phase 6 — Fidelity gate

- Deterministic snapshot/digest for the same seed and tick sequence.
- Golden scene screenshots for the first room and actor fixture.
- No console errors, broken selectors, or unresolved promoted fields.
- Behavior trace shows the expected idle → move → work/talk transitions.

### Phase 7 — Expansion

- Add more rooms, characters, objects, events, and language data one vertical slice at a time.
- Add player-facing gameplay only if later required; it is not part of the first runtime.

## First vertical slice

The first implementation should contain one room, one camera, three to five original characters, two or three furniture types, one valid route, and one complete living loop such as idle → walk → work → talk. It should already look alive, but it should not yet contain economy or progression systems.

## Current implementation checkpoint

The first `display-slice-01` runtime is implemented and verified. The display asset gate is now `pass`: `14` entries are approved, `0` remain blocked, and `26` exact source binaries are promoted. The OPT parser/reconstructor closes the `door_03 → door_02`, `desk_00`, `chair_00`, `chair_02`, and `chair_04` logical compositions with pixel matches against the supplied comparison images and full-pack validation. The strict native package closes wall/door predicates, exact cells, source sprite records, the null-FurnitureData door binding, and the native initial FurnitureData matrix. `furniture:2` and `furniture:5` remain explicit selector-only negatives. The historical placeholder screenshot remains unchanged until a new-baseline comparison policy is agreed; the remaining work is the approval decision.

## Next concrete work

1. **Phase 3C comparison-policy approval:** decide whether the strict frame-136 candidate may replace the historical baseline; preserve the historical file until the decision is recorded.
3. Expand beyond `display-slice-01` only after Phase 3C acceptance criteria pass.
