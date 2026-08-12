# W4-C4/C6 — MainProcess and DrawObj consumer slice

หลักฐานจาก categorized `form.c` ถูกจำกัดไว้ที่ function spans และ raw offsets ใน
`wave4_lifecycle_slices.json`.

- `MainProcess` ลด `HumanFukiTime` เมื่อค่าปัจจุบันมากกว่า 0;
- `DrawObj` ตรวจค่า `HumanFukiTime > 0`, อ่าน `HumanFukiIndex` และเรียก
  `DrawFukidashi`;
- `MessageTime` ถูกลดลงในสอง branch ที่ bounded ได้;
- เมื่อ timer ถึงศูนย์ มีการ shift `MessageText`, `MessageTime`, `MessageGraph`
  และ clear ช่องสุดท้าย;
- `MessageMaxTime - MessageTime == 1` เป็นหลักฐาน threshold ที่นำไปสู่ `SoundPlay`.

หน่วย timer, การล้าง `HumanFukiIndex` เมื่อหมดอายุ และชื่อ graph/UI category ยังไม่
ถูกสรุปจาก slice นี้.
