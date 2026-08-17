# VGO_Core removal record

`sources/raw/VGO_Core` was a human-authored derived scaffold, not extracted source evidence. It was removed before Social Dev runtime implementation and was never promoted to `runtime/social-dev`. The table below is retained as a historical record of the removed files.

- Files: `5`
- Bytes: `11647`
- Source status: `removed_derived_only`
- Runtime status: `never_promoted`

| File | Types | Methods | Reasons |
|---|---:|---:|---|
| `sources/raw/VGO_Core/DataManager.cs` | 1 | 3 | explicitly_simplified_derivation, mocked_loader_or_initialization |
| `sources/raw/VGO_Core/DataSchema.cs` | 7 | 0 | unproven_vgo_specific_extension |
| `sources/raw/VGO_Core/GameRuntime.cs` | 4 | 4 | placeholder_runtime_logic, unproven_vgo_specific_extension |
| `sources/raw/VGO_Core/SaveManager.cs` | 1 | 3 | save_without_matching_load |
| `sources/raw/VGO_Core/UIForm.cs` | 3 | 3 | no explicit marker |

## Historical gate

Do not copy fields such as `baseSpeed` or `isSpecialBody` into a canonical model; the scaffold that introduced them has been removed and the fields have no source provenance.

Machine-readable disposition: `knowledge/fixtures/accepted/vgo_core_disposition.json`.
