# Starter Staff transition

## Spawn

`Room.AddStaff` is the recovered bootstrap insertion point (`RVA 0x12CEB2C`). The frozen starter evidence records Staff `0`, `1`, and `2` at cell `[8,4]`, world coordinate `[280,-31]`, with bootstrap alpha `0`.

## Event 0

The event-0 `SCR_TALK` handler (`RVA 0x1217B50`) selects a staff context and calls `SubForm.CreateStaffTalk` (`RVA 0x11CF310`). `CreateStaffTalk` builds a talk subform; the recovered path does not write Staff direction, action, animation frame, or alpha. `SCR_DELAY(10)` also has no Staff write.

## Stable pose status

The available static evidence does not prove the stable direction, action, frame, or alpha for Staff `0` through `2`, nor does it prove that no later automatic event mutates those fields before the stable display. Those values remain `unknown` in the partial manifest. Assigning a pose from a screenshot would violate the recovery constraints.

The blocking contract is [starter-staff-transition.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/starter-staff-transition.json). Full starter-room reintegration and V8 remain stopped.
