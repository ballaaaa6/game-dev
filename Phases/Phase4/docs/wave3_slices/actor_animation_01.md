# Wave 3 C5 — selector and actor draw contract

สถานะ: selector/composition contract และ deterministic draw fixture พร้อมแล้ว; semantic animation ยังไม่ปิด

## หลักฐานที่ยืนยันได้

- `DrawHuman` มี selector contract `TFace`, `TBody`, `TMode` และ overload ที่มี `TKage`
- `TMode` ใช้เลือก `BodyFace[TMode]`; body ใช้ `imgBody[TBody]` กับ fields 0–5 และ face ใช้ `imgFace[TFace]` กับ fields 6–11
- actor `DrawObj` callsite ใช้ raw fields ที่ตรงกับ `HumanFaceG`/`HumanBodyG` สำหรับ selector บางส่วน ส่วน selector ที่สามใน callsite ยังไม่ถูก promote เป็น `HumanMode`/`HumanAnime`
- HumanDex dynamic path เป็น selector flow ที่ verified แต่ยังไม่ใช่ Agent semantic state

## TFace 40/41

callsite ที่เห็นค่า literal 40 และ 41 ถูกเก็บแยกเป็น unresolved selector cases เพราะ Phase 2 asset catalog มี face assets 0–35 และยังไม่มีหลักฐาน index-space mapping ที่ปลอดภัย ค่า raw selector จึงต้องถูกคงไว้ ไม่ substitute เป็น face อื่น

## semantic policy

mode 0–41 เป็น verified record selectors เท่านั้น ไม่ตั้งชื่อ idle/walking/working/sitting จากลำดับภาพหรือ crop geometry; timing, loop, direction, mirroring, shadow branch และ face-change timing คงเป็น `null/unknown` จนกว่าจะมี evidence เพิ่ม
