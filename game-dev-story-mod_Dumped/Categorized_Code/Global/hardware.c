// Function: hardware_concurrency
// Address: 00e93bbc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::thread::hardware_concurrency() */

undefined4 std::__ndk1::thread::hardware_concurrency(void)

{
  undefined4 uVar1;
  long lVar2;
  
                    /* try { // try from 00e93bc8 to 00e93bcf has its CatchHandler @ 00e93be4 */
  lVar2 = sysconf(0x61);
  uVar1 = (undefined4)lVar2;
  if (lVar2 < 1) {
    uVar1 = 0;
  }
  return uVar1;
}



// ==========================================================================================
