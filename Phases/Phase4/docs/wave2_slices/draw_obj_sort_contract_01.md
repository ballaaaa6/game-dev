# DrawObj — dispatch และ sort contract 01

อัปเดต: 2026-08-11

## สิ่งที่ยืนยันได้

- `DrawObj` มี compare-and-swap pattern ก่อนวาด object
- dispatch ที่ยืนยันจาก `dump.cs` และ callsite คือ parts, human, display, chair,
  desk, CEO desk และ reception
- `ObjecUpDown` ถูกใช้เป็น array ที่เก็บลำดับ/สถานะการจัด object ในเส้นทางนี้
- comparator อ่านค่าจาก raw offsets ที่ join กลับได้กับ `ObjecSY` และ `ObjecY`

## Neutral contract

```text
prepare ordered object slots
for each candidate slot:
    compare candidate components using recovered integer expressions
    swap/order slots when the recovered comparison requires it

for each ordered slot:
    dispatch ObjecSyurui[slot]
    call the corresponding renderer
```

การเรียก comparator ว่า depth sort ยังไม่ใช่ข้อสรุป เพราะ field semantics ของ expression
ยังไม่ถูกยืนยันครบ จึงเก็บชื่อเป็น neutral component ใน artifact
`wave2_draw_order_contract.json`
