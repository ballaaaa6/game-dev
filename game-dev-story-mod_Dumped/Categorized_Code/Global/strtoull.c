// Function: strtoull_l
// Address: 01ec6be0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ulonglong strtoull_l(char *__nptr,char **__endptr,int __base,__locale_t __loc)

{
  ulonglong uVar1;
  
  uVar1 = (*(code *)PTR_strtoull_l_01ff6810)(__nptr,__endptr,__base);
  return uVar1;
}



// ==========================================================================================
// Function: strtoull_l
// Address: 0231f708
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ulonglong strtoull_l(char *__nptr,char **__endptr,int __base,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
