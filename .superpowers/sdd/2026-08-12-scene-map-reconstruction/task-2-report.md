# Task 2 — SEB audit and conditional re-extraction

## Status

`DONE_WITH_CONCERNS`

## Scope and implementation

- Added the importable, standard-library-only `tools/scene_reconstruction/seb_codec.py`.
- Added `tools/scene_reconstruction/build_seb_audit.py` and the generated evidence at `knowledge/world-assets/evidence/scene_reconstruction/seb_audit.json`.
- Added six focused unit tests in `tools/scene_reconstruction/test_seb_codec.py`.
- Did not modify `runtime/office/app`, `room_manifest.json`, any source/extraction input, or create an `Assembly-CSharp/` directory.

The format-0 parser records the selector, declared group and record counts, signed big-endian short values, byte offsets, raw group/record bytes, exact partial-tail bytes, and the computed tail shortfall. Missing fields remain `null`; specifically, `reverse_u` and `reverse_v` are not invented when their final four bytes are absent. A high-bit selector is recorded as the explicit `compact_variant` decision with `unknown` status rather than being decoded as format 0.

## RED evidence

Tests were created before `seb_codec.py` and `build_seb_audit.py` existed. The required first command failed because Python could not import the absent `tools.scene_reconstruction.build_seb_audit` module:

```text
ERROR: test_seb_codec (unittest.loader._FailedTest)
ModuleNotFoundError: No module named 'tools.scene_reconstruction.build_seb_audit'
Ran 1 test
FAILED (errors=1)
```

This was the expected RED condition: neither the parser nor the explicit partial-record model was present.

## Verified audit result

`seb_audit.json` contains a record-level audit for all 21 discovered logical floor SEBs:

```text
floor0, floor1, floor3, floor5, floor6, floor7, floor8, floor11,
floor12, floor14, floor15, floor16, floor17, floor18, floor19,
floor21, floor31, floor33, floor34, floor35, floor36
```

Every sprite-side candidate is `candidate` under the declared format-0 structure with an exact `tail_shortfall` of `4`. The audit includes the raw final-record bytes and retains the final four observed bytes as `raw_tail_hex`; no record is declared complete.

For every logical floor, the source comparison table contains these direct candidate locations:

- sprite-side file — `byte-identical` to the current payload;
- extracted `floor*.seb` file — `absent`;
- APK member named `floor*.seb` — `absent`;
- ZIP member named `floor*.seb` — `absent`;
- existing Phase 1 SEB evidence — `byte-identical` by its preserved SHA-256.

The APK and ZIP are byte-identical inputs, each with SHA-256 `7361ef005b169b41bdc34a31c9835ecf6f386212207cfbce2ecb1ea914d409e5`. Their 1,226 members are hashed Unity data names and include no direct `floor*.seb` member. The extracted root has no direct `floor*.seb` counterpart. Therefore the outcome for all 21 floors is exactly `no_full_payload_found`.

No `reextract/<source-hash>/...` payload was staged. The implementation stages a content-addressed archive member only for `recovered_full_payload` or `recovered_different_payload`, records its archive path/member/hash, and never overwrites an extraction root. The test fixture exercises that branch with a longer archive payload.

## Pair entries and claim statuses

Each audit row includes explicit PNG/SEB pair entries. Present source paths are `verified`; a missing pair entry is `unknown`. Structural shortfall claims are `candidate`. The audit schema permits only `verified`, `candidate`, and `unknown` as claim statuses.

## Verification

```text
python -m unittest discover -s tools/scene_reconstruction -p 'test_*.py' -v
Ran 11 tests ... OK

python tools/scene_reconstruction/build_seb_audit.py
[OK] Audited 21 floor SEB files: {'no_full_payload_found': 21}

python -m py_compile tools/scene_reconstruction/seb_codec.py tools/scene_reconstruction/build_seb_audit.py tools/scene_reconstruction/test_seb_codec.py
exit 0

source/read-only hash check against source_inventory.json
OK: 1881 source/extraction file hashes match source_inventory.json
```

## Concern

The direct archive/extraction audit establishes that the four-byte shortfall is not repaired by any named `floor*.seb` payload present in the APK, ZIP, or extraction root. The original source payload may be embedded inside a Unity bundle under a hashed `assets/bin/Data` member; resolving that nested provenance requires a separately evidenced bundle/TextAsset extraction path. Until then, the source limitation remains `candidate`, not `verified`.

## Fix round 1 — recovery gate hardening

### Changed files

- `tools/scene_reconstruction/seb_codec.py`
- `tools/scene_reconstruction/build_seb_audit.py`
- `tools/scene_reconstruction/test_seb_codec.py`
- `knowledge/world-assets/evidence/scene_reconstruction/seb_audit.json` (rebuilt; content result remains unchanged)

### Fixes

1. A format-0 payload with bytes beyond its declared record structure is now `candidate`, preserving the suffix in `partial_tail`, instead of `verified`. It cannot qualify as a complete candidate.
2. Recovery selection now accepts only a `distinct`, `verified` payload from an archive or fresh source. A complete current sprite plus a distinct truncated archive payload produces `not_needed` and has no `best_complete` recovery candidate.
3. The staging guard now independently requires `best.parsed.status == "verified"`, in addition to the recovery outcome and archive/fresh source type.

### Added behavior coverage

- trailing format-0 bytes produce `candidate` and `no_full_payload_found`;
- a complete sprite plus a truncated archive payload does not report recovery;
- incomplete and trailing-byte archive payloads produce no staged file;
- the existing positive longer complete archive staging case remains covered.

### Verification commands and output

```text
python -m unittest discover -s tools/scene_reconstruction -p 'test_seb_codec.py' -v
Ran 9 tests in 0.037s
OK

python -m unittest discover -s tools/scene_reconstruction -p 'test_*.py' -v
Ran 14 tests in 0.209s
OK

python tools/scene_reconstruction/build_seb_audit.py
[OK] Audited 21 floor SEB files: {'no_full_payload_found': 21}

python -m py_compile tools/scene_reconstruction/seb_codec.py tools/scene_reconstruction/build_seb_audit.py tools/scene_reconstruction/test_seb_codec.py
exit 0

source/read-only hash check against source_inventory.json
OK: 1881 source/extraction hashes unchanged; 21 floor SEBs retain four-byte shortfalls
```
