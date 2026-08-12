# Roadmap 2.0 — C#-First Virtual Game Office

สถานะเอกสาร: ร่าง design ที่สร้างจากแนวทางซึ่งผู้ใช้อนุมัติแล้ว รอ user review ก่อนเริ่ม implementation plan
วันที่: 2026-08-12
ขอบเขต: workspace `D:\antigravity\test open ai`

## 1. คำตัดสินใจหลัก

โปรเจกต์จะเปลี่ยนจากเส้นทางเดิมที่เริ่มจาก recovered C/assembly แล้วค่อย port เป็นแนวทาง
**C#-first clean reconstruction**:

- `knowledge/csharp/primary/` เป็น primary working evidence สำหรับการอ่าน class, method, control flow และ callsite ที่ถูกขยาย
- `Assembly-CSharp/` ถูกผู้ใช้ลบแล้ว จึงไม่ลงทะเบียนกลับ; ใช้ recovered C/assembly และ dump เป็น validator/fallback ที่มีอยู่จริงแทน
- recovered C, assembly export และ field-offset artifacts ยังคงเป็น validator/backstop สำหรับ conflict สำคัญ ไม่ใช่แหล่งที่ต้องไล่อ่านเป็นเส้นทางหลักทุกวัน
- C# decompiler output จะไม่ถูก execute หรือ copy ไปเป็น runtime โดยตรง; จะถูกแปลงเป็น typed contracts, evidence maps และ clean TypeScript behavior
- raw source roots และ historical artifacts เป็น read-only; generated evidence, reports และ runtime artifacts อยู่ใต้ `knowledge/`, `runtime/`, `tools/` และ `docs/`

การ “freeze งานเก่า” หมายถึง mark เป็น historical baseline และไม่ขยาย roadmap เดิมต่อ ไม่ใช่ลบ source, artifact, report หรือผลการวิเคราะห์เดิม เพราะข้อมูลเหล่านั้นยังใช้ตรวจ decompiler conflict และ regression ได้

## 2. เป้าหมายผลิตภัณฑ์

สร้างหน้าเว็บ Virtual Game Office ที่โลกออฟฟิศเดินต่อเองตลอดเวลา มีฉากและตัวละครแบบเกม มี task dashboard สำหรับสั่งงาน Agent และแสดงสถานะการทำงาน โดยตัด gameplay ที่ผู้เล่นต้องเล่นเองออก

### สิ่งที่ต้องเห็นใน phase แรก

- office scene, floor, furniture และ drawing order ที่สอดคล้องกับ asset evidence ปัจจุบัน
- ตัวละครที่มี identity, profile, ตำแหน่ง, target, visual selectors และ live simulation state
- Agent เดินไปจุดทำงานเองหลังได้รับ task
- Agent อยู่ใน state อย่างน้อย `idle`, `assigned`, `walking`, `working`, `talking`, `blocked`, `resting`
- task lifecycle เป็น `queued → assigned → working → done` และมี `blocked`/`resume` path
- notification, dialogue bubble และ activity log
- โลกจำลองเดินต่อเนื่องโดยไม่มีปุ่ม Play, Pause, Step, Reset, x2 หรือ x3
- persistence ของ task, actor และ world state ตามขอบเขต local runtime ที่มีอยู่

### สิ่งที่ไม่อยู่ใน phase แรก

- gameplay loop, campaign, เงิน, win/lose, progression และ resource economy ของเกมเดิม
- การ execute recovered C# หรือการเปิดไฟล์ recovered C จาก browser runtime
- LLM, remote tool, authentication, backend และ multi-user sync
- การอ้างว่า numeric legacy mode ทุกค่าถูกตั้งชื่อ semantic แล้ว
- การสังเคราะห์ asset ที่ extraction ยังไม่มี เช่น face selector `40/41`

## 3. หลักฐานและสถานะความรู้

ทุกข้อสรุปต้องติดสถานะ namespace แยกกัน:

| Namespace | หน้าที่ | Policy |
|---|---|---|
| `legacy_csharp_evidence` | class/method/body/call/branch ที่อ่านจาก Cpp2IL | ใช้เป็นหลักสำหรับ discovery แต่ต้องเก็บ marker/conflict |
| `legacy_raw_field` | `Human*`, `Syain*`, `Target*`, object offsets และ raw writes | ห้ามตั้งชื่อ semantic จากตัวเลขอย่างเดียว |
| `legacy_render_selector` | `TFace`, `TBody`, `TMode`, `TKage`, `BodyFace` | แยกจาก Agent state |
| `adapter_simulation` | state และ behavior ที่เว็บกำหนดเอง | ใช้ได้เมื่อมี contract/test แม้ไม่ใช่ legacy equivalence |
| `product_task` | task, assignment, notification, activity และ result | เป็น product domain ไม่ใช่เกม state |

`HumanMode=0`, `HumanState=0`, `HumanAnime=0` และเลขอื่น ๆ จะถูกเก็บเป็น raw values จนกว่าจะมีหลักฐาน cross-tool และ fixture ที่พอ ยกเว้น adapter state ที่ประกาศชัดว่าเป็น web decision

## 4. สถาปัตยกรรมเป้าหมาย

```text
Cpp2IL C# variants + dump/C/assembly evidence
                    │
                    ▼
        Evidence index + method/field quality manifest
                    │
                    ▼
       Typed world / actor / task / event contracts
                    │
                    ▼
       Continuous Office Simulation Core (hidden clock)
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Scheduler       Navigation      Work Executor
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              Canvas renderer + dashboard
                         │
                         ▼
                 persistence / event log
```

### 4.1 Evidence layer

สร้าง source-backed index ที่ระบุอย่างน้อย:

- source root และ SHA-256
- namespace/class/method/overload
- declaration span และ body span ที่จับจาก declaration จริง
- method status: `present`, `empty`, `missing`, `conflicting`
- control-flow counts: `if`, `else`, `switch`, loops และ early returns
- issue counts: `//IL_`, `NoteDecompilerIssue`, unknown calls, object/default/nint placeholders
- field reads/writes และ called symbols
- comparison ระหว่าง C# primary evidence กับ recovered C/assembly/dump โดยไม่พึ่งโฟลเดอร์ `Assembly-CSharp/` ที่ถูกลบแล้ว
- links ไป recovered C, dump, assembly fallback และ existing Phase artifacts

ตัว checker เดิมที่ตรวจเพียงชื่อเมธอดและ semantic checker ที่เลือก match แรกจะเป็น prototype input เท่านั้น ต้องไม่ใช้ aggregate coverage ของมันเป็น gate

### 4.2 Domain layer

#### Actor

```text
Actor {
  id: stable adapter-owned ID
  employeeId: source-linked employee reference
  profile: name, role, job fields, body/face selectors
  rawLegacy: Human* fields and raw numeric IDs
  position: adapter world position
  navigation: target, path, arrival status
  simulation: idle/assigned/walking/working/talking/blocked/resting
  work: active task, workstation, progress, result
  visual: TFace, TBody, TMode, TKage, animation policy
  dialogue: bubble text/index/lifetime
}
```

Raw `HumanMode`/`HumanState` จะไม่ถูกเขียนทับด้วยชื่อ `simulation` และ stable actor ID จะไม่ใช้ global array index เป็น public identity

#### World

```text
World {
  rooms
  floor/background
  objects/furniture
  workstations
  seats
  walk graph / navigation provider
  coordinate and draw-order policy
}
```

world provider ต้องแยก `verified_asset_relation`, `adapter_coordinate_decision` และ `unknown_legacy_transform` ออกจากกัน

#### Task

```text
Task {
  id, title, description, priority
  status: queued/working/blocked/done
  assignee
  destination/workstation
  simulated duration and progress
  result, blocked reason, timestamps
}
```

งานจำลองจะใช้ `SimulatedWorkExecutor` ก่อน และมี interface เดียวกับ future `LlmWorkExecutor`/`RealToolExecutor`

### 4.3 Simulation core

- hidden continuous clock สำหรับ production runtime
- injectable clock/test harness สำหรับ deterministic tests โดยไม่แสดง control ให้ผู้ใช้
- scheduler รับ task ที่ assign แล้วและเลือก Agent/จุดหมายตาม explicit policy
- Agent controller ทำ state transition และเรียก navigation provider
- navigation provider คืน path, arrival, no-path หรือ unavailable
- work executor จำลอง progress/result โดยไม่เรียก LLM
- event bus ส่ง `actor.*`, `task.*`, `dialogue.*`, `notification.*` ไป renderer/dashboard/persistence
- blocked path ต้องเปลี่ยนเป็น `blocked` พร้อม reason ไม่ teleport Agent

### 4.4 Presentation layer

Canvas renderer รับ draw command จาก world/actor projection ไม่อ่าน C# โดยตรง ส่วน dashboard แสดง:

- scene และตัวละครแบบ live
- actor detail และ raw/adapter status ที่แยก namespace
- task queue, assignment, progress, blocked reason และ result
- notification/activity log
- controls เฉพาะการจัดการ task และ Agent เช่น create, assign, reassign, block, resume, complete; ไม่มี time/gameplay controls

### 4.5 Persistence

ใช้ repository boundary เดิมเป็นฐาน แล้วเพิ่ม snapshot สำหรับ world/actor simulation อย่างมี version:

- task state
- actor position/state/task projection
- world reservations/seat relation ที่เป็น adapter state
- logical event sequence และ migration version

localStorage เป็น phase แรก; backend/auth/multi-user เป็น future boundary

## 5. Roadmap 2.0

### R0 — Freeze และ provenance reset

ผลลัพธ์:

- mark roadmap เดิมเป็น historical/superseded โดยไม่แก้หรือลบ historical artifacts
- สร้าง Roadmap 2.0 เป็น current planning authority หลัง spec review
- ลงทะเบียน `knowledge/csharp/primary/`, dump, recovered C, assembly fallback และ existing evidence พร้อม hash โดยไม่สร้าง `Assembly-CSharp/` กลับ
- กำหนด source precedence ต่อ method: expanded new C# → old C# comparison → C/assembly validator
- สร้าง gap register ชุดใหม่ที่แยก `legacy_unknown`, `adapter_decision`, `product_out_of_scope`

Gate: ทุก input มี path/hash/status และไม่มีการเขียนทับ source root

### R1 — C# corpus index และ quality manifest

ผลลัพธ์:

- declaration-aware parser สำหรับ class, method, overload และ body span
- method diff ระหว่าง C# สอง variants
- field/method/call/branch/placeholder manifest
- quality score ต่อ method โดยไม่ใช้ตัวเลขเดียวตัดสิน semantic completeness
- shortlist product-scope methods: `CallSyain`, `AddObjec`, `NextTarget`, `MainProcess`, `DrawHuman`, `DrawObj`, `AddKaiwa`, `AddMessage`, `DoEvent`, `CallHikkosi` และ dependencies ที่จำเป็น

Gate: parser deterministic, source hash stable, method spans ไม่จับ callsite แทน declaration, regression fixtures ผ่าน

### R2 — Character, scene และ behavior map

ผลลัพธ์:

- employee → actor spawn map
- raw actor field map และ evidence status
- position/target/navigation map
- visual selector/bodyface map
- dialogue/bubble/notification map
- adapter state transition table ที่ไม่อ้างว่าเท่ากับ raw numeric state
- scene/workstation/seat contract สำหรับ initial office slice

Gate: ทุก product-scope field มี source reference, namespace, confidence และ consumer ที่ชัดเจน

### R3 — Typed simulation contracts

ผลลัพธ์:

- typed Actor/World/Task/Event contracts
- `SimulatedWorkExecutor` contract
- navigation, workstation reservation และ seat adapter contracts
- task-to-agent projection contract
- persistence snapshot/migration contract
- event catalog และ error/blocked policy

Gate: contract fixtures ครอบคลุม spawn, assign, walking, arrival, working, blocked, resume, complete, dialogue และ persistence restore

### R4 — Continuous Simulation Core

ผลลัพธ์:

- hidden continuous clock
- scheduler และ Agent state machine
- automatic movement/work loop
- progress/result/blocked behavior
- event bus และ task-system integration
- no Play/Pause/Step/Speed/Reset controls ใน product UI

Gate: เปิดหน้าแล้วโลกเดินเอง; assign task แล้ว Agent เคลื่อนที่และทำงานเอง; blocked ไม่ teleport; task/event projection ตรงกัน

### R5 — Game-like Dashboard

ผลลัพธ์:

- game-like canvas scene
- actor rendering จาก selector policy ที่ verified/adapter-labeled
- actor detail panel
- task queue/assignment/progress/result
- notification/activity timeline
- visible raw-vs-adapter status สำหรับ unknowns
- persistence restore หลัง refresh

Gate: browser smoke ไม่มี error/warning ใหม่, canvas และ dashboard อยู่ใน continuous mode, task action ไม่ทำให้ raw source semantics ถูกอ้างเกินหลักฐาน

### R6 — Golden traces และ fidelity audit

ผลลัพธ์:

- deterministic test harness ที่ฉีด clock ได้เฉพาะ test
- golden traces สำหรับ actor/task/dialogue/notification
- comparison report ระหว่าง C# evidence, existing adapter และ simulation output
- negative-evidence ledger สำหรับ behavior ที่ไม่มีหลักฐาน
- visual smoke fixtures สำหรับ floor, furniture, actor, bubble และ draw order

Gate: ทุก simulation behavior อยู่ใน `verified_source_behavior` หรือ `explicit_adapter_decision`; ไม่มี hidden assumption ที่ไม่มี label

### R7 — Hardening และ scope expansion

ผลลัพธ์:

- เพิ่ม actor/room/workstation ตาม manifest
- migration/versioning ของ snapshots
- recovery จาก corrupted/local persistence
- performance budget ของ continuous loop
- accessibility/observability ของ dashboard
- optional backend boundary โดยไม่ผูกกับ core

Gate: regression ของ runtime เดิมยังผ่าน, new simulation scenarios deterministic และ state migration ย้อนกลับได้ตาม policy

### R8 — Future brain adapters

ผลลัพธ์ภายหลังเท่านั้น:

- `LlmWorkExecutor`
- tool execution boundary
- agent memory/context
- approval/audit policy
- backend/auth/multi-user

LLM จะคืน task result/action proposal ผ่าน contract และไม่มีสิทธิ์แก้ sprite/render state โดยตรง

## 6. Migration จาก roadmap เดิม

งานเดิมจะถูกจัดกลุ่มดังนี้:

- Phase 0–2 asset/character evidence: retained baseline และนำมาใช้ใน R0–R2
- Phase 4 Wave 3–4 actor/dialogue contracts: retained evidence input และ revalidated ผ่าน C# method map
- Phase 5 runtime: retained compatibility baseline และเป็น renderer/asset fixture สำหรับ R4–R5
- Phase 6 task system: retained task/repository boundary และเชื่อมเข้ากับ R4 scheduler
- P0-A corpus pipeline: ปรับ scope จาก full translation-first เป็น C# evidence index/quality gate ใน R1
- P0-B TypeScript port: superseded ในฐานะ roadmap หลัก และถูกรวมเป็น clean simulation implementation ใน R3–R5
- Phase 7 AI: เลื่อนไป R8 หลัง simulated work loop และ dashboard fidelity gate ผ่าน

ไม่มีการลบไฟล์เก่า ไม่มีการเปลี่ยน historical result ให้กลายเป็น claim ใหม่ และไม่มีการ mark legacy equivalence จากการที่ simulation ทำงานได้

## 7. Definition of Done ของ Roadmap 2.0

Roadmap 2.0 จะถือว่าปิด product core เมื่อ:

- C# input ทั้งสอง variant มี hash และ method-level manifest
- product-scope methods มี declaration/body/call/field evidence ที่ trace ได้
- world, actor, task และ event contracts ถูกกำหนดและทดสอบ
- หน้าเว็บเปิดแล้ว office simulation เดินเองต่อเนื่อง
- Agent รับ task แล้วเดินไปทำงานและเปลี่ยน state เอง
- task complete/blocked/resume และ notification/activity ทำงาน
- actor visual/dialogue/seat/workstation relation แสดงได้ตาม evidence หรือ adapter policy
- refresh/restore state ผ่าน contract
- ไม่มี product UI สำหรับ pause/speed/playback
- unknown legacy semantics แสดงเป็น raw/adapter status ไม่ถูกตั้งชื่อด้วยการเดา
- runtime path ไม่อ่าน recovered C# หรือ C โดยตรง
- future LLM/tool executor สามารถเสียบผ่าน interface โดยไม่รื้อ simulation core

## 8. ข้อจำกัดและความเสี่ยงที่ยอมรับ

- C# decompiler corpus มี control-flow มากขึ้นแต่ยังไม่ใช่ clean source; quality manifest เป็น gate บังคับ
- `HumanMode`, `HumanState`, `HumanAnime`, `HumanTime` และ numeric `TMode` ยังไม่ตั้งชื่อ legacy semantics โดยอัตโนมัติ
- animation timing/direction/loop/mirroring และ `TFace=40/41` ยังเป็น open evidence
- full world/isometric/depth/pivot/SEB mapping ยังไม่ถูกอ้างเป็น legacy equivalence
- .NET SDK และ C# project references ไม่พร้อม จึงไม่ใช้ C# compilation เป็น phase gate ของเว็บ
- localStorage และ adapter state ไม่ใช่ multiplayer backend หรือ legacy save compatibility

ข้อจำกัดเหล่านี้ไม่ block simulated office MVP ตราบใดที่ state/behavior ถูก label เป็น `adapter_simulation` และมี fixture รองรับ

## 9. Review gate

เอกสารนี้เป็น design/roadmap ไม่ใช่ implementation plan และยังไม่มีการแก้ runtime code ตามเอกสารนี้

หลัง user review และ approval ให้สร้าง implementation plan แยกตาม R0 → R6 โดยเริ่มจาก R0/R1 และใช้ checkpoints review ก่อนต่อ R2/R3; ห้ามเริ่ม port หรือแก้ browser behavior ก่อน design scope และ source precedence ในเอกสารนี้ได้รับการยืนยัน
