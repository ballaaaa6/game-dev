# Project Organization — Knowledge-Centered Layout

สถานะเอกสาร: design ที่ผู้ใช้อนุมัติสำหรับการจัดโครงสร้าง workspace ครั้งใหญ่; รอ review เอกสารก่อนสร้าง implementation plan และย้ายไฟล์จริง

วันที่: 2026-08-12
ขอบเขต: `D:\antigravity\test open ai`

## 1. เป้าหมาย

เปลี่ยน workspace จากโครงสร้างที่แบ่งตามลำดับ `Phase0`–`Phase7` เป็นโครงสร้างที่แบ่งตามหน้าที่ของข้อมูล เพื่อให้ session ใหม่หา evidence, runtime, tools, เอกสารปัจจุบัน และงานเก่าได้ทันที

เป้าหมายหลัก:

- เอาชื่อ `Phase0`–`Phase7` ออกจาก active directory layout
- รวมหลักฐานและความรู้ไว้ใต้ `knowledge/`
- แยก executable/runtime ออกจาก evidence และ reports
- เก็บ C# ชุดใหม่เป็น primary evidence ในตำแหน่งที่ชัดเจน
- ย้ายงานเก่าไป `docs/archive/` หรือ `archive/` แทนการลบทิ้ง
- ลบเฉพาะ cache/temp ที่สร้างใหม่ได้
- ปรับ references, scripts, tests และ handoff ให้ชี้ path ใหม่ทั้งหมด

## 2. โครงสร้างเป้าหมาย

```text
workspace/
├─ knowledge/
│  ├─ baseline/
│  ├─ world-assets/
│  ├─ characters/
│  ├─ language/
│  ├─ reverse-engineering/
│  └─ csharp/
│     ├─ primary/
│     └─ coverage/
├─ runtime/
│  ├─ office/
│  └─ dashboard/
├─ tools/
│  ├─ csharp-evidence/
│  └─ reverse-engineering/
├─ docs/
│  ├─ roadmap/
│  ├─ guides/
│  ├─ references/
│  └─ archive/
└─ archive/
   ├─ future-ai/
   └─ legacy-tools/
```

Protected extraction/input directories remain at the workspace root because existing tooling and generated evidence use those paths:

- `game-dev-story-mod_Sprites/`
- `game-dev-story-mod_Dumped/`
- `game-dev-story-mod_Extracted/`
- `APK_Toolkit/`
- `ghidra_11.0.1_PUBLIC/`
- `viewer/`

`Assembly-CSharp/` has already been removed by the user and is not recreated or registered as a new input. The `Assembly-CSharp.dll` inside the protected dumped source remains untouched because it is a different existing input artifact.

## 3. Relocation map

### 3.1 Knowledge

| Existing path | New path | Meaning |
|---|---|---|
| `Phases/Phase0` | `knowledge/baseline` | baseline, checksums, inventory seed |
| `Phases/Phase1` | `knowledge/world-assets` | assets, rooms, SEB, placement evidence |
| `Phases/Phase2` | `knowledge/characters` | actor catalog, body/face, animation evidence |
| `Phases/Phase3` | `knowledge/language` | language extraction and translation evidence |
| `Phases/Phase4` | `knowledge/reverse-engineering` | corpus, traces, contracts, semantic gap evidence |
| `1_Click_CSharp_Code` | `knowledge/csharp/primary` | primary expanded C# evidence corpus |
| `Check_Code_Coverage.py` | `tools/csharp-evidence/check_coverage.py` | symbol baseline tool |
| `Semantic_Coverage_Checker.py` | `tools/csharp-evidence/check_semantic_coverage.py` | diagnostic semantic checker prototype |
| `Coverage_Report.md/.html` | `knowledge/csharp/coverage/` | symbol coverage reports |
| `Semantic_Report.csv/.md` | `knowledge/csharp/coverage/` | semantic diagnostic reports |

Within each knowledge bundle, generic folders retain their purpose: `artifacts/` becomes `evidence/`, `docs/` becomes `reports/`, and `references/` remains `references/` where renaming does not break a tool contract. Reverse-engineering tests/tools are centralized under `tools/reverse-engineering/`.

### 3.2 Runtime

| Existing path | New path |
|---|---|
| `Phases/Phase5/runtime` | `runtime/office/app` |
| `Phases/Phase5/artifacts` | `runtime/office/evidence` |
| `Phases/Phase5/docs` | `runtime/office/reports` |
| `Phases/Phase5/tests` | `runtime/office/tests` |
| `Phases/Phase5/tools` | `runtime/office/tools` |
| `Phases/Phase6/runtime` | `runtime/dashboard/app` |
| `Phases/Phase6/artifacts` | `runtime/dashboard/evidence` |
| `Phases/Phase6/docs` | `runtime/dashboard/reports` |
| `Phases/Phase6/tests` | `runtime/dashboard/tests` |
| `Phases/Phase6/tools` | `runtime/dashboard/tools` |

### 3.3 Documents and archive

| Existing path | New path |
|---|---|
| `Docs/superpowers/specs/2026-08-12-csharp-first-virtual-game-office-roadmap-2-design.md` | `docs/roadmap/Roadmap_2.0_CSharp_First.md` |
| `Docs/AI_Agent_Office_Roadmap.md` | `docs/roadmap/archive/AI_Agent_Office_Roadmap.md` |
| `Docs/superpowers/plans/*` | `docs/archive/plans/*` |
| old specs under `Docs/superpowers/specs/` | `docs/archive/specs/` |
| `Docs/APK_to_Ghidra_Detailed_Guide.md` | `docs/guides/APK_to_Ghidra_Detailed_Guide.md` |
| `Docs/enums.txt` | `docs/references/enums.txt` |
| `Phases/Phase7` | `archive/future-ai` |
| `Auto_Annotator.py` | `archive/legacy-tools/Auto_Annotator.py` |
| `Smart_Compressor.py` | `archive/legacy-tools/Smart_Compressor.py` |

The old plans and specs remain available for provenance but are no longer active execution authority. The current authority is Roadmap 2.0.

## 4. Safety rules

- Do not edit contents of protected extraction/input directories.
- Do not recreate `Assembly-CSharp/` or infer evidence from it.
- Do not delete C#, reports, contracts, tests, or historical plans merely because they are old; relocate them.
- Delete only `__pycache__/` directories and known `.corpus.*.tmp` temporary directories after verifying their names and locations.
- Use explicit absolute workspace paths for every move; do not use broad recursive deletion.
- Update path references in source code, tests, Markdown, JSON/JSONL manifests, README/state files, and scripts.
- Preserve semantic provenance labels such as `Phase4` inside historical evidence records when they describe the original extraction wave; only filesystem paths and active navigation are renamed.
- Do not stage unrelated user-provided source changes outside this reorganization.

## 5. Reference migration

The implementation will apply a deterministic path map, then scan all text-readable repository files for:

- `Phases/Phase0` through `Phases/Phase7`
- `Phases/README.md`
- old `Docs/superpowers/...` paths
- root C# checker/report paths
- `1_Click_CSharp_Code` path references

Binary files and protected source content are excluded from rewrite. Generated manifests are updated only where the field is a filesystem path; original semantic phase labels remain unchanged for provenance.

## 6. Verification gate

The reorganization is complete only when all of the following pass:

- no active path references `Phases/PhaseN` or the removed `Assembly-CSharp/` directory
- no active script/report path points to the old root C# checker or report location
- all target directories exist and expected source/report/runtime files are present
- `knowledge/csharp/primary` contains the full 85-file C# corpus and project file
- no protected input directory has a content hash change
- Python syntax checks pass for moved tools and runtime test/tool modules
- focused Phase 5/6 runtime tests and relevant reverse-engineering contract tests pass from new paths
- `git diff --check` passes
- `PROJECT_STATE.md`, `TODO.md`, `README.md`, and directory READMEs describe the new layout
- only explicitly approved cache/temp directories are deleted

## 7. Rollback boundary

Before moving files, record the current Git status and create a relocation manifest containing old path, new path, file count, byte count, and SHA-256 for tracked/untracked text evidence roots. If a verification gate fails, stop and restore the exact moved paths from that manifest; do not use `git reset --hard` or delete the archive.
