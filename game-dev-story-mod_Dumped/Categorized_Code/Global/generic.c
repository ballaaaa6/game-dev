// Function: generic_category
// Address: 00e92ef4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::generic_category() */

undefined8 * std::__ndk1::generic_category(void)

{
  int iVar1;
  
  if (((DAT_0231e000 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231e000), iVar1 != 0)) {
    DAT_0231dff8 = &PTR__error_category_01fbb978;
    __cxa_guard_release(&DAT_0231e000);
  }
  return &DAT_0231dff8;
}



// ==========================================================================================
