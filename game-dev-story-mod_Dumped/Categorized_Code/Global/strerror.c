// Function: strerror_r
// Address: 01ec5d70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

char * strerror_r(int __errnum,char *__buf,size_t __buflen)

{
  char *pcVar1;
  
  pcVar1 = (char *)(*(code *)PTR_strerror_r_01ff60d8)(__errnum);
  return pcVar1;
}



// ==========================================================================================
// Function: strerror_r
// Address: 0231f4b8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

char * strerror_r(int __errnum,char *__buf,size_t __buflen)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
