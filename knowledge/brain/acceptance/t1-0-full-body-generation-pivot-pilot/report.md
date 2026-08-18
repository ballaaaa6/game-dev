# T1.0 Full-Body Generation Pivot Pilot

Decision: `GO`
Token: `PASS_T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_GO`

This is a sidecar-only canonical 500-method pilot. It does not overwrite the Twin source, the read-only C# roots, Unity/V8 runtime code, or the original evidence roots.

## Cohort composition

- `BASELINE_READABLE`: 75
- `CFG_DEFERRED`: 175
- `NATIVE_DEFERRED`: 175
- `IDENTITY_MECHANICAL_SOURCE_LIMITED`: 50
- `EXTREME_COMPLEXITY`: 25
- Ownership: GAME_FIRST_PARTY=249, KAIRO_ENGINE=251

## Representation and conservation

- Coverage: 500/500 emitted; missing=0
- Tiers: EXISTING_READABLE=75, GENERATED_HIGH=49, GENERATED_LOW=16, GENERATED_MEDIUM=355, SOURCE_LIMITED_STUB=5
- Native instructions decoded: 117876
- Native instructions represented: 117876
- Omitted instructions: 0 (all selected native-backed methods explain the catalog convention)
- Resolved direct calls: 3873; unresolved direct calls: 11713
- Resolved field accesses: 16658; unresolved field accesses: 2427
- Branch targets: 18500; raw native fallback operations: 34

## Complexity and semantic quality

- Native-backed complexity: median=41, p90=332, p99=3958, max=8693
- High-level quality: source-oracle exact=75, structural confirmed=49, rejected/deferred to IR=376
- Extreme cohort: 1888–8693 native instructions

## Verification

- Sidecar Roslyn parse: PASS
- Sidecar analysis assembly compile: PASS
- Deterministic replay: PASS
- Google negative fixtures: REJECTED; false-positive count=0
- Source mutation: NO

## Boundary

No 10,827-method generation, T2 compile factory, semantic uplift, runtime change, or legacy R4 mass lift was started by this pilot.
Next authorized phase on GO: `T1_FULL_BODY_GENERATION`.
