# Dashboard Behavior Boundary

The dashboard may select or display StaffData, JobData, SkillData, FurnitureData, and explicit task-assignment inputs. It may remain a consumer of HP and parameter fields. EventData constants are event vocabulary, not authority for the autonomous Staff tick.

The autonomous authority remains Room.Update -> Staff.Update/ObjChip.Update, Staff state/move/flag fields, ObjChip reservations, FurnitureData recovery/passMap/type fields, and the native Astar route contract. Dashboard work must not replace these paths or infer behavior from sprites/names.

This phase performs no visual correction, no V8, no production renderer change, and no MapChip change. The full preserve/forbid list is in `dashboard-preservation-boundary.json`.
