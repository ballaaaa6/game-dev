# First-visible Staff state

Status: spawn `SOURCE_BACKED`; stable display pose `SOURCE_LIMITED`.

The pinned NewGame input creates three Staff entries. `Room.AddStaff` derives the door position from cell `[8,4]`, producing world coordinate `[280,-31]`, reserves the door, assigns a desk, sets the room reference and speed, and writes native `alpha_=0`. The pinned actor selectors are `86`, `87`, and `88`.

The readable source does not close the first stable action, direction, frame, or alpha after update/tutorial progression. The prior V6 `wait`/right/frame-0/alpha-255 display fixture remains a presentation compatibility policy; it must not be treated as a native rewrite of the AddStaff spawn state.

Evidence: [first-visible-staff-state.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-staff-state.json).
