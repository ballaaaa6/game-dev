// Function: toupper_l
// Address: 01ec6920
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int toupper_l(int __c,__locale_t __l)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_toupper_l_01ff66b0)(__c);
  return iVar1;
}



// ==========================================================================================
// Function: toupper_l
// Address: 0231f720
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int toupper_l(int __c,__locale_t __l)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
