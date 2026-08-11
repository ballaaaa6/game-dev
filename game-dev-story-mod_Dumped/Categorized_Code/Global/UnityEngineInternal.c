// Function: UnityEngineInternal_MathfInternal___cctor
// Address: 01c90074
// ==========================================================================================

void UnityEngineInternal_MathfInternal___cctor(void)

{
  undefined *puVar1;
  float fVar2;
  
  puVar1 = PTR_UnityEngineInternal_MathfInternal_TypeInfo_01fe74c8;
  if ((DAT_021039ac & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_MathfInternal_TypeInfo_01fe74c8);
    DAT_021039ac = 1;
  }
  thunk_FUN_00dd38ec();
  **(undefined4 **)(*(long *)puVar1 + 0xb8) = 0x800000;
  thunk_FUN_00dd38ec();
  *(undefined4 *)(*(long *)(*(long *)puVar1 + 0xb8) + 4) = 1;
  thunk_FUN_00dd38ec();
  fVar2 = (float)System_Threading_Interlocked__CompareExchange
                           (1,0,*(long *)(*(long *)puVar1 + 0xb8) + 4,0);
  *(bool *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = fVar2 == 0.0;
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_TypeInferenceRuleAttribute___ctor
// Address: 01c9010c
// ==========================================================================================

void UnityEngineInternal_TypeInferenceRuleAttribute___ctor(long param_1,undefined4 param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined4 local_38;
  
  puVar1 = PTR_UnityEngineInternal_TypeInferenceRules_TypeInfo_01fe74d0;
  if ((DAT_021039ad & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_TypeInferenceRules_TypeInfo_01fe74d0);
    DAT_021039ad = 1;
  }
  local_48 = *(undefined8 *)puVar1;
  uStack_40 = 0xffffffffffffffff;
  local_38 = param_2;
  uVar2 = System_Enum__ToString(&local_48,0);
  System_Attribute___ctor(param_1,0);
  *(undefined8 *)(param_1 + 0x10) = uVar2;
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_TypeInferenceRuleAttribute___ctor
// Address: 01c90190
// ==========================================================================================

void UnityEngineInternal_TypeInferenceRuleAttribute___ctor(long param_1,undefined8 param_2)

{
  System_Attribute___ctor(param_1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_TypeInferenceRuleAttribute__ToString
// Address: 01c901b8
// ==========================================================================================

undefined8 UnityEngineInternal_TypeInferenceRuleAttribute__ToString(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: UnityEngineInternal_GenericStack___ctor
// Address: 01c901c0
// ==========================================================================================

void UnityEngineInternal_GenericStack___ctor(undefined8 param_1)

{
  System_Collections_Stack___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeUpdateCallback___ctor
// Address: 01cf5a64
// ==========================================================================================

void UnityEngineInternal_Input_NativeUpdateCallback___ctor(long param_1,long param_2,long param_3)

{
  char cVar1;
  ulong uVar2;
  undefined8 uVar3;
  
  uVar3 = *(undefined8 *)(param_3 + 8);
  *(long *)(param_1 + 0x20) = param_2;
  *(long *)(param_1 + 0x28) = param_3;
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  cVar1 = *(char *)(param_3 + 0x52);
  *(long *)(param_1 + 0x40) = param_1;
  uVar2 = FUN_00db0c48(param_3);
  if ((uVar2 & 1) == 0) {
    if (param_2 == 0) {
      uVar3 = thunk_FUN_00e29584(0,"Delegate to an instance method cannot have null \'this\'.");
                    /* WARNING: Subroutine does not return */
      FUN_00db0cb0(uVar3,0);
    }
  }
  else if (cVar1 == '\x02') {
    *(code **)(param_1 + 0x18) = FUN_00d91e80;
    goto LAB_01cf5ac0;
  }
  *(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(param_1 + 0x10);
  *(undefined8 *)(param_1 + 0x40) = *(undefined8 *)(param_1 + 0x20);
LAB_01cf5ac0:
  *(code **)(param_1 + 0x38) = FUN_00d91e28;
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeUpdateCallback__Invoke
// Address: 01cf5af0
// ==========================================================================================

void UnityEngineInternal_Input_NativeUpdateCallback__Invoke
               (long param_1,undefined8 param_2,undefined8 param_3)

{
                    /* WARNING: Could not recover jumptable at 0x01cf5b00. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(param_1 + 0x18))
            (*(undefined8 *)(param_1 + 0x40),param_2,param_3,*(undefined8 *)(param_1 + 0x28));
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__get_onDeviceDiscovered
// Address: 01cf5b04
// ==========================================================================================

undefined8 UnityEngineInternal_Input_NativeInputSystem__get_onDeviceDiscovered(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_02105728 & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_02105728 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return *(undefined8 *)(*(long *)(lVar2 + 0xb8) + 0x18);
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__set_onDeviceDiscovered
// Address: 01cf5b5c
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__set_onDeviceDiscovered(long param_1)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_02105729 & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_02105729 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  *(long *)(*(long *)(lVar2 + 0xb8) + 0x18) = param_1;
  if (DAT_02105730 == (code *)0x0) {
    DAT_02105730 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::set_hasDeviceDiscoveredCallback(System.Boolean)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5bdc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105730)(param_1 != 0);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__set_hasDeviceDiscoveredCallback
// Address: 01cf5be0
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__set_hasDeviceDiscoveredCallback(uint param_1)

{
  if (DAT_02105730 == (code *)0x0) {
    DAT_02105730 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::set_hasDeviceDiscoveredCallback(System.Boolean)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5c18. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105730)(param_1 & 1);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem___cctor
// Address: 01cf5c1c
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem___cctor(void)

{
  if (DAT_02105730 == (code *)0x0) {
    DAT_02105730 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::set_hasDeviceDiscoveredCallback(System.Boolean)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5c48. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105730)(0);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__NotifyBeforeUpdate
// Address: 01cf5c4c
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__NotifyBeforeUpdate(undefined4 param_1)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_0210572a & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_0210572a = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
  if (lVar2 != 0) {
                    /* WARNING: Could not recover jumptable at 0x01cf5cb8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(lVar2 + 0x18))(*(undefined8 *)(lVar2 + 0x40),param_1,*(undefined8 *)(lVar2 + 0x28))
    ;
    return;
  }
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__NotifyUpdate
// Address: 01cf5cc8
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__NotifyUpdate(undefined4 param_1,long param_2)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_0210572b & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_0210572b = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = **(long **)(lVar2 + 0xb8);
  if (lVar2 != 0) {
                    /* WARNING: Could not recover jumptable at 0x01cf5d44. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(lVar2 + 0x18))
              (*(undefined8 *)(lVar2 + 0x40),param_1,param_2,*(undefined8 *)(lVar2 + 0x28));
    return;
  }
  if (param_2 != 0) {
    *(undefined8 *)(param_2 + 8) = 0;
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__NotifyDeviceDiscovered
// Address: 01cf5d64
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__NotifyDeviceDiscovered
               (undefined4 param_1,undefined8 param_2)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_0210572c & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_0210572c = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x18);
  if (lVar2 != 0) {
                    /* WARNING: Could not recover jumptable at 0x01cf5de0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(lVar2 + 0x18))
              (*(undefined8 *)(lVar2 + 0x40),param_1,param_2,*(undefined8 *)(lVar2 + 0x28));
    return;
  }
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__ShouldRunUpdate
// Address: 01cf5df4
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__ShouldRunUpdate(undefined4 param_1,byte *param_2)

{
  undefined *puVar1;
  byte bVar2;
  long lVar3;
  
  puVar1 = PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540;
  if ((DAT_0210572d & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngineInternal_Input_NativeInputSystem_TypeInfo_01fe6540);
    DAT_0210572d = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  lVar3 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x10);
  if (lVar3 == 0) {
    bVar2 = 1;
  }
  else {
    bVar2 = (**(code **)(lVar3 + 0x18))
                      (*(undefined8 *)(lVar3 + 0x40),param_1,*(undefined8 *)(lVar3 + 0x28));
    bVar2 = bVar2 & 1;
  }
  *param_2 = bVar2;
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__get_currentTime
// Address: 01cf5e84
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__get_currentTime(void)

{
  if (DAT_02105738 == (code *)0x0) {
    DAT_02105738 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::get_currentTime()"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5ea8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105738)();
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__get_currentTimeOffsetToRealtimeSinceStartup
// Address: 01cf5eac
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__get_currentTimeOffsetToRealtimeSinceStartup(void)

{
  if (DAT_02105740 == (code *)0x0) {
    DAT_02105740 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::get_currentTimeOffsetToRealtimeSinceStartup()"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5ed0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105740)();
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__AllocateDeviceId
// Address: 01cf5ed4
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__AllocateDeviceId(void)

{
  if (DAT_02105748 == (code *)0x0) {
    DAT_02105748 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::AllocateDeviceId()"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5ef8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105748)();
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__QueueInputEvent
// Address: 01cf5efc
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__QueueInputEvent(undefined8 param_1)

{
  if (DAT_02105750 == (code *)0x0) {
    DAT_02105750 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::QueueInputEvent(System.IntPtr)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5f34. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105750)(param_1);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__IOCTL
// Address: 01cf5f38
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__IOCTL
               (undefined4 param_1,undefined4 param_2,undefined8 param_3,undefined4 param_4)

{
  if (DAT_02105758 == (code *)0x0) {
    DAT_02105758 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::IOCTL(System.Int32,System.Int32,System.IntPtr,System.Int32)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5f90. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105758)(param_1,param_2,param_3,param_4);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__SetPollingFrequency
// Address: 01cf5f94
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__SetPollingFrequency(undefined8 param_1)

{
  if (DAT_02105760 == (code *)0x0) {
    DAT_02105760 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::SetPollingFrequency(System.Single)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf5fc8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105760)(param_1);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_Input_NativeInputSystem__Update
// Address: 01cf5fcc
// ==========================================================================================

void UnityEngineInternal_Input_NativeInputSystem__Update(undefined4 param_1)

{
  if (DAT_02105768 == (code *)0x0) {
    DAT_02105768 = (code *)FUN_00db0b80(
                                       "UnityEngineInternal.Input.NativeInputSystem::Update(UnityEngineInternal.Input.NativeInputUpdateType)"
                                       );
  }
                    /* WARNING: Could not recover jumptable at 0x01cf6004. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02105768)(param_1);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_WebRequestUtils__RedirectTo
// Address: 01ebe1f8
// ==========================================================================================

void UnityEngineInternal_WebRequestUtils__RedirectTo(undefined8 param_1,long param_2)

{
  undefined *puVar1;
  short sVar2;
  long lVar3;
  ulong uVar4;
  undefined8 uVar5;
  long lVar6;
  
  if ((DAT_0210704c & 1) == 0) {
    FUN_00db0bbc(PTR_System_Uri_TypeInfo_01fd0b48);
    DAT_0210704c = 1;
  }
  puVar1 = PTR_System_Uri_TypeInfo_01fd0b48;
  if (param_2 != 0) {
    sVar2 = System_String__get_Chars(param_2,0,0);
    lVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
    Method_System_Uri__ctor(lVar3,param_2,(ulong)(sVar2 == 0x2f) << 1,0);
    if (lVar3 != 0) {
      uVar4 = System_Uri__get_IsAbsoluteUri(lVar3,0);
      lVar6 = lVar3;
      if ((uVar4 & 1) == 0) {
        uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
        Method_System_Uri__ctor(uVar5,param_1,1,0);
        lVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
        Method_System_Uri__ctor(lVar6,uVar5,lVar3,0);
        if (lVar6 == 0) goto LAB_01ebe2e0;
      }
      Method_System_Uri_get_AbsoluteUri(lVar6,0);
      return;
    }
  }
LAB_01ebe2e0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: UnityEngineInternal_WebRequestUtils__MakeUriString
// Address: 01ebe654
// ==========================================================================================

void UnityEngineInternal_WebRequestUtils__MakeUriString(long param_1,long param_2,ulong param_3)

{
  undefined4 uVar1;
  short sVar2;
  ulong uVar3;
  long lVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  
  if ((DAT_0210704e & 1) == 0) {
    FUN_00db0bbc(PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    FUN_00db0bbc(PTR_UnityEngineInternal_WebRequestUtils_TypeInfo_01ff5178);
    FUN_00db0bbc(PTR_StringLiteral_7527_01fde030);
    FUN_00db0bbc(PTR_StringLiteral_7526_01ff5188);
    FUN_00db0bbc(PTR_StringLiteral_350_01fc0e50);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    FUN_00db0bbc(PTR_StringLiteral_7525_01fde040);
    FUN_00db0bbc(PTR_StringLiteral_8067_01ff5190);
    DAT_0210704e = 1;
  }
  if (param_1 == 0) goto LAB_01ebea34;
  uVar3 = Method_System_Uri_get_IsFile(param_1,0);
  if ((uVar3 & 1) == 0) {
    lVar4 = Method_System_Uri_get_Scheme(param_1,0);
    if ((param_3 & 1) == 0) {
      if ((param_2 == 0) || (lVar4 == 0)) {
LAB_01ebea34:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      if ((*(int *)(lVar4 + 0x10) + 2 <= *(int *)(param_2 + 0x10)) &&
         (sVar2 = System_String__get_Chars(param_2,*(int *)(lVar4 + 0x10) + 1,0), sVar2 != 0x2f)) {
        uVar1 = *(undefined4 *)(param_2 + 0x10);
        plVar6 = (long *)thunk_FUN_00e11c14(*(undefined8 *)
                                             PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
        System_Text_StringBuilder___ctor(plVar6,lVar4,uVar1,0);
        if (plVar6 != (long *)0x0) {
          System_Text_StringBuilder__Append(plVar6,0x3a,0);
          uVar3 = System_String__op_Equality(lVar4,*(undefined8 *)PTR_StringLiteral_8067_01ff5190,0)
          ;
          if ((uVar3 & 1) == 0) {
            uVar7 = Method_System_Uri_get_PathAndQuery(param_1,0);
            System_Text_StringBuilder__Append(plVar6,uVar7,0);
            lVar4 = Method_System_Uri_get_Fragment(param_1,0);
          }
          else {
            lVar4 = Method_System_Uri_get_AbsolutePath(param_1,0);
            if (lVar4 == 0) goto LAB_01ebea34;
            uVar3 = System_String__Contains(lVar4,*(undefined8 *)PTR_StringLiteral_350_01fc0e50,0);
            if ((uVar3 & 1) != 0) {
              if (*(int *)(*(long *)PTR_UnityEngineInternal_WebRequestUtils_TypeInfo_01ff5178 + 0xe0
                          ) == 0) {
                thunk_FUN_00df405c();
              }
              lVar4 = UnityEngineInternal_WebRequestUtils__URLDecode(lVar4);
              if (lVar4 == 0) goto LAB_01ebea34;
            }
            uVar3 = Method_System_String_StartsWith
                              (lVar4,*(undefined8 *)PTR_StringLiteral_7526_01ff5188,0);
            if ((((uVar3 & 1) != 0) && (6 < *(int *)(lVar4 + 0x10))) &&
               (sVar2 = System_String__get_Chars(lVar4,6,0), sVar2 != 0x2f)) {
              System_Text_StringBuilder__Append
                        (plVar6,*(undefined8 *)PTR_StringLiteral_7527_01fde030,0);
              lVar4 = System_String__Substring(lVar4,5,0);
            }
          }
          System_Text_StringBuilder__Append(plVar6,lVar4,0);
                    /* WARNING: Could not recover jumptable at 0x01ebea04. Too many branches */
                    /* WARNING: Treating indirect jump as call */
          (**(code **)(*plVar6 + 0x168))(plVar6,*(undefined8 *)(*plVar6 + 0x170));
          return;
        }
        goto LAB_01ebea34;
      }
    }
    else if (param_2 == 0) goto LAB_01ebea34;
    uVar3 = System_String__Contains(param_2,*(undefined8 *)PTR_StringLiteral_350_01fc0e50,0);
    if ((uVar3 & 1) == 0) {
      Method_System_Uri_get_AbsoluteUri(param_1,0);
      return;
    }
  }
  else {
    uVar3 = Method_System_Uri_get_IsLoopback(param_1,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = Method_System_Uri_get_AbsolutePath(param_1,0);
      lVar5 = System_Uri__get_OriginalString(param_1,0);
      if (lVar4 == 0) goto LAB_01ebea34;
      uVar3 = System_String__Contains(lVar4,*(undefined8 *)PTR_StringLiteral_350_01fc0e50,0);
      if ((uVar3 & 1) != 0) {
        uVar3 = System_String__Contains(lVar4,0x2b,0);
        if ((uVar3 & 1) != 0) {
          if (lVar5 == 0) goto LAB_01ebea34;
          uVar3 = Method_System_String_StartsWith
                            (lVar5,*(undefined8 *)PTR_StringLiteral_7525_01fde040,0);
          if ((uVar3 & 1) == 0) goto LAB_01ebe7f0;
        }
        if (*(int *)(*(long *)PTR_UnityEngineInternal_WebRequestUtils_TypeInfo_01ff5178 + 0xe0) == 0
           ) {
          thunk_FUN_00df405c();
        }
        lVar4 = UnityEngineInternal_WebRequestUtils__URLDecode(lVar4);
        if (lVar4 == 0) goto LAB_01ebea34;
      }
      lVar5 = lVar4;
      if ((0 < *(int *)(lVar5 + 0x10)) &&
         (sVar2 = System_String__get_Chars(lVar5,0,0), sVar2 != 0x2f)) {
        lVar5 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_838_01fbf908,lVar5,0);
      }
LAB_01ebe7f0:
      System_String__Concat(*(undefined8 *)PTR_StringLiteral_7527_01fde030,lVar5,0);
      return;
    }
  }
  System_Uri__get_OriginalString(param_1,0);
  return;
}



// ==========================================================================================
// Function: UnityEngineInternal_WebRequestUtils__URLDecode
// Address: 01ebea38
// ==========================================================================================

void UnityEngineInternal_WebRequestUtils__URLDecode(undefined8 param_1)

{
  undefined *puVar1;
  long *plVar2;
  undefined8 uVar3;
  
  if ((DAT_0210704f & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngine_WWWTranscoder_TypeInfo_01ff5198);
    DAT_0210704f = 1;
  }
  plVar2 = (long *)System_Text_Encoding__get_UTF8(0);
  puVar1 = PTR_UnityEngine_WWWTranscoder_TypeInfo_01ff5198;
  if (plVar2 != (long *)0x0) {
    uVar3 = (**(code **)(*plVar2 + 600))(plVar2,param_1,*(undefined8 *)(*plVar2 + 0x260));
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    uVar3 = UnityEngine_WWWTranscoder__URLDecode(uVar3);
    plVar2 = (long *)System_Text_Encoding__get_UTF8(0);
    if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x01ebead4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*plVar2 + 0x368))(plVar2,uVar3,*(undefined8 *)(*plVar2 + 0x370));
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: UnityEngineInternal_WebRequestUtils___cctor
// Address: 01ebeb40
// ==========================================================================================

void UnityEngineInternal_WebRequestUtils___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  
  puVar3 = PTR_StringLiteral_6354_01ff51a0;
  puVar2 = PTR_UnityEngineInternal_WebRequestUtils_TypeInfo_01ff5178;
  puVar1 = PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0;
  if ((DAT_02107050 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0);
    FUN_00db0bbc(PTR_UnityEngineInternal_WebRequestUtils_TypeInfo_01ff5178);
    FUN_00db0bbc(PTR_StringLiteral_6354_01ff51a0);
    DAT_02107050 = 1;
  }
  uVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Text_RegularExpressions_Regex___ctor(uVar4,*(undefined8 *)puVar3,0);
  **(undefined8 **)(*(long *)puVar2 + 0xb8) = uVar4;
  return;
}



// ==========================================================================================
