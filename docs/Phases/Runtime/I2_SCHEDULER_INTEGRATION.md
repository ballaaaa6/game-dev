# I2 Scheduler Integration

Status: PASS_I2_4_SINGLE_TICK_OWNER

The app interval is one fixed logical driver. Each scheduler step follows:

1. `LivingRuntime.tick()` exactly once.
2. The returned committed `LivingSnapshot` is retained.
3. `AssignmentAdapter.observeLiving(snapshot)` exactly once.
4. `DashboardRuntime` builds the combined dashboard snapshot and publishes subscribers.
5. The Canvas projection and DOM render use that same committed frame.

The D5 harness observed ten ticks, ten observations, ten publications, and frame 10 after ten steps. Product commands were separately verified to leave the living frame unchanged.
