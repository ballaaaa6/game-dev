// Function: recursive_mutex
// Address: 00e89a4c
// ==========================================================================================

/* std::__ndk1::recursive_mutex::recursive_mutex() */

void __thiscall std::__ndk1::recursive_mutex::recursive_mutex(recursive_mutex *this)

{
  long lVar1;
  int iVar2;
  int local_44;
  pthread_mutexattr_t apStack_40 [2];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_44 = pthread_mutexattr_init(apStack_40);
  if (local_44 == 0) {
    local_44 = pthread_mutexattr_settype(apStack_40,1);
    if (local_44 == 0) {
      local_44 = pthread_mutex_init((pthread_mutex_t *)this,apStack_40);
      iVar2 = pthread_mutexattr_destroy(apStack_40);
      if (local_44 == 0) {
        if (iVar2 == 0) {
          if (*(long *)(lVar1 + 0x28) != local_38) {
                    /* WARNING: Subroutine does not return */
            __stack_chk_fail();
          }
          return;
        }
        pthread_mutex_destroy((pthread_mutex_t *)this);
        local_44 = iVar2;
      }
    }
    else {
      pthread_mutexattr_destroy(apStack_40);
    }
  }
                    /* WARNING: Subroutine does not return */
  __throw_system_error(local_44,"recursive_mutex constructor failed");
}



// ==========================================================================================
// Function: ~recursive_mutex
// Address: 00e89b18
// ==========================================================================================

/* std::__ndk1::recursive_mutex::~recursive_mutex() */

int __thiscall std::__ndk1::recursive_mutex::~recursive_mutex(recursive_mutex *this)

{
  int iVar1;
  
                    /* try { // try from 00e89b24 to 00e89b27 has its CatchHandler @ 00e89b34 */
  iVar1 = pthread_mutex_destroy((pthread_mutex_t *)this);
  return iVar1;
}



// ==========================================================================================
// Function: recursive_timed_mutex
// Address: 00e89da4
// ==========================================================================================

/* std::__ndk1::recursive_timed_mutex::recursive_timed_mutex() */

void __thiscall
std::__ndk1::recursive_timed_mutex::recursive_timed_mutex(recursive_timed_mutex *this)

{
  *(undefined8 *)(this + 0x60) = 0;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x40) = 0;
  *(undefined8 *)(this + 0x58) = 0;
  *(undefined8 *)(this + 0x50) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 0x38) = 0;
  *(undefined8 *)(this + 0x30) = 0;
  *(undefined8 *)(this + 8) = 0;
  *(undefined8 *)this = 0;
  *(undefined8 *)(this + 0x18) = 0;
  *(undefined8 *)(this + 0x10) = 0;
  return;
}



// ==========================================================================================
// Function: ~recursive_timed_mutex
// Address: 00e89dc0
// ==========================================================================================

/* std::__ndk1::recursive_timed_mutex::~recursive_timed_mutex() */

void __thiscall
std::__ndk1::recursive_timed_mutex::~recursive_timed_mutex(recursive_timed_mutex *this)

{
  int iVar1;
  
                    /* try { // try from 00e89dd4 to 00e89dd7 has its CatchHandler @ 00e89e10 */
  iVar1 = pthread_mutex_lock((pthread_mutex_t *)this);
  if (iVar1 == 0) {
                    /* try { // try from 00e89ddc to 00e89de3 has its CatchHandler @ 00e89e0c */
    pthread_mutex_unlock((pthread_mutex_t *)this);
    condition_variable::~condition_variable((condition_variable *)(this + 0x28));
    mutex::~mutex((mutex *)this);
    return;
  }
                    /* try { // try from 00e89e00 to 00e89e0b has its CatchHandler @ 00e89e10 */
                    /* WARNING: Subroutine does not return */
  __throw_system_error(iVar1,"mutex lock failed");
}



// ==========================================================================================
