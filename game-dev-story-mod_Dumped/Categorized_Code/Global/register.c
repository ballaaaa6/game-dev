// Function: register_callback
// Address: 00e5b2a0
// ==========================================================================================

/* std::__ndk1::ios_base::register_callback(void (*)(std::__ndk1::ios_base::event,
   std::__ndk1::ios_base&, int), int) */

void __thiscall
std::__ndk1::ios_base::register_callback
          (ios_base *this,_func_void_event_ios_base_ptr_int *param_1,int param_2)

{
  ulong uVar1;
  uint uVar2;
  void *pvVar3;
  ulong uVar4;
  long lVar5;
  ulong uVar6;
  
  lVar5 = *(long *)(this + 0x48);
  uVar4 = lVar5 + 1;
  if (*(ulong *)(this + 0x50) < uVar4) {
    uVar6 = *(ulong *)(this + 0x50) << 1;
    uVar1 = uVar4;
    if (uVar4 <= uVar6) {
      uVar1 = uVar6;
    }
    if (0xffffffffffffffe < uVar4) {
      uVar1 = 0x1fffffffffffffff;
    }
    pvVar3 = realloc(*(void **)(this + 0x38),uVar1 << 3);
    if (pvVar3 == (void *)0x0) {
      uVar2 = *(uint *)(this + 0x20);
      *(uint *)(this + 0x20) = uVar2 | 1;
      if ((*(uint *)(this + 0x24) & (uVar2 | 1)) != 0) goto LAB_00e5b374;
    }
    *(void **)(this + 0x38) = pvVar3;
    pvVar3 = realloc(*(void **)(this + 0x40),uVar1 << 2);
    if (pvVar3 == (void *)0x0) {
      uVar2 = *(uint *)(this + 0x20);
      *(uint *)(this + 0x20) = uVar2 | 1;
      if ((*(uint *)(this + 0x24) & (uVar2 | 1)) != 0) {
LAB_00e5b374:
                    /* WARNING: Subroutine does not return */
        FUN_00e5b3f0("ios_base::clear");
      }
    }
    lVar5 = *(long *)(this + 0x48);
    *(void **)(this + 0x40) = pvVar3;
    *(ulong *)(this + 0x50) = uVar1;
    uVar4 = lVar5 + 1;
  }
  *(_func_void_event_ios_base_ptr_int **)(*(long *)(this + 0x38) + lVar5 * 8) = param_1;
  *(int *)(*(long *)(this + 0x40) + lVar5 * 4) = param_2;
  *(ulong *)(this + 0x48) = uVar4;
  return;
}



// ==========================================================================================
