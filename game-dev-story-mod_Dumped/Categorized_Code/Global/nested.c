// Function: nested_exception
// Address: 00e4df84
// ==========================================================================================

/* std::nested_exception::nested_exception() */

void __thiscall std::nested_exception::nested_exception(nested_exception *this)

{
  undefined8 uVar1;
  
  *(undefined **)this = PTR_vtable_01ff55e8 + 0x10;
  uVar1 = __cxa_current_primary_exception();
  *(undefined8 *)(this + 8) = uVar1;
  return;
}



// ==========================================================================================
// Function: ~nested_exception
// Address: 00e4dfec
// ==========================================================================================

/* std::nested_exception::~nested_exception() */

void __thiscall std::nested_exception::~nested_exception(nested_exception *this)

{
  *(undefined **)this = PTR_vtable_01ff55e8 + 0x10;
  __cxa_decrement_exception_refcount(*(undefined8 *)(this + 8));
  return;
}



// ==========================================================================================
// Function: ~nested_exception
// Address: 00e4e00c
// ==========================================================================================

/* std::nested_exception::~nested_exception() */

void __thiscall std::nested_exception::~nested_exception(nested_exception *this)

{
  *(undefined **)this = PTR_vtable_01ff55e8 + 0x10;
  __cxa_decrement_exception_refcount(*(undefined8 *)(this + 8));
  operator_delete(this);
  return;
}



// ==========================================================================================
