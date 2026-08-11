// Function: collate_byname
// Address: 00e784c0
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::collate_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::collate_byname<char>::collate_byname
          (collate_byname<char> *this,char *param_1,ulong param_2)

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
  *(undefined **)this = PTR_vtable_01ff58d0 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
                    /* try { // try from 00e78504 to 00e7850f has its CatchHandler @ 00e78620 */
  p_Var2 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 != (__locale_t)0x0) {
    if (*(long *)(lVar1 + 0x28) == local_48) {
      return;
    }
    goto LAB_00e785e8;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* try { // try from 00e78554 to 00e7858f has its CatchHandler @ 00e7861c */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_78 | 1);
    local_78 = CONCAT71(local_78._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e785a0;
  }
  else {
    uVar4 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar4);
    local_78 = uVar4 | 1;
    local_70 = __n;
    pvStack_68 = __dest;
LAB_00e785a0:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e785b4 to 00e785c7 has its CatchHandler @ 00e78604 */
  puVar3 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_78,0,"collate_byname<char>::collate_byname failed to construct for "
                     );
  local_50 = puVar3[2];
  uStack_58 = puVar3[1];
  local_60 = *puVar3;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
                    /* try { // try from 00e785e0 to 00e785e7 has its CatchHandler @ 00e785ec */
  FUN_00e78634(&local_60);
LAB_00e785e8:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: collate_byname
// Address: 00e78688
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::collate_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::collate_byname<char>::collate_byname
          (collate_byname<char> *this,basic_string *param_1,ulong param_2)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  *(undefined **)this = PTR_vtable_01ff58d0 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
                    /* try { // try from 00e786d8 to 00e786e3 has its CatchHandler @ 00e78750 */
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
                    /* try { // try from 00e78714 to 00e78727 has its CatchHandler @ 00e7874c */
    operator+(a_Stack_50,"collate_byname<char>::collate_byname failed to construct for ",param_1);
                    /* try { // try from 00e78728 to 00e7872f has its CatchHandler @ 00e78734 */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~collate_byname
// Address: 00e78764
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::~collate_byname() */

void __thiscall std::__ndk1::collate_byname<char>::~collate_byname(collate_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff58d0 + 0x10;
                    /* try { // try from 00e7878c to 00e7878f has its CatchHandler @ 00e787a4 */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: ~collate_byname
// Address: 00e787b8
// ==========================================================================================

/* std::__ndk1::collate_byname<char>::~collate_byname() */

void __thiscall std::__ndk1::collate_byname<char>::~collate_byname(collate_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff58d0 + 0x10;
                    /* try { // try from 00e787e0 to 00e787e3 has its CatchHandler @ 00e78800 */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: collate_byname
// Address: 00e78c00
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::collate_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::collate_byname<wchar_t>::collate_byname
          (collate_byname<wchar_t> *this,char *param_1,ulong param_2)

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
  *(undefined **)this = PTR_vtable_01ff58d8 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
                    /* try { // try from 00e78c44 to 00e78c4f has its CatchHandler @ 00e78d60 */
  p_Var2 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 != (__locale_t)0x0) {
    if (*(long *)(lVar1 + 0x28) == local_48) {
      return;
    }
    goto LAB_00e78d28;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* try { // try from 00e78c94 to 00e78ccf has its CatchHandler @ 00e78d5c */
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_78 | 1);
    local_78 = CONCAT71(local_78._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e78ce0;
  }
  else {
    uVar4 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar4);
    local_78 = uVar4 | 1;
    local_70 = __n;
    pvStack_68 = __dest;
LAB_00e78ce0:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e78cf4 to 00e78d07 has its CatchHandler @ 00e78d44 */
  puVar3 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_78,0,
                      "collate_byname<wchar_t>::collate_byname(size_t refs) failed to construct for "
                     );
  local_50 = puVar3[2];
  uStack_58 = puVar3[1];
  local_60 = *puVar3;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
                    /* try { // try from 00e78d20 to 00e78d27 has its CatchHandler @ 00e78d2c */
  FUN_00e78634(&local_60);
LAB_00e78d28:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: collate_byname
// Address: 00e78d74
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::collate_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::collate_byname<wchar_t>::collate_byname
          (collate_byname<wchar_t> *this,basic_string *param_1,ulong param_2)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  *(undefined **)this = PTR_vtable_01ff58d8 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
                    /* try { // try from 00e78dc4 to 00e78dcf has its CatchHandler @ 00e78e3c */
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)(this + 0x10) = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
                    /* try { // try from 00e78e00 to 00e78e13 has its CatchHandler @ 00e78e38 */
    operator+(a_Stack_50,
              "collate_byname<wchar_t>::collate_byname(size_t refs) failed to construct for ",
              param_1);
                    /* try { // try from 00e78e14 to 00e78e1b has its CatchHandler @ 00e78e20 */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~collate_byname
// Address: 00e78e50
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::~collate_byname() */

void __thiscall std::__ndk1::collate_byname<wchar_t>::~collate_byname(collate_byname<wchar_t> *this)

{
  *(undefined **)this = PTR_vtable_01ff58d8 + 0x10;
                    /* try { // try from 00e78e78 to 00e78e7b has its CatchHandler @ 00e78e90 */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: ~collate_byname
// Address: 00e78ea4
// ==========================================================================================

/* std::__ndk1::collate_byname<wchar_t>::~collate_byname() */

void __thiscall std::__ndk1::collate_byname<wchar_t>::~collate_byname(collate_byname<wchar_t> *this)

{
  *(undefined **)this = PTR_vtable_01ff58d8 + 0x10;
                    /* try { // try from 00e78ecc to 00e78ecf has its CatchHandler @ 00e78eec */
  freelocale(*(__locale_t *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: collate_byname
// Address: 01ec6780
// ==========================================================================================

void __thiscall
std::__ndk1::collate_byname<char>::collate_byname
          (collate_byname<char> *this,basic_string *param_1,ulong param_2)

{
  (*(code *)PTR_collate_byname_01ff65e0)();
  return;
}



// ==========================================================================================
// Function: collate_byname
// Address: 01ec6790
// ==========================================================================================

void __thiscall
std::__ndk1::collate_byname<wchar_t>::collate_byname
          (collate_byname<wchar_t> *this,basic_string *param_1,ulong param_2)

{
  (*(code *)PTR_collate_byname_01ff65e8)();
  return;
}



// ==========================================================================================
