# Project State

## สถานะปัจจุบัน

- จัดระเบียบ workspace ตามแนวทาง C#-first clean reconstruction เสร็จแล้ว
- ขอบเขต semantic inventory รอบแรกถูกล็อกไว้ที่ gameplay-critical C# slice; ยังไม่เริ่มแก้ runtime implementation
- design spec ของ C# semantic inventory และ Simulation Core ผ่าน written-spec review แล้ว
- implementation plan ถูกเขียนแล้ว; ยังไม่เริ่มแก้ runtime implementation และยังรอเลือกวิธี execute plan
- หลักฐาน C# ชุดใหม่อยู่ที่ `knowledge/csharp/primary/` และถูกแยกจาก runtime แล้ว
- baseline, world assets, characters, language และ reverse-engineering อยู่ใต้ `knowledge/`
- deterministic office runtime อยู่ที่ `runtime/office/`; dashboard/task runtime อยู่ที่ `runtime/dashboard/`
- roadmap ปัจจุบันอยู่ที่ `docs/roadmap/`; แผนเก่าและแนวคิด AI ที่ยังไม่เปิดใช้งานอยู่ใน `docs/archive/` และ `archive/future-ai/`
- `Assembly-CSharp/`, `Phases/` และ root C# corpus เดิมไม่อยู่ใน workspace และไม่ถูกสร้างกลับ

## สิ่งที่ตรวจสอบแล้ว

- C# primary corpus มี 85 `.cs` files และ `Assembly-CSharp.csproj`; source hash ตรงกับ relocation manifest ก่อนย้าย
- C# coverage/semantic checker compile ผ่าน และอ้างอิง path ภายใน workspace ใหม่
- character tests ผ่าน `5/5`
- reverse-engineering suite ผ่าน `214/214`; corpus A0/A1 checks และ A2 canonical `--check` ผ่าน
- office runtime ผ่าน Node `10` scenarios และ Python contract `17`
- dashboard runtime ผ่าน Node `18` scenarios และ Python contract `11`
- maintenance tests ผ่าน `4/4`; Python compile checks ผ่าน; browser smoke ผ่าน READY/tick/task และไม่มี console errors
- relocation comparison ผ่าน: logical members ครบและ protected roots มี file count/bytes เท่าเดิม
- cache/temp ที่สร้างระหว่างทดสอบถูกล้างแล้ว และไม่มี local server ค้าง
- source roots เดิมยังถูกเก็บไว้แบบ read-only; dumped `Assembly-CSharp.dll` ยังอยู่ใน dump ตามเดิม

## การตัดสินใจสำคัญ

- ใช้ `knowledge/csharp/primary/` เป็น discovery/control-flow evidence หลัก ไม่ execute decompiled C# โดยตรง
- ใช้ recovered C/assembly และ evidence contracts เป็น semantic validator เมื่อ C# มี decompiler artifact หรือยังเป็น `unknown`
- runtime ช่วงแรกเป็น deterministic simulation ต่อเนื่อง ไม่มีปุ่มเร่งเวลา/หยุด และค่อยต่อ LLM/task backend ภายหลัง
- เก็บ legacy tools และ roadmap เก่าไว้ใน archive แทนการลบทิ้ง เพื่อรักษา provenance

## Known limitations

- semantic names ของ numeric states และบาง branch ยังต้องยืนยันจาก C#/C/assembly หลายหลักฐาน ไม่ควรเดาเมื่อ evidence ยังขัดกัน
- C# corpus ยังเป็นหลักฐานจาก decompiler ไม่ใช่ buildable runtime; project อ้างอิง output ภายนอกและยังไม่มี compile verdict
- office/dashboard ปัจจุบันเป็น deterministic adapter baseline ยังไม่ใช่เกมเต็มและยังไม่มี LLM, backend, auth หรือ multi-user sync

## ไฟล์สำคัญ

- `knowledge/csharp/primary/` — C# discovery evidence
- `knowledge/csharp/coverage/` — coverage reports ที่ได้จาก input ใหม่
- `knowledge/reverse-engineering/evidence/corpus/` — canonical corpus/index/views
- `tools/csharp-evidence/` — C# checkers
- `tools/maintenance/workspace_layout.py` — snapshot/relocation guard
- `knowledge/reorganization/relocation_manifest.before.json` และ `relocation_manifest.after.json` — relocation boundary
- `runtime/office/` และ `runtime/dashboard/` — deterministic runtime adapters
- `docs/roadmap/Roadmap_2.0_CSharp_First.md` — roadmap ที่ใช้งานอยู่
- `docs/superpowers/specs/2026-08-12-csharp-semantic-inventory-simulation-core-design.md` — design spec ของงานรอบถัดไป
- `docs/superpowers/plans/2026-08-12-csharp-semantic-inventory-simulation-core.md` — implementation plan ที่ผ่านการ self-review

## งานถัดไป

1. เลือกวิธี execute implementation plan: subagent-driven หรือ inline execution
2. เริ่ม Task 1: structural inventory และ evidence boundary
3. ดำเนินต่อ Task 2–7 โดยคง provenance และ `unknown` ที่ยังพิสูจน์ไม่ได้
