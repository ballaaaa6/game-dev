# W4.5-R1 — Timer และ HumanFuki lifecycle

`form_GameForm___update` เรียก `MainProcess` ด้วยจำนวนรอบที่ขึ้นกับ config; หลักฐานนี้
รองรับ logical tick/speed multiplier candidate แต่ยังไม่มี direct delta-time mapping.

`CallFuki` เขียน `HumanFukiTime` และ `HumanFukiIndex`; `MainProcess` ลด timer ที่เป็นบวก;
`DrawObj` ตรวจ timer ก่อนอ่าน index และเรียก `DrawFukidashi`. ไม่พบ clear ของ index ใน
scoped MainProcess expiry path จึงต้องให้ Wave 5 adapter ลบ expired bubble state เอง.
