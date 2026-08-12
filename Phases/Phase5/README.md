# Phase 5 — Minimal web office runtime

สถานะ: `complete_with_known_limitations` — Wave 5 C0–C8, W5.1-B–G, W5.2, W5.3, W5.4, W5.5, W5.6 floor-parts/SEB structural trace, W5.7 SEB consumer/crop/base-placement trace, W5.8 room-caller/screen-placement trace และ W5.9 object-producer/camera/SEB mapping trace ผ่าน; runtime, adapter contracts, visual smoke artifact และ full regression พร้อมใช้ต่อ

Runtime host อยู่ที่ `runtime/`; generated manifests, contracts, gap register และ QA report อยู่ใน `artifacts/` และเอกสารอยู่ใน `docs/`. Source asset เดิมไม่ย้ายเข้ามา ให้ runtime reference path กลับไปยัง source root ผ่าน local server

งานหลักถัดไปคือ **Office Runtime TypeScript Port (P0)** ตาม
`docs/superpowers/plans/2026-08-12-office-typescript-port.md`. `runtime/` JavaScript
ปัจจุบันเป็น compatibility baseline; TypeScript จะถูก build เป็น Node/test output และ
browser bundle แยกกัน แล้วจึงค่อยสลับ browser consumer หลัง parity gate ผ่าน

สิ่งที่ทำแล้ว:

- deterministic `OfficeRuntime` พร้อม logical tick และ event log
- explicit path/collision/seat providers
- body/face draw command จาก 42 `BodyFace` records
- locale runtime artifact จาก CSV 12 ภาษา, default `th` แบบ web adapter
- dialogue/bubble/notification lifecycle และ cleanup
- bounded asset renderer สำหรับ reception/desk/chair จาก source-root PNG จริง
- deterministic mixed draw order สำหรับ furniture + actors ตาม adapter depth policy
- logical timer, zero-lifetime expiry และ explicit cleanup contract
- explicit adapter animation profiles และ raw numeric-event bridge โดยไม่ตั้งชื่อ legacy semantics
- `TFace=40/41` classification เป็น index-space gap โดยไม่ substitute asset
- แยก furniture image loading contract ระหว่าง `imgBihin_` กับ `imgFloorParts` พร้อม selector/crop/placement statuses
- decode numeric static selectors, floor-parts initial sentinel, furniture image-data records และ bounded `CallHikkosi` placement ไว้ใน `wave5_3_numeric_crop_placement_contract.json`
- ยืนยัน `AppData.GetImage` loader bridge และแยก recovered `IMG_LIST` literal namespace ออกจาก game `img.inf` manifest candidates ไว้ใน `wave5_4_img_list_loader_bridge.json`
- แก้ one-based `StringLiteral_N` กับ zero-based JSON indexing และ align ค่าไปยัง active APK metadata; ปิด `DDChair=25→chair0_origin.png/index29`, `DDDesk=26→desk0_origin.png/index30`, `DDPC=77→pc.png/index117` ใน `wave5_5_img_list_alignment.json`
- trace `IndexImgFloorParts=-1` → `EventGChange(param_2=1,param_3)` และยืนยัน initial `DDFloor+3=42→floorparts0.png/index79`; ถอด SEB loader framing, `RECT` tail marker และ `office/floor0.seb` partial record ใน `wave5_6_floorparts_seb_contract.json`
- trace `GetSpritesLocal`/`GetSpriteLocal` → `ConvBufferToSprite` → `DrawImage`; ยืนยัน `SP_TEX_ID`, `SP_U/V/W/H`, `SP_TRANS_X/Y`, bounded `GetBRectSeb` base addition และ anchor offset lifecycle ใน `wave5_7_seb_consumer_contract.json`
- trace `RenderGameScreen` clip/origin wrapper → `DrawObj`; ยืนยัน bounded PNG room destination/crop formula, `imgFloorParts` slot และแยก SEB UI callers ออกจาก room path ใน `wave5_8_room_caller_contract.json`
- trace `AddObjec` parameter-to-object-field provenance, `MainProcess` `ObjecX/Y` averaging update, furniture update producers และ camera/SEB boundaries ใน `wave5_9_object_producer_contract.json`; คง full world/isometric transform และ direct `floor0.seb` room mapping เป็น open
- browser smoke test ของ floor, actors, controls และ diagnostics
- public `setAgentTaskProjection`/`recordAdapterEvent` bridge สำหรับ Phase 6 โดยไม่เปลี่ยน legacy boundary

ข้อจำกัดที่ยังเปิด:

- furniture renderer ปิดได้เฉพาะ bounded asset families; bihin numeric selector values, active metadata join, exact chair/desk/PC filename mapping, bounded crop records, bounded `CallHikkosi` placement, loader bridge, observed floor-parts selector join, SEB local crop/base placement, bounded PNG room screen placement และ object-producer field provenance ปิดแล้ว แต่ source-array semantics, producer-side world/isometric mapping, full SEB room mapping, pivot/depth/transform semantics และ legacy equivalence ยังไม่ปิด
- animation ใช้ static verified frame policy เพราะ semantic animations ที่ verified ยังเป็น 0
- semantic animation mapping, `TFace=40/41` asset namespace, timer unit, raw speaker binding, event mode semantics และ universal depth/transform ยังคงไม่ปิด

เกณฑ์ closure ที่ผ่าน:

- Phase 4 regression `107/107`
- Phase 2 regression `5/5`
- Phase 5 Node runtime `10` scenarios และ Python contract/visual tests `17`
- browser smoke: floor + furniture assets + actors + controls ผ่าน, console error/warning `0`
- browser artifact เดิม: `artifacts/wave5_smoke.jpg`; W5.1 browser capture ตรวจใน session และไม่ได้อ้างเป็น legacy pixel equivalence
