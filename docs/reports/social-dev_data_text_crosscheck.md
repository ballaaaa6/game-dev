# Social Dev data text cross-check

This pass checks the source-backed DataManager registry against the extracted English/Japanese xls text-table names. It does not assign column semantics.

| Check | Count |
|---|---:|
| Registry records | 43 |
| English name matches | 43 |
| Japanese name matches | 43 |
| English extra text files | 3 |
| Japanese extra text files | 0 |

## Missing matches

None.

## Extra text files

### English.lproj
- `Exclusion.txt`
- `softkey.txt`
- `text.txt`
### Japanese.lproj
- None

## Gate

Name coverage is a structural match only. Column order, row meaning, language fallback, and loader behavior still require cross-checking against each `Load(StringArrayStream)` method and the assembly guide.
