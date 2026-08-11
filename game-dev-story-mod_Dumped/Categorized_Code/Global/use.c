// Function: use_facet
// Address: 00e78284
// ==========================================================================================

/* std::__ndk1::locale::use_facet(std::__ndk1::locale::id&) const */

void __thiscall std::__ndk1::locale::use_facet(locale *this,id *param_1)

{
  long lVar1;
  long lVar2;
  long lVar3;
  id *local_60;
  undefined *puStack_58;
  undefined8 local_50;
  undefined **local_48;
  id **local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  lVar3 = *(long *)this;
  puStack_58 = PTR___init_01ff5688;
  local_50 = 0;
  local_60 = param_1;
  if (*(long *)param_1 != -1) {
    local_48 = (undefined **)&local_40;
    local_40 = &local_60;
    __call_once((ulong *)param_1,&local_48,FUN_00e87ff8);
  }
  lVar2 = *(long *)(lVar3 + 0x10);
  if (((long)*(int *)(param_1 + 8) - 1U < (ulong)(*(long *)(lVar3 + 0x18) - lVar2 >> 3)) &&
     (*(long *)(lVar2 + ((long)*(int *)(param_1 + 8) - 1U) * 8) != 0)) {
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: use_facet
// Address: 01ec59c0
// ==========================================================================================

void __thiscall std::__ndk1::locale::use_facet(locale *this,id *param_1)

{
  (*(code *)PTR_use_facet_01ff5f00)();
  return;
}



// ==========================================================================================
