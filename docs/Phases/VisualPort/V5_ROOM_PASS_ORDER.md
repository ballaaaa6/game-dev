# V5 Room Pass Order

V5 preserves the Room.Draw order recovered in the native placement contract:

1. `map-extension-floor`
2. `map-chip`
3. `object-chip-primary`
4. `object-chip-wall`
5. `avatar-primary` (empty V5 slot)
6. `avatar-secondary` (empty V5 slot)
7. `object-chip-late-preview` (empty selected-fixture slot)
8. `object-chip-late`
9. `map-floor`

Within MapChip and ObjChip inputs, the V4 comparator remains row-ascending, x-descending, layer-ascending, and key-stable. V5 does not replace native pass order with a global y-sort. Room:0 uses the closed foreground wall cells `[8,7]` and `[8,8]`; the raw type-5 door at `[8,4]` remains in the rear wall slot.

The pass schedule is recorded in `knowledge/fixtures/accepted/visual-port/v5/room-pass-schedule.json`. Staff/Avatar slots are retained as explicit empty boundaries and are not synthesized in V5.
