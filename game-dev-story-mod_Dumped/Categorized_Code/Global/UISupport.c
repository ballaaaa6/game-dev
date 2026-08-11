// Function: UISupport__Initialize
// Address: 01b84d0c
// ==========================================================================================

void UISupport__Initialize(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar1 = PTR_UnityEngine_InputSystem_InputSystem_TypeInfo_01fc5be8;
  if ((DAT_02102943 & 1) == 0) {
    FUN_00db0bbc(PTR_UnityEngine_InputSystem_InputSystem_TypeInfo_01fc5be8);
    FUN_00db0bbc(PTR_StringLiteral_50_01fe0740);
    DAT_02102943 = 1;
  }
  puVar2 = PTR_StringLiteral_50_01fe0740;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  UnityEngine_InputSystem_InputSystem__RegisterLayout(*(undefined8 *)puVar2,0,0,0,0);
  return;
}



// ==========================================================================================
