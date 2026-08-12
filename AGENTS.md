# Agent Instructions

ขอบเขตของไฟล์นี้คือ workspace root และโฟลเดอร์ย่อยทั้งหมด เว้นแต่จะมี `AGENTS.md` ที่อยู่ใกล้โฟลเดอร์งานกว่าและกำหนดกฎเพิ่มเติม

## Cross-Session Handoff

1. ก่อนเริ่มงาน ให้อ่าน `AGENTS.md`, `PROJECT_STATE.md` และไฟล์ handoff/state ที่เกี่ยวข้องก่อนเสมอ
2. ถ้ามี `TODO.md` หรือ `DECISIONS.md` ให้อ่านด้วยเมื่อเกี่ยวข้อง
3. หลังอ่าน state แล้วต้องตรวจสอบ codebase และไฟล์จริงก่อนทำงานต่อ ห้ามถือ state แทนการตรวจสอบ repository
4. `PROJECT_STATE.md` เก็บเฉพาะสิ่งที่ทำเสร็จ สถานะปัจจุบัน ปัญหา/ข้อจำกัด การตัดสินใจ ไฟล์ที่เปลี่ยน และงานถัดไป
5. เมื่อสถานะเปลี่ยนอย่างมีนัยสำคัญ ให้ update `PROJECT_STATE.md` และ `TODO.md` ที่เกี่ยวข้องทันที
6. ก่อนจบ session หรือเมื่อผู้ใช้สั่ง handoff ให้ตรวจสอบไฟล์จริงและอัปเดต state ให้ตรงกับสถานะล่าสุด
7. เขียน handoff แบบกระชับ ไม่ใส่รายละเอียดที่หาได้จากการอ่าน codebase ซ้ำ

## Workspace Conventions

- ยึด source/extraction ปัจจุบันและหลักฐานจาก code เป็นหลัก อย่าเดาความหมายของสิ่งที่ยังเป็น `unknown`
- รักษา source roots เดิมแบบ read-only
- วาง generated evidence ใต้ `knowledge/*/evidence`, runtime contracts ใต้ `runtime/*/evidence` และรายงาน/roadmap ใต้ `docs/`
- ห้ามสร้าง generated JSON/PNG/report ใหม่ไว้ที่ root
- `knowledge/csharp/primary/` เป็น C# discovery evidence หลัก; ห้ามสร้าง `Assembly-CSharp/` กลับ
- แยกหลักฐานออกจาก runtime: decompiled/C# evidence ใช้สำหรับวิเคราะห์และสร้าง contract เท่านั้น ไม่ execute โดยตรงในเว็บ

## Local development server lifecycle

- ก่อนเริ่ม server ให้ตรวจ listener และ process command line ของ repository ก่อน
- reuse server ที่ healthy อยู่แล้ว ห้ามพึ่งพา auto-fallback port
- ติดตาม process ที่เริ่มเองและหยุด process tree หลัง verify เว้นแต่ผู้ใช้ขอให้เปิดค้าง
- ห้าม terminate Codex-owned `mcp/server.mjs`, `node_repl` หรือ process ใต้ `OpenAI\Codex\runtimes`
