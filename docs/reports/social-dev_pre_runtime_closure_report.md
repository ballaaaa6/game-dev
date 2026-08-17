# Social Dev Pre-runtime Closure Sweep Report

## Status

**Complete.** The historical Phase 0 through Phase 1C review boundary is now
closed for the display-slice runtime entry. This work does not claim that every
field in the original application has a known product meaning. It records a
safe final decision for every review item and prevents out-of-scope or damaged
evidence from entering runtime contracts.

## Closure result

| Boundary | Result |
|---|---|
| Phase 0 review queue | 6/6 items closed |
| Phase 1 first-slice review | 4/4 blocking items closed |
| Phase 1B scene/behavior review | 8/8 blocking items closed |
| Phase 1C historical review | 3/3 items superseded and closed |
| Total closure matrix | 21/21 closed, 0 open, 0 pending, 0 blocking remaining |

Final decisions are `13 verified`, `6 derived`, and `2 quarantine`. Loader
exceptions outside the display slice are recorded as explicit `deferred`
exceptions in the load contract.

## Phase 0 closure

The semantic diff and cleanup evidence cover all `72` files in the declared
scope: `44` data files, `23` game files, `2` route-search files, and `3`
lifecycle files. The comparison records `12` exact files and `60` marker-only
changes after normalization; no content change beyond the decompiler marker
cleanup is promoted as a semantic repair.

The five display-slice loader types (`RoomData`, `FurnitureData`, `StaffData`,
`JobData`, and `SkillData`) have matching reader and field-assignment
sequences. Array values remain raw/framed and are not zipped into invented
semantics. Two missing loaders and three count-mismatch rows outside the slice
are explicit deferred exceptions.

`Player` and `AppData` are not ported as monoliths. The entity contract assigns
their bounded responsibilities to `WorldContext`, `Clock`, `EventQueue`, and
`PresentationEffects`. `DataManager.Load`, `Room.Update`, `Staff.Update`, and
`Astar.SearchRoute` are quarantined as evidence boundaries; new runtime code
must be written from the approved contracts.

## Phase 1 and Phase 1B closure

The original candidate packages remain available as historical evidence. Their
display-slice claims are reconciled to the already-approved Phase 1D,
SceneCatalog, ObjectCatalog, ActorCatalog, asset-selector, staff behavior, and
tick contracts.

- Room 0 identity, map indexing, door relation, bounded placement, and the
  three-actor entry fixture are closed.
- First-slice loader framing and selected field assignments are closed without
  guessing after-array semantics.
- `StaffData.jobId_ → JobData(4)` and `StaffData.skill_ → SkillData(1)` are
  source/locale/consumer-backed for the selected actors.
- Furniture, staff, wait, and typing selectors used by the display slice are
  resolved with no unresolved selectors.
- Numeric state names remain source labels; only the bounded living-scene
  transitions are runtime-authorized.

Full automatic furniture placement, management state, and other non-visible
application systems are explicitly not promoted by this closure.

## Phase 1C supersession

`phase1_supersession.json` maps the three historical Phase 1C blockers to the
authoritative Phase 1D evidence:

1. passMap and standing-position semantics;
2. route goal filter and cardinal neighbor policy;
3. asset-selector carryover.

The old package is preserved as historical evidence and is no longer an active
review queue.

## Verification

The repeatable closure gate is:

```powershell
python tools/social-dev/test_pre_runtime_closure.py
```

It rebuilds the package, checks all `21` closure mappings, validates the data,
entity, save, and supersession contracts, and confirms that no runtime core or
renderer has been created before the gate.

## Next boundary

The pre-runtime gate is complete. The next work is the Vite/TypeScript core,
followed by the Canvas/DOM renderer and screenshot/behavior-trace gates.
