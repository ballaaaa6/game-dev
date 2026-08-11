// Function: current_exception
// Address: 00e4dfc0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::current_exception() */

void std::current_exception(void)

{
  undefined8 uVar1;
  undefined8 *in_x8;
  
  uVar1 = __cxa_current_primary_exception();
  *in_x8 = uVar1;
  return;
}



// ==========================================================================================
// Function: current_exception
// Address: 01ec5910
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::current_exception(void)

{
  (*(code *)PTR_current_exception_01ff5ea8)();
  return;
}



// ==========================================================================================
