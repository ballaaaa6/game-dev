# Starter event interpreter

## Event selection

The source is `sources/raw/1_Click_CSharp_Code update/data/EventData.cs` (`Load` line `462`, `NewGame` line `476`, `ExeAutoEvent` line `481`, `StartEvent` line `533`, `ExeEvent` line `752`). The event asset is `knowledge/fixtures/accepted/asset_guide_20260813/01_GAME_PACKS/xls/English.lproj/event.txt`.

Event `0` (`EV_FIRST_TALK`) is the recovered login-term starter event. Its parsed row is:

```text
id=0 oneLimit=0 term=[[3,1,4]] exec=[[0,0],[1,10]]
```

`3` is `TERM_LOGIN`; `0` and `1` are `SCR_TALK` and `SCR_DELAY`. `EventData.ExeAutoEvent(true)` evaluates the one-limit/execution count and term predicate, then pushes `DelayEvent(0,-99,-99,repParam,value)` into `Player.delayEventStock_`.

The complete automatic catalog order after event `0` is not recoverable from the allowed static evidence. No later event id is promoted in this contract.

## Native interpreter

`EventData.ExeEvent(DelayEvent,bool)` is at native `RVA 0x121747C`. Its `DelayEvent` fields are `eventID_ +0x10`, `exeLine_ +0x14`, `active_ +0x18`, `delayFrame_ +0x1C`, `charType_ +0x20`, `charIndex_ +0x24`, `repParam_ +0x28`, and `value_ +0x30`. The interpreter increments `exeLine_` before dispatch and decrements `delayFrame_` when the delay gate is active.

The opcode jump table is at `0x6363A0` in the pinned binary:

| Opcode | Name | Handler RVA |
| ---: | --- | --- |
| 0 | `SCR_TALK` | `0x1217B50` |
| 1 | `SCR_DELAY` | `0x1217ACC` |
| 2 | `SCR_NEWS` | `0x1217C90` |
| 3 | `SCR_EV_MSG` | `0x1217E50` |
| 4 | `SCR_GET_ITEM` | `0x12176B4` |
| 5 | `SCR_GET_AWARD` | `0x12176C4` |
| 6 | `SCR_DL_COMP` | `0x121785C` |
| 7 | `SCR_NEW_PLATFORM` | `0x12178B4` |
| 8 | `SCR_PRIZE_FIND` | `0x1217D38` |
| 9 | `SCR_ADD_MENU` | `0x1217A5C` |
| 10 | `SCR_GAME_AWARD_FIND` | `0x1217968` |
| 11 | `SCR_GAME_AWARD_SELECT` | `0x121787C` |
| 12 | `SCR_GET_MONEY` | `0x1217F8C` |
| 13 | `SCR_GET_COIN` | `0x1217AE4` |
| 14 | `SCR_SUB_FORM` | `0x1217A98` |
| 15 | `SCR_SPECIAL_COMMAND` | `0x1217EC8` |

For event `0`, `SCR_TALK(0,0)` calls `SubForm.CreateStaffTalk` (`RVA 0x11CF310`), while `SCR_DELAY(10)` stores `10` in `delayFrame_`. After all rows are consumed, `active_` becomes `1`; `AppData.ExeEvent(int)` (`RVA 0x1261520`) removes the completed delay event and handles queued forms. Event `0` has no explicit end opcode and no room/furniture/staff-pose mutation.

See [starter-event-selection.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/starter-event-selection.json) and [starter-event-command-map.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/starter-event-command-map.json).
