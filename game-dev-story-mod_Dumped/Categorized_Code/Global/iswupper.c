// Function: iswupper_l
// Address: 01ec6990
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswupper_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswupper_l_01ff66e8)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswupper_l
// Address: 0231f680
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswupper_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
