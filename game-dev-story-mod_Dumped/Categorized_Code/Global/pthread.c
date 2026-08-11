// Function: pthread_self
// Address: 00dcba9c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

pthread_t pthread_self(void)

{
  pthread_t pVar1;
  
  pVar1 = (*(code *)PTR_pthread_self_01ff61a0)();
  return pVar1;
}



// ==========================================================================================
// Function: pthread_self
// Address: 00e2fb4c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

pthread_t pthread_self(void)

{
  pthread_t pVar1;
  
  pVar1 = (*(code *)PTR_pthread_self_01ff61a0)();
  return pVar1;
}



// ==========================================================================================
// Function: pthread_key_delete
// Address: 01ec57d0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_key_delete(pthread_key_t __key)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_key_delete_01ff5e08)(__key);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutex_init
// Address: 01ec57e0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_init(pthread_mutex_t *__mutex,pthread_mutexattr_t *__mutexattr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutex_init_01ff5e10)((int)__mutex);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutex_destroy
// Address: 01ec57f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_destroy(pthread_mutex_t *__mutex)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutex_destroy_01ff5e18)((int)__mutex);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutex_lock
// Address: 01ec5800
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_lock(pthread_mutex_t *__mutex)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutex_lock_01ff5e20)((int)__mutex);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutex_unlock
// Address: 01ec5810
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_unlock(pthread_mutex_t *__mutex)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutex_unlock_01ff5e28)((int)__mutex);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_getspecific
// Address: 01ec5820
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * pthread_getspecific(pthread_key_t __key)

{
  void *pvVar1;
  
  pvVar1 = (void *)(*(code *)PTR_pthread_getspecific_01ff5e30)(__key);
  return pvVar1;
}



// ==========================================================================================
// Function: pthread_setspecific
// Address: 01ec5830
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_setspecific(pthread_key_t __key,void *__pointer)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_setspecific_01ff5e38)(__key);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_key_create
// Address: 01ec5840
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_key_create(pthread_key_t *__key,__destr_function *__destr_function)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_key_create_01ff5e40)((int)__key);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_once
// Address: 01ec5880
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_once(pthread_once_t *__once_control,__init_routine *__init_routine)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_once_01ff5e60)((int)__once_control);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_attr_init
// Address: 01ec5ed0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_init(pthread_attr_t *__attr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_attr_init_01ff6188)((int)__attr);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_create
// Address: 01ec5ee0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_create(pthread_t *__newthread,pthread_attr_t *__attr,__start_routine *__start_routine,
                  void *__arg)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_create_01ff6190)((int)__newthread);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_attr_destroy
// Address: 01ec5ef0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_destroy(pthread_attr_t *__attr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_attr_destroy_01ff6198)((int)__attr);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_self
// Address: 01ec5f00
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

pthread_t pthread_self(void)

{
  pthread_t pVar1;
  
  pVar1 = (*(code *)PTR_pthread_self_01ff61a0)();
  return pVar1;
}



// ==========================================================================================
// Function: pthread_detach
// Address: 01ec5f10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_detach(pthread_t __th)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_detach_01ff61a8)((int)__th);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_setname_np
// Address: 01ec5f20
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_setname_np(pthread_t __target_thread,char *__name)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_setname_np_01ff61b0)((int)__target_thread);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_getattr_np
// Address: 01ec5fc0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_getattr_np(pthread_t __th,pthread_attr_t *__attr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_getattr_np_01ff6200)((int)__th);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_attr_getstack
// Address: 01ec5fd0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_getstack(pthread_attr_t *__attr,void **__stackaddr,size_t *__stacksize)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_attr_getstack_01ff6208)((int)__attr);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_atfork
// Address: 01ec5fe0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_atfork(__prepare *__prepare,__parent *__parent,__child *__child)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_atfork_01ff6210)((int)__prepare);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_sigmask
// Address: 01ec6010
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_sigmask(int __how,__sigset_t *__newmask,__sigset_t *__oldmask)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_sigmask_01ff6228)(__how);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_kill
// Address: 01ec6040
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_kill(pthread_t __threadid,int __signo)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_kill_01ff6240)((int)__threadid,__signo);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutex_trylock
// Address: 01ec6c30
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_trylock(pthread_mutex_t *__mutex)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutex_trylock_01ff6838)((int)__mutex);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutexattr_init
// Address: 01ec6c50
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_init(pthread_mutexattr_t *__attr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutexattr_init_01ff6848)((int)__attr);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutexattr_settype
// Address: 01ec6c60
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_settype(pthread_mutexattr_t *__attr,int __kind)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutexattr_settype_01ff6850)((int)__attr,__kind);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_mutexattr_destroy
// Address: 01ec6c70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_destroy(pthread_mutexattr_t *__attr)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_mutexattr_destroy_01ff6858)((int)__attr);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_equal
// Address: 01ec6cc0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_equal(pthread_t __thread1,pthread_t __thread2)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_equal_01ff6880)((int)__thread1);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_cond_wait
// Address: 01ec6cd0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_wait(pthread_cond_t *__cond,pthread_mutex_t *__mutex)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_cond_wait_01ff6888)((int)__cond);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_cond_broadcast
// Address: 01ec6ce0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_broadcast(pthread_cond_t *__cond)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_cond_broadcast_01ff6890)((int)__cond);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_cond_signal
// Address: 01ec6cf0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_signal(pthread_cond_t *__cond)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_cond_signal_01ff6898)((int)__cond);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_cond_timedwait
// Address: 01ec6d00
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_timedwait(pthread_cond_t *__cond,pthread_mutex_t *__mutex,timespec *__abstime)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_cond_timedwait_01ff68a0)((int)__cond);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_cond_destroy
// Address: 01ec6d40
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_destroy(pthread_cond_t *__cond)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_cond_destroy_01ff68c0)((int)__cond);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_join
// Address: 01ec6f80
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_join(pthread_t __th,void **__thread_return)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_join_01ff69e0)((int)__th);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_rwlock_rdlock
// Address: 01ec71a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_rdlock(pthread_rwlock_t *__rwlock)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_rwlock_rdlock_01ff6af0)((int)__rwlock);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_rwlock_unlock
// Address: 01ec71b0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_unlock(pthread_rwlock_t *__rwlock)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_rwlock_unlock_01ff6af8)((int)__rwlock);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_rwlock_wrlock
// Address: 01ec71c0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_wrlock(pthread_rwlock_t *__rwlock)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_pthread_rwlock_wrlock_01ff6b00)((int)__rwlock);
  return iVar1;
}



// ==========================================================================================
// Function: pthread_getspecific
// Address: 0231f250
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * pthread_getspecific(pthread_key_t __key)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_key_create
// Address: 0231f258
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_key_create(pthread_key_t *__key,__destr_function *__destr_function)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_key_delete
// Address: 0231f260
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_key_delete(pthread_key_t __key)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutex_destroy
// Address: 0231f268
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_destroy(pthread_mutex_t *__mutex)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutex_init
// Address: 0231f270
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_init(pthread_mutex_t *__mutex,pthread_mutexattr_t *__mutexattr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutex_lock
// Address: 0231f278
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_lock(pthread_mutex_t *__mutex)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutex_unlock
// Address: 0231f280
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_unlock(pthread_mutex_t *__mutex)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_setspecific
// Address: 0231f288
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_setspecific(pthread_key_t __key,void *__pointer)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_once
// Address: 0231f2b0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_once(pthread_once_t *__once_control,__init_routine *__init_routine)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_cond_broadcast
// Address: 0231f3b0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_broadcast(pthread_cond_t *__cond)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_cond_destroy
// Address: 0231f3b8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_destroy(pthread_cond_t *__cond)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_cond_signal
// Address: 0231f3c0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_signal(pthread_cond_t *__cond)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_cond_timedwait
// Address: 0231f3c8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_timedwait(pthread_cond_t *__cond,pthread_mutex_t *__mutex,timespec *__abstime)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_cond_wait
// Address: 0231f3d0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_cond_wait(pthread_cond_t *__cond,pthread_mutex_t *__mutex)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutexattr_destroy
// Address: 0231f440
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_destroy(pthread_mutexattr_t *__attr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutexattr_init
// Address: 0231f448
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_init(pthread_mutexattr_t *__attr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutexattr_settype
// Address: 0231f450
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutexattr_settype(pthread_mutexattr_t *__attr,int __kind)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_rwlock_rdlock
// Address: 0231f458
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_rdlock(pthread_rwlock_t *__rwlock)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_rwlock_unlock
// Address: 0231f460
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_unlock(pthread_rwlock_t *__rwlock)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_rwlock_wrlock
// Address: 0231f468
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_rwlock_wrlock(pthread_rwlock_t *__rwlock)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_attr_destroy
// Address: 0231f4d0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_destroy(pthread_attr_t *__attr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_attr_init
// Address: 0231f4d8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_init(pthread_attr_t *__attr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_create
// Address: 0231f4e0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_create(pthread_t *__newthread,pthread_attr_t *__attr,__start_routine *__start_routine,
                  void *__arg)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_detach
// Address: 0231f4e8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_detach(pthread_t __th)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_self
// Address: 0231f4f0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

pthread_t pthread_self(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_setname_np
// Address: 0231f4f8
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_setname_np(pthread_t __target_thread,char *__name)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_atfork
// Address: 0231f530
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_atfork(__prepare *__prepare,__parent *__parent,__child *__child)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_attr_getstack
// Address: 0231f538
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_attr_getstack(pthread_attr_t *__attr,void **__stackaddr,size_t *__stacksize)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_getattr_np
// Address: 0231f540
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_getattr_np(pthread_t __th,pthread_attr_t *__attr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_join
// Address: 0231f548
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_join(pthread_t __th,void **__thread_return)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_kill
// Address: 0231f550
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_kill(pthread_t __threadid,int __signo)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_sigmask
// Address: 0231f558
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_sigmask(int __how,__sigset_t *__newmask,__sigset_t *__oldmask)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_mutex_trylock
// Address: 0231f788
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_mutex_trylock(pthread_mutex_t *__mutex)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: pthread_equal
// Address: 0231f790
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int pthread_equal(pthread_t __thread1,pthread_t __thread2)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
