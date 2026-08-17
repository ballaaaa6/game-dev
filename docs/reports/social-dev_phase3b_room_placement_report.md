# Social Dev Phase 3B Room Placement Report

## Outcome

Phase 3B is closed for the native `room:0` placement contract. The contract is
`pass` / `approved_for_runtime_contract`, and its deterministic validation gate
passes `20/20` checks.

The current contract hash is
`190ab9b8b520042a1604a06f8ba0d9554e8a0ec3249b1282cf7d02e791494897`.

The closure is evidence-bounded. `RoomData(0).floorImgId_ = 5` remains an
explicit unresolved selector because the pinned `chip/img.inf` has no entry for
id `5`. No floor filename or binary was inferred. The wall and door image
selectors resolve as `6 → wall_00.png` and `7 → door_01.png` in the source asset
index, but neither image is promoted into the Phase 3B runtime asset subset.

## Closed contract

The package closes the following native facts for `room:0`:

- `Room.InitMapChips → InitObjChips → SetupBigChipsParent → PlaceDoor` order.
- `RoomData.objMap_[y][x]` as the raw `ObjChip.type_` assignment with flat index
  `x + y * width`.
- Raw door type `5` at `(8,4)`, installed flag `1`, and the native
  `PlaceDoor` `FurnitureData=null` boundary.
- The verified type-4 `FurnitureData(0)` parent at `(4,2)`, its nine-cell
  footprint, and the closed 3×3 passability matrix.
- The route fixture `(8,4) → (7,4) → (6,4)`.
- Room cell, actor, map-chip, and object draw coordinate formulas, including
  the explicit `ofx/ofy` camera boundary and bounded 10×10 probe values.
- The observed `Room.Draw` call-site order, plus an overlap fixture that guards
  the door-object versus floor-image pass order.

## Furniture boundary

The approved display compositions remain separate from native room identity:

- `furniture:0` is the verified native type-4 fixture.
- `furniture:1` is an approved door composition and a selector candidate, not a
  claimed native `FurnitureData` binding for the raw door cell.
- `furniture:5` is an approved composition but has no evidenced native binding
  in `room:0`.
- `furniture:2` is now an approved source-backed display composition after the
  variable-piece `chair_00.opt` reconstruction, but it has no evidenced native
  `room:0` FurnitureData(2) binding and is therefore not claimed as a placed
  native object.

## Artifacts

- Source audit: `knowledge/fixtures/accepted/phase3b_room_placement_source_audit.json`
- Deterministic fixture: `knowledge/fixtures/accepted/phase3b_room_placement_fixture.json`
- Validation: `knowledge/fixtures/accepted/phase3b_room_placement_validation.json`
- Runtime contract: `knowledge/fixtures/accepted/runtime/room_placement_contract.json`
- Builder/test: `tools/social-dev/build_phase3b_room_placement.py` and
  `tools/social-dev/test_phase3b_room_placement.py`
- Runtime loader types and boundary: `runtime/social-dev/src/catalog/types.ts`
  and `runtime/social-dev/src/catalog/load-contracts.ts`

## Verification

- Phase 3B validation: `20/20` checks passed.
- Phase 1D closure: `18/18` checks passed.
- SceneCatalog: `22/22` checks passed.
- ObjectCatalog: `29/29` checks passed.
- Display asset gate: `10` checks passed; `12` approved and `2` blocked entries,
  with `22` promoted source binaries.
- Phase 3A approval gate: passed with exact `chair_00` source binaries and
  `furniture:2` included in the display manifest.
- Runtime typecheck: passed.
- Runtime tests: `6` files and `12` tests passed.

## Boundary to Phase 3C

Phase 3C may consume this contract to integrate Canvas placement and the visual
browser gate. It must retain the unresolved floor selector as fallback/raw-only
data, preserve the source-bounded draw pass order, and avoid changing the
existing screenshot baseline until a comparison-policy decision is recorded.
