# Draw-order fixture — neutral compare probe 01

อัปเดต: 2026-08-11

## ขอบเขต

- function: `form.GameForm.DrawObj`
- fixture: `artifacts/wave2_draw_order_fixture.json`
- contract: `artifacts/wave2_draw_order_contract.json`

## Fixture

fixture ใช้ object records สามรายการ โดยคำนวณ candidate key แบบที่ recovered C
แสดงเป็น `ObjecSY + ObjecY`

| slot | type | ObjecSY | ObjecY | candidate key |
|---:|---|---:|---:|---:|
| 0 | desk | 20 | 300 | 320 |
| 1 | chair | 10 | 120 | 130 |
| 2 | reception | 15 | 200 | 215 |

ผลลัพธ์ที่คาดหมายคือ draw order `[1, 2, 0]` โดยใช้ slot เป็น tie-break เพื่อให้
fixture deterministic

## ข้อจำกัด

นี่เป็น `neutral_sort_probe` ที่ทดสอบ compare-and-swap pattern และ field join เท่านั้น
ยังไม่เรียก key นี้ว่า depth หรือ z semantics จนกว่าจะมี assembly/pixel behavior ยืนยัน
และยังไม่ได้สร้าง pixel snapshot เพราะ room placement ยังไม่ปิด
