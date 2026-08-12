# Corpus Intelligence Pipeline Design

## สถานะและเป้าหมาย

งานนี้เป็นงานเร่งด่วน `P0-A` ของ repository และต้องทำก่อนงาน port runtime หรือการเก็บ Phase อื่นต่อ

เป้าหมายคือสร้างคลังความรู้จาก IL2CPP/Ghidra extraction ที่:

- ค้นหาได้ทั้ง corpus โดยไม่ต้องเปิดไฟล์ดิบทีละไฟล์
- ย้อนกลับได้ถึง source, symbol, address และ line span ทุกข้อสรุป
- ใช้ผลลัพธ์ Phase 4 เดิมเป็น evidence ตั้งต้นโดยไม่สร้างซ้ำ
- สร้าง annotated และ compressed views ได้โดยไม่ทำลาย source of truth
- ใช้ AI สร้าง candidate logic map แบบประหยัด token
- ตรวจ candidate ด้วย source, cross-tool comparison และ fixture ก่อน promote
- เก็บ metadata ของส่วนที่ยังไม่เกี่ยวกับ office ไว้สำหรับ feature ในอนาคต

งานนี้ไม่ได้มีเป้าหมายให้ AI เขียนเกมทั้งเกมเป็น TypeScript หรือยืนยัน semantic ของ decompiler ทุก function
โดยอัตโนมัติ การแปลกว้างจะเป็น knowledge candidate ส่วน implementation ที่ execute ได้จะทำภายหลังใน
`P0-B Office Runtime TypeScript Port` เฉพาะ dependency closure ที่ผ่าน gate

## หลักฐานตั้งต้นที่ตรวจแล้ว

- current extraction report มี 110,824 functions และ C recovery coverage 110,820 functions
- Phase 4 Wave 0 มี shortlist 88 functions จาก 12 classes, 1,850 fields และ call graph 277 nodes/359 edges
- shortlist มี categorized C 83 units, assembly fallback 2 units และ dump/script-only 3 units
- recovered-C ของ shortlist เป็น audit boundary ประมาณ 40,974 บรรทัด ไม่ใช่จำนวนที่ต้องคัดลอกลง runtime
- `NewGamePara`/`DoEvent` มี assembly fallback รวม 29,240 instructions และต้อง slice ตาม dependency
- Phase 4/5/6 มี contracts, fixtures, gap registers, manifests และ regression tests ที่ต้องนำเข้าเป็น evidence

ตัวเลข source และ artifact ที่ใหม่กว่าต้อง supersede เอกสารเก่าได้ผ่าน manifest และ reconciliation เท่านั้น
ห้ามแก้ source roots เพื่อให้ตัวเลขตรงกับเอกสาร

## ขอบเขต

### อยู่ในขอบเขต

1. Freeze source/artifact hashes และสร้าง baseline manifest
2. รวม `dump.cs`, `script.json`, `stringliteral.json`, `il2cpp.h`, recovered C, assembly และ Phase 4 artifacts
3. สร้าง canonical function/field/string/resource/call/data-flow index
4. สร้าง raw, annotated, normalized และ prompt-compressed views พร้อม source map
5. สร้าง cross-tool comparison สำหรับ Il2CppDumper, Ghidra และ Cpp2IL เมื่อมี tool
6. สร้าง pilot 100 functions และวัด coverage, determinism, token reduction และ conflict rate
7. สร้าง batch candidate logic-map schema, cache, request manifest และ provider boundary
8. สร้าง source validator, fixture promotion gate, negative-evidence ledger และ queryable knowledge store
9. ส่งต่อเฉพาะ verified evidence ไปยัง P0-B และปรับปรุง handoff/roadmap

### ไม่อยู่ในขอบเขต

- แก้ไข `game-dev-story-mod_Sprites/`, `game-dev-story-mod_Dumped/`, `game-dev-story-mod_Extracted/` หรือ Ghidra project
- แปล framework/library ทุก method เป็น prose
- promote ชื่อ semantic ของ mode, timer, event, speaker, animation หรือ coordinate ที่ยังไม่มี evidence
- เลือกผลจาก tool หนึ่งแทนอีก tool หนึ่งโดยอัตโนมัติเมื่อมี conflict
- สร้าง TypeScript implementation ในงาน P0-A
- ยิง AI batch ขนาดใหญ่ก่อน pilot ผ่าน deterministic/source-map/validation gates

## หลักการออกแบบ

### Evidence-first และ lossless-by-default

Raw source เป็น immutable input การย่อทั้งหมดเป็น view ที่สร้างใหม่ได้ ทุก omitted range ต้องเก็บ source path,
line span, hash และเหตุผลไว้ และต้อง reconstruct raw content ได้

### Stable identity ก่อน semantic

ทุก function ใช้ `unit_id` ที่ประกอบจาก source hash, canonical symbol, address namespace และ source span
ไม่ใช้ชื่อ function อย่างเดียว เพราะชื่อ generic/overload/namespace ซ้ำได้

### แยก fact, candidate และ adapter decision

ใช้สถานะและ namespace แยกกัน:

```text
indexed → annotated → candidate → source_validated → fixture_verified
                                              ↘ blocked
                                              ↘ out_of_scope
```

`web_adapter_decision` ไม่ถือเป็น `legacy_fact` และ JSON/pseudocode อย่างเดียวไม่ถือว่า ported

### เก็บกว้าง แปลลึกตาม impact

- ทุก function: identity, signature, source, call/data edges และ failure status
- game logic: compact candidate summary เมื่อ classifier จัดว่าเกี่ยวข้อง
- office dependency: source validation และ fixture verification
- framework/library: contract/side-effect metadata
- future feature: query index แล้วขยาย closure แบบ incremental

## สถาปัตยกรรม

```text
immutable extraction roots + Phase 4/5/6 artifacts
                    ↓
           baseline/source manifest
                    ↓
       canonical evidence graph + SQLite/JSONL index
                    ↓
 raw → annotated → normalized → prompt view (with source map)
                    ↓
     deterministic triage + cross-tool comparison
                    ↓
             AI candidate logic maps
                    ↓
      source validator + fixtures + negative evidence
                    ↓
    verified knowledge records / blocked records / queries
                    ↓
           P0-B Office Runtime TypeScript
```

### Canonical stores

Generated output อยู่ใต้ `Phases/Phase4/artifacts/corpus/`:

- `manifest.json` — source/artifact hashes, schema versions, counts และ supersession links
- `functions.jsonl` — หนึ่ง record ต่อ function สำหรับ streaming/review
- `edges.jsonl` — call, field, string, resource และ data-flow edges
- `corpus_index.sqlite` — query store พร้อม FTS5 สำหรับ symbol/source/claim search
- `views/` — raw-preserving view metadata และ source maps
- `candidates/` — AI request/response records ที่ cache ด้วย input hash
- `validation/` — validator, conflict, promotion และ negative-evidence reports

Phase 4 historical artifacts ไม่ถูกเขียนทับ ให้ `cross_wave_gap_reconciliation.json` เป็น current-status view
เมื่อ historical register ขัดกับ evidence ที่ใหม่กว่า

## Data contracts

### `SourceRef`

```json
{
  "root": "game-dev-story-mod_Dumped",
  "path": "Categorized_Code/Global/form.c",
  "line_start": 1,
  "line_end": 20,
  "address_namespace": "assembly_export",
  "address": "0x00efec90",
  "sha256": "..."
}
```

### `FunctionRecord`

ต้องมี `unit_id`, canonical symbol, namespace/class, signature, addresses, source refs, C/assembly availability,
caller/callee edges, fields read/write, string/resource refs, decompile status และ confidence/status

### `ViewRecord`

ต้องมี raw input hash, view kind, output hash, source-map path, omitted ranges, transformation rules และ tool version

### `CandidateLogicRecord`

ต้องมี symbol, source refs, reads, writes, calls, branches, state/timer/resource claims, pseudocode, unknowns,
model/prompt/schema version และ `confidence: candidate`

### `ValidationRecord`

ต้องมี checked claims, resolved/ambiguous/missing references, fixture IDs, cross-tool conflicts, promotion status,
validator version และ reason เมื่อไม่ promote

## External tool policy

- Il2CppDumper เป็น metadata/input baseline ที่มีอยู่แล้ว
- `ghidra_headless.py` และ `ghidra_export_c.py` เป็น decompile/symbol pipeline หลักที่มี report/retry อยู่แล้ว
- Cpp2IL ใช้เป็น optional side-by-side oracle สำหรับ ISIL/CFG และ method dump; output ไม่เขียนทับ extraction
- Il2CppInspector ใช้เป็น fallback เฉพาะกรณีจำเป็น เพราะ upstream ระบุว่าการพัฒนาถูกระงับ
- tool ที่ไม่มีในเครื่องต้องทำให้ comparison task รายงาน `not_available` แบบ deterministic ไม่ทำให้ทั้ง pipeline พัง

## Gate และตัวชี้วัด

### Gate A — baseline

- source roots hash ไม่เปลี่ยน
- manifest rerun แล้ว counts/hash stable
- Phase 4/5/6 artifacts ถูก import พร้อม schema/source refs

### Gate B — index

- ทุก discoverable function มี stable identity หรือ explicit parse failure
- ทุก failure มี source path/reason
- call/field/string/resource edges query ได้

### Gate C — views

- annotation ไม่สร้าง silent replacement
- compressed view reconstruct raw source ได้
- omitted ranges และ source map ครบ
- token reduction วัดจาก tokenizer จริง

### Gate D — pilot

- 100 functions ครอบคลุม direct office, dependencies, large/assembly-related และ out-of-scope sample
- JSON/schema valid ทุก candidate
- source refs resolve หรือถูกติดป้าย unknown
- cross-tool conflicts ถูกบันทึกครบ
- rerun ได้ผล deterministic

### Gate E — promotion

- candidate claims ผ่าน source validator
- มี deterministic fixture หรือ explicit contract สำหรับ behavior
- `fixture_verified` แยกจาก `web_adapter_decision`
- ทุก unresolved item มี owner, next action และ reopen trigger

### Gate F — handoff

- corpus closure report และ query guide สร้างแล้ว
- P0-B ได้เฉพาะ verified evidence
- Phase 4/5/6 regression เดิมยังผ่าน
- `PROJECT_STATE.md`, `TODO.md`, roadmap และ phase README สอดคล้องกัน

## การป้องกันการวนซ้ำ

1. Incremental hash จะข้าม unit ที่ source/prompt/schema version ไม่เปลี่ยน
2. Negative-evidence ledger เก็บ search scope, patterns, source hash และ conclusion
3. Supersession links ชี้ว่า artifact ใดถูก evidence ใหม่แทนที่
4. Query ก่อน trace ใหม่: ถ้ามี unit/edge/gap เดิมต้อง reuse ก่อนสร้างงานซ้ำ
5. Reopen ได้เฉพาะเมื่อมี source/asset/feature dependency ใหม่
6. Full corpus metadata เก็บไว้แม้ unit จะ out-of-scope ในรอบปัจจุบัน

## ผลลัพธ์ที่คาดหวัง

P0-A จะเพิ่ม breadth ของความรู้โดยไม่ลดความเข้มงวดของ Phase 4 เดิม: ทั้ง corpus มี searchable inventory,
office closure มี candidate/verified records, ส่วนที่ยังไม่เกี่ยวข้องมี metadata และ dependency สำรองสำหรับอนาคต
และ P0-B สามารถเริ่มจาก evidence ที่จัดประเภทแล้วโดยไม่ต้องย้อนอ่าน dump แบบไม่มีดัชนี
