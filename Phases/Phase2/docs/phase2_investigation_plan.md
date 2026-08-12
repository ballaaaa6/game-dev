# แผนศึกษาต่อ Phase 2 — กลไกประกอบภาพและ animation semantics

เอกสารนี้เป็นแผนต่อจาก catalog ที่สร้างแล้ว โดยยึด extraction จริงเป็นหลัก
และแยก “กลไกที่พิสูจน์ได้” ออกจาก “ความหมายของ state ที่ยังสรุปไม่ได้”.

## ผลตรวจล่าสุดที่ยืนยันได้

จาก `dump.cs` และ recovered C:

1. `GameForm.DrawHuman(Graphics g, int X, int Y, int TFace, int TBody, int TMode)` มี selector contract ชัดเจน
2. `imgBody` และ `imgFace` เป็น image arrays ของ `GameForm`
3. `TMode` ใช้เลือก `BodyFace[TMode]`
4. `AddBodyFace(P0..P13)` เขียนค่าลงตารางตามลำดับนี้:
   - `P0..P5` = body destination/source/size
   - `P6..P11` = face destination/source/size
   - `P12..P13` = shadow destination values
5. ใน DrawHuman มีการวาด body จาก `imgBody[TBody]` ด้วย fields `0..5` และวาด face จาก `imgFace[TFace]` ด้วย fields `6..11`; บาง branch มี offset ปรับเพิ่มตาม mode
6. HumanDex draw path ส่ง `HumanDexFaceG`, `HumanDexBodyG`, `HumanDexAnime` เข้า DrawHuman โดยตรงที่ `form.c:19687–19691`
7. ยังมี dynamic DrawHuman call จำนวนมากใน `form.c` ดังนั้นการเห็นภาพประกอบถูกต้องไม่ได้แปลว่า trace state ครบแล้ว

หลักฐานหลัก:

- `game-dev-story-mod_Dumped/dump.cs:276205–276206`
- `game-dev-story-mod_Dumped/dump.cs:276465`
- `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:26551–26659`
- `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:41288–41475`
- `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:19687–19691`

## สิ่งที่ยังไม่รู้ แบ่งตามลำดับความสำคัญ

### A. ต้องปิดก่อนนำไปใช้จริง

- index ของ `imgBody[]`/`imgFace[]` ตรงกับเลขในชื่อไฟล์โดยตรงหรือผ่านลำดับ resource จาก `img.inf`
- BodyFace ทั้ง 42 records ถูก initialize ที่ใดและมี callsite/ลำดับการสร้างอย่างไร
- dynamic selectors ของ `DrawObj`, Syain และ Kaiwa resolve กลับไปเป็นตัวละคร/asset ใด
- branch ของ DrawHuman ที่ใช้กับแต่ละ `TMode` และกรณี `TKage`

### B. ต้องศึกษาก่อนติดป้าย animation

- `TMode` แต่ละค่าหมายถึง pose, direction, frame หรือเป็นเพียงรูปแบบการวาด
- ลำดับ frame ที่วนจริง และ frame timer/duration
- การเปลี่ยนหน้า (`TFace`) ระหว่าง animation
- direction encoding, mirroring และการใช้ `HumanDexWalk`
- state transition ของ employee จากเดิน → ทำงาน → พัก/นั่ง

### C. ยังเป็น unknown ได้ แม้ Phase 2 เดินต่อได้

- semantic ของ `idle`, `walking`, `working`, `sitting`, `break`
- pivot/baseline/anchor และ seat/placement ของ Phase 1
- collision, walkable, zone และ depth contract

## ลำดับการทำงานที่เสนอ

### ขั้นที่ 1 — ทำ compositor ที่ไม่ใส่ semantic

สร้าง utility ที่รับ `TFace`, `TBody`, `TMode`, `X`, `Y` แล้วทำตาม contract ที่ยืนยันได้:

```text
record = BodyFace[TMode]
body_image = imgBody[TBody]
face_image = imgFace[TFace]
วาด body crop ตาม record[0..5]
วาด face crop ตาม record[6..11]
บันทึก branch/offset adjustment ที่ใช้
```

ผลลัพธ์ควรเป็น diagnostic renderer ที่ trace ได้ ไม่ใช่ animation player และต้องแยกกรณี
ที่ resource-index mapping ยังไม่ถูกพิสูจน์.

### ขั้นที่ 2 — ยืนยัน resource index กับไฟล์จริง

ไล่โค้ดโหลด resource ที่สร้าง `imgBody[]` และ `imgFace[]` แล้วเทียบกับ:

- `game/img.inf`
- filename numeric IDs
- `DDBody`, `DDFace`
- ขนาด/พิกเซลของ crop ที่รู้จัก

ถ้ายังพิสูจน์ไม่ได้ ให้ manifest ใช้ `asset_selector_index` แยกจาก `filename_numeric_id`
และคง mapping เป็น `probable` หรือ `unknown`.

### ขั้นที่ 3 — ปิด BodyFace table provenance

ค้นหา initialization จาก:

- recovered C/assembly รอบ RVA ของ `AddBodyFace`
- constructor/startup ที่ allocate `BodyFace`
- function pointer หรือ callsite ที่ extractor เดิมใช้สร้าง `bodyface_records.reference.json`

เป้าหมายคือยืนยันว่า record mode 0–41 เป็นลำดับ runtime จริง ไม่ใช่เพียงรายการที่ parser เก็บได้.

### ขั้นที่ 4 — แยก callsite เป็นสายงาน

จัดกลุ่ม DrawHuman callsites เป็น:

- `HumanDex` preview/debug/catalog path
- `DrawObj` / office object path
- `Syain` employee path
- `Kaiwa` dialogue path
- UI/demo paths ที่ไม่ใช่ office runtime

แต่ละกลุ่มต้องเก็บ selector source, timer source, TMode source และ furniture context แยกกัน
ก่อนจะรวมเป็น state เดียว.

### ขั้นที่ 5 — Trace timer และ state transition

เริ่มจากตัวแปรที่ code ชี้ตรงที่สุด:

- `KeyAnimeT`
- `HumanDexAnime`
- `HumanDexWalk`
- `HumanDexTime`
- `ObjecAnime`
- `SyainFaceG` / `SyainBodyG`
- `KaiwaFaceG` / `KaiwaBodyG`

ทำตาราง `state source → selector expression → TMode → BodyFace mode → asset crop`
โดยไม่เติมชื่อ idle/walking/working จนกว่าจะมี state trigger หรือ function context รองรับ.

### ขั้นที่ 6 — จัดกลุ่ม animation แบบ neutral ก่อน

ใช้ชื่อเช่น `mode_sequence_candidate_000` และเก็บ:

- mode sequence
- body/face source rows
- selector source
- timer expression
- loop evidence
- direction evidence

ค่อย map ไป Agent state เมื่อมีหลักฐานมากกว่ารูปลักษณ์ของ sprite.

### ขั้นที่ 7 — ยืนยัน semantic และสร้าง adapter layer

ผลลัพธ์ของแต่ละ state ใช้ได้ 3 ระดับ:

- `verified`: code/data link ครบ
- `probable`: มีหลายหลักฐาน แต่ยังขาด link สำคัญหนึ่งจุด
- `unknown`: ยังบอกไม่ได้

Adapter ของ Virtual AI Office ต้องแยกจาก original-game facts เสมอ เช่น
`legacy_mode` กับ `agent_state_candidate` คนละ field.

## เกณฑ์ว่าขั้นไหนถือว่าคลี่คลาย

- กลไกประกอบภาพ: มี test case ที่คำนวณ source/destination จาก selector และ record ได้ตรงกับ DrawHuman
- resource mapping: selector index และไฟล์ภาพมีหลักฐานจาก loader หรือ cross-check ที่ไม่พึ่งชื่อไฟล์อย่างเดียว
- animation group: มีลำดับและ timer จาก code ไม่ใช่จากการเรียง mode หรือความรู้สึกจากภาพ
- semantic state: มี callsite/state trigger ที่เชื่อมกับ animation โดยตรง
- placement: แยกเป็นงาน Phase 1 และไม่ถือว่ารูปตัวละครชนเฟอร์นิเจอร์คือหลักฐาน anchor

## งานถัดไปที่คุ้มค่าที่สุด

1. trace loader ของ `imgBody[]`/`imgFace[]` เพื่อปิด index-to-file mapping
2. trace `DrawObj` callsite ที่ `form.c:16325–16333`
3. trace HumanDex update ที่ปรับ `HumanDexAnime`/`HumanDexWalk`
4. จากนั้นค่อยปรับ `agent_state_mapping.json` ถ้ามีหลักฐานใหม่

ไม่ควรเริ่มจากการตั้งชื่อ mode เป็น walking/working หรือทำ GIF loop เพราะจะทำให้
สมมติฐานกลายเป็นข้อมูล canonical ก่อนที่ runtime evidence จะรองรับ.
