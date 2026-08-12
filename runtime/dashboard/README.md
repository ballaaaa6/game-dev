# Agent Dashboard Runtime

Deterministic task system และ dashboard interaction ที่ทำงานบน office runtime โดยยังไม่เชื่อม AI model, backend หรือระบบงานจริง

## โครงสร้าง

- `app/` — task system, repository adapter และ dashboard UI
- `evidence/` — contract, fixture, manifest และ interaction report
- `reports/` — runtime architecture และ closure reports
- `tests/` — Node/Python contract tests
- `tools/` — manifest builder

## สิ่งที่ runtime รองรับ

- task lifecycle `queued` / `working` / `blocked` / `done`
- assignment rule แบบหนึ่ง active task ต่อ Agent
- durable notification และ append-only activity log
- localStorage repository พร้อม memory fallback และ visible persistence status
- create/filter/detail/assign/start/block/resume/complete/reset/export/import
- strict snapshot validation, migration และ optimistic conflict handling

## ตรวจสอบจาก workspace root

```powershell
node --check runtime/dashboard/app/task_system.js
node runtime/dashboard/tests/test_wave6_task_system.js
python -m unittest runtime/dashboard/tests/test_wave6_contract.py -v
```

ข้อจำกัดปัจจุบัน: persistence ยังเป็น browser-local, permission ยังเป็น operator policy และ auto-assignment/AI decision ถูกเก็บไว้เป็นงานในอนาคต
