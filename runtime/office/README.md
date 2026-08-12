# Office Runtime

Deterministic web adapter ที่จำลอง office state, scene, actor rendering และ event lifecycle จากหลักฐานที่ตรวจสอบแล้ว โดยยังไม่เชื่อม LLM หรือระบบงานจริง

## โครงสร้าง

- `app/` — browser runtime, HTML, CSS และ room data
- `evidence/` — contract, fixture, manifest และ visual QA artifact
- `reports/` — runtime architecture, closure และ investigation reports
- `tests/` — Node/Python contract tests
- `tools/` — manifest และ evidence builders

Source asset เดิมยังอยู่ใน source roots ที่ root ของ workspace; runtime อ้างอิงกลับไปแบบ read-only

## สิ่งที่ runtime รองรับ

- logical tick และ event log แบบ deterministic
- scene, furniture, actor body/face และ bounded draw commands
- locale, dialogue, bubble, notification และ cleanup lifecycle
- task projection bridge สำหรับ dashboard โดยไม่ผูกกับ AI model
- browser smoke path สำหรับ floor, furniture, actors, controls และ diagnostics

## ตรวจสอบจาก workspace root

```powershell
node --check runtime/office/app/runtime.js
node --check runtime/office/app/app.js
node runtime/office/tests/test_wave5_runtime.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
```

ข้อจำกัดเชิงหลักฐานและรายละเอียดการ trace ให้อ่านจาก `reports/` และ contract JSON ใน `evidence/`
