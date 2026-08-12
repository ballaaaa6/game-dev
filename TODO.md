# TODO

รายการนี้เป็น backlog ที่ลงมือทำต่อได้จริง โดยเรียงตาม dependency และความสำคัญ ไม่ใช่รายการความฝันระยะยาวทั้งหมดของ roadmap

อัปเดตล่าสุด: 2026-08-12

## Primary — Corpus Intelligence Pipeline (P0-A, urgent)

งานนี้ถูกยกระดับให้ทำก่อนการ port runtime และก่อนเปิดงานเก็บ Phase อื่นต่อ โดยนำ evidence/contract/fixture
ของ Phase 4–6 มาใช้เป็นฐาน ไม่เริ่มวิเคราะห์จากศูนย์ และไม่แก้ source extraction roots

Design: `Docs/superpowers/specs/2026-08-12-corpus-intelligence-pipeline-design.md`
Plan: `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md`
A0 detail: `Docs/superpowers/plans/2026-08-12-p0-a0-corpus-baseline.md`

เป้าหมายคือสร้าง full-corpus index ที่ค้นหาได้, lossless annotated/prompt views, cross-tool comparison,
candidate logic maps, source validator และ negative-evidence ledger โดยเก็บ metadata ของส่วนที่ยังไม่เกี่ยวกับ
office ไว้สำหรับ feature ในอนาคต

- [x] P0-A0 freeze source/artifact hashes และสร้าง corpus baseline manifest
  - [x] สร้าง `p0-a0.corpus-baseline.v1` manifest/report จาก source roots และ Phase 0/4/5/6 artifacts แบบ read-only
  - [x] เพิ่ม canonical SHA-256 fingerprint, namespace-safe records, และ `--check` drift gate
  - [x] ผ่าน A0 focused `16/16`, Phase 4 regression `139/139`, Phase 2 regression `5/5` และ `git diff --check`
- [ ] P0-A1 import Phase 4/5/6 evidence และ current gap reconciliation โดยไม่เขียนทับ historical artifacts
- [ ] P0-A2 สร้าง canonical function/field/string/resource/call/data-flow index สำหรับ corpus ทั้งหมด
- [ ] P0-A3 สร้าง raw/annotated/normalized views พร้อม stable unit IDs และ source maps
- [ ] P0-A4 สร้าง prompt-compressed views ที่ reconstruct กลับ raw ได้และวัด token จริง
- [ ] P0-A5 เปรียบเทียบ Il2CppDumper/Ghidra กับ Cpp2IL เมื่อ tool พร้อม โดยคง conflict เป็น evidence
- [ ] P0-A6 รัน pilot 100 functions และผ่าน determinism/losslessness/schema/source-reference gate
- [ ] P0-A7 สร้าง cached candidate translation requests และ offline/provider boundary
- [ ] P0-A8 สร้าง source validator, fixture promotion, query CLI และ negative-evidence ledger
- [ ] P0-A9 สร้าง corpus closure report และส่ง handoff ให้ P0-B

## Downstream — Office Runtime TypeScript Port (P0-B)

งานนี้เป็นงานหลักถัดจาก P0-A และจะเริ่มเมื่อ corpus closure gate ผ่าน โดย port เฉพาะเส้นทางที่ Virtual AI Office ใช้จริง
ไม่ port เกมเต็มและไม่ถือว่า JSON artifact เป็น implementation

Design: `Docs/superpowers/specs/2026-08-12-office-typescript-port-design.md`
Plan: `Docs/superpowers/plans/2026-08-12-office-typescript-port.md`

ขอบเขตที่ตรวจพบจาก source จริง: Phase 4 shortlist 88 functions, recovered C ที่อยู่ใน shortlist ประมาณ 40,974 บรรทัด,
assembly fallback ของ `NewGamePara`/`DoEvent` รวม 29,240 instructions. ตัวเลขนี้เป็น audit boundary ไม่ใช่ target
ที่จะคัดลอกทั้งหมด; เป้าหมาย implementation เริ่มต้นประมาณ TypeScript 6,000–12,000 บรรทัด และ tests/fixtures 2,000–4,000 บรรทัด

- [ ] P0-B0 สร้าง isolated TypeScript toolchain และ `SourceRef`/typed legacy namespace
  - [ ] freeze `runtime.js` baseline และสร้าง migration guard ก่อนเปลี่ยน browser consumer
  - [ ] สร้าง `Phases/Phase5/package.json`/`tsconfig.json` โดยแยก `tsc` Node output กับ esbuild browser bundle
  - [ ] สร้าง `runtime-ts/src/source-ref.ts`, `types.ts`, `index.ts`
  - [ ] กำหนดสถานะ `evidence_ready → contract_ready → ts_ported → verified | blocked`
- [ ] P0-B1 port resource, selector และ room/furniture runtime
  - [ ] port `GetImage`, `LoadBihinImage`, `EventGChange`, `AddObjec`, `CallHikkosi`
  - [ ] port furniture selector/crop/placement/draw command ที่มีหลักฐานแล้ว
  - [ ] รักษา `TFace=40/41`, source-array, pivot/depth/transform ที่ยังไม่ยืนยันเป็น raw/adapter status
- [ ] P0-B2 port actor, movement, seat และ body/face draw
  - [ ] port `AddSyain`, `CallSyain`, `AddBodyFace`, `DrawHuman`, `NextTarget`
  - [ ] ใช้ injected path/collision/seat providers ตาม Wave 3/5 contracts
  - [ ] ไม่ port `MainProcess`/`NextPoint` ทั้ง function และไม่ตั้งชื่อ animation semantic จากการเดา
- [ ] P0-B3 port dialogue, bubble, notification และ event bridge
  - [ ] port `GetTalkTexts`, `GetTalkIndex`, `AddKaiwa`, `AddFuki`, `DrawFukidashi`, `AddMessage`
  - [ ] ใช้ locale generated lookup และ logical tick ที่ระบุเป็น web adapter
  - [ ] เก็บ numeric event mode/graph ID/speaker binding ที่ยัง unknown เป็น raw
- [ ] P0-B4 เชื่อม compiled TypeScript กับ Phase 5/6 browser shell
  - [ ] รักษา public `OfficeRuntime` methods ที่ `app.js` ใช้อยู่
  - [ ] เพิ่ม browser entry และย้าย consumer ทีละ moduleหลัง focused tests ผ่าน
  - [ ] รัน Node runtime, Phase 2/4/5/6 tests และ browser smoke ทุก checkpoint
- [ ] P0-B5 สร้าง port coverage manifest และ closure gate
  - [ ] ผูกทุก product-scope unit กับ source symbol, artifact, module และ test
  - [ ] ห้าม mark `ts_ported` ถ้ายังมีเพียง JSON/pseudocode
  - [ ] สร้าง `office_typescript_port_manifest.json` และ closure report
- [ ] P0-B6 อนุมัติการขยับไป Phase 7 ต่อเมื่อ TypeScript port gate ผ่าน
  - [ ] runtime path ไม่อ่าน recovered C โดยตรง
  - [ ] unknown ถูกแสดงเป็น raw/adapter status
  - [ ] Phase 2/4/5/6 regression และ browser smoke ผ่านโดยไม่มี console error/warning ใหม่

## Completed — Wave 6 task system และ dashboard

Wave 6 W6-C0–C7 และ W6.1 ปิดรอบแบบ `complete_with_known_limitations`; task system เป็น
product web adapter ใหม่บน Wave 5 โดยไม่เชื่อม AI และไม่อ้าง legacy equivalence

- [x] W6-C0 freeze baseline, contract และ controlled gap register
  - [x] สร้าง task/assignment/event/notification contracts
  - [x] คง source roots เดิมแบบ read-only และ `legacy_equivalence=false`
- [x] W6-C1 สร้าง deterministic task engine
  - [x] create/list/get task และ priority queue
  - [x] lifecycle `queued` → `working` → `blocked`/`done`
  - [x] ใช้ logical tick และ terminal `done` policy
- [x] W6-C2 สร้าง assignment rules
  - [x] one active task ต่อ Agent
  - [x] assignee validation, moving-agent guard และ conflict tests
  - [x] ไม่สั่ง movement/collision/seat จาก task action
- [x] W6-C3 สร้าง durable notification และ activity log
  - [x] แยก task notification จาก Wave 5 raw graph notification
  - [x] เก็บ named `task.*` events และ runtime diagnostic mirror
- [x] W6-C4 เชื่อม Agent projection
  - [x] เพิ่ม `taskId`/`taskStatus` projection ผ่าน public runtime adapter
  - [x] task state เปลี่ยน Agent state เฉพาะใน explicit lifecycle action
- [x] W6-C5 เพิ่ม persistence
  - [x] repository boundary, versioned localStorage key `phase6.task_state.v1` และ migration envelope
  - [x] optimistic revision conflict detection พร้อม reload path และ visible status
  - [x] memory-only fallback, restore, reset และ export
- [x] W6-C6 เพิ่ม dashboard interaction
  - [x] create/filter/detail/assign/start/block/resume/complete
  - [x] notification/activity panel และ Agent focus highlight
- [x] W6-C7 ปิด QA และ handoff
  - [x] Wave 6 tests `18/18` + contract tests `11/11`
  - [x] browser smoke ผ่าน, console error/warning `0`
  - [x] Wave 5 `10/10`, Phase 5 Python `17`, Phase 4 `107`, Phase 2 `5` ผ่าน
  - [x] อัปเดต Phase 6 README, roadmap, state และ closure artifacts

## Completed — Wave 6.1 production hardening

- [x] W6.1-A แยก `TaskRepository` interface จาก `TaskSystem` และเพิ่ม repository envelope
- [x] W6.1-B migrate snapshot ตรงจาก Wave 6.0 เป็น envelope revision `0`
- [x] W6.1-C เพิ่ม optimistic conflict handling, `reloadFromRepository()` และ degraded status
- [x] W6.1-D เพิ่ม explicit local permission policy โดยไม่อ้าง authentication
- [x] W6.1-E เพิ่ม `wave6-task-export-v1` import/export และ dashboard controls
- [x] W6.1-F เพิ่ม migration/conflict/permission contract fixtures และ regression coverage

ข้อจำกัดที่ยังเปิด: repository ยังใช้ localStorage เท่านั้น, ยังไม่มี auth/backend/multi-user,
auto-assignment ยังอยู่ Phase 7 และ focus ยังเป็น adapter highlight ไม่ใช่ legacy camera transform

## Completed — Phase 6 final hardening

- [x] strict validation สำหรับ task, notification, activity และ `legacy_equivalence=false`
- [x] validate repository envelope/save result และรายงาน localStorage failure เป็น degraded state
- [x] failed reload ไม่ล้าง in-memory state เดิม
- [x] dashboard lifecycle button guards, task description และ notification dismiss
- [x] runtime `18/18`, contract `11/11`, Wave 5 `10/10`, Phase 5 `17/17`, Phase 4 `107/107`, Phase 2 `5/5`
- [x] fresh browser smoke ผ่านและ console error/warning `0`; temporary server ถูกหยุดแล้ว

## Completed — Phase 4 cross-wave gap audit (2026-08-12)

- [x] สร้าง `cross_wave_gap_reconciliation.json` เพื่อ reconcile historical registers โดยไม่แก้สถานะเดิม
- [x] แยก later evidence ที่ปิดแบบ bounded แล้ว 7 กลุ่ม: selector values, face prefix/suffix, bihin/floorparts joins, SEB local placement, PNG room placement และ object-producer fields
- [x] สร้าง `targeted_gap_scan.json` จาก recovered C/Method/dump/assembly แบบ read-only
- [x] ยืนยัน source facts ใหม่: `DrawHuman` มี 106 symbol references, 36 parseable calls, literal `TFace=40` 9 จุด และ `TFace=41` 1 จุด; current face family ยัง `face_0..35`
- [x] ยืนยัน scoped C/assembly scan ไม่พบ literal `floor0.seb` หรือ direct `floor0.seb → DrawObj` caller
- [x] เพิ่ม deterministic builders/tests และผ่าน reconciliation `6/6` กับ targeted scan `5/5`

## Completed — Phase 4 bounded semantic gap trace (2026-08-12)

- [x] สร้าง `semantic_gap_trace.json` จาก assembly fallback, recovered C, `dump.cs` และ existing Wave 3/4 artifacts แบบ read-only
- [x] จัดกลุ่ม `NewGamePara`: static guard, repeated `AddObjec` setup 29 calls, unresolved helper cluster และ terminal boundary; ยืนยัน `w0` write-back ครบ 29/29 แต่ไม่ promote full lifecycle
- [x] จัดกลุ่ม `DoEvent`: `KikakuMode` comparison values `5/7/8` ที่ไปถึง bounded LT/Replace/AddKaiwa clusters และ `EventMode` indexed dispatch comparison `2`; numeric mode names ยังเป็น `unknown`
- [x] Trace `TFace=40/41` ทั้ง 10 literal callsites; ไม่พบ direct literal producer ใน scoped actor field paths (`HumanFaceG`/`HumanBodyG`/`SyainFaceG`/`HumanDexFaceG`)
- [x] เพิ่ม deterministic builder/test และผ่าน semantic trace `5/5`, Phase 4 regression `123/123`, Phase 2 `5/5`

## Next — Phase 4 targeted semantic recovery

- [x] จัดกลุ่ม bounded branch สำคัญของ `NewGamePara`/`DoEvent` จาก structural index + caller/field context โดยยังไม่ตั้งชื่อ mode ที่หลักฐานไม่พอ
- [x] trace producer/caller ของ `TFace=40/41`; ไม่พบ direct literal producer ใน scoped actor paths และคงเป็น extraction/index-space gap
- [ ] ปิดต่อเฉพาะเมื่อมีหลักฐาน: full initialization/reset/exit lifecycle, AddObjec parameter semantics หรือ alternate TFace asset/index namespace
- [ ] ค้น producer-side world/isometric/camera/pivot และ direct SEB room caller; ถ้าไม่มี source เพิ่มให้คงเป็น bounded/open
- [ ] ค่อย trace timer unit, talk token, graph/audio labels และ actor semantic animation เมื่อมี dependency ที่ต้องใช้จริง

## Remaining — Wave 5 minimal web office runtime follow-ups

Wave 5 C0–C8, W5.1-B–G, W5.2, W5.3, W5.4, W5.5, W5.6 floor-parts/SEB structural trace, W5.7
SEB consumer/crop/base-placement trace, W5.8 room-caller/screen-placement trace และ W5.9
object-producer/camera/SEB mapping trace ปิดรอบแบบ
`complete_with_known_limitations`; asset namespace join, semantic animation และ targeted event
translation ยังเป็น follow-up ที่ไม่ block runtime MVP

- [x] W5-C0 สร้าง runtime host และ build manifest
  - [x] วาง runtime ไว้ใต้ `Phases/Phase5/runtime/`
  - [x] คง source assets เดิมแบบ read-only และอ้าง URL กลับ source root
  - [x] สร้าง `wave5_build_manifest.json` และ `wave5_gap_register.json`
- [x] W5-C1 สร้าง room/asset adapter
  - [x] ใช้ `floor0.png` เป็น verified background
  - [x] คง `floor0.seb` tail shortfall 4 bytes
  - [x] ใช้ bounded reception/desk/chair asset renderer จาก source-root PNG จริง
  - [x] คง fixture-specific coordinate/depth profile และ placement เป็น adapter-only
- [x] W5-C2 สร้าง runtime state schema
  - [x] แยก Agent state, movement status, raw legacy fields และ draw selectors
  - [x] สร้าง deterministic snapshot และ event log
- [x] W5-C3 สร้าง logical tick/lifecycle cleanup
  - [x] ทำ logical clock แยกจาก wall-clock milliseconds
  - [x] cleanup bubble/notification เมื่อหมดอายุ
- [x] W5-C4 สร้าง movement/collision/seat adapter
  - [x] ทำ explicit path/collision/seat providers
  - [x] ผ่าน movement, blocked movement และ seat conflict/release scenarios
- [x] W5-C5 สร้าง draw adapter
  - [x] ใช้ 42 BodyFace records และ body/face crop contract
  - [x] คง `TFace=40/41` เป็น unresolved โดยไม่ substitute
  - [x] ใช้ static verified frame policy สำหรับ unknown animation
- [x] W5-C6 สร้าง locale/talk/bubble adapter
  - [x] สร้าง locale runtime จาก CSV 12 ภาษา, union IDs 2,420
  - [x] คง default `th` เป็น web adapter decision และรักษา placeholder
  - [x] ทำ dialogue → bubble → expire flow
- [x] W5-C7 สร้าง named event/notification bridge
  - [x] สร้าง named web event catalog
  - [x] คง raw graph ID และไม่ตั้งชื่อ numeric event mode
  - [x] ทำ notification expiry/compaction
- [x] W5-C8 ปิด visual QA และ closure
  - [x] browser smoke boot/floor/actor/control/console checks
  - [x] เพิ่ม visual regression snapshot ที่ `Phases/Phase5/artifacts/wave5_smoke.jpg`
  - [x] รัน Phase 2/Phase 4 full regression พร้อม Phase 5 และสร้าง final closure report
- [x] W5.1-B ปิด bounded furniture renderer
  - [x] เพิ่ม reception/desk/chair asset manifest และ source dimensions
  - [x] สร้าง object draw commands ที่มี asset/status/transform metadata
  - [x] คง `imgBihin_` selector/crop และ full room placement เป็น open semantics
- [x] W5.1-C ปิด adapter transform/depth fixture
  - [x] รวม furniture + actor เป็น deterministic mixed `draw_order`
  - [x] ใช้ object `sort_key` และ actor `position[1]` ตาม adapter policy
  - [x] คง universal legacy depth/transform semantics เป็น open
- [x] W5.1-D ปิด logical timer contract
  - [x] ระบุ `logical_tick` และ expiry comparison ใน runtime/manifest
  - [x] เพิ่ม zero-lifetime expiry regression และ cleanup assertions
  - [x] คง legacy timer unit เป็น `unknown`
- [x] W5.1-E เพิ่ม explicit adapter animation profiles
  - [x] เพิ่ม static/idle/walk/talk profile schema และ deterministic frame selection
  - [x] ติดสถานะ adapter-defined และคง semantic animation verified เป็น `false`
- [x] W5.1-F จัดประเภท `TFace=40/41`
  - [x] บันทึกเป็น `index_space_gap` และ preserve raw selector
  - [x] ยืนยัน runtime omit face layer โดยไม่ substitute asset
- [x] W5.1-G เพิ่ม raw numeric-event bridge
  - [x] เก็บ raw mode/args/source tag ใน event log แบบ opaque
  - [x] คง named web events และไม่ตั้งชื่อ legacy event mode
- [x] W5.2 ปิด furniture image-slot mapping contract
  - [x] ยืนยัน `.png.bytes` suffix และ extracted `.png` equivalent
  - [x] แยก `imgBihin_[1]` chair, `imgBihin_[2]` desk และ `imgFloorParts` reception
  - [x] เชื่อม office resource indices 10/55/121 กับ source assets จริง
  - [x] ระบุ destination/crop fields และคง numeric selector/crop/placement เป็น open
- [x] W5.3 decode numeric selectors และไล่ crop/room placement ที่มีหลักฐาน
  - [x] decode `DDBody=0`, `DDChair=25`, `DDDesk=26`, `DDPC=77` จาก packed cctor stores
  - [x] ยืนยัน `IndexImgFloorParts=-1` ตอนเริ่ม และ runtime update ผ่าน `EventGChange(param_3)`
  - [x] decode `DeskImgData`/`ChairImgData` 3×14 int records จาก `global-metadata.dat`
  - [x] ปิด bounded crop formulas และ `DrawObj → DrawChair/Desk/Reception` argument flow
  - [x] ปิด bounded numeric `CallHikkosi` placement branches และ `AddObjec` field map
- [x] W5.4 trace IMG_LIST → loader bridge
  - [x] ยืนยัน `AppData.GetImage`: name match จาก `resGame_.list_` แล้วคืน `resGame_.img[index]`
  - [x] ยืนยัน `LoadBihinImage`: `IMG_LIST[DDPC/DDChair/DDDesk] + .png.bytes` ไปยัง `imgBihin_[0/1/2]`
  - [x] แยก recovered literal namespace ออกจาก `game/img.inf` manifest index candidates
  - [x] บันทึก `stringliteral.json` กับ APK `global-metadata.dat` เป็น conflicting extraction sources
  - [x] ปิด `IMG_LIST` selector-to-furniture filename namespace join สำหรับ DDPC/DDChair/DDDesk ผ่าน W5.5
- [x] W5.5 align ScriptString/global-metadata และปิด bihin filename join
  - [x] แก้ one-based `StringLiteral_N` กับ zero-based `script.json`/`stringliteral.json` index
  - [x] ยืนยัน `StringLiteral_833=.png` และ `StringLiteral_7514=face_`
  - [x] align native literal values กับ APK `global-metadata.dat` แบบ exact value ครบ 80/80
  - [x] ปิด `DDChair=25→chair0_origin.png/index29`, `DDDesk=26→desk0_origin.png/index30`, `DDPC=77→pc.png/index117`
  - [x] trace `IndexImgFloorParts` mode-1 branch และ initial `DDFloor+3=42→floorparts0.png/index79`
  - [x] ถอด SEB loader framing, `RECT` optional tail marker และ `office/floor0.seb` partial record
- [x] W5.7 trace SEB consumer และ bounded local placement
  - [x] ยืนยัน `SP_*` constants กับ sprite-object offsets จาก `dump.cs`/`ConvBufferToSprite`
  - [x] ปิด SEB `DrawImage` crop `(U,V,W,H)` และ destination `base + (TRANS_X,TRANS_Y)`
  - [x] ปิด bounded `GetBRectSeb` external base addition และ anchor `SetOffset → draw → ClearOffset` lifecycle
  - [ ] ปิด full room/world placement, pivot/anchor enum, depth/transform semantics โดยไม่สังเคราะห์ tail bytes
- [x] W5.8 trace room caller และ screen placement boundary
  - [x] ยืนยัน `RenderGameScreen → SetOrigin → DrawObj → reset origin` พร้อม clip boundary
  - [x] ปิด bounded PNG room path: `ObjecX/Y + ObjecZX/ZY`, crop `ObjecCX/CY/WX/WY` และ `imgFloorParts`
  - [x] ยืนยัน scoped `DrawObj` ไม่มี `ResourceManager.DrawSeb` และแยก SEB UI callers ออกจาก room PNG path
- [x] W5.9 trace object producers และ camera/SEB mapping boundary
  - [x] ปิด `AddObjec` parameter → `Objec*` field provenance และ default `ObjecZX/ZY=0`
  - [x] ยืนยัน `MainProcess` มี `ObjecX/Y` averaging update จาก `GameForm+0xE40/+0xF50/+0xF58` โดยยังไม่ตั้งชื่อ source semantics
  - [x] inventory `CallPCChange`/`CallDeskChange`/`CallChairChange` field-update producers และไม่พบ `ObjecZX/ZY` write ใน scoped producer scan
  - [x] ยืนยัน `OnTouchCamera`/`SetOrigin` recovered C เป็น no-op และ `RenderGameScreen` เป็นเพียง screen-origin boundary
  - [x] scan ไม่พบ direct `floor0.seb` → `GameForm.DrawObj` caller ใน recovered C
  - [ ] ปิด source-array semantics, camera/world/isometric transform, nonzero `ObjecZX/ZY`, depth/pivot semantics และ full SEB room mapping

## Next — Wave 4 dialogue, bubble และ lifecycle bridge

แผน execution อยู่ที่ `Phases/Phase4/docs/wave4_plan.md`; W4-C0–C7 และ W4.5 evidence
hardening เสร็จแบบ bounded `complete_with_known_limitations` แล้ว โดย timer/token/graph/mode
semantic boundaries ยังคงเปิดอย่างมี status/next action

- [x] W4-C0 freeze baseline และสร้าง controlled gap register
  - [x] สร้าง `wave4_build_manifest.json` จาก source/artifact hashes
  - [x] ยืนยัน source roots แบบ read-only และ `legacy_equivalence=false`
- [x] W4-C1 สร้าง locale/language contract
  - [x] audit CSV 12 locale, duplicate ID, BOM และ strict UTF-8
  - [x] สร้าง placeholder/fallback fixture โดยไม่อ้าง English extraction
- [x] W4-C2 สร้าง talk index/speaker contract
  - [x] trace `GetTalkIndex`, `GetTalkTexts`, `AddKaiwaTalkData`, `GetHumanTalkName`, `AddKaiwa`
  - [x] แยก talk tag/index/language ID/raw speaker ID/actor ID namespaces
  - [x] สร้าง neutral talk fixture โดยไม่ invent production talk tag
- [x] W4-C3 สร้าง fukidashi/bubble contract
  - [x] trace `AddFuki`, `CallFuki`, `DrawFukidashi` และ `HumanFuki*` fields
  - [x] สร้าง deterministic attach/draw/expire fixture ด้วย adapter clock
  - [x] trace `MainProcess` decrement และ `DrawObj` positive-timer draw gate
  - [x] สร้าง W4.5 timer/fuki trace: update repeat `1/2/16`, decrement และ draw gate
  - [ ] ปิด legacy timer unit และ zero-time index cleanup ถ้า Phase 5 ต้องใช้ fidelity
- [ ] W4-C4 ทำ event/lifecycle bridge
  - [x] inventory `AddEvent` producer 53 callsites และ raw mode expressions
  - [x] เก็บ structural `DoEvent` assembly metadata โดยไม่แปลทั้งฟังก์ชัน
  - [x] slice bounded `MainProcess`/`DrawObj` calls และ `DoEvent` targets ที่แตะ `AddKaiwa`/`AddMessage`
  - [ ] ตั้งชื่อ semantic event modes หรือ actor lifecycle เฉพาะเมื่อมี dependency ที่ปิดได้
- [x] W4-C5 สร้าง actor dialogue composition fixture
  - [x] ทำ trace `spawn → dialogue request → talk lookup → bubble attach → draw → expire`
  - [x] คง `talking` เป็น adapter-only และ `legacy_equivalence=false`
- [x] W4-C6 สร้าง AddMessage notification contract/fixture
  - [x] ยืนยัน `MessageText`, `MessageTime`, `MessageMaxTime`, `MessageGraph` bounded writes
  - [x] คง raw lifetime `0x60` และ graph ID semantics เป็น unknown
  - [x] trace notification decrement, expiry compaction และ `MessageMaxTime` sound threshold
  - [x] trace MessageGraph `1/2` render path และ SoundPlay threshold
  - [ ] ปิด timer unit, graph label และ audio policy semantics ถ้ามี product dependency
- [x] W4-C7 closure และ handoff แบบมี known limitations
  - [x] สร้าง `wave4_closure_report.md`, lifecycle slices และ C7 manifest
  - [x] รัน final Wave 4/Phase 4/Phase 2 regression และตรวจ source hash/`git diff --check`
- [x] W4.5 evidence hardening ก่อน Wave 5
  - [x] R1 timer/HumanFuki trace และ explicit cleanup boundary
  - [x] R2 talk split/replace/parse/name pipeline และ speaker caller search
  - [x] R3 MessageGraph render behavior และ audio threshold
  - [x] R4 DoEvent target clusters/nearby constants โดยไม่ promote numeric modes
  - [x] สร้าง hardening manifest/report/tests และรัน Phase 4 รวม `107/107`
  - [ ] ใช้ Wave 5 adapter boundary; reopen เฉพาะเมื่อมี concrete timing/token/graph/event dependency

## Next — Wave 2 office scene truth

### Wave 2 foundation and contracts

- [x] W2-C0 freeze baseline และยืนยัน source roots แบบ read-only
  - [x] Wave 1 baseline source hashes ตรงกับ Wave 2 build manifest
  - [x] Wave 0 + Wave 1 regression ผ่าน และเพิ่ม Wave 2 regression
- [x] W2-C1 สร้าง symbolic selector adapter
  - [x] แยก selector/resource/img-array/filename namespaces
  - [x] คง static selectors เป็น symbolic เพราะ numeric values ยัง decode ไม่ได้
  - [x] คง `StringLiteral_7514` conflict และ `TFace=40/41` index-space gap
- [x] W2-C2 สร้าง office object contract
  - [x] map `AddObjec` arguments ไปยัง `Objec*` fields จาก `dump.cs`
  - [x] บันทึก object-type constants และ bounded function spans
- [x] W2-C3 เริ่ม room/SEB asset contract
  - [x] สร้าง verified asset fixture ของ `office/floor0.png` + `office/floor0.seb`
  - [x] คง SEB tail shortfall 4 bytes และ placement เป็น `not_yet_resolved`
- [ ] W2-C4 ปิด coordinate contract
  - [x] สร้าง coordinate-space evidence index และ centered-origin arithmetic fixture
  - [x] Trace observed object anchor/crop formula สำหรับ human/reception callsites
  - [ ] ปิด world/object/crop/screen transform ที่เป็น universal semantics
- [ ] W2-C5 ปิด draw order/depth contract
  - [x] สร้าง verified object dispatch index และ compare-and-swap evidence
  - [x] สร้าง neutral multi-object draw-order fixture
  - [ ] Resolve depth semantics จาก assembly/pixel behavior
- [ ] W2-C6 ปิด furniture/seat/placement contract
  - [x] Trace `CallPCChange`, `CallDeskChange`, `CallChairChange`, image accessors และ `DeskZahyou`
  - [x] ทำ bounded `CallHikkosi` placement trace และ fixture
  - [x] จัด boundary เป็น explicit Wave 3 adapter interface โดยไม่อ้าง legacy equivalence
  - [ ] ปิด legacy seat/collision/walkable producer semantics
- [ ] W2-C7 สร้าง end-to-end room fixture และ Wave 2 closure report
  - [x] สร้าง minimum room/object/coordinate/draw fixture โดยแยก symbolic placement จาก dispatch probe
  - [x] สร้าง `wave2_wave3_movement_interface.json`
  - [ ] สร้าง final room/pixel regression และ closure report

## Planned — Wave 3 actor truth

แผน execution อยู่ที่ `Phases/Phase4/docs/wave3_plan.md`; W3-C0 ถึง W3-C6
มี contract/fixture ที่สร้างซ้ำและทดสอบได้แล้ว โดย semantic legacy gaps ยังเปิดตามที่ระบุใน artifacts

- [x] W3-C0 freeze baseline และสร้าง actor evidence register
  - [x] สร้าง `wave3_build_manifest.json`, `wave3_gap_register.json` และ actor function map
  - [x] ทำ bounded slices ของ `CallSyain`, `NextTarget`, `MainProcess`, `DoEvent`
  - [x] ยืนยัน raw/export address namespace และ source roots แบบ read-only
  - [x] เพิ่ม `test_wave3_actor_contract.py` และรัน Phase 4 regression ผ่าน 42/42
- [x] W3-C1 สร้าง actor identity/spawn contract
  - [x] trace `AddSyain` → employee fields และ `CallSyain` → `Human*` fields
  - [x] สร้าง spawn fixture ที่มี stable adapter actor/employee/object references โดยไม่เปิดเผย legacy array index
- [x] W3-C2 สร้าง actor state/mode/timer contract ในระดับ raw audit/neutral fixture
  - [x] trace `HumanMode`, `HumanState`, `HumanAnime`, `HumanTime`, stop/wait/reaction fields
  - [x] คง Phase 2 mapping เป็น verified raw seed, adapter decision และ probable 8/9 โดยไม่ promote เป็น legacy semantic
  - [x] เพิ่ม bounded `MainProcess` tick slices: wait decrement, raw reset, mode/state branch และ anime counter
  - [ ] ปิด MainProcess/DoEvent state transition, timer units และ semantic mapping
- [x] W3-C3 สร้าง target/movement contract ในระดับ raw flow + adapter fixture
  - [x] แยก target arrays, actor position arrays และ adapter/graphics position spaces พร้อมระบุ role ที่ยังเปิด
  - [x] สร้าง adapter-only path/collision movement fixture พร้อม blocked/no-path/unavailable cases
  - [ ] ปิด legacy current/previous position, walkable และ collision semantics
- [ ] W3-C4 สร้าง furniture/seat/interaction contract
  - [x] trace `HumanSitChair`, `DeskSyain`, `ChairMainObjec`, `ChairSubObjec`, `PCObjec`, `DeskObjec`, `DeskZahyou` ใน bounded source/fixture scope
  - [x] ทำ explicit `occupy/release/query` contract และ fixture โดยไม่ derive จาก sprite
  - [x] ตรวจ bounded producer scope และตัดสินใจคง `not_closed`/adapter-only พร้อม handoff rule
- [x] W3-C5 สร้าง animation selector/draw contract ในระดับ evidence/contract/fixture
  - [x] trace bounded actor selector flows และ `DrawHuman(TFace, TBody, TMode)` composition contract
  - [x] สร้าง deterministic draw fixture สำหรับ selector/crop/offset/destination
  - [x] คง timing/loop/direction/mirroring เป็น unknown หากยังไม่มี evidence
  - [ ] ปิด semantic state/mode mapping และ resolve `TFace=40/41` asset namespace
- [x] W3-C6 สร้าง single-actor end-to-end fixture ในระดับ adapter boundary
  - [x] ทดสอบ deterministic `spawn → move → arrive → draw` golden trace
  - [x] เพิ่ม blocked target, occupied seat, seat release/reacquire และ unknown animation scenarios
  - [x] บันทึกว่า legacy state/movement/occupancy equivalence ยังเปิดและมี owner/next action
- [x] W3-C7 สร้าง closure report และ handoff ไป Wave 4/Phase 5 แบบมี known limitations
  - [x] รัน builder checks C0–C7, Phase4 regression 88/88 และ Phase2 regression 5/5
  - [x] ตรวจ gap register, roadmap และอัปเดต `PROJECT_STATE.md` พร้อม handoff rules

## Completed — Wave 1 resource truth

### Wave 1 closure pass

- [x] W1-C0 freeze baseline และสร้าง `wave1_gap_register.json` ตั้งต้น
  - [x] ตรึง artifact/source hashes และยืนยัน source roots แบบ read-only
  - [x] ยืนยัน address namespace: assembly export → raw `script.json`/ELF ด้วย delta `-0x100000`
  - [x] จัดประเภท gap ตั้งต้น 8 รายการโดยไม่มี unclassified unknown
- [x] W1-C1 trace ค่า `DDBody`, `DDPC`, `DDChair`, `DDDesk` ถึง provenance ของ static initializer/field writes
  - [x] ยืนยัน cctor write sites และ GOT/relocation provenance ของ DDBody, DDChair, DDDesk, DDFace, DDPC
  - [ ] Decode numeric selector values จาก runtime data/metadata และตรวจ IMG_LIST bounds
- [x] W1-C2 ตรวจ `StringLiteral_7514` กับ assembly/pointer และจัดประเภท `imgFace` conflict
  - [x] raw BootForm loop ยืนยันการโหลด `StringLiteral_7514` และ suffix `StringLiteral_833`
  - [x] จัดเป็น `conflicting_evidence`; ไม่แทนค่าเป็น `face_` จากการคาดเดา
- [x] W1-C3 audit asset/index spaces รวม `TFace=40/41` และไฟล์ที่ไม่ match manifest
  - [x] ตรวจ manifest 291 records: ทุก record มีไฟล์จริงใน audited roots
  - [x] แก้ canonical basename join กรณี `floorCover`/`floorCover.png`
  - [x] จัดประเภท unmatched IMG_LIST 15 รายการ และ `TFace=40/41` เป็น index-space gap
  - [x] Trace callers/branches แบบ bounded แล้ว; พบแต่ direct literal preview/screen/panel callsites และยังไม่ยืนยัน alternate namespace
  - [x] สร้าง `wave1_selector_resolution.json` พร้อมสถานะ dynamic value/preconditions; numeric literal ยังไม่เดา
- [x] W1-C4 เลือก bounded assembly slice แรกของ `NewGamePara` และ `DoEvent`
  - [x] สร้าง `wave1_slices.json` และ neutral pseudocode docs ที่มี block/call/exit boundaries
- [x] W1-C5 สร้าง gap register/closure report โดยไม่มี final `unknown` ที่ไร้เหตุผล
- [x] W1-C6 รัน regression และผ่าน Wave 2 gate แบบ `ready_for_wave2_with_known_limitations`

- [ ] Trace initializer/loader ของ `imgBody[]` และ `imgFace[]`
  - แหล่งหลัก: `game-dev-story-mod_Dumped/Categorized_Code/`, `dump.cs`, `script.json`
  - [x] บันทึก `ResourceManager`/`AppData.GetImage`/`JarInflater` contract จาก recovered C
  - [x] บันทึก destination/count ของ `imgFace` และ `imgBody` พร้อม source reference
  - [x] สร้าง fixture อย่างน้อยหนึ่งรายการต่อ family ที่มีไฟล์จริง
  - [ ] Resolve ค่า static base selectors และปิด trace เป็น selector-to-file mapping
- [ ] Resolve resource index-to-file mapping
  - ผูก selector (`TFace`, `TBody`, `TMode`) กับ resource index และไฟล์จริงใน `game-dev-story-mod_Sprites/`
  - [x] สร้าง manifest mapping สำหรับ `game/img.inf`, `office/img.inf`, `load/img.inf`, `office/seb.inf`
  - [x] เก็บกรณีชื่อไม่ match และ literal conflict เป็น `unknown`
  - [ ] ปิด mapping ของ `TFace`/`TBody` เมื่อค่า base selector มีหลักฐานตรง
- [ ] ทำ branch index สำหรับ `NewGamePara` และ `DoEvent`
  - ใช้ assembly fallback เป็นหลักฐานตั้งต้นก่อนเริ่ม lifecycle slice
  - [x] สร้าง structural instruction/branch/call/basic-block index ของทั้งสองฟังก์ชัน
  - [x] จัดกลุ่ม bounded branch/call/field context ของ guard, AddObjec, AddKaiwa และ EventMode dispatch พร้อม confidence/status
  - [ ] ปิด full lifecycle และตั้งชื่อ numeric mode เมื่อมีหลักฐานเพิ่ม

## Next — ปิด unknown ที่ block Phase 1/2

- [ ] Trace office placement, seat, collision, walkable/zone และ grid/depth contract
- [ ] Trace DrawObj/Syain/Kaiwa และ dynamic selector paths ที่ยังไม่ครบ
- [ ] Resolve literal selectors `TFace=40` และ `TFace=41` ที่ยังไม่มี extracted face asset หรือบันทึกเป็น out-of-scope พร้อมหลักฐาน
- [ ] อัปเดต Phase 1/2 manifests และ reports เมื่อมี evidence ใหม่

## Supporting — Phase 3 language layer (consumed by P0-B3)

- [ ] สร้าง/ยืนยัน generated locale lookup จาก CSV โดยคง language ID และ placeholder เดิม
- [ ] ทำ `getString(id, args, locale)` พร้อม fallbackใน TypeScript `LocaleStore`
- [ ] สร้าง/ยืนยัน QA report สำหรับ duplicate ID, missing ID, encoding และ placeholder mismatch

## Deferred — post-port runtime foundation

- [x] สร้าง selective translation contracts สำหรับ renderer, actor state, movement และ dialogueใน Phase 4/5 artifacts
- [x] สร้าง Phase 5 minimal web office runtime โดยยังไม่เชื่อม model (`complete_with_known_limitations`)
- [x] สร้าง Phase 6 task queue, assignment, notification และ activity log (`complete_with_known_limitations`)
- [ ] เชื่อม Phase 7 AI model หลัง visual runtime และ task system ผ่านเกณฑ์

## Completed reference

- [x] Phase 0 baseline และ checksum
- [x] Phase 1 inventory, legacy map, SEB structure, renderer evidence และ preview
- [x] Phase 2 character/body-face catalog, manifests, previews และ validation
- [x] Phase 4 Wave 0 translation index, coverage artifacts และ smoke tests 6/6

## Update rules

- เมื่อทำงานย่อยเสร็จ ให้ติ๊ก `[x]` พร้อมอัปเดต `PROJECT_STATE.md` ถ้าสถานะหรือ blocker เปลี่ยน
- ถ้าเป็นงานที่ทำได้บางส่วน ให้คง `[ ]` ไว้และแยกงานย่อยที่เสร็จแล้วเป็น checkbox ใต้รายการนั้น
- สิ่งที่ยังไม่มีหลักฐานให้ระบุเป็น `unknown` หรือ `out-of-scope` ห้ามติ๊กเสร็จจากการคาดเดา
