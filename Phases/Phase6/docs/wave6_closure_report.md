# Wave 6 closure report

สถานะ: `complete_with_known_limitations`

## Implemented

- deterministic `TaskSystem` สำหรับ task create/list/assign/unassign/start/block/resume/complete
- priority queue และ one-active-task-per-agent rule
- Agent task projection ผ่าน `OfficeRuntime.setAgentTaskProjection`
- named Phase 6 activity events และ runtime event mirror
- durable task notifications แยกจาก Wave 5 raw-graph notifications
- repository boundary แบบ backend-replaceable, versioned envelope และ migration จาก snapshot เดิม
- optimistic revision conflict detection พร้อม `reloadFromRepository()`
- explicit local permission policy, JSON import/export และ visible persistence status
- dashboard create/filter/detail/assignment/lifecycle/notification/activity controls
- Agent focus เป็น canvas highlight/dim adapter policy
- final hardening: strict task/notification/activity snapshot validation, repository envelope validation,
  localStorage unavailable errors, failed-reload memory preservation, lifecycle button guards,
  task description และ notification dismiss UI

## Validation target

- Wave 6 task system: 18 scenarios
- Phase 6 contract: 11 tests
- Wave 5 runtime: 10 scenarios
- Wave 5 Python/visual contract: 17 tests
- Phase 4 and Phase 2 regression: retain existing passing baseline
- browser smoke: boot, create, assign, start, block, resume, complete, refresh and reset
- final browser smoke: lifecycle guards, task description, notification dismiss, JSON import, persistence reload and reset

## Known limitations

- repository implementation ยังเป็น browser-local ผ่าน localStorage; ยังไม่มี backend หรือ multi-user sync
- permission เป็น explicit local policy; ยังไม่มี authentication หรือ server-side authorization
- auto-assignment และ AI decision อยู่ Phase 7
- notification text เป็น web adapter text
- focus เป็น highlight ไม่ใช่ recovered legacy camera transform
- `legacy_equivalence=false`
