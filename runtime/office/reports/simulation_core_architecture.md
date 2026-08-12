# Simulation Core Architecture

## สถานะ

เอกสารนี้สรุป implementation baseline ของ C#-first clean reconstruction รอบ Simulation Core และ continuous dashboard ที่ตรวจสอบแล้วใน workspace ปัจจุบัน ตัว runtime ที่อธิบายอยู่เป็น JavaScript adapter ไม่ใช่การ execute decompiled C# หรือการอ้างว่า legacy game equivalence สมบูรณ์

## Ownership boundary

```text
C# / reverse-engineering evidence
        │  status + provenance projection เท่านั้น
        ▼
semantic_inventory_runtime.json
        │
        ▼
dashboard task system ── task.projection.update ──► SimulationCore
                                                        │
                                   commands ────────────┤
                                                        ▼
                                      canonical state / event log / digest
                                                        │
                                                        ▼
                              OfficeRuntime compatibility facade
                                                        │
                                                        ▼
                                      renderer + dashboard diagnostics
```

`SimulationCore` เป็น state owner เดียวของ schema `simulation-core-v1` การเปลี่ยน state ผ่าน command reducer และ `advance()` เท่านั้น `OfficeRuntime` ยัง expose `agents`, `bubbles`, `notifications`, `events.records` และ provider APIs เดิมเป็น read-only compatibility projections เพื่อให้ renderer และ task system เดิมย้ายได้โดยไม่สร้าง state ซ้ำ

TaskSystem ยังคงเป็นเจ้าของ task lifecycle, repository revision, permission และ notification ของ task เมื่อ assignment/start/complete เปลี่ยน จะส่ง projection เข้า core เพื่อให้ actor activity ใน canonical snapshot สอดคล้องกัน Dashboard ไม่ mutate core state โดยตรง

## Canonical state and command/event contract

Root snapshot ประกอบด้วย `schema_version`, `simulation_id`, `clock`, `scene`, `actors`, `bubbles`, `notifications`, `task_projection`, `event_log`, `evidence` และ `legacy_equivalence=false` Actor แยก identity, adapter state, raw legacy values, position/movement, activity, interaction, animation และ provenance

คำสั่งที่รองรับในรอบนี้:

- `actor.spawn`
- `actor.move.request`
- `actor.seat.occupy` / `actor.seat.release`
- `dialogue.request`
- `notification.create`
- `task.projection.update`
- `legacy.event.record`

ทุก commit clone draft, validate canonical state, append monotonic event sequence และ notify subscribers หลัง commit เท่านั้น Invalid command ไม่เขียนทับ live state ผลของ `snapshot()` และ `digest()` จึง deterministic สำหรับ input เดียวกัน

## Tick order

```text
ContinuousScheduler (160 ms)
  → OfficeRuntime.step(1)
  → SimulationCore.advance(1)
  → clock.tick += 1
  → actor movement + collision decision
  → bubble/notification expiry
  → schema validation
  → event append + subscriber notification
  → dashboard render(snapshot)
```

Scheduler เป็น wall-clock driver ของ UI เท่านั้น มี `start()` แบบ idempotent และจับ exception จาก tick ส่งไปยัง error handler ของหน้าเว็บ ไม่มีปุ่ม stop/pause หรือ speed multiplier ใน DOM และไม่มีการสร้าง long-running scheduler ใน tests; lifecycle test ใช้ injected timers

## Provenance policy

Dashboard โหลด `runtime/office/evidence/semantic_inventory_runtime.json` ซึ่งสร้างจาก inventory claims และไม่มี source body C# ข้อมูลที่ยัง `raw_only`, `structural_only` หรือ `assembly_fallback_bounded_slice_required` แสดงเป็น unresolved/status counts เท่านั้น ไม่ถูกแปลงเป็น semantic name

รอบนี้ยังไม่ promote ความหมายของ `HumanMode`, `HumanState`, `HumanAnime`, `EventMode` และ numeric message/graph labels ข้อจำกัดนี้เป็น intentional evidence boundary ไม่ใช่ข้อมูลที่หายไปจาก UI โดยเงียบ ๆ

## Non-equivalence and next boundary

- runtime เป็น deterministic adapter baseline ไม่ใช่เกมเต็ม
- C# corpus เป็น decompiler evidence และยังไม่มี compile verdict
- animation profile, furniture placement/crop บางส่วน และ world/camera transform ยังเป็น adapter-defined หรือ unresolved
- ยังไม่มี LLM, backend, auth, multi-user sync หรือ real task backend
- scheduler จำลองการเดินของ simulation ตาม logical tick แต่ยังไม่ใช่การพิสูจน์ frame/timing equivalence กับเกม legacy

## Verification observed

คำสั่งที่ผ่านใน Task 7:

```powershell
node --check runtime/office/app/continuous_scheduler.js
node --check runtime/office/app/app.js
node runtime/office/tests/test_continuous_scheduler.js
node runtime/office/tests/test_wave5_runtime.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
```

ผลที่สังเกตได้: scheduler `2` scenarios, office runtime `11` scenarios, Wave 5 Python contract `20/20`; browser smoke พบ READY/tick เดินเองจาก `96` เป็น `101` ในประมาณ `700ms`, canvas `600x800`, diagnostics แสดง `simulation-core-v1` และ evidence, task create/assign ผ่าน และ browser console ไม่มี error/warning หลังทดสอบ
