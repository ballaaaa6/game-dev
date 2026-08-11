// Function: ctype_byname
// Address: 00e79e5c
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::ctype_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::ctype_byname<char>::ctype_byname(ctype_byname<char> *this,char *param_1,ulong param_2)

{
  undefined *puVar1;
  long lVar2;
  __locale_t p_Var3;
  size_t __n;
  undefined8 *puVar4;
  void *__dest;
  ulong uVar5;
  undefined8 local_78;
  size_t local_70;
  void *pvStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  puVar1 = PTR_vtable_01ff58e0 + 0x10;
  this[0x18] = (ctype_byname<char>)0x0;
  *(ulong *)(this + 8) = param_2 - 1;
  *(undefined **)(this + 0x10) = &DAT_00838378;
  *(undefined **)this = puVar1;
                    /* try { // try from 00e79eb0 to 00e79ebb has its CatchHandler @ 00e79fcc */
  p_Var3 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)(this + 0x20) = p_Var3;
  if (p_Var3 != (__locale_t)0x0) {
    if (*(long *)(lVar2 + 0x28) == local_48) {
      return;
    }
    goto LAB_00e79f94;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* try { // try from 00e79f00 to 00e79f3b has its CatchHandler @ 00e79fc8 */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_78 | 1);
    local_78 = CONCAT71(local_78._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e79f4c;
  }
  else {
    uVar5 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar5);
    local_78 = uVar5 | 1;
    local_70 = __n;
    pvStack_68 = __dest;
LAB_00e79f4c:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e79f60 to 00e79f73 has its CatchHandler @ 00e79fb0 */
  puVar4 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_78,0,"ctype_byname<char>::ctype_byname failed to construct for ");
  local_50 = puVar4[2];
  uStack_58 = puVar4[1];
  local_60 = *puVar4;
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = 0;
                    /* try { // try from 00e79f8c to 00e79f93 has its CatchHandler @ 00e79f98 */
  FUN_00e78634(&local_60);
LAB_00e79f94:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ctype_byname
// Address: 00e7a004
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::ctype_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::ctype_byname<char>::ctype_byname
          (ctype_byname<char> *this,basic_string *param_1,ulong param_2)

{
  long lVar1;
  undefined *puVar2;
  __locale_t p_Var3;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  *(undefined **)(this + 0x10) = &DAT_00838378;
  puVar2 = PTR_vtable_01ff58e0;
  this[0x18] = (ctype_byname<char>)0x0;
  *(undefined **)this = puVar2 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
                    /* try { // try from 00e7a064 to 00e7a06f has its CatchHandler @ 00e7a0dc */
  p_Var3 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)(this + 0x20) = p_Var3;
  if (p_Var3 == (__locale_t)0x0) {
                    /* try { // try from 00e7a0a0 to 00e7a0b3 has its CatchHandler @ 00e7a0d8 */
    operator+(a_Stack_50,"ctype_byname<char>::ctype_byname failed to construct for ",param_1);
                    /* try { // try from 00e7a0b4 to 00e7a0bb has its CatchHandler @ 00e7a0c0 */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~ctype_byname
// Address: 00e7a114
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::~ctype_byname() */

void __thiscall std::__ndk1::ctype_byname<char>::~ctype_byname(ctype_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff58e0 + 0x10;
                    /* try { // try from 00e7a13c to 00e7a13f has its CatchHandler @ 00e7a180 */
  freelocale(*(__locale_t *)(this + 0x20));
  *(undefined **)this = PTR_vtable_01ff5708 + 0x10;
  if ((*(void **)(this + 0x10) != (void *)0x0) && (this[0x18] != (ctype_byname<char>)0x0)) {
    operator_delete__(*(void **)(this + 0x10));
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ctype_byname
// Address: 00e7a29c
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::ctype_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::ctype_byname<wchar_t>::ctype_byname
          (ctype_byname<wchar_t> *this,char *param_1,ulong param_2)

{
  long lVar1;
  __locale_t p_Var2;
  size_t __n;
  undefined8 *puVar3;
  void *__dest;
  ulong uVar4;
  undefined8 local_78;
  size_t local_70;
  void *pvStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  *(undefined **)this = PTR_vtable_01ff58e8 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
                    /* try { // try from 00e7a2e0 to 00e7a2eb has its CatchHandler @ 00e7a3fc */
  p_Var2 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 != (__locale_t)0x0) {
    if (*(long *)(lVar1 + 0x28) == local_48) {
      return;
    }
    goto LAB_00e7a3c4;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* try { // try from 00e7a330 to 00e7a36b has its CatchHandler @ 00e7a3f8 */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_78 | 1);
    local_78 = CONCAT71(local_78._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e7a37c;
  }
  else {
    uVar4 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar4);
    local_78 = uVar4 | 1;
    local_70 = __n;
    pvStack_68 = __dest;
LAB_00e7a37c:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e7a390 to 00e7a3a3 has its CatchHandler @ 00e7a3e0 */
  puVar3 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_78,0,"ctype_byname<wchar_t>::ctype_byname failed to construct for ")
  ;
  local_50 = puVar3[2];
  uStack_58 = puVar3[1];
  local_60 = *puVar3;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
                    /* try { // try from 00e7a3bc to 00e7a3c3 has its CatchHandler @ 00e7a3c8 */
  FUN_00e78634(&local_60);
LAB_00e7a3c4:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ctype_byname
// Address: 00e7a410
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::ctype_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::ctype_byname<wchar_t>::ctype_byname
          (ctype_byname<wchar_t> *this,basic_string *param_1,ulong param_2)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  *(undefined **)this = PTR_vtable_01ff58e8 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
                    /* try { // try from 00e7a460 to 00e7a46b has its CatchHandler @ 00e7a4d8 */
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
                    /* try { // try from 00e7a49c to 00e7a4af has its CatchHandler @ 00e7a4d4 */
    operator+(a_Stack_50,"ctype_byname<wchar_t>::ctype_byname failed to construct for ",param_1);
                    /* try { // try from 00e7a4b0 to 00e7a4b7 has its CatchHandler @ 00e7a4bc */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~ctype_byname
// Address: 00e7a4ec
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::~ctype_byname() */

void __thiscall std::__ndk1::ctype_byname<wchar_t>::~ctype_byname(ctype_byname<wchar_t> *this)

{
  *(undefined **)this = PTR_vtable_01ff58e8 + 0x10;
                    /* try { // try from 00e7a514 to 00e7a517 has its CatchHandler @ 00e7a534 */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~ctype_byname
// Address: 00e83190
// ==========================================================================================

/* std::__ndk1::ctype_byname<char>::~ctype_byname() */

void __thiscall std::__ndk1::ctype_byname<char>::~ctype_byname(ctype_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff58e0 + 0x10;
                    /* try { // try from 00e831b8 to 00e831bb has its CatchHandler @ 00e831f4 */
  freelocale(*(__locale_t *)(this + 0x20));
  *(undefined **)this = PTR_vtable_01ff5708 + 0x10;
  if ((*(void **)(this + 0x10) != (void *)0x0) && (this[0x18] != (ctype_byname<char>)0x0)) {
    operator_delete__(*(void **)(this + 0x10));
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: ~ctype_byname
// Address: 00e838bc
// ==========================================================================================

/* std::__ndk1::ctype_byname<wchar_t>::~ctype_byname() */

void __thiscall std::__ndk1::ctype_byname<wchar_t>::~ctype_byname(ctype_byname<wchar_t> *this)

{
  *(undefined **)this = PTR_vtable_01ff58e8 + 0x10;
                    /* try { // try from 00e838e4 to 00e838e7 has its CatchHandler @ 00e838fc */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: ctype_byname
// Address: 01ec67a0
// ==========================================================================================

void __thiscall
std::__ndk1::ctype_byname<char>::ctype_byname
          (ctype_byname<char> *this,basic_string *param_1,ulong param_2)

{
  (*(code *)PTR_ctype_byname_01ff65f0)();
  return;
}



// ==========================================================================================
// Function: ctype_byname
// Address: 01ec67b0
// ==========================================================================================

void __thiscall
std::__ndk1::ctype_byname<wchar_t>::ctype_byname
          (ctype_byname<wchar_t> *this,basic_string *param_1,ulong param_2)

{
  (*(code *)PTR_ctype_byname_01ff65f8)();
  return;
}



// ==========================================================================================
// Function: ctype_byname
// Address: 01ec6b20
// ==========================================================================================

void __thiscall
std::__ndk1::ctype_byname<char>::ctype_byname(ctype_byname<char> *this,char *param_1,ulong param_2)

{
  (*(code *)PTR_ctype_byname_01ff67b0)();
  return;
}



// ==========================================================================================
// Function: ctype_byname
// Address: 01ec6b40
// ==========================================================================================

void __thiscall
std::__ndk1::ctype_byname<wchar_t>::ctype_byname
          (ctype_byname<wchar_t> *this,char *param_1,ulong param_2)

{
  (*(code *)PTR_ctype_byname_01ff67c0)();
  return;
}



// ==========================================================================================
