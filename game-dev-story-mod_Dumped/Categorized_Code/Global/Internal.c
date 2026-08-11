// Function: Internal_Threading_Tasks_Tracing_TaskTrace__get_Enabled
// Address: 0199147c
// ==========================================================================================

void Internal_Threading_Tasks_Tracing_TaskTrace__get_Enabled(void)

{
  undefined *puVar1;
  long *plVar2;
  
  puVar1 = PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68;
  if ((DAT_0210162b & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68);
    DAT_0210162b = 1;
  }
  plVar2 = **(long ***)(*(long *)puVar1 + 0xb8);
  if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x019914cc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x178))(plVar2,*(undefined8 *)(*plVar2 + 0x180));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitBegin_Asynchronous
// Address: 019914dc
// ==========================================================================================

void Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitBegin_Asynchronous
               (undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  undefined *puVar1;
  long *plVar2;
  
  puVar1 = PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68;
  if ((DAT_0210162c & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68);
    DAT_0210162c = 1;
  }
  plVar2 = **(long ***)(*(long *)puVar1 + 0xb8);
  if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x0199154c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x188))(plVar2,param_1,param_2,param_3,*(undefined8 *)(*plVar2 + 400));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitBegin_Synchronous
// Address: 01991560
// ==========================================================================================

void Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitBegin_Synchronous
               (undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  undefined *puVar1;
  long *plVar2;
  
  puVar1 = PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68;
  if ((DAT_0210162d & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68);
    DAT_0210162d = 1;
  }
  plVar2 = **(long ***)(*(long *)puVar1 + 0xb8);
  if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x019915d0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x198))(plVar2,param_1,param_2,param_3,*(undefined8 *)(*plVar2 + 0x1a0));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitEnd
// Address: 019915e4
// ==========================================================================================

void Internal_Threading_Tasks_Tracing_TaskTrace__TaskWaitEnd
               (undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  undefined *puVar1;
  long *plVar2;
  
  puVar1 = PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68;
  if ((DAT_0210162e & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68);
    DAT_0210162e = 1;
  }
  plVar2 = **(long ***)(*(long *)puVar1 + 0xb8);
  if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x01991654. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x1a8))(plVar2,param_1,param_2,param_3,*(undefined8 *)(*plVar2 + 0x1b0));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Internal_Threading_Tasks_Tracing_TaskTrace__TaskScheduled
// Address: 01991668
// ==========================================================================================

void Internal_Threading_Tasks_Tracing_TaskTrace__TaskScheduled
               (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  undefined *puVar1;
  long *plVar2;
  
  puVar1 = PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68;
  if ((DAT_0210162f & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Threading_Tasks_Tracing_TaskTrace_TypeInfo_01fd2c68);
    DAT_0210162f = 1;
  }
  plVar2 = **(long ***)(*(long *)puVar1 + 0xb8);
  if (plVar2 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x019916f0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x1b8))
              (plVar2,param_1,param_2,param_3,param_4,param_5,*(undefined8 *)(*plVar2 + 0x1c0));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeAugments__ReportUnhandledException
// Address: 01991708
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeAugments__ReportUnhandledException(undefined8 param_1)

{
  long lVar1;
  
  lVar1 = Method_System_Runtime_ExceptionServices_ExceptionDispatchInfo_Capture(param_1,0);
  if (lVar1 != 0) {
                    /* WARNING: Subroutine does not return */
    Method_System_Runtime_ExceptionServices_ExceptionDispatchInfo_Throw(lVar1,0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeAugments__get_Callbacks
// Address: 01991728
// ==========================================================================================

undefined8 Internal_Runtime_Augments_RuntimeAugments__get_Callbacks(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Internal_Runtime_Augments_RuntimeAugments_TypeInfo_01fd2c70;
  if ((DAT_02101630 & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Runtime_Augments_RuntimeAugments_TypeInfo_01fd2c70);
    DAT_02101630 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return **(undefined8 **)(lVar2 + 0xb8);
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeAugments___cctor
// Address: 01991780
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeAugments___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks_TypeInfo_01fd2c78;
  puVar1 = PTR_Internal_Runtime_Augments_RuntimeAugments_TypeInfo_01fd2c70;
  if ((DAT_02101631 & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks_TypeInfo_01fd2c78)
    ;
    FUN_00db0bbc(PTR_Internal_Runtime_Augments_RuntimeAugments_TypeInfo_01fd2c70);
    DAT_02101631 = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  System_Object___ctor(uVar3,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar3;
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks___ctor
// Address: 019917f0
// ==========================================================================================

void Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks__CreateMissingMetadataException
// Address: 019917f8
// ==========================================================================================

undefined8
Internal_Runtime_Augments_ReflectionExecutionDomainCallbacks__CreateMissingMetadataException(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_System_Reflection_MissingMetadataException_TypeInfo_01fd2c80;
  if ((DAT_02101632 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Reflection_MissingMetadataException_TypeInfo_01fd2c80);
    DAT_02101632 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Reflection_MissingMetadataException___ctor(uVar2,0);
  return uVar2;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread___ctor
// Address: 0199184c
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread___ctor(long param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__Create
// Address: 01991874
// ==========================================================================================

long Internal_Runtime_Augments_RuntimeThread__Create(undefined8 param_1,undefined4 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  long lVar4;
  
  puVar2 = PTR_System_Threading_Thread_TypeInfo_01fcd5f0;
  puVar1 = PTR_Internal_Runtime_Augments_RuntimeThread_TypeInfo_01fc6cc8;
  if ((DAT_02101633 & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Runtime_Augments_RuntimeThread_TypeInfo_01fc6cc8);
    FUN_00db0bbc(PTR_System_Threading_Thread_TypeInfo_01fcd5f0);
    DAT_02101633 = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  Method_System_Threading_Thread__ctor(uVar3,param_1,param_2,0);
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  *(undefined8 *)(lVar4 + 0x10) = uVar3;
  return lVar4;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__set_IsBackground
// Address: 0199190c
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread__set_IsBackground(long param_1,uint param_2)

{
  if (*(long *)(param_1 + 0x10) != 0) {
    System_Threading_Thread__set_IsBackground(*(long *)(param_1 + 0x10),param_2 & 1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__Start
// Address: 0199192c
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread__Start(long param_1,undefined8 param_2)

{
  if (*(long *)(param_1 + 0x10) != 0) {
    Method_System_Threading_Thread_Start(*(long *)(param_1 + 0x10),param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__Sleep
// Address: 01991948
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread__Sleep(undefined8 param_1)

{
  Method_System_Threading_Thread_Sleep(param_1,0);
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__Yield
// Address: 01991950
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread__Yield(void)

{
  System_Threading_Thread__Yield(0);
  return;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__SpinWait
// Address: 01991958
// ==========================================================================================

undefined8 Internal_Runtime_Augments_RuntimeThread__SpinWait(undefined8 param_1)

{
  System_Threading_Thread__SpinWait(param_1,0);
  return 1;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread__GetCurrentProcessorId
// Address: 01991970
// ==========================================================================================

undefined8 Internal_Runtime_Augments_RuntimeThread__GetCurrentProcessorId(void)

{
  return 1;
}



// ==========================================================================================
// Function: Internal_Runtime_Augments_RuntimeThread___cctor
// Address: 01991978
// ==========================================================================================

void Internal_Runtime_Augments_RuntimeThread___cctor(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_Internal_Runtime_Augments_RuntimeThread_TypeInfo_01fc6cc8;
  if ((DAT_02101634 & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Runtime_Augments_RuntimeThread_TypeInfo_01fc6cc8);
    DAT_02101634 = 1;
  }
  **(undefined4 **)(*(long *)puVar1 + 0xb8) = 0x40;
  return;
}



// ==========================================================================================
// Function: Internal_Cryptography_OidLookup__ShouldUseCache
// Address: 01b516b4
// ==========================================================================================

undefined8 Internal_Cryptography_OidLookup__ShouldUseCache(void)

{
  return 1;
}



// ==========================================================================================
// Function: Internal_Cryptography_OidLookup__NativeFriendlyNameToOid
// Address: 01b516bc
// ==========================================================================================

undefined8 Internal_Cryptography_OidLookup__NativeFriendlyNameToOid(undefined8 param_1)

{
  uint uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  
  if ((DAT_02102785 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_3109_01fde220);
    FUN_00db0bbc(PTR_StringLiteral_1077_01fde228);
    FUN_00db0bbc(PTR_StringLiteral_994_01fde230);
    FUN_00db0bbc(PTR_StringLiteral_3932_01fde238);
    FUN_00db0bbc(PTR_StringLiteral_995_01fde240);
    FUN_00db0bbc(PTR_StringLiteral_4145_01fde248);
    FUN_00db0bbc(PTR_StringLiteral_993_01fde250);
    FUN_00db0bbc(PTR_StringLiteral_1073_01fde258);
    FUN_00db0bbc(PTR_StringLiteral_5082_01fde260);
    FUN_00db0bbc(PTR_StringLiteral_1079_01fde268);
    FUN_00db0bbc(PTR_StringLiteral_1075_01fde270);
    FUN_00db0bbc(PTR_StringLiteral_989_01fde278);
    FUN_00db0bbc(PTR_StringLiteral_4544_01fde280);
    FUN_00db0bbc(PTR_StringLiteral_2140_01fde288);
    FUN_00db0bbc(PTR_StringLiteral_5212_01fde290);
    FUN_00db0bbc(PTR_StringLiteral_2552_01fde298);
    FUN_00db0bbc(PTR_StringLiteral_5213_01fde2a0);
    FUN_00db0bbc(PTR_StringLiteral_1076_01fde2a8);
    FUN_00db0bbc(PTR_StringLiteral_4256_01fde2b0);
    FUN_00db0bbc(PTR_StringLiteral_987_01fde2b8);
    FUN_00db0bbc(PTR_StringLiteral_1078_01fde2c0);
    FUN_00db0bbc(PTR_StringLiteral_7916_01fde2c8);
    DAT_02102785 = 1;
  }
  uVar1 = PrivateImplementationDetails___ComputeStringHash(param_1,0);
  if (uVar1 < 0x751680de) {
    if (uVar1 < 0x55d8b022) {
      if (uVar1 == 0x3a5710b) {
        uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_3932_01fde238,0)
        ;
        puVar4 = (undefined8 *)PTR_StringLiteral_1076_01fde2a8;
      }
      else {
        if (uVar1 != 0x55d8b021) {
          return 0;
        }
        uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_4544_01fde280,0)
        ;
        puVar4 = (undefined8 *)PTR_StringLiteral_987_01fde2b8;
      }
    }
    else if (uVar1 == 0x5bee62ef) {
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_5213_01fde2a0,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_1075_01fde270;
    }
    else if (uVar1 == 0x5f357efd) {
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_5082_01fde260,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_995_01fde240;
    }
    else {
      if (uVar1 != 0x751680dd) {
        return 0;
      }
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_2140_01fde288,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_1078_01fde2c0;
    }
  }
  else if (uVar1 < 0xb4301664) {
    if (uVar1 == 0x953b2236) {
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_2552_01fde298,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_993_01fde250;
    }
    else if (uVar1 == 0x9dcf2034) {
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_4256_01fde2b0,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_1073_01fde258;
    }
    else {
      if (uVar1 != 0xb4301663) {
        return 0;
      }
      uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_5212_01fde290,0);
      puVar4 = (undefined8 *)PTR_StringLiteral_1077_01fde228;
    }
  }
  else if (uVar1 == 0xb85a3360) {
    uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_3109_01fde220,0);
    puVar4 = (undefined8 *)PTR_StringLiteral_1079_01fde268;
  }
  else if (uVar1 == 0xccb33eb4) {
    uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_4145_01fde248,0);
    puVar4 = (undefined8 *)PTR_StringLiteral_994_01fde230;
  }
  else {
    if (uVar1 != 0xe2748de9) {
      return 0;
    }
    uVar2 = System_String__op_Equality(param_1,*(undefined8 *)PTR_StringLiteral_7916_01fde2c8,0);
    puVar4 = (undefined8 *)PTR_StringLiteral_989_01fde278;
  }
  uVar3 = *puVar4;
  if ((uVar2 & 1) == 0) {
    uVar3 = 0;
  }
  return uVar3;
}



// ==========================================================================================
// Function: Internal_Cryptography_OidLookup___cctor
// Address: 01b51a78
// ==========================================================================================

void Internal_Cryptography_OidLookup___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined *puVar9;
  undefined *puVar10;
  undefined8 uVar11;
  long lVar12;
  long lVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  
  puVar2 = 
  PTR_Method_System_Collections_Concurrent_ConcurrentDictionary_string__string___ctor_01fde2d8;
  puVar4 = PTR_System_Collections_Concurrent_ConcurrentDictionary_string__string__TypeInfo_01fde2d0;
  puVar1 = PTR_Internal_Cryptography_OidLookup_TypeInfo_01fde208;
  puVar3 = PTR_System_StringComparer_TypeInfo_01fd31d0;
  if ((DAT_02102786 & 1) == 0) {
    FUN_00db0bbc(
                PTR_Method_System_Collections_Concurrent_ConcurrentDictionary_string__string___ctor_01fde2e0
                );
    FUN_00db0bbc(
                PTR_Method_System_Collections_Concurrent_ConcurrentDictionary_string__string___ctor_01fde2d8
                );
    FUN_00db0bbc(
                PTR_System_Collections_Concurrent_ConcurrentDictionary_string__string__TypeInfo_01fde2d0
                );
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_Dictionary_string__string__Add_01fd79b0);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_Dictionary_string__string___ctor_01fde2e8);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_Dictionary_string__string___ctor_01fc9900);
    FUN_00db0bbc(PTR_System_Collections_Generic_Dictionary_string__string__TypeInfo_01fc9910);
    FUN_00db0bbc(
                PTR_Method_System_Linq_Enumerable_ToDictionary_KeyValuePair_string__string___string__string_01fde2f0
                );
    FUN_00db0bbc(PTR_System_Func_KeyValuePair_string__string___string__TypeInfo_01fde2f8);
    FUN_00db0bbc(PTR_Internal_Cryptography_OidLookup_TypeInfo_01fde208);
    FUN_00db0bbc(PTR_System_StringComparer_TypeInfo_01fd31d0);
    FUN_00db0bbc(PTR_Method_Internal_Cryptography_OidLookup___c___cctor_b__10_0_01fde300);
    FUN_00db0bbc(PTR_Method_Internal_Cryptography_OidLookup___c___cctor_b__10_1_01fde308);
    FUN_00db0bbc(PTR_Internal_Cryptography_OidLookup___c_TypeInfo_01fde310);
    FUN_00db0bbc(PTR_StringLiteral_6908_01fde318);
    FUN_00db0bbc(PTR_StringLiteral_974_01fde320);
    FUN_00db0bbc(PTR_StringLiteral_6896_01fde328);
    FUN_00db0bbc(PTR_StringLiteral_2242_01fc7d88);
    FUN_00db0bbc(PTR_StringLiteral_984_01fde330);
    FUN_00db0bbc(PTR_StringLiteral_1031_01fde338);
    FUN_00db0bbc(PTR_StringLiteral_986_01fde340);
    FUN_00db0bbc(PTR_StringLiteral_4935_01fca510);
    FUN_00db0bbc(PTR_StringLiteral_1070_01fde348);
    FUN_00db0bbc(PTR_StringLiteral_1090_01fde350);
    FUN_00db0bbc(PTR_StringLiteral_1030_01fde358);
    FUN_00db0bbc(PTR_StringLiteral_1021_01fde360);
    FUN_00db0bbc(PTR_StringLiteral_1085_01fde368);
    FUN_00db0bbc(PTR_StringLiteral_1002_01fde370);
    FUN_00db0bbc(PTR_StringLiteral_7318_01fde378);
    FUN_00db0bbc(PTR_StringLiteral_983_01fde380);
    FUN_00db0bbc(PTR_StringLiteral_1092_01fde388);
    FUN_00db0bbc(PTR_StringLiteral_964_01fde390);
    FUN_00db0bbc(PTR_StringLiteral_1001_01fde398);
    FUN_00db0bbc(PTR_StringLiteral_1065_01fde3a0);
    FUN_00db0bbc(PTR_StringLiteral_1096_01fde3a8);
    FUN_00db0bbc(PTR_StringLiteral_8977_01fde3b0);
    FUN_00db0bbc(PTR_StringLiteral_8520_01fde3b8);
    FUN_00db0bbc(PTR_StringLiteral_1000_01fde3c0);
    FUN_00db0bbc(PTR_StringLiteral_7268_01fde3c8);
    FUN_00db0bbc(PTR_StringLiteral_1095_01fde3d0);
    FUN_00db0bbc(PTR_StringLiteral_969_01fde3d8);
    FUN_00db0bbc(PTR_StringLiteral_2857_01fde3e0);
    FUN_00db0bbc(PTR_StringLiteral_8459_01fde3e8);
    FUN_00db0bbc(PTR_StringLiteral_985_01fde3f0);
    FUN_00db0bbc(PTR_StringLiteral_8460_01fde3f8);
    FUN_00db0bbc(PTR_StringLiteral_6091_01fde400);
    FUN_00db0bbc(PTR_StringLiteral_9033_01fde408);
    FUN_00db0bbc(PTR_StringLiteral_2241_01fde410);
    FUN_00db0bbc(PTR_StringLiteral_6907_01fde418);
    FUN_00db0bbc(PTR_StringLiteral_2856_01fde420);
    FUN_00db0bbc(PTR_StringLiteral_975_01fde428);
    FUN_00db0bbc(PTR_StringLiteral_1091_01fde430);
    FUN_00db0bbc(PTR_StringLiteral_1074_01fde438);
    FUN_00db0bbc(PTR_StringLiteral_9689_01fde440);
    FUN_00db0bbc(PTR_StringLiteral_8976_01fde448);
    FUN_00db0bbc(PTR_StringLiteral_1041_01fde450);
    FUN_00db0bbc(PTR_StringLiteral_1084_01fde458);
    FUN_00db0bbc(PTR_StringLiteral_968_01fde460);
    FUN_00db0bbc(PTR_StringLiteral_4707_01fde468);
    FUN_00db0bbc(PTR_StringLiteral_1008_01fde470);
    FUN_00db0bbc(PTR_StringLiteral_1064_01fde478);
    FUN_00db0bbc(PTR_StringLiteral_972_01fde480);
    FUN_00db0bbc(PTR_StringLiteral_962_01fde488);
    FUN_00db0bbc(PTR_StringLiteral_1036_01fde490);
    FUN_00db0bbc(PTR_StringLiteral_3254_01fc3740);
    FUN_00db0bbc(PTR_StringLiteral_4955_01fde498);
    FUN_00db0bbc(PTR_StringLiteral_967_01fde4a0);
    FUN_00db0bbc(PTR_StringLiteral_9039_01fde4a8);
    FUN_00db0bbc(PTR_StringLiteral_9688_01fde4b0);
    FUN_00db0bbc(PTR_StringLiteral_998_01fde4b8);
    FUN_00db0bbc(PTR_StringLiteral_2855_01fde4c0);
    FUN_00db0bbc(PTR_StringLiteral_1094_01fde4c8);
    FUN_00db0bbc(PTR_StringLiteral_988_01fde4d0);
    FUN_00db0bbc(PTR_StringLiteral_1034_01fde4d8);
    FUN_00db0bbc(PTR_StringLiteral_8521_01fde4e0);
    FUN_00db0bbc(PTR_StringLiteral_1040_01fde4e8);
    FUN_00db0bbc(PTR_StringLiteral_996_01fde4f0);
    FUN_00db0bbc(PTR_StringLiteral_1013_01fde4f8);
    FUN_00db0bbc(PTR_StringLiteral_929_01fde500);
    FUN_00db0bbc(PTR_StringLiteral_1006_01fde508);
    FUN_00db0bbc(PTR_StringLiteral_2837_01fcaf28);
    FUN_00db0bbc(PTR_StringLiteral_9027_01fde510);
    FUN_00db0bbc(PTR_StringLiteral_971_01fde518);
    FUN_00db0bbc(PTR_StringLiteral_9685_01fde520);
    FUN_00db0bbc(PTR_StringLiteral_4808_01fde528);
    FUN_00db0bbc(PTR_StringLiteral_6898_01fde530);
    FUN_00db0bbc(PTR_StringLiteral_9035_01fde538);
    FUN_00db0bbc(PTR_StringLiteral_2707_01fde540);
    FUN_00db0bbc(PTR_StringLiteral_2697_01fde548);
    FUN_00db0bbc(PTR_StringLiteral_1039_01fde550);
    FUN_00db0bbc(PTR_StringLiteral_4942_01fde558);
    FUN_00db0bbc(PTR_StringLiteral_2240_01fde560);
    FUN_00db0bbc(PTR_StringLiteral_9029_01fde568);
    FUN_00db0bbc(PTR_StringLiteral_1087_01fde570);
    FUN_00db0bbc(PTR_StringLiteral_9030_01fde578);
    FUN_00db0bbc(PTR_StringLiteral_1068_01fde580);
    FUN_00db0bbc(PTR_StringLiteral_959_01fde588);
    FUN_00db0bbc(PTR_StringLiteral_8978_01fde590);
    FUN_00db0bbc(PTR_StringLiteral_1072_01fde598);
    FUN_00db0bbc(PTR_StringLiteral_1035_01fde5a0);
    FUN_00db0bbc(PTR_StringLiteral_1027_01fde5a8);
    FUN_00db0bbc(PTR_StringLiteral_977_01fde5b0);
    FUN_00db0bbc(PTR_StringLiteral_1067_01fde5b8);
    FUN_00db0bbc(PTR_StringLiteral_6902_01fde5c0);
    FUN_00db0bbc(PTR_StringLiteral_3423_01fcb1e0);
    FUN_00db0bbc(PTR_StringLiteral_4810_01fde5c8);
    FUN_00db0bbc(PTR_StringLiteral_9623_01fde5d0);
    FUN_00db0bbc(PTR_StringLiteral_973_01fde5d8);
    FUN_00db0bbc(PTR_StringLiteral_991_01fde5e0);
    FUN_00db0bbc(PTR_StringLiteral_2678_01fde5e8);
    FUN_00db0bbc(PTR_StringLiteral_8384_01fde5f0);
    FUN_00db0bbc(PTR_StringLiteral_1062_01fde5f8);
    FUN_00db0bbc(PTR_StringLiteral_1007_01fde600);
    FUN_00db0bbc(PTR_StringLiteral_8387_01fde608);
    FUN_00db0bbc(PTR_StringLiteral_1086_01fde610);
    FUN_00db0bbc(PTR_StringLiteral_5259_01fcb380);
    FUN_00db0bbc(PTR_StringLiteral_4809_01fde618);
    FUN_00db0bbc(PTR_StringLiteral_3944_01fccb20);
    FUN_00db0bbc(PTR_StringLiteral_6906_01fde620);
    FUN_00db0bbc(PTR_StringLiteral_1015_01fde628);
    FUN_00db0bbc(PTR_StringLiteral_9686_01fde630);
    FUN_00db0bbc(PTR_StringLiteral_1026_01fde638);
    FUN_00db0bbc(PTR_StringLiteral_9036_01fde640);
    FUN_00db0bbc(PTR_StringLiteral_8385_01fde648);
    FUN_00db0bbc(PTR_StringLiteral_9032_01fde650);
    FUN_00db0bbc(PTR_StringLiteral_9040_01fde658);
    FUN_00db0bbc(PTR_StringLiteral_1083_01fde660);
    FUN_00db0bbc(PTR_StringLiteral_9026_01fde668);
    FUN_00db0bbc(PTR_StringLiteral_8389_01fde670);
    FUN_00db0bbc(PTR_StringLiteral_9031_01fde678);
    FUN_00db0bbc(PTR_StringLiteral_8979_01fde680);
    FUN_00db0bbc(PTR_StringLiteral_8388_01fde688);
    FUN_00db0bbc(PTR_StringLiteral_6659_01fde690);
    FUN_00db0bbc(PTR_StringLiteral_978_01fde698);
    FUN_00db0bbc(PTR_StringLiteral_4665_01fde6a0);
    FUN_00db0bbc(PTR_StringLiteral_965_01fde6a8);
    FUN_00db0bbc(PTR_StringLiteral_1126_01fde6b0);
    FUN_00db0bbc(PTR_StringLiteral_8416_01fde6b8);
    FUN_00db0bbc(PTR_StringLiteral_1088_01fde6c0);
    FUN_00db0bbc(PTR_StringLiteral_1010_01fde6c8);
    FUN_00db0bbc(PTR_StringLiteral_6900_01fde6d0);
    FUN_00db0bbc(PTR_StringLiteral_2860_01fde6d8);
    FUN_00db0bbc(PTR_StringLiteral_1005_01fde6e0);
    FUN_00db0bbc(PTR_StringLiteral_7334_01fde6e8);
    FUN_00db0bbc(PTR_StringLiteral_1081_01fde6f0);
    FUN_00db0bbc(PTR_StringLiteral_4399_01fcb7e0);
    FUN_00db0bbc(PTR_StringLiteral_1023_01fde6f8);
    FUN_00db0bbc(PTR_StringLiteral_999_01fde700);
    FUN_00db0bbc(PTR_StringLiteral_6657_01fde708);
    FUN_00db0bbc(PTR_StringLiteral_1012_01fde710);
    FUN_00db0bbc(PTR_StringLiteral_1024_01fde718);
    FUN_00db0bbc(PTR_StringLiteral_4548_01fde720);
    FUN_00db0bbc(PTR_StringLiteral_997_01fde728);
    FUN_00db0bbc(PTR_StringLiteral_1011_01fde730);
    FUN_00db0bbc(PTR_StringLiteral_960_01fde738);
    FUN_00db0bbc(PTR_StringLiteral_1019_01fde740);
    FUN_00db0bbc(PTR_StringLiteral_1029_01fde748);
    FUN_00db0bbc(PTR_StringLiteral_980_01fde750);
    FUN_00db0bbc(PTR_StringLiteral_4811_01fde758);
    FUN_00db0bbc(PTR_StringLiteral_1082_01fde760);
    FUN_00db0bbc(PTR_StringLiteral_1063_01fde768);
    FUN_00db0bbc(PTR_StringLiteral_9028_01fde770);
    FUN_00db0bbc(PTR_StringLiteral_9117_01fde778);
    FUN_00db0bbc(PTR_StringLiteral_1004_01fde780);
    FUN_00db0bbc(PTR_StringLiteral_6901_01fde788);
    FUN_00db0bbc(PTR_StringLiteral_1016_01fde790);
    FUN_00db0bbc(PTR_StringLiteral_1009_01fde798);
    FUN_00db0bbc(PTR_StringLiteral_979_01fde7a0);
    FUN_00db0bbc(PTR_StringLiteral_6895_01fde7a8);
    FUN_00db0bbc(PTR_StringLiteral_9687_01fde7b0);
    FUN_00db0bbc(PTR_StringLiteral_1020_01fde7b8);
    FUN_00db0bbc(PTR_StringLiteral_970_01fde7c0);
    FUN_00db0bbc(PTR_StringLiteral_4414_01fde7c8);
    FUN_00db0bbc(PTR_StringLiteral_961_01fde7d0);
    FUN_00db0bbc(PTR_StringLiteral_1033_01fde7d8);
    FUN_00db0bbc(PTR_StringLiteral_4220_01fde7e0);
    FUN_00db0bbc(PTR_StringLiteral_8811_01fde7e8);
    FUN_00db0bbc(PTR_StringLiteral_8386_01fde7f0);
    FUN_00db0bbc(PTR_StringLiteral_7403_01fde7f8);
    FUN_00db0bbc(PTR_StringLiteral_992_01fde800);
    FUN_00db0bbc(PTR_StringLiteral_2218_01fcbbe8);
    FUN_00db0bbc(PTR_StringLiteral_1037_01fde808);
    FUN_00db0bbc(PTR_StringLiteral_966_01fde810);
    FUN_00db0bbc(PTR_StringLiteral_6905_01fde818);
    FUN_00db0bbc(PTR_StringLiteral_6904_01fde820);
    FUN_00db0bbc(PTR_StringLiteral_2876_01fde828);
    FUN_00db0bbc(PTR_StringLiteral_9034_01fde830);
    FUN_00db0bbc(PTR_StringLiteral_990_01fde838);
    FUN_00db0bbc(PTR_StringLiteral_2858_01fde840);
    FUN_00db0bbc(PTR_StringLiteral_1003_01fde848);
    FUN_00db0bbc(PTR_StringLiteral_1018_01fde850);
    FUN_00db0bbc(PTR_StringLiteral_1017_01fde858);
    FUN_00db0bbc(PTR_StringLiteral_982_01fde860);
    FUN_00db0bbc(PTR_StringLiteral_2269_01fde868);
    FUN_00db0bbc(PTR_StringLiteral_1097_01fde870);
    FUN_00db0bbc(PTR_StringLiteral_963_01fde878);
    FUN_00db0bbc(PTR_StringLiteral_9037_01fde880);
    FUN_00db0bbc(PTR_StringLiteral_1038_01fde888);
    FUN_00db0bbc(PTR_StringLiteral_1069_01fde890);
    FUN_00db0bbc(PTR_StringLiteral_6658_01fde898);
    FUN_00db0bbc(PTR_StringLiteral_1043_01fde8a0);
    FUN_00db0bbc(PTR_StringLiteral_2861_01fde8a8);
    FUN_00db0bbc(PTR_StringLiteral_8975_01fde8b0);
    FUN_00db0bbc(PTR_StringLiteral_1071_01fde8b8);
    FUN_00db0bbc(PTR_StringLiteral_1025_01fde8c0);
    FUN_00db0bbc(PTR_StringLiteral_6662_01fde8c8);
    FUN_00db0bbc(PTR_StringLiteral_1080_01fde8d0);
    FUN_00db0bbc(PTR_StringLiteral_9038_01fde8d8);
    FUN_00db0bbc(PTR_StringLiteral_1014_01fde8e0);
    FUN_00db0bbc(PTR_StringLiteral_981_01fde8e8);
    FUN_00db0bbc(PTR_StringLiteral_8980_01fde8f0);
    FUN_00db0bbc(PTR_StringLiteral_1032_01fde8f8);
    FUN_00db0bbc(PTR_StringLiteral_2859_01fde900);
    FUN_00db0bbc(PTR_StringLiteral_1022_01fde908);
    FUN_00db0bbc(PTR_StringLiteral_6660_01fde910);
    FUN_00db0bbc(PTR_StringLiteral_958_01fde918);
    FUN_00db0bbc(PTR_StringLiteral_2769_01fde920);
    FUN_00db0bbc(PTR_StringLiteral_8810_01fde928);
    FUN_00db0bbc(PTR_StringLiteral_6897_01fde930);
    FUN_00db0bbc(PTR_StringLiteral_1093_01fde938);
    FUN_00db0bbc(PTR_StringLiteral_6661_01fde940);
    FUN_00db0bbc(PTR_StringLiteral_6899_01fde948);
    FUN_00db0bbc(PTR_StringLiteral_6903_01fde950);
    FUN_00db0bbc(PTR_StringLiteral_1028_01fde958);
    FUN_00db0bbc(PTR_StringLiteral_976_01fde960);
    FUN_00db0bbc(PTR_StringLiteral_1066_01fde968);
    FUN_00db0bbc(PTR_StringLiteral_4963_01fde970);
    FUN_00db0bbc(PTR_StringLiteral_1089_01fde978);
    DAT_02102786 = 1;
  }
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  System_Collections_Concurrent_ConcurrentDictionary_object__object____ctor
            (uVar11,*(undefined8 *)puVar2);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar11;
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02101806 == '\0') {
    FUN_00db0bbc(PTR_System_StringComparer_TypeInfo_01fd31d0);
    DAT_02101806 = '\x01';
  }
  puVar2 = 
  PTR_Method_System_Collections_Concurrent_ConcurrentDictionary_string__string___ctor_01fde2e0;
  lVar12 = *(long *)puVar3;
  if (*(int *)(lVar12 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar12 = *(long *)puVar3;
  }
  uVar14 = *(undefined8 *)(*(long *)(lVar12 + 0xb8) + 0x18);
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  System_Collections_Concurrent_ConcurrentDictionary_object__object____ctor
            (uVar11,uVar14,*(undefined8 *)puVar2);
  *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = uVar11;
  if (DAT_02101806 == '\0') {
    FUN_00db0bbc(PTR_System_StringComparer_TypeInfo_01fd31d0);
    DAT_02101806 = '\x01';
  }
  puVar4 = PTR_Method_System_Collections_Generic_Dictionary_string__string___ctor_01fde2e8;
  puVar1 = PTR_System_Collections_Generic_Dictionary_string__string__TypeInfo_01fc9910;
  lVar12 = *(long *)puVar3;
  if (*(int *)(lVar12 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar12 = *(long *)puVar3;
  }
  uVar11 = *(undefined8 *)(*(long *)(lVar12 + 0xb8) + 0x18);
  lVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Collections_Generic_Dictionary_object__object____ctor(lVar12,uVar11,*(undefined8 *)puVar4);
  puVar10 = PTR_StringLiteral_1028_01fde958;
  puVar9 = PTR_StringLiteral_6903_01fde950;
  puVar8 = PTR_StringLiteral_6904_01fde820;
  puVar7 = PTR_StringLiteral_6905_01fde818;
  puVar6 = PTR_StringLiteral_1029_01fde748;
  puVar5 = PTR_StringLiteral_1039_01fde550;
  puVar2 = PTR_StringLiteral_2697_01fde548;
  puVar4 = PTR_StringLiteral_1040_01fde4e8;
  puVar1 = PTR_Internal_Cryptography_OidLookup___c_TypeInfo_01fde310;
  puVar3 = PTR_Method_System_Collections_Generic_Dictionary_string__string__Add_01fd79b0;
  if (lVar12 != 0) {
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_1126_01fde6b0,
               *(undefined8 *)PTR_StringLiteral_1001_01fde398,
               *(undefined8 *)
                PTR_Method_System_Collections_Generic_Dictionary_string__string__Add_01fd79b0);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6657_01fde708,
               *(undefined8 *)PTR_StringLiteral_1064_01fde478,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6658_01fde898,
               *(undefined8 *)PTR_StringLiteral_1069_01fde890,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6659_01fde690,
               *(undefined8 *)PTR_StringLiteral_1065_01fde3a0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6660_01fde910,
               *(undefined8 *)PTR_StringLiteral_1066_01fde968,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6661_01fde940,
               *(undefined8 *)PTR_StringLiteral_1067_01fde5b8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6662_01fde8c8,
               *(undefined8 *)PTR_StringLiteral_1068_01fde580,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6895_01fde7a8,
               *(undefined8 *)PTR_StringLiteral_1027_01fde5a8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6896_01fde328,
               *(undefined8 *)PTR_StringLiteral_1033_01fde7d8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6897_01fde930,
               *(undefined8 *)PTR_StringLiteral_1034_01fde4d8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6898_01fde530,
               *(undefined8 *)PTR_StringLiteral_1035_01fde5a0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6899_01fde948,
               *(undefined8 *)PTR_StringLiteral_1036_01fde490,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6900_01fde6d0,
               *(undefined8 *)PTR_StringLiteral_1037_01fde808,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6901_01fde788,
               *(undefined8 *)PTR_StringLiteral_1038_01fde888,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6902_01fde5c0,*(undefined8 *)puVar5,
               *(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)puVar9,*(undefined8 *)puVar4,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)puVar8,*(undefined8 *)puVar10,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)puVar7,*(undefined8 *)puVar6,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6906_01fde620,
               *(undefined8 *)PTR_StringLiteral_1030_01fde358,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6907_01fde418,
               *(undefined8 *)PTR_StringLiteral_1031_01fde338,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6908_01fde318,
               *(undefined8 *)PTR_StringLiteral_1032_01fde8f8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2218_01fcbbe8,
               *(undefined8 *)PTR_StringLiteral_1094_01fde4c8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2240_01fde560,
               *(undefined8 *)PTR_StringLiteral_991_01fde5e0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2241_01fde410,
               *(undefined8 *)PTR_StringLiteral_992_01fde800,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2242_01fc7d88,
               *(undefined8 *)PTR_StringLiteral_1088_01fde6c0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2269_01fde868,
               *(undefined8 *)PTR_StringLiteral_1041_01fde450,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2678_01fde5e8,
               *(undefined8 *)PTR_StringLiteral_929_01fde500,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_7268_01fde3c8,
               *(undefined8 *)PTR_StringLiteral_1025_01fde8c0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2769_01fde920,
               *(undefined8 *)PTR_StringLiteral_1083_01fde660,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)puVar2,*(undefined8 *)PTR_StringLiteral_974_01fde320,
               *(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_7318_01fde378,
               *(undefined8 *)PTR_StringLiteral_1092_01fde388,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2707_01fde540,
               *(undefined8 *)PTR_StringLiteral_959_01fde588,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_7334_01fde6e8,
               *(undefined8 *)PTR_StringLiteral_1021_01fde360,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2837_01fcaf28,
               *(undefined8 *)PTR_StringLiteral_988_01fde4d0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_7403_01fde7f8,
               *(undefined8 *)PTR_StringLiteral_958_01fde918,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2855_01fde4c0,
               *(undefined8 *)PTR_StringLiteral_961_01fde7d0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2856_01fde420,
               *(undefined8 *)PTR_StringLiteral_1013_01fde4f8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2857_01fde3e0,
               *(undefined8 *)PTR_StringLiteral_1011_01fde730,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2858_01fde840,
               *(undefined8 *)PTR_StringLiteral_1012_01fde710,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2859_01fde900,
               *(undefined8 *)PTR_StringLiteral_968_01fde460,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2860_01fde6d8,
               *(undefined8 *)PTR_StringLiteral_1007_01fde600,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2861_01fde8a8,
               *(undefined8 *)PTR_StringLiteral_1008_01fde470,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_2876_01fde828,
               *(undefined8 *)PTR_StringLiteral_990_01fde838,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_3254_01fc3740,
               *(undefined8 *)PTR_StringLiteral_1090_01fde350,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_3423_01fcb1e0,
               *(undefined8 *)PTR_StringLiteral_1091_01fde430,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_3944_01fccb20,
               *(undefined8 *)PTR_StringLiteral_1095_01fde3d0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8384_01fde5f0,
               *(undefined8 *)PTR_StringLiteral_996_01fde4f0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8385_01fde648,
               *(undefined8 *)PTR_StringLiteral_980_01fde750,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8386_01fde7f0,
               *(undefined8 *)PTR_StringLiteral_997_01fde728,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8387_01fde608,
               *(undefined8 *)PTR_StringLiteral_981_01fde8e8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8388_01fde688,
               *(undefined8 *)PTR_StringLiteral_998_01fde4b8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8389_01fde670,
               *(undefined8 *)PTR_StringLiteral_982_01fde860,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8416_01fde6b8,
               *(undefined8 *)PTR_StringLiteral_985_01fde3f0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8459_01fde3e8,
               *(undefined8 *)PTR_StringLiteral_1063_01fde768,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8460_01fde3f8,
               *(undefined8 *)PTR_StringLiteral_1062_01fde5f8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8520_01fde3b8,
               *(undefined8 *)PTR_StringLiteral_962_01fde488,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8521_01fde4e0,
               *(undefined8 *)PTR_StringLiteral_1006_01fde508,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4220_01fde7e0,
               *(undefined8 *)PTR_StringLiteral_1043_01fde8a0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4399_01fcb7e0,
               *(undefined8 *)PTR_StringLiteral_1080_01fde8d0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4414_01fde7c8,
               *(undefined8 *)PTR_StringLiteral_1081_01fde6f0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4665_01fde6a0,
               *(undefined8 *)PTR_StringLiteral_1086_01fde610,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4548_01fde720,
               *(undefined8 *)PTR_StringLiteral_1085_01fde368,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4707_01fde468,
               *(undefined8 *)PTR_StringLiteral_1084_01fde458,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8810_01fde928,
               *(undefined8 *)PTR_StringLiteral_999_01fde700,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8811_01fde7e8,
               *(undefined8 *)PTR_StringLiteral_1000_01fde3c0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4808_01fde528,
               *(undefined8 *)PTR_StringLiteral_975_01fde428,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4809_01fde618,
               *(undefined8 *)PTR_StringLiteral_984_01fde330,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4810_01fde5c8,
               *(undefined8 *)PTR_StringLiteral_976_01fde960,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4935_01fca510,
               *(undefined8 *)PTR_StringLiteral_1096_01fde3a8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8975_01fde8b0,
               *(undefined8 *)PTR_StringLiteral_1010_01fde6c8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8976_01fde448,
               *(undefined8 *)PTR_StringLiteral_1009_01fde798,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8977_01fde3b0,
               *(undefined8 *)PTR_StringLiteral_1003_01fde848,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8978_01fde590,
               *(undefined8 *)PTR_StringLiteral_1004_01fde780,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8979_01fde680,
               *(undefined8 *)PTR_StringLiteral_1005_01fde6e0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_8980_01fde8f0,
               *(undefined8 *)PTR_StringLiteral_1002_01fde370,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4942_01fde558,
               *(undefined8 *)PTR_StringLiteral_1093_01fde938,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9027_01fde510,
               *(undefined8 *)PTR_StringLiteral_1020_01fde7b8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9028_01fde770,
               *(undefined8 *)PTR_StringLiteral_960_01fde738,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9029_01fde568,
               *(undefined8 *)PTR_StringLiteral_969_01fde3d8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9030_01fde578,
               *(undefined8 *)PTR_StringLiteral_983_01fde380,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9031_01fde678,
               *(undefined8 *)PTR_StringLiteral_1070_01fde348,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9032_01fde650,
               *(undefined8 *)PTR_StringLiteral_971_01fde518,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9033_01fde408,
               *(undefined8 *)PTR_StringLiteral_977_01fde5b0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9034_01fde830,
               *(undefined8 *)PTR_StringLiteral_1071_01fde8b8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9035_01fde538,
               *(undefined8 *)PTR_StringLiteral_972_01fde480,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9036_01fde640,
               *(undefined8 *)PTR_StringLiteral_978_01fde698,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9037_01fde880,
               *(undefined8 *)PTR_StringLiteral_1072_01fde598,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9038_01fde8d8,
               *(undefined8 *)PTR_StringLiteral_973_01fde5d8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9039_01fde4a8,
               *(undefined8 *)PTR_StringLiteral_979_01fde7a0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4955_01fde498,
               *(undefined8 *)PTR_StringLiteral_1089_01fde978,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9117_01fde778,
               *(undefined8 *)PTR_StringLiteral_970_01fde7c0,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_4963_01fde970,
               *(undefined8 *)PTR_StringLiteral_1097_01fde870,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_5259_01fcb380,
               *(undefined8 *)PTR_StringLiteral_1082_01fde760,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9623_01fde5d0,
               *(undefined8 *)PTR_StringLiteral_1074_01fde438,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_6091_01fde400,
               *(undefined8 *)PTR_StringLiteral_1087_01fde570,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9685_01fde520,
               *(undefined8 *)PTR_StringLiteral_963_01fde878,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9686_01fde630,
               *(undefined8 *)PTR_StringLiteral_964_01fde390,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9687_01fde7b0,
               *(undefined8 *)PTR_StringLiteral_965_01fde6a8,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9688_01fde4b0,
               *(undefined8 *)PTR_StringLiteral_966_01fde810,*(undefined8 *)puVar3);
    System_Collections_Generic_Dictionary_object__object___Add
              (lVar12,*(undefined8 *)PTR_StringLiteral_9689_01fde440,
               *(undefined8 *)PTR_StringLiteral_967_01fde4a0,*(undefined8 *)puVar3);
    puVar4 = PTR_Internal_Cryptography_OidLookup_TypeInfo_01fde208;
    *(long *)(*(long *)(*(long *)PTR_Internal_Cryptography_OidLookup_TypeInfo_01fde208 + 0xb8) +
             0x10) = lVar12;
    lVar13 = *(long *)puVar1;
    if (*(int *)(lVar13 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar13 = *(long *)puVar1;
    }
    puVar5 = PTR_System_Func_KeyValuePair_string__string___string__TypeInfo_01fde2f8;
    puVar2 = PTR_System_Collections_Generic_Dictionary_string__string__TypeInfo_01fc9910;
    uVar14 = **(undefined8 **)(lVar13 + 0xb8);
    uVar11 = thunk_FUN_00e11c14(*(undefined8 *)
                                 PTR_System_Func_KeyValuePair_string__string___string__TypeInfo_01fde2f8
                               );
    System_Func_KeyValuePair_object__object___object____ctor
              (uVar11,uVar14,
               *(undefined8 *)
                PTR_Method_Internal_Cryptography_OidLookup___c___cctor_b__10_0_01fde300,0);
    uVar15 = **(undefined8 **)(*(long *)puVar1 + 0xb8);
    uVar14 = thunk_FUN_00e11c14(*(undefined8 *)puVar5);
    System_Func_KeyValuePair_object__object___object____ctor
              (uVar14,uVar15,
               *(undefined8 *)
                PTR_Method_Internal_Cryptography_OidLookup___c___cctor_b__10_1_01fde308,0);
    uVar11 = System_Linq_Enumerable__ToDictionary_KeyValuePair_object__object___object__object
                       (lVar12,uVar11,uVar14,
                        *(undefined8 *)
                         PTR_Method_System_Linq_Enumerable_ToDictionary_KeyValuePair_string__string___string__string_01fde2f0
                       );
    *(undefined8 *)(*(long *)(*(long *)puVar4 + 0xb8) + 0x18) = uVar11;
    lVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    Method_System_Collections_Generic_Dictionary_object__object___ctor
              (lVar12,*(undefined8 *)
                       PTR_Method_System_Collections_Generic_Dictionary_string__string___ctor_01fc9900
              );
    puVar10 = PTR_StringLiteral_1014_01fde8e0;
    puVar9 = PTR_StringLiteral_1017_01fde858;
    puVar8 = PTR_StringLiteral_1018_01fde850;
    puVar7 = PTR_StringLiteral_1016_01fde790;
    puVar6 = PTR_StringLiteral_4811_01fde758;
    puVar5 = PTR_StringLiteral_1019_01fde740;
    puVar2 = PTR_StringLiteral_9026_01fde668;
    puVar4 = PTR_StringLiteral_9040_01fde658;
    puVar1 = PTR_StringLiteral_1015_01fde628;
    if (lVar12 != 0) {
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)PTR_StringLiteral_986_01fde340,
                 *(undefined8 *)PTR_StringLiteral_2697_01fde548,*(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar10,*(undefined8 *)PTR_StringLiteral_2707_01fde540,
                 *(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar1,*(undefined8 *)PTR_StringLiteral_9028_01fde770,
                 *(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar7,*(undefined8 *)puVar4,*(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar9,*(undefined8 *)puVar2,*(undefined8 *)puVar3);
      puVar1 = PTR_StringLiteral_8387_01fde608;
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar8,*(undefined8 *)PTR_StringLiteral_8387_01fde608,
                 *(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)puVar5,*(undefined8 *)puVar6,*(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)PTR_StringLiteral_1022_01fde908,
                 *(undefined8 *)PTR_StringLiteral_9030_01fde578,*(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)PTR_StringLiteral_1023_01fde6f8,
                 *(undefined8 *)PTR_StringLiteral_8389_01fde670,*(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)PTR_StringLiteral_1024_01fde718,*(undefined8 *)puVar1,
                 *(undefined8 *)puVar3);
      System_Collections_Generic_Dictionary_object__object___Add
                (lVar12,*(undefined8 *)PTR_StringLiteral_1026_01fde638,
                 *(undefined8 *)PTR_StringLiteral_8385_01fde648,*(undefined8 *)puVar3);
      *(long *)(*(long *)(*(long *)PTR_Internal_Cryptography_OidLookup_TypeInfo_01fde208 + 0xb8) +
               0x20) = lVar12;
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Internal_Cryptography_OidLookup___c___cctor
// Address: 01b53724
// ==========================================================================================

void Internal_Cryptography_OidLookup___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_Internal_Cryptography_OidLookup___c_TypeInfo_01fde310;
  if ((DAT_02102787 & 1) == 0) {
    FUN_00db0bbc(PTR_Internal_Cryptography_OidLookup___c_TypeInfo_01fde310);
    DAT_02102787 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: Internal_Cryptography_OidLookup___c___ctor
// Address: 01b53780
// ==========================================================================================

void Internal_Cryptography_OidLookup___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
