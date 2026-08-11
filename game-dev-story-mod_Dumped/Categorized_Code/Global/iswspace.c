// Function: iswspace_l
// Address: 01ec6950
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswspace_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswspace_l_01ff66c8)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswspace_l
// Address: 0231f678
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswspace_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
