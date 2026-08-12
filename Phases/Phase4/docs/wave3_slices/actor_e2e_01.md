# Wave 3 C6 — Single-actor end-to-end boundary

สถานะ: **deterministic contract/fixture พร้อม; legacy runtime equivalence ยังไม่ปิด**

## ขอบเขต

slice นี้รวม fixture ที่สร้างไว้ใน W3-C1 ถึง W3-C5 เข้ากับ Wave 2 minimum scene
boundary เป็น trace เดียว โดยไม่ port `MainProcess`/`DoEvent` ทั้งฟังก์ชัน และไม่อ้างว่า
adapter state หรือ movement เท่ากับ legacy semantics

Inputs ที่ใช้จริง:

- `wave2_minimum_scene_fixture.json` — room, coordinate และ draw-dispatch boundary
- `wave3_spawn_fixture.json` — bounded actor/employee spawn
- `wave3_state_transition_fixture.json` — raw seed และ explicit adapter state transitions
- `wave3_movement_fixture.json` — deterministic path/collision provider boundary
- `wave3_seat_fixture.json` — explicit occupy/release relation
- `wave3_draw_fixture.json` — verified body/face composition fixture

## Golden trace

`wave3_actor_trace.json` บันทึก `spawn_move_arrive_draw` ตามลำดับ:

1. spawn `adapter.actor.0` จาก `adapter.employee.0`
2. ใช้ adapter transition เป็น `walking`
3. เดินผ่าน `[1,0]`, `[2,0]`, `[3,0]`
4. เปลี่ยนเป็น adapter `idle` เมื่อถึง target
5. สร้าง explicit draw command จาก `TFace/TBody/TMode`

clock เป็น deterministic adapter clock 100 ms/frame และ position space เป็น
`adapter_world_position`; ไม่มีการอ้างว่าเป็น legacy pixel/world/isometric space

## Failure/edge scenarios

- `blocked_target` คงตำแหน่ง `[0,0]` และไม่ dispatch draw หลัง collision provider รายงาน blocked
- `seat_occupied` ให้ผล conflict โดยไม่เปลี่ยน owner
- `seat_release_then_sit` แสดง `occupy → release → occupy` เป็น adapter relation
- `animation_unknown_fallback` ใช้ static verified frame policy เท่านั้น; raw state ไม่เลือก
  `TMode` และไม่มีการ substitute asset ที่ unresolved

## ข้อจำกัด

- `HumanState`, `HumanMode`, `HumanAnime` ยังไม่ถูก promote เป็น semantic Agent state
- seat occupancy ยังไม่มี legacy producer ที่ยืนยันได้ และไม่ derive จาก `HumanSitChair`
- Wave 2 room object type, depth, collision และ walkable semantics ยังเป็น boundary/open
- `TFace=40/41` ยังคง unresolved ตาม C5 policy
