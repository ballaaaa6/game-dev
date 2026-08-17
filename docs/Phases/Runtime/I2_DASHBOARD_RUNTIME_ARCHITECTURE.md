# I2 Dashboard Runtime Architecture

Status: PASS_I2_3_DASHBOARD_RUNTIME_FACADE

`DashboardRuntime` is the in-process facade in `runtime/social-dev/src/product/dashboard/runtime.ts`. Its constructor receives the production `LivingRuntime` and creates exactly one `AssignmentAdapter` against that same object. The adapter retains I1 task/error semantics; no `LivingStaff` product fields are added.

Commands publish a new combined read model without calling `LivingRuntime.tick()`. The scheduler path commits a single living snapshot, observes it once, then publishes it. The UI consumes typed command results and re-renders from the next committed snapshot.

The bridge is `PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING`: RUNNING is a product lifecycle status, not a living state and not backend execution.
