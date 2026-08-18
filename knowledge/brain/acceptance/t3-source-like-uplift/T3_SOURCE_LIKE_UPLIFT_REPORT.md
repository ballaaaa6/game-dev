# T3 Source-Like Uplift

Status: `PASS_T3_SOURCE_LIKE_UPLIFT_CLOSED`

The T3 runner profiled every canonical method exactly once, retained T1 identity/segment provenance, and promoted only exact source bodies or mechanically proven straight-line native patterns that survived whole-Twin compilation.

## Corpus

- Types: 641; methods: 10827; fields: 10251; T1 operations: 988046.
- Original tiers: `{'DECLARATION_ONLY': 50, 'EXISTING_READABLE': 2481, 'GENERATED_LOW': 8291, 'SOURCE_LIMITED_STUB': 5}`.
- Promotions retained: 990; candidate rejections: 2; candidate pool: 992.
- Semantic tiers after T3: `{'DECLARATION_ONLY': 50, 'EXISTING_READABLE': 1783, 'GENERATED_LOW': 7999, 'SOURCE_LIKE_EXACT': 990, 'SOURCE_LIMITED_STUB': 5}`.

## Pre-T3 hygiene

- Status: `PASS`. The stale prework signature count was 467; the canonical builder and payload both report 614.

## Canary and waves

- Canary: 400 methods; ownership `{'GAME_FIRST_PARTY': 156, 'KAIRO_ENGINE': 244}`; all available dimensions covered: `True`.
- `canary`: compile pass `True`, errors `0`, active `35`.
- `wave-a-readable`: compile pass `True`, errors `0`, active `698`.
- `wave-b-simple`: compile pass `True`, errors `0`, active `990`.
- `wave-c-typed-ir`: compile pass `True`, errors `0`, active `990`.
- `wave-d-structured`: compile pass `True`, errors `0`, active `990`.
- `final`: compile pass `True`, errors `0`, active `990`.

## Negative regressions

- Status: `PASS`; all named rejection/identity/arithmetic checks: `True`.

## Validation

- Gates: `{'pre_t3_hygiene': True, 'canonical_universe': True, 'full_corpus_profile_exact_once': True, 'canary_compile': True, 'wave_compiles': True, 'final_compile': True, 'exact_t1_linkage': True, 'negative_regressions': True, 'deterministic_replay': True, 'semantic_tier_arithmetic': True, 'all_gates_pass': True, 'status': 'PASS'}`.

Next phase: `T4_WHOLE_TWIN_VALIDATION` when the PASS token is accepted.
