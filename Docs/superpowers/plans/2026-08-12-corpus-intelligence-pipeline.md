# Corpus Intelligence Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** สร้างคลังความรู้แบบ lossless และ queryable จาก IL2CPP/Ghidra corpus โดยรวม Phase 4 evidence, สร้าง safe views, ทำ candidate translation แบบ cache ได้ และส่งต่อเฉพาะข้อสรุปที่ตรวจแล้วไปยัง Office Runtime TypeScript

**Architecture:** ใช้ Python deterministic builders เป็นแกนกลาง, JSONL/SQLite เป็น canonical index และเก็บ raw extraction แบบ read-only. Ghidra/Il2CppDumper เป็นหลักฐานเดิม, Cpp2IL เป็น optional comparison oracle, ส่วน AI ทำ candidate logic maps ที่ต้องผ่าน source/fixture promotion gate ก่อนเสมอ

**Tech Stack:** Python 3.10+, `sqlite3`, JSONL, `hashlib`, `argparse`, existing Phase 4 builders/tests, existing Ghidra headless scripts, optional Cpp2IL CLI, existing Python `unittest` suite, tokenizer measurement available in the workspace

## Global Constraints

- ห้ามแก้ `game-dev-story-mod_Sprites/`, `game-dev-story-mod_Dumped/`, `game-dev-story-mod_Extracted/` หรือ Ghidra project
- generated artifacts ต้องอยู่ใต้ `Phases/Phase4/artifacts/corpus/` และเอกสารใต้ `Phases/Phase4/docs/` หรือ `Docs/superpowers/`
- Phase 4 historical artifacts ห้าม overwrite; current status ใช้ `cross_wave_gap_reconciliation.json` และ supersession links
- raw/annotated/normalized/compressed views ต้องมี input hash และ source map; compressed view ห้ามเป็น evidence source
- candidate AI output ต้องติดสถานะ `candidate` จนกว่า source validator และ fixture/contract gate จะผ่าน
- tool ที่ไม่มีในเครื่องต้องรายงาน `not_available` แบบ deterministic และไม่หยุด builder ทั้งชุด
- ห้ามสร้าง TypeScript runtime ในแผนนี้; P0-B ใช้ output หลัง corpus handoff เท่านั้น
- ทุก task ต้องมี deterministic test หรือ manifest check และต้องตรวจ `git diff --check`

---

## Execution order and parallelism

แผนนี้แบ่งเป็น `P0-A0` ถึง `P0-A9` รวม 10 task แต่ไม่ใช่ 10 งานที่รันพร้อมกันทั้งหมด:

- `A0` เป็น strict gate เดียว ต้อง freeze source/artifact baseline ให้เสร็จก่อน task ที่อ่าน corpus
- critical path คือ `A0 → A1 → A2 → A3 → A4 → A6 → A7 → A8 → A9`
- หลัง `A2` แล้ว `A3` (lossless views) และ `A5` (cross-tool adapters/comparison) ทำเป็น parallel lanes ได้ เพราะเขียนคนละ output และใช้ canonical identity ร่วมกัน
- โครง adapter/test ของ `A5` เริ่มคู่กับ `A1/A2` ได้ถ้าใช้ fixtures แยก แต่การรัน comparison รวมกับ corpus ต้องรอ `A2`
- `A6` ต้องรอ `A2`, `A3`, `A4` และ `A5` เพราะ pilot ต้องวัด index, source map, prompt view และ conflict พร้อมกัน
- `A7` สร้าง provider/cache/schema boundary ล่วงหน้าได้หลัง schema ของ `A3/A4` ชัด แต่สร้าง pilot requests จริงหลัง `A6` เท่านั้น
- `A8` แยกทำ query CLI และ validator tests คู่กับ `A6/A7` ได้ แต่ promotion gate ต้องรอ candidate และ pilot artifacts ครบ
- `A9` เป็น final barrier ต้องรอ `A0–A8`, regression suite และ `--check` ทั้งหมดผ่าน

กติกาการทำขนาน:

1. ขนานได้เฉพาะงานที่มี input hash/contract ชัดและเขียน output คนละ path หรือใช้ temporary output แล้ว merge ที่ gate
2. ห้ามให้ builder สองตัวเขียน `manifest.json`, `corpus_index.sqlite` หรือ closure report พร้อมกัน
3. ทุก lane ต้อง commit/ส่งผลผ่าน focused tests ของตัวเองก่อน merge เข้า gate ถัดไป
4. ถ้า schema หรือ stable `unit_id` เปลี่ยน ให้หยุด lanes ที่พึ่งพาและ rerun ตั้งแต่ `A2` ตาม incremental hash

| Task | ต้องรอ | ทำขนานกับ | ผลที่ปล่อยให้ task ถัดไป |
|---|---|---|---|
| A0 | ไม่มี | ไม่มี | baseline manifest และ source hashes |
| A1 | A0 | A5 adapter fixtures ได้ | imported Phase 4–6 evidence |
| A2 | A1 | A5 adapter development ได้ | canonical JSONL/SQLite identity/index |
| A3 | A2 | A5 | raw/annotated/normalized views และ source maps |
| A4 | A3 | A5 | prompt views และ token metrics |
| A5 | A0; integrated run รอ A2 | A3/A4 | comparison/conflict records |
| A6 | A2–A5 | ไม่มีใน execution | pilot manifest/report 100 functions |
| A7 | A6 สำหรับ batch จริง | A8 validator/query scaffolding | cached candidate requests/responses |
| A8 | A2, A5–A7 สำหรับ promotion | A7 scaffolding | validation, promotion และ negative evidence |
| A9 | A0–A8 | ไม่มี | closure report และ P0-B handoff |

---

### Task 0: Freeze corpus baseline and execution manifest

**Files:**
- Create: `Phases/Phase4/tools/build_corpus_manifest.py`
- Create: `Phases/Phase4/tests/test_corpus_manifest.py`
- Create: `Phases/Phase4/artifacts/corpus/manifest.json`
- Create: `Phases/Phase4/docs/corpus_baseline_report.md`
- Read: `Phases/Phase0/artifacts/phase0_baseline.json`
- Read: `Phases/Phase4/artifacts/wave0_build_manifest.json`
- Read: `Phases/Phase5/artifacts/wave5_build_manifest.json`
- Read: `Phases/Phase6/artifacts/wave6_build_manifest.json`

**Interfaces:**
- `build_corpus_manifest.py --output <dir> --check` writes source/artifact hashes, byte/line/function counts, schema versions and read-only policy
- `manifest.json` contains `source_roots_read_only`, `source_files`, `artifact_inputs`, `counts`, `tool_versions`, `supersedes` and `status`
- `--check` exits non-zero when a source hash or generated count differs from the recorded baseline

- [ ] **Step 1: Write the failing tests** for required source roots, Phase 4/5/6 artifact inputs, stable hash fields and `--check` mismatch behavior
- [ ] **Step 2: Run `python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v` and confirm failure because the builder/artifact do not exist**
- [ ] **Step 3: Implement the manifest builder** using streaming SHA-256 and explicit `Path` roots; do not scan or mutate generated output recursively without a declared allowlist
- [ ] **Step 4: Run the builder twice** and assert identical hashes/counts except for a separate generation timestamp field
- [ ] **Step 5: Write the baseline report** with measured local corpus values and the external-tool availability table
- [ ] **Step 6: Run the test and `git diff --check`**
- [ ] **Step 7: Commit** with message `docs: freeze corpus intelligence baseline`

### Task 1: Import Phase 4 evidence and current gap reconciliation

**Files:**
- Create: `Phases/Phase4/tools/build_corpus_evidence_import.py`
- Create: `Phases/Phase4/tests/test_corpus_evidence_import.py`
- Create: `Phases/Phase4/artifacts/corpus/phase4_evidence_index.json`
- Create: `Phases/Phase4/docs/corpus_phase4_handoff.md`
- Read: `Phases/Phase4/artifacts/function_inventory.json`
- Read: `Phases/Phase4/artifacts/field_offset_map.json`
- Read: `Phases/Phase4/artifacts/office_runtime_call_graph.json`
- Read: `Phases/Phase4/artifacts/translation_coverage.json`
- Read: `Phases/Phase4/artifacts/cross_wave_gap_reconciliation.json`
- Read: `Phases/Phase4/artifacts/targeted_gap_scan.json`
- Read: `Phases/Phase4/artifacts/semantic_gap_trace.json`

**Interfaces:**
- `build_corpus_evidence_import.py --check` produces one import record per existing artifact with schema, hash, scope, status and supersession relationship
- Evidence records expose `source_refs`, `legacy_facts`, `web_adapter_decisions`, `unknown_boundaries` and `open_gaps` as separate arrays
- Historical registers remain byte-for-byte unchanged

- [ ] **Step 1: Write tests** requiring the 88-unit inventory, 1,850-field map, 277/359 graph summary, current reconciliation and Phase 4 regression references
- [ ] **Step 2: Run the focused test and confirm failure because the import artifact does not exist**
- [ ] **Step 3: Implement deterministic import** that reads only declared artifacts and marks later evidence as superseding stale historical status
- [ ] **Step 4: Add a test for the known Wave 5/6 supersession groups** so the builder does not reopen already bounded closures
- [ ] **Step 5: Run Phase 4 reconciliation/targeted/semantic tests plus the new import test**
- [ ] **Step 6: Commit** with message `feat: import phase evidence into corpus index`

### Task 2: Build the canonical function, field and edge index

**Files:**
- Create: `Phases/Phase4/tools/build_corpus_index.py`
- Create: `Phases/Phase4/tools/corpus_index_schema.py`
- Create: `Phases/Phase4/tests/test_corpus_index.py`
- Create: `Phases/Phase4/artifacts/corpus/functions.jsonl`
- Create: `Phases/Phase4/artifacts/corpus/edges.jsonl`
- Create: `Phases/Phase4/artifacts/corpus/corpus_index.sqlite`
- Modify: `Phases/Phase4/tools/build_wave0_index.py` only when a shared parser helper is extracted without changing historical output

**Interfaces:**
- `canonical_unit_id(source_hash, symbol, address_namespace, address, line_start, line_end) -> str`
- `build_corpus_index.py --scope all --output <dir> --check`
- `functions.jsonl` records contain `unit_id`, symbol, namespace/class, signature, addresses, source refs, availability, fields, strings, resources, status and confidence
- `edges.jsonl` records contain `edge_id`, `kind`, `caller`, `callee/target`, evidence refs and confidence
- SQLite tables `functions`, `fields`, `edges`, `strings`, `resources`, `artifacts`, `failures` have indexes on `unit_id`, symbol, address and edge kind

- [ ] **Step 1: Write tests** for stable IDs, duplicate symbols, address namespace delta, multiline function headers, assembly-only functions and explicit parse failures
- [ ] **Step 2: Run the focused test and confirm failure because canonical stores do not exist**
- [ ] **Step 3: Implement streaming parsers** for `dump.cs`, `script.json`, `stringliteral.json`, categorized C, assembly reports and imported Phase 4 records
- [ ] **Step 4: Build SQLite/JSONL output** transactionally through temporary files and replace only declared generated targets after successful validation
- [ ] **Step 5: Add FTS5 queries** for symbol/source/field/string search and a CLI query mode that prints source refs and status
- [ ] **Step 6: Run builder twice and compare canonical output hashes**
- [ ] **Step 7: Run Wave 0 tests and the new corpus-index tests**
- [ ] **Step 8: Commit** with message `feat: add canonical corpus evidence index`

### Task 3: Implement lossless annotation views

**Files:**
- Create: `Phases/Phase4/tools/annotate_views.py`
- Create: `Phases/Phase4/tools/view_source_map.py`
- Create: `Phases/Phase4/tests/test_annotation_views.py`
- Create: `Phases/Phase4/artifacts/corpus/views/`
- Read: root `Auto_Annotator.py` as a compatibility reference only
- Read: `Phases/Phase4/artifacts/field_offset_map.json`
- Read: `Phases/Phase4/artifacts/corpus/functions.jsonl`

**Interfaces:**
- `annotate_views.py --input <raw-file> --function <unit-id> --view annotated --output <dir>`
- `annotate_views.py --scope pilot --view annotated --output <dir>`
- `view_source_map.py reconstruct --view <path> --output <path>`
- annotation records retain raw expression, resolved field candidate, declaring class/namespace, offset, evidence refs and `resolution_status`

- [ ] **Step 1: Write tests** for instance/static fields, namespace collisions, unresolved class headers, non-`param_1` receivers, multiline blocks and unchanged raw hash
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement function segmentation** from canonical function records instead of global regex state
- [ ] **Step 4: Implement context-aware field resolution** with ambiguity preserved as a record; never silently carry the previous class context
- [ ] **Step 5: Emit `raw`, `annotated` and `source_map` records** without overwriting raw source
- [ ] **Step 6: Implement reconstruction and verify reconstructed SHA-256 equals the raw input**
- [ ] **Step 7: Run annotation tests and `git diff --check`**
- [ ] **Step 8: Commit** with message `feat: add lossless corpus annotation views`

### Task 4: Build prompt-compressed views without semantic deletion

**Files:**
- Create: `Phases/Phase4/tools/build_prompt_view.py`
- Create: `Phases/Phase4/tests/test_prompt_views.py`
- Create: `Phases/Phase4/artifacts/corpus/views/prompt/`
- Read: `Smart_Compressor.py` as a compatibility reference only
- Read: `Phases/Phase4/tools/annotate_views.py`

**Interfaces:**
- `build_prompt_view.py --input <annotated-view> --output <dir> --profile candidate-summary`
- `ViewRecord` includes raw input hash, output hash, omitted ranges, collapsed ranges, dedup fingerprints, rules and tokenizer counts
- compression profiles are explicit: `compact-whitespace`, `candidate-summary`, `deep-analysis`; no profile mutates canonical evidence

- [ ] **Step 1: Write tests** for blank-line collapse, boilerplate grouping, address retention in source map, omitted-range recording and exact reconstruction
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement non-destructive transformations** that replace text only in the prompt view and record every omitted/collapsed range
- [ ] **Step 4: Add repeated-block fingerprints** so identical boilerplate is represented once in the prompt plus references to all source spans
- [ ] **Step 5: Measure lines, characters and tokenizer tokens** for raw/annotated/prompt views; do not report estimated reduction
- [ ] **Step 6: Run reconstruction and determinism tests**
- [ ] **Step 7: Commit** with message `feat: add provenance-preserving prompt views`

### Task 5: Add cross-tool comparison adapters

**Files:**
- Create: `Phases/Phase4/tools/compare_il2cpp_tools.py`
- Create: `Phases/Phase4/tests/test_il2cpp_tool_comparison.py`
- Create: `Phases/Phase4/artifacts/corpus/tool_comparison.json`
- Read: `game-dev-story-mod_Dumped/ghidra_headless.py`
- Read: `game-dev-story-mod_Dumped/ghidra_export_c.py`
- Read: Il2CppDumper outputs and optional Cpp2IL export directory

**Interfaces:**
- `compare_il2cpp_tools.py --ghidra <report> --dumper <dir> --cpp2il <dir> --output <path>`
- missing tools produce `availability: not_available`, not a fatal error
- comparison rows contain symbol/address, tool observations, agreement/conflict fields, source refs and `status`

- [ ] **Step 1: Write tests** for available, unavailable, same-symbol, address-delta and conflicting-field cases using local fixtures
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement adapters** for current Ghidra reports and Il2CppDumper metadata without importing external code into source roots
- [ ] **Step 4: Add optional Cpp2IL adapter** that reads ISIL/CFG/method-dump outputs when the executable is present
- [ ] **Step 5: Emit conflict records** and prohibit automatic winner selection
- [ ] **Step 6: Run comparison tests and record actual tool availability in the corpus baseline**
- [ ] **Step 7: Commit** with message `feat: compare il2cpp analysis outputs`

### Task 6: Run and evaluate the 100-function pilot

**Files:**
- Create: `Phases/Phase4/tools/build_corpus_pilot.py`
- Create: `Phases/Phase4/tests/test_corpus_pilot.py`
- Create: `Phases/Phase4/artifacts/corpus/pilot_manifest.json`
- Create: `Phases/Phase4/docs/corpus_pilot_report.md`
- Read: `Phases/Phase4/artifacts/function_inventory.json`
- Read: `Phases/Phase4/artifacts/corpus/corpus_index.sqlite`

**Interfaces:**
- `build_corpus_pilot.py --count 100 --output <dir>` selects 40 office units, 30 direct dependencies, 20 large/assembly-related units and 10 out-of-scope units deterministically
- pilot manifest records selection reason, unit IDs, input/view hashes, token counts, parse/annotation conflicts and tool availability
- pilot report has `pass`, `blocked`, `unknown`, `not_available`, `coverage`, `losslessness`, `determinism` and `token_measurement` sections

- [ ] **Step 1: Write tests** for deterministic selection, category quotas and exclusion of duplicate unit IDs
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement pilot selection** from canonical index and Phase 4 shortlist, with stable tie-break by unit ID
- [ ] **Step 4: Run annotation, prompt-view and comparison builders over the pilot**
- [ ] **Step 5: Measure actual source/view/token counts** and record every conflict instead of hiding it
- [ ] **Step 6: Write the pilot report** with explicit pass/fail gate and no forecast presented as a result
- [ ] **Step 7: Run all Phase 4 tests plus pilot tests**
- [ ] **Step 8: Commit** with message `test: evaluate corpus intelligence pilot`

### Task 7: Add cached candidate logic-map generation

**Files:**
- Create: `Phases/Phase4/tools/build_translation_requests.py`
- Create: `Phases/Phase4/tools/translation_provider.py`
- Create: `Phases/Phase4/tools/validate_candidate_schema.py`
- Create: `Phases/Phase4/tests/test_translation_requests.py`
- Create: `Phases/Phase4/artifacts/corpus/candidates/`
- Read: `Phases/Phase4/artifacts/corpus/pilot_manifest.json`

**Interfaces:**
- `build_translation_requests.py --input <unit/query> --profile candidate-summary --output <dir>` emits compact request JSON with source refs and context budget
- `TranslationProvider.translate(request) -> response` is provider-neutral; an offline fixture provider is required for tests
- cache key is `sha256(unit_id + input_view_hash + prompt_version + schema_version + model_id)`
- candidate schema requires `symbol`, `source_refs`, `reads`, `writes`, `calls`, `branches`, `unknowns`, `pseudocode`, `confidence: candidate`

- [ ] **Step 1: Write tests** for request construction, context ordering, cache hit/miss, schema rejection and offline provider output
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement provider-neutral request/cache layer** without embedding API keys or provider-specific assumptions in artifacts
- [ ] **Step 4: Add compact context assembly** from function, callers/callees, fields, strings, resources and relevant Phase 4 evidence
- [ ] **Step 5: Validate candidate JSON** and store invalid responses with raw response hash and rejection reason
- [ ] **Step 6: Generate pilot requests in dry-run mode** and measure input/output tokens before any large batch
- [ ] **Step 7: Run tests and `git diff --check`**
- [ ] **Step 8: Commit** with message `feat: add cached candidate translation requests`

### Task 8: Validate, promote and query knowledge records

**Files:**
- Create: `Phases/Phase4/tools/validate_corpus_claims.py`
- Create: `Phases/Phase4/tools/query_corpus.py`
- Create: `Phases/Phase4/tests/test_corpus_validation.py`
- Create: `Phases/Phase4/artifacts/corpus/validation/`
- Create: `Phases/Phase4/docs/corpus_query_guide.md`

**Interfaces:**
- `validate_corpus_claims.py --candidate <path> --index <sqlite> --fixtures <dir>` emits claim-level validation and promotion status
- `query_corpus.py function <symbol>`, `query_corpus.py field <class.field>`, `query_corpus.py edge <symbol>` print source refs, current status and superseded evidence
- promotion statuses are `source_validated`, `fixture_verified`, `blocked`, `out_of_scope`, `web_adapter_decision`
- negative-evidence records include search scope, patterns, source/artifact hashes, conclusion and reopen trigger

- [ ] **Step 1: Write tests** for missing field/call/source refs, valid claims, fixture promotion, conflict retention and negative-evidence persistence
- [ ] **Step 2: Run the focused test and confirm failure**
- [ ] **Step 3: Implement claim validators** against canonical SQLite/JSONL and imported Phase 4 evidence
- [ ] **Step 4: Implement fixture/contract promotion** with explicit `legacy_fact` versus `web_adapter_decision` namespaces
- [ ] **Step 5: Implement query commands** for future investigations so existing evidence is reused before new tracing
- [ ] **Step 6: Run Phase 2/4/5/6 regression suites and corpus validation tests**
- [ ] **Step 7: Commit** with message `feat: validate and query corpus knowledge`

### Task 9: Close P0-A and hand off to downstream phases

**Files:**
- Create: `Phases/Phase4/tools/build_corpus_closure.py`
- Create: `Phases/Phase4/tests/test_corpus_closure.py`
- Create: `Phases/Phase4/artifacts/corpus/closure_report.json`
- Create: `Phases/Phase4/docs/corpus_closure_report.md`
- Modify: `TODO.md`
- Modify: `PROJECT_STATE.md`
- Modify: `Docs/AI_Agent_Office_Roadmap.md`
- Modify: `Phases/Phase4/README.md`
- Modify: `Phases/README.md`
- Modify: `Docs/superpowers/plans/2026-08-12-office-typescript-port.md`

**Interfaces:**
- closure report records source counts, indexed counts, pilot metrics, candidate/validated/promoted counts, conflicts, open gaps, tool availability and exact regression commands/results
- P0-B status may change from `blocked_on_corpus_gate` only when closure report and all Gate A–F checks pass
- every remaining gap has status, owner, next action and reopen trigger

- [ ] **Step 1: Write closure tests** requiring manifest, evidence import, canonical index, source-map checks, pilot report, validation report and regression references
- [ ] **Step 2: Run the focused closure test and confirm failure**
- [ ] **Step 3: Implement deterministic closure builder** and fail when required artifacts are missing or source hashes drift
- [ ] **Step 4: Update TODO/state/roadmap/README** so P0-A is urgent and P0-B/other phases are downstream without deleting historical completion records
- [ ] **Step 5: Run all Phase 2/4/5/6 tests, corpus tests, `--check` builders and `git diff --check`**
- [ ] **Step 6: Write the exact handoff** naming the first P0-B task and the query commands for future phase work
- [ ] **Step 7: Commit** with message `docs: close corpus intelligence gate and reorder roadmap`

## Verification commands

```powershell
python -m unittest discover -s Phases/Phase4/tests -p "test_corpus_*.py"
python -m unittest discover -s Phases/Phase4/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase2/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase5/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase6/tests -p "test_*.py"
python Phases/Phase4/tools/build_corpus_manifest.py --check
python Phases/Phase4/tools/build_corpus_index.py --scope all --check
python Phases/Phase4/tools/build_corpus_closure.py --check
git diff --check
```
