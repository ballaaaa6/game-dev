# W4-C2 — Talk data slice

เส้นทางที่ตรวจ: `GetTalkIndex → GetTalkTexts → AddKaiwaTalkData → GetHumanTalkName
→ AddKaiwa`.

`GetTalkIndex` มี bounded scan/split/compare และคืน `-1` เมื่อไม่พบ tag.
`AddKaiwaTalkData` parse raw speaker/chara value แล้วส่งต่อชื่อและข้อความให้
`AddKaiwa`. ชื่อ special speaker IDs ยังไม่ promote เป็น semantic label.

Fixture ใช้ `fixture.tag` เป็น neutral record และไม่อ้างว่าเป็น production talk tag.
