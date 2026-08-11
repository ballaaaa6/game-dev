# Grid, Map และ Depth — Current Extraction Investigation

สถานะเอกสาร: research plan จากข้อมูลปัจจุบัน ยังไม่ใช่ runtime contract

เอกสาร grid เดิมอธิบาย `mapGrid`, A* และ Y-sorting แบบสรุปสำเร็จรูป แต่จาก
ข้อมูลชุดใหม่ยังไม่ควรยืนยันว่าเกมใช้รูปแบบนั้นทั้งหมด จึงเปลี่ยนเอกสารนี้ให้
เป็นรายการสิ่งที่ต้องพิสูจน์จาก asset และ decompiled code

## Current visual evidence

จาก `game-dev-story-mod_Sprites` ปัจจุบัน:

- `office/` มี 170 ไฟล์: PNG 146, SEB 22, INF 2
- `game/` มี 155 ไฟล์: PNG 151, SEB 2, INF 2
- `com/` มี 68 ไฟล์: PNG 37, SEB 29, INF 2
- `system/` มี PNG 12 ไฟล์

ตัวเลขนี้บอกขอบเขตของ asset ที่ต้องจัดหมวด แต่ยังไม่บอกว่าไฟล์ใดเป็น floor,
wall, collision หรือ foreground จนกว่าจะดูภาพและ trace การเรียกใช้

## Function entry points ที่ควรศึกษา

ใน dump ปัจจุบันพบ function ที่เป็นจุดเริ่มต้นของการ trace เช่น:

- `form_GameForm__Draw`
- `form_GameForm__DrawFloorCover`
- `form_GameForm__DrawObj`
- `form_GameForm__DrawHuman`
- `form_GameForm__DrawDesk`
- `form_GameForm__DrawChair`
- `form_GameForm__SetOrigin`
- `form_GameForm__SetScale`
- `form_GameForm__OnTouchCamera`
- `form_GameForm__GetGameWidth`
- `form_GameForm__GetGameHeight`
- `form_GameForm__NextPoint`
- `form_GameForm__Distan`
- `form_GameForm__Atan2`

ชื่อเหล่านี้เป็นหลักฐานว่ามีระบบวาด ขนาด กล้อง และการคำนวณตำแหน่งบางส่วน
แต่ยังไม่เพียงพอที่จะสรุปว่าใช้ grid แบบใดหรือใช้ A* หรือไม่

## สิ่งที่ยังไม่ยืนยัน

ห้ามถือข้อความต่อไปนี้เป็นข้อเท็จจริงจนกว่าจะ trace เพิ่ม:

- โลกเป็น 2D grid แบบ array ค่า 0/1/2
- pathfinding ใช้ A*
- collision ผูกกับตัวเลขใน `mapGrid`
- z-index ใช้ `sprite.y` โดยตรง
- ทุก furniture occupies หนึ่ง tile หรือมี footprint คงที่
- coordinate เป็น isometric ตามทิศทางที่เอกสารเก่าระบุ

ตัวอย่าง JavaScript หรือภาพประกอบในเอกสารรุ่นเก่าเป็นเพียง model สำหรับทดลอง
เว็บ ไม่ใช่การยืนยัน behavior ของเกมต้นฉบับ

## วิธีพิสูจน์ระบบจริง

1. จัดกลุ่ม asset ใน `office/` และ `game/` พร้อมขนาดภาพและชื่อ archive
2. ค้น callsite ของ `DrawFloorCover`, `DrawObj`, `DrawHuman`, `DrawDesk`
3. อ่านค่าพิกัดที่ส่งเข้า renderer และตรวจว่ามาจาก data structure ใด
4. ตรวจลำดับการเรียกวาดเพื่อพิสูจน์ depth ordering
5. ค้น function ที่อ่าน occupancy, seat, wall, door หรือ walkable state
6. ทดสอบตำแหน่งจริงจาก callsite ก่อนตั้งชื่อระบบว่า grid, collision หรือ pathfinding
7. เขียนผลลง `Phases/Phase1/artifacts/office_manifest.json` พร้อม source function และ confidence

## Web adapter ที่ควรทำหลัง trace

เว็บสามารถเริ่มด้วย model ที่เรียบง่ายได้ แต่ต้องติดป้ายว่าเป็น adapter ของเว็บ:

```ts
type OfficeObject = {
  id: string;
  asset: string;
  position: { x: number; y: number };
  layer?: number;
  walkable?: boolean;
  source?: string;
  confidence: 'verified' | 'probable' | 'unknown';
};
```

ห้ามนำกฎ Y-sort, collision หรือ pathfinding ที่ยังไม่พิสูจน์ไปฝังเป็น core logic
จนกว่าจะมีหลักฐานจาก dump/asset ปัจจุบัน

## เกณฑ์ผ่าน

- ห้องที่แสดงบนเว็บอ้าง asset และ coordinate จาก manifest
- ทุก collision/seat/zone ที่ใช้มี source หรือถูกระบุว่าเป็น web-only adapter
- depth ordering ผ่าน visual test หลายตำแหน่ง
- แยกสิ่งที่ยืนยันจากสิ่งที่สร้างขึ้นเพื่อให้เว็บทดลองได้

## Phase 1 evidence ที่สร้างแล้ว

ชุด artifact ปัจจุบันแยกหลักฐานออกจากสมมติฐานไว้ดังนี้:

- `Phases/Phase1/artifacts/phase1_code_trace.json` index function renderer 14 จุดและ claim ที่ยืนยันได้ 18 รายการ เช่น DrawObj dispatch, image slot ของ chair/desk/reception และโครงสร้าง DrawFloorCover
- `Phases/Phase1/artifacts/office_manifest.json` ครอบคลุม office PNG 146 และ SEB 22 พร้อม bonus catalog, dimensions, pairing และ confidence; ค่า placement/anchor/collision/seat ยังเป็น `unknown`
- `Phases/Phase1/artifacts/phase1_seb_manifest.json` ถอด SEB ได้เชิงโครงสร้าง 53 ไฟล์ โดยคง tail shortfall 4 ไบต์ทุกไฟล์ไว้เป็น anomaly ไม่เติมศูนย์; ยังไม่สรุปว่าเป็น legacy variant หรือ extraction boundary
- `Phases/Phase1/docs/phase1_office_preview.png` และ `phase1_office_floor_contact_sheet.png` เป็นภาพตรวจด้วยตาเท่านั้น ไม่ใช่ runtime coordinate contract
- `Phases/Phase1/artifacts/phase1_validation_report.json` และ `Phases/Phase1/docs/phase1_asset_report.md` ตรวจ hash, reference, trace และ preview artifacts แล้วได้ `pass_with_warnings`
