# Character Data Reference — Current Extraction

สถานะเอกสาร: อ้างอิงจาก extraction ชุดปัจจุบันเท่านั้น

เอกสารนี้เขียนใหม่เพื่อแทนคู่มือจาก build/workspace รุ่นเก่า ข้อมูลจาก
`web/`, `tools/`, `data/builds/`, build ID เก่า หรือ APK hash เก่า ห้ามใช้เป็น
หลักฐานของ runtime ปัจจุบันจนกว่าจะตรวจเทียบกับ dump และ asset ชุดใหม่

## Source of truth

- `game-dev-story-mod_Dumped/bodyface_records.reference.json`
- `game-dev-story-mod_Dumped/Categorized_Code/`
- `game-dev-story-mod_Sprites/game/`
- `game-dev-story-mod_Sprites/office/`

## สิ่งที่ยืนยันได้จากข้อมูลปัจจุบัน

### Body-face records

`bodyface_records.reference.json` มี record `mode` ตั้งแต่ `0` ถึง `41`
รวม 42 records แต่ละ record มีข้อมูลที่ตรวจสอบได้ เช่น:

- `callsite`
- `body_src_x`, `body_src_y`, `body_width`, `body_height`
- `body_dst_x`, `body_dst_y`
- `face_src_x`, `face_src_y`, `face_width`, `face_height`
- `face_dst_x`, `face_dst_y`
- `shadow_dst_x`, `shadow_dst_y`

นี่พิสูจน์ได้ว่า runtime มีข้อมูล crop/offset แบบ data-driven แต่ยังไม่ได้พิสูจน์
ความหมายเชิง semantic ของทุก mode

### Current character assets

จาก `game-dev-story-mod_Sprites/game/`:

- `body0.png` ถึง `body25.png` รวม 26 ไฟล์
- body 25 ไฟล์มีขนาด `102×66`
- `body25.png` มีขนาด `65×66` และต้องถือเป็นกรณีพิเศษจนกว่าจะ trace เพิ่ม
- `face_0.png` ถึง `face_35.png` รวม 36 ไฟล์ ขนาด `80×30`

ขนาดเหล่านี้เป็นผลจากไฟล์ที่ตรวจจริง ไม่ใช่ค่าที่คัดลอกจากคู่มือเก่า

### Function entry points ที่ควร trace

ใน `Categorized_Code` พบชื่อ function ที่เกี่ยวข้องกับการตรวจระบบตัวละครและ
การวาด เช่น:

- `form_GameForm__AddBodyFace`
- `form_GameForm__DrawHuman`
- `form_GameForm__GetChairImgData`
- `form_GameForm__GetDeskImgData`
- `form_GameForm__DrawDesk`
- `form_GameForm__DrawChair`
- `form_GameForm__DrawFukidashi`
- `form_GameForm__GetTalkIndex`
- `form_GameForm__GetHumanTalkName`

ชื่อ function เป็นจุดเริ่มต้นในการศึกษา ไม่ใช่ข้อสรุปว่า function ทำงานอย่างไร
ต้องอ่าน body, callsite และข้อมูลที่ส่งเข้าไปประกอบกัน

## สิ่งที่ยังห้ามสรุป

ข้อมูลปัจจุบันยังไม่ยืนยันสิ่งต่อไปนี้:

- mode 0–41 แต่ละตัวคือ walk, sit, work, talk หรือ emote อะไร
- ทิศทางของ mode แต่ละตัว
- mode ใดเป็น animation loop และ mode ใดเป็นภาพเดี่ยว
- ลำดับการวาด body กับ face ในทุกกรณี
- body/face asset ใดเป็นคู่ที่ runtime เลือกใช้จริงในแต่ละตัวละคร
- `body25.png` ใช้กับ state ใด

ดังนั้นการแบ่งกลุ่ม mode แบบ `walk 0–15`, `desk 20–23` หรือชื่อ semantic อื่น ๆ
ให้ถือเป็นสมมติฐานจนกว่าจะมี trace จาก code หรือการเทียบภาพกับ callsite รองรับ

## ขั้นตอนสร้าง character catalog

1. อ่าน records ทั้ง 42 รายการและตรวจว่า source rectangle อยู่ใน asset จริง
2. ทดลอง compose body/face ตาม `src` และ `dst` ของแต่ละ record
3. สร้าง preview ที่ติดป้ายเพียง `mode_00` ถึง `mode_41`
4. trace `form_GameForm__AddBodyFace` และ `form_GameForm__DrawHuman`
5. เทียบ callsite กับตำแหน่งที่ `GameForm` เรียกใช้ mode
6. จึงค่อยตั้งชื่อ semantic เช่น `walking` หรือ `working` เมื่อมีหลักฐาน

## Manifest ที่ต้องสร้าง

```json
{
  "mode": 0,
  "body_asset": "game/body0.png",
  "face_asset": "game/face_0.png",
  "record_source": "game-dev-story-mod_Dumped/bodyface_records.reference.json",
  "callsite": "0x00e2...",
  "semantic": null,
  "confidence": "verified-record-only"
}
```

`semantic` ให้เป็น `null` จนกว่าจะพิสูจน์ได้ และ `confidence` ต้องแยกอย่างน้อย
`verified-record-only`, `code-correlated`, `visual-confirmed`

## เกณฑ์ผ่าน

- compose ทุก mode ได้โดยไม่เดา crop หรือ offset
- ไม่มีการ mirror หรือสร้าง shadow ใหม่โดยไม่มีหลักฐาน
- แยกข้อมูลที่ยืนยันแล้วออกจากข้อมูลที่ยังเป็นสมมติฐาน
- ตัวละครเว็บใช้ asset เดิมก่อนที่จะพิจารณาสร้าง asset ใหม่
