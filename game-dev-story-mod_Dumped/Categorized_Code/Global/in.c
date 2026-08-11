// Function: in_avail
// Address: 00e4e7a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::basic_streambuf<char, std::__ndk1::char_traits<char> >::in_avail() */

long std::__ndk1::basic_streambuf<char,std::__ndk1::char_traits<char>>::in_avail(void)

{
  long *in_x0;
  long lVar1;
  
  if ((ulong)in_x0[3] < (ulong)in_x0[4]) {
    return in_x0[4] - in_x0[3];
  }
                    /* WARNING: Could not recover jumptable at 0x00e4e7c0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  lVar1 = (**(code **)(*in_x0 + 0x38))();
  return lVar1;
}



// ==========================================================================================
// Function: in_avail
// Address: 00e4eed4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::basic_streambuf<wchar_t, std::__ndk1::char_traits<wchar_t> >::in_avail() */

long std::__ndk1::basic_streambuf<wchar_t,std::__ndk1::char_traits<wchar_t>>::in_avail(void)

{
  long *in_x0;
  long lVar1;
  
  if ((ulong)in_x0[3] < (ulong)in_x0[4]) {
    return in_x0[4] - in_x0[3] >> 2;
  }
                    /* WARNING: Could not recover jumptable at 0x00e4eef8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  lVar1 = (**(code **)(*in_x0 + 0x38))();
  return lVar1;
}



// ==========================================================================================
