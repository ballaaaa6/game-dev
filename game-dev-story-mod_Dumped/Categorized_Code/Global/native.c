// Function: native_AppPlugin___cctor
// Address: 00f74f48
// ==========================================================================================

void native_AppPlugin___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  
  puVar4 = PTR_StringLiteral_8733_01fc32b8;
  puVar3 = PTR_StringLiteral_8732_01fc32b0;
  puVar2 = PTR_UnityEngine_AndroidJavaClass_TypeInfo_01fc32a8;
  puVar1 = PTR_native_AppPlugin_TypeInfo_01fbf828;
  if ((DAT_020ff7ed & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngine_AndroidJavaClass_TypeInfo_01fc32a8);
    FUN_00db0bbc(PTR_native_AppPlugin_TypeInfo_01fbf828);
    FUN_00db0bbc(PTR_StringLiteral_8733_01fc32b8);
    FUN_00db0bbc(PTR_StringLiteral_8732_01fc32b0);
    DAT_020ff7ed = 1;
  }
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  UnityEngine_AndroidJavaClass___ctor(uVar5,*(undefined8 *)puVar3,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar5;
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  UnityEngine_AndroidJavaClass___ctor(uVar5,*(undefined8 *)puVar4,0);
  *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = uVar5;
  return;
}



// ==========================================================================================
// Function: native_AppPlugin__Init
// Address: 00f75010
// ==========================================================================================

void native_AppPlugin__Init(undefined4 param_1,byte param_2,long param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  undefined8 uVar7;
  uint uVar8;
  long lVar9;
  byte local_38 [4];
  undefined4 local_34;
  
  puVar1 = PTR_native_AppPlugin_TypeInfo_01fbf828;
  if ((DAT_020ff7ee & 1) == 0) {
    FUN_00db0bbc(PTR_native_AppPlugin_TypeInfo_01fbf828);
    FUN_00db0bbc(PTR_bool_TypeInfo_01fbf460);
    FUN_00db0bbc(PTR_int_TypeInfo_01fc0108);
    FUN_00db0bbc(PTR_object___TypeInfo_01fc08c0);
    FUN_00db0bbc(PTR_StringLiteral_7959_01fc32c0);
    DAT_020ff7ee = 1;
  }
  puVar3 = PTR_object___TypeInfo_01fc08c0;
  puVar2 = PTR_int_TypeInfo_01fc0108;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar9 = **(long **)(lVar4 + 0xb8);
  plVar5 = (long *)FUN_00db0c30(*(undefined8 *)puVar3,3);
  local_34 = param_1;
  lVar4 = thunk_FUN_00e11868(*(undefined8 *)puVar2,&local_34);
  if (plVar5 == (long *)0x0) {
LAB_00f751a4:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if ((lVar4 != 0) &&
     (lVar6 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar5 + 0x40)), lVar6 == 0)) {
LAB_00f751a8:
    uVar7 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
    FUN_00db0cb0(uVar7,0);
  }
  puVar1 = PTR_bool_TypeInfo_01fbf460;
  if (*(int *)(plVar5 + 3) != 0) {
    plVar5[4] = lVar4;
    local_38[0] = param_2 & 1;
    lVar4 = thunk_FUN_00e11868(*(undefined8 *)puVar1,local_38);
    if ((lVar4 != 0) &&
       (lVar6 = thunk_FUN_00e11b18(lVar4,*(undefined8 *)(*plVar5 + 0x40)), lVar6 == 0))
    goto LAB_00f751a8;
    uVar8 = *(uint *)(plVar5 + 3);
    if (1 < uVar8) {
      plVar5[5] = lVar4;
      if (param_3 != 0) {
        lVar4 = thunk_FUN_00e11b18(param_3,*(undefined8 *)(*plVar5 + 0x40));
        if (lVar4 == 0) goto LAB_00f751a8;
        uVar8 = *(uint *)(plVar5 + 3);
      }
      if (2 < uVar8) {
        plVar5[6] = param_3;
        if (lVar9 != 0) {
          UnityEngine_AndroidJavaObject__CallStatic
                    (lVar9,*(undefined8 *)PTR_StringLiteral_7959_01fc32c0,plVar5,0);
          return;
        }
        goto LAB_00f751a4;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: native_AppPlugin__Finish
// Address: 00f751b4
// ==========================================================================================

void native_AppPlugin__Finish(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_020ff7ef & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_AppPlugin___c__Finish_b__4_0_01fc32c8);
    FUN_00db0bbc(PTR_native_AppPlugin___c_TypeInfo_01fc32d0);
    DAT_020ff7ef = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_AppPlugin___c_TypeInfo_01fc32d0;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 8);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,*(undefined8 *)PTR_Method_native_AppPlugin___c__Finish_b__4_0_01fc32c8,0)
    ;
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 8) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_AppPlugin__ShowPurchaseLog
// Address: 00f752fc
// ==========================================================================================

undefined4
native_AppPlugin__ShowPurchaseLog
          (undefined8 param_1,undefined4 param_2,undefined8 param_3,byte param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  long *plVar7;
  undefined4 *puVar8;
  
  puVar1 = PTR_native_AppPlugin___c__DisplayClass5_0_TypeInfo_01fc32d8;
  if ((DAT_020ff7f0 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_int_TypeInfo_01fc0108);
    FUN_00db0bbc(PTR_Method_native_AppPlugin___c__DisplayClass5_0__ShowPurchaseLog_b__0_01fc32e0);
    FUN_00db0bbc(PTR_native_AppPlugin___c__DisplayClass5_0_TypeInfo_01fc32d8);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    DAT_020ff7f0 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(undefined8 *)(lVar4 + 0x10) = param_1;
    *(undefined4 *)(lVar4 + 0x18) = param_2;
    *(undefined8 *)(lVar4 + 0x20) = param_3;
    *(byte *)(lVar4 + 0x28) = param_4 & 1;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_AppPlugin___c__DisplayClass5_0__ShowPurchaseLog_b__0_01fc32e0;
    puVar2 = PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    kairo_unity_ui_IApplication_UIMethod___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if ((lVar5 != 0) &&
       (plVar7 = (long *)Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0),
       plVar7 != (long *)0x0)) {
      if (*(long *)(*plVar7 + 0x40) == *(long *)(*(long *)PTR_int_TypeInfo_01fc0108 + 0x40)) {
        puVar8 = (undefined4 *)thunk_FUN_00e11d68();
        return *puVar8;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db1180();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_AppPlugin___c__DisplayClass5_0___ctor
// Address: 00f75480
// ==========================================================================================

void native_AppPlugin___c__DisplayClass5_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_AppPlugin__LaunchMailer
// Address: 00f75488
// ==========================================================================================

void native_AppPlugin__LaunchMailer(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_native_AppPlugin___c__DisplayClass6_0_TypeInfo_01fc32e8;
  if ((DAT_020ff7f1 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_AppPlugin___c__DisplayClass6_0__LaunchMailer_b__0_01fc32f0);
    FUN_00db0bbc(PTR_native_AppPlugin___c__DisplayClass6_0_TypeInfo_01fc32e8);
    DAT_020ff7f1 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(undefined8 *)(lVar4 + 0x10) = param_1;
    *(undefined8 *)(lVar4 + 0x18) = param_2;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_AppPlugin___c__DisplayClass6_0__LaunchMailer_b__0_01fc32f0;
    puVar2 = PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    System_Threading_ThreadStart___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if (lVar5 != 0) {
      Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_AppPlugin___c__DisplayClass6_0___ctor
// Address: 00f755ac
// ==========================================================================================

void native_AppPlugin___c__DisplayClass6_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_AppPlugin___c___cctor
// Address: 00f755b4
// ==========================================================================================

void native_AppPlugin___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_native_AppPlugin___c_TypeInfo_01fc32d0;
  if ((DAT_020ff7f2 & 1) == 0) {
    FUN_00db0bbc(PTR_native_AppPlugin___c_TypeInfo_01fc32d0);
    DAT_020ff7f2 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: native_AppPlugin___c___ctor
// Address: 00f75610
// ==========================================================================================

void native_AppPlugin___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPlugin__Create
// Address: 017d320c
// ==========================================================================================

undefined native_WebBoxPlugin__Create(void)

{
  undefined *puVar1;
  long lVar2;
  long *plVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  undefined8 uVar7;
  
  puVar4 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e2 & 1) == 0) {
    FUN_00db0bbc(PTR_bool_TypeInfo_01fbf460);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__Create_b__2_0_01fc7a70);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    DAT_021008e2 = 1;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar1 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar5 = *(long *)puVar4;
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar4;
  }
  lVar2 = *(long *)puVar1;
  lVar5 = **(long **)(lVar5 + 0xb8);
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar6 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
  if (lVar6 == 0) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    uVar7 = **(undefined8 **)(lVar2 + 0xb8);
    lVar6 = thunk_FUN_00e11c14(*(undefined8 *)
                                PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    kairo_unity_ui_IApplication_UIMethod___ctor
              (lVar6,uVar7,*(undefined8 *)PTR_Method_native_WebBoxPlugin___c__Create_b__2_0_01fc7a70
               ,0);
    *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = lVar6;
  }
  if ((lVar5 != 0) &&
     (plVar3 = (long *)Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,lVar6,1,0),
     plVar3 != (long *)0x0)) {
    if (*(long *)(*plVar3 + 0x40) == *(long *)(*(long *)PTR_bool_TypeInfo_01fbf460 + 0x40)) {
      puVar4 = (undefined *)thunk_FUN_00e11d68();
      return *puVar4;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db1180();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__SetViewRect
// Address: 017d3394
// ==========================================================================================

void native_WebBoxPlugin__SetViewRect(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e3 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__SetViewRect_b__3_0_01fc7a80);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008e3 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x10);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPlugin___c__SetViewRect_b__3_0_01fc7a80,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x10) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__LoadUrl
// Address: 017d34dc
// ==========================================================================================

void native_WebBoxPlugin__LoadUrl(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_native_WebBoxPlugin___c__DisplayClass4_0_TypeInfo_01fc7a88;
  if ((DAT_021008e4 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__DisplayClass4_0__LoadUrl_b__0_01fc7a90);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c__DisplayClass4_0_TypeInfo_01fc7a88);
    DAT_021008e4 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(undefined8 *)(lVar4 + 0x10) = param_1;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_WebBoxPlugin___c__DisplayClass4_0__LoadUrl_b__0_01fc7a90;
    puVar2 = PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    System_Threading_ThreadStart___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if (lVar5 != 0) {
      Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin___c__DisplayClass4_0___ctor
// Address: 017d35fc
// ==========================================================================================

void native_WebBoxPlugin___c__DisplayClass4_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPlugin__Dispose
// Address: 017d3604
// ==========================================================================================

void native_WebBoxPlugin__Dispose(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e5 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__Dispose_b__5_0_01fc7a98);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008e5 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x18);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPlugin___c__Dispose_b__5_0_01fc7a98,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x18) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__Visible
// Address: 017d374c
// ==========================================================================================

undefined native_WebBoxPlugin__Visible(void)

{
  undefined *puVar1;
  long lVar2;
  long *plVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  undefined8 uVar7;
  
  puVar4 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e6 & 1) == 0) {
    FUN_00db0bbc(PTR_bool_TypeInfo_01fbf460);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__Visible_b__6_0_01fc7aa0);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    DAT_021008e6 = 1;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar1 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar5 = *(long *)puVar4;
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar4;
  }
  lVar2 = *(long *)puVar1;
  lVar5 = **(long **)(lVar5 + 0xb8);
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar6 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x20);
  if (lVar6 == 0) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    uVar7 = **(undefined8 **)(lVar2 + 0xb8);
    lVar6 = thunk_FUN_00e11c14(*(undefined8 *)
                                PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    kairo_unity_ui_IApplication_UIMethod___ctor
              (lVar6,uVar7,
               *(undefined8 *)PTR_Method_native_WebBoxPlugin___c__Visible_b__6_0_01fc7aa0,0);
    *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x20) = lVar6;
  }
  if ((lVar5 != 0) &&
     (plVar3 = (long *)Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,lVar6,1,0),
     plVar3 != (long *)0x0)) {
    if (*(long *)(*plVar3 + 0x40) == *(long *)(*(long *)PTR_bool_TypeInfo_01fbf460 + 0x40)) {
      puVar4 = (undefined *)thunk_FUN_00e11d68();
      return *puVar4;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db1180();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__SetVisible
// Address: 017d38d4
// ==========================================================================================

void native_WebBoxPlugin__SetVisible(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e7 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__SetVisible_b__7_0_01fc7aa8);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008e7 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x28);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPlugin___c__SetVisible_b__7_0_01fc7aa8,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x28) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__SetJavaScriptEnabled
// Address: 017d3a1c
// ==========================================================================================

void native_WebBoxPlugin__SetJavaScriptEnabled(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e8 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__SetJavaScriptEnabled_b__8_0_01fc7ab0);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008e8 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x30);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)
                PTR_Method_native_WebBoxPlugin___c__SetJavaScriptEnabled_b__8_0_01fc7ab0,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x30) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin__OpenAuthWebView
// Address: 017d3b64
// ==========================================================================================

void native_WebBoxPlugin__OpenAuthWebView(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008e9 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPlugin___c__OpenAuthWebView_b__9_0_01fc7ab8);
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008e9 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x38);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPlugin___c__OpenAuthWebView_b__9_0_01fc7ab8,0)
    ;
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x38) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPlugin___c___cctor
// Address: 017d3cac
// ==========================================================================================

void native_WebBoxPlugin___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78;
  if ((DAT_021008ea & 1) == 0) {
    FUN_00db0bbc(PTR_native_WebBoxPlugin___c_TypeInfo_01fc7a78);
    DAT_021008ea = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: native_WebBoxPlugin___c___ctor
// Address: 017d3d08
// ==========================================================================================

void native_WebBoxPlugin___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___cctor
// Address: 017d4b10
// ==========================================================================================

void native_WebBoxPluginOld___cctor(void)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_021008ef & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngine_AndroidJavaClass_TypeInfo_01fc32a8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld_TypeInfo_01fc7b58);
    FUN_00db0bbc(PTR_StringLiteral_8734_01fc7b60);
    DAT_021008ef = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (*(char *)(*(long *)(lVar2 + 0xb8) + 0x30) == '\0') {
    uVar3 = thunk_FUN_00e11c14(*(undefined8 *)PTR_UnityEngine_AndroidJavaClass_TypeInfo_01fc32a8);
    UnityEngine_AndroidJavaClass___ctor(uVar3,*(undefined8 *)PTR_StringLiteral_8734_01fc7b60,0);
    **(undefined8 **)(*(long *)PTR_native_WebBoxPluginOld_TypeInfo_01fc7b58 + 0xb8) = uVar3;
  }
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__Create
// Address: 017d4bcc
// ==========================================================================================

undefined native_WebBoxPluginOld__Create(void)

{
  undefined *puVar1;
  long lVar2;
  long *plVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  undefined8 uVar7;
  
  puVar4 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008f0 & 1) == 0) {
    FUN_00db0bbc(PTR_bool_TypeInfo_01fbf460);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__Create_b__2_0_01fc7b68);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    DAT_021008f0 = 1;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar1 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  lVar5 = *(long *)puVar4;
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar4;
  }
  lVar2 = *(long *)puVar1;
  lVar5 = **(long **)(lVar5 + 0xb8);
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar6 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
  if (lVar6 == 0) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    uVar7 = **(undefined8 **)(lVar2 + 0xb8);
    lVar6 = thunk_FUN_00e11c14(*(undefined8 *)
                                PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    kairo_unity_ui_IApplication_UIMethod___ctor
              (lVar6,uVar7,
               *(undefined8 *)PTR_Method_native_WebBoxPluginOld___c__Create_b__2_0_01fc7b68,0);
    *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = lVar6;
  }
  if ((lVar5 != 0) &&
     (plVar3 = (long *)Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,lVar6,1,0),
     plVar3 != (long *)0x0)) {
    if (*(long *)(*plVar3 + 0x40) == *(long *)(*(long *)PTR_bool_TypeInfo_01fbf460 + 0x40)) {
      puVar4 = (undefined *)thunk_FUN_00e11d68();
      return *puVar4;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db1180();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__SetViewRect
// Address: 017d4d54
// ==========================================================================================

void native_WebBoxPluginOld__SetViewRect
               (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_native_WebBoxPluginOld___c__DisplayClass3_0_TypeInfo_01fc7b78;
  if ((DAT_021008f1 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__DisplayClass3_0__SetViewRect_b__0_01fc7b80);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c__DisplayClass3_0_TypeInfo_01fc7b78);
    DAT_021008f1 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(undefined4 *)(lVar4 + 0x10) = param_1;
    *(undefined4 *)(lVar4 + 0x14) = param_2;
    *(undefined4 *)(lVar4 + 0x18) = param_3;
    *(undefined4 *)(lVar4 + 0x1c) = param_4;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_WebBoxPluginOld___c__DisplayClass3_0__SetViewRect_b__0_01fc7b80;
    puVar2 = PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    System_Threading_ThreadStart___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if (lVar5 != 0) {
      Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___c__DisplayClass3_0___ctor
// Address: 017d4e8c
// ==========================================================================================

void native_WebBoxPluginOld___c__DisplayClass3_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__LoadUrl
// Address: 017d4e94
// ==========================================================================================

void native_WebBoxPluginOld__LoadUrl(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_native_WebBoxPluginOld___c__DisplayClass4_0_TypeInfo_01fc7b88;
  if ((DAT_021008f2 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__DisplayClass4_0__LoadUrl_b__0_01fc7b90);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c__DisplayClass4_0_TypeInfo_01fc7b88);
    DAT_021008f2 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(undefined8 *)(lVar4 + 0x10) = param_1;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_WebBoxPluginOld___c__DisplayClass4_0__LoadUrl_b__0_01fc7b90;
    puVar2 = PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    System_Threading_ThreadStart___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if (lVar5 != 0) {
      Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___c__DisplayClass4_0___ctor
// Address: 017d4fb4
// ==========================================================================================

void native_WebBoxPluginOld___c__DisplayClass4_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__Dispose
// Address: 017d4fbc
// ==========================================================================================

void native_WebBoxPluginOld__Dispose(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008f3 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__Dispose_b__5_0_01fc7b98);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    DAT_021008f3 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x10);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPluginOld___c__Dispose_b__5_0_01fc7b98,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x10) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__Visible
// Address: 017d5104
// ==========================================================================================

undefined native_WebBoxPluginOld__Visible(void)

{
  undefined *puVar1;
  long lVar2;
  long *plVar3;
  undefined *puVar4;
  long lVar5;
  long lVar6;
  undefined8 uVar7;
  
  puVar4 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008f4 & 1) == 0) {
    FUN_00db0bbc(PTR_bool_TypeInfo_01fbf460);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__Visible_b__6_0_01fc7ba0);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    DAT_021008f4 = 1;
  }
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar1 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  lVar5 = *(long *)puVar4;
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar4;
  }
  lVar2 = *(long *)puVar1;
  lVar5 = **(long **)(lVar5 + 0xb8);
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar6 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x18);
  if (lVar6 == 0) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    uVar7 = **(undefined8 **)(lVar2 + 0xb8);
    lVar6 = thunk_FUN_00e11c14(*(undefined8 *)
                                PTR_kairo_unity_ui_IApplication_UIMethod_TypeInfo_01fbfd68);
    kairo_unity_ui_IApplication_UIMethod___ctor
              (lVar6,uVar7,
               *(undefined8 *)PTR_Method_native_WebBoxPluginOld___c__Visible_b__6_0_01fc7ba0,0);
    *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x18) = lVar6;
  }
  if ((lVar5 != 0) &&
     (plVar3 = (long *)Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,lVar6,1,0),
     plVar3 != (long *)0x0)) {
    if (*(long *)(*plVar3 + 0x40) == *(long *)(*(long *)PTR_bool_TypeInfo_01fbf460 + 0x40)) {
      puVar4 = (undefined *)thunk_FUN_00e11d68();
      return *puVar4;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db1180();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__SetVisible
// Address: 017d528c
// ==========================================================================================

void native_WebBoxPluginOld__SetVisible(byte param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_native_WebBoxPluginOld___c__DisplayClass7_0_TypeInfo_01fc7ba8;
  if ((DAT_021008f5 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__DisplayClass7_0__SetVisible_b__0_01fc7bb0);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c__DisplayClass7_0_TypeInfo_01fc7ba8);
    DAT_021008f5 = 1;
  }
  lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar4,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (lVar4 != 0) {
    *(byte *)(lVar4 + 0x10) = param_1 & 1;
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    puVar3 = PTR_Method_native_WebBoxPluginOld___c__DisplayClass7_0__SetVisible_b__0_01fc7bb0;
    puVar2 = PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0;
    lVar5 = *(long *)puVar1;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    lVar5 = **(long **)(lVar5 + 0xb8);
    uVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
    System_Threading_ThreadStart___ctor(uVar6,lVar4,*(undefined8 *)puVar3,0);
    if (lVar5 != 0) {
      Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar5,uVar6,1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___c__DisplayClass7_0___ctor
// Address: 017d53b0
// ==========================================================================================

void native_WebBoxPluginOld___c__DisplayClass7_0___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__SetJavaScriptEnabled
// Address: 017d53b8
// ==========================================================================================

void native_WebBoxPluginOld__SetJavaScriptEnabled(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008f6 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__SetJavaScriptEnabled_b__8_0_01fc7bb8);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    DAT_021008f6 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x20);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)
                PTR_Method_native_WebBoxPluginOld___c__SetJavaScriptEnabled_b__8_0_01fc7bb8,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x20) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld__OpenAuthWebView
// Address: 017d5500
// ==========================================================================================

void native_WebBoxPluginOld__OpenAuthWebView(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_021008f7 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    FUN_00db0bbc(PTR_Method_native_WebBoxPluginOld___c__OpenAuthWebView_b__9_0_01fc7bc0);
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    DAT_021008f7 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  puVar2 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar4);
    lVar4 = *(long *)puVar1;
  }
  lVar3 = *(long *)puVar2;
  lVar4 = **(long **)(lVar4 + 0xb8);
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x28);
  if (lVar5 == 0) {
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar6 = **(undefined8 **)(lVar3 + 0xb8);
    lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_System_Threading_ThreadStart_TypeInfo_01fbf3e0);
    System_Threading_ThreadStart___ctor
              (lVar5,uVar6,
               *(undefined8 *)PTR_Method_native_WebBoxPluginOld___c__OpenAuthWebView_b__9_0_01fc7bc0
               ,0);
    *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x28) = lVar5;
  }
  if (lVar4 != 0) {
    Method_kairo_unity_ui_IApplication_RunOnUiThread(lVar4,lVar5,1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___c___cctor
// Address: 017d5648
// ==========================================================================================

void native_WebBoxPluginOld___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70;
  if ((DAT_021008f8 & 1) == 0) {
    FUN_00db0bbc(PTR_native_WebBoxPluginOld___c_TypeInfo_01fc7b70);
    DAT_021008f8 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: native_WebBoxPluginOld___c___ctor
// Address: 017d56a4
// ==========================================================================================

void native_WebBoxPluginOld___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
