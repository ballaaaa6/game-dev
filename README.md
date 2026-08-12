# Workspace index

โครงสร้างนี้แยก source เดิมออกจากผลลัพธ์ของแต่ละ phase แล้ว เพื่อให้ rerun หรือเริ่ม phase ใหม่ได้โดยไม่เขียนไฟล์ปนกันที่ root

## พื้นที่หลัก

- `Docs/AI_Agent_Office_Roadmap.md` — roadmap ใหญ่และ checklist ความคืบหน้าระดับ Phase
- `TODO.md` — backlog งานย่อยที่พร้อมลงมือทำ เรียงตาม dependency
- `PROJECT_STATE.md` — สถานะล่าสุด, known limitations และ handoff สำหรับ session ถัดไป
- `Phases/` — artifacts, report, preview และ reference ที่จัดตาม Phase 0–7
- `game-dev-story-mod_Sprites/` — source asset ที่ freeze ไว้ ห้ามแก้ระหว่างการวิเคราะห์
- `game-dev-story-mod_Dumped/` — dump/decompiled source ที่ freeze ไว้
- `game-dev-story-mod_Extracted/` — ไฟล์ extraction ดิบจาก APK
- `ghidra_11.0.1_PUBLIC/` — Ghidra project เดิม
- `APK_Toolkit/` — script, extractor และ input APK/ZIP; ผลลัพธ์ใหม่จะเขียนเข้า `Phases/`
- `Docs/` — เอกสารอ้างอิงข้าม phase และคู่มือเครื่องมือ
- `viewer/` — preview/runtime viewer เดิม

กติกาสำคัญ: ไม่สร้าง generated JSON/PNG/report ใหม่ไว้ที่ workspace root และไม่ย้ายหรือเขียนทับ source roots เดิม

ดูรายละเอียดการเก็บผลลัพธ์ได้ที่ [`Phases/README.md`](<Phases/README.md>)
