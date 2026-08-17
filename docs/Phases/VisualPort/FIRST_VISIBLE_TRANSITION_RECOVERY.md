# First-visible transition recovery

Status: `BLOCKED_SOURCE_LIMITED`

This static recovery reconstructs the path from the completed start-game form through `AppData.NewGame`, the starter event interpreter, and the `GameForm` main-display draw entry. It stops before full starter-room reintegration and V8 because the available source/native evidence does not close the complete post-event queue order or the stable Staff pose.

## Recovered result

The terminal caller is `form.TitleForm.Update()` (`RVA 0x1207E44`). Its only direct native `AppData.NewGame` call is at `0x01208248`, targeting `AppData.NewGame(string,int,FastVector)` (`RVA 0x1263A70`). The branch consumes the completed start-game form result, calls `NewGame`, and enters title fade-out state `3`; it does not directly call `EventData.StartEvent`.

`SubForm.InitStartGame()` and `SubForm.UpdateStartGame()` are the selection form lifecycle (`form type 73`). They initialize and complete the selection, but their recovered native bodies contain no direct `AppData.NewGame` or `EventData.StartEvent` call. `TitleForm.Update()` owns the terminal handoff.

The first source-backed event is event `0` (`EV_FIRST_TALK`). Its login-term row is `[[3,1,4]]` and its execution rows are `[[0,0],[1,10]]`: `SCR_TALK(0,0)` followed by `SCR_DELAY(10)`. The talk handler creates a staff-talk form; the delay handler writes `delayFrame_=10`. Neither handler writes room, furniture, wall, door, or Staff pose fields.

The recovered draw-entry predicate is: `GameForm.state_ == STATE_NORMAL == 2`; `AppData.ExeEvent(2)` returns false for that tick; the form is active; the offscreen buffer is non-empty; and the menu is not sliding. `DynamicRender` then calls `DrawGameScreen`, which iterates `Player.GetRoom(floor)` and calls `Room.Draw`.

## Checkpoint outcome

| Checkpoint | Result |
| --- | --- |
| FR.0 | Complete: filesystem unknown inventory captured |
| FR.1–FR.6 | Complete for the recovered caller, event 0, and bootstrap/no-mutation path |
| FR.7 | Source-limited: later automatic-event order and mutations unresolved |
| FR.8 | Native draw-entry predicate closed; full tutorial-stable frame not closed |
| FR.9 | Partial bootstrap manifest complete |
| FR.10–FR.11 | Partial/source-limited; FS-U01 closed, FS-U02–FS-U06 reclassified with blockers |
| FR.12 | Intentionally not run; no preview generated |
| FR.13 | Complete: 53 Python/static gates, 334 JSON files, 119 Python AST files, Vitest, typecheck, build, and diff checks pass |
| FR.14 | Stop before full-room reintegration and V8 |

## Source-backed bootstrap manifest

The partial manifest retains the frozen room-0 facts: a 14x14 floor, `floor_raw=5`, `wall_raw=6` using `wall_00.png` selector `5`, door cell `[8,4]` with raw type `5` and selector `7`, Wooden Desk furniture `3` at `[2,4]`, `[3,4]`, `[6,4]`, Trash Can `12` at `[8,5]`, Old Printer `26` at `[8,6]`, Calendar `56` at `[2,7]`, and three initial Staff at the source-backed spawn cell/world coordinate. The stable direction, action, frame, and alpha are not guessed.

## Required constraints honored

No subagents, emulator, ADB, live APK, server, network/browser automation, new screenshots, full starter-room render, screenshot-derived numeric tuning, MapChip change, V6 semantics change, V7 alpha change, production-renderer change, or V8 execution was used. Source roots remain read-only. The prior `first-visible-starter` ledgers remain frozen; this recovery is recorded in the separate `first-visible-transition` evidence directory.

## Final verification

- Focused V5–V7/MapChip/reintegration Vitest: `5/5` files, `124/124` tests.
- Full Vitest: `45/45` files, `284/284` tests.
- Typecheck: pass.
- Production build: pass with the existing non-blocking Vite large-chunk warning.
- Python/static gates: `53/53`.
- JSON validation: `334` files pass; Python AST validation: `119` files pass; `git diff --check`: pass.
- No server was started, so no development-process cleanup was required.

## Evidence

- [Checkpoint ledger](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/checkpoint-ledger.json)
- [First-visible stable manifest](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/first-visible-stable-manifest.json)
- [FS unknown closure](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/fs-unknown-closure.json)
- [Preview decision](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/previews/README.md)
