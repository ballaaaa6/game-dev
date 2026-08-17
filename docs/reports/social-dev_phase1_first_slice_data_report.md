# Social Dev Phase 1 — First-slice data extraction report

Date: 2026-08-13

Status: historical candidate extraction passed structural validation. The
selected display-slice mappings and non-promoted exceptions are now closed by
the Pre-runtime Closure Sweep; the candidate remains provenance evidence.

## Results

The first-slice data package was built from real asset-guide evidence and C# loader candidates, retaining raw rows, locale pairs, row/hash provenance, loader reader sequences, and scalar-prefix field candidates in full.

Latest checks:

- Selected types: 5 (`RoomData`, `FurnitureData`, `StaffData`, `JobData`, `SkillData`).
- Selected records: 22.
- Records missing from English/Japanese: 0.
- Candidate links: 6.
- Historical blocking review items: 5.
- Validation status: `pass`.
- Active closure status: `closed_before_runtime`.

## Primary machine-readable files

- `knowledge/fixtures/accepted/first_slice_data_candidate.json`
- `knowledge/fixtures/accepted/first_slice_data_validation.json`

## Selected first slice

| Type | IDs | Initial rationale |
| --- | --- | --- |
| `RoomData` | `0` | First base room; English `Floor A`, Japanese `フロアA` |
| `FurnitureData` | `1, 2, 5` | Minimum scene objects: Door, Desk, Graphics Workstation; Japanese `ドア`, `机`, `ペンタブデスク` |
| `StaffData` | `0–4` | First five actors for identity/living-slice checks |
| `JobData` | `4` | Selected from `jobId_` in the StaffData scalar prefix; relationship remains `order_candidate` |
| `SkillData` | `1` | Supporting record derived from `StaffData.skill_` after loader framing; relationship remains `order_candidate` |

This is a preparation candidate, not a semantic conclusion about the game. No room placement, spawn, route, or behavior is created by guessing numeric values.

## Data-retention policy

1. English is the primary row and Japanese is the cross-check; row counts, ID sequences, and duplicate checks must match.
2. Retain every raw column of selected rows with source path, row number, and row hash; do not rename numeric columns into game meanings.
3. Use field mapping only for scalar fields before the first array reader of a loader with evidence; this is the safer boundary for this candidate extraction.
4. Relationships inferred from data position/order remain `candidate` or `unknown` until body/assembly/selector evidence supports them.
5. The candidate package must not be imported directly into browser runtime; it must pass the canonical-contract and validation gates in Phase 2.

## Discovered links

The `jobId_` value of all five selected StaffData records is `4` and occurs in the scalar prefix before the `defParams_` array reader. Therefore `StaffData.jobId_ → JobData(4)` is stored as an `order_candidate` with medium confidence.

`StaffData.skill_` occurs after an array reader and must be read with complete loader framing. The observed value is `1` for all five selected staff records, so `SkillData(1)` is retained only as a supporting record. Status remains `order_candidate`, not a promoted semantic relation.

## Passed validation

- English/Japanese versions of all five tables have matching row counts and ID order.
- Selected records exist in both locales with no duplicate IDs.
- Raw rows for selected records were retained.
- Input provenance is hashed in the candidate manifest.
- Semantic status is forced to `pending_review` to prevent promotion of unverified meanings.

Re-run with:

```powershell
python -B tools/social-dev/build_first_slice_data_candidate.py
python -B tools/social-dev/test_first_slice_data_candidate.py
```

## Promotion blockers

- `RoomData` lacks evidence verifying room state, placement, and map-column semantics.
- Array columns cannot be assigned semantic names from this evidence alone.
- `StaffData.skill_ → SkillData(1)` remains only a loader-aware order candidate; relation/lookup semantics are unverified.
- Room/furniture/staff asset selectors are validation evidence, not a runtime selector contract.
- Locale names can verify alignment, but are not semantic proof for all field mappings.

## Active closure artifacts

- `knowledge/fixtures/accepted/load_contract_closure.json`
- `knowledge/fixtures/accepted/semantic_review_closure.json`
- `knowledge/fixtures/accepted/runtime/data_contract.json`
- `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json`
