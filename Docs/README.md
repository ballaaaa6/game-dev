# Project documentation status

เอกสารในโฟลเดอร์นี้ยังไม่ควรลบทิ้งทั้งหมด เพราะมีทั้งข้อมูลที่ยืนยันจาก dump/asset จริง และข้อเสนอเชิงสถาปัตยกรรมที่เขียนไว้สำหรับงานต่อยอด

## กฎสำคัญ: data ปัจจุบันมาก่อนเอกสาร

ข้อมูลจาก extraction ชุดล่าสุดที่ราก workspace เป็น source of truth หลัก:

- `game-dev-story-mod_Sprites/`
- `game-dev-story-mod_Dumped/`
- `game-dev-story-mod_Extracted/`

Markdown ในโฟลเดอร์นี้อาจมาจากการวิเคราะห์ build เก่าหรือข้อมูลที่ยังไม่ครบ
จึงใช้เป็น technical reference ได้เฉพาะส่วนที่ตรวจเทียบกับ data ปัจจุบันแล้ว
ถ้าข้อความในเอกสารขัดกับ asset, report, `script.json`, `dump.cs` หรือ C output
ให้ยึด data ปัจจุบันและแก้เอกสารทับ

## เอกสารที่ผ่านการปรับเป็น evidence-first reference

- `APK_to_Ghidra_Detailed_Guide.md` — ขั้นตอน APK → IL2CPP dump → Ghidra → decompiled C
- `enums.txt` — enum/type reference ที่ได้จาก IL2CPP dump
- `../Phases/Phase2/docs/CHARACTER_PRODUCTION_MANUAL.md` — current body/face assets และ 42 records ที่พบจริง; semantic ของ mode ยังต้อง trace
- `../Phases/Phase3/docs/kairosoft_language_system.md` — current language tables และ language entry points ที่ตรวจจาก dump/asset ปัจจุบัน

## ใช้เป็นแนวคิดหรือข้อเสนอ ไม่ใช่ runtime contract

- `../Phases/Phase1/docs/kairosoft_grid_system.md` — รายการตรวจสอบ grid, coordinate, depth และ collision จาก dump/asset ปัจจุบัน; ยังไม่ยืนยันว่าใช้ A* หรือ Y-sort แบบใด
- `AI_Agent_Office_Roadmap.md` — แผนงานที่ยึด data-first policy

ตัวอย่าง path เช่น `web/`, `tools/`, `data/builds/` และ build/hash เก่าในเอกสาร
เดิมถือเป็น legacy reference ไม่ใช่ path หรือ evidence ของ workspace ปัจจุบัน

## กติกาเวลาอัปเดต

ถ้า APK/build เปลี่ยน ให้ตรวจ hash, atlas dimensions และ body-face records ใหม่ก่อนนำข้อมูลเดิมไปใช้ต่อ ส่วน path ในตัวอย่างให้ยึดโครงสร้างปัจจุบันเป็นหลัก:

- extracted asset output: `game-dev-story-mod_Sprites/`
- raw APK source: `game-dev-story-mod_Extracted/`
- IL2CPP/Ghidra outputs: `game-dev-story-mod_Dumped/`
- character preview: `viewer/`
- extraction scripts: `APK_Toolkit/`
