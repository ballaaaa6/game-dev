// Function: notify_one
// Address: 00e8a1a4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::condition_variable::notify_one() */

int std::__ndk1::condition_variable::notify_one(void)

{
  int iVar1;
  pthread_cond_t *in_x0;
  
                    /* try { // try from 00e8a1b0 to 00e8a1b3 has its CatchHandler @ 00e8a1c0 */
  iVar1 = pthread_cond_signal(in_x0);
  return iVar1;
}



// ==========================================================================================
// Function: notify_all
// Address: 00e8a1c4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::condition_variable::notify_all() */

int std::__ndk1::condition_variable::notify_all(void)

{
  int iVar1;
  pthread_cond_t *in_x0;
  
                    /* try { // try from 00e8a1d0 to 00e8a1d3 has its CatchHandler @ 00e8a1e0 */
  iVar1 = pthread_cond_broadcast(in_x0);
  return iVar1;
}



// ==========================================================================================
// Function: notify_all_at_thread_exit
// Address: 00e8a300
// ==========================================================================================

/* std::__ndk1::notify_all_at_thread_exit(std::__ndk1::condition_variable&,
   std::__ndk1::unique_lock<std::__ndk1::mutex>) */

void std::__ndk1::notify_all_at_thread_exit(mutex *param_1,undefined8 *param_2)

{
  pthread_key_t *ppVar1;
  void *pvVar2;
  __thread_struct *this;
  condition_variable *pcVar3;
  
  ppVar1 = (pthread_key_t *)__thread_local_data();
  pvVar2 = pthread_getspecific(*ppVar1);
  if (pvVar2 == (void *)0x0) {
    this = (__thread_struct *)operator_new(8);
                    /* try { // try from 00e8a33c to 00e8a33f has its CatchHandler @ 00e8a37c */
    __thread_struct::__thread_struct(this);
    pthread_setspecific(*ppVar1,this);
  }
  ppVar1 = (pthread_key_t *)__thread_local_data();
  pcVar3 = (condition_variable *)pthread_getspecific(*ppVar1);
  *param_2 = 0;
  *(undefined *)(param_2 + 1) = 0;
  __thread_struct::notify_all_at_thread_exit(pcVar3,param_1);
  return;
}



// ==========================================================================================
// Function: notify_all_at_thread_exit
// Address: 00e9409c
// ==========================================================================================

/* std::__ndk1::__thread_struct::notify_all_at_thread_exit(std::__ndk1::condition_variable*,
   std::__ndk1::mutex*) */

void std::__ndk1::__thread_struct::notify_all_at_thread_exit
               (condition_variable *param_1,mutex *param_2)

{
  FUN_00e93e20(*(undefined8 *)param_1);
  return;
}



// ==========================================================================================
// Function: notify_one
// Address: 01ec6cb0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::condition_variable::notify_one(void)

{
  (*(code *)PTR_notify_one_01ff6878)();
  return;
}



// ==========================================================================================
// Function: notify_all_at_thread_exit
// Address: 01ec6d30
// ==========================================================================================

void std::__ndk1::__thread_struct::notify_all_at_thread_exit
               (condition_variable *param_1,mutex *param_2)

{
  (*(code *)PTR_notify_all_at_thread_exit_01ff68b8)();
  return;
}



// ==========================================================================================
// Function: notify_all
// Address: 01ec6fa0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::condition_variable::notify_all(void)

{
  (*(code *)PTR_notify_all_01ff69f0)();
  return;
}



// ==========================================================================================
