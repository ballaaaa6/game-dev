# Social Dev Phase 1D — Native scene-semantics closure report

Date: 2026-08-13

Status: **pass — Phase 1D is complete for entry into Phase 2; the later Phase 2A–2C catalogs and pre-runtime closure are also complete**

Closure validation passed `18/18` checks from the APK, asset ZIP, current C# source, and deterministic fixtures built from real data, without executing decompiled C# or native code in the web runtime.

## Main results

| Gate | Result |
|---|---|
| type-4 `passMap_` | `RoomData(0)` anchor `(4,2)` + `FurnitureData(0)` passMap `9×9`; matrix and probes pass |
| `IsPassable` | zero cell → `true`; all selected cells nonzero → `false`; 3×3 footprint |
| Astar neighbor/goal filter | occupied type-2, false type-4, and type-6 reject; goal flags `1/2/4` and equipment-direction mapping pass |
| real route | `(8,4) → (7,4) → (6,4)`, 2 steps, complete provenance |
| asset selectors | FurnitureData `103` rows + StaffData `141` rows × English/Japanese; unresolved `0` |
| staff semantics | state/move/flags, route dispatch, typing/wait animation, and SkillData(1) effect contract pass |

## Native/source provenance

- APK: `sources/raw/Social_Dev_Story_v2.5.1.apk`
- APK SHA-256 is pinned in `phase1d_closure.json`.
- Metadata version `31`, architecture `arm64-v8a`.
- Reviewed native methods include `Room.PlaceObj`, `Room.SetupBigChipsParent`, `ObjChip.IsPassable`, `Astar._searchRoute`, and public `Astar.SearchRoute`.
- RVA/file-offset mappings for the reviewed ELF segment are stored in the native evidence package.
- Source roots are read-only evidence; generated outputs are under `knowledge/fixtures/accepted/`.

## Asset-selector closure

`seb_`, `img_`, and `subSeb_` were checked from fully parsed `FurnitureData`/`StaffData` rows in both locales and cross-referenced with `chip/seb.inf`, `chip/img.inf`, and `human/img.inf` in the same ZIP. Typing/wait animation uses the real `human/seb.inf` and closes mapping IDs `23–26` and `10–13`.

This closes selector identity for the data rows used by the scene. It does not claim that every derived asset in the `3542`-row inventory is now a runtime catalog.

## Staff living-scene closure

Only semantics required to make staff visibly alive are closed: state/move/flag labels, route-flag dispatch, bounded visible transitions, talk timer, typing/wait selector, and selected `SkillData(1)` shared by staff `0–4` (`type=10`, `effects_[8][0]=150`, passive flag).

The complete `Staff.Update` and decompiler-damaged `GetSkill` lookup were not ported as runtime algorithms; they will be redesigned in Phase 2 from this contract.

## Authoritative files

- `knowledge/fixtures/accepted/phase1d_closure.json`
- `knowledge/fixtures/accepted/phase1d_passmap_fixture.json`
- `knowledge/fixtures/accepted/phase1d_route_fixture.json`
- `knowledge/fixtures/accepted/asset_selector_contract.json`
- `knowledge/fixtures/accepted/staff_semantics_contract.json`
- `knowledge/fixtures/accepted/phase1d_closure_validation.json`
- `tools/social-dev/build_phase1d_closure.py`
- `tools/social-dev/test_phase1d_closure.py`

## Phase 2 boundary

The later Phase 2A–2C work created the canonical catalogs, deterministic
fixtures, camera/coordinate, behavior, and fixed-tick contracts. The
Pre-runtime Closure Sweep then reconciled the historical Phase 0–1C review
queues without reopening this authority. The next work is the Vite/TypeScript
runtime core.
