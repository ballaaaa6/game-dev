# W4.5-R2 — Talk token และ speaker boundary

`GetTalkIndex` ใช้ `StringUtil.Split` แล้วเทียบ segment แรกกับ tag.
`AddKaiwaTalkData` ทำ optional replace, split, parse token ที่สองเป็น raw speaker ID,
เรียก `GetHumanTalkName` และส่งต่อ `AddKaiwa`.

Literal values ถูกบันทึกจาก table แต่ยังไม่ promote เพราะต้องตรวจ pointer/address และ
raw talk record ร่วมกัน. ไม่พบ direct `AddKaiwaTalkData` caller ใน scoped categorized C
หรือ assembly จึงยังไม่มีหลักฐาน raw speaker → Wave 3 actor โดยตรง.
