// Function: JNI_OnLoad
// Address: 00dcbe90
// ==========================================================================================

undefined8 JNI_OnLoad(undefined8 param_1)

{
  __android_log_print(4,"IL2CPP","JNI_OnLoad");
  DAT_021078f0 = param_1;
  FUN_00dcb268(FUN_00dcbed4);
  return 0x10006;
}



// ==========================================================================================
// Function: JNI_OnUnload
// Address: 00dcc1ac
// ==========================================================================================

void JNI_OnUnload(void)

{
  __android_log_print(4,"IL2CPP","JNI_OnUnload");
  DAT_021078f0 = 0;
  return;
}



// ==========================================================================================
