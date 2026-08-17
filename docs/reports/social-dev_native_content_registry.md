# Social Dev native content registry

This registry preserves the game's separate DataManager IDs, resource selector IDs, source/derived asset identities, and C# evidence consumer edges.

The decompiled C# and source archive are read-only evidence. This package is not runtime-approved; it is the identity and connection layer that later room/runtime catalogs consume.

## Counts

| Item | Count |
|---|---:|
| `data_manager_arrays` | 43 |
| `data_types` | 43 |
| `data_rows` | 3693 |
| `assets` | 3542 |
| `selectors` | 3192 |
| `data_selector_relations` | 523 |
| `selector_asset_relations` | 3191 |
| `asset_companion_relations` | 882 |
| `consumer_edges` | 250 |
| `lifecycle_edges` | 43 |

## Identity validation

- Registry status: `pass`
- Duplicate asset IDs: `0`
- Duplicate selector keys: `0`
- Unresolved selector targets: `1`
- Missing archive members: `0`

## Native identity policy

1. Numeric DataManager IDs remain scoped to their data type.
2. `seb_`, `subSeb_`, and `img_` remain resource selector references, not filenames.
3. Source/derived assets retain archive-relative paths, hashes, and provenance.
4. A runtime instance ID is separate from its source FurnitureData or selector ID.
5. Unknown values and `-1` sentinels are retained rather than guessed.

## Trace chain

`data tables → StringArrayStream readers → DataManager arrays → native indirection tables (when applicable) → selector fields → resource selector files → source/derived assets → C# consumers → lifecycle phase`

Content hash: `2fff10d3b8cb8a9e4d961d3fee7e4e7a2dec60018733cf4fe855eefee46b7313`
