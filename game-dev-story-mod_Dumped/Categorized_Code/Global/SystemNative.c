// Function: SystemNative_ConvertErrorPlatformToPal
// Address: 00e2e614
// ==========================================================================================

undefined4 SystemNative_ConvertErrorPlatformToPal(uint param_1)

{
  if (param_1 < 0x84) {
    return *(undefined4 *)(&DAT_008162e0 + (long)(int)param_1 * 4);
  }
  return 0x1ffff;
}



// ==========================================================================================
// Function: SystemNative_StrErrorR
// Address: 00e2e634
// ==========================================================================================

char * SystemNative_StrErrorR(int param_1,char *param_2,uint param_3)

{
  char *pcVar1;
  char *pcVar2;
  
  if (-1 < (int)param_3) {
    pcVar2 = strerror_r(param_1,param_2,(ulong)param_3);
    pcVar1 = (char *)0x0;
    if ((int)pcVar2 != 0x22) {
      pcVar1 = param_2;
    }
    return pcVar1;
  }
  return (char *)0x0;
}



// ==========================================================================================
// Function: SystemNative_ConvertErrorPalToPlatform
// Address: 00e2e660
// ==========================================================================================

undefined8 SystemNative_ConvertErrorPalToPlatform(undefined8 param_1)

{
  switch((int)param_1) {
  case 0x10001:
    return 7;
  case 0x10002:
    return 0xd;
  case 0x10003:
    return 0x62;
  case 0x10004:
    return 99;
  case 0x10005:
    return 0x61;
  case 0x10006:
    return 0xb;
  case 0x10007:
    return 0x72;
  case 0x10008:
    return 9;
  case 0x10009:
    return 0x4a;
  case 0x1000a:
    return 0x10;
  case 0x1000b:
    return 0x7d;
  case 0x1000c:
    return 10;
  case 0x1000d:
    return 0x67;
  case 0x1000e:
    return 0x6f;
  case 0x1000f:
    return 0x68;
  case 0x10010:
    return 0x23;
  case 0x10011:
    return 0x59;
  case 0x10012:
    return 0x21;
  case 0x10013:
    return 0x7a;
  case 0x10014:
    return 0x11;
  case 0x10015:
    return 0xe;
  case 0x10016:
    return 0x1b;
  case 0x10017:
    return 0x71;
  case 0x10018:
    return 0x2b;
  case 0x10019:
    return 0x54;
  case 0x1001a:
    return 0x73;
  case 0x1001b:
    return 4;
  case 0x1001c:
    return 0x16;
  case 0x1001d:
    return 5;
  case 0x1001e:
    return 0x6a;
  case 0x1001f:
    return 0x15;
  case 0x10020:
    return 0x28;
  case 0x10021:
    return 0x18;
  case 0x10022:
    return 0x1f;
  case 0x10023:
    return 0x5a;
  case 0x10024:
    return 0x48;
  case 0x10025:
    return 0x24;
  case 0x10026:
    return 100;
  case 0x10027:
    return 0x66;
  case 0x10028:
    return 0x65;
  case 0x10029:
    return 0x17;
  case 0x1002a:
    return 0x69;
  case 0x1002b:
  case 0x10035:
  case 0x10036:
  case 0x1004c:
  case 0x10050:
  case 0x10051:
  case 0x10052:
  case 0x10053:
  case 0x10054:
  case 0x10055:
  case 0x10056:
  case 0x10057:
  case 0x10058:
  case 0x10059:
  case 0x1005a:
  case 0x1005b:
  case 0x1005c:
  case 0x1005d:
  case 0x1005f:
  case 0x10061:
  case 0x10062:
  case 0x10063:
  case 0x10064:
  case 0x10065:
  case 0x10066:
  case 0x10067:
  case 0x10068:
  case 0x10069:
  case 0x1006a:
  case 0x1006b:
  case 0x1006d:
  case 0x1006e:
  case 0x1006f:
    goto switchD_00e2e684_caseD_1002b;
  case 0x1002c:
    return 0x13;
  case 0x1002d:
    return 2;
  case 0x1002e:
    return 8;
  case 0x1002f:
    return 0x25;
  case 0x10030:
    return 0x43;
  case 0x10031:
    return 0xc;
  case 0x10032:
    return 0x2a;
  case 0x10033:
    return 0x5c;
  case 0x10034:
    return 0x1c;
  case 0x10037:
    return 0x26;
  case 0x10038:
    return 0x6b;
  case 0x10039:
    return 0x14;
  case 0x1003a:
    return 0x27;
  case 0x1003b:
    return 0x83;
  case 0x1003c:
    return 0x58;
  case 0x1003d:
    return 0x5f;
  case 0x1003e:
    return 0x19;
  case 0x1003f:
    return 6;
  case 0x10040:
    return 0x4b;
  case 0x10041:
    return 0x82;
  case 0x10042:
    return 1;
  case 0x10043:
    return 0x20;
  case 0x10044:
    return 0x47;
  case 0x10045:
    return 0x5d;
  case 0x10046:
    return 0x5b;
  case 0x10047:
    return 0x22;
  case 0x10048:
    return 0x1e;
  case 0x10049:
    return 0x1d;
  case 0x1004a:
    return 3;
  case 0x1004b:
    return 0x74;
  case 0x1004d:
    return 0x6e;
  case 0x1004e:
    return 0x1a;
  case 0x1004f:
    return 0x12;
  case 0x1005e:
    return 0x5e;
  case 0x10060:
    return 0x60;
  case 0x1006c:
    return 0x6c;
  case 0x10070:
    return 0x70;
  case 0x10071:
    return 0x3d;
  default:
    if ((int)param_1 == 0) {
      return param_1;
    }
switchD_00e2e684_caseD_1002b:
    return 0xffffffff;
  }
}



// ==========================================================================================
// Function: SystemNative_Stat2
// Address: 00e2e914
// ==========================================================================================

int SystemNative_Stat2(char *param_1,undefined4 *param_2)

{
  int iVar1;
  int *piVar2;
  __dev_t local_a0;
  __ino_t _Stack_98;
  __nlink_t local_90;
  undefined8 local_88;
  undefined8 local_80;
  __dev_t _Stack_78;
  __off_t local_70;
  __blksize_t _Stack_68;
  __blkcnt_t local_60;
  __time_t _Stack_58;
  long lStack_50;
  __time_t _Stack_48;
  long local_40;
  __time_t _Stack_38;
  long lStack_30;
  long lStack_28;
  
  _Stack_38 = 0;
  local_40 = 0;
  lStack_28 = 0;
  lStack_30 = 0;
  _Stack_58 = 0;
  local_60 = 0;
  _Stack_48 = 0;
  lStack_50 = 0;
  _Stack_78 = 0;
  local_80._0_4_ = 0;
  local_80._4_4_ = 0;
  _Stack_68 = 0;
  local_70 = 0;
  _Stack_98 = 0;
  local_a0 = 0;
  local_88._0_4_ = 0;
  local_88._4_4_ = 0;
  local_90 = 0;
  do {
    iVar1 = stat(param_1,(stat *)&local_a0);
    if (-1 < iVar1) {
      if (iVar1 != 0) {
        return iVar1;
      }
      *(__ino_t *)(param_2 + 0x18) = _Stack_98;
      *(__dev_t *)(param_2 + 0x16) = local_a0;
      *param_2 = 0;
      param_2[1] = (undefined4)local_90;
      *(undefined8 *)(param_2 + 2) = local_88;
      *(__off_t *)(param_2 + 4) = local_70;
      *(long *)(param_2 + 8) = lStack_50;
      *(__time_t *)(param_2 + 6) = _Stack_58;
      *(long *)(param_2 + 0xc) = local_40;
      *(__time_t *)(param_2 + 10) = _Stack_48;
      param_2[0x1a] = 0;
      *(undefined8 *)(param_2 + 0x12) = 0;
      *(undefined8 *)(param_2 + 0x14) = 0;
      *(long *)(param_2 + 0x10) = lStack_30;
      *(__time_t *)(param_2 + 0xe) = _Stack_38;
      return 0;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_LStat2
// Address: 00e2e9bc
// ==========================================================================================

void SystemNative_LStat2(char *param_1,undefined4 *param_2)

{
  int iVar1;
  __dev_t local_90;
  __ino_t _Stack_88;
  __nlink_t local_80;
  undefined8 local_78;
  undefined8 local_70;
  __dev_t _Stack_68;
  __off_t local_60;
  __blksize_t _Stack_58;
  __blkcnt_t local_50;
  __time_t _Stack_48;
  long lStack_40;
  __time_t _Stack_38;
  long local_30;
  __time_t _Stack_28;
  long lStack_20;
  long lStack_18;
  
  _Stack_28 = 0;
  local_30 = 0;
  lStack_18 = 0;
  lStack_20 = 0;
  _Stack_48 = 0;
  local_50 = 0;
  _Stack_38 = 0;
  lStack_40 = 0;
  _Stack_68 = 0;
  local_70._0_4_ = 0;
  local_70._4_4_ = 0;
  _Stack_58 = 0;
  local_60 = 0;
  _Stack_88 = 0;
  local_90 = 0;
  local_78._0_4_ = 0;
  local_78._4_4_ = 0;
  local_80 = 0;
  iVar1 = lstat(param_1,(stat *)&local_90);
  if (iVar1 == 0) {
    *(__ino_t *)(param_2 + 0x18) = _Stack_88;
    *(__dev_t *)(param_2 + 0x16) = local_90;
    *param_2 = 0;
    param_2[1] = (undefined4)local_80;
    *(undefined8 *)(param_2 + 2) = local_78;
    *(__off_t *)(param_2 + 4) = local_60;
    *(long *)(param_2 + 8) = lStack_40;
    *(__time_t *)(param_2 + 6) = _Stack_48;
    *(long *)(param_2 + 0xc) = local_30;
    *(__time_t *)(param_2 + 10) = _Stack_38;
    param_2[0x1a] = 0;
    *(undefined8 *)(param_2 + 0x12) = 0;
    *(undefined8 *)(param_2 + 0x14) = 0;
    *(long *)(param_2 + 0x10) = lStack_20;
    *(__time_t *)(param_2 + 0xe) = _Stack_28;
  }
  return;
}



// ==========================================================================================
// Function: SystemNative_Unlink
// Address: 00e2ea34
// ==========================================================================================

int SystemNative_Unlink(char *param_1)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = unlink(param_1);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_GetReadDirRBufferSize
// Address: 00e2ea70
// ==========================================================================================

undefined8 SystemNative_GetReadDirRBufferSize(void)

{
  return 0;
}



// ==========================================================================================
// Function: SystemNative_ReadDirR
// Address: 00e2ea78
// ==========================================================================================

int SystemNative_ReadDirR(DIR **param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4)

{
  char **ppcVar1;
  byte bVar2;
  int iVar3;
  int *piVar4;
  dirent *pdVar5;
  DIR *pDVar6;
  char *pcVar7;
  DIR *__nmemb;
  long lVar8;
  DIR *pDVar9;
  undefined8 uVar10;
  
  piVar4 = (int *)__errno();
  *piVar4 = 0;
  if (param_1[1] == (DIR *)0x0) {
    __nmemb = (DIR *)0xffffffffffffffff;
    do {
      pdVar5 = readdir(*param_1);
      __nmemb = __nmemb + 1;
    } while (pdVar5 != (dirent *)0x0);
    if (__nmemb != (DIR *)0x0) {
      pDVar6 = (DIR *)calloc((size_t)__nmemb,0x10);
      param_1[1] = pDVar6;
      param_1[2] = (DIR *)0x0;
      closedir(*param_1);
      pDVar6 = opendir((char *)param_1[4]);
      *param_1 = pDVar6;
      pdVar5 = readdir(pDVar6);
      if (pdVar5 == (dirent *)0x0) {
        pDVar6 = (DIR *)0x0;
      }
      else {
        lVar8 = 0;
        pDVar6 = (DIR *)0x0;
        do {
          pDVar9 = param_1[1];
          pcVar7 = strdup(pdVar5->d_name);
          ppcVar1 = (char **)(pDVar9 + lVar8);
          *ppcVar1 = pcVar7;
          bVar2 = pdVar5->d_type;
          pDVar6 = pDVar6 + 1;
          *(undefined4 *)(ppcVar1 + 1) = 0xffffffff;
          *(uint *)((long)ppcVar1 + 0xc) = (uint)bVar2;
          pdVar5 = readdir(*param_1);
          if (__nmemb <= pDVar6) break;
          lVar8 = lVar8 + 0x10;
        } while (pdVar5 != (dirent *)0x0);
      }
      qsort(param_1[1],(size_t)__nmemb,0x10,FUN_00e2ebb4);
      param_1[3] = pDVar6;
    }
  }
  if (param_1[2] < param_1[3]) {
    iVar3 = 0;
    uVar10 = *(undefined8 *)(param_1[1] + (long)param_1[2] * 0x10);
    param_4[1] = *(undefined8 *)((long)(param_1[1] + (long)param_1[2] * 0x10) + 8);
    *param_4 = uVar10;
    param_1[2] = param_1[2] + 1;
  }
  else {
    *param_4 = 0;
    param_4[1] = 0;
    iVar3 = *piVar4;
    if (iVar3 == 0) {
      iVar3 = -1;
    }
  }
  return iVar3;
}



// ==========================================================================================
// Function: SystemNative_OpenDir
// Address: 00e2ebe8
// ==========================================================================================

DIR ** SystemNative_OpenDir(char *param_1)

{
  DIR *pDVar1;
  DIR **ppDVar2;
  
  pDVar1 = opendir(param_1);
  if (pDVar1 == (DIR *)0x0) {
    ppDVar2 = (DIR **)0x0;
  }
  else {
    ppDVar2 = (DIR **)malloc(0x28);
    *ppDVar2 = pDVar1;
    ppDVar2[1] = (DIR *)0x0;
    ppDVar2[2] = (DIR *)0x0;
    ppDVar2[3] = (DIR *)0x0;
    pDVar1 = (DIR *)strdup(param_1);
    ppDVar2[4] = pDVar1;
  }
  return ppDVar2;
}



// ==========================================================================================
// Function: SystemNative_CloseDir
// Address: 00e2ec38
// ==========================================================================================

int SystemNative_CloseDir(DIR **param_1)

{
  DIR *pDVar1;
  int iVar2;
  void **__ptr;
  long lVar3;
  int iVar4;
  
  iVar2 = closedir(*param_1);
  __ptr = (void **)param_1[1];
  if (__ptr != (void **)0x0) {
    if (param_1[3] != (DIR *)0x0) {
      free(*__ptr);
      if ((DIR *)0x1 < param_1[3]) {
        lVar3 = 1;
        iVar4 = 2;
        do {
          free(*(void **)(param_1[1] + lVar3 * 0x10));
          pDVar1 = (DIR *)(long)iVar4;
          lVar3 = (long)iVar4;
          iVar4 = iVar4 + 1;
        } while (pDVar1 < param_1[3]);
      }
      __ptr = (void **)param_1[1];
    }
    free(__ptr);
  }
  param_1[1] = (DIR *)0x0;
  if (param_1[4] != (DIR *)0x0) {
    free(param_1[4]);
  }
  free(param_1);
  return iVar2;
}



// ==========================================================================================
// Function: SystemNative_MkDir
// Address: 00e2ecd8
// ==========================================================================================

int SystemNative_MkDir(char *param_1,__mode_t param_2)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = mkdir(param_1,param_2);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_ChMod
// Address: 00e2ed1c
// ==========================================================================================

int SystemNative_ChMod(char *param_1,__mode_t param_2)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = chmod(param_1,param_2);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_Link
// Address: 00e2ed60
// ==========================================================================================

int SystemNative_Link(char *param_1,char *param_2)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = link(param_1,param_2);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_Symlink
// Address: 00e2eda4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int SystemNative_Symlink(char *__from,char *__to)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_symlink_01ff6128)((int)__from);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_ReadLink
// Address: 00e2eda8
// ==========================================================================================

ssize_t SystemNative_ReadLink(char *param_1,char *param_2,uint param_3)

{
  ssize_t sVar1;
  undefined4 *puVar2;
  
  if ((int)param_3 < 1) {
    puVar2 = (undefined4 *)__errno();
    *puVar2 = 0x16;
    sVar1 = 0xffffffff;
  }
  else {
    sVar1 = readlink(param_1,param_2,(ulong)param_3);
  }
  return sVar1;
}



// ==========================================================================================
// Function: SystemNative_Rename
// Address: 00e2edd8
// ==========================================================================================

int SystemNative_Rename(char *param_1,char *param_2)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = rename(param_1,param_2);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_RmDir
// Address: 00e2ee1c
// ==========================================================================================

int SystemNative_RmDir(char *param_1)

{
  int iVar1;
  int *piVar2;
  
  do {
    iVar1 = rmdir(param_1);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_CopyFile
// Address: 00e2ee58
// ==========================================================================================

undefined8 SystemNative_CopyFile(uint *param_1,uint *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  ulong uVar4;
  int *piVar5;
  ssize_t sVar6;
  void *__buf;
  size_t sVar7;
  long lVar8;
  timespec local_f0;
  __time_t _Stack_e0;
  long lStack_d8;
  uint local_c0;
  ulong local_a0;
  __time_t local_88;
  long lStack_80;
  __time_t local_78;
  long lStack_70;
  
  uVar4 = FUN_00dadad0();
  if ((uVar4 & 1) != 0) {
    param_1 = (uint *)(ulong)*param_1;
  }
  uVar4 = FUN_00dadad0(param_2);
  if ((uVar4 & 1) != 0) {
    param_2 = (uint *)(ulong)*param_2;
  }
  while( true ) {
    iVar3 = (int)param_1;
    iVar1 = fstat(iVar3,(stat *)&stack0xffffffffffffff30);
    if (-1 < iVar1) break;
    piVar5 = (int *)__errno();
    if (*piVar5 != 4) {
      return 0xffffffff;
    }
  }
  if (iVar1 != 0) {
    return 0xffffffff;
  }
  do {
    iVar1 = (int)param_2;
    iVar2 = fchmod(iVar1,local_c0 & 0x1ff);
    uVar4 = local_a0;
    if (-1 < iVar2) break;
    piVar5 = (int *)__errno();
    uVar4 = local_a0;
  } while (*piVar5 == 4);
  do {
    if (uVar4 == 0) goto LAB_00e2ef34;
    sVar7 = uVar4;
    if (0x7ffffffffffffffe < uVar4) {
      sVar7 = 0x7fffffffffffffff;
    }
    sVar6 = sendfile(iVar1,iVar3,(off_t *)0x0,sVar7);
    if (sVar6 < 0) {
      piVar5 = (int *)__errno();
      if ((*piVar5 != 0x26) && (*piVar5 != 0x16)) {
        return 0xffffffff;
      }
      __buf = malloc(0x14000);
      if (__buf == (void *)0x0) {
        return 0xffffffff;
      }
      break;
    }
    uVar4 = uVar4 - sVar6;
  } while( true );
LAB_00e2ef98:
  sVar7 = read(iVar3,__buf,0x14000);
  if ((long)sVar7 < 0) goto code_r0x00e2efb4;
  goto LAB_00e2efc0;
code_r0x00e2efb4:
  if (*piVar5 != 4) {
LAB_00e2efc0:
    if (sVar7 == 0xffffffffffffffff) {
      iVar3 = *piVar5;
      free(__buf);
      *piVar5 = iVar3;
      return 0xffffffff;
    }
    if (sVar7 == 0) {
      free(__buf);
LAB_00e2ef34:
      local_f0.tv_nsec = lStack_80;
      local_f0.tv_sec = local_88;
      lStack_d8 = lStack_70;
      _Stack_e0 = local_78;
      do {
        iVar3 = futimens(iVar1,&local_f0);
        if (-1 < iVar3) {
          return 0;
        }
        piVar5 = (int *)__errno();
      } while (*piVar5 == 4);
      return 0;
    }
    if (0 < (long)sVar7) {
      lVar8 = 0;
      do {
        do {
          sVar6 = write(iVar1,(void *)((long)__buf + lVar8),sVar7);
          if (-1 < sVar6) goto LAB_00e2f004;
          iVar2 = *piVar5;
        } while (iVar2 == 4);
        if (sVar6 == -1) {
          free(__buf);
          *piVar5 = iVar2;
          return 0xffffffff;
        }
LAB_00e2f004:
        sVar7 = sVar7 - sVar6;
        lVar8 = sVar6 + lVar8;
      } while (0 < (long)sVar7);
    }
  }
  goto LAB_00e2ef98;
}



// ==========================================================================================
// Function: SystemNative_LChflags
// Address: 00e2f048
// ==========================================================================================

undefined8 SystemNative_LChflags(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: SystemNative_LChflagsCanSetHiddenFlag
// Address: 00e2f050
// ==========================================================================================

undefined8 SystemNative_LChflagsCanSetHiddenFlag(void)

{
  return 0;
}



// ==========================================================================================
// Function: SystemNative_GetDomainSocketSizes
// Address: 00e2f058
// ==========================================================================================

void SystemNative_GetDomainSocketSizes(undefined4 *param_1,undefined4 *param_2,undefined4 *param_3)

{
  *param_1 = 2;
  *param_2 = 0x6c;
  *param_3 = 0x6e;
  return;
}



// ==========================================================================================
// Function: SystemNative_GetNonCryptographicallySecureRandomBytes
// Address: 00e2f074
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00e2f0dc) */

void SystemNative_GetNonCryptographicallySecureRandomBytes(long param_1,uint param_2)

{
  char cVar1;
  bool bVar2;
  int __fd;
  ssize_t sVar3;
  int *piVar4;
  time_t __seedval;
  long lVar5;
  uint uVar6;
  ulong uVar7;
  
  if ((DAT_02108a80 & 1) != 0) goto LAB_00e2f0fc;
  if (DAT_020ff0d0 == -1) {
    do {
      __fd = open("/dev/urandom",0,0x80000);
      if (__fd != -1) goto LAB_00e2f1b4;
      piVar4 = (int *)__errno();
    } while (*piVar4 == 4);
    if (*piVar4 == 2) {
      DAT_02108a80 = 1;
    }
  }
  goto LAB_00e2f0a4;
  while( true ) {
    cVar1 = '\x01';
    bVar2 = (bool)ExclusiveMonitorPass(0x20ff0d0,0x10);
    if (bVar2) {
      cVar1 = ExclusiveMonitorsStatus();
      DAT_020ff0d0 = __fd;
    }
    if (cVar1 == '\0') break;
LAB_00e2f1b4:
    if (DAT_020ff0d0 != -1) {
      ClearExclusiveLocal();
      close(__fd);
      break;
    }
  }
LAB_00e2f0a4:
  if (DAT_020ff0d0 != -1) {
    uVar6 = 0;
    do {
      sVar3 = read(DAT_020ff0d0,(void *)(param_1 + (int)uVar6),(long)(int)(param_2 - uVar6));
      if (sVar3 == -1) {
        piVar4 = (int *)__errno();
        if (*piVar4 != 4) break;
      }
      else {
        uVar6 = uVar6 + (int)sVar3;
      }
    } while (uVar6 != param_2);
  }
LAB_00e2f0fc:
  if ((DAT_02108a81 & 1) == 0) {
    __seedval = time((time_t *)0x0);
    srand48(__seedval);
    DAT_02108a81 = 1;
  }
  if (0 < (int)param_2) {
    uVar7 = 0;
    lVar5 = 0;
    do {
      if ((uVar7 & 3) == 0) {
        lVar5 = lrand48();
      }
      *(byte *)(param_1 + uVar7) = *(byte *)(param_1 + uVar7) ^ (byte)lVar5;
      uVar7 = uVar7 + 1;
      lVar5 = lVar5 >> 8;
    } while (param_2 != uVar7);
  }
  return;
}



// ==========================================================================================
// Function: SystemNative_UTimes
// Address: 00e2f1d8
// ==========================================================================================

int SystemNative_UTimes(char *param_1,__time_t *param_2)

{
  int iVar1;
  int *piVar2;
  timeval local_40;
  __time_t _Stack_30;
  __time_t _Stack_28;
  
  local_40.tv_usec = param_2[1];
  local_40.tv_sec = *param_2;
  _Stack_28 = param_2[3];
  _Stack_30 = param_2[2];
  do {
    iVar1 = utimes(param_1,&local_40);
    if (-1 < iVar1) {
      return iVar1;
    }
    piVar2 = (int *)__errno();
  } while (*piVar2 == 4);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_GetEUid
// Address: 00e2f22c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__uid_t SystemNative_GetEUid(void)

{
  __uid_t _Var1;
  
  _Var1 = (*(code *)PTR_geteuid_01ff6170)();
  return _Var1;
}



// ==========================================================================================
// Function: SystemNative_GetEGid
// Address: 00e2f230
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__gid_t SystemNative_GetEGid(void)

{
  __gid_t _Var1;
  
  _Var1 = (*(code *)PTR_getegid_01ff6178)();
  return _Var1;
}



// ==========================================================================================
// Function: SystemNative_FStat2
// Address: 00e2f238
// ==========================================================================================

void SystemNative_FStat2(void)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00e29d04(
                      "C:/Program Files/Unity/Hub/Editor/2022.3.62f2/Editor/Data/il2cpp/libil2cpp/os/ClassLibraryPAL/pal_unused.cpp(22) : Unsupported internal call for IL2CPP:SystemNative_FStat2 - Not implemented"
                      );
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar1,0);
}



// ==========================================================================================
// Function: SystemNative_UTime
// Address: 00e2f250
// ==========================================================================================

void SystemNative_UTime(void)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00e29d04(
                      "C:/Program Files/Unity/Hub/Editor/2022.3.62f2/Editor/Data/il2cpp/libil2cpp/os/ClassLibraryPAL/pal_unused.cpp(29) : Unsupported internal call for IL2CPP:SystemNative_UTime - Not implemented"
                      );
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar1,0);
}



// ==========================================================================================
// Function: SystemNative_ConvertErrorPalToPlatform
// Address: 01ec51e0
// ==========================================================================================

void SystemNative_ConvertErrorPalToPlatform(void)

{
  (*(code *)PTR_SystemNative_ConvertErrorPalToPlatform_01ff5b10)();
  return;
}



// ==========================================================================================
// Function: SystemNative_GetNonCryptographicallySecureRandomBytes
// Address: 01ec51f0
// ==========================================================================================

void SystemNative_GetNonCryptographicallySecureRandomBytes(void)

{
  (*(code *)PTR_SystemNative_GetNonCryptographicallySecureRandomBytes_01ff5b18)();
  return;
}



// ==========================================================================================
// Function: SystemNative_ConvertErrorPlatformToPal
// Address: 01ec5200
// ==========================================================================================

void SystemNative_ConvertErrorPlatformToPal(void)

{
  (*(code *)PTR_SystemNative_ConvertErrorPlatformToPal_01ff5b20)();
  return;
}



// ==========================================================================================
// Function: SystemNative_StrErrorR
// Address: 01ec5210
// ==========================================================================================

void SystemNative_StrErrorR(void)

{
  (*(code *)PTR_SystemNative_StrErrorR_01ff5b28)();
  return;
}



// ==========================================================================================
// Function: SystemNative_OpenDir
// Address: 01ec5220
// ==========================================================================================

void SystemNative_OpenDir(void)

{
  (*(code *)PTR_SystemNative_OpenDir_01ff5b30)();
  return;
}



// ==========================================================================================
// Function: SystemNative_GetReadDirRBufferSize
// Address: 01ec5230
// ==========================================================================================

void SystemNative_GetReadDirRBufferSize(void)

{
  (*(code *)PTR_SystemNative_GetReadDirRBufferSize_01ff5b38)();
  return;
}



// ==========================================================================================
// Function: SystemNative_ReadDirR
// Address: 01ec5240
// ==========================================================================================

void SystemNative_ReadDirR(void)

{
  (*(code *)PTR_SystemNative_ReadDirR_01ff5b40)();
  return;
}



// ==========================================================================================
// Function: SystemNative_CloseDir
// Address: 01ec5250
// ==========================================================================================

void SystemNative_CloseDir(void)

{
  (*(code *)PTR_SystemNative_CloseDir_01ff5b48)();
  return;
}



// ==========================================================================================
// Function: SystemNative_ReadLink
// Address: 01ec5260
// ==========================================================================================

void SystemNative_ReadLink(void)

{
  (*(code *)PTR_SystemNative_ReadLink_01ff5b50)();
  return;
}



// ==========================================================================================
// Function: SystemNative_Stat2
// Address: 01ec5270
// ==========================================================================================

void SystemNative_Stat2(void)

{
  (*(code *)PTR_SystemNative_Stat2_01ff5b58)();
  return;
}



// ==========================================================================================
// Function: SystemNative_LStat2
// Address: 01ec5280
// ==========================================================================================

void SystemNative_LStat2(void)

{
  (*(code *)PTR_SystemNative_LStat2_01ff5b60)();
  return;
}



// ==========================================================================================
// Function: SystemNative_Symlink
// Address: 01ec5290
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int SystemNative_Symlink(char *__from,char *__to)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_SystemNative_Symlink_01ff5b68)((int)__from);
  return iVar1;
}



// ==========================================================================================
// Function: SystemNative_CopyFile
// Address: 01ec52a0
// ==========================================================================================

void SystemNative_CopyFile(void)

{
  (*(code *)PTR_SystemNative_CopyFile_01ff5b70)();
  return;
}



// ==========================================================================================
// Function: SystemNative_GetEGid
// Address: 01ec52b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__gid_t SystemNative_GetEGid(void)

{
  __gid_t _Var1;
  
  _Var1 = (*(code *)PTR_SystemNative_GetEGid_01ff5b78)();
  return _Var1;
}



// ==========================================================================================
// Function: SystemNative_GetEUid
// Address: 01ec52c0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

__uid_t SystemNative_GetEUid(void)

{
  __uid_t _Var1;
  
  _Var1 = (*(code *)PTR_SystemNative_GetEUid_01ff5b80)();
  return _Var1;
}



// ==========================================================================================
// Function: SystemNative_LChflagsCanSetHiddenFlag
// Address: 01ec52d0
// ==========================================================================================

void SystemNative_LChflagsCanSetHiddenFlag(void)

{
  (*(code *)PTR_SystemNative_LChflagsCanSetHiddenFlag_01ff5b88)();
  return;
}



// ==========================================================================================
// Function: SystemNative_MkDir
// Address: 01ec52e0
// ==========================================================================================

void SystemNative_MkDir(void)

{
  (*(code *)PTR_SystemNative_MkDir_01ff5b90)();
  return;
}



// ==========================================================================================
// Function: SystemNative_RmDir
// Address: 01ec52f0
// ==========================================================================================

void SystemNative_RmDir(void)

{
  (*(code *)PTR_SystemNative_RmDir_01ff5b98)();
  return;
}



// ==========================================================================================
// Function: SystemNative_Unlink
// Address: 01ec5300
// ==========================================================================================

void SystemNative_Unlink(void)

{
  (*(code *)PTR_SystemNative_Unlink_01ff5ba0)();
  return;
}



// ==========================================================================================
