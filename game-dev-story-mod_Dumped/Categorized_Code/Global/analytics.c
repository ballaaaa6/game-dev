// Function: analytics_AnalyticsTracker__TrackPageView
// Address: 00ff9aac
// ==========================================================================================

void analytics_AnalyticsTracker__TrackPageView(uint param_1,undefined8 param_2)

{
  undefined *puVar1;
  
  puVar1 = PTR_StringLiteral_5729_01fc5560;
  if ((DAT_020ff8fc & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_5729_01fc5560);
    DAT_020ff8fc = 1;
  }
  analytics_AnalyticsTracker__TrackPageViewId(param_1 & 1,*(undefined8 *)puVar1,param_2);
  return;
}



// ==========================================================================================
// Function: analytics_AnalyticsTracker__TrackPageViewId
// Address: 00ff9b04
// ==========================================================================================

void analytics_AnalyticsTracker__TrackPageViewId(uint param_1,undefined8 param_2,long param_3)

{
  undefined *puVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  ulong uVar5;
  
  if ((DAT_020ff8fd & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_analytics_AnalyticsTracker_TypeInfo_01fc3598);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff8fd = 1;
  }
  puVar1 = PTR_StringLiteral_838_01fbf908;
  if (param_3 != 0) {
    uVar4 = *(undefined8 *)PTR_StringLiteral_1_01fbf388;
    if (0 < (int)*(ulong *)(param_3 + 0x18)) {
      uVar5 = 0;
      uVar3 = *(ulong *)(param_3 + 0x18) & 0xffffffff;
      do {
        if (uVar5 != 0) {
          uVar4 = System_String__Concat(uVar4,*(undefined8 *)puVar1,0);
          uVar3 = (ulong)*(uint *)(param_3 + 0x18);
        }
        if (uVar3 <= uVar5) goto LAB_00ff9c40;
        uVar4 = System_String__Concat(uVar4,*(undefined8 *)(param_3 + 0x20 + uVar5 * 8),0);
        uVar3 = (ulong)*(uint *)(param_3 + 0x18);
        uVar5 = uVar5 + 1;
      } while ((long)uVar5 < (long)(int)*(uint *)(param_3 + 0x18));
    }
    lVar2 = FUN_00db0c30(*(undefined8 *)PTR_string___TypeInfo_01fbf2f8,1);
    puVar1 = PTR_kairo_unity_analytics_AnalyticsTracker_TypeInfo_01fc3598;
    if (lVar2 != 0) {
      if (*(int *)(lVar2 + 0x18) != 0) {
        *(undefined8 *)(lVar2 + 0x20) = uVar4;
        if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        kairo_unity_analytics_AnalyticsTracker__TrackPageView(param_1 & 1,param_2,lVar2,0);
        return;
      }
LAB_00ff9c40:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: analytics_AnalyticsTracker__DispatchPageView
// Address: 00ff9c48
// ==========================================================================================

void analytics_AnalyticsTracker__DispatchPageView(void)

{
  return;
}



// ==========================================================================================
// Function: analytics_AnalyticsTracker___ctor
// Address: 00ff9c4c
// ==========================================================================================

void analytics_AnalyticsTracker___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
