# Social Dev native content connection graph

This graph connects native data records, resource selectors, source/derived assets, C# consumers, and lifecycle phases.

It intentionally keeps unresolved or decompiler-ambiguous edges visible instead of converting them into guessed semantics.

## Node counts

| Node type | Count |
|---|---:|
| `data_registry` | 43 |
| `data_records` | 3693 |
| `selectors` | 3191 |
| `assets` | 3542 |
| `consumers` | 98 |

## Edge counts

| Edge type | Count |
|---|---:|
| `data_selector` | 523 |
| `selector_asset_and_companion` | 4596 |
| `consumer` | 250 |
| `lifecycle` | 43 |

## Query path

`data record → native field value → native indirection table (when applicable) → selector reference → source/derived asset → consumer method → lifecycle phase`

Registry hash: `2fff10d3b8cb8a9e4d961d3fee7e4e7a2dec60018733cf4fe855eefee46b7313`
Graph hash: `fa5ef447f3fbd4a08a0beb6fae93a4d1e7897af0a87f6d6dd58fbb65a958f771`
