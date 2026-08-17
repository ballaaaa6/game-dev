# Repository Boundary

This repository is a lightweight live mirror of the active Social Dev project.

Git contains the active runtime source, tests, configuration, selected
runtime-required assets and contracts, active builders/validators, schemas and
manifests, compact canonical-state exports, acceptance summaries, project
state, roadmaps, and persistent repository instructions.

The local forensic vault contains the original APK/RAR/ZIP inputs, extracted
C# trees, native binaries, raw metadata, bulk original assets, large source
and reverse-engineering evidence, the canonical SQLite working database, and
rebuildable original data/runtime/visual packs. These roots remain read-only
and local-only:

- `sources/`
- `knowledge/sources/`
- `legacy/`
- `knowledge/brain/sqlite/`
- `knowledge/data/original/`
- large generated pack files under `knowledge/generated/`

Hashes and provenance manifests committed to Git refer back to those locally
preserved pinned sources. Small intentional provenance/hash manifests and
reasonably sized runtime-required product contracts or assets may be published;
raw source vault material and rebuildable/local-only outputs may not.
