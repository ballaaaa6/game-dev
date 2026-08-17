# Social Dev Phase 0 — C# System Extraction & Rewrite Inventory

Status: **closed by the Pre-runtime Closure Sweep for display-slice-01**

The original candidate evidence retains its historical statuses for provenance.
The active closure authority is `knowledge/fixtures/accepted/semantic_review_closure.json`
and `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json`.

## Goal

Turn decompiled C# evidence into a system map ready for rewriting, without creating the web runtime or promoting data into `runtime/social-dev/`.

When Phase 0 is complete, we must be able to answer:

1. Which systems make the scene and characters feel alive?
2. Which systems are data sources, state owners, services, or presentation?
3. Which fields, constants, transitions, loaders, and asset selectors must be extracted from each system?
4. Which systems must be rewritten now, adapted, deferred, or cut?
5. Which relationships are `verified`, `raw_only`, `derived`, `unknown`, `conflict`, or `quarantine`?
6. Which data is ready to enter Phase 1 for canonical-contract creation?

This phase is analysis/evidence work only. It is not scene creation, Canvas work, or a Vite-app bootstrap.

## Scope and rules

### Data sources

- `knowledge/fixtures/accepted/csharp_update_inventory/` — type, field, and method catalogs;
- `knowledge/sources/csharp_raw_20260813/` — RAR extraction as the provenance anchor;
- `sources/raw/1_Click_CSharp_Code update/` — read-only source input;
- `knowledge/fixtures/accepted/data_schema_candidate.json` — registry/data candidate;
- `knowledge/fixtures/accepted/runtime_schema_candidate.json` — entity/lifecycle candidate;
- `knowledge/fixtures/accepted/load_contract_candidates.json` and `field_load_candidates.json` — loader/column candidates;
- asset-guide/APK/ZIP evidence only when checking selector relationships.

### Prohibited actions

- Do not modify `sources/raw/` or source/extraction roots.
- Do not execute decompiled C# as runtime or browser code.
- Do not copy `VGO_Core` or the legacy Office runtime back into the active tree.
- Do not recreate `Assembly-CSharp/`.
- Do not assign semantic names to numeric fields/states based only on guesses.
- Do not create a production schema from column positions alone.
- Do not create Vite/package/runtime code before the Phase 0 gate passes.

## Taxonomy

### Evidence status

| Status | Meaning | Runtime use |
|---|---|---:|
| `verified` | Declaration, consumer, and cross-source evidence agree | Allowed after contract passes |
| `raw_only` | Found in source but semantic meaning is not known | No |
| `derived` | Re-grouped or recalculated from multiple evidence sources | Requires review |
| `unknown` | Function or relationship cannot yet be explained | No |
| `conflict` | Evidence sources disagree | No |
| `quarantine` | Decompiler/loader/asset issue | No |

### Rewrite scope

| Scope | Meaning | Examples |
|---|---|---|
| `keep` | Required in the display/living core | `Room`, `Staff`, `ObjChip`, `Astar` |
| `adapt` | Use selected responsibilities; do not port the whole type | `Player`, `AppData`, `DataManager` |
| `defer` | Add later when a visible requirement exists | `Meeting`, `Avatar`, special event |
| `cut` | Gameplay/management not required for the scene | economy, shop, proposal, development battle |

Every inventory record must have `scope`, `status`, `reason`, `source_refs`, `consumer_refs`, and `confidence`.

## Required outputs

Phase 0 files belong to the evidence/report boundary, not executable runtime:

```text
knowledge/fixtures/accepted/csharp_system_inventory.json
knowledge/fixtures/accepted/csharp_dependency_graph.json
knowledge/fixtures/accepted/csharp_source_slice_manifest.json
knowledge/fixtures/accepted/csharp_semantic_review_queue.json
knowledge/fixtures/accepted/csharp_extraction_validation.json
docs/reports/social-dev_phase0_extraction_report.md
```

If new scripts are needed, keep them at:

```text
tools/social-dev/build_csharp_system_inventory.py
tools/social-dev/build_csharp_source_slice.py
tools/social-dev/test_csharp_system_inventory.py
```

`knowledge/fixtures/accepted/runtime/` does not accept Phase 0 files until the canonical-contract gate passes.

## Work package 0 — Freeze input and provenance

### Work

1. Read `AGENTS.md`, `PROJECT_STATE.md`, `TODO.md`, and this roadmap.
2. Inspect source roots read-only and verify that `VGO_Core` has no active dependency.
3. Verify hashes/fingerprints for the catalogs and source inventories in use.
4. Record the input manifest with generated-at and tool version.
5. Use the RAR extraction as the baseline when the C# update is marker cleanup or ambiguous.

### Gate

If the input fingerprint changes during the work, stop and create a new manifest. Do not merge evidence across inputs without recording the difference.

## Work package 1 — Build the system inventory

Read `type_catalog.json`, `field_catalog.json`, and `method_catalog.json` and combine them into one record per type without going beyond structural facts:

- namespace and source file;
- type kind, base type, and nested/outer relationship;
- field/method counts;
- field names/types/static/constant markers and lines;
- method names/visibility/return types and lines;
- lifecycle candidates such as `Init`, `Load`, `NewGame`, `Update`, `Draw`, `Serialize`, and `Deserialize`;
- decompiler warnings/IL markers present in the source.

### Systems required in the first inventory

| Group | Primary types | Required knowledge |
|---|---|---|
| Data | `DataManager`, data classes | registry, loader, record shape |
| Bootstrap | `Main`, `AppData`, `Player` | lifecycle, ownership, clock/tick |
| Scene | `Room`, `RoomData`, `MapChip`, `Camera` | grid, map, camera, draw/update order |
| Object | `ObjChip`, `FurnitureData` | placement, footprint, passability, use state |
| Actor | `Staff`, `StaffData`, `JobData`, `SkillData` | identity, state, movement, work, talk, animation |
| Route | `Astar`, `Node` | node grid, neighbors, goal flags, route output |
| Event/text | `DelayEvent`, `EventData`, `AvatarEventData`, `TalkData`, `EventMessageData`, `TodayEventData` | visible event, delay, speaker, text |
| Optional | `Avatar`, `Meeting`, `ScheduleData` | feature-specific visible behavior |

`csharp_system_inventory.json` must separate `structural_facts` from `semantic_claims` so names we invent do not become source facts.

## Work package 2 — Owner/consumer and dependency graph

Create directed, evidence-backed edges; do not build a graph from class names alone:

- `DataManager → data records` from typed arrays and loaders;
- `Main → AppData/Canvas/FormManager` from lifecycle/presentation;
- `AppData/Player → Room/Staff/Astar` from ownership/access;
- `Room → MapChip/ObjChip/Staff/Astar` from fields, init, update, and draw;
- `Staff → Room/ObjChip/Astar/StaffData` from movement/work/talk;
- `ObjChip → FurnitureData/Room/Staff` from placement, occupancy, and actions;
- `EventData/AvatarEventData → DelayEvent/TalkData/Form` from event methods;
- `Camera → Room/viewport` from target/position/clamp methods.

Every edge must have `from`, `to`, `relation`, `status`, `confidence`, `source_refs`, and `review_note`.

Do not use `verified` for an edge supported only by a method name without consumer/trace evidence.

## Work package 3 — Split keep/adapt/defer/cut

### Keep — rewrite in core

- `DataCatalog` from extracted registry/data;
- `Room`/grid/map/camera contract;
- `ObjChip`/occupancy/passability/interaction;
- visible `Staff` state/movement/work/talk/animation;
- `Astar` route/collision;
- clock/tick and the event queue that drives visible output.

### Adapt — separate responsibilities

- `DataManager` → `DataCatalog`, without the original singleton/loader;
- `AppData` → only the required parts of `WorldContext`, `PresentationEffects`, and `EventQueue`;
- `Player` → `Clock`, world ownership, room/staff lookup, and visible real-time update;
- `Main` → browser-host lifecycle (`start`, `tick`, `render`, `dispose`).

### Defer or cut

- avatar profile/event, meeting sequences, and special events outside the first slice;
- economy/money/coin/shop, proposal/publish/progression/ranking;
- recruitment/management UI and development battle/enemy;
- save/backend/auth/multiplayer/LLM.

Record the reason for every cut; do not delete evidence from source/evidence.

## Work package 4 — Source-slice manifest

Do not read every method equally. Create slices by system and by methods that drive the output.

### Data slice

`DataManager.Load` and `Load` for `RoomData`, `FurnitureData`, `StaffData`, `JobData`, `SkillData`, `TalkData`, `EventData`, `AvatarEventData`, `ScheduleData`, and `TodayEventData`.

### Bootstrap/clock slice

`Main.OnCreate`, `OnUpdate`, `OnDraw`, `OnSuspend`, `OnDestroy`; `AppData.Init`, `InitGameData`, `NewGame`, `LoadGame`, `ExeEvent`, `UpdatePopup`, `UpdateAnnounce`; `Player.NewGame`, `UpdateCurrentTime`, `RealTimeProcess`, `UpdateRealTimeData`, `Update`, `Frame`.

### Scene slice

`Room.InitMapChips`, `InitObjChips`, `InitStaffs`, `Update`, `UpdateFukidashi`, `UpdatePlanning`, `Draw`, `PlaceObj`, `PlaceDesk`, `AddStaff`, `RemoveStaff`, and coordinate helpers.

### Object slice

`ObjChip.Init`, `Update`, `IsPassable`, `GetStandingPositions`, `ReserveUse`, `StartAction`, `OnUseComplate`, `AddStaff`, `RemoveStaff`, `Draw`, and placement/serialization boundaries.

### Actor slice

State/movement constants; `Staff.Init`, `Update`, `UpdateMove`, `UpdateWork`, `UpdateMeeting`, `SearchRoute`, `Move`, `OnArriveNextNode`, `OnArriveGoal`, `ChangeState`, talk/invite, typing/fukidashi, animation, and draw methods.

### Route slice

`Astar.AddNodeArray`, `ConnectNeighbors`, `SearchRoute`, `GetNode`, `RemoveNodeArray`; `Node` position/index/cost/neighbor facts.

### Event/text slice

`DelayEvent` fields/serialization; `EventData.Load`, `NewGame`, `ExeAutoEvent`, `StartEvent`, `ExeEvent`; equivalent `AvatarEventData` methods; `TalkData.Load`; text normalization and speaker fields.

Every source-slice record must have `purpose`, `inputs`, `outputs`, `called_types`, `source_refs`, `artifact_risk`, and `required_for_slice`.

## Work package 5 — Extract facts for the rewrite

### Data facts

- registry name and element type;
- source table/file/language;
- row/column count;
- reader sequence from the loader;
- matched field declarations;
- default/new-game initialization;
- loader mismatch/missing status.

### Scene/object facts

- room/floor identity, width/height/grid/index transform;
- map/floor/wall/door selectors;
- object placement/direction/footprint/passability;
- staff spawn/desk/equipment relationship;
- camera base/target/clamp/draw order;
- occupancy/use/reservation lifecycle.

### Actor facts

- state constants and movement modes found in the source;
- state entry/exit and visible output;
- route request/arrival callback;
- position/facing/animation frame;
- work/equipment/talk/typing/bubble timer;
- room/object/staff relationship.

Retain each numeric value with the label declared by the source. Do not rush to create a new semantic name.

### Route/event/text facts

- cell/node coordinates, passability, neighbor policy, and goal flags;
- route success/failure and route consumption during actor movement;
- event ID/opcode/term/delay/character parameter;
- speaker/character index/text key and newline/tab normalization;
- visible form/bubble/notification output.

## Work package 6 — Review and triangulation

Review claims in this evidence order:

1. declaration/field/method catalog;
2. RAR raw source;
3. C# update after marker-only normalization;
4. consumer/access edge;
5. recovered C/assembly trace;
6. data table/loader/language;
7. asset-guide/APK/ZIP selector relationship.

If higher-level evidence conflicts with a decompiled body, mark the body `quarantine` and retain the bounded, repeatable fact instead of guessing a body repair.

## Work package 7 — Validation and report

### Automated checks

- every type has a source reference and counts match catalog input;
- every dependency edge has all required fields;
- every core system has scope and owner;
- every source slice resolves to a real file/line;
- runtime has no active reference to `VGO_Core`, legacy runtime, or raw C#;
- input hashes in outputs match the manifest;
- JSON schema and duplicate-ID checks pass.

### Human review

- `keep/adapt/defer/cut` matches the display/living target;
- no scaffold field leaked into the package;
- `Player/AppData` is split by responsibility rather than copied as whole objects;
- unverified column mappings are not called semantic;
- the first slice has enough data/behavior for `idle → move → work → talk`.

### Report

`docs/reports/social-dev_phase0_extraction_report.md` must summarize input/type/field/method counts, the system matrix, dependency graph, source slices, status claims, blockers, and the exact next work for Phase 1.

## Definition of done

Phase 0 passes when:

- the system inventory, dependency graph, source-slice manifest, and review queue exist;
- every core-system group has owner/consumer/source references;
- `keep/adapt/defer/cut` is complete for relevant types;
- data, scene, object, actor, route, and event/text source slices are complete;
- uncertain claims have explicit status rather than being hidden by defaults;
- the validation script passes and the report matches the actual files;
- source roots are unchanged;
- `runtime/social-dev/` contains no raw C# or unapproved catalog;
- a Phase 1 task list can begin canonical-contract creation immediately.

## After Phase 0

1. Extract `RoomData/FurnitureData/StaffData/JobData/SkillData` for the first slice.
2. Build `SceneCatalog`, `ObjectCatalog`, and `ActorCatalog`.
3. Create route/occupancy/state fixtures.
4. Extract `TalkData/EventData/DelayEvent` for the visible loop only.
5. Promote reviewed contracts into `knowledge/fixtures/accepted/runtime/`.
6. Only then scaffold the Vite/TypeScript runtime.
