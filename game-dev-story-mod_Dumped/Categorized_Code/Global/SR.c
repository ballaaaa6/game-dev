// Function: SR__Format
// Address: 01983ce4
// ==========================================================================================

void SR__Format(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_021015d8 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    DAT_021015d8 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  uStack_48 = 0;
  local_50 = 0;
  uStack_38 = 0;
  uStack_40 = 0;
  System_ParamsArray___ctor(&local_50,param_2,0);
  uStack_68 = uStack_48;
  local_70 = local_50;
  uStack_58 = uStack_38;
  uStack_60 = uStack_40;
  Method_System_String_FormatHelper(uVar2,param_1,&local_70);
  return;
}



// ==========================================================================================
// Function: SR__GetString
// Address: 01984b18
// ==========================================================================================

void SR__GetString(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_021015d7 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    DAT_021015d7 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  Method_System_String_Format(uVar2,param_1,param_2);
  return;
}



// ==========================================================================================
// Function: SR__GetString
// Address: 01984b84
// ==========================================================================================

void SR__GetString(undefined8 param_1,long param_2,long param_3)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  if (param_3 != 0) {
    uStack_38 = 0;
    uStack_40 = 0;
    uStack_28 = 0;
    uStack_30 = 0;
    System_ParamsArray___ctor(&uStack_40,param_3,0);
    uStack_58 = uStack_38;
    uStack_60 = uStack_40;
    uStack_48 = uStack_28;
    uStack_50 = uStack_30;
    Method_System_String_FormatHelper(param_1,param_2,&uStack_60);
    return;
  }
  puVar1 = PTR_StringLiteral_7590_01fd28d0;
  if (param_2 != 0) {
    puVar1 = PTR_StringLiteral_6744_01fd28c8;
  }
  uVar2 = thunk_FUN_00e01b94(puVar1);
  thunk_FUN_00e01b94(PTR_System_ArgumentNullException_TypeInfo_01fc5570);
  uVar3 = thunk_FUN_00e11c14();
  System_ArgumentNullException___ctor(uVar3,uVar2,0);
  uVar2 = thunk_FUN_00e01b94(PTR_Method_System_String_Format_01fd28d8);
                    /* WARNING: Subroutine does not return */
  FUN_00db0cb0(uVar3,uVar2);
}



// ==========================================================================================
// Function: SR__GetString
// Address: 01984c38
// ==========================================================================================

void SR__GetString(void)

{
  return;
}



// ==========================================================================================
// Function: SR__Format
// Address: 01984c90
// ==========================================================================================

void SR__Format(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_021015d9 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    DAT_021015d9 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  uStack_48 = 0;
  local_50 = 0;
  uStack_38 = 0;
  uStack_40 = 0;
  System_ParamsArray___ctor(&local_50,param_2,param_3,0);
  uStack_68 = uStack_48;
  local_70 = local_50;
  uStack_58 = uStack_38;
  uStack_60 = uStack_40;
  Method_System_String_FormatHelper(uVar2,param_1,&local_70);
  return;
}



// ==========================================================================================
// Function: SR__Format
// Address: 01984d90
// ==========================================================================================

void SR__Format(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_021015da & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    DAT_021015da = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  uStack_58 = 0;
  local_60 = 0;
  uStack_48 = 0;
  uStack_50 = 0;
  System_ParamsArray___ctor(&local_60,param_2,param_3,param_4,0);
  uStack_78 = uStack_58;
  local_80 = local_60;
  uStack_68 = uStack_48;
  uStack_70 = uStack_50;
  Method_System_String_FormatHelper(uVar2,param_1,&local_80);
  return;
}



// ==========================================================================================
// Function: SR__GetResourceString
// Address: 01984ea4
// ==========================================================================================

void SR__GetResourceString(void)

{
  return;
}



// ==========================================================================================
// Function: SR__Format
// Address: 01b44324
// ==========================================================================================

void SR__Format(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_02102735 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    DAT_02102735 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  System_String__Format(uVar2,param_1,param_2,0);
  return;
}



// ==========================================================================================
