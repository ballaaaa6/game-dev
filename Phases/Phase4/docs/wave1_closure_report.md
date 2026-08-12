# Wave 1 closure report

อัปเดต: 2026-08-11

## คำตัดสินใจ

Wave 1 ปิดได้ในสถานะ `complete_with_known_limitations` และ gate เป็น `ready_for_wave2_with_known_limitations` ไม่ใช่การยืนยันว่า recovered source สมบูรณ์ทั้งเกม แต่เป็นการปิด resource truth ที่จำเป็นโดยไม่ปล่อยให้ Wave 2 เดา index หรือ filename

## สิ่งที่ตรวจสอบและผลลัพธ์

| งาน | หลักฐาน | ผล |
|---|---|---|
| W1-C0 baseline | `wave1_build_manifest.json`, `wave1_branch_index.json`, source hashes | ผ่าน; source roots ยังคง read-only |
| W1-C1 static selectors | `wave1_selector_resolution.json` | write provenance ครบ 5 selectors; numeric values ยังเป็น dynamic/runtime-backed และไม่ถูกเดา |
| W1-C2 imgFace | `wave1_imgface_conflict.json` | ยืนยัน conflict: raw loop โหลด `StringLiteral_7514 = false`; asset family ยืนยัน `face_0..35`; ไม่ rewrite เป็น `face_` |
| W1-C3 asset/index audit | `wave1_asset_gap_audit.json` | manifest 291/291 มีไฟล์จริง; 15 unmatched IMG_LIST ถูกจัดประเภท; `TFace=40/41` เป็น index-space mismatch |
| W1-C4 bounded slices | `wave1_slices.json` และ `docs/wave1_slices/` | มี slice ที่มี entry/exit/block/call/offset/confidence ครบทั้ง `NewGamePara` และ `DoEvent` |
| W1-C5/C6 | gap register + tests | ไม่มี unclassified unknown; builder และ regression ผ่าน; gate พร้อมไป Wave 2 แบบมีข้อจำกัด |

## สิ่งที่ยังขาด และสาเหตุ

- ค่า numeric ของ `DDBody`, `DDPC`, `DDChair`, `DDDesk` ยังไม่ถูก decode เป็น literal จาก cross-source trace; หลักฐานที่มีเป็น runtime/GOT-backed writes จึงเก็บเป็น `dynamic_value_with_preconditions`
- `imgFace` มี evidence ขัดกันระหว่าง recovered literal กับ asset family; การแก้ให้เป็น `face_` จะเป็นการเดา จึงคง `conflicting_evidence`
- `TFace=40/41` ไม่สามารถเป็น zero-based index ตรงของ `imgFace[36]` บน guarded direct paths; ยังต้อง trace caller/alternate namespace เมื่อทำ selector adapter
- `NewGamePara` และ `DoEvent` ยังไม่ได้แปลทั้งฟังก์ชัน; semantic label ของ state/offset ที่ไม่ได้ map ตรงยังถูกคงเป็น neutral structural description

สิ่งเหล่านี้ไม่ใช่ unclassified unknown: แต่ละรายการมี controlled status, evidence, impact และ next action ใน `wave1_gap_register.json`

## ขอบเขตที่ Wave 2 ใช้ได้

Wave 2 สามารถใช้ได้ทันทีสำหรับ:

- `ResourceManager`/`AppData.GetImage` contract และ manifest-to-file mapping ที่ตรวจแล้ว
- verified image fixtures และ canonical basename matching
- symbolic selector contracts ที่มี preconditions โดยไม่ hardcode numeric base
- bounded control-flow evidence ของ `NewGamePara` และ `DoEvent`

Wave 2 ห้ามทำสิ่งต่อไปนี้โดยไม่มีหลักฐานใหม่:

- hardcode ค่า static selector ที่ยังไม่ decode
- เปลี่ยน `StringLiteral_7514` เป็น `face_`
- map `TFace=40/41` เป็น `imgFace[40]` หรือ `imgFace[41]`
- ตั้งชื่อ field/state จาก raw offset หรือ literal เพียงอย่างเดียว

## Verification commands

```text
python Phases/Phase4/tools/build_wave1_resource_map.py --check
python -m unittest discover -s Phases/Phase4/tests -p "test_*.py"
```

ผลตรวจล่าสุด: Wave 1 tests ผ่านทั้งหมด `18/18` และ source roots ไม่ถูกแก้

## Handoff ต่อ Wave 2

งานถัดไปที่มีลำดับชัดเจนคือสร้าง selector adapter แบบ symbolic, trace caller ของ `TFace=40/41` เฉพาะจุดที่ runtime ต้องใช้ และเลือก semantic slice เพิ่มเมื่อมี dependency จริง ไม่จำเป็นต้องย้อนกลับไป decompile `NewGamePara` หรือ `DoEvent` ทั้งฟังก์ชันก่อนเริ่ม Wave 2
