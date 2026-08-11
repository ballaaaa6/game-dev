// Function: main_AppData__GetInstance
// Address: 00f73d0c
// ==========================================================================================

undefined8 main_AppData__GetInstance(void)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7f7 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff7f7 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) == 0) {
    uVar3 = thunk_FUN_00e11c14();
    main_AppData___ctor();
    lVar2 = *(long *)puVar1;
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    **(undefined8 **)(lVar2 + 0xb8) = uVar3;
    if (**(long **)(*(long *)puVar1 + 0xb8) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    main_AppData__Init();
    lVar2 = *(long *)puVar1;
  }
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return **(undefined8 **)(lVar2 + 0xb8);
}



// ==========================================================================================
// Function: main_Anim__Init
// Address: 00f75a10
// ==========================================================================================

void main_Anim__Init(long param_1)

{
  ulong uVar1;
  long lVar2;
  undefined4 *puVar3;
  
  if (param_1 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar1 = (ulong)*(uint *)(param_1 + 0x18);
  if (0 < (long)(uVar1 << 0x20)) {
    lVar2 = (long)(int)*(uint *)(param_1 + 0x18);
    puVar3 = (undefined4 *)(param_1 + 0x20);
    do {
      if (uVar1 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *puVar3 = 0;
      lVar2 = lVar2 + -1;
      uVar1 = uVar1 - 1;
      puVar3 = puVar3 + 1;
    } while (lVar2 != 0);
  }
  return;
}



// ==========================================================================================
// Function: main_Anim__Init
// Address: 00f75a54
// ==========================================================================================

void main_Anim__Init(long param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  ulong uVar4;
  long lVar5;
  
  if (param_1 == 0) {
LAB_00f75acc:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar1 = *(uint *)(param_1 + 0x18);
  if (0 < (int)uVar1) {
    uVar3 = 0;
    do {
      if (uVar3 == uVar1) {
LAB_00f75ac8:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      lVar5 = *(long *)(param_1 + (long)(int)uVar3 * 8 + 0x20);
      if (lVar5 == 0) goto LAB_00f75acc;
      uVar2 = *(uint *)(lVar5 + 0x18);
      uVar4 = 0;
      while ((long)uVar4 < (long)(int)uVar2) {
        if (uVar2 <= uVar4) goto LAB_00f75ac8;
        *(undefined4 *)(lVar5 + 0x20 + uVar4 * 4) = 0;
        uVar4 = uVar4 + 1;
        if (uVar1 <= uVar3) goto LAB_00f75ac8;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 != uVar1);
  }
  return;
}



// ==========================================================================================
// Function: main_Anim___ctor
// Address: 00f75ad0
// ==========================================================================================

void main_Anim___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: main_Anim___cctor
// Address: 00f75ad8
// ==========================================================================================

void main_Anim___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  long lVar5;
  long lVar6;
  
  puVar3 = PTR_main_Anim_TypeInfo_01fc0c58;
  puVar2 = PTR_int_____TypeInfo_01fbf5e8;
  puVar1 = PTR_int___TypeInfo_01fbf560;
  if ((DAT_020ff7f6 & 1) == 0) {
    FUN_00db0bbc(PTR_main_Anim_TypeInfo_01fc0c58);
    FUN_00db0bbc(PTR_int_____TypeInfo_01fbf5e8);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    DAT_020ff7f6 = 1;
  }
  **(undefined8 **)(*(long *)puVar3 + 0xb8) = 0;
  lVar5 = *(long *)(*(long *)puVar3 + 0xb8);
  *(undefined8 *)(lVar5 + 0x30) = 0;
  *(undefined8 *)(lVar5 + 0x28) = 0;
  *(undefined8 *)(lVar5 + 0x20) = 0;
  *(undefined8 *)(lVar5 + 0x18) = 0;
  *(undefined8 *)(lVar5 + 0x10) = 0;
  *(undefined8 *)(lVar5 + 8) = 0;
  lVar5 = FUN_00db0c30(*(undefined8 *)puVar2,0x18);
  uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
  if (lVar5 != 0) {
    if (*(int *)(lVar5 + 0x18) != 0) {
      *(undefined8 *)(lVar5 + 0x20) = uVar4;
      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
      if (1 < *(uint *)(lVar5 + 0x18)) {
        *(undefined8 *)(lVar5 + 0x28) = uVar4;
        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
        if (2 < *(uint *)(lVar5 + 0x18)) {
          *(undefined8 *)(lVar5 + 0x30) = uVar4;
          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
          if (3 < *(uint *)(lVar5 + 0x18)) {
            *(undefined8 *)(lVar5 + 0x38) = uVar4;
            uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
            if (4 < *(uint *)(lVar5 + 0x18)) {
              *(undefined8 *)(lVar5 + 0x40) = uVar4;
              uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
              if (5 < *(uint *)(lVar5 + 0x18)) {
                *(undefined8 *)(lVar5 + 0x48) = uVar4;
                uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                if (6 < *(uint *)(lVar5 + 0x18)) {
                  *(undefined8 *)(lVar5 + 0x50) = uVar4;
                  uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                  if (7 < *(uint *)(lVar5 + 0x18)) {
                    *(undefined8 *)(lVar5 + 0x58) = uVar4;
                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                    if (8 < *(uint *)(lVar5 + 0x18)) {
                      *(undefined8 *)(lVar5 + 0x60) = uVar4;
                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                      if (9 < *(uint *)(lVar5 + 0x18)) {
                        *(undefined8 *)(lVar5 + 0x68) = uVar4;
                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                        if (10 < *(uint *)(lVar5 + 0x18)) {
                          *(undefined8 *)(lVar5 + 0x70) = uVar4;
                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                          if (0xb < *(uint *)(lVar5 + 0x18)) {
                            *(undefined8 *)(lVar5 + 0x78) = uVar4;
                            uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                            if (0xc < *(uint *)(lVar5 + 0x18)) {
                              *(undefined8 *)(lVar5 + 0x80) = uVar4;
                              uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                              if (0xd < *(uint *)(lVar5 + 0x18)) {
                                *(undefined8 *)(lVar5 + 0x88) = uVar4;
                                uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                if (0xe < *(uint *)(lVar5 + 0x18)) {
                                  *(undefined8 *)(lVar5 + 0x90) = uVar4;
                                  uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                  if (0xf < *(uint *)(lVar5 + 0x18)) {
                                    *(undefined8 *)(lVar5 + 0x98) = uVar4;
                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                    if (0x10 < *(uint *)(lVar5 + 0x18)) {
                                      *(undefined8 *)(lVar5 + 0xa0) = uVar4;
                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                      if (0x11 < *(uint *)(lVar5 + 0x18)) {
                                        *(undefined8 *)(lVar5 + 0xa8) = uVar4;
                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                        if (0x12 < *(uint *)(lVar5 + 0x18)) {
                                          *(undefined8 *)(lVar5 + 0xb0) = uVar4;
                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                          if (0x13 < *(uint *)(lVar5 + 0x18)) {
                                            *(undefined8 *)(lVar5 + 0xb8) = uVar4;
                                            uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                            if (0x14 < *(uint *)(lVar5 + 0x18)) {
                                              *(undefined8 *)(lVar5 + 0xc0) = uVar4;
                                              uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                              if (0x15 < *(uint *)(lVar5 + 0x18)) {
                                                *(undefined8 *)(lVar5 + 200) = uVar4;
                                                uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                                if (0x16 < *(uint *)(lVar5 + 0x18)) {
                                                  *(undefined8 *)(lVar5 + 0xd0) = uVar4;
                                                  uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40);
                                                  if (0x17 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0xd8) = uVar4;
                                                    *(long *)(*(long *)(*(long *)puVar3 + 0xb8) +
                                                             0x38) = lVar5;
                                                    lVar5 = FUN_00db0c30(*(undefined8 *)puVar2,0x60)
                                                    ;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (lVar5 == 0) goto LAB_00f769c4;
                                                    if (*(int *)(lVar5 + 0x18) != 0) {
                                                      *(undefined8 *)(lVar5 + 0x20) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (1 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x28) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (2 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x30) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (3 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x38) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (4 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x40) = uVar4;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (5 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x48) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (6 < *(uint *)(lVar5 + 0x18)) {
                                                                  *(undefined8 *)(lVar5 + 0x50) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (7 < *(uint *)(lVar5 + 0x18)) {
                                                                    *(undefined8 *)(lVar5 + 0x58) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (8 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x60) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (9 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x68) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (10 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x70) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0xb < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x78) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0xc < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x80) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0xd < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x88) = uVar4;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0xe < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x90) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0xf < *(uint *)(lVar5 + 0x18)) {
                                                                  *(undefined8 *)(lVar5 + 0x98) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x10 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0xa0) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x11 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0xa8) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x12 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0xb0) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x13 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0xb8) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x14 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0xc0) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x15 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 200) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x16 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0xd0) = uVar4;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x17 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0xd8) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x18 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0xe0) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x19 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0xe8) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x1a < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0xf0) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x1b < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0xf8) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x1c < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x100) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x1d < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x108) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x1e < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x110) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x1f < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x118) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x20 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x120) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x21 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x128) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x22 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x130) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x23 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x138) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x24 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x140) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x25 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x148) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x26 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x150) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x27 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x158) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x28 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x160) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x29 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x168) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x2a < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x170) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x2b < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x178) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x2c < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x180) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x2d < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x188) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x2e < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 400) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x2f < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x198) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x30 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x1a0) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x31 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x1a8) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x32 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x1b0) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x33 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x1b8) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x34 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x1c0) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x35 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x1c8) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x36 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x1d0) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x37 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x1d8) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x38 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x1e0) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x39 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x1e8) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x3a < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x1f0) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x3b < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x1f8) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x3c < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x200) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x3d < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x208) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x3e < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x210) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x3f < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x218) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x40 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x220) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x41 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x228) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x42 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x230) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x43 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x238) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x44 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x240) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x45 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x248) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x46 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x250) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x47 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 600) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x48 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x260) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x49 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x268) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x4a < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x270) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x4b < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x278) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x4c < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x280) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x4d < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x288) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x4e < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x290) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x4f < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x298) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x50 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x2a0) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x51 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x2a8) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x52 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x2b0) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x53 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x2b8) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x54 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x2c0) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x55 < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x2c8) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x56 < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x2d0) =
                                                                     uVar4;
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,0x40);
                                                                if (0x57 < *(uint *)(lVar5 + 0x18))
                                                                {
                                                                  *(undefined8 *)(lVar5 + 0x2d8) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,
                                                                                       0x40);
                                                                  if (0x58 < *(uint *)(lVar5 + 0x18)
                                                                     ) {
                                                                    *(undefined8 *)(lVar5 + 0x2e0) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,0x40);
                                                  if (0x59 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x2e8) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x40)
                                                    ;
                                                    if (0x5a < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x2f0) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                           0x40);
                                                      if (0x5b < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x2f8) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,
                                                                             0x40);
                                                        if (0x5c < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x300) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,0x40);
                                                          if (0x5d < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x308) = uVar4;
                                                            uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                  puVar1,0x40);
                                                            if (0x5e < *(uint *)(lVar5 + 0x18)) {
                                                              *(undefined8 *)(lVar5 + 0x310) = uVar4
                                                              ;
                                                              uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                    puVar1,0x40);
                                                              if (0x5f < *(uint *)(lVar5 + 0x18)) {
                                                                *(undefined8 *)(lVar5 + 0x318) =
                                                                     uVar4;
                                                                lVar6 = *(long *)(*(long *)puVar3 +
                                                                                 0xb8);
                                                                *(long *)(lVar6 + 0x40) = lVar5;
                                                                *(undefined8 *)(lVar6 + 0x50) = 0;
                                                                *(undefined8 *)(lVar6 + 0x48) = 0;
                                                                *(undefined8 *)(lVar6 + 0x60) = 0;
                                                                *(undefined8 *)(lVar6 + 0x58) = 0;
                                                                *(undefined8 *)(lVar6 + 0x70) = 0;
                                                                *(undefined8 *)(lVar6 + 0x68) = 0;
                                                                lVar5 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar2,7);
                                                                uVar4 = FUN_00db0c30(*(undefined8 *)
                                                                                      puVar1,2);
                                                                if (lVar5 == 0) goto LAB_00f769c4;
                                                                if (*(int *)(lVar5 + 0x18) != 0) {
                                                                  *(undefined8 *)(lVar5 + 0x20) =
                                                                       uVar4;
                                                                  uVar4 = FUN_00db0c30(*(undefined8
                                                                                         *)puVar1,2)
                                                                  ;
                                                                  if (1 < *(uint *)(lVar5 + 0x18)) {
                                                                    *(undefined8 *)(lVar5 + 0x28) =
                                                                         uVar4;
                                                                    uVar4 = FUN_00db0c30(*(
                                                  undefined8 *)puVar1,2);
                                                  if (2 < *(uint *)(lVar5 + 0x18)) {
                                                    *(undefined8 *)(lVar5 + 0x30) = uVar4;
                                                    uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,2);
                                                    if (3 < *(uint *)(lVar5 + 0x18)) {
                                                      *(undefined8 *)(lVar5 + 0x38) = uVar4;
                                                      uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,2);
                                                      if (4 < *(uint *)(lVar5 + 0x18)) {
                                                        *(undefined8 *)(lVar5 + 0x40) = uVar4;
                                                        uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,2
                                                                            );
                                                        if (5 < *(uint *)(lVar5 + 0x18)) {
                                                          *(undefined8 *)(lVar5 + 0x48) = uVar4;
                                                          uVar4 = FUN_00db0c30(*(undefined8 *)puVar1
                                                                               ,2);
                                                          if (6 < *(uint *)(lVar5 + 0x18)) {
                                                            *(undefined8 *)(lVar5 + 0x50) = uVar4;
                                                            lVar6 = *(long *)(*(long *)puVar3 + 0xb8
                                                                             );
                                                            *(long *)(lVar6 + 0x78) = lVar5;
                                                            *(undefined8 *)(lVar6 + 0x80) = 0;
                                                            *(undefined8 *)(lVar6 + 0x88) = 0;
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
LAB_00f769c4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData___ctor
// Address: 00f769c8
// ==========================================================================================

void main_AppData___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  
  puVar3 = PTR_int___TypeInfo_01fbf560;
  puVar1 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_020ff82e & 1) == 0) {
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_StringLiteral_10680_01fc3320);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff82e = 1;
  }
  puVar4 = PTR_StringLiteral_10680_01fc3320;
  puVar2 = PTR_StringLiteral_1_01fbf388;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,3);
  *(undefined8 *)(param_1 + 0x28) = uVar5;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,4);
  *(undefined8 *)(param_1 + 0x68) = uVar5;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,4);
  *(undefined8 *)(param_1 + 0xb0) = uVar5;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar3,2);
  *(undefined8 *)(param_1 + 0xb8) = uVar5;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = kairo_unity_util_Language__LT(*(undefined8 *)puVar4,*(undefined8 *)puVar2,0);
  *(undefined8 *)(param_1 + 0xf0) = uVar5;
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__Init
// Address: 00f76ab8
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f77014) */
/* WARNING: Removing unreachable block (ram,0x00f77090) */

void main_AppData__Init(long param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined4 uVar9;
  undefined8 uVar10;
  ulong uVar11;
  long lVar12;
  long lVar13;
  uint uVar14;
  
  puVar5 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if ((DAT_020ff7f8 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_io_AssetReader_TypeInfo_01fc3328);
    FUN_00db0bbc(PTR_form_BootForm_TypeInfo_01fc3330);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Encrypter_TypeInfo_01fc0770);
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_kairo_unity_ui_Image_TypeInfo_01fbf500);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_long___TypeInfo_01fbf5c8);
    FUN_00db0bbc(PTR_kairo_unity_io_Storage_TypeInfo_01fbf4f8);
    FUN_00db0bbc(PTR_form_TitleForm_TypeInfo_01fc3338);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3B214A177E16100682A5FD602B50F5737EE0B82E3E865455AE4114EA8684C6CC_01fc3340
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A8FAED6ABBF35C12A4B26E40F6FEB19D736D90045C83B9F9A31F638D323E6811_01fc3348
                );
    FUN_00db0bbc(PTR_StringLiteral_4051_01fc3350);
    FUN_00db0bbc(PTR_StringLiteral_8122_01fc3358);
    DAT_020ff7f8 = 1;
  }
  puVar4 = PTR_main_AppData_TypeInfo_01fbf278;
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar5 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  uVar10 = kairo_unity_ui_Canvas__GetInstance(0);
  lVar13 = *(long *)puVar4;
  if (*(int *)(lVar13 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar13);
    lVar13 = *(long *)puVar4;
  }
  *(undefined8 *)(*(long *)(lVar13 + 0xb8) + 8) = uVar10;
  puVar6 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar7 = PTR_StringLiteral_4051_01fc3350;
  uVar10 = kairo_common_cfg_Config__GetPlatform(0);
  *(undefined8 *)(param_1 + 0x58) = uVar10;
  if (*(int *)(*(long *)puVar6 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar10 = kairo_unity_ui_IApplication__GetProperty(*(undefined8 *)puVar7,0);
  kairo_common_cfg_Config__Init(uVar10,0);
  uVar10 = kairo_unity_ui_IApplication__GetProperty(*(undefined8 *)puVar7,0);
  kairo_common_cfg_Config__Init(uVar10,0);
                    /* try { // try from 00f76c7c to 00f76c83 has its CatchHandler @ 00f770e0 */
  uVar11 = kairo_unity_io_RecordStore__Setup(0);
  if ((uVar11 & 1) == 0) {
                    /* try { // try from 00f76c88 to 00f76c8f has its CatchHandler @ 00f770a8 */
    kairo_unity_io_RecordStore__CreateRecordStore(0);
  }
  lVar13 = *(long *)puVar4;
  if (*(int *)(lVar13 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar13 = *(long *)puVar4;
  }
  puVar4 = PTR_kairo_unity_io_Storage_TypeInfo_01fbf4f8;
  lVar13 = *(long *)(*(long *)(lVar13 + 0xb8) + 0x20);
  if (lVar13 == 0) {
LAB_00f7708c:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(uint *)(lVar13 + 0x18) < 2) {
LAB_00f77088:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
  uVar10 = *(undefined8 *)(lVar13 + 0x28);
  if (DAT_020ff87d == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_io_RecordStore_TypeInfo_01fc3360);
    DAT_020ff87d = '\x01';
  }
  *(undefined8 *)
   (*(long *)(*(long *)PTR_kairo_unity_io_RecordStore_TypeInfo_01fc3360 + 0xb8) + 0x10) = uVar10;
  puVar8 = PTR_StringLiteral_8122_01fc3358;
  puVar7 = 
  PTR_Field__PrivateImplementationDetails__A8FAED6ABBF35C12A4B26E40F6FEB19D736D90045C83B9F9A31F638D323E6811_01fc3348
  ;
  puVar6 = PTR_int___TypeInfo_01fbf560;
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_io_Storage__Setup(2,8,*(undefined8 *)puVar8,0);
  lVar13 = FUN_00db0c30(*(undefined8 *)puVar6,4);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (lVar13,*(undefined8 *)puVar7,0);
  if ((lVar13 == 0) ||
     (lVar12 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,*(int *)(lVar13 + 0x18) << 2
                           ), lVar12 == 0)) goto LAB_00f7708c;
  uVar2 = *(uint *)(lVar12 + 0x18);
  if (0 < (long)((ulong)uVar2 << 0x20)) {
    uVar14 = 0;
    uVar11 = 0;
    do {
      uVar3 = (uint)(uVar11 >> 2) & 0x3fffffff;
      if ((*(uint *)(lVar13 + 0x18) <= uVar3) || (uVar2 <= uVar11)) goto LAB_00f77088;
      uVar1 = uVar14 & 0x18;
      uVar14 = uVar14 + 8;
      *(char *)(lVar12 + 0x20 + uVar11) =
           (char)(*(int *)(lVar13 + (ulong)uVar3 * 4 + 0x20) >> uVar1);
      uVar11 = uVar11 + 1;
    } while ((long)uVar11 < (long)(int)uVar2);
  }
  if (*(int *)(*(long *)PTR_kairo_unity_util_Encrypter_TypeInfo_01fc0770 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_util_Encrypter__SetEncryptionKey(lVar12,0);
  lVar13 = *(long *)puVar5;
  if (*(int *)(lVar13 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar13 = *(long *)puVar5;
  }
  puVar4 = PTR_kairo_unity_io_AssetReader_TypeInfo_01fc3328;
  lVar12 = *(long *)(lVar13 + 0xb8);
  if (*(char *)(lVar12 + 0x10) != '\0') {
    if (*(int *)(lVar13 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar12 = *(long *)(*(long *)puVar5 + 0xb8);
    }
    if (*(char *)(lVar12 + 0x11) == '\0') {
      if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar10 = 0;
      goto LAB_00f76e90;
    }
  }
  puVar5 = 
  PTR_Field__PrivateImplementationDetails__3B214A177E16100682A5FD602B50F5737EE0B82E3E865455AE4114EA8684C6CC_01fc3340
  ;
  uVar10 = FUN_00db0c30(*(undefined8 *)PTR_long___TypeInfo_01fbf5c8,10);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar10,*(undefined8 *)puVar5,0);
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
LAB_00f76e90:
  kairo_unity_io_AssetReader__SetSecurity(uVar10,1,0);
  surface_SurfaceManager__Setup();
                    /* try { // try from 00f76ea4 to 00f76eab has its CatchHandler @ 00f770dc */
  uVar11 = kairo_unity_io_RecordStore__Setup(0);
  if ((uVar11 & 1) == 0) {
                    /* try { // try from 00f76eb0 to 00f76ec3 has its CatchHandler @ 00f77174 */
    kairo_unity_io_RecordStore__CreateRecordStore(0);
  }
  kairo_unity_io_RecordStore__SetPreferenceMode(1,0);
  if (*(int *)(*(long *)PTR_kairo_unity_ui_Image_TypeInfo_01fbf500 + 0xe0) == 0) {
                    /* try { // try from 00f76ed8 to 00f76edb has its CatchHandler @ 00f770a4 */
    thunk_FUN_00df405c();
  }
                    /* try { // try from 00f76edc to 00f76ef3 has its CatchHandler @ 00f770cc */
  lVar13 = kairo_unity_ui_Image__CreateImage(4,4,3,0xffffffff,0);
  if (lVar13 != 0) {
                    /* try { // try from 00f76efc to 00f76f07 has its CatchHandler @ 00f770bc */
    lVar12 = kairo_unity_ui_Image__GetGraphics(lVar13,0);
    if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
                    /* try { // try from 00f76f20 to 00f76f23 has its CatchHandler @ 00f770a0 */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00f76f24 to 00f76f4b has its CatchHandler @ 00f77238 */
    uVar11 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,0,0);
    if (lVar12 != 0) {
      kairo_unity_ui_Graphics__SetColor(lVar12,uVar11 & 0xffffffff,0);
                    /* try { // try from 00f76f4c to 00f76f67 has its CatchHandler @ 00f770b8 */
      kairo_unity_ui_Graphics__FillRect(0,0,0x40800000,0x40800000,lVar12,0);
                    /* try { // try from 00f76f68 to 00f76f7f has its CatchHandler @ 00f770b4 */
      kairo_unity_ui_Graphics__SetRenderMode(lVar12,1,0x80,0x80,0);
                    /* try { // try from 00f76f80 to 00f76fa3 has its CatchHandler @ 00f77234 */
      uVar9 = kairo_unity_ui_Graphics__GetColorOfRGB(0xff,0xff,0xff,0);
      kairo_unity_ui_Graphics__SetColor(lVar12,uVar9,0);
                    /* try { // try from 00f76fa4 to 00f76fbf has its CatchHandler @ 00f770b0 */
      kairo_unity_ui_Graphics__FillRect(0,0,0x40800000,0x40800000,lVar12,0);
                    /* try { // try from 00f76fc0 to 00f76fd7 has its CatchHandler @ 00f770ac */
      kairo_unity_ui_Graphics__SetRenderMode(lVar12,0,0xff,0,0);
      *(undefined *)(param_1 + 0x60) = 0;
      kairo_unity_ui_Graphics__Dispose(lVar12,0,0);
      if (lVar13 != 0) {
        kairo_unity_ui_Image__Dispose(lVar13,0);
      }
      puVar4 = PTR_form_TitleForm_TypeInfo_01fc3338;
      puVar5 = PTR_form_GameForm_TypeInfo_01fbfab0;
      uVar10 = thunk_FUN_00e11c14(*(undefined8 *)PTR_form_BootForm_TypeInfo_01fc3330);
      form_BootForm___ctor();
      *(undefined8 *)(param_1 + 0x10) = uVar10;
      uVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
      form_TitleForm___ctor(uVar10,0);
      *(undefined8 *)(param_1 + 0x18) = uVar10;
      uVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar5);
      form_GameForm___ctor(uVar10,0);
      *(undefined8 *)(param_1 + 0x20) = uVar10;
      return;
    }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7709c to 00f7709f has its CatchHandler @ 00f77238 */
    FUN_00db0de4(uVar11,uVar11 & 0xffffffff);
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f77098 to 00f7709b has its CatchHandler @ 00f770c8 */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetCgiUrl
// Address: 00f77304
// ==========================================================================================

void main_AppData__GetCgiUrl(undefined8 param_1,uint param_2)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7f9 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff7f9 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar3 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x48);
  if (lVar3 != 0) {
    if (param_2 < *(uint *)(lVar3 + 0x18)) {
      System_String__Concat
                (*(undefined8 *)(*(long *)(lVar2 + 0xb8) + 0x38),
                 *(undefined8 *)(lVar3 + (long)(int)param_2 * 8 + 0x20),0);
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__PhpDlFile
// Address: 00f77388
// ==========================================================================================

void main_AppData__PhpDlFile(undefined8 param_1,long param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7fa & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_StringLiteral_816_01fc3368);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    DAT_020ff7fa = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  puVar2 = PTR_StringLiteral_816_01fc3368;
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  uVar4 = *(undefined8 *)(*(long *)(lVar3 + 0xb8) + 0x40);
  if (param_2 != 0) {
    uVar4 = System_String__Concat(uVar4,param_2,*(undefined8 *)PTR_StringLiteral_838_01fbf908,0);
  }
  uVar4 = System_String__Concat(uVar4,param_3,*(undefined8 *)puVar2,0);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar4,0,0,1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiRegist
// Address: 00f7747c
// ==========================================================================================

void main_AppData__CgiRegist(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff7fb & 1) == 0) {
    param_1 = FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    DAT_020ff7fb = 1;
  }
  uVar2 = main_AppData__CgiRegistURL(param_1,param_2,param_3);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar2,0,1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiRegistURL
// Address: 00f774fc
// ==========================================================================================

void main_AppData__CgiRegistURL(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7fc & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_382_01fc3378);
    DAT_020ff7fc = 1;
  }
  puVar3 = PTR_StringLiteral_382_01fc3378;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar4 = main_AppData__MakeQuery(*(undefined8 *)puVar3,param_2);
  uVar5 = main_AppData__MakeQuery(*(undefined8 *)puVar2,param_3);
  uVar6 = main_AppData__GetCgiUrl(uVar5,0);
  System_String__Concat(uVar6,uVar4,uVar5,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__MakeQuery
// Address: 00f775b8
// ==========================================================================================

undefined8 main_AppData__MakeQuery(undefined8 param_1,long param_2)

{
  undefined8 uVar1;
  
  if ((DAT_020ff803 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff803 = 1;
  }
  if (param_2 != 0) {
    uVar1 = System_String__Concat(param_1,param_2,0);
    return uVar1;
  }
  return *(undefined8 *)PTR_StringLiteral_1_01fbf388;
}



// ==========================================================================================
// Function: main_AppData__CgiRegistScore
// Address: 00f7761c
// ==========================================================================================

void main_AppData__CgiRegistScore
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff7fd & 1) == 0) {
    param_1 = FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    DAT_020ff7fd = 1;
  }
  uVar2 = main_AppData__CgiRegistScoreURL(param_1,param_2,param_3,param_4);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar2,0,0,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiRegistScoreURL
// Address: 00f776a4
// ==========================================================================================

void main_AppData__CgiRegistScoreURL
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff7fe & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    FUN_00db0bbc(PTR_StringLiteral_417_01fc3388);
    DAT_020ff7fe = 1;
  }
  puVar4 = PTR_StringLiteral_417_01fc3388;
  puVar3 = PTR_StringLiteral_407_01fc3380;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = main_AppData__MakeQuery(*(undefined8 *)puVar3,param_2);
  uVar6 = main_AppData__MakeQuery(*(undefined8 *)puVar4,param_3);
  uVar7 = main_AppData__MakeQuery(*(undefined8 *)puVar2,param_4);
  uVar8 = main_AppData__GetCgiUrl(uVar7,2);
  System_String__Concat(uVar8,uVar5,uVar6,uVar7,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiGetScore
// Address: 00f77798
// ==========================================================================================

void main_AppData__CgiGetScore(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff7ff & 1) == 0) {
    param_1 = FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    DAT_020ff7ff = 1;
  }
  uVar2 = main_AppData__CgiGetScoreURL(param_1,param_2);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar2,0,0,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiGetScoreURL
// Address: 00f77808
// ==========================================================================================

void main_AppData__CgiGetScoreURL(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff800 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    DAT_020ff800 = 1;
  }
  puVar2 = PTR_StringLiteral_407_01fc3380;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = main_AppData__MakeQuery(*(undefined8 *)puVar2,param_2);
  uVar4 = main_AppData__GetCgiUrl(uVar3,3);
  System_String__Concat(uVar4,uVar3,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiRanking
// Address: 00f7788c
// ==========================================================================================

void main_AppData__CgiRanking
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff801 & 1) == 0) {
    param_1 = FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    DAT_020ff801 = 1;
  }
  uVar2 = main_AppData__CgiRankingURL(param_1,param_2,param_3,param_4);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar2,0,0,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__CgiRankingURL
// Address: 00f77914
// ==========================================================================================

void main_AppData__CgiRankingURL
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff802 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_409_01fc3390);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    DAT_020ff802 = 1;
  }
  puVar4 = PTR_StringLiteral_409_01fc3390;
  puVar3 = PTR_StringLiteral_407_01fc3380;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = main_AppData__MakeQuery(*(undefined8 *)puVar3,param_2);
  uVar6 = main_AppData__MakeQuery(*(undefined8 *)puVar2,param_3);
  uVar7 = main_AppData__MakeQuery(*(undefined8 *)puVar4,param_4);
  uVar8 = main_AppData__GetCgiUrl(uVar7,1);
  System_String__Concat(uVar8,uVar5,uVar6,uVar7,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__IsPushSoftLabel
// Address: 00f77a08
// ==========================================================================================

void main_AppData__IsPushSoftLabel(undefined8 param_1,undefined8 param_2)

{
  main_AppData__IsPushSoftLabel(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__IsPushSoftLabel
// Address: 00f77a10
// ==========================================================================================

undefined8 main_AppData__IsPushSoftLabel(undefined8 param_1,uint param_2,undefined4 param_3)

{
  undefined *puVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  long lVar5;
  long lVar6;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff804 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff804 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
  if (lVar2 != 0) {
    lVar2 = kairo_unity_ui_Canvas__GetSoftLabelL(lVar2,0);
    lVar5 = *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 8);
    if (lVar5 != 0) {
      lVar5 = kairo_unity_ui_Canvas__GetSoftLabelR(lVar5,0);
      lVar6 = *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x60);
      if (lVar6 != 0) {
        if (*(uint *)(lVar6 + 0x18) <= param_2) {
LAB_00f77c08:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        if (lVar2 != 0) {
          uVar3 = System_String__Equals
                            (lVar2,*(undefined8 *)(lVar6 + (long)(int)param_2 * 8 + 0x20),0);
          if ((uVar3 & 1) != 0) {
            lVar2 = *(long *)puVar1;
            if (*(int *)(lVar2 + 0xe0) == 0) {
              thunk_FUN_00df405c();
              lVar2 = *(long *)puVar1;
            }
            lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
            if (lVar2 == 0) goto LAB_00f77c04;
            uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x200000,0);
            if ((uVar3 & 1) != 0) {
              return 1;
            }
          }
          lVar2 = *(long *)puVar1;
          if (*(int *)(lVar2 + 0xe0) == 0) {
            thunk_FUN_00df405c();
            lVar2 = *(long *)puVar1;
          }
          lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
          if (lVar2 != 0) {
            uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,param_3,0);
            if ((uVar3 & 1) != 0) {
              return 1;
            }
            lVar2 = *(long *)puVar1;
            if (*(int *)(lVar2 + 0xe0) == 0) {
              thunk_FUN_00df405c();
              lVar2 = *(long *)puVar1;
            }
            lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x60);
            if (lVar2 != 0) {
              if (*(uint *)(lVar2 + 0x18) <= param_2) goto LAB_00f77c08;
              if (lVar5 != 0) {
                uVar3 = System_String__Equals
                                  (lVar5,*(undefined8 *)(lVar2 + (long)(int)param_2 * 8 + 0x20),0);
                if ((uVar3 & 1) != 0) {
                  lVar2 = *(long *)puVar1;
                  if (*(int *)(lVar2 + 0xe0) == 0) {
                    thunk_FUN_00df405c();
                    lVar2 = *(long *)puVar1;
                  }
                  lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
                  if (lVar2 == 0) goto LAB_00f77c04;
                  uVar3 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,0x400000,0);
                  if ((uVar3 & 1) != 0) {
                    return 1;
                  }
                }
                lVar2 = *(long *)puVar1;
                if (*(int *)(lVar2 + 0xe0) == 0) {
                  thunk_FUN_00df405c();
                  lVar2 = *(long *)puVar1;
                }
                lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
                if (lVar2 != 0) {
                  uVar4 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar2,param_3,0);
                  return uVar4;
                }
              }
            }
          }
        }
      }
    }
  }
LAB_00f77c04:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Clamp
// Address: 00f77c0c
// ==========================================================================================

int main_AppData__Clamp(int param_1,int param_2,int param_3)

{
  if (param_1 <= param_3) {
    param_3 = param_1;
  }
  if (param_2 <= param_3) {
    param_2 = param_3;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__Clamp
// Address: 00f77c20
// ==========================================================================================

float main_AppData__Clamp(float param_1,float param_2,float param_3)

{
  if (param_1 <= param_3) {
    param_3 = param_1;
  }
  if (param_2 <= param_3) {
    param_2 = param_3;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__Clamp
// Address: 00f77c34
// ==========================================================================================

long main_AppData__Clamp(long param_1,long param_2,long param_3)

{
  if (param_1 <= param_3) {
    param_3 = param_1;
  }
  if (param_2 <= param_3) {
    param_2 = param_3;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMin
// Address: 00f77c48
// ==========================================================================================

int main_AppData__ClampMin(int param_1,int param_2)

{
  if (param_2 <= param_1) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMin
// Address: 00f77c54
// ==========================================================================================

float main_AppData__ClampMin(float param_1,float param_2)

{
  if (param_2 <= param_1) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMax
// Address: 00f77c60
// ==========================================================================================

int main_AppData__ClampMax(int param_1,int param_2)

{
  if (param_1 <= param_2) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMax
// Address: 00f77c6c
// ==========================================================================================

float main_AppData__ClampMax(float param_1,float param_2)

{
  if (param_1 <= param_2) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMin
// Address: 00f77c78
// ==========================================================================================

long main_AppData__ClampMin(long param_1,long param_2)

{
  if (param_2 <= param_1) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__ClampMax
// Address: 00f77c84
// ==========================================================================================

long main_AppData__ClampMax(long param_1,long param_2)

{
  if (param_1 <= param_2) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__Max
// Address: 00f77c90
// ==========================================================================================

int main_AppData__Max(int param_1,int param_2)

{
  if (param_2 <= param_1) {
    param_2 = param_1;
  }
  return param_2;
}



// ==========================================================================================
// Function: main_AppData__Min
// Address: 00f77c9c
// ==========================================================================================

int main_AppData__Min(int param_1,int param_2)

{
  if (param_2 <= param_1) {
    param_1 = param_2;
  }
  return param_1;
}



// ==========================================================================================
// Function: main_AppData__InitSystemSaveData
// Address: 00f77ca8
// ==========================================================================================

void main_AppData__InitSystemSaveData(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff805 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    FUN_00db0bbc(PTR_StringLiteral_6708_01fc33a0);
    DAT_020ff805 = 1;
  }
  puVar3 = PTR_kairo_unity_util_Property_TypeInfo_01fc3398;
  puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar4 = *(long *)(lVar4 + 0xb8);
  uVar7 = *(undefined8 *)(lVar4 + 0x68);
  uVar8 = *(undefined8 *)(lVar4 + 0x70);
  uVar9 = *(undefined8 *)(lVar4 + 0x78);
  uVar10 = *(undefined8 *)(lVar4 + 0x80);
  uVar11 = *(undefined8 *)(lVar4 + 0x88);
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  kairo_unity_util_Property___ctor(uVar5,uVar7,uVar8,uVar9,uVar10,uVar11,0);
  *(undefined8 *)(param_1 + 0x48) = uVar5;
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  if (*(char *)(*(long *)(lVar4 + 0xb8) + 0xc1) != '\0') {
    if (*(long *)(param_1 + 0x58) == 0) {
LAB_00f77de4:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar6 = Method_System_String_StartsWith
                      (*(long *)(param_1 + 0x58),*(undefined8 *)PTR_StringLiteral_6708_01fc33a0,0);
    if ((uVar6 & 1) != 0) {
      if ((*(long *)(param_1 + 0x48) == 0) ||
         (lVar4 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar4 == 0)) goto LAB_00f77de4;
      if (*(uint *)(lVar4 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined4 *)(lVar4 + 0x30) = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: main_AppData__LoadSystem
// Address: 00f77dec
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f7820c) */

undefined8 main_AppData__LoadSystem(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  long *plVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined4 local_64;
  
  if ((DAT_020ff806 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    FUN_00db0bbc(PTR_StringLiteral_8287_01fc33a8);
    DAT_020ff806 = 1;
  }
  plVar9 = (long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  local_64 = 0;
                    /* try { // try from 00f77e68 to 00f77e73 has its CatchHandler @ 00f782b8 */
  lVar4 = kairo_unity_io_RecordStore__OpenRecordStore(0,0);
  if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f781fc to 00f781ff has its CatchHandler @ 00f782b4 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f77e7c to 00f77e87 has its CatchHandler @ 00f782ac */
  iVar3 = kairo_unity_io_RecordStore__GetNumRecords(lVar4,0);
  if (iVar3 == 0) {
    kairo_unity_io_RecordStore__CloseRecordStore(lVar4,0);
    uVar6 = 0;
  }
  else {
    lVar5 = *plVar9;
    if (*(int *)(lVar5 + 0xe0) == 0) {
                    /* try { // try from 00f77e98 to 00f77e9b has its CatchHandler @ 00f782a8 */
      thunk_FUN_00df405c();
      lVar5 = *plVar9;
    }
                    /* try { // try from 00f77eac to 00f77eb7 has its CatchHandler @ 00f78290 */
    if ((*(int *)(*(long *)(lVar5 + 0xb8) + 0x4c) == 0) &&
       (iVar3 = kairo_unity_io_RecordStore__GetNumRecords(lVar4,0), iVar3 == 3)) {
                    /* try { // try from 00f77ec0 to 00f77ecb has its CatchHandler @ 00f7827c */
      local_64 = kairo_unity_io_RecordStore__GetNumRecords(lVar4,0);
                    /* try { // try from 00f77ed0 to 00f77edf has its CatchHandler @ 00f78278 */
      uVar6 = System_Int32__ToString(&local_64,0);
      puVar1 = PTR_StringLiteral_8287_01fc33a8;
                    /* try { // try from 00f77eec to 00f77f0f has its CatchHandler @ 00f78280 */
      uVar6 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_8287_01fc33a8,uVar6,0);
      if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
                    /* try { // try from 00f77f10 to 00f77f1f has its CatchHandler @ 00f78274 */
      kairo_unity_util_Log__Info(uVar6,0,0);
                    /* try { // try from 00f77f20 to 00f77f2f has its CatchHandler @ 00f78270 */
      kairo_unity_io_RecordStore__AddRecord(lVar4,0x800,0);
                    /* try { // try from 00f77f30 to 00f77f3f has its CatchHandler @ 00f7826c */
      kairo_unity_io_RecordStore__AddRecord(lVar4,0x9ab0,0);
                    /* try { // try from 00f77f40 to 00f77f4f has its CatchHandler @ 00f78268 */
      kairo_unity_io_RecordStore__AddRecord(lVar4,0x9ab0,0);
                    /* try { // try from 00f77f50 to 00f77f5b has its CatchHandler @ 00f78264 */
      local_64 = kairo_unity_io_RecordStore__GetNumRecords(lVar4,0);
                    /* try { // try from 00f77f60 to 00f77f6f has its CatchHandler @ 00f78260 */
      uVar6 = System_Int32__ToString(&local_64,0);
                    /* try { // try from 00f77f74 to 00f77f7b has its CatchHandler @ 00f7825c */
      uVar6 = System_String__Concat(*(undefined8 *)puVar1,uVar6,0);
                    /* try { // try from 00f77f7c to 00f77f87 has its CatchHandler @ 00f78258 */
      kairo_unity_util_Log__Info(uVar6,0,0);
                    /* try { // try from 00f77f88 to 00f77f97 has its CatchHandler @ 00f78254 */
      uVar6 = Method_kairo_unity_io_RecordStore_ReadRecord(lVar4,0,0);
                    /* try { // try from 00f77f9c to 00f77faf has its CatchHandler @ 00f78250 */
      kairo_unity_io_RecordStore__WriteRecord(lVar4,3,uVar6,0);
                    /* try { // try from 00f77fb0 to 00f77fbf has its CatchHandler @ 00f7824c */
      uVar7 = Method_kairo_unity_io_RecordStore_ReadRecord(lVar4,1,0);
                    /* try { // try from 00f77fc4 to 00f77fd7 has its CatchHandler @ 00f78248 */
      kairo_unity_io_RecordStore__WriteRecord(lVar4,4,uVar7,0);
                    /* try { // try from 00f77fd8 to 00f77fe7 has its CatchHandler @ 00f78244 */
      uVar8 = Method_kairo_unity_io_RecordStore_ReadRecord(lVar4,2,0);
                    /* try { // try from 00f77fec to 00f78007 has its CatchHandler @ 00f7828c */
      kairo_unity_io_RecordStore__WriteRecord(lVar4,5,uVar8,0);
      main_AppData__InitSystemSaveData(param_1);
      lVar5 = *(long *)(param_1 + 0x48);
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78214 to 00f78217 has its CatchHandler @ 00f78240 */
        FUN_00db0de4();
      }
      lVar5 = *(long *)(lVar5 + 0x10);
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78218 to 00f7821f has its CatchHandler @ 00f7829c */
        FUN_00db0de4();
      }
      if (*(int *)(lVar5 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar5 + 0x20) = uVar6;
                    /* try { // try from 00f78028 to 00f7804b has its CatchHandler @ 00f7829c */
      main_AppData__SaveSystem(param_1);
      puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
      lVar5 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
      if (*(int *)(lVar5 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar5 = *(long *)puVar1;
      }
      puVar2 = PTR_kairo_unity_util_Property_TypeInfo_01fc3398;
      lVar5 = *(long *)(lVar5 + 0xb8);
      uVar13 = *(undefined8 *)(lVar5 + 0x90);
      uVar12 = *(undefined8 *)(lVar5 + 0x98);
      uVar11 = *(undefined8 *)(lVar5 + 0xa0);
      uVar10 = *(undefined8 *)(lVar5 + 0xa8);
      uVar6 = *(undefined8 *)(lVar5 + 0xb0);
                    /* try { // try from 00f78070 to 00f78093 has its CatchHandler @ 00f78288 */
      lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
      kairo_unity_util_Property___ctor(lVar5,uVar13,uVar12,uVar11,uVar10,uVar6,0);
      *(long *)(param_1 + 0x50) = lVar5;
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78220 to 00f78223 has its CatchHandler @ 00f7823c */
        FUN_00db0de4();
      }
      lVar5 = *(long *)(lVar5 + 0x10);
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78224 to 00f7822b has its CatchHandler @ 00f78298 */
        FUN_00db0de4();
      }
      if (*(int *)(lVar5 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar5 + 0x20) = uVar7;
                    /* try { // try from 00f780b4 to 00f780bf has its CatchHandler @ 00f78298 */
      main_AppData__SaveGame(param_1,0);
      lVar5 = *(long *)(*(long *)puVar1 + 0xb8);
      uVar6 = *(undefined8 *)(lVar5 + 0x90);
      uVar7 = *(undefined8 *)(lVar5 + 0x98);
      uVar10 = *(undefined8 *)(lVar5 + 0xa0);
      uVar11 = *(undefined8 *)(lVar5 + 0xa8);
      uVar12 = *(undefined8 *)(lVar5 + 0xb0);
                    /* try { // try from 00f780d8 to 00f780fb has its CatchHandler @ 00f78284 */
      lVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      kairo_unity_util_Property___ctor(lVar5,uVar6,uVar7,uVar10,uVar11,uVar12,0);
      *(long *)(param_1 + 0x50) = lVar5;
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7822c to 00f7822f has its CatchHandler @ 00f78238 */
        FUN_00db0de4();
      }
      lVar5 = *(long *)(lVar5 + 0x10);
      if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78230 to 00f78237 has its CatchHandler @ 00f78294 */
        FUN_00db0de4();
      }
      if (*(int *)(lVar5 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar5 + 0x20) = uVar8;
                    /* try { // try from 00f7811c to 00f78127 has its CatchHandler @ 00f78294 */
      main_AppData__SaveGame(param_1,1);
      *(long *)(param_1 + 0x48) = 0;
      *(undefined8 *)(param_1 + 0x50) = 0;
      plVar9 = (long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
    }
                    /* try { // try from 00f78134 to 00f7813f has its CatchHandler @ 00f782a4 */
    kairo_unity_io_RecordStore__CloseRecordStore(lVar4,0);
                    /* try { // try from 00f78140 to 00f7814b has its CatchHandler @ 00f782a8 */
    main_AppData__InitSystemSaveData(param_1);
                    /* try { // try from 00f7814c to 00f7815f has its CatchHandler @ 00f782a0 */
    uVar6 = kairo_unity_io_RecordStore__ReadRecord(0,0,0);
    if (*(long *)(param_1 + 0x48) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78204 to 00f78207 has its CatchHandler @ 00f782bc */
      FUN_00db0de4(0,uVar6);
    }
                    /* try { // try from 00f78168 to 00f7816f has its CatchHandler @ 00f782bc */
    kairo_unity_util_Property__Load(*(long *)(param_1 + 0x48),uVar6,0);
    lVar4 = *plVar9;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *plVar9;
    }
    if (*(char *)(*(long *)(lVar4 + 0xb8) + 0xc1) != '\0') {
      if ((*(long *)(param_1 + 0x48) == 0) ||
         (lVar4 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar4 == 0)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      if (*(uint *)(lVar4 + 0x18) < 5) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined4 *)(lVar4 + 0x30) = 0;
    }
    uVar6 = 1;
  }
  return uVar6;
}



// ==========================================================================================
// Function: main_AppData__SaveSystem
// Address: 00f78328
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f78390) */

void main_AppData__SaveSystem(long param_1)

{
  long lVar1;
  long *plVar2;
  undefined8 uVar3;
  
                    /* try { // try from 00f78334 to 00f7833f has its CatchHandler @ 00f783a4 */
  lVar1 = kairo_unity_io_RecordStore__OpenRecordStore(0,0);
  plVar2 = *(long **)(param_1 + 0x48);
  if (plVar2 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78398 to 00f7839b has its CatchHandler @ 00f783a0 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f78354 to 00f78373 has its CatchHandler @ 00f783b0 */
  uVar3 = (**(code **)(*plVar2 + 0x178))(plVar2,*(undefined8 *)(*plVar2 + 0x180));
  if (lVar1 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7839c to 00f7839f has its CatchHandler @ 00f783b0 */
    FUN_00db0de4();
  }
  kairo_unity_io_RecordStore__WriteRecord(lVar1,0,uVar3,0);
  kairo_unity_io_RecordStore__CloseRecordStore(lVar1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__SaveGame
// Address: 00f78408
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f786d4) */

void main_AppData__SaveGame(long param_1,ulong param_2)

{
  int iVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  undefined8 uVar5;
  long *plVar6;
  int iVar7;
  undefined8 local_28;
  
  if ((DAT_020ff808 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_6935_01fc33b0);
    FUN_00db0bbc(PTR_StringLiteral_8943_01fc33b8);
    FUN_00db0bbc(PTR_StringLiteral_8123_01fc33c0);
    FUN_00db0bbc(PTR_StringLiteral_787_01fbf9c0);
    DAT_020ff808 = 1;
  }
  local_28 = 0;
                    /* try { // try from 00f78494 to 00f7849f has its CatchHandler @ 00f78730 */
  lVar3 = kairo_unity_io_RecordStore__OpenRecordStore(0,0);
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  lVar4 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
  iVar7 = 1;
  if ((param_2 & 1) != 0) {
    iVar7 = 2;
  }
  if (*(int *)(lVar4 + 0xe0) == 0) {
                    /* try { // try from 00f784c4 to 00f784c7 has its CatchHandler @ 00f7870c */
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  plVar6 = *(long **)(param_1 + 0x50);
  if (plVar6 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786dc to 00f786df has its CatchHandler @ 00f7872c */
    FUN_00db0de4();
  }
  iVar1 = *(int *)(*(long *)(lVar4 + 0xb8) + 200);
                    /* try { // try from 00f784e4 to 00f78523 has its CatchHandler @ 00f78750 */
  uVar5 = (**(code **)(*plVar6 + 0x178))(plVar6,*(undefined8 *)(*plVar6 + 0x180));
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786e0 to 00f786e3 has its CatchHandler @ 00f78750 */
    FUN_00db0de4();
  }
  kairo_unity_io_RecordStore__WriteRecord(lVar3,iVar1 + iVar7,uVar5,0);
  main_AppData__SaveSystem(param_1);
  puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar4 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  if (*(char *)(*(long *)(lVar4 + 0xb8) + 0x17) != '\0') {
    plVar6 = *(long **)(param_1 + 0x50);
    if (plVar6 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786e4 to 00f786e7 has its CatchHandler @ 00f78724 */
      FUN_00db0de4();
    }
                    /* try { // try from 00f78544 to 00f78547 has its CatchHandler @ 00f7874c */
    lVar4 = (**(code **)(*plVar6 + 0x178))(plVar6,*(undefined8 *)(*plVar6 + 0x180));
    if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786e8 to 00f786eb has its CatchHandler @ 00f7874c */
      FUN_00db0de4();
    }
    local_28._4_4_ = (int)*(undefined8 *)(lVar4 + 0x18);
                    /* try { // try from 00f78560 to 00f78567 has its CatchHandler @ 00f78720 */
    lVar4 = FUN_00db0c30(*(undefined8 *)PTR_string___TypeInfo_01fbf2f8,7);
    if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786ec to 00f786f3 has its CatchHandler @ 00f78748 */
      FUN_00db0de4();
    }
    if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x20) = *(undefined8 *)PTR_StringLiteral_8943_01fc33b8;
                    /* try { // try from 00f78588 to 00f78593 has its CatchHandler @ 00f78744 */
    uVar5 = System_Int32__ToString((long)&local_28 + 4,0);
    if (*(uint *)(lVar4 + 0x18) < 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786f4 to 00f786f7 has its CatchHandler @ 00f78744 */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x28) = uVar5;
    if (*(uint *)(lVar4 + 0x18) == 2) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786f8 to 00f786fb has its CatchHandler @ 00f7871c */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x30) = *(undefined8 *)PTR_StringLiteral_6935_01fc33b0;
    local_28._0_4_ = local_28._4_4_ + 0x3ff;
    if (-1 < local_28._4_4_) {
      local_28._0_4_ = local_28._4_4_;
    }
    local_28._0_4_ = (int)local_28 >> 10;
                    /* try { // try from 00f785d4 to 00f785df has its CatchHandler @ 00f78740 */
    uVar5 = System_Int32__ToString(&local_28,0);
    if (*(uint *)(lVar4 + 0x18) < 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f786fc to 00f786ff has its CatchHandler @ 00f78740 */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x38) = uVar5;
    if (*(uint *)(lVar4 + 0x18) == 4) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78700 to 00f78703 has its CatchHandler @ 00f78718 */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x40) = *(undefined8 *)PTR_StringLiteral_787_01fbf9c0;
    iVar1 = (local_28._4_4_ % 0x400) * 100;
    iVar7 = iVar1 + 0x3ff;
    if (-1 < iVar1) {
      iVar7 = iVar1;
    }
    local_28 = CONCAT44(local_28._4_4_,iVar7 >> 10);
                    /* try { // try from 00f7863c to 00f78647 has its CatchHandler @ 00f7873c */
    uVar5 = System_Int32__ToString(&local_28,0);
    if (*(uint *)(lVar4 + 0x18) < 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78704 to 00f78707 has its CatchHandler @ 00f7873c */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x48) = uVar5;
    if (*(uint *)(lVar4 + 0x18) == 6) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78708 to 00f7870b has its CatchHandler @ 00f78714 */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar4 + 0x50) = *(undefined8 *)PTR_StringLiteral_8123_01fc33c0;
                    /* try { // try from 00f78670 to 00f78697 has its CatchHandler @ 00f78728 */
    uVar5 = Method_System_String_Concat(lVar4,0);
    if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00f7869c to 00f786ab has its CatchHandler @ 00f78710 */
    kairo_unity_util_Log__Info(uVar5,0,0);
  }
  kairo_unity_io_RecordStore__CloseRecordStore(lVar3,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__NewGame
// Address: 00f787a8
// ==========================================================================================

void main_AppData__NewGame(long param_1,undefined4 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff807 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    DAT_020ff807 = 1;
  }
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  *(undefined4 *)(*(long *)(lVar4 + 0xb8) + 200) = param_2;
  puVar2 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar4 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar4 != 0)) {
    if (*(uint *)(lVar4 + 0x18) < 0xb) goto LAB_00f789bc;
    *(undefined4 *)(lVar4 + 0x48) = param_2;
    if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (DAT_020ff602 == '\0') {
      FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
      DAT_020ff602 = '\x01';
    }
    lVar4 = *(long *)puVar2;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar4 = **(long **)(lVar4 + 0xb8);
    if (lVar4 != 0) {
      iVar3 = kairo_unity_ui_IApplication__GetWidth(lVar4,0);
      if ((iVar3 < 0x1e1) ||
         (iVar3 = kairo_unity_ui_IApplication__GetHeight(lVar4,0), iVar3 < 0x1e1)) {
        if ((*(long *)(param_1 + 0x48) == 0) ||
           (lVar4 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar4 == 0)) goto LAB_00f789b8;
        if (*(uint *)(lVar4 + 0x18) < 0xf) goto LAB_00f789bc;
        *(undefined4 *)(lVar4 + 0x58) = 1;
      }
      lVar4 = *(long *)puVar1;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      puVar2 = PTR_kairo_unity_util_Property_TypeInfo_01fc3398;
      if ((*(long *)(param_1 + 0x48) != 0) &&
         (lVar5 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar5 != 0)) {
        if (*(uint *)(lVar5 + 0x18) < 0xf) {
LAB_00f789bc:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 8);
        if (lVar4 != 0) {
          kairo_unity_ui_Canvas__SetLinearFilterEnable(lVar4,*(int *)(lVar5 + 0x58) == 1,0);
          main_AppData__SaveSystem(param_1);
          lVar4 = *(long *)(*(long *)puVar1 + 0xb8);
          uVar6 = *(undefined8 *)(lVar4 + 0x90);
          uVar7 = *(undefined8 *)(lVar4 + 0x98);
          uVar8 = *(undefined8 *)(lVar4 + 0xa0);
          uVar9 = *(undefined8 *)(lVar4 + 0xa8);
          uVar10 = *(undefined8 *)(lVar4 + 0xb0);
          lVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
          kairo_unity_util_Property___ctor(lVar4,uVar6,uVar7,uVar8,uVar9,uVar10,0);
          *(long *)(param_1 + 0x50) = lVar4;
          if ((lVar4 != 0) && (lVar4 = *(long *)(lVar4 + 0x30), lVar4 != 0)) {
            if (*(int *)(lVar4 + 0x18) != 0) {
              *(undefined8 *)(lVar4 + 0x20) = param_3;
              return;
            }
            goto LAB_00f789bc;
          }
        }
      }
    }
  }
LAB_00f789b8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SaveGame
// Address: 00f789c0
// ==========================================================================================

void main_AppData__SaveGame(undefined8 param_1)

{
  main_AppData__SaveGame(param_1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__LoadGame
// Address: 00f789c8
// ==========================================================================================

void main_AppData__LoadGame(undefined8 param_1,undefined8 param_2)

{
  main_AppData__LoadGame(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__LoadGame
// Address: 00f789d0
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f78b9c) */

void main_AppData__LoadGame(long param_1,undefined4 param_2,ulong param_3)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  undefined8 uVar4;
  int iVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff809 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    DAT_020ff809 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  *(undefined4 *)(*(long *)(lVar2 + 0xb8) + 200) = param_2;
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar2 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar2 != 0)) {
    if (*(uint *)(lVar2 + 0x18) < 0xb) {
LAB_00f78b98:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    *(undefined4 *)(lVar2 + 0x48) = param_2;
    main_AppData__SaveSystem(param_1);
                    /* try { // try from 00f78a6c to 00f78a77 has its CatchHandler @ 00f78bb0 */
    lVar2 = kairo_unity_io_RecordStore__OpenRecordStore(0,0);
    lVar3 = *(long *)puVar1;
    iVar5 = 1;
    if ((param_3 & 1) != 0) {
      iVar5 = 2;
    }
    if (*(int *)(lVar3 + 0xe0) == 0) {
                    /* try { // try from 00f78a94 to 00f78a97 has its CatchHandler @ 00f78ba8 */
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
                    /* try { // try from 00f78aa8 to 00f78ab3 has its CatchHandler @ 00f78bac */
    uVar4 = kairo_unity_io_RecordStore__ReadRecord
                      (0,*(int *)(*(long *)(lVar3 + 0xb8) + 200) + iVar5,0);
    lVar3 = *(long *)(*(long *)puVar1 + 0xb8);
    uVar6 = *(undefined8 *)(lVar3 + 0x90);
    uVar7 = *(undefined8 *)(lVar3 + 0x98);
    uVar8 = *(undefined8 *)(lVar3 + 0xa0);
    uVar9 = *(undefined8 *)(lVar3 + 0xa8);
    uVar10 = *(undefined8 *)(lVar3 + 0xb0);
                    /* try { // try from 00f78ad8 to 00f78afb has its CatchHandler @ 00f78bc0 */
    lVar3 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    kairo_unity_util_Property___ctor(lVar3,uVar6,uVar7,uVar8,uVar9,uVar10,0);
    *(long *)(param_1 + 0x50) = lVar3;
    if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78ba4 to 00f78ba7 has its CatchHandler @ 00f78bbc */
      FUN_00db0de4();
    }
                    /* try { // try from 00f78b08 to 00f78b17 has its CatchHandler @ 00f78bbc */
    kairo_unity_util_Property__Load(lVar3,uVar4,0);
    if (lVar2 != 0) {
      kairo_unity_io_RecordStore__CloseRecordStore(lVar2,0);
    }
    lVar2 = *(long *)puVar1;
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    if ((*(long *)(param_1 + 0x48) != 0) &&
       (lVar3 = *(long *)(*(long *)(param_1 + 0x48) + 0x20), lVar3 != 0)) {
      if (*(uint *)(lVar3 + 0x18) < 0xf) goto LAB_00f78b98;
      lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
      if (lVar2 != 0) {
        kairo_unity_ui_Canvas__SetLinearFilterEnable(lVar2,*(int *)(lVar3 + 0x58) == 1,0);
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__ResetAllSaveData
// Address: 00f78c14
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x00f78f08) */

void main_AppData__ResetAllSaveData(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  long lVar7;
  
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_020ff80a & 1) == 0) {
    FUN_00db0bbc(PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_java_io_DataOutputStream_TypeInfo_01fc1fd0);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_StringLiteral_10873_01fc33c8);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_4894_01fc33d0);
    DAT_020ff80a = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  lVar7 = *(long *)(lVar3 + 0xb8);
  if (*(char *)(lVar7 + 0x10) == '\0') {
    if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_util_Log__Info(*(undefined8 *)PTR_StringLiteral_10873_01fc33c8,0,0);
    return;
  }
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar7 = *(long *)(*(long *)puVar1 + 0xb8);
  }
  puVar2 = PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8;
  puVar1 = PTR_byte___TypeInfo_01fbf258;
  if (*(char *)(lVar7 + 0x17) != '\0') {
    if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_util_Log__Info(*(undefined8 *)PTR_StringLiteral_4894_01fc33d0,0,0);
  }
  uVar4 = FUN_00db0c30(*(undefined8 *)puVar1,0x800);
                    /* try { // try from 00f78d34 to 00f78d47 has its CatchHandler @ 00f78fcc */
  plVar5 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  java_io_ByteArrayOutputStream___ctor(plVar5,0);
                    /* try { // try from 00f78d54 to 00f78d67 has its CatchHandler @ 00f78fc4 */
  plVar6 = (long *)thunk_FUN_00e11c14(*(undefined8 *)PTR_java_io_DataOutputStream_TypeInfo_01fc1fd0)
  ;
  java_io_DataOutputStream___ctor(plVar6,plVar5,0);
  if (plVar6 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78f14 to 00f78f17 has its CatchHandler @ 00f78f58 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f78d6c to 00f78d7b has its CatchHandler @ 00f78f58 */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78d7c to 00f78d8b has its CatchHandler @ 00f78f50 */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78d8c to 00f78d9b has its CatchHandler @ 00f78f4c */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
  puVar1 = PTR_StringLiteral_1_01fbf388;
                    /* try { // try from 00f78da8 to 00f78db3 has its CatchHandler @ 00f78f48 */
  java_io_DataOutputStream__WriteUTF(plVar6,*(undefined8 *)PTR_StringLiteral_1_01fbf388,0);
                    /* try { // try from 00f78db4 to 00f78dc3 has its CatchHandler @ 00f78f44 */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78dc4 to 00f78dd3 has its CatchHandler @ 00f78f40 */
  java_io_DataOutputStream__WriteLong(plVar6,0,0);
                    /* try { // try from 00f78dd4 to 00f78de3 has its CatchHandler @ 00f78f3c */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78de8 to 00f78df3 has its CatchHandler @ 00f78f38 */
  java_io_DataOutputStream__WriteUTF(plVar6,*(undefined8 *)puVar1,0);
                    /* try { // try from 00f78df4 to 00f78e03 has its CatchHandler @ 00f78f34 */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78e04 to 00f78e13 has its CatchHandler @ 00f78f30 */
  java_io_DataOutputStream__WriteLong(plVar6,0,0);
                    /* try { // try from 00f78e14 to 00f78e23 has its CatchHandler @ 00f78f2c */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
                    /* try { // try from 00f78e24 to 00f78e33 has its CatchHandler @ 00f78f28 */
  java_io_DataOutputStream__WriteInt(plVar6,0,0);
  if (plVar5 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78f18 to 00f78f1b has its CatchHandler @ 00f78f24 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f78e38 to 00f78e43 has its CatchHandler @ 00f78f20 */
  lVar3 = java_io_ByteArrayOutputStream__ToByteArray(plVar5,0);
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f78f1c to 00f78f1f has its CatchHandler @ 00f78f54 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f78e4c to 00f78e5f has its CatchHandler @ 00f78f54 */
  java_lang_JSystem__Arraycopy(lVar3,0,uVar4,0,*(undefined4 *)(lVar3 + 0x18),0);
  if (plVar5 != (long *)0x0) {
    (**(code **)(*plVar5 + 0x188))(plVar5,*(undefined8 *)(*plVar5 + 400));
  }
  if (plVar6 != (long *)0x0) {
    (**(code **)(*plVar6 + 0x188))(plVar6,*(undefined8 *)(*plVar6 + 400));
  }
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar3 = *(long *)(*(long *)(param_1 + 0x48) + 0x10), lVar3 != 0)) {
    if (*(int *)(lVar3 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    *(undefined8 *)(lVar3 + 0x20) = uVar4;
    main_AppData__SaveSystem(param_1);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawWindow
// Address: 00f78fdc
// ==========================================================================================

void main_AppData__DrawWindow
               (long param_1,long param_2,int param_3,int param_4,int param_5,undefined8 param_6)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  undefined *puVar4;
  undefined4 uVar5;
  long lVar6;
  float fVar7;
  undefined auStack_78 [24];
  
  if ((DAT_020ff80b & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598);
    DAT_020ff80b = 1;
  }
  puVar4 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__SetColor(param_2,0x46,0x54,0x4f,0);
    iVar1 = param_3;
    if (param_3 < 0) {
      iVar1 = param_3 + 1;
    }
    iVar1 = iVar1 >> 1;
    iVar2 = param_4;
    if (param_4 < 0) {
      iVar2 = param_4 + 1;
    }
    param_5 = param_5 - (iVar2 >> 1);
    kairo_unity_ui_Graphics__FillRect
              ((float)(0x76 - iVar1),(float)(param_5 + 0x76),(float)(param_3 + 5),
               (float)(param_4 + 4),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xa0,0xb1,0xf0,0);
    kairo_unity_ui_Graphics__FillRect
              ((float)(0x77 - iVar1),(float)(param_5 + 0x77),(float)(param_3 + 2),
               (float)(param_4 + 1),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xf0,0xf2,0xfa,0);
    fVar7 = (float)(0x78 - iVar1);
    iVar2 = param_5 + 0x78;
    kairo_unity_ui_Graphics__FillRect
              (fVar7,(float)iVar2,(float)param_3,(float)(param_4 + -1),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0x92,0xad,0xd5,0);
    kairo_unity_ui_Graphics__FillRect
              (fVar7,(float)(param_5 + 0x88),(float)(param_3 + 1),0x3f800000,param_2,0);
    lVar6 = *(long *)(param_1 + 0x20);
    if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (lVar6 != 0) {
      form_GameForm__DrawImage
                (lVar6,param_2,*(undefined8 *)(*(long *)(*(long *)puVar4 + 0xb8) + 0x1140),
                 0x78 - iVar1,iVar2,0,0x34,param_3 + -2,0x10,0);
      if (0x77 < param_3 + -1) {
        lVar6 = *(long *)(param_1 + 0x20);
        if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        if (lVar6 == 0) goto LAB_00f792f4;
        form_GameForm__DrawImage
                  (lVar6,param_2,*(undefined8 *)(*(long *)(*(long *)puVar4 + 0xb8) + 0x1140),
                   0xf0 - iVar1,iVar2,0,0x34,param_3 + -0x78,0x10,0);
      }
      puVar4 = PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598;
      uVar3 = param_3 - 0x24;
      if ((int)uVar3 < 0x51) {
        uVar3 = 0x50;
      }
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar5 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,100,0);
      if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar4);
      }
      kairo_unity_ui_TextLayout__Draw
                (auStack_78,(float)(0x78 - (uVar3 >> 1)),(float)(param_5 + 0x7a),(float)uVar3,
                 0x41400000,param_2,param_6,uVar5,0,0x22,0,0);
      return;
    }
  }
LAB_00f792f4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawWindow
// Address: 00f78fe0
// ==========================================================================================

void main_AppData__DrawWindow
               (long param_1,long param_2,int param_3,int param_4,int param_5,undefined8 param_6)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  undefined *puVar4;
  undefined4 uVar5;
  long lVar6;
  float fVar7;
  undefined auStack_78 [24];
  
  if ((DAT_020ff80b & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598);
    DAT_020ff80b = 1;
  }
  puVar4 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__SetColor(param_2,0x46,0x54,0x4f,0);
    iVar1 = param_3;
    if (param_3 < 0) {
      iVar1 = param_3 + 1;
    }
    iVar1 = iVar1 >> 1;
    iVar2 = param_4;
    if (param_4 < 0) {
      iVar2 = param_4 + 1;
    }
    param_5 = param_5 - (iVar2 >> 1);
    kairo_unity_ui_Graphics__FillRect
              ((float)(0x76 - iVar1),(float)(param_5 + 0x76),(float)(param_3 + 5),
               (float)(param_4 + 4),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xa0,0xb1,0xf0,0);
    kairo_unity_ui_Graphics__FillRect
              ((float)(0x77 - iVar1),(float)(param_5 + 0x77),(float)(param_3 + 2),
               (float)(param_4 + 1),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xf0,0xf2,0xfa,0);
    fVar7 = (float)(0x78 - iVar1);
    iVar2 = param_5 + 0x78;
    kairo_unity_ui_Graphics__FillRect
              (fVar7,(float)iVar2,(float)param_3,(float)(param_4 + -1),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0x92,0xad,0xd5,0);
    kairo_unity_ui_Graphics__FillRect
              (fVar7,(float)(param_5 + 0x88),(float)(param_3 + 1),0x3f800000,param_2,0);
    lVar6 = *(long *)(param_1 + 0x20);
    if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (lVar6 != 0) {
      form_GameForm__DrawImage
                (lVar6,param_2,*(undefined8 *)(*(long *)(*(long *)puVar4 + 0xb8) + 0x1140),
                 0x78 - iVar1,iVar2,0,0x34,param_3 + -2,0x10,0);
      if (0x77 < param_3 + -1) {
        lVar6 = *(long *)(param_1 + 0x20);
        if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        if (lVar6 == 0) goto LAB_00f792f4;
        form_GameForm__DrawImage
                  (lVar6,param_2,*(undefined8 *)(*(long *)(*(long *)puVar4 + 0xb8) + 0x1140),
                   0xf0 - iVar1,iVar2,0,0x34,param_3 + -0x78,0x10,0);
      }
      puVar4 = PTR_kairo_unity_ui_TextLayout_TypeInfo_01fbf598;
      uVar3 = param_3 - 0x24;
      if ((int)uVar3 < 0x51) {
        uVar3 = 0x50;
      }
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar5 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,100,0);
      if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar4);
      }
      kairo_unity_ui_TextLayout__Draw
                (auStack_78,(float)(0x78 - (uVar3 >> 1)),(float)(param_5 + 0x7a),(float)uVar3,
                 0x41400000,param_2,param_6,uVar5,0,0x22,0,0);
      return;
    }
  }
LAB_00f792f4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawBox
// Address: 00f792f8
// ==========================================================================================

void main_AppData__DrawBox
               (long param_1,long param_2,int param_3,int param_4,int param_5,int param_6)

{
  undefined *puVar1;
  long lVar2;
  float fVar3;
  float fVar4;
  
  if ((DAT_020ff80c & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    DAT_020ff80c = 1;
  }
  puVar1 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__SetColor(param_2,0xff,0xff,0xff,0);
    fVar3 = (float)param_3;
    fVar4 = (float)param_4;
    kairo_unity_ui_Graphics__FillRect
              (fVar3,fVar4,(float)(param_5 - param_3),(float)(param_6 - param_4),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xca,0xd4,0xf4,0);
    kairo_unity_ui_Graphics__DrawRect
              ((float)(param_3 + 1),(float)(param_4 + 1),(float)((param_5 - param_3) + -3),
               (float)((param_6 - param_4) + -3),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xf0,0xf2,0xfa,0);
    kairo_unity_ui_Graphics__FillRect(fVar3,fVar4,0x40800000,0x40800000,param_2,0);
    param_5 = param_5 + -4;
    kairo_unity_ui_Graphics__FillRect((float)param_5,fVar4,0x40800000,0x40800000,param_2,0);
    param_6 = param_6 + -4;
    kairo_unity_ui_Graphics__FillRect((float)param_5,(float)param_6,0x40800000,0x40800000,param_2,0)
    ;
    kairo_unity_ui_Graphics__FillRect(fVar3,(float)param_6,0x40800000,0x40800000,param_2,0);
    lVar2 = *(long *)(param_1 + 0x20);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (lVar2 != 0) {
      form_GameForm__DrawImage
                (lVar2,param_2,*(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_3,
                 param_4,8,0,4,4,0);
      if (*(long *)(param_1 + 0x20) != 0) {
        form_GameForm__DrawImage
                  (*(long *)(param_1 + 0x20),param_2,
                   *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_5,param_4,0xc,0
                   ,4,4,0);
        if (*(long *)(param_1 + 0x20) != 0) {
          form_GameForm__DrawImage
                    (*(long *)(param_1 + 0x20),param_2,
                     *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_5,param_6,0xc
                     ,4,4,4,0);
          if (*(long *)(param_1 + 0x20) != 0) {
            form_GameForm__DrawImage
                      (*(long *)(param_1 + 0x20),param_2,
                       *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_3,param_6,8
                       ,4,4,4,0);
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
// Function: main_AppData__DrawBox
// Address: 00f792fc
// ==========================================================================================

void main_AppData__DrawBox
               (long param_1,long param_2,int param_3,int param_4,int param_5,int param_6)

{
  undefined *puVar1;
  long lVar2;
  float fVar3;
  float fVar4;
  
  if ((DAT_020ff80c & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    DAT_020ff80c = 1;
  }
  puVar1 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (param_2 != 0) {
    kairo_unity_ui_Graphics__SetColor(param_2,0xff,0xff,0xff,0);
    fVar3 = (float)param_3;
    fVar4 = (float)param_4;
    kairo_unity_ui_Graphics__FillRect
              (fVar3,fVar4,(float)(param_5 - param_3),(float)(param_6 - param_4),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xca,0xd4,0xf4,0);
    kairo_unity_ui_Graphics__DrawRect
              ((float)(param_3 + 1),(float)(param_4 + 1),(float)((param_5 - param_3) + -3),
               (float)((param_6 - param_4) + -3),param_2,0);
    kairo_unity_ui_Graphics__SetColor(param_2,0xf0,0xf2,0xfa,0);
    kairo_unity_ui_Graphics__FillRect(fVar3,fVar4,0x40800000,0x40800000,param_2,0);
    param_5 = param_5 + -4;
    kairo_unity_ui_Graphics__FillRect((float)param_5,fVar4,0x40800000,0x40800000,param_2,0);
    param_6 = param_6 + -4;
    kairo_unity_ui_Graphics__FillRect((float)param_5,(float)param_6,0x40800000,0x40800000,param_2,0)
    ;
    kairo_unity_ui_Graphics__FillRect(fVar3,(float)param_6,0x40800000,0x40800000,param_2,0);
    lVar2 = *(long *)(param_1 + 0x20);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    if (lVar2 != 0) {
      form_GameForm__DrawImage
                (lVar2,param_2,*(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_3,
                 param_4,8,0,4,4,0);
      if (*(long *)(param_1 + 0x20) != 0) {
        form_GameForm__DrawImage
                  (*(long *)(param_1 + 0x20),param_2,
                   *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_5,param_4,0xc,0
                   ,4,4,0);
        if (*(long *)(param_1 + 0x20) != 0) {
          form_GameForm__DrawImage
                    (*(long *)(param_1 + 0x20),param_2,
                     *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_5,param_6,0xc
                     ,4,4,4,0);
          if (*(long *)(param_1 + 0x20) != 0) {
            form_GameForm__DrawImage
                      (*(long *)(param_1 + 0x20),param_2,
                       *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x1140),param_3,param_6,8
                       ,4,4,4,0);
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
// Function: main_AppData__DrawArcRect
// Address: 00f795a4
// ==========================================================================================

void main_AppData__DrawArcRect
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  
  if (param_2 != 0) {
    param_6 = param_6 + param_4;
    fVar1 = (float)param_3;
    kairo_unity_ui_Graphics__DrawLine
              (fVar1,(float)(param_7 + param_4),fVar1,(float)(param_6 - param_7),0x3f800000,param_2,
               0);
    param_5 = param_5 + param_3;
    kairo_unity_ui_Graphics__DrawLine
              ((float)param_5,(float)(param_7 + param_4),(float)param_5,(float)(param_6 - param_7),
               0x3f800000,param_2,0);
    fVar2 = (float)param_4;
    kairo_unity_ui_Graphics__DrawLine
              ((float)(param_7 + param_3),fVar2,(float)(param_5 - param_7),fVar2,0x3f800000,param_2,
               0);
    kairo_unity_ui_Graphics__DrawLine
              ((float)(param_7 + param_3),(float)param_6,(float)(param_5 - param_7),(float)param_6,
               0x3f800000,param_2,0);
    fVar3 = (float)(param_7 << 1);
    kairo_unity_ui_Graphics__DrawArc
              (fVar1,fVar2,fVar3,fVar3,0x42b40000,0x42b40000,0x3f800000,param_2,0);
    fVar4 = (float)(param_6 + param_7 * -2);
    kairo_unity_ui_Graphics__DrawArc
              (fVar1,fVar4,fVar3,fVar3,0x43340000,0x42b40000,0x3f800000,param_2,0);
    fVar1 = (float)(param_5 + param_7 * -2);
    kairo_unity_ui_Graphics__DrawArc(fVar1,fVar2,fVar3,fVar3,0,0x42b40000,0x3f800000,param_2,0);
    kairo_unity_ui_Graphics__DrawArc
              (fVar1,fVar4,fVar3,fVar3,0x43870000,0x42b40000,0x3f800000,param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__FillArcRect
// Address: 00f79770
// ==========================================================================================

void main_AppData__FillArcRect
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  
  if (param_2 != 0) {
    fVar4 = (float)(param_7 + param_4);
    fVar1 = (float)param_3;
    fVar3 = (float)param_7;
    fVar5 = (float)(param_6 + param_7 * -2);
    kairo_unity_ui_Graphics__FillRect(fVar1,fVar4,fVar3,fVar5,param_2,0);
    kairo_unity_ui_Graphics__FillRect
              ((float)((param_5 + param_3) - param_7),fVar4,fVar3,fVar5,param_2,0);
    fVar2 = (float)param_4;
    fVar6 = (float)(param_7 + param_3);
    fVar7 = (float)(param_5 + param_7 * -2);
    kairo_unity_ui_Graphics__FillRect(fVar6,fVar2,fVar7,fVar3,param_2,0);
    kairo_unity_ui_Graphics__FillRect
              (fVar6,(float)((param_6 + param_4) - param_7),fVar7,fVar3,param_2,0);
    kairo_unity_ui_Graphics__FillRect(fVar6,fVar4,fVar7,fVar5,param_2,0);
    fVar3 = (float)(param_7 * 2);
    kairo_unity_ui_Graphics__FillArc(fVar1,fVar2,fVar3,fVar3,0x42b40000,0x42b40000,param_2,0);
    fVar4 = (float)(param_6 + param_4 + param_7 * -2);
    kairo_unity_ui_Graphics__FillArc(fVar1,fVar4,fVar3,fVar3,0x43340000,0x42b40000,param_2,0);
    fVar1 = (float)(param_5 + param_3 + param_7 * -2);
    kairo_unity_ui_Graphics__FillArc(fVar1,fVar2,fVar3,fVar3,0,0x42b40000,param_2,0);
    kairo_unity_ui_Graphics__FillArc(fVar1,fVar4,fVar3,fVar3,0x43870000,0x42b40000,param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawFillArcRect
// Address: 00f79958
// ==========================================================================================

void main_AppData__DrawFillArcRect
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               undefined4 param_7,undefined4 param_8,undefined4 param_9,undefined4 param_10,
               undefined4 param_11,undefined4 param_12,undefined4 param_13)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if ((DAT_020ff80d & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff80d = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(param_8,param_9,param_10,0);
  if (param_2 != 0) {
    uVar3 = kairo_unity_ui_Graphics__SetColor(param_2,uVar2,0);
    main_AppData__FillArcRect
              (uVar3,param_2,param_3 + 1,param_4 + 1,param_5 + -2,param_6 + -2,param_7);
    uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(param_11,param_12,param_13,0);
    uVar3 = kairo_unity_ui_Graphics__SetColor(param_2,uVar2,0);
    main_AppData__DrawArcRect(uVar3,param_2,param_3,param_4,param_5 + -1,param_6 + -1,param_7);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Draw3DBox
// Address: 00f79a84
// ==========================================================================================

void main_AppData__Draw3DBox
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               long param_7)

{
  undefined4 uVar1;
  uint uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  long lVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  if ((DAT_020ff80e & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff80e = 1;
  }
  if (param_7 != 0) {
    if (*(int *)(param_7 + 0x18) != 0) {
      lVar5 = *(long *)(param_7 + 0x20);
      if (lVar5 == 0) goto LAB_00f79d50;
      uVar2 = *(uint *)(lVar5 + 0x18);
      if (((uVar2 != 0) && (uVar2 != 1)) && (2 < uVar2)) {
        uVar4 = *(undefined4 *)(lVar5 + 0x20);
        uVar1 = *(undefined4 *)(lVar5 + 0x24);
        uVar3 = *(undefined4 *)(lVar5 + 0x28);
        if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar4 = kairo_unity_ui_Graphics__GetColorOfRGB(uVar4,uVar1,uVar3,0);
        if (param_2 == 0) goto LAB_00f79d50;
        kairo_unity_ui_Graphics__SetColor(param_2,uVar4,0);
        kairo_unity_ui_Graphics__DrawRect
                  ((float)param_3,(float)param_4,(float)(param_5 + -1),(float)(param_6 + -1),param_2
                   ,0);
        if (2 < *(uint *)(param_7 + 0x18)) {
          lVar5 = *(long *)(param_7 + 0x30);
          if (lVar5 == 0) goto LAB_00f79d50;
          uVar2 = *(uint *)(lVar5 + 0x18);
          if (((uVar2 != 0) && (uVar2 != 1)) && (2 < uVar2)) {
            uVar4 = kairo_unity_ui_Graphics__GetColorOfRGB
                              (*(undefined4 *)(lVar5 + 0x20),*(undefined4 *)(lVar5 + 0x24),
                               *(undefined4 *)(lVar5 + 0x28),0);
            kairo_unity_ui_Graphics__SetColor(param_2,uVar4,0);
            fVar9 = (float)(param_3 + 1);
            fVar8 = (float)(param_3 + param_5 + -2);
            kairo_unity_ui_Graphics__DrawLine
                      (fVar9,(float)(param_4 + 1),fVar8,(float)(param_4 + 1),0x3f800000,param_2,0);
            fVar7 = (float)(param_4 + 2);
            fVar10 = (float)(param_4 + param_6 + -2 + -1);
            kairo_unity_ui_Graphics__DrawLine(fVar9,fVar7,fVar9,fVar10,0x3f800000,param_2,0);
            if (3 < *(uint *)(param_7 + 0x18)) {
              lVar5 = *(long *)(param_7 + 0x38);
              if (lVar5 == 0) goto LAB_00f79d50;
              uVar2 = *(uint *)(lVar5 + 0x18);
              if (((uVar2 != 0) && (uVar2 != 1)) && (2 < uVar2)) {
                uVar4 = kairo_unity_ui_Graphics__GetColorOfRGB
                                  (*(undefined4 *)(lVar5 + 0x20),*(undefined4 *)(lVar5 + 0x24),
                                   *(undefined4 *)(lVar5 + 0x28),0);
                kairo_unity_ui_Graphics__SetColor(param_2,uVar4,0);
                fVar6 = (float)(param_6 + -2 + param_4);
                kairo_unity_ui_Graphics__DrawLine(fVar9,fVar6,fVar8,fVar6,0x3f800000,param_2,0);
                kairo_unity_ui_Graphics__DrawLine(fVar8,fVar7,fVar8,fVar10,0x3f800000,param_2,0);
                if (1 < *(uint *)(param_7 + 0x18)) {
                  lVar5 = *(long *)(param_7 + 0x28);
                  if (lVar5 == 0) goto LAB_00f79d50;
                  uVar2 = *(uint *)(lVar5 + 0x18);
                  if (((uVar2 != 0) && (uVar2 != 1)) && (2 < uVar2)) {
                    uVar4 = kairo_unity_ui_Graphics__GetColorOfRGB
                                      (*(undefined4 *)(lVar5 + 0x20),*(undefined4 *)(lVar5 + 0x24),
                                       *(undefined4 *)(lVar5 + 0x28),0);
                    kairo_unity_ui_Graphics__SetColor(param_2,uVar4,0);
                    kairo_unity_ui_Graphics__FillRect
                              ((float)(param_3 + 2),fVar7,(float)(param_5 + -4),
                               (float)(param_6 + -4),param_2,0);
                    return;
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
LAB_00f79d50:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__IsTopForm
// Address: 00f79d54
// ==========================================================================================

bool main_AppData__IsTopForm(undefined8 param_1,long param_2)

{
  long lVar1;
  
  lVar1 = form_FormManager__GetInstance();
  if (lVar1 != 0) {
    lVar1 = kairo_unity_form_FormManagerBase__GetTopForm(lVar1,0);
    return lVar1 == param_2;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSeb
// Address: 00f79d80
// ==========================================================================================

void main_AppData__DrawSeb(void)

{
  main_AppData__DrawSeb();
  return;
}



// ==========================================================================================
// Function: main_AppData__DrawSeb
// Address: 00f79dac
// ==========================================================================================

int main_AppData__DrawSeb
              (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,long param_6,
              undefined4 param_7,int param_8,int param_9,int param_10,int param_11)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  undefined *puVar5;
  long lVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  uint uVar10;
  
  puVar5 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff80f & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff80f = 1;
  }
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  iVar1 = param_8;
  if (999 < param_8) {
    iVar1 = 1000;
  }
  if (param_8 < 1) {
    iVar1 = 0;
  }
  iVar2 = param_9;
  if (999 < param_9) {
    iVar2 = 1000;
  }
  if (param_9 < 1) {
    iVar2 = 0;
  }
  iVar8 = param_3;
  if ((0 < param_8) && (0 < param_9)) {
    if ((param_5 == 0) || (lVar6 = kairo_unity_ui_Seb__GetSprites(param_5,param_7,0), lVar6 == 0)) {
LAB_00f79fe0:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar3 = *(uint *)(lVar6 + 0x18);
    if (0 < (int)uVar3) {
      uVar10 = 0;
      iVar7 = param_3;
      do {
        if (uVar3 <= uVar10) {
LAB_00f79fdc:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar9 = *(long *)(lVar6 + (long)(int)uVar10 * 8 + 0x20);
        iVar8 = param_10;
        if (param_10 == -1) {
          if (lVar9 == 0) goto LAB_00f79fe0;
          if (*(uint *)(lVar9 + 0x18) < 5) goto LAB_00f79fdc;
          iVar8 = *(int *)(lVar9 + 0x30);
        }
        if (param_11 == -1) {
          if (lVar9 == 0) goto LAB_00f79fe0;
          if (*(uint *)(lVar9 + 0x18) < 6) goto LAB_00f79fdc;
          iVar4 = *(int *)(lVar9 + 0x34);
        }
        else {
          iVar4 = param_11;
          if (lVar9 == 0) goto LAB_00f79fe0;
        }
        if (*(uint *)(lVar9 + 0x18) < 2) goto LAB_00f79fdc;
        if (param_6 == 0) goto LAB_00f79fe0;
        if ((*(uint *)(param_6 + 0x18) <= *(uint *)(lVar9 + 0x24)) || (*(uint *)(lVar9 + 0x18) < 7))
        goto LAB_00f79fdc;
        if (param_2 == 0) goto LAB_00f79fe0;
        iVar8 = (iVar8 * iVar1) / 1000;
        kairo_unity_ui_Graphics__DrawImage
                  ((float)(*(int *)(lVar9 + 0x38) + param_3),
                   (float)(*(int *)(lVar9 + 0x38) + param_4),param_2,
                   *(undefined8 *)(param_6 + (long)(int)*(uint *)(lVar9 + 0x24) * 8 + 0x20),
                   *(undefined4 *)(lVar9 + 0x28),*(undefined4 *)(lVar9 + 0x2c),iVar8,
                   (iVar4 * iVar2) / 1000,0);
        if (*(uint *)(lVar9 + 0x18) < 7) goto LAB_00f79fdc;
        uVar3 = *(uint *)(lVar6 + 0x18);
        uVar10 = uVar10 + 1;
        iVar8 = iVar8 + param_3 + *(int *)(lVar9 + 0x38);
        if (iVar8 <= iVar7) {
          iVar8 = iVar7;
        }
        iVar7 = iVar8;
      } while ((int)uVar10 < (int)uVar3);
    }
  }
  return iVar8;
}



// ==========================================================================================
// Function: main_AppData__DrawSeb
// Address: 00f79fe4
// ==========================================================================================

void main_AppData__DrawSeb
               (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,long param_6,
               undefined4 param_7,int param_8)

{
  uint uVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  uint uVar5;
  
  if (param_5 != 0) {
    lVar2 = kairo_unity_ui_Seb__GetSprites(param_5,param_7,0);
    if (lVar2 != 0) {
      uVar1 = *(uint *)(lVar2 + 0x18);
      if (0 < (int)uVar1) {
        uVar5 = 0;
        do {
          if (uVar1 <= uVar5) {
LAB_00f7a0ec:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar4 = *(long *)(lVar2 + (long)(int)uVar5 * 8 + 0x20);
          if (lVar4 == 0) goto LAB_00f7a0f0;
          uVar1 = *(uint *)(lVar4 + 0x18);
          if (uVar1 < 2) goto LAB_00f7a0ec;
          if (param_6 == 0) goto LAB_00f7a0f0;
          if (((*(uint *)(param_6 + 0x18) <= *(uint *)(lVar4 + 0x24)) || (uVar1 < 3)) || (uVar1 < 5)
             ) goto LAB_00f7a0ec;
          lVar3 = *(long *)(param_6 + (long)(int)*(uint *)(lVar4 + 0x24) * 8 + 0x20);
          if (lVar3 == 0) goto LAB_00f7a0f0;
          if ((uVar1 < 7) || (uVar1 == 7)) goto LAB_00f7a0ec;
          if (param_2 == 0) goto LAB_00f7a0f0;
          kairo_unity_ui_Graphics__DrawImage
                    ((float)(*(int *)(lVar4 + 0x38) + param_3),
                     (float)(*(int *)(lVar4 + 0x3c) + param_4),param_2,lVar3,
                     *(int *)(lVar4 + 0x28) + *(int *)(lVar4 + 0x30) * param_8,
                     *(undefined4 *)(lVar4 + 0x2c),*(int *)(lVar4 + 0x30),
                     *(undefined4 *)(lVar4 + 0x34),0);
          uVar1 = *(uint *)(lVar2 + 0x18);
          uVar5 = uVar5 + 1;
        } while ((int)uVar5 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7a0f0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSebV
// Address: 00f7a0f4
// ==========================================================================================

void main_AppData__DrawSebV
               (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,long param_6,
               undefined4 param_7,int param_8)

{
  uint uVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  uint uVar5;
  
  if (param_5 != 0) {
    lVar2 = kairo_unity_ui_Seb__GetSprites(param_5,param_7,0);
    if (lVar2 != 0) {
      uVar1 = *(uint *)(lVar2 + 0x18);
      if (0 < (int)uVar1) {
        uVar5 = 0;
        do {
          if (uVar1 <= uVar5) {
LAB_00f7a1fc:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar4 = *(long *)(lVar2 + (long)(int)uVar5 * 8 + 0x20);
          if (lVar4 == 0) goto LAB_00f7a200;
          uVar1 = *(uint *)(lVar4 + 0x18);
          if (uVar1 < 2) goto LAB_00f7a1fc;
          if (param_6 == 0) goto LAB_00f7a200;
          if (((*(uint *)(param_6 + 0x18) <= *(uint *)(lVar4 + 0x24)) || (uVar1 < 4)) || (uVar1 < 6)
             ) goto LAB_00f7a1fc;
          lVar3 = *(long *)(param_6 + (long)(int)*(uint *)(lVar4 + 0x24) * 8 + 0x20);
          if (lVar3 == 0) goto LAB_00f7a200;
          if ((uVar1 < 7) || (uVar1 == 7)) goto LAB_00f7a1fc;
          if (param_2 == 0) goto LAB_00f7a200;
          kairo_unity_ui_Graphics__DrawImage
                    ((float)(*(int *)(lVar4 + 0x38) + param_3),
                     (float)(*(int *)(lVar4 + 0x3c) + param_4),param_2,lVar3,
                     *(undefined4 *)(lVar4 + 0x28),
                     *(int *)(lVar4 + 0x2c) + *(int *)(lVar4 + 0x34) * param_8,
                     *(undefined4 *)(lVar4 + 0x30),*(int *)(lVar4 + 0x34),0);
          uVar1 = *(uint *)(lVar2 + 0x18);
          uVar5 = uVar5 + 1;
        } while ((int)uVar5 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7a200:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSeb
// Address: 00f7a204
// ==========================================================================================

void main_AppData__DrawSeb
               (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,
               undefined8 param_6,undefined4 param_7)

{
  uint uVar1;
  long lVar2;
  long lVar3;
  uint uVar4;
  
  if (param_5 != 0) {
    lVar2 = kairo_unity_ui_Seb__GetSprites(param_5,param_7,0);
    if (lVar2 != 0) {
      uVar1 = *(uint *)(lVar2 + 0x18);
      if (0 < (int)uVar1) {
        uVar4 = 0;
        do {
          if (uVar1 <= uVar4) {
LAB_00f7a2dc:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar3 = *(long *)(lVar2 + (long)(int)uVar4 * 8 + 0x20);
          if (lVar3 == 0) goto LAB_00f7a2e0;
          uVar1 = *(uint *)(lVar3 + 0x18);
          if (uVar1 < 2) goto LAB_00f7a2dc;
          if (-1 < *(int *)(lVar3 + 0x24)) {
            if ((uVar1 < 7) || (uVar1 == 7)) goto LAB_00f7a2dc;
            if (param_2 == 0) goto LAB_00f7a2e0;
            kairo_unity_ui_Graphics__DrawImage
                      ((float)(*(int *)(lVar3 + 0x38) + param_3),
                       (float)(*(int *)(lVar3 + 0x3c) + param_4),param_2,param_6,
                       *(undefined4 *)(lVar3 + 0x28),*(undefined4 *)(lVar3 + 0x2c),
                       *(undefined4 *)(lVar3 + 0x30),*(undefined4 *)(lVar3 + 0x34),0);
          }
          uVar1 = *(uint *)(lVar2 + 0x18);
          uVar4 = uVar4 + 1;
        } while ((int)uVar4 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7a2e0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSebReverse
// Address: 00f7a2e4
// ==========================================================================================

void main_AppData__DrawSebReverse
               (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,
               undefined4 param_6,long param_7)

{
  uint uVar1;
  uint uVar2;
  long lVar3;
  long lVar4;
  uint uVar5;
  
  if (param_5 != 0) {
    lVar3 = kairo_unity_ui_Seb__GetSprites(param_5,param_6,0);
    if (lVar3 != 0) {
      uVar1 = *(uint *)(lVar3 + 0x18);
      if (0 < (int)uVar1) {
        uVar5 = 0;
        do {
          if (uVar1 <= uVar5) {
LAB_00f7a3d4:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar4 = *(long *)(lVar3 + (long)(int)uVar5 * 8 + 0x20);
          if (lVar4 == 0) goto LAB_00f7a3d8;
          uVar1 = *(uint *)(lVar4 + 0x18);
          if (uVar1 < 2) goto LAB_00f7a3d4;
          uVar2 = *(uint *)(lVar4 + 0x24);
          if (-1 < (int)uVar2) {
            if (param_7 == 0) goto LAB_00f7a3d8;
            if (((*(uint *)(param_7 + 0x18) <= uVar2) || (uVar1 < 7)) || (uVar1 == 7))
            goto LAB_00f7a3d4;
            if (param_2 == 0) goto LAB_00f7a3d8;
            kairo_unity_ui_Graphics__DrawImage
                      ((float)((param_3 - *(int *)(lVar4 + 0x38)) - *(int *)(lVar4 + 0x30)),
                       (float)(*(int *)(lVar4 + 0x3c) + param_4),param_2,
                       *(undefined8 *)(param_7 + (ulong)uVar2 * 8 + 0x20),
                       *(undefined4 *)(lVar4 + 0x28),*(undefined4 *)(lVar4 + 0x2c),
                       *(int *)(lVar4 + 0x30),*(undefined4 *)(lVar4 + 0x34),0);
          }
          uVar1 = *(uint *)(lVar3 + 0x18);
          uVar5 = uVar5 + 1;
        } while ((int)uVar5 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7a3d8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__ColRect
// Address: 00f7a3dc
// ==========================================================================================

bool main_AppData__ColRect(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6)

{
  return param_2 < param_6 && (param_4 < param_2 && (param_3 < param_1 && param_1 < param_5));
}



// ==========================================================================================
// Function: main_AppData__ColRect
// Address: 00f7a40c
// ==========================================================================================

bool main_AppData__ColRect
               (int param_1,int param_2,int param_3,int param_4,int param_5,int param_6,int param_7,
               int param_8)

{
  return ((param_5 <= param_3 && param_6 <= param_4) && param_1 <= param_7) && param_2 <= param_8;
}



// ==========================================================================================
// Function: main_AppData__CommaSeparate
// Address: 00f7a43c
// ==========================================================================================

long main_AppData__CommaSeparate(long param_1)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  long lVar7;
  int iVar8;
  undefined2 local_54 [2];
  long local_48;
  
  local_48 = param_1;
  if ((DAT_020ff810 & 1) == 0) {
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_StringLiteral_678_01fbf998);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff810 = 1;
  }
  puVar2 = PTR_StringLiteral_1_01fbf388;
  local_54[0] = 0;
  if (param_1 < 0) {
    local_48 = -param_1;
  }
  lVar5 = System_Int64__ToString(&local_48,0);
  lVar7 = *(long *)puVar2;
  lVar1 = lVar7;
  if (lVar5 != 0) {
    lVar1 = lVar5;
  }
  iVar4 = java_lang_StringEx__Length(lVar1,0);
  puVar3 = PTR_char_TypeInfo_01fbf990;
  puVar2 = PTR_StringLiteral_646_01fbf440;
  iVar4 = iVar4 + -1;
  if (-1 < iVar4) {
    iVar8 = 0;
    do {
      if ((0 < iVar8) && (iVar8 % 3 == 0)) {
        lVar7 = System_String__Concat(*(undefined8 *)puVar2,lVar7,0);
      }
      local_54[0] = java_lang_StringEx__CharAt(lVar1,iVar4,0);
      if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar3);
      }
      uVar6 = System_Char__ToString(local_54,0);
      lVar7 = System_String__Concat(uVar6,lVar7,0);
      iVar4 = iVar4 + -1;
      iVar8 = iVar8 + 1;
    } while (iVar4 != -1);
  }
  if (param_1 < 0) {
    lVar7 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_678_01fbf998,lVar7,0);
  }
  return lVar7;
}



// ==========================================================================================
// Function: main_AppData__GetBRectSeb
// Address: 00f7a5c8
// ==========================================================================================

long main_AppData__GetBRectSeb(long param_1,long param_2,int param_3,int param_4)

{
  uint uVar1;
  uint uVar2;
  long lVar3;
  long lVar4;
  
  if ((param_2 != 0) && (lVar3 = kairo_unity_ui_Seb__GetBoundingRect(param_2,0), lVar3 != 0)) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if (uVar1 != 0) {
      lVar4 = *(long *)(param_1 + 0x68);
      if (lVar4 == 0) goto LAB_00f7a674;
      uVar2 = *(uint *)(lVar4 + 0x18);
      if ((((uVar2 != 0) && (*(int *)(lVar4 + 0x20) = *(int *)(lVar3 + 0x20) + param_3, 1 < uVar1))
          && (1 < uVar2)) &&
         (((*(int *)(lVar4 + 0x24) = *(int *)(lVar3 + 0x24) + param_4, 2 < uVar1 && (2 < uVar2)) &&
          ((*(undefined4 *)(lVar4 + 0x28) = *(undefined4 *)(lVar3 + 0x28), 3 < uVar1 && (3 < uVar2))
          )))) {
        *(undefined4 *)(lVar4 + 0x2c) = *(undefined4 *)(lVar3 + 0x2c);
        return lVar4;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f7a674:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawVerticalScroll
// Address: 00f7a678
// ==========================================================================================

void main_AppData__DrawVerticalScroll
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7,uint param_8,int param_9)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  
  puVar5 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if ((DAT_020ff811 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff811 = 1;
  }
  uVar2 = param_9 - 1U;
  if ((int)(param_9 - 1U) <= (int)param_8) {
    uVar2 = param_8;
  }
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            ((float)(param_3 + 1),(float)param_4,0x3f800000,(float)(param_6 + -2),param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  fVar7 = (float)param_3;
  fVar8 = (float)param_5;
  kairo_unity_ui_Graphics__FillRect(fVar7,(float)param_4,fVar8,0x3f800000,param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            (fVar7,(float)(param_6 + param_4 + -3),fVar8,0x3f800000,param_2,0);
  iVar1 = (uVar2 & ((int)uVar2 >> 0x1f ^ 0xffffffffU)) + 1;
  iVar3 = 0;
  if (iVar1 != 0) {
    iVar3 = (param_7 * param_6) / iVar1;
  }
  iVar4 = 0;
  if (iVar1 != 0) {
    iVar4 = (param_9 * param_6) / iVar1;
  }
  iVar3 = iVar3 + param_4;
  iVar1 = param_6 - iVar3;
  if (iVar4 + iVar3 <= param_6 + param_4) {
    iVar1 = iVar4;
  }
  if (0 < iVar1) {
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    fVar9 = (float)iVar3;
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,fVar8,(float)iVar1,param_2,0);
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,0x3f800000,0x3f800000,param_2,0);
    fVar8 = (float)(param_3 + param_5 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar8,fVar9,0x3f800000,0x3f800000,param_2,0);
    fVar9 = (float)(iVar3 + iVar1 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,0x3f800000,0x3f800000,param_2,0);
    kairo_unity_ui_Graphics__FillRect(fVar8,fVar9,0x3f800000,0x3f800000,param_2,0);
    return;
  }
  return;
}



// ==========================================================================================
// Function: main_AppData__DrawVerticalScroll2
// Address: 00f7a958
// ==========================================================================================

void main_AppData__DrawVerticalScroll2
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7,uint param_8,int param_9)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  
  puVar5 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if ((DAT_020ff812 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff812 = 1;
  }
  uVar2 = param_9 - 1U;
  if ((int)(param_9 - 1U) <= (int)param_8) {
    uVar2 = param_8;
  }
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x61,0xa9,0xff,0);
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  fVar7 = (float)param_3;
  kairo_unity_ui_Graphics__FillRect
            (fVar7,(float)(param_4 + -1),(float)(param_5 + 2),(float)(param_6 + 2),param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            ((float)(param_3 + 1),(float)param_4,0x3f800000,(float)(param_6 + -2),param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  fVar8 = (float)param_5;
  kairo_unity_ui_Graphics__FillRect(fVar7,(float)param_4,fVar8,0x3f800000,param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            (fVar7,(float)(param_6 + -2 + param_4 + -1),fVar8,0x3f800000,param_2,0);
  iVar1 = (uVar2 & ((int)uVar2 >> 0x1f ^ 0xffffffffU)) + 1;
  iVar3 = 0;
  if (iVar1 != 0) {
    iVar3 = (param_7 * param_6) / iVar1;
  }
  iVar4 = 0;
  if (iVar1 != 0) {
    iVar4 = (param_9 * param_6) / iVar1;
  }
  iVar3 = iVar3 + param_4;
  iVar1 = param_6 - iVar3;
  if (iVar4 + iVar3 <= param_6 + param_4) {
    iVar1 = iVar4;
  }
  if (0 < iVar1) {
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    fVar9 = (float)iVar3;
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,fVar8,(float)iVar1,param_2,0);
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,0x3f800000,0x3f800000,param_2,0);
    fVar8 = (float)(param_3 + param_5 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar8,fVar9,0x3f800000,0x3f800000,param_2,0);
    fVar9 = (float)(iVar3 + iVar1 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar7,fVar9,0x3f800000,0x3f800000,param_2,0);
    kairo_unity_ui_Graphics__FillRect(fVar8,fVar9,0x3f800000,0x3f800000,param_2,0);
    return;
  }
  return;
}



// ==========================================================================================
// Function: main_AppData__DrawHorizontallScroll
// Address: 00f7ac84
// ==========================================================================================

void main_AppData__DrawHorizontallScroll
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               int param_7,uint param_8,int param_9)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  
  puVar5 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  if ((DAT_020ff813 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff813 = 1;
  }
  uVar2 = param_9 - 1U;
  if ((int)(param_9 - 1U) <= (int)param_8) {
    uVar2 = param_8;
  }
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            ((float)param_3,(float)(param_4 + 1),(float)(param_5 + -2),0x3f800000,param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  fVar7 = (float)param_4;
  fVar8 = (float)param_6;
  kairo_unity_ui_Graphics__FillRect((float)param_3,fVar7,0x3f800000,fVar8,param_2,0);
  uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
  kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
  kairo_unity_ui_Graphics__FillRect
            ((float)(param_5 + param_3 + -3),fVar7,0x3f800000,fVar8,param_2,0);
  iVar1 = (uVar2 & ((int)uVar2 >> 0x1f ^ 0xffffffffU)) + 1;
  iVar3 = 0;
  if (iVar1 != 0) {
    iVar3 = (param_7 * param_5) / iVar1;
  }
  iVar4 = 0;
  if (iVar1 != 0) {
    iVar4 = (param_9 * param_5) / iVar1;
  }
  iVar3 = iVar3 + param_3;
  iVar1 = param_5 - iVar3;
  if (iVar4 + iVar3 <= param_5 + param_3) {
    iVar1 = iVar4;
  }
  if (0 < iVar1) {
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x35,0x17,0xd8,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    fVar9 = (float)iVar3;
    kairo_unity_ui_Graphics__FillRect(fVar9,fVar7,(float)iVar1,fVar8,param_2,0);
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0x4e,0x55,0xcd,0);
    kairo_unity_ui_Graphics__SetColor(param_2,uVar6,0);
    kairo_unity_ui_Graphics__FillRect(fVar9,fVar7,0x3f800000,0x3f800000,param_2,0);
    fVar8 = (float)(param_4 + param_6 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar9,fVar8,0x3f800000,0x3f800000,param_2,0);
    fVar9 = (float)(iVar3 + iVar1 + -1);
    kairo_unity_ui_Graphics__FillRect(fVar9,fVar7,0x3f800000,0x3f800000,param_2,0);
    kairo_unity_ui_Graphics__FillRect(fVar9,fVar8,0x3f800000,0x3f800000,param_2,0);
    return;
  }
  return;
}



// ==========================================================================================
// Function: main_AppData__Random
// Address: 00f7af64
// ==========================================================================================

void main_AppData__Random(int param_1)

{
  int iVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff814 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff814 = 1;
  }
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0xe0);
  if (lVar4 != 0) {
    iVar3 = java_util_JRandom__NextInt(lVar4,0);
    iVar1 = 0;
    if (param_1 != 0) {
      iVar1 = iVar3 / param_1;
    }
    java_lang_JMath__Abs(iVar3 - iVar1 * param_1,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Push
// Address: 00f7afdc
// ==========================================================================================

void main_AppData__Push(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  undefined8 uVar2;
  
  lVar1 = form_FormManager__GetInstance();
  if (lVar1 != 0) {
    uVar2 = kairo_unity_form_FormManagerBase__GetCurrentForm(lVar1,0);
    kairo_unity_form_FormManagerBase__Push(lVar1,uVar2,param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__PlayBgm
// Address: 00f7b01c
// ==========================================================================================

void main_AppData__PlayBgm(long param_1,uint param_2)

{
  uint uVar1;
  undefined *puVar2;
  int iVar3;
  long *plVar4;
  long lVar5;
  long lVar6;
  uint uVar7;
  long lVar8;
  
  if ((DAT_020ff815 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    DAT_020ff815 = 1;
  }
  if ((*(long *)(param_1 + 0x40) != 0) &&
     (lVar5 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar5 != 0)) {
    if (*(uint *)(lVar5 + 0x18) <= param_2) {
LAB_00f7b20c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    plVar4 = *(long **)(lVar5 + (long)(int)param_2 * 8 + 0x20);
    if (plVar4 != (long *)0x0) {
      iVar3 = (**(code **)(*plVar4 + 0x1b8))(plVar4,*(undefined8 *)(*plVar4 + 0x1c0));
      puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
      if (iVar3 == 2) {
        return;
      }
      uVar7 = 0;
      while( true ) {
        lVar5 = *(long *)puVar2;
        if (*(int *)(lVar5 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar5 = *(long *)puVar2;
        }
        lVar6 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x50);
        if (lVar6 == 0) goto LAB_00f7b208;
        if (*(int *)(lVar6 + 0x18) <= (int)uVar7) break;
        if (*(long *)(param_1 + 0x40) == 0) goto LAB_00f7b208;
        lVar8 = *(long *)(*(long *)(param_1 + 0x40) + 0x20);
        if (*(int *)(lVar5 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar6 = *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x50);
          if (lVar6 == 0) goto LAB_00f7b208;
        }
        if (*(uint *)(lVar6 + 0x18) <= uVar7) goto LAB_00f7b20c;
        if (lVar8 == 0) goto LAB_00f7b208;
        uVar1 = *(uint *)(lVar6 + (long)(int)uVar7 * 4 + 0x20);
        if (*(uint *)(lVar8 + 0x18) <= uVar1) goto LAB_00f7b20c;
        plVar4 = *(long **)(lVar8 + (long)(int)uVar1 * 8 + 0x20);
        if (plVar4 == (long *)0x0) goto LAB_00f7b208;
        iVar3 = (**(code **)(*plVar4 + 0x1b8))(plVar4,*(undefined8 *)(*plVar4 + 0x1c0));
        if (iVar3 == 2) {
          if (*(long *)(param_1 + 0x40) == 0) goto LAB_00f7b208;
          lVar5 = *(long *)puVar2;
          lVar6 = *(long *)(*(long *)(param_1 + 0x40) + 0x20);
          if (*(int *)(lVar5 + 0xe0) == 0) {
            thunk_FUN_00df405c();
            lVar5 = *(long *)puVar2;
          }
          lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x50);
          if (lVar5 == 0) goto LAB_00f7b208;
          if (*(uint *)(lVar5 + 0x18) <= uVar7) goto LAB_00f7b20c;
          if (lVar6 == 0) goto LAB_00f7b208;
          uVar1 = *(uint *)(lVar5 + (long)(int)uVar7 * 4 + 0x20);
          if (*(uint *)(lVar6 + 0x18) <= uVar1) goto LAB_00f7b20c;
          plVar4 = *(long **)(lVar6 + (long)(int)uVar1 * 8 + 0x20);
          if (plVar4 == (long *)0x0) goto LAB_00f7b208;
          (**(code **)(*plVar4 + 0x198))(plVar4,*(undefined8 *)(*plVar4 + 0x1a0));
        }
        uVar7 = uVar7 + 1;
      }
      lVar5 = kairo_unity_ui_SoundPlayer__GetInstance(0);
      if ((*(long *)(param_1 + 0x40) != 0) &&
         (lVar6 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar6 != 0)) {
        if (*(uint *)(lVar6 + 0x18) <= param_2) goto LAB_00f7b20c;
        if (lVar5 != 0) {
          kairo_unity_ui_SoundPlayer__Play
                    (lVar5,*(undefined8 *)(lVar6 + (long)(int)param_2 * 8 + 0x20),0);
          return;
        }
      }
    }
  }
LAB_00f7b208:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__PlaySe
// Address: 00f7b210
// ==========================================================================================

void main_AppData__PlaySe(long param_1,uint param_2)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  
  lVar2 = kairo_unity_ui_SoundPlayer__GetInstance(0);
  if ((*(long *)(param_1 + 0x40) == 0) ||
     (lVar4 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar4 == 0)) goto LAB_00f7b2f8;
  if (*(uint *)(lVar4 + 0x18) <= param_2) {
LAB_00f7b2fc:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
  lVar5 = (long)(int)param_2;
  plVar3 = *(long **)(lVar4 + lVar5 * 8 + 0x20);
  if (plVar3 == (long *)0x0) {
    return;
  }
  iVar1 = (**(code **)(*plVar3 + 0x1b8))(plVar3,*(undefined8 *)(*plVar3 + 0x1c0));
  if (iVar1 != 3) {
    if ((*(long *)(param_1 + 0x40) == 0) ||
       (lVar4 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar4 == 0)) goto LAB_00f7b2f8;
    if (*(uint *)(lVar4 + 0x18) <= param_2) goto LAB_00f7b2fc;
    plVar3 = *(long **)(lVar4 + lVar5 * 8 + 0x20);
    if (plVar3 == (long *)0x0) goto LAB_00f7b2f8;
    iVar1 = (**(code **)(*plVar3 + 0x1b8))(plVar3,*(undefined8 *)(*plVar3 + 0x1c0));
    if (iVar1 != 0) {
      return;
    }
  }
  if ((*(long *)(param_1 + 0x40) != 0) &&
     (lVar4 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar4 != 0)) {
    if (*(uint *)(lVar4 + 0x18) <= param_2) goto LAB_00f7b2fc;
    if (lVar2 != 0) {
      kairo_unity_ui_SoundPlayer__Play(lVar2,*(undefined8 *)(lVar4 + lVar5 * 8 + 0x20),0);
      return;
    }
  }
LAB_00f7b2f8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__PlayJingle
// Address: 00f7b300
// ==========================================================================================

void main_AppData__PlayJingle(long param_1,uint param_2)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x40) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x40) + 0x20), lVar1 != 0)) {
    if (param_2 < *(uint *)(lVar1 + 0x18)) {
      main_Main__SetJingle(*(undefined8 *)(lVar1 + (long)(int)param_2 * 8 + 0x20),0x14);
      main_AppData__PlaySe(param_1,param_2);
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_Main__SetJingle
// Address: 00f7b358
// ==========================================================================================

void main_Main__SetJingle(undefined8 param_1,undefined4 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  int iVar5;
  long *plVar6;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff837 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_main_Main_TypeInfo_01fc33d8);
    DAT_020ff837 = 1;
  }
  puVar2 = PTR_main_Main_TypeInfo_01fc33d8;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  main_AppData__GetInstance();
  lVar3 = kairo_unity_ui_SoundPlayer__GetInstance(0);
  **(undefined8 **)(*(long *)puVar2 + 0xb8) = param_1;
  plVar6 = *(long **)(*(long *)puVar2 + 0xb8);
  *(undefined4 *)(plVar6 + 1) = param_2;
  puVar1 = PTR_form_GameForm_TypeInfo_01fbfab0;
  if (*plVar6 == 0) {
    lVar4 = *(long *)PTR_form_GameForm_TypeInfo_01fbfab0;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar1;
    }
    lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0xf70);
    if (lVar4 != 0) {
      if (*(int *)(lVar4 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      if (lVar3 != 0) {
        iVar5 = *(int *)(lVar4 + 0x20) * 0x33;
        goto LAB_00f7b440;
      }
    }
  }
  else if (lVar3 != 0) {
    iVar5 = 0;
LAB_00f7b440:
    kairo_unity_ui_SoundPlayer__SetVolume(lVar3,0,iVar5,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetHttpErrorText
// Address: 00f7b464
// ==========================================================================================

undefined8 main_AppData__GetHttpErrorText(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  
  puVar2 = PTR_StringLiteral_12180_01fc33e0;
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff816 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_StringLiteral_12180_01fc33e0);
    DAT_020ff816 = 1;
  }
  uVar4 = *(undefined8 *)puVar2;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = kairo_unity_io_Http__GetErrorText(0);
  if (lVar3 != 0) {
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar4 = kairo_unity_io_Http__GetErrorText(0);
    return uVar4;
  }
  return uVar4;
}



// ==========================================================================================
// Function: main_AppData__GetHighScore
// Address: 00f7b4f8
// ==========================================================================================

undefined8 main_AppData__GetHighScore(long param_1)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (*(int *)(lVar1 + 0x18) != 0) {
      return *(undefined8 *)(lVar1 + 0x20);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SetHighScore
// Address: 00f7b528
// ==========================================================================================

void main_AppData__SetHighScore(long param_1,undefined8 param_2)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (*(int *)(lVar1 + 0x18) != 0) {
      *(undefined8 *)(lVar1 + 0x20) = param_2;
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetNetHighScore
// Address: 00f7b558
// ==========================================================================================

undefined8 main_AppData__GetNetHighScore(long param_1)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (1 < *(uint *)(lVar1 + 0x18)) {
      return *(undefined8 *)(lVar1 + 0x28);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SetNetHighScore
// Address: 00f7b58c
// ==========================================================================================

void main_AppData__SetNetHighScore(long param_1,undefined8 param_2)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (1 < *(uint *)(lVar1 + 0x18)) {
      *(undefined8 *)(lVar1 + 0x28) = param_2;
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetMoneyHighScore
// Address: 00f7b5c0
// ==========================================================================================

undefined8 main_AppData__GetMoneyHighScore(long param_1)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (2 < *(uint *)(lVar1 + 0x18)) {
      return *(undefined8 *)(lVar1 + 0x30);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SetMoneyHighScore
// Address: 00f7b5f4
// ==========================================================================================

void main_AppData__SetMoneyHighScore(long param_1,undefined8 param_2)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (2 < *(uint *)(lVar1 + 0x18)) {
      *(undefined8 *)(lVar1 + 0x30) = param_2;
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GettMoneyNetHighScore
// Address: 00f7b628
// ==========================================================================================

undefined8 main_AppData__GettMoneyNetHighScore(long param_1)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (3 < *(uint *)(lVar1 + 0x18)) {
      return *(undefined8 *)(lVar1 + 0x38);
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SettMoneyNetHighScore
// Address: 00f7b65c
// ==========================================================================================

void main_AppData__SettMoneyNetHighScore(long param_1,undefined8 param_2)

{
  long lVar1;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (lVar1 = *(long *)(*(long *)(param_1 + 0x48) + 0x28), lVar1 != 0)) {
    if (3 < *(uint *)(lVar1 + 0x18)) {
      *(undefined8 *)(lVar1 + 0x38) = param_2;
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SendSaveData
// Address: 00f7b690
// ==========================================================================================

void main_AppData__SendSaveData(long param_1,undefined8 param_2)

{
  if (param_1 != 0) {
    main_AppData__SendSaveData(param_1,param_2,0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SendSaveData
// Address: 00f7b6a4
// ==========================================================================================

void main_AppData__SendSaveData(long param_1,undefined8 param_2,uint param_3)

{
  if (param_1 != 0) {
    main_AppData__SendSaveData(param_1,param_2,param_3 & 1);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SendSaveData
// Address: 00f7b6b8
// ==========================================================================================

void main_AppData__SendSaveData(long param_1,undefined8 param_2,int param_3)

{
  ulong uVar1;
  uint uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  int iVar6;
  undefined4 uVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  long lVar13;
  long lVar14;
  long lVar15;
  long lVar16;
  long lVar17;
  long lVar18;
  undefined8 *puVar19;
  undefined8 uVar20;
  ulong uVar21;
  int iVar22;
  undefined8 *puVar23;
  int local_64;
  
  puVar5 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_020ff817 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_byte_____TypeInfo_01fc00f8);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100);
    FUN_00db0bbc(PTR_java_util_JDate_TypeInfo_01fbf748);
    FUN_00db0bbc(PTR_java_lang_JString_TypeInfo_01fbf368);
    FUN_00db0bbc(PTR_java_lang_JThread_TypeInfo_01fbf2e0);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_45_01fbf350);
    FUN_00db0bbc(PTR_StringLiteral_8941_01fc33e8);
    FUN_00db0bbc(PTR_StringLiteral_12172_01fc2c88);
    FUN_00db0bbc(PTR_StringLiteral_8935_01fc2c90);
    FUN_00db0bbc(PTR_StringLiteral_11559_01fc0148);
    FUN_00db0bbc(PTR_StringLiteral_6380_01fc05d0);
    FUN_00db0bbc(PTR_StringLiteral_73_01fc33f0);
    FUN_00db0bbc(PTR_StringLiteral_78_01fc2c98);
    FUN_00db0bbc(PTR_StringLiteral_7956_01fc2ca0);
    FUN_00db0bbc(PTR_StringLiteral_7287_01fc2ca8);
    FUN_00db0bbc(PTR_StringLiteral_58_01fc33f8);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_787_01fbf9c0);
    FUN_00db0bbc(PTR_StringLiteral_927_01fbff50);
    DAT_020ff817 = 1;
  }
  lVar8 = FUN_00db0c30(*(undefined8 *)puVar5,6);
  if (lVar8 != 0) {
    uVar2 = *(uint *)(lVar8 + 0x18);
    if (((uVar2 != 0) &&
        (*(undefined8 *)(lVar8 + 0x20) = *(undefined8 *)PTR_StringLiteral_7287_01fc2ca8, uVar2 != 1)
        ) && (*(undefined8 *)(lVar8 + 0x28) = *(undefined8 *)(param_1 + 0x58), 2 < uVar2)) {
      *(undefined8 *)(lVar8 + 0x30) = *(undefined8 *)PTR_StringLiteral_78_01fc2c98;
      local_64 = 0x10d;
      uVar9 = System_Int32__ToString(&local_64,0);
      uVar2 = *(uint *)(lVar8 + 0x18);
      if (((3 < uVar2) && (*(undefined8 *)(lVar8 + 0x38) = uVar9, uVar2 != 4)) &&
         (*(undefined8 *)(lVar8 + 0x40) = *(undefined8 *)PTR_StringLiteral_45_01fbf350,
         puVar4 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8,
         puVar3 = PTR_main_AppData_TypeInfo_01fbf278, 5 < uVar2)) {
        *(undefined8 *)(lVar8 + 0x48) = param_2;
        uVar9 = Method_System_String_Concat(lVar8,0);
        if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c(*(long *)puVar4);
        }
        lVar8 = kairo_unity_ui_Canvas__GetInstance(0);
        if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c(*(long *)puVar3);
        }
        main_AppData__GetInstance();
        puVar4 = PTR_java_util_JDate_TypeInfo_01fbf748;
        puVar3 = PTR_StringLiteral_1_01fbf388;
        if (lVar8 != 0) {
          kairo_unity_ui_Canvas__SetSoftLabel(lVar8,0,*(undefined8 *)PTR_StringLiteral_1_01fbf388,0)
          ;
          kairo_unity_ui_Canvas__SetSoftLabel(lVar8,1,*(undefined8 *)puVar3,0);
          lVar10 = java_util_JCalendar__GetInstance(0);
          uVar11 = java_lang_JSystem__CurrentTimeMillis(0);
          uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
          java_util_JDate___ctor(uVar12,uVar11,0);
          puVar4 = PTR_StringLiteral_927_01fbff50;
          if (lVar10 != 0) {
            *(undefined8 *)(lVar10 + 0x10) = uVar12;
            local_64 = Method_java_util_JCalendar_Get(lVar10,1,0);
            lVar13 = System_Int32__ToString(&local_64,0);
            lVar18 = *(long *)puVar3;
            if (lVar13 != 0) {
              lVar18 = lVar13;
            }
            local_64 = Method_java_util_JCalendar_Get(lVar10,2,0);
            local_64 = local_64 + 1;
            lVar14 = System_Int32__ToString(&local_64,0);
            lVar13 = *(long *)puVar3;
            if (lVar14 != 0) {
              lVar13 = lVar14;
            }
            iVar6 = java_lang_StringEx__Length(lVar13,0);
            if (iVar6 == 1) {
              lVar13 = System_String__Concat(*(undefined8 *)puVar4,lVar13,0);
            }
            local_64 = Method_java_util_JCalendar_Get(lVar10,5,0);
            lVar15 = System_Int32__ToString(&local_64,0);
            lVar14 = *(long *)puVar3;
            if (lVar15 != 0) {
              lVar14 = lVar15;
            }
            iVar6 = java_lang_StringEx__Length(lVar14,0);
            if (iVar6 == 1) {
              lVar14 = System_String__Concat(*(undefined8 *)puVar4,lVar14,0);
            }
            local_64 = Method_java_util_JCalendar_Get(lVar10,0xb,0);
            lVar16 = System_Int32__ToString(&local_64,0);
            lVar15 = *(long *)puVar3;
            if (lVar16 != 0) {
              lVar15 = lVar16;
            }
            iVar6 = java_lang_StringEx__Length(lVar15,0);
            if (iVar6 == 1) {
              lVar15 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_927_01fbff50,lVar15,0)
              ;
            }
            local_64 = Method_java_util_JCalendar_Get(lVar10,0xc,0);
            lVar17 = System_Int32__ToString(&local_64,0);
            lVar16 = *(long *)puVar3;
            if (lVar17 != 0) {
              lVar16 = lVar17;
            }
            iVar6 = java_lang_StringEx__Length(lVar16,0);
            if (iVar6 == 1) {
              lVar16 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_927_01fbff50,lVar16,0)
              ;
            }
            local_64 = Method_java_util_JCalendar_Get(lVar10,0xd,0);
            lVar17 = System_Int32__ToString(&local_64,0);
            lVar10 = *(long *)PTR_StringLiteral_1_01fbf388;
            if (lVar17 != 0) {
              lVar10 = lVar17;
            }
            iVar6 = java_lang_StringEx__Length(lVar10,0);
            if (iVar6 == 1) {
              lVar10 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_927_01fbff50,lVar10,0)
              ;
            }
            lVar17 = FUN_00db0c30(*(undefined8 *)puVar5,0xb);
            if (lVar17 != 0) {
              uVar2 = *(uint *)(lVar17 + 0x18);
              if ((((uVar2 != 0) &&
                   (*(long *)(lVar17 + 0x20) = lVar18, puVar3 = PTR_StringLiteral_787_01fbf9c0,
                   uVar2 != 1)) &&
                  (((*(undefined8 *)(lVar17 + 0x28) = *(undefined8 *)PTR_StringLiteral_787_01fbf9c0,
                    2 < uVar2 &&
                    ((((*(long *)(lVar17 + 0x30) = lVar13, uVar2 != 3 &&
                       (*(undefined8 *)(lVar17 + 0x38) = *(undefined8 *)puVar3, 4 < uVar2)) &&
                      (*(long *)(lVar17 + 0x40) = lVar14, uVar2 != 5)) &&
                     ((*(undefined8 *)(lVar17 + 0x48) =
                            *(undefined8 *)PTR_StringLiteral_6380_01fc05d0, 6 < uVar2 &&
                      (*(long *)(lVar17 + 0x50) = lVar15, uVar2 != 7)))))) &&
                   (*(undefined8 *)(lVar17 + 0x58) = *(undefined8 *)puVar3,
                   puVar23 = (undefined8 *)PTR_StringLiteral_927_01fbff50, 8 < uVar2)))) &&
                 ((*(long *)(lVar17 + 0x60) = lVar16, uVar2 != 9 &&
                  (*(undefined8 *)(lVar17 + 0x68) = *(undefined8 *)puVar3,
                  puVar3 = PTR_main_AppData_TypeInfo_01fbf278, 10 < uVar2)))) {
                *(long *)(lVar17 + 0x70) = lVar10;
                uVar11 = Method_System_String_Concat(lVar17,0);
                *(undefined4 *)(param_1 + 0xac) = 0;
                kairo_unity_ui_Canvas__ClearKeyBuffer(lVar8,0);
                do {
                  kairo_unity_ui_Canvas__DecideKeyState(lVar8,0);
                  if (*(int *)(param_1 + 0xac) == 0) {
                    /* try { // try from 00f7bcf8 to 00f7bcff has its CatchHandler @ 00f7c77c */
                    main_AppData__Draw(param_1);
                    /* try { // try from 00f7bd00 to 00f7bd0f has its CatchHandler @ 00f7c778 */
                    uVar21 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar8,0x100000,0);
                    if ((uVar21 & 1) != 0) {
                      *(undefined4 *)(param_1 + 0xac) = 1;
                    }
                  }
                  else if (*(int *)(param_1 + 0xac) == 1) {
                    /* try { // try from 00f7bc94 to 00f7bc9b has its CatchHandler @ 00f7c6d4 */
                    main_AppData__Draw(param_1);
                    if (param_3 == 0) {
                    /* try { // try from 00f7be18 to 00f7be37 has its CatchHandler @ 00f7c504 */
                      lVar8 = kairo_unity_io_RecordStore__OpenRecordStore(0,0);
                      lVar10 = *(long *)puVar3;
                      if (*(int *)(lVar10 + 0xe0) == 0) {
                        thunk_FUN_00df405c();
                        lVar10 = *(long *)puVar3;
                      }
                    /* try { // try from 00f7be48 to 00f7be67 has its CatchHandler @ 00f7c510 */
                      lVar10 = kairo_unity_io_RecordStore__ReadRecord
                                         (0,*(int *)(*(long *)(lVar10 + 0xb8) + 200) + 1,0);
                      if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3d4 to 00f7c3d7 has its CatchHandler @ 00f7c510 */
                        FUN_00db0de4();
                      }
                      kairo_unity_io_RecordStore__CloseRecordStore(lVar8,0);
                    }
                    else if (param_3 == 2) {
                    /* try { // try from 00f7bd50 to 00f7bd5b has its CatchHandler @ 00f7c4fc */
                      uVar9 = System_String__Concat
                                        (uVar9,*(undefined8 *)PTR_StringLiteral_58_01fc33f8,0);
                    /* try { // try from 00f7bd60 to 00f7bd6b has its CatchHandler @ 00f7c4e4 */
                      uVar7 = kairo_unity_io_ScratchPad__GetSPSize(0,0);
                    /* try { // try from 00f7bd70 to 00f7bd7f has its CatchHandler @ 00f7c4dc */
                      lVar8 = kairo_unity_io_ScratchPad__ReadByteArray(0,0,uVar7,0);
                    /* try { // try from 00f7bd84 to 00f7bd8f has its CatchHandler @ 00f7c4d8 */
                      uVar7 = kairo_unity_io_ScratchPad__GetSPSize(1,0);
                    /* try { // try from 00f7bd94 to 00f7bda3 has its CatchHandler @ 00f7c4d4 */
                      lVar18 = kairo_unity_io_ScratchPad__ReadByteArray(1,0,uVar7,0);
                      if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3dc to 00f7c3df has its CatchHandler @ 00f7c4d0 */
                        FUN_00db0de4();
                      }
                      if (lVar18 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3e4 to 00f7c3e7 has its CatchHandler @ 00f7c4cc */
                        FUN_00db0de4();
                      }
                    /* try { // try from 00f7bdc8 to 00f7bdcb has its CatchHandler @ 00f7c4c8 */
                      lVar10 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,
                                            *(int *)(lVar18 + 0x18) + *(int *)(lVar8 + 0x18));
                    /* try { // try from 00f7bdd4 to 00f7bdeb has its CatchHandler @ 00f7c4c4 */
                      java_lang_JSystem__Arraycopy(lVar8,0,lVar10,0,*(undefined4 *)(lVar8 + 0x18),0)
                      ;
                    /* try { // try from 00f7bdf4 to 00f7be07 has its CatchHandler @ 00f7c4c0 */
                      java_lang_JSystem__Arraycopy
                                (lVar18,0,lVar10,*(undefined4 *)(lVar8 + 0x18),
                                 *(undefined4 *)(lVar18 + 0x18),0);
                      puVar23 = (undefined8 *)PTR_StringLiteral_927_01fbff50;
                    }
                    else if (param_3 == 1) {
                    /* try { // try from 00f7bcbc to 00f7bcc7 has its CatchHandler @ 00f7c500 */
                      uVar9 = System_String__Concat
                                        (uVar9,*(undefined8 *)PTR_StringLiteral_73_01fc33f0,0);
                    /* try { // try from 00f7bccc to 00f7bcd7 has its CatchHandler @ 00f7c4f4 */
                      uVar7 = kairo_unity_io_ScratchPad__GetSPSize(0,0);
                    /* try { // try from 00f7bcdc to 00f7bceb has its CatchHandler @ 00f7c4e0 */
                      lVar10 = kairo_unity_io_ScratchPad__ReadByteArray(0,0,uVar7,0);
                    }
                    else {
                      lVar10 = 0;
                    }
                    lVar8 = *(long *)puVar3;
                    if (*(int *)(lVar8 + 0xe0) == 0) {
                    /* try { // try from 00f7be7c to 00f7be7f has its CatchHandler @ 00f7c6d4 */
                      thunk_FUN_00df405c();
                      lVar8 = *(long *)puVar3;
                    }
                    uVar20 = *(undefined8 *)(*(long *)(lVar8 + 0xb8) + 0x28);
                    local_64 = 0x10d;
                    /* try { // try from 00f7be94 to 00f7be9f has its CatchHandler @ 00f7c6d0 */
                    uVar12 = System_Int32__ToString(&local_64,0);
                    /* try { // try from 00f7beb0 to 00f7bebb has its CatchHandler @ 00f7c6cc */
                    uVar12 = System_String__Concat
                                       (uVar20,*(undefined8 *)PTR_StringLiteral_8941_01fc33e8,uVar12
                                        ,0);
                    if (lVar10 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c36c to 00f7c36f has its CatchHandler @ 00f7c6c8 */
                      FUN_00db0de4();
                    }
                    /* try { // try from 00f7bef8 to 00f7befb has its CatchHandler @ 00f7c6c4 */
                    lVar8 = FUN_00db0c30(*(undefined8 *)PTR_byte_____TypeInfo_01fc00f8,
                                         (*(int *)(lVar10 + 0x18) + 0xc7ff) / 0xc800 + 1);
                    if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c374 to 00f7c377 has its CatchHandler @ 00f7c6c0 */
                      FUN_00db0de4();
                    }
                    /* try { // try from 00f7bf0c to 00f7bf0f has its CatchHandler @ 00f7c6bc */
                    lVar18 = FUN_00db0c30(*(undefined8 *)puVar5,*(undefined4 *)(lVar8 + 0x18));
                    if (lVar18 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c37c to 00f7c37f has its CatchHandler @ 00f7c6b8 */
                      FUN_00db0de4();
                    }
                    /* try { // try from 00f7bf28 to 00f7bf2b has its CatchHandler @ 00f7c6b4 */
                    lVar13 = FUN_00db0c30(*(undefined8 *)PTR_string___TypeInfo_01fbf2f8,
                                          *(undefined4 *)(lVar18 + 0x18));
                    puVar19 = (undefined8 *)PTR_StringLiteral_1_01fbf388;
                    if (*(long *)(param_1 + 0x50) != 0) {
                      lVar14 = *(long *)(*(long *)(param_1 + 0x50) + 0x30);
                      if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3c4 to 00f7c3c7 has its CatchHandler @ 00f7c50c */
                        FUN_00db0de4();
                      }
                      if (*(int *)(lVar14 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3cc to 00f7c3cf has its CatchHandler @ 00f7c508 */
                        FUN_00db0dec();
                      }
                      puVar19 = (undefined8 *)(lVar14 + 0x20);
                    }
                    /* try { // try from 00f7bf68 to 00f7bf73 has its CatchHandler @ 00f7c6b0 */
                    uVar9 = System_String__Concat
                                      (*puVar19,*(undefined8 *)PTR_StringLiteral_45_01fbf350,uVar9,0
                                      );
                    /* try { // try from 00f7bf74 to 00f7bf7b has its CatchHandler @ 00f7c6e4 */
                    uVar9 = java_lang_StringEx__GetBytes(uVar9,0);
                    iVar6 = *(int *)(lVar8 + 0x18);
                    if (iVar6 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c384 to 00f7c387 has its CatchHandler @ 00f7c6e4 */
                      FUN_00db0dec();
                    }
                    *(undefined8 *)(lVar8 + 0x20) = uVar9;
                    if (*(int *)(lVar18 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c38c to 00f7c38f has its CatchHandler @ 00f7c6ac */
                      FUN_00db0dec();
                    }
                    *(undefined8 *)(lVar18 + 0x20) = *(undefined8 *)PTR_StringLiteral_7956_01fc2ca0;
                    if (lVar13 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c394 to 00f7c39f has its CatchHandler @ 00f7c6e0 */
                      FUN_00db0de4();
                    }
                    if (*(int *)(lVar13 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
                      FUN_00db0dec();
                    }
                    *(undefined8 *)(lVar13 + 0x20) = *puVar23;
                    if (0 < iVar6 + -1) {
                      iVar22 = 0;
                      uVar21 = 0;
                      do {
                        iVar6 = *(int *)(lVar10 + 0x18) - iVar22;
                        if (0xc7ff < iVar6) {
                          iVar6 = 0xc800;
                        }
                    /* try { // try from 00f7bffc to 00f7c003 has its CatchHandler @ 00f7c71c */
                        uVar9 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar6);
                        uVar1 = uVar21 + 1;
                        if (*(uint *)(lVar8 + 0x18) <= uVar1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c35c to 00f7c35f has its CatchHandler @ 00f7c720 */
                          FUN_00db0dec();
                        }
                        *(undefined8 *)(lVar8 + 0x28 + uVar21 * 8) = uVar9;
                    /* try { // try from 00f7c01c to 00f7c033 has its CatchHandler @ 00f7c724 */
                        java_lang_JSystem__Arraycopy(lVar10,iVar22,uVar9,0,iVar6,0);
                        if (*(uint *)(lVar18 + 0x18) <= uVar1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c354 to 00f7c357 has its CatchHandler @ 00f7c728 */
                          FUN_00db0dec();
                        }
                        *(undefined8 *)(lVar18 + 0x28 + uVar21 * 8) =
                             *(undefined8 *)PTR_StringLiteral_8935_01fc2c90;
                        if (*(int *)(*(long *)PTR_java_lang_JString_TypeInfo_01fbf368 + 0xe0) == 0)
                        {
                    /* try { // try from 00f7c064 to 00f7c067 has its CatchHandler @ 00f7c710 */
                          thunk_FUN_00df405c();
                        }
                    /* try { // try from 00f7c068 to 00f7c073 has its CatchHandler @ 00f7c714 */
                        uVar9 = java_lang_JString__ValueOf(uVar21 & 0xffffffff,0);
                        if (*(uint *)(lVar13 + 0x18) <= uVar1) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c364 to 00f7c367 has its CatchHandler @ 00f7c718 */
                          FUN_00db0dec();
                        }
                        *(undefined8 *)(lVar13 + 0x28 + uVar21 * 8) = uVar9;
                        iVar22 = iVar6 + iVar22;
                        iVar6 = (int)*(undefined8 *)(lVar8 + 0x18);
                        uVar21 = uVar1;
                      } while ((long)uVar1 < (long)(iVar6 + -1));
                    }
                    if (0 < iVar6) {
                      uVar21 = 0;
                      do {
                    /* try { // try from 00f7c0dc to 00f7c0e3 has its CatchHandler @ 00f7c72c */
                        uVar9 = main_AppData__Draw(param_1);
                        if (*(uint *)(lVar18 + 0x18) <= uVar21) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c124 to 00f7c127 has its CatchHandler @ 00f7c140 */
                          FUN_00db0dec();
                        }
                        if (*(uint *)(lVar13 + 0x18) <= uVar21) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c12c to 00f7c12f has its CatchHandler @ 00f7c13c */
                          FUN_00db0dec();
                        }
                        if (*(uint *)(lVar8 + 0x18) <= uVar21) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c134 to 00f7c137 has its CatchHandler @ 00f7c150 */
                          FUN_00db0dec();
                        }
                    /* try { // try from 00f7c114 to 00f7c11f has its CatchHandler @ 00f7c150 */
                        main_AppData__Post(uVar9,uVar12,*(undefined8 *)(lVar18 + uVar21 * 8 + 0x20),
                                           *(undefined8 *)(lVar13 + uVar21 * 8 + 0x20),uVar11,
                                           *(undefined8 *)(lVar8 + uVar21 * 8 + 0x20));
                        uVar21 = uVar21 + 1;
                      } while ((long)uVar21 < (long)*(int *)(lVar8 + 0x18));
                    }
                    if (*(long *)(param_1 + 0x48) == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3a4 to 00f7c3a7 has its CatchHandler @ 00f7c6a8 */
                      FUN_00db0de4();
                    }
                    lVar8 = *(long *)(*(long *)(param_1 + 0x48) + 0x30);
                    if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3ac to 00f7c3b7 has its CatchHandler @ 00f7c70c */
                      FUN_00db0de4();
                    }
                    if (*(uint *)(lVar8 + 0x18) < 0xb) {
                    /* WARNING: Subroutine does not return */
                      FUN_00db0dec();
                    }
                    *(undefined8 *)(lVar8 + 0x70) = *(undefined8 *)PTR_StringLiteral_1_01fbf388;
                    /* try { // try from 00f7c2f4 to 00f7c2fb has its CatchHandler @ 00f7c70c */
                    main_AppData__SaveSystem(param_1);
                    /* try { // try from 00f7c308 to 00f7c327 has its CatchHandler @ 00f7c6dc */
                    lVar8 = thunk_FUN_00e11c14(*(undefined8 *)
                                                PTR_kairo_unity_ui_Dialog_TypeInfo_01fc0100);
                    kairo_unity_ui_Dialog___ctor
                              (lVar8,0,*(undefined8 *)PTR_StringLiteral_11559_01fc0148,0);
                    if (lVar8 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f7c3bc to 00f7c3bf has its CatchHandler @ 00f7c6d8 */
                      FUN_00db0de4();
                    }
                    /* try { // try from 00f7c338 to 00f7c343 has its CatchHandler @ 00f7c6d8 */
                    kairo_unity_ui_Dialog__SetText
                              (lVar8,*(undefined8 *)PTR_StringLiteral_12172_01fc2c88,0);
                    /* try { // try from 00f7c344 to 00f7c34f has its CatchHandler @ 00f7c74c */
                    kairo_unity_ui_Dialog__Show(lVar8,0);
                    return;
                  }
                  if (*(int *)(*(long *)PTR_java_lang_JThread_TypeInfo_01fbf2e0 + 0xe0) == 0) {
                    /* try { // try from 00f7bd30 to 00f7bd3f has its CatchHandler @ 00f7c77c */
                    thunk_FUN_00df405c();
                  }
                  java_lang_JThread__Sleep(100,0);
                } while( true );
              }
              goto LAB_00f7c900;
            }
          }
        }
        goto LAB_00f7c904;
      }
    }
LAB_00f7c900:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f7c904:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Draw
// Address: 00f7c94c
// ==========================================================================================

void main_AppData__Draw(long param_1)

{
  undefined *puVar1;
  undefined4 uVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  undefined8 uVar8;
  
  puVar1 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if ((DAT_020ff818 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_StringLiteral_12256_01fc2cd8);
    FUN_00db0bbc(PTR_StringLiteral_11830_01fc2ce0);
    FUN_00db0bbc(PTR_StringLiteral_11066_01fc2ce8);
    DAT_020ff818 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = kairo_unity_ui_Canvas__GetInstance(0);
  if (*(int *)(param_1 + 0xac) == 1) {
    if ((lVar4 != 0) && (lVar5 = kairo_unity_ui_Canvas__BeginPaint(lVar4,0), lVar5 != 0)) {
      lVar6 = kairo_unity_ui_Graphics__GetFont(lVar5,0,0);
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
      }
      uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,0x40,0);
      kairo_unity_ui_Graphics__SetColor(lVar5,uVar2,0);
      kairo_unity_ui_Graphics__FillRect(0,0,0x43700000,0x43700000,lVar5,0);
      uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(0xff,0xff,0xff,0);
      kairo_unity_ui_Graphics__SetColor(lVar5,uVar2,0);
      if (lVar6 != 0) {
        uVar8 = *(undefined8 *)PTR_StringLiteral_11066_01fc2ce8;
        iVar3 = kairo_unity_ui_Font__StringWidth(lVar6,uVar8,0);
        if (iVar3 < 0) {
          iVar3 = iVar3 + 1;
        }
        kairo_unity_ui_Graphics__DrawString((float)(0x78 - (iVar3 >> 1)),0x42c80000,lVar5,uVar8,0);
        uVar8 = *(undefined8 *)PTR_StringLiteral_12256_01fc2cd8;
        iVar3 = kairo_unity_ui_Font__StringWidth(lVar6,uVar8,0);
        if (iVar3 < 0) {
          iVar3 = iVar3 + 1;
        }
        kairo_unity_ui_Graphics__DrawString((float)(0x78 - (iVar3 >> 1)),0x42e80000,lVar5,uVar8,0);
        kairo_unity_ui_Canvas__EndPaint(lVar4,0);
        return;
      }
    }
  }
  else {
    if (*(int *)(param_1 + 0xac) != 0) {
      return;
    }
    if ((lVar4 != 0) && (lVar5 = kairo_unity_ui_Canvas__BeginPaint(lVar4,0), lVar5 != 0)) {
      lVar6 = kairo_unity_ui_Graphics__GetFont(lVar5,0,0);
      if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
      }
      uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,0x40,0);
      kairo_unity_ui_Graphics__SetColor(lVar5,uVar2,0);
      kairo_unity_ui_Graphics__FillRect(0,0,0x43700000,0x43700000,lVar5,0);
      uVar2 = kairo_unity_ui_Graphics__GetColorOfRGB(0xff,0xff,0xff,0);
      kairo_unity_ui_Graphics__SetColor(lVar5,uVar2,0);
      if (lVar6 != 0) {
        uVar8 = *(undefined8 *)PTR_StringLiteral_11830_01fc2ce0;
        iVar3 = kairo_unity_ui_Font__StringWidth(lVar6,uVar8,0);
        if (iVar3 < 0) {
          iVar3 = iVar3 + 1;
        }
        kairo_unity_ui_Graphics__DrawString((float)(0x78 - (iVar3 >> 1)),0x42c80000,lVar5,uVar8,0);
        kairo_unity_ui_Canvas__EndPaint(lVar4,0);
        uVar7 = kairo_unity_ui_Canvas__CheckKeyPulse(lVar4,0x100000,0);
        if ((uVar7 & 1) == 0) {
          return;
        }
        *(undefined4 *)(param_1 + 0xac) = 1;
        return;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Post
// Address: 00f7cc68
// ==========================================================================================

void main_AppData__Post(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                       undefined8 param_5,undefined8 param_6)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  
  puVar2 = PTR_string___TypeInfo_01fbf2f8;
  if ((DAT_020ff819 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_384_01fc2cf8);
    FUN_00db0bbc(PTR_StringLiteral_606_01fc0b78);
    FUN_00db0bbc(PTR_StringLiteral_396_01fc2d00);
    FUN_00db0bbc(PTR_StringLiteral_392_01fc2d08);
    DAT_020ff819 = 1;
  }
  lVar3 = FUN_00db0c30(*(undefined8 *)puVar2,8);
  if (lVar3 != 0) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if (((((uVar1 != 0) && (*(undefined8 *)(lVar3 + 0x20) = param_2, uVar1 != 1)) &&
         (*(undefined8 *)(lVar3 + 0x28) = *(undefined8 *)PTR_StringLiteral_392_01fc2d08, 2 < uVar1))
        && ((*(undefined8 *)(lVar3 + 0x30) = param_3, uVar1 != 3 &&
            (*(undefined8 *)(lVar3 + 0x38) = *(undefined8 *)PTR_StringLiteral_396_01fc2d00,
            4 < uVar1)))) &&
       ((*(undefined8 *)(lVar3 + 0x40) = param_4, uVar1 != 5 &&
        ((*(undefined8 *)(lVar3 + 0x48) = *(undefined8 *)PTR_StringLiteral_384_01fc2cf8, 6 < uVar1
         && (*(undefined8 *)(lVar3 + 0x50) = param_5,
            puVar2 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960, uVar1 != 7)))))) {
      *(undefined8 *)(lVar3 + 0x58) = *(undefined8 *)PTR_StringLiteral_606_01fc0b78;
      uVar4 = Method_System_String_Concat(lVar3,0);
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar2);
      }
      kairo_unity_io_Http__Connect(uVar4,param_6,1,0);
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__RemoveAllMenuForms
// Address: 00f7cde4
// ==========================================================================================

undefined8 main_AppData__RemoveAllMenuForms(void)

{
  byte bVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long *plVar5;
  ulong uVar6;
  
  if ((DAT_020ff81a & 1) == 0) {
    FUN_00db0bbc(PTR_form_SubForm_TypeInfo_01fbf300);
    DAT_020ff81a = 1;
  }
  lVar4 = form_FormManager__GetInstance();
  if (lVar4 != 0) {
    iVar3 = kairo_unity_form_FormManagerBase__GetFormsNum(lVar4,0);
    puVar2 = PTR_form_SubForm_TypeInfo_01fbf300;
    while( true ) {
      iVar3 = iVar3 + -1;
      if (iVar3 < 0) {
        return 1;
      }
      plVar5 = (long *)kairo_unity_form_FormManagerBase__GetForm(lVar4,iVar3,0);
      if (plVar5 == (long *)0x0) break;
      if (*(int *)(plVar5 + 2) == 4) {
        bVar1 = *(byte *)(*(long *)puVar2 + 0x130);
        if ((*(byte *)(*plVar5 + 0x130) < bVar1) ||
           (*(long *)(*(long *)(*plVar5 + 200) + (ulong)bVar1 * 8 + -8) != *(long *)puVar2)) {
                    /* WARNING: Subroutine does not return */
          FUN_00db1180(plVar5);
        }
        uVar6 = form_SubForm__IsMenu(plVar5,0);
        if ((uVar6 & 1) != 0) {
          kairo_unity_form_FormManagerBase__Pop(lVar4,plVar5,0);
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetIntArray
// Address: 00f7cecc
// ==========================================================================================

long main_AppData__GetIntArray(undefined8 param_1)

{
  uint uVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  ulong uVar6;
  
  puVar2 = PTR_StringLiteral_646_01fbf440;
  if ((DAT_020ff81b & 1) == 0) {
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    DAT_020ff81b = 1;
  }
  lVar4 = kairo_unity_util_StringUtil__Split(param_1,*(undefined8 *)puVar2,0);
  if ((lVar4 == 0) ||
     (lVar5 = FUN_00db0c30(*(undefined8 *)PTR_int___TypeInfo_01fbf560,*(undefined4 *)(lVar4 + 0x18))
     , lVar5 == 0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (0 < *(int *)(lVar5 + 0x18)) {
    uVar6 = 0;
    do {
      if (*(uint *)(lVar4 + 0x18) <= uVar6) {
LAB_00f7cfa4:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar3 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar4 + 0x20 + uVar6 * 8),0);
      uVar1 = *(uint *)(lVar5 + 0x18);
      if (uVar1 <= uVar6) goto LAB_00f7cfa4;
      *(undefined4 *)(lVar5 + 0x20 + uVar6 * 4) = uVar3;
      uVar6 = uVar6 + 1;
    } while ((long)uVar6 < (long)(int)uVar1);
  }
  return lVar5;
}



// ==========================================================================================
// Function: main_AppData__GetInt2Array
// Address: 00f7cfac
// ==========================================================================================

long main_AppData__GetInt2Array(undefined8 param_1)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  
  puVar2 = PTR_StringLiteral_371_01fbfc70;
  if ((DAT_020ff81c & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_int_____TypeInfo_01fbf5e8);
    FUN_00db0bbc(PTR_StringLiteral_371_01fbfc70);
    DAT_020ff81c = 1;
  }
  lVar3 = kairo_unity_util_StringUtil__Split(param_1,*(undefined8 *)puVar2,0);
  if ((lVar3 == 0) ||
     (lVar4 = FUN_00db0c30(*(undefined8 *)PTR_int_____TypeInfo_01fbf5e8,
                           *(undefined4 *)(lVar3 + 0x18)),
     puVar2 = PTR_main_AppData_TypeInfo_01fbf278, lVar4 == 0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (0 < *(int *)(lVar4 + 0x18)) {
    uVar6 = 0;
    do {
      if (*(uint *)(lVar3 + 0x18) <= uVar6) {
LAB_00f7d0b0:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar5 = *(undefined8 *)(lVar3 + 0x20 + uVar6 * 8);
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar5 = main_AppData__GetIntArray(uVar5);
      uVar1 = *(uint *)(lVar4 + 0x18);
      if (uVar1 <= uVar6) goto LAB_00f7d0b0;
      *(undefined8 *)(lVar4 + 0x20 + uVar6 * 8) = uVar5;
      uVar6 = uVar6 + 1;
    } while ((long)uVar6 < (long)(int)uVar1);
  }
  return lVar4;
}



// ==========================================================================================
// Function: main_AppData__BooleanToByteArray
// Address: 00f7d0b8
// ==========================================================================================

undefined8 main_AppData__BooleanToByteArray(undefined8 param_1,long param_2)

{
  undefined uVar1;
  undefined *puVar2;
  long *plVar3;
  undefined8 uVar4;
  ulong uVar5;
  ulong uVar6;
  
  puVar2 = PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8;
  if ((DAT_020ff81d & 1) == 0) {
    FUN_00db0bbc(PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8);
    FUN_00db0bbc(PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8);
    DAT_020ff81d = 1;
  }
  plVar3 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  java_io_ByteArrayOutputStream___ctor(plVar3,0);
  puVar2 = PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8;
  if (param_2 != 0) {
    if (*(int *)(*(long *)PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_util_StreamUtil__WriteInt(plVar3,*(undefined4 *)(param_2 + 0x18),0);
    if (0 < (int)*(ulong *)(param_2 + 0x18)) {
      uVar6 = 0;
      uVar5 = *(ulong *)(param_2 + 0x18) & 0xffffffff;
      do {
        if (uVar5 <= uVar6) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        uVar1 = *(undefined *)(param_2 + 0x20 + uVar6);
        if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        kairo_unity_util_StreamUtil__WriteByte(plVar3,uVar1,0);
        uVar5 = (ulong)*(uint *)(param_2 + 0x18);
        uVar6 = uVar6 + 1;
      } while ((long)uVar6 < (long)(int)*(uint *)(param_2 + 0x18));
    }
    if (plVar3 != (long *)0x0) {
      uVar4 = java_io_ByteArrayOutputStream__ToByteArray(plVar3,0);
      (**(code **)(*plVar3 + 0x188))(plVar3,*(undefined8 *)(*plVar3 + 400));
      return uVar4;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SbyteArrayToBoolean
// Address: 00f7d1d8
// ==========================================================================================

void main_AppData__SbyteArrayToBoolean(undefined8 param_1,undefined8 param_2)

{
  main_AppData__SbyteArrayToBoolean(param_1,param_2,0xffffffff);
  return;
}



// ==========================================================================================
// Function: main_AppData__SbyteArrayToBoolean
// Address: 00f7d1e0
// ==========================================================================================

long main_AppData__SbyteArrayToBoolean(undefined8 param_1,undefined8 param_2,uint param_3)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar5;
  uint uVar6;
  long *plVar7;
  long lVar8;
  ulong uVar9;
  ulong uVar10;
  
  puVar3 = PTR_java_io_ByteArrayInputStream_TypeInfo_01fbf640;
  puVar2 = PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8;
  if ((DAT_020ff81e & 1) == 0) {
    FUN_00db0bbc(PTR_bool___TypeInfo_01fc3418);
    FUN_00db0bbc(PTR_java_io_ByteArrayInputStream_TypeInfo_01fbf640);
    FUN_00db0bbc(PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8);
    DAT_020ff81e = 1;
  }
  puVar4 = PTR_bool___TypeInfo_01fc3418;
  plVar7 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  java_io_ByteArrayInputStream___ctor(plVar7,param_2,0);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_util_StreamUtil__ReadInt(plVar7,0);
  uVar1 = uVar6;
  if (param_3 != 0xffffffff) {
    uVar1 = param_3;
  }
  lVar8 = FUN_00db0c30(*(undefined8 *)puVar4,uVar1);
  if (0 < (int)uVar6) {
    if (lVar8 == 0) goto LAB_00f7d32c;
    uVar9 = *(ulong *)(lVar8 + 0x18);
    uVar10 = 0;
    do {
      if ((long)(int)uVar9 <= (long)uVar10) break;
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      cVar5 = kairo_unity_util_StreamUtil__ReadByte(plVar7,0);
      uVar9 = (ulong)*(uint *)(lVar8 + 0x18);
      if (uVar9 <= uVar10) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(bool *)(lVar8 + 0x20 + uVar10) = cVar5 == '\x01';
      uVar10 = uVar10 + 1;
    } while (uVar6 != uVar10);
  }
  if (plVar7 != (long *)0x0) {
    (**(code **)(*plVar7 + 0x198))(plVar7,*(undefined8 *)(*plVar7 + 0x1a0));
    return lVar8;
  }
LAB_00f7d32c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__IntToByteArray
// Address: 00f7d330
// ==========================================================================================

undefined8 main_AppData__IntToByteArray(undefined8 param_1,long param_2)

{
  undefined4 uVar1;
  undefined *puVar2;
  long *plVar3;
  undefined8 uVar4;
  ulong uVar5;
  ulong uVar6;
  
  puVar2 = PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8;
  if ((DAT_020ff81f & 1) == 0) {
    FUN_00db0bbc(PTR_java_io_ByteArrayOutputStream_TypeInfo_01fbf3f8);
    FUN_00db0bbc(PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8);
    DAT_020ff81f = 1;
  }
  plVar3 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  java_io_ByteArrayOutputStream___ctor(plVar3,0);
  puVar2 = PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8;
  if (param_2 != 0) {
    if (*(int *)(*(long *)PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_util_StreamUtil__WriteInt(plVar3,*(undefined4 *)(param_2 + 0x18),0);
    if (0 < (int)*(ulong *)(param_2 + 0x18)) {
      uVar6 = 0;
      uVar5 = *(ulong *)(param_2 + 0x18) & 0xffffffff;
      do {
        if (uVar5 <= uVar6) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        uVar1 = *(undefined4 *)(param_2 + 0x20 + uVar6 * 4);
        if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        kairo_unity_util_StreamUtil__WriteInt(plVar3,uVar1,0);
        uVar5 = (ulong)*(uint *)(param_2 + 0x18);
        uVar6 = uVar6 + 1;
      } while ((long)uVar6 < (long)(int)*(uint *)(param_2 + 0x18));
    }
    if (plVar3 != (long *)0x0) {
      uVar4 = java_io_ByteArrayOutputStream__ToByteArray(plVar3,0);
      (**(code **)(*plVar3 + 0x188))(plVar3,*(undefined8 *)(*plVar3 + 400));
      return uVar4;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__SbyteArrayToInt
// Address: 00f7d450
// ==========================================================================================

void main_AppData__SbyteArrayToInt(undefined8 param_1,undefined8 param_2)

{
  main_AppData__SbyteArrayToInt(param_1,param_2,0xffffffff);
  return;
}



// ==========================================================================================
// Function: main_AppData__SbyteArrayToInt
// Address: 00f7d458
// ==========================================================================================

long main_AppData__SbyteArrayToInt(undefined8 param_1,undefined8 param_2,uint param_3)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  uint uVar5;
  undefined4 uVar6;
  long *plVar7;
  long lVar8;
  ulong uVar9;
  ulong uVar10;
  
  puVar4 = PTR_java_io_ByteArrayInputStream_TypeInfo_01fbf640;
  puVar2 = PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8;
  if ((DAT_020ff820 & 1) == 0) {
    FUN_00db0bbc(PTR_java_io_ByteArrayInputStream_TypeInfo_01fbf640);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_kairo_unity_util_StreamUtil_TypeInfo_01fbf3e8);
    DAT_020ff820 = 1;
  }
  puVar3 = PTR_int___TypeInfo_01fbf560;
  plVar7 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  java_io_ByteArrayInputStream___ctor(plVar7,param_2,0);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = kairo_unity_util_StreamUtil__ReadInt(plVar7,0);
  uVar1 = uVar5;
  if (param_3 != 0xffffffff) {
    uVar1 = param_3;
  }
  lVar8 = FUN_00db0c30(*(undefined8 *)puVar3,uVar1);
  if (0 < (int)uVar5) {
    if (lVar8 == 0) goto LAB_00f7d598;
    uVar9 = *(ulong *)(lVar8 + 0x18);
    uVar10 = 0;
    do {
      if ((long)(int)uVar9 <= (long)uVar10) break;
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar6 = kairo_unity_util_StreamUtil__ReadInt(plVar7,0);
      uVar9 = (ulong)*(uint *)(lVar8 + 0x18);
      if (uVar9 <= uVar10) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      *(undefined4 *)(lVar8 + 0x20 + uVar10 * 4) = uVar6;
      uVar10 = uVar10 + 1;
    } while (uVar5 != uVar10);
  }
  if (plVar7 != (long *)0x0) {
    (**(code **)(*plVar7 + 0x198))(plVar7,*(undefined8 *)(*plVar7 + 0x1a0));
    return lVar8;
  }
LAB_00f7d598:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__FrameToMilliSecond
// Address: 00f7d59c
// ==========================================================================================

int main_AppData__FrameToMilliSecond(undefined8 param_1,int param_2)

{
  return (param_2 * 1000) / 0x14;
}



// ==========================================================================================
// Function: main_AppData__SearchInteger
// Address: 00f7d5c0
// ==========================================================================================

long main_AppData__SearchInteger(long param_1,int param_2)

{
  uint uVar1;
  long lVar2;
  
  if ((param_1 != 0) && (uVar1 = *(uint *)(param_1 + 0x18), 0 < (int)uVar1)) {
    lVar2 = 0;
    do {
      if (uVar1 <= (uint)lVar2) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      if (*(int *)(param_1 + 0x20 + lVar2 * 4) == param_2) {
        return lVar2;
      }
      lVar2 = lVar2 + 1;
    } while ((int)lVar2 < (int)uVar1);
  }
  return 0xffffffff;
}



// ==========================================================================================
// Function: main_AppData__DrawCommand
// Address: 00f7d610
// ==========================================================================================

void main_AppData__DrawCommand
               (undefined8 param_1,undefined8 param_2,long param_3,long param_4,undefined8 param_5,
               undefined4 param_6,uint param_7,int param_8)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  uint uVar5;
  undefined *puVar6;
  undefined4 uVar7;
  long lVar8;
  long lVar9;
  float fVar10;
  undefined8 uVar11;
  float fVar12;
  
  if ((DAT_020ff821 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff821 = 1;
  }
  if ((param_4 != 0) &&
     (lVar8 = kairo_unity_ui_Graphics__GetFont(param_4,0,0),
     puVar6 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590, lVar8 != 0)) {
    uVar11 = kairo_unity_ui_Font__StringWidthF(lVar8,param_5,0);
    iVar2 = *(int *)(lVar8 + 0x1c);
    if (*(int *)(*(long *)puVar6 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar8 = kairo_unity_ui_Graphics__GetAnchorPositionF
                      (param_1,param_2,uVar11,(float)iVar2,param_6,0);
    uVar3 = *(undefined4 *)(param_4 + 0x58);
    fVar12 = (float)uVar11;
    if ((param_7 & 1) == 0) {
      kairo_unity_ui_Graphics__SetColor(param_4,uVar3,0);
      if (lVar8 == 0) goto LAB_00f7d870;
    }
    else {
      if (*(int *)(*(long *)puVar6 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar7 = kairo_unity_ui_Graphics__GetColorOfRGB(0xaf,0xaf,0xff,0);
      kairo_unity_ui_Graphics__SetColor(param_4,uVar7,0);
      if (lVar8 == 0) goto LAB_00f7d870;
      if ((*(int *)(lVar8 + 0x18) == 1) || (*(int *)(lVar8 + 0x18) == 0)) goto LAB_00f7d86c;
      kairo_unity_ui_Graphics__FillRect
                (*(float *)(lVar8 + 0x20) - (float)param_8,*(float *)(lVar8 + 0x24) + -1.0,
                 fVar12 + (float)(param_8 << 1),(float)(iVar2 + 2),param_4,0);
      kairo_unity_ui_Graphics__SetColor(param_4,uVar3,0);
    }
    if ((*(int *)(lVar8 + 0x18) != 0) && (*(int *)(lVar8 + 0x18) != 1)) {
      kairo_unity_ui_Graphics__DrawString
                (*(undefined4 *)(lVar8 + 0x20),*(undefined4 *)(lVar8 + 0x24),param_4,param_5,0);
      uVar4 = *(uint *)(lVar8 + 0x18);
      if (uVar4 != 0) {
        lVar9 = *(long *)(param_3 + 0xb0);
        if (lVar9 == 0) goto LAB_00f7d870;
        uVar5 = *(uint *)(lVar9 + 0x18);
        if (uVar5 != 0) {
          fVar10 = *(float *)(lVar8 + 0x20) - (float)param_8;
          iVar1 = -0x80000000;
          if (fVar10 != INFINITY) {
            iVar1 = (int)fVar10;
          }
          *(int *)(lVar9 + 0x20) = iVar1;
          if ((1 < uVar4) && (1 < uVar5)) {
            fVar10 = *(float *)(lVar8 + 0x24) + -1.0;
            iVar1 = -0x80000000;
            if (fVar10 != INFINITY) {
              iVar1 = (int)fVar10;
            }
            *(int *)(lVar9 + 0x24) = iVar1;
            if (uVar5 != 2) {
              iVar1 = -0x80000000;
              if (fVar12 != INFINITY) {
                iVar1 = (int)fVar12;
              }
              *(int *)(lVar9 + 0x28) = iVar1 + param_8 * 2;
              if (3 < uVar5) {
                *(int *)(lVar9 + 0x2c) = iVar2 + 2;
                return;
              }
            }
          }
        }
      }
    }
LAB_00f7d86c:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f7d870:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawCommand
// Address: 00f7d874
// ==========================================================================================

void main_AppData__DrawCommand
               (undefined8 param_1,undefined8 param_2,long param_3,long param_4,undefined8 param_5,
               undefined4 param_6,uint param_7,int param_8)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  undefined *puVar5;
  undefined4 uVar6;
  long lVar7;
  ulong uVar8;
  long lVar9;
  int iVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  undefined8 uVar14;
  float fVar15;
  long param_10;
  
  if ((DAT_020ff822 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    DAT_020ff822 = 1;
  }
  puVar5 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if (param_4 == 0) goto LAB_00f7dc08;
  lVar7 = kairo_unity_ui_Graphics__GetFont(param_4,0,0);
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar5);
  }
  uVar8 = kairo_unity_util_Language__Japanese(0);
  if ((param_10 == 0) || ((uVar8 & 1) != 0)) {
    if (lVar7 == 0) goto LAB_00f7dc08;
    uVar14 = kairo_unity_ui_Font__StringWidthF(lVar7,param_5,0);
    fVar12 = 0.0;
    fVar11 = 0.0;
  }
  else {
    iVar1 = *(int *)(param_10 + 0x10);
    if (iVar1 == -1) {
LAB_00f7d948:
      iVar10 = -1;
    }
    else {
      if (lVar7 == 0) goto LAB_00f7dc08;
      iVar10 = *(int *)(lVar7 + 0x10);
      if (iVar1 == iVar10) goto LAB_00f7d948;
      kairo_unity_ui_Font__SetSize(lVar7,iVar1,1,0);
    }
    fVar11 = (float)kairo_unity_ui_TextFormat__GetX(param_1,param_10,0);
    fVar12 = (float)kairo_unity_ui_TextFormat__GetY(param_2,param_10,0);
    if (lVar7 == 0) goto LAB_00f7dc08;
    fVar11 = fVar11 - (float)param_1;
    fVar12 = fVar12 - (float)param_2;
    uVar14 = kairo_unity_ui_Font__StringWidthF(lVar7,param_5,0);
    if (iVar10 != -1) {
      kairo_unity_ui_Font__SetSize(lVar7,iVar10,1,0);
    }
  }
  puVar5 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  iVar1 = *(int *)(lVar7 + 0x1c);
  if (*(int *)(*(long *)PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar7 = kairo_unity_ui_Graphics__GetAnchorPositionF(param_1,param_2,uVar14,(float)iVar1,param_6,0)
  ;
  uVar2 = *(undefined4 *)(param_4 + 0x58);
  fVar15 = (float)uVar14;
  if ((param_7 & 1) == 0) {
    kairo_unity_ui_Graphics__SetColor(param_4,uVar2,0);
    if (lVar7 == 0) goto LAB_00f7dc08;
  }
  else {
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0xaf,0xaf,0xff,0);
    kairo_unity_ui_Graphics__SetColor(param_4,uVar6,0);
    if (lVar7 == 0) goto LAB_00f7dc08;
    if ((*(int *)(lVar7 + 0x18) == 1) || (*(int *)(lVar7 + 0x18) == 0)) goto LAB_00f7dc04;
    fVar13 = -2.147484e+09;
    if (fVar11 != INFINITY) {
      fVar13 = (float)(int)fVar11;
    }
    fVar11 = -2.147484e+09;
    if (fVar12 != INFINITY) {
      fVar11 = (float)(int)fVar12;
    }
    kairo_unity_ui_Graphics__FillRect
              (fVar13 + (*(float *)(lVar7 + 0x20) - (float)param_8),
               fVar11 + *(float *)(lVar7 + 0x24) + -1.0,fVar15 + (float)(param_8 << 1),
               (float)(iVar1 + 2),param_4,0);
    kairo_unity_ui_Graphics__SetColor(param_4,uVar2,0);
  }
  if ((*(int *)(lVar7 + 0x18) != 0) && (*(int *)(lVar7 + 0x18) != 1)) {
    kairo_unity_ui_Graphics__DrawString
              (*(undefined4 *)(lVar7 + 0x20),*(undefined4 *)(lVar7 + 0x24),param_4,param_10,param_5,
               0);
    uVar3 = *(uint *)(lVar7 + 0x18);
    if (uVar3 != 0) {
      lVar9 = *(long *)(param_3 + 0xb0);
      if (lVar9 == 0) {
LAB_00f7dc08:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      uVar4 = *(uint *)(lVar9 + 0x18);
      if (uVar4 != 0) {
        fVar11 = *(float *)(lVar7 + 0x20) - (float)param_8;
        iVar10 = -0x80000000;
        if (fVar11 != INFINITY) {
          iVar10 = (int)fVar11;
        }
        *(int *)(lVar9 + 0x20) = iVar10;
        if ((1 < uVar3) && (1 < uVar4)) {
          fVar11 = *(float *)(lVar7 + 0x24) + -1.0;
          iVar10 = -0x80000000;
          if (fVar11 != INFINITY) {
            iVar10 = (int)fVar11;
          }
          *(int *)(lVar9 + 0x24) = iVar10;
          if (uVar4 != 2) {
            iVar10 = -0x80000000;
            if (fVar15 != INFINITY) {
              iVar10 = (int)fVar15;
            }
            *(int *)(lVar9 + 0x28) = iVar10 + param_8 * 2;
            if (3 < uVar4) {
              *(int *)(lVar9 + 0x2c) = iVar1 + 2;
              return;
            }
          }
        }
      }
    }
  }
LAB_00f7dc04:
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: main_AppData__DrawCommand
// Address: 00f7dc0c
// ==========================================================================================

void main_AppData__DrawCommand
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,long param_4,long param_5,
               undefined8 param_6,undefined4 param_7,uint param_8)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  undefined *puVar5;
  undefined4 uVar6;
  long lVar7;
  long lVar8;
  float fVar9;
  undefined8 uVar10;
  float fVar11;
  
  if ((DAT_020ff823 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    DAT_020ff823 = 1;
  }
  if ((param_5 != 0) &&
     (lVar7 = kairo_unity_ui_Graphics__GetFont(param_5,0,0),
     puVar5 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590, lVar7 != 0)) {
    iVar2 = *(int *)(lVar7 + 0x1c);
    uVar10 = kairo_unity_ui_Font__StringWidthF(lVar7,param_6,0);
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar7 = kairo_unity_ui_Graphics__GetAnchorPositionF
                      (param_1,param_2,uVar10,(float)iVar2,param_7,0);
    uVar3 = *(undefined4 *)(param_5 + 0x58);
    fVar11 = (float)param_3;
    if ((param_8 & 1) == 0) {
      kairo_unity_ui_Graphics__SetColor(param_5,uVar3,0);
      if (lVar7 == 0) goto LAB_00f7de5c;
    }
    else {
      if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar6 = kairo_unity_ui_Graphics__GetColorOfRGB(0xaf,0xaf,0xff,0);
      kairo_unity_ui_Graphics__SetColor(param_5,uVar6,0);
      if (lVar7 == 0) goto LAB_00f7de5c;
      if (*(uint *)(lVar7 + 0x18) < 2) goto LAB_00f7de58;
      kairo_unity_ui_Graphics__FillRect
                ((float)param_1 + fVar11 * -0.5,*(float *)(lVar7 + 0x24) + -1.0,param_3,
                 (float)(iVar2 + 2),param_5,0);
      kairo_unity_ui_Graphics__SetColor(param_5,uVar3,0);
    }
    if ((*(int *)(lVar7 + 0x18) != 1) && (*(int *)(lVar7 + 0x18) != 0)) {
      kairo_unity_ui_Graphics__DrawString
                (*(undefined4 *)(lVar7 + 0x20),*(undefined4 *)(lVar7 + 0x24),param_5,param_6,0);
      lVar8 = *(long *)(param_4 + 0xb0);
      if (lVar8 == 0) goto LAB_00f7de5c;
      uVar4 = *(uint *)(lVar8 + 0x18);
      if (uVar4 != 0) {
        fVar9 = (float)param_1 + fVar11 * -0.5;
        iVar1 = -0x80000000;
        if (fVar9 != INFINITY) {
          iVar1 = (int)fVar9;
        }
        *(int *)(lVar8 + 0x20) = iVar1;
        if ((1 < *(uint *)(lVar7 + 0x18)) && (1 < uVar4)) {
          fVar9 = *(float *)(lVar7 + 0x24) + -1.0;
          iVar1 = -0x80000000;
          if (fVar9 != INFINITY) {
            iVar1 = (int)fVar9;
          }
          *(int *)(lVar8 + 0x24) = iVar1;
          if (uVar4 != 2) {
            iVar1 = -0x80000000;
            if (fVar11 != INFINITY) {
              iVar1 = (int)fVar11;
            }
            *(int *)(lVar8 + 0x28) = iVar1;
            if (3 < uVar4) {
              *(int *)(lVar8 + 0x2c) = iVar2 + 2;
              return;
            }
          }
        }
      }
    }
LAB_00f7de58:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f7de5c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetEvenlyDivisionArea
// Address: 00f7de60
// ==========================================================================================

void main_AppData__GetEvenlyDivisionArea
               (long param_1,int param_2,int param_3,int param_4,int param_5,int param_6)

{
  int iVar1;
  long lVar2;
  
  lVar2 = *(long *)(param_1 + 0xb8);
  if (lVar2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(int *)(lVar2 + 0x18) != 0) {
    iVar1 = 0;
    if (param_6 != 0) {
      iVar1 = ((param_3 - param_2) + (1 - param_6) * param_4) / param_6;
    }
    param_2 = param_2 + (iVar1 + param_4) * param_5;
    *(int *)(lVar2 + 0x20) = param_2;
    if (*(int *)(lVar2 + 0x18) != 1) {
      *(int *)(lVar2 + 0x24) = param_2 + iVar1;
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: main_AppData__BeginTempRender
// Address: 00f7deb4
// ==========================================================================================

long main_AppData__BeginTempRender(long param_1,long param_2)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  
  puVar1 = PTR_surface_GameView_TypeInfo_01fbf588;
  if ((DAT_020ff824 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    FUN_00db0bbc(PTR_UnityEngine_Texture2D_TypeInfo_01fc3420);
    DAT_020ff824 = 1;
  }
  *(undefined8 *)(param_1 + 0xd0) = 0;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar4 = surface_GameView__GetInstance(0);
  if (lVar4 != 0) {
    iVar2 = surface_GameView__GetSideSoftWidth(lVar4,0);
    iVar3 = surface_GameView__GetGameWidth(lVar4,0);
    iVar2 = iVar2 * 2 + 0xf0;
    if (iVar2 <= iVar3) {
      return param_2;
    }
    *(long *)(param_1 + 0xd0) = param_2;
    iVar3 = surface_GameView__GetGameHeight(lVar4,0);
    lVar4 = *(long *)(param_1 + 0xc0);
    if (lVar4 != 0) {
      if ((*(int *)(lVar4 + 0x28) < iVar2) || (*(int *)(lVar4 + 0x2c) < iVar3)) {
        kairo_unity_ui_Image__Dispose(lVar4,0);
        if (*(long *)(param_1 + 200) == 0) goto LAB_00f7e058;
        kairo_unity_ui_Graphics__Dispose(*(long *)(param_1 + 200),0,0);
        if (*(long *)(param_1 + 0xc0) == 0) goto LAB_00f7e058;
        uVar5 = kairo_unity_ui_Image__GetGraphics(*(long *)(param_1 + 0xc0),0);
        *(undefined8 *)(param_1 + 200) = uVar5;
        if (*(long *)(param_1 + 0xc0) == 0) goto LAB_00f7e058;
      }
      puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
      lVar4 = *(long *)PTR_main_AppData_TypeInfo_01fbf278;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar1;
      }
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 8);
      if (((lVar4 != 0) && (kairo_unity_ui_Canvas__BeginPaint(lVar4,0), param_2 != 0)) &&
         (*(long *)(param_1 + 200) != 0)) {
        kairo_unity_ui_Graphics__SetColor
                  (*(long *)(param_1 + 200),*(undefined4 *)(param_2 + 0x58),0);
        lVar4 = *(long *)(param_1 + 200);
        iVar2 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
        iVar3 = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
        if (lVar4 != 0) {
          kairo_unity_ui_Graphics__SetOrigin((float)iVar2,(float)iVar3,lVar4,0);
          return *(long *)(param_1 + 200);
        }
      }
    }
  }
LAB_00f7e058:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__EndTempRender
// Address: 00f7e05c
// ==========================================================================================

long main_AppData__EndTempRender(long param_1,long param_2,int param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  long lVar8;
  long lVar9;
  undefined8 uVar10;
  
  if ((DAT_020ff825 & 1) == 0) {
    FUN_00db0bbc(PTR_surface_GameView_TypeInfo_01fbf588);
    DAT_020ff825 = 1;
  }
  if (*(long *)(param_1 + 0xd0) == 0) {
    return param_2;
  }
  if (*(int *)(*(long *)PTR_surface_GameView_TypeInfo_01fbf588 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar8 = surface_GameView__GetInstance(0);
  if (lVar8 != 0) {
    iVar1 = surface_GameView__GetSideSoftWidth(lVar8,0);
    if (*(long *)(param_1 + 0xd0) != 0) {
      iVar2 = kairo_unity_ui_Graphics__GetOriginX(*(long *)(param_1 + 0xd0),0);
      lVar9 = *(long *)(param_1 + 0xd0);
      uVar10 = *(undefined8 *)(param_1 + 0xc0);
      iVar3 = surface_GameView__GetGameHeight(lVar8,0);
      iVar4 = surface_GameView__GetGameWidth(lVar8,0);
      if (param_2 != 0) {
        iVar5 = kairo_unity_ui_Graphics__GetOriginX(param_2,0);
        iVar6 = surface_GameView__GetGameHeight(lVar8,0);
        iVar7 = kairo_unity_ui_Graphics__GetOriginY(param_2,0);
        if (lVar9 != 0) {
          kairo_unity_ui_Graphics__DrawScaledImage
                    ((float)(iVar1 - iVar2),(float)(iVar3 - param_3),(float)(iVar4 + iVar1 * -2),
                     (float)param_3,lVar9,uVar10,iVar5 + (iVar1 - iVar2),(iVar6 - param_3) + iVar7,
                     0xf0,param_3,0);
          lVar8 = *(long *)(param_1 + 0xd0);
          *(undefined8 *)(param_1 + 0xd0) = 0;
          return lVar8;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSebScale
// Address: 00f7e1c0
// ==========================================================================================

void main_AppData__DrawSebScale
               (undefined8 param_1,long param_2,int param_3,int param_4,long param_5,
               undefined4 param_6,int param_7,int param_8)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  long lVar6;
  int iVar7;
  long lVar8;
  uint uVar9;
  
  if (param_5 != 0) {
    lVar4 = kairo_unity_ui_Seb__GetManager(param_5,0);
    lVar5 = kairo_unity_ui_Seb__GetSprites(param_5,param_6,0);
    if (lVar5 != 0) {
      uVar1 = *(uint *)(lVar5 + 0x18);
      if (0 < (int)uVar1) {
        uVar9 = 0;
        do {
          if (uVar1 <= uVar9) {
LAB_00f7e310:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar6 = *(long *)(lVar5 + (long)(int)uVar9 * 8 + 0x20);
          if (lVar6 == 0) goto LAB_00f7e314;
          uVar1 = *(uint *)(lVar6 + 0x18);
          if (uVar1 < 2) goto LAB_00f7e310;
          uVar2 = *(uint *)(lVar6 + 0x24);
          if (-1 < (int)uVar2) {
            iVar7 = param_7;
            if (param_7 == -1) {
              if (uVar1 < 5) goto LAB_00f7e310;
              iVar7 = *(int *)(lVar6 + 0x30);
            }
            iVar3 = param_8;
            if (param_8 == -1) {
              if (uVar1 < 6) goto LAB_00f7e310;
              iVar3 = *(int *)(lVar6 + 0x34);
            }
            if ((lVar4 == 0) || (lVar8 = *(long *)(lVar4 + 0x10), lVar8 == 0)) goto LAB_00f7e314;
            if ((*(uint *)(lVar8 + 0x18) <= uVar2) || ((uVar1 < 7 || (uVar1 == 7))))
            goto LAB_00f7e310;
            if (param_2 == 0) goto LAB_00f7e314;
            kairo_unity_ui_Graphics__DrawScaledImage
                      ((float)(*(int *)(lVar6 + 0x38) + param_3),
                       (float)(*(int *)(lVar6 + 0x3c) + param_4),(float)iVar7,(float)iVar3,param_2,
                       *(undefined8 *)(lVar8 + (ulong)uVar2 * 8 + 0x20),
                       *(undefined4 *)(lVar6 + 0x28),*(undefined4 *)(lVar6 + 0x2c),
                       *(undefined4 *)(lVar6 + 0x30),*(undefined4 *)(lVar6 + 0x34),0);
          }
          uVar1 = *(uint *)(lVar5 + 0x18);
          uVar9 = uVar9 + 1;
        } while ((int)uVar9 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7e314:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSebScale
// Address: 00f7e318
// ==========================================================================================

void main_AppData__DrawSebScale
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               long param_7,undefined4 param_8,int param_9,int param_10,int param_11,int param_12)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  int iVar10;
  int iVar11;
  long lVar12;
  uint uVar13;
  
  if (param_7 != 0) {
    lVar7 = kairo_unity_ui_Seb__GetManager(param_7,0);
    lVar8 = kairo_unity_ui_Seb__GetSprites(param_7,param_8,0);
    if (lVar8 != 0) {
      uVar1 = *(uint *)(lVar8 + 0x18);
      if (0 < (int)uVar1) {
        uVar13 = 0;
        do {
          if (uVar1 <= uVar13) {
LAB_00f7e4e4:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          lVar9 = *(long *)(lVar8 + (long)(int)uVar13 * 8 + 0x20);
          if (lVar9 == 0) goto LAB_00f7e4e8;
          uVar1 = *(uint *)(lVar9 + 0x18);
          if (uVar1 < 2) goto LAB_00f7e4e4;
          uVar2 = *(uint *)(lVar9 + 0x24);
          if (-1 < (int)uVar2) {
            iVar10 = param_5;
            if (param_5 == -1) {
              if (uVar1 < 5) goto LAB_00f7e4e4;
              iVar10 = *(int *)(lVar9 + 0x30);
            }
            iVar11 = param_6;
            if (param_6 == -1) {
              if (uVar1 < 6) goto LAB_00f7e4e4;
              iVar11 = *(int *)(lVar9 + 0x34);
            }
            iVar3 = param_9;
            if (param_9 == -1) {
              if (uVar1 < 3) goto LAB_00f7e4e4;
              iVar3 = *(int *)(lVar9 + 0x28);
            }
            iVar4 = param_10;
            if (param_10 == -1) {
              if (uVar1 < 4) goto LAB_00f7e4e4;
              iVar4 = *(int *)(lVar9 + 0x2c);
            }
            iVar5 = param_11;
            if (param_11 == -1) {
              if (uVar1 < 5) goto LAB_00f7e4e4;
              iVar5 = *(int *)(lVar9 + 0x30);
            }
            iVar6 = param_12;
            if (param_12 == -1) {
              if (uVar1 < 6) goto LAB_00f7e4e4;
              iVar6 = *(int *)(lVar9 + 0x34);
            }
            if ((lVar7 == 0) || (lVar12 = *(long *)(lVar7 + 0x10), lVar12 == 0)) goto LAB_00f7e4e8;
            if ((*(uint *)(lVar12 + 0x18) <= uVar2) || ((uVar1 < 7 || (uVar1 == 7))))
            goto LAB_00f7e4e4;
            if (param_2 == 0) goto LAB_00f7e4e8;
            kairo_unity_ui_Graphics__DrawScaledImage
                      ((float)(*(int *)(lVar9 + 0x38) + param_3),
                       (float)(*(int *)(lVar9 + 0x3c) + param_4),(float)iVar10,(float)iVar11,param_2
                       ,*(undefined8 *)(lVar12 + (ulong)uVar2 * 8 + 0x20),iVar3,iVar4,iVar5,iVar6,0)
            ;
          }
          uVar1 = *(uint *)(lVar8 + 0x18);
          uVar13 = uVar13 + 1;
        } while ((int)uVar13 < (int)uVar1);
      }
      return;
    }
  }
LAB_00f7e4e8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawSebScale
// Address: 00f7e4ec
// ==========================================================================================

void main_AppData__DrawSebScale
               (undefined8 param_1,long param_2,int param_3,int param_4,int param_5,int param_6,
               long param_7,undefined4 param_8,undefined4 param_9,int param_10,int param_11,
               int param_12,int param_13)

{
  uint uVar1;
  uint uVar2;
  long lVar3;
  long lVar4;
  
  if (param_7 != 0) {
    lVar3 = kairo_unity_ui_Seb__GetManager(param_7,0);
    kairo_unity_ui_Seb__GetSprites(param_7,param_8,0);
    lVar4 = kairo_unity_ui_Seb__GetSprite(param_7,param_8,param_9,0);
    if (lVar4 != 0) {
      uVar1 = *(uint *)(lVar4 + 0x18);
      if (uVar1 < 2) {
LAB_00f7e6ac:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar2 = *(uint *)(lVar4 + 0x24);
      if ((int)uVar2 < 0) {
        return;
      }
      if (param_5 == -1) {
        if (uVar1 < 5) goto LAB_00f7e6ac;
        param_5 = *(int *)(lVar4 + 0x30);
      }
      if (param_6 == -1) {
        if (uVar1 < 6) goto LAB_00f7e6ac;
        param_6 = *(int *)(lVar4 + 0x34);
      }
      if (param_10 == -1) {
        if (uVar1 < 3) goto LAB_00f7e6ac;
        param_10 = *(int *)(lVar4 + 0x28);
      }
      if (param_11 == -1) {
        if (uVar1 < 4) goto LAB_00f7e6ac;
        param_11 = *(int *)(lVar4 + 0x2c);
      }
      if (param_12 == -1) {
        if (uVar1 < 5) goto LAB_00f7e6ac;
        param_12 = *(int *)(lVar4 + 0x30);
      }
      if (param_13 == -1) {
        if (uVar1 < 6) goto LAB_00f7e6ac;
        param_13 = *(int *)(lVar4 + 0x34);
      }
      if ((lVar3 != 0) && (lVar3 = *(long *)(lVar3 + 0x10), lVar3 != 0)) {
        if ((*(uint *)(lVar3 + 0x18) <= uVar2) || ((uVar1 < 7 || (uVar1 == 7)))) goto LAB_00f7e6ac;
        if (param_2 != 0) {
          kairo_unity_ui_Graphics__DrawScaledImage
                    ((float)(*(int *)(lVar4 + 0x38) + param_3),
                     (float)(*(int *)(lVar4 + 0x3c) + param_4),(float)param_5,(float)param_6,param_2
                     ,*(undefined8 *)(lVar3 + (ulong)uVar2 * 8 + 0x20),param_10,param_11,param_12,
                     param_13,0);
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetImage
// Address: 00f7e6b4
// ==========================================================================================

undefined8 main_AppData__GetImage(long param_1,long param_2)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  ulong uVar4;
  undefined8 uVar5;
  long lVar6;
  uint uVar7;
  
  if ((DAT_020ff826 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_StringLiteral_7443_01fc3428);
    DAT_020ff826 = 1;
  }
  if ((*(long *)(param_1 + 0x38) != 0) &&
     (lVar6 = *(long *)(*(long *)(param_1 + 0x38) + 0x28), lVar6 != 0)) {
    if (*(int *)(lVar6 + 0x18) == 0) {
LAB_00f7e83c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar6 = *(long *)(lVar6 + 0x20);
    if (lVar6 != 0) {
      uVar1 = *(uint *)(lVar6 + 0x18);
      if (0 < (int)uVar1) {
        uVar7 = 0;
        do {
          if (uVar1 <= uVar7) goto LAB_00f7e83c;
          lVar3 = *(long *)(lVar6 + (long)(int)uVar7 * 8 + 0x20);
          if ((lVar3 == 0) || (lVar3 = System_String__Split(lVar3,0x2c,0,0), lVar3 == 0))
          goto LAB_00f7e838;
          if (*(int *)(lVar3 + 0x18) == 0) goto LAB_00f7e83c;
          if (param_2 == 0) goto LAB_00f7e838;
          uVar4 = System_String__Equals(param_2,*(undefined8 *)(lVar3 + 0x20),0);
          if ((uVar4 & 1) != 0) {
            if ((*(long *)(param_1 + 0x38) == 0) ||
               (lVar6 = *(long *)(*(long *)(param_1 + 0x38) + 0x10), lVar6 == 0)) goto LAB_00f7e838;
            if (uVar7 < *(uint *)(lVar6 + 0x18)) {
              return *(undefined8 *)(lVar6 + (long)(int)uVar7 * 8 + 0x20);
            }
            goto LAB_00f7e83c;
          }
          uVar1 = *(uint *)(lVar6 + 0x18);
          uVar7 = uVar7 + 1;
        } while ((int)uVar7 < (int)uVar1);
      }
      puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      lVar6 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
      if (*(int *)(lVar6 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar6 = *(long *)puVar2;
      }
      if (*(char *)(*(long *)(lVar6 + 0xb8) + 0x17) != '\0') {
        uVar5 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_7443_01fc3428,param_2,0);
        if (*(int *)(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340 + 0xe0) == 0) {
          thunk_FUN_00df405c(*(long *)PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
        }
        kairo_unity_util_Log__Info(uVar5,0,0);
      }
      return 0;
    }
  }
LAB_00f7e838:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__PopAllSubForms
// Address: 00f7e840
// ==========================================================================================

undefined8 main_AppData__PopAllSubForms(void)

{
  int iVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  
  lVar2 = form_FormManager__GetInstance();
  if (lVar2 != 0) {
    iVar4 = 0;
    do {
      iVar1 = kairo_unity_form_FormManagerBase__GetFormsNum(lVar2,0);
      if (iVar1 <= iVar4) {
        return 1;
      }
      lVar2 = form_FormManager__GetInstance();
      if ((lVar2 == 0) ||
         (lVar2 = kairo_unity_form_FormManagerBase__GetForm(lVar2,iVar4,0), lVar2 == 0)) break;
      if (*(int *)(lVar2 + 0x10) == 4) {
        lVar3 = form_FormManager__GetInstance();
        if (lVar3 == 0) break;
        kairo_unity_form_FormManagerBase__Pop(lVar3,lVar2,0);
      }
      iVar4 = iVar4 + 1;
      lVar2 = form_FormManager__GetInstance();
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__FinishCapture
// Address: 00f7e8c0
// ==========================================================================================

void main_AppData__FinishCapture(long param_1)

{
  long lVar1;
  
  if (*(long *)(param_1 + 0x20) != 0) {
    form_GameForm__ChangeState(*(long *)(param_1 + 0x20),0,0);
    if ((*(long *)(param_1 + 0x20) != 0) &&
       (lVar1 = *(long *)(*(long *)(param_1 + 0x20) + 0xa0), lVar1 != 0)) {
      kairo_unity_form_FormManagerBase__DrawAllForms(lVar1,0);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__Capture
// Address: 00f7e8fc
// ==========================================================================================

void main_AppData__Capture(long param_1)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined8 uVar6;
  ulong uVar7;
  undefined8 uVar8;
  long lVar9;
  undefined8 uVar10;
  
  puVar3 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_020ff827 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_main_AppData__Capture_b__402_0_01fc3430);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    FUN_00db0bbc(PTR_kairo_unity_util_SNSShareUtil_OnCaptureCompleted_TypeInfo_01fc3438);
    FUN_00db0bbc(PTR_StringLiteral_11027_01fc3440);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff827 = 1;
  }
  *(undefined *)(param_1 + 0xd8) = 1;
  *(undefined4 *)(param_1 + 0xf8) = 1;
  puVar5 = PTR_StringLiteral_11027_01fc3440;
  puVar4 = PTR_StringLiteral_1_01fbf388;
  puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar6 = kairo_unity_util_Language__LT(*(undefined8 *)puVar5,*(undefined8 *)puVar4,0);
  lVar9 = *(long *)puVar2;
  uVar10 = *(undefined8 *)puVar4;
  if (*(int *)(lVar9 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar9);
    lVar9 = *(long *)puVar2;
  }
  puVar5 = PTR_kairo_unity_util_SNSShareUtil_OnCaptureCompleted_TypeInfo_01fc3438;
  puVar4 = PTR_Method_main_AppData__Capture_b__402_0_01fc3430;
  puVar2 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  if (*(int *)(*(long *)(lVar9 + 0xb8) + 4) != 3) {
    if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar7 = kairo_unity_util_Language__Japanese(0);
    lVar9 = *(long *)puVar2;
    if (*(int *)(lVar9 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar9);
      lVar9 = *(long *)puVar2;
    }
    lVar1 = 0x50;
    if ((uVar7 & 1) == 0) {
      lVar1 = 0x58;
    }
    uVar10 = *(undefined8 *)(*(long *)(lVar9 + 0xb8) + lVar1);
  }
  uVar8 = thunk_FUN_00e11c14(*(undefined8 *)puVar5);
  kairo_unity_util_SNSShareUtil_OnCaptureCompleted___ctor(uVar8,param_1,*(undefined8 *)puVar4,0);
  kairo_unity_util_SNSShareUtil__ShareScreenshot(uVar6,uVar10,uVar8,0);
  main_AppData__FinishCapture(param_1);
  return;
}



// ==========================================================================================
// Function: main_AppData__CaptureShare
// Address: 00f7eaa0
// ==========================================================================================

void main_AppData__CaptureShare(void)

{
  return;
}



// ==========================================================================================
// Function: main_AppData__IsSystemLanguage
// Address: 00f7eaa4
// ==========================================================================================

undefined8 main_AppData__IsSystemLanguage(void)

{
  return 1;
}



// ==========================================================================================
// Function: main_AppData__JumpSite
// Address: 00f7eaac
// ==========================================================================================

void main_AppData__JumpSite(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  undefined8 uVar5;
  
  puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_020ff828 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660);
    DAT_020ff828 = 1;
  }
  lVar3 = *(long *)puVar2;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  puVar1 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  lVar4 = *(long *)(lVar3 + 0xb8);
  if (*(int *)(lVar4 + 4) == 5) {
    if (*(int *)(*(long *)PTR_kairo_unity_native_KairoPlugin_TypeInfo_01fbf660 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    kairo_unity_native_KairoPlugin__jumpStoreKairosoft(0);
    return;
  }
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)(*(long *)puVar2 + 0xb8);
  }
  uVar5 = *(undefined8 *)(lVar4 + 0x160);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_ui_Canvas__OpenBrowser(uVar5,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__InitGamecenter
// Address: 00f7eb84
// ==========================================================================================

void main_AppData__InitGamecenter(void)

{
  undefined8 uVar1;
  
  uVar1 = data_LeaderboardData__GetLeaderbordId(0,0);
  kairo_unity_system_social_Leaderboard__SetData(uVar1,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__SendScore
// Address: 00f7eba0
// ==========================================================================================

void main_AppData__SendScore(undefined8 param_1,undefined4 param_2,undefined8 param_3)

{
  kairo_unity_system_social_Leaderboard__Send(param_2,param_3,0);
  return;
}



// ==========================================================================================
// Function: main_AppData__GetTime
// Address: 00f7ebb0
// ==========================================================================================

void main_AppData__GetTime(void)

{
  java_lang_JSystem__CurrentTimeMillis(0);
  return;
}



// ==========================================================================================
// Function: main_AppData__DrawShatyo
// Address: 00f7ebb8
// ==========================================================================================

void main_AppData__DrawShatyo(undefined8 param_1,long param_2,int param_3,int param_4,int param_5)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  
  puVar3 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  if ((DAT_020ff829 & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    DAT_020ff829 = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  puVar2 = PTR_form_GameForm_TypeInfo_01fbfab0;
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) == '\0') {
LAB_00f7ec64:
    lVar4 = *(long *)puVar2;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1158);
    if (lVar5 == 0) goto LAB_00f7ee20;
    if (*(int *)(lVar5 + 0x18) == 0) goto LAB_00f7ee1c;
    lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
    if (lVar4 == 0) goto LAB_00f7ee20;
    if (*(uint *)(lVar4 + 0x18) < 9) goto LAB_00f7ee1c;
    lVar4 = *(long *)(lVar4 + 0x60);
    if (lVar4 == 0) goto LAB_00f7ee20;
    uVar1 = *(uint *)(lVar4 + 0x18);
    if ((((uVar1 == 0) || (uVar1 == 1)) || (uVar1 < 3)) ||
       (((uVar1 == 3 || (uVar1 < 5)) || (uVar1 == 5)))) goto LAB_00f7ee1c;
    if (param_2 == 0) goto LAB_00f7ee20;
    kairo_unity_ui_Graphics__DrawImage
              ((float)(*(int *)(lVar4 + 0x20) + param_3),(float)(*(int *)(lVar4 + 0x24) + param_4),
               param_2,*(undefined8 *)(lVar5 + 0x20),*(undefined4 *)(lVar4 + 0x28),
               *(undefined4 *)(lVar4 + 0x2c),*(undefined4 *)(lVar4 + 0x30),
               *(undefined4 *)(lVar4 + 0x34),0);
    lVar4 = *(long *)puVar3;
  }
  else {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar3;
      lVar5 = *(long *)(lVar4 + 0xb8);
    }
    lVar5 = *(long *)(lVar5 + 0x98);
    if (lVar5 == 0) goto LAB_00f7ee20;
    if (*(uint *)(lVar5 + 0x18) < 2) goto LAB_00f7ee1c;
    if (*(char *)(lVar5 + 0x21) == '\0') goto LAB_00f7ec64;
  }
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) != '\0') {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)(*(long *)puVar3 + 0xb8);
    }
    lVar4 = *(long *)(lVar5 + 0x98);
    if (lVar4 == 0) goto LAB_00f7ee20;
    if (*(uint *)(lVar4 + 0x18) < 3) goto LAB_00f7ee1c;
    if (*(char *)(lVar4 + 0x22) != '\0') {
      return;
    }
  }
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
  if (lVar5 != 0) {
    if (*(uint *)(lVar5 + 0x18) < 9) {
LAB_00f7ee1c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar5 = *(long *)(lVar5 + 0x60);
    if (lVar5 != 0) {
      uVar1 = *(uint *)(lVar5 + 0x18);
      if ((uVar1 < 9) || (uVar1 == 9)) goto LAB_00f7ee1c;
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1150);
      if (lVar4 != 0) {
        if (((*(uint *)(lVar4 + 0x18) < 3) || (uVar1 < 0xb)) || (uVar1 == 0xb)) goto LAB_00f7ee1c;
        if (param_2 != 0) {
          kairo_unity_ui_Graphics__DrawImage
                    ((float)(param_5 + param_3 + *(int *)(lVar5 + 0x38)),
                     (float)(*(int *)(lVar5 + 0x3c) + param_4),param_2,*(undefined8 *)(lVar4 + 0x30)
                     ,*(undefined4 *)(lVar5 + 0x40),*(undefined4 *)(lVar5 + 0x44),
                     *(undefined4 *)(lVar5 + 0x48),*(undefined4 *)(lVar5 + 0x4c),0);
          return;
        }
      }
    }
  }
LAB_00f7ee20:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawKairokun
// Address: 00f7ee24
// ==========================================================================================

void main_AppData__DrawKairokun(undefined8 param_1,long param_2,int param_3,int param_4,int param_5)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  
  puVar3 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  if ((DAT_020ff82a & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    DAT_020ff82a = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  puVar2 = PTR_form_GameForm_TypeInfo_01fbfab0;
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) == '\0') {
LAB_00f7eed0:
    lVar4 = *(long *)puVar2;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1158);
    if (lVar5 == 0) goto LAB_00f7f094;
    if (*(uint *)(lVar5 + 0x18) < 0x15) goto LAB_00f7f090;
    lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
    if (lVar4 == 0) goto LAB_00f7f094;
    if (*(uint *)(lVar4 + 0x18) < 0x12) goto LAB_00f7f090;
    lVar4 = *(long *)(lVar4 + 0xa8);
    if (lVar4 == 0) goto LAB_00f7f094;
    uVar1 = *(uint *)(lVar4 + 0x18);
    if ((((uVar1 == 0) || (uVar1 == 1)) || (uVar1 < 3)) ||
       (((uVar1 == 3 || (uVar1 < 5)) || (uVar1 == 5)))) goto LAB_00f7f090;
    if (param_2 == 0) goto LAB_00f7f094;
    kairo_unity_ui_Graphics__DrawImage
              ((float)(*(int *)(lVar4 + 0x20) + param_3),(float)(*(int *)(lVar4 + 0x24) + param_4),
               param_2,*(undefined8 *)(lVar5 + 0xc0),*(undefined4 *)(lVar4 + 0x28),
               *(undefined4 *)(lVar4 + 0x2c),*(undefined4 *)(lVar4 + 0x30),
               *(undefined4 *)(lVar4 + 0x34),0);
    lVar4 = *(long *)puVar3;
  }
  else {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar3;
      lVar5 = *(long *)(lVar4 + 0xb8);
    }
    lVar5 = *(long *)(lVar5 + 0x98);
    if (lVar5 == 0) goto LAB_00f7f094;
    if (*(uint *)(lVar5 + 0x18) < 2) goto LAB_00f7f090;
    if (*(char *)(lVar5 + 0x21) == '\0') goto LAB_00f7eed0;
  }
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) != '\0') {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)(*(long *)puVar3 + 0xb8);
    }
    lVar4 = *(long *)(lVar5 + 0x98);
    if (lVar4 == 0) goto LAB_00f7f094;
    if (*(uint *)(lVar4 + 0x18) < 3) goto LAB_00f7f090;
    if (*(char *)(lVar4 + 0x22) != '\0') {
      return;
    }
  }
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
  if (lVar5 != 0) {
    if (*(uint *)(lVar5 + 0x18) < 0x12) {
LAB_00f7f090:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar5 = *(long *)(lVar5 + 0xa8);
    if (lVar5 != 0) {
      uVar1 = *(uint *)(lVar5 + 0x18);
      if ((uVar1 < 9) || (uVar1 == 9)) goto LAB_00f7f090;
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1150);
      if (lVar4 != 0) {
        if (((*(uint *)(lVar4 + 0x18) < 0x21) || (uVar1 < 0xb)) || (uVar1 == 0xb))
        goto LAB_00f7f090;
        if (param_2 != 0) {
          kairo_unity_ui_Graphics__DrawImage
                    ((float)(param_5 + param_3 + *(int *)(lVar5 + 0x38)),
                     (float)(param_4 + *(int *)(lVar5 + 0x3c) + 1),param_2,
                     *(undefined8 *)(lVar4 + 0x120),*(undefined4 *)(lVar5 + 0x40),
                     *(undefined4 *)(lVar5 + 0x44),*(undefined4 *)(lVar5 + 0x48),
                     *(undefined4 *)(lVar5 + 0x4c),0);
          return;
        }
      }
    }
  }
LAB_00f7f094:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetNumLen
// Address: 00f7f098
// ==========================================================================================

undefined4 main_AppData__GetNumLen(undefined4 param_1)

{
  long lVar1;
  undefined4 local_4;
  
  local_4 = param_1;
  lVar1 = System_Int32__ToString(&local_4,0);
  if (lVar1 != 0) {
    return *(undefined4 *)(lVar1 + 0x10);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawHisyo
// Address: 00f7f0c0
// ==========================================================================================

void main_AppData__DrawHisyo(undefined8 param_1,long param_2,int param_3,int param_4,int param_5)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  
  puVar3 = PTR_cfg_MyConfig_TypeInfo_01fbff00;
  if ((DAT_020ff82b & 1) == 0) {
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_cfg_MyConfig_TypeInfo_01fbff00);
    DAT_020ff82b = 1;
  }
  lVar4 = *(long *)puVar3;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  puVar2 = PTR_form_GameForm_TypeInfo_01fbfab0;
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) == '\0') {
LAB_00f7f16c:
    lVar4 = *(long *)puVar2;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1158);
    if (lVar5 == 0) goto LAB_00f7f32c;
    if (*(uint *)(lVar5 + 0x18) < 0x10) goto LAB_00f7f328;
    lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
    if (lVar4 == 0) goto LAB_00f7f32c;
    if (*(uint *)(lVar4 + 0x18) < 9) goto LAB_00f7f328;
    lVar4 = *(long *)(lVar4 + 0x60);
    if (lVar4 == 0) goto LAB_00f7f32c;
    uVar1 = *(uint *)(lVar4 + 0x18);
    if ((((uVar1 == 0) || (uVar1 == 1)) || (uVar1 < 3)) ||
       (((uVar1 == 3 || (uVar1 < 5)) || (uVar1 == 5)))) goto LAB_00f7f328;
    if (param_2 == 0) goto LAB_00f7f32c;
    kairo_unity_ui_Graphics__DrawImage
              ((float)(*(int *)(lVar4 + 0x20) + param_3),(float)(*(int *)(lVar4 + 0x24) + param_4),
               param_2,*(undefined8 *)(lVar5 + 0x98),*(undefined4 *)(lVar4 + 0x28),
               *(undefined4 *)(lVar4 + 0x2c),*(undefined4 *)(lVar4 + 0x30),
               *(undefined4 *)(lVar4 + 0x34),0);
    lVar4 = *(long *)puVar3;
  }
  else {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar3;
      lVar5 = *(long *)(lVar4 + 0xb8);
    }
    lVar5 = *(long *)(lVar5 + 0x98);
    if (lVar5 == 0) goto LAB_00f7f32c;
    if (*(uint *)(lVar5 + 0x18) < 2) goto LAB_00f7f328;
    if (*(char *)(lVar5 + 0x21) == '\0') goto LAB_00f7f16c;
  }
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar3;
  }
  lVar5 = *(long *)(lVar4 + 0xb8);
  if (*(char *)(lVar5 + 5) != '\0') {
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)(*(long *)puVar3 + 0xb8);
    }
    lVar4 = *(long *)(lVar5 + 0x98);
    if (lVar4 == 0) goto LAB_00f7f32c;
    if (*(uint *)(lVar4 + 0x18) < 3) goto LAB_00f7f328;
    if (*(char *)(lVar4 + 0x22) != '\0') {
      return;
    }
  }
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x128);
  if (lVar5 != 0) {
    if (*(uint *)(lVar5 + 0x18) < 9) {
LAB_00f7f328:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar5 = *(long *)(lVar5 + 0x60);
    if (lVar5 != 0) {
      uVar1 = *(uint *)(lVar5 + 0x18);
      if ((uVar1 < 9) || (uVar1 == 9)) goto LAB_00f7f328;
      lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x1150);
      if (lVar4 != 0) {
        if (((*(uint *)(lVar4 + 0x18) < 0xb) || (uVar1 < 0xb)) || (uVar1 == 0xb)) goto LAB_00f7f328;
        if (param_2 != 0) {
          kairo_unity_ui_Graphics__DrawImage
                    ((float)(param_5 + param_3 + *(int *)(lVar5 + 0x38)),
                     (float)(*(int *)(lVar5 + 0x3c) + param_4),param_2,*(undefined8 *)(lVar4 + 0x70)
                     ,*(undefined4 *)(lVar5 + 0x40),*(undefined4 *)(lVar5 + 0x44),
                     *(undefined4 *)(lVar5 + 0x48),*(undefined4 *)(lVar5 + 0x4c),0);
          return;
        }
      }
    }
  }
LAB_00f7f32c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__DrawNumber
// Address: 00f7f330
// ==========================================================================================

void main_AppData__DrawNumber
               (undefined8 param_1,uint param_2,undefined8 param_3,long param_4,undefined8 param_5,
               int param_6,int param_7,int param_8,undefined4 param_9)

{
  bool bVar1;
  int iVar2;
  undefined *puVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  long lVar7;
  ulong uVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  float fVar13;
  
  puVar3 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff82c & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8);
    DAT_020ff82c = 1;
  }
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar7 = main_AppData__GetInstance();
  if (((lVar7 != 0) && (lVar7 = *(long *)(lVar7 + 0x30), lVar7 != 0)) &&
     (lVar9 = *(long *)(lVar7 + 0x18), lVar9 != 0)) {
    if (param_2 < *(uint *)(lVar9 + 0x18)) {
      lVar12 = (long)(int)param_2;
      lVar9 = *(long *)(lVar9 + lVar12 * 8 + 0x20);
      if ((lVar9 == 0) || (lVar9 = kairo_unity_ui_Seb__GetSprite(lVar9,0,0,0), lVar9 == 0))
      goto LAB_00f7f6d0;
      if (4 < *(uint *)(lVar9 + 0x18)) {
        iVar2 = *(int *)(lVar9 + 0x30);
        if (param_4 < 10) {
          lVar11 = 1;
          lVar9 = 1;
        }
        else {
          lVar9 = 1;
          lVar11 = 1;
          lVar10 = param_4;
          do {
            lVar11 = lVar11 * 10;
            lVar9 = lVar9 + 1;
            bVar1 = 99 < lVar10;
            lVar10 = lVar10 / 10;
          } while (bVar1);
        }
        iVar4 = java_lang_StringEx__Length(param_3,0);
        iVar5 = java_lang_StringEx__Length(param_5,0);
        iVar2 = iVar2 + param_8;
        param_8 = ((int)lVar9 + iVar4 + iVar5) * iVar2 - param_8;
        if (*(int *)(*(long *)PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar8 = kairo_unity_util_BitUtil__Check(param_9,2,0);
        if ((uVar8 & 1) == 0) {
          if (*(int *)(*(long *)PTR_kairo_unity_util_BitUtil_TypeInfo_01fbf9d8 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          uVar8 = kairo_unity_util_BitUtil__Check(param_9,4,0);
          if ((uVar8 & 1) != 0) {
            param_6 = param_6 - param_8;
          }
        }
        else {
          if (param_8 < 0) {
            param_8 = param_8 + 1;
          }
          param_6 = param_6 - (param_8 >> 1);
        }
        iVar4 = java_lang_StringEx__Length(param_3,0);
        fVar13 = (float)param_7;
        if (0 < iVar4) {
          iVar4 = 0;
          do {
            uVar6 = java_lang_StringEx__CharAt(param_3,iVar4,0);
            if ((uVar6 & 0xffff) != 0x20) {
              lVar10 = *(long *)(lVar7 + 0x18);
              if (lVar10 == 0) goto LAB_00f7f6d0;
              if (*(uint *)(lVar10 + 0x18) <= param_2) goto LAB_00f7f6d4;
              lVar10 = *(long *)(lVar10 + lVar12 * 8 + 0x20);
              if (lVar10 == 0) goto LAB_00f7f6d0;
              kairo_unity_ui_Seb__DrawFrame
                        ((float)param_6,fVar13,lVar10,param_1,*(undefined8 *)(lVar7 + 0x10),
                         (uVar6 & 0xffff) - 0x30,0xffffffff,0);
            }
            param_6 = param_6 + iVar2;
            iVar4 = iVar4 + 1;
            iVar5 = java_lang_StringEx__Length(param_3,0);
          } while (iVar4 < iVar5);
        }
        if (0 < lVar9) {
          iVar4 = 1;
          do {
            lVar10 = *(long *)(lVar7 + 0x18);
            if (lVar10 == 0) goto LAB_00f7f6d0;
            if (*(uint *)(lVar10 + 0x18) <= param_2) goto LAB_00f7f6d4;
            lVar10 = *(long *)(lVar10 + lVar12 * 8 + 0x20);
            if (lVar10 == 0) goto LAB_00f7f6d0;
            uVar8 = 0;
            if (lVar11 != 0) {
              uVar8 = param_4 / lVar11;
            }
            kairo_unity_ui_Seb__DrawFrame
                      ((float)param_6,fVar13,lVar10,param_1,*(undefined8 *)(lVar7 + 0x10),
                       uVar8 & 0xffffffff,0xffffffff,0);
            param_4 = param_4 - uVar8 * lVar11;
            lVar10 = (long)iVar4;
            iVar4 = iVar4 + 1;
            param_6 = param_6 + iVar2;
            lVar11 = lVar11 / 10;
          } while (lVar10 < lVar9);
        }
        iVar4 = java_lang_StringEx__Length(param_5,0);
        if (0 < iVar4) {
          iVar4 = 0;
          do {
            uVar6 = java_lang_StringEx__CharAt(param_5,iVar4,0);
            if ((uVar6 & 0xffff) != 0x20) {
              lVar9 = *(long *)(lVar7 + 0x18);
              if (lVar9 == 0) goto LAB_00f7f6d0;
              if (*(uint *)(lVar9 + 0x18) <= param_2) goto LAB_00f7f6d4;
              lVar9 = *(long *)(lVar9 + lVar12 * 8 + 0x20);
              if (lVar9 == 0) goto LAB_00f7f6d0;
              kairo_unity_ui_Seb__DrawFrame
                        ((float)param_6,fVar13,lVar9,param_1,*(undefined8 *)(lVar7 + 0x10),
                         (uVar6 & 0xffff) - 0x30,0xffffffff,0);
            }
            param_6 = param_6 + iVar2;
            iVar4 = iVar4 + 1;
            iVar5 = java_lang_StringEx__Length(param_5,0);
          } while (iVar4 < iVar5);
        }
        return;
      }
    }
LAB_00f7f6d4:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f7f6d0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData__GetTalkTexts
// Address: 00f7f6d8
// ==========================================================================================

undefined8 main_AppData__GetTalkTexts(long param_1,undefined8 param_2,long param_3)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  uint uVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  undefined8 uVar11;
  ulong uVar12;
  int iVar13;
  ulong uVar14;
  long lVar15;
  
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff82d & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_1404_01fc2000);
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    FUN_00db0bbc(PTR_StringLiteral_9823_01fbf7b0);
    FUN_00db0bbc(PTR_StringLiteral_1344_01fbf358);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff82d = 1;
  }
  lVar8 = *(long *)puVar2;
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar8 = *(long *)puVar2;
  }
  if (*(long *)(param_1 + 0x20) != 0) {
    lVar8 = *(long *)(*(long *)(lVar8 + 0xb8) + 0xb8);
    uVar7 = form_GameForm__GetTalkIndex(*(long *)(param_1 + 0x20),param_2,0);
    puVar2 = PTR_StringLiteral_38_01fbfae8;
    if (lVar8 != 0) {
      if (*(uint *)(lVar8 + 0x18) <= uVar7) {
LAB_00f7f93c:
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar9 = *(undefined8 *)(lVar8 + (long)(int)uVar7 * 8 + 0x20);
      if (param_3 != 0) {
        uVar9 = kairo_unity_util_StringUtil__Replace(uVar9,param_3,0);
      }
      lVar8 = kairo_unity_util_StringUtil__Split(uVar9,*(undefined8 *)puVar2,0);
      if ((lVar8 != 0) &&
         (lVar10 = FUN_00db0c30(*(undefined8 *)PTR_string___TypeInfo_01fbf2f8,
                                *(int *)(lVar8 + 0x18) + -2), lVar10 != 0)) {
        uVar12 = *(ulong *)(lVar10 + 0x18) & 0xffffffff;
        iVar13 = (int)*(ulong *)(lVar10 + 0x18);
        if (0 < (long)(uVar12 << 0x20)) {
          uVar7 = *(uint *)(lVar8 + 0x18);
          uVar14 = 0;
          lVar15 = 0x200000000;
          do {
            if (((ulong)uVar7 <= uVar14 + 2) || (uVar12 <= uVar14)) goto LAB_00f7f93c;
            lVar1 = lVar15 >> 0x1d;
            lVar15 = lVar15 + 0x100000000;
            *(undefined8 *)(lVar10 + 0x20 + uVar14 * 8) = *(undefined8 *)(lVar8 + lVar1 + 0x20);
            uVar14 = uVar14 + 1;
          } while ((long)iVar13 != uVar14);
        }
        puVar6 = PTR_StringLiteral_1404_01fc2000;
        puVar5 = PTR_StringLiteral_838_01fbf908;
        puVar4 = PTR_StringLiteral_9823_01fbf7b0;
        puVar3 = PTR_StringLiteral_1_01fbf388;
        puVar2 = PTR_StringLiteral_1344_01fbf358;
        uVar9 = *(undefined8 *)PTR_StringLiteral_1_01fbf388;
        if (0 < iVar13) {
          lVar8 = 0;
          do {
            if ((uint)uVar12 <= (uint)lVar8) goto LAB_00f7f93c;
            lVar15 = *(long *)(lVar10 + 0x20 + lVar8 * 8);
            if ((lVar15 == 0) ||
               (lVar15 = Method_System_String_Replace
                                   (lVar15,*(undefined8 *)puVar2,*(undefined8 *)puVar4,0),
               lVar15 == 0)) goto LAB_00f7f940;
            uVar11 = Method_System_String_Replace
                               (lVar15,*(undefined8 *)puVar6,*(undefined8 *)puVar3,0);
            uVar9 = System_String__Concat(uVar9,uVar11,0);
            uVar12 = *(ulong *)(lVar10 + 0x18);
            if ((uint)lVar8 != (int)uVar12 - 1U) {
              uVar9 = System_String__Concat(uVar9,*(undefined8 *)puVar5,0);
              uVar12 = *(ulong *)(lVar10 + 0x18);
            }
            lVar8 = lVar8 + 1;
          } while ((int)lVar8 < (int)uVar12);
        }
        return uVar9;
      }
    }
  }
LAB_00f7f940:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData___cctor
// Address: 00f7f944
// ==========================================================================================

void main_AppData___cctor(void)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined *puVar9;
  long lVar10;
  long lVar11;
  undefined8 uVar12;
  long *plVar13;
  undefined4 local_44;
  
  puVar3 = PTR_string___TypeInfo_01fbf2f8;
  puVar2 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff82f & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_long___TypeInfo_01fbf5c8);
    FUN_00db0bbc(PTR_java_util_JRandom_TypeInfo_01fbf4d0);
    FUN_00db0bbc(PTR_Method_java_util_JTool_MakeArray_byte_01fbf5d0);
    FUN_00db0bbc(PTR_kairo_unity_util_Property___TypeInfo_01fc3448);
    FUN_00db0bbc(PTR_kairo_unity_util_Property_TypeInfo_01fc3398);
    FUN_00db0bbc(PTR_string_____TypeInfo_01fbf400);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__28A51049A72145FE33EDA123D28FC40E636CA3D0347FE299E3E2D7DEF20B79AD_01fc3450
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C7482E0B15B6E49522EBE480F075553ED9056D97CEB98C8974953846D828B788_01fc3458
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E1A613AA4B331588D97B5FEEF1FAABE8E8138D8C488EE9122B8533BFDDA3C189_01fc3460
                );
    FUN_00db0bbc(PTR_StringLiteral_11246_01fc3468);
    FUN_00db0bbc(PTR_StringLiteral_12042_01fc3470);
    FUN_00db0bbc(PTR_StringLiteral_12524_01fc3478);
    FUN_00db0bbc(PTR_StringLiteral_1137_01fc3480);
    FUN_00db0bbc(PTR_StringLiteral_9105_01fc3488);
    FUN_00db0bbc(PTR_StringLiteral_12107_01fc3490);
    FUN_00db0bbc(PTR_StringLiteral_8838_01fc3498);
    FUN_00db0bbc(PTR_StringLiteral_12000_01fc34a0);
    FUN_00db0bbc(PTR_StringLiteral_8607_01fc34a8);
    FUN_00db0bbc(PTR_StringLiteral_7238_01fc34b0);
    FUN_00db0bbc(PTR_StringLiteral_11183_01fc34b8);
    FUN_00db0bbc(PTR_StringLiteral_6778_01fc34c0);
    FUN_00db0bbc(PTR_StringLiteral_10841_01fc0160);
    FUN_00db0bbc(PTR_StringLiteral_11419_01fc34c8);
    FUN_00db0bbc(PTR_StringLiteral_7631_01fc34d0);
    FUN_00db0bbc(PTR_StringLiteral_8808_01fc34d8);
    FUN_00db0bbc(PTR_StringLiteral_7237_01fc34e0);
    FUN_00db0bbc(PTR_StringLiteral_9202_01fc34e8);
    FUN_00db0bbc(PTR_StringLiteral_7234_01fc34f0);
    FUN_00db0bbc(PTR_StringLiteral_8942_01fc34f8);
    FUN_00db0bbc(PTR_StringLiteral_10575_01fc0178);
    FUN_00db0bbc(PTR_StringLiteral_7239_01fc3500);
    FUN_00db0bbc(PTR_StringLiteral_8832_01fc3508);
    FUN_00db0bbc(PTR_StringLiteral_11826_01fc3510);
    FUN_00db0bbc(PTR_StringLiteral_6742_01fc3518);
    FUN_00db0bbc(PTR_StringLiteral_12460_01fc0b08);
    FUN_00db0bbc(PTR_StringLiteral_11166_01fc3520);
    FUN_00db0bbc(PTR_StringLiteral_12045_01fc3528);
    FUN_00db0bbc(PTR_StringLiteral_7236_01fc3530);
    FUN_00db0bbc(PTR_StringLiteral_11943_01fbfbe8);
    FUN_00db0bbc(PTR_StringLiteral_8608_01fc3538);
    FUN_00db0bbc(PTR_StringLiteral_7713_01fc3540);
    FUN_00db0bbc(PTR_StringLiteral_11271_01fc3548);
    FUN_00db0bbc(PTR_StringLiteral_7896_01fc3550);
    FUN_00db0bbc(PTR_StringLiteral_9696_01fc3558);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    FUN_00db0bbc(PTR_StringLiteral_11654_01fc3560);
    FUN_00db0bbc(PTR_StringLiteral_12001_01fc3568);
    FUN_00db0bbc(PTR_StringLiteral_7235_01fc3570);
    FUN_00db0bbc(PTR_StringLiteral_7052_01fc3578);
    FUN_00db0bbc(PTR_StringLiteral_11060_01fc3580);
    FUN_00db0bbc(PTR_StringLiteral_8606_01fc3588);
    FUN_00db0bbc(PTR_StringLiteral_11806_01fc3590);
    DAT_020ff82f = 1;
  }
  local_44 = 0;
  **(undefined8 **)(*(long *)puVar2 + 0xb8) = 0;
  *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 8) = 0;
  lVar10 = FUN_00db0c30(*(undefined8 *)puVar3,6);
  if (lVar10 != 0) {
    uVar1 = *(uint *)(lVar10 + 0x18);
    if (((((uVar1 != 0) &&
          (*(undefined8 *)(lVar10 + 0x20) = *(undefined8 *)PTR_StringLiteral_7234_01fc34f0,
          uVar1 != 1)) &&
         (*(undefined8 *)(lVar10 + 0x28) = *(undefined8 *)PTR_StringLiteral_7235_01fc3570, 2 < uVar1
         )) && ((*(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)PTR_StringLiteral_7236_01fc3530,
                uVar1 != 3 &&
                (*(undefined8 *)(lVar10 + 0x38) = *(undefined8 *)PTR_StringLiteral_7237_01fc34e0,
                4 < uVar1)))) &&
       (*(undefined8 *)(lVar10 + 0x40) = *(undefined8 *)PTR_StringLiteral_7238_01fc34b0, uVar1 != 5)
       ) {
      *(undefined8 *)(lVar10 + 0x48) = *(undefined8 *)PTR_StringLiteral_7239_01fc3500;
      puVar5 = PTR_int___TypeInfo_01fbf560;
      *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x10) = lVar10;
      lVar10 = FUN_00db0c30(*(undefined8 *)puVar5,2);
      if (lVar10 == 0) goto LAB_00f804c4;
      if (1 < *(uint *)(lVar10 + 0x18)) {
        *(undefined4 *)(lVar10 + 0x24) = 1;
        puVar4 = PTR_string_____TypeInfo_01fbf400;
        *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x18) = lVar10;
        lVar10 = FUN_00db0c30(*(undefined8 *)puVar4,2);
        lVar11 = FUN_00db0c30(*(undefined8 *)puVar3,7);
        if (lVar11 == 0) goto LAB_00f804c4;
        uVar1 = *(uint *)(lVar11 + 0x18);
        if ((((uVar1 != 0) &&
             (*(undefined8 *)(lVar11 + 0x20) = *(undefined8 *)PTR_StringLiteral_9202_01fc34e8,
             uVar1 != 1)) &&
            ((*(undefined8 *)(lVar11 + 0x28) = *(undefined8 *)PTR_StringLiteral_8942_01fc34f8,
             2 < uVar1 &&
             (((*(undefined8 *)(lVar11 + 0x30) = *(undefined8 *)PTR_StringLiteral_6778_01fc34c0,
               uVar1 != 3 &&
               (*(undefined8 *)(lVar11 + 0x38) = *(undefined8 *)PTR_StringLiteral_8608_01fc3538,
               4 < uVar1)) &&
              (*(undefined8 *)(lVar11 + 0x40) = *(undefined8 *)PTR_StringLiteral_8607_01fc34a8,
              uVar1 != 5)))))) &&
           (*(undefined8 *)(lVar11 + 0x48) = *(undefined8 *)PTR_StringLiteral_8606_01fc3588,
           6 < uVar1)) {
          *(undefined8 *)(lVar11 + 0x50) = *(undefined8 *)PTR_StringLiteral_6742_01fc3518;
          if (lVar10 == 0) goto LAB_00f804c4;
          if (*(int *)(lVar10 + 0x18) != 0) {
            *(long *)(lVar10 + 0x20) = lVar11;
            lVar11 = FUN_00db0c30(*(undefined8 *)puVar3,4);
            if (lVar11 == 0) goto LAB_00f804c4;
            uVar1 = *(uint *)(lVar11 + 0x18);
            if (((uVar1 != 0) &&
                (*(undefined8 *)(lVar11 + 0x20) = *(undefined8 *)PTR_StringLiteral_9696_01fc3558,
                uVar1 != 1)) &&
               ((*(undefined8 *)(lVar11 + 0x28) = *(undefined8 *)PTR_StringLiteral_7052_01fc3578,
                2 < uVar1 &&
                (*(undefined8 *)(lVar11 + 0x30) = *(undefined8 *)PTR_StringLiteral_7631_01fc34d0,
                uVar1 != 3)))) {
              *(undefined8 *)(lVar11 + 0x38) = *(undefined8 *)PTR_StringLiteral_9105_01fc3488;
              if (1 < *(uint *)(lVar10 + 0x18)) {
                *(long *)(lVar10 + 0x28) = lVar11;
                lVar11 = *(long *)(*(long *)puVar2 + 0xb8);
                *(long *)(lVar11 + 0x20) = lVar10;
                *(undefined8 *)(lVar11 + 0x30) = 0;
                *(undefined8 *)(lVar11 + 0x28) = 0;
                *(undefined8 *)(lVar11 + 0x40) = 0;
                *(undefined8 *)(lVar11 + 0x38) = 0;
                puVar4 = PTR_StringLiteral_8832_01fc3508;
                lVar10 = FUN_00db0c30(*(undefined8 *)puVar3,4);
                local_44 = 0x10d;
                uVar12 = System_Int32__ToString(&local_44,0);
                uVar12 = System_String__Concat(*(undefined8 *)puVar4,uVar12,0);
                puVar4 = PTR_StringLiteral_8808_01fc34d8;
                if (lVar10 == 0) goto LAB_00f804c4;
                if (*(int *)(lVar10 + 0x18) != 0) {
                  *(undefined8 *)(lVar10 + 0x20) = uVar12;
                  local_44 = 0x10d;
                  uVar12 = System_Int32__ToString(&local_44,0);
                  uVar12 = System_String__Concat(*(undefined8 *)puVar4,uVar12,0);
                  puVar4 = PTR_StringLiteral_8838_01fc3498;
                  if (1 < *(uint *)(lVar10 + 0x18)) {
                    *(undefined8 *)(lVar10 + 0x28) = uVar12;
                    local_44 = 0x10d;
                    uVar12 = System_Int32__ToString(&local_44,0);
                    uVar12 = System_String__Concat(*(undefined8 *)puVar4,uVar12,0);
                    puVar4 = PTR_StringLiteral_7713_01fc3540;
                    if (2 < *(uint *)(lVar10 + 0x18)) {
                      *(undefined8 *)(lVar10 + 0x30) = uVar12;
                      local_44 = 0x10d;
                      uVar12 = System_Int32__ToString(&local_44,0);
                      uVar12 = System_String__Concat(*(undefined8 *)puVar4,uVar12,0);
                      if (3 < *(uint *)(lVar10 + 0x18)) {
                        *(undefined8 *)(lVar10 + 0x38) = uVar12;
                        *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x48) = lVar10;
                        puVar6 = 
                        PTR_Field__PrivateImplementationDetails__E1A613AA4B331588D97B5FEEF1FAABE8E8138D8C488EE9122B8533BFDDA3C189_01fc3460
                        ;
                        puVar4 = 
                        PTR_Field__PrivateImplementationDetails__28A51049A72145FE33EDA123D28FC40E636CA3D0347FE299E3E2D7DEF20B79AD_01fc3450
                        ;
                        uVar12 = FUN_00db0c30(*(undefined8 *)puVar5,7);
                        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                  (uVar12,*(undefined8 *)puVar6,0);
                        *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x50) = uVar12;
                        uVar12 = FUN_00db0c30(*(undefined8 *)puVar5,10);
                        Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                  (uVar12,*(undefined8 *)puVar4,0);
                        *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x58) = uVar12;
                        lVar10 = FUN_00db0c30(*(undefined8 *)puVar3,0x13);
                        puVar4 = PTR_StringLiteral_1_01fbf388;
                        if (lVar10 == 0) goto LAB_00f804c4;
                        uVar1 = *(uint *)(lVar10 + 0x18);
                        if (uVar1 != 0) {
                          *(undefined8 *)(lVar10 + 0x20) =
                               *(undefined8 *)PTR_StringLiteral_1_01fbf388;
                          if ((((uVar1 != 1) &&
                               (*(undefined8 *)(lVar10 + 0x28) =
                                     *(undefined8 *)PTR_StringLiteral_11826_01fc3510, 2 < uVar1)) &&
                              ((*(undefined8 *)(lVar10 + 0x30) =
                                     *(undefined8 *)PTR_StringLiteral_12001_01fc3568, uVar1 != 3 &&
                               (((*(undefined8 *)(lVar10 + 0x38) =
                                       *(undefined8 *)PTR_StringLiteral_11654_01fc3560, 4 < uVar1 &&
                                 (*(undefined8 *)(lVar10 + 0x40) =
                                       *(undefined8 *)PTR_StringLiteral_10841_01fc0160, uVar1 != 5))
                                && (*(undefined8 *)(lVar10 + 0x48) =
                                         *(undefined8 *)PTR_StringLiteral_10575_01fc0178, 6 < uVar1)
                                ))))) &&
                             (((*(undefined8 *)(lVar10 + 0x50) =
                                     *(undefined8 *)PTR_StringLiteral_11943_01fbfbe8, uVar1 != 7 &&
                               (*(undefined8 *)(lVar10 + 0x58) =
                                     *(undefined8 *)PTR_StringLiteral_11060_01fc3580, 8 < uVar1)) &&
                              ((*(undefined8 *)(lVar10 + 0x60) =
                                     *(undefined8 *)PTR_StringLiteral_11183_01fc34b8, uVar1 != 9 &&
                               (((*(undefined8 *)(lVar10 + 0x68) =
                                       *(undefined8 *)PTR_StringLiteral_12460_01fc0b08, 10 < uVar1
                                 && (*(undefined8 *)(lVar10 + 0x70) =
                                          *(undefined8 *)PTR_StringLiteral_11166_01fc3520,
                                    uVar1 != 0xb)) &&
                                ((*(undefined8 *)(lVar10 + 0x78) =
                                       *(undefined8 *)PTR_StringLiteral_12045_01fc3528, 0xc < uVar1
                                 && (((((*(undefined8 *)(lVar10 + 0x80) =
                                              *(undefined8 *)PTR_StringLiteral_11419_01fc34c8,
                                        uVar1 != 0xd &&
                                        (*(undefined8 *)(lVar10 + 0x88) =
                                              *(undefined8 *)PTR_StringLiteral_11246_01fc3468,
                                        0xe < uVar1)) &&
                                       (*(undefined8 *)(lVar10 + 0x90) =
                                             *(undefined8 *)PTR_StringLiteral_12042_01fc3470,
                                       uVar1 != 0xf)) &&
                                      ((*(undefined8 *)(lVar10 + 0x98) =
                                             *(undefined8 *)PTR_StringLiteral_11271_01fc3548,
                                       0x10 < uVar1 &&
                                       (*(undefined8 *)(lVar10 + 0xa0) =
                                             *(undefined8 *)PTR_StringLiteral_11806_01fc3590,
                                       uVar1 != 0x11)))) &&
                                     (*(undefined8 *)(lVar10 + 0xa8) =
                                           *(undefined8 *)PTR_StringLiteral_12524_01fc3478,
                                     0x12 < uVar1)))))))))))) {
                            *(undefined8 *)(lVar10 + 0xb0) =
                                 *(undefined8 *)PTR_StringLiteral_12000_01fc34a0;
                            puVar9 = PTR_kairo_unity_util_Property___TypeInfo_01fc3448;
                            *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x60) = lVar10;
                            puVar7 = 
                            PTR_Field__PrivateImplementationDetails__C7482E0B15B6E49522EBE480F075553ED9056D97CEB98C8974953846D828B788_01fc3458
                            ;
                            puVar6 = PTR_long___TypeInfo_01fbf5c8;
                            uVar12 = FUN_00db0c30(*(undefined8 *)puVar9,0);
                            *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x68) = uVar12;
                            uVar12 = FUN_00db0c30(*(undefined8 *)puVar5,0x14);
                            Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                                      (uVar12,*(undefined8 *)puVar7,0);
                            *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x70) = uVar12;
                            uVar12 = FUN_00db0c30(*(undefined8 *)puVar6,4);
                            *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x78) = uVar12;
                            lVar10 = FUN_00db0c30(*(undefined8 *)puVar3,0xb);
                            puVar7 = PTR_StringLiteral_12107_01fc3490;
                            if (lVar10 == 0) goto LAB_00f804c4;
                            uVar1 = *(uint *)(lVar10 + 0x18);
                            if (uVar1 != 0) {
                              *(undefined8 *)(lVar10 + 0x20) =
                                   *(undefined8 *)PTR_StringLiteral_12107_01fc3490;
                              if (((uVar1 != 1) &&
                                  (*(undefined8 *)(lVar10 + 0x28) = *(undefined8 *)puVar7, 2 < uVar1
                                  )) && ((*(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)puVar4,
                                         uVar1 != 3 &&
                                         (*(undefined8 *)(lVar10 + 0x38) = *(undefined8 *)puVar4,
                                         puVar7 = PTR_StringLiteral_1137_01fc3480, 4 < uVar1)))) {
                                *(undefined8 *)(lVar10 + 0x40) =
                                     *(undefined8 *)PTR_StringLiteral_1137_01fc3480;
                                if ((((uVar1 != 5) &&
                                     (*(undefined8 *)(lVar10 + 0x48) = *(undefined8 *)puVar7,
                                     6 < uVar1)) &&
                                    (*(undefined8 *)(lVar10 + 0x50) = *(undefined8 *)puVar4,
                                    uVar1 != 7)) &&
                                   (((*(undefined8 *)(lVar10 + 0x58) = *(undefined8 *)puVar4,
                                     8 < uVar1 &&
                                     (*(undefined8 *)(lVar10 + 0x60) = *(undefined8 *)puVar7,
                                     uVar1 != 9)) &&
                                    (*(undefined8 *)(lVar10 + 0x68) = *(undefined8 *)puVar7,
                                    10 < uVar1)))) {
                                  *(undefined8 *)(lVar10 + 0x70) = *(undefined8 *)puVar4;
                                  *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x80) = lVar10;
                                  lVar10 = FUN_00db0c30(*(undefined8 *)puVar5,2);
                                  puVar7 = PTR_Method_java_util_JTool_MakeArray_byte_01fbf5d0;
                                  if (lVar10 == 0) goto LAB_00f804c4;
                                  if (*(int *)(lVar10 + 0x18) != 0) {
                                    *(undefined4 *)(lVar10 + 0x20) = 1;
                                    puVar8 = PTR_kairo_unity_util_Property_TypeInfo_01fc3398;
                                    uVar12 = java_util_JTool__MakeArray_object
                                                       (lVar10,*(undefined8 *)puVar7);
                                    *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x88) =
                                         uVar12;
                                    plVar13 = (long *)FUN_00db0c30(*(undefined8 *)puVar9,1);
                                    lVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar8);
                                    kairo_unity_util_Property___ctor(lVar10,0);
                                    if (plVar13 == (long *)0x0) goto LAB_00f804c4;
                                    if ((lVar10 != 0) &&
                                       (lVar11 = thunk_FUN_00e11b18(lVar10,*(undefined8 *)
                                                                            (*plVar13 + 0x40)),
                                       lVar11 == 0)) {
                                      uVar12 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
                                      FUN_00db0cb0(uVar12,0);
                                    }
                                    if (*(int *)(plVar13 + 3) != 0) {
                                      plVar13[4] = lVar10;
                                      *(long **)(*(long *)(*(long *)puVar2 + 0xb8) + 0x90) = plVar13
                                      ;
                                      uVar12 = FUN_00db0c30(*(undefined8 *)puVar5,0);
                                      *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x98) =
                                           uVar12;
                                      uVar12 = FUN_00db0c30(*(undefined8 *)puVar6,0);
                                      *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0xa0) =
                                           uVar12;
                                      lVar10 = FUN_00db0c30(*(undefined8 *)puVar3,1);
                                      if (lVar10 == 0) goto LAB_00f804c4;
                                      if (*(int *)(lVar10 + 0x18) != 0) {
                                        *(undefined8 *)(lVar10 + 0x20) = *(undefined8 *)puVar4;
                                        *(long *)(*(long *)(*(long *)puVar2 + 0xb8) + 0xa8) = lVar10
                                        ;
                                        lVar10 = FUN_00db0c30(*(undefined8 *)puVar5,2);
                                        if (lVar10 == 0) goto LAB_00f804c4;
                                        if (*(int *)(lVar10 + 0x18) != 0) {
                                          *(undefined4 *)(lVar10 + 0x20) = 1;
                                          puVar5 = PTR_StringLiteral_7896_01fc3550;
                                          puVar3 = PTR_java_util_JRandom_TypeInfo_01fbf4d0;
                                          uVar12 = java_util_JTool__MakeArray_object
                                                             (lVar10,*(undefined8 *)puVar7);
                                          lVar10 = *(long *)(*(long *)puVar2 + 0xb8);
                                          *(undefined8 *)(lVar10 + 0xb0) = uVar12;
                                          *(undefined *)(lVar10 + 0xcc) = 1;
                                          *(undefined8 *)(lVar10 + 0xd0) = 0x700000007;
                                          *(undefined8 *)(lVar10 + 0xd8) = *(undefined8 *)puVar5;
                                          uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
                                          java_util_JRandom___ctor(uVar12,0);
                                          *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0xe0)
                                               = uVar12;
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
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f804c4:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_AppData___c___cctor
// Address: 00f80664
// ==========================================================================================

void main_AppData___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_main_AppData___c_TypeInfo_01fc3400;
  if ((DAT_020ff831 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData___c_TypeInfo_01fc3400);
    DAT_020ff831 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: main_AppData___c___ctor
// Address: 00f806c0
// ==========================================================================================

void main_AppData___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: main_Main___ctor
// Address: 00f806d0
// ==========================================================================================

void main_Main___ctor(undefined8 param_1)

{
  undefined *puVar1;
  
  puVar1 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_020ff832 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff832 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_ui_IApplication___ctor(param_1,0);
  kairo_unity_ui_IApplication__Init(param_1,param_1,0);
  return;
}



// ==========================================================================================
// Function: main_Main__GetInstance
// Address: 00f80738
// ==========================================================================================

void main_Main__GetInstance(void)

{
  byte bVar1;
  undefined *puVar2;
  long lVar3;
  
  puVar2 = PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8;
  if ((DAT_020ff833 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    FUN_00db0bbc(PTR_main_Main_TypeInfo_01fc33d8);
    DAT_020ff833 = 1;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_020ff602 == '\0') {
    FUN_00db0bbc(PTR_kairo_unity_ui_IApplication_TypeInfo_01fbf2d8);
    DAT_020ff602 = '\x01';
  }
  lVar3 = *(long *)puVar2;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar2;
  }
  if (**(long ***)(lVar3 + 0xb8) != (long *)0x0) {
    lVar3 = ***(long ***)(lVar3 + 0xb8);
    bVar1 = *(byte *)(*(long *)PTR_main_Main_TypeInfo_01fc33d8 + 0x130);
    if ((*(byte *)(lVar3 + 0x130) < bVar1) ||
       (*(long *)(*(long *)(lVar3 + 200) + (ulong)bVar1 * 8 + -8) !=
        *(long *)PTR_main_Main_TypeInfo_01fc33d8)) {
                    /* WARNING: Subroutine does not return */
      FUN_00db1180();
    }
  }
  return;
}



// ==========================================================================================
// Function: main_Main__OnCreate
// Address: 00f80808
// ==========================================================================================

void main_Main__OnCreate(undefined8 param_1)

{
  uint uVar1;
  char cVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined4 uVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  undefined8 uVar11;
  ulong uVar12;
  
  puVar5 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_020ff834 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_native_AppPlugin_TypeInfo_01fbf828);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590);
    FUN_00db0bbc(PTR_kairo_unity_util_JarInflater_TypeInfo_01fbf510);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_string_____TypeInfo_01fbf400);
    FUN_00db0bbc(PTR_StringLiteral_45_01fbf350);
    FUN_00db0bbc(PTR_StringLiteral_38_01fbfae8);
    FUN_00db0bbc(PTR_StringLiteral_9100_01fc35a8);
    FUN_00db0bbc(PTR_StringLiteral_9237_01fc35b0);
    FUN_00db0bbc(PTR_StringLiteral_6287_01fc0648);
    FUN_00db0bbc(PTR_StringLiteral_2918_01fc35b8);
    DAT_020ff834 = 1;
  }
  puVar3 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  kairo_unity_ui_IApplication__OnCreate(param_1,0);
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar4 = PTR_native_AppPlugin_TypeInfo_01fbf828;
  uVar7 = kairo_unity_util_Language__Get(0);
  lVar10 = *(long *)puVar3;
  if (*(int *)(lVar10 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar10);
    lVar10 = *(long *)puVar3;
  }
  puVar3 = PTR_main_AppData_TypeInfo_01fbf278;
  cVar2 = *(char *)(*(long *)(lVar10 + 0xb8) + 0x17);
  uVar11 = *(undefined8 *)(*(long *)(lVar10 + 0xb8) + 0x28);
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar4 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  native_AppPlugin__Init(uVar7,cVar2 != '\0',uVar11);
  kairo_unity_ui_IApplication__SetViewport(param_1,0xf0,0x118,0);
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar3 = PTR_kairo_unity_ui_Graphics_TypeInfo_01fbf590;
  lVar10 = main_AppData__GetInstance();
  if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar4);
  }
  lVar8 = kairo_unity_ui_Canvas__GetInstance(0);
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar3);
  }
  uVar7 = kairo_unity_ui_Graphics__GetColorOfRGB(0,0,0,0);
  if (lVar8 == 0) {
LAB_00f80c98:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  kairo_unity_ui_Canvas__SetBackground(lVar8,uVar7,0);
  lVar9 = form_FormManager__GetInstance();
  kairo_unity_ui_Canvas__SetDisplayCurrent(lVar8,param_1,0);
  if ((lVar10 == 0) || (lVar9 == 0)) goto LAB_00f80c98;
  kairo_unity_form_FormManagerBase__ChangeCurrentForm(lVar9,*(undefined8 *)(lVar10 + 0x10),0,0);
                    /* try { // try from 00f80a3c to 00f80a4b has its CatchHandler @ 00f80cd4 */
  uVar11 = kairo_unity_io_RecordStore__ReadRecord(1,0,0);
                    /* try { // try from 00f80a5c to 00f80a6f has its CatchHandler @ 00f80ce4 */
  lVar10 = thunk_FUN_00e11c14(*(undefined8 *)PTR_kairo_unity_util_JarInflater_TypeInfo_01fbf510);
  Method_kairo_unity_util_JarInflater__ctor(lVar10,uVar11,0);
                    /* try { // try from 00f80a7c to 00f80a87 has its CatchHandler @ 00f80cd0 */
  lVar8 = kairo_unity_util_StringUtil__LoadStringArray
                    (lVar10,*(undefined8 *)PTR_StringLiteral_9100_01fc35a8,0);
  puVar3 = PTR_string_____TypeInfo_01fbf400;
  if (lVar8 == 0) {
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
                    /* try { // try from 00f80b3c to 00f80b3f has its CatchHandler @ 00f80cac */
      thunk_FUN_00df405c();
    }
                    /* try { // try from 00f80b40 to 00f80b47 has its CatchHandler @ 00f80cb4 */
    uVar12 = kairo_unity_util_Language__English(0);
                    /* try { // try from 00f80b58 to 00f80b63 has its CatchHandler @ 00f80cb0 */
    if (((uVar12 & 1) == 0) ||
       (lVar8 = kairo_unity_util_StringUtil__LoadStringArray
                          (lVar10,*(undefined8 *)PTR_StringLiteral_2918_01fc35b8,0), lVar8 == 0))
    goto LAB_00f80b6c;
  }
                    /* try { // try from 00f80aa0 to 00f80aa3 has its CatchHandler @ 00f80cc4 */
  lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,*(undefined4 *)(lVar8 + 0x18));
  puVar4 = PTR_StringLiteral_38_01fbfae8;
  if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80ca4 to 00f80ca7 has its CatchHandler @ 00f80cc0 */
    FUN_00db0de4();
  }
  if (0 < *(int *)(lVar9 + 0x18)) {
    uVar12 = 0;
    do {
      if (*(uint *)(lVar8 + 0x18) <= uVar12) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80c88 to 00f80c8b has its CatchHandler @ 00f80d04 */
        FUN_00db0dec();
      }
                    /* try { // try from 00f80ae0 to 00f80af3 has its CatchHandler @ 00f80d08 */
      uVar11 = kairo_unity_util_StringUtil__Split
                         (*(undefined8 *)(lVar8 + 0x20 + uVar12 * 8),*(undefined8 *)puVar4,0,0,0,0);
      uVar1 = *(uint *)(lVar9 + 0x18);
      if (uVar1 <= uVar12) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80c84 to 00f80c87 has its CatchHandler @ 00f80d0c */
        FUN_00db0dec();
      }
      *(undefined8 *)(lVar9 + 0x20 + uVar12 * 8) = uVar11;
      uVar12 = uVar12 + 1;
    } while ((long)uVar12 < (long)(int)uVar1);
  }
  if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
                    /* try { // try from 00f80b1c to 00f80b2b has its CatchHandler @ 00f80ce0 */
    thunk_FUN_00df405c();
  }
  kairo_unity_util_Language__SetSoftLabelTable(lVar9,0);
LAB_00f80b6c:
                    /* try { // try from 00f80b78 to 00f80b83 has its CatchHandler @ 00f80ccc */
  lVar8 = kairo_unity_util_StringUtil__LoadStringArray
                    (lVar10,*(undefined8 *)PTR_StringLiteral_9237_01fc35b0,0);
  if (lVar8 != 0) {
                    /* try { // try from 00f80b94 to 00f80b97 has its CatchHandler @ 00f80cbc */
    lVar9 = FUN_00db0c30(*(undefined8 *)puVar3,*(undefined4 *)(lVar8 + 0x18));
    puVar6 = PTR_StringLiteral_6287_01fc0648;
    puVar4 = PTR_StringLiteral_38_01fbfae8;
    puVar3 = PTR_StringLiteral_45_01fbf350;
    if (lVar9 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80ca8 to 00f80cab has its CatchHandler @ 00f80cb8 */
      FUN_00db0de4();
    }
    if (0 < *(int *)(lVar9 + 0x18)) {
      uVar12 = 0;
      do {
        if (*(uint *)(lVar8 + 0x18) <= uVar12) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80c94 to 00f80c97 has its CatchHandler @ 00f80cf0 */
          FUN_00db0dec();
        }
                    /* try { // try from 00f80be8 to 00f80bef has its CatchHandler @ 00f80cf4 */
        uVar11 = kairo_unity_util_StringUtil__Replace
                           (*(undefined8 *)(lVar8 + 0x20 + uVar12 * 8),*(undefined8 *)puVar6,
                            *(undefined8 *)puVar3,0);
        if (*(uint *)(lVar8 + 0x18) <= uVar12) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80c90 to 00f80c93 has its CatchHandler @ 00f80cf8 */
          FUN_00db0dec();
        }
        *(undefined8 *)(lVar8 + 0x20 + uVar12 * 8) = uVar11;
                    /* try { // try from 00f80c04 to 00f80c17 has its CatchHandler @ 00f80cfc */
        uVar11 = kairo_unity_util_StringUtil__Split(uVar11,*(undefined8 *)puVar4,0,0,0,0);
        uVar1 = *(uint *)(lVar9 + 0x18);
        if (uVar1 <= uVar12) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f80c8c to 00f80c8f has its CatchHandler @ 00f80d00 */
          FUN_00db0dec();
        }
        *(undefined8 *)(lVar9 + 0x20 + uVar12 * 8) = uVar11;
        uVar12 = uVar12 + 1;
      } while ((long)uVar12 < (long)(int)uVar1);
    }
    if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
                    /* try { // try from 00f80c40 to 00f80c4f has its CatchHandler @ 00f80cc8 */
      thunk_FUN_00df405c();
    }
    kairo_unity_util_Language__SetTextTable(lVar9,0);
    lVar8 = 0;
  }
  if (lVar10 != 0) {
    kairo_unity_util_JarInflater__Close(lVar10,0);
  }
  if (lVar8 == 0) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0ddc(lVar8);
}



// ==========================================================================================
// Function: main_Main__OnUpdate
// Address: 00f80e40
// ==========================================================================================

void main_Main__OnUpdate(void)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  undefined4 uVar4;
  long lVar5;
  long lVar6;
  long *plVar7;
  ulong uVar8;
  long lVar9;
  long lVar10;
  
  puVar1 = PTR_main_AppData_TypeInfo_01fbf278;
  if ((DAT_020ff835 & 1) == 0) {
    FUN_00db0bbc(PTR_main_AppData_TypeInfo_01fbf278);
    FUN_00db0bbc(PTR_UnityEngine_Application_TypeInfo_01fc35c0);
    FUN_00db0bbc(PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8);
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_form_GameForm_TypeInfo_01fbfab0);
    FUN_00db0bbc(PTR_main_Main_TypeInfo_01fc33d8);
    DAT_020ff835 = 1;
  }
  puVar2 = PTR_kairo_unity_ui_Canvas_TypeInfo_01fbf2c8;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  main_AppData__GetInstance();
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  lVar5 = kairo_unity_ui_Canvas__GetInstance(0);
  lVar6 = form_FormManager__GetInstance();
  lVar9 = *(long *)puVar1;
  if (*(int *)(lVar9 + 0xe0) == 0) {
                    /* try { // try from 00f80f14 to 00f80f1b has its CatchHandler @ 00f8111c */
    thunk_FUN_00df405c(lVar9);
    lVar9 = *(long *)puVar1;
  }
  *(undefined *)(*(long *)(lVar9 + 0xb8) + 0xcc) = 1;
  if (lVar6 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f810e0 to 00f810e3 has its CatchHandler @ 00f81118 */
    FUN_00db0de4();
  }
                    /* try { // try from 00f80f30 to 00f80f3b has its CatchHandler @ 00f81114 */
  kairo_unity_form_FormManagerBase__Execute(lVar6,0);
  puVar1 = PTR_main_Main_TypeInfo_01fc33d8;
  plVar7 = **(long ***)(*(long *)PTR_main_Main_TypeInfo_01fc33d8 + 0xb8);
  if (plVar7 != (long *)0x0) {
                    /* try { // try from 00f80f5c to 00f80f5f has its CatchHandler @ 00f81110 */
    iVar3 = (**(code **)(*plVar7 + 0x1b8))(plVar7,*(undefined8 *)(*plVar7 + 0x1c0));
    if (iVar3 != 3) {
      plVar7 = **(long ***)(*(long *)puVar1 + 0xb8);
      if (plVar7 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f810ec to 00f810ef has its CatchHandler @ 00f810f4 */
        FUN_00db0de4();
      }
                    /* try { // try from 00f80f80 to 00f80f83 has its CatchHandler @ 00f810f0 */
      iVar3 = (**(code **)(*plVar7 + 0x1b8))(plVar7,*(undefined8 *)(*plVar7 + 0x1c0));
      if (iVar3 != 0) goto LAB_00f80fb0;
    }
    lVar9 = *(long *)(*(long *)puVar1 + 0xb8);
    iVar3 = *(int *)(lVar9 + 8);
    *(int *)(lVar9 + 8) = iVar3 + -1;
    if (iVar3 < 1) {
                    /* try { // try from 00f80fa4 to 00f80feb has its CatchHandler @ 00f8111c */
      main_Main__SetJingle(0,0x14);
    }
  }
LAB_00f80fb0:
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  lVar9 = *(long *)PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(lVar9 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar9 = *(long *)puVar1;
  }
  lVar10 = *(long *)(lVar9 + 0xb8);
  if (*(char *)(lVar10 + 0xc2) != '\0') {
    *(undefined4 *)(lVar6 + 0xb0) = 0x78;
  }
  if (*(int *)(lVar9 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar10 = *(long *)(*(long *)puVar1 + 0xb8);
  }
  if (*(char *)(lVar10 + 0xc5) != '\0') {
    if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f810e4 to 00f810e7 has its CatchHandler @ 00f8110c */
      FUN_00db0de4();
    }
                    /* try { // try from 00f81000 to 00f8100f has its CatchHandler @ 00f81108 */
    uVar8 = kairo_unity_ui_Canvas__CheckKeyState(lVar5,0x10,0);
    if ((uVar8 & 1) != 0) {
      *(undefined4 *)(lVar6 + 0xb0) = 400;
    }
  }
  puVar2 = PTR_form_GameForm_TypeInfo_01fbfab0;
  lVar9 = *(long *)PTR_form_GameForm_TypeInfo_01fbfab0;
  if (*(int *)(lVar9 + 0xe0) == 0) {
                    /* try { // try from 00f81030 to 00f81033 has its CatchHandler @ 00f810fc */
    thunk_FUN_00df405c();
    lVar9 = *(long *)puVar2;
  }
  *(undefined4 *)(lVar6 + 0xb0) = *(undefined4 *)(*(long *)(lVar9 + 0xb8) + 0x1290);
  lVar9 = *(long *)puVar1;
  if (*(int *)(lVar9 + 0xe0) == 0) {
                    /* try { // try from 00f81050 to 00f81053 has its CatchHandler @ 00f810f8 */
    thunk_FUN_00df405c();
    lVar9 = *(long *)puVar1;
  }
  if (*(char *)(*(long *)(lVar9 + 0xb8) + 0xc4) != '\0') {
    if (lVar5 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00f810e8 to 00f810eb has its CatchHandler @ 00f81104 */
      FUN_00db0de4();
    }
                    /* try { // try from 00f81068 to 00f81077 has its CatchHandler @ 00f81100 */
    uVar8 = kairo_unity_ui_Canvas__CheckKeyState(lVar5,0x400,0);
    if ((uVar8 & 1) != 0) {
      *(undefined4 *)(lVar6 + 0xb0) = 2;
    }
  }
                    /* try { // try from 00f81084 to 00f8108f has its CatchHandler @ 00f8111c */
  UnityEngine_QualitySettings__set_vSyncCount(0,0);
                    /* try { // try from 00f81090 to 00f810c3 has its CatchHandler @ 00f81128 */
  uVar4 = kairo_unity_form_FormManagerBase__GetTargetFps(lVar6,0);
  if (*(int *)(*(long *)PTR_UnityEngine_Application_TypeInfo_01fc35c0 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  UnityEngine_Application__set_targetFrameRate(uVar4,0);
  return;
}



// ==========================================================================================
// Function: main_Main__OnDraw
// Address: 00f81708
// ==========================================================================================

void main_Main__OnDraw(void)

{
  long *plVar1;
  
                    /* try { // try from 00f8170c to 00f8172b has its CatchHandler @ 00f8172c */
  plVar1 = (long *)form_FormManager__GetInstance();
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 0x178))(plVar1,*(undefined8 *)(*plVar1 + 0x180));
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_Main__OnResume
// Address: 00f817c4
// ==========================================================================================

void main_Main__OnResume(void)

{
  return;
}



// ==========================================================================================
// Function: main_Main__OnSuspend
// Address: 00f817c8
// ==========================================================================================

void main_Main__OnSuspend(void)

{
  analytics_AnalyticsTracker__DispatchPageView(0);
  return;
}



// ==========================================================================================
// Function: main_Main__OnDestroy
// Address: 00f817d0
// ==========================================================================================

void main_Main__OnDestroy(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_native_AppPlugin_TypeInfo_01fbf828;
  if ((DAT_020ff836 & 1) == 0) {
    FUN_00db0bbc(PTR_native_AppPlugin_TypeInfo_01fbf828);
    DAT_020ff836 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  native_AppPlugin__Finish();
  return;
}



// ==========================================================================================
// Function: main_Main__GetJingle
// Address: 00f8181c
// ==========================================================================================

undefined8 main_Main__GetJingle(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_main_Main_TypeInfo_01fc33d8;
  if ((DAT_020ff838 & 1) == 0) {
    FUN_00db0bbc(PTR_main_Main_TypeInfo_01fc33d8);
    DAT_020ff838 = 1;
  }
  return **(undefined8 **)(*(long *)puVar1 + 0xb8);
}



// ==========================================================================================
// Function: main_Main__GetFormManager
// Address: 00f81864
// ==========================================================================================

long main_Main__GetFormManager(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_form_FormManager_TypeInfo_01fbf568;
  if ((DAT_020ff85a & 1) == 0) {
    FUN_00db0bbc(PTR_form_FormManager_TypeInfo_01fbf568);
    DAT_020ff85a = 1;
  }
  lVar2 = **(long **)(*(long *)puVar1 + 0xb8);
  if (lVar2 == 0) {
    lVar2 = thunk_FUN_00e11c14();
    kairo_unity_form_FormManagerBase___ctor(lVar2,0);
    *(undefined4 *)(lVar2 + 0xb0) = 0x14;
    *(undefined8 *)(lVar2 + 0x128) = 0xffffffffffffffff;
    **(long **)(*(long *)puVar1 + 0xb8) = lVar2;
    lVar2 = **(long **)(*(long *)puVar1 + 0xb8);
  }
  return lVar2;
}



// ==========================================================================================
// Function: main_NetSystem__SetUp
// Address: 00f81868
// ==========================================================================================

void main_NetSystem__SetUp(undefined8 param_1,undefined4 param_2,undefined4 param_3)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  int iVar6;
  undefined4 uVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  undefined4 *puVar11;
  
  puVar3 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff839 & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_423_01fc2c80);
    FUN_00db0bbc(PTR_StringLiteral_1427_01fc35e0);
    FUN_00db0bbc(PTR_StringLiteral_4669_01fc35e8);
    FUN_00db0bbc(PTR_StringLiteral_7712_01fc35f0);
    FUN_00db0bbc(PTR_StringLiteral_8807_01fc35f8);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    FUN_00db0bbc(PTR_StringLiteral_794_01fc3600);
    FUN_00db0bbc(PTR_StringLiteral_8831_01fc3608);
    FUN_00db0bbc(PTR_StringLiteral_1151_01fc3610);
    FUN_00db0bbc(PTR_StringLiteral_8837_01fc3618);
    DAT_020ff839 = 1;
  }
  puVar5 = PTR_StringLiteral_4669_01fc35e8;
  puVar2 = PTR_string___TypeInfo_01fbf2f8;
  lVar8 = *(long *)puVar3;
  if (*(int *)(lVar8 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar8 = *(long *)puVar3;
  }
  puVar11 = *(undefined4 **)(lVar8 + 0xb8);
  *puVar11 = param_2;
  puVar11[1] = param_3;
  uVar9 = java_lang_JSystem__GetProperty(*(undefined8 *)puVar5,0);
  *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 8) = uVar9;
  lVar8 = FUN_00db0c30(*(undefined8 *)puVar2,4);
  lVar10 = FUN_00db0c30(*(undefined8 *)puVar2,6);
  if (lVar10 == 0) goto LAB_00f81e20;
  uVar1 = *(uint *)(lVar10 + 0x18);
  if (((uVar1 != 0) &&
      (*(undefined8 *)(lVar10 + 0x20) = *(undefined8 *)PTR_StringLiteral_8831_01fc3608, uVar1 != 1))
     && (*(undefined8 *)(lVar10 + 0x28) = *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x20),
        puVar5 = PTR_StringLiteral_1427_01fc35e0, 2 < uVar1)) {
    *(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)PTR_StringLiteral_1427_01fc35e0;
    uVar9 = System_Int32__ToString(*(undefined8 *)(*(long *)puVar3 + 0xb8),0);
    if ((3 < *(uint *)(lVar10 + 0x18)) &&
       (*(undefined8 *)(lVar10 + 0x38) = uVar9, puVar4 = PTR_StringLiteral_423_01fc2c80,
       *(uint *)(lVar10 + 0x18) != 4)) {
      *(undefined8 *)(lVar10 + 0x40) = *(undefined8 *)PTR_StringLiteral_423_01fc2c80;
      uVar9 = System_Int32__ToString(*(long *)(*(long *)puVar3 + 0xb8) + 4,0);
      if (5 < *(uint *)(lVar10 + 0x18)) {
        *(undefined8 *)(lVar10 + 0x48) = uVar9;
        uVar9 = Method_System_String_Concat(lVar10,0);
        if (lVar8 == 0) {
LAB_00f81e20:
                    /* WARNING: Subroutine does not return */
          FUN_00db0de4();
        }
        if (*(int *)(lVar8 + 0x18) != 0) {
          *(undefined8 *)(lVar8 + 0x20) = uVar9;
          lVar10 = FUN_00db0c30(*(undefined8 *)puVar2,6);
          if (lVar10 == 0) goto LAB_00f81e20;
          uVar1 = *(uint *)(lVar10 + 0x18);
          if (((uVar1 != 0) &&
              (*(undefined8 *)(lVar10 + 0x20) = *(undefined8 *)PTR_StringLiteral_8807_01fc35f8,
              uVar1 != 1)) &&
             (*(undefined8 *)(lVar10 + 0x28) =
                   *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x20), 2 < uVar1)) {
            *(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)puVar5;
            uVar9 = System_Int32__ToString(*(undefined8 *)(*(long *)puVar3 + 0xb8),0);
            if ((3 < *(uint *)(lVar10 + 0x18)) &&
               (*(undefined8 *)(lVar10 + 0x38) = uVar9, *(uint *)(lVar10 + 0x18) != 4)) {
              *(undefined8 *)(lVar10 + 0x40) = *(undefined8 *)puVar4;
              uVar9 = System_Int32__ToString(*(long *)(*(long *)puVar3 + 0xb8) + 4,0);
              if (5 < *(uint *)(lVar10 + 0x18)) {
                *(undefined8 *)(lVar10 + 0x48) = uVar9;
                uVar9 = Method_System_String_Concat(lVar10,0);
                if (1 < *(uint *)(lVar8 + 0x18)) {
                  *(undefined8 *)(lVar8 + 0x28) = uVar9;
                  lVar10 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                  if (lVar10 == 0) goto LAB_00f81e20;
                  uVar1 = *(uint *)(lVar10 + 0x18);
                  if (((uVar1 != 0) &&
                      (*(undefined8 *)(lVar10 + 0x20) =
                            *(undefined8 *)PTR_StringLiteral_8837_01fc3618, uVar1 != 1)) &&
                     (*(undefined8 *)(lVar10 + 0x28) =
                           *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x20), 2 < uVar1)) {
                    *(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)puVar5;
                    uVar9 = System_Int32__ToString(*(undefined8 *)(*(long *)puVar3 + 0xb8),0);
                    if ((3 < *(uint *)(lVar10 + 0x18)) &&
                       (*(undefined8 *)(lVar10 + 0x38) = uVar9, *(uint *)(lVar10 + 0x18) != 4)) {
                      *(undefined8 *)(lVar10 + 0x40) = *(undefined8 *)puVar4;
                      uVar9 = System_Int32__ToString(*(long *)(*(long *)puVar3 + 0xb8) + 4,0);
                      if (5 < *(uint *)(lVar10 + 0x18)) {
                        *(undefined8 *)(lVar10 + 0x48) = uVar9;
                        uVar9 = Method_System_String_Concat(lVar10,0);
                        if (2 < *(uint *)(lVar8 + 0x18)) {
                          *(undefined8 *)(lVar8 + 0x30) = uVar9;
                          lVar10 = FUN_00db0c30(*(undefined8 *)puVar2,6);
                          if (lVar10 == 0) goto LAB_00f81e20;
                          uVar1 = *(uint *)(lVar10 + 0x18);
                          if (((uVar1 != 0) &&
                              (*(undefined8 *)(lVar10 + 0x20) =
                                    *(undefined8 *)PTR_StringLiteral_7712_01fc35f0, uVar1 != 1)) &&
                             (*(undefined8 *)(lVar10 + 0x28) =
                                   *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x20),
                             2 < uVar1)) {
                            *(undefined8 *)(lVar10 + 0x30) = *(undefined8 *)puVar5;
                            uVar9 = System_Int32__ToString
                                              (*(undefined8 *)(*(long *)puVar3 + 0xb8),0);
                            if ((3 < *(uint *)(lVar10 + 0x18)) &&
                               (*(undefined8 *)(lVar10 + 0x38) = uVar9,
                               *(uint *)(lVar10 + 0x18) != 4)) {
                              *(undefined8 *)(lVar10 + 0x40) = *(undefined8 *)puVar4;
                              uVar9 = System_Int32__ToString
                                                (*(long *)(*(long *)puVar3 + 0xb8) + 4,0);
                              if (5 < *(uint *)(lVar10 + 0x18)) {
                                *(undefined8 *)(lVar10 + 0x48) = uVar9;
                                uVar9 = Method_System_String_Concat(lVar10,0);
                                if (3 < *(uint *)(lVar8 + 0x18)) {
                                  *(undefined8 *)(lVar8 + 0x38) = uVar9;
                                  lVar10 = *(long *)(*(long *)puVar3 + 0xb8);
                                  *(long *)(lVar10 + 0x60) = lVar8;
                                  puVar2 = PTR_StringLiteral_7857_01fc3620;
                                  if ((DAT_020ff83c & 1) == 0) {
                                    FUN_00db0bbc(PTR_StringLiteral_7857_01fc3620);
                                    DAT_020ff83c = 1;
                                    lVar10 = *(long *)(*(long *)puVar3 + 0xb8);
                                  }
                                  lVar8 = *(long *)puVar2;
                                  *(long *)(lVar10 + 0x28) = lVar8;
                                  if (lVar8 != 0) {
                                    iVar6 = System_String__LastIndexOf(lVar8,0x2f,0);
                                    lVar8 = java_lang_StringEx__SubstringJ(lVar8,0,iVar6 + 1,0);
                                    *(long *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x28) = lVar8;
                                    puVar4 = PTR_StringLiteral_1151_01fc3610;
                                    puVar5 = PTR_StringLiteral_794_01fc3600;
                                    puVar2 = PTR_StringLiteral_838_01fbf908;
                                    if (lVar8 != 0) {
                                      uVar7 = System_String__IndexOf
                                                        (lVar8,*(undefined8 *)
                                                                PTR_StringLiteral_838_01fbf908,7,0);
                                      uVar9 = java_lang_StringEx__SubstringJ(lVar8,0,uVar7,0);
                                      uVar9 = System_String__Concat(uVar9,*(undefined8 *)puVar2,0);
                                      lVar8 = *(long *)(*(long *)puVar3 + 0xb8);
                                      *(undefined8 *)(lVar8 + 0x30) = uVar9;
                                      uVar9 = System_String__Concat
                                                        (*(undefined8 *)(lVar8 + 0x28),
                                                         *(undefined8 *)puVar5,0);
                                      lVar8 = *(long *)(*(long *)puVar3 + 0xb8);
                                      *(undefined8 *)(lVar8 + 0x38) = uVar9;
                                      uVar9 = System_String__Concat
                                                        (*(undefined8 *)(lVar8 + 0x28),
                                                         *(undefined8 *)puVar4,0);
                                      *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x40) =
                                           uVar9;
                                      uVar9 = main_NetSystem__GetSiteURL();
                                      lVar8 = *(long *)(*(long *)puVar3 + 0xb8);
                                      *(undefined8 *)(lVar8 + 0x48) = uVar9;
                                      puVar2 = PTR_StringLiteral_7861_01fc3628;
                                      if ((DAT_020ff83d & 1) == 0) {
                                        FUN_00db0bbc(PTR_StringLiteral_7861_01fc3628);
                                        DAT_020ff83d = 1;
                                        lVar8 = *(long *)(*(long *)puVar3 + 0xb8);
                                      }
                                      *(undefined8 *)(lVar8 + 0x50) = *(undefined8 *)puVar2;
                                      uVar9 = main_NetSystem__GetSpInOutUrl();
                                      *(undefined8 *)(*(long *)(*(long *)puVar3 + 0xb8) + 0x58) =
                                           uVar9;
                                      return;
                                    }
                                  }
                                  goto LAB_00f81e20;
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



// ==========================================================================================
// Function: main_NetSystem__GetSourceURL
// Address: 00f81e24
// ==========================================================================================

undefined8 main_NetSystem__GetSourceURL(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_StringLiteral_7857_01fc3620;
  if ((DAT_020ff83c & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_7857_01fc3620);
    DAT_020ff83c = 1;
  }
  return *(undefined8 *)puVar1;
}



// ==========================================================================================
// Function: main_NetSystem__GetSiteURL
// Address: 00f81e64
// ==========================================================================================

void main_NetSystem__GetSiteURL(void)

{
  undefined8 *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  ulong uVar5;
  undefined8 uVar6;
  long lVar7;
  
  puVar3 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_020ff83b & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_StringLiteral_7850_01fc3630);
    FUN_00db0bbc(PTR_StringLiteral_7849_01fc3638);
    FUN_00db0bbc(PTR_StringLiteral_394_01fc3640);
    DAT_020ff83b = 1;
  }
  puVar2 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar4 = PTR_StringLiteral_394_01fc3640;
  puVar1 = (undefined8 *)PTR_StringLiteral_7849_01fc3638;
  puVar3 = PTR_StringLiteral_7850_01fc3630;
  uVar5 = kairo_unity_util_Language__Japanese(0);
  lVar7 = *(long *)puVar2;
  if (*(int *)(lVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar7);
    lVar7 = *(long *)puVar2;
  }
  uVar6 = System_Int32__ToString(*(long *)(lVar7 + 0xb8) + 0x10c,0);
  if ((uVar5 & 1) == 0) {
    puVar1 = (undefined8 *)puVar3;
  }
  System_String__Concat(*puVar1,uVar6,*(undefined8 *)puVar4,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__GetVersionURL
// Address: 00f81f58
// ==========================================================================================

undefined8 main_NetSystem__GetVersionURL(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_StringLiteral_7861_01fc3628;
  if ((DAT_020ff83d & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_7861_01fc3628);
    DAT_020ff83d = 1;
  }
  return *(undefined8 *)puVar1;
}



// ==========================================================================================
// Function: main_NetSystem__GetSpInOutUrl
// Address: 00f81f98
// ==========================================================================================

void main_NetSystem__GetSpInOutUrl(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  undefined8 uVar5;
  
  puVar2 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff83a & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_7848_01fc3648);
    FUN_00db0bbc(PTR_StringLiteral_838_01fbf908);
    DAT_020ff83a = 1;
  }
  puVar3 = PTR_StringLiteral_7848_01fc3648;
  puVar1 = PTR_StringLiteral_838_01fbf908;
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  uVar5 = System_Int32__ToString(*(undefined8 *)(lVar4 + 0xb8),0);
  System_String__Concat(*(undefined8 *)puVar3,uVar5,*(undefined8 *)puVar1,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__GetMarketURL
// Address: 00f82030
// ==========================================================================================

undefined8 main_NetSystem__GetMarketURL(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar1 = PTR_kairo_unity_util_Language_TypeInfo_01fbf348;
  if ((DAT_020ff83e & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_util_Language_TypeInfo_01fbf348);
    FUN_00db0bbc(PTR_StringLiteral_8352_01fc3650);
    DAT_020ff83e = 1;
  }
  puVar2 = PTR_StringLiteral_8352_01fc3650;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  kairo_unity_util_Language__Japanese(0);
  return *(undefined8 *)puVar2;
}



// ==========================================================================================
// Function: main_NetSystem__GetCgiUrl
// Address: 00f8209c
// ==========================================================================================

void main_NetSystem__GetCgiUrl(uint param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  long lVar5;
  
  puVar1 = PTR_kairo_common_cfg_Config_TypeInfo_01fbf338;
  if ((DAT_020ff83f & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_common_cfg_Config_TypeInfo_01fbf338);
    FUN_00db0bbc(PTR_kairo_unity_util_Log_TypeInfo_01fbf340);
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    DAT_020ff83f = 1;
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if (*(char *)(*(long *)(lVar3 + 0xb8) + 0x17) != '\0') {
    lVar3 = *(long *)PTR_main_NetSystem_TypeInfo_01fc2c78;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    puVar2 = PTR_kairo_unity_util_Log_TypeInfo_01fbf340;
    lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x60);
    if (lVar5 == 0) goto LAB_00f821c8;
    if (*(uint *)(lVar5 + 0x18) <= param_1) goto LAB_00f821cc;
    uVar4 = System_String__Concat
                      (*(undefined8 *)(*(long *)(lVar3 + 0xb8) + 0x38),
                       *(undefined8 *)(lVar5 + (long)(int)param_1 * 8 + 0x20),0);
    if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar2);
    }
    kairo_unity_util_Log__Info(uVar4,0,0);
  }
  lVar3 = *(long *)puVar1;
  if (*(int *)(lVar3 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)puVar1;
  }
  lVar5 = *(long *)(*(long *)(lVar3 + 0xb8) + 0x60);
  if (lVar5 != 0) {
    if (param_1 < *(uint *)(lVar5 + 0x18)) {
      System_String__Concat
                (*(undefined8 *)(*(long *)(lVar3 + 0xb8) + 0x38),
                 *(undefined8 *)(lVar5 + (long)(int)param_1 * 8 + 0x20),0);
      return;
    }
LAB_00f821cc:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
LAB_00f821c8:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_NetSystem__CgiRegist
// Address: 00f821d0
// ==========================================================================================

void main_NetSystem__CgiRegist(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff840 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    DAT_020ff840 = 1;
  }
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = main_NetSystem__CgiRegistURL(param_1,param_2);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar3,0,1,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__CgiRegistURL
// Address: 00f82274
// ==========================================================================================

void main_NetSystem__CgiRegistURL(undefined8 param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff841 & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_382_01fc3378);
    DAT_020ff841 = 1;
  }
  puVar3 = PTR_StringLiteral_382_01fc3378;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar4 = main_NetSystem__MakeQuery(*(undefined8 *)puVar3,param_1);
  uVar5 = main_NetSystem__MakeQuery(*(undefined8 *)puVar2,param_2);
  uVar6 = main_NetSystem__GetCgiUrl(0);
  System_String__Concat(uVar6,uVar4,uVar5,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__MakeQuery
// Address: 00f82330
// ==========================================================================================

undefined8 main_NetSystem__MakeQuery(undefined8 param_1,long param_2)

{
  undefined8 uVar1;
  
  if ((DAT_020ff848 & 1) == 0) {
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff848 = 1;
  }
  if (param_2 != 0) {
    uVar1 = System_String__Concat(param_1,param_2,0);
    return uVar1;
  }
  return *(undefined8 *)PTR_StringLiteral_1_01fbf388;
}



// ==========================================================================================
// Function: main_NetSystem__CgiGetScore
// Address: 00f82394
// ==========================================================================================

void main_NetSystem__CgiGetScore(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff842 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    DAT_020ff842 = 1;
  }
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = main_NetSystem__CgiGetScoreURL(param_1);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar3,0,0,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__CgiGetScoreURL
// Address: 00f82428
// ==========================================================================================

void main_NetSystem__CgiGetScoreURL(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff843 & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    DAT_020ff843 = 1;
  }
  puVar2 = PTR_StringLiteral_407_01fc3380;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = main_NetSystem__MakeQuery(*(undefined8 *)puVar2,param_1);
  uVar4 = main_NetSystem__GetCgiUrl(3);
  System_String__Concat(uVar4,uVar3,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__CgiRegistScoreURL
// Address: 00f824ac
// ==========================================================================================

void main_NetSystem__CgiRegistScoreURL(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff844 & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    FUN_00db0bbc(PTR_StringLiteral_417_01fc3388);
    DAT_020ff844 = 1;
  }
  puVar4 = PTR_StringLiteral_417_01fc3388;
  puVar3 = PTR_StringLiteral_407_01fc3380;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = main_NetSystem__MakeQuery(*(undefined8 *)puVar3,param_1);
  uVar6 = main_NetSystem__MakeQuery(*(undefined8 *)puVar4,param_2);
  uVar7 = main_NetSystem__MakeQuery(*(undefined8 *)puVar2,param_3);
  uVar8 = main_NetSystem__GetCgiUrl(2);
  System_String__Concat(uVar8,uVar5,uVar6,uVar7,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__CgiRanking
// Address: 00f825a0
// ==========================================================================================

void main_NetSystem__CgiRanking(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff845 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    DAT_020ff845 = 1;
  }
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = main_NetSystem__CgiRankingURL(param_1,param_2,param_3);
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar1);
  }
  kairo_unity_io_Http__Connect(uVar3,0,0,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__CgiRankingURL
// Address: 00f8264c
// ==========================================================================================

void main_NetSystem__CgiRankingURL(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff846 & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_413_01fc3370);
    FUN_00db0bbc(PTR_StringLiteral_409_01fc3390);
    FUN_00db0bbc(PTR_StringLiteral_407_01fc3380);
    DAT_020ff846 = 1;
  }
  puVar4 = PTR_StringLiteral_409_01fc3390;
  puVar3 = PTR_StringLiteral_407_01fc3380;
  puVar2 = PTR_StringLiteral_413_01fc3370;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = main_NetSystem__MakeQuery(*(undefined8 *)puVar3,param_1);
  uVar6 = main_NetSystem__MakeQuery(*(undefined8 *)puVar2,param_2);
  uVar7 = main_NetSystem__MakeQuery(*(undefined8 *)puVar4,param_3);
  uVar8 = main_NetSystem__GetCgiUrl(1);
  System_String__Concat(uVar8,uVar5,uVar6,uVar7,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem__GetHttpErrorText
// Address: 00f82740
// ==========================================================================================

undefined8 main_NetSystem__GetHttpErrorText(void)

{
  undefined *puVar1;
  undefined *puVar2;
  long lVar3;
  undefined8 uVar4;
  
  puVar2 = PTR_StringLiteral_12180_01fc33e0;
  puVar1 = PTR_kairo_unity_io_Http_TypeInfo_01fbf960;
  if ((DAT_020ff847 & 1) == 0) {
    FUN_00db0bbc(PTR_kairo_unity_io_Http_TypeInfo_01fbf960);
    FUN_00db0bbc(PTR_StringLiteral_12180_01fc33e0);
    DAT_020ff847 = 1;
  }
  uVar4 = *(undefined8 *)puVar2;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  lVar3 = kairo_unity_io_Http__GetErrorText(0);
  if (lVar3 != 0) {
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar4 = kairo_unity_io_Http__GetErrorText(0);
    return uVar4;
  }
  return uVar4;
}



// ==========================================================================================
// Function: main_NetSystem__Split
// Address: 00f827d4
// ==========================================================================================

long main_NetSystem__Split(long param_1,undefined8 param_2)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  int iVar7;
  int iVar8;
  undefined4 uVar9;
  long lVar10;
  undefined8 uVar11;
  long lVar12;
  long *plVar13;
  ulong uVar14;
  undefined8 uVar15;
  
  puVar2 = PTR_java_util_Vector_TypeInfo_01fbf3b8;
  if ((DAT_020ff849 & 1) == 0) {
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_string_TypeInfo_01fbfd50);
    FUN_00db0bbc(PTR_Method_java_util_Vector_object__AddElement_01fbf3a8);
    FUN_00db0bbc(PTR_Method_java_util_Vector_object__ElementAt_01fbf3b0);
    FUN_00db0bbc(PTR_Method_java_util_Vector_object__Size_01fbf308);
    FUN_00db0bbc(PTR_java_util_Vector_TypeInfo_01fbf3b8);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff849 = 1;
  }
  lVar10 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  java_util_Vector___ctor(lVar10,0);
  puVar6 = PTR_string_TypeInfo_01fbfd50;
  puVar5 = PTR_Method_java_util_Vector_object__ElementAt_01fbf3b0;
  puVar4 = PTR_Method_java_util_Vector_object__AddElement_01fbf3a8;
  puVar3 = PTR_StringLiteral_1_01fbf388;
  puVar2 = PTR_Method_java_util_Vector_object__Size_01fbf308;
  if (param_1 != 0) {
    iVar8 = 0;
    do {
      uVar15 = *(undefined8 *)puVar3;
      iVar7 = System_String__IndexOf(param_1,param_2,iVar8,0);
      if (iVar7 == -1) {
        uVar11 = java_lang_StringEx__SubstringJ(param_1,iVar8,0);
        lVar12 = System_String__Concat(uVar15,uVar11,0);
      }
      else {
        uVar11 = java_lang_StringEx__SubstringJ(param_1,iVar8,iVar7,0);
        lVar12 = System_String__Concat(uVar15,uVar11,0);
        iVar8 = java_lang_StringEx__Length(param_2,0);
        iVar8 = iVar8 + iVar7;
      }
      if ((lVar12 == 0) || (uVar15 = System_String__Trim(lVar12,0), lVar10 == 0)) goto LAB_00f829fc;
      Method_java_util_Vector_object__AddElement(lVar10,uVar15,*(undefined8 *)puVar4);
    } while (iVar7 != -1);
    uVar9 = Method_java_util_Vector_object__Size(lVar10,*(undefined8 *)puVar2);
    lVar12 = FUN_00db0c30(*(undefined8 *)PTR_string___TypeInfo_01fbf2f8,uVar9);
    if (lVar12 != 0) {
      if (0 < *(int *)(lVar12 + 0x18)) {
        uVar14 = 0;
        do {
          plVar13 = (long *)Method_java_util_Vector_object__ElementAt
                                      (lVar10,uVar14 & 0xffffffff,*(undefined8 *)puVar5);
          if ((plVar13 != (long *)0x0) && (*plVar13 != *(long *)puVar6)) {
                    /* WARNING: Subroutine does not return */
            FUN_00db1180();
          }
          uVar1 = *(uint *)(lVar12 + 0x18);
          if (uVar1 <= uVar14) {
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          *(long **)(lVar12 + 0x20 + uVar14 * 8) = plVar13;
          uVar14 = uVar14 + 1;
        } while ((long)uVar14 < (long)(int)uVar1);
      }
      return lVar12;
    }
  }
LAB_00f829fc:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_NetSystem__CommaSeparate
// Address: 00f82a08
// ==========================================================================================

long main_NetSystem__CommaSeparate(long param_1)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  long lVar7;
  int iVar8;
  undefined2 local_54 [2];
  long local_48;
  
  local_48 = param_1;
  if ((DAT_020ff84a & 1) == 0) {
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_StringLiteral_678_01fbf998);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    FUN_00db0bbc(PTR_StringLiteral_1_01fbf388);
    DAT_020ff84a = 1;
  }
  puVar2 = PTR_StringLiteral_1_01fbf388;
  local_54[0] = 0;
  if (param_1 < 0) {
    local_48 = -param_1;
  }
  lVar5 = System_Int64__ToString(&local_48,0);
  lVar7 = *(long *)puVar2;
  lVar1 = lVar7;
  if (lVar5 != 0) {
    lVar1 = lVar5;
  }
  iVar4 = java_lang_StringEx__Length(lVar1,0);
  puVar3 = PTR_char_TypeInfo_01fbf990;
  puVar2 = PTR_StringLiteral_646_01fbf440;
  iVar4 = iVar4 + -1;
  if (-1 < iVar4) {
    iVar8 = 0;
    do {
      if ((0 < iVar8) && (iVar8 % 3 == 0)) {
        lVar7 = System_String__Concat(*(undefined8 *)puVar2,lVar7,0);
      }
      local_54[0] = java_lang_StringEx__CharAt(lVar1,iVar4,0);
      if (*(int *)(*(long *)puVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar3);
      }
      uVar6 = System_Char__ToString(local_54,0);
      lVar7 = System_String__Concat(uVar6,lVar7,0);
      iVar4 = iVar4 + -1;
      iVar8 = iVar8 + 1;
    } while (iVar4 != -1);
  }
  if (param_1 < 0) {
    lVar7 = System_String__Concat(*(undefined8 *)PTR_StringLiteral_678_01fbf998,lVar7,0);
  }
  return lVar7;
}



// ==========================================================================================
// Function: main_NetSystem__GetCmId
// Address: 00f82b94
// ==========================================================================================

undefined8 main_NetSystem__GetCmId(void)

{
  return 0xffffffff;
}



// ==========================================================================================
// Function: main_NetSystem__SetCmId
// Address: 00f82b9c
// ==========================================================================================

void main_NetSystem__SetCmId(void)

{
  return;
}



// ==========================================================================================
// Function: main_NetSystem__UpdateScoreFromNetwork
// Address: 00f82ba0
// ==========================================================================================

undefined8 main_NetSystem__UpdateScoreFromNetwork(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 uVar4;
  long lVar5;
  ulong uVar6;
  ulong uVar7;
  
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff84b & 1) == 0) {
    FUN_00db0bbc(PTR_java_lang_JString_TypeInfo_01fbf368);
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_45_01fbf350);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    FUN_00db0bbc(PTR_StringLiteral_927_01fbff50);
    DAT_020ff84b = 1;
  }
  puVar3 = PTR_StringLiteral_927_01fbff50;
  puVar2 = PTR_java_lang_JString_TypeInfo_01fbf368;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  puVar1 = PTR_StringLiteral_45_01fbf350;
  uVar4 = main_NetSystem__CgiGetScore(*(undefined8 *)puVar3);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  uVar4 = java_lang_JString__New(uVar4,0);
  lVar5 = main_NetSystem__Split(uVar4,*(undefined8 *)puVar1);
  if (lVar5 != 0) {
    if (*(uint *)(lVar5 + 0x18) < 2) {
LAB_00f82cf4:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar5 = main_NetSystem__Split
                      (*(undefined8 *)(lVar5 + 0x28),*(undefined8 *)PTR_StringLiteral_646_01fbf440);
    if (lVar5 != 0) {
      if ((int)*(ulong *)(lVar5 + 0x18) < 1) {
        uVar4 = 0;
      }
      else {
        uVar7 = 0;
        uVar6 = *(ulong *)(lVar5 + 0x18) & 0xffffffff;
        do {
          if (uVar6 <= uVar7) goto LAB_00f82cf4;
          uVar4 = java_lang_StringEx__Length(*(undefined8 *)(lVar5 + 0x20 + uVar7 * 8),0);
          if ((int)uVar4 != 0) {
            if (*(uint *)(lVar5 + 0x18) <= uVar7) goto LAB_00f82cf4;
            uVar4 = java_lang_JInteger__ParseInt(*(undefined8 *)(lVar5 + 0x20 + uVar7 * 8),0);
          }
          uVar6 = (ulong)*(uint *)(lVar5 + 0x18);
          uVar7 = uVar7 + 1;
        } while ((long)uVar7 < (long)(int)*(uint *)(lVar5 + 0x18));
      }
      return uVar4;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: main_NetSystem___ctor
// Address: 00f82cfc
// ==========================================================================================

void main_NetSystem___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: main_NetSystem___cctor
// Address: 00f82d04
// ==========================================================================================

void main_NetSystem___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  puVar3 = PTR_StringLiteral_6944_01fc3660;
  puVar2 = PTR_StringLiteral_9367_01fc3658;
  puVar1 = PTR_main_NetSystem_TypeInfo_01fc2c78;
  if ((DAT_020ff84c & 1) == 0) {
    FUN_00db0bbc(PTR_main_NetSystem_TypeInfo_01fc2c78);
    FUN_00db0bbc(PTR_StringLiteral_9367_01fc3658);
    FUN_00db0bbc(PTR_StringLiteral_6944_01fc3660);
    DAT_020ff84c = 1;
  }
  puVar4 = *(undefined8 **)(*(long *)puVar1 + 0xb8);
  *puVar4 = 0xffffff9dffffff9d;
  puVar4[1] = 0;
  puVar4[2] = 0;
  uVar6 = *(undefined8 *)puVar2;
  uVar5 = *(undefined8 *)puVar3;
  puVar4[6] = 0;
  puVar4[5] = 0;
  puVar4[8] = 0;
  puVar4[7] = 0;
  puVar4[10] = 0;
  puVar4[9] = 0;
  puVar4[3] = uVar6;
  puVar4[4] = uVar5;
  puVar4[0xc] = 0;
  puVar4[0xb] = 0;
  return;
}



// ==========================================================================================
