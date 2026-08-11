// Function: Interop__GetExceptionForIoErrno
// Address: 019836f0
// ==========================================================================================

undefined8 Interop__GetExceptionForIoErrno(undefined8 param_1,long param_2,ulong param_3)

{
  undefined4 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  int iVar6;
  undefined8 local_28;
  
  local_28 = param_1;
  if ((DAT_021015c9 & 1) == 0) {
    FUN_00db0bbc(PTR_System_ArgumentOutOfRangeException_TypeInfo_01fc5598);
    FUN_00db0bbc(PTR_System_IO_DirectoryNotFoundException_TypeInfo_01fd2810);
    FUN_00db0bbc(PTR_System_IO_FileNotFoundException_TypeInfo_01fd2818);
    FUN_00db0bbc(PTR_System_IO_IOException_TypeInfo_01fbf720);
    FUN_00db0bbc(PTR_System_OperationCanceledException_TypeInfo_01fc6df8);
    FUN_00db0bbc(PTR_System_IO_PathTooLongException_TypeInfo_01fd2820);
    FUN_00db0bbc(PTR_System_UnauthorizedAccessException_TypeInfo_01fd21a8);
    FUN_00db0bbc(PTR_StringLiteral_2608_01fd2828);
    FUN_00db0bbc(PTR_StringLiteral_9533_01fc5f78);
    FUN_00db0bbc(PTR_StringLiteral_5455_01fd2830);
    FUN_00db0bbc(PTR_StringLiteral_5456_01fd2838);
    FUN_00db0bbc(PTR_StringLiteral_2605_01fd2840);
    FUN_00db0bbc(PTR_StringLiteral_1524_01fd2848);
    FUN_00db0bbc(PTR_StringLiteral_5836_01fd2850);
    FUN_00db0bbc(PTR_StringLiteral_5482_01fd2858);
    FUN_00db0bbc(PTR_StringLiteral_5124_01fd2860);
    FUN_00db0bbc(PTR_StringLiteral_1523_01fd2868);
    FUN_00db0bbc(PTR_StringLiteral_5452_01fd2870);
    FUN_00db0bbc(PTR_StringLiteral_2604_01fd2878);
    FUN_00db0bbc(PTR_StringLiteral_5407_01fd2880);
    DAT_021015c9 = 1;
  }
  iVar6 = (int)param_1;
  if (iVar6 < 0x1000c) {
    if (0x10006 < iVar6) {
      if (iVar6 != 0x10008) {
        if (iVar6 == 0x1000b) {
          uVar2 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_System_OperationCanceledException_TypeInfo_01fc6df8);
          System_OperationCanceledException___ctor(uVar2,0);
          return uVar2;
        }
        goto LAB_01983a54;
      }
LAB_01983980:
      uVar2 = Interop__GetIOException(param_1);
      if ((param_2 == 0) || (*(int *)(param_2 + 0x10) == 0)) {
        uVar4 = thunk_FUN_00e11c14(*(undefined8 *)
                                    PTR_System_UnauthorizedAccessException_TypeInfo_01fd21a8);
        uVar3 = *(undefined8 *)PTR_StringLiteral_1524_01fd2848;
      }
      else {
        uVar3 = SR__Format(*(undefined8 *)PTR_StringLiteral_1523_01fd2868,param_2);
        uVar4 = thunk_FUN_00e11c14(*(undefined8 *)
                                    PTR_System_UnauthorizedAccessException_TypeInfo_01fd21a8);
      }
      System_UnauthorizedAccessException___ctor(uVar4,uVar3,uVar2,0);
      return uVar4;
    }
    if (iVar6 == 0x10002) goto LAB_01983980;
    if (iVar6 != 0x10006) goto LAB_01983a54;
    if ((param_2 == 0) ||
       (puVar5 = (undefined8 *)PTR_StringLiteral_5455_01fd2830, *(int *)(param_2 + 0x10) == 0)) {
      uVar1 = Interop_ErrorInfo__get_RawErrno(&local_28);
      uVar3 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_IO_IOException_TypeInfo_01fbf720);
      uVar2 = *(undefined8 *)PTR_StringLiteral_5456_01fd2838;
      goto LAB_01983ae0;
    }
  }
  else {
    if (0x10016 < iVar6) {
      if (iVar6 == 0x10025) {
        if ((param_2 == 0) || (*(int *)(param_2 + 0x10) == 0)) {
          uVar3 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_System_IO_PathTooLongException_TypeInfo_01fd2820);
          uVar2 = *(undefined8 *)PTR_StringLiteral_5482_01fd2858;
        }
        else {
          uVar2 = SR__Format(*(undefined8 *)PTR_StringLiteral_5452_01fd2870,param_2);
          uVar3 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_System_IO_PathTooLongException_TypeInfo_01fd2820);
        }
        System_IO_PathTooLongException___ctor(uVar3,uVar2,0);
        return uVar3;
      }
      if (iVar6 == 0x10042) goto LAB_01983980;
      if (iVar6 == 0x1002d) {
        if ((param_2 == 0) || (*(int *)(param_2 + 0x10) == 0)) {
          if ((param_3 & 1) == 0) {
            uVar2 = thunk_FUN_00e11c14(*(undefined8 *)
                                        PTR_System_IO_FileNotFoundException_TypeInfo_01fd2818);
            System_IO_FileNotFoundException___ctor
                      (uVar2,*(undefined8 *)PTR_StringLiteral_5836_01fd2850,0);
            return uVar2;
          }
          uVar3 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_System_IO_DirectoryNotFoundException_TypeInfo_01fd2810);
          uVar2 = *(undefined8 *)PTR_StringLiteral_2605_01fd2840;
        }
        else {
          if ((param_3 & 1) == 0) {
            uVar2 = SR__Format(*(undefined8 *)PTR_StringLiteral_2608_01fd2828,param_2);
            uVar3 = thunk_FUN_00e11c14(*(undefined8 *)
                                        PTR_System_IO_FileNotFoundException_TypeInfo_01fd2818);
            System_IO_FileNotFoundException___ctor(uVar3,uVar2,param_2,0);
            return uVar3;
          }
          uVar2 = SR__Format(*(undefined8 *)PTR_StringLiteral_2604_01fd2878,param_2);
          uVar3 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_System_IO_DirectoryNotFoundException_TypeInfo_01fd2810);
        }
        System_IO_DirectoryNotFoundException___ctor(uVar3,uVar2,0);
        return uVar3;
      }
LAB_01983a54:
      uVar2 = Interop__GetIOException(param_1);
      return uVar2;
    }
    if (iVar6 != 0x10014) {
      if (iVar6 == 0x10016) {
        uVar2 = thunk_FUN_00e11c14(*(undefined8 *)
                                    PTR_System_ArgumentOutOfRangeException_TypeInfo_01fc5598);
        System_ArgumentOutOfRangeException___ctor
                  (uVar2,*(undefined8 *)PTR_StringLiteral_9533_01fc5f78,
                   *(undefined8 *)PTR_StringLiteral_5124_01fd2860,0);
        return uVar2;
      }
      goto LAB_01983a54;
    }
    if ((param_2 == 0) ||
       (puVar5 = (undefined8 *)PTR_StringLiteral_5407_01fd2880, *(int *)(param_2 + 0x10) == 0))
    goto LAB_01983a54;
  }
  uVar2 = SR__Format(*puVar5,param_2);
  uVar1 = Interop_ErrorInfo__get_RawErrno(&local_28);
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_IO_IOException_TypeInfo_01fbf720);
LAB_01983ae0:
  System_IO_IOException___ctor(uVar3,uVar2,uVar1,0);
  return uVar3;
}



// ==========================================================================================
// Function: Interop__CheckIo
// Address: 01983bc8
// ==========================================================================================

long Interop__CheckIo(long param_1,undefined8 param_2,uint param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  long lStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  if ((DAT_021015c8 & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015c8 = 1;
  }
  if (-1 < param_1) {
    return param_1;
  }
  FUN_00c81998(*(undefined8 *)PTR_Interop_Sys_TypeInfo_01fc6908);
  uVar3 = Interop_Sys__GetLastErrorInfo();
  Method_Interop_ThrowExceptionForIoErrno(uVar3,param_2,param_3 & 1,param_4);
  puVar1 = PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58;
  uStack_40 = param_2;
  uStack_38 = param_4;
  if ((DAT_021015d0 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58);
    DAT_021015d0 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Runtime_InteropServices_Marshal__GetLastWin32Error(0);
  lStack_48 = 0;
  Interop_ErrorInfo___ctor(&lStack_48,uVar2);
  return lStack_48;
}



// ==========================================================================================
// Function: Interop_Sys__GetLastErrorInfo
// Address: 01983c40
// ==========================================================================================

undefined8 Interop_Sys__GetLastErrorInfo(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined8 local_18;
  
  puVar1 = PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58;
  if ((DAT_021015d0 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58);
    DAT_021015d0 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Runtime_InteropServices_Marshal__GetLastWin32Error(0);
  local_18 = 0;
  Interop_ErrorInfo___ctor(&local_18,uVar2);
  return local_18;
}



// ==========================================================================================
// Function: Interop__CheckIo
// Address: 01983ca8
// ==========================================================================================

int Interop__CheckIo(int param_1,undefined8 param_2,uint param_3)

{
  Interop__CheckIo((long)param_1,param_2,param_3 & 1);
  return param_1;
}



// ==========================================================================================
// Function: Interop__GetIOException
// Address: 01983d84
// ==========================================================================================

undefined8 Interop__GetIOException(undefined8 param_1)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 local_28;
  
  puVar1 = PTR_System_IO_IOException_TypeInfo_01fbf720;
  local_28 = param_1;
  if ((DAT_021015ca & 1) == 0) {
    FUN_00db0bbc(PTR_System_IO_IOException_TypeInfo_01fbf720);
    DAT_021015ca = 1;
  }
  uVar3 = Interop_ErrorInfo__GetErrorMessage(&local_28);
  uVar2 = Interop_ErrorInfo__get_RawErrno(&local_28);
  uVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_IO_IOException___ctor(uVar4,uVar3,uVar2,0);
  return uVar4;
}



// ==========================================================================================
// Function: Interop_ErrorInfo__get_RawErrno
// Address: 01983e08
// ==========================================================================================

void Interop_ErrorInfo__get_RawErrno(undefined4 *param_1)

{
  undefined4 uVar1;
  
  if ((DAT_021015cd & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015cd = 1;
  }
  if (param_1[1] == -1) {
    uVar1 = *param_1;
    if (*(int *)(*(long *)PTR_Interop_Sys_TypeInfo_01fc6908 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar1 = SystemNative_ConvertErrorPalToPlatform(uVar1);
    param_1[1] = uVar1;
  }
  return;
}



// ==========================================================================================
// Function: Interop_ErrorInfo__GetErrorMessage
// Address: 01983e74
// ==========================================================================================

void Interop_ErrorInfo__GetErrorMessage(undefined8 param_1)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  puVar1 = PTR_Interop_Sys_TypeInfo_01fc6908;
  if ((DAT_021015ce & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015ce = 1;
  }
  uVar2 = Interop_ErrorInfo__get_RawErrno(param_1);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  Interop_Sys__StrError(uVar2);
  return;
}



// ==========================================================================================
// Function: Interop__GetRandomBytes
// Address: 01983ed8
// ==========================================================================================

void Interop__GetRandomBytes(undefined8 param_1,undefined4 param_2)

{
  undefined *puVar1;
  
  puVar1 = PTR_Interop_Sys_TypeInfo_01fc6908;
  if ((DAT_021015cb & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015cb = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  SystemNative_GetNonCryptographicallySecureRandomBytes(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: Interop_Sys__GetNonCryptographicallySecureRandomBytes
// Address: 01983f3c
// ==========================================================================================

void Interop_Sys__GetNonCryptographicallySecureRandomBytes(void)

{
  (*(code *)PTR_SystemNative_GetNonCryptographicallySecureRandomBytes_01ff5b18)();
  return;
}



// ==========================================================================================
// Function: Interop_ErrorInfo___ctor
// Address: 01983f40
// ==========================================================================================

void Interop_ErrorInfo___ctor(undefined4 *param_1,undefined4 param_2)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  puVar1 = PTR_Interop_Sys_TypeInfo_01fc6908;
  if ((DAT_021015cc & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015cc = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = SystemNative_ConvertErrorPlatformToPal(param_2);
  *param_1 = uVar2;
  param_1[1] = param_2;
  return;
}



// ==========================================================================================
// Function: Interop_Sys__ConvertErrorPlatformToPal
// Address: 01983fa8
// ==========================================================================================

void Interop_Sys__ConvertErrorPlatformToPal(void)

{
  (*(code *)PTR_SystemNative_ConvertErrorPlatformToPal_01ff5b20)();
  return;
}



// ==========================================================================================
// Function: Interop_ErrorInfo___ctor
// Address: 01983fac
// ==========================================================================================

void Interop_ErrorInfo___ctor(undefined4 *param_1,undefined4 param_2)

{
  *param_1 = param_2;
  param_1[1] = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: Interop_ErrorInfo__get_Error
// Address: 01983fb8
// ==========================================================================================

undefined4 Interop_ErrorInfo__get_Error(undefined4 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: Interop_Sys__ConvertErrorPalToPlatform
// Address: 01983fc0
// ==========================================================================================

void Interop_Sys__ConvertErrorPalToPlatform(void)

{
  (*(code *)PTR_SystemNative_ConvertErrorPalToPlatform_01ff5b10)();
  return;
}



// ==========================================================================================
// Function: Interop_Sys__StrError
// Address: 01983fc4
// ==========================================================================================

void Interop_Sys__StrError(undefined4 param_1)

{
  undefined *puVar1;
  long lVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined auStack_450 [1032];
  long local_48;
  
  puVar1 = PTR_Interop_Sys_TypeInfo_01fc6908;
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  if ((DAT_021015d1 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58);
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015d1 = 1;
  }
  puVar3 = PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58;
  memset(auStack_450,0,0x400);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar4 = (undefined *)SystemNative_StrErrorR(param_1,auStack_450,0x400);
  puVar1 = auStack_450;
  if (puVar4 != (undefined *)0x0) {
    puVar1 = puVar4;
  }
  uVar5 = System_IntPtr__op_Explicit(puVar1,0);
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar3);
  }
  System_Runtime_InteropServices_Marshal__PtrToStringAnsi(uVar5,0);
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: Interop_ErrorInfo__ToString
// Address: 019840c0
// ==========================================================================================

void Interop_ErrorInfo__ToString(undefined4 *param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined4 local_78;
  undefined4 local_74;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  puVar3 = PTR_StringLiteral_4823_01fd2890;
  puVar2 = PTR_Interop_Error_TypeInfo_01fd2888;
  puVar1 = PTR_int_TypeInfo_01fc0108;
  if ((DAT_021015cf & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Error_TypeInfo_01fd2888);
    FUN_00db0bbc(PTR_int_TypeInfo_01fc0108);
    FUN_00db0bbc(PTR_StringLiteral_4823_01fd2890);
    DAT_021015cf = 1;
  }
  local_74 = Interop_ErrorInfo__get_RawErrno(param_1);
  uVar4 = thunk_FUN_00e11868(*(undefined8 *)puVar1,&local_74);
  local_78 = *param_1;
  uVar5 = thunk_FUN_00e11868(*(undefined8 *)puVar2,&local_78);
  uVar6 = Interop_ErrorInfo__GetErrorMessage(param_1);
  uVar7 = *(undefined8 *)puVar3;
  uStack_48 = 0;
  local_50 = 0;
  uStack_38 = 0;
  uStack_40 = 0;
  System_ParamsArray___ctor(&local_50,uVar4,uVar5,uVar6,0);
  uStack_68 = uStack_48;
  local_70 = local_50;
  uStack_58 = uStack_38;
  uStack_60 = uStack_40;
  Method_System_String_FormatHelper(0,uVar7,&local_70);
  return;
}



// ==========================================================================================
// Function: Interop_Sys__StrErrorR
// Address: 019841f8
// ==========================================================================================

void Interop_Sys__StrErrorR(void)

{
  (*(code *)PTR_SystemNative_StrErrorR_01ff5b28)();
  return;
}



// ==========================================================================================
// Function: Interop_Sys__OpenDir
// Address: 019841fc
// ==========================================================================================

undefined8 Interop_Sys__OpenDir(void)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = thunk_FUN_00e12178();
  uVar2 = SystemNative_OpenDir();
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar1);
  return uVar2;
}



// ==========================================================================================
// Function: Interop_Sys__GetReadDirRBufferSize
// Address: 01984230
// ==========================================================================================

void Interop_Sys__GetReadDirRBufferSize(void)

{
  (*(code *)PTR_SystemNative_GetReadDirRBufferSize_01ff5b38)();
  return;
}



// ==========================================================================================
// Function: Interop_Sys__ReadDirR
// Address: 01984234
// ==========================================================================================

void Interop_Sys__ReadDirR(void)

{
  (*(code *)PTR_SystemNative_ReadDirR_01ff5b40)();
  return;
}



// ==========================================================================================
// Function: Interop_Sys__CloseDir
// Address: 01984238
// ==========================================================================================

undefined4 Interop_Sys__CloseDir(void)

{
  undefined4 uVar1;
  
  uVar1 = SystemNative_CloseDir();
  thunk_FUN_00dd09c8();
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__ReadLink
// Address: 01984254
// ==========================================================================================

undefined4 Interop_Sys__ReadLink(undefined8 param_1,long param_2,undefined4 param_3)

{
  long lVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  
  uVar3 = thunk_FUN_00e12178();
  lVar1 = 0;
  if (param_2 != 0) {
    lVar1 = param_2 + 0x20;
  }
  uVar2 = SystemNative_ReadLink(uVar3,lVar1,param_3);
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar3);
  return uVar2;
}



// ==========================================================================================
// Function: Interop_Sys__ReadLink
// Address: 019842a0
// ==========================================================================================

undefined8 Interop_Sys__ReadLink(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  int iVar8;
  long lVar9;
  undefined8 local_58;
  long *local_50;
  long local_48;
  
  if ((DAT_021015d2 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Buffers_ArrayPool_byte__get_Shared_01fc68e0);
    FUN_00db0bbc(PTR_System_Buffers_ArrayPool_byte__TypeInfo_01fc68f8);
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015d2 = 1;
  }
  puVar3 = PTR_Interop_Sys_TypeInfo_01fc6908;
  puVar2 = PTR_System_Buffers_ArrayPool_byte__TypeInfo_01fc68f8;
  puVar1 = PTR_Method_System_Buffers_ArrayPool_byte__get_Shared_01fc68e0;
  iVar8 = 0x100;
  local_48 = 0;
  while( true ) {
    if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar9 = *(long *)puVar1;
    lVar5 = *(long *)(lVar9 + 0x20);
    if ((*(byte *)(lVar5 + 0x135) & 1) == 0) {
      lVar5 = FUN_00e0dbd0();
    }
    lVar5 = *(long *)(*(long *)(lVar5 + 0xc0) + 8);
    if ((*(byte *)(lVar5 + 0x135) & 1) == 0) {
      lVar5 = FUN_00e0dbd0();
    }
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar5 = *(long *)(lVar9 + 0x20);
    if ((*(byte *)(lVar5 + 0x135) & 1) == 0) {
      lVar5 = FUN_00e0dbd0();
    }
    lVar5 = *(long *)(*(long *)(lVar5 + 0xc0) + 8);
    if ((*(byte *)(lVar5 + 0x135) & 1) == 0) {
      lVar5 = FUN_00e0dbd0();
    }
    plVar6 = **(long ***)(lVar5 + 0xb8);
    if (plVar6 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar5 = (**(code **)(*plVar6 + 0x178))(plVar6,iVar8,*(undefined8 *)(*plVar6 + 0x180));
    local_58 = 0;
    local_50 = &local_48;
    local_48 = lVar5;
    if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01984410 to 01984413 has its CatchHandler @ 01984438 */
      FUN_00db0de4();
    }
    if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
                    /* try { // try from 019843b4 to 019843b7 has its CatchHandler @ 01984438 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 019843bc to 019843c7 has its CatchHandler @ 01984434 */
    iVar4 = Interop_Sys__ReadLink(param_1,lVar5,*(undefined4 *)(lVar5 + 0x18));
    if (iVar4 < 0) break;
    if (local_48 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01984418 to 0198441b has its CatchHandler @ 01984430 */
      FUN_00db0de4();
    }
    if (iVar4 < *(int *)(local_48 + 0x18)) {
                    /* try { // try from 019843e4 to 019843eb has its CatchHandler @ 0198442c */
      plVar6 = (long *)System_Text_Encoding__get_UTF8(0);
      if (plVar6 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01984420 to 01984423 has its CatchHandler @ 01984428 */
        FUN_00db0de4();
      }
                    /* try { // try from 01984400 to 0198440b has its CatchHandler @ 0198443c */
      uVar7 = (**(code **)(*plVar6 + 0x378))
                        (plVar6,local_48,0,iVar4,*(undefined8 *)(*plVar6 + 0x380));
LAB_01984470:
      FUN_00d73b00(&local_58);
      return uVar7;
    }
    FUN_00d73b00(&local_58);
    iVar8 = iVar8 << 1;
  }
  uVar7 = 0;
  goto LAB_01984470;
}



// ==========================================================================================
// Function: Interop_Sys__Stat
// Address: 019844b8
// ==========================================================================================

undefined4 Interop_Sys__Stat(undefined8 param_1,undefined8 param_2)

{
  undefined4 uVar1;
  undefined8 uVar2;
  
  uVar2 = thunk_FUN_00e12178();
  uVar1 = SystemNative_Stat2(uVar2,param_2);
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__LStat
// Address: 019844f4
// ==========================================================================================

undefined4 Interop_Sys__LStat(undefined8 param_1,undefined8 param_2)

{
  undefined4 uVar1;
  undefined8 uVar2;
  
  uVar2 = thunk_FUN_00e12178();
  uVar1 = SystemNative_LStat2(uVar2,param_2);
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__Symlink
// Address: 01984530
// ==========================================================================================

int Interop_Sys__Symlink(undefined8 param_1,undefined8 param_2)

{
  int iVar1;
  char *__from;
  char *__to;
  
  __from = (char *)thunk_FUN_00e12178();
  __to = (char *)thunk_FUN_00e12178(param_2);
  iVar1 = SystemNative_Symlink(__from,__to);
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(__from);
  thunk_FUN_00e1216c(__to);
  return iVar1;
}



// ==========================================================================================
// Function: Interop_Sys__CopyFile
// Address: 01984584
// ==========================================================================================

undefined4 Interop_Sys__CopyFile(long param_1,long param_2)

{
  undefined4 uVar1;
  char *pcVar2;
  undefined8 uVar3;
  char local_28 [4];
  char local_24 [4];
  
  if (param_1 == 0) {
    pcVar2 = "source";
  }
  else {
    local_24[0] = '\0';
    Method_System_Runtime_InteropServices_SafeHandle_DangerousAddRef(param_1,local_24,0);
    if (param_2 != 0) {
      uVar3 = *(undefined8 *)(param_1 + 0x10);
      local_28[0] = '\0';
      Method_System_Runtime_InteropServices_SafeHandle_DangerousAddRef(param_2,local_28,0);
      uVar1 = SystemNative_CopyFile(uVar3,*(undefined8 *)(param_2 + 0x10));
      thunk_FUN_00dd09c8();
      if (local_24[0] != '\0') {
        System_Runtime_InteropServices_SafeHandle__DangerousRelease(param_1,0);
      }
      if (local_28[0] != '\0') {
        System_Runtime_InteropServices_SafeHandle__DangerousRelease(param_2,0);
      }
      return uVar1;
    }
    pcVar2 = "destination";
  }
  uVar3 = thunk_FUN_00e295e0(pcVar2);
                    /* WARNING: Subroutine does not return */
  FUN_00db0cb0(uVar3,0);
}



// ==========================================================================================
// Function: Interop_Sys__GetEGid
// Address: 01984638
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__gid_t Interop_Sys__GetEGid(void)

{
  __gid_t _Var1;
  
  _Var1 = (*(code *)PTR_SystemNative_GetEGid_01ff5b78)();
  return _Var1;
}



// ==========================================================================================
// Function: Interop_Sys__GetEUid
// Address: 0198463c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__uid_t Interop_Sys__GetEUid(void)

{
  __uid_t _Var1;
  
  _Var1 = (*(code *)PTR_SystemNative_GetEUid_01ff5b80)();
  return _Var1;
}



// ==========================================================================================
// Function: Interop_Sys__LChflagsCanSetHiddenFlag
// Address: 01984640
// ==========================================================================================

void Interop_Sys__LChflagsCanSetHiddenFlag(void)

{
  (*(code *)PTR_SystemNative_LChflagsCanSetHiddenFlag_01ff5b88)();
  return;
}



// ==========================================================================================
// Function: Interop_Sys__MkDir
// Address: 01984644
// ==========================================================================================

undefined4 Interop_Sys__MkDir(undefined8 param_1,undefined4 param_2)

{
  undefined4 uVar1;
  undefined8 uVar2;
  
  uVar2 = thunk_FUN_00e12178();
  uVar1 = SystemNative_MkDir(uVar2,param_2);
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__RmDir
// Address: 01984680
// ==========================================================================================

undefined4 Interop_Sys__RmDir(void)

{
  undefined4 uVar1;
  undefined8 uVar2;
  
  uVar2 = thunk_FUN_00e12178();
  uVar1 = SystemNative_RmDir();
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__Stat
// Address: 019846b4
// ==========================================================================================

undefined4 Interop_Sys__Stat(void)

{
  undefined4 uVar1;
  
  uVar1 = SystemNative_Stat2();
  thunk_FUN_00dd09c8();
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__Stat
// Address: 019846d0
// ==========================================================================================

undefined4 Interop_Sys__Stat(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  undefined auVar6 [16];
  undefined auStack_170 [256];
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  puVar3 = PTR_Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte_01fd2898;
  puVar2 = PTR_Interop_Sys_TypeInfo_01fc6908;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if ((DAT_021015d3 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte_01fd2898)
    ;
    FUN_00db0bbc(PTR_Method_System_Span_byte___ctor_01fd28a0);
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015d3 = 1;
  }
  local_70 = 0;
  uStack_68 = 0;
  local_60 = 0;
  memset(auStack_170,0,0x100);
  System_Text_ValueUtf8Converter___ctor(&local_70,auStack_170,0x100,0);
  auVar6 = System_Text_ValueUtf8Converter__ConvertAndTerminateString(&local_70,param_1,param_2,0);
  uVar5 = Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte
                    (auVar6._0_8_,auVar6._8_8_,*(undefined8 *)puVar3);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  uVar4 = SystemNative_Stat2(uVar5,param_3);
  thunk_FUN_00dd09c8();
  System_Text_ValueUtf8Converter__Dispose(&local_70,0);
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: Interop_Sys__LStat
// Address: 01984808
// ==========================================================================================

undefined4 Interop_Sys__LStat(void)

{
  undefined4 uVar1;
  
  uVar1 = SystemNative_LStat2();
  thunk_FUN_00dd09c8();
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__LStat
// Address: 01984824
// ==========================================================================================

undefined4 Interop_Sys__LStat(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  undefined auVar6 [16];
  undefined auStack_170 [256];
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  puVar3 = PTR_Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte_01fd2898;
  puVar2 = PTR_Interop_Sys_TypeInfo_01fc6908;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if ((DAT_021015d4 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte_01fd2898)
    ;
    FUN_00db0bbc(PTR_Method_System_Span_byte___ctor_01fd28a0);
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015d4 = 1;
  }
  local_70 = 0;
  uStack_68 = 0;
  local_60 = 0;
  memset(auStack_170,0,0x100);
  System_Text_ValueUtf8Converter___ctor(&local_70,auStack_170,0x100,0);
  auVar6 = System_Text_ValueUtf8Converter__ConvertAndTerminateString(&local_70,param_1,param_2,0);
  uVar5 = Method_System_Runtime_InteropServices_MemoryMarshal_GetReference_byte
                    (auVar6._0_8_,auVar6._8_8_,*(undefined8 *)puVar3);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  uVar4 = SystemNative_LStat2(uVar5,param_3);
  thunk_FUN_00dd09c8();
  System_Text_ValueUtf8Converter__Dispose(&local_70,0);
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: Interop_Sys__Unlink
// Address: 0198495c
// ==========================================================================================

undefined4 Interop_Sys__Unlink(void)

{
  undefined4 uVar1;
  undefined8 uVar2;
  
  uVar2 = thunk_FUN_00e12178();
  uVar1 = SystemNative_Unlink();
  thunk_FUN_00dd09c8();
  thunk_FUN_00e1216c(uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: Interop_Sys__DoubleToString
// Address: 01984990
// ==========================================================================================

int Interop_Sys__DoubleToString(char *param_1,char *param_2,int param_3)

{
  int iVar1;
  
  iVar1 = snprintf(param_2,(long)param_3,param_1);
  return iVar1;
}



// ==========================================================================================
// Function: Interop_Sys___cctor
// Address: 01984994
// ==========================================================================================

void Interop_Sys___cctor(void)

{
  undefined *puVar1;
  int iVar2;
  
  puVar1 = PTR_Interop_Sys_TypeInfo_01fc6908;
  if ((DAT_021015d5 & 1) == 0) {
    FUN_00db0bbc(PTR_Interop_Sys_TypeInfo_01fc6908);
    DAT_021015d5 = 1;
  }
  iVar2 = SystemNative_LChflagsCanSetHiddenFlag();
  *(bool *)*(undefined8 *)(*(long *)puVar1 + 0xb8) = iVar2 != 0;
  return;
}



// ==========================================================================================
// Function: Interop_Sys_DirectoryEntry__GetName
// Address: 019849e8
// ==========================================================================================

void Interop_Sys_DirectoryEntry__GetName(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  uint uVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  long lVar6;
  
  if ((DAT_021015d6 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_MemoryExtensions_IndexOf_byte_01fd28a8);
    FUN_00db0bbc(PTR_Method_System_ReadOnlySpan_byte___ctor_01fd28b0);
    FUN_00db0bbc(PTR_Method_System_Span_char__Slice_01fd28b8);
    FUN_00db0bbc(PTR_Method_System_Span_char__op_Implicit_01fd28c0);
    DAT_021015d6 = 1;
  }
  iVar3 = *(int *)(param_1 + 1);
  uVar5 = *param_1;
  if (iVar3 == -1) {
    iVar3 = FUN_0199a998(uVar5,0x100,0,
                         *(undefined8 *)PTR_Method_System_MemoryExtensions_IndexOf_byte_01fd28a8);
  }
  if (iVar3 < 0) {
    Method_System_ThrowHelper_ThrowArgumentOutOfRangeException(0);
  }
  plVar4 = (long *)System_Text_Encoding__get_UTF8(0);
  puVar1 = PTR_Method_System_Span_char__Slice_01fd28b8;
  if (plVar4 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar2 = (**(code **)(*plVar4 + 0x308))
                    (plVar4,uVar5,iVar3,param_2,param_3,*(undefined8 *)(*plVar4 + 0x310));
  lVar6 = *(long *)puVar1;
  if ((uint)param_3 < uVar2) {
    Method_System_ThrowHelper_ThrowArgumentOutOfRangeException(0);
  }
  puVar1 = PTR_Method_System_Span_char__op_Implicit_01fd28c0;
  if ((*(byte *)(*(long *)(lVar6 + 0x20) + 0x135) & 1) == 0) {
    FUN_00e0dbd0();
  }
  Method_System_Span_char__op_Implicit(param_2,uVar2,*(undefined8 *)puVar1);
  return;
}



// ==========================================================================================
