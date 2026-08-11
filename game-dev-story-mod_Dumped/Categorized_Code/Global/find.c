// Function: find_last_not_of
// Address: 00e8b070
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::find_last_not_of(char const*, unsigned long, unsigned long) const */

ulong __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
find_last_not_of(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                 *this,char *param_1,ulong param_2,ulong param_3)

{
  void *pvVar1;
  ulong uVar2;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar3;
  
  if (((byte)*this & 1) == 0) {
    pbVar3 = this + 1;
    uVar2 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar2 = *(ulong *)(this + 8);
    pbVar3 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
              (this + 0x10);
  }
  if (param_2 < uVar2) {
    uVar2 = param_2 + 1;
  }
  while( true ) {
    uVar2 = uVar2 - 1;
    if (uVar2 == 0xffffffffffffffff) {
      return 0xffffffffffffffff;
    }
    if (param_3 == 0) break;
    pvVar1 = memchr(param_1,(uint)(byte)pbVar3[uVar2],param_3);
    if (pvVar1 == (void *)0x0) {
      return uVar2;
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: find_first_not_of
// Address: 00e8b108
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::find_first_not_of(char const*, unsigned long, unsigned long) const */

long __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
find_first_not_of(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                  *this,char *param_1,ulong param_2,ulong param_3)

{
  void *pvVar1;
  ulong uVar2;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar3;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar4;
  long lVar5;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar6;
  
  if (((byte)*this & 1) == 0) {
    pbVar3 = this + 1;
    uVar2 = (ulong)((byte)*this >> 1);
    lVar5 = uVar2 - param_2;
    if (uVar2 < param_2 || lVar5 == 0) {
      return -1;
    }
  }
  else {
    pbVar3 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
              (this + 0x10);
    lVar5 = *(ulong *)(this + 8) - param_2;
    if (*(ulong *)(this + 8) < param_2 || lVar5 == 0) {
      return -1;
    }
  }
  pbVar6 = pbVar3 + param_2;
  while ((pbVar4 = pbVar3 + param_2, param_3 != 0 &&
         (pvVar1 = memchr(param_1,(uint)(byte)*pbVar6,param_3), pbVar4 = pbVar6,
         pvVar1 != (void *)0x0))) {
    lVar5 = lVar5 + -1;
    pbVar6 = pbVar6 + 1;
    if (lVar5 == 0) {
      return -1;
    }
  }
  return (long)pbVar4 - (long)pbVar3;
}



// ==========================================================================================
// Function: find_first_of
// Address: 00e8b60c
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::find_first_of(char const*, unsigned long, unsigned long) const */

long __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
find_first_of(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
             char *param_1,ulong param_2,ulong param_3)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar1;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar2;
  long lVar3;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar4;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar5;
  ulong uVar6;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar7;
  
  if (((byte)*this & 1) == 0) {
    pbVar2 = this + 1;
    uVar6 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar6 = *(ulong *)(this + 8);
    pbVar2 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
              (this + 0x10);
  }
  if ((param_3 == 0) || (uVar6 <= param_2)) {
    return -1;
  }
  pbVar4 = pbVar2 + param_2;
  pbVar1 = pbVar2 + uVar6;
  do {
    uVar6 = param_3;
    pbVar7 = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             param_1;
    do {
      pbVar5 = pbVar4;
      if (*pbVar4 == *pbVar7) goto LAB_00e8b678;
      uVar6 = uVar6 - 1;
      pbVar7 = pbVar7 + 1;
    } while (uVar6 != 0);
    pbVar4 = pbVar4 + 1;
    pbVar5 = pbVar1;
  } while (pbVar4 != pbVar1);
LAB_00e8b678:
  lVar3 = (long)pbVar5 - (long)pbVar2;
  if (pbVar5 == pbVar1) {
    lVar3 = -1;
  }
  return lVar3;
}



// ==========================================================================================
// Function: find_last_of
// Address: 00e8be70
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::find_last_of(char const*, unsigned long, unsigned long) const */

ulong __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
find_last_of(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
            char *param_1,ulong param_2,ulong param_3)

{
  void *pvVar1;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar2;
  ulong uVar3;
  
  if (((byte)*this & 1) == 0) {
    pbVar2 = this + 1;
    uVar3 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar3 = *(ulong *)(this + 8);
    pbVar2 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
              (this + 0x10);
  }
  if (param_3 == 0) {
LAB_00e8bed8:
    uVar3 = 0xffffffffffffffff;
  }
  else {
    if (param_2 < uVar3) {
      uVar3 = param_2 + 1;
    }
    do {
      if (uVar3 == 0) goto LAB_00e8bed8;
      pvVar1 = memchr(param_1,(uint)(byte)pbVar2[uVar3 - 1],param_3);
      uVar3 = uVar3 - 1;
    } while (pvVar1 == (void *)0x0);
  }
  return uVar3;
}



// ==========================================================================================
// Function: find_last_not_of
// Address: 00e8d2d8
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::find_last_not_of(wchar_t const*, unsigned long, unsigned long)
   const */

long __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::find_last_not_of(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                   *this,wchar_t *param_1,ulong param_2,ulong param_3)

{
  wchar_t *pwVar1;
  ulong uVar2;
  long lVar3;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar4;
  
  if (((byte)*this & 1) == 0) {
    pbVar4 = this + 4;
    uVar2 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar2 = *(ulong *)(this + 8);
    pbVar4 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
  }
  if (param_2 < uVar2) {
    uVar2 = param_2 + 1;
  }
  lVar3 = uVar2 * 4;
  do {
    lVar3 = lVar3 + -4;
    if (lVar3 == -4) {
      return -1;
    }
  } while ((param_3 != 0) &&
          (pwVar1 = wmemchr(param_1,*(wchar_t *)(pbVar4 + lVar3),param_3), pwVar1 != (wchar_t *)0x0)
          );
  return lVar3 >> 2;
}



// ==========================================================================================
// Function: find_first_not_of
// Address: 00e8d37c
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::find_first_not_of(wchar_t const*, unsigned long, unsigned
   long) const */

long __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::find_first_not_of(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                    *this,wchar_t *param_1,ulong param_2,ulong param_3)

{
  wchar_t *pwVar1;
  ulong uVar2;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar3;
  wchar_t *pwVar4;
  long lVar5;
  wchar_t *pwVar6;
  
  if (((byte)*this & 1) == 0) {
    pbVar3 = this + 4;
    uVar2 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar2 = *(ulong *)(this + 8);
    pbVar3 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
  }
  if (param_2 < uVar2) {
    lVar5 = uVar2 * 4 + param_2 * -4;
    pwVar6 = (wchar_t *)(pbVar3 + param_2 * 4);
    do {
      pwVar4 = (wchar_t *)(pbVar3 + param_2 * 4);
      if ((param_3 == 0) ||
         (pwVar1 = wmemchr(param_1,*pwVar6,param_3), pwVar4 = pwVar6, pwVar1 == (wchar_t *)0x0)) {
        return (long)pwVar4 - (long)pbVar3 >> 2;
      }
      lVar5 = lVar5 + -4;
      pwVar6 = pwVar6 + 1;
    } while (lVar5 != 0);
  }
  return -1;
}



// ==========================================================================================
// Function: find_first_of
// Address: 00e8d8c8
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::find_first_of(wchar_t const*, unsigned long, unsigned long)
   const */

long __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::find_first_of(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *this,wchar_t *param_1,ulong param_2,ulong param_3)

{
  wchar_t *pwVar1;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar2;
  long lVar3;
  wchar_t *pwVar4;
  wchar_t *pwVar5;
  ulong uVar6;
  wchar_t *pwVar7;
  
  if (((byte)*this & 1) == 0) {
    pbVar2 = this + 4;
    uVar6 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar6 = *(ulong *)(this + 8);
    pbVar2 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
  }
  if ((param_3 == 0) || (uVar6 <= param_2)) {
    return -1;
  }
  pwVar4 = (wchar_t *)(pbVar2 + param_2 * 4);
  pwVar1 = (wchar_t *)(pbVar2 + uVar6 * 4);
  do {
    lVar3 = param_3 << 2;
    pwVar7 = param_1;
    do {
      pwVar5 = pwVar4;
      if (*pwVar4 == *pwVar7) goto LAB_00e8d938;
      lVar3 = lVar3 + -4;
      pwVar7 = pwVar7 + 1;
    } while (lVar3 != 0);
    pwVar4 = pwVar4 + 1;
    pwVar5 = pwVar1;
  } while (pwVar4 != pwVar1);
LAB_00e8d938:
  lVar3 = (long)pwVar5 - (long)pbVar2 >> 2;
  if (pwVar5 == pwVar1) {
    lVar3 = -1;
  }
  return lVar3;
}



// ==========================================================================================
// Function: find_last_of
// Address: 00e8e0d8
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::find_last_of(wchar_t const*, unsigned long, unsigned long)
   const */

long __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::find_last_of(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               *this,wchar_t *param_1,ulong param_2,ulong param_3)

{
  wchar_t *pwVar1;
  long lVar2;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar3;
  ulong uVar4;
  
  if (((byte)*this & 1) == 0) {
    pbVar3 = this + 4;
    uVar4 = (ulong)((byte)*this >> 1);
  }
  else {
    uVar4 = *(ulong *)(this + 8);
    pbVar3 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
  }
  if (param_3 == 0) {
LAB_00e8e148:
    lVar2 = -1;
  }
  else {
    if (param_2 < uVar4) {
      uVar4 = param_2 + 1;
    }
    lVar2 = uVar4 << 2;
    do {
      if (lVar2 == 0) goto LAB_00e8e148;
      pwVar1 = wmemchr(param_1,*(wchar_t *)(pbVar3 + lVar2 + -4),param_3);
      lVar2 = lVar2 + -4;
    } while (pwVar1 == (wchar_t *)0x0);
    lVar2 = lVar2 >> 2;
  }
  return lVar2;
}



// ==========================================================================================
