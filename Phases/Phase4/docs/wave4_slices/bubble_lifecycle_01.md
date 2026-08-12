# W4-C3 — Fukidashi bubble slice

`AddFuki` ยืนยันการเขียน `FukiCX/FukiCY/FukiWX` และเพิ่ม `FukiMax`.
`CallFuki` ยืนยัน bounded writes ไปยัง `HumanFukiIndex/HumanFukiTime` หลัง limit
checks. `DrawFukidashi` อ่าน `fukiList`, เรียก `Language.LT`, trim และส่งเข้า
`Balloon.Draw`.

Timer unit และ expiry consumer ยังต้อง trace ใน `MainProcess/DrawObj`; fixture จึงใช้
deterministic adapter clock และติดป้าย non-legacy.
