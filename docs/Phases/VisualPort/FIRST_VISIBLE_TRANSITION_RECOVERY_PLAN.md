# First-Visible Transition Recovery Plan

## Scope

Recover the source-backed transition from the new-game form through tutorial/event startup to the first stable main-display state. This phase is static-only and ends before full starter-room reintegration and V8. Frozen V1–V3, MapChip, V6 staff, V7 alpha, and production-renderer contracts remain unchanged.

## Recovery targets

| Target | Source evidence | Native evidence | Expected transition evidence | Status |
| --- | --- | --- | --- | --- |
| `AppData.NewGame(string,int,FastVector)` | `sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs`; raw copy line 14063 | `0x1263A70` | Creates the 14x14 floor-0 room, places desks, adds initial staff, and places flagged starter equipment | Bootstrap closed; post-tutorial state source-limited |
| `TitleForm.Update()` start-game branch | `sources/raw/1_Click_CSharp_Code update/form/TitleForm.cs` | `0x1207E44`; direct `NewGame` call at `0x01208248` | Establishes the caller and title fade/state handoff | Closed native |
| `SubForm.Init()` dispatch to `InitStartGame()` | `sources/raw/1_Click_CSharp_Code update/form/SubForm.cs` | `InitStartGame` `0x112A27C`; dispatch site `0x0111EF34` | Establishes start-game form initialization and callback state | Closed native |
| `SubForm.Update()` dispatch to `UpdateStartGame()` | `sources/raw/1_Click_CSharp_Code update/form/SubForm.cs` | `UpdateStartGame` `0x119EF6C`; dispatch site `0x01182794` | Establishes the selection/submit state machine | Closed native |
| `EventData.NewGame()`, `StartEvent()`, and `ExeEvent()` | `sources/raw/1_Click_CSharp_Code update/data/EventData.cs` and event data files | `0x1216C98`, `0x1217278`, `0x121747C` | Identifies event-0 selection, command schema, queueing, and interpreter entry | Event 0 closed; later catalog source-limited |
| `AppData.ExeEvent(int)` and player event queues | `sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs`, `.../game/Player.cs` | `AppData.ExeEvent` `0x1261520`; player queue fields in native | Proves per-tick event dispatch and the event-work gate | Draw gate closed; full queue order source-limited |
| `GameForm.Update()` and `DrawGameScreen()` | `sources/raw/1_Click_CSharp_Code update/form/GameForm.cs` | `0x10FE56C`, `0x110422C` | Defines the first stable `main_display` draw-entry predicate | Draw entry closed; full stable frame source-limited |
| Room/staff mutation methods | `.../game/Room.cs`, `.../game/Staff.cs`, `.../game/Player.cs` | Room constructor `0x12CB050`, `AddStaff` `0x12CEB2C`, `PlaceDesk` `0x12CEFC8` | Records only source/native-proven mutations; no screenshot-derived replacement | Bootstrap/event-0 closed; later mutations and pose open |

## Acceptance criteria

1. The direct new-game caller, form handoff, event selection, command interpreter, and first stable display boundary are each tied to source and/or native evidence with explicit unresolved fields.
2. A sequential transition timeline and manifest distinguish bootstrap objects from post-tutorial mutations; unknowns remain unknown.
3. Isolated previews are generated only if the stable boundary is source-closed. It is not source-closed here, so no preview is generated. Full starter-room reintegration is not performed.
4. Baseline and final V1–V7/MapChip, Vitest, typecheck, build, static/evidence, JSON, and diff checks pass; the exact source-limited blocker is recorded.
5. No server, emulator, ADB, live APK, network/browser automation, subagents, new screenshots, or V8 execution is used.
