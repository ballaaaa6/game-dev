# I1 Original Work Regimes

Status: `PASS_I1_1_ORIGINAL_WORK_REGIMES`

The original no-project regime is autonomous office life. A Staff can own a desk, route, sit, enter `STATE_WORK`, type, use equipment, talk, recover, go home at low HP, return, and reacquire a desk. `STATE_WORK` is not a product task.

Planning is a player-wide phase: `Player.StartPlanning()` calls `Room.OnStartPlanning()`, which reaches every room Staff; updates flow through `Player.UpdatePlanning` → `Room.UpdatePlanning` → `Staff.UpdatePlanning2`; completion flows through `Player.IsCompletedPlanning()` → `Room.OnEndPlanning()` → `Staff.OnEndPlanning()`. It changes planning flags/rate/quality, not an arbitrary task identity.

Develop is distinct. `Staff.Update()` checks `state_ == 12` and calls native `UpdateDevelop` before ordinary recovery and low-HP office dispatch. Develop owns cloned Staff objects, proposal/step parameters, `developState_`, progress fields, HP/down behavior, and a separate enemy interruption path.

Evidence: `original-work-regime-matrix.json`, `source-reverification.json`, and the frozen I0/R0 contracts.
