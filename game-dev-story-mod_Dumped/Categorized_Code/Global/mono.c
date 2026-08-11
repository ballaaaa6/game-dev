// Function: mono_image_get_entry_point
// Address: 00de4b24
// ==========================================================================================

ulong mono_image_get_entry_point(void)

{
  ulong uVar1;
  
  uVar1 = thunk_FUN_00dcf4d4();
  if (uVar1 != 0) {
    uVar1 = (ulong)*(uint *)(uVar1 + 0x48);
  }
  return uVar1;
}



// ==========================================================================================
// Function: mono_image_get_filename
// Address: 00de4b3c
// ==========================================================================================

undefined8 mono_image_get_filename(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: mono_image_get_guid
// Address: 00de4b40
// ==========================================================================================

char * mono_image_get_guid(void)

{
  return "00000000-0000-0000-0000-000000000000";
}



// ==========================================================================================
// Function: mono_image_is_dynamic
// Address: 00de4b4c
// ==========================================================================================

undefined8 mono_image_is_dynamic(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_image_get_assembly
// Address: 00de4b54
// ==========================================================================================

undefined8 mono_image_get_assembly(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: mono_image_get_name
// Address: 00de4b58
// ==========================================================================================

undefined8 mono_image_get_name(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: mono_get_root_domain
// Address: 00de4b5c
// ==========================================================================================

long mono_get_root_domain(void)

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
// Function: mono_domain_get
// Address: 00de4b60
// ==========================================================================================

long mono_domain_get(void)

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
// Function: mono_domain_foreach
// Address: 00de4b64
// ==========================================================================================

void mono_domain_foreach(code *UNRECOVERED_JUMPTABLE,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = FUN_00dce854();
                    /* WARNING: Could not recover jumptable at 0x00de4b88. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar1,param_2);
  return;
}



// ==========================================================================================
// Function: mono_domain_get_corlib
// Address: 00de4b8c
// ==========================================================================================

void mono_domain_get_corlib(void)

{
  FUN_00deb060(*(undefined8 *)PTR_DAT_01ff5418);
  return;
}



// ==========================================================================================
// Function: mono_domain_get_assemblies_iter
// Address: 00de4b9c
// ==========================================================================================

undefined8 mono_domain_get_assemblies_iter(undefined8 param_1,long **param_2)

{
  long *plVar1;
  undefined8 uVar2;
  long *plVar3;
  undefined8 *puVar4;
  
  if (param_2 == (long **)0x0) {
    uVar2 = 0;
  }
  else {
    plVar1 = (long *)FUN_00e11408();
    plVar3 = *param_2;
    if (plVar3 == (long *)0x0) {
      plVar3 = (long *)operator_new(8);
      puVar4 = (undefined8 *)*plVar1;
      *plVar3 = (long)puVar4;
      *param_2 = plVar3;
      uVar2 = *puVar4;
    }
    else {
      puVar4 = (undefined8 *)(*plVar3 + 8);
      *plVar3 = (long)puVar4;
      if (puVar4 == (undefined8 *)plVar1[1]) {
        operator_delete(plVar3);
        uVar2 = 0;
        *param_2 = (long *)0x0;
      }
      else {
        uVar2 = *puVar4;
      }
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: mono_type_get_class
// Address: 00de4c1c
// ==========================================================================================

void mono_type_get_class(long param_1)

{
  if (param_1 != 0) {
    FUN_00dcf9a4();
    return;
  }
  return;
}



// ==========================================================================================
// Function: mono_type_is_struct
// Address: 00de4c20
// ==========================================================================================

uint mono_type_is_struct(void)

{
  uint uVar1;
  
  uVar1 = FUN_00def384();
  return uVar1 & 1;
}



// ==========================================================================================
// Function: mono_type_is_reference
// Address: 00de4c34
// ==========================================================================================

ulong mono_type_is_reference(ulong param_1)

{
  uint uVar1;
  
  if (param_1 != 0) {
    uVar1 = FUN_00def334();
    param_1 = (ulong)(uVar1 & 1);
  }
  return param_1;
}



// ==========================================================================================
// Function: mono_type_generic_inst_is_valuetype
// Address: 00de4c4c
// ==========================================================================================

uint mono_type_generic_inst_is_valuetype(undefined8 *param_1)

{
  uint uVar1;
  
  thunk_FUN_00dcfa80(*(undefined8 *)*param_1);
  uVar1 = thunk_FUN_00dcfa98();
  return uVar1 & 1;
}



// ==========================================================================================
// Function: mono_type_full_name
// Address: 00de4c6c
// ==========================================================================================

undefined8 mono_type_full_name(undefined8 param_1)

{
  void *pvVar1;
  undefined8 uVar2;
  byte local_28 [16];
  void *local_18;
  
  FUN_00deea58(local_28,param_1,2);
  pvVar1 = (void *)((ulong)local_28 | 1);
  if ((local_28[0] & 1) != 0) {
    pvVar1 = local_18;
  }
                    /* try { // try from 00de4c98 to 00de4c9b has its CatchHandler @ 00de4cc0 */
  uVar2 = FUN_00dc7118(pvVar1);
  if ((local_28[0] & 1) != 0) {
    operator_delete(local_18);
  }
  return uVar2;
}



// ==========================================================================================
// Function: mono_type_get_name_full
// Address: 00de4cdc
// ==========================================================================================

undefined8 mono_type_get_name_full(void)

{
  void *pvVar1;
  undefined8 uVar2;
  byte local_28 [16];
  void *local_18;
  
  FUN_00deea58(local_28);
  pvVar1 = (void *)((ulong)local_28 | 1);
  if ((local_28[0] & 1) != 0) {
    pvVar1 = local_18;
  }
                    /* try { // try from 00de4d04 to 00de4d07 has its CatchHandler @ 00de4d2c */
  uVar2 = FUN_00dc7118(pvVar1);
  if ((local_28[0] & 1) != 0) {
    operator_delete(local_18);
  }
  return uVar2;
}



// ==========================================================================================
// Function: mono_string_free
// Address: 00de4d48
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void mono_string_free(void *__ptr)

{
  (*(code *)PTR_free_020ff040)();
  return;
}



// ==========================================================================================
// Function: mono_type_get_type
// Address: 00de4d4c
// ==========================================================================================

undefined mono_type_get_type(long param_1)

{
  return *(undefined *)(param_1 + 10);
}



// ==========================================================================================
// Function: mono_type_is_byref
// Address: 00de4d50
// ==========================================================================================

uint mono_type_is_byref(long param_1)

{
  return *(uint *)(param_1 + 8) >> 0x1d & 1;
}



// ==========================================================================================
// Function: mono_type_get_attrs
// Address: 00de4d5c
// ==========================================================================================

undefined2 mono_type_get_attrs(long param_1)

{
  return *(undefined2 *)(param_1 + 8);
}



// ==========================================================================================
// Function: mono_class_instance_size
// Address: 00de4d64
// ==========================================================================================

void mono_class_instance_size(undefined8 param_1)

{
  FUN_00dfcccc();
  FUN_00dfcff8(param_1);
  return;
}



// ==========================================================================================
// Function: mono_class_value_size
// Address: 00de4d7c
// ==========================================================================================

int mono_class_value_size(long param_1,uint *param_2)

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
// Function: mono_class_get_flags
// Address: 00de4d80
// ==========================================================================================

undefined4 mono_class_get_flags(long param_1)

{
  return *(undefined4 *)(param_1 + 0x118);
}



// ==========================================================================================
// Function: mono_class_num_fields
// Address: 00de4d88
// ==========================================================================================

void mono_class_num_fields(void)

{
  FUN_00dfd3a8();
  return;
}



// ==========================================================================================
// Function: mono_class_num_methods
// Address: 00de4d98
// ==========================================================================================

void mono_class_num_methods(void)

{
  FUN_00dfd398();
  return;
}



// ==========================================================================================
// Function: mono_class_num_properties
// Address: 00de4da8
// ==========================================================================================

void mono_class_num_properties(void)

{
  FUN_00dfd3a0();
  return;
}



// ==========================================================================================
// Function: mono_class_get_methods
// Address: 00de4db8
// ==========================================================================================

undefined8 mono_class_get_methods(long param_1,ulong *param_2)

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
// Function: mono_class_get_properties
// Address: 00de4dbc
// ==========================================================================================

ulong mono_class_get_properties(long param_1,ulong *param_2)

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
// Function: mono_class_get_nested_types
// Address: 00de4dc0
// ==========================================================================================

undefined8 mono_class_get_nested_types(long param_1)

{
  undefined8 uVar1;
  
  if (*(long *)(param_1 + 0x60) != 0) {
    return 0;
  }
  uVar1 = FUN_00dfd2bc();
  return uVar1;
}



// ==========================================================================================
// Function: mono_class_get_context
// Address: 00de4dd4
// ==========================================================================================

long mono_class_get_context(long param_1)

{
  return *(long *)(param_1 + 0x60) + 8;
}



// ==========================================================================================
// Function: mono_class_is_valuetype
// Address: 00de4de0
// ==========================================================================================

uint mono_class_is_valuetype(long param_1)

{
  return *(uint *)(param_1 + 0x28) >> 0x1f;
}



// ==========================================================================================
// Function: mono_class_get_namespace
// Address: 00de4dec
// ==========================================================================================

undefined8 mono_class_get_namespace(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: mono_class_get_name
// Address: 00de4df0
// ==========================================================================================

undefined8 mono_class_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: mono_class_get_parent
// Address: 00de4df4
// ==========================================================================================

undefined8 mono_class_get_parent(long param_1)

{
  return *(undefined8 *)(param_1 + 0x58);
}



// ==========================================================================================
// Function: mono_class_get_type
// Address: 00de4df8
// ==========================================================================================

long mono_class_get_type(long param_1)

{
  return param_1 + 0x20;
}



// ==========================================================================================
// Function: mono_class_get_type_token
// Address: 00de4e00
// ==========================================================================================

undefined4 mono_class_get_type_token(long param_1)

{
  return *(undefined4 *)(param_1 + 0x11c);
}



// ==========================================================================================
// Function: mono_class_get_byref_type
// Address: 00de4e08
// ==========================================================================================

long mono_class_get_byref_type(long param_1)

{
  return param_1 + 0x30;
}



// ==========================================================================================
// Function: mono_class_get_image
// Address: 00de4e10
// ==========================================================================================

undefined8 mono_class_get_image(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: mono_class_get_interfaces
// Address: 00de4e14
// ==========================================================================================

undefined8 mono_class_get_interfaces(long param_1,ulong *param_2)

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
// Function: mono_class_get_rank
// Address: 00de4e18
// ==========================================================================================

undefined mono_class_get_rank(long param_1)

{
  return *(undefined *)(param_1 + 0x132);
}



// ==========================================================================================
// Function: mono_class_get_element_class
// Address: 00de4e20
// ==========================================================================================

undefined8 mono_class_get_element_class(long param_1)

{
  return *(undefined8 *)(param_1 + 0x40);
}



// ==========================================================================================
// Function: mono_class_is_enum
// Address: 00de4e24
// ==========================================================================================

ushort mono_class_is_enum(long param_1)

{
  return *(ushort *)(param_1 + 0x135) >> 2 & 1;
}



// ==========================================================================================
// Function: mono_free_method_signatures
// Address: 00de4e34
// ==========================================================================================

void mono_free_method_signatures(void)

{
  void *pvVar1;
  
  pvVar1 = DAT_02107b28;
  if (DAT_02107b28 != (void *)0x0) {
    FUN_00da3118((long)DAT_02107b28 + 0x40);
    operator_delete(pvVar1);
  }
  DAT_02107b28 = (void *)0x0;
  return;
}



// ==========================================================================================
// Function: mono_debug_lookup_locals
// Address: 00de4e68
// ==========================================================================================

undefined8 mono_debug_lookup_locals(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_debug_free_locals
// Address: 00de4e70
// ==========================================================================================

void mono_debug_free_locals(void)

{
  return;
}



// ==========================================================================================
// Function: mono_debug_find_method
// Address: 00de4e74
// ==========================================================================================

undefined8 mono_debug_find_method(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_method_get_param_names
// Address: 00de4e7c
// ==========================================================================================

void mono_method_get_param_names(undefined8 param_1,long param_2)

{
  uint uVar1;
  undefined8 uVar2;
  ulong uVar3;
  
  uVar1 = FUN_00dd15f4();
  if (uVar1 != 0) {
    uVar3 = 0;
    do {
      uVar2 = FUN_00dd161c(param_1,uVar3 & 0xffffffff);
      *(undefined8 *)(param_2 + uVar3 * 8) = uVar2;
      uVar3 = uVar3 + 1;
    } while (uVar1 != uVar3);
  }
  return;
}



// ==========================================================================================
// Function: mono_method_get_context
// Address: 00de4ecc
// ==========================================================================================

long mono_method_get_context(long param_1)

{
  if ((*(byte *)(param_1 + 0x53) & 3) == 2) {
    return *(long *)(param_1 + 0x40) + 8;
  }
  return 0;
}



// ==========================================================================================
// Function: mono_method_get_header_checked
// Address: 00de4ef0
// ==========================================================================================

undefined8 mono_method_get_header_checked(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_metadata_free_mh
// Address: 00de4ef8
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void mono_metadata_free_mh(void *__ptr)

{
  (*(code *)PTR_free_020ff040)();
  return;
}



// ==========================================================================================
// Function: mono_method_full_name
// Address: 00de4efc
// ==========================================================================================

void mono_method_full_name(long param_1)

{
  FUN_00dc7118(*(undefined8 *)(param_1 + 0x18));
  return;
}



// ==========================================================================================
// Function: mono_method_get_generic_container
// Address: 00de4f04
// ==========================================================================================

undefined8 mono_method_get_generic_container(long param_1)

{
  if ((*(byte *)(param_1 + 0x53) & 3) == 1) {
    return *(undefined8 *)(param_1 + 0x40);
  }
  return 0;
}



// ==========================================================================================
// Function: mono_method_get_declaring_generic_method
// Address: 00de4f24
// ==========================================================================================

undefined8 mono_method_get_declaring_generic_method(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_method_get_name
// Address: 00de4f2c
// ==========================================================================================

undefined8 mono_method_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: mono_method_get_class
// Address: 00de4f30
// ==========================================================================================

undefined8 mono_method_get_class(long param_1)

{
  return *(undefined8 *)(param_1 + 0x20);
}



// ==========================================================================================
// Function: mono_method_get_flags
// Address: 00de4f34
// ==========================================================================================

void mono_method_get_flags(undefined8 param_1,undefined4 *param_2)

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
// Function: mono_method_get_token
// Address: 00de4f64
// ==========================================================================================

undefined4 mono_method_get_token(long param_1)

{
  return *(undefined4 *)(param_1 + 0x48);
}



// ==========================================================================================
// Function: mono_method_is_generic
// Address: 00de4f68
// ==========================================================================================

byte mono_method_is_generic(long param_1)

{
  return *(byte *)(param_1 + 0x53) & 1;
}



// ==========================================================================================
// Function: mono_method_is_inflated
// Address: 00de4f6c
// ==========================================================================================

byte mono_method_is_inflated(long param_1)

{
  return *(byte *)(param_1 + 0x53) >> 1 & 1;
}



// ==========================================================================================
// Function: mono_array_element_size
// Address: 00de4f70
// ==========================================================================================

undefined4 mono_array_element_size(long param_1)

{
  return *(undefined4 *)(param_1 + 0x104);
}



// ==========================================================================================
// Function: mono_array_length
// Address: 00de4f78
// ==========================================================================================

undefined8 mono_array_length(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_field_get_name
// Address: 00de4f80
// ==========================================================================================

undefined8 mono_field_get_name(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: mono_field_set_value
// Address: 00de4f84
// ==========================================================================================

void mono_field_set_value(void)

{
  return;
}



// ==========================================================================================
// Function: mono_field_get_parent
// Address: 00de4f88
// ==========================================================================================

undefined8 mono_field_get_parent(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: mono_field_get_offset
// Address: 00de4f8c
// ==========================================================================================

void mono_field_get_offset(void)

{
  FUN_00df3d34();
  return;
}



// ==========================================================================================
// Function: mono_field_get_type
// Address: 00de4f9c
// ==========================================================================================

undefined8 mono_field_get_type(long param_1)

{
  return *(undefined8 *)(param_1 + 8);
}



// ==========================================================================================
// Function: mono_string_chars
// Address: 00de4fa0
// ==========================================================================================

long mono_string_chars(long param_1)

{
  return param_1 + 0x14;
}



// ==========================================================================================
// Function: mono_string_length
// Address: 00de4fa8
// ==========================================================================================

undefined4 mono_string_length(long param_1)

{
  return *(undefined4 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: mono_string_new
// Address: 00de4fb0
// ==========================================================================================

void mono_string_new(undefined8 param_1,undefined8 param_2)

{
  FUN_00e0e65c(param_2);
  return;
}



// ==========================================================================================
// Function: mono_object_unbox_internal
// Address: 00de4fb8
// ==========================================================================================

long mono_object_unbox_internal(long param_1)

{
  return param_1 + 0x10;
}



// ==========================================================================================
// Function: mono_object_get_type
// Address: 00de4fbc
// ==========================================================================================

long mono_object_get_type(long *param_1)

{
  return *param_1 + 0x20;
}



// ==========================================================================================
// Function: mono_thread_current
// Address: 00de4fc8
// ==========================================================================================

void mono_thread_current(void)

{
  pthread_getspecific(*DAT_02107b00);
  return;
}



// ==========================================================================================
// Function: mono_thread_get_main
// Address: 00de4fcc
// ==========================================================================================

undefined8 mono_thread_get_main(void)

{
  return DAT_02107a90;
}



// ==========================================================================================
// Function: mono_thread_attach
// Address: 00de4fd0
// ==========================================================================================

void * mono_thread_attach(undefined8 param_1)

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
// Function: mono_thread_detach
// Address: 00de4fd4
// ==========================================================================================

void mono_thread_detach(undefined8 param_1)

{
  FUN_00dd2860(param_1,0);
  FUN_00df6ae4();
  return;
}



// ==========================================================================================
// Function: mono_thread_set_name
// Address: 00de4fd8
// ==========================================================================================

void mono_thread_set_name(undefined8 param_1,undefined8 param_2)

{
  undefined8 uVar1;
  undefined4 *in_x5;
  
  uVar1 = FUN_00e0e65c(param_2);
  FUN_00dd31c0(param_1,uVar1);
  if (in_x5 != (undefined4 *)0x0) {
    *in_x5 = 0;
  }
  return;
}



// ==========================================================================================
// Function: mono_thread_suspend_all_other_threads
// Address: 00de5010
// ==========================================================================================

void mono_thread_suspend_all_other_threads(void)

{
  return;
}



// ==========================================================================================
// Function: mono_thread_state_init_from_current
// Address: 00de5014
// ==========================================================================================

undefined8 mono_thread_state_init_from_current(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_thread_state_init_from_monoctx
// Address: 00de501c
// ==========================================================================================

undefined8 mono_thread_state_init_from_monoctx(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_property_get_name
// Address: 00de5024
// ==========================================================================================

undefined8 mono_property_get_name(long param_1)

{
  return *(undefined8 *)(param_1 + 8);
}



// ==========================================================================================
// Function: mono_property_get_get_method
// Address: 00de5028
// ==========================================================================================

undefined8 mono_property_get_get_method(long param_1)

{
  return *(undefined8 *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: mono_property_get_set_method
// Address: 00de502c
// ==========================================================================================

undefined8 mono_property_get_set_method(long param_1)

{
  return *(undefined8 *)(param_1 + 0x18);
}



// ==========================================================================================
// Function: mono_property_get_parent
// Address: 00de5030
// ==========================================================================================

undefined8 mono_property_get_parent(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: mono_gc_register_root
// Address: 00de5034
// ==========================================================================================

undefined8 mono_gc_register_root(void)

{
  FUN_00e31d44();
  return 1;
}



// ==========================================================================================
// Function: mono_runtime_quit
// Address: 00de5050
// ==========================================================================================

void mono_runtime_quit(void)

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
// Function: mono_runtime_is_shutting_down
// Address: 00de5054
// ==========================================================================================

uint mono_runtime_is_shutting_down(void)

{
  uint uVar1;
  
  uVar1 = FUN_00df5ba8();
  return uVar1 & 1;
}



// ==========================================================================================
// Function: mono_arch_setup_resume_sighandler_ctx
// Address: 00de5068
// ==========================================================================================

void mono_arch_setup_resume_sighandler_ctx(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_set_breakpoint
// Address: 00de506c
// ==========================================================================================

void mono_arch_set_breakpoint(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_clear_breakpoint
// Address: 00de5070
// ==========================================================================================

void mono_arch_clear_breakpoint(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_start_single_stepping
// Address: 00de5074
// ==========================================================================================

void mono_arch_start_single_stepping(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_stop_single_stepping
// Address: 00de5078
// ==========================================================================================

void mono_arch_stop_single_stepping(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_skip_breakpoint
// Address: 00de507c
// ==========================================================================================

void mono_arch_skip_breakpoint(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_skip_single_step
// Address: 00de5080
// ==========================================================================================

void mono_arch_skip_single_step(void)

{
  return;
}



// ==========================================================================================
// Function: mono_arch_context_get_int_reg
// Address: 00de5084
// ==========================================================================================

undefined8 mono_arch_context_get_int_reg(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_arch_context_set_int_reg
// Address: 00de508c
// ==========================================================================================

void mono_arch_context_set_int_reg(void)

{
  return;
}



// ==========================================================================================
// Function: mono_jit_info_table_find
// Address: 00de5090
// ==========================================================================================

undefined8 mono_jit_info_table_find(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_jit_info_get_method
// Address: 00de5098
// ==========================================================================================

undefined8 mono_jit_info_get_method(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_debug_il_offset_from_address
// Address: 00de50a0
// ==========================================================================================

undefined8 mono_debug_il_offset_from_address(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_set_is_debugger_attached
// Address: 00de50a8
// ==========================================================================================

void mono_set_is_debugger_attached(void)

{
  return;
}



// ==========================================================================================
// Function: mono_get_runtime_build_info
// Address: 00de50ac
// ==========================================================================================

void mono_get_runtime_build_info(void)

{
  FUN_00dc7118("0.0 (IL2CPP)");
  return;
}



// ==========================================================================================
// Function: mono_marshal_method_from_wrapper
// Address: 00de50b8
// ==========================================================================================

undefined8 mono_marshal_method_from_wrapper(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_jit_find_compiled_method_with_jit_info
// Address: 00de50c0
// ==========================================================================================

undefined8 mono_jit_find_compiled_method_with_jit_info(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_get_lmf_addr
// Address: 00de50c8
// ==========================================================================================

undefined8 mono_get_lmf_addr(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_set_lmf
// Address: 00de50d0
// ==========================================================================================

void mono_set_lmf(void)

{
  return;
}



// ==========================================================================================
// Function: mono_restore_context
// Address: 00de50dc
// ==========================================================================================

void mono_restore_context(void)

{
  return;
}



// ==========================================================================================
// Function: mono_find_prev_seq_point_for_native_offset
// Address: 00de50e0
// ==========================================================================================

undefined8 mono_find_prev_seq_point_for_native_offset(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_environment_exitcode_get
// Address: 00de50e8
// ==========================================================================================

undefined4 mono_environment_exitcode_get(void)

{
  return DAT_02108170;
}



// ==========================================================================================
// Function: mono_environment_exitcode_set
// Address: 00de50ec
// ==========================================================================================

void mono_environment_exitcode_set(undefined4 param_1)

{
  DAT_02108170 = param_1;
  return;
}



// ==========================================================================================
// Function: mono_get_string_class
// Address: 00de50f8
// ==========================================================================================

undefined8 mono_get_string_class(void)

{
  return *(undefined8 *)(PTR_DAT_01ff5418 + 0x90);
}



// ==========================================================================================
// Function: mono_type_is_generic_parameter
// Address: 00de5108
// ==========================================================================================

bool mono_type_is_generic_parameter(long param_1)

{
  uint uVar1;
  
  if ((*(uint *)(param_1 + 8) >> 0x1d & 1) != 0) {
    return false;
  }
  uVar1 = *(uint *)(param_1 + 8) >> 0x10 & 0xff;
  if (uVar1 == 0x13) {
    return true;
  }
  return uVar1 == 0x1e;
}



// ==========================================================================================
// Function: mono_type_size
// Address: 00de5138
// ==========================================================================================

void mono_type_size(undefined8 param_1,uint *param_2)

{
  uint extraout_w1;
  
  FUN_00e35a88();
  *param_2 = extraout_w1 & 0xff;
  return;
}



// ==========================================================================================
// Function: mono_metadata_generic_class_is_valuetype
// Address: 00de5154
// ==========================================================================================

uint mono_metadata_generic_class_is_valuetype(long *param_1)

{
  return *(uint *)(*param_1 + 8) >> 0x1f;
}



// ==========================================================================================
// Function: mono_domain_is_unloading
// Address: 00de5164
// ==========================================================================================

undefined8 mono_domain_is_unloading(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_get_byte_class
// Address: 00de516c
// ==========================================================================================

undefined8 mono_get_byte_class(void)

{
  return *(undefined8 *)(PTR_DAT_01ff5418 + 0x18);
}



// ==========================================================================================
// Function: mono_class_has_parent
// Address: 00de517c
// ==========================================================================================

uint mono_class_has_parent(void)

{
  uint uVar1;
  
  uVar1 = FUN_00dfd678();
  return uVar1 & 1;
}



// ==========================================================================================
// Function: mono_class_get_checked
// Address: 00de5190
// ==========================================================================================

undefined8 mono_class_get_checked(void)

{
  return 0;
}



// ==========================================================================================
// Function: mono_pal_init
// Address: 00e2f234
// ==========================================================================================

void mono_pal_init(void)

{
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1___ctor
// Address: 01981f78
// ==========================================================================================

void Mono_Security_ASN1___ctor(long param_1,undefined param_2)

{
  System_Object___ctor(param_1,0);
  *(undefined *)(param_1 + 0x10) = param_2;
  *(undefined8 *)(param_1 + 0x18) = 0;
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1___ctor
// Address: 01981fa4
// ==========================================================================================

void Mono_Security_ASN1___ctor(long param_1,undefined param_2,undefined8 param_3)

{
  System_Object___ctor(param_1,0);
  *(undefined *)(param_1 + 0x10) = param_2;
  *(undefined8 *)(param_1 + 0x18) = param_3;
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__Decode
// Address: 01982138
// ==========================================================================================

void Mono_Security_ASN1__Decode(undefined8 param_1,undefined8 param_2,int *param_3,int param_4)

{
  int iVar1;
  undefined *puVar2;
  undefined8 uVar3;
  byte bVar4;
  undefined8 uVar5;
  long lVar6;
  int local_5c;
  undefined8 local_58;
  int local_48;
  byte local_44 [4];
  
  uVar5 = param_1;
  if ((DAT_021015c0 & 1) == 0) {
    uVar5 = FUN_00db0bbc(PTR_Mono_Security_ASN1_TypeInfo_01fd27a8);
    DAT_021015c0 = 1;
  }
  puVar2 = PTR_Mono_Security_ASN1_TypeInfo_01fd27a8;
  local_44[0] = 0;
  local_48 = 0;
  local_58 = 0;
  iVar1 = *param_3;
  while (iVar1 < param_4 + -1) {
    uVar5 = Mono_Security_ASN1__DecodeTLV(uVar5,param_2,param_3,local_44,&local_48,&local_58);
    bVar4 = local_44[0];
    uVar3 = local_58;
    if (local_44[0] == 0) {
      iVar1 = *param_3;
    }
    else {
      lVar6 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      System_Object___ctor(lVar6,0);
      *(byte *)(lVar6 + 0x10) = bVar4;
      *(undefined8 *)(lVar6 + 0x18) = uVar3;
      uVar5 = Mono_Security_ASN1__Add(param_1,lVar6);
      iVar1 = local_48;
      if ((bVar4 >> 5 & 1) != 0) {
        local_5c = *param_3;
        uVar5 = Mono_Security_ASN1__Decode(lVar6,param_2,&local_5c,local_48 + local_5c);
      }
      iVar1 = iVar1 + *param_3;
      *param_3 = iVar1;
    }
  }
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__get_Count
// Address: 01982254
// ==========================================================================================

void Mono_Security_ASN1__get_Count(long param_1)

{
  long *plVar1;
  
  plVar1 = *(long **)(param_1 + 0x20);
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x01982268. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x288))(plVar1,*(undefined8 *)(*plVar1 + 0x290));
    return;
  }
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__get_Tag
// Address: 01982270
// ==========================================================================================

undefined Mono_Security_ASN1__get_Tag(long param_1)

{
  return *(undefined *)(param_1 + 0x10);
}



// ==========================================================================================
// Function: Mono_Security_ASN1__get_Value
// Address: 01982278
// ==========================================================================================

void Mono_Security_ASN1__get_Value(long *param_1)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  
  if ((DAT_021015bc & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_021015bc = 1;
  }
  lVar1 = param_1[3];
  if (lVar1 == 0) {
    (**(code **)(*param_1 + 0x178))(param_1,*(undefined8 *)(*param_1 + 0x180));
    lVar1 = param_1[3];
  }
  if (lVar1 != 0) {
    lVar1 = System_Array__Clone(lVar1,0);
    if (lVar1 != 0) {
      uVar3 = *(undefined8 *)PTR_byte___TypeInfo_01fbf258;
      lVar2 = thunk_FUN_00e11b18(lVar1,uVar3);
      if (lVar2 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(lVar1,uVar3);
      }
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_ASN1__set_Value
// Address: 01982308
// ==========================================================================================

void Mono_Security_ASN1__set_Value(long param_1,long param_2)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  undefined8 uVar4;
  
  if ((DAT_021015bd & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_021015bd = 1;
  }
  if (param_2 != 0) {
    lVar2 = System_Array__Clone(param_2,0);
    puVar1 = PTR_byte___TypeInfo_01fbf258;
    if (lVar2 == 0) {
      *(undefined8 *)(param_1 + 0x18) = 0;
    }
    else {
      uVar4 = *(undefined8 *)PTR_byte___TypeInfo_01fbf258;
      lVar3 = thunk_FUN_00e11b18(lVar2,uVar4);
      if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(lVar2,uVar4);
      }
      *(long *)(param_1 + 0x18) = lVar3;
      uVar4 = *(undefined8 *)puVar1;
      lVar3 = thunk_FUN_00e11b18(lVar2,uVar4);
      if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(lVar2,uVar4);
      }
    }
  }
  return;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__Add
// Address: 019823b0
// ==========================================================================================

long Mono_Security_ASN1__Add(long param_1,long param_2)

{
  long *plVar1;
  
  if ((DAT_021015be & 1) == 0) {
    FUN_00db0bbc(PTR_System_Collections_ArrayList_TypeInfo_01fd27b0);
    DAT_021015be = 1;
  }
  if (param_2 != 0) {
    plVar1 = *(long **)(param_1 + 0x20);
    if (plVar1 == (long *)0x0) {
      plVar1 = (long *)thunk_FUN_00e11c14(*(undefined8 *)
                                           PTR_System_Collections_ArrayList_TypeInfo_01fd27b0);
      System_Collections_ArrayList___ctor(plVar1,0);
      *(long **)(param_1 + 0x20) = plVar1;
      if (plVar1 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
    }
    (**(code **)(*plVar1 + 0x2e8))(plVar1,param_2,*(undefined8 *)(*plVar1 + 0x2f0));
  }
  return param_2;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__GetBytes
// Address: 0198243c
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x019829d8) */
/* WARNING: Removing unreachable block (ram,0x01982804) */

long Mono_Security_ASN1__GetBytes(long param_1)

{
  uint uVar1;
  byte bVar2;
  undefined uVar3;
  undefined uVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  int iVar8;
  int iVar9;
  long *plVar10;
  long *plVar11;
  code **ppcVar12;
  long *plVar13;
  long lVar14;
  long lVar15;
  long lVar16;
  ulong uVar17;
  int *piVar18;
  undefined uVar19;
  int iVar20;
  undefined8 uVar21;
  
  if ((DAT_021015bf & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Security_ASN1_TypeInfo_01fd27a8);
    FUN_00db0bbc(PTR_System_Collections_ArrayList_TypeInfo_01fd27b0);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_System_IDisposable_TypeInfo_01fbf6e0);
    FUN_00db0bbc(PTR_System_Collections_IEnumerator_TypeInfo_01fbf6e8);
    DAT_021015bf = 1;
  }
  plVar10 = *(long **)(param_1 + 0x20);
  if ((plVar10 != (long *)0x0) &&
     (iVar8 = (**(code **)(*plVar10 + 0x288))(plVar10,*(undefined8 *)(*plVar10 + 0x290)), 0 < iVar8)
     ) {
    plVar10 = (long *)thunk_FUN_00e11c14(*(undefined8 *)
                                          PTR_System_Collections_ArrayList_TypeInfo_01fd27b0);
    System_Collections_ArrayList___ctor(plVar10,0);
    plVar11 = *(long **)(param_1 + 0x20);
    if (plVar11 != (long *)0x0) {
      plVar11 = (long *)(**(code **)(*plVar11 + 0x348))(plVar11,*(undefined8 *)(*plVar11 + 0x350));
      puVar7 = PTR_Mono_Security_ASN1_TypeInfo_01fd27a8;
      puVar5 = PTR_System_Collections_IEnumerator_TypeInfo_01fbf6e8;
      if (plVar11 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 019829d4 to 019829d7 has its CatchHandler @ 019829e0 */
        FUN_00db0de4();
      }
      iVar8 = 0;
      do {
        lVar16 = *plVar11;
        lVar15 = *(long *)puVar5;
        uVar17 = (ulong)*(ushort *)(lVar16 + 0x12e);
        if (uVar17 != 0) {
          piVar18 = (int *)(*(long *)(lVar16 + 0xb0) + 8);
          do {
            if (*(long *)(piVar18 + -2) == lVar15) {
              ppcVar12 = (code **)(lVar16 + (long)*piVar18 * 0x10 + 0x138);
              goto LAB_01982560;
            }
            uVar17 = uVar17 - 1;
            piVar18 = piVar18 + 4;
          } while (uVar17 != 0);
        }
                    /* try { // try from 01982544 to 0198256b has its CatchHandler @ 01982a00 */
        ppcVar12 = (code **)FUN_00e0dcd4(plVar11,lVar15,0);
LAB_01982560:
        uVar17 = (**ppcVar12)(plVar11,ppcVar12[1]);
        puVar6 = PTR_System_IDisposable_TypeInfo_01fbf6e0;
        if ((uVar17 & 1) == 0) {
          plVar11 = (long *)thunk_FUN_00e11b18(plVar11,*(undefined8 *)
                                                        PTR_System_IDisposable_TypeInfo_01fbf6e0);
          if (plVar11 == (long *)0x0) goto LAB_019827f8;
          lVar15 = *plVar11;
          uVar17 = (ulong)*(ushort *)(lVar15 + 0x12e);
          if (uVar17 == 0) goto LAB_019826d4;
          piVar18 = (int *)(*(long *)(lVar15 + 0xb0) + 8);
          goto LAB_019826bc;
        }
        lVar16 = *plVar11;
        lVar15 = *(long *)puVar5;
        uVar17 = (ulong)*(ushort *)(lVar16 + 0x12e);
        if (uVar17 != 0) {
          piVar18 = (int *)(*(long *)(lVar16 + 0xb0) + 8);
          do {
            if (*(long *)(piVar18 + -2) == lVar15) {
              ppcVar12 = (code **)(lVar16 + (long)(*piVar18 + 1) * 0x10 + 0x138);
              goto LAB_019825c0;
            }
            uVar17 = uVar17 - 1;
            piVar18 = piVar18 + 4;
          } while (uVar17 != 0);
        }
                    /* try { // try from 019825a0 to 019825cb has its CatchHandler @ 019829fc */
        ppcVar12 = (code **)FUN_00e0dcd4(plVar11,lVar15,1);
LAB_019825c0:
        plVar13 = (long *)(**ppcVar12)(plVar11,ppcVar12[1]);
        if (plVar13 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 019829bc to 019829bf has its CatchHandler @ 01982a04 */
          FUN_00db0de4();
        }
        lVar15 = *plVar13;
        bVar2 = *(byte *)(*(long *)puVar7 + 0x130);
        if ((*(byte *)(lVar15 + 0x130) < bVar2) ||
           (*(long *)(*(long *)(lVar15 + 200) + (ulong)bVar2 * 8 + -8) != *(long *)puVar7)) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 019829b4 to 019829b7 has its CatchHandler @ 01982a04 */
          FUN_00db1180();
        }
                    /* try { // try from 01982600 to 01982603 has its CatchHandler @ 019829e4 */
        lVar15 = (**(code **)(lVar15 + 0x178))(plVar13,*(undefined8 *)(lVar15 + 0x180));
        if (plVar10 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 019829c0 to 019829c3 has its CatchHandler @ 019829ec */
          FUN_00db0de4();
        }
                    /* try { // try from 01982618 to 01982623 has its CatchHandler @ 019829e8 */
        (**(code **)(*plVar10 + 0x2e8))(plVar10,lVar15,*(undefined8 *)(*plVar10 + 0x2f0));
        if (lVar15 == 0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 019829b8 to 019829bb has its CatchHandler @ 019829f8 */
          FUN_00db0de4();
        }
        iVar8 = iVar8 + *(int *)(lVar15 + 0x18);
      } while( true );
    }
    goto LAB_019828b0;
  }
  lVar15 = *(long *)(param_1 + 0x18);
LAB_01982638:
  if (lVar15 == 0) {
    lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,2);
    uVar19 = 0;
  }
  else {
    uVar17 = *(ulong *)(lVar15 + 0x18);
    iVar8 = (int)uVar17;
    if (iVar8 < 0x80) {
      lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8 + 2);
      Method_System_Buffer_BlockCopy(lVar15,0,lVar16,2,uVar17 & 0xffffffff,0);
    }
    else {
      uVar19 = (undefined)uVar17;
      if (iVar8 < 0x100) {
        lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8 + 3);
        Method_System_Buffer_BlockCopy(lVar15,0,lVar16,3,uVar17 & 0xffffffff,0);
        if (lVar16 == 0) goto LAB_019828b0;
        if (*(uint *)(lVar16 + 0x18) < 3) goto LAB_019829d0;
        *(undefined *)(lVar16 + 0x22) = uVar19;
        iVar8 = 0x81;
      }
      else {
        uVar3 = (undefined)(uVar17 >> 8);
        if (iVar8 < 0x10000) {
          lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8 + 4);
          Method_System_Buffer_BlockCopy(lVar15,0,lVar16,4,uVar17 & 0xffffffff,0);
          if (lVar16 == 0) goto LAB_019828b0;
          if ((*(uint *)(lVar16 + 0x18) < 3) ||
             (*(undefined *)(lVar16 + 0x22) = uVar3, *(uint *)(lVar16 + 0x18) == 3))
          goto LAB_019829d0;
          *(undefined *)(lVar16 + 0x23) = uVar19;
          iVar8 = 0x82;
        }
        else {
          uVar4 = (undefined)(uVar17 >> 0x10);
          if (iVar8 < 0x1000000) {
            lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8 + 5);
            Method_System_Buffer_BlockCopy(lVar15,0,lVar16,5,uVar17 & 0xffffffff,0);
            if (lVar16 == 0) goto LAB_019828b0;
            uVar1 = *(uint *)(lVar16 + 0x18);
            if (((uVar1 < 3) || (*(undefined *)(lVar16 + 0x22) = uVar4, uVar1 == 3)) ||
               (*(undefined *)(lVar16 + 0x23) = uVar3, uVar1 < 5)) goto LAB_019829d0;
            *(undefined *)(lVar16 + 0x24) = uVar19;
            iVar8 = 0x83;
          }
          else {
            lVar16 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8 + 6);
            Method_System_Buffer_BlockCopy(lVar15,0,lVar16,6,uVar17 & 0xffffffff,0);
            if (lVar16 == 0) goto LAB_019828b0;
            uVar1 = *(uint *)(lVar16 + 0x18);
            if (((uVar1 < 3) || (*(char *)(lVar16 + 0x22) = (char)(uVar17 >> 0x18), uVar1 == 3)) ||
               ((*(undefined *)(lVar16 + 0x23) = uVar4, uVar1 < 5 ||
                (*(undefined *)(lVar16 + 0x24) = uVar3, uVar1 == 5)))) goto LAB_019829d0;
            *(undefined *)(lVar16 + 0x25) = uVar19;
            iVar8 = 0x84;
          }
        }
      }
    }
    uVar19 = (undefined)iVar8;
    if (*(long *)(param_1 + 0x18) == 0) {
      *(long *)(param_1 + 0x18) = lVar15;
    }
  }
  if (lVar16 != 0) {
    if ((*(int *)(lVar16 + 0x18) != 0) &&
       (*(undefined *)(lVar16 + 0x20) = *(undefined *)(param_1 + 0x10), *(int *)(lVar16 + 0x18) != 1
       )) {
      *(undefined *)(lVar16 + 0x21) = uVar19;
      return lVar16;
    }
LAB_019829d0:
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
  goto LAB_019828b0;
  while( true ) {
    uVar17 = uVar17 - 1;
    piVar18 = piVar18 + 4;
    if (uVar17 == 0) break;
LAB_019826bc:
    if (*(long *)(piVar18 + -2) == *(long *)puVar6) {
      ppcVar12 = (code **)(lVar15 + (long)*piVar18 * 0x10 + 0x138);
      goto LAB_019827ec;
    }
  }
LAB_019826d4:
  ppcVar12 = (code **)FUN_00e0dcd4(plVar11,*(long *)puVar6,0);
LAB_019827ec:
  (**ppcVar12)(plVar11,ppcVar12[1]);
LAB_019827f8:
  puVar5 = PTR_byte___TypeInfo_01fbf258;
  lVar15 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,iVar8);
  plVar11 = *(long **)(param_1 + 0x20);
  if (plVar11 != (long *)0x0) {
    iVar20 = 0;
    iVar8 = 0;
    do {
      iVar9 = (**(code **)(*plVar11 + 0x288))(plVar11,*(undefined8 *)(*plVar11 + 0x290));
      if (iVar9 <= iVar8) goto LAB_01982638;
      if ((plVar10 == (long *)0x0) ||
         (lVar16 = (**(code **)(*plVar10 + 0x2c8))(plVar10,iVar8,*(undefined8 *)(*plVar10 + 0x2d0)),
         lVar16 == 0)) break;
      uVar21 = *(undefined8 *)puVar5;
      lVar14 = thunk_FUN_00e11b18(lVar16,uVar21);
      if (lVar14 == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(lVar16,uVar21);
      }
      Method_System_Buffer_BlockCopy(lVar14,0,lVar15,iVar20,*(undefined4 *)(lVar14 + 0x18),0);
      plVar11 = *(long **)(param_1 + 0x20);
      iVar8 = iVar8 + 1;
      iVar20 = iVar20 + *(int *)(lVar14 + 0x18);
    } while (plVar11 != (long *)0x0);
  }
LAB_019828b0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_ASN1__DecodeTLV
// Address: 01982ac0
// ==========================================================================================

void Mono_Security_ASN1__DecodeTLV
               (undefined8 param_1,long param_2,uint *param_3,undefined *param_4,uint *param_5,
               undefined8 *param_6)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  undefined8 uVar4;
  uint uVar5;
  uint uVar6;
  
  if ((DAT_021015c1 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_021015c1 = 1;
  }
  uVar2 = *param_3;
  *param_3 = uVar2 + 1;
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (uVar2 < *(uint *)(param_2 + 0x18)) {
    *param_4 = *(undefined *)(param_2 + (int)uVar2 + 0x20);
    uVar5 = *param_3;
    *param_3 = uVar5 + 1;
    uVar2 = *(uint *)(param_2 + 0x18);
    if (uVar5 < uVar2) {
      bVar1 = *(byte *)(param_2 + (int)uVar5 + 0x20);
      uVar5 = (uint)bVar1;
      *param_5 = (uint)bVar1;
      if ((char)bVar1 < '\0') {
        uVar6 = bVar1 & 0x7f;
        *param_5 = 0;
        if ((bVar1 & 0x7f) == 0) {
          uVar5 = 0;
        }
        else {
          uVar5 = 0;
          do {
            uVar3 = *param_3;
            *param_3 = uVar3 + 1;
            if (uVar2 <= uVar3) goto LAB_01982bdc;
            uVar6 = uVar6 - 1;
            uVar5 = (uint)*(byte *)(param_2 + (int)uVar3 + 0x20) | uVar5 << 8;
            *param_5 = uVar5;
          } while (uVar6 != 0);
        }
      }
      uVar4 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,uVar5);
      *param_6 = uVar4;
      Method_System_Buffer_BlockCopy(param_2,*param_3,uVar4,0,*param_5,0);
      return;
    }
  }
LAB_01982bdc:
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: Mono_Security_ASN1__get_Item
// Address: 01982be4
// ==========================================================================================

long * Mono_Security_ASN1__get_Item(long param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  long *plVar3;
  
  if ((DAT_021015c2 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Security_ASN1_TypeInfo_01fd27a8);
    DAT_021015c2 = 1;
  }
  plVar3 = *(long **)(param_1 + 0x20);
  if (plVar3 != (long *)0x0) {
                    /* try { // try from 01982c28 to 01982c2b has its CatchHandler @ 01982c94 */
    iVar2 = (**(code **)(*plVar3 + 0x288))(plVar3,*(undefined8 *)(*plVar3 + 0x290));
    if (param_2 < iVar2) {
      plVar3 = *(long **)(param_1 + 0x20);
      if (plVar3 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
                    /* try { // try from 01982c8c to 01982c8f has its CatchHandler @ 01982c90 */
        FUN_00db0de4();
      }
                    /* try { // try from 01982c48 to 01982c8b has its CatchHandler @ 01982c98 */
      plVar3 = (long *)(**(code **)(*plVar3 + 0x2c8))
                                 (plVar3,param_2,*(undefined8 *)(*plVar3 + 0x2d0));
      if (plVar3 != (long *)0x0) {
        bVar1 = *(byte *)(*(long *)PTR_Mono_Security_ASN1_TypeInfo_01fd27a8 + 0x130);
        if ((*(byte *)(*plVar3 + 0x130) < bVar1) ||
           (*(long *)(*(long *)(*plVar3 + 200) + (ulong)bVar1 * 8 + -8) !=
            *(long *)PTR_Mono_Security_ASN1_TypeInfo_01fd27a8)) {
                    /* WARNING: Subroutine does not return */
          FUN_00db1180();
        }
      }
    }
    else {
      plVar3 = (long *)0x0;
    }
  }
  return plVar3;
}



// ==========================================================================================
// Function: Mono_Security_ASN1__ToString
// Address: 01982d14
// ==========================================================================================

void Mono_Security_ASN1__ToString(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  ulong uVar9;
  undefined4 local_44;
  
  puVar2 = PTR_StringLiteral_6090_01fc7e48;
  puVar1 = PTR_System_Text_StringBuilder_TypeInfo_01fc08f0;
  if ((DAT_021015c3 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Array_Empty_object_01fc32f8);
    FUN_00db0bbc(PTR_int_TypeInfo_01fc0108);
    FUN_00db0bbc(PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    FUN_00db0bbc(PTR_StringLiteral_5296_01fd27b8);
    FUN_00db0bbc(PTR_StringLiteral_6005_01fd27c0);
    FUN_00db0bbc(PTR_StringLiteral_3990_01fd27c8);
    FUN_00db0bbc(PTR_StringLiteral_9758_01fd27d0);
    FUN_00db0bbc(PTR_StringLiteral_6090_01fc7e48);
    DAT_021015c3 = 1;
  }
  plVar4 = (long *)thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Text_StringBuilder___ctor(plVar4,0);
  uVar5 = System_Byte__ToString(param_1 + 0x10,*(undefined8 *)puVar2,0);
  uVar6 = System_Environment__get_NewLine(0);
  if (plVar4 != (long *)0x0) {
    System_Text_StringBuilder__AppendFormat
              (plVar4,*(undefined8 *)PTR_StringLiteral_5296_01fd27b8,uVar5,uVar6,0);
    lVar7 = Mono_Security_ASN1__get_Value(param_1);
    puVar3 = PTR_StringLiteral_3990_01fd27c8;
    puVar1 = PTR_StringLiteral_6005_01fd27c0;
    if (lVar7 != 0) {
      local_44 = (undefined4)*(undefined8 *)(lVar7 + 0x18);
      uVar5 = thunk_FUN_00e11868(*(undefined8 *)PTR_int_TypeInfo_01fc0108,&local_44);
      uVar6 = System_Environment__get_NewLine(0);
      System_Text_StringBuilder__AppendFormat(plVar4,*(undefined8 *)puVar3,uVar5,uVar6,0);
      System_Text_StringBuilder__Append(plVar4,*(undefined8 *)puVar1,0);
      uVar5 = System_Environment__get_NewLine(0);
      System_Text_StringBuilder__Append(plVar4,uVar5,0);
      lVar7 = Mono_Security_ASN1__get_Value(param_1);
      puVar3 = PTR_StringLiteral_9758_01fd27d0;
      puVar1 = PTR_Method_System_Array_Empty_object_01fc32f8;
      if (lVar7 != 0) {
        uVar9 = 0;
        do {
          if ((long)*(int *)(lVar7 + 0x18) <= (long)uVar9) {
            (**(code **)(*plVar4 + 0x168))(plVar4,*(undefined8 *)(*plVar4 + 0x170));
            return;
          }
          lVar7 = Mono_Security_ASN1__get_Value(param_1);
          if (lVar7 == 0) break;
          if (*(uint *)(lVar7 + 0x18) <= uVar9) {
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          uVar5 = System_Byte__ToString(lVar7 + uVar9 + 0x20,*(undefined8 *)puVar2,0);
          System_Text_StringBuilder__AppendFormat(plVar4,*(undefined8 *)puVar3,uVar5,0);
          uVar9 = uVar9 + 1;
          if ((uVar9 & 0xf) == 0) {
            uVar5 = System_Environment__get_NewLine(0);
            lVar8 = *(long *)puVar1;
            lVar7 = *(long *)(lVar8 + 0x38);
            if (lVar7 == 0) {
              FUN_00e0dc2c(lVar8);
              lVar7 = *(long *)(lVar8 + 0x38);
            }
            lVar7 = *(long *)(lVar7 + 0x10);
            if ((*(byte *)(lVar7 + 0x135) & 1) == 0) {
              lVar7 = FUN_00e0dbd0();
            }
            if (*(int *)(lVar7 + 0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            lVar7 = *(long *)(*(long *)(lVar8 + 0x38) + 0x10);
            if ((*(byte *)(lVar7 + 0x135) & 1) == 0) {
              lVar7 = FUN_00e0dbd0();
            }
            Method_System_Text_StringBuilder_AppendFormat
                      (plVar4,uVar5,**(undefined8 **)(lVar7 + 0xb8),0);
          }
          lVar7 = Mono_Security_ASN1__get_Value(param_1);
        } while (lVar7 != 0);
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_ASN1Convert__FromInt32
// Address: 01982fa8
// ==========================================================================================

long Mono_Security_ASN1Convert__FromInt32(undefined4 param_1)

{
  uint uVar1;
  uint uVar2;
  undefined *puVar3;
  long lVar4;
  long lVar5;
  long lVar6;
  uint uVar7;
  uint uVar8;
  undefined4 local_24;
  
  puVar3 = PTR_Method_System_Array_Reverse_byte_01fd27d8;
  if ((DAT_021015c4 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Security_ASN1_TypeInfo_01fd27a8);
    FUN_00db0bbc(PTR_Method_System_Array_Reverse_byte_01fd27d8);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_021015c4 = 1;
  }
  local_24 = param_1;
  lVar4 = Mono_Security_BitConverterLE__GetUIntBytes(&local_24);
  Method_System_Array_Reverse_byte(lVar4,*(undefined8 *)puVar3);
  if (lVar4 == 0) {
LAB_01983110:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar2 = *(uint *)(lVar4 + 0x18);
  uVar1 = uVar2 & ((int)uVar2 >> 0x1f ^ 0xffffffffU);
  uVar8 = uVar1;
  if (0 < (int)uVar2) {
    uVar7 = 0;
    do {
      if (uVar2 == uVar7) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar8 = uVar7;
    } while ((*(char *)(lVar4 + (int)uVar7 + 0x20) == '\0') &&
            (uVar7 = uVar7 + 1, uVar8 = uVar1, uVar1 != uVar7));
  }
  lVar5 = thunk_FUN_00e11c14(*(undefined8 *)PTR_Mono_Security_ASN1_TypeInfo_01fd27a8);
  System_Object___ctor(lVar5,0);
  *(undefined *)(lVar5 + 0x10) = 2;
  *(undefined8 *)(lVar5 + 0x18) = 0;
  if (uVar8 == 4) {
    lVar4 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,1);
  }
  else if (uVar8 != 0) {
    lVar6 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,4 - uVar8);
    if (lVar6 == 0) goto LAB_01983110;
    Method_System_Buffer_BlockCopy(lVar4,uVar8,lVar6,0,*(undefined4 *)(lVar6 + 0x18),0);
    lVar4 = lVar6;
  }
  Mono_Security_ASN1__set_Value(lVar5,lVar4);
  return lVar5;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetBytes
// Address: 01983114
// ==========================================================================================

void Mono_Security_BitConverterLE__GetBytes(undefined4 param_1)

{
  undefined4 local_4;
  
  local_4 = param_1;
  Mono_Security_BitConverterLE__GetUIntBytes(&local_4);
  return;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetUIntBytes
// Address: 019834c4
// ==========================================================================================

void Mono_Security_BitConverterLE__GetUIntBytes(undefined *param_1)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  
  puVar2 = PTR_byte___TypeInfo_01fbf258;
  if ((DAT_021015c6 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_021015c6 = 1;
  }
  lVar3 = FUN_00db0c30(*(undefined8 *)puVar2,4);
  if (lVar3 != 0) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if ((((uVar1 != 0) && (*(undefined *)(lVar3 + 0x20) = *param_1, uVar1 != 1)) &&
        (*(undefined *)(lVar3 + 0x21) = param_1[1], 2 < uVar1)) &&
       (*(undefined *)(lVar3 + 0x22) = param_1[2], uVar1 != 3)) {
      *(undefined *)(lVar3 + 0x23) = param_1[3];
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_Cryptography_CryptoConvert__ToHex
// Address: 0198355c
// ==========================================================================================

undefined8 Mono_Security_Cryptography_CryptoConvert__ToHex(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  long *plVar3;
  undefined8 uVar4;
  ulong uVar5;
  ulong uVar6;
  undefined local_34 [4];
  
  if ((DAT_021015c7 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    FUN_00db0bbc(PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    FUN_00db0bbc(PTR_StringLiteral_6090_01fc7e48);
    DAT_021015c7 = 1;
  }
  local_34[0] = 0;
  if (param_1 == 0) {
    uVar4 = 0;
  }
  else {
    plVar3 = (long *)thunk_FUN_00e11c14(*(undefined8 *)
                                         PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    System_Text_StringBuilder___ctor(plVar3,*(int *)(param_1 + 0x18) << 1,0);
    puVar2 = PTR_StringLiteral_6090_01fc7e48;
    puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
    if ((int)*(ulong *)(param_1 + 0x18) < 1) {
      if (plVar3 == (long *)0x0) {
LAB_01983690:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
    }
    else {
      uVar6 = 0;
      uVar5 = *(ulong *)(param_1 + 0x18) & 0xffffffff;
      do {
        if (uVar5 <= uVar6) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        local_34[0] = *(undefined *)(param_1 + 0x20 + uVar6);
        if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar4 = System_Globalization_CultureInfo__get_InvariantCulture(0);
        uVar4 = System_Byte__ToString(local_34,*(undefined8 *)puVar2,uVar4,0);
        if (plVar3 == (long *)0x0) goto LAB_01983690;
        System_Text_StringBuilder__Append(plVar3,uVar4,0);
        uVar5 = (ulong)*(uint *)(param_1 + 0x18);
        uVar6 = uVar6 + 1;
      } while ((long)uVar6 < (long)(int)*(uint *)(param_1 + 0x18));
    }
    uVar4 = (**(code **)(*plVar3 + 0x168))(plVar3,*(undefined8 *)(*plVar3 + 0x170));
  }
  return uVar4;
}



// ==========================================================================================
// Function: Mono_Runtime___cctor
// Address: 01984ea8
// ==========================================================================================

void Mono_Runtime___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_Mono_Runtime_TypeInfo_01fd28e0;
  puVar1 = PTR_object_TypeInfo_01fbfcc0;
  if ((DAT_021015db & 1) == 0) {
    FUN_00db0bbc(PTR_object_TypeInfo_01fbfcc0);
    FUN_00db0bbc(PTR_Mono_Runtime_TypeInfo_01fd28e0);
    DAT_021015db = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar3,0);
  **(undefined8 **)(*(long *)puVar2 + 0xb8) = uVar3;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle___ctor
// Address: 01984f18
// ==========================================================================================

void Mono_RuntimeClassHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  *param_1 = param_2;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle___ctor
// Address: 01984f20
// ==========================================================================================

void Mono_RuntimeClassHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = System_IntPtr__op_Explicit(param_2,0);
  *param_1 = uVar1;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle__get_Value
// Address: 01984f40
// ==========================================================================================

undefined8 Mono_RuntimeClassHandle__get_Value(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle__Equals
// Address: 01984f48
// ==========================================================================================

bool Mono_RuntimeClassHandle__Equals(long *param_1,long *param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  ulong uVar5;
  long *plVar6;
  long lVar7;
  long local_38;
  
  if ((DAT_021015dc & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_RuntimeClassHandle_TypeInfo_01fd28e8);
    FUN_00db0bbc(PTR_System_Type_TypeInfo_01fc3680);
    DAT_021015dc = 1;
  }
  puVar2 = PTR_Mono_RuntimeClassHandle_TypeInfo_01fd28e8;
  puVar1 = PTR_System_Type_TypeInfo_01fc3680;
  if (param_2 != (long *)0x0) {
    local_38 = *param_1;
    uVar3 = thunk_FUN_00e11868(*(undefined8 *)PTR_Mono_RuntimeClassHandle_TypeInfo_01fd28e8,
                               &local_38);
    uVar3 = System_Object__GetType(uVar3,0);
    uVar4 = System_Object__GetType(param_2,0);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    uVar5 = System_Type__op_Inequality(uVar3,uVar4,0);
    if ((uVar5 & 1) == 0) {
      if (*(long *)(*param_2 + 0x40) == *(long *)(*(long *)puVar2 + 0x40)) {
        lVar7 = *param_1;
        plVar6 = (long *)thunk_FUN_00e11d68(param_2);
        return lVar7 == *plVar6;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db1180(param_2);
    }
  }
  return false;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle__GetHashCode
// Address: 0198504c
// ==========================================================================================

void Mono_RuntimeClassHandle__GetHashCode(undefined8 *param_1)

{
  undefined8 local_8;
  
  local_8 = System_IntPtr__op_Explicit(*param_1,0);
  System_IntPtr__GetHashCode(&local_8,0);
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle__GetTypeFromClass
// Address: 01985074
// ==========================================================================================

long Mono_RuntimeClassHandle__GetTypeFromClass(long param_1)

{
  return param_1 + 0x20;
}



// ==========================================================================================
// Function: Mono_RuntimeClassHandle__GetTypeHandle
// Address: 01985078
// ==========================================================================================

void Mono_RuntimeClassHandle__GetTypeHandle(undefined8 *param_1)

{
  FUN_00de399c(*param_1);
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeRemoteClassHandle__get_ProxyClass
// Address: 01985080
// ==========================================================================================

undefined8 Mono_RuntimeRemoteClassHandle__get_ProxyClass(long *param_1)

{
  if (*param_1 != 0) {
    return *(undefined8 *)(*param_1 + 0x10);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_RuntimeGenericParamInfoHandle___ctor
// Address: 0198509c
// ==========================================================================================

void Mono_RuntimeGenericParamInfoHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = System_IntPtr__op_Explicit(param_2,0);
  *param_1 = uVar1;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeGenericParamInfoHandle__get_Constraints
// Address: 019850bc
// ==========================================================================================

long * Mono_RuntimeGenericParamInfoHandle__get_Constraints(long *param_1)

{
  undefined *puVar1;
  uint uVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  long lVar8;
  
  puVar1 = PTR_System_Type___TypeInfo_01fc6060;
  if ((DAT_021015dd & 1) == 0) {
    FUN_00db0bbc(PTR_System_Type___TypeInfo_01fc6060);
    FUN_00db0bbc(PTR_System_Type_TypeInfo_01fc3680);
    DAT_021015dd = 1;
  }
  uVar2 = Mono_RuntimeGenericParamInfoHandle__GetConstraintsCount(param_1);
  plVar3 = (long *)FUN_00db0c30(*(undefined8 *)puVar1,(ulong)uVar2);
  puVar1 = PTR_System_Type_TypeInfo_01fc3680;
  if (0 < (int)uVar2) {
    uVar7 = 0;
    lVar8 = 0x20;
    do {
      if (*param_1 == 0) {
LAB_019851d8:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      uVar4 = FUN_00de399c(*(undefined8 *)(lVar8 + *(long *)(*param_1 + 0x18) + -0x20));
      if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar1);
      }
      lVar5 = System_Type__GetTypeFromHandle(uVar4,0);
      if (plVar3 == (long *)0x0) goto LAB_019851d8;
      if ((lVar5 != 0) &&
         (lVar6 = thunk_FUN_00e11b18(lVar5,*(undefined8 *)(*plVar3 + 0x40)), lVar6 == 0)) {
        uVar4 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar4,0);
      }
      if (*(uint *)(plVar3 + 3) <= uVar7) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar7 = uVar7 + 1;
      *(long *)((long)plVar3 + lVar8) = lVar5;
      lVar8 = lVar8 + 8;
    } while (uVar2 != uVar7);
  }
  return plVar3;
}



// ==========================================================================================
// Function: Mono_RuntimeGenericParamInfoHandle__GetConstraints
// Address: 019850c0
// ==========================================================================================

long * Mono_RuntimeGenericParamInfoHandle__GetConstraints(long *param_1)

{
  undefined *puVar1;
  uint uVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  long lVar8;
  
  puVar1 = PTR_System_Type___TypeInfo_01fc6060;
  if ((DAT_021015dd & 1) == 0) {
    FUN_00db0bbc(PTR_System_Type___TypeInfo_01fc6060);
    FUN_00db0bbc(PTR_System_Type_TypeInfo_01fc3680);
    DAT_021015dd = 1;
  }
  uVar2 = Mono_RuntimeGenericParamInfoHandle__GetConstraintsCount(param_1);
  plVar3 = (long *)FUN_00db0c30(*(undefined8 *)puVar1,(ulong)uVar2);
  puVar1 = PTR_System_Type_TypeInfo_01fc3680;
  if (0 < (int)uVar2) {
    uVar7 = 0;
    lVar8 = 0x20;
    do {
      if (*param_1 == 0) {
LAB_019851d8:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      uVar4 = FUN_00de399c(*(undefined8 *)(lVar8 + *(long *)(*param_1 + 0x18) + -0x20));
      if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar1);
      }
      lVar5 = System_Type__GetTypeFromHandle(uVar4,0);
      if (plVar3 == (long *)0x0) goto LAB_019851d8;
      if ((lVar5 != 0) &&
         (lVar6 = thunk_FUN_00e11b18(lVar5,*(undefined8 *)(*plVar3 + 0x40)), lVar6 == 0)) {
        uVar4 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
        FUN_00db0cb0(uVar4,0);
      }
      if (*(uint *)(plVar3 + 3) <= uVar7) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      uVar7 = uVar7 + 1;
      *(long *)((long)plVar3 + lVar8) = lVar5;
      lVar8 = lVar8 + 8;
    } while (uVar2 != uVar7);
  }
  return plVar3;
}



// ==========================================================================================
// Function: Mono_RuntimeGenericParamInfoHandle__get_Attributes
// Address: 019851ec
// ==========================================================================================

undefined2 Mono_RuntimeGenericParamInfoHandle__get_Attributes(long *param_1)

{
  if (*param_1 != 0) {
    return *(undefined2 *)(*param_1 + 0x10);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_RuntimeGenericParamInfoHandle__GetConstraintsCount
// Address: 01985208
// ==========================================================================================

int Mono_RuntimeGenericParamInfoHandle__GetConstraintsCount(long *param_1)

{
  int iVar1;
  long *plVar2;
  
  if (*param_1 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  plVar2 = *(long **)(*param_1 + 0x18);
  if (plVar2 == (long *)0x0) {
    iVar1 = 0;
  }
  else {
    iVar1 = 0;
    do {
      if (*plVar2 == 0) {
        return iVar1;
      }
      plVar2 = plVar2 + 1;
      iVar1 = iVar1 + 1;
    } while (plVar2 != (long *)0x0);
  }
  return iVar1;
}



// ==========================================================================================
// Function: Mono_RuntimeEventHandle___ctor
// Address: 01985248
// ==========================================================================================

void Mono_RuntimeEventHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  *param_1 = param_2;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeEventHandle__get_Value
// Address: 01985250
// ==========================================================================================

undefined8 Mono_RuntimeEventHandle__get_Value(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: Mono_RuntimeEventHandle__Equals
// Address: 01985258
// ==========================================================================================

uint Mono_RuntimeEventHandle__Equals(undefined8 *param_1,long *param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined8 *puVar7;
  undefined8 local_38;
  
  if ((DAT_021015de & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_RuntimeEventHandle_TypeInfo_01fd28f0);
    FUN_00db0bbc(PTR_System_Type_TypeInfo_01fc3680);
    DAT_021015de = 1;
  }
  puVar2 = PTR_Mono_RuntimeEventHandle_TypeInfo_01fd28f0;
  puVar1 = PTR_System_Type_TypeInfo_01fc3680;
  if (param_2 != (long *)0x0) {
    local_38 = *param_1;
    uVar4 = thunk_FUN_00e11868(*(undefined8 *)PTR_Mono_RuntimeEventHandle_TypeInfo_01fd28f0,
                               &local_38);
    uVar4 = System_Object__GetType(uVar4,0);
    uVar5 = System_Object__GetType(param_2,0);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    uVar6 = System_Type__op_Inequality(uVar4,uVar5,0);
    if ((uVar6 & 1) == 0) {
      if (*(long *)(*param_2 + 0x40) != *(long *)(*(long *)puVar2 + 0x40)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(param_2);
      }
      uVar4 = *param_1;
      puVar7 = (undefined8 *)thunk_FUN_00e11d68(param_2);
      uVar3 = System_IntPtr__op_Equality(uVar4,*puVar7,0);
      goto LAB_01985344;
    }
  }
  uVar3 = 0;
LAB_01985344:
  return uVar3 & 1;
}



// ==========================================================================================
// Function: Mono_RuntimeEventHandle__GetHashCode
// Address: 01985364
// ==========================================================================================

void Mono_RuntimeEventHandle__GetHashCode(undefined8 param_1)

{
  System_IntPtr__GetHashCode(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_RuntimePropertyHandle___ctor
// Address: 0198536c
// ==========================================================================================

void Mono_RuntimePropertyHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  *param_1 = param_2;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimePropertyHandle__get_Value
// Address: 01985374
// ==========================================================================================

undefined8 Mono_RuntimePropertyHandle__get_Value(undefined8 *param_1)

{
  return *param_1;
}



// ==========================================================================================
// Function: Mono_RuntimePropertyHandle__Equals
// Address: 0198537c
// ==========================================================================================

uint Mono_RuntimePropertyHandle__Equals(undefined8 *param_1,long *param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined8 *puVar7;
  undefined8 local_38;
  
  if ((DAT_021015df & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_RuntimePropertyHandle_TypeInfo_01fd28f8);
    FUN_00db0bbc(PTR_System_Type_TypeInfo_01fc3680);
    DAT_021015df = 1;
  }
  puVar2 = PTR_Mono_RuntimePropertyHandle_TypeInfo_01fd28f8;
  puVar1 = PTR_System_Type_TypeInfo_01fc3680;
  if (param_2 != (long *)0x0) {
    local_38 = *param_1;
    uVar4 = thunk_FUN_00e11868(*(undefined8 *)PTR_Mono_RuntimePropertyHandle_TypeInfo_01fd28f8,
                               &local_38);
    uVar4 = System_Object__GetType(uVar4,0);
    uVar5 = System_Object__GetType(param_2,0);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    uVar6 = System_Type__op_Inequality(uVar4,uVar5,0);
    if ((uVar6 & 1) == 0) {
      if (*(long *)(*param_2 + 0x40) != *(long *)(*(long *)puVar2 + 0x40)) {
                    /* WARNING: Subroutine does not return */
        FUN_00db1180(param_2);
      }
      uVar4 = *param_1;
      puVar7 = (undefined8 *)thunk_FUN_00e11d68(param_2);
      uVar3 = System_IntPtr__op_Equality(uVar4,*puVar7,0);
      goto LAB_01985468;
    }
  }
  uVar3 = 0;
LAB_01985468:
  return uVar3 & 1;
}



// ==========================================================================================
// Function: Mono_RuntimePropertyHandle__GetHashCode
// Address: 01985488
// ==========================================================================================

void Mono_RuntimePropertyHandle__GetHashCode(undefined8 param_1)

{
  System_IntPtr__GetHashCode(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeGPtrArrayHandle___ctor
// Address: 01985490
// ==========================================================================================

void Mono_RuntimeGPtrArrayHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = System_IntPtr__op_Explicit(param_2,0);
  *param_1 = uVar1;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeGPtrArrayHandle__get_Length
// Address: 019854b0
// ==========================================================================================

undefined4 Mono_RuntimeGPtrArrayHandle__get_Length(long *param_1)

{
  if (*param_1 != 0) {
    return *(undefined4 *)(*param_1 + 8);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_RuntimeGPtrArrayHandle__get_Item
// Address: 019854cc
// ==========================================================================================

undefined8 Mono_RuntimeGPtrArrayHandle__get_Item(long **param_1,uint param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long *plVar3;
  
  if (-1 < (int)param_2) {
    plVar3 = *param_1;
    if (plVar3 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if ((int)param_2 < *(int *)(plVar3 + 1)) {
      return *(undefined8 *)(*plVar3 + (ulong)param_2 * 8);
    }
  }
  thunk_FUN_00e01b94(PTR_System_IndexOutOfRangeException_TypeInfo_01fc5ea0);
  uVar1 = thunk_FUN_00e11c14();
  System_IndexOutOfRangeException___ctor(uVar1,0);
  uVar2 = thunk_FUN_00e01b94(PTR_Method_Mono_RuntimeGPtrArrayHandle_Lookup_01fd2900);
                    /* WARNING: Subroutine does not return */
  FUN_00db0cb0(uVar1,uVar2);
}



// ==========================================================================================
// Function: Mono_RuntimeGPtrArrayHandle__GPtrArrayFree
// Address: 01985534
// ==========================================================================================

void Mono_RuntimeGPtrArrayHandle__GPtrArrayFree(void **param_1)

{
  if (param_1 != (void **)0x0) {
    if (*param_1 != (void *)0x0) {
      free(*param_1);
      *param_1 = (void *)0x0;
    }
    free(param_1);
    return;
  }
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeGPtrArrayHandle__DestroyAndFree
// Address: 01985538
// ==========================================================================================

void Mono_RuntimeGPtrArrayHandle__DestroyAndFree(undefined8 *param_1)

{
  thunk_FUN_00e09748(*param_1);
  *param_1 = 0;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__PtrToUtf8String
// Address: 01985554
// ==========================================================================================

undefined8 Mono_RuntimeMarshal__PtrToUtf8String(undefined8 param_1)

{
  ulong uVar1;
  char *pcVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  int iVar5;
  
  if ((DAT_021015e0 & 1) == 0) {
    FUN_00db0bbc(PTR_string_TypeInfo_01fbfd50);
    DAT_021015e0 = 1;
  }
  uVar1 = System_IntPtr__op_Equality(param_1,0,0);
  if ((uVar1 & 1) == 0) {
    pcVar2 = (char *)System_IntPtr__op_Explicit(param_1,0);
    if (*pcVar2 == '\0') {
      iVar5 = 0;
    }
    else {
      iVar5 = 0;
      do {
        pcVar2 = pcVar2 + 1;
        iVar5 = iVar5 + 1;
      } while (*pcVar2 != '\0');
    }
    uVar3 = System_IntPtr__op_Explicit(param_1,0);
    uVar4 = System_Text_Encoding__get_UTF8(0);
    uVar3 = Method_System_String_Ctor(uVar3,0,iVar5,uVar4);
    return uVar3;
  }
  return **(undefined8 **)(*(long *)PTR_string_TypeInfo_01fbfd50 + 0xb8);
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__MarshalString
// Address: 01985628
// ==========================================================================================

void Mono_RuntimeMarshal__MarshalString(void)

{
  return;
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal___ctor
// Address: 01985630
// ==========================================================================================

void Mono_SafeStringMarshal___ctor(undefined8 *param_1,undefined8 param_2)

{
  *param_1 = param_2;
  param_1[1] = 0;
  return;
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__DecodeBlobSize
// Address: 01985638
// ==========================================================================================

uint Mono_RuntimeMarshal__DecodeBlobSize(undefined8 param_1,undefined8 *param_2)

{
  byte bVar1;
  byte *pbVar2;
  undefined8 uVar3;
  uint uVar4;
  
  pbVar2 = (byte *)System_IntPtr__op_Explicit(param_1,0);
  bVar1 = *pbVar2;
  uVar4 = (uint)bVar1;
  if ((char)bVar1 < '\0') {
    if ((bVar1 >> 6 & 1) == 0) {
      uVar4 = (uint)pbVar2[1] | (bVar1 & 0x3f) << 8;
      pbVar2 = pbVar2 + 2;
    }
    else {
      uVar4 = (bVar1 & 0x1f) << 0x18 | (uint)pbVar2[1] << 0x10 | (uint)pbVar2[2] << 8 |
              (uint)pbVar2[3];
      pbVar2 = pbVar2 + 4;
    }
  }
  else {
    pbVar2 = pbVar2 + 1;
  }
  uVar3 = System_IntPtr__op_Explicit(pbVar2,0);
  *param_2 = uVar3;
  return uVar4;
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__DecodeBlobArray
// Address: 019856b4
// ==========================================================================================

undefined8 Mono_RuntimeMarshal__DecodeBlobArray(undefined8 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  undefined8 local_28;
  
  puVar2 = PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58;
  puVar1 = PTR_byte___TypeInfo_01fbf258;
  if ((DAT_021015e1 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_System_Runtime_InteropServices_Marshal_TypeInfo_01fc5e58);
    DAT_021015e1 = 1;
  }
  local_28 = 0;
  uVar4 = Mono_RuntimeMarshal__DecodeBlobSize(param_1,&local_28);
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar1,uVar4);
  uVar3 = local_28;
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  System_Runtime_InteropServices_Marshal__Copy(uVar3,uVar5,0,uVar4,0);
  return uVar5;
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__AsciHexDigitValue
// Address: 0198576c
// ==========================================================================================

uint Mono_RuntimeMarshal__AsciHexDigitValue(int param_1)

{
  uint uVar1;
  
  uVar1 = param_1 - 0x30;
  if (9 < uVar1) {
    if (param_1 - 0x61U < 6) {
      return param_1 - 0x57;
    }
    uVar1 = param_1 - 0x37;
  }
  return uVar1;
}



// ==========================================================================================
// Function: Mono_RuntimeMarshal__FreeAssemblyName
// Address: 01985798
// ==========================================================================================

void Mono_RuntimeMarshal__FreeAssemblyName(undefined8 param_1,uint param_2)

{
  FUN_00de39a8(param_1,param_2 & 1);
  return;
}



// ==========================================================================================
// Function: Mono_SafeGPtrArrayHandle___ctor
// Address: 019857a0
// ==========================================================================================

void Mono_SafeGPtrArrayHandle___ctor(undefined8 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  
  uVar1 = System_IntPtr__op_Explicit(param_2,0);
  *param_1 = uVar1;
  return;
}



// ==========================================================================================
// Function: Mono_SafeGPtrArrayHandle__Dispose
// Address: 019857c0
// ==========================================================================================

void Mono_SafeGPtrArrayHandle__Dispose(undefined8 *param_1)

{
  thunk_FUN_00e09748(*param_1);
  *param_1 = 0;
  return;
}



// ==========================================================================================
// Function: Mono_SafeGPtrArrayHandle__get_Length
// Address: 019857dc
// ==========================================================================================

undefined4 Mono_SafeGPtrArrayHandle__get_Length(long *param_1)

{
  if (*param_1 != 0) {
    return *(undefined4 *)(*param_1 + 8);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_SafeGPtrArrayHandle__get_Item
// Address: 019857f8
// ==========================================================================================

undefined8 Mono_SafeGPtrArrayHandle__get_Item(long **param_1,uint param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long *plVar3;
  
  if (-1 < (int)param_2) {
    plVar3 = *param_1;
    if (plVar3 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if ((int)param_2 < *(int *)(plVar3 + 1)) {
      return *(undefined8 *)(*plVar3 + (ulong)param_2 * 8);
    }
  }
  thunk_FUN_00e01b94(PTR_System_IndexOutOfRangeException_TypeInfo_01fc5ea0);
  uVar1 = thunk_FUN_00e11c14();
  System_IndexOutOfRangeException___ctor(uVar1,0);
  uVar2 = thunk_FUN_00e01b94(PTR_Method_Mono_RuntimeGPtrArrayHandle_Lookup_01fd2900);
                    /* WARNING: Subroutine does not return */
  FUN_00db0cb0(uVar1,uVar2);
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal__StringToUtf8_icall
// Address: 019857fc
// ==========================================================================================

undefined8 Mono_SafeStringMarshal__StringToUtf8_icall(long *param_1)

{
  void *pvVar1;
  undefined8 uVar2;
  byte abStack_28 [16];
  void *pvStack_18;
  
  FUN_00dc6cc8(abStack_28,*param_1 + 0x14,*(undefined4 *)(*param_1 + 0x10));
  pvVar1 = (void *)((ulong)abStack_28 | 1);
  if ((abStack_28[0] & 1) != 0) {
    pvVar1 = pvStack_18;
  }
  uVar2 = FUN_00dc7118(pvVar1);
  if ((abStack_28[0] & 1) != 0) {
    operator_delete(pvStack_18);
  }
  return uVar2;
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal__StringToUtf8
// Address: 01985800
// ==========================================================================================

void Mono_SafeStringMarshal__StringToUtf8(undefined8 param_1)

{
  undefined8 local_8;
  
  local_8 = param_1;
  FUN_00de39e8(&local_8);
  return;
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal__GFree
// Address: 01985818
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void Mono_SafeStringMarshal__GFree(void *__ptr)

{
  (*(code *)PTR_free_020ff040)();
  return;
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal__get_Value
// Address: 0198581c
// ==========================================================================================

long Mono_SafeStringMarshal__get_Value(long *param_1)

{
  ulong uVar1;
  long lVar2;
  long local_18;
  
  uVar1 = System_IntPtr__op_Equality(param_1[1],0,0);
  if (((uVar1 & 1) != 0) && (local_18 = *param_1, local_18 != 0)) {
    lVar2 = FUN_00de39e8(&local_18);
    param_1[1] = lVar2;
  }
  return param_1[1];
}



// ==========================================================================================
// Function: Mono_SafeStringMarshal__Dispose
// Address: 01985864
// ==========================================================================================

void Mono_SafeStringMarshal__Dispose(long param_1)

{
  ulong uVar1;
  
  uVar1 = System_IntPtr__op_Inequality(*(undefined8 *)(param_1 + 8),0,0);
  if ((uVar1 & 1) != 0) {
    free(*(void **)(param_1 + 8));
    *(undefined8 *)(param_1 + 8) = 0;
  }
  return;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser___ctor
// Address: 01985894
// ==========================================================================================

void Mono_Xml_SmallXmlParser___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined8 uVar5;
  
  puVar4 = PTR_Mono_Xml_SmallXmlParser_AttrListImpl_TypeInfo_01fd2910;
  puVar3 = PTR_System_Collections_Stack_TypeInfo_01fd2908;
  puVar2 = PTR_char___TypeInfo_01fc59b0;
  puVar1 = PTR_System_Text_StringBuilder_TypeInfo_01fc08f0;
  if ((DAT_021015e2 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Xml_SmallXmlParser_AttrListImpl_TypeInfo_01fd2910);
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    FUN_00db0bbc(PTR_System_Collections_Stack_TypeInfo_01fd2908);
    FUN_00db0bbc(PTR_System_Text_StringBuilder_TypeInfo_01fc08f0);
    DAT_021015e2 = 1;
  }
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  System_Collections_Stack___ctor(uVar5,0);
  *(undefined8 *)(param_1 + 0x20) = uVar5;
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  System_Collections_Stack___ctor(uVar5,0);
  *(undefined8 *)(param_1 + 0x28) = uVar5;
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Text_StringBuilder___ctor(uVar5,200,0);
  *(undefined8 *)(param_1 + 0x38) = uVar5;
  uVar5 = FUN_00db0c30(*(undefined8 *)puVar2,0x1e);
  *(undefined8 *)(param_1 + 0x40) = uVar5;
  uVar5 = thunk_FUN_00e11c14(*(undefined8 *)puVar4);
  Mono_Xml_SmallXmlParser_AttrListImpl___ctor();
  *(undefined8 *)(param_1 + 0x50) = uVar5;
  *(undefined4 *)(param_1 + 0x58) = 1;
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl___ctor
// Address: 019859a0
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl___ctor(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  
  puVar2 = PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470;
  puVar1 = PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468;
  if ((DAT_021015f2 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string___ctor_01fc0470);
    FUN_00db0bbc(PTR_System_Collections_Generic_List_string__TypeInfo_01fc0468);
    DAT_021015f2 = 1;
  }
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Method_System_Collections_Generic_List_object___ctor(uVar3,*(undefined8 *)puVar2);
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  uVar3 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Method_System_Collections_Generic_List_object___ctor(uVar3,*(undefined8 *)puVar2);
  *(undefined8 *)(param_1 + 0x18) = uVar3;
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__Error
// Address: 01985a34
// ==========================================================================================

undefined8 Mono_Xml_SmallXmlParser__Error(long param_1,undefined8 param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  undefined8 uVar4;
  
  puVar3 = PTR_Mono_Xml_SmallXmlParserException_TypeInfo_01fd2918;
  if ((DAT_021015e3 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Xml_SmallXmlParserException_TypeInfo_01fd2918);
    DAT_021015e3 = 1;
  }
  uVar1 = *(undefined4 *)(param_1 + 0x58);
  uVar2 = *(undefined4 *)(param_1 + 0x5c);
  uVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar3);
  Mono_Xml_SmallXmlParserException___ctor(uVar4,param_2,uVar1,uVar2);
  return uVar4;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParserException___ctor
// Address: 01985aa4
// ==========================================================================================

void Mono_Xml_SmallXmlParserException___ctor
               (long param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined4 local_88;
  undefined4 local_84;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  
  puVar2 = PTR_StringLiteral_9788_01fd2920;
  puVar1 = PTR_int_TypeInfo_01fc0108;
  if ((DAT_021015f3 & 1) == 0) {
    FUN_00db0bbc(PTR_int_TypeInfo_01fc0108);
    FUN_00db0bbc(PTR_StringLiteral_9788_01fd2920);
    DAT_021015f3 = 1;
  }
  local_84 = param_3;
  uVar3 = thunk_FUN_00e11868(*(undefined8 *)puVar1,&local_84);
  local_88 = param_4;
  uVar4 = thunk_FUN_00e11868(*(undefined8 *)puVar1,&local_88);
  uVar5 = *(undefined8 *)puVar2;
  uStack_58 = 0;
  local_60 = 0;
  uStack_48 = 0;
  uStack_50 = 0;
  System_ParamsArray___ctor(&local_60,param_2,uVar3,uVar4,0);
  uStack_78 = uStack_58;
  local_80 = local_60;
  uStack_68 = uStack_48;
  uStack_70 = uStack_50;
  uVar3 = Method_System_String_FormatHelper(0,uVar5,&local_80);
  System_SystemException___ctor(param_1,uVar3,0);
  *(undefined4 *)(param_1 + 0x8c) = param_3;
  *(undefined4 *)(param_1 + 0x90) = param_4;
  return;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__UnexpectedEndError
// Address: 01985b90
// ==========================================================================================

void Mono_Xml_SmallXmlParser__UnexpectedEndError(long param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  if ((DAT_021015e4 & 1) == 0) {
    FUN_00db0bbc(PTR_string___TypeInfo_01fbf2f8);
    FUN_00db0bbc(PTR_StringLiteral_5850_01fd2928);
    FUN_00db0bbc(PTR_StringLiteral_646_01fbf440);
    DAT_021015e4 = 1;
  }
  puVar1 = PTR_string___TypeInfo_01fbf2f8;
  plVar4 = *(long **)(param_1 + 0x20);
  if (plVar4 != (long *)0x0) {
    uVar3 = (**(code **)(*plVar4 + 0x1c8))(plVar4,*(undefined8 *)(*plVar4 + 0x1d0));
    uVar5 = FUN_00db0c30(*(undefined8 *)puVar1,uVar3);
    puVar2 = PTR_StringLiteral_5850_01fd2928;
    puVar1 = PTR_StringLiteral_646_01fbf440;
    plVar4 = *(long **)(param_1 + 0x20);
    if (plVar4 != (long *)0x0) {
      (**(code **)(*plVar4 + 0x208))(plVar4,uVar5,0,*(undefined8 *)(*plVar4 + 0x210));
      uVar5 = Method_System_String_Join(*(undefined8 *)puVar1,uVar5);
      uVar6 = *(undefined8 *)puVar2;
      uStack_48 = 0;
      local_50 = 0;
      uStack_38 = 0;
      uStack_40 = 0;
      System_ParamsArray___ctor(&local_50,uVar5,0);
      uStack_68 = uStack_48;
      local_70 = local_50;
      uStack_58 = uStack_38;
      uStack_60 = uStack_40;
      uVar5 = Method_System_String_FormatHelper(0,uVar6,&local_70);
      Mono_Xml_SmallXmlParser__Error(param_1,uVar5);
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__IsNameChar
// Address: 01985d48
// ==========================================================================================

uint Mono_Xml_SmallXmlParser__IsNameChar(undefined8 param_1,uint param_2,uint param_3)

{
  uint uVar1;
  uint uVar2;
  
  if ((DAT_021015e5 & 1) == 0) {
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    DAT_021015e5 = 1;
  }
  uVar1 = param_2 & 0xffff;
  if (uVar1 < 0x2f) {
    if (1 < (param_2 - 0x2d & 0xffff)) goto LAB_01985db8;
LAB_01985df8:
    uVar2 = param_3 ^ 1;
  }
  else {
    uVar2 = 1;
    if ((uVar1 == 0x3a) || (uVar1 == 0x5f)) goto LAB_01985e2c;
    uVar1 = param_2 & 0xffff;
    if (uVar1 < 0x101) {
LAB_01985db8:
      if (*(int *)(*(long *)PTR_char_TypeInfo_01fbf990 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar1 = System_Char__GetUnicodeCategory(param_2,0);
      if (9 < uVar1) {
        uVar2 = 0;
        goto LAB_01985e2c;
      }
      if ((1 << (ulong)(uVar1 & 0x1f) & 0x1e8U) != 0) goto LAB_01985df8;
    }
    else {
      uVar2 = 1;
      if ((uVar1 - 0x6e5 < 2) || (uVar1 == 0x559)) goto LAB_01985e2c;
      if (6 < (param_2 - 699 & 0xffff)) goto LAB_01985db8;
    }
    uVar2 = 1;
  }
LAB_01985e2c:
  return uVar2 & 1;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__IsWhitespace
// Address: 01985e44
// ==========================================================================================

bool Mono_Xml_SmallXmlParser__IsWhitespace(undefined8 param_1,int param_2)

{
  return param_2 == 0x20 || (param_2 == 0xd || param_2 - 9U < 2);
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__SkipWhitespaces
// Address: 01985e6c
// ==========================================================================================

void Mono_Xml_SmallXmlParser__SkipWhitespaces(undefined8 param_1)

{
  Method_Mono_Xml_SmallXmlParser_SkipWhitespaces(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__HandleWhitespaces
// Address: 01985f20
// ==========================================================================================

void Mono_Xml_SmallXmlParser__HandleWhitespaces(long param_1)

{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  long *plVar4;
  long lVar5;
  
  plVar4 = *(long **)(param_1 + 0x18);
  do {
    if (plVar4 == (long *)0x0) {
LAB_01985fdc:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar1 = (**(code **)(*plVar4 + 0x1c8))(plVar4,*(undefined8 *)(*plVar4 + 0x1d0));
    if ((0x20 < uVar1) || ((1L << ((ulong)uVar1 & 0x3f) & 0x100002600U) == 0)) {
      plVar4 = *(long **)(param_1 + 0x18);
      if (plVar4 == (long *)0x0) goto LAB_01985fdc;
      iVar3 = (**(code **)(*plVar4 + 0x1c8))(plVar4,*(undefined8 *)(*plVar4 + 0x1d0));
      if (iVar3 != 0x3c) {
        plVar4 = *(long **)(param_1 + 0x18);
        if (plVar4 == (long *)0x0) goto LAB_01985fdc;
        iVar3 = (**(code **)(*plVar4 + 0x1c8))(plVar4,*(undefined8 *)(*plVar4 + 0x1d0));
        if (-1 < iVar3) {
          *(undefined *)(param_1 + 0x48) = 0;
        }
      }
      return;
    }
    lVar5 = *(long *)(param_1 + 0x38);
    uVar2 = Mono_Xml_SmallXmlParser__Read(param_1);
    if (lVar5 == 0) goto LAB_01985fdc;
    System_Text_StringBuilder__Append(lVar5,uVar2,0);
    plVar4 = *(long **)(param_1 + 0x18);
  } while( true );
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__Read
// Address: 01985fe0
// ==========================================================================================

void Mono_Xml_SmallXmlParser__Read(long param_1)

{
  int iVar1;
  long *plVar2;
  
  plVar2 = *(long **)(param_1 + 0x18);
  if (plVar2 != (long *)0x0) {
    iVar1 = (**(code **)(*plVar2 + 0x1d8))(plVar2,*(undefined8 *)(*plVar2 + 0x1e0));
    if ((iVar1 == 10) || (*(char *)(param_1 + 0x60) != '\0')) {
      *(undefined *)(param_1 + 0x60) = 0;
      *(int *)(param_1 + 0x58) = *(int *)(param_1 + 0x58) + 1;
      *(undefined4 *)(param_1 + 0x5c) = 1;
    }
    else {
      *(int *)(param_1 + 0x5c) = *(int *)(param_1 + 0x5c) + 1;
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__Peek
// Address: 0198603c
// ==========================================================================================

void Mono_Xml_SmallXmlParser__Peek(long param_1)

{
  long *plVar1;
  
  plVar1 = *(long **)(param_1 + 0x18);
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x01986054. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x1c8))(plVar1,*(undefined8 *)(*plVar1 + 0x1d0));
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__HandleBufferedContent
// Address: 01986e1c
// ==========================================================================================

void Mono_Xml_SmallXmlParser__HandleBufferedContent(long param_1)

{
  char cVar1;
  ushort uVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  code **ppcVar6;
  long lVar7;
  undefined8 uVar8;
  long lVar9;
  ulong uVar10;
  int *piVar11;
  long *plVar12;
  
  if ((DAT_021015e9 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Xml_SmallXmlParser_IContentHandler_TypeInfo_01fd29b0);
    DAT_021015e9 = 1;
  }
  if (*(long *)(param_1 + 0x38) != 0) {
    iVar3 = System_Text_StringBuilder__get_Length(*(long *)(param_1 + 0x38),0);
    if (iVar3 == 0) {
      return;
    }
    plVar4 = *(long **)(param_1 + 0x38);
    if (plVar4 != (long *)0x0) {
      cVar1 = *(char *)(param_1 + 0x48);
      plVar12 = *(long **)(param_1 + 0x10);
      uVar5 = (**(code **)(*plVar4 + 0x168))(plVar4,*(undefined8 *)(*plVar4 + 0x170));
      if (plVar12 != (long *)0x0) {
        lVar9 = *plVar12;
        lVar7 = *(long *)PTR_Mono_Xml_SmallXmlParser_IContentHandler_TypeInfo_01fd29b0;
        uVar2 = *(ushort *)(lVar9 + 0x12e);
        uVar10 = (ulong)uVar2;
        if (cVar1 == '\0') {
          if (uVar2 != 0) {
            piVar11 = (int *)(*(long *)(lVar9 + 0xb0) + 8);
            do {
              if (*(long *)(piVar11 + -2) == lVar7) {
                iVar3 = *piVar11 + 5;
                goto LAB_01986f10;
              }
              uVar10 = uVar10 - 1;
              piVar11 = piVar11 + 4;
            } while (uVar10 != 0);
          }
          uVar8 = 5;
        }
        else {
          if (uVar2 != 0) {
            piVar11 = (int *)(*(long *)(lVar9 + 0xb0) + 8);
LAB_01986ea8:
            if (*(long *)(piVar11 + -2) != lVar7) goto code_r0x01986eb4;
            iVar3 = *piVar11 + 6;
LAB_01986f10:
            ppcVar6 = (code **)(lVar9 + (long)iVar3 * 0x10 + 0x138);
            goto LAB_01986f18;
          }
LAB_01986ec0:
          uVar8 = 6;
        }
        ppcVar6 = (code **)FUN_00e0dcd4(plVar12,lVar7,uVar8);
LAB_01986f18:
        (**ppcVar6)(plVar12,uVar5,ppcVar6[1]);
        if (*(long *)(param_1 + 0x38) != 0) {
          Method_System_Text_StringBuilder_set_Length(*(long *)(param_1 + 0x38),0,0);
          *(undefined *)(param_1 + 0x48) = 0;
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
code_r0x01986eb4:
  uVar10 = uVar10 - 1;
  piVar11 = piVar11 + 4;
  if (uVar10 == 0) goto LAB_01986ec0;
  goto LAB_01986ea8;
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__Cleanup
// Address: 01986f54
// ==========================================================================================

void Mono_Xml_SmallXmlParser__Cleanup(long param_1)

{
  undefined8 uVar1;
  long *plVar2;
  
  uVar1 = DAT_005bc9e8;
  plVar2 = *(long **)(param_1 + 0x20);
  *(undefined8 *)(param_1 + 0x10) = 0;
  *(undefined8 *)(param_1 + 0x18) = 0;
  *(undefined8 *)(param_1 + 0x58) = uVar1;
  if (plVar2 != (long *)0x0) {
    (**(code **)(*plVar2 + 0x1e8))(plVar2,*(undefined8 *)(*plVar2 + 0x1f0));
    plVar2 = *(long **)(param_1 + 0x28);
    if (plVar2 != (long *)0x0) {
      (**(code **)(*plVar2 + 0x1e8))(plVar2,*(undefined8 *)(*plVar2 + 0x1f0));
      if (*(long *)(param_1 + 0x50) != 0) {
        Mono_Xml_SmallXmlParser_AttrListImpl__Clear();
        if (*(long *)(param_1 + 0x38) != 0) {
          Method_System_Text_StringBuilder_set_Length(*(long *)(param_1 + 0x38),0,0);
          *(undefined8 *)(param_1 + 0x30) = 0;
          *(undefined *)(param_1 + 0x48) = 0;
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__Clear
// Address: 01986fc8
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl__Clear(long param_1)

{
  int iVar1;
  long lVar2;
  
  if ((DAT_021015f0 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__Clear_01fc9c28);
    DAT_021015f0 = 1;
  }
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 0x18);
    *(undefined4 *)(lVar2 + 0x18) = 0;
    *(int *)(lVar2 + 0x1c) = *(int *)(lVar2 + 0x1c) + 1;
    if (0 < iVar1) {
      Method_System_Array_Clear(*(undefined8 *)(lVar2 + 0x10),0,iVar1,0);
    }
    lVar2 = *(long *)(param_1 + 0x18);
    if (lVar2 != 0) {
      iVar1 = *(int *)(lVar2 + 0x18);
      *(undefined4 *)(lVar2 + 0x18) = 0;
      *(int *)(lVar2 + 0x1c) = *(int *)(lVar2 + 0x1c) + 1;
      if (0 < iVar1) {
        Method_System_Array_Clear(*(undefined8 *)(lVar2 + 0x10),0,iVar1,0);
        return;
      }
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__ReadCharacters
// Address: 0198742c
// ==========================================================================================

void Mono_Xml_SmallXmlParser__ReadCharacters(long param_1)

{
  int iVar1;
  undefined4 uVar2;
  long *plVar3;
  long lVar4;
  
  plVar3 = *(long **)(param_1 + 0x18);
  *(undefined *)(param_1 + 0x48) = 0;
  while (plVar3 != (long *)0x0) {
    iVar1 = (**(code **)(*plVar3 + 0x1c8))(plVar3,*(undefined8 *)(*plVar3 + 0x1d0));
    if (iVar1 == 0x26) {
      Mono_Xml_SmallXmlParser__Read(param_1);
      Method_Mono_Xml_SmallXmlParser_ReadReference(param_1);
    }
    else {
      if ((iVar1 == -1) || (iVar1 == 0x3c)) {
        return;
      }
      lVar4 = *(long *)(param_1 + 0x38);
      uVar2 = Mono_Xml_SmallXmlParser__Read(param_1);
      if (lVar4 == 0) break;
      System_Text_StringBuilder__Append(lVar4,uVar2,0);
    }
    plVar3 = *(long **)(param_1 + 0x18);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser__ReadCharacterReference
// Address: 019874b4
// ==========================================================================================

undefined8 Mono_Xml_SmallXmlParser__ReadCharacterReference(long param_1)

{
  int iVar1;
  uint uVar2;
  long *plVar3;
  
  plVar3 = *(long **)(param_1 + 0x18);
  if (plVar3 != (long *)0x0) {
    iVar1 = (**(code **)(*plVar3 + 0x1c8))(plVar3,*(undefined8 *)(*plVar3 + 0x1d0));
    if (iVar1 == 0x78) {
      do {
        Mono_Xml_SmallXmlParser__Read(param_1);
        plVar3 = *(long **)(param_1 + 0x18);
        if (plVar3 == (long *)0x0) goto LAB_0198756c;
        uVar2 = (**(code **)(*plVar3 + 0x1c8))(plVar3,*(undefined8 *)(*plVar3 + 0x1d0));
      } while ((-1 < (int)uVar2) && (((uVar2 & 0xffffffdf) - 0x41 < 6 || (uVar2 - 0x30 < 10))));
    }
    else {
      plVar3 = *(long **)(param_1 + 0x18);
      if (plVar3 == (long *)0x0) goto LAB_0198756c;
      iVar1 = (**(code **)(*plVar3 + 0x1c8))(plVar3,*(undefined8 *)(*plVar3 + 0x1d0));
      while (iVar1 - 0x30U < 10) {
        Mono_Xml_SmallXmlParser__Read(param_1);
        plVar3 = *(long **)(param_1 + 0x18);
        if (plVar3 == (long *)0x0) goto LAB_0198756c;
        iVar1 = (**(code **)(*plVar3 + 0x1c8))(plVar3,*(undefined8 *)(*plVar3 + 0x1d0));
      }
    }
    return 0;
  }
LAB_0198756c:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__Add
// Address: 01987574
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl__Add(long param_1,undefined8 param_2,undefined8 param_3)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  
  if ((DAT_021015f1 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__Add_01fc0498);
    DAT_021015f1 = 1;
  }
  puVar2 = PTR_Method_System_Collections_Generic_List_string__Add_01fc0498;
  lVar3 = *(long *)(param_1 + 0x10);
  if (lVar3 != 0) {
    lVar4 = *(long *)(lVar3 + 0x10);
    lVar5 = *(long *)PTR_Method_System_Collections_Generic_List_string__Add_01fc0498;
    *(int *)(lVar3 + 0x1c) = *(int *)(lVar3 + 0x1c) + 1;
    if (lVar4 != 0) {
      uVar1 = *(uint *)(lVar3 + 0x18);
      if (uVar1 < *(uint *)(lVar4 + 0x18)) {
        *(uint *)(lVar3 + 0x18) = uVar1 + 1;
        *(undefined8 *)(lVar4 + (long)(int)uVar1 * 8 + 0x20) = param_2;
      }
      else {
        System_Collections_Generic_List_object___AddWithResize
                  (lVar3,param_2,*(undefined8 *)(*(long *)(*(long *)(lVar5 + 0x20) + 0xc0) + 0x70));
      }
      lVar3 = *(long *)(param_1 + 0x18);
      if (lVar3 != 0) {
        lVar4 = *(long *)(lVar3 + 0x10);
        lVar5 = *(long *)puVar2;
        *(int *)(lVar3 + 0x1c) = *(int *)(lVar3 + 0x1c) + 1;
        if (lVar4 != 0) {
          uVar1 = *(uint *)(lVar3 + 0x18);
          if (uVar1 < *(uint *)(lVar4 + 0x18)) {
            *(uint *)(lVar3 + 0x18) = uVar1 + 1;
            *(undefined8 *)(lVar4 + (long)(int)uVar1 * 8 + 0x20) = param_3;
            return;
          }
          System_Collections_Generic_List_object___AddWithResize
                    (lVar3,param_3,*(undefined8 *)(*(long *)(*(long *)(lVar5 + 0x20) + 0xc0) + 0x70)
                    );
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__GetValue
// Address: 01987680
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl__GetValue(long param_1,undefined4 param_2)

{
  if ((DAT_021015ec & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__get_Item_01fc0638);
    DAT_021015ec = 1;
  }
  if (*(long *)(param_1 + 0x18) != 0) {
    Method_System_Collections_Generic_List_object__get_Item
              (*(long *)(param_1 + 0x18),param_2,
               *(undefined8 *)PTR_Method_System_Collections_Generic_List_string__get_Item_01fc0638);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__GetValue
// Address: 019876d8
// ==========================================================================================

undefined8 Mono_Xml_SmallXmlParser_AttrListImpl__GetValue(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  long lVar2;
  undefined8 uVar3;
  ulong uVar4;
  int iVar5;
  
  if ((DAT_021015ed & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__get_Count_01fc06b0);
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__get_Item_01fc0638);
    DAT_021015ed = 1;
  }
  puVar1 = PTR_Method_System_Collections_Generic_List_string__get_Item_01fc0638;
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    iVar5 = 0;
    do {
      if (*(int *)(lVar2 + 0x18) <= iVar5) {
        return 0;
      }
      uVar3 = Method_System_Collections_Generic_List_object__get_Item
                        (lVar2,iVar5,*(undefined8 *)puVar1);
      uVar4 = System_String__Equals(uVar3,param_2);
      if ((uVar4 & 1) != 0) {
        if (*(long *)(param_1 + 0x18) != 0) {
          uVar3 = Method_System_Collections_Generic_List_object__get_Item
                            (*(long *)(param_1 + 0x18),iVar5,*(undefined8 *)puVar1);
          return uVar3;
        }
        break;
      }
      lVar2 = *(long *)(param_1 + 0x10);
      iVar5 = iVar5 + 1;
    } while (lVar2 != 0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__get_Names
// Address: 01987794
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl__get_Names(long param_1)

{
  if ((DAT_021015ee & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    DAT_021015ee = 1;
  }
  if (*(long *)(param_1 + 0x10) != 0) {
    Method_System_Collections_Generic_List_object__ToArray
              (*(long *)(param_1 + 0x10),
               *(undefined8 *)PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Xml_SmallXmlParser_AttrListImpl__get_Values
// Address: 019877e4
// ==========================================================================================

void Mono_Xml_SmallXmlParser_AttrListImpl__get_Values(long param_1)

{
  if ((DAT_021015ef & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    DAT_021015ef = 1;
  }
  if (*(long *)(param_1 + 0x18) != 0) {
    Method_System_Collections_Generic_List_object__ToArray
              (*(long *)(param_1 + 0x18),
               *(undefined8 *)PTR_Method_System_Collections_Generic_List_string__ToArray_01fc0528);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Interop_MonoPInvokeCallbackAttribute___ctor
// Address: 01987834
// ==========================================================================================

void Mono_Interop_MonoPInvokeCallbackAttribute___ctor(undefined8 param_1)

{
  System_Attribute___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_CodePointIndexer___ctor
// Address: 0198783c
// ==========================================================================================

void Mono_Globalization_Unicode_CodePointIndexer___ctor
               (long param_1,long param_2,long param_3,undefined4 param_4,undefined4 param_5)

{
  int iVar1;
  int iVar2;
  long lVar3;
  int iVar4;
  long lVar5;
  uint uVar6;
  ulong uVar7;
  int *piVar8;
  uint uVar9;
  ulong uVar10;
  int iVar11;
  
  if ((DAT_021015f4 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_CodePointIndexer_TableRange___TypeInfo_01fd2a30);
    DAT_021015f4 = 1;
  }
  System_Object___ctor(param_1,0);
  *(undefined4 *)(param_1 + 0x1c) = param_4;
  *(undefined4 *)(param_1 + 0x20) = param_5;
  if (param_2 != 0) {
    lVar3 = FUN_00db0c30(*(undefined8 *)
                          PTR_Mono_Globalization_Unicode_CodePointIndexer_TableRange___TypeInfo_01fd2a30
                         ,*(undefined4 *)(param_2 + 0x18));
    *(long *)(param_1 + 0x10) = lVar3;
    if (lVar3 != 0) {
      lVar5 = 0;
      uVar7 = 0;
      do {
        uVar10 = *(ulong *)(lVar3 + 0x18) & 0xffffffff;
        uVar9 = (uint)*(ulong *)(lVar3 + 0x18);
        if ((long)(int)uVar9 <= (long)uVar7) {
          if (0 < (int)uVar9) {
            iVar4 = *(int *)(param_1 + 0x18);
            piVar8 = (int *)(lVar3 + 0x28);
            do {
              uVar10 = uVar10 - 1;
              iVar4 = *piVar8 + iVar4;
              piVar8 = piVar8 + 5;
            } while (uVar10 != 0);
            *(int *)(param_1 + 0x18) = iVar4;
          }
          return;
        }
        if (*(uint *)(param_2 + 0x18) <= uVar7) {
LAB_01987990:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        if (param_3 == 0) break;
        if (*(uint *)(param_3 + 0x18) <= uVar7) goto LAB_01987990;
        iVar4 = *(int *)(param_2 + 0x20 + uVar7 * 4);
        iVar1 = *(int *)(param_3 + 0x20 + uVar7 * 4);
        if (uVar7 == 0) {
          uVar6 = 0;
          iVar11 = 0;
        }
        else {
          uVar6 = (uint)uVar7;
          if (uVar9 <= uVar6 - 1) goto LAB_01987990;
          iVar11 = *(int *)(lVar3 + lVar5 + 0x14) + *(int *)(lVar3 + lVar5 + 0x18);
        }
        if (uVar9 <= uVar6) goto LAB_01987990;
        iVar2 = iVar1 - iVar4;
        lVar3 = lVar3 + (long)(int)uVar6 * 0x14;
        *(int *)(lVar3 + 0x20) = iVar4;
        *(int *)(lVar3 + 0x24) = iVar1;
        *(int *)(lVar3 + 0x28) = iVar2;
        *(int *)(lVar3 + 0x2c) = iVar11;
        *(int *)(lVar3 + 0x30) = iVar11 + iVar2;
        lVar3 = *(long *)(param_1 + 0x10);
        uVar7 = uVar7 + 1;
        lVar5 = lVar5 + 0x14;
      } while (lVar3 != 0);
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_CodePointIndexer_TableRange___ctor
// Address: 01987994
// ==========================================================================================

void Mono_Globalization_Unicode_CodePointIndexer_TableRange___ctor
               (int *param_1,int param_2,int param_3,int param_4)

{
  param_1[2] = param_3 - param_2;
  param_1[3] = param_4;
  *param_1 = param_2;
  param_1[1] = param_3;
  param_1[4] = (param_3 - param_2) + param_4;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_CodePointIndexer__ToIndex
// Address: 019879ac
// ==========================================================================================

int Mono_Globalization_Unicode_CodePointIndexer__ToIndex(long param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  long lVar3;
  uint uVar4;
  
  lVar3 = *(long *)(param_1 + 0x10);
  if (lVar3 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar1 = *(uint *)(lVar3 + 0x18);
  if (0 < (int)uVar1) {
    uVar4 = 0;
    do {
      if (uVar1 <= uVar4) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      iVar2 = *(int *)(lVar3 + (long)(int)uVar4 * 0x14 + 0x20);
      if (param_2 < iVar2) break;
      if (param_2 < *(int *)(lVar3 + (long)(int)uVar4 * 0x14 + 0x24)) {
        return (param_2 - iVar2) + *(int *)(lVar3 + (long)(int)uVar4 * 0x14 + 0x2c);
      }
      uVar4 = uVar4 + 1;
    } while ((int)uVar4 < (int)uVar1);
  }
  return *(int *)(param_1 + 0x1c);
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_TailoringInfo___ctor
// Address: 01987a30
// ==========================================================================================

void Mono_Globalization_Unicode_TailoringInfo___ctor
               (long param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,byte param_5)

{
  System_Object___ctor(param_1,0);
  *(undefined4 *)(param_1 + 0x10) = param_2;
  *(undefined4 *)(param_1 + 0x14) = param_3;
  *(undefined4 *)(param_1 + 0x18) = param_4;
  *(byte *)(param_1 + 0x1c) = param_5 & 1;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_Contraction___ctor
// Address: 01987a74
// ==========================================================================================

void Mono_Globalization_Unicode_Contraction___ctor
               (long param_1,undefined4 param_2,undefined8 param_3,undefined8 param_4,
               undefined8 param_5)

{
  System_Object___ctor(param_1,0);
  *(undefined4 *)(param_1 + 0x10) = param_2;
  *(undefined8 *)(param_1 + 0x18) = param_3;
  *(undefined8 *)(param_1 + 0x20) = param_4;
  *(undefined8 *)(param_1 + 0x28) = param_5;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_ContractionComparer__Compare
// Address: 01987ab8
// ==========================================================================================

ulong Mono_Globalization_Unicode_ContractionComparer__Compare
                (ulong param_1,long param_2,long param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  long lVar5;
  long lVar6;
  int iVar7;
  
  if ((((param_2 != 0) && (param_3 != 0)) && (lVar5 = *(long *)(param_2 + 0x18), lVar5 != 0)) &&
     (lVar6 = *(long *)(param_3 + 0x18), lVar6 != 0)) {
    iVar2 = *(int *)(lVar5 + 0x18);
    iVar3 = *(int *)(lVar6 + 0x18);
    iVar1 = iVar3;
    if (iVar2 <= iVar3) {
      iVar1 = iVar2;
    }
    if (0 < iVar1) {
      iVar7 = 0;
      do {
        if ((iVar2 == iVar7) || (iVar3 == iVar7)) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec(param_1);
        }
        uVar4 = (uint)*(ushort *)(lVar5 + (long)iVar7 * 2 + 0x20) -
                (uint)*(ushort *)(lVar6 + (long)iVar7 * 2 + 0x20);
        param_1 = (ulong)uVar4;
        if (uVar4 != 0) {
          return param_1;
        }
        iVar7 = iVar7 + 1;
      } while (iVar1 != iVar7);
    }
    uVar4 = iVar2 - iVar3;
    if (uVar4 == 0) {
      uVar4 = *(int *)(param_2 + 0x10) - *(int *)(param_3 + 0x10);
    }
    return (ulong)uVar4;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_ContractionComparer___ctor
// Address: 01987b4c
// ==========================================================================================

void Mono_Globalization_Unicode_ContractionComparer___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_ContractionComparer___cctor
// Address: 01987b54
// ==========================================================================================

void Mono_Globalization_Unicode_ContractionComparer___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_ContractionComparer_TypeInfo_01fd2a38;
  if ((DAT_021015f5 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_ContractionComparer_TypeInfo_01fd2a38);
    DAT_021015f5 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_Level2Map___ctor
// Address: 01987bb0
// ==========================================================================================

void Mono_Globalization_Unicode_Level2Map___ctor(long param_1,undefined param_2,undefined param_3)

{
  System_Object___ctor(param_1,0);
  *(undefined *)(param_1 + 0x10) = param_2;
  *(undefined *)(param_1 + 0x11) = param_3;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__GetTailoringInfo
// Address: 01987be0
// ==========================================================================================

undefined8 Mono_Globalization_Unicode_MSCompatUnicodeTable__GetTailoringInfo(int param_1)

{
  undefined *puVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  uint uVar5;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015f6 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015f6 = 1;
  }
  lVar2 = *(long *)puVar1;
  uVar5 = 0;
  while( true ) {
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    lVar3 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x80);
    if (lVar3 == 0) goto LAB_01987cdc;
    if (*(int *)(lVar3 + 0x18) <= (int)uVar5) {
      return 0;
    }
    if (*(int *)(lVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar2 = *(long *)puVar1;
    }
    lVar3 = *(long *)(*(long *)(lVar2 + 0xb8) + 0x80);
    if (lVar3 == 0) goto LAB_01987cdc;
    if (*(uint *)(lVar3 + 0x18) <= uVar5) goto LAB_01987ce0;
    lVar4 = *(long *)(lVar3 + (long)(int)uVar5 * 8 + 0x20);
    if (lVar4 == 0) goto LAB_01987cdc;
    if (*(int *)(lVar4 + 0x10) == param_1) break;
    uVar5 = uVar5 + 1;
  }
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar3 = *(long *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x80);
    if (lVar3 == 0) {
LAB_01987cdc:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
  }
  if (uVar5 < *(uint *)(lVar3 + 0x18)) {
    return *(undefined8 *)(lVar3 + (long)(int)uVar5 * 8 + 0x20);
  }
LAB_01987ce0:
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__SetCJKReferences
// Address: 01988438
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable__SetCJKReferences
               (undefined8 param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
               undefined8 *param_5,undefined8 *param_6)

{
  undefined *puVar1;
  ulong uVar2;
  long lVar3;
  long lVar4;
  undefined8 uVar5;
  
  puVar1 = PTR_StringLiteral_9723_01fd2ad0;
  if ((DAT_021015f8 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_StringLiteral_8062_01fbfe10);
    FUN_00db0bbc(PTR_StringLiteral_8142_01fc3770);
    FUN_00db0bbc(PTR_StringLiteral_9724_01fd2ae0);
    FUN_00db0bbc(PTR_StringLiteral_9723_01fd2ad0);
    DAT_021015f8 = 1;
  }
  uVar2 = System_String__Equals(param_1,*(undefined8 *)puVar1);
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((uVar2 & 1) == 0) {
    uVar2 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_9724_01fd2ae0);
    puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    if ((uVar2 & 1) == 0) {
      uVar2 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8062_01fbfe10);
      puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
      if ((uVar2 & 1) == 0) {
        uVar2 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8142_01fc3770);
        puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
        if ((uVar2 & 1) == 0) {
          return;
        }
        lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
        if (*(int *)(lVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar3 = *(long *)puVar1;
        }
        lVar3 = *(long *)(lVar3 + 0xb8);
        *param_3 = *(undefined8 *)(lVar3 + 0x48);
        *param_4 = *(undefined8 *)(lVar3 + 0x68);
        *param_6 = *(undefined8 *)(lVar3 + 0x70);
        puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
        lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
        if (*(int *)(lVar3 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar3 = *(long *)puVar1;
        }
        *param_2 = *(undefined8 *)(*(long *)(lVar3 + 0xb8) + 0x30);
        lVar3 = *(long *)puVar1;
        lVar4 = 0x30;
        param_2 = param_5;
        goto LAB_019885e0;
      }
      lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
      if (*(int *)(lVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar3 = *(long *)puVar1;
      }
      lVar3 = *(long *)(lVar3 + 0xb8);
      *param_3 = *(undefined8 *)(lVar3 + 0x40);
      uVar5 = *(undefined8 *)(lVar3 + 0x60);
    }
    else {
      lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
      if (*(int *)(lVar3 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar3 = *(long *)puVar1;
      }
      lVar3 = *(long *)(lVar3 + 0xb8);
      *param_3 = *(undefined8 *)(lVar3 + 0x38);
      uVar5 = *(undefined8 *)(lVar3 + 0x58);
    }
    *param_4 = uVar5;
    puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    lVar4 = 0x30;
  }
  else {
    lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    lVar3 = *(long *)(lVar3 + 0xb8);
    *param_3 = *(undefined8 *)(lVar3 + 0x30);
    *param_4 = *(undefined8 *)(lVar3 + 0x50);
    puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    lVar3 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    if (*(int *)(lVar3 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar3 = *(long *)puVar1;
    }
    lVar4 = 0x28;
  }
LAB_019885e0:
  *param_2 = *(undefined8 *)(*(long *)(lVar3 + 0xb8) + lVar4);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__Category
// Address: 01988688
// ==========================================================================================

undefined Mono_Globalization_Unicode_MSCompatUnicodeTable__Category(undefined4 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015f9 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015f9 = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar5 = *(long *)puVar2;
  lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x10);
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 8);
  if (lVar5 != 0) {
    iVar3 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(lVar5,param_1);
    return *(undefined *)(lVar4 + iVar3);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__Level1
// Address: 0198872c
// ==========================================================================================

undefined Mono_Globalization_Unicode_MSCompatUnicodeTable__Level1(undefined4 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015fa & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015fa = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar5 = *(long *)puVar2;
  lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x18);
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x10);
  if (lVar5 != 0) {
    iVar3 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(lVar5,param_1);
    return *(undefined *)(lVar4 + iVar3);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__Level2
// Address: 019887d0
// ==========================================================================================

undefined Mono_Globalization_Unicode_MSCompatUnicodeTable__Level2(undefined4 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015fb & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015fb = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar5 = *(long *)puVar2;
  lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x20);
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x18);
  if (lVar5 != 0) {
    iVar3 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(lVar5,param_1);
    return *(undefined *)(lVar4 + iVar3);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3
// Address: 01988874
// ==========================================================================================

undefined Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(undefined4 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  long lVar4;
  long lVar5;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015fc & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015fc = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
  lVar4 = *(long *)puVar1;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar1;
  }
  lVar5 = *(long *)puVar2;
  lVar4 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x28);
  if (*(int *)(lVar5 + 0xe0) == 0) {
    thunk_FUN_00df405c(lVar5);
    lVar5 = *(long *)puVar2;
  }
  lVar5 = *(long *)(*(long *)(lVar5 + 0xb8) + 0x20);
  if (lVar5 != 0) {
    iVar3 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(lVar5,param_1);
    return *(undefined *)(lVar4 + iVar3);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsSortable
// Address: 01988918
// ==========================================================================================

byte Mono_Globalization_Unicode_MSCompatUnicodeTable__IsSortable(long param_1)

{
  undefined2 uVar1;
  undefined *puVar2;
  ulong uVar3;
  bool bVar4;
  long lVar5;
  
  if ((DAT_021015fd & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015fd = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if (param_1 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  bVar4 = 0 < *(int *)(param_1 + 0x10);
  if (0 < *(int *)(param_1 + 0x10)) {
    lVar5 = 0;
    do {
      uVar1 = *(undefined2 *)(param_1 + 0x14 + lVar5 * 2);
      if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar3 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsSortable(uVar1);
      if ((uVar3 & 1) == 0) break;
      lVar5 = lVar5 + 1;
      bVar4 = lVar5 < *(int *)(param_1 + 0x10);
    } while (lVar5 < *(int *)(param_1 + 0x10));
  }
  return ~bVar4 & 1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsSortable
// Address: 01988a04
// ==========================================================================================

bool Mono_Globalization_Unicode_MSCompatUnicodeTable__IsSortable(uint param_1)

{
  undefined *puVar1;
  bool bVar2;
  ulong uVar3;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015fe & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015fe = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable(param_1);
  if ((((((uVar3 & 1) == 0) || (param_1 == 0)) || (param_1 == 0x640)) ||
      ((param_1 == 0xfeff || (param_1 >> 2 == 0x803)))) ||
     ((param_1 - 0x206a < 6 || ((param_1 - 0x202a < 5 || (param_1 - 0x180b < 4)))))) {
    bVar2 = true;
  }
  else {
    bVar2 = param_1 - 0xfff9 < 5;
  }
  return bVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable
// Address: 01988acc
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable(undefined4 param_1)

{
  undefined *puVar1;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_021015ff & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_021015ff = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable(param_1,1);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable
// Address: 01988b24
// ==========================================================================================

bool Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable(int param_1,byte param_2)

{
  undefined *puVar1;
  bool bVar2;
  int iVar3;
  uint uVar4;
  long lVar5;
  
  if ((DAT_02101600 & 1) == 0) {
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101600 = 1;
  }
  if (param_1 == 0) {
    bVar2 = true;
  }
  else {
    if ((param_2 & 1) != 0) {
      if (*(int *)(*(long *)PTR_char_TypeInfo_01fbf990 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      iVar3 = System_Char__GetUnicodeCategory(param_1,0);
      if (iVar3 == 0x1d) {
        return true;
      }
      if (param_1 - 0xd880U < 0x300) {
        return true;
      }
    }
    puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    lVar5 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
    if (*(int *)(lVar5 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar5 = *(long *)puVar1;
    }
    if (**(long **)(lVar5 + 0xb8) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar4 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(**(long **)(lVar5 + 0xb8),param_1);
    puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    if ((int)uVar4 < 0) {
      bVar2 = false;
    }
    else {
      lVar5 = *(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
      if (*(int *)(lVar5 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar5 = *(long *)puVar1;
      }
      bVar2 = (param_2 & *(byte *)(*(long *)(*(long *)(lVar5 + 0xb8) + 8) + (ulong)uVar4)) != 0;
    }
  }
  return bVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing
// Address: 01988c3c
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(undefined4 param_1)

{
  undefined *puVar1;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_02101601 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101601 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable(param_1,4);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__ToKanaTypeInsensitive
// Address: 01988c94
// ==========================================================================================

int Mono_Globalization_Unicode_MSCompatUnicodeTable__ToKanaTypeInsensitive(int param_1)

{
  int iVar1;
  
  iVar1 = param_1 + 0x60;
  if (0x53 < param_1 - 0x3041U) {
    iVar1 = param_1;
  }
  return iVar1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__ToWidthCompat
// Address: 01988cac
// ==========================================================================================

ulong Mono_Globalization_Unicode_MSCompatUnicodeTable__ToWidthCompat(ulong param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  
  uVar2 = (uint)param_1;
  if (0x218f < (int)uVar2) {
    if ((int)uVar2 < 0xff01) {
      if ((int)uVar2 < 0x32ff) {
        if ((int)uVar2 < 0x2194) {
          iVar3 = 0xde59;
          goto LAB_01988d60;
        }
        if (0x2501 < (int)uVar2) {
          if ((int)uVar2 < 0x25cc) {
            if (uVar2 == 0x2502) {
              return 0xffe8;
            }
            if (uVar2 == 0x25a0) {
              return 0xffed;
            }
            if (uVar2 == 0x25cb) {
              return 0xffee;
            }
          }
          else if (0x2fff < (int)uVar2) {
            if (0x3130 < (int)uVar2) {
              if (0x3163 < (int)uVar2) {
                uVar1 = 0xffa0;
                if (uVar2 != 0x3164) {
                  uVar1 = uVar2;
                }
                return (ulong)uVar1;
              }
              iVar3 = 0xce70;
              goto LAB_01988d60;
            }
            if ((int)uVar2 < 0x300d) {
              if ((int)uVar2 < 0x3002) {
                if (uVar2 == 0x3000) {
                  return 0x20;
                }
                if (uVar2 == 0x3001) {
                  return 0xff64;
                }
              }
              else {
                if (uVar2 == 0x3002) {
                  return 0xff61;
                }
                if (uVar2 == 0x300c) {
                  return 0xff62;
                }
              }
            }
            else {
              if (uVar2 == 0x300d) {
                return 0xff63;
              }
              if (uVar2 == 0x30fb) {
                return 0xff65;
              }
            }
          }
        }
      }
    }
    else {
      if ((int)uVar2 < 0xff5f) {
        iVar3 = -0xfee0;
LAB_01988d60:
        return (ulong)(uVar2 + iVar3);
      }
      if (uVar2 - 0xffe0 < 7) {
        param_1 = (ulong)*(uint *)(&DAT_0060cd3c + (long)(int)(uVar2 - 0xffe0) * 4);
      }
    }
  }
  return param_1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__HasSpecialWeight
// Address: 01988e38
// ==========================================================================================

bool Mono_Globalization_Unicode_MSCompatUnicodeTable__HasSpecialWeight(uint param_1)

{
  uint uVar1;
  
  if (0x3040 < (param_1 & 0xffff)) {
    if ((param_1 + 0x9a & 0xffff) < 0x38) {
      return true;
    }
    uVar1 = param_1 >> 8 & 0xff;
    if (uVar1 < 0x33) {
      if ((param_1 & 0xffff) < 0x309d) {
        uVar1 = 0x3099;
      }
      else {
        if (uVar1 < 0x31) {
          return (param_1 & 0xffff) != 0x30fb;
        }
        if ((param_1 >> 4 & 0xfff) < 0x32d) {
          return false;
        }
        uVar1 = 0x32ff;
      }
      return (param_1 & 0xffff) < uVar1;
    }
  }
  return false;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsHalfWidthKana
// Address: 01988eb8
// ==========================================================================================

bool Mono_Globalization_Unicode_MSCompatUnicodeTable__IsHalfWidthKana(short param_1)

{
  return (ushort)(param_1 + 0x9aU) < 0x38;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsHiragana
// Address: 01988ecc
// ==========================================================================================

bool Mono_Globalization_Unicode_MSCompatUnicodeTable__IsHiragana(short param_1)

{
  return (ushort)(param_1 + 0xcfbfU) < 0x54;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter
// Address: 01988ee4
// ==========================================================================================

uint Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter(uint param_1)

{
  ulong uVar1;
  ulong uVar2;
  
  if ((param_1 + 0x99 & 0xffff) < 9) {
    return 1;
  }
  if ((param_1 - 0x3041 & 0xffff) < 0xb9) {
    if ((param_1 & 0xffff) < 0x30aa) {
      if ((param_1 >> 2 & 0x3fff) < 0xc19) {
        uVar1 = (ulong)(param_1 - 0x3041);
        if ((param_1 - 0x3041 & 0xffff) < 0x23) {
          uVar2 = 0x400000155;
LAB_01988f9c:
          return (uint)(uVar2 >> (uVar1 & 0x3f)) & 1;
        }
      }
      else {
        uVar1 = (ulong)(param_1 - 0x3083);
        if ((param_1 - 0x3083 & 0xffff) < 0x27) {
          uVar2 = 0x5540000815;
          goto LAB_01988f9c;
        }
      }
    }
    else if ((param_1 >> 3 & 0x1fff) < 0x61d) {
      uVar1 = (ulong)(param_1 - 0x30c3);
      if ((param_1 - 0x30c3 & 0xffff) < 0x25) {
        uVar2 = 0x1500000001;
        goto LAB_01988f9c;
      }
    }
    else if ((param_1 - 0x30ee & 0xffff) < 9) {
      return 0x181U >> (ulong)(param_1 - 0x30ee & 0x1f) & 1;
    }
  }
  return 0;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__get_IsReady
// Address: 01988fcc
// ==========================================================================================

undefined Mono_Globalization_Unicode_MSCompatUnicodeTable__get_IsReady(void)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_02101602 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101602 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  return *(undefined *)(*(long *)(lVar2 + 0xb8) + 0x90);
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__UInt32FromBytePtr
// Address: 019890dc
// ==========================================================================================

undefined4
Mono_Globalization_Unicode_MSCompatUnicodeTable__UInt32FromBytePtr(long param_1,uint param_2)

{
  return CONCAT13(*(undefined *)(param_1 + (int)(param_2 + 3)),
                  CONCAT12(*(undefined *)(param_1 + (int)(param_2 + 2)),
                           CONCAT11(*(undefined *)(param_1 + (int)(param_2 + 1)),
                                    *(undefined *)(param_1 + (ulong)param_2))));
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable___cctor
// Address: 0198910c
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable___cctor(void)

{
  long lVar1;
  uint uVar2;
  uint uVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  char cVar9;
  char cVar10;
  char cVar11;
  char cVar12;
  char cVar13;
  char cVar14;
  char cVar15;
  char cVar16;
  undefined *puVar17;
  undefined *puVar18;
  undefined *puVar19;
  int iVar20;
  undefined8 uVar21;
  ulong uVar22;
  char *pcVar23;
  char *pcVar24;
  long lVar25;
  long lVar26;
  long lVar27;
  uint uVar28;
  int iVar29;
  int iVar30;
  long *plVar31;
  
  puVar19 = PTR_StringLiteral_7042_01fd2af8;
  puVar18 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  puVar17 = PTR_object_TypeInfo_01fbfcc0;
  if ((DAT_02101604 & 1) == 0) {
    FUN_00db0bbc(PTR_char___TypeInfo_01fc59b0);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_object_TypeInfo_01fbfcc0);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_TailoringInfo___TypeInfo_01fd2b00);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_TailoringInfo_TypeInfo_01fd2b08);
    FUN_00db0bbc(PTR_StringLiteral_7042_01fd2af8);
    FUN_00db0bbc(PTR_StringLiteral_7043_01fd2b10);
    DAT_02101604 = 1;
  }
  **(undefined4 **)(*(long *)puVar18 + 0xb8) = 3;
  uVar21 = thunk_FUN_00e11c14(*(undefined8 *)puVar17);
  System_Object___ctor(uVar21,0);
  *(undefined8 *)(*(long *)(*(long *)puVar18 + 0xb8) + 0x88) = uVar21;
  uVar21 = Method_Mono_Globalization_Unicode_MSCompatUnicodeTable_GetResource
                     (*(undefined8 *)puVar19);
  uVar22 = System_IntPtr__op_Equality(uVar21,0,0);
  puVar17 = PTR_StringLiteral_7043_01fd2b10;
  if ((uVar22 & 1) == 0) {
    pcVar23 = (char *)System_IntPtr__op_Explicit(uVar21,0);
    uVar21 = Method_Mono_Globalization_Unicode_MSCompatUnicodeTable_GetResource
                       (*(undefined8 *)puVar17);
    uVar22 = System_IntPtr__op_Equality(uVar21,0,0);
    if (((((uVar22 & 1) == 0) &&
         (pcVar24 = (char *)System_IntPtr__op_Explicit(uVar21,0), pcVar23 != (char *)0x0)) &&
        (pcVar24 != (char *)0x0)) && ((*pcVar23 == '\x03' && (*pcVar24 == '\x03')))) {
      iVar29 = *(int *)(pcVar23 + 1);
      lVar27 = *(long *)(*(long *)puVar18 + 0xb8);
      *(char **)(lVar27 + 8) = pcVar23 + 5;
      uVar2 = CONCAT13(pcVar23[iVar29 + 8],
                       CONCAT12(pcVar23[iVar29 + 7],
                                CONCAT11(pcVar23[iVar29 + 6],pcVar23[iVar29 + 5]))) + iVar29 + 9U;
      *(char **)(lVar27 + 0x10) = pcVar23 + (iVar29 + 9U);
      uVar28 = CONCAT13(pcVar23[(int)(uVar2 + 3)],
                        CONCAT12(pcVar23[(int)(uVar2 + 2)],
                                 CONCAT11(pcVar23[(int)(uVar2 + 1)],pcVar23[uVar2]))) + uVar2 + 4;
      *(char **)(lVar27 + 0x18) = pcVar23 + (uVar2 + 4);
      puVar17 = PTR_Mono_Globalization_Unicode_TailoringInfo___TypeInfo_01fd2b00;
      cVar4 = pcVar23[uVar28];
      cVar5 = pcVar23[(int)(uVar28 + 1)];
      cVar6 = pcVar23[(int)(uVar28 + 2)];
      cVar7 = pcVar23[(int)(uVar28 + 3)];
      *(char **)(lVar27 + 0x20) = pcVar23 + (uVar28 + 4);
      *(char **)(lVar27 + 0x28) =
           pcVar23 + (uVar28 + CONCAT13(cVar7,CONCAT12(cVar6,CONCAT11(cVar5,cVar4))) + 8);
      uVar2 = *(uint *)(pcVar24 + 1);
      uVar21 = FUN_00db0c30(*(undefined8 *)puVar17,(ulong)uVar2);
      *(undefined8 *)(*(long *)(*(long *)puVar18 + 0xb8) + 0x80) = uVar21;
      if (uVar2 == 0) {
        iVar29 = 5;
      }
      else {
        iVar30 = 1;
        lVar27 = 0;
        iVar20 = 8;
        do {
          iVar29 = iVar20;
          cVar4 = pcVar24[iVar29 - 3];
          cVar5 = pcVar24[iVar29 + -2];
          cVar6 = pcVar24[iVar29 + 5];
          cVar7 = pcVar24[iVar29 + 6];
          cVar8 = pcVar24[iVar29 + 1];
          cVar9 = pcVar24[iVar29 + 2];
          cVar10 = pcVar24[iVar29 + 7];
          cVar11 = pcVar24[iVar29 + -1];
          cVar12 = pcVar24[iVar29];
          cVar13 = pcVar24[iVar29 + 3];
          cVar14 = pcVar24[iVar29 + 4];
          cVar15 = pcVar24[iVar29 + 8];
          cVar16 = pcVar24[iVar29 + 9];
          lVar25 = thunk_FUN_00e11c14(*(undefined8 *)
                                       PTR_Mono_Globalization_Unicode_TailoringInfo_TypeInfo_01fd2b08
                                     );
          System_Object___ctor(lVar25,0);
          *(uint *)(lVar25 + 0x10) = CONCAT13(cVar12,CONCAT12(cVar11,CONCAT11(cVar5,cVar4)));
          *(uint *)(lVar25 + 0x14) = CONCAT13(cVar14,CONCAT12(cVar13,CONCAT11(cVar9,cVar8)));
          *(uint *)(lVar25 + 0x18) = CONCAT13(cVar15,CONCAT12(cVar10,CONCAT11(cVar7,cVar6)));
          *(bool *)(lVar25 + 0x1c) = cVar16 != '\0';
          plVar31 = *(long **)(*(long *)(*(long *)puVar18 + 0xb8) + 0x80);
          if (plVar31 == (long *)0x0) goto LAB_01989538;
          lVar26 = thunk_FUN_00e11b18(lVar25,*(undefined8 *)(*plVar31 + 0x40));
          if (lVar26 == 0) {
            uVar21 = thunk_FUN_00e29d2c();
                    /* WARNING: Subroutine does not return */
            FUN_00db0cb0(uVar21,0);
          }
          if (*(uint *)(plVar31 + 3) <= iVar30 - 1U) goto LAB_01989528;
          lVar26 = (long)iVar30;
          iVar30 = iVar30 + 1;
          plVar31[lVar27 + 4] = lVar25;
          lVar27 = lVar26;
          iVar20 = iVar29 + 0xd;
        } while (lVar26 < (long)(ulong)uVar2);
        iVar29 = iVar29 + 10;
      }
      uVar2 = CONCAT13(pcVar24[iVar29 + 5],
                       CONCAT12(pcVar24[iVar29 + 4],
                                CONCAT11(pcVar24[iVar29 + 3],pcVar24[iVar29 + 2])));
      lVar27 = FUN_00db0c30(*(undefined8 *)PTR_char___TypeInfo_01fc59b0,(ulong)uVar2);
      lVar25 = *(long *)(*(long *)puVar18 + 0xb8);
      *(long *)(lVar25 + 0x78) = lVar27;
      if (uVar2 != 0) {
        if (lVar27 == 0) {
LAB_01989538:
                    /* WARNING: Subroutine does not return */
          FUN_00db0de4();
        }
        uVar3 = *(uint *)(lVar27 + 0x18);
        lVar26 = 0;
        uVar28 = iVar29 + 6;
        iVar29 = 1;
        do {
          if (uVar3 <= iVar29 - 1U) {
LAB_01989528:
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          iVar30 = uVar28 + 1;
          uVar22 = (ulong)uVar28;
          lVar1 = lVar26 * 2;
          lVar26 = (long)iVar29;
          uVar28 = uVar28 + 2;
          iVar29 = iVar29 + 1;
          *(ushort *)(lVar27 + lVar1 + 0x20) = CONCAT11(pcVar24[iVar30],pcVar24[uVar22]);
        } while (lVar26 < (long)(ulong)uVar2);
      }
      *(undefined *)(lVar25 + 0x90) = 1;
    }
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJK
// Address: 0198953c
// ==========================================================================================

/* WARNING: Removing unreachable block (ram,0x01989634) */

void Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJK
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
               undefined8 param_5,undefined8 param_6)

{
  undefined *puVar1;
  long lVar2;
  undefined8 extraout_x1;
  undefined8 extraout_x1_00;
  undefined8 uVar3;
  undefined8 uVar4;
  char local_44 [4];
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_02101605 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101605 = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  uVar4 = *(undefined8 *)(*(long *)(lVar2 + 0xb8) + 0x88);
  local_44[0] = '\0';
                    /* try { // try from 019895b0 to 019895bf has its CatchHandler @ 01989640 */
  System_Threading_Monitor__Enter(uVar4,local_44,0);
  uVar3 = extraout_x1;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
                    /* try { // try from 019895cc to 019895e3 has its CatchHandler @ 01989644 */
    thunk_FUN_00df405c();
    uVar3 = extraout_x1_00;
  }
  Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJKCore(param_1,uVar3,param_3,param_4);
                    /* try { // try from 019895e4 to 019895ff has its CatchHandler @ 0198963c */
  Mono_Globalization_Unicode_MSCompatUnicodeTable__SetCJKReferences
            (param_1,param_2,param_3,param_4,param_5,param_6);
  if (local_44[0] != '\0') {
    System_Threading_Monitor__Exit(uVar4,0);
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJKCore
// Address: 0198969c
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJKCore
               (undefined8 param_1,undefined8 param_2,long *param_3,long *param_4,undefined8 param_5
               ,long *param_6)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  long lVar4;
  ulong uVar5;
  long *plVar6;
  long lVar7;
  long lVar8;
  undefined8 uVar9;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  
  puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_02101606 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_StringLiteral_8062_01fbfe10);
    FUN_00db0bbc(PTR_StringLiteral_7017_01fd2b18);
    FUN_00db0bbc(PTR_StringLiteral_8142_01fc3770);
    FUN_00db0bbc(PTR_StringLiteral_7041_01fd2b20);
    FUN_00db0bbc(PTR_StringLiteral_9724_01fd2ae0);
    FUN_00db0bbc(PTR_StringLiteral_7016_01fd2b28);
    FUN_00db0bbc(PTR_StringLiteral_9723_01fd2ad0);
    FUN_00db0bbc(PTR_StringLiteral_7015_01fd2b30);
    FUN_00db0bbc(PTR_StringLiteral_7044_01fd2b38);
    FUN_00db0bbc(PTR_StringLiteral_7018_01fd2b40);
    DAT_02101606 = 1;
  }
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  if (DAT_02101689 == '\0') {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101689 = '\x01';
  }
  lVar4 = *(long *)puVar2;
  if (*(int *)(lVar4 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar4 = *(long *)puVar2;
  }
  puVar3 = PTR_StringLiteral_9723_01fd2ad0;
  if (*(char *)(*(long *)(lVar4 + 0xb8) + 0x90) == '\0') {
    return;
  }
  uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_9723_01fd2ad0);
  if ((uVar5 & 1) == 0) {
    uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_9724_01fd2ae0);
    if ((uVar5 & 1) == 0) {
      uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8062_01fbfe10);
      if ((uVar5 & 1) == 0) {
        uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8142_01fc3770);
        if ((uVar5 & 1) == 0) {
          return;
        }
        lVar4 = *(long *)puVar2;
        lVar8 = *(long *)PTR_StringLiteral_7018_01fd2b40;
        if (*(int *)(lVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar4 = *(long *)puVar2;
        }
        lVar7 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x48);
        plVar6 = (long *)(*(long *)(lVar4 + 0xb8) + 0x68);
      }
      else {
        lVar4 = *(long *)puVar2;
        lVar8 = *(long *)PTR_StringLiteral_7017_01fd2b18;
        if (*(int *)(lVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar4 = *(long *)puVar2;
        }
        lVar7 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x40);
        plVar6 = (long *)(*(long *)(lVar4 + 0xb8) + 0x60);
      }
    }
    else {
      lVar4 = *(long *)puVar2;
      lVar8 = *(long *)PTR_StringLiteral_7016_01fd2b28;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar2;
      }
      lVar7 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x38);
      plVar6 = (long *)(*(long *)(lVar4 + 0xb8) + 0x58);
    }
  }
  else {
    lVar4 = *(long *)puVar2;
    lVar8 = *(long *)PTR_StringLiteral_7015_01fd2b30;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar7 = *(long *)(*(long *)(lVar4 + 0xb8) + 0x30);
    plVar6 = (long *)(*(long *)(lVar4 + 0xb8) + 0x50);
  }
  *param_3 = lVar7;
  lVar4 = *plVar6;
  *param_4 = lVar4;
  if (lVar8 == 0) {
    return;
  }
  if (lVar4 != 0) {
    return;
  }
  uVar9 = *(undefined8 *)PTR_StringLiteral_7044_01fd2b38;
  uStack_68 = 0;
  local_70 = 0;
  uStack_58 = 0;
  uStack_60 = 0;
  System_ParamsArray___ctor(&local_70,lVar8,0);
  uStack_88 = uStack_68;
  local_90 = local_70;
  uStack_78 = uStack_58;
  uStack_80 = uStack_60;
  uVar9 = Method_System_String_FormatHelper(0,uVar9,&local_90);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  uVar9 = Method_Mono_Globalization_Unicode_MSCompatUnicodeTable_GetResource(uVar9);
  uVar5 = System_IntPtr__op_Equality(uVar9,0,0);
  if ((uVar5 & 1) != 0) {
    return;
  }
  lVar4 = System_IntPtr__op_Explicit(uVar9,0);
  if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c(*(long *)puVar2);
  }
  uVar1 = *(uint *)(lVar4 + 1);
  *param_3 = lVar4 + 5;
  *param_4 = (ulong)uVar1 + lVar4 + 5;
  uVar5 = System_String__Equals(param_1,*(undefined8 *)puVar3);
  if ((uVar5 & 1) == 0) {
    uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_9724_01fd2ae0);
    if ((uVar5 & 1) == 0) {
      uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8062_01fbfe10);
      if ((uVar5 & 1) == 0) {
        uVar5 = System_String__Equals(param_1,*(undefined8 *)PTR_StringLiteral_8142_01fc3770);
        if ((uVar5 & 1) == 0) goto LAB_01989a88;
        lVar4 = *(long *)puVar2;
        lVar7 = *param_3;
        if (*(int *)(lVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar4 = *(long *)puVar2;
        }
        lVar4 = *(long *)(lVar4 + 0xb8);
        *(long *)(lVar4 + 0x48) = lVar7;
        plVar6 = (long *)(lVar4 + 0x68);
      }
      else {
        lVar4 = *(long *)puVar2;
        lVar7 = *param_3;
        if (*(int *)(lVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
          lVar4 = *(long *)puVar2;
        }
        lVar4 = *(long *)(lVar4 + 0xb8);
        *(long *)(lVar4 + 0x40) = lVar7;
        plVar6 = (long *)(lVar4 + 0x60);
      }
    }
    else {
      lVar4 = *(long *)puVar2;
      lVar7 = *param_3;
      if (*(int *)(lVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar4 = *(long *)puVar2;
      }
      lVar4 = *(long *)(lVar4 + 0xb8);
      *(long *)(lVar4 + 0x38) = lVar7;
      plVar6 = (long *)(lVar4 + 0x58);
    }
  }
  else {
    lVar4 = *(long *)puVar2;
    lVar7 = *param_3;
    if (*(int *)(lVar4 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar4 = *(long *)puVar2;
    }
    lVar4 = *(long *)(lVar4 + 0xb8);
    *(long *)(lVar4 + 0x30) = lVar7;
    plVar6 = (long *)(lVar4 + 0x50);
  }
  *plVar6 = *param_4;
LAB_01989a88:
  uVar5 = System_String__Equals(lVar8,*(undefined8 *)PTR_StringLiteral_7018_01fd2b40);
  if ((uVar5 & 1) != 0) {
    if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar9 = Method_Mono_Globalization_Unicode_MSCompatUnicodeTable_GetResource
                      (*(undefined8 *)PTR_StringLiteral_7041_01fd2b20);
    uVar5 = System_IntPtr__op_Equality(uVar9,0,0);
    if ((uVar5 & 1) == 0) {
      lVar4 = System_IntPtr__op_Explicit(uVar9,0);
      lVar8 = *(long *)puVar2;
      if (*(int *)(lVar8 + 0xe0) == 0) {
        thunk_FUN_00df405c(lVar8);
        lVar8 = *(long *)puVar2;
      }
      *(long *)(*(long *)(lVar8 + 0xb8) + 0x70) = lVar4 + 5;
      *param_6 = lVar4 + 5;
    }
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable___c___cctor
// Address: 01989b28
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable___c___cctor(void)

{
  undefined *puVar1;
  undefined8 uVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable___c_TypeInfo_01fd2ab8;
  if ((DAT_02101607 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable___c_TypeInfo_01fd2ab8);
    DAT_02101607 = 1;
  }
  uVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(uVar2,0);
  **(undefined8 **)(*(long *)puVar1 + 0xb8) = uVar2;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTable___c___ctor
// Address: 01989b84
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTable___c___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_MSCompatUnicodeTableUtil___cctor
// Address: 01989bb0
// ==========================================================================================

void Mono_Globalization_Unicode_MSCompatUnicodeTableUtil___cctor(void)

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
  long lVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined8 uVar21;
  undefined8 uVar22;
  undefined8 uVar23;
  undefined8 uVar24;
  undefined8 uVar25;
  
  puVar1 = PTR_int___TypeInfo_01fbf560;
  if ((DAT_02101608 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__042957A0DB5FF2D38A343AC5AE5F8635B88F10C32EB87A238B1DFB4756468476_01fd2b50
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__0F9E3C7E66CDEF5C44FA29E65CA676C480F7A2A4A067F70107FDC292C68D38B0_01fd2b58
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__2403FBEA85D0741C5727760E97EF16C9BF23294F21C0F1265A4BAF7F22202A64_01fd2b60
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__3D95E4501B1964D7FCE16E3F5682A038752B462357D87343880B1E819F6163FE_01fd2b68
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__42E1421FC2A5A6A33E964D7EB9603EB101818D858DDA09B2BC9B5A888C1C351C_01fd2b70
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__BB425A9B43E10C921902A25D07A4317DEFF9F606A788672E1B21633C143407F0_01fd2b78
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E32C465157D21F39B3DBF186A98FB02185C63B0260B47247A7A5FDF2B061EAA8_01fd2b80
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__E5F4F6214036DF103321A8A0CE30C2EF935694B4199D52BC538E7EF3F045CB92_01fd2b88
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__EF82B163CA8252A793A6E73F57775D843C9A21F65586926EB11893FA8BB603E9_01fd2b90
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__FEC387BA57A54BB6066E4CA8A4F9C0FF9C36B9CBD6600C3683F6FB1BDB5077EB_01fd2b98
                );
    DAT_02101608 = 1;
  }
  lVar11 = FUN_00db0c30(*(undefined8 *)puVar1,3);
  if (lVar11 != 0) {
    if ((1 < *(uint *)(lVar11 + 0x18)) &&
       (*(undefined4 *)(lVar11 + 0x24) = 0xa000,
       puVar10 = 
       PTR_Field__PrivateImplementationDetails__FEC387BA57A54BB6066E4CA8A4F9C0FF9C36B9CBD6600C3683F6FB1BDB5077EB_01fd2b98
       , puVar9 = 
         PTR_Field__PrivateImplementationDetails__EF82B163CA8252A793A6E73F57775D843C9A21F65586926EB11893FA8BB603E9_01fd2b90
       , puVar8 = 
         PTR_Field__PrivateImplementationDetails__E5F4F6214036DF103321A8A0CE30C2EF935694B4199D52BC538E7EF3F045CB92_01fd2b88
       , puVar7 = 
         PTR_Field__PrivateImplementationDetails__BB425A9B43E10C921902A25D07A4317DEFF9F606A788672E1B21633C143407F0_01fd2b78
       , puVar6 = 
         PTR_Field__PrivateImplementationDetails__42E1421FC2A5A6A33E964D7EB9603EB101818D858DDA09B2BC9B5A888C1C351C_01fd2b70
       , puVar5 = 
         PTR_Field__PrivateImplementationDetails__3D95E4501B1964D7FCE16E3F5682A038752B462357D87343880B1E819F6163FE_01fd2b68
       , puVar4 = 
         PTR_Field__PrivateImplementationDetails__2403FBEA85D0741C5727760E97EF16C9BF23294F21C0F1265A4BAF7F22202A64_01fd2b60
       , puVar3 = 
         PTR_Field__PrivateImplementationDetails__0F9E3C7E66CDEF5C44FA29E65CA676C480F7A2A4A067F70107FDC292C68D38B0_01fd2b58
       , puVar2 = 
         PTR_Field__PrivateImplementationDetails__042957A0DB5FF2D38A343AC5AE5F8635B88F10C32EB87A238B1DFB4756468476_01fd2b50
       , *(uint *)(lVar11 + 0x18) != 2)) {
      *(undefined4 *)(lVar11 + 0x28) = 0xf900;
      uVar12 = FUN_00db0c30(*(undefined8 *)puVar1,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar12,*(undefined8 *)puVar2,0);
      uVar13 = FUN_00db0c30(*(undefined8 *)puVar1,6);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar13,*(undefined8 *)puVar10,0);
      uVar14 = FUN_00db0c30(*(undefined8 *)puVar1,6);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar14,*(undefined8 *)puVar8,0);
      uVar15 = FUN_00db0c30(*(undefined8 *)puVar1,6);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar15,*(undefined8 *)puVar10,0);
      uVar16 = FUN_00db0c30(*(undefined8 *)puVar1,6);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar16,*(undefined8 *)puVar8,0);
      uVar17 = FUN_00db0c30(*(undefined8 *)puVar1,4);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar17,*(undefined8 *)puVar5,0);
      uVar18 = FUN_00db0c30(*(undefined8 *)puVar1,4);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar18,*(undefined8 *)puVar7,0);
      uVar19 = FUN_00db0c30(*(undefined8 *)puVar1,4);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar19,*(undefined8 *)puVar5,0);
      uVar20 = FUN_00db0c30(*(undefined8 *)puVar1,4);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar20,*(undefined8 *)puVar9,0);
      uVar21 = FUN_00db0c30(*(undefined8 *)puVar1,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar21,*(undefined8 *)puVar3,0);
      uVar22 = FUN_00db0c30(*(undefined8 *)puVar1,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar22,*(undefined8 *)puVar6,0);
      uVar23 = FUN_00db0c30(*(undefined8 *)puVar1,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar23,*(undefined8 *)puVar4,0);
      uVar24 = FUN_00db0c30(*(undefined8 *)puVar1,3);
      Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
                (uVar24,*(undefined8 *)
                         PTR_Field__PrivateImplementationDetails__E32C465157D21F39B3DBF186A98FB02185C63B0260B47247A7A5FDF2B061EAA8_01fd2b80
                 ,0);
      puVar2 = PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48;
      uVar25 = thunk_FUN_00e11c14(*(undefined8 *)
                                   PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48
                                 );
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar25,lVar11,uVar12,0xffffffff,0xffffffff)
      ;
      puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8;
      **(undefined8 **)
        (*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTableUtil_TypeInfo_01fd2ad8 + 0xb8)
           = uVar25;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar13,uVar14,0,0);
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 8) = uVar12;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar15,uVar16,0,0);
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x10) = uVar12;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar17,uVar18,0,0);
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x18) = uVar12;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar19,uVar20,0,0);
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x20) = uVar12;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar21,uVar22,0xffffffff,0xffffffff)
      ;
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x28) = uVar12;
      uVar12 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
      Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar12,uVar23,uVar24,0xffffffff,0xffffffff)
      ;
      *(undefined8 *)(*(long *)(*(long *)puVar1 + 0xb8) + 0x30) = uVar12;
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_NormalizationTableUtil___cctor
// Address: 01989fe4
// ==========================================================================================

void Mono_Globalization_Unicode_NormalizationTableUtil___cctor(void)

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
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined8 uVar21;
  
  puVar10 = 
  PTR_Field__PrivateImplementationDetails__C250CAD28060A4EB63B4C4A643DDA196CCD35FD2FC67FB749ADF4BAC6D62E1A0_01fd2be0
  ;
  puVar9 = 
  PTR_Field__PrivateImplementationDetails__D896D464C3726A21162F271ACB711464AD07EA9C9CE78E0297FD0DE934471FA6_01fd2bd8
  ;
  puVar8 = 
  PTR_Field__PrivateImplementationDetails__EBE07C3718876777F609CD22058F4C3A6CCCC695F5BDE90998DC1E12E0CBE63D_01fd2bd0
  ;
  puVar7 = 
  PTR_Field__PrivateImplementationDetails__4623CA5867960AA898AA1F65E720CD5ECD3552542E0C6F6FB65B21D14DD1CBC2_01fd2bc8
  ;
  puVar6 = 
  PTR_Field__PrivateImplementationDetails__A2DFDF9C2CED8BB1C0B9B06064345ACC9C22DFE5FEC9976FF061F0994451519B_01fd2bc0
  ;
  puVar5 = 
  PTR_Field__PrivateImplementationDetails__CAFFFC9D15E4037EE8FBDB1A45DFE456F0936BDC7310F1882EAF14B706A76658_01fd2bb8
  ;
  puVar4 = 
  PTR_Field__PrivateImplementationDetails__9960C7FC60CDD325C8A2A00995BE7064EAC3F6295C6A5C4E797D2281846131E4_01fd2bb0
  ;
  puVar3 = 
  PTR_Field__PrivateImplementationDetails__99E66DACA3EFF94776AF1258E0E5B2F4DF2900E4EA32351B0DF37A87F2426B1F_01fd2ba8
  ;
  puVar2 = 
  PTR_Field__PrivateImplementationDetails__508085E0DDEEA9CE48BFAE98CEC779F8D06301AE973555D37680D08190CAFA70_01fd2ba0
  ;
  puVar1 = PTR_int___TypeInfo_01fbf560;
  if ((DAT_02101609 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48);
    FUN_00db0bbc(PTR_int___TypeInfo_01fbf560);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8);
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__4623CA5867960AA898AA1F65E720CD5ECD3552542E0C6F6FB65B21D14DD1CBC2_01fd2bc8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__508085E0DDEEA9CE48BFAE98CEC779F8D06301AE973555D37680D08190CAFA70_01fd2ba0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__9960C7FC60CDD325C8A2A00995BE7064EAC3F6295C6A5C4E797D2281846131E4_01fd2bb0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__99E66DACA3EFF94776AF1258E0E5B2F4DF2900E4EA32351B0DF37A87F2426B1F_01fd2ba8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__A2DFDF9C2CED8BB1C0B9B06064345ACC9C22DFE5FEC9976FF061F0994451519B_01fd2bc0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__BABD01C34E7E65E57E4C431281E782B4101CE0644A8090AD6E501F1C6CF2C9DF_01fd2bf0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__C250CAD28060A4EB63B4C4A643DDA196CCD35FD2FC67FB749ADF4BAC6D62E1A0_01fd2be0
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__CAFFFC9D15E4037EE8FBDB1A45DFE456F0936BDC7310F1882EAF14B706A76658_01fd2bb8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__D896D464C3726A21162F271ACB711464AD07EA9C9CE78E0297FD0DE934471FA6_01fd2bd8
                );
    FUN_00db0bbc(
                PTR_Field__PrivateImplementationDetails__EBE07C3718876777F609CD22058F4C3A6CCCC695F5BDE90998DC1E12E0CBE63D_01fd2bd0
                );
    DAT_02101609 = 1;
  }
  uVar11 = FUN_00db0c30(*(undefined8 *)puVar1,0xb);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar11,*(undefined8 *)puVar2,0);
  uVar12 = FUN_00db0c30(*(undefined8 *)puVar1,0xb);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar12,*(undefined8 *)puVar3,0);
  uVar13 = FUN_00db0c30(*(undefined8 *)puVar1,9);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar13,*(undefined8 *)puVar4,0);
  uVar14 = FUN_00db0c30(*(undefined8 *)puVar1,9);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar14,*(undefined8 *)puVar5,0);
  uVar15 = FUN_00db0c30(*(undefined8 *)puVar1,0x1e);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar15,*(undefined8 *)puVar6,0);
  uVar16 = FUN_00db0c30(*(undefined8 *)puVar1,0x1e);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar16,*(undefined8 *)puVar7,0);
  uVar17 = FUN_00db0c30(*(undefined8 *)puVar1,3);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar17,*(undefined8 *)puVar8,0);
  uVar18 = FUN_00db0c30(*(undefined8 *)puVar1,3);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar18,*(undefined8 *)puVar9,0);
  uVar19 = FUN_00db0c30(*(undefined8 *)puVar1,9);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar19,*(undefined8 *)puVar10,0);
  uVar20 = FUN_00db0c30(*(undefined8 *)puVar1,9);
  Method_System_Runtime_CompilerServices_RuntimeHelpers_InitializeArray
            (uVar20,*(undefined8 *)
                     PTR_Field__PrivateImplementationDetails__BABD01C34E7E65E57E4C431281E782B4101CE0644A8090AD6E501F1C6CF2C9DF_01fd2bf0
             ,0);
  puVar1 = PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48;
  uVar21 = thunk_FUN_00e11c14(*(undefined8 *)
                               PTR_Mono_Globalization_Unicode_CodePointIndexer_TypeInfo_01fd2b48);
  Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar21,uVar11,uVar12,0,0);
  puVar2 = PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8;
  **(undefined8 **)
    (*(long *)PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8 + 0xb8) =
       uVar21;
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar11,uVar13,uVar14,0,0);
  *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 8) = uVar11;
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar11,uVar15,uVar16,0,0);
  *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x10) = uVar11;
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar11,uVar17,uVar18,0,0);
  *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x18) = uVar11;
  uVar11 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  Mono_Globalization_Unicode_CodePointIndexer___ctor(uVar11,uVar19,uVar20,0,0);
  *(undefined8 *)(*(long *)(*(long *)puVar2 + 0xb8) + 0x20) = uVar11;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_NormalizationTableUtil__PropIdx
// Address: 0198a32c
// ==========================================================================================

void Mono_Globalization_Unicode_NormalizationTableUtil__PropIdx(undefined4 param_1)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8;
  if ((DAT_0210160a & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8);
    DAT_0210160a = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  if (**(long **)(lVar2 + 0xb8) != 0) {
    Mono_Globalization_Unicode_CodePointIndexer__ToIndex(**(long **)(lVar2 + 0xb8),param_1);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_NormalizationTableUtil__MapIdx
// Address: 0198a394
// ==========================================================================================

void Mono_Globalization_Unicode_NormalizationTableUtil__MapIdx(undefined4 param_1)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8;
  if ((DAT_0210160b & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_NormalizationTableUtil_TypeInfo_01fd2be8);
    DAT_0210160b = 1;
  }
  lVar2 = *(long *)puVar1;
  if (*(int *)(lVar2 + 0xe0) == 0) {
    thunk_FUN_00df405c();
    lVar2 = *(long *)puVar1;
  }
  lVar2 = *(long *)(*(long *)(lVar2 + 0xb8) + 8);
  if (lVar2 != 0) {
    Mono_Globalization_Unicode_CodePointIndexer__ToIndex(lVar2,param_1);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator___ctor
// Address: 0198a3fc
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator___ctor(long param_1,long *param_2)

{
  ushort uVar1;
  ushort uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 uVar5;
  int iVar6;
  undefined8 uVar7;
  long lVar8;
  long *plVar9;
  uint uVar10;
  uint uVar11;
  long lVar12;
  long lVar13;
  long lVar14;
  
  if ((DAT_0210160c & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210160c = 1;
  }
  System_Object___ctor(param_1,0);
  puVar4 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  puVar3 = PTR_byte___TypeInfo_01fbf258;
  if (param_2 != (long *)0x0) {
    uVar5 = (**(code **)(*param_2 + 0x1a8))(param_2,*(undefined8 *)(*param_2 + 0x1b0));
    *(undefined4 *)(param_1 + 0x58) = uVar5;
    uVar7 = (**(code **)(*param_2 + 0x208))(param_2,*(undefined8 *)(*param_2 + 0x210));
    *(undefined8 *)(param_1 + 0x10) = uVar7;
    Mono_Globalization_Unicode_SimpleCollator__SetCJKTable
              (uVar7,param_2,param_1 + 0x18,param_1 + 0x38,param_1 + 0x40,param_1 + 0x50,
               param_1 + 0x48);
    plVar9 = param_2;
    do {
      iVar6 = (**(code **)(*plVar9 + 0x1a8))(plVar9,*(undefined8 *)(*plVar9 + 0x1b0));
      if (iVar6 == 0x7f) {
        if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        lVar8 = Mono_Globalization_Unicode_MSCompatUnicodeTable__GetTailoringInfo(0x7f);
        if (lVar8 != 0) {
LAB_0198a548:
          *(undefined *)(param_1 + 0x5c) = *(undefined *)(lVar8 + 0x1c);
          if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          Method_Mono_Globalization_Unicode_MSCompatUnicodeTable_BuildTailoringTables
                    (param_2,lVar8,param_1 + 0x20,param_1 + 0x28);
          uVar7 = FUN_00db0c30(*(undefined8 *)puVar3,0x60);
          lVar8 = *(long *)(param_1 + 0x20);
          *(undefined8 *)(param_1 + 0x30) = uVar7;
          if (lVar8 != 0) {
            uVar11 = *(uint *)(lVar8 + 0x18);
            if ((int)uVar11 < 1) goto LAB_0198a634;
            uVar10 = 0;
            goto LAB_0198a5a8;
          }
        }
        break;
      }
      uVar5 = (**(code **)(*plVar9 + 0x1a8))(plVar9,*(undefined8 *)(*plVar9 + 0x1b0));
      if (*(int *)(*(long *)puVar4 + 0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)puVar4);
      }
      lVar8 = Mono_Globalization_Unicode_MSCompatUnicodeTable__GetTailoringInfo(uVar5);
      if (lVar8 != 0) goto LAB_0198a548;
      plVar9 = (long *)(**(code **)(*plVar9 + 0x1f8))(plVar9,*(undefined8 *)(*plVar9 + 0x200));
    } while (plVar9 != (long *)0x0);
  }
LAB_0198a728:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
  while( true ) {
    lVar12 = *(long *)(lVar8 + (long)(int)uVar10 * 8 + 0x20);
    if ((lVar12 == 0) || (lVar12 = *(long *)(lVar12 + 0x18), lVar12 == 0)) goto LAB_0198a728;
    uVar11 = *(uint *)(lVar12 + 0x18);
    if (1 < (int)uVar11) {
      lVar13 = 0;
      do {
        if (uVar11 <= (uint)lVar13) goto LAB_0198a724;
        lVar14 = *(long *)(param_1 + 0x30);
        if (lVar14 == 0) goto LAB_0198a728;
        uVar1 = *(ushort *)(lVar12 + 0x20 + lVar13 * 2);
        uVar2 = uVar1 >> 3;
        if (*(uint *)(lVar14 + 0x18) <= (uint)uVar2) goto LAB_0198a724;
        lVar14 = lVar14 + (ulong)uVar2;
        lVar13 = lVar13 + 1;
        *(byte *)(lVar14 + 0x20) = *(byte *)(lVar14 + 0x20) | (byte)(1 << ((ulong)uVar1 & 7));
        uVar11 = *(uint *)(lVar12 + 0x18);
      } while ((int)lVar13 < (int)uVar11);
    }
    uVar11 = *(uint *)(lVar8 + 0x18);
    uVar10 = uVar10 + 1;
    if ((int)uVar11 <= (int)uVar10) break;
LAB_0198a5a8:
    if (uVar11 <= uVar10) goto LAB_0198a724;
  }
LAB_0198a634:
  puVar3 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (*(int *)(param_1 + 0x58) != 0x7f) {
    lVar8 = *(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
    if (*(int *)(lVar8 + 0xe0) == 0) {
      thunk_FUN_00df405c();
      lVar8 = *(long *)puVar3;
    }
    if ((**(long **)(lVar8 + 0xb8) == 0) ||
       (lVar8 = *(long *)(**(long **)(lVar8 + 0xb8) + 0x20), lVar8 == 0)) goto LAB_0198a728;
    uVar11 = *(uint *)(lVar8 + 0x18);
    if (0 < (int)uVar11) {
      uVar10 = 0;
      do {
        if (uVar11 <= uVar10) {
LAB_0198a724:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar12 = *(long *)(lVar8 + (long)(int)uVar10 * 8 + 0x20);
        if ((lVar12 == 0) || (lVar12 = *(long *)(lVar12 + 0x18), lVar12 == 0)) goto LAB_0198a728;
        uVar11 = *(uint *)(lVar12 + 0x18);
        if (1 < (int)uVar11) {
          lVar13 = 0;
          do {
            if (uVar11 <= (uint)lVar13) goto LAB_0198a724;
            lVar14 = *(long *)(param_1 + 0x30);
            if (lVar14 == 0) goto LAB_0198a728;
            uVar1 = *(ushort *)(lVar12 + 0x20 + lVar13 * 2);
            uVar2 = uVar1 >> 3;
            if (*(uint *)(lVar14 + 0x18) <= (uint)uVar2) goto LAB_0198a724;
            lVar14 = lVar14 + (ulong)uVar2;
            lVar13 = lVar13 + 1;
            *(byte *)(lVar14 + 0x20) = *(byte *)(lVar14 + 0x20) | (byte)(1 << ((ulong)uVar1 & 7));
            uVar11 = *(uint *)(lVar12 + 0x18);
          } while ((int)lVar13 < (int)uVar11);
        }
        uVar11 = *(uint *)(lVar8 + 0x18);
        uVar10 = uVar10 + 1;
      } while ((int)uVar10 < (int)uVar11);
    }
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__SetCJKTable
// Address: 0198a72c
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__SetCJKTable
               (undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
               undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  undefined *puVar1;
  long *plVar2;
  undefined8 uVar3;
  
  puVar1 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if ((DAT_0210160d & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210160d = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  plVar2 = (long *)Mono_Globalization_Unicode_SimpleCollator__GetNeutralCulture(param_2);
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if (plVar2 != (long *)0x0) {
    uVar3 = (**(code **)(*plVar2 + 0x1b8))(plVar2,*(undefined8 *)(*plVar2 + 0x1c0));
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    Mono_Globalization_Unicode_MSCompatUnicodeTable__FillCJK
              (uVar3,param_3,param_4,param_5,param_6,param_7);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetNeutralCulture
// Address: 0198a808
// ==========================================================================================

long * Mono_Globalization_Unicode_SimpleCollator__GetNeutralCulture(long *param_1)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  
  if (param_1 != (long *)0x0) {
    do {
      lVar2 = (**(code **)(*param_1 + 0x1f8))(param_1,*(undefined8 *)(*param_1 + 0x200));
      if (lVar2 == 0) {
        return param_1;
      }
      plVar3 = (long *)(**(code **)(*param_1 + 0x1f8))(param_1,*(undefined8 *)(*param_1 + 0x200));
      if (plVar3 == (long *)0x0) break;
      iVar1 = (**(code **)(*plVar3 + 0x1a8))(plVar3,*(undefined8 *)(*plVar3 + 0x1b0));
      if (iVar1 == 0x7f) {
        return param_1;
      }
      param_1 = (long *)(**(code **)(*param_1 + 0x1f8))(param_1,*(undefined8 *)(*param_1 + 0x200));
    } while (param_1 != (long *)0x0);
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__Category
// Address: 0198a878
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__Category(long param_1,int param_2)

{
  undefined *puVar1;
  uint uVar2;
  ulong uVar3;
  
  if ((DAT_0210160e & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_0210160e = 1;
  }
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((0x2fff < param_2) && (*(long *)(param_1 + 0x38) != 0)) {
    if (*(long *)(param_1 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar2 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(*(long *)(param_1 + 0x18),param_2);
    if (-1 < (int)uVar2) {
      return (ulong)*(byte *)(*(long *)(param_1 + 0x38) + (ulong)uVar2);
    }
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Category(param_2);
  return uVar3;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__Level1
// Address: 0198a90c
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__Level1(long param_1,int param_2)

{
  undefined *puVar1;
  uint uVar2;
  ulong uVar3;
  
  if ((DAT_0210160f & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_0210160f = 1;
  }
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((0x2fff < param_2) && (*(long *)(param_1 + 0x40) != 0)) {
    if (*(long *)(param_1 + 0x18) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar2 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex(*(long *)(param_1 + 0x18),param_2);
    if (-1 < (int)uVar2) {
      return (ulong)*(byte *)(*(long *)(param_1 + 0x40) + (ulong)uVar2);
    }
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level1(param_2);
  return uVar3;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__Level2
// Address: 0198a9a0
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__Level2(long param_1,int param_2,int param_3)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  uint uVar4;
  ulong uVar5;
  long lVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  
  if ((DAT_02101610 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101610 = 1;
  }
  if (param_3 == 3) {
    uVar5 = 0;
  }
  else {
    if (param_3 != 4) {
      if ((param_2 < 0x3000) || (*(long *)(param_1 + 0x48) == 0)) {
        if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40
                    + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar5 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level2(param_2);
        return uVar5;
      }
      if (*(long *)(param_1 + 0x50) != 0) {
        uVar4 = Mono_Globalization_Unicode_CodePointIndexer__ToIndex
                          (*(long *)(param_1 + 0x50),param_2);
        if ((-1 < (int)uVar4) &&
           (bVar2 = *(byte *)(*(long *)(param_1 + 0x48) + (ulong)uVar4), bVar2 != 0)) {
          return (ulong)bVar2;
        }
        if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40
                    + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar5 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level2(param_2);
        lVar6 = *(long *)(param_1 + 0x28);
        if (lVar6 != 0) {
          if (*(long *)(lVar6 + 0x18) == 0) {
            return uVar5;
          }
          iVar7 = (int)*(long *)(lVar6 + 0x18);
          if (iVar7 < 1) {
            return uVar5;
          }
          iVar8 = 0;
          while (lVar9 = *(long *)(lVar6 + (long)iVar8 * 8 + 0x20), lVar9 != 0) {
            bVar1 = *(byte *)(lVar9 + 0x10);
            bVar2 = (byte)uVar5;
            if (bVar1 == bVar2) {
              return (ulong)*(byte *)(lVar9 + 0x11);
            }
            if (bVar2 <= bVar1 && bVar1 != bVar2) {
              return uVar5;
            }
            bVar3 = iVar7 + -1 == iVar8;
            iVar8 = iVar8 + 1;
            if (bVar3) {
              return uVar5;
            }
          }
        }
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar5 = 5;
  }
  return uVar5;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsHalfKana
// Address: 0198aad4
// ==========================================================================================

bool Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(short param_1,uint param_2)

{
  bool bVar1;
  
  if ((DAT_02101611 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101611 = 1;
  }
  if ((param_2 >> 4 & 1) == 0) {
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    bVar1 = (ushort)(param_1 + 0x9aU) < 0x38;
  }
  else {
    bVar1 = true;
  }
  return bVar1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetContraction
// Address: 0198ab48
// ==========================================================================================

long Mono_Globalization_Unicode_SimpleCollator__GetContraction
               (long param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined *puVar1;
  long lVar2;
  
  lVar2 = param_1;
  if ((DAT_02101612 & 1) == 0) {
    lVar2 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101612 = 1;
  }
  lVar2 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                    (lVar2,param_2,param_3,param_4,*(undefined8 *)(param_1 + 0x20));
  puVar1 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (lVar2 == 0) {
    if (*(int *)(param_1 + 0x58) != 0x7f) {
      lVar2 = *(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
      if (*(int *)(lVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar2 = *(long *)puVar1;
      }
      if (**(long **)(lVar2 + 0xb8) != 0) {
        lVar2 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                          (lVar2,param_2,param_3,param_4,
                           *(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x20));
        return lVar2;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar2 = 0;
  }
  return lVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetContraction
// Address: 0198ac08
// ==========================================================================================

long Mono_Globalization_Unicode_SimpleCollator__GetContraction
               (undefined8 param_1,long param_2,uint param_3,int param_4,long param_5)

{
  ulong uVar1;
  uint uVar2;
  ushort uVar3;
  int iVar4;
  long lVar5;
  ulong uVar6;
  long lVar7;
  uint uVar8;
  ulong uVar9;
  
  if (param_5 != 0) {
    uVar2 = *(uint *)(param_5 + 0x18);
    if (0 < (int)uVar2) {
      uVar8 = 0;
      do {
        if (uVar2 <= uVar8) {
LAB_0198ad54:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar7 = *(long *)(param_5 + (long)(int)uVar8 * 8 + 0x20);
        if ((lVar7 == 0) || (lVar5 = *(long *)(lVar7 + 0x18), lVar5 == 0)) goto LAB_0198ad58;
        if (*(int *)(lVar5 + 0x18) == 0) goto LAB_0198ad54;
        if (param_2 == 0) goto LAB_0198ad58;
        uVar3 = *(ushort *)(lVar5 + 0x20);
        if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)param_3) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        iVar4 = (uint)uVar3 - (uint)*(ushort *)(param_2 + 0x14 + (long)(int)param_3 * 2);
        if (0 < iVar4) {
          return 0;
        }
        if (-1 < iVar4) {
          lVar5 = *(long *)(lVar7 + 0x18);
          if (lVar5 == 0) goto LAB_0198ad58;
          iVar4 = (int)*(ulong *)(lVar5 + 0x18);
          if (iVar4 <= (int)(param_4 - param_3)) {
            if (iVar4 < 1) {
              return lVar7;
            }
            uVar9 = 0;
            uVar6 = *(ulong *)(lVar5 + 0x18) & 0xffffffff;
            while( true ) {
              uVar1 = param_3 + uVar9;
              if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar1 & 0xffffffff)) {
                Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
                uVar6 = (ulong)*(uint *)(lVar5 + 0x18);
              }
              if (uVar6 <= uVar9) goto LAB_0198ad54;
              if (*(short *)(param_2 + 0x14 + (long)(int)uVar1 * 2) !=
                  *(short *)(lVar5 + 0x20 + uVar9 * 2)) break;
              uVar9 = uVar9 + 1;
              if ((long)(int)uVar6 <= (long)uVar9) {
                return lVar7;
              }
            }
          }
        }
        uVar2 = *(uint *)(param_5 + 0x18);
        uVar8 = uVar8 + 1;
      } while ((int)uVar8 < (int)uVar2);
    }
    return 0;
  }
LAB_0198ad58:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetTailContraction
// Address: 0198ad5c
// ==========================================================================================

long Mono_Globalization_Unicode_SimpleCollator__GetTailContraction
               (long param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined *puVar1;
  long lVar2;
  
  lVar2 = param_1;
  if ((DAT_02101613 & 1) == 0) {
    lVar2 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101613 = 1;
  }
  lVar2 = Method_Mono_Globalization_Unicode_SimpleCollator_GetTailContraction
                    (lVar2,param_2,param_3,param_4,*(undefined8 *)(param_1 + 0x20));
  puVar1 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (lVar2 == 0) {
    if (*(int *)(param_1 + 0x58) != 0x7f) {
      lVar2 = *(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
      if (*(int *)(lVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar2 = *(long *)puVar1;
      }
      if (**(long **)(lVar2 + 0xb8) != 0) {
        lVar2 = Method_Mono_Globalization_Unicode_SimpleCollator_GetTailContraction
                          (lVar2,param_2,param_3,param_4,
                           *(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x20));
        return lVar2;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar2 = 0;
  }
  return lVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetContraction
// Address: 0198b02c
// ==========================================================================================

long Mono_Globalization_Unicode_SimpleCollator__GetContraction(long param_1,undefined4 param_2)

{
  undefined *puVar1;
  long lVar2;
  
  lVar2 = param_1;
  if ((DAT_02101614 & 1) == 0) {
    lVar2 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101614 = 1;
  }
  lVar2 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                    (lVar2,param_2,*(undefined8 *)(param_1 + 0x20));
  puVar1 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (lVar2 == 0) {
    if (*(int *)(param_1 + 0x58) != 0x7f) {
      lVar2 = *(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
      if (*(int *)(lVar2 + 0xe0) == 0) {
        thunk_FUN_00df405c();
        lVar2 = *(long *)puVar1;
      }
      if (**(long **)(lVar2 + 0xb8) != 0) {
        lVar2 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                          (lVar2,param_2,*(undefined8 *)(**(long **)(lVar2 + 0xb8) + 0x20));
        return lVar2;
      }
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    lVar2 = 0;
  }
  return lVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetContraction
// Address: 0198b0c8
// ==========================================================================================

long Mono_Globalization_Unicode_SimpleCollator__GetContraction
               (undefined8 param_1,ushort param_2,long param_3)

{
  int iVar1;
  long lVar2;
  int iVar3;
  long lVar4;
  
  if (param_3 != 0) {
    iVar1 = *(int *)(param_3 + 0x18);
    if (0 < iVar1) {
      iVar3 = 0;
      do {
        if (iVar1 == iVar3) {
LAB_0198b13c:
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        lVar2 = *(long *)(param_3 + (long)iVar3 * 8 + 0x20);
        if ((lVar2 == 0) || (lVar4 = *(long *)(lVar2 + 0x18), lVar4 == 0)) goto LAB_0198b138;
        if (*(int *)(lVar4 + 0x18) == 0) goto LAB_0198b13c;
        if (param_2 < *(ushort *)(lVar4 + 0x20)) {
          return 0;
        }
        if ((*(int *)(lVar4 + 0x18) == 1) && (*(ushort *)(lVar4 + 0x20) == param_2)) {
          return lVar2;
        }
        iVar3 = iVar3 + 1;
      } while (iVar1 != iVar3);
    }
    return 0;
  }
LAB_0198b138:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__FilterOptions
// Address: 0198b140
// ==========================================================================================

uint Mono_Globalization_Unicode_SimpleCollator__FilterOptions
               (long param_1,uint param_2,uint param_3)

{
  undefined *puVar1;
  uint uVar2;
  long *plVar3;
  
  if ((DAT_02101615 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101615 = 1;
  }
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((param_3 >> 4 & 1) != 0) {
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar2 = Mono_Globalization_Unicode_MSCompatUnicodeTable__ToWidthCompat(param_2);
    if (uVar2 != 0) {
      param_2 = uVar2;
    }
  }
  if ((param_3 >> 0x1c & 1) != 0) {
    plVar3 = *(long **)(param_1 + 0x10);
    if (plVar3 == (long *)0x0) goto LAB_0198b228;
    param_2 = (**(code **)(*plVar3 + 0x208))(plVar3,param_2,*(undefined8 *)(*plVar3 + 0x210));
    param_2 = param_2 & 0xffff;
  }
  if ((param_3 & 1) != 0) {
    plVar3 = *(long **)(param_1 + 0x10);
    if (plVar3 == (long *)0x0) {
LAB_0198b228:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    param_2 = (**(code **)(*plVar3 + 0x208))(plVar3,param_2,*(undefined8 *)(*plVar3 + 0x210));
    param_2 = param_2 & 0xffff;
  }
  uVar2 = param_2;
  if ((param_3 >> 3 & 1) != 0) {
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar2 = param_2 + 0x60;
    if (0x53 < param_2 - 0x3041) {
      uVar2 = param_2;
    }
  }
  return uVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetExtenderType
// Address: 0198b22c
// ==========================================================================================

undefined4 Mono_Globalization_Unicode_SimpleCollator__GetExtenderType(long param_1,uint param_2)

{
  bool bVar1;
  undefined4 uVar2;
  uint uVar3;
  
  if (param_2 == 0x2015) {
    bVar1 = *(int *)(param_1 + 0x58) == 0x10;
  }
  else {
    if (0xcf6b < param_2 - 0x3005) {
      return 0;
    }
    if ((int)param_2 < 0xfe7c) {
      if ((int)param_2 < 0x30ff) {
        if ((int)param_2 < 0x3033) {
          if (param_2 == 0x3005) {
            return 4;
          }
          if (param_2 - 0x3031 < 2) {
            return 1;
          }
        }
        else {
          if ((int)param_2 < 0x30fc) {
            if (param_2 == 0x309d) {
              return 1;
            }
            uVar3 = 0x309e;
          }
          else {
            if (param_2 == 0x30fc) {
              return 3;
            }
            if (param_2 == 0x30fd) {
              return 1;
            }
            uVar3 = 0x30fe;
          }
          if (param_2 == uVar3) {
            return 2;
          }
        }
      }
      return 0;
    }
    if (param_2 >> 1 == 0x7f3e) {
      return 1;
    }
    bVar1 = param_2 == 0xff70;
  }
  uVar2 = 3;
  if (!bVar1) {
    uVar2 = 0;
  }
  return uVar2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__ToDashTypeValue
// Address: 0198b32c
// ==========================================================================================

undefined4 Mono_Globalization_Unicode_SimpleCollator__ToDashTypeValue(int param_1,uint param_2)

{
  undefined4 uVar1;
  
  if ((param_1 != 0) && ((param_2 >> 1 & 1) == 0)) {
    uVar1 = 4;
    if (param_1 == 3) {
      uVar1 = 5;
    }
    return uVar1;
  }
  return 3;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__FilterExtender
// Address: 0198b34c
// ==========================================================================================

uint Mono_Globalization_Unicode_SimpleCollator__FilterExtender
               (undefined8 param_1,uint param_2,int param_3,undefined4 param_4)

{
  undefined *puVar1;
  bool bVar2;
  uint uVar3;
  ulong uVar4;
  uint uVar5;
  
  if ((DAT_02101616 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101616 = 1;
  }
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if (param_3 != 3) {
    return param_2;
  }
  if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 + 0xe0
              ) == 0) {
    thunk_FUN_00df405c();
  }
  if (0x3040 < (param_2 & 0xffff)) {
    if (0x37 < (param_2 + 0x9a & 0xffff)) {
      uVar3 = param_2 >> 8 & 0xff;
      if (0x32 < uVar3) {
        return param_2;
      }
      if ((ushort)param_2 < 0x309d) {
        if (0x3098 < (param_2 & 0xffff)) {
          return param_2;
        }
      }
      else if (uVar3 < 0x31) {
        if ((param_2 & 0xffff) == 0x30fb) {
          return param_2;
        }
      }
      else if (0x2e < (param_2 - 0x32d0 & 0xffff)) {
        return param_2;
      }
    }
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0) ==
        0) {
      thunk_FUN_00df405c();
    }
    uVar4 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(param_2 & 0xffff,param_4);
    if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)puVar1);
    }
    uVar3 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,param_2);
    if (4 < (uVar3 & 7) - 2) {
      return param_2;
    }
    param_2 = param_2 - 0x3041;
    switch(uVar3 & 7) {
    case 2:
      if ((uVar4 & 1) != 0) {
        return 0xff71;
      }
      if ((param_2 & 0xffff) < 0x54) {
        return 0x3042;
      }
      return 0x30a2;
    case 3:
      uVar3 = 0x3044;
      if (0x53 < (param_2 & 0xffff)) {
        uVar3 = 0x30a4;
      }
      if ((uVar4 & 1) != 0) {
        return 0xff72;
      }
      return uVar3;
    case 4:
      uVar3 = 0x3046;
      if (0x53 < (param_2 & 0xffff)) {
        uVar3 = 0x30a6;
      }
      bVar2 = (uVar4 & 1) == 0;
      uVar5 = 0xff73;
      break;
    case 5:
      uVar3 = 0x3048;
      if (0x53 < (param_2 & 0xffff)) {
        uVar3 = 0x30a8;
      }
      bVar2 = (uVar4 & 1) == 0;
      uVar5 = 0xff74;
      break;
    case 6:
      uVar3 = 0x304a;
      if (0x53 < (param_2 & 0xffff)) {
        uVar3 = 0x30aa;
      }
      bVar2 = (uVar4 & 1) == 0;
      uVar5 = 0xff75;
    }
    if (bVar2) {
      uVar5 = uVar3;
    }
    return uVar5;
  }
  return param_2;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsIgnorable
// Address: 0198b55c
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(undefined4 param_1,ulong param_2)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((DAT_02101617 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101617 = 1;
  }
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar2 = (uint)((param_2 & 0xffffffff) >> 1);
  Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorable
            (param_1,uVar2 & 2 | (uVar2 & 1) << 2 | (uint)((param_2 & 0x50000000) == 0));
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsSafe
// Address: 0198b5d8
// ==========================================================================================

bool Mono_Globalization_Unicode_SimpleCollator__IsSafe(long param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  bool bVar3;
  long lVar4;
  
  lVar4 = *(long *)(param_1 + 0x30);
  if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  iVar2 = param_2 + 7;
  if (-1 < param_2) {
    iVar2 = param_2;
  }
  uVar1 = iVar2 >> 3;
  if ((int)uVar1 < (int)*(uint *)(lVar4 + 0x18)) {
    if (*(uint *)(lVar4 + 0x18) <= uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    bVar3 = (*(byte *)(lVar4 + (int)uVar1 + 0x20) >> (ulong)(param_2 + uVar1 * -8 & 0x1f) & 1) == 0;
  }
  else {
    bVar3 = true;
  }
  return bVar3;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetSortKey
// Address: 0198b634
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__GetSortKey
               (undefined8 param_1,long param_2,undefined4 param_3)

{
  if (param_2 != 0) {
    Mono_Globalization_Unicode_SimpleCollator__GetSortKey
              (param_1,param_2,0,*(undefined4 *)(param_2 + 0x10),param_3);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetSortKey
// Address: 0198b654
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__GetSortKey
               (long param_1,undefined8 param_2,int param_3,int param_4,undefined4 param_5)

{
  undefined *puVar1;
  long lVar2;
  
  puVar1 = PTR_Mono_Globalization_Unicode_SortKeyBuffer_TypeInfo_01fd2c18;
  if ((DAT_02101618 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SortKeyBuffer_TypeInfo_01fd2c18);
    DAT_02101618 = 1;
  }
  lVar2 = thunk_FUN_00e11c14(*(undefined8 *)puVar1);
  System_Object___ctor(lVar2,0);
  if (lVar2 != 0) {
    Mono_Globalization_Unicode_SortKeyBuffer__Initialize
              (lVar2,param_5,*(undefined4 *)(param_1 + 0x58),param_2,*(undefined *)(param_1 + 0x5c))
    ;
    Mono_Globalization_Unicode_SimpleCollator__GetSortKey
              (param_1,param_2,param_3,param_4 + param_3,lVar2,param_5);
    Mono_Globalization_Unicode_SortKeyBuffer__GetResult(lVar2);
    *(undefined *)(lVar2 + 0x82) = 0;
    *(undefined8 *)(lVar2 + 0x60) = 0;
    *(undefined8 *)(lVar2 + 0x58) = 0;
    *(undefined8 *)(lVar2 + 0x70) = 0;
    *(undefined8 *)(lVar2 + 0x68) = 0;
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer___ctor
// Address: 0198b71c
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer___ctor(undefined8 param_1)

{
  System_Object___ctor(param_1,0);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__Initialize
// Address: 0198b724
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__Initialize
               (long param_1,uint param_2,undefined4 param_3,long param_4,byte param_5)

{
  int iVar1;
  undefined *puVar2;
  undefined8 uVar3;
  uint uVar4;
  
  if ((DAT_02101624 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_02101624 = 1;
  }
  *(long *)(param_1 + 0x50) = param_4;
  *(undefined4 *)(param_1 + 0x78) = param_3;
  *(uint *)(param_1 + 0x7c) = param_2;
  puVar2 = PTR_byte___TypeInfo_01fbf258;
  if (param_4 != 0) {
    iVar1 = *(int *)(param_4 + 0x10);
    uVar4 = (param_2 >> 1 ^ 0xffffffff) & 1;
    *(char *)(param_1 + 0x80) = (char)uVar4;
    *(byte *)(param_1 + 0x81) = param_5 & 1;
    if ((*(long *)(param_1 + 0x10) == 0) || (*(int *)(*(long *)(param_1 + 0x10) + 0x18) < iVar1)) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,iVar1 * 2 + 10);
      uVar4 = (uint)*(byte *)(param_1 + 0x80);
      *(undefined8 *)(param_1 + 0x10) = uVar3;
    }
    if ((uVar4 != 0) &&
       ((*(long *)(param_1 + 0x18) == 0 || (*(int *)(*(long *)(param_1 + 0x18) + 0x18) < iVar1)))) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,iVar1 + 10);
      *(undefined8 *)(param_1 + 0x18) = uVar3;
    }
    if ((*(long *)(param_1 + 0x20) == 0) || (*(int *)(*(long *)(param_1 + 0x20) + 0x18) < iVar1)) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,iVar1 + 10);
      *(undefined8 *)(param_1 + 0x20) = uVar3;
    }
    if (*(long *)(param_1 + 0x28) == 0) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,10);
      *(undefined8 *)(param_1 + 0x28) = uVar3;
    }
    if (*(long *)(param_1 + 0x30) == 0) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,10);
      *(undefined8 *)(param_1 + 0x30) = uVar3;
    }
    if (*(long *)(param_1 + 0x38) == 0) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,10);
      *(undefined8 *)(param_1 + 0x38) = uVar3;
    }
    if (*(long *)(param_1 + 0x40) == 0) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,10);
      *(undefined8 *)(param_1 + 0x40) = uVar3;
    }
    if (*(long *)(param_1 + 0x48) == 0) {
      uVar3 = FUN_00db0c30(*(undefined8 *)puVar2,10);
      *(undefined8 *)(param_1 + 0x48) = uVar3;
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__GetSortKey
// Address: 0198b89c
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__GetSortKey
               (undefined8 param_1,long param_2,uint param_3,int param_4,long param_5,
               undefined4 param_6)

{
  undefined uVar1;
  undefined2 uVar2;
  undefined uVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  ulong uVar7;
  long lVar8;
  uint uVar9;
  long lVar10;
  uint uVar11;
  int iVar12;
  ulong uVar13;
  undefined4 uVar14;
  undefined4 local_b0 [6];
  byte *local_98;
  byte *local_90;
  undefined *local_88;
  int local_7c;
  long local_78;
  long local_70;
  long local_68;
  
  uVar13 = (ulong)param_3;
  if ((DAT_02101619 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101619 = 1;
  }
  lVar10 = 0;
  local_b0[0] = 0;
  do {
    *(undefined *)((long)local_b0 + lVar10) = 0;
    lVar10 = lVar10 + 1;
  } while (lVar10 != 4);
  if ((int)param_3 < param_4) {
    if (param_2 == 0) {
LAB_0198bc20:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    local_68 = param_2 + 0x14;
    local_88 = (undefined *)((ulong)local_b0 | 1);
    local_90 = (byte *)((ulong)local_b0 | 2);
    local_98 = (byte *)((ulong)local_b0 | 3);
    uVar14 = 0xffffffff;
    local_7c = param_4;
    local_78 = param_2;
    local_70 = param_5;
    do {
      iVar12 = (int)uVar13;
      if ((long)*(int *)(param_2 + 0x10) <= (long)uVar13) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      uVar2 = *(undefined2 *)(local_68 + (long)iVar12 * 2);
      iVar4 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType(param_1,uVar2);
      if (iVar4 == 0) {
        if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0
                    ) == 0) {
          thunk_FUN_00df405c();
        }
        uVar7 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar2,param_6);
        if ((uVar7 & 1) == 0) {
          uVar6 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions(param_1,uVar2,param_6);
          lVar10 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                             (param_1,param_2,uVar13,param_4);
          if (lVar10 == 0) {
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            uVar13 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(uVar6);
            if ((uVar13 & 1) == 0) {
              uVar14 = uVar6;
            }
            Mono_Globalization_Unicode_SimpleCollator__FillSortKeyRaw
                      (param_1,uVar6,0,param_5,param_6);
            param_2 = local_78;
            param_4 = local_7c;
          }
          else {
            lVar8 = *(long *)(lVar10 + 0x20);
            if (lVar8 == 0) {
              lVar8 = *(long *)(lVar10 + 0x28);
              if (lVar8 == 0) goto LAB_0198bc20;
              uVar13 = 0;
              while ((long)uVar13 < (long)(int)*(uint *)(lVar8 + 0x18)) {
                if (*(uint *)(lVar8 + 0x18) <= uVar13) {
                    /* WARNING: Subroutine does not return */
                  FUN_00db0dec();
                }
                *(undefined *)((long)local_b0 + uVar13) = *(undefined *)(lVar8 + uVar13 + 0x20);
                lVar8 = *(long *)(lVar10 + 0x28);
                uVar13 = uVar13 + 1;
                if (lVar8 == 0) goto LAB_0198bc20;
              }
              uVar3 = (undefined)local_b0[0];
              uVar11 = (uint)*local_90;
              uVar1 = *local_88;
              if (*local_90 == 1) {
                uVar11 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar6,0);
              }
              uVar9 = (uint)*local_98;
              if (*local_98 == 1) {
                if (*(int *)(*(long *)
                              PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40
                            + 0xe0) == 0) {
                  thunk_FUN_00df405c();
                }
                uVar9 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar6);
              }
              param_5 = local_70;
              if (local_70 == 0) goto LAB_0198bc20;
              Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal
                        (local_70,uVar3,uVar1,uVar11,uVar9);
              uVar14 = 0xffffffff;
            }
            else {
              Mono_Globalization_Unicode_SimpleCollator__GetSortKey
                        (param_1,lVar8,0,*(undefined4 *)(lVar8 + 0x10),param_5,param_6);
            }
            if (*(long *)(lVar10 + 0x18) == 0) goto LAB_0198bc20;
            iVar12 = iVar12 + *(int *)(*(long *)(lVar10 + 0x18) + 0x18) + -1;
            param_2 = local_78;
            param_4 = local_7c;
          }
        }
      }
      else {
        iVar5 = Mono_Globalization_Unicode_SimpleCollator__FilterExtender
                          (param_1,uVar14,iVar4,param_6);
        param_5 = local_70;
        if (iVar5 < 0) {
          uVar3 = (undefined)local_b0[0];
          uVar11 = (uint)*local_90;
          uVar1 = *local_88;
          if (*local_90 == 1) {
            uVar11 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,iVar5,iVar4);
          }
          uVar9 = (uint)*local_98;
          if (*local_98 == 1) {
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            uVar9 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(iVar5);
          }
          param_5 = local_70;
          if (local_70 == 0) goto LAB_0198bc20;
          Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal(local_70,uVar3,uVar1,uVar11,uVar9);
          param_2 = local_78;
          param_4 = local_7c;
        }
        else {
          Mono_Globalization_Unicode_SimpleCollator__FillSortKeyRaw
                    (param_1,iVar5,iVar4,local_70,param_6);
        }
      }
      uVar13 = (ulong)(iVar12 + 1U);
    } while ((int)(iVar12 + 1U) < param_4);
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__GetResultAndReset
// Address: 0198bc28
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__GetResultAndReset(long param_1)

{
  Mono_Globalization_Unicode_SortKeyBuffer__GetResult();
  *(undefined *)(param_1 + 0x82) = 0;
  *(undefined8 *)(param_1 + 0x60) = 0;
  *(undefined8 *)(param_1 + 0x58) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x68) = 0;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__ClearBuffer
// Address: 0198bc4c
// ==========================================================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void Mono_Globalization_Unicode_SimpleCollator__ClearBuffer
               (undefined8 param_1,undefined *param_2,uint param_3)

{
  undefined auVar1 [16];
  ulong uVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  undefined auVar6 [16];
  
  if (0 < (int)param_3) {
    lVar3 = (ulong)param_3 - 1;
    uVar2 = (ulong)param_3 + 1 & 0x1fffffffe;
    lVar4 = _DAT_005bd230;
    lVar5 = _UNK_005bd238;
    do {
      auVar6._8_8_ = lVar5;
      auVar6._0_8_ = lVar4;
      auVar1._8_8_ = lVar3;
      auVar1._0_8_ = lVar3;
      auVar6 = NEON_cmhs(auVar1,auVar6,8);
      if ((auVar6 & (undefined  [16])0x1) != (undefined  [16])0x0) {
        *param_2 = 0;
      }
      if ((auVar6 & (undefined  [16])0x1) != (undefined  [16])0x0) {
        param_2[1] = 0;
      }
      lVar4 = lVar4 + 2;
      lVar5 = lVar5 + 2;
      uVar2 = uVar2 - 2;
      param_2 = param_2 + 2;
    } while (uVar2 != 0);
  }
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator_Context___ctor
// Address: 0198bcac
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator_Context___ctor
               (undefined4 *param_1,undefined4 param_2,undefined8 param_3,undefined8 param_4,
               undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  *param_1 = param_2;
  *(undefined8 *)(param_1 + 2) = param_4;
  *(undefined8 *)(param_1 + 4) = param_3;
  *(undefined8 *)(param_1 + 6) = param_5;
  *(undefined8 *)(param_1 + 8) = param_6;
  *(undefined8 *)(param_1 + 0xc) = param_7;
  param_1[10] = 0xffffffff;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__FillSortKeyRaw
// Address: 0198bcc8
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__FillSortKeyRaw
               (undefined8 param_1,uint param_2,int param_3,long param_4,uint param_5)

{
  undefined4 uVar1;
  undefined *puVar2;
  byte bVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  uint uVar7;
  int iVar8;
  int iVar9;
  undefined4 uVar10;
  undefined8 uVar11;
  long lVar12;
  uint uVar13;
  undefined4 uVar14;
  
  if ((DAT_0210161a & 1) == 0) {
    FUN_00db0bbc(PTR_char_TypeInfo_01fbf990);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210161a = 1;
  }
  uVar7 = param_2 - 0x3400;
  if (uVar7 >> 1 < 0xcdb) {
    if (param_4 != 0) {
      uVar13 = (uVar7 >> 1 & 0x7fff) / 0x7f;
      Mono_Globalization_Unicode_SortKeyBuffer__AppendCJKExtension
                (param_4,uVar13 + 0x10,uVar7 + uVar13 * -0xfe + 2);
      return;
    }
    goto LAB_0198c05c;
  }
  if (*(int *)(*(long *)PTR_char_TypeInfo_01fbf990 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar11 = System_Char__GetUnicodeCategory(param_2,0);
  if ((int)uVar11 == 0x10) {
    Mono_Globalization_Unicode_SimpleCollator__FillSurrogateSortKeyRaw(uVar11,param_2,param_4);
    return;
  }
  if ((int)uVar11 == 0x11) {
    if (param_4 == 0) goto LAB_0198c05c;
    iVar8 = (int)(param_2 - 0xe000) / 0xfe + -0x1b;
    iVar9 = (int)(param_2 - 0xe000) % 0xfe + 2;
    uVar4 = 0;
LAB_0198bdb4:
    uVar10 = 0;
  }
  else {
    uVar4 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,param_2,param_3);
    puVar2 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                0xe0) == 0) {
      thunk_FUN_00df405c(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    }
    if (0x3040 < (ushort)param_2) {
      if ((param_2 + 0x9a & 0xffff) < 0x38) goto LAB_0198bec0;
      uVar7 = param_2 >> 8 & 0xff;
      if (uVar7 < 0x33) {
        if ((ushort)param_2 < 0x309d) {
          if ((param_2 & 0xffff) < 0x3099) goto LAB_0198bec0;
        }
        else if (uVar7 < 0x31) {
          if ((param_2 & 0xffff) != 0x30fb) goto LAB_0198bec0;
        }
        else if ((param_2 - 0x32d0 & 0xffff) < 0x2f) {
LAB_0198bec0:
          uVar10 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,param_2);
          uVar5 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,param_2);
          lVar12 = *(long *)puVar2;
          if (*(int *)(lVar12 + 0xe0) == 0) {
            thunk_FUN_00df405c(lVar12);
          }
          uVar6 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(param_2);
          uVar7 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter(param_2);
          if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 +
                      0xe0) == 0) {
            thunk_FUN_00df405c(*(long *)
                                PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
          }
          bVar3 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(param_2 & 0xffff,param_5);
          if (param_4 == 0) goto LAB_0198c05c;
          uVar14 = 4;
          if (param_3 == 3) {
            uVar14 = 5;
          }
          uVar1 = 3;
          if (((uint)(param_3 == 0) | (param_5 & 2) >> 1) == 0) {
            uVar1 = uVar14;
          }
          Mono_Globalization_Unicode_SortKeyBuffer__AppendKana
                    (param_4,uVar5,uVar10,uVar4,uVar6,uVar7 & 1,uVar1,
                     0x53 < (param_2 - 0x3041 & 0xffff),bVar3 & 1);
          if ((param_3 != 2) || ((param_5 & 2) != 0)) {
            return;
          }
          iVar8 = 1;
          iVar9 = 1;
          uVar4 = 1;
          goto LAB_0198bdb4;
        }
      }
    }
    iVar8 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,param_2);
    iVar9 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,param_2);
    lVar12 = *(long *)puVar2;
    if (*(int *)(lVar12 + 0xe0) == 0) {
      thunk_FUN_00df405c(lVar12);
    }
    uVar10 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(param_2);
    if (param_4 == 0) {
LAB_0198c05c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
  }
  Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal(param_4,iVar8,iVar9,uVar4,uVar10);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal
// Address: 0198c060
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal
               (long param_1,undefined8 param_2,undefined4 param_3,uint param_4,uint param_5)

{
  uint uVar1;
  byte bVar2;
  undefined8 uVar3;
  long lVar4;
  char cVar5;
  long lVar6;
  long lVar7;
  uint uVar8;
  uint uVar9;
  
  uVar1 = (uint)param_2 & 0xff;
  uVar8 = 2;
  if ((param_4 & 0xff) != 0) {
    uVar8 = param_4;
  }
  uVar9 = 2;
  if ((param_5 & 0xff) != 0) {
    uVar9 = param_5;
  }
  if (uVar1 == 6) {
    if ((*(byte *)(param_1 + 0x7f) >> 5 & 1) == 0) {
      Mono_Globalization_Unicode_SortKeyBuffer__AppendLevel5(param_1,6,param_3);
      return;
    }
LAB_0198c140:
    uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (param_1,param_2,param_1 + 0x10,param_1 + 0x58);
    lVar4 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (uVar3,param_3,param_1 + 0x10,param_1 + 0x58);
    cVar5 = *(char *)(param_1 + 0x80);
LAB_0198c168:
    if (cVar5 == '\0') goto LAB_0198c17c;
  }
  else {
    cVar5 = *(char *)(param_1 + 0x80);
    lVar4 = param_1;
    if (((uVar1 != 1) || (cVar5 == '\0')) || (*(int *)(param_1 + 0x58) < 1)) {
      if (((uint)param_2 & 0xff) != 1) goto LAB_0198c140;
      goto LAB_0198c168;
    }
    lVar6 = *(long *)(param_1 + 0x18);
    uVar1 = *(int *)(param_1 + 0x5c) - 1;
    *(uint *)(param_1 + 0x5c) = uVar1;
    if (lVar6 == 0) {
LAB_0198c19c:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    if (*(uint *)(lVar6 + 0x18) <= uVar1) {
LAB_0198c1a0:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar7 = *(long *)(param_1 + 0x20);
    bVar2 = *(byte *)(lVar6 + (int)uVar1 + 0x20);
    uVar1 = *(int *)(param_1 + 0x60) - 1;
    *(uint *)(param_1 + 0x60) = uVar1;
    if (lVar7 == 0) goto LAB_0198c19c;
    if (*(uint *)(lVar7 + 0x18) <= uVar1) goto LAB_0198c1a0;
    uVar9 = (uint)*(byte *)(lVar7 + (int)uVar1 + 0x20);
    uVar8 = bVar2 + uVar8;
  }
  lVar4 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                    (lVar4,uVar8,param_1 + 0x18,param_1 + 0x5c);
LAB_0198c17c:
  Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
            (lVar4,uVar9,param_1 + 0x20,param_1 + 0x60);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__AppendCJKExtension
// Address: 0198c1a4
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__AppendCJKExtension
               (long param_1,undefined4 param_2,undefined4 param_3)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  
  lVar1 = param_1 + 0x10;
  lVar2 = param_1 + 0x58;
  uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(param_1,0xfe,lVar1,lVar2);
  uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(uVar3,0xff,lVar1,lVar2);
  uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(uVar3,param_2,lVar1,lVar2)
  ;
  uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(uVar3,param_3,lVar1,lVar2)
  ;
  if (*(char *)(param_1 + 0x80) != '\0') {
    uVar3 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (uVar3,2,param_1 + 0x18,param_1 + 0x5c);
  }
  Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
            (uVar3,2,param_1 + 0x20,param_1 + 0x60);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__FillSurrogateSortKeyRaw
// Address: 0198c238
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__FillSurrogateSortKeyRaw
               (undefined8 param_1,uint param_2,long param_3)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  
  if ((int)param_2 < 0xd840) {
    iVar2 = -0xd800;
    uVar3 = 0x3e;
    if (param_2 != 0xd800) {
      uVar3 = 0x3f;
    }
    iVar1 = 0x41;
  }
  else {
    if ((int)param_2 < 0xd880) {
      iVar2 = -0xd840;
      iVar1 = 0xf2;
    }
    else {
      if (param_2 >> 7 != 0x1b7) {
        iVar2 = -0xdb0a;
        iVar1 = 0x41;
        uVar3 = 0x3f;
        goto joined_r0x0198c2e8;
      }
      iVar2 = -0xdb40;
      iVar1 = 0xfe;
    }
    uVar3 = 0x3e;
  }
joined_r0x0198c2e8:
  if (param_3 != 0) {
    Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal
              (param_3,(int)(iVar2 + param_2) / 0xfe + iVar1,(int)(iVar2 + param_2) % 0xfe + 2,uVar3
               ,uVar3);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__AppendKana
// Address: 0198c2f0
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__AppendKana(long param_1)

{
  undefined8 uVar1;
  uint in_w5;
  undefined4 in_w6;
  uint in_w7;
  undefined4 uVar2;
  undefined4 uVar3;
  byte param_9;
  
  uVar1 = Mono_Globalization_Unicode_SortKeyBuffer__AppendNormal();
  if (param_1 != 0) {
    uVar2 = 0xffffffc4;
    uVar3 = uVar2;
    if ((in_w5 & 1) == 0) {
      uVar3 = 0xffffffe4;
    }
    uVar1 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (uVar1,uVar3,param_1 + 0x28,param_1 + 100);
    uVar1 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (uVar1,in_w6,param_1 + 0x30,param_1 + 0x68);
    if ((in_w7 & 1) == 0) {
      uVar2 = 0xffffffe4;
    }
    uVar1 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                      (uVar1,uVar2,param_1 + 0x38,param_1 + 0x6c);
    uVar3 = 0xffffffc4;
    if ((param_9 & 1) == 0) {
      uVar3 = 0xffffffe4;
    }
    Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
              (uVar1,uVar3,param_1 + 0x40,param_1 + 0x70);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__Compare
// Address: 0198c384
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__Compare
               (undefined8 param_1,long param_2,long param_3)

{
  if ((param_2 != 0) && (param_3 != 0)) {
    Mono_Globalization_Unicode_SimpleCollator__Compare
              (param_1,param_2,0,*(undefined4 *)(param_2 + 0x10),param_3,0,
               *(undefined4 *)(param_3 + 0x10),0);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__Compare
// Address: 0198c3c0
// ==========================================================================================

undefined4 Mono_Globalization_Unicode_SimpleCollator__Compare(void)

{
  undefined4 uVar1;
  int iVar2;
  uint in_w7;
  long lVar3;
  undefined4 uVar4;
  undefined4 local_70 [4];
  undefined4 local_60 [2];
  undefined local_58;
  undefined local_54;
  ulong local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  undefined4 *puStack_38;
  undefined4 *puStack_30;
  undefined8 local_28;
  undefined8 local_20;
  
  lVar3 = 0;
  local_54 = 0;
  local_58 = 0;
  local_60[0] = 0;
  local_70[0] = 0;
  do {
    *(undefined *)((long)local_60 + lVar3) = 0;
    lVar3 = lVar3 + 1;
  } while (lVar3 != 4);
  lVar3 = 0;
  do {
    *(undefined *)((long)local_70 + lVar3) = 0;
    lVar3 = lVar3 + 1;
  } while (lVar3 != 4);
  puStack_38 = local_60;
  puStack_30 = local_70;
  local_50 = (ulong)in_w7;
  uStack_48 = 0;
  local_40 = 0;
  local_20 = 0;
  local_28 = 0xffffffff;
  iVar2 = Mono_Globalization_Unicode_SimpleCollator__CompareInternal();
  uVar4 = 0xffffffff;
  if (-1 < iVar2) {
    uVar4 = 1;
  }
  uVar1 = 0;
  if (iVar2 != 0) {
    uVar1 = uVar4;
  }
  return uVar1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__System_Globalization_ISimpleCollator_Compare
// Address: 0198c470
// ==========================================================================================

undefined4
Mono_Globalization_Unicode_SimpleCollator__System_Globalization_ISimpleCollator_Compare(void)

{
  undefined4 uVar1;
  int iVar2;
  uint in_w7;
  long lVar3;
  undefined4 uVar4;
  undefined4 auStack_70 [4];
  undefined4 auStack_60 [2];
  undefined uStack_58;
  undefined uStack_54;
  ulong uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined4 *puStack_38;
  undefined4 *puStack_30;
  undefined8 uStack_28;
  undefined8 uStack_20;
  
  lVar3 = 0;
  uStack_54 = 0;
  uStack_58 = 0;
  auStack_60[0] = 0;
  auStack_70[0] = 0;
  do {
    *(undefined *)((long)auStack_60 + lVar3) = 0;
    lVar3 = lVar3 + 1;
  } while (lVar3 != 4);
  lVar3 = 0;
  do {
    *(undefined *)((long)auStack_70 + lVar3) = 0;
    lVar3 = lVar3 + 1;
  } while (lVar3 != 4);
  puStack_38 = auStack_60;
  puStack_30 = auStack_70;
  uStack_50 = (ulong)in_w7;
  uStack_48 = 0;
  uStack_40 = 0;
  uStack_20 = 0;
  uStack_28 = 0xffffffff;
  iVar2 = Mono_Globalization_Unicode_SimpleCollator__CompareInternal();
  uVar4 = 0xffffffff;
  if (-1 < iVar2) {
    uVar4 = 1;
  }
  uVar1 = 0;
  if (iVar2 != 0) {
    uVar1 = uVar4;
  }
  return uVar1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__CompareInternal
// Address: 0198c474
// ==========================================================================================

int Mono_Globalization_Unicode_SimpleCollator__CompareInternal
              (long param_1,long param_2,ulong param_3,int param_4,long param_5,uint param_6,
              int param_7,undefined *param_8,undefined *param_9,byte param_10,byte param_11,
              uint *param_12)

{
  long lVar1;
  uint uVar2;
  undefined2 uVar3;
  short sVar4;
  uint uVar5;
  uint *puVar6;
  long *plVar7;
  long lVar8;
  bool bVar9;
  bool bVar10;
  char cVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  int iVar15;
  uint uVar16;
  int iVar17;
  uint uVar18;
  uint uVar19;
  undefined4 uVar20;
  uint uVar21;
  ulong uVar22;
  long lVar23;
  long lVar24;
  int iVar25;
  byte *pbVar26;
  ulong uVar27;
  ulong uVar28;
  ulong uVar29;
  long lVar30;
  int iVar31;
  byte *pbVar32;
  byte *pbVar33;
  long lVar34;
  byte *pbVar35;
  ulong uVar36;
  ulong uVar37;
  byte *pbVar38;
  int local_11c;
  byte *local_118;
  int local_108;
  int iStack_104;
  uint local_100;
  uint local_fc;
  int local_f8;
  int local_f4;
  undefined8 local_f0;
  undefined8 local_e8;
  undefined8 local_e0;
  long local_d8;
  ulong local_d0;
  undefined8 local_c8;
  byte *local_c0;
  ulong local_b8;
  undefined8 local_b0;
  byte *local_a8;
  ulong local_a0;
  ulong local_98;
  byte *local_90;
  long local_88;
  uint local_7c;
  ulong local_78;
  long local_70;
  long local_68;
  
  pbVar32 = (byte *)(ulong)param_6;
  local_d8 = param_1;
  local_a0 = param_3;
  if ((DAT_0210161b & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210161b = 1;
  }
  lVar24 = local_d8;
  uVar2 = *param_12;
  iVar15 = (int)local_a0;
  uVar37 = (ulong)(uint)(param_4 + iVar15);
  param_6 = param_7 + param_6;
  *param_8 = 0;
  *param_9 = 0;
  uVar29 = local_a0;
  local_c0 = pbVar32;
  if ((param_10 & 1) != 0) {
    if (iVar15 < param_4 + iVar15) {
      if (param_2 == 0) goto LAB_0198dc1c;
      uVar27 = (ulong)iVar15;
      do {
        if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar27 & 0xffffffff)) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        iVar15 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType
                           (lVar24,*(undefined2 *)(param_2 + 0x14 + uVar27 * 2));
        uVar29 = uVar27;
        if (iVar15 == 0) break;
        param_4 = param_4 + -1;
        uVar27 = uVar27 + 1;
        uVar29 = uVar37;
      } while (param_4 != 0);
    }
    pbVar32 = local_c0;
    if ((int)local_c0 < (int)param_6) {
      if (param_5 == 0) {
LAB_0198dc1c:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      pbVar33 = (byte *)(long)(int)local_c0;
      do {
        if ((long)*(int *)(param_5 + 0x10) <= (long)((ulong)pbVar33 & 0xffffffff)) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        iVar15 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType
                           (lVar24,*(undefined2 *)(param_5 + 0x14 + (long)pbVar33 * 2));
        pbVar32 = pbVar33;
        if (iVar15 == 0) break;
        param_7 = param_7 + -1;
        pbVar33 = pbVar33 + 1;
        pbVar32 = (byte *)(ulong)param_6;
      } while (param_7 != 0);
    }
  }
  local_90 = (byte *)((ulong)pbVar32 & 0xffffffff);
  local_98 = uVar29 & 0xffffffff;
  uVar5 = uVar2 >> 1 & 1;
  local_f4 = -1;
  local_118 = (byte *)0x0;
  local_b8 = 0;
  local_b0 = 0;
  local_d0 = 0;
  local_c8 = 0;
  local_e8 = 0;
  local_108 = 0;
  iStack_104 = 0;
  local_11c = 0;
  uVar29 = uVar29 & 0xffffffff;
  local_fc = 0xffffffff;
  local_f8 = -1;
  local_68 = 0;
  lVar24 = 0;
  lVar30 = local_d8;
  pbVar33 = (byte *)(ulong)param_6;
  uVar21 = 5;
LAB_0198c618:
  pbVar38 = pbVar33;
  lVar34 = param_5;
  uVar27 = uVar29 & 0xffffffff;
  iVar15 = (int)uVar29;
  pbVar33 = pbVar38;
  if (iVar15 < (int)uVar37) {
    if (param_2 == 0) goto LAB_0198dc1c;
    if ((long)*(int *)(param_2 + 0x10) <= (long)uVar27) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    uVar3 = *(undefined2 *)(param_2 + (long)iVar15 * 2 + 0x14);
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0) ==
        0) {
      thunk_FUN_00df405c();
    }
    uVar22 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar2);
    if ((uVar22 & 1) != 0) {
      uVar29 = (ulong)(iVar15 + 1);
      param_5 = lVar34;
      goto LAB_0198c618;
    }
  }
  iVar17 = (int)pbVar38;
  local_78 = uVar37;
  local_70 = param_2;
  if ((int)pbVar32 < iVar17) {
    local_88 = lVar24;
    local_7c = uVar21;
    if (lVar34 == 0) goto LAB_0198dc1c;
    local_a8 = (byte *)(lVar34 + 0x14);
    pbVar35 = (byte *)(long)(int)pbVar32;
    pbVar26 = (byte *)(long)iVar17;
    bVar10 = true;
    do {
      if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar35 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      uVar3 = *(undefined2 *)(lVar34 + (long)pbVar35 * 2 + 0x14);
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0)
          == 0) {
        thunk_FUN_00df405c();
      }
      uVar37 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar2);
      iVar25 = (int)pbVar32;
      uVar21 = local_7c;
      lVar24 = local_88;
      if ((uVar37 & 1) == 0) {
        if ((int)local_78 <= iVar15) goto LAB_0198c880;
        param_5 = local_88;
        if (!bVar10) goto LAB_0198c744;
        iVar31 = (int)local_90;
        uVar22 = local_98;
        if ((iVar15 <= (int)local_98) || (iVar25 <= iVar31)) goto LAB_0198caa0;
        if (iVar17 <= iVar25) {
          uVar29 = uVar29 & 0xffffffff;
          goto LAB_0198c8ec;
        }
        local_f0 = pbVar38;
        if (local_70 == 0) goto LAB_0198dc1c;
        local_e0 = (ulong)(int)local_78;
        lVar24 = local_70 + (long)iVar15 * 2;
        lVar30 = 0;
        goto LAB_0198c7f0;
      }
      pbVar35 = pbVar35 + 1;
      pbVar32 = (byte *)(ulong)(iVar25 + 1);
      bVar10 = (long)pbVar35 < (long)pbVar26;
    } while (pbVar26 != pbVar35);
    pbVar32 = (byte *)((ulong)pbVar38 & 0xffffffff);
  }
  param_5 = lVar24;
  if (iVar15 < (int)local_78) {
LAB_0198c744:
    local_90 = (byte *)(local_d0 & 0xffffffff);
    pbVar33 = (byte *)(local_d0 >> 0x20);
    local_c0 = (byte *)(local_c8 & 0xffffffff);
    lVar24 = 0;
    uVar29 = uVar29 & 0xffffffff;
    lVar23 = local_68;
    pbVar35 = pbVar32;
    pbVar32 = (byte *)(local_c8 >> 0x20);
    plVar7 = (long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    param_2 = local_70;
    lVar1 = local_68;
    uVar37 = local_78;
    lVar8 = param_5;
  }
  else {
LAB_0198c880:
    local_98 = local_b8 & 0xffffffff;
    local_a0 = local_b0 & 0xffffffff;
    uVar29 = local_b0 >> 0x20;
    lVar23 = 0;
    pbVar35 = pbVar32;
    param_5 = lVar34;
    plVar7 = (long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
    param_2 = local_68;
    lVar1 = local_68;
    uVar37 = local_b8 >> 0x20;
    lVar8 = local_68;
  }
  local_68 = lVar23;
  PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 = (undefined *)plVar7;
  if (lVar8 == 0) {
    uVar29 = (ulong)pbVar35 & 0xffffffff;
    iVar25 = (int)pbVar35;
    local_7c = uVar21;
    local_68 = lVar1;
    if ((uVar21 < 3) || (iVar31 = (int)local_78, (local_11c == 0 | uVar5) != 0)) goto LAB_0198da80;
    if ((iVar17 <= iVar25) || (iVar31 <= iVar15)) goto LAB_0198dbdc;
    if (local_70 == 0) goto LAB_0198dc1c;
    local_a0 = (ulong)iVar31;
    local_90 = (byte *)(long)iVar25;
    local_98 = (ulong)iVar17;
    local_88 = lVar34 + (long)iVar25 * 2 + 0x14;
    local_68 = local_70 + (long)iVar15 * 2 + 0x14;
    lVar24 = 0;
    local_f0 = pbVar38;
    goto LAB_0198d8ec;
  }
  goto LAB_0198c618;
  while( true ) {
    pbVar32 = (byte *)(ulong)((int)pbVar32 + 1);
    lVar23 = lVar30 + 1;
    if (((long)pbVar26 <= iVar25 + lVar30 + 1) ||
       (lVar1 = iVar15 + lVar30, lVar30 = lVar23, (long)local_e0 <= lVar1 + 1)) break;
LAB_0198c7f0:
    iVar17 = (int)lVar30;
    if ((long)*(int *)(local_70 + 0x10) <= (long)(ulong)(uint)(iVar15 + iVar17)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    sVar4 = *(short *)(lVar24 + 0x14 + lVar30 * 2);
    if ((long)*(int *)(lVar34 + 0x10) <= (long)(iVar25 + lVar30 & 0xffffffffU)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    if (sVar4 != *(short *)(lVar34 + (long)iVar25 * 2 + 0x14 + lVar30 * 2)) goto LAB_0198c8e8;
  }
  iVar17 = (int)lVar23;
LAB_0198c8e8:
  uVar29 = (ulong)(uint)(iVar15 + iVar17);
  lVar30 = local_d8;
  pbVar38 = local_f0;
LAB_0198c8ec:
  uVar22 = local_98;
  iVar31 = (int)pbVar32;
  uVar37 = local_78 & 0xffffffff;
  lVar24 = local_88;
  param_5 = lVar34;
  param_2 = local_70;
  pbVar33 = pbVar38;
  uVar21 = local_7c;
  if (iVar31 == (int)pbVar38) goto LAB_0198c618;
  uVar37 = local_78 & 0xffffffff;
  pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
  if ((int)uVar29 == (int)local_78) goto LAB_0198c618;
  lVar24 = local_70 + 0x14;
  uVar37 = (long)((int)uVar29 + -1);
  do {
    uVar28 = uVar37;
    iVar15 = (int)uVar28;
    if (iVar15 <= (int)uVar22) break;
    if (local_70 == 0) goto LAB_0198dc1c;
    if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar28 & 0xffffffff)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    cVar11 = Mono_Globalization_Unicode_SimpleCollator__Category
                       (lVar30,*(undefined2 *)(lVar24 + (long)iVar15 * 2));
    uVar37 = uVar28 - 1;
  } while (cVar11 == '\x01');
  uVar37 = (long)(iVar31 + -1);
  do {
    uVar36 = uVar37;
    if ((int)uVar36 <= (int)local_90) break;
    if ((long)*(int *)(lVar34 + 0x10) <= (long)(uVar36 & 0xffffffff)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    cVar11 = Mono_Globalization_Unicode_SimpleCollator__Category
                       (lVar30,*(undefined2 *)(lVar34 + 0x14 + uVar36 * 2));
    uVar37 = uVar36 - 1;
  } while (cVar11 == '\x01');
  uVar27 = uVar28;
  if ((int)uVar22 < iVar15) {
    if (local_70 == 0) goto LAB_0198dc1c;
    lVar24 = local_70 + 0x14;
    iVar15 = (int)local_98;
    do {
      if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar28 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      uVar37 = Mono_Globalization_Unicode_SimpleCollator__IsSafe
                         (lVar30,*(undefined2 *)(lVar24 + uVar28 * 2));
      uVar27 = uVar28;
    } while (((uVar37 & 1) == 0) &&
            (uVar28 = uVar28 - 1, uVar27 = local_98, (long)iVar15 < (long)uVar28));
  }
  iVar15 = (int)local_90;
  uVar22 = uVar29;
  if (iVar15 < (int)uVar36) {
    do {
      if ((long)*(int *)(lVar34 + 0x10) <= (long)(uVar36 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      uVar29 = Mono_Globalization_Unicode_SimpleCollator__IsSafe
                         (lVar30,*(undefined2 *)(lVar34 + 0x14 + uVar36 * 2));
      if ((uVar29 & 1) != 0) goto LAB_0198ca90;
      uVar36 = uVar36 - 1;
      pbVar32 = local_90;
    } while ((long)iVar15 < (long)uVar36);
  }
  else {
LAB_0198ca90:
    pbVar32 = (byte *)(uVar36 & 0xffffffff);
  }
LAB_0198caa0:
  uVar37 = local_78;
  uVar21 = local_7c;
  local_f0 = (byte *)CONCAT44(local_f0._4_4_,iVar31);
  if (local_70 == 0) goto LAB_0198dc1c;
  if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar27 & 0xffffffff)) {
    Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
  }
  iVar15 = (int)uVar27;
  uVar20 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                     (lVar30,*(undefined2 *)(local_70 + (long)iVar15 * 2 + 0x14),uVar2);
  local_e0 = CONCAT44(local_e0._4_4_,uVar20);
  if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar32 & 0xffffffff)) {
    Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
  }
  iVar25 = (int)pbVar32;
  uVar16 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                     (lVar30,*(undefined2 *)(local_a8 + (long)iVar25 * 2),uVar2);
  iVar17 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType(lVar30,local_e0 & 0xffffffff);
  local_e8 = CONCAT44(iVar17,(int)local_e8);
  local_98 = uVar22;
  if (iVar17 == 0) {
LAB_0198cb48:
    local_a8 = (byte *)0x0;
  }
  else {
    if (-1 < (int)param_12[10]) {
      uVar20 = Mono_Globalization_Unicode_SimpleCollator__FilterExtender
                         (lVar30,param_12[10],iVar17,uVar2);
      local_e0 = CONCAT44(local_e0._4_4_,uVar20);
      goto LAB_0198cb48;
    }
    local_a8 = *(byte **)(param_12 + 0xc);
    if (local_a8 == (byte *)0x0) {
      local_90 = (byte *)((ulong)local_f0 & 0xffffffff);
      uVar29 = (ulong)(iVar15 + 1);
      goto LAB_0198ce40;
    }
  }
  iVar17 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType(lVar30,uVar16);
  local_e8 = CONCAT44(local_e8._4_4_,iVar17);
  if (iVar17 == 0) {
LAB_0198cb84:
    local_90 = (byte *)0x0;
  }
  else {
    if (-1 < (int)local_fc) {
      uVar16 = Mono_Globalization_Unicode_SimpleCollator__FilterExtender
                         (lVar30,local_fc,iVar17,uVar2);
      goto LAB_0198cb84;
    }
    local_90 = local_118;
    if (local_118 == (byte *)0x0) {
      local_90 = (byte *)((ulong)local_f0 & 0xffffffff);
      uVar37 = uVar37 & 0xffffffff;
      local_118 = (byte *)0x0;
      pbVar32 = (byte *)(ulong)(iVar25 + 1);
      uVar29 = uVar27 & 0xffffffff;
      lVar24 = local_88;
      param_5 = lVar34;
      param_2 = local_70;
      pbVar33 = pbVar38;
      goto LAB_0198c618;
    }
  }
  bVar14 = Mono_Globalization_Unicode_SimpleCollator__Category(lVar30,local_e0 & 0xffffffff);
  local_100 = uVar16;
  bVar12 = Mono_Globalization_Unicode_SimpleCollator__Category(lVar30);
  uVar29 = local_e0;
  if (bVar14 == 6) {
    if (((uVar2 >> 0x1d & 1) == 0) && (local_7c == 5)) {
      local_f8 = iVar15 - (int)local_a0;
      if (local_68 != 0) {
        local_f8 = local_b0._4_4_ - (int)local_b0;
      }
      uVar21 = Mono_Globalization_Unicode_SimpleCollator__Level1(lVar30,local_e0 & 0xffffffff);
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                  0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)
                            PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
      }
      iVar17 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar29 & 0xffffffff);
      local_108 = (uVar21 & 0xff) << (ulong)(iVar17 + 8U & 0x1f);
      uVar37 = local_78;
    }
    uVar29 = (ulong)(iVar15 + 1);
    param_12[10] = (uint)local_e0;
    uVar16 = (uint)local_f0;
    if (bVar12 == 6) goto LAB_0198cc80;
  }
  else {
    if (bVar12 != 6) {
      uVar29 = uVar27 & 0xffffffff;
      if (local_e8._4_4_ == 0) {
        lVar24 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                           (lVar30,local_70,uVar29,uVar37 & 0xffffffff);
        if (local_a8 != (byte *)0x0) goto LAB_0198cef0;
        if (lVar24 == 0) goto LAB_0198ce68;
        if (*(long *)(lVar24 + 0x18) == 0) goto LAB_0198dc1c;
        lVar23 = *(long *)(lVar24 + 0x28);
        iVar31 = *(int *)(*(long *)(lVar24 + 0x18) + 0x18);
        pbVar35 = local_90;
        uVar16 = (uint)local_f0;
        if (lVar23 == 0) {
          if (local_68 == 0) {
            param_2 = *(long *)(lVar24 + 0x20);
            if (param_2 == 0) goto LAB_0198dc1c;
            local_b0 = CONCAT44(iVar15 + iVar31,(int)local_a0);
            local_90 = (byte *)((ulong)local_f0 & 0xffffffff);
            uVar37 = (ulong)*(uint *)(param_2 + 0x10);
            local_b8 = CONCAT44((int)local_78,(int)local_98);
            local_98 = 0;
            local_e8 = local_e8 & 0xffffffff;
            uVar29 = 0;
            local_a0 = 0;
            local_68 = local_70;
            lVar24 = local_88;
            param_5 = lVar34;
            pbVar33 = pbVar38;
            uVar21 = local_7c;
            goto LAB_0198c618;
          }
          bVar10 = false;
          local_a8 = (byte *)0x0;
        }
        else {
          local_a8 = *(byte **)(param_12 + 6);
          uVar27 = 0;
          while ((long)uVar27 < (long)(int)*(uint *)(lVar23 + 0x18)) {
            if (*(uint *)(lVar23 + 0x18) <= uVar27) goto LAB_0198dc20;
            local_a8[uVar27] = *(byte *)(lVar23 + uVar27 + 0x20);
            lVar23 = *(long *)(lVar24 + 0x28);
            uVar27 = uVar27 + 1;
            if (lVar23 == 0) goto LAB_0198dc1c;
          }
          bVar10 = false;
          param_12[10] = 0xffffffff;
          *(byte **)(param_12 + 0xc) = local_a8;
        }
      }
      else {
        if (local_a8 == (byte *)0x0) {
LAB_0198ce68:
          pbVar33 = *(byte **)(param_12 + 6);
          *pbVar33 = bVar14;
          bVar13 = Mono_Globalization_Unicode_SimpleCollator__Level1(lVar30,local_e0 & 0xffffffff);
          pbVar33[1] = bVar13;
          local_a8 = pbVar33;
          if ((local_7c < 2 | uVar5) == 0) {
            bVar13 = Mono_Globalization_Unicode_SimpleCollator__Level2
                               (lVar30,local_e0 & 0xffffffff,local_e8._4_4_);
            local_a8[2] = bVar13;
          }
          if (local_7c < 3) {
            pbVar35 = local_90;
            uVar16 = (uint)local_f0;
LAB_0198d3fc:
            bVar10 = false;
            uVar21 = (uint)local_e0;
          }
          else {
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            bVar13 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(local_e0 & 0xffffffff);
            pbVar35 = local_90;
            local_a8[3] = bVar13;
            uVar16 = (uint)local_f0;
            if (local_7c < 4) {
              goto LAB_0198d3fc;
            }
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
              uVar16 = (uint)local_f0;
            }
            if (((uint)local_e0 & 0xffff) < 0x3041) goto LAB_0198d3fc;
            uVar21 = (uint)local_e0;
            if (((uint)local_e0 + 0x9a & 0xffff) < 0x38) {
              bVar10 = true;
            }
            else {
              uVar18 = (uint)local_e0 >> 8 & 0xff;
              if (0x32 < uVar18) goto LAB_0198d3fc;
              if (((uint)local_e0 & 0xffff) < 0x309d) {
                bVar10 = ((uint)local_e0 & 0xffff) < 0x3099;
              }
              else if (uVar18 < 0x31) {
                bVar10 = ((uint)local_e0 & 0xffff) != 0x30fb;
              }
              else {
                bVar10 = ((uint)local_e0 - 0x32d0 & 0xffff) < 0x2f;
              }
            }
          }
          if (1 < bVar14) {
            param_12[10] = uVar21;
          }
        }
        else {
LAB_0198cef0:
          bVar10 = false;
          pbVar35 = local_90;
          uVar16 = (uint)local_f0;
        }
        iVar31 = 1;
      }
      if (iVar17 == 0) {
        lVar24 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                           (lVar30,lVar34,(ulong)pbVar32 & 0xffffffff,(ulong)pbVar38 & 0xffffffff);
        uVar16 = (uint)local_f0;
        if (pbVar35 == (byte *)0x0) {
          if (lVar24 != 0) {
            if (*(long *)(lVar24 + 0x18) == 0) goto LAB_0198dc1c;
            lVar23 = *(long *)(lVar24 + 0x28);
            uVar21 = iVar25 + *(int *)(*(long *)(lVar24 + 0x18) + 0x18);
            pbVar32 = (byte *)(ulong)uVar21;
            if (lVar23 == 0) {
              if (local_88 == 0) {
                param_5 = *(long *)(lVar24 + 0x20);
                if (param_5 == 0) goto LAB_0198dc1c;
                local_d0 = CONCAT44((int)pbVar38,(uint)local_f0);
                uVar37 = uVar37 & 0xffffffff;
                local_90 = (byte *)0x0;
                local_e8 = local_e8 & 0xffffffff00000000;
                local_c8 = CONCAT44(uVar21,(int)local_c0);
                local_c0 = (byte *)0x0;
                pbVar32 = (byte *)0x0;
                lVar24 = lVar34;
                param_2 = local_70;
                pbVar33 = (byte *)(ulong)*(uint *)(param_5 + 0x10);
                uVar21 = local_7c;
                goto LAB_0198c618;
              }
              bVar9 = false;
              pbVar35 = (byte *)0x0;
            }
            else {
              pbVar35 = *(byte **)(param_12 + 8);
              uVar29 = 0;
              while ((long)uVar29 < (long)(int)*(uint *)(lVar23 + 0x18)) {
                if (*(uint *)(lVar23 + 0x18) <= uVar29) {
LAB_0198dc20:
                    /* WARNING: Subroutine does not return */
                  FUN_00db0dec();
                }
                pbVar35[uVar29] = *(byte *)(lVar23 + uVar29 + 0x20);
                lVar23 = *(long *)(lVar24 + 0x28);
                uVar29 = uVar29 + 1;
                if (lVar23 == 0) goto LAB_0198dc1c;
              }
              bVar9 = false;
              local_fc = 0xffffffff;
              local_118 = pbVar35;
            }
            goto LAB_0198cfd4;
          }
          goto LAB_0198cf04;
        }
LAB_0198cfcc:
        bVar9 = false;
      }
      else {
        if (pbVar35 != (byte *)0x0) goto LAB_0198cfcc;
LAB_0198cf04:
        pbVar35 = *(byte **)(param_12 + 8);
        *pbVar35 = bVar12;
        bVar14 = Mono_Globalization_Unicode_SimpleCollator__Level1(lVar30,local_100);
        pbVar35[1] = bVar14;
        if ((local_7c < 2 | uVar5) == 0) {
          bVar14 = Mono_Globalization_Unicode_SimpleCollator__Level2(lVar30,local_100,iVar17);
          pbVar35[2] = bVar14;
        }
        if (local_7c < 3) {
LAB_0198cf8c:
LAB_0198cf94:
          bVar9 = false;
          uVar16 = (uint)local_f0;
        }
        else {
          if (*(int *)(*(long *)
                        PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 + 0xe0
                      ) == 0) {
            thunk_FUN_00df405c();
          }
          bVar14 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(local_100);
          pbVar35[3] = bVar14;
          if (local_7c < 4) goto LAB_0198cf8c;
          if (*(int *)(*(long *)
                        PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 + 0xe0
                      ) == 0) {
            thunk_FUN_00df405c();
          }
          if ((local_100 & 0xffff) < 0x3041) goto LAB_0198cf94;
          uVar16 = (uint)local_f0;
          if ((local_100 + 0x9a & 0xffff) < 0x38) {
            bVar9 = true;
          }
          else {
            uVar21 = local_100 >> 8 & 0xff;
            if (0x32 < uVar21) goto LAB_0198cf94;
            if ((local_100 & 0xffff) < 0x309d) {
              bVar9 = (local_100 & 0xffff) < 0x3099;
            }
            else if (uVar21 < 0x31) {
              bVar9 = (local_100 & 0xffff) != 0x30fb;
            }
            else {
              bVar9 = (local_100 - 0x32d0 & 0xffff) < 0x2f;
            }
          }
        }
        puVar6 = &local_fc;
        if (1 < bVar12) {
          puVar6 = &local_100;
        }
        local_fc = *puVar6;
      }
      pbVar32 = (byte *)(ulong)(iVar25 + 1);
LAB_0198cfd4:
      pbVar33 = local_a8;
      uVar21 = iVar31 + iVar15;
      uVar29 = (ulong)uVar21;
      if ((uVar2 >> 1 & 1) == 0) {
        if ((int)uVar21 < (int)uVar37) {
          uVar29 = (ulong)(int)uVar21;
          lVar24 = local_70 + 0x14;
          local_90 = pbVar35;
          do {
            if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar29 & 0xffffffff)) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            cVar11 = Mono_Globalization_Unicode_SimpleCollator__Category
                               (lVar30,*(undefined2 *)(lVar24 + uVar29 * 2));
            if (cVar11 != '\x01') goto LAB_0198d1a8;
            bVar14 = pbVar33[2];
            if (bVar14 == 0) {
              bVar14 = 2;
              pbVar33[2] = 2;
            }
            if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar29 & 0xffffffff)) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            lVar30 = local_d8;
            cVar11 = Mono_Globalization_Unicode_SimpleCollator__Level2
                               (local_d8,*(undefined2 *)(lVar24 + uVar29 * 2),0);
            uVar29 = uVar29 + 1;
            pbVar33[2] = cVar11 + bVar14;
          } while ((long)(int)uVar37 != uVar29);
          uVar29 = local_78 & 0xffffffff;
LAB_0198d1a8:
          pbVar35 = local_90;
          uVar37 = local_78;
          uVar16 = (uint)local_f0;
        }
        if ((int)pbVar32 < (int)pbVar38) {
          pbVar32 = (byte *)(long)(int)pbVar32;
          do {
            if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar32 & 0xffffffff)) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            cVar11 = Mono_Globalization_Unicode_SimpleCollator__Category
                               (lVar30,*(undefined2 *)(lVar34 + 0x14 + (long)pbVar32 * 2));
            if (cVar11 != '\x01') goto LAB_0198d250;
            bVar14 = pbVar35[2];
            if (bVar14 == 0) {
              bVar14 = 2;
              pbVar35[2] = 2;
            }
            if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar32 & 0xffffffff)) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            cVar11 = Mono_Globalization_Unicode_SimpleCollator__Level2
                               (lVar30,*(undefined2 *)(lVar34 + 0x14 + (long)pbVar32 * 2),0);
            pbVar32 = pbVar32 + 1;
            pbVar35[2] = cVar11 + bVar14;
          } while (pbVar26 != pbVar32);
          pbVar32 = (byte *)((ulong)pbVar38 & 0xffffffff);
LAB_0198d250:
          uVar37 = local_78;
          uVar16 = (uint)local_f0;
        }
      }
      iVar15 = (uint)*local_a8 - (uint)*pbVar35;
      if (iVar15 == 0) {
        iVar15 = (uint)local_a8[1] - (uint)pbVar35[1];
      }
      if (iVar15 != 0) {
        return iVar15;
      }
      uVar37 = uVar37 & 0xffffffff;
      local_90 = (byte *)(ulong)uVar16;
      lVar24 = local_88;
      param_5 = lVar34;
      param_2 = local_70;
      pbVar33 = pbVar38;
      uVar21 = 1;
      if (local_7c != 1) {
        if (((uVar2 >> 1 & 1) == 0) && ((uint)local_a8[2] - (uint)pbVar35[2] != 0)) {
          if ((param_11 & 1) != 0) {
            return -1;
          }
          uVar37 = local_78 & 0xffffffff;
          uVar21 = 1;
          if (*(char *)(lVar30 + 0x5c) != '\0') {
            uVar21 = 2;
          }
          local_90 = (byte *)(ulong)uVar16;
          pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
          local_11c = (uint)local_a8[2] - (uint)pbVar35[2];
          goto LAB_0198c618;
        }
        local_90 = (byte *)(ulong)uVar16;
        uVar37 = local_78 & 0xffffffff;
        pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
        uVar21 = 2;
        if (local_7c != 2) {
          if ((uint)local_a8[3] - (uint)pbVar35[3] == 0) {
            local_90 = (byte *)(ulong)uVar16;
            uVar37 = local_78 & 0xffffffff;
            pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
            uVar21 = 3;
            if (local_7c == 3) goto LAB_0198c618;
            if (bVar10 != bVar9) {
              if ((param_11 & 1) != 0) {
                return -1;
              }
              local_11c = -1;
              if (bVar10 != false) {
                local_11c = 1;
              }
              local_90 = (byte *)(ulong)uVar16;
              uVar21 = 3;
              uVar37 = local_78 & 0xffffffff;
              pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
              goto LAB_0198c618;
            }
            local_90 = (byte *)(ulong)uVar16;
            uVar37 = local_78 & 0xffffffff;
            pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
            uVar21 = local_7c;
            if (bVar10 == false) goto LAB_0198c618;
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            uVar21 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter
                               (local_e0 & 0xffffffff);
            uVar16 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter
                               (local_100);
            lVar23 = local_68;
            param_2 = local_70;
            uVar27 = local_78;
            iVar15 = 1;
            if ((uVar21 & 1) != 0) {
              iVar15 = -1;
            }
            if (((uVar21 ^ uVar16) & 1) == 0) {
              iVar15 = 0;
            }
            uVar16 = (uint)local_f0;
            if (iVar15 == 0) {
              if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8
                          + 0xe0) == 0) {
                thunk_FUN_00df405c();
                uVar16 = (uint)local_f0;
              }
              iVar15 = 4;
              if (local_e8._4_4_ == 3) {
                iVar15 = 5;
              }
              iVar17 = 3;
              if ((uVar5 | local_e8._4_4_ == 0) == 0) {
                iVar17 = iVar15;
              }
              iVar25 = -5;
              if ((int)local_e8 != 3) {
                iVar25 = -4;
              }
              iVar15 = -3;
              if ((uVar5 | (int)local_e8 == 0) == 0) {
                iVar15 = iVar25;
              }
              iVar15 = iVar15 + iVar17;
            }
            if (iVar15 == 0) {
              if (*(int *)(*(long *)
                            PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                          0xe0) == 0) {
                thunk_FUN_00df405c();
                uVar16 = (uint)local_f0;
              }
              bVar10 = ((uint)local_e0 - 0x3041 & 0xffff) < 0x54;
              iVar15 = -1;
              if (bVar10) {
                iVar15 = 1;
              }
              if (bVar10 == (local_100 - 0x3041 & 0xffff) < 0x54) {
                if (*(int *)(*(long *)
                              PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0
                            ) == 0) {
                  thunk_FUN_00df405c();
                }
                uVar21 = local_100 & 0xffff;
                uVar18 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana
                                   ((uint)local_e0 & 0xffff,uVar2);
                uVar19 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(uVar21,uVar2);
                iVar15 = 1;
                if ((uVar18 & 1) != 0) {
                  iVar15 = -1;
                }
                local_90 = (byte *)((ulong)local_f0 & 0xffffffff);
                uVar37 = uVar27 & 0xffffffff;
                local_68 = lVar23;
                lVar24 = local_88;
                uVar27 = local_78;
                param_2 = local_70;
                pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
                uVar21 = local_7c;
                uVar16 = (uint)local_f0;
                if ((uVar18 & 1) == (uVar19 & 1)) goto LAB_0198c618;
              }
            }
            uVar21 = 3;
            local_11c = iVar15;
          }
          else {
            uVar21 = 2;
            lVar23 = local_68;
            uVar27 = local_78;
            local_11c = (uint)local_a8[3] - (uint)pbVar35[3];
          }
          local_90 = (byte *)(ulong)uVar16;
          uVar37 = uVar27 & 0xffffffff;
          local_68 = lVar23;
          lVar24 = local_88;
          pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
          if ((param_11 & 1) != 0) {
            return -1;
          }
        }
      }
      goto LAB_0198c618;
    }
    uVar29 = uVar27 & 0xffffffff;
LAB_0198cc80:
    iVar15 = local_f8;
    uVar21 = local_100;
    uVar16 = (uint)local_f0;
    if (((uVar2 >> 0x1d & 1) == 0) && (local_7c == 5)) {
      local_f4 = iVar25 - (int)local_c0;
      if (local_88 != 0) {
        local_f4 = local_c8._4_4_ - (int)local_c8;
      }
      uVar16 = Mono_Globalization_Unicode_SimpleCollator__Level1(lVar30,local_100);
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                  0xe0) == 0) {
        thunk_FUN_00df405c(*(long *)
                            PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
      }
      iVar17 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar21);
      iStack_104 = (uVar16 & 0xff) << (ulong)(iVar17 + 8U & 0x1f);
      uVar16 = (uint)local_f0;
    }
    pbVar32 = (byte *)(ulong)(iVar25 + 1);
    local_fc = local_100;
    local_f8 = iVar15;
  }
  iVar31 = local_f4;
  iVar25 = local_f8;
  iVar17 = iStack_104;
  iVar15 = local_108;
  uVar37 = uVar37 & 0xffffffff;
  local_90 = (byte *)(ulong)uVar16;
  lVar24 = local_88;
  param_5 = lVar34;
  param_2 = local_70;
  pbVar33 = pbVar38;
  uVar21 = local_7c;
  local_100 = local_fc;
  if (local_7c != 5) goto LAB_0198c618;
  local_90 = (byte *)(ulong)uVar16;
  local_f8 = -1;
  local_f4 = -1;
  bVar10 = local_108 == iStack_104;
  uVar37 = local_78 & 0xffffffff;
  local_108 = 0;
  iStack_104 = 0;
  pbVar33 = (byte *)((ulong)pbVar38 & 0xffffffff);
  if (bVar10) goto LAB_0198c618;
  local_90 = (byte *)(ulong)uVar16;
  uVar21 = 4;
  pbVar38 = (byte *)((ulong)pbVar38 & 0xffffffff);
  uVar37 = local_78;
  local_f8 = iVar25;
  local_f4 = iVar31;
  local_108 = iVar15;
  iStack_104 = iVar17;
LAB_0198ce40:
  uVar37 = uVar37 & 0xffffffff;
  lVar24 = local_88;
  param_5 = lVar34;
  param_2 = local_70;
  pbVar33 = pbVar38;
  goto LAB_0198c618;
LAB_0198d8ec:
  iVar17 = (int)lVar24;
  if ((long)*(int *)(local_70 + 0x10) <= (long)(ulong)(uint)(iVar15 + iVar17)) {
    Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
  }
  uVar3 = *(undefined2 *)(local_68 + lVar24 * 2);
  if (*(int *)(*plVar7 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar29 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(uVar3);
  if ((uVar29 & 1) != 0) {
    if (lVar34 == 0) goto LAB_0198dc1c;
    pbVar32 = local_90 + lVar24;
    if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar32 & 0xffffffff)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    uVar3 = *(undefined2 *)(local_88 + lVar24 * 2);
    if (*(int *)(*plVar7 + 0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    uVar29 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(uVar3);
    if ((uVar29 & 1) == 0) goto LAB_0198da70;
    if ((long)*(int *)(local_70 + 0x10) <= (long)(ulong)(uint)(iVar15 + iVar17)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    lVar30 = local_d8;
    uVar20 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                       (local_d8,*(undefined2 *)(local_68 + lVar24 * 2),uVar2);
    uVar21 = Mono_Globalization_Unicode_SimpleCollator__Level2(lVar30,uVar20,local_e8._4_4_);
    uVar29 = local_e8;
    if ((long)*(int *)(lVar34 + 0x10) <= (long)((ulong)pbVar32 & 0xffffffff)) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    lVar30 = local_d8;
    uVar20 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                       (local_d8,*(undefined2 *)(local_88 + lVar24 * 2),uVar2);
    bVar14 = Mono_Globalization_Unicode_SimpleCollator__Level2(lVar30,uVar20,uVar29 & 0xffffffff);
    iVar31 = (int)local_78;
    local_11c = (uVar21 & 0xff) - (uint)bVar14;
    if (local_11c != 0) goto LAB_0198da70;
    lVar30 = lVar24 + 1;
    if ((long)(local_90 + lVar24 + 1) < (long)local_98) goto code_r0x0198da20;
    goto LAB_0198da48;
  }
LAB_0198da70:
  uVar27 = (ulong)(uint)(iVar15 + iVar17);
  uVar29 = (ulong)(uint)(iVar25 + iVar17);
  pbVar38 = local_f0;
LAB_0198da80:
  uVar37 = local_78;
  iVar25 = (int)uVar29;
  iVar15 = (int)uVar27;
  iVar31 = (int)local_78;
  if ((local_7c == 1) && (local_11c != 0)) {
    if (iVar15 < iVar31) {
      if (local_70 == 0) goto LAB_0198dc1c;
      uVar27 = (ulong)iVar15;
      lVar24 = local_70 + 0x14;
      do {
        if ((long)*(int *)(local_70 + 0x10) <= (long)(uVar27 & 0xffffffff)) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        uVar3 = *(undefined2 *)(lVar24 + uVar27 * 2);
        if (*(int *)(*plVar7 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar22 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(uVar3);
        if ((uVar22 & 1) == 0) goto LAB_0198db00;
        uVar27 = uVar27 + 1;
      } while ((long)iVar31 != uVar27);
      uVar27 = uVar37 & 0xffffffff;
    }
LAB_0198db00:
    if (iVar25 < (int)pbVar38) {
      if (lVar34 == 0) goto LAB_0198dc1c;
      uVar29 = (ulong)iVar25;
      do {
        if ((long)*(int *)(lVar34 + 0x10) <= (long)(uVar29 & 0xffffffff)) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        uVar3 = *(undefined2 *)(lVar34 + 0x14 + uVar29 * 2);
        if (*(int *)(*plVar7 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar37 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsIgnorableNonSpacing(uVar3);
        if ((uVar37 & 1) == 0) goto LAB_0198db58;
        uVar29 = uVar29 + 1;
      } while ((int)pbVar38 != (int)uVar29);
      uVar29 = (ulong)pbVar38 & 0xffffffff;
    }
LAB_0198db58:
    iVar25 = (int)uVar29;
    iVar15 = (int)uVar27;
  }
  if (local_11c != 0) goto LAB_0198dbdc;
  goto LAB_0198db64;
code_r0x0198da20:
  lVar23 = iVar15 + lVar24;
  local_11c = 0;
  local_e8 = 0;
  lVar24 = lVar30;
  if ((long)local_a0 <= lVar23 + 1) {
LAB_0198da48:
    iVar17 = (int)lVar30;
    iVar25 = iVar25 + iVar17;
    iVar15 = iVar15 + iVar17;
    pbVar38 = local_f0;
LAB_0198db64:
    if ((local_f4 < 0) || (-1 < local_f8)) {
      if ((local_f4 < 0) && (-1 < local_f8)) {
        local_11c = 1;
      }
      else {
        local_11c = local_f8 - local_f4;
        if ((local_11c == 0) && (local_11c = local_108 - iStack_104, local_11c == 0)) {
          if (iVar25 == (int)pbVar38) {
            *param_8 = 1;
          }
          if (iVar15 == iVar31) {
            local_11c = 0;
            *param_9 = 1;
          }
          else {
            local_11c = 0;
          }
        }
      }
    }
    else {
      local_11c = -1;
    }
LAB_0198dbdc:
    if (iVar15 == iVar31) {
      if (iVar25 != (int)pbVar38) {
        local_11c = -1;
      }
    }
    else {
      local_11c = 1;
    }
    return local_11c;
  }
  goto LAB_0198d8ec;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator_PreviousInfo___ctor
// Address: 0198dc24
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator_PreviousInfo___ctor(undefined4 *param_1)

{
  *param_1 = 0xffffffff;
  *(undefined8 *)(param_1 + 2) = 0;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__CompareFlagPair
// Address: 0198dc34
// ==========================================================================================

undefined4
Mono_Globalization_Unicode_SimpleCollator__CompareFlagPair
          (undefined8 param_1,uint param_2,uint param_3)

{
  undefined4 uVar1;
  
  uVar1 = 0xffffffff;
  if ((param_2 & 1) != 0) {
    uVar1 = 1;
  }
  if (((param_2 ^ param_3) & 1) == 0) {
    uVar1 = 0;
  }
  return uVar1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsPrefix
// Address: 0198dc50
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__IsPrefix(undefined8 param_1,long param_2)

{
  if (param_2 != 0) {
    Mono_Globalization_Unicode_SimpleCollator__IsPrefix();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsPrefix
// Address: 0198dc70
// ==========================================================================================

uint Mono_Globalization_Unicode_SimpleCollator__IsPrefix
               (undefined8 param_1,undefined8 param_2,long param_3,undefined8 param_4,
               undefined8 param_5,uint param_6)

{
  uint uVar1;
  long lVar2;
  undefined4 local_70 [4];
  undefined4 local_60 [4];
  ulong local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  undefined4 *puStack_38;
  undefined4 *puStack_30;
  undefined8 local_28;
  undefined8 local_20;
  
  puStack_38 = (undefined4 *)0x0;
  local_40 = 0;
  local_28 = 0;
  puStack_30 = (undefined4 *)0x0;
  uStack_48 = 0;
  local_50 = 0;
  if (param_3 != 0) {
    if (*(int *)(param_3 + 0x10) == 0) {
      uVar1 = 1;
    }
    else {
      puStack_38 = local_60;
      local_60[0] = 0;
      puStack_30 = local_70;
      lVar2 = 0;
      local_70[0] = 0;
      do {
        *(undefined *)((long)puStack_38 + lVar2) = 0;
        lVar2 = lVar2 + 1;
      } while (lVar2 != 4);
      lVar2 = 0;
      do {
        *(undefined *)((long)puStack_30 + lVar2) = 0;
        lVar2 = lVar2 + 1;
      } while (lVar2 != 4);
      local_50 = (ulong)param_6;
      uStack_48 = 0;
      local_40 = 0;
      local_20 = 0;
      local_28 = 0xffffffff;
      uVar1 = Mono_Globalization_Unicode_SimpleCollator__IsPrefix();
    }
    return uVar1 & 1;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsPrefix
// Address: 0198dd1c
// ==========================================================================================

undefined Mono_Globalization_Unicode_SimpleCollator__IsPrefix
                    (undefined8 param_1,undefined8 param_2,long param_3,undefined4 param_4,
                    undefined4 param_5,byte param_6,undefined8 param_7)

{
  undefined local_8 [4];
  undefined local_4 [4];
  
  local_4[0] = 0;
  local_8[0] = 0;
  if (param_3 != 0) {
    Mono_Globalization_Unicode_SimpleCollator__CompareInternal
              (param_1,param_2,param_4,param_5,param_3,0,*(undefined4 *)(param_3 + 0x10),local_4,
               local_8,param_6 & 1,1,param_7);
    return local_4[0];
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsSuffix
// Address: 0198dd84
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__IsSuffix(undefined8 param_1,long param_2)

{
  if (param_2 != 0) {
    Mono_Globalization_Unicode_SimpleCollator__IsSuffix();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IsSuffix
// Address: 0198dda4
// ==========================================================================================

bool Mono_Globalization_Unicode_SimpleCollator__IsSuffix
               (undefined8 param_1,long param_2,long param_3,undefined8 param_4,undefined8 param_5,
               undefined4 param_6)

{
  bool bVar1;
  int iVar2;
  
  if (param_3 != 0) {
    if (*(int *)(param_3 + 0x10) == 0) {
      bVar1 = true;
    }
    else {
      iVar2 = Method_Mono_Globalization_Unicode_SimpleCollator_LastIndexOf(param_1,param_2,param_3);
      if (iVar2 < 0) {
        bVar1 = false;
      }
      else {
        if (param_2 == 0) goto LAB_0198de34;
        iVar2 = Mono_Globalization_Unicode_SimpleCollator__Compare
                          (param_1,param_2,iVar2,*(int *)(param_2 + 0x10) - iVar2,param_3,0,
                           *(undefined4 *)(param_3 + 0x10),param_6);
        bVar1 = iVar2 == 0;
      }
    }
    return bVar1;
  }
LAB_0198de34:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__QuickIndexOf
// Address: 0198dfc0
// ==========================================================================================

int Mono_Globalization_Unicode_SimpleCollator__QuickIndexOf
              (undefined8 param_1,long param_2,long param_3,int param_4,int param_5,
              undefined *param_6)

{
  uint uVar1;
  short sVar2;
  ulong uVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  long lVar7;
  
  *param_6 = 1;
  if (param_3 == 0) {
LAB_0198e14c:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (*(int *)(param_3 + 0x10) == 0) {
    iVar4 = 0;
  }
  else {
    if (*(int *)(param_3 + 0x10) <= param_5) {
      *param_6 = 0;
      uVar1 = *(uint *)(param_3 + 0x10);
      iVar4 = ((param_4 + param_5) - uVar1) + 1;
      if (param_4 < iVar4) {
        if ((int)uVar1 < 1) {
          return param_4;
        }
        iVar5 = -1;
        uVar6 = 0xffffffff;
LAB_0198e038:
        uVar3 = (ulong)uVar1;
        lVar7 = 0;
        do {
          if (iVar5 < lVar7) {
            if ((int)uVar3 <= lVar7) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            iVar5 = (int)lVar7;
            if (*(ushort *)(param_3 + 0x14 + lVar7 * 2) - 1 < 0x7f) goto LAB_0198e068;
LAB_0198e120:
            *param_6 = 1;
            break;
          }
LAB_0198e068:
          uVar1 = (int)lVar7 + param_4;
          if ((int)uVar6 < (int)uVar1) {
            if (param_2 == 0) goto LAB_0198e14c;
            if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar1) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            uVar6 = uVar1;
            if (0x7e < *(ushort *)(param_2 + 0x14 + (long)(int)uVar1 * 2) - 1) goto LAB_0198e120;
          }
          else if (param_2 == 0) goto LAB_0198e14c;
          if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar1) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          sVar2 = *(short *)(param_2 + 0x14 + (long)(int)uVar1 * 2);
          if (*(int *)(param_3 + 0x10) <= lVar7) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          if (sVar2 != *(short *)(param_3 + 0x14 + lVar7 * 2)) goto LAB_0198e0fc;
          uVar3 = (ulong)*(int *)(param_3 + 0x10);
          lVar7 = lVar7 + 1;
          if ((long)uVar3 <= lVar7) {
            return param_4;
          }
        } while( true );
      }
    }
LAB_0198e128:
    iVar4 = -1;
  }
  return iVar4;
LAB_0198e0fc:
  param_4 = param_4 + 1;
  if (param_4 == iVar4) goto LAB_0198e128;
  uVar1 = *(uint *)(param_3 + 0x10);
  if ((int)uVar1 < 1) {
    return param_4;
  }
  goto LAB_0198e038;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IndexOf
// Address: 0198e340
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__IndexOf
                (ulong param_1,undefined8 param_2,long param_3,ulong param_4,int param_5,
                undefined *param_6,uint *param_7)

{
  ushort uVar1;
  int iVar2;
  undefined2 uVar3;
  bool bVar4;
  undefined uVar5;
  char cVar6;
  char cVar7;
  uint uVar8;
  ulong uVar9;
  undefined8 uVar10;
  long lVar11;
  byte bVar12;
  long lVar13;
  uint uVar14;
  undefined *puVar15;
  int iVar16;
  ulong uVar17;
  long local_78;
  uint local_64;
  
  param_4 = param_4 & 0xffffffff;
  uVar9 = param_1;
  if ((DAT_0210161d & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    uVar9 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210161d = 1;
  }
  puVar15 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (param_3 == 0) {
LAB_0198e4c8:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  iVar16 = *(int *)(param_3 + 0x10);
  uVar14 = *param_7;
  if (iVar16 < 1) {
    uVar17 = 0;
  }
  else {
    uVar17 = 0;
    do {
      uVar3 = *(undefined2 *)(param_3 + 0x14 + uVar17 * 2);
      if (*(int *)(*(long *)puVar15 + 0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar9 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar14);
      if ((uVar9 & 1) == 0) {
        iVar16 = *(int *)(param_3 + 0x10);
        break;
      }
      iVar16 = *(int *)(param_3 + 0x10);
      uVar17 = uVar17 + 1;
    } while ((long)uVar17 < (long)iVar16);
  }
  iVar16 = iVar16 - (int)uVar17;
  if (iVar16 == 0) {
    uVar10 = Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
                       (uVar9,param_3,0,0,uVar17 & 0xffffffff);
    if (-1 < (int)uVar10) {
      uVar9 = Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
                        (uVar10,param_2,param_3,param_4,param_5);
      return uVar9;
    }
    return param_4;
  }
  lVar11 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                     (param_1,param_3,uVar17 & 0xffffffff,iVar16);
  puVar15 = param_6;
  if (lVar11 != 0) {
    local_78 = *(long *)(lVar11 + 0x20);
    bVar4 = local_78 == 0;
    if (!bVar4) {
      puVar15 = (undefined *)0x0;
    }
    if (puVar15 == (undefined *)0x0) {
      uVar8 = 0xffffffff;
      bVar12 = 1;
      goto LAB_0198e6fc;
    }
    lVar13 = *(long *)(lVar11 + 0x28);
    if (lVar13 != 0) {
      uVar9 = 0;
      do {
        if ((long)(int)*(uint *)(lVar13 + 0x18) <= (long)uVar9) {
          bVar12 = 1;
          uVar8 = 0xffffffff;
          goto LAB_0198e650;
        }
        if (*(uint *)(lVar13 + 0x18) <= uVar9) {
                    /* WARNING: Subroutine does not return */
          FUN_00db0dec();
        }
        puVar15[uVar9] = *(undefined *)(lVar13 + uVar9 + 0x20);
        lVar13 = *(long *)(lVar11 + 0x28);
        uVar9 = uVar9 + 1;
      } while (lVar13 != 0);
    }
    goto LAB_0198e4c8;
  }
  if (param_6 == (undefined *)0x0) {
    local_78 = 0;
    puVar15 = (undefined *)0x0;
    uVar8 = 0xffffffff;
    bVar12 = 1;
    bVar4 = true;
    goto LAB_0198e6fc;
  }
  lVar11 = (long)*(int *)(param_3 + 0x10);
  uVar9 = uVar17 & 0xffffffff;
  if (lVar11 <= (long)uVar9) {
    Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    lVar11 = (long)*(int *)(param_3 + 0x10);
  }
  if (lVar11 <= (long)uVar9) {
    Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
  }
  uVar8 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                    (param_1,*(undefined2 *)(param_3 + 0x14 + uVar9 * 2),uVar14);
  uVar5 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,uVar8);
  *param_6 = uVar5;
  uVar5 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,uVar8);
  param_6[1] = uVar5;
  if ((uVar14 >> 1 & 1) == 0) {
    uVar5 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar8,0);
    param_6[2] = uVar5;
  }
  if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 + 0xe0
              ) == 0) {
    thunk_FUN_00df405c();
  }
  uVar5 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar8);
  uVar1 = (ushort)uVar8;
  param_6[3] = uVar5;
  if (uVar1 < 0x3041) {
LAB_0198e5f8:
    bVar4 = false;
  }
  else if ((uVar8 + 0x9a & 0xffff) < 0x38) {
    bVar4 = true;
  }
  else {
    uVar14 = uVar8 >> 8 & 0xff;
    if (0x32 < uVar14) goto LAB_0198e5f8;
    if (uVar1 < 0x309d) {
      bVar4 = uVar1 < 0x3099;
    }
    else if (uVar14 < 0x31) {
      bVar4 = uVar1 != 0x30fb;
    }
    else {
      bVar4 = (uVar8 - 0x32d0 & 0xffff) < 0x2f;
    }
  }
  bVar12 = bVar4 ^ 1;
  bVar4 = true;
  local_78 = 0;
LAB_0198e650:
  iVar2 = *(int *)(param_3 + 0x10);
  iVar16 = (int)uVar17 + 1;
  if (iVar16 < iVar2) {
    uVar9 = (ulong)iVar16;
    do {
      if ((long)iVar2 <= (long)(uVar9 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      cVar6 = Mono_Globalization_Unicode_SimpleCollator__Category
                        (param_1,*(undefined2 *)(param_3 + 0x14 + uVar9 * 2));
      if (cVar6 != '\x01') break;
      cVar6 = puVar15[2];
      if (cVar6 == '\0') {
        cVar6 = '\x02';
        puVar15[2] = 2;
      }
      if ((long)*(int *)(param_3 + 0x10) <= (long)(uVar9 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      cVar7 = Mono_Globalization_Unicode_SimpleCollator__Level2
                        (param_1,*(undefined2 *)(param_3 + 0x14 + uVar9 * 2),0);
      puVar15[2] = cVar7 + cVar6;
      iVar2 = *(int *)(param_3 + 0x10);
      uVar9 = uVar9 + 1;
    } while ((int)uVar9 < iVar2);
  }
LAB_0198e6fc:
  do {
    uVar14 = (uint)param_4;
    if (bVar4) {
      iVar16 = uVar14 + param_5;
      if (iVar16 <= (int)uVar14) {
        return 0xffffffff;
      }
      local_64 = uVar14;
      uVar9 = Mono_Globalization_Unicode_SimpleCollator__MatchesForward
                        (param_1,param_2,&local_64,iVar16,uVar8,puVar15,bVar12,param_7);
      while ((uVar9 & 1) == 0) {
        param_4 = (ulong)local_64;
        if (iVar16 <= (int)local_64) {
          return 0xffffffff;
        }
        uVar9 = Mono_Globalization_Unicode_SimpleCollator__MatchesForward
                          (param_1,param_2,&local_64,iVar16,uVar8,puVar15,bVar12,param_7);
      }
    }
    else {
      param_4 = Mono_Globalization_Unicode_SimpleCollator__IndexOf
                          (param_1,param_2,local_78,param_4,param_5,param_6,param_7);
      param_4 = param_4 & 0xffffffff;
    }
    iVar16 = (int)param_4;
    if (iVar16 < 0) {
      return 0xffffffff;
    }
    param_5 = (uVar14 - iVar16) + param_5;
    uVar9 = Mono_Globalization_Unicode_SimpleCollator__IsPrefix
                      (param_1,param_2,param_3,param_4,param_5,0,param_7);
    if ((uVar9 & 1) != 0) {
      return param_4;
    }
    lVar11 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                       (param_1,param_2,param_4,param_5);
    if (lVar11 == 0) {
      uVar14 = iVar16 + 1;
      iVar2 = -1;
    }
    else {
      if (*(long *)(lVar11 + 0x18) == 0) goto LAB_0198e4c8;
      iVar2 = *(int *)(*(long *)(lVar11 + 0x18) + 0x18);
      uVar14 = iVar16 + iVar2;
      iVar2 = -iVar2;
    }
    param_5 = param_5 + iVar2;
    param_4 = (ulong)uVar14;
    if (param_5 < 1) {
      return 0xffffffff;
    }
  } while( true );
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
// Address: 0198e83c
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
                (undefined8 param_1,long param_2,long param_3,uint param_4,int param_5)

{
  int iVar1;
  uint uVar2;
  short sVar3;
  int iVar4;
  ulong uVar5;
  ulong uVar6;
  long lVar7;
  
  if (param_3 == 0) {
LAB_0198e934:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  uVar2 = *(uint *)(param_3 + 0x10);
  if (uVar2 == 0) {
    uVar6 = 0;
  }
  else {
    if ((int)uVar2 <= param_5) {
      iVar1 = ((param_4 + param_5) - uVar2) + 1;
      uVar6 = (ulong)param_4;
      if ((int)param_4 < iVar1) {
        if (0 < (int)uVar2) {
          uVar6 = (ulong)(int)param_4;
          do {
            uVar5 = (ulong)uVar2;
            if (param_2 == 0) goto LAB_0198e934;
            lVar7 = 0;
            while( true ) {
              iVar4 = (int)uVar5;
              if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar6 + lVar7 & 0xffffffff)) {
                Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
                iVar4 = *(int *)(param_3 + 0x10);
              }
              sVar3 = *(short *)(param_2 + 0x14 + (long)(int)(uVar6 + lVar7) * 2);
              if (iVar4 <= lVar7) {
                Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
              }
              if (sVar3 != *(short *)(param_3 + 0x14 + lVar7 * 2)) break;
              uVar5 = (ulong)*(int *)(param_3 + 0x10);
              lVar7 = lVar7 + 1;
              if ((long)uVar5 <= lVar7) goto LAB_0198e918;
            }
            uVar6 = uVar6 + 1;
            if ((int)uVar6 == iVar1) goto LAB_0198e90c;
            uVar2 = *(uint *)(param_3 + 0x10);
          } while (0 < (int)uVar2);
        }
        goto LAB_0198e918;
      }
    }
LAB_0198e90c:
    uVar6 = 0xffffffff;
  }
LAB_0198e918:
  return uVar6 & 0xffffffff;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IndexOfSortKey
// Address: 0198ed2c
// ==========================================================================================

int Mono_Globalization_Unicode_SimpleCollator__IndexOfSortKey
              (undefined8 param_1,undefined8 param_2,int param_3,int param_4,undefined8 param_5,
              undefined8 param_6,undefined4 param_7,uint param_8,undefined8 param_9)

{
  int iVar1;
  ulong uVar2;
  int local_44;
  
  param_4 = param_4 + param_3;
  if (param_3 < param_4) {
    local_44 = param_3;
    do {
      iVar1 = local_44;
      uVar2 = Mono_Globalization_Unicode_SimpleCollator__MatchesForward
                        (param_1,param_2,&local_44,param_4,param_7,param_5,param_8 & 1,param_9);
      if ((uVar2 & 1) != 0) {
        return iVar1;
      }
    } while (local_44 < param_4);
  }
  return -1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
// Address: 0198edc8
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
                (undefined8 param_1,long param_2,short param_3,int param_4,int param_5)

{
  ulong uVar1;
  
  if (param_4 < param_5 + param_4) {
    if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar1 = (ulong)param_4;
    do {
      if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar1 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      if (*(short *)(param_2 + 0x14 + uVar1 * 2) == param_3) goto LAB_0198ee28;
      param_5 = param_5 + -1;
      uVar1 = uVar1 + 1;
    } while (param_5 != 0);
  }
  uVar1 = 0xffffffff;
LAB_0198ee28:
  return uVar1 & 0xffffffff;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__MatchesForward
// Address: 0198ee40
// ==========================================================================================

undefined8
Mono_Globalization_Unicode_SimpleCollator__MatchesForward
          (undefined8 param_1,long param_2,uint *param_3,undefined4 param_4,undefined4 param_5,
          undefined8 param_6,uint param_7,long param_8)

{
  uint uVar1;
  ushort uVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  long lVar6;
  uint uVar7;
  long local_68;
  
  local_68 = 0;
  if (param_2 != 0) {
    uVar7 = *param_3;
    if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar7) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    uVar2 = *(ushort *)(param_2 + 0x14 + (long)(int)uVar7 * 2);
    uVar7 = (uint)uVar2;
    if (((uVar2 < 0x80) && (*(long *)(param_8 + 0x10) != 0)) &&
       ((*(byte *)((ulong)(uVar2 >> 3) + *(long *)(param_8 + 0x10)) >> (ulong)(uVar7 & 7) & 1) != 0)
       ) {
      uVar4 = 1;
    }
    else if (((uVar7 < 0x80) && (*(long *)(param_8 + 8) != 0)) &&
            ((*(byte *)(*(long *)(param_8 + 8) + (ulong)(uVar2 >> 3)) >> (ulong)(uVar2 & 7) & 1) !=
             0)) {
      uVar4 = 0;
      *param_3 = *param_3 + 1;
    }
    else {
      uVar1 = *param_3;
      if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar1) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      iVar3 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType
                        (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar1 * 2));
      local_68 = 0;
      uVar5 = Mono_Globalization_Unicode_SimpleCollator__MatchesForwardCore
                        (param_1,param_2,param_3,param_4,param_5,param_6,param_7 & 1,iVar3,&local_68
                         ,param_8);
      if ((uVar5 & 1) == 0) {
        lVar6 = *(long *)(param_8 + 8);
        uVar4 = 0;
        if (((lVar6 != 0) && (local_68 == 0)) && ((uVar4 = 0, iVar3 == 0 && (uVar2 < 0x80)))) {
          uVar4 = 0;
          *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) =
               *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) | (byte)(1 << ((ulong)uVar7 & 7));
        }
      }
      else {
        lVar6 = *(long *)(param_8 + 0x10);
        uVar4 = 1;
        if ((((lVar6 != 0) && (local_68 == 0)) && (uVar4 = 1, iVar3 == 0)) && (uVar7 < 0x80)) {
          uVar4 = 1;
          *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) =
               *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) | (byte)(1 << ((ulong)uVar2 & 7));
        }
      }
    }
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__LastIndexOf
// Address: 0198f018
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__LastIndexOf(undefined8 param_1,long param_2)

{
  if (param_2 != 0) {
    Method_Mono_Globalization_Unicode_SimpleCollator_LastIndexOf();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__LastIndexOf
// Address: 0198f038
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__LastIndexOf
                (ulong param_1,long param_2,long param_3,uint param_4,int param_5,undefined *param_6
                ,uint *param_7)

{
  uint uVar1;
  int iVar2;
  undefined2 uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  bool bVar7;
  undefined uVar8;
  char cVar9;
  char cVar10;
  ulong uVar11;
  undefined8 uVar12;
  long lVar13;
  ulong uVar14;
  long lVar15;
  byte bVar16;
  int iVar17;
  ulong uVar18;
  undefined *puVar19;
  long local_80;
  uint local_68;
  uint local_64;
  
  uVar11 = param_1;
  if ((DAT_0210161f & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    uVar11 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_0210161f = 1;
  }
  if (param_3 == 0) {
LAB_0198f1c4:
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  iVar17 = *(int *)(param_3 + 0x10);
  uVar1 = *param_7;
  uVar18 = 0;
  if (0 < iVar17) {
    do {
      uVar3 = *(undefined2 *)(param_3 + 0x14 + uVar18 * 2);
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0)
          == 0) {
        thunk_FUN_00df405c();
      }
      uVar11 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar1);
      if ((uVar11 & 1) == 0) {
        iVar17 = *(int *)(param_3 + 0x10);
        break;
      }
      iVar17 = *(int *)(param_3 + 0x10);
      uVar18 = uVar18 + 1;
    } while ((long)uVar18 < (long)iVar17);
  }
  iVar17 = iVar17 - (int)uVar18;
  if (iVar17 == 0) {
    uVar12 = Mono_Globalization_Unicode_SimpleCollator__IndexOfOrdinal
                       (uVar11,param_3,0,0,uVar18 & 0xffffffff);
    uVar11 = (ulong)param_4;
    if (-1 < (int)uVar12) {
      uVar11 = Mono_Globalization_Unicode_SimpleCollator__LastIndexOfOrdinal
                         (uVar12,param_2,param_3,param_4,param_5);
      return uVar11;
    }
    goto LAB_0198f510;
  }
  lVar13 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                     (param_1,param_3,uVar18 & 0xffffffff,iVar17);
  puVar19 = param_6;
  uVar6 = param_4;
  if (lVar13 == 0) {
    if (param_6 == (undefined *)0x0) {
      local_68 = 0xffffffff;
      local_80 = 0;
      puVar19 = (undefined *)0x0;
      bVar16 = 1;
      bVar7 = true;
    }
    else {
      if ((long)*(int *)(param_3 + 0x10) <= (long)(uVar18 & 0xffffffff)) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      local_68 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                           (param_1,*(undefined2 *)(param_3 + 0x14 + (uVar18 & 0xffffffff) * 2),
                            uVar1);
      uVar8 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,local_68);
      *param_6 = uVar8;
      uVar8 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,local_68);
      param_6[1] = uVar8;
      if ((uVar1 >> 1 & 1) == 0) {
        uVar8 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,local_68,0);
        param_6[2] = uVar8;
      }
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                  0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar8 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(local_68);
      param_6[3] = uVar8;
      if ((ushort)local_68 < 0x3041) {
LAB_0198f2e8:
        bVar7 = false;
      }
      else if ((local_68 + 0x9a & 0xffff) < 0x38) {
        bVar7 = true;
      }
      else {
        uVar4 = local_68 >> 8 & 0xff;
        if (0x32 < uVar4) goto LAB_0198f2e8;
        if ((ushort)local_68 < 0x309d) {
          bVar7 = (local_68 & 0xffff) < 0x3099;
        }
        else if (uVar4 < 0x31) {
          bVar7 = (local_68 & 0xffff) != 0x30fb;
        }
        else {
          bVar7 = (local_68 - 0x32d0 & 0xffff) < 0x2f;
        }
      }
      bVar16 = bVar7 ^ 1;
      local_80 = 0;
      bVar7 = true;
LAB_0198f348:
      iVar2 = *(int *)(param_3 + 0x10);
      iVar17 = (int)uVar18 + 1;
      if (iVar17 < iVar2) {
        uVar11 = (ulong)iVar17;
        do {
          if ((long)iVar2 <= (long)(uVar11 & 0xffffffff)) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          cVar9 = Mono_Globalization_Unicode_SimpleCollator__Category
                            (param_1,*(undefined2 *)(param_3 + 0x14 + uVar11 * 2));
          if (cVar9 != '\x01') break;
          cVar9 = puVar19[2];
          if (cVar9 == '\0') {
            cVar9 = '\x02';
            puVar19[2] = 2;
          }
          if ((long)*(int *)(param_3 + 0x10) <= (long)(uVar11 & 0xffffffff)) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          cVar10 = Mono_Globalization_Unicode_SimpleCollator__Level2
                             (param_1,*(undefined2 *)(param_3 + 0x14 + uVar11 * 2),0);
          puVar19[2] = cVar10 + cVar9;
          iVar2 = *(int *)(param_3 + 0x10);
          uVar11 = uVar11 + 1;
        } while ((int)uVar11 < iVar2);
      }
    }
  }
  else {
    local_80 = *(long *)(lVar13 + 0x20);
    bVar7 = local_80 == 0;
    if (!bVar7) {
      puVar19 = (undefined *)0x0;
    }
    if (puVar19 != (undefined *)0x0) {
      lVar15 = *(long *)(lVar13 + 0x28);
      if (lVar15 != 0) {
        uVar11 = 0;
        do {
          if ((long)(int)*(uint *)(lVar15 + 0x18) <= (long)uVar11) {
            local_68 = 0xffffffff;
            bVar16 = 1;
            goto LAB_0198f348;
          }
          if (*(uint *)(lVar15 + 0x18) <= uVar11) {
                    /* WARNING: Subroutine does not return */
            FUN_00db0dec();
          }
          puVar19[uVar11] = *(undefined *)(lVar15 + uVar11 + 0x20);
          lVar15 = *(long *)(lVar13 + 0x28);
          uVar11 = uVar11 + 1;
        } while (lVar15 != 0);
      }
      goto LAB_0198f1c4;
    }
    local_68 = 0xffffffff;
    bVar16 = 1;
  }
  do {
    uVar18 = (ulong)uVar6;
    if (bVar7) {
      iVar17 = uVar6 - param_5;
      if ((int)uVar6 <= iVar17) break;
      local_64 = uVar6;
      uVar11 = Mono_Globalization_Unicode_SimpleCollator__MatchesBackward
                         (param_1,param_2,&local_64,iVar17,param_4,local_68,puVar19,bVar16,param_7);
      while ((uVar11 & 1) == 0) {
        uVar18 = (ulong)local_64;
        if ((int)local_64 <= iVar17) goto LAB_0198f50c;
        uVar11 = Mono_Globalization_Unicode_SimpleCollator__MatchesBackward
                           (param_1,param_2,&local_64,iVar17,param_4,local_68,puVar19,bVar16,param_7
                           );
      }
    }
    else {
      uVar18 = Mono_Globalization_Unicode_SimpleCollator__LastIndexOf
                         (param_1,param_2,local_80,uVar18,param_5,param_6,param_7);
      uVar18 = uVar18 & 0xffffffff;
    }
    iVar17 = (int)uVar18;
    if (iVar17 < 0) break;
    iVar2 = (param_4 - iVar17) + 1;
    uVar11 = Mono_Globalization_Unicode_SimpleCollator__IsPrefix
                       (param_1,param_2,param_3,uVar18,iVar2,0,param_7);
    if ((uVar11 & 1) != 0) {
      uVar11 = uVar18;
      if ((int)param_4 <= iVar17) goto LAB_0198f510;
      if (param_2 != 0) {
        do {
          if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar18 & 0xffffffff)) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          uVar3 = *(undefined2 *)(param_2 + 0x14 + uVar18 * 2);
          if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 +
                      0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          uVar14 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar1);
          uVar11 = uVar18;
        } while (((uVar14 & 1) != 0) &&
                (uVar18 = uVar18 + 1, uVar11 = (ulong)param_4, param_4 != (uint)uVar18));
        goto LAB_0198f510;
      }
      goto LAB_0198f1c4;
    }
    lVar13 = Mono_Globalization_Unicode_SimpleCollator__GetContraction(param_1,param_2,uVar18,iVar2)
    ;
    if (lVar13 == 0) {
      iVar5 = -1;
      iVar2 = -1;
    }
    else {
      if (*(long *)(lVar13 + 0x18) == 0) goto LAB_0198f1c4;
      iVar2 = *(int *)(*(long *)(lVar13 + 0x18) + 0x18);
      iVar5 = -iVar2;
      iVar2 = -iVar2;
    }
    param_5 = (iVar17 - uVar6) + param_5 + iVar2;
    uVar6 = iVar17 + iVar5;
  } while (0 < param_5);
LAB_0198f50c:
  uVar11 = 0xffffffff;
LAB_0198f510:
  return uVar11 & 0xffffffff;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__LastIndexOfOrdinal
// Address: 0198f5a8
// ==========================================================================================

int Mono_Globalization_Unicode_SimpleCollator__LastIndexOfOrdinal
              (undefined8 param_1,long param_2,long param_3,int param_4,int param_5)

{
  short sVar1;
  short sVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  ulong uVar6;
  uint uVar7;
  int iVar8;
  ulong uVar9;
  
  if (param_3 != 0) {
    iVar3 = *(int *)(param_3 + 0x10);
    iVar5 = param_4;
    if (iVar3 != 0) {
      if (param_2 == 0) goto LAB_0198f724;
      iVar5 = -1;
      if ((iVar3 <= param_5) && (iVar3 <= *(int *)(param_2 + 0x10))) {
        uVar7 = iVar3 - 1;
        param_5 = (uVar7 + param_4) - param_5;
        if ((long)iVar3 <= (long)(ulong)uVar7) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        if (param_5 < param_4) {
          sVar1 = *(short *)(param_3 + (long)(int)uVar7 * 2 + 0x14);
          uVar6 = (ulong)param_4;
          uVar7 = param_4 - 1;
          do {
            if ((long)*(int *)(param_2 + 0x10) <= (long)(uVar6 & 0xffffffff)) {
              Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
            }
            if (*(short *)(param_2 + 0x14 + uVar6 * 2) == sVar1) {
              iVar5 = *(int *)(param_3 + 0x10);
              iVar3 = ((int)uVar6 - iVar5) + 1;
              if ((int)(iVar5 - 2U) < 0) {
                return iVar3;
              }
              iVar8 = iVar5 + -1;
              uVar9 = (ulong)(iVar5 - 2U);
              uVar4 = uVar7;
              while( true ) {
                if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar4) {
                  Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
                }
                sVar2 = *(short *)(param_2 + 0x14 + (long)(int)uVar4 * 2);
                if ((long)*(int *)(param_3 + 0x10) <= (long)uVar9) {
                  Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
                }
                if (sVar2 != *(short *)(param_3 + 0x14 + uVar9 * 2)) break;
                iVar8 = iVar8 + -1;
                uVar9 = uVar9 - 1;
                uVar4 = uVar4 - 1;
                if (iVar8 < 1) {
                  return iVar3;
                }
              }
            }
            uVar6 = uVar6 - 1;
            uVar7 = uVar7 - 1;
            iVar5 = -1;
          } while ((long)param_5 < (long)uVar6);
        }
        else {
          iVar5 = -1;
        }
      }
    }
    return iVar5;
  }
LAB_0198f724:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__LastIndexOf
// Address: 0198f728
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator__LastIndexOf(undefined8 param_1,long param_2)

{
  if (param_2 != 0) {
    Method_Mono_Globalization_Unicode_SimpleCollator_LastIndexOf();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__LastIndexOfSortKey
// Address: 0198fb9c
// ==========================================================================================

int Mono_Globalization_Unicode_SimpleCollator__LastIndexOfSortKey
              (undefined8 param_1,undefined8 param_2,int param_3,undefined4 param_4,int param_5,
              undefined8 param_6,undefined4 param_7,uint param_8,undefined8 param_9)

{
  int iVar1;
  ulong uVar2;
  int local_54;
  
  param_5 = param_3 - param_5;
  if (param_5 < param_3) {
    local_54 = param_3;
    do {
      iVar1 = local_54;
      uVar2 = Mono_Globalization_Unicode_SimpleCollator__MatchesBackward
                        (param_1,param_2,&local_54,param_5,param_4,param_7,param_6,param_8 & 1,
                         param_9);
      if ((uVar2 & 1) != 0) {
        return iVar1;
      }
    } while (param_5 < local_54);
  }
  return -1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__MatchesBackward
// Address: 0198fc40
// ==========================================================================================

undefined8
Mono_Globalization_Unicode_SimpleCollator__MatchesBackward
          (undefined8 param_1,long param_2,uint *param_3,undefined4 param_4,undefined4 param_5,
          undefined4 param_6,undefined8 param_7,uint param_8,long param_9)

{
  uint uVar1;
  ushort uVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  long lVar6;
  uint uVar7;
  long local_68;
  
  local_68 = 0;
  if (param_2 != 0) {
    uVar7 = *param_3;
    if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar7) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    uVar2 = *(ushort *)(param_2 + 0x14 + (long)(int)uVar7 * 2);
    uVar7 = (uint)uVar2;
    if (((uVar2 < 0x80) && (*(long *)(param_9 + 0x10) != 0)) &&
       ((*(byte *)((ulong)(uVar2 >> 3) + *(long *)(param_9 + 0x10)) >> (ulong)(uVar7 & 7) & 1) != 0)
       ) {
      uVar4 = 1;
    }
    else if (((uVar7 < 0x80) && (*(long *)(param_9 + 8) != 0)) &&
            ((*(byte *)(*(long *)(param_9 + 8) + (ulong)(uVar2 >> 3)) >> (ulong)(uVar2 & 7) & 1) !=
             0)) {
      uVar4 = 0;
      *param_3 = *param_3 - 1;
    }
    else {
      uVar1 = *param_3;
      if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar1) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      iVar3 = Mono_Globalization_Unicode_SimpleCollator__GetExtenderType
                        (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar1 * 2));
      local_68 = 0;
      uVar5 = Mono_Globalization_Unicode_SimpleCollator__MatchesBackwardCore
                        (param_1,param_2,param_3,param_4,param_5,param_6,param_7,param_8 & 1,iVar3,
                         &local_68,param_9);
      if ((uVar5 & 1) == 0) {
        lVar6 = *(long *)(param_9 + 8);
        uVar4 = 0;
        if (((lVar6 != 0) && (local_68 == 0)) && ((uVar4 = 0, iVar3 == 0 && (uVar2 < 0x80)))) {
          uVar4 = 0;
          *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) =
               *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) | (byte)(1 << ((ulong)uVar7 & 7));
        }
      }
      else {
        lVar6 = *(long *)(param_9 + 0x10);
        uVar4 = 1;
        if ((((lVar6 != 0) && (local_68 == 0)) && (uVar4 = 1, iVar3 == 0)) && (uVar7 < 0x80)) {
          uVar4 = 1;
          *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) =
               *(byte *)(lVar6 + (ulong)(uVar2 >> 3)) | (byte)(1 << ((ulong)uVar2 & 7));
        }
      }
    }
    return uVar4;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__MatchesForwardCore
// Address: 0198fe24
// ==========================================================================================

uint Mono_Globalization_Unicode_SimpleCollator__MatchesForwardCore
               (ulong param_1,long param_2,uint *param_3,int param_4,undefined4 param_5,
               char *param_6,uint param_7,int param_8,ulong *param_9,uint *param_10)

{
  char cVar1;
  char cVar2;
  char cVar3;
  uint uVar4;
  ulong uVar5;
  ulong uVar6;
  long lVar7;
  ulong uVar8;
  uint uVar9;
  char *pcVar10;
  undefined4 local_64;
  
  uVar5 = param_1;
  if ((DAT_02101620 & 1) == 0) {
    uVar5 = FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    DAT_02101620 = 1;
  }
  local_64 = 0;
  uVar4 = *param_10;
  pcVar10 = *(char **)(param_10 + 6);
  if (param_8 == 0) {
    uVar5 = Mono_Globalization_Unicode_SimpleCollator__GetContraction
                      (param_1,param_2,*param_3,param_4);
    *param_9 = uVar5;
    uVar6 = uVar5;
    if (uVar5 == 0) goto LAB_0198ff4c;
LAB_0198fef4:
    uVar8 = 0xffffffff;
LAB_0198fef8:
    if (*(long *)(uVar6 + 0x18) == 0) goto LAB_019901bc;
    *param_3 = *param_3 + *(int *)(*(long *)(uVar6 + 0x18) + 0x18);
    if ((param_7 & 1) != 0) {
      if (*(long *)(uVar6 + 0x28) == 0) {
        local_64 = 0;
        lVar7 = *(long *)(uVar6 + 0x20);
        if (lVar7 == 0) goto LAB_019901bc;
        uVar4 = Mono_Globalization_Unicode_SimpleCollator__MatchesForward
                          (param_1,lVar7,&local_64,*(undefined4 *)(lVar7 + 0x10),param_5,param_6,1,
                           param_10);
        goto LAB_01990154;
      }
      lVar7 = 0;
      do {
        pcVar10[lVar7] = param_6[lVar7];
        lVar7 = lVar7 + 1;
      } while (lVar7 != 4);
      param_10[10] = 0xffffffff;
      *(char **)(param_10 + 0xc) = pcVar10;
      goto LAB_01990034;
    }
  }
  else {
    if ((int)param_10[10] < 0) {
      pcVar10 = *(char **)(param_10 + 0xc);
      if (pcVar10 == (char *)0x0) {
        uVar4 = 0;
        *param_3 = *param_3 + 1;
        goto LAB_01990154;
      }
      uVar6 = *param_9;
      if (*param_9 != 0) goto LAB_0198fef4;
LAB_0198ff4c:
      if (param_2 == 0) goto LAB_019901bc;
      uVar9 = *param_3;
      if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar9) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      uVar8 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                        (param_1,*(undefined2 *)(param_2 + (long)(int)uVar9 * 2 + 0x14),uVar4);
      uVar8 = uVar8 & 0xffffffff;
    }
    else {
      uVar5 = Mono_Globalization_Unicode_SimpleCollator__FilterExtender
                        (param_1,param_10[10],param_8,uVar4);
      uVar6 = *param_9;
      uVar8 = uVar5 & 0xffffffff;
      if (uVar6 != 0) goto LAB_0198fef8;
      if ((int)uVar5 < 0) goto LAB_0198ff4c;
    }
    *param_3 = *param_3 + 1;
    cVar1 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,uVar8);
    *pcVar10 = cVar1;
    cVar3 = *param_6;
    if (cVar3 == cVar1) {
      cVar2 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,uVar8);
      pcVar10[1] = cVar2;
    }
    if ((uVar4 >> 1 & 1) == 0) {
      if (param_6[1] == pcVar10[1]) {
        cVar2 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar8,param_8);
        pcVar10[2] = cVar2;
joined_r0x0198fffc:
        if (cVar3 == cVar1) {
          if (*(int *)(*(long *)
                        PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 + 0xe0
                      ) == 0) {
            thunk_FUN_00df405c();
          }
          uVar5 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar8);
          pcVar10[3] = (char)uVar5;
          if (*pcVar10 != '\x01') {
            param_10[10] = (uint)uVar8;
          }
LAB_01990034:
          uVar9 = *param_3;
          if ((int)uVar9 < param_4) {
            if (param_2 == 0) goto LAB_019901bc;
            do {
              if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar9) {
                Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
              }
              uVar5 = Mono_Globalization_Unicode_SimpleCollator__Category
                                (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar9 * 2));
              if (((uint)uVar5 & 0xff) != 1) break;
              if ((uVar4 >> 1 & 1) == 0) {
                cVar3 = pcVar10[2];
                if (cVar3 == '\0') {
                  cVar3 = '\x02';
                  pcVar10[2] = '\x02';
                }
                uVar9 = *param_3;
                if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar9) {
                  Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
                }
                uVar5 = Mono_Globalization_Unicode_SimpleCollator__Level2
                                  (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar9 * 2),0)
                ;
                pcVar10[2] = (char)uVar5 + cVar3;
              }
              uVar9 = *param_3 + 1;
              *param_3 = uVar9;
            } while ((int)uVar9 < param_4);
          }
          uVar4 = Mono_Globalization_Unicode_SimpleCollator__MatchesPrimitive
                            (uVar5,uVar4,pcVar10,uVar8,param_8,param_6,param_5,param_7 & 1);
          goto LAB_01990154;
        }
      }
    }
    else if ((uVar4 >> 1 & 1) != 0) goto joined_r0x0198fffc;
    uVar4 = *param_3;
    if ((int)uVar4 < param_4) {
      if (param_2 == 0) {
LAB_019901bc:
                    /* WARNING: Subroutine does not return */
        FUN_00db0de4();
      }
      do {
        if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar4) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        cVar3 = Mono_Globalization_Unicode_SimpleCollator__Category
                          (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar4 * 2));
        if (cVar3 != '\x01') break;
        uVar4 = *param_3 + 1;
        *param_3 = uVar4;
      } while ((int)uVar4 < param_4);
    }
  }
  uVar4 = 0;
LAB_01990154:
  return uVar4 & 1;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__MatchesPrimitive
// Address: 019901c0
// ==========================================================================================

uint Mono_Globalization_Unicode_SimpleCollator__MatchesPrimitive
               (undefined8 param_1,uint param_2,char *param_3,uint param_4,int param_5,char *param_6
               ,uint param_7,uint param_8)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  uint uVar4;
  
  if ((DAT_02101621 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101621 = 1;
  }
  puVar1 = PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40;
  if ((((*param_3 == *param_6) && (param_3[1] == param_6[1])) &&
      (((param_2 >> 1 & 1) != 0 || (param_3[2] == param_6[2])))) && (param_3[3] == param_6[3])) {
    if ((param_8 & 1) != 0) {
      if (-1 < (int)param_4) {
        if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40
                    + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        if (0x3040 < (param_4 & 0xffff)) {
          if ((param_4 + 0x9a & 0xffff) < 0x38) {
            return 0;
          }
          uVar3 = param_4 >> 8 & 0xff;
          if (uVar3 < 0x33) {
            if (0x309c < (param_4 & 0xffff)) {
              if (uVar3 < 0x31) {
                if ((param_4 & 0xffff) != 0x30fb) {
                  return 0;
                }
                return 1;
              }
              if ((param_4 - 0x32d0 & 0xffff) < 0x2f) {
                return 0;
              }
              return 1;
            }
            if ((param_4 & 0xffff) < 0x3099) {
              return 0;
            }
          }
        }
      }
      return 1;
    }
    if (((param_2 >> 1 & 1) != 0) || (param_5 != 3)) {
      if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                  0xe0) == 0) {
        thunk_FUN_00df405c();
      }
      uVar3 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter(param_4);
      uVar4 = Mono_Globalization_Unicode_MSCompatUnicodeTable__IsJapaneseSmallLetter(param_7);
      puVar2 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
      if (((uVar3 ^ uVar4) & 1) == 0) {
        if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8 + 0xe0
                    ) == 0) {
          thunk_FUN_00df405c();
        }
        if (((param_2 >> 1 & 1) != 0) || (param_5 == 0)) {
          if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
            thunk_FUN_00df405c();
          }
          if (0x53 < (param_4 - 0x3041 & 0xffff) != (param_7 - 0x3041 & 0xffff) < 0x54) {
            if (*(int *)(*(long *)puVar2 + 0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            uVar3 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(param_4 & 0xffff,param_2);
            uVar4 = Mono_Globalization_Unicode_SimpleCollator__IsHalfKana(param_7 & 0xffff,param_2);
            return (uVar3 ^ uVar4 ^ 0xffffffff) & 1;
          }
        }
      }
    }
  }
  return 0;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator__MatchesBackwardCore
// Address: 019903e8
// ==========================================================================================

ulong Mono_Globalization_Unicode_SimpleCollator__MatchesBackwardCore
                (undefined8 param_1,long param_2,uint *param_3,undefined4 param_4,uint param_5,
                undefined4 param_6,char *param_7,uint param_8,int param_9,long *param_10,
                uint *param_11)

{
  bool bVar1;
  uint uVar2;
  undefined2 uVar3;
  int iVar4;
  undefined *puVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  undefined4 uVar9;
  uint uVar10;
  uint uVar11;
  ulong uVar12;
  long lVar13;
  ulong uVar14;
  long lVar15;
  char *pcVar16;
  
  if ((DAT_02101622 & 1) == 0) {
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101622 = 1;
  }
  puVar5 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  uVar2 = *param_11;
  pcVar16 = *(char **)(param_11 + 6);
  uVar11 = *param_3;
  if (param_9 != 0) {
    if ((int)uVar11 < 0) {
      return 0;
    }
    if (param_2 != 0) {
      cVar7 = '\0';
      uVar14 = (ulong)uVar11;
      do {
        if ((long)*(int *)(param_2 + 0x10) <= (long)uVar14) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        uVar3 = *(undefined2 *)(param_2 + 0x14 + uVar14 * 2);
        if (*(int *)(*(long *)puVar5 + 0xe0) == 0) {
          thunk_FUN_00df405c();
        }
        uVar12 = Mono_Globalization_Unicode_SimpleCollator__IsIgnorable(uVar3,uVar2);
        if ((uVar12 & 1) == 0) {
          if ((long)*(int *)(param_2 + 0x10) <= (long)uVar14) {
            Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
          }
          uVar9 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                            (param_1,*(undefined2 *)(param_2 + 0x14 + uVar14 * 2),uVar2);
          cVar6 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,uVar9);
          if (cVar6 != '\x01') {
            uVar10 = Mono_Globalization_Unicode_SimpleCollator__FilterExtender
                               (param_1,uVar9,param_9,uVar2);
            *pcVar16 = cVar6;
            cVar6 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,uVar10);
            pcVar16[1] = cVar6;
            if ((uVar2 >> 1 & 1) == 0) {
              cVar6 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar10,param_9);
              pcVar16[2] = cVar6;
            }
            if (*(int *)(*(long *)
                          PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                        0xe0) == 0) {
              thunk_FUN_00df405c();
            }
            cVar6 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar10);
            pcVar16[3] = cVar6;
            if ((param_9 != 3) && (cVar7 != '\0')) {
              cVar6 = cVar7 + '\x02';
              if (pcVar16[2] != '\0') {
                cVar6 = cVar7;
              }
              pcVar16[2] = cVar6;
            }
            *param_3 = *param_3 - 1;
            lVar13 = *param_10;
            if (lVar13 == 0) goto LAB_01990828;
            goto LAB_019906c4;
          }
          cVar7 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar9,0);
        }
        bVar1 = (long)uVar14 < 1;
        uVar14 = uVar14 - 1;
        if (bVar1) {
          return 0;
        }
      } while( true );
    }
    goto LAB_019908a0;
  }
  lVar13 = Mono_Globalization_Unicode_SimpleCollator__GetTailContraction
                     (param_1,param_2,(ulong)uVar11,param_4);
  *param_10 = lVar13;
  if (lVar13 == 0) {
    if (param_2 == 0) goto LAB_019908a0;
    uVar10 = *param_3;
    if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar10) {
      Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
    }
    uVar10 = Mono_Globalization_Unicode_SimpleCollator__FilterOptions
                       (param_1,*(undefined2 *)(param_2 + (long)(int)uVar10 * 2 + 0x14),uVar2);
    *param_3 = *param_3 - 1;
    cVar6 = Mono_Globalization_Unicode_SimpleCollator__Category(param_1,uVar10);
    *pcVar16 = cVar6;
    cVar7 = *param_7;
    if (cVar7 == cVar6) {
      cVar8 = Mono_Globalization_Unicode_SimpleCollator__Level1(param_1,uVar10);
      pcVar16[1] = cVar8;
    }
    if ((uVar2 >> 1 & 1) == 0) {
      if (pcVar16[1] != param_7[1]) {
        return 0;
      }
      cVar8 = Mono_Globalization_Unicode_SimpleCollator__Level2(param_1,uVar10,0);
      pcVar16[2] = cVar8;
      if (cVar7 != cVar6) {
        return 0;
      }
    }
    else {
      if ((uVar2 >> 1 & 1) == 0) {
        return 0;
      }
      if (cVar7 != cVar6) {
        return 0;
      }
    }
    if (*(int *)(*(long *)PTR_Mono_Globalization_Unicode_MSCompatUnicodeTable_TypeInfo_01fd2a40 +
                0xe0) == 0) {
      thunk_FUN_00df405c();
    }
    lVar13 = Mono_Globalization_Unicode_MSCompatUnicodeTable__Level3(uVar10);
    pcVar16[3] = (char)lVar13;
    if (*pcVar16 != '\x01') {
      param_11[10] = uVar10;
    }
  }
  else {
    uVar10 = 0xffffffff;
LAB_019906c4:
    if (*(long *)(lVar13 + 0x18) == 0) goto LAB_019908a0;
    *param_3 = *param_3 - *(int *)(*(long *)(lVar13 + 0x18) + 0x18);
    if ((param_8 & 1) == 0) {
      return 0;
    }
    if (*(long *)(lVar13 + 0x28) == 0) {
      lVar13 = *(long *)(lVar13 + 0x20);
      if (lVar13 != 0) {
        iVar4 = *(int *)(lVar13 + 0x10) + -1;
        uVar11 = Mono_Globalization_Unicode_SimpleCollator__LastIndexOfSortKey
                           (param_1,lVar13,iVar4,iVar4,*(int *)(lVar13 + 0x10),param_7,param_6,1,
                            param_11);
        return (ulong)(~uVar11 >> 0x1f);
      }
      goto LAB_019908a0;
    }
    lVar15 = 0;
    do {
      pcVar16[lVar15] = param_7[lVar15];
      lVar15 = lVar15 + 1;
    } while (lVar15 != 4);
    param_11[10] = 0xffffffff;
    *(char **)(param_11 + 0xc) = pcVar16;
    if (param_9 != 0) goto LAB_01990828;
  }
  uVar11 = uVar11 + 1;
  if ((int)uVar11 < (int)param_5) {
    if (param_2 == 0) {
LAB_019908a0:
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    do {
      if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar11) {
        Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
      }
      lVar13 = Mono_Globalization_Unicode_SimpleCollator__Category
                         (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar11 * 2));
      if (((uint)lVar13 & 0xff) != 1) break;
      if ((uVar2 >> 1 & 1) == 0) {
        cVar7 = pcVar16[2];
        if (cVar7 == '\0') {
          cVar7 = '\x02';
          pcVar16[2] = '\x02';
        }
        if ((long)*(int *)(param_2 + 0x10) <= (long)(ulong)uVar11) {
          Method_System_ThrowHelper_ThrowIndexOutOfRangeException(0);
        }
        lVar13 = Mono_Globalization_Unicode_SimpleCollator__Level2
                           (param_1,*(undefined2 *)(param_2 + 0x14 + (long)(int)uVar11 * 2),0);
        pcVar16[2] = (char)lVar13 + cVar7;
      }
      uVar11 = uVar11 + 1;
    } while (param_5 != uVar11);
  }
LAB_01990828:
  uVar14 = Mono_Globalization_Unicode_SimpleCollator__MatchesPrimitive
                     (lVar13,uVar2,pcVar16,uVar10,param_9,param_7,param_6,param_8 & 1);
  return uVar14;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SimpleCollator___cctor
// Address: 019908a4
// ==========================================================================================

void Mono_Globalization_Unicode_SimpleCollator___cctor(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  puVar1 = PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8;
  if ((DAT_02101623 & 1) == 0) {
    FUN_00db0bbc(PTR_System_Globalization_CultureInfo_TypeInfo_01fc59b8);
    FUN_00db0bbc(PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8);
    DAT_02101623 = 1;
  }
  puVar2 = PTR_Mono_Globalization_Unicode_SimpleCollator_TypeInfo_01fd2bf8;
  if (*(int *)(*(long *)puVar1 + 0xe0) == 0) {
    thunk_FUN_00df405c();
  }
  uVar3 = System_Globalization_CultureInfo__get_InvariantCulture(0);
  uVar4 = thunk_FUN_00e11c14(*(undefined8 *)puVar2);
  Mono_Globalization_Unicode_SimpleCollator___ctor(uVar4,uVar3);
  **(undefined8 **)(*(long *)puVar2 + 0xb8) = uVar4;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__Reset
// Address: 01990934
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__Reset(long param_1)

{
  *(undefined *)(param_1 + 0x82) = 0;
  *(undefined8 *)(param_1 + 0x60) = 0;
  *(undefined8 *)(param_1 + 0x58) = 0;
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x68) = 0;
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
// Address: 01990948
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
               (undefined8 param_1,undefined param_2,long *param_3,uint *param_4)

{
  uint uVar1;
  long lVar2;
  long lVar3;
  
  if ((DAT_02101625 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_02101625 = 1;
  }
  uVar1 = *param_4;
  lVar3 = *param_3;
  *param_4 = uVar1 + 1;
  if (lVar3 != 0) {
    if (*(uint *)(lVar3 + 0x18) <= uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    *(undefined *)(lVar3 + (int)uVar1 + 0x20) = param_2;
    if (*param_3 != 0) {
      if (*param_4 == *(uint *)(*param_3 + 0x18)) {
        lVar3 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,*param_4 << 1);
        lVar2 = *param_3;
        if (lVar2 == 0) goto LAB_01990a08;
        Method_System_Array_Copy(lVar2,lVar3,*(undefined4 *)(lVar2 + 0x18),0);
        *param_3 = lVar3;
      }
      return;
    }
  }
LAB_01990a08:
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__AppendLevel5
// Address: 01990a10
// ==========================================================================================

void Mono_Globalization_Unicode_SortKeyBuffer__AppendLevel5
               (long param_1,undefined4 param_2,undefined4 param_3)

{
  uint uVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  undefined8 uVar5;
  
  iVar4 = *(int *)(param_1 + 0x5c);
  lVar2 = param_1 + 0x48;
  lVar3 = param_1 + 0x74;
  uVar1 = iVar4 + 0x2000;
  if (-1 < iVar4 + 1) {
    uVar1 = iVar4 + 1;
  }
  iVar4 = (iVar4 + 1) - (uVar1 & 0xffffe000);
  uVar5 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                    (param_1,iVar4 + ((uint)(int)(short)iVar4 >> 0x19 & 0x3f) >> 6 & 0x3ff ^
                             0xffffff80,lVar2,lVar3);
  uVar5 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive
                    (uVar5,iVar4 * 4 | 3,lVar2,lVar3);
  uVar5 = Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(uVar5,param_2,lVar2,lVar3)
  ;
  Mono_Globalization_Unicode_SortKeyBuffer__AppendBufferPrimitive(uVar5,param_3,lVar2,lVar3);
  return;
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__GetResult
// Address: 01990aa8
// ==========================================================================================

undefined8 Mono_Globalization_Unicode_SortKeyBuffer__GetResult(long param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  uint uVar11;
  int iVar12;
  undefined *puVar13;
  undefined *puVar14;
  int iVar15;
  long lVar16;
  undefined8 uVar17;
  int iVar18;
  long lVar19;
  undefined8 uVar20;
  uint uVar21;
  
  lVar16 = param_1;
  if ((DAT_02101626 & 1) == 0) {
    FUN_00db0bbc(PTR_Method_System_Array_Reverse_byte_01fd2c48);
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    lVar16 = FUN_00db0bbc(PTR_System_Globalization_SortKey_TypeInfo_01fd2c50);
    DAT_02101626 = 1;
  }
  puVar14 = PTR_System_Globalization_SortKey_TypeInfo_01fd2c50;
  puVar13 = PTR_byte___TypeInfo_01fbf258;
  lVar19 = *(long *)(param_1 + 0x50);
  if (lVar19 != 0) {
    if (*(int *)(lVar19 + 0x10) == 0) {
      uVar1 = *(undefined4 *)(param_1 + 0x78);
      uVar17 = FUN_00db0c30(*(undefined8 *)PTR_byte___TypeInfo_01fbf258,0);
      uVar2 = *(undefined4 *)(param_1 + 0x7c);
      uVar20 = thunk_FUN_00e11c14(*(undefined8 *)puVar14);
      System_Globalization_SortKey___ctor(uVar20,uVar1,lVar19,uVar17,uVar2,0,0,0,0,0,0,0,0,0);
      return uVar20;
    }
    if (((*(char *)(param_1 + 0x81) != '\0') && (*(char *)(param_1 + 0x82) == '\0')) &&
       (lVar16 = *(long *)(param_1 + 0x18), lVar16 != 0)) {
      uVar11 = *(uint *)(lVar16 + 0x18);
      if ((int)uVar11 < 1) {
        lVar19 = 0;
      }
      else {
        lVar19 = 0;
        do {
          if (uVar11 <= (uint)lVar19) goto LAB_01990f78;
        } while ((*(char *)(lVar16 + 0x20 + lVar19) != '\0') &&
                (lVar19 = lVar19 + 1, (int)lVar19 < (int)uVar11));
      }
      lVar16 = Method_System_Array_Reverse_byte
                         (lVar16,0,lVar19,
                          *(undefined8 *)PTR_Method_System_Array_Reverse_byte_01fd2c48);
      *(undefined *)(param_1 + 0x82) = 1;
    }
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (lVar16,*(undefined8 *)(param_1 + 0x18),*(undefined4 *)(param_1 + 0x5c),2);
    *(int *)(param_1 + 0x5c) = (int)uVar17;
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x20),*(undefined4 *)(param_1 + 0x60),2);
    iVar12 = *(int *)(param_1 + 100);
    *(int *)(param_1 + 0x60) = (int)uVar17;
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x28),iVar12,0xe4);
    *(int *)(param_1 + 100) = (int)uVar17;
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x30),*(undefined4 *)(param_1 + 0x68),3);
    *(int *)(param_1 + 0x68) = (int)uVar17;
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x38),*(undefined4 *)(param_1 + 0x6c),0xe4)
    ;
    *(int *)(param_1 + 0x6c) = (int)uVar17;
    uVar17 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x40),*(undefined4 *)(param_1 + 0x70),0xe4)
    ;
    *(int *)(param_1 + 0x70) = (int)uVar17;
    iVar15 = Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
                       (uVar17,*(undefined8 *)(param_1 + 0x48),*(undefined4 *)(param_1 + 0x74),2);
    *(int *)(param_1 + 0x74) = iVar15;
    iVar18 = (int)*(undefined8 *)(param_1 + 100) +
             (int)((ulong)*(undefined8 *)(param_1 + 100) >> 0x20) +
             (int)*(undefined8 *)(param_1 + 0x6c) +
             (int)((ulong)*(undefined8 *)(param_1 + 0x6c) >> 0x20) + 4;
    if (iVar12 < 1) {
      iVar18 = 0;
    }
    lVar16 = FUN_00db0c30(*(undefined8 *)puVar13,
                          iVar15 + *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x5c) +
                          *(int *)(param_1 + 0x60) + iVar18 + 5);
    Method_System_Array_Copy
              (*(undefined8 *)(param_1 + 0x10),lVar16,*(undefined4 *)(param_1 + 0x58),0);
    if (lVar16 != 0) {
      if (*(uint *)(param_1 + 0x58) < *(uint *)(lVar16 + 0x18)) {
        *(undefined *)(lVar16 + (int)*(uint *)(param_1 + 0x58) + 0x20) = 1;
        iVar15 = *(int *)(param_1 + 0x5c);
        iVar18 = *(int *)(param_1 + 0x58) + 1;
        if (0 < iVar15) {
          Method_System_Array_Copy(*(undefined8 *)(param_1 + 0x18),0,lVar16,iVar18,iVar15,0);
          iVar15 = *(int *)(param_1 + 0x5c);
        }
        uVar11 = iVar15 + iVar18;
        if (uVar11 < *(uint *)(lVar16 + 0x18)) {
          *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 1;
          iVar18 = *(int *)(param_1 + 0x60);
          if (0 < iVar18) {
            Method_System_Array_Copy(*(undefined8 *)(param_1 + 0x20),0,lVar16,uVar11 + 1,iVar18,0);
            iVar18 = *(int *)(param_1 + 0x60);
          }
          uVar11 = iVar18 + uVar11 + 1;
          if (uVar11 < *(uint *)(lVar16 + 0x18)) {
            uVar21 = uVar11 + 1;
            *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 1;
            if (0 < iVar12) {
              Method_System_Array_Copy
                        (*(undefined8 *)(param_1 + 0x28),0,lVar16,uVar21,
                         *(undefined4 *)(param_1 + 100),0);
              uVar21 = *(int *)(param_1 + 100) + uVar21;
              if (*(uint *)(lVar16 + 0x18) <= uVar21) goto LAB_01990f78;
              *(undefined *)(lVar16 + (int)uVar21 + 0x20) = 0xff;
              Method_System_Array_Copy
                        (*(undefined8 *)(param_1 + 0x30),0,lVar16,uVar21 + 1,
                         *(undefined4 *)(param_1 + 0x68),0);
              uVar11 = *(int *)(param_1 + 0x68) + uVar21 + 1;
              if (*(uint *)(lVar16 + 0x18) <= uVar11) goto LAB_01990f78;
              *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 2;
              Method_System_Array_Copy
                        (*(undefined8 *)(param_1 + 0x38),0,lVar16,uVar11 + 1,
                         *(undefined4 *)(param_1 + 0x6c),0);
              uVar11 = *(int *)(param_1 + 0x6c) + uVar11 + 1;
              if (*(uint *)(lVar16 + 0x18) <= uVar11) goto LAB_01990f78;
              *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 0xff;
              Method_System_Array_Copy
                        (*(undefined8 *)(param_1 + 0x40),0,lVar16,uVar11 + 1,
                         *(undefined4 *)(param_1 + 0x70),0);
              uVar11 = *(int *)(param_1 + 0x70) + uVar11 + 1;
              if (*(uint *)(lVar16 + 0x18) <= uVar11) goto LAB_01990f78;
              uVar21 = uVar11 + 1;
              *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 0xff;
            }
            if (uVar21 < *(uint *)(lVar16 + 0x18)) {
              *(undefined *)(lVar16 + (int)uVar21 + 0x20) = 1;
              iVar18 = *(int *)(param_1 + 0x74);
              if (0 < iVar18) {
                Method_System_Array_Copy
                          (*(undefined8 *)(param_1 + 0x48),0,lVar16,uVar21 + 1,iVar18,0);
                iVar18 = *(int *)(param_1 + 0x74);
              }
              uVar11 = iVar18 + uVar21 + 1;
              if (uVar11 < *(uint *)(lVar16 + 0x18)) {
                *(undefined *)(lVar16 + (int)uVar11 + 0x20) = 0;
                uVar1 = *(undefined4 *)(param_1 + 0x78);
                uVar6 = *(undefined4 *)(param_1 + 0x7c);
                uVar2 = *(undefined4 *)(param_1 + 0x58);
                uVar7 = *(undefined4 *)(param_1 + 0x5c);
                uVar20 = *(undefined8 *)(param_1 + 0x50);
                uVar3 = *(undefined4 *)(param_1 + 0x60);
                uVar8 = *(undefined4 *)(param_1 + 100);
                uVar4 = *(undefined4 *)(param_1 + 0x68);
                uVar9 = *(undefined4 *)(param_1 + 0x6c);
                uVar5 = *(undefined4 *)(param_1 + 0x70);
                uVar10 = *(undefined4 *)(param_1 + 0x74);
                uVar17 = thunk_FUN_00e11c14(*(undefined8 *)puVar14);
                System_Globalization_SortKey___ctor
                          (uVar17,uVar1,uVar20,lVar16,uVar6,uVar2,uVar7,uVar3,uVar8,uVar4,uVar9,
                           uVar5,uVar10,0);
                return uVar17;
              }
            }
          }
        }
      }
LAB_01990f78:
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
// Address: 01990f80
// ==========================================================================================

int Mono_Globalization_Unicode_SortKeyBuffer__GetOptimizedLength
              (undefined8 param_1,long param_2,uint param_3,char param_4)

{
  int iVar1;
  ulong uVar2;
  
  if ((int)param_3 < 1) {
    iVar1 = 0;
  }
  else {
    if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0de4();
    }
    uVar2 = 0;
    iVar1 = -1;
    do {
      if (*(uint *)(param_2 + 0x18) <= uVar2) {
                    /* WARNING: Subroutine does not return */
        FUN_00db0dec();
      }
      if (*(char *)(param_2 + 0x20 + uVar2) != param_4) {
        iVar1 = (int)uVar2;
      }
      uVar2 = uVar2 + 1;
    } while (param_3 != uVar2);
    iVar1 = iVar1 + 1;
  }
  return iVar1;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetUIntBytes
// Address: 01990fe0
// ==========================================================================================

void Mono_Security_BitConverterLE__GetUIntBytes(undefined *param_1)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  
  puVar2 = PTR_byte___TypeInfo_01fbf258;
  if ((DAT_02101627 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_02101627 = 1;
  }
  lVar3 = FUN_00db0c30(*(undefined8 *)puVar2,4);
  if (lVar3 != 0) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if ((((uVar1 != 0) && (*(undefined *)(lVar3 + 0x20) = *param_1, uVar1 != 1)) &&
        (*(undefined *)(lVar3 + 0x21) = param_1[1], 2 < uVar1)) &&
       (*(undefined *)(lVar3 + 0x22) = param_1[2], uVar1 != 3)) {
      *(undefined *)(lVar3 + 0x23) = param_1[3];
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetULongBytes
// Address: 01991078
// ==========================================================================================

void Mono_Security_BitConverterLE__GetULongBytes(undefined *param_1)

{
  uint uVar1;
  undefined *puVar2;
  long lVar3;
  
  puVar2 = PTR_byte___TypeInfo_01fbf258;
  if ((DAT_02101628 & 1) == 0) {
    FUN_00db0bbc(PTR_byte___TypeInfo_01fbf258);
    DAT_02101628 = 1;
  }
  lVar3 = FUN_00db0c30(*(undefined8 *)puVar2,8);
  if (lVar3 != 0) {
    uVar1 = *(uint *)(lVar3 + 0x18);
    if (((((uVar1 != 0) && (*(undefined *)(lVar3 + 0x20) = *param_1, uVar1 != 1)) &&
         (*(undefined *)(lVar3 + 0x21) = param_1[1], 2 < uVar1)) &&
        ((*(undefined *)(lVar3 + 0x22) = param_1[2], uVar1 != 3 &&
         (*(undefined *)(lVar3 + 0x23) = param_1[3], 4 < uVar1)))) &&
       ((*(undefined *)(lVar3 + 0x24) = param_1[4], uVar1 != 5 &&
        ((*(undefined *)(lVar3 + 0x25) = param_1[5], 6 < uVar1 &&
         (*(undefined *)(lVar3 + 0x26) = param_1[6], uVar1 != 7)))))) {
      *(undefined *)(lVar3 + 0x27) = param_1[7];
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_00db0dec();
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0de4();
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetBytes
// Address: 01991150
// ==========================================================================================

void Mono_Security_BitConverterLE__GetBytes(undefined4 param_1)

{
  undefined4 local_4;
  
  local_4 = param_1;
  Mono_Security_BitConverterLE__GetUIntBytes(&local_4);
  return;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__GetBytes
// Address: 01991168
// ==========================================================================================

void Mono_Security_BitConverterLE__GetBytes(undefined8 param_1)

{
  undefined8 local_8;
  
  local_8 = param_1;
  Mono_Security_BitConverterLE__GetULongBytes(&local_8);
  return;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__UIntFromBytes
// Address: 01991180
// ==========================================================================================

void Mono_Security_BitConverterLE__UIntFromBytes(undefined *param_1,long param_2,uint param_3)

{
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  if (param_3 < *(uint *)(param_2 + 0x18)) {
    *param_1 = *(undefined *)(param_2 + (int)param_3 + 0x20);
    if (param_3 + 1 < *(uint *)(param_2 + 0x18)) {
      param_1[1] = *(undefined *)(param_2 + (int)(param_3 + 1) + 0x20);
      if (param_3 + 2 < *(uint *)(param_2 + 0x18)) {
        param_1[2] = *(undefined *)(param_2 + (int)(param_3 + 2) + 0x20);
        if (param_3 + 3 < *(uint *)(param_2 + 0x18)) {
          param_1[3] = *(undefined *)(param_2 + (int)(param_3 + 3) + 0x20);
          return;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00db0dec();
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__ULongFromBytes
// Address: 01991204
// ==========================================================================================

void Mono_Security_BitConverterLE__ULongFromBytes(long param_1,long param_2,uint param_3)

{
  long lVar1;
  long lVar2;
  long lVar3;
  
  if (param_2 == 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00db0de4();
  }
  lVar2 = 0;
  lVar3 = (ulong)param_3 << 0x20;
  do {
    if ((ulong)*(uint *)(param_2 + 0x18) <= (ulong)param_3 + lVar2) {
                    /* WARNING: Subroutine does not return */
      FUN_00db0dec();
    }
    lVar1 = lVar3 >> 0x20;
    lVar3 = lVar3 + 0x100000000;
    *(undefined *)(param_1 + lVar2) = *(undefined *)(param_2 + lVar1 + 0x20);
    lVar2 = lVar2 + 1;
  } while (lVar2 != 8);
  return;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__ToSingle
// Address: 01991258
// ==========================================================================================

undefined4 Mono_Security_BitConverterLE__ToSingle(undefined8 param_1,undefined4 param_2)

{
  undefined4 local_4;
  
  local_4 = 0;
  Mono_Security_BitConverterLE__UIntFromBytes(&local_4,param_1,param_2);
  return local_4;
}



// ==========================================================================================
// Function: Mono_Security_BitConverterLE__ToDouble
// Address: 0199127c
// ==========================================================================================

undefined  [16] Mono_Security_BitConverterLE__ToDouble(undefined8 param_1,undefined4 param_2)

{
  undefined auVar1 [16];
  ulong local_8;
  
  local_8 = 0;
  Mono_Security_BitConverterLE__ULongFromBytes(&local_8,param_1,param_2);
  auVar1._8_8_ = 0;
  auVar1._0_8_ = local_8;
  return auVar1;
}



// ==========================================================================================
