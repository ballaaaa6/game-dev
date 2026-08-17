# Social Dev Phase 1C — Scene-semantics review

Date: 2026-08-13

Status: formally superseded and closed by Phase 1D native-semantics evidence
and the Pre-runtime Closure Sweep. The Phase 1C package is historical; the
replacement matrix is `knowledge/fixtures/accepted/phase1_supersession.json`.

## Results that remain useful

- RoomData(0) has `objMap_`/`objDir_` size `10×10`.
- Raw map domain is `0..6`; the raw door-code candidate is one cell `(x=8,y=4,value=5)`.
- Map histogram: `0=31`, `1=8`, `2=6`, `3=16`, `4=2`, `5=1`, `6=36`.
- FurnitureData parses in both locales with `103` IDs, parse errors `0`, and missing locales `0`.
- `13` FurnitureData records have non-empty `passMap_`.
- There are `12` source slices, `9` observations, and a `100`-node route grid.
- Validation status: `pass`; historical semantic status: `pending_review`.
- Active closure status: `closed_by_authority`.

## What Phase 1D additionally closed

Current-APK native evidence is normalized in `knowledge/fixtures/accepted/scene_native_semantics.json` and checked with `scene_native_semantics_validation.json`:

1. `Room.InitObjChips` passes `RoomData.objMap_[y][x]` directly as the `ObjChip` `type` argument and stores the flat index as `x + y * width`.
2. Raw code `5` is therefore the `ObjChip` door type before `Room.PlaceDoor`.
3. `GetStandingPositions` has four deterministic positions according to the native formula and the order recorded in evidence.
4. Furniture placement is a layer separate from `objMap`: `PlaceObj` binds `FurnitureData`, `PlaceDesk` uses `FLAG_INIT_DESK=16384`, and `AppData.NewGame` uses `FLAG_INIT_PLACE=32768` with empty type-1 chips.
5. `Astar.AddNeighbor` uses cardinal 4-neighbor movement; there are no diagonal edges and no center edge.

The previous conclusions that map assignment was unproven and that 8-neighbor movement was a candidate are superseded and must not be cited as current status.

## Historical blockers and final disposition

- `ObjChip.IsPassable` had already confirmed the `FurnitureData.passMap_` consumer window: anchor `dx_ + dy_ * 3 + 4` and a 3×3 read window, but the final boolean meaning of the zero-cell branch and null-furniture fallback still required fixture normalization.
- A candidate fixture was available: FurnitureData ID `0` (`Huge World`), type `4`, passMap `9×9`; the footprint still needed real `dx_`/`dy_` placement before testing.
- `_searchRoute` source showed type 2/3/4/6 filters, but Ghidra noise at the native function boundary kept it bounded-candidate.
- Goal predicate/selection was not closed; raw code `2` was only a goal candidate.
- `seb_`/`subSeb_`/`img_` selectors were quarantined and did not block the next route fixture, but they blocked visual-catalog promotion.

## Route-fixture status at the time

The historical `blocked_on_fixture_semantics` label is superseded. The Phase 1D
passMap, standing-position, neighbor, route-goal, and selector fixtures close
all three Phase 1C review items. The old route label remains in the historical
package only; it is not an active blocker.

## Key files

- `knowledge/fixtures/accepted/scene_semantics_review.json`
- `knowledge/fixtures/accepted/scene_semantics_validation.json`
- `knowledge/fixtures/accepted/scene_native_semantics.json`
- `knowledge/fixtures/accepted/scene_native_semantics_validation.json`
- `tools/social-dev/build_scene_native_semantics.py`
- `tools/social-dev/test_scene_native_semantics.py`
- `knowledge/fixtures/accepted/phase1_supersession.json`
- `knowledge/fixtures/accepted/semantic_review_closure.json`
- `docs/roadmap/Roadmap_SocialDev_Phase1D_NativeSemantics.md`

Re-run with:

```powershell
python -B tools/social-dev/build_scene_semantics_review.py
python -B tools/social-dev/test_scene_semantics_review.py
python -B tools/social-dev/build_scene_native_semantics.py
python -B tools/social-dev/test_scene_native_semantics.py
```
