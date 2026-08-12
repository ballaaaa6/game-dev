# AI Agent Office Roadmap

เอกสารนี้กำหนดแผนเปลี่ยนข้อมูลที่แกะจาก Game Dev Story ให้เป็นหน้า Virtual AI Office สำหรับเว็บ dashboard โดยคงฉาก ตัวละคร asset และ animation เดิมไว้ให้มากที่สุด และตัดระบบ gameplay ที่ไม่จำเป็นออก

## เป้าหมายหลัก

สร้างเว็บที่ผู้ใช้มองเห็นออฟฟิศแบบเดิม มีตัวละครเดิม และตัวละครสามารถแสดงสถานะการทำงาน เดิน นั่ง พัก คุย และตอบสนองต่อ task ได้เหมือนพนักงาน AI

ช่วงแรกยังไม่ใส่ model หรือ Cloudflare AI จนกว่า visual runtime และ state ของตัวละครจะทำงานถูกต้อง

## สรุปความคืบหน้าแบบ checklist

อัปเดตล่าสุด: 2026-08-12

ใช้ checkbox ระดับงานย่อยเพื่อแยกงานที่เสร็จแล้วออกจากงานที่ยังค้างอยู่ งานระดับ Phase ที่มีทั้งส่วนเสร็จและส่วนค้างให้คงเครื่องหมาย `[ ]` ไว้จนกว่างานสำคัญของ Phase นั้นจะผ่านเกณฑ์ครบ

### Foundation และ evidence

- [x] Phase 0 — freeze baseline และ checksum
- [ ] **P0-A — Corpus Intelligence Pipeline (urgent gate ก่อนเก็บ Phase อื่นต่อ)**
  - [ ] freeze source/artifact hashes และสร้าง baseline manifest
  - [ ] import Phase 4/5/6 evidence โดยคง historical artifacts แบบ read-only
  - [ ] สร้าง full-corpus function/field/string/resource/call/data-flow index
  - [ ] สร้าง lossless annotated/normalized/prompt views พร้อม source maps
  - [ ] เปรียบเทียบ Ghidra/Il2CppDumper กับ Cpp2IL เมื่อมี tool และคง conflict เป็น evidence
  - [ ] รัน pilot 100 functions, candidate logic maps, validator และ negative-evidence ledger
  - [ ] ปิด corpus closure gate ก่อนส่งต่อไป P0-B และงาน Phase อื่น
- [ ] Phase 1 — asset inventory และ visual map (inventory เสร็จแล้ว แต่ placement/grid/seat/depth semantics ยังไม่ปิด)
  - [x] asset catalog, legacy map และ input audit
  - [x] SEB structure และ renderer evidence
  - [x] office preview/contact sheet
  - [ ] ยืนยัน anchor/baseline/pivot และ coordinate placement
  - [ ] ยืนยัน collision/seat/walkable/zone และ grid/depth contract
- [ ] Phase 2 — character และ animation catalog (catalog เสร็จแล้ว แต่ semantic state ยังไม่ครบ)
  - [x] body/face audit, manifests และ character previews
  - [x] `DrawHuman` composition contract (`imgBody[TBody]` + `imgFace[TFace]`)
  - [x] HumanDex dynamic path อย่างน้อยหนึ่งเส้นทาง
  - [ ] resource index-to-file mapping ครบทุก asset family
  - [ ] ยืนยันความหมายของ idle/walking/working/sitting/break/talking
- [ ] Phase 3 — language extraction และ translation layer
  - [x] ตรวจ BOM/UTF-8 ของ CSV ปัจจุบัน
  - [ ] สร้าง locale JSON/runtime lookup
  - [ ] ตรวจ duplicate/missing ID และ placeholder mismatch
- [ ] Phase 4 — selective code translation และ logic classification
  - [x] Wave 0 translation index, field/function inventory และ coverage
  - [x] Wave 0 call graph/string-literal index และ smoke tests 6/6
  - [x] Wave 1 initializer/loader trace และ selector-to-resource-to-file mapping (closed with known limitations)
  - [ ] Wave 2 office scene/depth contracts (minimum contract/interface gate ready; scene semantic closure pending)
  - [ ] Wave 3 actor movement/state contracts (W3-C0–C7 contract/fixture/closure เสร็จแบบมี known limitations; C2 semantic mapping, legacy occupancy และ C5 semantic animation ยังเปิด ตามแผน `Phases/Phase4/docs/wave3_plan.md`)
  - [ ] Wave 4 dialogue/text/bubble/lifecycle bridge (W4-C0–C7 + W4.5 evidence hardening เสร็จแบบ known limitations; timer/cleanup/token/graph/mode semantics ยังเปิด ตามแผน `Phases/Phase4/docs/wave4_plan.md` และ `Phases/Phase4/docs/wave4_hardening_report.md`)
  - [x] Wave 5–6 runtime bridge และ closure sweep (`complete_with_known_limitations`; Wave 6 task/dashboard layer และ W6.1 persistence hardening ปิดแล้ว)
  - [ ] **P0-B — Office Runtime TypeScript Port**: เริ่มหลัง P0-A corpus closure แล้วเปลี่ยน evidence/contract ที่ปิดแล้วให้เป็น executable TypeScript และ test ก่อนเริ่ม Phase 7

### Runtime และ product

- [x] Phase 5 — minimal web office runtime (`complete_with_known_limitations`)
  - [x] room manifest, source-root asset loading และ explicit adapter providers
  - [x] deterministic Agent state, logical tick, event log และ lifecycle cleanup
  - [x] movement, seat conflict/release, body/face draw command และ unresolved selector policy
  - [x] locale runtime 12 ภาษา, dialogue/bubble และ raw notification graph IDs
  - [x] bounded furniture renderer, mixed draw-order policy, logical timer, adapter animation profiles และ raw event bridge (W5.1-B–G)
  - [x] furniture image-slot mapping contract แยก `imgBihin_`/`imgFloorParts` พร้อม crop/placement gap statuses (W5.2)
  - [ ] legacy furniture selector/crop/placement mapping และ targeted semantic traces เมื่อมีหลักฐาน/feature dependency
- [x] Phase 6 — task system และ dashboard interaction (`complete_with_known_limitations`)
  - [x] task schema, priority queue และ lifecycle contract
  - [x] explicit assignment และ one-active-task-per-agent rule
  - [x] durable task notification และ activity log
  - [x] Agent projection, repository-backed local persistence, migration/conflict handling และ reset/export
  - [x] explicit local permission policy และ JSON import/reload controls
  - [x] dashboard interaction, filters และ Agent focus highlight
  - [x] Wave 6 unit/contract tests และ browser smoke
- [ ] Phase 7 — เชื่อม AI model หลัง visual/task runtime เสถียร

งานย่อยที่พร้อมเริ่มและเกณฑ์เสร็จอยู่ใน `TODO.md` ที่ workspace root ส่วนรายละเอียด handoff และ known limitations อยู่ใน `PROJECT_STATE.md`

## Data-first policy

ข้อมูล extraction ล่าสุดเป็น source of truth หลัก ส่วน Markdown ที่อยู่ใน
`Docs/` เป็นเพียง reference และอาจมาจากการวิเคราะห์ข้อมูลชุดเก่า/ไม่ครบ

ถ้าเอกสารขัดกับ asset, extraction report, `script.json`, `dump.cs`,
`bodyface_records.reference.json` หรือ C/assembly output ให้ยึดข้อมูลเหล่านั้น
แล้วแก้เอกสารทับทันที ห้ามนำข้อสรุปจากเอกสารเก่ามาเติมช่องว่างด้วยการเดา

## แหล่งข้อมูลหลัก

ใช้ข้อมูลจากโฟลเดอร์ชุดใหม่ที่รากโปรเจกต์เท่านั้น

- `game-dev-story-mod_Sprites/` — ฉาก ตัวละคร เฟอร์นิเจอร์ UI animation และ language tables
- `game-dev-story-mod_Dumped/` — IL2CPP dump, Ghidra output, recovered C และ assembly fallback
- `game-dev-story-mod_Extracted/` — ข้อมูล APK ดิบสำหรับตรวจสอบย้อนกลับ
- `Phases/Phase2/docs/CHARACTER_PRODUCTION_MANUAL.md` — current body/face records และ asset evidence
- `Phases/Phase1/docs/kairosoft_grid_system.md` — รายการ trace grid/coordinate/depth ที่ยังต้องพิสูจน์
- `Phases/Phase3/docs/kairosoft_language_system.md` — current language tables และ language entry points

`APK_Toolkit/` ใช้สำหรับเครื่องมือและการสร้างข้อมูลใหม่ ไม่ใช่แหล่งข้อมูล runtime หลัก

## Current extraction baseline

ตัวเลขต่อไปนี้มาจากชุดข้อมูลปัจจุบัน ไม่ได้มาจาก Markdown รุ่นเก่า:

- code report: 110,824 functions; C success 110,819; recovery เพิ่ม 1 function
- remaining C failures: 4 functions; มี assembly fallback จาก failed list ครบ 5 รายการ
- asset output: 445 files; PNG 347; CSV 12; extraction errors 0
- language tables: 12 locale files ใน `game-dev-story-mod_Sprites/language/`
- character records: 42 `bodyface` modes ใน `bodyface_records.reference.json`
- current character assets: body 26 files และ face 36 files ใน `game/`

ตัวเลขนี้ใช้เป็น baseline สำหรับการตรวจครั้งต่อไป ถ้าเอกสารเดิมขัดกับ baseline
ให้แก้เอกสาร ไม่ใช่แก้ baseline ด้วยการเดา

## หลักการทำงาน

1. ใช้ asset และข้อมูลที่ตรวจสอบได้จากชุด extraction ปัจจุบัน
2. ไม่เดาความหมายของ animation หรือ function ถ้ายังไม่มีหลักฐานจาก asset, ID หรือ code reference
3. ไม่แปลหรือ port code ทั้งหมด แต่เลือกเฉพาะ logic ที่เกี่ยวกับ office runtime
4. แยกข้อมูลต้นฉบับออกจาก adapter ของเว็บ
5. ทุกขั้นต้องมี manifest, report หรือ test ที่ตรวจสอบย้อนกลับได้
6. คง ID และ placeholder เดิม เช่น `#00000`, `<0>`, `<1>`

## Roadmap

### Phase 0 — Freeze และตรวจ baseline

สถานะ: เสร็จแบบมี known limitations

สิ่งที่ต้องทำ:

- ยืนยันว่า root output เป็นชุดข้อมูลหลักเพียงชุดเดียว
- ตรวจ `extraction_report.json`, `Exported_ALL.report.json` และ recovery reports
- เก็บ hash หรือ manifest ของข้อมูลก่อนเริ่มแปลง
- ห้ามแก้ไฟล์ต้นฉบับโดยตรงระหว่างการวิเคราะห์

ผลลัพธ์:

- `Phases/Phase0/artifacts/asset_manifest.json`
- `Phases/Phase0/artifacts/language_manifest.json`
- `Phases/Phase0/artifacts/code_coverage_manifest.json`
- `Phases/Phase0/artifacts/phase0_baseline.json`
- `Phases/Phase0/artifacts/phase0_checksums.sha256`
- `Phases/Phase0/docs/phase0_baseline_report.md`
- extraction baseline ที่ใช้เปรียบเทียบในอนาคต

เกณฑ์ผ่าน:

- รู้จำนวน asset, language table, dump และไฟล์ที่ยังมีข้อจำกัด
- สามารถย้อนกลับไปหา source file ได้ทุก record
- แยก export รอบแรกที่ล้มเหลว 5 ฟังก์ชันออกจากสถานะหลัง recovery ที่เหลือ C ขาด 4 ฟังก์ชัน
- assembly fallback ของ failed-function list มีครบ 5 รายการและสถานะ `ok`

ข้อจำกัดที่บันทึกไว้:

- `extraction_report.json` ยังชี้ output ไปที่ `game-dev-story-mod_Sprites_fixed` ขณะที่ source root ปัจจุบันคือ `game-dev-story-mod_Sprites`
- report เดิมยังเก็บ warning UTF-8 3 รายการ แต่ CSV ปัจจุบันผ่านการตรวจ BOM และ strict UTF-8 แล้ว
- C ที่รวม recovery แล้วมี `110,820 / 110,824`; อีก 4 ฟังก์ชันใช้ assembly fallback ได้ และไม่จำเป็นต้องรัน APK/Ghidra ใหม่เพื่อเริ่มงานต่อ

### Phase 1 — Asset inventory และ visual map

สถานะ: กำลังดำเนินการ — inventory/legacy map/SEB structure/renderer evidence/preview เสร็จในชุดแรกแล้ว; runtime placement และ interaction semantics ยังรอหลักฐานเพิ่ม

พื้นที่ศึกษา:

- `game-dev-story-mod_Sprites/office/`
- `game-dev-story-mod_Sprites/game/`
- `game-dev-story-mod_Sprites/com/`
- `game-dev-story-mod_Sprites/system/`
- ไฟล์ `.png`, `.seb`, `.bin`, `.inf`, `.txt`

ต้องบันทึก:

- asset ID และชื่อไฟล์
- ขนาดภาพและขนาด atlas
- source archive
- anchor, baseline และ pivot ถ้าพบข้อมูลรองรับ
- ชั้นการวาดหน้า/หลัง
- collision, seat, interaction และ zone ถ้าพบข้อมูลรองรับ
- confidence: `verified`, `probable`, `unknown`

ผลลัพธ์:

- รายการฉากและ furniture ที่นำไปใช้ได้
- preview ของ office room
- mapping ระหว่าง asset เดิมกับ ID ที่เว็บจะใช้

เกณฑ์ผ่าน:

- วาดพื้น ผนัง ประตู furniture และของตกแต่งในตำแหน่งที่ตรวจสอบได้
- แยกของที่เป็น visual-only ออกจากของที่มี interaction

ผลการเริ่มงานรอบปัจจุบัน:

- สร้าง `Phases/Phase1/artifacts/phase1_asset_catalog.json`, `phase1_legacy_asset_map.json` และ `phase1_input_audit.json` จาก source root แบบ read-only
- สร้าง `Phases/Phase1/artifacts/phase1_seb_manifest.json` โดยถอดโครงสร้าง legacy record จาก decompiled loader; SEB ที่ extract ปัจจุบัน 53/53 สั้น 4 ไบต์เมื่อเทียบกับ ten-short record expectation จึงไม่เติมข้อมูลและคงสถานะ `truncated_final_record` (ยังไม่สรุปว่าเป็น variant หรือ extraction boundary)
- สร้าง `Phases/Phase1/artifacts/phase1_code_trace.json` และ `office_manifest.json` เพื่อผูก renderer callsite กับ asset โดยแยก `verified`, `probable`, `unknown`
- สร้าง preview จาก PNG จริงที่ `Phases/Phase1/docs/phase1_office_preview.png` และ `phase1_office_floor_contact_sheet.png`
- เกณฑ์ที่ยังไม่ผ่านการยืนยัน: anchor/baseline/pivot, coordinate placement, collision/seat/walkable/zone และ grid/depth contract

### Phase 2 — Character และ animation catalog

สถานะ: `complete_with_known_limitations`; Phase 1 placement/interaction semantics ที่ยังไม่ยืนยันไม่ block catalog นี้

พื้นที่ศึกษา:

- `game-dev-story-mod_Dumped/bodyface_records.reference.json`
- `game-dev-story-mod_Dumped/Categorized_Code/`
- function และ class ที่เกี่ยวกับ `Body`, `Face`, `Animation`, `Move`, `Walk`, `Work`, `Rest`, `Sit` และ `Talk`
- asset ใน `office/` และ `game/`

ต้องสร้าง catalog สำหรับ:

| Agent state | สิ่งที่ต้องผูกเข้าด้วยกัน |
| --- | --- |
| `idle` | frame และ loop ปกติ |
| `walking` | ทิศทาง ความเร็ว และ frame sequence |
| `working` | pose ทำงานและตำแหน่งโต๊ะ |
| `sitting` | pose นั่งและ seat anchor |
| `break` | pose พักหรือ idle แบบพัก |
| `talking` | face, bubble และ timing |

ผลลัพธ์:

- `character_manifest.json`
- `animation_manifest.json`
- character preview ที่แสดงทุกทิศทางและ state ที่ยืนยันได้

ผลการทำงานปัจจุบัน:

- สร้าง Phase 2 input audit, bodyface analysis, character asset catalog, code trace, state mapping, manifests, previews และ validation ใต้ `Phases/Phase2/`
- ยืนยัน rendering contract จาก recovered C: `imgBody[TBody]` + `imgFace[TFace]` โดยใช้ crop/offset จาก `BodyFace[TMode]`; `AddBodyFace` ผูก P0–P13 เข้ากับ fields ของ record
- trace HumanDex dynamic draw path ได้หนึ่งเส้นทาง (`HumanDexFaceG`, `HumanDexBodyG`, `HumanDexAnime` → `DrawHuman`); callsite แบบ variable-driven ที่เหลือต้องศึกษาต่อ
- semantic animation ที่ยืนยันได้: 0; `talking` เป็นเพียง probable candidate สำหรับ mode 8/9 ใน Kaiwa/dialogue draw path
- `idle`, `walking`, `working`, `sitting` และ `break` ยังคง `unknown` ตามหลักฐานปัจจุบัน
- แผนศึกษาต่ออยู่ที่ `Phases/Phase2/docs/phase2_investigation_plan.md`

เกณฑ์ผ่าน:

- ตัวละครเดิมถูก render ได้โดยไม่ต้องสร้าง sprite ใหม่
- animation ที่ยังยืนยันไม่ได้ถูกทำเครื่องหมาย `unknown` ไม่เดาความหมายเอง

### Phase 3 — Language extraction และ translation layer

สถานะ: CSV ถูกทำให้ Excel-compatible แล้ว

แหล่งข้อมูล:

- `game-dev-story-mod_Sprites/language/GameDevStory_*.csv`
- `Phases/Phase3/docs/kairosoft_language_system.md`

ต้องทำ:

- แปลง CSV เป็น JSON สำหรับ runtime
- คง language ID เดิม
- คง placeholder และ format token เดิม
- ทำ locale fallback
- ตรวจ duplicate ID, missing ID และ placeholder mismatch
- แยกข้อความตามกลุ่มที่ใช้จริงใน dashboard

ลำดับข้อความที่ควรแปลหรือปรับใช้ก่อน:

1. chat bubble ทั่วไปของพนักงาน
2. สถานะเริ่มงาน กำลังทำงาน และเสร็จงาน
3. ข้อความพัก เหนื่อย ติดปัญหา และขอความช่วยเหลือ
4. notification ของ task
5. ข้อความอนุมัติหรือรายงานผลลัพธ์

ยังไม่ต้องแปลหรือนำมาใช้ในระยะแรก:

- ยอดขายและงบประมาณเกม
- ranking และ magazine/news gameplay
- research, hiring และ progression แบบเกม

ผลลัพธ์:

- `language.json` หรือไฟล์ locale แยกภาษา
- `getString(id, args, locale)`
- language QA report

เกณฑ์ผ่าน:

- ข้อความไทยเปิดใน Excel และอ่านได้ถูกต้อง
- placeholder เช่น `<0>` และ `<1>` ยังทำงานหลังแปลงเป็น JSON
- ถ้าไม่มีคำแปลให้ fallback โดยไม่แสดงข้อความว่าง

### Phase 4 — Selective code translation และ logic classification

สถานะ: evidence/contract waves 0–4 และ adapter baseline waves 5–6 เสร็จแบบ
`complete_with_known_limitations`; **Office Runtime TypeScript Port** เป็นงานหลักถัดไป
และยังไม่มี TypeScript port implementation ที่ใช้แทน runtime JS ครบทั้งเส้นทาง

ไม่แปล C ทั้งหมด แต่ใช้ Phase 4 artifacts เป็นแผนที่ แล้ว port เฉพาะ office vertical slice
เป็น TypeScript ที่ runtime เรียกใช้ได้จริง โดย JSON/Markdown ทำหน้าที่เป็น evidence,
generated data และ fixture เท่านั้น

#### ใช้ต่อโดยตรง

- renderer, scene และ camera
- grid, coordinate และ depth sorting
- sprite loading
- movement และ animation state
- chat bubble และ text lookup
- interaction กับ furniture หรือ office zone
- time tick และ schedule ที่จำเป็นต่อการแสดงชีวิตของ Agent

#### ต้องแปลงเป็น Agent logic

| Logic เดิม | Logic ใหม่ |
| --- | --- |
| employee working | `agent.status = working` |
| employee resting | `agent.status = break` |
| employee walks to task | task navigation |
| employee asks for boost | approval/request event |
| employee has idea | suggestion event |
| employee talks | chat bubble event |

#### ตัดออกหรือพักไว้

- การพัฒนาเกม
- เงินและยอดขาย
- weekly ranking
- magazine/news simulation
- การซื้อของและ progression
- win/lose condition

ผลลัพธ์:

- `legacy_to_agent_mapping.md`
- รายการ function ที่ใช้จริงใน web runtime
- function trace สำหรับ state สำคัญแต่ละตัว

#### Downstream track — Office Runtime TypeScript Port (P0-B)

รายละเอียด design อยู่ที่ `Docs/superpowers/specs/2026-08-12-office-typescript-port-design.md`
และ implementation plan อยู่ที่ `Docs/superpowers/plans/2026-08-12-office-typescript-port.md`.
งานนี้เริ่มได้หลัง `P0-A Corpus Intelligence Pipeline` ผ่าน closure gate เท่านั้น

ขอบเขตหลัก:

- resource/selector และ room/furniture draw
- actor identity, body/face composition, movement/seat boundary และ draw command
- dialogue, locale lookup, bubble, notification และ raw/named event bridge
- browser entry ที่ใช้ compiled TypeScript แทน Phase 5 runtime JS ทีละ module
- source provenance, status manifest และ regression gate ต่อ port unit

ตัวเลข 40,974 บรรทัดเป็นขอบเขตสำหรับ audit/categorization ของ recovered C ไม่ใช่จำนวนที่ต้องคัดลอกทั้งหมด
เพราะ `MainProcess`, `NextPoint`, `NewGamePara` และ `DoEvent` มี gameplay หรือ assembly-only logic ปนอยู่
เป้าหมายเริ่มต้นคือ TypeScript ประมาณ 6,000–12,000 บรรทัด และ test/fixture ประมาณ 2,000–4,000 บรรทัด
โดยต้องวัดจริงเมื่อแต่ละ module ผ่าน gate

ลำดับงานหลัก:

1. สร้าง TypeScript toolchain และ typed source-reference contract
2. port resource/scene/furniture
3. port actor/movement/seat/draw
4. port dialogue/bubble/notification/event bridge
5. เชื่อม browser entry กับ Phase 5/6 shell
6. สร้าง port manifest และ closure report

เกณฑ์ gate: runtime path ไม่อ่าน recovered C โดยตรง, ทุก module มี source reference และ test,
unknown ยังแสดงเป็น raw/adapter status, Phase 2/4/5/6 regression ผ่าน และ browser smoke ไม่มี
console error/warning ใหม่

เกณฑ์ผ่าน:

- ทุก feature ที่จะ port มี source function และเหตุผลรองรับ
- ไม่มีการ port gameplay ที่ไม่จำเป็นเข้ามาปนกับ office runtime
- มี compiled TypeScript implementation สำหรับทุก feature ใน product scope และมี port status manifest
- Phase 7 AI model ยังไม่เริ่มจนกว่า TypeScript port gate และ Phase 6 task regression จะผ่าน

### Phase 5 — Minimal web office runtime

สถานะ: `complete_with_known_limitations`

เริ่มจากการทำให้เว็บ render ได้ก่อน โดยยังไม่เชื่อม model

ข้อมูลหลักที่ควรมี:

```ts
type Agent = {
  id: string;
  name: string;
  role?: string;
  position: { x: number; y: number };
  state: 'idle' | 'walking' | 'working' | 'sitting' | 'break' | 'talking';
  animationId: string;
  taskId?: string;
  bubbleId?: string;
};

type Office = {
  roomId: string;
  tiles: unknown[];
  furniture: unknown[];
  zones: unknown[];
  agents: Agent[];
};
```

ลำดับ runtime:

1. โหลด room manifest
2. render background และ furniture
3. render character ตาม depth order
4. เปลี่ยน state ของ Agent
5. เล่น animation ตาม state
6. แสดง chat bubble จาก language ID
7. บันทึก task/event log

เกณฑ์ผ่าน:

- เปิดเว็บแล้วเห็น office จริง
- Agent เดิน เปลี่ยน state และแสดงข้อความได้
- refresh แล้ว layout ไม่เพี้ยน
- ไม่มี model ก็สามารถทดสอบ state ได้

### Phase 6 — Task system และ dashboard interaction

สถานะ: `complete_with_known_limitations`

ทำแล้ว:

- สร้าง task
- assign task ให้ Agent
- task queue และ priority
- สถานะ `queued`, `working`, `blocked`, `done`
- notification และ activity log
- agent detail panel
- office filter หรือ focus camera

ข้อจำกัดที่ยังเปิด: local persistence เท่านั้น, ไม่มี auth/multi-user backend,
auto-assignment อยู่ Phase 7 และ focus ยังเป็น adapter highlight ไม่ใช่ legacy camera transform

ระบบนี้เป็น backend ใหม่ได้ ไม่จำเป็นต้องยก gameplay backend เดิมมาทั้งหมด

### Phase 7 — เชื่อม AI model

สถานะ: ทำท้ายสุด

เมื่อ visual และ task system เสถียรแล้วจึงเพิ่ม:

- model adapter ของ Cloudflare
- agent persona และ role prompt
- tool/action ที่ Agent เรียกได้
- memory และ task context
- guardrail และ permission
- log ของ model decision

AI ควรตัดสินใจเรื่อง task, message และ action แต่ไม่ควรควบคุมการวาด sprite โดยตรง

## Definition of Done ระยะต้น

งานระยะต้นถือว่าพร้อมเมื่อ:

- office scene เดิมแสดงผลได้
- ตัวละครเดิมแสดงผลและเล่น animation ที่ยืนยันแล้วได้
- Agent มี state idle/walking/working/break/talking
- task สามารถ assign ให้ Agent ได้
- chat bubble ใช้ language ID และ placeholder ได้
- CSV/JSON ไม่มี encoding error
- ไม่มีการเดา animation หรือ port gameplay ที่ยังไม่จำเป็น

## สิ่งที่ยังไม่ทำในช่วงนี้

- ยังไม่เชื่อม Cloudflare AI
- ยังไม่แปลทุกภาษาและทุกข้อความในเกม
- ยังไม่ port ระบบเศรษฐกิจหรือ progression
- ยังไม่เขียนฉากและตัวละครใหม่
- ยังไม่ลบ source dump หรือ asset ที่ยังไม่ได้จัดประเภท

## งานถัดไปตามลำดับเร่งด่วน

1. **ทำ P0-A Corpus Intelligence Pipeline ก่อน** ตาม `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md` และปิด closure gate
2. หลัง P0-A ผ่าน จึงเริ่ม P0-B Office Runtime TypeScript ตาม `Docs/superpowers/plans/2026-08-12-office-typescript-port.md`
3. ใช้ canonical/promoted evidence เป็น input โดยไม่ให้ runtime เปิด recovered C อ่านเอง
4. ปิด port ตามลำดับ resource/scene → actor/movement/seat → dialogue/event → browser integration
5. รักษา source roots แบบ read-only และคง Phase 7 AI model ไว้หลัง P0-B regression/closure gate
