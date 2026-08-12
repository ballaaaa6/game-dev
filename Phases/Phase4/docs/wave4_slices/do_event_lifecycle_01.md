# W4-C4 — DoEvent dialogue/message target slice

`DoEvent` ยังไม่มี categorized C ที่เชื่อถือได้ จึงใช้ assembly fallback และเก็บเฉพาะ
call-target ที่ map ผ่าน `dump.cs` RVA:

- `0x00f1a908`, `0x00f1a98c`, `0x00f4b038` → `AddKaiwa` overloads;
- `0x00f4a714` → `AddMessage(string,int)`;
- `0x00f1aa34` → `EventGChange`;
- `0x00f3ab48` → `Print`.

นอกจากนี้มี raw reads ของ `EventMode`, `EventTemp`, `EventTemp2`. การเก็บนี้เป็น
target/field index เท่านั้น ไม่ใช่การตั้งชื่อ event mode หรือการอธิบาย branch semantics
ของ `DoEvent` ทั้งฟังก์ชัน.
