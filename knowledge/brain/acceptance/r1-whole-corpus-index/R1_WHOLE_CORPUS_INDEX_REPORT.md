# R1 Whole-Corpus Index Report

## 1. Executive result

R1 status: PASS. The pinned source gate is PASS; no recovered C# body was edited or executed.
The R1 metadata authority contains 8,309 types and 62,884 methods across the DummyDll set.
The owned target catalog contains 557 non-generated types and 8,678 overload-safe method records.

## 2. Source gate and authority model

APK SHA-256: fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf (MATCH).
C# archive SHA-256: a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903 (MATCH).
libil2cpp SHA-256: 364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a (MATCH).
global-metadata SHA-256: f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579 (MATCH).
The independent C# corpus contains 5,568 files, 5,504 C# files, 64 project files, and 55,358,557 C# bytes.
Zero-byte C# files are retained as source evidence: -PrivateImplementationDetails-.cs, kairo.unity.ui/Graphics.cs, kairo.unity.util/Language.cs.
DummyDll metadata is the canonical R1 assembly/type/method identity authority. R0 source analysis is retained as a quality and repair-signal authority.

## 3. Ownership taxonomy and assembly inventory

The exact ownership taxonomy is: GAME_FIRST_PARTY, KAIRO_ENGINE, UNITY_BOUNDARY, DOTNET_FRAMEWORK, THIRD_PARTY, COMPILER_GENERATED, SOURCE_LIMITED_OWNERSHIP.
The catalog covers 114 assembly rows, including 64 DummyDll assemblies and 102 APK scripting-assembly names.
50 scripting assemblies have no matching DummyDll and remain explicit external/source-limited rows.
724 namespace/path exceptions are recorded; assembly authority wins for Assembly-CSharp and KairoLibrary.

## 4. Type and method identity catalog

Stable method identity hashes the pinned APK identity, assembly, declaring type full name, method name, method generic arity, return type, and ordered parameter types. Metadata tokens, RVAs, and file offsets remain attached as verification evidence.
Method IDs are unique: True. Queue IDs are unique: True.
Source matching found bodies for 6,388 target methods; 6,819 target methods have a source declaration.

## 5. Quality, verification, and repair disposition

Quality class, verification status, and repair disposition are separate fields. No record is marked verified merely because it has a source declaration or native availability.
Quality counts: {"CFG_REPAIR": 1902, "CLEAN": 2126, "NATIVE_BOUNDARY": 178, "NATIVE_LIFT_REQUIRED": 3337, "SOURCE_LIMITED": 755, "STATIC_DATA_REPAIR": 16, "TYPE_REPAIR": 364}.
Verification counts: {"BASELINE_READABLE": 2126, "EXTERNAL_BOUNDARY": 178, "NEEDS_REPAIR": 5619, "SOURCE_LIMITED": 755}.
Disposition counts: {"AUTO_STATIC_DATA_REPAIR": 16, "AUTO_TYPE_REPAIR": 364, "CFG_REPAIR": 1902, "EXTERNAL_BOUNDARY": 178, "ISIL_ASSISTED_REPAIR": 3001, "NATIVE_LIFT": 336, "SOURCE_LIMITED": 755, "VERIFY_ONLY": 2126}.
R1 records repaired bodies: 0.

## 6. Owned dependency graph

The graph contains 9,392 owned call edges, 700 metadata type edges, 8,769 field edges, and 87,175 explicit external or unresolved edges.
It contains 8,656 method SCCs, 407 recursive SCCs, and a maximum dependency layer of 13.
Ownership bridges are recorded in 35 bridge classes.

## 7. ISIL and native/static-data availability

The fresh ISIL root is present and contains 6,682 files and 62,943 method blocks.
Target methods with ISIL are 5,970; target methods with a native address are 5,970.
Static-data references are recorded as graph edges and repair signals. They do not authorize runtime integration or native lifting in R1.

## 8. Deterministic, resumable builder

The builder writes sorted JSON and JSONL, records source-file hashes, preserves a source parse checkpoint, and emits a content-addressed artifact tree manifest. Resume uses the source cache only when its source hashes match the pinned corpus.

## 9. Repair queue

The queue has 8,678 rows with exact one-to-one coverage of the owned target method catalog.
Priority counts: {"0": 3337, "1": 2282, "2": 755, "3": 2304}.
Native-required methods: 3,337; ISIL/native evidence is available for 2,994.
The queue is a plan and evidence index only. R1 performs no C# body repair.

## 10. Core-nine validation

Core-nine status: PASS.
The nine R0 anchor names are checked against the R1 metadata catalog; two DummyDll anchors are explicit compiler-generated identity gaps and remain excluded from the owned method catalog.

## 11. R0 baseline comparison and scope decision

R0 accepted 41,229 source-baseline methods and retained 43,103 raw lexical declarations. R1 deliberately adds the metadata/DummyDll authority rather than collapsing those two authorities into one number.
R1 is accepted as the whole-corpus index, ownership boundary, overload-safe identity catalog, dependency graph, and complete repair queue.

## 12. Stop boundary

STOP before R2. No V8, V8R, runtime, Unity, emulator, native lifting, C# repair, integration, persistence, backend, deployment, or source-root mutation was performed.

## Validation summary

Validation status: PASS. Failed checks: none.
