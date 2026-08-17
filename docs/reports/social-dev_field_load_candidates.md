# Social Dev field/load candidates

This pass pairs field assignments and `StringArrayStream` reader calls in each data class `Load` body by source order. A pair is not a semantic proof.

| Result | Classes |
|---|---:|
| candidate | 38 |
| count mismatch | 3 |
| Load missing | 3 |

## Count mismatches

| Type | Reader calls | Field assignments |
|---|---:|---:|
| `CompanyData` | 10 | 9 |
| `DownloadEventData` | 6 | 5 |
| `ProfileData` | 7 | 5 |

## Gate

Use this artifact to guide manual semantic review and to compare English/Japanese row shapes. Do not generate production models directly from positional pairs.
