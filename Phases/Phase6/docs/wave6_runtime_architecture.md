# Wave 6 — Task system runtime architecture

สถานะ: `complete_with_known_limitations`

Wave 6 เป็น product task layer ใหม่ที่ต่อบน deterministic Wave 5 runtime โดยไม่อ้างว่า
task status เป็น legacy gameplay state และยังคง `legacy_equivalence=false`

## Boundaries

- `TaskSystem` เป็นเจ้าของ task, assignment, lifecycle, durable notification และ task activity log
- `OfficeRuntime` เป็นเจ้าของ Agent movement, seat, bubble, raw runtime event และ canvas draw state
- Agent `taskId`/`taskStatus` เป็น projection สำหรับ UI ไม่ใช่ raw legacy field mapping
- Wave 5 notification ที่มี `graph_id` และ logical expiry ไม่ถูกนำมาใช้เป็น task notification
- task notification อยู่ใน versioned task snapshot และไม่มี automatic expiry

## Runtime flow

1. UI เรียก `TaskSystem` mutation API
2. TaskSystem validate transition และ assignment rule
3. TaskSystem เปลี่ยน task state ด้วย logical tick
4. TaskSystem update Agent task projection ผ่าน public `OfficeRuntime` adapter
5. TaskSystem append durable activity record
6. TaskSystem mirror `task.*` event ไปยัง Wave 5 runtime event log
7. TaskSystem persist snapshot ผ่าน repository adapter และ optimistic revision
8. UI render queue, detail, notification, activity และ Agent focus

## Persistence

TaskSystem ไม่ผูกกับ storage โดยตรง แต่เรียก repository interface (`load`, `save`, `clear`)
ค่าเริ่มต้นคือ `LocalStorageTaskRepository` ที่ใช้ key `phase6.task_state.v1` และ fallback
เป็น memory-only หาก storage ใช้งานไม่ได้หรือ snapshot เสียหาย

repository เก็บ envelope schema `wave6-task-repository-v1` ซึ่งมี `revision`, `snapshot`
และ `migrated_from`; snapshot มี schema version `wave6-task-state-v1` และเก็บ tasks,
notifications, activity log และ deterministic sequence counters โดยไม่ใช้ wall-clock timestamp

snapshot ตรงจาก Wave 6.0 จะถูก migrate เป็น envelope revision `0` โดยไม่ทิ้ง task state
การเขียนครั้งถัดไปจะเพิ่ม revision เป็น `1`; ถ้า expected revision ไม่ตรง repository จะรายงาน
`conflict_needs_reload` เพื่อให้ผู้ใช้ reload ก่อนเขียนทับ state อื่น

## Permission และ interchange

`DefaultTaskPermissionPolicy` แยก operator actions ออกจาก agent actions อย่าง explicit
และจำกัด agent ให้ทำ lifecycle เฉพาะ task ที่ assign ให้ตนเอง ส่วน authentication, backend
authority และ multi-user identity ยังอยู่นอก scope

TaskSystem มี `exportData()`/`importData()` ใน schema `wave6-task-export-v1` และ dashboard
แสดง persistence status พร้อม revision รวมถึงปุ่ม reload saved เพื่อแก้ conflict แบบโปร่งใส

## Focus policy

Dashboard focus จะ highlight Agent ที่เป็น assignee และ dim actor อื่นบน canvas
ยังไม่เปลี่ยน world/camera transform เพราะ Wave 5 ยังไม่มีหลักฐาน universal camera semantics
