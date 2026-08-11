// Function: wcsxfrm_l
// Address: 01ec68d0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t wcsxfrm_l(wchar_t *__s1,wchar_t *__s2,size_t __n,__locale_t __loc)

{
  size_t sVar1;
  
  sVar1 = (*(code *)PTR_wcsxfrm_l_01ff6688)();
  return sVar1;
}



// ==========================================================================================
// Function: wcsxfrm_l
// Address: 0231f770
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t wcsxfrm_l(wchar_t *__s1,wchar_t *__s2,size_t __n,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
