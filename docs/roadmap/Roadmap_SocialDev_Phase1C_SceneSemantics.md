# Social Dev Phase 1C — Scene-semantics review

> Status: historical review package; formally superseded and closed by `Roadmap_SocialDev_Phase1D_NativeSemantics.md` and the Pre-runtime Closure Sweep. The active replacement matrix is `knowledge/fixtures/accepted/phase1_supersession.json`.

Start date: 2026-08-13

## Goal

Close the first semantic review of the display slice so it is clear which parts can already build the canonical scene contract and which still require additional C#/assembly evidence. Focus on `RoomData(0)`, `ObjChip`, `Room`, `FurnitureData.passMap_`, and `Astar/Node`.

This phase is evidence work only. It does not create a Vite/TypeScript runtime or execute decompiled C# in the browser.

## Scope

1. Freeze raw `objMap_`/`objDir_` for `RoomData(0)` with a histogram and cell provenance.
2. Compare the raw map-code domain with `ObjChip` source constants and pass native-confirmed assignments to Phase 1D for contract promotion.
3. Inspect the source boundaries of `Room.InitObjChips` and `Room.PlaceDoor`.
4. Extract the coordinate transform, node-grid construction, neighbor-topology candidate, and Manhattan cost.
5. Parse every `FurnitureData` row in both locales to inventory `passMap_` and select records for further review.
6. Summarize the promotion matrix and route-fixture gate; do not create a path while passability/goal semantics are incomplete.

## Evidence to use

- `data/RoomData.cs`, `data/FurnitureData.cs`
- `game/Room.cs`, `game/ObjChip.cs`, `game/MapChip.cs`
- `game.routeSearch/Astar.cs`, `game.routeSearch/Node.cs`
- Loader evidence and English/Japanese furniture tables from Phase 1/1B

## Outputs

- `knowledge/fixtures/accepted/scene_semantics_review.json`
- `knowledge/fixtures/accepted/scene_semantics_validation.json`
- `docs/reports/social-dev_phase1c_scene_semantics_report.md`
- `tools/social-dev/build_scene_semantics_review.py`
- `tools/social-dev/test_scene_semantics_review.py`

## Package statuses

- `source_observed`: the source directly shows the referenced structure/value.
- `bounded_candidate`: multiple evidence points agree, but a decompiler or assignment gap remains.
- `unknown`: the required meaning or mapping is not known.
- `blocked`: do not create runtime/route fixtures from this part of the data.

Phase 1C originally used `blocked` and retained 8-neighbor as a candidate because native method-body evidence was not available at that time. Do not use those values as the Phase 1D status.

Do not convert `bounded_candidate` or `unknown` into product semantics during this phase.

## Validation gates

- The room map/direction is a rectangular grid and every cell has raw provenance.
- The raw map domain is within the object-constant domain and its mapping is covered by the Phase 1D native contract.
- The door raw-code candidate has deterministic count and location; the door scan source references literal type `5`.
- Every selected FurnitureData row parses completely in both locales and the passMap profile has shape/provenance.
- Astar source shows node-grid construction, coordinate projection, and the passability hook; Manhattan cost is kept separate from the neighbor candidate.
- The route fixture remains `blocked_on_fixture_semantics` until passMap boolean normalization and the goal filter are closed.
- Package semantic status must be `pending_review`, and no catalog may be written under `runtime/social-dev/`.

## Definition of done

A machine-readable review package states what evidence can be promoted at each level, tests/validation pass, report/state/TODO reflect the current blockers, and the next work for the canonical scene contract is explicit.
