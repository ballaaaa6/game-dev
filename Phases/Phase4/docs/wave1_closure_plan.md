# Wave 1 closure pass — แผนปิด resource truth ก่อนเข้า Wave 2

อัปเดต: 2026-08-11

## คำตัดสินใจ

จะยังไม่ข้ามไป Wave 2 ทันที แต่จะทำ Wave 1 closure pass ให้จบตามเกณฑ์ด้านล่างก่อน เป้าหมายไม่ใช่กู้ความหมายของ binary ทุกบรรทัด แต่คือทำให้ทุก gap ที่กระทบ resource/renderer ถูกจัดประเภทและมีหลักฐานรองรับ

Wave 1 จะถือว่า `complete_with_known_limitations` ได้เมื่อ:

- selector/resource path ที่สำคัญมีสถานะชัดเจนว่า `verified`, `conflicting_evidence`, `extraction_missing` หรือ `out_of_scope`
- ไม่มี unknown ที่ยังไม่รู้ว่าเกิดจาก code, decompiler, index space หรือ asset extraction
- มี fixture และ regression test สำหรับ mapping ที่ยืนยันแล้ว
- มี assembly slice ขั้นแรกของ `NewGamePara` และ `DoEvent` ที่ระบุขอบเขตและ confidence ได้
- gap ที่เหลือไม่ทำให้ Wave 2 ต้องเดา resource index หรือ filename

## สิ่งที่ไม่อยู่ใน closure pass

- ไม่แปล `NewGamePara` หรือ `DoEvent` ทั้งฟังก์ชัน
- ไม่แก้ recovered C หรือ source/asset roots เดิม
- ไม่ตั้งชื่อ field จาก raw offset เพียงอย่างเดียว
- ไม่ใช้รูปลักษณ์ของภาพเพื่อเดา semantic selector
- ไม่ไล่ปิด gameplay gaps เช่น collision, walkable, placement และ animation semantics เว้นแต่เป็น dependency โดยตรงของ slice ที่เลือก

## Work packages

### W1-C0 — Freeze baseline และทำ gap inventory

**เป้าหมาย:** ใช้ผลลัพธ์ Wave 1 ปัจจุบันเป็น baseline ที่ reproducible ก่อนแก้ความหมายใด ๆ

**งาน:**

1. รัน `build_wave1_resource_map.py --check`
2. ตรวจ source hashes ใน `wave1_build_manifest.json`
3. อ่าน `resource_selector_map.json`, `wave1_branch_index.json` และ Wave 0 field/function index
4. สร้างรายการ gap ตั้งต้น โดยไม่เพิ่มสมมติฐานจากชื่อไฟล์หรือเลขท้ายชื่อ

**เกณฑ์ผ่าน:** baseline ผ่าน check และ source roots ไม่มีการเปลี่ยนแปลง

**ผลลัพธ์:** ตาราง gap ตั้งต้นใน `artifacts/wave1_gap_register.json`

### W1-C1 — Resolve static base selectors

**เป้าหมาย:** หาค่าหรือ provenance ของ `DDBody`, `DDPC`, `DDChair`, `DDDesk` และ selector ที่เกี่ยวข้อง

**แหล่งหลักฐานตามลำดับ:**

1. `form.c` static initializer ของ `GameForm`
2. `Method.c`/categorized C ที่มี assignment ไปยัง offsets `0xA8`, `0xAC`, `0xB0`, `0xD4`
3. `dump.cs` field declarations และ constructor/static constructor
4. `script.json` หรือ generated metadata ที่บอกค่า enum/static array
5. assembly fallback เฉพาะจุดที่ C ไม่แสดง assignment

**วิธี trace:**

- แยกทุก occurrence เป็น `field write`, `field read`, `array index`, `comparison` หรือ `pass-through`
- ตาม dataflow จากจุดกำหนดค่าไปถึง `IMG_LIST[...]`
- ถ้าค่าเป็น literal ให้บันทึกค่าพร้อม source line/address
- ถ้าค่าเป็น dynamic ให้บันทึกเงื่อนไขที่ต้องมีแทนการเลือกค่าหนึ่งเอง
- join กับ `game/img.inf` เฉพาะเมื่อได้ selector index ที่ยืนยันแล้ว

**สถานะที่ยอมรับ:**

- `verified_value`
- `dynamic_value_with_preconditions`
- `not_recovered_after_cross_source_trace`

**เกณฑ์ผ่าน:** selectors ทั้งหมดมีหนึ่งในสามสถานะ พร้อม source references; ไม่มีรายการที่คงคำว่า `unknown` โดยไม่มีเหตุผล

**ผลลัพธ์:** `artifacts/wave1_selector_resolution.json` และ update ใน `resource_selector_map.json`

### W1-C2 — ปิดความขัดแย้งของ `imgFace`

**เป้าหมาย:** ตัดสินว่า `StringLiteral_7514 = "false"` เป็น runtime literal จริง, pointer naming/decompiler artifact หรือยังสรุปไม่ได้

**วิธีตรวจ:**

1. ตรวจค่า zero-based ใน `stringliteral.json` และ address/pointer ที่ `Method.c` อ้าง
2. ตรวจ assembly รอบ `Method_form_BootForm_GraphicLoad` ว่าโหลด pointer ใดก่อนต่อกับ loop index
3. ตรวจ `form_GameForm___cctor` และ callsites ที่ใช้ `face_`, `face_0` หรือ `false`
4. เปรียบเทียบกับ `game/img.inf` และ face assets 36 ไฟล์
5. ตรวจว่าค่า `TFace` เป็น index ของ `imgFace[]`, index ใน `IMG_LIST` หรือ resource index คนละ namespace

**ห้ามทำ:** เปลี่ยน `7514` เป็น `7513` เพียงเพราะ `7513 = "face_"` ดูสมเหตุผลกว่า

**ผลลัพธ์ที่เป็นไปได้:**

- `verified_face_prefix`
- `recovered_c_literal_conflict`
- `face_source_not_recovered`
- `selector_uses_different_index_space`

**เกณฑ์ผ่าน:** มีข้อสรุปหนึ่งข้อพร้อมหลักฐาน และ fixture `face_0.png` ยังถูกใช้เป็น verified asset fixture แยกจาก selector inference

### W1-C3 — Audit ความครบถ้วนของ assets และ index spaces

**เป้าหมาย:** แยก “ไม่มีไฟล์จริง” ออกจาก “ค้นผิด root/extension/index space”

**รายการตรวจ:**

- เปรียบเทียบทุก entry ใน `game/img.inf`, `office/img.inf`, `load/img.inf`, `office/seb.inf` กับไฟล์จริง
- ตรวจ exact filename, extension candidate (`.png`, `.seb`, `.bytes`) และ case-insensitive match
- ตรวจชื่อ `IMG_LIST` ที่ไม่ match game manifest ว่าเป็น image, text, utility หรือ resource pack อื่น
- ตรวจ `TFace=40` และ `TFace=41` โดยแยก namespace ของ `TFace`, `imgFace[]`, `IMG_LIST` และ resource index
- สร้างรายการไฟล์ที่ไม่มี direct extracted counterpart พร้อม source/manifest evidence

**สถานะที่ยอมรับ:**

- `asset_verified`
- `index_space_mismatch`
- `missing_from_current_extraction`
- `not_an_image_resource`
- `unresolved`

**เกณฑ์ผ่าน:** ทุก missing asset มี root/manifest ที่ตรวจแล้วและมีเหตุผลหนึ่งข้อ ไม่ใช้คำว่า “หาย” โดยไม่มี audit trail

**ผลลัพธ์:** `artifacts/wave1_asset_gap_audit.json` และ update fixtures/summary ตามหลักฐาน

### W1-C4 — ทำ semantic slice แรกจาก assembly

**เป้าหมาย:** เปลี่ยน structural branch index ให้เป็น evidence slice ขนาดเล็ก โดยไม่พยายาม decompile ทั้งฟังก์ชัน

**ลำดับ:**

1. ใช้ `wave1_branch_index.json` หา entry, return blocks และ call targets ที่ใกล้ resource/initialization fields
2. เลือก slice แรกของ `NewGamePara` ที่มี field read/write หรือ call ที่ map ได้จาก Wave 0
3. เลือก slice แรกของ `DoEvent` ที่มี entry/exit ชัดเจนและไม่ต้องตีความ branch ที่ไกลเกินขอบเขต
4. แปลงเฉพาะ basic blocks ที่เลือกเป็น neutral pseudocode
5. เชื่อม raw register/offset กับ `dump.cs` เฉพาะจุดที่ offset และ access pattern ตรงกัน
6. ระบุทุก call target ที่ยังเป็น address และห้ามตั้งชื่อจากการคาดเดา

**เกณฑ์เลือก slice:** ขอบเขตชัด, มี return/continuation ชัด, มี call/field ที่ตรวจสอบย้อนกลับได้ และไม่พึ่ง branch semantics ที่ยัง unknown ทั้งชุด

**เกณฑ์ผ่าน:** แต่ละฟังก์ชันมีอย่างน้อยหนึ่ง slice พร้อม entry, exit, block addresses, field accesses, calls และ confidence

**ผลลัพธ์:**

- `docs/wave1_slices/new_game_para_slice_01.md`
- `docs/wave1_slices/do_event_slice_01.md`
- machine-readable slice metadata ใน `artifacts/wave1_branch_index.json` หรือไฟล์เสริม

### W1-C5 — สร้าง gap register และ closure report

**เป้าหมาย:** ทำให้ handoff และการตัดสินใจไป Wave 2 ตรวจสอบได้จากไฟล์ ไม่ต้องพึ่ง chat history

**schema ขั้นต่ำของ gap register:**

| field | ความหมาย |
|---|---|
| `gap_id` | identifier คงที่ |
| `question` | คำถามที่ยังต้องตอบ |
| `evidence` | source file/line/address/manifest |
| `status` | สถานะจาก controlled vocabulary |
| `impact` | `blocker`, `risk`, `non_blocking` |
| `next_action` | ทำอะไรต่อหรือเหตุผลที่หยุด |
| `confidence` | ระดับความมั่นใจของการจัดประเภท |

**controlled status:** `verified`, `recoverable`, `conflicting_evidence`, `extraction_missing`, `out_of_scope`

**เกณฑ์ปิด gap:** ห้ามมี `unknown` เป็น final status; `recoverable` ต้องมี next action ที่ concrete; `extraction_missing` ต้องมีหลักฐานว่าตรวจ source roots/manifest ที่เกี่ยวข้องแล้ว

**ผลลัพธ์:** `artifacts/wave1_gap_register.json` และ `docs/wave1_closure_report.md`

### W1-C6 — Regression และ Wave 2 gate

**ตรวจซ้ำ:**

- builder `--check`
- Wave 0 + Wave 1 tests
- static selector resolution tests
- literal conflict classification test
- asset audit consistency test
- source root read-only check

**Wave 1 closure gate:**

1. `ResourceManager`/`AppData.GetImage` contract ยัง verified
2. ทุก selector ที่กระทบ renderer มีสถานะและ evidence
3. ทุก asset gap มี classification
4. `NewGamePara`/`DoEvent` มีอย่างน้อยหนึ่ง bounded slice หรือมีเหตุผลว่า extraction/assembly ไม่พอ
5. ไม่มี blocker ที่ทำให้ Wave 2 ต้องเดา resource index หรือ filename
6. state, TODO, artifacts และ tests สอดคล้องกัน

## ลำดับการทำงานที่แนะนำ

```text
W1-C0 baseline
  -> W1-C1 static selectors
  -> W1-C2 imgFace conflict
  -> W1-C3 asset/index audit
  -> W1-C4 assembly slices
  -> W1-C5 gap register + closure report
  -> W1-C6 tests + Wave 2 gate
```

W1-C1 ถึง W1-C3 ควรทำก่อน W1-C4 เพราะ slice ที่อ่าน `IMG_LIST` จะมีความหมายผิดได้ถ้า selector namespace ยังปะปนกัน ส่วน W1-C4 ไม่จำเป็นต้องรอให้ semantic ของ gameplay ทั้งระบบสมบูรณ์

## Stop rules

- ถ้าตรวจ C, `dump.cs`, metadata และ assembly cross-reference แล้วไม่พบ assignment/value ให้จัดเป็น `extraction_missing` หรือ `conflicting_evidence` พร้อมหลักฐาน ไม่ค้นแบบไม่มีจุดจบ
- ถ้า asset ไม่อยู่ใน source roots ที่กำหนดและไม่มี manifest/reference เพิ่ม ให้จัดเป็น `missing_from_current_extraction`; ห้ามสร้าง placeholder แล้วเรียกว่า verified
- ถ้า decompiler ให้ค่าขัดกับ asset ให้เก็บทั้งสองหลักฐานและหยุดที่ `conflicting_evidence`
- ถ้า branch slice ต้องเดาความหมายจากชื่อ register/offset ให้ตัด slice ให้สั้นลงหรือคงเป็น structural-only

## Definition of done

Wave 1 closure pass จบเมื่อสามารถตอบได้ทุกข้อว่า “รู้จากหลักฐานอะไร”, “ยังไม่รู้เพราะอะไร” และ “ผลกระทบต่อ Wave 2 คืออะไร” โดยไม่จำเป็นต้องกู้ source ที่ไม่มีอยู่จริงหรือแปล gameplay ทั้งหมด

