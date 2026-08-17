# V6 human actions and SEB selectors

The `human-staff-v1` capability profile is the selector authority for the bounded display surface. V6 resolves an action through `selector_by_direction` and retains the original numeric SEB selector.

| Action | Right | Left | Up | Down |
| --- | ---: | ---: | ---: | ---: |
| wait | 10 | 11 | 12 | 13 |
| move | 1 | 2 | 3 | 4 |
| typing | 23 | 24 | 25 | 26 |

Talk uses the source-backed typing action. Work, equipment, sit-down, meeting, invite-to-talk, wander, and stay-home preserve their explicit capability fallbacks. `fly_away` remains deferred with no selector; unsupported actions are never hidden behind a new animation.

The raw direction path preserves the native reverse table. A raw ObjChip direction is converted through the closed native reverse mapping before the directional selector is selected.
