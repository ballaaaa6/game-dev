# Social Dev display asset/frame gate

The gate promotes only source PNG/OPT/SEB bytes and frame records that passed exact selector, hash, source-rectangle, or native coordinate-composition checks.

## Result

- Gate status: `pass` / `approved_for_runtime_subset`
- Approved gate entries: `18` of `18`
- Promoted binary assets: `34`
- Gate content hash: `a9b5b2f9076dc3f05fde9ab64d88f96ef5dea27fd467ec045025d2fb2472dd08`

## Runtime-approved subset

- Staff source PNGs `chara86.png` through `chara90.png`.
- Human `wait_right.seb` and `typing_right.seb` records, with source rectangles verified against the selected 270x60 strips.
- `furniture:0` / `big_base00.seb` with its direct `big_base00.png` source rectangle.
- `furniture:1` / `door_03.seb` through the exact `door_02.png` + `door_02.opt` logical atlas.
- `furniture:5` / `desk_00.seb` plus `chair_02.seb` through exact OPT logical atlases.
- Room `wall_00.png`/`wall_00.seb` and `door_01.png`/`door_02.seb` through the native `ObjChip.DrawWall` coordinate contract.
- `furniture:2` / `desk_00.seb` plus `chair_00.seb` through the approved Phase 3A OPT logical composition.

## Explicitly blocked

- Room floor image id `5` remains source-unresolved; the selected `floor_09.png` (indexed selector `85`) is promoted only as an explicit runtime fallback.

## Runtime policy

The browser imports `knowledge/fixtures/accepted/runtime/display_asset_manifest.json` only. It loads no source archive, APK, C# file, or unapproved asset. Placeholders remain the bounded fallback while the approved subset loads.
