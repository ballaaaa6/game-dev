# Social Dev Character Metadata Catalog

## Outcome

The full source-derived character metadata package is implemented and approved for runtime lookup.

- `141` `StaffData` records are retained with English/Japanese names, all loaded source fields, job and skill references, source flag bits, and human image selector references.
- `19` `HelperData` records are retained as a separate role. They are not merged into the staff instance catalog.
- `30` `JobData` and `36` `SkillData` records are included so every staff relation resolves locally.
- The named special staff records remain in the full `StaffData` range. Assistant-shaped source rows are retained and explicitly marked as internal assistant templates.
- All `141` StaffData image selectors resolve to `105` unique human image identities. Helper image selectors preserve resolved, absent, and deferred scope statuses without inventing unresolved assets.

## Storage policy

The evidence fixture keeps field-level parser metadata, row hashes, source references, and selector provenance. The runtime contract is a compact projection containing static values and references only.

Mutable actor state is intentionally excluded from this catalog. Instance id, level, experience, current parameters/job, room/desk, position, lifecycle, route, facing, and animation frame remain owned by `ActorState` and are created lazily when an actor is spawned or displayed.

The current five-actor `ActorCatalog` remains the bounded room:0 display slice. The new full catalog is loaded separately as `CharacterMetadata` and does not change the active scene actor list.

## Shared capability layer

Character readiness now uses a hybrid model:

- `human-staff-v1` is one shared capability profile for all `141` StaffData records, including the named special range and assistant-shaped templates. The character record supplies the image selector; the profile supplies action/direction selector lookup.
- `helper-record-v1` is a separate HelperData profile. Helper records retain portrait, dialogue, and effect metadata without being silently promoted to employee movement or Staff ActorState behavior.
- `avatar-v1` reserves the body/head composition boundary, and `event-only-v1` reserves non-staff scene entities. They are explicit deferred families, not inferred staff variants.
- The central profile closes native human `wait`, `move`, and `typing` selectors in four directions. The bounded display `talk` mapping explicitly reuses `typing`; `work`, `equipment`, and related states expose explicit fallbacks; `fly_away` remains deferred because no promoted native selector is closed for it.
- `resolveCharacter`, `resolveCharacterAction`, and `createCharacterSpawnPlan` provide the lazy lookup path. Calling a character does not construct every character at boot: it resolves static metadata and a shared profile, then creates mutable `ActorState` only when a scene actually spawns the instance.

This keeps per-character data small: image selector, identity, source fields, relations, and optional override. Animation logic is shared by profile and action/direction; a per-character animation map is only added when native evidence proves a real exception.

The full profile contract is intentionally separate from the five-actor room display contract. It prepares every character for lookup while the dedicated character asset catalog supplies exact PNG/SEB promotion and decoded multilayer frame composition through a lazy renderer boundary.

## Artifacts

- Runtime contract: `knowledge/fixtures/accepted/runtime/character_metadata_contract.json`
- Shared capability contract: `knowledge/fixtures/accepted/runtime/character_capability_contract.json`
- Full human asset contract: `knowledge/fixtures/accepted/runtime/character_asset_manifest.json`
- Full evidence fixture: `knowledge/fixtures/accepted/character_metadata_fixture.json`
- Capability fixture/validation: `knowledge/fixtures/accepted/character_capability_fixture.json`, `knowledge/fixtures/accepted/character_capability_validation.json`
- Validation: `knowledge/fixtures/accepted/character_metadata_validation.json`
- Builder: `tools/social-dev/build_character_metadata.py`
- Capability builder: `tools/social-dev/build_character_capabilities.py`
- Regression test: `tools/social-dev/test_character_metadata.py`
- Capability regression test: `tools/social-dev/test_character_capabilities.py`
- Runtime resolver: `runtime/social-dev/src/catalog/character-resolver.ts`
- Lazy character asset/frame adapter: `runtime/social-dev/src/assets/character-assets.ts`
- Full-character roadmap: `docs/roadmap/Roadmap_SocialDev_FullCharacterAssets.md`

## Verification

- Character metadata validation: `13/13` checks passed.
- Character capability validation: `14/14` checks passed (`4` profiles, `141` StaffData bindings, `19` HelperData bindings, `35` human SEB selectors, `16` native action groups).
- Full human asset validation: `10/10` checks passed (`105` PNGs, `35` SEBs, `48` layers, `334` decoded records, `30` explicit control records).
- Python character metadata regression: passed.
- Python capability regression: passed.
- Existing ActorCatalog regression: `35/35` checks passed.
- TypeScript typecheck: passed.
- Vitest: `38/38` tests passed.
- Vite production build: passed.
