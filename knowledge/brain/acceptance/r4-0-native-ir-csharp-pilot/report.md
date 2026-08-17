# R4.0 Native/ISIL → Typed IR/CFG → C# Feasibility Pilot

Decision: GO
Token: PASS_R4_0_NATIVE_IR_CSHARP_FEASIBILITY_PILOT_GO

The pilot was bounded to the deterministic 200-method reproduction and a separate 100-method hard cohort. Original C# source remained read-only and no source write was permitted.

## Gate summary

- PASS: source_gate
- PASS: reproduction_200
- PASS: six_positives
- PASS: five_negatives_rejected
- PASS: zero_known_false_positive_source_writes
- PASS: hard_attempted_100
- PASS: hard_verified_50
- PASS: hard_ownership_diverse
- PASS: hard_cfg_family_diverse
- PASS: deterministic_replay
- PASS: source_unchanged
- PASS: generated_csharp_syntax_sanity

Required positives verified: 6/6
Negative fixtures rejected: 5/5
Hard cohort verified: 55/100
Deterministic replay: PASS
Source unchanged: PASS

A GO authorizes the next full R4 boundary; full-corpus native lifting was not started by this pilot.
