# Wave 3 C4 — furniture relation and seat boundary

สถานะ: raw relation audit และ explicit seat adapter fixture พร้อมแล้ว; legacy occupancy producer ยังไม่ปิด

## หลักฐานที่ตรวจได้

- `HumanSitChair` ถูกอ่านเป็น index ใน `MainProcess` และใช้ร่วมกับ `ChairMainObjec`/`ChairSubObjec` เพื่อเขียน raw relation arrays ตาม `HumanTime` branch
- `DeskSyain` มี bounded scan/assignment ใน `CallHikkosi` และมี bounded clear ใน `CallSyain`
- `PCObjec` และ `DeskZahyou` ถูกใช้ใน draw path; จึงเป็น render/object relation ไม่ใช่ occupancy proof
- Wave 2 furniture contract ยืนยัน accessor และ relation inputs แต่ไม่พบ producer ที่ผูก raw relation เข้ากับ public actor/seat ownership

## adapter boundary

fixture จึงใช้ `occupy`, `release` และ `query` เป็น explicit adapter state: seat หนึ่งตัวมี owner ได้หนึ่งราย, conflict ไม่เปลี่ยน owner เดิม, release ต้องเป็น owner และ provider unavailable ต้องไม่ mutate state การมีค่า `HumanSitChair` หรือการพบ chair/object array เพียงอย่างเดียวไม่เรียก operation เหล่านี้อัตโนมัติ

ดูรายละเอียด evidence และ scenarios ใน `wave3_interaction_contract.json` และ `wave3_seat_fixture.json`
