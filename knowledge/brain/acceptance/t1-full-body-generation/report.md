# T1 Full-Body Generation

Status: `PASS_T1_FULL_BODY_GENERATION_CLOSED`

This is the canonical coverage-first Whole-Twin representation pass.  It preserves every canonical method identity and every directly decoded native operation while keeping source-equivalent claims limited to accepted readable source rows.

## Coverage

- Canonical universe: 641 types / 10827 methods.
- Unique canonical IDs: 10827; unique represented IDs: 10827.
- Missing IDs: 0; duplicate output IDs: 0; extra IDs: 0.

## Tiers and evidence

- Tiers: DECLARATION_ONLY=50, EXISTING_READABLE=2481, GENERATED_LOW=8291, SOURCE_LIMITED_STUB=5
- Evidence sources: declaration=50, native=8291, source=2481, source_limited=5

## Native conservation

- Expected operations: 988046; serialized operations: 988046; omitted: 0.
- Raw unknown operations: 367 (all retained as raw operations).
- Resolved/unresolved calls: 32552/96310; fields: 46900/28099.
- Native range verified: 10772; ISIL/range-uncertain: 0.

## Complexity and shared code

- Complexity median/p90/p99/max: 32.0/192/1028/15357; extreme count: 28.
- Shared native address groups: 434; extra identities: 668; maximum group size: 11.

## Compilation and replay

- Sidecar shards: 49; representation bytes: 104468452.
- Roslyn parse errors: 0; compile errors: 0; registry entries: 10827.
- Native byte audit: PASS; Google negative regressions: PASS.
- Determinism: PASS; global manifest A/B: a32c983e133f493e5d20c19ec2a7ba98df060fc15fd67ca85235f9588e7e67a0 / a32c983e133f493e5d20c19ec2a7ba98df060fc15fd67ca85235f9588e7e67a0.

## Boundary

- Original source mutation: NO.
- Unity/V8/runtime: UNCHANGED.
- Generated LOW/native IR is a Reference-Twin analysis representation, not a claim that every body is source-equivalent or that the game Twin compiles.
- Next authorized phase: `T2_WHOLE_TWIN_COMPILE_FACTORY`.
