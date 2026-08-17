# Original Work Assignment Flow

Status: `CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER`

The original path is data-defined and autonomous: `Staff.Init` binds `StaffData.jobId_`/`skill_`; `Room.AddStaff` assigns a desk owner and optionally starts planning; `Staff.Update` dispatches the living state; and `Staff.UpdateWork` autonomously chooses typing, equipment, talk, or sleep. No recovered `Staff.UpdateWork` input is a dashboard task object.

The extracted source exposes `SetJobId`, `ChangeSkill`, and `EvolveJob`, but exact source call-site search recovers only their definitions. Forms read/display job data, but no reliable UI mutation caller is promoted. The original UI is therefore `CUT_LATER`, and future dashboard policy is `PRODUCT_POLICY_PENDING`.

Evidence: [`original-work-assignment-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/original-work-assignment-contract.json), [`original-task-to-living-core-boundary.json`](../../../knowledge/fixtures/accepted/living-core-closure/original-task-to-living-core-boundary.json ).
