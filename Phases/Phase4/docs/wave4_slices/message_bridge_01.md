# W4-C6 — Message bridge slice

`AddMessage` scan `MessageTime` หา slot ว่าง แล้วเขียน `MessageText`, ตั้ง
`MessageTime`/`MessageMaxTime` เป็น raw value `0x60` และเขียน `MessageGraph`.

ค่า `0x60` ยังไม่ถูกตีความเป็น milliseconds และ `MessageGraph` ยังเป็น raw ID.
Notification ที่ map เข้ากับ dashboard ต้องใช้ adapter contract จนกว่าจะ trace
consumer และ lifecycle event ที่แน่นอนได้.
