// Function: towupper_l
// Address: 01ec69e0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

wint_t towupper_l(wint_t __wc,__locale_t __locale)

{
  wint_t wVar1;
  
  wVar1 = (*(code *)PTR_towupper_l_01ff6710)(__wc);
  return wVar1;
}



// ==========================================================================================
// Function: towupper_l
// Address: 0231f730
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

wint_t towupper_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
