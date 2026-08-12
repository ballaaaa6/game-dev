# C#-first Virtual Game Office

Workspace สำหรับสร้าง deterministic simulation ของ office และ dashboard โดยยึดหลักฐาน C# จาก Cpp2IL เป็น discovery input แล้วแยก runtime ที่เขียนใหม่ออกจาก source/evidence อย่างชัดเจน

## โครงสร้างปัจจุบัน

- `knowledge/` — หลักฐานที่จัดตามความหมาย: baseline, world assets, characters, language, reverse-engineering และ C# corpus
- `runtime/office/` — office scene/actor runtime แบบจำลองต่อเนื่อง
- `runtime/dashboard/` — task system และ dashboard interaction
- `tools/` — evidence checkers, reverse-engineering builders และ maintenance utilities
- `docs/` — roadmap, guides, references และ archive ของแผนเก่า
- `archive/` — legacy tools และแนวคิด AI integration ที่ยังไม่เปิดใช้งาน

## แหล่งข้อมูลที่ห้ามแก้

- `game-dev-story-mod_Sprites/`
- `game-dev-story-mod_Dumped/`
- `game-dev-story-mod_Extracted/`
- `APK_Toolkit/`
- `ghidra_11.0.1_PUBLIC/`
- `viewer/`

`knowledge/csharp/primary/` คือ C# evidence ชุดใหม่ที่ใช้เป็นหลักในการอ่าน control flow; `Assembly-CSharp/` ที่ผู้ใช้ลบแล้วจะไม่ถูกสร้างกลับ และ DLL ที่อยู่ใน dump เป็นคนละ input จึงยังเก็บไว้ตามเดิม

## จุดเริ่มต้นสำหรับ session ถัดไป

อ่าน [AGENTS.md](AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), [TODO.md](TODO.md) แล้วดู [Roadmap 2.0](docs/roadmap/Roadmap_2.0_CSharp_First.md)

คำสั่งตรวจสอบหลัก:

```powershell
python -m unittest discover -s knowledge/characters/tests -p "test_*.py" -v
python -m unittest discover -s tools/reverse-engineering/tests -p "test_*.py" -v
node runtime/office/tests/test_wave5_runtime.js
node runtime/dashboard/tests/test_wave6_task_system.js
```
