# Phase 4 — Wave 1 plan: resource truth และ selective trace

อัปเดต: 2026-08-11

## เป้าหมาย

Wave 1 มีเป้าหมายปิด “resource truth” ก่อนเริ่มแปล lifecycle code: ต้องรู้ว่า selector ใน `GameForm` ไหลไปยัง resource index และไฟล์ใด, ระบุจุดที่ยังพิสูจน์ไม่ได้เป็น `unknown`, และสร้างโครงสร้างสำหรับตัด `NewGamePara`/`DoEvent` เป็นช่วงสั้น ๆ ที่ตรวจสอบได้

ขอบเขตของ wave นี้คือ initializer/loader, manifest/index mapping, fixture metadata และ structural assembly index เท่านั้น ยังไม่ใช่การ port gameplay หรือการแก้ source extraction เดิม

## หลักฐานตั้งต้นที่ยืนยันแล้ว

- `ResourceManager__LoadStart` แยก token ด้วย TAB; token แรกที่เป็นตัวเลขคือ resource index และรายการที่ไม่มี index ได้ index ว่างที่ต่ำที่สุดตามลำดับรายการ (`kairo.c`, บรรทัด 108035)
- `ResourceManager__GetImage` lookup ด้วย `img[texId]`; `main_AppData__GetImage` จับคู่ชื่อใน list แล้วคืน resource array ตำแหน่งเดียวกัน (`main.c`, บรรทัด 6462)
- `Method_form_BootForm_GraphicLoad` สร้าง `imgFace` 36 รายการและ `imgBody` 25 รายการ (`Method.c`, บรรทัด 5184 เป็นต้นไป)
- `GameForm.IMG_LIST` ถูก allocate เป็น 80 รายการใน static initializer (`form.c`, ฟังก์ชัน `form_GameForm___cctor`)
- `JarInflater` normalize extension สำหรับ archive และจึงพบรูปแบบ `.png.bytes`; asset ที่ extract แล้วตรวจด้วย `.png` metadata ได้โดยแยกเป็นคนละชั้นของหลักฐาน
- assembly fallback มี `NewGamePara` 13,671 instructions และ `DoEvent` 15,569 instructions จึงต้อง index ก่อนเลือก semantic slice

## แผนงานและเกณฑ์ผ่าน

| ช่วง | งาน | ผลลัพธ์ | สถานะ |
|---|---|---|---|
| W1.1 | Normalize `img.inf`/`seb.inf` | manifest ที่รักษา explicit index และคำนวณ lowest-unused index | เสร็จ |
| W1.2 | Trace resource loader | contract ของ `ResourceManager`, `AppData.GetImage`, `JarInflater` | เสร็จ |
| W1.3 | Trace initializer/selector | `IMG_LIST` 80 entries, `imgFace`/`imgBody` count และ selector expressions | เสร็จบางส่วน; mapping บางจุดยัง unknown |
| W1.4 | สร้าง fixtures | อย่างน้อยหนึ่ง fixture ต่อ family ที่หาไฟล์จริงได้ พร้อม SHA-256/ขนาด | เสร็จ |
| W1.5 | Index assembly | entry/exit, branches, calls และ basic blocks ของสองฟังก์ชัน | เสร็จเชิงโครงสร้าง |
| W1.6 | เลือก lifecycle slice แรก | slice ที่มี entry/exit, field map, neutral pseudocode และ confidence | ถัดไป |

## รายละเอียดการลงมือทำ

### 1. สร้าง resource manifest ที่ deterministic

ตัวสร้าง `tools/build_wave1_resource_map.py` อ่านเฉพาะ source และ asset roots แล้วสร้าง record ต่อบรรทัดใน:

- `game/img.inf`
- `office/img.inf`
- `load/img.inf`
- `office/seb.inf`

แต่ละ record มี manifest line, declared index, assigned index, filename, asset path, family, byte count และ SHA-256 ถ้าหาไฟล์จริงได้ จุดสำคัญคือห้ามใช้เลขท้าย filename เป็น resource index เช่น `body10.png` มี index 3 ตาม manifest ไม่ใช่ 10

### 2. ปิด loader contract

แยกให้ชัดระหว่าง:

1. ชื่อที่ selector สร้าง (`IMG_LIST[...]`, `face_...`)
2. ชื่อที่ `AppData.GetImage` ใช้ค้นใน list
3. resource index ใน `img[]`
4. ไฟล์ที่ถูก extract หรืออยู่ใน archive

ถ้าชั้นใดไม่มีหลักฐานตรง จะคงสถานะ `unknown` และไม่เดาชื่อแทน

### 3. ปิด initializer trace

บันทึกปลายทางและจำนวนที่ allocation เขียนลงจริง:

- `imgFace`: 36 slots, destination offset `0x1150`
- `imgBody`: 25 slots, destination offset `0x1158`
- `imgBihin_`: 3 slotsจาก `DDPC`, `DDChair`, `DDDesk`
- floor/event paths: เก็บ expression และ destination fields แยกจากการ resolve index

เกณฑ์ปิดส่วนนี้เต็มรูปแบบคือ resolve ค่า static base selectors (`DDBody`, `DDFace`, `DDPC`, `DDChair`, `DDDesk`) จากหลักฐานที่เชื่อถือได้ หรือบันทึกว่า out-of-scope พร้อม source reference

### 4. สร้าง fixture และ regression checks

เลือก fixture แรกตาม resource index ที่ resolve ได้จาก family `body`, `face`, `event`, `floor`, `chair`, `desk`, `pc`, `reception` โดยเก็บ dimensions และ hash เพื่อกันการ mapping ผิดแบบเงียบ ๆ

### 5. เตรียม assembly slices

`wave1_branch_index.json` เก็บข้อมูลเชิงโครงสร้างเท่านั้น:

- address ของ instruction และ branch target
- `bl`/`blr` call targets ที่ยังเป็น unresolved address
- basic-block starts/ends
- call frequency ต่อ target

ยังไม่ตั้งชื่อ field หรือความหมายของ branch จาก raw offset เกณฑ์ผ่านของ W1.5 จึงเป็น “index ครบและ reproducible” ไม่ใช่ semantic translation เสร็จ

## ผลลัพธ์ที่สร้างแล้ว

- `artifacts/resource_selector_map.json`
- `artifacts/wave1_branch_index.json`
- `artifacts/wave1_build_manifest.json`
- `tools/build_wave1_resource_map.py`
- `tests/test_wave1_resource_map.py`

## Known gaps ที่ต้องไม่กลบด้วยการเดา

- literal ที่ recovered C ระบุเป็น `StringLiteral_7514` มีค่าที่ extract ได้เป็น `false`; ยังไม่ใช่หลักฐานว่า face filename prefix คือ `false` จึงเก็บ `imgFace` mapping เป็น `unknown`
- expression ของ `imgBody` ยืนยันได้ว่าใช้ `IMG_LIST[DDBody+i]` แต่ค่า static `DDBody` ยังไม่ถูก resolve เป็น scalar ที่เชื่อถือได้
- `IMG_LIST` มีบางชื่อที่ไม่ match game image manifest (`bold`, `dest`, และชื่อข้อความ/utility อื่น ๆ); ถูกเก็บเป็น `unknown_or_not_a_game_image`
- branch index ยังไม่บอกว่า branch ใดคือ initialization, reset, exit หรือ event transition

## ลำดับงานถัดไป

1. Resolve ค่า static base selectors จาก `dump.cs`, static initializer และ callsites ที่เขียน field เหล่านี้
2. เลือก slice เล็กสุดของ `NewGamePara` ที่อ่าน selector แล้วเรียก loader; แปลเป็น neutral pseudocode พร้อม field/source map
3. เลือก slice แรกของ `DoEvent` ที่มี entry/exit ชัดและไม่ปนกับ branches ที่ยังไม่รู้ความหมาย
4. อัปเดต selector-to-file mapping และ Phase 1/2 manifests เฉพาะเมื่อมีหลักฐานใหม่

