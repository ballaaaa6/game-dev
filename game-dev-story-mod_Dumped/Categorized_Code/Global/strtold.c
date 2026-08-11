// Function: strtold_l
// Address: 01ec6c10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

double strtold_l(char *__nptr,char **__endptr,__locale_t __loc)

{
  double dVar1;
  
  dVar1 = (double)(*(code *)PTR_strtold_l_01ff6828)();
  return dVar1;
}



// ==========================================================================================
// Function: strtold_l
// Address: 0231f6f8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

double strtold_l(char *__nptr,char **__endptr,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
