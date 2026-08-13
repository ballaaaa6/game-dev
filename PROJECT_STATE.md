# Project State

## สถานะปัจจุบัน — Social Dev clean-room reset

- เปลี่ยน authority ใหม่เป็น Social Dev; GameDev/Virtual Game Office ถูกกั้นเป็น legacy boundary ตาม `archive/pre-social-reset/legacy_manifest.json`
- ขยาย legacy manifest ให้ครอบคลุม historical knowledge `31` ไฟล์ / `3,197,523` bytes, historical guides `1` ไฟล์, legacy viewer `67` ไฟล์ และ archived maintenance `4` ไฟล์
- จัด active data store ใหม่ที่ `knowledge/social-dev/data/csharp_update/`: staged C# data `44` ไฟล์ / `437,881` bytes พร้อม hash manifest; source ใน `social dev/` ยัง read-only
- ย้าย legacy C#/reverse-engineering/maintenance tools `124` ไฟล์ / `1,833,851` bytes ไป `archive/pre-social-reset/tools/`; active `tools/` เหลือ Social Dev tools
- เก็บกวาด root สำเร็จ: ย้าย GameDev source/extraction, APK toolkit, Ghidra, viewer และ `.superpowers` รวม `6,419` ไฟล์ / `3,766,761,367` bytes ไป `archive/pre-social-reset/`; root เหลือเฉพาะโครง Social Dev และ shared metadata
- R0 provenance pass เสร็จ: fingerprint RAR, APK, asset ZIP, C# update และ VGO_Core แล้ว โดย source/extraction roots ยัง read-only; มีเพียง organized data copy และ legacy-tool archive ที่จัดการแยกออกมา
- C# RAR baseline ถูก extract เป็น evidence ที่ `knowledge/social-dev/evidence/csharp_raw_20260813/`; ไม่ execute decompiled C# โดยตรง
- เทียบ C# update ด้วย canonical path แล้ว: `exact_match=4980`, `modified=588`, `update_only=586`
- สร้าง Social Dev structural inventory แล้ว: inputs `72`, types `82`, fields `3430`, methods `1685`, fingerprint `1b2f9396f2768545d4f719022fb1b116df0de9a5347fb46337a8417e1257093a`
- candidate diff ยืนยันว่า update ลบ `Cpp2ILHelpers.NoteDecompilerIssue` ใน 60 gameplay/lifecycle files (`16699 → 0`) แต่ `//IL_...` annotations ยังเท่าเดิม `29030`; structural counts ของ raw/update เท่ากัน จึงจัดเป็น textual cleanup ไม่ใช่ semantic repair
- marker-only normalization ยืนยัน `60` files เป็น byte-equivalent หลังตัดเฉพาะ marker lines, `12` files exact อยู่แล้ว และ `0` files มี content change นอกเหนือจาก marker; ใช้ RAR เป็น provenance anchor ต่อไป
- สร้าง candidate schema จากหลักฐานแล้ว: DataManager registry `43` typed arrays / data classes `44` / data fields `1112`; runtime entity candidate `14` types / `919` fields / `30` lifecycle hooks / `21` relation candidates โดยทุก semantic status ยัง `unknown`
- สร้าง load-contract candidates แล้ว: registry `41` รายการจับคู่กับ `Load(StringArrayStream)` ได้, `2` รายการยังไม่มี loader ที่จับได้; field/load alignment ได้ `38` candidate, `3` count mismatch และ `3` Load missing จึงยังไม่สร้าง production model จากตำแหน่งคอลัมน์
- asset/APK inventory ผ่าน read-only gate: ZIP `3566` members, asset index `3542` rows, `zip_exact=3542`, APK source entries `3508` present / `34` missing (misc text payloads), APK fingerprint ตรง และ pack map `25/25 roundtrip_exact`
- extract เฉพาะ evidence text/index จาก ZIP แล้ว `114` files; DataManager registry cross-check กับ xls ได้ English `43/43` และ Japanese `43/43`, เหลือ English extras `Exclusion.txt`, `softkey.txt`, `text.txt` ที่ยังไม่ promote
- จัด boundary เบื้องต้นแล้ว: `data`/`game`/`game.routeSearch`/`main` เป็น candidate evidence; `form` เป็น presentation; `KairoEngine`/`Dependencies` เป็น engine/dependency
- `VGO_Core` ถูกจัดเป็น derived architecture draft เท่านั้น เพราะยังมี mocked loader, placeholder movement และ save/load ไม่ครบ
- สร้าง VGO disposition manifest แล้ว: `5` ไฟล์ / `11,647` bytes ถูกติดสถานะ `derived_draft_not_promoted`; ห้ามใช้ `baseSpeed`/`isSpecialBody` เป็น schema จนกว่าจะมี source provenance
- active-reference scan หลัง root cleanup: อ่านไฟล์ข้อความ `5,820` ไฟล์ พบ `3,774` matches ใน `57` ไฟล์; intentional documentation `355`, legacy artifacts `3,419`, active dependency `0` — reference gate ผ่าน
- `runtime/social-dev/` ถูกสร้างเป็น boundary ว่างสำหรับ contract-first runtime; `runtime/office` และ `runtime/dashboard` ถูก freeze เป็น legacy

## ประวัติ baseline เดิม (GameDev legacy)

- Scene-map reconstruction Task 2 SEB audit เสร็จแล้ว: พบ floor SEB 21 logical files ที่ shortfall 4 bytes เท่ากัน; ไม่มี direct named payload ใน APK/ZIP/extracted ที่ complete จึงได้ผล `no_full_payload_found` ทั้งหมด และไม่มี reextract payload ถูก stage
- จัดระเบียบ workspace ตามแนวทาง C#-first clean reconstruction เสร็จแล้ว
- ขอบเขต semantic inventory รอบแรกถูกล็อกไว้ที่ gameplay-critical C# slice; runtime implementation ทำต่อแบบ local-only
- design spec ของ C# semantic inventory และ Simulation Core ผ่าน written-spec review แล้ว
- Task 1 structural C# inventory, Task 2 deep semantic slices, Task 3 canonical schema, Task 4 SimulationCore, Task 5 OfficeRuntime adapter migration, Task 6 dashboard canonical projection/provenance, Task 7 continuous scheduler และ Task 8 final verification/report เสร็จแล้วและตรวจผ่าน
- Task 4 scene-map reconstruction semantics contract เสร็จแล้ว: เพิ่ม deterministic C#/C/assembly text-trace helper, SEB consumer-boundary evidence contract และ report ที่ระบุ crop/translation/selector/object-base/camera/depth แยกจากกัน
- Task 5 object-placement contract เสร็จแล้ว: current page/reception-desk-chair fixture stays adapter-only, asset identity is verified, and original room/object placement remains unknown because no persisted/generated floor0 room-state record was found
- Task 5 fix round 1: added OfficeObjecList as the opening provenance anchor and renamed the summary classification so no contract field named `status` carries a non-approved value
- implementation ทำแบบ inline execution บนสาย `main`; exported OfficeRuntime ใช้ SimulationCore เป็น state owner และมี compatibility projections
- dashboard อ่าน canonical snapshot จาก SimulationCore และ source-free semantic evidence projection ที่โหลดจาก `runtime/office/evidence/`; ไม่มีการ import raw C# ใน browser
- dashboard เริ่ม scheduler ภายในเองที่ interval `160ms`; ไม่มี Play/Pause/Step/Reset หรือ speed control สำหรับ simulation
- หลักฐาน C# ชุดใหม่อยู่ที่ `knowledge/csharp/primary/` และถูกแยกจาก runtime แล้ว
- baseline, world assets, characters, language และ reverse-engineering อยู่ใต้ `knowledge/`
- deterministic office runtime อยู่ที่ `runtime/office/`; dashboard/task runtime อยู่ที่ `runtime/dashboard/`
- roadmap ปัจจุบันอยู่ที่ `docs/roadmap/`; แผนเก่าและแนวคิด AI ที่ยังไม่เปิดใช้งานอยู่ใน `docs/archive/` และ `archive/future-ai/`
- `Assembly-CSharp/`, `Phases/` และ root C# corpus เดิมไม่อยู่ใน workspace และไม่ถูกสร้างกลับ

## สิ่งที่ตรวจสอบแล้ว

- Task 2 fix round 1 closes trailing-byte/recovery/staging gates: codec/audit tests ผ่าน `9/9`; suite ของ Task 1+2 ผ่าน `14/14`; build audit และ `py_compile` ผ่าน; source/extraction file hashes `1,881` รายการตรงกับ Task 1 inventory
- C# primary corpus มี 85 `.cs` files และ `Assembly-CSharp.csproj`; source hash ตรงกับ relocation manifest ก่อนย้าย
- C# coverage/semantic checker compile ผ่าน และอ้างอิง path ภายใน workspace ใหม่
- structural inventory contract ผ่าน `3/3`; build/check ผ่านด้วย `types=14`, `fields=926`, `methods=257`
- semantic slice contract ผ่าน `5/5`; รวม C# evidence tests `8/8`
- inventory input boundary มี 11 ไฟล์: primary 5 ไฟล์และ `data/*.cs`; structural fingerprint ล่าสุดคือ `24e14f6e7beea8521406aee64e946803c257e5e7c537bc92450ca50ef29207da`
- semantic fingerprint ล่าสุดคือ `c67de72477df0273f68764f5c02d0a23993ab7ca28c291fda0bb93512ff002ae`; bounded access edges 18 รายการ
- gameplay field claims มีสถานะ `verified=8`, `raw_only=10`, `assembly_fallback_bounded_slice_required=3`; method claims มี `DoEvent` เป็น assembly fallback
- Simulation schema test ผ่าน และ Wave 5 contract ผ่าน `20/20`; `simulation-core-v1` contract artifact ถูกสร้างไว้ใน `runtime/office/evidence/`
- SimulationCore test ผ่าน: spawn/move/arrival, blocked collision, invalid-command immutability, deterministic digest/subscriber และ bubble expiry
- Wave 5 runtime regression ผ่าน `11` scenarios หลัง migrate facade; Wave 6 task system ผ่าน `18` scenarios
- Dashboard canonical snapshot/evidence contract ผ่าน `12/12`; `app.js` syntax check ผ่าน; browser script order ตรวจว่า schema → core → runtime
- Continuous scheduler test ผ่าน `2` scenarios; `app.js` และ scheduler syntax check ผ่าน
- Python office/dashboard contracts ผ่านรวม `32/32`
- final regression ผ่าน: C# evidence `8/8`, characters `5/5`, reverse-engineering `214/214`, maintenance `4/4`, office Python `20/20`, dashboard Python `12/12`; Node schema/core/scheduler/office/dashboard tests ผ่านทั้งหมด
- character tests ผ่าน `5/5`
- reverse-engineering suite ผ่าน `214/214`; corpus A0/A1 checks และ A2 canonical `--check` ผ่าน
- office runtime ผ่าน Node `11` scenarios และ Python Wave 5 contract `20/20`
- dashboard runtime ผ่าน Node `18` scenarios และ Python contract `12`
- maintenance tests ผ่าน `4/4`; Python compile checks ผ่าน; browser smoke ผ่าน: READY/tick เดินเอง `96 → 101` ในประมาณ `700ms`, canvas `600x800`, diagnostics มี `simulation-core-v1`/evidence, task create/assign ผ่าน, ไม่มี console error/warning และ server ที่เปิดทดสอบถูกปิดแล้ว
- relocation comparison ผ่าน: logical members ครบและ protected roots มี file count/bytes เท่าเดิม
- cache/temp ที่สร้างระหว่างทดสอบถูกล้างแล้ว และไม่มี local server ค้าง
- source roots เดิมยังถูกเก็บไว้แบบ read-only; dumped `Assembly-CSharp.dll` ยังอยู่ใน dump ตามเดิม

## การตัดสินใจสำคัญ

- ใช้ `knowledge/csharp/primary/` เป็น discovery/control-flow evidence หลัก ไม่ execute decompiled C# โดยตรง
- ใช้ recovered C/assembly และ evidence contracts เป็น semantic validator เมื่อ C# มี decompiler artifact หรือยังเป็น `unknown`
- runtime ช่วงแรกเป็น deterministic simulation ต่อเนื่อง ไม่มีปุ่มเร่งเวลา/หยุด และค่อยต่อ LLM/task backend ภายหลัง
- เก็บ legacy tools และ roadmap เก่าไว้ใน archive แทนการลบทิ้ง เพื่อรักษา provenance

## Known limitations

- APK/ZIP มี Unity data members ชื่อ hash และไม่มี direct `floor*.seb`; การตามหา TextAsset ที่ฝังอยู่ต้องใช้ bundle provenance evidence เพิ่มเติม จึงยังไม่ยืนยันว่า shortfall เป็น source limitation แท้หรือ nested-extraction defect
- semantic names ของ numeric states และบาง branch ยังต้องยืนยันจาก C#/C/assembly หลายหลักฐาน ไม่ควรเดาเมื่อ evidence ยังขัดกัน
- C# decompiler body ของ raw arrays หลายตัวไม่แสดงชื่อ field โดยตรง; access edges รอบนี้จึงใช้ bounded reverse-engineering claims ที่มี provenance ไม่ใช่การอ้างว่า C# body parse ได้ครบ
- `HumanMode`, `HumanState`, `HumanAnime`, `EventMode` และ numeric message/graph labels ยังไม่ถูก promote เป็น product semantics
- scheduler เป็น wall-clock driver ของ UI เท่านั้น; logical tick/snapshot/digest ยัง deterministic และไม่มี visible stop/pause/speed path
- `CoreOfficeRuntime` เป็น exported facade ที่ delegate mutation ไปยัง core; old provider contracts และ renderer projections ยังทำงานผ่าน API เดิม
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
- `runtime/office/app/runtime.js` — Core-backed OfficeRuntime compatibility facade (local-only)
- `runtime/office/app/app.js` และ `runtime/office/app/index.html` — dashboard canonical projection/evidence panel (local-only)
- `runtime/office/app/continuous_scheduler.js` และ `runtime/office/tests/test_continuous_scheduler.js` — internal continuous tick driver and lifecycle tests (local-only)
- `runtime/office/README.md` และ `runtime/office/reports/simulation_core_architecture.md` — implementation architecture/handoff docs
- `knowledge/reverse-engineering/evidence/corpus/` — canonical corpus/index/views
- `archive/pre-social-reset/tools/scene_reconstruction/csharp_trace.py` และ `archive/pre-social-reset/tools/scene_reconstruction/build_seb_semantics_contract.py` — frozen deterministic SEB evidence tools
- `knowledge/world-assets/evidence/scene_reconstruction/seb_semantics_contract.json` — SEB semantics evidence contract
- `archive/pre-social-reset/tools/scene_reconstruction/build_object_placement_contract.py` และ `archive/pre-social-reset/tools/scene_reconstruction/test_object_placement.py` — frozen object-placement lineage classifier and tests
- `knowledge/world-assets/evidence/scene_reconstruction/object_placement_contract.json` — object-placement provenance contract
- `.superpowers/sdd/2026-08-12-scene-map-reconstruction/task-4-report.md` — task 4 report and self-review
- `.superpowers/sdd/2026-08-12-scene-map-reconstruction/task-5-report.md` — task 5 report and self-review
- `archive/pre-social-reset/tools/csharp-evidence/` — frozen C# checkers
- `archive/pre-social-reset/tools/maintenance/workspace_layout.py` — frozen snapshot/relocation guard
- `knowledge/reorganization/relocation_manifest.before.json` และ `relocation_manifest.after.json` — relocation boundary
- `knowledge/social-dev/data/csharp_update/` และ `knowledge/social-dev/data/data_package_manifest.json` — active organized Social Dev data package
- `archive/pre-social-reset/tools/` — archived legacy tools; ห้าม import กลับเข้า active runtime
- `archive/pre-social-reset/root-sources/` — archived GameDev roots, APK toolkit, Ghidra และ viewer
- `archive/pre-social-reset/.superpowers/` — archived historical task plans
- `runtime/office/` และ `runtime/dashboard/` — deterministic runtime adapters
- `docs/roadmap/Roadmap_2.0_CSharp_First.md` — roadmap ที่ใช้งานอยู่
- `docs/superpowers/specs/2026-08-12-csharp-semantic-inventory-simulation-core-design.md` — design spec ของงานรอบถัดไป
- `docs/superpowers/plans/2026-08-12-csharp-semantic-inventory-simulation-core.md` — implementation plan ที่ผ่านการ self-review

## งานถัดไป — Social Dev

1. ตรวจ 588 modified files โดยเริ่มจาก `data`, `game`, `game.routeSearch` และ `main`
2. ปิด `Load`/field alignment mismatches แล้วแยก semantic contracts ของ DataManager, BaseData, Player, Staff, Room และ save/load โดยติดสถานะ provenance ทุก field
3. ตรวจ assembly guide และ APK metadata ต่อเพื่อยืนยัน asset selectors/relationships; ตอนนี้มีเพียง identity/roundtrip gate ยังไม่ใช่ selector promotion
4. สร้าง canonical Social Dev schema และ runtime contracts ใต้ `runtime/social-dev/`
5. รักษา active `tools/social-dev` ให้แยกจาก legacy archive; reference gate ผ่านแล้วด้วย `active_dependency=0`
6. เมื่อ contract tests และ reference gate ผ่าน ค่อยเสนอ cutover และขออนุมัติลบ legacy แบบถาวร

## งานเดิมที่ถูก freeze

- nested Unity bundle/TextAsset audit เดิมอยู่ใน legacy scope
- compatibility projections ของ office เดิมไม่ใช่ Social Dev state owner
- backend/auth/multi-user และ LLM รอจนกว่า Social Dev baseline จะผ่าน contract tests
