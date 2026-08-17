# Starter room mutations

## Bootstrap path

`AppData.NewGame` (`sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs:12996`, native `RVA 0x1263A70`) is the source-backed bootstrap boundary. The recovered native path reaches `InitGameData` (`0x12628EC`), `Player.NewGame` (`0x12ABAC4`), `EventData.NewGame` (`0x1216C98`), the 14x14 floor-0 `Room` constructor (`0x12CB050`), desk placement (`0x12CEFC8`), starter equipment placement, and `Room.AddStaff` (`0x12CEB2C`) from `sources/raw/1_Click_CSharp_Code update/game/Room.cs`.

The retained bootstrap state is:

- Floor raw `5`, wall raw `6`, `wall_00.png`, selector `5`.
- Door at `[8,4]`, raw type `5`, selector `7`, `door_01.png`/`door_02.png`, frame `0`, installed `1`.
- Wooden Desk raw furniture `3` at `[2,4]`, `[3,4]`, `[6,4]`, with raw directions `3`, `2`, `2`.
- Trash Can raw furniture `12` at `[8,5]`, Old Printer raw furniture `26` at `[8,6]`, and Calendar raw furniture `56` at `[2,7]`.
- Three initial Staff objects at the source-backed spawn cell/world coordinate.

These are inherited from the frozen first-visible-starter evidence and are not replaced by a screenshot-derived correction.

## Event path

Event `0` runs `SCR_TALK(0,0)` and `SCR_DELAY(10)`. The talk handler creates a staff-talk form; the delay handler only writes `DelayEvent.delayFrame_`. The recovered event-0 path contains no room, furniture, wall, door, or workstation/equipment write. Therefore event `0` does not alter the bootstrap manifest.

The unresolved later automatic-event catalog may contain mutation opcodes and may affect persistence before the first stable frame. That ordering is a blocking source limitation. The recovery therefore records bootstrap and event-0 no-mutation separately and does not claim the final post-tutorial room.

Evidence: [starter-room-mutation-timeline.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/starter-room-mutation-timeline.json), [starter-wall-door-transition.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/starter-wall-door-transition.json), and [first-visible-stable-manifest.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/first-visible-stable-manifest.json).
