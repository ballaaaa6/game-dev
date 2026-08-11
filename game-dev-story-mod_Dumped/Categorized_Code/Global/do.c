// Function: do_compare
// Address: 00e5b7c0
// ==========================================================================================

/* std::__ndk1::collate<char>::do_compare(char const*, char const*, char const*, char const*) const
    */

ulong __thiscall
std::__ndk1::collate<char>::do_compare
          (collate<char> *this,char *param_1,char *param_2,char *param_3,char *param_4)

{
  if (param_3 != param_4) {
    do {
      if (param_2 == param_1) {
        return 0xffffffff;
      }
      if ((byte)*param_1 < (byte)*param_3) {
        return 0xffffffff;
      }
      if ((byte)*param_3 < (byte)*param_1) {
        return 1;
      }
      param_3 = (char *)((byte *)param_3 + 1);
      param_1 = (char *)((byte *)param_1 + 1);
    } while (param_4 != param_3);
  }
  return (ulong)(param_1 != param_2);
}



// ==========================================================================================
// Function: do_transform
// Address: 00e5b818
// ==========================================================================================

/* std::__ndk1::collate<char>::do_transform(char const*, char const*) const */

char * std::__ndk1::collate<char>::do_transform(char *param_1,char *param_2)

{
  char *in_x2;
  ulong *in_x8;
  char *__dest;
  ulong __n;
  ulong uVar1;
  
  __n = (long)in_x2 - (long)param_2;
  if (__n < 0xfffffffffffffff0) {
    if (__n < 0x17) {
      __dest = (char *)((long)in_x8 + 1);
      *(char *)in_x8 = (char)((int)__n << 1);
    }
    else {
      uVar1 = __n + 0x10 & 0xfffffffffffffff0;
      __dest = (char *)operator_new(uVar1);
      in_x8[1] = __n;
      in_x8[2] = (ulong)__dest;
      *in_x8 = uVar1 | 1;
      param_1 = __dest;
    }
    if (param_2 != in_x2) {
      param_1 = (char *)memcpy(__dest,param_2,__n);
      __dest = __dest + __n;
    }
    *__dest = '\0';
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: do_hash
// Address: 00e5b8c4
// ==========================================================================================

/* std::__ndk1::collate<char>::do_hash(char const*, char const*) const */

ulong __thiscall
std::__ndk1::collate<char>::do_hash(collate<char> *this,char *param_1,char *param_2)

{
  ulong uVar1;
  byte *pbVar2;
  ulong uVar3;
  
  if (param_1 != param_2) {
    uVar1 = 0;
    do {
      pbVar2 = (byte *)param_1 + 1;
      uVar1 = (ulong)(byte)*param_1 + uVar1 * 0x10;
      uVar3 = uVar1 & 0xf000000000000000;
      uVar1 = (uVar3 | uVar3 >> 0x38) ^ uVar1;
      param_1 = (char *)pbVar2;
    } while ((byte *)param_2 != pbVar2);
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: do_compare
// Address: 00e5b930
// ==========================================================================================

/* std::__ndk1::collate<wchar_t>::do_compare(wchar_t const*, wchar_t const*, wchar_t const*, wchar_t
   const*) const */

ulong __thiscall
std::__ndk1::collate<wchar_t>::do_compare
          (collate<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t *param_4)

{
  if (param_3 != param_4) {
    do {
      if (param_2 == param_1) {
        return 0xffffffff;
      }
      if ((uint)*param_1 < (uint)*param_3) {
        return 0xffffffff;
      }
      if ((uint)*param_3 < (uint)*param_1) {
        return 1;
      }
      param_3 = param_3 + 1;
      param_1 = param_1 + 1;
    } while (param_4 != param_3);
  }
  return (ulong)(param_1 != param_2);
}



// ==========================================================================================
// Function: do_transform
// Address: 00e5b988
// ==========================================================================================

/* std::__ndk1::collate<wchar_t>::do_transform(wchar_t const*, wchar_t const*) const */

wchar_t * std::__ndk1::collate<wchar_t>::do_transform(wchar_t *param_1,wchar_t *param_2)

{
  ulong uVar1;
  wchar_t *in_x2;
  ulong *in_x8;
  wchar_t *__dest;
  ulong uVar2;
  ulong uVar3;
  
  uVar1 = (long)in_x2 - (long)param_2;
  if (-1 < (long)uVar1) {
    uVar2 = (long)uVar1 >> 2;
    if (uVar2 < 5) {
      __dest = (wchar_t *)((long)in_x8 + 4);
      *(byte *)in_x8 = (byte)(uVar1 >> 1) & 0xfe;
    }
    else {
      uVar3 = uVar2 + 4 & 0xfffffffffffffffc;
      __dest = (wchar_t *)operator_new(uVar3 << 2);
      in_x8[1] = uVar2;
      in_x8[2] = (ulong)__dest;
      *in_x8 = uVar3 | 1;
      param_1 = __dest;
    }
    if (param_2 != in_x2) {
      param_1 = (wchar_t *)memcpy(__dest,param_2,uVar1 & 0xfffffffffffffffc);
      __dest = (wchar_t *)((long)__dest + (uVar1 - 4 & 0xfffffffffffffffc) + 4);
    }
    *__dest = L'\0';
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: do_hash
// Address: 00e5ba44
// ==========================================================================================

/* std::__ndk1::collate<wchar_t>::do_hash(wchar_t const*, wchar_t const*) const */

ulong __thiscall
std::__ndk1::collate<wchar_t>::do_hash(collate<wchar_t> *this,wchar_t *param_1,wchar_t *param_2)

{
  ulong uVar1;
  wchar_t *pwVar2;
  ulong uVar3;
  
  if (param_1 != param_2) {
    uVar1 = 0;
    do {
      pwVar2 = param_1 + 1;
      uVar1 = (ulong)(uint)*param_1 + uVar1 * 0x10;
      uVar3 = uVar1 & 0xf000000000000000;
      uVar1 = (uVar3 | uVar3 >> 0x38) ^ uVar1;
      param_1 = pwVar2;
    } while (param_2 != pwVar2);
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5ba7c
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, bool&) const */

ulong __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      bool *param_5)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  ulong uVar4;
  undefined **ppuVar5;
  long lVar6;
  long *plVar7;
  long local_a8;
  ulong local_a0;
  undefined ***local_98;
  undefined **local_90;
  undefined *local_88;
  undefined *puStack_80;
  void *local_78;
  byte local_70 [16];
  void *local_60;
  long local_58;
  
  local_a0 = (ulong)param_1;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if (((byte)param_3[8] & 1) == 0) {
    local_88 = (undefined *)0xffffffffffffffff;
    uVar4 = (**(code **)(*(long *)this + 0x20))(this,local_a0,param_2,param_3,param_4,&local_88);
    local_a0 = uVar4;
    if (local_88 == (undefined *)0x1) {
      *param_5 = true;
    }
    else if (local_88 == (undefined *)0x0) {
      *param_5 = false;
    }
    else {
      *param_5 = true;
      *param_4 = 4;
    }
  }
  else {
    ios_base::getloc();
    puVar3 = PTR___init_01ff5688;
    puVar2 = PTR_id_01ff5500;
    local_78 = (void *)0x0;
    local_88 = PTR_id_01ff5500;
    puStack_80 = PTR___init_01ff5688;
    if (*(long *)PTR_id_01ff5500 != -1) {
      local_90 = &local_88;
      local_98 = &local_90;
                    /* try { // try from 00e5bb48 to 00e5bb5f has its CatchHandler @ 00e5bd24 */
      __call_once((ulong *)PTR_id_01ff5500,&local_98,FUN_00e87ff8);
    }
    if (((ulong)(*(long *)(local_a8 + 0x18) - *(long *)(local_a8 + 0x10) >> 3) <=
         (long)*(int *)(puVar2 + 8) - 1U) ||
       (lVar6 = *(long *)(*(long *)(local_a8 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
       lVar6 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e5bcd0 to 00e5bcd3 has its CatchHandler @ 00e5bd24 */
      FUN_00de5da0();
    }
    __shared_count::__release_shared();
    ios_base::getloc();
    puVar2 = PTR_id_01ff5690;
    local_78 = (void *)0x0;
    local_88 = PTR_id_01ff5690;
    puStack_80 = puVar3;
    if (*(long *)PTR_id_01ff5690 != -1) {
      local_90 = &local_88;
      local_98 = &local_90;
                    /* try { // try from 00e5bbc0 to 00e5bbd7 has its CatchHandler @ 00e5bd20 */
      __call_once((ulong *)PTR_id_01ff5690,&local_98,FUN_00e87ff8);
    }
    if (((ulong)(*(long *)(local_a8 + 0x18) - *(long *)(local_a8 + 0x10) >> 3) <=
         (long)*(int *)(puVar2 + 8) - 1U) ||
       (plVar7 = *(long **)(*(long *)(local_a8 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
       plVar7 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e5bcd4 to 00e5bcd7 has its CatchHandler @ 00e5bd20 */
      FUN_00de5da0();
    }
    __shared_count::__release_shared();
                    /* try { // try from 00e5bc08 to 00e5bc17 has its CatchHandler @ 00e5bd1c */
    (**(code **)(*plVar7 + 0x30))(&local_88,plVar7);
                    /* try { // try from 00e5bc24 to 00e5bc2b has its CatchHandler @ 00e5bd08 */
    (**(code **)(*plVar7 + 0x38))(local_70,plVar7);
                    /* try { // try from 00e5bc34 to 00e5bc4f has its CatchHandler @ 00e5bcdc */
    ppuVar5 = (undefined **)FUN_00e5bd3c(&local_a0,param_2,&local_88,&local_58,lVar6,param_4,1);
    uVar4 = local_a0;
    *param_5 = ppuVar5 == &local_88;
    if ((local_70[0] & 1) != 0) {
      operator_delete(local_60);
    }
    if (((ulong)local_88 & 1) != 0) {
      operator_delete(local_78);
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get
// Address: 00e5c1c0
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      long *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_signed<long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5c570
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      longlong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_signed<long_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5c920
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, unsigned short&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      ushort *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_short>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5ccd0
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, unsigned int&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      uint *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_int>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5d080
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, unsigned long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      ulong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5d430
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, unsigned long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      ulonglong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_long_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5d7e0
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, float&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      float *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<float>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5db74
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, double&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      double *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<double>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5df08
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, long double&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      longdouble *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<long_double>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5e29c
// ==========================================================================================

/* std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, void*&) const */

long * __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
      void **param_5)

{
  ulong uVar1;
  long lVar2;
  undefined *puVar3;
  char cVar4;
  int iVar5;
  long *plVar6;
  long *plVar7;
  long *plVar8;
  ulong uVar9;
  undefined ***pppuVar10;
  undefined ***pppuVar11;
  uint local_174;
  undefined **local_170;
  ulong local_168;
  undefined ***local_160;
  undefined **local_158;
  ulong local_150;
  undefined8 uStack_148;
  void *local_140;
  undefined ***local_138;
  undefined *local_130;
  undefined *puStack_128;
  undefined8 local_120;
  char acStack_8c [28];
  long local_70;
  
  plVar8 = (long *)(ulong)param_2;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  local_150 = 0;
  uStack_148 = 0;
  local_140 = (void *)0x0;
                    /* try { // try from 00e5e2e8 to 00e5e2ef has its CatchHandler @ 00e5e6ac */
  ios_base::getloc();
  puVar3 = PTR_id_01ff5500;
  local_120 = 0;
  local_130 = PTR_id_01ff5500;
  puStack_128 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_170 = &local_130;
    local_138 = &local_170;
                    /* try { // try from 00e5e328 to 00e5e37b has its CatchHandler @ 00e5e6c0 */
    __call_once((ulong *)PTR_id_01ff5500,&local_138,FUN_00e87ff8);
  }
  if (((ulong)((long)local_158[3] - (long)local_158[2] >> 3) <= (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar6 = *(long **)(local_158[2] + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar6 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e5e650 to 00e5e653 has its CatchHandler @ 00e5e6c0 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar6 + 0x40))(plVar6,PTR___src_01ff5698,PTR___src_01ff5698 + 0x1a,acStack_8c);
  __shared_count::__release_shared();
  local_170 = (undefined **)0x0;
  local_168 = 0;
  local_160 = (undefined ***)0x0;
                    /* try { // try from 00e5e394 to 00e5e3a7 has its CatchHandler @ 00e5e6a8 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_170,0x16,'\0');
  pppuVar11 = (undefined ***)((ulong)&local_170 | 1);
  local_158 = &local_130;
  pppuVar10 = pppuVar11;
  if (((ulong)local_170 & 1) != 0) {
    pppuVar10 = local_160;
  }
  local_174 = 0;
  plVar6 = (long *)(ulong)param_1;
  local_138 = pppuVar10;
LAB_00e5e3e4:
  plVar7 = plVar6;
  if ((plVar6 == (long *)0x0) || (plVar6[3] != plVar6[4])) {
    if (plVar8 == (long *)0x0) goto LAB_00e5e440;
LAB_00e5e3f8:
                    /* try { // try from 00e5e40c to 00e5e433 has its CatchHandler @ 00e5e6e0 */
    if ((plVar8[3] == plVar8[4]) && (iVar5 = (**(code **)(*plVar8 + 0x48))(plVar8), iVar5 == -1))
    goto LAB_00e5e440;
    if (plVar7 != (long *)0x0) goto LAB_00e5e524;
  }
  else {
    iVar5 = (**(code **)(*plVar6 + 0x48))(plVar6);
    plVar7 = (long *)0x0;
    if (iVar5 != -1) {
      plVar7 = plVar6;
    }
    if (plVar8 != (long *)0x0) goto LAB_00e5e3f8;
LAB_00e5e440:
    plVar8 = (long *)0x0;
    if (plVar7 == (long *)0x0) goto LAB_00e5e524;
  }
  uVar9 = local_168;
  if (((ulong)local_170 & 1) == 0) {
    uVar9 = (ulong)local_170 >> 1 & 0x7f;
  }
  if (local_138 == (undefined ***)((long)pppuVar10 + uVar9)) {
                    /* try { // try from 00e5e470 to 00e5e49f has its CatchHandler @ 00e5e6dc */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_170,uVar9 << 1,'\0');
    uVar1 = 0x16;
    if (((ulong)local_170 & 1) != 0) {
      uVar1 = ((ulong)local_170 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_170,uVar1,'\0');
    pppuVar10 = pppuVar11;
    if (((ulong)local_170 & 1) != 0) {
      pppuVar10 = local_160;
    }
    local_138 = (undefined ***)((long)pppuVar10 + uVar9);
  }
  if ((char *)plVar7[3] == (char *)plVar7[4]) {
                    /* try { // try from 00e5e4d4 to 00e5e51f has its CatchHandler @ 00e5e6e0 */
    cVar4 = (**(code **)(*plVar7 + 0x48))(plVar7);
  }
  else {
    cVar4 = *(char *)plVar7[3];
  }
  iVar5 = __num_get<char>::__stage2_int_loop
                    (cVar4,0x10,(char *)pppuVar10,(char **)&local_138,&local_174,'\0',
                     (basic_string *)&local_150,(uint *)&local_130,(uint **)&local_158,acStack_8c);
  if (iVar5 != 0) goto LAB_00e5e524;
  plVar6 = plVar7;
  if (plVar7[3] == plVar7[4]) {
    (**(code **)(*plVar7 + 0x50))(plVar7);
  }
  else {
    plVar7[3] = plVar7[3] + 1;
  }
  goto LAB_00e5e3e4;
LAB_00e5e524:
                    /* try { // try from 00e5e52c to 00e5e63b has its CatchHandler @ 00e5e6bc */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_170,(long)local_138 - (long)pppuVar10,'\0');
  if (((ulong)local_170 & 1) != 0) {
    pppuVar11 = local_160;
  }
  if (((DAT_0231cfb0 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_0231cfb0), iVar5 != 0)) {
                    /* try { // try from 00e5e664 to 00e5e677 has its CatchHandler @ 00e5e694 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar5 = __libcpp_sscanf_l((char *)pppuVar11,(__locale_t *)DAT_0231cfa8,"%p",param_5);
  if (iVar5 != 1) {
    *param_4 = 4;
  }
  plVar6 = plVar7;
  if ((plVar7 == (long *)0x0) || (plVar7[3] != plVar7[4])) {
    if (plVar8 != (long *)0x0) goto LAB_00e5e59c;
LAB_00e5e648:
    if (plVar6 != (long *)0x0) goto LAB_00e5e5d0;
  }
  else {
    iVar5 = (**(code **)(*plVar7 + 0x48))(plVar7);
    plVar6 = (long *)0x0;
    if (iVar5 != -1) {
      plVar6 = plVar7;
    }
    if (plVar8 == (long *)0x0) goto LAB_00e5e648;
LAB_00e5e59c:
    if ((plVar8[3] == plVar8[4]) && (iVar5 = (**(code **)(*plVar8 + 0x48))(plVar8), iVar5 == -1))
    goto LAB_00e5e648;
    if (plVar6 == (long *)0x0) goto LAB_00e5e5d0;
  }
  *param_4 = *param_4 | 2;
LAB_00e5e5d0:
  if (((ulong)local_170 & 1) != 0) {
    operator_delete(local_160);
  }
  if ((local_150 & 1) != 0) {
    operator_delete(local_140);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return plVar6;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5ebe8
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, bool&) const */

ulong __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,bool *param_5)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  ulong uVar4;
  undefined **ppuVar5;
  long lVar6;
  long *plVar7;
  long local_a8;
  ulong local_a0;
  undefined ***local_98;
  undefined **local_90;
  undefined *local_88;
  undefined *puStack_80;
  void *local_78;
  byte local_70 [16];
  void *local_60;
  long local_58;
  
  local_a0 = (ulong)param_1;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if (((byte)param_3[8] & 1) == 0) {
    local_88 = (undefined *)0xffffffffffffffff;
    uVar4 = (**(code **)(*(long *)this + 0x20))(this,local_a0,param_2,param_3,param_4,&local_88);
    local_a0 = uVar4;
    if (local_88 == (undefined *)0x1) {
      *param_5 = true;
    }
    else if (local_88 == (undefined *)0x0) {
      *param_5 = false;
    }
    else {
      *param_5 = true;
      *param_4 = 4;
    }
  }
  else {
    ios_base::getloc();
    puVar3 = PTR___init_01ff5688;
    puVar2 = PTR_id_01ff5620;
    local_78 = (void *)0x0;
    local_88 = PTR_id_01ff5620;
    puStack_80 = PTR___init_01ff5688;
    if (*(long *)PTR_id_01ff5620 != -1) {
      local_90 = &local_88;
      local_98 = &local_90;
                    /* try { // try from 00e5ecb4 to 00e5eccb has its CatchHandler @ 00e5ee90 */
      __call_once((ulong *)PTR_id_01ff5620,&local_98,FUN_00e87ff8);
    }
    if (((ulong)(*(long *)(local_a8 + 0x18) - *(long *)(local_a8 + 0x10) >> 3) <=
         (long)*(int *)(puVar2 + 8) - 1U) ||
       (lVar6 = *(long *)(*(long *)(local_a8 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
       lVar6 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e5ee3c to 00e5ee3f has its CatchHandler @ 00e5ee90 */
      FUN_00de5da0();
    }
    __shared_count::__release_shared();
    ios_base::getloc();
    puVar2 = PTR_id_01ff56a0;
    local_78 = (void *)0x0;
    local_88 = PTR_id_01ff56a0;
    puStack_80 = puVar3;
    if (*(long *)PTR_id_01ff56a0 != -1) {
      local_90 = &local_88;
      local_98 = &local_90;
                    /* try { // try from 00e5ed2c to 00e5ed43 has its CatchHandler @ 00e5ee8c */
      __call_once((ulong *)PTR_id_01ff56a0,&local_98,FUN_00e87ff8);
    }
    if (((ulong)(*(long *)(local_a8 + 0x18) - *(long *)(local_a8 + 0x10) >> 3) <=
         (long)*(int *)(puVar2 + 8) - 1U) ||
       (plVar7 = *(long **)(*(long *)(local_a8 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
       plVar7 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e5ee40 to 00e5ee43 has its CatchHandler @ 00e5ee8c */
      FUN_00de5da0();
    }
    __shared_count::__release_shared();
                    /* try { // try from 00e5ed74 to 00e5ed83 has its CatchHandler @ 00e5ee88 */
    (**(code **)(*plVar7 + 0x30))(&local_88,plVar7);
                    /* try { // try from 00e5ed90 to 00e5ed97 has its CatchHandler @ 00e5ee74 */
    (**(code **)(*plVar7 + 0x38))(local_70,plVar7);
                    /* try { // try from 00e5eda0 to 00e5edbb has its CatchHandler @ 00e5ee48 */
    ppuVar5 = (undefined **)FUN_00e5eea8(&local_a0,param_2,&local_88,&local_58,lVar6,param_4,1);
    uVar4 = local_a0;
    *param_5 = ppuVar5 == &local_88;
    if ((local_70[0] & 1) != 0) {
      operator_delete(local_60);
    }
    if (((ulong)local_88 & 1) != 0) {
      operator_delete(local_78);
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get
// Address: 00e5f360
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,long *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_signed<long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5f744
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longlong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_signed<long_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5fb28
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, unsigned short&)
   const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ushort *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_short>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e5ff0c
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, unsigned int&) const
    */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,uint *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_int>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e602f0
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, unsigned long&) const
    */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e606d4
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, unsigned long long&)
   const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulonglong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_unsigned<unsigned_long_long>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e60ab8
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, float&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,float *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<float>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e60e84
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, double&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,double *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<double>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e61250
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, long double&) const
    */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longdouble *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = __do_get_floating_point<long_double>(this,param_1,param_2,param_3,param_4,param_5);
  return iVar1;
}



// ==========================================================================================
// Function: do_get
// Address: 00e6161c
// ==========================================================================================

/* std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, void*&) const */

long * __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_get
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,void **param_5)

{
  ulong uVar1;
  long lVar2;
  undefined *puVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  long *plVar7;
  long *plVar8;
  long *plVar9;
  ulong uVar10;
  undefined ***pppuVar11;
  undefined ***pppuVar12;
  uint local_1bc;
  undefined **local_1b8;
  ulong local_1b0;
  undefined ***local_1a8;
  undefined **local_1a0;
  ulong local_198;
  undefined8 uStack_190;
  void *local_188;
  undefined ***local_180;
  undefined *local_178;
  undefined *puStack_170;
  undefined8 local_168;
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar9 = (long *)(ulong)param_2;
  plVar8 = (long *)(ulong)param_1;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  local_198 = 0;
  uStack_190 = 0;
  local_188 = (void *)0x0;
                    /* try { // try from 00e61668 to 00e6166f has its CatchHandler @ 00e61a64 */
  ios_base::getloc();
  puVar3 = PTR_id_01ff5620;
  local_168 = 0;
  local_178 = PTR_id_01ff5620;
  puStack_170 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_1b8 = &local_178;
    local_180 = &local_1b8;
                    /* try { // try from 00e616a8 to 00e616fb has its CatchHandler @ 00e61a78 */
    __call_once((ulong *)PTR_id_01ff5620,&local_180,FUN_00e87ff8);
  }
  if (((ulong)((long)local_1a0[3] - (long)local_1a0[2] >> 3) <= (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar7 = *(long **)(local_1a0[2] + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar7 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e61a08 to 00e61a0b has its CatchHandler @ 00e61a78 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar7 + 0x60))(plVar7,PTR___src_01ff5698,PTR___src_01ff5698 + 0x1a,awStack_d8);
  __shared_count::__release_shared();
  local_1b8 = (undefined **)0x0;
  local_1b0 = 0;
  local_1a8 = (undefined ***)0x0;
                    /* try { // try from 00e61714 to 00e61727 has its CatchHandler @ 00e61a60 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b8,0x16,'\0');
  pppuVar12 = (undefined ***)((ulong)&local_1b8 | 1);
  local_1a0 = &local_178;
  pppuVar11 = pppuVar12;
  if (((ulong)local_1b8 & 1) != 0) {
    pppuVar11 = local_1a8;
  }
  local_1bc = 0;
  local_180 = pppuVar11;
LAB_00e61764:
  if (plVar8 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e617a8;
LAB_00e617dc:
    plVar9 = (long *)0x0;
    if (bVar4) goto LAB_00e618c0;
  }
  else {
    if ((int *)plVar8[3] == (int *)plVar8[4]) {
                    /* try { // try from 00e61790 to 00e617cb has its CatchHandler @ 00e61a98 */
      iVar6 = (**(code **)(*plVar8 + 0x48))(plVar8);
    }
    else {
      iVar6 = *(int *)plVar8[3];
    }
    bVar4 = iVar6 == -1;
    plVar7 = (long *)0x0;
    if (!bVar4) {
      plVar7 = plVar8;
    }
    plVar8 = plVar7;
    if (plVar9 == (long *)0x0) goto LAB_00e617dc;
LAB_00e617a8:
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (iVar6 == -1) goto LAB_00e617dc;
    if (!bVar4) goto LAB_00e618c0;
  }
  uVar10 = local_1b0;
  if (((ulong)local_1b8 & 1) == 0) {
    uVar10 = (ulong)local_1b8 >> 1 & 0x7f;
  }
  if (local_180 == (undefined ***)((long)pppuVar11 + uVar10)) {
                    /* try { // try from 00e6180c to 00e6183b has its CatchHandler @ 00e61a94 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b8,uVar10 << 1,'\0');
    uVar1 = 0x16;
    if (((ulong)local_1b8 & 1) != 0) {
      uVar1 = ((ulong)local_1b8 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b8,uVar1,'\0');
    pppuVar11 = pppuVar12;
    if (((ulong)local_1b8 & 1) != 0) {
      pppuVar11 = local_1a8;
    }
    local_180 = (undefined ***)((long)pppuVar11 + uVar10);
  }
  if ((wchar_t *)plVar8[3] == (wchar_t *)plVar8[4]) {
                    /* try { // try from 00e61870 to 00e618bb has its CatchHandler @ 00e61a98 */
    wVar5 = (**(code **)(*plVar8 + 0x48))(plVar8);
  }
  else {
    wVar5 = *(wchar_t *)plVar8[3];
  }
  iVar6 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar5,0x10,(char *)pppuVar11,(char **)&local_180,&local_1bc,L'\0',
                     (basic_string *)&local_198,(uint *)&local_178,(uint **)&local_1a0,awStack_d8);
  if (iVar6 != 0) goto LAB_00e618c0;
  if (plVar8[3] == plVar8[4]) {
    (**(code **)(*plVar8 + 0x50))(plVar8);
  }
  else {
    plVar8[3] = plVar8[3] + 4;
  }
  goto LAB_00e61764;
LAB_00e618c0:
                    /* try { // try from 00e618c8 to 00e6198f has its CatchHandler @ 00e61a74 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b8,(long)local_180 - (long)pppuVar11,'\0');
  if (((ulong)local_1b8 & 1) != 0) {
    pppuVar12 = local_1a8;
  }
  if (((DAT_0231cfb0 & 1) == 0) && (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0), iVar6 != 0)) {
                    /* try { // try from 00e61a1c to 00e61a2f has its CatchHandler @ 00e61a4c */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_sscanf_l((char *)pppuVar12,(__locale_t *)DAT_0231cfa8,"%p",param_5);
  if (iVar6 != 1) {
    *param_4 = 4;
  }
  if (plVar8 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e6196c;
LAB_00e61944:
    if (!bVar4) goto LAB_00e619ac;
  }
  else {
    if ((int *)plVar8[3] == (int *)plVar8[4]) {
      iVar6 = (**(code **)(*plVar8 + 0x48))(plVar8);
    }
    else {
      iVar6 = *(int *)plVar8[3];
    }
    bVar4 = iVar6 == -1;
    plVar7 = (long *)0x0;
    if (!bVar4) {
      plVar7 = plVar8;
    }
    plVar8 = plVar7;
    if (plVar9 == (long *)0x0) goto LAB_00e61944;
LAB_00e6196c:
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (bVar4 != (iVar6 == -1)) goto LAB_00e619ac;
  }
  *param_4 = *param_4 | 2;
LAB_00e619ac:
  if (((ulong)local_1b8 & 1) != 0) {
    operator_delete(local_1a8);
  }
  if ((local_198 & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return plVar8;
}



// ==========================================================================================
// Function: do_put
// Address: 00e62dfc
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, bool) const */

long * __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,bool param_4)

{
  undefined uVar1;
  long lVar2;
  int iVar3;
  long *plVar4;
  undefined *puVar5;
  code *pcVar6;
  long *plVar7;
  undefined *puVar8;
  long local_78;
  undefined8 local_70;
  undefined *local_68;
  undefined *local_60;
  undefined8 **local_58;
  undefined8 *local_50;
  long local_48;
  
  plVar4 = (long *)(ulong)param_1;
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  if (((byte)param_2[8] & 1) == 0) {
    plVar4 = (long *)(**(code **)(*(long *)this + 0x30))(this,plVar4,param_2,param_3,param_4);
LAB_00e62f80:
    if (*(long *)(lVar2 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return plVar4;
  }
  ios_base::getloc();
  puVar8 = PTR_id_01ff5690;
  local_60 = (undefined *)0x0;
  local_70 = PTR_id_01ff5690;
  local_68 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5690 != -1) {
    local_50 = &local_70;
    local_58 = &local_50;
                    /* try { // try from 00e62e90 to 00e62ea7 has its CatchHandler @ 00e62fb8 */
    __call_once((ulong *)PTR_id_01ff5690,&local_58,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_78 + 0x18) - *(long *)(local_78 + 0x10) >> 3) <=
       (long)*(int *)(puVar8 + 8) - 1U) ||
     (plVar7 = *(long **)(*(long *)(local_78 + 0x10) + ((long)*(int *)(puVar8 + 8) - 1U) * 8),
     plVar7 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e62fb0 to 00e62fb3 has its CatchHandler @ 00e62fb8 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  if (param_4) {
    pcVar6 = *(code **)(*plVar7 + 0x30);
  }
  else {
    pcVar6 = *(code **)(*plVar7 + 0x38);
  }
  (*pcVar6)(&local_70,plVar7);
  puVar8 = (undefined *)((ulong)&local_70 | 1);
  if (((ulong)local_70 & 1) != 0) {
    puVar8 = local_60;
  }
  do {
    if (((byte)local_70 & 1) == 0) {
      if (puVar8 == (undefined *)((long)&local_70 + (ulong)((byte)local_70 >> 1) + 1))
      goto LAB_00e62f80;
    }
    else if (puVar8 == local_60 + (long)local_68) {
      operator_delete(local_60);
      goto LAB_00e62f80;
    }
    plVar7 = plVar4;
    if (plVar4 != (long *)0x0) {
      puVar5 = (undefined *)plVar4[6];
      uVar1 = *puVar8;
      if (puVar5 == (undefined *)plVar4[7]) {
                    /* try { // try from 00e62f68 to 00e62f6f has its CatchHandler @ 00e62fd0 */
        iVar3 = (**(code **)(*plVar4 + 0x68))(plVar4);
        plVar7 = (long *)0x0;
        if (iVar3 != -1) {
          plVar7 = plVar4;
        }
      }
      else {
        plVar4[6] = (long)(puVar5 + 1);
        *puVar5 = uVar1;
      }
    }
    plVar4 = plVar7;
    puVar8 = puVar8 + 1;
  } while( true );
}



// ==========================================================================================
// Function: do_put
// Address: 00e62fec
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, long) const */

void __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,long param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  char acStack_c0 [48];
  char acStack_90 [8];
  locale local_88 [8];
  char *local_80;
  char *pcStack_78;
  undefined4 local_70;
  undefined2 local_6c;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_6c = 0;
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *puVar7 = 0x23;
    puVar7 = puVar7 + 1;
  }
  *puVar7 = 0x6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 100;
  }
  puVar7[1] = uVar8;
  uVar1 = ((ulong)(*(uint *)(param_2 + 8) >> 9) & 1) + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = acStack_90 + lVar5;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e63204 to 00e63217 has its CatchHandler @ 00e63230 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = acStack_90 + lVar5 + 1;
    }
    else if (((1 < iVar6) && (cVar3 == '0')) && ((byte)(acStack_90[lVar5 + 1] | 0x20U) == 0x78)) {
      pcVar10 = acStack_90 + lVar5 + 2;
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e6317c to 00e6319b has its CatchHandler @ 00e63248 */
  __num_put<char>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,acStack_c0 + lVar5,&pcStack_78,&local_80,local_88);
  __shared_count::__release_shared();
  FUN_00de61dc(param_1,acStack_c0 + lVar5,pcStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e63874
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, long long) const */

void __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,longlong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  char acStack_c0 [48];
  char acStack_90 [8];
  locale local_88 [8];
  char *local_80;
  char *pcStack_78;
  undefined8 local_70;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined2 *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined2 *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *(undefined *)puVar7 = 0x23;
    puVar7 = (undefined2 *)((long)puVar7 + 1);
  }
  *puVar7 = 0x6c6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 100;
  }
  *(undefined *)(puVar7 + 1) = uVar8;
  uVar1 = ((ulong)(*(uint *)(param_2 + 8) >> 9) & 1) + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = acStack_90 + lVar5;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e63a88 to 00e63a9b has its CatchHandler @ 00e63ab4 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = acStack_90 + lVar5 + 1;
    }
    else if (((1 < iVar6) && (cVar3 == '0')) && ((byte)(acStack_90[lVar5 + 1] | 0x20U) == 0x78)) {
      pcVar10 = acStack_90 + lVar5 + 2;
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e63a00 to 00e63a1f has its CatchHandler @ 00e63acc */
  __num_put<char>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,acStack_c0 + lVar5,&pcStack_78,&local_80,local_88);
  __shared_count::__release_shared();
  FUN_00de61dc(param_1,acStack_c0 + lVar5,pcStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e63ae4
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, unsigned long) const */

void __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,ulong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  char acStack_90 [8];
  locale local_88 [8];
  char *local_80;
  char *pcStack_78;
  undefined4 local_70;
  undefined2 local_6c;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_6c = 0;
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *puVar7 = 0x23;
    puVar7 = puVar7 + 1;
  }
  *puVar7 = 0x6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 0x75;
  }
  puVar7[1] = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = acStack_90 + lVar5;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e63d18 to 00e63d2b has its CatchHandler @ 00e63d44 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = acStack_90 + lVar5 + 1;
    }
    else if (((1 < iVar6) && (cVar3 == '0')) && ((byte)(acStack_90[lVar5 + 1] | 0x20U) == 0x78)) {
      pcVar10 = acStack_90 + lVar5 + 2;
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e63c90 to 00e63caf has its CatchHandler @ 00e63d5c */
  __num_put<char>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) + 0xf & 0x1fffffff0),&pcStack_78,
             &local_80,local_88);
  __shared_count::__release_shared();
  FUN_00de61dc(param_1,pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) + 0xf & 0x1fffffff0),
               pcStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e63d74
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, unsigned long long) const */

void __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,ulonglong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  char acStack_90 [8];
  locale local_88 [8];
  char *local_80;
  char *pcStack_78;
  undefined8 local_70;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined2 *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined2 *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *(undefined *)puVar7 = 0x23;
    puVar7 = (undefined2 *)((long)puVar7 + 1);
  }
  *puVar7 = 0x6c6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 0x75;
  }
  *(undefined *)(puVar7 + 1) = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = acStack_90 + lVar5;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e63fa4 to 00e63fb7 has its CatchHandler @ 00e63fd0 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = acStack_90 + lVar5 + 1;
    }
    else if (((1 < iVar6) && (cVar3 == '0')) && ((byte)(acStack_90[lVar5 + 1] | 0x20U) == 0x78)) {
      pcVar10 = acStack_90 + lVar5 + 2;
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e63f1c to 00e63f3b has its CatchHandler @ 00e63fe8 */
  __num_put<char>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) + 0xf & 0x1fffffff0),&pcStack_78,
             &local_80,local_88);
  __shared_count::__release_shared();
  FUN_00de61dc(param_1,pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) + 0xf & 0x1fffffff0),
               pcStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e64000
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, double) const */

undefined8 __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,double param_4)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  char cVar4;
  long lVar5;
  char *pcVar6;
  bool bVar7;
  int iVar8;
  char *__ptr;
  undefined8 uVar9;
  undefined2 *puVar10;
  undefined uVar11;
  undefined uVar12;
  char *__ptr_00;
  char *pcVar13;
  char *pcVar14;
  locale local_100 [8];
  char *local_f8;
  char *pcStack_f0;
  char *local_e8;
  undefined8 local_e0;
  char acStack_d4 [60];
  char local_98 [32];
  long local_78;
  
  lVar5 = tpidr_el0;
  local_78 = *(long *)(lVar5 + 0x28);
  local_e0 = 0x25;
  uVar3 = *(uint *)(param_2 + 8);
  if ((uVar3 >> 0xb & 1) == 0) {
    puVar10 = (undefined2 *)((ulong)&local_e0 | 1);
  }
  else {
    puVar10 = (undefined2 *)((ulong)&local_e0 | 2);
    local_e0 = 0x2b25;
  }
  if ((uVar3 >> 10 & 1) != 0) {
    *(undefined *)puVar10 = 0x23;
    puVar10 = (undefined2 *)((long)puVar10 + 1);
  }
  uVar2 = uVar3 & 0x104;
  if (uVar2 == 0x104) {
    local_e8 = local_98;
    uVar12 = 0x61;
    if ((uVar3 & 0x4000) != 0) {
      uVar12 = 0x41;
    }
    *(undefined *)puVar10 = uVar12;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e64310 to 00e64323 has its CatchHandler @ 00e643f4 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_98,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_e0,param_4);
    if (iVar8 < 0x1e) goto LAB_00e641bc;
    if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e64384 to 00e64397 has its CatchHandler @ 00e643ec */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_asprintf_l(&local_e8,(__locale_t *)DAT_0231cfa8,(char *)&local_e0,param_4);
LAB_00e641b0:
    __ptr_00 = local_e8;
    if (local_e8 == (char *)0x0) {
      iVar8 = __throw_bad_alloc();
      goto LAB_00e641bc;
    }
  }
  else {
    *puVar10 = 0x2a2e;
    if (uVar2 == 0x100) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x45;
      uVar12 = 0x65;
    }
    else if (uVar2 == 4) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x46;
      uVar12 = 0x66;
    }
    else {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x47;
      uVar12 = 0x67;
    }
    if (!bVar7) {
      uVar12 = uVar11;
    }
    *(undefined *)(puVar10 + 1) = uVar12;
    local_e8 = local_98;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e6434c to 00e6435f has its CatchHandler @ 00e643f0 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_98,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_e0,param_4,
                                (ulong)*(uint *)(param_2 + 0x10));
    if (0x1d < iVar8) {
      if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e643bc to 00e643cf has its CatchHandler @ 00e643e8 */
        DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
        __cxa_guard_release(&DAT_0231cfb0);
      }
      iVar8 = __libcpp_asprintf_l(&local_e8,(__locale_t *)DAT_0231cfa8,(char *)&local_e0,param_4,
                                  (ulong)*(uint *)(param_2 + 0x10));
      goto LAB_00e641b0;
    }
LAB_00e641bc:
    __ptr_00 = (char *)0x0;
  }
  pcVar6 = local_e8;
  pcVar1 = local_e8 + iVar8;
  pcVar13 = pcVar1;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar13 = local_e8, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar4 = *local_e8;
    if ((cVar4 == '-') || (cVar4 == '+')) {
      pcVar13 = local_e8 + 1;
    }
    else if (((1 < iVar8) && (cVar4 == '0')) && ((byte)(local_e8[1] | 0x20U) == 0x78)) {
      pcVar13 = local_e8 + 2;
    }
  }
  if (local_e8 != local_98) {
    __ptr = (char *)malloc((long)iVar8 << 1);
    pcVar14 = __ptr;
    if (__ptr != (char *)0x0) goto LAB_00e6425c;
                    /* try { // try from 00e64250 to 00e64253 has its CatchHandler @ 00e6440c */
    __throw_bad_alloc();
  }
  __ptr = (char *)0x0;
  pcVar14 = acStack_d4;
LAB_00e6425c:
                    /* try { // try from 00e6425c to 00e64267 has its CatchHandler @ 00e64430 */
  ios_base::getloc();
                    /* try { // try from 00e64268 to 00e64287 has its CatchHandler @ 00e6441c */
  __num_put<char>::__widen_and_group_float
            (pcVar6,pcVar13,pcVar1,pcVar14,&pcStack_f0,&local_f8,local_100);
  __shared_count::__release_shared();
                    /* try { // try from 00e64294 to 00e642a7 has its CatchHandler @ 00e64418 */
  uVar9 = FUN_00de61dc(param_1,pcVar14,pcStack_f0,local_f8,param_2,param_3);
  if (__ptr != (char *)0x0) {
    free(__ptr);
  }
  if (__ptr_00 != (char *)0x0) {
    free(__ptr_00);
  }
  if (*(long *)(lVar5 + 0x28) == local_78) {
    return uVar9;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e64bf8
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, long double) const */

undefined8 __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,longdouble param_4)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  char cVar4;
  long lVar5;
  char *pcVar6;
  bool bVar7;
  int iVar8;
  char *__ptr;
  undefined8 uVar9;
  undefined2 *puVar10;
  undefined uVar11;
  undefined uVar12;
  char *__ptr_00;
  char *pcVar13;
  char *pcVar14;
  locale local_f0 [8];
  char *local_e8;
  char *pcStack_e0;
  char *local_d8;
  undefined8 local_d0;
  char acStack_c4 [60];
  char local_88 [32];
  long local_68;
  
  lVar5 = tpidr_el0;
  local_68 = *(long *)(lVar5 + 0x28);
  local_d0 = 0x25;
  uVar3 = *(uint *)(param_2 + 8);
  if ((uVar3 >> 0xb & 1) == 0) {
    puVar10 = (undefined2 *)((ulong)&local_d0 | 1);
  }
  else {
    puVar10 = (undefined2 *)((ulong)&local_d0 | 2);
    local_d0 = 0x2b25;
  }
  if ((uVar3 >> 10 & 1) != 0) {
    *(undefined *)puVar10 = 0x23;
    puVar10 = (undefined2 *)((long)puVar10 + 1);
  }
  uVar2 = uVar3 & 0x104;
  if (uVar2 == 0x104) {
    local_d8 = local_88;
    uVar12 = 0x61;
    if ((uVar3 & 0x4000) != 0) {
      uVar12 = 0x41;
    }
    *(undefined *)puVar10 = 0x4c;
    *(undefined *)((long)puVar10 + 1) = uVar12;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e64f10 to 00e64f23 has its CatchHandler @ 00e64ff4 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_88,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_d0,param_4);
    if (iVar8 < 0x1e) goto LAB_00e64dc0;
    if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e64f84 to 00e64f97 has its CatchHandler @ 00e64fec */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_asprintf_l(&local_d8,(__locale_t *)DAT_0231cfa8,(char *)&local_d0,param_4);
LAB_00e64db4:
    __ptr_00 = local_d8;
    if (local_d8 == (char *)0x0) {
      iVar8 = __throw_bad_alloc();
      goto LAB_00e64dc0;
    }
  }
  else {
    *puVar10 = 0x2a2e;
    *(undefined *)(puVar10 + 1) = 0x4c;
    if (uVar2 == 0x100) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x45;
      uVar12 = 0x65;
    }
    else if (uVar2 == 4) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x46;
      uVar12 = 0x66;
    }
    else {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x47;
      uVar12 = 0x67;
    }
    if (!bVar7) {
      uVar12 = uVar11;
    }
    *(undefined *)((long)puVar10 + 3) = uVar12;
    local_d8 = local_88;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e64f4c to 00e64f5f has its CatchHandler @ 00e64ff0 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_88,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_d0,param_4,
                                (ulong)*(uint *)(param_2 + 0x10));
    if (0x1d < iVar8) {
      if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e64fbc to 00e64fcf has its CatchHandler @ 00e64fe8 */
        DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
        __cxa_guard_release(&DAT_0231cfb0);
      }
      iVar8 = __libcpp_asprintf_l(&local_d8,(__locale_t *)DAT_0231cfa8,(char *)&local_d0,param_4,
                                  (ulong)*(uint *)(param_2 + 0x10));
      goto LAB_00e64db4;
    }
LAB_00e64dc0:
    __ptr_00 = (char *)0x0;
  }
  pcVar6 = local_d8;
  pcVar1 = local_d8 + iVar8;
  pcVar13 = pcVar1;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar13 = local_d8, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar4 = *local_d8;
    if ((cVar4 == '-') || (cVar4 == '+')) {
      pcVar13 = local_d8 + 1;
    }
    else if (((1 < iVar8) && (cVar4 == '0')) && ((byte)(local_d8[1] | 0x20U) == 0x78)) {
      pcVar13 = local_d8 + 2;
    }
  }
  if (local_d8 != local_88) {
    __ptr = (char *)malloc((long)iVar8 << 1);
    pcVar14 = __ptr;
    if (__ptr != (char *)0x0) goto LAB_00e64e60;
                    /* try { // try from 00e64e54 to 00e64e57 has its CatchHandler @ 00e6500c */
    __throw_bad_alloc();
  }
  __ptr = (char *)0x0;
  pcVar14 = acStack_c4;
LAB_00e64e60:
                    /* try { // try from 00e64e60 to 00e64e6b has its CatchHandler @ 00e65030 */
  ios_base::getloc();
                    /* try { // try from 00e64e6c to 00e64e8b has its CatchHandler @ 00e6501c */
  __num_put<char>::__widen_and_group_float
            (pcVar6,pcVar13,pcVar1,pcVar14,&pcStack_e0,&local_e8,local_f0);
  __shared_count::__release_shared();
                    /* try { // try from 00e64e98 to 00e64eab has its CatchHandler @ 00e65018 */
  uVar9 = FUN_00de61dc(param_1,pcVar14,pcStack_e0,local_e8,param_2,param_3);
  if (__ptr != (char *)0x0) {
    free(__ptr);
  }
  if (__ptr_00 != (char *)0x0) {
    free(__ptr_00);
  }
  if (*(long *)(lVar5 + 0x28) == local_68) {
    return uVar9;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e65060
// ==========================================================================================

/* std::__ndk1::num_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, void const*) const */

void __thiscall
std::__ndk1::num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(num_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,void *param_4)

{
  char *pcVar1;
  char *pcVar2;
  long lVar3;
  undefined *puVar4;
  int iVar5;
  long *plVar6;
  char *pcVar7;
  long local_e0;
  undefined *local_d8;
  undefined *puStack_d0;
  undefined8 local_c8;
  undefined ***local_c0;
  undefined **local_b8;
  undefined4 local_ac;
  undefined2 local_a8;
  char acStack_a4 [40];
  char local_7c [20];
  long local_68;
  
  lVar3 = tpidr_el0;
  local_68 = *(long *)(lVar3 + 0x28);
  local_a8 = 0;
  local_ac = 0x7025;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar5 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar5 != 0)) {
                    /* try { // try from 00e65268 to 00e6527b has its CatchHandler @ 00e65294 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar5 = __libcpp_snprintf_l(local_7c,0x14,(__locale_t *)DAT_0231cfa8,(char *)&local_ac,param_4);
  pcVar1 = local_7c + iVar5;
  pcVar7 = pcVar1;
  if ((*(uint *)(param_2 + 8) & 0xb0) == 0x20) goto LAB_00e65154;
  if ((*(uint *)(param_2 + 8) & 0xb0) == 0x10) {
    if ((local_7c[0] == '-') || (local_7c[0] == '+')) {
      pcVar7 = (char *)((ulong)local_7c | 1);
      goto LAB_00e65154;
    }
    if ((1 < iVar5) && ((local_7c[0] == '0' && ((byte)(local_7c[1] | 0x20U) == 0x78)))) {
      pcVar7 = (char *)((ulong)local_7c | 2);
      goto LAB_00e65154;
    }
  }
  pcVar7 = local_7c;
LAB_00e65154:
  ios_base::getloc();
  puVar4 = PTR_id_01ff5500;
  local_c8 = 0;
  local_d8 = PTR_id_01ff5500;
  puStack_d0 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_b8 = &local_d8;
    local_c0 = &local_b8;
                    /* try { // try from 00e65194 to 00e651ab has its CatchHandler @ 00e652ac */
    __call_once((ulong *)PTR_id_01ff5500,&local_c0,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_e0 + 0x18) - *(long *)(local_e0 + 0x10) >> 3) <=
       (long)*(int *)(puVar4 + 8) - 1U) ||
     (plVar6 = *(long **)(*(long *)(local_e0 + 0x10) + ((long)*(int *)(puVar4 + 8) - 1U) * 8),
     plVar6 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e65254 to 00e65257 has its CatchHandler @ 00e652ac */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  (**(code **)(*plVar6 + 0x40))(plVar6,local_7c,pcVar1,acStack_a4);
  pcVar2 = acStack_a4 + iVar5;
  if (pcVar7 != pcVar1) {
    pcVar2 = pcVar7 + (long)(acStack_a4 + -(long)local_7c);
  }
  FUN_00de61dc(param_1,acStack_a4,pcVar2,acStack_a4 + iVar5,param_2,param_3);
  if (*(long *)(lVar3 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e652c4
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, bool) const */

long * __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,bool param_4)

{
  long lVar1;
  undefined *puVar2;
  int iVar3;
  long *plVar4;
  ulong uVar5;
  int *piVar6;
  code *pcVar7;
  long *plVar8;
  int *piVar9;
  long local_78;
  undefined8 local_70;
  undefined *local_68;
  int *local_60;
  undefined8 **local_58;
  undefined8 *local_50;
  long local_48;
  
  plVar4 = (long *)(ulong)param_1;
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  if (((byte)param_2[8] & 1) == 0) {
    plVar4 = (long *)(**(code **)(*(long *)this + 0x30))(this,plVar4,param_2,param_3,param_4);
LAB_00e6544c:
    if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return plVar4;
  }
  ios_base::getloc();
  puVar2 = PTR_id_01ff56a0;
  local_60 = (int *)0x0;
  local_70 = PTR_id_01ff56a0;
  local_68 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff56a0 != -1) {
    local_50 = &local_70;
    local_58 = &local_50;
                    /* try { // try from 00e65358 to 00e6536f has its CatchHandler @ 00e65484 */
    __call_once((ulong *)PTR_id_01ff56a0,&local_58,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_78 + 0x18) - *(long *)(local_78 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar8 = *(long **)(*(long *)(local_78 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar8 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6547c to 00e6547f has its CatchHandler @ 00e65484 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  if (param_4) {
    pcVar7 = *(code **)(*plVar8 + 0x30);
  }
  else {
    pcVar7 = *(code **)(*plVar8 + 0x38);
  }
  (*pcVar7)(&local_70,plVar8);
  uVar5 = (ulong)local_70 & 0xff;
  piVar9 = (int *)((ulong)&local_70 | 4);
  if (((ulong)local_70 & 1) != 0) {
    piVar9 = local_60;
  }
  do {
    if ((uVar5 & 1) == 0) {
      if (piVar9 == (int *)((long)&local_70 + (uVar5 >> 1) * 4 + 4)) goto LAB_00e6544c;
    }
    else if (piVar9 == local_60 + (long)local_68) {
      operator_delete(local_60);
      goto LAB_00e6544c;
    }
    plVar8 = plVar4;
    if (plVar4 != (long *)0x0) {
      piVar6 = (int *)plVar4[6];
      iVar3 = *piVar9;
      if (piVar6 == (int *)plVar4[7]) {
                    /* try { // try from 00e65438 to 00e65443 has its CatchHandler @ 00e6549c */
        iVar3 = (**(code **)(*plVar4 + 0x68))(plVar4);
      }
      else {
        plVar4[6] = (long)(piVar6 + 1);
        *piVar6 = iVar3;
      }
      uVar5 = (ulong)local_70 & 0xff;
      plVar8 = (long *)0x0;
      if (iVar3 != -1) {
        plVar8 = plVar4;
      }
    }
    plVar4 = plVar8;
    piVar9 = piVar9 + 1;
  } while( true );
}



// ==========================================================================================
// Function: do_put
// Address: 00e654b8
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, long) const */

void __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,long param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  undefined4 uStack_90;
  locale local_88 [8];
  wchar_t *local_80;
  wchar_t *pwStack_78;
  undefined4 local_70;
  undefined2 local_6c;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_6c = 0;
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *puVar7 = 0x23;
    puVar7 = puVar7 + 1;
  }
  *puVar7 = 0x6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 100;
  }
  puVar7[1] = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = (char *)((long)&uStack_90 + lVar5);
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e656e0 to 00e656f3 has its CatchHandler @ 00e6570c */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 1);
    }
    else if (((1 < iVar6) && (cVar3 == '0')) &&
            ((*(byte *)((long)&uStack_90 + lVar5 + 1) | 0x20) == 0x78)) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 2);
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e65658 to 00e65677 has its CatchHandler @ 00e65724 */
  __num_put<wchar_t>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             (wchar_t *)(pcVar9 + -((ulong)((int)uVar11 * 8 + 0xbb) & 0xf0)),&pwStack_78,&local_80,
             local_88);
  __shared_count::__release_shared();
  FUN_00e65b40(param_1,pcVar9 + -((ulong)((int)uVar11 * 8 + 0xbb) & 0xf0),pwStack_78,local_80,
               param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e65d14
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, long long) const */

void __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,longlong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  undefined4 uStack_90;
  locale local_88 [8];
  wchar_t *local_80;
  wchar_t *pwStack_78;
  undefined8 local_70;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined2 *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined2 *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *(undefined *)puVar7 = 0x23;
    puVar7 = (undefined2 *)((long)puVar7 + 1);
  }
  *puVar7 = 0x6c6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 100;
  }
  *(undefined *)(puVar7 + 1) = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = (char *)((long)&uStack_90 + lVar5);
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e65f38 to 00e65f4b has its CatchHandler @ 00e65f64 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 1);
    }
    else if (((1 < iVar6) && (cVar3 == '0')) &&
            ((*(byte *)((long)&uStack_90 + lVar5 + 1) | 0x20) == 0x78)) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 2);
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e65eb0 to 00e65ecf has its CatchHandler @ 00e65f7c */
  __num_put<wchar_t>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             (wchar_t *)(pcVar9 + -((ulong)((int)uVar11 * 8 + 0xbb) & 0xf0)),&pwStack_78,&local_80,
             local_88);
  __shared_count::__release_shared();
  FUN_00e65b40(param_1,pcVar9 + -((ulong)((int)uVar11 * 8 + 0xbb) & 0xf0),pwStack_78,local_80,
               param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e65f94
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, unsigned long) const */

void __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,ulong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  undefined4 uStack_90;
  locale local_88 [8];
  wchar_t *local_80;
  wchar_t *pwStack_78;
  undefined4 local_70;
  undefined2 local_6c;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_6c = 0;
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *puVar7 = 0x23;
    puVar7 = puVar7 + 1;
  }
  *puVar7 = 0x6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 0x75;
  }
  puVar7[1] = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = (char *)((long)&uStack_90 + lVar5);
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e661cc to 00e661df has its CatchHandler @ 00e661f8 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 1);
    }
    else if (((1 < iVar6) && (cVar3 == '0')) &&
            ((*(byte *)((long)&uStack_90 + lVar5 + 1) | 0x20) == 0x78)) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 2);
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e66144 to 00e66163 has its CatchHandler @ 00e66210 */
  __num_put<wchar_t>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             (wchar_t *)(pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) * 4 + 0xf & 0x7fffffff0))
             ,&pwStack_78,&local_80,local_88);
  __shared_count::__release_shared();
  FUN_00e65b40(param_1,pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) * 4 + 0xf & 0x7fffffff0),
               pwStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e66228
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, unsigned long long) const
    */

void __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,ulonglong param_4)

{
  ulong uVar1;
  uint uVar2;
  char cVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined uVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  undefined4 uStack_90;
  locale local_88 [8];
  wchar_t *local_80;
  wchar_t *pwStack_78;
  undefined8 local_70;
  long local_68;
  
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  local_70 = 0x25;
  uVar2 = *(uint *)(param_2 + 8);
  if ((uVar2 >> 0xb & 1) == 0) {
    puVar7 = (undefined2 *)((ulong)&local_70 | 1);
  }
  else {
    puVar7 = (undefined2 *)((ulong)&local_70 | 2);
    local_70 = 0x2b25;
  }
  if ((uVar2 >> 9 & 1) != 0) {
    *(undefined *)puVar7 = 0x23;
    puVar7 = (undefined2 *)((long)puVar7 + 1);
  }
  *puVar7 = 0x6c6c;
  if ((uVar2 & 0x4a) == 0x40) {
    uVar8 = 0x6f;
  }
  else if ((uVar2 & 0x4a) == 8) {
    uVar8 = 0x78;
    if ((uVar2 & 0x4000) != 0) {
      uVar8 = 0x58;
    }
  }
  else {
    uVar8 = 0x75;
  }
  *(undefined *)(puVar7 + 1) = uVar8;
  uVar11 = (ulong)(*(uint *)(param_2 + 8) >> 9) & 1;
  uVar1 = uVar11 + 0x17;
  lVar5 = -((ulong)((int)uVar1 + 0xf) & 0x30);
  pcVar9 = (char *)((long)&uStack_90 + lVar5);
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar6 != 0)) {
                    /* try { // try from 00e6645c to 00e6646f has its CatchHandler @ 00e66488 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar6 = __libcpp_snprintf_l(pcVar9,uVar1,(__locale_t *)DAT_0231cfa8,(char *)&local_70,param_4);
  pcVar10 = pcVar9 + iVar6;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar10 = pcVar9, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar3 = *pcVar9;
    if ((cVar3 == '-') || (cVar3 == '+')) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 1);
    }
    else if (((1 < iVar6) && (cVar3 == '0')) &&
            ((*(byte *)((long)&uStack_90 + lVar5 + 1) | 0x20) == 0x78)) {
      pcVar10 = (char *)((long)&uStack_90 + lVar5 + 2);
    }
  }
  ios_base::getloc();
                    /* try { // try from 00e663d4 to 00e663f3 has its CatchHandler @ 00e664a0 */
  __num_put<wchar_t>::__widen_and_group_int
            (pcVar9,pcVar10,pcVar9 + iVar6,
             (wchar_t *)(pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) * 4 + 0xf & 0x7fffffff0))
             ,&pwStack_78,&local_80,local_88);
  __shared_count::__release_shared();
  FUN_00e65b40(param_1,pcVar9 + -((ulong)(((uint)uVar11 | 0x16) * 2 - 1) * 4 + 0xf & 0x7fffffff0),
               pwStack_78,local_80,param_2,param_3);
  if (*(long *)(lVar4 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e664b8
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, double) const */

undefined8 __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,double param_4)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  char cVar4;
  long lVar5;
  char *pcVar6;
  bool bVar7;
  int iVar8;
  wchar_t *__ptr;
  undefined8 uVar9;
  undefined2 *puVar10;
  undefined uVar11;
  undefined uVar12;
  char *__ptr_00;
  char *pcVar13;
  wchar_t *pwVar14;
  locale local_1b0 [8];
  wchar_t *local_1a8;
  wchar_t *pwStack_1a0;
  char *local_198;
  undefined8 local_190;
  wchar_t awStack_184 [57];
  char local_a0 [32];
  long local_80;
  
  lVar5 = tpidr_el0;
  local_80 = *(long *)(lVar5 + 0x28);
  local_190 = 0x25;
  uVar3 = *(uint *)(param_2 + 8);
  if ((uVar3 >> 0xb & 1) == 0) {
    puVar10 = (undefined2 *)((ulong)&local_190 | 1);
  }
  else {
    puVar10 = (undefined2 *)((ulong)&local_190 | 2);
    local_190 = 0x2b25;
  }
  if ((uVar3 >> 10 & 1) != 0) {
    *(undefined *)puVar10 = 0x23;
    puVar10 = (undefined2 *)((long)puVar10 + 1);
  }
  uVar2 = uVar3 & 0x104;
  if (uVar2 == 0x104) {
    local_198 = local_a0;
    uVar12 = 0x61;
    if ((uVar3 & 0x4000) != 0) {
      uVar12 = 0x41;
    }
    *(undefined *)puVar10 = uVar12;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e667c8 to 00e667db has its CatchHandler @ 00e668ac */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_a0,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_190,param_4)
    ;
    if (iVar8 < 0x1e) goto LAB_00e66674;
    if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e6683c to 00e6684f has its CatchHandler @ 00e668a4 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_asprintf_l(&local_198,(__locale_t *)DAT_0231cfa8,(char *)&local_190,param_4);
LAB_00e66668:
    __ptr_00 = local_198;
    if (local_198 == (char *)0x0) {
      iVar8 = __throw_bad_alloc();
      goto LAB_00e66674;
    }
  }
  else {
    *puVar10 = 0x2a2e;
    if (uVar2 == 0x100) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x45;
      uVar12 = 0x65;
    }
    else if (uVar2 == 4) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x46;
      uVar12 = 0x66;
    }
    else {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x47;
      uVar12 = 0x67;
    }
    if (!bVar7) {
      uVar12 = uVar11;
    }
    *(undefined *)(puVar10 + 1) = uVar12;
    local_198 = local_a0;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e66804 to 00e66817 has its CatchHandler @ 00e668a8 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_a0,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_190,param_4,
                                (ulong)*(uint *)(param_2 + 0x10));
    if (0x1d < iVar8) {
      if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e66874 to 00e66887 has its CatchHandler @ 00e668a0 */
        DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
        __cxa_guard_release(&DAT_0231cfb0);
      }
      iVar8 = __libcpp_asprintf_l(&local_198,(__locale_t *)DAT_0231cfa8,(char *)&local_190,param_4,
                                  (ulong)*(uint *)(param_2 + 0x10));
      goto LAB_00e66668;
    }
LAB_00e66674:
    __ptr_00 = (char *)0x0;
  }
  pcVar6 = local_198;
  pcVar1 = local_198 + iVar8;
  pcVar13 = pcVar1;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar13 = local_198, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar4 = *local_198;
    if ((cVar4 == '-') || (cVar4 == '+')) {
      pcVar13 = local_198 + 1;
    }
    else if (((1 < iVar8) && (cVar4 == '0')) && ((byte)(local_198[1] | 0x20U) == 0x78)) {
      pcVar13 = local_198 + 2;
    }
  }
  if (local_198 != local_a0) {
    __ptr = (wchar_t *)malloc((long)iVar8 << 3);
    pwVar14 = __ptr;
    if (__ptr != (wchar_t *)0x0) goto LAB_00e66714;
                    /* try { // try from 00e66708 to 00e6670b has its CatchHandler @ 00e668c4 */
    __throw_bad_alloc();
  }
  __ptr = (wchar_t *)0x0;
  pwVar14 = awStack_184;
LAB_00e66714:
                    /* try { // try from 00e66714 to 00e6671f has its CatchHandler @ 00e668e8 */
  ios_base::getloc();
                    /* try { // try from 00e66720 to 00e6673f has its CatchHandler @ 00e668d4 */
  __num_put<wchar_t>::__widen_and_group_float
            (pcVar6,pcVar13,pcVar1,pwVar14,&pwStack_1a0,&local_1a8,local_1b0);
  __shared_count::__release_shared();
                    /* try { // try from 00e6674c to 00e6675f has its CatchHandler @ 00e668d0 */
  uVar9 = FUN_00e65b40(param_1,pwVar14,pwStack_1a0,local_1a8,param_2,param_3);
  if (__ptr != (wchar_t *)0x0) {
    free(__ptr);
  }
  if (__ptr_00 != (char *)0x0) {
    free(__ptr_00);
  }
  if (*(long *)(lVar5 + 0x28) == local_80) {
    return uVar9;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e66f04
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, long double) const */

undefined8 __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,longdouble param_4)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  char cVar4;
  long lVar5;
  char *pcVar6;
  bool bVar7;
  int iVar8;
  wchar_t *__ptr;
  undefined8 uVar9;
  undefined2 *puVar10;
  undefined uVar11;
  undefined uVar12;
  char *__ptr_00;
  char *pcVar13;
  wchar_t *pwVar14;
  locale local_1a0 [8];
  wchar_t *local_198;
  wchar_t *pwStack_190;
  char *local_188;
  undefined8 local_180;
  wchar_t awStack_174 [57];
  char local_90 [32];
  long local_70;
  
  lVar5 = tpidr_el0;
  local_70 = *(long *)(lVar5 + 0x28);
  local_180 = 0x25;
  uVar3 = *(uint *)(param_2 + 8);
  if ((uVar3 >> 0xb & 1) == 0) {
    puVar10 = (undefined2 *)((ulong)&local_180 | 1);
  }
  else {
    puVar10 = (undefined2 *)((ulong)&local_180 | 2);
    local_180 = 0x2b25;
  }
  if ((uVar3 >> 10 & 1) != 0) {
    *(undefined *)puVar10 = 0x23;
    puVar10 = (undefined2 *)((long)puVar10 + 1);
  }
  uVar2 = uVar3 & 0x104;
  if (uVar2 == 0x104) {
    local_188 = local_90;
    uVar12 = 0x61;
    if ((uVar3 & 0x4000) != 0) {
      uVar12 = 0x41;
    }
    *(undefined *)puVar10 = 0x4c;
    *(undefined *)((long)puVar10 + 1) = uVar12;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e6721c to 00e6722f has its CatchHandler @ 00e67300 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_90,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_180,param_4)
    ;
    if (iVar8 < 0x1e) goto LAB_00e670cc;
    if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e67290 to 00e672a3 has its CatchHandler @ 00e672f8 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_asprintf_l(&local_188,(__locale_t *)DAT_0231cfa8,(char *)&local_180,param_4);
LAB_00e670c0:
    __ptr_00 = local_188;
    if (local_188 == (char *)0x0) {
      iVar8 = __throw_bad_alloc();
      goto LAB_00e670cc;
    }
  }
  else {
    *puVar10 = 0x2a2e;
    *(undefined *)(puVar10 + 1) = 0x4c;
    if (uVar2 == 0x100) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x45;
      uVar12 = 0x65;
    }
    else if (uVar2 == 4) {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x46;
      uVar12 = 0x66;
    }
    else {
      bVar7 = (uVar3 & 0x4000) == 0;
      uVar11 = 0x47;
      uVar12 = 0x67;
    }
    if (!bVar7) {
      uVar12 = uVar11;
    }
    *(undefined *)((long)puVar10 + 3) = uVar12;
    local_188 = local_90;
    if (((DAT_0231cfb0 & 1) == 0) &&
       (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar8 != 0)) {
                    /* try { // try from 00e67258 to 00e6726b has its CatchHandler @ 00e672fc */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar8 = __libcpp_snprintf_l(local_90,0x1e,(__locale_t *)DAT_0231cfa8,(char *)&local_180,param_4,
                                (ulong)*(uint *)(param_2 + 0x10));
    if (0x1d < iVar8) {
      if (((DAT_0231cfb0 & 1) == 0) && (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e672c8 to 00e672db has its CatchHandler @ 00e672f4 */
        DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
        __cxa_guard_release(&DAT_0231cfb0);
      }
      iVar8 = __libcpp_asprintf_l(&local_188,(__locale_t *)DAT_0231cfa8,(char *)&local_180,param_4,
                                  (ulong)*(uint *)(param_2 + 0x10));
      goto LAB_00e670c0;
    }
LAB_00e670cc:
    __ptr_00 = (char *)0x0;
  }
  pcVar6 = local_188;
  pcVar1 = local_188 + iVar8;
  pcVar13 = pcVar1;
  if (((*(uint *)(param_2 + 8) & 0xb0) != 0x20) &&
     (pcVar13 = local_188, (*(uint *)(param_2 + 8) & 0xb0) == 0x10)) {
    cVar4 = *local_188;
    if ((cVar4 == '-') || (cVar4 == '+')) {
      pcVar13 = local_188 + 1;
    }
    else if (((1 < iVar8) && (cVar4 == '0')) && ((byte)(local_188[1] | 0x20U) == 0x78)) {
      pcVar13 = local_188 + 2;
    }
  }
  if (local_188 != local_90) {
    __ptr = (wchar_t *)malloc((long)iVar8 << 3);
    pwVar14 = __ptr;
    if (__ptr != (wchar_t *)0x0) goto LAB_00e6716c;
                    /* try { // try from 00e67160 to 00e67163 has its CatchHandler @ 00e67318 */
    __throw_bad_alloc();
  }
  __ptr = (wchar_t *)0x0;
  pwVar14 = awStack_174;
LAB_00e6716c:
                    /* try { // try from 00e6716c to 00e67177 has its CatchHandler @ 00e6733c */
  ios_base::getloc();
                    /* try { // try from 00e67178 to 00e67197 has its CatchHandler @ 00e67328 */
  __num_put<wchar_t>::__widen_and_group_float
            (pcVar6,pcVar13,pcVar1,pwVar14,&pwStack_190,&local_198,local_1a0);
  __shared_count::__release_shared();
                    /* try { // try from 00e671a4 to 00e671b7 has its CatchHandler @ 00e67324 */
  uVar9 = FUN_00e65b40(param_1,pwVar14,pwStack_190,local_198,param_2,param_3);
  if (__ptr != (wchar_t *)0x0) {
    free(__ptr);
  }
  if (__ptr_00 != (char *)0x0) {
    free(__ptr_00);
  }
  if (*(long *)(lVar5 + 0x28) == local_70) {
    return uVar9;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e6736c
// ==========================================================================================

/* std::__ndk1::num_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, void const*) const */

void __thiscall
std::__ndk1::
num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::do_put
          (num_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,void *param_4)

{
  char *pcVar1;
  undefined *puVar2;
  long lVar3;
  int iVar4;
  long *plVar5;
  char *pcVar6;
  long local_150;
  undefined *local_148;
  undefined *puStack_140;
  undefined8 local_138;
  undefined ***local_130;
  undefined **local_128;
  undefined4 local_120;
  undefined2 local_11c;
  undefined auStack_118 [148];
  char local_84 [20];
  long local_70;
  
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  local_11c = 0;
  local_120 = 0x7025;
  if (((DAT_0231cfb0 & 1) == 0) &&
     (iVar4 = __cxa_guard_acquire(&DAT_0231cfb0,param_1,param_2,param_3), iVar4 != 0)) {
                    /* try { // try from 00e67574 to 00e67587 has its CatchHandler @ 00e675a0 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  iVar4 = __libcpp_snprintf_l(local_84,0x14,(__locale_t *)DAT_0231cfa8,(char *)&local_120,param_4);
  pcVar1 = local_84 + iVar4;
  pcVar6 = pcVar1;
  if ((*(uint *)(param_2 + 8) & 0xb0) == 0x20) goto LAB_00e67460;
  if ((*(uint *)(param_2 + 8) & 0xb0) == 0x10) {
    if ((local_84[0] == '-') || (local_84[0] == '+')) {
      pcVar6 = (char *)((ulong)local_84 | 1);
      goto LAB_00e67460;
    }
    if ((1 < iVar4) && ((local_84[0] == '0' && ((byte)(local_84[1] | 0x20U) == 0x78)))) {
      pcVar6 = (char *)((ulong)local_84 | 2);
      goto LAB_00e67460;
    }
  }
  pcVar6 = local_84;
LAB_00e67460:
  ios_base::getloc();
  puVar2 = PTR_id_01ff5620;
  local_138 = 0;
  local_148 = PTR_id_01ff5620;
  puStack_140 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_128 = &local_148;
    local_130 = &local_128;
                    /* try { // try from 00e674a0 to 00e674b7 has its CatchHandler @ 00e675b8 */
    __call_once((ulong *)PTR_id_01ff5620,&local_130,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_150 + 0x18) - *(long *)(local_150 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar5 = *(long **)(*(long *)(local_150 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e67560 to 00e67563 has its CatchHandler @ 00e675b8 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  (**(code **)(*plVar5 + 0x60))(plVar5,local_84,pcVar1,auStack_118);
  puVar2 = auStack_118 + (long)iVar4 * 4;
  if (pcVar6 != pcVar1) {
    puVar2 = auStack_118 + ((long)pcVar6 - (long)local_84) * 4;
  }
  FUN_00e65b40(param_1,auStack_118,puVar2,auStack_118 + (long)iVar4 * 4,param_2,param_3);
  if (*(long *)(lVar3 + 0x28) == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_date_order
// Address: 00e67a8c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_date_order() const */

undefined8
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_date_order(void)

{
  return 2;
}



// ==========================================================================================
// Function: do_get_time
// Address: 00e67a98
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get_time(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get_time(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  long lVar1;
  undefined8 local_30;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_30 = 0x53253a4d253a4825;
  get(this,param_1,param_2,param_3,param_4,param_5,(char *)&local_30,(char *)&local_28);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get_date
// Address: 00e67b04
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get_date(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get_date(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  ulong uVar1;
  bool bVar2;
  byte *pbVar3;
  byte *pbVar4;
  
  pbVar3 = (byte *)(**(code **)(*(long *)(this + 0x10) + 0x28))();
  pbVar4 = *(byte **)(pbVar3 + 0x10);
  bVar2 = (*pbVar3 & 1) == 0;
  if (bVar2) {
    pbVar4 = pbVar3 + 1;
  }
  uVar1 = (ulong)(*pbVar3 >> 1);
  if (!bVar2) {
    uVar1 = *(ulong *)(pbVar3 + 8);
  }
  get(this,param_1,param_2,param_3,param_4,param_5,(char *)pbVar4,(char *)(pbVar4 + uVar1));
  return;
}



// ==========================================================================================
// Function: do_get_weekday
// Address: 00e67b8c
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get_weekday(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get_weekday(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
               *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
              uint *param_4,tm *param_5)

{
  undefined auVar1 [16];
  long lVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  long local_90;
  ulong local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  local_88 = (ulong)param_1;
  lVar2 = tpidr_el0;
  local_58 = *(long *)(lVar2 + 0x28);
  ios_base::getloc();
  puVar3 = PTR_id_01ff5500;
  local_70 = 0;
  local_80 = PTR_id_01ff5500;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e67c0c to 00e67c23 has its CatchHandler @ 00e67d04 */
    __call_once((ulong *)PTR_id_01ff5500,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_90 + 0x18) - *(long *)(local_90 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (lVar5 = *(long *)(*(long *)(local_90 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     lVar5 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e67cfc to 00e67cff has its CatchHandler @ 00e67d04 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  lVar4 = (***(code ***)(this + 0x10))(this + 0x10);
  lVar5 = FUN_00e5bd3c(&local_88,param_2,lVar4,lVar4 + 0x150,lVar5,param_4,0);
  if (lVar5 - lVar4 < 0x150) {
    lVar5 = (lVar5 - lVar4 >> 3) * -0x5555555555555555;
    auVar1 = SEXT816(lVar5) * SEXT816(0x4924924924924925);
    param_5->tm_wday = (int)lVar5 + ((int)(auVar1._8_8_ >> 1) - (auVar1._12_4_ >> 0x1f)) * -7;
  }
  if (*(long *)(lVar2 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_88);
}



// ==========================================================================================
// Function: do_get_monthname
// Address: 00e67dd8
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get_monthname(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get_monthname(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                 *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
                uint *param_4,tm *param_5)

{
  long lVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long local_90;
  ulong local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  local_88 = (ulong)param_1;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar2 = PTR_id_01ff5500;
  local_70 = 0;
  local_80 = PTR_id_01ff5500;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e67e58 to 00e67e6f has its CatchHandler @ 00e67f4c */
    __call_once((ulong *)PTR_id_01ff5500,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_90 + 0x18) - *(long *)(local_90 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (lVar4 = *(long *)(*(long *)(local_90 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     lVar4 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e67f44 to 00e67f47 has its CatchHandler @ 00e67f4c */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  lVar3 = (**(code **)(*(long *)(this + 0x10) + 8))(this + 0x10);
  lVar4 = FUN_00e5bd3c(&local_88,param_2,lVar3,lVar3 + 0x240,lVar4,param_4,0);
  if (lVar4 - lVar3 < 0x240) {
    lVar4 = (lVar4 - lVar3 >> 3) * -0x5555555555555555;
    param_5->tm_mon =
         (int)lVar4 +
         ((int)((ulong)(lVar4 / 6 + (lVar4 >> 0x3f)) >> 1) -
         (SUB164(SEXT816(lVar4) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_88);
}



// ==========================================================================================
// Function: do_get_year
// Address: 00e6801c
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get_year(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get_year(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined *puVar4;
  int iVar5;
  long lVar6;
  long local_80;
  ulong local_78;
  undefined *local_70;
  undefined *puStack_68;
  undefined8 local_60;
  undefined ***local_58;
  undefined **local_50;
  long local_48;
  
  local_78 = (ulong)param_1;
  lVar3 = tpidr_el0;
  local_48 = *(long *)(lVar3 + 0x28);
  ios_base::getloc();
  puVar4 = PTR_id_01ff5500;
  local_60 = 0;
  local_70 = PTR_id_01ff5500;
  puStack_68 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_50 = &local_70;
    local_58 = &local_50;
                    /* try { // try from 00e68094 to 00e680ab has its CatchHandler @ 00e6814c */
    __call_once((ulong *)PTR_id_01ff5500,&local_58,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_80 + 0x18) - *(long *)(local_80 + 0x10) >> 3) <=
       (long)*(int *)(puVar4 + 8) - 1U) ||
     (lVar6 = *(long *)(*(long *)(local_80 + 0x10) + ((long)*(int *)(puVar4 + 8) - 1U) * 8),
     lVar6 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e68144 to 00e68147 has its CatchHandler @ 00e6814c */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  iVar5 = FUN_00e69024(&local_78,param_2,param_4,lVar6,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    iVar1 = iVar5 + 0x76c;
    if (99 < iVar5) {
      iVar1 = iVar5;
    }
    iVar2 = iVar5 + 2000;
    if (0x44 < iVar5) {
      iVar2 = iVar1;
    }
    param_5->tm_year = iVar2 + -0x76c;
  }
  if (*(long *)(lVar3 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_78);
}



// ==========================================================================================
// Function: do_get
// Address: 00e681cc
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_get(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&,
   unsigned int&, tm*, char, char) const */

void std::__ndk1::
     time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::do_get
               (istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
               uint *param_4,tm *param_5,char param_6,char param_7)

{
  int iVar1;
  int iVar2;
  undefined auVar3 [16];
  long lVar4;
  undefined *puVar5;
  int iVar6;
  long *this;
  long lVar7;
  long lVar8;
  ulong uVar9;
  byte *pbVar10;
  byte *pbVar11;
  istreambuf_iterator iVar12;
  istreambuf_iterator iVar13;
  tm *ptVar14;
  undefined5 *puVar15;
  uint uVar16;
  code *pcVar17;
  undefined8 uVar18;
  undefined4 *puVar19;
  ulong uVar20;
  ctype *pcVar21;
  long local_a0;
  ulong local_98;
  undefined4 **local_90;
  undefined4 *local_88;
  undefined4 local_80;
  char cStack_7c;
  undefined2 uStack_7b;
  char cStack_79;
  undefined3 uStack_78;
  undefined5 uStack_75;
  undefined8 local_70;
  long local_68;
  
  ptVar14 = (tm *)(ulong)(byte)param_6;
  local_98 = (ulong)param_2;
  this = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  param_5->tm_sec = 0;
  ios_base::getloc();
  puVar5 = PTR_id_01ff5500;
  local_70 = 0;
  local_80 = SUB84(PTR_id_01ff5500,0);
  cStack_7c = (char)((ulong)PTR_id_01ff5500 >> 0x20);
  uStack_7b = (undefined2)((ulong)PTR_id_01ff5500 >> 0x28);
  cStack_79 = (char)((ulong)PTR_id_01ff5500 >> 0x38);
  uStack_78 = SUB83(PTR___init_01ff5688,0);
  uStack_75 = (undefined5)((ulong)PTR___init_01ff5688 >> 0x18);
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_88 = &local_80;
    local_90 = &local_88;
                    /* try { // try from 00e6825c to 00e68273 has its CatchHandler @ 00e6885c */
    __call_once((ulong *)PTR_id_01ff5500,&local_90,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_a0 + 0x18) - *(long *)(local_a0 + 0x10) >> 3) <=
       (long)*(int *)(puVar5 + 8) - 1U) ||
     (pcVar21 = *(ctype **)(*(long *)(local_a0 + 0x10) + ((long)*(int *)(puVar5 + 8) - 1U) * 8),
     pcVar21 == (ctype *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e68854 to 00e68857 has its CatchHandler @ 00e6885c */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  iVar13 = (istreambuf_iterator)param_3;
  iVar12 = (istreambuf_iterator)local_98;
  switch(param_7) {
  case '%':
    __get_percent((time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                   *)this,(istreambuf_iterator *)&local_98,iVar13,(uint *)param_5,pcVar21);
    uVar9 = local_98;
    goto LAB_00e687c8;
  default:
    goto code_r0x00e687b8;
  case 'A':
  case 'a':
    lVar7 = (**(code **)this[2])(this + 2);
    lVar8 = FUN_00e5bd3c(&local_98,param_3,lVar7,lVar7 + 0x150,pcVar21,param_5,0);
    uVar9 = local_98;
    if (lVar8 - lVar7 < 0x150) {
      lVar7 = (lVar8 - lVar7 >> 3) * -0x5555555555555555;
      auVar3 = SEXT816(lVar7) * SEXT816(0x4924924924924925);
      ptVar14->tm_wday = (int)lVar7 + ((int)(auVar3._8_8_ >> 1) - (auVar3._12_4_ >> 0x1f)) * -7;
    }
    goto LAB_00e687c8;
  case 'B':
  case 'b':
  case 'h':
    lVar7 = (**(code **)(this[2] + 8))(this + 2);
    lVar8 = FUN_00e5bd3c(&local_98,param_3,lVar7,lVar7 + 0x240,pcVar21,param_5,0);
    uVar9 = local_98;
    if (lVar8 - lVar7 < 0x240) {
      lVar7 = (lVar8 - lVar7 >> 3) * -0x5555555555555555;
      ptVar14->tm_mon =
           (int)lVar7 +
           ((int)((ulong)(lVar7 / 6 + (lVar7 >> 0x3f)) >> 1) -
           (SUB164(SEXT816(lVar7) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
    }
    goto LAB_00e687c8;
  case 'D':
    uVar18 = 0x79252f64252f6d25;
    goto LAB_00e6865c;
  case 'F':
    uVar18 = 0x64252d6d252d5925;
    goto LAB_00e6865c;
  case 'H':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if (iVar6 < 0x18) {
LAB_00e685e8:
      if ((uVar16 >> 2 & 1) == 0) {
        ptVar14->tm_hour = iVar6;
        uVar9 = local_98;
        goto LAB_00e687c8;
      }
    }
    break;
  case 'I':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if (iVar6 - 1U < 0xc) goto LAB_00e685e8;
    break;
  case 'M':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if ((iVar6 < 0x3c) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_min = iVar6;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'R':
    cStack_7c = 'M';
    local_80 = 0x253a4825;
    puVar15 = (undefined5 *)&uStack_7b;
    goto LAB_00e6866c;
  case 'S':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if ((iVar6 < 0x3d) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_sec = iVar6;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'T':
    uVar18 = 0x53253a4d253a4825;
LAB_00e6865c:
    local_80 = (undefined4)uVar18;
    cStack_7c = (char)((ulong)uVar18 >> 0x20);
    uStack_7b = (undefined2)((ulong)uVar18 >> 0x28);
    cStack_79 = (char)((ulong)uVar18 >> 0x38);
    puVar15 = (undefined5 *)&uStack_78;
LAB_00e6866c:
    puVar19 = &local_80;
LAB_00e68670:
    local_98 = get((time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                    *)this,iVar12,iVar13,(ios_base *)param_4,(uint *)param_5,ptVar14,(char *)puVar19
                   ,(char *)puVar15);
    uVar9 = local_98;
    goto LAB_00e687c8;
  case 'X':
    pcVar17 = *(code **)(this[2] + 0x30);
    goto LAB_00e684d8;
  case 'Y':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,4);
    uVar9 = local_98;
    if ((*(byte *)&param_5->tm_sec >> 2 & 1) == 0) {
      ptVar14->tm_year = iVar6 + -0x76c;
    }
    goto LAB_00e687c8;
  case 'c':
    pcVar17 = *(code **)(this[2] + 0x18);
LAB_00e684d8:
    pbVar10 = (byte *)(*pcVar17)();
    uVar9 = *(ulong *)(pbVar10 + 8);
    puVar19 = *(undefined4 **)(pbVar10 + 0x10);
    iVar12 = (istreambuf_iterator)local_98;
    if ((*pbVar10 & 1) == 0) {
      puVar19 = (undefined4 *)(pbVar10 + 1);
      uVar9 = (ulong)(*pbVar10 >> 1);
    }
    puVar15 = (undefined5 *)((long)puVar19 + uVar9);
    goto LAB_00e68670;
  case 'd':
  case 'e':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if ((iVar6 - 1U < 0x1f) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_mday = iVar6;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'j':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,3);
    uVar16 = param_5->tm_sec;
    if ((iVar6 < 0x16e) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_yday = iVar6;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'm':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,2);
    uVar16 = param_5->tm_sec;
    if ((iVar6 < 0xd) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_mon = iVar6 + -1;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'n':
  case 't':
    __get_white_space((time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                       *)this,(istreambuf_iterator *)&local_98,iVar13,(uint *)param_5,pcVar21);
    uVar9 = local_98;
    goto LAB_00e687c8;
  case 'p':
    pbVar10 = (byte *)(**(code **)(this[2] + 0x10))(this + 2);
    if ((*pbVar10 & 1) == 0) {
      uVar9 = (ulong)(*pbVar10 >> 1);
    }
    else {
      uVar9 = *(ulong *)(pbVar10 + 8);
    }
    if ((pbVar10[0x18] & 1) == 0) {
      uVar20 = (ulong)(pbVar10[0x18] >> 1);
    }
    else {
      uVar20 = *(ulong *)(pbVar10 + 0x20);
    }
    if (uVar9 + uVar20 != 0) {
      pbVar11 = (byte *)FUN_00e5bd3c(&local_98,param_3,pbVar10,pbVar10 + 0x30,pcVar21,param_5,0);
      iVar6 = ptVar14->tm_hour;
      uVar9 = local_98;
      if ((iVar6 == 0xc) && (pbVar11 == pbVar10)) {
        ptVar14->tm_hour = 0;
      }
      else if ((iVar6 < 0xc) && ((long)pbVar11 - (long)pbVar10 == 0x18)) {
        ptVar14->tm_hour = iVar6 + 0xc;
      }
      goto LAB_00e687c8;
    }
    goto code_r0x00e687b8;
  case 'r':
    local_80 = (undefined4)s__I__M__S__p_008382a7._0_8_;
    cStack_7c = SUB81(s__I__M__S__p_008382a7._0_8_,4);
    uStack_7b = SUB82(s__I__M__S__p_008382a7._0_8_,5);
    uStack_78 = 0x702520;
    cStack_79 = SUB81(s__I__M__S__p_008382a7._0_8_,7);
    puVar15 = &uStack_75;
    goto LAB_00e6866c;
  case 'w':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,1);
    uVar16 = param_5->tm_sec;
    if ((iVar6 < 7) && ((uVar16 >> 2 & 1) == 0)) {
      ptVar14->tm_wday = iVar6;
      uVar9 = local_98;
      goto LAB_00e687c8;
    }
    break;
  case 'x':
    uVar9 = (**(code **)(*this + 0x28))(this,local_98,param_3,param_4,param_5,ptVar14);
    goto LAB_00e687c8;
  case 'y':
    iVar6 = FUN_00e69024(&local_98,param_3,param_5,pcVar21,4);
    uVar9 = local_98;
    if ((*(byte *)&param_5->tm_sec >> 2 & 1) == 0) {
      iVar1 = iVar6 + 0x76c;
      if (99 < iVar6) {
        iVar1 = iVar6;
      }
      iVar2 = iVar6 + 2000;
      if (0x44 < iVar6) {
        iVar2 = iVar1;
      }
      ptVar14->tm_year = iVar2 + -0x76c;
    }
    goto LAB_00e687c8;
  }
LAB_00e687bc:
  param_5->tm_sec = uVar16 | 4;
  uVar9 = local_98;
LAB_00e687c8:
  if (*(long *)(lVar4 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar9);
  }
  return;
code_r0x00e687b8:
  uVar16 = param_5->tm_sec;
  goto LAB_00e687bc;
}



// ==========================================================================================
// Function: do_date_order
// Address: 00e69850
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_date_order() const */

undefined8
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_date_order(void)

{
  return 2;
}



// ==========================================================================================
// Function: do_get_time
// Address: 00e6985c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get_time(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get_time(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  long lVar1;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  wchar_t awStack_30 [2];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  uStack_48 = _UNK_0060d9e4;
  local_50 = _DAT_0060d9dc;
  uStack_38 = _UNK_0060d9f4;
  uStack_40 = _DAT_0060d9ec;
  get(this,param_1,param_2,param_3,param_4,param_5,(wchar_t *)&local_50,awStack_30);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get_date
// Address: 00e698c4
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get_date(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get_date(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  ulong uVar1;
  wchar_t *pwVar2;
  byte *pbVar3;
  
  pbVar3 = (byte *)(**(code **)(*(long *)(this + 0x10) + 0x28))();
  uVar1 = (ulong)(*pbVar3 >> 1);
  pwVar2 = (wchar_t *)(pbVar3 + 4);
  if ((*pbVar3 & 1) != 0) {
    uVar1 = *(ulong *)(pbVar3 + 8);
    pwVar2 = *(wchar_t **)(pbVar3 + 0x10);
  }
  get(this,param_1,param_2,param_3,param_4,param_5,pwVar2,pwVar2 + uVar1);
  return;
}



// ==========================================================================================
// Function: do_get_weekday
// Address: 00e69950
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get_weekday(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get_weekday(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
               *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
              uint *param_4,tm *param_5)

{
  undefined auVar1 [16];
  long lVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  long local_90;
  ulong local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  local_88 = (ulong)param_1;
  lVar2 = tpidr_el0;
  local_58 = *(long *)(lVar2 + 0x28);
  ios_base::getloc();
  puVar3 = PTR_id_01ff5620;
  local_70 = 0;
  local_80 = PTR_id_01ff5620;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e699d0 to 00e699e7 has its CatchHandler @ 00e69ac8 */
    __call_once((ulong *)PTR_id_01ff5620,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_90 + 0x18) - *(long *)(local_90 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (lVar5 = *(long *)(*(long *)(local_90 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     lVar5 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e69ac0 to 00e69ac3 has its CatchHandler @ 00e69ac8 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  lVar4 = (***(code ***)(this + 0x10))(this + 0x10);
  lVar5 = FUN_00e5eea8(&local_88,param_2,lVar4,lVar4 + 0x150,lVar5,param_4,0);
  if (lVar5 - lVar4 < 0x150) {
    lVar5 = (lVar5 - lVar4 >> 3) * -0x5555555555555555;
    auVar1 = SEXT816(lVar5) * SEXT816(0x4924924924924925);
    param_5->tm_wday = (int)lVar5 + ((int)(auVar1._8_8_ >> 1) - (auVar1._12_4_ >> 0x1f)) * -7;
  }
  if (*(long *)(lVar2 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_88);
}



// ==========================================================================================
// Function: do_get_monthname
// Address: 00e69b9c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get_monthname(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get_monthname(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                 *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
                uint *param_4,tm *param_5)

{
  long lVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long local_90;
  ulong local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  local_88 = (ulong)param_1;
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar2 = PTR_id_01ff5620;
  local_70 = 0;
  local_80 = PTR_id_01ff5620;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e69c1c to 00e69c33 has its CatchHandler @ 00e69d10 */
    __call_once((ulong *)PTR_id_01ff5620,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_90 + 0x18) - *(long *)(local_90 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (lVar4 = *(long *)(*(long *)(local_90 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     lVar4 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e69d08 to 00e69d0b has its CatchHandler @ 00e69d10 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  lVar3 = (**(code **)(*(long *)(this + 0x10) + 8))(this + 0x10);
  lVar4 = FUN_00e5eea8(&local_88,param_2,lVar3,lVar3 + 0x240,lVar4,param_4,0);
  if (lVar4 - lVar3 < 0x240) {
    lVar4 = (lVar4 - lVar3 >> 3) * -0x5555555555555555;
    param_5->tm_mon =
         (int)lVar4 +
         ((int)((ulong)(lVar4 / 6 + (lVar4 >> 0x3f)) >> 1) -
         (SUB164(SEXT816(lVar4) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_88);
}



// ==========================================================================================
// Function: do_get_year
// Address: 00e69de0
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get_year(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get_year(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
           uint *param_4,tm *param_5)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined *puVar4;
  int iVar5;
  long lVar6;
  long local_80;
  ulong local_78;
  undefined *local_70;
  undefined *puStack_68;
  undefined8 local_60;
  undefined ***local_58;
  undefined **local_50;
  long local_48;
  
  local_78 = (ulong)param_1;
  lVar3 = tpidr_el0;
  local_48 = *(long *)(lVar3 + 0x28);
  ios_base::getloc();
  puVar4 = PTR_id_01ff5620;
  local_60 = 0;
  local_70 = PTR_id_01ff5620;
  puStack_68 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_50 = &local_70;
    local_58 = &local_50;
                    /* try { // try from 00e69e58 to 00e69e6f has its CatchHandler @ 00e69f10 */
    __call_once((ulong *)PTR_id_01ff5620,&local_58,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_80 + 0x18) - *(long *)(local_80 + 0x10) >> 3) <=
       (long)*(int *)(puVar4 + 8) - 1U) ||
     (lVar6 = *(long *)(*(long *)(local_80 + 0x10) + ((long)*(int *)(puVar4 + 8) - 1U) * 8),
     lVar6 == 0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e69f08 to 00e69f0b has its CatchHandler @ 00e69f10 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  iVar5 = FUN_00e6ae50(&local_78,param_2,param_4,lVar6,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    iVar1 = iVar5 + 0x76c;
    if (99 < iVar5) {
      iVar1 = iVar5;
    }
    iVar2 = iVar5 + 2000;
    if (0x44 < iVar5) {
      iVar2 = iVar1;
    }
    param_5->tm_year = iVar2 + -0x76c;
  }
  if (*(long *)(lVar3 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_78);
}



// ==========================================================================================
// Function: do_get
// Address: 00e69f90
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, tm*, char, char)
   const */

void std::__ndk1::
     time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
     do_get(istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
           tm *param_5,char param_6,char param_7)

{
  int iVar1;
  int iVar2;
  undefined auVar3 [16];
  long lVar4;
  undefined *puVar5;
  int iVar6;
  long *this;
  long lVar7;
  long lVar8;
  ulong uVar9;
  byte *pbVar10;
  byte *pbVar11;
  istreambuf_iterator iVar12;
  istreambuf_iterator iVar13;
  tm *ptVar14;
  undefined **ppuVar15;
  wchar_t *pwVar16;
  uint uVar17;
  code *pcVar18;
  undefined8 *puVar19;
  ulong uVar20;
  ctype *pcVar21;
  long local_c0;
  ulong local_b8;
  undefined ***local_b0;
  undefined **local_a8;
  undefined *local_a0;
  undefined *puStack_98;
  undefined8 local_90;
  undefined4 uStack_88;
  undefined4 local_84;
  wchar_t wStack_80;
  undefined8 uStack_7c;
  wchar_t awStack_74 [3];
  long local_68;
  
  ptVar14 = (tm *)(ulong)(byte)param_6;
  local_b8 = (ulong)param_2;
  this = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  param_5->tm_sec = 0;
  ios_base::getloc();
  puVar5 = PTR_id_01ff5620;
  local_90 = 0;
  local_a0 = PTR_id_01ff5620;
  puStack_98 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_a8 = &local_a0;
    local_b0 = &local_a8;
                    /* try { // try from 00e6a020 to 00e6a037 has its CatchHandler @ 00e6a610 */
    __call_once((ulong *)PTR_id_01ff5620,&local_b0,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_c0 + 0x18) - *(long *)(local_c0 + 0x10) >> 3) <=
       (long)*(int *)(puVar5 + 8) - 1U) ||
     (pcVar21 = *(ctype **)(*(long *)(local_c0 + 0x10) + ((long)*(int *)(puVar5 + 8) - 1U) * 8),
     pcVar21 == (ctype *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6a608 to 00e6a60b has its CatchHandler @ 00e6a610 */
    FUN_00de5da0();
  }
  __shared_count::__release_shared();
  iVar13 = (istreambuf_iterator)param_3;
  iVar12 = (istreambuf_iterator)local_b8;
  switch(param_7) {
  case '%':
    __get_percent((time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                   *)this,(istreambuf_iterator *)&local_b8,iVar13,(uint *)param_5,pcVar21);
    uVar9 = local_b8;
    goto LAB_00e6a57c;
  default:
    goto code_r0x00e6a56c;
  case 'A':
  case 'a':
    lVar7 = (**(code **)this[2])(this + 2);
    lVar8 = FUN_00e5eea8(&local_b8,param_3,lVar7,lVar7 + 0x150,pcVar21,param_5,0);
    uVar9 = local_b8;
    if (lVar8 - lVar7 < 0x150) {
      lVar7 = (lVar8 - lVar7 >> 3) * -0x5555555555555555;
      auVar3 = SEXT816(lVar7) * SEXT816(0x4924924924924925);
      ptVar14->tm_wday = (int)lVar7 + ((int)(auVar3._8_8_ >> 1) - (auVar3._12_4_ >> 0x1f)) * -7;
    }
    goto LAB_00e6a57c;
  case 'B':
  case 'b':
  case 'h':
    lVar7 = (**(code **)(this[2] + 8))(this + 2);
    lVar8 = FUN_00e5eea8(&local_b8,param_3,lVar7,lVar7 + 0x240,pcVar21,param_5,0);
    uVar9 = local_b8;
    if (lVar8 - lVar7 < 0x240) {
      lVar7 = (lVar8 - lVar7 >> 3) * -0x5555555555555555;
      ptVar14->tm_mon =
           (int)lVar7 +
           ((int)((ulong)(lVar7 / 6 + (lVar7 >> 0x3f)) >> 1) -
           (SUB164(SEXT816(lVar7) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
    }
    goto LAB_00e6a57c;
  case 'D':
    puVar19 = (undefined8 *)&DAT_0060d9fc;
    goto LAB_00e6a40c;
  case 'F':
    puVar19 = (undefined8 *)&DAT_0060da3c;
    goto LAB_00e6a40c;
  case 'H':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if (iVar6 < 0x18) {
LAB_00e6a3a0:
      if ((uVar17 >> 2 & 1) == 0) {
        ptVar14->tm_hour = iVar6;
        uVar9 = local_b8;
        goto LAB_00e6a57c;
      }
    }
    break;
  case 'I':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if (iVar6 - 1U < 0xc) goto LAB_00e6a3a0;
    break;
  case 'M':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if ((iVar6 < 0x3c) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_min = iVar6;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'R':
    puStack_98 = _UNK_008382e8;
    local_a0 = _DAT_008382e0;
    local_90 = CONCAT44(local_90._4_4_,DAT_008382f0);
    pwVar16 = (wchar_t *)((long)&local_90 + 4);
    goto LAB_00e6a420;
  case 'S':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if ((iVar6 < 0x3d) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_sec = iVar6;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'T':
    puVar19 = (undefined8 *)&DAT_0060d9dc;
LAB_00e6a40c:
    puStack_98 = (undefined *)puVar19[1];
    local_a0 = (undefined *)*puVar19;
    local_90 = puVar19[2];
    pwVar16 = &wStack_80;
    uStack_88 = (undefined4)puVar19[3];
    local_84 = (undefined4)((ulong)puVar19[3] >> 0x20);
LAB_00e6a420:
    ppuVar15 = &local_a0;
LAB_00e6a424:
    local_b8 = get((time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                    *)this,iVar12,iVar13,(ios_base *)param_4,(uint *)param_5,ptVar14,
                   (wchar_t *)ppuVar15,pwVar16);
    uVar9 = local_b8;
    goto LAB_00e6a57c;
  case 'X':
    pcVar18 = *(code **)(this[2] + 0x30);
    goto LAB_00e6a298;
  case 'Y':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,4);
    uVar9 = local_b8;
    if ((*(byte *)&param_5->tm_sec >> 2 & 1) == 0) {
      ptVar14->tm_year = iVar6 + -0x76c;
    }
    goto LAB_00e6a57c;
  case 'c':
    pcVar18 = *(code **)(this[2] + 0x18);
LAB_00e6a298:
    pbVar10 = (byte *)(*pcVar18)();
    iVar12 = (istreambuf_iterator)local_b8;
    uVar9 = (ulong)(*pbVar10 >> 1);
    ppuVar15 = (undefined **)(pbVar10 + 4);
    if ((*pbVar10 & 1) != 0) {
      uVar9 = *(ulong *)(pbVar10 + 8);
      ppuVar15 = *(undefined ***)(pbVar10 + 0x10);
    }
    pwVar16 = (wchar_t *)((long)ppuVar15 + uVar9 * 4);
    goto LAB_00e6a424;
  case 'd':
  case 'e':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if ((iVar6 - 1U < 0x1f) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_mday = iVar6;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'j':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,3);
    uVar17 = param_5->tm_sec;
    if ((iVar6 < 0x16e) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_yday = iVar6;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'm':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,2);
    uVar17 = param_5->tm_sec;
    if ((iVar6 < 0xd) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_mon = iVar6 + -1;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'n':
  case 't':
    __get_white_space((time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                       *)this,(istreambuf_iterator *)&local_b8,iVar13,(uint *)param_5,pcVar21);
    uVar9 = local_b8;
    goto LAB_00e6a57c;
  case 'p':
    pbVar10 = (byte *)(**(code **)(this[2] + 0x10))(this + 2);
    if ((*pbVar10 & 1) == 0) {
      uVar9 = (ulong)(*pbVar10 >> 1);
    }
    else {
      uVar9 = *(ulong *)(pbVar10 + 8);
    }
    if ((pbVar10[0x18] & 1) == 0) {
      uVar20 = (ulong)(pbVar10[0x18] >> 1);
    }
    else {
      uVar20 = *(ulong *)(pbVar10 + 0x20);
    }
    if (uVar9 + uVar20 != 0) {
      pbVar11 = (byte *)FUN_00e5eea8(&local_b8,param_3,pbVar10,pbVar10 + 0x30,pcVar21,param_5,0);
      iVar6 = ptVar14->tm_hour;
      uVar9 = local_b8;
      if ((iVar6 == 0xc) && (pbVar11 == pbVar10)) {
        ptVar14->tm_hour = 0;
      }
      else if ((iVar6 < 0xc) && ((long)pbVar11 - (long)pbVar10 == 0x18)) {
        ptVar14->tm_hour = iVar6 + 0xc;
      }
      goto LAB_00e6a57c;
    }
    goto code_r0x00e6a56c;
  case 'r':
    puStack_98 = _UNK_008382bc;
    local_a0 = _DAT_008382b4;
    uStack_88 = _UNK_008382cc;
    local_90 = _DAT_008382c4;
    uStack_7c = _UNK_008382d8;
    local_84 = _DAT_008382d0;
    wStack_80 = _UNK_008382d4;
    pwVar16 = awStack_74;
    goto LAB_00e6a420;
  case 'w':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,1);
    uVar17 = param_5->tm_sec;
    if ((iVar6 < 7) && ((uVar17 >> 2 & 1) == 0)) {
      ptVar14->tm_wday = iVar6;
      uVar9 = local_b8;
      goto LAB_00e6a57c;
    }
    break;
  case 'x':
    uVar9 = (**(code **)(*this + 0x28))(this,local_b8,param_3,param_4,param_5,ptVar14);
    goto LAB_00e6a57c;
  case 'y':
    iVar6 = FUN_00e6ae50(&local_b8,param_3,param_5,pcVar21,4);
    uVar9 = local_b8;
    if ((*(byte *)&param_5->tm_sec >> 2 & 1) == 0) {
      iVar1 = iVar6 + 0x76c;
      if (99 < iVar6) {
        iVar1 = iVar6;
      }
      iVar2 = iVar6 + 2000;
      if (0x44 < iVar6) {
        iVar2 = iVar1;
      }
      ptVar14->tm_year = iVar2 + -0x76c;
    }
    goto LAB_00e6a57c;
  }
LAB_00e6a570:
  param_5->tm_sec = uVar17 | 4;
  uVar9 = local_b8;
LAB_00e6a57c:
  if (*(long *)(lVar4 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar9);
  }
  return;
code_r0x00e6a56c:
  uVar17 = param_5->tm_sec;
  goto LAB_00e6a570;
}



// ==========================================================================================
// Function: do_put
// Address: 00e6b494
// ==========================================================================================

/* std::__ndk1::time_put<char, std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::do_put(std::__ndk1::ostreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, char, tm const*, char, char) const */

long * __thiscall
std::__ndk1::time_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(time_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,ios_base *param_2,char param_3,tm *param_4,char param_5,
      char param_6)

{
  char cVar1;
  long lVar2;
  int iVar3;
  size_t sVar4;
  long *plVar5;
  char *pcVar6;
  long *plVar7;
  char *pcVar8;
  char local_a0;
  char local_9f;
  char local_9e;
  undefined local_9d;
  char local_9c [100];
  long local_38;
  
  plVar5 = (long *)(ulong)param_1;
  lVar2 = tpidr_el0;
  local_38 = *(long *)(lVar2 + 0x28);
  local_a0 = '%';
  local_9d = 0;
  local_9f = param_5;
  local_9e = param_6;
  if (param_6 != '\0') {
    local_9f = param_6;
    local_9e = param_5;
  }
  sVar4 = strftime_l(local_9c,100,&local_a0,param_4,*(__locale_t *)(this + 0x10));
  if (sVar4 != 0) {
    pcVar8 = local_9c;
    plVar7 = plVar5;
    do {
      plVar5 = plVar7;
      if (plVar7 != (long *)0x0) {
        pcVar6 = (char *)plVar7[6];
        cVar1 = *pcVar8;
        if (pcVar6 == (char *)plVar7[7]) {
          iVar3 = (**(code **)(*plVar7 + 0x68))(plVar7);
          plVar5 = (long *)0x0;
          if (iVar3 != -1) {
            plVar5 = plVar7;
          }
        }
        else {
          plVar7[6] = (long)(pcVar6 + 1);
          *pcVar6 = cVar1;
        }
      }
      sVar4 = sVar4 - 1;
      pcVar8 = pcVar8 + 1;
      plVar7 = plVar5;
    } while (sVar4 != 0);
  }
  if (*(long *)(lVar2 + 0x28) != local_38) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return plVar5;
}



// ==========================================================================================
// Function: do_put
// Address: 00e6b90c
// ==========================================================================================

/* std::__ndk1::time_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, wchar_t, tm const*, char, char)
   const */

long * __thiscall
std::__ndk1::
time_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_put(time_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
       *this,ostreambuf_iterator param_1,ios_base *param_2,wchar_t param_3,tm *param_4,char param_5,
      char param_6)

{
  long lVar1;
  long *plVar2;
  int iVar3;
  long *plVar4;
  int *piVar5;
  long *plVar6;
  long *plVar7;
  long *local_1e0;
  long local_1d8 [50];
  long local_48;
  
  plVar4 = (long *)(ulong)param_1;
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  local_1e0 = &local_48;
  __time_put::__do_put
            ((__time_put *)(this + 0x10),(wchar_t *)local_1d8,(wchar_t **)&local_1e0,param_4,param_5
             ,param_6);
  plVar2 = local_1e0;
  if (local_1d8 != local_1e0) {
    plVar7 = local_1d8;
    plVar6 = plVar4;
    do {
      plVar4 = plVar6;
      if (plVar6 != (long *)0x0) {
        piVar5 = (int *)plVar6[6];
        iVar3 = *(int *)plVar7;
        if (piVar5 == (int *)plVar6[7]) {
          iVar3 = (**(code **)(*plVar6 + 0x68))(plVar6);
        }
        else {
          plVar6[6] = (long)(piVar5 + 1);
          *piVar5 = iVar3;
        }
        plVar4 = (long *)0x0;
        if (iVar3 != -1) {
          plVar4 = plVar6;
        }
      }
      plVar7 = (long *)((long)plVar7 + 4);
      plVar6 = plVar4;
    } while (plVar2 != plVar7);
  }
  if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return plVar4;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bb10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_decimal_point() const */

undefined8 std::__ndk1::moneypunct<char,false>::do_decimal_point(void)

{
  return 0xff;
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bb1c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_thousands_sep() const */

undefined8 std::__ndk1::moneypunct<char,false>::do_thousands_sep(void)

{
  return 0xff;
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bb28
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_grouping() const */

void std::__ndk1::moneypunct<char,false>::do_grouping(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bb38
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_curr_symbol() const */

void std::__ndk1::moneypunct<char,false>::do_curr_symbol(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bb48
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_positive_sign() const */

void std::__ndk1::moneypunct<char,false>::do_positive_sign(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bb58
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_negative_sign() const */

void std::__ndk1::moneypunct<char,false>::do_negative_sign(void)

{
  undefined2 *in_x8;
  
  *in_x8 = 0x2d02;
  *(undefined *)(in_x8 + 1) = 0;
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bb6c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_frac_digits() const */

undefined8 std::__ndk1::moneypunct<char,false>::do_frac_digits(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bb78
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_pos_format() const */

undefined8 std::__ndk1::moneypunct<char,false>::do_pos_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bb88
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, false>::do_neg_format() const */

undefined8 std::__ndk1::moneypunct<char,false>::do_neg_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bb98
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_decimal_point() const */

undefined8 std::__ndk1::moneypunct<char,true>::do_decimal_point(void)

{
  return 0xff;
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bba4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_thousands_sep() const */

undefined8 std::__ndk1::moneypunct<char,true>::do_thousands_sep(void)

{
  return 0xff;
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bbb0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_grouping() const */

void std::__ndk1::moneypunct<char,true>::do_grouping(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bbc0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_curr_symbol() const */

void std::__ndk1::moneypunct<char,true>::do_curr_symbol(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bbd0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_positive_sign() const */

void std::__ndk1::moneypunct<char,true>::do_positive_sign(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bbe0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_negative_sign() const */

void std::__ndk1::moneypunct<char,true>::do_negative_sign(void)

{
  undefined2 *in_x8;
  
  *in_x8 = 0x2d02;
  *(undefined *)(in_x8 + 1) = 0;
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bbf4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_frac_digits() const */

undefined8 std::__ndk1::moneypunct<char,true>::do_frac_digits(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bc00
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_pos_format() const */

undefined8 std::__ndk1::moneypunct<char,true>::do_pos_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bc10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<char, true>::do_neg_format() const */

undefined8 std::__ndk1::moneypunct<char,true>::do_neg_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bc20
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_decimal_point() const */

undefined8 std::__ndk1::moneypunct<wchar_t,false>::do_decimal_point(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bc2c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_thousands_sep() const */

undefined8 std::__ndk1::moneypunct<wchar_t,false>::do_thousands_sep(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bc38
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_grouping() const */

void std::__ndk1::moneypunct<wchar_t,false>::do_grouping(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bc48
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_curr_symbol() const */

void std::__ndk1::moneypunct<wchar_t,false>::do_curr_symbol(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bc58
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_positive_sign() const */

void std::__ndk1::moneypunct<wchar_t,false>::do_positive_sign(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bc68
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_negative_sign() const */

void std::__ndk1::moneypunct<wchar_t,false>::do_negative_sign(void)

{
  undefined *in_x8;
  
  *in_x8 = 2;
                    /* try { // try from 00e6bc88 to 00e6bc93 has its CatchHandler @ 00e6bca8 */
  wmemset((wchar_t *)(in_x8 + 4),L'-',1);
  *(undefined4 *)(in_x8 + 8) = 0;
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bcac
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_frac_digits() const */

undefined8 std::__ndk1::moneypunct<wchar_t,false>::do_frac_digits(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bcb8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_pos_format() const */

undefined8 std::__ndk1::moneypunct<wchar_t,false>::do_pos_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bcc8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, false>::do_neg_format() const */

undefined8 std::__ndk1::moneypunct<wchar_t,false>::do_neg_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bcd8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_decimal_point() const */

undefined8 std::__ndk1::moneypunct<wchar_t,true>::do_decimal_point(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bce4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_thousands_sep() const */

undefined8 std::__ndk1::moneypunct<wchar_t,true>::do_thousands_sep(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bcf0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_grouping() const */

void std::__ndk1::moneypunct<wchar_t,true>::do_grouping(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bd00
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_curr_symbol() const */

void std::__ndk1::moneypunct<wchar_t,true>::do_curr_symbol(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bd10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_positive_sign() const */

void std::__ndk1::moneypunct<wchar_t,true>::do_positive_sign(void)

{
  undefined8 *in_x8;
  
  *in_x8 = 0;
  in_x8[1] = 0;
  in_x8[2] = 0;
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bd20
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_negative_sign() const */

void std::__ndk1::moneypunct<wchar_t,true>::do_negative_sign(void)

{
  undefined *in_x8;
  
  *in_x8 = 2;
                    /* try { // try from 00e6bd40 to 00e6bd4b has its CatchHandler @ 00e6bd60 */
  wmemset((wchar_t *)(in_x8 + 4),L'-',1);
  *(undefined4 *)(in_x8 + 8) = 0;
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bd64
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_frac_digits() const */

undefined8 std::__ndk1::moneypunct<wchar_t,true>::do_frac_digits(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bd70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_pos_format() const */

undefined8 std::__ndk1::moneypunct<wchar_t,true>::do_pos_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bd80
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct<wchar_t, true>::do_neg_format() const */

undefined8 std::__ndk1::moneypunct<wchar_t,true>::do_neg_format(void)

{
  return 0x4000302;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bd90
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_decimal_point() const */

undefined std::__ndk1::moneypunct_byname<char,false>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bd9c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_thousands_sep() const */

undefined std::__ndk1::moneypunct_byname<char,false>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x11);
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bda8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_grouping() const */

void std::__ndk1::moneypunct_byname<char,false>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bdb8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_curr_symbol() const */

void std::__ndk1::moneypunct_byname<char,false>::do_curr_symbol(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x30));
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bdc8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_positive_sign() const */

void std::__ndk1::moneypunct_byname<char,false>::do_positive_sign(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x48));
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bdd8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_negative_sign() const */

void std::__ndk1::moneypunct_byname<char,false>::do_negative_sign(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x60));
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bde8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_frac_digits() const */

undefined4 std::__ndk1::moneypunct_byname<char,false>::do_frac_digits(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x78);
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bdf4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_pos_format() const */

undefined4 std::__ndk1::moneypunct_byname<char,false>::do_pos_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x7c);
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6be00
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, false>::do_neg_format() const */

undefined4 std::__ndk1::moneypunct_byname<char,false>::do_neg_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x80);
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6be0c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_decimal_point() const */

undefined std::__ndk1::moneypunct_byname<char,true>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6be18
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_thousands_sep() const */

undefined std::__ndk1::moneypunct_byname<char,true>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x11);
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6be24
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_grouping() const */

void std::__ndk1::moneypunct_byname<char,true>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6be34
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_curr_symbol() const */

void std::__ndk1::moneypunct_byname<char,true>::do_curr_symbol(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x30));
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6be44
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_positive_sign() const */

void std::__ndk1::moneypunct_byname<char,true>::do_positive_sign(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x48));
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6be54
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_negative_sign() const */

void std::__ndk1::moneypunct_byname<char,true>::do_negative_sign(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x60));
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6be64
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_frac_digits() const */

undefined4 std::__ndk1::moneypunct_byname<char,true>::do_frac_digits(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x78);
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6be70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_pos_format() const */

undefined4 std::__ndk1::moneypunct_byname<char,true>::do_pos_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x7c);
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6be7c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<char, true>::do_neg_format() const */

undefined4 std::__ndk1::moneypunct_byname<char,true>::do_neg_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x80);
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6be88
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_decimal_point() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,false>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6be94
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_thousands_sep() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,false>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x14);
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bea0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_grouping() const */

void std::__ndk1::moneypunct_byname<wchar_t,false>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6beb0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_curr_symbol() const */

void std::__ndk1::moneypunct_byname<wchar_t,false>::do_curr_symbol(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x30));
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bec0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_positive_sign() const */

void std::__ndk1::moneypunct_byname<wchar_t,false>::do_positive_sign(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x48));
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bed0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_negative_sign() const */

void std::__ndk1::moneypunct_byname<wchar_t,false>::do_negative_sign(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x60));
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bee0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_frac_digits() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,false>::do_frac_digits(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x78);
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6beec
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_pos_format() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,false>::do_pos_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x7c);
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bef8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, false>::do_neg_format() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,false>::do_neg_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x80);
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e6bf04
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_decimal_point() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,true>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e6bf10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_thousands_sep() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,true>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x14);
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e6bf1c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_grouping() const */

void std::__ndk1::moneypunct_byname<wchar_t,true>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_curr_symbol
// Address: 00e6bf2c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_curr_symbol() const */

void std::__ndk1::moneypunct_byname<wchar_t,true>::do_curr_symbol(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x30));
  return;
}



// ==========================================================================================
// Function: do_positive_sign
// Address: 00e6bf3c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_positive_sign() const */

void std::__ndk1::moneypunct_byname<wchar_t,true>::do_positive_sign(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x48));
  return;
}



// ==========================================================================================
// Function: do_negative_sign
// Address: 00e6bf4c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_negative_sign() const */

void std::__ndk1::moneypunct_byname<wchar_t,true>::do_negative_sign(void)

{
  long in_x0;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,(basic_string *)(in_x0 + 0x60));
  return;
}



// ==========================================================================================
// Function: do_frac_digits
// Address: 00e6bf5c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_frac_digits() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,true>::do_frac_digits(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x78);
}



// ==========================================================================================
// Function: do_pos_format
// Address: 00e6bf68
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_pos_format() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,true>::do_pos_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x7c);
}



// ==========================================================================================
// Function: do_neg_format
// Address: 00e6bf74
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::moneypunct_byname<wchar_t, true>::do_neg_format() const */

undefined4 std::__ndk1::moneypunct_byname<wchar_t,true>::do_neg_format(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x80);
}



// ==========================================================================================
// Function: do_get
// Address: 00e6bf80
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::money_get<char, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> > >::do_get(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, bool, std::__ndk1::ios_base&, unsigned int&, long double&)
   const */

long * __thiscall
std::__ndk1::money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,bool param_3,ios_base *param_4,
      uint *param_5,longdouble *param_6)

{
  char cVar1;
  long lVar2;
  undefined *puVar3;
  char *pcVar4;
  int iVar5;
  ulong uVar6;
  undefined **__ptr;
  long *plVar7;
  undefined8 *puVar8;
  undefined **ppuVar9;
  undefined **ppuVar10;
  char *pcVar11;
  long *plVar12;
  bool local_184 [4];
  long local_180;
  char *local_178;
  char *local_170;
  code *local_168;
  long *local_160;
  undefined *local_158;
  undefined *puStack_150;
  undefined8 local_148;
  undefined local_f0 [5];
  char cStack_eb;
  char cStack_ea;
  char cStack_e9;
  char local_e8;
  char local_e7;
  undefined auStack_e6 [6];
  undefined7 local_e0;
  undefined4 uStack_d9;
  char local_d4 [100];
  long local_70 [2];
  
  plVar7 = (long *)(ulong)param_2;
  local_160 = (long *)(ulong)param_1;
  lVar2 = tpidr_el0;
  local_70[0] = *(long *)(lVar2 + 0x28);
  local_170 = local_d4;
  local_168 = (code *)PTR___do_nothing_01ff56a8;
                    /* try { // try from 00e6bfd8 to 00e6bfe3 has its CatchHandler @ 00e6c350 */
  ios_base::getloc();
  puVar3 = PTR_id_01ff5500;
  local_148 = 0;
  local_158 = PTR_id_01ff5500;
  puStack_150 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    _local_f0 = &local_e0;
    local_e0 = SUB87(&local_158,0);
    uStack_d9._0_1_ = (char)((ulong)&local_158 >> 0x38);
                    /* try { // try from 00e6c020 to 00e6c037 has its CatchHandler @ 00e6c36c */
    __call_once((ulong *)PTR_id_01ff5500,local_f0,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_180 + 0x18) - *(long *)(local_180 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar12 = *(long **)(*(long *)(local_180 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar12 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6c318 to 00e6c31b has its CatchHandler @ 00e6c36c */
    FUN_00de5da0();
  }
  local_184[0] = false;
                    /* try { // try from 00e6c064 to 00e6c093 has its CatchHandler @ 00e6c368 */
  uVar6 = __do_get((istreambuf_iterator *)&local_160,param_2,param_3,(locale *)&local_180,
                   *(uint *)(param_4 + 8),param_5,local_184,(ctype *)plVar12,
                   (unique_ptr *)&local_170,&local_178,(char *)local_70);
  if ((uVar6 & 1) != 0) {
    local_e0 = (undefined7)s_0123456789_005c474a._0_8_;
    uStack_d9._0_1_ = SUB81(s_0123456789_005c474a._0_8_,7);
    uStack_d9 = CONCAT31(0x3938,(char)uStack_d9);
                    /* try { // try from 00e6c0c4 to 00e6c0d3 has its CatchHandler @ 00e6c348 */
    (**(code **)(*plVar12 + 0x40))(plVar12,&local_e0,(long)&uStack_d9 + 3,local_f0);
    pcVar11 = local_170;
    pcVar4 = local_178;
    if ((long)local_178 - (long)local_170 < 99) {
      __ptr = (undefined **)0x0;
      ppuVar10 = &local_158;
joined_r0x00e6c2fc:
      ppuVar9 = ppuVar10;
      if (local_184[0] != false) {
        ppuVar9 = (undefined **)((long)ppuVar10 + 1);
        *(char *)ppuVar10 = '-';
      }
      if (pcVar11 < pcVar4) {
        ppuVar10 = ppuVar9;
        do {
          cVar1 = *pcVar11;
          if (local_f0[0] == cVar1) {
            puVar8 = (undefined8 *)local_f0;
          }
          else {
            puVar8 = (undefined8 *)((ulong)local_f0 | 1);
            if (((((local_f0[1] != cVar1) &&
                  (puVar8 = (undefined8 *)((ulong)local_f0 | 2), local_f0[2] != cVar1)) &&
                 (puVar8 = (undefined8 *)((ulong)local_f0 | 3), local_f0[3] != cVar1)) &&
                (((puVar8 = (undefined8 *)((long)local_f0 + 4), local_f0[4] != cVar1 &&
                  (puVar8 = (undefined8 *)((long)local_f0 + 5), cStack_eb != cVar1)) &&
                 ((puVar8 = (undefined8 *)((long)local_f0 + 6), cStack_ea != cVar1 &&
                  ((puVar8 = (undefined8 *)((long)local_f0 + 7), cStack_e9 != cVar1 &&
                   (puVar8 = (undefined8 *)&local_e8, local_e8 != cVar1)))))))) &&
               (puVar8 = (undefined8 *)&local_e7, local_e7 != cVar1)) {
              puVar8 = (undefined8 *)auStack_e6;
            }
          }
          pcVar11 = pcVar11 + 1;
          ppuVar9 = (undefined **)((long)ppuVar10 + 1);
          *(char *)ppuVar10 = *(char *)((long)puVar8 + ((long)&local_e0 - (long)local_f0));
          ppuVar10 = ppuVar9;
        } while (pcVar11 < local_178);
      }
      *(char *)ppuVar9 = '\0';
      iVar5 = sscanf((char *)&local_158,"%Lf",param_6);
      if (iVar5 == 1) {
        if (__ptr != (undefined **)0x0) {
          free(__ptr);
        }
        goto LAB_00e6c230;
      }
                    /* try { // try from 00e6c31c to 00e6c327 has its CatchHandler @ 00e6c334 */
      __throw_runtime_error("money_get error");
    }
    else {
      __ptr = (undefined **)malloc(((long)local_178 - (long)local_170) + 2);
      ppuVar10 = __ptr;
      if (__ptr != (undefined **)0x0) goto joined_r0x00e6c2fc;
    }
                    /* try { // try from 00e6c328 to 00e6c32b has its CatchHandler @ 00e6c330 */
    __throw_bad_alloc();
    goto LAB_00e6c32c;
  }
LAB_00e6c230:
                    /* try { // try from 00e6c24c to 00e6c27f has its CatchHandler @ 00e6c368 */
  if (((local_160 == (long *)0x0) || (local_160[3] != local_160[4])) ||
     (iVar5 = (**(code **)(*local_160 + 0x48))(local_160), iVar5 != -1)) {
    plVar12 = local_160;
    if (plVar7 != (long *)0x0) goto LAB_00e6c264;
LAB_00e6c310:
    if (plVar12 == (long *)0x0) {
LAB_00e6c28c:
      *param_5 = *param_5 | 2;
    }
  }
  else {
    plVar12 = (long *)0x0;
    local_160 = (long *)0x0;
    if (plVar7 == (long *)0x0) goto LAB_00e6c310;
LAB_00e6c264:
    plVar12 = local_160;
    if ((plVar7[3] == plVar7[4]) && (iVar5 = (**(code **)(*plVar7 + 0x48))(plVar7), iVar5 == -1))
    goto LAB_00e6c310;
    if (plVar12 != (long *)0x0) goto LAB_00e6c28c;
  }
  plVar7 = local_160;
  __shared_count::__release_shared();
  pcVar11 = local_170;
  local_170 = (char *)0x0;
  if (pcVar11 != (char *)0x0) {
                    /* try { // try from 00e6c2b4 to 00e6c2b7 has its CatchHandler @ 00e6c34c */
    (*local_168)();
  }
  if (*(long *)(lVar2 + 0x28) == local_70[0]) {
    return plVar7;
  }
LAB_00e6c32c:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get
// Address: 00e6d640
// ==========================================================================================

/* std::__ndk1::money_get<char, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> > >::do_get(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, bool, std::__ndk1::ios_base&, unsigned int&,
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&)
   const */

long * __thiscall
std::__ndk1::money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_get(money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      istreambuf_iterator param_1,istreambuf_iterator param_2,bool param_3,ios_base *param_4,
      uint *param_5,basic_string *param_6)

{
  long lVar1;
  undefined *puVar2;
  char cVar3;
  int iVar4;
  ulong uVar5;
  long *plVar6;
  char *pcVar7;
  char *pcVar8;
  char *pcVar9;
  long *plVar10;
  long local_120;
  char *local_118;
  char *local_110;
  code *local_108;
  long *local_100;
  undefined *local_f8;
  undefined *puStack_f0;
  undefined8 local_e8;
  undefined ***local_e0;
  undefined **local_d8;
  char local_cc [100];
  long local_68;
  
  plVar6 = (long *)(ulong)param_2;
  local_100 = (long *)(ulong)param_1;
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  local_110 = local_cc;
  local_108 = (code *)PTR___do_nothing_01ff56a8;
                    /* try { // try from 00e6d698 to 00e6d6a3 has its CatchHandler @ 00e6d8dc */
  ios_base::getloc();
  puVar2 = PTR_id_01ff5500;
  local_e8 = 0;
  local_f8 = PTR_id_01ff5500;
  puStack_f0 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_d8 = &local_f8;
    local_e0 = &local_d8;
                    /* try { // try from 00e6d6d8 to 00e6d6ef has its CatchHandler @ 00e6d8f0 */
    __call_once((ulong *)PTR_id_01ff5500,&local_e0,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_120 + 0x18) - *(long *)(local_120 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar10 = *(long **)(*(long *)(local_120 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar10 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6d8c8 to 00e6d8cb has its CatchHandler @ 00e6d8f0 */
    FUN_00de5da0();
  }
  local_f8 = (undefined *)((ulong)local_f8 & 0xffffffffffffff00);
                    /* try { // try from 00e6d71c to 00e6d79b has its CatchHandler @ 00e6d8ec */
  uVar5 = __do_get((istreambuf_iterator *)&local_100,param_2,param_3,(locale *)&local_120,
                   *(uint *)(param_4 + 8),param_5,(bool *)&local_f8,(ctype *)plVar10,
                   (unique_ptr *)&local_110,&local_118,(char *)&local_68);
  if ((uVar5 & 1) != 0) {
    if (((byte)*param_6 & 1) == 0) {
      *(undefined2 *)param_6 = 0;
    }
    else {
      **(undefined **)(param_6 + 0x10) = 0;
      *(undefined8 *)(param_6 + 8) = 0;
    }
    if ((char)local_f8 != '\0') {
      cVar3 = (**(code **)(*plVar10 + 0x38))(plVar10,0x2d);
      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::push_back
                ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
                 param_6,cVar3);
    }
                    /* try { // try from 00e6d7a4 to 00e6d7af has its CatchHandler @ 00e6d8d4 */
    cVar3 = (**(code **)(*plVar10 + 0x38))(plVar10,0x30);
    pcVar9 = local_118 + -1;
    pcVar8 = local_110;
    if (local_110 < pcVar9) {
      pcVar7 = local_110;
      if (pcVar9 <= local_110 + 1) {
        pcVar9 = local_110 + 1;
      }
      do {
        pcVar8 = pcVar7;
        if (*pcVar7 != cVar3) break;
        pcVar7 = pcVar7 + 1;
        pcVar8 = pcVar9;
      } while (pcVar9 != pcVar7);
    }
                    /* try { // try from 00e6d7e8 to 00e6d7f3 has its CatchHandler @ 00e6d8d0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    __append_forward_unsafe<char*>
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               param_6,pcVar8,local_118);
  }
                    /* try { // try from 00e6d810 to 00e6d843 has its CatchHandler @ 00e6d8ec */
  if (((local_100 == (long *)0x0) || (local_100[3] != local_100[4])) ||
     (iVar4 = (**(code **)(*local_100 + 0x48))(local_100), iVar4 != -1)) {
    plVar10 = local_100;
    if (plVar6 != (long *)0x0) goto LAB_00e6d828;
LAB_00e6d8c0:
    if (plVar10 != (long *)0x0) goto LAB_00e6d85c;
  }
  else {
    plVar10 = (long *)0x0;
    local_100 = (long *)0x0;
    if (plVar6 == (long *)0x0) goto LAB_00e6d8c0;
LAB_00e6d828:
    plVar10 = local_100;
    if ((plVar6[3] == plVar6[4]) && (iVar4 = (**(code **)(*plVar6 + 0x48))(plVar6), iVar4 == -1))
    goto LAB_00e6d8c0;
    if (plVar10 == (long *)0x0) goto LAB_00e6d85c;
  }
  *param_5 = *param_5 | 2;
LAB_00e6d85c:
  plVar6 = local_100;
  __shared_count::__release_shared();
  pcVar9 = local_110;
  local_110 = (char *)0x0;
  if (pcVar9 != (char *)0x0) {
                    /* try { // try from 00e6d878 to 00e6d87b has its CatchHandler @ 00e6d8d8 */
    (*local_108)();
  }
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return plVar6;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get
// Address: 00e6dc74
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::money_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, bool, std::__ndk1::ios_base&, unsigned int&, long double&)
   const */

long * __thiscall
std::__ndk1::
money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get(money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
       *this,istreambuf_iterator param_1,istreambuf_iterator param_2,bool param_3,ios_base *param_4,
      uint *param_5,longdouble *param_6)

{
  wchar_t wVar1;
  long lVar2;
  undefined *puVar3;
  wchar_t *pwVar4;
  bool bVar5;
  int iVar6;
  ulong uVar7;
  undefined **__ptr;
  long *plVar8;
  undefined8 *puVar9;
  undefined **ppuVar10;
  undefined **ppuVar11;
  wchar_t *pwVar12;
  long *plVar13;
  bool local_2cc [4];
  long local_2c8;
  wchar_t *local_2c0;
  wchar_t *local_2b8;
  code *local_2b0;
  long *local_2a8;
  undefined *local_2a0;
  undefined *puStack_298;
  undefined8 local_290;
  undefined local_238 [8];
  wchar_t local_230;
  wchar_t local_22c;
  wchar_t local_228;
  wchar_t local_224;
  wchar_t local_220;
  wchar_t local_21c;
  wchar_t local_218;
  wchar_t local_214;
  undefined local_210 [8];
  undefined auStack_208 [8];
  wchar_t local_200 [100];
  long local_70 [2];
  
  plVar8 = (long *)(ulong)param_2;
  local_2a8 = (long *)(ulong)param_1;
  lVar2 = tpidr_el0;
  local_70[0] = *(long *)(lVar2 + 0x28);
  local_2b8 = local_200;
  local_2b0 = (code *)PTR___do_nothing_01ff56a8;
                    /* try { // try from 00e6dccc to 00e6dcd7 has its CatchHandler @ 00e6e060 */
  ios_base::getloc();
  puVar3 = PTR_id_01ff5620;
  local_290 = 0;
  local_2a0 = PTR_id_01ff5620;
  puStack_298 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_238 = (undefined  [8])&local_2a0;
    local_210._0_7_ = SUB87(local_238,0);
    local_210[7] = (char)((ulong)local_238 >> 0x38);
                    /* try { // try from 00e6dd10 to 00e6dd27 has its CatchHandler @ 00e6e07c */
    __call_once((ulong *)PTR_id_01ff5620,local_210,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_2c8 + 0x18) - *(long *)(local_2c8 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar13 = *(long **)(*(long *)(local_2c8 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar13 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6e028 to 00e6e02b has its CatchHandler @ 00e6e07c */
    FUN_00de5da0();
  }
  local_2cc[0] = false;
                    /* try { // try from 00e6dd54 to 00e6dd83 has its CatchHandler @ 00e6e078 */
  uVar7 = __do_get((istreambuf_iterator *)&local_2a8,param_2,param_3,(locale *)&local_2c8,
                   *(uint *)(param_4 + 8),param_5,local_2cc,(ctype *)plVar13,
                   (unique_ptr *)&local_2b8,&local_2c0,(wchar_t *)local_70);
  if ((uVar7 & 1) != 0) {
    local_210._0_7_ = (undefined7)s_0123456789_005c474a._0_8_;
    local_210[7] = SUB81(s_0123456789_005c474a._0_8_,7);
    stack0xfffffffffffffdf7 = CONCAT31(0x3938,local_210[7]);
                    /* try { // try from 00e6ddb4 to 00e6ddc3 has its CatchHandler @ 00e6e058 */
    (**(code **)(*plVar13 + 0x60))(plVar13,local_210,(long)auStack_208 + 2,local_238);
    pwVar12 = local_2b8;
    pwVar4 = local_2c0;
    if ((long)local_2c0 - (long)local_2b8 < 0x189) {
      __ptr = (undefined **)0x0;
      ppuVar11 = &local_2a0;
joined_r0x00e6df50:
      ppuVar10 = ppuVar11;
      if (local_2cc[0] != false) {
        ppuVar10 = (undefined **)((long)ppuVar11 + 1);
        *(undefined *)ppuVar11 = 0x2d;
      }
      if (pwVar12 < pwVar4) {
        ppuVar11 = ppuVar10;
        do {
          wVar1 = *pwVar12;
          if (local_238._0_4_ == wVar1) {
            puVar9 = (undefined8 *)local_238;
          }
          else {
            puVar9 = (undefined8 *)((long)local_238 + 4);
            if ((((((local_238._4_4_ != wVar1) &&
                   (puVar9 = (undefined8 *)&local_230, local_230 != wVar1)) &&
                  (puVar9 = (undefined8 *)&local_22c, local_22c != wVar1)) &&
                 ((puVar9 = (undefined8 *)&local_228, local_228 != wVar1 &&
                  (puVar9 = (undefined8 *)&local_224, local_224 != wVar1)))) &&
                ((puVar9 = (undefined8 *)&local_220, local_220 != wVar1 &&
                 ((puVar9 = (undefined8 *)&local_21c, local_21c != wVar1 &&
                  (puVar9 = (undefined8 *)&local_218, local_218 != wVar1)))))) &&
               (puVar9 = (undefined8 *)&local_214, local_214 != wVar1)) {
              puVar9 = (undefined8 *)local_210;
            }
          }
          pwVar12 = pwVar12 + 1;
          ppuVar10 = (undefined **)((long)ppuVar11 + 1);
          *(undefined *)ppuVar11 =
               *(undefined *)((long)local_210 + ((long)puVar9 - (long)local_238 >> 2));
          ppuVar11 = ppuVar10;
        } while (pwVar12 < local_2c0);
      }
      *(undefined *)ppuVar10 = 0;
      iVar6 = sscanf((char *)&local_2a0,"%Lf",param_6);
      if (iVar6 == 1) {
        if (__ptr != (undefined **)0x0) {
          free(__ptr);
        }
        goto LAB_00e6df28;
      }
                    /* try { // try from 00e6e02c to 00e6e037 has its CatchHandler @ 00e6e044 */
      __throw_runtime_error("money_get error");
    }
    else {
      __ptr = (undefined **)malloc(((ulong)((long)local_2c0 - (long)local_2b8) >> 2) + 2);
      ppuVar11 = __ptr;
      if (__ptr != (undefined **)0x0) goto joined_r0x00e6df50;
    }
                    /* try { // try from 00e6e038 to 00e6e03b has its CatchHandler @ 00e6e040 */
    __throw_bad_alloc();
    goto LAB_00e6e03c;
  }
LAB_00e6df28:
  if (local_2a8 == (long *)0x0) {
LAB_00e6df88:
    bVar5 = true;
    if (plVar8 == (long *)0x0) goto LAB_00e6df7c;
LAB_00e6df90:
    if ((int *)plVar8[3] == (int *)plVar8[4]) {
      iVar6 = (**(code **)(*plVar8 + 0x48))(plVar8);
    }
    else {
      iVar6 = *(int *)plVar8[3];
    }
    if (bVar5 == (iVar6 == -1)) goto LAB_00e6dfc4;
  }
  else {
    if ((int *)local_2a8[3] == (int *)local_2a8[4]) {
                    /* try { // try from 00e6df60 to 00e6dfb3 has its CatchHandler @ 00e6e078 */
      iVar6 = (**(code **)(*local_2a8 + 0x48))();
    }
    else {
      iVar6 = *(int *)local_2a8[3];
    }
    if (iVar6 == -1) {
      local_2a8 = (long *)0x0;
      goto LAB_00e6df88;
    }
    bVar5 = local_2a8 == (long *)0x0;
    if (plVar8 != (long *)0x0) goto LAB_00e6df90;
LAB_00e6df7c:
    if (bVar5) {
LAB_00e6dfc4:
      *param_5 = *param_5 | 2;
    }
  }
  plVar8 = local_2a8;
  __shared_count::__release_shared();
  pwVar12 = local_2b8;
  local_2b8 = (wchar_t *)0x0;
  if (pwVar12 != (wchar_t *)0x0) {
                    /* try { // try from 00e6dfec to 00e6dfef has its CatchHandler @ 00e6e05c */
    (*local_2b0)();
  }
  if (*(long *)(lVar2 + 0x28) == local_70[0]) {
    return plVar8;
  }
LAB_00e6e03c:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_get
// Address: 00e6f3e0
// ==========================================================================================

/* std::__ndk1::money_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, bool, std::__ndk1::ios_base&, unsigned int&,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >&) const */

long * __thiscall
std::__ndk1::
money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_get(money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
       *this,istreambuf_iterator param_1,istreambuf_iterator param_2,bool param_3,ios_base *param_4,
      uint *param_5,basic_string *param_6)

{
  long lVar1;
  wchar_t *pwVar2;
  undefined *puVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  ulong uVar7;
  long *plVar8;
  long *plVar9;
  long local_248;
  wchar_t *local_240;
  wchar_t *local_238;
  code *local_230;
  long *local_228;
  undefined *local_220;
  undefined *puStack_218;
  undefined8 local_210;
  undefined ***local_208;
  undefined **local_200;
  wchar_t local_1f8 [100];
  long local_68;
  
  plVar8 = (long *)(ulong)param_2;
  local_228 = (long *)(ulong)param_1;
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  local_238 = local_1f8;
  local_230 = (code *)PTR___do_nothing_01ff56a8;
                    /* try { // try from 00e6f438 to 00e6f443 has its CatchHandler @ 00e6f688 */
  ios_base::getloc();
  puVar3 = PTR_id_01ff5620;
  local_210 = 0;
  local_220 = PTR_id_01ff5620;
  puStack_218 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_200 = &local_220;
    local_208 = &local_200;
                    /* try { // try from 00e6f478 to 00e6f48f has its CatchHandler @ 00e6f69c */
    __call_once((ulong *)PTR_id_01ff5620,&local_208,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_248 + 0x18) - *(long *)(local_248 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar9 = *(long **)(*(long *)(local_248 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar9 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6f674 to 00e6f677 has its CatchHandler @ 00e6f69c */
    FUN_00de5da0();
  }
  local_220 = (undefined *)((ulong)local_220 & 0xffffffffffffff00);
                    /* try { // try from 00e6f4bc to 00e6f53f has its CatchHandler @ 00e6f698 */
  uVar7 = __do_get((istreambuf_iterator *)&local_228,param_2,param_3,(locale *)&local_248,
                   *(uint *)(param_4 + 8),param_5,(bool *)&local_220,(ctype *)plVar9,
                   (unique_ptr *)&local_238,&local_240,(wchar_t *)&local_68);
  if ((uVar7 & 1) != 0) {
    if (((byte)*param_6 & 1) == 0) {
      *(undefined4 *)(param_6 + 4) = 0;
      *param_6 = (basic_string)0x0;
    }
    else {
      **(undefined4 **)(param_6 + 0x10) = 0;
      *(undefined8 *)(param_6 + 8) = 0;
    }
    if ((char)local_220 != '\0') {
      wVar5 = (**(code **)(*plVar9 + 0x58))(plVar9,0x2d);
      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
      push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                 *)param_6,wVar5);
    }
                    /* try { // try from 00e6f548 to 00e6f553 has its CatchHandler @ 00e6f680 */
    wVar5 = (**(code **)(*plVar9 + 0x58))(plVar9,0x30);
    for (pwVar2 = local_238; (pwVar2 < local_240 + -1 && (*pwVar2 == wVar5)); pwVar2 = pwVar2 + 1) {
    }
                    /* try { // try from 00e6f57c to 00e6f587 has its CatchHandler @ 00e6f67c */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
    __append_forward_unsafe<wchar_t*>
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)param_6,pwVar2,local_240);
  }
  if (local_228 == (long *)0x0) {
LAB_00e6f5d4:
    bVar4 = true;
    if (plVar8 == (long *)0x0) goto LAB_00e6f5c8;
LAB_00e6f5dc:
    if ((int *)plVar8[3] == (int *)plVar8[4]) {
      iVar6 = (**(code **)(*plVar8 + 0x48))(plVar8);
    }
    else {
      iVar6 = *(int *)plVar8[3];
    }
    if (bVar4 != (iVar6 == -1)) goto LAB_00e6f61c;
  }
  else {
    if ((int *)local_228[3] == (int *)local_228[4]) {
                    /* try { // try from 00e6f5ac to 00e6f5ff has its CatchHandler @ 00e6f698 */
      iVar6 = (**(code **)(*local_228 + 0x48))();
    }
    else {
      iVar6 = *(int *)local_228[3];
    }
    if (iVar6 == -1) {
      local_228 = (long *)0x0;
      goto LAB_00e6f5d4;
    }
    bVar4 = local_228 == (long *)0x0;
    if (plVar8 != (long *)0x0) goto LAB_00e6f5dc;
LAB_00e6f5c8:
    if (!bVar4) goto LAB_00e6f61c;
  }
  *param_5 = *param_5 | 2;
LAB_00e6f61c:
  plVar8 = local_228;
  __shared_count::__release_shared();
  pwVar2 = local_238;
  local_238 = (wchar_t *)0x0;
  if (pwVar2 != (wchar_t *)0x0) {
                    /* try { // try from 00e6f638 to 00e6f63b has its CatchHandler @ 00e6f684 */
    (*local_230)();
  }
  if (*(long *)(lVar1 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return plVar8;
}



// ==========================================================================================
// Function: do_put
// Address: 00e6f928
// ==========================================================================================

/* std::__ndk1::money_put<char, std::__ndk1::ostreambuf_iterator<char,
   std::__ndk1::char_traits<char> > >::do_put(std::__ndk1::ostreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, bool, std::__ndk1::ios_base&, char, long double) const */

undefined8 __thiscall
std::__ndk1::money_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(money_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,bool param_2,ios_base *param_3,char param_4,longdouble param_5)

{
  size_t __size;
  long lVar1;
  undefined *puVar2;
  bool bVar3;
  uint uVar4;
  int iVar5;
  char *__ptr;
  undefined **__ptr_00;
  undefined8 uVar6;
  ulong uVar7;
  ulong uVar8;
  long lVar9;
  char *__ptr_01;
  char *pcVar10;
  size_t __size_00;
  undefined **ppuVar11;
  long *plVar12;
  char *local_220;
  char *pcStack_218;
  int local_20c;
  ulong local_208;
  ulong local_200;
  void *local_1f8;
  undefined ***local_1f0;
  ulong local_1e8;
  void *local_1e0;
  undefined **local_1d8;
  undefined8 uStack_1d0;
  void *local_1c8;
  char local_1c0 [4];
  char local_1bc [4];
  long local_1b8;
  char *local_1b0;
  pattern apStack_1a8 [8];
  undefined *local_1a0;
  undefined *puStack_198;
  undefined8 local_190;
  char acStack_138 [100];
  char local_d4 [100];
  long local_70;
  
  lVar1 = tpidr_el0;
  local_70 = *(long *)(lVar1 + 0x28);
  local_1b0 = local_d4;
  uVar4 = FUN_00e6fdcc(local_d4,100);
  if (99 < uVar4) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_0231cfb0), iVar5 != 0)) {
                    /* try { // try from 00e6fcb0 to 00e6fcc3 has its CatchHandler @ 00e6fce4 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
                    /* try { // try from 00e6f9a0 to 00e6f9b7 has its CatchHandler @ 00e6fd38 */
    iVar5 = __libcpp_asprintf_l(&local_1b0,(__locale_t *)DAT_0231cfa8,"%.0Lf",param_5);
    __ptr_01 = local_1b0;
    if (local_1b0 == (char *)0x0) {
                    /* try { // try from 00e6fcd8 to 00e6fcdf has its CatchHandler @ 00e6fd38 */
      __throw_bad_alloc();
    }
    else {
      __size_00 = (size_t)iVar5;
      __ptr = (char *)malloc(__size_00);
      pcVar10 = __ptr;
      if (__ptr != (char *)0x0) goto LAB_00e6f9ec;
    }
    __throw_bad_alloc();
    goto LAB_00e6fce0;
  }
  __ptr = (char *)0x0;
  __ptr_01 = (char *)0x0;
  __size_00 = (size_t)(int)uVar4;
  pcVar10 = acStack_138;
LAB_00e6f9ec:
                    /* try { // try from 00e6f9ec to 00e6fa03 has its CatchHandler @ 00e6fd30 */
  ios_base::getloc();
  puVar2 = PTR_id_01ff5500;
  local_190 = 0;
  local_1a0 = PTR_id_01ff5500;
  puStack_198 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_1d8 = &local_1a0;
    local_1f0 = &local_1d8;
                    /* try { // try from 00e6fa3c to 00e6fa8f has its CatchHandler @ 00e6fd8c */
    __call_once((ulong *)PTR_id_01ff5500,&local_1f0,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_1b8 + 0x18) - *(long *)(local_1b8 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar12 = *(long **)(*(long *)(local_1b8 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar12 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e6fc9c to 00e6fc9f has its CatchHandler @ 00e6fd8c */
    FUN_00de5da0();
  }
  (**(code **)(*plVar12 + 0x40))(plVar12,local_1b0,local_1b0 + __size_00,pcVar10);
  if (__size_00 == 0) {
    bVar3 = false;
  }
  else {
    bVar3 = *local_1b0 == '-';
  }
  local_1d8 = (undefined **)0x0;
  uStack_1d0 = 0;
  local_1c8 = (void *)0x0;
  local_1f0 = (undefined ***)0x0;
  local_1e8 = 0;
  local_1e0 = (void *)0x0;
  local_208 = 0;
  local_200 = 0;
  local_1f8 = (void *)0x0;
                    /* try { // try from 00e6fac8 to 00e6faf7 has its CatchHandler @ 00e6fd00 */
  __money_put<char>::__gather_info
            (param_2,bVar3,(locale *)&local_1b8,apStack_1a8,local_1bc,local_1c0,
             (basic_string *)&local_1d8,(basic_string *)&local_1f0,(basic_string *)&local_208,
             &local_20c);
  if (local_20c < (int)__size_00) {
    uVar7 = (ulong)((byte)local_208 >> 1);
    if ((local_208 & 1) != 0) {
      uVar7 = local_200;
    }
    uVar8 = (ulong)((byte)local_1f0 >> 1);
    if (((ulong)local_1f0 & 1) != 0) {
      uVar8 = local_1e8;
    }
    lVar9 = (__size_00 * 2 - (long)local_20c) + 1;
  }
  else {
    uVar7 = (ulong)((byte)local_208 >> 1);
    if ((local_208 & 1) != 0) {
      uVar7 = local_200;
    }
    uVar8 = (ulong)((byte)local_1f0 >> 1);
    if (((ulong)local_1f0 & 1) != 0) {
      uVar8 = local_1e8;
    }
    lVar9 = (long)local_20c + 2;
  }
  __size = lVar9 + uVar7 + uVar8;
  if (__size < 0x65) {
LAB_00e6fb8c:
    __ptr_00 = (undefined **)0x0;
    ppuVar11 = &local_1a0;
  }
  else {
    __ptr_00 = (undefined **)malloc(__size);
    ppuVar11 = __ptr_00;
    if (__ptr_00 == (undefined **)0x0) {
                    /* try { // try from 00e6fb88 to 00e6fb8b has its CatchHandler @ 00e6fcfc */
      __throw_bad_alloc();
      goto LAB_00e6fb8c;
    }
  }
                    /* try { // try from 00e6fba4 to 00e6fbff has its CatchHandler @ 00e6fd4c */
  __money_put<char>::__format
            ((char *)ppuVar11,&pcStack_218,&local_220,*(uint *)(param_3 + 8),pcVar10,
             pcVar10 + __size_00,(ctype *)plVar12,bVar3,apStack_1a8,local_1bc[0],local_1c0[0],
             (basic_string *)&local_1d8,(basic_string *)&local_1f0,(basic_string *)&local_208,
             local_20c);
  uVar6 = FUN_00de61dc(param_1,ppuVar11,pcStack_218,local_220,param_3,param_4);
  if (__ptr_00 != (undefined **)0x0) {
    free(__ptr_00);
  }
  if ((local_208 & 1) != 0) {
    operator_delete(local_1f8);
  }
  if (((ulong)local_1f0 & 1) != 0) {
    operator_delete(local_1e0);
  }
  if (((ulong)local_1d8 & 1) != 0) {
    operator_delete(local_1c8);
  }
  __shared_count::__release_shared();
  if (__ptr != (char *)0x0) {
    free(__ptr);
  }
  if (__ptr_01 != (char *)0x0) {
    free(__ptr_01);
  }
  if (*(long *)(lVar1 + 0x28) == local_70) {
    return uVar6;
  }
LAB_00e6fce0:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e705bc
// ==========================================================================================

/* std::__ndk1::money_put<char, std::__ndk1::ostreambuf_iterator<char,
   std::__ndk1::char_traits<char> > >::do_put(std::__ndk1::ostreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, bool, std::__ndk1::ios_base&, char,
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >
   const&) const */

undefined8 __thiscall
std::__ndk1::money_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
do_put(money_put<char,std::__ndk1::ostreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this,
      ostreambuf_iterator param_1,bool param_2,ios_base *param_3,char param_4,basic_string *param_5)

{
  size_t __size;
  basic_string bVar1;
  long lVar2;
  undefined *puVar3;
  bool bVar4;
  basic_string bVar5;
  undefined **__ptr;
  undefined8 uVar6;
  ulong uVar7;
  ulong uVar8;
  basic_string *pbVar9;
  ulong uVar10;
  long lVar11;
  long *plVar12;
  undefined **ppuVar13;
  char *local_150;
  char *pcStack_148;
  int local_13c;
  ulong local_138;
  ulong local_130;
  void *local_128;
  undefined ***local_120;
  ulong local_118;
  void *local_110;
  undefined **local_108;
  undefined8 uStack_100;
  void *local_f8;
  char local_f0 [4];
  char local_ec [4];
  long local_e8;
  pattern apStack_e0 [8];
  undefined *local_d8;
  undefined *puStack_d0;
  undefined8 local_c8;
  long local_70;
  
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  ios_base::getloc();
  puVar3 = PTR_id_01ff5500;
  local_c8 = 0;
  local_d8 = PTR_id_01ff5500;
  puStack_d0 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_108 = &local_d8;
    local_120 = &local_108;
                    /* try { // try from 00e70644 to 00e7065b has its CatchHandler @ 00e70970 */
    __call_once((ulong *)PTR_id_01ff5500,&local_120,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_e8 + 0x18) - *(long *)(local_e8 + 0x10) >> 3) <=
       (long)*(int *)(puVar3 + 8) - 1U) ||
     (plVar12 = *(long **)(*(long *)(local_e8 + 0x10) + ((long)*(int *)(puVar3 + 8) - 1U) * 8),
     plVar12 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e708f0 to 00e708f3 has its CatchHandler @ 00e70970 */
    FUN_00de5da0();
  }
  if (((byte)*param_5 & 1) == 0) {
    if ((byte)*param_5 < 2) goto LAB_00e706c4;
    pbVar9 = param_5 + 1;
LAB_00e706a0:
    bVar1 = *pbVar9;
                    /* try { // try from 00e706ac to 00e706b7 has its CatchHandler @ 00e708fc */
    bVar5 = (basic_string)(**(code **)(*plVar12 + 0x38))(plVar12,0x2d);
    bVar4 = bVar1 == bVar5;
  }
  else {
    if (*(long *)(param_5 + 8) != 0) {
      pbVar9 = *(basic_string **)(param_5 + 0x10);
      goto LAB_00e706a0;
    }
LAB_00e706c4:
    bVar4 = false;
  }
  local_108 = (undefined **)0x0;
  uStack_100 = 0;
  local_f8 = (void *)0x0;
  local_120 = (undefined ***)0x0;
  local_118 = 0;
  local_110 = (void *)0x0;
  local_138 = 0;
  local_130 = 0;
  local_128 = (void *)0x0;
                    /* try { // try from 00e706e0 to 00e7070f has its CatchHandler @ 00e70900 */
  __money_put<char>::__gather_info
            (param_2,bVar4,(locale *)&local_e8,apStack_e0,local_ec,local_f0,
             (basic_string *)&local_108,(basic_string *)&local_120,(basic_string *)&local_138,
             &local_13c);
  bVar1 = *param_5;
  if (((byte)bVar1 & 1) == 0) {
    uVar7 = (ulong)((byte)bVar1 >> 1);
  }
  else {
    uVar7 = *(ulong *)(param_5 + 8);
  }
  if (local_13c < (int)uVar7) {
    uVar8 = (ulong)((byte)local_138 >> 1);
    if ((local_138 & 1) != 0) {
      uVar8 = local_130;
    }
    uVar10 = (ulong)((byte)local_120 >> 1);
    if (((ulong)local_120 & 1) != 0) {
      uVar10 = local_118;
    }
    lVar11 = (uVar7 * 2 - (long)local_13c) + 1;
  }
  else {
    uVar8 = (ulong)((byte)local_138 >> 1);
    if ((local_138 & 1) != 0) {
      uVar8 = local_130;
    }
    uVar10 = (ulong)((byte)local_120 >> 1);
    if (((ulong)local_120 & 1) != 0) {
      uVar10 = local_118;
    }
    lVar11 = (long)local_13c + 2;
  }
  __size = lVar11 + uVar8 + uVar10;
  if (100 < __size) {
    __ptr = (undefined **)malloc(__size);
    ppuVar13 = __ptr;
    if (__ptr != (undefined **)0x0) goto LAB_00e707dc;
                    /* try { // try from 00e707d0 to 00e707d3 has its CatchHandler @ 00e708f8 */
    __throw_bad_alloc();
  }
  __ptr = (undefined **)0x0;
  ppuVar13 = &local_d8;
LAB_00e707dc:
  uVar7 = *(ulong *)(param_5 + 8);
  pbVar9 = *(basic_string **)(param_5 + 0x10);
  if (((byte)bVar1 & 1) == 0) {
    pbVar9 = param_5 + 1;
    uVar7 = (ulong)((byte)bVar1 >> 1);
  }
                    /* try { // try from 00e70800 to 00e70857 has its CatchHandler @ 00e70930 */
  __money_put<char>::__format
            ((char *)ppuVar13,&pcStack_148,&local_150,*(uint *)(param_3 + 8),(char *)pbVar9,
             (char *)(pbVar9 + uVar7),(ctype *)plVar12,bVar4,apStack_e0,local_ec[0],local_f0[0],
             (basic_string *)&local_108,(basic_string *)&local_120,(basic_string *)&local_138,
             local_13c);
  uVar6 = FUN_00de61dc(param_1,ppuVar13,pcStack_148,local_150,param_3,param_4);
  if (__ptr != (undefined **)0x0) {
    free(__ptr);
  }
  if ((local_138 & 1) != 0) {
    operator_delete(local_128);
  }
  if (((ulong)local_120 & 1) != 0) {
    operator_delete(local_110);
  }
  if (((ulong)local_108 & 1) != 0) {
    operator_delete(local_f8);
  }
  __shared_count::__release_shared();
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar6;
}



// ==========================================================================================
// Function: do_put
// Address: 00e70984
// ==========================================================================================

/* std::__ndk1::money_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, bool, std::__ndk1::ios_base&, wchar_t, long double) const */

undefined8 __thiscall
std::__ndk1::
money_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_put(money_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
       *this,ostreambuf_iterator param_1,bool param_2,ios_base *param_3,wchar_t param_4,
      longdouble param_5)

{
  long lVar1;
  undefined *puVar2;
  bool bVar3;
  uint uVar4;
  int iVar5;
  wchar_t *pwVar6;
  undefined **__ptr;
  undefined8 uVar7;
  ulong uVar8;
  ulong uVar9;
  long lVar10;
  char *__ptr_00;
  long lVar11;
  long *plVar12;
  wchar_t *__ptr_01;
  undefined **ppuVar13;
  wchar_t *local_478;
  wchar_t *pwStack_470;
  int local_464;
  ulong local_460;
  ulong local_458;
  void *local_450;
  undefined ***local_448;
  ulong local_440;
  void *local_438;
  undefined **local_430;
  undefined8 uStack_428;
  void *local_420;
  wchar_t local_418;
  wchar_t wStack_414;
  long local_410;
  char *local_408;
  pattern apStack_400 [8];
  undefined *local_3f8;
  undefined *puStack_3f0;
  undefined8 local_3e8;
  wchar_t awStack_264 [100];
  char local_d4 [100];
  long local_70;
  
  lVar1 = tpidr_el0;
  local_70 = *(long *)(lVar1 + 0x28);
  local_408 = local_d4;
  uVar4 = FUN_00e6fdcc(local_d4,100,param_2,param_3,param_4);
  if (99 < uVar4) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_0231cfb0), iVar5 != 0)) {
                    /* try { // try from 00e70d1c to 00e70d2f has its CatchHandler @ 00e70d50 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
                    /* try { // try from 00e709fc to 00e70a13 has its CatchHandler @ 00e70da4 */
    iVar5 = __libcpp_asprintf_l(&local_408,(__locale_t *)DAT_0231cfa8,"%.0Lf",param_5);
    __ptr_00 = local_408;
    if (local_408 == (char *)0x0) {
                    /* try { // try from 00e70d44 to 00e70d4b has its CatchHandler @ 00e70da4 */
      __throw_bad_alloc();
    }
    else {
      lVar11 = (long)iVar5;
      pwVar6 = (wchar_t *)malloc(lVar11 << 2);
      __ptr_01 = pwVar6;
      if (pwVar6 != (wchar_t *)0x0) goto LAB_00e70a48;
    }
    __throw_bad_alloc();
    goto LAB_00e70d4c;
  }
  __ptr_00 = (char *)0x0;
  pwVar6 = awStack_264;
  lVar11 = (long)(int)uVar4;
  __ptr_01 = (wchar_t *)0x0;
LAB_00e70a48:
                    /* try { // try from 00e70a48 to 00e70a5b has its CatchHandler @ 00e70d9c */
  ios_base::getloc();
  puVar2 = PTR_id_01ff5620;
  local_3e8 = 0;
  local_3f8 = PTR_id_01ff5620;
  puStack_3f0 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_430 = &local_3f8;
    local_448 = &local_430;
                    /* try { // try from 00e70a94 to 00e70ae7 has its CatchHandler @ 00e70df8 */
    __call_once((ulong *)PTR_id_01ff5620,&local_448,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_410 + 0x18) - *(long *)(local_410 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar12 = *(long **)(*(long *)(local_410 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar12 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e70d08 to 00e70d0b has its CatchHandler @ 00e70df8 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar12 + 0x60))(plVar12,local_408,local_408 + lVar11,pwVar6);
  if (lVar11 == 0) {
    bVar3 = false;
  }
  else {
    bVar3 = *local_408 == '-';
  }
  local_430 = (undefined **)0x0;
  uStack_428 = 0;
  local_420 = (void *)0x0;
  local_448 = (undefined ***)0x0;
  local_440 = 0;
  local_438 = (void *)0x0;
  local_460 = 0;
  local_458 = 0;
  local_450 = (void *)0x0;
                    /* try { // try from 00e70b1c to 00e70b4b has its CatchHandler @ 00e70d6c */
  __money_put<wchar_t>::__gather_info
            (param_2,bVar3,(locale *)&local_410,apStack_400,&wStack_414,&local_418,
             (basic_string *)&local_430,(basic_string *)&local_448,(basic_string *)&local_460,
             &local_464);
  if (local_464 < (int)lVar11) {
    uVar8 = (ulong)((byte)local_460 >> 1);
    if ((local_460 & 1) != 0) {
      uVar8 = local_458;
    }
    uVar9 = (ulong)((byte)local_448 >> 1);
    if (((ulong)local_448 & 1) != 0) {
      uVar9 = local_440;
    }
    lVar10 = (lVar11 * 2 - (long)local_464) + 1;
  }
  else {
    uVar8 = (ulong)((byte)local_460 >> 1);
    if ((local_460 & 1) != 0) {
      uVar8 = local_458;
    }
    uVar9 = (ulong)((byte)local_448 >> 1);
    if (((ulong)local_448 & 1) != 0) {
      uVar9 = local_440;
    }
    lVar10 = (long)local_464 + 2;
  }
  uVar9 = lVar10 + uVar8 + uVar9;
  if (uVar9 < 0x65) {
LAB_00e70be8:
    __ptr = (undefined **)0x0;
    ppuVar13 = &local_3f8;
  }
  else {
    __ptr = (undefined **)malloc(uVar9 * 4);
    ppuVar13 = __ptr;
    if (__ptr == (undefined **)0x0) {
                    /* try { // try from 00e70be4 to 00e70be7 has its CatchHandler @ 00e70d68 */
      __throw_bad_alloc();
      goto LAB_00e70be8;
    }
  }
                    /* try { // try from 00e70bfc to 00e70c57 has its CatchHandler @ 00e70db8 */
  __money_put<wchar_t>::__format
            ((wchar_t *)ppuVar13,&pwStack_470,&local_478,*(uint *)(param_3 + 8),pwVar6,
             pwVar6 + lVar11,(ctype *)plVar12,bVar3,apStack_400,wStack_414,local_418,
             (basic_string *)&local_430,(basic_string *)&local_448,(basic_string *)&local_460,
             local_464);
  uVar7 = FUN_00e65b40(param_1,ppuVar13,pwStack_470,local_478,param_3,param_4);
  if (__ptr != (undefined **)0x0) {
    free(__ptr);
  }
  if ((local_460 & 1) != 0) {
    operator_delete(local_450);
  }
  if (((ulong)local_448 & 1) != 0) {
    operator_delete(local_438);
  }
  if (((ulong)local_430 & 1) != 0) {
    operator_delete(local_420);
  }
  __shared_count::__release_shared();
  if (__ptr_01 != (wchar_t *)0x0) {
    free(__ptr_01);
  }
  if (__ptr_00 != (char *)0x0) {
    free(__ptr_00);
  }
  if (*(long *)(lVar1 + 0x28) == local_70) {
    return uVar7;
  }
LAB_00e70d4c:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_put
// Address: 00e7156c
// ==========================================================================================

/* std::__ndk1::money_put<wchar_t, std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::do_put(std::__ndk1::ostreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, bool, std::__ndk1::ios_base&, wchar_t,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> > const&) const */

undefined8 __thiscall
std::__ndk1::
money_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
do_put(money_put<wchar_t,std::__ndk1::ostreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
       *this,ostreambuf_iterator param_1,bool param_2,ios_base *param_3,wchar_t param_4,
      basic_string *param_5)

{
  int iVar1;
  basic_string bVar2;
  long lVar3;
  wchar_t *pwVar4;
  undefined *puVar5;
  bool bVar6;
  int iVar7;
  undefined **__ptr;
  undefined8 uVar8;
  int *piVar9;
  ulong uVar10;
  ulong uVar11;
  ulong uVar12;
  long lVar13;
  long *plVar14;
  undefined **ppuVar15;
  wchar_t *local_278;
  wchar_t *pwStack_270;
  int local_264;
  ulong local_260;
  ulong local_258;
  void *local_250;
  undefined ***local_248;
  ulong local_240;
  void *local_238;
  undefined **local_230;
  undefined8 uStack_228;
  void *local_220;
  wchar_t local_218;
  wchar_t wStack_214;
  long local_210;
  pattern apStack_208 [8];
  undefined *local_200;
  undefined *puStack_1f8;
  undefined8 local_1f0;
  long local_70;
  
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  ios_base::getloc();
  puVar5 = PTR_id_01ff5620;
  local_1f0 = 0;
  local_200 = PTR_id_01ff5620;
  puStack_1f8 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_230 = &local_200;
    local_248 = &local_230;
                    /* try { // try from 00e715f4 to 00e7160b has its CatchHandler @ 00e71924 */
    __call_once((ulong *)PTR_id_01ff5620,&local_248,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_210 + 0x18) - *(long *)(local_210 + 0x10) >> 3) <=
       (long)*(int *)(puVar5 + 8) - 1U) ||
     (plVar14 = *(long **)(*(long *)(local_210 + 0x10) + ((long)*(int *)(puVar5 + 8) - 1U) * 8),
     plVar14 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e718a4 to 00e718a7 has its CatchHandler @ 00e71924 */
    FUN_00de5da0();
  }
  if (((byte)*param_5 & 1) == 0) {
    if ((byte)*param_5 < 2) goto LAB_00e71674;
    piVar9 = (int *)(param_5 + 4);
LAB_00e71650:
    iVar1 = *piVar9;
                    /* try { // try from 00e7165c to 00e71667 has its CatchHandler @ 00e718b0 */
    iVar7 = (**(code **)(*plVar14 + 0x58))(plVar14,0x2d);
    bVar6 = iVar1 == iVar7;
  }
  else {
    if (*(long *)(param_5 + 8) != 0) {
      piVar9 = *(int **)(param_5 + 0x10);
      goto LAB_00e71650;
    }
LAB_00e71674:
    bVar6 = false;
  }
  local_230 = (undefined **)0x0;
  uStack_228 = 0;
  local_220 = (void *)0x0;
  local_248 = (undefined ***)0x0;
  local_240 = 0;
  local_238 = (void *)0x0;
  local_260 = 0;
  local_258 = 0;
  local_250 = (void *)0x0;
                    /* try { // try from 00e71690 to 00e716bf has its CatchHandler @ 00e718b4 */
  __money_put<wchar_t>::__gather_info
            (param_2,bVar6,(locale *)&local_210,apStack_208,&wStack_214,&local_218,
             (basic_string *)&local_230,(basic_string *)&local_248,(basic_string *)&local_260,
             &local_264);
  bVar2 = *param_5;
  if (((byte)bVar2 & 1) == 0) {
    uVar10 = (ulong)((byte)bVar2 >> 1);
  }
  else {
    uVar10 = *(ulong *)(param_5 + 8);
  }
  if (local_264 < (int)uVar10) {
    uVar11 = (ulong)((byte)local_260 >> 1);
    if ((local_260 & 1) != 0) {
      uVar11 = local_258;
    }
    uVar12 = (ulong)((byte)local_248 >> 1);
    if (((ulong)local_248 & 1) != 0) {
      uVar12 = local_240;
    }
    lVar13 = (uVar10 * 2 - (long)local_264) + 1;
  }
  else {
    uVar11 = (ulong)((byte)local_260 >> 1);
    if ((local_260 & 1) != 0) {
      uVar11 = local_258;
    }
    uVar12 = (ulong)((byte)local_248 >> 1);
    if (((ulong)local_248 & 1) != 0) {
      uVar12 = local_240;
    }
    lVar13 = (long)local_264 + 2;
  }
  uVar12 = lVar13 + uVar11 + uVar12;
  if (100 < uVar12) {
    __ptr = (undefined **)malloc(uVar12 * 4);
    ppuVar15 = __ptr;
    if (__ptr != (undefined **)0x0) goto LAB_00e71790;
                    /* try { // try from 00e71784 to 00e71787 has its CatchHandler @ 00e718ac */
    __throw_bad_alloc();
  }
  __ptr = (undefined **)0x0;
  ppuVar15 = &local_200;
LAB_00e71790:
  uVar10 = (ulong)((byte)bVar2 >> 1);
  pwVar4 = (wchar_t *)(param_5 + 4);
  if (((byte)bVar2 & 1) != 0) {
    uVar10 = *(ulong *)(param_5 + 8);
    pwVar4 = *(wchar_t **)(param_5 + 0x10);
  }
                    /* try { // try from 00e717b4 to 00e7180b has its CatchHandler @ 00e718e4 */
  __money_put<wchar_t>::__format
            ((wchar_t *)ppuVar15,&pwStack_270,&local_278,*(uint *)(param_3 + 8),pwVar4,
             pwVar4 + uVar10,(ctype *)plVar14,bVar6,apStack_208,wStack_214,local_218,
             (basic_string *)&local_230,(basic_string *)&local_248,(basic_string *)&local_260,
             local_264);
  uVar8 = FUN_00e65b40(param_1,ppuVar15,pwStack_270,local_278,param_3,param_4);
  if (__ptr != (undefined **)0x0) {
    free(__ptr);
  }
  if ((local_260 & 1) != 0) {
    operator_delete(local_250);
  }
  if (((ulong)local_248 & 1) != 0) {
    operator_delete(local_238);
  }
  if (((ulong)local_230 & 1) != 0) {
    operator_delete(local_220);
  }
  __shared_count::__release_shared();
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar8;
}



// ==========================================================================================
// Function: do_open
// Address: 00e71938
// ==========================================================================================

/* std::__ndk1::messages<char>::do_open(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, std::__ndk1::locale
   const&) const */

undefined8 std::__ndk1::messages<char>::do_open(basic_string *param_1,locale *param_2)

{
  return 0xffffffffffffffff;
}



// ==========================================================================================
// Function: do_get
// Address: 00e71944
// ==========================================================================================

/* std::__ndk1::messages<char>::do_get(long, int, int, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&) const */

void std::__ndk1::messages<char>::do_get(long param_1,int param_2,int param_3,basic_string *param_4)

{
  basic_string *in_x4;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,in_x4);
  return;
}



// ==========================================================================================
// Function: do_close
// Address: 00e71954
// ==========================================================================================

/* std::__ndk1::messages<char>::do_close(long) const */

void std::__ndk1::messages<char>::do_close(long param_1)

{
  return;
}



// ==========================================================================================
// Function: do_open
// Address: 00e7195c
// ==========================================================================================

/* std::__ndk1::messages<wchar_t>::do_open(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, std::__ndk1::locale
   const&) const */

undefined8 std::__ndk1::messages<wchar_t>::do_open(basic_string *param_1,locale *param_2)

{
  return 0xffffffffffffffff;
}



// ==========================================================================================
// Function: do_get
// Address: 00e71968
// ==========================================================================================

/* std::__ndk1::messages<wchar_t>::do_get(long, int, int, std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> > const&) const */

void std::__ndk1::messages<wchar_t>::do_get
               (long param_1,int param_2,int param_3,basic_string *param_4)

{
  basic_string *in_x4;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string(in_x8,in_x4);
  return;
}



// ==========================================================================================
// Function: do_close
// Address: 00e71978
// ==========================================================================================

/* std::__ndk1::messages<wchar_t>::do_close(long) const */

void std::__ndk1::messages<wchar_t>::do_close(long param_1)

{
  return;
}



// ==========================================================================================
// Function: do_compare
// Address: 00e78814
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::do_compare(char const*, char const*, char const*, char const*)
   const */

void __thiscall
std::__ndk1::collate_byname<char>::do_compare
          (collate_byname<char> *this,char *param_1,char *param_2,char *param_3,char *param_4)

{
  char *__s2;
  long lVar1;
  char *pcVar2;
  char *pcVar3;
  int iVar4;
  uint uVar5;
  ulong uVar6;
  ulong uVar7;
  char *pcVar8;
  undefined8 local_98;
  ulong local_90;
  char *local_88;
  undefined8 local_80;
  ulong local_78;
  char *local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  uVar6 = (long)param_2 - (long)param_1;
  if (0xffffffffffffffef < uVar6) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar6 < 0x17) {
    local_80 = CONCAT71(local_80._1_7_,(char)((int)uVar6 << 1));
    pcVar8 = (char *)((ulong)&local_80 | 1);
  }
  else {
    uVar7 = uVar6 + 0x10 & 0xfffffffffffffff0;
    pcVar8 = (char *)operator_new(uVar7);
    local_80 = uVar7 | 1;
    local_78 = uVar6;
    local_70 = pcVar8;
  }
  if (param_1 != param_2) {
    memcpy(pcVar8,param_1,uVar6);
    pcVar8 = pcVar8 + uVar6;
  }
  uVar6 = (long)param_4 - (long)param_3;
  *pcVar8 = '\0';
  if (uVar6 < 0xfffffffffffffff0) {
    if (uVar6 < 0x17) {
      local_98 = CONCAT71(local_98._1_7_,(char)((int)uVar6 << 1));
      pcVar8 = (char *)((ulong)&local_98 | 1);
    }
    else {
      uVar7 = uVar6 + 0x10 & 0xfffffffffffffff0;
                    /* try { // try from 00e789a8 to 00e789af has its CatchHandler @ 00e789e0 */
      pcVar8 = (char *)operator_new(uVar7);
      local_98 = uVar7 | 1;
      local_90 = uVar6;
      local_88 = pcVar8;
    }
    if (param_3 != param_4) {
      memcpy(pcVar8,param_3,uVar6);
      pcVar8 = pcVar8 + uVar6;
    }
    pcVar3 = local_70;
    uVar7 = local_80;
    pcVar2 = local_88;
    uVar6 = local_98;
    *pcVar8 = '\0';
    pcVar8 = (char *)((ulong)&local_80 | 1);
    if ((local_80 & 1) != 0) {
      pcVar8 = local_70;
    }
    __s2 = (char *)((ulong)&local_98 | 1);
    if ((local_98 & 1) != 0) {
      __s2 = local_88;
    }
    iVar4 = strcoll_l(pcVar8,__s2,*(__locale_t *)(this + 0x10));
    if ((uVar6 & 1) != 0) {
      operator_delete(pcVar2);
    }
    if ((uVar7 & 1) != 0) {
      operator_delete(pcVar3);
    }
    uVar5 = (uint)(iVar4 != 0);
    if (iVar4 < 0) {
      uVar5 = 0xffffffff;
    }
    if (*(long *)(lVar1 + 0x28) == local_68) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar5);
  }
                    /* try { // try from 00e789d4 to 00e789db has its CatchHandler @ 00e789e0 */
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: do_transform
// Address: 00e789fc
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::do_transform(char const*, char const*) const */

void std::__ndk1::collate_byname<char>::do_transform(char *param_1,char *param_2)

{
  long lVar1;
  size_t __n;
  char *in_x2;
  ulong *in_x8;
  ulong uVar2;
  byte *pbVar3;
  char *pcVar4;
  ulong uVar5;
  undefined8 local_70;
  ulong local_68;
  char *local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  uVar2 = (long)in_x2 - (long)param_2;
  if (0xffffffffffffffef < uVar2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (uVar2 < 0x17) {
    local_70 = CONCAT71(local_70._1_7_,(char)((int)uVar2 << 1));
    pcVar4 = (char *)((ulong)&local_70 | 1);
  }
  else {
    uVar5 = uVar2 + 0x10 & 0xfffffffffffffff0;
    pcVar4 = (char *)operator_new(uVar5);
    local_70 = uVar5 | 1;
    local_68 = uVar2;
    local_60 = pcVar4;
  }
  if (param_2 != in_x2) {
    memcpy(pcVar4,param_2,uVar2);
    pcVar4 = pcVar4 + uVar2;
  }
  *pcVar4 = '\0';
  pcVar4 = (char *)((ulong)&local_70 | 1);
  if ((local_70 & 1) != 0) {
    pcVar4 = local_60;
  }
                    /* try { // try from 00e78ac4 to 00e78b07 has its CatchHandler @ 00e78be4 */
  __n = strxfrm_l((char *)0x0,pcVar4,0,*(__locale_t *)(param_1 + 0x10));
  if (0xffffffffffffffef < __n) {
                    /* try { // try from 00e78ba8 to 00e78baf has its CatchHandler @ 00e78be4 */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    pbVar3 = (byte *)((long)in_x8 + 1);
    *(byte *)in_x8 = (byte)((int)__n << 1);
    if (__n == 0) goto LAB_00e78b28;
  }
  else {
    uVar2 = __n + 0x10 & 0xfffffffffffffff0;
    pbVar3 = (byte *)operator_new(uVar2);
    in_x8[1] = __n;
    in_x8[2] = (ulong)pbVar3;
    *in_x8 = uVar2 | 1;
  }
  memset(pbVar3,0,__n);
LAB_00e78b28:
  pbVar3[__n] = 0;
  uVar2 = in_x8[1];
  pbVar3 = (byte *)in_x8[2];
  pcVar4 = (char *)((ulong)&local_70 | 1);
  if ((local_70 & 1) != 0) {
    pcVar4 = local_60;
  }
  if ((*(byte *)in_x8 & 1) == 0) {
    pbVar3 = (byte *)((long)in_x8 + 1);
    uVar2 = (ulong)(*(byte *)in_x8 >> 1);
  }
                    /* try { // try from 00e78b5c to 00e78b5f has its CatchHandler @ 00e78bb4 */
  strxfrm_l((char *)pbVar3,pcVar4,uVar2 + 1,*(__locale_t *)(param_1 + 0x10));
  if ((local_70 & 1) != 0) {
    operator_delete(local_60);
  }
  if (*(long *)(lVar1 + 0x28) != local_58) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
// Function: do_compare
// Address: 00e78f00
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::do_compare(wchar_t const*, wchar_t const*, wchar_t const*,
   wchar_t const*) const */

void __thiscall
std::__ndk1::collate_byname<wchar_t>::do_compare
          (collate_byname<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t *param_4)

{
  wchar_t *__s2;
  ulong uVar1;
  long lVar2;
  wchar_t *pwVar3;
  wchar_t *pwVar4;
  int iVar5;
  uint uVar6;
  wchar_t *pwVar7;
  ulong uVar8;
  ulong uVar9;
  undefined8 local_98;
  ulong local_90;
  wchar_t *local_88;
  undefined8 local_80;
  ulong local_78;
  wchar_t *local_70;
  long local_68;
  
  lVar2 = tpidr_el0;
  local_68 = *(long *)(lVar2 + 0x28);
  uVar1 = (long)param_2 - (long)param_1;
  if ((long)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  uVar9 = (long)uVar1 >> 2;
  if (uVar9 < 5) {
    local_80 = CONCAT71(local_80._1_7_,(char)(uVar1 >> 1)) & 0xfffffffffffffffe;
    pwVar7 = (wchar_t *)((ulong)&local_80 | 4);
  }
  else {
    uVar8 = uVar9 + 4 & 0xfffffffffffffffc;
    pwVar7 = (wchar_t *)operator_new(uVar8 << 2);
    local_80 = uVar8 | 1;
    local_78 = uVar9;
    local_70 = pwVar7;
  }
  if (param_1 != param_2) {
    memcpy(pwVar7,param_1,uVar1 & 0xfffffffffffffffc);
    pwVar7 = (wchar_t *)((long)pwVar7 + (uVar1 - 4 & 0xfffffffffffffffc) + 4);
  }
  uVar1 = (long)param_4 - (long)param_3;
  *pwVar7 = L'\0';
  if (-1 < (long)uVar1) {
    uVar9 = (long)uVar1 >> 2;
    if (uVar9 < 5) {
      local_98 = CONCAT71(local_98._1_7_,(char)(uVar1 >> 1)) & 0xfffffffffffffffe;
      pwVar7 = (wchar_t *)((ulong)&local_98 | 4);
    }
    else {
      uVar8 = uVar9 + 4 & 0xfffffffffffffffc;
                    /* try { // try from 00e790b8 to 00e790bb has its CatchHandler @ 00e790ec */
      pwVar7 = (wchar_t *)operator_new(uVar8 << 2);
      local_98 = uVar8 | 1;
      local_90 = uVar9;
      local_88 = pwVar7;
    }
    if (param_3 != param_4) {
      memcpy(pwVar7,param_3,uVar1 & 0xfffffffffffffffc);
      pwVar7 = (wchar_t *)((long)pwVar7 + (uVar1 - 4 & 0xfffffffffffffffc) + 4);
    }
    pwVar4 = local_70;
    uVar9 = local_80;
    pwVar3 = local_88;
    uVar1 = local_98;
    *pwVar7 = L'\0';
    pwVar7 = (wchar_t *)((ulong)&local_80 | 4);
    if ((local_80 & 1) != 0) {
      pwVar7 = local_70;
    }
    __s2 = (wchar_t *)((ulong)&local_98 | 4);
    if ((local_98 & 1) != 0) {
      __s2 = local_88;
    }
    iVar5 = wcscoll_l(pwVar7,__s2,*(__locale_t *)(this + 0x10));
    if ((uVar1 & 1) != 0) {
      operator_delete(pwVar3);
    }
    if ((uVar9 & 1) != 0) {
      operator_delete(pwVar4);
    }
    uVar6 = (uint)(iVar5 != 0);
    if (iVar5 < 0) {
      uVar6 = 0xffffffff;
    }
    if (*(long *)(lVar2 + 0x28) == local_68) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar6);
  }
                    /* try { // try from 00e790e0 to 00e790e7 has its CatchHandler @ 00e790ec */
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: do_transform
// Address: 00e79108
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::do_transform(wchar_t const*, wchar_t const*) const */

void std::__ndk1::collate_byname<wchar_t>::do_transform(wchar_t *param_1,wchar_t *param_2)

{
  long lVar1;
  wchar_t *__s1;
  size_t __n;
  wchar_t *in_x2;
  ulong *in_x8;
  wchar_t *pwVar2;
  ulong uVar3;
  ulong uVar4;
  ulong uVar5;
  undefined8 local_80;
  ulong local_78;
  wchar_t *local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  uVar3 = (long)in_x2 - (long)param_2;
  if ((long)uVar3 < 0) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  uVar4 = (long)uVar3 >> 2;
  if (uVar4 < 5) {
    local_80 = CONCAT71(local_80._1_7_,(char)(uVar3 >> 1)) & 0xfffffffffffffffe;
    pwVar2 = (wchar_t *)((ulong)&local_80 | 4);
  }
  else {
    uVar5 = uVar4 + 4 & 0xfffffffffffffffc;
    pwVar2 = (wchar_t *)operator_new(uVar5 << 2);
    local_80 = uVar5 | 1;
    local_78 = uVar4;
    local_70 = pwVar2;
  }
  if (param_2 != in_x2) {
    memcpy(pwVar2,param_2,uVar3 & 0xfffffffffffffffc);
    pwVar2 = (wchar_t *)((long)pwVar2 + (uVar3 - 4 & 0xfffffffffffffffc) + 4);
  }
  *pwVar2 = L'\0';
  pwVar2 = (wchar_t *)((ulong)&local_80 | 4);
  if ((local_80 & 1) != 0) {
    pwVar2 = local_70;
  }
                    /* try { // try from 00e791e4 to 00e7922b has its CatchHandler @ 00e79314 */
  __n = wcsxfrm_l((wchar_t *)0x0,pwVar2,0,*(__locale_t *)(param_1 + 4));
  if (0x3fffffffffffffef < __n) {
                    /* try { // try from 00e792d4 to 00e792db has its CatchHandler @ 00e79314 */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 5) {
    pwVar2 = (wchar_t *)((long)in_x8 + 4);
    *(byte *)in_x8 = (byte)((int)__n << 1);
    if (__n == 0) goto LAB_00e7924c;
  }
  else {
    uVar3 = __n + 4 & 0xfffffffffffffffc;
    pwVar2 = (wchar_t *)operator_new(uVar3 << 2);
    in_x8[1] = __n;
    in_x8[2] = (ulong)pwVar2;
    *in_x8 = uVar3 | 1;
  }
                    /* try { // try from 00e7923c to 00e7924b has its CatchHandler @ 00e792e0 */
  wmemset(pwVar2,L'\0',__n);
LAB_00e7924c:
  pwVar2[__n] = L'\0';
  pwVar2 = (wchar_t *)((ulong)&local_80 | 4);
  if ((local_80 & 1) != 0) {
    pwVar2 = local_70;
  }
  uVar3 = (ulong)(*(byte *)in_x8 >> 1);
  __s1 = (wchar_t *)((long)in_x8 + 4);
  if ((*(byte *)in_x8 & 1) != 0) {
    uVar3 = in_x8[1];
    __s1 = (wchar_t *)in_x8[2];
  }
                    /* try { // try from 00e79284 to 00e79287 has its CatchHandler @ 00e792e4 */
  wcsxfrm_l(__s1,pwVar2,uVar3 + 1,*(__locale_t *)(param_1 + 4));
  if ((local_80 & 1) != 0) {
    operator_delete(local_70);
  }
  if (*(long *)(lVar1 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
// Function: do_is
// Address: 00e7935c
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_is(unsigned long, wchar_t) const */

bool __thiscall
std::__ndk1::ctype<wchar_t>::do_is(ctype<wchar_t> *this,ulong param_1,wchar_t param_2)

{
  if (0x7f < (uint)param_2) {
    return false;
  }
  return (*(ulong *)(&DAT_00838378 + (ulong)(uint)param_2 * 8) & param_1) != 0;
}



// ==========================================================================================
// Function: do_is
// Address: 00e79398
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_is(wchar_t const*, wchar_t const*, unsigned long*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_is
          (ctype<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,ulong *param_3)

{
  wchar_t *pwVar1;
  ulong uVar2;
  
  pwVar1 = param_1;
  if (param_1 != param_2) {
    do {
      if ((uint)*pwVar1 < 0x80) {
        uVar2 = *(ulong *)(&DAT_00838378 + (ulong)(uint)*pwVar1 * 8);
      }
      else {
        uVar2 = 0;
      }
      pwVar1 = pwVar1 + 1;
      *param_3 = uVar2;
      param_1 = param_2;
      param_3 = param_3 + 1;
    } while (param_2 != pwVar1);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_scan_is
// Address: 00e793e4
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_scan_is(unsigned long, wchar_t const*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_scan_is
          (ctype<wchar_t> *this,ulong param_1,wchar_t *param_2,wchar_t *param_3)

{
  if (param_2 != param_3) {
    while ((0x7f < (uint)*param_2 ||
           ((*(ulong *)(&DAT_00838378 + (ulong)(uint)*param_2 * 8) & param_1) == 0))) {
      param_2 = param_2 + 1;
      if (param_3 == param_2) {
        return param_3;
      }
    }
  }
  return param_2;
}



// ==========================================================================================
// Function: do_scan_not
// Address: 00e79430
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_scan_not(unsigned long, wchar_t const*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_scan_not
          (ctype<wchar_t> *this,ulong param_1,wchar_t *param_2,wchar_t *param_3)

{
  wchar_t *pwVar1;
  
  pwVar1 = param_2;
  if (param_2 != param_3) {
    do {
      if (0x7f < (uint)*pwVar1) {
        return pwVar1;
      }
      if ((*(ulong *)(&DAT_00838378 + (ulong)(uint)*pwVar1 * 8) & param_1) == 0) {
        return pwVar1;
      }
      pwVar1 = pwVar1 + 1;
      param_2 = param_3;
    } while (param_3 != pwVar1);
  }
  return param_2;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e79474
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_toupper(wchar_t) const */

wchar_t __thiscall std::__ndk1::ctype<wchar_t>::do_toupper(ctype<wchar_t> *this,wchar_t param_1)

{
  int iVar1;
  
  if ((uint)param_1 < 0x80) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e794e4 to 00e794f7 has its CatchHandler @ 00e7950c */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar1 = iswlower_l(param_1,DAT_0231cfa8);
    if (iVar1 != 0) {
      param_1 = param_1 + L'\xffffffe0';
    }
  }
  return param_1;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e79524
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_toupper(wchar_t*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_toupper(ctype<wchar_t> *this,wchar_t *param_1,wchar_t *param_2)

{
  int iVar1;
  wchar_t *pwVar2;
  wchar_t *pwVar3;
  wchar_t wVar4;
  
  pwVar3 = param_1;
  if (param_1 != param_2) {
    do {
      wVar4 = *pwVar3;
      if ((uint)wVar4 < 0x80) {
        if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e795b8 to 00e795c7 has its CatchHandler @ 00e795ec */
          DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
          __cxa_guard_release(&DAT_0231cfb0);
        }
        iVar1 = islower_l(wVar4,DAT_0231cfa8);
        wVar4 = *pwVar3;
        if (iVar1 != 0) {
          wVar4 = *pwVar3 + L'\xffffffe0';
        }
      }
      pwVar2 = pwVar3 + 1;
      *pwVar3 = wVar4;
      param_1 = param_2;
      pwVar3 = pwVar2;
    } while (param_2 != pwVar2);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e79604
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_tolower(wchar_t) const */

wchar_t __thiscall std::__ndk1::ctype<wchar_t>::do_tolower(ctype<wchar_t> *this,wchar_t param_1)

{
  int iVar1;
  
  if ((uint)param_1 < 0x80) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e79674 to 00e79687 has its CatchHandler @ 00e7969c */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar1 = isupper_l(param_1,DAT_0231cfa8);
    if (iVar1 != 0) {
      param_1 = param_1 + L' ';
    }
  }
  return param_1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e796b4
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_tolower(wchar_t*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_tolower(ctype<wchar_t> *this,wchar_t *param_1,wchar_t *param_2)

{
  int iVar1;
  wchar_t *pwVar2;
  wchar_t *pwVar3;
  wchar_t wVar4;
  
  pwVar3 = param_1;
  if (param_1 != param_2) {
    do {
      wVar4 = *pwVar3;
      if ((uint)wVar4 < 0x80) {
        if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e79748 to 00e79757 has its CatchHandler @ 00e7977c */
          DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
          __cxa_guard_release(&DAT_0231cfb0);
        }
        iVar1 = isupper_l(wVar4,DAT_0231cfa8);
        wVar4 = *pwVar3;
        if (iVar1 != 0) {
          wVar4 = *pwVar3 + L' ';
        }
      }
      pwVar2 = pwVar3 + 1;
      *pwVar3 = wVar4;
      param_1 = param_2;
      pwVar3 = pwVar2;
    } while (param_2 != pwVar2);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e79794
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_widen(char) const */

char __thiscall std::__ndk1::ctype<wchar_t>::do_widen(ctype<wchar_t> *this,char param_1)

{
  return param_1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e797a0
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_widen(char const*, char const*, wchar_t*) const */

char * __thiscall
std::__ndk1::ctype<wchar_t>::do_widen
          (ctype<wchar_t> *this,char *param_1,char *param_2,wchar_t *param_3)

{
  byte *pbVar1;
  byte *pbVar2;
  
  pbVar2 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      pbVar1 = pbVar2 + 1;
      *param_3 = (uint)*pbVar2;
      param_1 = param_2;
      pbVar2 = pbVar1;
      param_3 = param_3 + 1;
    } while ((byte *)param_2 != pbVar1);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e797c8
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_narrow(wchar_t, char) const */

wchar_t __thiscall
std::__ndk1::ctype<wchar_t>::do_narrow(ctype<wchar_t> *this,wchar_t param_1,char param_2)

{
  wchar_t wVar1;
  
  wVar1 = (uint)(byte)param_2;
  if ((uint)param_1 < 0x80) {
    wVar1 = param_1;
  }
  return wVar1;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e797d8
// ==========================================================================================

/* std::__ndk1::ctype<wchar_t>::do_narrow(wchar_t const*, wchar_t const*, char, char*) const */

wchar_t * __thiscall
std::__ndk1::ctype<wchar_t>::do_narrow
          (ctype<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,char param_3,char *param_4)

{
  unkbyte9 *pVar1;
  wchar_t wVar2;
  undefined auVar3 [16];
  undefined8 uVar4;
  undefined auVar5 [16];
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  unkbyte9 Var9;
  wchar_t *pwVar10;
  ulong uVar12;
  ulong uVar13;
  unkbyte9 *pVar14;
  char *pcVar15;
  ulong uVar16;
  undefined uVar17;
  undefined uVar18;
  undefined uVar19;
  undefined uVar20;
  undefined uVar21;
  undefined uVar22;
  undefined auVar23 [16];
  undefined auVar24 [16];
  wchar_t *pwVar11;
  
  if (param_1 != param_2) {
    uVar12 = (long)param_2 + (-4 - (long)param_1);
    pwVar10 = param_1;
    if ((0x1b < uVar12) &&
       ((uVar12 = (uVar12 >> 2) + 1, param_1 + uVar12 <= param_4 || (param_4 + uVar12 <= param_1))))
    {
      uVar13 = uVar12 & 0x7ffffffffffffff8;
      pVar14 = (unkbyte9 *)(param_1 + 4);
      pcVar15 = param_4 + 4;
      uVar16 = uVar13;
      do {
        pVar1 = pVar14 + -1;
        uVar7 = *(undefined8 *)((long)pVar14 + -8);
        uVar17 = (undefined)((ulong)uVar7 >> 8);
        uVar18 = (undefined)((ulong)uVar7 >> 0x20);
        uVar19 = (undefined)((ulong)uVar7 >> 0x28);
        uVar4 = *(undefined8 *)pVar1;
        uVar8 = *(undefined8 *)((long)pVar14 + 8);
        uVar20 = (undefined)((ulong)uVar8 >> 8);
        uVar21 = (undefined)((ulong)uVar8 >> 0x20);
        uVar22 = (undefined)((ulong)uVar8 >> 0x28);
        uVar6 = *(undefined8 *)pVar14;
        Var9 = *pVar14;
        pVar14 = pVar14 + 2;
        uVar16 = uVar16 - 8;
        auVar23._8_4_ = 0x7f;
        auVar23._0_8_ = 0x7f0000007f;
        auVar23._12_4_ = 0x7f;
        auVar3[9] = uVar17;
        auVar3._0_9_ = *pVar1;
        auVar3[10] = (char)((ulong)uVar7 >> 0x10);
        auVar3[11] = (char)((ulong)uVar7 >> 0x18);
        auVar3[12] = uVar18;
        auVar3[13] = uVar19;
        auVar3[14] = (char)((ulong)uVar7 >> 0x30);
        auVar3[15] = (char)((ulong)uVar7 >> 0x38);
        auVar23 = NEON_cmhi(auVar3,auVar23,4);
        auVar24._8_4_ = 0x7f;
        auVar24._0_8_ = 0x7f0000007f;
        auVar24._12_4_ = 0x7f;
        auVar5[9] = uVar20;
        auVar5._0_9_ = Var9;
        auVar5[10] = (char)((ulong)uVar8 >> 0x10);
        auVar5[11] = (char)((ulong)uVar8 >> 0x18);
        auVar5[12] = uVar21;
        auVar5[13] = uVar22;
        auVar5[14] = (char)((ulong)uVar8 >> 0x30);
        auVar5[15] = (char)((ulong)uVar8 >> 0x38);
        auVar24 = NEON_cmhi(auVar5,auVar24,4);
        uVar4 = NEON_bit(CONCAT17(uVar19,CONCAT16(uVar18,CONCAT15(uVar17,CONCAT14((char)uVar7,
                                                                                  CONCAT13((char)((
                                                  ulong)uVar4 >> 0x28),
                                                  CONCAT12((char)((ulong)uVar4 >> 0x20),(short)uVar4
                                                          )))))),
                         (ulong)CONCAT16(param_3,(uint6)CONCAT14(param_3,(uint)CONCAT12(param_3,(
                                                  ushort)(byte)param_3))),
                         CONCAT26(auVar23._12_2_,
                                  CONCAT24(auVar23._8_2_,CONCAT22(auVar23._4_2_,auVar23._0_2_))),1);
        uVar7 = NEON_bit(CONCAT17(uVar22,CONCAT16(uVar21,CONCAT15(uVar20,CONCAT14((char)uVar8,
                                                                                  CONCAT13((char)((
                                                  ulong)uVar6 >> 0x28),
                                                  CONCAT12((char)((ulong)uVar6 >> 0x20),(short)uVar6
                                                          )))))),
                         (ulong)CONCAT16(param_3,(uint6)CONCAT14(param_3,(uint)CONCAT12(param_3,(
                                                  ushort)(byte)param_3))),
                         CONCAT26(auVar24._12_2_,
                                  CONCAT24(auVar24._8_2_,CONCAT22(auVar24._4_2_,auVar24._0_2_))),1);
        *(ulong *)(pcVar15 + -4) =
             CONCAT17((char)((ulong)uVar7 >> 0x30),
                      CONCAT16((char)((ulong)uVar7 >> 0x20),
                               CONCAT15((char)((ulong)uVar7 >> 0x10),
                                        CONCAT14((char)uVar7,
                                                 CONCAT13((char)((ulong)uVar4 >> 0x30),
                                                          CONCAT12((char)((ulong)uVar4 >> 0x20),
                                                                   CONCAT11((char)((ulong)uVar4 >>
                                                                                  0x10),(char)uVar4)
                                                                  ))))));
        pcVar15 = pcVar15 + 8;
      } while (uVar16 != 0);
      pwVar10 = param_1 + uVar13;
      param_4 = param_4 + uVar13;
      if (uVar12 == uVar13) {
        return param_2;
      }
    }
    do {
      pwVar11 = pwVar10 + 1;
      wVar2 = (uint)(byte)param_3;
      if ((uint)*pwVar10 < 0x80) {
        wVar2 = *pwVar10;
      }
      *param_4 = (char)wVar2;
      pwVar10 = pwVar11;
      param_1 = param_2;
      param_4 = param_4 + 1;
    } while (param_2 != pwVar11);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e79980
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_toupper(char) const */

uint __thiscall std::__ndk1::ctype<char>::do_toupper(ctype<char> *this,char param_1)

{
  int iVar1;
  uint uVar2;
  
  uVar2 = (uint)(byte)param_1;
  if (-1 < param_1) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e799ec to 00e799ff has its CatchHandler @ 00e79a14 */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar1 = islower_l((uint)(byte)param_1,DAT_0231cfa8);
    uVar2 = (uint)(byte)param_1;
    if (iVar1 != 0) {
      uVar2 = (byte)param_1 - 0x20;
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e79a2c
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_toupper(char*, char const*) const */

char * __thiscall
std::__ndk1::ctype<char>::do_toupper(ctype<char> *this,char *param_1,char *param_2)

{
  int iVar1;
  byte *pbVar2;
  byte *pbVar3;
  byte bVar4;
  
  pbVar3 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      bVar4 = *pbVar3;
      if (-1 < (char)bVar4) {
        if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e79abc to 00e79acb has its CatchHandler @ 00e79af0 */
          DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
          __cxa_guard_release(&DAT_0231cfb0);
        }
        iVar1 = islower_l((uint)bVar4,DAT_0231cfa8);
        bVar4 = *pbVar3;
        if (iVar1 != 0) {
          bVar4 = *pbVar3 - 0x20;
        }
      }
      pbVar2 = pbVar3 + 1;
      *pbVar3 = bVar4;
      param_1 = param_2;
      pbVar3 = pbVar2;
    } while ((byte *)param_2 != pbVar2);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e79b08
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_tolower(char) const */

uint __thiscall std::__ndk1::ctype<char>::do_tolower(ctype<char> *this,char param_1)

{
  int iVar1;
  uint uVar2;
  
  uVar2 = (uint)(byte)param_1;
  if (-1 < param_1) {
    if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e79b74 to 00e79b87 has its CatchHandler @ 00e79b9c */
      DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
      __cxa_guard_release(&DAT_0231cfb0);
    }
    iVar1 = isupper_l((uint)(byte)param_1,DAT_0231cfa8);
    uVar2 = (uint)(byte)param_1;
    if (iVar1 != 0) {
      uVar2 = (byte)param_1 + 0x20;
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e79bb4
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_tolower(char*, char const*) const */

char * __thiscall
std::__ndk1::ctype<char>::do_tolower(ctype<char> *this,char *param_1,char *param_2)

{
  int iVar1;
  byte *pbVar2;
  byte *pbVar3;
  byte bVar4;
  
  pbVar3 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      bVar4 = *pbVar3;
      if (-1 < (char)bVar4) {
        if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e79c44 to 00e79c53 has its CatchHandler @ 00e79c78 */
          DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
          __cxa_guard_release(&DAT_0231cfb0);
        }
        iVar1 = isupper_l((uint)bVar4,DAT_0231cfa8);
        bVar4 = *pbVar3;
        if (iVar1 != 0) {
          bVar4 = *pbVar3 + 0x20;
        }
      }
      pbVar2 = pbVar3 + 1;
      *pbVar3 = bVar4;
      param_1 = param_2;
      pbVar3 = pbVar2;
    } while ((byte *)param_2 != pbVar2);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e79c90
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_widen(char) const */

char __thiscall std::__ndk1::ctype<char>::do_widen(ctype<char> *this,char param_1)

{
  return param_1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e79c9c
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_widen(char const*, char const*, char*) const */

char * __thiscall
std::__ndk1::ctype<char>::do_widen(ctype<char> *this,char *param_1,char *param_2,char *param_3)

{
  undefined8 *puVar1;
  char *pcVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  undefined8 *puVar6;
  ulong uVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  
  if (param_1 == param_2) {
    return param_1;
  }
  uVar3 = (long)param_2 - (long)param_1;
  if ((7 < uVar3) && ((param_2 <= param_3 || (param_3 + uVar3 <= param_1)))) {
    if (uVar3 < 0x20) {
      uVar4 = 0;
    }
    else {
      uVar4 = uVar3 & 0xffffffffffffffe0;
      puVar6 = (undefined8 *)(param_1 + 0x10);
      puVar8 = (undefined8 *)(param_3 + 0x10);
      uVar7 = uVar4;
      do {
        puVar1 = puVar6 + -1;
        uVar9 = puVar6[-2];
        uVar11 = puVar6[1];
        uVar10 = *puVar6;
        puVar6 = puVar6 + 4;
        uVar7 = uVar7 - 0x20;
        puVar8[-1] = *puVar1;
        puVar8[-2] = uVar9;
        puVar8[1] = uVar11;
        *puVar8 = uVar10;
        puVar8 = puVar8 + 4;
      } while (uVar7 != 0);
      if (uVar3 == uVar4) {
        return param_2;
      }
      if ((uVar3 & 0x18) == 0) {
        param_1 = param_1 + uVar4;
        param_3 = param_3 + uVar4;
        goto LAB_00e79d50;
      }
    }
    uVar7 = uVar3 & 0xfffffffffffffff8;
    lVar5 = uVar4 - uVar7;
    puVar6 = (undefined8 *)(param_1 + uVar4);
    puVar8 = (undefined8 *)(param_3 + uVar4);
    do {
      lVar5 = lVar5 + 8;
      *puVar8 = *puVar6;
      puVar6 = puVar6 + 1;
      puVar8 = puVar8 + 1;
    } while (lVar5 != 0);
    param_1 = param_1 + uVar7;
    param_3 = param_3 + uVar7;
    if (uVar3 == uVar7) {
      return param_2;
    }
  }
LAB_00e79d50:
  do {
    pcVar2 = param_1 + 1;
    *param_3 = *param_1;
    param_1 = pcVar2;
    param_3 = param_3 + 1;
  } while (param_2 != pcVar2);
  return param_2;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e79d68
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_narrow(char, char) const */

char __thiscall std::__ndk1::ctype<char>::do_narrow(ctype<char> *this,char param_1,char param_2)

{
  if (-1 < param_1) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e79d7c
// ==========================================================================================

/* std::__ndk1::ctype<char>::do_narrow(char const*, char const*, char, char*) const */

char * __thiscall
std::__ndk1::ctype<char>::do_narrow
          (ctype<char> *this,char *param_1,char *param_2,char param_3,char *param_4)

{
  char cVar1;
  char *pcVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  ulong uVar6;
  undefined8 *puVar7;
  undefined (*pauVar8) [16];
  undefined8 *puVar9;
  undefined auVar10 [16];
  undefined8 uVar11;
  undefined auVar12 [16];
  
  if (param_1 == param_2) {
    return param_1;
  }
  uVar3 = (long)param_2 - (long)param_1;
  if ((7 < uVar3) && ((param_2 <= param_4 || (param_4 + uVar3 <= param_1)))) {
    if (uVar3 < 0x10) {
      uVar4 = 0;
    }
    else {
      uVar4 = uVar3 & 0xfffffffffffffff0;
      uVar6 = uVar4;
      puVar7 = (undefined8 *)param_4;
      pauVar8 = (undefined (*) [16])param_1;
      do {
        uVar6 = uVar6 - 0x10;
        auVar12 = NEON_cmlt(*pauVar8,0,1);
        auVar10[1] = param_3;
        auVar10[0] = param_3;
        auVar10[2] = param_3;
        auVar10[3] = param_3;
        auVar10[4] = param_3;
        auVar10[5] = param_3;
        auVar10[6] = param_3;
        auVar10[7] = param_3;
        auVar10[8] = param_3;
        auVar10[9] = param_3;
        auVar10[10] = param_3;
        auVar10[11] = param_3;
        auVar10[12] = param_3;
        auVar10[13] = param_3;
        auVar10[14] = param_3;
        auVar10[15] = param_3;
        auVar10 = NEON_bit(*pauVar8,auVar10,auVar12,1);
        puVar7[1] = auVar10._8_8_;
        *puVar7 = auVar10._0_8_;
        puVar7 = puVar7 + 2;
        pauVar8 = pauVar8 + 1;
      } while (uVar6 != 0);
      if (uVar3 == uVar4) {
        return param_2;
      }
      if (((uint)uVar3 >> 3 & 1) == 0) {
        param_1 = param_1 + uVar4;
        param_4 = param_4 + uVar4;
        goto LAB_00e79e3c;
      }
    }
    uVar6 = uVar3 & 0xfffffffffffffff8;
    lVar5 = uVar4 - uVar6;
    puVar7 = (undefined8 *)(param_1 + uVar4);
    puVar9 = (undefined8 *)(param_4 + uVar4);
    do {
      lVar5 = lVar5 + 8;
      uVar11 = NEON_cmlt(*puVar7,0,1);
      uVar11 = NEON_bit(*puVar7,CONCAT17(param_3,CONCAT16(param_3,CONCAT15(param_3,CONCAT14(param_3,
                                                  CONCAT13(param_3,CONCAT12(param_3,CONCAT11(param_3
                                                  ,param_3))))))),uVar11,1);
      *puVar9 = uVar11;
      puVar7 = puVar7 + 1;
      puVar9 = puVar9 + 1;
    } while (lVar5 != 0);
    param_1 = param_1 + uVar6;
    param_4 = param_4 + uVar6;
    if (uVar3 == uVar6) {
      return param_2;
    }
  }
LAB_00e79e3c:
  do {
    pcVar2 = param_1 + 1;
    cVar1 = param_3;
    if (-1 < *param_1) {
      cVar1 = *param_1;
    }
    *param_4 = cVar1;
    param_1 = pcVar2;
    param_4 = param_4 + 1;
  } while (param_2 != pcVar2);
  return param_2;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e7a194
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::do_toupper(char) const */

int __thiscall std::__ndk1::ctype_byname<char>::do_toupper(ctype_byname<char> *this,char param_1)

{
  int iVar1;
  
  iVar1 = toupper_l((uint)(byte)param_1,*(__locale_t *)(this + 0x20));
  return iVar1;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e7a1bc
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::do_toupper(char*, char const*) const */

char * __thiscall
std::__ndk1::ctype_byname<char>::do_toupper(ctype_byname<char> *this,char *param_1,char *param_2)

{
  int iVar1;
  byte *pbVar2;
  byte *pbVar3;
  
  pbVar2 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      iVar1 = toupper_l((uint)*pbVar2,*(__locale_t *)(this + 0x20));
      pbVar3 = pbVar2 + 1;
      *pbVar2 = (byte)iVar1;
      param_1 = param_2;
      pbVar2 = pbVar3;
    } while ((byte *)param_2 != pbVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e7a218
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::do_tolower(char) const */

int __thiscall std::__ndk1::ctype_byname<char>::do_tolower(ctype_byname<char> *this,char param_1)

{
  int iVar1;
  
  iVar1 = tolower_l((uint)(byte)param_1,*(__locale_t *)(this + 0x20));
  return iVar1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e7a240
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::do_tolower(char*, char const*) const */

char * __thiscall
std::__ndk1::ctype_byname<char>::do_tolower(ctype_byname<char> *this,char *param_1,char *param_2)

{
  int iVar1;
  byte *pbVar2;
  byte *pbVar3;
  
  pbVar2 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      iVar1 = tolower_l((uint)*pbVar2,*(__locale_t *)(this + 0x20));
      pbVar3 = pbVar2 + 1;
      *pbVar2 = (byte)iVar1;
      param_1 = param_2;
      pbVar2 = pbVar3;
    } while ((byte *)param_2 != pbVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_is
// Address: 00e7a548
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::ctype_byname<wchar_t>::do_is(unsigned long, wchar_t) const */

bool __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_is(ctype_byname<wchar_t> *this,ulong param_1,wchar_t param_2)

{
  undefined uVar1;
  int iVar2;
  uint uVar3;
  
  uVar3 = (uint)param_1;
  if ((param_1 & 1) == 0) {
    uVar1 = false;
  }
  else {
    iVar2 = iswspace_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = iVar2 != 0;
  }
  if ((uVar3 >> 1 & 1) != 0) {
    iVar2 = iswprint_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 2 & 1) != 0) {
    iVar2 = iswcntrl_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 3 & 1) != 0) {
    iVar2 = iswupper_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 4 & 1) != 0) {
    iVar2 = iswlower_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 5 & 1) != 0) {
    iVar2 = iswalpha_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 6 & 1) != 0) {
    iVar2 = iswdigit_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 7 & 1) != 0) {
    iVar2 = iswpunct_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 8 & 1) != 0) {
    iVar2 = iswxdigit_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  if ((uVar3 >> 9 & 1) != 0) {
    iVar2 = iswblank_l(param_2,*(__locale_t *)(this + 0x10));
    uVar1 = uVar1 | iVar2 != 0;
  }
  return (bool)uVar1;
}



// ==========================================================================================
// Function: do_is
// Address: 00e7a6c0
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_is(wchar_t const*, wchar_t const*, unsigned long*) const
    */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_is
          (ctype_byname<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,ulong *param_3)

{
  wchar_t __wc;
  int iVar1;
  ulong uVar2;
  wchar_t *pwVar3;
  
  pwVar3 = param_1;
  if (param_1 != param_2) {
    do {
      __wc = *pwVar3;
      if ((uint)__wc < 0x80) {
        uVar2 = *(ulong *)(&DAT_00838378 + (ulong)(uint)__wc * 8);
LAB_00e7a700:
        *param_3 = uVar2;
      }
      else {
        *param_3 = 0;
        iVar1 = iswspace_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 1;
        }
        iVar1 = iswprint_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 2;
        }
        iVar1 = iswcntrl_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 4;
        }
        iVar1 = iswupper_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 8;
        }
        iVar1 = iswlower_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 0x10;
        }
        iVar1 = iswalpha_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 0x20;
        }
        iVar1 = iswdigit_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 0x40;
        }
        iVar1 = iswpunct_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 0x80;
        }
        iVar1 = iswxdigit_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          *param_3 = *param_3 | 0x100;
        }
        iVar1 = iswblank_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 != 0) {
          uVar2 = *param_3 | 0x200;
          goto LAB_00e7a700;
        }
      }
      pwVar3 = pwVar3 + 1;
      param_3 = param_3 + 1;
      param_1 = param_2;
    } while (param_2 != pwVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_scan_is
// Address: 00e7a85c
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_scan_is(unsigned long, wchar_t const*, wchar_t const*)
   const */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_scan_is
          (ctype_byname<wchar_t> *this,ulong param_1,wchar_t *param_2,wchar_t *param_3)

{
  wchar_t __wc;
  int iVar1;
  uint uVar2;
  
  if (param_2 != param_3) {
    while( true ) {
      __wc = *param_2;
      uVar2 = (uint)param_1;
      if ((((((param_1 & 1) != 0) &&
            (iVar1 = iswspace_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) ||
           (((uVar2 >> 1 & 1) != 0 &&
            (iVar1 = iswprint_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)))) ||
          (((uVar2 >> 2 & 1) != 0 &&
           (iVar1 = iswcntrl_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)))) ||
         (((uVar2 >> 3 & 1) != 0 &&
          (iVar1 = iswupper_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)))) break;
      if (((uVar2 >> 4 & 1) != 0) &&
         (iVar1 = iswlower_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      if (((uVar2 >> 5 & 1) != 0) &&
         (iVar1 = iswalpha_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      if (((uVar2 >> 6 & 1) != 0) &&
         (iVar1 = iswdigit_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      if (((uVar2 >> 7 & 1) != 0) &&
         (iVar1 = iswpunct_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      if (((uVar2 >> 8 & 1) != 0) &&
         (iVar1 = iswxdigit_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      if (((uVar2 >> 9 & 1) != 0) &&
         (iVar1 = iswblank_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 != 0)) {
        return param_2;
      }
      param_2 = param_2 + 1;
      if (param_3 == param_2) {
        return param_3;
      }
    }
  }
  return param_2;
}



// ==========================================================================================
// Function: do_scan_not
// Address: 00e7a98c
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_scan_not(unsigned long, wchar_t const*, wchar_t const*)
   const */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_scan_not
          (ctype_byname<wchar_t> *this,ulong param_1,wchar_t *param_2,wchar_t *param_3)

{
  wchar_t __wc;
  int iVar1;
  wchar_t *pwVar2;
  uint uVar3;
  
  pwVar2 = param_2;
  if (param_2 != param_3) {
    do {
      __wc = *pwVar2;
      uVar3 = (uint)param_1;
      if (((((((param_1 & 1) == 0) ||
             (iVar1 = iswspace_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)) &&
            (((uVar3 >> 1 & 1) == 0 ||
             (iVar1 = iswprint_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))) &&
           (((uVar3 >> 2 & 1) == 0 ||
            (iVar1 = iswcntrl_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))) &&
          (((uVar3 >> 3 & 1) == 0 ||
           (iVar1 = iswupper_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))) &&
         ((((((uVar3 >> 4 & 1) == 0 ||
             (iVar1 = iswlower_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)) &&
            (((uVar3 >> 5 & 1) == 0 ||
             (iVar1 = iswalpha_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))) &&
           (((uVar3 >> 6 & 1) == 0 ||
            (iVar1 = iswdigit_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))) &&
          ((((uVar3 >> 7 & 1) == 0 ||
            (iVar1 = iswpunct_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)) &&
           (((uVar3 >> 8 & 1) == 0 ||
            (iVar1 = iswxdigit_l(__wc,*(__locale_t *)(this + 0x10)), iVar1 == 0)))))))) {
        if ((uVar3 >> 9 & 1) == 0) {
          return pwVar2;
        }
        iVar1 = iswblank_l(__wc,*(__locale_t *)(this + 0x10));
        if (iVar1 == 0) {
          return pwVar2;
        }
      }
      pwVar2 = pwVar2 + 1;
      param_2 = param_3;
    } while (param_3 != pwVar2);
  }
  return param_2;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e7aabc
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_toupper(wchar_t) const */

wint_t __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_toupper(ctype_byname<wchar_t> *this,wchar_t param_1)

{
  wint_t wVar1;
  
  wVar1 = towupper_l(param_1,*(__locale_t *)(this + 0x10));
  return wVar1;
}



// ==========================================================================================
// Function: do_toupper
// Address: 00e7aad0
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_toupper(wchar_t*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_toupper
          (ctype_byname<wchar_t> *this,wchar_t *param_1,wchar_t *param_2)

{
  wchar_t wVar1;
  wchar_t *pwVar2;
  wchar_t *pwVar3;
  
  pwVar2 = param_1;
  if (param_1 != param_2) {
    do {
      wVar1 = towupper_l(*pwVar2,*(__locale_t *)(this + 0x10));
      pwVar3 = pwVar2 + 1;
      *pwVar2 = wVar1;
      param_1 = param_2;
      pwVar2 = pwVar3;
    } while (param_2 != pwVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e7ab2c
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_tolower(wchar_t) const */

wint_t __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_tolower(ctype_byname<wchar_t> *this,wchar_t param_1)

{
  wint_t wVar1;
  
  wVar1 = towlower_l(param_1,*(__locale_t *)(this + 0x10));
  return wVar1;
}



// ==========================================================================================
// Function: do_tolower
// Address: 00e7ab40
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_tolower(wchar_t*, wchar_t const*) const */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_tolower
          (ctype_byname<wchar_t> *this,wchar_t *param_1,wchar_t *param_2)

{
  wchar_t wVar1;
  wchar_t *pwVar2;
  wchar_t *pwVar3;
  
  pwVar2 = param_1;
  if (param_1 != param_2) {
    do {
      wVar1 = towlower_l(*pwVar2,*(__locale_t *)(this + 0x10));
      pwVar3 = pwVar2 + 1;
      *pwVar2 = wVar1;
      param_1 = param_2;
      pwVar2 = pwVar3;
    } while (param_2 != pwVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e7ab9c
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_widen(char) const */

wint_t __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_widen(ctype_byname<wchar_t> *this,char param_1)

{
  wint_t wVar1;
  __locale_t __dataset;
  
  __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7abbc to 00e7abc3 has its CatchHandler @ 00e7abec */
  wVar1 = btowc((uint)(byte)param_1);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7abcc to 00e7abd3 has its CatchHandler @ 00e7abe8 */
    uselocale(__dataset);
  }
  return wVar1;
}



// ==========================================================================================
// Function: do_widen
// Address: 00e7ac08
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_widen(char const*, char const*, wchar_t*) const */

char * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_widen
          (ctype_byname<wchar_t> *this,char *param_1,char *param_2,wchar_t *param_3)

{
  byte bVar1;
  wchar_t wVar2;
  __locale_t __dataset;
  byte *pbVar3;
  
  pbVar3 = (byte *)param_1;
  if (param_1 != param_2) {
    do {
      bVar1 = *pbVar3;
      __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7ac5c to 00e7ac63 has its CatchHandler @ 00e7ac9c */
      wVar2 = btowc((uint)bVar1);
      if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7ac6c to 00e7ac73 has its CatchHandler @ 00e7ac98 */
        uselocale(__dataset);
      }
      pbVar3 = pbVar3 + 1;
      *param_3 = wVar2;
      param_1 = param_2;
      param_3 = param_3 + 1;
    } while ((byte *)param_2 != pbVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e7acb8
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_narrow(wchar_t, char) const */

uint __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_narrow
          (ctype_byname<wchar_t> *this,wchar_t param_1,char param_2)

{
  uint uVar1;
  uint uVar2;
  __locale_t __dataset;
  
  __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7ace0 to 00e7ace7 has its CatchHandler @ 00e7ad18 */
  uVar2 = wctob(param_1);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7acf0 to 00e7acf7 has its CatchHandler @ 00e7ad14 */
    uselocale(__dataset);
  }
  uVar1 = (uint)(byte)param_2;
  if (uVar2 != 0xffffffff) {
    uVar1 = uVar2;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_narrow
// Address: 00e7ad34
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::do_narrow(wchar_t const*, wchar_t const*, char, char*) const
    */

wchar_t * __thiscall
std::__ndk1::ctype_byname<wchar_t>::do_narrow
          (ctype_byname<wchar_t> *this,wchar_t *param_1,wchar_t *param_2,char param_3,char *param_4)

{
  uint uVar1;
  wchar_t __c;
  uint uVar2;
  __locale_t __dataset;
  wchar_t *pwVar3;
  
  pwVar3 = param_1;
  if (param_1 != param_2) {
    do {
      __c = *pwVar3;
      __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7ad98 to 00e7ad9f has its CatchHandler @ 00e7addc */
      uVar2 = wctob(__c);
      if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7ada8 to 00e7adaf has its CatchHandler @ 00e7add8 */
        uselocale(__dataset);
      }
      pwVar3 = pwVar3 + 1;
      uVar1 = (uint)(byte)param_3;
      if (uVar2 != 0xffffffff) {
        uVar1 = uVar2;
      }
      *param_4 = (char)uVar1;
      param_1 = param_2;
      param_4 = param_4 + 1;
    } while (param_2 != pwVar3);
  }
  return param_1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7ae24
// ==========================================================================================

/* std::__ndk1::codecvt<char, char, mbstate_t>::do_out(mbstate_t&, char const*, char const*, char
   const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::codecvt<char,char,mbstate_t>::do_out
          (codecvt<char,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,char *param_5,char *param_6,char **param_7)

{
  *param_4 = param_2;
  *param_7 = param_5;
  return 3;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7ae38
// ==========================================================================================

/* std::__ndk1::codecvt<char, char, mbstate_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::codecvt<char,char,mbstate_t>::do_in
          (codecvt<char,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,char *param_5,char *param_6,char **param_7)

{
  *param_4 = param_2;
  *param_7 = param_5;
  return 3;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7ae4c
// ==========================================================================================

/* std::__ndk1::codecvt<char, char, mbstate_t>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::codecvt<char,char,mbstate_t>::do_unshift
          (codecvt<char,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7ae5c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char, char, mbstate_t>::do_encoding() const */

undefined8 std::__ndk1::codecvt<char,char,mbstate_t>::do_encoding(void)

{
  return 1;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7ae68
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char, char, mbstate_t>::do_always_noconv() const */

undefined8 std::__ndk1::codecvt<char,char,mbstate_t>::do_always_noconv(void)

{
  return 1;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7ae74
// ==========================================================================================

/* std::__ndk1::codecvt<char, char, mbstate_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

undefined4 __thiscall
std::__ndk1::codecvt<char,char,mbstate_t>::do_length
          (codecvt<char,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  undefined4 uVar1;
  
  uVar1 = (int)((long)param_3 - (long)param_2);
  if (param_4 <= (ulong)((long)param_3 - (long)param_2)) {
    uVar1 = (int)param_4;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7ae88
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char, char, mbstate_t>::do_max_length() const */

undefined8 std::__ndk1::codecvt<char,char,mbstate_t>::do_max_length(void)

{
  return 1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7b0e0
// ==========================================================================================

/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_out(mbstate_t&, wchar_t const*, wchar_t
   const*, wchar_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_out
          (codecvt<wchar_t,char,mbstate_t> *this,mbstate_t *param_1,wchar_t *param_2,
          wchar_t *param_3,wchar_t **param_4,char *param_5,char *param_6,char **param_7)

{
  wchar_t __wc;
  char cVar1;
  long lVar2;
  wchar_t *pwVar3;
  undefined uVar4;
  __locale_t p_Var5;
  size_t sVar6;
  char *pcVar7;
  char *pcVar8;
  wchar_t *pwVar9;
  mbstate_t local_78;
  char local_6c [4];
  long local_68;
  
  lVar2 = tpidr_el0;
  local_68 = *(long *)(lVar2 + 0x28);
  pwVar9 = param_2;
  pwVar3 = param_2;
  if (param_2 != param_3) {
    do {
      pwVar9 = pwVar3;
      if (*pwVar9 == L'\0') break;
      pwVar3 = pwVar9 + 1;
      pwVar9 = param_3;
    } while (param_3 != pwVar3);
  }
  *param_7 = param_5;
  *param_4 = param_2;
  if ((param_5 != param_6) && (param_2 != param_3)) {
    do {
      local_78 = *param_1;
      p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b1ac to 00e7b1c3 has its CatchHandler @ 00e7b40c */
      sVar6 = wcsnrtombs(param_5,param_4,(long)pwVar9 - (long)param_2 >> 2,
                         (long)param_6 - (long)param_5,param_1);
      if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b1cc to 00e7b1d3 has its CatchHandler @ 00e7b408 */
        uselocale(p_Var5);
      }
      if (sVar6 == 0) {
LAB_00e7b2f0:
        uVar4 = 1;
        goto LAB_00e7b38c;
      }
      if (sVar6 == 0xffffffffffffffff) {
        *param_7 = param_5;
        if (param_2 != *param_4) goto LAB_00e7b314;
        goto LAB_00e7b36c;
      }
      param_5 = *param_7 + sVar6;
      *param_7 = param_5;
      if (param_5 == param_6) {
        param_2 = *param_4;
        break;
      }
      if (pwVar9 == param_3) {
        param_2 = *param_4;
        pwVar9 = param_3;
      }
      else {
        p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b210 to 00e7b21f has its CatchHandler @ 00e7b3f0 */
        sVar6 = wcrtomb(local_6c,L'\0',param_1);
        if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b228 to 00e7b22f has its CatchHandler @ 00e7b3ec */
          uselocale(p_Var5);
        }
        if (sVar6 == 0xffffffffffffffff) {
          uVar4 = 2;
          goto LAB_00e7b38c;
        }
        pcVar7 = *param_7;
        if ((ulong)((long)param_6 - (long)pcVar7) < sVar6) goto LAB_00e7b2f0;
        if (sVar6 != 0) {
          *param_7 = pcVar7 + 1;
          *pcVar7 = local_6c[0];
          pcVar7 = (char *)((ulong)local_6c | 1);
          while (sVar6 = sVar6 - 1, sVar6 != 0) {
            pcVar8 = *param_7;
            cVar1 = *pcVar7;
            *param_7 = pcVar8 + 1;
            *pcVar8 = cVar1;
            pcVar7 = pcVar7 + 1;
          }
        }
        param_2 = *param_4 + 1;
        *param_4 = param_2;
        for (pwVar3 = param_2;
            (pwVar9 = param_3, pwVar3 != param_3 && (pwVar9 = pwVar3, *pwVar3 != L'\0'));
            pwVar3 = pwVar3 + 1) {
        }
        param_5 = *param_7;
      }
      if ((param_5 == param_6) || (param_2 == param_3)) break;
    } while( true );
  }
  uVar4 = param_2 != param_3;
  goto LAB_00e7b38c;
  while( true ) {
    param_2 = param_2 + 1;
    param_5 = *param_7 + sVar6;
    *param_7 = param_5;
    if (param_2 == *param_4) break;
LAB_00e7b314:
    __wc = *param_2;
    p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b324 to 00e7b333 has its CatchHandler @ 00e7b3d4 */
    sVar6 = wcrtomb(param_5,__wc,&local_78);
    if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b33c to 00e7b343 has its CatchHandler @ 00e7b3d0 */
      uselocale(p_Var5);
    }
    if (sVar6 == 0xffffffffffffffff) break;
  }
LAB_00e7b36c:
  uVar4 = 2;
  *param_4 = param_2;
LAB_00e7b38c:
  if (*(long *)(lVar2 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar4);
}



// ==========================================================================================
// Function: do_in
// Address: 00e7b428
// ==========================================================================================

/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, wchar_t*, wchar_t*, wchar_t*&) const */

void __thiscall
std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_in
          (codecvt<wchar_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar_t *param_5,wchar_t *param_6,wchar_t **param_7)

{
  char *pcVar1;
  wchar_t *__pwc;
  long lVar2;
  bool bVar3;
  undefined uVar4;
  __locale_t p_Var5;
  size_t sVar6;
  char *pcVar7;
  char *pcVar8;
  mbstate_t local_70;
  long local_68;
  
  lVar2 = tpidr_el0;
  local_68 = *(long *)(lVar2 + 0x28);
  pcVar8 = param_2;
  pcVar1 = param_2;
  if (param_2 != param_3) {
    do {
      pcVar8 = pcVar1;
      if (*pcVar8 == '\0') break;
      pcVar1 = pcVar8 + 1;
      pcVar8 = param_3;
    } while (param_3 != pcVar1);
  }
  *param_7 = param_5;
  *param_4 = param_2;
  if ((param_5 != param_6) && (param_2 != param_3)) {
    while( true ) {
      local_70 = *param_1;
      p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b4e8 to 00e7b4ff has its CatchHandler @ 00e7b72c */
      sVar6 = mbsnrtowcs(param_5,param_4,(long)pcVar8 - (long)param_2,
                         (long)param_6 - (long)param_5 >> 2,param_1);
      if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b508 to 00e7b50f has its CatchHandler @ 00e7b728 */
        uselocale(p_Var5);
      }
      if (sVar6 == 0xffffffffffffffff) {
        *param_7 = param_5;
        if (param_2 != *param_4) goto LAB_00e7b620;
        goto LAB_00e7b684;
      }
      __pwc = *param_7 + sVar6;
      *param_7 = __pwc;
      if (__pwc == param_6) break;
      bVar3 = pcVar8 != param_3;
      param_2 = *param_4;
      pcVar8 = param_3;
      if (bVar3) {
        p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b550 to 00e7b563 has its CatchHandler @ 00e7b710 */
        sVar6 = mbrtowc(__pwc,param_2,1,param_1);
        if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b56c to 00e7b573 has its CatchHandler @ 00e7b70c */
          uselocale(p_Var5);
        }
        if (sVar6 != 0) {
          uVar4 = 2;
          goto LAB_00e7b6a4;
        }
        *param_7 = *param_7 + 1;
        pcVar1 = *param_4 + 1;
        *param_4 = pcVar1;
        param_2 = param_3;
        pcVar7 = pcVar1;
        if (pcVar1 == param_3) goto LAB_00e7b69c;
        do {
          param_2 = pcVar1;
          pcVar8 = pcVar7;
          if (*pcVar7 == '\0') break;
          pcVar7 = pcVar7 + 1;
          pcVar8 = param_3;
        } while (param_3 != pcVar7);
      }
      param_5 = *param_7;
      if ((param_5 == param_6) || (param_2 == param_3)) goto LAB_00e7b69c;
    }
    param_2 = *param_4;
  }
  goto LAB_00e7b69c;
LAB_00e7b620:
  do {
    p_Var5 = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b630 to 00e7b643 has its CatchHandler @ 00e7b6f4 */
    sVar6 = mbrtowc(param_5,param_2,(long)pcVar8 - (long)param_2,&local_70);
    if (p_Var5 != (__locale_t)0x0) {
                    /* try { // try from 00e7b64c to 00e7b653 has its CatchHandler @ 00e7b6f0 */
      uselocale(p_Var5);
    }
    if (sVar6 == 0) {
      sVar6 = 1;
    }
    else {
      if (sVar6 == 0xfffffffffffffffe) {
        uVar4 = 1;
        *param_4 = param_2;
        goto LAB_00e7b6a4;
      }
      if (sVar6 == 0xffffffffffffffff) {
        uVar4 = 2;
        *param_4 = param_2;
        goto LAB_00e7b6a4;
      }
    }
    param_2 = param_2 + sVar6;
    param_5 = *param_7 + 1;
    *param_7 = param_5;
  } while (param_2 != *param_4);
LAB_00e7b684:
  *param_4 = param_2;
LAB_00e7b69c:
  uVar4 = param_2 != param_3;
LAB_00e7b6a4:
  if (*(long *)(lVar2 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar4);
  }
  return;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7b748
// ==========================================================================================

/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_unshift(mbstate_t&, char*, char*, char*&)
   const */

void __thiscall
std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_unshift
          (codecvt<wchar_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  char cVar1;
  long lVar2;
  __locale_t __dataset;
  size_t sVar3;
  undefined8 uVar4;
  long lVar5;
  char *pcVar6;
  char *pcVar7;
  char local_4c [4];
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  *param_4 = param_2;
  __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b78c to 00e7b79b has its CatchHandler @ 00e7b854 */
  sVar3 = wcrtomb(local_4c,L'\0',param_1);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7b7a4 to 00e7b7ab has its CatchHandler @ 00e7b850 */
    uselocale(__dataset);
  }
  if (sVar3 + 1 < 2) {
    uVar4 = 2;
  }
  else {
    pcVar6 = *param_4;
    if ((ulong)((long)param_3 - (long)pcVar6) < sVar3 - 1) {
      uVar4 = 1;
    }
    else {
      if (sVar3 != 1) {
        *param_4 = pcVar6 + 1;
        lVar5 = sVar3 - 2;
        *pcVar6 = local_4c[0];
        if (lVar5 != 0) {
          pcVar6 = (char *)((ulong)local_4c | 1);
          do {
            pcVar7 = *param_4;
            cVar1 = *pcVar6;
            lVar5 = lVar5 + -1;
            *param_4 = pcVar7 + 1;
            *pcVar7 = cVar1;
            pcVar6 = pcVar6 + 1;
          } while (lVar5 != 0);
        }
      }
      uVar4 = 0;
    }
  }
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar4);
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7b870
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_encoding() const */

ulong std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_encoding(void)

{
  int iVar1;
  long in_x0;
  __locale_t p_Var2;
  ulong uVar3;
  size_t sVar4;
  
                    /* try { // try from 00e7b88c to 00e7b88f has its CatchHandler @ 00e7b940 */
  p_Var2 = uselocale(*(__locale_t *)(in_x0 + 0x10));
                    /* try { // try from 00e7b894 to 00e7b8a3 has its CatchHandler @ 00e7b928 */
  iVar1 = mbtowc((wchar_t *)0x0,(char *)0x0,4);
  if (p_Var2 != (__locale_t)0x0) {
                    /* try { // try from 00e7b8ac to 00e7b8b3 has its CatchHandler @ 00e7b924 */
    uselocale(p_Var2);
  }
  if (iVar1 == 0) {
    if (*(__locale_t *)(in_x0 + 0x10) == (__locale_t)0x0) {
      uVar3 = 1;
    }
    else {
                    /* try { // try from 00e7b8c8 to 00e7b8cb has its CatchHandler @ 00e7b940 */
      p_Var2 = uselocale(*(__locale_t *)(in_x0 + 0x10));
                    /* try { // try from 00e7b8d0 to 00e7b8d3 has its CatchHandler @ 00e7b90c */
      sVar4 = __ctype_get_mb_cur_max();
      if (p_Var2 != (__locale_t)0x0) {
                    /* try { // try from 00e7b8dc to 00e7b8e3 has its CatchHandler @ 00e7b908 */
        uselocale(p_Var2);
      }
      uVar3 = (ulong)(sVar4 == 1);
    }
  }
  else {
    uVar3 = 0xffffffff;
  }
  return uVar3;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7b94c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_always_noconv() const */

undefined8 std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7b958
// ==========================================================================================

/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_length
          (codecvt<wchar_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  bool bVar1;
  __locale_t __dataset;
  size_t sVar2;
  int iVar3;
  int iVar4;
  ulong uVar5;
  
  if ((param_2 != param_3) && (param_4 != 0)) {
    iVar4 = 0;
    uVar5 = 1;
    while( true ) {
      __dataset = uselocale(*(__locale_t *)(this + 0x10));
                    /* try { // try from 00e7b9b4 to 00e7b9c3 has its CatchHandler @ 00e7ba38 */
      sVar2 = mbrlen(param_2,(long)param_3 - (long)param_2,param_1);
      if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7b9cc to 00e7b9d3 has its CatchHandler @ 00e7ba34 */
        uselocale(__dataset);
      }
      if (sVar2 == 0) {
        sVar2 = 1;
        iVar3 = 1;
      }
      else {
        if (sVar2 + 2 < 2) {
          return iVar4;
        }
        iVar3 = (int)sVar2;
      }
      param_2 = param_2 + sVar2;
      iVar4 = iVar3 + iVar4;
      if (param_2 == param_3) break;
      bVar1 = param_4 <= uVar5;
      uVar5 = uVar5 + 1;
      if (bVar1) {
        return iVar4;
      }
    }
    return iVar4;
  }
  return 0;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7ba54
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<wchar_t, char, mbstate_t>::do_max_length() const */

ulong std::__ndk1::codecvt<wchar_t,char,mbstate_t>::do_max_length(void)

{
  long in_x0;
  __locale_t __dataset;
  size_t sVar1;
  
  if (*(__locale_t *)(in_x0 + 0x10) == (__locale_t)0x0) {
    sVar1 = 1;
  }
  else {
                    /* try { // try from 00e7ba6c to 00e7ba6f has its CatchHandler @ 00e7bac0 */
    __dataset = uselocale(*(__locale_t *)(in_x0 + 0x10));
                    /* try { // try from 00e7ba74 to 00e7ba77 has its CatchHandler @ 00e7baa8 */
    sVar1 = __ctype_get_mb_cur_max();
    if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e7ba80 to 00e7ba87 has its CatchHandler @ 00e7baa4 */
      uselocale(__dataset);
    }
  }
  return sVar1 & 0xffffffff;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7baf8
// ==========================================================================================

/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_out(mbstate_t&, char16_t const*, char16_t
   const*, char16_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_out
          (codecvt<char16_t,char,mbstate_t> *this,mbstate_t *param_1,wchar16 *param_2,
          wchar16 *param_3,wchar16 **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar16 *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7bb90(param_2,param_3,&local_40,param_5,param_6,&local_48,0x10ffff,0);
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7bdb0
// ==========================================================================================

/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char16_t*, char16_t*, char16_t*&) const */

void __thiscall
std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_in
          (codecvt<char16_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar16 *param_5,wchar16 *param_6,wchar16 **param_7)

{
  long lVar1;
  wchar16 *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7be48(param_2,param_3,&local_40,param_5,param_6,&local_48,0x10ffff,0);
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7c0c4
// ==========================================================================================

/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_unshift(mbstate_t&, char*, char*, char*&)
   const */

undefined8 __thiscall
std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_unshift
          (codecvt<char16_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7c0d4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_encoding() const */

undefined8 std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7c0e0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_always_noconv() const */

undefined8 std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7c0ec
// ==========================================================================================

/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

void __thiscall
std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_length
          (codecvt<char16_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c108(param_2,param_3,param_4,0x10ffff,0);
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7c308
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char16_t, char, mbstate_t>::do_max_length() const */

undefined8 std::__ndk1::codecvt<char16_t,char,mbstate_t>::do_max_length(void)

{
  return 4;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7c340
// ==========================================================================================

/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_out(mbstate_t&, char32_t const*, char32_t
   const*, char32_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_out
          (codecvt<char32_t,char,mbstate_t> *this,mbstate_t *param_1,wchar32 *param_2,
          wchar32 *param_3,wchar32 **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar32 *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c3d8(param_2,param_3,&local_40,param_5,param_6,&local_48,0x10ffff,0);
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7c55c
// ==========================================================================================

/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char32_t*, char32_t*, char32_t*&) const */

void __thiscall
std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_in
          (codecvt<char32_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar32 *param_5,wchar32 *param_6,wchar32 **param_7)

{
  long lVar1;
  wchar32 *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c5f4(param_2,param_3,&local_40,param_5,param_6,&local_48,0x10ffff,0);
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7c82c
// ==========================================================================================

/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_unshift(mbstate_t&, char*, char*, char*&)
   const */

undefined8 __thiscall
std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_unshift
          (codecvt<char32_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7c83c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_encoding() const */

undefined8 std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7c848
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_always_noconv() const */

undefined8 std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7c854
// ==========================================================================================

/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

void __thiscall
std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_length
          (codecvt<char32_t,char,mbstate_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c870(param_2,param_3,param_4,0x10ffff,0);
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7ca6c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::codecvt<char32_t, char, mbstate_t>::do_max_length() const */

undefined8 std::__ndk1::codecvt<char32_t,char,mbstate_t>::do_max_length(void)

{
  return 4;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7ca78
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<wchar_t>::do_out(mbstate_t&, wchar_t const*, wchar_t const*, wchar_t
   const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8<wchar_t>::do_out
          (__codecvt_utf8<wchar_t> *this,mbstate_t *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar_t *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c3d8(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x18),
               *(undefined4 *)(this + 0x20));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7cb14
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<wchar_t>::do_in(mbstate_t&, char const*, char const*, char const*&,
   wchar_t*, wchar_t*, wchar_t*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8<wchar_t>::do_in
          (__codecvt_utf8<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar_t *param_5,wchar_t *param_6,wchar_t **param_7)

{
  long lVar1;
  wchar_t *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c5f4(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x18),
               *(undefined4 *)(this + 0x20));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7cbb0
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<wchar_t>::do_unshift(mbstate_t&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8<wchar_t>::do_unshift
          (__codecvt_utf8<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7cbc0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<wchar_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8<wchar_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7cbcc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<wchar_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8<wchar_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7cbd8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<wchar_t>::do_length(mbstate_t&, char const*, char const*, unsigned
   long) const */

void __thiscall
std::__ndk1::__codecvt_utf8<wchar_t>::do_length
          (__codecvt_utf8<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c870(param_2,param_3,param_4,*(undefined8 *)(this + 0x18),*(undefined4 *)(this + 0x20));
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7cbf8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<wchar_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8<wchar_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x20) & 4) != 0) {
    uVar1 = 7;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7cc14
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char16_t>::do_out(mbstate_t&, char16_t const*, char16_t const*,
   char16_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8<char16_t>::do_out
          (__codecvt_utf8<char16_t> *this,mbstate_t *param_1,wchar16 *param_2,wchar16 *param_3,
          wchar16 **param_4,char *param_5,char *param_6,char **param_7)

{
  wchar16 wVar1;
  byte bVar2;
  undefined8 uVar3;
  byte *pbVar4;
  ulong uVar5;
  
  uVar5 = *(ulong *)(this + 0x10);
  pbVar4 = (byte *)param_5;
  if (((byte)this[0x18] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 3) {
LAB_00e7cc30:
      uVar3 = 1;
      pbVar4 = (byte *)param_5;
      goto LAB_00e7cd10;
    }
    *(undefined2 *)param_5 = 0xbbef;
    pbVar4 = (byte *)(param_5 + 3);
    param_5[2] = -0x41;
  }
  if (param_2 < param_3) {
    uVar3 = 2;
    param_5 = (char *)pbVar4;
    do {
      wVar1 = *param_2;
      pbVar4 = (byte *)param_5;
      if (((ushort)wVar1 >> 0xb == 0x1b) || (uVar5 < (ushort)wVar1)) goto LAB_00e7cd10;
      bVar2 = (byte)wVar1;
      if ((ushort)wVar1 < 0x80) {
        if ((long)param_6 - (long)param_5 < 1) goto LAB_00e7cc30;
        pbVar4 = (byte *)param_5 + 1;
        *param_5 = bVar2;
      }
      else if ((ushort)wVar1 < 0x800) {
        if ((long)param_6 - (long)param_5 < 2) goto LAB_00e7cc30;
        *param_5 = (byte)((ushort)wVar1 >> 6) | 0xc0;
        pbVar4 = (byte *)param_5 + 2;
        ((byte *)param_5)[1] = bVar2 & 0x3f | 0x80;
      }
      else {
        if ((long)param_6 - (long)param_5 < 3) goto LAB_00e7cc30;
        pbVar4 = (byte *)param_5 + 3;
        *param_5 = (byte)((ushort)wVar1 >> 0xc) | 0xe0;
        ((byte *)param_5)[1] = (byte)((ushort)wVar1 >> 6) & 0x3f | 0x80;
        ((byte *)param_5)[2] = bVar2 & 0x3f | 0x80;
      }
      param_2 = param_2 + 1;
      param_5 = (char *)pbVar4;
    } while (param_2 < param_3);
  }
  uVar3 = 0;
LAB_00e7cd10:
  *param_4 = param_2;
  *param_7 = (char *)pbVar4;
  return uVar3;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7cd1c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char16_t>::do_in(mbstate_t&, char const*, char const*, char const*&,
   char16_t*, char16_t*, char16_t*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8<char16_t>::do_in
          (__codecvt_utf8<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar16 *param_5,wchar16 *param_6,wchar16 **param_7)

{
  ulong uVar1;
  ulong uVar2;
  byte bVar3;
  byte bVar4;
  undefined8 uVar5;
  byte *pbVar6;
  ulong uVar7;
  ulong uVar8;
  ulong uVar9;
  wchar16 *pwVar10;
  long lVar11;
  
  pbVar6 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (2 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -0x11)) &&
     ((param_2[1] == -0x45 && (pbVar6 = (byte *)(param_2 + 3), param_2[2] != -0x41)))) {
    pbVar6 = (byte *)param_2;
  }
  if (pbVar6 < param_3) {
    if (param_5 < param_6) {
      uVar7 = *(ulong *)(this + 0x10);
      do {
        bVar4 = *pbVar6;
        uVar8 = (ulong)bVar4;
        if ((char)bVar4 < '\0') {
          if (0xc1 < bVar4) {
            if (bVar4 < 0xe0) {
              if ((long)param_3 - (long)pbVar6 < 2) goto LAB_00e7ce8c;
              if (((pbVar6[1] & 0xc0) == 0x80) &&
                 (uVar8 = ((ulong)bVar4 & 0x1f) << 6 | (ulong)pbVar6[1] & 0x3f, uVar8 <= uVar7)) {
                lVar11 = 2;
                goto LAB_00e7ce58;
              }
            }
            else if (bVar4 < 0xf0) {
              if ((long)param_3 - (long)pbVar6 < 3) goto LAB_00e7ce8c;
              bVar3 = pbVar6[1];
              if (bVar4 == 0xed) {
                bVar4 = bVar3 & 0xe0;
joined_r0x00e7ce1c:
                if (bVar4 != 0x80) goto LAB_00e7ce94;
              }
              else {
                if (bVar4 != 0xe0) {
                  bVar4 = bVar3 & 0xc0;
                  goto joined_r0x00e7ce1c;
                }
                if ((bVar3 & 0xe0) != 0xa0) goto LAB_00e7ce94;
              }
              if (((pbVar6[2] & 0xc0) == 0x80) &&
                 (uVar9 = uVar8 << 0xc, uVar1 = ((ulong)bVar3 & 0x3f) << 6,
                 uVar2 = (ulong)pbVar6[2] & 0x3f, uVar8 = uVar9 | uVar1 | uVar2,
                 (uVar9 & 0xffc0 | uVar1 | uVar2) <= uVar7)) {
                lVar11 = 3;
                goto LAB_00e7ce58;
              }
            }
          }
LAB_00e7ce94:
          uVar5 = 2;
          goto LAB_00e7cea4;
        }
        if (uVar7 < uVar8) goto LAB_00e7ce94;
        lVar11 = 1;
LAB_00e7ce58:
        pbVar6 = pbVar6 + lVar11;
        pwVar10 = param_5 + 1;
        *param_5 = (wchar16)uVar8;
        if (param_3 <= pbVar6) {
          uVar5 = 0;
          param_5 = param_5 + 1;
          goto LAB_00e7cea4;
        }
        param_5 = pwVar10;
      } while (pwVar10 < param_6);
      uVar5 = 1;
    }
    else {
LAB_00e7ce8c:
      uVar5 = 1;
    }
  }
  else {
    uVar5 = 0;
  }
LAB_00e7cea4:
  *param_4 = (char *)pbVar6;
  *param_7 = param_5;
  return uVar5;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7ceb0
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char16_t>::do_unshift(mbstate_t&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8<char16_t>::do_unshift
          (__codecvt_utf8<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7cec0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char16_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8<char16_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7cecc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char16_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8<char16_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7ced8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char16_t>::do_length(mbstate_t&, char const*, char const*, unsigned
   long) const */

int __thiscall
std::__ndk1::__codecvt_utf8<char16_t>::do_length
          (__codecvt_utf8<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  byte bVar1;
  byte bVar2;
  byte *pbVar3;
  ulong uVar4;
  ulong uVar5;
  long lVar6;
  byte bVar7;
  
  pbVar3 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (2 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -0x11)) &&
     ((param_2[1] == -0x45 && (pbVar3 = (byte *)(param_2 + 3), param_2[2] != -0x41)))) {
    pbVar3 = (byte *)param_2;
  }
  if ((param_4 != 0) && (pbVar3 < param_3)) {
    uVar4 = *(ulong *)(this + 0x10);
    uVar5 = 1;
    do {
      bVar2 = *pbVar3;
      if ((char)bVar2 < '\0') {
        if (bVar2 < 0xc2) break;
        if (bVar2 < 0xe0) {
          if ((((long)param_3 - (long)pbVar3 < 2) || ((pbVar3[1] & 0xc0) != 0x80)) ||
             (uVar4 < (((ulong)bVar2 & 0x1f) << 6 | (ulong)pbVar3[1] & 0x3f))) break;
          lVar6 = 2;
        }
        else {
          if ((0xef < bVar2) || ((long)param_3 - (long)pbVar3 < 3)) break;
          bVar1 = pbVar3[1];
          if (bVar2 == 0xed) {
            bVar7 = bVar1 & 0xe0;
LAB_00e7cfec:
            if (bVar7 != 0x80) break;
          }
          else {
            if (bVar2 != 0xe0) {
              bVar7 = bVar1 & 0xc0;
              goto LAB_00e7cfec;
            }
            if ((bVar1 & 0xe0) != 0xa0) break;
          }
          if (((pbVar3[2] & 0xc0) != 0x80) ||
             (uVar4 < (((ulong)bVar2 & 0xf) << 0xc | ((ulong)bVar1 & 0x3f) << 6 |
                      (ulong)pbVar3[2] & 0x3f))) break;
          lVar6 = 3;
        }
      }
      else {
        if (uVar4 < bVar2) break;
        lVar6 = 1;
      }
      pbVar3 = pbVar3 + lVar6;
      if ((param_4 <= uVar5) || (uVar5 = uVar5 + 1, param_3 <= pbVar3)) break;
    } while( true );
  }
  return (int)pbVar3 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7d040
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char16_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8<char16_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 3;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 6;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7d05c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char32_t>::do_out(mbstate_t&, char32_t const*, char32_t const*,
   char32_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8<char32_t>::do_out
          (__codecvt_utf8<char32_t> *this,mbstate_t *param_1,wchar32 *param_2,wchar32 *param_3,
          wchar32 **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar32 *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c3d8(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7d0f8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char32_t>::do_in(mbstate_t&, char const*, char const*, char const*&,
   char32_t*, char32_t*, char32_t*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8<char32_t>::do_in
          (__codecvt_utf8<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar32 *param_5,wchar32 *param_6,wchar32 **param_7)

{
  long lVar1;
  wchar32 *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7c5f4(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7d194
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char32_t>::do_unshift(mbstate_t&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8<char32_t>::do_unshift
          (__codecvt_utf8<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7d1a4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char32_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8<char32_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7d1b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char32_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8<char32_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7d1bc
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char32_t>::do_length(mbstate_t&, char const*, char const*, unsigned
   long) const */

void __thiscall
std::__ndk1::__codecvt_utf8<char32_t>::do_length
          (__codecvt_utf8<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c870(param_2,param_3,param_4,*(undefined8 *)(this + 0x10),*(undefined4 *)(this + 0x18));
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7d1dc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8<char32_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8<char32_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 7;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7d1f8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_out(mbstate_t&, wchar_t const*, wchar_t const*,
   wchar_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,false>::do_out
          (__codecvt_utf16<wchar_t,false> *this,mbstate_t *param_1,wchar_t *param_2,wchar_t *param_3
          ,wchar_t **param_4,char *param_5,char *param_6,char **param_7)

{
  int iVar1;
  wchar_t wVar2;
  byte bVar3;
  undefined8 uVar4;
  ulong uVar5;
  byte *pbVar6;
  long lVar7;
  
  uVar5 = *(ulong *)(this + 0x18);
  if (((byte)this[0x20] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7d214:
      uVar4 = 1;
      goto LAB_00e7d2d0;
    }
    *(undefined2 *)param_5 = 0xfffe;
    param_5 = param_5 + 2;
  }
  if (param_2 < param_3) {
    uVar4 = 2;
    do {
      wVar2 = *param_2;
      if (((uint)wVar2 >> 0xb == 0x1b) || (uVar5 < (uint)wVar2)) goto LAB_00e7d2d0;
      bVar3 = (byte)((uint)wVar2 >> 8);
      if ((uint)wVar2 >> 0x10 == 0) {
        if ((long)param_6 - (long)param_5 < 2) goto LAB_00e7d214;
        pbVar6 = (byte *)param_5 + 1;
        *param_5 = bVar3;
        lVar7 = 2;
      }
      else {
        if ((long)param_6 - (long)param_5 < 4) goto LAB_00e7d214;
        iVar1 = ((uint)wVar2 >> 10 & 0x7c0) + 0x3fc0;
        ((byte *)param_5)[2] = bVar3 & 3 | 0xdc;
        pbVar6 = (byte *)param_5 + 3;
        ((byte *)param_5)[1] = (byte)iVar1 | (byte)((uint)wVar2 >> 10) & 0x3f;
        lVar7 = 4;
        *param_5 = (byte)((uint)iVar1 >> 8) | 0xd8;
      }
      param_2 = param_2 + 1;
      param_5 = (char *)((byte *)param_5 + lVar7);
      *pbVar6 = (byte)wVar2;
    } while (param_2 < param_3);
  }
  uVar4 = 0;
LAB_00e7d2d0:
  *param_4 = param_2;
  *param_7 = param_5;
  return uVar4;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7d2dc
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_in(mbstate_t&, char const*, char const*, char
   const*&, wchar_t*, wchar_t*, wchar_t*&) const */

ulong __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,false>::do_in
          (__codecvt_utf16<wchar_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar_t *param_5,wchar_t *param_6,wchar_t **param_7)

{
  byte bVar1;
  ushort uVar2;
  ulong uVar3;
  byte *pbVar4;
  wchar_t *pwVar5;
  ulong uVar6;
  ulong uVar7;
  
  pbVar4 = (byte *)param_2;
  if ((((((byte)this[0x20] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar4 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar4 = (byte *)param_2;
  }
  if (pbVar4 < param_3 + -1) {
    uVar6 = *(ulong *)(this + 0x18);
    pwVar5 = param_5;
    do {
      param_5 = pwVar5;
      if (param_6 <= pwVar5) break;
      bVar1 = *pbVar4 & 0xfc;
      uVar2 = CONCAT11(*pbVar4,pbVar4[1]);
      uVar7 = (ulong)uVar2;
      if (bVar1 == 0xd8) {
        if ((long)param_3 - (long)pbVar4 < 4) {
          uVar3 = 1;
          goto LAB_00e7d3cc;
        }
        if (((pbVar4[2] & 0xfc) != 0xdc) ||
           (uVar7 = (((ulong)uVar2 & 0x3ff) << 10 | ((ulong)pbVar4[2] & 3) << 8 | (ulong)pbVar4[3])
                    + 0x10000, uVar6 < uVar7)) goto LAB_00e7d3d8;
        uVar3 = 4;
      }
      else {
        if (bVar1 == 0xdc) {
LAB_00e7d3d8:
          uVar3 = 2;
          goto LAB_00e7d3cc;
        }
        uVar3 = 2;
        if (uVar6 < uVar7) goto LAB_00e7d3cc;
      }
      pbVar4 = pbVar4 + uVar3;
      param_5 = pwVar5 + 1;
      *pwVar5 = (wchar_t)uVar7;
      pwVar5 = param_5;
    } while (pbVar4 < param_3 + -1);
  }
  uVar3 = (ulong)(pbVar4 < param_3);
  pwVar5 = param_5;
LAB_00e7d3cc:
  *param_4 = (char *)pbVar4;
  *param_7 = pwVar5;
  return uVar3;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7d3e8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,false>::do_unshift
          (__codecvt_utf16<wchar_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7d3f8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<wchar_t,false>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7d404
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<wchar_t,false>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7d410
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,false>::do_length
          (__codecvt_utf16<wchar_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  byte bVar1;
  ushort uVar2;
  byte *pbVar3;
  ulong uVar4;
  
  pbVar3 = (byte *)param_2;
  if ((((((byte)this[0x20] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar3 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar3 = (byte *)param_2;
  }
  if ((param_4 != 0) && (pbVar3 < param_3 + -1)) {
    uVar4 = 1;
    do {
      bVar1 = *pbVar3 & 0xfc;
      uVar2 = CONCAT11(*pbVar3,pbVar3[1]);
      if (bVar1 == 0xd8) {
        if ((((long)param_3 - (long)pbVar3 < 4) || ((pbVar3[2] & 0xfc) != 0xdc)) ||
           (*(ulong *)(this + 0x18) <
            (((ulong)uVar2 & 0x3ff) << 10 | ((ulong)pbVar3[2] & 3) << 8 | (ulong)pbVar3[3]) +
            0x10000)) break;
        pbVar3 = pbVar3 + 4;
      }
      else {
        if ((bVar1 == 0xdc) || (*(ulong *)(this + 0x18) < (ulong)uVar2)) break;
        pbVar3 = pbVar3 + 2;
      }
      if ((param_4 <= uVar4) || (uVar4 = uVar4 + 1, param_3 + -1 <= pbVar3)) break;
    } while( true );
  }
  return (int)pbVar3 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7d510
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, false>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<wchar_t,false>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x20) & 4) != 0) {
    uVar1 = 6;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7d52c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_out(mbstate_t&, wchar_t const*, wchar_t const*,
   wchar_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,true>::do_out
          (__codecvt_utf16<wchar_t,true> *this,mbstate_t *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t **param_4,char *param_5,char *param_6,char **param_7)

{
  int iVar1;
  wchar_t wVar2;
  undefined8 uVar3;
  undefined2 *puVar4;
  ulong uVar5;
  
  uVar5 = *(ulong *)(this + 0x18);
  puVar4 = (undefined2 *)param_5;
  if (((byte)this[0x20] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7d548:
      uVar3 = 1;
      puVar4 = (undefined2 *)param_5;
      goto LAB_00e7d5f4;
    }
    puVar4 = (undefined2 *)(param_5 + 2);
    *(undefined2 *)param_5 = 0xfeff;
  }
  if (param_2 < param_3) {
    uVar3 = 2;
    param_5 = (char *)puVar4;
    do {
      wVar2 = *param_2;
      puVar4 = (undefined2 *)param_5;
      if (((uint)wVar2 >> 0xb == 0x1b) || (uVar5 < (uint)wVar2)) goto LAB_00e7d5f4;
      if ((wVar2 & 0xffff0000U) == 0) {
        if ((long)param_6 - (long)param_5 < 2) goto LAB_00e7d548;
        puVar4 = (undefined2 *)((long)param_5 + 2);
        *(short *)param_5 = (short)wVar2;
      }
      else {
        if ((long)param_6 - (long)param_5 < 4) goto LAB_00e7d548;
        iVar1 = ((uint)wVar2 >> 10 & 0x7c0) + 0x3fc0;
        *(byte *)((long)param_5 + 2) = (byte)wVar2;
        puVar4 = (undefined2 *)((long)param_5 + 4);
        *param_5 = (byte)iVar1 | (byte)((uint)wVar2 >> 10) & 0x3f;
        *(byte *)((long)param_5 + 1) = (byte)((uint)iVar1 >> 8) | 0xd8;
        *(byte *)((long)param_5 + 3) = (byte)((uint)wVar2 >> 8) & 3 | 0xdc;
      }
      param_2 = param_2 + 1;
      param_5 = (char *)puVar4;
    } while (param_2 < param_3);
  }
  uVar3 = 0;
LAB_00e7d5f4:
  *param_4 = param_2;
  *param_7 = (char *)puVar4;
  return uVar3;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7d600
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_in(mbstate_t&, char const*, char const*, char
   const*&, wchar_t*, wchar_t*, wchar_t*&) const */

ulong __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,true>::do_in
          (__codecvt_utf16<wchar_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar_t *param_5,wchar_t *param_6,wchar_t **param_7)

{
  byte bVar1;
  ulong uVar2;
  ushort *puVar3;
  wchar_t *pwVar4;
  ulong uVar5;
  ulong uVar6;
  
  puVar3 = (ushort *)param_2;
  if ((((((byte)this[0x20] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (puVar3 = (ushort *)(param_2 + 2), param_2[1] != -2)) {
    puVar3 = (ushort *)param_2;
  }
  if (puVar3 < param_3 + -1) {
    uVar5 = *(ulong *)(this + 0x18);
    pwVar4 = param_5;
    do {
      param_5 = pwVar4;
      if (param_6 <= pwVar4) break;
      bVar1 = *(byte *)((long)puVar3 + 1) & 0xfc;
      uVar6 = (ulong)*puVar3;
      if (bVar1 == 0xd8) {
        if ((long)param_3 - (long)puVar3 < 4) {
          uVar2 = 1;
          goto LAB_00e7d6f0;
        }
        if (((*(byte *)((long)puVar3 + 3) & 0xfc) != 0xdc) ||
           (uVar6 = (((ulong)*puVar3 & 0x3ff) << 10 |
                    ((ulong)*(byte *)((long)puVar3 + 3) & 3) << 8 | (ulong)*(byte *)(puVar3 + 1)) +
                    0x10000, uVar5 < uVar6)) goto LAB_00e7d6fc;
        uVar2 = 4;
      }
      else {
        if (bVar1 == 0xdc) {
LAB_00e7d6fc:
          uVar2 = 2;
          goto LAB_00e7d6f0;
        }
        uVar2 = 2;
        if (uVar5 < uVar6) goto LAB_00e7d6f0;
      }
      puVar3 = (ushort *)((long)puVar3 + uVar2);
      param_5 = pwVar4 + 1;
      *pwVar4 = (wchar_t)uVar6;
      pwVar4 = param_5;
    } while (puVar3 < param_3 + -1);
  }
  uVar2 = (ulong)(puVar3 < param_3);
  pwVar4 = param_5;
LAB_00e7d6f0:
  *param_4 = (char *)puVar3;
  *param_7 = pwVar4;
  return uVar2;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7d70c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,true>::do_unshift
          (__codecvt_utf16<wchar_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7d71c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<wchar_t,true>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7d728
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<wchar_t,true>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7d734
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,true>::do_length
          (__codecvt_utf16<wchar_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  byte bVar1;
  ushort *puVar2;
  ulong uVar3;
  
  puVar2 = (ushort *)param_2;
  if ((((((byte)this[0x20] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (puVar2 = (ushort *)(param_2 + 2), param_2[1] != -2)) {
    puVar2 = (ushort *)param_2;
  }
  if ((param_4 != 0) && (puVar2 < param_3 + -1)) {
    uVar3 = 1;
    do {
      bVar1 = *(byte *)((long)puVar2 + 1) & 0xfc;
      if (bVar1 == 0xd8) {
        if ((((long)param_3 - (long)puVar2 < 4) || ((*(byte *)((long)puVar2 + 3) & 0xfc) != 0xdc))
           || (*(ulong *)(this + 0x18) <
               (((ulong)*puVar2 & 0x3ff) << 10 |
               ((ulong)*(byte *)((long)puVar2 + 3) & 3) << 8 | (ulong)*(byte *)(puVar2 + 1)) +
               0x10000)) break;
        puVar2 = puVar2 + 2;
      }
      else {
        if ((bVar1 == 0xdc) || (*(ulong *)(this + 0x18) < (ulong)*puVar2)) break;
        puVar2 = puVar2 + 1;
      }
      if ((param_4 <= uVar3) || (uVar3 = uVar3 + 1, param_3 + -1 <= puVar2)) break;
    } while( true );
  }
  return (int)puVar2 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7d834
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<wchar_t, true>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<wchar_t,true>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x20) & 4) != 0) {
    uVar1 = 6;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7d850
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_out(mbstate_t&, char16_t const*, char16_t
   const*, char16_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char16_t,false>::do_out
          (__codecvt_utf16<char16_t,false> *this,mbstate_t *param_1,wchar16 *param_2,
          wchar16 *param_3,wchar16 **param_4,char *param_5,char *param_6,char **param_7)

{
  wchar16 wVar1;
  undefined8 uVar2;
  ushort *puVar3;
  ulong uVar4;
  long lVar5;
  
  uVar4 = *(ulong *)(this + 0x10);
  puVar3 = (ushort *)param_5;
  if (((byte)this[0x18] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7d86c:
      uVar2 = 1;
      puVar3 = (ushort *)param_5;
      goto LAB_00e7d8c4;
    }
    puVar3 = (ushort *)(param_5 + 2);
    *(undefined2 *)param_5 = 0xfffe;
  }
  if (param_2 < param_3) {
    uVar2 = 2;
    param_5 = (char *)puVar3;
    lVar5 = (long)param_6 - (long)puVar3;
    do {
      wVar1 = *param_2;
      puVar3 = (ushort *)param_5;
      if (((ushort)wVar1 >> 0xb == 0x1b) || (uVar4 < (ushort)wVar1)) goto LAB_00e7d8c4;
      if (lVar5 < 2) goto LAB_00e7d86c;
      param_2 = param_2 + 1;
      puVar3 = (ushort *)((long)param_5 + 2);
      *(ushort *)param_5 = (ushort)wVar1 >> 8 | (ushort)(((ushort)wVar1 & 0xff00ff) << 8);
      param_5 = (char *)puVar3;
      lVar5 = lVar5 + -2;
    } while (param_2 < param_3);
  }
  uVar2 = 0;
LAB_00e7d8c4:
  *param_4 = param_2;
  *param_7 = (char *)puVar3;
  return uVar2;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7d8d0
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char16_t*, char16_t*, char16_t*&) const */

undefined __thiscall
std::__ndk1::__codecvt_utf16<char16_t,false>::do_in
          (__codecvt_utf16<char16_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar16 *param_5,wchar16 *param_6,wchar16 **param_7)

{
  wchar16 wVar1;
  undefined uVar2;
  byte *pbVar3;
  wchar16 *pwVar4;
  ulong uVar5;
  
  pbVar3 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar3 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar3 = (byte *)param_2;
  }
  if (pbVar3 < param_3 + -1) {
    uVar5 = *(ulong *)(this + 0x10);
    uVar2 = 2;
    pwVar4 = param_5;
    while (param_5 = pwVar4, pwVar4 < param_6) {
      if (((*pbVar3 & 0xf8) == 0xd8) || (wVar1 = CONCAT11(*pbVar3,pbVar3[1]), uVar5 < (ushort)wVar1)
         ) goto LAB_00e7d958;
      pbVar3 = pbVar3 + 2;
      param_5 = pwVar4 + 1;
      *pwVar4 = wVar1;
      pwVar4 = param_5;
      if (param_3 + -1 <= pbVar3) break;
    }
  }
  uVar2 = pbVar3 < param_3;
LAB_00e7d958:
  *param_4 = (char *)pbVar3;
  *param_7 = param_5;
  return uVar2;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7d964
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char16_t,false>::do_unshift
          (__codecvt_utf16<char16_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7d974
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<char16_t,false>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7d980
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<char16_t,false>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7d98c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<char16_t,false>::do_length
          (__codecvt_utf16<char16_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  bool bVar1;
  byte *pbVar2;
  ulong uVar3;
  
  pbVar2 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar2 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar2 = (byte *)param_2;
  }
  if ((param_4 != 0) && (pbVar2 < param_3 + -1)) {
    uVar3 = 1;
    while (((*pbVar2 & 0xf8) != 0xd8 &&
           ((ulong)CONCAT11(*pbVar2,pbVar2[1]) <= *(ulong *)(this + 0x10)))) {
      pbVar2 = pbVar2 + 2;
      if ((param_3 + -1 <= pbVar2) || (bVar1 = param_4 <= uVar3, uVar3 = uVar3 + 1, bVar1)) break;
    }
  }
  return (int)pbVar2 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7da24
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, false>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<char16_t,false>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 2;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 4;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7da40
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_out(mbstate_t&, char16_t const*, char16_t
   const*, char16_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char16_t,true>::do_out
          (__codecvt_utf16<char16_t,true> *this,mbstate_t *param_1,wchar16 *param_2,wchar16 *param_3
          ,wchar16 **param_4,char *param_5,char *param_6,char **param_7)

{
  wchar16 wVar1;
  undefined8 uVar2;
  wchar16 *pwVar3;
  ulong uVar4;
  long lVar5;
  
  uVar4 = *(ulong *)(this + 0x10);
  pwVar3 = (wchar16 *)param_5;
  if (((byte)this[0x18] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7da5c:
      uVar2 = 1;
      pwVar3 = (wchar16 *)param_5;
      goto LAB_00e7dab0;
    }
    pwVar3 = (wchar16 *)(param_5 + 2);
    *(undefined2 *)param_5 = 0xfeff;
  }
  if (param_2 < param_3) {
    uVar2 = 2;
    param_5 = (char *)pwVar3;
    lVar5 = (long)param_6 - (long)pwVar3;
    do {
      wVar1 = *param_2;
      pwVar3 = (wchar16 *)param_5;
      if (((ushort)wVar1 >> 0xb == 0x1b) || (uVar4 < (ushort)wVar1)) goto LAB_00e7dab0;
      if (lVar5 < 2) goto LAB_00e7da5c;
      param_2 = param_2 + 1;
      pwVar3 = (wchar16 *)((long)param_5 + 2);
      *(wchar16 *)param_5 = wVar1;
      param_5 = (char *)pwVar3;
      lVar5 = lVar5 + -2;
    } while (param_2 < param_3);
  }
  uVar2 = 0;
LAB_00e7dab0:
  *param_4 = param_2;
  *param_7 = (char *)pwVar3;
  return uVar2;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7dabc
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char16_t*, char16_t*, char16_t*&) const */

undefined __thiscall
std::__ndk1::__codecvt_utf16<char16_t,true>::do_in
          (__codecvt_utf16<char16_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar16 *param_5,wchar16 *param_6,wchar16 **param_7)

{
  wchar16 wVar1;
  undefined uVar2;
  char *pcVar3;
  wchar16 *pwVar4;
  ulong uVar5;
  
  pcVar3 = param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (pcVar3 = param_2 + 2, param_2[1] != -2)) {
    pcVar3 = param_2;
  }
  if (pcVar3 < param_3 + -1) {
    uVar5 = *(ulong *)(this + 0x10);
    uVar2 = 2;
    pwVar4 = param_5;
    while (param_5 = pwVar4, pwVar4 < param_6) {
      if (((pcVar3[1] & 0xf8U) == 0xd8) ||
         (wVar1 = CONCAT11(pcVar3[1],*pcVar3), uVar5 < (ushort)wVar1)) goto LAB_00e7db44;
      pcVar3 = pcVar3 + 2;
      param_5 = pwVar4 + 1;
      *pwVar4 = wVar1;
      pwVar4 = param_5;
      if (param_3 + -1 <= pcVar3) break;
    }
  }
  uVar2 = pcVar3 < param_3;
LAB_00e7db44:
  *param_4 = pcVar3;
  *param_7 = param_5;
  return uVar2;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7db50
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char16_t,true>::do_unshift
          (__codecvt_utf16<char16_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7db60
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<char16_t,true>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7db6c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<char16_t,true>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7db78
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<char16_t,true>::do_length
          (__codecvt_utf16<char16_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  bool bVar1;
  char *pcVar2;
  ulong uVar3;
  char *pcVar4;
  
  pcVar2 = param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (pcVar2 = param_2 + 2, param_2[1] != -2)) {
    pcVar2 = param_2;
  }
  if ((param_4 != 0) && (pcVar2 < param_3 + -1)) {
    uVar3 = 1;
    do {
      if (((pcVar2[1] & 0xf8U) == 0xd8) ||
         (pcVar4 = pcVar2 + 2, *(ulong *)(this + 0x10) < (ulong)CONCAT11(pcVar2[1],*pcVar2))) break;
      if (param_3 + -1 <= pcVar4) {
        return (int)pcVar4 - (int)param_2;
      }
      bVar1 = uVar3 < param_4;
      uVar3 = uVar3 + 1;
      pcVar2 = pcVar4;
    } while (bVar1);
  }
  return (int)pcVar2 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7dc28
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char16_t, true>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<char16_t,true>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 2;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 4;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7dc44
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_out(mbstate_t&, char32_t const*, char32_t
   const*, char32_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char32_t,false>::do_out
          (__codecvt_utf16<char32_t,false> *this,mbstate_t *param_1,wchar32 *param_2,
          wchar32 *param_3,wchar32 **param_4,char *param_5,char *param_6,char **param_7)

{
  int iVar1;
  wchar32 wVar2;
  byte bVar3;
  undefined8 uVar4;
  ulong uVar5;
  byte *pbVar6;
  long lVar7;
  
  uVar5 = *(ulong *)(this + 0x10);
  if (((byte)this[0x18] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7dc60:
      uVar4 = 1;
      goto LAB_00e7dd1c;
    }
    *(undefined2 *)param_5 = 0xfffe;
    param_5 = param_5 + 2;
  }
  if (param_2 < param_3) {
    uVar4 = 2;
    do {
      wVar2 = *param_2;
      if (((uint)wVar2 >> 0xb == 0x1b) || (uVar5 < (uint)wVar2)) goto LAB_00e7dd1c;
      bVar3 = (byte)((uint)wVar2 >> 8);
      if ((uint)wVar2 >> 0x10 == 0) {
        if ((long)param_6 - (long)param_5 < 2) goto LAB_00e7dc60;
        pbVar6 = (byte *)param_5 + 1;
        *param_5 = bVar3;
        lVar7 = 2;
      }
      else {
        if ((long)param_6 - (long)param_5 < 4) goto LAB_00e7dc60;
        iVar1 = ((uint)wVar2 >> 10 & 0x7c0) + 0x3fc0;
        ((byte *)param_5)[2] = bVar3 & 3 | 0xdc;
        pbVar6 = (byte *)param_5 + 3;
        ((byte *)param_5)[1] = (byte)iVar1 | (byte)((uint)wVar2 >> 10) & 0x3f;
        lVar7 = 4;
        *param_5 = (byte)((uint)iVar1 >> 8) | 0xd8;
      }
      param_2 = param_2 + 1;
      param_5 = (char *)((byte *)param_5 + lVar7);
      *pbVar6 = (byte)wVar2;
    } while (param_2 < param_3);
  }
  uVar4 = 0;
LAB_00e7dd1c:
  *param_4 = param_2;
  *param_7 = param_5;
  return uVar4;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7dd28
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char32_t*, char32_t*, char32_t*&) const */

ulong __thiscall
std::__ndk1::__codecvt_utf16<char32_t,false>::do_in
          (__codecvt_utf16<char32_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar32 *param_5,wchar32 *param_6,wchar32 **param_7)

{
  byte bVar1;
  ushort uVar2;
  ulong uVar3;
  byte *pbVar4;
  wchar32 *pwVar5;
  ulong uVar6;
  ulong uVar7;
  
  pbVar4 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar4 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar4 = (byte *)param_2;
  }
  if (pbVar4 < param_3 + -1) {
    uVar6 = *(ulong *)(this + 0x10);
    pwVar5 = param_5;
    do {
      param_5 = pwVar5;
      if (param_6 <= pwVar5) break;
      bVar1 = *pbVar4 & 0xfc;
      uVar2 = CONCAT11(*pbVar4,pbVar4[1]);
      uVar7 = (ulong)uVar2;
      if (bVar1 == 0xd8) {
        if ((long)param_3 - (long)pbVar4 < 4) {
          uVar3 = 1;
          goto LAB_00e7de18;
        }
        if (((pbVar4[2] & 0xfc) != 0xdc) ||
           (uVar7 = (((ulong)uVar2 & 0x3ff) << 10 | ((ulong)pbVar4[2] & 3) << 8 | (ulong)pbVar4[3])
                    + 0x10000, uVar6 < uVar7)) goto LAB_00e7de24;
        uVar3 = 4;
      }
      else {
        if (bVar1 == 0xdc) {
LAB_00e7de24:
          uVar3 = 2;
          goto LAB_00e7de18;
        }
        uVar3 = 2;
        if (uVar6 < uVar7) goto LAB_00e7de18;
      }
      pbVar4 = pbVar4 + uVar3;
      param_5 = pwVar5 + 1;
      *pwVar5 = (wchar32)uVar7;
      pwVar5 = param_5;
    } while (pbVar4 < param_3 + -1);
  }
  uVar3 = (ulong)(pbVar4 < param_3);
  pwVar5 = param_5;
LAB_00e7de18:
  *param_4 = (char *)pbVar4;
  *param_7 = pwVar5;
  return uVar3;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7de34
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char32_t,false>::do_unshift
          (__codecvt_utf16<char32_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7de44
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<char32_t,false>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7de50
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<char32_t,false>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7de5c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<char32_t,false>::do_length
          (__codecvt_utf16<char32_t,false> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  byte bVar1;
  ushort uVar2;
  byte *pbVar3;
  ulong uVar4;
  
  pbVar3 = (byte *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -2)) && (pbVar3 = (byte *)(param_2 + 2), param_2[1] != -1)) {
    pbVar3 = (byte *)param_2;
  }
  if ((param_4 != 0) && (pbVar3 < param_3 + -1)) {
    uVar4 = 1;
    do {
      bVar1 = *pbVar3 & 0xfc;
      uVar2 = CONCAT11(*pbVar3,pbVar3[1]);
      if (bVar1 == 0xd8) {
        if ((((long)param_3 - (long)pbVar3 < 4) || ((pbVar3[2] & 0xfc) != 0xdc)) ||
           (*(ulong *)(this + 0x10) <
            (((ulong)uVar2 & 0x3ff) << 10 | ((ulong)pbVar3[2] & 3) << 8 | (ulong)pbVar3[3]) +
            0x10000)) break;
        pbVar3 = pbVar3 + 4;
      }
      else {
        if ((bVar1 == 0xdc) || (*(ulong *)(this + 0x10) < (ulong)uVar2)) break;
        pbVar3 = pbVar3 + 2;
      }
      if ((param_4 <= uVar4) || (uVar4 = uVar4 + 1, param_3 + -1 <= pbVar3)) break;
    } while( true );
  }
  return (int)pbVar3 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7df5c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, false>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<char32_t,false>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 6;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7df78
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_out(mbstate_t&, char32_t const*, char32_t
   const*, char32_t const*&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char32_t,true>::do_out
          (__codecvt_utf16<char32_t,true> *this,mbstate_t *param_1,wchar32 *param_2,wchar32 *param_3
          ,wchar32 **param_4,char *param_5,char *param_6,char **param_7)

{
  int iVar1;
  wchar32 wVar2;
  undefined8 uVar3;
  undefined2 *puVar4;
  ulong uVar5;
  
  uVar5 = *(ulong *)(this + 0x10);
  puVar4 = (undefined2 *)param_5;
  if (((byte)this[0x18] >> 1 & 1) != 0) {
    if ((long)param_6 - (long)param_5 < 2) {
LAB_00e7df94:
      uVar3 = 1;
      puVar4 = (undefined2 *)param_5;
      goto LAB_00e7e040;
    }
    puVar4 = (undefined2 *)(param_5 + 2);
    *(undefined2 *)param_5 = 0xfeff;
  }
  if (param_2 < param_3) {
    uVar3 = 2;
    param_5 = (char *)puVar4;
    do {
      wVar2 = *param_2;
      puVar4 = (undefined2 *)param_5;
      if (((uint)wVar2 >> 0xb == 0x1b) || (uVar5 < (uint)wVar2)) goto LAB_00e7e040;
      if ((wVar2 & 0xffff0000U) == 0) {
        if ((long)param_6 - (long)param_5 < 2) goto LAB_00e7df94;
        puVar4 = (undefined2 *)((long)param_5 + 2);
        *(short *)param_5 = (short)wVar2;
      }
      else {
        if ((long)param_6 - (long)param_5 < 4) goto LAB_00e7df94;
        iVar1 = ((uint)wVar2 >> 10 & 0x7c0) + 0x3fc0;
        *(byte *)((long)param_5 + 2) = (byte)wVar2;
        puVar4 = (undefined2 *)((long)param_5 + 4);
        *param_5 = (byte)iVar1 | (byte)((uint)wVar2 >> 10) & 0x3f;
        *(byte *)((long)param_5 + 1) = (byte)((uint)iVar1 >> 8) | 0xd8;
        *(byte *)((long)param_5 + 3) = (byte)((uint)wVar2 >> 8) & 3 | 0xdc;
      }
      param_2 = param_2 + 1;
      param_5 = (char *)puVar4;
    } while (param_2 < param_3);
  }
  uVar3 = 0;
LAB_00e7e040:
  *param_4 = param_2;
  *param_7 = (char *)puVar4;
  return uVar3;
}



// ==========================================================================================
// Function: do_in
// Address: 00e7e04c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char32_t*, char32_t*, char32_t*&) const */

ulong __thiscall
std::__ndk1::__codecvt_utf16<char32_t,true>::do_in
          (__codecvt_utf16<char32_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar32 *param_5,wchar32 *param_6,wchar32 **param_7)

{
  byte bVar1;
  ulong uVar2;
  ushort *puVar3;
  wchar32 *pwVar4;
  ulong uVar5;
  ulong uVar6;
  
  puVar3 = (ushort *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (puVar3 = (ushort *)(param_2 + 2), param_2[1] != -2)) {
    puVar3 = (ushort *)param_2;
  }
  if (puVar3 < param_3 + -1) {
    uVar5 = *(ulong *)(this + 0x10);
    pwVar4 = param_5;
    do {
      param_5 = pwVar4;
      if (param_6 <= pwVar4) break;
      bVar1 = *(byte *)((long)puVar3 + 1) & 0xfc;
      uVar6 = (ulong)*puVar3;
      if (bVar1 == 0xd8) {
        if ((long)param_3 - (long)puVar3 < 4) {
          uVar2 = 1;
          goto LAB_00e7e13c;
        }
        if (((*(byte *)((long)puVar3 + 3) & 0xfc) != 0xdc) ||
           (uVar6 = (((ulong)*puVar3 & 0x3ff) << 10 |
                    ((ulong)*(byte *)((long)puVar3 + 3) & 3) << 8 | (ulong)*(byte *)(puVar3 + 1)) +
                    0x10000, uVar5 < uVar6)) goto LAB_00e7e148;
        uVar2 = 4;
      }
      else {
        if (bVar1 == 0xdc) {
LAB_00e7e148:
          uVar2 = 2;
          goto LAB_00e7e13c;
        }
        uVar2 = 2;
        if (uVar5 < uVar6) goto LAB_00e7e13c;
      }
      puVar3 = (ushort *)((long)puVar3 + uVar2);
      param_5 = pwVar4 + 1;
      *pwVar4 = (wchar32)uVar6;
      pwVar4 = param_5;
    } while (puVar3 < param_3 + -1);
  }
  uVar2 = (ulong)(puVar3 < param_3);
  pwVar4 = param_5;
LAB_00e7e13c:
  *param_4 = (char *)puVar3;
  *param_7 = pwVar4;
  return uVar2;
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7e158
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf16<char32_t,true>::do_unshift
          (__codecvt_utf16<char32_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7e168
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf16<char32_t,true>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7e174
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf16<char32_t,true>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7e180
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

int __thiscall
std::__ndk1::__codecvt_utf16<char32_t,true>::do_length
          (__codecvt_utf16<char32_t,true> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  byte bVar1;
  ushort *puVar2;
  ulong uVar3;
  
  puVar2 = (ushort *)param_2;
  if ((((((byte)this[0x18] >> 2 & 1) != 0) && (1 < (long)param_3 - (long)param_2)) &&
      (*param_2 == -1)) && (puVar2 = (ushort *)(param_2 + 2), param_2[1] != -2)) {
    puVar2 = (ushort *)param_2;
  }
  if ((param_4 != 0) && (puVar2 < param_3 + -1)) {
    uVar3 = 1;
    do {
      bVar1 = *(byte *)((long)puVar2 + 1) & 0xfc;
      if (bVar1 == 0xd8) {
        if ((((long)param_3 - (long)puVar2 < 4) || ((*(byte *)((long)puVar2 + 3) & 0xfc) != 0xdc))
           || (*(ulong *)(this + 0x10) <
               (((ulong)*puVar2 & 0x3ff) << 10 |
               ((ulong)*(byte *)((long)puVar2 + 3) & 3) << 8 | (ulong)*(byte *)(puVar2 + 1)) +
               0x10000)) break;
        puVar2 = puVar2 + 2;
      }
      else {
        if ((bVar1 == 0xdc) || (*(ulong *)(this + 0x10) < (ulong)*puVar2)) break;
        puVar2 = puVar2 + 1;
      }
      if ((param_4 <= uVar3) || (uVar3 = uVar3 + 1, param_3 + -1 <= puVar2)) break;
    } while( true );
  }
  return (int)puVar2 - (int)param_2;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7e280
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf16<char32_t, true>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf16<char32_t,true>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 6;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7e29c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_out(mbstate_t&, wchar_t const*, wchar_t const*,
   wchar_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_out
          (__codecvt_utf8_utf16<wchar_t> *this,mbstate_t *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar_t *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7e338(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x18),
               *(undefined4 *)(this + 0x20));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7e55c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, wchar_t*, wchar_t*, wchar_t*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_in
          (__codecvt_utf8_utf16<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar_t *param_5,wchar_t *param_6,wchar_t **param_7)

{
  long lVar1;
  wchar_t *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7e5f8(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x18),
               *(undefined4 *)(this + 0x20));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7e874
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_unshift(mbstate_t&, char*, char*, char*&) const */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_unshift
          (__codecvt_utf8_utf16<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7e884
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7e890
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7e89c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_length
          (__codecvt_utf8_utf16<wchar_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c108(param_2,param_3,param_4,*(undefined8 *)(this + 0x18),*(undefined4 *)(this + 0x20));
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7e8bc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8_utf16<wchar_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x20) & 4) != 0) {
    uVar1 = 7;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7e8d8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_out(mbstate_t&, char16_t const*, char16_t const*,
   char16_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_out
          (__codecvt_utf8_utf16<char16_t> *this,mbstate_t *param_1,wchar16 *param_2,wchar16 *param_3
          ,wchar16 **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar16 *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7bb90(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7e974
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char16_t*, char16_t*, char16_t*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_in
          (__codecvt_utf8_utf16<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar16 *param_5,wchar16 *param_6,wchar16 **param_7)

{
  long lVar1;
  wchar16 *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7be48(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7ea10
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_unshift
          (__codecvt_utf8_utf16<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7ea20
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7ea2c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7ea38
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_length
          (__codecvt_utf8_utf16<char16_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c108(param_2,param_3,param_4,*(undefined8 *)(this + 0x10),*(undefined4 *)(this + 0x18));
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7ea58
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8_utf16<char16_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 7;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_out
// Address: 00e7ea74
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_out(mbstate_t&, char32_t const*, char32_t const*,
   char32_t const*&, char*, char*, char*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_out
          (__codecvt_utf8_utf16<char32_t> *this,mbstate_t *param_1,wchar32 *param_2,wchar32 *param_3
          ,wchar32 **param_4,char *param_5,char *param_6,char **param_7)

{
  long lVar1;
  char *local_48;
  wchar32 *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7e338(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_in
// Address: 00e7eb10
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_in(mbstate_t&, char const*, char const*, char
   const*&, char32_t*, char32_t*, char32_t*&) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_in
          (__codecvt_utf8_utf16<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4,wchar32 *param_5,wchar32 *param_6,wchar32 **param_7)

{
  long lVar1;
  wchar32 *local_48;
  char *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = param_5;
  local_40 = param_2;
  FUN_00e7e5f8(param_2,param_3,&local_40,param_5,param_6,&local_48,*(undefined8 *)(this + 0x10),
               *(undefined4 *)(this + 0x18));
  *param_4 = local_40;
  *param_7 = local_48;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: do_unshift
// Address: 00e7ebac
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_unshift(mbstate_t&, char*, char*, char*&) const
    */

undefined8 __thiscall
std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_unshift
          (__codecvt_utf8_utf16<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          char **param_4)

{
  *param_4 = param_2;
  return 3;
}



// ==========================================================================================
// Function: do_encoding
// Address: 00e7ebbc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_encoding() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_encoding(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_always_noconv
// Address: 00e7ebc8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_always_noconv() const */

undefined8 std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_always_noconv(void)

{
  return 0;
}



// ==========================================================================================
// Function: do_length
// Address: 00e7ebd4
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_length(mbstate_t&, char const*, char const*,
   unsigned long) const */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_length
          (__codecvt_utf8_utf16<char32_t> *this,mbstate_t *param_1,char *param_2,char *param_3,
          ulong param_4)

{
  FUN_00e7c108(param_2,param_3,param_4,*(undefined8 *)(this + 0x10),*(undefined4 *)(this + 0x18));
  return;
}



// ==========================================================================================
// Function: do_max_length
// Address: 00e7ebf4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_max_length() const */

undefined4 std::__ndk1::__codecvt_utf8_utf16<char32_t>::do_max_length(void)

{
  long in_x0;
  undefined4 uVar1;
  
  uVar1 = 4;
  if ((*(byte *)(in_x0 + 0x18) & 4) != 0) {
    uVar1 = 7;
  }
  return uVar1;
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e7ee4c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<char>::do_decimal_point() const */

undefined std::__ndk1::numpunct<char>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_decimal_point
// Address: 00e7ee58
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<wchar_t>::do_decimal_point() const */

undefined4 std::__ndk1::numpunct<wchar_t>::do_decimal_point(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x10);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e7ee64
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<char>::do_thousands_sep() const */

undefined std::__ndk1::numpunct<char>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined *)(in_x0 + 0x11);
}



// ==========================================================================================
// Function: do_thousands_sep
// Address: 00e7ee70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<wchar_t>::do_thousands_sep() const */

undefined4 std::__ndk1::numpunct<wchar_t>::do_thousands_sep(void)

{
  long in_x0;
  
  return *(undefined4 *)(in_x0 + 0x14);
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e7ee7c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<char>::do_grouping() const */

void std::__ndk1::numpunct<char>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_grouping
// Address: 00e7ee8c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<wchar_t>::do_grouping() const */

void std::__ndk1::numpunct<wchar_t>::do_grouping(void)

{
  long in_x0;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *in_x8;
  
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::basic_string
            (in_x8,(basic_string *)(in_x0 + 0x18));
  return;
}



// ==========================================================================================
// Function: do_truename
// Address: 00e7ee9c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<char>::do_truename() const */

void std::__ndk1::numpunct<char>::do_truename(void)

{
  undefined *in_x8;
  
  *in_x8 = 8;
  *(undefined4 *)(in_x8 + 1) = 0x65757274;
  in_x8[5] = 0;
  return;
}



// ==========================================================================================
// Function: do_truename
// Address: 00e7eebc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<wchar_t>::do_truename() const */

void std::__ndk1::numpunct<wchar_t>::do_truename(void)

{
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string<decltype(nullptr)>(in_x8,L"true");
  return;
}



// ==========================================================================================
// Function: do_falsename
// Address: 00e7ef70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<char>::do_falsename() const */

void std::__ndk1::numpunct<char>::do_falsename(void)

{
  undefined *in_x8;
  
  *in_x8 = 10;
  *(undefined4 *)(in_x8 + 1) = 0x736c6166;
  *(undefined2 *)(in_x8 + 5) = 0x65;
  return;
}



// ==========================================================================================
// Function: do_falsename
// Address: 00e7ef94
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::numpunct<wchar_t>::do_falsename() const */

void std::__ndk1::numpunct<wchar_t>::do_falsename(void)

{
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *in_x8;
  
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
  basic_string<decltype(nullptr)>(in_x8,L"false");
  return;
}



// ==========================================================================================
