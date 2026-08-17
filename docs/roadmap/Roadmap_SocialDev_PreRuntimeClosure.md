# Social Dev Pre-runtime Closure Sweep

Status: **complete**

This is a closure package, not a new numbered phase. It closes the historical
review boundary from Phase 0 through Phase 1C before the TypeScript runtime is
started. The original candidate evidence remains unchanged for provenance; the
closure matrix and contracts below are the active authority.

## Goal

Close every historical blocking review item with one of the allowed final
decisions:

- `verified` — supported by source, native, table, locale, or asset evidence;
- `derived` — a bounded architecture or behavior decision with explicit inputs;
- `deferred` — intentionally outside `display-slice-01`, with a reason;
- `quarantine` — evidence is retained but is prohibited from runtime promotion;
- `conflict` — retained only when sources disagree and no safe promotion exists.

No item may remain active as `open`, `pending_review`, or `unknown` in the
closure authority.

## Scope closed

1. Phase 0 loader/semantic review and the semantic-diff disposition.
2. Phase 0 Player/AppData split, decompiler-body policy, state boundary, and
   asset-selector boundary.
3. Phase 1 first-slice loader mappings, room/placement boundary, skill link,
   and selector promotion.
4. Phase 1B scene/behavior review carryovers.
5. Phase 1C historical review supersession by Phase 1D.
6. Canonical data, entity, and save contracts needed before runtime work.

## Active authority

- `knowledge/fixtures/accepted/semantic_review_closure.json`
- `knowledge/fixtures/accepted/load_contract_closure.json`
- `knowledge/fixtures/accepted/phase1_supersession.json`
- `knowledge/fixtures/accepted/runtime/data_contract.json`
- `knowledge/fixtures/accepted/runtime/entity_contract.json`
- `knowledge/fixtures/accepted/runtime/save_contract.json`
- `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json`

## Acceptance gate

The closure gate passes only when:

- all `21` historical review items have a closed final status;
- `blocking_items_remaining=0`, `open_items=0`, and `pending_review_items=0`;
- all five display-slice loader/field sequences match and preserve raw arrays;
- missing or mismatched loaders outside the display slice are explicit deferred
  exceptions rather than guessed mappings;
- Player/AppData are represented only through bounded contracts;
- decompiler bodies are quarantined and never copied into runtime;
- Phase 1C has a replacement matrix pointing to Phase 1D authority;
- raw C# and native evidence remain read-only inputs;
- `python tools/social-dev/test_pre_runtime_closure.py` passes.

The next active boundary after this sweep is the Vite/TypeScript runtime core.
