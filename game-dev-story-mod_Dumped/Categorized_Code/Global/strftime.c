// Function: strftime_l
// Address: 01ec6640
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t strftime_l(char *__s,size_t __maxsize,char *__format,tm *__tp,__locale_t __loc)

{
  size_t sVar1;
  
  sVar1 = (*(code *)PTR_strftime_l_01ff6540)();
  return sVar1;
}



// ==========================================================================================
// Function: strftime_l
// Address: 0231f6e0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t strftime_l(char *__s,size_t __maxsize,char *__format,tm *__tp,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
