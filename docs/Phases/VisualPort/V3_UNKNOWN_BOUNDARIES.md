# V3 Unknown and Deferred Boundaries

V3 is allowed to pass with explicit nonblocking unknowns. The unknowns are not repaired with naming similarity, browser manifests, runtime state, or guessed selectors.

| Boundary | Current status | Safe behavior | Next static investigation |
| --- | --- | --- | --- |
| `resInterface_` pack/member ownership | `UNKNOWN` | Keep an empty declared manager and typed missing lookups | Trace assignments and RecordStore selectors |
| `resEvents_` event pack membership | `UNKNOWN` | Keep outside the 11 declared visual groups | Reconcile event payloads and index ownership |
| Avatar head dynamic selector | `PARTIAL` | Expose only source-indexed avatar-head IDs | Trace `headIndex` construction |
| `LoadReady` allocation body | `PARTIAL` | Preserve INF IDs and null gaps | Recover the remaining native loop |
| `LoadStart` scheduling | `DEFERRED` | Use explicit preloaded fixture readiness | Reconcile static callback/state transitions |
| `CustomImages` population | `DEFERRED` | Keep the dictionary empty; retain lookup precedence | Trace all population callers |
| Atlas population/GPU lifetime | `DEFERRED` | Keep atlas status deferred | Trace static atlas index/build references |
| Unsupported SEB decode | `SOURCE_LIMITED` | Exclude the unsupported payload | Extend grammar only if a later fixture needs it |
| V2 `_drawBitmap` pixels | `DEFERRED_TO_V7` | Keep native/browser output hashes null | Use only future static shader/backend evidence |

None of these boundaries blocks a V4 caller from requesting a proven group and original ID. They do block any claim that an unresolved group, async schedule, custom image, atlas relationship, or raster pixel has been proven.
