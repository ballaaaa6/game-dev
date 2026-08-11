// Function: rethrow_nested
// Address: 00e4e04c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::nested_exception::rethrow_nested() const */

void std::nested_exception::rethrow_nested(void)

{
  long in_x0;
  undefined8 uVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 local_28;
  
  lVar3 = *(long *)(in_x0 + 8);
  __cxa_decrement_exception_refcount(0);
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
    terminate();
  }
  uVar2 = *(undefined8 *)(in_x0 + 8);
  local_28 = uVar2;
  __cxa_increment_exception_refcount(uVar2);
                    /* try { // try from 00e4e088 to 00e4e08f has its CatchHandler @ 00e4e090 */
  uVar1 = rethrow_exception(&local_28);
                    /* catch() { ... } // from try @ 00e4e088 with catch @ 00e4e090 */
  __cxa_decrement_exception_refcount(uVar2);
                    /* WARNING: Subroutine does not return */
  FUN_00ead3e8(uVar1);
}



// ==========================================================================================
// Function: rethrow_exception
// Address: 00e4e0a4
// ==========================================================================================

/* std::rethrow_exception(std::exception_ptr) */

void std::rethrow_exception(undefined8 *param_1)

{
  __cxa_rethrow_primary_exception(*param_1);
                    /* WARNING: Subroutine does not return */
  terminate();
}



// ==========================================================================================
// Function: rethrow_exception
// Address: 01ec5900
// ==========================================================================================

void std::rethrow_exception(void)

{
  (*(code *)PTR_rethrow_exception_01ff5ea0)();
  return;
}



// ==========================================================================================
