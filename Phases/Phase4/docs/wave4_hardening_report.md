# Phase 4 Wave 4.5 — Evidence hardening report

อัปเดต: 2026-08-11

สถานะ: **bounded hardening complete; Wave 5 handoff พร้อม โดยยังคง known limitations**

## สิ่งที่แกะเพิ่มได้

- `__update` เรียก `MainProcess` ด้วยจำนวนรอบที่สังเกตได้ `1/2/16` จึงบันทึก
  timer เป็น logical-tick candidate และยังไม่อ้างเป็น milliseconds;
- `HumanFukiTime` ถูกลดลงและใช้เป็น draw gate ส่วน `HumanFukiIndex` ถูกอ่านเพื่อเลือก
  text index แต่ไม่พบ clear ตอนหมดอายุใน MainProcess scope;
- `AddKaiwaTalkData` ยืนยัน pipeline `Replace → Split → Parse → GetHumanTalkName → AddKaiwa`;
  actor binding ยังเป็น adapter boundary และ literal pointer values ต้อง validate กับ raw records;
- `MessageGraph` consumer ใน `form_GameForm___draw` ยืนยัน render behavior ของค่า `1/2`
  ผ่าน `imgMain` crop แต่ยังไม่ตั้งชื่อ product label; `SoundPlay` threshold ถูกบันทึกแล้ว;
- `DoEvent` เพิ่ม target clusters และ nearby constant context แต่ยังไม่ตั้งชื่อ numeric event modes.

## Wave 5 decision

W4.5 ไม่เป็น blocker ต่อ Wave 5. ให้ใช้ adapter tick, explicit bubble cleanup,
raw MessageGraph IDs และ named web events โดยคง `legacy_equivalence=false`.

รายละเอียดอยู่ใน `artifacts/wave4_*_trace.json` และ slice docs ชุด `*_02.md`.
