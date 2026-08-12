# Phase 2 — Character และ animation catalog

สถานะ: `complete_with_known_limitations`

พื้นที่เตรียมไว้:

- `references/bodyface_records.json` — compatibility/reference copy ของ records ที่ใช้กับ extractor เดิม
- `docs/CHARACTER_PRODUCTION_MANUAL.md` — evidence-first character reference

source canonical ที่ freeze อยู่ใน `game-dev-story-mod_Dumped/bodyface_records.reference.json` และ asset อยู่ใน `game-dev-story-mod_Sprites/game/`

ผลลัพธ์ที่สร้างแล้วอยู่ใต้ `artifacts/`, `artifacts/preview/` และ `docs/phase2_report.md`:

- input audit, bodyface analysis และ character asset catalog
- `character_manifest.json`, `animation_manifest.json`, code trace และ Agent-state mapping
- body/face contact sheets และ neutral mode preview จาก original assets
- automated validation report และ deterministic smoke tests ใน `tests/`
- แผน follow-up สำหรับยืนยัน resource index และ animation semantics ใน `docs/phase2_investigation_plan.md`

หลักฐาน follow-up ยืนยันแล้วว่า `DrawHuman` ประกอบจาก `imgBody[TBody]` และ `imgFace[TFace]`
โดยใช้ crop/offset ของ `BodyFace[TMode]`; ข้อเท็จจริงนี้ไม่เท่ากับการยืนยันว่า mode ใดคือ
`idle`, `walking`, `working`, `sitting`, `break` หรือ `talking`.

สถานะนี้หมายถึงหลักฐานที่มีใน extraction ปัจจุบันถูก catalog แล้ว ไม่ได้หมายความว่า
semantic ของทุก mode หรือ Agent state ถูกยืนยันครบ. `idle`, `walking`, `working`,
`sitting` และ `break` ยังคงเป็น `unknown`; `talking` เป็น `probable` สำหรับ
candidate mode 8/9 ใน Kaiwa/dialogue draw path เท่านั้น.

สร้างซ้ำได้ด้วย:

```powershell
python Phases/Phase2/tools/build_phase2_catalog.py
python -m unittest discover -s Phases/Phase2/tests -p "test_*.py" -v
```
