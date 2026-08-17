# Staff State Machine

The numeric state labels are source-backed and the pinned dump supplies the native method addresses. The complete dispatcher is not promoted because the decompiled `Staff.Update` and `OnArriveGoal` contain unresolved indirect jumps.

## States

- `STATE_NORMAL=0`
- `STATE_MEETING=1`
- `STATE_MOVE=2`
- `STATE_SIT_DOWN=3`
- `STATE_WORK=4`
- `STATE_USE_EQUIPMENT=5`
- `STATE_TALK=6`
- `STATE_INVITE_TO_TALK=7`
- `STATE_FLY_AWAY=8`
- `STATE_WAIT=9`
- `STATE_WANDER=10`
- `STATE_WAIT_BACK_OF_DOOR=11`
- `STATE_DEVELOP=12`
- `STATE_STAY_HOME=13`

## Closed direct transitions

- `GetHpRatio() <= 5` clears the route and writes state `STATE_MOVE` with `MOVE_MODE_GO_TO_DOOR` unless already moving or staying home.
- `UpdateStayHome` calls `RecoverHp(1)` and, at `>=40%`, reserves the door and writes `STATE_WAIT_BACK_OF_DOOR` plus `MOVE_MODE_GOTO_DESK`.
- `GotoEquip` selects type 1 or 4, requires `GetUsersNum() <= 0`, reserves the chip, and writes `STATE_MOVE/MOVE_MODE_GOTO_EQUIPMENT`.
- `GotoTalk` selects one random colleague, checks sitting/work/flags/standing-cell guards, and writes bilateral talk flags and `STATE_MOVE/MOVE_MODE_TO_STAFF`.
- Talk at frame `>=130` clears talk flags and colleague identity, then calls `GotoDesk`.
- Equipment or desk destruction and colleague removal have explicit cleanup fallbacks.

## Source limits

The exact per-state indirect handler table, exact `OnArriveGoal` mapping, and exact modulo cadence are unknown. Numeric labels are retained as labels and are not treated as a replacement for the native body.
