# P0-A0 Corpus Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** สร้าง baseline manifest ที่ตรึง source roots และ evidence artifacts ของ corpus ปัจจุบันด้วย SHA-256, canonical fingerprint, counts และ tool availability เพื่อให้ทุกงาน P0-A ถัดไปตรวจ drift ได้ก่อนอ่านหรือสร้าง evidence ใหม่

**Architecture:** ใช้ deterministic Python builder อ่านไฟล์แบบ read-only, normalize path เป็น relative POSIX path และสร้าง record ต่อไฟล์จาก size, SHA-256 และ line count โดยแยก source files กับ Phase artifacts ชัดเจน. Manifest จะมี fingerprint ที่คำนวณจาก sorted file records เท่านั้น จึงไม่เปลี่ยนเมื่อเวลา/absolute workspace path เปลี่ยน; รายงาน Markdown ใช้สรุปผลตรวจและ known limitations แต่ไม่เป็น source of truth แยกจาก manifest.

**Tech Stack:** Python 3.10+, pathlib, hashlib, json, argparse, shutil.which, tempfile, unittest, existing Phase 0/4/5/6 JSON manifests

## Global Constraints

- ห้ามแก้ game-dev-story-mod_Sprites/, game-dev-story-mod_Dumped/, game-dev-story-mod_Extracted/ หรือ Ghidra project
- generated artifacts ต้องอยู่ใต้ Phases/Phase4/artifacts/corpus/ และเอกสารใต้ Phases/Phase4/docs/ หรือ Docs/superpowers/
- Phase 4 historical artifacts ห้าม overwrite; current status ใช้ cross_wave_gap_reconciliation.json และ supersession links
- raw/annotated/normalized/compressed views ต้องมี input hash และ source map; compressed view ห้ามเป็น evidence source
- candidate AI output ต้องติดสถานะ candidate จนกว่า source validator และ fixture/contract gate จะผ่าน
- tool ที่ไม่มีในเครื่องต้องรายงาน not_available แบบ deterministic และไม่หยุด builder ทั้งชุด
- ห้ามสร้าง TypeScript runtime ในแผนนี้; P0-B ใช้ output หลัง corpus handoff เท่านั้น
- ทุก task ต้องมี deterministic test หรือ manifest check และต้องตรวจ git diff --check

---

## 1. ขอบเขตที่ล็อกไว้สำหรับ A0

### ทำใน A0

1. ตรวจว่าขอบเขต input ที่ประกาศไว้มีอยู่จริงและอยู่ใต้ workspace root
2. Hash ไฟล์ทุกไฟล์ใน source roots ปัจจุบันแบบ recursive
3. Hash Phase 0/4/5/6 artifacts ที่จะถูกใช้เป็น evidence input โดยไม่รวม output ของ corpus เอง
4. เก็บ byte count, line count สำหรับ text, extension summary, root summary และ function/code counts ที่อ้างจาก manifest/report เดิม
5. ตรวจ availability ของ optional analysis tools แบบไม่ทำให้ baseline ล้มเมื่อ tool ไม่มี
6. สร้าง manifest.json และ corpus_baseline_report.md
7. เพิ่ม --check สำหรับตรวจ source/artifact drift, missing file, added file, removed file และ count drift
8. ทำให้ rerun ได้ผล canonical fingerprint เดิมเมื่อ input ไม่เปลี่ยน

### ห้ามทำใน A0

- ห้าม parse function ทั้ง corpus เพื่อสร้าง canonical index; งานนั้นคือ A2
- ห้าม import/merge evidence records; งานนั้นคือ A1
- ห้ามสร้าง raw/annotated/prompt views; งานนั้นคือ A3/A4
- ห้ามเรียก Cpp2IL หรือส่ง request ไป provider; งานนั้นคือ A5/A7
- ห้ามแก้ historical manifest, gap register, source extraction หรือ runtime
- ห้าม mark P0-B ว่าเริ่มได้จากการมี baseline เพียงอย่างเดียว

## 2. หลักฐานปัจจุบันที่ต้อง reconcile

ค่าด้านล่างเป็น evidence ตั้งต้นจากไฟล์จริง ไม่ใช่ค่าที่ให้ hardcode แทนการ scan. หลัง builder ทำงานต้องบันทึกค่าที่วัดได้จริง และถ้าไม่ตรงต้องแสดง drift/attention ใน report:

| ขอบเขต | จำนวนไฟล์ | ขนาดรวมโดยประมาณ | แหล่งอ้างอิงปัจจุบัน |
|---|---:|---:|---|
| game-dev-story-mod_Sprites/ | 445 | 12,376,079 bytes | Phases/Phase0/artifacts/phase0_baseline.json |
| game-dev-story-mod_Dumped/ | 208 | 2,452,540,798 bytes | Phases/Phase0/artifacts/phase0_baseline.json |
| game-dev-story-mod_Extracted/ | 1,226 | 96,455,046 bytes | Phases/Phase0/artifacts/phase0_baseline.json |
| Phases/Phase0/artifacts/ | 5 | 284,884 bytes | local file scan |
| Phases/Phase4/artifacts/ ยกเว้น corpus/ | 73 | 21,506,954 bytes | local file scan |
| Phases/Phase5/artifacts/ | 23 | 2,208,138 bytes | local file scan |
| Phases/Phase6/artifacts/ | 11 | 15,651 bytes | local file scan |

Function coverage ที่ต้องเก็บเป็น derived evidence คือ 110,824 total functions, 110,819 main successful, 5 original failures, 1 recovery-added, 110,820 combined C functions, 4 C-only remaining และ assembly fallback 5/5 ตาม Phase 0 baseline. ห้ามตีความตัวเลขเหล่านี้เป็น semantic closure.

Known attention ที่ report ต้องคงไว้:

- extraction report ระบุ output เดิมเป็น game-dev-story-mod_Sprites_fixed แต่ current root คือ game-dev-story-mod_Sprites
- extraction report มี UTF-8 warning เดิม 3 รายการ แม้ current CSV bytes ผ่าน validation
- recovered C ยังขาด 4 functions และ assembly fallback ครอบคลุม failed-function list 5 รายการ
- log บางไฟล์มี absolute path เดิมใต้ APK_Toolkit; ให้เก็บเป็น provenance note ไม่แก้ log

## 3. File map และ input boundary

### Files ที่ต้องสร้างหรือแก้

- Create: Phases/Phase4/tools/build_corpus_manifest.py
- Create: Phases/Phase4/tests/test_corpus_manifest.py
- Create: Phases/Phase4/artifacts/corpus/manifest.json
- Create: Phases/Phase4/docs/corpus_baseline_report.md
- Modify: TODO.md เพิ่มลิงก์ไปยังแผน A0 นี้เมื่อแผนถูกบันทึก
- Modify: PROJECT_STATE.md เพิ่มไฟล์แผนนี้ บันทึก actual baseline outputs และชี้งานถัดไปไป P0-A1

### Files/roots ที่ต้องอ่านแบบ read-only

~~~python
SOURCE_ROOTS = {
    "sprites": "game-dev-story-mod_Sprites",
    "dumped": "game-dev-story-mod_Dumped",
    "extracted": "game-dev-story-mod_Extracted",
}

ARTIFACT_ROOTS = {
    "phase0_artifacts": "Phases/Phase0/artifacts",
    "phase4_artifacts": "Phases/Phase4/artifacts",
    "phase5_artifacts": "Phases/Phase5/artifacts",
    "phase6_artifacts": "Phases/Phase6/artifacts",
}

EXCLUDED_GENERATED_ROOT = "Phases/Phase4/artifacts/corpus"
~~~

phase4_artifacts ต้อง exclude Phases/Phase4/artifacts/corpus/ แบบ path-component comparison ไม่ใช่ string prefix อย่างเดียว เพื่อไม่ให้ manifest hash ตัวเองหรือ output รอบก่อนกลายเป็น input ของรอบถัดไป. ไม่ต้อง scan ghidra_11.0.1_PUBLIC/, .git/, APK_Toolkit/ หรือ viewer/ เพราะเป็น tooling/operational directory นอก corpus input boundary นี้.

### CLI contract

~~~text
python Phases/Phase4/tools/build_corpus_manifest.py --root . --output Phases/Phase4/artifacts/corpus --report Phases/Phase4/docs/corpus_baseline_report.md

python Phases/Phase4/tools/build_corpus_manifest.py --root . --output Phases/Phase4/artifacts/corpus --check
~~~

- build mode สร้าง/แทนที่เฉพาะ manifest.json ใน output directory และ report ที่ระบุ
- --check อ่าน baseline เดิม ไม่แก้ manifest/report และคืน exit code 0 เมื่อผ่าน
- exit code 2 หมายถึง source/artifact drift
- exit code 3 หมายถึง baseline หรือ required input หาย/อ่านไม่ได้/โครงสร้างไม่ถูก schema
- exit code 4 หมายถึง output path ไม่ปลอดภัย เช่น อยู่ใน input root หรือ resolve ออกนอก workspace
- --root ต้อง resolve เป็น workspace root ที่มี AGENTS.md, source roots และ Phases/


## 4. Manifest schema ที่ต้องยึด

สร้าง schema version คงที่ชื่อ p0-a0.corpus-baseline.v1. ห้ามใส่ absolute path ใน canonical records. generated_at_utc, Python version และ machine-local executable path เก็บได้ใน metadata แต่ไม่รวมใน fingerprint.

Manifest ระดับบนสุดต้องมี:

- schema: p0-a0.corpus-baseline.v1
- generated_at_utc
- workspace_policy: source_roots_read_only, path_format, hash_algorithm, fingerprint_basis และ excluded_generated_roots
- source_roots
- artifact_inputs
- derived_counts
- external_tools
- checks
- known_limitations
- snapshot_fingerprint

แต่ละ source root ต้องมี id, path, exists, file_count, total_bytes, total_lines, by_extension, tree_sha256 และ status. แต่ละ artifact input ต้องมี path, exists, bytes, sha256, schema, status, role และ supersedes โดยใช้ null/unknown เมื่ออ่าน schema ไม่ได้ ห้ามเดา.

Canonical file record ต้องมี path, root_id, role, exists, bytes, sha256, line_count, text_encoding และ is_binary. ให้เก็บ file records ใน source_files และ artifact_files เป็น arrays ที่ sort ด้วย path; อย่าใช้ filesystem enumeration order. line_count ต้องเป็น null สำหรับ binary และเป็นจำนวน newline ที่ normalize แบบ binary-safe สำหรับ text; ไม่ต้องเขียนไฟล์ source กลับด้วย encoding ใหม่.

ตัวอย่างโครงสร้างระดับบนสุด:

~~~json
{
  "schema": "p0-a0.corpus-baseline.v1",
  "generated_at_utc": "2026-08-12T00:00:00Z",
  "workspace_policy": {
    "source_roots_read_only": true,
    "path_format": "workspace-relative-posix",
    "hash_algorithm": "sha256",
    "fingerprint_basis": "sorted(path, size_bytes, sha256)",
    "excluded_generated_roots": ["Phases/Phase4/artifacts/corpus"]
  },
  "source_roots": [],
  "artifact_inputs": [],
  "derived_counts": {},
  "external_tools": [],
  "checks": [],
  "known_limitations": [],
  "snapshot_fingerprint": ""
}
~~~

ตัวอย่าง canonical file record:

~~~json
{
  "path": "game-dev-story-mod_Dumped/dump.cs",
  "root_id": "dumped",
  "role": "source",
  "exists": true,
  "bytes": 12013789,
  "sha256": "bcdd145720a0124c641c6b80d959cca0ad2810e04147400f9003e96310c40074",
  "line_count": 0,
  "text_encoding": "utf-8-or-replacement",
  "is_binary": false
}
~~~


## 5. Canonical hashing และ drift algorithm

### File hash

อ่านทุกไฟล์เป็น binary chunks ขนาด 1 MiB และคำนวณ SHA-256. ห้ามใช้ read_text() กับ source file ทั้งก้อน เพราะ Dumped มีไฟล์ขนาดใหญ่และมี binary assets.

~~~python
def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
~~~

### Tree fingerprint

ใช้ path ที่ normalize เป็น /, sort แบบ byte-stable และ concatenate record โดยไม่รวม mtime, absolute path หรือ generation time:

~~~python
def tree_fingerprint(records: list[dict[str, object]]) -> str:
    rows = []
    for record in sorted(records, key=lambda item: str(item["path"])):
        rows.append(
            f'{record["path"]}{chr(0)}{record["bytes"]}{chr(0)}{record["sha256"]}{chr(10)}'.encode("utf-8")
        )
    return hashlib.sha256(b"".join(rows)).hexdigest()
~~~

source_tree_sha256 คำนวณแยกต่อ root และ snapshot_fingerprint คำนวณจากทุก source/artifact record รวมกันโดยใส่ role/root_id ใน row เพื่อไม่ให้ path ที่ซ้ำกันข้าม namespace ชนกัน. ใน --check ต้องรายงาน added, removed, changed, count_deltas และ fingerprint_changed; ห้ามรายงานแค่ boolean เดียว.

### Path safety

ก่อน scan ให้ resolve ทุก input/output path และตรวจ is_relative_to(root). ถ้า output อยู่ใต้ source root, ถ้ามี symlink ที่ resolve ออกนอก workspace หรือถ้า required root หาย ให้หยุดด้วย exit code 4/3 ตามกรณี. ห้ามสร้าง missing source root ให้อัตโนมัติ.


## 6. แผนลงมือทำทีละ task

### Task A0.1: Lock input boundary และเขียน failing tests

**Files:**

- Create: Phases/Phase4/tests/test_corpus_manifest.py
- Read: Phases/Phase0/artifacts/phase0_baseline.json
- Read: Phases/Phase4/artifacts/wave0_build_manifest.json
- Read: Phases/Phase5/artifacts/wave5_build_manifest.json
- Read: Phases/Phase6/artifacts/wave6_build_manifest.json

**Interfaces:**

- Tests will import build_manifest, scan_inputs, tree_fingerprint, compare_snapshot and main from build_corpus_manifest.py.
- Test fixtures use a temporary workspace with the same relative root names, so tests never hash the 2.6 GB local Dumped root.

- [x] **Step 1: สร้าง test constants และ temporary fixture** ให้มี game-dev-story-mod_Sprites/a.txt, game-dev-story-mod_Dumped/dump.cs, game-dev-story-mod_Extracted/assets/data.bin, Phases/Phase0/artifacts/phase0_baseline.json, Phases/Phase4/artifacts/wave0_build_manifest.json และ Phases/Phase4/artifacts/corpus/old-output.json

~~~python
class CorpusManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in (
            "game-dev-story-mod_Sprites",
            "game-dev-story-mod_Dumped",
            "game-dev-story-mod_Extracted",
            "Phases/Phase0/artifacts",
            "Phases/Phase4/artifacts",
            "Phases/Phase4/docs",
        ):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "game-dev-story-mod_Sprites/a.txt").write_bytes(b"alpha\n")
        (self.root / "game-dev-story-mod_Dumped/dump.cs").write_bytes(b"// Function: demo\n")
        (self.root / "game-dev-story-mod_Extracted/assets/data.bin").write_bytes(b"\x00\x01\x02")
        (self.root / "Phases/Phase0/artifacts/phase0_baseline.json").write_text(
            '{"schema": 1}\n', encoding="utf-8"
        )
        (self.root / "Phases/Phase4/artifacts/wave0_build_manifest.json").write_text(
            '{"schema": "phase4.wave0.index-build.v1"}\n', encoding="utf-8"
        )
        (self.root / "Phases/Phase4/artifacts/corpus/old-output.json").parent.mkdir(
            parents=True, exist_ok=True
        )
        (self.root / "Phases/Phase4/artifacts/corpus/old-output.json").write_text(
            "generated output\n", encoding="utf-8"
        )
~~~

- [x] **Step 2: เขียน failing tests** สำหรับ required roots, output exclusion, relative POSIX paths, binary/text classification และ sorted records

~~~python
def test_scan_uses_declared_roots_and_excludes_corpus_output(self):
    records = scan_inputs(self.root)
    paths = [row["path"] for row in records["artifact_files"]]
    self.assertIn("Phases/Phase4/artifacts/wave0_build_manifest.json", paths)
    self.assertNotIn("Phases/Phase4/artifacts/corpus/old-output.json", paths)
    self.assertEqual(paths, sorted(paths))

def test_binary_line_count_is_null_and_text_line_count_is_stable(self):
    records = scan_inputs(self.root)["source_files"]
    by_path = {row["path"]: row for row in records}
    self.assertEqual(by_path["game-dev-story-mod_Sprites/a.txt"]["line_count"], 1)
    self.assertIsNone(by_path["game-dev-story-mod_Extracted/assets/data.bin"]["line_count"])
~~~

- [x] **Step 3: รัน focused test เพื่อยืนยัน failure**

Run: python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v

Expected: FAIL เพราะ Phases/Phase4/tools/build_corpus_manifest.py ยังไม่มีอยู่หรือยังไม่มี interfaces ที่ test เรียก.

### Task A0.2: Implement read-only scanner และ canonical records

**Files:**

- Create: Phases/Phase4/tools/build_corpus_manifest.py
- Test: Phases/Phase4/tests/test_corpus_manifest.py

**Interfaces:**

~~~python
def scan_inputs(root: Path) -> dict[str, list[dict[str, object]]]:
    """Return sorted source_files and artifact_files for the declared input boundary."""

def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest of one file read as binary chunks."""

def tree_fingerprint(records: list[dict[str, object]]) -> str:
    """Return the canonical digest of sorted path/size/hash records."""

def build_manifest(root: Path, generated_at_utc: str | None = None) -> dict[str, object]:
    """Return one p0-a0.corpus-baseline.v1 manifest without writing input files."""

def compare_snapshot(root: Path, baseline: dict[str, object]) -> dict[str, object]:
    """Return pass or drift plus added, removed, changed and count-delta details."""

def main(argv: list[str] | None = None) -> int:
    """Parse build/check arguments, write only declared outputs, and return the CLI code."""
~~~

- [x] **Step 1: กำหนด constants และ root guards** ตาม input boundary ใน section 3
- [x] **Step 2: เขียน normalize_relative_path()** ให้คืน path แบบ POSIX และ reject path ที่ออกนอก root
- [x] **Step 3: เขียน sha256_file() แบบ streaming 1 MiB** และเพิ่ม test ด้วย known bytes b"alpha\n"
- [x] **Step 4: เขียน text detector แบบ conservative**: inspect binary chunk for NUL, ใช้ text suffix ที่ประกาศไว้, และไม่ decode/เขียน source กลับ
- [x] **Step 5: เขียน file record scanner** ที่เก็บ path, root_id, role, bytes, sha256, line_count, is_binary และ encoding status
- [x] **Step 6: sort records และคำนวณ root totals** โดยใช้ Path.as_posix() ไม่ใช้ filesystem order
- [x] **Step 7: รัน tests**

Run: python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v

Expected: PASS สำหรับ path, hash, file count, binary line count, output exclusion และ deterministic ordering.


### Task A0.3: Implement manifest schema, derived counts และ atomic output

**Files:**

- Modify: Phases/Phase4/tools/build_corpus_manifest.py
- Test: Phases/Phase4/tests/test_corpus_manifest.py

**Interfaces:**

- build_manifest() ต้องคืน schema p0-a0.corpus-baseline.v1
- write_manifest(path, manifest) ต้องเขียน JSON UTF-8, indent 2, trailing newline และใช้ temp file ใน parent directory ก่อน os.replace
- write_report(path, manifest) ต้องสร้าง Markdown ที่อ้าง snapshot fingerprint และ counts จาก manifest เดียวกัน

- [x] **Step 1: เพิ่ม source_roots summary** พร้อม existence/status, file count, total bytes, total lines, extension counts และ tree hash
- [x] **Step 2: เพิ่ม artifact_inputs** จาก Phase 0/4/5/6 artifact roots; อ่าน schema, schema_version, phase, wave, status เฉพาะเมื่อ JSON เป็น object และคง unknown เมื่อไม่มี field
- [x] **Step 3: เพิ่ม derived_counts** โดยอ่านค่าจาก phase0_baseline.json, wave0_build_manifest.json, Exported_ALL.report.json, Exported_FAILED.report.json และ source scan; เก็บ basis ต่อค่าและไม่ overwrite ค่าที่ source scan วัดเอง
- [x] **Step 4: เพิ่ม external_tools** โดย probe เฉพาะไฟล์/คำสั่งที่ประกาศ: ghidra_headless.py, ghidra_export_c.py, shutil.which("Cpp2IL"), shutil.which("Cpp2IL.exe"); missing optional tool ต้องเป็น { "status": "not_available", "required": false }
- [x] **Step 5: เพิ่ม checks** อย่างน้อย source_roots_present, artifact_inputs_present, source_roots_read_only, output_excluded, historical_manifest_inputs_present และ function_count_provenance
- [x] **Step 6: เพิ่ม test ว่า generated_at/tool metadata ไม่เปลี่ยน snapshot_fingerprint**

~~~python
first = build_manifest(root, generated_at_utc="2026-08-12T00:00:00Z")
second = build_manifest(root, generated_at_utc="2026-08-12T01:00:00Z")
self.assertEqual(first["snapshot_fingerprint"], second["snapshot_fingerprint"])
~~~

- [x] **Step 7: เพิ่ม test ว่า manifest/report เขียนได้เฉพาะ output/doc paths** และ source file bytes หลัง build เท่าเดิม
- [x] **Step 8: รัน tests และตรวจ formatting**

Run: python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v

Expected: PASS และ manifest fixture มี schema/fingerprint/records ครบโดยไม่มี absolute path.

### Task A0.4: Implement --check drift gate

**Files:**

- Modify: Phases/Phase4/tools/build_corpus_manifest.py
- Test: Phases/Phase4/tests/test_corpus_manifest.py

**Interfaces:**

compare_snapshot() ต้องคืน object รูปแบบนี้:

~~~json
{
  "status": "pass",
  "baseline_fingerprint": "fingerprint-from-baseline",
  "current_fingerprint": "fingerprint-from-current-input",
  "added": [],
  "removed": [],
  "changed": [],
  "count_deltas": []
}
~~~

เมื่อ drift ต้องเปลี่ยน status เป็น drift และเติมรายการที่ตรวจพบจริง; ห้ามย่อเป็นข้อความเดียว.

- [x] **Step 1: เขียน test --check pass** หลัง build baseline ใน temp workspace
- [x] **Step 2: เขียน test changed file** แก้ a.txt จาก alpha เป็น beta แล้ว assert exit code 2, path อยู่ใน changed และ baseline/current hash ต่างกัน
- [x] **Step 3: เขียน test added/removed file** และ assert แยกอยู่ใน added/removed
- [x] **Step 4: เขียน test missing baseline/required root** และ assert exit code 3 หรือ 4 ตามสาเหตุ
- [x] **Step 5: เขียน test output file เปลี่ยน** แล้ว assert --check ยัง pass เพราะ output root ถูก exclude
- [x] **Step 6: implement CLI parsing** ด้วย argparse และส่งผล JSON summary ไป stdout โดย errors ไป stderr
- [x] **Step 7: รัน focused suite**

Run: python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v

Expected: PASS ทั้ง pass, drift, missing input และ output-exclusion cases.


### Task A0.5: Build real baseline และ report จาก workspace

**Files:**

- Create/replace generated: Phases/Phase4/artifacts/corpus/manifest.json
- Create/replace generated: Phases/Phase4/docs/corpus_baseline_report.md
- Read-only verification: Phases/Phase0/artifacts/phase0_baseline.json, Phases/Phase4/artifacts/wave0_build_manifest.json, Phases/Phase5/artifacts/wave5_build_manifest.json, Phases/Phase6/artifacts/wave6_build_manifest.json

- [x] **Step 1: ตรวจว่าไม่มี process/งานเขียน source roots อยู่** และอย่า start local server เพราะ A0 ไม่ต้องใช้ server
- [x] **Step 2: รัน builder ครั้งแรก**

Run:

~~~powershell
python Phases/Phase4/tools/build_corpus_manifest.py --root . --output Phases/Phase4/artifacts/corpus --report Phases/Phase4/docs/corpus_baseline_report.md
~~~

Expected: สร้าง manifest.json และ report สำเร็จ; source roots ไม่ถูกแก้; output record ไม่รวม Phases/Phase4/artifacts/corpus/**.

- [x] **Step 3: ตรวจ measured totals กับ evidence ตั้งต้น**

Run:

~~~powershell
python -c "import json; p=json.load(open('Phases/Phase4/artifacts/corpus/manifest.json', encoding='utf-8')); print(json.dumps({'fingerprint':p['snapshot_fingerprint'],'roots':p['source_roots'],'derived_counts':p['derived_counts']}, ensure_ascii=False, indent=2))"
~~~

Expected: counts มีค่าจาก current scan; ถ้าต่างจาก Phase 0 ให้ report เป็น attention พร้อม expected/observed และไม่แก้ Phase 0 artifact.

- [x] **Step 4: รัน builder ซ้ำไปยัง temporary output** แล้วเปรียบเทียบ snapshot_fingerprint, source_roots, artifact_inputs และ derived_counts; generated_at_utc อาจต่างได้
- [x] **Step 5: รัน drift check จาก baselineจริง**

Run:

~~~powershell
python Phases/Phase4/tools/build_corpus_manifest.py --root . --output Phases/Phase4/artifacts/corpus --check
~~~

Expected: exit code 0, stdout ระบุ status=pass, added=[], removed=[], changed=[].

- [x] **Step 6: รัน focused tests และ diff check**

Run:

~~~powershell
python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v
git diff --check
~~~

Expected: tests PASS และไม่มี whitespace error.

### Task A0.6: ตรวจ A0 gate และบันทึก handoff state

**Files:**

- Modify: TODO.md mark only P0-A0 complete after all gates pass
- Modify: PROJECT_STATE.md record actual manifest fingerprint/counts, generated files, known limitations and next task P0-A1
- Read/verify: Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md

- [x] **Step 1: ตรวจ schema/fingerprint/output paths** ด้วย script read-only

~~~powershell
python -c "import json; p=json.load(open('Phases/Phase4/artifacts/corpus/manifest.json', encoding='utf-8')); assert p['schema']=='p0-a0.corpus-baseline.v1'; assert p['workspace_policy']['source_roots_read_only'] is True; assert p['snapshot_fingerprint']; print('A0 schema gate: PASS')"
~~~

- [x] **Step 2: ตรวจ source roots ไม่เปลี่ยน** ด้วย --check และยืนยัน source_roots_read_only=true; ห้ามใช้ git checkout, git reset หรือคำสั่งลบ/ย้ายไฟล์เพื่อทำให้ gate ผ่าน
- [x] **Step 3: ตรวจ historical artifacts byte-for-byte ไม่ถูก overwrite** โดยดู git diff -- Phases/Phase0/artifacts Phases/Phase4/artifacts/wave0_build_manifest.json Phases/Phase5/artifacts/wave5_build_manifest.json Phases/Phase6/artifacts/wave6_build_manifest.json
- [x] **Step 4: อัปเดต TODO.md และ PROJECT_STATE.md เฉพาะหลัง manifest/check/report/test ผ่าน**; ระบุ actual fingerprint และ attention ที่ตรวจพบ ไม่เขียนว่า complete จากการมีไฟล์อย่างเดียว
- [x] **Step 5: รัน baseline regression ที่เกี่ยวข้อง**

~~~powershell
python -m unittest Phases/Phase4/tests/test_corpus_manifest.py -v
python -m unittest Phases/Phase4/tests/test_wave0_index.py -v
python -m unittest Phases/Phase4/tests/test_cross_wave_gap_reconciliation.py -v
python -m unittest Phases/Phase4/tests/test_targeted_gap_scan.py -v
python -m unittest Phases/Phase4/tests/test_semantic_gap_trace.py -v
python Phases/Phase4/tools/build_corpus_manifest.py --root . --output Phases/Phase4/artifacts/corpus --check
git diff --check
~~~

Expected: ทุก command ผ่าน; historical tests ยังใช้ artifacts เดิม; A1 จึงเริ่มอ่าน manifest.json ได้.

- [ ] **Step 6: Commit เฉพาะ A0 ที่ผ่าน gate**

~~~powershell
git add Phases/Phase4/tools/build_corpus_manifest.py Phases/Phase4/tests/test_corpus_manifest.py Phases/Phase4/artifacts/corpus/manifest.json Phases/Phase4/docs/corpus_baseline_report.md TODO.md PROJECT_STATE.md
git commit -m "docs: freeze corpus intelligence baseline"
~~~

ห้าม stage ไฟล์ unrelated ที่มีอยู่ก่อนใน working tree.

สถานะ session นี้: ยังไม่ commit เนื่องจาก working tree มีการแก้ไขและไฟล์ untracked จากงานก่อนหน้าอยู่แล้ว จึงไม่ stage ไฟล์ทั้งก้อนที่อาจมีเนื้อหา unrelated; A0 artifacts พร้อมให้ผู้ดูแล review และ stage แบบเลือกเฉพาะ hunks/ไฟล์ที่ต้องการ


## 7. A0 acceptance gate

ถือว่า P0-A0 เสร็จได้เมื่อทุกข้อเป็นจริงพร้อมกัน:

- manifest.json มี schema p0-a0.corpus-baseline.v1 และ non-empty snapshot_fingerprint
- source roots ทั้งสามมี file records ครบตาม current filesystem และ source_roots_read_only=true
- Phase 0/4/5/6 artifact inputs มี hash/schema/status และ Phase 4 corpus/ output ถูก exclude
- canonical records ใช้ relative POSIX paths และไม่มี absolute path ใน fingerprint basis
- rerun บน input เดิมได้ fingerprint เดิมแม้ generated_at_utc ต่าง
- --check pass บน baseline และตรวจ added/removed/changed ได้เมื่อ fixture ถูกแก้
- missing required root/baseline/output path ที่ไม่ปลอดภัยให้ exit code ตาม contract
- optional tool ที่ไม่มีอยู่รายงาน not_available และ builder ยังสร้าง manifest ได้
- corpus_baseline_report.md แสดง measured counts, provenance, tool table และ known limitations ที่ตรวจได้จริง
- Phase 0/4/5/6 historical artifacts ไม่ถูก overwrite
- focused A0 tests, relevant Phase 4 tests และ git diff --check ผ่าน
- TODO.md ติ๊กเฉพาะ A0; PROJECT_STATE.md ชี้ไป A1 และบันทึก actual outputs

## 8. สิ่งที่ A1 ใช้ต่อได้ทันที

หลัง A0 ผ่าน ผู้ทำ A1 ต้องใช้:

- Phases/Phase4/artifacts/corpus/manifest.json เป็น input boundary และไม่ scan source roots แบบ ad hoc โดยไม่อ้าง manifest
- snapshot_fingerprint เป็น parent provenance ของ phase4_evidence_index.json
- artifact_inputs[*].sha256 เป็น basis สำหรับ supersession/current-gap reconciliation
- source_files[*].sha256 และ relative path เป็น source refs ตั้งต้นของ canonical index
- checks/known_limitations เป็น evidence metadata ไม่ใช่ semantic claims

ถ้า --check พบ drift ก่อนเริ่ม A1 ให้หยุด A1, สร้าง baseline candidate ใหม่ใน reviewable diff และระบุ source/artifact delta ก่อนตัดสินใจ freeze รอบใหม่.
