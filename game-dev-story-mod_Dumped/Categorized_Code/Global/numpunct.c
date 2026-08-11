// Function: ~numpunct_byname
// Address: 00e7ed1c
// ==========================================================================================

/* std::__ndk1::numpunct_byname<char>::~numpunct_byname() */

void __thiscall std::__ndk1::numpunct_byname<char>::~numpunct_byname(numpunct_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff5750 + 0x10;
  if (((byte)this[0x18] & 1) != 0) {
    operator_delete(*(void **)(this + 0x28));
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: numpunct_byname
// Address: 00e7efa8
// ==========================================================================================

/* std::__ndk1::numpunct_byname<char>::numpunct_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::numpunct_byname<char>::numpunct_byname
          (numpunct_byname<char> *this,char *param_1,ulong param_2)

{
  undefined *puVar1;
  
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  *(undefined8 *)(this + 0x18) = 0;
  puVar1 = PTR_vtable_01ff5868;
  *(undefined2 *)(this + 0x10) = 0x2c2e;
  *(undefined **)this = puVar1 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
                    /* try { // try from 00e7efe0 to 00e7efe3 has its CatchHandler @ 00e7eff4 */
  __init(this,param_1);
  return;
}



// ==========================================================================================
// Function: numpunct_byname
// Address: 00e7f3d8
// ==========================================================================================

/* std::__ndk1::numpunct_byname<char>::numpunct_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::numpunct_byname<char>::numpunct_byname
          (numpunct_byname<char> *this,basic_string *param_1,ulong param_2)

{
  basic_string *pbVar1;
  
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  *(undefined8 *)(this + 0x18) = 0;
  *(undefined2 *)(this + 0x10) = 0x2c2e;
  *(undefined **)this = PTR_vtable_01ff5868 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  pbVar1 = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    pbVar1 = param_1 + 1;
  }
                    /* try { // try from 00e7f420 to 00e7f423 has its CatchHandler @ 00e7f434 */
  __init(this,(char *)pbVar1);
  return;
}



// ==========================================================================================
// Function: ~numpunct_byname
// Address: 00e7f468
// ==========================================================================================

/* std::__ndk1::numpunct_byname<char>::~numpunct_byname() */

void __thiscall std::__ndk1::numpunct_byname<char>::~numpunct_byname(numpunct_byname<char> *this)

{
  *(undefined **)this = PTR_vtable_01ff5750 + 0x10;
  if (((byte)this[0x18] & 1) != 0) {
    operator_delete(*(void **)(this + 0x28));
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: numpunct_byname
// Address: 00e7f4b8
// ==========================================================================================

/* std::__ndk1::numpunct_byname<wchar_t>::numpunct_byname(char const*, unsigned long) */

void __thiscall
std::__ndk1::numpunct_byname<wchar_t>::numpunct_byname
          (numpunct_byname<wchar_t> *this,char *param_1,ulong param_2)

{
  undefined8 uVar1;
  undefined *puVar2;
  
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  uVar1 = DAT_005bc6e0;
  *(undefined8 *)(this + 0x18) = 0;
  puVar2 = PTR_vtable_01ff5870;
  *(undefined8 *)(this + 0x10) = uVar1;
  *(undefined **)this = puVar2 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
                    /* try { // try from 00e7f4f4 to 00e7f4f7 has its CatchHandler @ 00e7f508 */
  __init(this,param_1);
  return;
}



// ==========================================================================================
// Function: numpunct_byname
// Address: 00e7f80c
// ==========================================================================================

/* std::__ndk1::numpunct_byname<wchar_t>::numpunct_byname(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, unsigned long) */

void __thiscall
std::__ndk1::numpunct_byname<wchar_t>::numpunct_byname
          (numpunct_byname<wchar_t> *this,basic_string *param_1,ulong param_2)

{
  undefined8 uVar1;
  undefined *puVar2;
  basic_string *pbVar3;
  
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  uVar1 = DAT_005bc6e0;
  *(undefined8 *)(this + 0x18) = 0;
  puVar2 = PTR_vtable_01ff5870;
  *(undefined8 *)(this + 0x10) = uVar1;
  *(undefined **)this = puVar2 + 0x10;
  *(ulong *)(this + 8) = param_2 - 1;
  pbVar3 = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    pbVar3 = param_1 + 1;
  }
                    /* try { // try from 00e7f858 to 00e7f85b has its CatchHandler @ 00e7f86c */
  __init(this,(char *)pbVar3);
  return;
}



// ==========================================================================================
// Function: ~numpunct_byname
// Address: 00e7f8a0
// ==========================================================================================

/* std::__ndk1::numpunct_byname<wchar_t>::~numpunct_byname() */

void __thiscall
std::__ndk1::numpunct_byname<wchar_t>::~numpunct_byname(numpunct_byname<wchar_t> *this)

{
  *(undefined **)this = PTR_vtable_01ff5758 + 0x10;
  if (((byte)this[0x18] & 1) != 0) {
    operator_delete(*(void **)(this + 0x28));
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
