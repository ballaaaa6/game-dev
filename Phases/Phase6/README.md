# Phase 6 — Task system และ dashboard interaction

สถานะ: `complete_with_known_limitations`

Wave 6 W6-C0–C7 และ W6.1 สร้าง deterministic task system และ dashboard integration บน Wave 5 runtime
โดยไม่เชื่อม AI model และไม่ยก task state ขึ้นเป็น legacy gameplay semantics

สิ่งที่ทำแล้ว:

- task schema, priority queue และ lifecycle `queued`/`working`/`blocked`/`done`
- explicit assignment rule แบบหนึ่ง active task ต่อ Agent
- Agent task projection ผ่าน public Wave 5 runtime adapter
- durable task notification และ append-only activity log
- repository boundary แบบ backend-replaceable พร้อม versioned envelope, migration และ optimistic conflict handling
- localStorage repository พร้อม memory-only fallback และ visible persistence status
- dashboard create/filter/detail/assign/start/block/resume/complete/reset/export/import
- final hardening: strict snapshot validation, repository envelope validation, visible degraded state,
  failed-reload memory preservation, lifecycle button guards, task description และ notification dismiss
- Agent focus แบบ highlight/dim adapter policy
- contract artifacts, deterministic fixtures, unit tests และ fresh browser interaction report

ผล validation ล่าสุด:

- Wave 6 runtime `18/18` scenarios และ Phase 6 contract `11/11`
- Wave 5 runtime `10/10`, Phase 5 contract `17/17`, Phase 4 `107/107`, Phase 2 `5/5`
- browser smoke ผ่าน create/assign/start/block/resume/complete, persistence reload, notification dismiss,
  reset และ lifecycle guard; console error/warning `0`

ข้อจำกัดที่ยังเปิด:

- persistence เป็น browser-local ยังไม่มี backend หรือ multi-user sync
- permission เป็น operator policy และยังไม่มี authentication
- auto-assignment/AI decision อยู่ Phase 7
- notification text เป็น web adapter text
- focus เป็น highlight ไม่ใช่ recovered legacy camera transform
- backend/auth/multi-user sync ยังไม่อยู่ใน scope; local identity และ permission policy เป็น explicit adapter policy

ไฟล์หลักอยู่ใน `runtime/`, `tests/`, `tools/`, `artifacts/` และ `docs/`
