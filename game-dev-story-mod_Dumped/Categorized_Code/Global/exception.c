// Function: ~exception_ptr
// Address: 00e4df14
// ==========================================================================================

/* std::exception_ptr::~exception_ptr() */

void __thiscall std::exception_ptr::~exception_ptr(exception_ptr *this)

{
  __cxa_decrement_exception_refcount(*(undefined8 *)this);
  return;
}



// ==========================================================================================
// Function: exception_ptr
// Address: 00e4df20
// ==========================================================================================

/* std::exception_ptr::exception_ptr(std::exception_ptr const&) */

void __thiscall std::exception_ptr::exception_ptr(exception_ptr *this,exception_ptr *param_1)

{
  undefined8 uVar1;
  
  uVar1 = *(undefined8 *)param_1;
  *(undefined8 *)this = uVar1;
  __cxa_increment_exception_refcount(uVar1);
  return;
}



// ==========================================================================================
// Function: ~exception_ptr
// Address: 01ec58e0
// ==========================================================================================

void __thiscall std::exception_ptr::~exception_ptr(exception_ptr *this)

{
  (*(code *)PTR__exception_ptr_01ff5e90)();
  return;
}



// ==========================================================================================
// Function: exception_ptr
// Address: 01ec58f0
// ==========================================================================================

void __thiscall std::exception_ptr::exception_ptr(exception_ptr *this,exception_ptr *param_1)

{
  (*(code *)PTR_exception_ptr_01ff5e98)();
  return;
}



// ==========================================================================================
