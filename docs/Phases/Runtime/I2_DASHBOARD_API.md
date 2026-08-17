# I2 Dashboard API

Status: PASS_I2_6_TYPED_API

The facade exposes typed methods for `bindAgent`, `unbindAgent`, `assignTask`, `startTask`, `updateTaskProgress`, `completeTask`, `failTask`, and `cancelTask`, plus `execute` for the discriminated I1 command union. Queries are `getSnapshot`, `getDashboardReadModel`, `getStaffRoster`, `getBindings`, `getTasks`, and `getEvents`. `subscribe(listener)` returns a disposer.

I1 rejection codes are preserved. Query results are defensive copies with deterministic ordering. `lastCommandResult` is presentation-only and excluded from replay digest calculation.
