# Project State

## สถานะปัจจุบัน

- จัดระเบียบ workspace ตามแนวทาง C#-first clean reconstruction เสร็จแล้ว
- ขอบเขต semantic inventory รอบแรกถูกล็อกไว้ที่ gameplay-critical C# slice; ยังไม่เริ่มแก้ runtime implementation
- design spec ของ C# semantic inventory และ Simulation Core ผ่าน written-spec review แล้ว
- Task 1 structural C# inventory, Task 2 deep semantic slices, Task 3 canonical schema และ Task 4 SimulationCore เสร็จแล้วและตรวจผ่าน
- implementation ทำแบบ inline execution บนสาย `main`; core layer เสร็จแล้วแต่ยังไม่ migrate OfficeRuntime facade
- หลักฐาน C# ชุดใหม่อยู่ที่ `knowledge/csharp/primary/` และถูกแยกจาก runtime แล้ว
- baseline, world assets, characters, language และ reverse-engineering อยู่ใต้ `knowledge/`
- deterministic office runtime อยู่ที่ `runtime/office/`; dashboard/task runtime อยู่ที่ `runtime/dashboard/`
- roadmap ปัจจุบันอยู่ที่ `docs/roadmap/`; แผนเก่าและแนวคิด AI ที่ยังไม่เปิดใช้งานอยู่ใน `docs/archive/` และ `archive/future-ai/`
- `Assembly-CSharp/`, `Phases/` และ root C# corpus เดิมไม่อยู่ใน workspace และไม่ถูกสร้างกลับ

## สิ่งที่ตรวจสอบแล้ว

- C# primary corpus มี 85 `.cs` files และ `Assembly-CSharp.csproj`; source hash ตรงกับ relocation manifest ก่อนย้าย
- C# coverage/semantic checker compile ผ่าน และอ้างอิง path ภายใน workspace ใหม่
- structural inventory contract ผ่าน `3/3`; build/check ผ่านด้วย `types=14`, `fields=926`, `methods=257`
- semantic slice contract ผ่าน `5/5`; รวม C# evidence tests `8/8`
- inventory input boundary มี 11 ไฟล์: primary 5 ไฟล์และ `data/*.cs`; structural fingerprint ล่าสุดคือ `24e14f6e7beea8521406aee64e946803c257e5e7c537bc92450ca50ef29207da`
- semantic fingerprint ล่าสุดคือ `c67de72477df0273f68764f5c02d0a23993ab7ca28c291fda0bb93512ff002ae`; bounded access edges 18 รายการ
- gameplay field claims มีสถานะ `verified=8`, `raw_only=10`, `assembly_fallback_bounded_slice_required=3`; method claims มี `DoEvent` เป็น assembly fallback
- Simulation schema test ผ่าน และ Wave 5 contract ผ่าน `18/18`; `simulation-core-v1` contract artifact ถูกสร้างไว้ใน `runtime/office/evidence/`
- SimulationCore test ผ่าน: spawn/move/arrival, blocked collision, invalid-command immutability, deterministic digest/subscriber และ bubble expiry
- Wave 5 runtime regression ผ่าน `10` scenarios หลังเพิ่ม core แบบแยก module
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
- C# decompiler body ของ raw arrays หลายตัวไม่แสดงชื่อ field โดยตรง; access edges รอบนี้จึงใช้ bounded reverse-engineering claims ที่มี provenance ไม่ใช่การอ้างว่า C# body parse ได้ครบ
- `HumanMode`, `HumanState`, `HumanAnime`, `EventMode` และ numeric message/graph labels ยังไม่ถูก promote เป็น product semantics
- canonical schema ยังเป็น constructors/validators เท่านั้น; ยังไม่มี SimulationCore reducer, adapter ownership migration หรือ continuous scheduler
- SimulationCore ยังเป็น local module แยกจาก `runtime.js`; OfficeRuntime ยังเป็น state owner เดิมจนกว่า Task 5 migration จะผ่าน
- C# corpus ยังเป็นหลักฐานจาก decompiler ไม่ใช่ buildable runtime; project อ้างอิง output ภายนอกและยังไม่มี compile verdict
- office/dashboard ปัจจุบันเป็น deterministic adapter baseline ยังไม่ใช่เกมเต็มและยังไม่มี LLM, backend, auth หรือ multi-user sync

## ไฟล์สำคัญ

- `knowledge/csharp/primary/` — C# discovery evidence
- `knowledge/csharp/coverage/` — coverage reports ที่ได้จาก input ใหม่
- `knowledge/csharp/evidence/semantic_inventory/` — local structural inventory artifacts (ยังไม่ publish)
- `runtime/office/evidence/semantic_inventory_runtime.json` — local source-free status/provenance projection (ยังไม่ publish)
- `runtime/office/app/simulation_schema.js` — canonical state/command/event constructors and validators (local-only)
- `runtime/office/evidence/simulation_core_contract.json` — schema boundary contract (local-only)
- `runtime/office/app/simulation_core.js` — deterministic reducer/tick/snapshot/digest module (local-only)
- `knowledge/reverse-engineering/evidence/corpus/` — canonical corpus/index/views
- `tools/csharp-evidence/` — C# checkers
- `tools/maintenance/workspace_layout.py` — snapshot/relocation guard
- `knowledge/reorganization/relocation_manifest.before.json` และ `relocation_manifest.after.json` — relocation boundary
- `runtime/office/` และ `runtime/dashboard/` — deterministic runtime adapters
- `docs/roadmap/Roadmap_2.0_CSharp_First.md` — roadmap ที่ใช้งานอยู่
- `docs/superpowers/specs/2026-08-12-csharp-semantic-inventory-simulation-core-design.md` — design spec ของงานรอบถัดไป
- `docs/superpowers/plans/2026-08-12-csharp-semantic-inventory-simulation-core.md` — implementation plan ที่ผ่านการ self-review

## งานถัดไป

1. เริ่ม Task 5: ย้าย OfficeRuntime mutation ownership มาอยู่ที่ SimulationCore adapter boundary
2. คง compatibility projections สำหรับ providers/renderer เดิม โดยไม่สร้าง state owner ซ้ำ
3. ดำเนินต่อ task projection/provenance dashboard ก่อนแตะ UI playback removal
