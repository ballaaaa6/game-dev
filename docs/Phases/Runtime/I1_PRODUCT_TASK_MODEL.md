# I1 Product Task Model

Status: `PASS_I1_5_PRODUCT_STATE_SEPARATION`

`AgentBinding` maps an explicitly chosen `externalAgentId` to one existing `staffId`. `TaskRecord` owns `externalTaskId`, agent/staff references, `ASSIGNED | RUNNING | COMPLETED | FAILED | CANCELLED`, label, external progress, bridge mode, and deterministic sequence metadata.

No external ID or product status is added to `LivingStaff`. Product progress never overwrites `planningRate`, `planQuality`, `developState_`, or native gauges. No original save schema is modified. No `PAUSED` status is introduced in I1.
