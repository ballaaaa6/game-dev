# Social Dev Phase 2A — `SceneCatalog` Closure Report

Status: **complete**

Phase 2A created the canonical `SceneCatalog` from `RoomData(0)` and closed deterministic validation before starting `ObjectCatalog`. This work did not create a renderer, runtime behavior, `ObjectCatalog`, `ActorCatalog`, or TypeScript runtime core.

## Results

| Item | Result |
|---|---|
| canonical scene | `room:0` / `RoomData(0)` |
| locale names | English `Floor A`, Japanese `フロアA` |
| grid | `10×10`, `objMap` + `objDir` |
| native flat index | `x + y * width` |
| door | type `5`, cell `(8,4)`, installed flag `1` |
| type-4 fixture | anchor `(4,2)`, `FurnitureData(0)`, 9 footprint cells |
| passability | matrix `[[true,false,false],[true,false,false],[true,true,true]]` |
| route | `(8,4) → (7,4) → (6,4)`, 2 steps |
| route negative probes | occupied type-2, non-passable type-4, type-6; all rejected |
| validation | `22/22` checks passed |

## Artifacts

- Contract: `knowledge/fixtures/accepted/runtime/scene_catalog_contract.json`
- Deterministic fixture: `knowledge/fixtures/accepted/scene_catalog_fixture.json`
- Validation: `knowledge/fixtures/accepted/scene_catalog_validation.json`
- Builder: `tools/social-dev/build_scene_catalog.py`
- Test: `tools/social-dev/test_scene_catalog.py`
- Detailed plan: `docs/roadmap/Roadmap_SocialDev_Phase2A_SceneCatalog.md`

## Provenance closure

The package records and checks:

- English/Japanese `RoomData(0)` row hashes;
- English/Japanese `FurnitureData(0)` row hashes for the type-4 fixture;
- 11 selected C# source slices with current file/slice hashes;
- 9 native method records and the pinned current APK SHA-256;
- Phase 1D closure, native semantics, passMap, and route evidence references;
- a complete input manifest with hash `eb23e06212000bb77b86653e41f71291d4b8273a63df191378faafa876d615d2`.

Stable payload hashes:

- fixture: `005d370d3ac4ef4a56c3a64c67c91eb1156a3447742672c274a8e944c485dbd8`;
- contract: `7c7da0d1fa5fb64872e20fbd12d4c9a1bcaf15795908b475180f9e83dc010119`.

## Verification loop

The final run ordered upstream evidence generators before the SceneCatalog projection, then ran canonical and read-only regressions:

```powershell
python -B tools/social-dev/test_csharp_system_extraction.py
python -B tools/social-dev/test_first_slice_data_candidate.py
python -B tools/social-dev/test_phase1d_closure.py
python -B tools/social-dev/test_scene_behavior_candidates.py
python -B tools/social-dev/build_scene_catalog.py
python -B tools/social-dev/test_scene_catalog.py
python -B tools/social-dev/test_phase1d_closure.py
python -B tools/social-dev/test_scene_native_semantics.py
python -B tools/social-dev/test_scene_semantics_review.py
```

All commands passed. The older Phase 1C/native candidate packages still report their historical `blocked_on_fixture_semantics` route status as expected. The authoritative route status for Phase 2 entry is the Phase 1D closure package and the new SceneCatalog fixture.

## Boundary and next step

The contract deliberately keeps `doorImgId_` and visual-asset promotion as `raw_only`/deferred. Full furniture-to-cell placement is also deferred because native evidence establishes the placement model but does not provide a complete per-cell `FurnitureData` catalog. The next authorized phase is `ObjectCatalog`; runtime implementation must not begin before its canonical fixture and validation are closed.
