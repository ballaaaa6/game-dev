// Function: _FINI_0
// Address: 00c811ac
// ==========================================================================================

void _FINI_0(void)

{
  FUN_00ead0f0();
  return;
}



// ==========================================================================================
// Function: _INIT_0
// Address: 00dabe00
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _INIT_0(void)

{
  undefined auStack_60 [8];
  undefined auStack_58 [8];
  undefined auStack_50 [8];
  undefined auStack_48 [8];
  undefined auStack_40 [8];
  undefined auStack_38 [8];
  undefined auStack_30 [8];
  undefined auStack_28 [8];
  
  DAT_021071b0 = 0;
  DAT_021071b8 = 0;
  DAT_021071c0 = 0;
  __cxa_atexit(FUN_00da576c,&DAT_021071b0,&PTR_LOOP_01ecb1d0);
  FUN_00da6468(&DAT_021071c8,0,auStack_58,auStack_60);
  __cxa_atexit(FUN_00da64c0,&DAT_021071c8,&PTR_LOOP_01ecb1d0);
  FUN_00da64dc(&DAT_02107238,0,auStack_48,auStack_50);
  __cxa_atexit(FUN_00da6534,&DAT_02107238,&PTR_LOOP_01ecb1d0);
  FUN_00da74e4(&DAT_021072b0,0,auStack_38,auStack_40);
  __cxa_atexit(FUN_00da64c0,&DAT_021072b0,&PTR_LOOP_01ecb1d0);
  FUN_00da74e4(&DAT_02107320,0,auStack_28,auStack_30);
  __cxa_atexit(FUN_00da64c0,&DAT_02107320,&PTR_LOOP_01ecb1d0);
  uRam0000000002107398 = 0;
  _DAT_02107390 = 0;
  uRam00000000021073a8 = 0;
  DAT_021073a0 = 0;
  uRam00000000021073b8 = 0;
  _DAT_021073b0 = 0;
  uRam00000000021073c8 = 0;
  _DAT_021073c0 = 0;
  uRam00000000021073d8 = 0;
  _DAT_021073d0 = 0;
  _DAT_021073e8 = 0;
  _DAT_021073e0 = 0;
  uRam00000000021073f8 = 0;
  _DAT_021073f0 = 0;
  return;
}



// ==========================================================================================
// Function: _INIT_1
// Address: 00dae590
// ==========================================================================================

void _INIT_1(void)

{
  DAT_02107400 = 0;
  DAT_02107440 = 0;
  DAT_02107448 = 0;
  FUN_00dae488(&DAT_02107470,&DAT_005d824c,&DAT_005c099b);
                    /* try { // try from 00dae5d8 to 00dae6ab has its CatchHandler @ 00dae6d0 */
  FUN_00dae488(&DAT_021074a0,&DAT_005d824c,&DAT_005c099f);
  FUN_00dae488(&DAT_021074d0,&DAT_005d824c,".dylib");
  FUN_00dae488(&DAT_02107500,&DAT_005d824c,".bundle");
  FUN_00dae488(&DAT_02107530,&DAT_005c1559,&DAT_005c099b);
  FUN_00dae488(&DAT_02107560,&DAT_005c1559,&DAT_005c099f);
  FUN_00dae488(&DAT_02107590,&DAT_005c1559,".dylib");
  FUN_00dae488(&DAT_021075c0,&DAT_005c1559,".bundle");
  __cxa_atexit(FUN_00dae540,0,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_2
// Address: 00db0674
// ==========================================================================================

void _INIT_2(void)

{
  DAT_02107610 = 0;
  DAT_02107650 = 0;
  DAT_02107658 = 0;
  DAT_02107668 = 0;
  DAT_02107670 = 0;
  DAT_02107660 = &DAT_02107668;
  __cxa_atexit(FUN_00daf9fc,&DAT_02107660,&PTR_LOOP_01ecb1d0);
  DAT_02107680 = 0;
  DAT_02107688 = 0;
  DAT_02107678 = &DAT_02107680;
  __cxa_atexit(FUN_00daf9fc,&DAT_02107678,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_3
// Address: 00db0b30
// ==========================================================================================

void _INIT_3(void)

{
  DAT_02107690 = 0;
  DAT_02107698 = 0;
  DAT_021076a0 = 0;
  __cxa_atexit(FUN_00db0840,&DAT_02107690,&PTR_LOOP_01ecb1d0);
  DAT_021076a8 = 0;
  DAT_021076e8 = 0;
  DAT_021076f0 = 0;
  return;
}



// ==========================================================================================
// Function: _INIT_4
// Address: 00dc7bd0
// ==========================================================================================

void _INIT_4(void)

{
  DAT_021076f8 = 0;
  DAT_02107700 = 0;
  DAT_02107708 = 0;
  __cxa_atexit(thunk_FUN_00d9e330,&DAT_021076f8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_5
// Address: 00dca53c
// ==========================================================================================

void _INIT_5(void)

{
  memset(&DAT_02107738,0,0x8c);
  __cxa_atexit(FUN_00dc8d74,&DAT_02107738,&PTR_LOOP_01ecb1d0);
  DAT_021077c8 = 0;
  DAT_021077d0 = 0;
  DAT_021077d8 = 0;
  __cxa_atexit(FUN_00dc958c,&DAT_021077c8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_6
// Address: 00dcbcf8
// ==========================================================================================

void _INIT_6(void)

{
  pthread_key_t *ppVar1;
  pthread_key_t local_1c;
  pthread_key_t local_18;
  pthread_key_t local_14;
  
  ppVar1 = (pthread_key_t *)operator_new(4);
                    /* try { // try from 00dcbd0c to 00dcbd17 has its CatchHandler @ 00dcbe44 */
  pthread_key_create(&local_1c,(__destr_function *)0x0);
  DAT_02107800 = ppVar1;
  *ppVar1 = local_1c;
  __cxa_atexit(FUN_00dca670,&DAT_02107800,&PTR_LOOP_01ecb1d0);
  DAT_02107810 = 0;
  DAT_02107818 = 0;
  DAT_02107808 = 0;
  __cxa_atexit(thunk_FUN_00dcbacc,&DAT_02107808,&PTR_LOOP_01ecb1d0);
  DAT_02107820 = 0;
  DAT_02107860 = 0;
  DAT_02107868 = 0;
  ppVar1 = (pthread_key_t *)operator_new(4);
                    /* try { // try from 00dcbd84 to 00dcbd8f has its CatchHandler @ 00dcbe40 */
  pthread_key_create(&local_18,(__destr_function *)0x0);
  *ppVar1 = local_18;
  DAT_02107878 = ppVar1;
  __cxa_atexit(FUN_00dca670,&DAT_02107878,&PTR_LOOP_01ecb1d0);
  ppVar1 = (pthread_key_t *)operator_new(4);
                    /* try { // try from 00dcbdc4 to 00dcbdcf has its CatchHandler @ 00dcbe3c */
  pthread_key_create(&local_14,(__destr_function *)0x0);
  DAT_02107880 = ppVar1;
  *ppVar1 = local_14;
  __cxa_atexit(FUN_00dca670,&DAT_02107880,&PTR_LOOP_01ecb1d0);
  DAT_02107888 = 0;
  DAT_021078c8 = 0;
  DAT_021078d0 = 0;
  DAT_021078e0 = 0;
  DAT_021078e8 = 0;
  DAT_021078d8 = 0;
  __cxa_atexit(FUN_00dcb580,&DAT_021078d8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_7
// Address: 00dd7bec
// ==========================================================================================

void _INIT_7(void)

{
  pthread_key_t *ppVar1;
  pthread_key_t local_18;
  pthread_key_t local_14;
  
  DAT_021079d0 = 0;
  DAT_021079d8 = 0;
  DataMemoryBarrier(2,3);
  __cxa_atexit(FUN_00dd1964,&DAT_02107990,&PTR_LOOP_01ecb1d0);
  DAT_02107a50 = 0;
  DAT_02107a58 = 0;
  DataMemoryBarrier(2,3);
  __cxa_atexit(FUN_00dd19b0,&DAT_02107a10,&PTR_LOOP_01ecb1d0);
  DAT_02107a98 = 0;
  DAT_02107ad8 = 0;
  DAT_02107ae0 = 0;
  DAT_02107af0 = 0;
  DAT_02107af8 = 0;
  DAT_02107ae8 = 0;
  __cxa_atexit(FUN_00da576c,&DAT_02107ae8,&PTR_LOOP_01ecb1d0);
  ppVar1 = (pthread_key_t *)operator_new(4);
                    /* try { // try from 00dd7c7c to 00dd7c87 has its CatchHandler @ 00dd7d08 */
  pthread_key_create(&local_18,(__destr_function *)0x0);
  *ppVar1 = local_18;
  DAT_02107b00 = ppVar1;
  __cxa_atexit(FUN_00dca670,&DAT_02107b00,&PTR_LOOP_01ecb1d0);
  ppVar1 = (pthread_key_t *)operator_new(4);
                    /* try { // try from 00dd7cbc to 00dd7cc7 has its CatchHandler @ 00dd7d04 */
  pthread_key_create(&local_14,(__destr_function *)0x0);
  *ppVar1 = local_14;
  DAT_02107b08 = ppVar1;
  __cxa_atexit(FUN_00dca670,&DAT_02107b08,&PTR_LOOP_01ecb1d0);
  DAT_02107b10 = 0;
  return;
}



// ==========================================================================================
// Function: _INIT_8
// Address: 00dea9d8
// ==========================================================================================

void _INIT_8(void)

{
  FUN_00e27e58(&DAT_02107c58,0);
  __cxa_atexit(PTR_FUN_01ff5510,&DAT_02107c58,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_9
// Address: 00df152c
// ==========================================================================================

void _INIT_9(void)

{
  DAT_02107c60 = 0;
  DAT_02107ca0 = 0;
  DAT_02107ca8 = 0;
  DAT_02107cb0 = 0;
  DAT_02107cf0 = 0;
  DAT_02107cf8 = 0;
  DAT_02107d08 = 0;
  DAT_02107d10 = 0;
  DAT_02107d00 = 0;
  __cxa_atexit(thunk_FUN_00df0d6c,&DAT_02107d00,&PTR_LOOP_01ecb1d0);
  DAT_02107d20 = 0;
  DAT_02107d28 = 0;
  DAT_02107d18 = &DAT_02107d20;
  __cxa_atexit(FUN_00daf9fc,&DAT_02107d18,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_10
// Address: 00df7668
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _INIT_10(void)

{
  DAT_02108038 = 0;
  DAT_02108078 = 0;
  DAT_02108080 = 0;
  DAT_02108088 = 0;
  DAT_021080c8 = 0;
  DAT_021080d0 = 0;
  DAT_021080e0 = 0;
  DAT_021080e8 = 0;
  _DAT_021080d8 = 0;
  __cxa_atexit(PTR__basic_string_01ff5530,&DAT_021080d8,&PTR_LOOP_01ecb1d0);
  DAT_02108120 = 0;
  DAT_02108160 = 0;
  DAT_02108168 = 0;
  FUN_00df739c(&DAT_02108178);
  __cxa_atexit(FUN_00df6a04,&DAT_02108178,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_11
// Address: 00df8ca8
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _INIT_11(void)

{
  undefined *puVar1;
  
  puVar1 = PTR__basic_string_01ff5530;
  DAT_02108190 = 0;
  DAT_02108198 = 0;
  DAT_021081a0 = 0;
  __cxa_atexit(PTR__basic_string_01ff5530,&DAT_02108190,&PTR_LOOP_01ecb1d0);
  DAT_021081b0 = 0;
  DAT_021081b8 = 0;
  _DAT_021081a8 = 0;
  __cxa_atexit(puVar1,&DAT_021081a8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_12
// Address: 00e09258
// ==========================================================================================

void _INIT_12(void)

{
  undefined auStack_28 [8];
  undefined auStack_18 [8];
  
  DAT_021082b8 = 0;
  DAT_021082c0 = 0;
  DAT_021082c8 = 0;
  __cxa_atexit(FUN_00dfc7fc,&DAT_021082b8,&PTR_LOOP_01ecb1d0);
  FUN_00dfcd24(&DAT_021082d0,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_021082d0,&PTR_LOOP_01ecb1d0);
  FUN_00dffe8c(&DAT_02108338,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108338,&PTR_LOOP_01ecb1d0);
  FUN_00dca908(&DAT_021083a0);
                    /* try { // try from 00e092fc to 00e0930f has its CatchHandler @ 00e094a4 */
  FUN_00e0219c(&DAT_021083a8,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dffef0,&DAT_021083a0,&PTR_LOOP_01ecb1d0);
  FUN_00dfff20(&DAT_02108418,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00da64c0,&DAT_02108418,&PTR_LOOP_01ecb1d0);
  FUN_00dfff78(&DAT_02108488,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108488,&PTR_LOOP_01ecb1d0);
  FUN_00dfffdc(&DAT_021084f0,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_021084f0,&PTR_LOOP_01ecb1d0);
  FUN_00e00040(&DAT_02108558,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108558,&PTR_LOOP_01ecb1d0);
  FUN_00e000a4(&DAT_021085c0,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_021085c0,&PTR_LOOP_01ecb1d0);
  DAT_02108628 = 0;
  DAT_02108630 = 0;
  DAT_02108638 = 0;
  __cxa_atexit(FUN_00dc958c,&DAT_02108628,&PTR_LOOP_01ecb1d0);
  DAT_02108640 = 0;
  DAT_02108648 = 0;
  DAT_02108650 = 0;
  __cxa_atexit(FUN_00dc958c,&DAT_02108640,&PTR_LOOP_01ecb1d0);
  DAT_02108658 = 0;
  DAT_02108660 = 0;
  DAT_02108668 = 0;
  __cxa_atexit(FUN_00dc958c,&DAT_02108658,&PTR_LOOP_01ecb1d0);
  DAT_021086a8 = 0;
  DAT_021086e8 = 0;
  DAT_021086f0 = 0;
  return;
}



// ==========================================================================================
// Function: _INIT_13
// Address: 00e0ab98
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _INIT_13(void)

{
  undefined *puVar1;
  
  puVar1 = PTR__basic_string_01ff5530;
  _DAT_02108700 = 0;
  DAT_02108708 = 0;
  DAT_02108710 = 0;
  __cxa_atexit(PTR__basic_string_01ff5530,&DAT_02108700,&PTR_LOOP_01ecb1d0);
  DAT_02108720 = 0;
  DAT_02108728 = 0;
  _DAT_02108718 = 0;
  __cxa_atexit(puVar1,&DAT_02108718,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_14
// Address: 00e0fc68
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _INIT_14(void)

{
  _DAT_02108730 = 0;
  DAT_02108738 = 0;
  DAT_02108740 = 0;
  __cxa_atexit(PTR__basic_string_01ff5530,&DAT_02108730,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_15
// Address: 00e1c1ac
// ==========================================================================================

void _INIT_15(void)

{
  DAT_02108758 = 0;
  DAT_02108760 = 0;
  DAT_02108768 = 0;
  __cxa_atexit(FUN_00da576c,&DAT_02108758,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_16
// Address: 00e28148
// ==========================================================================================

void _INIT_16(void)

{
  DAT_02108840 = 0;
  DAT_02108880 = 0;
  DAT_02108888 = 0;
  DAT_02108898 = 0;
  DAT_021088a0 = 0;
  DAT_02108890 = &DAT_02108898;
  __cxa_atexit(FUN_00daf9fc,&DAT_02108890,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_17
// Address: 00e2d168
// ==========================================================================================

void _INIT_17(void)

{
  undefined auStack_28 [8];
  undefined auStack_18 [8];
  
  DAT_021088b8 = 0;
  DAT_021088c0 = 0;
  DAT_021088b0 = &DAT_021088b8;
  __cxa_atexit(FUN_00e28368,&DAT_021088b0,&PTR_LOOP_01ecb1d0);
  DAT_021088c8 = 0;
  DAT_02108908 = 0;
  DAT_02108910 = 0;
  DAT_02108928 = 0;
  DAT_02108930 = 0;
  DAT_02108920 = &DAT_02108928;
  __cxa_atexit(FUN_00e29fe8,&DAT_02108920,&PTR_LOOP_01ecb1d0);
  DAT_02108958 = 0;
  DAT_02108960 = 0;
  DAT_02108950 = 0;
  __cxa_atexit(FUN_00e2acc0,&DAT_02108950,&PTR_LOOP_01ecb1d0);
  DAT_02108970 = 0;
  DAT_021089b0 = 0;
  DAT_021089b8 = 0;
  FUN_00e2b130(&DAT_021089c0,0,auStack_18,auStack_28);
  __cxa_atexit(FUN_00dfcd88,&DAT_021089c0,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_18
// Address: 00e2f280
// ==========================================================================================

void _INIT_18(void)

{
  DAT_02108a88 = 0;
  DAT_02108ac8 = 0;
  DAT_02108ad0 = 0;
  DAT_02108ae0 = 0;
  DAT_02108ae8 = 0;
  DAT_02108ad8 = 0;
  __cxa_atexit(FUN_00da576c,&DAT_02108ad8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_19
// Address: 00e2fc64
// ==========================================================================================

void _INIT_19(void)

{
  FUN_00dca69c(&DAT_02108af0,0,0);
  __cxa_atexit(PTR_FUN_01ff5570,&DAT_02108af0,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_20
// Address: 00e34f2c
// ==========================================================================================

void _INIT_20(void)

{
  undefined *puVar1;
  undefined auStack_40 [8];
  undefined auStack_38 [8];
  undefined auStack_30 [8];
  undefined auStack_28 [8];
  
  FUN_00e316c8(&DAT_02108b08,0,auStack_38,auStack_40);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108b08,&PTR_LOOP_01ecb1d0);
  DAT_02108b80 = 0;
  DAT_02108bc0 = 0;
  DAT_02108bc8 = 0;
  DAT_02108bd0 = 0;
  DAT_02108c10 = 0;
  DAT_02108c18 = 0;
  DAT_02108c20 = 0;
  DAT_02108c60 = 0;
  DAT_02108c68 = 0;
  FUN_00e32a98(&DAT_02108c70,0,auStack_28,auStack_30);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108c70,&PTR_LOOP_01ecb1d0);
  FUN_00dcb3c4(&DAT_02108cd8,0,0x7fff);
  __cxa_atexit(PTR_FUN_01ff5580,&DAT_02108cd8,&PTR_LOOP_01ecb1d0);
  FUN_00dca69c(&DAT_02108ce0,0,0);
  puVar1 = PTR_FUN_01ff5570;
  __cxa_atexit(PTR_FUN_01ff5570,&DAT_02108ce0,&PTR_LOOP_01ecb1d0);
  FUN_00dca69c(&DAT_02108ce8,1,0);
  __cxa_atexit(puVar1,&DAT_02108ce8,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_21
// Address: 00e37cd4
// ==========================================================================================

void _INIT_21(void)

{
  undefined auStack_20 [8];
  undefined auStack_18 [8];
  
  DAT_02108d10 = 0;
  DAT_02108d50 = 0;
  DAT_02108d58 = 0;
  FUN_00e361b8(&DAT_02108d60,0,auStack_18,auStack_20);
  __cxa_atexit(FUN_00dfcd88,&DAT_02108d60,&PTR_LOOP_01ecb1d0);
  return;
}



// ==========================================================================================
// Function: _INIT_22
// Address: 00e4d7d0
// ==========================================================================================

void _INIT_22(void)

{
  undefined auVar1 [16];
  
  DAT_0231cde0 = 0;
  auVar1 = FUN_00e4dbb0();
  DAT_0231c578 = auVar1._0_8_;
  DAT_0231c580 = auVar1._8_8_;
  DAT_0231c588 = (double)(unkuint9)auVar1._0_8_ / (double)(unkuint9)auVar1._8_8_;
  return;
}



// ==========================================================================================
// Function: _INIT_23
// Address: 00e4ded8
// ==========================================================================================

void _INIT_23(void)

{
  DAT_0231cde8 = 0;
  DAT_0231cdf0 = 0;
  FUN_00e4dbf0();
  return;
}



// ==========================================================================================
// Function: __call_callbacks
// Address: 00e4e264
// ==========================================================================================

/* std::__ndk1::ios_base::__call_callbacks(std::__ndk1::ios_base::event) */

void __thiscall std::__ndk1::ios_base::__call_callbacks(ios_base *this,event param_1)

{
  long lVar1;
  
  if (*(long *)(this + 0x48) != 0) {
    lVar1 = *(long *)(this + 0x48) + -1;
    do {
      (**(code **)(*(long *)(this + 0x38) + lVar1 * 8))
                (param_1,this,*(undefined4 *)(*(long *)(this + 0x40) + lVar1 * 4));
      lVar1 = lVar1 + -1;
    } while (lVar1 != -1);
  }
  return;
}



// ==========================================================================================
// Function: __set_badbit_and_consider_rethrow
// Address: 00e565d8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::ios_base::__set_badbit_and_consider_rethrow() */

long * std::__ndk1::ios_base::__set_badbit_and_consider_rethrow(void)

{
  ulong uVar1;
  uint uVar2;
  long lVar3;
  uint uVar4;
  long *in_x0;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  long lVar8;
  undefined8 uVar9;
  undefined auVar10 [16];
  sentry asStack_80 [8];
  long *plStack_78;
  locale alStack_70 [8];
  long lStack_68;
  undefined *puStack_60;
  code *pcStack_58;
  
  *(uint *)(in_x0 + 4) = *(uint *)(in_x0 + 4) | 1;
  if ((*(byte *)((long)in_x0 + 0x24) & 1) == 0) {
    return in_x0;
  }
  auVar10 = __cxa_rethrow();
  plVar5 = auVar10._0_8_;
  pcStack_58 = basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<;
  lVar3 = tpidr_el0;
  lStack_68 = *(long *)(lVar3 + 0x28);
  asStack_80[0] = (sentry)0x0;
  lVar8 = *plVar5;
  plStack_78 = plVar5;
  puStack_60 = &stack0xfffffffffffffff0;
  if (*(int *)((long)plVar5 + *(long *)(lVar8 + -0x18) + 0x20) == 0) {
    puStack_60 = &stack0xfffffffffffffff0;
    if (*(long *)((long)plVar5 + *(long *)(lVar8 + -0x18) + 0x88) != 0) {
      puStack_60 = &stack0xfffffffffffffff0;
      basic_ostream<char,std::__ndk1::char_traits<char>>::flush();
      lVar8 = *plVar5;
    }
    asStack_80[0] = (sentry)0x1;
    uVar2 = *(uint *)((long)plVar5 + *(long *)(lVar8 + -0x18) + 8);
    locale::locale(alStack_70,(locale *)((long)plVar5 + *(long *)(lVar8 + -0x18) + 0x30));
    plVar6 = (long *)locale::use_facet(alStack_70,(id *)PTR_id_01ff5638);
    locale::~locale(alStack_70);
    lVar8 = (long)plVar5 + *(long *)(*plVar5 + -0x18);
    uVar4 = *(uint *)(lVar8 + 0x90);
    uVar9 = *(undefined8 *)(lVar8 + 0x28);
    if (uVar4 == 0xffffffff) {
      locale::locale(alStack_70,(locale *)(lVar8 + 0x30));
      plVar7 = (long *)locale::use_facet(alStack_70,(id *)PTR_id_01ff5500);
      uVar4 = (**(code **)(*plVar7 + 0x38))(plVar7,0x20);
      locale::~locale(alStack_70);
      uVar4 = uVar4 & 0xff;
      *(uint *)(lVar8 + 0x90) = uVar4;
    }
    uVar2 = uVar2 & 0x4a;
    uVar1 = auVar10._8_8_ & 0xffff;
    if (uVar2 != 8 && uVar2 != 0x40) {
      uVar1 = (long)auVar10._8_2_;
    }
    lVar8 = (**(code **)(*plVar6 + 0x20))(plVar6,uVar9,lVar8,uVar4,uVar1);
    if (lVar8 == 0) {
      lVar8 = *(long *)(*plVar5 + -0x18);
      uVar4 = *(uint *)((long)plVar5 + lVar8 + 0x20) | 5;
      *(uint *)((long)plVar5 + lVar8 + 0x20) = uVar4;
      if ((*(uint *)((long)plVar5 + lVar8 + 0x24) & uVar4) != 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00e5b3f0("ios_base::clear");
      }
    }
  }
  basic_ostream<char,std::__ndk1::char_traits<char>>::sentry::~sentry(asStack_80);
  if (*(long *)(lVar3 + 0x28) == lStack_68) {
    return plVar5;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __set_failbit_and_consider_rethrow
// Address: 00e58044
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::ios_base::__set_failbit_and_consider_rethrow() */

long * std::__ndk1::ios_base::__set_failbit_and_consider_rethrow(void)

{
  uint uVar1;
  long lVar2;
  int iVar3;
  long *in_x0;
  long *plVar4;
  long *plVar5;
  long lVar6;
  undefined *puVar7;
  undefined auVar8 [12];
  sentry asStack_58 [8];
  long *plStack_50;
  long lStack_48;
  undefined *puStack_40;
  code *pcStack_38;
  
  *(uint *)(in_x0 + 4) = *(uint *)(in_x0 + 4) | 4;
  if ((*(byte *)((long)in_x0 + 0x24) >> 2 & 1) == 0) {
    return in_x0;
  }
  auVar8 = __cxa_rethrow();
  plVar4 = auVar8._0_8_;
  pcStack_38 = basic_ostream<char,std::__ndk1::char_traits<char>>::put;
  lVar2 = tpidr_el0;
  lStack_48 = *(long *)(lVar2 + 0x28);
  asStack_58[0] = (sentry)0x0;
  lVar6 = *plVar4;
  plStack_50 = plVar4;
  puStack_40 = &stack0xfffffffffffffff0;
  if (*(int *)((long)plVar4 + *(long *)(lVar6 + -0x18) + 0x20) != 0) goto LAB_00e58138;
  puStack_40 = &stack0xfffffffffffffff0;
  if (*(long *)((long)plVar4 + *(long *)(lVar6 + -0x18) + 0x88) != 0) {
    puStack_40 = &stack0xfffffffffffffff0;
    basic_ostream<char,std::__ndk1::char_traits<char>>::flush();
    lVar6 = *plVar4;
  }
  asStack_58[0] = (sentry)0x1;
  lVar6 = *(long *)(lVar6 + -0x18);
  plVar5 = *(long **)((long)plVar4 + lVar6 + 0x28);
  if (plVar5 != (long *)0x0) {
    puVar7 = (undefined *)plVar5[6];
    if (puVar7 != (undefined *)plVar5[7]) {
      plVar5[6] = (long)(puVar7 + 1);
      *puVar7 = auVar8[8];
      goto LAB_00e58138;
    }
    iVar3 = (**(code **)(*plVar5 + 0x68))(plVar5,auVar8._8_4_ & 0xff);
    if (iVar3 != -1) goto LAB_00e58138;
    lVar6 = *(long *)(*plVar4 + -0x18);
  }
  uVar1 = *(uint *)((long)plVar4 + lVar6 + 0x20) | 1;
  *(uint *)((long)plVar4 + lVar6 + 0x20) = uVar1;
  if ((*(uint *)((long)plVar4 + lVar6 + 0x24) & uVar1) != 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e5b3f0("ios_base::clear");
  }
LAB_00e58138:
  basic_ostream<char,std::__ndk1::char_traits<char>>::sentry::~sentry(asStack_58);
  if (*(long *)(lVar2 + 0x28) == lStack_48) {
    return plVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __do_get_signed<long>
// Address: 00e5c1c8
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_signed<long>(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   >, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >,
   std::__ndk1::ios_base&, unsigned int&, long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_signed<long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          long *param_5)

{
  uint uVar1;
  ulong uVar2;
  long lVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  long lVar7;
  istreambuf_iterator iVar8;
  long *plVar9;
  long *plVar11;
  char *pcVar12;
  ulong uVar13;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar10;
  
  plVar11 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar6 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar6 = 8;
  }
  else if (uVar1 == 8) {
    iVar6 = 0x10;
  }
  else {
    iVar6 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5c268 to 00e5c27b has its CatchHandler @ 00e5c528 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar12 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar12 = local_150;
  }
  local_174 = 0;
  plVar10 = (long *)(ulong)param_1;
  local_168 = pcVar12;
LAB_00e5c2b0:
  plVar9 = plVar10;
  if ((plVar10 == (long *)0x0) || (plVar10[3] != plVar10[4])) {
    if (plVar11 == (long *)0x0) goto LAB_00e5c30c;
LAB_00e5c2c4:
                    /* try { // try from 00e5c2d8 to 00e5c2ff has its CatchHandler @ 00e5c534 */
    if ((plVar11[3] == plVar11[4]) && (iVar5 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar5 == -1)
       ) goto LAB_00e5c30c;
    if (plVar9 != (long *)0x0) goto LAB_00e5c3f0;
  }
  else {
    iVar5 = (**(code **)(*plVar10 + 0x48))(plVar10);
    plVar9 = (long *)0x0;
    if (iVar5 != -1) {
      plVar9 = plVar10;
    }
    if (plVar11 != (long *)0x0) goto LAB_00e5c2c4;
LAB_00e5c30c:
    plVar11 = (long *)0x0;
    if (plVar9 == (long *)0x0) goto LAB_00e5c3f0;
  }
  uVar13 = local_158;
  if ((local_160 & 1) == 0) {
    uVar13 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar12 + uVar13) {
                    /* try { // try from 00e5c33c to 00e5c36b has its CatchHandler @ 00e5c530 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar13 << 1,'\0');
    uVar2 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar2 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar2,'\0');
    pcVar12 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar12 = local_150;
    }
    local_168 = pcVar12 + uVar13;
  }
  if ((char *)plVar9[3] == (char *)plVar9[4]) {
                    /* try { // try from 00e5c3a0 to 00e5c3eb has its CatchHandler @ 00e5c534 */
    cVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    cVar4 = *(char *)plVar9[3];
  }
  iVar5 = __num_get<char>::__stage2_int_loop
                    (cVar4,iVar6,pcVar12,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar5 != 0) goto LAB_00e5c3f0;
  plVar10 = plVar9;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 1;
  }
  goto LAB_00e5c2b0;
LAB_00e5c3f0:
  uVar13 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar13 = local_140;
  }
  if ((uVar13 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5c430 to 00e5c50f has its CatchHandler @ 00e5c52c */
  lVar7 = FUN_00e880fc(pcVar12,local_168,param_4,iVar6);
  *param_5 = lVar7;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar10 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar11 != (long *)0x0) goto LAB_00e5c470;
LAB_00e5c51c:
    iVar8 = (istreambuf_iterator)plVar10;
    if (plVar10 != (long *)0x0) goto LAB_00e5c4a4;
  }
  else {
    iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar10 = (long *)0x0;
    if (iVar6 != -1) {
      plVar10 = plVar9;
    }
    if (plVar11 == (long *)0x0) goto LAB_00e5c51c;
LAB_00e5c470:
    iVar8 = (istreambuf_iterator)plVar10;
    if ((plVar11[3] == plVar11[4]) && (iVar6 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar6 == -1)
       ) goto LAB_00e5c51c;
    if (plVar10 == (long *)0x0) goto LAB_00e5c4a4;
  }
  *param_4 = *param_4 | 2;
LAB_00e5c4a4:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar8;
}



// ==========================================================================================
// Function: __do_get_signed<long_long>
// Address: 00e5c578
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_signed<long long>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_signed<long_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          longlong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long lVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  longlong lVar7;
  istreambuf_iterator iVar8;
  long *plVar9;
  long *plVar11;
  char *pcVar12;
  ulong uVar13;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar10;
  
  plVar11 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar6 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar6 = 8;
  }
  else if (uVar1 == 8) {
    iVar6 = 0x10;
  }
  else {
    iVar6 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5c618 to 00e5c62b has its CatchHandler @ 00e5c8d8 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar12 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar12 = local_150;
  }
  local_174 = 0;
  plVar10 = (long *)(ulong)param_1;
  local_168 = pcVar12;
LAB_00e5c660:
  plVar9 = plVar10;
  if ((plVar10 == (long *)0x0) || (plVar10[3] != plVar10[4])) {
    if (plVar11 == (long *)0x0) goto LAB_00e5c6bc;
LAB_00e5c674:
                    /* try { // try from 00e5c688 to 00e5c6af has its CatchHandler @ 00e5c8e4 */
    if ((plVar11[3] == plVar11[4]) && (iVar5 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar5 == -1)
       ) goto LAB_00e5c6bc;
    if (plVar9 != (long *)0x0) goto LAB_00e5c7a0;
  }
  else {
    iVar5 = (**(code **)(*plVar10 + 0x48))(plVar10);
    plVar9 = (long *)0x0;
    if (iVar5 != -1) {
      plVar9 = plVar10;
    }
    if (plVar11 != (long *)0x0) goto LAB_00e5c674;
LAB_00e5c6bc:
    plVar11 = (long *)0x0;
    if (plVar9 == (long *)0x0) goto LAB_00e5c7a0;
  }
  uVar13 = local_158;
  if ((local_160 & 1) == 0) {
    uVar13 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar12 + uVar13) {
                    /* try { // try from 00e5c6ec to 00e5c71b has its CatchHandler @ 00e5c8e0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar13 << 1,'\0');
    uVar2 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar2 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar2,'\0');
    pcVar12 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar12 = local_150;
    }
    local_168 = pcVar12 + uVar13;
  }
  if ((char *)plVar9[3] == (char *)plVar9[4]) {
                    /* try { // try from 00e5c750 to 00e5c79b has its CatchHandler @ 00e5c8e4 */
    cVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    cVar4 = *(char *)plVar9[3];
  }
  iVar5 = __num_get<char>::__stage2_int_loop
                    (cVar4,iVar6,pcVar12,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar5 != 0) goto LAB_00e5c7a0;
  plVar10 = plVar9;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 1;
  }
  goto LAB_00e5c660;
LAB_00e5c7a0:
  uVar13 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar13 = local_140;
  }
  if ((uVar13 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5c7e0 to 00e5c8bf has its CatchHandler @ 00e5c8dc */
  lVar7 = FUN_00e8824c(pcVar12,local_168,param_4,iVar6);
  *param_5 = lVar7;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar10 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar11 != (long *)0x0) goto LAB_00e5c820;
LAB_00e5c8cc:
    iVar8 = (istreambuf_iterator)plVar10;
    if (plVar10 != (long *)0x0) goto LAB_00e5c854;
  }
  else {
    iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar10 = (long *)0x0;
    if (iVar6 != -1) {
      plVar10 = plVar9;
    }
    if (plVar11 == (long *)0x0) goto LAB_00e5c8cc;
LAB_00e5c820:
    iVar8 = (istreambuf_iterator)plVar10;
    if ((plVar11[3] == plVar11[4]) && (iVar6 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar6 == -1)
       ) goto LAB_00e5c8cc;
    if (plVar10 == (long *)0x0) goto LAB_00e5c854;
  }
  *param_4 = *param_4 | 2;
LAB_00e5c854:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar8;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_short>
// Address: 00e5c928
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_unsigned<unsigned short>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, unsigned short&) const
    */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_short>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ushort *param_5)

{
  uint uVar1;
  ulong uVar2;
  long lVar3;
  char cVar4;
  ushort uVar5;
  int iVar6;
  int iVar7;
  istreambuf_iterator iVar8;
  long *plVar9;
  long *plVar11;
  char *pcVar12;
  ulong uVar13;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar10;
  
  plVar11 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar7 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar7 = 8;
  }
  else if (uVar1 == 8) {
    iVar7 = 0x10;
  }
  else {
    iVar7 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5c9c8 to 00e5c9db has its CatchHandler @ 00e5cc88 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar12 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar12 = local_150;
  }
  local_174 = 0;
  plVar10 = (long *)(ulong)param_1;
  local_168 = pcVar12;
LAB_00e5ca10:
  plVar9 = plVar10;
  if ((plVar10 == (long *)0x0) || (plVar10[3] != plVar10[4])) {
    if (plVar11 == (long *)0x0) goto LAB_00e5ca6c;
LAB_00e5ca24:
                    /* try { // try from 00e5ca38 to 00e5ca5f has its CatchHandler @ 00e5cc94 */
    if ((plVar11[3] == plVar11[4]) && (iVar6 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar6 == -1)
       ) goto LAB_00e5ca6c;
    if (plVar9 != (long *)0x0) goto LAB_00e5cb50;
  }
  else {
    iVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
    plVar9 = (long *)0x0;
    if (iVar6 != -1) {
      plVar9 = plVar10;
    }
    if (plVar11 != (long *)0x0) goto LAB_00e5ca24;
LAB_00e5ca6c:
    plVar11 = (long *)0x0;
    if (plVar9 == (long *)0x0) goto LAB_00e5cb50;
  }
  uVar13 = local_158;
  if ((local_160 & 1) == 0) {
    uVar13 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar12 + uVar13) {
                    /* try { // try from 00e5ca9c to 00e5cacb has its CatchHandler @ 00e5cc90 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar13 << 1,'\0');
    uVar2 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar2 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar2,'\0');
    pcVar12 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar12 = local_150;
    }
    local_168 = pcVar12 + uVar13;
  }
  if ((char *)plVar9[3] == (char *)plVar9[4]) {
                    /* try { // try from 00e5cb00 to 00e5cb4b has its CatchHandler @ 00e5cc94 */
    cVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    cVar4 = *(char *)plVar9[3];
  }
  iVar6 = __num_get<char>::__stage2_int_loop
                    (cVar4,iVar7,pcVar12,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar6 != 0) goto LAB_00e5cb50;
  plVar10 = plVar9;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 1;
  }
  goto LAB_00e5ca10;
LAB_00e5cb50:
  uVar13 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar13 = local_140;
  }
  if ((uVar13 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5cb90 to 00e5cc6f has its CatchHandler @ 00e5cc8c */
  uVar5 = FUN_00e8839c(pcVar12,local_168,param_4,iVar7);
  *param_5 = uVar5;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar10 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar11 != (long *)0x0) goto LAB_00e5cbd0;
LAB_00e5cc7c:
    iVar8 = (istreambuf_iterator)plVar10;
    if (plVar10 != (long *)0x0) goto LAB_00e5cc04;
  }
  else {
    iVar7 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar10 = (long *)0x0;
    if (iVar7 != -1) {
      plVar10 = plVar9;
    }
    if (plVar11 == (long *)0x0) goto LAB_00e5cc7c;
LAB_00e5cbd0:
    iVar8 = (istreambuf_iterator)plVar10;
    if ((plVar11[3] == plVar11[4]) && (iVar7 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar7 == -1)
       ) goto LAB_00e5cc7c;
    if (plVar10 == (long *)0x0) goto LAB_00e5cc04;
  }
  *param_4 = *param_4 | 2;
LAB_00e5cc04:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar8;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_int>
// Address: 00e5ccd8
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_unsigned<unsigned int>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, unsigned int&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_int>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          uint *param_5)

{
  ulong uVar1;
  long lVar2;
  char cVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  istreambuf_iterator iVar7;
  long *plVar8;
  long *plVar10;
  char *pcVar11;
  ulong uVar12;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar9;
  
  plVar10 = (long *)(ulong)param_2;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  uVar5 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar5 == 0) {
    iVar6 = 0;
  }
  else if (uVar5 == 0x40) {
    iVar6 = 8;
  }
  else if (uVar5 == 8) {
    iVar6 = 0x10;
  }
  else {
    iVar6 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5cd78 to 00e5cd8b has its CatchHandler @ 00e5d038 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar11 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar11 = local_150;
  }
  local_174 = 0;
  plVar9 = (long *)(ulong)param_1;
  local_168 = pcVar11;
LAB_00e5cdc0:
  plVar8 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar10 == (long *)0x0) goto LAB_00e5ce1c;
LAB_00e5cdd4:
                    /* try { // try from 00e5cde8 to 00e5ce0f has its CatchHandler @ 00e5d044 */
    if ((plVar10[3] == plVar10[4]) && (iVar4 = (**(code **)(*plVar10 + 0x48))(plVar10), iVar4 == -1)
       ) goto LAB_00e5ce1c;
    if (plVar8 != (long *)0x0) goto LAB_00e5cf00;
  }
  else {
    iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar8 = (long *)0x0;
    if (iVar4 != -1) {
      plVar8 = plVar9;
    }
    if (plVar10 != (long *)0x0) goto LAB_00e5cdd4;
LAB_00e5ce1c:
    plVar10 = (long *)0x0;
    if (plVar8 == (long *)0x0) goto LAB_00e5cf00;
  }
  uVar12 = local_158;
  if ((local_160 & 1) == 0) {
    uVar12 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar11 + uVar12) {
                    /* try { // try from 00e5ce4c to 00e5ce7b has its CatchHandler @ 00e5d040 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar12 << 1,'\0');
    uVar1 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar1 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar1,'\0');
    pcVar11 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar11 = local_150;
    }
    local_168 = pcVar11 + uVar12;
  }
  if ((char *)plVar8[3] == (char *)plVar8[4]) {
                    /* try { // try from 00e5ceb0 to 00e5cefb has its CatchHandler @ 00e5d044 */
    cVar3 = (**(code **)(*plVar8 + 0x48))(plVar8);
  }
  else {
    cVar3 = *(char *)plVar8[3];
  }
  iVar4 = __num_get<char>::__stage2_int_loop
                    (cVar3,iVar6,pcVar11,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar4 != 0) goto LAB_00e5cf00;
  plVar9 = plVar8;
  if (plVar8[3] == plVar8[4]) {
    (**(code **)(*plVar8 + 0x50))(plVar8);
  }
  else {
    plVar8[3] = plVar8[3] + 1;
  }
  goto LAB_00e5cdc0;
LAB_00e5cf00:
  uVar12 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar12 = local_140;
  }
  if ((uVar12 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5cf40 to 00e5d01f has its CatchHandler @ 00e5d03c */
  uVar5 = FUN_00e88520(pcVar11,local_168,param_4,iVar6);
  *param_5 = uVar5;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar9 = plVar8;
  if ((plVar8 == (long *)0x0) || (plVar8[3] != plVar8[4])) {
    if (plVar10 != (long *)0x0) goto LAB_00e5cf80;
LAB_00e5d02c:
    iVar7 = (istreambuf_iterator)plVar9;
    if (plVar9 != (long *)0x0) goto LAB_00e5cfb4;
  }
  else {
    iVar6 = (**(code **)(*plVar8 + 0x48))(plVar8);
    plVar9 = (long *)0x0;
    if (iVar6 != -1) {
      plVar9 = plVar8;
    }
    if (plVar10 == (long *)0x0) goto LAB_00e5d02c;
LAB_00e5cf80:
    iVar7 = (istreambuf_iterator)plVar9;
    if ((plVar10[3] == plVar10[4]) && (iVar6 = (**(code **)(*plVar10 + 0x48))(plVar10), iVar6 == -1)
       ) goto LAB_00e5d02c;
    if (plVar9 == (long *)0x0) goto LAB_00e5cfb4;
  }
  *param_4 = *param_4 | 2;
LAB_00e5cfb4:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar7;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long>
// Address: 00e5d088
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_unsigned<unsigned long>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, unsigned long&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ulong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long lVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  ulong uVar7;
  istreambuf_iterator iVar8;
  long *plVar9;
  long *plVar11;
  char *pcVar12;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar10;
  
  plVar11 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar6 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar6 = 8;
  }
  else if (uVar1 == 8) {
    iVar6 = 0x10;
  }
  else {
    iVar6 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5d128 to 00e5d13b has its CatchHandler @ 00e5d3e8 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar12 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar12 = local_150;
  }
  local_174 = 0;
  plVar10 = (long *)(ulong)param_1;
  local_168 = pcVar12;
LAB_00e5d170:
  plVar9 = plVar10;
  if ((plVar10 == (long *)0x0) || (plVar10[3] != plVar10[4])) {
    if (plVar11 == (long *)0x0) goto LAB_00e5d1cc;
LAB_00e5d184:
                    /* try { // try from 00e5d198 to 00e5d1bf has its CatchHandler @ 00e5d3f4 */
    if ((plVar11[3] == plVar11[4]) && (iVar5 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar5 == -1)
       ) goto LAB_00e5d1cc;
    if (plVar9 != (long *)0x0) goto LAB_00e5d2b0;
  }
  else {
    iVar5 = (**(code **)(*plVar10 + 0x48))(plVar10);
    plVar9 = (long *)0x0;
    if (iVar5 != -1) {
      plVar9 = plVar10;
    }
    if (plVar11 != (long *)0x0) goto LAB_00e5d184;
LAB_00e5d1cc:
    plVar11 = (long *)0x0;
    if (plVar9 == (long *)0x0) goto LAB_00e5d2b0;
  }
  uVar7 = local_158;
  if ((local_160 & 1) == 0) {
    uVar7 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar12 + uVar7) {
                    /* try { // try from 00e5d1fc to 00e5d22b has its CatchHandler @ 00e5d3f0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar7 << 1,'\0');
    uVar2 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar2 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar2,'\0');
    pcVar12 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar12 = local_150;
    }
    local_168 = pcVar12 + uVar7;
  }
  if ((char *)plVar9[3] == (char *)plVar9[4]) {
                    /* try { // try from 00e5d260 to 00e5d2ab has its CatchHandler @ 00e5d3f4 */
    cVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    cVar4 = *(char *)plVar9[3];
  }
  iVar5 = __num_get<char>::__stage2_int_loop
                    (cVar4,iVar6,pcVar12,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar5 != 0) goto LAB_00e5d2b0;
  plVar10 = plVar9;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 1;
  }
  goto LAB_00e5d170;
LAB_00e5d2b0:
  uVar7 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar7 = local_140;
  }
  if ((uVar7 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5d2f0 to 00e5d3cf has its CatchHandler @ 00e5d3ec */
  uVar7 = FUN_00e886a4(pcVar12,local_168,param_4,iVar6);
  *param_5 = uVar7;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar10 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar11 != (long *)0x0) goto LAB_00e5d330;
LAB_00e5d3dc:
    iVar8 = (istreambuf_iterator)plVar10;
    if (plVar10 != (long *)0x0) goto LAB_00e5d364;
  }
  else {
    iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar10 = (long *)0x0;
    if (iVar6 != -1) {
      plVar10 = plVar9;
    }
    if (plVar11 == (long *)0x0) goto LAB_00e5d3dc;
LAB_00e5d330:
    iVar8 = (istreambuf_iterator)plVar10;
    if ((plVar11[3] == plVar11[4]) && (iVar6 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar6 == -1)
       ) goto LAB_00e5d3dc;
    if (plVar10 == (long *)0x0) goto LAB_00e5d364;
  }
  *param_4 = *param_4 | 2;
LAB_00e5d364:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar8;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long_long>
// Address: 00e5d438
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_unsigned<unsigned long long>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, unsigned long long&)
   const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_long_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ulonglong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long lVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  ulonglong uVar7;
  istreambuf_iterator iVar8;
  long *plVar9;
  long *plVar11;
  char *pcVar12;
  ulong uVar13;
  uint local_174;
  uint *local_170;
  char *local_168;
  ulong local_160;
  ulong local_158;
  char *local_150;
  basic_string local_148 [8];
  ulong local_140;
  void *local_138;
  char local_130 [4];
  uint local_12c [40];
  ios_base aiStack_8c [28];
  long local_70;
  long *plVar10;
  
  plVar11 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar6 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar6 = 8;
  }
  else if (uVar1 == 8) {
    iVar6 = 0x10;
  }
  else {
    iVar6 = 10;
  }
  __num_get<char>::__stage2_int_prep
            ((__num_get<char> *)param_3,aiStack_8c,local_130,(char *)param_3);
  local_160 = 0;
  local_158 = 0;
  local_150 = (char *)0x0;
                    /* try { // try from 00e5d4d8 to 00e5d4eb has its CatchHandler @ 00e5d798 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_160,0x16,'\0');
  local_170 = local_12c;
  pcVar12 = (char *)((ulong)&local_160 | 1);
  if ((local_160 & 1) != 0) {
    pcVar12 = local_150;
  }
  local_174 = 0;
  plVar10 = (long *)(ulong)param_1;
  local_168 = pcVar12;
LAB_00e5d520:
  plVar9 = plVar10;
  if ((plVar10 == (long *)0x0) || (plVar10[3] != plVar10[4])) {
    if (plVar11 == (long *)0x0) goto LAB_00e5d57c;
LAB_00e5d534:
                    /* try { // try from 00e5d548 to 00e5d56f has its CatchHandler @ 00e5d7a4 */
    if ((plVar11[3] == plVar11[4]) && (iVar5 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar5 == -1)
       ) goto LAB_00e5d57c;
    if (plVar9 != (long *)0x0) goto LAB_00e5d660;
  }
  else {
    iVar5 = (**(code **)(*plVar10 + 0x48))(plVar10);
    plVar9 = (long *)0x0;
    if (iVar5 != -1) {
      plVar9 = plVar10;
    }
    if (plVar11 != (long *)0x0) goto LAB_00e5d534;
LAB_00e5d57c:
    plVar11 = (long *)0x0;
    if (plVar9 == (long *)0x0) goto LAB_00e5d660;
  }
  uVar13 = local_158;
  if ((local_160 & 1) == 0) {
    uVar13 = local_160 >> 1 & 0x7f;
  }
  if (local_168 == pcVar12 + uVar13) {
                    /* try { // try from 00e5d5ac to 00e5d5db has its CatchHandler @ 00e5d7a0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar13 << 1,'\0');
    uVar2 = 0x16;
    if ((local_160 & 1) != 0) {
      uVar2 = (local_160 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_160,uVar2,'\0');
    pcVar12 = (char *)((ulong)&local_160 | 1);
    if ((local_160 & 1) != 0) {
      pcVar12 = local_150;
    }
    local_168 = pcVar12 + uVar13;
  }
  if ((char *)plVar9[3] == (char *)plVar9[4]) {
                    /* try { // try from 00e5d610 to 00e5d65b has its CatchHandler @ 00e5d7a4 */
    cVar4 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    cVar4 = *(char *)plVar9[3];
  }
  iVar5 = __num_get<char>::__stage2_int_loop
                    (cVar4,iVar6,pcVar12,&local_168,&local_174,local_130[0],local_148,local_12c,
                     &local_170,(char *)aiStack_8c);
  if (iVar5 != 0) goto LAB_00e5d660;
  plVar10 = plVar9;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 1;
  }
  goto LAB_00e5d520;
LAB_00e5d660:
  uVar13 = (ulong)((byte)local_148[0] >> 1);
  if (((byte)local_148[0] & 1) != 0) {
    uVar13 = local_140;
  }
  if ((uVar13 != 0) && ((long)local_170 - (long)local_12c < 0xa0)) {
    *local_170 = local_174;
    local_170 = local_170 + 1;
  }
                    /* try { // try from 00e5d6a0 to 00e5d77f has its CatchHandler @ 00e5d79c */
  uVar7 = FUN_00e88818(pcVar12,local_168,param_4,iVar6);
  *param_5 = uVar7;
  __check_grouping(local_148,local_12c,local_170,param_4);
  plVar10 = plVar9;
  if ((plVar9 == (long *)0x0) || (plVar9[3] != plVar9[4])) {
    if (plVar11 != (long *)0x0) goto LAB_00e5d6e0;
LAB_00e5d78c:
    iVar8 = (istreambuf_iterator)plVar10;
    if (plVar10 != (long *)0x0) goto LAB_00e5d714;
  }
  else {
    iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    plVar10 = (long *)0x0;
    if (iVar6 != -1) {
      plVar10 = plVar9;
    }
    if (plVar11 == (long *)0x0) goto LAB_00e5d78c;
LAB_00e5d6e0:
    iVar8 = (istreambuf_iterator)plVar10;
    if ((plVar11[3] == plVar11[4]) && (iVar6 = (**(code **)(*plVar11 + 0x48))(plVar11), iVar6 == -1)
       ) goto LAB_00e5d78c;
    if (plVar10 == (long *)0x0) goto LAB_00e5d714;
  }
  *param_4 = *param_4 | 2;
LAB_00e5d714:
  if ((local_160 & 1) != 0) {
    operator_delete(local_150);
  }
  if (((byte)local_148[0] & 1) != 0) {
    operator_delete(local_138);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar8;
}



// ==========================================================================================
// Function: __do_get_floating_point<float>
// Address: 00e5d7e8
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_floating_point<float>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, float&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<float>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          float *param_5)

{
  ulong uVar1;
  long lVar2;
  char cVar3;
  int iVar4;
  istreambuf_iterator iVar5;
  long *plVar6;
  ulong uVar8;
  long *plVar9;
  char *pcVar10;
  float fVar11;
  char local_184 [4];
  bool local_180 [4];
  uint local_17c;
  uint *local_178;
  char *local_170;
  ulong local_168;
  ulong local_160;
  char *local_158;
  basic_string local_150 [8];
  ulong local_148;
  void *local_140;
  char local_138 [4];
  char local_134 [4];
  uint local_130 [40];
  ios_base aiStack_90 [32];
  long local_70;
  long *plVar7;
  
  plVar9 = (long *)(ulong)param_2;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  __num_get<char>::__stage2_float_prep
            ((__num_get<char> *)param_3,aiStack_90,local_134,local_138,(char *)param_4);
  local_168 = 0;
  local_160 = 0;
  local_158 = (char *)0x0;
                    /* try { // try from 00e5d84c to 00e5d85f has its CatchHandler @ 00e5db2c */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_168,0x16,'\0');
  pcVar10 = (char *)((ulong)&local_168 | 1);
  if ((local_168 & 1) != 0) {
    pcVar10 = local_158;
  }
  local_17c = 0;
  local_180[0] = true;
  local_184[0] = 'E';
  plVar7 = (long *)(ulong)param_1;
  local_178 = local_130;
  local_170 = pcVar10;
LAB_00e5d8a8:
  plVar6 = plVar7;
  if ((plVar7 == (long *)0x0) || (plVar7[3] != plVar7[4])) {
    if (plVar9 == (long *)0x0) goto LAB_00e5d904;
LAB_00e5d8bc:
                    /* try { // try from 00e5d8d0 to 00e5d8f7 has its CatchHandler @ 00e5db38 */
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5d904;
    if (plVar6 != (long *)0x0) goto LAB_00e5d9ec;
  }
  else {
    iVar4 = (**(code **)(*plVar7 + 0x48))(plVar7);
    plVar6 = (long *)0x0;
    if (iVar4 != -1) {
      plVar6 = plVar7;
    }
    if (plVar9 != (long *)0x0) goto LAB_00e5d8bc;
LAB_00e5d904:
    plVar9 = (long *)0x0;
    if (plVar6 == (long *)0x0) goto LAB_00e5d9ec;
  }
  uVar8 = local_160;
  if ((local_168 & 1) == 0) {
    uVar8 = local_168 >> 1 & 0x7f;
  }
  if (local_170 == pcVar10 + uVar8) {
                    /* try { // try from 00e5d934 to 00e5d963 has its CatchHandler @ 00e5db34 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_168 & 1) != 0) {
      uVar1 = (local_168 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar1,'\0');
    pcVar10 = (char *)((ulong)&local_168 | 1);
    if ((local_168 & 1) != 0) {
      pcVar10 = local_158;
    }
    local_170 = pcVar10 + uVar8;
  }
  if ((char *)plVar6[3] == (char *)plVar6[4]) {
                    /* try { // try from 00e5d998 to 00e5d9e7 has its CatchHandler @ 00e5db38 */
    cVar3 = (**(code **)(*plVar6 + 0x48))(plVar6);
  }
  else {
    cVar3 = *(char *)plVar6[3];
  }
  iVar4 = __num_get<char>::__stage2_float_loop
                    (cVar3,local_180,local_184,pcVar10,&local_170,local_134[0],local_138[0],
                     local_150,local_130,&local_178,&local_17c,(char *)aiStack_90);
  if (iVar4 != 0) goto LAB_00e5d9ec;
  plVar7 = plVar6;
  if (plVar6[3] == plVar6[4]) {
    (**(code **)(*plVar6 + 0x50))(plVar6);
  }
  else {
    plVar6[3] = plVar6[3] + 1;
  }
  goto LAB_00e5d8a8;
LAB_00e5d9ec:
  uVar8 = (ulong)((byte)local_150[0] >> 1);
  if (((byte)local_150[0] & 1) != 0) {
    uVar8 = local_148;
  }
  if (((local_180[0] != false) && (uVar8 != 0)) && ((long)local_178 - (long)local_130 < 0xa0)) {
    *local_178 = local_17c;
    local_178 = local_178 + 1;
  }
                    /* try { // try from 00e5da38 to 00e5db13 has its CatchHandler @ 00e5db30 */
  fVar11 = (float)FUN_00e8898c(pcVar10,local_170,param_4);
  *param_5 = fVar11;
  __check_grouping(local_150,local_130,local_178,param_4);
  plVar7 = plVar6;
  if ((plVar6 == (long *)0x0) || (plVar6[3] != plVar6[4])) {
    if (plVar9 != (long *)0x0) goto LAB_00e5da74;
LAB_00e5db20:
    iVar5 = (istreambuf_iterator)plVar7;
    if (plVar7 != (long *)0x0) goto LAB_00e5daa8;
  }
  else {
    iVar4 = (**(code **)(*plVar6 + 0x48))(plVar6);
    plVar7 = (long *)0x0;
    if (iVar4 != -1) {
      plVar7 = plVar6;
    }
    if (plVar9 == (long *)0x0) goto LAB_00e5db20;
LAB_00e5da74:
    iVar5 = (istreambuf_iterator)plVar7;
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5db20;
    if (plVar7 == (long *)0x0) goto LAB_00e5daa8;
  }
  *param_4 = *param_4 | 2;
LAB_00e5daa8:
  if ((local_168 & 1) != 0) {
    operator_delete(local_158);
  }
  if (((byte)local_150[0] & 1) != 0) {
    operator_delete(local_140);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar5;
}



// ==========================================================================================
// Function: __do_get_floating_point<double>
// Address: 00e5db7c
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_floating_point<double>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, double&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<double>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          double *param_5)

{
  ulong uVar1;
  long lVar2;
  char cVar3;
  int iVar4;
  istreambuf_iterator iVar5;
  long *plVar6;
  ulong uVar8;
  long *plVar9;
  char *pcVar10;
  double dVar11;
  char local_184 [4];
  bool local_180 [4];
  uint local_17c;
  uint *local_178;
  char *local_170;
  ulong local_168;
  ulong local_160;
  char *local_158;
  basic_string local_150 [8];
  ulong local_148;
  void *local_140;
  char local_138 [4];
  char local_134 [4];
  uint local_130 [40];
  ios_base aiStack_90 [32];
  long local_70;
  long *plVar7;
  
  plVar9 = (long *)(ulong)param_2;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  __num_get<char>::__stage2_float_prep
            ((__num_get<char> *)param_3,aiStack_90,local_134,local_138,(char *)param_4);
  local_168 = 0;
  local_160 = 0;
  local_158 = (char *)0x0;
                    /* try { // try from 00e5dbe0 to 00e5dbf3 has its CatchHandler @ 00e5dec0 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_168,0x16,'\0');
  pcVar10 = (char *)((ulong)&local_168 | 1);
  if ((local_168 & 1) != 0) {
    pcVar10 = local_158;
  }
  local_17c = 0;
  local_180[0] = true;
  local_184[0] = 'E';
  plVar7 = (long *)(ulong)param_1;
  local_178 = local_130;
  local_170 = pcVar10;
LAB_00e5dc3c:
  plVar6 = plVar7;
  if ((plVar7 == (long *)0x0) || (plVar7[3] != plVar7[4])) {
    if (plVar9 == (long *)0x0) goto LAB_00e5dc98;
LAB_00e5dc50:
                    /* try { // try from 00e5dc64 to 00e5dc8b has its CatchHandler @ 00e5decc */
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5dc98;
    if (plVar6 != (long *)0x0) goto LAB_00e5dd80;
  }
  else {
    iVar4 = (**(code **)(*plVar7 + 0x48))(plVar7);
    plVar6 = (long *)0x0;
    if (iVar4 != -1) {
      plVar6 = plVar7;
    }
    if (plVar9 != (long *)0x0) goto LAB_00e5dc50;
LAB_00e5dc98:
    plVar9 = (long *)0x0;
    if (plVar6 == (long *)0x0) goto LAB_00e5dd80;
  }
  uVar8 = local_160;
  if ((local_168 & 1) == 0) {
    uVar8 = local_168 >> 1 & 0x7f;
  }
  if (local_170 == pcVar10 + uVar8) {
                    /* try { // try from 00e5dcc8 to 00e5dcf7 has its CatchHandler @ 00e5dec8 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_168 & 1) != 0) {
      uVar1 = (local_168 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar1,'\0');
    pcVar10 = (char *)((ulong)&local_168 | 1);
    if ((local_168 & 1) != 0) {
      pcVar10 = local_158;
    }
    local_170 = pcVar10 + uVar8;
  }
  if ((char *)plVar6[3] == (char *)plVar6[4]) {
                    /* try { // try from 00e5dd2c to 00e5dd7b has its CatchHandler @ 00e5decc */
    cVar3 = (**(code **)(*plVar6 + 0x48))(plVar6);
  }
  else {
    cVar3 = *(char *)plVar6[3];
  }
  iVar4 = __num_get<char>::__stage2_float_loop
                    (cVar3,local_180,local_184,pcVar10,&local_170,local_134[0],local_138[0],
                     local_150,local_130,&local_178,&local_17c,(char *)aiStack_90);
  if (iVar4 != 0) goto LAB_00e5dd80;
  plVar7 = plVar6;
  if (plVar6[3] == plVar6[4]) {
    (**(code **)(*plVar6 + 0x50))(plVar6);
  }
  else {
    plVar6[3] = plVar6[3] + 1;
  }
  goto LAB_00e5dc3c;
LAB_00e5dd80:
  uVar8 = (ulong)((byte)local_150[0] >> 1);
  if (((byte)local_150[0] & 1) != 0) {
    uVar8 = local_148;
  }
  if (((local_180[0] != false) && (uVar8 != 0)) && ((long)local_178 - (long)local_130 < 0xa0)) {
    *local_178 = local_17c;
    local_178 = local_178 + 1;
  }
                    /* try { // try from 00e5ddcc to 00e5dea7 has its CatchHandler @ 00e5dec4 */
  dVar11 = (double)FUN_00e88ab8(pcVar10,local_170,param_4);
  *param_5 = dVar11;
  __check_grouping(local_150,local_130,local_178,param_4);
  plVar7 = plVar6;
  if ((plVar6 == (long *)0x0) || (plVar6[3] != plVar6[4])) {
    if (plVar9 != (long *)0x0) goto LAB_00e5de08;
LAB_00e5deb4:
    iVar5 = (istreambuf_iterator)plVar7;
    if (plVar7 != (long *)0x0) goto LAB_00e5de3c;
  }
  else {
    iVar4 = (**(code **)(*plVar6 + 0x48))(plVar6);
    plVar7 = (long *)0x0;
    if (iVar4 != -1) {
      plVar7 = plVar6;
    }
    if (plVar9 == (long *)0x0) goto LAB_00e5deb4;
LAB_00e5de08:
    iVar5 = (istreambuf_iterator)plVar7;
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5deb4;
    if (plVar7 == (long *)0x0) goto LAB_00e5de3c;
  }
  *param_4 = *param_4 | 2;
LAB_00e5de3c:
  if ((local_168 & 1) != 0) {
    operator_delete(local_158);
  }
  if (((byte)local_150[0] & 1) != 0) {
    operator_delete(local_140);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar5;
}



// ==========================================================================================
// Function: __do_get_floating_point<long_double>
// Address: 00e5df10
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >
   std::__ndk1::num_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__do_get_floating_point<long double>(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, std::__ndk1::ios_base&, unsigned int&, long double&) const */

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<long_double>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          longdouble *param_5)

{
  ulong uVar1;
  long lVar2;
  char cVar3;
  int iVar4;
  istreambuf_iterator iVar5;
  long *plVar6;
  ulong uVar8;
  long *plVar9;
  char *pcVar10;
  undefined auVar11 [16];
  char local_184 [4];
  bool local_180 [4];
  uint local_17c;
  uint *local_178;
  char *local_170;
  ulong local_168;
  ulong local_160;
  char *local_158;
  basic_string local_150 [8];
  ulong local_148;
  void *local_140;
  char local_138 [4];
  char local_134 [4];
  uint local_130 [40];
  ios_base aiStack_90 [32];
  long local_70;
  long *plVar7;
  
  plVar9 = (long *)(ulong)param_2;
  lVar2 = tpidr_el0;
  local_70 = *(long *)(lVar2 + 0x28);
  __num_get<char>::__stage2_float_prep
            ((__num_get<char> *)param_3,aiStack_90,local_134,local_138,(char *)param_4);
  local_168 = 0;
  local_160 = 0;
  local_158 = (char *)0x0;
                    /* try { // try from 00e5df74 to 00e5df87 has its CatchHandler @ 00e5e254 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_168,0x16,'\0');
  pcVar10 = (char *)((ulong)&local_168 | 1);
  if ((local_168 & 1) != 0) {
    pcVar10 = local_158;
  }
  local_17c = 0;
  local_180[0] = true;
  local_184[0] = 'E';
  plVar7 = (long *)(ulong)param_1;
  local_178 = local_130;
  local_170 = pcVar10;
LAB_00e5dfd0:
  plVar6 = plVar7;
  if ((plVar7 == (long *)0x0) || (plVar7[3] != plVar7[4])) {
    if (plVar9 == (long *)0x0) goto LAB_00e5e02c;
LAB_00e5dfe4:
                    /* try { // try from 00e5dff8 to 00e5e01f has its CatchHandler @ 00e5e260 */
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5e02c;
    if (plVar6 != (long *)0x0) goto LAB_00e5e114;
  }
  else {
    iVar4 = (**(code **)(*plVar7 + 0x48))(plVar7);
    plVar6 = (long *)0x0;
    if (iVar4 != -1) {
      plVar6 = plVar7;
    }
    if (plVar9 != (long *)0x0) goto LAB_00e5dfe4;
LAB_00e5e02c:
    plVar9 = (long *)0x0;
    if (plVar6 == (long *)0x0) goto LAB_00e5e114;
  }
  uVar8 = local_160;
  if ((local_168 & 1) == 0) {
    uVar8 = local_168 >> 1 & 0x7f;
  }
  if (local_170 == pcVar10 + uVar8) {
                    /* try { // try from 00e5e05c to 00e5e08b has its CatchHandler @ 00e5e25c */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_168 & 1) != 0) {
      uVar1 = (local_168 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_168,uVar1,'\0');
    pcVar10 = (char *)((ulong)&local_168 | 1);
    if ((local_168 & 1) != 0) {
      pcVar10 = local_158;
    }
    local_170 = pcVar10 + uVar8;
  }
  if ((char *)plVar6[3] == (char *)plVar6[4]) {
                    /* try { // try from 00e5e0c0 to 00e5e10f has its CatchHandler @ 00e5e260 */
    cVar3 = (**(code **)(*plVar6 + 0x48))(plVar6);
  }
  else {
    cVar3 = *(char *)plVar6[3];
  }
  iVar4 = __num_get<char>::__stage2_float_loop
                    (cVar3,local_180,local_184,pcVar10,&local_170,local_134[0],local_138[0],
                     local_150,local_130,&local_178,&local_17c,(char *)aiStack_90);
  if (iVar4 != 0) goto LAB_00e5e114;
  plVar7 = plVar6;
  if (plVar6[3] == plVar6[4]) {
    (**(code **)(*plVar6 + 0x50))(plVar6);
  }
  else {
    plVar6[3] = plVar6[3] + 1;
  }
  goto LAB_00e5dfd0;
LAB_00e5e114:
  uVar8 = (ulong)((byte)local_150[0] >> 1);
  if (((byte)local_150[0] & 1) != 0) {
    uVar8 = local_148;
  }
  if (((local_180[0] != false) && (uVar8 != 0)) && ((long)local_178 - (long)local_130 < 0xa0)) {
    *local_178 = local_17c;
    local_178 = local_178 + 1;
  }
                    /* try { // try from 00e5e160 to 00e5e23b has its CatchHandler @ 00e5e258 */
  auVar11 = FUN_00e88be4(pcVar10,local_170,param_4);
  *(undefined (*) [16])param_5 = auVar11;
  __check_grouping(local_150,local_130,local_178,param_4);
  plVar7 = plVar6;
  if ((plVar6 == (long *)0x0) || (plVar6[3] != plVar6[4])) {
    if (plVar9 != (long *)0x0) goto LAB_00e5e19c;
LAB_00e5e248:
    iVar5 = (istreambuf_iterator)plVar7;
    if (plVar7 != (long *)0x0) goto LAB_00e5e1d0;
  }
  else {
    iVar4 = (**(code **)(*plVar6 + 0x48))(plVar6);
    plVar7 = (long *)0x0;
    if (iVar4 != -1) {
      plVar7 = plVar6;
    }
    if (plVar9 == (long *)0x0) goto LAB_00e5e248;
LAB_00e5e19c:
    iVar5 = (istreambuf_iterator)plVar7;
    if ((plVar9[3] == plVar9[4]) && (iVar4 = (**(code **)(*plVar9 + 0x48))(plVar9), iVar4 == -1))
    goto LAB_00e5e248;
    if (plVar7 == (long *)0x0) goto LAB_00e5e1d0;
  }
  *param_4 = *param_4 | 2;
LAB_00e5e1d0:
  if ((local_168 & 1) != 0) {
    operator_delete(local_158);
  }
  if (((byte)local_150[0] & 1) != 0) {
    operator_delete(local_140);
  }
  if (*(long *)(lVar2 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar5;
}



// ==========================================================================================
// Function: __stage2_int_loop
// Address: 00e5e71c
// ==========================================================================================

/* std::__ndk1::__num_get<char>::__stage2_int_loop(char, int, char*, char*&, unsigned int&, char,
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >
   const&, unsigned int*, unsigned int*&, char*) */

undefined8
std::__ndk1::__num_get<char>::__stage2_int_loop
          (char param_1,int param_2,char *param_3,char **param_4,uint *param_5,char param_6,
          basic_string *param_7,uint *param_8,uint **param_9,char *param_10)

{
  ulong uVar1;
  uint uVar2;
  undefined *puVar3;
  char cVar4;
  char *pcVar5;
  uint *puVar6;
  char *pcVar7;
  long lVar8;
  
  puVar3 = PTR___src_01ff5698;
  pcVar5 = *param_4;
  if (pcVar5 == param_3) {
    if (param_10[0x18] == param_1) {
      cVar4 = '+';
LAB_00e5e7c0:
      *param_4 = param_3 + 1;
      *param_3 = cVar4;
      *param_5 = 0;
      return 0;
    }
    if (param_10[0x19] == param_1) {
      cVar4 = '-';
      goto LAB_00e5e7c0;
    }
  }
  uVar1 = (ulong)((byte)*param_7 >> 1);
  if (((byte)*param_7 & 1) != 0) {
    uVar1 = *(ulong *)(param_7 + 8);
  }
  if ((param_1 == param_6) && (uVar1 != 0)) {
    puVar6 = *param_9;
    if ((long)puVar6 - (long)param_8 < 0xa0) {
      uVar2 = *param_5;
      *param_9 = puVar6 + 1;
      *puVar6 = uVar2;
      *param_5 = 0;
      return 0;
    }
    return 0;
  }
  pcVar7 = param_10 + 0x1a;
  if (*param_10 == param_1) {
    lVar8 = 0;
LAB_00e5e9d0:
    pcVar7 = param_10 + lVar8;
  }
  else {
    if (param_10[1] == param_1) {
      lVar8 = 1;
      goto LAB_00e5e9d0;
    }
    if (param_10[2] == param_1) {
      lVar8 = 2;
      goto LAB_00e5e9d0;
    }
    if (param_10[3] == param_1) {
      lVar8 = 3;
      goto LAB_00e5e9d0;
    }
    if (param_10[4] == param_1) {
      lVar8 = 4;
      goto LAB_00e5e9d0;
    }
    if (param_10[5] == param_1) {
      lVar8 = 5;
      goto LAB_00e5e9d0;
    }
    if (param_10[6] == param_1) {
      lVar8 = 6;
      goto LAB_00e5e9d0;
    }
    if (param_10[7] == param_1) {
      lVar8 = 7;
      goto LAB_00e5e9d0;
    }
    if (param_10[8] == param_1) {
      lVar8 = 8;
      goto LAB_00e5e9d0;
    }
    if (param_10[9] == param_1) {
      lVar8 = 9;
      goto LAB_00e5e9d0;
    }
    if (param_10[10] == param_1) {
      lVar8 = 10;
      goto LAB_00e5e9d0;
    }
    if (param_10[0xb] == param_1) {
      lVar8 = 0xb;
      goto LAB_00e5e9d0;
    }
    if (param_10[0xc] == param_1) {
      lVar8 = 0xc;
      goto LAB_00e5e9d0;
    }
    if (param_10[0xd] == param_1) {
      lVar8 = 0xd;
      goto LAB_00e5e9d0;
    }
    if (param_10[0xe] == param_1) {
      lVar8 = 0xe;
      goto LAB_00e5e9d0;
    }
    if (param_10[0xf] == param_1) {
      lVar8 = 0xf;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x10] == param_1) {
      lVar8 = 0x10;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x11] == param_1) {
      lVar8 = 0x11;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x12] == param_1) {
      lVar8 = 0x12;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x13] == param_1) {
      lVar8 = 0x13;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x14] == param_1) {
      lVar8 = 0x14;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x15] == param_1) {
      lVar8 = 0x15;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x16] == param_1) {
      lVar8 = 0x16;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x17] == param_1) {
      lVar8 = 0x17;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x18] == param_1) {
      lVar8 = 0x18;
      goto LAB_00e5e9d0;
    }
    if (param_10[0x19] == param_1) {
      lVar8 = 0x19;
      goto LAB_00e5e9d0;
    }
  }
  lVar8 = (long)pcVar7 - (long)param_10;
  if (lVar8 < 0x18) {
    if (param_2 != 8) {
      if (param_2 == 0x10) {
        if (0x15 < lVar8) {
          if (pcVar5 == param_3) {
            return 0xffffffff;
          }
          if (2 < (long)pcVar5 - (long)param_3) {
            return 0xffffffff;
          }
          if (pcVar5[-1] != '0') {
            return 0xffffffff;
          }
          *param_5 = 0;
          cVar4 = puVar3[lVar8];
          *param_4 = pcVar5 + 1;
          *pcVar5 = cVar4;
          return 0;
        }
        goto LAB_00e5ea14;
      }
      if (param_2 != 10) goto LAB_00e5ea14;
    }
    if (lVar8 < (long)(ulong)(uint)param_2) {
LAB_00e5ea14:
      cVar4 = PTR___src_01ff5698[lVar8];
      *param_4 = pcVar5 + 1;
      *pcVar5 = cVar4;
      *param_5 = *param_5 + 1;
      return 0;
    }
  }
  return 0xffffffff;
}



// ==========================================================================================
// Function: __libcpp_sscanf_l
// Address: 00e5ea80
// ==========================================================================================

/* std::__ndk1::__libcpp_sscanf_l(char const*, __locale_t*, char const*, ...) */

int std::__ndk1::__libcpp_sscanf_l(char *param_1,__locale_t *param_2,char *param_3,...)

{
  long lVar1;
  int iVar2;
  __locale_t __dataset;
  undefined8 in_x3;
  undefined8 in_x4;
  undefined8 in_x5;
  undefined8 in_x6;
  undefined8 in_x7;
  long lVar3;
  undefined auStack_c0 [8];
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined *local_90;
  undefined **ppuStack_88;
  undefined *puStack_80;
  undefined8 uStack_78;
  
  lVar1 = tpidr_el0;
  lVar3 = *(long *)(lVar1 + 0x28);
  local_b8 = in_x3;
  uStack_b0 = in_x4;
  local_a8 = in_x5;
  uStack_a0 = in_x6;
  local_98 = in_x7;
  local_90 = (undefined *)register0x00000008;
  __dataset = uselocale((__locale_t)param_2);
  uStack_78 = 0xffffff80ffffffd8;
  ppuStack_88 = &local_90;
  puStack_80 = auStack_c0;
  iVar2 = vsscanf(param_1,param_3,&local_90);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e5eb20 to 00e5eb27 has its CatchHandler @ 00e5eb5c */
    uselocale(__dataset);
  }
  if (*(long *)(lVar1 + 0x28) == lVar3) {
    return iVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __cloc
// Address: 00e5eb60
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__cloc() */

__locale_t std::__ndk1::__cloc(void)

{
  int iVar1;
  
  if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e5eba8 to 00e5ebbb has its CatchHandler @ 00e5ebd0 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  return DAT_0231cfa8;
}



// ==========================================================================================
// Function: __do_get_signed<long>
// Address: 00e5f368
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >
   >::__do_get_signed<long>(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_signed<long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,long *param_5)

{
  uint uVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  bool bVar5;
  wchar_t wVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  long *plVar10;
  long *plVar11;
  istreambuf_iterator iVar12;
  char *pcVar13;
  ulong uVar14;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar11 = (long *)(ulong)param_2;
  plVar10 = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar8 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar8 = 8;
  }
  else if (uVar1 == 8) {
    iVar8 = 0x10;
  }
  else {
    iVar8 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e5f404 to 00e5f417 has its CatchHandler @ 00e5f6fc */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar13 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar13 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar13;
LAB_00e5f44c:
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5f490;
LAB_00e5f4c4:
    plVar11 = (long *)0x0;
    if (bVar5) goto LAB_00e5f5a8;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
                    /* try { // try from 00e5f478 to 00e5f4b3 has its CatchHandler @ 00e5f708 */
      iVar7 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar7 = *(int *)plVar10[3];
    }
    bVar5 = iVar7 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5f4c4;
LAB_00e5f490:
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar7 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar7 = *(int *)plVar11[3];
    }
    if (iVar7 == -1) goto LAB_00e5f4c4;
    if (!bVar5) goto LAB_00e5f5a8;
  }
  uVar14 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar14 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar13 + uVar14) {
                    /* try { // try from 00e5f4f4 to 00e5f523 has its CatchHandler @ 00e5f704 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar14 << 1,'\0');
    uVar2 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar2 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar2,'\0');
    pcVar13 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar13 = local_1a0;
    }
    local_1b8 = pcVar13 + uVar14;
  }
  if ((wchar_t *)plVar10[3] == (wchar_t *)plVar10[4]) {
                    /* try { // try from 00e5f558 to 00e5f5a3 has its CatchHandler @ 00e5f708 */
    wVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
  }
  else {
    wVar6 = *(wchar_t *)plVar10[3];
  }
  iVar7 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar6,iVar8,pcVar13,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar7 != 0) goto LAB_00e5f5a8;
  if (plVar10[3] == plVar10[4]) {
    (**(code **)(*plVar10 + 0x50))(plVar10);
  }
  else {
    plVar10[3] = plVar10[3] + 4;
  }
  goto LAB_00e5f44c;
LAB_00e5f5a8:
  uVar14 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar14 = local_190;
  }
  if ((uVar14 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e5f5e8 to 00e5f67f has its CatchHandler @ 00e5f700 */
  lVar9 = FUN_00e880fc(pcVar13,local_1b8,param_4,iVar8);
  *param_5 = lVar9;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5f65c;
LAB_00e5f634:
    iVar12 = (istreambuf_iterator)plVar10;
    if (!bVar5) goto LAB_00e5f69c;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    bVar5 = iVar8 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5f634;
LAB_00e5f65c:
    iVar12 = (istreambuf_iterator)plVar10;
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar8 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar8 = *(int *)plVar11[3];
    }
    if (bVar5 != (iVar8 == -1)) goto LAB_00e5f69c;
  }
  *param_4 = *param_4 | 2;
LAB_00e5f69c:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar4 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar12;
}



// ==========================================================================================
// Function: __do_get_signed<long_long>
// Address: 00e5f74c
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_signed<long
   long>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_signed<long_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longlong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  bool bVar5;
  wchar_t wVar6;
  int iVar7;
  int iVar8;
  longlong lVar9;
  long *plVar10;
  long *plVar11;
  istreambuf_iterator iVar12;
  char *pcVar13;
  ulong uVar14;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar11 = (long *)(ulong)param_2;
  plVar10 = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar8 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar8 = 8;
  }
  else if (uVar1 == 8) {
    iVar8 = 0x10;
  }
  else {
    iVar8 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e5f7e8 to 00e5f7fb has its CatchHandler @ 00e5fae0 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar13 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar13 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar13;
LAB_00e5f830:
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5f874;
LAB_00e5f8a8:
    plVar11 = (long *)0x0;
    if (bVar5) goto LAB_00e5f98c;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
                    /* try { // try from 00e5f85c to 00e5f897 has its CatchHandler @ 00e5faec */
      iVar7 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar7 = *(int *)plVar10[3];
    }
    bVar5 = iVar7 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5f8a8;
LAB_00e5f874:
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar7 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar7 = *(int *)plVar11[3];
    }
    if (iVar7 == -1) goto LAB_00e5f8a8;
    if (!bVar5) goto LAB_00e5f98c;
  }
  uVar14 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar14 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar13 + uVar14) {
                    /* try { // try from 00e5f8d8 to 00e5f907 has its CatchHandler @ 00e5fae8 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar14 << 1,'\0');
    uVar2 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar2 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar2,'\0');
    pcVar13 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar13 = local_1a0;
    }
    local_1b8 = pcVar13 + uVar14;
  }
  if ((wchar_t *)plVar10[3] == (wchar_t *)plVar10[4]) {
                    /* try { // try from 00e5f93c to 00e5f987 has its CatchHandler @ 00e5faec */
    wVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
  }
  else {
    wVar6 = *(wchar_t *)plVar10[3];
  }
  iVar7 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar6,iVar8,pcVar13,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar7 != 0) goto LAB_00e5f98c;
  if (plVar10[3] == plVar10[4]) {
    (**(code **)(*plVar10 + 0x50))(plVar10);
  }
  else {
    plVar10[3] = plVar10[3] + 4;
  }
  goto LAB_00e5f830;
LAB_00e5f98c:
  uVar14 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar14 = local_190;
  }
  if ((uVar14 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e5f9cc to 00e5fa63 has its CatchHandler @ 00e5fae4 */
  lVar9 = FUN_00e8824c(pcVar13,local_1b8,param_4,iVar8);
  *param_5 = lVar9;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5fa40;
LAB_00e5fa18:
    iVar12 = (istreambuf_iterator)plVar10;
    if (!bVar5) goto LAB_00e5fa80;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    bVar5 = iVar8 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5fa18;
LAB_00e5fa40:
    iVar12 = (istreambuf_iterator)plVar10;
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar8 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar8 = *(int *)plVar11[3];
    }
    if (bVar5 != (iVar8 == -1)) goto LAB_00e5fa80;
  }
  *param_4 = *param_4 | 2;
LAB_00e5fa80:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar4 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar12;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_short>
// Address: 00e5fb30
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_unsigned<unsigned
   short>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, unsigned short&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_short>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ushort *param_5)

{
  uint uVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  bool bVar5;
  ushort uVar6;
  wchar_t wVar7;
  int iVar8;
  int iVar9;
  long *plVar10;
  long *plVar11;
  istreambuf_iterator iVar12;
  char *pcVar13;
  ulong uVar14;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar11 = (long *)(ulong)param_2;
  plVar10 = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar9 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar9 = 8;
  }
  else if (uVar1 == 8) {
    iVar9 = 0x10;
  }
  else {
    iVar9 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e5fbcc to 00e5fbdf has its CatchHandler @ 00e5fec4 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar13 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar13 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar13;
LAB_00e5fc14:
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5fc58;
LAB_00e5fc8c:
    plVar11 = (long *)0x0;
    if (bVar5) goto LAB_00e5fd70;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
                    /* try { // try from 00e5fc40 to 00e5fc7b has its CatchHandler @ 00e5fed0 */
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    bVar5 = iVar8 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5fc8c;
LAB_00e5fc58:
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar8 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar8 = *(int *)plVar11[3];
    }
    if (iVar8 == -1) goto LAB_00e5fc8c;
    if (!bVar5) goto LAB_00e5fd70;
  }
  uVar14 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar14 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar13 + uVar14) {
                    /* try { // try from 00e5fcbc to 00e5fceb has its CatchHandler @ 00e5fecc */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar14 << 1,'\0');
    uVar2 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar2 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar2,'\0');
    pcVar13 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar13 = local_1a0;
    }
    local_1b8 = pcVar13 + uVar14;
  }
  if ((wchar_t *)plVar10[3] == (wchar_t *)plVar10[4]) {
                    /* try { // try from 00e5fd20 to 00e5fd6b has its CatchHandler @ 00e5fed0 */
    wVar7 = (**(code **)(*plVar10 + 0x48))(plVar10);
  }
  else {
    wVar7 = *(wchar_t *)plVar10[3];
  }
  iVar8 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar7,iVar9,pcVar13,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar8 != 0) goto LAB_00e5fd70;
  if (plVar10[3] == plVar10[4]) {
    (**(code **)(*plVar10 + 0x50))(plVar10);
  }
  else {
    plVar10[3] = plVar10[3] + 4;
  }
  goto LAB_00e5fc14;
LAB_00e5fd70:
  uVar14 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar14 = local_190;
  }
  if ((uVar14 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e5fdb0 to 00e5fe47 has its CatchHandler @ 00e5fec8 */
  uVar6 = FUN_00e8839c(pcVar13,local_1b8,param_4,iVar9);
  *param_5 = uVar6;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e5fe24;
LAB_00e5fdfc:
    iVar12 = (istreambuf_iterator)plVar10;
    if (!bVar5) goto LAB_00e5fe64;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar9 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar9 = *(int *)plVar10[3];
    }
    bVar5 = iVar9 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e5fdfc;
LAB_00e5fe24:
    iVar12 = (istreambuf_iterator)plVar10;
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar9 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar9 = *(int *)plVar11[3];
    }
    if (bVar5 != (iVar9 == -1)) goto LAB_00e5fe64;
  }
  *param_4 = *param_4 | 2;
LAB_00e5fe64:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar4 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar12;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_int>
// Address: 00e5ff14
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_unsigned<unsigned
   int>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, unsigned int&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_int>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,uint *param_5)

{
  ulong uVar1;
  long *plVar2;
  long lVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  uint uVar7;
  int iVar8;
  long *plVar9;
  long *plVar10;
  istreambuf_iterator iVar11;
  char *pcVar12;
  ulong uVar13;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar10 = (long *)(ulong)param_2;
  plVar9 = (long *)(ulong)param_1;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  uVar7 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar7 == 0) {
    iVar8 = 0;
  }
  else if (uVar7 == 0x40) {
    iVar8 = 8;
  }
  else if (uVar7 == 8) {
    iVar8 = 0x10;
  }
  else {
    iVar8 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e5ffb0 to 00e5ffc3 has its CatchHandler @ 00e602a8 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar12 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar12 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar12;
LAB_00e5fff8:
  if (plVar9 == (long *)0x0) {
    bVar4 = true;
    if (plVar10 != (long *)0x0) goto LAB_00e6003c;
LAB_00e60070:
    plVar10 = (long *)0x0;
    if (bVar4) goto LAB_00e60154;
  }
  else {
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
                    /* try { // try from 00e60024 to 00e6005f has its CatchHandler @ 00e602b4 */
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar9;
    }
    plVar9 = plVar2;
    if (plVar10 == (long *)0x0) goto LAB_00e60070;
LAB_00e6003c:
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar6 = *(int *)plVar10[3];
    }
    if (iVar6 == -1) goto LAB_00e60070;
    if (!bVar4) goto LAB_00e60154;
  }
  uVar13 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar13 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar12 + uVar13) {
                    /* try { // try from 00e600a0 to 00e600cf has its CatchHandler @ 00e602b0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar13 << 1,'\0');
    uVar1 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar1 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar1,'\0');
    pcVar12 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar12 = local_1a0;
    }
    local_1b8 = pcVar12 + uVar13;
  }
  if ((wchar_t *)plVar9[3] == (wchar_t *)plVar9[4]) {
                    /* try { // try from 00e60104 to 00e6014f has its CatchHandler @ 00e602b4 */
    wVar5 = (**(code **)(*plVar9 + 0x48))(plVar9);
  }
  else {
    wVar5 = *(wchar_t *)plVar9[3];
  }
  iVar6 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar5,iVar8,pcVar12,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar6 != 0) goto LAB_00e60154;
  if (plVar9[3] == plVar9[4]) {
    (**(code **)(*plVar9 + 0x50))(plVar9);
  }
  else {
    plVar9[3] = plVar9[3] + 4;
  }
  goto LAB_00e5fff8;
LAB_00e60154:
  uVar13 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar13 = local_190;
  }
  if ((uVar13 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e60194 to 00e6022b has its CatchHandler @ 00e602ac */
  uVar7 = FUN_00e88520(pcVar12,local_1b8,param_4,iVar8);
  *param_5 = uVar7;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar9 == (long *)0x0) {
    bVar4 = true;
    if (plVar10 != (long *)0x0) goto LAB_00e60208;
LAB_00e601e0:
    iVar11 = (istreambuf_iterator)plVar9;
    if (!bVar4) goto LAB_00e60248;
  }
  else {
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar8 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar8 = *(int *)plVar9[3];
    }
    bVar4 = iVar8 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar9;
    }
    plVar9 = plVar2;
    if (plVar10 == (long *)0x0) goto LAB_00e601e0;
LAB_00e60208:
    iVar11 = (istreambuf_iterator)plVar9;
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    if (bVar4 != (iVar8 == -1)) goto LAB_00e60248;
  }
  *param_4 = *param_4 | 2;
LAB_00e60248:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar11;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long>
// Address: 00e602f8
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_unsigned<unsigned
   long>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, unsigned long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  bool bVar5;
  wchar_t wVar6;
  int iVar7;
  int iVar8;
  ulong uVar9;
  long *plVar10;
  long *plVar11;
  istreambuf_iterator iVar12;
  char *pcVar13;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar11 = (long *)(ulong)param_2;
  plVar10 = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar8 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar8 = 8;
  }
  else if (uVar1 == 8) {
    iVar8 = 0x10;
  }
  else {
    iVar8 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e60394 to 00e603a7 has its CatchHandler @ 00e6068c */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar13 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar13 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar13;
LAB_00e603dc:
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e60420;
LAB_00e60454:
    plVar11 = (long *)0x0;
    if (bVar5) goto LAB_00e60538;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
                    /* try { // try from 00e60408 to 00e60443 has its CatchHandler @ 00e60698 */
      iVar7 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar7 = *(int *)plVar10[3];
    }
    bVar5 = iVar7 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e60454;
LAB_00e60420:
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar7 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar7 = *(int *)plVar11[3];
    }
    if (iVar7 == -1) goto LAB_00e60454;
    if (!bVar5) goto LAB_00e60538;
  }
  uVar9 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar9 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar13 + uVar9) {
                    /* try { // try from 00e60484 to 00e604b3 has its CatchHandler @ 00e60694 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar9 << 1,'\0');
    uVar2 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar2 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar2,'\0');
    pcVar13 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar13 = local_1a0;
    }
    local_1b8 = pcVar13 + uVar9;
  }
  if ((wchar_t *)plVar10[3] == (wchar_t *)plVar10[4]) {
                    /* try { // try from 00e604e8 to 00e60533 has its CatchHandler @ 00e60698 */
    wVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
  }
  else {
    wVar6 = *(wchar_t *)plVar10[3];
  }
  iVar7 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar6,iVar8,pcVar13,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar7 != 0) goto LAB_00e60538;
  if (plVar10[3] == plVar10[4]) {
    (**(code **)(*plVar10 + 0x50))(plVar10);
  }
  else {
    plVar10[3] = plVar10[3] + 4;
  }
  goto LAB_00e603dc;
LAB_00e60538:
  uVar9 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar9 = local_190;
  }
  if ((uVar9 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e60578 to 00e6060f has its CatchHandler @ 00e60690 */
  uVar9 = FUN_00e886a4(pcVar13,local_1b8,param_4,iVar8);
  *param_5 = uVar9;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e605ec;
LAB_00e605c4:
    iVar12 = (istreambuf_iterator)plVar10;
    if (!bVar5) goto LAB_00e6062c;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    bVar5 = iVar8 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e605c4;
LAB_00e605ec:
    iVar12 = (istreambuf_iterator)plVar10;
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar8 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar8 = *(int *)plVar11[3];
    }
    if (bVar5 != (iVar8 == -1)) goto LAB_00e6062c;
  }
  *param_4 = *param_4 | 2;
LAB_00e6062c:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar4 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar12;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long_long>
// Address: 00e606dc
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_unsigned<unsigned long
   long>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, unsigned long long&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_long_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulonglong *param_5)

{
  uint uVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  bool bVar5;
  wchar_t wVar6;
  int iVar7;
  int iVar8;
  ulonglong uVar9;
  long *plVar10;
  long *plVar11;
  istreambuf_iterator iVar12;
  char *pcVar13;
  ulong uVar14;
  uint local_1c4;
  uint *local_1c0;
  char *local_1b8;
  ulong local_1b0;
  ulong local_1a8;
  char *local_1a0;
  basic_string local_198 [8];
  ulong local_190;
  void *local_188;
  wchar_t local_17c;
  uint local_178 [40];
  wchar_t awStack_d8 [26];
  long local_70;
  
  plVar11 = (long *)(ulong)param_2;
  plVar10 = (long *)(ulong)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  uVar1 = *(uint *)(param_3 + 8) & 0x4a;
  if (uVar1 == 0) {
    iVar8 = 0;
  }
  else if (uVar1 == 0x40) {
    iVar8 = 8;
  }
  else if (uVar1 == 8) {
    iVar8 = 0x10;
  }
  else {
    iVar8 = 10;
  }
  __num_get<wchar_t>::__stage2_int_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_d8,&local_17c,(wchar_t *)param_3);
  local_1b0 = 0;
  local_1a8 = 0;
  local_1a0 = (char *)0x0;
                    /* try { // try from 00e60778 to 00e6078b has its CatchHandler @ 00e60a70 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1b0,0x16,'\0');
  local_1c0 = local_178;
  pcVar13 = (char *)((ulong)&local_1b0 | 1);
  if ((local_1b0 & 1) != 0) {
    pcVar13 = local_1a0;
  }
  local_1c4 = 0;
  local_1b8 = pcVar13;
LAB_00e607c0:
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e60804;
LAB_00e60838:
    plVar11 = (long *)0x0;
    if (bVar5) goto LAB_00e6091c;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
                    /* try { // try from 00e607ec to 00e60827 has its CatchHandler @ 00e60a7c */
      iVar7 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar7 = *(int *)plVar10[3];
    }
    bVar5 = iVar7 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e60838;
LAB_00e60804:
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar7 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar7 = *(int *)plVar11[3];
    }
    if (iVar7 == -1) goto LAB_00e60838;
    if (!bVar5) goto LAB_00e6091c;
  }
  uVar14 = local_1a8;
  if ((local_1b0 & 1) == 0) {
    uVar14 = local_1b0 >> 1 & 0x7f;
  }
  if (local_1b8 == pcVar13 + uVar14) {
                    /* try { // try from 00e60868 to 00e60897 has its CatchHandler @ 00e60a78 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar14 << 1,'\0');
    uVar2 = 0x16;
    if ((local_1b0 & 1) != 0) {
      uVar2 = (local_1b0 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1b0,uVar2,'\0');
    pcVar13 = (char *)((ulong)&local_1b0 | 1);
    if ((local_1b0 & 1) != 0) {
      pcVar13 = local_1a0;
    }
    local_1b8 = pcVar13 + uVar14;
  }
  if ((wchar_t *)plVar10[3] == (wchar_t *)plVar10[4]) {
                    /* try { // try from 00e608cc to 00e60917 has its CatchHandler @ 00e60a7c */
    wVar6 = (**(code **)(*plVar10 + 0x48))(plVar10);
  }
  else {
    wVar6 = *(wchar_t *)plVar10[3];
  }
  iVar7 = __num_get<wchar_t>::__stage2_int_loop
                    (wVar6,iVar8,pcVar13,&local_1b8,&local_1c4,local_17c,local_198,local_178,
                     &local_1c0,awStack_d8);
  if (iVar7 != 0) goto LAB_00e6091c;
  if (plVar10[3] == plVar10[4]) {
    (**(code **)(*plVar10 + 0x50))(plVar10);
  }
  else {
    plVar10[3] = plVar10[3] + 4;
  }
  goto LAB_00e607c0;
LAB_00e6091c:
  uVar14 = (ulong)((byte)local_198[0] >> 1);
  if (((byte)local_198[0] & 1) != 0) {
    uVar14 = local_190;
  }
  if ((uVar14 != 0) && ((long)local_1c0 - (long)local_178 < 0xa0)) {
    *local_1c0 = local_1c4;
    local_1c0 = local_1c0 + 1;
  }
                    /* try { // try from 00e6095c to 00e609f3 has its CatchHandler @ 00e60a74 */
  uVar9 = FUN_00e88818(pcVar13,local_1b8,param_4,iVar8);
  *param_5 = uVar9;
  __check_grouping(local_198,local_178,local_1c0,param_4);
  if (plVar10 == (long *)0x0) {
    bVar5 = true;
    if (plVar11 != (long *)0x0) goto LAB_00e609d0;
LAB_00e609a8:
    iVar12 = (istreambuf_iterator)plVar10;
    if (!bVar5) goto LAB_00e60a10;
  }
  else {
    if ((int *)plVar10[3] == (int *)plVar10[4]) {
      iVar8 = (**(code **)(*plVar10 + 0x48))(plVar10);
    }
    else {
      iVar8 = *(int *)plVar10[3];
    }
    bVar5 = iVar8 == -1;
    plVar3 = (long *)0x0;
    if (!bVar5) {
      plVar3 = plVar10;
    }
    plVar10 = plVar3;
    if (plVar11 == (long *)0x0) goto LAB_00e609a8;
LAB_00e609d0:
    iVar12 = (istreambuf_iterator)plVar10;
    if ((int *)plVar11[3] == (int *)plVar11[4]) {
      iVar8 = (**(code **)(*plVar11 + 0x48))(plVar11);
    }
    else {
      iVar8 = *(int *)plVar11[3];
    }
    if (bVar5 != (iVar8 == -1)) goto LAB_00e60a10;
  }
  *param_4 = *param_4 | 2;
LAB_00e60a10:
  if ((local_1b0 & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (((byte)local_198[0] & 1) != 0) {
    operator_delete(local_188);
  }
  if (*(long *)(lVar4 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar12;
}



// ==========================================================================================
// Function: __do_get_floating_point<float>
// Address: 00e60ac0
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >
   >::__do_get_floating_point<float>(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, float&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<float>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,float *param_5)

{
  ulong uVar1;
  long *plVar2;
  long lVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  long *plVar7;
  ulong uVar8;
  long *plVar9;
  istreambuf_iterator iVar10;
  char *pcVar11;
  float fVar12;
  char local_1e4 [4];
  bool local_1e0 [4];
  uint local_1dc;
  uint *local_1d8;
  char *local_1d0;
  ulong local_1c8;
  ulong local_1c0;
  char *local_1b8;
  basic_string local_1b0 [8];
  ulong local_1a8;
  void *local_1a0;
  wchar_t local_198;
  wchar_t wStack_194;
  uint local_190 [40];
  wchar_t awStack_f0 [32];
  long local_70;
  
  plVar9 = (long *)(ulong)param_2;
  plVar7 = (long *)(ulong)param_1;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  __num_get<wchar_t>::__stage2_float_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_f0,&wStack_194,&local_198,
             (wchar_t *)param_4);
  local_1c8 = 0;
  local_1c0 = 0;
  local_1b8 = (char *)0x0;
                    /* try { // try from 00e60b24 to 00e60b37 has its CatchHandler @ 00e60e3c */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1c8,0x16,'\0');
  pcVar11 = (char *)((ulong)&local_1c8 | 1);
  if ((local_1c8 & 1) != 0) {
    pcVar11 = local_1b8;
  }
  local_1dc = 0;
  local_1e0[0] = true;
  local_1e4[0] = 'E';
  local_1d8 = local_190;
  local_1d0 = pcVar11;
LAB_00e60b80:
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e60bc4;
LAB_00e60bf8:
    plVar9 = (long *)0x0;
    if (bVar4) goto LAB_00e60cdc;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
                    /* try { // try from 00e60bac to 00e60be7 has its CatchHandler @ 00e60e48 */
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e60bf8;
LAB_00e60bc4:
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (iVar6 == -1) goto LAB_00e60bf8;
    if (!bVar4) goto LAB_00e60cdc;
  }
  uVar8 = local_1c0;
  if ((local_1c8 & 1) == 0) {
    uVar8 = local_1c8 >> 1 & 0x7f;
  }
  if (local_1d0 == pcVar11 + uVar8) {
                    /* try { // try from 00e60c28 to 00e60c57 has its CatchHandler @ 00e60e44 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_1c8 & 1) != 0) {
      uVar1 = (local_1c8 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar1,'\0');
    pcVar11 = (char *)((ulong)&local_1c8 | 1);
    if ((local_1c8 & 1) != 0) {
      pcVar11 = local_1b8;
    }
    local_1d0 = pcVar11 + uVar8;
  }
  if ((wchar_t *)plVar7[3] == (wchar_t *)plVar7[4]) {
                    /* try { // try from 00e60c8c to 00e60cd7 has its CatchHandler @ 00e60e48 */
    wVar5 = (**(code **)(*plVar7 + 0x48))(plVar7);
  }
  else {
    wVar5 = *(wchar_t *)plVar7[3];
  }
  iVar6 = __num_get<wchar_t>::__stage2_float_loop
                    (wVar5,local_1e0,local_1e4,pcVar11,&local_1d0,wStack_194,local_198,local_1b0,
                     local_190,&local_1d8,&local_1dc,awStack_f0);
  if (iVar6 != 0) goto LAB_00e60cdc;
  if (plVar7[3] == plVar7[4]) {
    (**(code **)(*plVar7 + 0x50))(plVar7);
  }
  else {
    plVar7[3] = plVar7[3] + 4;
  }
  goto LAB_00e60b80;
LAB_00e60cdc:
  uVar8 = (ulong)((byte)local_1b0[0] >> 1);
  if (((byte)local_1b0[0] & 1) != 0) {
    uVar8 = local_1a8;
  }
  if (((local_1e0[0] != false) && (uVar8 != 0)) && ((long)local_1d8 - (long)local_190 < 0xa0)) {
    *local_1d8 = local_1dc;
    local_1d8 = local_1d8 + 1;
  }
                    /* try { // try from 00e60d28 to 00e60dbf has its CatchHandler @ 00e60e40 */
  fVar12 = (float)FUN_00e8898c(pcVar11,local_1d0,param_4);
  *param_5 = fVar12;
  __check_grouping(local_1b0,local_190,local_1d8,param_4);
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e60d9c;
LAB_00e60d70:
    iVar10 = (istreambuf_iterator)plVar7;
    if (!bVar4) goto LAB_00e60de0;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e60d70;
LAB_00e60d9c:
    iVar10 = (istreambuf_iterator)plVar7;
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (bVar4 != (iVar6 == -1)) goto LAB_00e60de0;
  }
  *param_4 = *param_4 | 2;
LAB_00e60de0:
  if ((local_1c8 & 1) != 0) {
    operator_delete(local_1b8);
  }
  if (((byte)local_1b0[0] & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar10;
}



// ==========================================================================================
// Function: __do_get_floating_point<double>
// Address: 00e60e8c
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >
   >::__do_get_floating_point<double>(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, std::__ndk1::ios_base&, unsigned int&, double&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<double>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,double *param_5)

{
  ulong uVar1;
  long *plVar2;
  long lVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  long *plVar7;
  ulong uVar8;
  long *plVar9;
  istreambuf_iterator iVar10;
  char *pcVar11;
  double dVar12;
  char local_1e4 [4];
  bool local_1e0 [4];
  uint local_1dc;
  uint *local_1d8;
  char *local_1d0;
  ulong local_1c8;
  ulong local_1c0;
  char *local_1b8;
  basic_string local_1b0 [8];
  ulong local_1a8;
  void *local_1a0;
  wchar_t local_198;
  wchar_t wStack_194;
  uint local_190 [40];
  wchar_t awStack_f0 [32];
  long local_70;
  
  plVar9 = (long *)(ulong)param_2;
  plVar7 = (long *)(ulong)param_1;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  __num_get<wchar_t>::__stage2_float_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_f0,&wStack_194,&local_198,
             (wchar_t *)param_4);
  local_1c8 = 0;
  local_1c0 = 0;
  local_1b8 = (char *)0x0;
                    /* try { // try from 00e60ef0 to 00e60f03 has its CatchHandler @ 00e61208 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1c8,0x16,'\0');
  pcVar11 = (char *)((ulong)&local_1c8 | 1);
  if ((local_1c8 & 1) != 0) {
    pcVar11 = local_1b8;
  }
  local_1dc = 0;
  local_1e0[0] = true;
  local_1e4[0] = 'E';
  local_1d8 = local_190;
  local_1d0 = pcVar11;
LAB_00e60f4c:
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e60f90;
LAB_00e60fc4:
    plVar9 = (long *)0x0;
    if (bVar4) goto LAB_00e610a8;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
                    /* try { // try from 00e60f78 to 00e60fb3 has its CatchHandler @ 00e61214 */
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e60fc4;
LAB_00e60f90:
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (iVar6 == -1) goto LAB_00e60fc4;
    if (!bVar4) goto LAB_00e610a8;
  }
  uVar8 = local_1c0;
  if ((local_1c8 & 1) == 0) {
    uVar8 = local_1c8 >> 1 & 0x7f;
  }
  if (local_1d0 == pcVar11 + uVar8) {
                    /* try { // try from 00e60ff4 to 00e61023 has its CatchHandler @ 00e61210 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_1c8 & 1) != 0) {
      uVar1 = (local_1c8 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar1,'\0');
    pcVar11 = (char *)((ulong)&local_1c8 | 1);
    if ((local_1c8 & 1) != 0) {
      pcVar11 = local_1b8;
    }
    local_1d0 = pcVar11 + uVar8;
  }
  if ((wchar_t *)plVar7[3] == (wchar_t *)plVar7[4]) {
                    /* try { // try from 00e61058 to 00e610a3 has its CatchHandler @ 00e61214 */
    wVar5 = (**(code **)(*plVar7 + 0x48))(plVar7);
  }
  else {
    wVar5 = *(wchar_t *)plVar7[3];
  }
  iVar6 = __num_get<wchar_t>::__stage2_float_loop
                    (wVar5,local_1e0,local_1e4,pcVar11,&local_1d0,wStack_194,local_198,local_1b0,
                     local_190,&local_1d8,&local_1dc,awStack_f0);
  if (iVar6 != 0) goto LAB_00e610a8;
  if (plVar7[3] == plVar7[4]) {
    (**(code **)(*plVar7 + 0x50))(plVar7);
  }
  else {
    plVar7[3] = plVar7[3] + 4;
  }
  goto LAB_00e60f4c;
LAB_00e610a8:
  uVar8 = (ulong)((byte)local_1b0[0] >> 1);
  if (((byte)local_1b0[0] & 1) != 0) {
    uVar8 = local_1a8;
  }
  if (((local_1e0[0] != false) && (uVar8 != 0)) && ((long)local_1d8 - (long)local_190 < 0xa0)) {
    *local_1d8 = local_1dc;
    local_1d8 = local_1d8 + 1;
  }
                    /* try { // try from 00e610f4 to 00e6118b has its CatchHandler @ 00e6120c */
  dVar12 = (double)FUN_00e88ab8(pcVar11,local_1d0,param_4);
  *param_5 = dVar12;
  __check_grouping(local_1b0,local_190,local_1d8,param_4);
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e61168;
LAB_00e6113c:
    iVar10 = (istreambuf_iterator)plVar7;
    if (!bVar4) goto LAB_00e611ac;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e6113c;
LAB_00e61168:
    iVar10 = (istreambuf_iterator)plVar7;
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (bVar4 != (iVar6 == -1)) goto LAB_00e611ac;
  }
  *param_4 = *param_4 | 2;
LAB_00e611ac:
  if ((local_1c8 & 1) != 0) {
    operator_delete(local_1b8);
  }
  if (((byte)local_1b0[0] & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar10;
}



// ==========================================================================================
// Function: __do_get_floating_point<long_double>
// Address: 00e61258
// ==========================================================================================

/* std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >
   std::__ndk1::num_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get_floating_point<long
   double>(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >,
   std::__ndk1::ios_base&, unsigned int&, long double&) const */

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<long_double>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longdouble *param_5)

{
  ulong uVar1;
  long *plVar2;
  long lVar3;
  bool bVar4;
  wchar_t wVar5;
  int iVar6;
  long *plVar7;
  ulong uVar8;
  long *plVar9;
  istreambuf_iterator iVar10;
  char *pcVar11;
  undefined auVar12 [16];
  char local_1e4 [4];
  bool local_1e0 [4];
  uint local_1dc;
  uint *local_1d8;
  char *local_1d0;
  ulong local_1c8;
  ulong local_1c0;
  char *local_1b8;
  basic_string local_1b0 [8];
  ulong local_1a8;
  void *local_1a0;
  wchar_t local_198;
  wchar_t wStack_194;
  uint local_190 [40];
  wchar_t awStack_f0 [32];
  long local_70;
  
  plVar9 = (long *)(ulong)param_2;
  plVar7 = (long *)(ulong)param_1;
  lVar3 = tpidr_el0;
  local_70 = *(long *)(lVar3 + 0x28);
  __num_get<wchar_t>::__stage2_float_prep
            ((__num_get<wchar_t> *)param_3,(ios_base *)awStack_f0,&wStack_194,&local_198,
             (wchar_t *)param_4);
  local_1c8 = 0;
  local_1c0 = 0;
  local_1b8 = (char *)0x0;
                    /* try { // try from 00e612bc to 00e612cf has its CatchHandler @ 00e615d4 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &local_1c8,0x16,'\0');
  pcVar11 = (char *)((ulong)&local_1c8 | 1);
  if ((local_1c8 & 1) != 0) {
    pcVar11 = local_1b8;
  }
  local_1dc = 0;
  local_1e0[0] = true;
  local_1e4[0] = 'E';
  local_1d8 = local_190;
  local_1d0 = pcVar11;
LAB_00e61318:
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e6135c;
LAB_00e61390:
    plVar9 = (long *)0x0;
    if (bVar4) goto LAB_00e61474;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
                    /* try { // try from 00e61344 to 00e6137f has its CatchHandler @ 00e615e0 */
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e61390;
LAB_00e6135c:
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (iVar6 == -1) goto LAB_00e61390;
    if (!bVar4) goto LAB_00e61474;
  }
  uVar8 = local_1c0;
  if ((local_1c8 & 1) == 0) {
    uVar8 = local_1c8 >> 1 & 0x7f;
  }
  if (local_1d0 == pcVar11 + uVar8) {
                    /* try { // try from 00e613c0 to 00e613ef has its CatchHandler @ 00e615dc */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar8 << 1,'\0');
    uVar1 = 0x16;
    if ((local_1c8 & 1) != 0) {
      uVar1 = (local_1c8 & 0xfffffffffffffffe) - 1;
    }
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::resize
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &local_1c8,uVar1,'\0');
    pcVar11 = (char *)((ulong)&local_1c8 | 1);
    if ((local_1c8 & 1) != 0) {
      pcVar11 = local_1b8;
    }
    local_1d0 = pcVar11 + uVar8;
  }
  if ((wchar_t *)plVar7[3] == (wchar_t *)plVar7[4]) {
                    /* try { // try from 00e61424 to 00e6146f has its CatchHandler @ 00e615e0 */
    wVar5 = (**(code **)(*plVar7 + 0x48))(plVar7);
  }
  else {
    wVar5 = *(wchar_t *)plVar7[3];
  }
  iVar6 = __num_get<wchar_t>::__stage2_float_loop
                    (wVar5,local_1e0,local_1e4,pcVar11,&local_1d0,wStack_194,local_198,local_1b0,
                     local_190,&local_1d8,&local_1dc,awStack_f0);
  if (iVar6 != 0) goto LAB_00e61474;
  if (plVar7[3] == plVar7[4]) {
    (**(code **)(*plVar7 + 0x50))(plVar7);
  }
  else {
    plVar7[3] = plVar7[3] + 4;
  }
  goto LAB_00e61318;
LAB_00e61474:
  uVar8 = (ulong)((byte)local_1b0[0] >> 1);
  if (((byte)local_1b0[0] & 1) != 0) {
    uVar8 = local_1a8;
  }
  if (((local_1e0[0] != false) && (uVar8 != 0)) && ((long)local_1d8 - (long)local_190 < 0xa0)) {
    *local_1d8 = local_1dc;
    local_1d8 = local_1d8 + 1;
  }
                    /* try { // try from 00e614c0 to 00e61557 has its CatchHandler @ 00e615d8 */
  auVar12 = FUN_00e88be4(pcVar11,local_1d0,param_4);
  *(undefined (*) [16])param_5 = auVar12;
  __check_grouping(local_1b0,local_190,local_1d8,param_4);
  if (plVar7 == (long *)0x0) {
    bVar4 = true;
    if (plVar9 != (long *)0x0) goto LAB_00e61534;
LAB_00e61508:
    iVar10 = (istreambuf_iterator)plVar7;
    if (!bVar4) goto LAB_00e61578;
  }
  else {
    if ((int *)plVar7[3] == (int *)plVar7[4]) {
      iVar6 = (**(code **)(*plVar7 + 0x48))(plVar7);
    }
    else {
      iVar6 = *(int *)plVar7[3];
    }
    bVar4 = iVar6 == -1;
    plVar2 = (long *)0x0;
    if (!bVar4) {
      plVar2 = plVar7;
    }
    plVar7 = plVar2;
    if (plVar9 == (long *)0x0) goto LAB_00e61508;
LAB_00e61534:
    iVar10 = (istreambuf_iterator)plVar7;
    if ((int *)plVar9[3] == (int *)plVar9[4]) {
      iVar6 = (**(code **)(*plVar9 + 0x48))(plVar9);
    }
    else {
      iVar6 = *(int *)plVar9[3];
    }
    if (bVar4 != (iVar6 == -1)) goto LAB_00e61578;
  }
  *param_4 = *param_4 | 2;
LAB_00e61578:
  if ((local_1c8 & 1) != 0) {
    operator_delete(local_1b8);
  }
  if (((byte)local_1b0[0] & 1) != 0) {
    operator_delete(local_1a0);
  }
  if (*(long *)(lVar3 + 0x28) != local_70) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar10;
}



// ==========================================================================================
// Function: __stage2_int_loop
// Address: 00e61ad4
// ==========================================================================================

/* std::__ndk1::__num_get<wchar_t>::__stage2_int_loop(wchar_t, int, char*, char*&, unsigned int&,
   wchar_t, std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, unsigned int*, unsigned int*&, wchar_t*) */

undefined8
std::__ndk1::__num_get<wchar_t>::__stage2_int_loop
          (wchar_t param_1,int param_2,char *param_3,char **param_4,uint *param_5,wchar_t param_6,
          basic_string *param_7,uint *param_8,uint **param_9,wchar_t *param_10)

{
  ulong uVar1;
  uint uVar2;
  undefined *puVar3;
  char cVar4;
  char *pcVar5;
  uint *puVar6;
  long lVar7;
  long lVar8;
  wchar_t *pwVar9;
  
  puVar3 = PTR___src_01ff5698;
  pcVar5 = *param_4;
  if (pcVar5 == param_3) {
    if (param_10[0x18] == param_1) {
      cVar4 = '+';
LAB_00e61b74:
      *param_4 = param_3 + 1;
      *param_3 = cVar4;
      *param_5 = 0;
      return 0;
    }
    if (param_10[0x19] == param_1) {
      cVar4 = '-';
      goto LAB_00e61b74;
    }
  }
  uVar1 = (ulong)((byte)*param_7 >> 1);
  if (((byte)*param_7 & 1) != 0) {
    uVar1 = *(ulong *)(param_7 + 8);
  }
  if ((param_1 == param_6) && (uVar1 != 0)) {
    puVar6 = *param_9;
    if ((long)puVar6 - (long)param_8 < 0xa0) {
      uVar2 = *param_5;
      *param_9 = puVar6 + 1;
      *puVar6 = uVar2;
      *param_5 = 0;
      return 0;
    }
    return 0;
  }
  pwVar9 = param_10 + 0x1a;
  if (*param_10 == param_1) {
    lVar8 = 0;
LAB_00e61d84:
    pwVar9 = param_10 + lVar8;
  }
  else {
    if (param_10[1] == param_1) {
      lVar8 = 1;
      goto LAB_00e61d84;
    }
    if (param_10[2] == param_1) {
      lVar8 = 2;
      goto LAB_00e61d84;
    }
    if (param_10[3] == param_1) {
      lVar8 = 3;
      goto LAB_00e61d84;
    }
    if (param_10[4] == param_1) {
      lVar8 = 4;
      goto LAB_00e61d84;
    }
    if (param_10[5] == param_1) {
      lVar8 = 5;
      goto LAB_00e61d84;
    }
    if (param_10[6] == param_1) {
      lVar8 = 6;
      goto LAB_00e61d84;
    }
    if (param_10[7] == param_1) {
      lVar8 = 7;
      goto LAB_00e61d84;
    }
    if (param_10[8] == param_1) {
      lVar8 = 8;
      goto LAB_00e61d84;
    }
    if (param_10[9] == param_1) {
      lVar8 = 9;
      goto LAB_00e61d84;
    }
    if (param_10[10] == param_1) {
      lVar8 = 10;
      goto LAB_00e61d84;
    }
    if (param_10[0xb] == param_1) {
      lVar8 = 0xb;
      goto LAB_00e61d84;
    }
    if (param_10[0xc] == param_1) {
      lVar8 = 0xc;
      goto LAB_00e61d84;
    }
    if (param_10[0xd] == param_1) {
      lVar8 = 0xd;
      goto LAB_00e61d84;
    }
    if (param_10[0xe] == param_1) {
      lVar8 = 0xe;
      goto LAB_00e61d84;
    }
    if (param_10[0xf] == param_1) {
      lVar8 = 0xf;
      goto LAB_00e61d84;
    }
    if (param_10[0x10] == param_1) {
      lVar8 = 0x10;
      goto LAB_00e61d84;
    }
    if (param_10[0x11] == param_1) {
      lVar8 = 0x11;
      goto LAB_00e61d84;
    }
    if (param_10[0x12] == param_1) {
      lVar8 = 0x12;
      goto LAB_00e61d84;
    }
    if (param_10[0x13] == param_1) {
      lVar8 = 0x13;
      goto LAB_00e61d84;
    }
    if (param_10[0x14] == param_1) {
      lVar8 = 0x14;
      goto LAB_00e61d84;
    }
    if (param_10[0x15] == param_1) {
      lVar8 = 0x15;
      goto LAB_00e61d84;
    }
    if (param_10[0x16] == param_1) {
      lVar8 = 0x16;
      goto LAB_00e61d84;
    }
    if (param_10[0x17] == param_1) {
      lVar8 = 0x17;
      goto LAB_00e61d84;
    }
    if (param_10[0x18] == param_1) {
      lVar8 = 0x18;
      goto LAB_00e61d84;
    }
    if (param_10[0x19] == param_1) {
      lVar8 = 0x19;
      goto LAB_00e61d84;
    }
  }
  lVar8 = (long)pwVar9 - (long)param_10;
  if (lVar8 < 0x5d) {
    lVar7 = lVar8 >> 2;
    if (param_2 != 8) {
      if (param_2 == 0x10) {
        if (0x57 < lVar8) {
          if (pcVar5 == param_3) {
            return 0xffffffff;
          }
          if (2 < (long)pcVar5 - (long)param_3) {
            return 0xffffffff;
          }
          if (pcVar5[-1] != '0') {
            return 0xffffffff;
          }
          *param_5 = 0;
          cVar4 = puVar3[lVar7];
          *param_4 = pcVar5 + 1;
          *pcVar5 = cVar4;
          return 0;
        }
        goto LAB_00e61dcc;
      }
      if (param_2 != 10) goto LAB_00e61dcc;
    }
    if (lVar7 < (long)(ulong)(uint)param_2) {
LAB_00e61dcc:
      cVar4 = PTR___src_01ff5698[lVar7];
      *param_4 = pcVar5 + 1;
      *pcVar5 = cVar4;
      *param_5 = *param_5 + 1;
      return 0;
    }
  }
  return 0xffffffff;
}



// ==========================================================================================
// Function: __stage2_float_prep
// Address: 00e61e38
// ==========================================================================================

/* std::__ndk1::__num_get<char>::__stage2_float_prep(std::__ndk1::ios_base&, char*, char&, char&) */

void __thiscall
std::__ndk1::__num_get<char>::__stage2_float_prep
          (__num_get<char> *this,ios_base *param_1,char *param_2,char *param_3,char *param_4)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  long *plVar5;
  long local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar3 = PTR___init_01ff5688;
  puVar2 = PTR_id_01ff5500;
  local_70 = 0;
  local_80 = PTR_id_01ff5500;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e61eb0 to 00e61f03 has its CatchHandler @ 00e61fe8 */
    __call_once((ulong *)PTR_id_01ff5500,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e61fdc to 00e61fdf has its CatchHandler @ 00e61fe8 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar5 + 0x40))(plVar5,PTR___src_01ff5698,PTR___src_01ff5698 + 0x20,param_1);
  puVar2 = PTR_id_01ff5690;
  local_70 = 0;
  local_80 = PTR_id_01ff5690;
  puStack_78 = puVar3;
  if (*(long *)PTR_id_01ff5690 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e61f30 to 00e61fa3 has its CatchHandler @ 00e61fec */
    __call_once((ulong *)PTR_id_01ff5690,&local_68,FUN_00e87ff8);
  }
  if (((long)*(int *)(puVar2 + 8) - 1U <
       (ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3)) &&
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 != (long *)0x0)) {
    cVar4 = (**(code **)(*plVar5 + 0x18))(plVar5);
    *param_2 = cVar4;
    cVar4 = (**(code **)(*plVar5 + 0x20))(plVar5);
    *param_3 = cVar4;
    (**(code **)(*plVar5 + 0x28))(plVar5);
    __shared_count::__release_shared();
    if (*(long *)(lVar1 + 0x28) == local_58) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e61fe0 to 00e61fe3 has its CatchHandler @ 00e61fec */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __stage2_float_loop
// Address: 00e62000
// ==========================================================================================

/* std::__ndk1::__num_get<char>::__stage2_float_loop(char, bool&, char&, char*, char*&, char, char,
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >
   const&, unsigned int*, unsigned int*&, unsigned int&, char*) */

undefined8
std::__ndk1::__num_get<char>::__stage2_float_loop
          (char param_1,bool *param_2,char *param_3,char *param_4,char **param_5,char param_6,
          char param_7,basic_string *param_8,uint *param_9,uint **param_10,uint *param_11,
          char *param_12)

{
  ulong uVar1;
  uint uVar2;
  byte bVar3;
  byte *pbVar4;
  char *pcVar5;
  uint *puVar6;
  long lVar7;
  
  if (param_1 == param_6) {
    if (*param_2 == false) {
      return 0xffffffff;
    }
    *param_2 = false;
    pcVar5 = *param_5;
    *param_5 = pcVar5 + 1;
    *pcVar5 = '.';
    uVar1 = (ulong)((byte)*param_8 >> 1);
    if (((byte)*param_8 & 1) != 0) {
      uVar1 = *(ulong *)(param_8 + 8);
    }
    if ((uVar1 != 0) && (puVar6 = *param_10, (long)puVar6 - (long)param_9 < 0xa0)) {
      uVar2 = *param_11;
      *param_10 = puVar6 + 1;
      *puVar6 = uVar2;
      return 0;
    }
    return 0;
  }
  if (param_1 == param_7) {
    uVar1 = (ulong)((byte)*param_8 >> 1);
    if (((byte)*param_8 & 1) != 0) {
      uVar1 = *(ulong *)(param_8 + 8);
    }
    if (uVar1 != 0) {
      if (*param_2 == false) {
        return 0xffffffff;
      }
      puVar6 = *param_10;
      if (0x9f < (long)puVar6 - (long)param_9) {
        return 0;
      }
      uVar2 = *param_11;
      *param_10 = puVar6 + 1;
      *puVar6 = uVar2;
      *param_11 = 0;
      return 0;
    }
  }
  pcVar5 = param_12 + 0x20;
  if (*param_12 == param_1) {
    lVar7 = 0;
  }
  else if (param_12[1] == param_1) {
    lVar7 = 1;
  }
  else if (param_12[2] == param_1) {
    lVar7 = 2;
  }
  else if (param_12[3] == param_1) {
    lVar7 = 3;
  }
  else if (param_12[4] == param_1) {
    lVar7 = 4;
  }
  else if (param_12[5] == param_1) {
    lVar7 = 5;
  }
  else if (param_12[6] == param_1) {
    lVar7 = 6;
  }
  else if (param_12[7] == param_1) {
    lVar7 = 7;
  }
  else if (param_12[8] == param_1) {
    lVar7 = 8;
  }
  else if (param_12[9] == param_1) {
    lVar7 = 9;
  }
  else if (param_12[10] == param_1) {
    lVar7 = 10;
  }
  else if (param_12[0xb] == param_1) {
    lVar7 = 0xb;
  }
  else if (param_12[0xc] == param_1) {
    lVar7 = 0xc;
  }
  else if (param_12[0xd] == param_1) {
    lVar7 = 0xd;
  }
  else if (param_12[0xe] == param_1) {
    lVar7 = 0xe;
  }
  else if (param_12[0xf] == param_1) {
    lVar7 = 0xf;
  }
  else if (param_12[0x10] == param_1) {
    lVar7 = 0x10;
  }
  else if (param_12[0x11] == param_1) {
    lVar7 = 0x11;
  }
  else if (param_12[0x12] == param_1) {
    lVar7 = 0x12;
  }
  else if (param_12[0x13] == param_1) {
    lVar7 = 0x13;
  }
  else if (param_12[0x14] == param_1) {
    lVar7 = 0x14;
  }
  else if (param_12[0x15] == param_1) {
    lVar7 = 0x15;
  }
  else if (param_12[0x16] == param_1) {
    lVar7 = 0x16;
  }
  else if (param_12[0x17] == param_1) {
    lVar7 = 0x17;
  }
  else if (param_12[0x18] == param_1) {
    lVar7 = 0x18;
  }
  else if (param_12[0x19] == param_1) {
    lVar7 = 0x19;
  }
  else if (param_12[0x1a] == param_1) {
    lVar7 = 0x1a;
  }
  else if (param_12[0x1b] == param_1) {
    lVar7 = 0x1b;
  }
  else if (param_12[0x1c] == param_1) {
    lVar7 = 0x1c;
  }
  else if (param_12[0x1d] == param_1) {
    lVar7 = 0x1d;
  }
  else if (param_12[0x1e] == param_1) {
    lVar7 = 0x1e;
  }
  else {
    if (param_12[0x1f] != param_1) goto LAB_00e6235c;
    lVar7 = 0x1f;
  }
  pcVar5 = param_12 + lVar7;
LAB_00e6235c:
  lVar7 = (long)pcVar5 - (long)param_12;
  if (0x1f < lVar7) {
    return 0xffffffff;
  }
  bVar3 = PTR___src_01ff5698[lVar7];
  if (lVar7 - 0x16U < 2) {
    *param_3 = 'P';
    pbVar4 = (byte *)*param_5;
  }
  else {
    if (1 < lVar7 - 0x18U) {
      if (((bVar3 & 0x5f) == *param_3) && (*param_3 = bVar3 & 0x5f | 0x80, *param_2 != false)) {
        *param_2 = false;
        uVar1 = (ulong)((byte)*param_8 >> 1);
        if (((byte)*param_8 & 1) != 0) {
          uVar1 = *(ulong *)(param_8 + 8);
        }
        if ((uVar1 != 0) && (puVar6 = *param_10, (long)puVar6 - (long)param_9 < 0xa0)) {
          uVar2 = *param_11;
          *param_10 = puVar6 + 1;
          *puVar6 = uVar2;
        }
      }
      pbVar4 = (byte *)*param_5;
      *param_5 = (char *)(pbVar4 + 1);
      *pbVar4 = bVar3;
      if (lVar7 < 0x16) {
        *param_11 = *param_11 + 1;
      }
      return 0;
    }
    pbVar4 = (byte *)*param_5;
    if ((pbVar4 != (byte *)param_4) && ((pbVar4[-1] & 0x5f) != (*param_3 & 0x7fU))) {
      return 0xffffffff;
    }
  }
  *param_5 = (char *)(pbVar4 + 1);
  *pbVar4 = bVar3;
  return 0;
}



// ==========================================================================================
// Function: __stage2_int_prep
// Address: 00e6246c
// ==========================================================================================

/* std::__ndk1::__num_get<char>::__stage2_int_prep(std::__ndk1::ios_base&, char*, char&) */

void __thiscall
std::__ndk1::__num_get<char>::__stage2_int_prep
          (__num_get<char> *this,ios_base *param_1,char *param_2,char *param_3)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  long *plVar5;
  long local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar3 = PTR___init_01ff5688;
  puVar2 = PTR_id_01ff5500;
  local_70 = 0;
  local_80 = PTR_id_01ff5500;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e624e0 to 00e62533 has its CatchHandler @ 00e62604 */
    __call_once((ulong *)PTR_id_01ff5500,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e625f8 to 00e625fb has its CatchHandler @ 00e62604 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar5 + 0x40))(plVar5,PTR___src_01ff5698,PTR___src_01ff5698 + 0x1a,param_1);
  puVar2 = PTR_id_01ff5690;
  local_70 = 0;
  local_80 = PTR_id_01ff5690;
  puStack_78 = puVar3;
  if (*(long *)PTR_id_01ff5690 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e62560 to 00e625bf has its CatchHandler @ 00e62608 */
    __call_once((ulong *)PTR_id_01ff5690,&local_68,FUN_00e87ff8);
  }
  if (((long)*(int *)(puVar2 + 8) - 1U <
       (ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3)) &&
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 != (long *)0x0)) {
    cVar4 = (**(code **)(*plVar5 + 0x20))(plVar5);
    *param_2 = cVar4;
    (**(code **)(*plVar5 + 0x28))(plVar5);
    __shared_count::__release_shared();
    if (*(long *)(lVar1 + 0x28) == local_58) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e625fc to 00e625ff has its CatchHandler @ 00e62608 */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __stage2_float_prep
// Address: 00e6261c
// ==========================================================================================

/* std::__ndk1::__num_get<wchar_t>::__stage2_float_prep(std::__ndk1::ios_base&, wchar_t*, wchar_t&,
   wchar_t&) */

void __thiscall
std::__ndk1::__num_get<wchar_t>::__stage2_float_prep
          (__num_get<wchar_t> *this,ios_base *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t *param_4)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  wchar_t wVar4;
  long *plVar5;
  long local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar3 = PTR___init_01ff5688;
  puVar2 = PTR_id_01ff5620;
  local_70 = 0;
  local_80 = PTR_id_01ff5620;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e62694 to 00e626e7 has its CatchHandler @ 00e627cc */
    __call_once((ulong *)PTR_id_01ff5620,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e627c0 to 00e627c3 has its CatchHandler @ 00e627cc */
    FUN_00de5da0();
  }
  (**(code **)(*plVar5 + 0x60))(plVar5,PTR___src_01ff5698,PTR___src_01ff5698 + 0x20,param_1);
  puVar2 = PTR_id_01ff56a0;
  local_70 = 0;
  local_80 = PTR_id_01ff56a0;
  puStack_78 = puVar3;
  if (*(long *)PTR_id_01ff56a0 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e62714 to 00e62787 has its CatchHandler @ 00e627d0 */
    __call_once((ulong *)PTR_id_01ff56a0,&local_68,FUN_00e87ff8);
  }
  if (((long)*(int *)(puVar2 + 8) - 1U <
       (ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3)) &&
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 != (long *)0x0)) {
    wVar4 = (**(code **)(*plVar5 + 0x18))(plVar5);
    *param_2 = wVar4;
    wVar4 = (**(code **)(*plVar5 + 0x20))(plVar5);
    *param_3 = wVar4;
    (**(code **)(*plVar5 + 0x28))(plVar5);
    __shared_count::__release_shared();
    if (*(long *)(lVar1 + 0x28) == local_58) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e627c4 to 00e627c7 has its CatchHandler @ 00e627d0 */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __stage2_float_loop
// Address: 00e627e4
// ==========================================================================================

/* std::__ndk1::__num_get<wchar_t>::__stage2_float_loop(wchar_t, bool&, char&, char*, char*&,
   wchar_t, wchar_t, std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, unsigned int*, unsigned int*&, unsigned int&, wchar_t*) */

undefined8
std::__ndk1::__num_get<wchar_t>::__stage2_float_loop
          (wchar_t param_1,bool *param_2,char *param_3,char *param_4,char **param_5,wchar_t param_6,
          wchar_t param_7,basic_string *param_8,uint *param_9,uint **param_10,uint *param_11,
          wchar_t *param_12)

{
  uint uVar1;
  byte bVar2;
  byte *pbVar3;
  char *pcVar4;
  uint *puVar5;
  long lVar6;
  wchar_t *pwVar7;
  ulong uVar8;
  
  if (param_1 == param_6) {
    if (*param_2 == false) {
      return 0xffffffff;
    }
    *param_2 = false;
    pcVar4 = *param_5;
    *param_5 = pcVar4 + 1;
    *pcVar4 = '.';
    uVar8 = (ulong)((byte)*param_8 >> 1);
    if (((byte)*param_8 & 1) != 0) {
      uVar8 = *(ulong *)(param_8 + 8);
    }
    if ((uVar8 != 0) && (puVar5 = *param_10, (long)puVar5 - (long)param_9 < 0xa0)) {
      uVar1 = *param_11;
      *param_10 = puVar5 + 1;
      *puVar5 = uVar1;
      return 0;
    }
    return 0;
  }
  if (param_1 == param_7) {
    uVar8 = (ulong)((byte)*param_8 >> 1);
    if (((byte)*param_8 & 1) != 0) {
      uVar8 = *(ulong *)(param_8 + 8);
    }
    if (uVar8 != 0) {
      if (*param_2 == false) {
        return 0xffffffff;
      }
      puVar5 = *param_10;
      if (0x9f < (long)puVar5 - (long)param_9) {
        return 0;
      }
      uVar1 = *param_11;
      *param_10 = puVar5 + 1;
      *puVar5 = uVar1;
      *param_11 = 0;
      return 0;
    }
  }
  pwVar7 = param_12 + 0x20;
  if (*param_12 == param_1) {
    lVar6 = 0;
  }
  else if (param_12[1] == param_1) {
    lVar6 = 1;
  }
  else if (param_12[2] == param_1) {
    lVar6 = 2;
  }
  else if (param_12[3] == param_1) {
    lVar6 = 3;
  }
  else if (param_12[4] == param_1) {
    lVar6 = 4;
  }
  else if (param_12[5] == param_1) {
    lVar6 = 5;
  }
  else if (param_12[6] == param_1) {
    lVar6 = 6;
  }
  else if (param_12[7] == param_1) {
    lVar6 = 7;
  }
  else if (param_12[8] == param_1) {
    lVar6 = 8;
  }
  else if (param_12[9] == param_1) {
    lVar6 = 9;
  }
  else if (param_12[10] == param_1) {
    lVar6 = 10;
  }
  else if (param_12[0xb] == param_1) {
    lVar6 = 0xb;
  }
  else if (param_12[0xc] == param_1) {
    lVar6 = 0xc;
  }
  else if (param_12[0xd] == param_1) {
    lVar6 = 0xd;
  }
  else if (param_12[0xe] == param_1) {
    lVar6 = 0xe;
  }
  else if (param_12[0xf] == param_1) {
    lVar6 = 0xf;
  }
  else if (param_12[0x10] == param_1) {
    lVar6 = 0x10;
  }
  else if (param_12[0x11] == param_1) {
    lVar6 = 0x11;
  }
  else if (param_12[0x12] == param_1) {
    lVar6 = 0x12;
  }
  else if (param_12[0x13] == param_1) {
    lVar6 = 0x13;
  }
  else if (param_12[0x14] == param_1) {
    lVar6 = 0x14;
  }
  else if (param_12[0x15] == param_1) {
    lVar6 = 0x15;
  }
  else if (param_12[0x16] == param_1) {
    lVar6 = 0x16;
  }
  else if (param_12[0x17] == param_1) {
    lVar6 = 0x17;
  }
  else if (param_12[0x18] == param_1) {
    lVar6 = 0x18;
  }
  else if (param_12[0x19] == param_1) {
    lVar6 = 0x19;
  }
  else if (param_12[0x1a] == param_1) {
    lVar6 = 0x1a;
  }
  else if (param_12[0x1b] == param_1) {
    lVar6 = 0x1b;
  }
  else if (param_12[0x1c] == param_1) {
    lVar6 = 0x1c;
  }
  else if (param_12[0x1d] == param_1) {
    lVar6 = 0x1d;
  }
  else if (param_12[0x1e] == param_1) {
    lVar6 = 0x1e;
  }
  else {
    if (param_12[0x1f] != param_1) goto LAB_00e62b3c;
    lVar6 = 0x1f;
  }
  pwVar7 = param_12 + lVar6;
LAB_00e62b3c:
  lVar6 = (long)pwVar7 - (long)param_12;
  if (0x7c < lVar6) {
    return 0xffffffff;
  }
  bVar2 = PTR___src_01ff5698[lVar6 >> 2];
  uVar8 = lVar6 - 0x58U >> 2 | lVar6 << 0x3e;
  if (uVar8 < 2) {
    *param_3 = 'P';
  }
  else {
    if (uVar8 - 2 < 2) {
      pbVar3 = (byte *)*param_5;
      if ((pbVar3 != (byte *)param_4) && ((pbVar3[-1] & 0x5f) != (*param_3 & 0x7fU))) {
        return 0xffffffff;
      }
      *param_5 = (char *)(pbVar3 + 1);
      *pbVar3 = bVar2;
      return 0;
    }
    if (((bVar2 & 0x5f) == *param_3) && (*param_3 = bVar2 & 0x5f | 0x80, *param_2 != false)) {
      *param_2 = false;
      uVar8 = (ulong)((byte)*param_8 >> 1);
      if (((byte)*param_8 & 1) != 0) {
        uVar8 = *(ulong *)(param_8 + 8);
      }
      if ((uVar8 != 0) && (puVar5 = *param_10, (long)puVar5 - (long)param_9 < 0xa0)) {
        uVar1 = *param_11;
        *param_10 = puVar5 + 1;
        *puVar5 = uVar1;
      }
    }
  }
  pbVar3 = (byte *)*param_5;
  *param_5 = (char *)(pbVar3 + 1);
  *pbVar3 = bVar2;
  if (lVar6 < 0x55) {
    *param_11 = *param_11 + 1;
  }
  return 0;
}



// ==========================================================================================
// Function: __stage2_int_prep
// Address: 00e62c4c
// ==========================================================================================

/* std::__ndk1::__num_get<wchar_t>::__stage2_int_prep(std::__ndk1::ios_base&, wchar_t*, wchar_t&) */

void __thiscall
std::__ndk1::__num_get<wchar_t>::__stage2_int_prep
          (__num_get<wchar_t> *this,ios_base *param_1,wchar_t *param_2,wchar_t *param_3)

{
  long lVar1;
  undefined *puVar2;
  undefined *puVar3;
  wchar_t wVar4;
  long *plVar5;
  long local_88;
  undefined *local_80;
  undefined *puStack_78;
  undefined8 local_70;
  undefined ***local_68;
  undefined **local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  ios_base::getloc();
  puVar3 = PTR___init_01ff5688;
  puVar2 = PTR_id_01ff5620;
  local_70 = 0;
  local_80 = PTR_id_01ff5620;
  puStack_78 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e62cc0 to 00e62d13 has its CatchHandler @ 00e62de4 */
    __call_once((ulong *)PTR_id_01ff5620,&local_68,FUN_00e87ff8);
  }
  if (((ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3) <=
       (long)*(int *)(puVar2 + 8) - 1U) ||
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e62dd8 to 00e62ddb has its CatchHandler @ 00e62de4 */
    FUN_00de5da0();
  }
  (**(code **)(*plVar5 + 0x60))(plVar5,PTR___src_01ff5698,PTR___src_01ff5698 + 0x1a,param_1);
  puVar2 = PTR_id_01ff56a0;
  local_70 = 0;
  local_80 = PTR_id_01ff56a0;
  puStack_78 = puVar3;
  if (*(long *)PTR_id_01ff56a0 != -1) {
    local_60 = &local_80;
    local_68 = &local_60;
                    /* try { // try from 00e62d40 to 00e62d9f has its CatchHandler @ 00e62de8 */
    __call_once((ulong *)PTR_id_01ff56a0,&local_68,FUN_00e87ff8);
  }
  if (((long)*(int *)(puVar2 + 8) - 1U <
       (ulong)(*(long *)(local_88 + 0x18) - *(long *)(local_88 + 0x10) >> 3)) &&
     (plVar5 = *(long **)(*(long *)(local_88 + 0x10) + ((long)*(int *)(puVar2 + 8) - 1U) * 8),
     plVar5 != (long *)0x0)) {
    wVar4 = (**(code **)(*plVar5 + 0x20))(plVar5);
    *param_2 = wVar4;
    (**(code **)(*plVar5 + 0x28))(plVar5);
    __shared_count::__release_shared();
    if (*(long *)(lVar1 + 0x28) == local_58) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 00e62ddc to 00e62ddf has its CatchHandler @ 00e62de8 */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __format_int
// Address: 00e63260
// ==========================================================================================

/* std::__ndk1::__num_put_base::__format_int(char*, char const*, bool, unsigned int) */

void std::__ndk1::__num_put_base::__format_int
               (char *param_1,char *param_2,bool param_3,uint param_4)

{
  char *pcVar1;
  char cVar3;
  char *pcVar4;
  char *pcVar2;
  
  if ((param_4 >> 0xb & 1) != 0) {
    *param_1 = '+';
    param_1 = param_1 + 1;
  }
  if ((param_4 >> 9 & 1) == 0) {
    cVar3 = *param_2;
    pcVar1 = param_1;
  }
  else {
    pcVar1 = param_1 + 1;
    *param_1 = '#';
    cVar3 = *param_2;
  }
  if (cVar3 != '\0') {
    pcVar2 = pcVar1;
    pcVar4 = param_2 + 1;
    do {
      pcVar1 = pcVar2 + 1;
      *pcVar2 = cVar3;
      cVar3 = *pcVar4;
      pcVar2 = pcVar1;
      pcVar4 = pcVar4 + 1;
    } while (cVar3 != '\0');
  }
  if ((param_4 & 0x4a) != 0x40) {
    if ((param_4 & 0x4a) == 8) {
      cVar3 = 'x';
      if ((param_4 & 0x4000) != 0) {
        cVar3 = 'X';
      }
      *pcVar1 = cVar3;
      return;
    }
    cVar3 = 'd';
    if (!param_3) {
      cVar3 = 'u';
    }
    *pcVar1 = cVar3;
    return;
  }
  *pcVar1 = 'o';
  return;
}



// ==========================================================================================
// Function: __libcpp_snprintf_l
// Address: 00e632f8
// ==========================================================================================

/* std::__ndk1::__libcpp_snprintf_l(char*, unsigned long, __locale_t*, char const*, ...) */

undefined4
std::__ndk1::__libcpp_snprintf_l(char *param_1,ulong param_2,__locale_t *param_3,char *param_4,...)

{
  long lVar1;
  undefined4 uVar2;
  __locale_t __dataset;
  undefined8 in_x4;
  undefined8 in_x5;
  undefined8 in_x6;
  undefined8 in_x7;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined *puVar3;
  undefined *local_70;
  undefined *puStack_68;
  undefined8 *puStack_60;
  undefined8 uStack_58;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  local_b0 = in_x4;
  uStack_a8 = in_x5;
  local_a0 = in_x6;
  uStack_98 = in_x7;
  puVar3 = (undefined *)register0x00000008;
  __dataset = uselocale((__locale_t)param_3);
  uStack_58 = 0xffffff80ffffffe0;
                    /* try { // try from 00e6337c to 00e63397 has its CatchHandler @ 00e633e0 */
  local_70 = puVar3;
  puStack_68 = &stack0xffffffffffffff70;
  puStack_60 = &local_b0;
  uVar2 = __vsnprintf_chk(param_1,param_2,0,0xffffffffffffffff,param_4,&local_70);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e633a0 to 00e633a7 has its CatchHandler @ 00e633dc */
    uselocale(__dataset);
  }
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return uVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __identify_padding
// Address: 00e633fc
// ==========================================================================================

/* std::__ndk1::__num_put_base::__identify_padding(char*, char*, std::__ndk1::ios_base const&) */

char * std::__ndk1::__num_put_base::__identify_padding
                 (char *param_1,char *param_2,ios_base *param_3)

{
  char cVar1;
  
  if ((*(uint *)(param_3 + 8) & 0xb0) == 0x20) {
    return param_2;
  }
  if ((*(uint *)(param_3 + 8) & 0xb0) == 0x10) {
    cVar1 = *param_1;
    if ((cVar1 == '-') || (cVar1 == '+')) {
      return param_1 + 1;
    }
    if ((1 < (long)param_2 - (long)param_1) &&
       ((cVar1 == '0' && ((byte)(param_1[1] | 0x20U) == 0x78)))) {
      param_1 = param_1 + 2;
    }
  }
  return param_1;
}



// ==========================================================================================
// Function: __widen_and_group_int
// Address: 00e6346c
// ==========================================================================================

/* std::__ndk1::__num_put<char>::__widen_and_group_int(char*, char*, char*, char*, char*&, char*&,
   std::__ndk1::locale const&) */

void std::__ndk1::__num_put<char>::__widen_and_group_int
               (char *param_1,char *param_2,char *param_3,char *param_4,char **param_5,
               char **param_6,locale *param_7)

{
  undefined *puVar1;
  byte bVar2;
  long lVar3;
  undefined *puVar4;
  char cVar5;
  char cVar6;
  long lVar7;
  char *pcVar8;
  char *pcVar9;
  char *pcVar10;
  undefined *puVar11;
  char *pcVar12;
  char *pcVar13;
  uint uVar14;
  long lVar15;
  long *plVar16;
  long *plVar17;
  uint uVar18;
  undefined8 local_90;
  undefined *local_88;
  void *local_80;
  undefined8 **local_78;
  undefined8 *local_70;
  long local_68;
  
  puVar1 = PTR___init_01ff5688;
  puVar11 = PTR_id_01ff5500;
  lVar3 = tpidr_el0;
  local_68 = *(long *)(lVar3 + 0x28);
  lVar15 = *(long *)param_7;
  local_80 = (void *)0x0;
  local_90 = PTR_id_01ff5500;
  local_88 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    __call_once((ulong *)PTR_id_01ff5500,&local_78,FUN_00e87ff8);
  }
  puVar4 = PTR_id_01ff5690;
  lVar7 = *(long *)(lVar15 + 0x10);
  if (((long)*(int *)(puVar11 + 8) - 1U < (ulong)(*(long *)(lVar15 + 0x18) - lVar7 >> 3)) &&
     (plVar16 = *(long **)(lVar7 + ((long)*(int *)(puVar11 + 8) - 1U) * 8), plVar16 != (long *)0x0))
  {
    lVar15 = *(long *)param_7;
    local_80 = (void *)0x0;
    local_90 = PTR_id_01ff5690;
    local_88 = puVar1;
    if (*(long *)PTR_id_01ff5690 != -1) {
      local_70 = &local_90;
      local_78 = &local_70;
      __call_once((ulong *)PTR_id_01ff5690,&local_78,FUN_00e87ff8);
    }
    lVar7 = *(long *)(lVar15 + 0x10);
    if (((long)*(int *)(puVar4 + 8) - 1U < (ulong)(*(long *)(lVar15 + 0x18) - lVar7 >> 3)) &&
       (plVar17 = *(long **)(lVar7 + ((long)*(int *)(puVar4 + 8) - 1U) * 8), plVar17 != (long *)0x0)
       ) {
      (**(code **)(*plVar17 + 0x28))(&local_90,plVar17);
      puVar11 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
      if (((ulong)local_90 & 1) != 0) {
        puVar11 = local_88;
      }
      if (puVar11 == (undefined *)0x0) {
                    /* try { // try from 00e637c0 to 00e637d3 has its CatchHandler @ 00e6384c */
        (**(code **)(*plVar16 + 0x40))(plVar16,param_1,param_3,param_4);
        pcVar8 = param_4 + ((long)param_3 - (long)param_1);
        *param_6 = pcVar8;
      }
      else {
        *param_6 = param_4;
        if ((*param_1 == '-') || (pcVar12 = param_1, *param_1 == '+')) {
                    /* try { // try from 00e635d8 to 00e63653 has its CatchHandler @ 00e63854 */
          cVar5 = (**(code **)(*plVar16 + 0x38))(plVar16);
          pcVar8 = *param_6;
          pcVar12 = param_1 + 1;
          *param_6 = pcVar8 + 1;
          *pcVar8 = cVar5;
        }
        if (((1 < (long)param_3 - (long)pcVar12) && (*pcVar12 == '0')) &&
           ((byte)(pcVar12[1] | 0x20U) == 0x78)) {
          cVar5 = (**(code **)(*plVar16 + 0x38))(plVar16,0x30);
          pcVar8 = *param_6;
          *param_6 = pcVar8 + 1;
          *pcVar8 = cVar5;
          cVar5 = (**(code **)(*plVar16 + 0x38))(plVar16,pcVar12[1]);
          pcVar8 = *param_6;
          pcVar12 = pcVar12 + 2;
          *param_6 = pcVar8 + 1;
          *pcVar8 = cVar5;
        }
        if ((pcVar12 != param_3) && (pcVar9 = param_3 + -1, pcVar8 = pcVar12, pcVar12 < pcVar9)) {
          do {
            pcVar13 = pcVar8 + 1;
            cVar5 = *pcVar8;
            *pcVar8 = *pcVar9;
            pcVar10 = pcVar9 + -1;
            *pcVar9 = cVar5;
            pcVar9 = pcVar10;
            pcVar8 = pcVar13;
          } while (pcVar13 < pcVar10);
        }
                    /* try { // try from 00e636a8 to 00e636af has its CatchHandler @ 00e63850 */
        cVar5 = (**(code **)(*plVar17 + 0x20))(plVar17);
        if (pcVar12 < param_3) {
          uVar14 = 0;
          uVar18 = 0;
          pcVar8 = pcVar12;
          do {
            puVar11 = (undefined *)(ulong)uVar14;
            if (((ulong)local_90 & 1) == 0) {
              bVar2 = puVar11[(long)&local_90 + 1];
            }
            else {
              bVar2 = *(byte *)((long)local_80 + (long)puVar11);
            }
            if ((bVar2 != 0) && (uVar18 == bVar2)) {
              pcVar9 = *param_6;
              uVar18 = 0;
              *param_6 = pcVar9 + 1;
              *pcVar9 = cVar5;
              puVar1 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
              if (((ulong)local_90 & 1) != 0) {
                puVar1 = local_88;
              }
              if (puVar11 < puVar1 + -1) {
                uVar14 = uVar14 + 1;
              }
            }
                    /* try { // try from 00e6373c to 00e63743 has its CatchHandler @ 00e63858 */
            cVar6 = (**(code **)(*plVar16 + 0x38))(plVar16,*pcVar8);
            pcVar9 = *param_6;
            pcVar8 = pcVar8 + 1;
            uVar18 = uVar18 + 1;
            *param_6 = pcVar9 + 1;
            *pcVar9 = cVar6;
          } while (param_3 != pcVar8);
        }
        pcVar8 = *param_6;
        if ((param_4 + ((long)pcVar12 - (long)param_1) != pcVar8) &&
           (param_4 + ((long)pcVar12 - (long)param_1) < pcVar8 + -1)) {
          pcVar9 = pcVar8 + -1;
          pcVar8 = param_4 + ((long)pcVar12 - (long)param_1);
          do {
            pcVar10 = pcVar8 + 1;
            cVar5 = *pcVar8;
            *pcVar8 = *pcVar9;
            pcVar12 = pcVar9 + -1;
            *pcVar9 = cVar5;
            pcVar9 = pcVar12;
            pcVar8 = pcVar10;
          } while (pcVar10 < pcVar12);
          pcVar8 = *param_6;
        }
      }
      if (param_2 != param_3) {
        pcVar8 = param_4 + ((long)param_2 - (long)param_1);
      }
      *param_5 = pcVar8;
      if (((ulong)local_90 & 1) != 0) {
        operator_delete(local_80);
      }
      if (*(long *)(lVar3 + 0x28) == local_68) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __format_float
// Address: 00e64460
// ==========================================================================================

/* std::__ndk1::__num_put_base::__format_float(char*, char const*, unsigned int) */

bool std::__ndk1::__num_put_base::__format_float(char *param_1,char *param_2,uint param_3)

{
  uint uVar1;
  bool bVar2;
  undefined2 *puVar3;
  undefined2 *puVar4;
  char cVar5;
  undefined uVar6;
  undefined uVar7;
  char *pcVar8;
  
  puVar3 = (undefined2 *)param_1;
  if ((param_3 >> 0xb & 1) != 0) {
    puVar3 = (undefined2 *)(param_1 + 1);
    *param_1 = '+';
  }
  puVar4 = puVar3;
  if ((param_3 >> 10 & 1) != 0) {
    puVar4 = (undefined2 *)((long)puVar3 + 1);
    *(undefined *)puVar3 = 0x23;
  }
  uVar1 = param_3 & 0x104;
  puVar3 = puVar4;
  if (uVar1 != 0x104) {
    puVar3 = puVar4 + 1;
    *puVar4 = 0x2a2e;
  }
  cVar5 = *param_2;
  if (cVar5 != '\0') {
    puVar4 = puVar3;
    pcVar8 = param_2 + 1;
    do {
      puVar3 = (undefined2 *)((long)puVar4 + 1);
      *(char *)puVar4 = cVar5;
      cVar5 = *pcVar8;
      puVar4 = puVar3;
      pcVar8 = pcVar8 + 1;
    } while (cVar5 != '\0');
  }
  if (uVar1 == 0x100) {
    bVar2 = (param_3 & 0x4000) == 0;
    uVar6 = 0x45;
    uVar7 = 0x65;
  }
  else if (uVar1 == 4) {
    bVar2 = (param_3 & 0x4000) == 0;
    uVar6 = 0x46;
    uVar7 = 0x66;
  }
  else if (uVar1 == 0x104) {
    bVar2 = (param_3 & 0x4000) == 0;
    uVar6 = 0x41;
    uVar7 = 0x61;
  }
  else {
    bVar2 = (param_3 & 0x4000) == 0;
    uVar6 = 0x47;
    uVar7 = 0x67;
  }
  if (!bVar2) {
    uVar7 = uVar6;
  }
  *(undefined *)puVar3 = uVar7;
  return uVar1 != 0x104;
}



// ==========================================================================================
// Function: __libcpp_asprintf_l
// Address: 00e64518
// ==========================================================================================

/* std::__ndk1::__libcpp_asprintf_l(char**, __locale_t*, char const*, ...) */

int std::__ndk1::__libcpp_asprintf_l(char **param_1,__locale_t *param_2,char *param_3,...)

{
  long lVar1;
  int iVar2;
  __locale_t __dataset;
  undefined8 in_x3;
  undefined8 in_x4;
  undefined8 in_x5;
  undefined8 in_x6;
  undefined8 in_x7;
  long lVar3;
  undefined auStack_c0 [8];
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined *local_90;
  undefined **ppuStack_88;
  undefined *puStack_80;
  undefined8 uStack_78;
  
  lVar1 = tpidr_el0;
  lVar3 = *(long *)(lVar1 + 0x28);
  local_b8 = in_x3;
  uStack_b0 = in_x4;
  local_a8 = in_x5;
  uStack_a0 = in_x6;
  local_98 = in_x7;
  local_90 = (undefined *)register0x00000008;
  __dataset = uselocale((__locale_t)param_2);
  uStack_78 = 0xffffff80ffffffd8;
                    /* try { // try from 00e645a0 to 00e645af has its CatchHandler @ 00e645f8 */
  ppuStack_88 = &local_90;
  puStack_80 = auStack_c0;
  iVar2 = vasprintf(param_1,param_3,&local_90);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e645b8 to 00e645bf has its CatchHandler @ 00e645f4 */
    uselocale(__dataset);
  }
  if (*(long *)(lVar1 + 0x28) == lVar3) {
    return iVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __widen_and_group_float
// Address: 00e64614
// ==========================================================================================

/* std::__ndk1::__num_put<char>::__widen_and_group_float(char*, char*, char*, char*, char*&, char*&,
   std::__ndk1::locale const&) */

void std::__ndk1::__num_put<char>::__widen_and_group_float
               (char *param_1,char *param_2,char *param_3,char *param_4,char **param_5,
               char **param_6,locale *param_7)

{
  undefined *puVar1;
  byte bVar2;
  long lVar3;
  char *pcVar4;
  undefined *puVar5;
  char cVar6;
  char cVar7;
  int iVar8;
  long lVar9;
  char *pcVar10;
  byte *pbVar11;
  byte *pbVar12;
  undefined *puVar13;
  char *pcVar14;
  byte *pbVar15;
  char *pcVar16;
  uint uVar17;
  long *plVar18;
  uint uVar19;
  long lVar20;
  long *plVar21;
  byte *pbVar22;
  byte *pbVar23;
  byte *pbVar24;
  undefined8 local_90;
  undefined *local_88;
  void *local_80;
  undefined8 **local_78;
  undefined8 *local_70;
  long local_68;
  
  puVar1 = PTR___init_01ff5688;
  puVar13 = PTR_id_01ff5500;
  lVar3 = tpidr_el0;
  local_68 = *(long *)(lVar3 + 0x28);
  lVar20 = *(long *)param_7;
  local_80 = (void *)0x0;
  local_90 = PTR_id_01ff5500;
  local_88 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5500 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    __call_once((ulong *)PTR_id_01ff5500,&local_78,FUN_00e87ff8);
  }
  puVar5 = PTR_id_01ff5690;
  lVar9 = *(long *)(lVar20 + 0x10);
  if (((long)*(int *)(puVar13 + 8) - 1U < (ulong)(*(long *)(lVar20 + 0x18) - lVar9 >> 3)) &&
     (plVar21 = *(long **)(lVar9 + ((long)*(int *)(puVar13 + 8) - 1U) * 8), plVar21 != (long *)0x0))
  {
    lVar20 = *(long *)param_7;
    local_80 = (void *)0x0;
    local_90 = PTR_id_01ff5690;
    local_88 = puVar1;
    if (*(long *)PTR_id_01ff5690 != -1) {
      local_70 = &local_90;
      local_78 = &local_70;
      __call_once((ulong *)PTR_id_01ff5690,&local_78,FUN_00e87ff8);
    }
    lVar9 = *(long *)(lVar20 + 0x10);
    if (((long)*(int *)(puVar5 + 8) - 1U < (ulong)(*(long *)(lVar20 + 0x18) - lVar9 >> 3)) &&
       (plVar18 = *(long **)(lVar9 + ((long)*(int *)(puVar5 + 8) - 1U) * 8), plVar18 != (long *)0x0)
       ) {
      (**(code **)(*plVar18 + 0x28))(&local_90,plVar18);
      *param_6 = param_4;
      if ((*param_1 == '-') || (pbVar22 = (byte *)param_1, *param_1 == '+')) {
                    /* try { // try from 00e64774 to 00e6477b has its CatchHandler @ 00e64bc8 */
        cVar6 = (**(code **)(*plVar21 + 0x38))(plVar21);
        pcVar10 = *param_6;
        pbVar22 = (byte *)(param_1 + 1);
        *param_6 = pcVar10 + 1;
        *pcVar10 = cVar6;
      }
      if ((((long)param_3 - (long)pbVar22 < 2) || (*pbVar22 != 0x30)) ||
         ((pbVar22[1] | 0x20) != 0x78)) {
        pbVar23 = pbVar22;
        pbVar24 = pbVar22;
        if (pbVar22 < param_3) {
          do {
            bVar2 = *pbVar23;
            if (((DAT_0231cfb0 & 1) == 0) &&
               (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e648d4 to 00e648e7 has its CatchHandler @ 00e64bb0 */
              DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
              __cxa_guard_release(&DAT_0231cfb0);
            }
                    /* try { // try from 00e648ac to 00e648b3 has its CatchHandler @ 00e64bd4 */
            iVar8 = isdigit_l((uint)bVar2,DAT_0231cfa8);
            pbVar24 = pbVar23;
          } while ((iVar8 != 0) &&
                  (pbVar23 = pbVar23 + 1, pbVar24 = (byte *)param_3, (byte *)param_3 != pbVar23));
        }
      }
      else {
                    /* try { // try from 00e647c8 to 00e647f7 has its CatchHandler @ 00e64bd0 */
        cVar6 = (**(code **)(*plVar21 + 0x38))(plVar21,0x30);
        pcVar10 = *param_6;
        *param_6 = pcVar10 + 1;
        *pcVar10 = cVar6;
        cVar6 = (**(code **)(*plVar21 + 0x38))(plVar21,pbVar22[1]);
        pcVar10 = *param_6;
        pbVar22 = pbVar22 + 2;
        *param_6 = pcVar10 + 1;
        *pcVar10 = cVar6;
        pbVar23 = pbVar22;
        pbVar24 = pbVar22;
        if (pbVar22 < param_3) {
          do {
            bVar2 = *pbVar23;
            if (((DAT_0231cfb0 & 1) == 0) &&
               (iVar8 = __cxa_guard_acquire(&DAT_0231cfb0), iVar8 != 0)) {
                    /* try { // try from 00e6485c to 00e6486f has its CatchHandler @ 00e64bac */
              DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
              __cxa_guard_release(&DAT_0231cfb0);
            }
                    /* try { // try from 00e64834 to 00e6483b has its CatchHandler @ 00e64bcc */
            iVar8 = isxdigit_l((uint)bVar2,DAT_0231cfa8);
            pbVar24 = pbVar23;
          } while ((iVar8 != 0) &&
                  (pbVar23 = pbVar23 + 1, pbVar24 = (byte *)param_3, (byte *)param_3 != pbVar23));
        }
      }
      puVar13 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
      if (((ulong)local_90 & 1) != 0) {
        puVar13 = local_88;
      }
      if (puVar13 == (undefined *)0x0) {
                    /* try { // try from 00e64a88 to 00e64a97 has its CatchHandler @ 00e64bd0 */
        (**(code **)(*plVar21 + 0x40))(plVar21,pbVar22,pbVar24,*param_6);
        *param_6 = *param_6 + ((long)pbVar24 - (long)pbVar22);
      }
      else {
        if ((pbVar22 != pbVar24) && (pbVar11 = pbVar24 + -1, pbVar23 = pbVar22, pbVar22 < pbVar11))
        {
          do {
            pbVar15 = pbVar23 + 1;
            bVar2 = *pbVar23;
            *pbVar23 = *pbVar11;
            pbVar12 = pbVar11 + -1;
            *pbVar11 = bVar2;
            pbVar11 = pbVar12;
            pbVar23 = pbVar15;
          } while (pbVar15 < pbVar12);
        }
                    /* try { // try from 00e64968 to 00e6496f has its CatchHandler @ 00e64bc4 */
        cVar6 = (**(code **)(*plVar18 + 0x20))(plVar18);
        if (pbVar22 < pbVar24) {
          uVar19 = 0;
          uVar17 = 0;
          pbVar23 = pbVar22;
          do {
            puVar13 = (undefined *)(ulong)uVar19;
            if (((ulong)local_90 & 1) == 0) {
              bVar2 = puVar13[(long)&local_90 + 1];
            }
            else {
              bVar2 = *(byte *)((long)local_80 + (long)puVar13);
            }
            if ((bVar2 != 0) && (uVar17 == bVar2)) {
              pcVar10 = *param_6;
              uVar17 = 0;
              *param_6 = pcVar10 + 1;
              *pcVar10 = cVar6;
              puVar1 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
              if (((ulong)local_90 & 1) != 0) {
                puVar1 = local_88;
              }
              if (puVar13 < puVar1 + -1) {
                uVar19 = uVar19 + 1;
              }
            }
                    /* try { // try from 00e649fc to 00e64a03 has its CatchHandler @ 00e64bdc */
            cVar7 = (**(code **)(*plVar21 + 0x38))(plVar21,*pbVar23);
            pcVar10 = *param_6;
            pbVar23 = pbVar23 + 1;
            uVar17 = uVar17 + 1;
            *param_6 = pcVar10 + 1;
            *pcVar10 = cVar7;
          } while (pbVar24 != pbVar23);
        }
        if ((param_4 + ((long)pbVar22 - (long)param_1) != *param_6) &&
           (pcVar10 = *param_6 + -1, param_4 + ((long)pbVar22 - (long)param_1) < pcVar10)) {
          pcVar4 = param_4 + ((long)pbVar22 - (long)param_1);
          do {
            pcVar16 = pcVar4 + 1;
            cVar6 = *pcVar4;
            *pcVar4 = *pcVar10;
            pcVar14 = pcVar10 + -1;
            *pcVar10 = cVar6;
            pcVar10 = pcVar14;
            pcVar4 = pcVar16;
          } while (pcVar16 < pcVar14);
        }
      }
      pbVar22 = pbVar24;
      if (pbVar24 < param_3) {
        do {
          if (*pbVar24 == 0x2e) {
                    /* try { // try from 00e64afc to 00e64b33 has its CatchHandler @ 00e64bd0 */
            cVar6 = (**(code **)(*plVar18 + 0x18))(plVar18);
            pcVar10 = *param_6;
            *param_6 = pcVar10 + 1;
            *pcVar10 = cVar6;
            pbVar22 = pbVar24 + 1;
            break;
          }
                    /* try { // try from 00e64ac8 to 00e64acf has its CatchHandler @ 00e64bd8 */
          cVar6 = (**(code **)(*plVar21 + 0x38))(plVar21);
          pcVar10 = *param_6;
          pbVar24 = pbVar24 + 1;
          *param_6 = pcVar10 + 1;
          *pcVar10 = cVar6;
          pbVar22 = (byte *)param_3;
        } while ((byte *)param_3 != pbVar24);
      }
      (**(code **)(*plVar21 + 0x40))(plVar21,pbVar22,param_3,*param_6);
      pcVar10 = *param_6;
      *param_6 = pcVar10 + ((long)param_3 - (long)pbVar22);
      pcVar10 = pcVar10 + ((long)param_3 - (long)pbVar22);
      if (param_2 != param_3) {
        pcVar10 = param_4 + ((long)param_2 - (long)param_1);
      }
      *param_5 = pcVar10;
      if (((ulong)local_90 & 1) != 0) {
        operator_delete(local_80);
      }
      if (*(long *)(lVar3 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __widen_and_group_int
// Address: 00e6573c
// ==========================================================================================

/* std::__ndk1::__num_put<wchar_t>::__widen_and_group_int(char*, char*, char*, wchar_t*, wchar_t*&,
   wchar_t*&, std::__ndk1::locale const&) */

void std::__ndk1::__num_put<wchar_t>::__widen_and_group_int
               (char *param_1,char *param_2,char *param_3,wchar_t *param_4,wchar_t **param_5,
               wchar_t **param_6,locale *param_7)

{
  undefined *puVar1;
  byte bVar2;
  char cVar3;
  long lVar4;
  undefined *puVar5;
  wchar_t wVar6;
  wchar_t wVar7;
  long lVar8;
  wchar_t *pwVar9;
  char *pcVar10;
  char *pcVar11;
  undefined *puVar12;
  wchar_t *pwVar13;
  char *pcVar14;
  wchar_t *pwVar15;
  wchar_t *pwVar16;
  uint uVar17;
  long lVar18;
  char *pcVar19;
  long *plVar20;
  long *plVar21;
  uint uVar22;
  char *pcVar23;
  undefined8 local_90;
  undefined *local_88;
  void *local_80;
  undefined8 **local_78;
  undefined8 *local_70;
  long local_68;
  
  puVar1 = PTR___init_01ff5688;
  puVar12 = PTR_id_01ff5620;
  lVar4 = tpidr_el0;
  local_68 = *(long *)(lVar4 + 0x28);
  lVar18 = *(long *)param_7;
  local_80 = (void *)0x0;
  local_90 = PTR_id_01ff5620;
  local_88 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    __call_once((ulong *)PTR_id_01ff5620,&local_78,FUN_00e87ff8);
  }
  puVar5 = PTR_id_01ff56a0;
  lVar8 = *(long *)(lVar18 + 0x10);
  if (((long)*(int *)(puVar12 + 8) - 1U < (ulong)(*(long *)(lVar18 + 0x18) - lVar8 >> 3)) &&
     (plVar20 = *(long **)(lVar8 + ((long)*(int *)(puVar12 + 8) - 1U) * 8), plVar20 != (long *)0x0))
  {
    lVar18 = *(long *)param_7;
    local_80 = (void *)0x0;
    local_90 = PTR_id_01ff56a0;
    local_88 = puVar1;
    if (*(long *)PTR_id_01ff56a0 != -1) {
      local_70 = &local_90;
      local_78 = &local_70;
      __call_once((ulong *)PTR_id_01ff56a0,&local_78,FUN_00e87ff8);
    }
    lVar8 = *(long *)(lVar18 + 0x10);
    if (((long)*(int *)(puVar5 + 8) - 1U < (ulong)(*(long *)(lVar18 + 0x18) - lVar8 >> 3)) &&
       (plVar21 = *(long **)(lVar8 + ((long)*(int *)(puVar5 + 8) - 1U) * 8), plVar21 != (long *)0x0)
       ) {
      (**(code **)(*plVar21 + 0x28))(&local_90,plVar21);
      puVar12 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
      if (((ulong)local_90 & 1) != 0) {
        puVar12 = local_88;
      }
      if (puVar12 == (undefined *)0x0) {
                    /* try { // try from 00e65a48 to 00e65a5b has its CatchHandler @ 00e65b18 */
        (**(code **)(*plVar20 + 0x60))(plVar20,param_1,param_3,param_4);
        *param_6 = param_4 + ((long)param_3 - (long)param_1);
      }
      else {
        *param_6 = param_4;
        if ((*param_1 == '-') || (pcVar19 = param_1, *param_1 == '+')) {
                    /* try { // try from 00e658a8 to 00e65923 has its CatchHandler @ 00e65b20 */
          wVar6 = (**(code **)(*plVar20 + 0x58))(plVar20);
          pwVar9 = *param_6;
          pcVar19 = param_1 + 1;
          *param_6 = pwVar9 + 1;
          *pwVar9 = wVar6;
        }
        if (((1 < (long)param_3 - (long)pcVar19) && (*pcVar19 == '0')) &&
           ((byte)(pcVar19[1] | 0x20U) == 0x78)) {
          wVar6 = (**(code **)(*plVar20 + 0x58))(plVar20,0x30);
          pwVar9 = *param_6;
          *param_6 = pwVar9 + 1;
          *pwVar9 = wVar6;
          wVar6 = (**(code **)(*plVar20 + 0x58))(plVar20,pcVar19[1]);
          pwVar9 = *param_6;
          pcVar19 = pcVar19 + 2;
          *param_6 = pwVar9 + 1;
          *pwVar9 = wVar6;
        }
        if ((pcVar19 != param_3) && (pcVar10 = param_3 + -1, pcVar23 = pcVar19, pcVar19 < pcVar10))
        {
          do {
            pcVar14 = pcVar23 + 1;
            cVar3 = *pcVar23;
            *pcVar23 = *pcVar10;
            pcVar11 = pcVar10 + -1;
            *pcVar10 = cVar3;
            pcVar10 = pcVar11;
            pcVar23 = pcVar14;
          } while (pcVar14 < pcVar11);
        }
                    /* try { // try from 00e65974 to 00e6597b has its CatchHandler @ 00e65b1c */
        wVar6 = (**(code **)(*plVar21 + 0x20))(plVar21);
        if (pcVar19 < param_3) {
          uVar17 = 0;
          uVar22 = 0;
          pcVar23 = pcVar19;
          do {
            puVar12 = (undefined *)(ulong)uVar17;
            if (((ulong)local_90 & 1) == 0) {
              bVar2 = puVar12[(long)&local_90 + 1];
            }
            else {
              bVar2 = *(byte *)((long)local_80 + (long)puVar12);
            }
            if ((bVar2 != 0) && (uVar22 == bVar2)) {
              pwVar9 = *param_6;
              uVar22 = 0;
              *param_6 = pwVar9 + 1;
              *pwVar9 = wVar6;
              puVar1 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
              if (((ulong)local_90 & 1) != 0) {
                puVar1 = local_88;
              }
              if (puVar12 < puVar1 + -1) {
                uVar17 = uVar17 + 1;
              }
            }
                    /* try { // try from 00e65a0c to 00e65a13 has its CatchHandler @ 00e65b24 */
            wVar7 = (**(code **)(*plVar20 + 0x58))(plVar20,*pcVar23);
            pwVar15 = *param_6;
            pcVar23 = pcVar23 + 1;
            uVar22 = uVar22 + 1;
            pwVar9 = pwVar15 + 1;
            *param_6 = pwVar9;
            *pwVar15 = wVar7;
          } while (param_3 != pcVar23);
        }
        else {
          pwVar9 = *param_6;
        }
        if ((param_4 + ((long)pcVar19 - (long)param_1) != pwVar9) &&
           (param_4 + ((long)pcVar19 - (long)param_1) < pwVar9 + -1)) {
          pwVar15 = pwVar9 + -1;
          pwVar9 = param_4 + ((long)pcVar19 - (long)param_1);
          do {
            pwVar16 = pwVar9 + 1;
            wVar6 = *pwVar9;
            *pwVar9 = *pwVar15;
            pwVar13 = pwVar15 + -1;
            *pwVar15 = wVar6;
            pwVar15 = pwVar13;
            pwVar9 = pwVar16;
          } while (pwVar16 < pwVar13);
        }
      }
      pwVar9 = *param_6;
      if (param_2 != param_3) {
        pwVar9 = param_4 + ((long)param_2 - (long)param_1);
      }
      *param_5 = pwVar9;
      if (((ulong)local_90 & 1) != 0) {
        operator_delete(local_80);
      }
      if (*(long *)(lVar4 + 0x28) == local_68) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __widen_and_group_float
// Address: 00e66918
// ==========================================================================================

/* std::__ndk1::__num_put<wchar_t>::__widen_and_group_float(char*, char*, char*, wchar_t*,
   wchar_t*&, wchar_t*&, std::__ndk1::locale const&) */

void std::__ndk1::__num_put<wchar_t>::__widen_and_group_float
               (char *param_1,char *param_2,char *param_3,wchar_t *param_4,wchar_t **param_5,
               wchar_t **param_6,locale *param_7)

{
  undefined *puVar1;
  byte bVar2;
  long lVar3;
  undefined *puVar4;
  wchar_t wVar5;
  int iVar6;
  wchar_t wVar7;
  long lVar8;
  wchar_t *pwVar9;
  byte *pbVar10;
  byte *pbVar11;
  undefined *puVar12;
  wchar_t *pwVar13;
  wchar_t *pwVar14;
  byte *pbVar15;
  wchar_t *pwVar16;
  uint uVar17;
  uint uVar18;
  long lVar19;
  long *plVar20;
  long *plVar21;
  byte *pbVar22;
  byte *pbVar23;
  byte *pbVar24;
  undefined8 local_90;
  undefined *local_88;
  void *local_80;
  undefined8 **local_78;
  undefined8 *local_70;
  long local_68;
  
  puVar1 = PTR___init_01ff5688;
  puVar12 = PTR_id_01ff5620;
  lVar3 = tpidr_el0;
  local_68 = *(long *)(lVar3 + 0x28);
  lVar19 = *(long *)param_7;
  local_80 = (void *)0x0;
  local_90 = PTR_id_01ff5620;
  local_88 = PTR___init_01ff5688;
  if (*(long *)PTR_id_01ff5620 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    __call_once((ulong *)PTR_id_01ff5620,&local_78,FUN_00e87ff8);
  }
  puVar4 = PTR_id_01ff56a0;
  lVar8 = *(long *)(lVar19 + 0x10);
  if (((long)*(int *)(puVar12 + 8) - 1U < (ulong)(*(long *)(lVar19 + 0x18) - lVar8 >> 3)) &&
     (plVar21 = *(long **)(lVar8 + ((long)*(int *)(puVar12 + 8) - 1U) * 8), plVar21 != (long *)0x0))
  {
    lVar19 = *(long *)param_7;
    local_80 = (void *)0x0;
    local_90 = PTR_id_01ff56a0;
    local_88 = puVar1;
    if (*(long *)PTR_id_01ff56a0 != -1) {
      local_70 = &local_90;
      local_78 = &local_70;
      __call_once((ulong *)PTR_id_01ff56a0,&local_78,FUN_00e87ff8);
    }
    lVar8 = *(long *)(lVar19 + 0x10);
    if (((long)*(int *)(puVar4 + 8) - 1U < (ulong)(*(long *)(lVar19 + 0x18) - lVar8 >> 3)) &&
       (plVar20 = *(long **)(lVar8 + ((long)*(int *)(puVar4 + 8) - 1U) * 8), plVar20 != (long *)0x0)
       ) {
      (**(code **)(*plVar20 + 0x28))(&local_90,plVar20);
      *param_6 = param_4;
      if ((*param_1 == '-') || (pbVar22 = (byte *)param_1, *param_1 == '+')) {
                    /* try { // try from 00e66a78 to 00e66a7f has its CatchHandler @ 00e66ed4 */
        wVar5 = (**(code **)(*plVar21 + 0x58))(plVar21);
        pwVar9 = *param_6;
        pbVar22 = (byte *)(param_1 + 1);
        *param_6 = pwVar9 + 1;
        *pwVar9 = wVar5;
      }
      if ((((long)param_3 - (long)pbVar22 < 2) || (*pbVar22 != 0x30)) ||
         ((pbVar22[1] | 0x20) != 0x78)) {
        pbVar24 = pbVar22;
        pbVar23 = pbVar22;
        if (pbVar22 < param_3) {
          do {
            bVar2 = *pbVar23;
            if (((DAT_0231cfb0 & 1) == 0) &&
               (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0), iVar6 != 0)) {
                    /* try { // try from 00e66bdc to 00e66bef has its CatchHandler @ 00e66ebc */
              DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
              __cxa_guard_release(&DAT_0231cfb0);
            }
                    /* try { // try from 00e66bb4 to 00e66bbb has its CatchHandler @ 00e66ee0 */
            iVar6 = isdigit_l((uint)bVar2,DAT_0231cfa8);
            pbVar24 = pbVar23;
          } while ((iVar6 != 0) &&
                  (pbVar23 = pbVar23 + 1, pbVar24 = (byte *)param_3, (byte *)param_3 != pbVar23));
        }
      }
      else {
                    /* try { // try from 00e66ac8 to 00e66af7 has its CatchHandler @ 00e66edc */
        wVar5 = (**(code **)(*plVar21 + 0x58))(plVar21,0x30);
        pwVar9 = *param_6;
        *param_6 = pwVar9 + 1;
        *pwVar9 = wVar5;
        wVar5 = (**(code **)(*plVar21 + 0x58))(plVar21,pbVar22[1]);
        pwVar9 = *param_6;
        pbVar22 = pbVar22 + 2;
        *param_6 = pwVar9 + 1;
        *pwVar9 = wVar5;
        pbVar24 = pbVar22;
        pbVar23 = pbVar22;
        if (pbVar22 < param_3) {
          do {
            bVar2 = *pbVar23;
            if (((DAT_0231cfb0 & 1) == 0) &&
               (iVar6 = __cxa_guard_acquire(&DAT_0231cfb0), iVar6 != 0)) {
                    /* try { // try from 00e66b68 to 00e66b77 has its CatchHandler @ 00e66eb8 */
              DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
              __cxa_guard_release(&DAT_0231cfb0);
            }
                    /* try { // try from 00e66b40 to 00e66b47 has its CatchHandler @ 00e66ed8 */
            iVar6 = isxdigit_l((uint)bVar2,DAT_0231cfa8);
            pbVar24 = pbVar23;
          } while ((iVar6 != 0) &&
                  (pbVar23 = pbVar23 + 1, pbVar24 = (byte *)param_3, (byte *)param_3 != pbVar23));
        }
      }
      puVar12 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
      if (((ulong)local_90 & 1) != 0) {
        puVar12 = local_88;
      }
      if (puVar12 == (undefined *)0x0) {
                    /* try { // try from 00e66d3c to 00e66d4b has its CatchHandler @ 00e66edc */
        (**(code **)(*plVar21 + 0x60))(plVar21,pbVar22,pbVar24,*param_6);
        *param_6 = *param_6 + ((long)pbVar24 - (long)pbVar22);
      }
      else {
        if ((pbVar22 != pbVar24) && (pbVar10 = pbVar24 + -1, pbVar23 = pbVar22, pbVar22 < pbVar10))
        {
          do {
            pbVar15 = pbVar23 + 1;
            bVar2 = *pbVar23;
            *pbVar23 = *pbVar10;
            pbVar11 = pbVar10 + -1;
            *pbVar10 = bVar2;
            pbVar10 = pbVar11;
            pbVar23 = pbVar15;
          } while (pbVar15 < pbVar11);
        }
                    /* try { // try from 00e66c68 to 00e66c73 has its CatchHandler @ 00e66ed0 */
        wVar5 = (**(code **)(*plVar20 + 0x20))(plVar20);
        if (pbVar22 < pbVar24) {
          uVar18 = 0;
          uVar17 = 0;
          pbVar23 = pbVar22;
          do {
            puVar12 = (undefined *)(ulong)uVar18;
            if (((ulong)local_90 & 1) == 0) {
              bVar2 = puVar12[(long)&local_90 + 1];
            }
            else {
              bVar2 = *(byte *)((long)local_80 + (long)puVar12);
            }
            if ((bVar2 != 0) && (uVar17 == bVar2)) {
              pwVar9 = *param_6;
              uVar17 = 0;
              *param_6 = pwVar9 + 1;
              *pwVar9 = wVar5;
              puVar1 = (undefined *)((ulong)local_90 >> 1 & 0x7f);
              if (((ulong)local_90 & 1) != 0) {
                puVar1 = local_88;
              }
              if (puVar12 < puVar1 + -1) {
                uVar18 = uVar18 + 1;
              }
            }
                    /* try { // try from 00e66d00 to 00e66d07 has its CatchHandler @ 00e66ee8 */
            wVar7 = (**(code **)(*plVar21 + 0x58))(plVar21,*pbVar23);
            pwVar13 = *param_6;
            pbVar23 = pbVar23 + 1;
            uVar17 = uVar17 + 1;
            pwVar9 = pwVar13 + 1;
            *param_6 = pwVar9;
            *pwVar13 = wVar7;
          } while (pbVar24 != pbVar23);
        }
        else {
          pwVar9 = *param_6;
        }
        if ((param_4 + ((long)pbVar22 - (long)param_1) != pwVar9) &&
           (param_4 + ((long)pbVar22 - (long)param_1) < pwVar9 + -1)) {
          pwVar13 = pwVar9 + -1;
          pwVar9 = param_4 + ((long)pbVar22 - (long)param_1);
          do {
            pwVar16 = pwVar9 + 1;
            wVar5 = *pwVar9;
            *pwVar9 = *pwVar13;
            pwVar14 = pwVar13 + -1;
            *pwVar13 = wVar5;
            pwVar13 = pwVar14;
            pwVar9 = pwVar16;
          } while (pwVar16 < pwVar14);
        }
      }
      pbVar22 = pbVar24;
      if (pbVar24 < param_3) {
        do {
          if (*pbVar24 == 0x2e) {
                    /* try { // try from 00e66df8 to 00e66e2b has its CatchHandler @ 00e66edc */
            wVar5 = (**(code **)(*plVar20 + 0x18))(plVar20);
            pwVar9 = *param_6;
            *param_6 = pwVar9 + 1;
            *pwVar9 = wVar5;
            pbVar22 = pbVar24 + 1;
            break;
          }
                    /* try { // try from 00e66dc4 to 00e66dcb has its CatchHandler @ 00e66ee4 */
          wVar5 = (**(code **)(*plVar21 + 0x58))(plVar21);
          pwVar9 = *param_6;
          pbVar24 = pbVar24 + 1;
          *param_6 = pwVar9 + 1;
          *pwVar9 = wVar5;
          pbVar22 = (byte *)param_3;
        } while ((byte *)param_3 != pbVar24);
      }
      (**(code **)(*plVar21 + 0x60))(plVar21,pbVar22,param_3);
      pwVar9 = *param_6;
      *param_6 = pwVar9 + ((long)param_3 - (long)pbVar22);
      pwVar9 = pwVar9 + ((long)param_3 - (long)pbVar22);
      if (param_2 != param_3) {
        pwVar9 = param_4 + ((long)param_2 - (long)param_1);
      }
      *param_5 = pwVar9;
      if (((ulong)local_90 & 1) != 0) {
        operator_delete(local_80);
      }
      if (*(long *)(lVar3 + 0x28) == local_68) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00de5da0();
}



// ==========================================================================================
// Function: __get_weekdayname
// Address: 00e67d1c
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_weekdayname(int&, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >&, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, unsigned int&, std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_weekdayname(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                  *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
                 uint *param_4,ctype *param_5)

{
  undefined auVar1 [16];
  long lVar2;
  long lVar3;
  
  lVar2 = (***(code ***)(this + 0x10))();
  lVar3 = FUN_00e5bd3c(param_2,param_3,lVar2,lVar2 + 0x150,param_5,param_4,0);
  if (lVar3 - lVar2 < 0x150) {
    lVar2 = (lVar3 - lVar2 >> 3) * -0x5555555555555555;
    auVar1 = SEXT816(lVar2) * SEXT816(0x4924924924924925);
    *param_1 = (int)lVar2 + ((int)(auVar1._8_8_ >> 1) - (auVar1._12_4_ >> 0x1f)) * -7;
  }
  return;
}



// ==========================================================================================
// Function: __get_monthname
// Address: 00e67f64
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_monthname(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   >&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_monthname(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
               uint *param_4,ctype *param_5)

{
  long lVar1;
  long lVar2;
  
  lVar1 = (**(code **)(*(long *)(this + 0x10) + 8))();
  lVar2 = FUN_00e5bd3c(param_2,param_3,lVar1,lVar1 + 0x240,param_5,param_4,0);
  if (lVar2 - lVar1 < 0x240) {
    lVar1 = (lVar2 - lVar1 >> 3) * -0x5555555555555555;
    *param_1 = (int)lVar1 +
               ((int)((ulong)(lVar1 / 6 + (lVar1 >> 0x3f)) >> 1) -
               (SUB164(SEXT816(lVar1) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
  }
  return;
}



// ==========================================================================================
// Function: __get_year
// Address: 00e68164
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_year(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_year(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
           *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4
          ,ctype *param_5)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = FUN_00e69024(param_2,param_3,param_4,param_5,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    iVar1 = iVar3 + 0x76c;
    if (99 < iVar3) {
      iVar1 = iVar3;
    }
    iVar2 = iVar3 + 2000;
    if (0x44 < iVar3) {
      iVar2 = iVar1;
    }
    *param_1 = iVar2 + -0x76c;
  }
  return;
}



// ==========================================================================================
// Function: __get_day
// Address: 00e68874
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_day(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_day(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
         ,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4,
         ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 - 1U < 0x1f) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_hour
// Address: 00e688d8
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_hour(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_hour(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
           *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4
          ,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x18) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_12_hour
// Address: 00e68938
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_12_hour(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   >&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_12_hour(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
              *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
             uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 - 1U < 0xc) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_day_year_num
// Address: 00e6899c
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_day_year_num(int&, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >&, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, unsigned int&, std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_day_year_num(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                   *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
                  uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,3);
  if ((iVar1 < 0x16e) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_month
// Address: 00e689fc
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_month(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_month(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0xd) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1 + -1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_minute
// Address: 00e68a60
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_minute(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_minute(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
             *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
            uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x3c) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_white_space
// Address: 00e68ac0
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_white_space(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_white_space(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                  *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
                 ctype *param_4)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  long *plVar4;
  long *plVar5;
  
  plVar4 = (long *)(ulong)param_2;
  plVar5 = *(long **)param_1;
  while( true ) {
    if ((plVar5 != (long *)0x0) && (plVar5[3] == plVar5[4])) {
      iVar2 = (**(code **)(*plVar5 + 0x48))(plVar5);
      if (iVar2 == -1) {
        plVar5 = (long *)0x0;
        *(undefined8 *)param_1 = 0;
      }
      else {
        plVar5 = *(long **)param_1;
      }
    }
    if ((plVar4 == (long *)0x0) ||
       ((plVar4[3] == plVar4[4] && (iVar2 = (**(code **)(*plVar4 + 0x48))(plVar4), iVar2 == -1)))) {
      plVar4 = (long *)0x0;
    }
    if (plVar5 == (long *)0x0) break;
    plVar5 = *(long **)param_1;
    if ((byte *)plVar5[3] == (byte *)plVar5[4]) {
      uVar3 = (**(code **)(*plVar5 + 0x48))();
      if ((uVar3 >> 7 & 1) != 0) break;
    }
    else {
      bVar1 = *(byte *)plVar5[3];
      uVar3 = (uint)bVar1;
      if ((char)bVar1 < '\0') break;
    }
    if ((*(ulong *)(*(long *)(param_4 + 0x10) + (ulong)(uVar3 & 0xff) * 8) & 1) == 0) break;
    plVar5 = *(long **)param_1;
    if (plVar5[3] == plVar5[4]) {
      (**(code **)(*plVar5 + 0x50))();
      plVar5 = *(long **)param_1;
    }
    else {
      plVar5[3] = plVar5[3] + 1;
      plVar5 = *(long **)param_1;
    }
  }
  plVar5 = *(long **)param_1;
  if ((plVar5 != (long *)0x0) && (plVar5[3] == plVar5[4])) {
    iVar2 = (**(code **)(*plVar5 + 0x48))(plVar5);
    if (iVar2 == -1) {
      plVar5 = (long *)0x0;
      *(undefined8 *)param_1 = 0;
    }
    else {
      plVar5 = *(long **)param_1;
    }
  }
  if ((plVar4 == (long *)0x0) ||
     ((plVar4[3] == plVar4[4] && (iVar2 = (**(code **)(*plVar4 + 0x48))(plVar4), iVar2 == -1)))) {
    if (plVar5 != (long *)0x0) {
      return;
    }
  }
  else if (plVar5 == (long *)0x0) {
    return;
  }
  *param_3 = *param_3 | 2;
  return;
}



// ==========================================================================================
// Function: __get_am_pm
// Address: 00e68c68
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_am_pm(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_am_pm(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  byte bVar2;
  byte *pbVar3;
  byte *pbVar4;
  ulong uVar5;
  ulong uVar6;
  
  pbVar3 = (byte *)(**(code **)(*(long *)(this + 0x10) + 0x10))();
  if ((*pbVar3 & 1) == 0) {
    uVar5 = (ulong)(*pbVar3 >> 1);
    bVar2 = pbVar3[0x18];
  }
  else {
    uVar5 = *(ulong *)(pbVar3 + 8);
    bVar2 = pbVar3[0x18];
  }
  if ((bVar2 & 1) == 0) {
    uVar6 = (ulong)(bVar2 >> 1);
  }
  else {
    uVar6 = *(ulong *)(pbVar3 + 0x20);
  }
  if (uVar5 + uVar6 == 0) {
    *param_4 = *param_4 | 4;
  }
  else {
    pbVar4 = (byte *)FUN_00e5bd3c(param_2,param_3,pbVar3,pbVar3 + 0x30,param_5,param_4,0);
    iVar1 = *param_1;
    if ((iVar1 == 0xc) && (pbVar4 == pbVar3)) {
      *param_1 = 0;
    }
    else if ((iVar1 < 0xc) && ((long)pbVar4 - (long)pbVar3 == 0x18)) {
      *param_1 = iVar1 + 0xc;
    }
  }
  return;
}



// ==========================================================================================
// Function: __get_second
// Address: 00e68d58
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_second(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_second(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
             *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
            uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x3d) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_weekday
// Address: 00e68db8
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_weekday(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   >&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_weekday(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
              *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
             uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,1);
  if ((iVar1 < 7) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_year4
// Address: 00e68e18
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_year4(int&, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_year4(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e69024(param_2,param_3,param_4,param_5,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    *param_1 = iVar1 + -0x76c;
  }
  return;
}



// ==========================================================================================
// Function: __get_percent
// Address: 00e68e68
// ==========================================================================================

/* std::__ndk1::time_get<char, std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char>
   > >::__get_percent(std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >&,
   std::__ndk1::istreambuf_iterator<char, std::__ndk1::char_traits<char> >, unsigned int&,
   std::__ndk1::ctype<char> const&) const */

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_percent(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
              *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
             ctype *param_4)

{
  char cVar1;
  int iVar2;
  uint uVar3;
  long *plVar4;
  long *plVar5;
  
  plVar4 = (long *)(ulong)param_2;
  plVar5 = *(long **)param_1;
  if ((plVar5 == (long *)0x0) || (plVar5[3] != plVar5[4])) {
LAB_00e68ec0:
    if (plVar4 == (long *)0x0) goto LAB_00e68efc;
LAB_00e68ec4:
    if ((plVar4[3] == plVar4[4]) && (iVar2 = (**(code **)(*plVar4 + 0x48))(plVar4), iVar2 == -1))
    goto LAB_00e68efc;
    if (plVar5 != (long *)0x0) goto LAB_00e68f1c;
  }
  else {
    iVar2 = (**(code **)(*plVar5 + 0x48))(plVar5);
    if (iVar2 != -1) {
      plVar5 = *(long **)param_1;
      goto LAB_00e68ec0;
    }
    plVar5 = (long *)0x0;
    *(undefined8 *)param_1 = 0;
    if (plVar4 != (long *)0x0) goto LAB_00e68ec4;
LAB_00e68efc:
    if (plVar5 == (long *)0x0) {
LAB_00e68f1c:
      uVar3 = *param_3 | 6;
      goto LAB_00e69008;
    }
    plVar4 = (long *)0x0;
  }
  plVar5 = *(long **)param_1;
  if ((byte *)plVar5[3] == (byte *)plVar5[4]) {
    uVar3 = (**(code **)(*plVar5 + 0x48))();
  }
  else {
    uVar3 = (uint)*(byte *)plVar5[3];
  }
  cVar1 = (**(code **)(*(long *)param_4 + 0x48))(param_4,uVar3,0);
  if (cVar1 != '%') {
    uVar3 = *param_3 | 4;
    goto LAB_00e69008;
  }
  plVar5 = *(long **)param_1;
  if (plVar5[3] == plVar5[4]) {
    (**(code **)(*plVar5 + 0x50))(plVar5);
    plVar5 = *(long **)param_1;
    if (plVar5 != (long *)0x0) goto LAB_00e68f98;
LAB_00e68fc0:
    if (plVar4 == (long *)0x0) goto LAB_00e68ffc;
LAB_00e68fc4:
    if ((plVar4[3] == plVar4[4]) && (iVar2 = (**(code **)(*plVar4 + 0x48))(plVar4), iVar2 == -1))
    goto LAB_00e68ffc;
    if (plVar5 == (long *)0x0) {
      return;
    }
  }
  else {
    plVar5[3] = plVar5[3] + 1;
LAB_00e68f98:
    if (plVar5[3] != plVar5[4]) goto LAB_00e68fc0;
    iVar2 = (**(code **)(*plVar5 + 0x48))(plVar5);
    if (iVar2 != -1) {
      plVar5 = *(long **)param_1;
      goto LAB_00e68fc0;
    }
    plVar5 = (long *)0x0;
    *(undefined8 *)param_1 = 0;
    if (plVar4 != (long *)0x0) goto LAB_00e68fc4;
LAB_00e68ffc:
    if (plVar5 != (long *)0x0) {
      return;
    }
  }
  uVar3 = *param_3 | 2;
LAB_00e69008:
  *param_3 = uVar3;
  return;
}



// ==========================================================================================
// Function: __get_weekdayname
// Address: 00e69ae0
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_weekdayname(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_weekdayname(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                  *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
                 uint *param_4,ctype *param_5)

{
  undefined auVar1 [16];
  long lVar2;
  long lVar3;
  
  lVar2 = (***(code ***)(this + 0x10))();
  lVar3 = FUN_00e5eea8(param_2,param_3,lVar2,lVar2 + 0x150,param_5,param_4,0);
  if (lVar3 - lVar2 < 0x150) {
    lVar2 = (lVar3 - lVar2 >> 3) * -0x5555555555555555;
    auVar1 = SEXT816(lVar2) * SEXT816(0x4924924924924925);
    *param_1 = (int)lVar2 + ((int)(auVar1._8_8_ >> 1) - (auVar1._12_4_ >> 0x1f)) * -7;
  }
  return;
}



// ==========================================================================================
// Function: __get_monthname
// Address: 00e69d28
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_monthname(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_monthname(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
               uint *param_4,ctype *param_5)

{
  long lVar1;
  long lVar2;
  
  lVar1 = (**(code **)(*(long *)(this + 0x10) + 8))();
  lVar2 = FUN_00e5eea8(param_2,param_3,lVar1,lVar1 + 0x240,param_5,param_4,0);
  if (lVar2 - lVar1 < 0x240) {
    lVar1 = (lVar2 - lVar1 >> 3) * -0x5555555555555555;
    *param_1 = (int)lVar1 +
               ((int)((ulong)(lVar1 / 6 + (lVar1 >> 0x3f)) >> 1) -
               (SUB164(SEXT816(lVar1) * SEXT816(0x2aaaaaaaaaaaaaab),0xc) >> 0x1f)) * -0xc;
  }
  return;
}



// ==========================================================================================
// Function: __get_year
// Address: 00e69f28
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_year(int&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, unsigned int&, std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_year(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4
          ,ctype *param_5)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = FUN_00e6ae50(param_2,param_3,param_4,param_5,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    iVar1 = iVar3 + 0x76c;
    if (99 < iVar3) {
      iVar1 = iVar3;
    }
    iVar2 = iVar3 + 2000;
    if (0x44 < iVar3) {
      iVar2 = iVar1;
    }
    *param_1 = iVar2 + -0x76c;
  }
  return;
}



// ==========================================================================================
// Function: __get_day
// Address: 00e6a628
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_day(int&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, unsigned int&, std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_day(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
          *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4,
         ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 - 1U < 0x1f) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_hour
// Address: 00e6a68c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_hour(int&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, unsigned int&, std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_hour(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,uint *param_4
          ,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x18) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_12_hour
// Address: 00e6a6ec
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_12_hour(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_12_hour(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
              *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
             uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 - 1U < 0xc) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_day_year_num
// Address: 00e6a750
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_day_year_num(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_day_year_num(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                   *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
                  uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,3);
  if ((iVar1 < 0x16e) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_month
// Address: 00e6a7b0
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_month(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_month(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0xd) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1 + -1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_minute
// Address: 00e6a814
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_minute(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_minute(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
             *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
            uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x3c) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_white_space
// Address: 00e6a874
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >
   >::__get_white_space(std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t>
   >&, std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_white_space(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                  *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
                 ctype *param_4)

{
  bool bVar1;
  undefined4 uVar2;
  int iVar3;
  long *plVar4;
  ulong uVar5;
  long *plVar6;
  
  plVar6 = (long *)(ulong)param_2;
  plVar4 = *(long **)param_1;
  if (plVar4 != (long *)0x0) goto LAB_00e6a8b8;
LAB_00e6a8fc:
  bVar1 = true;
  if (plVar6 == (long *)0x0) goto LAB_00e6a93c;
  while( true ) {
    if ((int *)plVar6[3] == (int *)plVar6[4]) {
      iVar3 = (**(code **)(*plVar6 + 0x48))(plVar6);
    }
    else {
      iVar3 = *(int *)plVar6[3];
    }
    if (iVar3 == -1) goto LAB_00e6a93c;
    if (!bVar1) break;
    while( true ) {
      plVar4 = *(long **)param_1;
      if ((undefined4 *)plVar4[3] == (undefined4 *)plVar4[4]) {
        uVar2 = (**(code **)(*plVar4 + 0x48))();
      }
      else {
        uVar2 = *(undefined4 *)plVar4[3];
      }
      uVar5 = (**(code **)(*(long *)param_4 + 0x18))(param_4,1,uVar2);
      if ((uVar5 & 1) == 0) goto LAB_00e6a9ac;
      plVar4 = *(long **)param_1;
      if (plVar4[3] == plVar4[4]) {
        (**(code **)(*plVar4 + 0x50))();
        plVar4 = *(long **)param_1;
      }
      else {
        plVar4[3] = plVar4[3] + 4;
        plVar4 = *(long **)param_1;
      }
      if (plVar4 == (long *)0x0) goto LAB_00e6a8fc;
LAB_00e6a8b8:
      if ((int *)plVar4[3] == (int *)plVar4[4]) {
        iVar3 = (**(code **)(*plVar4 + 0x48))();
      }
      else {
        iVar3 = *(int *)plVar4[3];
      }
      if (iVar3 == -1) {
        *(undefined8 *)param_1 = 0;
        goto LAB_00e6a8fc;
      }
      bVar1 = *(long *)param_1 == 0;
      if (plVar6 != (long *)0x0) break;
LAB_00e6a93c:
      plVar6 = (long *)0x0;
      if (bVar1) goto LAB_00e6a9ac;
    }
  }
LAB_00e6a9ac:
  plVar4 = *(long **)param_1;
  if (plVar4 != (long *)0x0) {
    if ((int *)plVar4[3] == (int *)plVar4[4]) {
      iVar3 = (**(code **)(*plVar4 + 0x48))();
    }
    else {
      iVar3 = *(int *)plVar4[3];
    }
    if (iVar3 != -1) {
      bVar1 = *(long *)param_1 == 0;
      goto joined_r0x00e6aa00;
    }
    *(undefined8 *)param_1 = 0;
  }
  bVar1 = true;
joined_r0x00e6aa00:
  if (plVar6 == (long *)0x0) {
    if (!bVar1) {
      return;
    }
  }
  else {
    if ((int *)plVar6[3] == (int *)plVar6[4]) {
      iVar3 = (**(code **)(*plVar6 + 0x48))(plVar6);
    }
    else {
      iVar3 = *(int *)plVar6[3];
    }
    if (bVar1 != (iVar3 == -1)) {
      return;
    }
  }
  *param_3 = *param_3 | 2;
  return;
}



// ==========================================================================================
// Function: __get_am_pm
// Address: 00e6aa5c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_am_pm(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_am_pm(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  byte bVar2;
  byte *pbVar3;
  byte *pbVar4;
  ulong uVar5;
  ulong uVar6;
  
  pbVar3 = (byte *)(**(code **)(*(long *)(this + 0x10) + 0x10))();
  if ((*pbVar3 & 1) == 0) {
    uVar5 = (ulong)(*pbVar3 >> 1);
    bVar2 = pbVar3[0x18];
  }
  else {
    uVar5 = *(ulong *)(pbVar3 + 8);
    bVar2 = pbVar3[0x18];
  }
  if ((bVar2 & 1) == 0) {
    uVar6 = (ulong)(bVar2 >> 1);
  }
  else {
    uVar6 = *(ulong *)(pbVar3 + 0x20);
  }
  if (uVar5 + uVar6 == 0) {
    *param_4 = *param_4 | 4;
  }
  else {
    pbVar4 = (byte *)FUN_00e5eea8(param_2,param_3,pbVar3,pbVar3 + 0x30,param_5,param_4,0);
    iVar1 = *param_1;
    if ((iVar1 == 0xc) && (pbVar4 == pbVar3)) {
      *param_1 = 0;
    }
    else if ((iVar1 < 0xc) && ((long)pbVar4 - (long)pbVar3 == 0x18)) {
      *param_1 = iVar1 + 0xc;
    }
  }
  return;
}



// ==========================================================================================
// Function: __get_second
// Address: 00e6ab4c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_second(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_second(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
             *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
            uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,2);
  if ((iVar1 < 0x3d) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_weekday
// Address: 00e6abac
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_weekday(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_weekday(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
              *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
             uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,1);
  if ((iVar1 < 7) && ((*param_4 >> 2 & 1) == 0)) {
    *param_1 = iVar1;
  }
  else {
    *param_4 = *param_4 | 4;
  }
  return;
}



// ==========================================================================================
// Function: __get_year4
// Address: 00e6ac0c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_year4(int&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >&,
   std::__ndk1::istreambuf_iterator<wchar_t, std::__ndk1::char_traits<wchar_t> >, unsigned int&,
   std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_year4(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
            *this,int *param_1,istreambuf_iterator *param_2,istreambuf_iterator param_3,
           uint *param_4,ctype *param_5)

{
  int iVar1;
  
  iVar1 = FUN_00e6ae50(param_2,param_3,param_4,param_5,4);
  if ((*(byte *)param_4 >> 2 & 1) == 0) {
    *param_1 = iVar1 + -0x76c;
  }
  return;
}



// ==========================================================================================
// Function: __get_percent
// Address: 00e6ac5c
// ==========================================================================================

/* std::__ndk1::time_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__get_percent(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, unsigned int&, std::__ndk1::ctype<wchar_t> const&) const */

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_percent(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
              *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
             ctype *param_4)

{
  bool bVar1;
  char cVar2;
  undefined4 uVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  uint uVar7;
  
  plVar6 = (long *)(ulong)param_2;
  plVar5 = *(long **)param_1;
  if (plVar5 == (long *)0x0) {
LAB_00e6acd8:
    bVar1 = true;
    if (plVar6 != (long *)0x0) goto LAB_00e6ace0;
LAB_00e6acb4:
    if (bVar1) goto LAB_00e6ad30;
    plVar5 = (long *)0x0;
  }
  else {
    if ((int *)plVar5[3] == (int *)plVar5[4]) {
      iVar4 = (**(code **)(*plVar5 + 0x48))();
    }
    else {
      iVar4 = *(int *)plVar5[3];
    }
    if (iVar4 == -1) {
      *(undefined8 *)param_1 = 0;
      goto LAB_00e6acd8;
    }
    bVar1 = *(long *)param_1 == 0;
    if (plVar6 == (long *)0x0) goto LAB_00e6acb4;
LAB_00e6ace0:
    if ((int *)plVar6[3] == (int *)plVar6[4]) {
      iVar4 = (**(code **)(*plVar6 + 0x48))(plVar6);
    }
    else {
      iVar4 = *(int *)plVar6[3];
    }
    plVar5 = (long *)0x0;
    if (iVar4 != -1) {
      plVar5 = plVar6;
    }
    if (bVar1 == (iVar4 == -1)) {
LAB_00e6ad30:
      uVar7 = *param_3 | 6;
      goto LAB_00e6ae34;
    }
  }
  plVar6 = *(long **)param_1;
  if ((undefined4 *)plVar6[3] == (undefined4 *)plVar6[4]) {
    uVar3 = (**(code **)(*plVar6 + 0x48))();
  }
  else {
    uVar3 = *(undefined4 *)plVar6[3];
  }
  cVar2 = (**(code **)(*(long *)param_4 + 0x68))(param_4,uVar3,0);
  if (cVar2 != '%') {
    uVar7 = *param_3 | 4;
    goto LAB_00e6ae34;
  }
  plVar6 = *(long **)param_1;
  if (plVar6[3] == plVar6[4]) {
    (**(code **)(*plVar6 + 0x50))();
    plVar6 = *(long **)param_1;
    if (plVar6 != (long *)0x0) goto LAB_00e6ada8;
LAB_00e6adfc:
    bVar1 = true;
    if (plVar5 == (long *)0x0) goto LAB_00e6ae04;
LAB_00e6add0:
    if ((int *)plVar5[3] == (int *)plVar5[4]) {
      iVar4 = (**(code **)(*plVar5 + 0x48))(plVar5);
    }
    else {
      iVar4 = *(int *)plVar5[3];
    }
    if (bVar1 != (iVar4 == -1)) {
      return;
    }
  }
  else {
    plVar6[3] = plVar6[3] + 4;
LAB_00e6ada8:
    if ((int *)plVar6[3] == (int *)plVar6[4]) {
      iVar4 = (**(code **)(*plVar6 + 0x48))();
    }
    else {
      iVar4 = *(int *)plVar6[3];
    }
    if (iVar4 == -1) {
      *(undefined8 *)param_1 = 0;
      goto LAB_00e6adfc;
    }
    bVar1 = *(long *)param_1 == 0;
    if (plVar5 != (long *)0x0) goto LAB_00e6add0;
LAB_00e6ae04:
    if (!bVar1) {
      return;
    }
  }
  uVar7 = *param_3 | 2;
LAB_00e6ae34:
  *param_3 = uVar7;
  return;
}



// ==========================================================================================
// Function: __do_put
// Address: 00e6b580
// ==========================================================================================

/* std::__ndk1::__time_put::__do_put(char*, char*&, tm const*, char, char) const */

void __thiscall
std::__ndk1::__time_put::__do_put
          (__time_put *this,char *param_1,char **param_2,tm *param_3,char param_4,char param_5)

{
  long lVar1;
  size_t sVar2;
  char local_3c;
  char local_3b;
  char local_3a;
  undefined local_39;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_3c = '%';
  local_39 = 0;
  local_3b = param_4;
  local_3a = param_5;
  if (param_5 != '\0') {
    local_3b = param_5;
    local_3a = param_4;
  }
  sVar2 = strftime_l(param_1,(long)*param_2 - (long)param_1,&local_3c,param_3,*(__locale_t *)this);
  *param_2 = param_1 + sVar2;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __do_put
// Address: 00e6b9f4
// ==========================================================================================

/* std::__ndk1::__time_put::__do_put(wchar_t*, wchar_t*&, tm const*, char, char) const */

void __thiscall
std::__ndk1::__time_put::__do_put
          (__time_put *this,wchar_t *param_1,wchar_t **param_2,tm *param_3,char param_4,char param_5
          )

{
  long lVar1;
  mbstate_t mVar2;
  __locale_t __dataset;
  size_t sVar3;
  wchar_t *pwVar4;
  char *local_c0;
  undefined8 local_b8;
  char acStack_ac [100];
  long local_48;
  
  mVar2 = local_b8;
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  local_b8._0_2_ = CONCAT11(param_4,0x25);
  local_b8._0_3_ = CONCAT12(param_5,(undefined2)local_b8);
  local_b8._4_4_ = mVar2.__value;
  local_b8._0_4_ = (uint)(uint3)local_b8;
  mVar2 = local_b8;
  if (param_5 != '\0') {
    local_b8._1_1_ = param_5;
    local_b8._0_1_ = 0x25;
    local_b8._3_5_ = mVar2._3_5_;
    local_b8._2_1_ = param_4;
  }
  strftime_l(acStack_ac,100,(char *)&local_b8,param_3,*(__locale_t *)this);
  local_b8._0_4_ = 0;
  local_b8._4_4_ = (_union_27)0x0;
  pwVar4 = *param_2;
  local_c0 = acStack_ac;
  __dataset = uselocale(*(__locale_t *)this);
                    /* try { // try from 00e6ba80 to 00e6ba93 has its CatchHandler @ 00e6baf4 */
  sVar3 = mbsrtowcs(param_1,&local_c0,(long)pwVar4 - (long)param_1 >> 2,(mbstate_t *)&local_b8);
  if (__dataset != (__locale_t)0x0) {
                    /* try { // try from 00e6ba9c to 00e6baa3 has its CatchHandler @ 00e6baf0 */
    uselocale(__dataset);
  }
  if (sVar3 == 0xffffffffffffffff) {
    __throw_runtime_error("locale not supported");
  }
  else {
    *param_2 = param_1 + sVar3;
    if (*(long *)(lVar1 + 0x28) == local_48) {
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __do_nothing
// Address: 00e6c398
// ==========================================================================================

/* std::__ndk1::__do_nothing(void*) */

void std::__ndk1::__do_nothing(void *param_1)

{
  return;
}



// ==========================================================================================
// Function: __do_get
// Address: 00e6c3a0
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::money_get<char, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> > >::__do_get(std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >&, std::__ndk1::istreambuf_iterator<char,
   std::__ndk1::char_traits<char> >, bool, std::__ndk1::locale const&, unsigned int, unsigned int&,
   bool&, std::__ndk1::ctype<char> const&, std::__ndk1::unique_ptr<char, void (*)(void*)>&, char*&,
   char*) */

undefined4
std::__ndk1::money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get(istreambuf_iterator *param_1,istreambuf_iterator param_2,bool param_3,locale *param_4,
        uint param_5,uint *param_6,bool *param_7,ctype *param_8,unique_ptr *param_9,char **param_10,
        char *param_11)

{
  byte *pbVar1;
  ulong uVar2;
  long lVar3;
  ulong *puVar4;
  bool bVar5;
  char cVar6;
  byte bVar7;
  int iVar8;
  int iVar9;
  uint uVar10;
  long *__ptr;
  void *pvVar11;
  char *pcVar12;
  byte *pbVar13;
  ulong uVar14;
  long *plVar15;
  ulong uVar16;
  size_t sVar17;
  long *plVar18;
  byte *pbVar19;
  long *plVar20;
  char *pcVar21;
  char *pcVar22;
  long lVar23;
  byte *pbVar24;
  byte *pbVar25;
  byte *pbVar26;
  undefined4 uVar27;
  long *plVar28;
  ulong uVar29;
  long *plVar30;
  ulong *local_2c8;
  code *local_2a8;
  long *local_2a0;
  int local_28c;
  undefined8 local_288;
  ulong local_280;
  void *local_278;
  ulong local_270;
  ulong local_268;
  char *local_260;
  ulong local_258;
  ulong local_250;
  char *local_248;
  ulong local_240;
  ulong local_238;
  byte *local_230;
  ulong local_228;
  ulong local_220;
  byte *local_218;
  byte local_210 [4];
  char local_20c [4];
  pattern local_208 [3];
  char local_205;
  long local_200 [50];
  long local_70 [2];
  
  plVar28 = (long *)(ulong)param_2;
  lVar3 = tpidr_el0;
  local_70[0] = *(long *)(lVar3 + 0x28);
  local_228 = 0;
  local_220 = 0;
  local_218 = (byte *)0x0;
  local_240 = 0;
  local_238 = 0;
  local_230 = (byte *)0x0;
  local_258 = 0;
  local_250 = 0;
  local_248 = (char *)0x0;
  local_270 = 0;
  local_268 = 0;
  local_260 = (char *)0x0;
  local_288 = 0;
  local_280 = 0;
  local_278 = (void *)0x0;
                    /* try { // try from 00e6c414 to 00e6c44b has its CatchHandler @ 00e6d504 */
  __money_get<char>::__gather_info
            (param_3,param_4,local_208,local_20c,(char *)local_210,(basic_string *)&local_228,
             (basic_string *)&local_240,(basic_string *)&local_258,(basic_string *)&local_270,
             &local_28c);
  pbVar19 = (byte *)((ulong)&local_240 | 1);
  pcVar21 = (char *)((ulong)&local_270 | 1);
  local_2c8 = (ulong *)0x0;
  __ptr = local_200;
  local_2a8 = (code *)PTR___do_nothing_01ff56a8;
  uVar29 = 0;
  local_2a0 = local_70;
  plVar15 = local_200;
  *param_10 = *(char **)param_9;
LAB_00e6c4bc:
  plVar30 = *(long **)param_1;
  if ((plVar30 == (long *)0x0) || (plVar30[3] != plVar30[4])) {
joined_r0x00e6c4d0:
    if (plVar28 == (long *)0x0) goto LAB_00e6c530;
LAB_00e6c4d4:
                    /* try { // try from 00e6c4e8 to 00e6c50f has its CatchHandler @ 00e6d530 */
    if ((plVar28[3] == plVar28[4]) && (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1)
       ) goto LAB_00e6c530;
    if (plVar30 != (long *)0x0) goto LAB_00e6d1b8;
  }
  else {
    iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
    if (iVar8 == -1) {
      plVar30 = (long *)0x0;
      *(undefined8 *)param_1 = 0;
      goto joined_r0x00e6c4d0;
    }
    plVar30 = *(long **)param_1;
    if (plVar28 != (long *)0x0) goto LAB_00e6c4d4;
LAB_00e6c530:
    plVar28 = (long *)0x0;
    if (plVar30 == (long *)0x0) goto LAB_00e6d1b8;
  }
  puVar4 = local_2c8;
  switch(local_208[uVar29]) {
  case (pattern)0x0:
    if (uVar29 != 3) goto LAB_00e6c9f8;
    goto LAB_00e6d1b8;
  case (pattern)0x1:
    if (uVar29 != 3) {
      plVar30 = *(long **)param_1;
      if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
                    /* try { // try from 00e6c990 to 00e6c993 has its CatchHandler @ 00e6d530 */
        uVar10 = (**(code **)(*plVar30 + 0x48))();
      }
      else {
        uVar10 = (uint)*(byte *)plVar30[3];
      }
      if (((uVar10 >> 7 & 1) == 0) &&
         ((*(ulong *)(*(long *)(param_8 + 0x10) + (ulong)(uVar10 & 0xff) * 8) & 1) != 0)) {
        plVar30 = *(long **)param_1;
        pcVar12 = (char *)plVar30[3];
        if (pcVar12 == (char *)plVar30[4]) {
                    /* try { // try from 00e6c9d0 to 00e6c9df has its CatchHandler @ 00e6d524 */
          cVar6 = (**(code **)(*plVar30 + 0x50))();
        }
        else {
          plVar30[3] = (long)(pcVar12 + 1);
          cVar6 = *pcVar12;
        }
        basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::push_back
                  ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *
                   )&local_288,cVar6);
LAB_00e6c9f8:
        do {
          plVar30 = *(long **)param_1;
          if ((plVar30 == (long *)0x0) || (plVar30[3] != plVar30[4])) {
joined_r0x00e6ca0c:
            if (plVar28 == (long *)0x0) goto LAB_00e6ca6c;
LAB_00e6ca10:
                    /* try { // try from 00e6ca24 to 00e6ca97 has its CatchHandler @ 00e6d548 */
            if ((plVar28[3] == plVar28[4]) &&
               (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1)) goto LAB_00e6ca6c;
            if (plVar30 != (long *)0x0) goto switchD_00e6c55c_caseD_5;
          }
          else {
            iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
            if (iVar8 == -1) {
              plVar30 = (long *)0x0;
              *(undefined8 *)param_1 = 0;
              goto joined_r0x00e6ca0c;
            }
            plVar30 = *(long **)param_1;
            if (plVar28 != (long *)0x0) goto LAB_00e6ca10;
LAB_00e6ca6c:
            plVar28 = (long *)0x0;
            if (plVar30 == (long *)0x0) goto switchD_00e6c55c_caseD_5;
          }
          plVar30 = *(long **)param_1;
          if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
            uVar10 = (**(code **)(*plVar30 + 0x48))();
          }
          else {
            uVar10 = (uint)*(byte *)plVar30[3];
          }
          if (((uVar10 >> 7 & 1) != 0) ||
             ((*(ulong *)(*(long *)(param_8 + 0x10) + (ulong)(uVar10 & 0xff) * 8) & 1) == 0))
          goto switchD_00e6c55c_caseD_5;
          plVar30 = *(long **)param_1;
          pcVar12 = (char *)plVar30[3];
          if (pcVar12 == (char *)plVar30[4]) {
                    /* try { // try from 00e6cac4 to 00e6cacb has its CatchHandler @ 00e6d54c */
            cVar6 = (**(code **)(*plVar30 + 0x50))();
          }
          else {
            plVar30[3] = (long)(pcVar12 + 1);
            cVar6 = *pcVar12;
          }
                    /* try { // try from 00e6c9f0 to 00e6c9f7 has its CatchHandler @ 00e6d54c */
          basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::push_back
                    ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      *)&local_288,cVar6);
        } while( true );
      }
      goto LAB_00e6d42c;
    }
    goto LAB_00e6d1b8;
  case (pattern)0x2:
    pbVar13 = pbVar19;
    if ((uVar29 < 2) || (local_2c8 != (ulong *)0x0)) {
      bVar5 = (local_240 & 1) == 0;
      if (!bVar5) {
        pbVar13 = local_230;
      }
      pbVar26 = pbVar13;
      if (uVar29 != 0) goto LAB_00e6c900;
    }
    else {
      if (((uint)(uVar29 == 2 && local_205 != '\0') | param_5 >> 9 & 1) != 1) {
        local_2c8 = (ulong *)0x0;
        puVar4 = local_2c8;
        break;
      }
      bVar5 = (local_240 & 1) == 0;
      if (!bVar5) {
        pbVar13 = local_230;
      }
LAB_00e6c900:
      pbVar26 = pbVar13;
      if ((byte)local_208[(int)uVar29 - 1] < 2) {
        uVar14 = (local_240 & 0xff) >> 1;
        if (!bVar5) {
          uVar14 = local_238;
        }
        pbVar25 = pbVar13;
        if (uVar14 != 0) {
          pbVar1 = pbVar13 + uVar14;
          pbVar24 = pbVar13;
          do {
            pbVar25 = pbVar24;
            if (((char)*pbVar24 < '\0') ||
               ((*(ulong *)(*(long *)(param_8 + 0x10) + (ulong)*pbVar24 * 8) & 1) == 0)) break;
            uVar14 = uVar14 - 1;
            pbVar24 = pbVar24 + 1;
            pbVar25 = pbVar1;
          } while (uVar14 != 0);
        }
        uVar14 = (long)pbVar25 - (long)pbVar13;
        if ((local_288 & 1) == 0) {
          uVar16 = local_288 >> 1 & 0x7f;
          if (uVar14 <= uVar16) {
            lVar23 = (long)&local_288 + uVar16 + 1;
            pvVar11 = (void *)((ulong)&local_288 | 1);
LAB_00e6ccb8:
            pbVar26 = pbVar25;
            if (lVar23 - uVar14 != (long)pvVar11 + uVar16) {
              pbVar24 = (byte *)0x0;
              do {
                pbVar26 = pbVar13;
                if (pbVar24[lVar23 - uVar14] != pbVar13[(long)pbVar24]) break;
                pbVar24 = pbVar24 + 1;
                pbVar26 = pbVar25;
              } while ((byte *)((long)pvVar11 +
                               (long)(pbVar25 + ((uVar16 - lVar23) - (long)pbVar13))) != pbVar24);
            }
          }
        }
        else if (uVar14 <= local_280) {
          lVar23 = (long)local_278 + local_280;
          uVar16 = local_280;
          pvVar11 = local_278;
          goto LAB_00e6ccb8;
        }
      }
    }
    uVar14 = (local_240 & 0xff) >> 1;
    if (!bVar5) {
      uVar14 = local_238;
    }
    for (pbVar13 = pbVar13 + uVar14; pbVar26 != pbVar13; pbVar13 = pbVar13 + uVar14) {
      plVar30 = *(long **)param_1;
      if ((plVar30 == (long *)0x0) || (plVar30[3] != plVar30[4])) {
joined_r0x00e6cb60:
        if (plVar28 == (long *)0x0) goto LAB_00e6cbc0;
LAB_00e6cb64:
                    /* try { // try from 00e6cb78 to 00e6cbeb has its CatchHandler @ 00e6d534 */
        if ((plVar28[3] == plVar28[4]) &&
           (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1)) goto LAB_00e6cbc0;
        if (plVar30 != (long *)0x0) break;
      }
      else {
        iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
        if (iVar8 == -1) {
          plVar30 = (long *)0x0;
          *(undefined8 *)param_1 = 0;
          goto joined_r0x00e6cb60;
        }
        plVar30 = *(long **)param_1;
        if (plVar28 != (long *)0x0) goto LAB_00e6cb64;
LAB_00e6cbc0:
        plVar28 = (long *)0x0;
        if (plVar30 == (long *)0x0) break;
      }
      plVar30 = *(long **)param_1;
      if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
        bVar7 = (**(code **)(*plVar30 + 0x48))();
      }
      else {
        bVar7 = *(byte *)plVar30[3];
      }
      if (*pbVar26 != bVar7) break;
      plVar30 = *(long **)param_1;
      if (plVar30[3] == plVar30[4]) {
                    /* try { // try from 00e6cc10 to 00e6cc13 has its CatchHandler @ 00e6d528 */
        (**(code **)(*plVar30 + 0x50))();
      }
      else {
        plVar30[3] = plVar30[3] + 1;
      }
      pbVar26 = pbVar26 + 1;
      uVar14 = local_240 >> 1 & 0x7f;
      pbVar13 = pbVar19;
      if ((local_240 & 1) != 0) {
        uVar14 = local_238;
        pbVar13 = local_230;
      }
    }
    if ((param_5 >> 9 & 1) == 0) break;
    uVar14 = local_240 >> 1 & 0x7f;
    pbVar13 = pbVar19;
    if ((local_240 & 1) != 0) {
      uVar14 = local_238;
      pbVar13 = local_230;
    }
    if (pbVar26 != pbVar13 + uVar14) goto LAB_00e6d42c;
    break;
  case (pattern)0x3:
    uVar16 = local_258 & 0xff;
    bVar7 = (byte)local_258 & 1;
    uVar14 = (ulong)((byte)local_258 >> 1);
    if ((local_258 & 1) != 0) {
      uVar14 = local_250;
    }
    uVar2 = (ulong)((byte)local_270 >> 1);
    if ((local_270 & 1) != 0) {
      uVar2 = local_268;
    }
    if (uVar14 + uVar2 != 0) {
      if (uVar14 == 0) {
        plVar30 = *(long **)param_1;
        if ((char *)plVar30[3] == (char *)plVar30[4]) {
          cVar6 = (**(code **)(*plVar30 + 0x48))();
        }
        else {
          cVar6 = *(char *)plVar30[3];
        }
        pcVar12 = pcVar21;
        if (((byte)local_270 & 1) != 0) {
          pcVar12 = local_260;
        }
        if (*pcVar12 == cVar6) {
          plVar30 = *(long **)param_1;
          if (plVar30[3] == plVar30[4]) {
            (**(code **)(*plVar30 + 0x50))();
            bVar7 = (byte)local_270;
          }
          else {
            plVar30[3] = plVar30[3] + 1;
            bVar7 = (byte)local_270;
          }
          *param_7 = true;
          uVar14 = (ulong)(bVar7 >> 1);
          if ((bVar7 & 1) != 0) {
            uVar14 = local_268;
          }
LAB_00e6d168:
          puVar4 = &local_270;
          if (uVar14 < 2) {
            puVar4 = local_2c8;
          }
        }
      }
      else {
        plVar30 = *(long **)param_1;
        pcVar12 = (char *)plVar30[3];
        if (uVar2 == 0) {
          if (pcVar12 == (char *)plVar30[4]) {
                    /* try { // try from 00e6d050 to 00e6d187 has its CatchHandler @ 00e6d530 */
            cVar6 = (**(code **)(*plVar30 + 0x48))();
            uVar16 = local_258 & 0xff;
            bVar7 = (byte)local_258 & 1;
          }
          else {
            cVar6 = *pcVar12;
          }
          pcVar12 = (char *)((ulong)&local_258 | 1);
          if (bVar7 != 0) {
            pcVar12 = local_248;
          }
          if (*pcVar12 != cVar6) {
            *param_7 = true;
            break;
          }
          plVar30 = *(long **)param_1;
          if (plVar30[3] == plVar30[4]) {
            (**(code **)(*plVar30 + 0x50))();
            goto LAB_00e6d188;
          }
          plVar30[3] = plVar30[3] + 1;
        }
        else {
          if (pcVar12 == (char *)plVar30[4]) {
                    /* try { // try from 00e6cc5c to 00e6cd07 has its CatchHandler @ 00e6d530 */
            cVar6 = (**(code **)(*plVar30 + 0x48))();
            uVar16 = local_258 & 0xff;
            bVar7 = (byte)local_258 & 1;
          }
          else {
            cVar6 = *pcVar12;
          }
          plVar30 = *(long **)param_1;
          pcVar12 = (char *)((ulong)&local_258 | 1);
          if (bVar7 != 0) {
            pcVar12 = local_248;
          }
          pcVar22 = (char *)plVar30[3];
          if (*pcVar12 != cVar6) {
            if (pcVar22 == (char *)plVar30[4]) {
              cVar6 = (**(code **)(*plVar30 + 0x48))(plVar30);
            }
            else {
              cVar6 = *pcVar22;
            }
            pcVar12 = pcVar21;
            if ((local_270 & 1) != 0) {
              pcVar12 = local_260;
            }
            if (*pcVar12 == cVar6) {
              plVar30 = *(long **)param_1;
              if (plVar30[3] == plVar30[4]) {
                (**(code **)(*plVar30 + 0x50))();
              }
              else {
                plVar30[3] = plVar30[3] + 1;
              }
              *param_7 = true;
              uVar14 = (ulong)((byte)local_270 >> 1);
              if (((byte)local_270 & 1) != 0) {
                uVar14 = local_268;
              }
              goto LAB_00e6d168;
            }
            goto LAB_00e6d42c;
          }
          if (pcVar22 == (char *)plVar30[4]) {
            (**(code **)(*plVar30 + 0x50))(plVar30);
LAB_00e6d188:
            uVar16 = local_258 & 0xff;
            bVar7 = (byte)local_258 & 1;
          }
          else {
            plVar30[3] = (long)(pcVar22 + 1);
          }
        }
        uVar14 = uVar16 >> 1;
        if (bVar7 != 0) {
          uVar14 = local_250;
        }
        puVar4 = &local_258;
        if (uVar14 < 2) {
          puVar4 = local_2c8;
        }
      }
    }
    break;
  case (pattern)0x4:
    iVar8 = 0;
    plVar30 = plVar15;
LAB_00e6c584:
    plVar15 = *(long **)param_1;
    if ((plVar15 == (long *)0x0) || (plVar15[3] != plVar15[4])) {
joined_r0x00e6c598:
      if (plVar28 == (long *)0x0) goto LAB_00e6c5f8;
LAB_00e6c59c:
                    /* try { // try from 00e6c5b0 to 00e6c5d7 has its CatchHandler @ 00e6d544 */
      if ((plVar28[3] == plVar28[4]) &&
         (iVar9 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar9 == -1)) goto LAB_00e6c5f8;
      if (plVar15 != (long *)0x0) goto LAB_00e6c884;
    }
    else {
      iVar9 = (**(code **)(*plVar15 + 0x48))(plVar15);
      if (iVar9 == -1) {
        plVar15 = (long *)0x0;
        *(undefined8 *)param_1 = 0;
        goto joined_r0x00e6c598;
      }
      plVar15 = *(long **)param_1;
      if (plVar28 != (long *)0x0) goto LAB_00e6c59c;
LAB_00e6c5f8:
      plVar28 = (long *)0x0;
      if (plVar15 == (long *)0x0) goto LAB_00e6c884;
    }
    plVar15 = *(long **)param_1;
    if ((byte *)plVar15[3] != (byte *)plVar15[4]) {
      bVar7 = *(byte *)plVar15[3];
      uVar10 = (uint)bVar7;
      if (-1 < (char)bVar7) goto LAB_00e6c630;
LAB_00e6c640:
      uVar14 = local_228 >> 1 & 0x7f;
      if ((local_228 & 1) != 0) {
        uVar14 = local_220;
      }
      if (((local_210[0] == bVar7) && (iVar8 != 0)) && (uVar14 != 0)) {
        if (plVar30 != local_2a0) {
LAB_00e6c740:
          *(int *)plVar30 = iVar8;
          iVar8 = 0;
          plVar30 = (long *)((long)plVar30 + 4);
          goto LAB_00e6c794;
        }
        uVar14 = (long)local_2a0 - (long)__ptr;
        sVar17 = 4;
        if (uVar14 != 0) {
          sVar17 = uVar14 * 2;
        }
        if (0x7ffffffffffffffe < uVar14) {
          sVar17 = 0xffffffffffffffff;
        }
        if (local_2a8 == (code *)PTR___do_nothing_01ff56a8) {
          __ptr = (long *)malloc(sVar17);
        }
        else {
          __ptr = (long *)realloc(__ptr,sVar17);
        }
        if (__ptr != (long *)0x0) {
          local_2a0 = (long *)((long)__ptr + (sVar17 & 0xfffffffffffffffc));
          plVar30 = (long *)((long)__ptr + uVar14);
          local_2a8 = (code *)PTR_free_01ff56b0;
          goto LAB_00e6c740;
        }
                    /* try { // try from 00e6d4dc to 00e6d4e7 has its CatchHandler @ 00e6d53c */
        __throw_bad_alloc();
LAB_00e6d4e4:
        __throw_bad_alloc();
LAB_00e6d4e8:
                    /* try { // try from 00e6d4e8 to 00e6d4f7 has its CatchHandler @ 00e6d520 */
        __throw_bad_alloc();
        goto LAB_00e6d4f0;
      }
      goto LAB_00e6c884;
    }
                    /* try { // try from 00e6c624 to 00e6c627 has its CatchHandler @ 00e6d540 */
    uVar10 = (**(code **)(*plVar15 + 0x48))();
    bVar7 = (byte)uVar10;
    if ((uVar10 >> 7 & 1) != 0) goto LAB_00e6c640;
LAB_00e6c630:
    bVar7 = (byte)uVar10;
    if (((uint)*(undefined8 *)(*(long *)(param_8 + 0x10) + (ulong)(uVar10 & 0xff) * 8) >> 6 & 1) ==
        0) goto LAB_00e6c640;
    pbVar13 = (byte *)*param_10;
    if (pbVar13 == (byte *)param_11) {
      uVar14 = (long)param_11 - (long)*(void **)param_9;
      sVar17 = uVar14 * 2;
      if (uVar14 == 0) {
        sVar17 = 1;
      }
      if (0x7ffffffffffffffe < uVar14) {
        sVar17 = 0xffffffffffffffff;
      }
      if (*(undefined **)(param_9 + 8) == PTR___do_nothing_01ff56a8) {
        pvVar11 = malloc(sVar17);
      }
      else {
        pvVar11 = realloc(*(void **)param_9,sVar17);
      }
      if (pvVar11 != (void *)0x0) {
        *(void **)param_9 = pvVar11;
        *(undefined **)(param_9 + 8) = PTR_free_01ff56b0;
        pbVar13 = (byte *)((long)pvVar11 + uVar14);
        *param_10 = (char *)pbVar13;
        param_11 = (char *)(*(long *)param_9 + sVar17);
        goto LAB_00e6c784;
      }
      goto LAB_00e6d4e4;
    }
LAB_00e6c784:
    iVar8 = iVar8 + 1;
    *param_10 = (char *)(pbVar13 + 1);
    *pbVar13 = bVar7;
LAB_00e6c794:
    plVar15 = *(long **)param_1;
    if (plVar15[3] == plVar15[4]) {
                    /* try { // try from 00e6c7ac to 00e6c7af has its CatchHandler @ 00e6d544 */
      (**(code **)(*plVar15 + 0x50))();
    }
    else {
      plVar15[3] = plVar15[3] + 1;
    }
    goto LAB_00e6c584;
  }
switchD_00e6c55c_caseD_5:
  local_2c8 = puVar4;
  uVar29 = uVar29 + 1;
  if (uVar29 == 4) goto LAB_00e6d1b8;
  goto LAB_00e6c4bc;
LAB_00e6c884:
  plVar15 = plVar30;
  if ((__ptr != plVar30) && (iVar8 != 0)) {
    if (plVar30 == local_2a0) {
      uVar14 = (long)local_2a0 - (long)__ptr;
      sVar17 = 4;
      if (uVar14 != 0) {
        sVar17 = uVar14 * 2;
      }
      if (0x7ffffffffffffffe < uVar14) {
        sVar17 = 0xffffffffffffffff;
      }
      if (local_2a8 == (code *)PTR___do_nothing_01ff56a8) {
        __ptr = (long *)malloc(sVar17);
      }
      else {
        __ptr = (long *)realloc(__ptr,sVar17);
      }
      if (__ptr == (long *)0x0) {
LAB_00e6d4f0:
        __throw_bad_alloc();
        goto LAB_00e6d4f8;
      }
      local_2a0 = (long *)((long)__ptr + (sVar17 & 0xfffffffffffffffc));
      plVar30 = (long *)((long)__ptr + uVar14);
      local_2a8 = (code *)PTR_free_01ff56b0;
    }
    plVar15 = (long *)((long)plVar30 + 4);
    *(int *)plVar30 = iVar8;
  }
  if (0 < local_28c) {
    plVar30 = *(long **)param_1;
    if ((plVar30 != (long *)0x0) && (plVar30[3] == plVar30[4])) {
      iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
      if (iVar8 == -1) {
        plVar30 = (long *)0x0;
        *(undefined8 *)param_1 = 0;
      }
      else {
        plVar30 = *(long **)param_1;
      }
    }
                    /* try { // try from 00e6cdb4 to 00e6ce5b has its CatchHandler @ 00e6d500 */
    if ((plVar28 == (long *)0x0) ||
       ((plVar28[3] == plVar28[4] && (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1))
       )) {
      if (plVar30 == (long *)0x0) goto LAB_00e6d42c;
      plVar28 = (long *)0x0;
    }
    else if (plVar30 != (long *)0x0) goto LAB_00e6d42c;
    plVar30 = *(long **)param_1;
    if ((char *)plVar30[3] == (char *)plVar30[4]) {
      cVar6 = (**(code **)(*plVar30 + 0x48))();
    }
    else {
      cVar6 = *(char *)plVar30[3];
    }
    if (local_20c[0] == cVar6) {
      plVar30 = *(long **)param_1;
      if (plVar30[3] == plVar30[4]) {
        (**(code **)(*plVar30 + 0x50))();
      }
      else {
        plVar30[3] = plVar30[3] + 1;
      }
joined_r0x00e6ce64:
      if (0 < local_28c) {
        do {
          plVar30 = *(long **)param_1;
          if ((plVar30 == (long *)0x0) || (plVar30[3] != plVar30[4])) {
joined_r0x00e6cea8:
            if (plVar28 == (long *)0x0) goto LAB_00e6cf08;
LAB_00e6ceac:
                    /* try { // try from 00e6cec0 to 00e6d037 has its CatchHandler @ 00e6d538 */
            if ((plVar28[3] == plVar28[4]) &&
               (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1)) goto LAB_00e6cf08;
            if (plVar30 != (long *)0x0) goto LAB_00e6d42c;
          }
          else {
            iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
            if (iVar8 == -1) {
              plVar30 = (long *)0x0;
              *(undefined8 *)param_1 = 0;
              goto joined_r0x00e6cea8;
            }
            plVar30 = *(long **)param_1;
            if (plVar28 != (long *)0x0) goto LAB_00e6ceac;
LAB_00e6cf08:
            if (plVar30 == (long *)0x0) goto LAB_00e6d42c;
            plVar28 = (long *)0x0;
          }
          plVar30 = *(long **)param_1;
          if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
            uVar10 = (**(code **)(*plVar30 + 0x48))();
          }
          else {
            uVar10 = (uint)*(byte *)plVar30[3];
          }
          if (((uVar10 >> 7 & 1) != 0) ||
             (((uint)*(undefined8 *)(*(long *)(param_8 + 0x10) + (ulong)(uVar10 & 0xff) * 8) >> 6 &
              1) == 0)) goto LAB_00e6d42c;
          pbVar13 = (byte *)*param_10;
          if (pbVar13 == (byte *)param_11) {
            uVar14 = (long)param_11 - (long)*(void **)param_9;
            sVar17 = uVar14 * 2;
            if (uVar14 == 0) {
              sVar17 = 1;
            }
            if (0x7ffffffffffffffe < uVar14) {
              sVar17 = 0xffffffffffffffff;
            }
            if (*(undefined **)(param_9 + 8) == PTR___do_nothing_01ff56a8) {
              pvVar11 = malloc(sVar17);
            }
            else {
              pvVar11 = realloc(*(void **)param_9,sVar17);
            }
            if (pvVar11 == (void *)0x0) goto LAB_00e6d4e8;
            *(void **)param_9 = pvVar11;
            *(undefined **)(param_9 + 8) = PTR_free_01ff56b0;
            pbVar13 = (byte *)((long)pvVar11 + uVar14);
            *param_10 = (char *)pbVar13;
            param_11 = (char *)(*(long *)param_9 + sVar17);
          }
          plVar30 = *(long **)param_1;
          if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
            bVar7 = (**(code **)(*plVar30 + 0x48))();
            pbVar13 = (byte *)*param_10;
          }
          else {
            bVar7 = *(byte *)plVar30[3];
          }
          *param_10 = (char *)(pbVar13 + 1);
          *pbVar13 = bVar7;
          local_28c = local_28c + -1;
          plVar30 = *(long **)param_1;
          if (plVar30[3] != plVar30[4]) goto LAB_00e6ce84;
          (**(code **)(*plVar30 + 0x50))();
          if (local_28c < 1) break;
        } while( true );
      }
      goto LAB_00e6ce68;
    }
    goto LAB_00e6d42c;
  }
LAB_00e6ce68:
  if (*param_10 == *(char **)param_9) goto LAB_00e6d42c;
  goto switchD_00e6c55c_caseD_5;
LAB_00e6ce84:
  plVar30[3] = plVar30[3] + 1;
  goto joined_r0x00e6ce64;
LAB_00e6d1b8:
  if (local_2c8 != (ulong *)0x0) {
    uVar29 = 1;
LAB_00e6d1d4:
    if ((*(byte *)local_2c8 & 1) == 0) {
      uVar14 = (ulong)(*(byte *)local_2c8 >> 1);
    }
    else {
      uVar14 = local_2c8[1];
    }
    if (uVar14 <= uVar29) goto LAB_00e6d2dc;
    plVar30 = *(long **)param_1;
    if ((plVar30 == (long *)0x0) || (plVar30[3] != plVar30[4])) {
joined_r0x00e6d210:
      if (plVar28 == (long *)0x0) goto LAB_00e6d270;
LAB_00e6d214:
                    /* try { // try from 00e6d228 to 00e6d2d7 has its CatchHandler @ 00e6d52c */
      if ((plVar28[3] == plVar28[4]) &&
         (iVar8 = (**(code **)(*plVar28 + 0x48))(plVar28), iVar8 == -1)) goto LAB_00e6d270;
      if (plVar30 != (long *)0x0) goto LAB_00e6d42c;
    }
    else {
      iVar8 = (**(code **)(*plVar30 + 0x48))(plVar30);
      if (iVar8 == -1) {
        plVar30 = (long *)0x0;
        *(undefined8 *)param_1 = 0;
        goto joined_r0x00e6d210;
      }
      plVar30 = *(long **)param_1;
      if (plVar28 != (long *)0x0) goto LAB_00e6d214;
LAB_00e6d270:
      if (plVar30 == (long *)0x0) goto LAB_00e6d42c;
      plVar28 = (long *)0x0;
    }
    plVar30 = *(long **)param_1;
    if ((byte *)plVar30[3] == (byte *)plVar30[4]) {
      bVar7 = (**(code **)(*plVar30 + 0x48))();
    }
    else {
      bVar7 = *(byte *)plVar30[3];
    }
    pbVar19 = (byte *)((long)local_2c8 + 1);
    if ((*(byte *)local_2c8 & 1) != 0) {
      pbVar19 = (byte *)local_2c8[2];
    }
    if (pbVar19[uVar29] != bVar7) goto LAB_00e6d42c;
    plVar30 = *(long **)param_1;
    uVar29 = (ulong)((int)uVar29 + 1);
    if (plVar30[3] == plVar30[4]) {
      (**(code **)(*plVar30 + 0x50))();
    }
    else {
      plVar30[3] = plVar30[3] + 1;
    }
    goto LAB_00e6d1d4;
  }
LAB_00e6d2dc:
  if (__ptr == plVar15) {
    uVar27 = 1;
    __ptr = plVar15;
  }
  else {
    uVar29 = (ulong)((byte)local_228 >> 1);
    if ((local_228 & 1) != 0) {
      uVar29 = local_220;
    }
    if ((uVar29 != 0) && (4 < (long)plVar15 - (long)__ptr)) {
      plVar15 = (long *)((long)plVar15 + -4);
      plVar30 = plVar15;
      plVar28 = __ptr;
      if (__ptr < plVar15) {
        do {
          plVar18 = (long *)((long)plVar28 + 4);
          iVar8 = *(int *)plVar28;
          *(int *)plVar28 = *(int *)plVar30;
          plVar20 = (long *)((long)plVar30 + -4);
          *(int *)plVar30 = iVar8;
          plVar30 = plVar20;
          plVar28 = plVar18;
        } while (plVar18 < plVar20);
        pbVar13 = (byte *)((ulong)&local_228 | 1);
        if ((local_228 & 1) != 0) {
          pbVar13 = local_218;
        }
        pbVar19 = pbVar13;
        if (__ptr < plVar15) {
          plVar28 = __ptr;
          uVar29 = (ulong)((byte)local_228 >> 1);
          if ((local_228 & 1) != 0) {
            uVar29 = local_220;
          }
          do {
            bVar7 = *pbVar19;
            if (((bVar7 != 0) && (bVar7 != 0xff)) && (*(uint *)plVar28 != (uint)bVar7))
            goto LAB_00e6d42c;
            plVar28 = (long *)((long)plVar28 + 4);
            if (1 < (long)(pbVar13 + (uVar29 - (long)pbVar19))) {
              pbVar19 = pbVar19 + 1;
            }
          } while (plVar28 < plVar15);
        }
      }
      else {
        pbVar19 = (byte *)((ulong)&local_228 | 1);
        if ((local_228 & 1) != 0) {
          pbVar19 = local_218;
        }
      }
      bVar7 = *pbVar19;
      if (((bVar7 != 0) && (bVar7 != 0xff)) && ((uint)bVar7 <= *(int *)plVar15 - 1U)) {
LAB_00e6d42c:
        uVar27 = 0;
        *param_6 = *param_6 | 4;
        goto joined_r0x00e6d3b8;
      }
    }
    uVar27 = 1;
  }
joined_r0x00e6d3b8:
  if ((local_288 & 1) != 0) {
    operator_delete(local_278);
  }
  if ((local_270 & 1) != 0) {
    operator_delete(local_260);
  }
  if ((local_258 & 1) != 0) {
    operator_delete(local_248);
  }
  if ((local_240 & 1) != 0) {
    operator_delete(local_230);
  }
  if ((local_228 & 1) != 0) {
    operator_delete(local_218);
  }
  if (__ptr != (long *)0x0) {
                    /* try { // try from 00e6d494 to 00e6d49f has its CatchHandler @ 00e6d4fc */
    (*local_2a8)(__ptr);
  }
  if (*(long *)(lVar3 + 0x28) == local_70[0]) {
    return uVar27;
  }
LAB_00e6d4f8:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __throw_runtime_error
// Address: 00e6d5ec
// ==========================================================================================

/* std::__ndk1::__throw_runtime_error(char const*) */

void std::__ndk1::__throw_runtime_error(char *param_1)

{
  runtime_error *this;
  
  this = (runtime_error *)__cxa_allocate_exception(0x10);
                    /* try { // try from 00e6d60c to 00e6d613 has its CatchHandler @ 00e6d62c */
  runtime_error::runtime_error(this,param_1);
                    /* WARNING: Subroutine does not return */
  __cxa_throw(this,PTR_PTR_01ff56b8,PTR__runtime_error_01ff56c0);
}



// ==========================================================================================
// Function: __gather_info
// Address: 00e6d91c
// ==========================================================================================

/* std::__ndk1::__money_get<char>::__gather_info(bool, std::__ndk1::locale const&,
   std::__ndk1::money_base::pattern&, char&, char&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, int&) */

void std::__ndk1::__money_get<char>::__gather_info
               (bool param_1,locale *param_2,pattern *param_3,char *param_4,char *param_5,
               basic_string *param_6,basic_string *param_7,basic_string *param_8,
               basic_string *param_9,int *param_10)

{
  long lVar1;
  ulong *puVar2;
  char cVar3;
  undefined4 uVar4;
  int iVar5;
  long lVar6;
  long lVar7;
  long *plVar8;
  ulong *local_90;
  undefined *puStack_88;
  undefined8 local_80;
  ulong ***local_78;
  ulong **local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  lVar7 = *(long *)param_2;
  if (param_1) {
    lVar6 = *(long *)PTR_id_01ff56c8;
    puVar2 = (ulong *)PTR_id_01ff56c8;
  }
  else {
    lVar6 = *(long *)PTR_id_01ff56d0;
    puVar2 = (ulong *)PTR_id_01ff56d0;
  }
  puStack_88 = PTR___init_01ff5688;
  local_80 = 0;
  local_90 = puVar2;
  if (lVar6 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    local_80 = 0;
    __call_once(puVar2,&local_78,FUN_00e87ff8);
  }
  lVar6 = *(long *)(lVar7 + 0x10);
  if (((ulong)(*(long *)(lVar7 + 0x18) - lVar6 >> 3) <= (long)*(int *)(puVar2 + 1) - 1U) ||
     (plVar8 = *(long **)(lVar6 + ((long)*(int *)(puVar2 + 1) - 1U) * 8), plVar8 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00de5da0();
  }
  uVar4 = (**(code **)(*plVar8 + 0x58))(plVar8);
  *(undefined4 *)param_3 = uVar4;
  (**(code **)(*plVar8 + 0x40))(&local_90,plVar8);
  if (((byte)*param_9 & 1) != 0) {
    operator_delete(*(void **)(param_9 + 0x10));
  }
  *(undefined8 *)(param_9 + 0x10) = local_80;
  *(undefined **)(param_9 + 8) = puStack_88;
  *(ulong **)param_9 = local_90;
  (**(code **)(*plVar8 + 0x38))(&local_90,plVar8);
  if (((byte)*param_8 & 1) != 0) {
    operator_delete(*(void **)(param_8 + 0x10));
  }
  *(undefined8 *)(param_8 + 0x10) = local_80;
  *(undefined **)(param_8 + 8) = puStack_88;
  *(ulong **)param_8 = local_90;
  cVar3 = (**(code **)(*plVar8 + 0x18))(plVar8);
  *param_4 = cVar3;
  cVar3 = (**(code **)(*plVar8 + 0x20))(plVar8);
  *param_5 = cVar3;
  (**(code **)(*plVar8 + 0x28))(&local_90,plVar8);
  if (((byte)*param_6 & 1) != 0) {
    operator_delete(*(void **)(param_6 + 0x10));
  }
  *(undefined8 *)(param_6 + 0x10) = local_80;
  *(undefined **)(param_6 + 8) = puStack_88;
  *(ulong **)param_6 = local_90;
  (**(code **)(*plVar8 + 0x30))(&local_90,plVar8);
  if (((byte)*param_7 & 1) != 0) {
    operator_delete(*(void **)(param_7 + 0x10));
  }
  *(undefined8 *)(param_7 + 0x10) = local_80;
  *(undefined **)(param_7 + 8) = puStack_88;
  *(ulong **)param_7 = local_90;
  iVar5 = (**(code **)(*plVar8 + 0x48))(plVar8);
  *param_10 = iVar5;
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __check_grouping
// Address: 00e6db7c
// ==========================================================================================

/* std::__ndk1::__check_grouping(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, unsigned int*, unsigned int*, unsigned int&) */

void std::__ndk1::__check_grouping(basic_string *param_1,uint *param_2,uint *param_3,uint *param_4)

{
  ulong uVar1;
  uint uVar2;
  basic_string bVar3;
  bool bVar4;
  uint *puVar5;
  ulong uVar6;
  uint *puVar7;
  uint *puVar8;
  basic_string *pbVar9;
  basic_string *pbVar10;
  byte bVar11;
  
  bVar3 = *param_1;
  uVar6 = (ulong)(byte)bVar3;
  bVar11 = (byte)bVar3 & 1;
  uVar1 = (ulong)((byte)bVar3 >> 1);
  if (((byte)bVar3 & 1) != 0) {
    uVar1 = *(ulong *)(param_1 + 8);
  }
  if ((uVar1 != 0) && (4 < (long)param_3 - (long)param_2)) {
    puVar5 = param_3 + -1;
    if ((param_2 != param_3) && (param_2 < puVar5)) {
      puVar7 = param_2 + 1;
      puVar8 = puVar5;
      do {
        uVar2 = puVar7[-1];
        puVar7[-1] = *puVar8;
        *puVar8 = uVar2;
        bVar4 = puVar7 < puVar8 + -1;
        puVar7 = puVar7 + 1;
        puVar8 = puVar8 + -1;
      } while (bVar4);
      uVar6 = (ulong)(byte)*param_1;
      bVar11 = (byte)*param_1 & 1;
    }
    pbVar9 = *(basic_string **)(param_1 + 0x10);
    if (bVar11 == 0) {
      pbVar9 = param_1 + 1;
    }
    pbVar10 = pbVar9;
    if (param_2 < puVar5) {
      uVar1 = uVar6 >> 1;
      if (bVar11 != 0) {
        uVar1 = *(ulong *)(param_1 + 8);
      }
      do {
        bVar3 = *pbVar10;
        if (((bVar3 != (basic_string)0x0) && (bVar3 != (basic_string)0xff)) &&
           (*param_2 != (uint)(byte)bVar3)) goto LAB_00e6dc68;
        param_2 = param_2 + 1;
        if (1 < (long)(pbVar9 + (uVar1 - (long)pbVar10))) {
          pbVar10 = pbVar10 + 1;
        }
      } while (param_2 < puVar5);
    }
    bVar3 = *pbVar10;
    if (((bVar3 != (basic_string)0x0) && (bVar3 != (basic_string)0xff)) &&
       ((uint)(byte)bVar3 <= *puVar5 - 1)) {
LAB_00e6dc68:
      *param_4 = 4;
    }
  }
  return;
}



// ==========================================================================================
// Function: __do_get
// Address: 00e6e0a8
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* std::__ndk1::money_get<wchar_t, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> > >::__do_get(std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >&, std::__ndk1::istreambuf_iterator<wchar_t,
   std::__ndk1::char_traits<wchar_t> >, bool, std::__ndk1::locale const&, unsigned int, unsigned
   int&, bool&, std::__ndk1::ctype<wchar_t> const&, std::__ndk1::unique_ptr<wchar_t, void
   (*)(void*)>&, wchar_t*&, wchar_t*) */

undefined4
std::__ndk1::
money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get(istreambuf_iterator *param_1,istreambuf_iterator param_2,bool param_3,locale *param_4,
        uint param_5,uint *param_6,bool *param_7,ctype *param_8,unique_ptr *param_9,
        wchar_t **param_10,wchar_t *param_11)

{
  ulong uVar1;
  byte *pbVar2;
  size_t sVar3;
  long lVar4;
  ulong *puVar5;
  bool bVar6;
  undefined uVar7;
  bool bVar8;
  int iVar9;
  undefined4 uVar10;
  wchar_t wVar11;
  int iVar12;
  long *plVar13;
  long *plVar14;
  void *pvVar15;
  wchar_t *pwVar16;
  int *piVar17;
  ulong uVar18;
  byte *pbVar19;
  byte bVar20;
  int *piVar21;
  int *piVar22;
  ulong uVar23;
  long *plVar24;
  long *plVar25;
  int *piVar26;
  ulong uVar27;
  ulong uVar28;
  void *pvVar29;
  void *pvVar30;
  long lVar31;
  long *plVar32;
  int *piVar33;
  ulong uVar34;
  ulong *local_2c8;
  code *local_2b8;
  long *local_2a8;
  long *local_298;
  int local_28c;
  undefined8 local_288;
  ulong local_280;
  void *local_278;
  ulong local_270;
  ulong local_268;
  int *local_260;
  ulong local_258;
  ulong local_250;
  int *local_248;
  ulong local_240;
  ulong local_238;
  int *local_230;
  ulong local_228;
  ulong local_220;
  byte *local_218;
  wchar_t local_210;
  wchar_t local_20c;
  pattern local_208 [3];
  char local_205;
  long local_200 [50];
  long local_70 [2];
  
  plVar32 = (long *)(ulong)param_2;
  lVar4 = tpidr_el0;
  local_70[0] = *(long *)(lVar4 + 0x28);
  local_228 = 0;
  local_220 = 0;
  local_218 = (byte *)0x0;
  local_240 = 0;
  local_238 = 0;
  local_230 = (int *)0x0;
  local_258 = 0;
  local_250 = 0;
  local_248 = (int *)0x0;
  local_270 = 0;
  local_268 = 0;
  local_260 = (int *)0x0;
  local_288 = 0;
  local_280 = 0;
  local_278 = (void *)0x0;
                    /* try { // try from 00e6e11c to 00e6e153 has its CatchHandler @ 00e6f2fc */
  __money_get<wchar_t>::__gather_info
            (param_3,param_4,local_208,&local_20c,&local_210,(basic_string *)&local_228,
             (basic_string *)&local_240,(basic_string *)&local_258,(basic_string *)&local_270,
             &local_28c);
  piVar21 = (int *)((ulong)&local_240 | 4);
  piVar22 = (int *)((ulong)&local_270 | 4);
  local_2c8 = (ulong *)0x0;
  local_2a8 = local_200;
  local_298 = local_70;
  uVar34 = 0;
  plVar14 = local_200;
  local_2b8 = (code *)PTR___do_nothing_01ff56a8;
  *param_10 = *(wchar_t **)param_9;
LAB_00e6e1e4:
  plVar13 = *(long **)param_1;
  if (plVar13 == (long *)0x0) {
LAB_00e6e22c:
    bVar6 = true;
    if (plVar32 == (long *)0x0) goto LAB_00e6e268;
LAB_00e6e234:
    if ((int *)plVar32[3] == (int *)plVar32[4]) {
      iVar12 = (**(code **)(*plVar32 + 0x48))(plVar32);
    }
    else {
      iVar12 = *(int *)plVar32[3];
    }
    if (iVar12 == -1) goto LAB_00e6e268;
    if (!bVar6) goto LAB_00e6efa4;
  }
  else {
    if ((int *)plVar13[3] == (int *)plVar13[4]) {
                    /* try { // try from 00e6e208 to 00e6e257 has its CatchHandler @ 00e6f32c */
      iVar12 = (**(code **)(*plVar13 + 0x48))();
    }
    else {
      iVar12 = *(int *)plVar13[3];
    }
    if (iVar12 == -1) {
      *(undefined8 *)param_1 = 0;
      goto LAB_00e6e22c;
    }
    bVar6 = *(long *)param_1 == 0;
    if (plVar32 != (long *)0x0) goto LAB_00e6e234;
LAB_00e6e268:
    plVar32 = (long *)0x0;
    if (bVar6) goto LAB_00e6efa4;
  }
  puVar5 = local_2c8;
  switch(local_208[uVar34]) {
  case (pattern)0x0:
    if (uVar34 != 3) goto LAB_00e6e738;
    goto LAB_00e6efa4;
  case (pattern)0x1:
    if (uVar34 != 3) {
      plVar13 = *(long **)param_1;
      if ((undefined4 *)plVar13[3] == (undefined4 *)plVar13[4]) {
                    /* try { // try from 00e6e6c8 to 00e6e6e3 has its CatchHandler @ 00e6f32c */
        uVar10 = (**(code **)(*plVar13 + 0x48))();
      }
      else {
        uVar10 = *(undefined4 *)plVar13[3];
      }
      uVar18 = (**(code **)(*(long *)param_8 + 0x18))(param_8,1,uVar10);
      if ((uVar18 & 1) != 0) {
        plVar13 = *(long **)param_1;
        pwVar16 = (wchar_t *)plVar13[3];
        if (pwVar16 == (wchar_t *)plVar13[4]) {
                    /* try { // try from 00e6e710 to 00e6e71f has its CatchHandler @ 00e6f314 */
          wVar11 = (**(code **)(*plVar13 + 0x50))();
        }
        else {
          plVar13[3] = (long)(pwVar16 + 1);
          wVar11 = *pwVar16;
        }
        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
        push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                   *)&local_288,wVar11);
LAB_00e6e738:
        do {
          plVar13 = *(long **)param_1;
          if (plVar13 == (long *)0x0) {
LAB_00e6e780:
            bVar6 = true;
            if (plVar32 == (long *)0x0) goto LAB_00e6e7bc;
LAB_00e6e788:
            if ((int *)plVar32[3] == (int *)plVar32[4]) {
              iVar12 = (**(code **)(*plVar32 + 0x48))(plVar32);
            }
            else {
              iVar12 = *(int *)plVar32[3];
            }
            if (iVar12 == -1) goto LAB_00e6e7bc;
            if (!bVar6) goto switchD_00e6e294_caseD_5;
          }
          else {
            if ((int *)plVar13[3] == (int *)plVar13[4]) {
                    /* try { // try from 00e6e75c to 00e6e7ff has its CatchHandler @ 00e6f344 */
              iVar12 = (**(code **)(*plVar13 + 0x48))();
            }
            else {
              iVar12 = *(int *)plVar13[3];
            }
            if (iVar12 == -1) {
              *(undefined8 *)param_1 = 0;
              goto LAB_00e6e780;
            }
            bVar6 = *(long *)param_1 == 0;
            if (plVar32 != (long *)0x0) goto LAB_00e6e788;
LAB_00e6e7bc:
            plVar32 = (long *)0x0;
            if (bVar6) goto switchD_00e6e294_caseD_5;
          }
          plVar13 = *(long **)param_1;
          if ((undefined4 *)plVar13[3] == (undefined4 *)plVar13[4]) {
            uVar10 = (**(code **)(*plVar13 + 0x48))();
          }
          else {
            uVar10 = *(undefined4 *)plVar13[3];
          }
          uVar18 = (**(code **)(*(long *)param_8 + 0x18))(param_8,1,uVar10);
          if ((uVar18 & 1) == 0) goto switchD_00e6e294_caseD_5;
          plVar13 = *(long **)param_1;
          pwVar16 = (wchar_t *)plVar13[3];
          if (pwVar16 == (wchar_t *)plVar13[4]) {
                    /* try { // try from 00e6e81c to 00e6e823 has its CatchHandler @ 00e6f340 */
            wVar11 = (**(code **)(*plVar13 + 0x50))();
          }
          else {
            plVar13[3] = (long)(pwVar16 + 1);
            wVar11 = *pwVar16;
          }
                    /* try { // try from 00e6e730 to 00e6e737 has its CatchHandler @ 00e6f340 */
          basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
          push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                     *)&local_288,wVar11);
        } while( true );
      }
      goto LAB_00e6f0e4;
    }
    goto LAB_00e6efa4;
  case (pattern)0x2:
    if ((uVar34 < 2) || (local_2c8 != (ulong *)0x0)) {
      bVar6 = (local_240 & 1) == 0;
      piVar17 = piVar21;
      if (!bVar6) {
        piVar17 = local_230;
      }
      piVar26 = piVar17;
      if (uVar34 != 0) goto LAB_00e6e644;
LAB_00e6e6b8:
      bVar20 = (byte)local_240 & 1;
      uVar18 = local_240 & 0xff;
      piVar33 = piVar17;
    }
    else {
      if (((uint)(uVar34 == 2 && local_205 != '\0') | param_5 >> 9 & 1) != 1) {
        local_2c8 = (ulong *)0x0;
        puVar5 = local_2c8;
        break;
      }
      bVar6 = (local_240 & 1) == 0;
      piVar26 = piVar21;
      if (!bVar6) {
        piVar26 = local_230;
      }
LAB_00e6e644:
      bVar20 = (byte)local_240 & 1;
      uVar18 = local_240 & 0xff;
      piVar17 = piVar26;
      if (1 < (byte)local_208[(int)uVar34 - 1]) goto LAB_00e6e6b8;
      uVar23 = uVar18 >> 1;
      if (!bVar6) {
        uVar23 = local_238;
      }
      if (uVar23 != 0) {
        do {
                    /* try { // try from 00e6e678 to 00e6e683 has its CatchHandler @ 00e6f320 */
          uVar18 = (**(code **)(*(long *)param_8 + 0x18))(param_8,1,*piVar26);
          if ((uVar18 & 1) == 0) {
            uVar18 = local_240 & 0xff;
            bVar20 = (byte)local_240 & 1;
            break;
          }
          uVar18 = local_240 & 0xff;
          piVar26 = piVar26 + 1;
          bVar20 = (byte)local_240 & 1;
          uVar23 = (ulong)((byte)local_240 >> 1);
          piVar17 = piVar21;
          if ((local_240 & 1) != 0) {
            uVar23 = local_238;
            piVar17 = local_230;
          }
        } while (piVar26 != piVar17 + uVar23);
      }
      piVar17 = piVar21;
      if (bVar20 != 0) {
        piVar17 = local_230;
      }
      uVar23 = (long)piVar26 - (long)piVar17;
      uVar28 = (long)uVar23 >> 2;
      piVar33 = piVar17;
      if ((local_288 & 1) == 0) {
        uVar27 = local_288 >> 1 & 0x7f;
        if (uVar28 <= uVar27) {
          pvVar15 = (void *)((long)&local_288 + uVar27 * 4 + 4);
          pvVar30 = (void *)((ulong)&local_288 | 4);
LAB_00e6e964:
          pvVar29 = (void *)((long)pvVar15 + uVar28 * -4);
          piVar33 = piVar26;
          if (pvVar29 != (void *)((long)pvVar30 + uVar27 * 4)) {
            uVar28 = uVar23;
            if ((long)uVar23 < 0) {
              uVar28 = 0xffffffffffffffff;
            }
            if (0 < (long)uVar28) {
              uVar28 = 1;
            }
            uVar1 = (long)piVar17 - (long)piVar26;
            if ((long)piVar17 - (long)piVar26 <= (long)uVar23) {
              uVar1 = uVar23;
            }
            lVar31 = 0;
            do {
              piVar33 = piVar17;
              if (*(int *)((long)pvVar29 + lVar31) != *(int *)((long)piVar17 + lVar31)) break;
              lVar31 = lVar31 + 4;
              piVar33 = piVar26;
            } while ((long)pvVar30 + ((uVar27 + uVar28 * (uVar1 >> 2)) * 4 - (long)pvVar15) !=
                     lVar31);
          }
        }
      }
      else if (uVar28 <= local_280) {
        pvVar15 = (void *)((long)local_278 + local_280 * 4);
        uVar27 = local_280;
        pvVar30 = local_278;
        goto LAB_00e6e964;
      }
    }
    uVar18 = uVar18 >> 1;
    if (bVar20 != 0) {
      uVar18 = local_238;
    }
    for (piVar17 = piVar17 + uVar18; piVar33 != piVar17; piVar17 = piVar17 + uVar18) {
      plVar13 = *(long **)param_1;
      if (plVar13 == (long *)0x0) {
LAB_00e6ea54:
        bVar6 = true;
        if (plVar32 == (long *)0x0) goto LAB_00e6ea90;
LAB_00e6ea5c:
        if ((int *)plVar32[3] == (int *)plVar32[4]) {
          iVar12 = (**(code **)(*plVar32 + 0x48))(plVar32);
        }
        else {
          iVar12 = *(int *)plVar32[3];
        }
        if (iVar12 == -1) goto LAB_00e6ea90;
        if (!bVar6) break;
      }
      else {
        if ((int *)plVar13[3] == (int *)plVar13[4]) {
                    /* try { // try from 00e6ea30 to 00e6eabb has its CatchHandler @ 00e6f328 */
          iVar12 = (**(code **)(*plVar13 + 0x48))();
        }
        else {
          iVar12 = *(int *)plVar13[3];
        }
        if (iVar12 == -1) {
          *(undefined8 *)param_1 = 0;
          goto LAB_00e6ea54;
        }
        bVar6 = *(long *)param_1 == 0;
        if (plVar32 != (long *)0x0) goto LAB_00e6ea5c;
LAB_00e6ea90:
        plVar32 = (long *)0x0;
        if (bVar6) break;
      }
      plVar13 = *(long **)param_1;
      if ((int *)plVar13[3] == (int *)plVar13[4]) {
        iVar12 = (**(code **)(*plVar13 + 0x48))();
      }
      else {
        iVar12 = *(int *)plVar13[3];
      }
      if (iVar12 != *piVar33) break;
      plVar13 = *(long **)param_1;
      if (plVar13[3] == plVar13[4]) {
                    /* try { // try from 00e6eae4 to 00e6eae7 has its CatchHandler @ 00e6f31c */
        (**(code **)(*plVar13 + 0x50))();
      }
      else {
        plVar13[3] = plVar13[3] + 4;
      }
      piVar33 = piVar33 + 1;
      uVar18 = local_240 >> 1 & 0x7f;
      piVar17 = piVar21;
      if ((local_240 & 1) != 0) {
        uVar18 = local_238;
        piVar17 = local_230;
      }
    }
    if ((param_5 >> 9 & 1) == 0) break;
    uVar18 = local_240 >> 1 & 0x7f;
    piVar17 = piVar21;
    if ((local_240 & 1) != 0) {
      uVar18 = local_238;
      piVar17 = local_230;
    }
    if (piVar33 != piVar17 + uVar18) goto LAB_00e6f0e4;
    break;
  case (pattern)0x3:
    uVar23 = local_258 & 0xff;
    bVar20 = (byte)local_258 & 1;
    uVar18 = (ulong)((byte)local_258 >> 1);
    if ((local_258 & 1) != 0) {
      uVar18 = local_250;
    }
    uVar28 = (ulong)((byte)local_270 >> 1);
    if ((local_270 & 1) != 0) {
      uVar28 = local_268;
    }
    if (uVar18 + uVar28 != 0) {
      if (uVar18 == 0) {
        plVar13 = *(long **)param_1;
        if ((int *)plVar13[3] == (int *)plVar13[4]) {
          iVar12 = (**(code **)(*plVar13 + 0x48))();
        }
        else {
          iVar12 = *(int *)plVar13[3];
        }
        piVar17 = piVar22;
        if (((byte)local_270 & 1) != 0) {
          piVar17 = local_260;
        }
        if (iVar12 == *piVar17) {
          plVar13 = *(long **)param_1;
          if (plVar13[3] == plVar13[4]) {
            (**(code **)(*plVar13 + 0x50))();
            bVar20 = (byte)local_270;
          }
          else {
            plVar13[3] = plVar13[3] + 4;
            bVar20 = (byte)local_270;
          }
          *param_7 = true;
          uVar18 = (ulong)(bVar20 >> 1);
          if ((bVar20 & 1) != 0) {
            uVar18 = local_268;
          }
LAB_00e6ef54:
          puVar5 = &local_270;
          if (uVar18 < 2) {
            puVar5 = local_2c8;
          }
        }
      }
      else {
        plVar13 = *(long **)param_1;
        piVar17 = (int *)plVar13[3];
        if (uVar28 == 0) {
          if (piVar17 == (int *)plVar13[4]) {
                    /* try { // try from 00e6ee38 to 00e6ef73 has its CatchHandler @ 00e6f32c */
            iVar12 = (**(code **)(*plVar13 + 0x48))();
            uVar23 = local_258 & 0xff;
            bVar20 = (byte)local_258 & 1;
          }
          else {
            iVar12 = *piVar17;
          }
          piVar17 = (int *)((ulong)&local_258 | 4);
          if (bVar20 != 0) {
            piVar17 = local_248;
          }
          if (iVar12 != *piVar17) {
            *param_7 = true;
            break;
          }
          plVar13 = *(long **)param_1;
          if (plVar13[3] == plVar13[4]) {
            (**(code **)(*plVar13 + 0x50))();
            goto LAB_00e6ef74;
          }
          plVar13[3] = plVar13[3] + 4;
        }
        else {
          if (piVar17 == (int *)plVar13[4]) {
                    /* try { // try from 00e6e8b8 to 00e6e91b has its CatchHandler @ 00e6f32c */
            iVar12 = (**(code **)(*plVar13 + 0x48))();
            uVar23 = local_258 & 0xff;
            bVar20 = (byte)local_258 & 1;
          }
          else {
            iVar12 = *piVar17;
          }
          plVar13 = *(long **)param_1;
          piVar17 = (int *)((ulong)&local_258 | 4);
          if (bVar20 != 0) {
            piVar17 = local_248;
          }
          piVar26 = (int *)plVar13[3];
          if (iVar12 != *piVar17) {
            if (piVar26 == (int *)plVar13[4]) {
              iVar12 = (**(code **)(*plVar13 + 0x48))(plVar13);
            }
            else {
              iVar12 = *piVar26;
            }
            piVar17 = piVar22;
            if ((local_270 & 1) != 0) {
              piVar17 = local_260;
            }
            if (iVar12 == *piVar17) {
              plVar13 = *(long **)param_1;
              if (plVar13[3] == plVar13[4]) {
                (**(code **)(*plVar13 + 0x50))();
              }
              else {
                plVar13[3] = plVar13[3] + 4;
              }
              *param_7 = true;
              uVar18 = (ulong)((byte)local_270 >> 1);
              if (((byte)local_270 & 1) != 0) {
                uVar18 = local_268;
              }
              goto LAB_00e6ef54;
            }
            goto LAB_00e6f0e4;
          }
          if (piVar26 == (int *)plVar13[4]) {
            (**(code **)(*plVar13 + 0x50))(plVar13);
LAB_00e6ef74:
            uVar23 = local_258 & 0xff;
            bVar20 = (byte)local_258 & 1;
          }
          else {
            plVar13[3] = (long)(piVar26 + 1);
          }
        }
        uVar18 = uVar23 >> 1;
        if (bVar20 != 0) {
          uVar18 = local_250;
        }
        puVar5 = &local_258;
        if (uVar18 < 2) {
          puVar5 = local_2c8;
        }
      }
    }
    break;
  case (pattern)0x4:
    iVar12 = 0;
    plVar13 = plVar14;
LAB_00e6e2bc:
    plVar14 = *(long **)param_1;
    if (plVar14 == (long *)0x0) {
LAB_00e6e304:
      bVar6 = true;
      if (plVar32 == (long *)0x0) goto LAB_00e6e340;
LAB_00e6e30c:
      if ((int *)plVar32[3] == (int *)plVar32[4]) {
        iVar9 = (**(code **)(*plVar32 + 0x48))(plVar32);
      }
      else {
        iVar9 = *(int *)plVar32[3];
      }
      if (iVar9 == -1) goto LAB_00e6e340;
      if (!bVar6) goto LAB_00e6e5c4;
    }
    else {
      if ((int *)plVar14[3] == (int *)plVar14[4]) {
                    /* try { // try from 00e6e2e0 to 00e6e32f has its CatchHandler @ 00e6f338 */
        iVar9 = (**(code **)(*plVar14 + 0x48))();
      }
      else {
        iVar9 = *(int *)plVar14[3];
      }
      if (iVar9 == -1) {
        *(undefined8 *)param_1 = 0;
        goto LAB_00e6e304;
      }
      bVar6 = *(long *)param_1 == 0;
      if (plVar32 != (long *)0x0) goto LAB_00e6e30c;
LAB_00e6e340:
      plVar32 = (long *)0x0;
      if (bVar6) goto LAB_00e6e5c4;
    }
    plVar14 = *(long **)param_1;
    if ((wchar_t *)plVar14[3] == (wchar_t *)plVar14[4]) {
                    /* try { // try from 00e6e368 to 00e6e387 has its CatchHandler @ 00e6f33c */
      wVar11 = (**(code **)(*plVar14 + 0x48))();
    }
    else {
      wVar11 = *(wchar_t *)plVar14[3];
    }
    uVar18 = (**(code **)(*(long *)param_8 + 0x18))(param_8,0x40,wVar11);
    if ((uVar18 & 1) == 0) {
      uVar18 = local_228 >> 1 & 0x7f;
      if ((local_228 & 1) != 0) {
        uVar18 = local_220;
      }
      if (((wVar11 == local_210) && (iVar12 != 0)) && (uVar18 != 0)) {
        if (plVar13 != local_298) {
LAB_00e6e4cc:
          plVar14 = (long *)((long)plVar13 + 4);
          *(int *)plVar13 = iVar12;
          iVar12 = 0;
          goto LAB_00e6e4d4;
        }
        uVar18 = (long)local_298 - (long)local_2a8;
        sVar3 = 4;
        if (uVar18 != 0) {
          sVar3 = uVar18 * 2;
        }
        if (0x7ffffffffffffffe < uVar18) {
          sVar3 = 0xffffffffffffffff;
        }
        if (local_2b8 == (code *)PTR___do_nothing_01ff56a8) {
          local_2a8 = (long *)malloc(sVar3);
        }
        else {
          local_2a8 = (long *)realloc(local_2a8,sVar3);
        }
        if (local_2a8 != (long *)0x0) {
          local_298 = (long *)((long)local_2a8 + (sVar3 & 0xfffffffffffffffc));
          plVar13 = (long *)((long)local_2a8 + uVar18);
          local_2b8 = (code *)PTR_free_01ff56b0;
          goto LAB_00e6e4cc;
        }
LAB_00e6f2e4:
        __throw_bad_alloc();
LAB_00e6f2e8:
                    /* try { // try from 00e6f2e8 to 00e6f2ef has its CatchHandler @ 00e6f318 */
        __throw_bad_alloc();
        goto LAB_00e6f2ec;
      }
      goto LAB_00e6e5c4;
    }
    pwVar16 = *param_10;
    if (pwVar16 == param_11) {
      uVar18 = (long)param_11 - (long)*(void **)param_9;
      sVar3 = 4;
      if (uVar18 != 0) {
        sVar3 = uVar18 * 2;
      }
      if (0x7ffffffffffffffe < uVar18) {
        sVar3 = 0xffffffffffffffff;
      }
      if (*(undefined **)(param_9 + 8) == PTR___do_nothing_01ff56a8) {
        pvVar15 = malloc(sVar3);
      }
      else {
        pvVar15 = realloc(*(void **)param_9,sVar3);
      }
      if (pvVar15 == (void *)0x0) {
                    /* try { // try from 00e6f2e0 to 00e6f2e7 has its CatchHandler @ 00e6f330 */
        __throw_bad_alloc();
        goto LAB_00e6f2e4;
      }
      *(void **)param_9 = pvVar15;
      *(undefined **)(param_9 + 8) = PTR_free_01ff56b0;
      pwVar16 = (wchar_t *)((long)pvVar15 + uVar18);
      *param_10 = pwVar16;
      param_11 = (wchar_t *)(*(long *)param_9 + (sVar3 & 0xfffffffffffffffc));
    }
    *param_10 = pwVar16 + 1;
    *pwVar16 = wVar11;
    iVar12 = iVar12 + 1;
    plVar14 = plVar13;
LAB_00e6e4d4:
    plVar24 = *(long **)param_1;
    plVar13 = plVar14;
    if (plVar24[3] == plVar24[4]) {
                    /* try { // try from 00e6e4ec to 00e6e4ef has its CatchHandler @ 00e6f338 */
      (**(code **)(*plVar24 + 0x50))();
    }
    else {
      plVar24[3] = plVar24[3] + 4;
    }
    goto LAB_00e6e2bc;
  }
switchD_00e6e294_caseD_5:
  local_2c8 = puVar5;
  uVar34 = uVar34 + 1;
  if (uVar34 == 4) goto LAB_00e6efa4;
  goto LAB_00e6e1e4;
LAB_00e6e5c4:
  plVar14 = plVar13;
  if ((local_2a8 != plVar13) && (iVar12 != 0)) {
    if (plVar13 == local_298) {
      uVar18 = (long)local_298 - (long)local_2a8;
      sVar3 = 4;
      if (uVar18 != 0) {
        sVar3 = uVar18 * 2;
      }
      if (0x7ffffffffffffffe < uVar18) {
        sVar3 = 0xffffffffffffffff;
      }
      if (local_2b8 == (code *)PTR___do_nothing_01ff56a8) {
        local_2a8 = (long *)malloc(sVar3);
      }
      else {
        local_2a8 = (long *)realloc(local_2a8,sVar3);
      }
      if (local_2a8 == (long *)0x0) {
LAB_00e6f2ec:
        __throw_bad_alloc();
        goto LAB_00e6f2f0;
      }
      local_298 = (long *)((long)local_2a8 + (sVar3 & 0xfffffffffffffffc));
      plVar13 = (long *)((long)local_2a8 + uVar18);
      local_2b8 = (code *)PTR_free_01ff56b0;
    }
    plVar14 = (long *)((long)plVar13 + 4);
    *(int *)plVar13 = iVar12;
  }
  if (local_28c < 1) {
LAB_00e6e1c4:
    if (*param_10 == *(wchar_t **)param_9) goto LAB_00e6f0e4;
    goto switchD_00e6e294_caseD_5;
  }
  plVar13 = *(long **)param_1;
  if (plVar13 != (long *)0x0) {
    if ((int *)plVar13[3] == (int *)plVar13[4]) {
                    /* try { // try from 00e6eb84 to 00e6ec47 has its CatchHandler @ 00e6f2f8 */
      iVar12 = (**(code **)(*plVar13 + 0x48))();
    }
    else {
      iVar12 = *(int *)plVar13[3];
    }
    if (iVar12 != -1) {
      uVar7 = *(long *)param_1 == 0;
      goto joined_r0x00e6ebb4;
    }
    *(undefined8 *)param_1 = 0;
  }
  uVar7 = true;
joined_r0x00e6ebb4:
  if (plVar32 == (long *)0x0) {
    if ((bool)uVar7) goto LAB_00e6f0e4;
    plVar13 = (long *)0x0;
  }
  else {
    if ((int *)plVar32[3] == (int *)plVar32[4]) {
      iVar12 = (**(code **)(*plVar32 + 0x48))(plVar32);
    }
    else {
      iVar12 = *(int *)plVar32[3];
    }
    plVar13 = (long *)0x0;
    if (iVar12 != -1) {
      plVar13 = plVar32;
    }
    if ((bool)uVar7 == (iVar12 == -1)) goto LAB_00e6f0e4;
  }
  plVar32 = *(long **)param_1;
  if ((wchar_t *)plVar32[3] == (wchar_t *)plVar32[4]) {
    wVar11 = (**(code **)(*plVar32 + 0x48))();
  }
  else {
    wVar11 = *(wchar_t *)plVar32[3];
  }
  if (wVar11 == local_20c) {
    plVar24 = *(long **)param_1;
    plVar32 = plVar13;
    if (plVar24[3] == plVar24[4]) {
      (**(code **)(*plVar24 + 0x50))();
    }
    else {
      plVar24[3] = plVar24[3] + 4;
    }
joined_r0x00e6ec50:
    plVar13 = plVar32;
    if (0 < local_28c) {
      do {
        plVar32 = *(long **)param_1;
        if (plVar32 == (long *)0x0) {
LAB_00e6ecb8:
          bVar8 = true;
          bVar6 = true;
          if (plVar13 == (long *)0x0) goto LAB_00e6eca8;
LAB_00e6ecc0:
          if ((int *)plVar13[3] == (int *)plVar13[4]) {
            iVar12 = (**(code **)(*plVar13 + 0x48))(plVar13);
          }
          else {
            iVar12 = *(int *)plVar13[3];
          }
          plVar32 = (long *)0x0;
          if (iVar12 != -1) {
            plVar32 = plVar13;
          }
          if (bVar8 == (iVar12 == -1)) goto LAB_00e6f0e4;
        }
        else {
          if ((int *)plVar32[3] == (int *)plVar32[4]) {
                    /* try { // try from 00e6ec8c to 00e6ee1f has its CatchHandler @ 00e6f334 */
            iVar12 = (**(code **)(*plVar32 + 0x48))();
          }
          else {
            iVar12 = *(int *)plVar32[3];
          }
          if (iVar12 == -1) {
            *(undefined8 *)param_1 = 0;
            goto LAB_00e6ecb8;
          }
          bVar8 = *(long *)param_1 == 0;
          bVar6 = bVar8;
          if (plVar13 != (long *)0x0) goto LAB_00e6ecc0;
LAB_00e6eca8:
          if (bVar6) goto LAB_00e6f0e4;
          plVar32 = (long *)0x0;
        }
        plVar13 = *(long **)param_1;
        if ((undefined4 *)plVar13[3] == (undefined4 *)plVar13[4]) {
          uVar10 = (**(code **)(*plVar13 + 0x48))();
        }
        else {
          uVar10 = *(undefined4 *)plVar13[3];
        }
        uVar18 = (**(code **)(*(long *)param_8 + 0x18))(param_8,0x40,uVar10);
        if ((uVar18 & 1) == 0) goto LAB_00e6f0e4;
        pwVar16 = *param_10;
        if (pwVar16 == param_11) {
          uVar18 = (long)param_11 - (long)*(void **)param_9;
          sVar3 = 4;
          if (uVar18 != 0) {
            sVar3 = uVar18 * 2;
          }
          if (0x7ffffffffffffffe < uVar18) {
            sVar3 = 0xffffffffffffffff;
          }
          if (*(undefined **)(param_9 + 8) == PTR___do_nothing_01ff56a8) {
            pvVar15 = malloc(sVar3);
          }
          else {
            pvVar15 = realloc(*(void **)param_9,sVar3);
          }
          if (pvVar15 == (void *)0x0) goto LAB_00e6f2e8;
          *(void **)param_9 = pvVar15;
          *(undefined **)(param_9 + 8) = PTR_free_01ff56b0;
          pwVar16 = (wchar_t *)((long)pvVar15 + uVar18);
          *param_10 = pwVar16;
          param_11 = (wchar_t *)(*(long *)param_9 + (sVar3 & 0xfffffffffffffffc));
        }
        plVar13 = *(long **)param_1;
        if ((wchar_t *)plVar13[3] == (wchar_t *)plVar13[4]) {
          wVar11 = (**(code **)(*plVar13 + 0x48))();
          pwVar16 = *param_10;
        }
        else {
          wVar11 = *(wchar_t *)plVar13[3];
        }
        *param_10 = pwVar16 + 1;
        *pwVar16 = wVar11;
        local_28c = local_28c + -1;
        plVar13 = *(long **)param_1;
        if (plVar13[3] == plVar13[4]) goto code_r0x00e6ee14;
        plVar13[3] = plVar13[3] + 4;
        plVar13 = plVar32;
        if (local_28c < 1) break;
      } while( true );
    }
    goto LAB_00e6e1c4;
  }
  goto LAB_00e6f0e4;
code_r0x00e6ee14:
  (**(code **)(*plVar13 + 0x50))();
  goto joined_r0x00e6ec50;
LAB_00e6efa4:
  if (local_2c8 != (ulong *)0x0) {
    uVar34 = 1;
LAB_00e6efc0:
    if ((*(byte *)local_2c8 & 1) == 0) {
      uVar18 = (ulong)(*(byte *)local_2c8 >> 1);
    }
    else {
      uVar18 = local_2c8[1];
    }
    if (uVar18 <= uVar34) goto LAB_00e6f1b8;
    plVar13 = *(long **)param_1;
    if (plVar13 == (long *)0x0) {
LAB_00e6f038:
      bVar8 = true;
      bVar6 = true;
      if (plVar32 == (long *)0x0) goto LAB_00e6f028;
LAB_00e6f040:
      if ((int *)plVar32[3] == (int *)plVar32[4]) {
        iVar12 = (**(code **)(*plVar32 + 0x48))(plVar32);
      }
      else {
        iVar12 = *(int *)plVar32[3];
      }
      plVar13 = (long *)0x0;
      if (iVar12 != -1) {
        plVar13 = plVar32;
      }
      if (bVar8 == (iVar12 == -1)) goto LAB_00e6f0e4;
    }
    else {
      if ((int *)plVar13[3] == (int *)plVar13[4]) {
                    /* try { // try from 00e6f00c to 00e6f0d7 has its CatchHandler @ 00e6f324 */
        iVar12 = (**(code **)(*plVar13 + 0x48))();
      }
      else {
        iVar12 = *(int *)plVar13[3];
      }
      if (iVar12 == -1) {
        *(undefined8 *)param_1 = 0;
        goto LAB_00e6f038;
      }
      bVar8 = *(long *)param_1 == 0;
      bVar6 = bVar8;
      if (plVar32 != (long *)0x0) goto LAB_00e6f040;
LAB_00e6f028:
      if (bVar6) goto LAB_00e6f0e4;
      plVar13 = (long *)0x0;
    }
    plVar32 = *(long **)param_1;
    if ((int *)plVar32[3] == (int *)plVar32[4]) {
      iVar12 = (**(code **)(*plVar32 + 0x48))();
    }
    else {
      iVar12 = *(int *)plVar32[3];
    }
    pbVar19 = (byte *)((long)local_2c8 + 4);
    if ((*(byte *)local_2c8 & 1) != 0) {
      pbVar19 = (byte *)local_2c8[2];
    }
    if (iVar12 != *(int *)(pbVar19 + uVar34 * 4)) goto LAB_00e6f0e4;
    plVar24 = *(long **)param_1;
    uVar34 = (ulong)((int)uVar34 + 1);
    plVar32 = plVar13;
    if (plVar24[3] == plVar24[4]) {
      (**(code **)(*plVar24 + 0x50))();
    }
    else {
      plVar24[3] = plVar24[3] + 4;
    }
    goto LAB_00e6efc0;
  }
LAB_00e6f1b8:
  if (local_2a8 == plVar14) {
    uVar10 = 1;
    goto LAB_00e6f0f4;
  }
  uVar34 = (ulong)((byte)local_228 >> 1);
  if ((local_228 & 1) != 0) {
    uVar34 = local_220;
  }
  if ((uVar34 != 0) && (4 < (long)plVar14 - (long)local_2a8)) {
    plVar13 = (long *)((long)plVar14 + -4);
    plVar32 = plVar13;
    plVar14 = local_2a8;
    if (local_2a8 < plVar13) {
      do {
        plVar24 = (long *)((long)plVar14 + 4);
        iVar12 = *(int *)plVar14;
        *(int *)plVar14 = *(int *)plVar32;
        plVar25 = (long *)((long)plVar32 + -4);
        *(int *)plVar32 = iVar12;
        plVar32 = plVar25;
        plVar14 = plVar24;
      } while (plVar24 < plVar25);
      pbVar2 = (byte *)((ulong)&local_228 | 1);
      if ((local_228 & 1) != 0) {
        pbVar2 = local_218;
      }
      pbVar19 = pbVar2;
      if (local_2a8 < plVar13) {
        plVar14 = local_2a8;
        uVar34 = (ulong)((byte)local_228 >> 1);
        if ((local_228 & 1) != 0) {
          uVar34 = local_220;
        }
        do {
          bVar20 = *pbVar19;
          if (((bVar20 != 0) && (bVar20 != 0xff)) && (*(uint *)plVar14 != (uint)bVar20))
          goto LAB_00e6f0e4;
          plVar14 = (long *)((long)plVar14 + 4);
          if (1 < (long)(pbVar2 + (uVar34 - (long)pbVar19))) {
            pbVar19 = pbVar19 + 1;
          }
        } while (plVar14 < plVar13);
      }
    }
    else {
      pbVar19 = (byte *)((ulong)&local_228 | 1);
      if ((local_228 & 1) != 0) {
        pbVar19 = local_218;
      }
    }
    bVar20 = *pbVar19;
    uVar10 = 1;
    plVar14 = local_2a8;
    if ((bVar20 == 0) || (bVar20 == 0xff)) goto LAB_00e6f0f4;
    if ((uint)bVar20 <= *(int *)plVar13 - 1U) {
LAB_00e6f0e4:
      uVar10 = 0;
      *param_6 = *param_6 | 4;
      plVar14 = local_2a8;
      goto LAB_00e6f0f4;
    }
  }
  uVar10 = 1;
  plVar14 = local_2a8;
LAB_00e6f0f4:
  if ((local_288 & 1) != 0) {
    operator_delete(local_278);
  }
  if ((local_270 & 1) != 0) {
    operator_delete(local_260);
  }
  if ((local_258 & 1) != 0) {
    operator_delete(local_248);
  }
  if ((local_240 & 1) != 0) {
    operator_delete(local_230);
  }
  if ((local_228 & 1) != 0) {
    operator_delete(local_218);
  }
  if (plVar14 != (long *)0x0) {
                    /* try { // try from 00e6f170 to 00e6f17b has its CatchHandler @ 00e6f2f4 */
    (*local_2b8)(plVar14);
  }
  if (*(long *)(lVar4 + 0x28) == local_70[0]) {
    return uVar10;
  }
LAB_00e6f2f0:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __gather_info
// Address: 00e6f6c8
// ==========================================================================================

/* std::__ndk1::__money_get<wchar_t>::__gather_info(bool, std::__ndk1::locale const&,
   std::__ndk1::money_base::pattern&, wchar_t&, wchar_t&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >&, std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> >&,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >&, int&) */

void std::__ndk1::__money_get<wchar_t>::__gather_info
               (bool param_1,locale *param_2,pattern *param_3,wchar_t *param_4,wchar_t *param_5,
               basic_string *param_6,basic_string *param_7,basic_string *param_8,
               basic_string *param_9,int *param_10)

{
  long lVar1;
  ulong *puVar2;
  undefined4 uVar3;
  wchar_t wVar4;
  int iVar5;
  long lVar6;
  long lVar7;
  long *plVar8;
  ulong *local_90;
  undefined *puStack_88;
  undefined8 local_80;
  ulong ***local_78;
  ulong **local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  lVar7 = *(long *)param_2;
  if (param_1) {
    lVar6 = *(long *)PTR_id_01ff56d8;
    puVar2 = (ulong *)PTR_id_01ff56d8;
  }
  else {
    lVar6 = *(long *)PTR_id_01ff56e0;
    puVar2 = (ulong *)PTR_id_01ff56e0;
  }
  puStack_88 = PTR___init_01ff5688;
  local_80 = 0;
  local_90 = puVar2;
  if (lVar6 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    local_80 = 0;
    __call_once(puVar2,&local_78,FUN_00e87ff8);
  }
  lVar6 = *(long *)(lVar7 + 0x10);
  if (((ulong)(*(long *)(lVar7 + 0x18) - lVar6 >> 3) <= (long)*(int *)(puVar2 + 1) - 1U) ||
     (plVar8 = *(long **)(lVar6 + ((long)*(int *)(puVar2 + 1) - 1U) * 8), plVar8 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00de5da0();
  }
  uVar3 = (**(code **)(*plVar8 + 0x58))(plVar8);
  *(undefined4 *)param_3 = uVar3;
  (**(code **)(*plVar8 + 0x40))(&local_90,plVar8);
  if (((byte)*param_9 & 1) != 0) {
    operator_delete(*(void **)(param_9 + 0x10));
  }
  *(undefined8 *)(param_9 + 0x10) = local_80;
  *(undefined **)(param_9 + 8) = puStack_88;
  *(ulong **)param_9 = local_90;
  (**(code **)(*plVar8 + 0x38))(&local_90,plVar8);
  if (((byte)*param_8 & 1) != 0) {
    operator_delete(*(void **)(param_8 + 0x10));
  }
  *(undefined8 *)(param_8 + 0x10) = local_80;
  *(undefined **)(param_8 + 8) = puStack_88;
  *(ulong **)param_8 = local_90;
  wVar4 = (**(code **)(*plVar8 + 0x18))(plVar8);
  *param_4 = wVar4;
  wVar4 = (**(code **)(*plVar8 + 0x20))(plVar8);
  *param_5 = wVar4;
  (**(code **)(*plVar8 + 0x28))(&local_90,plVar8);
  if (((byte)*param_6 & 1) != 0) {
    operator_delete(*(void **)(param_6 + 0x10));
  }
  *(undefined8 *)(param_6 + 0x10) = local_80;
  *(undefined **)(param_6 + 8) = puStack_88;
  *(ulong **)param_6 = local_90;
  (**(code **)(*plVar8 + 0x30))(&local_90,plVar8);
  if (((byte)*param_7 & 1) != 0) {
    operator_delete(*(void **)(param_7 + 0x10));
  }
  *(undefined8 *)(param_7 + 0x10) = local_80;
  *(undefined **)(param_7 + 8) = puStack_88;
  *(ulong **)param_7 = local_90;
  iVar5 = (**(code **)(*plVar8 + 0x48))(plVar8);
  *param_10 = iVar5;
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __gather_info
// Address: 00e6fe78
// ==========================================================================================

/* std::__ndk1::__money_put<char>::__gather_info(bool, bool, std::__ndk1::locale const&,
   std::__ndk1::money_base::pattern&, char&, char&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&, int&) */

void std::__ndk1::__money_put<char>::__gather_info
               (bool param_1,bool param_2,locale *param_3,pattern *param_4,char *param_5,
               char *param_6,basic_string *param_7,basic_string *param_8,basic_string *param_9,
               int *param_10)

{
  long lVar1;
  ulong *puVar2;
  char cVar3;
  undefined4 uVar4;
  int iVar5;
  long lVar6;
  code *pcVar7;
  long lVar8;
  long *plVar9;
  ulong *local_90;
  undefined *puStack_88;
  undefined8 local_80;
  ulong ***local_78;
  ulong **local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  lVar8 = *(long *)param_3;
  if (param_1) {
    lVar6 = *(long *)PTR_id_01ff56c8;
    puVar2 = (ulong *)PTR_id_01ff56c8;
  }
  else {
    lVar6 = *(long *)PTR_id_01ff56d0;
    puVar2 = (ulong *)PTR_id_01ff56d0;
  }
  puStack_88 = PTR___init_01ff5688;
  local_80 = 0;
  local_90 = puVar2;
  if (lVar6 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    local_80 = 0;
    __call_once(puVar2,&local_78,FUN_00e87ff8);
  }
  lVar6 = *(long *)(lVar8 + 0x10);
  if (((ulong)(*(long *)(lVar8 + 0x18) - lVar6 >> 3) <= (long)*(int *)(puVar2 + 1) - 1U) ||
     (plVar9 = *(long **)(lVar6 + ((long)*(int *)(puVar2 + 1) - 1U) * 8), plVar9 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00de5da0();
  }
  if (param_2) {
    uVar4 = (**(code **)(*plVar9 + 0x58))(plVar9);
    *(undefined4 *)param_4 = uVar4;
    pcVar7 = *(code **)(*plVar9 + 0x40);
  }
  else {
    uVar4 = (**(code **)(*plVar9 + 0x50))(plVar9);
    *(undefined4 *)param_4 = uVar4;
    pcVar7 = *(code **)(*plVar9 + 0x38);
  }
  (*pcVar7)(&local_90,plVar9);
  if (((byte)*param_9 & 1) != 0) {
    operator_delete(*(void **)(param_9 + 0x10));
  }
  *(undefined8 *)(param_9 + 0x10) = local_80;
  *(undefined **)(param_9 + 8) = puStack_88;
  *(ulong **)param_9 = local_90;
  cVar3 = (**(code **)(*plVar9 + 0x18))(plVar9);
  *param_5 = cVar3;
  cVar3 = (**(code **)(*plVar9 + 0x20))(plVar9);
  *param_6 = cVar3;
  (**(code **)(*plVar9 + 0x28))(&local_90,plVar9);
  if (((byte)*param_7 & 1) != 0) {
    operator_delete(*(void **)(param_7 + 0x10));
  }
  *(undefined8 *)(param_7 + 0x10) = local_80;
  *(undefined **)(param_7 + 8) = puStack_88;
  *(ulong **)param_7 = local_90;
  (**(code **)(*plVar9 + 0x30))(&local_90,plVar9);
  if (((byte)*param_8 & 1) != 0) {
    operator_delete(*(void **)(param_8 + 0x10));
  }
  *(undefined8 *)(param_8 + 0x10) = local_80;
  *(undefined **)(param_8 + 8) = puStack_88;
  *(ulong **)param_8 = local_90;
  iVar5 = (**(code **)(*plVar9 + 0x48))(plVar9);
  *param_10 = iVar5;
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __format
// Address: 00e700c4
// ==========================================================================================

/* std::__ndk1::__money_put<char>::__format(char*, char*&, char*&, unsigned int, char const*, char
   const*, std::__ndk1::ctype<char> const&, bool, std::__ndk1::money_base::pattern const&, char,
   char, std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&,
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >
   const&, int) */

void std::__ndk1::__money_put<char>::__format
               (char *param_1,char **param_2,char **param_3,uint param_4,char *param_5,char *param_6
               ,ctype *param_7,bool param_8,pattern *param_9,char param_10,char param_11,
               basic_string *param_12,basic_string *param_13,basic_string *param_14,int param_15)

{
  bool bVar1;
  bool bVar2;
  byte bVar3;
  basic_string bVar4;
  int iVar5;
  char cVar6;
  uint uVar7;
  basic_string *pbVar8;
  ulong uVar9;
  basic_string *pbVar10;
  byte *pbVar11;
  basic_string *pbVar12;
  uint uVar13;
  byte *pbVar14;
  long lVar15;
  char *pcVar16;
  int iVar17;
  int iVar18;
  size_t __n;
  byte *pbVar19;
  byte *pbVar20;
  
  pbVar12 = param_14 + 1;
  iVar5 = param_15 + -1;
  lVar15 = 0;
  bVar1 = iVar5 != 0 && 0 < param_15;
  *param_3 = param_1;
  do {
    switch(param_9[lVar15]) {
    case (pattern)0x0:
      *param_2 = *param_3;
      break;
    case (pattern)0x1:
      *param_2 = *param_3;
      cVar6 = (**(code **)(*(long *)param_7 + 0x38))(param_7,0x20);
      pcVar16 = *param_3;
      *param_3 = pcVar16 + 1;
      *pcVar16 = cVar6;
      break;
    case (pattern)0x2:
      bVar4 = *param_13;
      if (((byte)bVar4 & 1) == 0) {
        if (((param_4 >> 9 & 1) != 0) && (1 < (byte)bVar4)) {
          __n = (size_t)((byte)bVar4 >> 1);
          pbVar8 = param_13 + 1;
LAB_00e7016c:
          pcVar16 = *param_3;
          memmove(pcVar16,pbVar8,__n);
          *param_3 = pcVar16 + __n;
        }
      }
      else if (((param_4 >> 9 & 1) != 0) && (__n = *(size_t *)(param_13 + 8), __n != 0)) {
        pbVar8 = *(basic_string **)(param_13 + 0x10);
        goto LAB_00e7016c;
      }
      break;
    case (pattern)0x3:
      if (((byte)*param_14 & 1) == 0) {
        pbVar8 = pbVar12;
        if (1 < (byte)*param_14) {
LAB_00e70354:
          pbVar10 = (basic_string *)*param_3;
          bVar4 = *pbVar8;
          *param_3 = (char *)(pbVar10 + 1);
          *pbVar10 = bVar4;
        }
      }
      else if (*(long *)(param_14 + 8) != 0) {
        pbVar8 = *(basic_string **)(param_14 + 0x10);
        goto LAB_00e70354;
      }
      break;
    case (pattern)0x4:
      if (param_8) {
        param_5 = (char *)((byte *)param_5 + 1);
      }
      pbVar14 = (byte *)param_5;
      if (param_5 < param_6) {
        pbVar19 = (byte *)param_5;
        do {
          pbVar14 = pbVar19;
          if (((char)*pbVar19 < '\0') ||
             (((uint)*(undefined8 *)(*(long *)(param_7 + 0x10) + (ulong)*pbVar19 * 8) >> 6 & 1) == 0
             )) break;
          pbVar19 = pbVar19 + 1;
          pbVar14 = (byte *)param_6;
        } while ((byte *)param_6 != pbVar19);
      }
      pbVar19 = (byte *)*param_3;
      if (param_15 < 1) {
        if (pbVar14 != (byte *)param_5) goto LAB_00e70440;
LAB_00e70378:
        cVar6 = (**(code **)(*(long *)param_7 + 0x38))(param_7,0x30);
        pcVar16 = *param_3;
        *param_3 = pcVar16 + 1;
        *pcVar16 = cVar6;
      }
      else {
        pbVar20 = pbVar14;
        iVar18 = param_15;
        if (param_5 < pbVar14) {
          pbVar20 = pbVar14 + -1;
          bVar3 = *pbVar20;
          *param_3 = (char *)(pbVar19 + 1);
          *pbVar19 = bVar3;
          iVar18 = iVar5;
          if (param_15 < 2) {
            if (bVar1) goto LAB_00e703e4;
          }
          else {
            bVar2 = bVar1;
            if (param_5 < pbVar20) {
              pbVar14 = pbVar14 + -2;
              iVar17 = iVar5;
              do {
                pbVar20 = pbVar14;
                pbVar14 = (byte *)*param_3;
                bVar3 = *pbVar20;
                iVar18 = iVar17 + -1;
                bVar2 = iVar18 != 0 && 0 < iVar17;
                *param_3 = (char *)(pbVar14 + 1);
                *pbVar14 = bVar3;
                if (iVar17 < 2) break;
                pbVar14 = pbVar20 + -1;
                iVar17 = iVar18;
              } while (param_5 < pbVar20);
            }
            if (bVar2) goto LAB_00e703e4;
          }
          cVar6 = '\0';
          pbVar14 = pbVar20;
        }
        else {
LAB_00e703e4:
          cVar6 = (**(code **)(*(long *)param_7 + 0x38))(param_7,0x30);
          pbVar14 = pbVar20;
        }
        if (0 < iVar18) {
          iVar18 = iVar18 + 1;
          do {
            pcVar16 = *param_3;
            iVar18 = iVar18 + -1;
            *param_3 = pcVar16 + 1;
            *pcVar16 = cVar6;
          } while (1 < iVar18);
        }
        pcVar16 = *param_3;
        *param_3 = pcVar16 + 1;
        *pcVar16 = param_10;
        if (pbVar14 == (byte *)param_5) goto LAB_00e70378;
LAB_00e70440:
        if (((byte)*param_12 & 1) == 0) {
          pbVar8 = param_12 + 1;
          if (1 < (byte)*param_12) goto LAB_00e70464;
LAB_00e7046c:
          uVar7 = 0xffffffff;
        }
        else {
          if (*(long *)(param_12 + 8) == 0) goto LAB_00e7046c;
          pbVar8 = *(basic_string **)(param_12 + 0x10);
LAB_00e70464:
          uVar7 = (uint)(byte)*pbVar8;
        }
        uVar9 = 0;
        uVar13 = 0;
        do {
          if (uVar13 == uVar7) {
            pcVar16 = *param_3;
            uVar13 = (int)uVar9 + 1;
            uVar9 = (ulong)uVar13;
            *param_3 = pcVar16 + 1;
            *pcVar16 = param_11;
            if (((byte)*param_12 & 1) == 0) {
              if (uVar13 < (byte)*param_12 >> 1) {
                bVar4 = param_12[uVar9 + 1];
joined_r0x00e704f8:
                uVar7 = (uint)(byte)bVar4;
                if (uVar7 == 0xff) {
                  uVar13 = 0;
                  uVar7 = 0xffffffff;
                  goto LAB_00e70480;
                }
              }
            }
            else if (uVar9 < *(ulong *)(param_12 + 8)) {
              bVar4 = *(basic_string *)(*(long *)(param_12 + 0x10) + uVar9);
              goto joined_r0x00e704f8;
            }
            uVar13 = 0;
          }
LAB_00e70480:
          pbVar14 = pbVar14 + -1;
          bVar3 = *pbVar14;
          pbVar20 = (byte *)*param_3;
          uVar13 = uVar13 + 1;
          *param_3 = (char *)(pbVar20 + 1);
          *pbVar20 = bVar3;
        } while ((byte *)param_5 != pbVar14);
      }
      if ((pbVar19 != (byte *)*param_3) && (pbVar14 = (byte *)(*param_3 + -1), pbVar19 < pbVar14)) {
        do {
          pbVar11 = pbVar19 + 1;
          bVar3 = *pbVar19;
          *pbVar19 = *pbVar14;
          pbVar20 = pbVar14 + -1;
          *pbVar14 = bVar3;
          pbVar14 = pbVar20;
          pbVar19 = pbVar11;
        } while (pbVar11 < pbVar20);
      }
    }
    lVar15 = lVar15 + 1;
  } while (lVar15 != 4);
  bVar4 = *param_14;
  if (((byte)bVar4 & 1) == 0) {
    if ((byte)bVar4 < 4) goto LAB_00e70570;
    uVar9 = (ulong)((byte)bVar4 >> 1);
  }
  else {
    uVar9 = *(ulong *)(param_14 + 8);
    if (uVar9 < 2) goto LAB_00e70570;
    pbVar12 = *(basic_string **)(param_14 + 0x10);
  }
  pcVar16 = *param_3;
  memmove(pcVar16,pbVar12 + 1,uVar9 - 1);
  *param_3 = pcVar16 + (uVar9 - 1);
LAB_00e70570:
  if ((param_4 & 0xb0) != 0x10) {
    if ((param_4 & 0xb0) == 0x20) {
      param_1 = *param_3;
    }
    *param_2 = param_1;
  }
  return;
}



// ==========================================================================================
// Function: __gather_info
// Address: 00e70e3c
// ==========================================================================================

/* std::__ndk1::__money_put<wchar_t>::__gather_info(bool, bool, std::__ndk1::locale const&,
   std::__ndk1::money_base::pattern&, wchar_t&, wchar_t&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >&, std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> >&, int&) */

void std::__ndk1::__money_put<wchar_t>::__gather_info
               (bool param_1,bool param_2,locale *param_3,pattern *param_4,wchar_t *param_5,
               wchar_t *param_6,basic_string *param_7,basic_string *param_8,basic_string *param_9,
               int *param_10)

{
  long lVar1;
  ulong *puVar2;
  undefined4 uVar3;
  wchar_t wVar4;
  int iVar5;
  long lVar6;
  code *pcVar7;
  long lVar8;
  long *plVar9;
  ulong *local_90;
  undefined *puStack_88;
  undefined8 local_80;
  ulong ***local_78;
  ulong **local_70;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  lVar8 = *(long *)param_3;
  if (param_1) {
    lVar6 = *(long *)PTR_id_01ff56d8;
    puVar2 = (ulong *)PTR_id_01ff56d8;
  }
  else {
    lVar6 = *(long *)PTR_id_01ff56e0;
    puVar2 = (ulong *)PTR_id_01ff56e0;
  }
  puStack_88 = PTR___init_01ff5688;
  local_80 = 0;
  local_90 = puVar2;
  if (lVar6 != -1) {
    local_70 = &local_90;
    local_78 = &local_70;
    local_80 = 0;
    __call_once(puVar2,&local_78,FUN_00e87ff8);
  }
  lVar6 = *(long *)(lVar8 + 0x10);
  if (((ulong)(*(long *)(lVar8 + 0x18) - lVar6 >> 3) <= (long)*(int *)(puVar2 + 1) - 1U) ||
     (plVar9 = *(long **)(lVar6 + ((long)*(int *)(puVar2 + 1) - 1U) * 8), plVar9 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00de5da0();
  }
  if (param_2) {
    uVar3 = (**(code **)(*plVar9 + 0x58))(plVar9);
    *(undefined4 *)param_4 = uVar3;
    pcVar7 = *(code **)(*plVar9 + 0x40);
  }
  else {
    uVar3 = (**(code **)(*plVar9 + 0x50))(plVar9);
    *(undefined4 *)param_4 = uVar3;
    pcVar7 = *(code **)(*plVar9 + 0x38);
  }
  (*pcVar7)(&local_90,plVar9);
  if (((byte)*param_9 & 1) != 0) {
    operator_delete(*(void **)(param_9 + 0x10));
  }
  *(undefined8 *)(param_9 + 0x10) = local_80;
  *(undefined **)(param_9 + 8) = puStack_88;
  *(ulong **)param_9 = local_90;
  wVar4 = (**(code **)(*plVar9 + 0x18))(plVar9);
  *param_5 = wVar4;
  wVar4 = (**(code **)(*plVar9 + 0x20))(plVar9);
  *param_6 = wVar4;
  (**(code **)(*plVar9 + 0x28))(&local_90,plVar9);
  if (((byte)*param_7 & 1) != 0) {
    operator_delete(*(void **)(param_7 + 0x10));
  }
  *(undefined8 *)(param_7 + 0x10) = local_80;
  *(undefined **)(param_7 + 8) = puStack_88;
  *(ulong **)param_7 = local_90;
  (**(code **)(*plVar9 + 0x30))(&local_90,plVar9);
  if (((byte)*param_8 & 1) != 0) {
    operator_delete(*(void **)(param_8 + 0x10));
  }
  *(undefined8 *)(param_8 + 0x10) = local_80;
  *(undefined **)(param_8 + 8) = puStack_88;
  *(ulong **)param_8 = local_90;
  iVar5 = (**(code **)(*plVar9 + 0x48))(plVar9);
  *param_10 = iVar5;
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __format
// Address: 00e71088
// ==========================================================================================

/* std::__ndk1::__money_put<wchar_t>::__format(wchar_t*, wchar_t*&, wchar_t*&, unsigned int, wchar_t
   const*, wchar_t const*, std::__ndk1::ctype<wchar_t> const&, bool,
   std::__ndk1::money_base::pattern const&, wchar_t, wchar_t, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&,
   std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> > const&, std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t> > const&, int) */

void std::__ndk1::__money_put<wchar_t>::__format
               (wchar_t *param_1,wchar_t **param_2,wchar_t **param_3,uint param_4,wchar_t *param_5,
               wchar_t *param_6,ctype *param_7,bool param_8,pattern *param_9,wchar_t param_10,
               wchar_t param_11,basic_string *param_12,basic_string *param_13,basic_string *param_14
               ,int param_15)

{
  basic_string bVar1;
  size_t __n;
  wchar_t wVar2;
  uint uVar3;
  wchar_t *pwVar4;
  basic_string *pbVar5;
  ulong uVar6;
  wchar_t *pwVar7;
  undefined8 *puVar8;
  uint uVar9;
  ulong uVar10;
  ulong uVar11;
  wchar_t *pwVar12;
  long lVar13;
  wchar_t *pwVar14;
  int iVar15;
  int iVar16;
  wchar_t *local_a0;
  
  lVar13 = 0;
  local_a0 = (wchar_t *)(param_14 + 4);
  *param_3 = param_1;
  do {
    switch(param_9[lVar13]) {
    case (pattern)0x0:
      *param_2 = *param_3;
      break;
    case (pattern)0x1:
      *param_2 = *param_3;
      wVar2 = (**(code **)(*(long *)param_7 + 0x58))(param_7,0x20);
      pwVar14 = *param_3;
      *param_3 = pwVar14 + 1;
      *pwVar14 = wVar2;
      break;
    case (pattern)0x2:
      bVar1 = *param_13;
      if (((byte)bVar1 & 1) == 0) {
        if (((param_4 >> 9 & 1) != 0) && (1 < (byte)bVar1)) {
          uVar6 = (ulong)((byte)bVar1 >> 1);
          pbVar5 = param_13 + 4;
LAB_00e7111c:
          pwVar14 = *param_3;
          memmove(pwVar14,pbVar5,uVar6 * 4);
          *param_3 = pwVar14 + uVar6;
        }
      }
      else if (((param_4 >> 9 & 1) != 0) && (uVar6 = *(ulong *)(param_13 + 8), uVar6 != 0)) {
        pbVar5 = *(basic_string **)(param_13 + 0x10);
        goto LAB_00e7111c;
      }
      break;
    case (pattern)0x3:
      if (((byte)*param_14 & 1) == 0) {
        pwVar14 = local_a0;
        if (1 < (byte)*param_14) {
LAB_00e712e0:
          pwVar4 = *param_3;
          wVar2 = *pwVar14;
          *param_3 = pwVar4 + 1;
          *pwVar4 = wVar2;
        }
      }
      else if (*(long *)(param_14 + 8) != 0) {
        pwVar14 = *(wchar_t **)(param_14 + 0x10);
        goto LAB_00e712e0;
      }
      break;
    case (pattern)0x4:
      pwVar4 = *param_3;
      pwVar14 = param_5 + 1;
      pwVar7 = param_5 + 1;
      if (!param_8) {
        pwVar14 = param_5;
        pwVar7 = param_5;
      }
      while ((param_5 = pwVar7, pwVar14 < param_6 &&
             (uVar6 = (**(code **)(*(long *)param_7 + 0x18))(param_7,0x40,*pwVar14),
             (uVar6 & 1) != 0))) {
        pwVar14 = pwVar14 + 1;
        pwVar7 = param_5;
      }
      if (0 < param_15) {
        iVar16 = param_15;
        if (param_5 < pwVar14) {
          pwVar7 = *param_3;
          do {
            iVar15 = iVar16;
            pwVar14 = pwVar14 + -1;
            iVar16 = iVar15 + -1;
            pwVar12 = pwVar7 + 1;
            *pwVar7 = *pwVar14;
            if (iVar15 < 2) break;
            pwVar7 = pwVar12;
          } while (param_5 < pwVar14);
          *param_3 = pwVar12;
          if (1 < iVar15) goto LAB_00e712fc;
          wVar2 = L'\0';
        }
        else {
LAB_00e712fc:
          wVar2 = (**(code **)(*(long *)param_7 + 0x58))(param_7,0x30);
        }
        pwVar7 = *param_3;
        if (0 < iVar16) {
          if (6 < iVar16 - 1U) {
            uVar6 = (ulong)(iVar16 - 1U) + 1;
            uVar10 = uVar6 & 0x1fffffff8;
            pwVar12 = pwVar7 + uVar10;
            iVar16 = iVar16 - (int)uVar10;
            puVar8 = (undefined8 *)(pwVar7 + 4);
            uVar11 = uVar10;
            do {
              puVar8[-1] = CONCAT44(wVar2,wVar2);
              puVar8[-2] = CONCAT44(wVar2,wVar2);
              puVar8[1] = CONCAT44(wVar2,wVar2);
              *puVar8 = CONCAT44(wVar2,wVar2);
              uVar11 = uVar11 - 8;
              puVar8 = puVar8 + 4;
            } while (uVar11 != 0);
            pwVar7 = pwVar12;
            if (uVar6 == uVar10) goto LAB_00e7137c;
          }
          iVar16 = iVar16 + 1;
          pwVar12 = pwVar7;
          do {
            iVar16 = iVar16 + -1;
            *pwVar12 = wVar2;
            pwVar7 = pwVar12 + 1;
            pwVar12 = pwVar12 + 1;
          } while (1 < iVar16);
        }
LAB_00e7137c:
        *param_3 = pwVar7 + 1;
        *pwVar7 = param_10;
      }
      if (pwVar14 == param_5) {
        wVar2 = (**(code **)(*(long *)param_7 + 0x58))(param_7,0x30);
        pwVar14 = *param_3;
        pwVar7 = pwVar14 + 1;
        *param_3 = pwVar7;
        *pwVar14 = wVar2;
      }
      else {
        if (((byte)*param_12 & 1) == 0) {
          pbVar5 = param_12 + 1;
          if (1 < (byte)*param_12) goto LAB_00e71420;
LAB_00e71428:
          uVar3 = 0xffffffff;
        }
        else {
          if (*(long *)(param_12 + 8) == 0) goto LAB_00e71428;
          pbVar5 = *(basic_string **)(param_12 + 0x10);
LAB_00e71420:
          uVar3 = (uint)(byte)*pbVar5;
        }
        uVar6 = 0;
        uVar9 = 0;
        do {
          pwVar12 = *param_3;
          if (uVar9 == uVar3) {
            pwVar7 = pwVar12 + 1;
            *param_3 = pwVar7;
            *pwVar12 = param_11;
            uVar9 = (int)uVar6 + 1;
            uVar6 = (ulong)uVar9;
            pwVar12 = pwVar7;
            if (((byte)*param_12 & 1) == 0) {
              if (uVar9 < (byte)*param_12 >> 1) {
                bVar1 = param_12[uVar6 + 1];
joined_r0x00e714b0:
                uVar3 = (uint)(byte)bVar1;
                if (uVar3 == 0xff) {
                  uVar9 = 0;
                  uVar3 = 0xffffffff;
                  goto LAB_00e7143c;
                }
              }
            }
            else if (uVar6 < *(ulong *)(param_12 + 8)) {
              bVar1 = *(basic_string *)(*(long *)(param_12 + 0x10) + uVar6);
              goto joined_r0x00e714b0;
            }
            uVar9 = 0;
          }
LAB_00e7143c:
          pwVar14 = pwVar14 + -1;
          wVar2 = *pwVar14;
          pwVar7 = pwVar12 + 1;
          uVar9 = uVar9 + 1;
          *param_3 = pwVar7;
          *pwVar12 = wVar2;
        } while (param_5 != pwVar14);
      }
      if ((pwVar4 != pwVar7) && (pwVar7 = pwVar7 + -1, pwVar4 < pwVar7)) {
        do {
          pwVar12 = pwVar4 + 1;
          wVar2 = *pwVar4;
          *pwVar4 = *pwVar7;
          pwVar14 = pwVar7 + -1;
          *pwVar7 = wVar2;
          pwVar7 = pwVar14;
          pwVar4 = pwVar12;
        } while (pwVar12 < pwVar14);
      }
    }
    lVar13 = lVar13 + 1;
  } while (lVar13 != 4);
  bVar1 = *param_14;
  if (((byte)bVar1 & 1) == 0) {
    if ((byte)bVar1 < 4) goto LAB_00e71520;
    uVar6 = (ulong)((byte)bVar1 >> 1);
  }
  else {
    uVar6 = *(ulong *)(param_14 + 8);
    if (uVar6 < 2) goto LAB_00e71520;
    local_a0 = *(wchar_t **)(param_14 + 0x10);
  }
  pwVar14 = *param_3;
  __n = uVar6 * 4 - 4;
  if (__n != 0) {
    memmove(pwVar14,local_a0 + 1,__n);
  }
  *param_3 = pwVar14 + (uVar6 - 1);
LAB_00e71520:
  if ((param_4 & 0xb0) != 0x10) {
    if ((param_4 & 0xb0) == 0x20) {
      param_1 = *param_3;
    }
    *param_2 = param_1;
  }
  return;
}



// ==========================================================================================
// Function: __global
// Address: 00e77998
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::locale::__global() */

undefined8 * std::__ndk1::locale::__global(void)

{
  int iVar1;
  
  if (((DAT_0231cfe0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfe0), iVar1 != 0)) {
    if (((DAT_0231cfc8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfc8), iVar1 != 0)) {
                    /* try { // try from 00e77a34 to 00e77a47 has its CatchHandler @ 00e77a6c */
      FUN_00e71a50(&DAT_0231dbe0,1);
      DAT_0231cfb8 = &DAT_0231dbe0;
      DAT_0231cfc0 = &DAT_0231cfb8;
      __cxa_guard_release(&DAT_0231cfc8);
    }
    DAT_0231cfd0 = DAT_0231cfb8;
    __shared_count::__add_shared();
    DAT_0231cfd8 = &DAT_0231cfd0;
    __cxa_guard_release(&DAT_0231cfe0);
  }
  return DAT_0231cfd8;
}



// ==========================================================================================
// Function: __install_ctor
// Address: 00e77f34
// ==========================================================================================

/* std::__ndk1::locale::__install_ctor(std::__ndk1::locale const&, std::__ndk1::locale::facet*,
   long) */

void __thiscall
std::__ndk1::locale::__install_ctor(locale *this,locale *param_1,facet *param_2,long param_3)

{
  void *pvVar1;
  
  if (param_2 == (facet *)0x0) {
    pvVar1 = *(void **)param_1;
  }
  else {
    pvVar1 = operator_new(0x140);
                    /* try { // try from 00e77f6c to 00e77f77 has its CatchHandler @ 00e77f9c */
    FUN_00e7766c(pvVar1,*(undefined8 *)param_1,param_2,param_3);
  }
  *(void **)this = pvVar1;
  __shared_count::__add_shared();
  return;
}



// ==========================================================================================
// Function: __get
// Address: 00e781f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::locale::id::__get() */

long std::__ndk1::locale::id::__get(void)

{
  long lVar1;
  ulong *in_x0;
  undefined local_50 [8];
  undefined *puStack_48;
  undefined8 local_40;
  undefined **local_38;
  undefined *local_30;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  puStack_48 = PTR___init_01ff5688;
  local_40 = 0;
  if (*in_x0 != 0xffffffffffffffff) {
    local_38 = &local_30;
    local_30 = local_50;
    __call_once(in_x0,&local_38,FUN_00e87ff8);
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return (long)*(int *)(in_x0 + 1) + -1;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __on_zero_shared
// Address: 00e7848c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::locale::facet::__on_zero_shared() */

void std::__ndk1::locale::facet::__on_zero_shared(void)

{
  long *in_x0;
  
                    /* WARNING: Could not recover jumptable at 0x00e78498. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*in_x0 + 8))();
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e7849c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::locale::id::__init() */

void std::__ndk1::locale::id::__init(void)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  undefined *puVar4;
  long in_x0;
  
  puVar4 = PTR___next_id_01ff58c8;
  do {
    iVar1 = *(int *)puVar4;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
    if (bVar3) {
      *(int *)puVar4 = iVar1 + 1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  *(int *)(in_x0 + 8) = iVar1 + 1;
  return;
}



// ==========================================================================================
// Function: ~__narrow_to_utf8
// Address: 00e7ec10
// ==========================================================================================

/* std::__ndk1::__narrow_to_utf8<16ul>::~__narrow_to_utf8() */

void __thiscall std::__ndk1::__narrow_to_utf8<16ul>::~__narrow_to_utf8(__narrow_to_utf8<16ul> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__narrow_to_utf8
// Address: 00e7ec3c
// ==========================================================================================

/* std::__ndk1::__narrow_to_utf8<32ul>::~__narrow_to_utf8() */

void __thiscall std::__ndk1::__narrow_to_utf8<32ul>::~__narrow_to_utf8(__narrow_to_utf8<32ul> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__widen_from_utf8
// Address: 00e7ec68
// ==========================================================================================

/* std::__ndk1::__widen_from_utf8<16ul>::~__widen_from_utf8() */

void __thiscall
std::__ndk1::__widen_from_utf8<16ul>::~__widen_from_utf8(__widen_from_utf8<16ul> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__widen_from_utf8
// Address: 00e7ec94
// ==========================================================================================

/* std::__ndk1::__widen_from_utf8<32ul>::~__widen_from_utf8() */

void __thiscall
std::__ndk1::__widen_from_utf8<32ul>::~__widen_from_utf8(__widen_from_utf8<32ul> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e7f028
// ==========================================================================================

/* std::__ndk1::numpunct_byname<char>::__init(char const*) */

void __thiscall
std::__ndk1::numpunct_byname<char>::__init(numpunct_byname<char> *this,char *param_1)

{
  long lVar1;
  wint_t wVar2;
  int iVar3;
  __locale_t __dataset;
  __locale_t p_Var4;
  lconv *plVar5;
  size_t sVar6;
  mbstate_t *pmVar7;
  numpunct_byname<char> nVar8;
  void *__dest;
  numpunct_byname<char> *pnVar9;
  ulong uVar10;
  undefined8 local_88;
  size_t local_80;
  void *pvStack_78;
  mbstate_t local_70;
  mbstate_t mStack_68;
  mbstate_t local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  iVar3 = strcmp(param_1,"C");
  if (iVar3 != 0) {
    __dataset = newlocale(0x1fbf,param_1,(__locale_t)0x0);
    if (__dataset == (__locale_t)0x0) {
      sVar6 = strlen(param_1);
      if (0xffffffffffffffef < sVar6) {
                    /* try { // try from 00e7f260 to 00e7f29b has its CatchHandler @ 00e7f3a0 */
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      if (sVar6 < 0x17) {
        __dest = (void *)((ulong)&local_88 | 1);
        local_88 = CONCAT71(local_88._1_7_,(char)((int)sVar6 << 1));
        if (sVar6 != 0) goto LAB_00e7f2ac;
      }
      else {
        uVar10 = sVar6 + 0x10 & 0xfffffffffffffff0;
        __dest = operator_new(uVar10);
        local_88 = uVar10 | 1;
        local_80 = sVar6;
        pvStack_78 = __dest;
LAB_00e7f2ac:
        memcpy(__dest,param_1,sVar6);
      }
      *(undefined *)((long)__dest + sVar6) = 0;
                    /* try { // try from 00e7f2c0 to 00e7f2d3 has its CatchHandler @ 00e7f318 */
      pmVar7 = (mbstate_t *)
               basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
               insert((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_88,0,
                      "numpunct_byname<char>::numpunct_byname failed to construct for ");
      local_60 = pmVar7[2];
      mStack_68 = pmVar7[1];
      local_70 = *pmVar7;
      pmVar7[1].__count = 0;
      pmVar7[1].__value = (_union_27)0x0;
      pmVar7[2].__count = 0;
      pmVar7[2].__value = (_union_27)0x0;
      pmVar7->__count = 0;
      pmVar7->__value = (_union_27)0x0;
                    /* try { // try from 00e7f2ec to 00e7f2f3 has its CatchHandler @ 00e7f300 */
      FUN_00e78634(&local_70);
      goto LAB_00e7f2f4;
    }
                    /* try { // try from 00e7f088 to 00e7f08b has its CatchHandler @ 00e7f3c0 */
    p_Var4 = uselocale(__dataset);
                    /* try { // try from 00e7f090 to 00e7f093 has its CatchHandler @ 00e7f3a8 */
    plVar5 = localeconv();
    if (p_Var4 != (__locale_t)0x0) {
                    /* try { // try from 00e7f09c to 00e7f0a3 has its CatchHandler @ 00e7f39c */
      uselocale(p_Var4);
    }
    pnVar9 = (numpunct_byname<char> *)plVar5->decimal_point;
    nVar8 = *pnVar9;
    if (nVar8 != (numpunct_byname<char>)0x0) {
      if (pnVar9[1] == (numpunct_byname<char>)0x0) {
LAB_00e7f154:
        this[0x10] = nVar8;
      }
      else {
        local_70.__count = 0;
        local_70.__value = (_union_27)0x0;
                    /* try { // try from 00e7f0bc to 00e7f0d3 has its CatchHandler @ 00e7f3c0 */
        sVar6 = __strlen_chk(pnVar9,0xffffffffffffffff);
        p_Var4 = uselocale(__dataset);
                    /* try { // try from 00e7f0d8 to 00e7f0eb has its CatchHandler @ 00e7f384 */
        sVar6 = mbrtowc((wchar_t *)&local_88,(char *)pnVar9,sVar6,&local_70);
        if (p_Var4 != (__locale_t)0x0) {
                    /* try { // try from 00e7f0f4 to 00e7f0fb has its CatchHandler @ 00e7f368 */
          uselocale(p_Var4);
        }
        if (sVar6 < 0xfffffffffffffffe) {
          wVar2 = (wint_t)local_88;
                    /* try { // try from 00e7f108 to 00e7f10f has its CatchHandler @ 00e7f3c0 */
          p_Var4 = uselocale(__dataset);
                    /* try { // try from 00e7f114 to 00e7f11b has its CatchHandler @ 00e7f34c */
          iVar3 = wctob(wVar2);
          if (p_Var4 != (__locale_t)0x0) {
                    /* try { // try from 00e7f124 to 00e7f12b has its CatchHandler @ 00e7f2fc */
            uselocale(p_Var4);
          }
          if (iVar3 == -1) {
            if ((wVar2 == 0x202f) || (wVar2 == 0xa0)) {
              nVar8 = (numpunct_byname<char>)0x20;
              goto LAB_00e7f154;
            }
          }
          else {
            this[0x10] = SUB41(iVar3,0);
          }
        }
      }
    }
    pnVar9 = (numpunct_byname<char> *)plVar5->thousands_sep;
    nVar8 = *pnVar9;
    if (nVar8 != (numpunct_byname<char>)0x0) {
      if (pnVar9[1] == (numpunct_byname<char>)0x0) {
LAB_00e7f208:
        this[0x11] = nVar8;
      }
      else {
        local_70.__count = 0;
        local_70.__value = (_union_27)0x0;
                    /* try { // try from 00e7f170 to 00e7f187 has its CatchHandler @ 00e7f3c0 */
        sVar6 = __strlen_chk(pnVar9,0xffffffffffffffff);
        p_Var4 = uselocale(__dataset);
                    /* try { // try from 00e7f18c to 00e7f19f has its CatchHandler @ 00e7f36c */
        sVar6 = mbrtowc((wchar_t *)&local_88,(char *)pnVar9,sVar6,&local_70);
        if (p_Var4 != (__locale_t)0x0) {
                    /* try { // try from 00e7f1a8 to 00e7f1af has its CatchHandler @ 00e7f364 */
          uselocale(p_Var4);
        }
        if (sVar6 < 0xfffffffffffffffe) {
          wVar2 = (wint_t)local_88;
                    /* try { // try from 00e7f1bc to 00e7f1c3 has its CatchHandler @ 00e7f3c0 */
          p_Var4 = uselocale(__dataset);
                    /* try { // try from 00e7f1c8 to 00e7f1cf has its CatchHandler @ 00e7f334 */
          iVar3 = wctob(wVar2);
          if (p_Var4 != (__locale_t)0x0) {
                    /* try { // try from 00e7f1d8 to 00e7f1df has its CatchHandler @ 00e7f2f8 */
            uselocale(p_Var4);
          }
          if (iVar3 == -1) {
            if ((wVar2 == 0x202f) || (wVar2 == 0xa0)) {
              nVar8 = (numpunct_byname<char>)0x20;
              goto LAB_00e7f208;
            }
          }
          else {
            this[0x11] = SUB41(iVar3,0);
          }
        }
      }
    }
                    /* try { // try from 00e7f214 to 00e7f217 has its CatchHandler @ 00e7f3c0 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               (this + 0x18),plVar5->grouping);
                    /* try { // try from 00e7f218 to 00e7f21f has its CatchHandler @ 00e7f3a4 */
    freelocale(__dataset);
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
LAB_00e7f2f4:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __init
// Address: 00e7f53c
// ==========================================================================================

/* std::__ndk1::numpunct_byname<wchar_t>::__init(char const*) */

void __thiscall
std::__ndk1::numpunct_byname<wchar_t>::__init(numpunct_byname<wchar_t> *this,char *param_1)

{
  long lVar1;
  int iVar2;
  __locale_t __dataset;
  __locale_t p_Var3;
  lconv *plVar4;
  size_t sVar5;
  mbstate_t *pmVar6;
  void *__dest;
  char *pcVar7;
  ulong uVar8;
  undefined8 local_88;
  size_t local_80;
  void *pvStack_78;
  mbstate_t local_70;
  mbstate_t mStack_68;
  mbstate_t local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  iVar2 = strcmp(param_1,"C");
  if (iVar2 != 0) {
    __dataset = newlocale(0x1fbf,param_1,(__locale_t)0x0);
    if (__dataset == (__locale_t)0x0) {
      sVar5 = strlen(param_1);
      if (0xffffffffffffffef < sVar5) {
                    /* try { // try from 00e7f6cc to 00e7f707 has its CatchHandler @ 00e7f7d4 */
                    /* WARNING: Subroutine does not return */
        __basic_string_common<true>::__throw_length_error();
      }
      if (sVar5 < 0x17) {
        __dest = (void *)((ulong)&local_88 | 1);
        local_88 = CONCAT71(local_88._1_7_,(char)((int)sVar5 << 1));
        if (sVar5 != 0) goto LAB_00e7f718;
      }
      else {
        uVar8 = sVar5 + 0x10 & 0xfffffffffffffff0;
        __dest = operator_new(uVar8);
        local_88 = uVar8 | 1;
        local_80 = sVar5;
        pvStack_78 = __dest;
LAB_00e7f718:
        memcpy(__dest,param_1,sVar5);
      }
      *(undefined *)((long)__dest + sVar5) = 0;
                    /* try { // try from 00e7f72c to 00e7f73f has its CatchHandler @ 00e7f77c */
      pmVar6 = (mbstate_t *)
               basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
               insert((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_88,0,
                      "numpunct_byname<wchar_t>::numpunct_byname failed to construct for ");
      local_60 = pmVar6[2];
      mStack_68 = pmVar6[1];
      local_70 = *pmVar6;
      pmVar6[1].__count = 0;
      pmVar6[1].__value = (_union_27)0x0;
      pmVar6[2].__count = 0;
      pmVar6[2].__value = (_union_27)0x0;
      pmVar6->__count = 0;
      pmVar6->__value = (_union_27)0x0;
                    /* try { // try from 00e7f758 to 00e7f75f has its CatchHandler @ 00e7f764 */
      FUN_00e78634(&local_70);
      goto LAB_00e7f760;
    }
                    /* try { // try from 00e7f59c to 00e7f59f has its CatchHandler @ 00e7f7f4 */
    p_Var3 = uselocale(__dataset);
                    /* try { // try from 00e7f5a4 to 00e7f5a7 has its CatchHandler @ 00e7f7dc */
    plVar4 = localeconv();
    if (p_Var3 != (__locale_t)0x0) {
                    /* try { // try from 00e7f5b0 to 00e7f5b7 has its CatchHandler @ 00e7f7d0 */
      uselocale(p_Var3);
    }
    pcVar7 = plVar4->decimal_point;
    if (*pcVar7 != '\0') {
      local_70.__count = 0;
      local_70.__value = (_union_27)0x0;
                    /* try { // try from 00e7f5c8 to 00e7f5df has its CatchHandler @ 00e7f7f4 */
      sVar5 = __strlen_chk(pcVar7,0xffffffffffffffff);
      p_Var3 = uselocale(__dataset);
                    /* try { // try from 00e7f5e4 to 00e7f5f7 has its CatchHandler @ 00e7f7b8 */
      sVar5 = mbrtowc((wchar_t *)&local_88,pcVar7,sVar5,&local_70);
      if (p_Var3 != (__locale_t)0x0) {
                    /* try { // try from 00e7f600 to 00e7f607 has its CatchHandler @ 00e7f79c */
        uselocale(p_Var3);
      }
      if (sVar5 < 0xfffffffffffffffe) {
        *(undefined4 *)(this + 0x10) = (undefined4)local_88;
      }
    }
    pcVar7 = plVar4->thousands_sep;
    if (*pcVar7 != '\0') {
      local_70.__count = 0;
      local_70.__value = (_union_27)0x0;
                    /* try { // try from 00e7f628 to 00e7f63f has its CatchHandler @ 00e7f7f4 */
      sVar5 = __strlen_chk(pcVar7,0xffffffffffffffff);
      p_Var3 = uselocale(__dataset);
                    /* try { // try from 00e7f644 to 00e7f657 has its CatchHandler @ 00e7f7a0 */
      sVar5 = mbrtowc((wchar_t *)&local_88,pcVar7,sVar5,&local_70);
      if (p_Var3 != (__locale_t)0x0) {
                    /* try { // try from 00e7f660 to 00e7f667 has its CatchHandler @ 00e7f798 */
        uselocale(p_Var3);
      }
      if (sVar5 < 0xfffffffffffffffe) {
        *(undefined4 *)(this + 0x14) = (undefined4)local_88;
      }
    }
                    /* try { // try from 00e7f680 to 00e7f683 has its CatchHandler @ 00e7f7f4 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               (this + 0x18),plVar4->grouping);
                    /* try { // try from 00e7f684 to 00e7f68b has its CatchHandler @ 00e7f7d8 */
    freelocale(__dataset);
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
LAB_00e7f760:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __get_base
// Address: 00e7f8f0
// ==========================================================================================

/* std::__ndk1::__num_get_base::__get_base(std::__ndk1::ios_base&) */

undefined8 std::__ndk1::__num_get_base::__get_base(ios_base *param_1)

{
  uint uVar1;
  
  uVar1 = *(uint *)(param_1 + 8) & 0x4a;
  if (uVar1 == 0) {
    return 0;
  }
  if (uVar1 != 0x40) {
    if (uVar1 == 8) {
      return 0x10;
    }
    return 10;
  }
  return 8;
}



// ==========================================================================================
// Function: __weeks
// Address: 00e7f934
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__weeks() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__weeks(void)

{
  int iVar1;
  
  if (((DAT_0231d078 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d078), iVar1 != 0)) {
    if (((DAT_0231d320 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d320), iVar1 != 0)) {
      _DAT_0231d308 = 0;
      DAT_0231d300 = 0;
      DAT_0231d318 = 0;
      _DAT_0231d310 = 0;
      DAT_0231d2e8 = 0;
      _DAT_0231d2e0 = 0;
      uRam000000000231d2f8 = 0;
      _DAT_0231d2f0 = 0;
      uRam000000000231d2c8 = 0;
      _DAT_0231d2c0 = 0;
      _DAT_0231d2d8 = 0;
      DAT_0231d2d0 = 0;
      _DAT_0231d2a8 = 0;
      DAT_0231d2a0 = 0;
      DAT_0231d2b8 = 0;
      _DAT_0231d2b0 = 0;
      DAT_0231d288 = 0;
      _DAT_0231d280 = 0;
      uRam000000000231d298 = 0;
      _DAT_0231d290 = 0;
      uRam000000000231d268 = 0;
      _DAT_0231d260 = 0;
      _DAT_0231d278 = 0;
      DAT_0231d270 = 0;
      _DAT_0231d248 = 0;
      DAT_0231d240 = 0;
      DAT_0231d258 = 0;
      _DAT_0231d250 = 0;
      DAT_0231d228 = 0;
      _DAT_0231d220 = 0;
      uRam000000000231d238 = 0;
      _DAT_0231d230 = 0;
      uRam000000000231d208 = 0;
      _DAT_0231d200 = 0;
      _DAT_0231d218 = 0;
      DAT_0231d210 = 0;
      _DAT_0231d1e8 = 0;
      DAT_0231d1e0 = 0;
      DAT_0231d1f8 = 0;
      _DAT_0231d1f0 = 0;
      uRam000000000231d1d8 = 0;
      _DAT_0231d1d0 = 0;
      __cxa_atexit(FUN_00e87900,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d320);
    }
                    /* try { // try from 00e7f98c to 00e7faa7 has its CatchHandler @ 00e7fb34 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d1d0,"Sunday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d1e8,"Monday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d200,"Tuesday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d218,"Wednesday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d230,"Thursday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d248,"Friday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d260,"Saturday");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d278,"Sun");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d290,"Mon");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d2a8,"Tue");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d2c0,"Wed");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d2d8,"Thu");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d2f0,"Fri");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d308,"Sat");
    DAT_0231d070 = &DAT_0231d1d0;
    __cxa_guard_release(&DAT_0231d078);
  }
  return DAT_0231d070;
}



// ==========================================================================================
// Function: __weeks
// Address: 00e7fb4c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__weeks() const */

undefined1 * std::__ndk1::__time_get_c_storage<wchar_t>::__weeks(void)

{
  int iVar1;
  
  if (((DAT_0231d088 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d088), iVar1 != 0)) {
    if (((DAT_0231d478 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d478), iVar1 != 0)) {
      _DAT_0231d460 = 0;
      DAT_0231d458 = 0;
      DAT_0231d470 = 0;
      _DAT_0231d468 = 0;
      DAT_0231d440 = 0;
      _DAT_0231d438 = 0;
      uRam000000000231d450 = 0;
      _DAT_0231d448 = 0;
      uRam000000000231d420 = 0;
      _DAT_0231d418 = 0;
      _DAT_0231d430 = 0;
      DAT_0231d428 = 0;
      _DAT_0231d400 = 0;
      DAT_0231d3f8 = 0;
      DAT_0231d410 = 0;
      _DAT_0231d408 = 0;
      DAT_0231d3e0 = 0;
      _DAT_0231d3d8 = 0;
      uRam000000000231d3f0 = 0;
      _DAT_0231d3e8 = 0;
      uRam000000000231d3c0 = 0;
      _DAT_0231d3b8 = 0;
      _DAT_0231d3d0 = 0;
      DAT_0231d3c8 = 0;
      _DAT_0231d3a0 = 0;
      DAT_0231d398 = 0;
      DAT_0231d3b0 = 0;
      _DAT_0231d3a8 = 0;
      DAT_0231d380 = 0;
      _DAT_0231d378 = 0;
      uRam000000000231d390 = 0;
      _DAT_0231d388 = 0;
      uRam000000000231d360 = 0;
      _DAT_0231d358 = 0;
      _DAT_0231d370 = 0;
      DAT_0231d368 = 0;
      _DAT_0231d340 = 0;
      DAT_0231d338 = 0;
      DAT_0231d350 = 0;
      _DAT_0231d348 = 0;
      uRam000000000231d330 = 0;
      _DAT_0231d328 = 0;
      __cxa_atexit(FUN_00e87a70,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d478);
    }
                    /* try { // try from 00e7fba4 to 00e7fcbf has its CatchHandler @ 00e7fd4c */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d328,L"Sunday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d340,L"Monday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d358,L"Tuesday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d370,L"Wednesday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d388,L"Thursday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d3a0,L"Friday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d3b8,L"Saturday");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d3d0,L"Sun");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d3e8,L"Mon");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d400,L"Tue");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d418,L"Wed");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d430,L"Thu");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d448,L"Fri");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d460,L"Sat");
    DAT_0231d080 = &DAT_0231d328;
    __cxa_guard_release(&DAT_0231d088);
  }
  return DAT_0231d080;
}



// ==========================================================================================
// Function: __months
// Address: 00e7fd64
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__months() const */

undefined * std::__ndk1::__time_get_c_storage<char>::__months(void)

{
  int iVar1;
  
  if (((DAT_0231d098 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d098), iVar1 != 0)) {
    if (((DAT_0231d6c0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d6c0), iVar1 != 0)) {
      memset(&DAT_0231d480,0,0x240);
      __cxa_atexit(FUN_00e87be0,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d6c0);
    }
                    /* try { // try from 00e7fdbc to 00e7ff9f has its CatchHandler @ 00e80008 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d480,"January");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d498,"February");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d4b0,"March");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d4c8,"April");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d4e0,"May");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d4f8,"June");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d510,"July");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d528,"August");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d540,"September");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d558,"October");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d570,"November");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d588,"December");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d5a0,"Jan");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d5b8,"Feb");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d5d0,"Mar");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d5e8,"Apr");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d600,"May");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d618,"Jun");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d630,"Jul");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d648,"Aug");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d660,"Sep");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d678,"Oct");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d690,"Nov");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d6a8,"Dec");
    DAT_0231d090 = &DAT_0231d480;
    __cxa_guard_release(&DAT_0231d098);
  }
  return DAT_0231d090;
}



// ==========================================================================================
// Function: __months
// Address: 00e80020
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__months() const */

undefined * std::__ndk1::__time_get_c_storage<wchar_t>::__months(void)

{
  int iVar1;
  
  if (((DAT_0231d0a8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d0a8), iVar1 != 0)) {
    if (((DAT_0231d908 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d908), iVar1 != 0)) {
      memset(&DAT_0231d6c8,0,0x240);
      __cxa_atexit(FUN_00e87c30,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d908);
    }
                    /* try { // try from 00e80078 to 00e8025b has its CatchHandler @ 00e802c4 */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d6c8,L"January");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d6e0,L"February");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d6f8,L"March");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d710,L"April");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d728,L"May");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d740,L"June");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d758,L"July");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d770,L"August");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d788,L"September");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d7a0,L"October");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d7b8,L"November");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d7d0,L"December");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d7e8,L"Jan");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d800,L"Feb");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d818,L"Mar");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d830,L"Apr");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d848,L"May");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d860,L"Jun");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d878,L"Jul");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d890,L"Aug");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d8a8,L"Sep");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d8c0,L"Oct");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d8d8,L"Nov");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d8f0,L"Dec");
    DAT_0231d0a0 = &DAT_0231d6c8;
    __cxa_guard_release(&DAT_0231d0a8);
  }
  return DAT_0231d0a0;
}



// ==========================================================================================
// Function: __am_pm
// Address: 00e802dc
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__am_pm() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__am_pm(void)

{
  int iVar1;
  
  if (((DAT_0231d0b8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d0b8), iVar1 != 0)) {
    if (((DAT_0231d940 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d940), iVar1 != 0)) {
      _DAT_0231d928 = 0;
      DAT_0231d920 = 0;
      DAT_0231d938 = 0;
      _DAT_0231d930 = 0;
      uRam000000000231d918 = 0;
      _DAT_0231d910 = 0;
      __cxa_atexit(FUN_00e87c80,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d940);
    }
                    /* try { // try from 00e80334 to 00e8035f has its CatchHandler @ 00e803c8 */
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d910,"AM");
    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::assign
              ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               &DAT_0231d928,"PM");
    DAT_0231d0b0 = &DAT_0231d910;
    __cxa_guard_release(&DAT_0231d0b8);
  }
  return DAT_0231d0b0;
}



// ==========================================================================================
// Function: __am_pm
// Address: 00e803e0
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__am_pm() const */

undefined1 * std::__ndk1::__time_get_c_storage<wchar_t>::__am_pm(void)

{
  int iVar1;
  
  if (((DAT_0231d0c8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d0c8), iVar1 != 0)) {
    if (((DAT_0231d978 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d978), iVar1 != 0)) {
      _DAT_0231d960 = 0;
      DAT_0231d958 = 0;
      DAT_0231d970 = 0;
      _DAT_0231d968 = 0;
      uRam000000000231d950 = 0;
      _DAT_0231d948 = 0;
      __cxa_atexit(FUN_00e87cd0,0,&PTR_LOOP_01ecb1d0);
      __cxa_guard_release(&DAT_0231d978);
    }
                    /* try { // try from 00e80438 to 00e80463 has its CatchHandler @ 00e804cc */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d948,L"AM");
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::assign
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d960,L"PM");
    DAT_0231d0c0 = &DAT_0231d948;
    __cxa_guard_release(&DAT_0231d0c8);
  }
  return DAT_0231d0c0;
}



// ==========================================================================================
// Function: __x
// Address: 00e804e4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__x() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__x(void)

{
  int iVar1;
  
  if (((DAT_0231d0e8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d0e8), iVar1 != 0)) {
    DAT_0231d0d0 = 0x10;
    DAT_0231d0d1 = 0x79252f64252f6d25;
    DAT_0231d0d9 = 0;
    __cxa_atexit(PTR__basic_string_01ff5530,&DAT_0231d0d0,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d0e8);
  }
  return &DAT_0231d0d0;
}



// ==========================================================================================
// Function: __x
// Address: 00e80570
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__x() const */

undefined * std::__ndk1::__time_get_c_storage<wchar_t>::__x(void)

{
  int iVar1;
  
  if (((DAT_0231d108 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d108), iVar1 != 0)) {
                    /* try { // try from 00e805b8 to 00e805cb has its CatchHandler @ 00e805f8 */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
    basic_string<decltype(nullptr)>
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d0f0,L"%m/%d/%y");
    __cxa_atexit(PTR__basic_string_01ff58f0,&DAT_0231d0f0,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d108);
  }
  return &DAT_0231d0f0;
}



// ==========================================================================================
// Function: __X
// Address: 00e80610
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__X() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__X(void)

{
  int iVar1;
  
  if (((DAT_0231d128 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d128), iVar1 != 0)) {
    DAT_0231d110 = 0x10;
    DAT_0231d111 = 0x53253a4d253a4825;
    DAT_0231d119 = 0;
    __cxa_atexit(PTR__basic_string_01ff5530,&DAT_0231d110,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d128);
  }
  return &DAT_0231d110;
}



// ==========================================================================================
// Function: __X
// Address: 00e8069c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__X() const */

undefined * std::__ndk1::__time_get_c_storage<wchar_t>::__X(void)

{
  int iVar1;
  
  if (((DAT_0231d148 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d148), iVar1 != 0)) {
                    /* try { // try from 00e806e4 to 00e806f7 has its CatchHandler @ 00e80724 */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
    basic_string<decltype(nullptr)>
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d130,L"%H:%M:%S");
    __cxa_atexit(PTR__basic_string_01ff58f0,&DAT_0231d130,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d148);
  }
  return &DAT_0231d130;
}



// ==========================================================================================
// Function: __c
// Address: 00e8073c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__c() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__c(void)

{
  int iVar1;
  
  if (((DAT_0231d168 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d168), iVar1 != 0)) {
    DAT_0231d150 = 0x28;
    DAT_0231d161 = 0x59252053;
    uRam000000000231d159._0_1_ = s__a__b__d__H__M__S__Y_005c0ae4[8];
    uRam000000000231d159._1_1_ = s__a__b__d__H__M__S__Y_005c0ae4[9];
    uRam000000000231d159._2_1_ = s__a__b__d__H__M__S__Y_005c0ae4[10];
    uRam000000000231d159._3_1_ = s__a__b__d__H__M__S__Y_005c0ae4[11];
    uRam000000000231d159._4_1_ = s__a__b__d__H__M__S__Y_005c0ae4[12];
    uRam000000000231d159._5_1_ = s__a__b__d__H__M__S__Y_005c0ae4[13];
    uRam000000000231d159._6_1_ = s__a__b__d__H__M__S__Y_005c0ae4[14];
    uRam000000000231d159._7_1_ = s__a__b__d__H__M__S__Y_005c0ae4[15];
    DAT_0231d151 = s__a__b__d__H__M__S__Y_005c0ae4[0];
    DAT_0231d151_1._0_1_ = s__a__b__d__H__M__S__Y_005c0ae4[1];
    DAT_0231d151_1._1_1_ = s__a__b__d__H__M__S__Y_005c0ae4[2];
    DAT_0231d151_1._2_1_ = s__a__b__d__H__M__S__Y_005c0ae4[3];
    DAT_0231d151_1._3_1_ = s__a__b__d__H__M__S__Y_005c0ae4[4];
    DAT_0231d151_1._4_1_ = s__a__b__d__H__M__S__Y_005c0ae4[5];
    DAT_0231d151_1._5_1_ = s__a__b__d__H__M__S__Y_005c0ae4[6];
    DAT_0231d151_1._6_1_ = s__a__b__d__H__M__S__Y_005c0ae4[7];
    DAT_0231d165 = 0;
    __cxa_atexit(PTR__basic_string_01ff5530,&DAT_0231d150,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d168);
  }
  return &DAT_0231d150;
}



// ==========================================================================================
// Function: __c
// Address: 00e807d0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__c() const */

undefined * std::__ndk1::__time_get_c_storage<wchar_t>::__c(void)

{
  int iVar1;
  
  if (((DAT_0231d188 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d188), iVar1 != 0)) {
                    /* try { // try from 00e80818 to 00e8082b has its CatchHandler @ 00e80858 */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
    basic_string<decltype(nullptr)>
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d170,L"%a %b %d %H:%M:%S %Y");
    __cxa_atexit(PTR__basic_string_01ff58f0,&DAT_0231d170,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d188);
  }
  return &DAT_0231d170;
}



// ==========================================================================================
// Function: __r
// Address: 00e80870
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<char>::__r() const */

undefined1 * std::__ndk1::__time_get_c_storage<char>::__r(void)

{
  int iVar1;
  
  if (((DAT_0231d1a8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d1a8), iVar1 != 0)) {
    DAT_0231d190 = 0x16;
    DAT_0231d191._0_7_ = (undefined7)s__I__M__S__p_005d1029._0_8_;
    ram0x0231d198 = CONCAT31(0x702520,SUB81(s__I__M__S__p_005d1029._0_8_,7));
    DAT_0231d19c = 0;
    __cxa_atexit(PTR__basic_string_01ff5530,&DAT_0231d190,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d1a8);
  }
  return &DAT_0231d190;
}



// ==========================================================================================
// Function: __r
// Address: 00e80904
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_c_storage<wchar_t>::__r() const */

undefined * std::__ndk1::__time_get_c_storage<wchar_t>::__r(void)

{
  int iVar1;
  
  if (((DAT_0231d1c8 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231d1c8), iVar1 != 0)) {
                    /* try { // try from 00e8094c to 00e8095f has its CatchHandler @ 00e8098c */
    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
    basic_string<decltype(nullptr)>
              ((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                *)&DAT_0231d1b0,L"%I:%M:%S %p");
    __cxa_atexit(PTR__basic_string_01ff58f0,&DAT_0231d1b0,&PTR_LOOP_01ecb1d0);
    __cxa_guard_release(&DAT_0231d1c8);
  }
  return &DAT_0231d1b0;
}



// ==========================================================================================
// Function: __time_get
// Address: 00e809a4
// ==========================================================================================

/* std::__ndk1::__time_get::__time_get(char const*) */

void __thiscall std::__ndk1::__time_get::__time_get(__time_get *this,char *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  size_t __n;
  undefined8 *puVar3;
  void *__dest;
  ulong uVar4;
  undefined8 local_68;
  size_t local_60;
  void *pvStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  p_Var2 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 != (__locale_t)0x0) {
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return;
    }
    goto LAB_00e80ab0;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_68 | 1);
    local_68 = CONCAT71(local_68._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e80a68;
  }
  else {
    uVar4 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar4);
    local_68 = uVar4 | 1;
    local_60 = __n;
    pvStack_58 = __dest;
LAB_00e80a68:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e80a7c to 00e80a8f has its CatchHandler @ 00e80ae4 */
  puVar3 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_68,0,"time_get_byname failed to construct for ");
  local_40 = puVar3[2];
  uStack_48 = puVar3[1];
  local_50 = *puVar3;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
                    /* try { // try from 00e80aa8 to 00e80aaf has its CatchHandler @ 00e80ab4 */
  FUN_00e78634(&local_50);
LAB_00e80ab0:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_get
// Address: 00e80b00
// ==========================================================================================

/* std::__ndk1::__time_get::__time_get(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&) */

void __thiscall std::__ndk1::__time_get::__time_get(__time_get *this,basic_string *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
    operator+(a_Stack_50,"time_get_byname failed to construct for ",param_1);
                    /* try { // try from 00e80b8c to 00e80b93 has its CatchHandler @ 00e80b98 */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~__time_get
// Address: 00e80bb4
// ==========================================================================================

/* std::__ndk1::__time_get::~__time_get() */

void __thiscall std::__ndk1::__time_get::~__time_get(__time_get *this)

{
                    /* try { // try from 00e80bc4 to 00e80bc7 has its CatchHandler @ 00e80bd4 */
  freelocale(*(__locale_t *)this);
  return;
}



// ==========================================================================================
// Function: __analyze
// Address: 00e80bd8
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::__time_get_storage<char>::__analyze(char, std::__ndk1::ctype<char> const&) */

void std::__ndk1::__time_get_storage<char>::__analyze(char param_1,ctype *param_2)

{
  __locale_t *pp_Var1;
  __locale_t *pp_Var2;
  byte *pbVar3;
  ulong uVar4;
  long lVar5;
  byte bVar6;
  uint uVar7;
  __locale_t *pp_Var8;
  size_t sVar9;
  long lVar10;
  long *in_x2;
  undefined8 *in_x8;
  __locale_t p_Var11;
  byte *pbVar12;
  byte *pbVar13;
  byte *pbVar14;
  int iVar15;
  int iVar16;
  byte *local_118;
  undefined local_110 [40];
  long lStack_e8;
  char *local_e0;
  undefined2 local_d8;
  byte local_d6 [102];
  long local_70;
  
  pp_Var8 = (__locale_t *)(ulong)(byte)param_1;
  lVar5 = tpidr_el0;
  local_70 = *(long *)(lVar5 + 0x28);
  lStack_e8 = 0;
  local_110._32_4_ = -1;
  local_110._36_4_ = 0;
  local_e0 = (char *)0x0;
  local_110._8_8_ = _UNK_005bd668;
  local_110._0_8_ = _DAT_005bd660;
  local_110._24_8_ = _UNK_005bda58;
  local_110._16_8_ = _DAT_005bda50;
  local_d6[0] = 0;
  local_d8 = CONCAT11((char)param_2,0x25);
  pbVar12 = local_d6 + 2;
  sVar9 = strftime_l((char *)(local_d6 + 2),100,(char *)&local_d8,(tm *)local_110,*pp_Var8);
  in_x8[1] = 0;
  in_x8[2] = 0;
  *in_x8 = 0;
  if (sVar9 != 0) {
    pbVar3 = pbVar12 + sVar9;
    pp_Var1 = pp_Var8 + 0x2b;
    pp_Var2 = pp_Var8 + 0x73;
    do {
      if (((char)*pbVar12 < '\0') || ((*(ulong *)(in_x2[2] + (ulong)*pbVar12 * 8) & 1) == 0)) {
        local_118 = pbVar12;
        lVar10 = FUN_00e81214(&local_118,pbVar3,pp_Var8 + 1,pp_Var1);
        lVar10 = lVar10 - (long)(pp_Var8 + 1);
        if (lVar10 < 0x150) {
          basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::push_back
                    ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      *)in_x8,'%');
          if (lVar10 < 0xa8) {
            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
            push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)in_x8,'A');
            pbVar12 = local_118;
          }
          else {
                    /* try { // try from 00e80cb0 to 00e80d87 has its CatchHandler @ 00e811f8 */
            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
            push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)in_x8,'a');
            pbVar12 = local_118;
          }
        }
        else {
          local_118 = pbVar12;
          lVar10 = FUN_00e81214(&local_118,pbVar3,pp_Var1,pp_Var2);
          lVar10 = lVar10 - (long)pp_Var1;
          if (lVar10 < 0x240) {
            basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
            push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)in_x8,'%');
            if (lVar10 < 0x120) {
              basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
              push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                         *)in_x8,'B');
            }
            else {
              basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
              push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                         *)in_x8,'b');
            }
            pbVar12 = local_118;
            if (((uint)param_2 & 0xff) == 0x78) {
              lVar10 = lVar10 >> 3;
              if ((*(byte *)(pp_Var8 + lVar10 + 0x2b) & 1) == 0) {
                bVar6 = *(byte *)((long)pp_Var8 + lVar10 * 8 + 0x159);
              }
              else {
                bVar6 = *(byte *)pp_Var8[lVar10 + 0x2d]->__locales;
              }
              if ((-1 < (char)bVar6) &&
                 (((uint)*(undefined8 *)(in_x2[2] + (ulong)bVar6 * 8) >> 6 & 1) != 0)) {
                uVar4 = (ulong)(*(byte *)in_x8 >> 1);
                lVar10 = (long)in_x8 + 1;
                if ((*(byte *)in_x8 & 1) != 0) {
                  uVar4 = in_x8[1];
                  lVar10 = in_x8[2];
                }
                *(undefined *)(lVar10 + uVar4 + -1) = 0x6d;
              }
            }
          }
          else {
            if ((*(byte *)pp_Var2 & 1) == 0) {
              p_Var11 = (__locale_t)(ulong)(*(byte *)pp_Var2 >> 1);
              bVar6 = *(byte *)(pp_Var8 + 0x76);
              if ((bVar6 & 1) != 0) goto LAB_00e80ddc;
LAB_00e80df8:
              lVar10 = (long)p_Var11->__locales + (ulong)(bVar6 >> 1);
            }
            else {
              p_Var11 = pp_Var8[0x74];
              bVar6 = *(byte *)(pp_Var8 + 0x76);
              if ((bVar6 & 1) == 0) goto LAB_00e80df8;
LAB_00e80ddc:
              lVar10 = (long)pp_Var8[0x77]->__locales + (long)p_Var11->__locales;
            }
                    /* try { // try from 00e80e08 to 00e80f47 has its CatchHandler @ 00e811f8 */
            if ((lVar10 == 0) ||
               (local_118 = pbVar12, lVar10 = FUN_00e81214(&local_118,pbVar3,pp_Var2,pp_Var8 + 0x79)
               , 0x2f < lVar10 - (long)pp_Var2)) {
              bVar6 = *pbVar12;
              if ((char)bVar6 < '\0') {
LAB_00e80ed8:
                local_118 = pbVar12;
                basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                           *)in_x8,bVar6);
              }
              else {
                if (((uint)*(undefined8 *)(in_x2[2] + (ulong)bVar6 * 8) >> 6 & 1) != 0) {
                  local_118 = pbVar12;
                  uVar7 = (**(code **)(*in_x2 + 0x48))();
                  iVar15 = (uVar7 & 0xff) - 0x30;
                  pbVar14 = pbVar3;
                  if (pbVar12 + 1 != pbVar3) {
                    iVar16 = 4;
                    do {
                      pbVar13 = pbVar12;
                      if (((char)pbVar13[1] < '\0') ||
                         (((uint)*(undefined8 *)(in_x2[2] + (ulong)pbVar13[1] * 8) >> 6 & 1) == 0))
                      {
                        pbVar14 = pbVar13 + 1;
                        goto LAB_00e80ff4;
                      }
                    /* try { // try from 00e80f84 to 00e80f8f has its CatchHandler @ 00e811f0 */
                      bVar6 = (**(code **)(*in_x2 + 0x48))();
                      iVar15 = iVar15 * 10 + (uint)bVar6 + -0x30;
                    } while ((2 < iVar16) &&
                            (iVar16 = iVar16 + -1, pbVar12 = pbVar13 + 1,
                            local_d6 + sVar9 != pbVar13));
                    if (local_d6 + sVar9 + 1 != pbVar13 + 1) {
                      pbVar14 = pbVar13 + 2;
                    }
                  }
LAB_00e80ff4:
                  pbVar12 = pbVar14;
                  switch(iVar15) {
                  case 6:
                    /* try { // try from 00e8101c to 00e8105f has its CatchHandler @ 00e811f8 */
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'w');
                    break;
                  case 7:
                    /* try { // try from 00e8109c to 00e811af has its CatchHandler @ 00e811f8 */
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'u');
                    break;
                  case 8:
                  case 9:
                  case 10:
                  case 0xd:
                  case 0xe:
                  case 0xf:
                  case 0x10:
                  case 0x11:
                  case 0x12:
                  case 0x13:
                  case 0x14:
                  case 0x15:
                  case 0x16:
                  case 0x18:
                  case 0x19:
                  case 0x1a:
                  case 0x1b:
                  case 0x1c:
                  case 0x1d:
                  case 0x1e:
                  case 0x20:
                  case 0x21:
                  case 0x22:
                  case 0x23:
                  case 0x24:
                  case 0x25:
                  case 0x26:
                  case 0x27:
                  case 0x28:
                  case 0x29:
                  case 0x2a:
                  case 0x2b:
                  case 0x2c:
                  case 0x2d:
                  case 0x2e:
                  case 0x2f:
                  case 0x30:
                  case 0x31:
                  case 0x32:
                  case 0x33:
                  case 0x34:
                  case 0x35:
                  case 0x36:
                  case 0x38:
                  case 0x39:
                  case 0x3a:
                  case 0x3c:
joined_r0x00e81070:
                    for (; local_118 != pbVar14; local_118 = local_118 + 1) {
                    /* try { // try from 00e81078 to 00e8107f has its CatchHandler @ 00e811ec */
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                   *)in_x8,*local_118);
                    }
                    break;
                  case 0xb:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'I');
                    break;
                  case 0xc:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'m');
                    break;
                  case 0x17:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'H');
                    break;
                  case 0x1f:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'d');
                    break;
                  case 0x37:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'M');
                    break;
                  case 0x3b:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'S');
                    break;
                  case 0x3d:
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'%');
                    basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                    push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                               *)in_x8,'y');
                    break;
                  default:
                    if (iVar15 == 0x16c) {
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                   *)in_x8,'%');
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                   *)in_x8,'j');
                    }
                    else {
                      if (iVar15 != 0x80d) goto joined_r0x00e81070;
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                   *)in_x8,'%');
                      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                      ::push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                                   *)in_x8,'Y');
                    }
                  }
                  goto LAB_00e80cc0;
                }
                if (bVar6 != 0x25) goto LAB_00e80ed8;
                local_118 = pbVar12;
                basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                           *)in_x8,'%');
                basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
                push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                           *)in_x8,'%');
              }
              pbVar12 = pbVar12 + 1;
            }
            else {
              basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
              push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                         *)in_x8,'%');
              basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
              push_back((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                         *)in_x8,'p');
              pbVar12 = local_118;
            }
          }
        }
      }
      else {
                    /* try { // try from 00e80d8c to 00e80d97 has its CatchHandler @ 00e811f4 */
        basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::push_back
                  ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *
                   )in_x8,' ');
        do {
          pbVar12 = pbVar12 + 1;
          if (pbVar3 == pbVar12) goto LAB_00e811b4;
        } while ((-1 < (char)*pbVar12) && ((*(ulong *)(in_x2[2] + (ulong)*pbVar12 * 8) & 1) != 0));
      }
LAB_00e80cc0:
    } while (pbVar12 != pbVar3);
  }
LAB_00e811b4:
  if (*(long *)(lVar5 + 0x28) == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __analyze
// Address: 00e81568
// ==========================================================================================

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* std::__ndk1::__time_get_storage<wchar_t>::__analyze(char, std::__ndk1::ctype<wchar_t> const&) */

void std::__ndk1::__time_get_storage<wchar_t>::__analyze(char param_1,ctype *param_2)

{
  __locale_t *pp_Var1;
  __locale_t *pp_Var2;
  wchar_t *pwVar3;
  long lVar4;
  byte bVar5;
  char cVar6;
  uint uVar7;
  __locale_t *pp_Var8;
  __locale_t p_Var9;
  size_t sVar10;
  ulong uVar11;
  long lVar12;
  long *in_x2;
  undefined8 *in_x8;
  wchar_t *pwVar13;
  wchar_t *pwVar14;
  wchar_t *pwVar15;
  int iVar16;
  wchar_t *local_2b8;
  char *local_2b0;
  mbstate_t mStack_2a8;
  undefined local_2a0 [40];
  long lStack_278;
  undefined8 local_270;
  undefined4 local_268;
  wchar_t local_264 [100];
  char acStack_d4 [100];
  long local_70;
  
  pp_Var8 = (__locale_t *)(ulong)(byte)param_1;
  lVar4 = tpidr_el0;
  local_70 = *(long *)(lVar4 + 0x28);
  lStack_278 = 0;
  local_2a0._32_4_ = -1;
  local_2a0._36_4_ = 0;
  local_270 = (char *)0x0;
  local_2a0._8_8_ = _UNK_005bd668;
  local_2a0._0_8_ = _DAT_005bd660;
  local_2a0._24_8_ = _UNK_005bda58;
  local_2a0._16_8_ = _DAT_005bda50;
  local_268._2_1_ = 0;
  local_268._0_2_ = CONCAT11((char)param_2,0x25);
  strftime_l(acStack_d4,100,(char *)&local_268,(tm *)local_2a0,*pp_Var8);
  mStack_2a8.__count = 0;
  mStack_2a8.__value = (_union_27)0x0;
  local_2b0 = acStack_d4;
  p_Var9 = uselocale(*pp_Var8);
                    /* try { // try from 00e8160c to 00e8161f has its CatchHandler @ 00e81c40 */
  sVar10 = mbsrtowcs(local_264,&local_2b0,100,&mStack_2a8);
  if (p_Var9 != (__locale_t)0x0) {
                    /* try { // try from 00e81628 to 00e8162f has its CatchHandler @ 00e81c3c */
    uselocale(p_Var9);
  }
  if (sVar10 == 0xffffffffffffffff) {
    __throw_runtime_error("locale not supported");
  }
  else {
    *in_x8 = 0;
    in_x8[1] = 0;
    in_x8[2] = 0;
    if (sVar10 != 0) {
      pp_Var1 = pp_Var8 + 0x73;
      pwVar13 = local_264;
      pwVar3 = pwVar13 + sVar10;
      pp_Var2 = pp_Var8 + 0x2b;
      do {
                    /* try { // try from 00e816a4 to 00e816bf has its CatchHandler @ 00e81c60 */
        uVar11 = (**(code **)(*in_x2 + 0x18))();
        if ((uVar11 & 1) == 0) {
                    /* try { // try from 00e816f4 to 00e81883 has its CatchHandler @ 00e81c64 */
          local_2b8 = pwVar13;
          lVar12 = FUN_00e81c84(&local_2b8,pwVar3,pp_Var8 + 1,pp_Var2);
          lVar12 = lVar12 - (long)(pp_Var8 + 1);
          if (lVar12 < 0x150) {
            basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                         *)in_x8,L'%');
            if (lVar12 < 0xa8) {
              basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                           *)in_x8,L'A');
              pwVar13 = local_2b8;
            }
            else {
                    /* try { // try from 00e81680 to 00e8168b has its CatchHandler @ 00e81c64 */
              basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                           *)in_x8,L'a');
              pwVar13 = local_2b8;
            }
          }
          else {
            local_2b8 = pwVar13;
            lVar12 = FUN_00e81c84(&local_2b8,pwVar3,pp_Var2,pp_Var1);
            if (lVar12 - (long)pp_Var2 < 0x240) {
              basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
              ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                           *)in_x8,L'%');
              if (lVar12 - (long)pp_Var2 < 0x120) {
                basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                             *)in_x8,L'B');
              }
              else {
                    /* try { // try from 00e81918 to 00e819bb has its CatchHandler @ 00e81c64 */
                basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                             *)in_x8,L'b');
              }
              pwVar13 = local_2b8;
              if ((((uint)param_2 & 0xff) == 0x78) &&
                 (uVar11 = (**(code **)(*in_x2 + 0x18))(), pwVar13 = local_2b8, (uVar11 & 1) != 0))
              {
                uVar11 = (ulong)(*(byte *)in_x8 >> 1);
                lVar12 = (long)in_x8 + 4;
                if ((*(byte *)in_x8 & 1) != 0) {
                  uVar11 = in_x8[1];
                  lVar12 = in_x8[2];
                }
                *(undefined4 *)(lVar12 + uVar11 * 4 + -4) = 0x6d;
              }
            }
            else {
              if ((*(byte *)pp_Var1 & 1) == 0) {
                p_Var9 = (__locale_t)(ulong)(*(byte *)pp_Var1 >> 1);
                bVar5 = *(byte *)(pp_Var8 + 0x76);
                if ((bVar5 & 1) != 0) goto LAB_00e817b4;
LAB_00e817d0:
                lVar12 = (long)p_Var9->__locales + (ulong)(bVar5 >> 1);
              }
              else {
                p_Var9 = pp_Var8[0x74];
                bVar5 = *(byte *)(pp_Var8 + 0x76);
                if ((bVar5 & 1) == 0) goto LAB_00e817d0;
LAB_00e817b4:
                lVar12 = (long)pp_Var8[0x77]->__locales + (long)p_Var9->__locales;
              }
              if ((lVar12 == 0) ||
                 (local_2b8 = pwVar13,
                 lVar12 = FUN_00e81c84(&local_2b8,pwVar3,pp_Var1,pp_Var8 + 0x79),
                 0x2f < lVar12 - (long)pp_Var1)) {
                local_2b8 = pwVar13;
                uVar11 = (**(code **)(*in_x2 + 0x18))();
                if ((uVar11 & 1) == 0) {
                  cVar6 = (**(code **)(*in_x2 + 0x68))();
                  if (cVar6 == '%') {
                    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                    ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                 *)in_x8,L'%');
                    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                    ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                 *)in_x8,L'%');
                  }
                  else {
                    /* try { // try from 00e81a30 to 00e81beb has its CatchHandler @ 00e81c64 */
                    basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                    ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                 *)in_x8,*pwVar13);
                  }
                  pwVar13 = pwVar13 + 1;
                }
                else {
                  uVar11 = (**(code **)(*in_x2 + 0x18))();
                  pwVar15 = pwVar13;
                  if ((uVar11 & 1) == 0) {
joined_r0x00e81a04:
                    for (; pwVar13 = pwVar15, local_2b8 != pwVar15; local_2b8 = local_2b8 + 1) {
                    /* try { // try from 00e81a0c to 00e81a13 has its CatchHandler @ 00e81c5c */
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,*local_2b8);
                    }
                  }
                  else {
                    uVar7 = (**(code **)(*in_x2 + 0x68))();
                    iVar16 = (uVar7 & 0xff) - 0x30;
                    pwVar15 = pwVar3;
                    if (pwVar13 + 1 != pwVar3) {
                      uVar7 = 4;
                      do {
                        pwVar14 = pwVar13;
                    /* try { // try from 00e818ac to 00e818d7 has its CatchHandler @ 00e81c58 */
                        uVar11 = (**(code **)(*in_x2 + 0x18))();
                        if ((uVar11 & 1) == 0) {
                          pwVar15 = pwVar14 + 1;
                          goto LAB_00e81a58;
                        }
                        bVar5 = (**(code **)(*in_x2 + 0x68))();
                        iVar16 = iVar16 * 10 + (uint)bVar5 + -0x30;
                      } while ((2 < uVar7) &&
                              (uVar7 = uVar7 - 1, pwVar13 = pwVar14 + 1,
                              (wchar_t *)(local_2a0 + sVar10 * 4 + 0x34) != pwVar14));
                      if ((wchar_t *)((long)&local_268 + sVar10 * 2 * 2) != pwVar14 + 1) {
                        pwVar15 = pwVar14 + 2;
                      }
                    }
LAB_00e81a58:
                    pwVar13 = pwVar15;
                    switch(iVar16) {
                    case 6:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'w');
                      break;
                    case 7:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'u');
                      break;
                    case 8:
                    case 9:
                    case 10:
                    case 0xd:
                    case 0xe:
                    case 0xf:
                    case 0x10:
                    case 0x11:
                    case 0x12:
                    case 0x13:
                    case 0x14:
                    case 0x15:
                    case 0x16:
                    case 0x18:
                    case 0x19:
                    case 0x1a:
                    case 0x1b:
                    case 0x1c:
                    case 0x1d:
                    case 0x1e:
                    case 0x20:
                    case 0x21:
                    case 0x22:
                    case 0x23:
                    case 0x24:
                    case 0x25:
                    case 0x26:
                    case 0x27:
                    case 0x28:
                    case 0x29:
                    case 0x2a:
                    case 0x2b:
                    case 0x2c:
                    case 0x2d:
                    case 0x2e:
                    case 0x2f:
                    case 0x30:
                    case 0x31:
                    case 0x32:
                    case 0x33:
                    case 0x34:
                    case 0x35:
                    case 0x36:
                    case 0x38:
                    case 0x39:
                    case 0x3a:
                    case 0x3c:
                      goto joined_r0x00e81a04;
                    case 0xb:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'I');
                      break;
                    case 0xc:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'm');
                      break;
                    case 0x17:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'H');
                      break;
                    case 0x1f:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'd');
                      break;
                    case 0x37:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'M');
                      break;
                    case 0x3b:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'S');
                      break;
                    case 0x3d:
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'%');
                      basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                      ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                   *)in_x8,L'y');
                      break;
                    default:
                      if (iVar16 == 0x16c) {
                        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                        ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                     *)in_x8,L'%');
                        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                        ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                     *)in_x8,L'j');
                      }
                      else {
                        if (iVar16 != 0x80d) goto joined_r0x00e81a04;
                        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                        ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                     *)in_x8,L'%');
                        basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                        ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                                     *)in_x8,L'Y');
                      }
                    }
                  }
                }
              }
              else {
                basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                             *)in_x8,L'%');
                basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                ::push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                             *)in_x8,L'p');
                pwVar13 = local_2b8;
              }
            }
          }
        }
        else {
          basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>::
          push_back((basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
                     *)in_x8,L' ');
          do {
            if ((wchar_t *)((long)&local_268 + sVar10 * 2 * 2) == pwVar13) goto LAB_00e81bf8;
                    /* try { // try from 00e816d4 to 00e816df has its CatchHandler @ 00e81c68 */
            uVar11 = (**(code **)(*in_x2 + 0x18))();
            pwVar13 = pwVar13 + 1;
          } while ((uVar11 & 1) != 0);
        }
      } while (pwVar13 != pwVar3);
    }
LAB_00e81bf8:
    if (*(long *)(lVar4 + 0x28) == local_70) {
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 00e82e3c
// ==========================================================================================

/* std::__ndk1::__time_get_storage<char>::__time_get_storage(char const*) */

void __thiscall
std::__ndk1::__time_get_storage<char>::__time_get_storage
          (__time_get_storage<char> *this,char *param_1)

{
  long lVar1;
  undefined **local_60 [2];
  void *local_50;
  char local_48;
  __locale_t local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __time_get::__time_get((__time_get *)this,param_1);
  memset(this + 8,0,0x420);
                    /* try { // try from 00e82e7c to 00e82e8b has its CatchHandler @ 00e82f78 */
  ctype_byname<char>::ctype_byname((ctype_byname<char> *)local_60,param_1,1);
  local_60[0] = &PTR__ctype_byname_01fbb6d0;
                    /* try { // try from 00e82e98 to 00e82ea3 has its CatchHandler @ 00e82f18 */
  init((ctype *)this);
  local_60[0] = (undefined **)(PTR_vtable_01ff58e0 + 0x10);
                    /* try { // try from 00e82eb8 to 00e82ebb has its CatchHandler @ 00e82f14 */
  freelocale(local_40);
  local_60[0] = (undefined **)(PTR_vtable_01ff5708 + 0x10);
  if ((local_50 != (void *)0x0) && (local_48 != '\0')) {
    operator_delete__(local_50);
  }
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)local_60);
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 00e83208
// ==========================================================================================

/* std::__ndk1::__time_get_storage<char>::__time_get_storage(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&) */

void __thiscall
std::__ndk1::__time_get_storage<char>::__time_get_storage
          (__time_get_storage<char> *this,basic_string *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  undefined **local_60 [2];
  void *local_50;
  char local_48;
  __locale_t local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
    operator+((__ndk1 *)local_60,"time_get_byname failed to construct for ",param_1);
                    /* try { // try from 00e83310 to 00e83317 has its CatchHandler @ 00e83594 */
    FUN_00e78634(local_60);
  }
  else {
    memset(this + 8,0,0x420);
                    /* try { // try from 00e83268 to 00e83277 has its CatchHandler @ 00e83380 */
    ctype_byname<char>::ctype_byname((ctype_byname<char> *)local_60,param_1,1);
    local_60[0] = &PTR__ctype_byname_01fbb6d0;
                    /* try { // try from 00e83284 to 00e8328f has its CatchHandler @ 00e83320 */
    init((ctype *)this);
    local_60[0] = (undefined **)(PTR_vtable_01ff58e0 + 0x10);
                    /* try { // try from 00e832a4 to 00e832a7 has its CatchHandler @ 00e8331c */
    freelocale(local_40);
    local_60[0] = (undefined **)(PTR_vtable_01ff5708 + 0x10);
    if ((local_50 != (void *)0x0) && (local_48 != '\0')) {
      operator_delete__(local_50);
    }
    __shared_weak_count::~__shared_weak_count((__shared_weak_count *)local_60);
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 00e835b0
// ==========================================================================================

/* std::__ndk1::__time_get_storage<wchar_t>::__time_get_storage(char const*) */

void __thiscall
std::__ndk1::__time_get_storage<wchar_t>::__time_get_storage
          (__time_get_storage<wchar_t> *this,char *param_1)

{
  long lVar1;
  undefined **local_50 [2];
  __locale_t local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __time_get::__time_get((__time_get *)this,param_1);
  memset(this + 8,0,0x420);
                    /* try { // try from 00e835f0 to 00e835ff has its CatchHandler @ 00e836a4 */
  ctype_byname<wchar_t>::ctype_byname((ctype_byname<wchar_t> *)local_50,param_1,1);
  local_50[0] = &PTR__ctype_byname_01fbb750;
                    /* try { // try from 00e8360c to 00e83617 has its CatchHandler @ 00e83668 */
  init((ctype *)this);
  local_50[0] = (undefined **)(PTR_vtable_01ff58e8 + 0x10);
                    /* try { // try from 00e8362c to 00e8362f has its CatchHandler @ 00e83664 */
  freelocale(local_40);
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)local_50);
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 00e83910
// ==========================================================================================

/* std::__ndk1::__time_get_storage<wchar_t>::__time_get_storage(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&) */

void __thiscall
std::__ndk1::__time_get_storage<wchar_t>::__time_get_storage
          (__time_get_storage<wchar_t> *this,basic_string *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  undefined **local_50 [2];
  __locale_t local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
    operator+((__ndk1 *)local_50,"time_get_byname failed to construct for ",param_1);
                    /* try { // try from 00e839f4 to 00e839fb has its CatchHandler @ 00e83c54 */
    FUN_00e78634(local_50);
  }
  else {
    memset(this + 8,0,0x420);
                    /* try { // try from 00e83970 to 00e8397f has its CatchHandler @ 00e83a40 */
    ctype_byname<wchar_t>::ctype_byname((ctype_byname<wchar_t> *)local_50,param_1,1);
    local_50[0] = &PTR__ctype_byname_01fbb750;
                    /* try { // try from 00e8398c to 00e83997 has its CatchHandler @ 00e83a04 */
    init((ctype *)this);
    local_50[0] = (undefined **)(PTR_vtable_01ff58e8 + 0x10);
                    /* try { // try from 00e839ac to 00e839af has its CatchHandler @ 00e83a00 */
    freelocale(local_40);
    __shared_weak_count::~__shared_weak_count((__shared_weak_count *)local_50);
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __do_date_order
// Address: 00e83c70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_storage<char>::__do_date_order() const */

undefined8 std::__ndk1::__time_get_storage<char>::__do_date_order(void)

{
  long lVar1;
  byte bVar2;
  char cVar3;
  uint uVar4;
  long in_x0;
  long lVar5;
  uint uVar6;
  int iVar7;
  ulong uVar8;
  long lVar9;
  ulong uVar10;
  
  bVar2 = *(byte *)(in_x0 + 0x3f8);
  lVar1 = in_x0 + 0x3f8;
  lVar5 = in_x0 + 0x3f9;
  uVar6 = 2;
  uVar4 = (uint)(bVar2 >> 1);
  do {
    uVar8 = (ulong)(uVar6 - 2);
    if ((bVar2 & 1) == 0) {
      lVar9 = lVar5;
      if ((uVar4 <= uVar6 - 2) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
    }
    else if ((*(ulong *)(in_x0 + 0x400) <= uVar8) ||
            (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) == '%')) {
      lVar9 = *(long *)(in_x0 + 0x408);
      break;
    }
    uVar6 = uVar6 + 1;
  } while( true );
  switch(*(undefined *)(lVar9 + (ulong)(uVar6 - 1))) {
  case 0x59:
  case 0x79:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar2 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83d08;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar9 = *(long *)(in_x0 + 0x408);
        goto LAB_00e83e28;
      }
      if ((uVar4 <= uVar6) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83d08:
      uVar6 = uVar6 + 1;
    }
    lVar9 = lVar5;
    if (uVar4 != uVar6) {
LAB_00e83e28:
      cVar3 = *(char *)(lVar9 + (ulong)(uVar6 + 1));
      iVar7 = uVar6 - 2;
      if (cVar3 == 'd') {
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar2 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83e48;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            lVar5 = *(long *)(in_x0 + 0x408);
            goto LAB_00e84020;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83e48:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
LAB_00e84020:
          if (*(char *)(lVar5 + (ulong)(iVar7 + 5)) == 'm') {
            return 4;
          }
        }
      }
      else if (cVar3 == 'm') {
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar2 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83ea4;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            lVar5 = *(long *)(in_x0 + 0x408);
            goto LAB_00e84044;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83ea4:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
LAB_00e84044:
          if (*(char *)(lVar5 + (ulong)(iVar7 + 5)) == 'd') {
            return 3;
          }
        }
      }
    }
    break;
  case 100:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar2 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83d64;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar5 = *(long *)(in_x0 + 0x408);
        goto LAB_00e83f98;
      }
      if ((uVar4 <= uVar6) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83d64:
      uVar6 = uVar6 + 1;
    }
    if (uVar4 != uVar6) {
LAB_00e83f98:
      if (*(char *)(lVar5 + (ulong)(uVar6 + 1)) == 'm') {
        iVar7 = uVar6 - 2;
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar2 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83fb0;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            cVar3 = *(char *)(*(long *)(in_x0 + 0x408) + (ulong)(iVar7 + 5));
            goto LAB_00e8409c;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83fb0:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
          cVar3 = *(char *)(lVar1 + (ulong)(iVar7 + 5) + 1);
LAB_00e8409c:
          if ((cVar3 == 'y') || (cVar3 == 'Y')) {
            return 1;
          }
        }
      }
    }
    break;
  case 0x6d:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar2 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83dc0;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar5 = *(long *)(in_x0 + 0x408);
        goto LAB_00e83f08;
      }
      if ((uVar4 <= uVar6) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83dc0:
      uVar6 = uVar6 + 1;
    }
    if (uVar4 != uVar6) {
LAB_00e83f08:
      if (*(char *)(lVar5 + (ulong)(uVar6 + 1)) == 'd') {
        iVar7 = uVar6 - 2;
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar2 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(char *)(*(long *)(in_x0 + 0x408) + uVar8) != '%') goto LAB_00e83f20;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            cVar3 = *(char *)(*(long *)(in_x0 + 0x408) + (ulong)(iVar7 + 5));
            if (cVar3 == 'y') {
              return 2;
            }
            goto LAB_00e840b4;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(char *)(lVar1 + uVar8 + 1) == '%')) break;
LAB_00e83f20:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
          cVar3 = *(char *)(lVar1 + (ulong)(iVar7 + 5) + 1);
          if (cVar3 == 'y') {
            return 2;
          }
LAB_00e840b4:
          if (cVar3 == 'Y') {
            return 2;
          }
        }
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: __do_date_order
// Address: 00e840d0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__time_get_storage<wchar_t>::__do_date_order() const */

undefined8 std::__ndk1::__time_get_storage<wchar_t>::__do_date_order(void)

{
  long lVar1;
  int iVar2;
  byte bVar3;
  uint uVar4;
  long in_x0;
  long lVar5;
  uint uVar6;
  int iVar7;
  ulong uVar8;
  long lVar9;
  ulong uVar10;
  
  bVar3 = *(byte *)(in_x0 + 0x3f8);
  lVar1 = in_x0 + 0x3f8;
  lVar5 = in_x0 + 0x3fc;
  uVar6 = 2;
  uVar4 = (uint)(bVar3 >> 1);
  do {
    uVar8 = (ulong)(uVar6 - 2);
    if ((bVar3 & 1) == 0) {
      lVar9 = lVar5;
      if ((uVar4 <= uVar6 - 2) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
    }
    else if ((*(ulong *)(in_x0 + 0x400) <= uVar8) ||
            (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) == 0x25)) {
      lVar9 = *(long *)(in_x0 + 0x408);
      break;
    }
    uVar6 = uVar6 + 1;
  } while( true );
  switch(*(undefined4 *)(lVar9 + (ulong)(uVar6 - 1) * 4)) {
  case 0x59:
  case 0x79:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar3 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e84168;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar9 = *(long *)(in_x0 + 0x408);
        goto LAB_00e84288;
      }
      if ((uVar4 <= uVar6) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e84168:
      uVar6 = uVar6 + 1;
    }
    lVar9 = lVar5;
    if (uVar4 != uVar6) {
LAB_00e84288:
      iVar2 = *(int *)(lVar9 + (ulong)(uVar6 + 1) * 4);
      iVar7 = uVar6 - 2;
      if (iVar2 == 100) {
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar3 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e842a8;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            lVar5 = *(long *)(in_x0 + 0x408);
            goto LAB_00e84480;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e842a8:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
LAB_00e84480:
          if (*(int *)(lVar5 + (ulong)(iVar7 + 5) * 4) == 0x6d) {
            return 4;
          }
        }
      }
      else if (iVar2 == 0x6d) {
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar3 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e84304;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            lVar5 = *(long *)(in_x0 + 0x408);
            goto LAB_00e844a4;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e84304:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
LAB_00e844a4:
          if (*(int *)(lVar5 + (ulong)(iVar7 + 5) * 4) == 100) {
            return 3;
          }
        }
      }
    }
    break;
  case 100:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar3 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e841c4;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar5 = *(long *)(in_x0 + 0x408);
        goto LAB_00e843f8;
      }
      if ((uVar4 <= uVar6) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e841c4:
      uVar6 = uVar6 + 1;
    }
    if (uVar4 != uVar6) {
LAB_00e843f8:
      if (*(int *)(lVar5 + (ulong)(uVar6 + 1) * 4) == 0x6d) {
        iVar7 = uVar6 - 2;
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar3 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e84410;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            iVar7 = *(int *)(*(long *)(in_x0 + 0x408) + (ulong)(iVar7 + 5) * 4);
            goto LAB_00e844fc;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e84410:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
          iVar7 = *(int *)(lVar1 + (ulong)(iVar7 + 5) * 4 + 4);
LAB_00e844fc:
          if ((iVar7 == 0x79) || (iVar7 == 0x59)) {
            return 1;
          }
        }
      }
    }
    break;
  case 0x6d:
    while( true ) {
      uVar8 = (ulong)uVar6;
      if ((bVar3 & 1) != 0) {
        uVar10 = *(ulong *)(in_x0 + 0x400);
        if (uVar8 < uVar10) {
          if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e84220;
          uVar10 = *(ulong *)(in_x0 + 0x400);
        }
        if (uVar10 == uVar8) {
          return 0;
        }
        lVar5 = *(long *)(in_x0 + 0x408);
        goto LAB_00e84368;
      }
      if ((uVar4 <= uVar6) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e84220:
      uVar6 = uVar6 + 1;
    }
    if (uVar4 != uVar6) {
LAB_00e84368:
      if (*(int *)(lVar5 + (ulong)(uVar6 + 1) * 4) == 100) {
        iVar7 = uVar6 - 2;
        while( true ) {
          uVar8 = (ulong)(iVar7 + 4U);
          if ((bVar3 & 1) != 0) {
            uVar10 = *(ulong *)(in_x0 + 0x400);
            if (uVar8 < uVar10) {
              if (*(int *)(*(long *)(in_x0 + 0x408) + uVar8 * 4) != 0x25) goto LAB_00e84380;
              uVar10 = *(ulong *)(in_x0 + 0x400);
            }
            if (uVar10 == iVar7 + 4) {
              return 0;
            }
            iVar7 = *(int *)(*(long *)(in_x0 + 0x408) + (ulong)(iVar7 + 5) * 4);
            if (iVar7 == 0x79) {
              return 2;
            }
            goto LAB_00e84514;
          }
          if ((uVar4 <= iVar7 + 4U) || (*(int *)(lVar1 + uVar8 * 4 + 4) == 0x25)) break;
LAB_00e84380:
          iVar7 = iVar7 + 1;
        }
        if (uVar4 - 4 != iVar7) {
          iVar7 = *(int *)(lVar1 + (ulong)(iVar7 + 5) * 4 + 4);
          if (iVar7 == 0x79) {
            return 2;
          }
LAB_00e84514:
          if (iVar7 == 0x59) {
            return 2;
          }
        }
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: __time_put
// Address: 00e84530
// ==========================================================================================

/* std::__ndk1::__time_put::__time_put(char const*) */

void __thiscall std::__ndk1::__time_put::__time_put(__time_put *this,char *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  size_t __n;
  undefined8 *puVar3;
  void *__dest;
  ulong uVar4;
  undefined8 local_68;
  size_t local_60;
  void *pvStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  p_Var2 = newlocale(0x1fbf,param_1,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 != (__locale_t)0x0) {
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return;
    }
    goto LAB_00e8463c;
  }
  __n = strlen(param_1);
  if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (__n < 0x17) {
    __dest = (void *)((ulong)&local_68 | 1);
    local_68 = CONCAT71(local_68._1_7_,(char)((int)__n << 1));
    if (__n != 0) goto LAB_00e845f4;
  }
  else {
    uVar4 = __n + 0x10 & 0xfffffffffffffff0;
    __dest = operator_new(uVar4);
    local_68 = uVar4 | 1;
    local_60 = __n;
    pvStack_58 = __dest;
LAB_00e845f4:
    memcpy(__dest,param_1,__n);
  }
  *(undefined *)((long)__dest + __n) = 0;
                    /* try { // try from 00e84608 to 00e8461b has its CatchHandler @ 00e84670 */
  puVar3 = (undefined8 *)
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::insert
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&local_68,0,"time_put_byname failed to construct for ");
  local_40 = puVar3[2];
  uStack_48 = puVar3[1];
  local_50 = *puVar3;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
                    /* try { // try from 00e84634 to 00e8463b has its CatchHandler @ 00e84640 */
  FUN_00e78634(&local_50);
LAB_00e8463c:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __time_put
// Address: 00e8468c
// ==========================================================================================

/* std::__ndk1::__time_put::__time_put(std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&) */

void __thiscall std::__ndk1::__time_put::__time_put(__time_put *this,basic_string *param_1)

{
  long lVar1;
  __locale_t p_Var2;
  basic_string *__locale;
  __ndk1 a_Stack_50 [24];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  __locale = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __locale = param_1 + 1;
  }
  p_Var2 = newlocale(0x1fbf,(char *)__locale,(__locale_t)0x0);
  *(__locale_t *)this = p_Var2;
  if (p_Var2 == (__locale_t)0x0) {
    operator+(a_Stack_50,"time_put_byname failed to construct for ",param_1);
                    /* try { // try from 00e84718 to 00e8471f has its CatchHandler @ 00e84724 */
    FUN_00e78634(a_Stack_50);
  }
  else if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: ~__time_put
// Address: 00e84740
// ==========================================================================================

/* std::__ndk1::__time_put::~__time_put() */

void __thiscall std::__ndk1::__time_put::~__time_put(__time_put *this)

{
  int iVar1;
  __locale_t p_Var2;
  
  p_Var2 = *(__locale_t *)this;
  if (((DAT_0231cfb0 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231cfb0), iVar1 != 0)) {
                    /* try { // try from 00e847a8 to 00e847bb has its CatchHandler @ 00e847d0 */
    DAT_0231cfa8 = newlocale(0x1fbf,"C",(__locale_t)0x0);
    __cxa_guard_release(&DAT_0231cfb0);
  }
  if (p_Var2 != DAT_0231cfa8) {
                    /* try { // try from 00e84780 to 00e84783 has its CatchHandler @ 00e847e8 */
    freelocale(*(__locale_t *)this);
  }
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8
// Address: 00e86c7c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<wchar_t>::~__codecvt_utf8() */

void __thiscall std::__ndk1::__codecvt_utf8<wchar_t>::~__codecvt_utf8(__codecvt_utf8<wchar_t> *this)

{
  codecvt<wchar_t,char,mbstate_t>::~codecvt((codecvt<wchar_t,char,mbstate_t> *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8
// Address: 00e86ca8
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char16_t>::~__codecvt_utf8() */

void __thiscall
std::__ndk1::__codecvt_utf8<char16_t>::~__codecvt_utf8(__codecvt_utf8<char16_t> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8
// Address: 00e86cd4
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8<char32_t>::~__codecvt_utf8() */

void __thiscall
std::__ndk1::__codecvt_utf8<char32_t>::~__codecvt_utf8(__codecvt_utf8<char32_t> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86d00
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, false>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,false>::~__codecvt_utf16(__codecvt_utf16<wchar_t,false> *this)

{
  codecvt<wchar_t,char,mbstate_t>::~codecvt((codecvt<wchar_t,char,mbstate_t> *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86d2c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<wchar_t, true>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<wchar_t,true>::~__codecvt_utf16(__codecvt_utf16<wchar_t,true> *this)

{
  codecvt<wchar_t,char,mbstate_t>::~codecvt((codecvt<wchar_t,char,mbstate_t> *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86d58
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, false>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<char16_t,false>::~__codecvt_utf16
          (__codecvt_utf16<char16_t,false> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86d84
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char16_t, true>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<char16_t,true>::~__codecvt_utf16(__codecvt_utf16<char16_t,true> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86db0
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, false>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<char32_t,false>::~__codecvt_utf16
          (__codecvt_utf16<char32_t,false> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf16
// Address: 00e86ddc
// ==========================================================================================

/* std::__ndk1::__codecvt_utf16<char32_t, true>::~__codecvt_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf16<char32_t,true>::~__codecvt_utf16(__codecvt_utf16<char32_t,true> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8_utf16
// Address: 00e86ed4
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<wchar_t>::~__codecvt_utf8_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<wchar_t>::~__codecvt_utf8_utf16
          (__codecvt_utf8_utf16<wchar_t> *this)

{
  codecvt<wchar_t,char,mbstate_t>::~codecvt((codecvt<wchar_t,char,mbstate_t> *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8_utf16
// Address: 00e86f00
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char32_t>::~__codecvt_utf8_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char32_t>::~__codecvt_utf8_utf16
          (__codecvt_utf8_utf16<char32_t> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__codecvt_utf8_utf16
// Address: 00e86f2c
// ==========================================================================================

/* std::__ndk1::__codecvt_utf8_utf16<char16_t>::~__codecvt_utf8_utf16() */

void __thiscall
std::__ndk1::__codecvt_utf8_utf16<char16_t>::~__codecvt_utf8_utf16
          (__codecvt_utf8_utf16<char16_t> *this)

{
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~__shared_weak_count
// Address: 00e87008
// ==========================================================================================

void __thiscall std::__ndk1::__shared_weak_count::~__shared_weak_count(__shared_weak_count *this)

{
  ~__shared_weak_count(this);
  return;
}



// ==========================================================================================
// Function: ~__shared_weak_count
// Address: 00e8703c
// ==========================================================================================

void __thiscall std::__ndk1::__shared_weak_count::~__shared_weak_count(__shared_weak_count *this)

{
  ~__shared_weak_count(this);
  return;
}



// ==========================================================================================
// Function: __append_forward_unsafe<char*>
// Address: 00e88d1c
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >&
   std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__append_forward_unsafe<char*>(char*, char*) */

basic_string * __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__append_forward_unsafe<char*>
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          char *param_1,char *param_2)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> bVar1;
  long lVar2;
  undefined8 *puVar3;
  ulong uVar4;
  ulong uVar5;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar6;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  ulong __n;
  ulong uVar10;
  char *pcVar11;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *pbVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 local_70;
  ulong local_68;
  char *local_60;
  long local_58;
  
  lVar2 = tpidr_el0;
  local_58 = *(long *)(lVar2 + 0x28);
  bVar1 = *this;
  uVar5 = (ulong)(byte)bVar1;
  __n = (long)param_2 - (long)param_1;
  if (((byte)bVar1 & 1) == 0) {
    if (__n == 0) goto LAB_00e88f28;
    uVar10 = (ulong)((byte)bVar1 >> 1);
    pbVar12 = this + 1;
    uVar4 = 0x16;
  }
  else {
    if (__n == 0) goto LAB_00e88f28;
    uVar5 = *(ulong *)this;
    uVar10 = *(ulong *)(this + 8);
    pbVar12 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
               (this + 0x10);
    uVar4 = (uVar5 & 0xfffffffffffffffe) - 1;
  }
  if ((pbVar12 <= param_1) && (param_1 < pbVar12 + uVar10)) {
    if (0xffffffffffffffef < __n) {
                    /* WARNING: Subroutine does not return */
      __basic_string_common<true>::__throw_length_error();
    }
    if (__n < 0x17) {
      local_70 = CONCAT71(local_70._1_7_,(char)((int)__n << 1));
      pcVar11 = (char *)((ulong)&local_70 | 1);
    }
    else {
      uVar5 = __n + 0x10 & 0xfffffffffffffff0;
      pcVar11 = (char *)operator_new(uVar5);
      local_70 = uVar5 | 1;
      local_68 = __n;
      local_60 = pcVar11;
    }
    if (param_1 != param_2) {
      memcpy(pcVar11,param_1,__n);
      pcVar11 = pcVar11 + __n;
    }
    *pcVar11 = '\0';
    uVar5 = local_70 >> 1 & 0x7f;
    pcVar11 = (char *)((ulong)&local_70 | 1);
    if ((local_70 & 1) != 0) {
      uVar5 = local_68;
      pcVar11 = local_60;
    }
                    /* try { // try from 00e88f10 to 00e88f17 has its CatchHandler @ 00e88f68 */
    append(this,pcVar11,uVar5);
    if ((local_70 & 1) != 0) {
      operator_delete(local_60);
    }
    goto LAB_00e88f28;
  }
  if (uVar4 - uVar10 < __n) {
    __grow_by(this,uVar4,(__n + uVar10) - uVar4,uVar10,uVar10,0,0);
    uVar5 = (ulong)(byte)*this;
  }
  if ((uVar5 & 1) == 0) {
    pbVar12 = this + 1;
  }
  else {
    pbVar12 = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
               (this + 0x10);
  }
  pbVar7 = pbVar12 + uVar10;
  if (param_1 != param_2) {
    pbVar6 = pbVar7;
    if ((0x1f < __n) &&
       ((param_2 <= pbVar7 || (pbVar12 + (long)(param_2 + (uVar10 - (long)param_1)) <= param_1)))) {
      uVar4 = __n & 0xffffffffffffffe0;
      puVar9 = (undefined8 *)(param_1 + 0x10);
      pbVar7 = pbVar7 + uVar4;
      puVar8 = (undefined8 *)(pbVar12 + uVar10 + 0x10);
      uVar5 = uVar4;
      do {
        puVar3 = puVar9 + -1;
        uVar13 = puVar9[-2];
        uVar15 = puVar9[1];
        uVar14 = *puVar9;
        puVar9 = puVar9 + 4;
        uVar5 = uVar5 - 0x20;
        puVar8[-1] = *puVar3;
        puVar8[-2] = uVar13;
        puVar8[1] = uVar15;
        *puVar8 = uVar14;
        puVar8 = puVar8 + 4;
      } while (uVar5 != 0);
      pbVar6 = pbVar7;
      param_1 = (char *)(param_1 + uVar4);
      if (__n == uVar4) goto LAB_00e88e8c;
    }
    do {
      pbVar12 = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
                param_1 + 1;
      pbVar7 = pbVar6 + 1;
      *pbVar6 = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)
                *param_1;
      pbVar6 = pbVar7;
      param_1 = (char *)pbVar12;
    } while ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             param_2 != pbVar12);
  }
LAB_00e88e8c:
  *pbVar7 = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)0x0;
  if (((byte)*this & 1) == 0) {
    *this = SUB41((int)(__n + uVar10) << 1,0);
  }
  else {
    *(ulong *)(this + 8) = __n + uVar10;
  }
LAB_00e88f28:
  if (*(long *)(lVar2 + 0x28) != local_58) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return (basic_string *)this;
}



// ==========================================================================================
// Function: __append_forward_unsafe<wchar_t*>
// Address: 00e88f84
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >& std::__ndk1::basic_string<wchar_t,
   std::__ndk1::char_traits<wchar_t>, std::__ndk1::allocator<wchar_t>
   >::__append_forward_unsafe<wchar_t*>(wchar_t*, wchar_t*) */

basic_string * __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__append_forward_unsafe<wchar_t*>
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,wchar_t *param_1,wchar_t *param_2)

{
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> bVar1;
  long lVar2;
  undefined8 *puVar3;
  ulong uVar4;
  ulong uVar5;
  wchar_t *pwVar6;
  basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>> *pbVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  ulong uVar10;
  wchar_t *pwVar11;
  wchar_t *pwVar12;
  ulong uVar13;
  ulong uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 local_70;
  ulong local_68;
  wchar_t *local_60;
  long local_58;
  
  lVar2 = tpidr_el0;
  local_58 = *(long *)(lVar2 + 0x28);
  bVar1 = *this;
  uVar5 = (ulong)(byte)bVar1;
  uVar14 = (long)param_2 - (long)param_1;
  if (((byte)bVar1 & 1) == 0) {
    if (uVar14 == 0) goto LAB_00e891b0;
    uVar10 = (ulong)((byte)bVar1 >> 1);
    pwVar11 = (wchar_t *)(this + 4);
    uVar4 = 4;
  }
  else {
    if (uVar14 == 0) goto LAB_00e891b0;
    uVar5 = *(ulong *)this;
    uVar10 = *(ulong *)(this + 8);
    pwVar11 = *(wchar_t **)(this + 0x10);
    uVar4 = (uVar5 & 0xfffffffffffffffe) - 1;
  }
  uVar13 = (long)uVar14 >> 2;
  if ((pwVar11 <= param_1) && (param_1 < pwVar11 + uVar10)) {
    if ((long)uVar14 < 0) {
                    /* WARNING: Subroutine does not return */
      __basic_string_common<true>::__throw_length_error();
    }
    if (uVar13 < 5) {
      local_70 = CONCAT71(local_70._1_7_,(char)(uVar14 >> 1)) & 0xfffffffffffffffe;
      pwVar11 = (wchar_t *)((ulong)&local_70 | 4);
    }
    else {
      uVar5 = uVar13 + 4 & 0xfffffffffffffffc;
      pwVar11 = (wchar_t *)operator_new(uVar5 << 2);
      local_70 = uVar5 | 1;
      local_68 = uVar13;
      local_60 = pwVar11;
    }
    if (param_1 != param_2) {
      memcpy(pwVar11,param_1,uVar14 & 0xfffffffffffffffc);
      pwVar11 = (wchar_t *)((long)pwVar11 + (uVar14 - 4 & 0xfffffffffffffffc) + 4);
    }
    *pwVar11 = L'\0';
    uVar5 = local_70 >> 1 & 0x7f;
    pwVar11 = (wchar_t *)((ulong)&local_70 | 4);
    if ((local_70 & 1) != 0) {
      uVar5 = local_68;
      pwVar11 = local_60;
    }
                    /* try { // try from 00e89198 to 00e8919f has its CatchHandler @ 00e891f0 */
    append(this,pwVar11,uVar5);
    if ((local_70 & 1) != 0) {
      operator_delete(local_60);
    }
    goto LAB_00e891b0;
  }
  if (uVar4 - uVar10 < uVar13) {
    __grow_by(this,uVar4,(uVar13 + uVar10) - uVar4,uVar10,uVar10,0,0);
    uVar5 = (ulong)(byte)*this;
  }
  if ((uVar5 & 1) == 0) {
    pbVar7 = this + 4;
  }
  else {
    pbVar7 = *(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
               **)(this + 0x10);
  }
  pwVar11 = (wchar_t *)(pbVar7 + uVar10 * 4);
  if (param_1 != param_2) {
    uVar14 = uVar14 - 4;
    pwVar6 = pwVar11;
    if ((0x1b < uVar14) &&
       (((wchar_t *)((long)param_1 + (uVar14 & 0xfffffffffffffffc) + 4) <= pwVar11 ||
        (pbVar7 + (uVar10 + (uVar14 >> 2)) * 4 + 4 <= param_1)))) {
      uVar5 = (uVar14 >> 2) + 1;
      uVar4 = uVar5 & 0x7ffffffffffffff8;
      puVar8 = (undefined8 *)(param_1 + 4);
      pwVar11 = pwVar11 + uVar4;
      puVar9 = (undefined8 *)(pbVar7 + uVar10 * 4 + 0x10);
      uVar14 = uVar4;
      do {
        puVar3 = puVar8 + -1;
        uVar15 = puVar8[-2];
        uVar17 = puVar8[1];
        uVar16 = *puVar8;
        puVar8 = puVar8 + 4;
        uVar14 = uVar14 - 8;
        puVar9[-1] = *puVar3;
        puVar9[-2] = uVar15;
        puVar9[1] = uVar17;
        *puVar9 = uVar16;
        puVar9 = puVar9 + 4;
      } while (uVar14 != 0);
      pwVar6 = pwVar11;
      param_1 = param_1 + uVar4;
      if (uVar5 == uVar4) goto LAB_00e89108;
    }
    do {
      pwVar12 = param_1 + 1;
      pwVar11 = pwVar6 + 1;
      *pwVar6 = *param_1;
      pwVar6 = pwVar11;
      param_1 = pwVar12;
    } while (param_2 != pwVar12);
  }
LAB_00e89108:
  *pwVar11 = L'\0';
  if (((byte)*this & 1) == 0) {
    *this = SUB41((int)(uVar13 + uVar10) << 1,0);
  }
  else {
    *(ulong *)(this + 8) = uVar13 + uVar10;
  }
LAB_00e891b0:
  if (*(long *)(lVar2 + 0x28) != local_58) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return (basic_string *)this;
}



// ==========================================================================================
// Function: ~__shared_weak_count
// Address: 00e896b0
// ==========================================================================================

/* std::__ndk1::__shared_weak_count::~__shared_weak_count() */

void __thiscall std::__ndk1::__shared_weak_count::~__shared_weak_count(__shared_weak_count *this)

{
  return;
}



// ==========================================================================================
// Function: ~__shared_count
// Address: 00e896b8
// ==========================================================================================

/* std::__ndk1::__shared_count::~__shared_count() */

void __thiscall std::__ndk1::__shared_count::~__shared_count(__shared_count *this)

{
  code *UNRECOVERED_JUMPTABLE;
  
                    /* WARNING: Treating indirect jump as call */
  UNRECOVERED_JUMPTABLE = (code *)SoftwareBreakpoint(1,0xe896c0);
  (*UNRECOVERED_JUMPTABLE)();
  return;
}



// ==========================================================================================
// Function: ~__shared_weak_count
// Address: 00e896c0
// ==========================================================================================

/* std::__ndk1::__shared_weak_count::~__shared_weak_count() */

void __thiscall std::__ndk1::__shared_weak_count::~__shared_weak_count(__shared_weak_count *this)

{
  code *UNRECOVERED_JUMPTABLE;
  
                    /* WARNING: Treating indirect jump as call */
  UNRECOVERED_JUMPTABLE = (code *)SoftwareBreakpoint(1,0xe896c8);
  (*UNRECOVERED_JUMPTABLE)();
  return;
}



// ==========================================================================================
// Function: __add_shared
// Address: 00e896c8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_count::__add_shared() */

void std::__ndk1::__shared_count::__add_shared(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long in_x0;
  
  plVar1 = (long *)(in_x0 + 8);
  do {
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
    if (bVar3) {
      *plVar1 = *plVar1 + 1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  return;
}



// ==========================================================================================
// Function: __release_shared
// Address: 00e896e4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_count::__release_shared() */

bool std::__ndk1::__shared_count::__release_shared(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long *in_x0;
  long lVar4;
  
  plVar1 = in_x0 + 1;
  do {
    lVar4 = *plVar1;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
    if (bVar3) {
      *plVar1 = lVar4 + -1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  if (lVar4 == 0) {
    (**(code **)(*in_x0 + 0x10))();
  }
  return lVar4 == 0;
}



// ==========================================================================================
// Function: __add_shared
// Address: 00e89730
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_weak_count::__add_shared() */

void std::__ndk1::__shared_weak_count::__add_shared(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long in_x0;
  
  plVar1 = (long *)(in_x0 + 8);
  do {
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
    if (bVar3) {
      *plVar1 = *plVar1 + 1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  return;
}



// ==========================================================================================
// Function: __add_weak
// Address: 00e8974c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_weak_count::__add_weak() */

void std::__ndk1::__shared_weak_count::__add_weak(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long in_x0;
  
  plVar1 = (long *)(in_x0 + 0x10);
  do {
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
    if (bVar3) {
      *plVar1 = *plVar1 + 1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  return;
}



// ==========================================================================================
// Function: __release_shared
// Address: 00e89768
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_weak_count::__release_shared() */

void std::__ndk1::__shared_weak_count::__release_shared(void)

{
  char cVar1;
  bool bVar2;
  long *in_x0;
  long lVar3;
  long *plVar4;
  
  plVar4 = in_x0 + 1;
  do {
    lVar3 = *plVar4;
    cVar1 = '\x01';
    bVar2 = (bool)ExclusiveMonitorPass(plVar4,0x10);
    if (bVar2) {
      *plVar4 = lVar3 + -1;
      cVar1 = ExclusiveMonitorsStatus();
    }
  } while (cVar1 != '\0');
  if (lVar3 != 0) {
    return;
  }
  plVar4 = in_x0 + 2;
  (**(code **)(*in_x0 + 0x10))();
  if (*plVar4 != 0) {
    do {
      lVar3 = *plVar4;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(plVar4,0x10);
      if (bVar2) {
        *plVar4 = lVar3 + -1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (lVar3 != 0) {
      return;
    }
  }
                    /* WARNING: Could not recover jumptable at 0x00e897ec. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*in_x0 + 0x20))();
  return;
}



// ==========================================================================================
// Function: __release_weak
// Address: 00e897f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__shared_weak_count::__release_weak() */

void std::__ndk1::__shared_weak_count::__release_weak(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long *in_x0;
  long lVar4;
  
  plVar1 = in_x0 + 2;
  if (*plVar1 != 0) {
    do {
      lVar4 = *plVar1;
      cVar2 = '\x01';
      bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
      if (bVar3) {
        *plVar1 = lVar4 + -1;
        cVar2 = ExclusiveMonitorsStatus();
      }
    } while (cVar2 != '\0');
    if (lVar4 != 0) {
      return;
    }
  }
                    /* WARNING: Could not recover jumptable at 0x00e89820. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*in_x0 + 0x20))();
  return;
}



// ==========================================================================================
// Function: __get_deleter
// Address: 00e89878
// ==========================================================================================

/* std::__ndk1::__shared_weak_count::__get_deleter(std::type_info const&) const */

undefined8 std::__ndk1::__shared_weak_count::__get_deleter(type_info *param_1)

{
  return 0;
}



// ==========================================================================================
// Function: __get_sp_mut
// Address: 00e89900
// ==========================================================================================

/* std::__ndk1::__get_sp_mut(void const*) */

int std::__ndk1::__get_sp_mut(void *param_1)

{
  long lVar1;
  ulong uVar2;
  
  uVar2 = ((ulong)(uint)((int)param_1 << 3) + 8 ^ (ulong)param_1 >> 0x20) * -0x622015f714c7d297;
  lVar1 = (uVar2 ^ (ulong)param_1 >> 0x20 ^ uVar2 >> 0x2f) * -0x622015f714c7d297;
  return (((uint)((ulong)lVar1 >> 0x2f) ^ (uint)lVar1) * 0x2d69 & 0xf) * 8 + 0x20ff470;
}



// ==========================================================================================
// Function: __undeclare_reachable
// Address: 00e89980
// ==========================================================================================

/* std::__ndk1::__undeclare_reachable(void*) */

void std::__ndk1::__undeclare_reachable(void *param_1)

{
  return;
}



// ==========================================================================================
// Function: __call_once
// Address: 00e8a074
// ==========================================================================================

/* std::__ndk1::__call_once(unsigned long volatile&, void*, void (*)(void*)) */

int std::__ndk1::__call_once(ulong *param_1,void *param_2,_func_void_void_ptr *param_3)

{
  int iVar1;
  ulong uVar2;
  
  pthread_mutex_lock((pthread_mutex_t *)&DAT_0231dfa0);
  uVar2 = *param_1;
  while (uVar2 == 1) {
    pthread_cond_wait((pthread_cond_t *)&DAT_0231dfc8,(pthread_mutex_t *)&DAT_0231dfa0);
    uVar2 = *param_1;
  }
  if (*param_1 != 0) {
    iVar1 = pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231dfa0);
    return iVar1;
  }
  *param_1 = 1;
                    /* try { // try from 00e8a108 to 00e8a147 has its CatchHandler @ 00e8a160 */
  pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231dfa0);
  (*param_3)(param_2);
  pthread_mutex_lock((pthread_mutex_t *)&DAT_0231dfa0);
  *param_1 = 0xffffffffffffffff;
  pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231dfa0);
  iVar1 = pthread_cond_broadcast((pthread_cond_t *)&DAT_0231dfc8);
  return iVar1;
}



// ==========================================================================================
// Function: __do_timed_wait
// Address: 00e8a234
// ==========================================================================================

/* std::__ndk1::condition_variable::__do_timed_wait(std::__ndk1::unique_lock<std::__ndk1::mutex>&,
   std::__ndk1::chrono::time_point<std::__ndk1::chrono::system_clock,
   std::__ndk1::chrono::duration<long long, std::__ndk1::ratio<1l, 1000000000l> > >) */

void __thiscall
std::__ndk1::condition_variable::__do_timed_wait
          (condition_variable *this,unique_lock *param_1,time_point param_2)

{
  long lVar1;
  int iVar2;
  timespec local_38;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  if (param_1[8] == (unique_lock)0x0) {
                    /* try { // try from 00e8a2d8 to 00e8a2e7 has its CatchHandler @ 00e8a2f8 */
                    /* WARNING: Subroutine does not return */
    __throw_system_error(1,"condition_variable::timed wait: mutex not locked");
  }
  local_38.tv_nsec = (ulong)param_2;
  if (0x59682f000000e940 < (ulong)param_2) {
    local_38.tv_nsec = 0x59682f000000e941;
  }
  local_38.tv_sec = (ulong)local_38.tv_nsec / 1000000000;
  local_38.tv_nsec = (ulong)local_38.tv_nsec % 1000000000;
                    /* try { // try from 00e8a2a0 to 00e8a2a7 has its CatchHandler @ 00e8a2fc */
  iVar2 = pthread_cond_timedwait((pthread_cond_t *)this,*(pthread_mutex_t **)param_1,&local_38);
  if ((iVar2 != 0) && (iVar2 != 0x6e)) {
                    /* try { // try from 00e8a2e8 to 00e8a2f3 has its CatchHandler @ 00e8a2fc */
                    /* WARNING: Subroutine does not return */
    __throw_system_error(iVar2,"condition_variable timed_wait failed");
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __throw_bad_alloc
// Address: 00e8a3d0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__throw_bad_alloc() */

void std::__throw_bad_alloc(void)

{
  bad_alloc *this;
  
  this = (bad_alloc *)__cxa_allocate_exception(8);
  bad_alloc::bad_alloc(this);
                    /* WARNING: Subroutine does not return */
  __cxa_throw(this,PTR_PTR_01ff58f8,PTR__bad_alloc_01ff5900);
}



// ==========================================================================================
// Function: __throw_length_error
// Address: 00e8a9e0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__basic_string_common<true>::__throw_length_error() const */

void std::__ndk1::__basic_string_common<true>::__throw_length_error(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00d9e940("basic_string");
}



// ==========================================================================================
// Function: __throw_out_of_range
// Address: 00e8a9f8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__basic_string_common<true>::__throw_out_of_range() const */

void std::__ndk1::__basic_string_common<true>::__throw_out_of_range(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e8aa10("basic_string");
}



// ==========================================================================================
// Function: __grow_by_and_replace
// Address: 00e8ac48
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__grow_by_and_replace(unsigned long, unsigned long, unsigned long, unsigned long, unsigned
   long, unsigned long, char const*) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__grow_by_and_replace
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6,
          char *param_7)

{
  long lVar1;
  ulong uVar2;
  size_t __n;
  void *__dest;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__src;
  ulong uVar3;
  
  if (-param_1 - 0x12 < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (((byte)*this & 1) == 0) {
    __src = this + 1;
  }
  else {
    __src = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
             (this + 0x10);
  }
  if (param_1 < 0x7fffffffffffffe7) {
    uVar2 = param_1 << 1;
    if (param_1 << 1 <= param_2 + param_1) {
      uVar2 = param_2 + param_1;
    }
    uVar3 = 0x17;
    if (0x16 < uVar2) {
      uVar3 = uVar2 + 0x10 & 0xfffffffffffffff0;
    }
  }
  else {
    uVar3 = 0xffffffffffffffef;
  }
  __dest = operator_new(uVar3);
  if (param_4 != 0) {
    memcpy(__dest,__src,param_4);
  }
  if (param_6 != 0) {
    memcpy((void *)((long)__dest + param_4),param_7,param_6);
  }
  __n = (param_3 - param_5) - param_4;
  if (__n != 0) {
    memcpy((void *)((long)__dest + param_6 + param_4),__src + param_5 + param_4,__n);
  }
  if (param_1 != 0x16) {
    operator_delete(__src);
  }
  lVar1 = (param_3 - param_5) + param_6;
  *(ulong *)this = uVar3 | 1;
  *(long *)(this + 8) = lVar1;
  *(void **)(this + 0x10) = __dest;
  *(undefined *)((long)__dest + lVar1) = 0;
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8ae48
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__init(char const*, unsigned long, unsigned long) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::__init
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          char *param_1,ulong param_2,ulong param_3)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__dest;
  ulong uVar1;
  
  if (param_3 < 0xfffffffffffffff0) {
    if (param_3 < 0x17) {
      __dest = this + 1;
      *this = SUB41((int)param_2 << 1,0);
    }
    else {
      uVar1 = param_3 + 0x10 & 0xfffffffffffffff0;
      __dest = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
               operator_new(uVar1);
      *(ulong *)(this + 8) = param_2;
      *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
       (this + 0x10) = __dest;
      *(ulong *)this = uVar1 | 1;
    }
    if (param_2 != 0) {
      memcpy(__dest,param_1,param_2);
    }
    __dest[param_2] =
         (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)0x0;
    return;
  }
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: __grow_by
// Address: 00e8b2bc
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__grow_by(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned
   long) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__grow_by(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
         ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6)

{
  ulong uVar1;
  size_t __n;
  void *__dest;
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__src;
  ulong uVar2;
  
  if (-param_1 - 0x11 < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (((byte)*this & 1) == 0) {
    __src = this + 1;
  }
  else {
    __src = *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
             (this + 0x10);
  }
  if (param_1 < 0x7fffffffffffffe7) {
    uVar1 = param_1 << 1;
    if (param_1 << 1 <= param_2 + param_1) {
      uVar1 = param_2 + param_1;
    }
    uVar2 = 0x17;
    if (0x16 < uVar1) {
      uVar2 = uVar1 + 0x10 & 0xfffffffffffffff0;
    }
  }
  else {
    uVar2 = 0xffffffffffffffef;
  }
  __dest = operator_new(uVar2);
  if (param_4 != 0) {
    memcpy(__dest,__src,param_4);
  }
  __n = (param_3 - param_5) - param_4;
  if (__n != 0) {
    memcpy((void *)((long)__dest + param_6 + param_4),__src + param_5 + param_4,__n);
  }
  if (param_1 != 0x16) {
    operator_delete(__src);
  }
  *(void **)(this + 0x10) = __dest;
  *(ulong *)this = uVar2 | 1;
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8b40c
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__init(char const*, unsigned long) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::__init
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          char *param_1,ulong param_2)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__dest;
  ulong uVar1;
  
  if (0xffffffffffffffef < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (param_2 < 0x17) {
    __dest = this + 1;
    *this = SUB41((int)param_2 << 1,0);
    if (param_2 == 0) goto LAB_00e8b47c;
  }
  else {
    uVar1 = param_2 + 0x10 & 0xfffffffffffffff0;
    __dest = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             operator_new(uVar1);
    *(ulong *)(this + 8) = param_2;
    *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
     (this + 0x10) = __dest;
    *(ulong *)this = uVar1 | 1;
  }
  memcpy(__dest,param_1,param_2);
LAB_00e8b47c:
  __dest[param_2] =
       (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)0x0;
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8bd94
// ==========================================================================================

/* std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>, std::__ndk1::allocator<char>
   >::__init(unsigned long, char) */

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::__init
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          ulong param_1,char param_2)

{
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *__s;
  ulong uVar1;
  
  if (0xffffffffffffffef < param_1) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (param_1 < 0x17) {
    __s = this + 1;
    *this = SUB41((int)param_1 << 1,0);
    if (param_1 == 0) goto LAB_00e8be04;
  }
  else {
    uVar1 = param_1 + 0x10 & 0xfffffffffffffff0;
    __s = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
          operator_new(uVar1);
    *(ulong *)(this + 8) = param_1;
    *(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> **)
     (this + 0x10) = __s;
    *(ulong *)this = uVar1 | 1;
  }
  memset(__s,(uint)(byte)param_2,param_1);
LAB_00e8be04:
  __s[param_1] = (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>)0x0
  ;
  return;
}



// ==========================================================================================
// Function: __grow_by_and_replace
// Address: 00e8ce68
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::__grow_by_and_replace(unsigned long, unsigned long, unsigned
   long, unsigned long, unsigned long, unsigned long, wchar_t const*) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__grow_by_and_replace
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6
          ,wchar_t *param_7)

{
  long lVar1;
  ulong uVar2;
  size_t __n;
  wchar_t *__s1;
  wchar_t *__s2;
  ulong uVar3;
  
  if (0x3fffffffffffffee - param_1 < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (((byte)*this & 1) == 0) {
    __s2 = (wchar_t *)(this + 4);
  }
  else {
    __s2 = *(wchar_t **)(this + 0x10);
  }
  if (param_1 < 0x1fffffffffffffe7) {
    uVar2 = param_1 << 1;
    if (param_1 << 1 <= param_2 + param_1) {
      uVar2 = param_2 + param_1;
    }
    uVar3 = 5;
    if (4 < uVar2) {
      uVar3 = uVar2 + 4 & 0xfffffffffffffffc;
    }
    if (uVar3 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00d9e940("allocator<T>::allocate(size_t n) \'n\' exceeds maximum supported size");
    }
  }
  else {
    uVar3 = 0x3fffffffffffffef;
  }
  __s1 = (wchar_t *)operator_new(uVar3 << 2);
  if (param_4 != 0) {
                    /* try { // try from 00e8cf28 to 00e8cf37 has its CatchHandler @ 00e8cfc4 */
    wmemcpy(__s1,__s2,param_4);
  }
  if (param_6 != 0) {
                    /* try { // try from 00e8cf40 to 00e8cf4b has its CatchHandler @ 00e8cfc0 */
    wmemcpy(__s1 + param_4,param_7,param_6);
  }
  __n = (param_3 - param_5) - param_4;
  if (__n != 0) {
                    /* try { // try from 00e8cf6c to 00e8cf6f has its CatchHandler @ 00e8cfbc */
    wmemcpy(__s1 + param_4 + param_6,__s2 + param_4 + param_5,__n);
  }
  if (param_1 != 4) {
    operator_delete(__s2);
  }
  lVar1 = (param_3 - param_5) + param_6;
  *(ulong *)this = uVar3 | 1;
  *(long *)(this + 8) = lVar1;
  *(wchar_t **)(this + 0x10) = __s1;
  __s1[lVar1] = L'\0';
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8d098
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::__init(wchar_t const*, unsigned long, unsigned long) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__init(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
         *this,wchar_t *param_1,ulong param_2,ulong param_3)

{
  wchar_t *__s1;
  ulong uVar1;
  
  if (param_3 < 0x3ffffffffffffff0) {
    if (param_3 < 5) {
      __s1 = (wchar_t *)(this + 4);
      *this = SUB41((int)param_2 << 1,0);
    }
    else {
      uVar1 = param_3 + 4 & 0xfffffffffffffffc;
      __s1 = (wchar_t *)operator_new(uVar1 << 2);
      *(ulong *)(this + 8) = param_2;
      *(wchar_t **)(this + 0x10) = __s1;
      *(ulong *)this = uVar1 | 1;
    }
    if (param_2 != 0) {
                    /* try { // try from 00e8d100 to 00e8d10f has its CatchHandler @ 00e8d130 */
      wmemcpy(__s1,param_1,param_2);
    }
    __s1[param_2] = L'\0';
    return;
  }
                    /* WARNING: Subroutine does not return */
  __basic_string_common<true>::__throw_length_error();
}



// ==========================================================================================
// Function: __grow_by
// Address: 00e8d548
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::__grow_by(unsigned long, unsigned long, unsigned long,
   unsigned long, unsigned long, unsigned long) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__grow_by(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            *this,ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,
           ulong param_6)

{
  ulong uVar1;
  size_t __n;
  wchar_t *__s1;
  wchar_t *__s2;
  ulong uVar2;
  
  uVar2 = 0x3fffffffffffffef;
  if (0x3fffffffffffffef - param_1 < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (((byte)*this & 1) == 0) {
    __s2 = (wchar_t *)(this + 4);
  }
  else {
    __s2 = *(wchar_t **)(this + 0x10);
  }
  if (param_1 < 0x1fffffffffffffe7) {
    uVar1 = param_1 << 1;
    if (param_1 << 1 <= param_2 + param_1) {
      uVar1 = param_2 + param_1;
    }
    uVar2 = 5;
    if (4 < uVar1) {
      uVar2 = uVar1 + 4 & 0xfffffffffffffffc;
    }
    if (uVar2 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00d9e940("allocator<T>::allocate(size_t n) \'n\' exceeds maximum supported size");
    }
  }
  __s1 = (wchar_t *)operator_new(uVar2 << 2);
  if (param_4 != 0) {
                    /* try { // try from 00e8d5f4 to 00e8d603 has its CatchHandler @ 00e8d67c */
    wmemcpy(__s1,__s2,param_4);
  }
  __n = (param_3 - param_5) - param_4;
  if (__n != 0) {
                    /* try { // try from 00e8d624 to 00e8d627 has its CatchHandler @ 00e8d678 */
    wmemcpy(__s1 + param_4 + param_6,__s2 + param_4 + param_5,__n);
  }
  if (param_1 != 4) {
    operator_delete(__s2);
  }
  *(wchar_t **)(this + 0x10) = __s1;
  *(ulong *)this = uVar2 | 1;
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8d6b4
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::__init(wchar_t const*, unsigned long) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__init(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
         *this,wchar_t *param_1,ulong param_2)

{
  wchar_t *__s1;
  ulong uVar1;
  
  if (0x3fffffffffffffef < param_2) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (param_2 < 5) {
    __s1 = (wchar_t *)(this + 4);
    *this = SUB41((int)param_2 << 1,0);
    if (param_2 == 0) goto LAB_00e8d728;
  }
  else {
    uVar1 = param_2 + 4 & 0xfffffffffffffffc;
    __s1 = (wchar_t *)operator_new(uVar1 << 2);
    *(ulong *)(this + 8) = param_2;
    *(wchar_t **)(this + 0x10) = __s1;
    *(ulong *)this = uVar1 | 1;
  }
                    /* try { // try from 00e8d718 to 00e8d727 has its CatchHandler @ 00e8d748 */
  wmemcpy(__s1,param_1,param_2);
LAB_00e8d728:
  __s1[param_2] = L'\0';
  return;
}



// ==========================================================================================
// Function: __init
// Address: 00e8dff4
// ==========================================================================================

/* std::__ndk1::basic_string<wchar_t, std::__ndk1::char_traits<wchar_t>,
   std::__ndk1::allocator<wchar_t> >::__init(unsigned long, wchar_t) */

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__init(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
         *this,ulong param_1,wchar_t param_2)

{
  wchar_t *__s;
  ulong uVar1;
  
  if (0x3fffffffffffffef < param_1) {
                    /* WARNING: Subroutine does not return */
    __basic_string_common<true>::__throw_length_error();
  }
  if (param_1 < 5) {
    __s = (wchar_t *)(this + 4);
    *this = SUB41((int)param_1 << 1,0);
    if (param_1 == 0) goto LAB_00e8e068;
  }
  else {
    uVar1 = param_1 + 4 & 0xfffffffffffffffc;
    __s = (wchar_t *)operator_new(uVar1 << 2);
    *(ulong *)(this + 8) = param_1;
    *(wchar_t **)(this + 0x10) = __s;
    *(ulong *)this = uVar1 | 1;
  }
                    /* try { // try from 00e8e058 to 00e8e067 has its CatchHandler @ 00e8e088 */
  wmemset(__s,param_2,param_1);
LAB_00e8e068:
  __s[param_1] = L'\0';
  return;
}



// ==========================================================================================
// Function: __u32toa
// Address: 00e927a8
// ==========================================================================================

/* std::__ndk1::__itoa::__u32toa(unsigned int, char*) */

undefined2 * std::__ndk1::__itoa::__u32toa(uint param_1,char *param_2)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  uint uVar4;
  undefined2 *puVar5;
  long lVar6;
  
  if (99999999 < param_1) {
    uVar4 = param_1 % 100000000;
    if (param_1 < 1000000000) {
      *param_2 = (char)(param_1 / 100000000) + '0';
      lVar6 = 1;
    }
    else {
      *(undefined2 *)param_2 = *(undefined2 *)(&DAT_00839ed8 + (ulong)(param_1 / 100000000) * 2);
      lVar6 = 2;
    }
    uVar1 = *(undefined2 *)
             (&DAT_00839ed8 +
             ((ulong)(uVar4 / 10000 + (int)(((ulong)uVar4 / 10000) / 100) * -100) & 0xffff) * 2);
    uVar2 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)(uVar4 % 10000) / 100) * 2);
    uVar3 = *(undefined2 *)(&DAT_00839ed8 + (ulong)((uVar4 % 10000) % 100) * 2);
    puVar5 = (undefined2 *)(param_2 + lVar6);
    *puVar5 = *(undefined2 *)(&DAT_00839ed8 + (((ulong)uVar4 / 10000) / 100) * 2);
    puVar5[1] = uVar1;
    puVar5[2] = uVar2;
    puVar5[3] = uVar3;
    return puVar5 + 4;
  }
  puVar5 = (undefined2 *)FUN_00e92880(param_2,param_1);
  return puVar5;
}



// ==========================================================================================
// Function: __u64toa
// Address: 00e92a40
// ==========================================================================================

/* std::__ndk1::__itoa::__u64toa(unsigned long, char*) */

undefined2 * std::__ndk1::__itoa::__u64toa(ulong param_1,char *param_2)

{
  undefined2 *puVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  undefined2 uVar7;
  undefined2 uVar8;
  uint uVar9;
  uint uVar10;
  undefined2 *puVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  long lVar15;
  ulong uVar16;
  
  if (99999999 < param_1) {
    if (param_1 < 10000000000000000) {
      uVar16 = param_1 % 100000000;
      puVar11 = (undefined2 *)FUN_00e92880(param_2,param_1 / 100000000 & 0xffffffff);
      uVar12 = (uint)(uVar16 / 10000);
      uVar9 = (int)uVar16 + uVar12 * -10000;
      uVar14 = uVar9 & 0xffff;
      uVar2 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)uVar14 / 100) * 2);
      uVar3 = *(undefined2 *)
               (&DAT_00839ed8 +
               ((ulong)((int)(uVar16 / 10000) + (uVar12 / 100) * -100) & 0xffff) * 2);
      uVar4 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)(uVar9 + (uVar14 / 100) * -100) & 0xffff) * 2)
      ;
      *puVar11 = *(undefined2 *)(&DAT_00839ed8 + ((uVar16 / 10000) / 100) * 2);
      puVar11[2] = uVar2;
      puVar11[1] = uVar3;
      puVar11[3] = uVar4;
      puVar11 = puVar11 + 4;
    }
    else {
      uVar16 = param_1 / 10000000000000000;
      uVar14 = (uint)uVar16;
      if (uVar14 < 100) {
        if (uVar14 < 10) {
          *param_2 = (char)uVar16 + '0';
          lVar15 = 1;
        }
        else {
          *(undefined2 *)param_2 = *(undefined2 *)(&DAT_00839ed8 + uVar16 * 2);
          lVar15 = 2;
        }
      }
      else if (uVar14 < 1000) {
        uVar2 = *(undefined2 *)(&DAT_00839ed8 + (ulong)(uVar14 % 100) * 2);
        *param_2 = (char)(uVar14 / 100) + '0';
        *(undefined2 *)(param_2 + 1) = uVar2;
        lVar15 = 3;
      }
      else {
        uVar2 = *(undefined2 *)(&DAT_00839ed8 + (ulong)(uVar14 / 100) * 2);
        *(undefined2 *)(param_2 + 2) = *(undefined2 *)(&DAT_00839ed8 + (ulong)(uVar14 % 100) * 2);
        lVar15 = 4;
        *(undefined2 *)param_2 = uVar2;
      }
      uVar16 = (param_1 % 10000000000000000) / 100000000;
      uVar12 = (int)(param_1 % 10000000000000000) + (int)uVar16 * -100000000;
      uVar13 = (uint)(uVar16 / 10000);
      uVar10 = (int)uVar16 + uVar13 * -10000;
      uVar14 = uVar12 / 10000 & 0xffff;
      uVar9 = uVar10 & 0xffff;
      uVar2 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)uVar14 / 100) * 2);
      uVar3 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)uVar9 / 100) * 2);
      uVar4 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)(uVar12 % 10000) / 100) * 2);
      uVar5 = *(undefined2 *)
               (&DAT_00839ed8 +
               ((ulong)((int)(uVar16 / 10000) + (uVar13 / 100) * -100) & 0xffff) * 2);
      uVar6 = *(undefined2 *)
               (&DAT_00839ed8 + ((ulong)(uVar12 / 10000 + (uVar14 / 100) * -100) & 0xffff) * 2);
      uVar7 = *(undefined2 *)(&DAT_00839ed8 + ((ulong)(uVar10 + (uVar9 / 100) * -100) & 0xffff) * 2)
      ;
      uVar8 = *(undefined2 *)(&DAT_00839ed8 + (ulong)((uVar12 % 10000) % 100) * 2);
      puVar1 = (undefined2 *)(param_2 + lVar15);
      puVar11 = puVar1 + 8;
      *puVar1 = *(undefined2 *)(&DAT_00839ed8 + ((uVar16 / 10000) / 100) * 2);
      puVar1[4] = uVar2;
      puVar1[2] = uVar3;
      puVar1[6] = uVar4;
      puVar1[1] = uVar5;
      puVar1[5] = uVar6;
      puVar1[3] = uVar7;
      puVar1[7] = uVar8;
    }
    return puVar11;
  }
  puVar11 = (undefined2 *)FUN_00e92880(param_2,param_1 & 0xffffffff);
  return puVar11;
}



// ==========================================================================================
// Function: __init
// Address: 00e93150
// ==========================================================================================

/* std::__ndk1::system_error::__init(std::__ndk1::error_code const&, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >) */

void __thiscall
std::__ndk1::system_error::__init(undefined8 *param_1_00,system_error *this,undefined8 *param_1)

{
  ulong uVar1;
  long lVar2;
  char *pcVar3;
  int iVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  byte local_50 [8];
  ulong local_48;
  char *local_40;
  long local_38;
  
  lVar2 = tpidr_el0;
  local_38 = *(long *)(lVar2 + 0x28);
  iVar4 = *(int *)this;
  if (iVar4 == 0) goto LAB_00e93204;
  if ((*(byte *)param_1 & 1) == 0) {
    if (*(byte *)param_1 >> 1 != 0) {
LAB_00e931a4:
      basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::append
                ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
                 param_1,": ");
      iVar4 = *(int *)this;
    }
  }
  else if (param_1[1] != 0) goto LAB_00e931a4;
  (**(code **)(**(long **)(this + 8) + 0x30))(local_50,*(long **)(this + 8),iVar4);
  uVar1 = (ulong)(local_50[0] >> 1);
  pcVar3 = (char *)((ulong)local_50 | 1);
  if ((local_50[0] & 1) != 0) {
    uVar1 = local_48;
    pcVar3 = local_40;
  }
                    /* try { // try from 00e931ec to 00e931f3 has its CatchHandler @ 00e93248 */
  basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::append
            ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             param_1,pcVar3,uVar1);
  if ((local_50[0] & 1) != 0) {
    operator_delete(local_40);
  }
LAB_00e93204:
  uVar6 = param_1[1];
  uVar5 = *param_1;
  param_1_00[2] = param_1[2];
  param_1_00[1] = uVar6;
  *param_1_00 = uVar5;
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
  if (*(long *)(lVar2 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: __throw_system_error
// Address: 00e9399c
// ==========================================================================================

/* std::__ndk1::__throw_system_error(int, char const*) */

void std::__ndk1::__throw_system_error(int param_1,char *param_2)

{
  int iVar1;
  system_error *psVar2;
  
  psVar2 = (system_error *)__cxa_allocate_exception(0x20);
  if (((DAT_0231e010 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231e010), iVar1 != 0)) {
    DAT_0231e008 = &PTR__error_category_01fbb9d8;
    __cxa_guard_release(&DAT_0231e010);
  }
                    /* try { // try from 00e939e0 to 00e939eb has its CatchHandler @ 00e93a34 */
  system_error::system_error(psVar2,param_1,&DAT_0231e008,param_2);
                    /* WARNING: Subroutine does not return */
  __cxa_throw(psVar2,PTR_PTR_01ff5958,PTR__system_error_01ff5960);
}



// ==========================================================================================
// Function: __thread_local_data
// Address: 00e93c8c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__thread_local_data() */

undefined * std::__ndk1::__thread_local_data(void)

{
  int iVar1;
  
  if (((DAT_0231e020 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_0231e020), iVar1 != 0)) {
                    /* try { // try from 00e93cd4 to 00e93d07 has its CatchHandler @ 00e93d08 */
    iVar1 = pthread_key_create((pthread_key_t *)&DAT_0231e018,FUN_00e940b4);
    if (iVar1 != 0) {
                    /* WARNING: Subroutine does not return */
      __throw_system_error(iVar1,"__thread_specific_ptr construction failed");
    }
    __cxa_guard_release(&DAT_0231e020);
  }
  return &DAT_0231e018;
}



// ==========================================================================================
// Function: __thread_struct
// Address: 00e9401c
// ==========================================================================================

/* std::__ndk1::__thread_struct::__thread_struct() */

void __thiscall std::__ndk1::__thread_struct::__thread_struct(__thread_struct *this)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)operator_new(0x30);
  puVar1[1] = 0;
  *puVar1 = 0;
  puVar1[3] = 0;
  puVar1[2] = 0;
  puVar1[5] = 0;
  puVar1[4] = 0;
  *(undefined8 **)this = puVar1;
  return;
}



// ==========================================================================================
// Function: ~__thread_struct
// Address: 00e94058
// ==========================================================================================

/* std::__ndk1::__thread_struct::~__thread_struct() */

void __thiscall std::__ndk1::__thread_struct::~__thread_struct(__thread_struct *this)

{
  void *pvVar1;
  
  pvVar1 = *(void **)this;
  if (pvVar1 != (void *)0x0) {
    FUN_00e93d20(pvVar1);
    operator_delete(pvVar1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: __make_ready_at_thread_exit
// Address: 00e940a8
// ==========================================================================================

/* std::__ndk1::__thread_struct::__make_ready_at_thread_exit(std::__ndk1::__assoc_sub_state*) */

void std::__ndk1::__thread_struct::__make_ready_at_thread_exit(__assoc_sub_state *param_1)

{
  FUN_00e93f30(*(undefined8 *)param_1);
  return;
}



// ==========================================================================================
// Function: __on_zero_shared
// Address: 00e9440c
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__assoc_sub_state::__on_zero_shared() */

void std::__ndk1::__assoc_sub_state::__on_zero_shared(void)

{
  long *in_x0;
  
                    /* WARNING: Could not recover jumptable at 0x00e94418. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*in_x0 + 8))();
  return;
}



// ==========================================================================================
// Function: __make_ready
// Address: 00e947f4
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__assoc_sub_state::__make_ready() */

void std::__ndk1::__assoc_sub_state::__make_ready(void)

{
  long in_x0;
  
  mutex::lock();
  *(uint *)(in_x0 + 0x70) = *(uint *)(in_x0 + 0x70) | 4;
  condition_variable::notify_all();
  mutex::unlock();
  return;
}



// ==========================================================================================
// Function: __sub_wait
// Address: 00e94958
// ==========================================================================================

/* std::__ndk1::__assoc_sub_state::__sub_wait(std::__ndk1::unique_lock<std::__ndk1::mutex>&) */

void __thiscall
std::__ndk1::__assoc_sub_state::__sub_wait(__assoc_sub_state *this,unique_lock *param_1)

{
  uint uVar1;
  
  uVar1 = *(uint *)(this + 0x70);
  if ((uVar1 >> 2 & 1) == 0) {
    if ((uVar1 >> 3 & 1) != 0) {
      *(uint *)(this + 0x70) = uVar1 & 0xfffffff7;
      if (param_1[8] != (unique_lock)0x0) {
        mutex::unlock();
        param_1[8] = (unique_lock)0x0;
                    /* WARNING: Could not recover jumptable at 0x00e949e4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        (**(code **)(*(long *)this + 0x18))(this);
        return;
      }
                    /* WARNING: Subroutine does not return */
      __throw_system_error(1,"unique_lock::unlock: not locked");
    }
    do {
      condition_variable::wait((condition_variable *)(this + 0x40),param_1);
    } while (((byte)this[0x70] >> 2 & 1) == 0);
  }
  return;
}



// ==========================================================================================
// Function: __execute
// Address: 00e94adc
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__assoc_sub_state::__execute() */

void std::__ndk1::__assoc_sub_state::__execute(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e944d4(3);
}



// ==========================================================================================
// Function: ~__assoc_sub_state
// Address: 00e950b8
// ==========================================================================================

/* std::__ndk1::__assoc_sub_state::~__assoc_sub_state() */

void __thiscall std::__ndk1::__assoc_sub_state::~__assoc_sub_state(__assoc_sub_state *this)

{
  *(undefined **)this = PTR_vtable_01ff5980 + 0x10;
  condition_variable::~condition_variable((condition_variable *)(this + 0x40));
  mutex::~mutex((mutex *)(this + 0x18));
  exception_ptr::~exception_ptr((exception_ptr *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  return;
}



// ==========================================================================================
// Function: ~__assoc_sub_state
// Address: 00e9510c
// ==========================================================================================

/* std::__ndk1::__assoc_sub_state::~__assoc_sub_state() */

void __thiscall std::__ndk1::__assoc_sub_state::~__assoc_sub_state(__assoc_sub_state *this)

{
  *(undefined **)this = PTR_vtable_01ff5980 + 0x10;
  condition_variable::~condition_variable((condition_variable *)(this + 0x40));
  mutex::~mutex((mutex *)(this + 0x18));
  exception_ptr::~exception_ptr((exception_ptr *)(this + 0x10));
  __shared_weak_count::~__shared_weak_count((__shared_weak_count *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: __throw_length_error
// Address: 00e95194
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__vector_base_common<true>::__throw_length_error() const */

void std::__ndk1::__vector_base_common<true>::__throw_length_error(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00d9e940("vector");
}



// ==========================================================================================
// Function: __throw_out_of_range
// Address: 00e951ac
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* std::__ndk1::__vector_base_common<true>::__throw_out_of_range() const */

void std::__ndk1::__vector_base_common<true>::__throw_out_of_range(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e8aa10("vector");
}



// ==========================================================================================
// Function: __cxa_allocate_exception
// Address: 00e951f4
// ==========================================================================================

long __cxa_allocate_exception(long param_1)

{
  void *__s;
  ulong __n;
  
  __n = param_1 + 0x8fU & 0xfffffffffffffff0;
                    /* try { // try from 00e9520c to 00e95213 has its CatchHandler @ 00e95244 */
  __s = (void *)FUN_00eaaedc(__n);
  if (__s != (void *)0x0) {
    memset(__s,0,__n);
    return (long)__s + 0x80;
  }
                    /* WARNING: Subroutine does not return */
  std::terminate();
}



// ==========================================================================================
// Function: __cxa_free_exception
// Address: 00e95248
// ==========================================================================================

void __cxa_free_exception(long param_1)

{
                    /* try { // try from 00e95258 to 00e9525b has its CatchHandler @ 00e95268 */
  FUN_00eab044(param_1 + -0x80);
  return;
}



// ==========================================================================================
// Function: __cxa_allocate_dependent_exception
// Address: 00e9526c
// ==========================================================================================

void __cxa_allocate_dependent_exception(void)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_00eaaedc(0x80);
  if (puVar1 != (undefined8 *)0x0) {
    puVar1[0xd] = 0;
    puVar1[0xc] = 0;
    puVar1[0xf] = 0;
    puVar1[0xe] = 0;
    puVar1[9] = 0;
    puVar1[8] = 0;
    puVar1[0xb] = 0;
    puVar1[10] = 0;
    puVar1[5] = 0;
    puVar1[4] = 0;
    puVar1[7] = 0;
    puVar1[6] = 0;
    puVar1[1] = 0;
    *puVar1 = 0;
    puVar1[3] = 0;
    puVar1[2] = 0;
    return;
  }
                    /* WARNING: Subroutine does not return */
  std::terminate();
}



// ==========================================================================================
// Function: __cxa_free_dependent_exception
// Address: 00e952a8
// ==========================================================================================

void __cxa_free_dependent_exception(void)

{
  FUN_00eab044();
  return;
}



// ==========================================================================================
// Function: __cxa_throw
// Address: 00e952b0
// ==========================================================================================

void __cxa_throw(long param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  
  lVar1 = __cxa_get_globals();
  uVar2 = std::get_unexpected();
  *(undefined8 *)(param_1 + -0x60) = uVar2;
  uVar2 = std::get_terminate();
  *(undefined8 *)(param_1 + -0x70) = param_2;
  *(undefined8 *)(param_1 + -0x68) = param_3;
  *(undefined8 *)(param_1 + -0x58) = uVar2;
  FUN_00e95330(param_1 + -0x20);
  *(undefined8 *)(param_1 + -0x78) = 1;
  *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  *(code **)(param_1 + -0x18) = FUN_00e9534c;
  FUN_00ead1ec(param_1 + -0x20);
  puVar3 = (undefined8 *)FUN_00e953b8(param_1 + -0x80);
  *puVar3 = 0x434c4e47432b2b00;
  return;
}



// ==========================================================================================
// Function: __cxa_get_exception_ptr
// Address: 00e953dc
// ==========================================================================================

undefined8 __cxa_get_exception_ptr(long param_1)

{
  return *(undefined8 *)(param_1 + -8);
}



// ==========================================================================================
// Function: __cxa_begin_catch
// Address: 00e953e8
// ==========================================================================================

ulong * __cxa_begin_catch(ulong *param_1)

{
  int iVar1;
  int iVar2;
  ulong **ppuVar3;
  ulong *puVar4;
  ulong uVar5;
  
  uVar5 = *param_1;
                    /* try { // try from 00e95400 to 00e95403 has its CatchHandler @ 00e95480 */
  ppuVar3 = (ulong **)__cxa_get_globals();
  puVar4 = param_1 + -0xc;
  if (uVar5 >> 8 == 0x434c4e47432b2b) {
    iVar2 = *(int *)(param_1 + -5);
    iVar1 = -iVar2;
    if (-1 < iVar2) {
      iVar1 = iVar2;
    }
    *(int *)(param_1 + -5) = iVar1 + 1;
    if (*ppuVar3 != puVar4) {
      param_1[-6] = (ulong)*ppuVar3;
      *ppuVar3 = puVar4;
    }
    *(int *)(ppuVar3 + 1) = *(int *)(ppuVar3 + 1) + -1;
    param_1 = (ulong *)param_1[-1];
  }
  else {
    if (*ppuVar3 != (ulong *)0x0) {
                    /* WARNING: Subroutine does not return */
      std::terminate();
    }
    *ppuVar3 = puVar4;
    param_1 = param_1 + 4;
  }
  return param_1;
}



// ==========================================================================================
// Function: __cxa_end_catch
// Address: 00e95484
// ==========================================================================================

void __cxa_end_catch(void)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  long *plVar4;
  long lVar5;
  long lVar6;
  
  plVar4 = (long *)__cxa_get_globals_fast();
  lVar5 = *plVar4;
  if (lVar5 != 0) {
    if (*(ulong *)(lVar5 + 0x60) >> 8 == 0x434c4e47432b2b) {
      iVar1 = *(int *)(lVar5 + 0x38);
      if (iVar1 < 0) {
        *(int *)(lVar5 + 0x38) = iVar1 + 1;
        if (iVar1 == -1) {
          *plVar4 = *(long *)(lVar5 + 0x30);
        }
      }
      else {
        *(int *)(lVar5 + 0x38) = iVar1 + -1;
        if (iVar1 + -1 == 0) {
          *plVar4 = *(long *)(lVar5 + 0x30);
          lVar6 = lVar5;
          if (*(char *)(lVar5 + 0x60) == '\x01') {
            lVar6 = *(long *)(lVar5 + 8) + -0x80;
            FUN_00eab044(lVar5);
          }
          plVar4 = (long *)(lVar6 + 8);
          do {
            lVar5 = *plVar4;
            cVar2 = '\x01';
            bVar3 = (bool)ExclusiveMonitorPass(plVar4,0x10);
            if (bVar3) {
              *plVar4 = lVar5 + -1;
              cVar2 = ExclusiveMonitorsStatus();
            }
          } while (cVar2 != '\0');
          if (lVar5 + -1 == 0) {
            if (*(code **)(lVar6 + 0x18) != (code *)0x0) {
                    /* try { // try from 00e95524 to 00e95527 has its CatchHandler @ 00e95564 */
              (**(code **)(lVar6 + 0x18))(lVar6 + 0x80);
            }
                    /* try { // try from 00e95528 to 00e9552f has its CatchHandler @ 00e95568 */
            FUN_00eab044(lVar6);
          }
        }
      }
    }
    else {
      FUN_00ead5bc();
      *plVar4 = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: __cxa_decrement_exception_refcount
// Address: 00e9556c
// ==========================================================================================

void __cxa_decrement_exception_refcount(long param_1)

{
  char cVar1;
  bool bVar2;
  long *plVar3;
  long lVar4;
  
  if (param_1 != 0) {
    plVar3 = (long *)(param_1 + -0x78);
    do {
      lVar4 = *plVar3;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(plVar3,0x10);
      if (bVar2) {
        *plVar3 = lVar4 + -1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (lVar4 + -1 == 0) {
      if (*(code **)(param_1 + -0x68) != (code *)0x0) {
                    /* try { // try from 00e955a4 to 00e955a7 has its CatchHandler @ 00e955c0 */
        (**(code **)(param_1 + -0x68))();
      }
                    /* try { // try from 00e955a8 to 00e955af has its CatchHandler @ 00e955c4 */
      FUN_00eab044(param_1 + -0x80);
    }
  }
  return;
}



// ==========================================================================================
// Function: __cxa_current_exception_type
// Address: 00e955c8
// ==========================================================================================

long * __cxa_current_exception_type(void)

{
  long *plVar1;
  long lVar2;
  
  plVar1 = (long *)__cxa_get_globals_fast();
  if (plVar1 != (long *)0x0) {
    lVar2 = *plVar1;
    if ((lVar2 == 0) || (*(ulong *)(lVar2 + 0x60) >> 8 != 0x434c4e47432b2b)) {
      plVar1 = (long *)0x0;
    }
    else {
      plVar1 = *(long **)(lVar2 + 0x10);
    }
  }
  return plVar1;
}



// ==========================================================================================
// Function: __cxa_rethrow
// Address: 00e95618
// ==========================================================================================

void __cxa_rethrow(void)

{
  int iVar1;
  int iVar2;
  long *plVar3;
  ulong uVar4;
  ulong *puVar5;
  long lVar6;
  ulong uVar7;
  
  plVar3 = (long *)__cxa_get_globals();
  lVar6 = *plVar3;
  if (lVar6 != 0) {
    puVar5 = (ulong *)(lVar6 + 0x60);
    uVar4 = *puVar5;
    if ((uVar4 & 0xffffffffffffff00) == 0x434c4e47432b2b00) {
      *(int *)(lVar6 + 0x38) = -*(int *)(lVar6 + 0x38);
      *(int *)(plVar3 + 1) = *(int *)(plVar3 + 1) + 1;
    }
    else {
      *plVar3 = 0;
    }
    FUN_00ead1ec(puVar5);
    uVar7 = *puVar5;
                    /* try { // try from 00e95690 to 00e95693 has its CatchHandler @ 00e95700 */
    plVar3 = (long *)__cxa_get_globals();
    if ((uVar7 & 0xffffffffffffff00) == 0x434c4e47432b2b00) {
      iVar2 = *(int *)(lVar6 + 0x38);
      iVar1 = -iVar2;
      if (-1 < iVar2) {
        iVar1 = iVar2;
      }
      *(int *)(lVar6 + 0x38) = iVar1 + 1;
      if (*plVar3 != lVar6) {
        *(long *)(lVar6 + 0x30) = *plVar3;
        *plVar3 = lVar6;
      }
      *(int *)(plVar3 + 1) = *(int *)(plVar3 + 1) + -1;
    }
    else {
      if (*plVar3 != 0) goto LAB_00e9563c;
      *plVar3 = lVar6;
    }
    if ((uVar4 & 0xffffffffffffff00) == 0x434c4e47432b2b00) {
      FUN_00e95e24(*(undefined8 *)(lVar6 + 0x28));
                    /* WARNING: Subroutine does not return */
                    /* catch() { ... } // from try @ 00e95690 with catch @ 00e95700 */
      __cxa_call_unexpected();
    }
  }
LAB_00e9563c:
                    /* WARNING: Subroutine does not return */
  std::terminate();
}



// ==========================================================================================
// Function: __cxa_increment_exception_refcount
// Address: 00e95704
// ==========================================================================================

void __cxa_increment_exception_refcount(long param_1)

{
  char cVar1;
  bool bVar2;
  long *plVar3;
  
  if (param_1 != 0) {
    plVar3 = (long *)(param_1 + -0x78);
    do {
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(plVar3,0x10);
      if (bVar2) {
        *plVar3 = *plVar3 + 1;
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
  }
  return;
}



// ==========================================================================================
// Function: __cxa_current_primary_exception
// Address: 00e95724
// ==========================================================================================

long * __cxa_current_primary_exception(void)

{
  long *plVar1;
  char cVar2;
  bool bVar3;
  long *plVar4;
  long lVar5;
  
                    /* try { // try from 00e95730 to 00e95733 has its CatchHandler @ 00e9579c */
  plVar4 = (long *)__cxa_get_globals_fast();
  if (plVar4 != (long *)0x0) {
    lVar5 = *plVar4;
    if ((lVar5 == 0) || (*(ulong *)(lVar5 + 0x60) >> 8 != 0x434c4e47432b2b)) {
      plVar4 = (long *)0x0;
    }
    else {
      if ((*(ulong *)(lVar5 + 0x60) & 0xff) == 1) {
        lVar5 = *(long *)(lVar5 + 8) + -0x80;
      }
      plVar4 = (long *)(lVar5 + 0x80);
      plVar1 = (long *)(lVar5 + 8);
      do {
        cVar2 = '\x01';
        bVar3 = (bool)ExclusiveMonitorPass(plVar1,0x10);
        if (bVar3) {
          *plVar1 = *plVar1 + 1;
          cVar2 = ExclusiveMonitorsStatus();
        }
      } while (cVar2 != '\0');
    }
  }
  return plVar4;
}



// ==========================================================================================
// Function: __cxa_rethrow_primary_exception
// Address: 00e957a0
// ==========================================================================================

void __cxa_rethrow_primary_exception(long param_1)

{
  int iVar1;
  int iVar2;
  char cVar3;
  bool bVar4;
  undefined8 *puVar5;
  undefined8 uVar6;
  long lVar7;
  long *plVar8;
  ulong *puVar9;
  ulong uVar10;
  
  if (param_1 != 0) {
    puVar5 = (undefined8 *)FUN_00eaaedc(0x80);
    if (puVar5 == (undefined8 *)0x0) {
LAB_00e958bc:
                    /* WARNING: Subroutine does not return */
      std::terminate();
    }
    plVar8 = (long *)(param_1 + -0x78);
    puVar5[0xd] = 0;
    puVar5[0xc] = 0;
    puVar5[0xf] = 0;
    puVar5[0xe] = 0;
    puVar5[9] = 0;
    puVar5[8] = 0;
    puVar5[0xb] = 0;
    puVar5[10] = 0;
    puVar5[5] = 0;
    puVar5[4] = 0;
    puVar5[7] = 0;
    puVar5[6] = 0;
    puVar5[1] = 0;
    *puVar5 = 0;
    puVar5[3] = 0;
    puVar5[2] = 0;
    puVar5[1] = param_1;
    do {
      cVar3 = '\x01';
      bVar4 = (bool)ExclusiveMonitorPass(plVar8,0x10);
      if (bVar4) {
        *plVar8 = *plVar8 + 1;
        cVar3 = ExclusiveMonitorsStatus();
      }
    } while (cVar3 != '\0');
    puVar5[2] = *(undefined8 *)(param_1 + -0x70);
    uVar6 = std::get_unexpected();
    puVar5[4] = uVar6;
    uVar6 = std::get_terminate();
    puVar9 = puVar5 + 0xc;
    *puVar9 = 0x434c4e47432b2b01;
    puVar5[5] = uVar6;
    lVar7 = __cxa_get_globals();
    *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
    puVar5[0xd] = FUN_00e958c4;
    FUN_00ead1ec(puVar9);
    uVar10 = *puVar9;
                    /* try { // try from 00e95854 to 00e95857 has its CatchHandler @ 00e958c0 */
    plVar8 = (long *)__cxa_get_globals();
    if ((uVar10 & 0xffffffffffffff00) == 0x434c4e47432b2b00) {
      iVar2 = *(int *)(puVar5 + 7);
      iVar1 = -iVar2;
      if (-1 < iVar2) {
        iVar1 = iVar2;
      }
      *(int *)(puVar5 + 7) = iVar1 + 1;
      if ((undefined8 *)*plVar8 != puVar5) {
        puVar5[6] = (undefined8 *)*plVar8;
        *plVar8 = (long)puVar5;
      }
      *(int *)(plVar8 + 1) = *(int *)(plVar8 + 1) + -1;
    }
    else {
      if (*plVar8 != 0) goto LAB_00e958bc;
      *plVar8 = (long)puVar5;
    }
  }
  return;
}



// ==========================================================================================
// Function: __cxa_uncaught_exception
// Address: 00e9593c
// ==========================================================================================

ulong __cxa_uncaught_exception(void)

{
  ulong uVar1;
  
                    /* try { // try from 00e95948 to 00e9594b has its CatchHandler @ 00e95968 */
  uVar1 = __cxa_get_globals_fast();
  if (uVar1 != 0) {
    uVar1 = (ulong)(*(int *)(uVar1 + 8) != 0);
  }
  return uVar1;
}



// ==========================================================================================
// Function: __cxa_uncaught_exceptions
// Address: 00e9596c
// ==========================================================================================

ulong __cxa_uncaught_exceptions(void)

{
  ulong uVar1;
  
                    /* try { // try from 00e95978 to 00e9597b has its CatchHandler @ 00e95990 */
  uVar1 = __cxa_get_globals_fast();
  if (uVar1 != 0) {
    uVar1 = (ulong)*(uint *)(uVar1 + 8);
  }
  return uVar1;
}



// ==========================================================================================
// Function: __cxa_get_globals
// Address: 00e95994
// ==========================================================================================

void __cxa_get_globals(void)

{
  __emutls_get_address(&DAT_020ff4f0);
  return;
}



// ==========================================================================================
// Function: __cxa_get_globals_fast
// Address: 00e959b8
// ==========================================================================================

void __cxa_get_globals_fast(void)

{
  __emutls_get_address(&DAT_020ff4f0);
  return;
}



// ==========================================================================================
// Function: __cxa_guard_acquire
// Address: 00e959dc
// ==========================================================================================

undefined4 __cxa_guard_acquire(char *param_1)

{
  byte bVar1;
  byte bVar2;
  int iVar3;
  long lVar4;
  undefined4 uVar5;
  int unaff_w20;
  
  if (*param_1 == '\0') {
    iVar3 = pthread_mutex_lock((pthread_mutex_t *)&DAT_0231e038);
    if (iVar3 != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00e95c8c("%s failed to acquire mutex","__cxa_guard_acquire");
    }
    bVar1 = param_1[1];
    if ((bVar1 >> 1 & 1) != 0) {
      iVar3 = *(int *)(param_1 + 4);
                    /* try { // try from 00e95a28 to 00e95a2f has its CatchHandler @ 00e95afc */
      lVar4 = syscall(0xb2);
      unaff_w20 = (int)lVar4;
      if (iVar3 == unaff_w20) {
                    /* try { // try from 00e95af0 to 00e95afb has its CatchHandler @ 00e95afc */
                    /* WARNING: Subroutine does not return */
        FUN_00e95c8c("__cxa_guard_acquire detected recursive initialization");
      }
    }
    while (bVar2 = param_1[1], (bVar2 >> 1 & 1) != 0) {
      param_1[1] = bVar2 | 4;
                    /* try { // try from 00e95a5c to 00e95a67 has its CatchHandler @ 00e95b04 */
      pthread_cond_wait((pthread_cond_t *)&DAT_0231e060,(pthread_mutex_t *)&DAT_0231e038);
    }
    if (bVar2 == 1) {
      uVar5 = 0;
    }
    else {
      if ((bVar1 >> 1 & 1) == 0) {
                    /* try { // try from 00e95a80 to 00e95a87 has its CatchHandler @ 00e95afc */
        lVar4 = syscall(0xb2);
        unaff_w20 = (int)lVar4;
      }
      *(int *)(param_1 + 4) = unaff_w20;
      param_1[1] = '\x02';
      uVar5 = 1;
    }
                    /* try { // try from 00e95a9c to 00e95aa7 has its CatchHandler @ 00e95b00 */
    iVar3 = pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231e038);
    if (iVar3 != 0) {
                    /* try { // try from 00e95adc to 00e95aef has its CatchHandler @ 00e95b00 */
                    /* WARNING: Subroutine does not return */
      FUN_00e95c8c("%s failed to release mutex","__cxa_guard_acquire");
    }
  }
  else {
    uVar5 = 0;
  }
  return uVar5;
}



// ==========================================================================================
// Function: __cxa_guard_release
// Address: 00e95b38
// ==========================================================================================

void __cxa_guard_release(undefined4 *param_1)

{
  byte bVar1;
  int iVar2;
  
  *param_1 = 1;
  iVar2 = pthread_mutex_lock((pthread_mutex_t *)&DAT_0231e038);
  if (iVar2 != 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e95c8c("%s failed to acquire mutex","__cxa_guard_release");
  }
  bVar1 = *(byte *)((long)param_1 + 1);
  *(undefined *)((long)param_1 + 1) = 1;
                    /* try { // try from 00e95b70 to 00e95b7b has its CatchHandler @ 00e95be4 */
  iVar2 = pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231e038);
  if (iVar2 == 0) {
    if (((bVar1 >> 2 & 1) != 0) &&
       (iVar2 = pthread_cond_broadcast((pthread_cond_t *)&DAT_0231e060), iVar2 != 0)) {
                    /* WARNING: Subroutine does not return */
      FUN_00e95c8c("%s failed to broadcast","__cxa_guard_release");
    }
    return;
  }
                    /* try { // try from 00e95bbc to 00e95bcf has its CatchHandler @ 00e95be4 */
                    /* WARNING: Subroutine does not return */
  FUN_00e95c8c("%s failed to release mutex","__cxa_guard_release");
}



// ==========================================================================================
// Function: __cxa_guard_abort
// Address: 00e95be8
// ==========================================================================================

void __cxa_guard_abort(long param_1)

{
  byte bVar1;
  int iVar2;
  
  iVar2 = pthread_mutex_lock((pthread_mutex_t *)&DAT_0231e038);
  if (iVar2 != 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00e95c8c("%s failed to acquire mutex","__cxa_guard_abort");
  }
  bVar1 = *(byte *)(param_1 + 1);
  *(undefined4 *)(param_1 + 4) = 0;
  *(undefined *)(param_1 + 1) = 0;
                    /* try { // try from 00e95c18 to 00e95c23 has its CatchHandler @ 00e95c88 */
  iVar2 = pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231e038);
  if (iVar2 == 0) {
    if (((bVar1 >> 2 & 1) != 0) &&
       (iVar2 = pthread_cond_broadcast((pthread_cond_t *)&DAT_0231e060), iVar2 != 0)) {
                    /* WARNING: Subroutine does not return */
      FUN_00e95c8c("%s failed to broadcast","__cxa_guard_abort");
    }
    return;
  }
                    /* try { // try from 00e95c60 to 00e95c73 has its CatchHandler @ 00e95c88 */
                    /* WARNING: Subroutine does not return */
  FUN_00e95c8c("%s failed to release mutex","__cxa_guard_abort");
}



// ==========================================================================================
// Function: __cxa_demangle
// Address: 00e96038
// ==========================================================================================

void * __cxa_demangle(byte *param_1,void *param_2,ulong *param_3,undefined4 *param_4)

{
  byte bVar1;
  long lVar2;
  size_t sVar3;
  long *plVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  undefined4 uVar7;
  long lVar8;
  long *plVar9;
  long lVar10;
  ulong uVar11;
  byte *pbVar12;
  byte *pbVar13;
  byte *pbVar14;
  byte *pbVar15;
  void *pvVar16;
  ulong uVar17;
  void *local_13e0;
  ulong local_13d8;
  size_t local_13d0;
  undefined8 local_13c8;
  byte *local_13c0;
  byte *local_13b8;
  undefined8 *local_13b0;
  undefined8 *local_13a8;
  undefined8 **ppuStack_13a0;
  undefined8 local_1398;
  undefined8 uStack_1390;
  undefined8 local_1388;
  undefined8 uStack_1380;
  undefined8 local_1378;
  undefined8 uStack_1370;
  undefined8 local_1368;
  undefined8 uStack_1360;
  undefined8 local_1358;
  undefined8 uStack_1350;
  undefined8 local_1348;
  undefined8 uStack_1340;
  undefined8 local_1338;
  undefined8 uStack_1330;
  undefined8 local_1328;
  undefined8 uStack_1320;
  undefined8 local_1318;
  undefined8 uStack_1310;
  undefined8 local_1308;
  undefined8 uStack_1300;
  undefined8 local_12f8;
  undefined8 uStack_12f0;
  undefined8 local_12e8;
  undefined8 uStack_12e0;
  undefined8 local_12d8;
  undefined8 uStack_12d0;
  undefined8 local_12c8;
  undefined8 uStack_12c0;
  undefined8 local_12b8;
  undefined8 uStack_12b0;
  undefined8 local_12a8;
  undefined8 uStack_12a0;
  undefined8 *local_1298;
  undefined8 *local_1290;
  undefined8 **ppuStack_1288;
  undefined8 local_1280;
  undefined8 uStack_1278;
  undefined8 uStack_1270;
  undefined8 uStack_1268;
  undefined8 local_1260;
  undefined8 uStack_1258;
  undefined8 uStack_1250;
  undefined8 uStack_1248;
  undefined8 local_1240;
  undefined8 uStack_1238;
  undefined8 uStack_1230;
  undefined8 uStack_1228;
  undefined8 local_1220;
  undefined8 uStack_1218;
  undefined8 uStack_1210;
  undefined8 uStack_1208;
  undefined8 local_1200;
  undefined8 uStack_11f8;
  undefined8 uStack_11f0;
  undefined8 uStack_11e8;
  undefined8 local_11e0;
  undefined8 uStack_11d8;
  undefined8 uStack_11d0;
  undefined8 uStack_11c8;
  undefined8 local_11c0;
  undefined8 uStack_11b8;
  undefined8 uStack_11b0;
  undefined8 uStack_11a8;
  undefined8 local_11a0;
  undefined8 uStack_1198;
  undefined8 uStack_1190;
  undefined8 uStack_1188;
  undefined8 *local_1180;
  undefined8 *local_1178;
  undefined8 **local_1170;
  undefined8 local_1168;
  undefined8 uStack_1160;
  undefined8 local_1158;
  undefined8 uStack_1150;
  undefined8 local_1148;
  undefined8 uStack_1140;
  undefined8 local_1138;
  undefined8 uStack_1130;
  undefined8 *local_1128;
  undefined8 *local_1120;
  undefined8 **local_1118;
  undefined8 local_1110;
  undefined8 uStack_1108;
  undefined8 uStack_1100;
  undefined8 uStack_10f8;
  undefined8 *local_10f0;
  undefined8 *local_10e8;
  undefined2 *local_10e0;
  undefined8 local_10d8;
  undefined8 uStack_10d0;
  undefined8 local_10c8;
  undefined8 uStack_10c0;
  undefined2 local_10b8 [4];
  undefined8 local_10b0;
  undefined8 local_10a8;
  undefined4 local_10a0;
  undefined8 local_1090;
  undefined8 uStack_1088;
  undefined8 *local_90;
  long local_78;
  
  lVar2 = tpidr_el0;
  local_78 = *(long *)(lVar2 + 0x28);
  if ((param_1 == (byte *)0x0) || ((param_2 != (void *)0x0 && (param_3 == (ulong *)0x0)))) {
    pvVar16 = (void *)0x0;
    if (param_4 != (undefined4 *)0x0) {
      *param_4 = 0xfffffffd;
    }
    goto LAB_00e96694;
  }
  sVar3 = strlen((char *)param_1);
  local_13b8 = param_1 + sVar3;
  ppuStack_13a0 = &local_1298;
  uStack_12b0 = 0;
  local_12b8 = 0;
  local_1170 = &local_1128;
  ppuStack_1288 = &local_1180;
  uStack_1350 = 0;
  local_1358 = 0;
  uStack_1340 = 0;
  local_1348 = 0;
  uStack_1330 = 0;
  local_1338 = 0;
  uStack_1320 = 0;
  local_1328 = 0;
  uStack_1310 = 0;
  local_1318 = 0;
  uStack_1300 = 0;
  local_1308 = 0;
  uStack_12f0 = 0;
  local_12f8 = 0;
  uStack_12e0 = 0;
  local_12e8 = 0;
  uStack_12d0 = 0;
  local_12d8 = 0;
  uStack_12c0 = 0;
  local_12c8 = 0;
  uStack_12a0 = 0;
  local_12a8 = 0;
  uStack_1390 = 0;
  local_1398 = 0;
  uStack_1380 = 0;
  local_1388 = 0;
  uStack_1370 = 0;
  local_1378 = 0;
  uStack_1360 = 0;
  local_1368 = 0;
  uStack_1278 = 0;
  local_1280 = 0;
  uStack_1268 = 0;
  uStack_1270 = 0;
  uStack_1258 = 0;
  local_1260 = 0;
  uStack_1248 = 0;
  uStack_1250 = 0;
  uStack_1238 = 0;
  local_1240 = 0;
  uStack_1228 = 0;
  uStack_1230 = 0;
  uStack_1218 = 0;
  local_1220 = 0;
  uStack_1208 = 0;
  uStack_1210 = 0;
  uStack_11f8 = 0;
  local_1200 = 0;
  uStack_11e8 = 0;
  uStack_11f0 = 0;
  uStack_11d8 = 0;
  local_11e0 = 0;
  uStack_11c8 = 0;
  uStack_11d0 = 0;
  uStack_11b8 = 0;
  local_11c0 = 0;
  uStack_11a8 = 0;
  uStack_11b0 = 0;
  uStack_1198 = 0;
  local_11a0 = 0;
  uStack_1188 = 0;
  uStack_1190 = 0;
  uStack_1150 = 0;
  local_1158 = 0;
  local_10e0 = local_10b8;
  uStack_1130 = 0;
  local_1138 = 0;
  uStack_1140 = 0;
  local_1148 = 0;
  local_1118 = &local_10f0;
  uStack_1160 = 0;
  local_1168 = 0;
  uStack_1108 = 0;
  local_1110 = 0;
  uStack_10f8 = 0;
  uStack_1100 = 0;
  uStack_10c0 = 0;
  local_10c8 = 0;
  uStack_10d0 = 0;
  local_10d8 = 0;
  local_10b8[0] = 1;
  uStack_1088 = 0;
  local_1090 = 0;
  local_13e0 = (void *)0x0;
  local_13d8 = 0;
  local_13d0 = 0;
  local_10b0 = 0xffffffffffffffff;
  local_10a0 = 0;
  local_10a8 = 0;
  local_13c8 = 0xffffffffffffffff;
  local_13b0 = &local_1398;
  local_13a8 = &local_1398;
  local_1298 = &local_1280;
  local_1290 = &local_1280;
  local_1180 = &local_1168;
  local_1178 = &local_1168;
  local_1128 = &local_1110;
  local_1120 = &local_1110;
  local_10f0 = &local_10d8;
  local_10e8 = &local_10d8;
  local_90 = &local_1090;
  if ((sVar3 < 2) || (*param_1 != 0x5f)) {
LAB_00e962d0:
    local_13c0 = param_1;
    plVar4 = (long *)FUN_00e97444(&local_13c0);
    pvVar16 = (void *)0x0;
    uVar7 = 0xfffffffe;
    if ((plVar4 != (long *)0x0) && (local_13b8 == local_13c0)) {
LAB_00e962f4:
      if (param_2 == (void *)0x0) {
LAB_00e96550:
        uVar17 = 0x400;
        param_2 = malloc(0x400);
        if (param_2 == (void *)0x0) {
          pvVar16 = (void *)0x0;
          uVar7 = 0xffffffff;
          goto LAB_00e965fc;
        }
      }
      else {
LAB_00e962f8:
        uVar17 = *param_3;
      }
      local_13d8 = 0;
      local_13e0 = param_2;
      local_13d0 = uVar17;
      (**(code **)(*plVar4 + 0x20))(plVar4,&local_13e0);
      if (*(char *)((long)plVar4 + 9) != '\x01') {
        (**(code **)(*plVar4 + 0x28))(plVar4,&local_13e0);
      }
      uVar17 = local_13d8 + 1;
      if (local_13d0 <= uVar17) {
        uVar11 = local_13d0 << 1;
        local_13d0 = uVar17;
        if (uVar17 <= uVar11) {
          local_13d0 = uVar11;
        }
        local_13e0 = realloc(local_13e0,local_13d0);
        if (local_13e0 == (void *)0x0) {
LAB_00e966e8:
                    /* WARNING: Subroutine does not return */
          std::terminate();
        }
        uVar17 = local_13d8 + 1;
      }
      *(undefined *)((long)local_13e0 + local_13d8) = 0;
      if (param_3 != (ulong *)0x0) {
        *param_3 = uVar17;
      }
      uVar7 = 0;
      pvVar16 = local_13e0;
      local_13d8 = uVar17;
    }
  }
  else if (param_1[1] == 0x5a) {
    lVar8 = 2;
LAB_00e96204:
    local_13c0 = param_1 + lVar8;
                    /* try { // try from 00e9620c to 00e9659f has its CatchHandler @ 00e966f0 */
    plVar4 = (long *)FUN_00e96790(&local_13c0);
    puVar6 = local_90;
    pbVar13 = local_13b8;
    pbVar12 = local_13c0;
    if (plVar4 != (long *)0x0) {
      if (local_13b8 == local_13c0) goto LAB_00e962f4;
      if (*local_13c0 != 0x2e) goto LAB_00e966d0;
      lVar8 = local_90[1];
      if (0xfef < lVar8 + 0x30U) {
        puVar5 = (undefined8 *)malloc(0x1000);
        if (puVar5 == (undefined8 *)0x0) goto LAB_00e966e8;
        lVar8 = 0;
        *puVar5 = puVar6;
        puVar5[1] = 0;
        local_90 = puVar5;
      }
      local_90[1] = lVar8 + 0x30;
      plVar9 = (long *)((long)local_90 + lVar8 + 0x10);
      *plVar9 = (long)&PTR_FUN_01fbd570;
      *(undefined4 *)((long)local_90 + lVar8 + 0x18) = 0x1010101;
      *(long **)((long)local_90 + lVar8 + 0x20) = plVar4;
      *(byte **)((long)local_90 + lVar8 + 0x28) = pbVar12;
      *(byte **)((long)local_90 + lVar8 + 0x30) = pbVar13;
      plVar4 = plVar9;
      local_13c0 = local_13b8;
joined_r0x00e9654c:
      if (param_2 != (void *)0x0) goto LAB_00e962f8;
      goto LAB_00e96550;
    }
LAB_00e966d0:
    pvVar16 = (void *)0x0;
    uVar7 = 0xfffffffe;
  }
  else {
    if ((sVar3 < 3) || (param_1[1] != 0x5f)) goto LAB_00e962d0;
    if (param_1[2] == 0x5a) {
      lVar8 = 3;
      goto LAB_00e96204;
    }
    if (sVar3 < 4) goto LAB_00e962d0;
    if ((param_1[2] == 0x5f) && (param_1[3] == 0x5a)) {
      lVar8 = 4;
    }
    else {
      if ((sVar3 < 5) || (((param_1[2] != 0x5f || (param_1[3] != 0x5f)) || (param_1[4] != 0x5a))))
      goto LAB_00e962d0;
      lVar8 = 5;
    }
    local_13c0 = param_1 + lVar8;
    lVar8 = FUN_00e96790(&local_13c0);
    puVar6 = local_90;
    if (lVar8 != 0) {
      if (((((0xc < (ulong)((long)local_13b8 - (long)local_13c0)) && (*local_13c0 == 0x5f)) &&
           ((local_13c0[1] == 0x62 &&
            ((((local_13c0[2] == 0x6c && (local_13c0[3] == 0x6f)) && (local_13c0[4] == 99)) &&
             ((local_13c0[5] == 0x6b && (local_13c0[6] == 0x5f)))))))) && (local_13c0[7] == 0x69))
         && (((local_13c0[8] == 0x6e && (local_13c0[9] == 0x76)) &&
             ((local_13c0[10] == 0x6f && ((local_13c0[0xb] == 0x6b && (local_13c0[0xc] == 0x65))))))
            )) {
        pbVar12 = local_13c0 + 0xd;
        if (pbVar12 != local_13b8) {
          bVar1 = *pbVar12;
          if (bVar1 == 0x5f) {
            pbVar12 = local_13c0 + 0xe;
          }
          local_13c0 = pbVar12;
          if (local_13b8 == pbVar12) {
            pbVar13 = (byte *)0x0;
            pbVar14 = local_13b8;
            pbVar15 = (byte *)0x0;
          }
          else if (*pbVar12 - 0x30 < 10) {
            do {
              local_13c0 = local_13c0 + 1;
              pbVar13 = pbVar12;
              pbVar14 = local_13b8;
              pbVar15 = local_13b8;
              if (local_13b8 == local_13c0) break;
              pbVar14 = local_13c0;
              pbVar15 = local_13c0;
            } while (*local_13c0 - 0x30 < 10);
          }
          else {
            pbVar13 = (byte *)0x0;
            pbVar14 = pbVar12;
            pbVar15 = (byte *)0x0;
          }
          if ((bVar1 == 0x5f) && (pbVar13 == pbVar15)) goto LAB_00e966d0;
          pbVar12 = local_13c0;
          if (local_13b8 != pbVar14) {
            if (*pbVar14 != 0x2e) goto LAB_00e966d0;
            local_13c0 = local_13b8;
            pbVar12 = local_13c0;
          }
        }
        local_13c0 = pbVar12;
        lVar10 = local_90[1];
        if (0xfef < lVar10 + 0x30U) {
          puVar5 = (undefined8 *)malloc(0x1000);
          if (puVar5 == (undefined8 *)0x0) goto LAB_00e966e8;
          lVar10 = 0;
          *puVar5 = puVar6;
          puVar5[1] = 0;
          local_90 = puVar5;
        }
        local_90[1] = lVar10 + 0x30;
        plVar4 = (long *)((long)local_90 + lVar10 + 0x10);
        *plVar4 = (long)&PTR_FUN_01fbbb20;
        *(undefined4 *)((long)local_90 + lVar10 + 0x18) = 0x1010114;
        *(char **)((long)local_90 + lVar10 + 0x20) = "invocation function for block in ";
        *(char **)((long)local_90 + lVar10 + 0x28) = "";
        *(long *)((long)local_90 + lVar10 + 0x30) = lVar8;
        goto joined_r0x00e9654c;
      }
      goto LAB_00e966d0;
    }
    uVar7 = 0xfffffffe;
    pvVar16 = (void *)0x0;
  }
LAB_00e965fc:
  if (param_4 != (undefined4 *)0x0) {
    *param_4 = uVar7;
  }
  while (puVar6 = local_90, local_90 != (undefined8 *)0x0) {
    while (local_90 = (undefined8 *)*puVar6, &local_1090 == puVar6) {
      puVar6 = local_90;
      if (local_90 == (undefined8 *)0x0) goto LAB_00e96634;
    }
    free(puVar6);
  }
LAB_00e96634:
  local_1090 = 0;
  uStack_1088 = 0;
  local_90 = &local_1090;
  if (local_10f0 != &local_10d8) {
    free(local_10f0);
  }
  if (local_1128 != &local_1110) {
    free(local_1128);
  }
  if (local_1180 != &local_1168) {
    free(local_1180);
  }
  if (local_1298 != &local_1280) {
    free(local_1298);
  }
  if (local_13b0 != &local_1398) {
    free(local_13b0);
  }
LAB_00e96694:
  if (*(long *)(lVar2 + 0x28) != local_78) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return pvVar16;
}



// ==========================================================================================
// Function: __gxx_personality_v0
// Address: 00eaa1dc
// ==========================================================================================

void __gxx_personality_v0(int param_1,ulong param_2,ulong param_3,long param_4,long param_5)

{
  long lVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  long local_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 local_58;
  uint local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  uVar3 = 3;
  if (((param_1 == 1) && (param_4 != 0)) && (param_5 != 0)) {
    param_3 = param_3 & 0xffffffffffffff00;
    if ((param_2 & 1) == 0) {
      if (((uint)param_2 >> 1 & 1) == 0) {
        uVar3 = 3;
      }
      else {
        if (((uint)param_2 >> 2 & 1) == 0) {
          FUN_00eaa3ac(&local_78,param_2,param_3 == 0x434c4e47432b2b00,param_4,param_5);
          uVar3 = (ulong)local_50;
          if (local_50 != 6) goto LAB_00eaa370;
          thunk_FUN_00ead734(param_5,0,param_4);
          thunk_FUN_00ead734(param_5,1,local_78);
          uVar4 = local_60;
        }
        else {
          if (param_3 == 0x434c4e47432b2b00) {
            local_78 = (long)*(int *)(param_4 + -0x24);
            uStack_68 = *(undefined8 *)(param_4 + -0x18);
            local_70 = *(undefined8 *)(param_4 + -0x20);
            local_60 = *(undefined8 *)(param_4 + -0x10);
            local_58 = *(undefined8 *)(param_4 + -8);
          }
          else {
            FUN_00eaa3ac(&local_78,param_2,0,param_4,param_5);
            if (local_50 != 6) {
              uVar3 = FUN_00eaa994(0,param_4);
              goto LAB_00eaa3a8;
            }
          }
          uVar4 = local_60;
          lVar2 = local_78;
          thunk_FUN_00ead734(param_5,0,param_4);
          thunk_FUN_00ead734(param_5,1,lVar2);
        }
        FUN_00ead610(param_5,uVar4);
        uVar3 = 7;
      }
    }
    else {
      FUN_00eaa3ac(&local_78,param_2,param_3 == 0x434c4e47432b2b00,param_4,param_5);
      uVar3 = (ulong)local_50;
      if ((local_50 == 6) && (param_3 == 0x434c4e47432b2b00)) {
        uVar3 = 6;
        *(int *)(param_4 + -0x24) = (int)local_78;
        *(undefined8 *)(param_4 + -0x18) = uStack_68;
        *(undefined8 *)(param_4 + -0x20) = local_70;
        *(undefined8 *)(param_4 + -0x10) = local_60;
        *(undefined8 *)(param_4 + -8) = local_58;
      }
    }
  }
LAB_00eaa370:
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return;
  }
LAB_00eaa3a8:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar3);
}



// ==========================================================================================
// Function: __cxa_call_unexpected
// Address: 00eaa9c4
// ==========================================================================================

void __cxa_call_unexpected(long param_1)

{
  long lVar1;
  byte bVar2;
  byte bVar3;
  undefined *puVar4;
  uint uVar5;
  ulong uVar6;
  undefined8 uVar7;
  long *plVar8;
  long *plVar9;
  ulong uVar10;
  ulong uVar11;
  byte *extraout_x9;
  undefined *unaff_x19;
  undefined8 uVar12;
  ulong uVar13;
  undefined **unaff_x23;
  undefined **ppuVar14;
  long lVar15;
  undefined *puVar16;
  byte *pbVar17;
  long lVar19;
  ulong uVar20;
  undefined *local_78;
  byte *local_70;
  undefined **local_68;
  byte *pbVar18;
  
  if (param_1 == 0) {
    param_1 = FUN_00eaa994(0,0);
  }
  __cxa_begin_catch();
  uVar6 = FUN_00e951d0(param_1);
  if ((uVar6 & 1) == 0) {
    uVar12 = std::get_terminate();
    uVar7 = std::get_unexpected();
    lVar15 = 0;
  }
  else {
    uVar7 = *(undefined8 *)(param_1 + -0x40);
    uVar12 = *(undefined8 *)(param_1 + -0x38);
    unaff_x19 = *(undefined **)(param_1 + -0x18);
    lVar15 = param_1 + -0x60;
    unaff_x23 = (undefined **)(long)(int)~*(uint *)(param_1 + -0x24);
  }
                    /* try { // try from 00eaaa38 to 00eaaa3b has its CatchHandler @ 00eaaa3c */
  FUN_00e95dd8(uVar7);
                    /* catch(type#1 @ 00000000) { ... } // from try @ 00eaaa38 with catch @ 00eaaa3c
                        */
  __cxa_begin_catch();
  ppuVar14 = unaff_x23;
  if ((uVar6 & 1) != 0) {
    local_70 = unaff_x19 + 1;
                    /* try { // try from 00eaaa50 to 00eaaa57 has its CatchHandler @ 00eaad20 */
    FUN_00eaad34(&local_70,*unaff_x19);
    bVar3 = *local_70;
    uVar6 = (ulong)bVar3;
    if (uVar6 != 0xff) goto LAB_00eaaa70;
    do {
      FUN_00e95e24(uVar12);
      local_70 = extraout_x9;
LAB_00eaaa70:
      uVar10 = 0;
      uVar20 = 0;
      pbVar18 = local_70 + 1;
      do {
        pbVar17 = pbVar18 + 1;
        bVar2 = *pbVar18;
        uVar20 = ((ulong)bVar2 & 0x7f) << (uVar10 & 0x3f) | uVar20;
        uVar10 = uVar10 + 7;
        pbVar18 = pbVar17;
      } while ((char)bVar2 < '\0');
      local_70 = pbVar17;
                    /* try { // try from 00eaaa98 to 00eaaa9b has its CatchHandler @ 00eaad1c */
      plVar8 = (long *)__cxa_get_globals_fast();
      lVar19 = *plVar8;
    } while (lVar19 == 0);
    lVar1 = lVar19 + 0x60;
                    /* try { // try from 00eaaaac to 00eaaab3 has its CatchHandler @ 00eaad18 */
    uVar5 = FUN_00e951d0(lVar1);
    if ((lVar19 != lVar15) && (((uVar5 ^ 1) & 1) == 0)) {
      uVar7 = *(undefined8 *)(lVar19 + 0x10);
                    /* try { // try from 00eaaae4 to 00eaaae7 has its CatchHandler @ 00eaad14 */
      lVar15 = FUN_00e951c4(lVar1);
      if (lVar15 == 0x434c4e47432b2b01) {
        ppuVar14 = *(undefined ***)(lVar19 + 8);
      }
      else {
        ppuVar14 = (undefined **)(lVar19 + 0x80);
      }
      uVar13 = uVar6 & 0xf;
      uVar10 = 0;
      uVar11 = 0;
      puVar16 = (undefined *)((long)unaff_x23 + uVar20);
      while( true ) {
        for (; uVar11 = ((ulong)pbVar17[(long)puVar16] & 0x7f) << (uVar10 & 0x3f) | uVar11,
            (char)pbVar17[(long)puVar16] < '\0'; puVar16 = puVar16 + 1) {
          uVar10 = uVar10 + 7;
        }
        if (uVar11 == 0) break;
        if ((0xc < (uint)uVar13) || ((0x1c1dU >> uVar13 & 1) == 0)) goto LAB_00eaac74;
        local_68 = (undefined **)(pbVar17 + uVar11 * *(long *)(&DAT_0083b748 + uVar13 * 8) + uVar20)
        ;
                    /* try { // try from 00eaab7c to 00eaab9f has its CatchHandler @ 00eaacfc */
        plVar9 = (long *)FUN_00eaad34(&local_68,uVar6);
        local_68 = ppuVar14;
        uVar10 = (**(code **)(*plVar9 + 0x20))(plVar9,uVar7,&local_68);
        if ((uVar10 & 1) != 0) {
          *(int *)(lVar19 + 0x38) = -*(int *)(lVar19 + 0x38);
          *(int *)(plVar8 + 1) = *(int *)(plVar8 + 1) + 1;
                    /* try { // try from 00eaace4 to 00eaacfb has its CatchHandler @ 00eaad14 */
          __cxa_end_catch();
          __cxa_end_catch();
          __cxa_begin_catch(lVar1);
          uVar12 = __cxa_rethrow();
                    /* catch(type#1 @ 00000000) { ... } // from try @ 00eaab7c with catch @ 00eaacfc
                        */
                    /* catch(type#1 @ 00000000) { ... } // from try @ 00eaaa50 with catch @ 00eaad20
                        */
                    /* try { // try from 00eaad24 to 00eaad27 has its CatchHandler @ 00eaad30 */
          __cxa_end_catch();
                    /* WARNING: Subroutine does not return */
          FUN_00ead3e8(uVar12);
        }
        uVar10 = 0;
        uVar11 = 0;
        puVar16 = puVar16 + 1;
      }
    }
    puVar4 = PTR_PTR_01ff59b0;
    ppuVar14 = (undefined **)PTR_vtable_01ff59a8;
    puVar16 = (undefined *)((long)unaff_x23 + uVar20);
    local_78 = PTR_vtable_01ff59a8 + 0x10;
    uVar11 = (ulong)(bVar3 + 6) & 0xf;
    uVar6 = 0;
    uVar10 = 0;
    while( true ) {
      for (; uVar10 = ((ulong)pbVar17[(long)puVar16] & 0x7f) << (uVar6 & 0x3f) | uVar10,
          (char)pbVar17[(long)puVar16] < '\0'; puVar16 = puVar16 + 1) {
        uVar6 = uVar6 + 7;
      }
      if (uVar10 == 0) goto LAB_00eaac80;
      if ((10 < (uint)uVar11) || ((0x747U >> uVar11 & 1) == 0)) goto LAB_00eaac74;
      local_68 = (undefined **)(pbVar17 + uVar10 * *(long *)(&DAT_0083b7b0 + uVar11 * 8) + uVar20);
                    /* try { // try from 00eaac3c to 00eaac5f has its CatchHandler @ 00eaad04 */
      plVar8 = (long *)FUN_00eaad34(&local_68,(uint)bVar3);
      local_68 = &local_78;
      uVar6 = (**(code **)(*plVar8 + 0x20))(plVar8,puVar4,&local_68);
      if ((uVar6 & 1) != 0) break;
      uVar6 = 0;
      uVar10 = 0;
      puVar16 = puVar16 + 1;
    }
    goto LAB_00eaac98;
  }
  goto LAB_00eaac8c;
LAB_00eaac74:
  FUN_00eaa994(1,param_1);
LAB_00eaac80:
  std::bad_alloc::~bad_alloc((bad_alloc *)&local_78);
LAB_00eaac8c:
  __cxa_end_catch();
  FUN_00e95e24(uVar12);
LAB_00eaac98:
                    /* try { // try from 00eaac98 to 00eaac9b has its CatchHandler @ 00eaad00 */
  __cxa_end_catch();
  plVar8 = (long *)__cxa_allocate_exception(8);
  *plVar8 = (long)(ppuVar14 + 2);
                    /* try { // try from 00eaacac to 00eaacbf has its CatchHandler @ 00eaad00 */
                    /* WARNING: Subroutine does not return */
  __cxa_throw(plVar8,PTR_PTR_01ff59b0,PTR__bad_alloc_01ff59b8);
}



// ==========================================================================================
// Function: __cxa_pure_virtual
// Address: 00eaaeac
// ==========================================================================================

void __cxa_pure_virtual(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e95c8c("Pure virtual function called!");
}



// ==========================================================================================
// Function: __cxa_deleted_virtual
// Address: 00eaaec4
// ==========================================================================================

void __cxa_deleted_virtual(void)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e95c8c("Deleted virtual function called!");
}



// ==========================================================================================
// Function: __dynamic_cast
// Address: 00eabd4c
// ==========================================================================================

void __dynamic_cast(long *param_1,undefined8 param_2,long param_3,undefined8 param_4)

{
  long lVar1;
  long *plVar2;
  long lVar3;
  long local_78;
  long *plStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  long local_58;
  long lStack_50;
  undefined8 local_48;
  int iStack_40;
  int iStack_3c;
  int local_38;
  undefined4 uStack_34;
  undefined4 local_30;
  uint uStack_2c;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  plVar2 = *(long **)(*param_1 + -8);
  lStack_50 = 0;
  local_58 = 0;
  iStack_40 = 0;
  local_48 = 0;
  local_30 = 0;
  uStack_2c = uStack_2c & 0xff000000;
  iStack_3c = 0;
  local_38 = 0;
  uStack_34 = 0;
  lVar3 = (long)param_1 + *(long *)(*param_1 + -0x10);
  local_78 = param_3;
  plStack_70 = param_1;
  local_68 = param_2;
  uStack_60 = param_4;
  if (plVar2[1] == *(long *)(param_3 + 8)) {
    local_30 = 1;
    (**(code **)(*plVar2 + 0x28))(plVar2,&local_78,lVar3,lVar3,1,0);
    if ((int)local_48 != 1) {
      lVar3 = 0;
    }
  }
  else {
    (**(code **)(*plVar2 + 0x30))(plVar2,&local_78,lVar3,1,0);
    if (iStack_3c == 1) {
      if (((int)local_48 == 1) ||
         (((lVar3 = 0, local_38 == 0 && (local_48._4_4_ == 1)) && (iStack_40 == 1)))) {
        lVar3 = local_58;
      }
    }
    else if (iStack_3c == 0) {
      lVar3 = lStack_50;
      if ((iStack_40 != 1 || local_48._4_4_ != 1) || local_38 != 1) {
        lVar3 = 0;
      }
    }
    else {
      lVar3 = 0;
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(lVar3);
}



// ==========================================================================================
// Function: __emutls_get_address
// Address: 00eacf30
// ==========================================================================================

void * __emutls_get_address(size_t *param_1)

{
  undefined8 *__ptr;
  void *pvVar1;
  void *__s;
  ulong uVar2;
  size_t __n;
  size_t sVar3;
  long lVar4;
  
  sVar3 = param_1[2];
  if (sVar3 == 0) {
    pthread_once((pthread_once_t *)&DAT_0231e2d8,FUN_00ead128);
    pthread_mutex_lock((pthread_mutex_t *)&DAT_0231e2e8);
    sVar3 = param_1[2];
    if (sVar3 == 0) {
      sVar3 = DAT_0231e2e0 + 1;
      DAT_0231e2e0 = sVar3;
      param_1[2] = sVar3;
    }
    pthread_mutex_unlock((pthread_mutex_t *)&DAT_0231e2e8);
    __ptr = (undefined8 *)pthread_getspecific(DAT_0231e2d4);
    if (__ptr != (undefined8 *)0x0) goto LAB_00eacf64;
LAB_00ead010:
    lVar4 = (sVar3 + 0x11 & 0xfffffffffffffff0) - 2;
    __ptr = (undefined8 *)malloc(lVar4 * 8 + 0x10);
    if (__ptr == (undefined8 *)0x0) goto LAB_00ead0ec;
    memset(__ptr + 2,0,lVar4 * 8);
    *__ptr = 1;
LAB_00ead048:
    __ptr[1] = lVar4;
    pthread_setspecific(DAT_0231e2d4,__ptr);
  }
  else {
    __ptr = (undefined8 *)pthread_getspecific(DAT_0231e2d4);
    if (__ptr == (undefined8 *)0x0) goto LAB_00ead010;
LAB_00eacf64:
    uVar2 = __ptr[1];
    if (uVar2 < sVar3) {
      lVar4 = (sVar3 + 0x11 & 0xfffffffffffffff0) - 2;
      __ptr = (undefined8 *)realloc(__ptr,lVar4 * 8 + 0x10);
      if (__ptr == (undefined8 *)0x0) goto LAB_00ead0ec;
      memset(__ptr + uVar2 + 2,0,(lVar4 - uVar2) * 8);
      goto LAB_00ead048;
    }
  }
  pvVar1 = (void *)__ptr[sVar3 + 1];
  if (pvVar1 != (void *)0x0) {
    return pvVar1;
  }
  uVar2 = param_1[1];
  if (uVar2 < 9) {
    uVar2 = 8;
  }
  if ((uVar2 & uVar2 - 1) == 0) {
    __n = *param_1;
    pvVar1 = malloc(uVar2 + 7 + __n);
    if (pvVar1 != (void *)0x0) {
      __s = (void *)((long)pvVar1 + uVar2 + 7 & -uVar2);
      *(void **)((long)__s + -8) = pvVar1;
      if ((void *)param_1[3] == (void *)0x0) {
        memset(__s,0,__n);
      }
      else {
        memcpy(__s,(void *)param_1[3],__n);
      }
      __ptr[sVar3 + 1] = __s;
      return __s;
    }
  }
LAB_00ead0ec:
                    /* WARNING: Subroutine does not return */
  abort();
}



// ==========================================================================================
// Function: __stop_il2cpp
// Address: 01ec5010
// ==========================================================================================

void __stop_il2cpp(void)

{
  (*(code *)PTR_01ff5a30)();
  return;
}



// ==========================================================================================
// Function: __cxa_finalize
// Address: 01ec5030
// ==========================================================================================

void __cxa_finalize(void)

{
  (*(code *)PTR___cxa_finalize_01ff5a38)();
  return;
}



// ==========================================================================================
// Function: __cxa_atexit
// Address: 01ec5040
// ==========================================================================================

void __cxa_atexit(void)

{
  (*(code *)PTR___cxa_atexit_01ff5a40)();
  return;
}



// ==========================================================================================
// Function: __cxa_begin_catch
// Address: 01ec5050
// ==========================================================================================

void __cxa_begin_catch(void)

{
  (*(code *)PTR___cxa_begin_catch_01ff5a48)();
  return;
}



// ==========================================================================================
// Function: __cxa_end_catch
// Address: 01ec5060
// ==========================================================================================

void __cxa_end_catch(void)

{
  (*(code *)PTR___cxa_end_catch_01ff5a50)();
  return;
}



// ==========================================================================================
// Function: __cxa_allocate_exception
// Address: 01ec5070
// ==========================================================================================

void __cxa_allocate_exception(void)

{
  (*(code *)PTR___cxa_allocate_exception_01ff5a58)();
  return;
}



// ==========================================================================================
// Function: __cxa_throw
// Address: 01ec5080
// ==========================================================================================

void __cxa_throw(void)

{
  (*(code *)PTR___cxa_throw_01ff5a60)();
  return;
}



// ==========================================================================================
// Function: __stack_chk_fail
// Address: 01ec50a0
// ==========================================================================================

void __stack_chk_fail(void)

{
  (*(code *)PTR___stack_chk_fail_01ff5a70)();
  return;
}



// ==========================================================================================
// Function: __errno
// Address: 01ec5390
// ==========================================================================================

void __errno(void)

{
  (*(code *)PTR___errno_01ff5be8)();
  return;
}



// ==========================================================================================
// Function: __throw_length_error
// Address: 01ec53c0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__basic_string_common<true>::__throw_length_error(void)

{
  (*(code *)PTR___throw_length_error_01ff5c00)();
  return;
}



// ==========================================================================================
// Function: __throw_length_error
// Address: 01ec53f0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__vector_base_common<true>::__throw_length_error(void)

{
  (*(code *)PTR___throw_length_error_01ff5c18)();
  return;
}



// ==========================================================================================
// Function: __cxa_free_exception
// Address: 01ec5400
// ==========================================================================================

void __cxa_free_exception(void)

{
  (*(code *)PTR___cxa_free_exception_01ff5c20)();
  return;
}



// ==========================================================================================
// Function: __cxa_guard_acquire
// Address: 01ec5660
// ==========================================================================================

void __cxa_guard_acquire(void)

{
  (*(code *)PTR___cxa_guard_acquire_01ff5d50)();
  return;
}



// ==========================================================================================
// Function: __cxa_guard_release
// Address: 01ec5680
// ==========================================================================================

void __cxa_guard_release(void)

{
  (*(code *)PTR___cxa_guard_release_01ff5d60)();
  return;
}



// ==========================================================================================
// Function: __cxa_guard_abort
// Address: 01ec5690
// ==========================================================================================

void __cxa_guard_abort(void)

{
  (*(code *)PTR___cxa_guard_abort_01ff5d68)();
  return;
}



// ==========================================================================================
// Function: __android_log_print
// Address: 01ec5860
// ==========================================================================================

void __android_log_print(void)

{
  (*(code *)PTR___android_log_print_01ff5e50)();
  return;
}



// ==========================================================================================
// Function: __cxa_rethrow
// Address: 01ec58d0
// ==========================================================================================

void __cxa_rethrow(void)

{
  (*(code *)PTR___cxa_rethrow_01ff5e88)();
  return;
}



// ==========================================================================================
// Function: __set_badbit_and_consider_rethrow
// Address: 01ec5ac0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::ios_base::__set_badbit_and_consider_rethrow(void)

{
  (*(code *)PTR___set_badbit_and_consider_rethrow_01ff5f80)();
  return;
}



// ==========================================================================================
// Function: __grow_by
// Address: 01ec5b20
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__grow_by(basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
         ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6)

{
  (*(code *)PTR___grow_by_01ff5fb0)();
  return;
}



// ==========================================================================================
// Function: __FD_SET_chk
// Address: 01ec5b90
// ==========================================================================================

void __FD_SET_chk(void)

{
  (*(code *)PTR___FD_SET_chk_01ff5fe8)();
  return;
}



// ==========================================================================================
// Function: __throw_out_of_range
// Address: 01ec5d60
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__basic_string_common<true>::__throw_out_of_range(void)

{
  (*(code *)PTR___throw_out_of_range_01ff60d0)();
  return;
}



// ==========================================================================================
// Function: __cxa_uncaught_exceptions
// Address: 01ec6110
// ==========================================================================================

void __cxa_uncaught_exceptions(void)

{
  (*(code *)PTR___cxa_uncaught_exceptions_01ff62a8)();
  return;
}



// ==========================================================================================
// Function: __cxa_decrement_exception_refcount
// Address: 01ec6120
// ==========================================================================================

void __cxa_decrement_exception_refcount(void)

{
  (*(code *)PTR___cxa_decrement_exception_refcount_01ff62b0)();
  return;
}



// ==========================================================================================
// Function: __cxa_increment_exception_refcount
// Address: 01ec6130
// ==========================================================================================

void __cxa_increment_exception_refcount(void)

{
  (*(code *)PTR___cxa_increment_exception_refcount_01ff62b8)();
  return;
}



// ==========================================================================================
// Function: __cxa_current_primary_exception
// Address: 01ec6140
// ==========================================================================================

void __cxa_current_primary_exception(void)

{
  (*(code *)PTR___cxa_current_primary_exception_01ff62c0)();
  return;
}



// ==========================================================================================
// Function: __cxa_rethrow_primary_exception
// Address: 01ec6150
// ==========================================================================================

void __cxa_rethrow_primary_exception(void)

{
  (*(code *)PTR___cxa_rethrow_primary_exception_01ff62c8)();
  return;
}



// ==========================================================================================
// Function: __throw_bad_alloc
// Address: 01ec6180
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__throw_bad_alloc(void)

{
  (*(code *)PTR___throw_bad_alloc_01ff62e0)();
  return;
}



// ==========================================================================================
// Function: ~__shared_weak_count
// Address: 01ec6310
// ==========================================================================================

void __thiscall std::__ndk1::__shared_weak_count::~__shared_weak_count(__shared_weak_count *this)

{
  (*(code *)PTR____shared_weak_count_01ff63a8)();
  return;
}



// ==========================================================================================
// Function: __call_once
// Address: 01ec6320
// ==========================================================================================

void std::__ndk1::__call_once(ulong *param_1,void *param_2,_func_void_void_ptr *param_3)

{
  (*(code *)PTR___call_once_01ff63b0)();
  return;
}



// ==========================================================================================
// Function: __release_shared
// Address: 01ec6330
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__shared_count::__release_shared(void)

{
  (*(code *)PTR___release_shared_01ff63b8)();
  return;
}



// ==========================================================================================
// Function: __do_get_signed<long>
// Address: 01ec6340
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_signed<long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          long *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_signed<long>_01ff63c0)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __stage2_int_prep
// Address: 01ec6350
// ==========================================================================================

void __thiscall
std::__ndk1::__num_get<char>::__stage2_int_prep
          (__num_get<char> *this,ios_base *param_1,char *param_2,char *param_3)

{
  (*(code *)PTR___stage2_int_prep_01ff63c8)();
  return;
}



// ==========================================================================================
// Function: __stage2_int_loop
// Address: 01ec6360
// ==========================================================================================

void std::__ndk1::__num_get<char>::__stage2_int_loop
               (char param_1,int param_2,char *param_3,char **param_4,uint *param_5,char param_6,
               basic_string *param_7,uint *param_8,uint **param_9,char *param_10)

{
  (*(code *)PTR___stage2_int_loop_01ff63d0)(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __check_grouping
// Address: 01ec6370
// ==========================================================================================

void std::__ndk1::__check_grouping(basic_string *param_1,uint *param_2,uint *param_3,uint *param_4)

{
  (*(code *)PTR___check_grouping_01ff63d8)();
  return;
}



// ==========================================================================================
// Function: __do_get_signed<long_long>
// Address: 01ec6380
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_signed<long_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          longlong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_signed<long_long>_01ff63e0)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_short>
// Address: 01ec6390
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_short>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ushort *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_short>_01ff63e8)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_int>
// Address: 01ec63a0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_int>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          uint *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_int>_01ff63f0)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long>
// Address: 01ec63b0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ulong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_long>_01ff63f8)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long_long>
// Address: 01ec63c0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_unsigned<unsigned_long_long>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          ulonglong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_long_long>_01ff6400)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_floating_point<float>
// Address: 01ec63d0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<float>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          float *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<float>_01ff6408)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __stage2_float_prep
// Address: 01ec63e0
// ==========================================================================================

void __thiscall
std::__ndk1::__num_get<char>::__stage2_float_prep
          (__num_get<char> *this,ios_base *param_1,char *param_2,char *param_3,char *param_4)

{
  (*(code *)PTR___stage2_float_prep_01ff6410)();
  return;
}



// ==========================================================================================
// Function: __stage2_float_loop
// Address: 01ec63f0
// ==========================================================================================

void std::__ndk1::__num_get<char>::__stage2_float_loop
               (char param_1,bool *param_2,char *param_3,char *param_4,char **param_5,char param_6,
               char param_7,basic_string *param_8,uint *param_9,uint **param_10,uint *param_11,
               char *param_12)

{
  (*(code *)PTR___stage2_float_loop_01ff6418)(param_1);
  return;
}



// ==========================================================================================
// Function: __do_get_floating_point<double>
// Address: 01ec6400
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<double>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          double *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<double>_01ff6420)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_floating_point<long_double>
// Address: 01ec6410
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__do_get_floating_point<long_double>
          (num_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>> *this
          ,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,uint *param_4,
          longdouble *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<long_double>_01ff6428)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __libcpp_sscanf_l
// Address: 01ec6420
// ==========================================================================================

void std::__ndk1::__libcpp_sscanf_l(char *param_1,__locale_t *param_2,char *param_3,...)

{
  (*(code *)PTR___libcpp_sscanf_l_01ff6430)();
  return;
}



// ==========================================================================================
// Function: __do_get_signed<long>
// Address: 01ec6460
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_signed<long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,long *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_signed<long>_01ff6450)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __stage2_int_prep
// Address: 01ec6470
// ==========================================================================================

void __thiscall
std::__ndk1::__num_get<wchar_t>::__stage2_int_prep
          (__num_get<wchar_t> *this,ios_base *param_1,wchar_t *param_2,wchar_t *param_3)

{
  (*(code *)PTR___stage2_int_prep_01ff6458)();
  return;
}



// ==========================================================================================
// Function: __stage2_int_loop
// Address: 01ec6480
// ==========================================================================================

void std::__ndk1::__num_get<wchar_t>::__stage2_int_loop
               (wchar_t param_1,int param_2,char *param_3,char **param_4,uint *param_5,
               wchar_t param_6,basic_string *param_7,uint *param_8,uint **param_9,wchar_t *param_10)

{
  (*(code *)PTR___stage2_int_loop_01ff6460)(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __do_get_signed<long_long>
// Address: 01ec6490
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_signed<long_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longlong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_signed<long_long>_01ff6468)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_short>
// Address: 01ec64a0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_short>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ushort *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_short>_01ff6470)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_int>
// Address: 01ec64b0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_int>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,uint *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_int>_01ff6478)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long>
// Address: 01ec64c0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_long>_01ff6480)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_unsigned<unsigned_long_long>
// Address: 01ec64d0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_unsigned<unsigned_long_long>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,ulonglong *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_unsigned<unsigned_long_long>_01ff6488)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_floating_point<float>
// Address: 01ec64e0
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<float>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,float *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<float>_01ff6490)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __stage2_float_prep
// Address: 01ec64f0
// ==========================================================================================

void __thiscall
std::__ndk1::__num_get<wchar_t>::__stage2_float_prep
          (__num_get<wchar_t> *this,ios_base *param_1,wchar_t *param_2,wchar_t *param_3,
          wchar_t *param_4)

{
  (*(code *)PTR___stage2_float_prep_01ff6498)();
  return;
}



// ==========================================================================================
// Function: __stage2_float_loop
// Address: 01ec6500
// ==========================================================================================

void std::__ndk1::__num_get<wchar_t>::__stage2_float_loop
               (wchar_t param_1,bool *param_2,char *param_3,char *param_4,char **param_5,
               wchar_t param_6,wchar_t param_7,basic_string *param_8,uint *param_9,uint **param_10,
               uint *param_11,wchar_t *param_12)

{
  (*(code *)PTR___stage2_float_loop_01ff64a0)(param_1);
  return;
}



// ==========================================================================================
// Function: __do_get_floating_point<double>
// Address: 01ec6510
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<double>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,double *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<double>_01ff64a8)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __do_get_floating_point<long_double>
// Address: 01ec6520
// ==========================================================================================

istreambuf_iterator __thiscall
std::__ndk1::
num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__do_get_floating_point<long_double>
          (num_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
           *this,istreambuf_iterator param_1,istreambuf_iterator param_2,ios_base *param_3,
          uint *param_4,longdouble *param_5)

{
  istreambuf_iterator iVar1;
  
  iVar1 = (*(code *)PTR___do_get_floating_point<long_double>_01ff64b0)((int)this,param_1,param_2);
  return iVar1;
}



// ==========================================================================================
// Function: __libcpp_snprintf_l
// Address: 01ec6530
// ==========================================================================================

void std::__ndk1::__libcpp_snprintf_l
               (char *param_1,ulong param_2,__locale_t *param_3,char *param_4,...)

{
  (*(code *)PTR___libcpp_snprintf_l_01ff64b8)();
  return;
}



// ==========================================================================================
// Function: __widen_and_group_int
// Address: 01ec6540
// ==========================================================================================

void std::__ndk1::__num_put<char>::__widen_and_group_int
               (char *param_1,char *param_2,char *param_3,char *param_4,char **param_5,
               char **param_6,locale *param_7)

{
  (*(code *)PTR___widen_and_group_int_01ff64c0)();
  return;
}



// ==========================================================================================
// Function: __vsnprintf_chk
// Address: 01ec6550
// ==========================================================================================

void __vsnprintf_chk(void)

{
  (*(code *)PTR___vsnprintf_chk_01ff64c8)();
  return;
}



// ==========================================================================================
// Function: __libcpp_asprintf_l
// Address: 01ec6560
// ==========================================================================================

void std::__ndk1::__libcpp_asprintf_l(char **param_1,__locale_t *param_2,char *param_3,...)

{
  (*(code *)PTR___libcpp_asprintf_l_01ff64d0)();
  return;
}



// ==========================================================================================
// Function: __widen_and_group_float
// Address: 01ec6570
// ==========================================================================================

void std::__ndk1::__num_put<char>::__widen_and_group_float
               (char *param_1,char *param_2,char *param_3,char *param_4,char **param_5,
               char **param_6,locale *param_7)

{
  (*(code *)PTR___widen_and_group_float_01ff64d8)();
  return;
}



// ==========================================================================================
// Function: __widen_and_group_int
// Address: 01ec65b0
// ==========================================================================================

void std::__ndk1::__num_put<wchar_t>::__widen_and_group_int
               (char *param_1,char *param_2,char *param_3,wchar_t *param_4,wchar_t **param_5,
               wchar_t **param_6,locale *param_7)

{
  (*(code *)PTR___widen_and_group_int_01ff64f8)();
  return;
}



// ==========================================================================================
// Function: __widen_and_group_float
// Address: 01ec65d0
// ==========================================================================================

void std::__ndk1::__num_put<wchar_t>::__widen_and_group_float
               (char *param_1,char *param_2,char *param_3,wchar_t *param_4,wchar_t **param_5,
               wchar_t **param_6,locale *param_7)

{
  (*(code *)PTR___widen_and_group_float_01ff6508)();
  return;
}



// ==========================================================================================
// Function: __get_white_space
// Address: 01ec65f0
// ==========================================================================================

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_white_space(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
                  *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
                 ctype *param_4)

{
  (*(code *)PTR___get_white_space_01ff6518)(this,param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __get_percent
// Address: 01ec6600
// ==========================================================================================

void __thiscall
std::__ndk1::time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::
__get_percent(time_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>
              *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
             ctype *param_4)

{
  (*(code *)PTR___get_percent_01ff6520)(this,param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __get_white_space
// Address: 01ec6620
// ==========================================================================================

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_white_space(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
                  *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
                 ctype *param_4)

{
  (*(code *)PTR___get_white_space_01ff6530)(this,param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __get_percent
// Address: 01ec6630
// ==========================================================================================

void __thiscall
std::__ndk1::
time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>::
__get_percent(time_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
              *this,istreambuf_iterator *param_1,istreambuf_iterator param_2,uint *param_3,
             ctype *param_4)

{
  (*(code *)PTR___get_percent_01ff6538)(this,param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __do_put
// Address: 01ec6650
// ==========================================================================================

void __thiscall
std::__ndk1::__time_put::__do_put
          (__time_put *this,wchar_t *param_1,wchar_t **param_2,tm *param_3,char param_4,char param_5
          )

{
  (*(code *)PTR___do_put_01ff6548)();
  return;
}



// ==========================================================================================
// Function: __throw_runtime_error
// Address: 01ec6670
// ==========================================================================================

void std::__ndk1::__throw_runtime_error(char *param_1)

{
  (*(code *)PTR___throw_runtime_error_01ff6558)();
  return;
}



// ==========================================================================================
// Function: __do_get
// Address: 01ec6690
// ==========================================================================================

void std::__ndk1::
     money_get<char,std::__ndk1::istreambuf_iterator<char,std::__ndk1::char_traits<char>>>::__do_get
               (istreambuf_iterator *param_1,istreambuf_iterator param_2,bool param_3,
               locale *param_4,uint param_5,uint *param_6,bool *param_7,ctype *param_8,
               unique_ptr *param_9,char **param_10,char *param_11)

{
  (*(code *)PTR___do_get_01ff6568)(param_1,param_2,param_3,param_4,param_5);
  return;
}



// ==========================================================================================
// Function: __gather_info
// Address: 01ec66b0
// ==========================================================================================

void std::__ndk1::__money_get<char>::__gather_info
               (bool param_1,locale *param_2,pattern *param_3,char *param_4,char *param_5,
               basic_string *param_6,basic_string *param_7,basic_string *param_8,
               basic_string *param_9,int *param_10)

{
  (*(code *)PTR___gather_info_01ff6578)(param_1);
  return;
}



// ==========================================================================================
// Function: __append_forward_unsafe<char*>
// Address: 01ec66d0
// ==========================================================================================

basic_string * __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__append_forward_unsafe<char*>
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          char *param_1,char *param_2)

{
  basic_string *pbVar1;
  
  pbVar1 = (basic_string *)(*(code *)PTR___append_forward_unsafe<char*>_01ff6588)();
  return pbVar1;
}



// ==========================================================================================
// Function: __do_get
// Address: 01ec66e0
// ==========================================================================================

void std::__ndk1::
     money_get<wchar_t,std::__ndk1::istreambuf_iterator<wchar_t,std::__ndk1::char_traits<wchar_t>>>
     ::__do_get(istreambuf_iterator *param_1,istreambuf_iterator param_2,bool param_3,
               locale *param_4,uint param_5,uint *param_6,bool *param_7,ctype *param_8,
               unique_ptr *param_9,wchar_t **param_10,wchar_t *param_11)

{
  (*(code *)PTR___do_get_01ff6590)(param_1,param_2,param_3,param_4,param_5);
  return;
}



// ==========================================================================================
// Function: __gather_info
// Address: 01ec66f0
// ==========================================================================================

void std::__ndk1::__money_get<wchar_t>::__gather_info
               (bool param_1,locale *param_2,pattern *param_3,wchar_t *param_4,wchar_t *param_5,
               basic_string *param_6,basic_string *param_7,basic_string *param_8,
               basic_string *param_9,int *param_10)

{
  (*(code *)PTR___gather_info_01ff6598)(param_1);
  return;
}



// ==========================================================================================
// Function: __append_forward_unsafe<wchar_t*>
// Address: 01ec6710
// ==========================================================================================

basic_string * __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__append_forward_unsafe<wchar_t*>
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,wchar_t *param_1,wchar_t *param_2)

{
  basic_string *pbVar1;
  
  pbVar1 = (basic_string *)(*(code *)PTR___append_forward_unsafe<wchar_t*>_01ff65a8)();
  return pbVar1;
}



// ==========================================================================================
// Function: __gather_info
// Address: 01ec6720
// ==========================================================================================

void std::__ndk1::__money_put<char>::__gather_info
               (bool param_1,bool param_2,locale *param_3,pattern *param_4,char *param_5,
               char *param_6,basic_string *param_7,basic_string *param_8,basic_string *param_9,
               int *param_10)

{
  (*(code *)PTR___gather_info_01ff65b0)(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __format
// Address: 01ec6730
// ==========================================================================================

void std::__ndk1::__money_put<char>::__format
               (char *param_1,char **param_2,char **param_3,uint param_4,char *param_5,char *param_6
               ,ctype *param_7,bool param_8,pattern *param_9,char param_10,char param_11,
               basic_string *param_12,basic_string *param_13,basic_string *param_14,int param_15)

{
  (*(code *)PTR___format_01ff65b8)();
  return;
}



// ==========================================================================================
// Function: __gather_info
// Address: 01ec6740
// ==========================================================================================

void std::__ndk1::__money_put<wchar_t>::__gather_info
               (bool param_1,bool param_2,locale *param_3,pattern *param_4,wchar_t *param_5,
               wchar_t *param_6,basic_string *param_7,basic_string *param_8,basic_string *param_9,
               int *param_10)

{
  (*(code *)PTR___gather_info_01ff65c0)(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: __format
// Address: 01ec6750
// ==========================================================================================

void std::__ndk1::__money_put<wchar_t>::__format
               (wchar_t *param_1,wchar_t **param_2,wchar_t **param_3,uint param_4,wchar_t *param_5,
               wchar_t *param_6,ctype *param_7,bool param_8,pattern *param_9,wchar_t param_10,
               wchar_t param_11,basic_string *param_12,basic_string *param_13,basic_string *param_14
               ,int param_15)

{
  (*(code *)PTR___format_01ff65c8)();
  return;
}



// ==========================================================================================
// Function: __add_shared
// Address: 01ec6770
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__shared_count::__add_shared(void)

{
  (*(code *)PTR___add_shared_01ff65d8)();
  return;
}



// ==========================================================================================
// Function: __init
// Address: 01ec67d0
// ==========================================================================================

void __thiscall
std::__ndk1::numpunct_byname<char>::__init(numpunct_byname<char> *this,char *param_1)

{
  (*(code *)PTR___init_01ff6608)();
  return;
}



// ==========================================================================================
// Function: __init
// Address: 01ec67e0
// ==========================================================================================

void __thiscall
std::__ndk1::numpunct_byname<wchar_t>::__init(numpunct_byname<wchar_t> *this,char *param_1)

{
  (*(code *)PTR___init_01ff6610)();
  return;
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 01ec67f0
// ==========================================================================================

void __thiscall
std::__ndk1::__time_get_storage<char>::__time_get_storage
          (__time_get_storage<char> *this,basic_string *param_1)

{
  (*(code *)PTR___time_get_storage_01ff6618)();
  return;
}



// ==========================================================================================
// Function: __time_get_storage
// Address: 01ec6800
// ==========================================================================================

void __thiscall
std::__ndk1::__time_get_storage<wchar_t>::__time_get_storage
          (__time_get_storage<wchar_t> *this,basic_string *param_1)

{
  (*(code *)PTR___time_get_storage_01ff6620)();
  return;
}



// ==========================================================================================
// Function: __global
// Address: 01ec6850
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::locale::__global(void)

{
  (*(code *)PTR___global_01ff6648)();
  return;
}



// ==========================================================================================
// Function: __ctype_get_mb_cur_max
// Address: 01ec6a70
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t __ctype_get_mb_cur_max(void)

{
  size_t sVar1;
  
  sVar1 = (*(code *)PTR___ctype_get_mb_cur_max_01ff6758)();
  return sVar1;
}



// ==========================================================================================
// Function: __strlen_chk
// Address: 01ec6ac0
// ==========================================================================================

void __strlen_chk(void)

{
  (*(code *)PTR___strlen_chk_01ff6780)();
  return;
}



// ==========================================================================================
// Function: __analyze
// Address: 01ec6ae0
// ==========================================================================================

void std::__ndk1::__time_get_storage<char>::__analyze(char param_1,ctype *param_2)

{
  (*(code *)PTR___analyze_01ff6790)(param_1);
  return;
}



// ==========================================================================================
// Function: __grow_by
// Address: 01ec6af0
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__grow_by(basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
            *this,ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,
           ulong param_6)

{
  (*(code *)PTR___grow_by_01ff6798)();
  return;
}



// ==========================================================================================
// Function: __analyze
// Address: 01ec6b00
// ==========================================================================================

void std::__ndk1::__time_get_storage<wchar_t>::__analyze(char param_1,ctype *param_2)

{
  (*(code *)PTR___analyze_01ff67a0)(param_1);
  return;
}



// ==========================================================================================
// Function: __time_get
// Address: 01ec6b10
// ==========================================================================================

void __thiscall std::__ndk1::__time_get::__time_get(__time_get *this,char *param_1)

{
  (*(code *)PTR___time_get_01ff67a8)();
  return;
}



// ==========================================================================================
// Function: __do_date_order
// Address: 01ec6ba0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__time_get_storage<char>::__do_date_order(void)

{
  (*(code *)PTR___do_date_order_01ff67f0)();
  return;
}



// ==========================================================================================
// Function: __do_date_order
// Address: 01ec6bb0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__time_get_storage<wchar_t>::__do_date_order(void)

{
  (*(code *)PTR___do_date_order_01ff67f8)();
  return;
}



// ==========================================================================================
// Function: ~__time_put
// Address: 01ec6bc0
// ==========================================================================================

void __thiscall std::__ndk1::__time_put::~__time_put(__time_put *this)

{
  (*(code *)PTR____time_put_01ff6800)();
  return;
}



// ==========================================================================================
// Function: __throw_system_error
// Address: 01ec6c40
// ==========================================================================================

void std::__ndk1::__throw_system_error(int param_1,char *param_2)

{
  (*(code *)PTR___throw_system_error_01ff6840)(param_1);
  return;
}



// ==========================================================================================
// Function: __thread_local_data
// Address: 01ec6d10
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__thread_local_data(void)

{
  (*(code *)PTR___thread_local_data_01ff68a8)();
  return;
}



// ==========================================================================================
// Function: __thread_struct
// Address: 01ec6d20
// ==========================================================================================

void __thiscall std::__ndk1::__thread_struct::__thread_struct(__thread_struct *this)

{
  (*(code *)PTR___thread_struct_01ff68b0)();
  return;
}



// ==========================================================================================
// Function: __grow_by_and_replace
// Address: 01ec6dc0
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
__grow_by_and_replace
          (basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *this,
          ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6,
          char *param_7)

{
  (*(code *)PTR___grow_by_and_replace_01ff6900)();
  return;
}



// ==========================================================================================
// Function: __grow_by_and_replace
// Address: 01ec6df0
// ==========================================================================================

void __thiscall
std::__ndk1::basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
::__grow_by_and_replace
          (basic_string<wchar_t,std::__ndk1::char_traits<wchar_t>,std::__ndk1::allocator<wchar_t>>
           *this,ulong param_1,ulong param_2,ulong param_3,ulong param_4,ulong param_5,ulong param_6
          ,wchar_t *param_7)

{
  (*(code *)PTR___grow_by_and_replace_01ff6918)();
  return;
}



// ==========================================================================================
// Function: __u32toa
// Address: 01ec6f20
// ==========================================================================================

void std::__ndk1::__itoa::__u32toa(uint param_1,char *param_2)

{
  (*(code *)PTR___u32toa_01ff69b0)(param_1);
  return;
}



// ==========================================================================================
// Function: __u64toa
// Address: 01ec6f30
// ==========================================================================================

void std::__ndk1::__itoa::__u64toa(ulong param_1,char *param_2)

{
  (*(code *)PTR___u64toa_01ff69b8)();
  return;
}



// ==========================================================================================
// Function: __init
// Address: 01ec6f50
// ==========================================================================================

void __thiscall std::__ndk1::system_error::__init(void)

{
  (*(code *)PTR___init_01ff69c8)();
  return;
}



// ==========================================================================================
// Function: __make_ready
// Address: 01ec6fb0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void std::__ndk1::__assoc_sub_state::__make_ready(void)

{
  (*(code *)PTR___make_ready_01ff69f8)();
  return;
}



// ==========================================================================================
// Function: __make_ready_at_thread_exit
// Address: 01ec7000
// ==========================================================================================

void std::__ndk1::__thread_struct::__make_ready_at_thread_exit(__assoc_sub_state *param_1)

{
  (*(code *)PTR___make_ready_at_thread_exit_01ff6a20)();
  return;
}



// ==========================================================================================
// Function: __cxa_call_unexpected
// Address: 01ec7080
// ==========================================================================================

void __cxa_call_unexpected(void)

{
  (*(code *)PTR___cxa_call_unexpected_01ff6a60)();
  return;
}



// ==========================================================================================
// Function: __cxa_get_globals
// Address: 01ec7090
// ==========================================================================================

void __cxa_get_globals(void)

{
  (*(code *)PTR___cxa_get_globals_01ff6a68)();
  return;
}



// ==========================================================================================
// Function: __cxa_get_globals_fast
// Address: 01ec70c0
// ==========================================================================================

void __cxa_get_globals_fast(void)

{
  (*(code *)PTR___cxa_get_globals_fast_01ff6a80)();
  return;
}



// ==========================================================================================
// Function: __emutls_get_address
// Address: 01ec70d0
// ==========================================================================================

void __emutls_get_address(void)

{
  (*(code *)PTR___emutls_get_address_01ff6a88)();
  return;
}



// ==========================================================================================
// Function: __cxa_demangle
// Address: 01ec7140
// ==========================================================================================

void __cxa_demangle(void)

{
  (*(code *)PTR___cxa_demangle_01ff6ac0)();
  return;
}



// ==========================================================================================
// Function: __memmove_chk
// Address: 01ec7150
// ==========================================================================================

void __memmove_chk(void)

{
  (*(code *)PTR___memmove_chk_01ff6ac8)();
  return;
}



// ==========================================================================================
// Function: __dynamic_cast
// Address: 01ec7180
// ==========================================================================================

void __dynamic_cast(void)

{
  (*(code *)PTR___dynamic_cast_01ff6ae0)();
  return;
}



// ==========================================================================================
// Function: __cxa_atexit
// Address: 0231f000
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __cxa_atexit(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __cxa_finalize
// Address: 0231f008
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __cxa_finalize(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __stack_chk_fail
// Address: 0231f010
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __stack_chk_fail(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __errno
// Address: 0231f0e0
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __errno(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __android_log_print
// Address: 0231f298
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __android_log_print(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __FD_SET_chk
// Address: 0231f348
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __FD_SET_chk(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __ctype_get_mb_cur_max
// Address: 0231f600
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t __ctype_get_mb_cur_max(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __strlen_chk
// Address: 0231f608
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __strlen_chk(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __vsnprintf_chk
// Address: 0231f610
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __vsnprintf_chk(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
// Function: __memmove_chk
// Address: 0231f830
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void __memmove_chk(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
