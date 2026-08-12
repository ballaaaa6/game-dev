# Wave 5 — Runtime architecture

อัปเดต: 2026-08-11

สถานะ: **C0–C8 implemented; complete_with_known_limitations**

## Runtime boundary

`Phases/Phase5/runtime/runtime.js` เป็น deterministic web adapter runtime ที่รับ room manifest,
explicit providers, locale records และ BodyFace records แล้วคืน state snapshot, event log และ
draw commands. Canvas renderer ใน `app.js` เป็น presentation adapter เท่านั้น.

Phase 6 ใช้ public bridge `setAgentTaskProjection` และ `recordAdapterEvent` เพื่อเพิ่ม product
task layer แบบแยก namespace; Wave 5 ยังคงเป็นเจ้าของ movement, seat, bubble, raw event และ draw
state และไม่รับรอง task status เป็น legacy semantic.

ลำดับ tick:

1. movement provider / collision provider
2. bubble expiry
3. notification expiry
4. named web event log
5. render snapshot

## Namespace policy

- `agent.state` เป็น web adapter state
- `movement.status` เป็นผลจาก explicit path/collision provider
- `TFace/TBody/TMode/TKage` เป็น draw selectors
- raw `Human*` fields ไม่ถูก promote เป็น semantic Agent state
- `legacy_equivalence` เป็น `false` ใน runtime snapshot และ event log

## Asset policy

Runtime โหลด `floor0.png`, body และ face จาก source-root URL ผ่าน local server. ไม่มีการย้ายหรือ
แก้ source asset. `floor0.seb` คงสถานะ `truncated_final_record` และไม่สังเคราะห์ข้อมูลส่วนท้าย.

`TFace=40/41` จะคง selector ไว้และ omit face layer เมื่อ asset resolve ไม่ได้. Unknown animation
ใช้ static verified frame policy; ไม่ใช้สูตรจาก viewer เดิมเป็น recovered legacy semantics.

## Lifecycle policy

Bubble และ notification ใช้ logical ticks และลบ record เมื่อ `expires_at_tick` ถึงค่า expiry.
Notification `graph_id` ยังเป็น raw ID และ event queue ใช้ named web events โดยไม่ตั้งชื่อจาก
`EventMode/EventTemp/EventTemp2`.
