# Phase 0 — Freeze baseline

สถานะ: เสร็จแล้วแบบ `complete_with_known_limitations`

ผลลัพธ์อยู่ที่:

- `artifacts/asset_manifest.json`
- `artifacts/language_manifest.json`
- `artifacts/code_coverage_manifest.json`
- `artifacts/phase0_baseline.json`
- `artifacts/phase0_checksums.sha256`
- `docs/phase0_baseline_report.md`

Phase 0 อ่าน source roots แบบ read-only และเก็บ hash สำหรับใช้ตรวจใน phase ถัดไป ไม่แก้ asset, dump, APK หรือ Ghidra project

รันใหม่จาก workspace root ด้วย `python APK_Toolkit/create_phase0_baseline.py`
