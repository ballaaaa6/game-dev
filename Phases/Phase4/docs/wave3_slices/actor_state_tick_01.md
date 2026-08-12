# W3-C2 — Actor state/timer audit slice 01

สถานะ: `raw_state_audit_with_adapter_transitions`

slice นี้ลงทะเบียน `Human*` state/timer fields และ raw initial seed จาก
`CallSyain` แล้วสร้าง transition fixture แยก raw legacy namespace ออกจาก
web Agent state namespace ยังไม่ใช่การปิด semantic mapping ของ `HumanMode`,
`HumanState` หรือ `HumanAnime`

## Raw fields ที่ตรวจสอบ

`HumanMode`, `HumanTime`, `HumanStop`, `HumanWalkLong`, `HumanSitChair`,
`HumanReaction`, `HumanWait`, `HumanState`, `HumanAnime`, `HumanDegree`,
`HumanFukiIndex` และ `HumanFukiTime` ถูก map จาก `dump.cs` พร้อม offset และ
offset references ใน `wave3_actor_function_map.json`

`CallSyain` มี bounded initial writes ที่ตรวจสอบได้ เช่น `HumanStop=1`,
`HumanMode=0`, `HumanWalkLong=0`, `HumanTime=0`, `HumanAnime=0` และ
`HumanState=0` แต่ค่าเหล่านี้ยังไม่ถูกแปลเป็น Agent semantics

## Transition namespaces

| Namespace | ตัวอย่าง | สถานะ |
|---|---|---|
| raw legacy field | `HumanMode`, `HumanTime`, `HumanState` | evidence-only |
| raw mode ID | `0`, `8`, `9` | evidence-only/probable ตาม callsite |
| Agent state | `walking`, `idle`, `talking` | verified หรือ explicit web adapter decision เท่านั้น |
| animation ID | `mode_08`, `mode_09` | แยกจาก Agent state และ timing |

## Transition ที่ fixture อนุญาต

- `raw_spawn_seed`: verified bounded raw writes จาก `CallSyain`; `agent_state=null`
- `adapter_move_requested`: `walking` ในฐานะ `web_adapter_decision` เท่านั้น
- `adapter_move_arrived`: `idle` ในฐานะ `web_adapter_decision` เท่านั้น
- `dialogue_candidate_modes`: `talking` เป็น probable จาก Phase 2 candidate mode 8/9

## Stop rules

- ไม่เรียก `HumanMode=0` ว่า `idle`
- ไม่เรียก `HumanState=0` ว่า Agent state ใด
- ไม่เรียก `HumanAnime=0` ว่า animation เฉพาะตัว
- ไม่ถือ deterministic adapter clock ว่าเท่ากับ `HumanTime` timing เดิม
- ไม่ขยาย `DoEvent` เพราะ C0/C2 ยังมีเพียง assembly fallback boundary

Machine-readable outputs:

- `Phases/Phase4/artifacts/wave3_actor_state_contract.json`
- `Phases/Phase4/artifacts/wave3_state_transition_fixture.json`
