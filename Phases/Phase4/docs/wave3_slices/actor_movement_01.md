# Wave 3 C3 — target / position flow and movement adapter

สถานะ: สร้าง contract และ deterministic fixture แล้ว; legacy movement semantics ยังไม่ปิด

## หลักฐานที่ปิดได้

- `AddTarget(TIndex, TX, TY)` เขียนค่าเข้า raw arrays `TargetX[TIndex]` และ `TargetY[TIndex]`
- `NextTarget(TPos, THumanIndex, TMode)` เมื่อ `TMode == 0` คัดลอก target ไปยัง `HumanX/HumanY`
- `NextTarget` มีการคัดลอก target ไปยัง `HumanPX/HumanPY` ใน bounded path ที่เหลือ
- `CallHikkosi` และ `CallSyain` เป็น callers ที่เห็นจาก source/call graph

## ขอบเขตที่ยังไม่อ้างว่าเทียบเท่า

จาก source นี้ยังไม่ควรเรียก `HumanX/HumanY` ว่า current position ในทุก context หรือ `HumanPX/HumanPY` ว่า previous position โดยอัตโนมัติ นอกจากนี้ `TargetX/Y` เป็น target arrays ไม่ใช่ path graph ที่พิสูจน์แล้ว และ Wave 2 ยังไม่พบ legacy collision, walkable หรือ seat producer ที่ปิดได้

## adapter fixture

fixture ใช้ path ที่ inject จาก adapter, เดินทีละ waypoint ต่อ tick, ไม่ teleport เมื่อ collision เป็น `blocked`, และคงตำแหน่งเดิมเมื่อ provider ให้ `no_path` หรือ `unavailable` พฤติกรรมทั้งหมดติดป้าย `legacy_equivalence: false` จนกว่าจะมีหลักฐาน producer/runtime เพิ่มเติม

ดูรายละเอียดและ evidence refs ใน `wave3_movement_contract.json` และ `wave3_movement_fixture.json`
