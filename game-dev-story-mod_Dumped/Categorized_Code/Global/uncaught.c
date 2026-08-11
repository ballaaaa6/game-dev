// Function: uncaught_exception
// Address: 00e4dee8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::uncaught_exception() */

bool std::uncaught_exception(void)

{
  int iVar1;
  
  iVar1 = __cxa_uncaught_exceptions();
  return 0 < iVar1;
}



// ==========================================================================================
// Function: uncaught_exceptions
// Address: 00e4df0c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::uncaught_exceptions() */

void std::uncaught_exceptions(void)

{
  __cxa_uncaught_exceptions();
  return;
}



// ==========================================================================================
// Function: uncaught_exception
// Address: 01ec62b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::uncaught_exception(void)

{
  (*(code *)PTR_uncaught_exception_01ff6378)();
  return;
}



// ==========================================================================================
