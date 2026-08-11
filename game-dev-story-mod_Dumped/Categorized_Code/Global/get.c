// Function: get_pointer_safety
// Address: 00e89974
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::get_pointer_safety() */

undefined8 std::__ndk1::get_pointer_safety(void)

{
  return 0;
}



// ==========================================================================================
// Function: get_future
// Address: 00e94e78
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::promise<void>::get_future() */

void std::__ndk1::promise<void>::get_future(void)

{
  long *in_x0;
  long *in_x8;
  long lVar1;
  
  lVar1 = *in_x0;
  if (lVar1 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e944d4(3);
  }
  *in_x8 = lVar1;
  mutex::lock();
  if ((*(byte *)(lVar1 + 0x70) >> 1 & 1) == 0) {
    __shared_count::__add_shared();
    *(uint *)(lVar1 + 0x70) = *(uint *)(lVar1 + 0x70) | 2;
    mutex::unlock();
    return;
  }
                    /* try { // try from 00e94ed8 to 00e94edf has its CatchHandler @ 00e94ee0 */
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(1);
}



// ==========================================================================================
// Function: get_unexpected
// Address: 00e95d80
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::get_unexpected() */

undefined8 std::get_unexpected(void)

{
  return *(undefined8 *)PTR___cxa_unexpected_handler_01ff5988;
}



// ==========================================================================================
// Function: get_terminate
// Address: 00e95e10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::get_terminate() */

undefined8 std::get_terminate(void)

{
  return *(undefined8 *)PTR___cxa_terminate_handler_01ff5990;
}



// ==========================================================================================
// Function: get_new_handler
// Address: 00e95e88
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::get_new_handler() */

undefined8 std::get_new_handler(void)

{
  return *(undefined8 *)PTR___cxa_new_handler_01ff5998;
}



// ==========================================================================================
// Function: get_new_handler
// Address: 01ec6d60
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::get_new_handler(void)

{
  (*(code *)PTR_get_new_handler_01ff68d0)();
  return;
}



// ==========================================================================================
// Function: get_unexpected
// Address: 01ec70a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::get_unexpected(void)

{
  (*(code *)PTR_get_unexpected_01ff6a70)();
  return;
}



// ==========================================================================================
// Function: get_terminate
// Address: 01ec70b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::get_terminate(void)

{
  (*(code *)PTR_get_terminate_01ff6a78)();
  return;
}



// ==========================================================================================
