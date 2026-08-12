# Phase 4 — Selective code translation และ logic classification

สถานะ: Wave 4 W4-C0–C7 และ W4.5 evidence hardening ปิดรอบแบบ `complete_with_known_limitations` — Wave 3 handoff
พร้อมใช้, สร้าง locale/talk/bubble/event/notification/actor-dialogue boundaries และ
bounded consumer/hardening slices แล้ว; timer unit, cleanup, token/actor binding, graph labels
และ DoEvent branch semantics ยังเปิดอย่างมีขอบเขต

งานเร่งด่วนถัดไปของ workspace คือ **Corpus Intelligence Pipeline (P0-A)** ตาม
`Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md`. งานนี้จะรวม evidence เดิม,
สร้าง full-corpus index, lossless views, cross-tool comparison, candidate logic maps และ validator
ก่อนเปิดงานเก็บ Phase อื่นต่อ โดยไม่แก้ source roots และไม่เขียนทับ historical artifacts

หลัง P0-A closure gate จึงเริ่ม **Office Runtime TypeScript Port (P0-B)** ตาม
`Docs/superpowers/plans/2026-08-12-office-typescript-port.md`. งาน P0-B จะเปลี่ยนเฉพาะ
resource/scene, actor/movement/seat/draw, dialogue/bubble/notification และ event bridge
ให้เป็น executable TypeScript; JSON/Markdown ยังคงเป็น evidence/generated data/fixture
และ runtime JavaScript เดิมจะไม่ถูกแทนที่จนกว่า parity และ browser gate จะผ่าน

แผน foundation เดิมอยู่ที่ `docs/selective_code_translation_plan.md`; สำหรับลำดับการลงมือปัจจุบัน
ให้ยึด P0-A corpus closure และ P0-B TypeScript handoff ด้านบนก่อน แล้วจึงกลับมาเก็บ dependency
ข้าม Phase 1/2/3 ตาม evidence ที่ query ได้

หลักการคือแปลเฉพาะ office runtime แบบ dependency-closed และสร้างทั้ง field/function map,
neutral pseudocode, runtime contracts, fixtures และ confidence evidence ไม่แปล gameplay หรือ C
ทั้งเกม

Wave 0 สร้างผลลัพธ์ไว้ที่ `artifacts/` ได้แก่ field offsets, function/source status,
office call graph, string-literal references, assembly fallback targets และ translation coverage
พร้อม smoke tests ใน `tests/test_wave0_index.py` ผลตรวจล่าสุดผ่าน 6/6 tests

Wave 1 สร้างผลลัพธ์เพิ่มใน `artifacts/` ได้แก่ `resource_selector_map.json`,
`wave1_branch_index.json` และ `wave1_build_manifest.json` จาก source/asset roots แบบ read-only
พร้อม builder ที่รันซ้ำได้ใน `tools/build_wave1_resource_map.py`, แผนละเอียดใน
`docs/wave1_plan.md`, contract ใน `docs/resource_loading.md` และ smoke tests ใน
`tests/test_wave1_resource_map.py`

Wave 2 สร้างผลลัพธ์เพิ่มใน `artifacts/` ได้แก่ `wave2_selector_adapter.json`,
`scene_contract.json`, `wave2_room_contract.json`, `wave2_coordinate_contract.json`,
`wave2_coordinate_fixture.json`, `wave2_draw_order_contract.json`,
`wave2_draw_order_fixture.json`, `wave2_furniture_contract.json`,
`wave2_placement_fixture.json`, `wave2_minimum_scene_fixture.json`,
`wave2_wave3_movement_interface.json`, `wave2_gap_register.json` และ
`wave2_build_manifest.json` จาก source/asset roots แบบ read-only โดยใช้ builder
`tools/build_wave2_scene_contract.py` และ tests ใน `tests/test_wave2_scene_contract.py`

minimum Wave 2 gate พร้อมสำหรับ Wave 3 ในระดับ contract/interface แล้ว แต่
สิ่งที่ยังเปิดอยู่คือ numeric selector values, `TFace=40/41` namespace, full room placement,
world/object/crop/screen transform, depth semantics และ seat/collision/walkable contract
ซึ่งต้อง trace ต่อด้วย bounded slices และห้ามปิดด้วยการคาดเดา ส่วน coordinate/draw fixtures
ที่สร้างแล้วเป็น regression probes ที่แยก semantic uncertainty ไว้ชัดเจน

แผน execution ของ Wave 3 อยู่ที่ `docs/wave3_plan.md` โดยแบ่งเป็น actor baseline,
identity/spawn, state/timer, target/movement, seat/interaction, animation/draw,
single-actor end-to-end fixture และ closure/handoff ตามลำดับ dependency ปัจจุบัน
W3-C0 ถึง W3-C7 มีผลลัพธ์ในระดับ evidence/contract/fixture และ closure/handoff แล้ว ได้แก่ actor provenance,
identity/spawn, raw state/tick slices, target/position flow, furniture/seat boundary และ
animation/draw selector/composition contract รวมถึง single-actor end-to-end fixture/golden
trace พร้อม deterministic fixtures ใน `artifacts/`
และ bounded slices ใน `docs/wave3_slices/`; state/timer semantic mapping,
current/previous position, legacy seat occupancy, collision, walkable และ semantic animation
ยังไม่ปิด; `docs/wave3_closure_report.md` ระบุ controlled gaps และ handoff rules ใช้
`wave2_wave3_movement_interface.json` ได้เฉพาะในฐานะ contract/stub boundary และต้องติดป้าย
web adapter เมื่อยังไม่มี legacy producer evidence

## Wave 4 — Dialogue, text, bubble และ lifecycle bridge

แผน execution อยู่ที่ `docs/wave4_plan.md`, contract builder อยู่ที่
`tools/build_wave4_dialogue_contract.py` และ closure builder อยู่ที่
`tools/build_wave4_closure.py`. W4-C0–C7 สร้าง artifact แบบ deterministic
จาก language CSV, `dump.cs`, categorized C, `DoEvent` assembly และ Wave 3 fixtures
โดยคง source roots แบบ read-only.

ผลลัพธ์หลัก:

- `wave4_locale_contract.json` และ `wave4_locale_fixture.json` — CSV 12 locale,
  placeholder, fallback และ encoding contract
- `wave4_talk_contract.json` และ `wave4_talk_fixture.json` — talk index, text,
  speaker และ `KaiwaLine` boundary
- `wave4_bubble_contract.json` และ `wave4_bubble_fixture.json` — Fuki/HumanFuki
  storage, draw และ adapter clock boundary
- `wave4_event_contract.json` และ `wave4_event_fixture.json` — `AddEvent` producer
  inventory 53 callsites และ structural `DoEvent` consumer boundary
- `wave4_notification_contract.json` และ `wave4_notification_fixture.json` —
  bounded `AddMessage` writes โดย raw lifetime `0x60`/graph semantics ยังเปิด
- `wave4_actor_dialogue_fixture.json` — deterministic actor dialogue-to-bubble trace
- `wave4_lifecycle_slices.json` — bounded MainProcess/DrawObj/DoEvent consumer slices
- `wave4_c7_build_manifest.json` และ `docs/wave4_closure_report.md` — closure/handoff
- `wave4_*_trace.json` และ `wave4_hardening_manifest.json` — W4.5 timer/talk/graph/event traces
- `docs/wave4_hardening_report.md` และ `docs/wave4_slices/*_02.md` — hardening findings

ผลตรวจล่าสุด: Wave 4 contract `8/8` + closure `5/5` + hardening `6/6`, Phase 4 รวม `107/107`, Phase 2 `5/5`.
ห้าม promote
`talking`, raw speaker IDs, numeric event modes, bubble timer หรือ message lifetime
เป็น legacy semantic จาก fixture เพียงอย่างเดียว.
