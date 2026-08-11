// Function: surface_GamePad___ctor
// Address: 00ef13c0
// ==========================================================================================

void surface_GamePad___ctor(long param_1)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  int iVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  float fVar9;
  
  puVar4 = PTR_float___TypeInfo_01fc0858;
  puVar2 = PTR_kairo_unity_surface_SurfaceBase_TypeInfo_01fbf4c8;
  if ((DAT_020ff71b & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660);
    FUN_00db0bbc(PTR_float___TypeInfo_01fc0858);
    FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceBase_TypeInfo_01fbf4c8);
    DAT_020ff71b = 1;
  }
  *(undefined4 *)(param_1 + 0x16c) = 2;
  puVar3 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  uVar6 = FUN_00db0c30(*(undefined8 *)puVar4,3);
  *(undefined8 *)(param_1 + 0x180) = uVar6;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_surface_SurfaceBase___ctor(param_1,0);
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  lVar7 = *(long *)puVar3;
  if (*(int *)(lVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar7 = *(long *)puVar3;
  }
  *(undefined8 *)(param_1 + 0x128) = **(undefined8 **)(lVar7 + 0xb8);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_ui_Canvas__GetInstance(0);
  *(undefined8 *)(param_1 + 0x130) = uVar6;
  uVar6 = surface_TouchEffectManager__GetInstance(0);
  *(undefined8 *)(param_1 + 0x138) = uVar6;
  puVar2 = PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70;
  if (*(long *)(param_1 + 0x128) != 0) {
    fVar9 = (float)kairo_unity_ui_IApplication__GetScaleRatio(*(long *)(param_1 + 0x128),1,0);
    *(float *)(param_1 + 0xc4) = (((fVar9 * 240.0) / 100.0) * 100.0) / 320.0;
    lVar7 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    kairo_unity_ui_Font___ctor(lVar7,0);
    *(long *)(param_1 + 0x140) = lVar7;
    puVar2 = PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660;
    if (lVar7 != 0) {
      kairo_unity_ui_Font__SetSize(lVar7,0xe,1,0);
      *(undefined4 *)(param_1 + 0x178) = 1;
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar6 = kairo_unity_native_KairoPlugin__GetReleaseNumber(0);
      uVar6 = java_lang_StringEx__SubstringJ(uVar6,0,1,0);
      iVar5 = java_lang_JInteger__ParseInt(uVar6,0);
      puVar2 = PTR_surface_GamePad_TypeInfo_01fc0860;
      if (iVar5 != 3) {
        return;
      }
      lVar7 = *(long *)PTR_surface_GamePad_TypeInfo_01fc0860;
      if (*(int *)(lVar7 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar7 = *(long *)puVar2;
      }
      lVar7 = *(long *)(*(long *)(lVar7 + 0xb8) + 0x28);
      if (lVar7 != 0) {
        uVar1 = *(uint *)(lVar7 + 0x18);
        if (8 < uVar1) {
          lVar8 = *(long *)(lVar7 + 0x60);
          if (lVar8 == 0) goto LAB_00ef1640;
          if ((*(int *)(lVar8 + 0x18) != 0) && (*(undefined4 *)(lVar8 + 0x20) = 0, 9 < uVar1)) {
            lVar7 = *(long *)(lVar7 + 0x68);
            if (lVar7 == 0) goto LAB_00ef1640;
            if (1 < *(uint *)(lVar7 + 0x18)) {
              *(undefined4 *)(lVar7 + 0x24) = 0;
              return;
            }
          }
        }
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
    }
  }
LAB_00ef1640:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__Load
// Address: 00ef1648
// ==========================================================================================

void surface_GamePad__Load(long param_1)

{
  int iVar1;
  uint uVar2;
  undefined *puVar3;
  undefined *puVar4;
  long lVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  ulong uVar10;
  long *plVar11;
  
  puVar4 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff71c & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_Image___TypeInfo_01fc0248);
    FUN_00db0bbc(PTR_kairo_unity_ui_Image_TypeInfo_01fbf500);
    DAT_020ff71c = 1;
  }
  lVar5 = *(long *)puVar4;
  if (*(int *)(lVar5 + 0xe0) == 0) {
                    /* try { // try from 00ef16a8 to 00ef16ab has its CatchHandler @ 00ef1904 */
    thunk_FUN_00df405c();
    lVar5 = *(long *)puVar4;
  }
  lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x10);
  if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18dc to 00ef18df has its CatchHandler @ 00ef190c */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef16cc to 00ef16cf has its CatchHandler @ 00ef1908 */
  uVar6 = FUN_00db0c30(*(undefined8 *)PTR_kairo_unity_ui_Image___TypeInfo_01fc0248,
                       *(undefined4 *)(lVar5 + 0x18));
  puVar3 = PTR_kairo_unity_ui_Image_TypeInfo_01fbf500;
  lVar7 = *(long *)puVar4;
  lVar5 = 4;
  *(undefined8 *)(*(long *)(lVar7 + 0xb8) + 8) = uVar6;
  do {
    if (*(int *)(lVar7 + 0xe0) == 0) {
                    /* try { // try from 00ef16f0 to 00ef16f7 has its CatchHandler @ 00ef191c */
      thunk_FUN_00df405c(lVar7);
      lVar7 = *(long *)puVar4;
    }
    lVar8 = *(long *)(lVar7 + 0xb8);
    lVar9 = *(long *)(lVar8 + 8);
    if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18b0 to 00ef18b3 has its CatchHandler @ 00ef1938 */
      FUN_00db0de4();
    }
    uVar10 = lVar5 - 4;
    if ((long)*(int *)(lVar9 + 0x18) <= (long)uVar10) {
      if (*(int *)(lVar7 + 0xe0) == 0) {
                    /* try { // try from 00ef1808 to 00ef187b has its CatchHandler @ 00ef1904 */
        thunk_FUN_00df405c(lVar7);
        lVar7 = *(long *)puVar4;
        lVar8 = *(long *)(lVar7 + 0xb8);
        lVar9 = *(long *)(lVar8 + 8);
        if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18e8 to 00ef18eb has its CatchHandler @ 00ef18fc */
          FUN_00db0de4();
        }
      }
      if (*(int *)(lVar9 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18e0 to 00ef18e7 has its CatchHandler @ 00ef1910 */
        FUN_00db0dec();
      }
      if (*(long *)(lVar9 + 0x20) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      iVar1 = *(int *)(*(long *)(lVar9 + 0x20) + 0x28);
      uVar2 = iVar1 - 0x180U >> 6;
      if ((6 < (uVar2 | iVar1 << 0x1a)) || ((1 << (ulong)(uVar2 & 0x1f) & 0x4dU) == 0)) {
        if (*(int *)(lVar7 + 0xe0) == 0) {
          thunk_FUN_00df405c(lVar7);
          lVar8 = *(long *)(*(long *)puVar4 + 0xb8);
        }
        lVar5 = *(long *)(lVar8 + 0x18);
        if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18ec to 00ef18f3 has its CatchHandler @ 00ef1900 */
          FUN_00db0de4();
        }
        if (*(int *)(lVar5 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        *(undefined4 *)(lVar5 + 0x20) = 0x1e4;
        if (*(int *)(lVar5 + 0x18) == 1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18f4 to 00ef18f7 has its CatchHandler @ 00ef18f8 */
          FUN_00db0dec();
        }
        *(undefined4 *)(lVar5 + 0x24) = 0x195;
      }
      return;
    }
    if (*(int *)(lVar7 + 0xe0) == 0) {
                    /* try { // try from 00ef1720 to 00ef1727 has its CatchHandler @ 00ef1918 */
      thunk_FUN_00df405c(lVar7);
      lVar8 = *(long *)(*(long *)puVar4 + 0xb8);
    }
    lVar7 = *(long *)(lVar8 + 0x10);
    if (lVar7 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18b8 to 00ef18bb has its CatchHandler @ 00ef1930 */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar7 + 0x18) <= uVar10) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18b4 to 00ef18b7 has its CatchHandler @ 00ef1940 */
      FUN_00db0dec();
    }
    if (param_1 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18bc to 00ef18bf has its CatchHandler @ 00ef1940 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef174c to 00ef1757 has its CatchHandler @ 00ef192c */
    lVar7 = kairo_unity_util_JarInflater__GetSize(param_1,*(undefined8 *)(lVar7 + lVar5 * 8),0);
    if (lVar7 != -1) {
      lVar7 = *(long *)puVar4;
      if (*(int *)(lVar7 + 0xe0) == 0) {
                    /* try { // try from 00ef176c to 00ef176f has its CatchHandler @ 00ef1914 */
        thunk_FUN_00df405c();
        lVar7 = *(long *)puVar4;
      }
      lVar8 = *(long *)(*(long *)(lVar7 + 0xb8) + 0x10);
      if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18c4 to 00ef18c7 has its CatchHandler @ 00ef1924 */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar8 + 0x18) <= uVar10) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18c8 to 00ef18cb has its CatchHandler @ 00ef1920 */
        FUN_00db0dec();
      }
      plVar11 = *(long **)(*(long *)(lVar7 + 0xb8) + 8);
                    /* try { // try from 00ef1794 to 00ef17b3 has its CatchHandler @ 00ef1928 */
      uVar6 = kairo_unity_util_JarInflater__GetData(param_1,*(undefined8 *)(lVar8 + lVar5 * 8),0);
      if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef17b4 to 00ef17e3 has its CatchHandler @ 00ef1934 */
      lVar7 = kairo_unity_ui_Image__Load(uVar6,0xffffffff,0xffffffff,0);
      if (plVar11 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18c0 to 00ef18c3 has its CatchHandler @ 00ef193c */
        FUN_00db0de4();
      }
      if ((lVar7 != 0) &&
         (lVar8 = thunk_FUN_00e11b18(lVar7,*(undefined8 *)(*plVar11 + 0x40)), lVar8 == 0)) {
        uVar6 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar6,0);
      }
      if (*(uint *)(plVar11 + 3) <= uVar10) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef18cc to 00ef18db has its CatchHandler @ 00ef193c */
        FUN_00db0dec();
      }
      plVar11[lVar5] = lVar7;
    }
    lVar7 = *(long *)puVar4;
    lVar5 = lVar5 + 1;
  } while( true );
}



// ==========================================================================================
// Function: surface_GamePad__GetInstance
// Address: 00ef19bc
// ==========================================================================================

undefined8 surface_GamePad__GetInstance(void)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff71d & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    DAT_020ff71d = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) == 0) {
    uVar3 = thunk_FUN_00e11c14();
    surface_GamePad___ctor();
    lVar2 = *(long *)puVar1;
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    **(undefined8 **)(lVar2 + 0xb8) = uVar3;
    lVar2 = *(long *)puVar1;
  }
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return **(undefined8 **)(lVar2 + 0xb8);
}



// ==========================================================================================
// Function: surface_GamePad__GetMode
// Address: 00ef1a5c
// ==========================================================================================

undefined4 surface_GamePad__GetMode(long param_1)

{
  return *(undefined4 *)(param_1 + 0x178);
}



// ==========================================================================================
// Function: surface_GamePad__SetMode
// Address: 00ef1a64
// ==========================================================================================

void surface_GamePad__SetMode(long param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x178) = param_2;
  return;
}



// ==========================================================================================
// Function: surface_GamePad__IsGameSurface
// Address: 00ef1a6c
// ==========================================================================================

undefined8 surface_GamePad__IsGameSurface(void)

{
  return 0;
}



// ==========================================================================================
// Function: surface_GamePad__AddTouch
// Address: 00ef1a74
// ==========================================================================================

void surface_GamePad__AddTouch(void)

{
  surface_GamePad__AddTouch();
  return;
}



// ==========================================================================================
// Function: surface_GamePad__AddTouch
// Address: 00ef1a84
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00ef2684) */

void surface_GamePad__AddTouch
               (float param_1,float param_2,long param_3,long param_4,uint param_5,
               undefined4 param_6,uint param_7,int param_8)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined *puVar9;
  undefined *puVar10;
  uint uVar11;
  long lVar12;
  ulong uVar13;
  long lVar14;
  long lVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  long *plVar18;
  long lVar19;
  undefined4 uVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  int local_c0;
  int iStack_bc;
  undefined auStack_a8 [20];
  int local_94;
  
  puVar9 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff71e & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
    FUN_00db0bbc(PTR_StringLiteral_7254_01fc0868);
    FUN_00db0bbc(PTR_StringLiteral_7811_01fc0870);
    FUN_00db0bbc(PTR_StringLiteral_7301_01fc0878);
    FUN_00db0bbc(PTR_StringLiteral_9091_01fc0880);
    FUN_00db0bbc(PTR_StringLiteral_8728_01fc0888);
    FUN_00db0bbc(PTR_StringLiteral_8696_01fc0890);
    FUN_00db0bbc(PTR_StringLiteral_8194_01fc0898);
    FUN_00db0bbc(PTR_StringLiteral_6963_01fc08a0);
    FUN_00db0bbc(PTR_StringLiteral_154_01fc08a8);
    FUN_00db0bbc(PTR_StringLiteral_7822_01fc08b0);
    FUN_00db0bbc(PTR_StringLiteral_9082_01fc08b8);
    DAT_020ff71e = 1;
  }
  lVar12 = *(long *)puVar9;
  local_94 = 0;
  if (*(int *)(lVar12 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar12 = *(long *)puVar9;
  }
  lVar19 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x28);
  if (lVar19 == 0) {
LAB_00ef267c:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar19 + 0x18) <= param_5) {
LAB_00ef2680:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
  lVar19 = *(long *)(lVar19 + (long)(int)param_5 * 8 + 0x20);
  if (lVar19 == 0) goto LAB_00ef267c;
  if (*(uint *)(lVar19 + 0x18) < 5) goto LAB_00ef2680;
  lVar12 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
  if (lVar12 == 0) goto LAB_00ef267c;
  uVar11 = *(uint *)(lVar19 + 0x30);
  if (*(uint *)(lVar12 + 0x18) <= uVar11) goto LAB_00ef2680;
  if (param_4 == 0) {
    if ((param_7 & 1) == 0) {
      return;
    }
    local_c0 = 0;
    iStack_bc = 0;
    goto LAB_00ef1c94;
  }
  lVar12 = *(long *)(lVar12 + (long)(int)uVar11 * 8 + 0x20);
  iStack_bc = kairo_unity_ui_Graphics__GetOriginX(param_4,0);
  local_c0 = kairo_unity_ui_Graphics__GetOriginY(param_4,0);
  fVar21 = (float)iStack_bc;
  fVar23 = (float)local_c0;
  param_1 = fVar21 + param_1;
  param_2 = fVar23 + param_2;
  kairo_unity_ui_Graphics__SetOrigin(0,0,param_4,0);
                    /* try { // try from 00ef1c60 to 00ef1c7f has its CatchHandler @ 00ef288c */
  uVar13 = surface_GamePad__DrawMiniSoftLabel
                     (param_1,param_2,param_3,param_4,param_5,param_6,param_7 & 1);
  if ((uVar13 & 1) != 0) goto LAB_00ef2070;
  if (param_5 - 6 < 5) {
    if ((param_7 & 1) != 0) {
                    /* try { // try from 00ef2014 to 00ef2023 has its CatchHandler @ 00ef282c */
      uVar13 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_3,param_5,0);
      if ((uVar13 & 1) != 0) {
        if (*(uint *)(lVar19 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26ec to 00ef26ef has its CatchHandler @ 00ef27d8 */
          FUN_00db0dec();
        }
        if (*(int *)(lVar19 + 0x34) != -1) {
                    /* try { // try from 00ef2040 to 00ef2053 has its CatchHandler @ 00ef27b8 */
          surface_GamePad__DrawImage(param_1,param_2,param_3,param_4);
        }
      }
      goto LAB_00ef1c94;
    }
    goto LAB_00ef2070;
  }
  if ((param_7 & 1) == 0) {
    if ((param_5 != 4) || (*(int *)(param_3 + 0x178) != 0)) {
      if (*(uint *)(lVar19 + 0x18) < 7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26cc to 00ef26cf has its CatchHandler @ 00ef2820 */
        FUN_00db0dec();
      }
      if (*(int *)(lVar19 + 0x38) != -1) {
        if (param_5 == 4) {
          if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef270c to 00ef270f has its CatchHandler @ 00ef27a4 */
            FUN_00db0de4();
          }
                    /* try { // try from 00ef224c to 00ef2257 has its CatchHandler @ 00ef2798 */
          lVar12 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),2,0);
          if (lVar12 == 0) {
            if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2734 to 00ef2737 has its CatchHandler @ 00ef2750 */
              FUN_00db0de4();
            }
                    /* try { // try from 00ef2268 to 00ef2273 has its CatchHandler @ 00ef274c */
            lVar12 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),3,0);
            goto LAB_00ef2274;
          }
        }
        else {
          if (param_5 == 3) {
            if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2708 to 00ef270b has its CatchHandler @ 00ef27a8 */
              FUN_00db0de4();
            }
                    /* try { // try from 00ef2230 to 00ef223b has its CatchHandler @ 00ef279c */
            lVar12 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),3,0);
          }
          else {
            if (param_5 != 2) goto LAB_00ef2278;
            if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2710 to 00ef2713 has its CatchHandler @ 00ef27a0 */
              FUN_00db0de4();
            }
                    /* try { // try from 00ef220c to 00ef2217 has its CatchHandler @ 00ef2794 */
            lVar12 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),2,0);
          }
LAB_00ef2274:
          if (lVar12 == 0) goto LAB_00ef2070;
        }
LAB_00ef2278:
        if (*(uint *)(lVar19 + 0x18) < 7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26f4 to 00ef26f7 has its CatchHandler @ 00ef281c */
          FUN_00db0dec();
        }
                    /* try { // try from 00ef2288 to 00ef229b has its CatchHandler @ 00ef281c */
        surface_GamePad__DrawImage(param_1,param_2,param_3,param_4,*(undefined4 *)(lVar19 + 0x38));
      }
    }
    goto LAB_00ef2070;
  }
                    /* try { // try from 00ef20b8 to 00ef20d3 has its CatchHandler @ 00ef2828 */
  surface_GamePad__DrawImage(param_1,param_2,param_3,param_4,uVar11);
                    /* try { // try from 00ef20d4 to 00ef20e3 has its CatchHandler @ 00ef2824 */
  uVar13 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_3,param_5,0);
  if ((uVar13 & 1) != 0) {
    if (*(uint *)(lVar19 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26f0 to 00ef26f3 has its CatchHandler @ 00ef27d4 */
      FUN_00db0dec();
    }
    if (*(int *)(lVar19 + 0x34) != -1) {
                    /* try { // try from 00ef2100 to 00ef2113 has its CatchHandler @ 00ef27b4 */
      surface_GamePad__DrawImage(param_1,param_2,param_3,param_4);
    }
  }
  lVar14 = 0;
  switch(param_5) {
  case 0:
  case 5:
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2714 to 00ef2717 has its CatchHandler @ 00ef2790 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef2148 to 00ef214f has its CatchHandler @ 00ef2788 */
    lVar14 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_3 + 0x130),0);
  default:
    puVar10 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    if (param_5 == 0x15) {
      if (*(int *)(*(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338 + 0xe0) == 0) {
                    /* try { // try from 00ef2638 to 00ef263b has its CatchHandler @ 00ef2744 */
        thunk_FUN_00df405c();
      }
      if (param_3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2730 to 00ef2733 has its CatchHandler @ 00ef2780 */
        FUN_00db0de4();
      }
      fVar21 = 27.0;
      if (*(char *)(*(long *)(*(long *)puVar10 + 0xb8) + 0x10) != '\0') {
        fVar21 = 22.0;
      }
                    /* try { // try from 00ef266c to 00ef2677 has its CatchHandler @ 00ef2780 */
      surface_GamePad__DrawImage(param_1 + fVar21,param_2 + 4.0,param_3,param_4,0x13);
    }
    else if (param_5 == 0x16) {
      if (*(int *)(*(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338 + 0xe0) == 0) {
                    /* try { // try from 00ef2178 to 00ef217b has its CatchHandler @ 00ef2748 */
        thunk_FUN_00df405c();
      }
      if (param_3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef272c to 00ef272f has its CatchHandler @ 00ef2784 */
        FUN_00db0de4();
      }
      fVar21 = 27.0;
      if (*(char *)(*(long *)(*(long *)puVar10 + 0xb8) + 0x10) != '\0') {
        fVar21 = 22.0;
      }
                    /* try { // try from 00ef21ac to 00ef21b7 has its CatchHandler @ 00ef2784 */
      surface_GamePad__DrawImage(param_1 + fVar21,param_2 + 4.0,param_3,param_4,0x14);
    }
    goto LAB_00ef2408;
  case 1:
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2718 to 00ef271b has its CatchHandler @ 00ef277c */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef22e4 to 00ef22eb has its CatchHandler @ 00ef2768 */
    lVar14 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_3 + 0x130),0);
    goto LAB_00ef2408;
  case 2:
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2724 to 00ef2727 has its CatchHandler @ 00ef276c */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef23ac to 00ef23b7 has its CatchHandler @ 00ef2758 */
    lVar14 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),2,0);
    goto LAB_00ef2408;
  case 3:
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef271c to 00ef271f has its CatchHandler @ 00ef2778 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef22fc to 00ef2307 has its CatchHandler @ 00ef2764 */
    lVar14 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),3,0);
    goto LAB_00ef2408;
  case 4:
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2720 to 00ef2723 has its CatchHandler @ 00ef2770 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef2324 to 00ef232f has its CatchHandler @ 00ef2760 */
    lVar14 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),2,0);
    if (lVar14 == 0) {
      if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2738 to 00ef273b has its CatchHandler @ 00ef2740 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef2344 to 00ef234f has its CatchHandler @ 00ef273c */
      lVar14 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_3 + 0x130),3,0);
      goto LAB_00ef2408;
    }
    goto LAB_00ef240c;
  case 0xb:
    plVar18 = (long *)PTR_StringLiteral_7254_01fc0868;
    break;
  case 0xc:
    plVar18 = (long *)PTR_StringLiteral_9082_01fc08b8;
    break;
  case 0xd:
    plVar18 = (long *)PTR_StringLiteral_7301_01fc0878;
    break;
  case 0xe:
    plVar18 = (long *)PTR_StringLiteral_7822_01fc08b0;
    break;
  case 0xf:
    plVar18 = (long *)PTR_StringLiteral_9091_01fc0880;
    break;
  case 0x10:
    local_94 = *(int *)(param_3 + 0x168) + 1;
                    /* try { // try from 00ef2364 to 00ef236f has its CatchHandler @ 00ef2774 */
    uVar17 = System_Int32__ToString(&local_94,0);
                    /* try { // try from 00ef2378 to 00ef237f has its CatchHandler @ 00ef275c */
    uVar16 = System_Int32__ToString(param_3 + 0x16c,0);
                    /* try { // try from 00ef2390 to 00ef239b has its CatchHandler @ 00ef2754 */
    lVar14 = System_String__Concat(uVar17,*(undefined8 *)PTR_StringLiteral_154_01fc08a8,uVar16,0);
    goto LAB_00ef2408;
  case 0x11:
    plVar18 = (long *)PTR_StringLiteral_8194_01fc0898;
    break;
  case 0x12:
                    /* try { // try from 00ef22a0 to 00ef22a7 has its CatchHandler @ 00ef278c */
    lVar14 = form_FormManager__GetInstance(0);
    if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2728 to 00ef272b has its CatchHandler @ 00ef278c */
      FUN_00db0de4();
    }
    plVar18 = (long *)PTR_StringLiteral_8696_01fc0890;
    if (*(char *)(lVar14 + 0x32) != '\0') {
      plVar18 = (long *)PTR_StringLiteral_8728_01fc0888;
    }
    break;
  case 0x13:
    plVar18 = (long *)PTR_StringLiteral_6963_01fc08a0;
    break;
  case 0x14:
    plVar18 = (long *)PTR_StringLiteral_7811_01fc0870;
  }
  lVar14 = *plVar18;
LAB_00ef2408:
  if (lVar14 != 0) {
LAB_00ef240c:
    if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26d8 to 00ef26db has its CatchHandler @ 00ef2810 */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar12 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26dc to 00ef26df has its CatchHandler @ 00ef280c */
      FUN_00db0dec();
    }
    if (*(uint *)(lVar12 + 0x18) == 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26e0 to 00ef26e3 has its CatchHandler @ 00ef2808 */
      FUN_00db0dec();
    }
    fVar23 = param_1 + (float)(*(int *)(lVar12 + 0x24) + *(int *)(lVar12 + 0x34)) * 0.5 + -1.0;
    fVar21 = param_2 + (float)(*(int *)(lVar12 + 0x28) + *(int *)(lVar12 + 0x38)) * 0.5 + -1.0;
    if (param_5 == 5) {
      if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26f8 to 00ef26fb has its CatchHandler @ 00ef27d0 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef2470 to 00ef2477 has its CatchHandler @ 00ef27cc */
      uVar11 = kairo_unity_ui_Canvas__IsLinearFilterEnable(*(long *)(param_3 + 0x130),0);
      if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26fc to 00ef26ff has its CatchHandler @ 00ef2804 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef2488 to 00ef2493 has its CatchHandler @ 00ef2804 */
      kairo_unity_ui_Canvas__SetLinearFilterEnable(*(long *)(param_3 + 0x130),1,0);
                    /* try { // try from 00ef2494 to 00ef249b has its CatchHandler @ 00ef27c8 */
      lVar12 = java_lang_JSystem__CurrentTimeMillis(0);
      uVar20 = 0xf;
      if (399 < lVar12 % 800) {
        uVar20 = 0x10;
      }
                    /* try { // try from 00ef24e0 to 00ef24eb has its CatchHandler @ 00ef287c */
      surface_GamePad__DrawImage(fVar23 + -27.0,fVar21 + -10.0,param_3,param_4,uVar20);
      if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2704 to 00ef2707 has its CatchHandler @ 00ef27f8 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef24f8 to 00ef2503 has its CatchHandler @ 00ef27f8 */
      kairo_unity_ui_Canvas__SetLinearFilterEnable(*(long *)(param_3 + 0x130),uVar11 & 1,0);
      fVar23 = fVar23 + 12.0;
    }
    if (*(uint *)(lVar19 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26e4 to 00ef26e7 has its CatchHandler @ 00ef2800 */
      FUN_00db0dec();
    }
    if (*(int *)(lVar19 + 0x30) == 7) {
                    /* try { // try from 00ef2524 to 00ef2533 has its CatchHandler @ 00ef27c4 */
      lVar12 = kairo_unity_ui_Graphics__GetFont(param_4,0,0);
      if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2700 to 00ef2703 has its CatchHandler @ 00ef27fc */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef253c to 00ef254f has its CatchHandler @ 00ef27fc */
      kairo_unity_ui_Font__SetSize(lVar12,8,1,0);
                    /* try { // try from 00ef2550 to 00ef255f has its CatchHandler @ 00ef27c0 */
      kairo_unity_ui_Graphics__PushFont(param_4,lVar12,0);
    }
                    /* try { // try from 00ef2560 to 00ef2577 has its CatchHandler @ 00ef27f4 */
    kairo_unity_ui_Graphics__SetColor(param_4,0,0,0,0);
    if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
                    /* try { // try from 00ef258c to 00ef258f has its CatchHandler @ 00ef27b0 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef2590 to 00ef259b has its CatchHandler @ 00ef27f0 */
    uVar17 = kairo_unity_util_Language__TranslateSoftLabel(lVar14,0);
    uVar20 = *(undefined4 *)(param_4 + 0x58);
    if (*(int *)(*(long *)PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598 + 0xe0) == 0) {
                    /* try { // try from 00ef25b8 to 00ef25bb has its CatchHandler @ 00ef27ac */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef25cc to 00ef25fb has its CatchHandler @ 00ef27ec */
    kairo_unity_ui_TextLayout__Draw
              (auStack_a8,fVar23 + -30.0,fVar21 + -15.0,0x42700000,0x41f00000,param_4,uVar17,uVar20,
               0,0x22,0,0);
    if (*(uint *)(lVar19 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26e8 to 00ef26eb has its CatchHandler @ 00ef27e8 */
      FUN_00db0dec();
    }
    if (*(int *)(lVar19 + 0x30) == 7) {
                    /* try { // try from 00ef2614 to 00ef261f has its CatchHandler @ 00ef27bc */
      kairo_unity_ui_Graphics__PopFont(param_4,0);
    }
  }
LAB_00ef1c94:
  uVar11 = (uint)*(undefined8 *)(lVar19 + 0x18);
  if (uVar11 < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef268c to 00ef268f has its CatchHandler @ 00ef2880 */
    FUN_00db0dec();
  }
  if (*(int *)(lVar19 + 0x34) != -1) {
    lVar12 = *(long *)puVar9;
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef1cb8 to 00ef1d47 has its CatchHandler @ 00ef287c */
      thunk_FUN_00df405c();
      lVar12 = *(long *)puVar9;
      uVar11 = (uint)*(undefined8 *)(lVar19 + 0x18);
    }
    if (uVar11 < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2690 to 00ef2697 has its CatchHandler @ 00ef2888 */
      FUN_00db0dec();
    }
    lVar12 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
    if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar12 + 0x18) <= *(uint *)(lVar19 + 0x34)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef2698 to 00ef269b has its CatchHandler @ 00ef2878 */
      FUN_00db0dec();
    }
    lVar12 = *(long *)(lVar12 + (long)(int)*(uint *)(lVar19 + 0x34) * 8 + 0x20);
    if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef269c to 00ef269f has its CatchHandler @ 00ef2874 */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar12 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26a0 to 00ef26a3 has its CatchHandler @ 00ef2870 */
      FUN_00db0dec();
    }
    if (*(uint *)(lVar12 + 0x18) == 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26a4 to 00ef26a7 has its CatchHandler @ 00ef286c */
      FUN_00db0dec();
    }
    iVar1 = *(int *)(lVar19 + 0x20);
    iVar5 = *(int *)(lVar19 + 0x24);
    iVar2 = *(int *)(lVar12 + 0x34);
    iVar6 = *(int *)(lVar12 + 0x38);
    iVar3 = *(int *)(lVar19 + 0x28);
    iVar7 = *(int *)(lVar19 + 0x2c);
    iVar4 = *(int *)(lVar12 + 0x24);
    iVar8 = *(int *)(lVar12 + 0x28);
    if ((param_5 - 6 < 4) || (param_5 == 0xd)) {
      if (*(int *)(*(long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef1d48 to 00ef1d53 has its CatchHandler @ 00ef2850 */
      lVar12 = kairo_unity_surface_TouchOption__Create(1,0);
    }
    else {
      lVar12 = 0;
    }
    if ((param_5 == 0xc) && (*(int *)(param_3 + 0x178) == 0)) {
      if (*(int *)(*(long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888 + 0xe0) == 0) {
                    /* try { // try from 00ef1d80 to 00ef1d83 has its CatchHandler @ 00ef287c */
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef1d84 to 00ef1d8f has its CatchHandler @ 00ef27e4 */
      lVar12 = kairo_unity_surface_TouchOption__Create(1,0);
    }
    if (lVar12 == 0) {
      if (*(int *)(*(long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888 + 0xe0) == 0) {
                    /* try { // try from 00ef1dac to 00ef1daf has its CatchHandler @ 00ef287c */
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef1db0 to 00ef1db7 has its CatchHandler @ 00ef2830 */
      lVar12 = kairo_unity_surface_TouchOption__Create(0);
    }
    if (*(int *)(param_3 + 0x178) != 2) {
      if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26b0 to 00ef26b3 has its CatchHandler @ 00ef2848 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef1dd8 to 00ef1de3 has its CatchHandler @ 00ef2844 */
      kairo_unity_surface_TouchOption__Flag(lVar12,*(uint *)(lVar12 + 0x10) | 2,0);
    }
    if (*(long *)(param_3 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26a8 to 00ef26ab has its CatchHandler @ 00ef2868 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef1df0 to 00ef1df7 has its CatchHandler @ 00ef2864 */
    lVar19 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_3 + 0x130),0);
                    /* try { // try from 00ef1dfc to 00ef1e03 has its CatchHandler @ 00ef2884 */
    lVar14 = form_FormManager__GetInstance(0);
    if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26ac to 00ef26af has its CatchHandler @ 00ef2884 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef1e08 to 00ef1e0f has its CatchHandler @ 00ef2860 */
    lVar14 = kairo_unity_form_FormManagerBase__GetTopForm(lVar14,0);
    puVar9 = PTR_main_AppData_TypeInfo_01fbf278;
    fVar24 = (param_1 - (float)iVar1) + (float)iVar4;
    fVar22 = (float)((iVar1 + iVar2 + iVar5) - iVar4);
    fVar23 = (float)((iVar3 + iVar6 + iVar7) - iVar8);
    fVar21 = (param_2 - (float)iVar3) + (float)iVar8;
    if ((param_5 == 1) && (*(int *)(param_3 + 0x178) == 2)) {
      lVar15 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
      if (*(int *)(lVar15 + 0xe0) == 0) {
                    /* try { // try from 00ef1e88 to 00ef1e8b has its CatchHandler @ 00ef27e0 */
        thunk_FUN_00df405c();
        lVar15 = *(long *)puVar9;
      }
      lVar15 = *(long *)(*(long *)(lVar15 + 0xb8) + 0x60);
      if (lVar15 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26b4 to 00ef26b7 has its CatchHandler @ 00ef2840 */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar15 + 0x18) < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26b8 to 00ef26bf has its CatchHandler @ 00ef285c */
        FUN_00db0dec();
      }
      if (lVar19 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef1eb0 to 00ef1ebb has its CatchHandler @ 00ef2838 */
      uVar13 = System_String__Equals(lVar19,*(undefined8 *)(lVar15 + 0x38),0);
      if ((uVar13 & 1) != 0) {
        if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26d0 to 00ef26d3 has its CatchHandler @ 00ef2818 */
          FUN_00db0de4();
        }
        if (*(int *)(lVar14 + 0x10) - 3U < 2) {
          fVar24 = fVar24 + -10.0;
          fVar22 = fVar22 + 10.0;
          fVar21 = fVar21 + -30.0;
          fVar23 = fVar23 + 30.0;
        }
      }
    }
    puVar9 = PTR_main_AppData_TypeInfo_01fbf278;
    if (param_5 == 1) {
      lVar15 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
      if (*(int *)(lVar15 + 0xe0) == 0) {
                    /* try { // try from 00ef1f10 to 00ef1f13 has its CatchHandler @ 00ef27dc */
        thunk_FUN_00df405c();
        lVar15 = *(long *)puVar9;
      }
      lVar15 = *(long *)(*(long *)(lVar15 + 0xb8) + 0x60);
      if (lVar15 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26c0 to 00ef26c3 has its CatchHandler @ 00ef283c */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar15 + 0x18) < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26c4 to 00ef26cb has its CatchHandler @ 00ef2858 */
        FUN_00db0dec();
      }
      if (lVar19 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef1f38 to 00ef1f43 has its CatchHandler @ 00ef2834 */
      uVar13 = System_String__Equals(lVar19,*(undefined8 *)(lVar15 + 0x38),0);
      if ((uVar13 & 1) != 0) {
        if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef26d4 to 00ef26d7 has its CatchHandler @ 00ef2814 */
          FUN_00db0de4();
        }
        if (*(int *)(lVar14 + 0x10) == 5) {
          fVar24 = fVar24 + 30.0;
          fVar22 = fVar22 + -30.0;
        }
      }
    }
    fVar23 = fVar23 - (float)param_8;
    fVar21 = fVar21 + (float)param_8;
    iVar1 = -0x80000000;
    if (fVar24 != INFINITY) {
      iVar1 = (int)fVar24;
    }
    iVar2 = -0x80000000;
    if (fVar21 != INFINITY) {
      iVar2 = (int)fVar21;
    }
    iVar3 = -0x80000000;
    if (fVar22 != INFINITY) {
      iVar3 = (int)fVar22;
    }
    iVar4 = -0x80000000;
    if (fVar23 != INFINITY) {
      iVar4 = (int)fVar23;
    }
                    /* try { // try from 00ef1fb4 to 00ef1fcb has its CatchHandler @ 00ef2854 */
    lVar12 = kairo_unity_surface_SurfaceBase__AddTouchComponent
                       (param_3,param_5,iVar1,iVar2,iVar3,iVar4,param_6,lVar12,0);
    if (lVar12 != 0) {
      iVar1 = -0x80000000;
      if (param_1 != INFINITY) {
        iVar1 = (int)param_1;
      }
      iVar2 = -0x80000000;
      if (param_2 != INFINITY) {
        iVar2 = (int)param_2;
      }
                    /* try { // try from 00ef1ff8 to 00ef1fff has its CatchHandler @ 00ef284c */
      kairo_unity_surface_TouchComponent__SetPaint(lVar12,iVar1,iVar2,0);
    }
  }
  if (param_4 != 0) {
    fVar21 = (float)iStack_bc;
    fVar23 = (float)local_c0;
LAB_00ef2070:
    kairo_unity_ui_Graphics__SetOrigin(fVar21,fVar23,param_4,0);
  }
  return;
}



// ==========================================================================================
// Function: surface_GamePad__AddTouch
// Address: 00ef28f0
// ==========================================================================================

void surface_GamePad__AddTouch(void)

{
  surface_GamePad__AddTouch();
  return;
}



// ==========================================================================================
// Function: surface_GamePad__DrawMiniSoftLabel
// Address: 00ef28fc
// ==========================================================================================

undefined8
surface_GamePad__DrawMiniSoftLabel
          (float param_1,float param_2,long param_3,long param_4,uint param_5,undefined4 param_6,
          ulong param_7)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  uint uVar6;
  long lVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  ulong uVar11;
  long lVar12;
  undefined4 uVar13;
  int iVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  
  if ((DAT_020ff722 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    DAT_020ff722 = 1;
  }
  fVar15 = (float)surface_GamePad__GetSideViewRatio(param_3);
  if (fVar15 <= 0.0) {
    return 0;
  }
  if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar7 = surface_GameView__GetInstance();
  puVar5 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if (lVar7 == 0) goto LAB_00ef302c;
  lVar8 = *(long *)PTR_surface_GamePad_TypeInfo_01fc0860;
  fVar16 = (float)(*(int *)(lVar7 + 0xbc) * 100) / *(float *)(lVar7 + 0xc4) + DAT_005bcfd0;
  fVar15 = -2.147484e+09;
  if (fVar16 != INFINITY) {
    fVar15 = (float)(int)fVar16;
  }
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar8 = *(long *)puVar5;
  }
  lVar7 = *(long *)(*(long *)(lVar8 + 0xb8) + 0x28);
  if (lVar7 == 0) goto LAB_00ef302c;
  if (*(uint *)(lVar7 + 0x18) <= param_5) goto LAB_00ef3030;
  lVar7 = *(long *)(lVar7 + (long)(int)param_5 * 8 + 0x20);
  if (lVar7 == 0) goto LAB_00ef302c;
  if (*(uint *)(lVar7 + 0x18) < 5) goto LAB_00ef3030;
  lVar8 = *(long *)(*(long *)(lVar8 + 0xb8) + 0x20);
  if (lVar8 == 0) goto LAB_00ef302c;
  uVar6 = *(uint *)(lVar7 + 0x30);
  if (*(uint *)(lVar8 + 0x18) <= uVar6) goto LAB_00ef3030;
  uVar9 = 0;
  lVar8 = *(long *)(lVar8 + (long)(int)uVar6 * 8 + 0x20);
  switch(param_5) {
  case 0:
  case 5:
    if (*(long *)(param_3 + 0x130) == 0) goto LAB_00ef302c;
    lVar10 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_3 + 0x130),0);
    break;
  case 1:
    if (*(long *)(param_3 + 0x130) == 0) goto LAB_00ef302c;
    lVar10 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_3 + 0x130),0);
    break;
  case 2:
    lVar10 = *(long *)(param_3 + 0x130);
    if (lVar10 == 0) goto LAB_00ef302c;
    uVar9 = 2;
    goto LAB_00ef2ac4;
  case 3:
    lVar10 = *(long *)(param_3 + 0x130);
    if (lVar10 == 0) goto LAB_00ef302c;
    uVar9 = 3;
LAB_00ef2ac4:
    lVar10 = kairo_unity_ui_Canvas__GetSoftLabel(lVar10,uVar9,0);
    break;
  default:
    goto switchD_00ef2a7c_caseD_4;
  }
  if (lVar10 == 0) {
    return 0;
  }
  fVar16 = (float)surface_GamePad__GetSideViewRatio(param_3);
  if (lVar8 == 0) goto LAB_00ef302c;
  if ((*(uint *)(lVar8 + 0x18) < 6) || (*(uint *)(lVar8 + 0x18) == 6)) goto LAB_00ef3030;
  fVar17 = fVar16 * (float)*(int *)(lVar8 + 0x34);
  fVar19 = fVar16 * (float)*(int *)(lVar8 + 0x38);
  iVar4 = -0x80000000;
  if (fVar17 != INFINITY) {
    iVar4 = (int)fVar17;
  }
  iVar1 = -0x80000000;
  if (fVar19 != INFINITY) {
    iVar1 = (int)fVar19;
  }
  fVar19 = (float)(*(int *)(lVar8 + 0x34) - iVar4) + param_1;
  uVar9 = 0x15;
  fVar17 = param_1;
  if (fVar15 <= param_1) {
    fVar17 = fVar19;
  }
  fVar20 = (float)(*(int *)(lVar8 + 0x38) - iVar1) + param_2;
  fVar18 = -2.0;
  if ((param_5 == 0) || (fVar18 = -2.0, param_5 == 5)) {
LAB_00ef2b74:
    surface_GamePad__DrawMiniSoftLabelImage(fVar17 + fVar18,fVar20 + -3.0,param_3,param_4,uVar9);
  }
  else if (param_5 == 1) {
    uVar9 = 0x16;
    fVar18 = -5.0;
    goto LAB_00ef2b74;
  }
  fVar17 = param_1 + 1.0;
  if (fVar15 <= param_1) {
    fVar17 = fVar19;
  }
  if ((param_7 & 1) == 0) {
    if (*(uint *)(lVar7 + 0x18) < 7) goto LAB_00ef3030;
    if (*(int *)(lVar7 + 0x38) == -1) goto LAB_00ef2bd8;
    surface_GamePad__DrawMiniSoftLabelImage(fVar17,fVar20,param_3,param_4);
  }
  else {
LAB_00ef2bd8:
    surface_GamePad__DrawMiniSoftLabelImage(fVar17,fVar20,param_3,param_4,uVar6);
    uVar11 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_3,param_5,0);
    if ((uVar11 & 1) != 0) {
      if (*(uint *)(lVar7 + 0x18) < 6) goto LAB_00ef3030;
      if (*(int *)(lVar7 + 0x34) != -1) {
        lVar12 = *(long *)puVar5;
        if (*(int *)(lVar12 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          if (*(uint *)(lVar7 + 0x18) < 6) goto LAB_00ef3030;
          lVar12 = *(long *)puVar5;
        }
        lVar12 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
        if (lVar12 == 0) goto LAB_00ef302c;
        if (*(uint *)(lVar12 + 0x18) <= *(uint *)(lVar7 + 0x34)) goto LAB_00ef3030;
        lVar12 = *(long *)(lVar12 + (long)(int)*(uint *)(lVar7 + 0x34) * 8 + 0x20);
        if (lVar12 == 0) goto LAB_00ef302c;
        if ((*(uint *)(lVar12 + 0x18) < 6) || (*(uint *)(lVar12 + 0x18) == 6)) goto LAB_00ef3030;
        fVar19 = fVar16 * (float)*(int *)(lVar12 + 0x34);
        fVar18 = fVar16 * (float)*(int *)(lVar12 + 0x38);
        iVar4 = -0x80000000;
        if (fVar19 != INFINITY) {
          iVar4 = (int)fVar19;
        }
        iVar1 = -0x80000000;
        if (fVar18 != INFINITY) {
          iVar1 = (int)fVar18;
        }
        if (fVar15 <= param_1) {
          param_1 = (float)(*(int *)(lVar12 + 0x34) - iVar4) + param_1;
        }
        surface_GamePad__DrawMiniSoftLabelImage
                  (param_1,(float)(*(int *)(lVar12 + 0x38) - iVar1) + param_2,param_3,param_4);
      }
    }
    if ((*(uint *)(lVar8 + 0x18) < 6) || (*(uint *)(lVar8 + 0x18) == 6)) goto LAB_00ef3030;
    fVar19 = fVar17 + fVar16 * (float)(*(int *)(lVar8 + 0x24) + *(int *)(lVar8 + 0x34)) * 0.5 + -1.0
    ;
    fVar15 = fVar20 + fVar16 * (float)(*(int *)(lVar8 + 0x28) + *(int *)(lVar8 + 0x38)) * 0.5 + -1.0
    ;
    if (param_5 == 5) {
      if (*(long *)(param_3 + 0x130) == 0) goto LAB_00ef302c;
      uVar6 = kairo_unity_ui_Canvas__IsLinearFilterEnable(*(long *)(param_3 + 0x130),0);
      if (*(long *)(param_3 + 0x130) == 0) goto LAB_00ef302c;
      kairo_unity_ui_Canvas__SetLinearFilterEnable(*(long *)(param_3 + 0x130),1,0);
      lVar8 = java_lang_JSystem__CurrentTimeMillis(0);
      uVar13 = 0xf;
      if (399 < lVar8 % 800) {
        uVar13 = 0x10;
      }
      surface_GamePad__DrawMiniSoftLabelImage
                (fVar19 + fVar16 * -27.0,fVar15 + fVar16 * -10.0,param_3,param_4,uVar13);
      if (*(long *)(param_3 + 0x130) == 0) goto LAB_00ef302c;
      kairo_unity_ui_Canvas__SetLinearFilterEnable(*(long *)(param_3 + 0x130),uVar6 & 1,0);
      fVar19 = fVar16 * 12.0 + fVar19;
    }
    if ((param_4 == 0) || (lVar8 = kairo_unity_ui_Graphics__GetFont(param_4,0,0), lVar8 == 0))
    goto LAB_00ef302c;
    fVar18 = fVar16 * (float)*(int *)(lVar8 + 0x10);
    iVar4 = -0x80000000;
    if (fVar18 != INFINITY) {
      iVar4 = (int)fVar18;
    }
    kairo_unity_ui_Graphics__PushFont(param_4,iVar4,0);
    kairo_unity_ui_Graphics__SetColor(param_4,0,0,0,0);
    if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar9 = kairo_unity_util_Language__TranslateSoftLabel(lVar10,0);
    kairo_unity_ui_Graphics__DrawString(fVar19,fVar15,param_4,uVar9,0x22,0);
    kairo_unity_ui_Graphics__PopFont(param_4,0);
    if ((param_7 & 1) != 0) {
      uVar6 = (uint)*(undefined8 *)(lVar7 + 0x18);
      if (uVar6 < 6) {
LAB_00ef3030:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      if (*(int *)(lVar7 + 0x34) != -1) {
        lVar8 = *(long *)puVar5;
        if (*(int *)(lVar8 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar8 = *(long *)puVar5;
          uVar6 = (uint)*(undefined8 *)(lVar7 + 0x18);
        }
        if (uVar6 < 6) goto LAB_00ef3030;
        lVar8 = *(long *)(*(long *)(lVar8 + 0xb8) + 0x20);
        if (lVar8 == 0) {
LAB_00ef302c:
                    /* WARNING: Subroutine does not return */
          FUN_00db0de4();
        }
        if (*(uint *)(lVar8 + 0x18) <= *(uint *)(lVar7 + 0x34)) goto LAB_00ef3030;
        lVar8 = *(long *)(lVar8 + (long)(int)*(uint *)(lVar7 + 0x34) * 8 + 0x20);
        if (lVar8 == 0) goto LAB_00ef302c;
        if ((*(uint *)(lVar8 + 0x18) < 6) || (*(uint *)(lVar8 + 0x18) == 6)) goto LAB_00ef3030;
        fVar15 = (fVar17 - (float)*(int *)(lVar7 + 0x20)) + (float)*(int *)(lVar8 + 0x24);
        fVar19 = (1.0 - fVar16) * (float)*(int *)(lVar8 + 0x38) * 0.5;
        fVar18 = ((fVar20 - (float)*(int *)(lVar7 + 0x28)) + (float)*(int *)(lVar8 + 0x28)) - fVar19
        ;
        fVar16 = fVar16 * (float)((*(int *)(lVar7 + 0x20) + *(int *)(lVar8 + 0x34) +
                                  *(int *)(lVar7 + 0x24)) - *(int *)(lVar8 + 0x24));
        iVar4 = -0x80000000;
        if (fVar15 != INFINITY) {
          iVar4 = (int)fVar15;
        }
        fVar19 = fVar19 + (float)((*(int *)(lVar7 + 0x28) + *(int *)(lVar8 + 0x38) +
                                  *(int *)(lVar7 + 0x2c)) - *(int *)(lVar8 + 0x28));
        iVar1 = -0x80000000;
        if (fVar18 != INFINITY) {
          iVar1 = (int)fVar18;
        }
        iVar14 = -0x80000000;
        iVar2 = iVar14;
        if (fVar16 != INFINITY) {
          iVar2 = (int)fVar16;
        }
        iVar3 = iVar14;
        if (fVar19 != INFINITY) {
          iVar3 = (int)fVar19;
        }
        lVar7 = kairo_unity_surface_SurfaceBase__AddTouchComponent
                          (param_3,param_5,iVar4,iVar1,iVar2,iVar3,param_6,0,0);
        if (lVar7 != 0) {
          iVar4 = iVar14;
          if (fVar17 != INFINITY) {
            iVar4 = (int)fVar17;
          }
          if (fVar20 != INFINITY) {
            iVar14 = (int)fVar20;
          }
          kairo_unity_surface_TouchComponent__SetPaint(lVar7,iVar4,iVar14,0);
        }
      }
    }
  }
  uVar9 = 1;
switchD_00ef2a7c_caseD_4:
  return uVar9;
}



// ==========================================================================================
// Function: surface_GamePad__DrawImage
// Address: 00ef3034
// ==========================================================================================

void surface_GamePad__DrawImage
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
               uint param_5)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  
  puVar1 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff726 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    DAT_020ff726 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar3 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x20);
  if (lVar3 != 0) {
    if (param_5 < *(uint *)(lVar3 + 0x18)) {
      lVar3 = *(long *)(lVar3 + (long)(int)param_5 * 8 + 0x20);
      if (lVar3 == 0) goto LAB_00ef30fc;
      if ((5 < *(uint *)(lVar3 + 0x18)) && (*(uint *)(lVar3 + 0x18) != 6)) {
        surface_GamePad__DrawScaledImage
                  (param_1,param_2,(float)*(int *)(lVar3 + 0x34),(float)*(int *)(lVar3 + 0x38),lVar2
                   ,param_4,param_5);
        return;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ef30fc:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__OnTouchEvent
// Address: 00ef3100
// ==========================================================================================

void surface_GamePad__OnTouchEvent(long param_1,long param_2)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  undefined *puVar4;
  long lVar5;
  ulong uVar6;
  long *plVar7;
  undefined8 uVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  int iVar13;
  int iVar14;
  float fVar15;
  int iVar16;
  
  if ((DAT_020ff71f & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_object___TypeInfo_01fc08c0);
    FUN_00db0bbc(PTR_float___TypeInfo_01fc0858);
    FUN_00db0bbc(PTR_form_SpForm_TypeInfo_01fc08c8);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_1051_01fc08d0);
    DAT_020ff71f = 1;
  }
  if (param_2 == 0) goto LAB_00ef3a40;
  lVar12 = *(long *)(param_2 + 0x40);
  lVar5 = form_FormManager__GetInstance(0);
  puVar4 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(long *)(param_2 + 0x40) == 0) goto LAB_00ef3a40;
  uVar3 = *(uint *)(*(long *)(param_2 + 0x40) + 0x18);
  iVar1 = *(int *)(param_2 + 0x10);
  switch(uVar3) {
  case 5:
    if (iVar1 + -5 == 0) {
      if ((lVar12 == 0) || (*(long *)(param_1 + 0x130) == 0)) goto LAB_00ef3a40;
      kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
    }
    if (lVar5 != 0) {
      lVar9 = kairo_unity_form_FormManagerBase__GetTopForm(lVar5,0);
      switch(iVar1 + -5) {
      case 0:
        goto switchD_00ef34e8_caseD_5;
      case 1:
      case 5:
        *(undefined8 *)(param_1 + 0x150) = 0;
        return;
      case 2:
      case 3:
      case 4:
      case 6:
      case 7:
        return;
      case 8:
        if (*(long *)(param_1 + 0x150) < 1) {
          return;
        }
        uVar6 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,5,0);
        if ((uVar6 & 1) == 0) {
          return;
        }
        if (lVar9 != 0) {
          if (*(int *)(lVar9 + 0x10) != 1) {
            return;
          }
          lVar12 = java_lang_JSystem__CurrentTimeMillis(0);
          if (lVar12 - *(long *)(param_1 + 0x150) < 0x1389) {
            return;
          }
          *(undefined8 *)(param_1 + 0x150) = 0;
          uVar8 = thunk_FUN_00e11c14(*(undefined8 *)PTR_form_SpForm_TypeInfo_01fc08c8);
          form_SpForm___ctor(uVar8,0);
          kairo_unity_form_FormManagerBase__Push(lVar5,uVar8,0);
          return;
        }
        break;
      default:
        if (iVar1 != 0) {
          return;
        }
        uVar8 = java_lang_JSystem__CurrentTimeMillis(0);
        *(undefined8 *)(param_1 + 0x150) = uVar8;
        return;
      }
    }
    goto LAB_00ef3a40;
  case 6:
  case 7:
  case 8:
  case 9:
    if (5 < iVar1) {
      if ((iVar1 != 6) && (iVar1 != 10)) {
        return;
      }
switchD_00ef34e8_caseD_6:
      if (lVar12 == 0) goto LAB_00ef3a40;
LAB_00ef34f0:
      if (*(long *)(param_1 + 0x130) != 0) {
        kairo_unity_ui_Canvas__KeyUp(*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
        return;
      }
      goto LAB_00ef3a40;
    }
    if (iVar1 == 0) {
      if ((lVar12 != 0) && (*(long *)(param_1 + 0x130) != 0)) {
        kairo_unity_ui_Canvas__KeyDown
                  (*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),1,0);
        return;
      }
      goto LAB_00ef3a40;
    }
    if (iVar1 != 5) {
      return;
    }
    break;
  default:
    if (iVar1 != 5) {
      return;
    }
    if ((lVar12 == 0) || (*(long *)(param_1 + 0x130) == 0)) goto LAB_00ef3a40;
    kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
    goto LAB_00ef375c;
  case 0xc:
    switch(iVar1) {
    case 5:
      goto switchD_00ef34e8_caseD_5;
    case 6:
    case 10:
      goto switchD_00ef34e8_caseD_6;
    case 7:
    case 8:
    case 9:
    case 0xb:
    case 0xc:
      goto switchD_00ef34e8_caseD_7;
    case 0xd:
      if ((lVar12 == 0) || (*(long *)(param_1 + 0x130) == 0)) goto LAB_00ef3a40;
      uVar6 = kairo_unity_ui_Canvas__CheckKeyState
                        (*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
      if ((uVar6 & 1) != 0) {
        return;
      }
      uVar8 = 0xc;
LAB_00ef3640:
      uVar6 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,uVar8,0);
      if ((uVar6 & 1) == 0) {
        return;
      }
      break;
    default:
switchD_00ef34e8_caseD_9:
      if (iVar1 != 0) {
        return;
      }
      if (lVar12 == 0) goto LAB_00ef3a40;
    }
    if (*(long *)(param_1 + 0x130) == 0) goto LAB_00ef3a40;
    kairo_unity_ui_Canvas__KeyDown(*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),1,0);
    if (iVar1 != 5) {
      if ((iVar1 != 6) && (iVar1 != 10)) {
        return;
      }
      goto LAB_00ef34f0;
    }
    goto LAB_00ef375c;
  case 0xd:
    switch(iVar1) {
    case 5:
      break;
    case 6:
    case 10:
      goto switchD_00ef34e8_caseD_6;
    case 7:
    case 8:
    case 9:
    case 0xb:
    case 0xc:
      goto switchD_00ef34e8_caseD_7;
    case 0xd:
      if ((lVar12 == 0) || (*(long *)(param_1 + 0x130) == 0)) goto LAB_00ef3a40;
      uVar6 = kairo_unity_ui_Canvas__CheckKeyState
                        (*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
      if ((uVar6 & 1) != 0) {
        return;
      }
      uVar8 = 0xd;
      goto LAB_00ef3640;
    default:
      goto switchD_00ef34e8_caseD_9;
    }
  case 0xe:
    if (iVar1 != 5) {
      return;
    }
    if (param_1 == 0) goto LAB_00ef3a40;
    *(byte *)(param_1 + 0x148) = *(byte *)(param_1 + 0x148) ^ 1;
    break;
  case 0xf:
    switch(iVar1) {
    case 5:
      break;
    case 6:
    case 10:
      goto switchD_00ef34e8_caseD_6;
    case 7:
    case 8:
    case 9:
    case 0xb:
    case 0xc:
      goto switchD_00ef34e8_caseD_7;
    case 0xd:
      if ((lVar12 == 0) || (*(long *)(param_1 + 0x130) == 0)) goto LAB_00ef3a40;
      uVar6 = kairo_unity_ui_Canvas__CheckKeyState
                        (*(long *)(param_1 + 0x130),*(undefined4 *)(lVar12 + 0x2c),0);
      if ((uVar6 & 1) != 0) {
        return;
      }
      uVar8 = 0xf;
      goto LAB_00ef3640;
    default:
      goto switchD_00ef34e8_caseD_9;
    }
  case 0x10:
    if (iVar1 != 5) {
      return;
    }
    iVar16 = *(int *)(param_1 + 0x16c);
    iVar1 = *(int *)(param_1 + 0x168) + 1;
    iVar13 = 0;
    if (iVar16 != 0) {
      iVar13 = iVar1 / iVar16;
    }
    *(int *)(param_1 + 0x168) = iVar1 - iVar13 * iVar16;
    break;
  case 0x11:
    if (iVar1 != 5) {
      return;
    }
    iVar1 = *(int *)(param_1 + 0x170);
    uVar2 = iVar1 + 2;
    if (-1 < iVar1 + 1) {
      uVar2 = iVar1 + 1;
    }
    *(uint *)(param_1 + 0x170) = (iVar1 + 1) - (uVar2 & 0xfffffffe);
    surface_GamePad__SetLayoutMode(param_1);
    break;
  case 0x12:
    if (iVar1 != 5) {
      if (iVar1 != 0) {
        return;
      }
      if (lVar5 != 0) {
        kairo_unity_form_FormManagerBase__SetPause(lVar5,*(char *)(lVar5 + 0x32) == '\0',0);
        lVar5 = surface_TouchEffectManager__GetInstance(0);
        if (lVar5 != 0) {
          surface_TouchEffectManager__Clear(lVar5,0);
          return;
        }
      }
      goto LAB_00ef3a40;
    }
    break;
  case 0x13:
    if (iVar1 != 5) {
      return;
    }
    if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar8 = surface_GameView__GetInstance();
    if (lVar5 == 0) goto LAB_00ef3a40;
    kairo_unity_form_FormManagerBase__Capture(lVar5,uVar8,0,0,0,1,0);
    break;
  case 0x14:
    if (iVar1 != 5) {
      return;
    }
    *(byte *)(param_1 + 0x174) = *(byte *)(param_1 + 0x174) ^ 1;
    break;
  case 0x15:
  case 0x16:
    lVar5 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar4;
    }
    lVar9 = *(long *)(lVar5 + 0xb8);
    if (*(char *)(lVar9 + 0x10) != '\0') {
      if (*(int *)(lVar5 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar9 = *(long *)(*(long *)puVar4 + 0xb8);
      }
      if (*(char *)(lVar9 + 0x11) == '\0') {
        if (5 < iVar1) {
          if (iVar1 == 6) {
            *(undefined8 *)(param_1 + 0x160) = 0;
            return;
          }
          if (iVar1 != 0xd) {
            return;
          }
          if (*(long *)(param_1 + 0x160) < 1) {
            return;
          }
          uVar6 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,uVar3,0);
          if ((uVar6 & 1) == 0) {
            return;
          }
          lVar5 = java_lang_JSystem__CurrentTimeMillis(0);
          if (lVar5 - *(long *)(param_1 + 0x160) < 0x3e9) {
            return;
          }
          *(undefined8 *)(param_1 + 0x160) = 0;
          *(byte *)(param_1 + 0x158) = *(byte *)(param_1 + 0x158) ^ 1;
          kairo_unity_surface_SurfaceBase__ClearTouchComponent(param_1,0);
          return;
        }
        if (iVar1 == 0) {
          uVar8 = java_lang_JSystem__CurrentTimeMillis(0);
          *(undefined8 *)(param_1 + 0x160) = uVar8;
          return;
        }
      }
    }
    if (iVar1 != 5) {
      return;
    }
    if (*(int *)(*(long *)PTR_main_AppData_TypeInfo_01fbf278 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar5 = main_AppData__GetInstance(0);
    *(uint *)(param_1 + 0x178) = (uint)(uVar3 != 0x15);
    if (((lVar5 == 0) || (*(long *)(lVar5 + 0x48) == 0)) ||
       (lVar9 = *(long *)(*(long *)(lVar5 + 0x48) + 0x20), lVar9 == 0)) goto LAB_00ef3a40;
    if (*(uint *)(lVar9 + 0x18) < 0xe) goto LAB_00ef3a44;
    *(uint *)(lVar9 + 0x54) = (uint)(uVar3 != 0x15);
                    /* try { // try from 00ef32ac to 00ef32b3 has its CatchHandler @ 00ef3720 */
    main_AppData__SaveSystem(lVar5,0);
  }
switchD_00ef34e8_caseD_5:
  if (lVar12 != 0) {
LAB_00ef375c:
    puVar4 = PTR_surface_GamePad_TypeInfo_01fc0860;
    if (*(int *)(lVar12 + 0x38) == 0x7fffffff) {
switchD_00ef34e8_caseD_7:
      return;
    }
    lVar5 = *(long *)PTR_surface_GamePad_TypeInfo_01fc0860;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar4;
    }
    lVar9 = *(long *)(lVar5 + 0xb8);
    lVar10 = *(long *)(lVar9 + 0x28);
    if (lVar10 != 0) {
      if (uVar3 < *(uint *)(lVar10 + 0x18)) {
        lVar11 = *(long *)(lVar10 + (long)(int)uVar3 * 8 + 0x20);
        if (lVar11 == 0) goto LAB_00ef3a40;
        if (5 < *(uint *)(lVar11 + 0x18)) {
          if (*(int *)(lVar11 + 0x34) == -1) {
            return;
          }
          if (uVar3 - 0x15 < 2) {
            return;
          }
          if (*(int *)(lVar5 + 0xe0) == 0) {
            thunk_FUN_00df405c();
            lVar9 = *(long *)(*(long *)puVar4 + 0xb8);
            lVar10 = *(long *)(lVar9 + 0x28);
            if (lVar10 == 0) goto LAB_00ef3a40;
          }
          if (uVar3 < *(uint *)(lVar10 + 0x18)) {
            lVar5 = *(long *)(lVar10 + (long)(int)uVar3 * 8 + 0x20);
            if (lVar5 == 0) goto LAB_00ef3a40;
            if (5 < *(uint *)(lVar5 + 0x18)) {
              lVar10 = *(long *)(lVar9 + 0x20);
              if (lVar10 == 0) goto LAB_00ef3a40;
              if (*(uint *)(lVar5 + 0x34) < *(uint *)(lVar10 + 0x18)) {
                lVar5 = *(long *)(lVar10 + (long)(int)*(uint *)(lVar5 + 0x34) * 8 + 0x20);
                if (lVar5 == 0) goto LAB_00ef3a40;
                if (*(int *)(lVar5 + 0x18) != 0) {
                  lVar10 = *(long *)(lVar9 + 8);
                  if (lVar10 == 0) goto LAB_00ef3a40;
                  uVar3 = *(uint *)(lVar5 + 0x20);
                  if (uVar3 < *(uint *)(lVar10 + 0x18)) {
                    lVar10 = *(long *)(lVar10 + (long)(int)uVar3 * 8 + 0x20);
                    if ((lVar10 == 0) || (lVar9 = *(long *)(lVar9 + 0x18), lVar9 == 0))
                    goto LAB_00ef3a40;
                    if (uVar3 < *(uint *)(lVar9 + 0x18)) {
                      iVar1 = *(int *)(lVar10 + 0x28);
                      iVar16 = *(int *)(lVar9 + (long)(int)uVar3 * 4 + 0x20);
                      plVar7 = (long *)FUN_00db0c30(*(undefined8 *)PTR_object___TypeInfo_01fc08c0,2)
                      ;
                      if (*(int *)(lVar5 + 0x18) != 0) {
                        lVar9 = *(long *)(*(long *)(*(long *)puVar4 + 0xb8) + 8);
                        if (lVar9 == 0) goto LAB_00ef3a40;
                        if (*(uint *)(lVar5 + 0x20) < *(uint *)(lVar9 + 0x18)) {
                          if (plVar7 == (long *)0x0) goto LAB_00ef3a40;
                          lVar9 = *(long *)(lVar9 + (long)(int)*(uint *)(lVar5 + 0x20) * 8 + 0x20);
                          if ((lVar9 != 0) &&
                             (lVar10 = thunk_FUN_00e11b18(lVar9,*(undefined8 *)(*plVar7 + 0x40)),
                             lVar10 == 0)) {
LAB_00ef3a48:
                            uVar8 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
                            FUN_00db0cb0(uVar8,0);
                          }
                          if (*(int *)(plVar7 + 3) != 0) {
                            plVar7[4] = lVar9;
                            lVar9 = FUN_00db0c30(*(undefined8 *)PTR_float___TypeInfo_01fc0858,6);
                            uVar3 = *(uint *)(lVar5 + 0x18);
                            if (5 < uVar3) {
                              if (lVar9 == 0) goto LAB_00ef3a40;
                              uVar2 = *(uint *)(lVar9 + 0x18);
                              if (uVar2 != 0) {
                                iVar13 = *(int *)(lVar5 + 0x34);
                                *(float *)(lVar9 + 0x20) = (float)iVar13;
                                if ((6 < uVar3) && (1 < uVar2)) {
                                  iVar14 = *(int *)(lVar5 + 0x38);
                                  *(float *)(lVar9 + 0x24) = (float)iVar14;
                                  if (uVar2 != 2) {
                                    fVar15 = (float)iVar1 / (float)iVar16;
                                    *(float *)(lVar9 + 0x28) =
                                         fVar15 * (float)*(int *)(lVar5 + 0x2c);
                                    if (((3 < uVar2) &&
                                        (*(float *)(lVar9 + 0x2c) =
                                              fVar15 * (float)*(int *)(lVar5 + 0x30), uVar2 != 4))
                                       && (*(float *)(lVar9 + 0x30) = fVar15 * (float)iVar13,
                                          5 < uVar2)) {
                                      *(float *)(lVar9 + 0x34) = fVar15 * (float)iVar14;
                                      lVar10 = thunk_FUN_00e11b18(lVar9,*(undefined8 *)
                                                                         (*plVar7 + 0x40));
                                      if (lVar10 == 0) goto LAB_00ef3a48;
                                      if (1 < *(uint *)(plVar7 + 3)) {
                                        plVar7[5] = lVar9;
                                        if ((1 < *(uint *)(lVar5 + 0x18)) &&
                                           (*(uint *)(lVar5 + 0x18) != 2)) {
                                          if (*(long *)(param_1 + 0x138) != 0) {
                                            surface_TouchEffectManager__AddEffect
                                                      ((float)(*(int *)(lVar5 + 0x24) +
                                                              *(int *)(lVar12 + 0x38)),
                                                       (float)(*(int *)(lVar5 + 0x28) +
                                                              *(int *)(lVar12 + 0x3c)),
                                                       *(long *)(param_1 + 0x138),param_1,0,lVar12,
                                                       plVar7,0);
                                            return;
                                          }
                                          goto LAB_00ef3a40;
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
LAB_00ef3a44:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
LAB_00ef3a40:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__SetLayoutMode
// Address: 00ef3a88
// ==========================================================================================

void surface_GamePad__SetLayoutMode(long param_1,int param_2)

{
  byte bVar1;
  undefined *puVar2;
  long lVar3;
  long *plVar4;
  
  puVar2 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if ((DAT_020ff729 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_surface_SurfaceManager_TypeInfo_01fc08d8);
    DAT_020ff729 = 1;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = kairo_unity_ui_Canvas__GetInstance(0);
  if (lVar3 != 0) {
    plVar4 = *(long **)(lVar3 + 0x28);
    if (plVar4 != (long *)0x0) {
      bVar1 = *(byte *)(*(long *)PTR_surface_SurfaceManager_TypeInfo_01fc08d8 + 0x130);
      if ((*(byte *)(*plVar4 + 0x130) < bVar1) ||
         (*(long *)(*(long *)(*plVar4 + 200) + (ulong)bVar1 * 8 + -8) !=
          *(long *)PTR_surface_SurfaceManager_TypeInfo_01fc08d8)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180();
      }
    }
    if (param_2 == 1) {
      if (plVar4 != (long *)0x0) {
        *(undefined *)((long)plVar4 + 0x39) = 1;
        return;
      }
    }
    else {
      if (param_2 != 0) {
        return;
      }
      if (plVar4 != (long *)0x0) {
        *(undefined *)((long)plVar4 + 0x39) = 0;
        if (*(long *)(param_1 + 0x128) != 0) {
          *(undefined4 *)(*(long *)(param_1 + 0x128) + 0xfc) = 0x7fc00000;
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__GetInstance
// Address: 00ef3b74
// ==========================================================================================

undefined8 surface_GameView__GetInstance(void)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff72d & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff72d = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) == 0) {
    uVar3 = thunk_FUN_00e11c14();
    surface_GameView___ctor();
    lVar2 = *(long *)puVar1;
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    **(undefined8 **)(lVar2 + 0xb8) = uVar3;
    lVar2 = *(long *)puVar1;
  }
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return **(undefined8 **)(lVar2 + 0xb8);
}



// ==========================================================================================
// Function: surface_GamePad__Draw
// Address: 00ef3c14
// ==========================================================================================

void surface_GamePad__Draw(long param_1,long param_2)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  byte bVar4;
  undefined *puVar5;
  undefined *puVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  long lVar11;
  long lVar12;
  long lVar13;
  ulong uVar14;
  ulong uVar15;
  ulong uVar16;
  undefined8 uVar17;
  long *plVar18;
  uint uVar19;
  int iVar20;
  undefined4 uVar21;
  ulong uVar22;
  undefined4 *puVar23;
  long lVar24;
  int iVar25;
  long lVar26;
  float fVar27;
  float fVar28;
  undefined8 local_a0;
  long *plStack_98;
  undefined8 *local_90;
  undefined8 local_88;
  long local_78;
  
  puVar6 = PTR_surface_SurfaceManager_TypeInfo_01fc08d8;
  local_78 = param_2;
  if ((DAT_020ff720 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_form_SubForm_TypeInfo_01fbf300);
    FUN_00db0bbc(PTR_surface_SurfaceManager_TypeInfo_01fc08d8);
    DAT_020ff720 = 1;
  }
  lVar26 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
  lVar11 = form_FormManager__GetInstance(0);
  puVar6 = PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70;
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  local_88 = kairo_unity_ui_Graphics__GetFont(param_2,0,0);
  plStack_98 = &local_78;
  local_a0 = 0;
  local_90 = &local_88;
  if (*(int *)(*(long *)puVar6 + 0xe0) == 0) {
                    /* try { // try from 00ef3d38 to 00ef3d47 has its CatchHandler @ 00ef57a4 */
    thunk_FUN_00df405c();
  }
  kairo_unity_ui_Font__PushLocalizeSetting(0,0);
  if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53d0 to 00ef53d3 has its CatchHandler @ 00ef57a0 */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef3d58 to 00ef3d5f has its CatchHandler @ 00ef57a0 */
  kairo_unity_ui_Graphics__SetRenderRect
            (local_78,*(undefined4 *)(param_1 + 0xb4),*(undefined4 *)(param_1 + 0xb8),
             *(undefined4 *)(param_1 + 0xbc),*(undefined4 *)(param_1 + 0xc0),0);
  if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53d4 to 00ef53d7 has its CatchHandler @ 00ef579c */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef3d68 to 00ef3d77 has its CatchHandler @ 00ef579c */
  kairo_unity_ui_Graphics__Scale(0x42c80000,local_78,0);
  if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53d8 to 00ef53db has its CatchHandler @ 00ef57ac */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef3d84 to 00ef3da3 has its CatchHandler @ 00ef57ac */
  kairo_unity_ui_Graphics__SetFont(local_78,*(undefined8 *)(param_1 + 0x140),0);
  puVar6 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar12 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar12 = *(long *)puVar6;
  }
  puVar6 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if (*(char *)(*(long *)(lVar12 + 0xb8) + 0xba) == '\0') {
    bVar1 = true;
  }
  else {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
                    /* try { // try from 00ef3dd0 to 00ef3dd3 has its CatchHandler @ 00ef57a4 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef3dd4 to 00ef3df7 has its CatchHandler @ 00ef5780 */
    lVar12 = kairo_unity_ui_Canvas__GetInstance(0);
    puVar5 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
    if (*(int *)(*(long *)PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
                    /* try { // try from 00ef3e04 to 00ef3e27 has its CatchHandler @ 00ef5790 */
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    lVar13 = *(long *)puVar5;
    if (*(int *)(lVar13 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar13 = *(long *)puVar5;
    }
    if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53e8 to 00ef53eb has its CatchHandler @ 00ef5790 */
      FUN_00db0de4();
    }
    lVar13 = **(long **)(lVar13 + 0xb8);
                    /* try { // try from 00ef3e38 to 00ef3e5f has its CatchHandler @ 00ef577c */
    iVar7 = kairo_unity_ui_Canvas__GetHeight(lVar12,0);
    if (*(int *)(*(long *)PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef3e60 to 00ef3e67 has its CatchHandler @ 00ef5778 */
    iVar8 = kairo_unity_ad_AdMobView__GetAdHeight(0);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53ec to 00ef53ef has its CatchHandler @ 00ef5774 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef3e70 to 00ef3e7f has its CatchHandler @ 00ef5770 */
    fVar27 = (float)kairo_unity_ui_IApplication__GetScaleRatio(lVar13,0,0);
    lVar12 = *(long *)puVar6;
    fVar27 = (fVar27 * 240.0) / 100.0;
    iVar9 = -0x80000000;
    if (fVar27 != INFINITY) {
      iVar9 = (int)fVar27;
    }
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef3ebc to 00ef3ebf has its CatchHandler @ 00ef56cc */
      thunk_FUN_00df405c();
      lVar12 = *(long *)puVar6;
    }
    bVar1 = (*(float *)(param_1 + 0xc4) * (float)*(int *)(*(long *)(lVar12 + 0xb8) + 0x30)) / 100.0
            <= (float)((iVar7 - iVar8) - iVar9);
  }
  if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53dc to 00ef53df has its CatchHandler @ 00ef578c */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef3f08 to 00ef3f0f has its CatchHandler @ 00ef5788 */
  uVar14 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_1 + 0x130),0);
  uVar15 = uVar14;
  uVar16 = 0;
  do {
    uVar22 = uVar16;
    lVar12 = *(long *)puVar6;
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef3f28 to 00ef3f2f has its CatchHandler @ 00ef57b8 */
      uVar15 = thunk_FUN_00df405c(lVar12);
      lVar12 = *(long *)puVar6;
    }
    lVar13 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x40);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53c0 to 00ef53c3 has its CatchHandler @ 00ef57c4 */
      FUN_00db0de4();
    }
    lVar24 = (long)*(int *)(lVar13 + 0x18);
    if (lVar24 <= (long)uVar22) break;
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef3f54 to 00ef3f5b has its CatchHandler @ 00ef57b0 */
      thunk_FUN_00df405c(lVar12);
      lVar13 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x40);
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53c8 to 00ef53cb has its CatchHandler @ 00ef57b4 */
        FUN_00db0de4();
      }
    }
    if (*(uint *)(lVar13 + 0x18) <= uVar22) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53c4 to 00ef53c7 has its CatchHandler @ 00ef57bc */
      FUN_00db0dec();
    }
                    /* try { // try from 00ef3f80 to 00ef3f8b has its CatchHandler @ 00ef57c0 */
    uVar15 = java_lang_StringEx__EqualsIgnoreCase
                       (*(undefined8 *)(lVar13 + uVar22 * 8 + 0x20),uVar14,0);
    uVar16 = uVar22 + 1;
  } while ((uVar15 & 1) == 0);
  iVar8 = *(int *)(param_1 + 0xc0);
  fVar28 = (float)(*(int *)(param_1 + 0xbc) * 100) / *(float *)(param_1 + 0xc4);
  fVar27 = (float)(iVar8 * 100) / *(float *)(param_1 + 0xc4);
  iVar7 = -0x80000000;
  if (fVar28 != INFINITY) {
    iVar7 = (int)fVar28;
  }
  iVar9 = -0x80000000;
  if (fVar27 != INFINITY) {
    iVar9 = (int)fVar27;
  }
  if (lVar26 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53e0 to 00ef53e3 has its CatchHandler @ 00ef5784 */
    FUN_00db0de4();
  }
  iVar2 = *(int *)(lVar26 + 0xb8);
  iVar25 = *(int *)(param_1 + 0xb8);
  iVar3 = *(int *)(lVar26 + 0xc0);
  iVar10 = iVar2 - iVar25;
  if (0 < iVar10) {
    lVar12 = *(long *)puVar6;
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef4008 to 00ef400b has its CatchHandler @ 00ef57a4 */
      thunk_FUN_00df405c();
      lVar12 = *(long *)puVar6;
    }
    lVar13 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53f0 to 00ef53f3 has its CatchHandler @ 00ef576c */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar13 + 0x18) < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53f4 to 00ef53fb has its CatchHandler @ 00ef5794 */
      FUN_00db0dec();
    }
    lVar13 = *(long *)(lVar13 + 0x30);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar13 + 0x18) < 7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53fc to 00ef53ff has its CatchHandler @ 00ef5768 */
      FUN_00db0dec();
    }
    iVar20 = *(int *)(lVar13 + 0x38);
    if (iVar10 < iVar20) {
                    /* try { // try from 00ef405c to 00ef4067 has its CatchHandler @ 00ef574c */
      uVar15 = surface_GamePad__DrawScaledImage
                         (0,(float)(iVar10 - iVar20),(float)*(int *)(param_1 + 0xbc),(float)iVar20,
                          lVar12,local_78,2);
    }
    else {
                    /* try { // try from 00ef4070 to 00ef407f has its CatchHandler @ 00ef5748 */
      uVar15 = surface_GamePad__DrawScaledImage
                         (0,0,(float)*(int *)(param_1 + 0xbc),(float)iVar10,lVar12,local_78,2);
    }
  }
  uVar19 = (iVar8 + iVar25) - (iVar2 + iVar3);
  if (*(int *)(param_1 + 0x178) == 0) {
                    /* try { // try from 00ef4148 to 00ef4153 has its CatchHandler @ 00ef5758 */
    surface_GamePad__DrawScaledImage
              (0,(float)(*(int *)(param_1 + 0xc0) - uVar19) + -0.5,(float)*(int *)(param_1 + 0xbc),
               (float)uVar19,uVar15,local_78,0);
  }
  else if ((0 < (int)uVar19) && (*(int *)(param_1 + 0x178) == 1)) {
    lVar12 = *(long *)puVar6;
    if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef40b0 to 00ef40b3 has its CatchHandler @ 00ef57a4 */
      thunk_FUN_00df405c();
      lVar12 = *(long *)puVar6;
    }
    lVar13 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5400 to 00ef5403 has its CatchHandler @ 00ef5750 */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar13 + 0x18) < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5404 to 00ef540b has its CatchHandler @ 00ef5764 */
      FUN_00db0dec();
    }
    lVar13 = *(long *)(lVar13 + 0x38);
    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar13 + 0x18) < 7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef540c to 00ef540f has its CatchHandler @ 00ef5744 */
      FUN_00db0dec();
    }
    fVar27 = (float)(*(int *)(param_1 + 0xc0) + ~uVar19);
    if ((int)uVar19 < *(int *)(lVar13 + 0x38)) {
                    /* try { // try from 00ef4114 to 00ef411f has its CatchHandler @ 00ef56b8 */
      surface_GamePad__DrawScaledImage
                (0,fVar27,(float)*(int *)(param_1 + 0xbc),(float)(*(int *)(lVar13 + 0x38) + 1),
                 lVar12,local_78,3);
    }
    else {
                    /* try { // try from 00ef4160 to 00ef416b has its CatchHandler @ 00ef56b4 */
      surface_GamePad__DrawScaledImage
                (0,fVar27,(float)*(int *)(param_1 + 0xbc),(float)(uVar19 + 1),lVar12,local_78,3);
    }
  }
  if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef53e4 to 00ef53e7 has its CatchHandler @ 00ef5798 */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef4178 to 00ef417f has its CatchHandler @ 00ef5798 */
  kairo_unity_ui_Graphics__Scale(*(undefined4 *)(param_1 + 0xc4),local_78,0);
  iVar2 = *(int *)(param_1 + 0x178);
  fVar27 = (float)(uVar19 * 100) / *(float *)(param_1 + 0xc4);
  iVar8 = -0x80000000;
  if (fVar27 != INFINITY) {
    iVar8 = (int)fVar27;
  }
  if (iVar2 == 0) {
    if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5414 to 00ef5417 has its CatchHandler @ 00ef575c */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef433c to 00ef4347 has its CatchHandler @ 00ef575c */
    kairo_unity_ui_Graphics__SetOrigin(0,(float)(iVar9 - iVar8),local_78,0);
    puVar6 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
                    /* try { // try from 00ef4354 to 00ef4377 has its CatchHandler @ 00ef5734 */
    surface_GamePad__AddTouch(0x42d00000,0,param_1,local_78,6,0x20000,1,0);
                    /* try { // try from 00ef437c to 00ef43a3 has its CatchHandler @ 00ef572c */
    surface_GamePad__AddTouch(0x42d40000,0x42d60000,param_1,local_78,7,0x80000,1,0);
                    /* try { // try from 00ef43a8 to 00ef43cb has its CatchHandler @ 00ef5728 */
    surface_GamePad__AddTouch(0x429e0000,0x41d80000,param_1,local_78,8,0x10000,1,0);
                    /* try { // try from 00ef43d0 to 00ef43f3 has its CatchHandler @ 00ef5720 */
    surface_GamePad__AddTouch(0x433a0000,0x41c80000,param_1,local_78,9,0x40000,1,0);
                    /* try { // try from 00ef43f8 to 00ef4433 has its CatchHandler @ 00ef5754 */
    surface_GamePad__AddTouch(0x42f20000,0x42240000,param_1,local_78,10,0x100000,1,0);
    lVar26 = *(long *)puVar6;
    if (*(int *)(lVar26 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar26);
      lVar26 = *(long *)puVar6;
    }
    if ((*(char *)(*(long *)(lVar26 + 0xb8) + 0x10) != '\0') && (*(char *)(param_1 + 0x158) == '\0')
       ) {
      if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54b8 to 00ef54bb has its CatchHandler @ 00ef55b4 */
        FUN_00db0de4();
      }
      if (*(char *)(lVar11 + 0x5c) == '\0') {
        if (*(int *)(lVar26 + 0xe0) == 0) {
                    /* try { // try from 00ef4464 to 00ef446b has its CatchHandler @ 00ef57a4 */
          thunk_FUN_00df405c(lVar26);
          lVar11 = *(long *)puVar6;
          if (*(char *)(*(long *)(lVar11 + 0xb8) + 0x10) != '\0') goto LAB_00ef447c;
        }
        else {
LAB_00ef447c:
                    /* try { // try from 00ef4480 to 00ef44a3 has its CatchHandler @ 00ef557c */
          surface_GamePad__AddTouch(0x40a00000,0x42a00000,param_1,local_78,0xb,1,1,0);
          lVar11 = *(long *)puVar6;
        }
        if (*(int *)(lVar11 + 0xe0) == 0) {
                    /* try { // try from 00ef44b0 to 00ef44b7 has its CatchHandler @ 00ef57a4 */
          thunk_FUN_00df405c(lVar11);
          lVar11 = *(long *)puVar6;
        }
        if (*(char *)(*(long *)(lVar11 + 0xb8) + 0x10) != '\0') {
                    /* try { // try from 00ef44cc to 00ef44f3 has its CatchHandler @ 00ef5560 */
          surface_GamePad__AddTouch(0x43730000,0x42dc0000,param_1,local_78,0xc,0x10,1,0);
          lVar11 = *(long *)puVar6;
        }
        if (*(int *)(lVar11 + 0xe0) == 0) {
                    /* try { // try from 00ef4500 to 00ef4507 has its CatchHandler @ 00ef57a4 */
          thunk_FUN_00df405c(lVar11);
          lVar11 = *(long *)puVar6;
        }
        if (*(char *)(*(long *)(lVar11 + 0xb8) + 0x11) == '\0') {
                    /* try { // try from 00ef451c to 00ef4543 has its CatchHandler @ 00ef5550 */
          surface_GamePad__AddTouch(0x43730000,0x42b40000,param_1,local_78,0xd,0x40,1,0);
          lVar11 = *(long *)puVar6;
        }
        if (*(int *)(lVar11 + 0xe0) == 0) {
                    /* try { // try from 00ef4550 to 00ef4557 has its CatchHandler @ 00ef57a4 */
          thunk_FUN_00df405c(lVar11);
          lVar11 = *(long *)puVar6;
        }
        if (*(char *)(*(long *)(lVar11 + 0xb8) + 0x11) == '\0') {
                    /* try { // try from 00ef456c to 00ef4593 has its CatchHandler @ 00ef554c */
          surface_GamePad__AddTouch(0x43730000,0x42800000,param_1,local_78,0xe,0,1,0);
        }
      }
    }
    lVar11 = local_78;
    if ((long)uVar22 < lVar24) {
                    /* try { // try from 00ef45a0 to 00ef45c3 has its CatchHandler @ 00ef5654 */
      surface_GamePad__AddTouch(0x40a00000,0x40e00000,param_1,local_78,5,0x200000,1,0);
      lVar11 = local_78;
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef545c to 00ef545f has its CatchHandler @ 00ef5648 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef45d0 to 00ef45d7 has its CatchHandler @ 00ef5640 */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef45d8 to 00ef4623 has its CatchHandler @ 00ef573c */
      iVar7 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x43730000,0x40e00000,param_1,lVar11,1,0x400000,0 < iVar7,0);
      if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef4624 to 00ef462b has its CatchHandler @ 00ef5628 */
      uVar15 = kairo_unity_util_Language__Japanese(0);
      if ((uVar15 & 1) == 0) {
                    /* try { // try from 00ef4a2c to 00ef4a43 has its CatchHandler @ 00ef55c0 */
        surface_GamePad__DrawImage(0x41700000,0x42400000,param_1,local_78,0x12);
      }
      else {
                    /* try { // try from 00ef4634 to 00ef464b has its CatchHandler @ 00ef55c4 */
        surface_GamePad__DrawImage(0x41700000,0x42400000,param_1,local_78,0x11);
      }
    }
    else {
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5458 to 00ef545b has its CatchHandler @ 00ef5650 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef4750 to 00ef4757 has its CatchHandler @ 00ef564c */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef4758 to 00ef4787 has its CatchHandler @ 00ef570c */
      iVar7 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x40a00000,0x40e00000,param_1,lVar11,0,0x200000,0 < iVar7,0);
      lVar11 = local_78;
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5464 to 00ef5467 has its CatchHandler @ 00ef5634 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef4794 to 00ef479b has its CatchHandler @ 00ef562c */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef479c to 00ef47cf has its CatchHandler @ 00ef56f8 */
      iVar7 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x43730000,0x40e00000,param_1,lVar11,1,0x400000,0 < iVar7,0);
    }
                    /* try { // try from 00ef4a48 to 00ef4a5f has its CatchHandler @ 00ef56f4 */
    surface_GamePad__DrawWatch(0x43a00000,0x430f0000,param_1,local_78);
                    /* try { // try from 00ef4a64 to 00ef4a7b has its CatchHandler @ 00ef56ec */
    uVar17 = surface_GamePad__DrawBattery(0x43920000,0x430e0000,param_1,local_78);
    if (bVar1) {
                    /* try { // try from 00ef4a90 to 00ef4aab has its CatchHandler @ 00ef5618 */
      uVar17 = surface_GamePad__AddTouch
                         (0x40a00000,(float)(iVar8 + -0x1c),param_1,local_78,0x16,0,1,0);
    }
                    /* try { // try from 00ef4ab0 to 00ef4abf has its CatchHandler @ 00ef56e4 */
    surface_GamePad__DrawVersion(uVar17,local_78,0x115,0x2d,0);
    goto LAB_00ef4fac;
  }
  if (iVar2 == 1) {
    if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5410 to 00ef5413 has its CatchHandler @ 00ef5760 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4228 to 00ef424b has its CatchHandler @ 00ef5760 */
    kairo_unity_ui_Graphics__SetOrigin(0,(float)(iVar9 - iVar8),local_78,0);
    lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    if (*(int *)(lVar12 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    }
    lVar13 = local_78;
    uVar21 = 0x40e00000;
    if (*(char *)(*(long *)(lVar12 + 0xb8) + 0x10) != '\0') {
      uVar21 = 0x40800000;
    }
    if ((long)uVar22 < lVar24) {
                    /* try { // try from 00ef427c to 00ef429f has its CatchHandler @ 00ef5698 */
      surface_GamePad__AddTouch(0x40a00000,uVar21,param_1,local_78,5,0x200000,1,0);
      lVar12 = local_78;
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5444 to 00ef5447 has its CatchHandler @ 00ef5688 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef42ac to 00ef42b3 has its CatchHandler @ 00ef5680 */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef42b4 to 00ef42ff has its CatchHandler @ 00ef5740 */
      iVar9 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x43730000,uVar21,param_1,lVar12,1,0x400000,0 < iVar9,0);
      if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef4300 to 00ef4307 has its CatchHandler @ 00ef5658 */
      uVar15 = kairo_unity_util_Language__Japanese(0);
      if ((uVar15 & 1) == 0) {
                    /* try { // try from 00ef47d4 to 00ef47eb has its CatchHandler @ 00ef55d0 */
        surface_GamePad__DrawImage(0x41700000,0x42400000,param_1,local_78,0x12);
      }
      else {
                    /* try { // try from 00ef4310 to 00ef4327 has its CatchHandler @ 00ef55d4 */
        surface_GamePad__DrawImage(0x41700000,0x42400000,param_1,local_78,0x11);
      }
    }
    else {
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef543c to 00ef543f has its CatchHandler @ 00ef5694 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef46c4 to 00ef46cb has its CatchHandler @ 00ef568c */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef46cc to 00ef46fb has its CatchHandler @ 00ef5724 */
      iVar9 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x40a00000,uVar21,param_1,lVar13,0,0x200000,0 < iVar9,0);
      lVar12 = local_78;
      if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5450 to 00ef5453 has its CatchHandler @ 00ef5670 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef4708 to 00ef470f has its CatchHandler @ 00ef5660 */
      uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef4710 to 00ef4743 has its CatchHandler @ 00ef5718 */
      iVar9 = java_lang_StringEx__Length(uVar17,0);
      surface_GamePad__AddTouch(0x43730000,uVar21,param_1,lVar12,1,0x400000,0 < iVar9,0);
    }
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5418 to 00ef541b has its CatchHandler @ 00ef5710 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef47f4 to 00ef47ff has its CatchHandler @ 00ef5708 */
    uVar15 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_1 + 0x130),2,0);
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef541c to 00ef541f has its CatchHandler @ 00ef5704 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef480c to 00ef4817 has its CatchHandler @ 00ef56fc */
    uVar16 = kairo_unity_ui_Canvas__GetSoftLabel(*(long *)(param_1 + 0x130),3,0);
    lVar12 = local_78;
    if ((uVar15 == 0) || (uVar16 == 0)) {
      if ((uVar15 | uVar16) != 0) {
        if (uVar15 == 0) {
          if (uVar16 != 0) {
            lVar13 = *(long *)puVar6;
            if (*(int *)(lVar13 + 0xe0) == 0) {
                    /* try { // try from 00ef4ed4 to 00ef4ed7 has its CatchHandler @ 00ef5528 */
              thunk_FUN_00df405c();
              lVar13 = *(long *)puVar6;
            }
            lVar13 = *(long *)(*(long *)(lVar13 + 0xb8) + 0x20);
            if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54d8 to 00ef54db has its CatchHandler @ 00ef556c */
              FUN_00db0de4();
            }
            if (*(uint *)(lVar13 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54dc to 00ef54e3 has its CatchHandler @ 00ef5580 */
              FUN_00db0dec();
            }
            lVar13 = *(long *)(lVar13 + 0x40);
            if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
              FUN_00db0de4();
            }
            if (*(uint *)(lVar13 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54e4 to 00ef54e7 has its CatchHandler @ 00ef5568 */
              FUN_00db0dec();
            }
            iVar2 = *(int *)(lVar13 + 0x34);
            iVar9 = iVar7;
            if (iVar7 < 0) {
              iVar9 = iVar7 + 1;
            }
            if (iVar2 < 0) {
              iVar2 = iVar2 + 1;
            }
                    /* try { // try from 00ef4f38 to 00ef4f53 has its CatchHandler @ 00ef5564 */
            surface_GamePad__AddTouch
                      ((float)((iVar9 >> 1) - (iVar2 >> 1)),uVar21,param_1,lVar12,4,0x1000000,
                       0 < *(int *)(uVar16 + 0x10),0);
          }
        }
        else {
          lVar13 = *(long *)puVar6;
          if (*(int *)(lVar13 + 0xe0) == 0) {
                    /* try { // try from 00ef49a8 to 00ef49ab has its CatchHandler @ 00ef5570 */
            thunk_FUN_00df405c();
            lVar13 = *(long *)puVar6;
          }
          lVar13 = *(long *)(*(long *)(lVar13 + 0xb8) + 0x20);
          if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54c0 to 00ef54c3 has its CatchHandler @ 00ef55a0 */
            FUN_00db0de4();
          }
          if (*(uint *)(lVar13 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54c4 to 00ef54cb has its CatchHandler @ 00ef55d8 */
            FUN_00db0dec();
          }
          lVar13 = *(long *)(lVar13 + 0x40);
          if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
            FUN_00db0de4();
          }
          if (*(uint *)(lVar13 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54cc to 00ef54cf has its CatchHandler @ 00ef559c */
            FUN_00db0dec();
          }
          iVar2 = *(int *)(lVar13 + 0x34);
          iVar9 = iVar7;
          if (iVar7 < 0) {
            iVar9 = iVar7 + 1;
          }
          if (iVar2 < 0) {
            iVar2 = iVar2 + 1;
          }
                    /* try { // try from 00ef4a0c to 00ef4a27 has its CatchHandler @ 00ef5598 */
          surface_GamePad__AddTouch
                    ((float)((iVar9 >> 1) - (iVar2 >> 1)),uVar21,param_1,lVar12,4,0x800000,
                     0 < *(int *)(uVar15 + 0x10),0);
        }
      }
    }
    else {
                    /* try { // try from 00ef4830 to 00ef484b has its CatchHandler @ 00ef5624 */
      lVar13 = surface_GamePad__GetDivisionArea(0x40a00000,(float)(iVar7 + -5),0,param_1,1,4);
      lVar12 = local_78;
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5468 to 00ef546b has its CatchHandler @ 00ef5620 */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar13 + 0x18) < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef546c to 00ef546f has its CatchHandler @ 00ef56c4 */
        FUN_00db0dec();
      }
      lVar24 = *(long *)puVar6;
      fVar27 = *(float *)(lVar13 + 0x28);
      if (*(int *)(lVar24 + 0xe0) == 0) {
                    /* try { // try from 00ef4870 to 00ef4877 has its CatchHandler @ 00ef56c4 */
        thunk_FUN_00df405c(lVar24);
        lVar24 = *(long *)puVar6;
      }
      lVar13 = *(long *)(*(long *)(lVar24 + 0xb8) + 0x20);
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5470 to 00ef5473 has its CatchHandler @ 00ef561c */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar13 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5474 to 00ef547b has its CatchHandler @ 00ef56dc */
        FUN_00db0dec();
      }
      lVar13 = *(long *)(lVar13 + 0x40);
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar13 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef547c to 00ef547f has its CatchHandler @ 00ef5610 */
        FUN_00db0dec();
      }
      iVar9 = *(int *)(lVar13 + 0x34);
      if (iVar9 < 0) {
        iVar9 = iVar9 + 1;
      }
                    /* try { // try from 00ef48cc to 00ef48e7 has its CatchHandler @ 00ef560c */
      surface_GamePad__AddTouch
                (fVar27 - (float)(iVar9 >> 1),uVar21,param_1,lVar12,2,0x800000,
                 0 < *(int *)(uVar15 + 0x10),0);
                    /* try { // try from 00ef48e8 to 00ef4903 has its CatchHandler @ 00ef5608 */
      lVar12 = surface_GamePad__GetDivisionArea(0x40a00000,(float)(iVar7 + -5),0,param_1,2,4);
      if (lVar12 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5480 to 00ef5483 has its CatchHandler @ 00ef5604 */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar12 + 0x18) < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5484 to 00ef5487 has its CatchHandler @ 00ef5600 */
        FUN_00db0dec();
      }
      lVar13 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x20);
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5488 to 00ef548b has its CatchHandler @ 00ef55fc */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar13 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef548c to 00ef5493 has its CatchHandler @ 00ef56d4 */
        FUN_00db0dec();
      }
      lVar13 = *(long *)(lVar13 + 0x40);
      if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar13 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5494 to 00ef5497 has its CatchHandler @ 00ef55f8 */
        FUN_00db0dec();
      }
      iVar9 = *(int *)(lVar13 + 0x34);
      if (iVar9 < 0) {
        iVar9 = iVar9 + 1;
      }
                    /* try { // try from 00ef4970 to 00ef4987 has its CatchHandler @ 00ef55f4 */
      surface_GamePad__AddTouch
                (*(float *)(lVar12 + 0x28) - (float)(iVar9 >> 1),uVar21,param_1,local_78,3,0x1000000
                 ,0 < *(int *)(uVar16 + 0x10),0);
    }
    if (*(char *)(param_1 + 0x174) == '\0') {
      lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      if (bVar1) {
        if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef4ff8 to 00ef501f has its CatchHandler @ 00ef57a4 */
          thunk_FUN_00df405c();
          lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
        }
        if (*(char *)(*(long *)(lVar12 + 0xb8) + 0x10) == '\0') {
          if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
                    /* try { // try from 00ef5104 to 00ef5107 has its CatchHandler @ 00ef57a4 */
            thunk_FUN_00df405c();
          }
                    /* try { // try from 00ef5108 to 00ef510f has its CatchHandler @ 00ef5594 */
          lVar11 = kairo_unity_ui_Canvas__GetInstance(0);
          if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54d4 to 00ef54d7 has its CatchHandler @ 00ef5594 */
            FUN_00db0de4();
          }
                    /* try { // try from 00ef5114 to 00ef511b has its CatchHandler @ 00ef5574 */
          iVar7 = kairo_unity_ui_Canvas__GetHeight(lVar11,0);
          puVar5 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
          fVar27 = *(float *)(lVar26 + 0xc4);
          lVar11 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
          if (*(int *)(lVar11 + 0xe0) == 0) {
                    /* try { // try from 00ef5138 to 00ef513b has its CatchHandler @ 00ef552c */
            thunk_FUN_00df405c();
            lVar11 = *(long *)puVar5;
          }
          if (*(char *)(*(long *)(lVar11 + 0xb8) + 0xba) == '\0') {
            iVar9 = 0;
          }
          else {
            if (*(int *)(*(long *)PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0 + 0xe0) == 0) {
                    /* try { // try from 00ef5160 to 00ef5163 has its CatchHandler @ 00ef57a4 */
              thunk_FUN_00df405c();
            }
                    /* try { // try from 00ef5164 to 00ef516b has its CatchHandler @ 00ef5558 */
            iVar9 = kairo_unity_ad_AdMobView__GetAdHeight(0);
          }
          lVar12 = *(long *)puVar6;
          if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef5184 to 00ef5187 has its CatchHandler @ 00ef57a4 */
            thunk_FUN_00df405c();
            lVar12 = *(long *)puVar6;
          }
          if ((*(float *)(param_1 + 0xc4) * (float)*(int *)(*(long *)(lVar12 + 0xb8) + 0x30)) /
              100.0 <= ((float)iVar7 + (fVar27 * -240.0) / 100.0) - (float)iVar9) {
                    /* try { // try from 00ef51e8 to 00ef5207 has its CatchHandler @ 00ef5554 */
            lVar12 = surface_GamePad__AddTouch
                               (0x42f40000,(float)(iVar8 + -0x1c),param_1,local_78,0x15,0,1,0);
          }
          goto LAB_00ef4f98;
        }
      }
      if (*(int *)(lVar12 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar12 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      }
      if ((*(char *)(*(long *)(lVar12 + 0xb8) + 0x10) != '\0') &&
         (*(char *)(param_1 + 0x158) == '\0')) {
        if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54d0 to 00ef54d3 has its CatchHandler @ 00ef5578 */
          FUN_00db0de4();
        }
        if (*(char *)(lVar11 + 0x5c) == '\0') {
                    /* try { // try from 00ef505c to 00ef5063 has its CatchHandler @ 00ef553c */
          lVar11 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,5);
          if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54e8 to 00ef54eb has its CatchHandler @ 00ef5538 */
            FUN_00db0de4();
          }
          uVar15 = *(ulong *)(lVar11 + 0x18) & 0xffffffff;
          uVar19 = (uint)*(ulong *)(lVar11 + 0x18);
          if (0 < (long)(uVar15 << 0x20)) {
            lVar26 = (long)(int)uVar19;
            puVar23 = (undefined4 *)(lVar11 + 0x20);
            uVar16 = uVar15;
            do {
              if (uVar16 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5434 to 00ef5437 has its CatchHandler @ 00ef56a4 */
                FUN_00db0dec();
              }
              *puVar23 = 0xffffffff;
              lVar26 = lVar26 + -1;
              uVar16 = uVar16 - 1;
              puVar23 = puVar23 + 1;
            } while (lVar26 != 0);
          }
          if (uVar19 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54ec to 00ef54ef has its CatchHandler @ 00ef5534 */
            FUN_00db0dec();
          }
          *(undefined4 *)(lVar11 + 0x20) = 0x15;
          if (*(int *)(param_1 + 0x168) == 0) {
            if (uVar19 < 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54f8 to 00ef54fb has its CatchHandler @ 00ef551c */
              FUN_00db0dec();
            }
            *(undefined4 *)(lVar11 + 0x24) = 0xb;
            if (uVar19 == 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5500 to 00ef5503 has its CatchHandler @ 00ef5514 */
              FUN_00db0dec();
            }
            *(undefined4 *)(lVar11 + 0x28) = 0xe;
            if (uVar19 < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5508 to 00ef550b has its CatchHandler @ 00ef550c */
              FUN_00db0dec();
            }
            uVar21 = 0xc;
LAB_00ef5268:
            *(undefined4 *)(lVar11 + 0x2c) = uVar21;
          }
          else if (*(int *)(param_1 + 0x168) == 1) {
            if (uVar19 < 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54f4 to 00ef54f7 has its CatchHandler @ 00ef5520 */
              FUN_00db0dec();
            }
            *(undefined4 *)(lVar11 + 0x24) = 0x13;
            if (uVar19 == 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54fc to 00ef54ff has its CatchHandler @ 00ef5518 */
              FUN_00db0dec();
            }
            *(undefined4 *)(lVar11 + 0x28) = 0x12;
            if (uVar19 < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5504 to 00ef5507 has its CatchHandler @ 00ef5510 */
              FUN_00db0dec();
            }
            uVar21 = 0x14;
            goto LAB_00ef5268;
          }
          if (uVar19 < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54f0 to 00ef54f3 has its CatchHandler @ 00ef5530 */
            FUN_00db0dec();
          }
          *(undefined4 *)(lVar11 + 0x30) = 0x10;
          lVar12 = lVar11;
          if (0 < (int)uVar19) {
            uVar16 = 0;
            do {
              if (uVar15 <= uVar16) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5438 to 00ef543b has its CatchHandler @ 00ef56a0 */
                FUN_00db0dec();
              }
              if (*(int *)(lVar11 + 0x20 + uVar16 * 4) != -1) {
                    /* try { // try from 00ef52b4 to 00ef52cb has its CatchHandler @ 00ef55e4 */
                lVar26 = surface_GamePad__GetDivisionArea
                                   (0,(float)iVar7,0,param_1,uVar16 & 0xffffffff);
                if (*(uint *)(lVar11 + 0x18) <= uVar16) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54a4 to 00ef54a7 has its CatchHandler @ 00ef56bc */
                  FUN_00db0dec();
                }
                if (lVar26 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54b0 to 00ef54b3 has its CatchHandler @ 00ef56bc */
                  FUN_00db0de4();
                }
                if (*(uint *)(lVar26 + 0x18) < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5498 to 00ef549b has its CatchHandler @ 00ef55ec */
                  FUN_00db0dec();
                }
                lVar12 = *(long *)puVar6;
                iVar9 = *(int *)(lVar11 + 0x20 + uVar16 * 4);
                fVar27 = *(float *)(lVar26 + 0x28);
                if (*(int *)(lVar12 + 0xe0) == 0) {
                    /* try { // try from 00ef52fc to 00ef5303 has its CatchHandler @ 00ef558c */
                  thunk_FUN_00df405c(lVar12);
                  lVar12 = *(long *)puVar6;
                }
                lVar26 = *(long *)(*(long *)(lVar12 + 0xb8) + 0x20);
                if (lVar26 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54a0 to 00ef54a3 has its CatchHandler @ 00ef55e8 */
                  FUN_00db0de4();
                }
                if (*(uint *)(lVar26 + 0x18) < 8) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef549c to 00ef549f has its CatchHandler @ 00ef56c0 */
                  FUN_00db0dec();
                }
                lVar26 = *(long *)(lVar26 + 0x58);
                if (lVar26 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54a8 to 00ef54ab has its CatchHandler @ 00ef56c0 */
                  FUN_00db0de4();
                }
                if (*(uint *)(lVar26 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54ac to 00ef54af has its CatchHandler @ 00ef55e0 */
                  FUN_00db0dec();
                }
                iVar2 = *(int *)(lVar26 + 0x34);
                if (iVar2 < 0) {
                  iVar2 = iVar2 + 1;
                }
                iVar25 = 0x400;
                if (iVar9 != 0xf) {
                  iVar25 = -1;
                }
                iVar3 = 0x10;
                if (iVar9 != 0xc) {
                  iVar3 = iVar25;
                }
                if (iVar9 == 0xb) {
                  iVar3 = 1;
                }
                fVar27 = fVar27 - (float)(iVar2 >> 1);
                if (iVar3 == -1) {
                    /* try { // try from 00ef538c to 00ef53a7 has its CatchHandler @ 00ef5590 */
                  lVar12 = surface_GamePad__AddTouch
                                     (fVar27,(float)(iVar8 + -0x15),param_1,local_78,iVar9,0,1,0);
                }
                else {
                    /* try { // try from 00ef5370 to 00ef5387 has its CatchHandler @ 00ef55ac */
                  lVar12 = surface_GamePad__AddTouch
                                     (fVar27,(float)(iVar8 + -0x15),param_1,local_78,iVar9,iVar3,1,0
                                     );
                }
              }
              uVar16 = uVar16 + 1;
              uVar15 = *(ulong *)(lVar11 + 0x18) & 0xffffffff;
            } while ((long)uVar16 < (long)(int)*(ulong *)(lVar11 + 0x18));
          }
        }
      }
    }
    else {
      if (local_78 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5430 to 00ef5433 has its CatchHandler @ 00ef56b0 */
        FUN_00db0de4();
      }
                    /* try { // try from 00ef4f64 to 00ef4f6b has its CatchHandler @ 00ef56ac */
      iVar7 = kairo_unity_ui_Graphics__GetOriginY(local_78,0);
                    /* try { // try from 00ef4f78 to 00ef4f97 has its CatchHandler @ 00ef56a8 */
      lVar12 = kairo_unity_surface_SurfaceBase__AddTouchComponent
                         (param_1,0x14,0,iVar8 + iVar7 + -0x1e,*(undefined4 *)(param_1 + 0xbc),0x23,
                          0,0,0);
    }
LAB_00ef4f98:
                    /* try { // try from 00ef4f9c to 00ef4fab has its CatchHandler @ 00ef56d0 */
    surface_GamePad__DrawVersion(lVar12,local_78,0x115,0x2d,0);
    goto LAB_00ef4fac;
  }
  if (iVar2 != 2) goto LAB_00ef4fac;
                    /* try { // try from 00ef41c4 to 00ef41cb has its CatchHandler @ 00ef5738 */
  fVar27 = (float)surface_GamePad__GetSideViewRatio(param_1);
  if (0.0 < fVar27) {
LAB_00ef4650:
    iVar8 = 0;
  }
  else {
    if (*(int *)(*(long *)PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660 + 0xe0) == 0) {
                    /* try { // try from 00ef41e8 to 00ef41eb has its CatchHandler @ 00ef57a4 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef41ec to 00ef41f7 has its CatchHandler @ 00ef569c */
    lVar26 = kairo_unity_native_KairoPlugin__GetSafeArea(0,0);
    if (lVar26 == 0) goto LAB_00ef4650;
    if (*(int *)(lVar26 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54b4 to 00ef54b7 has its CatchHandler @ 00ef55dc */
      FUN_00db0dec();
    }
    iVar8 = *(int *)(lVar26 + 0x20);
    if (iVar8 < 0) {
      iVar8 = iVar8 + 1;
    }
    iVar8 = iVar8 >> 1;
  }
                    /* try { // try from 00ef4654 to 00ef465b has its CatchHandler @ 00ef5730 */
  fVar27 = (float)surface_GamePad__GetSideViewRatio(param_1);
  iVar2 = iVar7 - iVar8;
  if (fVar27 <= 0.0) {
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5440 to 00ef5443 has its CatchHandler @ 00ef5690 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4678 to 00ef467f has its CatchHandler @ 00ef5684 */
    lVar26 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_1 + 0x130),0);
    fVar27 = (float)(iVar9 + -0x2e);
    if (lVar26 != 0) {
      if (iVar8 < 1) {
                    /* try { // try from 00ef4ac8 to 00ef4ad7 has its CatchHandler @ 00ef5588 */
        surface_GamePad__DrawImage((float)iVar8,fVar27,param_1,local_78,0x15);
      }
      else {
                    /* try { // try from 00ef46a0 to 00ef46b7 has its CatchHandler @ 00ef55a8 */
        surface_GamePad__DrawScaledImage
                  (0,fVar27,(float)(iVar8 + 0x54),0x42380000,lVar26,local_78,0x15);
      }
    }
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef544c to 00ef544f has its CatchHandler @ 00ef5674 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4ae0 to 00ef4ae7 has its CatchHandler @ 00ef5668 */
    lVar26 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
    if (lVar26 != 0) {
      if (iVar8 < 1) {
                    /* try { // try from 00ef4b1c to 00ef4b2b has its CatchHandler @ 00ef5584 */
        surface_GamePad__DrawImage((float)(iVar2 + -0x54),fVar27,param_1,local_78,0x16);
      }
      else {
                    /* try { // try from 00ef4b04 to 00ef4b17 has its CatchHandler @ 00ef55a4 */
        surface_GamePad__DrawScaledImage
                  ((float)(iVar2 + -0x54),fVar27,(float)(iVar8 + 0x54),0x42380000,lVar26,local_78,
                   0x16);
      }
    }
  }
  lVar26 = local_78;
  iVar8 = iVar8 + 3;
  iVar25 = iVar2 + -0x4b;
  iVar3 = iVar9 + -0x27;
  if ((long)uVar22 < lVar24) {
                    /* try { // try from 00ef4b4c to 00ef4b6b has its CatchHandler @ 00ef567c */
    surface_GamePad__AddTouch((float)iVar8,(float)iVar3,param_1,local_78,5,0x200000,1,0);
    lVar26 = local_78;
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5454 to 00ef5457 has its CatchHandler @ 00ef5664 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4b78 to 00ef4b7f has its CatchHandler @ 00ef565c */
    uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef4b80 to 00ef4baf has its CatchHandler @ 00ef5714 */
    iVar10 = java_lang_StringEx__Length(uVar17,0);
    surface_GamePad__AddTouch((float)iVar25,(float)iVar3,param_1,lVar26,1,0x400000,0 < iVar10,0);
                    /* try { // try from 00ef4bb0 to 00ef4bb7 has its CatchHandler @ 00ef563c */
    fVar27 = (float)surface_GamePad__GetSideViewRatio(param_1);
    iVar10 = -6;
    if (fVar27 <= 0.0) {
      iVar10 = -0x14;
    }
    iVar20 = -2;
    if (fVar27 <= 0.0) {
      iVar20 = 10;
    }
    if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
                    /* try { // try from 00ef4be8 to 00ef4beb has its CatchHandler @ 00ef57a4 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00ef4bec to 00ef4bf3 has its CatchHandler @ 00ef5630 */
    uVar15 = kairo_unity_util_Language__Japanese(0);
    if ((uVar15 & 1) == 0) {
                    /* try { // try from 00ef4ca8 to 00ef4cb3 has its CatchHandler @ 00ef55c8 */
      surface_GamePad__DrawImage
                ((float)(iVar20 + iVar8),(float)(iVar10 + iVar3),param_1,local_78,0x12);
    }
    else {
                    /* try { // try from 00ef4c0c to 00ef4c17 has its CatchHandler @ 00ef55cc */
      surface_GamePad__DrawImage
                ((float)(iVar20 + iVar8),(float)(iVar10 + iVar3),param_1,local_78,0x11);
    }
  }
  else {
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5448 to 00ef544b has its CatchHandler @ 00ef5678 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4c24 to 00ef4c2b has its CatchHandler @ 00ef566c */
    uVar17 = kairo_unity_ui_Canvas__GetSoftLabelL(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef4c2c to 00ef4c5f has its CatchHandler @ 00ef571c */
    iVar10 = java_lang_StringEx__Length(uVar17,0);
    surface_GamePad__AddTouch((float)iVar8,(float)iVar3,param_1,lVar26,0,0x200000,0 < iVar10,0);
    lVar26 = local_78;
    if (*(long *)(param_1 + 0x130) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5460 to 00ef5463 has its CatchHandler @ 00ef5644 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef4c6c to 00ef4c73 has its CatchHandler @ 00ef5638 */
    uVar17 = kairo_unity_ui_Canvas__GetSoftLabelR(*(long *)(param_1 + 0x130),0);
                    /* try { // try from 00ef4c74 to 00ef4ca3 has its CatchHandler @ 00ef5700 */
    iVar10 = java_lang_StringEx__Length(uVar17,0);
    surface_GamePad__AddTouch((float)iVar25,(float)iVar3,param_1,lVar26,1,0x400000,0 < iVar10,0);
  }
  lVar26 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar26 + 0xe0) == 0) {
                    /* try { // try from 00ef4cc8 to 00ef4ccb has its CatchHandler @ 00ef57a4 */
    thunk_FUN_00df405c();
    lVar26 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  }
  if (*(char *)(*(long *)(lVar26 + 0xb8) + 0x10) == '\0') {
LAB_00ef4d14:
    if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef542c to 00ef542f has its CatchHandler @ 00ef56c8 */
      FUN_00db0de4();
    }
  }
  else {
    if (*(char *)(param_1 + 0x174) != '\0') {
                    /* try { // try from 00ef4cf4 to 00ef4d13 has its CatchHandler @ 00ef55f0 */
      kairo_unity_surface_SurfaceBase__AddTouchComponent
                (param_1,0x14,iVar25,iVar9 + -0x81,*(undefined4 *)(param_1 + 0xbc),0x23,0,0,0);
      goto LAB_00ef4d14;
    }
    if (lVar11 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef54bc to 00ef54bf has its CatchHandler @ 00ef55b0 */
      FUN_00db0de4();
    }
    if ((*(char *)(lVar11 + 0x32) == '\0') && (*(char *)(lVar11 + 0x5c) == '\0')) {
      fVar27 = (float)iVar25;
                    /* try { // try from 00ef4df8 to 00ef4e17 has its CatchHandler @ 00ef5548 */
      surface_GamePad__AddTouch(fVar27,(float)(iVar9 + -0x45),param_1,local_78,0xc,0x10,1,0);
                    /* try { // try from 00ef4e24 to 00ef4e43 has its CatchHandler @ 00ef5544 */
      surface_GamePad__AddTouch(fVar27,(float)(iVar9 + -99),param_1,local_78,0xe,0,1,0);
                    /* try { // try from 00ef4e50 to 00ef4e83 has its CatchHandler @ 00ef555c */
      surface_GamePad__AddTouch(fVar27,(float)(iVar9 + -0x81),param_1,local_78,0x14,0,1,0);
      puVar6 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      lVar26 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      if (*(int *)(lVar26 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar26 = *(long *)puVar6;
      }
      if (*(char *)(*(long *)(lVar26 + 0xb8) + 0x30) != '\0') {
                    /* try { // try from 00ef4e9c to 00ef4ebb has its CatchHandler @ 00ef5524 */
        surface_GamePad__AddTouch((float)iVar8,(float)(iVar9 + -99),param_1,local_78,0x13,0,1,0);
      }
                    /* try { // try from 00ef5214 to 00ef5233 has its CatchHandler @ 00ef5540 */
      surface_GamePad__AddTouch((float)iVar8,(float)(iVar9 + -0x45),param_1,local_78,0xb,1,1,0);
    }
  }
                    /* try { // try from 00ef4d1c to 00ef4d23 has its CatchHandler @ 00ef56f0 */
  plVar18 = (long *)kairo_unity_form_FormManagerBase__GetTopForm(lVar11,0);
  if (plVar18 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef5420 to 00ef5423 has its CatchHandler @ 00ef56e8 */
    FUN_00db0de4();
  }
  if (*(int *)(plVar18 + 2) == 4) {
    bVar4 = *(byte *)(*(long *)PTR_form_SubForm_TypeInfo_01fbf300 + 0x130);
    if ((*(byte *)(*plVar18 + 0x130) < bVar4) ||
       (*(long *)(*(long *)(*plVar18 + 200) + (ulong)bVar4 * 8 + -8) !=
        *(long *)PTR_form_SubForm_TypeInfo_01fbf300)) {
                    /* try { // try from 00ef5424 to 00ef542b has its CatchHandler @ 00ef56e0 */
                    /* WARNING: Subroutine does not return */
      FUN_00db1180(plVar18);
    }
                    /* try { // try from 00ef4d70 to 00ef4d7b has its CatchHandler @ 00ef5614 */
    plVar18 = (long *)form_SubForm__IsMenu(plVar18,0);
    if (((ulong)plVar18 & 1) != 0) {
                    /* try { // try from 00ef4d94 to 00ef4d9b has its CatchHandler @ 00ef55bc */
      surface_GamePad__DrawWatch((float)(iVar7 + 2),(float)(iVar9 + -0x3a),param_1,local_78);
                    /* try { // try from 00ef4db0 to 00ef4db7 has its CatchHandler @ 00ef55b8 */
      plVar18 = (long *)surface_GamePad__DrawBattery
                                  ((float)(iVar7 + -0x1a),(float)(iVar9 + -0x3b),param_1,local_78);
    }
  }
                    /* try { // try from 00ef4dc4 to 00ef4dcb has its CatchHandler @ 00ef56d8 */
  surface_GamePad__DrawVersion(plVar18,local_78,iVar2 + -0x2a,iVar9 + -0x3f,1);
LAB_00ef4fac:
  FUN_00c819ac(&local_a0);
  return;
}



// ==========================================================================================
// Function: surface_GamePad__DrawScaledImage
// Address: 00ef5874
// ==========================================================================================

void surface_GamePad__DrawScaledImage
               (float param_1,float param_2,undefined8 param_3,undefined8 param_4,undefined8 param_5
               ,long param_6,uint param_7)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  undefined *puVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  
  puVar7 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff727 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    DAT_020ff727 = 1;
  }
  lVar8 = *(long *)puVar7;
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar8 = *(long *)puVar7;
  }
  lVar9 = *(long *)(lVar8 + 0xb8);
  lVar8 = *(long *)(lVar9 + 0x20);
  if (lVar8 != 0) {
    if (*(uint *)(lVar8 + 0x18) <= param_7) {
LAB_00ef5a44:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar8 = *(long *)(lVar8 + (long)(int)param_7 * 8 + 0x20);
    if (lVar8 != 0) {
      uVar5 = *(uint *)(lVar8 + 0x18);
      if (uVar5 == 0) goto LAB_00ef5a44;
      lVar10 = *(long *)(lVar9 + 8);
      if (lVar10 != 0) {
        uVar6 = *(uint *)(lVar8 + 0x20);
        if (*(uint *)(lVar10 + 0x18) <= uVar6) goto LAB_00ef5a44;
        lVar10 = *(long *)(lVar10 + (long)(int)uVar6 * 8 + 0x20);
        if ((lVar10 != 0) && (lVar9 = *(long *)(lVar9 + 0x18), lVar9 != 0)) {
          if (((*(uint *)(lVar9 + 0x18) <= uVar6) || (((uVar5 < 2 || (uVar5 == 2)) || (uVar5 < 4))))
             || (((uVar5 == 4 || (uVar5 < 6)) || (uVar5 == 6)))) goto LAB_00ef5a44;
          if (param_6 != 0) {
            fVar11 = (float)*(int *)(lVar10 + 0x28) /
                     (float)*(int *)(lVar9 + (long)(int)uVar6 * 4 + 0x20);
            fVar13 = fVar11 * (float)*(int *)(lVar8 + 0x2c) + 0.5;
            fVar14 = fVar11 * (float)*(int *)(lVar8 + 0x30) + 0.5;
            fVar12 = fVar11 * (float)*(int *)(lVar8 + 0x34) + 0.5;
            fVar11 = fVar11 * (float)*(int *)(lVar8 + 0x38) + 0.5;
            iVar1 = -0x80000000;
            if (fVar13 != INFINITY) {
              iVar1 = (int)fVar13;
            }
            iVar2 = -0x80000000;
            if (fVar14 != INFINITY) {
              iVar2 = (int)fVar14;
            }
            iVar3 = -0x80000000;
            if (fVar12 != INFINITY) {
              iVar3 = (int)fVar12;
            }
            iVar4 = -0x80000000;
            if (fVar11 != INFINITY) {
              iVar4 = (int)fVar11;
            }
            kairo_unity_ui_Graphics__DrawScaledImage
                      ((float)*(int *)(lVar8 + 0x24) + param_1,
                       (float)*(int *)(lVar8 + 0x28) + param_2,param_3,param_4,param_6,lVar10,iVar1,
                       iVar2,iVar3,iVar4,0);
            return;
          }
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__DrawWatch
// Address: 00ef5a4c
// ==========================================================================================

void surface_GamePad__DrawWatch(float param_1,ulong param_2,undefined8 param_3,undefined8 param_4)

{
  bool bVar1;
  undefined *puVar2;
  bool bVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  undefined8 uVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  ulong uVar12;
  float fVar13;
  undefined4 local_64;
  
  puVar2 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff725 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_java_util_JDate_TypeInfo_01fbf748);
    FUN_00db0bbc(PTR_StringLiteral_1050_01fc08e8);
    DAT_020ff725 = 1;
  }
  lVar8 = *(long *)puVar2;
  local_64 = 0;
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar8);
    lVar8 = *(long *)puVar2;
  }
  if (*(long *)(*(long *)(lVar8 + 0xb8) + 0x50) == 0) {
    uVar7 = java_util_JCalendar__GetInstance(0);
    lVar8 = *(long *)puVar2;
    if (*(int *)(lVar8 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar8);
      lVar8 = *(long *)puVar2;
    }
    *(undefined8 *)(*(long *)(lVar8 + 0xb8) + 0x50) = uVar7;
  }
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar8);
    lVar8 = *(long *)puVar2;
  }
  lVar11 = *(long *)(*(long *)(lVar8 + 0xb8) + 0x50);
  lVar8 = java_lang_JSystem__CurrentTimeMillis(0);
  lVar9 = *(long *)puVar2;
  lVar10 = *(long *)(lVar9 + 0xb8);
  if (lVar8 < *(long *)(lVar10 + 0x58)) {
LAB_00ef5b78:
    if (lVar11 == 0) goto LAB_00ef5e10;
    java_util_JCalendar__SetTimeInMillis(lVar11,lVar8,0);
    iVar6 = Method_java_util_JCalendar_Get(lVar11,0xd,0);
    iVar4 = Method_java_util_JCalendar_Get(lVar11,0xe,0);
    lVar9 = *(long *)puVar2;
    if (*(int *)(lVar9 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar9);
      lVar9 = *(long *)puVar2;
    }
    lVar9 = *(long *)(lVar9 + 0xb8);
    lVar8 = (lVar8 - iVar6 * 1000) - (long)iVar4;
    *(long *)(lVar9 + 0x58) = lVar8;
    *(long *)(lVar9 + 0x60) = lVar8 + 60000;
  }
  else {
    if (*(int *)(lVar9 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar9);
      lVar10 = *(long *)(*(long *)puVar2 + 0xb8);
    }
    if (*(long *)(lVar10 + 0x60) <= lVar8) goto LAB_00ef5b78;
    if (lVar11 == 0) goto LAB_00ef5e10;
  }
  puVar2 = PTR_java_util_JDate_TypeInfo_01fbf748;
  uVar5 = Method_java_util_JCalendar_Get(lVar11,0xb,0);
  iVar6 = Method_java_util_JCalendar_Get(lVar11,0xc,0);
  lVar8 = java_util_JCalendar__GetInstance(0);
  uVar7 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  java_util_JDate___ctor(uVar7,0);
  if (lVar8 != 0) {
    *(undefined8 *)(lVar8 + 0x10) = uVar7;
    local_64 = Method_java_util_JCalendar_Get(lVar8,0xb,0);
    lVar8 = System_Int32__ToString(&local_64,0);
    if ((lVar8 == 0) ||
       (uVar12 = System_String__Equals(lVar8,*(undefined8 *)PTR_StringLiteral_1050_01fc08e8,0),
       (uVar12 & 1) != 0)) {
      if ((int)uVar5 < 0xc) {
        uVar7 = 0x17;
        uVar12 = param_2;
      }
      else {
        uVar7 = 0x18;
        uVar12 = (ulong)(uint)((float)param_2 + 5.0);
      }
      surface_GamePad__DrawImage(param_1 + -81.0,uVar12,param_3,param_4,uVar7);
      uVar5 = (int)uVar5 % 0xc;
    }
    uVar12 = (ulong)uVar5;
    fVar13 = 0.0;
    bVar3 = true;
    do {
      bVar1 = bVar3;
      surface_GamePad__DrawImage
                ((param_1 + -63.0 + 2.0) - fVar13,param_2,param_3,param_4,(int)uVar12 % 10 + 0x19);
      if ((int)uVar12 < 10) break;
      uVar12 = uVar12 / 10;
      fVar13 = 9.0;
      bVar3 = false;
    } while (bVar1);
    surface_GamePad__DrawImage(param_1 + -54.0 + 2.0,param_2,param_3,param_4,0x23);
    fVar13 = 0.0;
    bVar3 = true;
    do {
      bVar1 = bVar3;
      surface_GamePad__DrawImage
                ((param_1 + -40.0 + 2.0) - fVar13,param_2,param_3,param_4,iVar6 % 10 + 0x19);
      fVar13 = 9.0;
      bVar3 = false;
      iVar6 = iVar6 / 10;
    } while (bVar1);
    return;
  }
LAB_00ef5e10:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__DrawBattery
// Address: 00ef5e14
// ==========================================================================================

void surface_GamePad__DrawBattery
               (undefined8 param_1,undefined8 param_2,long param_3,undefined8 param_4)

{
  int iVar1;
  ulong uVar2;
  
  if (*(long *)(param_3 + 0x128) != 0) {
    uVar2 = kairo_unity_ui_IApplication__IsBatteryCharging(*(long *)(param_3 + 0x128),0);
    if ((uVar2 & 1) == 0) {
      if (*(long *)(param_3 + 0x128) == 0) goto LAB_00ef5ea0;
      iVar1 = kairo_unity_ui_IApplication__GetBattery(*(long *)(param_3 + 0x128),0);
      iVar1 = (iVar1 * 0xe) / 100 + 0x24;
    }
    else {
      iVar1 = 0x32;
    }
    surface_GamePad__DrawImage(param_1,param_2,param_3,param_4,iVar1);
    return;
  }
LAB_00ef5ea0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__DrawVersion
// Address: 00ef5ea4
// ==========================================================================================

void surface_GamePad__DrawVersion
               (undefined8 param_1,long param_2,int param_3,int param_4,ulong param_5)

{
  undefined *puVar1;
  undefined4 uVar2;
  long lVar3;
  long lVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined4 local_34;
  
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_020ff724 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_9549_01fc08f8);
    FUN_00db0bbc(PTR_StringLiteral_787_01fbf9c0);
    DAT_020ff724 = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  if (*(char *)(*(long *)(lVar3 + 0xb8) + 0x10) != '\0') {
    lVar3 = form_FormManager__GetInstance(0);
    if (lVar3 == 0) goto LAB_00ef6130;
    if (*(char *)(lVar3 + 0x5c) != '\0') {
      return;
    }
  }
  puVar1 = PTR_surface_GamePad_TypeInfo_01fc0860;
  lVar3 = *(long *)PTR_surface_GamePad_TypeInfo_01fc0860;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  if (*(char *)(*(long *)(lVar3 + 0xb8) + 0x48) == '\0') {
    return;
  }
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__GetOriginX(param_2,0);
    kairo_unity_ui_Graphics__GetOriginY(param_2,0);
    local_34 = 0x10d;
    lVar4 = System_Int32__ToString(&local_34,0);
    lVar3 = *(long *)PTR_StringLiteral_1_01fbf388;
    if (lVar4 != 0) {
      lVar3 = lVar4;
    }
    plVar5 = (long *)thunk_FUN_00e11c14(*(undefined8 *)
                                         PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    System_Text_StringBuilder___ctor(plVar5,lVar3,0);
    if (plVar5 != (long *)0x0) {
      Method_System_Text_StringBuilder_Insert
                (plVar5,1,*(undefined8 *)PTR_StringLiteral_787_01fbf9c0,0);
      uVar6 = (**(code **)(*plVar5 + 0x168))(plVar5,*(undefined8 *)(*plVar5 + 0x170));
      uVar6 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_9549_01fc08f8,uVar6,0);
      lVar3 = kairo_unity_ui_Graphics__GetFont(param_2,0,0);
      kairo_unity_ui_Graphics__SetFont(param_2,lVar3,0);
      kairo_unity_ui_Graphics__SetColor(param_2,0xff,0xff,0xff,0);
      if ((param_5 & 1) == 0) {
        kairo_unity_ui_Graphics__DrawString((float)param_3,(float)param_4,param_2,uVar6,2,0);
      }
      else {
        if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(0x1e,0x1e,0x1e,0);
        kairo_unity_ui_Graphics__DrawStringBold
                  ((float)param_3,(float)param_4,param_2,uVar6,uVar2,2,0);
      }
      if (lVar3 != 0) {
        kairo_unity_ui_Font__SetSize(lVar3,0,1,0);
        kairo_unity_ui_Graphics__SetFont(param_2,lVar3,0);
        return;
      }
    }
  }
LAB_00ef6130:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__GetDivisionArea
// Address: 00ef6134
// ==========================================================================================

void surface_GamePad__GetDivisionArea
               (float param_1,float param_2,float param_3,long param_4,undefined4 param_5,
               int param_6)

{
  undefined *puVar1;
  int iVar2;
  long lVar3;
  uint uVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff728 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff728 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  iVar2 = main_AppData__ClampMax(param_5,param_6 + -1,0);
  fVar5 = DAT_005bcf0c;
  if (param_6 + -1 == 0) {
    lVar3 = *(long *)(param_4 + 0x180);
    if (lVar3 == 0) {
LAB_00ef62bc:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar4 = (uint)*(undefined8 *)(lVar3 + 0x18);
    if ((uVar4 == 0) || (*(float *)(lVar3 + 0x20) = param_1, fVar6 = param_1, uVar4 == 1))
    goto LAB_00ef62b8;
  }
  else {
    lVar3 = *(long *)(param_4 + 0x180);
    if (lVar3 == 0) goto LAB_00ef62bc;
    uVar4 = (uint)*(undefined8 *)(lVar3 + 0x18);
    if (uVar4 == 0) goto LAB_00ef62b8;
    fVar7 = ((param_2 - param_1) - (float)(param_6 + -1) * param_3) / (float)param_6;
    fVar8 = (fVar7 + param_3) * (float)iVar2;
    fVar9 = fVar8 + DAT_005bcf0c;
    fVar6 = -2.147484e+09;
    if (fVar9 != INFINITY) {
      fVar6 = (float)(int)fVar9;
    }
    fVar6 = fVar6 + param_1;
    *(float *)(lVar3 + 0x20) = fVar6;
    if (uVar4 == 1) goto LAB_00ef62b8;
    fVar5 = fVar7 + fVar8 + fVar5;
    param_2 = -2.147484e+09;
    if (fVar5 != INFINITY) {
      param_2 = (float)(int)fVar5;
    }
    param_2 = param_2 + param_1;
  }
  *(float *)(lVar3 + 0x24) = param_2;
  if ((uVar4 != 1) && ((uVar4 != 0 && (2 < uVar4)))) {
    *(float *)(lVar3 + 0x28) = fVar6 + (param_2 - fVar6) * 0.5;
    return;
  }
LAB_00ef62b8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: surface_GamePad__IsSmallSideView
// Address: 00ef62c0
// ==========================================================================================

bool surface_GamePad__IsSmallSideView(void)

{
  float fVar1;
  
  fVar1 = (float)surface_GamePad__GetSideViewRatio();
  return 0.0 < fVar1;
}



// ==========================================================================================
// Function: surface_GamePad__GetSideViewRatio
// Address: 00ef62d8
// ==========================================================================================

float surface_GamePad__GetSideViewRatio(long param_1)

{
  undefined *puVar1;
  long lVar2;
  float fVar3;
  float fVar4;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff721 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff721 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar2 = surface_GameView__GetInstance();
  if (lVar2 != 0) {
    fVar3 = (float)(*(int *)(lVar2 + 0xbc) * 100) / *(float *)(lVar2 + 0xc4) + DAT_005bcfd0;
    fVar4 = DAT_005bcfb4;
    if (fVar3 != INFINITY) {
      fVar4 = (float)((int)fVar3 + -0xa4) / 240.0;
    }
    fVar3 = 0.0;
    if (fVar4 < DAT_005bcf10 && *(int *)(param_1 + 0x178) == 2) {
      fVar3 = fVar4;
    }
    return fVar3;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__GetGameWidth
// Address: 00ef63a4
// ==========================================================================================

int surface_GameView__GetGameWidth(long param_1)

{
  int iVar1;
  float fVar2;
  
  fVar2 = (float)(*(int *)(param_1 + 0xbc) * 100) / *(float *)(param_1 + 0xc4) + DAT_005bcfd0;
  iVar1 = -0x80000000;
  if (fVar2 != INFINITY) {
    iVar1 = (int)fVar2;
  }
  return iVar1;
}



// ==========================================================================================
// Function: surface_GamePad__DrawMiniSoftLabelImage
// Address: 00ef63e4
// ==========================================================================================

void surface_GamePad__DrawMiniSoftLabelImage
               (float param_1,float param_2,undefined8 param_3,long param_4,uint param_5)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  long lVar6;
  long lVar7;
  long lVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  
  puVar5 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff723 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    DAT_020ff723 = 1;
  }
  lVar6 = *(long *)puVar5;
  if (*(int *)(lVar6 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar6 = *(long *)puVar5;
  }
  lVar8 = *(long *)(*(long *)(lVar6 + 0xb8) + 0x20);
  if (lVar8 != 0) {
    if (param_5 < *(uint *)(lVar8 + 0x18)) {
      lVar8 = *(long *)(lVar8 + (long)(int)param_5 * 8 + 0x20);
      if (lVar8 == 0) goto LAB_00ef65d0;
      if (*(int *)(lVar8 + 0x18) != 0) {
        lVar6 = *(long *)(*(long *)(lVar6 + 0xb8) + 8);
        if (lVar6 == 0) goto LAB_00ef65d0;
        if (*(uint *)(lVar8 + 0x20) < *(uint *)(lVar6 + 0x18)) {
          lVar6 = *(long *)(lVar6 + (long)(int)*(uint *)(lVar8 + 0x20) * 8 + 0x20);
          fVar9 = (float)surface_GamePad__GetSideViewRatio(param_3);
          if ((5 < *(uint *)(lVar8 + 0x18)) && (*(uint *)(lVar8 + 0x18) != 6)) {
            if ((lVar6 != 0) &&
               (lVar7 = *(long *)(*(long *)(*(long *)puVar5 + 0xb8) + 0x18), lVar7 != 0)) {
              if (*(uint *)(lVar7 + 0x18) <= *(uint *)(lVar8 + 0x20)) goto LAB_00ef65cc;
              if (param_4 != 0) {
                fVar11 = (float)*(int *)(lVar6 + 0x28) /
                         (float)*(int *)(lVar7 + (long)(int)*(uint *)(lVar8 + 0x20) * 4 + 0x20);
                fVar14 = fVar9 * (float)*(int *)(lVar8 + 0x34);
                fVar9 = fVar9 * (float)*(int *)(lVar8 + 0x38);
                fVar10 = -2.147484e+09;
                if (fVar14 != INFINITY) {
                  fVar10 = (float)(int)fVar14;
                }
                fVar12 = fVar11 * (float)*(int *)(lVar8 + 0x2c) + 0.5;
                fVar15 = fVar11 * (float)*(int *)(lVar8 + 0x34) + 0.5;
                fVar13 = fVar11 * (float)*(int *)(lVar8 + 0x30) + 0.5;
                fVar14 = -2.147484e+09;
                if (fVar9 != INFINITY) {
                  fVar14 = (float)(int)fVar9;
                }
                iVar1 = -0x80000000;
                if (fVar12 != INFINITY) {
                  iVar1 = (int)fVar12;
                }
                fVar9 = fVar11 * (float)*(int *)(lVar8 + 0x38) + 0.5;
                iVar2 = -0x80000000;
                if (fVar13 != INFINITY) {
                  iVar2 = (int)fVar13;
                }
                iVar3 = -0x80000000;
                if (fVar15 != INFINITY) {
                  iVar3 = (int)fVar15;
                }
                iVar4 = -0x80000000;
                if (fVar9 != INFINITY) {
                  iVar4 = (int)fVar9;
                }
                kairo_unity_ui_Graphics__DrawScaledImage
                          ((float)*(int *)(lVar8 + 0x24) + param_1,
                           (float)*(int *)(lVar8 + 0x28) + param_2,fVar10,fVar14,param_4,lVar6,iVar1
                           ,iVar2,iVar3,iVar4,0);
                return;
              }
            }
            goto LAB_00ef65d0;
          }
        }
      }
    }
LAB_00ef65cc:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ef65d0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GamePad__RotateClear
// Address: 00ef65d4
// ==========================================================================================

void surface_GamePad__RotateClear(void)

{
  return;
}



// ==========================================================================================
// Function: surface_GamePad__GetLayoutMode
// Address: 00ef65d8
// ==========================================================================================

undefined4 surface_GamePad__GetLayoutMode(long param_1)

{
  return *(undefined4 *)(param_1 + 0x170);
}



// ==========================================================================================
// Function: surface_GamePad__SetOptionPage
// Address: 00ef65e0
// ==========================================================================================

void surface_GamePad__SetOptionPage(long param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x168) = param_2;
  return;
}



// ==========================================================================================
// Function: surface_GamePad__GetOptionPage
// Address: 00ef65e8
// ==========================================================================================

undefined4 surface_GamePad__GetOptionPage(long param_1)

{
  return *(undefined4 *)(param_1 + 0x168);
}



// ==========================================================================================
// Function: surface_GamePad___cctor
// Address: 00ef65f0
// ==========================================================================================

void surface_GamePad___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  long lVar7;
  undefined8 uVar8;
  long lVar9;
  long lVar10;
  uint uVar11;
  undefined4 uVar12;
  
  puVar1 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_020ff72a & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_int_____TypeInfo_01fbf5e8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__060AB557A62D0EBD5AE7184CEFB4AA7D73A01B9EB519BDFF1970621B3354A068_01fc0900
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__094BD93212DD6BF3D5AF5EE916EF63832FFA44F24AB6AAA090EA89503DD47961_01fc0908
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__114784B0A3F7D86055349B707B990F53003D6FFEE4C9F85617FCC43EE1BC38E2_01fc0910
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__16CB64EBB0C81B2664913F9EF09D3C10029112ABE891FF3280151C288DF2DC2B_01fc0918
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__17406A3EE4DB453B8554C3E8BF51B7766A4398218D72AA24AEFA09948EB67AC0_01fc0920
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__189A6FB253DB78812F7A25EEE2AA9FD0701F09A79A99C7ED4A4AD3F0E8C600D6_01fc0928
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__203460CE0D6DC30740C452FD26AD0B2F59EEA27A10DFFF23AE94121351875F92_01fc0930
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__216B53D2A9BB40BCCEB5230A154C39CBC50274665DC04984EA72CBAD4C3953AE_01fc0938
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__21B384FAF1F2192AFB095066628E1A3115BB7D5895E3F663501F95E457890901_01fc0940
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__274B84432B576258556A976F8B783318DDCECA254AF0E02A9C058E1981F22893_01fc0948
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__27BF9E3866E6327F60A29B565216F4BB62983D4AD2DAD38F006D1AD2B75F70FA_01fc0950
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__287A927D57CD7EEC7DAAD813814982B03C48FE1D151321A3F68A7C19475DA56B_01fc0958
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__313AAE015B4CC379DD3AAFD8B7F39726A851EB1449651A51F3B0AFEC388D0D9E_01fc0960
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__348D8CEDFC79361A3ABC0B3B774B5022055F097699DC08A77549C3F9C4EA6091_01fc0968
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3AC1F097348D392151B97B2D51BA2E3456B72D18DB815316D52A4FF00947A2A8_01fc0970
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3ADA5114435DD38EB13B94789F29106985FE5461C271B0D864370F4C9B02A7CA_01fc0978
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3CD2185A3849F297CE1ED138DCF84AEED165FE6F51352F1FF5E6952578131004_01fc0980
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3D9C2CA6214621E7DD825BC792B6500D0BFA266F3B1E37C3565377C309063242_01fc0988
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__4112FD5FE18D3589EC0D07A30D7E2476E474468414E7BF0D4BCDDB4E1C713751_01fc0990
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__4CB343473449F7A07F1788DB581FA4837BBC8F7946F7932EA431FE9F5EC3A524_01fc0998
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__4F34C1C1C5D96909887D2D39CBB4055DA8E52F55B204AB6646C0A3D352AE8277_01fc09a0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__50EBE7C53B9A0CF7D1FBBD330707CC44FF6C3B5C872E94F3CB0F27D8D38892D5_01fc09a8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__554CEA5AF069A94890BFA3B7DE6A8991CEC6F25AD17FD042837DB26D019860F8_01fc09b0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__57CA3A7CAF60EEE24B256889BE63B46FF64645CA1F80BCFCB61F4E9D9F634905_01fc09b8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__61C8F29F25B2556C4B3C21D278EA7D25D573B297827F2662F18321F07F3A4AD0_01fc09c0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__668DE511316ACAF91DC1A1B61FA1870F519B0E3CFEC02CAF5002A5DDEB548053_01fc09c8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__66E151B81B945E1C419502A6835349069B29CBFF628C912FC2363E2A1D4175B5_01fc09d0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__6A2DB42891CCCD310B228A75377EE0EC0A17F6F60DE070335512257A13A940F0_01fc09d8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__715E14060E262CA477AF59058CF0E790D3A0493B150AD9D3E52610BA831CE1DE_01fc09e0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__79AB8B2B0B25720333466ED03E4041240C2FB50764F8023078DCE5031EFFF024_01fc09e8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__8F6973E90679A609BD85E05012CAB30F60AAD027B9687A7CAB6CEA6A4D1747CD_01fc09f0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__90353B9B897E72A312F3AF5F499FC2BF391B1983D1A9B36963B027CCE7AB0F85_01fc09f8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__99E522D6FE5873BE685531599A2EC420A3DED38E4FC188E3CC06D2D105CBE328_01fc0a00
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__9C071F45BBD9B0789704ECF7927830E67FB7FABBBF35302B685AFEBD0FA5C0C1_01fc0a08
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__9CFA9840F2A5F87C88AB6AF0C8D68865DA453643894458A285FAAA0297848B64_01fc0a10
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__9E5130B0D0019F433385EB1D909811CD2E74A5972E2C43CB2EC8521419782685_01fc0a18
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A413DA46E3E163AE1A3D77A2992CC655F0B3C84A550C9FA80C474EDD5BCDB58F_01fc0a20
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A4D31CB62DBBCCF81FE09E09D27E110749A044C8C770222A751694485265C85F_01fc0a28
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A99CF00D5447D8E39EED810C34DFDD6C96CC4BD2F1283C16133742D322698827_01fc0a30
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__AA9514025D1ADCB7EEE763C16BD88D909975CC79FA1B14B4AA4FBA50336464D7_01fc0a38
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__B02A6EC21F488113766CAE3B38BBA5A9684C54AB3427C22CC69DDB374D7CAED6_01fc0a40
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__B52816EE3069EAF226E55961CE9DCB3858BA66FBFAFC3C6AFC6F60E25B90DB37_01fc0a48
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__BC4641709FE115FAF8F414FF54DCD15B725823E11736BAA799B7B7F2BAFF9290_01fc0a50
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C83F38A6ED69DC4A17C8C317AEA3D16865BB2ACDB967BA74BD3FA61544A08EA2_01fc0a58
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C875D29459E5EAC22E36E3A26EA5E5DA96CDC72E721A530154BBA8A6E86833B4_01fc0a60
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C9226542048CB7D607CAC565FB0F9C49DFEB9F35CC24321FADFC0023811B22F5_01fc0a68
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C92C1A800BC8F404A17138A5E171E52B1DF11782D29ECCBE54829FA1361A9876_01fc0a70
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__CA7A627BF653F72FEA13FE97A0A77133D2C97BBFFF81D65A352CA2310CD813FB_01fc0a78
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__CC27E476918BB62D2D58FD4B2005B6D58F1B12826B112E84F33DFA4A2D98C771_01fc0a80
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__CD244CAB0BFE01176EAF96189CAFAE1331E89A2D9F767484E20A391C1BEA775D_01fc0a88
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__D0D92D6D61F7C44AF54FF0D407CDFAC79257AC760B2FAE619C8254A47C9B9EE2_01fc0a90
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__D64AE924DFC9D30D844A0532A1C9B6655639A19679E43DA38B953204E910B21E_01fc0a98
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__D84BC72F0EAD9B56BE42E6E7891E0A6A1405E4D0BEB931A163AD6FCA813B313B_01fc0aa0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__D91F3AF9B89CB5F698FF6F6B570E9292C4E6D3F43854354E5481DDD93621BAC5_01fc0aa8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E2F48059EB4DBDB2CECF62A0116F0553650787BCE9708EC3DDC1149BAABEE2A0_01fc0ab0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E332F898B41E5EBFB13C3A14717D372BD84F360EA24A3289F9749E93C5D1A200_01fc0ab8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E88E80E748494A4AC3ADB68D1D573FD8FE383B7075EEA7BB5A142817611BF141_01fc0ac0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E8FB1EAA0F93BEC300FA4BE58105410CBDEA071CF7248DD26E46C12E3DDB31E9_01fc0ac8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__F6CD20E89CD0E56E95EA9F2B9BECDBAFB2A156DFBC566840DE4B9DC20311EF01_01fc0ad0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__FB571B50B3567B5B7335992C5D52C69524A97FA0691862BD42B1D2114459AAA8_01fc0ad8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__FBB78CFD71C961DA104EF4F453BD2D3409645E983CD794565ACD38944A428DA5_01fc0ae0
                );
    FUN_00db0bbc(PTR_StringLiteral_6819_01fc0ae8);
    FUN_00db0bbc(PTR_StringLiteral_9591_01fc0af0);
    FUN_00db0bbc(PTR_StringLiteral_9074_01fc0af8);
    FUN_00db0bbc(PTR_StringLiteral_8131_01fc0b00);
    FUN_00db0bbc(PTR_StringLiteral_12460_01fc0b08);
    FUN_00db0bbc(PTR_StringLiteral_8130_01fc0b10);
    DAT_020ff72a = 1;
  }
  lVar7 = FUN_00db0c30(*(undefined8 *)puVar1,3);
  if (lVar7 != 0) {
    uVar11 = *(uint *)(lVar7 + 0x18);
    if (((uVar11 != 0) &&
        (*(undefined8 *)(lVar7 + 0x20) = *(undefined8 *)PTR_StringLiteral_8130_01fc0b10, uVar11 != 1
        )) && (*(undefined8 *)(lVar7 + 0x28) = *(undefined8 *)PTR_StringLiteral_8131_01fc0b00,
              puVar5 = PTR_surface_GamePad_TypeInfo_01fc0860, 2 < uVar11)) {
      *(undefined8 *)(lVar7 + 0x30) = *(undefined8 *)PTR_StringLiteral_6819_01fc0ae8;
      puVar3 = PTR_int___TypeInfo_01fbf560;
      *(long *)(*(long *)(*(long *)puVar5 + 0xb8) + 0x10) = lVar7;
      puVar2 = 
      PTR_Field__PrivateImplementationDetails__348D8CEDFC79361A3ABC0B3B774B5022055F097699DC08A77549C3F9C4EA6091_01fc0968
      ;
      puVar4 = PTR_int_____TypeInfo_01fbf5e8;
      uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar8,*(undefined8 *)puVar2,0);
      *(undefined8 *)(*(long *)(*(long *)puVar5 + 0xb8) + 0x18) = uVar8;
      lVar7 = FUN_00db0c30(*(undefined8 *)puVar4,0x33);
      lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,7);
      if (lVar9 == 0) goto LAB_00ef7a90;
      if ((5 < *(uint *)(lVar9 + 0x18)) &&
         (*(undefined4 *)(lVar9 + 0x34) = 0x140, *(uint *)(lVar9 + 0x18) != 6)) {
        *(undefined4 *)(lVar9 + 0x38) = 0xa0;
        if (lVar7 == 0) goto LAB_00ef7a90;
        if (*(int *)(lVar7 + 0x18) != 0) {
          *(long *)(lVar7 + 0x20) = lVar9;
          puVar2 = 
          PTR_Field__PrivateImplementationDetails__A413DA46E3E163AE1A3D77A2992CC655F0B3C84A550C9FA80C474EDD5BCDB58F_01fc0a20
          ;
          uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
          Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                    (uVar8,*(undefined8 *)puVar2,0);
          if (1 < *(uint *)(lVar7 + 0x18)) {
            *(undefined8 *)(lVar7 + 0x28) = uVar8;
            puVar2 = 
            PTR_Field__PrivateImplementationDetails__57CA3A7CAF60EEE24B256889BE63B46FF64645CA1F80BCFCB61F4E9D9F634905_01fc09b8
            ;
            uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
            Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                      (uVar8,*(undefined8 *)puVar2,0);
            if (2 < *(uint *)(lVar7 + 0x18)) {
              *(undefined8 *)(lVar7 + 0x30) = uVar8;
              puVar2 = 
              PTR_Field__PrivateImplementationDetails__E332F898B41E5EBFB13C3A14717D372BD84F360EA24A3289F9749E93C5D1A200_01fc0ab8
              ;
              uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
              Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                        (uVar8,*(undefined8 *)puVar2,0);
              if (3 < *(uint *)(lVar7 + 0x18)) {
                *(undefined8 *)(lVar7 + 0x38) = uVar8;
                puVar2 = 
                PTR_Field__PrivateImplementationDetails__CD244CAB0BFE01176EAF96189CAFAE1331E89A2D9F767484E20A391C1BEA775D_01fc0a88
                ;
                uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                          (uVar8,*(undefined8 *)puVar2,0);
                if (4 < *(uint *)(lVar7 + 0x18)) {
                  *(undefined8 *)(lVar7 + 0x40) = uVar8;
                  puVar2 = 
                  PTR_Field__PrivateImplementationDetails__203460CE0D6DC30740C452FD26AD0B2F59EEA27A10DFFF23AE94121351875F92_01fc0930
                  ;
                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                            (uVar8,*(undefined8 *)puVar2,0);
                  if (5 < *(uint *)(lVar7 + 0x18)) {
                    *(undefined8 *)(lVar7 + 0x48) = uVar8;
                    puVar2 = 
                    PTR_Field__PrivateImplementationDetails__4112FD5FE18D3589EC0D07A30D7E2476E474468414E7BF0D4BCDDB4E1C713751_01fc0990
                    ;
                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                    Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                              (uVar8,*(undefined8 *)puVar2,0);
                    if (6 < *(uint *)(lVar7 + 0x18)) {
                      *(undefined8 *)(lVar7 + 0x50) = uVar8;
                      lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                      puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
                      if (lVar9 == 0) goto LAB_00ef7a90;
                      uVar11 = (uint)*(undefined8 *)(lVar9 + 0x18);
                      if (4 < uVar11) {
                        *(undefined4 *)(lVar9 + 0x30) = 0xc6;
                        if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
                          thunk_FUN_00df405c();
                          uVar11 = (uint)*(undefined8 *)(lVar9 + 0x18);
                        }
                        if (5 < uVar11) {
                          uVar12 = 0x4b;
                          if (*(char *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x10) != '\0') {
                            uVar12 = 0x40;
                          }
                          *(undefined4 *)(lVar9 + 0x34) = uVar12;
                          if (uVar11 != 6) {
                            *(undefined4 *)(lVar9 + 0x38) = 0x14;
                            if (7 < *(uint *)(lVar7 + 0x18)) {
                              *(long *)(lVar7 + 0x58) = lVar9;
                              puVar6 = 
                              PTR_Field__PrivateImplementationDetails__50EBE7C53B9A0CF7D1FBBD330707CC44FF6C3B5C872E94F3CB0F27D8D38892D5_01fc09a8
                              ;
                              lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                              Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                        (lVar9,*(undefined8 *)puVar6,0);
                              lVar10 = *(long *)puVar2;
                              if (*(int *)(lVar10 + 0xe0) == 0) {
                                thunk_FUN_00df405c();
                                lVar10 = *(long *)puVar2;
                              }
                              uVar12 = 0x52;
                              if (*(char *)(*(long *)(lVar10 + 0xb8) + 0x10) != '\0') {
                                uVar12 = 0x40;
                              }
                              if (lVar9 == 0) goto LAB_00ef7a90;
                              if (5 < *(uint *)(lVar9 + 0x18)) {
                                *(undefined4 *)(lVar9 + 0x34) = uVar12;
                                if (8 < *(uint *)(lVar7 + 0x18)) {
                                  *(long *)(lVar7 + 0x60) = lVar9;
                                  puVar6 = 
                                  PTR_Field__PrivateImplementationDetails__E8FB1EAA0F93BEC300FA4BE58105410CBDEA071CF7248DD26E46C12E3DDB31E9_01fc0ac8
                                  ;
                                  lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                            (lVar9,*(undefined8 *)puVar6,0);
                                  lVar10 = *(long *)puVar2;
                                  if (*(int *)(lVar10 + 0xe0) == 0) {
                                    thunk_FUN_00df405c();
                                    lVar10 = *(long *)puVar2;
                                  }
                                  uVar12 = 0x49;
                                  if (*(char *)(*(long *)(lVar10 + 0xb8) + 0x10) != '\0') {
                                    uVar12 = 0x40;
                                  }
                                  if (lVar9 == 0) goto LAB_00ef7a90;
                                  if (5 < *(uint *)(lVar9 + 0x18)) {
                                    *(undefined4 *)(lVar9 + 0x34) = uVar12;
                                    if (9 < *(uint *)(lVar7 + 0x18)) {
                                      *(long *)(lVar7 + 0x68) = lVar9;
                                      puVar2 = 
                                      PTR_Field__PrivateImplementationDetails__21B384FAF1F2192AFB095066628E1A3115BB7D5895E3F663501F95E457890901_01fc0940
                                      ;
                                      uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                (uVar8,*(undefined8 *)puVar2,0);
                                      if (10 < *(uint *)(lVar7 + 0x18)) {
                                        *(undefined8 *)(lVar7 + 0x70) = uVar8;
                                        puVar2 = 
                                        PTR_Field__PrivateImplementationDetails__9E5130B0D0019F433385EB1D909811CD2E74A5972E2C43CB2EC8521419782685_01fc0a18
                                        ;
                                        uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                  (uVar8,*(undefined8 *)puVar2,0);
                                        if (0xb < *(uint *)(lVar7 + 0x18)) {
                                          *(undefined8 *)(lVar7 + 0x78) = uVar8;
                                          puVar2 = 
                                          PTR_Field__PrivateImplementationDetails__D84BC72F0EAD9B56BE42E6E7891E0A6A1405E4D0BEB931A163AD6FCA813B313B_01fc0aa0
                                          ;
                                          uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                          Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                    (uVar8,*(undefined8 *)puVar2,0);
                                          if (0xc < *(uint *)(lVar7 + 0x18)) {
                                            *(undefined8 *)(lVar7 + 0x80) = uVar8;
                                            puVar2 = 
                                            PTR_Field__PrivateImplementationDetails__B52816EE3069EAF226E55961CE9DCB3858BA66FBFAFC3C6AFC6F60E25B90DB37_01fc0a48
                                            ;
                                            uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                            Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                      (uVar8,*(undefined8 *)puVar2,0);
                                            if (0xd < *(uint *)(lVar7 + 0x18)) {
                                              *(undefined8 *)(lVar7 + 0x88) = uVar8;
                                              puVar2 = 
                                              PTR_Field__PrivateImplementationDetails__C83F38A6ED69DC4A17C8C317AEA3D16865BB2ACDB967BA74BD3FA61544A08EA2_01fc0a58
                                              ;
                                              uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                              Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                        (uVar8,*(undefined8 *)puVar2,0);
                                              if (0xe < *(uint *)(lVar7 + 0x18)) {
                                                *(undefined8 *)(lVar7 + 0x90) = uVar8;
                                                puVar2 = 
                                                PTR_Field__PrivateImplementationDetails__E2F48059EB4DBDB2CECF62A0116F0553650787BCE9708EC3DDC1149BAABEE2A0_01fc0ab0
                                                ;
                                                uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                          (uVar8,*(undefined8 *)puVar2,0);
                                                if (0xf < *(uint *)(lVar7 + 0x18)) {
                                                  *(undefined8 *)(lVar7 + 0x98) = uVar8;
                                                  puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__8F6973E90679A609BD85E05012CAB30F60AAD027B9687A7CAB6CEA6A4D1747CD_01fc09f0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x10 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xa0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__C875D29459E5EAC22E36E3A26EA5E5DA96CDC72E721A530154BBA8A6E86833B4_01fc0a60
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x11 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xa8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__3CD2185A3849F297CE1ED138DCF84AEED165FE6F51352F1FF5E6952578131004_01fc0980
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x12 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xb0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__61C8F29F25B2556C4B3C21D278EA7D25D573B297827F2662F18321F07F3A4AD0_01fc09c0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x13 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xb8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__114784B0A3F7D86055349B707B990F53003D6FFEE4C9F85617FCC43EE1BC38E2_01fc0910
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x14 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xc0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__9C071F45BBD9B0789704ECF7927830E67FB7FABBBF35302B685AFEBD0FA5C0C1_01fc0a08
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x15 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 200) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__FBB78CFD71C961DA104EF4F453BD2D3409645E983CD794565ACD38944A428DA5_01fc0ae0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x16 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xd0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__E88E80E748494A4AC3ADB68D1D573FD8FE383B7075EEA7BB5A142817611BF141_01fc0ac0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x17 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xd8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__17406A3EE4DB453B8554C3E8BF51B7766A4398218D72AA24AEFA09948EB67AC0_01fc0920
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x18 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xe0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__4CB343473449F7A07F1788DB581FA4837BBC8F7946F7932EA431FE9F5EC3A524_01fc0998
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x19 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xe8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__BC4641709FE115FAF8F414FF54DCD15B725823E11736BAA799B7B7F2BAFF9290_01fc0a50
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1a < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xf0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__90353B9B897E72A312F3AF5F499FC2BF391B1983D1A9B36963B027CCE7AB0F85_01fc09f8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1b < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xf8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__C9226542048CB7D607CAC565FB0F9C49DFEB9F35CC24321FADFC0023811B22F5_01fc0a68
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1c < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x100) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__094BD93212DD6BF3D5AF5EE916EF63832FFA44F24AB6AAA090EA89503DD47961_01fc0908
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1d < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x108) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__216B53D2A9BB40BCCEB5230A154C39CBC50274665DC04984EA72CBAD4C3953AE_01fc0938
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1e < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x110) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__CC27E476918BB62D2D58FD4B2005B6D58F1B12826B112E84F33DFA4A2D98C771_01fc0a80
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x1f < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x118) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__F6CD20E89CD0E56E95EA9F2B9BECDBAFB2A156DFBC566840DE4B9DC20311EF01_01fc0ad0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x20 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x120) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__060AB557A62D0EBD5AE7184CEFB4AA7D73A01B9EB519BDFF1970621B3354A068_01fc0900
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x21 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x128) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__274B84432B576258556A976F8B783318DDCECA254AF0E02A9C058E1981F22893_01fc0948
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x22 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x130) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__4F34C1C1C5D96909887D2D39CBB4055DA8E52F55B204AB6646C0A3D352AE8277_01fc09a0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x23 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x138) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__189A6FB253DB78812F7A25EEE2AA9FD0701F09A79A99C7ED4A4AD3F0E8C600D6_01fc0928
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x24 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x140) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__715E14060E262CA477AF59058CF0E790D3A0493B150AD9D3E52610BA831CE1DE_01fc09e0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x25 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x148) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__AA9514025D1ADCB7EEE763C16BD88D909975CC79FA1B14B4AA4FBA50336464D7_01fc0a38
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x26 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x150) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__6A2DB42891CCCD310B228A75377EE0EC0A17F6F60DE070335512257A13A940F0_01fc09d8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x27 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x158) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__66E151B81B945E1C419502A6835349069B29CBFF628C912FC2363E2A1D4175B5_01fc09d0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x28 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x160) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__27BF9E3866E6327F60A29B565216F4BB62983D4AD2DAD38F006D1AD2B75F70FA_01fc0950
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x29 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x168) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__79AB8B2B0B25720333466ED03E4041240C2FB50764F8023078DCE5031EFFF024_01fc09e8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2a < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x170) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__D0D92D6D61F7C44AF54FF0D407CDFAC79257AC760B2FAE619C8254A47C9B9EE2_01fc0a90
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2b < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x178) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__668DE511316ACAF91DC1A1B61FA1870F519B0E3CFEC02CAF5002A5DDEB548053_01fc09c8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2c < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x180) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__D64AE924DFC9D30D844A0532A1C9B6655639A19679E43DA38B953204E910B21E_01fc0a98
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2d < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x188) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__313AAE015B4CC379DD3AAFD8B7F39726A851EB1449651A51F3B0AFEC388D0D9E_01fc0960
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2e < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 400) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__3ADA5114435DD38EB13B94789F29106985FE5461C271B0D864370F4C9B02A7CA_01fc0978
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x2f < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x198) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__3AC1F097348D392151B97B2D51BA2E3456B72D18DB815316D52A4FF00947A2A8_01fc0970
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x30 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x1a0) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__B02A6EC21F488113766CAE3B38BBA5A9684C54AB3427C22CC69DDB374D7CAED6_01fc0a40
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x31 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x1a8) = uVar8;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__287A927D57CD7EEC7DAAD813814982B03C48FE1D151321A3F68A7C19475DA56B_01fc0958
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (0x32 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x1b0) = uVar8;
                                                    *(long *)(*(long *)(*(long *)puVar5 + 0xb8) +
                                                             0x20) = lVar7;
                                                    puVar2 = 
                                                  PTR_Field__PrivateImplementationDetails__16CB64EBB0C81B2664913F9EF09D3C10029112ABE891FF3280151C288DF2DC2B_01fc0918
                                                  ;
                                                  lVar7 = FUN_00db0c30(*(undefined8 *)puVar4,0x17);
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (lVar7 == 0) goto LAB_00ef7a90;
                                                  if (*(int *)(lVar7 + 0x18) != 0) {
                                                    *(undefined8 *)(lVar7 + 0x20) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__3D9C2CA6214621E7DD825BC792B6500D0BFA266F3B1E37C3565377C309063242_01fc0988
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (1 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x28) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (2 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x30) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (3 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x38) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__CA7A627BF653F72FEA13FE97A0A77133D2C97BBFFF81D65A352CA2310CD813FB_01fc0a78
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (4 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x40) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar2,0);
                                                  if (5 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x48) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__A99CF00D5447D8E39EED810C34DFDD6C96CC4BD2F1283C16133742D322698827_01fc0a30
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (6 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x50) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__99E522D6FE5873BE685531599A2EC420A3DED38E4FC188E3CC06D2D105CBE328_01fc0a00
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (7 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x58) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__FB571B50B3567B5B7335992C5D52C69524A97FA0691862BD42B1D2114459AAA8_01fc0ad8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (8 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x60) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__9CFA9840F2A5F87C88AB6AF0C8D68865DA453643894458A285FAAA0297848B64_01fc0a10
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (9 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x68) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__A4D31CB62DBBCCF81FE09E09D27E110749A044C8C770222A751694485265C85F_01fc0a28
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (10 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x70) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__C92C1A800BC8F404A17138A5E171E52B1DF11782D29ECCBE54829FA1361A9876_01fc0a70
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0xb < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x78) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0xc < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x80) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0xd < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x88) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0xe < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x90) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0xf < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0x98) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x10 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xa0) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x11 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xa8) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x12 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xb0) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x13 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xb8) = uVar8;
                                                    uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                                                                        
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x14 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xc0) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__D91F3AF9B89CB5F698FF6F6B570E9292C4E6D3F43854354E5481DDD93621BAC5_01fc0aa8
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x15 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 200) = uVar8;
                                                    puVar4 = 
                                                  PTR_Field__PrivateImplementationDetails__554CEA5AF069A94890BFA3B7DE6A8991CEC6F25AD17FD042837DB26D019860F8_01fc09b0
                                                  ;
                                                  uVar8 = FUN_00db0c30(*(undefined8 *)puVar3,7);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar8,*(undefined8 *)puVar4,0);
                                                  if (0x16 < *(uint *)(lVar7 + 0x18)) {
                                                    *(undefined8 *)(lVar7 + 0xd0) = uVar8;
                                                    uVar8 = DAT_005bca38;
                                                    lVar9 = *(long *)(*(long *)puVar5 + 0xb8);
                                                    *(long *)(lVar9 + 0x28) = lVar7;
                                                    *(undefined8 *)(lVar9 + 0x30) = uVar8;
                                                    *(undefined4 *)(lVar9 + 0x38) = 0x28;
                                                    lVar7 = FUN_00db0c30(*(undefined8 *)puVar1,3);
                                                    if (lVar7 == 0) goto LAB_00ef7a90;
                                                    uVar11 = *(uint *)(lVar7 + 0x18);
                                                    if (((uVar11 != 0) &&
                                                        (*(undefined8 *)(lVar7 + 0x20) =
                                                              *(undefined8 *)
                                                               PTR_StringLiteral_12460_01fc0b08,
                                                        uVar11 != 1)) &&
                                                       (*(undefined8 *)(lVar7 + 0x28) =
                                                             *(undefined8 *)
                                                              PTR_StringLiteral_9074_01fc0af8,
                                                       2 < uVar11)) {
                                                      *(undefined8 *)(lVar7 + 0x30) =
                                                           *(undefined8 *)
                                                            PTR_StringLiteral_9591_01fc0af0;
                                                      lVar9 = *(long *)(*(long *)puVar5 + 0xb8);
                                                      *(long *)(lVar9 + 0x40) = lVar7;
                                                      *(undefined *)(lVar9 + 0x48) = 1;
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
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00ef7a90:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView___ctor
// Address: 00ef7a94
// ==========================================================================================

void surface_GameView___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined8 uVar6;
  long lVar7;
  undefined4 uVar8;
  
  puVar5 = PTR_Method_java_util_Vector_int_____ctor_01fc0b20;
  puVar4 = PTR_java_util_Vector_int____TypeInfo_01fc0b18;
  puVar3 = PTR_int___TypeInfo_01fbf560;
  puVar1 = PTR_kairo_unity_surface_SurfaceBase_TypeInfo_01fbf4c8;
  if ((DAT_020ff72b & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceBase_TypeInfo_01fbf4c8);
    FUN_00db0bbc(PTR_Method_java_util_Vector_int_____ctor_01fc0b20);
    FUN_00db0bbc(PTR_java_util_Vector_int____TypeInfo_01fc0b18);
    DAT_020ff72b = 1;
  }
  puVar2 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  Method_java_util_Vector_object___ctor(uVar6,*(undefined8 *)puVar5);
  *(undefined8 *)(param_1 + 0x198) = uVar6;
  uVar6 = FUN_00db0c30(*(undefined8 *)puVar3,2);
  *(undefined8 *)(param_1 + 0x1a8) = uVar6;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_surface_SurfaceBase___ctor(param_1,0);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar1 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  lVar7 = *(long *)puVar2;
  if (*(int *)(lVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar7 = *(long *)puVar2;
  }
  *(undefined8 *)(param_1 + 0x128) = **(undefined8 **)(lVar7 + 0xb8);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_ui_Canvas__GetInstance(0);
  *(undefined8 *)(param_1 + 0x130) = uVar6;
  uVar6 = surface_TouchEffectManager__GetInstance(0);
  *(undefined8 *)(param_1 + 0x138) = uVar6;
  uVar6 = form_FormManager__GetInstance(0);
  *(undefined8 *)(param_1 + 0x140) = uVar6;
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  lVar7 = *(long *)puVar2;
  if (*(int *)(lVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar7 = *(long *)puVar2;
  }
  puVar1 = PTR_kairo_unity_ui_Font_TypeInfo_01fbfe70;
  if (**(long **)(lVar7 + 0xb8) != 0) {
    uVar8 = kairo_unity_ui_IApplication__GetScaleRatio(**(long **)(lVar7 + 0xb8),0,0);
    *(undefined4 *)(param_1 + 0xc4) = uVar8;
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
    kairo_unity_ui_Font___ctor(uVar6,0);
    *(undefined8 *)(param_1 + 0x158) = uVar6;
    *(undefined8 *)(param_1 + 0x160) = 0xffffffffffffffff;
    *(undefined4 *)(param_1 + 0x168) = 0;
    lVar7 = FUN_00db0c30(*(undefined8 *)puVar3,1);
    if (lVar7 != 0) {
      if (*(int *)(lVar7 + 0x18) != 0) {
        *(undefined4 *)(lVar7 + 0x20) = 0xc;
        kairo_unity_surface_SurfaceBase__SetScrollComponent(param_1,0x21,lVar7,0);
        return;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Load
// Address: 00ef7cc8
// ==========================================================================================

void surface_GameView__Load(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  long *plVar8;
  
  puVar2 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff72c & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_kairo_unity_ui_Image___TypeInfo_01fc0248);
    FUN_00db0bbc(PTR_kairo_unity_ui_Image_TypeInfo_01fbf500);
    DAT_020ff72c = 1;
  }
  lVar3 = *(long *)puVar2;
  if (*(int *)(lVar3 + 0xe0) == 0) {
                    /* try { // try from 00ef7d28 to 00ef7d2b has its CatchHandler @ 00ef7ec8 */
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar3 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x10);
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7ec4 to 00ef7ec7 has its CatchHandler @ 00ef7ed0 */
    FUN_00db0de4();
  }
                    /* try { // try from 00ef7d4c to 00ef7d4f has its CatchHandler @ 00ef7ecc */
  uVar4 = FUN_00db0c30(*(undefined8 *)PTR_kairo_unity_ui_Image___TypeInfo_01fc0248,
                       *(undefined4 *)(lVar3 + 0x18));
  puVar1 = PTR_kairo_unity_ui_Image_TypeInfo_01fbf500;
  lVar5 = *(long *)puVar2;
  lVar3 = 4;
  *(undefined8 *)(*(long *)(lVar5 + 0xb8) + 8) = uVar4;
  while( true ) {
    if (*(int *)(lVar5 + 0xe0) == 0) {
                    /* try { // try from 00ef7d70 to 00ef7d77 has its CatchHandler @ 00ef7edc */
      thunk_FUN_00df405c(lVar5);
      lVar5 = *(long *)puVar2;
    }
    lVar6 = *(long *)(lVar5 + 0xb8);
    if (*(long *)(lVar6 + 8) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7e98 to 00ef7e9b has its CatchHandler @ 00ef7ef8 */
      FUN_00db0de4();
    }
    uVar7 = lVar3 - 4;
    if ((long)*(int *)(*(long *)(lVar6 + 8) + 0x18) <= (long)uVar7) {
      return;
    }
    if (*(int *)(lVar5 + 0xe0) == 0) {
                    /* try { // try from 00ef7da0 to 00ef7da7 has its CatchHandler @ 00ef7ed8 */
      thunk_FUN_00df405c(lVar5);
      lVar6 = *(long *)(*(long *)puVar2 + 0xb8);
    }
    lVar5 = *(long *)(lVar6 + 0x10);
    if (lVar5 == 0) break;
    if (*(uint *)(lVar5 + 0x18) <= uVar7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7e9c to 00ef7e9f has its CatchHandler @ 00ef7f00 */
      FUN_00db0dec();
    }
    if (param_1 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7ea4 to 00ef7ea7 has its CatchHandler @ 00ef7f00 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef7dcc to 00ef7dd7 has its CatchHandler @ 00ef7eec */
    lVar5 = kairo_unity_util_JarInflater__GetSize(param_1,*(undefined8 *)(lVar5 + lVar3 * 8),0);
    if (lVar5 != -1) {
      lVar5 = *(long *)puVar2;
      if (*(int *)(lVar5 + 0xe0) == 0) {
                    /* try { // try from 00ef7dec to 00ef7def has its CatchHandler @ 00ef7ed4 */
        thunk_FUN_00df405c();
        lVar5 = *(long *)puVar2;
      }
      lVar6 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x10);
      if (lVar6 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7eac to 00ef7eaf has its CatchHandler @ 00ef7ee4 */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar6 + 0x18) <= uVar7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7eb0 to 00ef7eb3 has its CatchHandler @ 00ef7ee0 */
        FUN_00db0dec();
      }
      plVar8 = *(long **)(*(long *)(lVar5 + 0xb8) + 8);
                    /* try { // try from 00ef7e14 to 00ef7e33 has its CatchHandler @ 00ef7ee8 */
      uVar4 = kairo_unity_util_JarInflater__GetData(param_1,*(undefined8 *)(lVar6 + lVar3 * 8),0);
      if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef7e34 to 00ef7e63 has its CatchHandler @ 00ef7ef4 */
      lVar5 = kairo_unity_ui_Image__Load(uVar4,0xffffffff,0xffffffff,0);
      if (plVar8 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7ea8 to 00ef7eab has its CatchHandler @ 00ef7efc */
        FUN_00db0de4();
      }
      if ((lVar5 != 0) &&
         (lVar6 = thunk_FUN_00e11b18(lVar5,*(undefined8 *)(*plVar8 + 0x40)), lVar6 == 0)) {
        uVar4 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar4,0);
      }
      if (*(uint *)(plVar8 + 3) <= uVar7) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7eb4 to 00ef7ec3 has its CatchHandler @ 00ef7efc */
        FUN_00db0dec();
      }
      plVar8[lVar3] = lVar5;
    }
    lVar5 = *(long *)puVar2;
    lVar3 = lVar3 + 1;
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00ef7ea0 to 00ef7ea3 has its CatchHandler @ 00ef7ef0 */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__GetGameHeight
// Address: 00ef7f7c
// ==========================================================================================

int surface_GameView__GetGameHeight(long param_1)

{
  int iVar1;
  float fVar2;
  
  fVar2 = (float)(*(int *)(param_1 + 0xc0) * 100) / *(float *)(param_1 + 0xc4) + DAT_005bcfd0;
  iVar1 = -0x80000000;
  if (fVar2 != INFINITY) {
    iVar1 = (int)fVar2;
  }
  return iVar1;
}



// ==========================================================================================
// Function: surface_GameView__GetSideSoftWidth
// Address: 00ef7fbc
// ==========================================================================================

int surface_GameView__GetSideSoftWidth(long param_1)

{
  undefined *puVar1;
  int iVar2;
  long lVar3;
  float fVar4;
  
  puVar1 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if ((DAT_020ff72e & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    DAT_020ff72e = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = surface_GamePad__GetInstance();
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(int *)(lVar3 + 0x178) == 2) {
    fVar4 = (*(float *)(lVar3 + 0xc4) * 82.0) / *(float *)(param_1 + 0xc4) + DAT_005bcfd0;
    iVar2 = -0x80000000;
    if (fVar4 != INFINITY) {
      iVar2 = (int)fVar4;
    }
  }
  else {
    iVar2 = 0;
  }
  return iVar2;
}



// ==========================================================================================
// Function: surface_GameView__IsGameSurface
// Address: 00ef8068
// ==========================================================================================

undefined8 surface_GameView__IsGameSurface(void)

{
  return 1;
}



// ==========================================================================================
// Function: surface_GameView__BeginTouchRegist
// Address: 00ef8070
// ==========================================================================================

void surface_GameView__BeginTouchRegist(undefined8 param_1,undefined8 param_2)

{
  kairo_unity_surface_SurfaceBase__BeginTouchRegist(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__EndTouchRegist
// Address: 00ef8078
// ==========================================================================================

void surface_GameView__EndTouchRegist(long param_1,long param_2)

{
  short sVar1;
  int iVar2;
  undefined *puVar3;
  undefined *puVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  int iVar9;
  long lVar10;
  long lVar11;
  ulong uVar12;
  long lVar13;
  long lVar14;
  undefined8 uVar15;
  long lVar16;
  int iVar17;
  long lVar18;
  int iVar19;
  long lVar20;
  int iVar21;
  int iVar22;
  undefined8 *puVar23;
  undefined8 *puVar24;
  int iVar25;
  uint uVar26;
  long *plVar27;
  long lVar28;
  float fVar29;
  float fVar30;
  float fVar31;
  undefined4 uVar32;
  long local_78;
  
  if ((DAT_020ff72f & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_TouchComponent__Add_01fc0b28);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_TouchComponent___ctor_01fc0b30);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_TouchComponent__get_Count_01fc0b38);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_TouchComponent__get_Item_01fc0b40);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_TouchComponent__TypeInfo_01fc0b48);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
    FUN_00db0bbc(PTR_Method_java_util_Vector_int____ElementAt_01fc0b50);
    FUN_00db0bbc(PTR_Method_java_util_Vector_int____RemoveAllElements_01fc0b58);
    FUN_00db0bbc(PTR_Method_java_util_Vector_int____Size_01fc0b60);
    DAT_020ff72f = 1;
  }
  iVar5 = kairo_unity_surface_SurfaceBase__GetComponentLength(param_1,0);
  puVar3 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if (iVar5 < 1) {
    lVar10 = 0;
    lVar16 = 0;
    lVar28 = 0;
    local_78 = 0;
  }
  else {
    local_78 = 0;
    lVar28 = 0;
    iVar8 = 0;
    lVar13 = 0;
    lVar11 = 0;
    do {
      lVar10 = kairo_unity_surface_SurfaceBase__GetComponent(param_1,iVar8,0);
      if (lVar10 == 0) goto LAB_00ef8d48;
      iVar25 = *(int *)(lVar10 + 0x18);
      lVar16 = lVar10;
      if (((iVar25 != 0xf) && (iVar25 != 0xc)) && (lVar16 = lVar11, iVar25 == 0xb)) {
        uVar32 = *(undefined4 *)(lVar10 + 0x2c);
        if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        lVar11 = kairo_unity_util_BitUtil__Split(uVar32,0);
        if (lVar11 == 0) goto LAB_00ef8d48;
        if (*(uint *)(lVar11 + 0x18) < 2) goto LAB_00ef8de8;
        sVar1 = *(short *)(lVar11 + 0x22);
        if (local_78 == 0) {
LAB_00ef822c:
          local_78 = lVar10;
        }
        else {
          uVar32 = *(undefined4 *)(local_78 + 0x2c);
          if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          lVar11 = kairo_unity_util_BitUtil__Split(uVar32,0);
          if (lVar11 == 0) goto LAB_00ef8d48;
          if (*(uint *)(lVar11 + 0x18) < 2) goto LAB_00ef8de8;
          if (sVar1 < *(short *)(lVar11 + 0x22)) goto LAB_00ef822c;
        }
        if (lVar28 != 0) {
          uVar32 = *(undefined4 *)(lVar28 + 0x2c);
          if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          lVar11 = kairo_unity_util_BitUtil__Split(uVar32,0);
          if (lVar11 == 0) goto LAB_00ef8d48;
          if (*(uint *)(lVar11 + 0x18) < 2) goto LAB_00ef8de8;
          if (sVar1 <= *(short *)(lVar11 + 0x22)) goto LAB_00ef827c;
        }
        lVar28 = lVar10;
      }
LAB_00ef827c:
      uVar12 = kairo_unity_surface_TouchComponent__Check(lVar10,0x10,0);
      iVar8 = iVar8 + 1;
      if ((uVar12 & 1) == 0) {
        lVar10 = lVar13;
      }
      lVar13 = lVar10;
      lVar11 = lVar16;
    } while (iVar5 != iVar8);
  }
  puVar4 = PTR_System_Collections_Generic_List_TouchComponent__TypeInfo_01fc0b48;
  puVar3 = PTR_Method_System_Collections_Generic_List_TouchComponent___ctor_01fc0b30;
  lVar13 = thunk_FUN_00e11c14(*(undefined8 *)
                               PTR_System_Collections_Generic_List_TouchComponent__TypeInfo_01fc0b48
                             );
  Method_System_Collections_Generic_List_object___ctor(lVar13,*(undefined8 *)puVar3);
  lVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  Method_System_Collections_Generic_List_object___ctor(lVar11,*(undefined8 *)puVar3);
  puVar3 = PTR_Method_System_Collections_Generic_List_TouchComponent__Add_01fc0b28;
  if (0 < iVar5) {
    iVar8 = 0;
    do {
      lVar14 = kairo_unity_surface_SurfaceBase__GetComponent(param_1,iVar8,0);
      if (lVar14 == 0) goto LAB_00ef8d48;
      if (*(int *)(lVar14 + 0x18) == 0xb) {
        if ((local_78 != 0) && (*(int *)(local_78 + 0x20) == *(int *)(lVar14 + 0x20))) {
          if (lVar13 == 0) goto LAB_00ef8d48;
          lVar18 = *(long *)(lVar13 + 0x10);
          lVar20 = *(long *)puVar3;
          *(int *)(lVar13 + 0x1c) = *(int *)(lVar13 + 0x1c) + 1;
          if (lVar18 == 0) goto LAB_00ef8d48;
          uVar26 = *(uint *)(lVar13 + 0x18);
          if (uVar26 < *(uint *)(lVar18 + 0x18)) {
            *(uint *)(lVar13 + 0x18) = uVar26 + 1;
            *(long *)(lVar18 + (long)(int)uVar26 * 8 + 0x20) = lVar14;
          }
          else {
            System_Collections_Generic_List_object___AddWithResize
                      (lVar13,lVar14,
                       *(undefined8 *)(*(long *)(*(long *)(lVar20 + 0x20) + 0xc0) + 0x70));
          }
        }
        if ((lVar28 != 0) &&
           (*(int *)(lVar28 + 0x28) + *(int *)(lVar28 + 0x20) ==
            *(int *)(lVar14 + 0x28) + *(int *)(lVar14 + 0x20))) {
          if (lVar11 == 0) goto LAB_00ef8d48;
          lVar18 = *(long *)(lVar11 + 0x10);
          lVar20 = *(long *)puVar3;
          *(int *)(lVar11 + 0x1c) = *(int *)(lVar11 + 0x1c) + 1;
          if (lVar18 == 0) goto LAB_00ef8d48;
          uVar26 = *(uint *)(lVar11 + 0x18);
          if (uVar26 < *(uint *)(lVar18 + 0x18)) {
            *(uint *)(lVar11 + 0x18) = uVar26 + 1;
            *(long *)(lVar18 + (long)(int)uVar26 * 8 + 0x20) = lVar14;
          }
          else {
            System_Collections_Generic_List_object___AddWithResize
                      (lVar11,lVar14,
                       *(undefined8 *)(*(long *)(*(long *)(lVar20 + 0x20) + 0xc0) + 0x70));
          }
        }
      }
      iVar8 = iVar8 + 1;
    } while (iVar5 != iVar8);
  }
  puVar3 = PTR_Method_System_Collections_Generic_List_TouchComponent__get_Item_01fc0b40;
  if (lVar13 != 0) {
    if (0 < *(int *)(lVar13 + 0x18)) {
      iVar8 = 0;
      do {
        lVar14 = Method_System_Collections_Generic_List_object__get_Item
                           (lVar13,iVar8,*(undefined8 *)puVar3);
        if (lVar14 == 0) goto LAB_00ef8d48;
        *(int *)(lVar14 + 0x20) = *(int *)(lVar14 + 0x20) + -10;
        lVar14 = Method_System_Collections_Generic_List_object__get_Item
                           (lVar13,iVar8,*(undefined8 *)puVar3);
        if (lVar14 == 0) goto LAB_00ef8d48;
        iVar8 = iVar8 + 1;
        *(int *)(lVar14 + 0x28) = *(int *)(lVar14 + 0x28) + 10;
      } while (iVar8 < *(int *)(lVar13 + 0x18));
    }
    if (lVar11 != 0) {
      iVar8 = *(int *)(lVar11 + 0x18);
      if (0 < iVar8) {
        iVar25 = 0;
        do {
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar11,iVar25,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          iVar25 = iVar25 + 1;
          *(int *)(lVar14 + 0x28) = *(int *)(lVar14 + 0x28) + 10;
          iVar8 = *(int *)(lVar11 + 0x18);
        } while (iVar25 < iVar8);
      }
      if (*(int *)(lVar13 + 0x18) < 1) {
        iVar9 = 0x7fffffff;
        iVar25 = -0x80000000;
      }
      else {
        iVar8 = 0;
        iVar25 = -0x80000000;
        iVar9 = 0x7fffffff;
        do {
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar13,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          if (*(int *)(lVar14 + 0x1c) < iVar9) {
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar13,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar9 = *(int *)(lVar14 + 0x1c);
          }
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar13,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          iVar21 = *(int *)(lVar14 + 0x1c);
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar13,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          if (iVar25 < *(int *)(lVar14 + 0x24) + iVar21) {
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar13,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar25 = *(int *)(lVar14 + 0x1c);
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar13,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar25 = *(int *)(lVar14 + 0x24) + iVar25;
          }
          iVar8 = iVar8 + 1;
        } while (iVar8 < *(int *)(lVar13 + 0x18));
        iVar8 = *(int *)(lVar11 + 0x18);
      }
      if (0 < iVar8) {
        iVar8 = 0;
        do {
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar11,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          if (*(int *)(lVar14 + 0x1c) < iVar9) {
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar11,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar9 = *(int *)(lVar14 + 0x1c);
          }
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar11,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          iVar21 = *(int *)(lVar14 + 0x1c);
          lVar14 = Method_System_Collections_Generic_List_object__get_Item
                             (lVar11,iVar8,*(undefined8 *)puVar3);
          if (lVar14 == 0) goto LAB_00ef8d48;
          if (iVar25 < *(int *)(lVar14 + 0x24) + iVar21) {
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar11,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar25 = *(int *)(lVar14 + 0x1c);
            lVar14 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar11,iVar8,*(undefined8 *)puVar3);
            if (lVar14 == 0) goto LAB_00ef8d48;
            iVar25 = *(int *)(lVar14 + 0x24) + iVar25;
          }
          iVar8 = iVar8 + 1;
        } while (iVar8 < *(int *)(lVar11 + 0x18));
      }
      plVar27 = (long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888;
      if ((lVar16 != 0) && (local_78 != 0)) {
        if ((*(long *)(lVar16 + 0x30) == 0) ||
           (lVar14 = *(long *)(*(long *)(lVar16 + 0x30) + 0x38), lVar14 == 0)) goto LAB_00ef8d48;
        lVar14 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,
                              *(undefined4 *)(lVar14 + 0x18));
        if ((*(long *)(lVar16 + 0x30) == 0) || (lVar14 == 0)) goto LAB_00ef8d48;
        java_lang_JSystem__Arraycopy
                  (*(undefined8 *)(*(long *)(lVar16 + 0x30) + 0x38),0,lVar14,0,
                   *(undefined4 *)(lVar14 + 0x18),0);
        if (*(int *)(lVar13 + 0x18) < 1) {
          uVar26 = 0;
        }
        else {
          uVar26 = 0;
          iVar8 = 0;
          do {
            lVar18 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar13,iVar8,*(undefined8 *)puVar3);
            if (lVar18 == 0) goto LAB_00ef8d48;
            uVar6 = kairo_unity_surface_SurfaceBase__CheckTouch
                              (param_1,0xb,*(undefined4 *)(lVar18 + 0x2c),0);
            iVar8 = iVar8 + 1;
            uVar26 = uVar26 | uVar6;
          } while (iVar8 < *(int *)(lVar13 + 0x18));
        }
        if (*(int *)(lVar11 + 0x18) < 1) {
          uVar6 = 0;
        }
        else {
          uVar6 = 0;
          iVar8 = 0;
          do {
            lVar13 = Method_System_Collections_Generic_List_object__get_Item
                               (lVar11,iVar8,*(undefined8 *)puVar3);
            if (lVar13 == 0) goto LAB_00ef8d48;
            uVar7 = kairo_unity_surface_SurfaceBase__CheckTouch
                              (param_1,0xb,*(undefined4 *)(lVar13 + 0x2c),0);
            iVar8 = iVar8 + 1;
            uVar6 = uVar6 | uVar7;
          } while (iVar8 < *(int *)(lVar11 + 0x18));
        }
        if (*(int *)(*(long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar15 = kairo_unity_surface_TouchOption__Create(lVar14,0);
        if (((uVar26 & 1) != 0) ||
           (uVar12 = kairo_unity_surface_SurfaceBase__CheckTouch
                               (param_1,0xd,*(undefined4 *)(lVar16 + 0x2c),0), (uVar12 & 1) != 0)) {
          kairo_unity_surface_SurfaceBase__AddTouchComponent
                    (param_1,0xd,iVar9,0,iVar25 - iVar9,*(undefined4 *)(local_78 + 0x20),
                     *(undefined4 *)(lVar16 + 0x2c),uVar15,0);
        }
        plVar27 = (long *)PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888;
        if (((uVar6 & 1) != 0) ||
           (uVar12 = kairo_unity_surface_SurfaceBase__CheckTouch
                               (param_1,0xd,*(uint *)(lVar16 + 0x2c) | 1,0), (uVar12 & 1) != 0)) {
          if (lVar28 == 0) goto LAB_00ef8d48;
          kairo_unity_surface_SurfaceBase__AddTouchComponent
                    (param_1,0xd,iVar9,*(int *)(lVar28 + 0x28) + *(int *)(lVar28 + 0x20),
                     iVar25 - iVar9,0xf0,*(uint *)(lVar16 + 0x2c) | 1,uVar15,0);
        }
      }
      if (lVar16 != 0) {
        lVar28 = *(long *)(lVar16 + 0x30);
        if ((lVar28 == 0) || (lVar13 = *(long *)(lVar28 + 0x38), lVar13 == 0)) goto LAB_00ef8d48;
        if ((*(int *)(lVar13 + 0x18) == 1) || (*(int *)(lVar13 + 0x18) == 0)) {
LAB_00ef8de8:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        if (*(int *)(lVar13 + 0x20) <= *(int *)(lVar13 + 0x24)) {
          *(uint *)(lVar28 + 0x10) = *(uint *)(lVar28 + 0x10) | 2;
          *(int *)(lVar16 + 0x1c) = *(int *)(lVar16 + 0x1c) + 0x14;
          if (0 < iVar5) {
            iVar8 = 0;
            do {
              lVar16 = kairo_unity_surface_SurfaceBase__GetComponent(param_1,iVar8,0);
              if (lVar16 == 0) goto LAB_00ef8d48;
              if (*(int *)(lVar16 + 0x18) == 0xb) {
                *(int *)(lVar16 + 0x24) = *(int *)(lVar16 + 0x24) + 0x14;
              }
              iVar8 = iVar8 + 1;
            } while (iVar5 != iVar8);
          }
        }
      }
      if (lVar10 != 0) {
        fVar30 = (float)(*(int *)(param_1 + 0xbc) * 100) / *(float *)(param_1 + 0xc4) + DAT_005bcfd0
        ;
        fVar29 = (float)(*(int *)(param_1 + 0xc0) * 100) / *(float *)(param_1 + 0xc4) + DAT_005bcfd0
        ;
        iVar5 = -0x80000000;
        if (fVar30 != INFINITY) {
          iVar5 = (int)fVar30;
        }
        iVar8 = -0x80000000;
        if (fVar29 != INFINITY) {
          iVar8 = (int)fVar29;
        }
        if (*(int *)(*plVar27 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar15 = kairo_unity_surface_TouchOption__Create(1,0);
        kairo_unity_surface_SurfaceBase__AddTouchComponent(param_1,0x10,0,0,iVar5,iVar8,0,uVar15,0);
      }
      if (param_2 != 0) {
        iVar5 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
        iVar8 = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
        if (*(long *)(param_1 + 0x128) != 0) {
          uVar32 = *(undefined4 *)(param_2 + 0x5c);
          iVar25 = *(int *)(param_1 + 0xb4);
          fVar29 = (float)kairo_unity_ui_IApplication__GetScaleRatio(*(long *)(param_1 + 0x128),0,0)
          ;
          if (*(long *)(param_1 + 0x128) != 0) {
            iVar9 = *(int *)(param_1 + 0xb8);
            fVar30 = (float)kairo_unity_ui_IApplication__GetScaleRatio
                                      (*(long *)(param_1 + 0x128),0,0);
            fVar31 = (float)(iVar25 * 100) / fVar29 + DAT_005bcfd0;
            fVar30 = (float)(iVar9 * 100) / fVar30 + DAT_005bcfd0;
            fVar29 = -2.147484e+09;
            if (fVar31 != INFINITY) {
              fVar29 = (float)(int)fVar31;
            }
            fVar31 = -2.147484e+09;
            if (fVar30 != INFINITY) {
              fVar31 = (float)(int)fVar30;
            }
            kairo_unity_ui_Graphics__SetOrigin(fVar29,fVar31,param_2,0);
            kairo_unity_ui_Graphics__Scale(*(float *)(param_1 + 0xc4) + 1.0,param_2,0);
            lVar10 = *(long *)(param_1 + 0x198);
            if (lVar10 != 0) {
              iVar25 = 0;
              puVar23 = (undefined8 *)PTR_Method_java_util_Vector_int____Size_01fc0b60;
              puVar24 = (undefined8 *)PTR_Method_java_util_Vector_int____ElementAt_01fc0b50;
              do {
                iVar9 = Method_java_util_Vector_object__Size(lVar10,*puVar23);
                lVar10 = *(long *)(param_1 + 0x198);
                if (lVar10 == 0) break;
                if (iVar9 <= iVar25) {
                  Method_java_util_Vector_object__RemoveAllElements
                            (lVar10,*(undefined8 *)
                                     PTR_Method_java_util_Vector_int____RemoveAllElements_01fc0b58);
                  uVar26 = *(int *)(param_1 + 0x1a0) + 1;
                  iVar25 = (int)((-(ulong)(uVar26 >> 0x1f) & 0xc000000000000000 |
                                 (ulong)uVar26 << 0x1e) + (long)(int)uVar26 >> 0x20);
                  *(uint *)(param_1 + 0x1a0) =
                       uVar26 + ((iVar25 >> 0x1d) - (iVar25 >> 0x1f)) * -0x7fffffff;
                  kairo_unity_ui_Graphics__Scale(uVar32,param_2,0);
                  kairo_unity_ui_Graphics__SetOrigin((float)iVar5,(float)iVar8,param_2,0);
                  kairo_unity_surface_SurfaceBase__EndTouchRegist(param_1,param_2,0);
                  return;
                }
                lVar10 = Method_java_util_Vector_object__ElementAt(lVar10,iVar25,*puVar24);
                if (lVar10 == 0) break;
                if ((int)*(long *)(lVar10 + 0x18) == 0) goto LAB_00ef8de8;
                kairo_unity_ui_Graphics__Scale
                          ((float)*(int *)(lVar10 + ((*(long *)(lVar10 + 0x18) << 0x20) +
                                                     -0x100000000 >> 0x1e) + 0x20) / 100.0,param_2,0
                          );
                uVar26 = *(uint *)(lVar10 + 0x18);
                if (uVar26 == 0) goto LAB_00ef8de8;
                if (*(int *)(lVar10 + 0x20) == 0) {
                  if ((((uVar26 < 2) || (uVar26 == 2)) || (uVar26 < 4)) || (uVar26 == 4))
                  goto LAB_00ef8de8;
                  iVar21 = *(int *)(lVar10 + 0x28);
                  iVar17 = *(int *)(lVar10 + 0x2c);
                  iVar9 = *(int *)(lVar10 + 0x24);
                  iVar19 = *(int *)(lVar10 + 0x30);
                  iVar22 = 2;
                  if ((0x1e < iVar17) && (0x1e < iVar19)) {
                    iVar9 = iVar9 + 4;
                    iVar21 = iVar21 + 3;
                    iVar17 = iVar17 + -8;
                    iVar19 = iVar19 + -6;
                    iVar22 = 3;
                  }
                  iVar2 = 0;
                  if (iVar22 != 0) {
                    iVar2 = *(int *)(param_1 + 0x168) / iVar22;
                  }
                  uVar26 = iVar2 % 6;
                  if (uVar26 < 5) {
                    uVar6 = *(uint *)(&DAT_005dbc74 + (long)(int)uVar26 * 4);
                  }
                  else {
                    uVar6 = 0x60;
                  }
                  iVar22 = iVar9 + 2;
                  iVar17 = iVar17 + -4;
                  uVar15 = kairo_unity_ui_Graphics__SetRenderMode(param_2,1,uVar6,uVar6 ^ 0xff,0);
                  fVar29 = (float)(iVar21 + -3);
                  fVar30 = (float)(iVar19 + 6);
                  uVar15 = surface_GameView__DrawScaledImage
                                     ((float)(iVar9 + -3),fVar29,0x40a00000,fVar30,uVar15,param_2,8)
                  ;
                  uVar15 = surface_GameView__DrawScaledImage
                                     ((float)iVar22,fVar29,(float)iVar17,fVar30,uVar15,param_2,9);
                  uVar15 = surface_GameView__DrawScaledImage
                                     ((float)(iVar22 + iVar17),fVar29,0x40a00000,fVar30,uVar15,
                                      param_2,10);
                  if (0 < (int)uVar26) {
                    fVar29 = (float)((iVar21 + -3) - uVar26);
                    fVar30 = (float)(iVar19 + 6 + uVar26 * 2);
                    uVar15 = surface_GameView__DrawScaledImage
                                       ((float)((iVar9 + -3) - uVar26),fVar29,0x40a00000,fVar30,
                                        uVar15,param_2,8);
                    uVar15 = surface_GameView__DrawScaledImage
                                       ((float)(iVar22 - uVar26),fVar29,(float)(iVar17 + uVar26 * 2)
                                        ,fVar30,uVar15,param_2,9);
                    surface_GameView__DrawScaledImage
                              ((float)(uVar26 + iVar22 + iVar17),fVar29,0x40a00000,fVar30,uVar15,
                               param_2,10);
                  }
                  kairo_unity_ui_Graphics__SetRenderMode(param_2,0,0xff,0,0);
                  puVar3 = PTR_main_AppData_TypeInfo_01fbf278;
                  lVar10 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
                  if (*(int *)(lVar10 + 0xe0) == 0) {
                    thunk_FUN_00df405c();
                    lVar10 = *(long *)puVar3;
                  }
                  puVar23 = (undefined8 *)PTR_Method_java_util_Vector_int____Size_01fc0b60;
                  puVar24 = (undefined8 *)PTR_Method_java_util_Vector_int____ElementAt_01fc0b50;
                  if (*(char *)(*(long *)(lVar10 + 0xb8) + 0xcc) != '\0') {
                    uVar26 = *(int *)(param_1 + 0x168) + 1;
                    iVar9 = (int)((-(ulong)(uVar26 >> 0x1f) & 0xc000000000000000 |
                                  (ulong)uVar26 << 0x1e) + (long)(int)uVar26 >> 0x20);
                    *(uint *)(param_1 + 0x168) =
                         uVar26 + ((iVar9 >> 0x1d) - (iVar9 >> 0x1f)) * -0x7fffffff;
                  }
                }
                lVar10 = *(long *)(param_1 + 0x198);
                iVar25 = iVar25 + 1;
              } while (lVar10 != 0);
            }
          }
        }
      }
    }
  }
LAB_00ef8d48:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__DrawScaledImage
// Address: 00ef8dec
// ==========================================================================================

void surface_GameView__DrawScaledImage
               (float param_1,float param_2,undefined8 param_3,undefined8 param_4,undefined8 param_5
               ,long param_6,uint param_7)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  undefined *puVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  
  puVar7 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff753 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff753 = 1;
  }
  lVar8 = *(long *)puVar7;
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar8 = *(long *)puVar7;
  }
  lVar9 = *(long *)(lVar8 + 0xb8);
  lVar8 = *(long *)(lVar9 + 0x20);
  if (lVar8 != 0) {
    if (*(uint *)(lVar8 + 0x18) <= param_7) {
LAB_00ef8fc8:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar8 = *(long *)(lVar8 + (long)(int)param_7 * 8 + 0x20);
    if (lVar8 != 0) {
      uVar5 = *(uint *)(lVar8 + 0x18);
      if (uVar5 == 0) goto LAB_00ef8fc8;
      lVar10 = *(long *)(lVar9 + 8);
      if (lVar10 != 0) {
        uVar6 = *(uint *)(lVar8 + 0x20);
        if (*(uint *)(lVar10 + 0x18) <= uVar6) goto LAB_00ef8fc8;
        lVar10 = *(long *)(lVar10 + (long)(int)uVar6 * 8 + 0x20);
        if ((lVar10 != 0) && (lVar9 = *(long *)(lVar9 + 0x18), lVar9 != 0)) {
          if (((*(uint *)(lVar9 + 0x18) <= uVar6) || (((uVar5 < 2 || (uVar5 == 2)) || (uVar5 < 4))))
             || (((uVar5 == 4 || (uVar5 < 6)) || (uVar5 == 6)))) goto LAB_00ef8fc8;
          if (param_6 != 0) {
            fVar12 = (float)*(int *)(lVar10 + 0x28) /
                     (float)*(int *)(lVar9 + (long)(int)uVar6 * 4 + 0x20);
            fVar13 = fVar12 * (float)*(int *)(lVar8 + 0x2c) + 0.5;
            fVar11 = fVar12 * (float)*(int *)(lVar8 + 0x30) + 0.5;
            fVar14 = fVar12 * (float)*(int *)(lVar8 + 0x34) + 0.5;
            fVar12 = fVar12 * (float)*(int *)(lVar8 + 0x38) + 0.5;
            iVar1 = -0x80000000;
            if (fVar13 != INFINITY) {
              iVar1 = (int)fVar13;
            }
            iVar2 = -0x80000000;
            if (fVar11 != INFINITY) {
              iVar2 = (int)fVar11;
            }
            iVar3 = -0x80000000;
            if (fVar14 != INFINITY) {
              iVar3 = (int)fVar14;
            }
            iVar4 = -0x80000000;
            if (fVar12 != INFINITY) {
              iVar4 = (int)fVar12;
            }
            kairo_unity_ui_Graphics__DrawScaledImage
                      ((float)*(int *)(lVar8 + 0x24) * 0.75 + param_1,
                       (float)*(int *)(lVar8 + 0x28) * 0.75 + param_2,param_3,param_4,param_6,lVar10
                       ,iVar1,iVar2,iVar3,iVar4,0);
            return;
          }
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__DoEnd
// Address: 00ef8fd0
// ==========================================================================================

void surface_GameView__DoEnd(undefined8 param_1)

{
  kairo_unity_surface_SurfaceBase__DoEnd(param_1,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00ef8fd8
// ==========================================================================================

void surface_GameView__AddTouch(undefined4 param_1)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  long lVar4;
  float fVar5;
  float fVar6;
  
  puVar3 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff730 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff730 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (lVar4 != 0) {
    fVar6 = (float)(*(int *)(lVar4 + 0xbc) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    fVar5 = (float)(*(int *)(lVar4 + 0xc0) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    iVar1 = -0x80000000;
    if (fVar6 != INFINITY) {
      iVar1 = (int)fVar6;
    }
    iVar2 = -0x80000000;
    if (fVar5 != INFINITY) {
      iVar2 = (int)fVar5;
    }
    surface_GameView___addTouch(lVar4,0,param_1,0,0,iVar1,iVar2,0,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView___addTouch
// Address: 00ef90b8
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00efa390) */

long surface_GameView___addTouch
               (long param_1,long param_2,uint param_3,uint param_4,int param_5,int param_6,
               int param_7,uint param_8,long param_9)

{
  float *pfVar1;
  long lVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  float fVar11;
  float fVar12;
  undefined *puVar13;
  bool bVar14;
  bool bVar15;
  byte bVar16;
  int iVar17;
  int iVar18;
  int iVar19;
  undefined4 uVar20;
  uint uVar21;
  int iVar22;
  long lVar23;
  long lVar24;
  long *plVar25;
  long *plVar26;
  ulong uVar27;
  undefined8 uVar28;
  long lVar29;
  uint uVar30;
  uint uVar31;
  int iVar32;
  float fVar33;
  double dVar34;
  float fVar35;
  int local_7c;
  int local_78;
  int local_74;
  uint local_64;
  
  local_64 = param_8;
  if ((DAT_020ff73e & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100);
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_form_MyFormBase_TypeInfo_01fbf360);
    FUN_00db0bbc(PTR_form_SubForm_TypeInfo_01fbf300);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
    FUN_00db0bbc(PTR_StringLiteral_9542_01fc0b68);
    FUN_00db0bbc(PTR_StringLiteral_3286_01fc0b70);
    FUN_00db0bbc(PTR_StringLiteral_606_01fc0b78);
    DAT_020ff73e = 1;
  }
  if (param_3 == 2) {
    if (param_9 == 0) {
      param_9 = thunk_FUN_00e11c14(*(undefined8 *)
                                    PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
      kairo_unity_surface_TouchOption___ctor(param_9,0);
      if (param_9 == 0) goto LAB_00efa360;
    }
    kairo_unity_surface_TouchOption__Flag(param_9,*(uint *)(param_9 + 0x10) | 0xc00,0);
  }
  puVar13 = PTR_form_MyFormBase_TypeInfo_01fbf360;
  lVar23 = *(long *)PTR_form_MyFormBase_TypeInfo_01fbf360;
  if (*(int *)(lVar23 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar23 = *(long *)puVar13;
  }
  puVar13 = PTR_form_SubForm_TypeInfo_01fbf300;
  if (*(int *)(*(long *)(lVar23 + 0xb8) + 0x44) == 1) {
    lVar23 = *(long *)PTR_form_SubForm_TypeInfo_01fbf300;
    if (*(int *)(lVar23 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar23 = *(long *)puVar13;
    }
    if (*(char *)(*(long *)(lVar23 + 0xb8) + 0x18) == '\0') {
      return 0;
    }
  }
  if (param_2 == 0) goto LAB_00ef95c8;
  switch(param_3) {
  case 0x13:
    iVar19 = param_7 + -3;
    if (-1 < param_7 + -4) {
      iVar19 = param_7 + -4;
    }
    iVar19 = param_5 + (iVar19 >> 1);
    kairo_unity_ui_Graphics__SetColor(param_2,0x1e,0x1e,0x1e,0);
    kairo_unity_ui_Graphics__FillRect
              ((float)(param_4 + 1),(float)iVar19,(float)(param_6 + -2),0x40800000,param_2,0);
    kairo_unity_ui_Graphics__FillRect
              ((float)param_4,(float)(iVar19 + 1),(float)param_6,0x40000000,param_2,0);
    if ((param_9 == 0) || (lVar23 = *(long *)(param_9 + 0x30), lVar23 == 0)) goto LAB_00efa360;
    if (*(uint *)(lVar23 + 0x18) < 5) goto LAB_00efa38c;
    iVar22 = *(int *)(lVar23 + 0x30) + -1;
    iVar32 = 0;
    if (iVar22 != 0) {
      iVar32 = (param_6 + -2) / iVar22;
    }
    uVar28 = surface_GameView__Get(param_1,param_8);
    surface_GameView__DrawImage
              ((float)(param_4 + (int)uVar28 * iVar32),(float)(iVar19 + 2),uVar28,param_2,0xb);
    iVar19 = surface_GameView__Get(param_1,param_8);
    param_4 = (param_4 + iVar19 * iVar32) - 0xf;
    param_6 = 0x20;
    goto LAB_00ef95c8;
  case 0x14:
    uVar27 = kairo_unity_surface_SurfaceBase__CheckTouch(param_1,0x14,param_8,0);
    fVar33 = (float)(param_4 + 0xf);
    iVar19 = param_7;
    if (param_7 < 0) {
      iVar19 = param_7 + 1;
    }
    fVar35 = (float)(param_5 + (iVar19 >> 1));
    if ((uVar27 & 1) == 0) {
      uVar28 = 5;
    }
    else {
      uVar28 = 7;
    }
    break;
  case 0x15:
    uVar27 = kairo_unity_surface_SurfaceBase__CheckTouch(param_1,0x15,param_8,0);
    iVar19 = param_7;
    if (param_7 < 0) {
      iVar19 = param_7 + 1;
    }
    fVar33 = (float)(param_4 + param_6 + -0xf);
    fVar35 = (float)(param_5 + (iVar19 >> 1));
    if ((uVar27 & 1) == 0) {
      uVar28 = 4;
    }
    else {
      uVar28 = 6;
    }
    break;
  default:
    if ((param_3 == 0xf) || (param_3 == 0xc)) {
      if ((param_9 == 0) || (lVar23 = *(long *)(param_9 + 0x38), lVar23 == 0)) goto LAB_00efa360;
      if ((*(int *)(lVar23 + 0x18) == 0) || (*(int *)(lVar23 + 0x18) == 1)) goto LAB_00efa38c;
      iVar19 = *(int *)(lVar23 + 0x20);
      iVar32 = *(int *)(lVar23 + 0x24);
      bVar16 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,param_3,param_8,0);
      iVar22 = iVar19 - iVar32;
      bVar16 = (iVar22 != 0 && iVar32 <= iVar19) & bVar16;
      if (bVar16 == 1) {
        if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        surface_GameView__ClearMarker();
      }
      if (param_1 == 0) goto LAB_00efa360;
      *(byte *)(param_1 + 0x188) = (byte)(*(uint *)(param_9 + 0x10) >> 9) & 1;
      if (param_3 == 0xc) {
        surface_GameView__Get(param_1,param_8);
        lVar23 = surface_GameView__DrawVerticalScroll(param_1,param_2,param_4,param_5);
        if (lVar23 != 0) {
          if ((bVar16 == 0) || (iVar22 < 1)) {
            if ((*(int *)(lVar23 + 0x18) == 1) || (*(int *)(lVar23 + 0x18) == 0)) {
LAB_00efa38c:
                    /* WARNING: Subroutine does not return */
              FUN_00db0dec();
            }
            param_5 = *(int *)(lVar23 + 0x20);
            param_7 = *(int *)(lVar23 + 0x24);
            param_6 = 5;
          }
          else {
            *(uint *)(param_9 + 0x10) = *(uint *)(param_9 + 0x10) | 0x24;
            iVar17 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
            iVar18 = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
            if (iVar32 == 1) {
              lVar23 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,6);
              if (lVar23 == 0) goto LAB_00efa360;
              uVar21 = *(uint *)(lVar23 + 0x18);
              if ((((uVar21 == 0) || (*(uint *)(lVar23 + 0x20) = iVar17 + param_4, uVar21 == 1)) ||
                  (*(int *)(lVar23 + 0x24) = iVar18 + param_5, uVar21 < 3)) ||
                 ((*(int *)(lVar23 + 0x28) = param_6, uVar21 == 3 ||
                  (*(int *)(lVar23 + 0x2c) = param_7, uVar21 < 6)))) goto LAB_00efa38c;
              *(int *)(lVar23 + 0x34) = iVar19;
              *(long *)(param_9 + 0x30) = lVar23;
            }
            else {
              if (*(uint *)(lVar23 + 0x18) < 2) goto LAB_00efa38c;
              fVar33 = (float)(param_7 - *(int *)(lVar23 + 0x24)) / (float)iVar22;
              *(float *)(param_9 + 0x1c) = fVar33;
              if (fVar33 <= 0.0) {
                *(undefined4 *)(param_9 + 0x1c) = 0x3f800000;
              }
            }
            param_4 = param_4 - 0x1e;
            param_5 = -1000;
            param_6 = 0x7d;
            param_7 = 2000;
          }
        }
      }
    }
    goto LAB_00ef95c8;
  case 0x1b:
    uVar27 = kairo_unity_surface_SurfaceBase__CheckTouch(param_1,0x1b,param_8,0);
    iVar19 = param_6;
    if (param_6 < 0) {
      iVar19 = param_6 + 1;
    }
    iVar32 = param_7;
    if (param_7 < 0) {
      iVar32 = param_7 + 1;
    }
    fVar33 = (float)(param_4 + (iVar19 >> 1) + 1);
    fVar35 = (float)(param_5 + (iVar32 >> 1));
    if ((uVar27 & 1) == 0) {
      uVar28 = 1;
    }
    else {
      uVar28 = 3;
    }
    break;
  case 0x1c:
    uVar27 = kairo_unity_surface_SurfaceBase__CheckTouch(param_1,0x1c,param_8,0);
    iVar19 = param_6;
    if (param_6 < 0) {
      iVar19 = param_6 + 1;
    }
    iVar32 = param_7;
    if (param_7 < 0) {
      iVar32 = param_7 + 1;
    }
    fVar33 = (float)(param_4 + (iVar19 >> 1));
    fVar35 = (float)(param_5 + (iVar32 >> 1));
    if ((uVar27 & 1) == 0) {
      uVar28 = 0;
    }
    else {
      uVar28 = 2;
    }
  }
  surface_GameView__DrawImage(fVar33,fVar35,uVar27,param_2,uVar28);
LAB_00ef95c8:
  if (*(long *)(param_1 + 0x140) == 0) {
LAB_00efa360:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  lVar23 = kairo_unity_form_FormManagerBase__GetCurrentForm(*(long *)(param_1 + 0x140),0);
  if (*(long *)(param_1 + 0x140) == 0) goto LAB_00efa360;
  lVar24 = kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
  if (lVar23 != lVar24) {
    if (*(long *)(param_1 + 0x140) == 0) goto LAB_00efa360;
    plVar25 = (long *)kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    if (((*(long *)(param_1 + 0x140) == 0) ||
        (plVar26 = (long *)kairo_unity_form_FormManagerBase__GetCurrentForm
                                     (*(long *)(param_1 + 0x140),0),
        puVar13 = PTR_form_SubForm_TypeInfo_01fbf300, plVar25 == (long *)0x0)) ||
       (plVar26 == (long *)0x0)) goto LAB_00efa360;
    if (*(int *)(plVar25 + 2) != 4) {
      return 0;
    }
    if (*(int *)(plVar26 + 2) != 4) {
      return 0;
    }
    bVar16 = *(byte *)(*(long *)PTR_form_SubForm_TypeInfo_01fbf300 + 0x130);
    if ((*(byte *)(*plVar25 + 0x130) < bVar16) ||
       (*(long *)(*(long *)(*plVar25 + 200) + (ulong)bVar16 * 8 + -8) !=
        *(long *)PTR_form_SubForm_TypeInfo_01fbf300)) {
                    /* WARNING: Subroutine does not return */
      FUN_00db1180(plVar25);
    }
    uVar27 = form_SubForm__IsMenu(plVar25,0);
    if ((uVar27 & 1) == 0) {
      return 0;
    }
    bVar16 = *(byte *)(*(long *)puVar13 + 0x130);
    if ((*(byte *)(*plVar26 + 0x130) < bVar16) ||
       (*(long *)(*(long *)(*plVar26 + 200) + (ulong)bVar16 * 8 + -8) != *(long *)puVar13)) {
                    /* WARNING: Subroutine does not return */
      FUN_00db1180(plVar26);
    }
    uVar27 = form_SubForm__IsMenu(plVar26,0);
    if ((uVar27 & 1) == 0) {
      return 0;
    }
  }
  uVar21 = local_64;
  puVar13 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((param_9 != 0) && ((*(byte *)(param_9 + 0x10) >> 6 & 1) != 0)) {
    return 0;
  }
  if ((int)local_64 < 0) {
    lVar23 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    if (*(int *)(lVar23 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar23 = *(long *)puVar13;
    }
    if (*(char *)(*(long *)(lVar23 + 0xb8) + 0x17) != '\0') {
      lVar23 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100);
      kairo_unity_ui_Dialog___ctor(lVar23,1,*(undefined8 *)PTR_StringLiteral_3286_01fc0b70,0);
      uVar28 = System_Int32__ToString(&local_64,0);
      uVar28 = System_String__Concat
                         (*(undefined8 *)PTR_StringLiteral_9542_01fc0b68,uVar28,
                          *(undefined8 *)PTR_StringLiteral_606_01fc0b78,0);
      if (lVar23 != 0) {
        kairo_unity_ui_Dialog__SetText(lVar23,uVar28,0);
        kairo_unity_ui_Dialog__Show(lVar23,0);
        if (*(long *)(param_1 + 0x128) != 0) {
          kairo_unity_ui_IApplication__Terminate(*(long *)(param_1 + 0x128),0);
          return 0;
        }
      }
      goto LAB_00efa360;
    }
  }
  if (param_2 == 0) {
    local_7c = 0;
    local_78 = 0;
    local_74 = param_5;
  }
  else {
    local_78 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
    local_7c = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
    local_74 = local_7c + param_5;
    param_4 = local_78 + param_4;
    kairo_unity_ui_Graphics__SetOrigin(0,0,param_2,0);
    if (param_9 != 0) {
      if ((*(byte *)(param_9 + 0x10) >> 4 & 1) != 0) {
        if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
                    /* try { // try from 00ef9754 to 00ef9757 has its CatchHandler @ 00efa468 */
          thunk_FUN_00df405c();
        }
                    /* try { // try from 00ef9758 to 00ef9763 has its CatchHandler @ 00efa4c4 */
        uVar27 = surface_GameView__CheckMarker(param_3,uVar21);
        if (((uVar27 & 1) != 0) && (*(char *)(param_1 + 0x48) == '\0')) {
                    /* try { // try from 00ef977c to 00ef9783 has its CatchHandler @ 00efa434 */
          lVar23 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,5);
                    /* try { // try from 00ef9788 to 00ef9793 has its CatchHandler @ 00efa484 */
          iVar19 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
          if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3f0 to 00efa3f7 has its CatchHandler @ 00efa484 */
            FUN_00db0de4();
          }
          if (*(uint *)(lVar23 + 0x18) < 2) {
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          *(uint *)(lVar23 + 0x24) = iVar19 + param_4;
                    /* try { // try from 00ef97ac to 00ef97b7 has its CatchHandler @ 00efa464 */
          iVar19 = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
          uVar21 = *(uint *)(lVar23 + 0x18);
          if (uVar21 < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3f8 to 00efa3fb has its CatchHandler @ 00efa464 */
            FUN_00db0dec();
          }
          *(int *)(lVar23 + 0x28) = iVar19 + local_74;
          if (uVar21 == 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3fc to 00efa3ff has its CatchHandler @ 00efa430 */
            FUN_00db0dec();
          }
          *(int *)(lVar23 + 0x2c) = param_6;
          if (uVar21 < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa400 to 00efa403 has its CatchHandler @ 00efa460 */
            FUN_00db0dec();
          }
          *(int *)(lVar23 + 0x30) = param_7;
                    /* try { // try from 00ef97e8 to 00ef97f7 has its CatchHandler @ 00efa460 */
          surface_GameView__AddDelayPaintBuffer(param_1,param_2,lVar23);
        }
      }
      uVar3 = *(undefined4 *)(param_2 + 0x58);
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
                    /* try { // try from 00ef9810 to 00ef9813 has its CatchHandler @ 00efa4a8 */
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00ef9814 to 00ef9827 has its CatchHandler @ 00efa4cc */
      uVar20 = kairo_unity_ui_Graphics__GetColorOfRGB(0xef,0x9a,0x16,0);
                    /* try { // try from 00ef983c to 00ef9843 has its CatchHandler @ 00efa48c */
      if (((*(byte *)(param_9 + 0x11) & 1) != 0) &&
         ((local_64 == 0 || (uVar21 = surface_GameView__Get(param_1), uVar21 != (local_64 & 0xffff))
          ))) {
                    /* try { // try from 00ef9850 to 00ef985f has its CatchHandler @ 00efa4a4 */
        kairo_unity_ui_Graphics__SetColor(param_2,uVar20,0);
                    /* try { // try from 00ef9890 to 00ef9897 has its CatchHandler @ 00efa4a0 */
        java_lang_JMath__ToRadians((double)((*(int *)(param_1 + 0x1a0) % 0x2d) * 4),0);
                    /* try { // try from 00ef9898 to 00ef989f has its CatchHandler @ 00efa49c */
        dVar34 = (double)java_lang_JMath__Sin(0);
        iVar19 = -0x80000000;
        if (dVar34 * 96.0 != INFINITY) {
          iVar19 = (int)(dVar34 * 96.0);
        }
                    /* try { // try from 00ef98cc to 00ef98db has its CatchHandler @ 00efa498 */
        kairo_unity_ui_Graphics__SetRenderMode(param_2,1,iVar19,0xff - iVar19,0);
        lVar23 = *(long *)(param_9 + 0x38);
        if (lVar23 == 0) {
                    /* try { // try from 00ef9a40 to 00ef9a4b has its CatchHandler @ 00efa43c */
          kairo_unity_ui_Graphics__FillRect
                    ((float)param_4,(float)local_74,(float)param_6,(float)param_7,param_2,0);
        }
        else {
          uVar21 = *(uint *)(lVar23 + 0x18);
          if (uVar21 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3d8 to 00efa3db has its CatchHandler @ 00efa474 */
            FUN_00db0dec();
          }
          if (uVar21 == 1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3dc to 00efa3df has its CatchHandler @ 00efa470 */
            FUN_00db0dec();
          }
          if (uVar21 < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3e0 to 00efa3e3 has its CatchHandler @ 00efa46c */
            FUN_00db0dec();
          }
          if (uVar21 == 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3e4 to 00efa3e7 has its CatchHandler @ 00efa4ac */
            FUN_00db0dec();
          }
                    /* try { // try from 00ef992c to 00ef9937 has its CatchHandler @ 00efa4ac */
          kairo_unity_ui_Graphics__FillRect
                    ((float)(*(int *)(lVar23 + 0x20) + local_78),
                     (float)(*(int *)(lVar23 + 0x24) + local_7c),(float)*(int *)(lVar23 + 0x28),
                     (float)*(int *)(lVar23 + 0x2c),param_2,0);
        }
                    /* try { // try from 00ef9a4c to 00ef9a57 has its CatchHandler @ 00efa494 */
        kairo_unity_ui_Graphics__SetRenderMode(param_2,0);
      }
      uVar21 = *(uint *)(param_9 + 0x10);
      if ((uVar21 >> 7 & 1) != 0) {
                    /* try { // try from 00ef9a60 to 00ef9a6f has its CatchHandler @ 00efa4c0 */
        kairo_unity_ui_Graphics__SetColor(param_2,uVar20,0);
        iVar19 = (*(int *)(param_1 + 0x1a0) / 0xc) % 2;
                    /* try { // try from 00ef9ac0 to 00ef9acb has its CatchHandler @ 00efa4bc */
        kairo_unity_ui_Graphics__DrawRect
                  ((float)(iVar19 + param_4),(float)(iVar19 + local_74),
                   (float)(param_6 + iVar19 * -2),(float)(param_7 + iVar19 * -2),param_2,0);
        uVar21 = *(uint *)(param_9 + 0x10);
      }
                    /* try { // try from 00ef9ad8 to 00ef9ae7 has its CatchHandler @ 00efa4b8 */
      if (((uVar21 >> 0xb & 1) != 0) &&
         (uVar27 = kairo_unity_surface_SurfaceBase__CheckTouch(param_1,param_3,local_64,0),
         (uVar27 & 1) != 0)) {
                    /* try { // try from 00ef9aec to 00ef9b03 has its CatchHandler @ 00efa480 */
        kairo_unity_ui_Graphics__SetColor(param_2,0xff,0xff,0xff,0);
                    /* try { // try from 00ef9b04 to 00ef9b1b has its CatchHandler @ 00efa47c */
        kairo_unity_ui_Graphics__PushRenderMode(param_2,1,0x40,0xff,0);
                    /* try { // try from 00ef9b1c to 00ef9b27 has its CatchHandler @ 00efa478 */
        kairo_unity_ui_Graphics__PopRenderMode(param_2,0);
      }
                    /* try { // try from 00ef9b28 to 00ef9b37 has its CatchHandler @ 00efa4c8 */
      kairo_unity_ui_Graphics__SetColor(param_2,uVar3,0);
    }
  }
                    /* try { // try from 00ef9b38 to 00ef9b43 has its CatchHandler @ 00efa50c */
  uVar27 = kairo_unity_surface_SurfaceBase__get_registTouch(param_1,0);
  puVar13 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((uVar27 & 1) == 0) {
    lVar23 = 0;
    if (param_2 == 0) {
      return 0;
    }
    goto LAB_00ef9c64;
  }
  lVar23 = *(long *)PTR_surface_GameView_TypeInfo_01fbf588;
  if (*(int *)(lVar23 + 0xe0) == 0) {
                    /* try { // try from 00ef9b5c to 00ef9b5f has its CatchHandler @ 00efa4b4 */
    thunk_FUN_00df405c();
    lVar23 = *(long *)puVar13;
  }
  lVar23 = *(long *)(*(long *)(lVar23 + 0xb8) + 0x28);
  if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa398 to 00efa39b has its CatchHandler @ 00efa500 */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar23 + 0x18) <= param_3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa39c to 00efa39f has its CatchHandler @ 00efa4fc */
    FUN_00db0dec();
  }
  lVar24 = (long)(int)param_3;
  lVar23 = *(long *)(lVar23 + lVar24 * 8 + 0x20);
  if ((param_9 != 0) && (*(long *)(param_9 + 0x40) != 0)) {
    lVar23 = *(long *)(param_9 + 0x40);
  }
  if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3a0 to 00efa3a3 has its CatchHandler @ 00efa4f8 */
    FUN_00db0de4();
  }
  uVar21 = *(uint *)(lVar23 + 0x18);
  if (uVar21 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3a4 to 00efa3a7 has its CatchHandler @ 00efa4f4 */
    FUN_00db0dec();
  }
  if (uVar21 == 1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3a8 to 00efa3ab has its CatchHandler @ 00efa4f0 */
    FUN_00db0dec();
  }
  if (uVar21 < 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3ac to 00efa3af has its CatchHandler @ 00efa4ec */
    FUN_00db0dec();
  }
  if (uVar21 == 3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3b0 to 00efa3b3 has its CatchHandler @ 00efa4e8 */
    FUN_00db0dec();
  }
  uVar21 = param_4 - *(int *)(lVar23 + 0x20);
  iVar19 = *(int *)(lVar23 + 0x24) + param_4 + param_6;
  uVar30 = local_74 - *(int *)(lVar23 + 0x28);
  iVar32 = local_74 + param_7 + *(int *)(lVar23 + 0x2c);
  uVar31 = uVar30;
  switch(param_3) {
  case 8:
    if (*(long *)(param_1 + 0x140) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3e8 to 00efa3eb has its CatchHandler @ 00efa450 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef9d84 to 00ef9d8b has its CatchHandler @ 00efa44c */
    lVar23 = kairo_unity_form_FormManagerBase__GetCurrentForm(*(long *)(param_1 + 0x140),0);
    if (*(long *)(param_1 + 0x140) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3ec to 00efa3ef has its CatchHandler @ 00efa444 */
      FUN_00db0de4();
    }
                    /* try { // try from 00ef9d98 to 00ef9d9f has its CatchHandler @ 00efa440 */
    lVar29 = kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    if (lVar23 != lVar29) {
      iVar19 = param_4 + param_6;
    }
    break;
  case 9:
                    /* try { // try from 00ef9d5c to 00ef9d6b has its CatchHandler @ 00efa458 */
    lVar23 = kairo_unity_surface_SurfaceBase__GetComponentId(param_1,8,0);
    if (lVar23 != 0) {
      uVar21 = param_4;
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x188) != '\0') {
      iVar19 = iVar19 + 0x78;
    }
    break;
  case 0xc:
  case 0xf:
                    /* try { // try from 00ef9c10 to 00ef9c1f has its CatchHandler @ 00efa490 */
    uVar27 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,param_3,local_64,0);
    if ((uVar27 & 1) == 0) {
                    /* try { // try from 00ef9e54 to 00ef9e5b has its CatchHandler @ 00efa448 */
      iVar22 = surface_GameView__Get(param_1,local_64);
      if (iVar22 < 1) {
        uVar30 = uVar30 - 0x14;
      }
      if ((param_9 != 0) && (*(long *)(param_9 + 0x38) != 0)) {
                    /* try { // try from 00ef9e78 to 00ef9e7f has its CatchHandler @ 00efa428 */
        iVar22 = surface_GameView__Get(param_1,local_64);
        lVar23 = *(long *)(param_9 + 0x38);
        if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa408 to 00efa40b has its CatchHandler @ 00efa424 */
          FUN_00db0de4();
        }
        if (*(int *)(lVar23 + 0x18) == 1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa40c to 00efa40f has its CatchHandler @ 00efa420 */
          FUN_00db0dec();
        }
        if (*(int *)(lVar23 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa410 to 00efa413 has its CatchHandler @ 00efa41c */
          FUN_00db0dec();
        }
        if (*(int *)(lVar23 + 0x20) - *(int *)(lVar23 + 0x24) <= iVar22) {
          iVar32 = iVar32 + 0x14;
        }
      }
    }
    else {
      if (param_9 == 0) {
                    /* try { // try from 00ef9c34 to 00ef9c43 has its CatchHandler @ 00efa438 */
        param_9 = thunk_FUN_00e11c14(*(undefined8 *)
                                      PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
        kairo_unity_surface_TouchOption___ctor(param_9,0);
        if (param_9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa414 to 00efa417 has its CatchHandler @ 00efa418 */
          FUN_00db0de4();
        }
      }
      *(uint *)(param_9 + 0x10) = *(uint *)(param_9 + 0x10) | 8;
    }
  default:
switchD_00ef9c08_caseD_a:
    uVar31 = uVar30;
    if (param_3 == 0xe) {
                    /* try { // try from 00ef9eb4 to 00ef9ec3 has its CatchHandler @ 00efa488 */
      uVar27 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,0xe,0);
      bVar15 = (uVar27 & 1) == 0;
      iVar22 = iVar32 + 0xf0;
      if (bVar15) {
        iVar22 = iVar32;
      }
      uVar31 = 0;
      iVar32 = iVar22;
      if (bVar15) {
        uVar31 = uVar30;
      }
    }
    break;
  case 0xd:
                    /* try { // try from 00ef9ca8 to 00ef9cb3 has its CatchHandler @ 00efa45c */
    iVar22 = kairo_unity_surface_SurfaceBase__GetComponentLength(param_1,0);
    if (0 < iVar22) {
      iVar17 = 0;
      do {
                    /* try { // try from 00ef9cc4 to 00ef9cd3 has its CatchHandler @ 00efa514 */
        lVar23 = kairo_unity_surface_SurfaceBase__GetComponent(param_1,iVar17,0);
        if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa388 to 00efa38b has its CatchHandler @ 00efa518 */
          FUN_00db0de4();
        }
        uVar31 = uVar30;
        iVar18 = iVar32;
        if ((*(uint *)(lVar23 + 0x18) & 0xfffffffe) == 2) {
          if ((local_64 & 0xffff) == 1) {
            iVar5 = *(int *)(lVar23 + 0x1c);
            iVar18 = *(int *)(lVar23 + 0x20);
            iVar4 = *(int *)(lVar23 + 0x24) + iVar5;
            bVar15 = (int)uVar30 <= *(int *)(lVar23 + 0x28) + iVar18;
            bVar14 = true;
            if (bVar15) {
              bVar14 = (int)(iVar4 - uVar21) < 0;
            }
            bVar15 = bVar14 == (bVar15 && SBORROW4(iVar4,uVar21));
            bVar14 = true;
            if (bVar15) {
              bVar14 = iVar19 - iVar5 < 0;
            }
            bVar15 = bVar14 == (bVar15 && SBORROW4(iVar19,iVar5));
            bVar14 = true;
            if (bVar15) {
              bVar14 = iVar32 - iVar18 < 0;
            }
            if (bVar14 != (bVar15 && SBORROW4(iVar32,iVar18))) {
              iVar18 = iVar32;
            }
          }
          else if ((local_64 & 0xffff) == 0) {
            iVar5 = *(int *)(lVar23 + 0x1c);
            iVar6 = *(int *)(lVar23 + 0x20);
            uVar31 = *(int *)(lVar23 + 0x28) + iVar6;
            iVar4 = *(int *)(lVar23 + 0x24) + iVar5;
            bVar15 = true;
            if ((int)uVar30 <= (int)uVar31) {
              bVar15 = (int)(iVar4 - uVar21) < 0;
            }
            bVar15 = bVar15 == ((int)uVar30 <= (int)uVar31 && SBORROW4(iVar4,uVar21));
            bVar14 = true;
            if (bVar15) {
              bVar14 = iVar19 - iVar5 < 0;
            }
            bVar15 = bVar14 == (bVar15 && SBORROW4(iVar19,iVar5));
            bVar14 = true;
            if (bVar15) {
              bVar14 = iVar32 - iVar6 < 0;
            }
            if (bVar14 != (bVar15 && SBORROW4(iVar32,iVar6))) {
              uVar31 = uVar30;
            }
          }
        }
        iVar32 = iVar18;
        uVar30 = uVar31;
        iVar17 = iVar17 + 1;
      } while (iVar22 != iVar17);
      goto switchD_00ef9c08_caseD_a;
    }
    break;
  case 0x13:
                    /* try { // try from 00ef9db0 to 00ef9dbf has its CatchHandler @ 00efa454 */
    uVar27 = kairo_unity_surface_SurfaceBase__CheckFirstTouch(param_1,0x13,local_64,0);
    fVar33 = DAT_005bcfd0;
    if ((uVar27 & 1) != 0) {
      if (param_9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa404 to 00efa407 has its CatchHandler @ 00efa42c */
        FUN_00db0de4();
      }
      *(uint *)(param_9 + 0x10) = *(uint *)(param_9 + 0x10) | 8;
      fVar35 = (float)(*(int *)(param_1 + 0xbc) * 100) / *(float *)(param_1 + 0xc4) + fVar33;
      fVar33 = (float)(*(int *)(param_1 + 0xc0) * 100) / *(float *)(param_1 + 0xc4) + fVar33;
      iVar19 = -0x80000000;
      if (fVar35 != INFINITY) {
        iVar19 = (int)fVar35;
      }
      uVar31 = 0;
      iVar32 = -0x80000000;
      uVar21 = 0;
      if (fVar33 != INFINITY) {
        iVar32 = (int)fVar33;
      }
    }
  }
  lVar23 = *(long *)puVar13;
  if (*(int *)(lVar23 + 0xe0) == 0) {
                    /* try { // try from 00ef9eec to 00ef9eef has its CatchHandler @ 00efa4b0 */
    thunk_FUN_00df405c();
    lVar23 = *(long *)puVar13;
  }
  lVar23 = *(long *)(*(long *)(lVar23 + 0xb8) + 0x28);
  if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3b4 to 00efa3b7 has its CatchHandler @ 00efa4e4 */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar23 + 0x18) <= param_3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3b8 to 00efa3bf has its CatchHandler @ 00efa508 */
    FUN_00db0dec();
  }
  lVar23 = *(long *)(lVar23 + lVar24 * 8 + 0x20);
  if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar23 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3c0 to 00efa3c3 has its CatchHandler @ 00efa4e0 */
    FUN_00db0dec();
  }
  iVar17 = iVar19;
  iVar22 = iVar32;
  if ((*(int *)(lVar23 + 0x34) == 1) &&
     ((param_9 == 0 || ((*(byte *)(param_9 + 0x10) >> 5 & 1) == 0)))) {
    pfVar1 = (float *)(param_1 + 0xc4);
    if (param_2 != 0) {
      pfVar1 = (float *)(param_2 + 0x5c);
    }
    fVar35 = (float)(*(int *)(param_1 + 0xbc) * 100) / *pfVar1 + DAT_005bcfd0;
    fVar33 = (float)(*(int *)(param_1 + 0xc0) * 100) / *pfVar1 + DAT_005bcfd0;
    iVar17 = -0x80000000;
    if (fVar35 != INFINITY) {
      iVar17 = (int)fVar35;
    }
    iVar22 = -0x80000000;
    if (fVar33 != INFINITY) {
      iVar22 = (int)fVar33;
    }
    if (iVar19 <= iVar17) {
      iVar17 = iVar19;
    }
    uVar21 = uVar21 & ((int)uVar21 >> 0x1f ^ 0xffffffffU);
    uVar31 = uVar31 & ((int)uVar31 >> 0x1f ^ 0xffffffffU);
    if (iVar32 <= iVar22) {
      iVar22 = iVar32;
    }
  }
  iVar17 = iVar17 - uVar21;
  iVar22 = iVar22 - uVar31;
  if (param_2 != 0) {
    if (*(float *)(param_2 + 0x5c) != *(float *)(param_1 + 0xc4)) {
      fVar12 = (float)iVar17;
      fVar33 = *(float *)(param_2 + 0x5c) / *(float *)(param_1 + 0xc4);
      fVar35 = fVar33 * (float)(uVar21 - local_78);
      fVar11 = fVar33 * (float)(uVar31 - local_7c);
      iVar19 = -0x80000000;
      if (fVar35 != INFINITY) {
        iVar19 = (int)fVar35;
      }
      uVar21 = iVar19 + local_78;
      iVar19 = -0x80000000;
      if (fVar11 != INFINITY) {
        iVar19 = (int)fVar11;
      }
      iVar17 = -0x80000000;
      if (fVar33 * fVar12 != INFINITY) {
        iVar17 = (int)(fVar33 * fVar12);
      }
      uVar31 = iVar19 + local_7c;
      iVar22 = -0x80000000;
      if (fVar33 * (float)iVar22 != INFINITY) {
        iVar22 = (int)(fVar33 * (float)iVar22);
      }
    }
  }
                    /* try { // try from 00efa05c to 00efa077 has its CatchHandler @ 00efa4dc */
  lVar23 = kairo_unity_surface_SurfaceBase__AddTouchComponent
                     (param_1,param_3,uVar21,uVar31,iVar17,iVar22,local_64,param_9,0);
  if (lVar23 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3c4 to 00efa3c7 has its CatchHandler @ 00efa510 */
    FUN_00db0de4();
  }
                    /* try { // try from 00efa080 to 00efa0a3 has its CatchHandler @ 00efa510 */
  kairo_unity_surface_TouchComponent__SetPaint(lVar23,param_4,local_74,0);
  lVar29 = *(long *)puVar13;
  if (*(int *)(lVar29 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar29 = *(long *)puVar13;
  }
  lVar29 = *(long *)(*(long *)(lVar29 + 0xb8) + 0x28);
  if (lVar29 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3c8 to 00efa3cb has its CatchHandler @ 00efa4d8 */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar29 + 0x18) <= param_3) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3cc to 00efa3d3 has its CatchHandler @ 00efa504 */
    FUN_00db0dec();
  }
  lVar24 = *(long *)(lVar29 + lVar24 * 8 + 0x20);
  if (lVar24 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar24 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa3d4 to 00efa3d7 has its CatchHandler @ 00efa4d4 */
    FUN_00db0dec();
  }
  uVar21 = 1 << (ulong)(param_3 & 0x1f);
  if (*(int *)(lVar24 + 0x30) != 1) {
    uVar21 = 0;
  }
  if (param_9 != 0) {
    uVar21 = *(uint *)(param_9 + 0x48) | uVar21;
  }
                    /* try { // try from 00efa0fc to 00efa107 has its CatchHandler @ 00efa4d0 */
  iVar19 = kairo_unity_surface_SurfaceBase__GetComponentLength(param_1,0);
  if (0 < iVar19) {
    iVar32 = 0;
    do {
                    /* try { // try from 00efa11c to 00efa12b has its CatchHandler @ 00efa534 */
      lVar24 = kairo_unity_surface_SurfaceBase__GetComponent(param_1,iVar32,0);
      if (lVar24 != lVar23) {
        lVar29 = *(long *)puVar13;
        if (*(int *)(lVar29 + 0xe0) == 0) {
                    /* try { // try from 00efa144 to 00efa147 has its CatchHandler @ 00efa51c */
          thunk_FUN_00df405c();
          lVar29 = *(long *)puVar13;
        }
        if (lVar24 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa374 to 00efa377 has its CatchHandler @ 00efa528 */
          FUN_00db0de4();
        }
        lVar29 = *(long *)(*(long *)(lVar29 + 0xb8) + 0x28);
        if (lVar29 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa364 to 00efa367 has its CatchHandler @ 00efa530 */
          FUN_00db0de4();
        }
        uVar31 = *(uint *)(lVar24 + 0x18);
        if (*(uint *)(lVar29 + 0x18) <= uVar31) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa370 to 00efa373 has its CatchHandler @ 00efa538 */
          FUN_00db0dec();
        }
        lVar29 = *(long *)(lVar29 + (long)(int)uVar31 * 8 + 0x20);
        if (lVar29 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa368 to 00efa36b has its CatchHandler @ 00efa538 */
          FUN_00db0de4();
        }
        if (*(uint *)(lVar29 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efa36c to 00efa36f has its CatchHandler @ 00efa52c */
          FUN_00db0dec();
        }
        uVar30 = 1 << (ulong)(uVar31 & 0x1f);
        uVar31 = uVar30;
        if (*(int *)(lVar29 + 0x30) != 1) {
          uVar31 = 0;
        }
        if (*(long *)(lVar24 + 0x30) != 0) {
          uVar31 = *(uint *)(*(long *)(lVar24 + 0x30) + 0x48) | uVar31;
        }
        if ((1 << (ulong)(*(uint *)(lVar23 + 0x18) & 0x1f) & uVar31 | uVar30 & uVar21) != 0) {
                    /* try { // try from 00efa1bc to 00efa1c7 has its CatchHandler @ 00efa524 */
          iVar22 = kairo_unity_surface_TouchComponent__GetPriority(lVar23,0);
                    /* try { // try from 00efa1cc to 00efa1d7 has its CatchHandler @ 00efa520 */
          iVar17 = kairo_unity_surface_TouchComponent__GetPriority(lVar24,0);
          if (iVar22 == iVar17) {
            iVar17 = *(int *)(lVar23 + 0x20);
            iVar18 = *(int *)(lVar24 + 0x20);
            iVar22 = *(int *)(lVar23 + 0x28) + iVar17;
            if (iVar18 <= iVar22) {
              iVar4 = *(int *)(lVar23 + 0x1c);
              iVar5 = *(int *)(lVar23 + 0x24);
              iVar6 = *(int *)(lVar24 + 0x1c);
              if (((iVar6 <= iVar5 + iVar4) &&
                  (iVar7 = *(int *)(lVar24 + 0x24), iVar4 <= iVar7 + iVar6)) &&
                 (iVar8 = *(int *)(lVar24 + 0x28), iVar17 <= iVar8 + iVar18)) {
                iVar9 = (iVar18 - iVar17) + iVar8;
                if (iVar17 <= iVar18) {
                  iVar9 = iVar22 - iVar18;
                }
                iVar10 = iVar6 - iVar4;
                iVar22 = iVar10 + iVar7;
                if (iVar4 <= iVar6) {
                  iVar22 = (iVar5 + iVar4) - iVar6;
                }
                if (iVar18 == iVar17) {
                  if (*(int *)(lVar23 + 0x28) != iVar8 &&
                      (iVar10 == 0 && iVar5 == iVar7 || iVar9 <= iVar22)) {
LAB_00efa2c0:
                    lVar29 = lVar24;
                    if (iVar17 <= iVar18) {
                      lVar29 = lVar23;
                    }
                    lVar2 = lVar23;
                    if (iVar17 <= iVar18) {
                      lVar2 = lVar24;
                    }
                    iVar22 = iVar9;
                    if (iVar9 < 0) {
                      iVar22 = iVar9 + 1;
                    }
                    *(int *)(lVar29 + 0x28) = *(int *)(lVar29 + 0x28) - (iVar22 >> 1);
                    iVar9 = iVar9 - (iVar22 >> 1);
                    *(int *)(lVar2 + 0x20) = *(int *)(lVar2 + 0x20) + iVar9;
                    *(int *)(lVar2 + 0x28) = *(int *)(lVar2 + 0x28) - iVar9;
                    goto LAB_00efa2fc;
                  }
                }
                else if (iVar10 == 0 && iVar5 == iVar7 || iVar9 <= iVar22) goto LAB_00efa2c0;
                lVar29 = lVar24;
                if (iVar4 <= iVar6) {
                  lVar29 = lVar23;
                }
                lVar2 = lVar23;
                if (iVar4 <= iVar6) {
                  lVar2 = lVar24;
                }
                iVar17 = iVar22;
                if (iVar22 < 0) {
                  iVar17 = iVar22 + 1;
                }
                *(int *)(lVar29 + 0x24) = *(int *)(lVar29 + 0x24) - (iVar17 >> 1);
                iVar22 = iVar22 - (iVar17 >> 1);
                *(int *)(lVar2 + 0x1c) = *(int *)(lVar2 + 0x1c) + iVar22;
                *(int *)(lVar2 + 0x24) = *(int *)(lVar2 + 0x24) - iVar22;
              }
            }
          }
        }
      }
LAB_00efa2fc:
      iVar32 = iVar32 + 1;
    } while (iVar19 != iVar32);
  }
  if (param_2 != 0) {
LAB_00ef9c64:
    kairo_unity_ui_Graphics__SetOrigin((float)local_78,(float)local_7c,param_2,0);
  }
  return lVar23;
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efa5a4
// ==========================================================================================

void surface_GameView__AddTouch(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  long lVar4;
  float fVar5;
  float fVar6;
  
  puVar3 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff731 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff731 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (lVar4 != 0) {
    fVar6 = (float)(*(int *)(lVar4 + 0xbc) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    fVar5 = (float)(*(int *)(lVar4 + 0xc0) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    iVar1 = -0x80000000;
    if (fVar6 != INFINITY) {
      iVar1 = (int)fVar6;
    }
    iVar2 = -0x80000000;
    if (fVar5 != INFINITY) {
      iVar2 = (int)fVar5;
    }
    surface_GameView___addTouch(lVar4,0,param_1,0,0,iVar1,iVar2,param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efa690
// ==========================================================================================

void surface_GameView__AddTouch(undefined4 param_1,undefined8 param_2)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  long lVar4;
  float fVar5;
  float fVar6;
  
  puVar3 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff732 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff732 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (lVar4 != 0) {
    fVar6 = (float)(*(int *)(lVar4 + 0xbc) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    fVar5 = (float)(*(int *)(lVar4 + 0xc0) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    iVar1 = -0x80000000;
    if (fVar6 != INFINITY) {
      iVar1 = (int)fVar6;
    }
    iVar2 = -0x80000000;
    if (fVar5 != INFINITY) {
      iVar2 = (int)fVar5;
    }
    surface_GameView___addTouch(lVar4,0,param_1,0,0,iVar1,iVar2,0,param_2);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efa77c
// ==========================================================================================

void surface_GameView__AddTouch(undefined4 param_1,undefined4 param_2,undefined8 param_3)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  long lVar4;
  float fVar5;
  float fVar6;
  
  puVar3 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff733 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff733 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (lVar4 != 0) {
    fVar6 = (float)(*(int *)(lVar4 + 0xbc) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    fVar5 = (float)(*(int *)(lVar4 + 0xc0) * 100) / *(float *)(lVar4 + 0xc4) + DAT_005bcfd0;
    iVar1 = -0x80000000;
    if (fVar6 != INFINITY) {
      iVar1 = (int)fVar6;
    }
    iVar2 = -0x80000000;
    if (fVar5 != INFINITY) {
      iVar2 = (int)fVar5;
    }
    surface_GameView___addTouch(lVar4,0,param_1,0,0,iVar1,iVar2,param_2,param_3);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efa86c
// ==========================================================================================

void surface_GameView__AddTouch
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff734 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff734 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    surface_GameView___addTouch
              (**(long **)(lVar2 + 0xb8),param_1,param_2,param_3,param_4,param_5,param_6,0,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efa928
// ==========================================================================================

void surface_GameView__AddTouch
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff735 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff735 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    surface_GameView___addTouch
              (**(long **)(lVar2 + 0xb8),param_1,param_2,param_3,param_4,param_5,param_6,param_7,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__DrawImage
// Address: 00efab64
// ==========================================================================================

void surface_GameView__DrawImage
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
               uint param_5)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff752 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff752 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar3 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x20);
  if (lVar3 != 0) {
    if (param_5 < *(uint *)(lVar3 + 0x18)) {
      lVar3 = *(long *)(lVar3 + (long)(int)param_5 * 8 + 0x20);
      if (lVar3 == 0) goto LAB_00efac38;
      if ((5 < *(uint *)(lVar3 + 0x18)) && (*(uint *)(lVar3 + 0x18) != 6)) {
        surface_GameView__DrawScaledImage
                  (param_1,param_2,(float)*(int *)(lVar3 + 0x34) * 0.75,
                   (float)*(int *)(lVar3 + 0x38) * 0.75,lVar2,param_4,param_5);
        return;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00efac38:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efac3c
// ==========================================================================================

void surface_GameView__AddTouch(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff737 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff737 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  do {
    if ((DAT_020ff738 & 1) == 0) {
      FUN_00db0bbc(puVar1);
      DAT_020ff738 = 1;
    }
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
  } while( true );
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efacac
// ==========================================================================================

void surface_GameView__AddTouch(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  do {
    do {
      if ((DAT_020ff738 & 1) == 0) {
        FUN_00db0bbc(puVar1);
        DAT_020ff738 = 1;
      }
    } while (*(int *)(*(long *)puVar1 + 0xe0) != 0);
    thunk_FUN_00df405c();
  } while( true );
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efacec
// ==========================================================================================

long surface_GameView__AddTouch
               (long param_1,undefined4 param_2,undefined8 param_3,int param_4,int param_5,
               undefined4 param_6,undefined4 param_7,undefined4 param_8,undefined4 param_9,
               undefined4 param_10,undefined8 param_11)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  long lVar4;
  
  if ((DAT_020ff739 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff739 = 1;
  }
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if (param_1 != 0) {
    kairo_unity_ui_Graphics__DrawImage
              ((float)param_4,(float)param_5,param_1,param_3,param_6,param_7,param_8,param_9,0);
    lVar4 = *(long *)puVar1;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar1;
    }
    if (**(long **)(lVar4 + 0xb8) != 0) {
      lVar4 = surface_GameView___addTouch
                        (**(long **)(lVar4 + 0xb8),param_1,param_2,param_4,param_5,param_8,param_9,
                         param_10,param_11);
      if (lVar4 != 0) {
        iVar2 = kairo_unity_ui_Graphics__GetOriginX(param_1,0);
        iVar3 = kairo_unity_ui_Graphics__GetOriginY(param_1,0);
        kairo_unity_surface_TouchComponent__SetPaint(lVar4,iVar2 + param_4,iVar3 + param_5,0);
      }
      return lVar4;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efae28
// ==========================================================================================

void surface_GameView__AddTouch
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined8 param_5,undefined4 param_6)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff73a & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff73a = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  surface_GameView__AddTouch(param_1,param_2,param_3,param_4,param_5,param_6,0,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efaed0
// ==========================================================================================

long surface_GameView__AddTouch
               (long param_1,uint param_2,int param_3,int param_4,long param_5,int param_6,
               undefined4 param_7,undefined8 param_8)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  int iVar8;
  int iVar9;
  undefined4 uVar10;
  long *plVar11;
  int iVar12;
  int iVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  
  if ((DAT_020ff73c & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff73c = 1;
  }
  if ((param_5 == 0) ||
     (lVar5 = kairo_unity_ui_Seb__GetBoundingRect(param_5,param_6,0),
     puVar4 = PTR_surface_GameView_TypeInfo_01fbf588, lVar5 == 0)) goto LAB_00efb2c8;
  uVar1 = *(uint *)(lVar5 + 0x18);
  if ((uVar1 == 0) || (((uVar1 == 1 || (uVar1 < 3)) || (uVar1 == 3)))) goto LAB_00efb2c4;
  iVar12 = (int)*(short *)(lVar5 + 0x24);
  iVar9 = (int)*(short *)(lVar5 + 0x26);
  iVar13 = *(short *)(lVar5 + 0x20) + param_3;
  iVar8 = *(short *)(lVar5 + 0x22) + param_4;
  plVar11 = (long *)PTR_surface_GameView_TypeInfo_01fbf588;
  if ((param_1 != 0) && (((param_2 == 1 || (param_2 == 0x12)) || (param_2 - 0x17 < 3)))) {
    lVar6 = *(long *)PTR_surface_GameView_TypeInfo_01fbf588;
    if (*(int *)(lVar6 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar6 = *(long *)puVar4;
    }
    if (**(long **)(lVar6 + 0xb8) == 0) goto LAB_00efb2c8;
    uVar7 = kairo_unity_surface_SurfaceBase__CheckTouch(**(long **)(lVar6 + 0xb8),param_2,param_7,0)
    ;
    if ((uVar7 & 1) == 0) {
      if ((param_6 == 3) || (param_6 == 0)) {
        uVar10 = 0;
      }
      else {
        uVar10 = 1;
      }
    }
    else if ((param_6 == 3) || (param_6 == 0)) {
      uVar10 = 2;
    }
    else {
      uVar10 = 3;
    }
    if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar6 = surface_GameView__GetImageRect(uVar10);
    plVar11 = (long *)PTR_surface_GameView_TypeInfo_01fbf588;
    uVar1 = *(uint *)(lVar5 + 0x18);
    if ((uVar1 == 0) || (uVar1 < 3)) goto LAB_00efb2c4;
    if (lVar6 == 0) goto LAB_00efb2c8;
    uVar2 = *(uint *)(lVar6 + 0x18);
    if ((uVar2 == 0) || (uVar2 < 3)) {
LAB_00efb2c4:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    fVar14 = *(float *)(lVar6 + 0x28);
    fVar16 = (float)((int)*(short *)(lVar5 + 0x20) +
                    ((int)(short)(*(short *)(lVar5 + 0x24) - (*(short *)(lVar5 + 0x24) >> 0xf)) >> 1
                    )) - (*(float *)(lVar6 + 0x20) + fVar14 * 0.5);
    iVar12 = -0x80000000;
    if (fVar16 != INFINITY) {
      iVar12 = (int)fVar16;
    }
    if ((uVar1 < 4) || (uVar2 < 4)) goto LAB_00efb2c4;
    fVar16 = *(float *)(lVar6 + 0x2c);
    param_3 = iVar12 + param_3;
    fVar17 = (float)((int)*(short *)(lVar5 + 0x22) +
                    ((int)(short)(*(short *)(lVar5 + 0x26) - (*(short *)(lVar5 + 0x26) >> 0xf)) >> 1
                    )) - (*(float *)(lVar6 + 0x24) + fVar16 * 0.5);
    iVar12 = -0x80000000;
    if (fVar17 != INFINITY) {
      iVar12 = (int)fVar17;
    }
    param_4 = iVar12 + param_4;
    fVar17 = *(float *)(lVar6 + 0x20) + (float)param_3;
    fVar15 = *(float *)(lVar6 + 0x24) + (float)param_4;
    iVar13 = -0x80000000;
    if (fVar17 != INFINITY) {
      iVar13 = (int)fVar17;
    }
    iVar9 = -0x80000000;
    iVar8 = iVar9;
    if (fVar15 != INFINITY) {
      iVar8 = (int)fVar15;
    }
    iVar12 = iVar9;
    if (fVar14 != INFINITY) {
      iVar12 = (int)fVar14;
    }
    if (fVar16 != INFINITY) {
      iVar9 = (int)fVar16;
    }
    if ((param_2 < 0x1a) && ((1 << (ulong)(param_2 & 0x1f) & 0x3840000U) != 0)) {
      if ((param_2 == 0x18) || (param_2 != 0x19 && (param_6 == 0 || param_6 == 3))) {
        iVar3 = -0x1e;
      }
      else {
        iVar3 = -10;
      }
      iVar13 = iVar13 + iVar3;
      iVar8 = iVar8 + -10;
      iVar12 = iVar12 + 0x28;
      iVar9 = iVar9 + 0x14;
    }
    lVar5 = *(long *)PTR_surface_GameView_TypeInfo_01fbf588;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *plVar11;
    }
    if (**(long **)(lVar5 + 0xb8) == 0) goto LAB_00efb2c8;
    surface_GameView__DrawImage((float)param_3,(float)param_4,lVar5,param_1,uVar10);
  }
  lVar5 = *plVar11;
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar5 = *plVar11;
  }
  if (**(long **)(lVar5 + 0xb8) != 0) {
    lVar5 = surface_GameView___addTouch
                      (**(long **)(lVar5 + 0xb8),param_1,param_2,iVar13,iVar8,iVar12,iVar9,param_7,
                       param_8);
    if (lVar5 != 0) {
      if (param_1 != 0) {
        iVar12 = kairo_unity_ui_Graphics__GetOriginX(param_1,0);
        iVar9 = kairo_unity_ui_Graphics__GetOriginY(param_1,0);
        param_3 = iVar12 + param_3;
        param_4 = iVar9 + param_4;
      }
      kairo_unity_surface_TouchComponent__SetPaint(lVar5,param_3,param_4,param_6,0);
    }
    return lVar5;
  }
LAB_00efb2c8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efb2cc
// ==========================================================================================

void surface_GameView__AddTouch
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined8 param_5,undefined4 param_6,undefined4 param_7)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff73b & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff73b = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  surface_GameView__AddTouch(param_1,param_2,param_3,param_4,param_5,param_6,param_7,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__GetImageRect
// Address: 00efb378
// ==========================================================================================

void surface_GameView__GetImageRect(uint param_1)

{
  uint uVar1;
  uint uVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  
  puVar3 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff754 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff754 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x20);
  if (lVar5 != 0) {
    if (param_1 < *(uint *)(lVar5 + 0x18)) {
      lVar5 = *(long *)(lVar5 + (long)(int)param_1 * 8 + 0x20);
      if (lVar5 == 0) goto LAB_00efb490;
      uVar1 = *(uint *)(lVar5 + 0x18);
      if (1 < uVar1) {
        lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x30);
        if (lVar4 == 0) goto LAB_00efb490;
        uVar2 = *(uint *)(lVar4 + 0x18);
        if (uVar2 != 0) {
          *(float *)(lVar4 + 0x20) = (float)*(int *)(lVar5 + 0x24) * 0.75;
          if ((2 < uVar1) && (1 < uVar2)) {
            *(float *)(lVar4 + 0x24) = (float)*(int *)(lVar5 + 0x28) * 0.75;
            if ((5 < uVar1) && (2 < uVar2)) {
              *(float *)(lVar4 + 0x28) = (float)*(int *)(lVar5 + 0x34) * 0.75;
              if ((6 < uVar1) && (3 < uVar2)) {
                *(float *)(lVar4 + 0x2c) = (float)*(int *)(lVar5 + 0x38) * 0.75;
                return;
              }
            }
          }
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00efb490:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__AddTouch
// Address: 00efb494
// ==========================================================================================

void surface_GameView__AddTouch
               (long param_1,uint param_2,int param_3,int param_4,undefined4 param_5,
               undefined4 param_6,int param_7)

{
  undefined *puVar1;
  undefined uVar2;
  long lVar3;
  ulong uVar4;
  ulong uVar5;
  
  if ((DAT_020ff73d & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff73d = 1;
  }
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if (((param_1 != 0) && (param_2 < 0x18)) && ((1 << (ulong)(param_2 & 0x1f) & 0x840002U) != 0)) {
    lVar3 = *(long *)PTR_surface_GameView_TypeInfo_01fbf588;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    if (**(long **)(lVar3 + 0xb8) == 0) goto LAB_00efb600;
    uVar4 = kairo_unity_surface_SurfaceBase__CheckTouch(**(long **)(lVar3 + 0xb8),param_2,param_7,0)
    ;
    lVar3 = *(long *)puVar1;
    uVar5 = uVar4;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      uVar5 = thunk_FUN_00df405c(lVar3);
      lVar3 = *(long *)puVar1;
    }
    if ((uVar4 & 1) == 0) {
      if (**(long **)(lVar3 + 0xb8) == 0) goto LAB_00efb600;
      uVar2 = param_7 != 0x10;
    }
    else {
      if (**(long **)(lVar3 + 0xb8) == 0) goto LAB_00efb600;
      uVar2 = 2;
      if (param_7 != 0x10) {
        uVar2 = 3;
      }
    }
    surface_GameView__DrawImage((float)param_3,(float)(param_4 + 3),uVar5,param_1,uVar2);
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  if (**(long **)(lVar3 + 0xb8) != 0) {
    surface_GameView___addTouch
              (**(long **)(lVar3 + 0xb8),param_1,param_2,param_3,param_4,param_5,param_6,param_7,0);
    return;
  }
LAB_00efb600:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Get
// Address: 00efb604
// ==========================================================================================

void surface_GameView__Get(long param_1,undefined4 param_2)

{
  undefined8 uVar1;
  
  if (*(long *)(param_1 + 0x140) != 0) {
    uVar1 = kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    surface_GameView__Get(uVar1,uVar1,param_2);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__ClearMarker
// Address: 00efb630
// ==========================================================================================

void surface_GameView__ClearMarker(void)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff741 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff741 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar3 = **(long **)(lVar2 + 0xb8);
  if (lVar3 != 0) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = **(long **)(*(long *)puVar1 + 0xb8);
      if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
    }
    *(undefined8 *)(lVar3 + 0x160) = 0xffffffffffffffff;
    *(undefined4 *)(lVar3 + 0x168) = 0;
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__DrawVerticalScroll
// Address: 00efb6b8
// ==========================================================================================

long surface_GameView__DrawVerticalScroll
               (long param_1,long param_2,int param_3,int param_4,undefined8 param_5,int param_6,
               int param_7,int param_8,int param_9,byte param_10)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined *puVar4;
  undefined4 uVar5;
  undefined8 uVar6;
  long lVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  float fVar10;
  
  puVar4 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if ((DAT_020ff755 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff755 = 1;
  }
  param_6 = param_6 + -1;
  if (param_6 < 2) {
    param_6 = 1;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = kairo_unity_ui_Graphics__GetColorOfRGB(0xd8,0xe6,0xff,0);
  if (param_2 == 0) goto LAB_00efb8f4;
  kairo_unity_ui_Graphics__SetColor(param_2,uVar5,0);
  fVar10 = (float)param_3;
  kairo_unity_ui_Graphics__FillRect(fVar10,(float)param_4,0x40a00000,(float)param_6,param_2,0);
  iVar1 = param_9 + -1;
  if (param_9 + -1 <= param_8) {
    iVar1 = param_8;
  }
  iVar1 = iVar1 + 1;
  iVar2 = 0;
  if (iVar1 != 0) {
    iVar2 = (param_6 * param_7) / iVar1;
  }
  iVar3 = 0;
  if (iVar1 != 0) {
    iVar3 = (param_6 * param_9) / iVar1;
  }
  iVar2 = iVar2 + param_4;
  iVar1 = param_6 - iVar2;
  if (iVar3 + iVar2 <= param_6 + param_4) {
    iVar1 = iVar3;
  }
  if (iVar1 < 1) {
    return 0;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = kairo_unity_ui_Graphics__GetColorOfRGB(0xa1,0xd2,0xff,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar5,0);
  kairo_unity_ui_Graphics__FillRect(fVar10,(float)iVar2,0x40a00000,(float)iVar1,param_2,0);
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    if ((param_10 & 1) != 0) goto LAB_00efb82c;
LAB_00efb84c:
    uVar6 = 0x79;
    uVar8 = 0xa0;
    uVar9 = 0xff;
  }
  else {
    if ((param_10 & 1) == 0) goto LAB_00efb84c;
LAB_00efb82c:
    uVar6 = 0x2f;
    uVar8 = 0xf6;
    uVar9 = 0x5f;
  }
  uVar5 = kairo_unity_ui_Graphics__GetColorOfRGB(uVar6,uVar8,uVar9,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar5,0);
  kairo_unity_ui_Graphics__FillRect
            ((float)(param_3 + 1),(float)iVar2,0x40400000,(float)iVar1,param_2,0);
  kairo_unity_ui_Graphics__FillRect
            (fVar10,(float)(iVar2 + 1),0x40a00000,(float)(iVar1 + -2),param_2,0);
  lVar7 = *(long *)(param_1 + 0x1a8);
  if (lVar7 != 0) {
    if ((*(int *)(lVar7 + 0x18) != 0) &&
       (*(int *)(lVar7 + 0x20) = iVar2, *(int *)(lVar7 + 0x18) != 1)) {
      *(int *)(lVar7 + 0x24) = iVar1;
      return lVar7;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00efb8f4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__CheckMarker
// Address: 00efb8fc
// ==========================================================================================

bool surface_GameView__CheckMarker(undefined4 param_1,undefined4 param_2)

{
  undefined *puVar1;
  bool bVar2;
  long lVar3;
  long lVar4;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff740 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff740 = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  lVar4 = **(long **)(lVar3 + 0xb8);
  if (lVar4 == 0) {
    bVar2 = false;
  }
  else {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = **(long **)(*(long *)puVar1 + 0xb8);
      if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
    }
    lVar4 = *(long *)(lVar4 + 0x160);
    lVar3 = kairo_unity_surface_TouchComponent__GetKey(param_1,param_2,0);
    bVar2 = lVar4 == lVar3;
  }
  return bVar2;
}



// ==========================================================================================
// Function: surface_GameView__AddDelayPaintBuffer
// Address: 00efb9ac
// ==========================================================================================

void surface_GameView__AddDelayPaintBuffer(long param_1,long param_2,long param_3)

{
  int iVar1;
  long lVar2;
  float fVar3;
  
  if ((DAT_020ff758 & 1) == 0) {
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_Method_java_util_Vector_int____Add_01fc0b80);
    DAT_020ff758 = 1;
  }
  if (param_3 != 0) {
    lVar2 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,*(int *)(param_3 + 0x18) + 1);
    Method_System_Array_Copy(param_3,0,lVar2,0,*(undefined4 *)(param_3 + 0x18),0);
    if ((lVar2 != 0) && (param_2 != 0)) {
      if ((int)*(long *)(lVar2 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      fVar3 = *(float *)(param_2 + 0x5c) * 100.0;
      iVar1 = -0x80000000;
      if (fVar3 != INFINITY) {
        iVar1 = (int)fVar3;
      }
      *(int *)(lVar2 + ((*(long *)(lVar2 + 0x18) << 0x20) + -0x100000000 >> 0x1e) + 0x20) = iVar1;
      if (*(long *)(param_1 + 0x198) != 0) {
        Method_java_util_Vector_object__Add
                  (*(long *)(param_1 + 0x198),lVar2,
                   *(undefined8 *)PTR_Method_java_util_Vector_int____Add_01fc0b80);
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__CheckHitRect
// Address: 00efbaa4
// ==========================================================================================

bool surface_GameView__CheckHitRect
               (undefined8 param_1,int param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7,int param_8,int param_9)

{
  bool bVar1;
  
  bVar1 = false;
  if (((param_6 <= param_4 + param_2) && (param_2 <= param_8 + param_6)) &&
     (param_3 <= param_9 + param_7)) {
    bVar1 = param_7 <= param_5 + param_3;
  }
  return bVar1;
}



// ==========================================================================================
// Function: surface_GameView__CheckMarker
// Address: 00efbae0
// ==========================================================================================

bool surface_GameView__CheckMarker(long param_1)

{
  undefined *puVar1;
  bool bVar2;
  long lVar3;
  long lVar4;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff73f & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff73f = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  lVar4 = **(long **)(lVar3 + 0xb8);
  if (lVar4 == 0) {
    bVar2 = false;
  }
  else {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = **(long **)(*(long *)puVar1 + 0xb8);
      if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
    }
    bVar2 = *(long *)(lVar4 + 0x160) == param_1;
  }
  return bVar2;
}



// ==========================================================================================
// Function: surface_GameView__OnKeyDown
// Address: 00efbb74
// ==========================================================================================

void surface_GameView__OnKeyDown(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff742 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff742 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  surface_GameView__ClearMarker();
  return;
}



// ==========================================================================================
// Function: surface_GameView__Set
// Address: 00efbbc0
// ==========================================================================================

void surface_GameView__Set(long param_1,uint param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined8 uVar2;
  long lVar3;
  
  if ((DAT_020ff743 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff743 = 1;
  }
  puVar1 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if (*(long *)(param_1 + 0x140) != 0) {
    uVar2 = kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    lVar3 = kairo_unity_util_BitUtil__Split(param_2,0);
    if (lVar3 != 0) {
      if (1 < *(uint *)(lVar3 + 0x18)) {
        surface_GameView__Set
                  (lVar3,uVar2,param_2 & 0xffff0000,(long)*(short *)(lVar3 + 0x22),param_3);
        return;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__GetTouchValueAccessor
// Address: 00efbc6c
// ==========================================================================================

void surface_GameView__GetTouchValueAccessor(long param_1)

{
  if (*(long *)(param_1 + 0x140) != 0) {
    kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Set
// Address: 00efbc88
// ==========================================================================================

void surface_GameView__Set
               (undefined8 param_1,long *param_2,uint param_3,undefined4 param_4,long param_5)

{
  uint uVar1;
  short sVar2;
  undefined *puVar3;
  undefined *puVar4;
  code **ppcVar5;
  long lVar6;
  long lVar7;
  ulong uVar8;
  long lVar9;
  ulong uVar10;
  int *piVar11;
  
  if ((DAT_020ff745 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88);
    DAT_020ff745 = 1;
  }
  puVar4 = PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88;
  if ((param_3 & 0xffff0000) != 0) {
    if (param_2 == (long *)0x0) {
LAB_00efbe4c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar7 = *param_2;
    uVar10 = (ulong)*(ushort *)(lVar7 + 0x12e);
    if (uVar10 != 0) {
      piVar11 = (int *)(*(long *)(lVar7 + 0xb0) + 8);
      do {
        if (*(long *)(piVar11 + -2) ==
            *(long *)PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88) {
          ppcVar5 = (code **)(lVar7 + (long)(*piVar11 + 1) * 0x10 + 0x138);
          goto LAB_00efbd38;
        }
        uVar10 = uVar10 - 1;
        piVar11 = piVar11 + 4;
      } while (uVar10 != 0);
    }
    ppcVar5 = (code **)FUN_00e0dcd4(param_2,*(long *)
                                             PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88
                                    ,1);
LAB_00efbd38:
    (**ppcVar5)(param_2,param_3 & 0xffff0000,param_4,ppcVar5[1]);
  }
  puVar3 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((((param_5 != 0) && (*(long *)(param_5 + 0x30) != 0)) &&
      (lVar7 = *(long *)(*(long *)(param_5 + 0x30) + 0x50), lVar7 != 0)) &&
     (0 < (int)*(ulong *)(lVar7 + 0x18))) {
    uVar10 = 0;
    uVar8 = *(ulong *)(lVar7 + 0x18) & 0xffffffff;
    do {
      if (uVar8 <= uVar10) {
LAB_00efbe48:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar1 = *(uint *)(lVar7 + uVar10 * 4 + 0x20);
      if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar6 = kairo_unity_util_BitUtil__Split(uVar1,0);
      if (lVar6 == 0) goto LAB_00efbe4c;
      if (*(uint *)(lVar6 + 0x18) < 2) goto LAB_00efbe48;
      if (param_2 == (long *)0x0) goto LAB_00efbe4c;
      lVar9 = *param_2;
      sVar2 = *(short *)(lVar6 + 0x22);
      uVar8 = (ulong)*(ushort *)(lVar9 + 0x12e);
      if (uVar8 != 0) {
        piVar11 = (int *)(*(long *)(lVar9 + 0xb0) + 8);
        do {
          if (*(long *)(piVar11 + -2) == *(long *)puVar4) {
            ppcVar5 = (code **)(lVar9 + (long)(*piVar11 + 1) * 0x10 + 0x138);
            goto LAB_00efbe10;
          }
          uVar8 = uVar8 - 1;
          piVar11 = piVar11 + 4;
        } while (uVar8 != 0);
      }
      ppcVar5 = (code **)FUN_00e0dcd4(param_2,*(long *)puVar4,1);
LAB_00efbe10:
      (**ppcVar5)(param_2,uVar1 & 0xffff0000,(int)sVar2,ppcVar5[1]);
      uVar8 = (ulong)*(uint *)(lVar7 + 0x18);
      uVar10 = uVar10 + 1;
    } while ((long)uVar10 < (long)(int)*(uint *)(lVar7 + 0x18));
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__Set
// Address: 00efbe50
// ==========================================================================================

void surface_GameView__Set(undefined8 param_1,undefined8 param_2,uint param_3,undefined8 param_4)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff744 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff744 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar2 = kairo_unity_util_BitUtil__Split(param_3,0);
  if (lVar2 != 0) {
    if (1 < *(uint *)(lVar2 + 0x18)) {
      surface_GameView__Set
                (lVar2,param_2,param_3 & 0xffff0000,(long)*(short *)(lVar2 + 0x22),param_4);
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Set
// Address: 00efbee4
// ==========================================================================================

void surface_GameView__Set(long param_1,undefined4 param_2,undefined4 param_3,undefined8 param_4)

{
  undefined8 uVar1;
  
  if (*(long *)(param_1 + 0x140) != 0) {
    uVar1 = kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    surface_GameView__Set(uVar1,uVar1,param_2,param_3,param_4);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Get
// Address: 00efbf28
// ==========================================================================================

void surface_GameView__Get(undefined8 param_1,long *param_2,uint param_3)

{
  code **ppcVar1;
  long lVar2;
  ulong uVar3;
  int *piVar4;
  
  if ((DAT_020ff746 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88);
    DAT_020ff746 = 1;
  }
  if (param_2 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  lVar2 = *param_2;
  uVar3 = (ulong)*(ushort *)(lVar2 + 0x12e);
  if (uVar3 != 0) {
    piVar4 = (int *)(*(long *)(lVar2 + 0xb0) + 8);
    do {
      if (*(long *)(piVar4 + -2) ==
          *(long *)PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88) {
        ppcVar1 = (code **)(lVar2 + (long)*piVar4 * 0x10 + 0x138);
        goto LAB_00efbfb0;
      }
      uVar3 = uVar3 - 1;
      piVar4 = piVar4 + 4;
    } while (uVar3 != 0);
  }
  ppcVar1 = (code **)FUN_00e0dcd4(param_2,*(long *)
                                           PTR_kairo_unity_surface_TouchValueAccessor_TypeInfo_01fc0b88
                                  ,0);
LAB_00efbfb0:
                    /* WARNING: Could not recover jumptable at 0x00efbfc8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**ppcVar1)(param_2,param_3 & 0xffff0000,0,ppcVar1[1]);
  return;
}



// ==========================================================================================
// Function: surface_GameView__Join
// Address: 00efbfd0
// ==========================================================================================

void surface_GameView__Join(undefined8 param_1,uint param_2,undefined4 param_3)

{
  undefined *puVar1;
  
  puVar1 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff747 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff747 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (param_2 != (int)(short)param_2) {
    param_2 = param_2 >> 0x10;
  }
  kairo_unity_util_BitUtil__Join(param_2,param_3,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchEvent
// Address: 00efc040
// ==========================================================================================

void surface_GameView__OnTouchEvent(long param_1,long param_2)

{
  byte bVar1;
  undefined *puVar2;
  long *plVar3;
  ulong uVar4;
  long lVar5;
  long lVar6;
  
  if ((DAT_020ff748 & 1) == 0) {
    FUN_00db0bbc(PTR_form_MyFormBase_TypeInfo_01fbf360);
    DAT_020ff748 = 1;
  }
  if ((param_2 != 0) && (*(long *)(param_1 + 0x140) != 0)) {
    lVar6 = *(long *)(param_2 + 0x40);
    plVar3 = (long *)kairo_unity_form_FormManagerBase__GetTopForm(*(long *)(param_1 + 0x140),0);
    puVar2 = PTR_form_MyFormBase_TypeInfo_01fbf360;
    if (plVar3 != (long *)0x0) {
      bVar1 = *(byte *)(*(long *)PTR_form_MyFormBase_TypeInfo_01fbf360 + 0x130);
      if ((bVar1 <= *(byte *)(*plVar3 + 0x130)) &&
         (*(long *)(*(long *)(*plVar3 + 200) + (ulong)bVar1 * 8 + -8) ==
          *(long *)PTR_form_MyFormBase_TypeInfo_01fbf360)) {
        if ((*(long *)(param_1 + 0x140) == 0) ||
           (plVar3 = (long *)kairo_unity_form_FormManagerBase__GetTopForm
                                       (*(long *)(param_1 + 0x140),0), plVar3 == (long *)0x0))
        goto LAB_00efc404;
        lVar5 = *plVar3;
        bVar1 = *(byte *)(*(long *)puVar2 + 0x130);
        if ((*(byte *)(lVar5 + 0x130) < bVar1) ||
           (*(long *)(*(long *)(lVar5 + 200) + (ulong)bVar1 * 8 + -8) != *(long *)puVar2)) {
                    /* WARNING: Subroutine does not return */
          FUN_00db1180();
        }
        uVar4 = (**(code **)(lVar5 + 0x348))(plVar3,param_2,*(undefined8 *)(lVar5 + 0x350));
        if ((uVar4 & 1) == 0) {
          return;
        }
      }
    }
    if (lVar6 != 0) {
      switch(*(undefined4 *)(lVar6 + 0x18)) {
      case 0:
        surface_GameView__OnTouchTitleMenu
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 1:
      case 0x12:
        surface_GameView__OnTouchDlgPage
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 2:
        surface_GameView__OnTouchDlgCmd
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 3:
        surface_GameView__OnTouchDlgSel
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 4:
      case 0x14:
      case 0x15:
        surface_GameView__OnTouchKeyClick
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 5:
        surface_GameView__OnTouchKeyPress
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 6:
        surface_GameView__OnTouchKeyDown
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 7:
        surface_GameView__OnTouchKeyUp
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 8:
        surface_GameView__OnTouchMainMenu
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 9:
        surface_GameView__OnTouchSubMenu
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 10:
        surface_GameView__OnTouchList
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0xb:
        surface_GameView__OnTouchScrollList
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0xc:
      case 0xf:
        surface_GameView__OnTouchVScrollBar
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0xd:
        surface_GameView__OnTouchVScrollButton
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0xe:
        surface_GameView__onTouchBottomBar(param_1,*(undefined4 *)(param_2 + 0x10));
        return;
      case 0x10:
        surface_GameView__OnTouchUnMarker(param_1,*(undefined4 *)(param_2 + 0x10));
        return;
      default:
        return;
      case 0x13:
        surface_GameView__OnTouchTrackBar
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0x16:
        surface_GameView__OnTouchOver
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0x17:
      case 0x18:
      case 0x19:
        surface_GameView__OnTouchArrowPress
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0x1b:
      case 0x1c:
        surface_GameView__OnTouchNextPrev
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0x1d:
        surface_GameView__OnTouchNo
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      case 0x1f:
        surface_GameView__onTouchConcept
                  (param_1,*(undefined4 *)(param_2 + 0x10),*(undefined4 *)(lVar6 + 0x2c),param_2);
        return;
      }
    }
  }
LAB_00efc404:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchTitleMenu
// Address: 00efc40c
// ==========================================================================================

void surface_GameView__OnTouchTitleMenu(long param_1,int param_2,undefined8 param_3,long param_4)

{
  undefined4 uVar1;
  long lVar2;
  
  if (param_2 == 1) {
    if (param_4 != 0) {
      lVar2 = *(long *)(param_1 + 0x130);
      uVar1 = surface_GameView__GetKey(param_1,*(undefined8 *)(param_4 + 0x40),0x100000);
      if (lVar2 != 0) {
        kairo_unity_ui_Canvas__KeyClick(lVar2,uVar1,0);
        return;
      }
    }
  }
  else {
    if (param_2 != 2) {
      return;
    }
    if (param_4 != 0) {
      surface_GameView__Set(param_1,0x30000,param_3,*(undefined8 *)(param_4 + 0x40));
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchDlgPage
// Address: 00efc46c
// ==========================================================================================

void surface_GameView__OnTouchDlgPage(long param_1,int param_2,uint param_3,long param_4)

{
  undefined4 uVar1;
  long lVar2;
  long lVar3;
  
  if (param_4 != 0) {
    lVar2 = *(long *)(param_4 + 0x40);
    if ((param_2 == 10) || (param_2 == 6)) {
      lVar3 = *(long *)(param_1 + 0x130);
      uVar1 = surface_GameView__GetKey(param_1,lVar2,1 << (ulong)(param_3 & 0x1f));
      if (lVar3 != 0) {
        kairo_unity_ui_Canvas__KeyUp(lVar3,uVar1,0);
        return;
      }
    }
    else {
      if (param_2 != 0) {
        return;
      }
      lVar3 = *(long *)(param_1 + 0x130);
      uVar1 = surface_GameView__GetKey(param_1,lVar2,1 << (ulong)(param_3 & 0x1f));
      if ((lVar3 != 0) && (kairo_unity_ui_Canvas__KeyDown(lVar3,uVar1,1,0), lVar2 != 0)) {
        uVar1 = 2;
        if (*(int *)(lVar2 + 0x40) != 3) {
          uVar1 = 3;
        }
        lVar2 = surface_GameView__AddEffect
                          (param_1,0,*(undefined4 *)(lVar2 + 0x38),*(undefined4 *)(lVar2 + 0x3c),
                           uVar1,lVar2);
        if (lVar2 != 0) {
          uVar1 = 0xc1200000;
          if (param_3 != 0x10) {
            uVar1 = 0x41200000;
          }
          *(undefined4 *)(lVar2 + 0x20) = uVar1;
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchDlgCmd
// Address: 00efc550
// ==========================================================================================

void surface_GameView__OnTouchDlgCmd(long param_1,int param_2,undefined4 param_3,long param_4)

{
  undefined4 uVar1;
  undefined8 uVar2;
  long lVar3;
  
  if (1 < param_2 - 1U) {
    return;
  }
  if (param_4 != 0) {
    uVar2 = surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
    if (param_2 != 1) {
      return;
    }
    lVar3 = *(long *)(param_1 + 0x130);
    uVar1 = surface_GameView__GetKey(uVar2,*(undefined8 *)(param_4 + 0x40),0x100000);
    if (lVar3 != 0) {
      kairo_unity_ui_Canvas__KeyClick(lVar3,uVar1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchDlgSel
// Address: 00efc5c8
// ==========================================================================================

void surface_GameView__OnTouchDlgSel(long param_1,int param_2,undefined4 param_3,long param_4)

{
  undefined4 uVar1;
  ulong uVar2;
  undefined8 uVar3;
  long lVar4;
  ulong uVar5;
  
  if (param_4 == 0) {
LAB_00efc68c:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (param_2 - 1U < 2) {
    lVar4 = *(long *)(param_4 + 0x40);
    surface_GameView__Set(param_1,param_3,lVar4);
    if (param_2 == 1) {
      if (lVar4 != 0) {
        uVar2 = kairo_unity_surface_TouchComponent__Check(lVar4,0x10,0);
        if (((uVar2 & 1) == 0) ||
           (uVar5 = *(ulong *)(param_1 + 0x160),
           uVar2 = kairo_unity_surface_TouchComponent__GetKey(lVar4,0), uVar5 == uVar2)) {
          lVar4 = *(long *)(param_1 + 0x130);
          uVar1 = surface_GameView__GetKey(uVar2,*(undefined8 *)(param_4 + 0x40),0x100000);
          if (lVar4 != 0) {
            kairo_unity_ui_Canvas__KeyClick(lVar4,uVar1,0);
            return;
          }
        }
        else if (*(long *)(param_4 + 0x40) != 0) {
          uVar3 = kairo_unity_surface_TouchComponent__GetKey(*(long *)(param_4 + 0x40),0);
          *(undefined8 *)(param_1 + 0x160) = uVar3;
          return;
        }
      }
      goto LAB_00efc68c;
    }
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchKeyClick
// Address: 00efc690
// ==========================================================================================

void surface_GameView__OnTouchKeyClick(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  
  puVar2 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff74a & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff74a = 1;
  }
  uVar1 = 0x14;
  if (param_3 != 0) {
    uVar1 = param_3;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_util_BitUtil__Split(uVar1,0);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if (param_2 != 5) {
      return;
    }
    if (*(short *)(lVar4 + 0x20) == 0) {
      if (param_4 != 0) {
        lVar5 = *(long *)(param_1 + 0x130);
        uVar3 = surface_GameView__GetKey
                          (lVar4,*(undefined8 *)(param_4 + 0x40),1 << (ulong)(uVar1 & 0x1f));
        if (lVar5 != 0) {
          kairo_unity_ui_Canvas__KeyClick(lVar5,uVar3,0);
          return;
        }
      }
    }
    else if (param_4 != 0) {
      surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchKeyPress
// Address: 00efc798
// ==========================================================================================

void surface_GameView__OnTouchKeyPress(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  
  puVar2 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff74b & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff74b = 1;
  }
  uVar1 = 0x14;
  if (param_3 != 0) {
    uVar1 = param_3;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_util_BitUtil__Split(uVar1,0);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if ((param_2 == 10) || (param_2 == 6)) {
      if (*(short *)(lVar4 + 0x20) != 0) {
        return;
      }
      if (param_4 != 0) {
        lVar5 = *(long *)(param_1 + 0x130);
        uVar3 = surface_GameView__GetKey
                          (lVar4,*(undefined8 *)(param_4 + 0x40),1 << (ulong)(uVar1 & 0x1f));
        if (lVar5 != 0) {
          kairo_unity_ui_Canvas__KeyUp(lVar5,uVar3,0);
          return;
        }
      }
    }
    else {
      if (param_2 != 0) {
        return;
      }
      if (*(short *)(lVar4 + 0x20) == 0) {
        if (param_4 != 0) {
          lVar5 = *(long *)(param_1 + 0x130);
          uVar3 = surface_GameView__GetKey
                            (lVar4,*(undefined8 *)(param_4 + 0x40),1 << (ulong)(uVar1 & 0x1f));
          if (lVar5 != 0) {
            kairo_unity_ui_Canvas__KeyDown(lVar5,uVar3,0,0);
            return;
          }
        }
      }
      else if (param_4 != 0) {
        surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchArrowPress
// Address: 00efc8f0
// ==========================================================================================

void surface_GameView__OnTouchArrowPress(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined4 uVar2;
  long lVar3;
  int iVar4;
  undefined8 uVar5;
  long lVar6;
  long lVar7;
  
  if ((DAT_020ff74c & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff74c = 1;
  }
  if (param_4 != 0) {
    lVar7 = *(long *)(param_4 + 0x40);
    uVar1 = 0x14;
    if (param_3 != 0) {
      uVar1 = param_3;
    }
    if (*(int *)(*(long *)PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar3 = kairo_unity_util_BitUtil__Split(uVar1,0);
    if (lVar3 != 0) {
      if (*(int *)(lVar3 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      if (param_2 < 6) {
        if (param_2 == 0) {
          if (*(short *)(lVar3 + 0x20) == 0) {
            lVar6 = *(long *)(param_1 + 0x130);
            lVar7 = *(long *)(param_4 + 0x40);
            iVar4 = 1 << (ulong)(uVar1 & 0x1f);
          }
          else {
            lVar3 = surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
            lVar7 = *(long *)(param_4 + 0x40);
            if (lVar7 == 0) goto LAB_00efcb00;
            if (*(int *)(lVar7 + 0x18) == 0x19) {
              lVar6 = *(long *)(param_1 + 0x130);
              iVar4 = 0x40000;
            }
            else {
              if (*(int *)(lVar7 + 0x18) != 0x18) {
                return;
              }
              lVar6 = *(long *)(param_1 + 0x130);
              iVar4 = 0x10000;
            }
          }
          uVar2 = surface_GameView__GetKey(lVar3,lVar7,iVar4);
          if (lVar6 != 0) {
            kairo_unity_ui_Canvas__KeyDown(lVar6,uVar2,1,0);
            return;
          }
        }
        else {
          if (param_2 != 5) {
            return;
          }
          if (lVar7 != 0) {
            if ((*(int *)(lVar7 + 0x40) == 3) || (*(int *)(lVar7 + 0x40) == 0)) {
              uVar5 = 2;
            }
            else {
              uVar5 = 3;
            }
            if ((param_1 != 0) &&
               (lVar7 = surface_GameView__AddEffect
                                  (param_1,0,*(undefined4 *)(lVar7 + 0x38),
                                   *(undefined4 *)(lVar7 + 0x3c),uVar5,lVar7), lVar7 != 0)) {
              *(undefined4 *)(lVar7 + 0x20) = 0x41200000;
              if (uVar1 != 0x10) {
                if (*(long *)(param_4 + 0x40) == 0) goto LAB_00efcb00;
                if (*(int *)(*(long *)(param_4 + 0x40) + 0x18) != 0x18) {
                  return;
                }
              }
              *(undefined4 *)(lVar7 + 0x20) = 0xc1200000;
              return;
            }
          }
        }
      }
      else {
        if ((param_2 != 6) && (param_2 != 10)) {
          return;
        }
        if (*(short *)(lVar3 + 0x20) == 0) {
          lVar6 = *(long *)(param_1 + 0x130);
          lVar7 = *(long *)(param_4 + 0x40);
          iVar4 = 1 << (ulong)(uVar1 & 0x1f);
        }
        else {
          lVar7 = *(long *)(param_4 + 0x40);
          if (lVar7 == 0) goto LAB_00efcb00;
          if (*(int *)(lVar7 + 0x18) == 0x19) {
            lVar6 = *(long *)(param_1 + 0x130);
            iVar4 = 0x40000;
          }
          else {
            if (*(int *)(lVar7 + 0x18) != 0x18) {
              return;
            }
            lVar6 = *(long *)(param_1 + 0x130);
            iVar4 = 0x10000;
          }
        }
        uVar2 = surface_GameView__GetKey(lVar3,lVar7,iVar4);
        if (lVar6 != 0) {
          kairo_unity_ui_Canvas__KeyUp(lVar6,uVar2,0);
          return;
        }
      }
    }
  }
LAB_00efcb00:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchKeyDown
// Address: 00efcb08
// ==========================================================================================

void surface_GameView__OnTouchKeyDown(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  
  puVar2 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff74d & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff74d = 1;
  }
  uVar1 = 0x14;
  if (param_3 != 0) {
    uVar1 = param_3;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_util_BitUtil__Split(uVar1,0);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if (param_2 != 0) {
      return;
    }
    if (*(short *)(lVar4 + 0x20) == 0) {
      if (param_4 != 0) {
        lVar5 = *(long *)(param_1 + 0x130);
        uVar3 = surface_GameView__GetKey
                          (lVar4,*(undefined8 *)(param_4 + 0x40),1 << (ulong)(uVar1 & 0x1f));
        if (lVar5 != 0) {
          kairo_unity_ui_Canvas__KeyDown(lVar5,uVar3,1,0);
          return;
        }
      }
    }
    else if (param_4 != 0) {
      surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchKeyUp
// Address: 00efcc10
// ==========================================================================================

void surface_GameView__OnTouchKeyUp(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  
  puVar2 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff74e & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff74e = 1;
  }
  uVar1 = 0x14;
  if (param_3 != 0) {
    uVar1 = param_3;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_util_BitUtil__Split(uVar1,0);
  if (lVar4 != 0) {
    if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if (param_2 != 1) {
      return;
    }
    if (*(short *)(lVar4 + 0x20) == 0) {
      if (param_4 != 0) {
        lVar5 = *(long *)(param_1 + 0x130);
        uVar3 = surface_GameView__GetKey
                          (lVar4,*(undefined8 *)(param_4 + 0x40),1 << (ulong)(uVar1 & 0x1f));
        if (lVar5 != 0) {
          kairo_unity_ui_Canvas__KeyDown(lVar5,uVar3,1,0);
          return;
        }
      }
    }
    else if (param_4 != 0) {
      surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchMainMenu
// Address: 00efcd1c
// ==========================================================================================

void surface_GameView__OnTouchMainMenu(long param_1,int param_2,uint param_3,long param_4)

{
  byte bVar1;
  undefined *puVar2;
  int iVar3;
  uint uVar4;
  long lVar5;
  long *plVar6;
  int iVar7;
  
  if ((DAT_020ff74f & 1) == 0) {
    FUN_00db0bbc(PTR_form_SubForm_TypeInfo_01fbf300);
    DAT_020ff74f = 1;
  }
  puVar2 = PTR_form_SubForm_TypeInfo_01fbf300;
  lVar5 = *(long *)(param_1 + 0x140);
  if (lVar5 != 0) {
    iVar7 = 0;
    while (iVar3 = kairo_unity_form_FormManagerBase__GetFormsNum(lVar5,0), iVar7 < iVar3) {
      if ((*(long *)(param_1 + 0x140) == 0) ||
         (plVar6 = (long *)kairo_unity_form_FormManagerBase__GetForm
                                     (*(long *)(param_1 + 0x140),iVar7,0), plVar6 == (long *)0x0))
      goto LAB_00efcde8;
      if (*(int *)(plVar6 + 2) == 4) {
        bVar1 = *(byte *)(*(long *)puVar2 + 0x130);
        if ((*(byte *)(*plVar6 + 0x130) < bVar1) ||
           (*(long *)(*(long *)(*plVar6 + 200) + (ulong)bVar1 * 8 + -8) != *(long *)puVar2)) {
                    /* WARNING: Subroutine does not return */
          FUN_00db1180();
        }
        if (*(int *)(plVar6 + 0x1b) == 3) break;
      }
      lVar5 = *(long *)(param_1 + 0x140);
      iVar7 = iVar7 + 1;
      if (lVar5 == 0) goto LAB_00efcde8;
    }
    if (1 < param_2 - 1U) {
      return;
    }
    lVar5 = kairo_unity_surface_SurfaceBase__GetComponentId(param_1,9,0);
    if (lVar5 == 0) {
      if (param_4 != 0) {
        surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
        if (param_2 != 1) {
          return;
        }
        if (*(long *)(param_1 + 0x130) != 0) {
          kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),0x100000,0);
          return;
        }
      }
    }
    else {
      uVar4 = surface_GameView__Get(param_1,param_3);
      if (uVar4 == (param_3 & 0xffff)) {
        return;
      }
      if ((*(long *)(param_1 + 0x130) != 0) &&
         (kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),0x10000,0), param_4 != 0)) {
        surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
        return;
      }
    }
  }
LAB_00efcde8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchSubMenu
// Address: 00efceb0
// ==========================================================================================

void surface_GameView__OnTouchSubMenu(long param_1,int param_2,undefined4 param_3,long param_4)

{
  undefined4 uVar1;
  undefined8 uVar2;
  long lVar3;
  
  if (1 < param_2 - 1U) {
    return;
  }
  if (param_4 != 0) {
    uVar2 = surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
    if (param_2 != 1) {
      return;
    }
    lVar3 = *(long *)(param_1 + 0x130);
    uVar1 = surface_GameView__GetKey(uVar2,*(undefined8 *)(param_4 + 0x40),0x100000);
    if (lVar3 != 0) {
      kairo_unity_ui_Canvas__KeyClick(lVar3,uVar1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchList
// Address: 00efcf28
// ==========================================================================================

void surface_GameView__OnTouchList(long param_1,int param_2,undefined4 param_3,long param_4)

{
  undefined4 uVar1;
  ulong uVar2;
  undefined8 uVar3;
  long lVar4;
  ulong uVar5;
  
  if (param_4 == 0) {
LAB_00efcfec:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (param_2 - 1U < 2) {
    lVar4 = *(long *)(param_4 + 0x40);
    surface_GameView__Set(param_1,param_3,lVar4);
    if (param_2 == 1) {
      if (lVar4 != 0) {
        uVar2 = kairo_unity_surface_TouchComponent__Check(lVar4,0x10,0);
        if (((uVar2 & 1) == 0) ||
           (uVar5 = *(ulong *)(param_1 + 0x160),
           uVar2 = kairo_unity_surface_TouchComponent__GetKey(lVar4,0), uVar5 == uVar2)) {
          lVar4 = *(long *)(param_1 + 0x130);
          uVar1 = surface_GameView__GetKey(uVar2,*(undefined8 *)(param_4 + 0x40),0x100000);
          if (lVar4 != 0) {
            kairo_unity_ui_Canvas__KeyClick(lVar4,uVar1,0);
            return;
          }
        }
        else if (*(long *)(param_4 + 0x40) != 0) {
          uVar3 = kairo_unity_surface_TouchComponent__GetKey(*(long *)(param_4 + 0x40),0);
          *(undefined8 *)(param_1 + 0x160) = uVar3;
          return;
        }
      }
      goto LAB_00efcfec;
    }
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchScrollList
// Address: 00efcff0
// ==========================================================================================

void surface_GameView__OnTouchScrollList(long param_1,int param_2,undefined4 param_3,long param_4)

{
  undefined4 uVar1;
  ulong uVar2;
  undefined8 uVar3;
  long lVar4;
  ulong uVar5;
  
  if (param_4 == 0) {
LAB_00efd0b4:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (param_2 - 1U < 2) {
    lVar4 = *(long *)(param_4 + 0x40);
    surface_GameView__Set(param_1,param_3,lVar4);
    if (param_2 == 1) {
      if (lVar4 != 0) {
        uVar2 = kairo_unity_surface_TouchComponent__Check(lVar4,0x10,0);
        if (((uVar2 & 1) == 0) ||
           (uVar5 = *(ulong *)(param_1 + 0x160),
           uVar2 = kairo_unity_surface_TouchComponent__GetKey(lVar4,0), uVar5 == uVar2)) {
          lVar4 = *(long *)(param_1 + 0x130);
          uVar1 = surface_GameView__GetKey(uVar2,*(undefined8 *)(param_4 + 0x40),0x100000);
          if (lVar4 != 0) {
            kairo_unity_ui_Canvas__KeyClick(lVar4,uVar1,0);
            return;
          }
        }
        else if (*(long *)(param_4 + 0x40) != 0) {
          uVar3 = kairo_unity_surface_TouchComponent__GetKey(*(long *)(param_4 + 0x40),0);
          *(undefined8 *)(param_1 + 0x160) = uVar3;
          return;
        }
      }
      goto LAB_00efd0b4;
    }
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchVScrollBar
// Address: 00efd0b8
// ==========================================================================================

void surface_GameView__OnTouchVScrollBar
               (undefined8 param_1,int param_2,undefined4 param_3,long param_4)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  long lVar6;
  int iVar7;
  
  if ((((param_4 != 0) && (*(long *)(param_4 + 0x40) != 0)) &&
      (lVar6 = *(long *)(*(long *)(param_4 + 0x40) + 0x30), lVar6 != 0)) &&
     (lVar6 = *(long *)(lVar6 + 0x38), lVar6 != 0)) {
    iVar7 = *(int *)(lVar6 + 0x18);
    if ((iVar7 != 0) && (iVar7 != 1)) {
      if (iVar7 < 3) {
        iVar7 = -1;
      }
      else {
        iVar7 = *(int *)(lVar6 + 0x28);
      }
      iVar1 = *(int *)(lVar6 + 0x20);
      iVar5 = *(int *)(lVar6 + 0x24);
      if (param_2 == 9) {
        uVar4 = *(uint *)(param_4 + 0x20);
      }
      else {
        if (param_2 != 8) {
          return;
        }
        iVar3 = surface_GameView__Get(param_1,param_3);
        uVar4 = *(int *)(param_4 + 0x20) + iVar3;
      }
      if (uVar4 != 0x7fffffff) {
        uVar2 = iVar1 - iVar5;
        if ((int)uVar4 <= (int)uVar2) {
          uVar2 = uVar4;
        }
        uVar2 = uVar2 & ((int)uVar2 >> 0x1f ^ 0xffffffffU);
        uVar4 = surface_GameView__Get(param_1,param_3);
        if (uVar4 != uVar2) {
          iVar5 = surface_GameView__Get(param_1,param_3);
          surface_GameView__Set(param_1,param_3,uVar2,*(undefined8 *)(param_4 + 0x40));
          if (iVar7 != -1) {
            iVar3 = surface_GameView__Get(param_1,iVar7);
            uVar4 = iVar3 + (uVar2 - iVar5);
            uVar4 = uVar4 & ((int)uVar4 >> 0x1f ^ 0xffffffffU);
            if (iVar1 <= (int)uVar4) {
              uVar4 = iVar1 - 1;
            }
            surface_GameView__Set(param_1,iVar7,uVar4,*(undefined8 *)(param_4 + 0x40));
            return;
          }
        }
      }
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchVScrollButton
// Address: 00efd200
// ==========================================================================================

void surface_GameView__OnTouchVScrollButton
               (undefined8 param_1,int param_2,uint param_3,long param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined8 uVar6;
  long lVar7;
  
  if ((((param_4 == 0) || (*(long *)(param_4 + 0x40) == 0)) ||
      (lVar7 = *(long *)(*(long *)(param_4 + 0x40) + 0x30), lVar7 == 0)) ||
     (lVar7 = *(long *)(lVar7 + 0x38), lVar7 == 0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  iVar5 = *(int *)(lVar7 + 0x18);
  if ((iVar5 == 0) || (iVar5 == 1)) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
  if (iVar5 < 3) {
    return;
  }
  if (param_2 != 0xd) {
    return;
  }
  iVar5 = *(int *)(lVar7 + 0x28);
  if (iVar5 == -1) {
    return;
  }
  iVar1 = *(int *)(lVar7 + 0x20);
  iVar2 = *(int *)(lVar7 + 0x24);
  if ((param_3 & 0xffff) == 1) {
    iVar3 = surface_GameView__Get(param_1,iVar5);
    if (iVar1 + -1 <= iVar3) goto LAB_00efd2dc;
    iVar3 = surface_GameView__Get(param_1,iVar5);
    uVar6 = *(undefined8 *)(param_4 + 0x40);
    iVar3 = iVar3 + 1;
  }
  else {
    if (((param_3 & 0xffff) != 0) || (iVar3 = surface_GameView__Get(param_1,iVar5), iVar3 < 1))
    goto LAB_00efd2dc;
    iVar3 = surface_GameView__Get(param_1,iVar5);
    uVar6 = *(undefined8 *)(param_4 + 0x40);
    iVar3 = iVar3 + -1;
  }
  surface_GameView__Set(param_1,iVar5,iVar3,uVar6);
LAB_00efd2dc:
  iVar3 = surface_GameView__Get(param_1,iVar5);
  iVar4 = surface_GameView__Get(param_1,param_3);
  if (iVar4 + iVar2 <= iVar3) {
    iVar3 = surface_GameView__Get(param_1,iVar5);
    surface_GameView__Set(param_1,param_3,(iVar3 - iVar2) + 1,*(undefined8 *)(param_4 + 0x40));
  }
  iVar3 = surface_GameView__Get(param_1,iVar5);
  iVar4 = surface_GameView__Get(param_1,param_3);
  if (iVar4 <= iVar3) goto LAB_00efd38c;
  iVar5 = surface_GameView__Get(param_1,iVar5);
  uVar6 = *(undefined8 *)(param_4 + 0x40);
  while( true ) {
    surface_GameView__Set(param_1,param_3,iVar5,uVar6);
LAB_00efd38c:
    iVar5 = surface_GameView__Get(param_1,param_3);
    if (iVar5 < 1) break;
    iVar5 = surface_GameView__Get(param_1,param_3);
    if (iVar5 + iVar2 <= iVar1) {
      return;
    }
    iVar5 = surface_GameView__Get(param_1,param_3);
    uVar6 = *(undefined8 *)(param_4 + 0x40);
    iVar5 = iVar5 + -1;
  }
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchUnMarker
// Address: 00efd3cc
// ==========================================================================================

void surface_GameView__OnTouchUnMarker(long param_1,int param_2)

{
  long lVar1;
  undefined8 uVar2;
  
  if ((DAT_020ff750 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff750 = 1;
  }
  if (param_2 == 7) {
    lVar1 = *(long *)(param_1 + 0x160);
    if (lVar1 == -1) {
      return;
    }
    uVar2 = 7;
  }
  else if (param_2 == 1) {
    if (*(long *)(param_1 + 0x160) == -1) {
      return;
    }
    lVar1 = kairo_unity_surface_SurfaceBase__GetTouchEventId(param_1,0xc,1,0);
    if (lVar1 != 0) {
      return;
    }
    lVar1 = kairo_unity_surface_SurfaceBase__GetTouchEventId(param_1,0xf,1,0);
    if (lVar1 != 0) {
      return;
    }
    lVar1 = *(long *)(param_1 + 0x160);
    uVar2 = 1;
  }
  else {
    if (param_2 != 0) {
      return;
    }
    *(undefined4 *)(param_1 + 0x168) = 0;
    lVar1 = kairo_unity_surface_SurfaceBase__GetTouchEventId(param_1,0xc,0,0);
    if (lVar1 != 0) {
      return;
    }
    lVar1 = kairo_unity_surface_SurfaceBase__GetTouchEventId(param_1,0xf,0,0);
    if (lVar1 != 0) {
      return;
    }
    lVar1 = *(long *)(param_1 + 0x160);
    if (lVar1 == -1) goto LAB_00efd47c;
    uVar2 = 0;
  }
  lVar1 = kairo_unity_surface_SurfaceBase__GetTouchEventKey(param_1,lVar1,uVar2,0);
  if (lVar1 != 0) {
    return;
  }
LAB_00efd47c:
  if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  surface_GameView__ClearMarker();
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchCamera
// Address: 00efd4f4
// ==========================================================================================

void surface_GameView__OnTouchCamera(void)

{
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnTouchTrackBar
// Address: 00efd4f8
// ==========================================================================================

void surface_GameView__OnTouchTrackBar
               (undefined8 param_1,int param_2,undefined4 param_3,long param_4)

{
  if (param_2 != 9) {
    return;
  }
  if (param_4 != 0) {
    surface_GameView__Set
              (param_1,param_3,*(undefined4 *)(param_4 + 0x1c),*(undefined8 *)(param_4 + 0x40));
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchOver
// Address: 00efd52c
// ==========================================================================================

void surface_GameView__OnTouchOver(undefined8 param_1,int param_2,undefined4 param_3,long param_4)

{
  if (param_2 != 0xd) {
    return;
  }
  if (param_4 != 0) {
    surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchNextPrev
// Address: 00efd55c
// ==========================================================================================

void surface_GameView__OnTouchNextPrev(long param_1,int param_2,uint param_3,long param_4)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  
  puVar2 = PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8;
  if ((DAT_020ff749 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff749 = 1;
  }
  uVar1 = 0x14;
  if (param_3 != 0) {
    uVar1 = param_3;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = kairo_unity_util_BitUtil__Split(uVar1,0);
  if (lVar3 != 0) {
    if (*(int *)(lVar3 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    if ((param_2 == 6) || (param_2 == 10)) {
      if (*(short *)(lVar3 + 0x20) != 0) {
        return;
      }
      if (*(long *)(param_1 + 0x130) != 0) {
        kairo_unity_ui_Canvas__KeyUp(*(long *)(param_1 + 0x130),1 << (ulong)(uVar1 & 0x1f),0);
        return;
      }
    }
    else {
      if (param_2 != 0xd) {
        return;
      }
      if (*(short *)(lVar3 + 0x20) == 0) {
        if (*(long *)(param_1 + 0x130) != 0) {
          kairo_unity_ui_Canvas__KeyDown(*(long *)(param_1 + 0x130),1 << (ulong)(uVar1 & 0x1f),1,0);
          return;
        }
      }
      else if (param_4 != 0) {
        surface_GameView__Set(param_1,uVar1,*(undefined8 *)(param_4 + 0x40));
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__OnTouchNo
// Address: 00efd690
// ==========================================================================================

void surface_GameView__OnTouchNo(undefined8 param_1,int param_2,undefined4 param_3,long param_4)

{
  if (param_2 != 2) {
    return;
  }
  if (param_4 != 0) {
    surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__onTouchBottomBar
// Address: 00efd6c0
// ==========================================================================================

void surface_GameView__onTouchBottomBar(long param_1,int param_2,undefined8 param_3,long param_4)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  
  if (param_2 < 6) {
    if (param_2 != 3) {
      if (param_2 != 5) {
        return;
      }
      iVar1 = surface_GameView__Get(param_1,0x140000);
      if (iVar1 != 0) {
        return;
      }
      lVar2 = *(long *)(param_1 + 0x130);
      if (lVar2 != 0) {
        uVar3 = 0x100000;
        goto LAB_00efd788;
      }
      goto LAB_00efd798;
    }
  }
  else {
    if (param_2 == 8) {
      if (param_4 != 0) {
        surface_GameView__Set(param_1,0x140000,1,*(undefined8 *)(param_4 + 0x40));
        if (*(int *)(param_4 + 0x20) < 0) {
          lVar2 = *(long *)(param_1 + 0x130);
          if (lVar2 != 0) {
            uVar3 = 0x20000;
            goto LAB_00efd788;
          }
        }
        else {
          if (*(int *)(param_4 + 0x20) == 0) {
            return;
          }
          lVar2 = *(long *)(param_1 + 0x130);
          if (lVar2 != 0) {
            uVar3 = 0x80000;
LAB_00efd788:
            kairo_unity_ui_Canvas__KeyClick(lVar2,uVar3,0);
            return;
          }
        }
      }
      goto LAB_00efd798;
    }
    if (param_2 != 10) {
      return;
    }
  }
  if (param_4 != 0) {
    surface_GameView__Set(param_1,0x140000,0,*(undefined8 *)(param_4 + 0x40));
    return;
  }
LAB_00efd798:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__onTouchConcept
// Address: 00efd79c
// ==========================================================================================

void surface_GameView__onTouchConcept(long param_1,int param_2,undefined4 param_3,long param_4)

{
  int iVar1;
  
  if (param_2 == 8) {
    if (param_4 != 0) {
      iVar1 = *(int *)(param_4 + 0x1c);
      if (0 < iVar1) {
        if (*(long *)(param_1 + 0x130) == 0) goto LAB_00efd82c;
        kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),0x40000,0);
        iVar1 = *(int *)(param_4 + 0x1c);
      }
      if (-1 < iVar1) {
        return;
      }
      if (*(long *)(param_1 + 0x130) != 0) {
        kairo_unity_ui_Canvas__KeyClick(*(long *)(param_1 + 0x130),0x10000,0);
        return;
      }
    }
  }
  else {
    if (param_2 != 0) {
      return;
    }
    if (param_4 != 0) {
      surface_GameView__Set(param_1,param_3,*(undefined8 *)(param_4 + 0x40));
      return;
    }
  }
LAB_00efd82c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__GetKey
// Address: 00efd830
// ==========================================================================================

undefined4 surface_GameView__GetKey(undefined8 param_1,long param_2,undefined4 param_3)

{
  long lVar1;
  
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (((*(long *)(param_2 + 0x30) != 0) &&
      (lVar1 = *(long *)(*(long *)(param_2 + 0x30) + 0x58), lVar1 != 0)) &&
     (*(long *)(lVar1 + 0x18) != 0)) {
    if ((int)*(long *)(lVar1 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    param_3 = *(undefined4 *)(lVar1 + 0x20);
  }
  return param_3;
}



// ==========================================================================================
// Function: surface_GameView__AddEffect
// Address: 00efd86c
// ==========================================================================================

void surface_GameView__AddEffect
               (long param_1,undefined4 param_2,int param_3,int param_4,uint param_5,
               undefined8 param_6)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  undefined *puVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  long lVar8;
  long lVar9;
  int iVar10;
  int iVar11;
  float fVar12;
  float fVar13;
  int iVar14;
  
  if ((DAT_020ff756 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_object___TypeInfo_01fc08c0);
    FUN_00db0bbc(PTR_float___TypeInfo_01fc0858);
    DAT_020ff756 = 1;
  }
  puVar4 = PTR_surface_GameView_TypeInfo_01fbf588;
  if (param_5 == 0xffffffff) {
    lVar5 = *(long *)(param_1 + 0x138);
    if (lVar5 != 0) {
      fVar13 = (float)param_3;
      fVar12 = (float)param_4;
      plVar6 = (long *)0x0;
LAB_00efdb3c:
      surface_TouchEffectManager__AddEffect(fVar13,fVar12,lVar5,param_1,param_2,param_6,plVar6,0);
      return;
    }
  }
  else {
    lVar5 = *(long *)PTR_surface_GameView_TypeInfo_01fbf588;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar4;
    }
    lVar5 = *(long *)(lVar5 + 0xb8);
    lVar8 = *(long *)(lVar5 + 0x20);
    if (lVar8 != 0) {
      if (param_5 < *(uint *)(lVar8 + 0x18)) {
        lVar8 = *(long *)(lVar8 + (long)(int)param_5 * 8 + 0x20);
        if (lVar8 == 0) goto LAB_00efdb60;
        if (*(int *)(lVar8 + 0x18) != 0) {
          lVar9 = *(long *)(lVar5 + 8);
          if (lVar9 == 0) goto LAB_00efdb60;
          uVar3 = *(uint *)(lVar8 + 0x20);
          if (uVar3 < *(uint *)(lVar9 + 0x18)) {
            lVar9 = *(long *)(lVar9 + (long)(int)uVar3 * 8 + 0x20);
            if ((lVar9 == 0) || (lVar5 = *(long *)(lVar5 + 0x18), lVar5 == 0)) goto LAB_00efdb60;
            if (uVar3 < *(uint *)(lVar5 + 0x18)) {
              iVar1 = *(int *)(lVar9 + 0x28);
              iVar14 = *(int *)(lVar5 + (long)(int)uVar3 * 4 + 0x20);
              plVar6 = (long *)FUN_00db0c30(*(undefined8 *)PTR_object___TypeInfo_01fc08c0,2);
              if (*(int *)(lVar8 + 0x18) != 0) {
                lVar5 = *(long *)(*(long *)(*(long *)puVar4 + 0xb8) + 8);
                if (lVar5 == 0) goto LAB_00efdb60;
                if (*(uint *)(lVar8 + 0x20) < *(uint *)(lVar5 + 0x18)) {
                  if (plVar6 == (long *)0x0) goto LAB_00efdb60;
                  lVar5 = *(long *)(lVar5 + (long)(int)*(uint *)(lVar8 + 0x20) * 8 + 0x20);
                  if ((lVar5 != 0) &&
                     (lVar9 = thunk_FUN_00e11b18(lVar5,*(undefined8 *)(*plVar6 + 0x40)), lVar9 == 0)
                     ) {
LAB_00efdb64:
                    uVar7 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
                    FUN_00db0cb0(uVar7,0);
                  }
                  puVar4 = PTR_float___TypeInfo_01fc0858;
                  if (*(int *)(plVar6 + 3) != 0) {
                    plVar6[4] = lVar5;
                    lVar5 = FUN_00db0c30(*(undefined8 *)puVar4,6);
                    uVar3 = *(uint *)(lVar8 + 0x18);
                    if (5 < uVar3) {
                      if (lVar5 == 0) goto LAB_00efdb60;
                      uVar2 = *(uint *)(lVar5 + 0x18);
                      if (uVar2 != 0) {
                        iVar10 = *(int *)(lVar8 + 0x34);
                        *(float *)(lVar5 + 0x20) = (float)iVar10 * 0.75;
                        if ((6 < uVar3) && (1 < uVar2)) {
                          iVar11 = *(int *)(lVar8 + 0x38);
                          *(float *)(lVar5 + 0x24) = (float)iVar11 * 0.75;
                          if (uVar2 != 2) {
                            fVar13 = (float)iVar1 / (float)iVar14;
                            *(float *)(lVar5 + 0x28) = fVar13 * (float)*(int *)(lVar8 + 0x2c);
                            if (3 < uVar2) {
                              *(float *)(lVar5 + 0x2c) = fVar13 * (float)*(int *)(lVar8 + 0x30);
                              if (uVar2 != 4) {
                                *(float *)(lVar5 + 0x30) = fVar13 * (float)iVar10;
                                if (5 < uVar2) {
                                  *(float *)(lVar5 + 0x34) = fVar13 * (float)iVar11;
                                  lVar9 = thunk_FUN_00e11b18(lVar5,*(undefined8 *)(*plVar6 + 0x40));
                                  if (lVar9 == 0) goto LAB_00efdb64;
                                  if (1 < *(uint *)(plVar6 + 3)) {
                                    plVar6[5] = lVar5;
                                    if ((1 < *(uint *)(lVar8 + 0x18)) &&
                                       (*(uint *)(lVar8 + 0x18) != 2)) {
                                      lVar5 = *(long *)(param_1 + 0x138);
                                      if (lVar5 != 0) {
                                        fVar13 = (float)*(int *)(lVar8 + 0x24) * 0.75 +
                                                 (float)param_3;
                                        fVar12 = (float)*(int *)(lVar8 + 0x28) * 0.75 +
                                                 (float)param_4;
                                        goto LAB_00efdb3c;
                                      }
                                      goto LAB_00efdb60;
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
LAB_00efdb60:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__Draw
// Address: 00efdb70
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00efdf00) */

void surface_GameView__Draw(long param_1,long param_2)

{
  long lVar1;
  int iVar2;
  int iVar3;
  undefined *puVar4;
  int iVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  float fVar9;
  int local_34;
  
  if ((DAT_020ff751 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff751 = 1;
  }
  local_34 = 0;
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__SetRenderRect
              (param_2,*(undefined4 *)(param_1 + 0xb4),*(undefined4 *)(param_1 + 0xb8),
               *(undefined4 *)(param_1 + 0xbc),*(undefined4 *)(param_1 + 0xc0),0);
    kairo_unity_ui_Graphics__Scale(*(undefined4 *)(param_1 + 0xc4),param_2,0);
    uVar6 = kairo_unity_ui_Graphics__GetFont(param_2,0,0);
                    /* try { // try from 00efdc04 to 00efdc0f has its CatchHandler @ 00efdf0c */
    kairo_unity_ui_Graphics__SetFont(param_2,*(undefined8 *)(param_1 + 0x158),0);
    if (*(long *)(param_1 + 0x140) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00efdf08 to 00efdf0b has its CatchHandler @ 00efdf10 */
      FUN_00db0de4();
    }
                    /* try { // try from 00efdc18 to 00efdc23 has its CatchHandler @ 00efdf10 */
    kairo_unity_form_FormManagerBase__Draw(*(long *)(param_1 + 0x140),param_2,0);
    kairo_unity_ui_Graphics__SetFont(param_2,uVar6,0);
    kairo_unity_ui_Graphics__Scale(0x42c80000,param_2,0);
    kairo_unity_ui_Graphics__ClearRenderRect(param_2,0);
    if (*(int *)(param_1 + 0x18c) != 0) {
      *(int *)(param_1 + 0x18c) = *(int *)(param_1 + 0x18c) + 1;
    }
    puVar4 = PTR_surface_GamePad_TypeInfo_01fc0860;
    if (*(long *)(param_1 + 0x140) != 0) {
      if (*(char *)(*(long *)(param_1 + 0x140) + 0x32) != '\0') {
        return;
      }
      if (*(int *)(*(long *)PTR_surface_GamePad_TypeInfo_01fc0860 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar7 = surface_GamePad__GetInstance();
      if (lVar7 != 0) {
        if (*(char *)(lVar7 + 0x174) != '\0') {
          return;
        }
        if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        lVar7 = surface_GamePad__GetInstance();
        if (lVar7 != 0) {
          if (*(char *)(lVar7 + 0x148) != '\0') {
            kairo_unity_ui_Graphics__SetColor(param_2,0xff,0,0,0);
            fVar9 = (*(float *)(param_1 + 0xc4) * (float)*(int *)(param_1 + 0xf4)) / 100.0 +
                    (float)*(int *)(param_1 + 0xb8);
            kairo_unity_ui_Graphics__DrawLine
                      ((float)*(int *)(param_1 + 0xb4),fVar9,
                       (float)(*(int *)(param_1 + 0xbc) + *(int *)(param_1 + 0xb4)),fVar9,0x3f800000
                       ,param_2,0);
            fVar9 = (*(float *)(param_1 + 0xc4) * (float)*(int *)(param_1 + 0xf0)) / 100.0 +
                    (float)*(int *)(param_1 + 0xb4);
            kairo_unity_ui_Graphics__DrawLine
                      (fVar9,(float)*(int *)(param_1 + 0xb8),fVar9,
                       (float)(*(int *)(param_1 + 0xc0) + *(int *)(param_1 + 0xb8)),0x3f800000,
                       param_2,0);
          }
          puVar4 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
          lVar7 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
          if (*(int *)(lVar7 + 0xe0) == 0) {
            thunk_FUN_00df405c();
            lVar7 = *(long *)puVar4;
          }
          if (*(char *)(*(long *)(lVar7 + 0xb8) + 0xbf) == '\0') {
            return;
          }
          fVar9 = (*(float *)(param_1 + 0xc4) / 100.0) * 10.0;
          iVar5 = -0x80000000;
          if (fVar9 != INFINITY) {
            iVar5 = (int)fVar9;
          }
          kairo_unity_ui_Graphics__PushFont(param_2,iVar5,0);
          if (*(long *)(param_1 + 0x140) != 0) {
            local_34 = *(int *)(*(long *)(param_1 + 0x140) + 0xb4);
            lVar7 = kairo_unity_ui_Graphics__GetFont(param_2,0,0);
            lVar8 = System_Int32__ToString(&local_34,0);
            if (lVar7 != 0) {
              lVar1 = *(long *)PTR_StringLiteral_1_01fbf388;
              if (lVar8 != 0) {
                lVar1 = lVar8;
              }
              iVar5 = kairo_unity_ui_Font__StringWidth(lVar7,lVar1,0);
              iVar2 = *(int *)(param_1 + 0xb4);
              iVar3 = *(int *)(param_1 + 0xb8);
              kairo_unity_ui_Graphics__SetColor(param_2,0,0,0,0);
              kairo_unity_ui_Graphics__SetRenderMode(param_2,1,0x80,0x80,0);
              kairo_unity_ui_Graphics__FillRect
                        ((float)iVar2,(float)iVar3,(float)(iVar5 + 3),fVar9 + 1.0,param_2,0);
              kairo_unity_ui_Graphics__SetRenderMode(param_2,0);
              kairo_unity_ui_Graphics__SetColor(param_2,0xff,0xff,0xff,0);
              if (iVar5 < 0) {
                iVar5 = iVar5 + 1;
              }
              kairo_unity_ui_Graphics__DrawString
                        ((float)(iVar2 + (iVar5 >> 1) + 1),(float)(iVar3 + 1),param_2,(long)local_34
                         ,2,0);
              kairo_unity_ui_Graphics__PopFont(param_2,0);
              return;
            }
          }
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_GameView__RotateClear
// Address: 00efdf84
// ==========================================================================================

void surface_GameView__RotateClear(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff757 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff757 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  surface_GameView__ClearMarker();
  return;
}



// ==========================================================================================
// Function: surface_GameView__OnReceiveTouchEvent
// Address: 00efdfd0
// ==========================================================================================

void surface_GameView__OnReceiveTouchEvent(undefined8 param_1,undefined8 param_2)

{
  kairo_unity_surface_SurfaceBase__OnReceiveTouchEvent(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: surface_GameView__GetMouseWheelMode
// Address: 00efdfd8
// ==========================================================================================

undefined8 surface_GameView__GetMouseWheelMode(void)

{
  return 1;
}



// ==========================================================================================
// Function: surface_GameView___cctor
// Address: 00efdfe0
// ==========================================================================================

void surface_GameView___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  long lVar5;
  undefined8 uVar6;
  long lVar7;
  uint *puVar8;
  
  puVar1 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_020ff759 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_int_____TypeInfo_01fbf5e8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_float___TypeInfo_01fc0858);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__09DCE5B68109D69FE7729C4C08347D87FF40A8A12B353A6558EB1C547749FE3F_01fc0b90
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__0D478B7E3CB0C94A64490FBB26A914097A9F2F2EB5EC44362F84C6F1D44205D8_01fc0b98
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__0F1D94E770E86F934D33E9380692C9AC6E1063F133155F0572DF11C64266BA88_01fc0ba0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__1143430196D8C07F5CC4A264F4AE4D9CB6EFF20A414B9F5A14A9C1C4071DDD47_01fc0ba8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__175AE9923DCB95322E7398B26DCBA91F470C9BCDBAB6F15C801F9384BB936051_01fc0bb0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__1B5E851C43EB70B46171E99A0E27F30A7A310C4769A71FCF9D8081455A436B45_01fc0bb8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__25089026340FA720ACD141D3EA5733122182D842A3C3B9DCCEF05B69B041E153_01fc0bc0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__28DF962F3B3D9EDABECE3C54222E4FCB00092A2B750F7982E05B09E4E9648A8F_01fc0bc8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__291D4725459DF6D1F67CA03C479B11D5B239B3B15BFC72134915C39AF5B89387_01fc0bd0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__2A484E78288870EC0C6AC99000BF5F2059392421EE24CEA554DDC23F783A466F_01fc0bd8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__47FEA97EC28296759586BCDDE4A508C9EAD5C75FC766E234060E0F8BD4F676A1_01fc0be0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__48C168F741687E056C44300E008E5900ABE186579BEF27820ED5FB85F55A59D0_01fc0be8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__4E6A6ACB5EA125FCB105F736C2D6AE04432742D216FF2F8DF2BA2854E6320EE5_01fc0bf0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__55B017B39A8C43A00648432F1E0C0D64FFB8AF35AA8280933A6F52F61B9E3D66_01fc0bf8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__7C3C0135C0731195966FF1074253ADFCE0E23935702E16F3AA68E6E1771A4D26_01fc0c00
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A1BC563D3044B1691DF90531DD6271054E0C89BF92F4D9AA10B3AC6BC2DEE6BD_01fc0c08
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A8F4AEBD9D5155575957F6BAAB3D3CD6E36F7E654246E28BF255E2FB062DAF74_01fc0c10
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__ADE37EDF138B4FAC3EE0C28F070ECC337010AC177898730F705832E2BCFBDC1D_01fc0c18
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__B56513A58D02F4EC3B31F3AEDA7A5C31656C97D79E39C62C9BB77DCA3BA029A5_01fc0c20
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E2D5533B1A6119EB77CF265D53D5461F3287813BE277FAF57C51F67CD5CD4308_01fc0c28
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__EADAA826B6C82565641E16EE3F8AB64D094FC77BE607C0A44E988E2F72D0E9C1_01fc0c30
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__EF57C005A469CC2E3ED2E920E36186CE2354052FFCE1E2F9C5FF61DD6F7F8B74_01fc0c38
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__F78DABD96FE6E2A955EB577353FF465E7DB6F6FCCE5D18FF6A5174D9FE7F99D6_01fc0c40
                );
    FUN_00db0bbc(PTR_StringLiteral_8542_01fc0c48);
    FUN_00db0bbc(PTR_StringLiteral_6931_01fc0c50);
    DAT_020ff759 = 1;
  }
  lVar5 = FUN_00db0c30(*(undefined8 *)puVar1,2);
  if (lVar5 != 0) {
    if ((*(int *)(lVar5 + 0x18) != 0) &&
       (*(undefined8 *)(lVar5 + 0x20) = *(undefined8 *)PTR_StringLiteral_6931_01fc0c50,
       puVar1 = PTR_surface_GameView_TypeInfo_01fbf588, *(int *)(lVar5 + 0x18) != 1)) {
      *(undefined8 *)(lVar5 + 0x28) = *(undefined8 *)PTR_StringLiteral_8542_01fc0c48;
      puVar2 = PTR_int___TypeInfo_01fbf560;
      *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x10) = lVar5;
      lVar5 = FUN_00db0c30(*(undefined8 *)puVar2,2);
      if (lVar5 == 0) goto LAB_00efec8c;
      if ((*(int *)(lVar5 + 0x18) != 0) &&
         (*(undefined4 *)(lVar5 + 0x20) = 0x80, *(int *)(lVar5 + 0x18) != 1)) {
        *(undefined4 *)(lVar5 + 0x24) = 0x3f;
        puVar3 = PTR_int_____TypeInfo_01fbf5e8;
        *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x18) = lVar5;
        puVar4 = 
        PTR_Field__PrivateImplementationDetails__28DF962F3B3D9EDABECE3C54222E4FCB00092A2B750F7982E05B09E4E9648A8F_01fc0bc8
        ;
        lVar5 = FUN_00db0c30(*(undefined8 *)puVar3,0xd);
        uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                  (uVar6,*(undefined8 *)puVar4,0);
        if (lVar5 == 0) goto LAB_00efec8c;
        if (*(int *)(lVar5 + 0x18) != 0) {
          *(undefined8 *)(lVar5 + 0x20) = uVar6;
          puVar4 = 
          PTR_Field__PrivateImplementationDetails__175AE9923DCB95322E7398B26DCBA91F470C9BCDBAB6F15C801F9384BB936051_01fc0bb0
          ;
          uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
          Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                    (uVar6,*(undefined8 *)puVar4,0);
          if (1 < *(uint *)(lVar5 + 0x18)) {
            *(undefined8 *)(lVar5 + 0x28) = uVar6;
            puVar4 = 
            PTR_Field__PrivateImplementationDetails__55B017B39A8C43A00648432F1E0C0D64FFB8AF35AA8280933A6F52F61B9E3D66_01fc0bf8
            ;
            uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
            Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                      (uVar6,*(undefined8 *)puVar4,0);
            if (2 < *(uint *)(lVar5 + 0x18)) {
              *(undefined8 *)(lVar5 + 0x30) = uVar6;
              puVar4 = 
              PTR_Field__PrivateImplementationDetails__7C3C0135C0731195966FF1074253ADFCE0E23935702E16F3AA68E6E1771A4D26_01fc0c00
              ;
              uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
              Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                        (uVar6,*(undefined8 *)puVar4,0);
              if (3 < *(uint *)(lVar5 + 0x18)) {
                *(undefined8 *)(lVar5 + 0x38) = uVar6;
                puVar4 = 
                PTR_Field__PrivateImplementationDetails__09DCE5B68109D69FE7729C4C08347D87FF40A8A12B353A6558EB1C547749FE3F_01fc0b90
                ;
                uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                          (uVar6,*(undefined8 *)puVar4,0);
                if (4 < *(uint *)(lVar5 + 0x18)) {
                  *(undefined8 *)(lVar5 + 0x40) = uVar6;
                  puVar4 = 
                  PTR_Field__PrivateImplementationDetails__0F1D94E770E86F934D33E9380692C9AC6E1063F133155F0572DF11C64266BA88_01fc0ba0
                  ;
                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                            (uVar6,*(undefined8 *)puVar4,0);
                  if (5 < *(uint *)(lVar5 + 0x18)) {
                    *(undefined8 *)(lVar5 + 0x48) = uVar6;
                    puVar4 = 
                    PTR_Field__PrivateImplementationDetails__A1BC563D3044B1691DF90531DD6271054E0C89BF92F4D9AA10B3AC6BC2DEE6BD_01fc0c08
                    ;
                    uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                    Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                              (uVar6,*(undefined8 *)puVar4,0);
                    if (6 < *(uint *)(lVar5 + 0x18)) {
                      *(undefined8 *)(lVar5 + 0x50) = uVar6;
                      puVar4 = 
                      PTR_Field__PrivateImplementationDetails__0D478B7E3CB0C94A64490FBB26A914097A9F2F2EB5EC44362F84C6F1D44205D8_01fc0b98
                      ;
                      uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                (uVar6,*(undefined8 *)puVar4,0);
                      if (7 < *(uint *)(lVar5 + 0x18)) {
                        *(undefined8 *)(lVar5 + 0x58) = uVar6;
                        puVar4 = 
                        PTR_Field__PrivateImplementationDetails__1B5E851C43EB70B46171E99A0E27F30A7A310C4769A71FCF9D8081455A436B45_01fc0bb8
                        ;
                        uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                  (uVar6,*(undefined8 *)puVar4,0);
                        if (8 < *(uint *)(lVar5 + 0x18)) {
                          *(undefined8 *)(lVar5 + 0x60) = uVar6;
                          puVar4 = 
                          PTR_Field__PrivateImplementationDetails__ADE37EDF138B4FAC3EE0C28F070ECC337010AC177898730F705832E2BCFBDC1D_01fc0c18
                          ;
                          uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                          Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                    (uVar6,*(undefined8 *)puVar4,0);
                          if (9 < *(uint *)(lVar5 + 0x18)) {
                            *(undefined8 *)(lVar5 + 0x68) = uVar6;
                            puVar4 = 
                            PTR_Field__PrivateImplementationDetails__A8F4AEBD9D5155575957F6BAAB3D3CD6E36F7E654246E28BF255E2FB062DAF74_01fc0c10
                            ;
                            uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                            Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                      (uVar6,*(undefined8 *)puVar4,0);
                            if (10 < *(uint *)(lVar5 + 0x18)) {
                              *(undefined8 *)(lVar5 + 0x70) = uVar6;
                              puVar4 = 
                              PTR_Field__PrivateImplementationDetails__2A484E78288870EC0C6AC99000BF5F2059392421EE24CEA554DDC23F783A466F_01fc0bd8
                              ;
                              uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                              Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                        (uVar6,*(undefined8 *)puVar4,0);
                              if (0xb < *(uint *)(lVar5 + 0x18)) {
                                *(undefined8 *)(lVar5 + 0x78) = uVar6;
                                puVar4 = 
                                PTR_Field__PrivateImplementationDetails__1143430196D8C07F5CC4A264F4AE4D9CB6EFF20A414B9F5A14A9C1C4071DDD47_01fc0ba8
                                ;
                                uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,7);
                                Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                          (uVar6,*(undefined8 *)puVar4,0);
                                if (0xc < *(uint *)(lVar5 + 0x18)) {
                                  *(undefined8 *)(lVar5 + 0x80) = uVar6;
                                  *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x20) = lVar5;
                                  puVar4 = 
                                  PTR_Field__PrivateImplementationDetails__25089026340FA720ACD141D3EA5733122182D842A3C3B9DCCEF05B69B041E153_01fc0bc0
                                  ;
                                  lVar5 = FUN_00db0c30(*(undefined8 *)puVar3,0x22);
                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                            (uVar6,*(undefined8 *)puVar4,0);
                                  if (lVar5 == 0) goto LAB_00efec8c;
                                  puVar8 = (uint *)(lVar5 + 0x18);
                                  if (*puVar8 != 0) {
                                    *(undefined8 *)(lVar5 + 0x20) = uVar6;
                                    puVar3 = 
                                    PTR_Field__PrivateImplementationDetails__47FEA97EC28296759586BCDDE4A508C9EAD5C75FC766E234060E0F8BD4F676A1_01fc0be0
                                    ;
                                    uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                    Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                              (uVar6,*(undefined8 *)puVar3,0);
                                    if (1 < *(uint *)(lVar5 + 0x18)) {
                                      *(undefined8 *)(lVar5 + 0x28) = uVar6;
                                      puVar3 = 
                                      PTR_Field__PrivateImplementationDetails__291D4725459DF6D1F67CA03C479B11D5B239B3B15BFC72134915C39AF5B89387_01fc0bd0
                                      ;
                                      uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                (uVar6,*(undefined8 *)puVar3,0);
                                      if (2 < *(uint *)(lVar5 + 0x18)) {
                                        *(undefined8 *)(lVar5 + 0x30) = uVar6;
                                        puVar3 = 
                                        PTR_Field__PrivateImplementationDetails__EADAA826B6C82565641E16EE3F8AB64D094FC77BE607C0A44E988E2F72D0E9C1_01fc0c30
                                        ;
                                        uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                  (uVar6,*(undefined8 *)puVar3,0);
                                        if (3 < *(uint *)(lVar5 + 0x18)) {
                                          *(undefined8 *)(lVar5 + 0x38) = uVar6;
                                          lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                          if (lVar7 == 0) goto LAB_00efec8c;
                                          if (5 < *(uint *)(lVar7 + 0x18)) {
                                            *(undefined4 *)(lVar7 + 0x34) = 1;
                                            if (4 < *puVar8) {
                                              *(long *)(lVar5 + 0x40) = lVar7;
                                              lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                              if (lVar7 == 0) goto LAB_00efec8c;
                                              if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                 (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                 *(uint *)(lVar7 + 0x18) != 5)) {
                                                *(undefined4 *)(lVar7 + 0x34) = 1;
                                                if (5 < *puVar8) {
                                                  *(long *)(lVar5 + 0x48) = lVar7;
                                                  lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  if (lVar7 == 0) goto LAB_00efec8c;
                                                  if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                     (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                     *(uint *)(lVar7 + 0x18) != 5)) {
                                                    *(undefined4 *)(lVar7 + 0x34) = 1;
                                                    if (6 < *puVar8) {
                                                      *(long *)(lVar5 + 0x50) = lVar7;
                                                      lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                      if (lVar7 == 0) goto LAB_00efec8c;
                                                      if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                         (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                         *(uint *)(lVar7 + 0x18) != 5)) {
                                                        *(undefined4 *)(lVar7 + 0x34) = 1;
                                                        if (7 < *puVar8) {
                                                          *(long *)(lVar5 + 0x58) = lVar7;
                                                          puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__48C168F741687E056C44300E008E5900ABE186579BEF27820ED5FB85F55A59D0_01fc0be8
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (8 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x60) = uVar6;
                                                    puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__E2D5533B1A6119EB77CF265D53D5461F3287813BE277FAF57C51F67CD5CD4308_01fc0c28
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (9 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x68) = uVar6;
                                                    puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__4E6A6ACB5EA125FCB105F736C2D6AE04432742D216FF2F8DF2BA2854E6320EE5_01fc0bf0
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (10 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x70) = uVar6;
                                                    puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__F78DABD96FE6E2A955EB577353FF465E7DB6F6FCCE5D18FF6A5174D9FE7F99D6_01fc0c40
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (0xb < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x78) = uVar6;
                                                    puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__B56513A58D02F4EC3B31F3AEDA7A5C31656C97D79E39C62C9BB77DCA3BA029A5_01fc0c20
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (0xc < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x80) = uVar6;
                                                    uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                    if (0xd < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x88) = uVar6;
                                                      lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                      if (lVar7 == 0) goto LAB_00efec8c;
                                                      if (5 < *(uint *)(lVar7 + 0x18)) {
                                                        *(undefined4 *)(lVar7 + 0x34) = 1;
                                                        if (0xe < *puVar8) {
                                                          *(long *)(lVar5 + 0x90) = lVar7;
                                                          uVar6 = FUN_00db0c30(*(undefined8 *)puVar2
                                                                               ,6);
                                                                                                                    
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (0xf < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x98) = uVar6;
                                                    lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                    if (lVar7 == 0) goto LAB_00efec8c;
                                                    if (5 < *(uint *)(lVar7 + 0x18)) {
                                                      *(undefined4 *)(lVar7 + 0x34) = 1;
                                                      if (0x10 < *puVar8) {
                                                        *(long *)(lVar5 + 0xa0) = lVar7;
                                                        lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6
                                                                            );
                                                        if (lVar7 == 0) goto LAB_00efec8c;
                                                        if (5 < *(uint *)(lVar7 + 0x18)) {
                                                          *(undefined4 *)(lVar7 + 0x34) = 1;
                                                          if (0x11 < *puVar8) {
                                                            *(long *)(lVar5 + 0xa8) = lVar7;
                                                            lVar7 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar2,6);
                                                            if (lVar7 == 0) goto LAB_00efec8c;
                                                            if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                               (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                               *(uint *)(lVar7 + 0x18) != 5)) {
                                                              *(undefined4 *)(lVar7 + 0x34) = 1;
                                                              if (0x12 < *puVar8) {
                                                                *(long *)(lVar5 + 0xb0) = lVar7;
                                                                uVar6 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar2,6);
                                                                if (0x13 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0xb8) =
                                                                       uVar6;
                                                                  lVar7 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar2,6)
                                                                  ;
                                                                  if (lVar7 == 0) goto LAB_00efec8c;
                                                                  if ((4 < *(uint *)(lVar7 + 0x18))
                                                                     && (*(undefined4 *)
                                                                          (lVar7 + 0x30) = 1,
                                                                        *(uint *)(lVar7 + 0x18) != 5
                                                                        )) {
                                                                    *(undefined4 *)(lVar7 + 0x34) =
                                                                         1;
                                                                    if (0x14 < *puVar8) {
                                                                      *(long *)(lVar5 + 0xc0) =
                                                                           lVar7;
                                                                      lVar7 = FUN_00db0c30(*(
                                                  undefined8 *)puVar2,6);
                                                  if (lVar7 == 0) goto LAB_00efec8c;
                                                  if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                     (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                     *(uint *)(lVar7 + 0x18) != 5)) {
                                                    *(undefined4 *)(lVar7 + 0x34) = 1;
                                                    if (0x15 < *puVar8) {
                                                      *(long *)(lVar5 + 200) = lVar7;
                                                      lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                      if (lVar7 == 0) goto LAB_00efec8c;
                                                      if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                         (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                         *(uint *)(lVar7 + 0x18) != 5)) {
                                                        *(undefined4 *)(lVar7 + 0x34) = 1;
                                                        if (0x16 < *puVar8) {
                                                          *(long *)(lVar5 + 0xd0) = lVar7;
                                                          lVar7 = FUN_00db0c30(*(undefined8 *)puVar2
                                                                               ,6);
                                                          if (lVar7 == 0) goto LAB_00efec8c;
                                                          if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                             (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                             *(uint *)(lVar7 + 0x18) != 5)) {
                                                            *(undefined4 *)(lVar7 + 0x34) = 1;
                                                            if (0x17 < *puVar8) {
                                                              *(long *)(lVar5 + 0xd8) = lVar7;
                                                              lVar7 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar2,6);
                                                              if (lVar7 == 0) goto LAB_00efec8c;
                                                              if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                                 (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                                 *(uint *)(lVar7 + 0x18) != 5)) {
                                                                *(undefined4 *)(lVar7 + 0x34) = 1;
                                                                if (0x18 < *puVar8) {
                                                                  *(long *)(lVar5 + 0xe0) = lVar7;
                                                                  lVar7 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar2,6)
                                                                  ;
                                                                  if (lVar7 == 0) goto LAB_00efec8c;
                                                                  if ((4 < *(uint *)(lVar7 + 0x18))
                                                                     && (*(undefined4 *)
                                                                          (lVar7 + 0x30) = 1,
                                                                        *(uint *)(lVar7 + 0x18) != 5
                                                                        )) {
                                                                    *(undefined4 *)(lVar7 + 0x34) =
                                                                         1;
                                                                    if (0x19 < *puVar8) {
                                                                      *(long *)(lVar5 + 0xe8) =
                                                                           lVar7;
                                                                      lVar7 = FUN_00db0c30(*(
                                                  undefined8 *)puVar2,6);
                                                  if (lVar7 == 0) goto LAB_00efec8c;
                                                  if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                     (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                     *(uint *)(lVar7 + 0x18) != 5)) {
                                                    *(undefined4 *)(lVar7 + 0x34) = 1;
                                                    if (0x1a < *puVar8) {
                                                      *(long *)(lVar5 + 0xf0) = lVar7;
                                                      lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                      if (lVar7 == 0) goto LAB_00efec8c;
                                                      if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                         (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                         *(uint *)(lVar7 + 0x18) != 5)) {
                                                        *(undefined4 *)(lVar7 + 0x34) = 1;
                                                        if (0x1b < *puVar8) {
                                                          *(long *)(lVar5 + 0xf8) = lVar7;
                                                          lVar7 = FUN_00db0c30(*(undefined8 *)puVar2
                                                                               ,6);
                                                          if (lVar7 == 0) goto LAB_00efec8c;
                                                          if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                             (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                             *(uint *)(lVar7 + 0x18) != 5)) {
                                                            *(undefined4 *)(lVar7 + 0x34) = 1;
                                                            if (0x1c < *puVar8) {
                                                              *(long *)(lVar5 + 0x100) = lVar7;
                                                              lVar7 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar2,6);
                                                              if (lVar7 == 0) goto LAB_00efec8c;
                                                              if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                                 (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                                 *(uint *)(lVar7 + 0x18) != 5)) {
                                                                *(undefined4 *)(lVar7 + 0x34) = 1;
                                                                if (0x1d < *puVar8) {
                                                                  *(long *)(lVar5 + 0x108) = lVar7;
                                                                  uVar6 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar2,6)
                                                                  ;
                                                                  if (0x1e < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x110) =
                                                                         uVar6;
                                                                    puVar3 = 
                                                  PTR_Field__PrivateImplementationDetails__EF57C005A469CC2E3ED2E920E36186CE2354052FFCE1E2F9C5FF61DD6F7F8B74_01fc0c38
                                                  ;
                                                  uVar6 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                                            (uVar6,*(undefined8 *)puVar3,0);
                                                  if (0x1f < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x118) = uVar6;
                                                    lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                                                    if (lVar7 == 0) goto LAB_00efec8c;
                                                    if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                       (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                       *(uint *)(lVar7 + 0x18) != 5)) {
                                                      *(undefined4 *)(lVar7 + 0x34) = 1;
                                                      if (0x20 < *puVar8) {
                                                        *(long *)(lVar5 + 0x120) = lVar7;
                                                        lVar7 = FUN_00db0c30(*(undefined8 *)puVar2,6
                                                                            );
                                                        if (lVar7 == 0) goto LAB_00efec8c;
                                                        if ((4 < *(uint *)(lVar7 + 0x18)) &&
                                                           (*(undefined4 *)(lVar7 + 0x30) = 1,
                                                           *(uint *)(lVar7 + 0x18) != 5)) {
                                                          *(undefined4 *)(lVar7 + 0x34) = 1;
                                                          if (0x21 < *puVar8) {
                                                            *(long *)(lVar5 + 0x128) = lVar7;
                                                            puVar2 = PTR_float___TypeInfo_01fc0858;
                                                            *(long *)(*(long *)(*(long *)puVar1 +
                                                                               0xb8) + 0x28) = lVar5
                                                            ;
                                                            uVar6 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar2,4);
                                                            *(undefined8 *)
                                                             (*(long *)(*(long *)puVar1 + 0xb8) +
                                                             0x30) = uVar6;
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
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00efec8c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_SurfaceManager___ctor
// Address: 00f72ec4
// ==========================================================================================

void surface_SurfaceManager___ctor(undefined8 param_1)

{
  kairo_unity_surface_SurfaceManagerBase___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: surface_SurfaceManager__Setup
// Address: 00f72ecc
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f7314c) */
/* WARNING: Removing unreachable block (ram,0x00f73264) */

void surface_SurfaceManager__Setup(void)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  int iVar5;
  undefined8 uVar6;
  long lVar7;
  ulong uVar8;
  long lVar9;
  
  puVar3 = PTR_surface_SurfaceManager_TypeInfo_01fc08d8;
  if ((DAT_020ff7da & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_system_surface_GameBanner_TypeInfo_01fbf4d8);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_kairo_unity_util_JarInflater_TypeInfo_01fbf510);
    FUN_00db0bbc(PTR_kairo_unity_io_Storage_TypeInfo_01fbf4f8);
    FUN_00db0bbc(PTR_surface_SurfaceManager_TypeInfo_01fc08d8);
    FUN_00db0bbc(PTR_Method_java_util_Vector_SurfaceBase__Add_01fc3240);
    FUN_00db0bbc(PTR_StringLiteral_9203_01fc3248);
    DAT_020ff7da = 1;
  }
  if (**(long **)(*(long *)puVar3 + 0xb8) != 0) {
    return;
  }
  uVar6 = thunk_FUN_00e11c14();
  kairo_unity_surface_SurfaceManagerBase___ctor(uVar6,0);
  **(undefined8 **)(*(long *)puVar3 + 0xb8) = uVar6;
  puVar2 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (*(int *)(*(long *)PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  lVar7 = *(long *)puVar2;
  if (*(int *)(lVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar7 = *(long *)puVar2;
  }
  lVar7 = **(long **)(lVar7 + 0xb8);
  if (lVar7 != 0) {
    uVar8 = kairo_unity_ui_IApplication__IsSide(lVar7,0);
    lVar9 = **(long **)(*(long *)puVar3 + 0xb8);
    iVar4 = kairo_unity_ui_IApplication__GetWidth(lVar7,0);
    iVar5 = kairo_unity_ui_IApplication__GetHeight(lVar7,0);
    if (lVar9 != 0) {
      bVar1 = iVar4 < iVar5;
      if ((uVar8 & 1) == 0) {
        bVar1 = iVar5 < iVar4;
      }
      *(bool *)(lVar9 + 0x38) = bVar1;
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar7 = kairo_unity_ui_Canvas__GetInstance(0);
      if (lVar7 != 0) {
        *(undefined8 *)(lVar7 + 0x28) = **(undefined8 **)(*(long *)puVar3 + 0xb8);
        if (*(int *)(*(long *)PTR_kairo_unity_io_Storage_TypeInfo_01fbf4f8 + 0xe0) == 0) {
                    /* try { // try from 00f7309c to 00f7309f has its CatchHandler @ 00f7326c */
          thunk_FUN_00df405c();
        }
                    /* try { // try from 00f730ac to 00f730bb has its CatchHandler @ 00f73270 */
        uVar6 = kairo_unity_io_Storage__Read(3,0,*(undefined8 *)PTR_StringLiteral_9203_01fc3248,0);
                    /* try { // try from 00f730cc to 00f730df has its CatchHandler @ 00f73288 */
        lVar7 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_util_JarInflater_TypeInfo_01fbf510
                                  );
        Method_kairo_unity_util_JarInflater__ctor(lVar7,uVar6,0);
        if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
                    /* try { // try from 00f730f4 to 00f73103 has its CatchHandler @ 00f73280 */
          thunk_FUN_00df405c();
        }
        surface_GameView__Load(lVar7,0);
        if (*(int *)(*(long *)PTR_surface_GamePad_TypeInfo_01fc0860 + 0xe0) == 0) {
                    /* try { // try from 00f73118 to 00f73127 has its CatchHandler @ 00f7327c */
          thunk_FUN_00df405c();
        }
        surface_GamePad__Load(lVar7,0);
        if (lVar7 != 0) {
          kairo_unity_util_JarInflater__Close(lVar7,0);
        }
        if (**(long **)(*(long *)puVar3 + 0xb8) != 0) {
          lVar7 = *(long *)(**(long **)(*(long *)puVar3 + 0xb8) + 0x10);
          if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          uVar6 = surface_GameView__GetInstance(0);
          *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 8) = uVar6;
          puVar2 = PTR_Method_java_util_Vector_SurfaceBase__Add_01fc3240;
          if (lVar7 != 0) {
            Method_java_util_Vector_object__Add
                      (lVar7,uVar6,
                       *(undefined8 *)PTR_Method_java_util_Vector_SurfaceBase__Add_01fc3240);
            if (**(long **)(*(long *)puVar3 + 0xb8) != 0) {
              lVar7 = *(long *)(**(long **)(*(long *)puVar3 + 0xb8) + 0x10);
              if (*(int *)(*(long *)PTR_surface_GamePad_TypeInfo_01fc0860 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar6 = surface_GamePad__GetInstance(0);
              *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x10) = uVar6;
              if (lVar7 != 0) {
                Method_java_util_Vector_object__Add(lVar7,uVar6,*(undefined8 *)puVar2);
                if (**(long **)(*(long *)puVar3 + 0xb8) != 0) {
                  lVar7 = *(long *)(**(long **)(*(long *)puVar3 + 0xb8) + 0x10);
                  if (*(int *)(*(long *)PTR_system_surface_GameBanner_TypeInfo_01fbf4d8 + 0xe0) == 0
                     ) {
                    thunk_FUN_00df405c();
                  }
                  uVar6 = system_surface_GameBanner__GetInstance(0);
                  *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x18) = uVar6;
                  if (lVar7 != 0) {
                    Method_java_util_Vector_object__Add(lVar7,uVar6,*(undefined8 *)puVar2);
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
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_SurfaceManager__AdjustSurfaceLayout
// Address: 00f7335c
// ==========================================================================================

void surface_SurfaceManager__AdjustSurfaceLayout(long param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  bool bVar5;
  undefined *puVar6;
  undefined *puVar7;
  byte bVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  long lVar16;
  long lVar17;
  long lVar18;
  long lVar19;
  ulong uVar20;
  long lVar21;
  uint uVar22;
  long lVar23;
  int iVar24;
  int iVar25;
  float fVar26;
  undefined4 uVar27;
  float fVar28;
  float fVar29;
  float fVar30;
  float fVar31;
  float fVar32;
  
  puVar6 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7db & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0);
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_java_lang_JThread_TypeInfo_01fbf2e0);
    FUN_00db0bbc(PTR_surface_SurfaceManager_TypeInfo_01fc08d8);
    DAT_020ff7db = 1;
  }
  puVar7 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if (*(int *)(*(long *)puVar6 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar16 = main_AppData__GetInstance();
  if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar7);
  }
  lVar17 = kairo_unity_ui_Canvas__GetInstance(0);
  lVar18 = surface_TouchEffectManager__GetInstance();
  lVar19 = form_FormManager__GetInstance();
  if (lVar19 == 0) goto LAB_00f73c94;
  iVar9 = kairo_unity_form_FormManagerBase__GetFormsNum(lVar19,0);
  puVar6 = PTR_surface_SurfaceManager_TypeInfo_01fc08d8;
  if (iVar9 == 0) {
    return;
  }
  kairo_unity_form_FormManagerBase__GetForm(lVar19,0,0);
  lVar19 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10);
  if (lVar19 == 0) goto LAB_00f73c94;
  iVar9 = *(int *)(lVar19 + 0xc0);
  surface_SurfaceManager__UpdateAdMobView();
  if (lVar17 == 0) goto LAB_00f73c94;
  uVar20 = kairo_unity_ui_Canvas__IsGetStatusBarHeight(lVar17,0);
  if ((uVar20 & 1) == 0) {
    kairo_unity_ui_Canvas__GetStatusBarHeight(lVar17,0);
  }
  puVar7 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  uVar20 = kairo_unity_ui_Canvas__IsGetStatusBarPosition(lVar17,0);
  if ((uVar20 & 1) == 0) {
    kairo_unity_ui_Canvas__GetStatusBarPosition(lVar17,0);
  }
  if (*(int *)(*(long *)puVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  lVar19 = *(long *)puVar7;
  if (*(int *)(lVar19 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar19 = *(long *)puVar7;
  }
  lVar19 = **(long **)(lVar19 + 0xb8);
  if (lVar19 == 0) goto LAB_00f73c94;
  iVar10 = kairo_unity_ui_IApplication__GetWidth(lVar19,0);
  iVar11 = kairo_unity_ui_IApplication__GetHeight(lVar19,0);
  iVar12 = kairo_unity_ui_Canvas__GetWidth2(lVar17,0);
  iVar13 = kairo_unity_ui_Canvas__GetHeight2(lVar17,0);
  iVar24 = iVar10;
  iVar14 = iVar12;
  if (*(char *)(param_1 + 0x38) == '\0') {
    uVar20 = kairo_unity_ui_IApplication__IsSide(lVar19,0);
    bVar5 = iVar10 < iVar11;
    if ((uVar20 & 1) == 0) {
      bVar5 = iVar11 < iVar10;
    }
    if (bVar5) goto LAB_00f735fc;
    if (*(char *)(param_1 + 0x38) != '\0') goto LAB_00f73574;
  }
  else {
LAB_00f73574:
    uVar20 = kairo_unity_ui_IApplication__IsSide(lVar19,0);
    bVar5 = iVar11 < iVar10;
    if ((uVar20 & 1) == 0) {
      bVar5 = iVar10 < iVar11;
    }
    if (bVar5) {
LAB_00f735fc:
      iVar24 = iVar11;
      iVar14 = iVar13;
      iVar11 = iVar10;
      iVar13 = iVar12;
    }
  }
  puVar7 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar21 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar21 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar21 = *(long *)puVar7;
  }
  lVar23 = *(long *)(lVar21 + 0xb8);
  if ((iVar24 < iVar11) || (*(int *)(lVar23 + 0x40) == 4)) {
    if (*(int *)(lVar21 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar23 = *(long *)(*(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338 + 0xb8);
    }
    if (*(char *)(lVar23 + 0xba) != '\0') {
      if (*(int *)(*(long *)PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      iVar10 = kairo_unity_ad_AdMobView__GetAdHeight(0);
      iVar11 = iVar11 - iVar10;
      iVar10 = kairo_unity_ad_AdMobView__GetAdHeight(0);
      iVar13 = iVar13 - iVar10;
    }
  }
  fVar26 = (float)kairo_unity_ui_IApplication__GetScaleRatio(lVar19,1,0);
  lVar21 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
  uVar27 = kairo_unity_ui_IApplication__GetScaleRatio(lVar19,0,0);
  if (lVar21 == 0) goto LAB_00f73c94;
  *(undefined4 *)(lVar21 + 0xc4) = uVar27;
  lVar23 = *(long *)(*(long *)puVar6 + 0xb8);
  lVar21 = *(long *)(lVar23 + 0x10);
  if (lVar21 == 0) goto LAB_00f73c94;
  fVar32 = (((fVar26 * 240.0) / 100.0) * 100.0) / 320.0;
  *(float *)(lVar21 + 0xc4) = fVar32;
  fVar26 = DAT_005bcfd0;
  lVar23 = *(long *)(lVar23 + 8);
  if (lVar23 == 0) goto LAB_00f73c94;
  iVar2 = *(int *)(lVar23 + 0xc0);
  iVar12 = *(int *)(lVar21 + 0xbc);
  iVar1 = *(int *)(lVar21 + 0xc0);
  iVar3 = *(int *)(lVar23 + 0xbc);
  fVar31 = *(float *)(lVar23 + 0xc4);
  fVar28 = (fVar31 * 240.0) / 100.0 + DAT_005bcfd0;
  iVar10 = -0x80000000;
  if (fVar28 != INFINITY) {
    iVar10 = (int)fVar28;
  }
  kairo_unity_surface_SurfaceBase__SetSize(lVar23,iVar10,iVar10,0);
  puVar7 = PTR_surface_GamePad_TypeInfo_01fc0860;
  lVar21 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
  if ((lVar21 == 0) || (lVar23 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10), lVar23 == 0))
  goto LAB_00f73c94;
  kairo_unity_surface_SurfaceBase__SetSize(lVar23,*(undefined4 *)(lVar21 + 0xbc),iVar13,0);
  lVar21 = *(long *)puVar7;
  if (*(int *)(lVar21 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar21 = *(long *)puVar7;
  }
  lVar21 = *(long *)(lVar21 + 0xb8);
  fVar28 = (fVar32 * (float)*(int *)(lVar21 + 0x30)) / 100.0 + fVar26;
  fVar29 = (fVar32 * (float)*(int *)(lVar21 + 0x34)) / 100.0 + fVar26;
  iVar10 = 0;
  if (iVar13 != 0) {
    iVar10 = (iVar14 * 100) / iVar13;
  }
  fVar30 = (fVar32 * (float)*(int *)(lVar21 + 0x38)) / 100.0 + fVar26;
  iVar13 = -0x80000000;
  if (fVar28 != INFINITY) {
    iVar13 = (int)fVar28;
  }
  fVar32 = (fVar32 * 65.0) / 100.0 + fVar26;
  iVar14 = -0x80000000;
  if (fVar29 != INFINITY) {
    iVar14 = (int)fVar29;
  }
  iVar25 = -0x80000000;
  if (fVar30 != INFINITY) {
    iVar25 = (int)fVar30;
  }
  iVar15 = -0x80000000;
  if (fVar32 != INFINITY) {
    iVar15 = (int)fVar32;
  }
  iVar14 = kairo_unity_graph_Graph__Easing(iVar14,iVar15,10,iVar10 + -0x37,0,0);
  lVar21 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
  if ((lVar21 == 0) || (lVar23 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10), lVar23 == 0))
  goto LAB_00f73c94;
  iVar10 = iVar11 - *(int *)(lVar21 + 0xc0);
  if (iVar10 < iVar25) {
    iVar25 = 2;
  }
  else {
    if (iVar13 <= iVar10) {
      if (lVar16 == 0) goto LAB_00f73c94;
      if ((*(long *)(lVar16 + 0x48) != 0) &&
         (lVar16 = *(long *)(*(long *)(lVar16 + 0x48) + 0x20), lVar16 != 0)) {
        if (*(uint *)(lVar16 + 0x18) < 0xe) goto LAB_00f73c98;
        iVar25 = *(int *)(lVar16 + 0x54);
        goto LAB_00f738d0;
      }
    }
    iVar25 = 1;
  }
LAB_00f738d0:
  if (iVar25 != *(int *)(lVar23 + 0x178)) {
    *(int *)(lVar23 + 0x178) = iVar25;
  }
  if (iVar25 != 0) {
    if (iVar25 == 1) {
      iVar15 = kairo_unity_ui_Canvas__GetStatusBarHeight(lVar17,0);
      iVar13 = iVar10 - iVar15;
      if (iVar14 <= iVar10 - iVar15) {
        iVar13 = iVar14;
      }
      lVar23 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10);
      if (lVar23 == 0) goto LAB_00f73c94;
    }
    else {
      iVar13 = 0;
    }
  }
  *(int *)(lVar23 + 0xc0) = iVar13;
  bVar5 = iVar11 < iVar24 || iVar25 == 2;
  bVar8 = kairo_unity_ui_Canvas__IsFullscreen(lVar17,0);
  if ((bVar5 != (bool)(bVar8 & 1)) &&
     (kairo_unity_ui_Canvas__Fullscreen(lVar17,bVar5,0), iVar9 == 0)) {
    if (*(int *)(*(long *)PTR_java_lang_JThread_TypeInfo_01fbf2e0 + 0xe0) == 0) {
                    /* try { // try from 00f73978 to 00f73987 has its CatchHandler @ 00f73c9c */
      thunk_FUN_00df405c();
    }
    java_lang_JThread__Sleep(100,0);
  }
  iVar9 = kairo_unity_ui_Canvas__GetWidth2(lVar17,0);
  iVar14 = kairo_unity_ui_Canvas__GetHeight2(lVar17,0);
  puVar7 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar16 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar16 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar16);
    lVar16 = *(long *)puVar7;
  }
  lVar17 = *(long *)(lVar16 + 0xb8);
  if ((iVar24 < iVar11) || (*(int *)(lVar17 + 0x40) == 4)) {
    if (*(int *)(lVar16 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar16);
      lVar17 = *(long *)(*(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338 + 0xb8);
    }
    if (*(char *)(lVar17 + 0xba) != '\0') {
      if (*(int *)(*(long *)PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      iVar11 = kairo_unity_ad_AdMobView__GetAdHeight(0);
      iVar14 = iVar14 - iVar11;
    }
  }
  if (iVar25 == 2) {
    lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
    if (lVar16 == 0) goto LAB_00f73c94;
    kairo_unity_surface_SurfaceBase__SetSize(lVar16,iVar9,iVar14,0);
    lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
    if (lVar16 == 0) goto LAB_00f73c94;
    iVar11 = 0;
    iVar13 = 0;
  }
  else {
    uVar22 = (uint)*(byte *)(param_1 + 0x39);
    if (*(byte *)(param_1 + 0x39) != 0) {
      lVar16 = kairo_unity_ui_IApplication__GetViewport(lVar19,0);
      if (lVar16 == 0) goto LAB_00f73c94;
      if (*(uint *)(lVar16 + 0x18) < 2) {
LAB_00f73c98:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      fVar26 = (fVar31 * (float)*(int *)(lVar16 + 0x24)) / 100.0 + fVar26;
      uVar22 = 0x80000000;
      if (fVar26 != INFINITY) {
        uVar22 = (int)fVar26;
      }
    }
    lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 8);
    if (lVar16 == 0) goto LAB_00f73c94;
    uVar4 = iVar14 - iVar13;
    iVar11 = iVar9 - *(int *)(lVar16 + 0xbc);
    if (((int)uVar4 <= (int)uVar22 || uVar22 == 0) || (int)uVar22 < (int)uVar4 && (int)uVar22 < 0) {
      uVar22 = uVar4;
    }
    if (iVar11 < 0) {
      iVar11 = iVar11 + 1;
    }
    iVar11 = iVar11 >> 1;
    iVar13 = uVar4 - uVar22;
    *(uint *)(lVar16 + 0xc0) = uVar22;
  }
  kairo_unity_surface_SurfaceBase__SetLocation(lVar16,iVar11,iVar13,0);
  lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10);
  if (lVar16 != 0) {
    kairo_unity_surface_SurfaceBase__SetSize(lVar16,iVar9,iVar14,0);
    lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x10);
    if (lVar16 != 0) {
      iVar9 = iVar9 - *(int *)(lVar16 + 0xbc);
      if (iVar9 < 0) {
        iVar9 = iVar9 + 1;
      }
      kairo_unity_surface_SurfaceBase__SetLocation(lVar16,iVar9 >> 1,0,0);
      lVar17 = *(long *)(*(long *)puVar6 + 0xb8);
      lVar16 = *(long *)(lVar17 + 8);
      if (lVar16 != 0) {
        if (*(int *)(lVar16 + 0xb8) < 0) {
          kairo_unity_surface_SurfaceBase__SetLocation(lVar16,*(undefined4 *)(lVar16 + 0xb4),0,0);
          lVar17 = *(long *)(*(long *)puVar6 + 0xb8);
        }
        lVar16 = *(long *)(lVar17 + 0x10);
        if (lVar16 != 0) {
          if ((iVar12 != *(int *)(lVar16 + 0xbc)) || (iVar1 != *(int *)(lVar16 + 0xc0))) {
            if (lVar18 == 0) goto LAB_00f73c94;
            surface_TouchEffectManager__RemoveSurface(lVar18);
            lVar17 = *(long *)(*(long *)puVar6 + 0xb8);
          }
          lVar16 = *(long *)(lVar17 + 8);
          if (lVar16 != 0) {
            if ((iVar3 != *(int *)(lVar16 + 0xbc)) || (iVar2 != *(int *)(lVar16 + 0xc0))) {
              if (lVar18 == 0) goto LAB_00f73c94;
              surface_TouchEffectManager__RemoveSurface(lVar18);
              lVar17 = *(long *)(*(long *)puVar6 + 0xb8);
            }
            if (*(long *)(lVar17 + 0x18) != 0) {
              kairo_unity_surface_SurfaceBase__SetLocation(*(long *)(lVar17 + 0x18),0,iVar14,0);
              lVar16 = *(long *)(*(long *)(*(long *)puVar6 + 0xb8) + 0x18);
              if (*(int *)(*(long *)PTR_kairo_unity_ad_AdMobView_TypeInfo_01fc08e0 + 0xe0) == 0) {
                thunk_FUN_00df405c();
              }
              uVar27 = kairo_unity_ad_AdMobView__GetAdHeight(0);
              if (lVar16 != 0) {
                kairo_unity_surface_SurfaceBase__SetSize(lVar16,iVar24,uVar27,0);
                return;
              }
            }
          }
        }
      }
    }
  }
LAB_00f73c94:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__GetInstance
// Address: 00f73dc4
// ==========================================================================================

long surface_TouchEffectManager__GetInstance(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  long lVar3;
  
  puVar1 = PTR_surface_TouchEffectManager_TypeInfo_01fc3250;
  if ((DAT_020ff7e1 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_TouchEffectManager_TypeInfo_01fc3250);
    DAT_020ff7e1 = 1;
  }
  lVar3 = **(long **)(*(long *)puVar1 + 0xb8);
  if (lVar3 == 0) {
    uVar2 = thunk_FUN_00e11c14();
    surface_TouchEffectManager___ctor();
    **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
    lVar3 = **(long **)(*(long *)puVar1 + 0xb8);
  }
  return lVar3;
}



// ==========================================================================================
// Function: surface_SurfaceManager__UpdateAdMobView
// Address: 00f73ec0
// ==========================================================================================

void surface_SurfaceManager__UpdateAdMobView(void)

{
  undefined *puVar1;
  undefined *puVar2;
  bool bVar3;
  long lVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  long *plVar8;
  
  puVar1 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if ((DAT_020ff7de & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_surface_GamePad_TypeInfo_01fc0860);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff7de = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_ui_Canvas__GetInstance(0);
  lVar5 = system_KairoService__GetInstance(0);
  lVar6 = system_billing_MyBilling__GetInstance(0);
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (lVar5 == 0) goto LAB_00f740a0;
  if (*(char *)(lVar5 + 0x58) != '\0') {
    lVar5 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    if (*(char *)(*(long *)(lVar5 + 0xb8) + 0x30) == '\0') {
      if ((lVar6 == 0) || (lVar5 = system_billing_ui_BillingManager__GetItem(lVar6,0,0), lVar5 == 0)
         ) goto LAB_00f740a0;
      uVar7 = system_billing_ui_BillingItem__CheckProvision(lVar5,0,0);
      puVar2 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
      if ((uVar7 & 1) == 0) {
        if (*(int *)(*(long *)PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        if (DAT_020ff602 == '\0') {
          FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
          DAT_020ff602 = '\x01';
        }
        lVar5 = *(long *)puVar2;
        if (*(int *)(lVar5 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar5 = *(long *)puVar2;
        }
        plVar8 = **(long ***)(lVar5 + 0xb8);
        if ((plVar8 == (long *)0x0) ||
           (lVar5 = (**(code **)(*plVar8 + 0x228))(plVar8,*(undefined8 *)(*plVar8 + 0x230)),
           lVar5 == 0)) goto LAB_00f740a0;
        bVar3 = *(char *)(lVar5 + 0x5c) == '\0';
      }
      else {
        bVar3 = false;
      }
    }
    else {
      bVar3 = false;
    }
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    *(bool *)(*(long *)(lVar5 + 0xb8) + 0xba) = bVar3;
  }
  puVar1 = PTR_surface_GamePad_TypeInfo_01fc0860;
  if (lVar4 != 0) {
    kairo_unity_ui_Canvas__UpdateAdMobView(lVar4,0);
    lVar4 = *(long *)puVar1;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar1;
    }
    *(undefined4 *)(*(long *)(lVar4 + 0xb8) + 0x34) = 0x5a;
    return;
  }
LAB_00f740a0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveSurface
// Address: 00f740a4
// ==========================================================================================

void surface_TouchEffectManager__RemoveSurface(long param_1,long param_2)

{
  undefined *puVar1;
  long lVar2;
  int iVar3;
  
  if ((DAT_020ff7e8 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7e8 = 1;
  }
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar3 = *(int *)(lVar2 + 0x14) + -1;
    if (iVar3 < 0) {
      return;
    }
    do {
      lVar2 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar2,iVar3,*(undefined8 *)puVar1);
      if (lVar2 == 0) break;
      if (*(long *)(lVar2 + 0x10) == param_2) {
        surface_TouchEffectManager__RemoveEffect(param_1,iVar3);
      }
      iVar3 = iVar3 + -1;
      if (iVar3 < 0) {
        return;
      }
      lVar2 = *(long *)(param_1 + 0x10);
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_SurfaceManager__Draw
// Address: 00f7414c
// ==========================================================================================

void surface_SurfaceManager__Draw(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if ((DAT_020ff7dc & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    DAT_020ff7dc = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_ui_Canvas__GetInstance(0);
  lVar2 = surface_TouchEffectManager__GetInstance();
  kairo_unity_surface_SurfaceManagerBase__Draw(param_1,param_2,0);
  if (lVar2 != 0) {
    surface_TouchEffectManager__Draw(lVar2,param_2);
    surface_TouchEffectManager__Frame(lVar2);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__Draw
// Address: 00f741e0
// ==========================================================================================

void surface_TouchEffectManager__Draw(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  long lVar2;
  int iVar3;
  
  if ((DAT_020ff7e4 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7e4 = 1;
  }
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar3 = 0;
    do {
      if (*(int *)(lVar2 + 0x14) <= iVar3) {
        return;
      }
                    /* try { // try from 00f74264 to 00f7426b has its CatchHandler @ 00f74290 */
      lVar2 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar2,iVar3,*(undefined8 *)puVar1);
      if (lVar2 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
                    /* try { // try from 00f74270 to 00f7428b has its CatchHandler @ 00f74294 */
      surface_TouchEffect__Draw(lVar2,param_2);
      lVar2 = *(long *)(param_1 + 0x10);
      iVar3 = iVar3 + 1;
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__Frame
// Address: 00f7436c
// ==========================================================================================

void surface_TouchEffectManager__Frame(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  ulong uVar4;
  int iVar5;
  
  if ((DAT_020ff7e3 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElementAt_01fc3268);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7e3 = 1;
  }
  puVar2 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElementAt_01fc3268;
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar3 = *(long *)(param_1 + 0x10);
  if (lVar3 != 0) {
    iVar5 = *(int *)(lVar3 + 0x14) + -1;
    if (iVar5 < 0) {
      return;
    }
    do {
      lVar3 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar3,iVar5,*(undefined8 *)puVar1);
      if (lVar3 == 0) break;
      uVar4 = surface_TouchEffect__Frame();
      if ((uVar4 & 1) != 0) {
        if (*(long *)(param_1 + 0x10) == 0) break;
        kairo_unity_util_FastVector_object___RemoveElementAt
                  (*(long *)(param_1 + 0x10),iVar5,*(undefined8 *)puVar2);
      }
      iVar5 = iVar5 + -1;
      if (iVar5 < 0) {
        return;
      }
      lVar3 = *(long *)(param_1 + 0x10);
    } while (lVar3 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_SurfaceManager__DrawComponents
// Address: 00f74428
// ==========================================================================================

void surface_SurfaceManager__DrawComponents(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_surface_SurfaceManager_TypeInfo_01fc08d8;
  if ((DAT_020ff7dd & 1) == 0) {
    FUN_00db0bbc(PTR_surface_SurfaceManager_TypeInfo_01fc08d8);
    DAT_020ff7dd = 1;
  }
  lVar2 = *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x10);
  if (lVar2 == 0) {
LAB_00f744c0:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(char *)(lVar2 + 0x148) == '\0') {
    return;
  }
  if (*(char *)(lVar2 + 0x48) == '\0') {
    lVar2 = *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 8);
    if (lVar2 == 0) goto LAB_00f744c0;
    if (*(char *)(lVar2 + 0x48) == '\0') {
      return;
    }
  }
  kairo_unity_surface_SurfaceManagerBase__DrawComponents(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: surface_SurfaceManager__SetLayoutMode
// Address: 00f744c4
// ==========================================================================================

void surface_SurfaceManager__SetLayoutMode(long param_1,byte param_2)

{
  *(byte *)(param_1 + 0x39) = param_2 & 1;
  return;
}



// ==========================================================================================
// Function: surface_SurfaceManager__IsLayoutMode
// Address: 00f744d0
// ==========================================================================================

undefined surface_SurfaceManager__IsLayoutMode(long param_1)

{
  return *(undefined *)(param_1 + 0x39);
}



// ==========================================================================================
// Function: surface_TouchEffect__Init
// Address: 00f744d8
// ==========================================================================================

void surface_TouchEffect__Init(void)

{
  surface_TouchEffect__Init();
  return;
}



// ==========================================================================================
// Function: surface_TouchEffect__Init
// Address: 00f744e0
// ==========================================================================================

void surface_TouchEffect__Init
               (undefined4 param_1,undefined4 param_2,long param_3,undefined8 param_4,
               undefined4 param_5,long param_6,undefined8 param_7)

{
  undefined8 uVar1;
  
  *(undefined8 *)(param_3 + 0x10) = param_4;
  *(undefined4 *)(param_3 + 0x40) = param_5;
  *(undefined4 *)(param_3 + 0x18) = param_1;
  *(undefined4 *)(param_3 + 0x1c) = param_2;
  uVar1 = java_lang_JSystem__CurrentTimeMillis(0);
  *(undefined8 *)(param_3 + 0x48) = param_7;
  *(undefined8 *)(param_3 + 0x50) = uVar1;
  *(undefined8 *)(param_3 + 0x30) = uVar1;
  *(undefined8 *)(param_3 + 0x38) = 0;
  if (param_6 != 0) {
    uVar1 = kairo_unity_surface_TouchComponent__GetKey(param_6,0);
    *(undefined8 *)(param_3 + 0x38) = uVar1;
  }
  *(undefined8 *)(param_3 + 0x20) = 0;
  *(undefined8 *)(param_3 + 0x28) = 0;
  return;
}



// ==========================================================================================
// Function: surface_TouchEffect__Frame
// Address: 00f74534
// ==========================================================================================

bool surface_TouchEffect__Frame(long param_1)

{
  undefined auVar1 [16];
  double dVar2;
  double dVar3;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  double dVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  
  iVar4 = java_lang_JSystem__CurrentTimeMillis(0);
  iVar4 = iVar4 - *(int *)(param_1 + 0x30);
  if (iVar4 < 400) {
    fVar11 = *(float *)(param_1 + 0x20);
    fVar10 = *(float *)(param_1 + 0x24);
    lVar5 = java_lang_JSystem__CurrentTimeMillis(0);
    dVar7 = (double)(lVar5 - *(long *)(param_1 + 0x50)) / DAT_005bc7f0;
    fVar8 = (float)*(undefined8 *)(param_1 + 0x20);
    fVar9 = (float)((ulong)*(undefined8 *)(param_1 + 0x20) >> 0x20);
    dVar2 = (double)fVar8 * dVar7;
    dVar3 = (double)fVar9 * dVar7;
    auVar1._8_4_ = SUB84(dVar3,0);
    auVar1._0_8_ = dVar2;
    auVar1._12_4_ = (int)((ulong)dVar3 >> 0x20);
    fVar8 = fVar8 + (float)((double)(float)*(undefined8 *)(param_1 + 0x28) * dVar7);
    fVar9 = fVar9 + (float)((double)(float)((ulong)*(undefined8 *)(param_1 + 0x28) >> 0x20) * dVar7)
    ;
    *(ulong *)(param_1 + 0x20) = CONCAT44(fVar9,fVar8);
    *(ulong *)(param_1 + 0x18) =
         CONCAT44((float)((ulong)*(undefined8 *)(param_1 + 0x18) >> 0x20) + (float)auVar1._8_8_,
                  (float)*(undefined8 *)(param_1 + 0x18) + (float)dVar2);
    if (((0.0 <= fVar11) && (fVar8 < 0.0)) || ((fVar11 < 0.0 && (0.0 <= fVar8)))) {
      *(undefined4 *)(param_1 + 0x20) = 0;
    }
    if (((0.0 <= fVar10) && (fVar9 < 0.0)) || ((fVar10 < 0.0 && (0.0 <= fVar9)))) {
      *(undefined4 *)(param_1 + 0x20) = 0;
    }
    uVar6 = java_lang_JSystem__CurrentTimeMillis(0);
    *(undefined8 *)(param_1 + 0x50) = uVar6;
  }
  return 399 < iVar4;
}



// ==========================================================================================
// Function: surface_TouchEffect__Draw
// Address: 00f74624
// ==========================================================================================

void surface_TouchEffect__Draw(long param_1,long param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  byte bVar5;
  int iVar6;
  long lVar7;
  long lVar8;
  long *plVar9;
  undefined8 uVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  int iVar19;
  int iVar20;
  float fVar21;
  
  if ((DAT_020ff7df & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Image_TypeInfo_01fbf500);
    FUN_00db0bbc(PTR_object___TypeInfo_01fc08c0);
    FUN_00db0bbc(PTR_float___TypeInfo_01fc0858);
    DAT_020ff7df = 1;
  }
  if (*(long *)(param_1 + 0x10) != 0) {
    fVar14 = *(float *)(*(long *)(param_1 + 0x10) + 0xc4);
    iVar6 = java_lang_JSystem__CurrentTimeMillis(0);
    if (*(int *)(param_1 + 0x40) != 0) {
      return;
    }
    lVar8 = *(long *)(param_1 + 0x48);
    if (lVar8 != 0) {
      iVar3 = *(int *)(param_1 + 0x30);
      uVar10 = *(undefined8 *)PTR_object___TypeInfo_01fc08c0;
      lVar7 = thunk_FUN_00e11b18(lVar8,uVar10);
      if (lVar7 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(lVar8,uVar10);
      }
      if (*(uint *)(lVar7 + 0x18) != 0) {
        plVar9 = *(long **)(lVar7 + 0x20);
        if (plVar9 != (long *)0x0) {
          bVar5 = *(byte *)(*(long *)PTR_kairo_unity_ui_Image_TypeInfo_01fbf500 + 0x130);
          if ((*(byte *)(*plVar9 + 0x130) < bVar5) ||
             (*(long *)(*(long *)(*plVar9 + 200) + (ulong)bVar5 * 8 + -8) !=
              *(long *)PTR_kairo_unity_ui_Image_TypeInfo_01fbf500)) {
                    /* WARNING: Subroutine does not return */
            FUN_00db1180(plVar9);
          }
        }
        if (1 < *(uint *)(lVar7 + 0x18)) {
          lVar8 = *(long *)(lVar7 + 0x28);
          if (lVar8 == 0) {
            lVar7 = 0;
          }
          else {
            uVar10 = *(undefined8 *)PTR_float___TypeInfo_01fc0858;
            lVar7 = thunk_FUN_00e11b18(lVar8,uVar10);
            if (lVar7 == 0) {
                    /* WARNING: Subroutine does not return */
              FUN_00db1180(lVar8,uVar10);
            }
          }
          iVar3 = (iVar6 - iVar3) / 0x32;
          iVar6 = iVar3 * -0x12;
          if (iVar6 + 0x9f < 0 != SCARRY4(iVar6,0x9f)) {
            return;
          }
          lVar8 = *(long *)(param_1 + 0x10);
          if ((lVar8 == 0) || (lVar7 == 0)) goto LAB_00f7490c;
          if ((*(int *)(lVar7 + 0x18) != 0) && (*(int *)(lVar7 + 0x18) != 1)) {
            if (param_2 == 0) goto LAB_00f7490c;
            fVar15 = *(float *)(param_1 + 0x18);
            fVar16 = *(float *)(param_1 + 0x1c);
            iVar20 = *(int *)(lVar8 + 0xb4);
            iVar19 = *(int *)(lVar8 + 0xb8);
            fVar17 = *(float *)(lVar7 + 0x20);
            fVar18 = *(float *)(lVar7 + 0x24);
            kairo_unity_ui_Graphics__SetRenderMode(param_2,1,iVar6 + 0xa0,iVar3 * 0x12 + 0x5f,0);
            uVar4 = *(uint *)(lVar7 + 0x18);
            if ((((2 < uVar4) && (uVar4 != 3)) && (4 < uVar4)) && (uVar4 != 5)) {
              fVar14 = fVar14 / 100.0;
              fVar11 = fVar14 * (float)iVar3 * 2.5;
              fVar12 = *(float *)(lVar7 + 0x28) + 0.5;
              fVar21 = *(float *)(lVar7 + 0x2c) + 0.5;
              fVar13 = *(float *)(lVar7 + 0x30) + 0.5;
              iVar6 = -0x80000000;
              if (fVar12 != INFINITY) {
                iVar6 = (int)fVar12;
              }
              fVar12 = *(float *)(lVar7 + 0x34) + 0.5;
              iVar3 = -0x80000000;
              if (fVar21 != INFINITY) {
                iVar3 = (int)fVar21;
              }
              iVar1 = -0x80000000;
              if (fVar13 != INFINITY) {
                iVar1 = (int)fVar13;
              }
              iVar2 = -0x80000000;
              if (fVar12 != INFINITY) {
                iVar2 = (int)fVar12;
              }
              kairo_unity_ui_Graphics__DrawScaledImage
                        ((fVar14 * fVar15 + (float)iVar20) - fVar11 * 0.5,
                         (fVar14 * fVar16 + (float)iVar19) - fVar11 * 0.5,fVar11 + fVar14 * fVar17,
                         fVar11 + fVar14 * fVar18,param_2,plVar9,iVar6,iVar3,iVar1,iVar2,0);
              kairo_unity_ui_Graphics__SetRenderMode(param_2,0,0xff,0,0);
              return;
            }
          }
        }
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
LAB_00f7490c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffect___ctor
// Address: 00f74928
// ==========================================================================================

void surface_TouchEffect___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: surface_TouchEffectManager___ctor
// Address: 00f74930
// ==========================================================================================

void surface_TouchEffectManager___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_Method_kairo_unity_util_FastVector_TouchEffect___ctor_01fc3278;
  puVar1 = PTR_kairo_unity_util_FastVector_TouchEffect__TypeInfo_01fc3270;
  if ((DAT_020ff7e0 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect___ctor_01fc3278);
    FUN_00db0bbc(PTR_kairo_unity_util_FastVector_TouchEffect__TypeInfo_01fc3270);
    DAT_020ff7e0 = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Method_kairo_unity_util_FastVector_object___ctor(uVar3,*(undefined8 *)puVar2);
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Method_kairo_unity_util_FastVector_object___ctor(uVar3,*(undefined8 *)puVar2);
  *(undefined8 *)(param_1 + 0x18) = uVar3;
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: surface_TouchEffectManager__Add
// Address: 00f749c4
// ==========================================================================================

void surface_TouchEffectManager__Add(long param_1,undefined8 param_2)

{
  if ((DAT_020ff7e2 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Add_01fc3280);
    DAT_020ff7e2 = 1;
  }
  if (*(long *)(param_1 + 0x10) != 0) {
    Method_kairo_unity_util_FastVector_object__Add
              (*(long *)(param_1 + 0x10),param_2,
               *(undefined8 *)PTR_Method_kairo_unity_util_FastVector_TouchEffect__Add_01fc3280);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__Clear
// Address: 00f74a1c
// ==========================================================================================

void surface_TouchEffectManager__Clear(long param_1)

{
  long lVar1;
  int iVar2;
  
  if ((DAT_020ff7e5 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveAllElementsKeep_01fc3288)
    ;
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7e5 = 1;
  }
  lVar1 = *(long *)(param_1 + 0x10);
  if (lVar1 != 0) {
    iVar2 = *(int *)(lVar1 + 0x14);
    if (-1 < iVar2 + -1) {
      do {
        iVar2 = iVar2 + -1;
        surface_TouchEffectManager__RemoveEffect(param_1,iVar2);
      } while (0 < iVar2);
      lVar1 = *(long *)(param_1 + 0x10);
      if (lVar1 == 0) goto LAB_00f74aa0;
    }
    kairo_unity_util_FastVector_object___RemoveAllElementsKeep
              (lVar1,*(undefined8 *)
                      PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveAllElementsKeep_01fc3288
              );
    return;
  }
LAB_00f74aa0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveEffect
// Address: 00f74aa4
// ==========================================================================================

void surface_TouchEffectManager__RemoveEffect(long param_1,undefined4 param_2)

{
  if ((DAT_020ff7e7 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElementAt_01fc3268);
    DAT_020ff7e7 = 1;
  }
  if (*(long *)(param_1 + 0x10) != 0) {
    kairo_unity_util_FastVector_object___RemoveElementAt
              (*(long *)(param_1 + 0x10),param_2,
               *(undefined8 *)
                PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElementAt_01fc3268);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveEffect
// Address: 00f74afc
// ==========================================================================================

void surface_TouchEffectManager__RemoveEffect(long param_1,undefined8 param_2)

{
  if ((DAT_020ff7e6 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElement_01fc3290);
    DAT_020ff7e6 = 1;
  }
  if (*(long *)(param_1 + 0x10) != 0) {
    Method_kairo_unity_util_FastVector_object__RemoveElement
              (*(long *)(param_1 + 0x10),param_2,
               *(undefined8 *)
                PTR_Method_kairo_unity_util_FastVector_TouchEffect__RemoveElement_01fc3290);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveId
// Address: 00f74b54
// ==========================================================================================

void surface_TouchEffectManager__RemoveId(long param_1,int param_2)

{
  undefined *puVar1;
  long lVar2;
  int iVar3;
  
  if ((DAT_020ff7e9 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7e9 = 1;
  }
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar3 = *(int *)(lVar2 + 0x14) + -1;
    if (iVar3 < 0) {
      return;
    }
    do {
      lVar2 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar2,iVar3,*(undefined8 *)puVar1);
      if (lVar2 == 0) break;
      if (*(int *)(lVar2 + 0x40) == param_2) {
        surface_TouchEffectManager__RemoveEffect(param_1,iVar3);
      }
      iVar3 = iVar3 + -1;
      if (iVar3 < 0) {
        return;
      }
      lVar2 = *(long *)(param_1 + 0x10);
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveComponentId
// Address: 00f74bfc
// ==========================================================================================

void surface_TouchEffectManager__RemoveComponentId(long param_1,long param_2,int param_3)

{
  undefined *puVar1;
  int iVar2;
  long lVar3;
  int iVar4;
  
  if ((DAT_020ff7ea & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7ea = 1;
  }
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar3 = *(long *)(param_1 + 0x10);
  if (lVar3 != 0) {
    iVar4 = *(int *)(lVar3 + 0x14) + -1;
    if (iVar4 < 0) {
      return;
    }
    do {
      lVar3 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar3,iVar4,*(undefined8 *)puVar1);
      if (lVar3 == 0) break;
      if ((*(long *)(lVar3 + 0x10) == param_2) &&
         (iVar2 = kairo_unity_surface_TouchComponent__GetId(*(undefined8 *)(lVar3 + 0x38),0),
         iVar2 == param_3)) {
        surface_TouchEffectManager__RemoveEffect(param_1,iVar4);
      }
      iVar4 = iVar4 + -1;
      if (iVar4 < 0) {
        return;
      }
      lVar3 = *(long *)(param_1 + 0x10);
    } while (lVar3 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__RemoveComponentKey
// Address: 00f74cbc
// ==========================================================================================

void surface_TouchEffectManager__RemoveComponentKey(long param_1,long param_2,long param_3)

{
  undefined *puVar1;
  long lVar2;
  int iVar3;
  
  if ((DAT_020ff7eb & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    DAT_020ff7eb = 1;
  }
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar3 = *(int *)(lVar2 + 0x14) + -1;
    if (iVar3 < 0) {
      return;
    }
    do {
      lVar2 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar2,iVar3,*(undefined8 *)puVar1);
      if (lVar2 == 0) break;
      if ((*(long *)(lVar2 + 0x10) == param_2) && (*(long *)(lVar2 + 0x38) == param_3)) {
        surface_TouchEffectManager__RemoveEffect(param_1,iVar3);
      }
      iVar3 = iVar3 + -1;
      if (iVar3 < 0) {
        return;
      }
      lVar2 = *(long *)(param_1 + 0x10);
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: surface_TouchEffectManager__AddEffect
// Address: 00f74d74
// ==========================================================================================

void surface_TouchEffectManager__AddEffect(void)

{
  surface_TouchEffectManager__AddEffect();
  return;
}



// ==========================================================================================
// Function: surface_TouchEffectManager__AddEffect
// Address: 00f74d7c
// ==========================================================================================

long surface_TouchEffectManager__AddEffect
               (undefined8 param_1,undefined8 param_2,long param_3,undefined8 param_4,
               undefined4 param_5,undefined8 param_6,undefined8 param_7)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  ulong uVar5;
  long lVar6;
  int iVar7;
  
  if ((DAT_020ff7ec & 1) == 0) {
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Add_01fc3280);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Contains_01fc3298);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258);
    FUN_00db0bbc(PTR_Method_kairo_unity_util_FastVector_TouchEffect__Size_01fc3260);
    FUN_00db0bbc(PTR_surface_TouchEffect_TypeInfo_01fc32a0);
    DAT_020ff7ec = 1;
  }
  puVar3 = PTR_surface_TouchEffect_TypeInfo_01fc32a0;
  puVar2 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__Contains_01fc3298;
  puVar1 = PTR_Method_kairo_unity_util_FastVector_TouchEffect__ElementAt_01fc3258;
  lVar6 = *(long *)(param_3 + 0x18);
  if (lVar6 != 0) {
    iVar7 = 0;
    do {
      if (*(int *)(lVar6 + 0x14) <= iVar7) {
LAB_00f74e7c:
        lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
        System_Object___ctor(lVar4,0);
        if ((lVar6 != 0) &&
           (Method_kairo_unity_util_FastVector_object__Add
                      (lVar6,lVar4,
                       *(undefined8 *)
                        PTR_Method_kairo_unity_util_FastVector_TouchEffect__Add_01fc3280),
           lVar4 != 0)) {
LAB_00f74eb0:
          surface_TouchEffect__Init(param_1,param_2,lVar4,param_4,param_5,param_6,param_7);
          surface_TouchEffectManager__Add(param_3,lVar4);
          return lVar4;
        }
        break;
      }
      lVar4 = Method_kairo_unity_util_FastVector_object__ElementAt
                        (lVar6,iVar7,*(undefined8 *)puVar1);
      if (*(long *)(param_3 + 0x10) == 0) break;
      uVar5 = Method_kairo_unity_util_FastVector_object__Contains
                        (*(long *)(param_3 + 0x10),lVar4,*(undefined8 *)puVar2);
      if ((uVar5 & 1) == 0) {
        if (lVar4 != 0) goto LAB_00f74eb0;
        lVar6 = *(long *)(param_3 + 0x18);
        goto LAB_00f74e7c;
      }
      lVar6 = *(long *)(param_3 + 0x18);
      iVar7 = iVar7 + 1;
    } while (lVar6 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
