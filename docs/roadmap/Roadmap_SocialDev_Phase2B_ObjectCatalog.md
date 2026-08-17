# Social Dev Phase 2B — Canonical `ObjectCatalog`

สถานะ: **ปิดครบ**

Phase 2B follows the completed `SceneCatalog` by creating a canonical object contract for `display-slice-01` only. The work must separate `ObjChip.type_`, which represents the raw room layout/type grid, from `FurnitureData`, which is bound when objects are placed later, because `RoomData.objMap_` does not store a `FurnitureData.id_` per cell directly.

## Goal and scope

At the end of the phase, the following must be repeatably verifiable:

- how raw object types `0..6` from `RoomData(0)` are passed into `ObjChip.type_`;
- which FurnitureData records the display slice requires and which stable IDs they have;
- which selectors each record's `seb_`, `subSeb_`, and `img_` resolve to;
- what evidence supports the type-4 multi-chip/passMap, door, and desk-route probes;
- which direction, footprint, standing-position, and passability policies can be promoted;
- which values are `verified`, `derived`, `raw_only`, `deferred`, or `quarantine`;
- that the contract loads and validates without importing or executing C#/native code.

Do not expand the work to renderer, camera, coordinate transforms, animation, actor behavior, TypeScript runtime, or copying binary assets into runtime.

## Authority and preconditions

The builder must stop before writing output if any input fails its status/hash gate:

1. `knowledge/fixtures/accepted/runtime/scene_catalog_contract.json` must be `pass` / `approved_for_runtime_contract`.
2. `knowledge/fixtures/accepted/asset_selector_contract.json` must be `pass`, and English/Japanese selectors must match.
3. `phase1d_closure.json` and `phase1d_closure_validation.json` must be `pass` / `closed_for_phase2_entry`.
4. `phase1d_passmap_fixture.json` is authoritative for type-4 passMap/placement.
5. `phase1d_route_fixture.json` is authoritative for route filters, the type-2 probe, and goal/direction fixtures.
6. Source, table, APK, and ZIP hashes referenced in provenance must match the actual files.

C#/native evidence is used to create the contract only; it is not a runtime dependency. The original source roots remain read-only.

## First promoted records

Use stable IDs of the form `furniture:<source_id>` and promote only the display-slice set:

| Stable ID | Source | Type | Role | Status |
|---|---|---:|---|---|
| `furniture:0` | FurnitureData(0), `Huge World` | 4 | type-4 multi-chip/passMap anchor | verified fixture |
| `furniture:1` | FurnitureData(1), `Door` | 5 | door selector record | verified selector; scene binding separate |
| `furniture:2` | FurnitureData(2), `Desk` | 2 | occupied desk route probe | verified fixture binding |
| `furniture:5` | FurnitureData(5), `Graphics Workstation` | 2 | desk/visual variant | verified selector; not a whole-room placement map |

All `103` FurnitureData rows in both locales are selector cross-check evidence, but are not promoted into this runtime contract version.

## Raw types and binding policy

- Retain raw types `0..6`, the histogram, and source-constant references in `raw_object_types`; names `OBJ_TYPE_*` are `source_label_only`.
- Promote `objMap[y][x] → ObjChip.type_` and flat index `x + y * width` as `verified`.
- Promote door cell `(8,4)`, raw type `5`, and installed flag `1` as `verified`.
- Do not claim that raw type `5` binds to FurnitureData(1) in the native path: `Room.PlaceDoor` calls `PlaceObj` with `FurnitureData=null` and then writes the flag. Keep FurnitureData(1) as a selector record and classify door binding as `candidate_by_type_and_selector` or `deferred`.
- Promote type-4 anchor `(4,2)` ↔ FurnitureData(0) according to the passMap fixture with its 3×3 footprint and passability fixture.
- Keep route probe `(6,4)` ↔ FurnitureData(2) as `fixture_only`.
- Treat types `0`, `1`, `3`, and `6` as raw/type policy and scene evidence while per-cell FurnitureData binding is unavailable.

## Contract shape

`knowledge/fixtures/accepted/runtime/object_catalog_contract.json` uses schema `social-dev-object-catalog-v1` and contains:

```text
ObjectCatalog
├─ catalog_id = display-slice-01
├─ scene_ref = SceneCatalog(display-slice-01 / room:0)
├─ objects[] = furniture:0, furniture:1, furniture:2, furniture:5
│  ├─ source_identity / locale names
│  ├─ raw_fields: category_, type_, flag_, passMap_
│  ├─ selectors: seb_, subSeb_, img_
│  ├─ geometry / direction_policy / interaction
│  ├─ status / semantic_status / provenance_ref
├─ raw_object_types[]
├─ scene_bindings[]
│  ├─ type4-anchor
│  ├─ door-cell
│  └─ occupied-type2-route-probe
├─ provenance / limits / determinism
```

Selector identity must remain separate from visual-frame composition, and asset binaries must not be copied into `runtime/social-dev/` in this phase.

## Work packages

### WP0 — Source lock and schema review

- Check input status/hash and read SceneCatalog as the room/grid authority.
- Read FurnitureData rows `0,1,2,5` from the real English/Japanese tables.
- Cross-check `FurnitureData.Load` for `id_`, `name_`, `category_`, `type_`, `flag_`, `seb_`, `subSeb_`, `img_`, and `passMap_`.
- Check evidence for `Room.InitObjChips`, `Room.PlaceDoor`, `ObjChip.PlaceObj`, `ObjChip.GetStandingPositions`, `ObjChip.IsPassable`, and the Astar path.
- Ensure every field has status and provenance before creating the package.

### WP1 — Selector projection

- Project selectors for all four records from `asset_selector_contract.json`.
- Check `chip/seb.inf`/`chip/img.inf` through the selector contract and asset index with filename, member path, and hash.
- Enforce sentinel `-1` only for permitted fields.
- Cross-check locale row identity/row hashes.
- Separate `selector_resolved` from `visual_frame_verified`.

### WP2 — Geometry, occupancy, and direction

- Project the type-4 3×3 footprint, anchor, passMap window, matrix, and probes.
- Project only the local standing-position policy covered by closed evidence.
- Project type-2 direction from `objDir_[iy][ix]` and the route-goal fixture.
- Retain type-1 border direction/type-4 child layout as bounded policy.
- Do not derive placement for every occupied RoomData cell from raw type alone.

### WP3 — Deterministic binding fixtures

Create at least these three cases:

1. `type4-anchor`: `(4,2)`, raw type `4`, `furniture:0`, 9-cell footprint, passability matrix, and native references.
2. `door-cell`: `(8,4)`, raw type `5`, installed flag `1`, and the `furniture:1` selector candidate kept separate from native PlaceDoor binding.
3. `occupied-type2-route-probe`: `(6,4)`, raw type `2`, explicit `furniture:2`, `has_obj=true`, route admission rejected.

Every binding must have `binding_status` separate from `object_status`; fixture-only bindings must not be used as global mappings.

### WP4 — Builder and artifacts

Create:

```text
tools/social-dev/build_object_catalog.py
tools/social-dev/test_object_catalog.py
knowledge/fixtures/accepted/object_catalog_fixture.json
knowledge/fixtures/accepted/object_catalog_validation.json
knowledge/fixtures/accepted/runtime/object_catalog_contract.json
```

The builder must fail fast when upstream status/hash checks fail, use relative provenance paths, create stable JSON without counting `generated_at_utc` in the content hash, avoid importing/executing C#, and reject duplicate IDs, invalid sentinels, selector drift, shape drift, unproven global bindings, and `unknown` promoted objects.

### WP5 — Validation gates

Check at least:

1. SceneCatalog passes and `room:0` has a `10×10` grid.
2. Provenance files exist and hashes match.
3. Exactly 4 records are promoted with stable IDs.
4. English/Japanese rows and hashes match.
5. Non-sentinel selectors resolve and sentinel policy is correct.
6. FurnitureData(0) type `4`, passMap `9×9`, 9-cell footprint, and matrix `[[true,false,false],[true,false,false],[true,true,true]]`.
7. Zero-cell probes are passable and the all-nonzero probe is blocked.
8. Scene raw types include `{0,1,2,3,4,5,6}` and the histogram matches SceneCatalog.
9. Map assignment, flat index, and door flag match native evidence.
10. Route path/filter and 4-neighbor policy match Phase 1D.
11. Type-2 direction/desk fixture matches `objDir`/route evidence.
12. The door candidate is not promoted to a native binding.
13. Promoted fields have status, source/evidence references, confidence, and review note.
14. Fixture/contract/validation hashes are deterministic on rebuild.
15. No renderer, runtime core, ActorCatalog, camera, or raw C# import exists.

### WP6 — Regression and report

Run in order:

```powershell
python -B tools/social-dev/test_phase1d_closure.py
python -B tools/social-dev/test_scene_catalog.py
python -B tools/social-dev/test_scene_native_semantics.py
python -B tools/social-dev/test_scene_semantics_review.py
python -B tools/social-dev/build_object_catalog.py
python -B tools/social-dev/test_object_catalog.py
```

Create `docs/reports/social-dev_phase2b_object_catalog_report.md` with records, selector counts, binding statuses, validation counts, hashes, and deferred items.

### WP7 — State handoff

After the gate passes, update `PROJECT_STATE.md` and `TODO.md` with schema/hash, artifact paths, check counts, upstream regression, deferred boundaries, and next work: Phase 2C `ActorCatalog`.

## Definition of done

- Contract is `pass` / `approved_for_runtime_contract`.
- Fixture/validation is deterministic with no failed checks.
- Records `furniture:0,1,2,5` load with complete provenance.
- Type-4, door, and occupied type-2 fixtures are repeatable with correct binding status.
- No unproven global map-to-FurnitureData claim exists.
- SceneCatalog/Phase 1D regression passes.
- Report/state handoff matches actual files.
- No ActorCatalog, Vite/TypeScript runtime, renderer, or behavior core exists yet.

Only after this gate passes may Phase 2C (`ActorCatalog`) begin.
