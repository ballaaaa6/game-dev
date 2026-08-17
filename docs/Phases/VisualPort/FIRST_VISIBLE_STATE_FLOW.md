# First-visible state flow

Status: `SOURCE_LIMITED`.

The source-backed portion is `AppData.NewGame` through `Room.AddStaff`. `Room` construction selects floor `0`, creates the 14×14 MapChip extent and 10×10 ObjChip grid, installs the raw type-5 door, places initial desks, creates the pinned initial Staff entries, and places eligible type-1 equipment after room insertion.

The open portion starts at the tutorial/startup boundary. `GameForm` can push a first-login notice and `GameForm.DrawGameScreen` can call `Room.Draw`, but the pinned C# does not provide a readable direct start-game caller for `AppData.NewGame`, a complete EventData action interpreter, or a stable-state predicate that identifies the first drawable main display. Those missing edges are recorded as FS-U01, FS-U02, and FS-U03.

The result is a bootstrap contract, not a final first-visible scene. `RoomData(0)`, `Room` construction, NewGame bootstrap, AddStaff spawn, first stable display, and later starter state remain separate labels until the missing transitions are proven.

Evidence: [first-visible-state-flow.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-state-flow.json) and [unknowns.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/unknowns.json).
