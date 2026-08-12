# C# Semantic Inventory and Simulation Core Design

**Date:** 2026-08-12
**Status:** Design approved in conversation; written-spec review pending
**Scope:** Gameplay-critical C# slice and the first canonical Simulation Core

## Goal

สร้าง semantic inventory ที่อ้างอิงกลับไปยัง C# และหลักฐาน reverse-engineering ได้ทุกจุด แล้วใช้ inventory นั้นออกแบบ deterministic Simulation Core สำหรับ office scene, actor, movement, timer, dialogue/event และ task projection โดยไม่ execute decompiled C# โดยตรงและไม่ตั้งชื่อ semantic ให้ค่าที่หลักฐานยังพิสูจน์ไม่ได้

## Context and constraints

- C# discovery evidence หลักอยู่ที่ `knowledge/csharp/primary/` และมี 85 `.cs` files พร้อม `Assembly-CSharp.csproj`.
- รอบแรกจะวิเคราะห์ gameplay-critical slice ก่อน ไม่ inventory ระบบ billing, network, install, analytics และ external-service ทั้งหมดในเชิงลึก.
- source/extraction roots เดิมเป็น read-only และ `Assembly-CSharp/` จะไม่ถูกสร้างกลับ.
- decompiled C# เป็น evidence ไม่ใช่ buildable production runtime; runtime จะใช้ JavaScript adapter ที่เขียนใหม่.
- ค่า numeric mode/state ที่ยังไม่มีหลักฐานยืนยันต้องคงเป็น raw value หรือ `unknown`.
- recovered C, assembly fallback และ reverse-engineering reports ใช้เป็น corroborating evidence และ validator ไม่ใช่ source ที่ execute.
- Simulation Core รุ่นแรกต้อง deterministic, snapshot-able และ replay/debug ได้จาก code/tests โดยไม่แสดง playback controls ให้ผู้ใช้.
- LLM, backend, authentication, multi-user synchronization และงานจริงอยู่นอกขอบเขตรอบนี้.
- runtime UI เป้าหมายเป็น continuous simulation: เริ่มเดินเองเมื่อ boot และไม่มีปุ่ม Play, Pause, Step, Reset หรือ speed multiplier.

## Scope

### C# structural inventory

ทำ structural inventory ให้ไฟล์ gameplay-critical ที่เลือก รวมถึง dependency ที่ถูกอ้างถึงโดย slice นี้:

- `knowledge/csharp/primary/form/GameForm.cs`
- `knowledge/csharp/primary/main/Main.cs`
- `knowledge/csharp/primary/main/Anim.cs`
- `knowledge/csharp/primary/form/FormManager.cs`
- `knowledge/csharp/primary/form/MyFormBase.cs`
- `knowledge/csharp/primary/data/*.cs` เฉพาะ type ที่ถูกใช้โดย actor, employee, appearance, event หรือ scene slice
- supporting evidence จาก `knowledge/characters/evidence/` และ `knowledge/reverse-engineering/`

Structural inventory จะบันทึก class, enum, interface, field, method, signature, inheritance, source span, source hash และ decompiler warnings ที่เกี่ยวข้อง

### Deep semantic inventory

ฟังก์ชันที่ต้องวิเคราะห์เป็น priority slice:

```text
Main.OnUpdate
FormManager.PreUpdate
FormManager.Updated
GameForm.Update
GameForm.MainProcess
GameForm.DoEvent
GameForm.ProcessEvent
GameForm.AddEvent
GameForm.CallSyain
GameForm.NextTarget
GameForm.AddTarget
GameForm.CallFuki
GameForm.AddKaiwa
GameForm.AddMessage
GameForm.DrawObj
GameForm.DrawHuman
```

field groups ที่ต้อง trace:

```text
Human*
Event*
Message*
Object/Objectec*
Target*
Camera*
GameTime / FormTime / cycle_time
BodyFace / HumanFaceG / HumanBodyG
```

การ trace ต้องบันทึก read sites, write sites, callsites, branch conditions, timer behavior, downstream effects และ provenance ไม่ใช่เพียงรายการชื่อ field

## Architecture

```text
Protected source and extraction roots
              |
              v
      C# / C / assembly evidence
              |
              v
      Semantic inventory register
              |
              v
      Canonical SimulationState
              |
              v
      Deterministic SimulationCore
              |
              v
      OfficeRuntime adapter ports
              |
              v
      Derived render commands + dashboard projection
```

### Ownership boundaries

- `Semantic Inventory` owns evidence records, source spans, field-flow facts and semantic status.
- `SimulationCore` owns logical clock, canonical scene state, actor state, command application, transition validation and event ordering.
- `OfficeRuntime` owns adapter implementations for path finding, collision, seats, locale, body/face assets and canvas draw commands.
- `TaskSystem` owns task lifecycle, persistence and assignment rules; Simulation Core receives a task projection rather than duplicating task ownership.
- Dashboard reads snapshots/projections and submits commands; it never mutates actor state directly.
- C# and raw reverse-engineering artifacts remain outside runtime imports.

ช่วง migration สามารถมี facade เพื่อรักษา public methods เดิมของ `OfficeRuntime` ให้ tests เดิมทำงานได้ แต่ต้องมี source of truth เดียวต่อ state และต้องระบุใน code ว่า facade เป็น compatibility boundary

## Semantic inventory artifacts

สร้าง generated evidence ใต้:

```text
knowledge/csharp/evidence/semantic_inventory/
├── inventory_manifest.json
├── type_catalog.json
├── field_catalog.json
├── method_catalog.json
├── transition_catalog.json
├── provenance_index.json
└── inventory_report.md
```

### Inventory record rules

ทุก record ต้องมีอย่างน้อย:

```json
{
  "symbol": "form.GameForm.HumanMode",
  "kind": "field",
  "source": {
    "file": "knowledge/csharp/primary/form/GameForm.cs",
    "line_start": 1617,
    "line_end": 1617
  },
  "raw_type": "int[]",
  "semantic_status": "unknown",
  "evidence_refs": [],
  "notes": []
}
```

สถานะที่อนุญาต:

- `verified`: field flow หรือ behavior รองรับโดยหลักฐานที่ตรวจสอบซ้ำได้
- `candidate`: มีหลักฐานบางส่วนแต่ยังมีช่องว่างหรือความขัดแย้ง
- `unknown`: ยังตั้งชื่อหรืออธิบายไม่ได้อย่างปลอดภัย
- `adapter_only`: เป็น semantic ที่ runtime เพิ่มเพื่อใช้งานเว็บและยังไม่อ้างว่าเท่ากับเกมเดิม
- `raw_only`: เก็บค่า/branch/call target ได้ แต่ยังไม่มี semantic interpretation

### Provenance model

ทุก semantic claim ใช้ record รูปแบบนี้:

```json
{
  "claim_id": "claim.actor.human_mode",
  "field_path": "actors[*].state.legacy.human_mode",
  "status": "raw_only",
  "source_refs": [
    {
      "source_type": "csharp",
      "file": "knowledge/csharp/primary/form/GameForm.cs",
      "line_start": 1617,
      "line_end": 1617,
      "symbol": "form.GameForm.HumanMode"
    },
    {
      "source_type": "reverse_report",
      "file": "knowledge/reverse-engineering/reports/wave4_slices/event_mode_02.md",
      "symbol": "DoEvent"
    }
  ],
  "rationale": "Raw mode is preserved; semantic names are not established."
}
```

ไม่มี `semantic_name` ใดผ่านเข้า canonical state โดยไม่มี provenance และ status ที่รองรับ

## Canonical SimulationState

schema รุ่นแรกใช้ version `simulation-core-v1`:

```json
{
  "schema_version": "simulation-core-v1",
  "simulation_id": "office-demo",
  "clock": {
    "tick": 0,
    "unit": "logical_tick",
    "wall_clock_policy": "ui_scheduler_only",
    "deterministic": true
  },
  "scene": {
    "scene_id": "office.floor0",
    "room_id": "office.floor0.adapter",
    "camera": {},
    "objects": []
  },
  "actors": [],
  "task_projection": [],
  "event_log": [],
  "evidence": {},
  "legacy_equivalence": false
}
```

### Actor contract

```json
{
  "id": "actor.0",
  "identity": {
    "employee_id": "employee.0",
    "name": "Aoi",
    "role": "worker",
    "face_id": 2,
    "body_id": 3,
    "provenance": []
  },
  "state": {
    "adapter": "idle",
    "semantic": null,
    "semantic_status": "adapter_defined",
    "legacy": {
      "human_mode": null,
      "human_state": null,
      "human_anime": null
    }
  },
  "position": {
    "x": 220,
    "y": 326,
    "target": null,
    "direction": null,
    "provenance": []
  },
  "movement": {
    "status": "idle",
    "path": [],
    "goal_point": null,
    "raw_now_point": null,
    "raw_goal_point": null
  },
  "activity": {
    "task_id": null,
    "task_status": null,
    "timer": null
  },
  "interaction": {
    "seat_id": null,
    "bubble_id": null
  },
  "animation": {
    "face_selector": 2,
    "body_selector": 3,
    "raw_mode": 0,
    "semantic_mode": null,
    "frame_index": 0
  },
  "provenance": []
}
```

หลักการแยก state:

- `state.adapter` ใช้สำหรับ deterministic web behavior ที่ยืนยันได้ใน runtime
- `state.semantic` ใช้เมื่อ inventory ยืนยันความหมายจากหลักฐานแล้ว
- `state.legacy` เก็บค่าดิบจาก `HumanMode`, `HumanState`, `HumanAnime` โดยไม่แปลความ
- `animation.raw_mode` ไม่ได้แปลว่าเป็น animation semantic ของเกมจนกว่าจะมีหลักฐาน
- `unknown` และ `null` เป็นค่าที่ถูกต้องและต้องแสดง provenance ได้

### Initial field mapping policy

| C# field | Canonical target | Initial status |
|---|---|---|
| `HumanX`, `HumanY` | `actor.position` | `verified` field-flow |
| `HumanPX`, `HumanPY` | raw previous/intermediate position | `unknown` |
| `HumanNowPoint` | `movement.raw_now_point` | `raw_only` |
| `HumanGoalPoint` | `movement.raw_goal_point` | `raw_only` |
| `HumanFaceG` | `identity.face_id` | `verified` selector |
| `HumanBodyG` | `identity.body_id` | `verified` selector |
| `HumanMode` | `state.legacy.human_mode` | `raw_only` |
| `HumanState` | `state.legacy.human_state` | `raw_only` |
| `HumanAnime` | `animation.raw_mode` | `raw_only` |
| `HumanTime` | actor timer candidate | `candidate` until branch proof |
| `HumanFukiTime` | bubble timer | `verified` lifecycle slice |
| `HumanFukiIndex` | bubble raw index | `verified` lifecycle slice |
| `EventMode` | raw event mode | `raw_only` |
| `EventTemp`, `EventTemp2` | raw event arguments | `raw_only` |
| `MessageText` | message/dialogue payload | `candidate` lifecycle slice |
| `MessageTime` | message timer | `candidate` lifecycle slice |
| `MessageGraph` | raw graph selector | `raw_only` |

เลข mode เช่น `HumanMode = 5` จะไม่ถูกตั้งเป็น `working` โดยการเดา

## Actor state machine

### Adapter states

รอบแรกใช้ state ที่ runtime รองรับอยู่แล้ว:

```text
idle
walking
working
sitting
break
talking
```

movement status แยกจาก actor state:

```text
idle
moving
arrived
blocked
no_path
unavailable
```

### Transition table

```text
spawn                         -> idle
move.requested                -> walking
actor.arrived                 -> idle
collision.blocked             -> idle + movement.blocked
seat.occupied                 -> sitting
seat.released                 -> idle
task.started                  -> working
dialogue.requested            -> talking
bubble.expired                -> previous adapter state or idle
```

กฎบังคับ:

1. actor state เปลี่ยนผ่าน command/reducer เท่านั้น
2. Dashboard ไม่เขียน state object โดยตรง
3. ทุก transition สร้าง event
4. transition ผิดกฎต้องคืน error และไม่ mutate state
5. adapter-defined state ต้องติด `legacy_equivalence: false`
6. clock และ event sequence ต้องเพิ่มแบบ monotonic
7. semantic state ที่ยังไม่มีหลักฐานต้องคง `null`/`unknown`

## Commands and event envelope

### Command boundary

คำสั่งที่ core รุ่นแรกต้องรองรับ:

```text
actor.spawn
actor.move.request
actor.seat.occupy
actor.seat.release
dialogue.request
notification.create
task.projection.update
legacy.event.record
```

ทุก command ต้องมี `command_id`, `type`, `source`, `payload` และ actor/task reference ที่จำเป็น

### Event contract

```json
{
  "sequence": 12,
  "tick": 8,
  "type": "actor.arrived",
  "actor_id": "actor.0",
  "source": "simulation_core",
  "status": "verified_adapter_event",
  "payload": {
    "position": [336, 326]
  },
  "provenance": []
}
```

event status ที่อนุญาต:

```text
verified_adapter_event
raw_opaque_event
candidate_event
unknown
```

สำหรับ `DoEvent` หรือ mode ที่ยังถอดไม่ได้ ต้องเก็บ raw event แทนการตั้งชื่อ:

```json
{
  "type": "legacy.event.raw",
  "status": "raw_opaque_event",
  "payload": {
    "mode": 17,
    "args": [2, 4, 9],
    "source_tag": "GameForm.DoEvent"
  }
}
```

## Tick pipeline

หนึ่ง logical tick ทำงานตามลำดับ deterministic นี้:

```text
1. รับ command ที่ค้างอยู่
2. เพิ่ม clock หนึ่ง tick
3. ประมวลผล actor movement
4. ประมวลผล timer
5. ประมวลผล event queue
6. อัปเดต task projection
7. หมดอายุ bubble และ notification
8. ตรวจ invariants
9. สร้าง snapshot และ digest
10. ส่ง snapshot ให้ adapter และ renderer
```

ลำดับนี้เป็น adapter order ที่ deterministic ไม่ใช่ข้ออ้างว่าเป็นลำดับภายในเกมเดิม 100%; ต้องระบุ `legacy_equivalence: false` ไว้ใน snapshot และ contract

## Runtime integration

ไฟล์ runtime ที่เสนอสำหรับ implementation:

```text
runtime/office/app/simulation_schema.js
runtime/office/app/simulation_core.js
runtime/office/app/runtime.js
runtime/office/app/app.js
runtime/office/tests/test_simulation_core.js
runtime/office/tests/test_simulation_contract.py
runtime/office/evidence/simulation_core_contract.json
runtime/office/reports/simulation_core_architecture.md
```

บทบาท:

- `simulation_schema.js` สร้าง/normalize/validate canonical state, command และ event
- `simulation_core.js` เป็น reducer, transition validator, tick loop, snapshot และ digest
- `runtime.js` ให้ adapter ports สำหรับ path, collision, seat, locale, body/face และ render commands
- `app.js` รับ snapshot และวาด UI; ไม่เป็นเจ้าของ state
- tests JavaScript ตรวจ behavior และ deterministic replay
- tests Python ตรวจ contract artifact, schema version, path boundary และ provenance policy

ระหว่าง migration ต้องรักษา public compatibility ที่ tests ของ `OfficeRuntime` ใช้อยู่ หรือสร้าง facade ที่ชัดเจนจนกว่าจะย้าย consumer ครบ

## Continuous simulation UI

หลัง core และ adapter contracts ผ่านแล้ว `runtime/office/app/app.js` จะเปลี่ยนเป็น:

```text
boot
  -> create SimulationCore
  -> load scene and actors
  -> start internal scheduler
  -> advance one tick per interval
  -> render latest snapshot
```

ปุ่ม Play, Pause, Step, Reset และ speed multiplier จะถูกถอดออกจากหน้าเว็บ การ advance แบบ manual จะเหลือเฉพาะ API ภายใน tests/debugging ไม่ใช่ user control

## Testing strategy

### Inventory tests

- structural manifest นับ source files และ hash ได้ตรงกับ input
- expected symbols เช่น `MainProcess`, `DoEvent`, `HumanMode`, `CallSyain`, `DrawObj` ต้องพบ
- source span ต้องเป็น line range ที่มี symbol จริง
- run ซ้ำจาก input เดิมต้องได้ output digest เดิม
- inventory tool ต้องไม่แก้ `knowledge/csharp/primary/`
- ทุก deep record ต้องมี provenance อย่างน้อยหนึ่งรายการ
- semantic report ต้องแยก `verified`, `candidate`, `unknown`, `raw_only`, `adapter_only`

### Simulation Core tests

- สร้าง actor แล้วได้ `actor.spawned` และ state `idle`
- move request สร้าง path/movement event และเดินตาม tick อย่าง deterministic
- arrival, collision, no-path และ unavailable เปลี่ยน movement status ถูกต้อง
- seat conflict ไม่ mutate actor ที่เข้าไม่สำเร็จ
- timer expiry ล้าง bubble/notification และสร้าง expiry event
- dialogue เปลี่ยน adapter state และเก็บ raw speaker/talk data
- task projection ไม่กลายเป็น task lifecycle ซ้ำใน core
- raw legacy event เก็บ mode/args ครบโดยไม่ตั้ง semantic name
- invalid command/state ถูกปฏิเสธโดย snapshot ก่อนและหลังเท่ากัน
- snapshot/digest จาก fixture เดิมเท่ากันทุกครั้ง
- sequence และ tick monotonic
- provenance path ถูก validate และชี้ไปยังไฟล์จริง

### Regression checks

หลังแต่ละ milestone ต้องรันชุดเดิมทั้งหมดที่เกี่ยวข้อง:

```text
reverse-engineering suite
character tests
maintenance/layout tests
office runtime tests
dashboard task tests
Python compile checks
browser smoke หลัง UI cutover
```

## Implementation milestones

### M0 — Evidence baseline

อ่าน state, hash input, ตรวจ source roots และล็อก target manifest ก่อนสร้าง generated artifact ใหม่

### M1 — Structural inventory

สร้าง inventory tool และ catalog type/field/method พร้อม deterministic output และ contract tests

### M2 — Deep semantic slices

trace actor identity, position, movement, timer, bubble, event, message และ rendering พร้อม provenance และ unknown preservation

### M3 — Canonical schema

สร้าง schema/normalizer/validator, fixture และ contract artifact โดยยังไม่ตัด UI controls

### M4 — Deterministic Simulation Core

สร้าง command reducer, actor state machine, tick pipeline, event log, snapshot/digest และ test suite

### M5 — Office adapter integration

เชื่อม path/collision/seat/locale/body-face/render กับ core โดยคง compatibility facade ให้ runtime tests เดิมผ่าน

### M6 — Continuous dashboard

เชื่อม snapshot stream, ถอด Play/Pause/Step/Reset/speed controls, start scheduler อัตโนมัติ และทำ browser smoke

### M7 — Handoff

อัปเดต `PROJECT_STATE.md`, `TODO.md`, runtime reports และเก็บ unresolved semantic gaps เป็นรายการ evidence-backed สำหรับรอบถัดไป

## Out of scope

- การ compile หรือ execute decompiled C# ในเว็บ
- การสร้าง `Assembly-CSharp/` กลับ
- การเดาความหมาย numeric state จากเลขเพียงอย่างเดียว
- การถอด `DoEvent` ทั้งหมดให้เป็น semantic event ในรอบแรก
- LLM decision loop, backend, auth, multi-user sync และ live work integrations
- ระบบ playback controls สำหรับผู้ใช้
- การลบ evidence เดิมเพราะยังไม่ได้ใช้ใน core

## Acceptance criteria

งานรอบนี้ถือว่าผ่านเมื่อ:

1. gameplay-critical C# slice มี structural catalog ที่สร้างซ้ำได้และมี source hash
2. deep semantic records ทุกตัวมี source span และ provenance
3. ค่า unknown/raw ที่ยังพิสูจน์ไม่ได้ไม่ถูกแปลงเป็น semantic name
4. `simulation-core-v1` validate ได้และมี fixture ครบสำหรับ actor, movement, timer, dialogue, event และ task projection
5. Simulation Core มี state ownership, reducer, event ordering, snapshot และ deterministic digest
6. OfficeRuntime ทำหน้าที่เป็น adapter/render boundary ไม่ใช่แหล่ง semantic claim
7. regression suite เดิมยังผ่าน
8. หน้าเว็บเริ่ม simulation ต่อเนื่องเองและไม่มี Play/Pause/Step/Reset/speed controls
9. state ที่หน้า dashboard แสดงกลับไปถึง canonical snapshot และ evidence/provenance ได้
10. `PROJECT_STATE.md` และ `TODO.md` ระบุสิ่งที่ verified, สิ่งที่เป็น adapter และ semantic gaps ที่ยังเหลืออย่างตรงไปตรงมา

## Decisions recorded

- ใช้ evidence-led staged inventory แทน full 85-file semantic rewrite
- ใช้ canonical schema แยกจาก decompiled object layout
- แยก adapter state กับ raw legacy state เพื่อไม่ปน semantic ที่ยังไม่พิสูจน์
- เก็บ raw event/mode/args เมื่อ semantic mapping ยังไม่ปิด
- ให้ Simulation Core เป็น source of truth ระยะยาว และใช้ OfficeRuntime เป็น adapter
- ใช้ deterministic logical tick; wall-clock scheduler มีหน้าที่แค่ขับ tick ใน UI
- เก็บ manual advance ไว้ใน tests/debug API แต่ไม่เปิดเป็น user controls
