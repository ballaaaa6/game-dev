// Function: sched_yield
// Address: 00e4d97c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sched_yield(void)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sched_yield_01ff61b8)();
  return iVar1;
}



// ==========================================================================================
// Function: sched_yield
// Address: 01ec5f30
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sched_yield(void)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sched_yield_01ff61b8)();
  return iVar1;
}



// ==========================================================================================
// Function: sched_yield
// Address: 0231f500
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sched_yield(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
