// Function: timed_mutex
// Address: 00e89bac
// ==========================================================================================

/* std::__ndk1::timed_mutex::timed_mutex() */

void __thiscall std::__ndk1::timed_mutex::timed_mutex(timed_mutex *this)

{
  *(undefined8 *)(this + 0x51) = 0;
  *(undefined8 *)(this + 0x49) = 0;
  *(undefined8 *)(this + 0x38) = 0;
  *(undefined8 *)(this + 0x30) = 0;
  *(undefined8 *)(this + 0x48) = 0;
  *(undefined8 *)(this + 0x40) = 0;
  *(undefined8 *)(this + 0x18) = 0;
  *(undefined8 *)(this + 0x10) = 0;
  *(undefined8 *)(this + 0x28) = 0;
  *(undefined8 *)(this + 0x20) = 0;
  *(undefined8 *)(this + 8) = 0;
  *(undefined8 *)this = 0;
  return;
}



// ==========================================================================================
// Function: ~timed_mutex
// Address: 00e89bc8
// ==========================================================================================

/* std::__ndk1::timed_mutex::~timed_mutex() */

void __thiscall std::__ndk1::timed_mutex::~timed_mutex(timed_mutex *this)

{
  int iVar1;
  
                    /* try { // try from 00e89bdc to 00e89bdf has its CatchHandler @ 00e89c18 */
  iVar1 = pthread_mutex_lock((pthread_mutex_t *)this);
  if (iVar1 == 0) {
                    /* try { // try from 00e89be4 to 00e89beb has its CatchHandler @ 00e89c14 */
    pthread_mutex_unlock((pthread_mutex_t *)this);
    condition_variable::~condition_variable((condition_variable *)(this + 0x28));
    mutex::~mutex((mutex *)this);
    return;
  }
                    /* try { // try from 00e89c08 to 00e89c13 has its CatchHandler @ 00e89c18 */
                    /* WARNING: Subroutine does not return */
  __throw_system_error(iVar1,"mutex lock failed");
}



// ==========================================================================================
