// Function: future_category
// Address: 00e942a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::future_category() */

undefined8 * std::__ndk1::future_category(void)

{
  int iVar1;
  
  if (((DAT_0231e030 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231e030), iVar1 != 0)) {
    error_category::error_category((error_category *)&DAT_0231e028);
    DAT_0231e028 = &PTR__error_category_01fbbac0;
    __cxa_atexit(PTR__error_category_01ff5660,&DAT_0231e028,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231e030);
  }
  return &DAT_0231e028;
}



// ==========================================================================================
// Function: future_error
// Address: 00e9432c
// ==========================================================================================

/* std::__ndk1::future_error::future_error(std::__ndk1::error_code) */

void __thiscall
std::__ndk1::future_error::future_error(future_error *this,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  basic_string local_50 [16];
  void *local_40;
  undefined8 local_38;
  undefined8 uStack_30;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_38 = param_2;
  uStack_30 = param_3;
  error_code::message();
                    /* try { // try from 00e94360 to 00e9436b has its CatchHandler @ 00e943bc */
  logic_error::logic_error((logic_error *)this,local_50);
  if (((byte)local_50[0] & 1) != 0) {
    operator_delete(local_40);
  }
  *(undefined **)this = PTR_vtable_01ff5968 + 0x10;
  *(undefined8 *)(this + 0x18) = uStack_30;
  *(undefined8 *)(this + 0x10) = local_38;
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~future_error
// Address: 00e943d8
// ==========================================================================================

/* std::__ndk1::future_error::~future_error() */

void __thiscall std::__ndk1::future_error::~future_error(future_error *this)

{
  domain_error::~domain_error((domain_error *)this);
  return;
}



// ==========================================================================================
// Function: ~future_error
// Address: 00e943e0
// ==========================================================================================

/* std::__ndk1::future_error::~future_error() */

void __thiscall std::__ndk1::future_error::~future_error(future_error *this)

{
  domain_error::~domain_error((domain_error *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: future_error
// Address: 01ec6ff0
// ==========================================================================================

void __thiscall std::__ndk1::future_error::future_error(void)

{
  (*(code *)PTR_future_error_01ff6a18)();
  return;
}



// ==========================================================================================
// Function: ~future_error
// Address: 01ec7030
// ==========================================================================================

void __thiscall std::__ndk1::future_error::~future_error(future_error *this)

{
  (*(code *)PTR__future_error_01ff6a38)();
  return;
}



// ==========================================================================================
