// Function: ~bad_function_call
// Address: 00e36d50
// ==========================================================================================

/* std::__ndk1::bad_function_call::~bad_function_call() */

void __thiscall std::__ndk1::bad_function_call::~bad_function_call(bad_function_call *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~bad_weak_ptr
// Address: 00e8966c
// ==========================================================================================

/* std::__ndk1::bad_weak_ptr::~bad_weak_ptr() */

void __thiscall std::__ndk1::bad_weak_ptr::~bad_weak_ptr(bad_weak_ptr *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  return;
}



// ==========================================================================================
// Function: ~bad_weak_ptr
// Address: 00e89674
// ==========================================================================================

/* std::__ndk1::bad_weak_ptr::~bad_weak_ptr() */

void __thiscall std::__ndk1::bad_weak_ptr::~bad_weak_ptr(bad_weak_ptr *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~bad_alloc
// Address: 00eac97c
// ==========================================================================================

/* std::bad_alloc::~bad_alloc() */

void __thiscall std::bad_alloc::~bad_alloc(bad_alloc *this)

{
  return;
}



// ==========================================================================================
// Function: ~bad_exception
// Address: 00eac99c
// ==========================================================================================

/* std::bad_exception::~bad_exception() */

void __thiscall std::bad_exception::~bad_exception(bad_exception *this)

{
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: bad_alloc
// Address: 00eac9b4
// ==========================================================================================

/* std::bad_alloc::bad_alloc() */

void __thiscall std::bad_alloc::bad_alloc(bad_alloc *this)

{
  *(undefined **)this = PTR_vtable_01ff5a00 + 0x10;
  return;
}



// ==========================================================================================
// Function: ~bad_alloc
// Address: 00eac9cc
// ==========================================================================================

/* std::bad_alloc::~bad_alloc() */

void __thiscall std::bad_alloc::~bad_alloc(bad_alloc *this)

{
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: bad_array_new_length
// Address: 00eac9e4
// ==========================================================================================

/* std::bad_array_new_length::bad_array_new_length() */

void __thiscall std::bad_array_new_length::bad_array_new_length(bad_array_new_length *this)

{
  *(undefined **)this = PTR_vtable_01ff5a08 + 0x10;
  return;
}



// ==========================================================================================
// Function: ~bad_array_new_length
// Address: 00eac9fc
// ==========================================================================================

/* std::bad_array_new_length::~bad_array_new_length() */

void __thiscall std::bad_array_new_length::~bad_array_new_length(bad_array_new_length *this)

{
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: bad_cast
// Address: 00eace78
// ==========================================================================================

/* std::bad_cast::bad_cast() */

void __thiscall std::bad_cast::bad_cast(bad_cast *this)

{
  *(undefined **)this = PTR_vtable_01ff5a10 + 0x10;
  return;
}



// ==========================================================================================
// Function: ~bad_cast
// Address: 00eace90
// ==========================================================================================

/* std::bad_cast::~bad_cast() */

void __thiscall std::bad_cast::~bad_cast(bad_cast *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  return;
}



// ==========================================================================================
// Function: ~bad_cast
// Address: 00eace98
// ==========================================================================================

/* std::bad_cast::~bad_cast() */

void __thiscall std::bad_cast::~bad_cast(bad_cast *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: bad_typeid
// Address: 00eaced4
// ==========================================================================================

/* std::bad_typeid::bad_typeid() */

void __thiscall std::bad_typeid::bad_typeid(bad_typeid *this)

{
  *(undefined **)this = PTR_vtable_01ff5a18 + 0x10;
  return;
}



// ==========================================================================================
// Function: ~bad_typeid
// Address: 00eaceec
// ==========================================================================================

/* std::bad_typeid::~bad_typeid() */

void __thiscall std::bad_typeid::~bad_typeid(bad_typeid *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  return;
}



// ==========================================================================================
// Function: ~bad_typeid
// Address: 00eacef4
// ==========================================================================================

/* std::bad_typeid::~bad_typeid() */

void __thiscall std::bad_typeid::~bad_typeid(bad_typeid *this)

{
  bad_alloc::~bad_alloc((bad_alloc *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: bad_cast
// Address: 01ec5a20
// ==========================================================================================

void __thiscall std::bad_cast::bad_cast(bad_cast *this)

{
  (*(code *)PTR_bad_cast_01ff5f30)();
  return;
}



// ==========================================================================================
// Function: ~bad_alloc
// Address: 01ec5f40
// ==========================================================================================

void __thiscall std::bad_alloc::~bad_alloc(bad_alloc *this)

{
  (*(code *)PTR__bad_alloc_01ff61c0)();
  return;
}



// ==========================================================================================
// Function: bad_alloc
// Address: 01ec6d50
// ==========================================================================================

void __thiscall std::bad_alloc::bad_alloc(bad_alloc *this)

{
  (*(code *)PTR_bad_alloc_01ff68c8)();
  return;
}



// ==========================================================================================
// Function: ~bad_alloc
// Address: 01ec7160
// ==========================================================================================

void __thiscall std::bad_alloc::~bad_alloc(bad_alloc *this)

{
  (*(code *)PTR__bad_alloc_01ff6ad0)();
  return;
}



// ==========================================================================================
