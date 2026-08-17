# Gameplay Cut List

The visual port is not a simulation port. The cut list removes behavior whose purpose is economy, progression, interaction, scheduling, or planning while preserving source-derived state that is directly observable in a scene.

| Area | Original boundary | Disposition | Visual dependency retained |
|---|---|---|---|
| Economy and money | `AppData` balances, purchase/build cost, income, price changes, and resource accounting | `CUT_GAMEPLAY` | Furniture/room selectors already present in scene data. |
| Progression and unlocks | Unlock checks, rank/date gates, development completion, research progression | `CUT_GAMEPLAY` | Only an explicit source-derived visual ID may remain. |
| Furniture interaction | `ObjChip.StartAction`, use/reservation/action timers, staff-use bookkeeping | `CUT_GAMEPLAY` | `ObjChip` direction, parent, frame, and pass-map fields remain for visible placement. |
| Furniture/object placement | `ObjChip.PlaceObj`, placement selection, parent/child topology, `GetStandingPositions` | `VISUAL_EXTRACT` | Keep final object coordinates, direction, multi-cell parent, and visible standing positions. |
| Collision/passability | `ObjChip.IsPassable` and `FurnitureData.passMap_` | `VISUAL_EXTRACT` | Retain only when it determines a visible placement or the captured staff position. |
| Staff jobs and scheduling | job assignment, room work, meetings, development tasks, reservation queues | `CUT_GAMEPLAY` | `StaffData` identity and proven visible action/SEB selectors. |
| Staff movement planning | `Staff.SearchRoute`, route scoring, `Astar` search and node bookkeeping | `CUT_GAMEPLAY` | A captured/source-derived position or a later minimal movement adapter; do not import the planner by default. |
| Character animation | `Staff.AdvanceSebFrame`, action/direction/frame state | `NEEDS_NATIVE_TRACE` | Visible frame progression, loop, direction, scale, alpha, and transition only after native/fixture proof. |
| Room simulation | `Room.Update` branches that mutate economy, jobs, interaction, or timers | `CUT_GAMEPLAY` | A visual update hook may be extracted after the draw/animation contract is known. |
| Room construction | `Room.InitMapChips`, `InitObjChips`, `SetupBigChipsParent`, `PlaceDoor`, `InitStaffs` | `VISUAL_EXTRACT` | Grid topology, source IDs, parent/door relationships, and draw order. |
| Save/load gameplay | save records, migration, continue/new-game state, persistence side effects | `CUT_GAMEPLAY` | Load only the immutable visual fixture/catalogue needed for a scene. |
| Combat, skills, effects | combat resolution, damage, skill rules, effect timers | `CUT_GAMEPLAY` | A proven effect SEB/resource may be added as a visual fixture later. |
| Dialogues and fukidashi logic | conversation selection, text progression, social state | `CUT_GAMEPLAY` | A captured fukidashi asset may be rendered only as an explicit visual fixture. |
| Camera behavior | `Camera` target/position/base coordinate methods | `KEEP_EXACT` | Camera transform and screen projection remain visible behavior. |
| Lifecycle | `Main`/`GameForm` create/update/draw host | `PORT_BACKEND` | Preserve the outer visible ordering and dimensions; replace Unity services. |

## Retention rule

“Cut” does not authorize deleting source evidence or changing the current runtime during V0. It means the later port must not make the simulation a prerequisite for rendering. Any retained gameplay-looking field must have a direct visual consumer recorded in `visual-dependency-graph.json` or `visual-data-flow.json`.
