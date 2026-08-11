// Function: ~domain_error
// Address: 00eaca14
// ==========================================================================================

/* std::domain_error::~domain_error() */

void __thiscall std::domain_error::~domain_error(domain_error *this)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  long lVar4;
  int *piVar5;
  
  lVar4 = *(long *)(this + 8);
  *(undefined **)this = PTR_vtable_01ff5908 + 0x10;
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
// Function: ~domain_error
// Address: 00eacbac
// ==========================================================================================

/* std::domain_error::~domain_error() */

void __thiscall std::domain_error::~domain_error(domain_error *this)

{
  int iVar1;
  char cVar2;
  bool bVar3;
  long lVar4;
  int *piVar5;
  
  lVar4 = *(long *)(this + 8);
  *(undefined **)this = PTR_vtable_01ff5908 + 0x10;
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
// Function: ~domain_error
// Address: 01ec6fd0
// ==========================================================================================

void __thiscall std::domain_error::~domain_error(domain_error *this)

{
  (*(code *)PTR__domain_error_01ff6a08)();
  return;
}



// ==========================================================================================
