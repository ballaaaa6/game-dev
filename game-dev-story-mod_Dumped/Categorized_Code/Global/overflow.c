// Function: ~overflow_error
// Address: 00eacda0
// ==========================================================================================

/* std::overflow_error::~overflow_error() */

void __thiscall std::overflow_error::~overflow_error(overflow_error *this)

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
