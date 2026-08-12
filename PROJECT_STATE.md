# Project State

ตรวจสอบล่าสุด: 2026-08-12
ขอบเขต: `D:\antigravity\test open ai`

## สถานะปัจจุบัน

- Workspace นี้ถูก initialize เป็น Git repository แล้ว โดยใช้ branch `main`
- ตั้ง remote `origin` เป็น `https://github.com/ballaaaa6/game-dev.git` และ push initial commit สำเร็จแล้ว
- Commit ล่าสุดที่ push ก่อนการบันทึกสถานะนี้: `90c96e9` (`Keep toolkit and viewer out of repository`)
- การอัปโหลดตัด `APK_Toolkit/`, `viewer/`, APK/ZIP, extraction raw, `game-dev-story-mod_Dumped/`, Ghidra installation/database และ export C ขนาดใหญ่ตาม `.gitignore`; โฟลเดอร์ที่ตัดออกยังอยู่ในเครื่องและไม่ถูกลบ
- เป็น workspace สำหรับวิเคราะห์และต่อยอด office runtime จาก extraction เดิม โดยแยกผลลัพธ์ไว้ใน `Phases/`
- ไม่มีงานที่กำลังรันใน repository

## สิ่งที่ทำเสร็จแล้ว

- Phase 0: baseline เสร็จแบบ `complete_with_known_limitations`; source ที่ตรวจพบคือ Sprites 445 ไฟล์, Dumped 208 ไฟล์ และ Extracted 1,226 ไฟล์
- Phase 1: inventory, legacy map, SEB structure, renderer evidence และ preview ถูกสร้างแล้ว; validation เป็น `pass_with_warnings` โดย catalog มี 405 ไฟล์, SEB 53 รายการ และ office manifest 168 รายการ
- Artifacts และรายงานหลักอยู่ใต้ `Phases/Phase0/` และ `Phases/Phase1/` ตาม README และรายงานที่มีอยู่จริง
- Phase 2: เสร็จแบบ `complete_with_known_limitations`; audit ยืนยัน bodyface 42 records, body 26 ไฟล์, face 36 ไฟล์; สร้าง manifests, code trace, previews, state mapping และ validation (`pass`). Follow-up trace ยืนยันกลไกประกอบภาพ `imgBody[TBody] + imgFace[TFace]` โดยใช้ `BodyFace[TMode]` crop/offset และเพิ่มแผนศึกษาต่อไว้ใน `Phases/Phase2/docs/phase2_investigation_plan.md`
- Phase 4 Wave 0: สร้าง translation index จาก `dump.cs`, `script.json`, categorized C, assembly fallback และ `stringliteral.json` แล้ว; shortlist 88 functions, selected 12 classes/1,850 fields, call graph 277 nodes/359 edges และ coverage matrix ครบ
- Wave 0 validation: `Phases/Phase4/tests/test_wave0_index.py` ผ่าน 6/6 tests; builder rerun สำเร็จและ source roots เดิมยังไม่ถูกแก้
- P0-A0: สร้าง read-only corpus baseline builder, test suite, manifest และ report แล้ว; source roots 1,879 ไฟล์ / 2,561,371,923 bytes ตามราย root และ Phase 0/4/5/6 artifact inputs 112 ไฟล์; fingerprint ปัจจุบันคือ `ce92294f66da1d85a1cc476c7a01fb01a07a0956d418683afdd85658e0b7bceb`

## สิ่งที่กำลังทำ

- Wave 3 W3-C0–C7 handoff เสร็จแบบ `complete_with_known_limitations`; actor, movement, seat, draw และ e2e adapter boundaries พร้อมใช้ต่อ โดย semantic state/timer, legacy occupancy/collision/walkable และ semantic animation ยังเปิด
- Wave 4 W4-C0–C7 และ W4.5 evidence hardening เสร็จแบบ `complete_with_known_limitations`: เพิ่ม timer/bubble, talk/speaker, message graph/audio และ DoEvent target-cluster traces พร้อม handoff
- Wave 4 validation ล่าสุด: contract tests `8/8`, closure tests `5/5`, hardening tests `6/6`, Phase 4 regression เดิม `107/107`; เมื่อรวม audit/semantic-trace tests ล่าสุดเป็น `123/123`, Phase 2 regression `5/5`; source roots เดิมยัง read-only
- Wave 4 ที่ยังเปิดแบบมีขอบเขต: timer ยังเป็น logical-tick candidate, HumanFukiIndex cleanup ไม่พบใน scoped expiry path, literal/token semantics และ actor binding ยัง adapter-boundary, graph/audio labels และ numeric event modes ยังไม่ตั้งชื่อ
- Wave 5 Phase 5 C0–C8, W5.1-B–G, W5.2, W5.3, W5.4, W5.5, W5.6, W5.7, W5.8 และ W5.9 ปิดรอบแบบ `complete_with_known_limitations`: runtime host, bounded furniture asset renderer, image-slot mapping, numeric selector decode, exact bihin selector/metadata/filename alignment, `IndexImgFloorParts`/floor-main selector joins, SEB structural decode, consumer crop/local placement, bounded PNG room screen placement, `AddObjec`/`MainProcess`/furniture producer provenance, loader bridge, mixed draw order, logical timer policy, explicit adapter animation profiles, raw numeric-event bridge, movement/collision/seat providers, draw commands, locale/talk/bubble, named events, notification cleanup และ visual artifact พร้อม
- Wave 5 validation ล่าสุด: Node runtime `10` scenarios ผ่าน, Python contract/visual `17` tests ผ่าน, Phase 4 regression `107/107`, Phase 2 regression `5/5`, locale artifact 12 ภาษา/union IDs 2,420, browser smoke ของ furniture + actors ผ่าน และ source roots เดิมยัง read-only
- Wave 6 W6-C0–C7 และ W6.1 ปิดรอบแบบ `complete_with_known_limitations`: deterministic task engine, priority queue, explicit assignment, lifecycle, durable task notification/activity log, Agent projection, repository boundary, migration, optimistic conflict handling, explicit local permission policy, import/export, dashboard interaction, focus highlight และ closure artifacts พร้อม
- Wave 6 final hardening validation ล่าสุด: task system `18/18` scenarios, Phase 6 contract `11/11`, Wave 5 runtime `10/10`, Phase 5 contract `17/17`, Phase 4 `107/107`, Phase 2 `5/5`, fresh browser smoke console error/warning `0`; source roots เดิมยัง read-only
- งานเร่งด่วนที่ยืนยันใหม่: **P0-A Corpus Intelligence Pipeline** — รวม Phase 4–6 evidence, สร้าง full-corpus index, lossless views, cross-tool comparison, candidate logic maps, validator และ negative-evidence ledger ก่อนเปิดงานเก็บ Phase อื่นต่อ
- งาน downstream ถัดจาก P0-A: **P0-B Phase 4 Office Runtime TypeScript Port** — port เฉพาะ resource/scene, actor/movement/seat/draw, dialogue/bubble/notification และ event bridge ให้เป็น executable TypeScript ก่อนเริ่ม Phase 7; Phase 5/6 JavaScript runtime ยังคงเป็น compatibility baseline ระหว่าง migration
- Design และ implementation plan ของงาน downstream อยู่ที่ `Docs/superpowers/specs/2026-08-12-office-typescript-port-design.md` และ `Docs/superpowers/plans/2026-08-12-office-typescript-port.md`; ยังไม่มี TypeScript implementation ที่เริ่มสร้างแล้ว
- Design และ implementation plan ของ P0-A อยู่ที่ `Docs/superpowers/specs/2026-08-12-corpus-intelligence-pipeline-design.md` และ `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md`; P0-A0 เป็นงานแรกที่ implement แล้ว
- รายละเอียด execution plan ของ `P0-A0` อยู่ที่ `Docs/superpowers/plans/2026-08-12-p0-a0-corpus-baseline.md`; baseline builder, focused tests, manifest และ report ผ่าน A0 gate แล้ว และงานถัดไปคือ P0-A1
- P0-A execution order ถูกกำหนดเป็น `A0 → A1 → A2`; จากนั้น `A3/A5` ทำ parallel ได้, `A6` เป็น pilot barrier, `A7/A8` ทำได้บางส่วนแบบ parallel และ `A9` เป็น final closure barrier
- แผน P0 ผ่าน self-review แล้ว: แยก baseline guard, `tsc` Node output, esbuild browser bundle, resource/scene, actor/movement/seat, dialogue/event, browser integration และ coverage closure เป็น 9 tasks; runtime JS เดิมจะไม่ถูกแทนที่จนกว่า parity/browser gate จะผ่าน
- P0-B ถูกจัดเป็น downstream ของ P0-A; จะเริ่ม port หลัง corpus closure report ผ่าน แต่ยังคงใช้ Phase 4 artifacts เดิมเป็น evidence ตั้งต้นโดยไม่สร้างซ้ำ
- Phase 4 cross-wave gap audit ล่าสุด: สร้าง reconciliation ที่ supersede สถานะเก่าซึ่งมีหลักฐาน Wave5 ปิดแบบ bounded แล้ว 7 กลุ่ม และจัดกลุ่ม open recoverable 9 กลุ่ม, not-found scoped 3 กลุ่ม, product boundary 3 กลุ่ม
- Phase 4 targeted source scan ล่าสุด: `DrawHuman` มี 106 symbol references/36 parseable calls, literal `TFace=40` 9 จุดและ `TFace=41` 1 จุด; พบ current face family เพียง `face_0..35`; scoped C/assembly ไม่พบ literal `floor0.seb`
- Phase 4 semantic gap trace ล่าสุด: `NewGamePara` มี bounded `AddObjec` setup 29 calls พร้อม `w0` write-back ครบทุก call; `DoEvent` แยก `KikakuMode` values 5/7/8 ที่เชื่อม LT/Replace/AddKaiwa และ `EventMode` comparison 2 ได้ โดยยังไม่ตั้งชื่อ mode
- Phase 4 TFace producer trace ล่าสุด: literal `TFace=40/41` ทั้ง 10 จุดอยู่ใน direct DrawHuman callsites ของ preview/screen/panel; scoped actor field producers ไม่พบ literal 40/41 และยังไม่มี alternate asset/index namespace ที่ยืนยันได้

## ปัญหาและ known limitations

- Phase 0: extraction report ยังชี้ output ไปที่ `game-dev-story-mod_Sprites_fixed` ขณะที่ source ปัจจุบันคือ `game-dev-story-mod_Sprites`
- Phase 0: report เดิมมี warning UTF-8 3 รายการ แม้ CSV ปัจจุบันผ่าน BOM/strict UTF-8; C export ที่รวม recovery แล้วยังขาด C 4 ฟังก์ชัน แต่ assembly fallback ของ failed-function list ครบ 5/5
- Phase 1: SEB ทั้ง 53 รายการมี final-record tail shortfall 4 ไบต์; ยังสรุปไม่ได้ว่าเป็น variant หรือ extraction boundary
- Phase 1: พบ INF missing-extension references 6 รายการ, office floor ที่ไม่มี SEB คู่ชื่อเดียวกัน 4 รายการ และ office PNG ที่ไม่มี direct bonus reference 2 รายการ
- Phase 1: anchor/baseline/pivot, coordinate placement, collision/seat/walkable/zone และ grid/depth contract ยังเป็น `unknown` หรือยังไม่ยืนยันจากหลักฐาน
- เอกสารสถานะไม่ตรงกันทั้งหมด: `Phases/README.md` ระบุ Phase 1 inventory เสร็จแล้ว ขณะที่ `Docs/AI_Agent_Office_Roadmap.md` ยังระบุว่ากำลังดำเนินการอยู่; สำหรับการทำงานต่อ ให้ถือว่า inventory artifacts มีแล้ว แต่ runtime semantics ที่ยังไม่ยืนยันเป็นงานคงค้าง
- มี `TODO.md` เป็น backlog แบบ actionable ที่ workspace root; ยังไม่มี `DECISIONS.md`
- P0-A0: ไฟล์ artifact ที่ไม่ใช่ JSON หรือไม่มี metadata ใช้ `schema=null` และ `status=unknown` ตามหลักฐานจริง; `Cpp2IL`/`Cpp2IL.exe` ไม่พร้อมใช้งานใน environment นี้ แต่เป็น optional tools; baseline ไม่ตีความ semantic ของ source
- Phase 2: literal `DrawHuman` selectors `TFace=40` และ `TFace=41` ไม่มี extracted face asset; ตรวจพบ DrawHuman callsites 106 จุด โดย 92 จุดมี selector แบบ variable-driven; มีการ resolve HumanDex dynamic path แล้วหนึ่งเส้นทาง แต่ DrawObj/Syain/Kaiwa และ resource-index-to-filename mapping ยัง trace ไม่ครบ
- Phase 2: semantic animation ที่ verified = 0; Agent mapping เป็น probable 1 (`talking`, candidate mode 8/9) และ unknown 5; timing, loop, direction, mirroring, pivot และ exact body/face pair ยังไม่ยืนยัน
- Phase 4 Wave 0: categorized C ที่มีอยู่ยังไม่เท่ากับแปลเสร็จ; ต้อง resolve named fields, branch behavior, fixtures และ confidence ต่อ unit
- Phase 4 Wave 0: `NewGamePara` และ `DoEvent` ยังมีเพียง assembly fallback (13,671 และ 15,569 instructions); semantic-gap trace ปิดได้เฉพาะ bounded branch/call clusters แต่ full lifecycle grouping และ numeric mode naming ยังไม่ปิด
- Phase 4 Wave 0: call graph มี unresolved/external nodes 5 รายการ และยังไม่ใช่ semantic dependency closure ที่ปิดแล้ว
- Phase 4 Wave 0: `StringLiteral_12647` เป็น terminal pointer นอกช่วงตาราง zero-based; artifact เก็บไว้ใน `terminal_sentinel_ids` ไม่ถือเป็น missing literal
- Phase 4 Wave 1: W1 historical artifacts อ่าน `StringLiteral_N` เป็น zero-based JSON index จึงเคยรายงาน `7514=false` และ `833=.png.bytes`; W5.5 แก้ด้วย one-based label rule เป็น `7514=face_`, `833=.png` และเป็น source of truth ล่าสุดสำหรับ IMG_LIST alignment
- Phase 4 Wave 1: ค่า static base selectors มี numeric decode ใน Phase5 W5.3 (`DDBody=0`, `DDChair=25`, `DDDesk=26`, `DDPC=77`) และ W5.5 ปิด exact bihin filename/metadata join; W5.6 ปิด observed `IndexImgFloorParts`/floor-main selector joins, W5.7 ปิด SEB consumer crop/local base flow และ W5.8 ปิด bounded PNG room screen caller flow แต่ full world/SEB room mapping ยังไม่ปิด
- Phase 4 Wave 1: W1-C1 ยืนยัน write provenance ของ selectors จาก raw ELF แล้ว; W5.3/W5.5 แปลง packed cctor stores และ native literal labels เป็น mapping โดยไม่ยกระดับเป็น universal room/transform semantics
- Phase 4 Wave 1: W5.5 ยืนยัน imgFace prefix `StringLiteral_7514=face_` และ suffix `StringLiteral_833=.png`; `TFace=40/41` asset/index-space gap ยังเปิดคนละประเด็น
- Phase 4 Wave 1: W1-C3 asset audit ยืนยัน manifest records 291/291 มีไฟล์จริง; unmatched IMG_LIST เหลือ 2 face-like extraction gaps และ utility/text tokens; bounded caller trace ของ `TFace=40/41` พบแต่ direct literal preview/screen/panel callsites จึงยังเป็น index-space mismatch
- Phase 4 Wave 1: `NewGamePara` และ `DoEvent` มี bounded evidence slices แล้ว แต่ branch semantics/lifecycle grouping ของทั้งฟังก์ชันยังไม่ถูกกู้ครบ และ helper `0x00cb0cc0` ยังไม่มีชื่อที่ยืนยันได้
- Phase 4 Wave 1: assembly export/recovered-C address ใช้ namespace ที่สูงกว่า raw `script.json`/ELF `0x100000`; artifact เก็บทั้ง export และ raw addresses แล้ว
- Phase 4 Wave 2: static selectors 5 ตัวมี symbolic contract ใน Phase4; W5.3 เพิ่ม numeric evidence สำหรับ 4 base selectors และคง adapter ห้าม hardcode จนกว่า namespace join จะปิด
- Phase 4 Wave 2: room asset fixture ใช้ `office/floor0.png` + `office/floor0.seb` ซึ่ง SEB ยังมี tail shortfall 4 bytes; W5.3 เพิ่ม bounded `CallHikkosi` placement, W5.7 ปิด local SEB crop/base offset, W5.8 ปิด bounded GameForm PNG screen path และ W5.9 ปิด object-producer field provenance แต่ยังไม่ใช่ full SEB room reconstruction
- Phase 4 Wave 2: coordinate fixture, W5.7 SEB consumer, W5.8 caller trace และ W5.9 producer trace ยืนยัน centered Graphics origin, local `base + trans` arithmetic, `ObjecX/Y + ObjecZX/ZY` PNG placement, `AddObjec` parameter map, `MainProcess` XY averaging และ furniture update field sets; source-array semantics, producer-side transform/isometric/pivot/anchor enum/depth semantics ยังไม่ปิด
- Phase 4 Wave 2: draw-order fixture เป็น neutral compare probe ของ `ObjecSY + ObjecY`; ยังไม่ยืนยันว่าเป็น depth/z semantics
- Phase 4 Wave 2: furniture relation/placement trace ยืนยัน accessor normalization; W5.3 ปิด numeric `AddObjec` field map และ bounded `CallHikkosi` branches แต่ยังไม่มี full room placement หรือ seat occupancy/collision/walkable contract
- Phase 4 Wave 2: minimum scene fixture พร้อมใช้เป็น contract/stub boundary สำหรับ Wave 3 แต่ bounded room object type ยัง symbolic และ reception dispatch ใน fixture เป็น probe ไม่ใช่ claim ว่า CallHikkosi สร้าง reception
- Phase 4 cross-wave reconciliation: historical Wave1/2 registers ยังเก็บสถานะเดิมตามหลักฐาน ณ ตอนนั้น; ให้ใช้ `cross_wave_gap_reconciliation.json` เป็น current view และอย่าเปิดงาน selector/placement ที่ Wave5 ปิดแบบ bounded แล้วซ้ำ
- Phase 4 targeted scan/semantic trace: `TFace=40/41` มี literal source hits จริง 10 จุด (40=9, 41=1) แต่ยังไม่มี asset/alternate namespace ที่ยืนยันได้; actor selector paths เป็น dynamic field/array flow; `floor0.seb` ยังไม่มี literal/direct room caller ใน scoped C/assembly; ผลนี้เก็บเป็น evidence ไม่ใช่ semantic closure
- Phase 4 Wave 3 W3-C0: actor field map เป็น declaration/offset provenance เท่านั้น; semantic state, timer, position space, seat, collision และ walkable ยังไม่ปิด; `DoEvent` ยังเป็น assembly fallback only
- Phase 4 Wave 3 W3-C1: employee/actor/object references เป็น bounded source flow และ stable IDs เป็น web adapter policy; ไม่ใช่ public legacy identity
- Phase 4 Wave 3 W3-C2: raw state fields/initial seeds ถูก audit แล้ว แต่ MainProcess/DoEvent transition, timer และ numeric mode semantics ยังไม่ปิด; mode 8/9 เป็น probable Phase 2 candidate เท่านั้น
- Phase 4 Wave 3 W3-C3: `TargetX/Y` → `HumanX/Y`/`HumanPX/PY` raw writes verified; current/previous role, walkable/collision producer และ legacy movement timing ยังเปิด; adapter fixture ติดป้าย non-equivalent
- Phase 4 Wave 3 W3-C2 ต่อ: bounded `MainProcess` slices ยืนยัน `HumanWait` decrement, raw reset, raw mode/state branch และ `HumanAnime` threshold 15; timer unit, `bVar14` provenance และ Agent semantics ยังเปิด
- Phase 4 Wave 3 W3-C4: `HumanSitChair`/chair relation และ `DeskSyain` scan/clear/assignment มี bounded evidence; `occupy/release/query` เป็น explicit web adapter contract เท่านั้น ยังไม่พบ legacy occupancy producer
- Phase 4 Wave 3 W3-C5: `DrawHuman` signature และ bounded composition (`TMode → BodyFace`, `TBody → imgBody`, `TFace → imgFace`) verified; มี 42 record-only modes, `TFace=40/41` ยังไม่มี extracted face asset จึงเก็บ unresolved โดยไม่ fallback; verified semantic animations = 0, talking mode 8/9 เป็น probable candidate และ timing/loop/direction/mirroring ยัง unknown
- Phase 4 Wave 3 W3-C6: single-actor e2e fixture มี 6 scenarios และ golden trace 7 events; spawn → move → arrive → draw ผ่านใน adapter boundary, blocked ไม่ teleport, seat conflict/release แยกชัด และ unknown animation ใช้ static verified frame policy โดยไม่ substitute asset; legacy equivalence ยัง false
- Phase 4 Wave 3 W3-C7: closure report และ `wave3_legacy_occupancy_decision.json` ยืนยัน handoff พร้อมใช้ใน Phase 5 แบบมี known limitations; occupancy เป็น adapter-only สำหรับ scope ปัจจุบัน, C2/Phase2 mapping ไม่ถูก promote และ W3-GAP-001–007 ยังมี controlled status/next action
- Phase 4 Wave 4: locale contract ยืนยัน CSV ปัจจุบัน 12 ภาษา, duplicate ID `0`, BOM/strict UTF-8 ผ่าน; English CSV ไม่มีใน extraction และ fallback เป็น web adapter decision
- Phase 4 Wave 4: `GetTalkIndex`/`GetTalkTexts`/`AddKaiwaTalkData`/`GetHumanTalkName`/`AddKaiwa` ยืนยัน bounded raw pipeline; literal pointer/token meanings ต้อง validate กับ raw records และไม่พบ direct producer caller ที่ผูก raw speaker กับ Wave 3 actor ใน scoped C/assembly
- Phase 4 Wave 4: `MainProcess` ลด `HumanFukiTime`, `DrawObj` gate การวาดด้วยค่าที่เป็นบวกก่อนอ่าน `HumanFukiIndex`, และ `__update` เรียก MainProcess ด้วย candidate counts `1/2/16`; timer unit กับ zero-time cleanup ยังไม่ปิด
- Phase 4 Wave 4: `AddEvent` producer contract เดิมนับ same-line calls 53 จุด; bounded source scan พบ symbol callsites 55 จุดเพราะ 2 จุดเป็น multiline; raw mode expressions ยังไม่ตั้งชื่อ
- Phase 4 Wave 4: `DoEvent` ยังคง assembly-only (15,569 instructions) แต่ W4.5 เพิ่ม target clusters/nearby constants ของ `AddKaiwa`/`AddMessage`/`EventGChange`/`Print`; exact mode-to-branch mapping และ full branch semantics ยัง unknown
- Phase 4 Wave 4: `AddMessage` bounded contract และ `MainProcess` consumer ยืนยัน raw lifetime `0x60`, decrement, expiry compaction; `form_GameForm___draw` ยืนยัน render behavior ของ MessageGraph `1/2` ผ่าน `imgMain`, แต่ graph labels/audio meaning ยัง unknown
- Phase 5: furniture ใน runtime เป็น bounded asset renderer สำหรับ reception/desk/chair จาก source-root PNG จริง; W5.2 ปิด image-slot expression, W5.3 ปิด numeric selectors/3×14 image-data records/bounded crop formulas/bounded `CallHikkosi` placement, W5.4 trace loader bridge, W5.5 ปิด exact bihin join (`25→29 chair`, `26→30 desk`, `77→117 pc`), W5.6 ปิด observed floor-parts/floor-main selector joins พร้อม SEB structural decode, W5.7 ปิด SEB consumer crop/local base placement, W5.8 ปิด bounded GameForm PNG room screen caller flow และ W5.9 ปิด `AddObjec`/`MainProcess`/furniture producer provenance; source-array semantics, producer-side world/SEB mapping, placement/pivot/depth/transform semantics และ legacy equivalence ยังไม่ปิด; semantic animation ที่ verified ยังเป็น 0 แม้มี explicit adapter profiles แล้ว
- Phase 5: `stringliteral.json` มี 12,647 entries ขณะที่ APK `global-metadata.dat` มี 12,661 entries และพบ first observed value mismatch ที่ literal ID 2395; ห้ามเลือก source ใดแทนกันโดยอัตโนมัติก่อน align runtime metadata
- Phase 5: local browser runtime ต้อง serve จาก workspace root เพื่อโหลด source-root assets; producer-side universal coordinate/depth transform, SEB room caller mapping, anchor/pivot semantics, timer unit, speaker binding, `TFace=40/41` และ numeric event modes ยังคงไม่ปิด
- Phase 6: task state เป็น product web adapter ใหม่ ไม่ใช่ legacy gameplay state; `TaskSystem` เรียก `TaskRepository` ผ่าน envelope/revision และ migrate snapshot เดิมได้ แต่ implementation ปัจจุบันยังเป็น localStorage เท่านั้น, permission เป็น explicit local policy ที่ยังไม่มี auth/backend/multi-user, auto-assignment/AI อยู่ Phase 7 และ focus เป็น highlight ไม่ใช่ recovered camera transform
- TypeScript port: เครื่องมือปัจจุบันยังไม่มี root/package/tsconfig หรือ compiler ที่ติดตั้งไว้; ต้องสร้าง isolated `Phases/Phase5` toolchain ก่อน port และไม่ควร mark unit ว่า `ts_ported` จาก JSON/pseudocode เพียงอย่างเดียว
- TypeScript port: 40,974 บรรทัดเป็น recovered-C audit boundary และ 29,240 assembly instructions เป็น fallback evidence; ทั้งสองตัวเลขไม่ใช่จำนวนโค้ดที่ต้องคัดลอกทั้งหมด เพราะ `MainProcess`/`DoEvent` มี gameplay และ semantic unknown ปนอยู่

## การตัดสินใจสำคัญ

- คง source roots เดิม (`game-dev-story-mod_Sprites/`, `game-dev-story-mod_Dumped/`, `game-dev-story-mod_Extracted/` และ Ghidra project) ไว้ และอ่านแบบ read-only ระหว่างการวิเคราะห์
- วาง generated output ใหม่ไว้ใต้ `Phases/` ไม่สร้าง generated JSON/PNG/report ปะปนที่ workspace root
- ใช้แนวทาง evidence-first: สิ่งที่ยังไม่มีหลักฐานให้คงเป็น `unknown` และไม่เติมความหมายจากการคาดเดา
- ใช้ `DrawHuman` signature จาก `dump.cs` เป็นหลักฐาน selector contract: `TFace`, `TBody`, `TMode`; ไม่ใช้ชื่อภาพหรือรูปลักษณ์เพียงอย่างเดียวเพื่อตั้ง semantic state
- กลไกประกอบภาพที่ยืนยันได้จาก code คือ `imgBody[TBody]` และ `imgFace[TFace]` ใช้ fields ของ `BodyFace[TMode]`; ถือเป็น rendering contract แยกจาก semantic state mapping
- ยืนยันการตัดสินใจ: ยก Phase 4 ขึ้นมาทำเป็น **Office Runtime TypeScript Port** งานหลัก P0 โดยแปลตาม dependency closure, ใช้ JSON เป็น evidence/generated data และไม่แปล gameplay/C ทั้งเกม
- อัปเดตลำดับงาน: ยก **Corpus Intelligence Pipeline เป็น P0-A urgent gate** ก่อน P0-B TypeScript และการเก็บ Phase อื่นต่อ; full-corpus metadata จะเก็บกว้าง ส่วน semantic translation จะ promote แบบมี source/fixture gate
- ยืนยันการเริ่ม Wave 0 แล้ว: สร้าง index/coverage ก่อน translation และคง source roots เดิมแบบ read-only
- ยืนยันการเริ่ม Wave 1: สร้าง generated resource/branch artifacts ใต้ `Phases/Phase4/` และคง source roots เดิมแบบ read-only
- ใช้ lowest-unused resource index สำหรับ unindexed `img.inf`/`seb.inf` entries ตาม recovered `ResourceManager__LoadStart`; ไม่อนุมาน index จากเลขท้าย filename
- ก่อนเข้า Wave 2 จะใช้ controlled statuses (`verified`, `recoverable`, `conflicting_evidence`, `extraction_missing`, `out_of_scope`) แทนการปล่อย unknown ที่ไม่บอกสาเหตุ
- W1-C0 พบและยืนยัน address delta `assembly export - 0x100000 = raw ELF/script address`; ใช้ delta นี้ทุกครั้งที่เชื่อม assembly กับ binary/metadata
- เริ่ม Wave 2 ด้วย symbolic selector adapter; numeric selector values จะ decode เฉพาะเมื่อมี dependency runtime ที่ต้องใช้จริง
- ใช้ `AddObjec` field mapping และ object-type constants เป็น scene contract; field semantics ที่ยังไม่ยืนยันต้องคงเป็น neutral
- ใช้ room asset fixture เป็นหลักฐาน asset/SEB เท่านั้น ไม่ใช้ preview หรือ alpha bounds เพื่ออนุมาน placement, pivot, seat หรือ collision
- ใช้ coordinate และ draw-order fixtures เป็น regression probes เท่านั้นจนกว่าจะมี assembly/runtime/pixel evidence ปิด semantic labels
- ใช้ furniture/placement trace เพื่อบันทึก producer/consumer relations; ไม่ถือว่า chair arrays หรือ furniture image assets เป็น seat occupancy/collision หลักฐาน
- อนุญาตให้ Wave 3 เริ่มจาก `wave2_wave3_movement_interface.json` ในระดับ contract/stub; ห้ามยกระดับ adapter input ให้เป็น recovered legacy movement semantics
- W3-C0 ใช้ actor function/field provenance เป็นหลักฐานตั้งต้น; field offset reference ไม่ถูกยกระดับเป็น Agent semantic state และ bounded slices ต้องแยก recovered C ออกจาก assembly fallback
- W3-C1–C3 ใช้ deterministic contract/fixture เป็น artifact boundary; adapter-owned identity, state และ movement ต้องแยก namespace/status จาก raw legacy evidence และห้าม promote เป็น legacy equivalence
- W3-C4 ใช้ seat ownership เป็น explicit adapter state; ห้าม derive occupancy จาก `HumanSitChair`, chair/object array presence, sprite หรือ draw coordinate และห้ามผูก raw relation clear เข้ากับ adapter release โดยอัตโนมัติ
- W3-C5 แยก legacy draw selectors (`TFace/TBody/TMode/TKage`), actor raw fields และ semantic Agent state เป็นคนละ namespace; `TFace=40/41` ต้องคง raw selector และ unresolved status โดยไม่ substitute asset หรือ promote mode เป็น semantic animation
- W3-C6 ใช้ existing C1–C5 fixtures และ Wave 2 minimum scene เป็น composition boundary เท่านั้น; golden trace เป็น deterministic web-adapter probe ไม่ใช่หลักฐานว่า state/movement/seat/draw semantics เท่ากับ legacy runtime
- W3-C7 ปิด Wave 3 ได้ในระดับ contract handoff เท่านั้น; legacy occupancy ตัดสินเป็น adapter-only ในขอบเขตปัจจุบัน, Phase 2 mapping คงเดิมเมื่อไม่มี evidence ใหม่ และทุก open gap ต้องมี status/owner/next action ก่อนส่งต่อ
- W4-C0–C6 ใช้ `build_wave4_dialogue_contract.py`; W4-C7 ใช้ `build_wave4_closure.py` แยกเป็น deterministic closure builder และแยก locale, talk, bubble, event, notification และ actor dialogue namespaces
- W4-C1 ใช้ `th` เป็น configured default locale ใน web adapter เท่านั้น; ไม่มีการอ้างว่าเป็น legacy fallback หรือแทน English extraction
- W4-C2 คง talk tag, talk index, language ID, raw speaker ID และ actor ID เป็นคนละ namespace; special speaker IDs `-5/-4/-3/-2` ยังไม่ตั้งชื่อ semantic
- W4-C3/C6/W4.5 trace consumer decrement/compaction และ logical tick candidate ได้แล้ว แต่คง timer raw values (`HumanFukiTime`, `0x60`) เป็น evidence-only; Wave 5 adapter ต้องมี explicit expired-state cleanup
- W4-C4 ไม่ตั้งชื่อ numeric event modes จาก producer callsites; `DoEvent` จะ trace เฉพาะ bounded dialogue/message/actor branches
- W4-C7 ปิดรอบด้วย bounded source slices และ Phase 5 handoff เท่านั้น; `legacy_equivalence=false` และ open gaps ต้องคง status/next action ต่อไป
- W4.5 เพิ่ม evidence hardening แบบ bounded; render/target behavior ที่ยืนยันได้ไม่ถูกยกระดับเป็น product labels, actor identity หรือ legacy event names
- Wave 5 แยก runtime host ไว้ใต้ `Phases/Phase5/runtime/`; generated contracts/reports อยู่ใต้ `Phases/Phase5/artifacts/` และ source asset ยังถูกอ้างผ่าน read-only source-root URL
- Wave 5 ใช้ logical tick, explicit path/collision/seat providers, named web events และ raw graph IDs; ไม่แปลง raw `0x60` เป็น milliseconds และไม่ตั้งชื่อ numeric event modes
- Wave 5 ใช้ static verified frame สำหรับ unknown animation และ omit face layer เมื่อ `TFace` resolve ไม่ได้; ไม่มี substitution สำหรับ `TFace=40/41`
- Wave 6 แยก durable task notification/activity log ออกจาก Wave 5 raw-graph notification; task lifecycle ใช้ logical tick, `done` เป็น terminal และ Agent projection ผ่าน public runtime adapter เท่านั้น
- Wave 6.1 ใช้ `TaskRepository` interface, envelope `wave6-task-repository-v1`, migration จาก direct state revision `0`, optimistic conflict status `conflict_needs_reload`, local permission policy และ schema-stable import/export; default implementation ยังใช้ localStorage key `phase6.task_state.v1` พร้อม memory-only fallback
- Phase 6 final hardening คง task state เป็น product adapter และเพิ่ม strict snapshot validation, repository envelope validation, memory-preserving failed reload, explicit localStorage failure status, lifecycle UI guards, task description และ notification dismiss โดยไม่เปลี่ยน legacy boundary
- W5.1-B ใช้ source-family PNG จริงเป็น bounded furniture asset fixture; ไม่อ้างว่า source index 0 หรือ manifest destination คือ legacy selector/crop/placement ที่กู้คืนแล้ว
- W5.1-C ใช้ mixed draw order แบบ adapter: furniture `sort_key`, actor `position[1]`, tie-break `kind_then_id`; depth label ของ legacy `ObjecSY + ObjecY` ยังเปิด
- W5.1-D ใช้ `expires_at_tick <= clock.value` เป็น timer policy ของ adapter และเก็บ legacy timer unit เป็น `unknown`
- W5.1-E ใช้ animation profile sequences ที่ explicit และ deterministic; profile status เป็น adapter-defined ไม่ใช่ legacy semantic recovery
- W5.1-F จัด `TFace=40/41` เป็น `index_space_gap`; raw selector ถูก preserve และ face layer ถูก omit
- W5.1-G เก็บ numeric event mode/args/source tag แบบ raw opaque ใน event log; named adapter events ยังเป็น canonical
- W5.2 ยืนยัน `.png.bytes` suffix และแยก `imgBihin_` chair/desk จาก `imgFloorParts` reception; resource indices 10/55/121 เป็น office manifest indices เท่านั้น ไม่ promote เป็น legacy selector values
- W5.3 ใช้ `wave5_3_numeric_crop_placement_contract.json` เป็นหลักฐาน numeric/crop/placement; `IndexImgFloorParts` เป็น `-1` initial sentinel และ runtime-selected ผ่าน `EventGChange(param_3)`; ห้าม promote raw `game/img.inf` candidates เป็น `IMG_LIST` selectors
- W5.4 ยืนยัน `AppData.GetImage` เป็น name-to-resource-array bridge; W5.5 ยืนยัน `StringLiteral_N` one-based/JSON zero-based correction และใช้ exact string-value join กับ active APK metadata ก่อนปิด bihin selectors; W5.6 ใช้ W5.5 IMG_LIST rows เพื่อ resolve `DDFloor+3`; W5.7 ใช้ `dump.cs` SP constants และ C consumers เพื่อปิด SEB local crop/base flow; W5.8 ปิด PNG room caller boundary; W5.9 ปิด `AddObjec`/`MainProcess`/furniture producer provenance แต่คง SEB room/world semantics เป็น bounded/open

## ไฟล์ที่ถูกสร้างใน handoff นี้

- `AGENTS.md` — กฎ Cross-Session Handoff และ workspace conventions
- `PROJECT_STATE.md` — สถานะปัจจุบันจากการตรวจสอบไฟล์จริงและรายงานปัจจุบัน
- `.gitignore` — รายการ raw/generated data ที่ไม่อัปโหลดไป GitHub
- `Phases/Phase2/tools/build_phase2_catalog.py` และ `Phases/Phase2/tests/test_phase2_catalog.py`
- `Phases/Phase2/artifacts/` — audit, analysis, catalogs, manifests, trace, state mapping, validation และ previews
- `Phases/Phase2/docs/phase2_report.md` และการปรับปรุง `Phases/Phase2/README.md`
- `Phases/Phase2/docs/phase2_investigation_plan.md` — แผน trace กลไกประกอบภาพ, resource index และ animation semantics ต่อ
- `Phases/Phase4/docs/selective_code_translation_plan.md` — proposal กำหนดขอบเขต direct/indirect/conditional/out-of-scope, work waves, artifacts และ closure gates ก่อนเริ่มแปล
- `Docs/superpowers/specs/2026-08-12-corpus-intelligence-pipeline-design.md` — design ของ P0-A full-corpus index, lossless views, cross-tool comparison, candidate translation และ promotion gates
- `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md` — implementation plan ของ P0-A ตั้งแต่ baseline/pilot ถึง closure/handoff
- `Docs/superpowers/plans/2026-08-12-p0-a0-corpus-baseline.md` — detailed execution plan ของ P0-A0 baseline manifest, hash freeze และ drift gate
- `Phases/Phase4/tools/build_corpus_manifest.py` และ `Phases/Phase4/tests/test_corpus_manifest.py` — P0-A0 read-only scanner, namespace-safe fingerprint, manifest/report writer, `--check` gate และ TDD coverage
- `Phases/Phase4/artifacts/corpus/manifest.json` และ `Phases/Phase4/docs/corpus_baseline_report.md` — real-corpus baseline snapshot/report; source fingerprint `ce92294f…b7bceb`
- `Docs/superpowers/specs/2026-08-12-office-typescript-port-design.md` — design ของงาน downstream Office Runtime TypeScript Port และขอบเขต 40k audit/6k–12k implementation estimate
- `Docs/superpowers/plans/2026-08-12-office-typescript-port.md` — implementation plan แบบ task/gate/test สำหรับ TypeScript port
- `Phases/Phase4/tools/build_wave0_index.py` และ `Phases/Phase4/tests/test_wave0_index.py` — builder และ smoke tests สำหรับ Wave 0
- `Phases/Phase4/artifacts/` — field/function/string/call-graph/coverage index และ build manifest ที่สร้างจาก source จริง
- `Phases/Phase4/docs/wave0_report.md` — รายงานผล Wave 0, ข้อจำกัด และงาน Wave 1
- `TODO.md` — backlog งานถัดไปแบบ checkbox แยกตาม dependency
- `Phases/Phase4/tools/build_wave1_resource_map.py` — deterministic builder สำหรับ resource map, selector trace, fixtures และ branch index
- `Phases/Phase4/tests/test_wave1_resource_map.py` — Wave 1 regression/smoke tests
- `Phases/Phase4/artifacts/resource_selector_map.json`, `wave1_branch_index.json`, `wave1_build_manifest.json` — Wave 1 generated evidence
- `Phases/Phase4/artifacts/wave1_gap_register.json` — W1-C0 baseline gap register และ source hashes
- `Phases/Phase4/artifacts/wave1_selector_resolution.json` — W1-C1 static selector write provenance และ unresolved value sources
- `Phases/Phase4/artifacts/wave1_imgface_conflict.json` — W1-C2 raw loop/literal/asset conflict evidence
- `Phases/Phase4/artifacts/wave1_asset_gap_audit.json` — W1-C3 manifest completeness, unmatched IMG_LIST และ TFace namespace audit
- `Phases/Phase4/artifacts/wave1_slices.json` — W1-C4 machine-readable bounded slice metadata
- `Phases/Phase4/docs/wave1_slices/new_game_para_slice_01.md` — bounded slice ของ `NewGamePara`
- `Phases/Phase4/docs/wave1_slices/do_event_slice_01.md` — bounded slice ของ `DoEvent`
- `Phases/Phase4/docs/wave1_closure_report.md` — W1-C5/C6 closure decision และ Wave 2 gate
- `Phases/Phase4/docs/wave1_plan.md` และ `resource_loading.md` — แผนละเอียดและ loader contract
- `Phases/Phase4/docs/wave1_closure_plan.md` — แผน closure pass ที่เหลือ, deliverables, stop rules และ Wave 2 gate
- `Phases/Phase4/tools/build_wave2_scene_contract.py` และ `Phases/Phase4/tests/test_wave2_scene_contract.py` — Wave 2 deterministic builder และ regression tests
- `Phases/Phase4/artifacts/wave2_selector_adapter.json`, `scene_contract.json`, `wave2_room_contract.json`, `wave2_coordinate_contract.json`, `wave2_coordinate_fixture.json`, `wave2_draw_order_contract.json`, `wave2_draw_order_fixture.json`, `wave2_furniture_contract.json`, `wave2_placement_fixture.json`, `wave2_gap_register.json`, `wave2_build_manifest.json` — W2-C0 ถึง W2-C6 contract/evidence/fixture artifacts
- `Phases/Phase4/artifacts/wave2_minimum_scene_fixture.json`, `wave2_wave3_movement_interface.json` — W2-C7 minimum scene gate และ Wave 3 movement boundary
- `Phases/Phase4/docs/wave2_slices/minimum_scene_gate_01.md` — acceptance boundary สำหรับการเริ่ม Wave 3 ในระดับ contract/stub
- `Phases/Phase4/docs/wave2_plan.md` และ `Phases/Phase4/docs/wave2_slices/` — Wave 2 handoff plan, coordinate/draw/furniture slices และ bounded neutral contracts
- `Phases/Phase4/docs/wave3_plan.md` — แผน execution Wave 3 ตั้งแต่ actor evidence register ถึง single-actor closure/handoff
- `Phases/Phase4/tools/build_wave3_actor_contract.py` และ `Phases/Phase4/tests/test_wave3_actor_contract.py` — W3-C0 deterministic builder และ regression tests
- `Phases/Phase4/artifacts/wave3_actor_function_map.json`, `wave3_gap_register.json`, `wave3_build_manifest.json` — W3-C0 actor provenance, controlled gaps และ source hashes
- `Phases/Phase4/docs/wave3_slices/actor_spawn_01.md`, `actor_tick_01.md` — bounded C0 spawn/tick boundaries
- `Phases/Phase4/tools/build_wave3_identity_contract.py`, `build_wave3_state_contract.py`, `build_wave3_movement_contract.py` และ tests ของแต่ละ contract — W3-C1–C3 deterministic builders/regression
- `Phases/Phase4/artifacts/wave3_actor_identity_contract.json`, `wave3_spawn_fixture.json`, `wave3_c1_build_manifest.json` — W3-C1 identity/spawn boundary
- `Phases/Phase4/artifacts/wave3_actor_state_contract.json`, `wave3_state_transition_fixture.json`, `wave3_c2_build_manifest.json` — W3-C2 raw state/transition boundary
- `Phases/Phase4/artifacts/wave3_movement_contract.json`, `wave3_movement_fixture.json`, `wave3_c3_build_manifest.json` และ `docs/wave3_slices/actor_state_tick_01.md`, `actor_movement_01.md` — W3-C2/C3 state/movement fixtures
- `Phases/Phase4/tools/build_wave3_interaction_contract.py`, `Phases/Phase4/tests/test_wave3_interaction_contract.py`, `Phases/Phase4/artifacts/wave3_interaction_contract.json`, `wave3_seat_fixture.json`, `wave3_c4_build_manifest.json`, `docs/wave3_slices/actor_interaction_01.md` — W3-C4 relation/seat boundary
- `Phases/Phase4/tools/build_wave3_animation_contract.py`, `Phases/Phase4/tests/test_wave3_animation_contract.py`, `Phases/Phase4/artifacts/wave3_actor_animation_contract.json`, `wave3_draw_fixture.json`, `wave3_c5_build_manifest.json`, `docs/wave3_slices/actor_animation_01.md` — W3-C5 selector/composition/draw boundary
- `Phases/Phase4/tools/build_wave3_e2e_contract.py`, `Phases/Phase4/tests/test_wave3_e2e_contract.py`, `Phases/Phase4/artifacts/wave3_actor_e2e_fixture.json`, `wave3_actor_trace.json`, `wave3_c6_build_manifest.json`, `docs/wave3_slices/actor_e2e_01.md` — W3-C6 single-actor e2e boundary
- `Phases/Phase4/tools/build_wave3_closure.py`, `Phases/Phase4/tests/test_wave3_closure.py`, `Phases/Phase4/artifacts/wave3_legacy_occupancy_decision.json`, `wave3_c7_build_manifest.json`, `docs/wave3_closure_report.md` — W3-C7 closure/occupancy decision/handoff
- `Phases/Phase4/tools/build_wave4_dialogue_contract.py` และ `Phases/Phase4/tests/test_wave4_dialogue_contract.py` — W4-C0–C6 deterministic builder/regression
- `Phases/Phase4/artifacts/wave4_*` — W4 locale, talk, bubble, event, notification และ actor-dialogue contracts/fixtures/build manifest/gap register
- `Phases/Phase4/docs/wave4_plan.md` และ `Phases/Phase4/docs/wave4_slices/` — Wave 4 execution plan และ bounded source slices
- `Phases/Phase4/tools/build_wave4_closure.py`, `Phases/Phase4/tests/test_wave4_closure.py`, `Phases/Phase4/artifacts/wave4_lifecycle_slices.json`, `wave4_c7_build_manifest.json`, `docs/wave4_closure_report.md` และ lifecycle slice docs — W4-C7 consumer closure/handoff
- `Phases/Phase4/tools/build_wave4_hardening.py`, `Phases/Phase4/tests/test_wave4_hardening.py`, `Phases/Phase4/artifacts/wave4_*_trace.json`, `wave4_hardening_manifest.json`, `docs/wave4_hardening_report.md` และ `wave4_slices/*_02.md` — W4.5 evidence hardening
- `Phases/Phase5/runtime/runtime.js`, `app.js`, `index.html`, `style.css`, `data/room_manifest.json` — Wave 5 deterministic runtime host และ browser adapter
- `Phases/Phase5/tools/build_wave5_manifest.py`, `build_wave5_locale_runtime.py`, `Phases/Phase5/tests/test_wave5_runtime.js`, `test_wave5_contract.py` — Wave 5 builders/tests
- `Phases/Phase5/artifacts/wave5_build_manifest.json`, `wave5_locale_runtime.json`, `wave5_runtime_contract.json`, `wave5_adapter_policy.json`, `wave5_event_catalog.json`, `wave5_gap_register.json`, `wave5_visual_test_report.json` — Wave 5 contracts, source manifest, locale runtime, controlled gaps และ smoke report
- `Phases/Phase5/artifacts/wave5_1_furniture_manifest.json`, `wave5_1_transform_depth_contract.json`, `wave5_1_timer_contract.json` — W5.1 bounded furniture, transform/depth และ timer closure artifacts
- `Phases/Phase5/artifacts/wave5_1_animation_policy.json`, `wave5_1_selector_gap_contract.json`, `wave5_1_event_mode_policy.json` — W5.1 adapter animation, TFace classification และ raw event policy artifacts
- `Phases/Phase5/artifacts/wave5_2_furniture_mapping_contract.json` — W5.2 image-slot, suffix, asset join และ crop/placement gap contract
- `Phases/Phase5/artifacts/wave5_2_furniture_draw_fixture.json` — W5.2 furniture draw fixture พร้อม source/crop/placement status
- `Phases/Phase5/artifacts/wave5_3_numeric_crop_placement_contract.json` — W5.3 numeric selectors, floor-parts sentinel, image-data records, crop formulas และ bounded `CallHikkosi` placement
- `Phases/Phase5/artifacts/wave5_4_img_list_loader_bridge.json` — W5.4 loader bridge, selector namespace split, manifest candidates และ cross-source literal conflict
- `Phases/Phase5/tools/build_wave5_5_img_list_alignment.py` และ `Phases/Phase5/artifacts/wave5_5_img_list_alignment.json` — W5.5 corrected label indexing, active metadata value alignment และ exact bihin selector/filename join
- `Phases/Phase5/tools/build_wave5_6_floorparts_seb.py` และ `Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json` — W5.6 floor-parts selector, floor-main probe และ SEB structural/RECT-tail evidence
- `Phases/Phase5/tools/build_wave5_7_seb_consumer_contract.py` และ `Phases/Phase5/artifacts/wave5_7_seb_consumer_contract.json` — W5.7 SEB loader consumer, crop, local base, bounding/anchor evidence
- `Phases/Phase5/tools/build_wave5_8_room_caller_contract.py` และ `Phases/Phase5/artifacts/wave5_8_room_caller_contract.json` — W5.8 RenderGameScreen/DrawObj PNG room caller, screen origin, crop/placement และ SEB caller separation evidence
- `Phases/Phase5/tools/build_wave5_9_object_producer_contract.py` และ `Phases/Phase5/artifacts/wave5_9_object_producer_contract.json` — W5.9 AddObjec/MainProcess/furniture producer provenance, camera no-op boundary และ direct floor0.seb mapping scan
- `Phases/Phase5/docs/wave5_runtime_architecture.md`, `wave5_closure_report.md`, `Phases/Phase5/README.md` — Wave 5 architecture, closure report และ phase handoff
- `Phases/Phase6/runtime/task_system.js`, `task_storage.js`, `task_repository.js` — Wave 6 task engine, lifecycle, assignment, notification, activity log และ repository/persistence adapters
- `Phases/Phase6/tests/test_wave6_task_system.js`, `test_wave6_contract.py`, `Phases/Phase6/tools/build_wave6_manifest.py` — Wave 6 runtime/contract tests และ source manifest builder
- `Phases/Phase6/artifacts/` — Wave 6 task, assignment, event, notification, queue, interaction, repository, permission, migration, gap และ build manifest artifacts
- `Phases/Phase6/artifacts/wave6_repository_contract.json`, `wave6_permission_policy.json`, `wave6_migration_fixture.json` — W6.1 repository, local permission และ migration contracts
- `Phases/Phase6/docs/wave6_plan.md`, `wave6_runtime_architecture.md`, `wave6_closure_report.md`, `Phases/Phase6/README.md` — Wave 6 plan, architecture, closure และ handoff
- `Phases/Phase4/tools/build_cross_wave_gap_reconciliation.py`, `Phases/Phase4/tests/test_cross_wave_gap_reconciliation.py`, `Phases/Phase4/artifacts/cross_wave_gap_reconciliation.json` — current cross-wave gap view และ stale-status reconciliation
- `Phases/Phase4/tools/build_targeted_gap_scan.py`, `Phases/Phase4/tests/test_targeted_gap_scan.py`, `Phases/Phase4/artifacts/targeted_gap_scan.json` — read-only source scan ของ uncovered functions, TFace callers, actor/object fields, room/SEB และ event touchpoints
- `Phases/Phase4/tools/build_semantic_gap_trace.py`, `Phases/Phase4/tests/test_semantic_gap_trace.py`, `Phases/Phase4/artifacts/semantic_gap_trace.json` — bounded `NewGamePara`/`DoEvent` branch-context และ `TFace=40/41` producer trace

## การเปลี่ยนแปลงล่าสุด

- อนุมัติและวางแผน P0-A Corpus Intelligence Pipeline: import Phase 4–6 evidence, canonical full-corpus index, lossless views, optional Cpp2IL comparison, 100-function pilot, cached candidate maps, validator, negative-evidence ledger และ closure gate; P0-B TypeScript ถูกจัดเป็น downstream
- สร้างและ execute detailed P0-A0 plan: ล็อก input boundary/manifest schema/namespace-safe fingerprint/`--check` exit codes, เพิ่ม TDD tests และสร้าง real baseline/report พร้อม A1 handoff
- ลบ `game-dev-story-mod_Dumped/` ออกจาก GitHub และเพิ่มทั้งโฟลเดอร์เข้า `.gitignore`
- ลบ `APK_Toolkit/` และ `viewer/` ออกจาก GitHub และเพิ่มทั้งสองโฟลเดอร์เข้า `.gitignore` ตามขอบเขตการอัปโหลดใหม่
- สร้าง Phase 2 catalog/tooling/previews/tests และอัปเดต Phase 2 README, roadmap และ state ตามผลตรวจจริง
- ปรับ parser/code trace ให้รองรับ multiline `DrawHuman` callsites และบันทึก composition contract กับ HumanDex dynamic selector evidence
- ตรวจ codebase/asset จริงเพื่อวางแผน selective code translation และอัปเดต Phase 4/phase index ให้สะท้อนว่าแผนพร้อมแล้วแต่ยังไม่เริ่ม translation
- รัน Wave 0 builder, แก้ field grouping และจัดประเภท terminal string sentinel ตามหลักฐานจริง; ตรวจ test 6/6 ผ่าน และอัปเดต Phase 4/roadmap/state ให้เข้าสู่ Wave 1
- เริ่ม Wave 1: สร้าง resource/selector map, fixtures และ structural branch index จาก source จริง; สร้าง docs/tests และระบุ face-prefix/base-selector gaps เป็น `unknown`
- ทำ W1-C0: ตรึง baseline, แก้ branch index ให้บันทึก raw address namespace, สร้าง gap register 8 รายการ และเพิ่ม regression coverage
- ทำ W1-C1 บางส่วน: trace cctor write sites/GOT relocations ของ static selectors 5 ตัว; คง numeric values เป็น unresolved ตามหลักฐาน
- ทำ W1-C2: trace raw BootForm loop, ยืนยัน literal conflict และเพิ่ม regression test โดยไม่แก้ค่าแบบเดา
- ทำ W1-C3: ตรวจ manifest/asset roots 291 records, เพิ่ม canonical basename join สำหรับ floorCover และจัดประเภท asset/index gaps
- ทำ W1-C4: สกัด bounded slices ของ `NewGamePara`/`DoEvent`, map call targets ที่มีหลักฐานตรง และคง helper/field semantics ที่ยังไม่ยืนยันเป็น unresolved/neutral
- ทำ W1-C5/C6: สร้าง closure report, ปรับ gap impact ให้สะท้อนว่า Wave 2 ใช้ symbolic preconditions ได้ และรัน regression 18/18 ผ่าน
- เริ่ม Wave 2: สร้าง symbolic selector adapter, AddObjec scene contract, room/SEB asset fixture, coordinate evidence และ DrawObj dispatch/sort evidence; รัน regression 28/28 และยืนยัน source hashes ไม่เปลี่ยน
- ทำ Wave 2 ต่อ: สร้าง centered-origin coordinate fixture, neutral draw-order fixture, furniture accessor/relation contract และ bounded `CallHikkosi` placement fixture; รัน regression 32/32 และคง semantic gaps เป็น recoverable/not_closed
- ทำ Wave 2 minimum gate: ยืนยัน observed object anchor/crop callsites, สร้าง combined room/object/coordinate/draw fixture และ explicit Wave 3 movement interface; คง final room/depth/legacy movement semantics เป็น open
- วางแผน Wave 3 โดยแบ่ง actor truth เป็น baseline, identity/spawn, state/timer, movement, seat/interaction, animation/draw และ end-to-end closure; คง legacy semantics ที่ยังไม่พบเป็น adapter decision หรือ unresolved
- เริ่มและทำ W3-C0: สร้าง actor function/field provenance map, gap register, bounded spawn/tick slices และ regression test; Phase 4 regression ผ่าน 42/42 และ source hashes ตรง baseline
- ทำ W3-C1: สร้าง employee parameter/actor initial-write map, bounded stable-ID spawn fixture และรัน test ผ่าน; คง public identity เป็น adapter policy
- ทำ W3-C2: สร้าง raw state field/transition audit และ neutral fixture; แก้ manifest summary ให้สอดคล้องกับ contract และรัน test ผ่าน
- ทำ W3-C3: สร้าง raw `AddTarget`/`NextTarget` flow, coordinate-space boundary, provider contract และ deterministic movement fixture; regression ณ จุดนั้นผ่าน 59/59 และ Phase 2 ผ่าน 5/5
- ต่อ W3-C2: เพิ่ม bounded `MainProcess` raw tick slices และ fixture สำหรับ wait/reset/mode-state/anime counter โดยไม่ promote semantic timing
- ทำ W3-C4: สร้าง furniture relation audit, explicit seat adapter contract และ fixture success/conflict/release/non-owner/unavailable; คง legacy occupancy เป็น `not_closed`
- รัน regression หลัง W3-C2/C4: builder checks ของ W3-C0–C4 ผ่าน, Phase 4 รวมผ่าน 66/66 และ Phase 2 ผ่าน 5/5
- ทำ W3-C5: สร้าง bounded actor selector/composition contract, TFace 40/41 unresolved cases และ deterministic draw fixture; ไม่แก้ Phase 2 semantic mapping เพราะไม่มี evidence ใหม่เรื่อง timing/loop/direction
- รัน regression หลัง W3-C5: builder checks ของ W3-C0–C5 ผ่าน, Phase 4 รวมผ่าน 73/73 และ Phase 2 ผ่าน 5/5
- ทำ W3-C6: รวม C1–C5 กับ Wave 2 minimum scene เป็น single-actor e2e fixture 6 scenarios และ golden trace 7 events; รัน C6 test ผ่าน
- รัน regression หลัง W3-C6: builder checks ของ W3-C0–C6 ผ่าน, Phase 4 รวมผ่าน 81/81 และ Phase 2 ผ่าน 5/5
- ทำ W3-C7: ตรวจ controlled gaps, สร้าง closure report และตัดสินใจ occupancy เป็น adapter-only สำหรับ scope ปัจจุบันโดยไม่แก้ Phase 2 mapping
- รัน regression หลัง W3-C7: builder checks ของ W3-C0–C7 ผ่าน, Phase 4 รวมผ่าน 88/88 และ Phase 2 ผ่าน 5/5
- เริ่ม Wave 4: สร้าง deterministic `build_wave4_dialogue_contract.py` จาก CSV, dump, categorized C, DoEvent assembly และ Wave 3 artifacts แบบ read-only
- ทำ W4-C0–C5: สร้าง locale/talk/bubble/event/actor-dialogue contracts, fixtures, source evidence และ controlled gap register
- ทำ W4-C6: สร้าง `AddMessage` notification contract/fixture โดยคง raw lifetime `0x60` และ graph ID semantics เป็น open
- รัน Wave 4 regression `8/8`, Phase 4 รวม `96/96` และ Phase 2 `5/5`; `--check` ของ Wave 4 builder ผ่าน
- ทำ W4-C4/C6 bounded consumer slice: ยืนยัน `HumanFukiTime` decrement, `DrawObj` timer/index gate, MessageTime decrement/expiry compaction และ DoEvent target/RVA map โดยไม่ตั้งชื่อ mode/timer/graph semantics
- ทำ W4-C7: สร้าง lifecycle artifact, closure report และ C7 manifest; อัปเดต gap register, README, roadmap, TODO และ state เป็น `complete_with_known_limitations`
- รัน final Wave 4 contract `8/8` + closure `5/5`, Phase 4 `101/101`, Phase 2 `5/5`, builder `--check` และ `git diff --check`
- ทำ W4.5-R1/R2: trace logical tick `1/2/16`, HumanFuki write/read/cleanup boundary, talk split/replace/parse/name pipeline และยืนยัน raw speaker-to-actor caller ไม่พบใน scoped sources
- ทำ W4.5-R3/R4: trace MessageGraph `1/2` render path และ SoundPlay threshold; เพิ่ม DoEvent target clusters/nearby constants โดยไม่ตั้งชื่อ numeric modes
- รัน final W4.5 hardening `6/6`, Phase 4 `107/107`, Phase 2 `5/5`, builder checks และอัปเดต gap register/README/roadmap/TODO/state
- เพิ่ม checklist ความคืบหน้าใน `Docs/AI_Agent_Office_Roadmap.md` และสร้าง `TODO.md` เพื่อแยก roadmap ระดับ Phase ออกจากงานย่อยที่พร้อมลงมือทำ
- เริ่มและปิด Wave 5 C0–C8: สร้าง deterministic runtime host, room manifest, locale artifact, adapter policy/event/gap artifacts และ visual smoke snapshot
- ทำ W5.1-B–G: เพิ่ม bounded reception/desk/chair asset renderer, mixed draw-order contract, logical timer, explicit animation profiles, TFace gap classification และ raw numeric-event bridge โดยคง legacy gaps
- ทำ W5.2: แยก `imgBihin_`/`imgFloorParts`, เชื่อม office asset indices และเพิ่ม source/crop/placement metadata ใน runtime draw commands
- ทำ W5.3: decode packed static selectors, ยืนยัน `IndexImgFloorParts=-1`, decode metadata furniture records, ปิด bounded crop formulas และ numeric `CallHikkosi` placement; คง `IMG_LIST` namespace join เป็น gap
- ทำ W5.4: ยืนยัน `AppData.GetImage` name-to-array bridge และ `LoadBihinImage` selector flow; พบ recovered `IMG_LIST` names ไม่ join furniture manifest และบันทึก string-literal extraction conflict โดยไม่ hardcode runtime mapping
- ทำ W5.5: แก้ one-based `StringLiteral_N`/zero-based JSON indexing, align native values กับ APK metadata, ปิด bihin exact joins และ mark W5.4 direct-index result as superseded
- ทำ W5.6: ปิด observed floor-parts/floor-main selector joins, ถอด SEB group/record framing และบันทึก `RECT` optional-tail/partial-record evidence โดยไม่เติม bytes
- ทำ W5.7: trace `LoadSeb`/`GetSpritesLocal`/`ConvBufferToSprite`/`DrawSeb`, ปิด local `U/V/W/H` crop + `base + trans` placement, `GetBRectSeb` base addition และ anchor offset lifecycle; คง room caller/depth/transform semantics เป็น open
- ทำ W5.8: trace `RenderGameScreen` → `SetOrigin` → `DrawObj`, ปิด bounded `ObjecX/Y + ObjecZX/ZY` PNG room placement/crop และยืนยันไม่มี `ResourceManager.DrawSeb` ใน scoped `DrawObj`; คง producer-side world/SEB mapping เป็น open
- ทำ W5.9: trace `AddObjec` parameter-to-field writes, `MainProcess` `ObjecX/Y` averaging, `CallPCChange`/`CallDeskChange`/`CallChairChange` field updates, camera no-op bodies และ generic `LoadSeb` bridge; คง source-array/world/isometric/depth/SEB room semantics เป็น open
- รัน Wave 5 Node runtime 10 scenarios, Python/visual contract 17 tests, Phase 4 107/107, Phase 2 5/5 และ `git diff --check`; source roots เดิมยัง read-only
- เริ่มและปิด Wave 6 W6-C0–C7: สร้าง task engine, contracts, assignment rules, durable task notifications, activity log, Agent projection, local persistence และ dashboard integration
- เพิ่ม public `OfficeRuntime.setAgentTaskProjection`/`recordAdapterEvent` โดยคง Wave 5 behavior เดิมและติด source `phase6_task_system` ให้ runtime mirror events
- รัน Wave 6 task `12/12`, contract `8/8`, Wave 5 runtime `10/10`, Phase 5 `17/17`, Phase 4 `107/107`, Phase 2 `5/5`, browser smoke และ `git diff --check`; temporary local server ถูกหยุดแล้ว
- ทำ Wave 6.1: เพิ่ม `TaskRepository` boundary, repository envelope/revision, migration จาก direct snapshot, optimistic conflict/reload, explicit local permission policy และ JSON import/export พร้อม dashboard persistence status
- รัน Wave 6.1 task `15/15` และอัปเดต repository/permission/migration contracts; backend/auth/multi-user, auto-assignment และ legacy camera transform ยังคงเป็น known limitations
- ทำ Phase 6 final hardening: ตรวจ strict task/notification/activity snapshots, validate repository failures, รักษา in-memory state เมื่อ reload เสีย, เพิ่ม lifecycle button guards, task description และ notification dismiss UI
- รัน Phase 6 task `18/18`, contract `11/11`, Wave 5 `10/10`, Phase 5 `17/17`, Phase 4 `107/107`, Phase 2 `5/5`, fresh browser smoke และ `git diff --check`; temporary local server ถูกหยุดแล้ว
- ทำ Phase 4 cross-wave gap audit: สร้าง reconciliation จาก gap registers Wave1–6 และ later Wave5/6 evidence; แยก resolved-later 7 กลุ่มออกจาก open recoverable/not-found/product boundary โดยไม่แก้ historical registers
- ทำ Phase 4 targeted gap scan: ตรวจ uncovered functions, parse `DrawHuman` selectors, actor/object fields, room/SEB references และ event producers; พบ `TFace=40/41` source hits 9/1 และยังไม่พบ direct `floor0.seb` room caller
- รัน reconciliation `6/6`, targeted scan `5/5` และ builder `--check` ผ่าน; source roots เดิมยัง read-only
- ทำ Phase 4 semantic gap trace: จัดกลุ่ม bounded `NewGamePara`/`DoEvent` branch-call-field context และ trace `TFace=40/41` producer/caller โดยคง unresolved status ที่หลักฐานยังไม่พอ
- รัน semantic trace `5/5`, Phase 4 regression `123/123`, Phase 2 `5/5` และ builder `--check`; source roots เดิมยัง read-only
- ทำ P0-A0: สร้าง manifest `p0-a0.corpus-baseline.v1`, report, namespace-safe SHA-256 fingerprint และ drift gate จาก source/artifact inputs จริง; source roots เดิมยัง read-only
- รัน P0-A0 focused `16/16`, Phase 4 regression `139/139`, Phase 2 `5/5`, temporary-output determinism, schema/output gate, `--check` และ `git diff --check`; historical artifacts ไม่มี diff

## งานที่ต้องทำต่อ

1. ทำ P0-A1 ตาม `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md` โดยใช้ `Phases/Phase4/artifacts/corpus/manifest.json` เป็น input boundary และไม่เขียนทับ historical artifacts
2. หลัง P0-A gate ผ่าน จึงเริ่ม P0-B Office Runtime TypeScript ตาม `Docs/superpowers/plans/2026-08-12-office-typescript-port.md` โดยใช้ promoted evidence เป็น input เดียว
3. ใช้ corpus query และ negative-evidence ledger ก่อน trace ซ้ำ; เปิดงานใหม่เฉพาะเมื่อมี source/evidence delta หรือ product dependency ที่ระบุได้
4. ถ้าต้องการปิดต่อ ให้ trace full initialization/reset/exit lifecycle ของ `NewGamePara`/`DoEvent` และ producer parameters รอบ target clusters; bounded clusters ที่หลักฐานถึงแล้วอยู่ใน `semantic_gap_trace.json`
5. ค้น alternate asset/index namespace หรือ source pack ของ literal `TFace=40/41`; หากไม่มี extraction เพิ่ม ให้คงเป็น extraction/index-space gap พร้อมหลักฐานที่ trace แล้ว
6. trace source-array semantics (`GameForm+0xE40/+0xF50/+0xF58`), camera/world-isometric mapping, nonzero `ObjecZX/ZY`, depth/pivot และ direct `floor0.seb` room mapping หากมี product dependency
7. ถ้ามี source/asset extraction เพิ่ม ค่อยตรวจ full SEB room reconstruction; ไม่สังเคราะห์ 4-byte tail ที่หาย
8. ถ้า runtime ต้องการ fidelity เพิ่ม ค่อย trace timer unit, zero-time `HumanFukiIndex`, talk tokens, graph labels หรือ event modes แบบ targeted
9. ถ้าต้องการ product deployment ค่อยเพิ่ม remote task backend, authentication, server-side permissions, multi-user sync และ auto-assignment ผ่าน boundaries เดิม
10. คง `legacy_equivalence=false` และไม่ promote `talking`, animation semantics หรือ numeric event modes
