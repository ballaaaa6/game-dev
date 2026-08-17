# First stable main-display boundary

## Predicate

The static native boundary for the first main-display draw is:

1. `GameForm.state_ == STATE_NORMAL == 2`.
2. `GameForm._update` calls `AppData.ExeEvent(2)`; a true event-work result takes the event branch and prevents the normal update remainder. The candidate stable tick therefore has an event-work result of false.
3. `GameForm.DynamicRender` has a non-null, non-empty offscreen buffer and the form is active.
4. `AppData.frmMenu_` is present and `isSliding_ == false`.
5. `DynamicRender` calls `DrawGameScreen`; that method iterates `Player.GetRoom(floor)` and calls `Room.Draw`.

The relevant source is `sources/raw/1_Click_CSharp_Code update/form/GameForm.cs:667,762,4148,6063`, with native RVAs `GameForm.Update 0x10FE56C`, internal update `0x10FF1AC`, `AppData.ExeEvent 0x1261520`, `DrawGameScreen 0x110422C`, and `Room.Draw 0x12CBB80`.

## What is closed

The native draw-entry conjunction and the event-work gate are closed. The path from the title handoff to GameForm is also closed: title state `4` changes the current form to GameForm and sets `FLAG_FROM_TITLE`; GameForm initialization consumes that flag.

## What is not closed

The full stable boundary additionally requires a source-backed final queue snapshot, complete post-event automatic ordering, and stable Staff pose. The allowed evidence does not establish those facts. It also cannot confirm the exact completion ordering of the startup get-server-time subform without live execution.

## Preview decision

No isolated preview is generated because the stable boundary is only partially source-closed. Full starter-room rendering, final-room reintegration, screenshot tuning, and V8 are explicitly out of scope for this stop point.

See [first-stable-boundary-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/first-stable-boundary-contract.json) and [previews/README.md](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/previews/README.md).
