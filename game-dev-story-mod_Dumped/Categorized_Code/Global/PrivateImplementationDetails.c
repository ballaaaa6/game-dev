// Function: PrivateImplementationDetails___ComputeStringHash
// Address: 01a904f4
// ==========================================================================================

uint PrivateImplementationDetails___ComputeStringHash(long param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  
  if (param_1 == 0) {
    uVar2 = 0;
  }
  else {
    uVar2 = 0x811c9dc5;
    if (0 < *(int *)(param_1 + 0x10)) {
      iVar3 = 0;
      do {
        uVar1 = System_String__get_Chars(param_1,iVar3,0);
        iVar3 = iVar3 + 1;
        uVar2 = (uVar2 ^ uVar1 & 0xffff) * 0x1000193;
      } while (iVar3 < *(int *)(param_1 + 0x10));
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: PrivateImplementationDetails___ComputeStringHash
// Address: 01b82d8c
// ==========================================================================================

uint PrivateImplementationDetails___ComputeStringHash(long param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  
  if (param_1 == 0) {
    uVar2 = 0;
  }
  else {
    uVar2 = 0x811c9dc5;
    if (0 < *(int *)(param_1 + 0x10)) {
      iVar3 = 0;
      do {
        uVar1 = System_String__get_Chars(param_1,iVar3,0);
        iVar3 = iVar3 + 1;
        uVar2 = (uVar2 ^ uVar1 & 0xffff) * 0x1000193;
      } while (iVar3 < *(int *)(param_1 + 0x10));
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: PrivateImplementationDetails___ComputeStringHash
// Address: 01cf3998
// ==========================================================================================

uint PrivateImplementationDetails___ComputeStringHash(long param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  
  if (param_1 == 0) {
    uVar2 = 0;
  }
  else {
    uVar2 = 0x811c9dc5;
    if (0 < *(int *)(param_1 + 0x10)) {
      iVar3 = 0;
      do {
        uVar1 = System_String__get_Chars(param_1,iVar3,0);
        iVar3 = iVar3 + 1;
        uVar2 = (uVar2 ^ uVar1 & 0xffff) * 0x1000193;
      } while (iVar3 < *(int *)(param_1 + 0x10));
    }
  }
  return uVar2;
}



// ==========================================================================================
