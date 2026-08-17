# Social Dev asset metadata coverage matrix

AM-1 compares every indexed asset, native selector, data-selector relation, field inventory, and runtime manifest entry. Index presence is not treated as runtime approval.

## Identity

- Coverage content hash: `9d47764ac1964516ceaef3329d178fc284e457d36cc5ccccfb2d7d2e2fedf377`
- Baseline content hash: `2ce296a4c47b92e1667cda63d719a433573dc9871172d1978bcd5537cd52d7e7`
- Contract content hash: `b7ccc1e0962fc9edfacf2bc8d24b58ebc20f11c3c201a4c8b043cbc858cedb31`

## Matrix counts

| Dimension | Count |
|---|---:|
| Indexed assets | 3,542 |
| Native catalog assets | 3,542 |
| Selectors | 3,192 |
| Data-selector relations | 523 |
| Data fields | 1,063 |
| Consumer edges | 250 |
| Lifecycle edges | 43 |
| Runtime manifest asset entries | 197 |
| Display gate entries | 18 |

## Asset coverage status

| Status | Count | Meaning |
|---|---:|---|
| `cataloged_with_native_relation` | 129 | Present in the native catalog and reached by a relation, but not currently in a runtime manifest. |
| `cataloged_without_current_relation` | 3,231 | Indexed/native-present but not reached by the current graph; may be companion/unused/under-modeled. |
| `runtime_manifest_referenced` | 182 | Referenced by a runtime manifest; family semantics still have their own gates. |

## Selector coverage

- Current selector statuses: `{'resolved_target_not_runtime_referenced': 3013, 'resolved_target_runtime_referenced': 178, 'unresolved_selector': 1}`.
- Unresolved selector records: **1**.
- The unresolved selector remains explicit and is not replaced with a guessed id.

## Data-field coverage

- Fields requiring semantic classification: **1,055**.
- These fields are not automatically asset fields. AM-3 must classify them as selector-bearing, data-only, control, relation, or intentionally non-visual.

## Runtime reference gaps

- Runtime manifest entries: **197**.
- Entries without an index/native identity: **0**.
- A manifest entry can use a derived runtime path; the matrix records both its raw manifest id and canonical source identity when available.

## Orphan interpretation

The orphan report is a work queue, not a deletion list. Unreferenced assets remain in evidence until a later family/consumer pass proves they are unused or classifies them as companion, localization, control, or runtime content.

```powershell
python -B tools/social-dev/build_asset_metadata_coverage.py
python -B tools/social-dev/test_asset_metadata_coverage.py
```
