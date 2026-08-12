# Phase 4 Wave 0 — Translation index report

สถานะ: เสร็จแล้ว (index/coverage only; ยังไม่ port implementation)

## ผลตรวจจาก source จริง

- shortlist: 88 functions
- categorized C: 83 functions
- assembly fallback only: `form_GameForm__NewGamePara` (13,671 instructions) และ `form_GameForm__DoEvent` (15,569 instructions)
- dump/script-only: 3 functions
- selected classes: 12; fields: 1,850 (มี offset 1,345 รายการ)
- string table: 12,647 entries; C references ที่พบ 10,804 literal IDs
- office-runtime graph: 277 nodes, 359 edges; unresolved/external nodes 5
- coverage actions: translate 74, slice 5, contract-only 9

## Artifacts

- `../artifacts/field_offset_map.json`
- `../artifacts/function_inventory.json`
- `../artifacts/string_literal_map.json`
- `../artifacts/office_runtime_call_graph.json`
- `../artifacts/translation_coverage.json`
- `../artifacts/wave0_build_manifest.json`

Builder: `../tools/build_wave0_index.py`

ตรวจด้วย:

```powershell
python Phases/Phase4/tools/build_wave0_index.py
python -m unittest discover -s Phases/Phase4/tests -p "test_*.py" -v
```

ผลล่าสุด: 6/6 tests ผ่าน และ source roots เดิมยังอ่านแบบ read-only

## ข้อสังเกตและข้อจำกัด

- `StringLiteral_<index>` ถูก map แบบ zero-based ตาม `stringliteral.json`; `StringLiteral_12647` เป็น terminal pointer ที่อยู่นอกช่วง table และถูกเก็บใน `terminal_sentinel_ids` แยกจาก missing literals
- call graph เป็นหลักฐานจาก categorized C และอาจมี external/framework nodes; ยังไม่ใช่ semantic dependency closure ที่ปิดแล้ว
- `NewGamePara`/`DoEvent` ยังเป็น assembly evidence เท่านั้น ต้องทำ branch index ก่อน slice ใน Wave 5
- การมี categorized C ไม่ได้แปลว่า unit แปลเสร็จ; ยังต้อง resolve named fields, branch behavior, fixtures และ confidence ใน Wave 1–6

## งานถัดไป

เริ่ม Wave 1 โดย trace `GameForm..cctor`, `AppData.Init`, `ResourceManager.Load*`, `JarInflater` และ initializer slice ที่เติม `imgBody[]`/`imgFace[]` เพื่อสร้าง selector-to-resource-to-file map พร้อม fixture อย่างน้อยหนึ่งรายการต่อ asset family
