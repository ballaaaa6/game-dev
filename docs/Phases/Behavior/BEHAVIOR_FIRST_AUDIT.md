# Behavior-First Forensic Audit

Status: `PASS_BEHAVIOR_MODEL_WITH_SOURCE_LIMITS`.

This phase reconstructs the original autonomous Staff living/execution system from the pinned IL2CPP dump, decompiled C# declarations/call sites, and static data. It does not reconstruct a renderer and does not promote the dashboard UI into behavior authority.

## Boundary

- V8 started: **NO**
- Visual work performed: **NO**
- Production renderer changed: **NO**
- MapChip changed: **NO**
- Emulator/ADB/live server/network: **NO**
- Subagents: **NO**

The phase read and reconciled the prior Phase 1D closure, route/passMap fixtures, Staff living-scene contract, historical candidate artifacts, the pinned dump, Staff/Room/ObjChip source, StaffData/JobData/SkillData/EventData, and all 103 FurnitureData records.

## Findings

- `Staff` has an authoritative `hp_` field at dump offset `0xE8`; `StaffData.PARAM_HP` is exactly `5`.
- The maximum HP formula is `GetBaseParam(5, 0) + GetJobParam(5, level_)`.
- Low HP (`<=5%`) sends Staff to the door; `STATE_STAY_HOME` recovers one HP per readable tick and returns at `>=40%`.
- Work autonomy chooses typing, equipment, talk, or sleeping through readable bounded branches; exact modulo cadence remains source-limited.
- No Staff field named `stamina_`, `energy_`, `fatigue_`, or `condition_` was found. No readable ordinary-work `RecoverHp(-...)`, `hp_ -=`, or `hp_--` write was found; work drain remains unknown.
- FurnitureData classification is source-based: EQUIPMENT_NO_HP_EFFECT_PROVEN=43, DOOR_RECORD=1, WORKSTATION=10, RECOVERY_EQUIPMENT=49. No rest/social role is inferred from a record name or sprite.
- Native route, passMap, standing-position, raw object-chip, and reservation authorities are preserved.

## Required evidence

The machine-readable contracts are in `knowledge/fixtures/accepted/behavior-first/`; the checkpoint ledger records BF.0 through BF.19. The broad Staff.Update and OnArriveGoal indirect dispatches remain explicitly unresolved.

## Stop

Do not begin visual correction, V8, renderer cutover, MapChip work, emulator/ADB/live-server work, or source-root edits from this handoff.
