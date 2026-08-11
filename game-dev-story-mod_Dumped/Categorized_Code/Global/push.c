// Function: push_back
// Address: 00e8bef4
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::push_back(char) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
push_back(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
         char param_1)

{
  byte bVar1;
  ulong uVar2;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar3;
  ulong uVar4;
  
  if (((byte)*this & 1) == 0) {
    bVar1 = (byte)*this >> 1;
    uVar4 = (ulong)bVar1;
    if (bVar1 == 0x16) {
      uVar4 = 0x16;
      uVar2 = 0x16;
LAB_00e8bf44:
      __grow_by(this,uVar2,1,uVar2,uVar2,0,0);
      if (((byte)*this & 1) != 0) goto LAB_00e8bf78;
    }
    pbVar3 = this + 1;
    *this = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)
            ((char)uVar4 * '\x02' + '\x02');
  }
  else {
    uVar4 = *(ulong *)(this + 8);
    uVar2 = (*(ulong *)this & 0xfffffffffffffffe) - 1;
    if (uVar4 == uVar2) goto LAB_00e8bf44;
LAB_00e8bf78:
    pbVar3 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
              (this + 0x10);
    *(ulong *)(this + 8) = uVar4 + 1;
  }
  pbVar3[uVar4] =
       (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)param_1;
  (pbVar3 + uVar4)[1] =
       (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)0x0;
  return;
}



// ==========================================================================================
// Function: push_back
// Address: 00e8e160
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::push_back(wchar_t) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::push_back(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            *this,wchar_t param_1)

{
  byte bVar1;
  ulong uVar2;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar3;
  ulong uVar4;
  
  if (((byte)*this & 1) == 0) {
    bVar1 = (byte)*this >> 1;
    uVar4 = (ulong)bVar1;
    if (bVar1 == 4) {
      uVar4 = 4;
      uVar2 = 4;
LAB_00e8e1b0:
      __grow_by(this,uVar2,1,uVar2,uVar2,0,0);
      if (((byte)*this & 1) != 0) goto LAB_00e8e1e4;
    }
    pbVar3 = this + 4;
    *this = (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            )((char)uVar4 * '\x02' + '\x02');
  }
  else {
    uVar4 = *(ulong *)(this + 8);
    uVar2 = (*(ulong *)this & 0xfffffffffffffffe) - 1;
    if (uVar4 == uVar2) goto LAB_00e8e1b0;
LAB_00e8e1e4:
    pbVar3 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
    *(ulong *)(this + 8) = uVar4 + 1;
  }
  *(wchar_t *)(pbVar3 + uVar4 * 4) = param_1;
  *(wchar_t *)((long)(pbVar3 + uVar4 * 4) + 4) = L'\0';
  return;
}



// ==========================================================================================
// Function: push_back
// Address: 01ec5760
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
push_back(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
         char param_1)

{
  (*(code *)PTR_push_back_01ff5dd0)(this,param_1);
  return;
}



// ==========================================================================================
// Function: push_back
// Address: 01ec6700
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::push_back(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            *this,wchar_t param_1)

{
  (*(code *)PTR_push_back_01ff65a0)(this,param_1);
  return;
}



// ==========================================================================================
