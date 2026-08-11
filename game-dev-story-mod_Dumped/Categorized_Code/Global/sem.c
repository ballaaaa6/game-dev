// Function: sem_post
// Address: 01ec6020
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_post(sem_t *__sem)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sem_post_01ff6230)((int)__sem);
  return iVar1;
}



// ==========================================================================================
// Function: sem_timedwait
// Address: 01ec6050
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_timedwait(sem_t *__sem,timespec *__abstime)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sem_timedwait_01ff6248)((int)__sem);
  return iVar1;
}



// ==========================================================================================
// Function: sem_wait
// Address: 01ec6060
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_wait(sem_t *__sem)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sem_wait_01ff6250)((int)__sem);
  return iVar1;
}



// ==========================================================================================
// Function: sem_init
// Address: 01ec6070
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_init(sem_t *__sem,int __pshared,uint __value)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sem_init_01ff6258)((int)__sem,__pshared,__value);
  return iVar1;
}



// ==========================================================================================
// Function: sem_getvalue
// Address: 01ec6090
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_getvalue(sem_t *__sem,int *__sval)

{
  int iVar1;
  
  iVar1 = (*(code *)PTR_sem_getvalue_01ff6268)((int)__sem);
  return iVar1;
}



// ==========================================================================================
// Function: sem_getvalue
// Address: 0231f560
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_getvalue(sem_t *__sem,int *__sval)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: sem_init
// Address: 0231f568
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_init(sem_t *__sem,int __pshared,uint __value)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: sem_post
// Address: 0231f570
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_post(sem_t *__sem)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: sem_timedwait
// Address: 0231f578
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_timedwait(sem_t *__sem,timespec *__abstime)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: sem_wait
// Address: 0231f580
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int sem_wait(sem_t *__sem)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
