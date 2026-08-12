# TODO

## ปิดงานจัดระเบียบ workspace

- [x] ย้าย/ลบ empty legacy directories ให้เหลือเฉพาะหมวดปัจจุบัน
- [x] ลบ cache ที่สร้างจาก test/compile โดยตรวจ target แบบ explicit
- [x] เขียน `knowledge/reorganization/relocation_manifest.after.json`
- [x] อัปเดต `PROJECT_STATE.md` หลัง final verification
- [x] รัน relocation comparison, path scan, full tests และ browser smoke

## C#-first Simulation Core

- [x] ล็อก gameplay-critical C# slice และเขียน design spec ของ inventory/Simulation Core
- [x] review written spec และแตก implementation plan ก่อนแก้โค้ด
- [x] เลือกวิธี execute implementation plan ก่อนแก้โค้ด (inline execution บน `main`)
- [x] ทำ structural inventory class/method/field ของ gameplay-critical C# slice
- [ ] แยก state, transition, timer, movement, scene, actor และ event contracts จากหลักฐาน
- [x] สร้าง bounded semantic claims table โดยให้สถานะ `unknown`/`raw_only` อยู่ได้และมี provenance ต่อค่า
- [x] ออกแบบและตรวจ canonical simulation schema ที่ไม่ผูกกับ decompiled object layout
- [ ] ทำ deterministic tick loop ที่จำลอง office ต่อเนื่องโดยไม่มี playback controls
- [ ] เชื่อม scene/actor state เข้ากับ `runtime/office/` ผ่าน adapter contracts
- [ ] ค่อยเชื่อม task assignment จริงและ LLM หลัง simulation baseline ผ่าน contract tests

## Dashboard

- [ ] แสดง actor state, task state, scene, event log และ evidence/provenance ในหน้าเดียว
- [ ] เพิ่ม live state stream โดยยังรักษา deterministic replay/debug snapshot
- [ ] วาง backend/auth/multi-user sync เป็น adapter boundary แยกจาก simulation core

## ห้ามทำในช่วงนี้

- อย่าสร้าง `Assembly-CSharp/` กลับ
- อย่าแก้ source roots หรือ execute decompiled C# เป็น production runtime
- อย่าเปลี่ยน `unknown` เป็น semantic name โดยไม่มี evidence ที่ตรวจสอบได้
- อย่าลบ evidence เดิม; ถ้าไม่ใช้ให้ย้ายไป archive พร้อมรักษา provenance

## ประวัติที่ freeze แล้ว

รายละเอียด corpus intelligence, TypeScript port และ roadmap เก่าเก็บอยู่ใน `docs/archive/`; ให้ใช้ roadmap ปัจจุบันใน `docs/roadmap/` เป็นตัวนำ
