// Function: runtime_error
// Address: 00e8a820
// ==========================================================================================

/* std::runtime_error::runtime_error(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&) */

void __thiscall std::runtime_error::runtime_error(runtime_error *this,basic_string *param_1)

{
  long lVar1;
  long *plVar2;
  basic_string *__src;
  
  *(undefined **)this = PTR_vtable_01ff5910 + 0x10;
  __src = *(basic_string **)(param_1 + 0x10);
  if (((byte)*param_1 & 1) == 0) {
    __src = param_1 + 1;
  }
                    /* try { // try from 00e8a858 to 00e8a86f has its CatchHandler @ 00e8a8a4 */
  lVar1 = __strlen_chk(__src,0xffffffffffffffff);
  plVar2 = (long *)operator_new(lVar1 + 0x19);
  *plVar2 = lVar1;
  plVar2[1] = lVar1;
  *(undefined4 *)(plVar2 + 2) = 0;
  memcpy(plVar2 + 3,__src,lVar1 + 1);
  *(long **)(this + 8) = plVar2 + 3;
  return;
}



// ==========================================================================================
// Function: runtime_error
// Address: 00e8a8b8
// ==========================================================================================

/* std::runtime_error::runtime_error(char const*) */

void __thiscall std::runtime_error::runtime_error(runtime_error *this,char *param_1)

{
  long lVar1;
  long *plVar2;
  
  *(undefined **)this = PTR_vtable_01ff5910 + 0x10;
                    /* try { // try from 00e8a8e4 to 00e8a8fb has its CatchHandler @ 00e8a930 */
  lVar1 = __strlen_chk(param_1,0xffffffffffffffff);
  plVar2 = (long *)operator_new(lVar1 + 0x19);
  *plVar2 = lVar1;
  plVar2[1] = lVar1;
  *(undefined4 *)(plVar2 + 2) = 0;
  memcpy(plVar2 + 3,param_1,lVar1 + 1);
  *(long **)(this + 8) = plVar2 + 3;
  return;
}



// ==========================================================================================
// Function: runtime_error
// Address: 00e8a944
// ==========================================================================================

/* std::runtime_error::runtime_error(std::runtime_error const&) */

void __thiscall std::runtime_error::runtime_error(runtime_error *this,runtime_error *param_1)

{
  char cVar1;
  bool bVar2;
  long lVar3;
  int *piVar4;
  
  *(undefined **)this = PTR_vtable_01ff5910 + 0x10;
  lVar3 = *(long *)(param_1 + 8);
  *(long *)(this + 8) = lVar3;
  piVar4 = (int *)(lVar3 + -8);
  do {
    cVar1 = '\x01';
    bVar2 = (bool)ExclusiveMonitorPass(piVar4,0x10);
    if (bVar2) {
      *piVar4 = *piVar4 + 1;
      cVar1 = ExclusiveMonitorsStatus();
    }
  } while (cVar1 != '\0');
  return;
}



// ==========================================================================================
// Function: ~runtime_error
// Address: 00eacae0
// ==========================================================================================

/* std::runtime_error::~runtime_error() */

void __thiscall std::runtime_error::~runtime_error(runtime_error *this)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  long lVar4;
  int *piVar5;
  
  lVar4 = *(long *)(this + 8);
  *(undefined **)this = PTR_vtable_01ff5910 + 0x10;
  piVar5 = (int *)(lVar4 + -8);
  do {
    iVar1 = *piVar5;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(piVar5,0x10);
    if (bVar3) {
      *piVar5 = iVar1 + -1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  if (iVar1 + -1 < 0) {
    operator_delete((void *)(lVar4 + -0x18));
  }
  bad_alloc::~bad_alloc((bad_alloc *)this);
  return;
}



// ==========================================================================================
// Function: ~runtime_error
// Address: 00eacb3c
// ==========================================================================================

/* std::runtime_error::~runtime_error() */

void __thiscall std::runtime_error::~runtime_error(runtime_error *this)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  long lVar4;
  int *piVar5;
  
  lVar4 = *(long *)(this + 8);
  *(undefined **)this = PTR_vtable_01ff5910 + 0x10;
  piVar5 = (int *)(lVar4 + -8);
  do {
    iVar1 = *piVar5;
    cVar2 = '\x01';
    bVar3 = (bool)ExclusiveMonitorPass(piVar5,0x10);
    if (bVar3) {
      *piVar5 = iVar1 + -1;
      cVar2 = ExclusiveMonitorsStatus();
    }
  } while (cVar2 != '\0');
  if (iVar1 + -1 < 0) {
    operator_delete((void *)(lVar4 + -0x18));
  }
  bad_alloc::~bad_alloc((bad_alloc *)this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: runtime_error
// Address: 01ec66c0
// ==========================================================================================

void __thiscall std::runtime_error::runtime_error(runtime_error *this,char *param_1)

{
  (*(code *)PTR_runtime_error_01ff6580)();
  return;
}



// ==========================================================================================
// Function: runtime_error
// Address: 01ec6860
// ==========================================================================================

void __thiscall std::runtime_error::runtime_error(runtime_error *this,basic_string *param_1)

{
  (*(code *)PTR_runtime_error_01ff6650)();
  return;
}



// ==========================================================================================
// Function: runtime_error
// Address: 01ec6f60
// ==========================================================================================

void __thiscall std::runtime_error::runtime_error(runtime_error *this,basic_string *param_1)

{
  (*(code *)PTR_runtime_error_01ff69d0)();
  return;
}



// ==========================================================================================
// Function: ~runtime_error
// Address: 01ec6f70
// ==========================================================================================

void __thiscall std::runtime_error::~runtime_error(runtime_error *this)

{
  (*(code *)PTR__runtime_error_01ff69d8)();
  return;
}



// ==========================================================================================
