// Function: cfg_MyConfig__UpdataDebugFlag
// Address: 00ff4b90
// ==========================================================================================

void cfg_MyConfig__UpdataDebugFlag(void)

{
  undefined *puVar1;
  long lVar2;
  ulong uVar3;
  long lVar4;
  
  puVar1 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  if ((DAT_020ff8f9 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    DAT_020ff8f9 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (*(char *)(*(long *)(lVar2 + 0xb8) + 5) != '\0') {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar2 = kairo_unity_ui_Canvas__GetInstance(0);
    if (lVar2 == 0) {
LAB_00ff4f24:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    kairo_unity_ui_Canvas__DecideKeyState(lVar2,0);
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,1,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(int *)(lVar4 + 0x18) == 0) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x20) = *(byte *)(lVar4 + 0x20) ^ 1;
      if ((uVar3 & 1) == 0) goto LAB_00ff4f24;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,2,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 2) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x21) = *(byte *)(lVar4 + 0x21) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,4,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 3) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x22) = *(byte *)(lVar4 + 0x22) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,8,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 4) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x23) = *(byte *)(lVar4 + 0x23) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x10,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 5) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x24) = *(byte *)(lVar4 + 0x24) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x20,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 6) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x25) = *(byte *)(lVar4 + 0x25) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x40,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 7) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x26) = *(byte *)(lVar4 + 0x26) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x80,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 8) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x27) = *(byte *)(lVar4 + 0x27) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x100,0);
    if ((uVar3 & 1) != 0) {
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x98);
      if (lVar4 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar4 + 0x18) < 9) goto LAB_00ff4f28;
      *(byte *)(lVar4 + 0x28) = *(byte *)(lVar4 + 0x28) ^ 1;
    }
    uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x200,0);
    if ((uVar3 & 1) != 0) {
      lVar2 = *(long *)puVar1;
      if (*(int *)(lVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar2 = *(long *)puVar1;
      }
      lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x98);
      if (lVar2 == 0) goto LAB_00ff4f24;
      if (*(uint *)(lVar2 + 0x18) < 10) {
LAB_00ff4f28:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(byte *)(lVar2 + 0x29) = *(byte *)(lVar2 + 0x29) ^ 1;
    }
  }
  return;
}



// ==========================================================================================
// Function: cfg_MyConfig__IsAndroid
// Address: 00ff9880
// ==========================================================================================

undefined8 cfg_MyConfig__IsAndroid(void)

{
  return 1;
}



// ==========================================================================================
// Function: cfg_MyConfig___ctor
// Address: 00ff9888
// ==========================================================================================

void cfg_MyConfig___ctor(undefined8 param_1)

{
  undefined *puVar1;
  
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_020ff8fa & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    DAT_020ff8fa = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_common_cfg_Config___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: cfg_MyConfig___cctor
// Address: 00ff98e0
// ==========================================================================================

void cfg_MyConfig___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined *puVar9;
  undefined *puVar10;
  undefined4 *puVar11;
  long lVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  
  puVar10 = PTR_StringLiteral_3288_01fc5558;
  puVar9 = PTR_StringLiteral_3281_01fc5550;
  puVar8 = PTR_StringLiteral_7897_01fc5548;
  puVar7 = PTR_StringLiteral_7867_01fc5540;
  puVar6 = PTR_StringLiteral_4224_01fc5538;
  puVar5 = PTR_StringLiteral_4052_01fc5530;
  puVar4 = PTR_StringLiteral_6944_01fc3660;
  puVar3 = PTR_bool___TypeInfo_01fc3418;
  puVar2 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  puVar1 = PTR_StringLiteral_1_01fbf388;
  if ((DAT_020ff8fb & 1) == 0) {
    FUN_00db0bbc(PTR_bool___TypeInfo_01fc3418);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    FUN_00db0bbc(PTR_StringLiteral_4224_01fc5538);
    FUN_00db0bbc(PTR_StringLiteral_7867_01fc5540);
    FUN_00db0bbc(PTR_StringLiteral_3288_01fc5558);
    FUN_00db0bbc(PTR_StringLiteral_7897_01fc5548);
    FUN_00db0bbc(PTR_StringLiteral_3281_01fc5550);
    FUN_00db0bbc(PTR_StringLiteral_6944_01fc3660);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_4052_01fc5530);
    DAT_020ff8fb = 1;
  }
  puVar11 = *(undefined4 **)(*(long *)puVar2 + 0xb8);
  *puVar11 = 2;
  *(undefined *)(puVar11 + 1) = 1;
  *(undefined4 *)((long)puVar11 + 5) = 0;
  *(undefined *)((long)puVar11 + 9) = 0;
  puVar11[3] = 0xffffffff;
  *(undefined2 *)(puVar11 + 4) = 0;
  puVar11[5] = 0;
  *(undefined2 *)(puVar11 + 6) = 0;
  *(undefined *)((long)puVar11 + 0x1a) = 1;
  uVar14 = *(undefined8 *)puVar5;
  uVar13 = *(undefined8 *)puVar1;
  *(undefined2 *)(puVar11 + 0xc) = 0x101;
  *(undefined8 *)(puVar11 + 8) = uVar14;
  *(undefined8 *)(puVar11 + 10) = uVar13;
  uVar13 = *(undefined8 *)puVar6;
  *(undefined *)(puVar11 + 0x10) = 1;
  puVar11[0x11] = 0;
  *(undefined4 *)((long)puVar11 + 0x41) = 0;
  *(undefined *)(puVar11 + 0x12) = 1;
  *(undefined8 *)(puVar11 + 0xe) = uVar13;
  uVar13 = *(undefined8 *)puVar7;
  *(undefined8 *)(puVar11 + 0x14) = uVar13;
  *(undefined8 *)(puVar11 + 0x16) = uVar13;
  uVar13 = *(undefined8 *)puVar8;
  *(undefined *)(puVar11 + 0x1a) = 0;
  puVar11[0x1b] = 8;
  *(undefined8 *)(puVar11 + 0x18) = uVar13;
  uVar13 = *(undefined8 *)puVar9;
  *(undefined8 *)(puVar11 + 0x1c) = *(undefined8 *)puVar4;
  *(undefined8 *)(puVar11 + 0x1e) = uVar13;
  *(undefined8 *)(puVar11 + 0x20) = *(undefined8 *)puVar10;
  uVar13 = FUN_00db0c30(*(undefined8 *)puVar3,10);
  lVar12 = *(long *)(*(long *)puVar2 + 0xb8);
  *(undefined8 *)(lVar12 + 0x98) = uVar13;
  *(undefined *)(lVar12 + 0xa0) = 1;
  *(undefined4 *)(lVar12 + 0xa4) = 0x14;
  *(undefined *)(lVar12 + 0xa8) = 1;
  return;
}



// ==========================================================================================
