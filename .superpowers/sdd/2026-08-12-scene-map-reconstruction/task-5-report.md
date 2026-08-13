# Task 5 Report — real object placement from producer lineage

Completed on 2026-08-13.

## What changed

- Added `tools/scene_reconstruction/test_object_placement.py` to lock the classification boundary first.
- Added `tools/scene_reconstruction/build_object_placement_contract.py` to publish the object-placement provenance contract.
- Published `knowledge/world-assets/evidence/scene_reconstruction/object_placement_contract.json`.

## Evidence summary

The current page still shows only three fixture objects because the runtime adapter baseline exposes exactly three records:

- `reception.fixture.0`
- `desk.fixture.0`
- `chair.fixture.0`

Those records verify asset identity, but they do not by themselves prove original room placement. The page coordinates and sort/depth values are diagnostic adapter values, not a recovered floor snapshot.

The contract keeps these evidence layers separate:

- asset identity: verified from the source inventory and the furniture manifest;
- SEB/local crop: bounded and separate from placement;
- producer lineage: preserved as lineage evidence, including one verified lineage edge and candidate lineage records;
- room/base destination: unknown;
- world coordinate: unknown;
- screen coordinate: diagnostic-only for the adapter fixture;
- sort/depth: diagnostic-only for the adapter fixture;
- floor snapshot presence: unknown.

No persisted or generated `floor0` room-state record was found, so the contract intentionally reports unknown placement instead of converting the adapter fixture into an original map.

## Results

- Contract status: `asset_identity_verified_placement_unknown`
- Verified asset count: `3`
- Verified lineage count: `1`
- Candidate lineage count: `3`
- Floor snapshot status: `unknown`

## Tests

- `python -m unittest discover -s tools/scene_reconstruction -p 'test_object_placement.py' -v`
- `python tools/scene_reconstruction/build_object_placement_contract.py`
- `python -m unittest discover -s tools/scene_reconstruction -p 'test_*.py' -v`
- `python -m compileall tools/scene_reconstruction`

## Self-review

The main guardrail held: verified asset identity was not promoted into verified original placement.

The only open limitation is evidentiary, not implementation-related. The workspace still lacks a persisted or generated floor snapshot that ties these three fixtures back to an original room-state record, so placement remains unknown by design.

## Fix round 1

Review feedback closed in this round:

- added `OfficeObjecList` as the opening provenance anchor in the evidence walk, with source ref and line-level proof from `GameForm.cs`;
- renamed the summary label to `classification` so no field named `status` now carries a non-approved value;
- added a recursive test that checks every `status` field in the contract tree stays within `verified`, `candidate`, or `unknown`;
- added a regression assertion that the generated evidence explicitly includes `OfficeObjecList`.
