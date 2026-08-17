# V6 Room and Staff integration

V6 integrates Staff into `RoomV5` by reconstructing the existing pass ranges and inserting Staff commands at the native `avatar-primary` seam. V5 is not edited and its baseline command, trace, event, and pass semantics remain available as the immutable base result.

The static order is:

`object-chip-wall` → `avatar-primary` Staff → `avatar-secondary` → `object-chip-late-preview` → `object-chip-late` → `map-floor`.

This preserves rear-wall-before-actor and foreground-wall-after-actor occlusion. The native nine-pass contract proves the pass position and order. The decompiled general Room.Draw body does not prove whether live Staff instances reach that slot directly or through an Avatar relationship, so that relationship is retained as `SOURCE-LIMITED` rather than guessed.

The room:0 fixture keeps all three native initial Staff records at the verified door cell `[8,4]` and world position `[280,-31]`. The visible static preview is an explicit action/direction/frame presentation state and does not rewrite the native alpha-zero spawn contract.
