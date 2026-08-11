# AI Agent Office Roadmap

เอกสารนี้กำหนดแผนเปลี่ยนข้อมูลที่แกะจาก Game Dev Story ให้เป็นหน้า Virtual AI Office สำหรับเว็บ dashboard โดยคงฉาก ตัวละคร asset และ animation เดิมไว้ให้มากที่สุด และตัดระบบ gameplay ที่ไม่จำเป็นออก

## เป้าหมายหลัก

สร้างเว็บที่ผู้ใช้มองเห็นออฟฟิศแบบเดิม มีตัวละครเดิม และตัวละครสามารถแสดงสถานะการทำงาน เดิน นั่ง พัก คุย และตอบสนองต่อ task ได้เหมือนพนักงาน AI

ช่วงแรกยังไม่ใส่ model หรือ Cloudflare AI จนกว่า visual runtime และ state ของตัวละครจะทำงานถูกต้อง

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

สถานะ: รอ Phase 1

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

### Phase 4 — Code study และ logic classification

สถานะ: รอ asset และ animation catalog

ไม่ต้องศึกษา C ทั้งหมด ให้จัดกลุ่ม function ใน `Categorized_Code/` เป็น 3 ประเภท

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

เกณฑ์ผ่าน:

- ทุก feature ที่จะ port มี source function และเหตุผลรองรับ
- ไม่มีการ port gameplay ที่ไม่จำเป็นเข้ามาปนกับ office runtime

### Phase 5 — Minimal web office runtime

สถานะ: ยังไม่เริ่ม

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

สถานะ: หลัง visual runtime

ต้องเพิ่ม:

- สร้าง task
- assign task ให้ Agent
- task queue และ priority
- สถานะ `queued`, `working`, `blocked`, `done`
- notification และ activity log
- agent detail panel
- office filter หรือ focus camera

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

## งานถัดไปที่ควรเริ่มทันที

1. สร้าง asset inventory จาก `game-dev-story-mod_Sprites/`
2. ทำ preview ของ `office/` และ `game/`
3. ตรวจ body-face และสร้าง character catalog
4. สร้าง language JSON จาก CSV พร้อม placeholder validation
5. คัด function ที่เกี่ยวกับ renderer, character state และ chat bubble
