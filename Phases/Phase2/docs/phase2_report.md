# Phase 2 — Character and animation catalog

สถานะ: `complete_with_known_limitations` สำหรับหลักฐานที่มีใน extraction ปัจจุบัน

เอกสารนี้แยกข้อเท็จจริงจาก extraction ออกจาก adaptation layer ของ Virtual AI Office.

## Verified

- `bodyface_records.reference.json` มี 42 records, mode 0–41 และทุก mode ไม่ซ้ำกัน.
- พบ body asset 26 ไฟล์ และ face asset 36 ไฟล์; asset files ถูก hash และตรวจ dimensions แล้ว.
- `GameForm.DrawHuman` ระบุพารามิเตอร์ `TFace`, `TBody`, `TMode` ใน `dump.cs`; recovered C ใช้ `TMode` เพื่อเลือกข้อมูลจาก static `BodyFace` table.
- กลไกประกอบภาพที่ยืนยันได้คือ `imgBody[TBody]` + `imgFace[TFace]` โดยใช้ crop/offset จาก `BodyFace[TMode]`; `AddBodyFace` ยืนยัน mapping ของ P0–P13 เป็น body/face/shadow fields. บาง branch มี offset ปรับเพิ่มตาม mode.
- HumanDex draw path ส่ง `HumanDexFaceG`, `HumanDexBodyG`, `HumanDexAnime` เข้า `DrawHuman` โดยตรง; นี่เป็น dynamic selector path ที่ยืนยันได้หนึ่งเส้นทาง แต่ยังไม่ใช่ semantic mapping ของ Agent state.
- crop/offset record ที่ parse และ trace ได้: 42/42.
- สร้าง neutral frame descriptors: 42 และ mechanical source-layout groups: 11.

## Probable

- `talking` มี candidate mapping เป็น mode 8/9 ใน Kaiwa/dialogue draw path เพราะเห็น TMode สลับ `iVar % 2 + 8` และมี callsite ของ `DrawFukidashi` ในอีก dialogue-like draw path; timing/loop/face timing ยังไม่ยืนยัน.
- Mechanical groups เป็นกลุ่ม candidate จาก source-row geometry เท่านั้น ไม่ใช่ semantic animation.

## Unknown

- ไม่สามารถยืนยัน semantic ของ mode ใด ๆ ว่าเป็น idle/walking/working/sitting/break ได้จากหลักฐานชุดนี้; ห้า state แรกจึงคงเป็น `unknown`.
- direction, frame timing, loop mode, mirroring, pivot/baseline, seat/placement และ exact runtime body/face pairing ของทุก callsite ยังไม่ยืนยัน.
- literal selector references ที่ไม่มี extracted asset: TFace=40, TFace=41.

## Coverage

- BodyFace records: 42 parsed; semantic modes verified: 0.
- Agent states: verified 0, probable 1, unknown 5.
- Literal DrawHuman callsites scanned: 106; selector coverage is partial because 92 calls contain variable-driven selectors.

## Preview policy

- `body_contact_sheet.png` และ `face_contact_sheet.png` แสดง original atlases.
- `bodyface_mode_preview.png` ใช้ `body0.png` + `face_0.png` เป็น diagnostic sample เท่านั้น; ไม่ใช่ข้อสรุปว่า runtime เลือก pair นี้.
- ไม่มี GIF/WebP animation ที่อ้าง timing ได้ จึงไม่สร้าง loop ที่เดาขึ้นเอง.

## Dependencies and next evidence

- Phase 1 placement/seat/grid/depth unknowns ยังไม่ถูกปิด และไม่ถูกใช้เป็นเงื่อนไข block Phase 2.
- งานถัดไปที่คุ้มค่าคือ trace dynamic `DrawHuman` ที่เหลือกลับไปยัง `DrawObj`/Syain/Kaiwa data, ยืนยันลำดับ resource array กับชื่อไฟล์จริง และหา initialization ของ BodyFace table ที่ยังหายจาก categorized callsites.

## Artifacts

- `artifacts/phase2_input_audit.json`
- `artifacts/bodyface_analysis.json`
- `artifacts/character_asset_catalog.json`
- `artifacts/character_manifest.json`
- `artifacts/animation_manifest.json`
- `artifacts/phase2_code_trace.json`
- `artifacts/agent_state_mapping.json`
- `artifacts/phase2_validation_report.json`
- `artifacts/preview/*.png`
