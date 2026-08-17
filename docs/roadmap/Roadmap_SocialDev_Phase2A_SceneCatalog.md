# Social Dev Phase 2A — Canonical `SceneCatalog`

Status: **complete**

Phase 2A closes only the canonical scene contract and deterministic evidence fixture for `RoomData(0)` so that it can provide a repeatable input to the next `ObjectCatalog` step. It does not create a renderer, camera runtime, runtime behavior, `ObjectCatalog`, `ActorCatalog`, or TypeScript runtime core.

## Goal and scope

### Goal

Create the first `SceneCatalog` that answers these questions completely and can be traced back to real evidence:

- Is this scene `RoomData(0)`, and what locale names can be read?
- What is the grid size, and how does indexing use `x + y * width`?
- What are the room's `objMap` and `objDir` values, without assigning new meaning to raw map codes?
- Where is the door, which raw/type code does it use, and how does the native path install the door?
- What footprint and `IsPassable` result does the type-4 object used as the passability anchor have?
- What path and filter probes does the repeatable route fixture contain?
- Which source/evidence hash and provenance status does every promoted value have?

### Out of scope

- Selecting `FurnitureData` for every cell or creating `ObjectCatalog`.
- Promoting floor/wall/door asset selectors as visual runtime assets.
- Camera/draw order/coordinate transforms that remain candidates.
- Actor spawn, living state, animation, tick, event, or renderer.
- Executing decompiled C# or native code.

## Authority

The builder must read and verify the status of these evidence packages before creating the package:

1. `scene_data_candidate.json` — `RoomData(0)` row, `objMap`, `objDir`, scalar-field projection, and source-slice references.
2. `scene_native_semantics.json` — native assignment, door, footprint/placement, and A* neighbor/filter claims.
3. `phase1d_passmap_fixture.json` — type-4 `FurnitureData(0)` binding, 3×3 footprint, and passability normalization.
4. `phase1d_route_fixture.json` — real route, goal filter, and negative probes.
5. `phase1d_closure.json` and `phase1d_closure_validation.json` — the Phase 1D entry gate must be `pass` / `closed_for_phase2_entry`.
6. Referenced source/table/APK files in provenance — hashes must match the current files every time.

Native/C# evidence is contract input only, not an executable runtime dependency.

## Required outputs

```text
docs/roadmap/Roadmap_SocialDev_Phase2A_SceneCatalog.md
docs/reports/social-dev_phase2a_scene_catalog_report.md
knowledge/fixtures/accepted/scene_catalog_fixture.json
knowledge/fixtures/accepted/scene_catalog_validation.json
knowledge/fixtures/accepted/runtime/scene_catalog_contract.json
tools/social-dev/build_scene_catalog.py
tools/social-dev/test_scene_catalog.py
```

`knowledge/fixtures/accepted/` stores fixtures/validation generated from evidence. `knowledge/fixtures/accepted/runtime/` stores only promoted contracts.

## First contract

`knowledge/fixtures/accepted/runtime/scene_catalog_contract.json` uses schema `social-dev-scene-catalog-v1` and contains one record in `scenes`:

```text
SceneCatalog
├─ catalog_id = display-slice-01
├─ scenes[0]
│  ├─ id = room:0
│  ├─ name = { English: "Floor A", Japanese: "フロアA" }
│  ├─ source_identity = RoomData / id_ 0
│  ├─ grid
│  │  ├─ width/height = 10/10
│  │  ├─ objMap[10][10]
│  │  ├─ objDir[10][10]
│  │  └─ flat_index = x + y * width
│  ├─ door
│  │  ├─ type = 5
│  │  ├─ cell = (8, 4)
│  │  └─ installed_flag = 1
│  ├─ type4_fixture
│  │  ├─ anchor = (4, 2), raw_map_value = 4
│  │  ├─ FurnitureData id = 0, type = 4
│  │  ├─ footprint = nine offsets/cells, parent center = (0, 0)
│  │  └─ passability = native 3×3 window + verified matrix/probes
│  └─ route_fixtures[0]
│     ├─ start = (8, 4), goal = (6, 4)
│     ├─ path = (8,4) → (7,4) → (6,4)
│     ├─ 4-neighbor policy
│     └─ occupied/type-4/type-6 negative probes
└─ provenance
   ├─ input_manifest with current hashes
   ├─ source_refs and evidence_refs
   └─ limits / deferred contracts
```

### Field statuses

- `verified`: may be promoted into the canonical SceneCatalog because source and cross-evidence are closed.
- `derived`: calculated from verified values, such as `room:0`, footprint cell coordinates, and route step count; the formula/evidence must be recorded.
- `raw_only`: retained for provenance but not interpreted further by runtime, such as scalar image IDs while the selector contract remains open.
- `deferred`: not included in this catalog version, such as camera transforms and full object-to-furniture placement.

## Closed-loop engineering process

### Loop 1 — Source lock

- Check Phase 1D closure status.
- Parse the English/Japanese `room.txt` row `id=0` from the real files.
- Check the `RoomData.Load` reader/field sequence against the actual source.
- Check source/APK/evidence hashes and stop immediately if the input drifts.

### Loop 2 — Contract projection

- Create a stable canonical ID from type + source ID (`room:0`), not from array position alone.
- Project `name`, `objMap`, `objDir`, dimensions, and the raw-value histogram.
- Project door/type-4/route data from the authoritative Phase 1D fixtures.
- Attach provenance at record/fixture level and retain evidence references as relative paths.

### Loop 3 — Deterministic validation

Check at least:

1. `RoomData(0)` ID/name and row hashes match both locale tables.
2. `objMap`/`objDir` are rectangular 10×10 grids and every cell uses row-major `(x,y)`.
3. The raw map domain is `{0,1,2,3,4,5,6}` and the only door cell is `(8,4)`.
4. Native map assignment and the flat-index contract match `x + y * width`.
5. Type-4 anchor `(4,2)` binds `FurnitureData(0)` and has all 9 footprint cells.
6. The passability matrix matches `[[true,false,false],[true,false,false],[true,true,true]]`; zero-cell probes are `true` and the all-nonzero probe is `false`.
7. The route path matches `[[8,4],[7,4],[6,4]]`, has 2 steps, and every step is a cardinal neighbor.
8. Occupied type-2, non-passable type-4, and type-6 probes are rejected.
9. Every provenance path exists and its SHA-256 matches.
10. No raw C# import, renderer, runtime behavior, or `ObjectCatalog` output exists.

### Loop 4 — Regression

Commands that must pass:

```powershell
python -B tools/social-dev/build_scene_catalog.py
python -B tools/social-dev/test_scene_catalog.py
python -B tools/social-dev/test_phase1d_closure.py
```

The builder must be deterministic in its data payload and must not include a timestamp in the fixture hash used for comparison; timestamps are allowed only in package metadata.

### Loop 5 — State handoff

Update `PROJECT_STATE.md` and `TODO.md` only after validation passes, recording:

- artifact paths and schema versions;
- check count and pass status;
- input-hash/provenance summary;
- remaining deferred items;
- next work: `ObjectCatalog` only.

## Phase 2A acceptance gate

Phase 2A is closed when:

- `scene_catalog_contract.json` has status `pass` and semantic status `approved_for_runtime_contract`;
- fixture validation has no failed checks and includes at least 10 checks from the list above;
- the contract has one scene record `room:0` with complete grid/door/type-4/route data;
- provenance is complete for source tables, C# source, native/APK, and Phase 1D evidence;
- running the builder twice produces equal fixture/contract data except for `generated_at_utc`;
- the Phase 1D regression still passes;
- no renderer, runtime behavior, `ObjectCatalog`, `ActorCatalog`, or TypeScript core files were created by this work.

Only after this gate passes may Phase 2B (`ObjectCatalog`) begin from this contract.
