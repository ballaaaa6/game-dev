# Social Dev Phase 2C — ActorCatalog and Readiness Report

Date: 2026-08-13
Status: **Complete**
Scope: `display-slice-01`

## Outcome

Phase 2C produced the canonical static `ActorCatalog` and closed the display/runtime readiness boundary from the approved SceneCatalog/ObjectCatalog boundary, the closed staff living-scene contract, the loader-aware English/Japanese data rows, and the indexed human asset selectors.

The contract is `pass` / `approved_for_runtime_contract`.

The package contains:

- `5` promoted StaffData records: `0–4`.
- `1` selected JobData record: `4` (`Senior Planner` / `著名ﾌﾟﾗﾝﾅｰ`).
- `1` selected SkillData record: `1` (`Loving Meetings` / `打ち合わせ好き`).
- `5` resolved human image selectors: `chara86.png` through `chara90.png`.
- `8` resolved wait/typing animation selectors: wait `10–13`, typing `23–26`.
- `1` bounded living-scene behavior profile with `35` source constants, `3` route mappings, `4` transitions/timing records, and the selected skill-effect contract.
- A deterministic source-bounded spawn fixture for `3` actors through the verified `room:0` door cell.
- Pass / approved runtime contracts for camera coordinates, actor behavior, and fixed-tick order.

## Canonical artifacts

- Runtime contract: `knowledge/fixtures/accepted/runtime/actor_catalog_contract.json`
- Evidence fixture: `knowledge/fixtures/accepted/actor_catalog_fixture.json`
- Validation: `knowledge/fixtures/accepted/actor_catalog_validation.json`
- Display-slice scope: `knowledge/fixtures/accepted/display_slice_contract.json`
- Spawn fixture: `knowledge/fixtures/accepted/actor_spawn_fixture.json`
- Readiness validation: `knowledge/fixtures/accepted/actor_spawn_validation.json`
- Runtime readiness contracts: `knowledge/fixtures/accepted/runtime/actor_spawn_contract.json`, `knowledge/fixtures/accepted/runtime/camera_coordinate_contract.json`, `knowledge/fixtures/accepted/runtime/actor_behavior_contract.json`, `knowledge/fixtures/accepted/runtime/tick_order_contract.json`
- Builder: `tools/social-dev/build_actor_catalog.py`
- Deterministic test: `tools/social-dev/test_actor_catalog.py`
- Readiness builder/test: `tools/social-dev/build_phase2c_readiness.py`, `tools/social-dev/test_phase2c_readiness.py`

Validation passed `35/35` checks.
The readiness package passed `12/12` checks with `3` spawned actors and `13` pinned source slices.

Stable hashes:

- Input manifest: `f58dc7f973388c5b63ad3d22f32da4951f3a13ea305b90484e488246c2a8090f`
- Fixture: `322b68ea77f0c5567ba6470ae63e70fa95e689e104b9e7c87973611a1967f553`
- Contract: `1268382df3f052096c2f648688d08feb0d38f868e4772a8ace1d2c97207c7a14`

Readiness contract hashes:

- Spawn: `5e8d0e7cffbcbf1145acbf976a7d1f568a098bef138b8fdc2af69f501f09abd6`
- Camera/coordinate: `094429870c590de4253d9ef0986a7c969a00cf42c624f9b495535848d1726663`
- Behavior: `3af31b5781833a204ce59a4e1b26b0191445d7ecb5856454d13179b3c13de91f`
- Tick: `d0fc4c8afc2834ee94494f9ad4d9abdce3a6b04c15974959863d609e3f5f1fad`

## Verified boundaries

Actor IDs use `actor:staff:<source_id>` and are not array-position identities. English and Japanese StaffData rows preserve the same five source IDs and row provenance. The selected staff rows all reference JobData(4) and SkillData(1); the skill relationship is promoted from the approved staff semantics contract rather than inferred from column order alone.

Human image selector identity is closed through `human/img.inf` and the indexed asset package. Wait and typing selectors are closed through `human/seb.inf`, with typing start/end frame rules retained. Frame composition, crop, scale, alpha, and binary promotion remain outside this phase.

The behavior profile retains numeric state/move/flag values as source-labelled evidence. It promotes only the bounded route dispatch, talk timing, typing/wait selector, and selected skill-effect contracts. `Staff.Update` and the damaged `GetSkill` body are not ported.

## Deferred boundary

The static ActorCatalog keeps mutable actor state outside its record shape. The separate readiness package now closes the initial source-bounded spawn boundary for three actors: the verified door cell is `(8,4)`, and the readable `Room.AddStaff` assignments produce the deterministic position `(280,-31)`, `alpha_=0`, `speed_=3`, `objIndex_=(8,4)`, and `room_=room:0`. Desk selection remains explicitly deferred because its decompiler body is not sufficiently readable; it is outside the spawn-cell gate.

The readiness package also closes the coordinate/camera offset interface, bounded actor behavior/talk trace, and one-frame fixed-tick order. The Vite/TypeScript core has not been created; it is now the next allowed boundary after this completed Phase 2C gate.

## Regression verification

The following commands passed:

```text
python -B tools/social-dev/test_phase1d_closure.py       # 18/18
python -B tools/social-dev/test_scene_catalog.py         # 22/22
python -B tools/social-dev/test_scene_native_semantics.py
python -B tools/social-dev/test_scene_semantics_review.py
python -B tools/social-dev/test_object_catalog.py        # 29/29
python -B tools/social-dev/test_actor_catalog.py         # 35/35
python -B tools/social-dev/test_phase2c_readiness.py     # 12/12
```

The native/semantics tests retain their documented `route=blocked_on_fixture_semantics` review label. The authoritative Phase 1D route fixture consumed by SceneCatalog/ObjectCatalog remains closed and the regression/readiness suite exits successfully.

## Next boundary

The next allowed boundary is the Vite/TypeScript deterministic core. Phase 2C is complete; no Vite/TypeScript core or renderer was introduced before the readiness gate passed.
