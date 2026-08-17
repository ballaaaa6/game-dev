# V1 Core Format Recovery

## Scope and status

V1 recovers the selected visual data path from the real `social dev` source and archive evidence into isolated runtime contracts. The scope is the `Sprite`, `Seb`, `Image`, and `ResourceManager` format boundary, the selected ZIP fixtures, and synchronous lookup behavior. Source and extracted evidence remain read-only; the runtime consumes generated contracts rather than executing decompiled C#.

The selected V1 contracts pass their focused parity checks. The result is intentionally partial: depth payloads, atlas membership, raster resize, `optimizeSeb`, asynchronous callback scheduling, and unproven resource memberships remain deferred or unknown.

## Recovered domains

- `Sprite`: the 14-field serialized/runtime projection, including frame, texture, UV, translation, flip, blend, and packed color fields. Native accessor RVAs and the conversion-buffer slot mapping are recorded in `native-recovery-map.json`.
- `Seb`: header fields, record order, layer order, source-image association, sprite destination bounds, and pixel-rectangle fallback behavior. Numeric depth values are not claimed.
- `Image`: selected OPT headers, cells, logical reconstruction, exact pixel hashes, source-region lookup, use-count metadata, and atlas identity metadata. Raw OPT bytes, raster resize, and atlas region promotion are outside the proven contract.
- `ResourceManager`: the 11 declared resource groups, source-indexed sparse image/SEB bindings where `img.inf` or `seb.inf` proves membership, and explicit missing-lookup behavior.

## Native-versus-format proof

`FORMAT-PROVEN` means the selected source/fixture bytes and runtime contract agree. `NATIVE-RVA-PINNED` means the native method location is recorded against the pinned APK and dump hashes. A native RVA does not, by itself, prove a missing payload or deferred branch. The complete claim-level ledger is `knowledge/fixtures/accepted/visual-port/v1/native-recovery-map.json`.

## Evidence and boundaries

The selected fixtures are real members of the source ZIP and are hash-checked by the fixture validator. `01_GAME_PACKS/develop/develop_menu_light.seb` is present in the archive but is recorded as `NON_SELECTED_UNSUPPORTED`; it is not used to infer a V1 decoder rule.

The unknown register contains the nine required fields for every open question: `id`, `class`, `method`, `question`, `known_evidence`, `missing_evidence`, `affected_fixtures`, `impact`, and `next_investigation`. See `unknowns.json` for the machine-readable register.

## Changed V1 surfaces

V1 adds isolated TypeScript contracts and runtime adapters under `runtime/social-dev/src/v1/`, focused tests under `runtime/social-dev/tests/`, evidence builders and validators under `tools/social-dev/`, machine evidence under `knowledge/fixtures/accepted/visual-port/v1/`, and these reports. Existing renderer/source behavior is unchanged.

## V2 stop decision

V2 has not started. Start it only after new native or fixture evidence closes at least one deferred branch; do not promote depth, atlas, raster resize, `optimizeSeb`, or unknown resource memberships from inference to fact.
