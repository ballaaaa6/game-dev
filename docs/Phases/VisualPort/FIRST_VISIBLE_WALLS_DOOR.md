# First-visible walls and door

Status: bootstrap contracts `SOURCE_BACKED`; final first-visible selection `SOURCE_LIMITED`.

For room 0, the bootstrap wall family is raw selector `6`, `wall_00.png`, and SEB selector `5` / `wall_00.seb`. The horizontal frame-0 cells are `[1,1]` through `[8,1]`. The vertical frame-1 cells are `[8,1]`, `[8,2]`, `[8,3]`, `[8,5]`, `[8,6]`, `[8,7]`, and `[8,8]`; the door cell is excluded from the vertical wall set. The native wall coordinate formula is preserved from the ObjChip draw contract.

The bootstrap door is raw type `5` at `[8,4]`, installed with `FurnitureData=null`. Its room image selector is `7` / `door_01.png`; its SEB record is selector `6` / `door_02.seb`, frame `0`, image id `7`. The PNG selector and SEB selector are separate roles and are not renamed from visual appearance.

No later tutorial/event wall or door mutation is source-proven. These contracts must not be promoted to the final first-visible manifest until the state transition is closed.

Evidence: [first-visible-wall-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-wall-contract.json) and [first-visible-door-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-door-contract.json).
