// Function: isdigit_l
// Address: 01ec65a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int isdigit_l(int param_1,__locale_t param_2)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_isdigit_l_01ff64f0)(param_1);
  return iVar1;
}



// ==========================================================================================
// Function: isdigit_l
// Address: 0231f628
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int isdigit_l(int param_1,__locale_t param_2)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
