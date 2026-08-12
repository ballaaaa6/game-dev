# Office Runtime

Deterministic web adapter ที่จำลอง office state, scene, actor rendering และ event lifecycle จากหลักฐานที่ตรวจสอบแล้ว โดยยังไม่เชื่อม LLM หรือระบบงานจริง โดย `SimulationCore` เป็น state owner เดียว และ dashboard ขับ logical tick ผ่าน scheduler ภายใน

## โครงสร้าง

- `app/` — canonical schema/core, compatibility facade, continuous scheduler, browser runtime และ HTML/CSS
- `evidence/` — contract, fixture, manifest และ visual QA artifact
- `reports/` — runtime architecture, closure และ investigation reports
- `tests/` — Node/Python contract tests
- `tools/` — manifest และ evidence builders

Source asset เดิมยังอยู่ใน source roots ที่ root ของ workspace; runtime อ้างอิงกลับไปแบบ read-only

## สิ่งที่ runtime รองรับ

- logical tick และ event log แบบ deterministic
- canonical snapshot/digest/subscriber จาก `SimulationCore` โดยไม่สร้าง state owner ซ้ำใน facade
- scene, furniture, actor body/face และ bounded draw commands
- locale, dialogue, bubble, notification และ cleanup lifecycle
- task projection bridge สำหรับ dashboard โดยไม่ผูกกับ AI model
- semantic evidence/provenance projection แบบ source-free สำหรับ diagnostics
- continuous browser tick ที่เริ่มเองทุก `160ms`; ไม่มี Play/Pause/Step/Reset หรือ speed control ของ simulation
- browser smoke path สำหรับ floor, furniture, actors, task controls และ diagnostics

## Ownership boundary

`SimulationCore` รับ command แล้วลดรูปเป็น canonical state, event log และ deterministic digest ส่วน `OfficeRuntime` ทำหน้าที่เป็น compatibility facade ให้ provider/renderer เดิมอ่าน projection จาก core เท่านั้น Dashboard จัดการ task repository/permission และส่ง task projection กลับเข้า core แต่ไม่แก้ canonical state โดยตรง

ลำดับ tick คือ: scheduler เรียก `runtime.step(1)` → core เพิ่ม logical tick → ประมวลผล movement/collision และ expiry → ตรวจ state → append event/notify subscribers → dashboard render snapshot ล่าสุด

## Evidence policy

Browser โหลดเฉพาะ `runtime/office/evidence/semantic_inventory_runtime.json` ซึ่งเป็น status/provenance projection ที่ไม่มี C# source body การแสดง `HumanMode`, `HumanState`, `HumanAnime`, `EventMode` และ numeric message/graph values จึงยังคงเป็น raw/unknown ตามหลักฐาน ไม่ promote เป็น semantic name เอง

## ตรวจสอบจาก workspace root

```powershell
node --check runtime/office/app/runtime.js
node --check runtime/office/app/continuous_scheduler.js
node --check runtime/office/app/app.js
node runtime/office/tests/test_simulation_schema.js
node runtime/office/tests/test_simulation_core.js
node runtime/office/tests/test_continuous_scheduler.js
node runtime/office/tests/test_wave5_runtime.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
```

ผลรอบ Task 7 ที่ตรวจแล้ว: scheduler `2` scenarios, office runtime `11` scenarios, Wave 5 Python contract `20/20`, browser tick เดินเองและ task create/assign ผ่าน โดยไม่มี console error/warning

ข้อจำกัดเชิงหลักฐานและรายละเอียดการ trace ให้อ่านจาก `reports/` และ contract JSON ใน `evidence/`
