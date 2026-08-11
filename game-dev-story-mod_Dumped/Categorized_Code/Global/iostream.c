// Function: iostream_category
// Address: 00e5ae9c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::iostream_category() */

undefined8 * std::__ndk1::iostream_category(void)

{
  int iVar1;
  
  if (((DAT_0231ce48 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231ce48), iVar1 != 0)) {
    error_category::error_category((error_category *)&DAT_0231ce40);
    DAT_0231ce40 = &PTR__error_category_01fb92b0;
    __cxa_atexit(PTR__error_category_01ff5660,&DAT_0231ce40,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231ce48);
  }
  return &DAT_0231ce40;
}



// ==========================================================================================
