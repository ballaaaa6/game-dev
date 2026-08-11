// Function: R_Library_Kairolib__get_ButtonLanguage
// Address: 017ce8bc
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonLanguage(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a3 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a3 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (*(int *)(lVar2 + 0x18) != 0) {
      return *(undefined8 *)(lVar2 + 0x20);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ConnectingBg
// Address: 017ce964
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ConnectingBg(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a4 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a4 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (1 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x28);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ConnectingAnim
// Address: 017cea10
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ConnectingAnim(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a5 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a5 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (2 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x30);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Balloon
// Address: 017ceabc
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Balloon(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a6 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a6 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (3 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x38);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonCancel
// Address: 017ceb68
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonCancel(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a7 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a7 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (4 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x40);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Ranking
// Address: 017cec14
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Ranking(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a8 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a8 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (5 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x48);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Linked
// Address: 017cecc0
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Linked(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008a9 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008a9 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (6 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x50);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Unlinked
// Address: 017ced6c
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Unlinked(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008aa & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008aa = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (7 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x58);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_SafeareaBg
// Address: 017cee18
// ==========================================================================================

undefined8 R_Library_Kairolib__get_SafeareaBg(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ab & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008ab = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (8 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x60);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_IPhoneX
// Address: 017ceec4
// ==========================================================================================

undefined8 R_Library_Kairolib__get_IPhoneX(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ac & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008ac = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (9 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x68);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ScreenCursor
// Address: 017cef70
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ScreenCursor(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ad & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008ad = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (10 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x70);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonMigration
// Address: 017cf01c
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonMigration(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ae & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008ae = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0xb < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x78);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_DataTransfer
// Address: 017cf0c8
// ==========================================================================================

undefined8 R_Library_Kairolib__get_DataTransfer(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008af & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008af = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0xc < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x80);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonsSwitch
// Address: 017cf174
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonsSwitch(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b0 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b0 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0xd < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x88);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonsPs4
// Address: 017cf220
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonsPs4(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b1 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b1 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x13 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xb8);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonsXbox
// Address: 017cf2cc
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonsXbox(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b2 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b2 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x1d < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x108);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Window
// Address: 017cf378
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Window(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b3 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b3 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0xe < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x90);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_PrivacyPolicy
// Address: 017cf424
// ==========================================================================================

undefined8 R_Library_Kairolib__get_PrivacyPolicy(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b4 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b4 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0xf < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x98);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_CurrencyPolicy
// Address: 017cf4d0
// ==========================================================================================

undefined8 R_Library_Kairolib__get_CurrencyPolicy(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b5 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b5 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x10 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xa0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_AutoSave
// Address: 017cf57c
// ==========================================================================================

undefined8 R_Library_Kairolib__get_AutoSave(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b6 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b6 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x11 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xa8);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Kairokun
// Address: 017cf628
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Kairokun(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b7 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b7 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x12 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xb0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Emoji
// Address: 017cf6d4
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Emoji(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b8 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b8 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x14 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xc0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_NewText
// Address: 017cf780
// ==========================================================================================

undefined8 R_Library_Kairolib__get_NewText(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008b9 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008b9 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x15 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 200);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_SteamBg
// Address: 017cf82c
// ==========================================================================================

undefined8 R_Library_Kairolib__get_SteamBg(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ba & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008ba = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x16 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xd0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonGamePad
// Address: 017cf8d8
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonGamePad(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008bb & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008bb = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x17 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xd8);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Splash
// Address: 017cf984
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Splash(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008bc & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008bc = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x18 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xe0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonKeyboard
// Address: 017cfa30
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonKeyboard(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008bd & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008bd = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x19 < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xe8);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonReview
// Address: 017cfadc
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonReview(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008be & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008be = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x1a < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xf0);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_RightClick
// Address: 017cfb88
// ==========================================================================================

undefined8 R_Library_Kairolib__get_RightClick(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008bf & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008bf = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x1b < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0xf8);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_ButtonStorageDelete
// Address: 017cfc34
// ==========================================================================================

undefined8 R_Library_Kairolib__get_ButtonStorageDelete(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c0 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c0 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x1c < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x100);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_Review
// Address: 017cfce0
// ==========================================================================================

undefined8 R_Library_Kairolib__get_Review(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c1 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c1 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if ((**(long **)(lVar2 + 0xb8) != 0) &&
     (lVar2 = *(long *)(**(long **)(lVar2 + 0xb8) + 0x18), lVar2 != 0)) {
    if (0x1e < *(uint *)(lVar2 + 0x18)) {
      return *(undefined8 *)(lVar2 + 0x110);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_seb
// Address: 017cfd8c
// ==========================================================================================

undefined8 R_Library_Kairolib__get_seb(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c2 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c2 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    return *(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x18);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_img
// Address: 017cfe20
// ==========================================================================================

undefined8 R_Library_Kairolib__get_img(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c3 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c3 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    return *(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x10);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_sound
// Address: 017cfeb4
// ==========================================================================================

undefined8 R_Library_Kairolib__get_sound(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c4 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c4 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02100977 == '\0') {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_02100977 = '\x01';
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    return *(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x20);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__get_resource
// Address: 017cff48
// ==========================================================================================

undefined8 R_Library_Kairolib__get_resource(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c5 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c5 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return **(undefined8 **)(lVar2 + 0xb8);
}



// ==========================================================================================
// Function: R_Library_Kairolib__set_resource
// Address: 017cffa0
// ==========================================================================================

void R_Library_Kairolib__set_resource(undefined8 param_1)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c6 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c6 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  **(undefined8 **)(lVar2 + 0xb8) = param_1;
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawConnectingAnim
// Address: 017cfffc
// ==========================================================================================

void R_Library_Kairolib__DrawConnectingAnim(undefined8 param_1,uint param_2)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  long *plVar4;
  
  if ((DAT_021008c7 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c7 = 1;
  }
  if (DAT_02100978 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968);
    DAT_02100978 = '\x01';
  }
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  plVar4 = *(long **)(*(long *)(*(long *)
                                 PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968 + 0xb8
                               ) + 8);
  if (plVar4 != (long *)0x0) {
    iVar2 = (**(code **)(*plVar4 + 0x218))(plVar4,*(undefined8 *)(*plVar4 + 0x220));
    iVar3 = (**(code **)(*plVar4 + 0x228))(plVar4,*(undefined8 *)(*plVar4 + 0x230));
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    if (iVar2 < 0) {
      iVar2 = iVar2 + 1;
    }
    if (iVar3 < 0) {
      iVar3 = iVar3 + 1;
    }
    R_Library_Kairolib__DrawConnectingAnim(param_1,iVar2 >> 1,iVar3 >> 1,param_2 & 1);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawConnectingAnim
// Address: 017d00e8
// ==========================================================================================

void R_Library_Kairolib__DrawConnectingAnim(long param_1,int param_2,int param_3,ulong param_4)

{
  int iVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  undefined8 uVar5;
  long lVar6;
  long lVar7;
  long lVar8;
  
  puVar2 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c8 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8);
    DAT_021008c8 = 1;
  }
  lVar4 = java_lang_JSystem__CurrentTimeMillis(0);
  lVar6 = *(long *)puVar2;
  if (*(int *)(lVar6 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar6);
    lVar6 = *(long *)puVar2;
  }
  lVar7 = *(long *)(lVar6 + 0xb8);
  lVar8 = *(long *)(lVar7 + 0x10);
  if (lVar4 - lVar8 < 0x2711) {
    lVar4 = (lVar4 - lVar8) / 100;
    if (*(int *)(lVar6 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar6);
      lVar6 = *(long *)puVar2;
      lVar7 = *(long *)(lVar6 + 0xb8);
      lVar8 = *(long *)(lVar7 + 0x10);
    }
    *(int *)(lVar7 + 0x18) = *(int *)(lVar7 + 0x18) + (int)lVar4;
    *(long *)(lVar7 + 0x10) = lVar8 + (lVar4 * 0x6400000000 >> 0x20);
  }
  else {
    if (*(int *)(lVar6 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar6);
      lVar6 = *(long *)puVar2;
      lVar7 = *(long *)(lVar6 + 0xb8);
    }
    *(long *)(lVar7 + 0x10) = lVar4;
    *(undefined4 *)(lVar7 + 0x18) = 0;
  }
  if ((param_4 & 1) != 0) {
    if (*(int *)(lVar6 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar6);
    }
    lVar4 = R_Library_Kairolib__get_ConnectingBg();
    if (lVar4 == 0) goto LAB_017d0300;
    kairo_unity_ui_Seb__Draw((float)param_2,(float)param_3,lVar4,param_1,0);
    lVar6 = *(long *)puVar2;
  }
  puVar3 = PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8;
  if (*(int *)(lVar6 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar6);
    lVar6 = *(long *)puVar2;
  }
  iVar1 = *(int *)(*(long *)(lVar6 + 0xb8) + 0x18);
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = kairo_unity_ui_Matrix__RotateTemporary((float)((iVar1 * 0x1e) % 0x168),0,0,0);
  if (param_1 != 0) {
    kairo_unity_ui_Graphics__PushMatrix(param_1,uVar5,0);
    lVar4 = R_Library_Kairolib__get_ConnectingAnim();
    if (lVar4 != 0) {
      kairo_unity_ui_Seb__Draw((float)param_2,(float)param_3,lVar4,param_1,0,0xffffffff,0);
      kairo_unity_ui_Graphics__PopMatrix(param_1,0);
      return;
    }
  }
LAB_017d0300:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawPrivacyPolicy
// Address: 017d0304
// ==========================================================================================

void R_Library_Kairolib__DrawPrivacyPolicy
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined *puVar1;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008c9 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008c9 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  R_Library_Kairolib__DrawPrivacyPolicy(param_1,param_2,param_3,3,param_4);
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawPrivacyPolicy
// Address: 017d0384
// ==========================================================================================

void R_Library_Kairolib__DrawPrivacyPolicy
               (long param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  undefined8 uVar13;
  undefined auStack_78 [8];
  int local_70;
  int iStack_6c;
  
  puVar3 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008ca & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_OnTouchEventDelegate_TypeInfo_01fc5450);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
    FUN_00db0bbc(PTR_Method_R_Library_Kairolib___c__DrawPrivacyPolicy_b__114_0_01fc7970);
    FUN_00db0bbc(PTR_R_Library_Kairolib___c_TypeInfo_01fc7978);
    DAT_021008ca = 1;
  }
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar9 = R_Library_Kairolib__get_PrivacyPolicy();
  puVar3 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if (lVar9 != 0) {
    kairo_unity_ui_Seb__GetBRect(auStack_78,lVar9,0);
    if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar9 = kairo_unity_ui_Graphics__GetAnchorPosition(param_2,param_3,local_70,iStack_6c,param_5,0)
    ;
    if (lVar9 != 0) {
      if ((*(int *)(lVar9 + 0x18) == 0) || (*(int *)(lVar9 + 0x18) == 1)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      iVar1 = *(int *)(lVar9 + 0x20);
      iVar2 = *(int *)(lVar9 + 0x24);
      if (DAT_02100978 == '\0') {
        FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968);
        DAT_02100978 = '\x01';
      }
      puVar3 = PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968;
      lVar9 = *(long *)(*(long *)(*(long *)
                                   PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968 +
                                 0xb8) + 8);
      if (lVar9 != 0) {
        uVar6 = kairo_unity_surface_SurfaceBase__CheckTouch(lVar9,param_4,0x136,0);
        lVar9 = R_Library_Kairolib__get_PrivacyPolicy();
        if (lVar9 != 0) {
          kairo_unity_ui_Seb__Draw((float)iVar1,(float)iVar2,lVar9,param_1,uVar6 & 1,0xffffffff,0);
          if (DAT_02100978 == '\0') {
            FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968);
            DAT_02100978 = '\x01';
          }
          puVar5 = PTR_R_Library_Kairolib___c_TypeInfo_01fc7978;
          puVar4 = PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888;
          if (param_1 != 0) {
            lVar9 = *(long *)(*(long *)(*(long *)puVar3 + 0xb8) + 8);
            iVar7 = kairo_unity_ui_Graphics__GetOriginX(param_1,0);
            iVar8 = kairo_unity_ui_Graphics__GetOriginY(param_1,0);
            if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
              thunk_FUN_00df405c(*(long *)puVar4);
            }
            lVar10 = kairo_unity_surface_TouchOption__Create(0x400,0);
            lVar11 = *(long *)puVar5;
            if (*(int *)(lVar11 + 0xe0) == 0) {
              thunk_FUN_00df405c(lVar11);
              lVar11 = *(long *)puVar5;
            }
            lVar12 = *(long *)(*(long *)(lVar11 + 0xb8) + 8);
            if (lVar12 == 0) {
              if (*(int *)(lVar11 + 0xe0) == 0) {
                thunk_FUN_00df405c(lVar11);
                lVar11 = *(long *)puVar5;
              }
              uVar13 = **(undefined8 **)(lVar11 + 0xb8);
              lVar12 = thunk_FUN_00e11c14(*(undefined8 *)
                                           PTR_kairo_unity_surface_TouchOption_OnTouchEventDelegate_TypeInfo_01fc5450
                                         );
              kairo_unity_surface_TouchOption_OnTouchEventDelegate___ctor
                        (lVar12,uVar13,
                         *(undefined8 *)
                          PTR_Method_R_Library_Kairolib___c__DrawPrivacyPolicy_b__114_0_01fc7970,0);
              *(long *)(*(long *)(*(long *)puVar5 + 0xb8) + 8) = lVar12;
            }
            if ((lVar10 != 0) &&
               (uVar13 = kairo_unity_surface_TouchOption__OnTouchEvent(lVar10,lVar12,0), lVar9 != 0)
               ) {
              kairo_unity_surface_SurfaceBase__AddTouchComponent
                        (lVar9,param_4,iVar1 + iVar7 + -10,iVar2 + iVar8 + -10,local_70 + 0x14,
                         iStack_6c + 0x14,0x136,uVar13,0);
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
// Function: R_Library_Kairolib__DrawCurrencyPolicy
// Address: 017d067c
// ==========================================================================================

void R_Library_Kairolib__DrawCurrencyPolicy
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  undefined *puVar1;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008cb & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008cb = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  R_Library_Kairolib__DrawCurrencyPolicy(param_1,param_2,param_3,param_4,3,param_5);
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawCurrencyPolicy
// Address: 017d0704
// ==========================================================================================

void R_Library_Kairolib__DrawCurrencyPolicy
               (long param_1,undefined4 param_2,undefined4 param_3,int param_4,undefined4 param_5,
               undefined4 param_6)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  ulong uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  long lVar13;
  long lVar14;
  long lVar15;
  float fVar16;
  undefined auStack_88 [8];
  int local_80;
  int iStack_7c;
  
  puVar3 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_021008cc & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_OnTouchEventDelegate_TypeInfo_01fc5450);
    FUN_00db0bbc(PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888);
    FUN_00db0bbc(PTR_Method_R_Library_Kairolib___c__DrawCurrencyPolicy_b__116_0_01fc7980);
    FUN_00db0bbc(PTR_R_Library_Kairolib___c_TypeInfo_01fc7978);
    FUN_00db0bbc(PTR_StringLiteral_12148_01fc7988);
    FUN_00db0bbc(PTR_StringLiteral_11509_01fc7990);
    FUN_00db0bbc(PTR_StringLiteral_12149_01fc7998);
    DAT_021008cc = 1;
  }
  lVar9 = *(long *)puVar3;
  if (*(int *)(lVar9 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar9 = *(long *)puVar3;
  }
  lVar13 = *(long *)(lVar9 + 0xb8);
  if (*(char *)(lVar13 + 0x30) == '\0') {
    if (*(int *)(lVar9 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar9 = *(long *)puVar3;
      lVar13 = *(long *)(lVar9 + 0xb8);
    }
    if (*(char *)(lVar13 + 0x10) == '\0') {
      if (*(int *)(lVar9 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar9 = *(long *)puVar3;
      }
      if (**(int **)(lVar9 + 0xb8) != 3) {
        return;
      }
      if (*(int *)(*(long *)PTR_kairo_unity_util_Language_TypeInfo_01fbf348 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar10 = kairo_unity_util_Language__Japanese(0);
      if ((uVar10 & 1) == 0) {
        return;
      }
    }
  }
  if (*(int *)(*(long *)PTR_R_Library_Kairolib_TypeInfo_01fbf5b0 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar9 = R_Library_Kairolib__get_CurrencyPolicy();
  puVar3 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if (lVar9 != 0) {
    kairo_unity_ui_Seb__GetBRect(auStack_88,lVar9,param_4 << 1,0);
    if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar9 = kairo_unity_ui_Graphics__GetAnchorPosition(param_2,param_3,local_80,iStack_7c,param_6,0)
    ;
    if (lVar9 != 0) {
      if ((*(int *)(lVar9 + 0x18) == 0) || (*(int *)(lVar9 + 0x18) == 1)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      iVar1 = *(int *)(lVar9 + 0x20);
      iVar2 = *(int *)(lVar9 + 0x24);
      if (DAT_02100978 == '\0') {
        FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968);
        DAT_02100978 = '\x01';
      }
      puVar3 = PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968;
      lVar9 = *(long *)(*(long *)(*(long *)
                                   PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968 +
                                 0xb8) + 8);
      if (lVar9 != 0) {
        uVar6 = kairo_unity_surface_SurfaceBase__CheckTouch(lVar9,param_5,0x231,0);
        lVar9 = R_Library_Kairolib__get_CurrencyPolicy();
        if ((lVar9 != 0) &&
           (kairo_unity_ui_Seb__Draw
                      ((float)iVar1,(float)iVar2,lVar9,param_1,param_4 << 1 | uVar6 & 1,0xffffffff,0
                      ), param_1 != 0)) {
          kairo_unity_ui_Graphics__SetColor(param_1,0,0,0,0);
          puVar5 = PTR_StringLiteral_11509_01fc7990;
          puVar4 = PTR_StringLiteral_12148_01fc7988;
          if (param_4 == 0) {
            kairo_unity_ui_Graphics__PushFont(param_1,8,0);
            uVar12 = 0x22;
            uVar11 = *(undefined8 *)PTR_StringLiteral_12149_01fc7998;
            iVar7 = local_80;
            if (local_80 < 0) {
              iVar7 = local_80 + 1;
            }
            iVar8 = iStack_7c;
            if (iStack_7c < 0) {
              iVar8 = iStack_7c + 1;
            }
            fVar16 = (float)(iVar1 + (iVar7 >> 1));
            iVar7 = iVar2 + (iVar8 >> 1) + 1;
          }
          else {
            kairo_unity_ui_Graphics__PushFont(param_1,5,0);
            fVar16 = (float)(iVar1 + 4);
            iVar7 = iStack_7c;
            if (iStack_7c < 0) {
              iVar7 = iStack_7c + 1;
            }
            iVar7 = iVar2 + (iVar7 >> 1);
            kairo_unity_ui_Graphics__DrawString
                      (fVar16,(float)(iVar7 + -3),param_1,*(undefined8 *)puVar4,0x20,0);
            uVar11 = *(undefined8 *)puVar5;
            iVar7 = iVar7 + 5;
            uVar12 = 0x20;
          }
          kairo_unity_ui_Graphics__DrawString(fVar16,(float)iVar7,param_1,uVar11,uVar12,0);
          puVar4 = PTR_kairo_unity_surface_TouchOption_TypeInfo_01fbf888;
          kairo_unity_ui_Graphics__PopFont(param_1,0);
          if (DAT_02100978 == '\0') {
            FUN_00db0bbc(PTR_kairo_unity_surface_SurfaceManagerBase_TypeInfo_01fc7968);
            DAT_02100978 = '\x01';
          }
          puVar5 = PTR_R_Library_Kairolib___c_TypeInfo_01fc7978;
          lVar9 = *(long *)(*(long *)(*(long *)puVar3 + 0xb8) + 8);
          iVar7 = kairo_unity_ui_Graphics__GetOriginX(param_1,0);
          iVar8 = kairo_unity_ui_Graphics__GetOriginY(param_1,0);
          if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
            thunk_FUN_00df405c(*(long *)puVar4);
          }
          lVar13 = kairo_unity_surface_TouchOption__Create(0x400,0);
          lVar14 = *(long *)puVar5;
          if (*(int *)(lVar14 + 0xe0) == 0) {
            thunk_FUN_00df405c(lVar14);
            lVar14 = *(long *)puVar5;
          }
          lVar15 = *(long *)(*(long *)(lVar14 + 0xb8) + 0x10);
          if (lVar15 == 0) {
            if (*(int *)(lVar14 + 0xe0) == 0) {
              thunk_FUN_00df405c(lVar14);
              lVar14 = *(long *)puVar5;
            }
            uVar11 = **(undefined8 **)(lVar14 + 0xb8);
            lVar15 = thunk_FUN_00e11c14(*(undefined8 *)
                                         PTR_kairo_unity_surface_TouchOption_OnTouchEventDelegate_TypeInfo_01fc5450
                                       );
            kairo_unity_surface_TouchOption_OnTouchEventDelegate___ctor
                      (lVar15,uVar11,
                       *(undefined8 *)
                        PTR_Method_R_Library_Kairolib___c__DrawCurrencyPolicy_b__116_0_01fc7980,0);
            *(long *)(*(long *)(*(long *)puVar5 + 0xb8) + 0x10) = lVar15;
          }
          if ((lVar13 != 0) &&
             (uVar11 = kairo_unity_surface_TouchOption__OnTouchEvent(lVar13,lVar15,0), lVar9 != 0))
          {
            kairo_unity_surface_SurfaceBase__AddTouchComponent
                      (lVar9,param_5,iVar1 + iVar7 + -10,iVar2 + iVar8 + -10,local_80 + 0x14,
                       iStack_7c + 0x14,0x231,uVar11,0);
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
// Function: R_Library_Kairolib__SetAutoSavePosition
// Address: 017d0bac
// ==========================================================================================

void R_Library_Kairolib__SetAutoSavePosition(undefined4 param_1,undefined4 param_2)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008cd & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008cd = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = *(long *)(lVar2 + 0xb8);
  *(undefined4 *)(lVar2 + 0x20) = param_1;
  *(undefined4 *)(lVar2 + 0x24) = param_2;
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawAutoSaveAnim
// Address: 017d0c14
// ==========================================================================================

void R_Library_Kairolib__DrawAutoSaveAnim(long param_1,ulong param_2,ulong param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  float fVar5;
  
  if ((DAT_021008ce & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8);
    DAT_021008ce = 1;
  }
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  fVar5 = 1.0;
  if ((param_3 & 1) != 0) {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    lVar3 = *(long *)puVar1;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    if (**(long **)(lVar3 + 0xb8) == 0) goto LAB_017d0f2c;
    fVar5 = (float)kairo_unity_ui_IApplication__GetScaleRatio(**(long **)(lVar3 + 0xb8),0,0);
    fVar5 = fVar5 / 100.0;
  }
  puVar1 = PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8;
  if (*(int *)(*(long *)PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar4 = kairo_unity_ui_Matrix__ScaleTemporary(fVar5,fVar5,0,0,0);
  puVar2 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if (param_1 != 0) {
    kairo_unity_ui_Graphics__PushMatrix(param_1,uVar4,0);
    lVar3 = *(long *)puVar2;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    *(int *)(*(long *)(lVar3 + 0xb8) + 0x1c) = (*(int *)(*(long *)(lVar3 + 0xb8) + 0x1c) + 1) % 0xc;
    if ((param_2 & 1) != 0) {
      kairo_unity_ui_Graphics__SetColor(param_1,0,0,0,0x80,0);
      lVar3 = *(long *)puVar2;
      if (*(int *)(lVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar3 = *(long *)puVar2;
      }
      kairo_unity_ui_Graphics__FillRect
                (fVar5 * (float)(*(int *)(*(long *)(lVar3 + 0xb8) + 0x20) + -0x1e),
                 fVar5 * (float)*(int *)(*(long *)(lVar3 + 0xb8) + 0x24),0x42740000,0x42740000,
                 param_1,0);
    }
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar4 = kairo_unity_ui_Matrix__ScaleTemporary(0x3f000000,0x3f000000,0,0,0);
    kairo_unity_ui_Graphics__PushMatrix(param_1,uVar4,0);
    lVar3 = *(long *)puVar2;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar2;
    }
    uVar4 = kairo_unity_ui_Matrix__RotateTemporary
                      ((float)((*(int *)(*(long *)(lVar3 + 0xb8) + 0x1c) * 0x1e) % 0x168),0,0,0);
    kairo_unity_ui_Graphics__PushMatrix(param_1,uVar4,0);
    lVar3 = R_Library_Kairolib__get_ConnectingAnim();
    if (lVar3 != 0) {
      kairo_unity_ui_Seb__Draw
                (fVar5 * (float)*(int *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x20),
                 fVar5 * (float)(*(int *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x24) + 0x25),lVar3,
                 param_1,0,0xffffffff,0);
      kairo_unity_ui_Graphics__PopMatrix(param_1,0);
      kairo_unity_ui_Graphics__PopMatrix(param_1,0);
      lVar3 = R_Library_Kairolib__get_AutoSave();
      if (lVar3 != 0) {
        kairo_unity_ui_Seb__Draw
                  (fVar5 * (float)*(int *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x20),
                   fVar5 * (float)*(int *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x24),lVar3,param_1,0
                   ,0xffffffff,0);
        kairo_unity_ui_Graphics__PopMatrix(param_1,0);
        return;
      }
    }
  }
LAB_017d0f2c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawButtons
// Address: 017d0f30
// ==========================================================================================

void R_Library_Kairolib__DrawButtons
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,uint param_6)

{
  undefined *puVar1;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008cf & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008cf = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  R_Library_Kairolib___drawButtons(param_1,param_2,param_3,param_4,param_5,param_6 & 1,0);
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib___drawButtons
// Address: 017d0fc8
// ==========================================================================================

void R_Library_Kairolib___drawButtons
               (undefined8 param_1,int param_2,int param_3,int param_4,int param_5,uint param_6,
               uint param_7)

{
  int iVar1;
  int iVar2;
  undefined *puVar3;
  long lVar4;
  ulong uVar5;
  
  puVar3 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_021008d1 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8);
    FUN_00db0bbc(PTR_kairo_unity_ui_SteamInputManager_TypeInfo_01fc3c70);
    DAT_021008d1 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  if (**(int **)(lVar4 + 0xb8) == 4) {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_SteamInputManager_TypeInfo_01fc3c70 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar5 = kairo_unity_ui_SteamInputManager__HasController(0);
    if (((param_4 != 7) && ((uVar5 & 1) == 0)) && ((param_7 & 1) == 0)) {
      return;
    }
  }
  if (*(int *)(*(long *)PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_ui_Canvas__GetInstance(0);
  if ((param_6 & 1) != 0) {
    if (param_4 == 1) {
      if (lVar4 == 0) goto LAB_017d1268;
      param_4 = kairo_unity_ui_Canvas__GetJoystickKeyCancel(lVar4,0);
    }
    else if (param_4 == 0) {
      if (lVar4 == 0) goto LAB_017d1268;
      param_4 = kairo_unity_ui_Canvas__GetJoystickKeyOK(lVar4,0);
    }
  }
  puVar3 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if (param_5 == 1) {
    iVar2 = 0x20;
    if (param_4 != 0x10) {
      iVar2 = param_4;
    }
    iVar1 = 0x21;
    if (iVar2 != 0x11) {
      iVar1 = iVar2;
    }
    iVar2 = 0x22;
    if (iVar1 != 0x12) {
      iVar2 = iVar1;
    }
    param_4 = 0x23;
    if (iVar2 != 0x13) {
      param_4 = iVar2;
    }
  }
  if (lVar4 == 0) goto LAB_017d1268;
  iVar2 = *(int *)(lVar4 + 0x144);
  if (iVar2 == 1) {
    if (*(int *)(*(long *)PTR_R_Library_Kairolib_TypeInfo_01fbf5b0 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar4 = R_Library_Kairolib__get_ButtonsSwitch();
joined_r0x017d11ac:
    if (lVar4 == 0) goto LAB_017d1268;
    kairo_unity_ui_Seb__Draw((float)param_2,(float)param_3,lVar4,param_1,param_4,0,0);
  }
  else {
    if (iVar2 == 3) {
      if (*(int *)(*(long *)PTR_R_Library_Kairolib_TypeInfo_01fbf5b0 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar4 = R_Library_Kairolib__get_ButtonsXbox();
      goto joined_r0x017d11ac;
    }
    if (iVar2 == 2) {
      if (*(int *)(*(long *)PTR_R_Library_Kairolib_TypeInfo_01fbf5b0 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar4 = R_Library_Kairolib__get_ButtonsPs4();
      goto joined_r0x017d11ac;
    }
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  if (*(char *)(*(long *)(lVar4 + 0xb8) + 8) != '\0') {
    if (DAT_020ff90e == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_form_FormManagerBase_TypeInfo_01fc5a08);
      DAT_020ff90e = '\x01';
    }
    if (**(long **)(*(long *)PTR_kairo_unity_form_FormManagerBase_TypeInfo_01fc5a08 + 0xb8) == 0) {
LAB_017d1268:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar4 = kairo_unity_form_FormManagerBase__GetCurrentForm
                      (**(long **)(*(long *)PTR_kairo_unity_form_FormManagerBase_TypeInfo_01fc5a08 +
                                  0xb8),0);
    if (lVar4 != 0) {
      kairo_unity_form_FormBase__SetAutoCancelJoystick(lVar4,param_4,0);
      return;
    }
  }
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawButtons
// Address: 017d126c
// ==========================================================================================

void R_Library_Kairolib__DrawButtons
               (undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,uint param_6,uint param_7)

{
  undefined *puVar1;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008d0 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008d0 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  R_Library_Kairolib___drawButtons(param_1,param_2,param_3,param_4,param_5,param_6 & 1,param_7 & 1);
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawNewText
// Address: 017d1308
// ==========================================================================================

void R_Library_Kairolib__DrawNewText
               (undefined8 param_1,undefined8 param_2,undefined param_3 [16],long param_4,
               int param_5)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  if ((DAT_021008d2 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8);
    DAT_021008d2 = 1;
  }
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if (param_3._0_4_ == 1.0) {
    if (*(int *)(*(long *)PTR_R_Library_Kairolib_TypeInfo_01fbf5b0 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar2 = R_Library_Kairolib__get_NewText();
    if (lVar2 != 0) {
      kairo_unity_ui_Seb__Draw(param_1,param_2,lVar2,param_4,param_5 % 0x10,0xffffffff,0);
      return;
    }
  }
  else {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_Matrix_TypeInfo_01fbf5b8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar3 = kairo_unity_ui_Matrix__ScaleTemporary(param_3._0_8_,param_3._0_8_,0,0,0);
    if (param_4 != 0) {
      kairo_unity_ui_Graphics__PushMatrix(param_4,uVar3,0);
      if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      lVar2 = R_Library_Kairolib__get_NewText();
      if (lVar2 != 0) {
        kairo_unity_ui_Seb__Draw(param_1,param_2,lVar2,param_4,param_5 % 0x10,0xffffffff,0);
        kairo_unity_ui_Graphics__PopMatrix(param_4,0);
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: R_Library_Kairolib__DrawTouchEffect
// Address: 017d1468
// ==========================================================================================

void R_Library_Kairolib__DrawTouchEffect
               (float param_1,float param_2,long param_3,int param_4,int param_5)

{
  undefined *puVar1;
  int iVar2;
  long lVar3;
  float fVar4;
  float fVar5;
  
  if ((DAT_021008d3 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008d3 = 1;
  }
  if (param_5 < 2) {
    param_5 = 1;
  }
  iVar2 = kairo_unity_graph_Graph__Easing(0xff,0,param_5,param_4,0,0);
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (0 < iVar2) {
    if (*(int *)(*(long *)PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    lVar3 = *(long *)puVar1;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    if (**(long **)(lVar3 + 0xb8) != 0) {
      fVar4 = (float)kairo_unity_ui_IApplication__GetScaleRatio(**(long **)(lVar3 + 0xb8),0,0);
      fVar5 = (float)kairo_unity_graph_Graph__Easing
                               (0x3f800000,0x3fc00000,(float)param_5,(float)param_4,0,0);
      puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
      if (param_3 != 0) {
        kairo_unity_ui_Graphics__SetRenderMode(param_3,1,iVar2,0xff - iVar2,0);
        if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        if (DAT_02100977 == '\0') {
          FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
          DAT_02100977 = '\x01';
        }
        lVar3 = *(long *)puVar1;
        if (*(int *)(lVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar3 = *(long *)puVar1;
        }
        if ((**(long **)(lVar3 + 0xb8) != 0) &&
           (lVar3 = *(long *)(**(long **)(lVar3 + 0xb8) + 0x10), lVar3 != 0)) {
          if (0x19 < *(uint *)(lVar3 + 0x18)) {
            fVar4 = (fVar4 / 100.0) * fVar5 * 80.0;
            kairo_unity_ui_Graphics__DrawScaledImage
                      (param_1 - fVar4 * 0.5,param_2 - fVar4 * 0.5,fVar4,fVar4,param_3,
                       *(undefined8 *)(lVar3 + 0xe8),0,0,0x50,0x50,0);
            kairo_unity_ui_Graphics__SetRenderMode(param_3,0,0xff,0,0);
            return;
          }
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib___cctor
// Address: 017d16a8
// ==========================================================================================

void R_Library_Kairolib___cctor(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_R_Library_Kairolib_TypeInfo_01fbf5b0;
  if ((DAT_021008d4 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib_TypeInfo_01fbf5b0);
    DAT_021008d4 = 1;
  }
  lVar2 = *(long *)(*(long *)puVar1 + 0xb8);
  *(undefined *)(lVar2 + 8) = 1;
  *(undefined8 *)(lVar2 + 0x20) = 0;
  *(undefined4 *)(lVar2 + 0x1c) = 0;
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib___c___cctor
// Address: 017d16fc
// ==========================================================================================

void R_Library_Kairolib___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_R_Library_Kairolib___c_TypeInfo_01fc7978;
  if ((DAT_021008d5 & 1) == 0) {
    FUN_00db0bbc(PTR_R_Library_Kairolib___c_TypeInfo_01fc7978);
    DAT_021008d5 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: R_Library_Kairolib___c___ctor
// Address: 017d1758
// ==========================================================================================

void R_Library_Kairolib___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
