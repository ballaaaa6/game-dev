# Phase 4 Wave 4 — Closure report

อัปเดต: 2026-08-11

สถานะ: **W4-C0 ถึง W4-C7 ปิดรอบแบบ `complete_with_known_limitations`**

รอบนี้ปิดหลักฐาน dialogue, bubble และ notification consumer ที่ bounded แล้ว:

- `MainProcess` ลด `HumanFukiTime` และใช้ค่าที่เป็นบวกเป็น gate ก่อนการวาดใน `DrawObj`;
- `MainProcess` ลด `MessageTime`, compaction `MessageText/MessageTime/MessageGraph`
  เมื่อหมดอายุ และอ่าน `MessageMaxTime` ใน threshold สำหรับ `SoundPlay`;
- `DoEvent` มี raw field reads ของ `EventMode/EventTemp/EventTemp2` และมี call-target
  ที่ map กับ `AddKaiwa`, `AddMessage`, `EventGChange` และ `Print` ผ่าน RVA ใน `dump.cs`;
- `MainProcess` มี bounded producer callsites ของ `AddEvent`, `AddMessage`, `CallFuki`
  และ `AddKaiwa` ซึ่งเก็บไว้เป็น raw callsite index ไม่ใช่ semantic event table.

## Artifacts

- `Phases/Phase4/artifacts/wave4_lifecycle_slices.json`
- `Phases/Phase4/artifacts/wave4_c7_build_manifest.json`
- `Phases/Phase4/docs/wave4_slices/mainprocess_lifecycle_01.md`
- `Phases/Phase4/docs/wave4_slices/do_event_lifecycle_01.md`

## Boundaries retained

ยังไม่ปิดหน่วยของ timer `0x60`/counter, label ของ `MessageGraph`, semantic name ของ
numeric event modes, delimiter/token semantics, raw speaker-to-actor binding และ
ความหมายของ `HumanMode`. `DoEvent` ยังเป็น assembly fallback จึงยังไม่แปลง branch graph
เป็น implementation ที่อ้างว่าเทียบเท่า legacy.

ผลลัพธ์นี้พร้อมเป็น Phase 5 handoff สำหรับ adapter implementation และ targeted trace
ต่อเมื่อมี feature ที่ต้องใช้ semantics เหล่านี้โดยตรง.
