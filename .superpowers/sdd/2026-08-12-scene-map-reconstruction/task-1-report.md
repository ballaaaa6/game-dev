# Task 1 report: Freeze the source inventory and floor universe

## Status

DONE

## RED test evidence

Command:

```text
python -m unittest discover -s tools/scene_reconstruction -p 'test_source_inventory.py' -v
```

Initial result before implementation:

```text
ImportError: Failed to import test module: test_source_inventory
ModuleNotFoundError: No module named 'tools.scene_reconstruction.paths'
FAILED (errors=1)
```

This was the expected failure because the new interfaces were absent.

## Implementation

- Added `tools/scene_reconstruction/paths.py` with workspace-boundary validation.
- Added `tools/scene_reconstruction/source_inventory.py` with deterministic file/directory records, SHA-256 hashing, ZIP/APK member enumeration, `.last_extraction.env` path capture, floor discovery, and explicit `verified`/`candidate`/`unknown` relation statuses.
- Added `tools/scene_reconstruction/build_source_inventory.py` to emit `knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json`.
- Added focused tests covering hash stability, archive member metadata, cross-root floor discovery, missing office SEB pairs, and outside-workspace rejection.

## Verification

- Focused tests: `4/4` passed.
- Full package discovery currently finds the same `4` Task 1 tests: `4/4` passed.
- `python tools/scene_reconstruction/build_source_inventory.py`: passed.
- `python -m compileall -q tools/scene_reconstruction`: passed.
- `git diff --check`: passed.
- Source-content hash comparison before and after rebuild: unchanged for `2005` files.
- No local server was started.

## Snapshot facts

- Inventory roots: `9`.
- Inventory files: `1970`.
- Enumerated archives: `2` (APK and ZIP).
- Discovered floors: `25` (`floor0` through the discovered non-contiguous universe, including `floor31`, `floor33`–`floor36`).
- Required missing office SEB relations remain `unknown` for `floor2`, `floor4`, `floor9`, and `floor13`.
- No SEB tail bytes or records were padded or synthesized.

## Files changed by Task 1

- `tools/scene_reconstruction/paths.py`
- `tools/scene_reconstruction/source_inventory.py`
- `tools/scene_reconstruction/build_source_inventory.py`
- `tools/scene_reconstruction/test_source_inventory.py`
- `knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json`
- `.superpowers/sdd/2026-08-12-scene-map-reconstruction/task-1-report.md`

## Fix round 1: preserve `.last_extraction.env` declarations

Changed `source_inventory.py` so `declared_paths` is keyed by the original env key. Each record now preserves `key`, exact `raw_value`, `normalized_path`, and `resolved_path`; values such as the absolute `APK_PATH` and the non-path `APK_BASE` declaration are no longer ambiguous or discarded. Added `test_preserves_extraction_env_keys_and_raw_declarations`.

Test command and output:

```text
python -m unittest discover -s tools/scene_reconstruction -p 'test_source_inventory.py' -v
Ran 5 tests in 0.174s
OK
```

Rebuild and verification command results:

```text
python tools/scene_reconstruction/build_source_inventory.py
source_hashes_unchanged True source_files 2005
declared_keys ['APK_BASE', 'APK_PATH', 'DUMP_OUT', 'OUT_FOLDER', 'SPRITE_OUT']
apk_raw_value D:\antigravity\test open ai\APK_Toolkit\game-dev-story-mod.apk
apk_normalized_path APK_Toolkit/game-dev-story-mod.apk
apk_resolved_path D:\antigravity\test open ai\APK_Toolkit\game-dev-story-mod.apk
python -m unittest discover -s tools/scene_reconstruction -p 'test_*.py' -v
Ran 5 tests in 0.159s
OK
python -m compileall -q tools/scene_reconstruction
git diff --check
```

The source-content hash comparison remained unchanged for all `2005` files across the rebuild. No source/extraction root was modified.
