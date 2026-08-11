// Function: il2cpp_string_intern
// Address: 00dad454
// ==========================================================================================

void il2cpp_string_intern(void)

{
  (*(code *)PTR_il2cpp_string_intern_01ff5cc8)();
  return;
}



// ==========================================================================================
// Function: il2cpp_init
// Address: 00de3d34
// ==========================================================================================

uint il2cpp_init(undefined8 param_1)

{
  uint uVar1;
  
  setlocale(6,"");
  uVar1 = FUN_00df48f0(param_1);
  return uVar1 & 1;
}



// ==========================================================================================
// Function: il2cpp_init_utf16
// Address: 00de3d60
// ==========================================================================================

uint il2cpp_init_utf16(void)

{
  void *pvVar1;
  byte bVar2;
  void *pvVar3;
  uint uVar4;
  byte local_38 [16];
  void *local_28;
  
  FUN_00dc6cc0(local_38);
  pvVar3 = local_28;
  bVar2 = local_38[0];
                    /* try { // try from 00de3d80 to 00de3d9f has its CatchHandler @ 00de3dc8 */
  setlocale(6,"");
  pvVar1 = (void *)((ulong)local_38 | 1);
  if ((bVar2 & 1) != 0) {
    pvVar1 = pvVar3;
  }
  uVar4 = FUN_00df48f0(pvVar1);
  if ((local_38[0] & 1) != 0) {
    operator_delete(local_28);
  }
  return uVar4 & 1;
}



// ==========================================================================================
// Function: il2cpp_shutdown
// Address: 00de3de4
// ==========================================================================================

void il2cpp_shutdown(void)

{
  char cVar1;
  bool bVar2;
  int iVar3;
  pthread_t pVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  int iVar8;
  long lVar9;
  undefined4 *puStack_50;
  long lStack_48;
  undefined8 uStack_40;
  undefined8 *puStack_38;
  undefined8 uStack_28;
  
  puStack_50 = &DAT_02108038;
  pVar4 = pthread_self();
  if (pVar4 == DAT_02108078) {
    DAT_02108080 = DAT_02108080 + 1;
  }
  else {
    iVar8 = 0;
    do {
      iVar3 = DAT_02108038;
      if (DAT_02108038 == iVar8) {
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(0x2108038,0x10);
        if (bVar2) {
          cVar1 = ExclusiveMonitorsStatus();
          DAT_02108038 = iVar8 + 1;
        }
        if (cVar1 != '\0') goto LAB_00df59f0;
        bVar2 = true;
      }
      else {
        ClearExclusiveLocal();
LAB_00df59f0:
        bVar2 = false;
      }
    } while ((iVar3 != 2) && (iVar8 = iVar3, !bVar2));
    while (iVar3 != 0) {
      FUN_00e4d8f8(&DAT_02108038,2,0xffffffff);
      do {
        iVar3 = DAT_02108038;
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(0x2108038,0x10);
        if (bVar2) {
          DAT_02108038 = 2;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
    }
    DAT_02108080 = 1;
    DAT_02108078 = pVar4;
  }
  DAT_021080f0 = DAT_021080f0 + -1;
  if (0 < DAT_021080f0) goto LAB_00df5b6c;
  lVar5 = FUN_00dfcf44(DAT_02107e40,"ProcessExit");
  if (lVar5 != 0) {
    plVar6 = (long *)FUN_00dce854();
    lVar9 = *plVar6;
    FUN_00df3d5c(*(undefined8 *)(lVar5 + 8),&puStack_38,lVar9 + *(int *)(lVar5 + 0x18),1);
    if (puStack_38 != (undefined8 *)0x0) {
      lStack_48 = lVar9;
      lVar5 = thunk_FUN_00deb928(DAT_02107d30,"System","EventArgs");
      if (lVar5 == 0) {
LAB_00df5af0:
        uStack_28 = 0;
      }
      else {
        FUN_00dfcccc(lVar5);
        lVar5 = FUN_00dfcf44(lVar5,"Empty");
        if (lVar5 == 0) goto LAB_00df5af0;
        FUN_00df44a4(lVar5,&uStack_28,0);
      }
      uStack_40 = uStack_28;
      uVar7 = FUN_00dfd198(*puStack_38,"Invoke",0xffffffff);
      FUN_00df5da8(uVar7,puStack_38,&lStack_48,&uStack_28);
    }
  }
  DAT_02108100 = 1;
  FUN_00e2b0d8();
  FUN_00de75f4();
  FUN_00dd2a24();
  thunk_FUN_00d9e750();
  FUN_00e0e5dc();
  FUN_00e32c08();
  FUN_00dd2488();
  FUN_00dcb814();
  FUN_00e156e8();
  thunk_FUN_00e43fd8();
  FUN_00dcb180();
  FUN_00dec3d4();
  FUN_00e2abf8();
  FUN_00e285dc();
  FUN_00d9e750();
  FUN_00d9e750();
LAB_00df5b6c:
  FUN_00da71f4(&puStack_50);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_config_dir
// Address: 00de3de8
// ==========================================================================================

void il2cpp_set_config_dir(char *param_1)

{
  std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
  assign((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
         &DAT_021080d8,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_data_dir
// Address: 00de3dec
// ==========================================================================================

void il2cpp_set_data_dir(char *param_1)

{
  std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
  assign((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
         &DAT_02108718,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_temp_dir
// Address: 00de3df0
// ==========================================================================================

void il2cpp_set_temp_dir(char *param_1)

{
  std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
  assign((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
         &DAT_02108730,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_commandline_arguments
// Address: 00de3df4
// ==========================================================================================

void il2cpp_set_commandline_arguments(undefined4 param_1,undefined8 param_2)

{
  FUN_00dc6864(param_2,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_commandline_arguments_utf16
// Address: 00de3e04
// ==========================================================================================

void il2cpp_set_commandline_arguments_utf16(undefined4 param_1,undefined8 param_2)

{
  FUN_00dc697c(param_2,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_config_utf16
// Address: 00de3e14
// ==========================================================================================

void il2cpp_set_config_utf16(void)

{
  byte abStack_28 [16];
  void *pvStack_18;
  
  FUN_00dc6cc0(abStack_28);
  FUN_00df5858(abStack_28);
  if ((abStack_28[0] & 1) != 0) {
    operator_delete(pvStack_18);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_set_config
// Address: 00de3e18
// ==========================================================================================

void il2cpp_set_config(undefined8 param_1)

{
  byte abStack_28 [16];
  void *pvStack_18;
  
  FUN_00d9e440(abStack_28,param_1);
  FUN_00df5858(abStack_28);
  if ((abStack_28[0] & 1) != 0) {
    operator_delete(pvStack_18);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_set_memory_callbacks
// Address: 00de3e1c
// ==========================================================================================

void il2cpp_set_memory_callbacks(undefined8 *param_1)

{
  PTR_FUN_020ff060 = (undefined *)param_1[6];
  PTR_free_020ff048 = (undefined *)param_1[3];
  PTR_free_020ff040 = (undefined *)param_1[2];
  PTR_realloc_020ff058 = (undefined *)param_1[5];
  PTR_calloc_020ff050 = (undefined *)param_1[4];
  PTR_FUN_020ff038 = (undefined *)param_1[1];
  PTR_malloc_020ff030 = (undefined *)*param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_memory_pool_set_region_size
// Address: 00de3e20
// ==========================================================================================

void il2cpp_memory_pool_set_region_size(undefined8 param_1)

{
  DAT_020ff068 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_memory_pool_get_region_size
// Address: 00de3e24
// ==========================================================================================

undefined8 il2cpp_memory_pool_get_region_size(void)

{
  return DAT_020ff068;
}



// ==========================================================================================
// Function: il2cpp_get_corlib
// Address: 00de3e28
// ==========================================================================================

undefined8 il2cpp_get_corlib(void)

{
  return *(undefined8 *)PTR_DAT_01ff5418;
}



// ==========================================================================================
// Function: il2cpp_add_internal_call
// Address: 00de3e2c
// ==========================================================================================

void il2cpp_add_internal_call(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  byte abStack_40 [16];
  void *pvStack_30;
  undefined auStack_28 [8];
  byte *pbStack_18;
  
  FUN_00d9e440(abStack_40,param_1);
  pbStack_18 = abStack_40;
  lVar1 = FUN_00e2c3ac(&DAT_02108920,abStack_40,&DAT_00816258,&pbStack_18,auStack_28);
  *(undefined8 *)(lVar1 + 0x38) = param_2;
  if ((abStack_40[0] & 1) != 0) {
    operator_delete(pvStack_30);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_resolve_icall
// Address: 00de3e30
// ==========================================================================================

undefined8 il2cpp_resolve_icall(undefined8 param_1)

{
  undefined8 *puVar1;
  allocator *paVar2;
  undefined8 uVar3;
  ulong uStack_58;
  undefined8 uStack_50;
  void *pvStack_48;
  ulong uStack_40;
  undefined8 uStack_38;
  void *pvStack_30;
  
  FUN_00d9e440(&uStack_40,param_1);
  puVar1 = (undefined8 *)FUN_00e2c554(&DAT_02108920,&uStack_40);
  if ((uStack_40 & 1) != 0) {
    operator_delete(pvStack_30);
  }
  if (puVar1 != &DAT_02108928) {
    return puVar1[7];
  }
  FUN_00d9e440(&uStack_40,param_1);
  paVar2 = (allocator *)
           std::__ndk1::
           basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::find
                     ((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>
                       *)&uStack_40,'(',0);
  if (paVar2 != (allocator *)0xffffffffffffffff) {
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    basic_string((basic_string *)&uStack_58,(ulong)&uStack_40,0,paVar2);
    if ((uStack_40 & 1) != 0) {
      operator_delete(pvStack_30);
    }
    uStack_38 = uStack_50;
    uStack_40 = uStack_58;
    pvStack_30 = pvStack_48;
    puVar1 = (undefined8 *)FUN_00e2c554(&DAT_02108920,&uStack_40);
    if (puVar1 != &DAT_02108928) {
      uVar3 = puVar1[7];
      goto LAB_00e2a14c;
    }
  }
  uVar3 = 0;
LAB_00e2a14c:
  if ((uStack_40 & 1) != 0) {
    operator_delete(pvStack_30);
  }
  return uVar3;
}



// ==========================================================================================
// Function: il2cpp_alloc
// Address: 00de3e34
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * il2cpp_alloc(size_t __size)

{
  void *pvVar1;
  
  pvVar1 = (void *)(*(code *)PTR_malloc_020ff030)();
  return pvVar1;
}



// ==========================================================================================
// Function: il2cpp_free
// Address: 00de3e38
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void il2cpp_free(void *__ptr)

{
  (*(code *)PTR_free_020ff040)();
  return;
}



// ==========================================================================================
// Function: il2cpp_array_class_get
// Address: 00de3e3c
// ==========================================================================================

void il2cpp_array_class_get(undefined8 param_1,undefined8 param_2)

{
  FUN_00da6550(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_array_length
// Address: 00de3e40
// ==========================================================================================

undefined4 il2cpp_array_length(long param_1)

{
  return *(undefined4 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: il2cpp_array_get_byte_length
// Address: 00de3e44
// ==========================================================================================

int il2cpp_array_get_byte_length(long *param_1)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  long lVar4;
  long *plVar5;
  ulong uVar6;
  
  if ((long *)param_1[2] == (long *)0x0) {
    iVar3 = (int)param_1[3];
  }
  else {
    bVar1 = *(byte *)(*param_1 + 0x132);
    if (bVar1 == 0) {
      iVar3 = 1;
    }
    else {
      uVar2 = (uint)bVar1;
      if (bVar1 < 2) {
        uVar2 = 1;
      }
      uVar6 = (ulong)uVar2;
      lVar4 = 1;
      plVar5 = (long *)param_1[2];
      do {
        uVar6 = uVar6 - 1;
        lVar4 = *plVar5 * lVar4;
        iVar3 = (int)lVar4;
        plVar5 = plVar5 + 2;
      } while (uVar6 != 0);
    }
  }
  return *(int *)(*param_1 + 0x104) * iVar3;
}



// ==========================================================================================
// Function: il2cpp_array_new
// Address: 00de3e48
// ==========================================================================================

void il2cpp_array_new(undefined8 param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00dfca98(param_1,1);
  FUN_00e11234(uVar1,param_2);
  return;
}



// ==========================================================================================
// Function: il2cpp_array_new_specific
// Address: 00de3e4c
// ==========================================================================================

long * il2cpp_array_new_specific(long param_1,ulong param_2)

{
  long lVar1;
  char cVar2;
  bool bVar3;
  undefined *puVar4;
  ulong uVar5;
  long *plVar6;
  undefined8 uVar7;
  long lVar8;
  
  FUN_00dfcccc();
  if (param_2 >> 0x1f != 0) {
    FUN_00e11364();
    uVar7 = FUN_00e29cb8("Arithmetic operation resulted in an overflow.");
                    /* WARNING: Subroutine does not return */
    FUN_00e28a74(uVar7,0);
  }
  uVar5 = il2cpp_array_element_size(param_1);
  lVar8 = (uVar5 & 0xffffffff) * param_2;
  lVar1 = lVar8 + 0x20;
  if ((*(byte *)(param_1 + 0x135) >> 5 & 1) == 0) {
    plVar6 = (long *)FUN_00e3eccc();
    *plVar6 = param_1;
    plVar6[1] = 0;
    puVar4 = PTR_DAT_01ff5430;
    do {
      cVar2 = '\x01';
      bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
      if (bVar3) {
        *(long *)puVar4 = *(long *)puVar4 + 1;
        cVar2 = ExclusiveMonitorsStatus();
      }
    } while (cVar2 != '\0');
    plVar6[2] = 0;
    memset(plVar6 + 2,0,lVar8 + 0x10);
  }
  else if ((*(int *)(*(long *)(param_1 + 0x40) + 0x28) < 0) &&
          ((*(ulong *)(*(long *)(param_1 + 0x40) + 8) & 3) == 1)) {
    plVar6 = (long *)FUN_00e44f44(lVar1,param_1);
  }
  else if (*(long *)(param_1 + 8) == 0) {
    plVar6 = (long *)FUN_00e3eaec(lVar1);
    *plVar6 = param_1;
    puVar4 = PTR_DAT_01ff5430;
    do {
      cVar2 = '\x01';
      bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
      if (bVar3) {
        *(long *)puVar4 = *(long *)puVar4 + 1;
        cVar2 = ExclusiveMonitorsStatus();
      }
    } while (cVar2 != '\0');
  }
  else {
    plVar6 = (long *)FUN_00e39958(lVar1,param_1);
    puVar4 = PTR_DAT_01ff5430;
    do {
      cVar2 = '\x01';
      bVar3 = (bool)ExclusiveMonitorPass(puVar4,0x10);
      if (bVar3) {
        *(long *)puVar4 = *(long *)puVar4 + 1;
        cVar2 = ExclusiveMonitorsStatus();
      }
    } while (cVar2 != '\0');
  }
  puVar4 = PTR_DAT_01ff5438;
  plVar6[3] = param_2;
  if ((char)*puVar4 < '\0') {
    FUN_00e2ae40(plVar6,param_1);
  }
  return plVar6;
}



// ==========================================================================================
// Function: il2cpp_array_new_full
// Address: 00de3e50
// ==========================================================================================

long * il2cpp_array_new_full(long param_1,ulong *param_2,long *param_3)

{
  long lVar1;
  byte bVar2;
  char cVar3;
  bool bVar4;
  undefined *puVar5;
  int iVar6;
  long *plVar7;
  long *__s;
  uint uVar8;
  ulong uVar9;
  ulong *puVar10;
  undefined4 *puVar11;
  long *plVar12;
  long lVar13;
  ulong uVar14;
  undefined auVar15 [16];
  
  FUN_00dfcccc();
  iVar6 = il2cpp_array_element_size(param_1);
  uVar9 = (ulong)*(byte *)(param_1 + 0x132);
  if (uVar9 == 1) {
    if ((*(char *)(param_1 + 0x2a) == '\x1d') || ((param_3 != (long *)0x0 && (*param_3 == 0)))) {
      uVar14 = *param_2;
      if (uVar14 >> 0x1f != 0) {
LAB_00e1115c:
        auVar15 = FUN_00e11364();
        lVar13 = auVar15._8_8_;
        plVar12 = auVar15._0_8_;
        *plVar12 = 0;
        plVar12[1] = 0;
        plVar12[2] = 0;
        plVar7 = plVar12;
        if (lVar13 != 0) {
          FUN_00de9088();
          __s = (long *)plVar12[1];
          plVar7 = __s;
          if (lVar13 << 3 != 0) {
            plVar7 = __s + lVar13;
            memset(__s,0,lVar13 << 3);
          }
          plVar12[1] = (long)plVar7;
        }
        return plVar7;
      }
      lVar13 = 0;
      goto LAB_00e1100c;
    }
    lVar13 = 0x10;
  }
  else {
    lVar13 = uVar9 << 4;
    if (*(byte *)(param_1 + 0x132) == 0) {
      uVar14 = 1;
      goto LAB_00e1100c;
    }
  }
  uVar14 = 1;
  puVar10 = param_2;
  do {
    if (*puVar10 >> 0x1f != 0) goto LAB_00e1115c;
    uVar14 = *puVar10 * uVar14;
    uVar9 = uVar9 - 1;
    puVar10 = puVar10 + 1;
  } while (uVar9 != 0);
LAB_00e1100c:
  lVar1 = uVar14 * (long)iVar6 + 0x20;
  if (lVar13 != 0) {
    lVar1 = (uVar14 * (long)iVar6 + 0x27 & 0xfffffffffffffff8) + lVar13;
  }
  if ((*(byte *)(param_1 + 0x135) >> 5 & 1) == 0) {
    plVar7 = (long *)FUN_00e3eccc(lVar1);
    *plVar7 = param_1;
    plVar7[1] = 0;
    puVar5 = PTR_DAT_01ff5430;
    do {
      cVar3 = '\x01';
      bVar4 = (bool)ExclusiveMonitorPass(puVar5,0x10);
      if (bVar4) {
        *(long *)puVar5 = *(long *)puVar5 + 1;
        cVar3 = ExclusiveMonitorsStatus();
      }
    } while (cVar3 != '\0');
    memset(plVar7 + 2,0,lVar1 - 0x10);
  }
  else if (*(long *)(param_1 + 8) == 0) {
    plVar7 = (long *)FUN_00e3eaec(lVar1);
    *plVar7 = param_1;
    puVar5 = PTR_DAT_01ff5430;
    do {
      cVar3 = '\x01';
      bVar4 = (bool)ExclusiveMonitorPass(puVar5,0x10);
      if (bVar4) {
        *(long *)puVar5 = *(long *)puVar5 + 1;
        cVar3 = ExclusiveMonitorsStatus();
      }
    } while (cVar3 != '\0');
  }
  else {
    plVar7 = (long *)FUN_00e39958(lVar1,param_1);
    puVar5 = PTR_DAT_01ff5430;
    do {
      cVar3 = '\x01';
      bVar4 = (bool)ExclusiveMonitorPass(puVar5,0x10);
      if (bVar4) {
        *(long *)puVar5 = *(long *)puVar5 + 1;
        cVar3 = ExclusiveMonitorsStatus();
      }
    } while (cVar3 != '\0');
  }
  plVar7[3] = uVar14;
  if (lVar13 != 0) {
    plVar7[2] = (long)plVar7 + (lVar1 - lVar13);
    bVar2 = *(byte *)(param_1 + 0x132);
    if (bVar2 != 0) {
      uVar8 = (uint)bVar2;
      if (bVar2 < 2) {
        uVar8 = 1;
      }
      uVar9 = (ulong)uVar8;
      puVar11 = (undefined4 *)((long)plVar7 + (lVar1 - lVar13) + 8);
      plVar12 = param_3;
      do {
        *(ulong *)(puVar11 + -2) = *param_2;
        if (param_3 != (long *)0x0) {
          *puVar11 = (int)*plVar12;
        }
        puVar11 = puVar11 + 4;
        plVar12 = plVar12 + 1;
        uVar9 = uVar9 - 1;
        param_2 = param_2 + 1;
      } while (uVar9 != 0);
    }
  }
  if ((char)*PTR_DAT_01ff5438 < '\0') {
    FUN_00e2ae40(plVar7,param_1);
  }
  return plVar7;
}



// ==========================================================================================
// Function: il2cpp_bounded_array_class_get
// Address: 00de3e54
// ==========================================================================================

void il2cpp_bounded_array_class_get(undefined8 param_1,undefined8 param_2,uint param_3)

{
  FUN_00dfca7c(param_1,param_2,param_3 & 1);
  return;
}



// ==========================================================================================
// Function: il2cpp_array_element_size
// Address: 00de3e5c
// ==========================================================================================

undefined4 il2cpp_array_element_size(long param_1)

{
  return *(undefined4 *)(param_1 + 0x104);
}



// ==========================================================================================
// Function: il2cpp_assembly_get_image
// Address: 00de3e60
// ==========================================================================================

undefined8 il2cpp_assembly_get_image(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_class_enum_basetype
// Address: 00de3e64
// ==========================================================================================

long il2cpp_class_enum_basetype(long param_1)

{
  long lVar1;
  
  lVar1 = 0;
  if (*(long *)(param_1 + 0x40) != param_1) {
    lVar1 = *(long *)(param_1 + 0x40) + 0x20;
  }
  return lVar1;
}



// ==========================================================================================
// Function: il2cpp_class_from_system_type
// Address: 00de3e68
// ==========================================================================================

undefined8 il2cpp_class_from_system_type(long param_1)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00dfc824(*(undefined8 *)(param_1 + 0x10),1);
  FUN_00dfcccc();
  return uVar1;
}



// ==========================================================================================
// Function: il2cpp_class_is_inited
// Address: 00de3e6c
// ==========================================================================================

byte il2cpp_class_is_inited(long param_1)

{
  return *(byte *)(param_1 + 0x135) >> 1 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_is_generic
// Address: 00de3e78
// ==========================================================================================

byte il2cpp_class_is_generic(long param_1)

{
  return *(byte *)(param_1 + 0x135) >> 4 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_is_inflated
// Address: 00de3e7c
// ==========================================================================================

bool il2cpp_class_is_inflated(long param_1)

{
  return *(long *)(param_1 + 0x60) != 0;
}



// ==========================================================================================
// Function: il2cpp_class_is_assignable_from
// Address: 00de3e80
// ==========================================================================================

bool il2cpp_class_is_assignable_from(long param_1,long param_2)

{
  undefined *puVar1;
  bool bVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  long lVar6;
  long *plVar7;
  long lVar8;
  
  puVar1 = PTR_DAT_01ff5418;
  do {
    bVar2 = param_1 == param_2;
    if (bVar2) {
      return true;
    }
    while( true ) {
      FUN_00dfcccc(param_1);
      FUN_00dfcccc(param_2);
      if ((((*(byte *)(param_1 + 0x118) >> 5 & 1) != 0) || (*(char *)(param_1 + 0x2a) == '\x13')) ||
         (*(char *)(param_1 + 0x2a) == '\x1e')) {
        if (*(long *)(param_1 + 0x60) == 0) {
          if (param_2 == 0) {
            return false;
          }
          do {
            if ((ulong)*(ushort *)(param_2 + 300) != 0) {
              uVar4 = 0;
              do {
                if (*(long *)(*(long *)(param_2 + 0xa8) + uVar4 * 8) == param_1) {
                  return true;
                }
                uVar4 = uVar4 + 1;
              } while (uVar4 < *(ushort *)(param_2 + 300));
            }
            if ((ulong)*(ushort *)(param_2 + 0x12e) != 0) {
              plVar7 = *(long **)(param_2 + 0xb0);
              uVar4 = 0;
              do {
                if (*plVar7 == param_1) {
                  return true;
                }
                uVar4 = uVar4 + 1;
                plVar7 = plVar7 + 2;
              } while (uVar4 < *(ushort *)(param_2 + 0x12e));
            }
            param_2 = *(long *)(param_2 + 0x58);
          } while (param_2 != 0);
          return false;
        }
        lVar8 = param_2;
        if (param_2 == 0) {
          return false;
        }
        do {
          if ((lVar8 == param_1) || (uVar4 = FUN_00e01d10(param_1,lVar8,param_2), (uVar4 & 1) != 0))
          {
            return true;
          }
          if (*(short *)(lVar8 + 300) != 0) {
            uVar4 = 0;
            do {
              lVar5 = *(long *)(*(long *)(lVar8 + 0xa8) + uVar4 * 8);
              if (lVar5 == param_1) {
                return true;
              }
              uVar3 = FUN_00e01d10(param_1,lVar5,param_2);
              if ((uVar3 & 1) != 0) {
                return true;
              }
              uVar4 = uVar4 + 1;
            } while (uVar4 < *(ushort *)(lVar8 + 300));
          }
          if (*(short *)(lVar8 + 0x12e) != 0) {
            lVar5 = 0;
            uVar4 = 0;
            do {
              lVar6 = *(long *)(*(long *)(lVar8 + 0xb0) + lVar5);
              if (lVar6 == param_1) {
                return true;
              }
              uVar3 = FUN_00e01d10(param_1,lVar6,param_2);
              if ((uVar3 & 1) != 0) {
                return true;
              }
              uVar4 = uVar4 + 1;
              lVar5 = lVar5 + 0x10;
            } while (uVar4 < *(ushort *)(lVar8 + 0x12e));
          }
          plVar7 = (long *)(lVar8 + 0x58);
          lVar8 = *plVar7;
          if (*plVar7 == 0) {
            return false;
          }
        } while( true );
      }
      if (*(char *)(param_1 + 0x132) != '\0') break;
      if (*(long *)(puVar1 + 0x10) == param_1) {
        return true;
      }
      if (*(long *)(param_1 + 0x60) == 0) {
LAB_00dfd91c:
        if (*(byte *)(param_2 + 0x130) < *(byte *)(param_1 + 0x130)) {
          return false;
        }
        return *(long *)(*(long *)(param_2 + 200) + (ulong)*(byte *)(param_1 + 0x130) * 8 + -8) ==
               param_1;
      }
      if ((*(byte *)(param_1 + 0x135) >> 3 & 1) == 0) {
        if ((*(long *)(param_1 + 0x58) == *(long *)(puVar1 + 0xb0)) &&
           (uVar4 = FUN_00e01d10(param_1,param_2,param_2), (uVar4 & 1) != 0)) {
          return true;
        }
        goto LAB_00dfd91c;
      }
      param_1 = *(long *)(param_1 + 0x40);
      if (param_1 == param_2) {
        return true;
      }
    }
    if (*(char *)(param_2 + 0x132) != *(char *)(param_1 + 0x132)) {
      return bVar2;
    }
    param_2 = *(long *)(param_2 + 0x48);
    param_1 = *(long *)(param_1 + 0x48);
    if (*(int *)(param_2 + 0x28) < 0) {
      return param_1 == param_2;
    }
  } while( true );
}



// ==========================================================================================
// Function: il2cpp_class_is_subclass_of
// Address: 00de3e84
// ==========================================================================================

void il2cpp_class_is_subclass_of(undefined8 param_1,undefined8 param_2,uint param_3)

{
  FUN_00dfd9e4(param_1,param_2,param_3 & 1);
  return;
}



// ==========================================================================================
// Function: il2cpp_class_has_parent
// Address: 00de3e8c
// ==========================================================================================

bool il2cpp_class_has_parent(long param_1,long param_2)

{
  bool bVar1;
  
  FUN_00dfd6cc();
  FUN_00dfd6cc(param_2);
  if (*(byte *)(param_1 + 0x130) < *(byte *)(param_2 + 0x130)) {
    bVar1 = false;
  }
  else {
    bVar1 = *(long *)(*(long *)(param_1 + 200) + (ulong)*(byte *)(param_2 + 0x130) * 8 + -8) ==
            param_2;
  }
  return bVar1;
}



// ==========================================================================================
// Function: il2cpp_class_from_il2cpp_type
// Address: 00de3e90
// ==========================================================================================

void il2cpp_class_from_il2cpp_type(undefined8 param_1)

{
  FUN_00dfc824(param_1,1);
  return;
}



// ==========================================================================================
// Function: il2cpp_class_from_name
// Address: 00de3e98
// ==========================================================================================

undefined8 il2cpp_class_from_name(long param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  void *pvVar5;
  undefined8 uVar6;
  uint uVar7;
  long *plVar8;
  undefined4 auStack_98 [2];
  undefined8 uStack_90;
  undefined8 uStack_88;
  long lStack_80;
  long lStack_78;
  long lStack_70;
  long lStack_68;
  long lStack_60;
  long lStack_58;
  long lStack_50;
  long lStack_48;
  undefined8 uStack_40;
  undefined auStack_38 [8];
  
  plVar8 = (long *)(param_1 + 0x30);
  lVar4 = *plVar8;
  if (lVar4 == 0) {
    FUN_00da6960(&lStack_80,&DAT_02107c60);
    if (*plVar8 == 0) {
      pvVar5 = operator_new(0x70);
      FUN_00df0a9c(pvVar5,0,auStack_98,auStack_38);
      *(void **)(param_1 + 0x30) = pvVar5;
      if (*(int *)(param_1 + 0x18) != 0) {
        uVar7 = 0;
        do {
          uVar6 = thunk_FUN_00dcf4f4(param_1,uVar7);
          FUN_00debac4(param_1,uVar6);
          uVar7 = uVar7 + 1;
        } while (uVar7 < *(uint *)(param_1 + 0x18));
      }
      if (*(int *)(param_1 + 0x1c) != 0) {
        uVar7 = 0;
        do {
          uVar6 = thunk_FUN_00dcf598(param_1,uVar7);
          FUN_00debac4(param_1,uVar6);
          uVar7 = uVar7 + 1;
        } while (uVar7 < *(uint *)(param_1 + 0x1c));
      }
    }
    FUN_00da71f4(&lStack_80);
    lVar4 = *plVar8;
  }
  auStack_98[0] = 0;
  uStack_90 = param_2;
  uStack_88 = param_3;
  FUN_00df0cc8(&lStack_80,lVar4,auStack_98);
  lVar3 = lStack_60;
  lVar2 = lStack_68;
  lVar1 = lStack_70;
  lVar4 = lStack_78;
  lStack_80 = *plVar8;
  lStack_78 = *(long *)(lStack_80 + 0x48);
  lStack_70 = *(long *)(lStack_80 + 0x50);
  uStack_40 = 0;
  lStack_60 = 0;
  lStack_68 = lStack_70;
  lStack_58 = lStack_78;
  lStack_50 = lStack_70;
  lStack_48 = lStack_70;
  FUN_00df0a1c(&lStack_80);
  if ((((lVar4 == lStack_78) && (lVar1 == lStack_70)) && (lVar2 == lStack_68)) &&
     ((lVar2 == lVar1 || (lVar3 == lStack_60)))) {
    uVar6 = 0;
  }
  else {
    uVar6 = thunk_FUN_00dcf974(*(undefined8 *)(lVar3 + 0x18));
  }
  return uVar6;
}



// ==========================================================================================
// Function: il2cpp_class_get_element_class
// Address: 00de3e9c
// ==========================================================================================

undefined8 il2cpp_class_get_element_class(long param_1)

{
  return *(undefined8 *)(param_1 + 0x40);
}



// ==========================================================================================
// Function: il2cpp_class_get_events
// Address: 00de3ea0
// ==========================================================================================

ulong il2cpp_class_get_events(long param_1,ulong *param_2)

{
  ulong uVar1;
  
  if (param_2 != (ulong *)0x0) {
    if (*param_2 == 0) {
      FUN_00dfce20(param_1);
      if (*(short *)(param_1 + 0x126) != 0) {
        *param_2 = *(ulong *)(param_1 + 0x88);
        return *(ulong *)(param_1 + 0x88);
      }
    }
    else {
      uVar1 = *param_2 + 0x38;
      if (uVar1 < *(long *)(param_1 + 0x88) + (ulong)*(ushort *)(param_1 + 0x126) * 0x38) {
        *param_2 = uVar1;
        return uVar1;
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_fields
// Address: 00de3ea4
// ==========================================================================================

ulong il2cpp_class_get_fields(long param_1,ulong *param_2)

{
  ulong uVar1;
  
  if (param_2 != (ulong *)0x0) {
    if (*param_2 == 0) {
      FUN_00dfceec(param_1);
      if (*(short *)(param_1 + 0x124) != 0) {
        *param_2 = *(ulong *)(param_1 + 0x80);
        return *(ulong *)(param_1 + 0x80);
      }
    }
    else {
      uVar1 = *param_2 + 0x20;
      if (uVar1 < *(long *)(param_1 + 0x80) + (ulong)*(ushort *)(param_1 + 0x124) * 0x20) {
        *param_2 = uVar1;
        return uVar1;
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_nested_types
// Address: 00de3ea8
// ==========================================================================================

undefined8 il2cpp_class_get_nested_types(long param_1,ulong *param_2)

{
  undefined8 *puVar1;
  
  if ((param_2 != (ulong *)0x0) && (*(long *)(param_1 + 0x60) == 0)) {
    if (*param_2 == 0) {
      FUN_00dfd334(param_1);
      if (*(short *)(param_1 + 0x128) != 0) {
        *param_2 = *(ulong *)(param_1 + 0xa0);
        puVar1 = *(undefined8 **)(param_1 + 0xa0);
        goto LAB_00dfd32c;
      }
    }
    else {
      puVar1 = (undefined8 *)(*param_2 + 8);
      if (puVar1 < (undefined8 *)
                   (*(long *)(param_1 + 0xa0) + (ulong)*(ushort *)(param_1 + 0x128) * 8)) {
        *param_2 = (ulong)puVar1;
LAB_00dfd32c:
        return *puVar1;
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_interfaces
// Address: 00de3eac
// ==========================================================================================

undefined8 il2cpp_class_get_interfaces(long param_1,ulong *param_2)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  
  if (param_2 == (ulong *)0x0) {
LAB_00dfd060:
    uVar1 = 0;
  }
  else {
    if (*param_2 == 0) {
      FUN_00dfd070(param_1);
      if (*(short *)(param_1 + 300) == 0) goto LAB_00dfd060;
      *param_2 = *(ulong *)(param_1 + 0xa8);
      puVar2 = *(undefined8 **)(param_1 + 0xa8);
    }
    else {
      puVar2 = (undefined8 *)(*param_2 + 8);
      if ((undefined8 *)(*(long *)(param_1 + 0xa8) + (ulong)*(ushort *)(param_1 + 300) * 8) <=
          puVar2) goto LAB_00dfd060;
      *param_2 = (ulong)puVar2;
    }
    uVar1 = *puVar2;
  }
  return uVar1;
}



// ==========================================================================================
// Function: il2cpp_class_get_properties
// Address: 00de3eb0
// ==========================================================================================

ulong il2cpp_class_get_properties(long param_1,ulong *param_2)

{
  ulong uVar1;
  
  if (param_2 != (ulong *)0x0) {
    if (*param_2 == 0) {
      FUN_00dfd428(param_1);
      if (*(short *)(param_1 + 0x122) != 0) {
        *param_2 = *(ulong *)(param_1 + 0x90);
        return *(ulong *)(param_1 + 0x90);
      }
    }
    else {
      uVar1 = *param_2 + 0x28;
      if (uVar1 < *(long *)(param_1 + 0x90) + (ulong)*(ushort *)(param_1 + 0x122) * 0x28) {
        *param_2 = uVar1;
        return uVar1;
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_property_from_name
// Address: 00de3eb4
// ==========================================================================================

long il2cpp_class_get_property_from_name(long param_1,char *param_2)

{
  int iVar1;
  long lVar2;
  char *__s2;
  undefined8 uStack_28;
  
  if (param_1 != 0) {
    do {
      uStack_28 = 0;
      while (lVar2 = FUN_00dfd3b8(param_1,&uStack_28), lVar2 != 0) {
        __s2 = (char *)FUN_00dec5d4();
        iVar1 = strcmp(param_2,__s2);
        if (iVar1 == 0) {
          return lVar2;
        }
      }
      param_1 = *(long *)(param_1 + 0x58);
    } while (param_1 != 0);
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_field_from_name
// Address: 00de3eb8
// ==========================================================================================

long il2cpp_class_get_field_from_name(long param_1,char *param_2)

{
  int iVar1;
  long lVar2;
  char *__s2;
  undefined8 uStack_28;
  
  if (param_1 != 0) {
    do {
      uStack_28 = 0;
      while (lVar2 = FUN_00dfce80(param_1,&uStack_28), lVar2 != 0) {
        __s2 = (char *)FUN_00dcfa80();
        iVar1 = strcmp(param_2,__s2);
        if (iVar1 == 0) {
          return lVar2;
        }
      }
      param_1 = *(long *)(param_1 + 0x58);
    } while (param_1 != 0);
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_class_get_methods
// Address: 00de3ebc
// ==========================================================================================

undefined8 il2cpp_class_get_methods(long param_1,ulong *param_2)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  
  if (param_2 == (ulong *)0x0) {
LAB_00dfd128:
    uVar1 = 0;
  }
  else {
    if (*param_2 == 0) {
      FUN_00dfd138(param_1);
      if (*(short *)(param_1 + 0x120) == 0) goto LAB_00dfd128;
      *param_2 = *(ulong *)(param_1 + 0x98);
      puVar2 = *(undefined8 **)(param_1 + 0x98);
    }
    else {
      puVar2 = (undefined8 *)(*param_2 + 8);
      if ((undefined8 *)(*(long *)(param_1 + 0x98) + (ulong)*(ushort *)(param_1 + 0x120) * 8) <=
          puVar2) goto LAB_00dfd128;
      *param_2 = (ulong)puVar2;
    }
    uVar1 = *puVar2;
  }
  return uVar1;
}



// ==========================================================================================
// Function: il2cpp_class_get_method_from_name
// Address: 00de3ec0
// ==========================================================================================

void il2cpp_class_get_method_from_name(void)

{
  FUN_00dfd1ac();
  return;
}



// ==========================================================================================
// Function: il2cpp_class_get_name
// Address: 00de3ec4
// ==========================================================================================

undefined8 il2cpp_class_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_class_get_namespace
// Address: 00de3ec8
// ==========================================================================================

undefined8 il2cpp_class_get_namespace(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: il2cpp_class_get_parent
// Address: 00de3ecc
// ==========================================================================================

undefined8 il2cpp_class_get_parent(long param_1)

{
  return *(undefined8 *)(param_1 + 0x58);
}



// ==========================================================================================
// Function: il2cpp_class_get_declaring_type
// Address: 00de3ed0
// ==========================================================================================

undefined8 il2cpp_class_get_declaring_type(long param_1)

{
  return *(undefined8 *)(param_1 + 0x50);
}



// ==========================================================================================
// Function: il2cpp_class_instance_size
// Address: 00de3ed4
// ==========================================================================================

undefined4 il2cpp_class_instance_size(long param_1)

{
  return *(undefined4 *)(param_1 + 0xf8);
}



// ==========================================================================================
// Function: il2cpp_class_num_fields
// Address: 00de3ed8
// ==========================================================================================

undefined2 il2cpp_class_num_fields(long param_1)

{
  return *(undefined2 *)(param_1 + 0x124);
}



// ==========================================================================================
// Function: il2cpp_class_is_valuetype
// Address: 00de3edc
// ==========================================================================================

uint il2cpp_class_is_valuetype(long param_1)

{
  return *(uint *)(param_1 + 0x28) >> 0x1f;
}



// ==========================================================================================
// Function: il2cpp_class_is_blittable
// Address: 00de3ee8
// ==========================================================================================

byte il2cpp_class_is_blittable(long param_1)

{
  return *(byte *)(param_1 + 0x136) >> 3 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_value_size
// Address: 00de3ef4
// ==========================================================================================

int il2cpp_class_value_size(long param_1,uint *param_2)

{
  ushort *puVar1;
  void *pvVar2;
  ushort uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined8 uVar6;
  ulong uStack_48;
  undefined8 uStack_40;
  void *pvStack_38;
  
  puVar1 = (ushort *)(param_1 + 0x135);
  uVar3 = *puVar1;
  if ((uVar3 >> 7 & 1) == 0) {
    FUN_00dfceec(param_1);
    uVar3 = *puVar1;
  }
  if ((uVar3 >> 8 & 1) == 0) {
    uStack_48 = 0;
    uStack_40 = 0;
    pvStack_38 = (void *)0x0;
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_48,"Could not load type \'");
    if (**(char **)(param_1 + 0x18) != '\0') {
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_48,*(char **)(param_1 + 0x18));
      std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
      append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
             &uStack_48,":");
    }
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_48,*(char **)(param_1 + 0x10));
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    append((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
           &uStack_48,"\'");
    pvVar2 = (void *)((ulong)&uStack_48 | 1);
    if ((uStack_48 & 1) != 0) {
      pvVar2 = pvStack_38;
    }
    uVar6 = FUN_00e29c90(pvVar2);
    uVar4 = FUN_00e31e1c(uVar6,0);
    *(undefined4 *)(param_1 + 0xd8) = uVar4;
    DataMemoryBarrier(2,3);
    *puVar1 = *puVar1 & 0xffbc | (ushort)(*(int *)(param_1 + 0xd8) == 0) | 2;
    if ((uStack_48 & 1) != 0) {
      operator_delete(pvStack_38);
    }
    iVar5 = 1;
  }
  else {
    iVar5 = *(int *)(param_1 + 0xf8) + -0x10;
  }
  if (param_2 != (uint *)0x0) {
    *param_2 = (uint)*(byte *)(param_1 + 0x133);
  }
  return iVar5;
}



// ==========================================================================================
// Function: il2cpp_class_get_flags
// Address: 00de3ef8
// ==========================================================================================

undefined4 il2cpp_class_get_flags(long param_1)

{
  return *(undefined4 *)(param_1 + 0x118);
}



// ==========================================================================================
// Function: il2cpp_class_is_abstract
// Address: 00de3f00
// ==========================================================================================

byte il2cpp_class_is_abstract(long param_1)

{
  return *(byte *)(param_1 + 0x118) >> 7;
}



// ==========================================================================================
// Function: il2cpp_class_is_interface
// Address: 00de3f0c
// ==========================================================================================

bool il2cpp_class_is_interface(long param_1)

{
  if ((*(byte *)(param_1 + 0x118) >> 5 & 1) == 0) {
    return *(char *)(param_1 + 0x2a) == '\x13' || *(char *)(param_1 + 0x2a) == '\x1e';
  }
  return true;
}



// ==========================================================================================
// Function: il2cpp_class_array_element_size
// Address: 00de3f38
// ==========================================================================================

int il2cpp_class_array_element_size(long param_1)

{
  long lVar1;
  ulong uVar2;
  undefined8 *puVar3;
  
  puVar3 = (undefined8 *)(param_1 + 0x20);
  do {
    switch(*(undefined *)((long)puVar3 + 10)) {
    case 1:
      return 0;
    case 2:
    case 4:
    case 5:
      return 1;
    case 3:
    case 6:
    case 7:
      return 2;
    case 8:
    case 9:
    case 0xc:
      return 4;
    case 10:
    case 0xb:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x18:
    case 0x19:
    case 0x1c:
    case 0x1d:
    case 0x1e:
      return 8;
    default:
      return -1;
    case 0x11:
      uVar2 = FUN_00def4e8(puVar3);
      if ((uVar2 & 1) == 0) {
        return *(int *)(param_1 + 0xf8) + -0x10;
      }
      lVar1 = thunk_FUN_00e019cc(puVar3);
      param_1 = *(long *)(param_1 + 0x40);
      puVar3 = (undefined8 *)0x0;
      if (*(long *)(lVar1 + 0x40) != lVar1) {
        puVar3 = (undefined8 *)(*(long *)(lVar1 + 0x40) + 0x20);
      }
      break;
    case 0x15:
      lVar1 = FUN_00deb11c(*puVar3);
      puVar3 = (undefined8 *)(lVar1 + 0x20);
    }
  } while( true );
}



// ==========================================================================================
// Function: il2cpp_class_from_type
// Address: 00de3f3c
// ==========================================================================================

void il2cpp_class_from_type(undefined8 param_1)

{
  FUN_00dfc824(param_1,1);
  return;
}



// ==========================================================================================
// Function: il2cpp_class_get_type
// Address: 00de3f44
// ==========================================================================================

long il2cpp_class_get_type(long param_1)

{
  return param_1 + 0x20;
}



// ==========================================================================================
// Function: il2cpp_class_get_type_token
// Address: 00de3f4c
// ==========================================================================================

undefined4 il2cpp_class_get_type_token(long param_1)

{
  return *(undefined4 *)(param_1 + 0x11c);
}



// ==========================================================================================
// Function: il2cpp_class_has_attribute
// Address: 00de3f54
// ==========================================================================================

uint il2cpp_class_has_attribute(undefined8 *param_1,undefined8 param_2)

{
  uint uVar1;
  undefined auStack_30 [32];
  
  thunk_FUN_00dcfbf0(auStack_30,*param_1,*(undefined4 *)((long)param_1 + 0x11c));
  uVar1 = FUN_00e1494c(auStack_30,param_2);
  return uVar1 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_has_references
// Address: 00de3f58
// ==========================================================================================

ushort il2cpp_class_has_references(long param_1)

{
  ushort uVar1;
  
  uVar1 = *(ushort *)(param_1 + 0x135);
  if ((uVar1 >> 8 & 1) == 0) {
    FUN_00dfceec();
    uVar1 = *(ushort *)(param_1 + 0x135);
    if ((uVar1 >> 8 & 1) == 0) {
                    /* WARNING: Subroutine does not return */
      abort();
    }
  }
  return uVar1 >> 5 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_is_enum
// Address: 00de3f5c
// ==========================================================================================

byte il2cpp_class_is_enum(long param_1)

{
  return *(byte *)(param_1 + 0x135) >> 2 & 1;
}



// ==========================================================================================
// Function: il2cpp_class_get_image
// Address: 00de3f68
// ==========================================================================================

undefined8 il2cpp_class_get_image(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_class_get_assemblyname
// Address: 00de3f6c
// ==========================================================================================

undefined8 il2cpp_class_get_assemblyname(long *param_1)

{
  return *(undefined8 *)(*param_1 + 8);
}



// ==========================================================================================
// Function: il2cpp_class_get_rank
// Address: 00de3f70
// ==========================================================================================

undefined il2cpp_class_get_rank(long param_1)

{
  return *(undefined *)(param_1 + 0x132);
}



// ==========================================================================================
// Function: il2cpp_class_get_data_size
// Address: 00de3f78
// ==========================================================================================

undefined4 il2cpp_class_get_data_size(long param_1)

{
  return *(undefined4 *)(param_1 + 0x10c);
}



// ==========================================================================================
// Function: il2cpp_class_get_static_field_data
// Address: 00de3f80
// ==========================================================================================

undefined8 il2cpp_class_get_static_field_data(long param_1)

{
  return *(undefined8 *)(param_1 + 0xb8);
}



// ==========================================================================================
// Function: il2cpp_class_get_bitmap_size
// Address: 00de3f88
// ==========================================================================================

int il2cpp_class_get_bitmap_size(long param_1)

{
  return (*(uint *)(param_1 + 0xf8) >> 3 & 0x1ffffff8) + 8;
}



// ==========================================================================================
// Function: il2cpp_class_get_bitmap
// Address: 00de3f8c
// ==========================================================================================

void il2cpp_class_get_bitmap(undefined8 param_1,undefined8 param_2)

{
  undefined8 local_8;
  
  local_8 = 0;
  FUN_00dff8a8(param_1,param_2,&local_8);
  return;
}



// ==========================================================================================
// Function: il2cpp_stats_dump_to_file
// Address: 00de3fa4
// ==========================================================================================

undefined8 il2cpp_stats_dump_to_file(undefined8 param_1)

{
  undefined *puVar1;
  long lVar2;
  undefined *puVar3;
  basic_ostream<char,std::__ndk1::char_traits<char>> *pbVar4;
  undefined8 uVar5;
  long lVar6;
  undefined *local_1a0;
  undefined8 local_198;
  undefined *local_190;
  undefined auStack_188 [8];
  uint auStack_180 [40];
  undefined *local_e0 [17];
  undefined8 local_58;
  undefined4 local_50;
  long local_48;
  
  puVar3 = PTR_vtable_01ff54b8;
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  puVar1 = PTR_vtable_01ff54b8 + 0x40;
  local_1a0 = PTR_construction_vtable_01ff54c0 + 0x18;
  local_e0[0] = PTR_construction_vtable_01ff54c0 + 0x40;
  local_198 = 0;
  local_190 = puVar1;
                    /* try { // try from 00de3ffc to 00de4007 has its CatchHandler @ 00de4284 */
  std::__ndk1::ios_base::init((ios_base *)local_e0,auStack_188);
  local_1a0 = puVar3 + 0x18;
  local_e0[0] = puVar3 + 0x68;
  local_50 = 0xffffffff;
  local_58 = 0;
  local_190 = puVar1;
                    /* try { // try from 00de4028 to 00de402f has its CatchHandler @ 00de427c */
  FUN_00de5e34(auStack_188);
                    /* try { // try from 00de4030 to 00de420f has its CatchHandler @ 00de428c */
  FUN_00de42d4(&local_1a0,param_1,0x30);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"New object count: ",0x12);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b30);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Method count: ",0xe);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b40);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Class static data size: ",0x18);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b48);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Inflated method count: ",0x17);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b60);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Inflated type count: ",0x15);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b68);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Initialized class count: ",0x19);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b38);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Generic instance count: ",0x18);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b50);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  pbVar4 = (basic_ostream<char,std::__ndk1::char_traits<char>> *)
           FUN_00de6084(&local_190,"Generic class count: ",0x15);
  uVar5 = std::__ndk1::basic_ostream<char,std::__ndk1::char_traits<char>>::operator<<
                    (pbVar4,DAT_02107b58);
  FUN_00de6084(uVar5,&DAT_005d3812,1);
  lVar6 = FUN_00de53fc(auStack_188);
  if (lVar6 == 0) {
    std::__ndk1::ios_base::clear
              ((ios_base *)((long)&local_1a0 + *(long *)(local_1a0 + -0x18)),
               *(uint *)((long)auStack_180 + *(long *)(local_1a0 + -0x18)) | 4);
  }
  local_1a0 = puVar3 + 0x18;
  local_e0[0] = puVar3 + 0x68;
  local_190 = puVar3 + 0x40;
  FUN_00de5384(auStack_188);
  std::__ndk1::basic_iostream<char,std::__ndk1::char_traits<char>>::~basic_iostream
            ((basic_iostream<char,std::__ndk1::char_traits<char>> *)&local_1a0);
  std::__ndk1::basic_ios<char,std::__ndk1::char_traits<char>>::~basic_ios
            ((basic_ios<char,std::__ndk1::char_traits<char>> *)local_e0);
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return 1;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: il2cpp_stats_get_value
// Address: 00de4310
// ==========================================================================================

undefined8 il2cpp_stats_get_value(uint param_1)

{
  if (param_1 < 8) {
    return *(undefined8 *)(&PTR_DAT_01fb85c8)[(int)param_1];
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_domain_get
// Address: 00de4390
// ==========================================================================================

long il2cpp_domain_get(void)

{
  long lVar1;
  undefined8 uVar2;
  
  if (DAT_02107928 == 0) {
    DAT_02107928 = thunk_FUN_00e3ecd4(0x38,0);
    lVar1 = DAT_02107928 + 0x18;
    uVar2 = thunk_FUN_00e11c14(*(undefined8 *)(PTR_DAT_01ff5418 + 0x10));
    FUN_00e331f0(lVar1,uVar2);
  }
  return DAT_02107928;
}



// ==========================================================================================
// Function: il2cpp_domain_assembly_open
// Address: 00de4394
// ==========================================================================================

void il2cpp_domain_assembly_open(undefined8 param_1,undefined8 param_2)

{
  FUN_00e11594(param_2);
  return;
}



// ==========================================================================================
// Function: il2cpp_domain_get_assemblies
// Address: 00de439c
// ==========================================================================================

void il2cpp_domain_get_assemblies(undefined8 param_1,long *param_2)

{
  long *plVar1;
  
  plVar1 = (long *)FUN_00e11408();
  *param_2 = plVar1[1] - *plVar1 >> 3;
  return;
}



// ==========================================================================================
// Function: il2cpp_raise_exception
// Address: 00de43c0
// ==========================================================================================

void il2cpp_raise_exception(undefined8 param_1)

{
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(param_1,0);
}



// ==========================================================================================
// Function: il2cpp_exception_from_name_msg
// Address: 00de43cc
// ==========================================================================================

undefined8
il2cpp_exception_from_name_msg
          (undefined8 param_1,undefined8 param_2,undefined8 param_3,long param_4)

{
  void *pvVar1;
  undefined8 uVar2;
  uint uVar3;
  void *pvStack_58;
  ulong uStack_50;
  void *pvStack_48;
  void *pvStack_40;
  ulong uStack_38;
  void *pvStack_30;
  
  pvStack_40 = (void *)0x0;
  uStack_38 = 0;
  pvStack_30 = (void *)0x0;
  if (param_4 == 0) {
    uVar3 = 0;
  }
  else {
    FUN_00dc6950(&pvStack_58,param_4);
    if (((ulong)pvStack_40 & 1) != 0) {
      operator_delete(pvStack_30);
    }
    uStack_38 = uStack_50;
    pvStack_40 = pvStack_58;
    pvVar1 = pvStack_40;
    pvStack_40._0_1_ = (byte)pvStack_58;
    uVar3 = (uint)(byte)pvStack_40;
    pvStack_30 = pvStack_48;
    pvStack_40 = pvVar1;
  }
  pvStack_58 = (void *)((ulong)&pvStack_40 | 2);
  uStack_50 = (ulong)(uVar3 >> 1);
  if ((uVar3 & 1) != 0) {
    pvStack_58 = pvStack_30;
    uStack_50 = uStack_38;
  }
  uVar2 = FUN_00e293f8(param_1,param_2,param_3,&pvStack_58);
  if (((ulong)pvStack_40 & 1) != 0) {
    operator_delete(pvStack_30);
  }
  return uVar2;
}



// ==========================================================================================
// Function: il2cpp_get_exception_argument_null
// Address: 00de43d0
// ==========================================================================================

long il2cpp_get_exception_argument_null(long param_1)

{
  undefined8 uVar1;
  long lVar2;
  
  uVar1 = FUN_00deb760();
  lVar2 = FUN_00e294a4(uVar1,"System","ArgumentNullException",0);
  if (param_1 != 0) {
    uVar1 = FUN_00e0e65c(param_1);
    FUN_00e331f0(lVar2 + 0x90,uVar1);
  }
  return lVar2;
}



// ==========================================================================================
// Function: il2cpp_format_exception
// Address: 00de43d4
// ==========================================================================================

void il2cpp_format_exception(undefined8 param_1,char *param_2,int param_3)

{
  byte local_38 [16];
  char *local_28;
  
  FUN_00daf2b0(local_38);
  if ((local_38[0] & 1) == 0) {
    strncpy(param_2,(char *)((ulong)local_38 | 1),(long)param_3);
  }
  else {
    strncpy(param_2,local_28,(long)param_3);
    operator_delete(local_28);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_format_stack_trace
// Address: 00de443c
// ==========================================================================================

void il2cpp_format_stack_trace(undefined8 param_1,char *param_2,int param_3)

{
  byte local_38 [16];
  char *local_28;
  
  FUN_00daf704(local_38);
  if ((local_38[0] & 1) == 0) {
    strncpy(param_2,(char *)((ulong)local_38 | 1),(long)param_3);
  }
  else {
    strncpy(param_2,local_28,(long)param_3);
    operator_delete(local_28);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_unhandled_exception
// Address: 00de44a4
// ==========================================================================================

void il2cpp_unhandled_exception(long *param_1)

{
  long *plVar1;
  long lVar2;
  long lStack_28;
  
  FUN_00dce854();
  plVar1 = (long *)thunk_FUN_00dce854();
  lStack_28 = 0;
  lVar2 = FUN_00dfcf44(DAT_02107e40,"UnhandledException");
  if (*param_1 != DAT_02107e28) {
    FUN_00df3d5c(*(undefined8 *)(lVar2 + 8),&lStack_28,*plVar1 + (long)*(int *)(lVar2 + 0x18),1);
    if (lStack_28 != 0) {
      FUN_00df64f4(plVar1,lStack_28,param_1);
    }
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_native_stack_trace
// Address: 00de44a8
// ==========================================================================================

void il2cpp_native_stack_trace
               (long param_1,void **param_2,uint *param_3,undefined8 *param_4,undefined8 *param_5)

{
  uint uVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  ulong uVar4;
  undefined8 *puVar5;
  
  if ((param_1 == 0) || (*(long *)(param_1 + 0x80) == 0)) {
    *param_3 = 0;
  }
  else {
    uVar1 = FUN_00debcc4();
    *param_3 = uVar1;
    if (0 < (int)uVar1) {
      puVar2 = (undefined8 *)malloc((ulong)uVar1 << 3);
      *param_2 = puVar2;
      uVar4 = (ulong)*param_3;
      if (0 < (int)*param_3) {
        puVar5 = (undefined8 *)(*(long *)(param_1 + 0x80) + 0x20);
        do {
          uVar4 = uVar4 - 1;
          *puVar2 = *puVar5;
          puVar2 = puVar2 + 1;
          puVar5 = puVar5 + 1;
        } while (uVar4 != 0);
      }
      uVar3 = thunk_FUN_00df8134();
      *param_4 = uVar3;
      uVar3 = FUN_00df82a8();
      goto LAB_00de4540;
    }
  }
  uVar3 = 0;
  *param_2 = (void *)0x0;
  *param_4 = 0;
LAB_00de4540:
  *param_5 = uVar3;
  return;
}



// ==========================================================================================
// Function: il2cpp_field_get_name
// Address: 00de4554
// ==========================================================================================

undefined8 il2cpp_field_get_name(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_field_get_flags
// Address: 00de4558
// ==========================================================================================

undefined2 il2cpp_field_get_flags(long param_1)

{
  return *(undefined2 *)(*(long *)(param_1 + 8) + 8);
}



// ==========================================================================================
// Function: il2cpp_field_get_parent
// Address: 00de455c
// ==========================================================================================

undefined8 il2cpp_field_get_parent(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_field_get_offset
// Address: 00de4560
// ==========================================================================================

long il2cpp_field_get_offset(long param_1)

{
  return (long)*(int *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: il2cpp_field_get_type
// Address: 00de4564
// ==========================================================================================

undefined8 il2cpp_field_get_type(long param_1)

{
  return *(undefined8 *)(param_1 + 8);
}



// ==========================================================================================
// Function: il2cpp_field_get_value
// Address: 00de4568
// ==========================================================================================

void il2cpp_field_get_value(long param_1,long param_2,undefined8 param_3)

{
  FUN_00df3d5c(*(undefined8 *)(param_2 + 8),param_3,param_1 + *(int *)(param_2 + 0x18),1);
  return;
}



// ==========================================================================================
// Function: il2cpp_field_get_value_object
// Address: 00de456c
// ==========================================================================================

void il2cpp_field_get_value_object(long param_1,long param_2)

{
  uint uVar1;
  long lVar2;
  int iVar3;
  long lVar4;
  undefined8 uStack_40;
  long lStack_38;
  
  lVar2 = tpidr_el0;
  lStack_38 = *(long *)(lVar2 + 0x28);
  lVar4 = FUN_00dfc824(*(undefined8 *)(param_1 + 8),1);
  uVar1 = *(uint *)(*(long *)(param_1 + 8) + 8);
  if ((uVar1 >> 6 & 1) == 0) {
    if ((uVar1 >> 4 & 1) == 0) {
LAB_00df3f6c:
      iVar3 = *(int *)(param_1 + 0x18);
    }
    else {
      iVar3 = *(int *)(param_1 + 0x18);
      FUN_00df405c(*(undefined8 *)(param_1 + 0x10));
      if (iVar3 != -1) {
        param_2 = *(long *)(*(long *)(param_1 + 0x10) + 0xb8);
        goto LAB_00df3f6c;
      }
      iVar3 = FUN_00e01b08(param_1);
      param_2 = FUN_00dd0990(*(undefined4 *)(*(long *)(param_1 + 0x10) + 0x114));
    }
    param_2 = param_2 + iVar3;
  }
  else {
    if (-1 < *(int *)(lVar4 + 0x28)) {
      FUN_00df4014(param_1,&uStack_40);
      goto LAB_00df3fc8;
    }
    param_2 = (long)&uStack_40 - ((ulong)*(uint *)(lVar4 + 0xf8) - 1 & 0xfffffffffffffff0);
    FUN_00df4014(param_1,param_2);
  }
  uStack_40 = FUN_00e11868(lVar4,param_2);
LAB_00df3fc8:
  if (*(long *)(lVar2 + 0x28) == lStack_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uStack_40);
}



// ==========================================================================================
// Function: il2cpp_field_has_attribute
// Address: 00de4570
// ==========================================================================================

uint il2cpp_field_has_attribute(long param_1,undefined8 param_2)

{
  undefined4 uVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined auStack_40 [32];
  
  uVar3 = **(undefined8 **)(param_1 + 0x10);
  uVar1 = FUN_00df3f00();
  thunk_FUN_00dcfbf0(auStack_40,uVar3,uVar1);
  uVar2 = FUN_00e1494c(auStack_40,param_2);
  return uVar2 & 1;
}



// ==========================================================================================
// Function: il2cpp_field_set_value
// Address: 00de4574
// ==========================================================================================

void il2cpp_field_set_value(long param_1,long param_2,undefined8 param_3)

{
  FUN_00df3d5c(*(undefined8 *)(param_2 + 8),param_1 + *(int *)(param_2 + 0x18),param_3,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_field_set_value_object
// Address: 00de4578
// ==========================================================================================

void il2cpp_field_set_value_object(long param_1,long param_2,undefined8 param_3)

{
  FUN_00e331f0(param_1 + *(int *)(param_2 + 0x18),param_3);
  return;
}



// ==========================================================================================
// Function: il2cpp_field_static_get_value
// Address: 00de457c
// ==========================================================================================

void il2cpp_field_static_get_value(undefined8 param_1,undefined8 param_2)

{
  FUN_00df44a4(param_1,param_2,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_field_static_set_value
// Address: 00de4580
// ==========================================================================================

void il2cpp_field_static_set_value(long param_1,undefined8 param_2)

{
  int iVar1;
  long lVar2;
  
  FUN_00dfcccc(*(undefined8 *)(param_1 + 0x10));
  iVar1 = *(int *)(param_1 + 0x18);
  if (iVar1 == -1) {
    iVar1 = FUN_00e01b08(param_1);
    lVar2 = FUN_00dd0990(*(undefined4 *)(*(long *)(param_1 + 0x10) + 0x114));
  }
  else {
    lVar2 = *(long *)(*(long *)(param_1 + 0x10) + 0xb8);
  }
  FUN_00df3d5c(*(undefined8 *)(param_1 + 8),lVar2 + iVar1,param_2,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_field_is_literal
// Address: 00de4584
// ==========================================================================================

byte il2cpp_field_is_literal(long param_1)

{
  return *(byte *)(*(long *)(param_1 + 8) + 8) >> 6 & 1;
}



// ==========================================================================================
// Function: il2cpp_gc_collect
// Address: 00de4594
// ==========================================================================================

void il2cpp_gc_collect(void)

{
  FUN_00e3ddec(0,0);
  if (DAT_0231b800 != 0) {
    FUN_00e3e01c();
    return;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_collect_a_little
// Address: 00de4598
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool il2cpp_gc_collect_a_little(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  int iVar4;
  
  if (DAT_0231b2f8 != 0) {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
  }
  if (DAT_0231b718 == 0) {
    FUN_00e3ce1c(1);
  }
  iVar4 = DAT_0231b940;
  if (DAT_0231b2f8 != 0) {
    _DAT_0231b300 = 0;
  }
  if ((DAT_0231b30c != 0) && (DAT_0231b940 == 0)) {
    (*DAT_0231b7c8)();
  }
  return iVar4 != 0;
}



// ==========================================================================================
// Function: il2cpp_gc_start_incremental_collection
// Address: 00de459c
// ==========================================================================================

void il2cpp_gc_start_incremental_collection(void)

{
  if (DAT_0231b308 != 0) {
    DAT_0231b788 = 1;
    FUN_00e3c160();
    return;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_enable
// Address: 00de45a0
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void il2cpp_gc_enable(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 == 0) {
    DAT_0231b718 = DAT_0231b718 + -1;
  }
  else {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
    DAT_0231b718 = DAT_0231b718 + -1;
    if (DAT_0231b2f8 != 0) {
      _DAT_0231b300 = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_disable
// Address: 00de45a4
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void il2cpp_gc_disable(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 == 0) {
    DAT_0231b718 = DAT_0231b718 + 1;
  }
  else {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
    DAT_0231b718 = DAT_0231b718 + 1;
    if (DAT_0231b2f8 != 0) {
      _DAT_0231b300 = 0;
    }
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_is_disabled
// Address: 00de45a8
// ==========================================================================================

bool il2cpp_gc_is_disabled(void)

{
  int iVar1;
  
  iVar1 = FUN_00e44328();
  return iVar1 != 0;
}



// ==========================================================================================
// Function: il2cpp_gc_set_mode
// Address: 00de45ac
// ==========================================================================================

void il2cpp_gc_set_mode(int param_1)

{
  undefined auStack_18 [8];
  
  FUN_00da6960(auStack_18,&DAT_02108b80);
  if (param_1 == 0) {
    if (DAT_020ff0d4 != 0) {
      FUN_00e442b8();
    }
  }
  else if (param_1 == 2) {
    if (DAT_020ff0d4 == 0) {
      FUN_00e44248();
    }
    FUN_00e3c134(1);
  }
  else if (param_1 == 1) {
    if (DAT_020ff0d4 == 0) {
      FUN_00e44248();
    }
    FUN_00e3c134(0);
  }
  DAT_020ff0d4 = param_1;
  FUN_00da71f4(auStack_18);
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_is_incremental
// Address: 00de45b0
// ==========================================================================================

bool il2cpp_gc_is_incremental(void)

{
  int iVar1;
  
  iVar1 = FUN_00e3c078();
  return iVar1 != 0;
}



// ==========================================================================================
// Function: il2cpp_gc_get_max_time_slice_ns
// Address: 00de45b4
// ==========================================================================================

undefined8 il2cpp_gc_get_max_time_slice_ns(void)

{
  return DAT_020ff1b0;
}



// ==========================================================================================
// Function: il2cpp_gc_set_max_time_slice_ns
// Address: 00de45b8
// ==========================================================================================

void il2cpp_gc_set_max_time_slice_ns(undefined8 param_1)

{
  DAT_020ff1b0 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_get_used_size
// Address: 00de45bc
// ==========================================================================================

long il2cpp_gc_get_used_size(void)

{
  long lVar1;
  long lVar2;
  
  lVar1 = FUN_00e43c40();
  lVar2 = FUN_00e43c58();
  return lVar1 - lVar2;
}



// ==========================================================================================
// Function: il2cpp_gc_get_heap_size
// Address: 00de45c0
// ==========================================================================================

long il2cpp_gc_get_heap_size(void)

{
  return DAT_02108e00 - DAT_02108ea0;
}



// ==========================================================================================
// Function: il2cpp_gc_foreach_heap
// Address: 00de45c4
// ==========================================================================================

void il2cpp_gc_foreach_heap(undefined8 param_1,undefined8 param_2)

{
  undefined8 local_20;
  undefined8 local_18;
  
  local_20 = param_1;
  local_18 = param_2;
  thunk_FUN_00e44c80(&local_20,PTR_FUN_01ff54d0);
  return;
}



// ==========================================================================================
// Function: il2cpp_stop_gc_world
// Address: 00de45ec
// ==========================================================================================

void il2cpp_stop_gc_world(void)

{
  char cVar1;
  bool bVar2;
  char cVar3;
  
  if (DAT_0231b2f8 != 0) {
    do {
      cVar3 = DAT_0231b300;
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
      if (bVar2) {
        DAT_0231b300 = '\x01';
        cVar1 = ExclusiveMonitorsStatus();
      }
    } while (cVar1 != '\0');
    if (cVar3 != '\0') {
      FUN_00e39788();
    }
  }
  FUN_00e3d320();
  return;
}



// ==========================================================================================
// Function: il2cpp_start_gc_world
// Address: 00de45f0
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void il2cpp_start_gc_world(void)

{
  FUN_00e3d400();
  if (DAT_0231b2f8 != 0) {
    _DAT_0231b300 = 0;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_alloc_fixed
// Address: 00de45f4
// ==========================================================================================

void il2cpp_gc_alloc_fixed(undefined8 param_1)

{
  thunk_FUN_00e3ecd4(param_1,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_free_fixed
// Address: 00de45fc
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void il2cpp_gc_free_fixed(undefined8 *param_1)

{
  byte bVar1;
  char cVar2;
  bool bVar3;
  char cVar4;
  undefined *puVar5;
  long lVar6;
  long *plVar7;
  ulong uVar8;
  
  if (param_1 != (undefined8 *)0x0) {
    plVar7 = (long *)(&DAT_023172e0 + ((ulong)param_1 >> 0x16 & 0x7ff) * 8);
    do {
      lVar6 = *plVar7;
      if (lVar6 == DAT_02108ea8) break;
      plVar7 = (long *)(lVar6 + 0x2018);
    } while (*(ulong *)(lVar6 + 0x2010) != (ulong)param_1 >> 0x16);
    lVar6 = *(long *)(lVar6 + ((ulong)param_1 >> 0xc & 0x3ff) * 8);
    uVar8 = *(ulong *)(lVar6 + 0x20);
    bVar1 = *(byte *)(lVar6 + 0x18);
    if (uVar8 < 0x810) {
      if (DAT_0231b2f8 != 0) {
        do {
          cVar4 = DAT_0231b300;
          cVar2 = '\x01';
          bVar3 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
          if (bVar3) {
            _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
            cVar2 = ExclusiveMonitorsStatus();
          }
        } while (cVar2 != '\0');
        if (cVar4 != '\0') {
          FUN_00e39788();
        }
      }
      DAT_02108e58 = DAT_02108e58 + uVar8;
      if (bVar1 == 2) {
        DAT_0231b738 = DAT_0231b738 - uVar8;
      }
      if ((8 < uVar8) && (*(int *)(&DAT_020ff244 + (ulong)bVar1 * 0x20) != 0)) {
        memset(param_1 + 1,0,uVar8 - 8);
      }
      puVar5 = (&PTR_DAT_020ff228)[(ulong)bVar1 * 4];
      *param_1 = *(undefined8 *)(puVar5 + (uVar8 >> 4) * 8);
      *(undefined8 **)(puVar5 + (uVar8 >> 4) * 8) = param_1;
      if (DAT_0231b2f8 != 0) {
        _DAT_0231b300 = 0;
      }
    }
    else {
      if (DAT_0231b2f8 != 0) {
        do {
          cVar4 = DAT_0231b300;
          cVar2 = '\x01';
          bVar3 = (bool)ExclusiveMonitorPass(0x231b300,0x10);
          if (bVar3) {
            _DAT_0231b300 = CONCAT71(DAT_0231b300_1,1);
            cVar2 = ExclusiveMonitorsStatus();
          }
        } while (cVar2 != '\0');
        if (cVar4 != '\0') {
          FUN_00e39788((ulong)param_1 & 0xfffffffffffff000);
        }
      }
      DAT_02108e58 = DAT_02108e58 + uVar8;
      if (bVar1 == 2) {
        DAT_0231b738 = DAT_0231b738 - uVar8;
      }
      if (0x1fff < uVar8 + 0xfff) {
        DAT_02108e28 = DAT_02108e28 - (uVar8 + 0xfff & 0xfffffffffffff000);
      }
      FUN_00e3bdb0((ulong)param_1 & 0xfffffffffffff000);
      if (DAT_0231b2f8 != 0) {
        _DAT_0231b300 = 0;
      }
    }
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_gchandle_new
// Address: 00de4600
// ==========================================================================================

void il2cpp_gchandle_new(undefined8 param_1,uint param_2)

{
  FUN_00e31e1c(param_1,param_2 & 1);
  return;
}



// ==========================================================================================
// Function: il2cpp_gchandle_new_weakref
// Address: 00de4608
// ==========================================================================================

undefined4 il2cpp_gchandle_new_weakref(undefined8 param_1,uint param_2)

{
  undefined4 local_40 [4];
  byte local_30;
  void *local_20;
  
  FUN_00e32284(local_40,param_1,param_2 & 1);
  if ((local_30 & 1) != 0) {
    operator_delete(local_20);
  }
  return local_40[0];
}



// ==========================================================================================
// Function: il2cpp_gchandle_get_target
// Address: 00de4640
// ==========================================================================================

long il2cpp_gchandle_get_target(uint param_1)

{
  char cVar1;
  bool bVar2;
  uint uVar3;
  int iVar4;
  pthread_t pVar5;
  long lVar6;
  int iVar7;
  long lVar8;
  ulong uVar9;
  
  uVar3 = (param_1 & 7) - 1;
  uVar9 = (ulong)uVar3;
  if (uVar3 < 4) {
    uVar3 = param_1 >> 3;
    pVar5 = pthread_self();
    if (pVar5 == DAT_02108c10) {
      DAT_02108c18 = DAT_02108c18 + 1;
    }
    else {
      iVar7 = 0;
      do {
        iVar4 = DAT_02108bd0;
        if (DAT_02108bd0 == iVar7) {
          cVar1 = '\x01';
          bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar2) {
            cVar1 = ExclusiveMonitorsStatus();
            DAT_02108bd0 = iVar7 + 1;
          }
          if (cVar1 != '\0') goto LAB_00e323cc;
          bVar2 = true;
        }
        else {
          ClearExclusiveLocal();
LAB_00e323cc:
          bVar2 = false;
        }
      } while ((iVar4 != 2) && (iVar7 = iVar4, !bVar2));
      while (iVar4 != 0) {
        FUN_00e4d8f8(&DAT_02108bd0,2,0xffffffff);
        do {
          iVar4 = DAT_02108bd0;
          cVar1 = '\x01';
          bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar2) {
            DAT_02108bd0 = 2;
            cVar1 = ExclusiveMonitorsStatus();
          }
        } while (cVar1 != '\0');
      }
      DAT_02108c18 = 1;
      DAT_02108c10 = pVar5;
    }
    if ((uVar3 < *(uint *)(&DAT_020ff0e8 + uVar9 * 0x20)) &&
       ((*(uint *)(*(long *)(&DAT_020ff0d8 + uVar9 * 0x20) + (ulong)(param_1 >> 8) * 4) >>
         (ulong)(uVar3 & 0x1f) & 1) != 0)) {
      if ((byte)(&DAT_020ff0ec)[uVar9 * 0x20] < 2) {
        lVar6 = FUN_00e4433c(FUN_00e31cd8);
        lVar8 = 0;
        if (lVar6 != -1) {
          lVar8 = lVar6;
        }
      }
      else {
        lVar8 = *(long *)(*(long *)(&DAT_020ff0e0 + uVar9 * 0x20) + (ulong)uVar3 * 8);
      }
    }
    else {
      lVar8 = 0;
    }
    iVar7 = DAT_02108c18 + -1;
    if ((0 < DAT_02108c18) && (DAT_02108c18 = iVar7, iVar7 == 0)) {
      DAT_02108c10 = 0;
      DAT_02108c18 = 0;
      do {
        iVar7 = DAT_02108bd0;
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
        if (bVar2) {
          DAT_02108bd0 = 0;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
      if (iVar7 == 2) {
        FUN_00e4d950(&DAT_02108bd0,1,0);
      }
    }
  }
  else {
    lVar8 = 0;
  }
  return lVar8;
}



// ==========================================================================================
// Function: il2cpp_gchandle_foreach_get_target
// Address: 00de4644
// ==========================================================================================

void il2cpp_gchandle_foreach_get_target(undefined8 param_1,undefined8 param_2)

{
  undefined8 local_20;
  undefined8 local_18;
  
  local_20 = param_1;
  local_18 = param_2;
  FUN_00e328f8(PTR_FUN_01ff54d8,&local_20);
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_wbarrier_set_field
// Address: 00de466c
// ==========================================================================================

void il2cpp_gc_wbarrier_set_field(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  FUN_00e331f0(param_2,param_3);
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_has_strict_wbarriers
// Address: 00de4678
// ==========================================================================================

undefined8 il2cpp_gc_has_strict_wbarriers(void)

{
  return 0;
}



// ==========================================================================================
// Function: il2cpp_gc_set_external_allocation_tracker
// Address: 00de4680
// ==========================================================================================

void il2cpp_gc_set_external_allocation_tracker(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_gc_set_external_wbarrier_tracker
// Address: 00de4684
// ==========================================================================================

void il2cpp_gc_set_external_wbarrier_tracker(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_gchandle_free
// Address: 00de4688
// ==========================================================================================

void il2cpp_gchandle_free(uint param_1)

{
  long lVar1;
  long *plVar2;
  uint uVar3;
  uint uVar4;
  char cVar5;
  bool bVar6;
  uint uVar7;
  ulong uVar8;
  int iVar9;
  pthread_t pVar10;
  long lVar11;
  int iVar12;
  
  uVar7 = (param_1 & 7) - 1;
  if (uVar7 < 4) {
    uVar4 = param_1 >> 3;
    pVar10 = pthread_self();
    if (pVar10 == DAT_02108c10) {
      DAT_02108c18 = DAT_02108c18 + 1;
    }
    else {
      iVar12 = 0;
      do {
        iVar9 = DAT_02108bd0;
        if (DAT_02108bd0 == iVar12) {
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar6) {
            cVar5 = ExclusiveMonitorsStatus();
            DAT_02108bd0 = iVar12 + 1;
          }
          if (cVar5 != '\0') goto LAB_00e32570;
          bVar6 = true;
        }
        else {
          ClearExclusiveLocal();
LAB_00e32570:
          bVar6 = false;
        }
      } while ((iVar9 != 2) && (iVar12 = iVar9, !bVar6));
      while (iVar9 != 0) {
        FUN_00e4d8f8(&DAT_02108bd0,2,0xffffffff);
        do {
          iVar9 = DAT_02108bd0;
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
          if (bVar6) {
            DAT_02108bd0 = 2;
            cVar5 = ExclusiveMonitorsStatus();
          }
        } while (cVar5 != '\0');
      }
      DAT_02108c18 = 1;
      DAT_02108c10 = pVar10;
    }
    lVar11 = (ulong)uVar7 * 0x20;
    if (uVar4 < *(uint *)(&DAT_020ff0e8 + lVar11)) {
      uVar8 = (ulong)(param_1 >> 8);
      uVar3 = 1 << (ulong)(uVar4 & 0x1f);
      if ((*(uint *)(*(long *)(&DAT_020ff0d8 + lVar11) + uVar8 * 4) & uVar3) != 0) {
        lVar1 = (ulong)uVar7 * 0x20;
        plVar2 = (long *)(*(long *)(&DAT_020ff0e0 + lVar1) + (ulong)uVar4 * 8);
        if ((byte)(&DAT_020ff0ec)[lVar1] < 2) {
          if (*plVar2 != 0) {
            FUN_00e31c9c();
          }
        }
        else {
          *plVar2 = 0;
        }
        lVar11 = *(long *)(&DAT_020ff0d8 + lVar11);
        *(uint *)(lVar11 + uVar8 * 4) = *(uint *)(lVar11 + uVar8 * 4) & (uVar3 ^ 0xffffffff);
      }
    }
    iVar12 = DAT_02108c18 + -1;
    if ((0 < DAT_02108c18) && (DAT_02108c18 = iVar12, iVar12 == 0)) {
      DAT_02108c10 = 0;
      DAT_02108c18 = 0;
      do {
        iVar12 = DAT_02108bd0;
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108bd0,0x10);
        if (bVar6) {
          DAT_02108bd0 = 0;
          cVar5 = ExclusiveMonitorsStatus();
        }
      } while (cVar5 != '\0');
      if (iVar12 == 2) {
        FUN_00e4d950(&DAT_02108bd0,1,0);
        return;
      }
    }
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_object_header_size
// Address: 00de468c
// ==========================================================================================

undefined8 il2cpp_object_header_size(void)

{
  return 0x10;
}



// ==========================================================================================
// Function: il2cpp_array_object_header_size
// Address: 00de4694
// ==========================================================================================

undefined8 il2cpp_array_object_header_size(void)

{
  return 0x20;
}



// ==========================================================================================
// Function: il2cpp_offset_of_array_length_in_array_object_header
// Address: 00de469c
// ==========================================================================================

undefined8 il2cpp_offset_of_array_length_in_array_object_header(void)

{
  return 0x18;
}



// ==========================================================================================
// Function: il2cpp_offset_of_array_bounds_in_array_object_header
// Address: 00de46a4
// ==========================================================================================

undefined8 il2cpp_offset_of_array_bounds_in_array_object_header(void)

{
  return 0x10;
}



// ==========================================================================================
// Function: il2cpp_allocation_granularity
// Address: 00de46ac
// ==========================================================================================

undefined8 il2cpp_allocation_granularity(void)

{
  return 0x10;
}



// ==========================================================================================
// Function: il2cpp_unity_liveness_allocate_struct
// Address: 00de46b4
// ==========================================================================================

void * il2cpp_unity_liveness_allocate_struct(undefined8 param_1)

{
  void *pvVar1;
  
  FUN_00dfd6cc();
  pvVar1 = operator_new(0x38);
  FUN_00e2a2ac(pvVar1,param_1);
  return pvVar1;
}



// ==========================================================================================
// Function: il2cpp_unity_liveness_calculation_from_root
// Address: 00de46b8
// ==========================================================================================

void il2cpp_unity_liveness_calculation_from_root(undefined8 param_1,long param_2)

{
  long **pplVar1;
  long *plVar2;
  
  pplVar1 = *(long ***)(param_2 + 0x10);
  for (plVar2 = *pplVar1; plVar2 != (long *)0x0; plVar2 = (long *)plVar2[2]) {
    *plVar2 = (long)(plVar2 + 3);
  }
  FUN_00e2a194(pplVar1,param_1,param_2);
  FUN_00e2a404(param_2);
  FUN_00e2a4d0(param_2);
  return;
}



// ==========================================================================================
// Function: il2cpp_unity_liveness_calculation_from_statics
// Address: 00de46bc
// ==========================================================================================

void il2cpp_unity_liveness_calculation_from_statics(long param_1)

{
  int iVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  undefined8 uVar5;
  long *plVar6;
  ulong uVar7;
  long lVar8;
  long **pplVar9;
  long **pplVar10;
  long lStack_50;
  undefined8 uStack_48;
  
  plVar3 = (long *)FUN_00dff888();
  plVar2 = (long *)PTR_DAT_01ff5418;
  for (plVar6 = **(long ***)(param_1 + 0x10); PTR_DAT_01ff5418 = (undefined *)plVar2,
      plVar6 != (long *)0x0; plVar6 = (long *)plVar6[2]) {
    *plVar6 = (long)(plVar6 + 3);
    plVar2 = (long *)PTR_DAT_01ff5418;
  }
  uVar7 = plVar3[1];
  if ((uVar7 & 0x1fffffffffffffff) != 0) {
    pplVar9 = (long **)*plVar3;
    pplVar10 = pplVar9;
    do {
      plVar6 = *pplVar10;
      if (((plVar6 != (long *)0x0) && (*plVar6 != *plVar2)) &&
         ((*(byte *)((long)plVar6 + 0x136) & 1) != 0)) {
        uStack_48 = 0;
        lVar4 = FUN_00dfce80(plVar6,&uStack_48);
        while (lVar4 != 0) {
          uVar7 = FUN_00df4610(lVar4);
          if (((uVar7 & 1) != 0) && (uVar7 = FUN_00e2a8f0(lVar4), (uVar7 & 1) != 0)) {
            uVar7 = FUN_00def384(*(undefined8 *)(lVar4 + 8));
            if ((uVar7 & 1) == 0) {
              lStack_50 = 0;
              FUN_00df449c(lVar4,&lStack_50);
              if (lStack_50 != 0) {
                FUN_00e2a834(lStack_50,param_1);
              }
            }
            else {
              lVar8 = plVar6[0x17];
              iVar1 = *(int *)(lVar4 + 0x18);
              uVar7 = FUN_00def174(*(undefined8 *)(lVar4 + 8));
              if ((uVar7 & 1) == 0) {
                uVar5 = thunk_FUN_00e019cc(*(long **)(lVar4 + 8));
              }
              else {
                uVar5 = *(undefined8 *)(**(long **)(lVar4 + 8) + 0x18);
              }
              FUN_00e2a710(lVar8 + iVar1,1,uVar5,param_1);
            }
          }
          lVar4 = FUN_00dfce80(plVar6,&uStack_48);
        }
        pplVar9 = (long **)*plVar3;
        uVar7 = plVar3[1];
      }
      pplVar10 = pplVar10 + 1;
    } while (pplVar10 != pplVar9 + uVar7);
  }
  FUN_00e2a404(param_1);
  FUN_00e2a4d0(param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_unity_liveness_finalize
// Address: 00de46c0
// ==========================================================================================

void il2cpp_unity_liveness_finalize(long **param_1)

{
  long *plVar1;
  ulong *puVar2;
  long lVar3;
  long lVar4;
  
  plVar1 = *param_1;
  lVar3 = *plVar1;
  lVar4 = plVar1[2];
  *(long *)(lVar4 + 8) = lVar3;
  *(long *)(lVar4 + 0x10) = lVar3 + 0x18;
  while (puVar2 = (ulong *)FUN_00e2a204(plVar1), puVar2 != (ulong *)0x0) {
    *puVar2 = *puVar2 & 0xfffffffffffffffe;
    plVar1 = *param_1;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_unity_liveness_free_struct
// Address: 00de46c4
// ==========================================================================================

void il2cpp_unity_liveness_free_struct(void *param_1)

{
  if (param_1 != (void *)0x0) {
    FUN_00e2a398();
    operator_delete(param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_method_get_return_type
// Address: 00de46c8
// ==========================================================================================

undefined8 il2cpp_method_get_return_type(long param_1)

{
  return *(undefined8 *)(param_1 + 0x28);
}



// ==========================================================================================
// Function: il2cpp_method_get_from_reflection
// Address: 00de46cc
// ==========================================================================================

undefined8 il2cpp_method_get_from_reflection(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_method_get_object
// Address: 00de46d0
// ==========================================================================================

undefined8 il2cpp_method_get_object(long param_1,long param_2)

{
  int iVar1;
  ulong uVar2;
  long lVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  char *__s1;
  long lStack_40;
  long lStack_38;
  undefined8 uStack_28;
  
  if (param_2 == 0) {
    param_2 = *(long *)(param_1 + 0x20);
  }
  uStack_28 = 0;
  lStack_40 = param_1;
  lStack_38 = param_2;
  uVar2 = FUN_00e132c4(DAT_02108790,&lStack_40,&uStack_28);
  if ((uVar2 & 1) == 0) {
    __s1 = *(char **)(param_1 + 0x18);
    if ((*__s1 == '.') &&
       ((iVar1 = strcmp(__s1,".ctor"), iVar1 == 0 || (iVar1 = strcmp(__s1,".cctor"), iVar1 == 0))))
    {
      puVar5 = &DAT_02108798;
    }
    else {
      puVar5 = &DAT_021087a0;
    }
    lVar3 = FUN_00e11c14(*puVar5);
    *(long *)(lVar3 + 0x10) = param_1;
    uVar4 = FUN_00e12fb0(param_2 + 0x20);
    FUN_00e331f0(lVar3 + 0x20,uVar4);
    uStack_28 = FUN_00e133cc(DAT_02108790,&lStack_40,lVar3);
  }
  return uStack_28;
}



// ==========================================================================================
// Function: il2cpp_method_get_name
// Address: 00de46d4
// ==========================================================================================

undefined8 il2cpp_method_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: il2cpp_method_is_generic
// Address: 00de46d8
// ==========================================================================================

byte il2cpp_method_is_generic(long param_1)

{
  return *(byte *)(param_1 + 0x53) & 1;
}



// ==========================================================================================
// Function: il2cpp_method_is_inflated
// Address: 00de46dc
// ==========================================================================================

byte il2cpp_method_is_inflated(long param_1)

{
  return *(byte *)(param_1 + 0x53) >> 1 & 1;
}



// ==========================================================================================
// Function: il2cpp_method_is_instance
// Address: 00de46e0
// ==========================================================================================

bool il2cpp_method_is_instance(long param_1)

{
  return (*(byte *)(param_1 + 0x4c) & 0x10) == 0;
}



// ==========================================================================================
// Function: il2cpp_method_get_param_count
// Address: 00de46e4
// ==========================================================================================

undefined il2cpp_method_get_param_count(long param_1)

{
  return *(undefined *)(param_1 + 0x52);
}



// ==========================================================================================
// Function: il2cpp_method_get_param
// Address: 00de46e8
// ==========================================================================================

undefined8 il2cpp_method_get_param(long param_1,uint param_2)

{
  if (param_2 < *(byte *)(param_1 + 0x52)) {
    return *(undefined8 *)(*(long *)(param_1 + 0x30) + (ulong)param_2 * 8);
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_method_get_class
// Address: 00de46ec
// ==========================================================================================

undefined8 il2cpp_method_get_class(long param_1)

{
  return *(undefined8 *)(param_1 + 0x20);
}



// ==========================================================================================
// Function: il2cpp_method_has_attribute
// Address: 00de46f0
// ==========================================================================================

uint il2cpp_method_has_attribute(long param_1,undefined8 param_2)

{
  undefined4 uVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined auStack_40 [32];
  
  uVar3 = **(undefined8 **)(param_1 + 0x20);
  uVar1 = FUN_00dd1684();
  thunk_FUN_00dcfbf0(auStack_40,uVar3,uVar1);
  uVar2 = FUN_00e1494c(auStack_40,param_2);
  return uVar2 & 1;
}



// ==========================================================================================
// Function: il2cpp_method_get_declaring_type
// Address: 00de46f4
// ==========================================================================================

undefined8 il2cpp_method_get_declaring_type(long param_1)

{
  return *(undefined8 *)(param_1 + 0x20);
}



// ==========================================================================================
// Function: il2cpp_method_get_flags
// Address: 00de46f8
// ==========================================================================================

void il2cpp_method_get_flags(undefined8 param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  
  if (param_2 != (undefined4 *)0x0) {
    uVar1 = FUN_00dd1674(param_1);
    *param_2 = uVar1;
  }
  FUN_00dd167c(param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_method_get_token
// Address: 00de4728
// ==========================================================================================

undefined4 il2cpp_method_get_token(long param_1)

{
  return *(undefined4 *)(param_1 + 0x48);
}



// ==========================================================================================
// Function: il2cpp_method_get_param_name
// Address: 00de472c
// ==========================================================================================

undefined8 il2cpp_method_get_param_name(long param_1,uint param_2)

{
  undefined8 auStack_28 [3];
  
  if (param_2 < *(byte *)(param_1 + 0x52)) {
    if ((*(byte *)(param_1 + 0x53) >> 1 & 1) != 0) {
      param_1 = FUN_00e00adc();
    }
    if (*(long *)(param_1 + 0x38) != 0) {
      thunk_FUN_00dd0070(auStack_28,*(undefined8 *)(param_1 + 0x20),*(long *)(param_1 + 0x38),
                         param_2);
      return auStack_28[0];
    }
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_profiler_install
// Address: 00de4730
// ==========================================================================================

void il2cpp_profiler_install(undefined8 param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  
  puVar1 = (undefined8 *)calloc(1,0x58);
  *puVar1 = param_1;
  puVar1[2] = param_2;
  puVar2 = (undefined8 *)FUN_00da55e0(&DAT_02108950);
  *puVar2 = puVar1;
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_set_events
// Address: 00de4734
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void il2cpp_profiler_set_events(undefined4 param_1)

{
  long *plVar1;
  long lVar2;
  
  lVar2 = DAT_02108958;
  plVar1 = DAT_02108950;
  if (DAT_02108958 != 0) {
    *(undefined4 *)(DAT_02108950[DAT_02108958 + -1] + 8) = param_1;
  }
  _DAT_02108968 = 0;
  for (lVar2 = lVar2 << 3; lVar2 != 0; lVar2 = lVar2 + -8) {
    _DAT_02108968 = *(uint *)(*plVar1 + 8) | _DAT_02108968;
    plVar1 = plVar1 + 1;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_install_enter_leave
// Address: 00de4738
// ==========================================================================================

void il2cpp_profiler_install_enter_leave(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  
  if (DAT_02108958 != 0) {
    lVar1 = DAT_02108950 + DAT_02108958 * 8;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x18) = param_1;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x20) = param_2;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_install_allocation
// Address: 00de473c
// ==========================================================================================

void il2cpp_profiler_install_allocation(undefined8 param_1)

{
  if (DAT_02108958 != 0) {
    *(undefined8 *)(*(long *)(DAT_02108950 + DAT_02108958 * 8 + -8) + 0x28) = param_1;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_install_gc
// Address: 00de4740
// ==========================================================================================

void il2cpp_profiler_install_gc(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  
  if (DAT_02108958 != 0) {
    lVar1 = DAT_02108950 + DAT_02108958 * 8;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x30) = param_1;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x38) = param_2;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_install_fileio
// Address: 00de4744
// ==========================================================================================

void il2cpp_profiler_install_fileio(undefined8 param_1)

{
  if (DAT_02108958 != 0) {
    *(undefined8 *)(*(long *)(DAT_02108950 + DAT_02108958 * 8 + -8) + 0x40) = param_1;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_profiler_install_thread
// Address: 00de4748
// ==========================================================================================

void il2cpp_profiler_install_thread(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  
  if (DAT_02108958 != 0) {
    lVar1 = DAT_02108950 + DAT_02108958 * 8;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x48) = param_1;
    *(undefined8 *)(*(long *)(lVar1 + -8) + 0x50) = param_2;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_property_get_name
// Address: 00de474c
// ==========================================================================================

undefined8 il2cpp_property_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 8);
}



// ==========================================================================================
// Function: il2cpp_property_get_get_method
// Address: 00de4750
// ==========================================================================================

undefined8 il2cpp_property_get_get_method(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_property_get_set_method
// Address: 00de4754
// ==========================================================================================

undefined8 il2cpp_property_get_set_method(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: il2cpp_property_get_parent
// Address: 00de4758
// ==========================================================================================

undefined8 il2cpp_property_get_parent(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_property_get_flags
// Address: 00de475c
// ==========================================================================================

undefined4 il2cpp_property_get_flags(long param_1)

{
  return *(undefined4 *)(param_1 + 0x20);
}



// ==========================================================================================
// Function: il2cpp_object_get_class
// Address: 00de4760
// ==========================================================================================

undefined8 il2cpp_object_get_class(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_object_get_size
// Address: 00de4764
// ==========================================================================================

ulong il2cpp_object_get_size(long *param_1)

{
  int iVar1;
  ulong uVar2;
  long lVar3;
  
  lVar3 = *param_1;
  if (lVar3 == *(long *)(PTR_DAT_01ff5418 + 0x90)) {
    iVar1 = FUN_00dc71b0();
    uVar2 = (ulong)(iVar1 * 2 + 0x1a);
  }
  else {
    if (*(byte *)(lVar3 + 0x132) == 0) {
      uVar2 = FUN_00dfcff8(lVar3);
      return uVar2;
    }
    iVar1 = *(int *)(lVar3 + 0x104) * *(int *)(param_1 + 3);
    if (param_1[2] == 0) {
      uVar2 = (ulong)(iVar1 + 0x20);
    }
    else {
      uVar2 = (ulong)((iVar1 + 0x23U & 0xfffffffc) + (uint)*(byte *)(lVar3 + 0x132) * 0x10);
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: il2cpp_object_get_virtual_method
// Address: 00de4768
// ==========================================================================================

long il2cpp_object_get_virtual_method(long *param_1,long param_2)

{
  long lVar1;
  long lVar2;
  long *plVar3;
  ulong uVar4;
  int *piVar5;
  
  lVar1 = param_2;
  if ((*(ushort *)(param_2 + 0x4c) & 0x60) == 0x40) {
    lVar1 = *(long *)(param_2 + 0x20);
    if ((((*(byte *)(lVar1 + 0x118) >> 5 & 1) == 0) && (*(char *)(lVar1 + 0x2a) != '\x1e')) &&
       (*(char *)(lVar1 + 0x2a) != '\x13')) {
      plVar3 = (long *)(*param_1 + (ulong)*(ushort *)(param_2 + 0x50) * 0x10 + 0x140);
    }
    else {
      lVar2 = *param_1;
      uVar4 = (ulong)*(ushort *)(lVar2 + 0x12e);
      if (uVar4 != 0) {
        piVar5 = (int *)(*(long *)(lVar2 + 0xb0) + 8);
        do {
          if (*(long *)(piVar5 + -2) == lVar1) {
            lVar1 = lVar2 + (long)(int)(*piVar5 + (uint)*(ushort *)(param_2 + 0x50)) * 0x10 + 0x138;
            goto LAB_00e11ac8;
          }
          uVar4 = uVar4 - 1;
          piVar5 = piVar5 + 4;
        } while (uVar4 != 0);
      }
      lVar1 = FUN_00e0dcd4();
LAB_00e11ac8:
      plVar3 = (long *)(lVar1 + 8);
    }
    lVar1 = *plVar3;
    uVar4 = FUN_00dd1560(param_2);
    if ((uVar4 & 1) != 0) {
      lVar1 = FUN_00da7550(lVar1,param_2);
      return lVar1;
    }
  }
  return lVar1;
}



// ==========================================================================================
// Function: il2cpp_object_new
// Address: 00de476c
// ==========================================================================================

void il2cpp_object_new(void)

{
                    /* try { // try from 00de4770 to 00de4773 has its CatchHandler @ 00de477c */
  thunk_FUN_00e11c14();
  return;
}



// ==========================================================================================
// Function: il2cpp_object_unbox
// Address: 00de478c
// ==========================================================================================

long il2cpp_object_unbox(long param_1)

{
  return param_1 + 0x10;
}



// ==========================================================================================
// Function: il2cpp_value_box
// Address: 00de4790
// ==========================================================================================

long il2cpp_value_box(long param_1,long *param_2)

{
  bool bVar1;
  int iVar2;
  size_t __n;
  long lVar3;
  
  if (*(int *)(param_1 + 0x28) < 0) {
    if ((*(long *)(param_1 + 0x60) == 0) || ((*(byte *)(param_1 + 0x135) >> 3 & 1) == 0)) {
      bVar1 = false;
    }
    else {
      if (*(char *)param_2 == '\0') {
        return 0;
      }
      bVar1 = true;
    }
    lVar3 = FUN_00e11c14(param_1);
    iVar2 = FUN_00dfcff8(param_1);
    __n = (long)iVar2 - 0x10;
    if (bVar1) {
      iVar2 = *(int *)(*(long *)(param_1 + 0x80) + 0x38) + -0x10;
      param_2 = (long *)((long)param_2 + (long)iVar2);
      __n = __n - (long)iVar2;
    }
    memcpy((void *)(lVar3 + 0x10),param_2,__n);
  }
  else {
    lVar3 = *param_2;
  }
  return lVar3;
}



// ==========================================================================================
// Function: il2cpp_monitor_enter
// Address: 00de4794
// ==========================================================================================

void il2cpp_monitor_enter(undefined8 param_1)

{
  FUN_00dd19fc(param_1,0xffffffff);
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_try_enter
// Address: 00de4798
// ==========================================================================================

undefined8 il2cpp_monitor_try_enter(long param_1,int param_2)

{
  long *plVar1;
  pthread_t *ppVar2;
  int *piVar3;
  char cVar4;
  bool bVar5;
  int iVar6;
  pthread_t pVar7;
  undefined8 *puVar8;
  void *pvVar9;
  long lVar10;
  
  pVar7 = pthread_self();
  plVar1 = (long *)(param_1 + 8);
LAB_00dd1a40:
  do {
    while (lVar10 = *plVar1, lVar10 == 0) {
      puVar8 = (undefined8 *)FUN_00dd1ccc(&DAT_02107990);
      do {
        cVar4 = '\x01';
        bVar5 = (bool)ExclusiveMonitorPass(puVar8 + 1,0x10);
        if (bVar5) {
          puVar8[1] = pVar7;
          cVar4 = ExclusiveMonitorsStatus();
        }
      } while (cVar4 != '\0');
      DataMemoryBarrier(2,3);
      while (*plVar1 == 0) {
        cVar4 = '\x01';
        bVar5 = (bool)ExclusiveMonitorPass(plVar1,0x10);
        if (bVar5) {
          *plVar1 = (long)puVar8;
          cVar4 = ExclusiveMonitorsStatus();
        }
        if (cVar4 == '\0') goto LAB_00dd1c3c;
      }
      ClearExclusiveLocal();
      DataMemoryBarrier(2,3);
      puVar8[1] = 0xffffffffffffffff;
      do {
        *puVar8 = DAT_021079d0;
        cVar4 = '\x01';
        bVar5 = (bool)ExclusiveMonitorPass(0x21079d0,0x10);
        if (bVar5) {
          cVar4 = ExclusiveMonitorsStatus();
          DAT_021079d0 = puVar8;
        }
      } while (cVar4 != '\0');
    }
    ppVar2 = (pthread_t *)(lVar10 + 8);
    if (*ppVar2 == pVar7) {
      *(int *)(lVar10 + 0x14) = *(int *)(lVar10 + 0x14) + 1;
      return 1;
    }
    while (*ppVar2 == 0) {
      cVar4 = '\x01';
      bVar5 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
      if (bVar5) {
        *ppVar2 = pVar7;
        cVar4 = ExclusiveMonitorsStatus();
      }
      if (cVar4 == '\0') goto code_r0x00dd1a68;
    }
    ClearExclusiveLocal();
    DataMemoryBarrier(2,3);
    if (param_2 == 0) {
      return 0;
    }
    piVar3 = (int *)(lVar10 + 0x20);
    do {
      cVar4 = '\x01';
      bVar5 = (bool)ExclusiveMonitorPass(piVar3,0x10);
      if (bVar5) {
        *piVar3 = *piVar3 + 1;
        cVar4 = ExclusiveMonitorsStatus();
      }
    } while (cVar4 != '\0');
    DataMemoryBarrier(2,3);
    pvVar9 = pthread_getspecific(*DAT_02107b00);
    FUN_00dd2f68(pvVar9,0x20);
    if (*plVar1 == lVar10) {
      while (*plVar1 == lVar10) {
        while (*ppVar2 == 0) {
          cVar4 = '\x01';
          bVar5 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
          if (bVar5) {
            *ppVar2 = pVar7;
            cVar4 = ExclusiveMonitorsStatus();
          }
          if (cVar4 == '\0') {
            DataMemoryBarrier(2,3);
            do {
              cVar4 = '\x01';
              bVar5 = (bool)ExclusiveMonitorPass(piVar3,0x10);
              if (bVar5) {
                *piVar3 = *piVar3 + -1;
                cVar4 = ExclusiveMonitorsStatus();
              }
            } while (cVar4 != '\0');
            DataMemoryBarrier(2,3);
            pvVar9 = pthread_getspecific(*DAT_02107b00);
            FUN_00dd30e4(pvVar9,0x20);
            return 1;
          }
        }
        ClearExclusiveLocal();
        DataMemoryBarrier(2,3);
        if (param_2 == -1) {
          iVar6 = FUN_00dca8e8(lVar10 + 0x18,1);
        }
        else {
          iVar6 = FUN_00dca8f4(lVar10 + 0x18,param_2,1);
        }
        if (iVar6 == -2) {
          do {
            iVar6 = *piVar3;
            cVar4 = '\x01';
            bVar5 = (bool)ExclusiveMonitorPass(piVar3,0x10);
            if (bVar5) {
              *piVar3 = iVar6 + -1;
              cVar4 = ExclusiveMonitorsStatus();
            }
          } while (cVar4 != '\0');
          DataMemoryBarrier(2,3);
          pvVar9 = pthread_getspecific(*DAT_02107b00);
          FUN_00dd30e4(pvVar9,0x20);
          if ((iVar6 == 1) && (*plVar1 == lVar10)) {
            while (*ppVar2 == 0) {
              cVar4 = '\x01';
              bVar5 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
              if (bVar5) {
                *ppVar2 = pVar7;
                cVar4 = ExclusiveMonitorsStatus();
              }
              if (cVar4 == '\0') {
LAB_00dd1c3c:
                DataMemoryBarrier(2,3);
                return 1;
              }
            }
            ClearExclusiveLocal();
            DataMemoryBarrier(2,3);
          }
          if (*plVar1 != lVar10) {
            FUN_00dca72c(lVar10 + 0x28);
          }
          return 0;
        }
      }
    }
    FUN_00dd1d28(lVar10);
  } while( true );
code_r0x00dd1a68:
  DataMemoryBarrier(2,3);
  if (*plVar1 == lVar10) {
    return 1;
  }
  do {
    cVar4 = '\x01';
    bVar5 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar5) {
      *ppVar2 = 0;
      cVar4 = ExclusiveMonitorsStatus();
    }
  } while (cVar4 != '\0');
  DataMemoryBarrier(2,3);
  goto LAB_00dd1a40;
}



// ==========================================================================================
// Function: il2cpp_monitor_exit
// Address: 00de479c
// ==========================================================================================

void il2cpp_monitor_exit(long param_1)

{
  char cVar1;
  bool bVar2;
  int iVar3;
  undefined8 *puVar4;
  
  puVar4 = (undefined8 *)FUN_00dd1e90();
  iVar3 = *(int *)((long)puVar4 + 0x14) + -1;
  if (iVar3 < 1) {
    if ((int)puVar4[4] != 0) {
      do {
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(puVar4 + 1,0x10);
        if (bVar2) {
          puVar4[1] = 0;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
      DataMemoryBarrier(2,3);
LAB_00dd1dc8:
      FUN_00dcb420(puVar4 + 3,1,0);
      return;
    }
    if (puVar4[6] == 0) {
      do {
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass((undefined8 *)(param_1 + 8),0x10);
        if (bVar2) {
          *(undefined8 *)(param_1 + 8) = 0;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
      DataMemoryBarrier(2,3);
      FUN_00dca830(puVar4 + 5);
      if ((int)puVar4[4] != 0) {
        do {
          FUN_00dcb420(puVar4 + 3,puVar4[4],0);
          FUN_00dca8f4(puVar4 + 5,1,0);
        } while ((int)puVar4[4] != 0);
      }
      puVar4[1] = 0xffffffffffffffff;
      do {
        *puVar4 = DAT_021079d0;
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(0x21079d0,0x10);
        if (bVar2) {
          cVar1 = ExclusiveMonitorsStatus();
          DAT_021079d0 = puVar4;
        }
      } while (cVar1 != '\0');
    }
    else {
      do {
        cVar1 = '\x01';
        bVar2 = (bool)ExclusiveMonitorPass(puVar4 + 1,0x10);
        if (bVar2) {
          puVar4[1] = 0;
          cVar1 = ExclusiveMonitorsStatus();
        }
      } while (cVar1 != '\0');
      DataMemoryBarrier(2,3);
      if ((int)puVar4[4] != 0) goto LAB_00dd1dc8;
    }
  }
  else {
    *(int *)((long)puVar4 + 0x14) = iVar3;
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_pulse
// Address: 00de47a0
// ==========================================================================================

void il2cpp_monitor_pulse(undefined8 param_1)

{
  FUN_00dd1ef4(param_1,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_pulse_all
// Address: 00de47a4
// ==========================================================================================

void il2cpp_monitor_pulse_all(undefined8 param_1)

{
  FUN_00dd1ef4(param_1,1);
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_wait
// Address: 00de47a8
// ==========================================================================================

void il2cpp_monitor_wait(undefined8 param_1)

{
  FUN_00dd1f84(param_1,0xffffffff);
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_try_wait
// Address: 00de47ac
// ==========================================================================================

bool il2cpp_monitor_try_wait(long param_1,int param_2)

{
  long *plVar1;
  long lVar2;
  undefined4 uVar3;
  char cVar4;
  bool bVar5;
  int iVar6;
  long lVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  long lVar10;
  exception_ptr aeStack_58 [8];
  undefined4 auStack_50 [2];
  void *pvStack_48;
  long lStack_38;
  
  lVar7 = FUN_00dd1e90();
  uVar3 = *(undefined4 *)(lVar7 + 0x14);
  *(undefined4 *)(lVar7 + 0x14) = 1;
  if (param_2 == 0) {
    puVar8 = (undefined8 *)0x0;
  }
  else {
    puVar8 = (undefined8 *)FUN_00dd3f40(&DAT_02107a10);
    plVar1 = (long *)(lVar7 + 0x30);
    *(undefined4 *)(puVar8 + 3) = 1;
    do {
      lVar7 = *plVar1;
      puVar8[1] = lVar7;
      do {
        lVar10 = *plVar1;
        if (lVar10 != lVar7) {
          ClearExclusiveLocal();
          bVar5 = false;
          goto LAB_00dd1ffc;
        }
        cVar4 = '\x01';
        bVar5 = (bool)ExclusiveMonitorPass(plVar1,0x10);
        if (bVar5) {
          *plVar1 = (long)puVar8;
          cVar4 = ExclusiveMonitorsStatus();
        }
      } while (cVar4 != '\0');
      bVar5 = true;
LAB_00dd1ffc:
      DataMemoryBarrier(2,3);
      lVar2 = lVar7;
      if (!bVar5) {
        lVar2 = lVar10;
      }
    } while (lVar2 != lVar7);
  }
  FUN_00dd1d6c(param_1);
  lStack_38 = 0;
  if (param_2 == 0) {
    iVar6 = -2;
  }
  else {
    auStack_50[0] = 0x20;
    pvStack_48 = pthread_getspecific(*DAT_02107b00);
    FUN_00dd2f68(pvStack_48,0x20);
    iVar6 = FUN_00dca8f4(puVar8 + 2,param_2,1);
    FUN_00dd2164(auStack_50);
  }
  while( true ) {
    FUN_00dd19fc(param_1,0xffffffff);
    lVar7 = *(long *)(param_1 + 8);
    *(undefined4 *)(lVar7 + 0x14) = uVar3;
    if (puVar8 != (undefined8 *)0x0) {
      FUN_00dd2184(lVar7,puVar8);
      *(undefined4 *)(puVar8 + 3) = 0;
      FUN_00dca830(puVar8 + 2);
      do {
        *puVar8 = DAT_02107a50;
        cVar4 = '\x01';
        bVar5 = (bool)ExclusiveMonitorPass(0x2107a50,0x10);
        if (bVar5) {
          cVar4 = ExclusiveMonitorsStatus();
          DAT_02107a50 = puVar8;
        }
      } while (cVar4 != '\0');
    }
    if (lStack_38 == 0) break;
    std::exception_ptr::exception_ptr(aeStack_58,(exception_ptr *)&lStack_38);
    uVar9 = std::rethrow_exception(aeStack_58);
    FUN_00dd2164(auStack_50);
    __cxa_begin_catch(uVar9);
    std::current_exception();
    std::exception_ptr::operator=((exception_ptr *)&lStack_38,(exception_ptr *)auStack_50);
    std::exception_ptr::~exception_ptr((exception_ptr *)auStack_50);
    __cxa_end_catch();
    iVar6 = -3;
  }
  std::exception_ptr::~exception_ptr((exception_ptr *)&lStack_38);
  return iVar6 != -2;
}



// ==========================================================================================
// Function: il2cpp_runtime_invoke_convert_args
// Address: 00de47b0
// ==========================================================================================

long il2cpp_runtime_invoke_convert_args
               (long param_1,long param_2,long param_3,uint param_4,undefined8 param_5)

{
  uint uVar1;
  int iVar2;
  long lVar3;
  long lVar4;
  long *plVar5;
  long *__s;
  undefined8 uVar6;
  undefined8 uVar7;
  long lVar8;
  undefined8 uVar9;
  ulong __n;
  long *plVar10;
  ulong uVar11;
  long lVar12;
  uint uVar13;
  long alStack_80 [4];
  
  lVar3 = tpidr_el0;
  alStack_80[3] = *(long *)(lVar3 + 0x28);
  uVar11 = (ulong)param_4;
  if (param_3 == 0) {
    uVar13 = 0;
    plVar10 = (long *)0x0;
  }
  else {
    plVar10 = (long *)((long)alStack_80 -
                      ((-(ulong)(param_4 >> 0x1f) & 0xfffffff800000000 | uVar11 << 3) + 0xf &
                      0xfffffffffffffff0));
    alStack_80[0] = param_2;
    alStack_80[1] = param_5;
    alStack_80[2] = lVar3;
    if ((int)param_4 < 1) {
      uVar13 = 0;
    }
    else {
      lVar12 = 0;
      uVar13 = 0;
      __s = plVar10;
      do {
        lVar3 = *(long *)(*(long *)(param_1 + 0x30) + lVar12);
        uVar1 = *(uint *)(lVar3 + 8) & 0x20000000;
        lVar3 = FUN_00dfc824(lVar3,1);
        FUN_00dfcccc();
        if ((int)*(uint *)(lVar3 + 0x28) < 0) {
          if ((*(long *)(lVar3 + 0x60) == 0) || ((*(byte *)(lVar3 + 0x135) >> 3 & 1) == 0)) {
            lVar4 = *(long *)(param_3 + lVar12);
            if (uVar1 == 0) {
              if (lVar4 == 0) {
                __n = (ulong)(*(int *)(lVar3 + 0xf8) - 0x10);
                __s = (long *)((long)__s - (__n + 0xf & 0x1fffffff0));
                *(long **)((long)plVar10 + lVar12) = __s;
                memset(__s,0,__n);
                goto LAB_00df6178;
              }
            }
            else if (lVar4 == 0) {
              uVar9 = thunk_FUN_00e11c14(lVar3);
              FUN_00e331f0((long *)(param_3 + lVar12),uVar9);
              lVar4 = *(long *)(param_3 + lVar12);
            }
            lVar4 = FUN_00e11d68(lVar4);
LAB_00df6134:
            *(long *)((long)plVar10 + lVar12) = lVar4;
          }
          else {
            __s = (long *)((long)__s - ((ulong)*(uint *)(lVar3 + 0xf8) - 1 & 0xfffffffffffffff0));
            FUN_00e11d70(*(undefined8 *)(param_3 + lVar12),lVar3,__s);
            *(long **)((long)plVar10 + lVar12) = __s;
            uVar13 = uVar13 | uVar1 >> 0x1d;
          }
        }
        else {
          if (uVar1 == 0) {
            lVar4 = *(long *)(param_3 + lVar12);
            if ((*(uint *)(lVar3 + 0x28) & 0xff0000) != 0xf0000) goto LAB_00df6134;
            if (lVar4 == 0) {
              *(undefined8 *)((long)plVar10 + lVar12) = 0;
              goto LAB_00df6178;
            }
            plVar5 = (long *)FUN_00e11d68();
            lVar3 = *plVar5;
          }
          else {
            lVar3 = param_3 + lVar12;
          }
          *(long *)((long)plVar10 + lVar12) = lVar3;
        }
LAB_00df6178:
        lVar12 = lVar12 + 8;
        param_2 = alStack_80[0];
        lVar3 = alStack_80[2];
        param_5 = alStack_80[1];
      } while (uVar11 * 8 - lVar12 != 0);
    }
  }
  lVar12 = *(long *)(param_1 + 0x20);
  iVar2 = strcmp(*(char **)(param_1 + 0x18),".ctor");
  if ((iVar2 == 0) && (lVar12 != DAT_02107dc0)) {
    if (param_2 == 0) {
      if ((*(long *)(lVar12 + 0x60) == 0) || ((*(byte *)(lVar12 + 0x135) >> 3 & 1) == 0)) {
        lVar4 = thunk_FUN_00e11c14(lVar12);
        lVar8 = lVar4;
        if (*(int *)(lVar12 + 0x28) < 0) {
          lVar8 = FUN_00e11d68(lVar4,lVar4);
        }
        FUN_00df5da8(param_1,lVar8,plVar10,param_5);
        goto LAB_00df625c;
      }
      lVar12 = *(long *)(lVar12 + 0x48);
      param_2 = *plVar10;
    }
    else {
      FUN_00df5da8(param_1,param_2,plVar10,param_5);
    }
    lVar4 = FUN_00e11868(lVar12,param_2);
  }
  else {
    if ((*(long *)(lVar12 + 0x60) != 0) && ((*(byte *)(lVar12 + 0x135) >> 3 & 1) != 0)) {
      uVar9 = thunk_FUN_00e11c14(lVar12);
      uVar6 = FUN_00e11868(*(undefined8 *)(*(long *)(param_1 + 0x20) + 0x48),param_2);
      uVar7 = FUN_00e11d68(uVar9);
      FUN_00e11dd8(uVar7,uVar6,*(undefined8 *)(param_1 + 0x20));
      param_2 = FUN_00e11d68(uVar9);
    }
    lVar4 = FUN_00df5da8(param_1,param_2,plVar10,param_5);
  }
LAB_00df625c:
  if ((uVar13 ^ 1 | (uint)((int)param_4 < 1)) == 0) {
    lVar12 = 0;
    do {
      lVar8 = *(long *)(*(long *)(param_1 + 0x30) + lVar12);
      if ((((*(byte *)(lVar8 + 0xb) >> 5 & 1) != 0) &&
          (lVar8 = FUN_00dfc824(lVar8,1), *(long *)(lVar8 + 0x60) != 0)) &&
         ((*(byte *)(lVar8 + 0x135) >> 3 & 1) != 0)) {
        uVar9 = FUN_00e11868(lVar8,*(undefined8 *)((long)plVar10 + lVar12));
        FUN_00e331f0(param_3 + lVar12,uVar9);
      }
      lVar12 = lVar12 + 8;
    } while (uVar11 * 8 - lVar12 != 0);
  }
  lVar12 = lVar4;
  if (*(char *)(*(long *)(param_1 + 0x28) + 10) == '\x0f') {
    if (((DAT_02108118 & 1) == 0) && (iVar2 = __cxa_guard_acquire(&DAT_02108118), iVar2 != 0)) {
      DAT_02108110 = thunk_FUN_00deb928(DAT_02107d30,"System.Reflection","Pointer");
      __cxa_guard_release(&DAT_02108118);
    }
    lVar12 = thunk_FUN_00e11c14(DAT_02108110);
    *(long *)(lVar12 + 0x10) = lVar4;
    uVar9 = FUN_00e12fb0(*(undefined8 *)(param_1 + 0x28));
    FUN_00e331f0(lVar12 + 0x18,uVar9);
  }
  if (*(long *)(lVar3 + 0x28) != alStack_80[3]) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return lVar12;
}



// ==========================================================================================
// Function: il2cpp_runtime_invoke
// Address: 00de47b4
// ==========================================================================================

void il2cpp_runtime_invoke(long param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4)

{
  if (param_4 != (undefined8 *)0x0) {
    *param_4 = 0;
  }
  if ((((*(byte *)(param_1 + 0x4c) >> 4 & 1) != 0) && (*(long *)(param_1 + 0x20) != 0)) &&
     (*(int *)(*(long *)(param_1 + 0x20) + 0xe0) == 0)) {
    FUN_00df405c();
  }
  FUN_00df5e4c(param_1,param_2,param_3);
  return;
}



// ==========================================================================================
// Function: il2cpp_runtime_class_init
// Address: 00de47b8
// ==========================================================================================

void il2cpp_runtime_class_init(long param_1)

{
  int *piVar1;
  pthread_t *ppVar2;
  void *pvVar3;
  pthread_t pVar4;
  char cVar5;
  bool bVar6;
  int iVar7;
  pthread_t pVar8;
  long lVar9;
  undefined8 uVar10;
  pthread_t pVar11;
  int iVar12;
  int *piVar13;
  byte abStack_78 [16];
  void *pvStack_68;
  byte abStack_60 [16];
  void *pvStack_50;
  long lStack_48;
  
  piVar13 = (int *)(param_1 + 0xe0);
  if (*piVar13 != 0) {
    return;
  }
  pVar8 = pthread_self();
  if (pVar8 == DAT_02108160) {
    DAT_02108168 = DAT_02108168 + 1;
  }
  else {
    iVar12 = 0;
    do {
      iVar7 = DAT_02108120;
      if (DAT_02108120 == iVar12) {
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
        if (bVar6) {
          cVar5 = ExclusiveMonitorsStatus();
          DAT_02108120 = iVar12 + 1;
        }
        if (cVar5 != '\0') goto LAB_00df40e4;
        bVar6 = true;
      }
      else {
        ClearExclusiveLocal();
LAB_00df40e4:
        bVar6 = false;
      }
    } while ((iVar7 != 2) && (iVar12 = iVar7, !bVar6));
    while (iVar7 != 0) {
      FUN_00e4d8f8(&DAT_02108120,2,0xffffffff);
      do {
        iVar7 = DAT_02108120;
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
        if (bVar6) {
          DAT_02108120 = 2;
          cVar5 = ExclusiveMonitorsStatus();
        }
      } while (cVar5 != '\0');
    }
    DAT_02108168 = 1;
    DAT_02108160 = pVar8;
  }
  while (*piVar13 == 1) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') {
      DataMemoryBarrier(2,3);
      if (DAT_02108168 < 1) {
        return;
      }
      if (DAT_02108168 + -1 == 0) {
        DAT_02108160 = 0;
        DAT_02108168 = 0;
        do {
          iVar12 = DAT_02108120;
          cVar5 = '\x01';
          bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
          if (bVar6) {
            DAT_02108120 = 0;
            cVar5 = ExclusiveMonitorsStatus();
          }
        } while (cVar5 != '\0');
        if (iVar12 == 2) {
          FUN_00e4d950(&DAT_02108120,1,0);
          return;
        }
        DAT_02108160 = 0;
        DAT_02108168 = 0;
        return;
      }
      DAT_02108168 = DAT_02108168 + -1;
      return;
    }
  }
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  piVar1 = (int *)(param_1 + 0xdc);
LAB_00df41b4:
  if (*piVar1 == 1) goto code_r0x00df41c0;
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  ppVar2 = (pthread_t *)(param_1 + 0xe8);
  pVar8 = pthread_self();
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = pVar8;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar6) {
      *piVar1 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  iVar12 = DAT_02108168 + -1;
  if ((0 < DAT_02108168) && (DAT_02108168 = iVar12, iVar12 == 0)) {
    DAT_02108160 = 0;
    DAT_02108168 = 0;
    do {
      iVar12 = DAT_02108120;
      cVar5 = '\x01';
      bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
      if (bVar6) {
        DAT_02108120 = 0;
        cVar5 = ExclusiveMonitorsStatus();
      }
    } while (cVar5 != '\0');
    if (iVar12 == 2) {
      FUN_00e4d950(&DAT_02108120,1,0);
    }
  }
  lStack_48 = 0;
  lVar9 = FUN_00dff79c(param_1);
  if (lVar9 != 0) {
    FUN_00df5da8(lVar9,0,0,&lStack_48);
  }
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = 0;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  DataMemoryBarrier(2,3);
  if (lStack_48 != 0) {
    FUN_00deea58(abStack_78,param_1 + 0x20,0);
    pvVar3 = (void *)((ulong)abStack_78 | 1);
    if ((abStack_78[0] & 1) != 0) {
      pvVar3 = pvStack_68;
    }
    FUN_00dc6ac4(abStack_60,"The type initializer for \'%s\' threw an exception.",pvVar3);
    if ((abStack_78[0] & 1) != 0) {
      operator_delete(pvStack_68);
    }
    pvVar3 = (void *)((ulong)abStack_60 | 1);
    if ((abStack_60[0] & 1) != 0) {
      pvVar3 = pvStack_50;
    }
    uVar10 = FUN_00e29638(pvVar3,lStack_48);
    FUN_00dfd62c(param_1,uVar10);
    if ((abStack_60[0] & 1) != 0) {
      operator_delete(pvStack_50);
    }
    goto LAB_00df43bc;
  }
  do {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  goto LAB_00df43b8;
code_r0x00df41c0:
  cVar5 = '\x01';
  bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
  if (bVar6) {
    *piVar1 = 1;
    cVar5 = ExclusiveMonitorsStatus();
  }
  if (cVar5 == '\0') goto code_r0x00df41c8;
  goto LAB_00df41b4;
code_r0x00df41c8:
  DataMemoryBarrier(2,3);
  iVar12 = DAT_02108168 + -1;
  if ((0 < DAT_02108168) && (DAT_02108168 = iVar12, iVar12 == 0)) {
    DAT_02108160 = 0;
    DAT_02108168 = 0;
    do {
      iVar12 = DAT_02108120;
      cVar5 = '\x01';
      bVar6 = (bool)ExclusiveMonitorPass(0x2108120,0x10);
      if (bVar6) {
        DAT_02108120 = 0;
        cVar5 = ExclusiveMonitorsStatus();
      }
    } while (cVar5 != '\0');
    if (iVar12 == 2) {
      FUN_00e4d950(&DAT_02108120,1,0);
    }
  }
  pVar8 = pthread_self();
  ppVar2 = (pthread_t *)(param_1 + 0xe8);
  do {
    pVar11 = *ppVar2;
    if (pVar11 != pVar8) {
      ClearExclusiveLocal();
      bVar6 = false;
      goto LAB_00df4378;
    }
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(ppVar2,0x10);
    if (bVar6) {
      *ppVar2 = pVar8;
      cVar5 = ExclusiveMonitorsStatus();
    }
  } while (cVar5 != '\0');
  bVar6 = true;
LAB_00df4378:
  DataMemoryBarrier(2,3);
  pVar4 = pVar8;
  if (!bVar6) {
    pVar4 = pVar11;
  }
  if (pVar4 == pVar8) {
    return;
  }
  while (*piVar13 == 1) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
    if (bVar6) {
      *piVar13 = 1;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') goto LAB_00df43b8;
  }
  ClearExclusiveLocal();
  DataMemoryBarrier(2,3);
  piVar1 = (int *)(param_1 + 0xd8);
  while (*piVar1 == 0) {
    cVar5 = '\x01';
    bVar6 = (bool)ExclusiveMonitorPass(piVar1,0x10);
    if (bVar6) {
      *piVar1 = 0;
      cVar5 = ExclusiveMonitorsStatus();
    }
    if (cVar5 == '\0') {
      DataMemoryBarrier(2,3);
      FUN_00dcba94(1,0);
      while (*piVar13 == 1) {
        cVar5 = '\x01';
        bVar6 = (bool)ExclusiveMonitorPass(piVar13,0x10);
        if (bVar6) {
          *piVar13 = 1;
          cVar5 = ExclusiveMonitorsStatus();
        }
        if (cVar5 == '\0') goto LAB_00df43b8;
      }
      ClearExclusiveLocal();
      DataMemoryBarrier(2,3);
    }
  }
  ClearExclusiveLocal();
LAB_00df43b8:
  DataMemoryBarrier(2,3);
LAB_00df43bc:
  if (*(int *)(param_1 + 0xd8) == 0) {
    return;
  }
  uVar10 = FUN_00e3234c();
                    /* WARNING: Subroutine does not return */
  FUN_00e28a74(uVar10,0);
}



// ==========================================================================================
// Function: il2cpp_runtime_object_init
// Address: 00de47bc
// ==========================================================================================

void il2cpp_runtime_object_init(undefined8 param_1)

{
  FUN_00df6404(param_1,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_runtime_object_init_exception
// Address: 00de47c0
// ==========================================================================================

void il2cpp_runtime_object_init_exception(undefined8 *param_1,undefined8 param_2)

{
  long lVar1;
  
  lVar1 = FUN_00dfd198(*param_1,".ctor",0);
  if (*(int *)(*(long *)(lVar1 + 0x20) + 0x28) < 0) {
    param_1 = (undefined8 *)FUN_00e11d68(param_1);
  }
  FUN_00df5da8(lVar1,param_1,0,param_2);
  return;
}



// ==========================================================================================
// Function: il2cpp_runtime_unhandled_exception_policy_set
// Address: 00de47c4
// ==========================================================================================

void il2cpp_runtime_unhandled_exception_policy_set(undefined4 param_1)

{
  DAT_020ff0a8 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_string_length
// Address: 00de47c8
// ==========================================================================================

undefined4 il2cpp_string_length(long param_1)

{
  return *(undefined4 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_string_chars
// Address: 00de47cc
// ==========================================================================================

long il2cpp_string_chars(long param_1)

{
  return param_1 + 0x14;
}



// ==========================================================================================
// Function: il2cpp_string_new
// Address: 00de47d0
// ==========================================================================================

void il2cpp_string_new(char *param_1)

{
  size_t sVar1;
  
  sVar1 = strlen(param_1);
  FUN_00e0e678(param_1,sVar1);
  return;
}



// ==========================================================================================
// Function: il2cpp_string_new_wrapper
// Address: 00de47d4
// ==========================================================================================

void il2cpp_string_new_wrapper(char *param_1)

{
  size_t sVar1;
  
  sVar1 = strlen(param_1);
  FUN_00e0e678(param_1,sVar1);
  return;
}



// ==========================================================================================
// Function: il2cpp_string_new_utf16
// Address: 00de47d8
// ==========================================================================================

undefined8 il2cpp_string_new_utf16(void *param_1,uint param_2)

{
  undefined8 uVar1;
  void *__dest;
  
  uVar1 = FUN_00e0e748(param_2);
  __dest = (void *)FUN_00dc71a8();
  memcpy(__dest,param_1,-(ulong)(param_2 >> 0x1f) & 0xfffffffe00000000 | (ulong)param_2 << 1);
  return uVar1;
}



// ==========================================================================================
// Function: il2cpp_string_new_len
// Address: 00de47dc
// ==========================================================================================

undefined8 il2cpp_string_new_len(undefined8 param_1,undefined4 param_2)

{
  ulong uVar1;
  void *__src;
  undefined8 uVar2;
  void *__dest;
  byte abStack_38 [8];
  ulong uStack_30;
  void *pvStack_28;
  
  FUN_00dc6e94(abStack_38,param_1,param_2);
  uVar1 = (ulong)(abStack_38[0] >> 1);
  __src = (void *)((ulong)abStack_38 | 2);
  if ((abStack_38[0] & 1) != 0) {
    uVar1 = uStack_30;
    __src = pvStack_28;
  }
  uVar2 = FUN_00e0e748(uVar1 & 0xffffffff);
  __dest = (void *)FUN_00dc71a8();
  memcpy(__dest,__src,-(uVar1 >> 0x1f & 1) & 0xfffffffe00000000 | (uVar1 & 0xffffffff) << 1);
  if ((abStack_38[0] & 1) != 0) {
    operator_delete(pvStack_28);
  }
  return uVar2;
}



// ==========================================================================================
// Function: il2cpp_string_intern
// Address: 00de47e0
// ==========================================================================================

undefined8 il2cpp_string_intern(long param_1)

{
  char cVar1;
  bool bVar2;
  void *pvVar3;
  ulong uVar4;
  undefined8 uStack_38;
  undefined4 auStack_30 [2];
  long lStack_28;
  
  if (DAT_02108750 == (void *)0x0) {
    pvVar3 = operator_new(0x88);
    FUN_00e0e8e0();
    do {
      if (DAT_02108750 != (void *)0x0) {
        ClearExclusiveLocal();
        DataMemoryBarrier(2,3);
        FUN_00e0e930(pvVar3);
        operator_delete(pvVar3);
        goto LAB_00e0e86c;
      }
      cVar1 = '\x01';
      bVar2 = (bool)ExclusiveMonitorPass(0x2108750,0x10);
      if (bVar2) {
        cVar1 = ExclusiveMonitorsStatus();
        DAT_02108750 = pvVar3;
      }
    } while (cVar1 != '\0');
    DataMemoryBarrier(2,3);
  }
LAB_00e0e86c:
  auStack_30[0] = *(undefined4 *)(param_1 + 0x10);
  lStack_28 = param_1 + 0x14;
  uStack_38 = 0;
  uVar4 = FUN_00e0e97c(DAT_02108750,auStack_30,&uStack_38);
  if ((uVar4 & 1) == 0) {
    lStack_28 = FUN_00dc71a8(param_1);
    uStack_38 = FUN_00e0ea84(DAT_02108750,auStack_30,param_1);
  }
  return uStack_38;
}



// ==========================================================================================
// Function: il2cpp_string_is_interned
// Address: 00de47e4
// ==========================================================================================

undefined8 il2cpp_string_is_interned(long param_1)

{
  ulong uVar1;
  undefined4 auStack_20 [2];
  long lStack_18;
  undefined8 uStack_8;
  
  if (DAT_02108750 == 0) {
    uStack_8 = 0;
  }
  else {
    auStack_20[0] = *(undefined4 *)(param_1 + 0x10);
    lStack_18 = param_1 + 0x14;
    uStack_8 = 0;
    uVar1 = FUN_00e0e97c(DAT_02108750,auStack_20,&uStack_8);
    if ((uVar1 & 1) == 0) {
      uStack_8 = 0;
    }
  }
  return uStack_8;
}



// ==========================================================================================
// Function: il2cpp_thread_current
// Address: 00de47e8
// ==========================================================================================

void il2cpp_thread_current(void)

{
  pthread_getspecific(*DAT_02107b00);
  return;
}



// ==========================================================================================
// Function: il2cpp_thread_attach
// Address: 00de47ec
// ==========================================================================================

void * il2cpp_thread_attach(undefined8 param_1)

{
  void *pvVar1;
  undefined8 uVar2;
  
  pvVar1 = pthread_getspecific(*DAT_02107b00);
  if (pvVar1 == (void *)0x0) {
    FUN_00e31c10();
    FUN_00df6a5c();
    uVar2 = FUN_00dcb79c();
    pvVar1 = (void *)thunk_FUN_00e11c14(*(undefined8 *)(PTR_DAT_01ff5418 + 0x100));
    FUN_00dd24cc(pvVar1,uVar2);
    *(undefined4 *)(*(long *)((long)pvVar1 + 0x10) + 0x38) = 0;
    FUN_00dd256c(pvVar1,param_1);
  }
  return pvVar1;
}



// ==========================================================================================
// Function: il2cpp_thread_detach
// Address: 00de47f0
// ==========================================================================================

void il2cpp_thread_detach(undefined8 param_1)

{
  FUN_00dd2860(param_1,0);
  FUN_00df6ae4();
  return;
}



// ==========================================================================================
// Function: il2cpp_thread_get_all_attached_threads
// Address: 00de47f4
// ==========================================================================================

long il2cpp_thread_get_all_attached_threads(long *param_1)

{
  long lVar1;
  
  lVar1 = *DAT_02107b18;
  *param_1 = DAT_02107b18[1] - lVar1 >> 3;
  return lVar1;
}



// ==========================================================================================
// Function: il2cpp_is_vm_thread
// Address: 00de47f8
// ==========================================================================================

uint il2cpp_is_vm_thread(void)

{
  uint uVar1;
  
  uVar1 = FUN_00e32afc();
  return ~uVar1 & 1;
}



// ==========================================================================================
// Function: il2cpp_current_thread_walk_frame_stack
// Address: 00de47fc
// ==========================================================================================

void il2cpp_current_thread_walk_frame_stack(code *param_1,undefined8 param_2)

{
  long *plVar1;
  long lVar2;
  
  plVar1 = (long *)FUN_00df6b64();
  lVar2 = *plVar1;
  if (lVar2 != plVar1[1]) {
    do {
      (*param_1)(lVar2,param_2);
      lVar2 = lVar2 + 0x20;
    } while (lVar2 != plVar1[1]);
  }
  return;
}



// ==========================================================================================
// Function: il2cpp_thread_walk_frame_stack
// Address: 00de4800
// ==========================================================================================

void il2cpp_thread_walk_frame_stack(long param_1,undefined8 param_2,undefined8 param_3)

{
  undefined auStack_38 [8];
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  FUN_00dca69c(auStack_38,0,0);
  uStack_30 = param_2;
  uStack_28 = param_3;
  FUN_00dcba8c(*(undefined8 *)(*(long *)(param_1 + 0x10) + 0x18),FUN_00df6e60,auStack_38);
  FUN_00dca8e8(auStack_38,0);
  FUN_00dca704(auStack_38);
  return;
}



// ==========================================================================================
// Function: il2cpp_current_thread_get_top_frame
// Address: 00de4804
// ==========================================================================================

void il2cpp_current_thread_get_top_frame(undefined8 param_1)

{
  FUN_00df6c60(0,param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_thread_get_top_frame
// Address: 00de4810
// ==========================================================================================

undefined il2cpp_thread_get_top_frame(long param_1,undefined8 param_2)

{
  undefined auStack_38 [8];
  undefined8 uStack_30;
  undefined uStack_28;
  
  FUN_00dca69c(auStack_38,0,0);
  uStack_30 = param_2;
  FUN_00dcba8c(*(undefined8 *)(*(long *)(param_1 + 0x10) + 0x18),FUN_00df6fd0,auStack_38);
  FUN_00dca8e8(auStack_38,0);
  FUN_00dca704(auStack_38);
  return uStack_28;
}



// ==========================================================================================
// Function: il2cpp_current_thread_get_frame_at
// Address: 00de4814
// ==========================================================================================

bool il2cpp_current_thread_get_frame_at(undefined4 param_1,long *param_2)

{
  undefined4 auStack_20 [2];
  long lStack_18;
  
  lStack_18 = 0;
  auStack_20[0] = param_1;
  FUN_00e2807c(FUN_00df762c,auStack_20,1);
  if (lStack_18 != 0) {
    *param_2 = lStack_18;
  }
  return lStack_18 != 0;
}



// ==========================================================================================
// Function: il2cpp_thread_get_frame_at
// Address: 00de4818
// ==========================================================================================

undefined il2cpp_thread_get_frame_at(long param_1,undefined4 param_2,undefined8 param_3)

{
  undefined auStack_40 [8];
  undefined4 uStack_38;
  undefined8 uStack_30;
  undefined uStack_28;
  
  FUN_00dca69c(auStack_40,0,0);
  uStack_38 = param_2;
  uStack_30 = param_3;
  FUN_00dcba8c(*(undefined8 *)(*(long *)(param_1 + 0x10) + 0x18),FUN_00df6d84,auStack_40);
  FUN_00dca8e8(auStack_40,0);
  FUN_00dca704(auStack_40);
  return uStack_28;
}



// ==========================================================================================
// Function: il2cpp_current_thread_get_stack_depth
// Address: 00de481c
// ==========================================================================================

ulong il2cpp_current_thread_get_stack_depth(void)

{
  long *plVar1;
  
  plVar1 = (long *)FUN_00df6b64();
  return (ulong)(plVar1[1] - *plVar1) >> 5;
}



// ==========================================================================================
// Function: il2cpp_thread_get_stack_depth
// Address: 00de4838
// ==========================================================================================

undefined4 il2cpp_thread_get_stack_depth(long param_1)

{
  undefined auStack_20 [8];
  undefined4 uStack_18;
  
  FUN_00dca69c(auStack_20,0,0);
  FUN_00dcba8c(*(undefined8 *)(*(long *)(param_1 + 0x10) + 0x18),FUN_00df6f28,auStack_20);
  FUN_00dca8e8(auStack_20,0);
  FUN_00dca704(auStack_20);
  return uStack_18;
}



// ==========================================================================================
// Function: il2cpp_set_default_thread_affinity
// Address: 00de483c
// ==========================================================================================

void il2cpp_set_default_thread_affinity(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_override_stack_backtrace
// Address: 00de4840
// ==========================================================================================

void il2cpp_override_stack_backtrace(undefined8 param_1)

{
  DAT_021088a8 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_type_get_object
// Address: 00de4844
// ==========================================================================================

undefined8 il2cpp_type_get_object(undefined8 param_1)

{
  ulong uVar1;
  long lVar2;
  undefined8 uStack_20;
  undefined8 uStack_18;
  
  uStack_20 = 0;
  uStack_18 = param_1;
  uVar1 = FUN_00e13fe8(DAT_021087d8,&uStack_18,&uStack_20);
  if ((uVar1 & 1) == 0) {
    lVar2 = FUN_00e11c14(*(undefined8 *)(PTR_DAT_01ff5418 + 0x1a0));
    *(undefined8 *)(lVar2 + 0x10) = uStack_18;
    uStack_20 = FUN_00e140f0(DAT_021087d8,&uStack_18,lVar2);
  }
  return uStack_20;
}



// ==========================================================================================
// Function: il2cpp_type_get_type
// Address: 00de4848
// ==========================================================================================

undefined il2cpp_type_get_type(long param_1)

{
  return *(undefined *)(param_1 + 10);
}



// ==========================================================================================
// Function: il2cpp_type_get_class_or_element_class
// Address: 00de484c
// ==========================================================================================

void il2cpp_type_get_class_or_element_class(long **param_1)

{
  if (*(char *)((long)param_1 + 10) == '\x1d') {
    param_1 = (long **)*param_1;
  }
  else if (*(char *)((long)param_1 + 10) == '\x14') {
    param_1 = (long **)**param_1;
  }
  FUN_00dfc824(param_1,1);
  return;
}



// ==========================================================================================
// Function: il2cpp_type_get_name
// Address: 00de4850
// ==========================================================================================

void * il2cpp_type_get_name(undefined8 param_1)

{
  ulong uVar1;
  void *__src;
  void *__dest;
  byte local_38 [8];
  ulong local_30;
  void *local_28;
  
  FUN_00deea58(local_38,param_1,0);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    uVar1 = local_30;
  }
                    /* try { // try from 00de4884 to 00de4887 has its CatchHandler @ 00de48d4 */
  __dest = malloc(uVar1 + 1);
  __src = (void *)((ulong)local_38 | 1);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    __src = local_28;
    uVar1 = local_30;
  }
  memcpy(__dest,__src,uVar1 + 1);
  if ((local_38[0] & 1) != 0) {
    operator_delete(local_28);
  }
  return __dest;
}



// ==========================================================================================
// Function: il2cpp_type_get_assembly_qualified_name
// Address: 00de48f0
// ==========================================================================================

void * il2cpp_type_get_assembly_qualified_name(undefined8 param_1)

{
  ulong uVar1;
  void *__src;
  void *__dest;
  byte local_38 [8];
  ulong local_30;
  void *local_28;
  
  FUN_00deea58(local_38,param_1,3);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    uVar1 = local_30;
  }
                    /* try { // try from 00de4924 to 00de4927 has its CatchHandler @ 00de4974 */
  __dest = malloc(uVar1 + 1);
  __src = (void *)((ulong)local_38 | 1);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    __src = local_28;
    uVar1 = local_30;
  }
  memcpy(__dest,__src,uVar1 + 1);
  if ((local_38[0] & 1) != 0) {
    operator_delete(local_28);
  }
  return __dest;
}



// ==========================================================================================
// Function: il2cpp_type_get_reflection_name
// Address: 00de4990
// ==========================================================================================

void * il2cpp_type_get_reflection_name(undefined8 param_1)

{
  ulong uVar1;
  void *__src;
  void *__dest;
  byte local_38 [8];
  ulong local_30;
  void *local_28;
  
  FUN_00deea58(local_38,param_1,1);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    uVar1 = local_30;
  }
                    /* try { // try from 00de49c4 to 00de49c7 has its CatchHandler @ 00de4a14 */
  __dest = malloc(uVar1 + 1);
  __src = (void *)((ulong)local_38 | 1);
  uVar1 = (ulong)(local_38[0] >> 1);
  if ((local_38[0] & 1) != 0) {
    __src = local_28;
    uVar1 = local_30;
  }
  memcpy(__dest,__src,uVar1 + 1);
  if ((local_38[0] & 1) != 0) {
    operator_delete(local_28);
  }
  return __dest;
}



// ==========================================================================================
// Function: il2cpp_type_is_byref
// Address: 00de4a30
// ==========================================================================================

byte il2cpp_type_is_byref(long param_1)

{
  return *(byte *)(param_1 + 0xb) >> 5 & 1;
}



// ==========================================================================================
// Function: il2cpp_type_get_attrs
// Address: 00de4a3c
// ==========================================================================================

undefined2 il2cpp_type_get_attrs(long param_1)

{
  return *(undefined2 *)(param_1 + 8);
}



// ==========================================================================================
// Function: il2cpp_type_equals
// Address: 00de4a44
// ==========================================================================================

bool il2cpp_type_equals(void)

{
  int iVar1;
  
  iVar1 = FUN_00da7e84();
  return iVar1 == 0;
}



// ==========================================================================================
// Function: il2cpp_type_is_static
// Address: 00de4a48
// ==========================================================================================

byte il2cpp_type_is_static(long param_1)

{
  return *(byte *)(param_1 + 8) >> 4 & 1;
}



// ==========================================================================================
// Function: il2cpp_type_is_pointer_type
// Address: 00de4a54
// ==========================================================================================

bool il2cpp_type_is_pointer_type(long param_1)

{
  return *(char *)(param_1 + 10) == '\x0f';
}



// ==========================================================================================
// Function: il2cpp_image_get_assembly
// Address: 00de4a68
// ==========================================================================================

undefined8 il2cpp_image_get_assembly(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: il2cpp_image_get_name
// Address: 00de4a6c
// ==========================================================================================

undefined8 il2cpp_image_get_name(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_image_get_filename
// Address: 00de4a70
// ==========================================================================================

undefined8 il2cpp_image_get_filename(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: il2cpp_image_get_entry_point
// Address: 00de4a74
// ==========================================================================================

undefined8 il2cpp_image_get_entry_point(long param_1)

{
  undefined8 uVar1;
  
  if ((*(long *)(param_1 + 0x28) != 0) && (*(int *)(*(long *)(param_1 + 0x28) + 0xc) != -1)) {
    uVar1 = FUN_00dce95c();
    return uVar1;
  }
  return 0;
}



// ==========================================================================================
// Function: il2cpp_image_get_class_count
// Address: 00de4a78
// ==========================================================================================

undefined4 il2cpp_image_get_class_count(void)

{
  undefined4 uVar1;
  
  uVar1 = FUN_00debcc4();
  return uVar1;
}



// ==========================================================================================
// Function: il2cpp_image_get_class
// Address: 00de4a8c
// ==========================================================================================

void il2cpp_image_get_class(void)

{
  thunk_FUN_00dcf4f4();
  thunk_FUN_00dcf974();
  return;
}



// ==========================================================================================
// Function: il2cpp_capture_memory_snapshot
// Address: 00de4a90
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int * il2cpp_capture_memory_snapshot(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  int iVar4;
  int *piVar5;
  undefined8 *puVar6;
  ulong uVar7;
  void *pvVar8;
  void *pvVar9;
  void *__dest;
  undefined4 uVar10;
  long **pplVar11;
  uint *puVar12;
  long *****ppppplVar13;
  long ******pppppplVar14;
  long ******pppppplVar15;
  undefined4 *puVar16;
  long ******pppppplVar17;
  long *****ppppplVar18;
  undefined8 *puVar19;
  long ******pppppplVar20;
  long *****ppppplVar21;
  long lVar22;
  uint uVar23;
  ulong uVar24;
  long ****pppplVar25;
  long **pplVar26;
  ulong uVar27;
  long ******pppppplVar28;
  long ****pppplVar29;
  ulong uStack_98;
  ulong uStack_90;
  void *pvStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  long ******pppppplStack_70;
  ulong uStack_68;
  
  piVar5 = (int *)calloc(1,0x60);
  uStack_80 = (undefined8 *)((ulong)uStack_80._4_4_ << 0x20);
  pppppplStack_70 = (long ******)0x0;
  uStack_68 = 0;
  uStack_78 = (long ******)&pppppplStack_70;
  puVar6 = (undefined8 *)FUN_00e11408();
  pplVar26 = (long **)*puVar6;
  pplVar11 = (long **)puVar6[1];
  if (pplVar26 != pplVar11) {
    do {
      lVar22 = **pplVar26;
      if (*(int *)(lVar22 + 0x18) != 0) {
        uVar23 = 0;
        do {
          thunk_FUN_00dcf4f4(lVar22,uVar23);
          uVar7 = thunk_FUN_00dcf974();
          if ((*(byte *)(uVar7 + 0x135) >> 1 & 1) != 0) {
            uStack_90 = (ulong)uStack_80 & 0xffffffff;
            uStack_80 = (undefined8 *)CONCAT44(uStack_80._4_4_,(int)uStack_80 + 1);
            uStack_98 = uVar7;
            FUN_00dd3bec(&uStack_78,&uStack_98,&uStack_98);
          }
          uVar23 = uVar23 + 1;
        } while (uVar23 < *(uint *)(lVar22 + 0x18));
        pplVar11 = (long **)puVar6[1];
      }
      pplVar26 = pplVar26 + 1;
    } while (pplVar26 != pplVar11);
  }
  FUN_00da73a0(FUN_00dd3bac,&uStack_80);
  FUN_00da7248(FUN_00dd3bac,&uStack_80);
  FUN_00e36930(FUN_00dd3bac,&uStack_80);
  FUN_00e01b9c(FUN_00dd3bac,&uStack_80);
  piVar5[8] = (int)uStack_68;
  pvVar8 = calloc(uStack_68 & 0xffffffff,0x48);
  *(void **)(piVar5 + 10) = pvVar8;
  if ((long *******)uStack_78 != &pppppplStack_70) {
    pppppplVar28 = uStack_78;
    do {
      ppppplVar21 = pppppplVar28[4];
      uVar7 = (ulong)*(uint *)(pppppplVar28 + 5);
      puVar12 = (uint *)((long)pvVar8 + uVar7 * 0x48);
      if (*(byte *)((long)ppppplVar21 + 0x132) == 0) {
        *puVar12 = (uint)((*(uint *)(ppppplVar21 + 5) & 0xff0000) == 0xf0000) |
                   *(uint *)(ppppplVar21 + 5) >> 0x1f;
        puVar12 = (uint *)((long)pvVar8 + uVar7 * 0x48 + 0x10);
        *puVar12 = 0;
        if ((ulong)*(ushort *)((long)ppppplVar21 + 0x124) != 0) {
          pvVar9 = calloc((ulong)*(ushort *)((long)ppppplVar21 + 0x124),0x18);
          *(void **)((long)pvVar8 + uVar7 * 0x48 + 8) = pvVar9;
          if (*(short *)((long)ppppplVar21 + 0x124) != 0) {
            uVar27 = 0;
            do {
              pppplVar29 = ppppplVar21[0x10];
              uVar24 = (ulong)*puVar12;
              lVar22 = *(long *)(*(long *)(piVar5 + 10) + uVar7 * 0x48 + 8);
              pppplVar25 = pppplVar29 + uVar27 * 4 + 1;
              ppppplVar13 = (long *****)FUN_00dfc824(*pppplVar25,1);
              pppppplVar15 = (long ******)&pppppplStack_70;
              pppppplVar17 = pppppplStack_70;
              if (pppppplStack_70 == (long ******)0x0) {
LAB_00dd0f4c:
                *(undefined4 *)(lVar22 + uVar24 * 0x18 + 4) = 0xffffffff;
              }
              else {
                do {
                  pppppplVar20 = pppppplVar17;
                  pppppplVar14 = pppppplVar15;
                  ppppplVar18 = pppppplVar20[4];
                  pppppplVar15 = pppppplVar14;
                  if (ppppplVar18 >= ppppplVar13) {
                    pppppplVar15 = pppppplVar20;
                  }
                  pppppplVar17 = (long ******)pppppplVar20[ppppplVar18 < ppppplVar13];
                } while ((long ******)pppppplVar20[ppppplVar18 < ppppplVar13] != (long ******)0x0);
                if ((long *******)pppppplVar15 == &pppppplStack_70) goto LAB_00dd0f4c;
                pppppplVar15 = pppppplVar14;
                if (ppppplVar13 <= ppppplVar18) {
                  pppppplVar15 = pppppplVar20;
                }
                if (ppppplVar13 < pppppplVar15[4]) goto LAB_00dd0f4c;
                if (ppppplVar13 <= ppppplVar18) {
                  pppppplVar14 = pppppplVar20;
                }
                iVar1 = *(int *)(pppppplVar14 + 5);
                *(int *)(lVar22 + uVar24 * 0x18 + 4) = iVar1;
                if ((iVar1 != -1) && (uVar23 = *(uint *)(*pppplVar25 + 1), (uVar23 >> 6 & 1) == 0))
                {
                  puVar16 = (undefined4 *)(lVar22 + uVar24 * 0x18);
                  *(byte *)(puVar16 + 4) = (byte)(uVar23 >> 4) & 1;
                  pppplVar29 = pppplVar29 + uVar27 * 4;
                  *puVar16 = *(undefined4 *)(pppplVar29 + 3);
                  *(long ****)(puVar16 + 2) = *pppplVar29;
                  *puVar12 = *puVar12 + 1;
                }
              }
              uVar27 = uVar27 + 1;
            } while (uVar27 < *(ushort *)((long)ppppplVar21 + 0x124));
          }
        }
        uVar23 = *(uint *)((long)ppppplVar21 + 0x10c);
        puVar12 = (uint *)((long)pvVar8 + uVar7 * 0x48 + 0x14);
        *puVar12 = uVar23;
        if ((uVar23 != 0) && (ppppplVar21[0x17] != (long ****)0x0)) {
          pvVar9 = malloc((ulong)uVar23);
          *(void **)((long)pvVar8 + uVar7 * 0x48 + 0x18) = pvVar9;
          memcpy(pvVar9,ppppplVar21[0x17],(ulong)*puVar12);
        }
        ppppplVar13 = (long *****)FUN_00dfd3b0(ppppplVar21);
        uVar10 = 0xffffffff;
        if ((ppppplVar13 != (long *****)0x0) &&
           (pppppplVar15 = (long ******)&pppppplStack_70, pppppplVar17 = pppppplStack_70,
           pppppplStack_70 != (long ******)0x0)) {
          do {
            pppppplVar20 = pppppplVar17;
            pppppplVar14 = pppppplVar15;
            ppppplVar18 = pppppplVar20[4];
            pppppplVar15 = pppppplVar14;
            if (ppppplVar18 >= ppppplVar13) {
              pppppplVar15 = pppppplVar20;
            }
            pppppplVar17 = (long ******)pppppplVar20[ppppplVar18 < ppppplVar13];
          } while ((long ******)pppppplVar20[ppppplVar18 < ppppplVar13] != (long ******)0x0);
          if ((long *******)pppppplVar15 != &pppppplStack_70) {
            pppppplVar15 = pppppplVar14;
            if (ppppplVar13 <= ppppplVar18) {
              pppppplVar15 = pppppplVar20;
            }
            if (pppppplVar15[4] <= ppppplVar13) {
              if (ppppplVar13 <= ppppplVar18) {
                pppppplVar14 = pppppplVar20;
              }
              goto LAB_00dd1078;
            }
          }
          goto LAB_00dd1068;
        }
      }
      else {
        *puVar12 = (uint)*(byte *)((long)ppppplVar21 + 0x132) << 0x10 | 2;
        if (pppppplStack_70 != (long ******)0x0) {
          ppppplVar13 = (long *****)ppppplVar21[8];
          pppppplVar15 = (long ******)&pppppplStack_70;
          pppppplVar17 = pppppplStack_70;
          do {
            pppppplVar20 = pppppplVar17;
            pppppplVar14 = pppppplVar15;
            ppppplVar18 = pppppplVar20[4];
            pppppplVar15 = pppppplVar14;
            if (ppppplVar18 >= ppppplVar13) {
              pppppplVar15 = pppppplVar20;
            }
            pppppplVar17 = (long ******)pppppplVar20[ppppplVar18 < ppppplVar13];
          } while ((long ******)pppppplVar20[ppppplVar18 < ppppplVar13] != (long ******)0x0);
          if ((long *******)pppppplVar15 != &pppppplStack_70) {
            pppppplVar15 = pppppplVar14;
            if (ppppplVar13 <= ppppplVar18) {
              pppppplVar15 = pppppplVar20;
            }
            if (pppppplVar15[4] <= ppppplVar13) {
              if (ppppplVar13 <= ppppplVar18) {
                pppppplVar14 = pppppplVar20;
              }
LAB_00dd1078:
              uVar10 = *(undefined4 *)(pppppplVar14 + 5);
              goto LAB_00dd1080;
            }
          }
        }
LAB_00dd1068:
        uVar10 = 0xffffffff;
      }
LAB_00dd1080:
      *(undefined4 *)((long)pvVar8 + uVar7 * 0x48 + 0x20) = uVar10;
      *(long ***)((long)pvVar8 + uVar7 * 0x48 + 0x30) = (*ppppplVar21)[2][3];
      FUN_00deea58(&uStack_98,ppppplVar21 + 4,0);
      uVar27 = uStack_98 >> 1 & 0x7f;
      if ((uStack_98 & 1) != 0) {
        uVar27 = uStack_90;
      }
      __dest = calloc(uVar27 + 1,1);
      *(void **)((long)pvVar8 + uVar7 * 0x48 + 0x28) = __dest;
      pvVar9 = (void *)((ulong)&uStack_98 | 1);
      uVar27 = uStack_98 >> 1 & 0x7f;
      if ((uStack_98 & 1) != 0) {
        pvVar9 = pvStack_88;
        uVar27 = uStack_90;
      }
      memcpy(__dest,pvVar9,uVar27 + 1);
      *(long ******)((long)pvVar8 + uVar7 * 0x48 + 0x38) = ppppplVar21;
      iVar1 = *(int *)(ppppplVar21 + 0x1f);
      if (*(int *)(ppppplVar21 + 5) < 0) {
        iVar1 = *(int *)(ppppplVar21 + 0x1f) + -0x10;
      }
      *(int *)((long)pvVar8 + uVar7 * 0x48 + 0x40) = iVar1;
      if ((uStack_98 & 1) != 0) {
        operator_delete(pvStack_88);
      }
      pppppplVar15 = (long ******)pppppplVar28[1];
      if ((long ******)pppppplVar28[1] == (long ******)0x0) {
        pppppplVar15 = pppppplVar28 + 2;
        pppppplVar17 = (long ******)*pppppplVar15;
        if ((long ******)*pppppplVar17 != pppppplVar28) {
          do {
            ppppplVar21 = *pppppplVar15;
            pppppplVar15 = (long ******)(ppppplVar21 + 2);
            pppppplVar17 = (long ******)*pppppplVar15;
          } while (*pppppplVar17 != ppppplVar21);
        }
      }
      else {
        do {
          pppppplVar17 = pppppplVar15;
          pppppplVar15 = (long ******)*pppppplVar17;
        } while ((long ******)*pppppplVar17 != (long ******)0x0);
      }
      if ((long *******)pppppplVar17 == &pppppplStack_70) break;
      pvVar8 = *(void **)(piVar5 + 10);
      pppppplVar28 = pppppplVar17;
    } while( true );
  }
  FUN_00da562c(&uStack_78,pppppplStack_70);
  do {
    thunk_FUN_00e4433c(FUN_00dd3cb0,piVar5);
    thunk_FUN_00e44498();
    iVar1 = *piVar5;
    iVar4 = thunk_FUN_00e44e18();
    if (iVar1 == iVar4) {
      uStack_80 = *(undefined8 **)(piVar5 + 2);
      uStack_78 = (long ******)CONCAT71(uStack_78._1_7_,1);
      thunk_FUN_00e44c80(&uStack_80,FUN_00dd3d64);
      if ((char)uStack_78 != '\0') break;
    }
    thunk_FUN_00e444d0();
    FUN_00dd13ac(piVar5);
  } while( true );
  uStack_80 = *(undefined8 **)(piVar5 + 2);
  thunk_FUN_00e44c80(&uStack_80,FUN_00dd3cf8);
  thunk_FUN_00e444d0();
  uStack_80 = (undefined8 *)0x0;
  uStack_78 = (long ******)0x0;
  pppppplStack_70 = (long ******)0x0;
  FUN_00e328f8(FUN_00dd3d94,&uStack_80);
  uVar7 = (long)uStack_78 - (long)uStack_80 >> 3;
  piVar5[0xc] = (int)uVar7;
  puVar6 = (undefined8 *)calloc(uVar7 & 0xffffffff,8);
  *(undefined8 **)(piVar5 + 0xe) = puVar6;
  uVar7 = (ulong)(uint)piVar5[0xc];
  puVar19 = uStack_80;
  if (piVar5[0xc] == 0) {
    if (uStack_80 == (undefined8 *)0x0) goto LAB_00dd1278;
  }
  else {
    do {
      uVar7 = uVar7 - 1;
      *puVar6 = *puVar19;
      puVar6 = puVar6 + 1;
      puVar19 = puVar19 + 1;
    } while (uVar7 != 0);
  }
  uStack_78 = (long ******)uStack_80;
  operator_delete(uStack_80);
LAB_00dd1278:
  uVar3 = _DAT_005bd410;
  uVar2 = DAT_005bc9e0;
  *(undefined8 *)(piVar5 + 0x12) = _UNK_005bd418;
  *(undefined8 *)(piVar5 + 0x10) = uVar3;
  *(undefined8 *)(piVar5 + 0x14) = uVar2;
  return piVar5;
}



// ==========================================================================================
// Function: il2cpp_free_captured_memory_snapshot
// Address: 00de4a94
// ==========================================================================================

void il2cpp_free_captured_memory_snapshot(void *param_1)

{
  long lVar1;
  long lVar2;
  ulong uVar3;
  
  FUN_00dd13ac();
  free(*(void **)((long)param_1 + 0x38));
  if (*(int *)((long)param_1 + 0x20) != 0) {
    lVar2 = 0;
    uVar3 = 0;
    do {
      lVar1 = *(long *)((long)param_1 + 0x28);
      if ((*(byte *)(lVar1 + lVar2) >> 1 & 1) == 0) {
        free(*(void **)(lVar1 + lVar2 + 8));
        free(*(void **)(*(long *)((long)param_1 + 0x28) + lVar2 + 0x18));
        lVar1 = *(long *)((long)param_1 + 0x28);
      }
      free(*(void **)(lVar1 + lVar2 + 0x28));
      uVar3 = uVar3 + 1;
      lVar2 = lVar2 + 0x48;
    } while (uVar3 < *(uint *)((long)param_1 + 0x20));
  }
  free(*(void **)((long)param_1 + 0x28));
  free(param_1);
  return;
}



// ==========================================================================================
// Function: il2cpp_set_find_plugin_callback
// Address: 00de4a98
// ==========================================================================================

void il2cpp_set_find_plugin_callback(undefined8 param_1)

{
  DAT_02107870 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_register_log_callback
// Address: 00de4a9c
// ==========================================================================================

void il2cpp_register_log_callback(undefined *param_1)

{
  PTR_FUN_020ff028 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_debugger_set_agent_options
// Address: 00de4aa0
// ==========================================================================================

void il2cpp_debugger_set_agent_options(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_is_debugger_attached
// Address: 00de4aa4
// ==========================================================================================

undefined8 il2cpp_is_debugger_attached(void)

{
  return 0;
}



// ==========================================================================================
// Function: il2cpp_register_debugger_agent_transport
// Address: 00de4aa8
// ==========================================================================================

void il2cpp_register_debugger_agent_transport(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_debug_get_method_info
// Address: 00de4aac
// ==========================================================================================

undefined8 il2cpp_debug_get_method_info(long param_1,undefined8 *param_2)

{
  ulong uVar1;
  long lVar2;
  undefined4 uVar3;
  undefined8 uVar4;
  
  uVar4 = *(undefined8 *)(param_1 + 8);
  uVar1 = FUN_00e27de4();
  if (((uVar1 & 1) == 0) || (uVar1 = FUN_00e27e0c(uVar4), (uVar1 & 1) != 0)) {
    if (DAT_021077f0 < 1) {
      uVar3 = 0;
    }
    else {
      lVar2 = FUN_00dc9938(uVar4);
      if (lVar2 == 0) {
        return 0;
      }
      uVar3 = *(undefined4 *)(lVar2 + 8);
    }
    if (param_2 != (undefined8 *)0x0) {
      uVar4 = *(undefined8 *)(param_1 + 8);
      *(undefined4 *)(param_2 + 1) = uVar3;
      param_2[2] = 0;
      *param_2 = uVar4;
    }
    uVar4 = 1;
  }
  else {
    uVar4 = 0;
  }
  return uVar4;
}



// ==========================================================================================
// Function: il2cpp_unity_install_unitytls_interface
// Address: 00de4ab0
// ==========================================================================================

void il2cpp_unity_install_unitytls_interface(undefined8 param_1)

{
  DAT_02108108 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_from_class
// Address: 00de4ab4
// ==========================================================================================

void il2cpp_custom_attrs_from_class(undefined8 *param_1)

{
  thunk_FUN_00dcfb90(*param_1,*(undefined4 *)((long)param_1 + 0x11c));
  return;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_from_method
// Address: 00de4ac4
// ==========================================================================================

void il2cpp_custom_attrs_from_method(long param_1)

{
  thunk_FUN_00dcfb90(**(undefined8 **)(param_1 + 0x20),*(undefined4 *)(param_1 + 0x48));
  return;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_from_field
// Address: 00de4ad8
// ==========================================================================================

void il2cpp_custom_attrs_from_field(long param_1)

{
  thunk_FUN_00dcfb90(**(undefined8 **)(param_1 + 0x10),*(undefined4 *)(param_1 + 0x1c));
  return;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_has_attr
// Address: 00de4aec
// ==========================================================================================

uint il2cpp_custom_attrs_has_attr(undefined8 param_1,undefined8 param_2)

{
  uint uVar1;
  undefined auStack_30 [32];
  
  thunk_FUN_00dcfc98(auStack_30);
  uVar1 = FUN_00e1494c(auStack_30,param_2);
  return uVar1 & 1;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_get_attr
// Address: 00de4af0
// ==========================================================================================

undefined8 il2cpp_custom_attrs_get_attr(undefined8 param_1,long param_2)

{
  long lVar1;
  byte bVar2;
  int iVar3;
  undefined8 uVar4;
  code *pcVar5;
  undefined *puStack_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  long lStack_c8;
  undefined auStack_c0 [24];
  int iStack_a8;
  undefined auStack_a0 [16];
  long alStack_90 [4];
  long *plStack_70;
  undefined **ppuStack_60;
  long lStack_58;
  undefined ***pppuStack_40;
  long lStack_28;
  
  lVar1 = tpidr_el0;
  lStack_28 = *(long *)(lVar1 + 0x28);
  thunk_FUN_00dcfc98(auStack_c0);
  if (iStack_a8 == 0) {
    uVar4 = 0;
    goto LAB_00e14f28;
  }
  pppuStack_40 = &ppuStack_60;
  if (param_2 == 0) {
    ppuStack_60 = &PTR_FUN_01fb8940;
  }
  else {
    ppuStack_60 = &PTR_FUN_01fb8988;
    lStack_58 = param_2;
  }
  iVar3 = FUN_00e352b4(auStack_c0,&ppuStack_60);
  if (iVar3 == 0) {
    uVar4 = 0;
  }
  else {
    FUN_00e3538c(auStack_a0,auStack_c0,&ppuStack_60);
    lStack_c8 = 0;
    uStack_d8 = 0;
    uStack_d0 = 0;
    puStack_e0 = PTR_DAT_01ff5560 + 0x10;
    bVar2 = FUN_00e355e0(auStack_c0,auStack_a0,&puStack_e0,&lStack_c8);
    if ((lStack_c8 != 0 | (bVar2 ^ 0xff) & 1) == 0) {
      uVar4 = FUN_00e35274(&puStack_e0,&lStack_c8);
    }
    else {
      uVar4 = 0;
    }
    if (lStack_c8 != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00e28a74(lStack_c8,0);
    }
    if (alStack_90 == plStack_70) {
      pcVar5 = *(code **)(*plStack_70 + 0x20);
    }
    else {
      if (plStack_70 == (long *)0x0) goto LAB_00e14efc;
      pcVar5 = *(code **)(*plStack_70 + 0x28);
    }
    (*pcVar5)();
  }
LAB_00e14efc:
  if (&ppuStack_60 == pppuStack_40) {
    pcVar5 = (code *)(*pppuStack_40)[4];
  }
  else {
    if (pppuStack_40 == (undefined ***)0x0) goto LAB_00e14f28;
    pcVar5 = (code *)(*pppuStack_40)[5];
  }
  (*pcVar5)();
LAB_00e14f28:
  if (*(long *)(lVar1 + 0x28) == lStack_28) {
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_construct
// Address: 00de4af4
// ==========================================================================================

void il2cpp_custom_attrs_construct(void)

{
  undefined auStack_30 [32];
  
  thunk_FUN_00dcfc98(auStack_30);
  FUN_00e14b64(auStack_30,0);
  return;
}



// ==========================================================================================
// Function: il2cpp_custom_attrs_free
// Address: 00de4af8
// ==========================================================================================

void il2cpp_custom_attrs_free(void)

{
  return;
}



// ==========================================================================================
// Function: il2cpp_type_get_name_chunked
// Address: 00de4afc
// ==========================================================================================

void il2cpp_type_get_name_chunked(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  FUN_00def0c0(param_1,0,param_2,param_3);
  return;
}



// ==========================================================================================
// Function: il2cpp_class_set_userdata
// Address: 00de4b0c
// ==========================================================================================

void il2cpp_class_set_userdata(long param_1,undefined8 param_2)

{
  *(undefined8 *)(param_1 + 0xd0) = param_2;
  return;
}



// ==========================================================================================
// Function: il2cpp_class_get_userdata_offset
// Address: 00de4b14
// ==========================================================================================

undefined8 il2cpp_class_get_userdata_offset(void)

{
  return 0xd0;
}



// ==========================================================================================
// Function: il2cpp_class_for_each
// Address: 00de4b1c
// ==========================================================================================

void il2cpp_class_for_each(code *param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  long lVar2;
  long **pplVar3;
  long lVar4;
  uint uVar5;
  long **pplVar6;
  
  puVar1 = (undefined8 *)FUN_00e11408();
  pplVar6 = (long **)*puVar1;
  pplVar3 = (long **)puVar1[1];
  if (pplVar6 != pplVar3) {
    do {
      lVar4 = **pplVar6;
      if (*(int *)(lVar4 + 0x18) != 0) {
        uVar5 = 0;
        do {
          thunk_FUN_00dcf4f4(lVar4,uVar5);
          lVar2 = thunk_FUN_00dcf974();
          if ((*(byte *)(lVar2 + 0x135) >> 1 & 1) != 0) {
            (*param_1)(lVar2,param_2);
          }
          uVar5 = uVar5 + 1;
        } while (uVar5 < *(uint *)(lVar4 + 0x18));
        pplVar3 = (long **)puVar1[1];
      }
      pplVar6 = pplVar6 + 1;
    } while (pplVar6 != pplVar3);
  }
  FUN_00da73a0(param_1,param_2);
  FUN_00da7248(param_1,param_2);
  FUN_00e36930(param_1,param_2);
  FUN_00e01b9c(param_1,param_2);
  return;
}



// ==========================================================================================
// Function: il2cpp_unity_set_android_network_up_state_func
// Address: 00de4b20
// ==========================================================================================

void il2cpp_unity_set_android_network_up_state_func(undefined8 param_1)

{
  DAT_02107920 = param_1;
  return;
}



// ==========================================================================================
// Function: il2cpp_object_new
// Address: 01ec5470
// ==========================================================================================

void il2cpp_object_new(void)

{
  (*(code *)PTR_il2cpp_object_new_01ff5c58)();
  return;
}



// ==========================================================================================
// Function: il2cpp_raise_exception
// Address: 01ec5490
// ==========================================================================================

void il2cpp_raise_exception(void)

{
  (*(code *)PTR_il2cpp_raise_exception_01ff5c68)();
  return;
}



// ==========================================================================================
// Function: il2cpp_class_from_il2cpp_type
// Address: 01ec54b0
// ==========================================================================================

void il2cpp_class_from_il2cpp_type(void)

{
  (*(code *)PTR_il2cpp_class_from_il2cpp_type_01ff5c78)();
  return;
}



// ==========================================================================================
// Function: il2cpp_bounded_array_class_get
// Address: 01ec54c0
// ==========================================================================================

void il2cpp_bounded_array_class_get(void)

{
  (*(code *)PTR_il2cpp_bounded_array_class_get_01ff5c80)();
  return;
}



// ==========================================================================================
// Function: il2cpp_array_class_get
// Address: 01ec54d0
// ==========================================================================================

void il2cpp_array_class_get(void)

{
  (*(code *)PTR_il2cpp_array_class_get_01ff5c88)();
  return;
}



// ==========================================================================================
// Function: il2cpp_string_intern
// Address: 01ec5550
// ==========================================================================================

void il2cpp_string_intern(void)

{
  (*(code *)PTR_il2cpp_string_intern_01ff5cc8)();
  return;
}



// ==========================================================================================
// Function: il2cpp_array_element_size
// Address: 01ec5710
// ==========================================================================================

void il2cpp_array_element_size(void)

{
  (*(code *)PTR_il2cpp_array_element_size_01ff5da8)();
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_enter
// Address: 01ec5770
// ==========================================================================================

void il2cpp_monitor_enter(void)

{
  (*(code *)PTR_il2cpp_monitor_enter_01ff5dd8)();
  return;
}



// ==========================================================================================
// Function: il2cpp_monitor_exit
// Address: 01ec5780
// ==========================================================================================

void il2cpp_monitor_exit(void)

{
  (*(code *)PTR_il2cpp_monitor_exit_01ff5de0)();
  return;
}



// ==========================================================================================
// Function: il2cpp_array_new_specific
// Address: 01ec5790
// ==========================================================================================

void il2cpp_array_new_specific(void)

{
  (*(code *)PTR_il2cpp_array_new_specific_01ff5de8)();
  return;
}



// ==========================================================================================
// Function: il2cpp_method_get_object
// Address: 01ec58b0
// ==========================================================================================

void il2cpp_method_get_object(void)

{
  (*(code *)PTR_il2cpp_method_get_object_01ff5e78)();
  return;
}



// ==========================================================================================
// Function: il2cpp_class_from_type
// Address: 01ec5ad0
// ==========================================================================================

void il2cpp_class_from_type(void)

{
  (*(code *)PTR_il2cpp_class_from_type_01ff5f88)();
  return;
}



// ==========================================================================================
// Function: il2cpp_object_unbox
// Address: 01ec5b80
// ==========================================================================================

void il2cpp_object_unbox(void)

{
  (*(code *)PTR_il2cpp_object_unbox_01ff5fe0)();
  return;
}



// ==========================================================================================
// Function: il2cpp_string_new
// Address: 01ec5d20
// ==========================================================================================

void il2cpp_string_new(void)

{
  (*(code *)PTR_il2cpp_string_new_01ff60b0)();
  return;
}



// ==========================================================================================
// Function: il2cpp_array_new
// Address: 01ec5d40
// ==========================================================================================

void il2cpp_array_new(void)

{
  (*(code *)PTR_il2cpp_array_new_01ff60c0)();
  return;
}



// ==========================================================================================
