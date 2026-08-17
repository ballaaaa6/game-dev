# R1.5 Metadata Identity Reconciliation Report

## Final decision

R1.5 status: PASS_R1_5_METADATA_IDENTITY_RECONCILIATION_AND_REPAIR_UNIVERSE_CORRECTION_CLOSED.
The corrected metadata foundation is the only canonical identity authority for the next repair phase.
The previous R1 architecture and acceptance package remain retained as audit history, but its pre-R1.5 counts, IDs, queue, and graph are superseded.

## Source and reader gate

Pinned source identity: PASS; APK, C# archive, libil2cpp, global-metadata, and C# corpus inventory match.
Alternate raw evidence hashes: PASS.
Metadata reader defect: CONFIRMED. The installed dnfile API uses 0-based bracket indexing and 1-based RID lookup; the prior builder's `table[1:]` discarded the first real row. Fix: `table_rows` now returns `list(table)` and all local RID/token conversions are explicit.

## Alternate evidence policy

Raw dump.cs, script.json, and the three selected alternate DummyDll files are retained as cross-check evidence.
Original Google-derived type/method/repair/call/field catalogs are comparison-only and are not canonical.

## Corrected totals

Canonical metadata: 8,373 types, 62,945 methods.
Corrected Twin target: GAME_FIRST_PARTY 198 types / 4,547 methods; KAIRO_ENGINE 443 types / 6,280 methods; combined 641 / 10,827.
Difference versus old R1 target 8,678: +2,149 methods.

## Core identity

Core-nine identity: PASS. AppData and GameForm are normal Assembly-CSharp types; Node is the canonical game.routeSearch.Node with 3 methods. No compiler-generated alias is primary.

## Alternate reconciliation

All 64 metadata-present assembly identities were compared. The cross-check normalizes only literal `.dll` suffixes, nested namespace qualification, generic-arity spellings, and ordered overload parameter spellings; it does not overwrite canonical IDs or counts.
Type classifications: {"DUMPER_VERSION_DIFFERENCE": 25, "GENERATED_TYPE_NAMING_DIFFERENCE": 1, "MATCH": 3, "REPRESENTATION_DIFFERENCE": 35}.
Method classifications: {"DUMPER_VERSION_DIFFERENCE": 25, "GENERATED_TYPE_NAMING_DIFFERENCE": 1, "MATCH": 3, "REPRESENTATION_DIFFERENCE": 35}.
Canonical/alternate method totals: 62,945 / 62,943; common normalized method instances: 60,793; RVA presence matches: 56,277; exact RVA value matches: 0.
Canonical RVA values come from DummyDll PE MethodDef rows, while alternate RVA/offset values come from the native Il2CppDumper dump; they are different address domains and are therefore reported, not substituted or treated as equal.

## Quality and repair universe

Quality distribution: {"CFG_REPAIR": 2856, "CLEAN": 2477, "NATIVE_LIFT_REQUIRED": 4997, "SOURCE_LIMITED": 41, "STATIC_DATA_REPAIR": 27, "TYPE_REPAIR": 429}.
Repair disposition: {"AUTO_STATIC_DATA_REPAIR": 27, "AUTO_TYPE_REPAIR": 429, "CFG_REPAIR": 2856, "ISIL_ASSISTED_REPAIR": 4997, "SOURCE_LIMITED": 41, "VERIFY_ONLY": 2477}.
Queue coverage: PASS; repaired C# bodies: 0.

## Dependency graph

Resolved owned calls: 13,512; external-resolved calls: 8,668; owned-unresolved calls: 104,306; ambiguous calls: 5,306; source-limited calls: 0.
SCCs: 10,801; recursive SCCs: 348; largest SCC: 4; dependency layers: 19.
Fields are split into owned/external resolved and unresolved/ambiguous/source-limited classes; unresolved field rows: 26,795.

## Boundary

Source roots modified: NO.
C# gameplay/Kairo bodies repaired: NO.
Native lifting started: NO.
R2 started: NO.
V8/V8R changed: NO.
Unity/Unity-MCP started: NO.

## Determinism and validation

Deterministic rerun: PASS; local builder validation: PASS; git diff --check is required before closure.

## Next boundary

R2_AUTOMATED_WHOLE_CORPUS_REPAIR is the recommended next phase. This task stops here.
