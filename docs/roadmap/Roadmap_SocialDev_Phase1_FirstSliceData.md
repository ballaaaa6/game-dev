# Social Dev Phase 1 — First-slice data extraction

Status: **closed by the Pre-runtime Closure Sweep for display-slice-01**

The candidate package remains historical evidence. Its selected loader mappings,
relations, and non-promoted exceptions are closed by
`knowledge/fixtures/accepted/load_contract_closure.json` and
`knowledge/fixtures/accepted/runtime/data_contract.json`.

## Goal

Build a candidate data package for the first scene by extracting real data from table evidence, C# loader contracts, and English/Japanese locales. Do not call it a runtime contract until semantic review passes.

The selected first slice is:

- room: ID 0, English name Floor A, Japanese name フロアA;
- furniture/object: ID 1 Door, ID 2 Desk, ID 5 Graphics Workstation;
- staff: IDs 0–4, five records to cover multiple character and animation identities;
- linked job candidate: ID 4 from the scalar-prefix `jobId_` field in staff records;
- supporting skill candidate: ID 0 to retain shape and provenance, not to promote it as actor semantics.

This selection is a `derived_candidate` from the lowest/base records and extracted relationships. It does not confirm that this is the actual room state where the player starts.

## Rules

- Use English as the primary table and Japanese as the locale cross-check.
- Always retain the complete raw row columns.
- Decode only the scalar prefix before the first array when the loader provides evidence for that mapping.
- After `GetIntArray`, `GetIntIntArray`, or another array reader, do not automatically zip columns into semantic fields.
- Store the reader sequence and field-assignment sequence with every record.
- Every record has table path, row number, row hash, source references, input hash, and status.
- This package belongs under `knowledge/fixtures/accepted/` only; it does not enter `runtime/social-dev/`.

## Work package 1 — Verify table/loader boundaries

1. Load `load_contract_candidates.json` and `field_load_candidates.json`.
2. Select rows for RoomData, FurnitureData, StaffData, JobData, and SkillData.
3. Resolve the English table path from the loader candidate.
4. Resolve the matching Japanese table.
5. Check row counts, first-column ID sequences, and column-count distributions.
6. Record a mismatch or missing table as a review item.

The result is a table summary and loader-candidate shape for each data type.

## Work package 2 — Extract raw records

For each selected ID, retain:

- type, ID, locale;
- table path, row number, row SHA-256;
- column count, raw columns;
- reader sequence;
- field-assignment sequence;
- scalar-prefix candidate;
- mapping status;
- semantic status.

`scalar_prefix_candidate` means fields before the first array reader. For example, RoomData can verify the scalar order before `objMap_`; it does not certify the semantics of the entire row.

## Work package 3 — Create candidate links

Create links with confidence levels:

- `StaffData.jobId_ → JobData.id` is usable at `order_candidate` level because it appears before the first array field;
- `StaffData.skill_ → SkillData.id` remains unknown if it appears after an array field;
- retain room/object relationships from selected IDs and loader shape, but do not claim that object placement is in room ID 0 without room-state/placement evidence;
- use English/Japanese records and ID alignment to verify row correspondence, not to invent new meanings.

## Work package 4 — Locale and integrity checks

Check:

- English/Japanese row counts;
- ID-sequence equality;
- selected IDs present in both languages;
- duplicate IDs;
- row hashes;
- raw column counts;
- loader reader counts;
- scalar-prefix counts;
- C# and table evidence source files/hashes.

## Work package 5 — Review queue

Open review items for:

- room-state-placement-unverified;
- array-column-semantic-unverified;
- staff-skill-link-unverified;
- asset-selector-not-promoted;
- locale-name-is-evidence-not-semantic.

Do not delete records that remain unknown; keep them separated in the candidate package.

## Outputs

- `knowledge/fixtures/accepted/first_slice_data_candidate.json`;
- `knowledge/fixtures/accepted/first_slice_data_validation.json`;
- `docs/reports/social-dev_phase1_first_slice_data_report.md`;
- `tools/social-dev/build_first_slice_data_candidate.py`;
- `tools/social-dev/test_first_slice_data_candidate.py`.

## Gate

This Phase 1 extraction passes when:

- selected IDs resolve completely in English/Japanese;
- raw room/furniture/staff/job/skill rows have provenance and hashes;
- loader/field sequences are fully retained;
- no array field is misinterpreted through positional zipping;
- the staff-to-job link is recorded as a candidate with confidence;
- validation passes;
- semantic blockers remain explicit and are not promoted into runtime.

## After the gate

Create candidate SceneCatalog, ObjectCatalog, and ActorCatalog from this package, then build route/occupancy/state fixtures before creating the Vite scaffold.
