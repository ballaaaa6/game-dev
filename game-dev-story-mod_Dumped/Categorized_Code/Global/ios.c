// Function: ~ios_base
// Address: 00e4e0c4
// ==========================================================================================

/* std::__ndk1::ios_base::~ios_base() */

void __thiscall std::__ndk1::ios_base::~ios_base(ios_base *this)

{
  long lVar1;
  
  *(undefined **)this = PTR_vtable_01ff55f0 + 0x10;
  if (*(long *)(this + 0x48) != 0) {
    lVar1 = *(long *)(this + 0x48) + -1;
    do {
                    /* try { // try from 00e4e100 to 00e4e10b has its CatchHandler @ 00e4e14c */
      (**(code **)(*(long *)(this + 0x38) + lVar1 * 8))
                (0,this,*(undefined4 *)(*(long *)(this + 0x40) + lVar1 * 4));
      lVar1 = lVar1 + -1;
    } while (lVar1 != -1);
  }
  locale::~locale((locale *)(this + 0x30));
  free(*(void **)(this + 0x38));
  free(*(void **)(this + 0x40));
  free(*(void **)(this + 0x58));
  free(*(void **)(this + 0x70));
  return;
}



// ==========================================================================================
// Function: ~ios_base
// Address: 00e5b380
// ==========================================================================================

/* std::__ndk1::ios_base::~ios_base() */

void __thiscall std::__ndk1::ios_base::~ios_base(ios_base *this)

{
  ~ios_base(this);
  operator_delete(this);
  return;
}



// ==========================================================================================
// Function: ~ios_base
// Address: 01ec6160
// ==========================================================================================

void __thiscall std::__ndk1::ios_base::~ios_base(ios_base *this)

{
  (*(code *)PTR__ios_base_01ff62d0)();
  return;
}



// ==========================================================================================
