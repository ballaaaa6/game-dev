# TODO

## Social Dev clean-room reset

- [x] กำหนด Social Dev เป็น source of truth และสร้าง legacy boundary สำหรับ GameDev
- [x] fingerprint RAR, APK, asset ZIP, C# update และ VGO_Core
- [x] extract RAR เป็น read-only evidence ใต้ `knowledge/social-dev/evidence/`
- [x] เทียบ C# baseline/update ด้วย canonical path: `4980` exact, `588` modified, `586` update-only
- [x] สร้าง Social Dev structural inventory: `72` inputs, `82` types, `3430` fields, `1685` methods
- [x] วัด candidate diff: update ลด decompiler issue markers `16699 → 0` แต่ยังมี IL annotations `29030` และยังไม่ใช่ buildable verdict
- [x] ตรวจ marker-only equivalence: `60` cleanup-only, `12` exact, `0` content changes beyond markers
- [x] สร้าง candidate data registry: `43` DataManager arrays, `44` data types, `1112` fields
- [x] สร้าง candidate runtime boundary: `14` key entities, `919` fields, `30` lifecycle hooks, `21` relation candidates
- [x] สร้าง load-contract candidate: `41` registry loaders, `2` loader-missing; field/load alignment `38` candidate, `3` mismatch, `3` missing
- [x] ทำ read-only asset/APK consistency gate: `3542` ZIP rows exact, `3508` APK entries present, `34` misc text payloads unresolved, `25/25` pack roundtrip exact
- [x] extract เฉพาะ index/assembly guide/xls evidence `114` files และ cross-check DataManager กับภาษา English/Japanese `43/43`
- [x] แยก `data`, `game`, `game.routeSearch`, `main`, `form`, engine/dependency และ VGO_Core ตาม boundary contract
- [x] ทำ VGO_Core disposition manifest: `5` derived files, ทั้งหมด `not_promoted`
- [x] ขยาย legacy boundary ให้ครอบคลุม historical knowledge, guides, viewer และ shared maintenance โดยไม่ลบ evidence
- [x] stage C# data `44` ไฟล์ไป `knowledge/social-dev/data/csharp_update/` พร้อม hash manifest โดยรักษา source read-only
- [x] ย้าย legacy C#/reverse-engineering/maintenance tools ออกจาก active `tools/` ไป `archive/pre-social-reset/tools/`
- [x] เก็บกวาด root: ย้าย GameDev source/extraction, APK toolkit, Ghidra, viewer และ `.superpowers` ไป `archive/pre-social-reset/` โดยไม่ลบข้อมูล
- [x] สแกน active references หลัง root cleanup: `5820` ไฟล์, `3774` matches, `active_dependency=0`
- [ ] ตรวจ semantic diff ของ `data` 44 ไฟล์, `game` 23 ไฟล์, route-search 2 ไฟล์ และ lifecycle 3 ไฟล์
- [ ] สร้าง canonical Social Dev data/entity/save contracts พร้อม provenance statuses
- [x] สร้าง read-only asset validation manifest จาก assembly guide/APK/index
- [ ] ยืนยัน selector/semantic relationship ของ asset ก่อน promote เข้า runtime
- [ ] สร้าง runtime contracts ใต้ `runtime/social-dev/`
- [x] decouple Social Dev inventory tool จาก `tools/csharp-evidence` ด้วย local active parser
- [x] ตัด GameDev dependency ออกจาก active tree และทำ scan ซ้ำ: gate ผ่าน (`active_dependency=0`)
- [ ] ขออนุมัติและลบ legacy archive หลัง cutover gates ผ่านเท่านั้น

## Legacy GameDev baseline — frozen

- [x] ย้าย/ลบ empty legacy directories ให้เหลือเฉพาะหมวดปัจจุบัน
- [x] ลบ cache ที่สร้างจาก test/compile โดยตรวจ target แบบ explicit
- [x] เขียน `knowledge/reorganization/relocation_manifest.after.json`
- [x] อัปเดต `PROJECT_STATE.md` หลัง final verification
- [x] รัน relocation comparison, path scan, full tests และ browser smoke

## Legacy C#-first Simulation Core — frozen

- [x] ล็อก gameplay-critical C# slice และเขียน design spec ของ inventory/Simulation Core
- [x] review written spec และแตก implementation plan ก่อนแก้โค้ด
- [x] เลือกวิธี execute implementation plan ก่อนแก้โค้ด (inline execution บน `main`)
- [x] ทำ structural inventory class/method/field ของ gameplay-critical C# slice
- [ ] แยก state, transition, timer, movement, scene, actor และ event contracts จากหลักฐาน
- [x] สร้าง bounded semantic claims table โดยให้สถานะ `unknown`/`raw_only` อยู่ได้และมี provenance ต่อค่า
- [x] ออกแบบและตรวจ canonical simulation schema ที่ไม่ผูกกับ decompiled object layout
- [x] ทำ deterministic SimulationCore reducer/tick/snapshot/digest พร้อม collision/event/bubble contracts
- [x] ทำ deterministic tick loop ที่จำลอง office ต่อเนื่องโดยไม่มี playback controls
- [x] เชื่อม scene/actor state เข้ากับ `runtime/office/` ผ่าน Core-backed adapter contracts
- [ ] ค่อยเชื่อม task assignment จริงและ LLM หลัง simulation baseline ผ่าน contract tests

## Legacy scene-map reconstruction — frozen

- [x] Audit every discovered `floor*.seb`, preserve four-byte partial tails, and conditionally stage only a verified complete archive candidate
- [x] Reject trailing-byte and incomplete archive payloads from recovery and staging
- [x] Trace SEB consumer-boundary semantics with deterministic C#/C/assembly evidence and keep crop/translation/selector/object-base/camera/depth separate
- [ ] Establish nested Unity bundle/TextAsset provenance before treating the four-byte SEB shortfall as a source limitation

## Legacy dashboard — frozen

- [x] แสดง actor state, task state, scene, event log และ evidence/provenance ในหน้าเดียว
- [x] เพิ่ม live UI state stream โดยยังรักษา deterministic replay/debug snapshot
- [ ] วาง backend/auth/multi-user sync เป็น adapter boundary แยกจาก simulation core

## ห้ามทำในช่วงนี้

- อย่าสร้าง `Assembly-CSharp/` กลับ
- อย่าแก้ source roots หรือ execute decompiled C# เป็น production runtime
- อย่าเปลี่ยน `unknown` เป็น semantic name โดยไม่มี evidence ที่ตรวจสอบได้
- อย่าลบ evidence เดิม; ถ้าไม่ใช้ให้ย้ายไป archive พร้อมรักษา provenance

## ประวัติที่ freeze แล้ว

รายละเอียด corpus intelligence, TypeScript port และ roadmap เก่าเก็บอยู่ใน `docs/archive/`; ให้ใช้ roadmap ปัจจุบันใน `docs/roadmap/` เป็นตัวนำ
