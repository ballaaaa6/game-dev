# Furniture / seat / placement trace 01

อัปเดต: 2026-08-11

## สิ่งที่ยืนยันได้

- `GetPcImgData`, `GetDeskImgData`, `GetChairImgData` อ่าน array ที่ตรงกับ
  `PCImgData`, `DeskImgData`, `ChairImgData` และ normalize `param_1` ด้วย remainder
  ของ array length ก่อนคืน slot
- `CallPCChange` เชื่อม `PCImgData`, `PCObjec`, `DeskZahyou` และ object arrays หลายตัว
- `CallDeskChange` เชื่อม `DeskImgData`, `DeskObjec`, `DeskZahyou`, `ObjecSyurui`
  และ object arrays
- `CallChairChange` เชื่อม `ChairImgData`, `ChairMainObjec`, `ChairSubObjec`,
  `DeskZahyou` และ object arrays
- `LoadBihinImage` โหลด image เข้า `imgBihin_`
- ใน `CallHikkosi`, branch `param_2 == 0` มี bounded trace ที่อ่าน `DeskImgData` ด้วย
  `KaishaOffice`, ตรวจ record length แล้วเรียก `AddObjec` ด้วยค่าคงที่ที่อ่านได้จาก source
  ก่อนเขียน object index เข้า `OfficeObjecList`

รายละเอียดและ source line references อยู่ใน
`artifacts/wave2_furniture_contract.json` และ
`artifacts/wave2_placement_fixture.json`

## ยังไม่สรุป

- numeric office record และ object list แบบ end-to-end
- การ assign employee ให้ seat หรือ occupancy state
- collision และ walkable zones ใน scoped scene functions

ดังนั้น web layer ห้ามถือว่าการมี chair asset หรือ `ChairMainObjec` แปลว่า seat ถูกใช้งาน
และห้ามสร้าง collision/walkable geometry จากภาพ furniture เอง
