# Social Dev Load contract candidates

This report pairs each DataManager registry entry with the C# `Load(StringArrayStream)` reader sequence and English table row shape. It does not label columns.

| Status | Files |
|---|---:|
| `candidate` | 41 |
| `load_method_missing` | 2 |

| Registry | Type | Reader calls | English rows | Column counts |
|---|---|---:|---:|---|
| `areaData_` | `AreaData` | 9 | 6 | `{23: 6}` |
| `avatarEventData_` | `AvatarEventData` | 4 | 121 | `{16: 1, 20: 1, 21: 2, 22: 1, 24: 1, 25: 110, 28: 5}` |
| `avatarTalkData_` | `AvatarTalkData` | 5 | 12 | `{6: 12}` |
| `awardData_` | `AwardData` | 12 | 27 | `{16: 27}` |
| `companyData_` | `CompanyData` | 10 | 59 | `{22: 18, 25: 10, 31: 10, 34: 8, 37: 13}` |
| `contentMatchListData_` | `ContentMatchListData` | 3 | 100 | `{50: 100}` |
| `downloadEventData_` | `DownloadEventData` | 6 | 20 | `{6: 20}` |
| `enemySkillData_` | `EnemySkillData` | 9 | 20 | `{14: 20}` |
| `eventData_` | `EventData` | 4 | 383 | `{7: 256, 10: 61, 12: 1, 13: 20, 14: 1, 15: 1, 16: 28, 18: 3, 19: 1, 22: 2, 23: 2, 26: 7}` |
| `eventMessageData_` | `EventMessageData` | 3 | 69 | `{3: 69}` |
| `favoriteData_` | `FavoriteData` | 4 | 21 | `{5: 7, 6: 10, 7: 1, 9: 3}` |
| `festivalData_` | `FestivalData` | 5 | 56 | `{5: 56}` |
| `furnitureData_` | `FurnitureData` | 21 | 103 | `{26: 90, 116: 13}` |
| `gameDexData_` | `GameDexData` | 7 | 7 | `{11: 1, 14: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1}` |
| `hardwareData_` | `HardwareData` | 8 | 4 | `{12: 4}` |
| `helpTexts_` | `string` | 0 | 1 | `{1: 1}` |
| `helperData_` | `HelperData` | 16 | 19 | `{18: 19}` |
| `historyData_` | `HistoryData` | 11 | 117 | `{16: 117}` |
| `ideaData_` | `IdeaData` | 22 | 172 | `{49: 172}` |
| `installData_` | `Install` | 0 | 27 | `{12: 27}` |
| `itemData_` | `ItemData` | 21 | 137 | `{21: 90, 25: 47}` |
| `jobData_` | `JobData` | 12 | 30 | `{39: 30}` |
| `loginBonusData_` | `LoginBonusData` | 2 | 30 | `{2: 30}` |
| `mailData_` | `MailData` | 11 | 191 | `{14: 5, 17: 52, 18: 39, 19: 94, 21: 1}` |
| `mailWordData_` | `MailWordData` | 5 | 769 | `{5: 769}` |
| `managementData_` | `ManagementData` | 15 | 16 | `{29: 16}` |
| `managementEventData_` | `ManagementEventData` | 8 | 23 | `{10: 23}` |
| `methodMatchListData_` | `MethodMatchListData` | 3 | 25 | `{50: 25}` |
| `newsData_` | `NewsData` | 3 | 1 | `{3: 1}` |
| `platformContentData_` | `PlatformContentData` | 14 | 20 | `{31: 20}` |
| `platformData_` | `PlatformData` | 18 | 12 | `{48: 12}` |
| `prizeData_` | `PrizeData` | 6 | 26 | `{7: 4, 8: 10, 9: 5, 10: 3, 12: 4}` |
| `profileData_` | `ProfileData` | 7 | 16 | `{12: 16}` |
| `releaseEventData_` | `ReleaseEventData` | 8 | 27 | `{12: 27}` |
| `roomData_` | `RoomData` | 14 | 18 | `{234: 18}` |
| `rouletteData_` | `RouletteData` | 4 | 111 | `{4: 111}` |
| `saleTaskData_` | `SaleTaskData` | 3 | 21 | `{23: 21}` |
| `scheduleData_` | `ScheduleData` | 16 | 32 | `{33: 9, 34: 15, 35: 2, 36: 6}` |
| `skillData_` | `SkillData` | 10 | 36 | `{56: 36}` |
| `staffData_` | `StaffData` | 21 | 141 | `{29: 99, 32: 42}` |
| `talkData_` | `TalkData` | 4 | 572 | `{4: 226, 5: 202, 6: 89, 7: 33, 8: 20, 9: 2}` |
| `todayEventData_` | `TodayEventData` | 4 | 20 | `{8: 20}` |
| `trophyData_` | `TrophyData` | 7 | 75 | `{9: 75}` |

## Gate

Column meanings remain unknown until the loader sequence, table bytes, language variants, and assembly-guide rules are reconciled. These candidates are not runtime data yet.
