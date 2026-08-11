// Function: try_lock
// Address: 00e89a04
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::mutex::try_lock() */

bool std::__ndk1::mutex::try_lock(void)

{
  int iVar1;
  pthread_mutex_t *in_x0;
  
                    /* try { // try from 00e89a10 to 00e89a13 has its CatchHandler @ 00e89a28 */
  iVar1 = pthread_mutex_trylock(in_x0);
  return iVar1 == 0;
}



// ==========================================================================================
// Function: try_lock
// Address: 00e89b84
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::recursive_mutex::try_lock() */

bool std::__ndk1::recursive_mutex::try_lock(void)

{
  int iVar1;
  pthread_mutex_t *in_x0;
  
                    /* try { // try from 00e89b90 to 00e89b93 has its CatchHandler @ 00e89ba8 */
  iVar1 = pthread_mutex_trylock(in_x0);
  return iVar1 == 0;
}



// ==========================================================================================
// Function: try_lock
// Address: 00e89cf0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::timed_mutex::try_lock() */

bool std::__ndk1::timed_mutex::try_lock(void)

{
  bool bVar1;
  int iVar2;
  pthread_mutex_t *in_x0;
  
                    /* try { // try from 00e89d04 to 00e89d07 has its CatchHandler @ 00e89d4c */
  iVar2 = pthread_mutex_trylock(in_x0);
  if (iVar2 == 0) {
    bVar1 = *(char *)((long)in_x0 + 0x58) == '\0';
    if (*(char *)((long)in_x0 + 0x58) == '\0') {
      *(undefined *)((long)in_x0 + 0x58) = 1;
    }
                    /* try { // try from 00e89d2c to 00e89d33 has its CatchHandler @ 00e89d48 */
    pthread_mutex_unlock(in_x0);
  }
  else {
    bVar1 = false;
  }
  return bVar1;
}



// ==========================================================================================
// Function: try_lock
// Address: 00e89f58
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::recursive_timed_mutex::try_lock() */

undefined4 std::__ndk1::recursive_timed_mutex::try_lock(void)

{
  int iVar1;
  pthread_mutex_t *in_x0;
  pthread_t __thread1;
  pthread_t __thread2;
  long lVar2;
  undefined4 uVar3;
  
  __thread1 = pthread_self();
                    /* try { // try from 00e89f74 to 00e89f7b has its CatchHandler @ 00e89ff4 */
  iVar1 = pthread_mutex_trylock(in_x0);
  if (iVar1 != 0) {
    return 0;
  }
  lVar2 = *(long *)((long)in_x0 + 0x58);
  if (lVar2 == 0) {
LAB_00e89fbc:
    *(long *)((long)in_x0 + 0x58) = lVar2 + 1;
    *(pthread_t *)((long)in_x0 + 0x60) = __thread1;
    uVar3 = 1;
  }
  else {
    __thread2 = *(pthread_t *)((long)in_x0 + 0x60);
    if (__thread1 == 0) {
      if (__thread2 == 0) goto LAB_00e89fb4;
    }
    else {
                    /* try { // try from 00e89f9c to 00e89fa3 has its CatchHandler @ 00e89fec */
      if ((__thread2 != 0) && (iVar1 = pthread_equal(__thread1,__thread2), iVar1 != 0)) {
        lVar2 = *(long *)((long)in_x0 + 0x58);
LAB_00e89fb4:
        if (lVar2 != -1) goto LAB_00e89fbc;
      }
    }
    uVar3 = 0;
  }
                    /* try { // try from 00e89fd0 to 00e89fd7 has its CatchHandler @ 00e89ff0 */
  pthread_mutex_unlock(in_x0);
  return uVar3;
}



// ==========================================================================================
