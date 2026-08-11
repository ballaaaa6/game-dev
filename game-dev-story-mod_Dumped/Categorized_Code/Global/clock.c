// Function: clock_gettime
// Address: 01ec5c90
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int clock_gettime(clockid_t __clock_id,timespec *__tp)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_clock_gettime_01ff6068)(__clock_id);
  return iVar1;
}



// ==========================================================================================
// Function: clock_getres
// Address: 01ec5ca0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int clock_getres(clockid_t __clock_id,timespec *__res)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_clock_getres_01ff6070)(__clock_id);
  return iVar1;
}



// ==========================================================================================
// Function: clock_getres
// Address: 0231f350
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int clock_getres(clockid_t __clock_id,timespec *__res)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: clock_gettime
// Address: 0231f358
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int clock_gettime(clockid_t __clock_id,timespec *__tp)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
