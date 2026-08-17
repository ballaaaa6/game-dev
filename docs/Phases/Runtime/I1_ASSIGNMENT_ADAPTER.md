# I1 Assignment Adapter

Status: `PASS_I1_6_ASSIGNMENT_ADAPTER_API`

The adapter exposes `bind_agent`, `unbind_agent`, `assign_task`, `start_task`, `complete_task`, `fail_task`, `cancel_task`, and product-only progress updates. Expected conflicts return structured codes rather than exception-only control flow.

The adapter references `LivingRuntime` for snapshots and calls only `ProductTaskOverlayBridge.enter/exit`. It does not expose raw Staff setters. Assignment is not start; assignment is not a forced desk route; terminal commands do not delete Staff, destroy desks, send Staff home, or change HP.

Implementation: `runtime/social-dev/src/product/assignment/`.
