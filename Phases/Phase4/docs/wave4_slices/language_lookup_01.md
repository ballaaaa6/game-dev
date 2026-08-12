# W4-C1 — Language lookup slice

หลักฐานหลัก: `Phases/Phase3/docs/kairosoft_language_system.md`, language CSV 12 ไฟล์,
`Language.SetTextTable`, `MakeTextTable`, `TranslateText`, `_translateText2`.

สิ่งที่ยืนยันใน bounded scope:

- CSV มี metadata และ language IDs เดิม
- current extraction ไม่มี English CSV
- runtime มี text-table setup, translation และ cache boundary
- placeholder ต้องถูกเก็บเป็น token และตรวจ argument ก่อนแทนค่า

สิ่งที่ยังไม่ปิด: ความหมาย token เฉพาะเกม, fallback แบบ legacy และการเลือกข้อความ
สำหรับ dashboard ทั้งหมด.
