# Phase workspace

โฟลเดอร์นี้เป็นที่เก็บงานตาม phase โดยแยก `artifacts/`, `docs/` และ `references/` ออกจากกัน

| Phase | สถานะ | ที่เก็บหลัก |
|---|---|---|
| Phase 0 | เสร็จแล้ว มี known limitations | `Phase0/artifacts/`, `Phase0/docs/` |
| Phase 1 | inventory เสร็จ มี warnings ที่บันทึกไว้ | `Phase1/artifacts/`, `Phase1/docs/` |
| Phase 2 | รอเริ่ม | `Phase2/references/`, `Phase2/docs/` |
| Phase 3 | รอเริ่ม | `Phase3/references/`, `Phase3/docs/` |
| Phase 4 | รอเริ่ม | `Phase4/docs/` |
| Phase 5 | รอเริ่ม | `Phase5/docs/` |
| Phase 6 | รอเริ่ม | `Phase6/docs/` |
| Phase 7 | รอเริ่ม | `Phase7/docs/` |

## Source ที่ไม่อยู่ใน Phases

โฟลเดอร์ต่อไปนี้เป็น source/input เดิมและตั้งใจคงไว้ที่ตำแหน่งเดิมเพื่อไม่ทำลาย path ของเครื่องมือ:

- `game-dev-story-mod_Sprites/`
- `game-dev-story-mod_Dumped/`
- `game-dev-story-mod_Extracted/`
- `ghidra_11.0.1_PUBLIC/`
- `APK_Toolkit/game-dev-story-mod.apk`
- `APK_Toolkit/game-dev-story-mod.zip`

## วิธี rerun

รันจาก workspace root; scripts จะอ่าน source เดิมและเขียนผลลัพธ์กลับเข้า phase ที่ถูกต้องโดยอัตโนมัติ:

```powershell
python APK_Toolkit/create_phase0_baseline.py
python APK_Toolkit/decode_seb.py
python APK_Toolkit/create_phase1_catalog.py
python APK_Toolkit/create_phase1_code_trace.py
python APK_Toolkit/create_phase1_office_manifest.py
python APK_Toolkit/create_phase1_preview.py
python APK_Toolkit/validate_phase1.py
python -m unittest APK_Toolkit.test_phase1_seb -v
```

อย่าวางผลลัพธ์ไว้ที่ root ด้วย `--output` เอง เว้นแต่กำลังทำงานชั่วคราวที่ไม่ได้เป็น artifact ของ phase
