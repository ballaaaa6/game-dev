// Function: data_LeaderboardData__GetHardLeaderbordData
// Address: 00fec8b0
// ==========================================================================================

undefined8 data_LeaderboardData__GetHardLeaderbordData(uint param_1)

{
  undefined *puVar1;
  long lVar2;
  int iVar3;
  
  if ((DAT_020ff8f4 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff8f4 = 1;
  }
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((param_1 & 0xfffffffe) == 0x16) {
    return 0;
  }
  iVar3 = 3;
  if (0x17 < (int)param_1) {
    iVar3 = 1;
  }
  if (*(int *)(*(long *)PTR_main_AppData_TypeInfo_01fbf278 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar2 = main_AppData__GetInstance(0);
  if ((lVar2 != 0) && (*(long *)(lVar2 + 0x98) != 0)) {
    param_1 = iVar3 + param_1;
    if (*(int *)(*(long *)(lVar2 + 0x98) + 0x18) <= (int)param_1) {
      return 0;
    }
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar2 = main_AppData__GetInstance(0);
    if ((lVar2 != 0) && (lVar2 = *(long *)(lVar2 + 0x98), lVar2 != 0)) {
      if (*(uint *)(lVar2 + 0x18) <= param_1) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      return *(undefined8 *)(lVar2 + (long)(int)param_1 * 8 + 0x20);
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_LeaderboardData__GetLeaderbordId
// Address: 00fec984
// ==========================================================================================

undefined4 data_LeaderboardData__GetLeaderbordId(undefined8 param_1)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  ulong uVar4;
  uint uVar5;
  long lVar6;
  
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff8f5 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff8f5 = 1;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = main_AppData__GetInstance(0);
  if ((lVar3 != 0) && (lVar3 = *(long *)(lVar3 + 0x98), lVar3 != 0)) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if (0 < (int)uVar1) {
      uVar5 = 0;
      do {
        if (uVar1 <= uVar5) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar6 = *(long *)(lVar3 + (long)(int)uVar5 * 8 + 0x20);
        if (lVar6 == 0) goto LAB_00feca44;
        uVar4 = System_String__op_Equality(*(undefined8 *)(lVar6 + 0x18),param_1,0);
        if ((uVar4 & 1) != 0) {
          return *(undefined4 *)(lVar6 + 0x10);
        }
        uVar1 = *(uint *)(lVar3 + 0x18);
        uVar5 = uVar5 + 1;
      } while ((int)uVar5 < (int)uVar1);
    }
    return 0xffffffff;
  }
LAB_00feca44:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_AchievementData___ctor
// Address: 00ff874c
// ==========================================================================================

void data_AchievementData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_BaseData___ctor
// Address: 00ff8754
// ==========================================================================================

void data_BaseData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_AchievementData___ctor
// Address: 00ff875c
// ==========================================================================================

void data_AchievementData___ctor(undefined8 param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  data_AchievementData__Load(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: data_AchievementData__Load
// Address: 00ff8788
// ==========================================================================================

void data_AchievementData__Load(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined4 uVar2;
  long lVar3;
  undefined8 uVar4;
  
  puVar1 = PTR_StringLiteral_38_01fbfae8;
  if ((DAT_020ff8ed & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    DAT_020ff8ed = 1;
  }
  lVar3 = kairo_unity_util_StringUtil__Split(param_2,*(undefined8 *)puVar1,0);
  if (lVar3 != 0) {
    if (*(int *)(lVar3 + 0x18) != 0) {
      uVar2 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar3 + 0x20),0);
      *(undefined4 *)(param_1 + 0x10) = uVar2;
      if (1 < *(uint *)(lVar3 + 0x18)) {
        if (*(long *)(lVar3 + 0x28) != 0) {
          uVar4 = System_String__Trim(*(long *)(lVar3 + 0x28),0);
          *(undefined8 *)(param_1 + 0x18) = uVar4;
          return;
        }
        goto LAB_00ff8824;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ff8824:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_AchievementData__GetAchievementIds
// Address: 00ff882c
// ==========================================================================================

void data_AchievementData__GetAchievementIds(void)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  undefined8 uVar7;
  ulong uVar8;
  long lVar9;
  long lVar10;
  uint uVar11;
  
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff8ee & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__Add_01fc0498);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468);
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_7722_01fc54d0);
    DAT_020ff8ee = 1;
  }
  puVar4 = PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470;
  puVar3 = PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar5 = main_AppData__GetInstance(0);
  lVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  Method_System_Collections_Generic_List_object___ctor(lVar6,*(undefined8 *)puVar4);
  puVar4 = PTR_StringLiteral_7722_01fc54d0;
  puVar3 = PTR_Method_System_Collections_Generic_List_string__Add_01fc0498;
  puVar2 = PTR_StringLiteral_38_01fbfae8;
  if ((lVar5 != 0) && (lVar5 = *(long *)(lVar5 + 0xa0), lVar5 != 0)) {
    uVar1 = *(uint *)(lVar5 + 0x18);
    if (0 < (int)uVar1) {
      uVar11 = 0;
      do {
        if (uVar1 <= uVar11) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar10 = *(long *)(lVar5 + (long)(int)uVar11 * 8 + 0x20);
        if (lVar10 == 0) goto LAB_00ff8a00;
        uVar7 = System_Int32__ToString(lVar10 + 0x10,0);
        uVar7 = System_String__Concat(uVar7,*(undefined8 *)puVar2,*(undefined8 *)(lVar10 + 0x18),0);
        uVar8 = System_String__op_Equality(*(undefined8 *)puVar4,*(undefined8 *)(lVar10 + 0x18),0);
        if ((uVar8 & 1) == 0) {
          if (lVar6 == 0) goto LAB_00ff8a00;
          lVar10 = *(long *)(lVar6 + 0x10);
          lVar9 = *(long *)puVar3;
          *(int *)(lVar6 + 0x1c) = *(int *)(lVar6 + 0x1c) + 1;
          if (lVar10 == 0) goto LAB_00ff8a00;
          uVar1 = *(uint *)(lVar6 + 0x18);
          if (uVar1 < *(uint *)(lVar10 + 0x18)) {
            *(uint *)(lVar6 + 0x18) = uVar1 + 1;
            *(undefined8 *)(lVar10 + (long)(int)uVar1 * 8 + 0x20) = uVar7;
          }
          else {
            System_Collections_Generic_List_object___AddWithResize
                      (lVar6,uVar7,*(undefined8 *)(*(long *)(*(long *)(lVar9 + 0x20) + 0xc0) + 0x70)
                      );
          }
        }
        uVar1 = *(uint *)(lVar5 + 0x18);
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < (int)uVar1);
    }
    if (lVar6 != 0) {
      Method_System_Collections_Generic_List_object__ToArray
                (lVar6,*(undefined8 *)
                        PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
      return;
    }
  }
LAB_00ff8a00:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_BonusData___ctor
// Address: 00ff8a08
// ==========================================================================================

void data_BonusData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_BonusData___ctor
// Address: 00ff8a10
// ==========================================================================================

void data_BonusData___ctor(undefined8 param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  data_BonusData__Load(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: data_BonusData__Load
// Address: 00ff8a3c
// ==========================================================================================

void data_BonusData__Load(long param_1,undefined8 param_2)

{
  uint uVar1;
  undefined *puVar2;
  byte bVar3;
  undefined4 uVar4;
  long lVar5;
  long lVar6;
  long lVar7;
  undefined8 uVar8;
  ulong uVar9;
  
  puVar2 = PTR_StringLiteral_38_01fbfae8;
  if ((DAT_020ff8ef & 1) == 0) {
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    FUN_00db0bbc(PTR_StringLiteral_10540_01fc54d8);
    DAT_020ff8ef = 1;
  }
  lVar5 = kairo_unity_util_StringUtil__Split(param_2,*(undefined8 *)puVar2,0);
  if (lVar5 != 0) {
    if (*(int *)(lVar5 + 0x18) != 0) {
      uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x20),0);
      *(undefined4 *)(param_1 + 0x10) = uVar4;
      if (1 < *(uint *)(lVar5 + 0x18)) {
        uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x28),0);
        *(undefined4 *)(param_1 + 0x14) = uVar4;
        if (2 < *(uint *)(lVar5 + 0x18)) {
          uVar8 = *(undefined8 *)(lVar5 + 0x30);
          uVar4 = data_BonusData__GetSkinImgId(uVar8);
          *(undefined4 *)(param_1 + 0x18) = uVar4;
          *(undefined8 *)(param_1 + 0x40) = uVar8;
          if (3 < *(uint *)(lVar5 + 0x18)) {
            uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x38),0);
            *(undefined4 *)(param_1 + 0x1c) = uVar4;
            if (4 < *(uint *)(lVar5 + 0x18)) {
              uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x40),0);
              *(undefined4 *)(param_1 + 0x20) = uVar4;
              uVar1 = *(uint *)(lVar5 + 0x18);
              if (((5 < uVar1) &&
                  (*(undefined8 *)(param_1 + 0x28) = *(undefined8 *)(lVar5 + 0x48), uVar1 != 6)) &&
                 (*(undefined8 *)(param_1 + 0x30) = *(undefined8 *)(lVar5 + 0x50), 7 < uVar1)) {
                lVar6 = kairo_unity_util_StringUtil__Split
                                  (*(undefined8 *)(lVar5 + 0x58),
                                   *(undefined8 *)PTR_StringLiteral_646_01fbf440,1,0);
                if (lVar6 == 0) goto LAB_00ff8c74;
                lVar7 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,
                                     *(undefined4 *)(lVar6 + 0x18));
                *(long *)(param_1 + 0x50) = lVar7;
                if ((int)*(ulong *)(lVar6 + 0x18) < 1) {
LAB_00ff8c10:
                  puVar2 = PTR_StringLiteral_10540_01fc54d8;
                  if (8 < *(uint *)(lVar5 + 0x18)) {
                    bVar3 = System_String__op_Equality
                                      (*(undefined8 *)(lVar5 + 0x60),
                                       *(undefined8 *)PTR_StringLiteral_10540_01fc54d8,0);
                    *(byte *)(param_1 + 0x39) = bVar3 & 1;
                    if (9 < *(uint *)(lVar5 + 0x18)) {
                      bVar3 = System_String__op_Equality
                                        (*(undefined8 *)(lVar5 + 0x68),*(undefined8 *)puVar2,0);
                      *(byte *)(param_1 + 0x38) = bVar3 & 1;
                      return;
                    }
                  }
                }
                else if ((*(ulong *)(lVar6 + 0x18) & 0xffffffff) != 0) {
                  uVar9 = 0;
                  do {
                    uVar4 = System_Int32__Parse(*(undefined8 *)(lVar6 + 0x20 + uVar9 * 8),0);
                    if (lVar7 == 0) goto LAB_00ff8c74;
                    if (*(uint *)(lVar7 + 0x18) <= uVar9) break;
                    *(undefined4 *)(lVar7 + uVar9 * 4 + 0x20) = uVar4;
                    uVar9 = uVar9 + 1;
                    if ((long)(int)*(uint *)(lVar6 + 0x18) <= (long)uVar9) goto LAB_00ff8c10;
                    lVar7 = *(long *)(param_1 + 0x50);
                  } while (uVar9 < *(uint *)(lVar6 + 0x18));
                }
              }
            }
          }
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ff8c74:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_BonusData__GetSkinImgId
// Address: 00ff8c78
// ==========================================================================================

void data_BonusData__GetSkinImgId(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  bool bVar4;
  long lVar5;
  undefined8 uVar6;
  ulong uVar7;
  bool bVar8;
  
  puVar2 = PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0;
  if ((DAT_020ff8f0 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0);
    FUN_00db0bbc(PTR_StringLiteral_6244_01fc4f90);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_927_01fbff50);
    DAT_020ff8f0 = 1;
  }
  puVar3 = PTR_StringLiteral_6244_01fc4f90;
  puVar1 = PTR_StringLiteral_1_01fbf388;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar2 = PTR_StringLiteral_927_01fbff50;
  lVar5 = System_Text_RegularExpressions_Regex__Replace
                    (param_1,*(undefined8 *)puVar3,*(undefined8 *)puVar1,0);
  bVar4 = true;
  do {
    bVar8 = bVar4;
    if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if (*(int *)(lVar5 + 0x10) < 2) break;
    uVar6 = Method_System_String_Substring(lVar5,0,1,0);
    uVar7 = System_String__op_Equality(uVar6,*(undefined8 *)puVar2,0);
    if ((uVar7 & 1) == 0) break;
    lVar5 = Method_System_String_Remove(lVar5,0,1,0);
    bVar4 = false;
  } while (bVar8);
  System_Int32__Parse(lVar5,0);
  return;
}



// ==========================================================================================
// Function: data_EventMessageData___ctor
// Address: 00ff8d84
// ==========================================================================================

void data_EventMessageData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_EventMessageData___ctor
// Address: 00ff8d8c
// ==========================================================================================

void data_EventMessageData___ctor(undefined8 param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  data_EventMessageData__Load(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: data_EventMessageData__Load
// Address: 00ff8db8
// ==========================================================================================

void data_EventMessageData__Load(long param_1,undefined8 param_2)

{
  int iVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  
  puVar2 = PTR_StringLiteral_38_01fbfae8;
  if ((DAT_020ff8f1 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    DAT_020ff8f1 = 1;
  }
  lVar4 = kairo_unity_util_StringUtil__Split(param_2,*(undefined8 *)puVar2,0);
  if (lVar4 != 0) {
    iVar1 = *(int *)(lVar4 + 0x18);
    if ((iVar1 != 0) &&
       (*(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(lVar4 + 0x20), iVar1 != 1)) {
      uVar3 = System_Int32__Parse(*(undefined8 *)(lVar4 + 0x28),0);
      *(undefined4 *)(param_1 + 0x20) = uVar3;
      if (2 < *(uint *)(lVar4 + 0x18)) {
        *(undefined8 *)(param_1 + 0x28) = *(undefined8 *)(lVar4 + 0x30);
        return;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_LeaderboardData___ctor
// Address: 00ff8e60
// ==========================================================================================

void data_LeaderboardData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_LeaderboardData___ctor
// Address: 00ff8e68
// ==========================================================================================

void data_LeaderboardData___ctor(undefined8 param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  data_LeaderboardData__Load(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: data_LeaderboardData__Load
// Address: 00ff8e94
// ==========================================================================================

void data_LeaderboardData__Load(long param_1,undefined8 param_2)

{
  uint uVar1;
  undefined *puVar2;
  byte bVar3;
  undefined4 uVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar2 = PTR_StringLiteral_38_01fbfae8;
  if ((DAT_020ff8f2 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_10540_01fc54d8);
    DAT_020ff8f2 = 1;
  }
  lVar5 = kairo_unity_util_StringUtil__Split(param_2,*(undefined8 *)puVar2,0);
  if (lVar5 != 0) {
    if (*(int *)(lVar5 + 0x18) != 0) {
      uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x20),0);
      *(undefined4 *)(param_1 + 0x10) = uVar4;
      uVar1 = *(uint *)(lVar5 + 0x18);
      if ((1 < uVar1) &&
         (*(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(lVar5 + 0x28), uVar1 != 2)) {
        uVar4 = System_Int32__Parse(*(undefined8 *)(lVar5 + 0x30),0);
        *(undefined4 *)(param_1 + 0x20) = uVar4;
        puVar2 = PTR_StringLiteral_1_01fbf388;
        if (3 < *(uint *)(lVar5 + 0x18)) {
          bVar3 = System_String__op_Equality
                            (*(undefined8 *)(lVar5 + 0x38),
                             *(undefined8 *)PTR_StringLiteral_10540_01fc54d8,0);
          *(byte *)(param_1 + 0x24) = bVar3 & 1;
          *(undefined4 *)(param_1 + 0x28) = 0xffffffff;
          uVar6 = *(undefined8 *)puVar2;
          *(undefined8 *)(param_1 + 0x38) = 0xffffffffffffffff;
          *(undefined8 *)(param_1 + 0x40) = 0xffffffffffffffff;
          *(undefined8 *)(param_1 + 0x30) = uVar6;
          return;
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_LeaderboardData__SetSaveData
// Address: 00ff8fa8
// ==========================================================================================

void data_LeaderboardData__SetSaveData
               (long param_1,undefined8 param_2,int param_3,uint param_4,uint param_5)

{
  int iVar1;
  undefined *puVar2;
  long lVar3;
  undefined4 uVar4;
  long lVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  
  if ((DAT_020ff8f3 & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    DAT_020ff8f3 = 1;
  }
  puVar2 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (param_4 == 0xffffffff) {
    uVar4 = 0xffffffff;
    uVar6 = 0xffffffff;
    iVar7 = -1;
    iVar8 = -1;
LAB_00ff90b8:
    if ((param_3 != -1) && (iVar1 = *(int *)(param_1 + 0x28), iVar1 != -1)) {
      if ((param_5 & 1) == 0) {
        if (param_3 < iVar1) {
          return;
        }
      }
      else if (iVar1 < param_3) {
        return;
      }
    }
    *(int *)(param_1 + 0x28) = param_3;
    *(undefined8 *)(param_1 + 0x30) = param_2;
    *(int *)(param_1 + 0x38) = iVar8;
    *(int *)(param_1 + 0x3c) = iVar7;
    *(undefined4 *)(param_1 + 0x40) = uVar6;
    *(undefined4 *)(param_1 + 0x44) = uVar4;
    return;
  }
  lVar3 = *(long *)PTR_form_GameForm_TypeInfo_01fbfab0;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar9 = *(long *)(lVar3 + 0xb8);
  lVar3 = *(long *)(lVar9 + 0xb78);
  if (lVar3 != 0) {
    if (param_4 < *(uint *)(lVar3 + 0x18)) {
      lVar5 = (long)(int)param_4;
      iVar1 = *(int *)(lVar3 + lVar5 * 4 + 0x20);
      lVar3 = *(long *)(lVar9 + 0xb58);
      iVar7 = iVar1 + 3;
      if (-1 < iVar1) {
        iVar7 = iVar1;
      }
      if (lVar3 == 0) goto LAB_00ff9104;
      if (param_4 < *(uint *)(lVar3 + 0x18)) {
        lVar9 = *(long *)(lVar9 + 0xb60);
        if (lVar9 == 0) goto LAB_00ff9104;
        if (param_4 < *(uint *)(lVar9 + 0x18)) {
          uVar6 = *(undefined4 *)(lVar3 + lVar5 * 4 + 0x20);
          uVar4 = *(undefined4 *)(lVar9 + lVar5 * 4 + 0x20);
          iVar8 = iVar1 / 0x30 + 1;
          iVar7 = (iVar1 / 0x30) * -0xc + (iVar7 >> 2) + 1;
          goto LAB_00ff90b8;
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ff9104:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_LeaderboardData__SetSaveData
// Address: 00ff910c
// ==========================================================================================

void data_LeaderboardData__SetSaveData
               (long param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  *(undefined4 *)(param_1 + 0x28) = param_3;
  *(undefined8 *)(param_1 + 0x30) = param_2;
  *(undefined4 *)(param_1 + 0x38) = param_4;
  *(undefined4 *)(param_1 + 0x3c) = param_5;
  *(undefined4 *)(param_1 + 0x40) = param_6;
  *(undefined4 *)(param_1 + 0x44) = param_7;
  return;
}



// ==========================================================================================
// Function: data_LeaderboardData__GetLeaderbordId
// Address: 00ff9120
// ==========================================================================================

void data_LeaderboardData__GetLeaderbordId(ulong param_1)

{
  undefined8 *puVar1;
  uint uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  ulong uVar12;
  uint uVar13;
  undefined8 uVar14;
  long lVar15;
  undefined8 local_98;
  undefined8 uStack_90;
  long local_88;
  undefined8 local_80;
  undefined8 uStack_78;
  long local_70;
  
  puVar3 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff8f6 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_System_Comparison_LeaderboardData__TypeInfo_01fc54e0);
    FUN_00db0bbc(
                PTR_Method_System_Collections_Generic_List_Enumerator_LeaderboardData__Dispose_01fc54e8
                );
    FUN_00db0bbc(
                PTR_Method_System_Collections_Generic_List_Enumerator_LeaderboardData__MoveNext_01fc54f0
                );
    FUN_00db0bbc(
                PTR_Method_System_Collections_Generic_List_Enumerator_LeaderboardData__get_Current_01fc54f8
                );
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__Add_01fc0498);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_LeaderboardData__GetEnumerator_01fc5500)
    ;
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_LeaderboardData__Sort_01fc5508);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_LeaderboardData___ctor_01fc5510);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_LeaderboardData__TypeInfo_01fc5518);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_Method_data_LeaderboardData___c__GetLeaderbordId_b__16_0_01fc5520);
    FUN_00db0bbc(PTR_data_LeaderboardData___c_TypeInfo_01fc5528);
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_953_01fc02e0);
    FUN_00db0bbc(PTR_StringLiteral_927_01fbff50);
    DAT_020ff8f6 = 1;
  }
  puVar5 = PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470;
  puVar4 = PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468;
  local_80 = 0;
  uStack_78 = 0;
  local_70 = 0;
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar9 = main_AppData__GetInstance(0);
  lVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  Method_System_Collections_Generic_List_object___ctor(lVar10,*(undefined8 *)puVar5);
  puVar7 = PTR_Method_System_Collections_Generic_List_string__Add_01fc0498;
  puVar6 = PTR_StringLiteral_953_01fc02e0;
  puVar5 = PTR_StringLiteral_927_01fbff50;
  puVar4 = PTR_StringLiteral_38_01fbfae8;
  puVar3 = PTR_string___TypeInfo_01fbf2f8;
  if ((param_1 & 1) == 0) {
    if ((lVar9 == 0) || (lVar9 = *(long *)(lVar9 + 0x98), lVar9 == 0)) goto LAB_00ff96c0;
    uVar2 = *(uint *)(lVar9 + 0x18);
    if (0 < (int)uVar2) {
      uVar13 = 0;
      do {
        if (uVar2 <= uVar13) {
LAB_00ff96bc:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar15 = *(long *)(lVar9 + (long)(int)uVar13 * 8 + 0x20);
        lVar11 = FUN_00db0c30(*(undefined8 *)puVar3,5);
        if ((lVar15 == 0) || (uVar14 = System_Int32__ToString(lVar15 + 0x10,0), lVar11 == 0))
        goto LAB_00ff96c0;
        uVar2 = *(uint *)(lVar11 + 0x18);
        if (((uVar2 == 0) ||
            (((*(undefined8 *)(lVar11 + 0x20) = uVar14, uVar2 == 1 ||
              (*(undefined8 *)(lVar11 + 0x28) = *(undefined8 *)puVar4, uVar2 < 3)) ||
             (*(undefined8 *)(lVar11 + 0x30) = *(undefined8 *)(lVar15 + 0x18), uVar2 == 3)))) ||
           (*(undefined8 *)(lVar11 + 0x38) = *(undefined8 *)puVar4, uVar2 < 5)) goto LAB_00ff96bc;
        puVar1 = (undefined8 *)puVar5;
        if (*(char *)(lVar15 + 0x24) != '\0') {
          puVar1 = (undefined8 *)puVar6;
        }
        *(undefined8 *)(lVar11 + 0x40) = *puVar1;
        uVar14 = Method_System_String_Concat(lVar11,0);
        if (lVar10 == 0) goto LAB_00ff96c0;
        lVar11 = *(long *)(lVar10 + 0x10);
        lVar15 = *(long *)puVar7;
        *(int *)(lVar10 + 0x1c) = *(int *)(lVar10 + 0x1c) + 1;
        if (lVar11 == 0) goto LAB_00ff96c0;
        uVar2 = *(uint *)(lVar10 + 0x18);
        if (uVar2 < *(uint *)(lVar11 + 0x18)) {
          *(uint *)(lVar10 + 0x18) = uVar2 + 1;
          *(undefined8 *)(lVar11 + (long)(int)uVar2 * 8 + 0x20) = uVar14;
        }
        else {
          System_Collections_Generic_List_object___AddWithResize
                    (lVar10,uVar14,
                     *(undefined8 *)(*(long *)(*(long *)(lVar15 + 0x20) + 0xc0) + 0x70));
        }
        uVar2 = *(uint *)(lVar9 + 0x18);
        uVar13 = uVar13 + 1;
      } while ((int)uVar13 < (int)uVar2);
    }
  }
  else {
    if (lVar9 == 0) goto LAB_00ff96c0;
    uVar14 = *(undefined8 *)(lVar9 + 0x98);
    lVar9 = thunk_FUN_00e11c14(*(undefined8 *)
                                PTR_System_Collections_Generic_List_LeaderboardData__TypeInfo_01fc5518
                              );
    System_Collections_Generic_List_object____ctor
              (lVar9,uVar14,
               *(undefined8 *)
                PTR_Method_System_Collections_Generic_List_LeaderboardData___ctor_01fc5510);
    puVar3 = PTR_data_LeaderboardData___c_TypeInfo_01fc5528;
    lVar11 = *(long *)PTR_data_LeaderboardData___c_TypeInfo_01fc5528;
    if (*(int *)(lVar11 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar11 = *(long *)puVar3;
    }
    lVar15 = *(long *)(*(long *)(lVar11 + 0xb8) + 8);
    if (lVar15 == 0) {
      if (*(int *)(lVar11 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar11 = *(long *)puVar3;
      }
      uVar14 = **(undefined8 **)(lVar11 + 0xb8);
      lVar15 = thunk_FUN_00e11c14(*(undefined8 *)
                                   PTR_System_Comparison_LeaderboardData__TypeInfo_01fc54e0);
      System_Comparison_object____ctor
                (lVar15,uVar14,
                 *(undefined8 *)
                  PTR_Method_data_LeaderboardData___c__GetLeaderbordId_b__16_0_01fc5520,0);
      *(long *)(*(long *)(*(long *)puVar3 + 0xb8) + 8) = lVar15;
    }
    if (lVar9 == 0) goto LAB_00ff96c0;
    System_Collections_Generic_List_object___Sort
              (lVar9,lVar15,
               *(undefined8 *)
                PTR_Method_System_Collections_Generic_List_LeaderboardData__Sort_01fc5508);
    Method_System_Collections_Generic_List_object__GetEnumerator
              (&local_98,lVar9,
               *(undefined8 *)
                PTR_Method_System_Collections_Generic_List_LeaderboardData__GetEnumerator_01fc5500);
    puVar8 = 
    PTR_Method_System_Collections_Generic_List_Enumerator_LeaderboardData__MoveNext_01fc54f0;
    puVar7 = PTR_Method_System_Collections_Generic_List_string__Add_01fc0498;
    puVar6 = PTR_StringLiteral_953_01fc02e0;
    puVar5 = PTR_StringLiteral_927_01fbff50;
    puVar4 = PTR_StringLiteral_38_01fbfae8;
    puVar3 = PTR_string___TypeInfo_01fbf2f8;
    uStack_78 = uStack_90;
    local_80 = local_98;
    local_70 = local_88;
                    /* try { // try from 00ff93b0 to 00ff93b7 has its CatchHandler @ 00ff9504 */
    while (uVar12 = Method_System_Collections_Generic_List_Enumerator_object__MoveNext
                              (&local_80,*(undefined8 *)puVar8), lVar9 = local_70, (uVar12 & 1) != 0
          ) {
                    /* try { // try from 00ff93c4 to 00ff93cb has its CatchHandler @ 00ff94fc */
      lVar11 = FUN_00db0c30(*(undefined8 *)puVar3,5);
      if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94c8 to 00ff94cb has its CatchHandler @ 00ff94ec */
        FUN_00db0de4();
      }
                    /* try { // try from 00ff93d8 to 00ff93df has its CatchHandler @ 00ff9500 */
      uVar14 = System_Int32__ToString(lVar9 + 0x10,0);
      if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94cc to 00ff94cf has its CatchHandler @ 00ff950c */
        FUN_00db0de4();
      }
      uVar2 = *(uint *)(lVar11 + 0x18);
      if (uVar2 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94c0 to 00ff94c3 has its CatchHandler @ 00ff950c */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar11 + 0x20) = uVar14;
      if (uVar2 == 1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94c4 to 00ff94c7 has its CatchHandler @ 00ff94f0 */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar11 + 0x28) = *(undefined8 *)puVar4;
      if (uVar2 < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94d8 to 00ff94db has its CatchHandler @ 00ff94e8 */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar11 + 0x30) = *(undefined8 *)(lVar9 + 0x18);
      if (uVar2 == 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94bc to 00ff94bf has its CatchHandler @ 00ff94f8 */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar11 + 0x38) = *(undefined8 *)puVar4;
      if (uVar2 < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94dc to 00ff94df has its CatchHandler @ 00ff94e4 */
        FUN_00db0dec();
      }
      puVar1 = (undefined8 *)puVar5;
      if (*(char *)(lVar9 + 0x24) != '\0') {
        puVar1 = (undefined8 *)puVar6;
      }
      *(undefined8 *)(lVar11 + 0x40) = *puVar1;
                    /* try { // try from 00ff943c to 00ff944b has its CatchHandler @ 00ff94f4 */
      uVar14 = Method_System_String_Concat(lVar11,0);
      if (lVar10 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ff94d0 to 00ff94d7 has its CatchHandler @ 00ff9508 */
        FUN_00db0de4();
      }
      lVar9 = *(long *)(lVar10 + 0x10);
      lVar11 = *(long *)puVar7;
      *(int *)(lVar10 + 0x1c) = *(int *)(lVar10 + 0x1c) + 1;
      if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      uVar2 = *(uint *)(lVar10 + 0x18);
      if (uVar2 < *(uint *)(lVar9 + 0x18)) {
        *(uint *)(lVar10 + 0x18) = uVar2 + 1;
        *(undefined8 *)(lVar9 + (long)(int)uVar2 * 8 + 0x20) = uVar14;
      }
      else {
                    /* try { // try from 00ff9498 to 00ff949f has its CatchHandler @ 00ff94e0 */
        System_Collections_Generic_List_object___AddWithResize
                  (lVar10,uVar14,*(undefined8 *)(*(long *)(*(long *)(lVar11 + 0x20) + 0xc0) + 0x70))
        ;
      }
    }
    Method_System_Collections_Generic_List_Enumerator_object__Dispose
              (&local_80,
               *(undefined8 *)
                PTR_Method_System_Collections_Generic_List_Enumerator_LeaderboardData__Dispose_01fc54e8
              );
  }
  if (lVar10 != 0) {
    Method_System_Collections_Generic_List_object__ToArray
              (lVar10,*(undefined8 *)
                       PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    return;
  }
LAB_00ff96c0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: data_LeaderboardData___c___cctor
// Address: 00ff9704
// ==========================================================================================

void data_LeaderboardData___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_data_LeaderboardData___c_TypeInfo_01fc5528;
  if ((DAT_020ff8f7 & 1) == 0) {
    FUN_00db0bbc(PTR_data_LeaderboardData___c_TypeInfo_01fc5528);
    DAT_020ff8f7 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: data_LeaderboardData___c___ctor
// Address: 00ff9760
// ==========================================================================================

void data_LeaderboardData___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_MissionData___ctor
// Address: 00ff978c
// ==========================================================================================

void data_MissionData___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: data_MissionData___ctor
// Address: 00ff9794
// ==========================================================================================

void data_MissionData___ctor(undefined8 param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  data_MissionData__Load(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: data_MissionData__Load
// Address: 00ff97c0
// ==========================================================================================

void data_MissionData__Load(long param_1,undefined8 param_2)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  
  puVar2 = PTR_StringLiteral_38_01fbfae8;
  if ((DAT_020ff8f8 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    DAT_020ff8f8 = 1;
  }
  lVar4 = kairo_unity_util_StringUtil__Split(param_2,*(undefined8 *)puVar2,0);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) != 0) {
      uVar3 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar4 + 0x20),0);
      *(undefined4 *)(param_1 + 0x10) = uVar3;
      uVar1 = *(uint *)(lVar4 + 0x18);
      if (((1 < uVar1) &&
          (*(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(lVar4 + 0x28), uVar1 != 2)) &&
         (*(undefined8 *)(param_1 + 0x20) = *(undefined8 *)(lVar4 + 0x30), 3 < uVar1)) {
        uVar3 = System_Int32__Parse(*(undefined8 *)(lVar4 + 0x38),0);
        *(undefined4 *)(param_1 + 0x28) = uVar3;
        return;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
