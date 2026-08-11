// Function: sleep_for
// Address: 00e93be8
// ==========================================================================================

/* std::__ndk1::this_thread::sleep_for(std::__ndk1::chrono::duration<long long,
   std::__ndk1::ratio<1l, 1000000000l> > const&) */

void std::__ndk1::this_thread::sleep_for(duration *param_1)

{
  long lVar1;
  int iVar2;
  int *piVar3;
  ulong uVar4;
  timespec local_38;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  uVar4 = *(ulong *)param_1;
  if (0 < (long)uVar4) {
    local_38.tv_sec = uVar4 / 1000000000;
    local_38.tv_nsec = uVar4 % 1000000000;
    do {
      iVar2 = nanosleep(&local_38,&local_38);
      if (iVar2 != -1) break;
      piVar3 = (int *)__errno();
    } while (*piVar3 == 4);
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
