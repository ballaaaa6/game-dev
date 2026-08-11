// Function: tolower_l
// Address: 01ec6930
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int tolower_l(int __c,__locale_t __l)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_tolower_l_01ff66b8)(__c);
  return iVar1;
}



// ==========================================================================================
// Function: tolower_l
// Address: 0231f718
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int tolower_l(int __c,__locale_t __l)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
