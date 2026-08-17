# I1 Living Interruption Policy

Status: `PASS_I1_8_INTERRUPTION_RETENTION`

Equipment, talk, low-HP home/return, and desk destruction/reacquisition are read-only living observations. While a product task is active, its identity, status, external progress, and binding persist. The adapter emits deterministic interruption/resume events but never turns a living interruption into `PAUSED`, `FAILED`, or `CANCELLED`.

Only explicit product commands complete, fail, or cancel a task. Backend continue/pause/slow/wait policy remains outside I1.
