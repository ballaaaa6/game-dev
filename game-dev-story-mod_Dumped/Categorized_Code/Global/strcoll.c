// Function: strcoll_l
// Address: 01ec6890
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int strcoll_l(char *__s1,char *__s2,__locale_t __l)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_strcoll_l_01ff6668)((int)__s1);
  return iVar1;
}



// ==========================================================================================
// Function: strcoll_l
// Address: 0231f6d8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int strcoll_l(char *__s1,char *__s2,__locale_t __l)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
