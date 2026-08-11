// Function: to_string
// Address: 00e90e14
// ==========================================================================================

/* std::__ndk1::to_string(int) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,int param_1)

{
  uint uVar1;
  long lVar2;
  uint uVar3;
  char *pcVar4;
  char *pcVar5;
  ulong *in_x8;
  undefined *__dest;
  ulong __n;
  ulong uVar6;
  char local_54 [11];
  char cStack_49;
  long local_48;
  
  uVar3 = (uint)this;
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pcVar5 = local_54;
  pcVar4 = &cStack_49;
  if ((int)uVar3 < 0) {
    pcVar5 = (char *)((ulong)pcVar5 | 1);
    uVar3 = -uVar3;
    local_54[0] = '-';
  }
  if ((9 < (long)pcVar4 - (long)pcVar5) ||
     (uVar1 = (uint)((0x20 - (int)LZCOUNT(uVar3 | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar1 - (uVar3 < *(uint *)(&DAT_00839e10 + (ulong)uVar1 * 4))) + 1) <=
     (long)pcVar4 - (long)pcVar5)) {
    pcVar4 = (char *)__itoa::__u32toa(uVar3,pcVar5);
  }
  __n = (long)pcVar4 - (long)local_54;
  if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)__n << 1);
  }
  else {
    uVar6 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar6);
    in_x8[1] = __n;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar6 | 1;
  }
  if (local_54 != pcVar4) {
    memcpy(__dest,local_54,__n);
    __dest = __dest + __n;
  }
  *__dest = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e90f50
// ==========================================================================================

/* std::__ndk1::to_string(long) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,long param_1)

{
  uint uVar1;
  long lVar2;
  long *plVar3;
  char *pcVar4;
  ulong *in_x8;
  undefined *__dest;
  ulong __n;
  ulong uVar5;
  long local_5c [2];
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pcVar4 = (char *)local_5c;
  plVar3 = &local_48;
  if ((long)this < 0) {
    pcVar4 = (char *)((ulong)pcVar4 | 1);
    this = (__ndk1 *)-(long)this;
    local_5c[0]._0_1_ = '-';
  }
  if ((0x13 < (long)plVar3 - (long)pcVar4) ||
     (uVar1 = (uint)((0x40 - (int)LZCOUNT((ulong)this | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar1 - (this < *(__ndk1 **)(&DAT_00839e38 + (ulong)uVar1 * 8))) + 1) <=
     (long)plVar3 - (long)pcVar4)) {
    plVar3 = (long *)__itoa::__u64toa((ulong)this,pcVar4);
  }
  __n = (long)plVar3 - (long)local_5c;
  if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)__n << 1);
  }
  else {
    uVar5 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar5);
    in_x8[1] = __n;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar5 | 1;
  }
  if (local_5c != plVar3) {
    memcpy(__dest,local_5c,__n);
    __dest = __dest + __n;
  }
  *__dest = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e9108c
// ==========================================================================================

/* std::__ndk1::to_string(long long) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,longlong param_1)

{
  uint uVar1;
  long lVar2;
  long *plVar3;
  char *pcVar4;
  ulong *in_x8;
  undefined *__dest;
  ulong __n;
  ulong uVar5;
  long local_5c [2];
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pcVar4 = (char *)local_5c;
  plVar3 = &local_48;
  if ((long)this < 0) {
    pcVar4 = (char *)((ulong)pcVar4 | 1);
    this = (__ndk1 *)-(long)this;
    local_5c[0]._0_1_ = '-';
  }
  if ((0x13 < (long)plVar3 - (long)pcVar4) ||
     (uVar1 = (uint)((0x40 - (int)LZCOUNT((ulong)this | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar1 - (this < *(__ndk1 **)(&DAT_00839e38 + (ulong)uVar1 * 8))) + 1) <=
     (long)plVar3 - (long)pcVar4)) {
    plVar3 = (long *)__itoa::__u64toa((ulong)this,pcVar4);
  }
  __n = (long)plVar3 - (long)local_5c;
  if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)__n << 1);
  }
  else {
    uVar5 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar5);
    in_x8[1] = __n;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar5 | 1;
  }
  if (local_5c != plVar3) {
    memcpy(__dest,local_5c,__n);
    __dest = __dest + __n;
  }
  *__dest = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e911c8
// ==========================================================================================

/* std::__ndk1::to_string(unsigned int) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,uint param_1)

{
  long lVar1;
  char *pcVar2;
  ulong *in_x8;
  long lVar3;
  ulong uVar4;
  undefined *__dest;
  ulong uVar5;
  ulong uVar6;
  char *pcVar7;
  char acStack_54 [12];
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  pcVar2 = (char *)__itoa::__u32toa((uint)this,acStack_54);
  uVar5 = (long)pcVar2 - (long)acStack_54;
  if (0xffffffffffffffef < uVar5) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar5 < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)uVar5 << 1);
  }
  else {
    uVar6 = uVar5 + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar6);
    in_x8[1] = uVar5;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar6 | 1;
  }
  pcVar7 = acStack_54;
  if (pcVar7 != pcVar2) {
    memcpy(__dest,acStack_54,uVar5);
    uVar5 = (long)pcVar2 - (long)pcVar7;
    if (1 < uVar5) {
      uVar4 = uVar5 & 0xfffffffffffffffe;
      pcVar7 = acStack_54 + uVar4;
      __dest = __dest + uVar4;
      uVar6 = uVar4;
      do {
        uVar6 = uVar6 - 2;
      } while (uVar6 != 0);
      if (uVar5 == uVar4) goto LAB_00e912a0;
    }
    lVar3 = (long)pcVar2 - (long)pcVar7;
    do {
      lVar3 = lVar3 + -1;
      __dest = __dest + 1;
    } while (lVar3 != 0);
  }
LAB_00e912a0:
  *__dest = 0;
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e912dc
// ==========================================================================================

/* std::__ndk1::to_string(unsigned long) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,ulong param_1)

{
  long lVar1;
  undefined *puVar2;
  ulong *in_x8;
  long lVar3;
  ulong uVar4;
  undefined *__dest;
  ulong uVar5;
  ulong uVar6;
  char *pcVar7;
  char acStack_60 [24];
  long local_48;
  
  pcVar7 = acStack_60;
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  puVar2 = (undefined *)__itoa::__u64toa((ulong)this,acStack_60);
  uVar5 = (long)puVar2 - (long)acStack_60;
  if (0xffffffffffffffef < uVar5) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar5 < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)uVar5 << 1);
  }
  else {
    uVar6 = uVar5 + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar6);
    in_x8[1] = uVar5;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar6 | 1;
  }
  if (acStack_60 != puVar2) {
    memcpy(__dest,acStack_60,uVar5);
    uVar5 = (long)puVar2 - (long)acStack_60;
    if (1 < uVar5) {
      uVar4 = uVar5 & 0xfffffffffffffffe;
      pcVar7 = acStack_60 + uVar4;
      __dest = __dest + uVar4;
      uVar6 = uVar4;
      do {
        uVar6 = uVar6 - 2;
      } while (uVar6 != 0);
      if (uVar5 == uVar4) goto LAB_00e913b4;
    }
    lVar3 = (long)puVar2 - (long)pcVar7;
    do {
      lVar3 = lVar3 + -1;
      __dest = __dest + 1;
    } while (lVar3 != 0);
  }
LAB_00e913b4:
  *__dest = 0;
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e913f0
// ==========================================================================================

/* std::__ndk1::to_string(unsigned long long) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,ulonglong param_1)

{
  long lVar1;
  undefined *puVar2;
  ulong *in_x8;
  long lVar3;
  ulong uVar4;
  undefined *__dest;
  ulong uVar5;
  ulong uVar6;
  char *pcVar7;
  char acStack_60 [24];
  long local_48;
  
  pcVar7 = acStack_60;
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  puVar2 = (undefined *)__itoa::__u64toa((ulong)this,acStack_60);
  uVar5 = (long)puVar2 - (long)acStack_60;
  if (0xffffffffffffffef < uVar5) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar5 < 0x17) {
    __dest = (undefined *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)uVar5 << 1);
  }
  else {
    uVar6 = uVar5 + 0x10 & 0xfffffffffffffff0;
    __dest = (undefined *)operator_new(uVar6);
    in_x8[1] = uVar5;
    in_x8[2] = (ulong)__dest;
    *in_x8 = uVar6 | 1;
  }
  if (acStack_60 != puVar2) {
    memcpy(__dest,acStack_60,uVar5);
    uVar5 = (long)puVar2 - (long)acStack_60;
    if (1 < uVar5) {
      uVar4 = uVar5 & 0xfffffffffffffffe;
      pcVar7 = acStack_60 + uVar4;
      __dest = __dest + uVar4;
      uVar6 = uVar4;
      do {
        uVar6 = uVar6 - 2;
      } while (uVar6 != 0);
      if (uVar5 == uVar4) goto LAB_00e914c8;
    }
    lVar3 = (long)puVar2 - (long)pcVar7;
    do {
      lVar3 = lVar3 + -1;
      __dest = __dest + 1;
    } while (lVar3 != 0);
  }
LAB_00e914c8:
  *__dest = 0;
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e91504
// ==========================================================================================

/* std::__ndk1::to_wstring(int) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,int param_1)

{
  byte bVar1;
  uint uVar2;
  long lVar3;
  uint uVar4;
  byte *pbVar5;
  byte *pbVar6;
  ulong *in_x8;
  byte *pbVar7;
  ulong uVar8;
  uint *puVar9;
  uint *puVar10;
  ulong uVar11;
  ulong uVar12;
  byte local_54 [11];
  byte bStack_49;
  long local_48;
  
  uVar4 = (uint)this;
  lVar3 = tpidr_el0;
  pbVar6 = local_54;
  pbVar5 = &bStack_49;
  local_48 = *(long *)(lVar3 + 0x28);
  if ((int)uVar4 < 0) {
    pbVar6 = (byte *)((ulong)pbVar6 | 1);
    uVar4 = -uVar4;
    local_54[0] = 0x2d;
  }
  if ((9 < (long)pbVar5 - (long)pbVar6) ||
     (uVar2 = (uint)((0x20 - (int)LZCOUNT(uVar4 | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar2 - (uVar4 < *(uint *)(&DAT_00839e10 + (ulong)uVar2 * 4))) + 1) <=
     (long)pbVar5 - (long)pbVar6)) {
    pbVar5 = (byte *)__itoa::__u32toa(uVar4,(char *)pbVar6);
  }
  uVar11 = (long)pbVar5 - (long)local_54;
  if (0x3fffffffffffffef < uVar11) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar11 < 5) {
    puVar10 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar11 << 1);
  }
  else {
    uVar12 = uVar11 + 4 & 0xfffffffffffffffc;
    puVar10 = (uint *)operator_new(uVar12 << 2);
    in_x8[1] = uVar11;
    in_x8[2] = (ulong)puVar10;
    *in_x8 = uVar12 | 1;
  }
  if (local_54 != pbVar5) {
    uVar11 = (long)pbVar5 - (long)local_54;
    pbVar6 = local_54;
    puVar9 = puVar10;
    if (1 < uVar11) {
      uVar8 = uVar11 & 0xfffffffffffffffe;
      puVar9 = puVar10 + 1;
      puVar10 = puVar10 + uVar8;
      pbVar6 = (byte *)((ulong)local_54 | 1);
      uVar12 = uVar8;
      do {
        bVar1 = *pbVar6;
        uVar12 = uVar12 - 2;
        puVar9[-1] = (uint)pbVar6[-1];
        *puVar9 = (uint)bVar1;
        puVar9 = puVar9 + 2;
        pbVar6 = pbVar6 + 2;
      } while (uVar12 != 0);
      pbVar6 = local_54 + uVar8;
      puVar9 = puVar10;
      if (uVar11 == uVar8) goto LAB_00e9164c;
    }
    do {
      pbVar7 = pbVar6 + 1;
      puVar10 = puVar9 + 1;
      *puVar9 = (uint)*pbVar6;
      pbVar6 = pbVar7;
      puVar9 = puVar10;
    } while (pbVar5 != pbVar7);
  }
LAB_00e9164c:
  *puVar10 = 0;
  if (*(long *)(lVar3 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e91688
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::to_wstring(long) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,long param_1)

{
  byte bVar1;
  uint uVar2;
  long lVar3;
  long *plVar4;
  char *pcVar5;
  ulong *in_x8;
  long *plVar6;
  ulong uVar8;
  uint *puVar9;
  byte *pbVar10;
  uint *puVar11;
  ulong uVar12;
  ulong uVar13;
  long local_5c [2];
  long local_48;
  long *plVar7;
  
  lVar3 = tpidr_el0;
  pcVar5 = (char *)local_5c;
  plVar4 = &local_48;
  local_48 = *(long *)(lVar3 + 0x28);
  if ((long)this < 0) {
    pcVar5 = (char *)((ulong)pcVar5 | 1);
    this = (__ndk1 *)-(long)this;
    local_5c[0]._0_1_ = '-';
  }
  if ((0x13 < (long)plVar4 - (long)pcVar5) ||
     (uVar2 = (uint)((0x40 - (int)LZCOUNT((ulong)this | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar2 - (this < *(__ndk1 **)(&DAT_00839e38 + (ulong)uVar2 * 8))) + 1) <=
     (long)plVar4 - (long)pcVar5)) {
    plVar4 = (long *)__itoa::__u64toa((ulong)this,pcVar5);
  }
  uVar12 = (long)plVar4 - (long)local_5c;
  if (0x3fffffffffffffef < uVar12) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar12 < 5) {
    puVar11 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar12 << 1);
  }
  else {
    uVar13 = uVar12 + 4 & 0xfffffffffffffffc;
    puVar11 = (uint *)operator_new(uVar13 << 2);
    in_x8[1] = uVar12;
    in_x8[2] = (ulong)puVar11;
    *in_x8 = uVar13 | 1;
  }
  if (local_5c != plVar4) {
    uVar12 = (long)plVar4 - (long)local_5c;
    plVar7 = local_5c;
    puVar9 = puVar11;
    if (1 < uVar12) {
      uVar8 = uVar12 & 0xfffffffffffffffe;
      puVar9 = puVar11 + 1;
      puVar11 = puVar11 + uVar8;
      pbVar10 = (byte *)((ulong)local_5c | 1);
      uVar13 = uVar8;
      do {
        bVar1 = *pbVar10;
        uVar13 = uVar13 - 2;
        puVar9[-1] = (uint)pbVar10[-1];
        *puVar9 = (uint)bVar1;
        puVar9 = puVar9 + 2;
        pbVar10 = pbVar10 + 2;
      } while (uVar13 != 0);
      plVar7 = (long *)((long)local_5c + uVar8);
      puVar9 = puVar11;
      if (uVar12 == uVar8) goto LAB_00e917d0;
    }
    do {
      plVar6 = (long *)((long)plVar7 + 1);
      puVar11 = puVar9 + 1;
      *puVar9 = (uint)*(byte *)plVar7;
      plVar7 = plVar6;
      puVar9 = puVar11;
    } while (plVar4 != plVar6);
  }
LAB_00e917d0:
  *puVar11 = 0;
  if (*(long *)(lVar3 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e9180c
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::to_wstring(long long) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,longlong param_1)

{
  byte bVar1;
  uint uVar2;
  long lVar3;
  long *plVar4;
  char *pcVar5;
  ulong *in_x8;
  long *plVar6;
  ulong uVar8;
  uint *puVar9;
  byte *pbVar10;
  uint *puVar11;
  ulong uVar12;
  ulong uVar13;
  long local_5c [2];
  long local_48;
  long *plVar7;
  
  lVar3 = tpidr_el0;
  pcVar5 = (char *)local_5c;
  plVar4 = &local_48;
  local_48 = *(long *)(lVar3 + 0x28);
  if ((long)this < 0) {
    pcVar5 = (char *)((ulong)pcVar5 | 1);
    this = (__ndk1 *)-(long)this;
    local_5c[0]._0_1_ = '-';
  }
  if ((0x13 < (long)plVar4 - (long)pcVar5) ||
     (uVar2 = (uint)((0x40 - (int)LZCOUNT((ulong)this | 1)) * 0x4d1) >> 0xc,
     (long)(int)((uVar2 - (this < *(__ndk1 **)(&DAT_00839e38 + (ulong)uVar2 * 8))) + 1) <=
     (long)plVar4 - (long)pcVar5)) {
    plVar4 = (long *)__itoa::__u64toa((ulong)this,pcVar5);
  }
  uVar12 = (long)plVar4 - (long)local_5c;
  if (0x3fffffffffffffef < uVar12) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar12 < 5) {
    puVar11 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar12 << 1);
  }
  else {
    uVar13 = uVar12 + 4 & 0xfffffffffffffffc;
    puVar11 = (uint *)operator_new(uVar13 << 2);
    in_x8[1] = uVar12;
    in_x8[2] = (ulong)puVar11;
    *in_x8 = uVar13 | 1;
  }
  if (local_5c != plVar4) {
    uVar12 = (long)plVar4 - (long)local_5c;
    plVar7 = local_5c;
    puVar9 = puVar11;
    if (1 < uVar12) {
      uVar8 = uVar12 & 0xfffffffffffffffe;
      puVar9 = puVar11 + 1;
      puVar11 = puVar11 + uVar8;
      pbVar10 = (byte *)((ulong)local_5c | 1);
      uVar13 = uVar8;
      do {
        bVar1 = *pbVar10;
        uVar13 = uVar13 - 2;
        puVar9[-1] = (uint)pbVar10[-1];
        *puVar9 = (uint)bVar1;
        puVar9 = puVar9 + 2;
        pbVar10 = pbVar10 + 2;
      } while (uVar13 != 0);
      plVar7 = (long *)((long)local_5c + uVar8);
      puVar9 = puVar11;
      if (uVar12 == uVar8) goto LAB_00e91954;
    }
    do {
      plVar6 = (long *)((long)plVar7 + 1);
      puVar11 = puVar9 + 1;
      *puVar9 = (uint)*(byte *)plVar7;
      plVar7 = plVar6;
      puVar9 = puVar11;
    } while (plVar4 != plVar6);
  }
LAB_00e91954:
  *puVar11 = 0;
  if (*(long *)(lVar3 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e91990
// ==========================================================================================

/* std::__ndk1::to_wstring(unsigned int) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,uint param_1)

{
  byte bVar1;
  long lVar2;
  byte *pbVar3;
  ulong *in_x8;
  byte *pbVar4;
  ulong uVar6;
  uint *puVar7;
  uint *puVar8;
  ulong uVar9;
  ulong uVar10;
  byte abStack_54 [12];
  long local_48;
  byte *pbVar5;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pbVar3 = (byte *)__itoa::__u32toa((uint)this,(char *)abStack_54);
  uVar9 = (long)pbVar3 - (long)abStack_54;
  if (0x3fffffffffffffef < uVar9) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar9 < 5) {
    puVar8 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar9 << 1);
  }
  else {
    uVar10 = uVar9 + 4 & 0xfffffffffffffffc;
    puVar8 = (uint *)operator_new(uVar10 << 2);
    in_x8[1] = uVar9;
    in_x8[2] = (ulong)puVar8;
    *in_x8 = uVar10 | 1;
  }
  if (abStack_54 != pbVar3) {
    uVar9 = (long)pbVar3 - (long)abStack_54;
    pbVar5 = abStack_54;
    puVar7 = puVar8;
    if (1 < uVar9) {
      uVar6 = uVar9 & 0xfffffffffffffffe;
      puVar7 = puVar8 + 1;
      puVar8 = puVar8 + uVar6;
      pbVar5 = (byte *)((ulong)abStack_54 | 1);
      uVar10 = uVar6;
      do {
        bVar1 = *pbVar5;
        uVar10 = uVar10 - 2;
        puVar7[-1] = (uint)pbVar5[-1];
        *puVar7 = (uint)bVar1;
        puVar7 = puVar7 + 2;
        pbVar5 = pbVar5 + 2;
      } while (uVar10 != 0);
      pbVar5 = abStack_54 + uVar6;
      puVar7 = puVar8;
      if (uVar9 == uVar6) goto LAB_00e91a74;
    }
    do {
      pbVar4 = pbVar5 + 1;
      puVar8 = puVar7 + 1;
      *puVar7 = (uint)*pbVar5;
      pbVar5 = pbVar4;
      puVar7 = puVar8;
    } while (pbVar3 != pbVar4);
  }
LAB_00e91a74:
  *puVar8 = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e91ab0
// ==========================================================================================

/* std::__ndk1::to_wstring(unsigned long) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,ulong param_1)

{
  byte bVar1;
  long lVar2;
  byte *pbVar3;
  ulong *in_x8;
  byte *pbVar4;
  ulong uVar6;
  uint *puVar7;
  uint *puVar8;
  ulong uVar9;
  ulong uVar10;
  byte abStack_60 [24];
  long local_48;
  byte *pbVar5;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pbVar3 = (byte *)__itoa::__u64toa((ulong)this,(char *)abStack_60);
  uVar9 = (long)pbVar3 - (long)abStack_60;
  if (0x3fffffffffffffef < uVar9) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar9 < 5) {
    puVar8 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar9 << 1);
  }
  else {
    uVar10 = uVar9 + 4 & 0xfffffffffffffffc;
    puVar8 = (uint *)operator_new(uVar10 << 2);
    in_x8[1] = uVar9;
    in_x8[2] = (ulong)puVar8;
    *in_x8 = uVar10 | 1;
  }
  if (abStack_60 != pbVar3) {
    uVar9 = (long)pbVar3 - (long)abStack_60;
    pbVar5 = abStack_60;
    puVar7 = puVar8;
    if (1 < uVar9) {
      uVar6 = uVar9 & 0xfffffffffffffffe;
      puVar7 = puVar8 + 1;
      puVar8 = puVar8 + uVar6;
      pbVar5 = (byte *)((ulong)abStack_60 | 1);
      uVar10 = uVar6;
      do {
        bVar1 = *pbVar5;
        uVar10 = uVar10 - 2;
        puVar7[-1] = (uint)pbVar5[-1];
        *puVar7 = (uint)bVar1;
        puVar7 = puVar7 + 2;
        pbVar5 = pbVar5 + 2;
      } while (uVar10 != 0);
      pbVar5 = abStack_60 + uVar6;
      puVar7 = puVar8;
      if (uVar9 == uVar6) goto LAB_00e91b94;
    }
    do {
      pbVar4 = pbVar5 + 1;
      puVar8 = puVar7 + 1;
      *puVar7 = (uint)*pbVar5;
      pbVar5 = pbVar4;
      puVar7 = puVar8;
    } while (pbVar3 != pbVar4);
  }
LAB_00e91b94:
  *puVar8 = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e91bd0
// ==========================================================================================

/* std::__ndk1::to_wstring(unsigned long long) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,ulonglong param_1)

{
  byte bVar1;
  long lVar2;
  byte *pbVar3;
  ulong *in_x8;
  byte *pbVar4;
  ulong uVar6;
  uint *puVar7;
  uint *puVar8;
  ulong uVar9;
  ulong uVar10;
  byte abStack_60 [24];
  long local_48;
  byte *pbVar5;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  pbVar3 = (byte *)__itoa::__u64toa((ulong)this,(char *)abStack_60);
  uVar9 = (long)pbVar3 - (long)abStack_60;
  if (0x3fffffffffffffef < uVar9) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar9 < 5) {
    puVar8 = (uint *)((long)in_x8 + 4);
    *(char *)in_x8 = (char)((int)uVar9 << 1);
  }
  else {
    uVar10 = uVar9 + 4 & 0xfffffffffffffffc;
    puVar8 = (uint *)operator_new(uVar10 << 2);
    in_x8[1] = uVar9;
    in_x8[2] = (ulong)puVar8;
    *in_x8 = uVar10 | 1;
  }
  if (abStack_60 != pbVar3) {
    uVar9 = (long)pbVar3 - (long)abStack_60;
    pbVar5 = abStack_60;
    puVar7 = puVar8;
    if (1 < uVar9) {
      uVar6 = uVar9 & 0xfffffffffffffffe;
      puVar7 = puVar8 + 1;
      puVar8 = puVar8 + uVar6;
      pbVar5 = (byte *)((ulong)abStack_60 | 1);
      uVar10 = uVar6;
      do {
        bVar1 = *pbVar5;
        uVar10 = uVar10 - 2;
        puVar7[-1] = (uint)pbVar5[-1];
        *puVar7 = (uint)bVar1;
        puVar7 = puVar7 + 2;
        pbVar5 = pbVar5 + 2;
      } while (uVar10 != 0);
      pbVar5 = abStack_60 + uVar6;
      puVar7 = puVar8;
      if (uVar9 == uVar6) goto LAB_00e91cb4;
    }
    do {
      pbVar4 = pbVar5 + 1;
      puVar8 = puVar7 + 1;
      *puVar7 = (uint)*pbVar5;
      pbVar5 = pbVar4;
      puVar7 = puVar8;
    } while (pbVar3 != pbVar4);
  }
LAB_00e91cb4:
  *puVar8 = 0;
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: to_string
// Address: 00e91cf0
// ==========================================================================================

/* std::__ndk1::to_string(float) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,float param_1)

{
  char *__s;
  long lVar1;
  uint uVar2;
  ulong uVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong local_60;
  ulong uStack_58;
  char *local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  uStack_58 = 0;
  local_50 = (char *)0x0;
  local_60 = 0;
                    /* try { // try from 00e91d2c to 00e91d3b has its CatchHandler @ 00e91e04 */
  FUN_00e926a4(&local_60,0x16);
  uVar4 = (ulong)((byte)local_60 >> 1);
  if ((local_60 & 1) != 0) {
    uVar4 = uStack_58;
  }
  do {
    __s = (char *)((ulong)&local_60 | 1);
    if (((byte)local_60 & 1) != 0) {
      __s = local_50;
    }
    uVar2 = snprintf(__s,uVar4 + 1,"%f",(double)param_1);
    if ((int)uVar2 < 0) {
      uVar3 = uVar4 << 1 | 1;
    }
    else {
      uVar3 = (ulong)uVar2;
      if (uVar3 <= uVar4) {
                    /* try { // try from 00e91db4 to 00e91dbb has its CatchHandler @ 00e91e00 */
        FUN_00e926a4(&local_60);
        in_x8[2] = (ulong)local_50;
        in_x8[1] = uStack_58;
        *in_x8 = local_60;
        if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return;
      }
    }
                    /* try { // try from 00e91da0 to 00e91dab has its CatchHandler @ 00e91e08 */
    FUN_00e926a4(&local_60,uVar3);
    uVar4 = uVar3;
  } while( true );
}



// ==========================================================================================
// Function: to_string
// Address: 00e91e24
// ==========================================================================================

/* std::__ndk1::to_string(double) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,double param_1)

{
  char *__s;
  long lVar1;
  uint uVar2;
  ulong uVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong local_60;
  ulong uStack_58;
  char *local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  uStack_58 = 0;
  local_50 = (char *)0x0;
  local_60 = 0;
                    /* try { // try from 00e91e60 to 00e91e6f has its CatchHandler @ 00e91f34 */
  FUN_00e926a4(&local_60,0x16);
  uVar4 = (ulong)((byte)local_60 >> 1);
  if ((local_60 & 1) != 0) {
    uVar4 = uStack_58;
  }
  do {
    __s = (char *)((ulong)&local_60 | 1);
    if (((byte)local_60 & 1) != 0) {
      __s = local_50;
    }
    uVar2 = snprintf(__s,uVar4 + 1,"%f",param_1);
    if ((int)uVar2 < 0) {
      uVar3 = uVar4 << 1 | 1;
    }
    else {
      uVar3 = (ulong)uVar2;
      if (uVar3 <= uVar4) {
                    /* try { // try from 00e91ee4 to 00e91eeb has its CatchHandler @ 00e91f30 */
        FUN_00e926a4(&local_60);
        in_x8[2] = (ulong)local_50;
        in_x8[1] = uStack_58;
        *in_x8 = local_60;
        if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return;
      }
    }
                    /* try { // try from 00e91ed0 to 00e91edb has its CatchHandler @ 00e91f38 */
    FUN_00e926a4(&local_60,uVar3);
    uVar4 = uVar3;
  } while( true );
}



// ==========================================================================================
// Function: to_string
// Address: 00e91f54
// ==========================================================================================

/* std::__ndk1::to_string(long double) */

void __thiscall std::__ndk1::to_string(__ndk1 *this,longdouble param_1)

{
  char *__s;
  long lVar1;
  uint uVar2;
  ulong uVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong local_60;
  ulong uStack_58;
  char *local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  uStack_58 = 0;
  local_50 = (char *)0x0;
  local_60 = 0;
                    /* try { // try from 00e91f8c to 00e91f9b has its CatchHandler @ 00e9205c */
  FUN_00e926a4(&local_60,0x16);
  uVar4 = (ulong)((byte)local_60 >> 1);
  if ((local_60 & 1) != 0) {
    uVar4 = uStack_58;
  }
  do {
    __s = (char *)((ulong)&local_60 | 1);
    if (((byte)local_60 & 1) != 0) {
      __s = local_50;
    }
    uVar2 = snprintf(__s,uVar4 + 1,"%Lf",param_1);
    if ((int)uVar2 < 0) {
      uVar3 = uVar4 << 1 | 1;
    }
    else {
      uVar3 = (ulong)uVar2;
      if (uVar3 <= uVar4) {
                    /* try { // try from 00e92010 to 00e92017 has its CatchHandler @ 00e92058 */
        FUN_00e926a4(&local_60);
        in_x8[2] = (ulong)local_50;
        in_x8[1] = uStack_58;
        *in_x8 = local_60;
        if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return;
      }
    }
                    /* try { // try from 00e91ffc to 00e92007 has its CatchHandler @ 00e92060 */
    FUN_00e926a4(&local_60,uVar3);
    uVar4 = uVar3;
  } while( true );
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e9207c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::to_wstring(float) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,float param_1)

{
  long lVar1;
  uint uVar2;
  wchar_t *pwVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong uVar5;
  ulong uVar6;
  undefined8 local_70;
  ulong uStack_68;
  wchar_t *local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  pwVar3 = (wchar_t *)operator_new(0x60);
  uStack_68 = _UNK_005be0b8;
  local_70 = _DAT_005be0b0;
  local_60 = pwVar3;
                    /* try { // try from 00e920cc to 00e920d7 has its CatchHandler @ 00e9225c */
  wmemset(pwVar3,L'\0',0x14);
  pwVar3[0x14] = L'\0';
                    /* try { // try from 00e920dc to 00e920ef has its CatchHandler @ 00e92258 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_70,3,L'\0');
  uVar4 = local_70 & 0xff;
  uVar5 = local_70 >> 1 & 0x7f;
  if ((local_70 & 1) != 0) {
    uVar5 = uStack_68;
  }
  do {
    while( true ) {
      pwVar3 = (wchar_t *)((ulong)&local_70 | 4);
      if ((uVar4 & 1) != 0) {
        pwVar3 = local_60;
      }
      uVar2 = swprintf(pwVar3,uVar5 + 1,L"%f",(double)param_1);
      if (-1 < (int)uVar2) break;
      uVar6 = uVar5 << 1 | 1;
      if ((local_70 & 1) == 0) goto LAB_00e92164;
LAB_00e9219c:
      uVar5 = uStack_68;
      if (uStack_68 < uVar6) {
LAB_00e92118:
                    /* try { // try from 00e9211c to 00e92147 has its CatchHandler @ 00e92260 */
        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
        append((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&local_70,uVar6 - uVar5,L'\0');
      }
      else {
        local_60[uVar6] = L'\0';
        uStack_68 = uVar6;
      }
      uVar4 = local_70 & 0xff;
      uVar5 = uVar6;
    }
    uVar6 = (ulong)uVar2;
    if (uVar6 <= uVar5) break;
    if ((local_70 & 1) != 0) goto LAB_00e9219c;
LAB_00e92164:
    uVar5 = (ulong)((byte)local_70 >> 1);
    if ((byte)local_70 >> 1 < uVar6) goto LAB_00e92118;
    *(undefined4 *)((long)&local_70 + uVar6 * 4 + 4) = 0;
    local_70 = CONCAT71(local_70._1_7_,(char)((int)uVar6 << 1));
    uVar4 = 0;
    uVar5 = uVar6;
  } while( true );
  if ((local_70 & 1) == 0) {
    uVar5 = (ulong)((byte)local_70 >> 1);
    if (uVar6 <= (byte)local_70 >> 1) {
      *(undefined4 *)((long)&local_70 + uVar6 * 4 + 4) = 0;
      local_70 = CONCAT71(local_70._1_7_,(char)(uVar2 << 1));
      goto LAB_00e92210;
    }
  }
  else {
    uVar5 = uStack_68;
    if (uVar6 <= uStack_68) {
      local_60[uVar6] = L'\0';
      uStack_68 = uVar6;
      goto LAB_00e92210;
    }
  }
                    /* try { // try from 00e921f4 to 00e921ff has its CatchHandler @ 00e92254 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_70,uVar6 - uVar5,L'\0');
LAB_00e92210:
  in_x8[2] = (ulong)local_60;
  in_x8[1] = uStack_68;
  *in_x8 = local_70;
  if (*(long *)(lVar1 + 0x28) != local_58) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e9227c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::to_wstring(double) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,double param_1)

{
  long lVar1;
  uint uVar2;
  wchar_t *pwVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong uVar5;
  ulong uVar6;
  undefined8 local_70;
  ulong uStack_68;
  wchar_t *local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  pwVar3 = (wchar_t *)operator_new(0x60);
  uStack_68 = _UNK_005be0b8;
  local_70 = _DAT_005be0b0;
  local_60 = pwVar3;
                    /* try { // try from 00e922cc to 00e922d7 has its CatchHandler @ 00e92458 */
  wmemset(pwVar3,L'\0',0x14);
  pwVar3[0x14] = L'\0';
                    /* try { // try from 00e922dc to 00e922ef has its CatchHandler @ 00e92454 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_70,3,L'\0');
  uVar4 = local_70 & 0xff;
  uVar5 = local_70 >> 1 & 0x7f;
  if ((local_70 & 1) != 0) {
    uVar5 = uStack_68;
  }
  do {
    while( true ) {
      pwVar3 = (wchar_t *)((ulong)&local_70 | 4);
      if ((uVar4 & 1) != 0) {
        pwVar3 = local_60;
      }
      uVar2 = swprintf(pwVar3,uVar5 + 1,L"%f",param_1);
      if (-1 < (int)uVar2) break;
      uVar6 = uVar5 << 1 | 1;
      if ((local_70 & 1) == 0) goto LAB_00e92360;
LAB_00e92398:
      uVar5 = uStack_68;
      if (uStack_68 < uVar6) {
LAB_00e92314:
                    /* try { // try from 00e92318 to 00e92343 has its CatchHandler @ 00e9245c */
        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
        append((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&local_70,uVar6 - uVar5,L'\0');
      }
      else {
        local_60[uVar6] = L'\0';
        uStack_68 = uVar6;
      }
      uVar4 = local_70 & 0xff;
      uVar5 = uVar6;
    }
    uVar6 = (ulong)uVar2;
    if (uVar6 <= uVar5) break;
    if ((local_70 & 1) != 0) goto LAB_00e92398;
LAB_00e92360:
    uVar5 = (ulong)((byte)local_70 >> 1);
    if ((byte)local_70 >> 1 < uVar6) goto LAB_00e92314;
    *(undefined4 *)((long)&local_70 + uVar6 * 4 + 4) = 0;
    local_70 = CONCAT71(local_70._1_7_,(char)((int)uVar6 << 1));
    uVar4 = 0;
    uVar5 = uVar6;
  } while( true );
  if ((local_70 & 1) == 0) {
    uVar5 = (ulong)((byte)local_70 >> 1);
    if (uVar6 <= (byte)local_70 >> 1) {
      *(undefined4 *)((long)&local_70 + uVar6 * 4 + 4) = 0;
      local_70 = CONCAT71(local_70._1_7_,(char)(uVar2 << 1));
      goto LAB_00e9240c;
    }
  }
  else {
    uVar5 = uStack_68;
    if (uVar6 <= uStack_68) {
      local_60[uVar6] = L'\0';
      uStack_68 = uVar6;
      goto LAB_00e9240c;
    }
  }
                    /* try { // try from 00e923f0 to 00e923fb has its CatchHandler @ 00e92450 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_70,uVar6 - uVar5,L'\0');
LAB_00e9240c:
  in_x8[2] = (ulong)local_60;
  in_x8[1] = uStack_68;
  *in_x8 = local_70;
  if (*(long *)(lVar1 + 0x28) != local_58) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
// Function: to_wstring
// Address: 00e92478
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::to_wstring(long double) */

void __thiscall std::__ndk1::to_wstring(__ndk1 *this,longdouble param_1)

{
  long lVar1;
  uint uVar2;
  wchar_t *pwVar3;
  ulong *in_x8;
  ulong uVar4;
  ulong uVar5;
  ulong uVar6;
  undefined8 local_60;
  ulong uStack_58;
  wchar_t *local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  pwVar3 = (wchar_t *)operator_new(0x60);
  uStack_58 = _UNK_005be0b8;
  local_60 = _DAT_005be0b0;
  local_50 = pwVar3;
                    /* try { // try from 00e924c4 to 00e924cf has its CatchHandler @ 00e9264c */
  wmemset(pwVar3,L'\0',0x14);
  pwVar3[0x14] = L'\0';
                    /* try { // try from 00e924d4 to 00e924e7 has its CatchHandler @ 00e92648 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_60,3,L'\0');
  uVar4 = local_60 & 0xff;
  uVar5 = local_60 >> 1 & 0x7f;
  if ((local_60 & 1) != 0) {
    uVar5 = uStack_58;
  }
  do {
    while( true ) {
      pwVar3 = (wchar_t *)((ulong)&local_60 | 4);
      if ((uVar4 & 1) != 0) {
        pwVar3 = local_50;
      }
      uVar2 = swprintf(pwVar3,uVar5 + 1,L"%Lf",param_1);
      if (-1 < (int)uVar2) break;
      uVar6 = uVar5 << 1 | 1;
      if ((local_60 & 1) == 0) goto LAB_00e92558;
LAB_00e92590:
      uVar5 = uStack_58;
      if (uStack_58 < uVar6) {
LAB_00e9250c:
                    /* try { // try from 00e92510 to 00e9253b has its CatchHandler @ 00e92650 */
        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
        append((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&local_60,uVar6 - uVar5,L'\0');
      }
      else {
        local_50[uVar6] = L'\0';
        uStack_58 = uVar6;
      }
      uVar4 = local_60 & 0xff;
      uVar5 = uVar6;
    }
    uVar6 = (ulong)uVar2;
    if (uVar6 <= uVar5) break;
    if ((local_60 & 1) != 0) goto LAB_00e92590;
LAB_00e92558:
    uVar5 = (ulong)((byte)local_60 >> 1);
    if ((byte)local_60 >> 1 < uVar6) goto LAB_00e9250c;
    *(undefined4 *)((long)&local_60 + uVar6 * 4 + 4) = 0;
    local_60 = CONCAT71(local_60._1_7_,(char)((int)uVar6 << 1));
    uVar4 = 0;
    uVar5 = uVar6;
  } while( true );
  if ((local_60 & 1) == 0) {
    uVar5 = (ulong)((byte)local_60 >> 1);
    if (uVar6 <= (byte)local_60 >> 1) {
      *(undefined4 *)((long)&local_60 + uVar6 * 4 + 4) = 0;
      local_60 = CONCAT71(local_60._1_7_,(char)(uVar2 << 1));
      goto LAB_00e92604;
    }
  }
  else {
    uVar5 = uStack_58;
    if (uVar6 <= uStack_58) {
      local_50[uVar6] = L'\0';
      uStack_58 = uVar6;
      goto LAB_00e92604;
    }
  }
                    /* try { // try from 00e925e8 to 00e925f3 has its CatchHandler @ 00e92644 */
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::append
            ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              *)&local_60,uVar6 - uVar5,L'\0');
LAB_00e92604:
  in_x8[2] = (ulong)local_50;
  in_x8[1] = uStack_58;
  *in_x8 = local_60;
  if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
