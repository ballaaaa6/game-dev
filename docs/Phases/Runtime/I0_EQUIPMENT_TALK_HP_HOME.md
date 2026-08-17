# I0 Equipment, Talk, HP, and Home

Equipment selection keeps owner, active users, and reserved users distinct. `GetUsersNum` reads reserved users only. GOTO_EQUIPMENT reserves the target, arrival enters USE_EQUIPMENT, completion releases the reservation, adds FurnitureData recovery stock only when HP is below max, and returns through GotoDesk.

Talk preserves candidate guards, bilateral reservation and colleague relations, TO_STAFF → TO_BACK_OF_CHAIR → TO_STAND_TALKING, frame-20/frame-70 bubble events, the frame-110 Lib gauge draw, frame-130 cleanup, and desk return. Bubble events do not mutate the renderer.

HP is computed from generated StaffData/JobData formulas and neutral source fixtures. Staff:0/Job:4 at level 0 evaluates to max HP 108. Low HP uses the door/home path, home recovery calls RecoverHp(1), and the 40% threshold returns through the valid desk. Equipment recovery stock uses the 20-frame delay and frame-modulo cadence.
