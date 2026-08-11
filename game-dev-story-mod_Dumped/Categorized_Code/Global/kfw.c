// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType____ctor
// Address: 01788514
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType____ctor
               (long param_1,undefined4 param_2,undefined4 param_3,long param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  ulong uVar7;
  uint uVar8;
  long *plVar9;
  
  puVar1 = PTR_kfw_bsp_BspContents___TypeInfo_01fc78b8;
  if ((DAT_02100804 & 1) == 0) {
    FUN_00db0bbc(PTR_kfw_bsp_BspContents___TypeInfo_01fc78b8);
    FUN_00db0bbc(PTR_kfw_bsp_BspNode_____TypeInfo_01fc78c0);
    FUN_00db0bbc(PTR_kfw_bsp_BspNode___TypeInfo_01fc78c8);
    FUN_00db0bbc(PTR_kfw_bsp_BspNode_TypeInfo_01fc78d0);
    DAT_02100804 = 1;
  }
  puVar2 = PTR_kfw_bsp_BspNode_____TypeInfo_01fc78c0;
  uVar3 = FUN_00db0c30(*(undefined8 *)puVar1,10);
  *(undefined8 *)(param_1 + 0x30) = uVar3;
  lVar4 = *(long *)(*(long *)(*(long *)(param_4 + 0x20) + 0xc0) + 8);
  if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
    lVar4 = FUN_00e0dbd0();
  }
  uVar3 = FUN_00db0c30(lVar4,10);
  *(undefined8 *)(param_1 + 0x38) = uVar3;
  System_Object___ctor(param_1,0);
  *(undefined4 *)(param_1 + 0x18) = param_2;
  *(undefined4 *)(param_1 + 0x1c) = param_3;
  plVar5 = (long *)FUN_00db0c30(*(undefined8 *)puVar2,1);
  *(long **)(param_1 + 0x20) = plVar5;
  puVar2 = PTR_kfw_bsp_BspNode_TypeInfo_01fc78d0;
  puVar1 = PTR_kfw_bsp_BspNode___TypeInfo_01fc78c8;
  if (plVar5 == (long *)0x0) {
LAB_01788730:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (0 < *(int *)(plVar5 + 3)) {
    uVar8 = 0;
    do {
      lVar4 = FUN_00db0c30(*(undefined8 *)puVar1,1);
      if ((lVar4 != 0) &&
         (lVar6 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar5 + 0x40)), lVar6 == 0)) {
LAB_01788734:
        uVar3 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar3,0);
      }
      if (*(uint *)(plVar5 + 3) <= uVar8) {
LAB_0178872c:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      plVar5[(long)(int)uVar8 + 4] = lVar4;
      plVar5 = *(long **)(param_1 + 0x20);
      if (plVar5 == (long *)0x0) goto LAB_01788730;
      uVar7 = 0;
      while( true ) {
        if ((uint)plVar5[3] <= uVar8) goto LAB_0178872c;
        plVar9 = (long *)plVar5[(long)(int)uVar8 + 4];
        if (plVar9 == (long *)0x0) goto LAB_01788730;
        if ((long)*(int *)(plVar9 + 3) <= (long)uVar7) break;
        lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
        kfw_bsp_BspNode___ctor(lVar4,0);
        if ((lVar4 != 0) &&
           (lVar6 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar9 + 0x40)), lVar6 == 0))
        goto LAB_01788734;
        if (*(uint *)(plVar9 + 3) <= uVar7) goto LAB_0178872c;
        plVar9[uVar7 + 4] = lVar4;
        plVar5 = *(long **)(param_1 + 0x20);
        uVar7 = uVar7 + 1;
        if (plVar5 == (long *)0x0) goto LAB_01788730;
      }
      uVar8 = uVar8 + 1;
    } while ((int)uVar8 < (int)(uint)plVar5[3]);
  }
  if ((*(byte *)(*(long *)(*(long *)(*(long *)(param_4 + 0x20) + 0xc0) + 0x18) + 0x135) & 1) == 0) {
    FUN_00e0dbd0();
  }
  uVar3 = thunk_FUN_00e11c14();
  (***(code ***)(*(long *)(*(long *)(param_4 + 0x20) + 0xc0) + 0x20))();
  *(undefined8 *)(param_1 + 0x28) = uVar3;
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___Expand
// Address: 01788740
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___Expand
               (long param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  ulong uVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  uint uVar13;
  uint uVar14;
  undefined *puVar15;
  long *plVar16;
  long *plVar17;
  long lVar18;
  undefined8 uVar19;
  uint uVar20;
  long lVar21;
  int iVar22;
  int iVar23;
  uint uVar24;
  ulong uVar25;
  
  if ((DAT_02100805 & 1) == 0) {
    FUN_00db0bbc(PTR_kfw_bsp_BspNode_____TypeInfo_01fc78c0);
    FUN_00db0bbc(PTR_kfw_bsp_BspNode___TypeInfo_01fc78c8);
    FUN_00db0bbc(PTR_kfw_bsp_BspNode_TypeInfo_01fc78d0);
    DAT_02100805 = 1;
  }
  lVar21 = *(long *)(param_1 + 0x20);
  if (lVar21 != 0) {
    iVar11 = *(int *)(lVar21 + 0x18);
    if (iVar11 == 0) {
LAB_017889d4:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if (*(long *)(lVar21 + 0x20) != 0) {
      iVar9 = *(int *)(param_1 + 0x10);
      iVar10 = *(int *)(param_1 + 0x14);
      iVar12 = *(int *)(*(long *)(lVar21 + 0x20) + 0x18);
      iVar23 = (int)param_2;
      iVar22 = (int)((ulong)param_2 >> 0x20);
      iVar7 = iVar9;
      if (iVar9 + iVar23 < 0 != SBORROW4(iVar9,-iVar23)) {
        iVar7 = -iVar23;
      }
      iVar8 = iVar10;
      if (iVar10 + iVar22 < 0 != SBORROW4(iVar10,-iVar22)) {
        iVar8 = -iVar22;
      }
      iVar1 = (int)param_3 + iVar7;
      iVar2 = (iVar7 - iVar9) + iVar12;
      iVar3 = (int)((ulong)param_3 >> 0x20) + iVar8;
      iVar4 = (iVar8 - iVar10) + iVar11;
      if (iVar2 < iVar1 + 1) {
        iVar2 = iVar1 + 1;
      }
      if (iVar4 < iVar3 + 1) {
        iVar4 = iVar3 + 1;
      }
      if ((((iVar10 + iVar22 < 0 != SBORROW4(iVar10,-iVar22)) ||
           (iVar9 + iVar23 < 0 != SBORROW4(iVar9,-iVar23))) || (iVar12 < iVar2)) || (iVar11 < iVar4)
         ) {
        plVar16 = (long *)FUN_00db0c30(*(undefined8 *)PTR_kfw_bsp_BspNode_____TypeInfo_01fc78c0);
        puVar15 = PTR_kfw_bsp_BspNode_TypeInfo_01fc78d0;
        if (plVar16 == (long *)0x0) goto LAB_017889d8;
        if (0 < *(int *)(plVar16 + 3)) {
          uVar24 = 0;
          do {
            plVar17 = (long *)FUN_00db0c30(*(undefined8 *)PTR_kfw_bsp_BspNode___TypeInfo_01fc78c8,
                                           iVar2);
            if ((plVar17 != (long *)0x0) &&
               (lVar21 = thunk_FUN_00e11b18(plVar17,*(undefined8 *)(*plVar16 + 0x40)), lVar21 == 0))
            {
LAB_017889dc:
              uVar19 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
              FUN_00db0cb0(uVar19,0);
            }
            lVar21 = plVar16[3];
            if ((uint)lVar21 <= uVar24) goto LAB_017889d4;
            plVar16[(long)(int)uVar24 + 4] = (long)plVar17;
            if (plVar17 == (long *)0x0) goto LAB_017889d8;
            uVar25 = 0;
            while (uVar13 = *(uint *)(plVar17 + 3), (long)uVar25 < (long)(int)uVar13) {
              uVar5 = (*(int *)(param_1 + 0x14) - iVar8) + uVar24;
              if ((int)uVar5 < 0) {
LAB_01788940:
                lVar21 = thunk_FUN_00e11c14(*(undefined8 *)puVar15);
                kfw_bsp_BspNode___ctor(lVar21,0);
                if (lVar21 != 0) {
LAB_01788958:
                  lVar18 = thunk_FUN_00e11b18(lVar21,*(undefined8 *)(*plVar17 + 0x40));
                  if (lVar18 == 0) goto LAB_017889dc;
                }
                uVar13 = *(uint *)(plVar17 + 3);
              }
              else {
                lVar21 = *(long *)(param_1 + 0x20);
                if (lVar21 == 0) goto LAB_017889d8;
                uVar6 = (uint)-iVar7 + uVar25 + (ulong)*(uint *)(param_1 + 0x10);
                uVar20 = (uint)uVar6;
                if (((int)uVar20 < 0) ||
                   (uVar14 = *(uint *)(lVar21 + 0x18), (int)uVar14 <= (int)uVar5))
                goto LAB_01788940;
                if (uVar14 == 0) goto LAB_017889d4;
                if (*(long *)(lVar21 + 0x20) == 0) goto LAB_017889d8;
                if (*(int *)(*(long *)(lVar21 + 0x20) + 0x18) <= (int)uVar20) goto LAB_01788940;
                if (uVar14 <= uVar5) goto LAB_017889d4;
                lVar21 = *(long *)(lVar21 + (ulong)uVar5 * 8 + 0x20);
                if (lVar21 == 0) goto LAB_017889d8;
                if (*(uint *)(lVar21 + 0x18) <= uVar20) goto LAB_017889d4;
                lVar21 = *(long *)(lVar21 + (uVar6 & 0xffffffff) * 8 + 0x20);
                if (lVar21 != 0) goto LAB_01788958;
              }
              if (uVar13 <= uVar25) goto LAB_017889d4;
              plVar17[uVar25 + 4] = lVar21;
              lVar21 = plVar16[3];
              if ((uint)lVar21 <= uVar24) goto LAB_017889d4;
              plVar17 = (long *)plVar16[(long)(int)uVar24 + 4];
              uVar25 = uVar25 + 1;
              if (plVar17 == (long *)0x0) goto LAB_017889d8;
            }
            uVar24 = uVar24 + 1;
          } while ((int)uVar24 < (int)lVar21);
        }
        *(long **)(param_1 + 0x20) = plVar16;
        *(int *)(param_1 + 0x10) = iVar7;
        *(int *)(param_1 + 0x14) = iVar8;
      }
      return;
    }
  }
LAB_017889d8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___Add
// Address: 017889e8
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___Add
               (long param_1,undefined8 *****param_2,long param_3)

{
  undefined8 *****pppppuVar1;
  undefined *puVar2;
  ulong uVar3;
  undefined8 uVar4;
  code **ppcVar5;
  undefined8 *puVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  int *piVar10;
  undefined8 *__dest;
  uint uVar11;
  long lVar12;
  long lVar13;
  long *plVar14;
  ulong uVar15;
  ulong uVar16;
  undefined auVar17 [16];
  long local_a0 [2];
  undefined8 local_90;
  undefined8 local_88;
  undefined8 *****local_80;
  undefined8 *local_78;
  char local_6c [4];
  long local_68;
  
  lVar8 = tpidr_el0;
  local_68 = *(long *)(lVar8 + 0x28);
  local_80 = param_2;
  if ((DAT_02100806 & 1) == 0) {
    FUN_00db0bbc(PTR_kfw_bsp_BspContents_TypeInfo_01fc78d8);
    FUN_00db0bbc(PTR_kfw_bsp_BspKey_TypeInfo_01fc78e0);
    FUN_00db0bbc(PTR_kfw_bsp_IBspObject_TypeInfo_01fc78e8);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__Add_01fc78f0);
    DAT_02100806 = 1;
  }
  lVar9 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
  lVar7 = *(long *)(lVar9 + 0x28);
  lVar13 = lVar7;
  if ((*(byte *)(lVar7 + 0x135) & 1) == 0) {
    lVar7 = FUN_00e0dbd0(lVar7);
    lVar9 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    lVar13 = *(long *)(lVar9 + 0x28);
  }
  lVar12 = (long)local_a0 - ((ulong)(*(int *)(lVar7 + 0xfc) + 0x10) + 0xf & 0x1fffffff0);
  uVar15 = (ulong)*(uint *)(lVar13 + 0xfc);
  __dest = (undefined8 *)(lVar12 - (uVar15 + 0xf & 0x1fffffff0));
  local_90 = 0;
  local_88 = 0;
  lVar7 = *(long *)(lVar9 + 0x28);
  lVar13 = lVar7;
  if ((*(byte *)(lVar7 + 0x135) & 1) == 0) {
    lVar7 = FUN_00e0dbd0(lVar7);
    lVar9 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    lVar13 = *(long *)(lVar9 + 0x28);
  }
  local_78 = &local_90;
  if (-1 < *(int *)(lVar13 + 0x28)) {
    param_2 = &local_80;
  }
  FUN_00db16c0(lVar7,*(undefined8 *)(lVar9 + 0x30),lVar12,param_2,&local_78,local_6c);
  puVar2 = PTR_kfw_bsp_BspContents_TypeInfo_01fc78d8;
  if (local_6c[0] == '\0') {
LAB_01788db8:
    if (*(long *)(lVar8 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return;
  }
  auVar17 = (***(code ***)(*(long *)(*(long *)(param_3 + 0x20) + 0xc0) + 0x38))
                      ((undefined4)local_90,local_90._4_4_,(undefined4)local_88,local_88._4_4_,
                       param_1);
  uVar3 = auVar17._0_8_;
  (***(code ***)(*(long *)(*(long *)(param_3 + 0x20) + 0xc0) + 0x40))(param_1,uVar3,auVar17._8_8_);
  lVar13 = *(long *)(param_3 + 0x20);
  pppppuVar1 = local_80;
  if (-1 < *(int *)(*(long *)(*(long *)(lVar13 + 0xc0) + 0x28) + 0x28)) {
    pppppuVar1 = &local_80;
  }
  memcpy(__dest,pppppuVar1,uVar15);
  uVar4 = thunk_FUN_00e11868(*(undefined8 *)(*(long *)(lVar13 + 0xc0) + 0x28),__dest);
  lVar13 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  kfw_bsp_BspContents___ctor(lVar13,uVar4,0);
  puVar2 = PTR_kfw_bsp_BspKey_TypeInfo_01fc78e0;
  if (lVar13 != 0) {
    *(undefined (*) [16])(lVar13 + 0x18) = auVar17;
    plVar14 = *(long **)(lVar13 + 0x10);
    local_a0[0] = lVar8;
    local_a0[1] = uVar15;
    uVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    kfw_bsp_BspKey___ctor(uVar4,lVar13,0);
    if (plVar14 != (long *)0x0) {
      lVar8 = *plVar14;
      uVar16 = uVar3 >> 0x20;
      uVar15 = (ulong)*(ushort *)(lVar8 + 0x12e);
      if (uVar15 != 0) {
        piVar10 = (int *)(*(long *)(lVar8 + 0xb0) + 8);
        do {
          if (*(long *)(piVar10 + -2) == *(long *)PTR_kfw_bsp_IBspObject_TypeInfo_01fc78e8) {
            ppcVar5 = (code **)(lVar8 + (long)(*piVar10 + 2) * 0x10 + 0x138);
            goto LAB_01788c64;
          }
          uVar15 = uVar15 - 1;
          piVar10 = piVar10 + 4;
        } while (uVar15 != 0);
      }
      ppcVar5 = (code **)FUN_00e0dcd4(plVar14,*(long *)PTR_kfw_bsp_IBspObject_TypeInfo_01fc78e8,2);
LAB_01788c64:
      (**ppcVar5)(plVar14,uVar4,ppcVar5[1]);
      puVar2 = PTR_Method_System_Collections_Generic_List_BspContents__Add_01fc78f0;
      uVar11 = auVar17._4_4_;
      while ((int)uVar11 <= auVar17._12_4_) {
        uVar11 = auVar17._0_4_;
        uVar15 = uVar3 & 0xffffffff;
        while ((int)uVar11 <= auVar17._8_4_) {
          lVar8 = *(long *)(param_1 + 0x20);
          if (lVar8 == 0) goto LAB_01788de8;
          uVar11 = *(int *)(param_1 + 0x14) + (int)uVar16;
          if (*(uint *)(lVar8 + 0x18) <= uVar11) {
LAB_01788dec:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar8 = *(long *)(lVar8 + (long)(int)uVar11 * 8 + 0x20);
          if (lVar8 == 0) goto LAB_01788de8;
          uVar11 = (int)uVar15 + *(int *)(param_1 + 0x10);
          if (*(uint *)(lVar8 + 0x18) <= uVar11) goto LAB_01788dec;
          lVar8 = *(long *)(lVar8 + (long)(int)uVar11 * 8 + 0x20);
          if ((lVar8 == 0) || (lVar8 = *(long *)(lVar8 + 0x10), lVar8 == 0)) goto LAB_01788de8;
          lVar7 = *(long *)(lVar8 + 0x10);
          lVar9 = *(long *)puVar2;
          *(int *)(lVar8 + 0x1c) = *(int *)(lVar8 + 0x1c) + 1;
          if (lVar7 == 0) goto LAB_01788de8;
          uVar11 = *(uint *)(lVar8 + 0x18);
          if (uVar11 < *(uint *)(lVar7 + 0x18)) {
            *(uint *)(lVar8 + 0x18) = uVar11 + 1;
            *(long *)(lVar7 + (long)(int)uVar11 * 8 + 0x20) = lVar13;
          }
          else {
            System_Collections_Generic_List_object___AddWithResize
                      (lVar8,lVar13,
                       *(undefined8 *)(*(long *)(*(long *)(lVar9 + 0x20) + 0xc0) + 0x70));
          }
          uVar11 = (int)uVar15 + 1;
          uVar15 = (ulong)uVar11;
        }
        uVar11 = (int)uVar16 + 1;
        uVar16 = (ulong)uVar11;
      }
      lVar7 = *(long *)(param_3 + 0x20);
      lVar13 = *(long *)(param_1 + 0x28);
      pppppuVar1 = local_80;
      if (-1 < *(int *)(*(long *)(*(long *)(lVar7 + 0xc0) + 0x28) + 0x28)) {
        pppppuVar1 = &local_80;
      }
      memcpy(__dest,pppppuVar1,local_a0[1]);
      lVar8 = local_a0[0];
      if (lVar13 != 0) {
        lVar7 = *(long *)(lVar7 + 0xc0);
        puVar6 = *(undefined8 **)(lVar7 + 0x48);
        if (-1 < *(int *)(*(long *)(lVar7 + 0x28) + 0x28)) {
          __dest = (undefined8 *)*__dest;
        }
        local_78 = __dest;
        (*(code *)puVar6[2])(*puVar6,puVar6,lVar13,&local_78,__dest);
        goto LAB_01788db8;
      }
    }
  }
LAB_01788de8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___Remove
// Address: 01788df4
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___Remove
               (long param_1,undefined8 ****param_2,long param_3)

{
  undefined8 ****ppppuVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  ushort uVar6;
  int iVar7;
  undefined *puVar8;
  long lVar9;
  undefined8 *puVar10;
  long lVar11;
  long lVar12;
  void **__dest;
  void *pvVar13;
  int iVar14;
  long lVar15;
  long lVar16;
  void *local_90;
  ulong local_88;
  undefined8 ****local_80;
  undefined auStack_74 [4];
  void *local_70;
  long local_68;
  
  pvVar13 = (void *)tpidr_el0;
  local_68 = *(long *)((long)pvVar13 + 0x28);
  local_80 = param_2;
  if ((DAT_02100807 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__Remove_01fc78f8);
    DAT_02100807 = 1;
  }
  lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
  lVar11 = *(long *)(lVar12 + 0x28);
  uVar6 = *(ushort *)(lVar11 + 0x135);
  lVar9 = lVar11;
  if ((uVar6 & 1) == 0) {
    lVar11 = FUN_00e0dbd0(lVar11);
    lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    uVar6 = *(ushort *)(*(long *)(lVar12 + 0x28) + 0x135);
    lVar9 = *(long *)(lVar12 + 0x28);
  }
  lVar16 = (long)&local_90 - ((ulong)(*(int *)(lVar11 + 0xfc) + 0x10) + 0xf & 0x1fffffff0);
  lVar11 = lVar9;
  if ((uVar6 & 1) == 0) {
    lVar9 = FUN_00e0dbd0(lVar9);
    lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    uVar6 = *(ushort *)(*(long *)(lVar12 + 0x28) + 0x135);
    lVar11 = *(long *)(lVar12 + 0x28);
  }
  lVar15 = lVar16 - ((ulong)(*(int *)(lVar9 + 0xfc) + 0x10) + 0xf & 0x1fffffff0);
  uVar2 = *(uint *)(lVar11 + 0xfc);
  __dest = (void **)(lVar15 - ((ulong)uVar2 + 0xf & 0x1fffffff0));
  lVar9 = lVar11;
  if ((uVar6 & 1) == 0) {
    lVar11 = FUN_00e0dbd0(lVar11);
    lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    lVar9 = *(long *)(lVar12 + 0x28);
  }
  if (-1 < *(int *)(lVar9 + 0x28)) {
    param_2 = &local_80;
  }
  FUN_00db16c0(lVar11,*(undefined8 *)(lVar12 + 0x50),lVar16,param_2,0,&local_70);
  if (local_70 == (void *)0x0) {
LAB_017890c8:
    if (*(long *)((long)pvVar13 + 0x28) == local_68) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
  lVar11 = *(long *)(lVar12 + 0x28);
  lVar9 = lVar11;
  if ((*(byte *)(lVar11 + 0x135) & 1) == 0) {
    lVar11 = FUN_00e0dbd0(lVar11);
    lVar12 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    lVar9 = *(long *)(lVar12 + 0x28);
  }
  ppppuVar1 = local_80;
  if (-1 < *(int *)(lVar9 + 0x28)) {
    ppppuVar1 = &local_80;
  }
  local_88 = (ulong)uVar2;
  FUN_00db16c0(lVar11,*(undefined8 *)(lVar12 + 0x50),lVar15,ppppuVar1,0,&local_70);
  puVar8 = PTR_Method_System_Collections_Generic_List_BspContents__Remove_01fc78f8;
  if ((local_70 != (void *)0x0) &&
     (lVar9 = *(long *)((long)local_70 + 0x10), local_90 = pvVar13, lVar9 != 0)) {
    iVar14 = *(int *)(lVar9 + 0x1c);
    iVar3 = *(int *)(lVar9 + 0x24);
    if (iVar14 <= iVar3) {
      iVar4 = *(int *)(lVar9 + 0x18);
      iVar5 = *(int *)(lVar9 + 0x20);
      iVar7 = iVar4;
joined_r0x01788fe8:
      do {
        if (iVar7 <= iVar5) {
          lVar11 = *(long *)(param_1 + 0x20);
          if (lVar11 == 0) goto LAB_017890f8;
          uVar2 = *(int *)(param_1 + 0x14) + iVar14;
          if (uVar2 < *(uint *)(lVar11 + 0x18)) {
            lVar11 = *(long *)(lVar11 + (long)(int)uVar2 * 8 + 0x20);
            if (lVar11 == 0) goto LAB_017890f8;
            uVar2 = iVar7 + *(int *)(param_1 + 0x10);
            if (uVar2 < *(uint *)(lVar11 + 0x18)) {
              lVar11 = *(long *)(lVar11 + (long)(int)uVar2 * 8 + 0x20);
              if ((lVar11 == 0) || (lVar11 = *(long *)(lVar11 + 0x10), lVar11 == 0))
              goto LAB_017890f8;
              System_Collections_Generic_List_object___Remove(lVar11,lVar9,*(undefined8 *)puVar8);
              iVar7 = iVar7 + 1;
              goto joined_r0x01788fe8;
            }
          }
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        iVar14 = iVar14 + 1;
        iVar7 = iVar4;
      } while (iVar14 <= iVar3);
    }
    lVar11 = *(long *)(param_3 + 0x20);
    lVar9 = *(long *)(param_1 + 0x28);
    ppppuVar1 = local_80;
    if (-1 < *(int *)(*(long *)(*(long *)(lVar11 + 0xc0) + 0x28) + 0x28)) {
      ppppuVar1 = &local_80;
    }
    memcpy(__dest,ppppuVar1,local_88);
    pvVar13 = local_90;
    if (lVar9 != 0) {
      lVar11 = *(long *)(lVar11 + 0xc0);
      puVar10 = *(undefined8 **)(lVar11 + 0x58);
      if (-1 < *(int *)(*(long *)(lVar11 + 0x28) + 0x28)) {
        __dest = (void **)*__dest;
      }
      local_70 = __dest;
      (*(code *)puVar10[2])(*puVar10,puVar10,lVar9,&local_70,auStack_74);
      goto LAB_017890c8;
    }
  }
LAB_017890f8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___Update
// Address: 01789104
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___Update
               (long param_1,undefined8 ****param_2,long param_3)

{
  undefined8 ****ppppuVar1;
  ushort uVar2;
  long lVar3;
  undefined *puVar4;
  undefined auVar5 [16];
  long lVar6;
  undefined8 *puVar7;
  int iVar8;
  long lVar9;
  int iVar10;
  long lVar11;
  uint uVar12;
  int iVar13;
  long lVar14;
  undefined (*pauVar15) [16];
  ulong uVar16;
  int iVar17;
  undefined8 *__dest;
  undefined local_a0 [8];
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 ****local_80;
  undefined8 *local_78;
  char local_6c [4];
  long local_68;
  
  lVar3 = tpidr_el0;
  local_68 = *(long *)(lVar3 + 0x28);
  local_80 = param_2;
  if ((DAT_02100808 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__Add_01fc78f0);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__Remove_01fc78f8);
    DAT_02100808 = 1;
  }
  lVar11 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
  lVar9 = *(long *)(lVar11 + 0x28);
  uVar2 = *(ushort *)(lVar9 + 0x135);
  lVar6 = lVar9;
  if ((uVar2 & 1) == 0) {
    lVar9 = FUN_00e0dbd0(lVar9);
    lVar11 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    uVar2 = *(ushort *)(*(long *)(lVar11 + 0x28) + 0x135);
    lVar6 = *(long *)(lVar11 + 0x28);
  }
  iVar13 = *(int *)(lVar9 + 0xfc);
  uVar12 = *(uint *)(lVar6 + 0xfc);
  uVar16 = (ulong)uVar12;
  if ((uVar2 & 1) == 0) {
    lVar6 = FUN_00e0dbd0(lVar6);
    uVar12 = *(uint *)(lVar6 + 0xfc);
    lVar11 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
  }
  lVar14 = (long)(local_a0 + -((ulong)(iVar13 + 0x10) + 0xf & 0x1fffffff0)) -
           ((ulong)(uVar12 + 0x10) + 0xf & 0x1fffffff0);
  __dest = (undefined8 *)(lVar14 - (uVar16 + 0xf & 0x1fffffff0));
  local_90 = 0;
  local_88 = 0;
  local_a0 = (undefined  [8])0x0;
  uStack_98 = 0;
  lVar9 = *(long *)(lVar11 + 0x28);
  lVar6 = lVar9;
  if ((*(byte *)(lVar9 + 0x135) & 1) == 0) {
    lVar9 = FUN_00e0dbd0(lVar9);
    lVar11 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
    lVar6 = *(long *)(lVar11 + 0x28);
  }
  if (-1 < *(int *)(lVar6 + 0x28)) {
    param_2 = &local_80;
  }
  FUN_00db16c0(lVar9,*(undefined8 *)(lVar11 + 0x50),
               local_a0 + -((ulong)(iVar13 + 0x10) + 0xf & 0x1fffffff0),param_2,0,&local_78);
  puVar7 = local_78;
  lVar11 = *(long *)(param_3 + 0x20);
  lVar9 = *(long *)(lVar11 + 0xc0);
  lVar6 = *(long *)(lVar9 + 0x28);
  if (local_78 == (undefined8 *)0x0) {
    ppppuVar1 = local_80;
    if (-1 < *(int *)(lVar6 + 0x28)) {
      ppppuVar1 = &local_80;
    }
    memcpy(__dest,ppppuVar1,uVar16);
    lVar6 = *(long *)(lVar11 + 0xc0);
    puVar7 = *(undefined8 **)(lVar6 + 0x60);
    if (-1 < *(int *)(*(long *)(lVar6 + 0x28) + 0x28)) {
      __dest = (undefined8 *)*__dest;
    }
    local_78 = __dest;
    (*(code *)puVar7[2])(*puVar7,puVar7,param_1,&local_78,__dest);
  }
  else {
    lVar11 = lVar6;
    if ((*(byte *)(lVar6 + 0x135) & 1) == 0) {
      lVar6 = FUN_00e0dbd0(lVar6);
      lVar9 = *(long *)(*(long *)(param_3 + 0x20) + 0xc0);
      lVar11 = *(long *)(lVar9 + 0x28);
    }
    local_78 = &local_90;
    ppppuVar1 = local_80;
    if (-1 < *(int *)(lVar11 + 0x28)) {
      ppppuVar1 = &local_80;
    }
    FUN_00db16c0(lVar6,*(undefined8 *)(lVar9 + 0x30),lVar14,ppppuVar1,&local_78,local_6c);
    if (local_6c[0] != '\0') {
      lVar6 = puVar7[2];
      _local_a0 = (***(code ***)(*(long *)(*(long *)(param_3 + 0x20) + 0xc0) + 0x38))
                            (local_90 & 0xffffffff,local_90._4_4_,(undefined4)local_88,
                             local_88._4_4_,param_1);
      if (lVar6 == 0) {
LAB_017895b4:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      pauVar15 = (undefined (*) [16])(lVar6 + 0x18);
      uVar16 = kfw_bsp_BspRange__Equals
                         (local_a0,*(undefined8 *)*pauVar15,*(undefined8 *)(lVar6 + 0x20),0);
      if ((uVar16 & 1) == 0) {
        (***(code ***)(*(long *)(*(long *)(param_3 + 0x20) + 0xc0) + 0x40))
                  (param_1,local_a0,uStack_98);
        puVar4 = PTR_Method_System_Collections_Generic_List_BspContents__Remove_01fc78f8;
        iVar13 = *(int *)(lVar6 + 0x1c);
        iVar10 = *(int *)(lVar6 + 0x24);
        if (iVar13 <= iVar10) {
          iVar8 = *(int *)(lVar6 + 0x20);
          do {
            iVar17 = *(int *)*pauVar15;
            if (iVar17 <= iVar8) {
              do {
                if ((((iVar17 < (int)local_a0._0_4_) || ((int)uStack_98 < iVar17)) ||
                    (iVar13 < (int)local_a0._4_4_)) || (uStack_98._4_4_ < iVar13)) {
                  lVar9 = *(long *)(param_1 + 0x20);
                  if (lVar9 == 0) goto LAB_017895b4;
                  uVar12 = *(int *)(param_1 + 0x14) + iVar13;
                  if (*(uint *)(lVar9 + 0x18) <= uVar12) goto LAB_017895b8;
                  lVar9 = *(long *)(lVar9 + (long)(int)uVar12 * 8 + 0x20);
                  if (lVar9 == 0) goto LAB_017895b4;
                  uVar12 = iVar17 + *(int *)(param_1 + 0x10);
                  if (*(uint *)(lVar9 + 0x18) <= uVar12) goto LAB_017895b8;
                  lVar9 = *(long *)(lVar9 + (long)(int)uVar12 * 8 + 0x20);
                  if ((lVar9 == 0) || (lVar9 = *(long *)(lVar9 + 0x10), lVar9 == 0))
                  goto LAB_017895b4;
                  System_Collections_Generic_List_object___Remove(lVar9,lVar6,*(undefined8 *)puVar4)
                  ;
                  iVar8 = *(int *)(lVar6 + 0x20);
                }
                iVar17 = iVar17 + 1;
              } while (iVar17 <= iVar8);
              iVar10 = *(int *)(lVar6 + 0x24);
            }
            iVar13 = iVar13 + 1;
          } while (iVar13 <= iVar10);
        }
        puVar4 = PTR_Method_System_Collections_Generic_List_BspContents__Add_01fc78f0;
        auVar5 = _local_a0;
        if ((int)local_a0._4_4_ <= uStack_98._4_4_) {
          iVar13 = local_a0._4_4_;
          do {
            local_a0._0_4_ = auVar5._0_4_;
            iVar10 = local_a0._0_4_;
            if ((int)local_a0._0_4_ <= (int)uStack_98) {
              do {
                _local_a0 = auVar5;
                auVar5 = _local_a0;
                if (((iVar10 < *(int *)*pauVar15) || (*(int *)(lVar6 + 0x20) < iVar10)) ||
                   ((iVar13 < *(int *)(lVar6 + 0x1c) || (*(int *)(lVar6 + 0x24) < iVar13)))) {
                  lVar9 = *(long *)(param_1 + 0x20);
                  if (lVar9 == 0) goto LAB_017895b4;
                  uVar12 = *(int *)(param_1 + 0x14) + iVar13;
                  if (*(uint *)(lVar9 + 0x18) <= uVar12) {
LAB_017895b8:
                    /* WARNING: Subroutine does not return */
                    FUN_00db0dec();
                  }
                  lVar9 = *(long *)(lVar9 + (long)(int)uVar12 * 8 + 0x20);
                  if (lVar9 == 0) goto LAB_017895b4;
                  uVar12 = iVar10 + *(int *)(param_1 + 0x10);
                  if (*(uint *)(lVar9 + 0x18) <= uVar12) goto LAB_017895b8;
                  lVar9 = *(long *)(lVar9 + (long)(int)uVar12 * 8 + 0x20);
                  if ((lVar9 == 0) || (lVar9 = *(long *)(lVar9 + 0x10), lVar9 == 0))
                  goto LAB_017895b4;
                  lVar11 = *(long *)(lVar9 + 0x10);
                  lVar14 = *(long *)puVar4;
                  *(int *)(lVar9 + 0x1c) = *(int *)(lVar9 + 0x1c) + 1;
                  if (lVar11 == 0) goto LAB_017895b4;
                  uVar12 = *(uint *)(lVar9 + 0x18);
                  if (uVar12 < *(uint *)(lVar11 + 0x18)) {
                    *(uint *)(lVar9 + 0x18) = uVar12 + 1;
                    *(long *)(lVar11 + (long)(int)uVar12 * 8 + 0x20) = lVar6;
                  }
                  else {
                    System_Collections_Generic_List_object___AddWithResize
                              (lVar9,lVar6,
                               *(undefined8 *)(*(long *)(*(long *)(lVar14 + 0x20) + 0xc0) + 0x70));
                    auVar5 = _local_a0;
                  }
                }
                uStack_98._0_4_ = auVar5._8_4_;
                iVar10 = iVar10 + 1;
              } while (iVar10 <= (int)uStack_98);
              uStack_98._4_4_ = auVar5._12_4_;
            }
            iVar13 = iVar13 + 1;
          } while (iVar13 <= uStack_98._4_4_);
        }
        _local_a0 = auVar5;
        *pauVar15 = _local_a0;
      }
    }
  }
  if (*(long *)(lVar3 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetRange
// Address: 017895c0
// ==========================================================================================

long kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetRange(long param_1,long param_2)

{
  uint uVar1;
  long lVar2;
  undefined8 uVar3;
  long lVar4;
  long *plVar5;
  ulong uVar6;
  undefined8 local_38;
  
  local_38 = 0;
  uVar1 = (***(code ***)(*(long *)(*(long *)(param_2 + 0x20) + 0xc0) + 0x68))(param_1,&local_38);
  plVar5 = *(long **)(param_1 + 0x40);
  if (plVar5 != (long *)0x0) {
LAB_01789600:
    if ((int)uVar1 < (int)*(uint *)(plVar5 + 3)) {
      if (*(uint *)(plVar5 + 3) <= uVar1) {
LAB_01789708:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      lVar4 = plVar5[(long)(int)uVar1 + 4];
    }
    else {
      lVar4 = *(long *)(*(long *)(*(long *)(param_2 + 0x20) + 0xc0) + 8);
      if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
        lVar4 = FUN_00e0dbd0();
      }
      lVar4 = FUN_00db0c30(lVar4,uVar1);
    }
    Method_System_Array_Copy(local_38,lVar4,uVar1,0);
    return lVar4;
  }
  lVar4 = *(long *)(*(long *)(*(long *)(param_2 + 0x20) + 0xc0) + 0x80);
  if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
    lVar4 = FUN_00e0dbd0();
  }
  plVar5 = (long *)FUN_00db0c30(lVar4,10);
  *(long **)(param_1 + 0x40) = plVar5;
  if (plVar5 != (long *)0x0) {
    uVar6 = 0;
    do {
      if ((long)*(int *)(plVar5 + 3) <= (long)uVar6) goto LAB_01789600;
      lVar4 = *(long *)(*(long *)(*(long *)(param_2 + 0x20) + 0xc0) + 8);
      if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
        lVar4 = FUN_00e0dbd0();
      }
      lVar4 = FUN_00db0c30(lVar4,uVar6 & 0xffffffff);
      if ((lVar4 != 0) &&
         (lVar2 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar5 + 0x40)), lVar2 == 0)) {
        uVar3 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar3,0);
      }
      if (*(uint *)(plVar5 + 3) <= uVar6) goto LAB_01789708;
      plVar5[uVar6 + 4] = lVar4;
      plVar5 = *(long **)(param_1 + 0x40);
      uVar6 = uVar6 + 1;
    } while (plVar5 != (long *)0x0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetRange
// Address: 01789718
// ==========================================================================================

uint kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetRange
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
               long param_5,long *param_6,long param_7)

{
  uint uVar1;
  undefined *puVar2;
  size_t __n;
  long lVar3;
  long lVar4;
  void *__src;
  uint uVar5;
  long lVar6;
  undefined8 uVar7;
  ulong uVar8;
  ulong uVar9;
  long *plVar10;
  uint uVar11;
  int iVar12;
  undefined auVar13 [16];
  long local_c0;
  long *local_b8;
  ulong local_b0;
  long lStack_a8;
  ulong local_a0;
  ulong local_98;
  long local_90;
  long local_88;
  
  local_c0 = tpidr_el0;
  local_88 = *(long *)(local_c0 + 0x28);
  local_b8 = param_6;
  if ((DAT_02100809 & 1) == 0) {
    FUN_00db0bbc(PTR_kfw_bsp_BspContents___TypeInfo_01fc78b8);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__get_Count_01fc7900);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents__get_Item_01fc7908);
    DAT_02100809 = 1;
  }
  lVar6 = *(long *)(*(long *)(param_7 + 0x20) + 0xc0);
  local_b0 = (ulong)*(uint *)(*(long *)(lVar6 + 0x28) + 0xfc);
  local_90 = (long)&local_c0 - (local_b0 + 0xf & 0x1fffffff0);
  lStack_a8 = param_7;
  auVar13 = (***(code ***)(lVar6 + 0x38))(param_1,param_2,param_3,param_4,param_5);
  puVar2 = PTR_Method_System_Collections_Generic_List_BspContents__get_Item_01fc7908;
  local_98 = auVar13._0_8_;
  uVar9 = local_98 >> 0x20;
  local_a0 = auVar13._8_8_ >> 0x20;
  if (auVar13._12_4_ < auVar13._4_4_) {
    uVar11 = 0;
  }
  else {
    uVar11 = 0;
    do {
      uVar5 = (uint)local_98;
      uVar8 = local_98 & 0xffffffff;
      while ((int)uVar5 <= auVar13._8_4_) {
        uVar5 = *(int *)(param_5 + 0x14) + (int)uVar9;
        if (-1 < (int)uVar5) {
          lVar6 = *(long *)(param_5 + 0x20);
          if (lVar6 == 0) goto LAB_01789ae4;
          uVar1 = *(int *)(param_5 + 0x10) + (int)uVar8;
          if ((-1 < (int)uVar1) && ((int)uVar5 < (int)*(uint *)(lVar6 + 0x18))) {
            if (*(uint *)(lVar6 + 0x18) <= uVar5) goto LAB_01789ae8;
            lVar6 = *(long *)(lVar6 + (ulong)uVar5 * 8 + 0x20);
            if (lVar6 == 0) goto LAB_01789ae4;
            if ((int)uVar1 < (int)*(uint *)(lVar6 + 0x18)) {
              if (*(uint *)(lVar6 + 0x18) <= uVar1) goto LAB_01789ae8;
              lVar6 = *(long *)(lVar6 + (ulong)uVar1 * 8 + 0x20);
              if ((lVar6 == 0) || (lVar4 = *(long *)(lVar6 + 0x10), lVar4 == 0)) goto LAB_01789ae4;
              iVar12 = 0;
              while (iVar12 < *(int *)(lVar4 + 0x18)) {
                lVar4 = Method_System_Collections_Generic_List_object__get_Item
                                  (lVar4,iVar12,*(undefined8 *)puVar2);
                if (lVar4 == 0) goto LAB_01789ae4;
                if (*(char *)(lVar4 + 0x28) == '\0') {
                  if ((*(long *)(lVar6 + 0x10) == 0) ||
                     (lVar4 = Method_System_Collections_Generic_List_object__get_Item
                                        (*(long *)(lVar6 + 0x10),iVar12,*(undefined8 *)puVar2),
                     lVar4 == 0)) goto LAB_01789ae4;
                  *(undefined *)(lVar4 + 0x28) = 1;
                  plVar10 = *(long **)(param_5 + 0x30);
                  if (plVar10 == (long *)0x0) goto LAB_01789ae4;
                  if (*(int *)(plVar10 + 3) <= (int)uVar11) {
                    plVar10 = (long *)FUN_00db0c30(*(undefined8 *)
                                                    PTR_kfw_bsp_BspContents___TypeInfo_01fc78b8,
                                                   *(int *)(plVar10 + 3) << 1);
                    lVar4 = *(long *)(param_5 + 0x30);
                    if (lVar4 == 0) goto LAB_01789ae4;
                    Method_System_Array_Copy(lVar4,plVar10,*(undefined4 *)(lVar4 + 0x18),0);
                    *(long **)(param_5 + 0x30) = plVar10;
                  }
                  if ((*(long *)(lVar6 + 0x10) == 0) ||
                     (lVar4 = Method_System_Collections_Generic_List_object__get_Item
                                        (*(long *)(lVar6 + 0x10),iVar12,*(undefined8 *)puVar2),
                     plVar10 == (long *)0x0)) goto LAB_01789ae4;
                  if ((lVar4 != 0) &&
                     (lVar3 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar10 + 0x40)), lVar3 == 0
                     )) {
                    uVar7 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
                    FUN_00db0cb0(uVar7,0);
                  }
                  if (*(uint *)(plVar10 + 3) <= uVar11) goto LAB_01789ae8;
                  lVar3 = (long)(int)uVar11;
                  uVar11 = uVar11 + 1;
                  plVar10[lVar3 + 4] = lVar4;
                }
                lVar4 = *(long *)(lVar6 + 0x10);
                iVar12 = iVar12 + 1;
                if (lVar4 == 0) goto LAB_01789ae4;
              }
            }
          }
        }
        uVar5 = (int)uVar8 + 1;
        uVar8 = (ulong)uVar5;
      }
      uVar5 = (int)uVar9 + 1;
      uVar9 = (ulong)uVar5;
    } while ((int)uVar5 <= (int)local_a0);
  }
  lVar6 = lStack_a8;
  __n = local_b0;
  lVar4 = *(long *)(param_5 + 0x38);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) < (int)uVar11) {
      lVar4 = *(long *)(*(long *)(*(long *)(lStack_a8 + 0x20) + 0xc0) + 8);
      if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
        lVar4 = FUN_00e0dbd0();
      }
      lVar4 = FUN_00db0c30(lVar4,uVar11);
      *(long *)(param_5 + 0x38) = lVar4;
    }
    if (0 < (int)uVar11) {
      uVar5 = 0;
      do {
        lVar4 = *(long *)(param_5 + 0x30);
        if (lVar4 == 0) goto LAB_01789ae4;
        if (*(uint *)(lVar4 + 0x18) <= uVar5) {
LAB_01789ae8:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar4 = *(long *)(lVar4 + (long)(int)uVar5 * 8 + 0x20);
        if (lVar4 == 0) goto LAB_01789ae4;
        *(undefined *)(lVar4 + 0x28) = 0;
        plVar10 = *(long **)(param_5 + 0x38);
        uVar7 = *(undefined8 *)(lVar4 + 0x10);
        lVar4 = *(long *)(*(long *)(*(long *)(lVar6 + 0x20) + 0xc0) + 0x28);
        if ((*(byte *)(lVar4 + 0x135) & 1) == 0) {
          lVar4 = FUN_00e0dbd0(lVar4);
        }
        __src = (void *)FUN_00db0cd4(uVar7,lVar4,local_90);
        if (plVar10 == (long *)0x0) goto LAB_01789ae4;
        if (*(uint *)(plVar10 + 3) <= uVar5) goto LAB_01789ae8;
        memcpy((void *)((long)plVar10 + (ulong)*(uint *)(*plVar10 + 0x104) * (long)(int)uVar5 + 0x20
                       ),__src,__n);
        if ((*(byte *)(*(long *)(*(long *)(*(long *)(lVar6 + 0x20) + 0xc0) + 0x28) + 0x135) & 1) ==
            0) {
          FUN_00e0dbd0();
        }
        if (*(uint *)(plVar10 + 3) <= uVar5) goto LAB_01789ae8;
        uVar5 = uVar5 + 1;
      } while (uVar11 != uVar5);
      lVar4 = *(long *)(param_5 + 0x38);
    }
    *local_b8 = lVar4;
    if (*(long *)(local_c0 + 0x28) == local_88) {
      return uVar11;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
LAB_01789ae4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetBspPoints
// Address: 01789afc
// ==========================================================================================

undefined  [16]
kfw_bsp_BspMap___Il2CppFullySharedGenericType___GetBspPoints
          (float param_1,float param_2,float param_3,float param_4,long param_5)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  undefined auVar10 [16];
  float fVar11;
  float fVar12;
  undefined8 local_20;
  undefined8 uStack_18;
  
  iVar4 = *(int *)(param_5 + 0x18);
  fVar12 = param_1 + param_3 + -1.0;
  iVar5 = -0x80000000;
  if (param_1 != INFINITY) {
    iVar5 = (int)param_1;
  }
  fVar11 = param_2 + param_4 + -1.0;
  iVar1 = -0x80000000;
  if (param_2 != INFINITY) {
    iVar1 = (int)param_2;
  }
  iVar2 = -0x80000000;
  if (fVar12 != INFINITY) {
    iVar2 = (int)fVar12;
  }
  iVar3 = -0x80000000;
  if (fVar11 != INFINITY) {
    iVar3 = (int)fVar11;
  }
  if (iVar5 < 0) {
    uVar6 = 0;
    if (iVar4 != 0) {
      uVar6 = -iVar5 / iVar4;
    }
    uVar6 = ~uVar6;
  }
  else {
    uVar6 = 0;
    if (iVar4 != 0) {
      uVar6 = iVar5 / iVar4;
    }
  }
  iVar5 = *(int *)(param_5 + 0x1c);
  if (iVar1 < 0) {
    uVar7 = 0;
    if (iVar5 != 0) {
      uVar7 = -iVar1 / iVar5;
    }
    uVar7 = ~uVar7;
  }
  else {
    uVar7 = 0;
    if (iVar5 != 0) {
      uVar7 = iVar1 / iVar5;
    }
  }
  if (iVar2 < 0) {
    uVar8 = 0;
    if (iVar4 != 0) {
      uVar8 = -iVar2 / iVar4;
    }
    uVar8 = ~uVar8;
  }
  else {
    uVar8 = 0;
    if (iVar4 != 0) {
      uVar8 = iVar2 / iVar4;
    }
  }
  if (iVar3 < 0) {
    uVar9 = 0;
    if (iVar5 != 0) {
      uVar9 = -iVar3 / iVar5;
    }
    uVar9 = ~uVar9;
  }
  else {
    uVar9 = 0;
    if (iVar5 != 0) {
      uVar9 = iVar3 / iVar5;
    }
  }
  local_20 = 0;
  uStack_18 = 0;
  kfw_bsp_BspRange___ctor(&local_20,uVar6,uVar7,uVar8,uVar9,0);
  auVar10._8_8_ = uStack_18;
  auVar10._0_8_ = local_20;
  return auVar10;
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___get_Count
// Address: 01789bdc
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___get_Count(long param_1,long param_2)

{
  if (*(long *)(param_1 + 0x28) != 0) {
                    /* WARNING: Could not recover jumptable at 0x01789bfc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (***(code ***)(*(long *)(*(long *)(param_2 + 0x20) + 0xc0) + 0x88))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_bsp_BspMap___Il2CppFullySharedGenericType___get_Item
// Address: 01789c04
// ==========================================================================================

void kfw_bsp_BspMap___Il2CppFullySharedGenericType___get_Item
               (long param_1,undefined4 param_2,void *param_3,long param_4)

{
  long lVar1;
  long lVar2;
  undefined8 *puVar3;
  ulong __n;
  void *__src;
  undefined4 *local_50;
  void *pvStack_48;
  undefined4 local_3c;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  lVar2 = *(long *)(*(long *)(param_4 + 0x20) + 0xc0);
  __n = (ulong)*(uint *)(*(long *)(lVar2 + 0x28) + 0xfc);
  __src = (void *)((long)&local_50 - (__n + 0xf & 0x1fffffff0));
  if (*(long *)(param_1 + 0x28) == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  puVar3 = *(undefined8 **)(lVar2 + 0x90);
  local_50 = &local_3c;
  pvStack_48 = __src;
  local_3c = param_2;
  (*(code *)puVar3[2])(*puVar3,puVar3,*(long *)(param_1 + 0x28),&local_50,__src);
  memcpy(param_3,__src,__n);
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: kfw_panel_MainPanel___ctor
// Address: 017d1938
// ==========================================================================================

void kfw_panel_MainPanel___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  puVar4 = 
  PTR_Field__PrivateImplementationDetails__B9B4BF90537CFC069C0DC7C85ED61BD888F406CE37AB4C20F65BD2B4767A2219_01fc79b8
  ;
  puVar3 = PTR_char___TypeInfo_01fc59b0;
  puVar2 = PTR_StringLiteral_11483_01fc3fd8;
  puVar1 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_021008d8 & 1) == 0) {
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__B9B4BF90537CFC069C0DC7C85ED61BD888F406CE37AB4C20F65BD2B4767A2219_01fc79b8
                );
    FUN_00db0bbc(PTR_StringLiteral_11483_01fc3fd8);
    DAT_021008d8 = 1;
  }
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,4);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar5,*(undefined8 *)puVar4,0);
  uVar6 = *(undefined8 *)puVar2;
  *(undefined *)(param_1 + 0x78) = 1;
  *(undefined8 *)(param_1 + 0x68) = uVar5;
  *(undefined8 *)(param_1 + 0x70) = uVar6;
  *(undefined4 *)(param_1 + 0x7c) = 2;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar1,4);
  *(undefined8 *)(param_1 + 0xa0) = uVar5;
  kairo_unity_panel_FepPanel___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel___ctor
// Address: 017d1a10
// ==========================================================================================

void kfw_panel_MainPanel___ctor
               (long param_1,undefined8 param_2,undefined8 param_3,undefined4 param_4,
               undefined4 param_5,undefined8 param_6)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  puVar4 = 
  PTR_Field__PrivateImplementationDetails__B9B4BF90537CFC069C0DC7C85ED61BD888F406CE37AB4C20F65BD2B4767A2219_01fc79b8
  ;
  puVar3 = PTR_char___TypeInfo_01fc59b0;
  puVar2 = PTR_StringLiteral_11483_01fc3fd8;
  puVar1 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_021008d9 & 1) == 0) {
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__B9B4BF90537CFC069C0DC7C85ED61BD888F406CE37AB4C20F65BD2B4767A2219_01fc79b8
                );
    FUN_00db0bbc(PTR_StringLiteral_11483_01fc3fd8);
    DAT_021008d9 = 1;
  }
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,4);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar5,*(undefined8 *)puVar4,0);
  uVar6 = *(undefined8 *)puVar2;
  *(undefined *)(param_1 + 0x78) = 1;
  *(undefined8 *)(param_1 + 0x68) = uVar5;
  *(undefined8 *)(param_1 + 0x70) = uVar6;
  *(undefined4 *)(param_1 + 0x7c) = 2;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar1,4);
  *(undefined8 *)(param_1 + 0xa0) = uVar5;
  kairo_unity_panel_FepPanel___ctor(param_1,0);
  kfw_panel_MainPanel__Init(param_1,param_2,param_3,param_4,param_5,param_6);
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__Init
// Address: 017d1b28
// ==========================================================================================

void kfw_panel_MainPanel__Init
               (long param_1,undefined8 param_2,long param_3,int param_4,int param_5,long param_6)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined8 uVar8;
  ulong uVar9;
  long lVar10;
  long lVar11;
  undefined2 local_54 [2];
  
  if ((DAT_021008da & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_panel_Button_TypeInfo_01fc79c0);
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_panel_Label_TypeInfo_01fc79c8);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0);
    FUN_00db0bbc(PTR_kairo_unity_panel_TextBox_TypeInfo_01fc79d0);
    FUN_00db0bbc(PTR_StringLiteral_9587_01fc79d8);
    FUN_00db0bbc(PTR_StringLiteral_11826_01fc3510);
    FUN_00db0bbc(PTR_StringLiteral_2471_01fc79e0);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_11654_01fc3560);
    FUN_00db0bbc(PTR_StringLiteral_6343_01fc79e8);
    DAT_021008da = 1;
  }
  local_54[0] = 0;
  *(long *)(param_1 + 0x98) = param_3;
  *(int *)(param_1 + 0x60) = param_4;
  *(int *)(param_1 + 0x7c) = param_5;
  if (param_6 != 0) {
    *(long *)(param_1 + 0x70) = param_6;
  }
  puVar2 = PTR_StringLiteral_1_01fbf388;
  if (param_5 != 2) {
    *(undefined2 *)(param_1 + 0x78) = 0x100;
  }
  puVar3 = PTR_StringLiteral_9587_01fc79d8;
  puVar1 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  uVar8 = *(undefined8 *)puVar2;
  if (0 < param_4) {
    iVar5 = 0;
    do {
      uVar8 = System_String__Concat(uVar8,*(undefined8 *)puVar3,0);
      iVar5 = iVar5 + 1;
    } while (iVar5 < *(int *)(param_1 + 0x60));
  }
  iVar4 = kfw_panel_MainPanel__GetStringWidth(uVar8,uVar8);
  iVar5 = -0x80000000;
  if ((float)iVar4 * DAT_005bcee4 != INFINITY) {
    iVar5 = (int)((float)iVar4 * DAT_005bcee4);
  }
  *(int *)(param_1 + 100) = iVar5;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar9 = kairo_unity_util_Language__Japanese(0);
  puVar3 = PTR_char_TypeInfo_01fbf990;
  lVar11 = param_3;
  if ((uVar9 & 1) == 0) {
    if (param_3 == 0) goto LAB_017d2108;
    lVar11 = *(long *)puVar2;
    if (0 < *(int *)(param_3 + 0x10)) {
      iVar5 = 0;
      do {
        local_54[0] = System_String__get_Chars(param_3,iVar5,0);
        if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c(*(long *)puVar3);
        }
        uVar8 = System_Char__ToString(local_54,0);
        lVar10 = System_String__Concat(lVar11,uVar8,0);
        iVar4 = kfw_panel_MainPanel__GetStringWidth(lVar10,lVar10);
      } while ((iVar4 <= *(int *)(param_1 + 100)) &&
              (iVar5 = iVar5 + 1, lVar11 = lVar10, iVar5 < *(int *)(param_3 + 0x10)));
    }
  }
  if (*(int *)(*(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar3 = PTR_kairo_unity_panel_TextBox_TypeInfo_01fc79d0;
  puVar2 = PTR_kairo_unity_panel_Label_TypeInfo_01fc79c8;
  iVar5 = kairo_common_cfg_Config__get_Platform(0);
  if (iVar5 == 2) {
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar10 = kairo_unity_util_Language__GetLanguageCode(0);
    if (lVar10 != 0) {
      if (*(int *)(*(long *)PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0 + 0xe0) == 0)
      {
        thunk_FUN_00df405c();
      }
      uVar9 = System_Text_RegularExpressions_Regex__IsMatch
                        (lVar10,*(undefined8 *)PTR_StringLiteral_6343_01fc79e8,1,0);
      if ((uVar9 & 1) == 0) goto LAB_017d1df8;
    }
    param_2 = *(undefined8 *)PTR_StringLiteral_2471_01fc79e0;
  }
LAB_017d1df8:
  uVar8 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  kairo_unity_panel_Label___ctor(uVar8,param_2,0);
  *(undefined8 *)(param_1 + 0x38) = uVar8;
  lVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  kairo_unity_panel_TextBox___ctor(lVar10,lVar11,0x14,1,0,0);
  *(long *)(param_1 + 0x40) = lVar10;
  puVar2 = PTR_kairo_unity_panel_Button_TypeInfo_01fc79c0;
  if (lVar10 != 0) {
    *(int *)(lVar10 + 0x1c) = param_5;
    *(int *)(lVar10 + 0x20) = param_4;
    puVar3 = PTR_StringLiteral_11654_01fc3560;
    puVar1 = PTR_StringLiteral_11826_01fc3510;
    uVar8 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    kairo_unity_panel_Button___ctor(uVar8,*(undefined8 *)puVar1,0);
    *(undefined8 *)(param_1 + 0x48) = uVar8;
    uVar8 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    kairo_unity_panel_Button___ctor(uVar8,*(undefined8 *)puVar3,0);
    *(undefined8 *)(param_1 + 0x50) = uVar8;
    if (*(long *)(param_1 + 0x40) != 0) {
      *(undefined8 *)(param_1 + 0x90) = *(undefined8 *)(*(long *)(param_1 + 0x40) + 0x10);
      kairo_unity_panel_FepPanel__SetLayoutManager(param_1,0,0);
      lVar11 = *(long *)(param_1 + 0x38);
      iVar5 = kairo_unity_panel_FepPanel__GetWidth(param_1,0);
      if (*(long *)(param_1 + 0x38) != 0) {
        iVar4 = kairo_unity_panel_Label__GetWidth(*(long *)(param_1 + 0x38),0);
        iVar6 = kairo_unity_panel_FepPanel__GetHeight(param_1,0);
        if ((*(long *)(param_1 + 0x38) != 0) &&
           (iVar7 = kairo_unity_panel_Label__GetHeight(*(long *)(param_1 + 0x38),0), lVar11 != 0)) {
          if (iVar5 < 0) {
            iVar5 = iVar5 + 1;
          }
          if (iVar4 < 0) {
            iVar4 = iVar4 + 1;
          }
          if (iVar6 < 0) {
            iVar6 = iVar6 + 1;
          }
          kairo_unity_panel_Label__SetLocation
                    (lVar11,(iVar5 >> 1) - (iVar4 >> 1),((iVar6 >> 1) - iVar7) + -0x10,0);
          lVar11 = *(long *)(param_1 + 0x40);
          iVar5 = kairo_unity_panel_FepPanel__GetWidth(param_1,0);
          if (*(long *)(param_1 + 0x40) != 0) {
            iVar4 = kairo_unity_panel_TextBox__GetWidth(*(long *)(param_1 + 0x40),0);
            iVar6 = kairo_unity_panel_FepPanel__GetHeight(param_1,0);
            if (lVar11 != 0) {
              if (iVar5 < 0) {
                iVar5 = iVar5 + 1;
              }
              if (iVar4 < 0) {
                iVar4 = iVar4 + 1;
              }
              if (iVar6 < 0) {
                iVar6 = iVar6 + 1;
              }
              kairo_unity_panel_TextBox__SetLocation
                        (lVar11,(iVar5 >> 1) - (iVar4 >> 1),(iVar6 >> 1) + -0xc,0);
              lVar11 = *(long *)(param_1 + 0x48);
              iVar5 = kairo_unity_panel_FepPanel__GetWidth(param_1,0);
              if (*(long *)(param_1 + 0x48) != 0) {
                iVar6 = kairo_unity_panel_Button__GetWidth(*(long *)(param_1 + 0x48),0);
                iVar4 = kairo_unity_panel_FepPanel__GetHeight(param_1,0);
                if ((*(long *)(param_1 + 0x40) != 0) &&
                   (iVar7 = kairo_unity_panel_TextBox__GetHeight(*(long *)(param_1 + 0x40),0),
                   lVar11 != 0)) {
                  if (iVar5 < 0) {
                    iVar5 = iVar5 + 1;
                  }
                  if (iVar4 < 0) {
                    iVar4 = iVar4 + 1;
                  }
                  kairo_unity_panel_Button__SetLocation
                            (lVar11,((iVar5 >> 1) - iVar6) + -4,iVar7 + (iVar4 >> 1) + -8,0);
                  lVar11 = *(long *)(param_1 + 0x50);
                  iVar5 = kairo_unity_panel_FepPanel__GetWidth(param_1,0);
                  iVar4 = kairo_unity_panel_FepPanel__GetHeight(param_1,0);
                  if ((*(long *)(param_1 + 0x40) != 0) &&
                     (iVar6 = kairo_unity_panel_TextBox__GetHeight(*(long *)(param_1 + 0x40),0),
                     lVar11 != 0)) {
                    if (iVar5 < 0) {
                      iVar5 = iVar5 + 1;
                    }
                    if (iVar4 < 0) {
                      iVar4 = iVar4 + 1;
                    }
                    kairo_unity_panel_Button__SetLocation
                              (lVar11,(iVar5 >> 1) + 4,iVar6 + (iVar4 >> 1) + -8,0);
                    kairo_unity_panel_FepPanel__Add(param_1,*(undefined8 *)(param_1 + 0x38),0);
                    kairo_unity_panel_FepPanel__Add(param_1,*(undefined8 *)(param_1 + 0x40),0);
                    kairo_unity_panel_FepPanel__Add(param_1,*(undefined8 *)(param_1 + 0x48),0);
                    kairo_unity_panel_FepPanel__Add(param_1,*(undefined8 *)(param_1 + 0x50),0);
                    kairo_unity_panel_FepPanel__SetComponentListener(param_1,param_1,0);
                    return;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
LAB_017d2108:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__GetStringWidth
// Address: 017d210c
// ==========================================================================================

undefined4 kfw_panel_MainPanel__GetStringWidth(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined4 uVar2;
  long lVar3;
  
  puVar1 = PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70;
  if ((DAT_021008df & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70);
    DAT_021008df = 1;
  }
  lVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  kairo_unity_ui_Font___ctor(lVar3,0);
  if (lVar3 != 0) {
    uVar2 = kairo_unity_ui_Font__StringWidth(lVar3,param_2,0);
    kairo_unity_ui_Font__Dispose(lVar3,0);
    return uVar2;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__Show
// Address: 017d218c
// ==========================================================================================

undefined8 kfw_panel_MainPanel__Show(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar2 = PTR_StringLiteral_1_01fbf388;
  if ((DAT_021008db & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_021008db = 1;
  }
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  *(undefined8 *)(param_1 + 0x58) = param_2;
  kairo_unity_panel_FepPanel_Display__SetCurrent(param_1,0);
  kairo_unity_panel_FepPanel__SetSoftLabel(param_1,0,*(undefined8 *)puVar2,0);
  kairo_unity_panel_FepPanel__SetSoftLabel(param_1,1,*(undefined8 *)puVar2,0);
  *(undefined *)(param_1 + 0x80) = 0;
  do {
    kairo_unity_panel_FepPanel__Show(param_1,0);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_ui_IApplication__Sleep(1,0);
  } while (*(char *)(param_1 + 0x80) == '\0');
  return *(undefined8 *)(param_1 + 0x88);
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__Show
// Address: 017d225c
// ==========================================================================================

void kfw_panel_MainPanel__Show(long param_1,long param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined8 uVar2;
  long lVar3;
  
  if ((DAT_021008dc & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_021008dc = 1;
  }
  *(long *)(param_1 + 0x58) = param_2;
  if (param_2 != 0) {
    lVar3 = *(long *)(param_1 + 0xa0);
    uVar2 = kairo_unity_ui_Canvas__GetSoftLabel(param_2,0,0);
    if (lVar3 != 0) {
      if (*(int *)(lVar3 + 0x18) != 0) {
        *(undefined8 *)(lVar3 + 0x20) = uVar2;
        lVar3 = *(long *)(param_1 + 0xa0);
        uVar2 = kairo_unity_ui_Canvas__GetSoftLabel(param_2,1,0);
        if (lVar3 == 0) goto LAB_017d2394;
        if (1 < *(uint *)(lVar3 + 0x18)) {
          *(undefined8 *)(lVar3 + 0x28) = uVar2;
          lVar3 = *(long *)(param_1 + 0xa0);
          uVar2 = kairo_unity_ui_Canvas__GetSoftLabel(param_2,2,0);
          if (lVar3 == 0) goto LAB_017d2394;
          if (2 < *(uint *)(lVar3 + 0x18)) {
            *(undefined8 *)(lVar3 + 0x30) = uVar2;
            lVar3 = *(long *)(param_1 + 0xa0);
            uVar2 = kairo_unity_ui_Canvas__GetSoftLabel(param_2,3,0);
            puVar1 = PTR_StringLiteral_1_01fbf388;
            if (lVar3 == 0) goto LAB_017d2394;
            if (3 < *(uint *)(lVar3 + 0x18)) {
              *(undefined8 *)(lVar3 + 0x38) = uVar2;
              kairo_unity_ui_Canvas__SetSoftLabel
                        (param_2,*(undefined8 *)puVar1,*(undefined8 *)puVar1,0,0,0);
              kairo_unity_ui_Canvas__UpdateSoftLabel(param_2,0);
              kairo_unity_panel_FepPanel_Display__SetCurrent(param_1,0);
              *(undefined *)(param_1 + 0x80) = 0;
              *(undefined8 *)(param_1 + 0xa8) = param_3;
              kairo_unity_panel_FepPanel__Start(param_1,0);
              return;
            }
          }
        }
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
LAB_017d2394:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__ComponentAction
// Address: 017d239c
// ==========================================================================================

void kfw_panel_MainPanel__ComponentAction(long param_1,long param_2,int param_3)

{
  int iVar1;
  undefined uVar2;
  uint uVar3;
  char cVar4;
  char cVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  bool bVar9;
  bool bVar10;
  byte bVar11;
  int iVar12;
  int iVar13;
  long lVar14;
  long lVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 *puVar18;
  undefined uVar19;
  ulong uVar20;
  long lVar21;
  int local_64;
  
  if ((DAT_021008dd & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100);
    FUN_00db0bbc(PTR_java_lang_JString_TypeInfo_01fbf368);
    FUN_00db0bbc(PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_0_01fc79f0);
    FUN_00db0bbc(PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_1_01fc79f8);
    FUN_00db0bbc(PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_2_01fc7a00);
    FUN_00db0bbc(PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_3_01fc7a08);
    FUN_00db0bbc(PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_4_01fc7a10);
    FUN_00db0bbc(PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128);
    FUN_00db0bbc(PTR_StringLiteral_37_01fbf7b8);
    FUN_00db0bbc(PTR_StringLiteral_11691_01fc7a18);
    FUN_00db0bbc(PTR_StringLiteral_113_01fbf6b8);
    FUN_00db0bbc(PTR_StringLiteral_11391_01fc7a20);
    FUN_00db0bbc(PTR_StringLiteral_11042_01fc7a28);
    FUN_00db0bbc(PTR_StringLiteral_12625_01fc7a30);
    FUN_00db0bbc(PTR_StringLiteral_499_01fc7a38);
    FUN_00db0bbc(PTR_StringLiteral_11402_01fc7a40);
    FUN_00db0bbc(PTR_StringLiteral_1275_01fc7a48);
    FUN_00db0bbc(PTR_StringLiteral_11370_01fc7a50);
    FUN_00db0bbc(PTR_StringLiteral_1244_01fc7a58);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_021008dd = 1;
  }
  if (param_3 == 1) {
    if (param_2 == *(long *)(param_1 + 0x48)) {
      if ((*(long *)(param_1 + 0x40) == 0) ||
         (lVar14 = *(long *)(*(long *)(param_1 + 0x40) + 0x10), lVar14 == 0)) goto LAB_017d2e1c;
      lVar14 = System_String__Replace(lVar14,10,0x20,0);
      if (*(char *)(param_1 + 0x79) != '\0') {
        if (lVar14 == 0) goto LAB_017d2e1c;
        lVar14 = System_String__Trim(lVar14,0);
      }
      puVar7 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
      if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      bVar11 = kairo_unity_util_Language__Japanese(0);
      puVar6 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      lVar15 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      bVar11 = 3 < *(int *)(param_1 + 0x60) & (bVar11 ^ 1);
      if (*(int *)(lVar15 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar15 = *(long *)puVar6;
      }
      cVar4 = *(char *)(*(long *)(lVar15 + 0xb8) + 0x19a);
      cVar5 = *(char *)(*(long *)(lVar15 + 0xb8) + 0x19c);
      if (bVar11 == 0) {
        iVar13 = *(int *)(param_1 + 0x60);
        if (3 < iVar13) {
          iVar12 = kairo_unity_panel_FepPanel__GetStringLength(lVar14,0);
          iVar13 = *(int *)(param_1 + 0x60);
          goto LAB_017d26ec;
        }
        if (lVar14 == 0) goto LAB_017d2e1c;
        iVar12 = *(int *)(lVar14 + 0x10);
        bVar9 = SBORROW4(iVar12,iVar13);
        iVar1 = iVar12 - iVar13;
        bVar10 = iVar12 == iVar13;
      }
      else {
        iVar12 = kfw_panel_MainPanel__GetStringWidth(lVar15,lVar14);
        iVar13 = *(int *)(param_1 + 100);
LAB_017d26ec:
        bVar9 = SBORROW4(iVar12,iVar13);
        iVar1 = iVar12 - iVar13;
        bVar10 = iVar12 == iVar13;
      }
      lVar15 = *(long *)puVar6;
      bVar9 = iVar1 < 0 == bVar9;
      uVar19 = !bVar10 && bVar9;
      if (*(int *)(lVar15 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar15 = *(long *)puVar6;
      }
      if (((*(char *)(*(long *)(lVar15 + 0xb8) + 0x10) != '\0') && (!bVar10 && bVar9)) &&
         (*(int *)(param_1 + 0x7c) == 0)) {
        if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        kairo_unity_util_Log__Info(*(undefined8 *)PTR_StringLiteral_11691_01fc7a18,0,0);
        uVar19 = false;
      }
      lVar15 = *(long *)(param_1 + 0x68);
      if (lVar15 != 0) {
        uVar20 = 0;
        do {
          if ((long)(int)*(uint *)(lVar15 + 0x18) <= (long)uVar20) {
LAB_017d27ac:
            lVar15 = FUN_00db0c30(*(undefined8 *)PTR_char___TypeInfo_01fc59b0,1);
            if (lVar15 == 0) break;
            if (*(int *)(lVar15 + 0x18) == 0) goto LAB_017d2e20;
            *(undefined2 *)(lVar15 + 0x20) = 8;
            if ((lVar14 == 0) || (lVar15 = System_String__Trim(lVar14,lVar15,0), lVar15 == 0))
            break;
            uVar16 = System_String__Trim(lVar15,0);
            iVar13 = java_lang_StringEx__Length(uVar16,0);
            puVar6 = PTR_StringLiteral_499_01fc7a38;
            uVar2 = 3;
            if (iVar13 != 0) {
              uVar2 = uVar19;
            }
            uVar20 = System_String__Contains(lVar14,*(undefined8 *)PTR_StringLiteral_499_01fc7a38,0)
            ;
            uVar19 = 4;
            if ((uVar20 & 1) == 0) {
              uVar19 = uVar2;
            }
            if (cVar5 != '\0') {
              uVar16 = kairo_unity_util_StringUtil__Replace
                                 (*(undefined8 *)(param_1 + 0x98),
                                  *(undefined8 *)PTR_StringLiteral_37_01fbf7b8,
                                  *(undefined8 *)PTR_StringLiteral_1_01fbf388,0);
              uVar20 = System_String__op_Inequality(uVar16,lVar14,0);
              if ((uVar20 & 1) == 0) goto LAB_017d288c;
              if (*(int *)(*(long *)PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660 + 0xe0) ==
                  0) {
                thunk_FUN_00df405c();
              }
              uVar20 = kairo_unity_native_KairoPlugin__CheckNgWord(lVar14,0);
              if ((uVar20 & 1) == 0) goto LAB_017d288c;
switchD_017d28ac_caseD_5:
              lVar14 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100
                                         );
              kairo_unity_ui_Dialog___ctor
                        (lVar14,1,*(undefined8 *)PTR_StringLiteral_12625_01fc7a30,0);
              if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar16 = kairo_unity_util_Language__TranslateText
                                 (*(undefined8 *)PTR_StringLiteral_11370_01fc7a50,1,0);
              if (lVar14 != 0) {
                kairo_unity_ui_Dialog__SetText(lVar14,uVar16,0);
                if (cVar4 == '\0') goto LAB_017d2e0c;
                uVar16 = thunk_FUN_00e11c14(*(undefined8 *)
                                             PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128
                                           );
                puVar18 = (undefined8 *)
                          PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_4_01fc7a10;
                goto LAB_017d2c24;
              }
              break;
            }
LAB_017d288c:
            switch(uVar19) {
            case 0:
              *(long *)(param_1 + 0x88) = lVar14;
              uVar20 = System_String__Equals(lVar14,*(undefined8 *)(param_1 + 0x90),0);
              if ((uVar20 & 1) == 0) {
                lVar14 = System_String__Concat
                                   (*(undefined8 *)(param_1 + 0x88),
                                    *(undefined8 *)PTR_StringLiteral_37_01fbf7b8,0);
              }
              else {
                lVar14 = *(long *)(param_1 + 0x98);
              }
              cVar4 = *(char *)(param_1 + 0x78);
              *(long *)(param_1 + 0x88) = lVar14;
              puVar7 = PTR_StringLiteral_37_01fbf7b8;
              goto joined_r0x017d2c84;
            case 1:
              iVar13 = *(int *)(param_1 + 0x60);
              if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar20 = kairo_unity_util_Language__Japanese(0);
              puVar18 = (undefined8 *)PTR_StringLiteral_1275_01fc7a48;
              if (*(int *)(param_1 + 0x7c) == 2) {
                iVar12 = *(int *)(param_1 + 0x60);
                iVar1 = iVar13;
                if (iVar13 < 0) {
                  iVar1 = iVar13 + 1;
                }
                iVar1 = iVar1 >> 1;
                if ((uVar20 & 1) == 0) {
                  iVar1 = iVar13;
                }
                if (3 < iVar12) {
                  puVar18 = (undefined8 *)PTR_StringLiteral_11391_01fc7a20;
                  iVar12 = iVar1;
                }
              }
              else {
                iVar12 = *(int *)(param_1 + 0x60);
              }
              if (bVar11 == 0) {
                uVar16 = *puVar18;
                if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                  thunk_FUN_00df405c();
                }
                uVar20 = kairo_unity_util_Language__Japanese(0);
                if ((uVar20 & 1) == 0) goto LAB_017d2d1c;
              }
              else {
LAB_017d2d1c:
                uVar16 = *(undefined8 *)PTR_StringLiteral_11402_01fc7a40;
              }
              lVar14 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100
                                         );
              kairo_unity_ui_Dialog___ctor
                        (lVar14,1,*(undefined8 *)PTR_StringLiteral_12625_01fc7a30,0);
              if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar16 = kairo_unity_util_Language__TranslateText(uVar16,1,0);
              if (*(int *)(*(long *)PTR_java_lang_JString_TypeInfo_01fbf368 + 0xe0) == 0) {
                thunk_FUN_00df405c(*(long *)PTR_java_lang_JString_TypeInfo_01fbf368);
              }
              local_64 = iVar12;
              uVar17 = System_Int32__ToString(&local_64,0);
              uVar16 = kairo_unity_util_StringUtil__Replace(uVar16,uVar17,0);
              if (lVar14 != 0) {
                kairo_unity_ui_Dialog__SetText(lVar14,uVar16,0);
                if (cVar4 != '\0') {
                  uVar16 = thunk_FUN_00e11c14(*(undefined8 *)
                                               PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128
                                             );
                  kairo_unity_ui_Dialog_OnFinishMethod___ctor
                            (uVar16,param_1,
                             *(undefined8 *)
                              PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_0_01fc79f0,0);
                  kairo_unity_ui_Dialog__Show(lVar14,uVar16,0);
                  return;
                }
                goto LAB_017d2e0c;
              }
              goto LAB_017d2e1c;
            case 2:
              lVar14 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100
                                         );
              kairo_unity_ui_Dialog___ctor
                        (lVar14,1,*(undefined8 *)PTR_StringLiteral_12625_01fc7a30,0);
              puVar8 = PTR_char_TypeInfo_01fbf990;
              puVar6 = PTR_StringLiteral_113_01fbf6b8;
              lVar15 = *(long *)(param_1 + 0x68);
              if (lVar15 != 0) {
                uVar20 = 0;
                uVar16 = *(undefined8 *)PTR_StringLiteral_1_01fbf388;
                lVar21 = 0x20;
                goto LAB_017d2a08;
              }
              goto LAB_017d2e1c;
            case 3:
              lVar14 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100
                                         );
              kairo_unity_ui_Dialog___ctor
                        (lVar14,1,*(undefined8 *)PTR_StringLiteral_12625_01fc7a30,0);
              if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar16 = kairo_unity_util_Language__TranslateText
                                 (*(undefined8 *)PTR_StringLiteral_1244_01fc7a58,1,0);
              uVar16 = kairo_unity_util_StringUtil__Replace
                                 (uVar16,*(undefined8 *)(param_1 + 0x70),0);
              if (lVar14 != 0) {
                kairo_unity_ui_Dialog__SetText(lVar14,uVar16,0);
                if (cVar4 == '\0') goto LAB_017d2e0c;
                uVar16 = thunk_FUN_00e11c14(*(undefined8 *)
                                             PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128
                                           );
                puVar18 = (undefined8 *)
                          PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_2_01fc7a00;
                goto LAB_017d2c24;
              }
              goto LAB_017d2e1c;
            case 4:
              lVar14 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100
                                         );
              kairo_unity_ui_Dialog___ctor
                        (lVar14,1,*(undefined8 *)PTR_StringLiteral_12625_01fc7a30,0);
              if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar16 = kairo_unity_util_Language__TranslateText
                                 (*(undefined8 *)PTR_StringLiteral_11042_01fc7a28,1,0);
              uVar16 = kairo_unity_util_StringUtil__Replace(uVar16,*(undefined8 *)puVar6,0);
              if (lVar14 != 0) {
                kairo_unity_ui_Dialog__SetText(lVar14,uVar16,0);
                if (cVar4 == '\0') goto LAB_017d2e0c;
                uVar16 = thunk_FUN_00e11c14(*(undefined8 *)
                                             PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128
                                           );
                puVar18 = (undefined8 *)
                          PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_3_01fc7a08;
                goto LAB_017d2c24;
              }
              goto LAB_017d2e1c;
            case 5:
              goto switchD_017d28ac_caseD_5;
            default:
              goto switchD_017d28ac_caseD_6;
            }
          }
          if (*(uint *)(lVar15 + 0x18) <= uVar20) goto LAB_017d2e20;
          if (lVar14 == 0) break;
          iVar13 = System_String__IndexOf(lVar14,*(undefined2 *)(lVar15 + uVar20 * 2 + 0x20),0);
          if (iVar13 != -1) {
            uVar19 = 2;
            goto LAB_017d27ac;
          }
          lVar15 = *(long *)(param_1 + 0x68);
          uVar20 = uVar20 + 1;
        } while (lVar15 != 0);
      }
      goto LAB_017d2e1c;
    }
    *(undefined8 *)(param_1 + 0x88) = 0;
    kairo_unity_panel_FepPanel_Display__SetCurrent(*(undefined8 *)(param_1 + 0x58),0);
    *(undefined *)(param_1 + 0x80) = 1;
    if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar14 = kairo_unity_ui_Canvas__GetInstance(0);
    if (lVar14 == 0) goto LAB_017d2e1c;
    kairo_unity_ui_Canvas__SetInputGuard(lVar14,100,0);
  }
switchD_017d28ac_caseD_6:
  if (*(char *)(param_1 + 0x80) == '\0') {
    kairo_unity_panel_FepPanel__Start(param_1,0);
    return;
  }
  lVar14 = *(long *)(param_1 + 0xa8);
  if (lVar14 != 0) {
    (**(code **)(lVar14 + 0x18))
              (*(undefined8 *)(lVar14 + 0x40),*(undefined8 *)(param_1 + 0x88),
               *(undefined8 *)(lVar14 + 0x28));
  }
  lVar14 = *(long *)(param_1 + 0xa0);
  if (lVar14 != 0) {
    uVar3 = *(uint *)(lVar14 + 0x18);
    if (((uVar3 == 0) || (uVar3 == 1)) || ((uVar3 < 3 || (uVar3 == 3)))) {
LAB_017d2e20:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if (*(long *)(param_1 + 0x58) != 0) {
      kairo_unity_ui_Canvas__SetSoftLabel
                (*(long *)(param_1 + 0x58),*(undefined8 *)(lVar14 + 0x20),
                 *(undefined8 *)(lVar14 + 0x28),*(undefined8 *)(lVar14 + 0x30),
                 *(undefined8 *)(lVar14 + 0x38),0);
      return;
    }
  }
LAB_017d2e1c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
LAB_017d2a08:
  if ((long)uVar20 < (long)*(int *)(lVar15 + 0x18)) {
    iVar13 = java_lang_StringEx__Length(uVar16,0);
    if (0 < iVar13) {
      uVar16 = System_String__Concat(uVar16,*(undefined8 *)puVar6,0);
    }
    lVar15 = *(long *)(param_1 + 0x68);
    if (lVar15 != 0) {
      if (*(int *)(*(long *)puVar8 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      if (uVar20 < *(uint *)(lVar15 + 0x18)) goto code_r0x017d2a60;
      goto LAB_017d2e20;
    }
  }
  else {
    if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar17 = kairo_unity_util_Language__TranslateText
                       (*(undefined8 *)PTR_StringLiteral_11042_01fc7a28,1,0);
    uVar16 = kairo_unity_util_StringUtil__Replace(uVar17,uVar16,0);
    if (lVar14 != 0) {
      kairo_unity_ui_Dialog__SetText(lVar14,uVar16,0);
      if (cVar4 != '\0') {
        uVar16 = thunk_FUN_00e11c14(*(undefined8 *)
                                     PTR_kairo_unity_ui_Dialog_OnFinishMethod_TypeInfo_01fc0128);
        puVar18 = (undefined8 *)PTR_Method_kfw_panel_MainPanel__ComponentAction_b__30_1_01fc79f8;
LAB_017d2c24:
        kairo_unity_ui_Dialog_OnFinishMethod___ctor(uVar16,param_1,*puVar18,0);
        kairo_unity_ui_Dialog__Show(lVar14,uVar16,0);
        return;
      }
LAB_017d2e0c:
      kairo_unity_ui_Dialog__Show(lVar14,0);
      goto switchD_017d28ac_caseD_6;
    }
  }
  goto LAB_017d2e1c;
code_r0x017d2a60:
  lVar15 = lVar15 + lVar21;
  uVar20 = uVar20 + 1;
  lVar21 = lVar21 + 2;
  uVar17 = System_Char__ToString(lVar15,0);
  uVar16 = System_String__Concat(uVar16,uVar17,0);
  lVar15 = *(long *)(param_1 + 0x68);
  if (lVar15 == 0) goto LAB_017d2e1c;
  goto LAB_017d2a08;
joined_r0x017d2c84:
  if (cVar4 != '\0') goto LAB_017d2cd4;
  if (lVar14 == 0) goto LAB_017d2e1c;
  uVar20 = System_String__EndsWith(lVar14,*(undefined8 *)puVar7,0);
  if ((uVar20 & 1) == 0) goto LAB_017d2cd4;
  uVar16 = *(undefined8 *)(param_1 + 0x88);
  iVar13 = java_lang_StringEx__Length(uVar16,0);
  lVar14 = java_lang_StringEx__SubstringJ(uVar16,0,iVar13 + -1,0);
  cVar4 = *(char *)(param_1 + 0x78);
  *(long *)(param_1 + 0x88) = lVar14;
  goto joined_r0x017d2c84;
LAB_017d2cd4:
  kairo_unity_panel_FepPanel_Display__SetCurrent(*(undefined8 *)(param_1 + 0x58),0);
  *(undefined *)(param_1 + 0x80) = 1;
  goto switchD_017d28ac_caseD_6;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__ReStart
// Address: 017d2e40
// ==========================================================================================

void kfw_panel_MainPanel__ReStart(undefined8 param_1)

{
  kairo_unity_panel_FepPanel__Start(param_1,0);
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__SetProhibition
// Address: 017d2e48
// ==========================================================================================

void kfw_panel_MainPanel__SetProhibition(long param_1,long param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_char___TypeInfo_01fc59b0;
  if ((DAT_021008de & 1) == 0) {
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    DAT_021008de = 1;
  }
  if (param_2 != 0) {
    uVar2 = FUN_00db0c30(*(undefined8 *)puVar1,*(undefined4 *)(param_2 + 0x18));
    *(undefined8 *)(param_1 + 0x68) = uVar2;
    java_lang_JSystem__Arraycopy(param_2,0,uVar2,0,*(undefined4 *)(param_2 + 0x18),0);
    return;
  }
  uVar2 = FUN_00db0c30(*(undefined8 *)puVar1,0);
  *(undefined8 *)(param_1 + 0x68) = uVar2;
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__SetItemName
// Address: 017d2edc
// ==========================================================================================

void kfw_panel_MainPanel__SetItemName(long param_1,undefined8 param_2)

{
  *(undefined8 *)(param_1 + 0x70) = param_2;
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__SetEndMark
// Address: 017d2ee4
// ==========================================================================================

void kfw_panel_MainPanel__SetEndMark(long param_1,byte param_2)

{
  *(byte *)(param_1 + 0x78) = param_2 & 1;
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__SetTrim
// Address: 017d2ef0
// ==========================================================================================

void kfw_panel_MainPanel__SetTrim(long param_1,byte param_2)

{
  *(byte *)(param_1 + 0x79) = param_2 & 1;
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel__IsSupportsLanguage
// Address: 017d2efc
// ==========================================================================================

undefined8 kfw_panel_MainPanel__IsSupportsLanguage(void)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  ulong uVar5;
  
  puVar2 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_021008e0 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0);
    FUN_00db0bbc(PTR_StringLiteral_6343_01fc79e8);
    DAT_021008e0 = 1;
  }
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_util_Language__GetLanguageCode(0);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  iVar3 = kairo_common_cfg_Config__get_Platform(0);
  puVar2 = PTR_StringLiteral_6343_01fc79e8;
  if ((lVar4 != 0) && (iVar3 == 2)) {
    if (*(int *)(*(long *)PTR_System_Text_RegularExpressions_Regex_TypeInfo_01fc04c0 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar5 = System_Text_RegularExpressions_Regex__IsMatch(lVar4,*(undefined8 *)puVar2,1,0);
    if ((uVar5 & 1) != 0) {
      return 0;
    }
  }
  return 1;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel_OnFinishMethod___ctor
// Address: 017d3014
// ==========================================================================================

void kfw_panel_MainPanel_OnFinishMethod___ctor(long param_1,long param_2,long param_3)

{
  char cVar1;
  ulong uVar2;
  undefined8 uVar3;
  code *pcVar4;
  
  uVar3 = *(undefined8 *)(param_3 + 8);
  *(long *)(param_1 + 0x20) = param_2;
  *(long *)(param_1 + 0x28) = param_3;
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  cVar1 = *(char *)(param_3 + 0x52);
  *(long *)(param_1 + 0x40) = param_1;
  uVar2 = FUN_00db0c48(param_3);
  if ((uVar2 & 1) == 0) {
    if (cVar1 != '\0') {
      if (param_2 == 0) {
        uVar3 = thunk_FUN_00e29584(0,"Delegate to an instance method cannot have null \'this\'.");
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar3,0);
      }
      goto LAB_017d3060;
    }
    pcVar4 = FUN_00d6bd0c;
  }
  else {
    if (cVar1 != '\x01') {
LAB_017d3060:
      *(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(param_1 + 0x10);
      *(undefined8 *)(param_1 + 0x40) = *(undefined8 *)(param_1 + 0x20);
      goto LAB_017d3080;
    }
    pcVar4 = FUN_00d6bd2c;
  }
  *(code **)(param_1 + 0x18) = pcVar4;
LAB_017d3080:
  *(code **)(param_1 + 0x38) = FUN_00d6bcc4;
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel_OnFinishMethod__Invoke
// Address: 017d30b0
// ==========================================================================================

void kfw_panel_MainPanel_OnFinishMethod__Invoke(long param_1,undefined8 param_2)

{
                    /* WARNING: Could not recover jumptable at 0x017d30c0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(param_1 + 0x18))
            (*(undefined8 *)(param_1 + 0x40),param_2,*(undefined8 *)(param_1 + 0x28));
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel_OnFinishMethod__BeginInvoke
// Address: 017d30c4
// ==========================================================================================

void kfw_panel_MainPanel_OnFinishMethod__BeginInvoke(undefined8 param_1,undefined8 param_2)

{
  undefined8 local_20;
  undefined8 local_18;
  
  local_18 = 0;
  local_20 = param_2;
  thunk_FUN_00df702c(param_1,&local_20);
  return;
}



// ==========================================================================================
// Function: kfw_panel_MainPanel_OnFinishMethod__EndInvoke
// Address: 017d30e4
// ==========================================================================================

void kfw_panel_MainPanel_OnFinishMethod__EndInvoke(undefined8 param_1,undefined8 param_2)

{
  thunk_FUN_00df70f0(param_2,0);
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspContents___ctor
// Address: 017d30f0
// ==========================================================================================

void kfw_bsp_BspContents___ctor(long param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspKey___ctor
// Address: 017d3118
// ==========================================================================================

void kfw_bsp_BspKey___ctor(long param_1,undefined8 param_2)

{
  System_Object___ctor(param_1,0);
  *(undefined8 *)(param_1 + 0x10) = param_2;
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspNode___ctor
// Address: 017d3140
// ==========================================================================================

void kfw_bsp_BspNode___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_Method_System_Collections_Generic_List_BspContents___ctor_01fc7a68;
  puVar1 = PTR_System_Collections_Generic_List_BspContents__TypeInfo_01fc7a60;
  if ((DAT_021008e1 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_BspContents___ctor_01fc7a68);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_BspContents__TypeInfo_01fc7a60);
    DAT_021008e1 = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Method_System_Collections_Generic_List_object___ctor(uVar3,*(undefined8 *)puVar2);
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspRange___ctor
// Address: 017d31bc
// ==========================================================================================

void kfw_bsp_BspRange___ctor
               (undefined4 *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  *param_1 = param_2;
  param_1[1] = param_3;
  param_1[2] = param_4;
  param_1[3] = param_5;
  return;
}



// ==========================================================================================
// Function: kfw_bsp_BspRange__Equals
// Address: 017d31c8
// ==========================================================================================

bool kfw_bsp_BspRange__Equals(int *param_1,undefined8 param_2,undefined8 param_3)

{
  if (((*param_1 == (int)param_2) && (param_1[1] == (int)((ulong)param_2 >> 0x20))) &&
     (param_1[2] == (int)param_3)) {
    return param_1[3] == (int)((ulong)param_3 >> 0x20);
  }
  return false;
}



// ==========================================================================================
