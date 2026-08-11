// Function: iswcntrl_l
// Address: 01ec6980
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswcntrl_l(wint_t __wc,__locale_t __locale)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_iswcntrl_l_01ff66e0)(__wc);
  return iVar1;
}



// ==========================================================================================
// Function: iswcntrl_l
// Address: 0231f650
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int iswcntrl_l(wint_t __wc,__locale_t __locale)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
