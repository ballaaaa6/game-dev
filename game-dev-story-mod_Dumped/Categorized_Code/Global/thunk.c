// Function: thunk_FUN_00d71ee4
// Address: 00d7147c
// ==========================================================================================

void thunk_FUN_00d71ee4(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d71ff0
// Address: 00d71640
// ==========================================================================================

void thunk_FUN_00d71ff0(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d71ee4
// Address: 00d71840
// ==========================================================================================

void thunk_FUN_00d71ee4(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d71ff0
// Address: 00d71aa0
// ==========================================================================================

void thunk_FUN_00d71ff0(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d71ff0
// Address: 00d72bc0
// ==========================================================================================

void thunk_FUN_00d71ff0(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d83350
// Address: 00d82b20
// ==========================================================================================

void thunk_FUN_00d83350(undefined8 *param_1)

{
  thunk_FUN_00e1216c(*param_1);
  *param_1 = 0;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d81f3c
// Address: 00d85b44
// ==========================================================================================

void thunk_FUN_00d81f3c(undefined8 *param_1)

{
  thunk_FUN_00e1216c(*param_1);
  *param_1 = 0;
  thunk_FUN_00e1216c(param_1[1]);
  param_1[1] = 0;
  thunk_FUN_00e1216c(param_1[2]);
  param_1[2] = 0;
  thunk_FUN_00e1216c(param_1[3]);
  param_1[3] = 0;
  thunk_FUN_00e1216c(param_1[4]);
  param_1[4] = 0;
  thunk_FUN_00e1216c(param_1[5]);
  param_1[5] = 0;
  thunk_FUN_00e1216c(param_1[6]);
  param_1[6] = 0;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3dff0
// Address: 00d9ee3c
// ==========================================================================================

void thunk_FUN_00e3dff0(void)

{
  FUN_00e3ddec(0,0);
  if (DAT_0231b800 != 0) {
    FUN_00e3e01c();
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e31db8
// Address: 00d9ee40
// ==========================================================================================

undefined8 thunk_FUN_00e31db8(undefined8 param_1)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_00e3eaec(0x10);
  *puVar1 = 0;
  puVar1[1] = 0;
  FUN_00e31c58(puVar1 + 1,param_1,0);
  FUN_00e4433c(FUN_00e31e04,puVar1);
  return 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dfd95c
// Address: 00da27b8
// ==========================================================================================

undefined8 thunk_FUN_00dfd95c(long param_1,long param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = FUN_00dfc824(*(undefined8 *)(param_1 + 0x10),1);
  uVar2 = FUN_00dfc824(*(undefined8 *)(param_2 + 0x10),1);
  if (((*(byte *)(*(long *)(param_1 + 0x10) + 0xb) >> 5 & 1) != 0) &&
     ((*(byte *)(*(long *)(param_2 + 0x10) + 0xb) >> 5 & 1) == 0)) {
    return 0;
  }
  uVar1 = FUN_00dfd720(uVar1,uVar2);
  return uVar1;
}



// ==========================================================================================
// Function: thunk_FUN_00df7750
// Address: 00dac864
// ==========================================================================================

uint thunk_FUN_00df7750(int param_1)

{
  int iVar1;
  uint uVar2;
  div_t dVar3;
  int *piVar4;
  timeval *__timeout;
  uint uStack_a4;
  timeval tStack_a0;
  fd_set fStack_90;
  
  while( true ) {
    fStack_90.fds_bits[13] = 0;
    fStack_90.fds_bits[12] = 0;
    fStack_90.fds_bits[15] = 0;
    fStack_90.fds_bits[14] = 0;
    fStack_90.fds_bits[9] = 0;
    fStack_90.fds_bits[8] = 0;
    fStack_90.fds_bits[11] = 0;
    fStack_90.fds_bits[10] = 0;
    fStack_90.fds_bits[5] = 0;
    fStack_90.fds_bits[4] = 0;
    fStack_90.fds_bits[7] = 0;
    fStack_90.fds_bits[6] = 0;
    fStack_90.fds_bits[1] = 0;
    fStack_90.fds_bits[0] = 0;
    fStack_90.fds_bits[3] = 0;
    fStack_90.fds_bits[2] = 0;
    __FD_SET_chk(0,&fStack_90,0x80);
    if (param_1 < 0) {
      __timeout = (timeval *)0x0;
    }
    else {
      dVar3 = div(param_1,1000);
      tStack_a0.tv_sec = (__time_t)dVar3.quot;
      tStack_a0.tv_usec = (long)dVar3 >> 0x20;
      __timeout = &tStack_a0;
    }
    iVar1 = select(1,&fStack_90,(fd_set *)0x0,(fd_set *)0x0,__timeout);
    if (iVar1 != -1) break;
    piVar4 = (int *)__errno();
    if (*piVar4 != 4) {
      return 0;
    }
  }
  if (iVar1 < 1) {
    return 0;
  }
  uStack_a4 = 0;
  uVar2 = ioctl(0,0x541b,&uStack_a4);
  if ((int)uVar2 < 0) {
    uStack_a4 = uVar2;
  }
  return uStack_a4 & ((int)uStack_a4 >> 0x1f ^ 0xffffffffU);
}



// ==========================================================================================
// Function: thunk_FUN_00df5ba8
// Address: 00dacdac
// ==========================================================================================

undefined thunk_FUN_00df5ba8(void)

{
  return DAT_02108100;
}



// ==========================================================================================
// Function: thunk_FUN_00df7c2c
// Address: 00dacdb0
// ==========================================================================================

void thunk_FUN_00df7c2c(void)

{
  sysconf(0x61);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df8634
// Address: 00dacdb4
// ==========================================================================================

int thunk_FUN_00df8634(void)

{
  int iVar1;
  int iStack_20;
  long lStack_18;
  
  iVar1 = clock_gettime(1,(timespec *)&iStack_20);
  if (iVar1 == 0) {
    iVar1 = ((int)(SUB168(SEXT816(lStack_18) * SEXT816(0x431bde82d7b634db),8) >> 0x12) -
            (SUB164(SEXT816(lStack_18) * SEXT816(0x431bde82d7b634db),0xc) >> 0x1f)) +
            iStack_20 * 1000;
  }
  else {
    iVar1 = -0x4d2fa200;
  }
  return iVar1;
}



// ==========================================================================================
// Function: thunk_FUN_00df646c
// Address: 00dad44c
// ==========================================================================================

void thunk_FUN_00df646c(long *param_1)

{
  long *plVar1;
  long lVar2;
  long lStack_28;
  
  FUN_00dce854();
  plVar1 = (long *)thunk_FUN_00dce854();
  lStack_28 = 0;
  lVar2 = FUN_00dfcf44(DAT_02107e40,"UnhandledException");
  if (*param_1 != DAT_02107e28) {
    FUN_00df3d5c(*(undefined8 *)(lVar2 + 8),&lStack_28,*plVar1 + (long)*(int *)(lVar2 + 0x18),1);
    if (lStack_28 != 0) {
      FUN_00df64f4(plVar1,lStack_28,param_1);
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e0e748
// Address: 00dad450
// ==========================================================================================

long thunk_FUN_00e0e748(uint param_1)

{
  ulong uVar1;
  undefined *puVar2;
  long lVar3;
  void **ppvVar4;
  void *__dest;
  void *__src;
  void *pvVar5;
  
  puVar2 = PTR_DAT_01ff5418;
  lVar3 = DAT_02108748;
  if (param_1 != 0) {
    uVar1 = (-(ulong)(param_1 >> 0x1f) & 0xfffffffe00000000 | (ulong)param_1 << 1) + 0x1a;
    if (uVar1 < param_1) {
      ppvVar4 = (void **)FUN_00e28ac0();
      __src = *ppvVar4;
      pvVar5 = ppvVar4[1];
      lVar3 = FUN_00e0e748((ulong)pvVar5 & 0xffffffff);
      __dest = (void *)FUN_00dc71a8();
      memcpy(__dest,__src,
             -((ulong)pvVar5 >> 0x1f & 1) & 0xfffffffe00000000 | ((ulong)pvVar5 & 0xffffffff) << 1);
      return lVar3;
    }
    lVar3 = FUN_00e1137c(uVar1,*(undefined8 *)(PTR_DAT_01ff5418 + 0x90));
    *(uint *)(lVar3 + 0x10) = param_1;
    *(undefined2 *)(lVar3 + (long)(int)param_1 * 2 + 0x14) = 0;
    if ((char)*PTR_DAT_01ff5438 < '\0') {
      FUN_00e2ae40(lVar3,*(undefined8 *)(puVar2 + 0x90));
    }
  }
  return lVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e4da18
// Address: 00dae900
// ==========================================================================================

long thunk_FUN_00e4da18(undefined8 *param_1)

{
  long lVar1;
  undefined8 uVar2;
  undefined8 uStack_18;
  
  if (*(int *)(param_1 + 5) == 0) {
    lVar1 = dlopen(0,1);
    if (lVar1 != 0) {
      return lVar1;
    }
    uVar2 = dlerror();
    FUN_00e4de58(&uStack_18,"dlerror() = %s",uVar2);
    if (*(int *)(param_1 + 5) == 0) {
      *param_1 = 0;
      param_1[1] = 0;
      *(undefined4 *)(param_1 + 2) = 0;
      param_1[3] = 0;
      param_1[4] = uStack_18;
      param_1[5] = 0x20006000000;
    }
  }
  return -100;
}



// ==========================================================================================
// Function: thunk_FUN_00db0ac4
// Address: 00daeea4
// ==========================================================================================

undefined8 thunk_FUN_00db0ac4(void)

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
// Function: thunk_FUN_00df82f8
// Address: 00daf9b4
// ==========================================================================================

void thunk_FUN_00df82f8(void)

{
  (*(code *)PTR_FUN_020ff038)();
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df8308
// Address: 00daf9f0
// ==========================================================================================

void thunk_FUN_00df8308(void)

{
  (*(code *)PTR_FUN_020ff060)();
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00db0150
// Address: 00daff4c
// ==========================================================================================

void thunk_FUN_00db0150(long *param_1)

{
  long *plVar1;
  long lVar2;
  long lVar3;
  long *plVar4;
  
  if (param_1[2] != 0) {
    lVar2 = *param_1;
    plVar1 = (long *)param_1[1];
    lVar3 = *plVar1;
    *(undefined8 *)(lVar3 + 8) = *(undefined8 *)(lVar2 + 8);
    **(long **)(lVar2 + 8) = lVar3;
    param_1[2] = 0;
    while (plVar1 != param_1) {
      plVar4 = (long *)plVar1[1];
      operator_delete(plVar1);
      plVar1 = plVar4;
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00da2754
// Address: 00db06e8
// ==========================================================================================

undefined8 thunk_FUN_00da2754(void)

{
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dae030
// Address: 00db06ec
// ==========================================================================================

undefined8 thunk_FUN_00dae030(int *param_1,undefined4 *param_2)

{
  char *__name;
  int *piVar1;
  undefined auStack_18 [8];
  
  if ((param_1[1] == 1) && ((*(byte *)((long)param_1 + 0x23) >> 2 & 1) != 0)) {
    if ((*(byte *)(param_1 + 2) & 1) == 0) {
      __name = (char *)((long)param_1 + 9);
    }
    else {
      __name = *(char **)(param_1 + 6);
    }
    unlink(__name);
  }
  close(*param_1);
  FUN_00da6960(auStack_18,&DAT_02107400);
  if (DAT_02107450 == param_1) {
    DAT_02107450 = *(int **)(param_1 + 0x12);
  }
  piVar1 = *(int **)(param_1 + 0x10);
  if (DAT_021075f8 == param_1) {
    DAT_021075f8 = piVar1;
  }
  if (piVar1 != (int *)0x0) {
    *(undefined8 *)(piVar1 + 0x12) = *(undefined8 *)(param_1 + 0x12);
  }
  if (*(long *)(param_1 + 0x12) != 0) {
    *(int **)(*(long *)(param_1 + 0x12) + 0x40) = piVar1;
  }
  FUN_00da71f4(auStack_18);
  if ((*(byte *)(param_1 + 2) & 1) != 0) {
    operator_delete(*(void **)(param_1 + 6));
  }
  operator_delete(param_1);
  *param_2 = 0;
  return 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dae16c
// Address: 00db0874
// ==========================================================================================

bool thunk_FUN_00dae16c(int *param_1,__off_t param_2,undefined4 *param_3)

{
  bool bVar1;
  int iVar2;
  undefined4 uVar3;
  __off_t _Var4;
  __off_t _Var5;
  int *piVar6;
  undefined4 *puVar7;
  
  if (param_1[1] == 1) {
    _Var4 = lseek(*param_1,0,1);
    if ((_Var4 == -1) || (_Var5 = lseek(*param_1,param_2,0), _Var5 == -1)) {
      piVar6 = (int *)__errno();
      iVar2 = *piVar6;
    }
    else {
      do {
        iVar2 = ftruncate(*param_1,param_2);
        if (iVar2 != -1) {
          _Var4 = lseek(*param_1,_Var4,0);
          uVar3 = 0;
          if (_Var4 == -1) {
            puVar7 = (undefined4 *)__errno();
            uVar3 = FUN_00e2f2bc(*puVar7);
          }
          bVar1 = _Var4 != -1;
          goto LAB_00dae208;
        }
        piVar6 = (int *)__errno();
        iVar2 = *piVar6;
      } while (iVar2 == 4);
    }
    uVar3 = FUN_00e2f2bc(iVar2);
    bVar1 = false;
  }
  else {
    bVar1 = false;
    uVar3 = 6;
  }
LAB_00dae208:
  *param_3 = uVar3;
  return bVar1;
}



// ==========================================================================================
// Function: thunk_FUN_00dae104
// Address: 00db09b0
// ==========================================================================================

__off_t thunk_FUN_00dae104(int *param_1,undefined4 *param_2)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  __off_t _Stack_60;
  
  if (param_1[1] == 1) {
    iVar1 = fstat(*param_1,(stat *)&stack0xffffffffffffff70);
    if (iVar1 == -1) {
      puVar3 = (undefined4 *)__errno();
      uVar2 = FUN_00e2f2bc(*puVar3);
      *param_2 = uVar2;
      _Stack_60 = -1;
    }
    else {
      *param_2 = 0;
    }
  }
  else {
    _Stack_60 = 0;
    *param_2 = 6;
  }
  return _Stack_60;
}



// ==========================================================================================
// Function: thunk_FUN_00dae258
// Address: 00db09b4
// ==========================================================================================

__off_t thunk_FUN_00dae258(int *param_1,__off_t param_2,uint param_3,undefined4 *param_4)

{
  undefined4 uVar1;
  __off_t _Var2;
  undefined4 *puVar3;
  
  if (param_1[1] == 1) {
    if (param_3 < 3) {
      _Var2 = lseek(*param_1,param_2,param_3);
      if (_Var2 == -1) {
        puVar3 = (undefined4 *)__errno();
        uVar1 = FUN_00e2f2bc(*puVar3);
        _Var2 = -1;
      }
      else {
        uVar1 = 0;
      }
    }
    else {
      _Var2 = -1;
      uVar1 = 0x57;
    }
  }
  else {
    _Var2 = 0;
    uVar1 = 6;
  }
  *param_4 = uVar1;
  return _Var2;
}



// ==========================================================================================
// Function: thunk_FUN_00dadb50
// Address: 00db09b8
// ==========================================================================================

void thunk_FUN_00dadb50(void)

{
  undefined8 *puVar1;
  
  if (DAT_02107458 == (undefined8 *)0x0) {
    puVar1 = (undefined8 *)operator_new(0x50);
    DAT_02107458 = puVar1;
    puVar1[2] = 0;
    puVar1[1] = 0;
    puVar1[4] = 0;
    puVar1[3] = 0;
    *(undefined8 *)((long)puVar1 + 0x25) = 0;
    puVar1[7] = 0;
    puVar1[6] = 0;
    puVar1[9] = 0;
    puVar1[8] = 0;
    *puVar1 = 0x200000002;
    *(undefined4 *)(puVar1 + 5) = 3;
    puVar1[4] = 0xffffffff00000000;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dadba0
// Address: 00db09bc
// ==========================================================================================

void thunk_FUN_00dadba0(void)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  
  if (DAT_02107460 == (undefined8 *)0x0) {
    puVar2 = (undefined8 *)operator_new(0x50);
    uVar1 = DAT_005bc4b8;
    DAT_02107460 = puVar2;
    puVar2[2] = 0;
    puVar2[1] = 0;
    puVar2[4] = 0;
    puVar2[3] = 0;
    *(undefined8 *)((long)puVar2 + 0x25) = 0;
    puVar2[7] = 0;
    puVar2[6] = 0;
    puVar2[9] = 0;
    puVar2[8] = 0;
    *(undefined4 *)(puVar2 + 5) = 1;
    *puVar2 = uVar1;
    puVar2[4] = 0xffffffff00000000;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dadbf4
// Address: 00db09c0
// ==========================================================================================

void thunk_FUN_00dadbf4(void)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  
  if (DAT_02107468 == (undefined8 *)0x0) {
    puVar2 = (undefined8 *)operator_new(0x50);
    uVar1 = DAT_005bc3c8;
    DAT_02107468 = puVar2;
    puVar2[2] = 0;
    puVar2[1] = 0;
    puVar2[4] = 0;
    puVar2[3] = 0;
    *(undefined8 *)((long)puVar2 + 0x25) = 0;
    puVar2[7] = 0;
    puVar2[6] = 0;
    puVar2[9] = 0;
    puVar2[8] = 0;
    *(undefined4 *)(puVar2 + 5) = 3;
    *puVar2 = uVar1;
    puVar2[4] = 0xffffffff00000000;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dadd30
// Address: 00db0a54
// ==========================================================================================

undefined4 thunk_FUN_00dadd30(long param_1)

{
  return *(undefined4 *)(param_1 + 4);
}



// ==========================================================================================
// Function: thunk_FUN_00dd09c8
// Address: 00db0b74
// ==========================================================================================

void thunk_FUN_00dd09c8(void)

{
  uint uVar1;
  undefined4 uVar2;
  void *pvVar3;
  ulong uVar4;
  
  uVar2 = FUN_00dae474();
  uVar4 = (ulong)DAT_020ff078;
  uVar1 = DAT_020ff078 >> 0xd;
  pvVar3 = pthread_getspecific(*DAT_02107b08);
  **(undefined4 **)(*(long *)((long)pvVar3 + ((ulong)uVar1 & 0x7fff8)) + (uVar4 & 0xffff) * 8) =
       uVar2;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df702c
// Address: 00db0b78
// ==========================================================================================

undefined8 thunk_FUN_00df702c(long param_1,long param_2,undefined8 param_3,undefined8 param_4)

{
  byte bVar1;
  undefined8 uVar2;
  long lVar3;
  ulong uVar4;
  long lStack_48;
  long lStack_40;
  long lStack_38;
  
  bVar1 = *(byte *)(*(long *)(param_1 + 0x28) + 0x52);
  uVar4 = (ulong)bVar1;
  lStack_40 = uVar4 + 2;
  lStack_38 = lStack_40;
  lStack_48 = thunk_FUN_00df82f8(lStack_40 * 8,8);
  if (bVar1 != 0) {
    lVar3 = 0;
    do {
      *(undefined8 *)(lStack_48 + lVar3) = *(undefined8 *)(param_2 + lVar3);
      lVar3 = lVar3 + 8;
    } while ((ulong)(uint)bVar1 * 8 - lVar3 != 0);
  }
  *(undefined8 *)(lStack_48 + uVar4 * 8) = param_3;
  *(undefined8 *)(lStack_48 + uVar4 * 8 + 8) = param_4;
  uVar2 = FUN_00dce854();
  uVar2 = FUN_00de77fc(uVar2,param_1,*(undefined8 *)(param_1 + 0x28),lStack_48);
  FUN_00d9f2a8(&lStack_48);
  return uVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00df70f0
// Address: 00db0b7c
// ==========================================================================================

undefined8 thunk_FUN_00df70f0(long param_1,long param_2,undefined8 param_3,long *param_4)

{
  long lVar1;
  byte bVar2;
  undefined8 uVar3;
  long lVar4;
  void *__src;
  undefined8 uVar5;
  long *plVar6;
  int iVar7;
  ulong uVar8;
  long *plVar9;
  uint uVar10;
  void *__dest;
  long lVar11;
  long lVar12;
  ulong uVar13;
  undefined auVar14 [16];
  long lStack_58;
  long lStack_48;
  
  plVar6 = &lStack_58;
  uVar3 = FUN_00de7a4c(param_1,&lStack_48);
  if (lStack_58 == 0) {
    if (param_2 != 0) {
      lVar11 = *(long *)(*(long *)(param_1 + 0x20) + 0x28);
      uVar8 = (ulong)*(byte *)(lVar11 + 0x52);
      if (*(byte *)(lVar11 + 0x52) != 0) {
        lVar12 = 0;
        uVar13 = 0;
        do {
          if ((*(byte *)(*(long *)(*(long *)(lVar11 + 0x30) + uVar13 * 8) + 0xb) >> 5 & 1) != 0) {
            lVar4 = il2cpp_class_from_type();
            if (*(int *)(lVar4 + 0x28) < 0) {
              __dest = *(void **)(param_2 + lVar12 * 8);
              __src = (void *)FUN_00e11d68(*(undefined8 *)(lStack_48 + 0x20 + lVar12 * 8));
              memcpy(__dest,__src,(long)*(int *)(lVar4 + 0x108));
            }
            else {
              **(undefined8 **)(param_2 + lVar12 * 8) =
                   *(undefined8 *)(lStack_48 + 0x20 + lVar12 * 8);
            }
            uVar8 = (ulong)*(byte *)(lVar11 + 0x52);
            lVar12 = lVar12 + 1;
          }
          uVar13 = uVar13 + 1;
        } while (uVar13 < uVar8);
      }
    }
    return uVar3;
  }
  auVar14 = il2cpp_raise_exception(lStack_58);
  lVar11 = auVar14._8_8_;
  uVar3 = auVar14._0_8_;
  lVar12 = *(long *)(*(long *)(lVar11 + 0x10) + 0x10);
  bVar2 = *(byte *)(lVar12 + 0x52);
  if (bVar2 == 0) {
    lVar4 = 0;
  }
  else {
    uVar10 = (uint)bVar2;
    iVar7 = 0;
    if (bVar2 < 2) {
      uVar10 = 1;
    }
    uVar8 = (ulong)uVar10;
    plVar9 = *(long **)(lVar12 + 0x30);
    do {
      uVar8 = uVar8 - 1;
      iVar7 = (*(uint *)(*plVar9 + 8) >> 0x1d & 1) + iVar7;
      plVar9 = plVar9 + 1;
    } while (uVar8 != 0);
    lVar4 = (long)iVar7;
  }
  if (DAT_02108188 == 0) {
    DAT_02108188 = il2cpp_array_class_get(DAT_02107d40,1);
    DataMemoryBarrier(2,3);
  }
  uVar5 = il2cpp_array_new_specific(DAT_02108188,lVar4);
  FUN_00e331f0(param_4,uVar5);
  *plVar6 = 0;
  if (*(int *)(*(long *)(lVar12 + 0x20) + 0x28) < 0) {
    uVar3 = il2cpp_object_unbox(uVar3);
  }
  if (*(char *)(lVar12 + 0x52) == '\0') {
    uVar5 = 0;
  }
  else {
    uVar5 = *(undefined8 *)(lVar11 + 0x18);
  }
  uVar3 = FUN_00df5f8c(lVar12,uVar3,uVar5,plVar6);
  bVar2 = *(byte *)(lVar12 + 0x52);
  if (bVar2 != 0) {
    uVar10 = (uint)bVar2;
    if (bVar2 < 2) {
      uVar10 = 1;
    }
    lVar4 = 0;
    iVar7 = 0;
    do {
      if ((*(byte *)(*(long *)(*(long *)(lVar12 + 0x30) + lVar4) + 0xb) >> 5 & 1) != 0) {
        lVar1 = (long)iVar7;
        iVar7 = iVar7 + 1;
        *(undefined8 *)(*param_4 + lVar1 * 8 + 0x20) =
             *(undefined8 *)(*(long *)(lVar11 + 0x18) + lVar4 + 0x20);
      }
      lVar4 = lVar4 + 8;
    } while ((ulong)uVar10 * 8 - lVar4 != 0);
  }
  return uVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e00108
// Address: 00db0bb8
// ==========================================================================================

void thunk_FUN_00e00108(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  FUN_00dcea18();
  DAT_02108678 = param_2;
  DAT_02108680 = param_3;
  DAT_02108670 = param_1;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e01b94
// Address: 00db0bd0
// ==========================================================================================

void thunk_FUN_00e01b94(undefined8 param_1)

{
  FUN_00dcec04(param_1,1);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df4668
// Address: 00db0bdc
// ==========================================================================================

long thunk_FUN_00df4668(long param_1,long param_2)

{
  param_1 = param_1 + *(int *)(param_2 + 0x18);
  if (*(int *)(*(long *)(param_2 + 0x10) + 0x28) < 0) {
    param_1 = param_1 + -0x10;
  }
  return param_1;
}



// ==========================================================================================
// Function: thunk_FUN_00dd38ec
// Address: 00db0c08
// ==========================================================================================

void thunk_FUN_00dd38ec(void)

{
  DataMemoryBarrier(2,3);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd1560
// Address: 00db0c40
// ==========================================================================================

bool thunk_FUN_00dd1560(long param_1)

{
  if ((*(byte *)(param_1 + 0x53) & 3) == 2) {
    return *(long *)(*(long *)(param_1 + 0x40) + 0x10) != 0;
  }
  return false;
}



// ==========================================================================================
// Function: thunk_FUN_00dd1400
// Address: 00db0c44
// ==========================================================================================

undefined8 thunk_FUN_00dd1400(long param_1)

{
  return *(undefined8 *)(param_1 + 0x20);
}



// ==========================================================================================
// Function: thunk_FUN_00da7550
// Address: 00db0cbc
// ==========================================================================================

void thunk_FUN_00da7550(long param_1,long param_2)

{
  long **pplVar1;
  long lStack_28;
  long lStack_20;
  undefined8 uStack_18;
  
  if ((*(byte *)(param_1 + 0x53) >> 1 & 1) == 0) {
    lStack_20 = 0;
  }
  else {
    pplVar1 = (long **)(param_1 + 0x40);
    param_1 = **pplVar1;
    lStack_20 = (*pplVar1)[1];
  }
  uStack_18 = *(undefined8 *)(*(long *)(param_2 + 0x40) + 0x10);
  lStack_28 = param_1;
  FUN_00da75bc(&lStack_28,1);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df405c
// Address: 00db0cc0
// ==========================================================================================

void thunk_FUN_00df405c(long param_1)

{
  int *piVar1;
  pthread_t *ppVar2;
  void *pvVar3;
  pthread_t pVar4;
  char cVar5;
  bool bVar6;
  int iVar7;
  pthread_t pVar8;
  long lVar9;
  undefined8 uVar10;
  pthread_t pVar11;
  int iVar12;
  int *piVar13;
  byte abStack_78 [16];
  void *pvStack_68;
  byte abStack_60 [16];
  void *pvStack_50;
  long lStack_48;
  
  piVar13 = (int *)(param_1 + 0xe0);
  if (*piVar13 != 0) {
    return;
  }
  pVar8 = pthread_self();
  if (pVar8 == DAT_02108160) {
    DAT_02108168 = DAT_02108168 + 1;
  }
  else {
    iVar12 = 0;
    do {
      iVar7 = DAT_02108120;
      if (DAT_02108120 == iVar12) {
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
        if (bVar6) {
          cVar5 = ExclusiveMonitorsStatus();
          DAT_02108120 = iVar12 + 1;
        }
        if (cVar5 != '\0') goto LAB_00df40e4;
        bVar6 = true;
      }
      else {
        ClearExclusiveLocal();
LAB_00df40e4:
        bVar6 = false;
      }
    } while ((iVar7 != 2) && (iVar12 = iVar7, !bVar6));
    while (iVar7 != 0) {
      FUN_00e4d8f8(&DAT_02108120,2,0xffffffff);
      do {
        iVar7 = DAT_02108120;
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
        if (bVar6) {
          DAT_02108120 = 2;
          cVar5 = ExclusiveMonitorsStatus();
        }
      } while (cVar5 != '\0');
    }
    DAT_02108168 = 1;
    DAT_02108160 = pVar8;
  }
  while (*piVar13 == 1) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') {
      DataMemoryBarrier(2,3);
      if (DAT_02108168 < 1) {
        return;
      }
      if (DAT_02108168 + -1 == 0) {
        DAT_02108160 = 0;
        DAT_02108168 = 0;
        do {
          iVar12 = DAT_02108120;
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
          if (bVar6) {
            DAT_02108120 = 0;
            cVar5 = ExclusiveMonitorsStatus();
          }
        } while (cVar5 != '\0');
        if (iVar12 == 2) {
          FUN_00e4d950(&DAT_02108120,1,0);
          return;
        }
        DAT_02108160 = 0;
        DAT_02108168 = 0;
        return;
      }
      DAT_02108168 = DAT_02108168 + -1;
      return;
    }
  }
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  piVar1 = (int *)(param_1 + 0xdc);
LAB_00df41b4:
  if (*piVar1 == 1) goto code_r0x00df41c0;
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  ppVar2 = (pthread_t *)(param_1 + 0xe8);
  pVar8 = pthread_self();
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = pVar8;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar6) {
      *piVar1 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  iVar12 = DAT_02108168 + -1;
  if ((0 < DAT_02108168) && (DAT_02108168 = iVar12, iVar12 == 0)) {
    DAT_02108160 = 0;
    DAT_02108168 = 0;
    do {
      iVar12 = DAT_02108120;
      cVar5 = '\x01';
      bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
      if (bVar6) {
        DAT_02108120 = 0;
        cVar5 = ExclusiveMonitorsStatus();
      }
    } while (cVar5 != '\0');
    if (iVar12 == 2) {
      FUN_00e4d950(&DAT_02108120,1,0);
    }
  }
  lStack_48 = 0;
  lVar9 = FUN_00dff79c(param_1);
  if (lVar9 != 0) {
    FUN_00df5da8(lVar9,0,0,&lStack_48);
  }
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = 0;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  if (lStack_48 != 0) {
    FUN_00deea58(abStack_78,param_1 + 0x20,0);
    pvVar3 = (void *)((ulong)abStack_78 | 1);
    if ((abStack_78[0] & 1) != 0) {
      pvVar3 = pvStack_68;
    }
    FUN_00dc6ac4(abStack_60,"The type initializer for \'%s\' threw an exception.",pvVar3);
    if ((abStack_78[0] & 1) != 0) {
      operator_delete(pvStack_68);
    }
    pvVar3 = (void *)((ulong)abStack_60 | 1);
    if ((abStack_60[0] & 1) != 0) {
      pvVar3 = pvStack_50;
    }
    uVar10 = FUN_00e29638(pvVar3,lStack_48);
    FUN_00dfd62c(param_1,uVar10);
    if ((abStack_60[0] & 1) != 0) {
      operator_delete(pvStack_50);
    }
    goto LAB_00df43bc;
  }
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  goto LAB_00df43b8;
code_r0x00df41c0:
  cVar5 = '\x01';
  bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
  if (bVar6) {
    *piVar1 = 1;
    cVar5 = ExclusiveMonitorsStatus();
  }
  if (cVar5 == '\0') goto code_r0x00df41c8;
  goto LAB_00df41b4;
code_r0x00df41c8:
  DataMemoryBarrier(2,3);
  iVar12 = DAT_02108168 + -1;
  if ((0 < DAT_02108168) && (DAT_02108168 = iVar12, iVar12 == 0)) {
    DAT_02108160 = 0;
    DAT_02108168 = 0;
    do {
      iVar12 = DAT_02108120;
      cVar5 = '\x01';
      bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
      if (bVar6) {
        DAT_02108120 = 0;
        cVar5 = ExclusiveMonitorsStatus();
      }
    } while (cVar5 != '\0');
    if (iVar12 == 2) {
      FUN_00e4d950(&DAT_02108120,1,0);
    }
  }
  pVar8 = pthread_self();
  ppVar2 = (pthread_t *)(param_1 + 0xe8);
  do {
    pVar11 = *ppVar2;
    if (pVar11 != pVar8) {
      ClearExclusiveLocal();
      bVar6 = false;
      goto LAB_00df4378;
    }
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = pVar8;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  bVar6 = true;
LAB_00df4378:
  DataMemoryBarrier(2,3);
  pVar4 = pVar8;
  if (!bVar6) {
    pVar4 = pVar11;
  }
  if (pVar4 == pVar8) {
    return;
  }
  while (*piVar13 == 1) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') goto LAB_00df43b8;
  }
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  piVar1 = (int *)(param_1 + 0xd8);
  while (*piVar1 == 0) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar6) {
      *piVar1 = 0;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') {
      DataMemoryBarrier(2,3);
      FUN_00dcba94(1,0);
      while (*piVar13 == 1) {
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
        if (bVar6) {
          *piVar13 = 1;
          cVar5 = ExclusiveMonitorsStatus();
        }
        if (cVar5 == '\0') goto LAB_00df43b8;
      }
      ClearExclusiveLocal();
      DataMemoryBarrier(2,3);
    }
  }
  ClearExclusiveLocal();
LAB_00df43b8:
  DataMemoryBarrier(2,3);
LAB_00df43bc:
  if (*(int *)(param_1 + 0xd8) == 0) {
    return;
  }
  uVar10 = FUN_00e3234c();
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar10,0);
}



// ==========================================================================================
// Function: thunk_FUN_00e11b18
// Address: 00db0cc4
// ==========================================================================================

long * thunk_FUN_00e11b18(long *param_1,long param_2)

{
  int iVar1;
  ulong uVar2;
  long lVar3;
  long *plStack_28;
  
  if (param_1 != (long *)0x0) {
    lVar3 = *param_1;
    uVar2 = FUN_00dfd720(param_2,lVar3);
    if ((uVar2 & 1) == 0) {
      if ((*(byte *)(lVar3 + 0x136) >> 4 & 1) == 0) {
        param_1 = (long *)0x0;
      }
      else {
        if (((((*(byte *)(param_2 + 0x118) >> 5 & 1) != 0) || (*(char *)(param_2 + 0x2a) == '\x1e'))
            || (*(char *)(param_2 + 0x2a) == '\x13')) &&
           ((*(long *)(param_2 + 0x70) != 0 &&
            (lVar3 = *(long *)(*(long *)(param_2 + 0x70) + 0x28), lVar3 != 0)))) {
          plStack_28 = (long *)FUN_00e2ba24(param_1,lVar3);
          if (plStack_28 != (long *)0x0) {
            return param_1;
          }
          iVar1 = (***(code ***)(undefined8 *)param_1[2])
                            ((undefined8 *)param_1[2],lVar3,&plStack_28);
          if (-1 < iVar1) {
            uVar2 = FUN_00e2bab4(param_1,lVar3,plStack_28);
            if ((uVar2 & 1) == 0) {
              (**(code **)(*plStack_28 + 0x10))(plStack_28);
              plStack_28 = (long *)FUN_00e2ba24(param_1,lVar3);
            }
            if (plStack_28 != (long *)0x0) {
              return param_1;
            }
          }
        }
        if (*(long *)(PTR_DAT_01ff5418 + 0x10) != param_2) {
          param_1 = (long *)0x0;
        }
      }
    }
  }
  return param_1;
}



// ==========================================================================================
// Function: thunk_FUN_00e11868
// Address: 00db0cc8
// ==========================================================================================

long thunk_FUN_00e11868(long param_1,long *param_2)

{
  bool bVar1;
  int iVar2;
  size_t __n;
  long lVar3;
  
  if (*(int *)(param_1 + 0x28) < 0) {
    if ((*(long *)(param_1 + 0x60) == 0) || ((*(byte *)(param_1 + 0x135) >> 3 & 1) == 0)) {
      bVar1 = false;
    }
    else {
      if (*(char *)param_2 == '\0') {
        return 0;
      }
      bVar1 = true;
    }
    lVar3 = FUN_00e11c14(param_1);
    iVar2 = FUN_00dfcff8(param_1);
    __n = (long)iVar2 - 0x10;
    if (bVar1) {
      iVar2 = *(int *)(*(long *)(param_1 + 0x80) + 0x38) + -0x10;
      param_2 = (long *)((long)param_2 + (long)iVar2);
      __n = __n - (long)iVar2;
    }
    memcpy((void *)(lVar3 + 0x10),param_2,__n);
  }
  else {
    lVar3 = *param_2;
  }
  return lVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e11d68
// Address: 00db0ccc
// ==========================================================================================

long thunk_FUN_00e11d68(long param_1)

{
  return param_1 + 0x10;
}



// ==========================================================================================
// Function: thunk_FUN_00e11d70
// Address: 00db0cd0
// ==========================================================================================

void thunk_FUN_00e11d70(long param_1,long param_2,undefined8 param_3)

{
  uint uVar1;
  void *__s;
  
  __s = (void *)FUN_00df4668(param_3,*(long *)(param_2 + 0x80) + 0x20);
  uVar1 = *(int *)(*(long *)(param_2 + 0x40) + 0xf8) - 0x10;
  if (param_1 == 0) {
    memset(__s,0,(ulong)uVar1);
  }
  else {
    memcpy(__s,(void *)(param_1 + 0x10),(ulong)uVar1);
  }
  *(bool *)param_3 = param_1 != 0;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e11c14
// Address: 00db0dd4
// ==========================================================================================

long * thunk_FUN_00e11c14(long param_1)

{
  char cVar1;
  bool bVar2;
  undefined *puVar3;
  long *plVar4;
  
  FUN_00dfcccc();
  if ((*(long *)(param_1 + 0x60) != 0) && ((*(byte *)(param_1 + 0x135) >> 3 & 1) != 0)) {
    param_1 = *(long *)(param_1 + 0x40);
  }
  if ((*(byte *)(param_1 + 0x135) >> 5 & 1) == 0) {
    plVar4 = (long *)FUN_00e11cf0(param_1);
  }
  else if (*(long *)(param_1 + 8) == 0) {
    plVar4 = (long *)FUN_00e3eaec(*(undefined4 *)(param_1 + 0xf8));
    *plVar4 = param_1;
    puVar3 = PTR_DAT_01ff5430;
    do {
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(puVar3,0x10);
      if (bVar2) {
        *(long *)puVar3 = *(long *)puVar3 + 1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
  }
  else {
    plVar4 = (long *)FUN_00e39958(*(undefined4 *)(param_1 + 0xf8),param_1);
    puVar3 = PTR_DAT_01ff5430;
    do {
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(puVar3,0x10);
      if (bVar2) {
        *(long *)puVar3 = *(long *)puVar3 + 1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
  }
  if ((*(byte *)(param_1 + 0x136) >> 1 & 1) != 0) {
    FUN_00e32cb0(plVar4);
  }
  if ((char)*PTR_DAT_01ff5438 < '\0') {
    FUN_00e2ae40(plVar4,param_1);
  }
  FUN_00df405c(param_1);
  return plVar4;
}



// ==========================================================================================
// Function: thunk_FUN_00e29584
// Address: 00db0e00
// ==========================================================================================

long thunk_FUN_00e29584(long param_1,undefined8 param_2)

{
  undefined8 uVar1;
  long lVar2;
  
  uVar1 = FUN_00deb760();
  lVar2 = FUN_00e294a4(uVar1,"System","ArgumentException",param_2);
  if (param_1 != 0) {
    uVar1 = FUN_00e0e65c(param_1);
    FUN_00e331f0(lVar2 + 0x90,uVar1);
  }
  return lVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00e295e0
// Address: 00db0e04
// ==========================================================================================

long thunk_FUN_00e295e0(long param_1)

{
  undefined8 uVar1;
  long lVar2;
  
  uVar1 = FUN_00deb760();
  lVar2 = FUN_00e294a4(uVar1,"System","ArgumentNullException",0);
  if (param_1 != 0) {
    uVar1 = FUN_00e0e65c(param_1);
    FUN_00e331f0(lVar2 + 0x90,uVar1);
  }
  return lVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00e29d2c
// Address: 00db0e08
// ==========================================================================================

void thunk_FUN_00e29d2c(void)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00deb760();
  FUN_00e294a4(uVar1,"System","ArrayTypeMismatchException",0);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e29dc8
// Address: 00db0e0c
// ==========================================================================================

void thunk_FUN_00e29dc8(undefined8 param_1)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00deb760();
  FUN_00e294a4(uVar1,"System","InvalidOperationException",param_1);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e2819c
// Address: 00db0ef4
// ==========================================================================================

long thunk_FUN_00e2819c(undefined4 param_1,long param_2)

{
  int iVar1;
  long lVar2;
  void *__src;
  ulong uVar3;
  void *pvStack_38;
  undefined4 uStack_28;
  undefined4 uStack_24;
  
  if (param_2 == 0) {
    return 0;
  }
  uStack_28 = FUN_00debcc4(param_2);
  uStack_24 = 0;
  lVar2 = FUN_00dac34c(param_1,1,&uStack_28);
  if (lVar2 != 0) {
    iVar1 = FUN_00df7700(lVar2,&pvStack_38);
    if (-1 < iVar1) {
      __src = (void *)FUN_00de399c(param_2);
      uVar3 = FUN_00e111cc(param_2);
      memcpy(pvStack_38,__src,uVar3 & 0xffffffff);
      iVar1 = FUN_00dac730(lVar2);
      if (-1 < iVar1) {
        return lVar2;
      }
    }
    FUN_00dac730(lVar2);
                    /* WARNING: Subroutine does not return */
    FUN_00e28188(iVar1,1);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e28188(0x8007000e,1);
}



// ==========================================================================================
// Function: thunk_FUN_00e28260
// Address: 00db0ef8
// ==========================================================================================

undefined8 thunk_FUN_00e28260(short param_1,undefined8 param_2,long param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  void *__dest;
  ulong uVar4;
  void *pvStack_40;
  int iStack_34;
  int iStack_28;
  short asStack_24 [2];
  
  if (param_3 == 0) {
    return 0;
  }
  uVar2 = FUN_00df7710(param_3,asStack_24);
  if (-1 < (int)uVar2) {
    if ((asStack_24[0] == param_1) && (iVar1 = FUN_00da2754(param_3), iVar1 == 1)) {
      uVar2 = FUN_00df7720(param_3,1,&iStack_28);
      if ((-1 < (int)uVar2) && (uVar2 = FUN_00df7720(param_3,1,&iStack_34), -1 < (int)uVar2)) {
        uVar3 = FUN_00e11218(param_2,(long)((iStack_34 - iStack_28) + 1));
        uVar2 = FUN_00df7700(param_3,&pvStack_40);
        if (-1 < (int)uVar2) {
          __dest = (void *)FUN_00de399c(uVar3);
          uVar4 = FUN_00e111cc(uVar3);
          memcpy(__dest,pvStack_40,uVar4 & 0xffffffff);
          uVar2 = FUN_00dac730(param_3);
          if (-1 < (int)uVar2) {
            return uVar3;
          }
        }
      }
    }
    else {
      uVar2 = 0x80070057;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e28188(uVar2,1);
}



// ==========================================================================================
// Function: thunk_FUN_00e32ee4
// Address: 00db0f18
// ==========================================================================================

long * thunk_FUN_00e32ee4(long *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  ulong uVar2;
  long *plVar3;
  undefined8 *puVar4;
  undefined8 uStack_e8;
  long *plStack_e0;
  long lStack_d8;
  long lStack_d0;
  long lStack_c8;
  long lStack_c0;
  long lStack_b8;
  long lStack_b0;
  undefined8 uStack_a8;
  undefined4 auStack_98 [2];
  long *plStack_90;
  undefined8 *puStack_88;
  undefined uStack_80;
  undefined3 uStack_7b;
  undefined4 uStack_74;
  undefined auStack_70 [8];
  long lStack_68;
  long lStack_60;
  long lStack_58;
  long lStack_50;
  undefined auStack_28 [8];
  
  if (param_1 == (long *)0x0) {
    plVar3 = (long *)0x0;
  }
  else if ((*(byte *)(*param_1 + 0x136) >> 4 & 1) == 0) {
    FUN_00da6960(auStack_28,&DAT_02108c20);
    uStack_e8 = (long *)((ulong)uStack_e8._4_4_ << 0x20);
    plStack_e0 = param_1;
    FUN_00e34940(auStack_70,&DAT_02108c70,&uStack_e8);
    uStack_a8 = 0;
    uStack_e8 = (long *)&DAT_02108c70;
    plStack_e0 = (long *)DAT_02108cb0;
    lStack_d8 = DAT_02108cb8;
    lStack_d0 = DAT_02108cb8;
    lStack_c8 = 0;
    lStack_c0 = DAT_02108cb0;
    lStack_b8 = DAT_02108cb8;
    lStack_b0 = DAT_02108cb8;
    FUN_00e33b64(&uStack_e8);
    if (((((long *)lStack_68 == plStack_e0) && (lStack_60 == lStack_d8)) && (lStack_58 == lStack_d0)
        ) && ((lStack_58 == lStack_60 || (lStack_50 == lStack_c8)))) {
      puVar4 = (undefined8 *)FUN_00dce7e4(param_1);
      if ((*param_1 != *(long *)(PTR_DAT_01ff5418 + 0x2a0)) ||
         (*(long *)(PTR_DAT_01ff5418 + 0x290) == 0)) {
        FUN_00e3f01c(param_1,FUN_00e3313c,0,&uStack_e8,auStack_98);
        auStack_98[0] = 0;
        uStack_80 = uStack_e8 != (long *)0x0;
        uStack_7b = (undefined3)uStack_74;
        plStack_90 = param_1;
        puStack_88 = puVar4;
        FUN_00e34b90(&DAT_02108c70,1);
        FUN_00e34cd0(&uStack_e8,&DAT_02108c70,auStack_98);
      }
    }
    else {
      puVar4 = *(undefined8 **)(lStack_50 + 0x10);
    }
    uVar1 = (**(code **)*puVar4)(puVar4,param_2,&uStack_e8);
    plVar3 = uStack_e8;
    if ((int)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00e28188(uVar1,1);
    }
    FUN_00da71f4(auStack_28);
  }
  else {
    uStack_e8 = (long *)FUN_00e2ba24(param_1,param_2);
    plVar3 = uStack_e8;
    if (uStack_e8 == (long *)0x0) {
      uVar1 = (***(code ***)(undefined8 *)param_1[2])((undefined8 *)param_1[2],param_2,&uStack_e8);
      if ((int)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00e28188(uVar1,1);
      }
      uVar2 = FUN_00e2bab4(param_1,param_2,uStack_e8);
      plVar3 = uStack_e8;
      if ((uVar2 & 1) == 0) {
        (**(code **)(*uStack_e8 + 0x10))(uStack_e8);
        plVar3 = (long *)FUN_00e2ba24(param_1,param_2);
      }
    }
    (**(code **)(*plVar3 + 8))(plVar3);
  }
  return plVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e2b550
// Address: 00db0f1c
// ==========================================================================================

long thunk_FUN_00e2b550(undefined8 *param_1,long param_2)

{
  int *piVar1;
  char cVar2;
  bool bVar3;
  long *plVar4;
  int iVar5;
  long lVar6;
  undefined8 uVar7;
  long lVar8;
  undefined4 auStack_120 [2];
  long *plStack_118;
  undefined4 uStack_110;
  undefined8 uStack_108;
  long *plStack_100;
  void *pvStack_f8;
  void *pvStack_f0;
  undefined8 uStack_e8;
  long *plStack_e0;
  void *pvStack_d8;
  void *pvStack_d0;
  undefined8 uStack_c8;
  undefined4 auStack_b8 [2];
  undefined4 uStack_b0;
  basic_string abStack_a8 [16];
  void *pvStack_98;
  undefined4 uStack_90;
  undefined auStack_88 [8];
  long *plStack_80;
  void *pvStack_78;
  void *pvStack_70;
  long lStack_68;
  undefined auStack_38 [8];
  
  iVar5 = (**(code **)*param_1)(param_1,&DAT_008161f4,&uStack_108);
  if (-1 < iVar5) {
    lVar6 = (**(code **)(*uStack_108 + 0x18))();
    (**(code **)(*uStack_108 + 0x10))(uStack_108);
    return lVar6;
  }
  uVar7 = (**(code **)*param_1)(param_1,&DAT_008161d4,&uStack_108);
  plVar4 = uStack_108;
  if ((int)uVar7 < 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e28188(uVar7,1);
  }
  FUN_00da6960(auStack_38,&DAT_02108970);
  uStack_108 = (long *)((ulong)uStack_108 & 0xffffffff00000000);
  plStack_100 = plVar4;
  FUN_00e02c6c(auStack_88,&DAT_021089c0,&uStack_108);
  uStack_c8 = 0;
  uStack_108 = &DAT_021089c0;
  plStack_100 = DAT_02108a00;
  pvStack_f8 = DAT_02108a08;
  pvStack_f0 = DAT_02108a08;
  uStack_e8 = 0;
  plStack_e0 = DAT_02108a00;
  pvStack_d8 = DAT_02108a08;
  pvStack_d0 = DAT_02108a08;
  FUN_00dd5a44(&uStack_108);
  if ((((plStack_80 != plStack_100) || (pvStack_78 != pvStack_f8)) || (pvStack_70 != pvStack_f0)) ||
     ((pvStack_70 != pvStack_78 && (lStack_68 != uStack_e8)))) {
    lVar6 = FUN_00e3234c(*(undefined4 *)(lStack_68 + 0x10));
    if (lVar6 != 0) {
      piVar1 = (int *)(lVar6 + 0xac);
      do {
        iVar5 = *piVar1;
        cVar2 = '\x01';
        bVar3 = (bool)ExclusiveMonitorPass(piVar1,0x10);
        if (bVar3) {
          *piVar1 = iVar5 + 1;
          cVar2 = ExclusiveMonitorsStatus();
        }
      } while (cVar2 != '\0');
      DataMemoryBarrier(2,3);
      if (1 < iVar5 + 1) {
        (**(code **)(*plVar4 + 0x10))(plVar4);
        goto LAB_00e2b7e4;
      }
    }
    memcpy(&uStack_108,auStack_88,0x48);
    FUN_00e2d06c(&DAT_021089c0,&uStack_108);
  }
  iVar5 = (**(code **)*param_1)(param_1,&DAT_00816204,&uStack_108);
  lVar8 = param_2;
  if (-1 < iVar5) {
    lVar8 = FUN_00e2cf2c(uStack_108,param_2);
    (**(code **)(*uStack_108 + 0x10))();
  }
  lVar6 = FUN_00e2b194(param_1,lVar8);
  if (lVar6 == 0) {
    if (((*(char *)(lVar8 + 0x2a) != '\x12') || ((*(byte *)(lVar8 + 0x118) >> 5 & 1) != 0)) ||
       ((*(byte *)(lVar8 + 0x135) >> 4 & 1) != 0)) {
      lVar8 = param_2;
    }
    lVar6 = thunk_FUN_00e11c14(lVar8);
    *(long **)(lVar6 + 0x10) = plVar4;
    *(undefined4 *)(lVar6 + 0xac) = 1;
    FUN_00e32284(auStack_b8,lVar6,0);
    uStack_108 = (long *)CONCAT44(uStack_108._4_4_,uStack_b0);
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    basic_string((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
                 &plStack_100,abStack_a8);
    uStack_e8 = CONCAT44(uStack_e8._4_4_,uStack_90);
    iVar5 = FUN_00daf844(&uStack_108);
    if (iVar5 != 0) {
      uVar7 = FUN_00e28b9c(&uStack_108);
      if (((byte)abStack_a8[0] & 1) != 0) {
        operator_delete(pvStack_98);
      }
      FUN_00da71f4(auStack_38);
                    /* WARNING: Subroutine does not return */
      FUN_00ead3e8(uVar7);
    }
    if (((ulong)plStack_100 & 1) != 0) {
      operator_delete(pvStack_f0);
    }
    auStack_120[0] = 0;
    plStack_118 = plVar4;
    uStack_110 = auStack_b8[0];
    FUN_00e2cd38(&DAT_021089c0,1);
    FUN_00e08f74(&uStack_108,&DAT_021089c0,auStack_120);
    if (((byte)abStack_a8[0] & 1) != 0) {
      operator_delete(pvStack_98);
    }
  }
LAB_00e2b7e4:
  FUN_00da71f4(auStack_38);
  return lVar6;
}



// ==========================================================================================
// Function: thunk_FUN_00e2b894
// Address: 00db0fd8
// ==========================================================================================

void thunk_FUN_00e2b894(long *param_1)

{
  uint uVar1;
  long *plVar2;
  ulong uVar3;
  long lVar4;
  long **pplVar5;
  undefined auStack_b8 [8];
  long lStack_b0;
  long lStack_a8;
  long lStack_a0;
  long lStack_98;
  undefined auStack_70 [8];
  undefined8 *puStack_68;
  long lStack_60;
  long lStack_58;
  long lStack_50;
  long lStack_48;
  long lStack_40;
  long lStack_38;
  long lStack_30;
  undefined8 uStack_28;
  
  if ((*(byte *)(*param_1 + 0x136) >> 4 & 1) != 0) {
    FUN_00da6960(auStack_70,&DAT_02108970);
    puStack_68 = (undefined8 *)((ulong)puStack_68 & 0xffffffff00000000);
    lStack_60 = param_1[2];
    FUN_00e02c6c(auStack_b8,&DAT_021089c0,&puStack_68);
    uStack_28 = 0;
    puStack_68 = &DAT_021089c0;
    lStack_60 = DAT_02108a00;
    lStack_58 = DAT_02108a08;
    lStack_50 = DAT_02108a08;
    lStack_48 = 0;
    lStack_40 = DAT_02108a00;
    lStack_38 = DAT_02108a08;
    lStack_30 = DAT_02108a08;
    FUN_00dd5a44(&puStack_68);
    if (((((lStack_b0 != lStack_60) || (lStack_a8 != lStack_58)) || (lStack_a0 != lStack_50)) ||
        ((lStack_a0 != lStack_a8 && (lStack_98 != lStack_48)))) &&
       ((plVar2 = (long *)FUN_00e3234c(*(undefined4 *)(lStack_98 + 0x10)), plVar2 == (long *)0x0 ||
        (plVar2 == param_1)))) {
      memcpy(&puStack_68,auStack_b8,0x48);
      FUN_00e2d06c(&DAT_021089c0,&puStack_68);
    }
    FUN_00da71f4(auStack_70);
  }
  uVar3 = (ulong)*(uint *)(param_1 + 0x14);
  if (0 < (int)*(uint *)(param_1 + 0x14)) {
    pplVar5 = (long **)(param_1 + 4);
    do {
      (**(code **)(**pplVar5 + 0x10))();
      uVar3 = uVar3 - 1;
      pplVar5 = pplVar5 + 2;
    } while (uVar3 != 0);
  }
  uVar1 = *(uint *)((long)param_1 + 0xa4);
  if (0 < (int)uVar1) {
    lVar4 = 0;
    do {
      (**(code **)(**(long **)(param_1[0x13] + lVar4 + 8) + 0x10))();
      lVar4 = lVar4 + 0x10;
    } while ((ulong)uVar1 * 0x10 - lVar4 != 0);
    free((void *)param_1[0x13]);
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dfd720
// Address: 00db1210
// ==========================================================================================

bool thunk_FUN_00dfd720(long param_1,long param_2)

{
  undefined *puVar1;
  bool bVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  long lVar6;
  long *plVar7;
  long lVar8;
  
  puVar1 = PTR_DAT_01ff5418;
  do {
    bVar2 = param_1 == param_2;
    if (bVar2) {
      return true;
    }
    while( true ) {
      FUN_00dfcccc(param_1);
      FUN_00dfcccc(param_2);
      if ((((*(byte *)(param_1 + 0x118) >> 5 & 1) != 0) || (*(char *)(param_1 + 0x2a) == '\x13')) ||
         (*(char *)(param_1 + 0x2a) == '\x1e')) {
        if (*(long *)(param_1 + 0x60) == 0) {
          if (param_2 == 0) {
            return false;
          }
          do {
            if ((ulong)*(ushort *)(param_2 + 300) != 0) {
              uVar4 = 0;
              do {
                if (*(long *)(*(long *)(param_2 + 0xa8) + uVar4 * 8) == param_1) {
                  return true;
                }
                uVar4 = uVar4 + 1;
              } while (uVar4 < *(ushort *)(param_2 + 300));
            }
            if ((ulong)*(ushort *)(param_2 + 0x12e) != 0) {
              plVar7 = *(long **)(param_2 + 0xb0);
              uVar4 = 0;
              do {
                if (*plVar7 == param_1) {
                  return true;
                }
                uVar4 = uVar4 + 1;
                plVar7 = plVar7 + 2;
              } while (uVar4 < *(ushort *)(param_2 + 0x12e));
            }
            param_2 = *(long *)(param_2 + 0x58);
          } while (param_2 != 0);
          return false;
        }
        lVar8 = param_2;
        if (param_2 == 0) {
          return false;
        }
        do {
          if ((lVar8 == param_1) || (uVar4 = FUN_00e01d10(param_1,lVar8,param_2), (uVar4 & 1) != 0))
          {
            return true;
          }
          if (*(short *)(lVar8 + 300) != 0) {
            uVar4 = 0;
            do {
              lVar5 = *(long *)(*(long *)(lVar8 + 0xa8) + uVar4 * 8);
              if (lVar5 == param_1) {
                return true;
              }
              uVar3 = FUN_00e01d10(param_1,lVar5,param_2);
              if ((uVar3 & 1) != 0) {
                return true;
              }
              uVar4 = uVar4 + 1;
            } while (uVar4 < *(ushort *)(lVar8 + 300));
          }
          if (*(short *)(lVar8 + 0x12e) != 0) {
            lVar5 = 0;
            uVar4 = 0;
            do {
              lVar6 = *(long *)(*(long *)(lVar8 + 0xb0) + lVar5);
              if (lVar6 == param_1) {
                return true;
              }
              uVar3 = FUN_00e01d10(param_1,lVar6,param_2);
              if ((uVar3 & 1) != 0) {
                return true;
              }
              uVar4 = uVar4 + 1;
              lVar5 = lVar5 + 0x10;
            } while (uVar4 < *(ushort *)(lVar8 + 0x12e));
          }
          plVar7 = (long *)(lVar8 + 0x58);
          lVar8 = *plVar7;
          if (*plVar7 == 0) {
            return false;
          }
        } while( true );
      }
      if (*(char *)(param_1 + 0x132) != '\0') break;
      if (*(long *)(puVar1 + 0x10) == param_1) {
        return true;
      }
      if (*(long *)(param_1 + 0x60) == 0) {
LAB_00dfd91c:
        if (*(byte *)(param_2 + 0x130) < *(byte *)(param_1 + 0x130)) {
          return false;
        }
        return *(long *)(*(long *)(param_2 + 200) + (ulong)*(byte *)(param_1 + 0x130) * 8 + -8) ==
               param_1;
      }
      if ((*(byte *)(param_1 + 0x135) >> 3 & 1) == 0) {
        if ((*(long *)(param_1 + 0x58) == *(long *)(puVar1 + 0xb0)) &&
           (uVar4 = FUN_00e01d10(param_1,param_2,param_2), (uVar4 & 1) != 0)) {
          return true;
        }
        goto LAB_00dfd91c;
      }
      param_1 = *(long *)(param_1 + 0x40);
      if (param_1 == param_2) {
        return true;
      }
    }
    if (*(char *)(param_2 + 0x132) != *(char *)(param_1 + 0x132)) {
      return bVar2;
    }
    param_2 = *(long *)(param_2 + 0x48);
    param_1 = *(long *)(param_1 + 0x48);
    if (*(int *)(param_2 + 0x28) < 0) {
      return param_1 == param_2;
    }
  } while( true );
}



// ==========================================================================================
// Function: thunk_FUN_00e12178
// Address: 00db121c
// ==========================================================================================

char * thunk_FUN_00e12178(long param_1)

{
  ulong uVar1;
  char *__src;
  char *__dest;
  byte abStack_38 [8];
  ulong uStack_30;
  char *pcStack_28;
  
  if (param_1 == 0) {
    __dest = (char *)0x0;
  }
  else {
    FUN_00dc6cc0(abStack_38,param_1 + 0x14);
    uVar1 = (ulong)(abStack_38[0] >> 1);
    if ((abStack_38[0] & 1) != 0) {
      uVar1 = uStack_30;
    }
    __dest = (char *)malloc(uVar1 + 1);
    __src = (char *)((ulong)abStack_38 | 1);
    if ((abStack_38[0] & 1) != 0) {
      __src = pcStack_28;
    }
    strcpy(__dest,__src);
    if ((abStack_38[0] & 1) != 0) {
      operator_delete(pcStack_28);
    }
  }
  return __dest;
}



// ==========================================================================================
// Function: thunk_FUN_00dc5858
// Address: 00db1220
// ==========================================================================================

void thunk_FUN_00dc5858(long param_1)

{
  if (param_1 != 0) {
    FUN_00e0e65c();
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e12218
// Address: 00db1224
// ==========================================================================================

void thunk_FUN_00e12218(short *param_1)

{
  long lVar1;
  long lVar2;
  
  if (param_1 == (short *)0x0) {
    return;
  }
  if (*param_1 != 0) {
    lVar2 = 0;
    do {
      lVar1 = lVar2 + 1;
      lVar2 = lVar2 + 1;
    } while (param_1[lVar1] != 0);
    FUN_00e0e70c();
    return;
  }
  FUN_00e0e70c(param_1,0);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e1216c
// Address: 00db1228
// ==========================================================================================

void thunk_FUN_00e1216c(void *param_1)

{
  if (param_1 != (void *)0x0) {
    free(param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e12248
// Address: 00db122c
// ==========================================================================================

void thunk_FUN_00e12248(long param_1)

{
  undefined *puVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  ulong *puVar5;
  char *pcVar6;
  uint uVar7;
  uint uVar8;
  long *plVar9;
  __ndk1 a_Stack_118 [16];
  void *pvStack_108;
  ulong uStack_100;
  ulong uStack_f8;
  void *pvStack_f0;
  ulong uStack_e0;
  ulong uStack_d8;
  void *pvStack_d0;
  ulong uStack_c0;
  ulong uStack_b8;
  char *pcStack_b0;
  __ndk1 a_Stack_a8 [8];
  ulong uStack_a0;
  char *pcStack_98;
  ulong uStack_90;
  ulong uStack_88;
  char *pcStack_80;
  ulong uStack_70;
  ulong uStack_68;
  void *pvStack_60;
  ulong uStack_50;
  ulong uStack_48;
  ulong uStack_40;
  undefined auStack_38 [24];
  
  if (((param_1 == 0) || (*(long *)(param_1 + 0x30) != 0)) ||
     (lVar2 = FUN_00e017a4(**(undefined8 **)(*(long *)(param_1 + 0x28) + 0x20)), lVar2 != 0)) {
    return;
  }
  FUN_00dd1810(auStack_38,*(undefined8 *)(param_1 + 0x28));
  uVar3 = FUN_00dd15e4(*(undefined8 *)(param_1 + 0x28));
  if ((uVar3 & 1) != 0) {
    std::__ndk1::operator+
              ((__ndk1 *)&uStack_50,
               "IL2CPP does not support marshaling delegates that point to instance methods to native code. The method we\'re attempting to marshal is: "
               ,auStack_38);
    uVar3 = (ulong)&uStack_50 | 1;
    if (((byte)uStack_50 & 1) != 0) {
      uVar3 = uStack_40;
    }
    uVar4 = FUN_00e29d04(uVar3);
                    /* WARNING: Subroutine does not return */
    FUN_00e28a74(uVar4,0);
  }
  uVar3 = FUN_00dd1958(*(undefined8 *)(param_1 + 0x28));
  if ((uVar3 & 1) != 0) {
    std::__ndk1::operator+
              ((__ndk1 *)&uStack_50,
               "IL2CPP does not support marshaling generic delegates when full generic sharing is enabled. The method we\'re attempting to marshal is: "
               ,auStack_38);
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_50,
           "\nTo marshal this delegate, please add an attribute named \'MonoPInvokeCallback\' to the method definition."
          );
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_50,
           "\nThis attribute should have a type argument which is a generic delegate with all of the types required for this generic instantiation:"
          );
    FUN_00e12894(&uStack_70,*(undefined8 *)(*(long *)(*(long *)(param_1 + 0x28) + 0x40) + 8));
    uVar3 = uStack_70 >> 1 & 0x7f;
    if ((uStack_70 & 1) != 0) {
      uVar3 = uStack_68;
    }
    if (uVar3 != 0) {
      std::__ndk1::operator+((__ndk1 *)&uStack_90,"\nGeneric type arguments: ",&uStack_70);
      uVar3 = uStack_90 >> 1 & 0x7f;
      pcVar6 = (char *)((ulong)&uStack_90 | 1);
      if ((uStack_90 & 1) != 0) {
        uVar3 = uStack_88;
        pcVar6 = pcStack_80;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,pcVar6,uVar3);
      if ((uStack_90 & 1) != 0) {
        operator_delete(pcStack_80);
      }
    }
    FUN_00e12894(&uStack_90,*(undefined8 *)(*(long *)(*(long *)(param_1 + 0x28) + 0x40) + 0x10));
    uVar3 = uStack_90 >> 1 & 0x7f;
    if ((uStack_90 & 1) != 0) {
      uVar3 = uStack_88;
    }
    if (uVar3 != 0) {
      std::__ndk1::operator+(a_Stack_a8,"\nGeneric method arguments: ",&uStack_90);
      uVar3 = (ulong)((byte)a_Stack_a8[0] >> 1);
      pcVar6 = (char *)((ulong)a_Stack_a8 | 1);
      if (((byte)a_Stack_a8[0] & 1) != 0) {
        uVar3 = uStack_a0;
        pcVar6 = pcStack_98;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,pcVar6,uVar3);
      if (((byte)a_Stack_a8[0] & 1) != 0) {
        operator_delete(pcStack_98);
      }
    }
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_50,"\nThis C# code should work, for example:");
    uVar3 = (ulong)((byte)uStack_70 >> 1);
    if (((byte)uStack_70 & 1) != 0) {
      uVar3 = uStack_68;
    }
    puVar1 = &DAT_005d824c;
    if (uVar3 != 0) {
      puVar1 = &DAT_005d743a;
    }
    FUN_00d9e440(a_Stack_a8,puVar1);
    std::__ndk1::operator+(a_Stack_118,"\n[MonoPInvokeCallback(typeof(System.Action<",&uStack_70);
    uVar3 = (ulong)((byte)a_Stack_a8[0] >> 1);
    pcVar6 = (char *)((ulong)a_Stack_a8 | 1);
    if (((byte)a_Stack_a8[0] & 1) != 0) {
      uVar3 = uStack_a0;
      pcVar6 = pcStack_98;
    }
    puVar5 = (ulong *)std::__ndk1::
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                *)a_Stack_118,pcVar6,uVar3);
    pvStack_f0 = (void *)puVar5[2];
    uStack_f8 = puVar5[1];
    uStack_100 = *puVar5;
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    uVar3 = (ulong)((byte)uStack_90 >> 1);
    pcVar6 = (char *)((ulong)&uStack_90 | 1);
    if (((byte)uStack_90 & 1) != 0) {
      uVar3 = uStack_88;
      pcVar6 = pcStack_80;
    }
    puVar5 = (ulong *)std::__ndk1::
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                *)&uStack_100,pcVar6,uVar3);
    pvStack_d0 = (void *)puVar5[2];
    uStack_d8 = puVar5[1];
    uStack_e0 = *puVar5;
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    puVar5 = (ulong *)std::__ndk1::
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                *)&uStack_e0,">))]");
    pcStack_b0 = (char *)puVar5[2];
    uStack_b8 = puVar5[1];
    uStack_c0 = *puVar5;
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    uVar3 = uStack_c0 >> 1 & 0x7f;
    pcVar6 = (char *)((ulong)&uStack_c0 | 1);
    if ((uStack_c0 & 1) != 0) {
      uVar3 = uStack_b8;
      pcVar6 = pcStack_b0;
    }
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_50,pcVar6,uVar3);
    if ((uStack_c0 & 1) != 0) {
      operator_delete(pcStack_b0);
    }
    if ((uStack_e0 & 1) != 0) {
      operator_delete(pvStack_d0);
    }
    if ((uStack_100 & 1) != 0) {
      operator_delete(pvStack_f0);
    }
    if (((byte)a_Stack_118[0] & 1) != 0) {
      operator_delete(pvStack_108);
    }
    uVar3 = (ulong)&uStack_50 | 1;
    if (((byte)uStack_50 & 1) != 0) {
      uVar3 = uStack_40;
    }
    uVar4 = FUN_00e29d04(uVar3);
                    /* WARNING: Subroutine does not return */
    FUN_00e28a74(uVar4,0);
  }
  lVar2 = *(long *)(*(long *)(param_1 + 0x28) + 0x30);
  if ((lVar2 != 0) && (uVar7 = (uint)*(byte *)(*(long *)(param_1 + 0x28) + 0x52), uVar7 != 0)) {
    uVar8 = 0;
    do {
      plVar9 = *(long **)(lVar2 + (long)(int)uVar8 * 8);
      while( true ) {
        if ((*(uint *)(plVar9 + 1) & 0xff0000) == 0x150000) {
          std::__ndk1::operator+(a_Stack_a8,"Cannot marshal method \'",auStack_38);
          puVar5 = (ulong *)std::__ndk1::
                            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                            ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                      *)a_Stack_a8,"\' parameter \'");
          pcStack_80 = (char *)puVar5[2];
          uStack_88 = puVar5[1];
          uStack_90 = *puVar5;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *puVar5 = 0;
          pcVar6 = (char *)FUN_00dd161c(*(undefined8 *)(param_1 + 0x28),uVar8);
          puVar5 = (ulong *)std::__ndk1::
                            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                            ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                      *)&uStack_90,pcVar6);
          pvStack_60 = (void *)puVar5[2];
          uStack_68 = puVar5[1];
          uStack_70 = *puVar5;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *puVar5 = 0;
          puVar5 = (ulong *)std::__ndk1::
                            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                            ::append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                      *)&uStack_70,"\': Generic types cannot be marshaled.");
          uStack_40 = puVar5[2];
          uStack_48 = puVar5[1];
          uStack_50 = *puVar5;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *puVar5 = 0;
          if ((uStack_70 & 1) != 0) {
            operator_delete(pvStack_60);
          }
          if ((uStack_90 & 1) != 0) {
            operator_delete(pcStack_80);
          }
          if (((byte)a_Stack_a8[0] & 1) != 0) {
            operator_delete(pcStack_98);
          }
          uVar3 = (ulong)&uStack_50 | 1;
          if ((uStack_50 & 1) != 0) {
            uVar3 = uStack_40;
          }
          uVar4 = FUN_00e29e88(uVar3);
                    /* WARNING: Subroutine does not return */
          FUN_00e28a74(uVar4,0);
        }
        if ((*(uint *)(plVar9 + 1) & 0xff0000) != 0x1d0000) break;
        plVar9 = (long *)*plVar9;
      }
      uVar8 = uVar8 + 1;
    } while (uVar8 < uVar7);
  }
  std::__ndk1::operator+
            ((__ndk1 *)&uStack_50,
             "To marshal a managed method, please add an attribute named \'MonoPInvokeCallback\' to the method definition. The method we\'re attempting to marshal is: "
             ,auStack_38);
  uVar3 = (ulong)&uStack_50 | 1;
  if (((byte)uStack_50 & 1) != 0) {
    uVar3 = uStack_40;
  }
  uVar4 = FUN_00e29d04(uVar3);
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar4,0);
}



// ==========================================================================================
// Function: thunk_FUN_00e1299c
// Address: 00db1230
// ==========================================================================================

long thunk_FUN_00e1299c(long param_1,long param_2)

{
  ulong uVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 uVar4;
  long lVar5;
  byte abStack_48 [16];
  ulong uStack_38;
  
  if (param_1 == 0) {
    lVar3 = 0;
  }
  else {
    uVar1 = FUN_00dfd678(param_2,*(undefined8 *)(PTR_DAT_01ff5418 + 0xa8));
    if ((uVar1 & 1) == 0) {
      uVar2 = FUN_00e29584(&DAT_005c24d4,"Type must derive from Delegate.");
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(uVar2,0);
    }
    if ((*(long **)(param_2 + 0x70) == (long *)0x0) ||
       (lVar5 = **(long **)(param_2 + 0x70), lVar5 == 0)) {
      uVar2 = FUN_00dd1408(param_2);
      uVar4 = FUN_00deb060(param_2);
      FUN_00dc6ac4(abStack_48,"Cannot marshal P/Invoke call through delegate of type \'%s.%s\'",
                   uVar2,uVar4);
      uVar1 = (ulong)abStack_48 | 1;
      if ((abStack_48[0] & 1) != 0) {
        uVar1 = uStack_38;
      }
      uVar2 = FUN_00e29e88(uVar1);
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(uVar2,0);
    }
    uVar2 = FUN_00df5d58(param_2);
    lVar3 = FUN_00e11c14(param_2);
    FUN_00def650(lVar3,lVar3,lVar5,uVar2);
    *(long *)(lVar3 + 0x30) = param_1;
  }
  return lVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e11e58
// Address: 00db1234
// ==========================================================================================

long thunk_FUN_00e11e58(undefined8 *param_1)

{
  void *pvVar1;
  char *pcVar2;
  long lVar3;
  ulong uVar4;
  undefined8 uVar5;
  byte abStack_80 [8];
  ulong uStack_78;
  char *pcStack_70;
  ulong uStack_68;
  ulong uStack_60;
  char *pcStack_58;
  ulong uStack_50;
  ulong uStack_48;
  char *pcStack_40;
  ulong uStack_38;
  ulong uStack_30;
  char *pcStack_28;
  
  lVar3 = FUN_00dca98c(param_1,param_1 + 2,*(undefined4 *)((long)param_1 + 0x24));
  if (lVar3 == 0) {
    uStack_38 = 0;
    uStack_30 = 0;
    pcStack_28 = (char *)0x0;
    FUN_00d9e440(&uStack_50,*param_1);
    pvVar1 = (void *)((ulong)&uStack_50 | 1);
    if ((uStack_50 & 1) != 0) {
      pvVar1 = pcStack_40;
    }
    uVar4 = FUN_00dc9c0c(pvVar1,"__InternalDynamic");
    if (((byte)uStack_50 & 1) != 0) {
      operator_delete(pcStack_40);
    }
    if ((uVar4 & 1) == 0) {
      lVar3 = FUN_00dcab4c(*param_1,param_1[1],&uStack_38);
    }
    else {
      lVar3 = FUN_00dcab4c(0,0,&uStack_38);
    }
    if (lVar3 == -100) {
      uStack_50 = 0;
      uStack_48 = 0;
      pcStack_40 = (char *)0x0;
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,"Unable to load DLL \'");
      FUN_00d9e440(&uStack_68,*param_1);
      uVar4 = (ulong)((byte)uStack_68 >> 1);
      pcVar2 = (char *)((ulong)&uStack_68 | 1);
      if ((uStack_68 & 1) != 0) {
        uVar4 = uStack_60;
        pcVar2 = pcStack_58;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,pcVar2,uVar4);
      if (((byte)uStack_68 & 1) != 0) {
        operator_delete(pcStack_58);
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,"\'. Tried the load the following dynamic libraries: ");
      uVar4 = uStack_38 >> 1 & 0x7f;
      pcVar2 = (char *)((ulong)&uStack_38 | 1);
      if ((uStack_38 & 1) != 0) {
        uVar4 = uStack_30;
        pcVar2 = pcStack_28;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_50,pcVar2,uVar4);
      uVar4 = (ulong)&uStack_50 | 1;
      if ((uStack_50 & 1) != 0) {
        uVar4 = (ulong)pcStack_40;
      }
      uVar5 = FUN_00e29da0(uVar4);
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(uVar5,0);
    }
    uStack_50 = 0;
    uStack_48 = 0;
    pcStack_40 = (char *)0x0;
    lVar3 = FUN_00dcae44(lVar3,param_1,&uStack_50);
    if (lVar3 == 0) {
      uStack_68 = 0;
      uStack_60 = 0;
      pcStack_58 = (char *)0x0;
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,"Unable to find an entry point named \'");
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,(char *)param_1[2]);
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,"\' in \'");
      FUN_00d9e440(abStack_80,*param_1);
      uVar4 = (ulong)(abStack_80[0] >> 1);
      pcVar2 = (char *)((ulong)abStack_80 | 1);
      if ((abStack_80[0] & 1) != 0) {
        uVar4 = uStack_78;
        pcVar2 = pcStack_70;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,pcVar2,uVar4);
      if ((abStack_80[0] & 1) != 0) {
        operator_delete(pcStack_70);
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,"\'. Tried the following entry points: ");
      uVar4 = uStack_50 >> 1 & 0x7f;
      pcVar2 = (char *)((ulong)&uStack_50 | 1);
      if ((uStack_50 & 1) != 0) {
        uVar4 = uStack_48;
        pcVar2 = pcStack_40;
      }
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_68,pcVar2,uVar4);
      uVar4 = (ulong)&uStack_68 | 1;
      if ((uStack_68 & 1) != 0) {
        uVar4 = (ulong)pcStack_58;
      }
      uVar5 = FUN_00e29d50(uVar4);
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(uVar5,0);
    }
    if ((uStack_50 & 1) != 0) {
      operator_delete(pcStack_40);
    }
    if ((uStack_38 & 1) != 0) {
      operator_delete(pcStack_28);
    }
  }
  return lVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00e324f8
// Address: 00dc56f0
// ==========================================================================================

void thunk_FUN_00e324f8(uint param_1)

{
  long lVar1;
  long *plVar2;
  uint uVar3;
  uint uVar4;
  char cVar5;
  bool bVar6;
  uint uVar7;
  ulong uVar8;
  int iVar9;
  pthread_t pVar10;
  long lVar11;
  int iVar12;
  
  uVar7 = (param_1 & 7) - 1;
  if (uVar7 < 4) {
    uVar4 = param_1 >> 3;
    pVar10 = pthread_self();
    if (pVar10 == DAT_02108c10) {
      DAT_02108c18 = DAT_02108c18 + 1;
    }
    else {
      iVar12 = 0;
      do {
        iVar9 = DAT_02108bd0;
        if (DAT_02108bd0 == iVar12) {
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar6) {
            cVar5 = ExclusiveMonitorsStatus();
            DAT_02108bd0 = iVar12 + 1;
          }
          if (cVar5 != '\0') goto LAB_00e32570;
          bVar6 = true;
        }
        else {
          ClearExclusiveLocal();
LAB_00e32570:
          bVar6 = false;
        }
      } while ((iVar9 != 2) && (iVar12 = iVar9, !bVar6));
      while (iVar9 != 0) {
        FUN_00e4d8f8(&DAT_02108bd0,2,0xffffffff);
        do {
          iVar9 = DAT_02108bd0;
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar6) {
            DAT_02108bd0 = 2;
            cVar5 = ExclusiveMonitorsStatus();
          }
        } while (cVar5 != '\0');
      }
      DAT_02108c18 = 1;
      DAT_02108c10 = pVar10;
    }
    lVar11 = (ulong)uVar7 * 0x20;
    if (uVar4 < *(uint *)(&DAT_020ff0e8 + lVar11)) {
      uVar8 = (ulong)(param_1 >> 8);
      uVar3 = 1 << (ulong)(uVar4 & 0x1f);
      if ((*(uint *)(*(long *)(&DAT_020ff0d8 + lVar11) + uVar8 * 4) & uVar3) != 0) {
        lVar1 = (ulong)uVar7 * 0x20;
        plVar2 = (long *)(*(long *)(&DAT_020ff0e0 + lVar1) + (ulong)uVar4 * 8);
        if ((byte)(&DAT_020ff0ec)[lVar1] < 2) {
          if (*plVar2 != 0) {
            FUN_00e31c9c();
          }
        }
        else {
          *plVar2 = 0;
        }
        lVar11 = *(long *)(&DAT_020ff0d8 + lVar11);
        *(uint *)(lVar11 + uVar8 * 4) = *(uint *)(lVar11 + uVar8 * 4) & (uVar3 ^ 0xffffffff);
      }
    }
    iVar12 = DAT_02108c18 + -1;
    if ((0 < DAT_02108c18) && (DAT_02108c18 = iVar12, iVar12 == 0)) {
      DAT_02108c10 = 0;
      DAT_02108c18 = 0;
      do {
        iVar12 = DAT_02108bd0;
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
        if (bVar6) {
          DAT_02108bd0 = 0;
          cVar5 = ExclusiveMonitorsStatus();
        }
      } while (cVar5 != '\0');
      if (iVar12 == 2) {
        FUN_00e4d950(&DAT_02108bd0,1,0);
        return;
      }
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3234c
// Address: 00dc5754
// ==========================================================================================

long thunk_FUN_00e3234c(uint param_1)

{
  char cVar1;
  bool bVar2;
  uint uVar3;
  int iVar4;
  pthread_t pVar5;
  long lVar6;
  int iVar7;
  long lVar8;
  ulong uVar9;
  
  uVar3 = (param_1 & 7) - 1;
  uVar9 = (ulong)uVar3;
  if (uVar3 < 4) {
    uVar3 = param_1 >> 3;
    pVar5 = pthread_self();
    if (pVar5 == DAT_02108c10) {
      DAT_02108c18 = DAT_02108c18 + 1;
    }
    else {
      iVar7 = 0;
      do {
        iVar4 = DAT_02108bd0;
        if (DAT_02108bd0 == iVar7) {
          cVar1 = '\x01';
          bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar2) {
            cVar1 = ExclusiveMonitorsStatus();
            DAT_02108bd0 = iVar7 + 1;
          }
          if (cVar1 != '\0') goto LAB_00e323cc;
          bVar2 = true;
        }
        else {
          ClearExclusiveLocal();
LAB_00e323cc:
          bVar2 = false;
        }
      } while ((iVar4 != 2) && (iVar7 = iVar4, !bVar2));
      while (iVar4 != 0) {
        FUN_00e4d8f8(&DAT_02108bd0,2,0xffffffff);
        do {
          iVar4 = DAT_02108bd0;
          cVar1 = '\x01';
          bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar2) {
            DAT_02108bd0 = 2;
            cVar1 = ExclusiveMonitorsStatus();
          }
        } while (cVar1 != '\0');
      }
      DAT_02108c18 = 1;
      DAT_02108c10 = pVar5;
    }
    if ((uVar3 < *(uint *)(&DAT_020ff0e8 + uVar9 * 0x20)) &&
       ((*(uint *)(*(long *)(&DAT_020ff0d8 + uVar9 * 0x20) + (ulong)(param_1 >> 8) * 4) >>
         (ulong)(uVar3 & 0x1f) & 1) != 0)) {
      if ((byte)(&DAT_020ff0ec)[uVar9 * 0x20] < 2) {
        lVar6 = FUN_00e4433c(FUN_00e31cd8);
        lVar8 = 0;
        if (lVar6 != -1) {
          lVar8 = lVar6;
        }
      }
      else {
        lVar8 = *(long *)(*(long *)(&DAT_020ff0e0 + uVar9 * 0x20) + (ulong)uVar3 * 8);
      }
    }
    else {
      lVar8 = 0;
    }
    iVar7 = DAT_02108c18 + -1;
    if ((0 < DAT_02108c18) && (DAT_02108c18 = iVar7, iVar7 == 0)) {
      DAT_02108c10 = 0;
      DAT_02108c18 = 0;
      do {
        iVar7 = DAT_02108bd0;
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
        if (bVar2) {
          DAT_02108bd0 = 0;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
      if (iVar7 == 2) {
        FUN_00e4d950(&DAT_02108bd0,1,0);
      }
    }
  }
  else {
    lVar8 = 0;
  }
  return lVar8;
}



// ==========================================================================================
// Function: thunk_FUN_00db0efc
// Address: 00dc5854
// ==========================================================================================

void thunk_FUN_00db0efc(void)

{
  int iVar1;
  
  iVar1 = FUN_00dac730();
  if (-1 < iVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e28188(iVar1,1);
}



// ==========================================================================================
// Function: thunk_FUN_00dd0940
// Address: 00dc5c58
// ==========================================================================================

undefined4 thunk_FUN_00dd0940(void)

{
  uint uVar1;
  undefined4 uVar2;
  void *pvVar3;
  ulong uVar4;
  
  uVar4 = (ulong)DAT_020ff078;
  if (DAT_020ff078 == 0xffffffff) {
    uVar2 = 0;
  }
  else {
    uVar1 = DAT_020ff078 >> 0x10;
    pvVar3 = pthread_getspecific(*DAT_02107b08);
    uVar2 = **(undefined4 **)(*(long *)((long)pvVar3 + (ulong)uVar1 * 8) + (uVar4 & 0xffff) * 8);
  }
  return uVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00d9e330
// Address: 00dc6860
// ==========================================================================================

void thunk_FUN_00d9e330(void **param_1)

{
  if (*param_1 != (void *)0x0) {
    FUN_00d9e358();
    operator_delete(*param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcbacc
// Address: 00dca988
// ==========================================================================================

void thunk_FUN_00dcbacc(void **param_1)

{
  if (*param_1 != (void *)0x0) {
    FUN_00dcbaf4();
    operator_delete(*param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcb79c
// Address: 00dcb798
// ==========================================================================================

void * thunk_FUN_00dcb79c(void)

{
  void *__pointer;
  undefined8 uVar1;
  
  __pointer = pthread_getspecific(*DAT_02107878);
  if (__pointer == (void *)0x0) {
    __pointer = operator_new(0x28);
    uVar1 = FUN_00e2fb64();
    FUN_00dcb64c(__pointer,uVar1);
    pthread_setspecific(*DAT_02107878,__pointer);
  }
  return __pointer;
}



// ==========================================================================================
// Function: thunk_FUN_00e2f754
// Address: 00dcb964
// ==========================================================================================

undefined8 thunk_FUN_00e2f754(void)

{
  return 0x7fffffff;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fbb0
// Address: 00dcbab4
// ==========================================================================================

bool thunk_FUN_00e2fbb0(void)

{
  int iVar1;
  
  iVar1 = sched_yield();
  return iVar1 == 0;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fbc8
// Address: 00dcbab8
// ==========================================================================================

int thunk_FUN_00e2fbc8(long param_1)

{
  int iVar1;
  
  if (param_1 != 0) {
    DAT_02108af8 = param_1;
    iVar1 = pthread_key_create(&DAT_02108b00,FUN_00e2fc10);
    return iVar1;
  }
  iVar1 = pthread_key_delete(DAT_02108b00);
  DAT_02108af8 = 0;
  return iVar1;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fc24
// Address: 00dcbabc
// ==========================================================================================

int thunk_FUN_00e2fc24(void *param_1)

{
  int iVar1;
  
  iVar1 = pthread_setspecific(DAT_02108b00,param_1);
  return iVar1;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fc38
// Address: 00dcbac0
// ==========================================================================================

int thunk_FUN_00e2fc38(void)

{
  int iVar1;
  void *pvVar2;
  
  pvVar2 = pthread_getspecific(DAT_02108b00);
  if (pvVar2 != (void *)0x0) {
    iVar1 = pthread_setspecific(DAT_02108b00,(void *)0x0);
    return iVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00e147e8
// Address: 00dcce50
// ==========================================================================================

void thunk_FUN_00e147e8(undefined8 param_1)

{
  FUN_00e147fc(param_1,1);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df1b3c
// Address: 00dce7d0
// ==========================================================================================

void thunk_FUN_00df1b3c(long param_1,long param_2,long param_3)

{
  long *__s;
  int iVar1;
  long lVar2;
  void *__src;
  long lVar3;
  
  lVar3 = *(long *)(param_1 + 0x18);
  lVar2 = FUN_00dfc824(*(undefined8 *)(lVar3 + 8),1);
  FUN_00dfcccc();
  if ((*(byte *)(*(long *)(lVar3 + 8) + 8) >> 4 & 1) != 0) {
    FUN_00df405c(*(undefined8 *)(lVar3 + 0x10));
    param_2 = *(long *)(*(long *)(lVar3 + 0x10) + 0xb8);
  }
  __s = (long *)(param_2 + *(int *)(lVar3 + 0x18));
  if (-1 < *(int *)(lVar2 + 0x28)) {
    *__s = param_3;
    return;
  }
  if ((*(long *)(lVar2 + 0x60) != 0) && ((*(byte *)(lVar2 + 0x135) >> 3 & 1) != 0)) {
    FUN_00e11d70(param_3,lVar2,__s);
    return;
  }
  iVar1 = FUN_00dfcff8(lVar2);
  if (param_3 != 0) {
    __src = (void *)FUN_00e11d68(param_3);
    memcpy(__s,__src,(ulong)(iVar1 - 0x10U));
    return;
  }
  memset(__s,0,(ulong)(iVar1 - 0x10U));
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00def318
// Address: 00dce7d4
// ==========================================================================================

void thunk_FUN_00def318(undefined8 param_1)

{
  long lVar1;
  
  lVar1 = FUN_00dfc824(param_1,1);
  FUN_00e12fb0(lVar1 + 0x20);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dce854
// Address: 00dce8ac
// ==========================================================================================

long thunk_FUN_00dce854(void)

{
  long lVar1;
  undefined8 uVar2;
  
  if (DAT_02107928 == 0) {
    DAT_02107928 = thunk_FUN_00e3ecd4(0x38,0);
    lVar1 = DAT_02107928 + 0x18;
    uVar2 = thunk_FUN_00e11c14(*(undefined8 *)(PTR_DAT_01ff5418 + 0x10));
    FUN_00e331f0(lVar1,uVar2);
  }
  return DAT_02107928;
}



// ==========================================================================================
// Function: thunk_FUN_00e15444
// Address: 00dd1670
// ==========================================================================================

uint thunk_FUN_00e15444(long param_1,undefined8 param_2)

{
  undefined4 uVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined auStack_40 [32];
  
  uVar3 = **(undefined8 **)(param_1 + 0x20);
  uVar1 = FUN_00dd1684();
  thunk_FUN_00dcfbf0(auStack_40,uVar3,uVar1);
  uVar2 = FUN_00e1494c(auStack_40,param_2);
  return uVar2 & 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfd74
// Address: 00dd17a0
// ==========================================================================================

long thunk_FUN_00dcfd74(long param_1,int param_2,undefined8 *param_3,undefined *param_4)

{
  uint uVar1;
  void *pvVar2;
  undefined8 uVar3;
  int aiStack_40 [4];
  
  *param_4 = 0;
  if ((*(byte *)(param_1 + 0x53) & 3) == 2) {
    param_1 = FUN_00e00adc();
  }
  if (*(long *)(param_1 + 0x38) != 0) {
    aiStack_40[0] = *(int *)(*(long *)(param_1 + 0x38) + 0x10) + param_2;
    pvVar2 = bsearch(aiStack_40,(void *)(DAT_02107948 + *(long *)(DAT_02107950 + 0x38)),
                     *(ulong *)(DAT_02107950 + 0x40) / 0xc,0xc,FUN_00dd3b9c);
    if (pvVar2 == (void *)0x0) {
      return 0;
    }
    if (*(int *)((long)pvVar2 + 4) == -1) {
      uVar3 = 0;
    }
    else {
      uVar3 = *(undefined8 *)(*(long *)(DAT_02107940 + 0x38) + (long)*(int *)((long)pvVar2 + 4) * 8)
      ;
    }
    *param_3 = uVar3;
    uVar1 = *(uint *)((long)pvVar2 + 8);
    *param_4 = (ulong)uVar1 == 0xffffffff;
    if (uVar1 != 0xffffffff) {
      return DAT_02107948 + *(int *)(DAT_02107950 + 0x48) + (ulong)uVar1;
    }
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dada18
// Address: 00dd223c
// ==========================================================================================

undefined8 thunk_FUN_00dada18(void)

{
  int iVar1;
  
  iVar1 = open("/dev/urandom",0);
  DAT_020ff020 = (long)iVar1;
  return 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dd32b0
// Address: 00dd32ac
// ==========================================================================================

void thunk_FUN_00dd32b0(void)

{
  uint uVar1;
  void *pvVar2;
  undefined8 uVar3;
  undefined auStack_28 [8];
  undefined auStack_18 [8];
  
  pvVar2 = pthread_getspecific(*DAT_02107b00);
  if (pvVar2 != (void *)0x0) {
    FUN_00da6960(auStack_28,*(undefined8 *)(*(long *)(*(long *)((long)pvVar2 + 0x10) + 0xa0) + 0x10)
                );
    if (*(int *)(*(long *)((long)pvVar2 + 0x10) + 0x98) != 0) {
      FUN_00da6960(auStack_18,
                   *(undefined8 *)(*(long *)(*(long *)((long)pvVar2 + 0x10) + 0xa0) + 0x10));
      uVar1 = *(uint *)(*(long *)((long)pvVar2 + 0x10) + 0x38);
      FUN_00da71f4(auStack_18);
      if ((uVar1 >> 5 & 1) != 0) {
        *(undefined4 *)(*(long *)((long)pvVar2 + 0x10) + 0x98) = 0;
        FUN_00dd30e4(pvVar2,0x20);
        uVar3 = FUN_00e29df0();
                    /* WARNING: Subroutine does not return */
        FUN_00e28a74(uVar3,0);
      }
    }
    FUN_00da71f4(auStack_28);
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd3838
// Address: 00dd3364
// ==========================================================================================

void thunk_FUN_00dd3838(void)

{
  uint uVar1;
  void *pvVar2;
  undefined8 uVar3;
  undefined auStack_28 [8];
  undefined auStack_18 [8];
  
  pvVar2 = pthread_getspecific(*DAT_02107b00);
  if (pvVar2 != (void *)0x0) {
    FUN_00da6960(auStack_28,*(undefined8 *)(*(long *)(*(long *)((long)pvVar2 + 0x10) + 0xa0) + 0x10)
                );
    FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(*(long *)((long)pvVar2 + 0x10) + 0xa0) + 0x10)
                );
    uVar1 = *(uint *)(*(long *)((long)pvVar2 + 0x10) + 0x38);
    FUN_00da71f4(auStack_18);
    if ((uVar1 >> 7 & 1) != 0) {
      uVar3 = FUN_00e29e14();
      FUN_00e331f0(*(long *)((long)pvVar2 + 0x10) + 0x40,uVar3);
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(uVar3,0);
    }
    FUN_00da71f4(auStack_28);
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fbb0
// Address: 00dd3834
// ==========================================================================================

bool thunk_FUN_00e2fbb0(void)

{
  int iVar1;
  
  iVar1 = sched_yield();
  return iVar1 == 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd3aa4
// Address: 00dd39f8
// ==========================================================================================

int thunk_FUN_00dd3aa4(long param_1)

{
  int *piVar1;
  int iVar2;
  char cVar3;
  bool bVar4;
  int iVar5;
  
  piVar1 = (int *)(param_1 + 0x30);
  do {
    iVar2 = *piVar1;
    cVar3 = '\x01';
    bVar4 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar4) {
      *piVar1 = iVar2 + 1;
      cVar3 = ExclusiveMonitorsStatus();
    }
  } while (cVar3 != '\0');
  DataMemoryBarrier(2,3);
  if (iVar2 == 0) {
    iVar5 = FUN_00e31e1c(*(undefined8 *)(param_1 + 0x28),0);
    piVar1 = (int *)(param_1 + 0x34);
    do {
      while (*piVar1 != 0) {
        ClearExclusiveLocal();
        DataMemoryBarrier(2,3);
      }
      cVar3 = '\x01';
      bVar4 = (bool)ExclusiveMonitorPass(piVar1,0x10);
      if (bVar4) {
        *piVar1 = iVar5;
        cVar3 = ExclusiveMonitorsStatus();
      }
    } while (cVar3 != '\0');
    DataMemoryBarrier(2,3);
  }
  return iVar2 + 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dd3b0c
// Address: 00dd39fc
// ==========================================================================================

int thunk_FUN_00dd3b0c(long param_1)

{
  int *piVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  char cVar4;
  bool bVar5;
  int iVar6;
  
  piVar1 = (int *)(param_1 + 0x30);
  do {
    iVar6 = *piVar1 + -1;
    cVar4 = '\x01';
    bVar5 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar5) {
      *piVar1 = iVar6;
      cVar4 = ExclusiveMonitorsStatus();
    }
  } while (cVar4 != '\0');
  DataMemoryBarrier(2,3);
  if (iVar6 == 0) {
    puVar2 = (undefined4 *)(param_1 + 0x34);
    do {
      uVar3 = *puVar2;
      cVar4 = '\x01';
      bVar5 = (bool)ExclusiveMonitorPass(puVar2,0x10);
      if (bVar5) {
        *puVar2 = 0;
        cVar4 = ExclusiveMonitorsStatus();
      }
    } while (cVar4 != '\0');
    DataMemoryBarrier(2,3);
    FUN_00e324f8(uVar3);
  }
  return iVar6;
}



// ==========================================================================================
// Function: thunk_FUN_00e09748
// Address: 00de39a4
// ==========================================================================================

void thunk_FUN_00e09748(void **param_1)

{
  if (param_1 != (void **)0x0) {
    if (*param_1 != (void *)0x0) {
      free(*param_1);
      *param_1 = (void *)0x0;
    }
    free(param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd02f8
// Address: 00deb62c
// ==========================================================================================

undefined8 thunk_FUN_00dd02f8(undefined4 *param_1)

{
  long lVar1;
  undefined8 uVar2;
  
  if (param_1[2] != 0) {
    lVar1 = FUN_00dce95c();
    return *(undefined8 *)(lVar1 + 0x20);
  }
  uVar2 = FUN_00dcf5ec(*param_1);
  return uVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dcf4d4
// Address: 00deb7cc
// ==========================================================================================

undefined8 thunk_FUN_00dcf4d4(long param_1)

{
  undefined8 uVar1;
  
  if ((*(long *)(param_1 + 0x28) != 0) && (*(int *)(*(long *)(param_1 + 0x28) + 0xc) != -1)) {
    uVar1 = FUN_00dce95c();
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00df0d6c
// Address: 00debfbc
// ==========================================================================================

void thunk_FUN_00df0d6c(void **param_1)

{
  if (*param_1 != (void *)0x0) {
    FUN_00df0d94();
    operator_delete(*param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfa80
// Address: 00deea54
// ==========================================================================================

undefined8 thunk_FUN_00dcfa80(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: thunk_FUN_00da7e6c
// Address: 00def314
// ==========================================================================================

bool thunk_FUN_00da7e6c(void)

{
  int iVar1;
  
  iVar1 = FUN_00da7e84();
  return iVar1 == 0;
}



// ==========================================================================================
// Function: thunk_FUN_00e019cc
// Address: 00def330
// ==========================================================================================

void thunk_FUN_00e019cc(long param_1)

{
  if (param_1 != 0) {
    FUN_00dcf9a4();
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcce54
// Address: 00df19bc
// ==========================================================================================

void thunk_FUN_00dcce54(long param_1,long param_2,long param_3,undefined8 *param_4)

{
  undefined8 *puVar1;
  byte bVar2;
  long lVar3;
  bool bVar4;
  uint uVar5;
  int iVar6;
  long lVar7;
  ulong uVar8;
  undefined8 uVar9;
  char *pcVar10;
  char *pcVar11;
  long *plVar12;
  undefined8 *puVar13;
  undefined8 *puVar14;
  long lVar15;
  ulong auStack_60 [4];
  
  lVar3 = tpidr_el0;
  auStack_60[3] = *(long *)(lVar3 + 0x28);
  lVar15 = *(long *)(param_1 + 0x10);
  *param_4 = 0;
  if ((*(byte *)(lVar15 + 0x4c) >> 4 & 1) == 0) {
    if (param_2 == 0) {
      iVar6 = strcmp(*(char **)(lVar15 + 0x18),".ctor");
      if (iVar6 != 0) {
        uVar8 = FUN_00e29eb0("Non-static method requires a target");
        goto LAB_00dcd08c;
      }
      goto LAB_00dccef4;
    }
    lVar7 = FUN_00e11b18(param_2,*(undefined8 *)(lVar15 + 0x20));
    if (lVar7 != 0) {
      lVar15 = FUN_00e11a44(param_2,lVar15);
      uVar8 = FUN_00dd1944();
      if ((uVar8 & 1) != 0) {
        FUN_00dd1810(auStack_60,*(undefined8 *)(param_1 + 0x10));
        uVar8 = (ulong)auStack_60 | 1;
        if ((auStack_60[0] & 1) != 0) {
          uVar8 = auStack_60[2];
        }
        uVar9 = FUN_00e29d50(uVar8);
                    /* WARNING: Subroutine does not return */
        FUN_00e28a74(uVar9,0);
      }
      if (*(int *)(*(long *)(lVar15 + 0x20) + 0x28) < 0) {
        param_2 = FUN_00e11d68(param_2);
      }
      goto LAB_00dccef4;
    }
    uVar9 = *(undefined8 *)PTR_DAT_01ff5418;
    pcVar10 = "TargetException";
    pcVar11 = "Object does not match target type.";
  }
  else {
LAB_00dccef4:
    if (param_3 == 0) {
      uVar5 = 0;
    }
    else {
      uVar5 = FUN_00debcc4(param_3);
    }
    if (uVar5 == *(byte *)(lVar15 + 0x52)) {
      if ((*(char *)(*(long *)(lVar15 + 0x20) + 0x132) == '\0') ||
         (iVar6 = strcmp(*(char **)(lVar15 + 0x18),".ctor"), iVar6 != 0)) {
        auStack_60[0] = 0;
        uVar9 = FUN_00df5f8c(lVar15,param_2,param_3,auStack_60);
        uVar8 = auStack_60[0];
        if (auStack_60[0] != 0) {
LAB_00dcd08c:
                    /* WARNING: Subroutine does not return */
          FUN_00e28a74(uVar8,0);
        }
      }
      else {
        uVar8 = FUN_00debcc4(param_3);
        puVar13 = (undefined8 *)
                  ((long)auStack_60 -
                  ((-(uVar8 >> 0x1f & 1) & 0xfffffff800000000 | (uVar8 & 0xffffffff) << 3) + 0xf &
                  0xfffffffffffffff0));
        uVar5 = (uint)uVar8;
        if (0 < (int)uVar5) {
          uVar8 = uVar8 & 0xffffffff;
          plVar12 = (long *)(param_3 + 0x20);
          puVar14 = puVar13;
          do {
            uVar8 = uVar8 - 1;
            *puVar14 = *(undefined8 *)(*plVar12 + 0x10);
            plVar12 = plVar12 + 1;
            puVar14 = puVar14 + 1;
          } while (uVar8 != 0);
        }
        bVar2 = *(byte *)(*(long *)(lVar15 + 0x20) + 0x132);
        bVar4 = uVar5 != bVar2;
        puVar14 = puVar13;
        if (bVar4) {
          puVar14 = puVar13 + bVar2;
        }
        puVar1 = (undefined8 *)0x0;
        if (bVar4) {
          puVar1 = puVar13;
        }
        uVar9 = FUN_00e10f70(*(long *)(lVar15 + 0x20),puVar14,puVar1);
      }
      goto LAB_00dccfbc;
    }
    uVar9 = *(undefined8 *)PTR_DAT_01ff5418;
    pcVar10 = "TargetParameterCountException";
    pcVar11 = "Incorrect number of parameters";
  }
  uVar9 = FUN_00e294a4(uVar9,"System.Reflection",pcVar10,pcVar11);
  FUN_00e331f0(param_4,uVar9);
  uVar9 = 0;
LAB_00dccfbc:
  if (*(long *)(lVar3 + 0x28) != auStack_60[3]) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar9);
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e153f8
// Address: 00df4480
// ==========================================================================================

uint thunk_FUN_00e153f8(long param_1,undefined8 param_2)

{
  undefined4 uVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined auStack_40 [32];
  
  uVar3 = **(undefined8 **)(param_1 + 0x10);
  uVar1 = FUN_00df3f00();
  thunk_FUN_00dcfbf0(auStack_40,uVar3,uVar1);
  uVar2 = FUN_00e1494c(auStack_40,param_2);
  return uVar2 & 1;
}



// ==========================================================================================
// Function: thunk_FUN_00df8134
// Address: 00df82a4
// ==========================================================================================

void * thunk_FUN_00df8134(void)

{
  uint *puVar1;
  long lVar2;
  uint uVar3;
  uint uVar4;
  ushort uVar5;
  int iVar6;
  int *piVar7;
  ulong uVar8;
  ulong uVar9;
  ulong *puVar10;
  ulong uVar11;
  void *unaff_x20;
  uint *puVar12;
  uint uVar13;
  undefined auStack_70 [8];
  long lStack_68;
  
  iVar6 = dladdr(FUN_00df80f0,auStack_70);
  lVar2 = 0;
  if (iVar6 != 0) {
    lVar2 = lStack_68;
  }
  uVar5 = *(ushort *)(lVar2 + 0x38);
  piVar7 = (int *)(*(long *)(lVar2 + 0x20) + lVar2);
  if (uVar5 != 0) {
    puVar10 = (ulong *)(piVar7 + 4);
    uVar3 = (uint)uVar5;
    if (uVar5 < 2) {
      uVar3 = 1;
    }
    uVar11 = (ulong)uVar3;
    uVar8 = 0xffffffffffffffff;
    do {
      uVar9 = uVar8;
      if ((*(int *)(puVar10 + -2) == 1) && (uVar9 = *puVar10, uVar8 <= *puVar10)) {
        uVar9 = uVar8;
      }
      uVar11 = uVar11 - 1;
      puVar10 = puVar10 + 7;
      uVar8 = uVar9;
    } while (uVar11 != 0);
    if (uVar9 != 0xffffffffffffffff) goto joined_r0x00df81c0;
  }
  uVar9 = 0;
joined_r0x00df81c0:
  if (uVar5 != 0) {
    uVar11 = (ulong)(uint)uVar5;
    do {
      if (*piVar7 == 4) {
        puVar12 = (uint *)((lVar2 - uVar9) + *(long *)(piVar7 + 4));
        puVar1 = (uint *)((long)puVar12 + *(long *)(piVar7 + 10));
        do {
          if (puVar1 <= puVar12) {
            return (void *)0x0;
          }
          uVar3 = puVar12[2];
          if (uVar3 == 3) {
            uVar4 = *puVar12;
            unaff_x20 = malloc(0x29);
            if (puVar12[1] == 0) {
              return unaff_x20;
            }
            iVar6 = 0;
            uVar13 = 0;
            do {
              snprintf((char *)((long)unaff_x20 + (long)iVar6),3,"%02x",
                       (ulong)*(byte *)((long)puVar12 + (long)(int)uVar13 + (ulong)uVar4 + 0xc));
              uVar13 = uVar13 + 1;
              iVar6 = iVar6 + 2;
            } while (uVar13 < puVar12[1]);
          }
          else {
            puVar12 = (uint *)((long)puVar12 + (ulong)*puVar12 + (ulong)puVar12[1] + 0xc);
          }
        } while (uVar3 != 3);
        return unaff_x20;
      }
      uVar11 = uVar11 - 1;
      piVar7 = piVar7 + 0xe;
    } while (uVar11 != 0);
  }
  return (void *)0x0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd2fb4
// Address: 00dfc0b8
// ==========================================================================================

void thunk_FUN_00dd2fb4(long param_1,uint param_2)

{
  undefined auStack_18 [8];
  
  FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(param_1 + 0xa0) + 0x10));
  *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) & (param_2 ^ 0xffffffff);
  FUN_00da71f4(auStack_18);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e2fbb0
// Address: 00dfc304
// ==========================================================================================

bool thunk_FUN_00e2fbb0(void)

{
  int iVar1;
  
  iVar1 = sched_yield();
  return iVar1 == 0;
}



// ==========================================================================================
// Function: thunk_FUN_00e2f754
// Address: 00dfc31c
// ==========================================================================================

undefined8 thunk_FUN_00e2f754(void)

{
  return 0x7fffffff;
}



// ==========================================================================================
// Function: thunk_FUN_00dd3368
// Address: 00dfc364
// ==========================================================================================

undefined4 thunk_FUN_00dd3368(long param_1)

{
  uint uVar1;
  undefined4 uVar2;
  long lVar3;
  undefined auStack_28 [8];
  undefined auStack_18 [8];
  
  FUN_00da6960(auStack_28,*(undefined8 *)(*(long *)(param_1 + 0xa0) + 0x10));
  FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(param_1 + 0xa0) + 0x10));
  uVar1 = *(uint *)(param_1 + 0x38);
  FUN_00da71f4(auStack_18);
  if ((uVar1 & 0x91) == 0) {
    lVar3 = *(long *)(param_1 + 0x18);
    if (lVar3 == 0) {
      FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(param_1 + 0xa0) + 0x10));
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x100;
      FUN_00da71f4(auStack_18);
    }
    else {
      FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(param_1 + 0xa0) + 0x10));
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x80;
      FUN_00da71f4(auStack_18);
      FUN_00dcba8c(lVar3,thunk_FUN_00dd3838,0);
    }
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  FUN_00da71f4(auStack_28);
  return uVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dd27ec
// Address: 00dfc3d4
// ==========================================================================================

void thunk_FUN_00dd27ec(long param_1)

{
  long lVar1;
  undefined auStack_18 [8];
  
  FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(*(long *)(param_1 + 0x10) + 0xa0) + 0x10));
  lVar1 = *(long *)(*(long *)(param_1 + 0x10) + 0x18);
  *(undefined4 *)(*(long *)(param_1 + 0x10) + 0x98) = 1;
  if (lVar1 != 0) {
    FUN_00dcba8c(lVar1,thunk_FUN_00dd32b0,0);
  }
  FUN_00da71f4(auStack_18);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd3458
// Address: 00dfc4bc
// ==========================================================================================

void thunk_FUN_00dd3458(long param_1,undefined4 param_2)

{
  long lVar1;
  undefined auStack_18 [8];
  
  lVar1 = *(long *)(param_1 + 0x10);
  FUN_00da6960(auStack_18,*(undefined8 *)(*(long *)(lVar1 + 0xa0) + 0x10));
  FUN_00dcb954(*(undefined8 *)(lVar1 + 0x18),param_2);
  FUN_00da71f4(auStack_18);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00df8694
// Address: 00dfc500
// ==========================================================================================

long thunk_FUN_00df8694(void)

{
  int iVar1;
  long lVar2;
  timespec tStack_30;
  timeval tStack_20;
  
  if (DAT_02108238 == 0) {
    iVar1 = clock_getres(1,(timespec *)&DAT_02108230);
    DAT_02108240 = (uint)(iVar1 == 0);
    if (DAT_02108240 == 0) goto LAB_00df86ec;
  }
  else if (DAT_02108240 == 0) goto LAB_00df86ec;
  iVar1 = clock_gettime(1,&tStack_30);
  if (iVar1 == 0) {
    return tStack_30.tv_nsec / 100 + tStack_30.tv_sec * 10000000;
  }
LAB_00df86ec:
  iVar1 = gettimeofday(&tStack_20,(__timezone_ptr_t)0x0);
  lVar2 = 0;
  if (iVar1 == 0) {
    lVar2 = (tStack_20.tv_usec + tStack_20.tv_sec * 1000000) * 10;
  }
  return lVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0544
// Address: 00dfcd90
// ==========================================================================================

void thunk_FUN_00dd0544(long *param_1,int *param_2)

{
  long lVar1;
  long lVar2;
  long lVar3;
  
  lVar2 = DAT_02107950;
  lVar1 = DAT_02107948;
  if (*param_2 == -1) {
    lVar3 = 0;
  }
  else {
    lVar3 = DAT_02107948 + *(int *)(DAT_02107950 + 0x78) + (long)*param_2 * 0x10;
  }
  *param_1 = lVar3;
  param_1[1] = lVar1 + *(int *)(lVar2 + 0x18) + (long)param_2[1];
  *(undefined2 *)(param_1 + 2) = *(undefined2 *)(param_2 + 3);
  *(undefined2 *)((long)param_1 + 0x12) = *(undefined2 *)((long)param_2 + 0xe);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0070
// Address: 00dfe974
// ==========================================================================================

void thunk_FUN_00dd0070(long *param_1,undefined8 param_2,long param_3,int param_4)

{
  long lVar1;
  int *piVar2;
  
  piVar2 = (int *)(DAT_02107948 + *(int *)(DAT_02107950 + 0x58) +
                  (long)(*(int *)(param_3 + 0x10) + param_4) * 0xc);
  *param_1 = DAT_02107948 + *(int *)(DAT_02107950 + 0x18) + (long)*piVar2;
  *(int *)(param_1 + 1) = piVar2[1];
  if (piVar2[2] == -1) {
    lVar1 = 0;
  }
  else {
    lVar1 = *(long *)(*(long *)(DAT_02107940 + 0x38) + (long)piVar2[2] * 8);
  }
  param_1[2] = lVar1;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd02bc
// Address: 00dfe978
// ==========================================================================================

long thunk_FUN_00dd02bc(long param_1)

{
  if (*(int *)(param_1 + 0x14) != -1) {
    return DAT_02107948 + *(int *)(DAT_02107950 + 0x78) + (long)*(int *)(param_1 + 0x14) * 0x10;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00deb928
// Address: 00dff098
// ==========================================================================================

undefined8 thunk_FUN_00deb928(long param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  void *pvVar5;
  undefined8 uVar6;
  uint uVar7;
  long *plVar8;
  undefined4 auStack_98 [2];
  undefined8 uStack_90;
  undefined8 uStack_88;
  long lStack_80;
  long lStack_78;
  long lStack_70;
  long lStack_68;
  long lStack_60;
  long lStack_58;
  long lStack_50;
  long lStack_48;
  undefined8 uStack_40;
  undefined auStack_38 [8];
  
  plVar8 = (long *)(param_1 + 0x30);
  lVar4 = *plVar8;
  if (lVar4 == 0) {
    FUN_00da6960(&lStack_80,&DAT_02107c60);
    if (*plVar8 == 0) {
      pvVar5 = operator_new(0x70);
      FUN_00df0a9c(pvVar5,0,auStack_98,auStack_38);
      *(void **)(param_1 + 0x30) = pvVar5;
      if (*(int *)(param_1 + 0x18) != 0) {
        uVar7 = 0;
        do {
          uVar6 = thunk_FUN_00dcf4f4(param_1,uVar7);
          FUN_00debac4(param_1,uVar6);
          uVar7 = uVar7 + 1;
        } while (uVar7 < *(uint *)(param_1 + 0x18));
      }
      if (*(int *)(param_1 + 0x1c) != 0) {
        uVar7 = 0;
        do {
          uVar6 = thunk_FUN_00dcf598(param_1,uVar7);
          FUN_00debac4(param_1,uVar6);
          uVar7 = uVar7 + 1;
        } while (uVar7 < *(uint *)(param_1 + 0x1c));
      }
    }
    FUN_00da71f4(&lStack_80);
    lVar4 = *plVar8;
  }
  auStack_98[0] = 0;
  uStack_90 = param_2;
  uStack_88 = param_3;
  FUN_00df0cc8(&lStack_80,lVar4,auStack_98);
  lVar3 = lStack_60;
  lVar2 = lStack_68;
  lVar1 = lStack_70;
  lVar4 = lStack_78;
  lStack_80 = *plVar8;
  lStack_78 = *(long *)(lStack_80 + 0x48);
  lStack_70 = *(long *)(lStack_80 + 0x50);
  uStack_40 = 0;
  lStack_60 = 0;
  lStack_68 = lStack_70;
  lStack_58 = lStack_78;
  lStack_50 = lStack_70;
  lStack_48 = lStack_70;
  FUN_00df0a1c(&lStack_80);
  if ((((lVar4 == lStack_78) && (lVar1 == lStack_70)) && (lVar2 == lStack_68)) &&
     ((lVar2 == lVar1 || (lVar3 == lStack_60)))) {
    uVar6 = 0;
  }
  else {
    uVar6 = thunk_FUN_00dcf974(*(undefined8 *)(lVar3 + 0x18));
  }
  return uVar6;
}



// ==========================================================================================
// Function: thunk_FUN_00e15490
// Address: 00dff790
// ==========================================================================================

uint thunk_FUN_00e15490(undefined8 *param_1,undefined8 param_2)

{
  uint uVar1;
  undefined auStack_30 [32];
  
  thunk_FUN_00dcfbf0(auStack_30,*param_1,*(undefined4 *)((long)param_1 + 0x11c));
  uVar1 = FUN_00e1494c(auStack_30,param_2);
  return uVar1 & 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dceeb4
// Address: 00dff7c4
// ==========================================================================================

void * thunk_FUN_00dceeb4(long param_1,undefined8 *param_2)

{
  ulong uVar1;
  void *pvVar2;
  undefined8 uVar3;
  long lVar4;
  long lVar5;
  int aiStack_40 [4];
  
  lVar4 = *(long *)(param_1 + 0x10);
  lVar5 = *(long *)(lVar4 + 0x80);
  uVar1 = FUN_00def174(lVar4 + 0x20);
  if ((uVar1 & 1) != 0) {
    lVar4 = FUN_00deb11c(*(undefined8 *)(lVar4 + 0x60));
  }
  aiStack_40[0] = *(int *)(*(long *)(lVar4 + 0x68) + 0x20) + (int)((ulong)(param_1 - lVar5) >> 5);
  pvVar2 = bsearch(aiStack_40,(void *)(DAT_02107948 + *(long *)(DAT_02107950 + 0x40)),
                   *(ulong *)(DAT_02107950 + 0x48) / 0xc,0xc,FUN_00dd3b8c);
  if (pvVar2 != (void *)0x0) {
    if (*(int *)((long)pvVar2 + 4) == -1) {
      uVar3 = 0;
    }
    else {
      uVar3 = *(undefined8 *)(*(long *)(DAT_02107940 + 0x38) + (long)*(int *)((long)pvVar2 + 4) * 8)
      ;
    }
    *param_2 = uVar3;
    if (*(uint *)((long)pvVar2 + 8) == 0xffffffff) {
      pvVar2 = (void *)0x0;
    }
    else {
      pvVar2 = (void *)(DAT_02107948 + *(int *)(DAT_02107950 + 0x48) +
                       (ulong)*(uint *)((long)pvVar2 + 8));
    }
  }
  return pvVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dd02f8
// Address: 00dffe80
// ==========================================================================================

undefined8 thunk_FUN_00dd02f8(undefined4 *param_1)

{
  long lVar1;
  undefined8 uVar2;
  
  if (param_1[2] != 0) {
    lVar1 = FUN_00dce95c();
    return *(undefined8 *)(lVar1 + 0x20);
  }
  uVar2 = FUN_00dcf5ec(*param_1);
  return uVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dcf4d4
// Address: 00e00158
// ==========================================================================================

undefined8 thunk_FUN_00dcf4d4(long param_1)

{
  undefined8 uVar1;
  
  if ((*(long *)(param_1 + 0x28) != 0) && (*(int *)(*(long *)(param_1 + 0x28) + 0xc) != -1)) {
    uVar1 = FUN_00dce95c();
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dcf4f4
// Address: 00e0015c
// ==========================================================================================

long thunk_FUN_00dcf4f4(long param_1,int param_2)

{
  param_2 = **(int **)(param_1 + 0x28) + param_2;
  if (param_2 != -1) {
    return DAT_02107948 + *(int *)(DAT_02107950 + 0xa0) + (long)param_2 * 0x58;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dcf598
// Address: 00e00160
// ==========================================================================================

long thunk_FUN_00dcf598(long param_1,int param_2)

{
  int iVar1;
  
  if (param_2 != -1) {
    iVar1 = *(int *)(DAT_02107948 + *(int *)(DAT_02107950 + 0xf8) +
                    (long)(*(int *)(*(long *)(param_1 + 0x28) + 4) + param_2) * 4);
    if (iVar1 != -1) {
      return DAT_02107948 + *(int *)(DAT_02107950 + 0xa0) + (long)iVar1 * 0x58;
    }
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd05a8
// Address: 00e00164
// ==========================================================================================

void thunk_FUN_00dd05a8(long param_1)

{
  FUN_00dce95c((int)((ulong)(param_1 - (DAT_02107948 + *(int *)(DAT_02107950 + 0x30))) >> 2) *
               0x38e38e39);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd045c
// Address: 00e01708
// ==========================================================================================

undefined8 thunk_FUN_00dd045c(long param_1)

{
  if (**(int **)(param_1 + 8) != -1) {
    return *(undefined8 *)(*(long *)(DAT_02107940 + 0x38) + (long)**(int **)(param_1 + 8) * 8);
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0488
// Address: 00e0170c
// ==========================================================================================

void thunk_FUN_00dd0488(long param_1)

{
  FUN_00dcf2c8(**(undefined4 **)(param_1 + 8));
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0494
// Address: 00e01710
// ==========================================================================================

undefined  [16] thunk_FUN_00dd0494(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined auVar4 [16];
  
  iVar1 = **(int **)(param_1 + 8);
  if (iVar1 == -1) {
    uVar3 = 0;
  }
  else {
    uVar3 = *(undefined8 *)(*(long *)(DAT_02107940 + 0x38) + (long)iVar1 * 8);
  }
  uVar2 = FUN_00dcee68((*(int **)(param_1 + 8))[1]);
  auVar4._8_8_ = uVar2;
  auVar4._0_8_ = uVar3;
  return auVar4;
}



// ==========================================================================================
// Function: thunk_FUN_00dcf974
// Address: 00e019d8
// ==========================================================================================

void thunk_FUN_00dcf974(long param_1)

{
  FUN_00dcf5ec((int)((ulong)(param_1 - (DAT_02107948 + *(int *)(DAT_02107950 + 0xa0))) >> 3) *
               -0x45d1745d);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfa80
// Address: 00e019dc
// ==========================================================================================

undefined8 thunk_FUN_00dcfa80(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0320
// Address: 00e019e0
// ==========================================================================================

undefined8 thunk_FUN_00dd0320(int *param_1)

{
  undefined4 *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  puVar1 = (undefined4 *)(DAT_02107948 + *(int *)(DAT_02107950 + 0x78) + (long)*param_1 * 0x10);
  if (puVar1[2] != 0) {
    lVar2 = FUN_00dce95c();
    return *(undefined8 *)(lVar2 + 0x20);
  }
  uVar3 = FUN_00dcf5ec(*puVar1);
  return uVar3;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0368
// Address: 00e019e4
// ==========================================================================================

undefined8 thunk_FUN_00dd0368(int *param_1)

{
  undefined8 uVar1;
  undefined4 *puVar2;
  
  if (*param_1 == -1) {
    puVar2 = (undefined4 *)0x0;
  }
  else {
    puVar2 = (undefined4 *)(DAT_02107948 + *(int *)(DAT_02107950 + 0x78) + (long)*param_1 * 0x10);
  }
  if (puVar2[2] != 0) {
    uVar1 = FUN_00dce95c(*puVar2);
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd03b0
// Address: 00e019e8
// ==========================================================================================

long thunk_FUN_00dd03b0(long param_1,int param_2)

{
  param_2 = *(int *)(param_1 + 0xc) + param_2;
  if (param_2 != -1) {
    return DAT_02107948 + *(int *)(DAT_02107950 + 0x68) + (long)param_2 * 0x10;
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfd74
// Address: 00e01a68
// ==========================================================================================

long thunk_FUN_00dcfd74(long param_1,int param_2,undefined8 *param_3,undefined *param_4)

{
  uint uVar1;
  void *pvVar2;
  undefined8 uVar3;
  int aiStack_40 [4];
  
  *param_4 = 0;
  if ((*(byte *)(param_1 + 0x53) & 3) == 2) {
    param_1 = FUN_00e00adc();
  }
  if (*(long *)(param_1 + 0x38) != 0) {
    aiStack_40[0] = *(int *)(*(long *)(param_1 + 0x38) + 0x10) + param_2;
    pvVar2 = bsearch(aiStack_40,(void *)(DAT_02107948 + *(long *)(DAT_02107950 + 0x38)),
                     *(ulong *)(DAT_02107950 + 0x40) / 0xc,0xc,FUN_00dd3b9c);
    if (pvVar2 == (void *)0x0) {
      return 0;
    }
    if (*(int *)((long)pvVar2 + 4) == -1) {
      uVar3 = 0;
    }
    else {
      uVar3 = *(undefined8 *)(*(long *)(DAT_02107940 + 0x38) + (long)*(int *)((long)pvVar2 + 4) * 8)
      ;
    }
    *param_3 = uVar3;
    uVar1 = *(uint *)((long)pvVar2 + 8);
    *param_4 = (ulong)uVar1 == 0xffffffff;
    if (uVar1 != 0xffffffff) {
      return DAT_02107948 + *(int *)(DAT_02107950 + 0x48) + (ulong)uVar1;
    }
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfb90
// Address: 00e01b74
// ==========================================================================================

void thunk_FUN_00dcfb90(long param_1,uint param_2)

{
  ulong uStack_8;
  
  uStack_8 = (ulong)param_2;
  bsearch(&uStack_8,
          (void *)(DAT_02107948 + *(int *)(DAT_02107950 + 0xd0) +
                  (long)*(int *)(*(long *)(param_1 + 0x28) + 8) * 8),
          (ulong)*(uint *)(param_1 + 0x20),8,FUN_00dcfbe0);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfbf0
// Address: 00e01b78
// ==========================================================================================

void thunk_FUN_00dcfbf0(undefined8 *param_1,long param_2,uint param_3)

{
  long lVar1;
  void *pvVar2;
  ulong uStack_28;
  
  uStack_28 = (ulong)param_3;
  pvVar2 = bsearch(&uStack_28,
                   (void *)(DAT_02107948 + *(int *)(DAT_02107950 + 0xd0) +
                           (long)*(int *)(*(long *)(param_2 + 0x28) + 8) * 8),
                   (ulong)*(uint *)(param_2 + 0x20),8,FUN_00dcfbe0);
  if (pvVar2 == (void *)0x0) {
    *param_1 = 0;
    param_1[1] = 0;
    *(undefined4 *)(param_1 + 3) = 0;
    param_1[2] = 0;
  }
  else {
    lVar1 = DAT_02107948 + *(int *)(DAT_02107950 + 200);
    FUN_00e35284(param_1,param_2,lVar1 + (ulong)*(uint *)((long)pvVar2 + 4),
                 lVar1 + (ulong)*(uint *)((long)pvVar2 + 0xc));
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfc98
// Address: 00e01b7c
// ==========================================================================================

void thunk_FUN_00dcfc98(undefined8 *param_1,long param_2)

{
  long lVar1;
  long lVar2;
  ulong uVar3;
  long *plVar4;
  uint uVar5;
  
  if (param_2 == 0) {
    *param_1 = 0;
    param_1[1] = 0;
    *(undefined4 *)(param_1 + 3) = 0;
    param_1[2] = 0;
    return;
  }
  uVar3 = (ulong)DAT_02107958;
  if (0 < (int)DAT_02107958) {
    plVar4 = (long *)(DAT_02107960 + 0x10);
    do {
      uVar5 = (uint)((ulong)(param_2 - (DAT_02107948 + *(int *)(DAT_02107950 + 0xd0))) >> 3);
      if ((*(int *)(plVar4 + -1) <= (int)uVar5) &&
         (uVar5 < (uint)(*(int *)(*plVar4 + 0x20) + *(int *)(plVar4 + -1)))) {
        if (plVar4 != (long *)0x10) {
          lVar2 = *plVar4;
          goto LAB_00dcfd08;
        }
        break;
      }
      uVar3 = uVar3 - 1;
      plVar4 = plVar4 + 3;
    } while (uVar3 != 0);
  }
  lVar2 = 0;
LAB_00dcfd08:
  lVar1 = DAT_02107948 + *(int *)(DAT_02107950 + 200);
  FUN_00e35284(param_1,lVar2,lVar1 + (ulong)*(uint *)(param_2 + 4),
               lVar1 + (ulong)*(uint *)(param_2 + 0xc));
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfa88
// Address: 00e01cf4
// ==========================================================================================

bool thunk_FUN_00dcfa88(long param_1)

{
  return *(int *)(param_1 + 0xc) != -1;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfa98
// Address: 00e01cf8
// ==========================================================================================

uint thunk_FUN_00dcfa98(long param_1)

{
  return *(uint *)(param_1 + 0x50) & 1;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfab0
// Address: 00e01cfc
// ==========================================================================================

undefined  [16] thunk_FUN_00dcfab0(long *param_1)

{
  long lVar1;
  undefined auVar2 [16];
  
  lVar1 = DAT_02107948 + *(int *)(DAT_02107950 + 0x18);
  auVar2._8_8_ = lVar1 + *param_1;
  auVar2._0_8_ = lVar1 + param_1[1];
  return auVar2;
}



// ==========================================================================================
// Function: thunk_FUN_00dcfb04
// Address: 00e01d00
// ==========================================================================================

long thunk_FUN_00dcfb04(long param_1,int **param_2)

{
  int *piVar1;
  long lVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  
  lVar5 = DAT_02107950;
  lVar4 = DAT_02107948;
  if (param_2 != (int **)0x0) {
    lVar2 = DAT_02107948 + *(int *)(DAT_02107950 + 0x80);
    if (*param_2 == (int *)0x0) {
      if (*(short *)(param_1 + 0x48) == 0) {
        return 0;
      }
      iVar3 = *(int *)(param_1 + 0x30);
      *param_2 = (int *)(lVar2 + (long)iVar3 * 4);
      iVar3 = *(int *)(lVar2 + (long)iVar3 * 4);
    }
    else {
      piVar1 = *param_2 + 1;
      if ((long)(int)(*(int *)(param_1 + 0x30) + (uint)*(ushort *)(param_1 + 0x48)) <=
          (long)piVar1 - lVar2 >> 2) {
        return 0;
      }
      *param_2 = piVar1;
      iVar3 = *piVar1;
    }
    if (iVar3 != -1) {
      return lVar4 + *(int *)(lVar5 + 0xa0) + (long)iVar3 * 0x58;
    }
  }
  return 0;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0278
// Address: 00e01d04
// ==========================================================================================

undefined4 thunk_FUN_00dd0278(long param_1)

{
  return *(undefined4 *)(param_1 + 0xc);
}



// ==========================================================================================
// Function: thunk_FUN_00dd04d8
// Address: 00e01d08
// ==========================================================================================

ulong thunk_FUN_00dd04d8(ulong param_1)

{
  if (param_1 != 0) {
    param_1 = (ulong)*(uint *)(param_1 + 4);
  }
  return param_1;
}



// ==========================================================================================
// Function: thunk_FUN_00dd0520
// Address: 00e01d0c
// ==========================================================================================

long thunk_FUN_00dd0520(long param_1)

{
  return DAT_02107948 + *(int *)(DAT_02107950 + 0x18) + (long)*(int *)(param_1 + 4);
}



// ==========================================================================================
// Function: thunk_FUN_00e11c14
// Address: 00e1190c
// ==========================================================================================

long * thunk_FUN_00e11c14(long param_1)

{
  char cVar1;
  bool bVar2;
  undefined *puVar3;
  long *plVar4;
  
  FUN_00dfcccc();
  if ((*(long *)(param_1 + 0x60) != 0) && ((*(byte *)(param_1 + 0x135) >> 3 & 1) != 0)) {
    param_1 = *(long *)(param_1 + 0x40);
  }
  if ((*(byte *)(param_1 + 0x135) >> 5 & 1) == 0) {
    plVar4 = (long *)FUN_00e11cf0(param_1);
  }
  else if (*(long *)(param_1 + 8) == 0) {
    plVar4 = (long *)FUN_00e3eaec(*(undefined4 *)(param_1 + 0xf8));
    *plVar4 = param_1;
    puVar3 = PTR_DAT_01ff5430;
    do {
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(puVar3,0x10);
      if (bVar2) {
        *(long *)puVar3 = *(long *)puVar3 + 1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
  }
  else {
    plVar4 = (long *)FUN_00e39958(*(undefined4 *)(param_1 + 0xf8),param_1);
    puVar3 = PTR_DAT_01ff5430;
    do {
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(puVar3,0x10);
      if (bVar2) {
        *(long *)puVar3 = *(long *)puVar3 + 1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
  }
  if ((*(byte *)(param_1 + 0x136) >> 1 & 1) != 0) {
    FUN_00e32cb0(plVar4);
  }
  if ((char)*PTR_DAT_01ff5438 < '\0') {
    FUN_00e2ae40(plVar4,param_1);
  }
  FUN_00df405c(param_1);
  return plVar4;
}



// ==========================================================================================
// Function: thunk_FUN_00dcb268
// Address: 00e11e54
// ==========================================================================================

void thunk_FUN_00dcb268(undefined8 param_1)

{
  DAT_02107870 = param_1;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00d9e750
// Address: 00e28078
// ==========================================================================================

void thunk_FUN_00d9e750(void)

{
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e2a3c4
// Address: 00e2a9c4
// ==========================================================================================

void thunk_FUN_00e2a3c4(long **param_1)

{
  long *plVar1;
  ulong *puVar2;
  long lVar3;
  long lVar4;
  
  plVar1 = *param_1;
  lVar3 = *plVar1;
  lVar4 = plVar1[2];
  *(long *)(lVar4 + 8) = lVar3;
  *(long *)(lVar4 + 0x10) = lVar3 + 0x18;
  while (puVar2 = (ulong *)FUN_00e2a204(plVar1), puVar2 != (ulong *)0x0) {
    *puVar2 = *puVar2 & 0xfffffffffffffffe;
    plVar1 = *param_1;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00dce938
// Address: 00e2d66c
// ==========================================================================================

undefined8 thunk_FUN_00dce938(void)

{
  void *pvVar1;
  
  pvVar1 = pthread_getspecific(*DAT_02107b00);
  return *(undefined8 *)(*(long *)((long)pvVar1 + 0x10) + 0x70);
}



// ==========================================================================================
// Function: thunk_FUN_00df875c
// Address: 00e2e5fc
// ==========================================================================================

long thunk_FUN_00df875c(void)

{
  timeval tStack_20;
  
  gettimeofday(&tStack_20,(__timezone_ptr_t)0x0);
  return tStack_20.tv_usec * 10 + tStack_20.tv_sec * 10000000 + 0x19db1ded53e8000;
}



// ==========================================================================================
// Function: thunk_FUN_00e119c0
// Address: 00e2e600
// ==========================================================================================

int thunk_FUN_00e119c0(ulong param_1)

{
  return ((uint)(param_1 >> 3) & 0x1fffffff) * -0x61c8864f;
}



// ==========================================================================================
// Function: thunk_FUN_00e11910
// Address: 00e2e604
// ==========================================================================================

long * thunk_FUN_00e11910(long *param_1)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  undefined *puVar4;
  long *plVar5;
  long lVar6;
  
  lVar6 = *param_1;
  if (*(char *)(lVar6 + 0x132) != '\0') {
    plVar5 = (long *)FUN_00e10e18(param_1);
    return plVar5;
  }
  iVar1 = *(int *)(lVar6 + 0xf8);
  plVar5 = (long *)FUN_00e3eaec((long)iVar1);
  *plVar5 = lVar6;
  puVar4 = PTR_DAT_01ff5430;
  do {
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
    if (bVar3) {
      *(long *)puVar4 = *(long *)puVar4 + 1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  memcpy(plVar5 + 2,param_1 + 2,(long)iVar1 - 0x10);
  if ((*(byte *)(*param_1 + 0x136) >> 1 & 1) != 0) {
    FUN_00e32cb0(plVar5);
  }
  if ((char)*PTR_DAT_01ff5438 < '\0') {
    FUN_00e2ae40(plVar5,*param_1);
  }
  return plVar5;
}



// ==========================================================================================
// Function: thunk_FUN_00e2af24
// Address: 00e31b0c
// ==========================================================================================

void thunk_FUN_00e2af24(undefined8 param_1)

{
  ulong uVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  
  uVar1 = DAT_02108958;
  puVar2 = DAT_02108950;
  puVar4 = DAT_02108950;
  if ((DAT_02108958 & 0x1fffffffffffffff) != 0) {
    do {
      puVar3 = (undefined8 *)*puVar4;
      if (((*(byte *)((long)puVar3 + 9) & 1) != 0) && (puVar3[6] != 0)) {
        (*(code *)puVar3[7])(*puVar3,param_1);
        uVar1 = DAT_02108958;
        puVar2 = DAT_02108950;
      }
      puVar4 = puVar4 + 1;
    } while (puVar4 != puVar2 + uVar1);
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e43fd8
// Address: 00e31b24
// ==========================================================================================

void thunk_FUN_00e43fd8(void)

{
  if (DAT_0231b338 != 0) {
    DAT_0231b338 = 0;
    DAT_0231b998 = 0;
    memset(&DAT_02108e00,0,0x2124e0);
    memset(&DAT_0231b340,0,0x1e8);
    memset(&DAT_0231b528,0,0x1e8);
    DAT_020ff218 = 0xffffffffffffffff;
    DAT_020ff180 = 8;
    DAT_020ff1d8 = 3;
    DAT_0231b310 = 0;
    DAT_0231b318 = 0;
    DAT_0231b920 = 0;
    DAT_0231b8f0 = 0;
    DAT_0231b8f8 = 0;
    DAT_0231b970 = 0;
    DAT_0231b940 = 0;
    DAT_0231b974 = 0;
    DAT_0231b978 = 0;
    PTR_thunk_FUN_00e44acc_020ff428 = thunk_FUN_00e44acc;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3dff0
// Address: 00e31b28
// ==========================================================================================

void thunk_FUN_00e3dff0(void)

{
  FUN_00e3ddec(0,0);
  if (DAT_0231b800 != 0) {
    FUN_00e3e01c();
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3c160
// Address: 00e31b2c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool thunk_FUN_00e3c160(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  int iVar4;
  
  if (DAT_0231b2f8 != 0) {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
  }
  if (DAT_0231b718 == 0) {
    FUN_00e3ce1c(1);
  }
  iVar4 = DAT_0231b940;
  if (DAT_0231b2f8 != 0) {
    _DAT_0231b300 = 0;
  }
  if ((DAT_0231b30c != 0) && (DAT_0231b940 == 0)) {
    (*DAT_0231b7c8)();
  }
  return iVar4 != 0;
}



// ==========================================================================================
// Function: thunk_FUN_00e3c140
// Address: 00e31b30
// ==========================================================================================

void thunk_FUN_00e3c140(void)

{
  if (DAT_0231b308 != 0) {
    DAT_0231b788 = 1;
    FUN_00e3c160();
    return;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e43c40
// Address: 00e31b50
// ==========================================================================================

long thunk_FUN_00e43c40(void)

{
  return DAT_02108e00 - DAT_02108ea0;
}



// ==========================================================================================
// Function: thunk_FUN_00e442b8
// Address: 00e31b54
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_00e442b8(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 == 0) {
    DAT_0231b718 = DAT_0231b718 + 1;
  }
  else {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
    DAT_0231b718 = DAT_0231b718 + 1;
    if (DAT_0231b2f8 != 0) {
      _DAT_0231b300 = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e44248
// Address: 00e31b58
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_00e44248(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 == 0) {
    DAT_0231b718 = DAT_0231b718 + -1;
  }
  else {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
    DAT_0231b718 = DAT_0231b718 + -1;
    if (DAT_0231b2f8 != 0) {
      _DAT_0231b300 = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e44498
// Address: 00e31d08
// ==========================================================================================

void thunk_FUN_00e44498(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 != 0) {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        DAT_0231b300 = '\x01';
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
  }
  FUN_00e3d320();
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e444d0
// Address: 00e31d0c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_00e444d0(void)

{
  FUN_00e3d400();
  if (DAT_0231b2f8 != 0) {
    _DAT_0231b300 = 0;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3ecd4
// Address: 00e31d10
// ==========================================================================================

void thunk_FUN_00e3ecd4(undefined8 param_1)

{
  FUN_00e41024(param_1,2);
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3ecdc
// Address: 00e31d14
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_00e3ecdc(undefined8 *param_1)

{
  byte bVar1;
  char cVar2;
  bool bVar3;
  char cVar4;
  undefined *puVar5;
  long lVar6;
  long *plVar7;
  ulong uVar8;
  
  if (param_1 != (undefined8 *)0x0) {
    plVar7 = (long *)(&DAT_023172e0 + ((ulong)param_1 >> 0x16 & 0x7ff) * 8);
    do {
      lVar6 = *plVar7;
      if (lVar6 == DAT_02108ea8) break;
      plVar7 = (long *)(lVar6 + 0x2018);
    } while (*(ulong *)(lVar6 + 0x2010) != (ulong)param_1 >> 0x16);
    lVar6 = *(long *)(lVar6 + ((ulong)param_1 >> 0xc & 0x3ff) * 8);
    uVar8 = *(ulong *)(lVar6 + 0x20);
    bVar1 = *(byte *)(lVar6 + 0x18);
    if (uVar8 < 0x810) {
      if (DAT_0231b2f8 != 0) {
        do {
          cVar4 = DAT_0231b300;
          cVar2 = '\x01';
          bVar3 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
          if (bVar3) {
            _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
            cVar2 = ExclusiveMonitorsStatus();
          }
        } while (cVar2 != '\0');
        if (cVar4 != '\0') {
          FUN_00e39788();
        }
      }
      DAT_02108e58 = DAT_02108e58 + uVar8;
      if (bVar1 == 2) {
        DAT_0231b738 = DAT_0231b738 - uVar8;
      }
      if ((8 < uVar8) && (*(int *)(&DAT_020ff244 + (ulong)bVar1 * 0x20) != 0)) {
        memset(param_1 + 1,0,uVar8 - 8);
      }
      puVar5 = (&PTR_DAT_020ff228)[(ulong)bVar1 * 4];
      *param_1 = *(undefined8 *)(puVar5 + (uVar8 >> 4) * 8);
      *(undefined8 **)(puVar5 + (uVar8 >> 4) * 8) = param_1;
      if (DAT_0231b2f8 != 0) {
        _DAT_0231b300 = 0;
      }
    }
    else {
      if (DAT_0231b2f8 != 0) {
        do {
          cVar4 = DAT_0231b300;
          cVar2 = '\x01';
          bVar3 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
          if (bVar3) {
            _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
            cVar2 = ExclusiveMonitorsStatus();
          }
        } while (cVar2 != '\0');
        if (cVar4 != '\0') {
          FUN_00e39788((ulong)param_1 & 0xfffffffffffff000);
        }
      }
      DAT_02108e58 = DAT_02108e58 + uVar8;
      if (bVar1 == 2) {
        DAT_0231b738 = DAT_0231b738 - uVar8;
      }
      if (0x1fff < uVar8 + 0xfff) {
        DAT_02108e28 = DAT_02108e28 - (uVar8 + 0xfff & 0xfffffffffffff000);
      }
      FUN_00e3bdb0((ulong)param_1 & 0xfffffffffffff000);
      if (DAT_0231b2f8 != 0) {
        _DAT_0231b300 = 0;
      }
    }
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e4448c
// Address: 00e31d18
// ==========================================================================================

undefined8 thunk_FUN_00e4448c(void)

{
  return DAT_020ff1b0;
}



// ==========================================================================================
// Function: thunk_FUN_00e44480
// Address: 00e31d1c
// ==========================================================================================

void thunk_FUN_00e44480(undefined8 param_1)

{
  DAT_020ff1b0 = param_1;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e44c80
// Address: 00e31d38
// ==========================================================================================

void thunk_FUN_00e44c80(undefined8 param_1,code *param_2)

{
  ulong uVar1;
  ulong uVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  long *plVar6;
  ulong uVar7;
  ulong uVar8;
  uint uVar9;
  ulong uVar10;
  
  if ((param_2 != (code *)0x0) && (DAT_0231b710 != 0)) {
    uVar10 = 0;
    uVar3 = DAT_0231b710;
    do {
      uVar7 = (&DAT_0218f2e0)[uVar10 * 2];
      uVar9 = (uint)uVar10;
      uVar1 = uVar7 + (&DAT_0218f2e8)[uVar10 * 2];
      while( true ) {
        uVar9 = uVar9 + 1;
        uVar10 = (ulong)uVar9;
        if ((uVar3 <= uVar10) || ((&DAT_0218f2e0)[uVar10 * 2] != uVar1)) break;
        uVar1 = uVar1 + (&DAT_0218f2e8)[uVar10 * 2];
      }
joined_r0x00e44d20:
      while (uVar7 < uVar1) {
        plVar6 = (long *)(&DAT_023172e0 + (uVar7 >> 0x16 & 0x7ff) * 8);
        do {
          lVar5 = *plVar6;
          if (lVar5 == DAT_02108ea8) break;
          plVar6 = (long *)(lVar5 + 0x2018);
        } while (*(ulong *)(lVar5 + 0x2010) != uVar7 >> 0x16);
        uVar4 = *(ulong *)(lVar5 + (uVar7 >> 0xc & 0x3ff) * 8);
        uVar3 = DAT_0231b710;
        if (uVar4 < 0x1000) {
          uVar7 = uVar7 + 0x1000;
        }
        else {
          lVar5 = *(long *)(uVar4 + 0x20);
          if ((*(byte *)(uVar4 + 0x19) >> 2 & 1) != 0) goto LAB_00e44db4;
          uVar2 = uVar7 + lVar5;
          if (uVar7 < uVar2) {
            (*param_2)(param_1,uVar7,uVar2);
          }
          uVar8 = uVar7 + (lVar5 + 0xfffU & 0xfffffffffffff000);
          uVar7 = uVar8;
          uVar3 = DAT_0231b710;
          if (uVar2 < uVar8) goto LAB_00e44dc4;
        }
      }
    } while (uVar10 < uVar3);
  }
  return;
LAB_00e44db4:
  uVar8 = uVar7 + lVar5;
  uVar2 = uVar7;
  uVar7 = uVar8;
  if ((*(byte *)(uVar4 + 0x19) >> 1 & 1) == 0) {
LAB_00e44dc4:
    (*param_2)(param_1,uVar2,uVar8);
    uVar7 = uVar8;
    uVar3 = DAT_0231b710;
  }
  goto joined_r0x00e44d20;
}



// ==========================================================================================
// Function: thunk_FUN_00e44e18
// Address: 00e31d3c
// ==========================================================================================

undefined8 thunk_FUN_00e44e18(void)

{
  undefined8 uStack_8;
  
  uStack_8 = 0;
  FUN_00e44c80(&uStack_8,FUN_00e44e08);
  return uStack_8;
}



// ==========================================================================================
// Function: thunk_FUN_00e4433c
// Address: 00e31d40
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_00e4433c(code *param_1,undefined8 param_2)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 != 0) {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
  }
  (*param_1)(param_2);
  if (DAT_0231b2f8 != 0) {
    _DAT_0231b300 = 0;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e3f8e0
// Address: 00e3fbd8
// ==========================================================================================

void thunk_FUN_00e3f8e0(ulong param_1)

{
  ulong *puVar1;
  ulong *puVar2;
  long lVar3;
  long *plVar4;
  ulong uVar5;
  
  puVar1 = DAT_02108e88;
  plVar4 = (long *)(&DAT_023172e0 + (param_1 >> 0x16 & 0x7ff) * 8);
  do {
    lVar3 = *plVar4;
    if (lVar3 == DAT_02108ea8) break;
    plVar4 = (long *)(lVar3 + 0x2018);
  } while (*(ulong *)(lVar3 + 0x2010) != param_1 >> 0x16);
  uVar5 = *(ulong *)(*(long *)(lVar3 + (param_1 >> 0xc & 0x3ff) * 8) + 0x28);
  if (uVar5 != 0) {
    puVar2 = DAT_02108e88 + 2;
    if ((ulong *)(DAT_02108e78 + DAT_0231b920 * 0x10) <= puVar2) {
      DAT_0231b940 = 5;
      DAT_0231b970 = 1;
      if (DAT_02108df8 != 0) {
        DAT_02108e88 = puVar2;
        FUN_00e38d00("Mark stack overflow; current size = %lu entries\n");
      }
      puVar2 = puVar1 + -0x3fe;
    }
    DAT_02108e88 = puVar2;
    *puVar2 = param_1;
    puVar2[1] = uVar5;
  }
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00e38854
// Address: 00e44110
// ==========================================================================================

void thunk_FUN_00e38854(char *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                       undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8)

{
  long lVar1;
  undefined auStack_4b0 [8];
  undefined8 uStack_4a8;
  undefined8 uStack_4a0;
  undefined8 uStack_498;
  undefined8 uStack_490;
  undefined8 uStack_488;
  undefined8 uStack_480;
  undefined8 uStack_478;
  undefined *puStack_470;
  undefined **ppuStack_468;
  undefined *puStack_460;
  undefined8 uStack_458;
  char acStack_42c [1024];
  char cStack_2c;
  long lStack_28;
  
  lVar1 = tpidr_el0;
  lStack_28 = *(long *)(lVar1 + 0x28);
  puStack_460 = auStack_4b0;
  ppuStack_468 = &puStack_470;
  cStack_2c = '\x15';
  uStack_458 = 0xffffff80ffffffc8;
  uStack_4a8 = param_2;
  uStack_4a0 = param_3;
  uStack_498 = param_4;
  uStack_490 = param_5;
  uStack_488 = param_6;
  uStack_480 = param_7;
  uStack_478 = param_8;
  puStack_470 = (undefined *)register0x00000008;
  vsnprintf(acStack_42c,0x400,param_1,&puStack_470);
  if (cStack_2c != '\x15') {
    (*(code *)PTR_FUN_020ff168)("GC_printf clobbered stack");
                    /* WARNING: Subroutine does not return */
    abort();
  }
  FUN_00e440b4(acStack_42c);
  if (*(long *)(lVar1 + 0x28) == lStack_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: thunk_FUN_00e44acc
// Address: 00e44ac8
// ==========================================================================================

void thunk_FUN_00e44acc(void)

{
  ulong *puVar1;
  pthread_t pVar2;
  undefined *puVar3;
  int iVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  uint uVar8;
  long lVar9;
  long *plVar10;
  
  pVar2 = pthread_self();
  if (DAT_0231bcc0 == 0) {
    FUN_00e43e78();
  }
  lVar9 = 0;
  puVar7 = (undefined *)0x0;
  uVar8 = 0;
  iVar4 = 0;
  do {
    for (plVar10 = (long *)(&DAT_0231bcc8)[lVar9]; plVar10 != (long *)0x0;
        plVar10 = (long *)*plVar10) {
      if ((*(byte *)(plVar10 + 4) & 1) == 0) {
        if (plVar10[1] == pVar2) {
          uVar8 = 1;
          puVar5 = &stack0xffffffffffffffa0;
        }
        else {
          puVar5 = (undefined *)plVar10[3];
        }
        puVar1 = (ulong *)(plVar10 + 5);
        if ((*(byte *)(plVar10 + 4) & 4) != 0) {
          puVar1 = &DAT_0231bc28;
        }
        if (puVar5 == (undefined *)0x0) {
          (*(code *)PTR_FUN_020ff168)("GC_push_all_stacks: sp not set!");
                    /* WARNING: Subroutine does not return */
          abort();
        }
        puVar3 = (undefined *)plVar10[6];
        puVar6 = (undefined *)*puVar1;
        if (((puVar3 != (undefined *)0x0) && (puVar3 <= puVar5)) && (puVar5 <= puVar3 + plVar10[7]))
        {
          puVar6 = puVar3 + plVar10[7];
        }
        iVar4 = iVar4 + 1;
        FUN_00e428d8(puVar5,puVar6);
        puVar7 = puVar6 + ((long)puVar7 - (long)puVar5);
      }
    }
    lVar9 = lVar9 + 1;
    if (lVar9 == 0x100) {
      if (DAT_02108df8 == 2) {
        FUN_00e38d00("Pushed %d thread stacks\n",iVar4);
      }
      if ((DAT_0231c4c8 | uVar8) == 0) {
        (*(code *)PTR_FUN_020ff168)("Collecting from unknown thread");
                    /* WARNING: Subroutine does not return */
        abort();
      }
      DAT_0231b778 = puVar7;
      return;
    }
  } while( true );
}



// ==========================================================================================
// Function: thunk_FUN_00e48ee0
// Address: 00e48edc
// ==========================================================================================

void thunk_FUN_00e48ee0(long param_1)

{
  int iVar1;
  long lVar2;
  
  if (*(int *)(param_1 + 0x1734) == 0x10) {
    lVar2 = *(long *)(param_1 + 0x28);
    *(long *)(param_1 + 0x28) = lVar2 + 1;
    iVar1 = 0;
    *(undefined *)(*(long *)(param_1 + 0x10) + lVar2) = *(undefined *)(param_1 + 0x1730);
    lVar2 = *(long *)(param_1 + 0x28);
    *(long *)(param_1 + 0x28) = lVar2 + 1;
    *(undefined *)(*(long *)(param_1 + 0x10) + lVar2) = *(undefined *)(param_1 + 0x1731);
    *(undefined2 *)(param_1 + 0x1730) = 0;
  }
  else {
    if (*(int *)(param_1 + 0x1734) < 8) {
      return;
    }
    lVar2 = *(long *)(param_1 + 0x28);
    *(long *)(param_1 + 0x28) = lVar2 + 1;
    *(undefined *)(*(long *)(param_1 + 0x10) + lVar2) = *(undefined *)(param_1 + 0x1730);
    *(ushort *)(param_1 + 0x1730) = (ushort)*(byte *)(param_1 + 0x1731);
    iVar1 = *(int *)(param_1 + 0x1734) + -8;
  }
  *(int *)(param_1 + 0x1734) = iVar1;
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00ead734
// Address: 00ead5d8
// ==========================================================================================

void thunk_FUN_00ead734(void)

{
  FUN_00ead734();
  return;
}



// ==========================================================================================
// Function: thunk_FUN_00db0dec
// Address: 01820694
// ==========================================================================================

void thunk_FUN_00db0dec(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: thunk_FUN_00db0de4
// Address: 019b9294
// ==========================================================================================

void thunk_FUN_00db0de4(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
