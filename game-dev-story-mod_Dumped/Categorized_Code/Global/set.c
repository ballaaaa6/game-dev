// Function: set_value
// Address: 00e9441c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__assoc_sub_state::set_value() */

void std::__ndk1::__assoc_sub_state::set_value(void)

{
  long lVar1;
  long in_x0;
  long lVar2;
  undefined8 local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  mutex::lock();
  if ((*(byte *)(in_x0 + 0x70) & 1) == 0) {
    local_40 = 0;
    lVar2 = *(long *)(in_x0 + 0x10);
    exception_ptr::~exception_ptr((exception_ptr *)&local_40);
    if (lVar2 == 0) {
      *(uint *)(in_x0 + 0x70) = *(uint *)(in_x0 + 0x70) | 5;
      condition_variable::notify_all();
      mutex::unlock();
      if (*(long *)(lVar1 + 0x28) == local_38) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* try { // try from 00e944b4 to 00e944bb has its CatchHandler @ 00e944c0 */
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(2);
}



// ==========================================================================================
// Function: set_value_at_thread_exit
// Address: 00e9459c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__assoc_sub_state::set_value_at_thread_exit() */

void std::__ndk1::__assoc_sub_state::set_value_at_thread_exit(void)

{
  long lVar1;
  long in_x0;
  pthread_key_t *ppVar2;
  __assoc_sub_state *p_Var3;
  long lVar4;
  undefined8 local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  mutex::lock();
  if ((*(byte *)(in_x0 + 0x70) & 1) == 0) {
    local_40 = 0;
    lVar4 = *(long *)(in_x0 + 0x10);
    exception_ptr::~exception_ptr((exception_ptr *)&local_40);
    if (lVar4 == 0) {
      *(uint *)(in_x0 + 0x70) = *(uint *)(in_x0 + 0x70) | 1;
                    /* try { // try from 00e945f8 to 00e94643 has its CatchHandler @ 00e94648 */
      ppVar2 = (pthread_key_t *)__thread_local_data();
      p_Var3 = (__assoc_sub_state *)pthread_getspecific(*ppVar2);
      __thread_struct::__make_ready_at_thread_exit(p_Var3);
      mutex::unlock();
      if (*(long *)(lVar1 + 0x28) == local_38) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(2);
}



// ==========================================================================================
// Function: set_exception
// Address: 00e9465c
// ==========================================================================================

/* std::__ndk1::__assoc_sub_state::set_exception(std::exception_ptr) */

void __thiscall
std::__ndk1::__assoc_sub_state::set_exception(__assoc_sub_state *this,exception_ptr *param_2)

{
  long lVar1;
  long lVar2;
  undefined8 local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  mutex::lock();
  if (((byte)this[0x70] & 1) == 0) {
    local_50 = 0;
    lVar2 = *(long *)(this + 0x10);
    exception_ptr::~exception_ptr((exception_ptr *)&local_50);
    if (lVar2 == 0) {
      exception_ptr::operator=((exception_ptr *)(this + 0x10),param_2);
      *(uint *)(this + 0x70) = *(uint *)(this + 0x70) | 4;
      condition_variable::notify_all();
      mutex::unlock();
      if (*(long *)(lVar1 + 0x28) == local_48) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* try { // try from 00e94708 to 00e9470f has its CatchHandler @ 00e94714 */
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(2);
}



// ==========================================================================================
// Function: set_exception_at_thread_exit
// Address: 00e94728
// ==========================================================================================

/* std::__ndk1::__assoc_sub_state::set_exception_at_thread_exit(std::exception_ptr) */

void __thiscall
std::__ndk1::__assoc_sub_state::set_exception_at_thread_exit
          (__assoc_sub_state *this,exception_ptr *param_2)

{
  long lVar1;
  pthread_key_t *ppVar2;
  __assoc_sub_state *p_Var3;
  long lVar4;
  undefined8 local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  mutex::lock();
  if (((byte)this[0x70] & 1) == 0) {
    local_50 = 0;
    lVar4 = *(long *)(this + 0x10);
    exception_ptr::~exception_ptr((exception_ptr *)&local_50);
    if (lVar4 == 0) {
      exception_ptr::operator=((exception_ptr *)(this + 0x10),param_2);
                    /* try { // try from 00e9478c to 00e947db has its CatchHandler @ 00e947e0 */
      ppVar2 = (pthread_key_t *)__thread_local_data();
      p_Var3 = (__assoc_sub_state *)pthread_getspecific(*ppVar2);
      __thread_struct::__make_ready_at_thread_exit(p_Var3);
      mutex::unlock();
      if (*(long *)(lVar1 + 0x28) == local_48) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(2);
}



// ==========================================================================================
// Function: set_value
// Address: 00e94ef4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::promise<void>::set_value() */

void std::__ndk1::promise<void>::set_value(void)

{
  long *in_x0;
  
  if (*in_x0 != 0) {
    __assoc_sub_state::set_value();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(3);
}



// ==========================================================================================
// Function: set_exception
// Address: 00e94f1c
// ==========================================================================================

/* std::__ndk1::promise<void>::set_exception(std::exception_ptr) */

void __thiscall
std::__ndk1::promise<void>::set_exception(promise<void> *this,exception_ptr *param_2)

{
  long lVar1;
  __assoc_sub_state *p_Var2;
  exception_ptr aeStack_30 [8];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  p_Var2 = *(__assoc_sub_state **)this;
  if (p_Var2 == (__assoc_sub_state *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e944d4(3);
  }
  exception_ptr::exception_ptr(aeStack_30,param_2);
                    /* try { // try from 00e94f4c to 00e94f57 has its CatchHandler @ 00e94f90 */
  __assoc_sub_state::set_exception(p_Var2,aeStack_30);
  exception_ptr::~exception_ptr(aeStack_30);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: set_value_at_thread_exit
// Address: 00e94fa4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::promise<void>::set_value_at_thread_exit() */

void std::__ndk1::promise<void>::set_value_at_thread_exit(void)

{
  long *in_x0;
  
  if (*in_x0 != 0) {
    __assoc_sub_state::set_value_at_thread_exit();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(3);
}



// ==========================================================================================
// Function: set_exception_at_thread_exit
// Address: 00e94fcc
// ==========================================================================================

/* std::__ndk1::promise<void>::set_exception_at_thread_exit(std::exception_ptr) */

void __thiscall
std::__ndk1::promise<void>::set_exception_at_thread_exit(promise<void> *this,exception_ptr *param_2)

{
  long lVar1;
  __assoc_sub_state *p_Var2;
  exception_ptr aeStack_30 [8];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  p_Var2 = *(__assoc_sub_state **)this;
  if (p_Var2 == (__assoc_sub_state *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e944d4(3);
  }
  exception_ptr::exception_ptr(aeStack_30,param_2);
                    /* try { // try from 00e94ffc to 00e95007 has its CatchHandler @ 00e95040 */
  __assoc_sub_state::set_exception_at_thread_exit(p_Var2,aeStack_30);
  exception_ptr::~exception_ptr(aeStack_30);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: set_new_handler
// Address: 00e95e68
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::set_new_handler(void (*)()) */

undefined8 std::set_new_handler(_func_void *param_1)

{
  char cVar1;
  bool bVar2;
  undefined *puVar3;
  undefined8 uVar4;
  
  puVar3 = PTR___cxa_new_handler_01ff5998;
  do {
    uVar4 = *(undefined8 *)puVar3;
    cVar1 = '\x01';
    bVar2 = (bool)ExclusiveMonitorPass(puVar3,0x10);
    if (bVar2) {
      *(_func_void **)puVar3 = param_1;
      cVar1 = ExclusiveMonitorsStatus();
    }
  } while (cVar1 != '\0');
  return uVar4;
}



// ==========================================================================================
// Function: set_unexpected
// Address: 00e95fe0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::set_unexpected(void (*)()) */

undefined8 std::set_unexpected(_func_void *param_1)

{
  code *pcVar1;
  char cVar2;
  bool bVar3;
  undefined *puVar4;
  undefined8 uVar5;
  
  puVar4 = PTR___cxa_unexpected_handler_01ff5988;
  pcVar1 = FUN_00e95fc0;
  if (param_1 != (_func_void *)0x0) {
    pcVar1 = param_1;
  }
  do {
    uVar5 = *(undefined8 *)puVar4;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
    if (bVar3) {
      *(code **)puVar4 = pcVar1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  return uVar5;
}



// ==========================================================================================
// Function: set_terminate
// Address: 00e9600c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::set_terminate(void (*)()) */

undefined8 std::set_terminate(_func_void *param_1)

{
  code *pcVar1;
  char cVar2;
  bool bVar3;
  undefined *puVar4;
  undefined8 uVar5;
  
  puVar4 = PTR___cxa_terminate_handler_01ff5990;
  pcVar1 = FUN_00e95e9c;
  if (param_1 != (_func_void *)0x0) {
    pcVar1 = param_1;
  }
  do {
    uVar5 = *(undefined8 *)puVar4;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
    if (bVar3) {
      *(code **)puVar4 = pcVar1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  return uVar5;
}



// ==========================================================================================
// Function: set_exception
// Address: 01ec7020
// ==========================================================================================

void __thiscall std::__ndk1::__assoc_sub_state::set_exception(void)

{
  (*(code *)PTR_set_exception_01ff6a30)();
  return;
}



// ==========================================================================================
// Function: set_value
// Address: 01ec7050
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__assoc_sub_state::set_value(void)

{
  (*(code *)PTR_set_value_01ff6a48)();
  return;
}



// ==========================================================================================
// Function: set_value_at_thread_exit
// Address: 01ec7060
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__assoc_sub_state::set_value_at_thread_exit(void)

{
  (*(code *)PTR_set_value_at_thread_exit_01ff6a50)();
  return;
}



// ==========================================================================================
// Function: set_exception_at_thread_exit
// Address: 01ec7070
// ==========================================================================================

void __thiscall std::__ndk1::__assoc_sub_state::set_exception_at_thread_exit(void)

{
  (*(code *)PTR_set_exception_at_thread_exit_01ff6a58)();
  return;
}



// ==========================================================================================
