# V5 Room Recovery

Phase V5 recovers the original `Room` / `RoomData` surface and places the room-owned static orchestration in an isolated runtime boundary. The implementation is additive under `runtime/social-dev/src/v5/` and reuses the already-verified V4 MapChip, ObjChip, FurnitureData, Camera, and ordering adapters.

## Result

The selected static scope is `PASS_STATIC`:

- all 18 RoomData records load with native names, numeric selectors, 10x10 `objMap_` and `objDir_` grids, raw ObjChip identities, door cells, and source-row hashes;
- `Room.floor_` selects the native 14x14 or 4x4 map topology independently from `RoomData.floorImgId_`;
- room initialization preserves `InitMapChips`, `InitObjChips`, structural facility setup, door placement, and explicit FurnitureData placement;
- the original nine Room.Draw visual pass slots and local row/column ordering are preserved;
- room:0 emits a deterministic static command manifest with 74 commands, 59 traces, and 788 pass events;
- rooms 1-17 remain topology-only because their constructor evidence contains no native furniture bindings.

## Evidence and implementation

The evidence package is in `knowledge/fixtures/accepted/visual-port/v5/`. The runtime package is in `runtime/social-dev/src/v5/`, with focused tests in `runtime/social-dev/tests/v5-room.test.ts`.

The native source and generated evidence roots remain read-only and are never executed. V5 records command and call-flow evidence; it does not claim exact framebuffer pixels.

## Boundary

No production renderer import, local server, emulator, ADB, live app, network evidence, gameplay, Staff/Avatar behavior, or V6 work is included. The task stops after V5 static verification.
