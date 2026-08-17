# Work Interruption and Resume

Status: `CLOSED_ORIGINAL_RESUME_PATH`

Equipment and talk are explicit interruptions from ordinary work. Equipment uses reservations, dispatches through the native arrival table, completes through `OnUseComplate`, and returns through `GotoDesk`. Talk uses reserved-talk flags and the TO_STAFF/TO_BACK_OF_CHAIR/TO_STAND_TALKING modes, then returns to the owned desk. Low HP routes through the door to stay-home recovery; at HP ratio 40 or above, the staff reserves the door and returns toward the desk. Desk destruction/floor removal clears ownership before any new desk resolution.

Evidence: [`work-interruption-resume-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/work-interruption-resume-contract.json ).
