# W4.5-R4 — Event mode candidate trace

เพิ่ม target clusters ของ `DoEvent` สำหรับ `AddKaiwa`, `AddMessage`, `EventGChange` และ
`Print` พร้อม nearby immediate constants และ raw `EventMode/EventTemp/EventTemp2` refs.

ผลลัพธ์เป็น target-context evidence เท่านั้น ไม่ใช่ event-mode mapping. Numeric modes
ยังไม่ถูกตั้งชื่อ และ Wave 5 ควรใช้ named adapter events แทน.
