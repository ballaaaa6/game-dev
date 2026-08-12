# Wave 6 — Task system และ dashboard interaction plan

## Goal

ทำให้ office runtime มี task queue, explicit assignment, lifecycle, notification,
activity log และ dashboard interaction ที่ deterministic และทำงานได้โดยไม่มี AI model

## Execution slices

- W6-C0: freeze Wave 5 baseline, contract และ gap register
- W6-C1: task schema, store, lifecycle validation และ logical tick
- W6-C2: assignment rules, one-active-task-per-agent และ deterministic queue ordering
- W6-C3: durable task notification และ append-only activity log
- W6-C4: Agent projection ผ่าน public runtime adapter โดยไม่แก้ raw legacy fields
- W6-C5: versioned local persistence, restore, reset และ export
- W6-C6: task dashboard, Agent detail, filters, notification/activity views และ highlight focus
- W6-C7: contract test, runtime test, browser smoke, closure report และ state handoff

## Wave 6.1 — production hardening ที่ทำได้โดยไม่รอ backend

- W6.1-A: แยก `TaskRepository` interface จาก `TaskSystem` และกำหนด repository envelope/revision
- W6.1-B: migrate direct `wave6-task-state-v1` snapshot เดิมโดยไม่ทำ task state หาย
- W6.1-C: เพิ่ม optimistic conflict detection, visible degraded/conflict status และ reload path
- W6.1-D: กำหนด local permission policy แบบ explicit และคง authentication เป็น boundary
- W6.1-E: เพิ่ม schema-stable JSON import/export และ dashboard persistence controls
- W6.1-F: เพิ่ม contract/runtime/browser regression และ handoff update

## Explicit non-goals

- ไม่เชื่อม AI model
- ไม่ทำ auto-assignment
- ไม่ทำ remote backend หรือ multi-user synchronization
- ไม่ตีความ raw legacy event modes, MessageGraph หรือ gameplay state
- ไม่สังเคราะห์ world/camera/SEB semantics ที่ Wave 5 ยังเปิดอยู่

## Closure gates

- task system tests ผ่านทุก lifecycle และ conflict scenario
- persistence/restore deterministic
- dashboard create/assign/start/block/resume/complete/read ผ่าน
- Wave 5, Phase 4 และ Phase 2 regression ยังผ่าน
- browser console ไม่มี error/warning
- artifacts มี schema version, source hash และ controlled gaps
