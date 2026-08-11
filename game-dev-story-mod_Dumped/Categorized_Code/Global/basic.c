// Function: ~basic_ios
// Address: 00e4e0bc
// ==========================================================================================

/* std::__ndk1::basic_ios<char, std::__ndk1::char_traits<char> >::~basic_ios() */

void __thiscall
std::__ndk1::basic_ios<char,std::__ndk1::char_traits<char>>::~basic_ios
          (basic_ios<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)this);
  return;
}



// ==========================================================================================
// Function: ~basic_ios
// Address: 00e4e150
// ==========================================================================================

/* std::__ndk1::basic_ios<char, std::__ndk1::char_traits<char> >::~basic_ios() */

void __thiscall
std::__ndk1::basic_ios<char,std::__ndk1::char_traits<char>>::~basic_ios
          (basic_ios<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_ios
// Address: 00e4e58c
// ==========================================================================================

/* std::__ndk1::basic_ios<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_ios() */

void __thiscall
std::__ndk1::basic_ios<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ios
          (basic_ios<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)this);
  return;
}



// ==========================================================================================
// Function: ~basic_ios
// Address: 00e4e594
// ==========================================================================================

/* std::__ndk1::basic_ios<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_ios() */

void __thiscall
std::__ndk1::basic_ios<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ios
          (basic_ios<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_streambuf
// Address: 00e4e6a8
// ==========================================================================================

/* std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >::~basic_streambuf() */

void __thiscall
std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::~basic_streambuf
          (basic_streambuf<char,std::__ndk1::char_traits<char>> *this)

{
  *(undefined **)this = PTR_vtable_01ff55f8 + 0x10;
  locale::~locale((locale *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_streambuf
// Address: 00e4e6c0
// ==========================================================================================

/* std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >::~basic_streambuf() */

void __thiscall
std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::~basic_streambuf
          (basic_streambuf<char,std::__ndk1::char_traits<char>> *this)

{
  *(undefined **)this = PTR_vtable_01ff55f8 + 0x10;
  locale::~locale((locale *)(this + 8));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: basic_streambuf
// Address: 00e4e95c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >::basic_streambuf() */

void std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::basic_streambuf(void)

{
  long *in_x0;
  
  *in_x0 = (long)(PTR_vtable_01ff55f8 + 0x10);
  locale::locale((locale *)(in_x0 + 1));
  in_x0[5] = 0;
  in_x0[4] = 0;
  in_x0[7] = 0;
  in_x0[6] = 0;
  in_x0[3] = 0;
  in_x0[2] = 0;
  return;
}



// ==========================================================================================
// Function: basic_streambuf
// Address: 00e4e9a0
// ==========================================================================================

/* std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char>
   >::basic_streambuf(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> > const&) */

void __thiscall
std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::basic_streambuf
          (basic_streambuf<char,std::__ndk1::char_traits<char>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  
  *(undefined **)this = PTR_vtable_01ff55f8 + 0x10;
  locale::locale((locale *)(this + 8),(locale *)(param_1 + 8));
  uVar1 = *(undefined8 *)(param_1 + 0x10);
  *(undefined8 *)(this + 0x18) = *(undefined8 *)(param_1 + 0x18);
  *(undefined8 *)(this + 0x10) = uVar1;
  uVar1 = *(undefined8 *)(param_1 + 0x20);
  *(undefined8 *)(this + 0x28) = *(undefined8 *)(param_1 + 0x28);
  *(undefined8 *)(this + 0x20) = uVar1;
  uVar1 = *(undefined8 *)(param_1 + 0x30);
  *(undefined8 *)(this + 0x38) = *(undefined8 *)(param_1 + 0x38);
  *(undefined8 *)(this + 0x30) = uVar1;
  return;
}



// ==========================================================================================
// Function: ~basic_streambuf
// Address: 00e4eddc
// ==========================================================================================

/* std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_streambuf() */

void __thiscall
std::__ndk1::basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_streambuf
          (basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  *(undefined **)this = PTR_vtable_01ff5600 + 0x10;
  locale::~locale((locale *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_streambuf
// Address: 00e4edf4
// ==========================================================================================

/* std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_streambuf() */

void __thiscall
std::__ndk1::basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_streambuf
          (basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  *(undefined **)this = PTR_vtable_01ff5600 + 0x10;
  locale::~locale((locale *)(this + 8));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: basic_streambuf
// Address: 00e4f08c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >::basic_streambuf() */

void std::__ndk1::basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_streambuf(void)

{
  long *in_x0;
  
  *in_x0 = (long)(PTR_vtable_01ff5600 + 0x10);
  locale::locale((locale *)(in_x0 + 1));
  in_x0[5] = 0;
  in_x0[4] = 0;
  in_x0[7] = 0;
  in_x0[6] = 0;
  in_x0[3] = 0;
  in_x0[2] = 0;
  return;
}



// ==========================================================================================
// Function: basic_streambuf
// Address: 00e4f0d0
// ==========================================================================================

/* std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::basic_streambuf(std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >
   const&) */

void __thiscall
std::__ndk1::basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_streambuf
          (basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>> *this,basic_streambuf *param_1
          )

{
  undefined8 uVar1;
  
  *(undefined **)this = PTR_vtable_01ff5600 + 0x10;
  locale::locale((locale *)(this + 8),(locale *)(param_1 + 8));
  uVar1 = *(undefined8 *)(param_1 + 0x10);
  *(undefined8 *)(this + 0x18) = *(undefined8 *)(param_1 + 0x18);
  *(undefined8 *)(this + 0x10) = uVar1;
  uVar1 = *(undefined8 *)(param_1 + 0x20);
  *(undefined8 *)(this + 0x28) = *(undefined8 *)(param_1 + 0x28);
  *(undefined8 *)(this + 0x20) = uVar1;
  uVar1 = *(undefined8 *)(param_1 + 0x30);
  *(undefined8 *)(this + 0x38) = *(undefined8 *)(param_1 + 0x38);
  *(undefined8 *)(this + 0x30) = uVar1;
  return;
}



// ==========================================================================================
// Function: basic_istream
// Address: 00e4f524
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char>
   >::basic_istream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::basic_istream
               (basic_streambuf *param_1)

{
  undefined8 uVar1;
  long *in_x1;
  long in_x2;
  long lVar2;
  
  lVar2 = *in_x1;
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[1];
  *(undefined8 *)(param_1 + 8) = 0;
  uVar1 = _DAT_005bea70;
  lVar2 = *(long *)(*(long *)param_1 + -0x18);
  *(undefined8 *)(param_1 + lVar2 + 0x18) = _UNK_005bea78;
  *(undefined8 *)(param_1 + lVar2 + 0x10) = uVar1;
  *(long *)(param_1 + lVar2 + 0x28) = in_x2;
  *(uint *)(param_1 + lVar2 + 0x20) = (uint)(in_x2 == 0);
  *(undefined4 *)(param_1 + lVar2 + 0x24) = 0;
  *(undefined4 *)(param_1 + lVar2 + 8) = 0x1002;
  *(undefined8 *)(param_1 + lVar2 + 0x40) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x38) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x50) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x48) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x60) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x58) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x70) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x68) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x80) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x78) = 0;
  locale::locale((locale *)(param_1 + lVar2 + 0x30));
  *(undefined8 *)(param_1 + lVar2 + 0x88) = 0;
  *(undefined4 *)(param_1 + lVar2 + 0x90) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: basic_istream
// Address: 00e4f5b8
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char>
   >::basic_istream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined *puVar3;
  
  puVar3 = PTR_vtable_01ff5608;
  uVar2 = _UNK_005bea78;
  uVar1 = _DAT_005bea70;
  *(basic_streambuf **)(this + 0x38) = param_1;
  *(undefined4 *)(this + 0x18) = 0x1002;
  *(undefined8 *)(this + 0x28) = uVar2;
  *(undefined8 *)(this + 0x20) = uVar1;
  *(undefined8 *)(this + 8) = 0;
  *(undefined **)(this + 0x10) = puVar3 + 0x40;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x70) = 0;
  *(undefined8 *)(this + 0x68) = 0;
  *(undefined8 *)(this + 0x80) = 0;
  *(undefined8 *)(this + 0x78) = 0;
  *(undefined **)this = puVar3 + 0x18;
  *(uint *)(this + 0x30) = (uint)(param_1 == (basic_streambuf *)0x0);
  *(undefined4 *)(this + 0x34) = 0;
  *(undefined8 *)(this + 0x90) = 0;
  *(undefined8 *)(this + 0x88) = 0;
  locale::locale((locale *)(this + 0x40));
  *(undefined8 *)(this + 0x98) = 0;
  *(undefined4 *)(this + 0xa0) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e4f644
// ==========================================================================================

/* std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::~basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this)

{
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e4f64c
// ==========================================================================================

/* std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::~basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x10));
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e4f658
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char>
   >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::~basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + *(long *)(*(long *)this + -0x18) + 0x10));
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e4f670
// ==========================================================================================

/* std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::~basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x10));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e4f6a0
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_istream<char, std::__ndk1::char_traits<char>
   >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<char,std::__ndk1::char_traits<char>>::~basic_istream
          (basic_istream<char,std::__ndk1::char_traits<char>> *this)

{
  long lVar1;
  
  lVar1 = *(long *)(*(long *)this + -0x18);
  ios_base::~ios_base((ios_base *)(this + lVar1 + 0x10));
  operator_delete(this + lVar1);
  return;
}



// ==========================================================================================
// Function: basic_istream
// Address: 00e52ab4
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::basic_istream(std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >*) */

void std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_istream
               (basic_streambuf *param_1)

{
  undefined8 uVar1;
  long *in_x1;
  long in_x2;
  long lVar2;
  
  lVar2 = *in_x1;
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[1];
  *(undefined8 *)(param_1 + 8) = 0;
  uVar1 = _DAT_005bea70;
  lVar2 = *(long *)(*(long *)param_1 + -0x18);
  *(undefined8 *)(param_1 + lVar2 + 0x18) = _UNK_005bea78;
  *(undefined8 *)(param_1 + lVar2 + 0x10) = uVar1;
  *(long *)(param_1 + lVar2 + 0x28) = in_x2;
  *(uint *)(param_1 + lVar2 + 0x20) = (uint)(in_x2 == 0);
  *(undefined4 *)(param_1 + lVar2 + 0x24) = 0;
  *(undefined4 *)(param_1 + lVar2 + 8) = 0x1002;
  *(undefined8 *)(param_1 + lVar2 + 0x40) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x38) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x50) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x48) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x60) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x58) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x70) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x68) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x80) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x78) = 0;
  locale::locale((locale *)(param_1 + lVar2 + 0x30));
  *(undefined8 *)(param_1 + lVar2 + 0x88) = 0;
  *(undefined4 *)(param_1 + lVar2 + 0x90) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: basic_istream
// Address: 00e52b48
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::basic_istream(std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >*) */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined *puVar3;
  
  puVar3 = PTR_vtable_01ff5618;
  uVar2 = _UNK_005bea78;
  uVar1 = _DAT_005bea70;
  *(basic_streambuf **)(this + 0x38) = param_1;
  *(undefined4 *)(this + 0x18) = 0x1002;
  *(undefined8 *)(this + 0x28) = uVar2;
  *(undefined8 *)(this + 0x20) = uVar1;
  *(undefined8 *)(this + 8) = 0;
  *(undefined **)(this + 0x10) = puVar3 + 0x40;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x70) = 0;
  *(undefined8 *)(this + 0x68) = 0;
  *(undefined8 *)(this + 0x80) = 0;
  *(undefined8 *)(this + 0x78) = 0;
  *(undefined **)this = puVar3 + 0x18;
  *(uint *)(this + 0x30) = (uint)(param_1 == (basic_streambuf *)0x0);
  *(undefined4 *)(this + 0x34) = 0;
  *(undefined8 *)(this + 0x90) = 0;
  *(undefined8 *)(this + 0x88) = 0;
  locale::locale((locale *)(this + 0x40));
  *(undefined8 *)(this + 0x98) = 0;
  *(undefined4 *)(this + 0xa0) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e52bd4
// ==========================================================================================

/* std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e52bdc
// ==========================================================================================

/* std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x10));
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e52be8
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + *(long *)(*(long *)this + -0x18) + 0x10));
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e52c00
// ==========================================================================================

/* std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x10));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_istream
// Address: 00e52c30
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_istream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::~basic_istream() */

void __thiscall
std::__ndk1::basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_istream
          (basic_istream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  long lVar1;
  
  lVar1 = *(long *)(*(long *)this + -0x18);
  ios_base::~ios_base((ios_base *)(this + lVar1 + 0x10));
  operator_delete(this + lVar1);
  return;
}



// ==========================================================================================
// Function: basic_ostream
// Address: 00e5604c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char>
   >::basic_ostream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::basic_ostream
               (basic_streambuf *param_1)

{
  undefined8 uVar1;
  long *in_x1;
  long in_x2;
  long lVar2;
  
  lVar2 = *in_x1;
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[1];
  uVar1 = _DAT_005bea70;
  lVar2 = *(long *)(*(long *)param_1 + -0x18);
  *(undefined8 *)(param_1 + lVar2 + 0x18) = _UNK_005bea78;
  *(undefined8 *)(param_1 + lVar2 + 0x10) = uVar1;
  *(long *)(param_1 + lVar2 + 0x28) = in_x2;
  *(uint *)(param_1 + lVar2 + 0x20) = (uint)(in_x2 == 0);
  *(undefined4 *)(param_1 + lVar2 + 0x24) = 0;
  *(undefined4 *)(param_1 + lVar2 + 8) = 0x1002;
  *(undefined8 *)(param_1 + lVar2 + 0x40) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x38) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x50) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x48) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x60) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x58) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x70) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x68) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x80) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x78) = 0;
  locale::locale((locale *)(param_1 + lVar2 + 0x30));
  *(undefined8 *)(param_1 + lVar2 + 0x88) = 0;
  *(undefined4 *)(param_1 + lVar2 + 0x90) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: basic_ostream
// Address: 00e560dc
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char>
   >::basic_ostream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined *puVar3;
  
  puVar3 = PTR_vtable_01ff5630;
  uVar2 = _UNK_005bea78;
  uVar1 = _DAT_005bea70;
  *(basic_streambuf **)(this + 0x30) = param_1;
  *(undefined8 *)(this + 0x20) = uVar2;
  *(undefined8 *)(this + 0x18) = uVar1;
  *(undefined4 *)(this + 0x10) = 0x1002;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x40) = 0;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x68) = 0;
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x78) = 0;
  *(undefined8 *)(this + 0x70) = 0;
  *(undefined **)this = puVar3 + 0x18;
  *(undefined **)(this + 8) = puVar3 + 0x40;
  *(uint *)(this + 0x28) = (uint)(param_1 == (basic_streambuf *)0x0);
  *(undefined4 *)(this + 0x2c) = 0;
  *(undefined8 *)(this + 0x88) = 0;
  *(undefined8 *)(this + 0x80) = 0;
  locale::locale((locale *)(this + 0x38));
  *(undefined8 *)(this + 0x90) = 0;
  *(undefined4 *)(this + 0x98) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e5615c
// ==========================================================================================

/* std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::~basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this)

{
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e56164
// ==========================================================================================

/* std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::~basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e56170
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char>
   >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::~basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + *(long *)(*(long *)this + -0x18) + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e56188
// ==========================================================================================

/* std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::~basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e561b8
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_ostream<char, std::__ndk1::char_traits<char>
   >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::~basic_ostream
          (basic_ostream<char,std::__ndk1::char_traits<char>> *this)

{
  long lVar1;
  
  lVar1 = *(long *)(*(long *)this + -0x18);
  ios_base::~ios_base((ios_base *)(this + lVar1 + 8));
  operator_delete(this + lVar1);
  return;
}



// ==========================================================================================
// Function: basic_ostream
// Address: 00e585f0
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::basic_ostream(std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >*) */

void std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_ostream
               (basic_streambuf *param_1)

{
  undefined8 uVar1;
  long *in_x1;
  long in_x2;
  long lVar2;
  
  lVar2 = *in_x1;
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[1];
  uVar1 = _DAT_005bea70;
  lVar2 = *(long *)(*(long *)param_1 + -0x18);
  *(undefined8 *)(param_1 + lVar2 + 0x18) = _UNK_005bea78;
  *(undefined8 *)(param_1 + lVar2 + 0x10) = uVar1;
  *(long *)(param_1 + lVar2 + 0x28) = in_x2;
  *(uint *)(param_1 + lVar2 + 0x20) = (uint)(in_x2 == 0);
  *(undefined4 *)(param_1 + lVar2 + 0x24) = 0;
  *(undefined4 *)(param_1 + lVar2 + 8) = 0x1002;
  *(undefined8 *)(param_1 + lVar2 + 0x40) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x38) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x50) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x48) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x60) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x58) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x70) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x68) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x80) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x78) = 0;
  locale::locale((locale *)(param_1 + lVar2 + 0x30));
  *(undefined8 *)(param_1 + lVar2 + 0x88) = 0;
  *(undefined4 *)(param_1 + lVar2 + 0x90) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: basic_ostream
// Address: 00e58680
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::basic_ostream(std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >*) */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined *puVar3;
  
  puVar3 = PTR_vtable_01ff5640;
  uVar2 = _UNK_005bea78;
  uVar1 = _DAT_005bea70;
  *(basic_streambuf **)(this + 0x30) = param_1;
  *(undefined8 *)(this + 0x20) = uVar2;
  *(undefined8 *)(this + 0x18) = uVar1;
  *(undefined4 *)(this + 0x10) = 0x1002;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x40) = 0;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x68) = 0;
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x78) = 0;
  *(undefined8 *)(this + 0x70) = 0;
  *(undefined **)this = puVar3 + 0x18;
  *(undefined **)(this + 8) = puVar3 + 0x40;
  *(uint *)(this + 0x28) = (uint)(param_1 == (basic_streambuf *)0x0);
  *(undefined4 *)(this + 0x2c) = 0;
  *(undefined8 *)(this + 0x88) = 0;
  *(undefined8 *)(this + 0x80) = 0;
  locale::locale((locale *)(this + 0x38));
  *(undefined8 *)(this + 0x90) = 0;
  *(undefined4 *)(this + 0x98) = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e58700
// ==========================================================================================

/* std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e58708
// ==========================================================================================

/* std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e58714
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + *(long *)(*(long *)this + -0x18) + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e5872c
// ==========================================================================================

/* std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t> >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_ostream
// Address: 00e5875c
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_ostream<wchar_t, std::__ndk1::char_traits<wchar_t>
   >::~basic_ostream() */

void __thiscall
std::__ndk1::basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>>::~basic_ostream
          (basic_ostream<wchar_t,std::__ndk1::char_traits<wchar_t>> *this)

{
  long lVar1;
  
  lVar1 = *(long *)(*(long *)this + -0x18);
  ios_base::~ios_base((ios_base *)(this + lVar1 + 8));
  operator_delete(this + lVar1);
  return;
}



// ==========================================================================================
// Function: basic_iostream
// Address: 00e5ab50
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::basic_iostream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::basic_iostream
               (basic_streambuf *param_1)

{
  undefined8 uVar1;
  long *in_x1;
  long in_x2;
  long lVar2;
  long *plVar3;
  
  lVar2 = in_x1[1];
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[2];
  *(undefined8 *)(param_1 + 8) = 0;
  uVar1 = _DAT_005bea70;
  lVar2 = *(long *)(*(long *)param_1 + -0x18);
  *(undefined8 *)(param_1 + lVar2 + 0x18) = _UNK_005bea78;
  *(undefined8 *)(param_1 + lVar2 + 0x10) = uVar1;
  *(long *)(param_1 + lVar2 + 0x28) = in_x2;
  *(uint *)(param_1 + lVar2 + 0x20) = (uint)(in_x2 == 0);
  *(undefined4 *)(param_1 + lVar2 + 0x24) = 0;
  *(undefined4 *)(param_1 + lVar2 + 8) = 0x1002;
  *(undefined8 *)(param_1 + lVar2 + 0x40) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x38) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x50) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x48) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x60) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x58) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x70) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x68) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x80) = 0;
  *(undefined8 *)(param_1 + lVar2 + 0x78) = 0;
  locale::locale((locale *)(param_1 + lVar2 + 0x30));
  *(undefined8 *)(param_1 + lVar2 + 0x88) = 0;
  *(undefined4 *)(param_1 + lVar2 + 0x90) = 0xffffffff;
  lVar2 = in_x1[3];
  plVar3 = (long *)(param_1 + 0x10);
  *plVar3 = lVar2;
  *(long *)((long)plVar3 + *(long *)(lVar2 + -0x18)) = in_x1[4];
  lVar2 = *in_x1;
  *(long *)param_1 = lVar2;
  *(long *)(param_1 + *(long *)(lVar2 + -0x18)) = in_x1[5];
  *plVar3 = in_x1[6];
  return;
}



// ==========================================================================================
// Function: basic_iostream
// Address: 00e5ac28
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::basic_iostream(std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >*) */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this,basic_streambuf *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined *puVar3;
  
  puVar3 = PTR_construction_vtable_01ff5650;
  uVar2 = _UNK_005bea78;
  uVar1 = _DAT_005bea70;
  *(basic_streambuf **)(this + 0x40) = param_1;
  *(undefined4 *)(this + 0x20) = 0x1002;
  *(undefined8 *)(this + 0x30) = uVar2;
  *(undefined8 *)(this + 0x28) = uVar1;
  *(undefined **)(this + 0x18) = puVar3 + 0x40;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x68) = 0;
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x78) = 0;
  *(undefined8 *)(this + 0x70) = 0;
  *(undefined8 *)(this + 0x88) = 0;
  *(undefined8 *)(this + 0x80) = 0;
  *(undefined **)this = puVar3 + 0x18;
  *(undefined8 *)(this + 8) = 0;
  *(uint *)(this + 0x38) = (uint)(param_1 == (basic_streambuf *)0x0);
  *(undefined4 *)(this + 0x3c) = 0;
  *(undefined8 *)(this + 0x98) = 0;
  *(undefined8 *)(this + 0x90) = 0;
  locale::locale((locale *)(this + 0x48));
  *(undefined8 *)(this + 0xa0) = 0;
  puVar3 = PTR_vtable_01ff5658;
  *(undefined4 *)(this + 0xa8) = 0xffffffff;
  *(undefined **)this = puVar3 + 0x18;
  *(undefined **)(this + 0x10) = puVar3 + 0x40;
  *(undefined **)(this + 0x18) = puVar3 + 0x68;
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5acc8
// ==========================================================================================

/* std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char> >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5acd0
// ==========================================================================================

/* std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char> >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x18));
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5acdc
// ==========================================================================================

/* non-virtual thunk to std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5ace8
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + *(long *)(*(long *)this + -0x18) + 0x18));
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5ad00
// ==========================================================================================

/* std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char> >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 0x18));
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5ad30
// ==========================================================================================

/* non-virtual thunk to std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  ios_base::~ios_base((ios_base *)(this + 8));
  operator_delete(this + -0x10);
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 00e5ad60
// ==========================================================================================

/* virtual thunk to std::__ndk1::basic_iostream<char, std::__ndk1::char_traits<char>
   >::~basic_iostream() */

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  long lVar1;
  
  lVar1 = *(long *)(*(long *)this + -0x18);
  ios_base::~ios_base((ios_base *)(this + lVar1 + 0x18));
  operator_delete(this + lVar1);
  return;
}



// ==========================================================================================
// Function: basic_string<decltype(nullptr)>
// Address: 00e7eed0
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::basic_string<decltype(nullptr)>(wchar_t const*) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::basic_string<decltype(nullptr)>
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,wchar_t *param_1)

{
  size_t __n;
  wchar_t *__s1;
  ulong uVar1;
  
  __n = wcslen(param_1);
  if (0x3fffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 5) {
    __s1 = (wchar_t *)(this + 4);
    *this = SUB41((int)__n << 1,0);
    if (__n == 0) goto LAB_00e7ef4c;
  }
  else {
    uVar1 = __n + 4 & 0xfffffffffffffffc;
    __s1 = (wchar_t *)operator_new(uVar1 << 2);
    *(size_t *)(this + 8) = __n;
    *(wchar_t **)(this + 0x10) = __s1;
    *(ulong *)this = uVar1 | 1;
  }
                    /* try { // try from 00e7ef3c to 00e7ef4b has its CatchHandler @ 00e7ef6c */
  wmemcpy(__s1,param_1,__n);
LAB_00e7ef4c:
  __s1[__n] = L'\0';
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8aedc
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::basic_string(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
basic_string(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
            basic_string *param_1)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__dest;
  void *__src;
  ulong uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  if (((byte)*param_1 & 1) == 0) {
    uVar4 = *(undefined8 *)(param_1 + 8);
    uVar3 = *(undefined8 *)param_1;
    *(undefined8 *)(this + 0x10) = *(undefined8 *)(param_1 + 0x10);
    *(undefined8 *)(this + 8) = uVar4;
    *(undefined8 *)this = uVar3;
  }
  else {
    uVar2 = *(ulong *)(param_1 + 8);
    __src = *(void **)(param_1 + 0x10);
    if (uVar2 < 0x17) {
      __dest = this + 1;
      *this = SUB41((int)uVar2 << 1,0);
    }
    else {
      if (0xffffffffffffffef < uVar2) {
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      uVar1 = uVar2 + 0x10 & 0xfffffffffffffff0;
      __dest = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               operator_new(uVar1);
      *(ulong *)(this + 8) = uVar2;
      *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
       (this + 0x10) = __dest;
      *(ulong *)this = uVar1 | 1;
    }
    memcpy(__dest,__src,uVar2 + 1);
  }
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8afd0
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::basic_string(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, std::__ndk1::allocator<char> const&) */

void std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
     basic_string(basic_string *param_1,allocator *param_2)

{
  basic_string *__dest;
  void *__src;
  ulong uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  if (((byte)*param_2 & 1) == 0) {
    uVar4 = *(undefined8 *)(param_2 + 8);
    uVar3 = *(undefined8 *)param_2;
    *(undefined8 *)(param_1 + 0x10) = *(undefined8 *)(param_2 + 0x10);
    *(undefined8 *)(param_1 + 8) = uVar4;
    *(undefined8 *)param_1 = uVar3;
  }
  else {
    uVar2 = *(ulong *)(param_2 + 8);
    __src = *(void **)(param_2 + 0x10);
    if (uVar2 < 0x17) {
      __dest = param_1 + 1;
      *param_1 = SUB41((int)uVar2 << 1,0);
    }
    else {
      if (0xffffffffffffffef < uVar2) {
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      uVar1 = uVar2 + 0x10 & 0xfffffffffffffff0;
      __dest = (basic_string *)operator_new(uVar1);
      *(ulong *)(param_1 + 8) = uVar2;
      *(basic_string **)(param_1 + 0x10) = __dest;
      *(ulong *)param_1 = uVar1 | 1;
    }
    memcpy(__dest,__src,uVar2 + 1);
  }
  return;
}



// ==========================================================================================
// Function: ~basic_string
// Address: 00e8b0f0
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::~basic_string() */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
~basic_string(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this)

{
  if (((byte)*this & 1) == 0) {
    return;
  }
  operator_delete(*(void **)(this + 0x10));
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8bc4c
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::basic_string(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, unsigned long, unsigned long, std::__ndk1::allocator<char>
   const&) */

void std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
     basic_string(basic_string *param_1,ulong param_2,ulong param_3,allocator *param_4)

{
  allocator *__n;
  ulong uVar1;
  basic_string *__dest;
  long lVar2;
  
  if ((*(byte *)param_2 & 1) == 0) {
    uVar1 = (ulong)(*(byte *)param_2 >> 1);
    if (uVar1 < param_3) {
LAB_00e8bd10:
                    /* WARNING: Subroutine does not return */
      __basic_string_common<true>::__throw_out_of_range();
    }
    lVar2 = param_2 + 1;
  }
  else {
    uVar1 = *(ulong *)(param_2 + 8);
    if (uVar1 < param_3) goto LAB_00e8bd10;
    lVar2 = *(long *)(param_2 + 0x10);
  }
  __n = (allocator *)(uVar1 - param_3);
  if (param_4 <= (allocator *)(uVar1 - param_3)) {
    __n = param_4;
  }
  if ((allocator *)0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < (allocator *)0x17) {
    __dest = param_1 + 1;
    *param_1 = SUB41((int)__n << 1,0);
    if (__n == (allocator *)0x0) goto LAB_00e8bcf4;
  }
  else {
    __dest = (basic_string *)operator_new((ulong)(__n + 0x10) & 0xfffffffffffffff0);
    *(allocator **)(param_1 + 8) = __n;
    *(basic_string **)(param_1 + 0x10) = __dest;
    *(ulong *)param_1 = (ulong)(__n + 0x10) & 0xfffffffffffffff0 | 1;
  }
  memcpy(__dest,(void *)(lVar2 + param_3),(size_t)__n);
LAB_00e8bcf4:
  __dest[(long)__n] = (basic_string)0x0;
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8d134
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::basic_string(std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> > const&) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::basic_string(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               *this,basic_string *param_1)

{
  wchar_t *__s1;
  wchar_t *__s2;
  ulong uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  if (((byte)*param_1 & 1) == 0) {
    uVar4 = *(undefined8 *)(param_1 + 8);
    uVar3 = *(undefined8 *)param_1;
    *(undefined8 *)(this + 0x10) = *(undefined8 *)(param_1 + 0x10);
    *(undefined8 *)(this + 8) = uVar4;
    *(undefined8 *)this = uVar3;
  }
  else {
    uVar1 = *(ulong *)(param_1 + 8);
    __s2 = *(wchar_t **)(param_1 + 0x10);
    if (uVar1 < 5) {
      __s1 = (wchar_t *)(this + 4);
      *this = SUB41((int)uVar1 << 1,0);
    }
    else {
      if (0x3fffffffffffffef < uVar1) {
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      uVar2 = uVar1 + 4 & 0xfffffffffffffffc;
      __s1 = (wchar_t *)operator_new(uVar2 << 2);
      *(ulong *)(this + 8) = uVar1;
      *(wchar_t **)(this + 0x10) = __s1;
      *(ulong *)this = uVar2 | 1;
    }
                    /* try { // try from 00e8d1b0 to 00e8d1bb has its CatchHandler @ 00e8d1d8 */
    wmemcpy(__s1,__s2,uVar1 + 1);
  }
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8d230
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::basic_string(std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> > const&,
   std::__ndk1::allocator<wchar_t> const&) */

void std::__ndk1::
     basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
     basic_string(basic_string *param_1,allocator *param_2)

{
  wchar_t *__s1;
  wchar_t *__s2;
  ulong uVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  if (((byte)*param_2 & 1) == 0) {
    uVar4 = *(undefined8 *)(param_2 + 8);
    uVar3 = *(undefined8 *)param_2;
    *(undefined8 *)(param_1 + 0x10) = *(undefined8 *)(param_2 + 0x10);
    *(undefined8 *)(param_1 + 8) = uVar4;
    *(undefined8 *)param_1 = uVar3;
  }
  else {
    uVar1 = *(ulong *)(param_2 + 8);
    __s2 = *(wchar_t **)(param_2 + 0x10);
    if (uVar1 < 5) {
      __s1 = (wchar_t *)(param_1 + 4);
      *param_1 = SUB41((int)uVar1 << 1,0);
    }
    else {
      if (0x3fffffffffffffef < uVar1) {
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      uVar2 = uVar1 + 4 & 0xfffffffffffffffc;
      __s1 = (wchar_t *)operator_new(uVar2 << 2);
      *(ulong *)(param_1 + 8) = uVar1;
      *(wchar_t **)(param_1 + 0x10) = __s1;
      *(ulong *)param_1 = uVar2 | 1;
    }
                    /* try { // try from 00e8d2ac to 00e8d2b7 has its CatchHandler @ 00e8d2d4 */
    wmemcpy(__s1,__s2,uVar1 + 1);
  }
  return;
}



// ==========================================================================================
// Function: ~basic_string
// Address: 00e8d364
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::~basic_string() */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::~basic_string(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *this)

{
  if (((byte)*this & 1) == 0) {
    return;
  }
  operator_delete(*(void **)(this + 0x10));
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 00e8dea4
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::basic_string(std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> > const&, unsigned long,
   unsigned long, std::__ndk1::allocator<wchar_t> const&) */

void std::__ndk1::
     basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
     basic_string(basic_string *param_1,ulong param_2,ulong param_3,allocator *param_4)

{
  allocator *__n;
  ulong uVar1;
  wchar_t *__s1;
  long lVar2;
  
  if ((*(byte *)param_2 & 1) == 0) {
    uVar1 = (ulong)(*(byte *)param_2 >> 1);
    if (uVar1 < param_3) {
LAB_00e8df6c:
                    /* WARNING: Subroutine does not return */
      __basic_string_common<true>::__throw_out_of_range();
    }
    lVar2 = param_2 + 4;
  }
  else {
    uVar1 = *(ulong *)(param_2 + 8);
    if (uVar1 < param_3) goto LAB_00e8df6c;
    lVar2 = *(long *)(param_2 + 0x10);
  }
  __n = (allocator *)(uVar1 - param_3);
  if (param_4 <= (allocator *)(uVar1 - param_3)) {
    __n = param_4;
  }
  if ((allocator *)0x3fffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < (allocator *)0x5) {
    __s1 = (wchar_t *)(param_1 + 4);
    *param_1 = SUB41((int)__n << 1,0);
    if (__n == (allocator *)0x0) goto LAB_00e8df50;
  }
  else {
    __s1 = (wchar_t *)operator_new(((ulong)(__n + 4) & 0xfffffffffffffffc) << 2);
    *(allocator **)(param_1 + 8) = __n;
    *(wchar_t **)(param_1 + 0x10) = __s1;
    *(ulong *)param_1 = (ulong)(__n + 4) & 0xfffffffffffffffc | 1;
  }
                    /* try { // try from 00e8df44 to 00e8df4f has its CatchHandler @ 00e8df7c */
  wmemcpy(__s1,(wchar_t *)(lVar2 + param_3 * 4),(size_t)__n);
LAB_00e8df50:
  __s1[(long)__n] = L'\0';
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 01ec5460
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
basic_string(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
            basic_string *param_1)

{
  (*(code *)PTR_basic_string_01ff5c50)();
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 01ec5730
// ==========================================================================================

void std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
     basic_string(basic_string *param_1,ulong param_2,ulong param_3,allocator *param_4)

{
  (*(code *)PTR_basic_string_01ff5db8)();
  return;
}



// ==========================================================================================
// Function: ~basic_iostream
// Address: 01ec5970
// ==========================================================================================

void __thiscall
std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
          (basic_iostream<char,std::__ndk1::char_traits<char>> *this)

{
  (*(code *)PTR__basic_iostream_01ff5ed8)();
  return;
}



// ==========================================================================================
// Function: ~basic_ios
// Address: 01ec5980
// ==========================================================================================

void __thiscall
std::__ndk1::basic_ios<char,std::__ndk1::char_traits<char>>::~basic_ios
          (basic_ios<char,std::__ndk1::char_traits<char>> *this)

{
  (*(code *)PTR__basic_ios_01ff5ee0)();
  return;
}



// ==========================================================================================
// Function: ~basic_streambuf
// Address: 01ec59a0
// ==========================================================================================

void __thiscall
std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::~basic_streambuf
          (basic_streambuf<char,std::__ndk1::char_traits<char>> *this)

{
  (*(code *)PTR__basic_streambuf_01ff5ef0)();
  return;
}



// ==========================================================================================
// Function: basic_streambuf
// Address: 01ec5a30
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::basic_streambuf(void)

{
  (*(code *)PTR_basic_streambuf_01ff5f38)();
  return;
}



// ==========================================================================================
// Function: basic_string
// Address: 01ec6680
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::basic_string(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               *this,basic_string *param_1)

{
  (*(code *)PTR_basic_string_01ff6560)();
  return;
}



// ==========================================================================================
// Function: basic_string<decltype(nullptr)>
// Address: 01ec6a90
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::basic_string<decltype(nullptr)>
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,wchar_t *param_1)

{
  (*(code *)PTR_basic_string<decltype(nullptr)>_01ff6768)();
  return;
}



// ==========================================================================================
