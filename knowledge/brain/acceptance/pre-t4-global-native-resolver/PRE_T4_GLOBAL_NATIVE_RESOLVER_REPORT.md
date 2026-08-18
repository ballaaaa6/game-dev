# Pre-T4 Global Native Resolver Experiment

Decision: `NO_GO_FULL_DECOMPILATION`. T3 remains accepted/closed and T4 started: `False`.

## Reproduced advisory measurements

- Unique unresolved method addresses: 311; PLT: 16; direct-B thunks: 16.
- Unique fixed unmanaged loads: 9074; GOT/RELA recognized: 8785.
- Advisory field comparison: `True`.

## Canonical method impact

- Canonical methods measured: 10827; resolver-touched methods: 6632.
- `GENERATED_LOW`: 7999 before → 7999 after; delta 0.
- `RESOLVED_NATIVE_NOISE` occurrences: 20216.
- Recovered semantics: 0; compiler-valid new bodies: 0.

## Bounded reconstruction

The experiment identified 234 normalization-only candidates but authorized zero promotions because address resolution is not semantic equivalence and no new proof-gated emitter was introduced.

## Decision rationale

Stop expanding the full source-recovery strategy; retain the resolver as evidence infrastructure and prefer a rebuild/behavioral-twin strategy.

The remaining dominant blockers are other decompiler issues, unresolved method targets, unresolved fixed loads, and ambiguous/virtual native targets. Original source roots, native inputs, accepted T1/T2/T3 evidence, and T4 were left untouched.
