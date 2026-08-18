# T2 Whole-Twin Compile Factory Report

Status: `PASS_T2_WHOLE_TWIN_COMPILE_FACTORY_CLOSED`

The canonical input gate passed with 641 owned types, 10827 methods, and 10251 fields. The 500-method canary compiled with zero parse/compile diagnostics and exact T1 linkage. The full structural factory compiled all 10827 methods with zero parse/compile diagnostics.

Representation tiers: 2481 existing-readable, 8291 generated-low, 50 declaration-only, and 5 source-limited stubs. Every generated method identity is linked to its exact T1 representation hash and segment descriptors; operation conservation and omitted-operation checks pass.

The bounded readable-body probe attempted 200 deterministic existing-readable bodies. It produced 44 direct compile successes and 156 rejected bodies. This diagnostic result is non-blocking by design; T3 owns source-like uplift.

Canary and full replay hashes, registry hashes, and deterministic assembly hashes pass. Original source identity is unchanged; semantic uplift is not started; Unity/V8/runtime work is untouched. The next authorized boundary is T3 source-like uplift.
