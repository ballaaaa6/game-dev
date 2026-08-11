// Function: Microsoft_Win32_Win32Native__GetMessage
// Address: 019912a0
// ==========================================================================================

void Microsoft_Win32_Win32Native__GetMessage(undefined4 param_1)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined4 local_14;
  
  puVar1 = PTR_StringLiteral_2946_01fd2c58;
  local_14 = param_1;
  if ((DAT_02101629 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_2946_01fd2c58);
    DAT_02101629 = 1;
  }
  uVar2 = System_Int32__ToString(&local_14,0);
  System_String__Concat(*(undefined8 *)puVar1,uVar2);
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_Win32Native__MakeHRFromErrorCode
// Address: 019912fc
// ==========================================================================================

uint Microsoft_Win32_Win32Native__MakeHRFromErrorCode(uint param_1)

{
  return param_1 | 0x80070000;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeFileHandle___ctor
// Address: 01991308
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeFileHandle___ctor(long param_1,undefined8 param_2,uint param_3)

{
  System_Runtime_InteropServices_SafeHandle___ctor(param_1,0,param_3 & 1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor
// Address: 01991338
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor
               (undefined8 param_1,uint param_2)

{
  System_Runtime_InteropServices_SafeHandle___ctor(param_1,0,param_2 & 1,0);
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeFileHandle__ReleaseHandle
// Address: 01991348
// ==========================================================================================

bool Microsoft_Win32_SafeHandles_SafeFileHandle__ReleaseHandle(long param_1)

{
  undefined *puVar1;
  undefined8 uVar2;
  int local_24;
  
  puVar1 = PTR_System_IO_MonoIO_TypeInfo_01fd2c60;
  if ((DAT_0210162a & 1) == 0) {
    FUN_00db0bbc(PTR_System_IO_MonoIO_TypeInfo_01fd2c60);
    DAT_0210162a = 1;
  }
  local_24 = 0;
  uVar2 = *(undefined8 *)(param_1 + 0x10);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  System_IO_MonoIO__Close(uVar2,&local_24,0);
  return local_24 == 0;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeWaitHandle___ctor
// Address: 019913c4
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeWaitHandle___ctor(undefined8 param_1)

{
  System_Runtime_InteropServices_SafeHandle___ctor(param_1,0,1,0);
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeWaitHandle___ctor
// Address: 019913d4
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeWaitHandle___ctor(long param_1,undefined8 param_2,uint param_3)

{
  System_Runtime_InteropServices_SafeHandle___ctor(param_1,0,param_3 & 1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeWaitHandle__ReleaseHandle
// Address: 01991404
// ==========================================================================================

undefined8 Microsoft_Win32_SafeHandles_SafeWaitHandle__ReleaseHandle(long param_1)

{
  System_Threading_NativeEventCalls__CloseEvent_internal(*(undefined8 *)(param_1 + 0x10),0);
  return 1;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid__get_IsInvalid
// Address: 01991420
// ==========================================================================================

uint Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid__get_IsInvalid(long param_1)

{
  uint uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 local_18;
  
  uVar2 = System_IntPtr__IsNull((undefined8 *)(param_1 + 0x10),0);
  if ((uVar2 & 1) == 0) {
    uVar3 = *(undefined8 *)(param_1 + 0x10);
    local_18 = 0;
    System_IntPtr___ctor(&local_18,0xffffffff,0);
    uVar1 = System_IntPtr__op_Equality(uVar3,local_18,0);
  }
  else {
    uVar1 = 1;
  }
  return uVar1 & 1;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor
// Address: 01b5393c
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor
               (long param_1,undefined8 param_2,uint param_3)

{
  Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor(param_1,param_3 & 1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__GetCurrentProcess
// Address: 01b53968
// ==========================================================================================

undefined8 Microsoft_Win32_NativeMethods__GetCurrentProcess(void)

{
  undefined4 auStack_68 [2];
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> abStack_60 [16];
  void *pvStack_50;
  undefined4 uStack_48;
  undefined8 uStack_40;
  undefined4 uStack_38;
  basic_string abStack_30 [16];
  void *pvStack_20;
  undefined4 uStack_18;
  
  FUN_00df836c(&uStack_40);
  auStack_68[0] = uStack_38;
  std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
  basic_string(abStack_60,abStack_30);
  uStack_48 = uStack_18;
  FUN_00e285b0(auStack_68);
  if (((byte)abStack_60[0] & 1) != 0) {
    operator_delete(pvStack_50);
  }
  if (((byte)abStack_30[0] & 1) != 0) {
    operator_delete(pvStack_20);
  }
  return uStack_40;
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__GetExitCodeProcess
// Address: 01b5396c
// ==========================================================================================

bool Microsoft_Win32_NativeMethods__GetExitCodeProcess(void)

{
  undefined4 auStack_68 [2];
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> abStack_60 [16];
  void *pvStack_50;
  undefined4 uStack_48;
  char acStack_40 [8];
  undefined4 uStack_38;
  basic_string abStack_30 [16];
  void *pvStack_20;
  undefined4 uStack_18;
  
  FUN_00db0ac4(acStack_40);
  auStack_68[0] = uStack_38;
  std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
  basic_string(abStack_60,abStack_30);
  uStack_48 = uStack_18;
  FUN_00e285b0(auStack_68);
  if (((byte)abStack_60[0] & 1) != 0) {
    operator_delete(pvStack_50);
  }
  if (((byte)abStack_30[0] & 1) != 0) {
    operator_delete(pvStack_20);
  }
  return acStack_40[0] != '\0';
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__GetExitCodeProcess
// Address: 01b53970
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x01b53a1c) */

uint Microsoft_Win32_NativeMethods__GetExitCodeProcess(long param_1,undefined8 param_2)

{
  uint uVar1;
  char local_24 [4];
  
  local_24[0] = '\0';
  if (param_1 != 0) {
                    /* try { // try from 01b5398c to 01b5399b has its CatchHandler @ 01b539e4 */
    Method_System_Runtime_InteropServices_SafeHandle_DangerousAddRef(param_1,local_24,0);
                    /* try { // try from 01b539a0 to 01b539a7 has its CatchHandler @ 01b539e0 */
    uVar1 = FUN_00daeea8(*(undefined8 *)(param_1 + 0x10),param_2);
    if (local_24[0] != '\0') {
      System_Runtime_InteropServices_SafeHandle__DangerousRelease(param_1,0);
    }
    return uVar1 & 1;
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01b539dc to 01b539df has its CatchHandler @ 01b539e4 */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__TerminateProcess
// Address: 01b53a68
// ==========================================================================================

void Microsoft_Win32_NativeMethods__TerminateProcess(void)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00e29d04(
                      "C:/Program Files/Unity/Hub/Editor/2022.3.62f2/Editor/Data/il2cpp/libil2cpp/icalls/System/Microsoft.Win32/NativeMethods.cpp(55) : Unsupported internal call for IL2CPP:NativeMethods::SetPriorityClass - \"IL2CPP does not support process termination\""
                      );
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar1,0);
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__TerminateProcess
// Address: 01b53a6c
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x01b53b18) */

uint Microsoft_Win32_NativeMethods__TerminateProcess(long param_1,undefined4 param_2)

{
  uint uVar1;
  char local_24 [4];
  
  local_24[0] = '\0';
  if (param_1 != 0) {
                    /* try { // try from 01b53a88 to 01b53a97 has its CatchHandler @ 01b53ae0 */
    Method_System_Runtime_InteropServices_SafeHandle_DangerousAddRef(param_1,local_24,0);
                    /* try { // try from 01b53a9c to 01b53aa3 has its CatchHandler @ 01b53adc */
    uVar1 = FUN_00daef50(*(undefined8 *)(param_1 + 0x10),param_2);
    if (local_24[0] != '\0') {
      System_Runtime_InteropServices_SafeHandle__DangerousRelease(param_1,0);
    }
    return uVar1 & 1;
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01b53ad8 to 01b53adb has its CatchHandler @ 01b53ae0 */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__GetCurrentProcessId
// Address: 01b53b64
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__pid_t Microsoft_Win32_NativeMethods__GetCurrentProcessId(void)

{
  __pid_t _Var1;
  
  _Var1 = (*(code *)PTR_getpid_01ff6050)();
  return _Var1;
}



// ==========================================================================================
// Function: Microsoft_Win32_NativeMethods__CloseProcess
// Address: 01b53b68
// ==========================================================================================

undefined8 Microsoft_Win32_NativeMethods__CloseProcess(void)

{
  void *pvVar1;
  undefined8 uVar2;
  byte abStack_28 [16];
  void *pvStack_18;
  
  FUN_00e0e578(abStack_28);
  pvVar1 = (void *)((ulong)abStack_28 | 1);
  if ((abStack_28[0] & 1) != 0) {
    pvVar1 = pvStack_18;
  }
  uVar2 = FUN_00e0e65c(pvVar1);
  if ((abStack_28[0] & 1) != 0) {
    operator_delete(pvStack_18);
  }
  return uVar2;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor
// Address: 01b53b6c
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor(undefined8 param_1)

{
  Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor(param_1,1,0);
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor
// Address: 01b53b78
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeProcessHandle___ctor(long param_1,undefined8 param_2)

{
  Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor(param_1,1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeProcessHandle__ReleaseHandle
// Address: 01b53ba4
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeProcessHandle__ReleaseHandle(long param_1)

{
  thunk_FUN_00db0ac4(*(undefined8 *)(param_1 + 0x10));
  return;
}



// ==========================================================================================
// Function: Microsoft_Win32_SafeHandles_SafeProcessHandle___cctor
// Address: 01b53bac
// ==========================================================================================

void Microsoft_Win32_SafeHandles_SafeProcessHandle___cctor(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Microsoft_Win32_SafeHandles_SafeProcessHandle_TypeInfo_01fde980;
  if ((DAT_0210278b & 1) == 0) {
    FUN_00db0bbc(PTR_Microsoft_Win32_SafeHandles_SafeProcessHandle_TypeInfo_01fde980);
    DAT_0210278b = 1;
  }
  lVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Microsoft_Win32_SafeHandles_SafeHandleZeroOrMinusOneIsInvalid___ctor(lVar2,1,0);
  *(undefined8 *)(lVar2 + 0x10) = 0;
  **(long **)(*(long *)puVar1 + 0xb8) = lVar2;
  return;
}



// ==========================================================================================
// Function: Microsoft_CodeAnalysis_EmbeddedAttribute___ctor
// Address: 01c90064
// ==========================================================================================

void Microsoft_CodeAnalysis_EmbeddedAttribute___ctor(undefined8 param_1)

{
  System_Attribute___ctor(param_1,0);
  return;
}



// ==========================================================================================
