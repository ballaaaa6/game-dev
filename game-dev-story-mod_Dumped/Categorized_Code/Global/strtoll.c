// Function: strtoll_l
// Address: 01ec6bd0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

longlong strtoll_l(char *__nptr,char **__endptr,int __base,__locale_t __loc)

{
  longlong lVar1;
  
  lVar1 = (*(code *)PTR_strtoll_l_01ff6808)(__nptr,__endptr,__base);
  return lVar1;
}



// ==========================================================================================
// Function: strtoll_l
// Address: 0231f700
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

longlong strtoll_l(char *__nptr,char **__endptr,int __base,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
