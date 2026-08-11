// Function: dl_iterate_phdr
// Address: 01ec7190
// ==========================================================================================

void dl_iterate_phdr(void)

{
  (*(code *)PTR_dl_iterate_phdr_01ff6ae8)();
  return;
}



// ==========================================================================================
// Function: dl_iterate_phdr
// Address: 0231f838
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */

void dl_iterate_phdr(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



