# I2 Current Web Runtime Audit

Status: PASS_I2_1_WEB_SHELL_AUDIT

The production entrypoint is `runtime/social-dev/src/main.ts`, which mounts `createSocialDevRuntime` into `#app`. The production controller is `runtime/social-dev/src/app/runtime.ts`.

Ownership is explicit:

- `DashboardRuntime` owns the one `LivingRuntime` reference, the one I1 `AssignmentAdapter`, the combined snapshot, and subscriber publication.
- `app/runtime.ts` owns one wall-clock interval. It requests fixed logical steps only.
- `renderer/canvas-renderer.ts` remains the Canvas semantic renderer. The Canvas receives a `SimulationState` projection built from the committed LivingSnapshot.
- `product/dashboard/ui.ts` owns the DOM/CSS product control surface.
- `core/simulation.ts` remains a compatibility/test facade and is not imported by the production app controller.

Static verification found one production `createLivingRuntime` call and one production `window.setInterval` call. No second scheduler or synthetic production frame owner is present.
