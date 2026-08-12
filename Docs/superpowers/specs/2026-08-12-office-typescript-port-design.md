# Office Runtime TypeScript Port Design

## สถานะและเป้าหมาย

เอกสารนี้เป็น downstream design ของ `P0-A Corpus Intelligence Pipeline` ซึ่งต้องผ่าน corpus closure gate
ก่อนเริ่ม port implementation; Phase 4 artifacts เดิมถูกนำเข้าเป็น evidence ตั้งต้นและไม่ต้องสร้างซ้ำ

เอกสารนี้กำหนดให้การ port โค้ดเฉพาะ office runtime เป็นงานหลักถัดไปของโปรเจกต์ โดยเปลี่ยนผลจาก Phase 4 จาก evidence/contract ที่อ่านอ้างอิงได้ ให้กลายเป็น TypeScript implementation ที่ runtime เรียกใช้ได้จริงและมี regression test รองรับ

ขอบเขตนี้ไม่ใช่การแปลเกมทั้งเกมและไม่ใช่การทำ legacy-equivalence ทั้งหมด เป้าหมายคือปิดเส้นทางที่ Virtual AI Office ต้องใช้จริง:

```text
asset/resource → room/furniture → employee actor → movement/seat → draw
              → dialogue/bubble → notification/task event
```

## หลักฐานและขนาดงาน

ข้อมูลที่ตรวจสอบแล้วจาก repository ปัจจุบัน:

- Phase 4 shortlist มี 88 functions จาก 12 classes และ 1,850 fields
- shortlist แบ่งเป็น categorized C 83, assembly fallback 2 และ dump/script-only 3
- marker-spanned recovered C ของ shortlist รวมประมาณ 40,974 บรรทัดในกลุ่ม foundation/resource/render/scene/actor/dialogue/lifecycle
- `MainProcess` มีประมาณ 15,353 บรรทัด และ `NextPoint` ประมาณ 2,403 บรรทัด แต่เป็น mixed gameplay/office logic จึงไม่ port ทั้ง function
- `NewGamePara` และ `DoEvent` มี assembly fallback รวม 29,240 instructions; จะ port เฉพาะ bounded clusters ที่มี dependency ต่อ office เท่านั้น

ตัวเลข 40,974 บรรทัดจึงเป็น audit boundary สำหรับการอ่านและคัดกรอง ไม่ใช่ target ที่ต้องคัดลอกลง TypeScript ทั้งหมด คาดว่า implementation ที่ใช้กับ product scope จะอยู่ราว 6,000–12,000 บรรทัด TypeScript และมี test/fixture เพิ่มราว 2,000–4,000 บรรทัด โดยตัวเลขนี้เป็น engineering estimate และจะปรับตามผลของแต่ละ port gate

## ขอบเขตที่ต้อง port

### Resource และ scene

Port เฉพาะ resource bridge และ room/object behavior ที่ web runtime ใช้:

- `AppData.GetImage`, `LoadBihinImage`, `EventGChange`
- `AddObjec`, `CallHikkosi`, `AddTarget`
- `CallPCChange`, `CallDeskChange`, `CallChairChange`
- `GetPcImgData`, `GetDeskImgData`, `GetChairImgData`
- `DrawObj`, `DrawFloorCover`, `DrawDesk`, `DrawChair`, `DrawReception`
- selector, crop, local placement และ deterministic draw ordering ที่มี evidence แล้ว

ข้อมูล selector/filename/crop ที่ปิดได้แล้วให้ generate เป็น typed data หรือ runtime manifest โดยไม่ให้ runtime เปิด recovered C อ่านทีละบรรทัด

### Actor และ interaction

Portเฉพาะ employee/actor lifecycle ที่จำเป็นต่อ office:

- `AddBodyFace`, `DrawHuman`
- `AddSyain`, `CallSyain`
- `NextTarget` และ movement interface ที่รองรับ path provider
- seat occupy/release/query boundary
- actor position, draw command และ selector composition

state/mode/timer ที่ยังพิสูจน์ไม่ได้จะเก็บเป็น raw numeric value หรือ adapter policy ห้ามตั้งชื่อ legacy semantic จากการเดา

### Dialogue, bubble และ event bridge

Portเฉพาะข้อความและ event ที่ agent ใช้:

- `GetTalkTexts`, `GetTalkIndex`, `AddKaiwaTalkData`, `AddKaiwa`
- `AddFuki`, `CallFuki`, `DrawFukidashi`, `ResetTextLayout`
- `AddMessage`, notification expiry และ activity/event mirror
- bounded `DoEvent`/`MainProcess` clusters ที่แตะ actor, dialogue, bubble หรือ notification

ระบบ game progression, economy, sales, ranking, research และ event branches ที่ไม่ส่งผลต่อ office ไม่อยู่ใน port

## สิ่งที่ไม่ port

- `MainProcess` และ `DoEvent` ทั้ง function
- game development, sales, market, research, fans, ranking, awards และ progression
- save/load, menu/UI นอก office และ platform services
- generic Unity/.NET/Android framework
- full legacy pathfinding, physics, animation semantics, camera/isometric transform หรือ SEB world mapping เมื่อยังไม่มี evidence ปิด
- `TFace=40/41` จะไม่ substitute asset ที่ไม่มีหลักฐาน

## สถาปัตยกรรม

```text
Raw C / dump / assembly
        ↓
Phase 4 evidence JSON + Markdown
        ↓
typed source references + contracts
        ↓
Phase 5 runtime-ts TypeScript modules
        ↓
compiled browser runtime + Node tests
```

JSON ยังคงเป็น source evidence, generated data, manifest และ fixture ส่วน behavior จะย้ายมาอยู่ใน TypeScript แยกเป็น module ที่ทดสอบได้:

- `source-ref.ts` — source symbol, file, line, artifact และ confidence
- `types.ts` — typed legacy namespaces, office objects, actors, selectors, raw modes
- `resource-adapter.ts` — resource/asset resolution จาก verified manifests
- `scene-runtime.ts` — room objects, crop, placement และ draw commands
- `actor-runtime.ts` — spawn, actor state, selector composition และ actor draw
- `movement-seat.ts` — injected path/collision/seat providers
- `dialogue-runtime.ts` — locale lookup, talk, bubble และ placeholder formatting
- `event-bridge.ts` — named product events และ raw legacy event preservation
- `browser-entry.ts` — exposes the browser bundle to the existing browser shell

ใช้ TypeScript compiler สำหรับ Node/test output และใช้ esbuild เป็น browser bundler เพื่อให้ browser shell ได้ไฟล์ IIFE เดียวที่ expose `window.Wave5Runtime`; ไม่โหลด TypeScript modules จาก browser โดยตรง Phase 5 JavaScript runtime จะเป็น compatibility baseline ระหว่างการ port และจะถูกเปลี่ยน consumer ไปยัง compiled TypeScript ทีละ module หลัง contract เดิมผ่านครบ

## สถานะความรู้

ทุก port unit ต้องมีสถานะหนึ่งค่า:

```text
evidence_ready → contract_ready → ts_ported → verified
                                      ↘ blocked
```

`verified` ต้องมี source reference, deterministic fixture, unit test และระบุชัดว่า behavior เป็น `legacy_fact`, `web_adapter_decision` หรือ `unknown` การมี JSON หรือ pseudocode อย่างเดียวไม่ถือว่า `ts_ported` สถานะ `known` ใน TypeScript ใช้ได้เฉพาะกับ product adapter status ไม่ใช่การยืนยันว่า raw legacy mode มีความหมายเดียวกัน

## เกณฑ์ผ่านของงานหลัก

- runtime เรียกใช้ TypeScript implementation ได้โดยไม่ต้องอ่าน recovered C ตอน request/runtime path
- room, furniture, actor, movement/seat, draw, dialogue/bubble และ task event มี typed interface ครบตาม product scope
- ทุก module มี source provenance และ test ที่รันซ้ำได้
- unknown ที่ยังเปิดถูกแสดงเป็น raw/adapter status ไม่ถูกซ่อนด้วยชื่อ semantic ที่เดา
- Phase 5/6 regression เดิมยังผ่าน และ browser smoke ไม่มี console error/warning ใหม่
- Phase 7 AI model จะเริ่มต่อได้หลัง port gate ผ่าน ไม่ต้องย้อนกลับไปอ่าน source dump สำหรับ feature พื้นฐาน
