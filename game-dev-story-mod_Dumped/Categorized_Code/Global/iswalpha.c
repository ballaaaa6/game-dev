// Function: iswalpha_l
// Address: 01ec69a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswalpha_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswalpha_l_01ff66f0)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswalpha_l
// Address: 0231f640
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswalpha_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
