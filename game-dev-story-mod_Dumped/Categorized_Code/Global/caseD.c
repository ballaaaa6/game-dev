// Function: caseD_5
// Address: 01357020
// ==========================================================================================

long * switchD_01356fa4::caseD_5(void)

{
  long *plVar1;
  long lVar2;
  long unaff_x19;
  undefined8 uVar3;
  long *unaff_x24;
  long *unaff_x25;
  
  uVar3 = *(undefined8 *)PTR_System_Collections_Generic_SByteEnumEqualityComparer_T__var_01fc67c8;
  if (*(int *)(*unaff_x25 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = System_Type__GetTypeFromHandle(uVar3,0);
  if (*(int *)(*unaff_x24 + 0xe0) == 0) {
    thunk_FUN_00df405c(*unaff_x24);
  }
  plVar1 = (long *)System_RuntimeType__CreateInstanceForAnotherGenericParameter(uVar3);
  lVar2 = *(long *)(unaff_x19 + 0x20);
  if ((*(byte *)(lVar2 + 0x135) & 1) == 0) {
    lVar2 = FUN_00e0dbd0(lVar2);
  }
  lVar2 = **(long **)(lVar2 + 0xc0);
  if ((*(byte *)(lVar2 + 0x135) & 1) == 0) {
    lVar2 = FUN_00e0dbd0(lVar2);
  }
  if (plVar1 != (long *)0x0) {
    if ((*(byte *)(*plVar1 + 0x130) < *(byte *)(lVar2 + 0x130)) ||
       (*(long *)(*(long *)(*plVar1 + 200) + (ulong)*(byte *)(lVar2 + 0x130) * 8 + -8) != lVar2)) {
                    /* WARNING: Subroutine does not return */
      FUN_00db1180(plVar1);
    }
  }
  return plVar1;
}



// ==========================================================================================
