# Derived Staff Parameters

Status: `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`

This report is static/offline evidence only. No decompiled C# was executed and no runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.

`Staff.GetParam` is the sum of `Staff.GetBaseParam` and `Staff.GetJobParam`. The native component path includes StaffData base parameters, room equipment, desk FurnitureData parameter value, master-job bonuses, item effects, motivation scaling, and the 1..9999 clamp.

Three source-row MaxHP fixtures are recorded in `staff-derived-parameter-contract.json`; they use a neutral room/equipment context and motivation 0 so the data dependency is reproducible without inventing live state.
