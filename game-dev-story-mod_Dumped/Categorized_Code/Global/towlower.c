// Function: towlower_l
// Address: 01ec69f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

wint_t towlower_l(wint_t __wc,__locale_t __locale)

{
  wint_t wVar1;
  
  wVar1 = (*(code *)PTR_towlower_l_01ff6718)(__wc);
  return wVar1;
}



// ==========================================================================================
// Function: towlower_l
// Address: 0231f728
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

wint_t towlower_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
