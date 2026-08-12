# Wave 3 — Actor truth

อัปเดต: 2026-08-11

สถานะ: **W3-C0–C7 handoff เสร็จแบบมี known limitations; C2 semantic mapping,
legacy occupancy, C5 semantic animation และ Wave 2/Phase 5 runtime semantics ยังเปิด**

Wave 3 มีเป้าหมายสร้าง actor state, employee binding, target/movement,
seat/interaction boundary และ animation/render contract ที่ตรวจสอบย้อนกลับไปยัง
source ได้พอสำหรับ actor หนึ่งตัวใน office scene เดียวกัน โดยใช้
`Phases/Phase4/artifacts/wave2_wave3_movement_interface.json` เป็น input boundary

Wave 3 เริ่มได้ที่ระดับ contract/state/stub แม้ Wave 2 ยังไม่ปิด full room placement,
depth, seat, collision และ walkable semantics แต่ทุกส่วนที่รับมาจาก adapter ต้องติดป้าย
`web_adapter_decision` หรือ `non_legacy` ชัดเจน ห้ามยกระดับให้เป็น recovered legacy behavior

## 1. ขอบเขต

### อยู่ใน Wave 3

- actor identity และการผูกกับ employee record
- actor position, previous position, target point และ movement tick
- state/mode/timer contract ที่เกี่ยวกับการแสดง actor
- การผูก `TFace`, `TBody`, `TMode` กับ `DrawHuman`
- ความสัมพันธ์ actor–object–seat ในระดับที่มีหลักฐาน หรือประกาศเป็น adapter contract
- deterministic trace ตั้งแต่ spawn → target → move → state/animation → draw
- การอัปเดต Phase 2 agent-state mapping ด้วยสถานะ `verified`, `probable`,
  `conflicting_evidence`, `recoverable`, `web_adapter_decision` หรือ `out_of_scope`

### ไม่อยู่ใน Wave 3

- การ port `MainProcess` หรือ `DoEvent` ทั้งฟังก์ชัน
- dialogue text, bubble/language lookup แบบครบ pipeline (Wave 4)
- business simulation, hiring/progression, task queue และ AI model
- การอนุมาน collision จากขนาดภาพหรือ alpha bounds
- การอนุมาน seat occupancy จากภาพเก้าอี้หรือการมี `ChairMainObjec`
- การ claim ว่า path/grid/animation ที่สร้างในเว็บเท่ากับ semantics เดิม

## 2. หลักฐานตั้งต้นที่ต้องถือเป็น source-of-truth

จาก `game-dev-story-mod_Dumped/dump.cs` มี field groups ที่ Wave 3 ต้อง map ให้ครบ:

- actor identity/binding: `HumanEnabled`, `HumanObjec`, `HumanSyain`,
  `HumanSyurui`, `HumanVisitor`
- actor position: `HumanX`, `HumanY`, `HumanPX`, `HumanPY`
- target/point: `HumanNowPoint`, `HumanGoalPoint`, `TargetX`, `TargetY`
- state/timing: `HumanMode`, `HumanTime`, `HumanStop`, `HumanWalkLong`,
  `HumanSitChair`, `HumanReaction`, `HumanWait`, `HumanState`, `HumanAnime`
- composition: `HumanFaceG`, `HumanBodyG`, `HumanDegree`, `HumanFukiIndex`,
  `HumanFukiTime`
- furniture relation: `DeskSyain`, `DeskObjec`, `ChairMainObjec`,
  `ChairSubObjec`, `PCObjec`, `DeskZahyou`

เส้นทาง function ที่ต้องใช้เป็น evidence boundary คือ `AddSyain`, `CallSyain`,
`NextTarget`, `MainProcess`, `ProcessEvent`, `DoEvent`, `DrawObj` และ `DrawHuman`.
จากหลักฐานปัจจุบัน `NextTarget` มีการคัดลอก `TargetX/TargetY` ไปยังตำแหน่ง actor
ตาม index ที่รับเข้า แต่ความหมายของ point, pixel และ world space ยังต้องแยกยืนยัน
ไม่ให้ปะปนกัน

Phase 2 ให้ composition contract ที่ยืนยันแล้วว่า `DrawHuman` ประกอบจาก
`imgBody[TBody] + imgFace[TFace]` และมี BodyFace record 42 รายการ แต่ semantic
animation ที่ verified ยังเป็น 0; ดังนั้น frame grouping ยังไม่ใช่ state mapping

## 3. Work packages

### W3-C0 — Baseline และ actor evidence register

**เป้าหมาย:** ตรึง input และกำหนดรายการ function/field ที่ Wave 3 จะรับผิดชอบ
ก่อนตีความ semantics

งาน:

- freeze source/artifact hashes จาก Wave 2 และยืนยัน source roots แบบ read-only
- สร้าง actor function map จาก function inventory/call graph พร้อม raw/export address
- ทำ field-to-function provenance สำหรับ field groups ด้านบน
- แยกสถานะของแต่ละ field เป็น `verified`, `recoverable`, `conflicting_evidence`,
  `not_found_in_scoped_functions`, `web_adapter_decision` หรือ `out_of_scope`
- ระบุ bounded slices ของ `CallSyain`, `NextTarget`, `MainProcess` และ `DoEvent`
  เฉพาะ branch ที่แตะ actor state/position/timer

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_build_manifest.json`
- `artifacts/wave3_gap_register.json`
- `artifacts/wave3_actor_function_map.json`
- `docs/wave3_slices/actor_spawn_01.md`
- `docs/wave3_slices/actor_tick_01.md`

**Gate:** ไม่มี field สำคัญที่ถูกทิ้งเป็น `unknown` โดยไม่ระบุเหตุผลและ next action;
baseline hash และ Wave 0–2 regression ต้องยังตรงเดิม

### W3-C1 — Actor identity และ spawn contract

**เป้าหมาย:** สร้าง actor หนึ่งตัวจาก employee data โดย trace ได้ว่าแต่ละค่าถูกเขียน
ลง actor record ที่ใด

งาน:

- trace `AddSyain` ว่า employee record ใดเป็น source ของ name/type/face/body/speed
  และแยกค่าที่เป็น business stat ออกจากค่าที่ renderer/movement ต้องใช้
- trace `CallSyain` ตั้งแต่ slot allocation ถึงการเขียน `HumanSyain`, `HumanObjec`,
  `HumanSyurui`, enabled, face/body, initial mode/state/time และ initial point
- map actor ↔ office object แบบ ID/reference ไม่ใช้ array index เป็น public identity
- กำหนด invalid/disabled/slot-full behavior ตามหลักฐานหรือระบุเป็น adapter policy

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_actor_identity_contract.json`
- `artifacts/wave3_spawn_fixture.json`
- neutral pseudocode ของ bounded `CallSyain` path พร้อม source citations

**Acceptance:** spawn fixture สร้าง actor ได้อย่างน้อย 1 ตัว, มี stable `actor_id`,
employee reference, face/body selectors และ position/target fields ครบ หรือ field ที่
ยัง resolve ไม่ได้ถูกเก็บเป็น unresolved พร้อมเหตุผล

### W3-C2 — State, mode และ timer contract

**เป้าหมาย:** แยก legacy fields ที่สังเกตได้ออกจาก semantic Agent state ที่ยังไม่ยืนยัน

งาน:

- trace writes/reads ของ `HumanMode`, `HumanState`, `HumanAnime`, `HumanTime`,
  `HumanStop`, `HumanWalkLong`, `HumanReaction`, `HumanWait` ใน bounded branches
- สร้าง transition table โดยทุก transition ต้องมี trigger, guard, mutation,
  timer behavior และ exit/next state
- update mapping ของ `idle`, `walking`, `working`, `sitting`, `break`, `talking`
  เป็น `verified`/`probable`/`unknown`/`web_adapter_decision` แยกจาก raw mode ID
- คง `talking` candidate mode 8/9 เป็น probable จนกว่าจะมีหลักฐานเรื่อง loop/timing
- ไม่ตั้งชื่อ mode จากลำดับภาพหรือ mechanical group ใน `animation_manifest.json`

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_actor_state_contract.json`
- `artifacts/wave3_state_transition_fixture.json`
- `docs/wave3_slices/actor_state_tick_01.md`
- update `Phases/Phase2/artifacts/agent_state_mapping.json` และรายงาน Phase 2

**Acceptance:** ทุก state ที่จะนำไปใช้ใน fixture มี transition หรือมีคำประกาศว่าเป็น
web-native adapter state; timer ที่ยังหาไม่พบต้องเป็น `null/unknown` ไม่ใช่ค่าที่เติมเอง

### W3-C3 — Target และ movement contract

**เป้าหมาย:** ทำให้ actor เดินจากจุดเริ่มไป target ได้ด้วย interface ที่ตรวจสอบได้ โดย
แยก source evidence ออกจาก path provider ที่เว็บเลือกใช้

งาน:

- trace `TargetX/TargetY`, `HumanNowPoint`, `HumanGoalPoint`, `HumanX/Y`, `HumanPX/PY`
  และ `NextTarget` เพื่อแยก target point, current position และ previous position
- trace movement/tick branch จาก `MainProcess`/`DoEvent` เฉพาะช่วงที่มีผลต่อ actor
- กำหนด position space, integer rounding, arrival tolerance และ tick ordering
  ให้เป็น contract ที่ test ได้; ถ้ายังไม่มีหลักฐานให้ระบุเป็น adapter decision
- ใช้ Wave 2 provider boundary สำหรับ `path`, `collision` และ `seat occupancy`
- รองรับผลลัพธ์ `path`, `no_path`, `blocked`, `clear`, `unavailable`, `arrived`,
  `cancelled` โดยไม่กลบความแตกต่างระหว่าง legacy evidence กับ web behavior

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_movement_contract.json`
- `artifacts/wave3_movement_fixture.json`
- `artifacts/wave3_movement_trace.json`
- neutral pseudocode ของ actor tick และ movement adapter

**Acceptance:** actor fixture เดินได้หนึ่งเส้นทางจาก start → target, trace ทุก tick
reproducible, blocked/no-path case ไม่ทำให้ actor ถูก teleport และ position space
ถูกระบุครบ

### W3-C4 — Furniture, seat และ interaction boundary

**เป้าหมาย:** ทำให้การนั่ง/ลุก/ผูก desk เป็น explicit relation โดยไม่เดา producer

งาน:

- trace producer/consumer ของ `HumanSitChair`, `DeskSyain`, `DeskObjec`,
  `ChairMainObjec`, `ChairSubObjec`, `PCObjec`, `DeskZahyou`
- ตรวจว่า field ใดเป็น relation, object reference, point data หรือ state flag
- ใช้ interface จาก Wave 2 เป็น authoritative boundary เมื่อ legacy producer ยังไม่พบ:
  `occupy(agent_id, seat_id)`, `release(agent_id, seat_id)`,
  `can_enter(object_id, position)` และ `walk(from, to, context)`
- กำหนด conflict policy สำหรับ seat เดียวกัน, actor ถูก disable, path ถูกยกเลิก
  และการลุกก่อนถึงเป้าหมาย

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_interaction_contract.json`
- `artifacts/wave3_seat_fixture.json`
- gap update ใน `wave2_gap_register.json` หรือ register Wave 3 โดยอ้างเหตุผลใหม่

**Acceptance:** seat occupancy เป็น state ที่ query/release ได้, ไม่ derive จาก sprite,
และ fixture มีทั้ง success, occupied และ unavailable case

### W3-C5 — Animation selector และ actor draw contract

**เป้าหมาย:** เชื่อม actor state/tick กับคำสั่งวาดที่ใช้ composition contract เดิม

งาน:

- trace `HumanFaceG`, `HumanBodyG`, `HumanAnime`, `HumanState`, `HumanDegree`
  ไปยัง callsite `DrawHuman`
- ใช้ `BodyFace[TMode]` crop/offset ที่ verified แล้วเป็น renderer input
- แยก `mode_id`, `animation_id`, semantic state และ direction เป็นคนละ namespace
- resolve timing/loop/direction/mirroring ต่อเมื่อมี assembly/runtime evidence;
  หากไม่มี ให้ใช้ static frame หรือ web-native timing ที่ติดป้ายชัดเจน
- ตรวจ selector adapter ต่อกับ unresolved static selectors และ `TFace=40/41`
  โดยไม่ hardcode ค่าใหม่

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_actor_animation_contract.json`
- `artifacts/wave3_draw_fixture.json`
- update `Phases/Phase2/artifacts/animation_manifest.json` เฉพาะรายการที่มี evidence ใหม่

**Acceptance:** จาก actor state ที่ระบุได้ สร้าง draw command ที่ deterministic มี
`TFace/TBody/TMode`, crop, offset และ destination ครบ; semantic label ที่ยังไม่ปิด
ต้องไม่ถูกเขียนทับเป็น verified

**ผลตรวจ W3-C5:** สร้าง contract และ fixture แล้ว โดยยืนยัน `DrawHuman` signature,
`TMode → BodyFace`, `TBody → imgBody` และ `TFace → imgFace` ใน bounded renderer
branches; มี actor selector flow จาก `DrawObj` และ HumanDex preview ที่แยก namespace
จาก semantic Agent state. `TFace=40/41` ถูกเก็บเป็น unresolved โดยไม่ substitute asset,
และ timing/loop/direction/mirroring ยังคง unknown ตามหลักฐานปัจจุบัน

### W3-C6 — Single-actor end-to-end fixture

**เป้าหมาย:** รวม contract ทั้งหมดเป็น trace เดียวก่อนเริ่ม Phase 5 runtime

ลำดับ fixture:

1. load `wave2_minimum_scene_fixture.json`
2. spawn actor จาก `wave3_spawn_fixture.json`
3. bind employee/object และตั้ง start/target point
4. inject explicit walk/collision/seat providers
5. tick state + movement ตาม deterministic clock
6. resolve animation selector และสร้าง draw command
7. sort/dispatch actor ผ่าน Wave 2 scene boundary

ต้องมี scenario อย่างน้อย:

- `spawn_idle_draw`
- `walk_to_target_arrive`
- `blocked_target`
- `seat_occupied`
- `seat_release_then_sit`
- `animation_unknown_fallback`

ผลลัพธ์ที่คาดหวัง:

- `artifacts/wave3_actor_e2e_fixture.json`
- `artifacts/wave3_actor_trace.json`
- `tests/test_wave3_actor_contract.py`
- `tools/build_wave3_actor_contract.py` ถ้าต้อง regenerate fixture จาก source

**Acceptance:** scenario หลัก `spawn → move → arrive → draw` ผ่านแบบ deterministic;
failure scenarios ให้ผลตาม contract และไม่ถูกแปลงเป็น success เงียบ ๆ

**ผลตรวจ W3-C6:** สร้าง single-actor fixture 6 scenarios และ golden trace 7 events
แล้ว ครอบคลุม `spawn_idle_draw`, `walk_to_target_arrive`, `blocked_target`,
`seat_occupied`, `seat_release_then_sit` และ `animation_unknown_fallback`; trace หลัก
ผ่านตำแหน่ง `[1,0] → [2,0] → [3,0]` และ draw command พร้อม โดยยังคง
`legacy_equivalence=false` และแยก raw/adapter/renderer namespaces

### W3-C7 — Closure และ handoff

**เป้าหมาย:** ปิด Wave 3 ในระดับที่ Phase 4/Phase 5 ใช้ต่อได้ โดยรายงานข้อจำกัดครบ

งาน:

- สร้าง `docs/wave3_closure_report.md`
- อัปเดต `wave3_gap_register.json`, Phase 2 mapping, roadmap และ `PROJECT_STATE.md`
- สรุป field/function ที่เป็น translated contract, contract-only, adapter decision,
  out-of-scope และ unresolved พร้อมผลกระทบต่อ Phase 5
- ระบุเส้นทางที่ Wave 4 ต้องรับต่อ เช่น dialogue/talk bubble และ lifecycle event

**Wave 3 gate:**

- actor หนึ่งตัว spawn ได้จาก contract ที่มี provenance
- actor เดินถึง target หรือรายงาน blocked/no-path ตาม provider contract
- state/timer ที่ใช้จริงมี transition evidence หรือประกาศเป็น web-native อย่างชัดเจน
- `DrawHuman` command มี selector/crop/offset/destination ครบ
- มี golden trace อย่างน้อยหนึ่งเส้นทาง `spawn → move → arrive → draw`
- test regression ของ Wave 0–3 ผ่าน และ source roots ไม่ถูกแก้
- ไม่มี unresolved dependency ที่ถูกปล่อยไว้โดยไม่มี status, owner หรือ next action

**ผลตรวจ W3-C7:** สร้าง closure report และ machine-readable occupancy decision แล้ว;
W3-GAP-001 ถึง W3-GAP-007 ถูกคงเป็น controlled open gaps พร้อม next action, W3-GAP-008
คงเป็น out-of-scope. Phase 2 mapping ไม่ถูกแก้เพราะไม่มี semantic evidence ใหม่ และ
seat occupancy ถูกตัดสินเป็น adapter-only สำหรับขอบเขต Wave 3 ปัจจุบัน

## 4. ลำดับการทำงานและ dependency

ลำดับบังคับคือ:

```text
W3-C0 baseline
  ├─> W3-C1 identity/spawn
  ├─> W3-C2 state/timer
  └─> W3-C3 target/movement
          └─> W3-C4 seat/interaction
W3-C1 + W3-C2 ──> W3-C5 animation/draw
W3-C3 + W3-C4 + W3-C5 ──> W3-C6 end-to-end fixture
W3-C6 ──> W3-C7 closure/handoff
```

ทำ W3-C1 และ W3-C2 ขนานกันได้หลัง C0; W3-C3 เริ่มได้โดยใช้ adapter-only
movement interface แต่ห้ามรอหรืออ้างว่า Wave 2 ปิด walkable/collision แล้ว
W3-C5 ต้องใช้ composition evidence จาก Phase 2 และ selector adapter จาก Wave 2
ก่อนสร้าง fixture

## 5. Definition of Ready / Definition of Done

### ก่อนเริ่มแต่ละ unit

- มี input artifact และ source path ที่ตรวจสอบได้
- ระบุ function span/field span และ address namespace แล้ว
- ระบุสิ่งที่ unit จะไม่ตีความไว้ก่อน
- มี expected status เมื่อหลักฐานไม่พอ
- มี fixture/test boundary ที่ตรวจสอบผลลัพธ์ได้

### เมื่อถือว่า unit เสร็จ

- มี artifact ที่ regenerate หรือ audit ได้
- มี source citation ทุก claim ที่เป็น legacy evidence
- ทุก unknown มีสาเหตุและ next action
- มี regression test หรือ deterministic fixture
- source roots เดิมยัง hash ตรง baseline
- ไม่มี web adapter decision ถูกเขียนในชื่อหรือคำอธิบายให้ดูเหมือน legacy fact

## 6. Stop rules และความเสี่ยง

- ไม่ hardcode numeric static selector (`DDBody`, `DDPC`, `DDChair`, `DDDesk`) หรือ
  map `TFace=40/41` จากชื่อ/ภาพอย่างเดียว
- ไม่เรียก `HumanMode` ว่า walking/working/sitting จนกว่าจะมี branch/timer/consumer evidence
- ไม่ derive collision, seat, walkable, pivot หรือ depth จาก preview/alpha bounds
- ไม่ขยาย `MainProcess`/`DoEvent` ทั้งฟังก์ชัน; ขยายเฉพาะเมื่อ dependency ของ fixture พิสูจน์ได้
- ถ้า trace หา legacy producer ไม่พบ ให้ปิด unit ด้วย `not_found_in_scoped_functions`
  และ `web_adapter_decision` แทนการเติม semantics
- ถ้า animation timing ยังไม่พบ ให้ใช้ deterministic adapter clock ใน fixture และคง
  `frame_timing_ms`, `loop_mode`, `direction` เป็น `unknown`

ความเสี่ยงหลักคือ actor field จำนวนมากอยู่ใน global arrays และมีทั้ง employee,
visitor, dialogue และ gameplay lifecycle ปะปนกัน จึงต้องรักษา dependency closure
แบบ bounded ต่อไป ไม่ยกทั้ง `GameForm` state มาเป็น web runtime model

## 7. ลำดับลงมือรอบแรก

1. ทำ W3-C0 และ freeze manifest จาก `wave2_build_manifest.json`
2. สกัด `CallSyain`/`NextTarget` slices พร้อม field map ที่อ่านจาก `dump.cs`
3. สร้าง spawn fixture ที่ยังไม่ผูก semantic state เกินหลักฐาน
4. trace actor tick จาก `MainProcess` เฉพาะ branch ที่แตะ `Human*`
5. เติม movement adapter fixture ให้ actor เดินได้หนึ่งเส้นทาง
6. ค่อยเชื่อม Phase 2 composition และสร้าง draw fixture
7. รวม end-to-end fixture แล้วตัดสินใจจากผลทดสอบว่าจะปิดหรือเปิด gap ใดต่อ

เอกสารนี้เป็นแผน execution; W3-C0 ถึง W3-C4 เริ่ม implementation ในระดับ deterministic
evidence/contract builder แล้ว แต่ยังไม่มี actor state/movement/seat runtime หรือ web port ที่อ้าง
legacy equivalence ต้องทำ W3-C2 semantic mapping ต่อ และหา legacy occupancy producer ก่อน draw/end-to-end
