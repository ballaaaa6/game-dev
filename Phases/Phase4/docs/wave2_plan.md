# Wave 2 — Office scene truth

อัปเดต: 2026-08-11

Wave 2 เริ่มจาก contract และ evidence ไม่ใช่ web renderer implementation เป้าหมาย
คือทำให้ room asset, object record, selector namespace, coordinate และ draw dispatch
สามารถตรวจสอบย้อนกลับไปยัง source ได้ ก่อนส่งต่อให้ Wave 3 และ Phase 5

## สถานะที่สร้างแล้ว

- W2-C0: baseline จาก Wave 1 ถูกใช้เป็น input และคง source roots แบบ read-only
- W2-C1: สร้าง `artifacts/wave2_selector_adapter.json` โดยยังไม่ hardcode ค่า static selector
- W2-C2: สร้าง `artifacts/scene_contract.json` และ map `AddObjec` argument-to-field
- W2-C3: สร้าง room asset fixture จาก `office/floor0.png` และ `office/floor0.seb` โดยคง
  SEB tail shortfall 4 bytes และยังไม่อ้าง placement
- W2-C4: สร้าง coordinate-space evidence index และ centered-origin arithmetic fixture โดยยังไม่ปิด transform semantics
- W2-C5: สร้าง draw dispatch/sort evidence index และ neutral compare-and-swap fixture โดยยังไม่ปิด depth semantics
- W2-C6: สร้าง furniture accessor/relation contract และ bounded `CallHikkosi` placement fixture
  โดยยังไม่ปิด seat, collision, walkable และ full room placement
- W2-C7 (minimum gate): รวม room/object/coordinate/draw boundary เป็น
  `wave2_minimum_scene_fixture.json` และกำหนด Wave 3 movement interface โดยคง room object type
  เป็น symbolic และแยก dispatch probe ที่ verified ออกจาก bounded placement record

## Minimum Wave 2 gate ที่ทำแล้ว

| Gate | หลักฐาน | สถานะ |
|---|---|---|
| room asset | `floor0.png` + `floor0.seb` พร้อม hash และ SEB limitation | ผ่าน |
| object producer | bounded `CallHikkosi(param_2=0)` → `AddObjec` → `OfficeObjecList` | ผ่านแบบ symbolic type |
| coordinate | centered origin 800×600 → `(280,180)` และ observed anchor/crop formula | ผ่านเฉพาะ observed callsites |
| draw boundary | neutral compare fixture + verified reception dispatch probe | ผ่านแบบ neutral |
| movement boundary | seat/collision/walkable explicit adapter interface | ผ่านแบบ non-legacy adapter |
| legacy semantic closure | depth, full placement, seat occupancy, collision, walkable | ยังเปิด |

เกณฑ์นี้ทำให้เริ่ม Wave 3 ได้ในระดับ contract, state model และ stub โดยไม่ต้องรอ
numeric selector หรือ legacy movement semantics ที่ยังไม่มีหลักฐาน ส่วน final scene renderer
ยังต้องรอการปิดรายการแถวสุดท้าย

## แผนลงมือต่อแบบละเอียด

1. **Scene closure pass** — ขยาย `CallHikkosi` branch และตรวจ producer ของ office record ให้ได้
   object type/ตำแหน่งที่ไม่เป็น symbolic; ถ้ายังหาไม่ได้ให้คง gap และไม่เลื่อนสถานะด้วยภาพ
2. **Coordinate validation pass** — ตรวจ observed anchor formula กับ assembly หรือ runtime/pixel
   evidence; แยก transform ที่ verified ออกจาก adapter transform ที่เสนอ
3. **Depth validation pass** — ตรวจ compare-and-swap กับ multi-object behavior และตั้งชื่อ depth
   เฉพาะเมื่อมีหลักฐานรองรับ
4. **Movement evidence pass** — trace caller ที่เขียน employee/seat occupancy และ movement/path
   graph; ถ้าไม่พบ ให้คง Wave 3 interface เป็น adapter-only
5. **Wave 3 handoff pass** — ใช้ `wave2_wave3_movement_interface.json` เป็น input boundary
   สำหรับ actor state/interaction stub โดยไม่สร้าง legacy claim ใหม่
6. **Final closure** — รวม pixel/room regression, update gap register และเปลี่ยน gate เฉพาะเมื่อ
   room placement, draw semantics และ movement limitations ถูกบันทึกครบ

## Stop rules

- ไม่ hardcode `DDBody`, `DDPC`, `DDChair`, `DDDesk` หากยังไม่มี numeric evidence
- ไม่ rewrite `StringLiteral_7514` และไม่ map `TFace=40/41` เข้าสู่ `imgFace[]` โดยเดา
- ไม่ตั้งชื่อ `depth`, `z`, `pivot`, `seat` หรือ `isometric` จากภาพหรือ raw offset เพียงอย่างเดียว
- ไม่ขยาย `NewGamePara`/`DoEvent` นอก bounded slice หากยังไม่มี dependency ที่ใช้จริง
