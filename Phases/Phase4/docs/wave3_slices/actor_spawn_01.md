# W3-C0 — Actor spawn evidence slice 01

สถานะ: `bounded_structural_slice`

ขอบเขตของ slice นี้คือการตรึงจุดเริ่มต้นสำหรับ W3-C1 จาก `AddSyain` และ
`CallSyain` เท่านั้น ยังไม่ใช่ actor state contract และยังไม่สรุปความหมายของ
ค่า `TMode`, `TSyurui`, point หรือ `HumanMode`

## Source boundary

| Source | Evidence |
|---|---|
| `game-dev-story-mod_Dumped/dump.cs` | `AddSyain(...)` signature ที่บรรทัด 276474 และ `CallSyain(int TMode, int TIndex, int TSyurui)` ที่บรรทัด 276480 |
| `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c` | `form_GameForm__AddSyain` บรรทัด 26951–27322 |
| `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c` | `form_GameForm__CallSyain` บรรทัด 27392–27925 |
| `Phases/Phase4/artifacts/office_runtime_call_graph.json` | `CallSyain → AddObjec` 2 ครั้ง และ `CallSyain → NextTarget` 1 ครั้ง |

## สิ่งที่ตรวจสอบได้จาก source

- `AddSyain` หา free slot จาก `SyainEnabled` และเก็บผลไว้ใน `SyainIndex`
  ก่อนเขียน employee-facing arrays หลายชุด
- `CallSyain` รับ `TMode`, `TIndex`, `TSyurui` และตั้ง `SyainIndex` จาก `TIndex`
  ก่อนเลือก actor slotจาก `HumanEnabled`
- `CallSyain` เรียก `AddObjec` เพื่อสร้าง object slot และเก็บ object reference
  ใน `HumanObjec` ของ actor slot
- `CallSyain` เขียน `HumanSyain`, `HumanSyurui`, `HumanEnabled`, `HumanFaceG`,
  `HumanBodyG` และ initial actor fields ใน branch ที่สร้าง actor สำเร็จ
- `CallSyain` เรียก `NextTarget` ใน branch เดียวกัน แต่ความหมายของ target/current
  point ยังต้องตรวจต่อใน W3-C3

## Field map ที่ W3-C0 ลงทะเบียน

| Group | Fields | สถานะ |
|---|---|---|
| identity/binding | `HumanEnabled`, `HumanObjec`, `HumanSyain`, `HumanSyurui`, `HumanVisitor` | field declaration + offset provenance; semantic role ยังไม่ปิด |
| composition | `HumanFaceG`, `HumanBodyG` | field declaration + offset provenance; selector namespace ยังใช้ Wave 2 adapter |
| state seed | `HumanMode`, `HumanTime`, `HumanStop`, `HumanWalkLong`, `HumanState`, `HumanAnime` | initial writes มี bounded evidence; state label/timer semantics ยังไม่ปิด |
| position/target | `HumanX`, `HumanY`, `HumanPX`, `HumanPY`, `HumanNowPoint`, `HumanGoalPoint`, `TargetX`, `TargetY` | ลงทะเบียนแล้ว; ต้องแยก point/pixel/world space ใน W3-C3 |

## สิ่งที่ยังไม่ claim

- ยังไม่ claim ว่า actor slot คือ employee แบบเดียวกับ Agent identity ในเว็บ
- ยังไม่ claim ว่า `HumanMode=0` คือ `idle`
- ยังไม่ claim ว่า `HumanX/Y` เป็น world coordinate หรือ screen coordinate
- ยังไม่ claim ว่า object ที่ `CallSyain` สร้างเป็น collision/seat anchor
- ยังไม่ claim ว่า `HumanFaceG/HumanBodyG` เป็น filename หรือ resource index โดยตรง

## Next action

1. ทำ W3-C1 bounded contract โดย map parameter-to-field ของ `AddSyain` และ
   `CallSyain` ให้ครบพร้อม failure branches
2. ทำ W3-C2 โดย trace initial `HumanMode/HumanState/HumanAnime/HumanTime`
3. ทำ W3-C3 โดยตรวจ `NextTarget` และ `AddTarget` ต่อกับ position/target spaces

หลักฐาน machine-readable อยู่ที่ `artifacts/wave3_actor_function_map.json` และ
`artifacts/wave3_gap_register.json`
