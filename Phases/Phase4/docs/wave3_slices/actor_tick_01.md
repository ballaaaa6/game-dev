# W3-C0 — Actor tick evidence slice 01

สถานะ: `bounded_structural_slice`

slice นี้ตรึงขอบเขตของ tick/lifecycle ที่ Wave 3 จะตรวจต่อ ไม่ได้แปล
`MainProcess` หรือ `DoEvent` ทั้งฟังก์ชัน และยังไม่ตั้งชื่อ semantic state จาก
branch ที่ยังไม่ได้ trace

## Source boundary

| Function | Source status | Boundary |
|---|---|---|
| `form_GameForm__MainProcess` | recovered C | `form.c:1–15354`; มี direct `NextTarget` call ที่บรรทัด 7798 และมี branch จำนวนมากนอก scope actor |
| `form_GameForm__DoEvent` | assembly fallback only | ใช้ `wave1_branch_index.json`/assembly index เป็นโครงสร้างตั้งต้น ยังไม่มี recovered C semantic slice |
| `form_GameForm__ProcessEvent` | recovered C | `form.c:18536–19166`; ใช้เป็น event boundary เท่านั้นใน C0 |
| `form_GameForm__NextTarget` | recovered C | `form.c:27926–28005`; เป็น target-to-position field-flow boundary |

## C0 evidence ที่ยืนยันได้

- `MainProcess` เรียก `NextTarget` จริงอย่างน้อยหนึ่ง callsite ใน recovered C
- `NextTarget` อ่าน `TargetX/TargetY` และเขียนไปยัง arrays ที่ map ใน `dump.cs`
  เป็น `HumanX/HumanY` ตาม actor index ที่รับเข้า
- `DoEvent` มี method signature และ assembly fallback แต่ยังไม่มี C definition
  ให้ใช้เป็น semantic implementation source ใน W3-C0
- `ProcessEvent` อยู่ใน call graph แต่ C0 ยังไม่อ้างว่าเป็น actor state mutator

## Field groups ที่ต้อง traceใน actor tick

- position: `HumanX`, `HumanY`, `HumanPX`, `HumanPY`
- target: `TargetX`, `TargetY`, `HumanNowPoint`, `HumanGoalPoint`
- state/timer: `HumanMode`, `HumanTime`, `HumanStop`, `HumanWalkLong`,
  `HumanReaction`, `HumanWait`, `HumanState`, `HumanAnime`
- interaction boundary: `HumanSitChair`, `HumanMeetMode`, `HumanMeetSyain`,
  `HumanRequestMax`, `HumanBallTime`, `HumanBallMode`, `HumanBallIndex`,
  `HumanBallNumber`

Field declarations อยู่ใน `game-dev-story-mod_Dumped/dump.cs` ช่วงบรรทัด
276078–276120; C0 map จะเก็บ offset references ที่พบใน function spans แต่จะไม่
เปลี่ยนชื่อ field ให้เป็น semantic Agent state

## Stop conditions

- ไม่ขยาย `MainProcess` นอก branch ที่อ่าน/เขียน field กลุ่มด้านบน
- ไม่ขยาย `DoEvent` จนกว่าจะมี lifecycle dependency ที่ fixture ใช้จริง
- ไม่สรุป `HumanMode`, `HumanState` หรือ `HumanAnime` เป็น walking/working/sitting
- ไม่สร้าง path, collision หรือ seat semantics จากการเห็น field reference เพียงอย่างเดียว

## Next action

1. สร้าง W3-C2 state/timer slice จาก branch ที่มี actor field writes/read pairs
2. สร้าง W3-C3 target/movement slice จาก `AddTarget → NextTarget → HumanX/Y`
3. ใช้ Wave 2 movement interface เป็น adapter boundary ถ้าไม่พบ legacy producer
