// Function: ~condition_variable
// Address: 00e8a390
// ==========================================================================================

/* std::__ndk1::condition_variable::~condition_variable() */

int __thiscall std::__ndk1::condition_variable::~condition_variable(condition_variable *this)

{
  int iVar1;
  
                    /* try { // try from 00e8a39c to 00e8a39f has its CatchHandler @ 00e8a3ac */
  iVar1 = pthread_cond_destroy((pthread_cond_t *)this);
  return iVar1;
}



// ==========================================================================================
// Function: ~condition_variable
// Address: 01ec6c80
// ==========================================================================================

void __thiscall std::__ndk1::condition_variable::~condition_variable(condition_variable *this)

{
  (*(code *)PTR__condition_variable_01ff6860)();
  return;
}



// ==========================================================================================
