# Social Dev Phase 0 Extraction Report

## Status

The original Phase 0 extraction package passed its structural gate. Its
historical candidate statuses are preserved, but the semantic review is now
closed for the display-slice runtime boundary by the Pre-runtime Closure Sweep.
The active closure authority is
`knowledge/fixtures/accepted/semantic_review_closure.json`; no Vite/TypeScript
runtime was created during this sweep.

Artifact creation dates are available from `generated_at_utc` in the evidence files.

## Created outputs

- `knowledge/fixtures/accepted/csharp_system_inventory.json`
- `knowledge/fixtures/accepted/csharp_dependency_graph.json`
- `knowledge/fixtures/accepted/csharp_source_slice_manifest.json`
- `knowledge/fixtures/accepted/csharp_semantic_review_queue.json`
- `knowledge/fixtures/accepted/csharp_extraction_validation.json`
- Generator: `tools/social-dev/build_csharp_system_extraction.py`
- Repeatable test: `tools/social-dev/test_csharp_system_extraction.py`

## Structural boundary

| Item | Count |
|---|---:|
| C# types | 82 |
| fields | 3,430 |
| methods | 1,685 |
| DataManager registry | 43 |
| data types | 44 |
| runtime entity candidates | 14 |
| extracted system groups | 11 |
| dependency edges | 14 |
| source slices | 7 |
| review items | 6 |

The type rollup is `keep=19`, `adapt=4`, `defer=49`, `cut=10`. `defer` means not in the first display slice; it does not mean the system is absent from the game.

## System groups

| System | Scope | Phase | Types | Used in first slice |
|---|---|---|---:|---:|
| data registry | adapt | P0 | 44 | yes |
| bootstrap/world/clock | adapt | P0 | 3 | yes |
| scene/room | keep | P0 | 4 | yes |
| object/occupancy | keep | P0 | 2 | yes |
| actor/living | keep | P0 | 4 | yes |
| route service | keep | P0 | 2 | yes |
| visible event/text | keep | P1 | 7 | yes |
| schedule/interaction | defer | P1 | 1 | no |
| avatar | defer | P2 | 1 | no |
| meeting | defer | P2 | 1 | no |
| management/gameplay | cut | P2 | 10 | no |

The grouping is a derived scope decision; source-fact semantic status remains `unknown` until bounded review passes.

## Source slices ready for follow-up

1. `data_loading` — DataManager and first-slice data loaders;
2. `bootstrap_clock` — Main/AppData/Player lifecycle and clock boundary;
3. `scene_room` — room construction, update order, map/object/staff ownership;
4. `object_occupancy` — object placement, passability, reservation, and use;
5. `actor_living` — Staff state, movement, work, talk, and animation;
6. `route_service` — Astar/Node grid, neighbors, goal flags, and route;
7. `visible_event_text` — delay, script, talk, text, and visible output.

Every slice has complete references to the type/method/field catalogs, and validation confirms no type/method/field/constant is missing.

## Historical review queue and current closure

- The six historical items are mapped to final statuses in
  `knowledge/fixtures/accepted/semantic_review_closure.json`.
- Selected loader mappings are verified; non-slice missing/count-mismatch rows
  are explicit deferred exceptions in `load_contract_closure.json`.
- Decompiler bodies remain quarantined and are not runtime implementations.
- Player/AppData responsibilities are closed by `knowledge/fixtures/accepted/runtime/entity_contract.json`.
- Display-slice selectors, state boundary, and fixture scope are closed by the
  Phase 1D and Phase 2 contracts.

Validation status `pass` in this historical artifact still describes the
original structural gate. Semantic closure is reported by the active
pre-runtime closure contract.

## Definition of done already passed

- machine-readable system inventory, dependency graph, source-slice manifest, and review queue exist;
- counts match the current C# update catalog `82/3,430/1,685`;
- system IDs and slice IDs are unique;
- every source slice resolves to a real file/line;
- every dependency edge has source references and a review note;
- artifacts record the input hash and do not write into runtime;
- generator and repeatable test pass.

## Active closure artifacts

- `knowledge/fixtures/accepted/load_contract_closure.json`
- `knowledge/fixtures/accepted/semantic_review_closure.json`
- `knowledge/fixtures/accepted/runtime/data_contract.json`
- `knowledge/fixtures/accepted/runtime/entity_contract.json`
- `knowledge/fixtures/accepted/runtime/save_contract.json`
- `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json`
- Asset-selector promotion is not verified.
- The complete tick order/state-transition set is not verified.
- There is no Vite/TypeScript package or browser code.

## Next work — Phase 1

1. Select a concrete first slice: one room, 3–5 staff, and 2–3 object types.
2. Resolve loader/field review only for `RoomData`, `FurnitureData`, `StaffData`, `JobData`, and `SkillData`.
3. Create `SceneCatalog`, `ObjectCatalog`, and `ActorCatalog` as candidate contracts.
4. Create route/occupancy/state fixtures for `idle → move → work → talk`.
5. Extract Talk/Event/Delay for the visible loop only.
6. Create the Vite/TypeScript scaffold only after the contract gate passes.
