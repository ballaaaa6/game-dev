# Social Dev data schema candidate

This is a source-backed candidate, not an approved runtime schema. Field names/types are copied from the structural inventory; semantic meaning remains `unknown`.

Inventory fingerprint: `1b2f9396f2768545d4f719022fb1b116df0de9a5347fb46337a8417e1257093a`

## Counts

| Item | Count |
|---|---:|
| DataManager typed arrays | 43 |
| Data record classes | 44 |
| Data fields | 1112 |
| Lifecycle hooks | 117 |

## DataManager registry

| Field | Element type | Source | Semantic status |
|---|---|---|---|
| `areaData_` | `AreaData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:53` | `unknown` |
| `avatarEventData_` | `AvatarEventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:43` | `unknown` |
| `avatarTalkData_` | `AvatarTalkData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:41` | `unknown` |
| `awardData_` | `AwardData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:63` | `unknown` |
| `companyData_` | `CompanyData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:71` | `unknown` |
| `contentMatchListData_` | `ContentMatchListData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:75` | `unknown` |
| `downloadEventData_` | `DownloadEventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:87` | `unknown` |
| `enemySkillData_` | `EnemySkillData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:55` | `unknown` |
| `eventData_` | `EventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:21` | `unknown` |
| `eventMessageData_` | `EventMessageData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:17` | `unknown` |
| `favoriteData_` | `FavoriteData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:61` | `unknown` |
| `festivalData_` | `FestivalData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:97` | `unknown` |
| `furnitureData_` | `FurnitureData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:47` | `unknown` |
| `gameDexData_` | `GameDexData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:73` | `unknown` |
| `hardwareData_` | `HardwareData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:57` | `unknown` |
| `helpTexts_` | `string[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:23` | `unknown` |
| `helperData_` | `HelperData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:65` | `unknown` |
| `historyData_` | `HistoryData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:39` | `unknown` |
| `ideaData_` | `IdeaData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:29` | `unknown` |
| `installData_` | `Install[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:83` | `unknown` |
| `itemData_` | `ItemData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:25` | `unknown` |
| `jobData_` | `JobData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:59` | `unknown` |
| `loginBonusData_` | `LoginBonusData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:35` | `unknown` |
| `mailData_` | `MailData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:93` | `unknown` |
| `mailWordData_` | `MailWordData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:95` | `unknown` |
| `managementData_` | `ManagementData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:67` | `unknown` |
| `managementEventData_` | `ManagementEventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:99` | `unknown` |
| `methodMatchListData_` | `MethodMatchListData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:77` | `unknown` |
| `newsData_` | `NewsData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:19` | `unknown` |
| `platformContentData_` | `PlatformContentData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:79` | `unknown` |
| `platformData_` | `PlatformData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:51` | `unknown` |
| `prizeData_` | `PrizeData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:69` | `unknown` |
| `profileData_` | `ProfileData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:37` | `unknown` |
| `releaseEventData_` | `ReleaseEventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:81` | `unknown` |
| `roomData_` | `RoomData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:45` | `unknown` |
| `rouletteData_` | `RouletteData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:91` | `unknown` |
| `saleTaskData_` | `SaleTaskData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:89` | `unknown` |
| `scheduleData_` | `ScheduleData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:33` | `unknown` |
| `skillData_` | `SkillData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:85` | `unknown` |
| `staffData_` | `StaffData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:27` | `unknown` |
| `talkData_` | `TalkData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:15` | `unknown` |
| `todayEventData_` | `TodayEventData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:49` | `unknown` |
| `trophyData_` | `TrophyData[]` | `knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/DataManager.cs:31` | `unknown` |

## Promotion rule

This registry is the first canonical boundary candidate. It must be reconciled with the update corpus, ZIP data/guide, and APK provenance before any data is copied into `runtime/social-dev`.
