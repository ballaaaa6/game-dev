// Function: iswdigit_l
// Address: 01ec69b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswdigit_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswdigit_l_01ff66f8)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswdigit_l
// Address: 0231f658
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswdigit_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
