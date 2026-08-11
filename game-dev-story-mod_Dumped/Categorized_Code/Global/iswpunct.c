// Function: iswpunct_l
// Address: 01ec69c0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswpunct_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswpunct_l_01ff6700)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswpunct_l
// Address: 0231f670
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswpunct_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
