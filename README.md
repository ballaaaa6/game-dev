# Social Dev clean-room runtime

This workspace rebuilds Social Dev from pinned APK/native/C#/asset evidence while keeping source, accepted contracts, generated outputs, canonical knowledge, and runtime code separate.

## Canonical topology

- `knowledge/brain/` — canonical SQLite brain, schema, graphs, reconciliation, K2 acceptance, and query exports
- `knowledge/data/original/` — local original-data authority and provenance-bound JSONL/SQLite inputs; not a Git archive
- `knowledge/generated/` — rebuildable original-data, visual, and runtime packs
- `knowledge/fixtures/accepted/` — active contracts and deterministic regression fixtures
- `knowledge/sources/` and `sources/raw/` — read-only source/extraction roots
- `knowledge/gaps/` — the closed K3 targeted missing-link queue and its canonical exports
- `legacy/` — verified historical/preflight material, never an active authority or dependency
- `runtime/social-dev/` — active browser runtime; its generated pack is a verified mirror of `knowledge/generated/original-runtime-pack/`
- `tools/social-dev/` and `docs/` — active validation tools and project reports

The Git publication boundary is documented in
`docs/state/REPOSITORY_BOUNDARY.md`; large source, binary, database, and
rebuildable forensic inputs remain local-only.

The canonical semantic database is `knowledge/brain/sqlite/social_dev_brain.sqlite`. The browser entrypoint is `runtime/social-dev/`; it loads the canonical generated runtime pack and the approved native floor00 scene.

## Verification

Read [AGENTS.md](AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), and [TODO.md](TODO.md) before continuing work. The primary offline checks are:

```powershell
python -B tools/social-dev/test_k2_unified_brain.py
python -B tools/social-dev/test_game_knowledge_g0_g1.py
python -B tools/social-dev/test_runtime_contract_freeze.py
python -B tools/social-dev/test_i0_living_runtime.py --static-only
```

The active runtime smoke URL, when a repository-owned server is already available, is `http://127.0.0.1:4173/?auto=0`.
