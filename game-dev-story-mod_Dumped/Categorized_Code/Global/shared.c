// Function: ~shared_future
// Address: 00e95054
// ==========================================================================================

/* std::__ndk1::shared_future<void>::~shared_future() */

void __thiscall std::__ndk1::shared_future<void>::~shared_future(shared_future<void> *this)

{
  if (*(long *)this != 0) {
    __shared_count::__release_shared();
    return;
  }
  return;
}



// ==========================================================================================
