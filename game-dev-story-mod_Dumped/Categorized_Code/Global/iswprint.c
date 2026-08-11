// Function: iswprint_l
// Address: 01ec6960
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswprint_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswprint_l_01ff66d0)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswprint_l
// Address: 0231f668
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswprint_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
