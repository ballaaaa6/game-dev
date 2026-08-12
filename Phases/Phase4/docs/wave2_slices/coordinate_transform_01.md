# Coordinate transform — verified center-origin fixture 01

อัปเดต: 2026-08-11

## ขอบเขต

- source: `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c`
- caller evidence: `form.GameForm.Draw` / `DrawFloorCover`
- fixture: `artifacts/wave2_coordinate_fixture.json`

## สิ่งที่ยืนยันได้

ใน render path มีการอ่าน `GameWidth` และ `GameHeight` แล้วเลือก candidate จาก
`size - 0xF0` เมื่อผลไม่ติดลบ มิฉะนั้นใช้ `size - 0xEF` จากนั้นเรียก
`Graphics.SetOrigin(candidate >> 1, ...)` เมื่อใช้ input fixture 800x600 ผลคือ
origin `(280, 180)`

`DrawFloorCover` รับ offset ที่สัมพันธ์กับ origin และใช้ record fields `+0x20`, `+0x24`
เป็นส่วนหนึ่งของปลายทาง draw image ส่วน object path อ่าน `Graphics.GetOriginX` และ
object record arrays ที่ join ได้กับ `ObjecX`, `ObjecY`, `ObjecCX`, `ObjecCY`, `ObjecWX`,
`ObjecWY`, `ObjecSY`

## สิ่งที่ยังไม่สรุป

- ยังไม่มีหลักฐานตรงพอสำหรับ isometric projection หรือ world-to-tile transform
- ยังไม่รู้ว่า `ObjecSY`, `ObjecZX`, `ObjecZY` เป็น depth, layer, pivot หรือ component อื่น
- fixture นี้จึงทดสอบเฉพาะ arithmetic ของ centered graphics origin ไม่ใช่ room placement

ห้ามใช้ fixture นี้เพื่ออนุมานตำแหน่ง furniture จากภาพหรือ alpha bounds
