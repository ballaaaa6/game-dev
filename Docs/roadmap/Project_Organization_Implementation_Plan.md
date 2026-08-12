# Knowledge-Centered Workspace Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Replace the active Phases/Phase0–Phase7 layout with knowledge/, runtime/, tools/, docs/, and archive/ while preserving source/evidence content and deleting only verified cache/temp directories.

**Architecture:** Evidence lives under knowledge/, browser code under runtime/, analysis utilities under tools/, current and historical written material under docs/, and deferred/compatibility material under archive/. Protected extraction roots remain at their existing paths. Every move is explicit, recorded, and followed by reference and regression checks.

**Tech Stack:** PowerShell for guarded moves and process inspection; Git for tracked renames; Python pathlib/hashlib for relocation manifests and syntax checks; Node.js for runtime tests; ripgrep for stale-path scans.

**Status:** Completed in the working tree. The checklist below is retained as the execution record; final state and verification results are summarized in `PROJECT_STATE.md` and `TODO.md`.

## Global Constraints

- Keep game-dev-story-mod_Sprites/, game-dev-story-mod_Dumped/, game-dev-story-mod_Extracted/, APK_Toolkit/, ghidra_11.0.1_PUBLIC/, and viewer/ at their current paths and do not edit their contents.
- Do not recreate or register Assembly-CSharp/. Do not delete game-dev-story-mod_Dumped/DummyDll/Assembly-CSharp.dll; it is a separate protected input.
- Move evidence and historical plans; delete only exact __pycache__/ and .corpus.*.tmp directories after safety checks.
- Do not stage the user-provided C# corpus or its untracked reports unless separately requested.
- Use explicit paths under D:\antigravity\test open ai; no broad recursive delete, git reset --hard, or git checkout --.
- Preserve PhaseN labels inside evidence records when they describe original provenance; rename filesystem paths and active navigation.
- Generated reorganization artifacts belong under knowledge/reorganization/, never at root.
- Stop at any failed verification before starting the next task.

## Target Path Map

| Existing path | Target path |
|---|---|
| Phases/Phase0/artifacts | knowledge/baseline/evidence |
| Phases/Phase0/docs | knowledge/baseline/reports |
| Phases/Phase0/references | knowledge/baseline/references |
| Phases/Phase1/artifacts | knowledge/world-assets/evidence |
| Phases/Phase1/docs | knowledge/world-assets/reports |
| Phases/Phase1/references | knowledge/world-assets/references |
| Phases/Phase2/artifacts | knowledge/characters/evidence |
| Phases/Phase2/docs | knowledge/characters/reports |
| Phases/Phase2/references | knowledge/characters/references |
| Phases/Phase2/tests | knowledge/characters/tests |
| Phases/Phase2/tools | knowledge/characters/tools |
| Phases/Phase3/artifacts | knowledge/language/evidence |
| Phases/Phase3/docs | knowledge/language/reports |
| Phases/Phase3/references | knowledge/language/references |
| Phases/Phase4/artifacts | knowledge/reverse-engineering/evidence |
| Phases/Phase4/docs | knowledge/reverse-engineering/reports |
| Phases/Phase4/references | knowledge/reverse-engineering/references |
| Phases/Phase4/tests | tools/reverse-engineering/tests |
| Phases/Phase4/tools | tools/reverse-engineering |
| Phases/Phase5/runtime | runtime/office/app |
| Phases/Phase5/artifacts | runtime/office/evidence |
| Phases/Phase5/docs | runtime/office/reports |
| Phases/Phase5/tests | runtime/office/tests |
| Phases/Phase5/tools | runtime/office/tools |
| Phases/Phase6/runtime | runtime/dashboard/app |
| Phases/Phase6/artifacts | runtime/dashboard/evidence |
| Phases/Phase6/docs | runtime/dashboard/reports |
| Phases/Phase6/tests | runtime/dashboard/tests |
| Phases/Phase6/tools | runtime/dashboard/tools |
| Phases/Phase7 | archive/future-ai |
| Phases/README.md | docs/archive/Phase_Archive_Index.md |
| 1_Click_CSharp_Code | knowledge/csharp/primary |
| C# checkers | tools/csharp-evidence/ |
| C# reports | knowledge/csharp/coverage/ |
| current Roadmap 2.0 spec | docs/roadmap/Roadmap_2.0_CSharp_First.md |
| old specs | docs/archive/specs/ |
| old plans | docs/archive/plans/ |
| old roadmap | docs/roadmap/archive/AI_Agent_Office_Roadmap.md |
| APK guide | docs/guides/APK_to_Ghidra_Detailed_Guide.md |
| enums.txt | docs/references/enums.txt |
| Auto_Annotator.py, Smart_Compressor.py | archive/legacy-tools/ |

### Task 1: Freeze the boundary and create the relocation manifest

**Files:**
- Create: tools/maintenance/workspace_layout.py
- Create: tools/maintenance/test_workspace_layout.py
- Create: knowledge/reorganization/relocation_manifest.before.json

**Interfaces:** build_snapshot(root: Path) -> dict, write_snapshot(root: Path, output: Path) -> None, and verify_snapshot(root: Path, snapshot: dict) -> list[str]. The snapshot records the commit, mapped-root counts/bytes, hashes for the C# corpus and text evidence, and protected-root status. It skips Git metadata, caches, temporary directories, SQLite/binary protected roots, and paths outside the workspace.

- [x] Write and pass a temporary-fixture test for sorted paths, counts, bytes, deterministic SHA-256, and one mismatch after changing a fixture file.
- [x] Run:

    python -m unittest tools/maintenance/test_workspace_layout.py -v

  Expected initially: FAIL because the utility is absent. The implementation was then added and the focused test passed.
- [x] Implement the utility with pathlib, hashlib, stable JSON, and UTF-8 newline output.
- [x] Re-run the focused unittest and expect PASS.
- [x] Capture the real boundary:

    New-Item -ItemType Directory -Force -Path knowledge\reorganization | Out-Null
    python tools/maintenance/workspace_layout.py --root . --output knowledge/reorganization/relocation_manifest.before.json

  Assert that the pre-move snapshot commit is ed1fa53, the C# corpus has 85 .cs files plus its project file, Assembly-CSharp/ is absent, and protected binary content is not copied into the manifest.
- [x] Commit only the utility and pre-move manifest:

    git add tools/maintenance/workspace_layout.py tools/maintenance/test_workspace_layout.py knowledge/reorganization/relocation_manifest.before.json
    git commit -m "Add workspace relocation manifest guard"

**Verification:** focused unittest and JSON parsing of the pre-move manifest exit 0. Verified before proceeding.

### Task 2: Relocate primary C# evidence, reports, and root utilities

**Files:**
- Move 1_Click_CSharp_Code/ → knowledge/csharp/primary/
- Move Check_Code_Coverage.py and Semantic_Coverage_Checker.py → tools/csharp-evidence/
- Move Coverage_Report.html, Coverage_Report.md, Semantic_Report.csv, Semantic_Report.md → knowledge/csharp/coverage/
- Move Auto_Annotator.py and Smart_Compressor.py → archive/legacy-tools/
- Modify the two moved C# checker scripts.
- Create knowledge/csharp/README.md, knowledge/csharp/coverage/README.md, and tools/csharp-evidence/README.md.

**Interfaces:** Both checkers use ROOT = Path(__file__).resolve().parents[2], read ROOT / game-dev-story-mod_Dumped / dump.cs, read ROOT / knowledge / csharp / primary, and write only to ROOT / knowledge / csharp / coverage. Existing report filenames remain unchanged.

- [ ] Create target directories; resolve each absolute target and fail if it is outside the workspace or already contains files.
- [ ] Move the untracked corpus/reports with explicit Move-Item -LiteralPath operations; compare counts, bytes, and aggregate SHA-256 with the pre-move manifest.
- [ ] Add pathlib.Path to both checkers, replace hardcoded external paths, and replace root-relative report writes with REPORT_DIR / filename. Keep checker logic unchanged.
- [ ] Write READMEs stating that the C# output is decompiler evidence, the 100% report is symbol presence only, and scripts derive paths from __file__.
- [ ] Run:

    python -m py_compile tools/csharp-evidence/check_coverage.py tools/csharp-evidence/check_semantic_coverage.py
    $cs = @(Get-ChildItem knowledge/csharp/primary -Recurse -File -Filter '*.cs')
    if ($cs.Count -ne 85) { throw "Expected 85 C# files, found $($cs.Count)" }
    if (-not (Test-Path knowledge/csharp/primary/Assembly-CSharp.csproj)) { throw 'C# project file missing' }
    rg -n 'D:\\antigravity\\kairosoft' tools/csharp-evidence knowledge/csharp -g '*.py' -g '*.md' -g '*.html' -g '*.csv'

  The final scan must find no old external path.
- [ ] Commit checker scripts, moved tracked legacy tools, and new READMEs; leave the user-provided C# corpus/reports untracked:

    git add tools/csharp-evidence archive/legacy-tools knowledge/csharp/README.md knowledge/csharp/coverage/README.md
    git commit -m "Organize primary CSharp evidence"

**Verification:** 85 C# files plus the project file exist at the target, both checkers compile, and no external hardcoded path remains.

### Task 3: Relocate baseline, world, character, and language knowledge

**Files:**
- Move Phase0 artifacts/docs/references/README to knowledge/baseline evidence/reports/references/README.
- Move Phase1 artifacts/docs/references/README to knowledge/world-assets evidence/reports/references/README.
- Move Phase2 artifacts/docs/references/tests/tools/README to knowledge/characters evidence/reports/references/tests/tools/README.
- Move Phase3 artifacts/docs/references/README to knowledge/language evidence/reports/references/README.
- Modify moved READMEs and path-bearing manifests/reports.

**Interfaces:** These bundles are evidence-only; their READMEs use semantic names and link to knowledge/README.md, the new Roadmap 2.0 path, and protected source roots.

- [ ] Create target trees and abort if any destination contains a pre-existing file.
- [ ] Use git mv for tracked directories and explicit Move-Item -LiteralPath only for untracked files.
- [ ] Rewrite filesystem paths in text-readable files: each Phases/PhaseN/artifacts path becomes the mapped knowledge/.../evidence path, with corresponding docs and references paths. Leave provenance fields such as phase: PhaseN unchanged.
- [ ] Change headings to Baseline Evidence, World and Asset Evidence, Character Evidence, and Language Evidence while retaining results and known limitations.
- [ ] Run:

    foreach ($p in @('knowledge/baseline/evidence','knowledge/world-assets/evidence','knowledge/characters/evidence','knowledge/language/evidence')) { if (-not (Test-Path $p)) { throw "Missing $p" } }
    rg -n 'Phases/Phase[0-3]|Phases\\Phase[0-3]' knowledge/baseline knowledge/world-assets knowledge/characters knowledge/language
    python -m unittest discover -s knowledge/characters/tests -p 'test_*.py' -v

  The stale-path scan must return no matches and character tests must pass.
- [ ] Commit the tracked relocation without using a broad add that could stage the C# corpus:

    git add -u knowledge/baseline knowledge/world-assets knowledge/characters knowledge/language
    git add knowledge/baseline/README.md knowledge/world-assets/README.md knowledge/characters/README.md knowledge/language/README.md
    git commit -m "Group baseline asset character and language knowledge"

**Verification:** target bundles exist, old Phase0–3 directories are absent, scans are empty, and character tests pass.

### Task 4: Relocate reverse-engineering evidence and central tools/tests

**Files:**
- Move Phase4 artifacts → knowledge/reverse-engineering/evidence.
- Move Phase4 docs → knowledge/reverse-engineering/reports.
- Move Phase4 references → knowledge/reverse-engineering/references.
- Move Phase4 tests → tools/reverse-engineering/tests.
- Move Phase4 tools → tools/reverse-engineering.
- Move Phase4 README → knowledge/reverse-engineering/README.md.
- Modify moved Python tools/tests and path-bearing JSON/JSONL/Markdown.
- Create knowledge/reverse-engineering/README.md and tools/reverse-engineering/README.md.

**Interfaces:** Moved tools resolve the workspace root with Path(__file__).resolve().parents[2]. Evidence root is ROOT / knowledge / reverse-engineering / evidence; reports root is ROOT / knowledge / reverse-engineering / reports. Corpus output defaults to evidence/corpus and report defaults to reports/.

- [ ] Record the pre-move count/bytes/SHA-256 for Phase4/artifacts/corpus/ from the manifest. Do not open or rewrite corpus_index.sqlite.
- [ ] Move with guarded explicit commands and verify corpus_index.sqlite, JSONL files, and views at knowledge/reverse-engineering/evidence/corpus/.
- [ ] Replace ROOT / Phases / Phase4 constants with REVERSE_ENGINEERING = ROOT / knowledge / reverse-engineering; update Phase0/1/2/5/6 artifact references and corpus output/report safety guards.
- [ ] Update every command in the moved README to the new tools/evidence/reports paths.
- [ ] Run:

    python -m compileall -q tools/reverse-engineering
    python -m unittest tools/reverse-engineering/tests/test_wave0_index.py tools/reverse-engineering/tests/test_corpus_manifest.py tools/reverse-engineering/tests/test_corpus_index.py -v
    python tools/reverse-engineering/build_corpus_index.py --scope all --output knowledge/reverse-engineering/evidence/corpus --check

  Expected: syntax and selected contracts pass; canonical --check validates without rewriting output.
- [ ] Commit:

    git add -u knowledge/reverse-engineering tools/reverse-engineering
    git add knowledge/reverse-engineering/README.md tools/reverse-engineering/README.md
    git commit -m "Organize reverse engineering knowledge and tools"

**Verification:** no Phase4 directory remains, corpus counts/hashes match, selected tests pass, and canonical --check is clean.

### Task 5: Relocate office runtime, dashboard runtime, and deferred AI material

**Files:**
- Move Phase5 runtime/artifacts/docs/tests/tools to runtime/office app/evidence/reports/tests/tools.
- Move Phase6 runtime/artifacts/docs/tests/tools to runtime/dashboard app/evidence/reports/tests/tools.
- Move Phase7 → archive/future-ai.
- Modify runtime test/tool path constants and READMEs.
- Create runtime/README.md, runtime/office/README.md, runtime/dashboard/README.md, and archive/future-ai/README.md.

**Interfaces:** Browser entry files remain runtime/office/app/index.html, app.js, runtime.js, and style.css. Task modules remain in runtime/dashboard/app/. Source assets continue to resolve from protected roots; no copy is made.

- [ ] Before browser verification, inspect Get-NetTCPConnection -State Listen and matching node/python/vite/wrangler/workerd command lines. Reuse a healthy repository server or record that none exists.
- [ ] Move Phase5, Phase6, and Phase7 with explicit guarded operations; assert all runtime entrypoints exist.
- [ ] Update only path references required by the move; preserve public runtime APIs, task schema, localStorage keys, and adapter semantics.
- [ ] Run:

    node --check runtime/office/app/runtime.js
    node --check runtime/office/app/app.js
    node --check runtime/dashboard/app/task_system.js
    node runtime/office/tests/test_wave5_runtime.js
    node runtime/dashboard/tests/test_wave6_task_system.js
    python -m unittest runtime/office/tests/test_wave5_contract.py runtime/dashboard/tests/test_wave6_contract.py -v

- [ ] Serve from the workspace root on the configured project port after listener checks; verify task interaction and zero new console errors/warnings. Stop only the process tree started by this task and re-check listeners.
- [ ] Commit:

    git add -u runtime archive
    git add runtime/README.md runtime/office/README.md runtime/dashboard/README.md archive/future-ai/README.md
    git commit -m "Separate office dashboard runtime from historical phases"

**Verification:** runtime entrypoints and tests use new paths, browser smoke passes, and no process started by this task remains.

### Task 6: Rebuild documentation and navigation

**Files:**
- Move current Roadmap 2.0 spec → docs/roadmap/Roadmap_2.0_CSharp_First.md.
- Move frozen roadmap → docs/roadmap/archive/AI_Agent_Office_Roadmap.md.
- Move old specs → docs/archive/specs/; old plans → docs/archive/plans/.
- Move guide/reference files to docs/guides/ and docs/references/.
- Move Docs/README.md → docs/README.md.
- Modify README.md, AGENTS.md, PROJECT_STATE.md, TODO.md, active READMEs, and path-bearing historical docs.
- Create docs/README.md, docs/roadmap/README.md, knowledge/README.md, runtime/README.md, tools/README.md, and archive/README.md.

**Interfaces:** Root README links only to new top-level directories and protected roots. AGENTS.md names the new output policy and current roadmap. PROJECT_STATE.md/TODO.md distinguish active Roadmap 2.0 from archived plans.

- [ ] Create docs/roadmap/archive, docs/archive/specs, docs/archive/plans, docs/guides, and docs/references; move explicit files and rename only the current roadmap file.
- [ ] Rewrite active navigation and handoff files, preserving evidence provenance labels and historical result text.
- [ ] Run:

    $stale = @(rg -n --hidden --glob '!.git/**' --glob '!game-dev-story-mod_Dumped/**' --glob '!game-dev-story-mod_Extracted/**' --glob '!game-dev-story-mod_Sprites/**' --glob '!ghidra_11.0.1_PUBLIC/**' --glob '!runtime/office/evidence/**' --glob '!runtime/dashboard/evidence/**' 'Phases/Phase[0-7]|Phases\\Phase[0-7]|Docs/superpowers|(^|[\\/])1_Click_CSharp_Code([\\/]|$)|Assembly-CSharp/' .)
    if ($stale.Count -gt 0) { $stale; throw 'Stale active filesystem references remain' }

  Historical prose may mention phase names, but no active path or removed Assembly-CSharp/ path may remain.
- [ ] Resolve local Markdown links and assert that docs/roadmap/Roadmap_2.0_CSharp_First.md and knowledge/csharp/primary/Assembly-CSharp.csproj exist.
- [ ] Commit:

    git add README.md AGENTS.md PROJECT_STATE.md TODO.md docs knowledge/README.md runtime/README.md tools/README.md archive/README.md
    git commit -m "Refresh workspace navigation after reorganization"

**Verification:** navigation targets resolve, stale-path scan is empty, and state points to the new roadmap.

### Task 7: Delete only verified caches and temporary directories

**Files:**
- Delete root and nested __pycache__/ directories from the exact pre-move scan.
- Delete knowledge/reverse-engineering/evidence/.corpus.build-*.tmp and knowledge/reverse-engineering/reports/.corpus-index-report-*.tmp only after exact-name checks.
- Preserve all source, C#, reports, JSON/JSONL, SQLite, runtime, tests, and archive content.

- [ ] Enumerate exact targets and resolve each absolute path:

    $targets = @(Get-ChildItem -Path . -Recurse -Directory -Force | Where-Object { $_.Name -eq '__pycache__' -or $_.Name -like '.corpus.*.tmp' })
    foreach ($t in $targets) { $resolved = (Resolve-Path -LiteralPath $t.FullName).Path; if (-not $resolved.StartsWith((Get-Location).Path, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe target $resolved" } }

- [ ] Remove only each exact resolved target with Remove-Item -LiteralPath $resolved -Recurse -Force. Do not pass a root, wildcard, or computed parent directory.
- [ ] Re-enumerate and require zero cache/temp results; record the deleted list in relocation_manifest.after.json.

**Verification:** only enumerated cache/temp directories are gone; no protected root or evidence file was deleted.

### Task 8: Final integrity gate and handoff

**Files:**
- Create/modify knowledge/reorganization/relocation_manifest.after.json.
- Modify PROJECT_STATE.md and TODO.md.

- [ ] Build the post-move snapshot:

    python tools/maintenance/workspace_layout.py --root . --output knowledge/reorganization/relocation_manifest.after.json

  Compare target counts/bytes/hashes with the pre-move manifest and assert protected source-root counts/fingerprints are unchanged.
- [ ] Run:

    git diff --check
    python -m py_compile tools/csharp-evidence/*.py tools/reverse-engineering/*.py tools/reverse-engineering/tests/*.py runtime/office/tools/*.py runtime/office/tests/*.py runtime/dashboard/tools/*.py runtime/dashboard/tests/*.py
    python -m unittest discover -s knowledge/characters/tests -p 'test_*.py' -v
    python -m unittest tools/reverse-engineering/tests/test_wave0_index.py tools/reverse-engineering/tests/test_corpus_manifest.py tools/reverse-engineering/tests/test_corpus_index.py -v
    node runtime/office/tests/test_wave5_runtime.js
    node runtime/dashboard/tests/test_wave6_task_system.js

  Expected: all commands exit 0, stale active paths are absent, and protected roots remain read-only.
- [ ] Review git status --short --ignored; stage only tracked relocations, path updates, READMEs, manifest utility, and approved cache deletions. Verify untracked C# files exist only under knowledge/csharp/primary/.
- [ ] Update PROJECT_STATE.md/TODO.md with new top-level paths, deleted cache/temp targets, verification results, and Assembly-CSharp/ absence.
- [ ] Commit:

    git add PROJECT_STATE.md TODO.md knowledge/reorganization/relocation_manifest.after.json
    git commit -m "Finalize knowledge-centered workspace reorganization"

**Verification:** post-move snapshot matches, all focused tests pass, git diff --check passes, no duplicate runtime server remains, and user-provided C# source is not staged unless explicitly requested.

## Execution Order and Rollback

Run tasks strictly in order 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Stop at a failed gate. The rollback boundary is the pre-move snapshot plus the latest successful commit; restore only exact moved paths from the manifest and retain the archive.
