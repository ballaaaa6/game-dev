# Phase 4 Wave 4 — Dialogue, text, bubble และ lifecycle bridge

อัปเดต: 2026-08-11

สถานะ: **W4-C0 ถึง W4-C7 ปิดรอบแบบ `complete_with_known_limitations`**

Wave 4 ใช้ Wave 3 actor handoff เป็น input และคง `legacy_equivalence=false` สำหรับ
ทุก adapter fixture. ไม่แปล `DoEvent` หรือ `MainProcess` ทั้งฟังก์ชัน และไม่ตั้งชื่อ
raw event/mode/speaker จากการเดา.

## Packages

- W4-C0: baseline/hash/gap register
- W4-C1: CSV locale contract และ fallback/token fixture
- W4-C2: talk index, talk text, speaker และ `KaiwaLine` contract
- W4-C3: `Fuki*`, `HumanFuki*`, `DrawFukidashi` contract
- W4-C4: `AddEvent` producer และ bounded `DoEvent` consumer boundary
- W4-C5: actor → talk → bubble deterministic adapter trace
- W4-C6: `AddMessage` notification bridge — bounded producer/consumer/compaction slice
- W4-C7: closure/handoff — bounded consumer slices, manifest และ Phase 5 handoff เสร็จ
- W4.5: evidence hardening — logical timer candidate, HumanFuki cleanup boundary,
  talk/speaker pipeline, MessageGraph render behavior และ DoEvent target clusters

## Source policy

CSV, `dump.cs`, categorized C, assembly fallback และ Wave 3 artifacts เป็น read-only
source-of-truth. Generated output อยู่ใต้ `Phases/Phase4/`.

## Closure evidence

ดู `artifacts/wave4_lifecycle_slices.json` และ `docs/wave4_closure_report.md` สำหรับ
MainProcess/DrawObj consumer ranges, DoEvent target map และ notification compaction.

## Open gaps

ดู `artifacts/wave4_gap_register.json`; ข้อสำคัญคือ English fallback, talk token
semantics, raw speaker-to-actor binding, bubble timer cleanup, `DoEvent` branch semantics,
talking state และ message graph/audio labels.
