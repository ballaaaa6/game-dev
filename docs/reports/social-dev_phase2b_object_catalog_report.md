# Social Dev Phase 2B — ObjectCatalog Report

Date: 2026-08-13
Status: **Complete**
Scope: `display-slice-01`

## Outcome

Phase 2B produced and validated the canonical ObjectCatalog contract from the approved SceneCatalog and Phase 1D authority package. The contract is `pass` / `approved_for_runtime_contract`.

The package contains:

- `4` promoted FurnitureData records: `0`, `1`, `2`, and `5`.
- `7` raw ObjChip types: `0..6`, with source constant labels preserved as source-only evidence.
- `3` scene bindings: the verified type-4 fixture, the raw door cell, and the occupied type-2 route probe.
- `8` resolved selector identities and `4` explicit `-1` sentinel selectors across `seb_`, `subSeb_`, and `img_`.

## Canonical artifacts

- Runtime contract: `knowledge/fixtures/accepted/runtime/object_catalog_contract.json`
- Evidence fixture: `knowledge/fixtures/accepted/object_catalog_fixture.json`
- Validation: `knowledge/fixtures/accepted/object_catalog_validation.json`
- Builder: `tools/social-dev/build_object_catalog.py`
- Deterministic test: `tools/social-dev/test_object_catalog.py`

The validation package passed `29/29` checks. Stable hashes are:

- Fixture: `ef34d649b29f5e2335a411a4e383f6d94c344388ea8234b774efa7ee3090da83`
- Contract: `c9bfa41fa8d6f8b2904a4cd025d431543898f036d16356abb74c9c9c1b2621e4`
- Input manifest: `ac140df6ab5dc54f4aa77cb172add0ce0b63cd249e5c077f5153ccf2feae77d5`

## Verified boundaries

The type-4 anchor at `(4,2)` is bound to `FurnitureData(0)` as a bounded native fixture. Its `9`-cell footprint and `3×3` passability matrix are preserved from the Phase 1D authority.

The door cell at `(8,4)` is represented as raw type `5`, installed flag `1`, and a `FurnitureData(1)` selector candidate. Native binding remains deferred because `Room.PlaceDoor` passes `FurnitureData=null`; the contract does not promote that candidate as a native relationship.

The occupied type-2 route probe at `(6,4)` keeps its explicit `FurnitureData(2)` fixture-only relation and rejected route admission. The real route fixture remains `(8,4) → (7,4) → (6,4)` with 4-neighbor movement.

Selector identities are tied to the existing asset selector contract, indexed asset rows, selector-index hashes, and the pinned asset ZIP. No PNG/SEB binaries are copied into the runtime contract. Raw map assignment remains separate from FurnitureData placement.

## Provenance and verification

The package records `11` current source slices, `17` manifest inputs, both locale rows for every promoted FurnitureData record, `9` native methods, the pinned APK hash, and the pinned asset ZIP hash. All source-slice and binary hash checks pass.

The following deterministic commands passed:

```text
python -B tools/social-dev/test_phase1d_closure.py       # 18/18
python -B tools/social-dev/test_scene_catalog.py         # 22/22
python -B tools/social-dev/test_scene_native_semantics.py
python -B tools/social-dev/test_scene_semantics_review.py
python -B tools/social-dev/test_object_catalog.py        # 29/29
```

The native and semantics tests retain their documented `route=blocked_on_fixture_semantics` review label; this is an upstream evidence-review status and does not invalidate the closed Phase 1D route fixture consumed by ObjectCatalog.

## Next boundary

`ActorCatalog` is the next active contract. Full object placement, standing positions, visual frame composition, camera/coordinate transforms, renderer behavior, and the TypeScript runtime remain outside Phase 2B.
