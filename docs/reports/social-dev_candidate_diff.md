# Social Dev candidate C# diff

This report measures the gameplay/lifecycle slice only: `data`, `game`, `game.routeSearch`, and `main`. It does not promote semantics or treat a marker reduction as proof of correctness.

## Result

| Status | Files |
|---|---:|
| exact_match | 12 |
| modified | 60 |

## Modified-file marker direction

| Update marker direction | Files | Interpretation |
|---|---:|---|
| reduced | 60 | possible cleanup; still needs semantic review |
| same | 0 | layout/content changed without marker-count change |
| increased | 0 | possible added decompiler damage or expanded extraction |

## Largest changed files by absolute byte delta

| File | Bytes Δ | Lines Δ | Issue markers Δ | Array-field lines Δ |
|---|---:|---:|---:|---:|
| `main/AppData.cs` | -479,369 | -4,217 | -4,217 | +0 |
| `game/Player.cs` | -346,970 | -3,687 | -3,687 | +0 |
| `game/Staff.cs` | -155,021 | -1,702 | -1,702 | +0 |
| `game/Meeting.cs` | -96,896 | -1,084 | -1,084 | +0 |
| `game/ObjChip.cs` | -76,508 | -786 | -786 | +0 |
| `game/Room.cs` | -58,911 | -656 | -656 | +0 |
| `game/Camera.cs` | -53,438 | -604 | -604 | +0 |
| `game/Proposal.cs` | -32,365 | -355 | -355 | +0 |
| `game/Avatar.cs` | -31,134 | -351 | -351 | +0 |
| `game/Enemy.cs` | -21,762 | -237 | -237 | +0 |
| `data/IdeaData.cs` | -21,104 | -245 | -245 | +0 |
| `game.routeSearch/Astar.cs` | -21,099 | -228 | -228 | +0 |
| `data/PlatformData.cs` | -16,098 | -190 | -190 | +0 |
| `data/ItemData.cs` | -15,431 | -172 | -172 | +0 |
| `main/RecordStoreResume.cs` | -15,103 | -147 | -147 | +0 |
| `game/MapChip.cs` | -13,720 | -155 | -155 | +0 |
| `main/Main.cs` | -11,671 | -147 | -147 | +0 |
| `data/SaleTaskData.cs` | -11,390 | -129 | -129 | +0 |
| `data/HelperData.cs` | -10,051 | -120 | -120 | +0 |
| `game/FriendGameData.cs` | -9,311 | -113 | -113 | +0 |
| `game/Company.cs` | -9,281 | -107 | -107 | +0 |
| `data/PlatformContentData.cs` | -7,103 | -83 | -83 | +0 |
| `game/Fan.cs` | -6,417 | -75 | -75 | +0 |
| `game/Treasure.cs` | -5,750 | -63 | -63 | +0 |
| `data/DataManager.cs` | -5,384 | -66 | -66 | +0 |
| `data/CompanyData.cs` | -5,163 | -60 | -60 | +0 |
| `data/StaffData.cs` | -4,992 | -60 | -60 | +0 |
| `data/FurnitureData.cs` | -4,941 | -59 | -59 | +0 |
| `game/GameRecord.cs` | -4,903 | -58 | -58 | +0 |
| `data/ScheduleData.cs` | -4,791 | -57 | -57 | +0 |

## Decision

The update corpus is not promoted wholesale. Only the candidate slice is measured here; form/UI splits and dependency rewrites remain separate evidence. A reduced decompiler-marker count is a review signal, not a correctness verdict.
