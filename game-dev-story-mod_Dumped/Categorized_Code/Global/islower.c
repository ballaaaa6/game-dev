// Function: islower_l
// Address: 01ec68f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int islower_l(int param_1,__locale_t param_2)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_islower_l_01ff6698)(param_1);
  return iVar1;
}



// ==========================================================================================
// Function: islower_l
// Address: 0231f630
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int islower_l(int param_1,__locale_t param_2)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
