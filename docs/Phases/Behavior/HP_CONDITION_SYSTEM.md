# HP and Condition System

## Authority

`Staff.hp_` at offset `0xE8` is the authoritative Staff health field. `StaffData.PARAM_HP=5` names the HP parameter. The dynamic maximum is `GetBaseParam(5,0)+GetJobParam(5,level_)`.

## Proven writes and reads

- Init starts at `hp_=100`; Room.AddStaff then calls `RecoverHpMax` for new Staff or `ClampHpMax` for loaded Staff.
- `RecoverHp(value)` adds a value, clamps below zero, caps at the dynamic maximum, and clears `FLAG_SLEEPING` when full.
- `AddRecoveryHpStock` sets a 20-frame delay; `UpdateRecoveryHp` consumes stock through `RecoverHp(1)`.
- `UpdateStayHome` calls `RecoverHp(1)` directly.
- `SetHp`, clone/overwrite, save/load, and combat paths are explicit additional writers.
- `GetHpRatio` feeds low-HP door escape, work sleeping decisions, home return, and UI consumers.

## Exact-name result

No Staff `stamina_`, `energy_`, `fatigue_`, or `condition_` field was found. The expanded exact-token scan records only unrelated Player stamina, Avatar energy, EventData/UI vocabulary, or Unity binding hits; none establishes a Staff condition field. No readable ordinary-work `RecoverHp(-...)`, `hp_ -=`, or `hp_--` write was found.

## Limits

Ordinary work HP drain and the exact sleeping-stock cadence remain unknown because the decompiled broad update body is damaged. The model must not invent them.
