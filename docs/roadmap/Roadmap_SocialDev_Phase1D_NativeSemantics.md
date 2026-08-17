# Social Dev Phase 1D — Native scene-semantics closure

Status: **complete for entry into Phase 2**

Phase 1D closes only the evidence/fixture/behavior gates required for a living scene. It does not create `SceneCatalog`, `ObjectCatalog`, `ActorCatalog`, or the TypeScript runtime core; those are the next Phase 2 work in the user-defined order.

## Engineering loop used

1. Read the current APK and ZIP native/source/data/asset evidence.
2. Build fixtures from real records rather than guessing semantic values from raw maps.
3. Perform deterministic normalization/emulation only for verified branches.
4. Check negative probes and provenance with the test runner.
5. Update state/TODO only after the complete closure validation passes.

## Closed gates

### 1. Type-4 `passMap_` fixture / `IsPassable`

- Use the `RoomData(0)` anchor `(x=4,y=2, raw=4)` and `FurnitureData(0)` (`Huge World`, type `4`).
- Verify the native footprint `dx_/dy_ ∈ {-1,0,1}`, totaling 9 child cells with parent center `(0,0)`.
- Verify the window: `anchor = dx + dy * 3 + 4`, divided into a 3×3 block in the 9×9 passMap.
- Verify the native-loop result: a selected zero cell → `true`; all 9 selected cells nonzero → `false`.
- Verify the full 9-offset matrix and zero-cell/all-nonzero probes.
- Handle the null-furniture branch within the fixture through explicit FurnitureData binding; record that the native fallback branch returns to the same consumer and do not guess selector identity.

### 2. Astar neighbor / goal filter

- Cardinal neighbors only: west/east/north/south.
- Type `2`: reject when `HasObj()` is true.
- Type `3/4`: reject when `IsPassable()` is false.
- Type `6`: always reject.
- Public goal flags: desk `1`, equipment `2`, staff `4`.
- Equipment goal type `1` uses `objDir`: `0→7`, `1→6`, other values `→0`; desk/staff/default branches are recorded separately.
- Staff move dispatch matches flags: equipment `1→2`, to-staff `7→4`, goto-desk `3→1`.

### 3. Real route fixture

- Real route from RoomData(0): `(8,4) → (7,4) → (6,4)`, two steps.
- Negative probes cover occupied type-2, the real type-4 center with `IsPassable=false`, and type-6.
- Provenance is complete: RoomData row hash, C# source hashes, native method RVAs/file offsets, and APK SHA-256.

### 4. Asset selectors

- Check all `103` parsed FurnitureData rows × 2 locales and all `141` StaffData rows × 2 locales.
- Every nonnegative `FurnitureData.seb_`, `img_`, and `subSeb_` resolves in chip `seb.inf`/`img.inf`.
- Every `StaffData.img_` value resolves in human `img.inf`; permitted `-1` sentinels are stored as absent rather than asset IDs.
- English/Japanese selector sets match, and selected furniture/staff mappings have filenames from the real ZIP.

### 5. Staff living-scene semantics

- The complete set of source-labeled state/move/flag constants used by the living scene.
- Bounded transitions: stay-home→door, work→equipment, work→talk, and talk timing markers `20/70/110/130`.
- Typing start: `FLAG_TYPING`, frame `100`, interval `3`, seb `reverseDirection+23`.
- Typing end: clear the flag, frame `0`, interval `1`, seb `reverseDirection+10`.
- Human seb IDs typing `23–26` and wait `10–13` resolve to right/left/up/down.
- Selected staff `0–4` point to `SkillData(1)`; the skill is type `10`, scene `1`, target `0`, `effects_[8]=[150]`, passive flag `1`.

## Authoritative evidence and commands

Builder/test:

```powershell
python -B tools/social-dev/build_phase1d_closure.py
python -B tools/social-dev/test_phase1d_closure.py
```

Evidence:

- `knowledge/fixtures/accepted/phase1d_closure.json`
- `knowledge/fixtures/accepted/phase1d_passmap_fixture.json`
- `knowledge/fixtures/accepted/phase1d_route_fixture.json`
- `knowledge/fixtures/accepted/asset_selector_contract.json`
- `knowledge/fixtures/accepted/staff_semantics_contract.json`
- `knowledge/fixtures/accepted/phase1d_closure_validation.json`

## Phase 2 entry boundary

Phase 2 starts with this evidence set as input, in this order:

`SceneCatalog → ObjectCatalog → ActorCatalog → deterministic fixtures → TypeScript runtime core`

Do not treat this evidence package as runtime implementation, and do not skip ahead to create catalogs from data outside this selector/behavior scope without adding a new gate.
