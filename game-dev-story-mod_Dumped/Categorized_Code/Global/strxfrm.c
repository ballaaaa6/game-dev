// Function: strxfrm_l
// Address: 01ec68a0
// ==========================================================================================

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t strxfrm_l(char *__dest,char *__src,size_t __n,__locale_t __l)

{
  size_t sVar1;
  
  sVar1 = (*(code *)PTR_strxfrm_l_01ff6670)();
  return sVar1;
}



// ==========================================================================================
// Function: strxfrm_l
// Address: 0231f710
// ==========================================================================================

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t strxfrm_l(char *__dest,char *__src,size_t __n,__locale_t __l)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



// ==========================================================================================
