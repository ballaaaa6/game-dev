// Function: wcscoll_l
// Address: 01ec68c0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int wcscoll_l(wchar_t *__s1,wchar_t *__s2,__locale_t __loc)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_wcscoll_l_01ff6680)((int)__s1);
  return iVar1;
}



// ==========================================================================================
// Function: wcscoll_l
// Address: 0231f758
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int wcscoll_l(wchar_t *__s1,wchar_t *__s2,__locale_t __loc)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
