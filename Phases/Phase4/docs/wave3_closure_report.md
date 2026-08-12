# Wave 3 — Closure และ handoff report

อัปเดต: 2026-08-11

สถานะ: **`complete_with_known_limitations` สำหรับ contract/fixture handoff; legacy
state, movement, occupancy และ semantic animation ยังไม่เทียบเท่า runtime เดิม**

## คำตัดสินใจหลัก

Wave 3 ปิดได้ในระดับที่ Phase 4/Phase 5 ใช้เป็น contract boundary ต่อได้ เพราะ W3-C0
ถึง W3-C6 มี provenance, deterministic fixture, golden trace และ regression ครบ
แต่ไม่ใช่การ claim ว่า recovered legacy runtime ถูกแปลครบ

1. `HumanMode`, `HumanState`, `HumanAnime`, `HumanTime` และ raw relation fields คงเป็น
   evidence-only หรือ raw IDs ตาม artifact เดิม
2. `walking`, `idle` และ `sitting` ใน fixture เป็น explicit web-adapter state ไม่ใช่
   recovered legacy state
3. legacy seat occupancy producer ยังไม่พบใน bounded `MainProcess`, `CallHikkosi`,
   `CallSyain` และ `DrawObj` traces; ใช้ explicit `occupy/release/query` adapter ต่อไป
   โดยไม่ derive จาก `HumanSitChair`, chair arrays, sprite หรือ draw coordinate
4. Phase 2 `agent_state_mapping.json` ไม่ถูกแก้ เพราะ C5/C6 เพิ่ม selector/composition
   และ integration evidence แต่ยังไม่มี verified semantic animation, timing, loop หรือ
   direction ใหม่

## ผลลัพธ์ตาม work package

| Package | ผลตรวจ | สถานะส่งต่อ |
|---|---|---|
| W3-C0 | actor function/field provenance และ controlled gaps | evidence-backed |
| W3-C1 | bounded employee → actor spawn contract | contract/fixture |
| W3-C2 | raw state/timer fields, 4 bounded `MainProcess` tick slices และ explicit adapter transitions | raw evidence; semantic mapping open |
| W3-C3 | target/position flow และ deterministic path/collision adapter fixture | adapter-only movement |
| W3-C4 | chair/desk relation traces และ explicit seat ownership policy | adapter-only occupancy |
| W3-C5 | `DrawHuman` selector/composition contract, 42 BodyFace records และ unresolved TFace 40/41 | renderer contract; semantic animation open |
| W3-C6 | 6 single-actor scenarios และ golden `spawn → move → arrive → draw` trace | e2e adapter boundary |

## Classification สำหรับงานถัดไป

### Evidence-backed / translated boundary

- field declarations, offsets และ bounded source spansจาก W3-C0
- bounded spawn writes จาก `CallSyain` และ employee binding จาก W3-C1
- `TargetX/Y` → actor position array raw flowจาก W3-C3
- `DrawHuman` signature และ `imgBody[TBody]` + `imgFace[TFace]` + `BodyFace[TMode]`
  composition จาก W3-C5
- deterministic trace และ failure behavior ที่ระบุใน W3-C6

### Contract-only / adapter decision

- stable `actor_id` และ employee/object referencesที่เปิดเผยให้ runtime
- adapter `walking`, `idle`, `sitting` และ deterministic clock
- path, collision, walkable และ seat providers
- explicit seat ownership และ static verified draw frame policyเมื่อ semantic animation
  ยังไม่รู้

### Unresolved / controlled gaps

- W3-GAP-001: semantic role ของ raw actor fields
- W3-GAP-003: current/previous position และ coordinate-space equivalence
- W3-GAP-004: full `MainProcess`/`DoEvent` lifecycle semantics
- W3-GAP-005: state → mode, timing, loop, direction และ mirroring
- W3-GAP-006: legacy seat occupancy producer
- W3-GAP-007: legacy collision/walkable producer
- `TFace=40/41`: asset/index namespace ยังไม่ resolve

ทุกข้อมี status และ next action ใน `wave3_gap_register.json`; ห้ามเปลี่ยนเป็น success
หรือ verified โดยอาศัย fixture behavior เพียงอย่างเดียว

## Handoff ไป Phase 5 / Wave 4

Phase 5 สามารถใช้ `wave2_minimum_scene_fixture.json`, W3 spawn/state/movement/seat/draw
contracts และ `wave3_actor_trace.json` เพื่อสร้าง runtime adapter ได้ โดยต้อง:

- แยก raw legacy fields, adapter state และ renderer selectors เป็นคนละ namespace
- คง `legacy_equivalence=false` ใน trace ที่ใช้ adapter provider
- ไม่ hardcode static selector หรือแทน `TFace=40/41` ด้วย asset อื่น
- ไม่ derive occupancy, collision หรือ walkable จาก sprite/coordinate เพียงอย่างเดียว

Wave 4 รับต่อได้ที่ dialogue/talk-bubble/lifecycle boundary โดย mode 8/9 เป็นเพียง
probable talking candidate และยังต้องคง timing/face-change behavior เป็น unknown

## Verification

```text
python Phases/Phase4/tools/build_wave3_actor_contract.py --check
python Phases/Phase4/tools/build_wave3_identity_contract.py --check
python Phases/Phase4/tools/build_wave3_state_contract.py --check
python Phases/Phase4/tools/build_wave3_movement_contract.py --check
python Phases/Phase4/tools/build_wave3_interaction_contract.py --check
python Phases/Phase4/tools/build_wave3_animation_contract.py --check
python Phases/Phase4/tools/build_wave3_e2e_contract.py --check
python Phases/Phase4/tools/build_wave3_closure.py --check
python -m unittest discover -s Phases/Phase4/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase2/tests -p "test_*.py"
```

ผลตรวจล่าสุด: Phase 4 `88/88`, Phase 2 `5/5`; source roots เดิมยัง read-only และ
`git diff --check` ผ่าน
