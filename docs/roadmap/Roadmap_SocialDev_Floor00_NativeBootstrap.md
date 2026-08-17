# Roadmap — Social Dev `floor00` Native Bootstrap Scene

Status: implemented and gated; retained as an explicit comparison route

## Objective

Add a web-visible `floor00` scene that reproduces the first-game bootstrap from the approved native/runtime contracts. The scene must use the quantities and coordinates that the bootstrap actually consumes, while keeping the historical `display-slice-01` visual baseline available for comparison.

## Identity decision

In this roadmap, `floor00` means the initial bootstrap scene:

```text
AppData.NewGame
  -> roomData_[0]
  -> Room(14, 14, 0, roomData_[0], isPreview=false)
  -> Room.PlaceDesk(0)
  -> initStaffs / Room.AddStaff
```

It does not mean replacing the room with the literal `floor_00.png` texture. The native `room:0` row has `floorImgId_=5`, which resolves through `Room.FLOOR_IMAGE_ID_ARRAY` to `floor_05.png`. The literal `floor_00.png` is used by other RoomData rows and is not the `room:0` bootstrap floor.

## Authority inputs

- `knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json`
- `knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json`
- `knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json`
- `knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json`
- `knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json`
- `knowledge/fixtures/accepted/runtime/actor_spawn_contract.json`
- `knowledge/fixtures/accepted/runtime/display_asset_manifest.json`
- `knowledge/fixtures/accepted/runtime/scene_catalog_contract.json`
- `knowledge/fixtures/accepted/runtime/room_catalog_contract.json`

C# and native files remain evidence inputs only. The browser continues to import approved runtime contracts and promoted assets, not source roots or recovered code.

## Native scene contents

### Map and topology

- Native `MapChip` topology: `floor=0`, `14x14`, `196` cells from `MAPCHIP_ARRAY[0]`.
- Native `ObjChip` topology: separate `10x10`, `100` cells from `RoomData.objMap_`/`objDir_`.
- Preserve the raw ObjChip type histogram `{0:31, 1:8, 2:6, 3:16, 4:2, 5:1, 6:36}`.
- Use the existing floor selector policy: selector/data alias `85/floor_09.png` with the approved `floor_05.png` render pixels. Do not relabel the alias as recovered native provenance.
- Keep the native extension-wall predicates, floor culling, coordinate transform, and nine-pass render order unchanged.

### Native room assets

- Floor: `floor_05.png` render asset under the explicit selector policy above.
- Wall: `wall_00.png`, drawn from the closed `ObjChip.DrawWall` predicates and sprite records.
- Door: `door_01.png` at raw ObjChip cell `(8,4)`, raw type `5`, installed flag `1`, with `FurnitureData=null` in `Room.PlaceDoor`.

### Native initial furniture instances

Render exactly six instances, with four unique FurnitureData IDs:

| FurnitureData | Name | Count | Cells | Native trigger |
|---|---|---:|---|---|
| `3` | Wooden Desk | 3 | `(2,4)`, `(3,4)`, `(6,4)` | `FLAG_INIT_DESK` |
| `12` | Trash Can | 1 | `(8,5)` | `FLAG_INIT_PLACE` |
| `26` | Old Printer | 1 | `(8,6)` | `FLAG_INIT_PLACE` |
| `56` | Calendar | 1 | `(2,7)` | `FLAG_INIT_PLACE` |

Raw ObjChip cells that have no explicit FurnitureData binding remain topology/footprint evidence; they must not become invented furniture instances.

### Native initial actors

Spawn exactly three actors from the `actor_spawn_contract`:

- `actor:staff:0` / StaffData `0` — `10s Female`
- `actor:staff:1` / StaffData `1` — `10s Male`
- `actor:staff:2` / StaffData `2` — `20s Female`

The native contract records all three entering through `(8,4)` and initially using the closed `Room.AddStaff` position `(280,-31)`. The presentation route uses `floor00_display_policy.json` to reserve `(4,6)`, `(5,6)`, and `(7,6)` as distinct raw type-0 empty walkable cells and keeps those actors idle for map inspection. Preserve the source-bounded initial fields (`alpha_=0`, `speed_=3`, room reference, and raw identity) in the native spawn contract. ActorCatalog contains five available records, but the bootstrap spawn fixture contains three.

## Implementation sequence

1. Add a deterministic `floor00` bootstrap contract/fixture that references the existing room, assembly, asset, and spawn contracts and freezes the counts above.
2. Add an explicit scene mode/query (`scene=floor00`) and retain the current display slice as a comparison mode; do not silently overwrite its historical screenshots.
3. Project native room assets, the two separate grids, the six native furniture instances, the raw door, and the three actor spawn records into the Canvas renderer.
4. Remove legacy fixture-only drawables from the `floor00` projection (`furniture:0` type-4 anchor, selector-only `furniture:2`/`furniture:5`, and the FurnitureData door surrogate). They remain available only to the preserved comparison mode where required by existing tests.
5. Add UI and diagnostics for scene mode, native counts, FurnitureData IDs, selector IDs, cell coordinates, and the nine native render passes.
6. Add deterministic unit/contract tests and a browser visual gate for the static `floor00` presentation while keeping the existing living trace boundary on `display-slice-01`. Capture new `floor00` screenshots without modifying the historical baseline.
7. After all gates pass, decide whether `floor00` becomes the default landing scene; otherwise keep it as an explicit comparison route.

## Acceptance gates

- Contract status is `pass` and its content hash is deterministic.
- `14x14` MapChip and `10x10` ObjChip grids remain separate.
- Exactly six native furniture draw attempts occur at the six closed cells; no raw-cell inference adds objects.
- Exactly three actors are present in the native spawn contract; the presentation route reserves exactly three distinct verified empty walkable cells and keeps them static.
- Door trace records `FurnitureData=null`; wall/door sprite rectangles and cells match the native assembly contract.
- All nine render passes execute in the declared order.
- Floor alias/render policy is visible in diagnostics and unchanged from the approved contract.
- Browser smoke has zero console errors/warnings and zero unresolved runtime assets for the promoted floor00 subset; the floor00 route remains static while the legacy route retains the behavior trace.
- Historical `display-slice-01` screenshots and evidence remain byte-for-byte unchanged.
- Existing typecheck, Vitest, build, and Phase 3C/all-room gates remain green.

## Explicit non-goals

- Do not use `floor_00.png` as a guessed replacement for the `room:0` floor.
- Do not derive FurnitureData IDs from raw ObjChip types or occupancy.
- Do not spawn all five ActorCatalog records in the first scene.
- Do not add furniture whose native initial binding is absent.
- Do not execute decompiled C# or native code in the browser runtime.
