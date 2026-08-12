# W4-C4 — Event dispatch slice

`AddEvent` scan first-free slot แล้วเขียน `EventMode/EventTemp/EventTemp2`.
Callsite inventory เก็บ raw mode expressions และไม่ตั้งชื่อ semantic event.

`DoEvent` ยังเป็น assembly fallback ขนาดใหญ่; งานถัดไปคือ slice เฉพาะ branch ที่แตะ
`AddKaiwa`, `AddMessage`, `CallFuki` หรือ actor lifecycle.
