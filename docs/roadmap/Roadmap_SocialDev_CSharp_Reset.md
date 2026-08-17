# Roadmap — Social Dev C# clean-room reset

Social Dev is the active source-of-truth. The previous GameDev/Virtual Game Office reconstruction was deleted and must not supply new product semantics.

## Phase 0 — Boundary and provenance

- Keep the deleted historical GameDev boundary closed; do not recreate its source, knowledge, runtime, tools, or roadmap.
- Preserve source roots read-only.
- Maintain active Social Dev provenance and validation gates.
- Fingerprint the RAR, APK, asset ZIP, and update corpus.

## Phase 1 — C# corpus audit

- Compare the RAR baseline and `1_Click_CSharp_Code update` by canonical path and SHA-256.
- Treat `data`, `game`, `game.routeSearch`, and bounded `main` as gameplay candidates.
- Treat `form` and `form/SubForm_Split` as presentation evidence.
- Treat `KairoEngine` and `Dependencies` as engine/dependency evidence.
- Keep modified, split, missing, and decompiler-damaged files explicitly labelled.

## Phase 1.5 — Evidence triage gate

- Treat the RAR extraction as the provenance anchor and the update as marker-cleaned evidence only.
- Use the load-contract and field/load candidate reports as review queues, not generated models.
- Keep human-authored scaffolds out of the active state owner; derive runtime contracts only from source-backed evidence.
- Complete the active-reference scan and retarget shared tools before calling the Social Dev tree cutover-ready.

## Phase 2 — Canonical Social Dev model

- Build structural inventories before semantic promotion.
- Separate static data, runtime state, lifecycle/save state, presentation, and assets.
- Use typed records and entity relations; do not recreate parallel primitive arrays.
- Keep `verified`, `raw_only`, `derived`, `unknown`, and `conflict` statuses with provenance.
- Keep derived code and unverified mappings out of the executable runtime.

## Phase 3 — Asset and binary validation

- Parse the assembly guide and asset indexes from the ZIP.
- Use the APK for Unity metadata and missing/contradictory asset provenance.
- Promote an asset only when its selector, identity, and source relationship are verified.
- Keep image previews and unresolved assets outside the active runtime.

## Phase 4 — Social Dev runtime

- Create `runtime/social-dev` contracts from the verified model.
- Implement scene, Camera, Room, Staff, route, animation, interaction, and visible event contracts in the order defined by `Roadmap_SocialDev_DisplayRuntime.md`.
- Add a source-free projection for the UI.
- Do not recreate or port the deleted legacy Office runtime as a compatibility layer.

## Phase 5 — Cutover

- Update README, TODO, PROJECT_STATE, and roadmap pointers to Social Dev.
- Require an active-reference scan with no GameDev dependency in the active tree.
- Run deterministic contract tests and asset provenance checks.
- The legacy archive deletion gate is complete; future work continues only from current Social Dev sources and contracts.
