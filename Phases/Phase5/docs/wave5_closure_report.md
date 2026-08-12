# Wave 5 — Closure report

อัปเดต: 2026-08-12

สถานะ: **complete_with_known_limitations**

## Verified in this pass

- locale artifact สร้างจาก CSV ปัจจุบัน 12 ภาษา, union IDs 2,420, duplicate ID 0 และ strict UTF-8 ผ่าน
- room manifest reference `floor0.png`/`floor0.seb` โดยคง tail shortfall 4 bytes
- Node runtime tests ผ่าน 10 scenarios: movement, blocked movement, seat ownership, lifecycle cleanup,
  locale/draw selector, deterministic replay, bounded furniture/depth, timer policy, adapter animation profile และ raw event mode
- Python contract/visual tests ผ่าน 17 tests
- W5.2 furniture mapping contract แยก `imgBihin_[1]` chair, `imgBihin_[2]` desk และ `imgFloorParts` reception
- W5.3 numeric contract decode `DDBody=0`, `DDChair=25`, `DDDesk=26`, `DDPC=77`, `IndexImgFloorParts=-1` initial sentinel และ 3×14 `DeskImgData`/`ChairImgData` records
- W5.3 crop/placement trace ปิด `DrawObj` source-rect flow, `AddObjec` field map และ bounded `CallHikkosi` numeric placement branches
- suffix `.png.bytes` → extracted `.png` และ field flow ของ destination/crop ถูกบันทึกเป็น evidence-backed contract
- W5.4 ยืนยัน `AppData.GetImage` เป็น name-to-resource-array bridge และ `LoadBihinImage` เป็น `IMG_LIST[selector] + .png.bytes` consumer
- W5.4 พบว่า recovered `IMG_LIST` values ที่ selector 25/26/77 ไม่ join กับ `chair0_origin.png`/`desk0_origin.png`/`pc.png`; manifest indices 29/30/117 จึงคงเป็น candidate เท่านั้น
- W5.4 บันทึกความขัดแย้งของ `stringliteral.json` (12,647 entries) กับ APK `global-metadata.dat` (12,661 entries; first observed mismatch ID 2395) และห้าม hardcode selector-to-filename mapping
- W5.5 แก้ indexing root cause: Ghidra `StringLiteral_N` เป็น one-based แต่ JSON tables เป็น zero-based; `StringLiteral_833=.png` และ `StringLiteral_7514=face_`
- W5.5 align native literal values กับ active APK metadata แบบ exact string-value join ครบ 80/80 และ join กับ game `img.inf` ได้ exact 77 รายการ + normalized face 3 รายการ
- W5.5 ปิด bihin selectors แบบ exact: `DDChair=25→chair0_origin.png/index29`, `DDDesk=26→desk0_origin.png/index30`, `DDPC=77→pc.png/index117`
- W5.6 ยืนยัน `IndexImgFloorParts=-1`, mode `param_2=1` ที่รับ `param_3` ตรง ๆ และ callsites ที่คำนวณ `DDFloor+3=42→floorparts0.png/index79`
- W5.6 ยืนยัน bounded `DDFloor+param_3` mapping สำหรับ `floor0.png`/`floor1.png`/`floor2.png` และถอด SEB loader เป็น group/record structure; `office/floor0.seb` มี 1 group/1 partial record และ tail shortfall 4 bytes
- W5.6 resolve `StringLiteral_4798` เป็น `RECT` สำหรับ optional rectangle tail แต่ยังไม่พบ tail ใน `floor0.seb`; field semantics และ room placement จึงยังคงเปิด
- W5.7 trace `GetSpritesLocal`/`GetSpriteLocal` → `ConvBufferToSprite` → `DrawImage`; `dump.cs` constants ยืนยัน `SP_TEX_ID`, `SP_U/V/W/H`, `SP_TRANS_X/Y` และ C consumer ปิด local crop กับ `base + trans` destination
- W5.7 ยืนยัน `GetBRectSeb` บวก external base x/y, optional pixel rect fallback และ anchor `GetBoundingRect → SetOffset → draw → ClearOffset`; room/world caller mapping, anchor enum, depth และ universal transform ยังคงเปิด
- W5.8 ยืนยัน `RenderGameScreen` clip/origin wrapper ครอบ `DrawObj` และ reset origin หลังวาด
- W5.8 ปิด bounded PNG room formula `ObjecX/Y + ObjecZX/ZY` กับ crop `ObjecCX/CY/WX/WY` ผ่าน `GameForm.imgFloorParts`; scoped `DrawObj` ไม่มี `ResourceManager.DrawSeb`
- W5.8 inventory พบ SEB callsites อยู่ใน UI/subform/rank/special-form consumers; ยังไม่พบ direct `floor0.seb` → `GameForm.DrawObj` caller ใน scope นี้
- W5.9 ปิด `AddObjec` parameter-to-field provenance, default `ObjecZX/ZY=0`, `MainProcess` `ObjecX/Y` averaging update และ furniture producer field sets ของ `CallPCChange`/`CallDeskChange`/`CallChairChange`
- W5.9 ยืนยัน recovered `OnTouchCamera` และ `SetOrigin` เป็น no-op, ไม่พบ named camera-symbol references ใน categorized C และไม่พบ nonzero `ObjecZX/ZY` writes ใน scoped producer scan
- W5.9 ยืนยัน generic `JarInflater.GetData → ResourceManager.LoadSeb` เป็น loader bridge เท่านั้น; direct `floor0.seb` → `GameForm.DrawObj` mapping และ literal `floor0.seb` ใน categorized C ยังไม่พบ
- browser smoke test boot, floor render, bounded reception/desk/chair assets, actor render, step, movement,
  dialogue, notification และ console logs ผ่าน
- browser screenshot ถูกบันทึกเป็น `Phases/Phase5/artifacts/wave5_smoke.jpg` และตรวจ JPEG header สำเร็จ
- source roots ไม่ถูกแก้โดย Wave 5 runtime

## Known limitations

- furniture เป็น bounded asset renderer สำหรับ reception/desk/chair จาก source-root PNG จริง; bihin numeric selectors,
  exact metadata/filename join, bounded crop records, bounded `CallHikkosi` placement, observed floor-parts
  selector join, SEB local crop/base placement, bounded PNG room screen placement และ object-producer field provenance
  ปิดแล้ว แต่ source-array semantics, producer-side world/isometric mapping, full SEB room/world reconstruction,
  placement/pivot/depth semantics และ universal transform/legacy equivalence ยังไม่ปิด
- semantic animation verified = 0; runtime มี explicit adapter profiles แต่ยังไม่ claim state-to-mode semantics
- `TFace=40/41` ยัง unresolved และไม่มี face substitution
- timer unit, universal coordinate/depth semantics, raw speaker binding และ numeric event modes ยังเปิด; raw mode/args ถูกเก็บแบบ opaque

## Follow-up ที่ไม่ block closure

1. trace source-array semantics (`GameForm+0xE40/+0xF50/+0xF58`), camera/world-isometric mapping, nonzero `ObjecZX/ZY`, depth/pivot และ direct `floor0.seb` room mapping โดยไม่ pad final-record tail
2. ทำ responsive visual checks เพิ่มเมื่อ runtime host ถูกนำไปใช้งานใน deployment context
3. trace timer/token/graph/event semantics แบบ targeted เฉพาะเมื่อมี concrete product dependency
