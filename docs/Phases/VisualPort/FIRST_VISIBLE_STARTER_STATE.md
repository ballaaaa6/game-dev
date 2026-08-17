# First-visible starter state

Status: `FIX_REQUIRED` — forensic gate stopped before V8.

The static source closes the NewGame bootstrap but does not close the state boundary requested by this gate: the exact content shown after tutorial/startup initialization when the main display becomes stable. The earlier reintegration artifact classified `Room(0)` after `AppData.NewGame` as a starter environment, but it explicitly excluded tutorial overlays, event mutations, and gameplay. It is therefore secondary evidence, not proof of the first-visible state.

The closed bootstrap chain is:

`RoomData(0)` → `Room(14,14,0,roomData_[0],false)` → MapChip/ObjChip setup → `PlaceDoor` → `PlaceDesk(0)` → `AddStaff` for the pinned three `initStaffs` → room insertion → `FLAG_INIT_PLACE` equipment scan.

The bootstrap contains source-backed wall, door, three Wooden Desk cells, Trash Can, Old Printer, Calendar, and three Staff spawn records. The transition from that state through tutorial/event startup to the first stable `main_display` is not source-closed. No object was renamed, moved, rotated, or removed based on a screenshot.

Evidence: [starter-state-model.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/starter-state-model.json), [first-visible-scene-manifest.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-scene-manifest.json), and [checkpoint-ledger.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/checkpoint-ledger.json).

V8 was not started. MapChip, V6 Staff semantics, and the production renderer remain unchanged.
