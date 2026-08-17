# HP Data Dependency

Status: `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`

This report is static/offline evidence only. No decompiled C# was executed and no runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.

`Staff.hp_` is the saved mutable life resource at dump offset `0xE8`. `StaffData.PARAM_HP` is 5. Max HP is `GetBaseParam(5,0) + GetJobParam(5,level_)`; HP ratio uses integer division against that same max.

Low HP at `<=5%` routes to the door; home recovery returns at `>=40%`. Equipment recovery adds stock after use completion and delayed recovery consumes one stock per readable tick. Ordinary work HP drain is explicitly `UNKNOWN`.
