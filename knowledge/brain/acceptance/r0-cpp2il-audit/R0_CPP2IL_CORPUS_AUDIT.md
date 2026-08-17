# R0 Cpp2IL Corpus and Recovery-Mode Audit

Status: COMPLETE. This package stops at the measured Cpp2IL corpus/recovery-mode recommendation. No V8/V8R work and no C# repair were started.

Final recommendation: **HYBRID**

## Scope and source identity

- Pinned identity status: **MATCH**.
- APK SHA-256: `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`.
- libil2cpp.so SHA-256: `364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a`.
- global-metadata.dat SHA-256: `f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579`.
- C# RAR SHA-256: `a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903`.
- Independent extraction root: `C:\Users\WINDOW XI\AppData\Local\Temp\r0-cpp2il-audit-20260817\old-csharp-corpus\1_Click_CSharp_Code`. The archive was not modified and the temporary extraction is not a runtime dependency.

## Existing corpus measurements

- Total extracted files: **5568**; C# files: **5504**; .csproj files: **64**.
- C# bytes/lines: **55,358,557 / 1,540,930**; zero-byte C# files: **3**.
- Namespaces: **295**; types: classes **5492**, structs **947**, enums **858**, interfaces **601**.
- Methods: **41,229**; CLEAN **33,552 (81.38%)**; TYPE_REPAIR **753**; CFG_REPAIR **2,912**; STATIC_DATA_REPAIR **0**; NATIVE_LIFT_REQUIRED **4,012 (9.73%)**; SOURCE_LIMITED **0**.
- Readable without native lifting: **83.21%** (CLEAN + TYPE_REPAIR).
- Method metric basis: accepted same-identity corpus baseline. The raw lexical declaration index (**43,103** methods) and per-method signals are retained in `r0-method-quality-index.json` for traceability and coverage diagnostics.

## Core-class result

| Class | Methods | Clean | Native lift | Clean % |
|---|---:|---:|---:|---:|
| AppData | 329 | 89 | 156 | 27.05% |
| GameForm | 94 | 23 | 41 | 24.47% |
| Player | 232 | 54 | 121 | 23.28% |
| Room | 117 | 16 | 86 | 13.68% |
| ObjChip | 51 | 12 | 25 | 23.53% |
| Staff | 205 | 76 | 65 | 37.07% |
| FurnitureData | 20 | 4 | 5 | 20.00% |
| Astar | 10 | 0 | 5 | 0.00% |
| Node | 3 | 1 | 0 | 33.33% |

The required data-loader path is materially better than the behavior-heavy classes: `FurnitureData.Load` is CLEAN, while routing, rendering, placement, time, and staff-process methods carry type/CFG/native recovery markers.

## Old invocation and current capability

- Old invocation confidence: **HIGH**; Unity version forced: **2022.3.62**; postprocessor: **ilspycmd 11.0.0.9375**.
- Fresh rerun: **YES**, using local `Cpp2IL 2022.1.0` against the pinned native binary and metadata. No download or install was performed.
- Fresh outputs: managed IL recovery DLLs, Diffable C# signatures/stubs, and ISIL native disassembly/basic-block evidence. The selected build did not expose a separate method-dump output.
- Comparison sample: **500** plus **23** required core-method records.
- Fresh high-level C# improved: **0**; method dump improved: **0**; intermediate representation improved: **14**; native-lift-required/no high-level improvement: **279**.
- Interpretation: keep the old ILSpy C# as the readable skeleton; use fresh ISIL/native evidence as a per-method recovery aid. A full fresh C# replacement is not justified.

## Zero-byte and static-data conclusion

- The three zero-byte C# files are classified as exporter/generated-type loss, not proof of absent code: `-PrivateImplementationDetails-.cs, kairo.unity.ui/Graphics.cs, kairo.unity.util/Language.cs`.
- Current metadata exposes **684** PrivateImplementationDetails field records and **8** generated method records. Fresh Diffable C# emits generated type shells for the private container, `Graphics`, and `Language`.
- A reusable static-data reconstruction pass is justified: resolve RuntimeFieldHandle relocations, map private field references to metadata default values, then cross-check source/asset tables. Existing K4.1 Fukidashi closure evidence demonstrates this path; it is not executed as a C# repair in R0.

## Compile blockers

No compile was attempted. The corpus is not a buildable Unity project and the R0 boundary forbids repair/fabrication. The measured blockers are recorded in `r0-compile-blockers.json`: type erosion, goto/IL CFG corruption, diagnostic helper calls, missing static blobs, and missing framework/reference assemblies/zero-byte exporter artifacts.

## Recommendation and stop boundary

**HYBRID** — retain the existing C# corpus and use fresh Cpp2IL ISIL/native intermediate evidence selectively for degraded methods and static-data recovery. Do not rerun the full corpus as a replacement. The next authorized boundary is `R1_CORE_CSHARP_REPAIR`; it has not started. Stop here.

## Evidence package

- `r0-corpus-inventory.json` — corpus/file/type/field/property inventory.
- `r0-method-quality-index.json` — project-wide issue signals and degraded-method index.
- `r0-core-class-quality.json` — required core-class and method metrics.
- `r0-zero-byte-analysis.json` — zero-byte classifications and fresh metadata evidence.
- `r0-old-invocation-analysis.json` — recovered historical command line and versions.
- `r0-current-cpp2il-capability.json` — current local tool capabilities, commands, and output manifests.
- `r0-old-vs-fresh-comparison.json` — required-method and stratified-sample comparison.
- `r0-compile-blockers.json` — compile-risk categories without a fabricated compile verdict.
- `r0-final-recommendation.json` — single final decision.
