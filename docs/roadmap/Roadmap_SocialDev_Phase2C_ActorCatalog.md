# Social Dev Phase 2C — Canonical `ActorCatalog`

Status: **complete**

Phase 2C follows the approved `SceneCatalog` and `ObjectCatalog` contracts by projecting the first visible staff slice into a canonical, provenance-backed actor catalog and closing the display/runtime readiness boundary. This phase creates static actor definitions, a deterministic source-bounded spawn fixture, camera/coordinate contracts, and bounded living-scene behavior/tick contracts. It does not create mutable runtime state, execute decompiled C#, promote binary assets, or implement the renderer.

## Goal and scope

The phase must close the following questions for `display-slice-01`:

- Which `StaffData` records are the first actor set, and what stable IDs do they have?
- Do English and Japanese rows identify the same five source records?
- Which human image selector belongs to each actor, and does it resolve through the indexed asset package?
- Which bounded animation selectors are closed for wait and typing states?
- Which `JobData` and `SkillData` records are referenced by the selected staff rows?
- Which state, move, route, talk, and skill-effect facts can be referenced without guessing product semantics?
- Which initial spawn/placement values can be closed from the verified door and readable `Room.AddStaff` assignments, and which remain deferred?
- What camera-offset, coordinate-transform, fixed-tick, and behavior contracts must be complete before the Vite/TypeScript core starts?
- Can the contract be rebuilt with stable content hashes without importing or executing C# or native code?

The initial target is `StaffData(0–4)`. A record may be retained as evidence without promotion when a required selector or relation gate fails. No record is promoted by array position alone.

## Authority and preconditions

The builder must fail before writing output when any required authority is invalid:

1. `SceneCatalog` is `pass` / `approved_for_runtime_contract`.
2. `ObjectCatalog` is `pass` / `approved_for_runtime_contract`.
3. `asset_selector_contract.json` is `pass` with no unresolved selectors.
4. `staff_semantics_contract.json` is `pass`.
5. English/Japanese `StaffData`, `JobData`, and `SkillData` rows parse successfully through the loader-aware evidence parser.
6. Source-slice and asset-index hashes match the current read-only files.

`staff_behavior_candidate.json` remains evidence-only input. Its pending review labels must not be silently promoted. The approved `staff_semantics_contract.json` is the authority for bounded state, route, talk, typing, wait, and selected skill-effect facts.

## Promoted static records

The catalog uses stable IDs of the form `actor:staff:<source_id>`:

| Stable ID | Source | Image selector | Job | Skill |
|---|---|---:|---:|---:|
| `actor:staff:0` | `StaffData(0)` — `10s Female` | `86` | `4` | `1` |
| `actor:staff:1` | `StaffData(1)` — `10s Male` | `87` | `4` | `1` |
| `actor:staff:2` | `StaffData(2)` — `20s Female` | `88` | `4` | `1` |
| `actor:staff:3` | `StaffData(3)` — `20s Male` | `89` | `4` | `1` |
| `actor:staff:4` | `StaffData(4)` — `30s Female` | `90` | `4` | `1` |

The catalog promotes source identity, locale values, image selector identity, job/skill references, and bounded animation/behavior profile references. Mutable fields such as `x_`, `y_`, `state_`, `route_`, timers, and flags are not actor definitions and remain outside this catalog.

## Contract shape

```text
ActorCatalog
├─ catalog_id = display-slice-01
├─ scene_ref = room:0
├─ actors[]
│  ├─ source_identity
│  ├─ locale_names
│  ├─ source_fields
│  ├─ portrait_selector
│  ├─ job_ref
│  ├─ skill_ref
│  ├─ animation_profile_ref
│  ├─ behavior_profile_ref
│  ├─ spawn_boundary
│  └─ provenance_ref
├─ job_records[]
├─ skill_records[]
├─ behavior_profiles[]
├─ provenance
└─ limits
```

Every promoted value carries a controlled status: `verified`, `derived`, `raw_only`, `deferred`, or `quarantine`. Numeric source labels remain source labels; they are not renamed into broader product semantics.

## Spawn boundary

The static catalog keeps mutable actor state outside its record shape. Phase 2C nevertheless closes the display-slice spawn boundary with a separate source-bounded fixture: at least three actors enter through the verified `room:0` door cell and use the readable `Room.AddStaff` position/field assignments. The fixture does not invent free cells, fan actors out, or promote the damaged desk-selection body. The camera/coordinate and behavior/tick contracts record the remaining explicit runtime boundary before the core starts.

## Work packages

### WP0 — State and scope lock

- Reconcile the stale Phase 2A roadmap status with the completed SceneCatalog artifacts.
- Lock `room:0`, FurnitureData `0,1,2,5`, StaffData `0–4`, route fixture, and the `idle → move → work/talk` acceptance trace.
- Keep the display-slice scope separate from runtime readiness; spawn, camera, coordinate transforms, and frame composition remain explicit boundaries.

### WP1 — Loader-aware actor projection

- Parse English/Japanese `StaffData(0–4)` rows from the current tables.
- Parse `JobData(4)` and `SkillData(1)` in both locales.
- Cross-check `StaffData.cs`, `JobData.cs`, `SkillData.cs`, and `StringArrayStream.cs`.
- Use the approved staff semantics contract for the `skill_ → skillId_` relationship.

### WP2 — Human selector and animation projection

- Resolve `img_ 86–90` through `human/img.inf` and the asset index.
- Resolve the four direction pairs for wait `10–13` and typing `23–26` through `human/seb.inf`.
- Preserve the typing start/end frame and interval rules.
- Keep frame composition, crop, scale, alpha, and binary promotion outside this phase.

### WP3 — Bounded behavior profile

- Project source constants with `source_label_only` semantics.
- Project the three route flag mappings.
- Project the four closed transition/timing records and the selected skill-effect contract.
- Reference the profile from each actor without copying mutable live state into the catalog.

### WP4 — Deterministic artifact build

Create:

```text
tools/social-dev/build_actor_catalog.py
tools/social-dev/test_actor_catalog.py
knowledge/fixtures/accepted/actor_catalog_fixture.json
knowledge/fixtures/accepted/actor_catalog_validation.json
knowledge/fixtures/accepted/runtime/actor_catalog_contract.json
```

The builder must reject stale upstream contracts, locale drift, selector drift, duplicate IDs, missing provenance, invalid statuses, unresolved promoted assets, and content-hash instability.

### WP5 — Regression and handoff

Run Phase 1D, SceneCatalog, native-semantics, semantics-review, ObjectCatalog, ActorCatalog, and Phase 2C readiness tests. Only after all gates pass may the roadmap and `PROJECT_STATE.md` mark Phase 2C complete.

### WP6 — Display/runtime readiness closure

- Build `actor_spawn_fixture.json` and `actor_spawn_contract.json` for at least three stable actors.
- Build `camera_coordinate_contract.json` from the verified grid, screen-coordinate, standing-position, and draw-offset boundaries.
- Build `actor_behavior_contract.json` and `tick_order_contract.json` from the approved bounded transitions and fixed frame boundary.
- Keep `runtime/social-dev/core/`, renderer code, and Vite scaffolding absent until this package passes.

## Acceptance gate

Phase 2C is complete when:

- the contract is `pass` / `approved_for_runtime_contract`;
- five actor records have stable IDs and complete locale provenance;
- all five image selectors resolve through the indexed asset package;
- wait and typing selector pairs match the approved semantics contract;
- JobData and SkillData relations are explicit and provenance-backed;
- behavior values are bounded and source-labelled, with no guessed product semantics;
- the deterministic spawn fixture contains at least three stable actors and uses the verified door plus source-bounded `Room.AddStaff` assignments;
- camera/coordinate, actor behavior, and fixed-tick contracts are `pass` / `approved_for_runtime_contract`;
- fixture, contract, and validation hashes are stable on rebuild;
- all upstream regression gates pass;
- no TypeScript runtime, renderer, or raw C# import is introduced before this gate.

Only after this gate should the project create the Vite/TypeScript deterministic core.
