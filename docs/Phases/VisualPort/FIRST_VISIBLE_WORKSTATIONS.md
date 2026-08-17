# First-visible workstations

Status: bootstrap IDs, cells, directions, and relative placement `SOURCE_BACKED`; first-visible state identity `SOURCE_LIMITED`.

`Room.PlaceDesk` scans the source-backed `FLAG_INIT_DESK` value `0x4000` and binds FurnitureData id `3` (`Wooden Desk`, SEB `1`, sub-SEB `3`, image `148`) to raw type-2 cells `[2,4]`, `[3,4]`, and `[6,4]`. The pair `[2,4]` and `[3,4]` is adjacent and carries opposite native directions: raw `3` / `DIRECTION_DOWN` / vector `[-1,0]` and raw `2` / `DIRECTION_UP` / vector `[1,0]`. The third workstation at `[6,4]` is raw direction `2` / `DIRECTION_UP`.

The direction mapping is native and the runtime policy is to preserve the raw value. No manual rotation, directional asset inference, or screenshot-derived coordinates were used. Catalogue id `5` (`Graphics Workstation`) is not promoted because the NewGame binding evidence does not select it.

This closes the bootstrap workstation contract only. It does not prove that the same binding is the first stable visible set after tutorial/event normalization, so FS.7 stops before a full-room render.

Evidence: [workstation-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/workstation-contract.json) and [workstation-orientation-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/workstation-orientation-contract.json).
