# Minimum Wave 2 scene gate 01

อัปเดต: 2026-08-11

## เป้าหมาย

สร้าง boundary ที่ Wave 3 ใช้เริ่มทำ actor state, interaction contract และ stub ได้
โดยไม่เลื่อนสถานะหลักฐานที่ยังเป็น symbolic หรือ unresolved ให้กลายเป็น legacy fact

## สิ่งที่รวมใน fixture

- room asset: `office/floor0.png` และ `office/floor0.seb` พร้อม hash และ SEB tail limitation
- bounded object: `CallHikkosi(param_2=0)` → `DeskImgData[KaishaOffice]` → `AddObjec` → `OfficeObjecList`
- coordinate: centered origin fixture 800×600 → `(280,180)`
- observed draw anchor: `ObjecX + ObjecZX`, `ObjecY + ObjecZY` และ crop
  `ObjecCX/CY/WX/WY` สำหรับ callsites ที่มีหลักฐานตรง
- draw probe: `OBJ_TYPE_RECEPTION` ใช้ทดสอบ dispatch/argument flow แยกจาก bounded room object
- movement boundary: explicit seat/collision/walkable adapter interface

## สิ่งที่ห้ามตีความเพิ่ม

- bounded room object ยังมี `ObjecSyurui` เป็น `selected_desk_record_plus_5`
- reception probe ไม่ได้แปลว่า `CallHikkosi` สร้าง reception object
- candidate sort key 93 เป็น sort probe ไม่ใช่ depth/z ที่ปิดแล้ว
- seat occupancy, collision และ walkable ยังไม่มี legacy producer ที่ยืนยันใน scoped functions

## Acceptance

Wave 3 เริ่มได้ในระดับ contract/state/stub โดยใช้
`artifacts/wave2_wave3_movement_interface.json` เป็น input boundary
แต่ final room renderer, pixel regression และ legacy-equivalent movement ยังต้องรอ
Wave 2 closure pass
