/* ------------------------utility routines ----------------------- */
/* miscellaneous utility routines                                   */
/* ---------------------------------------------------------------- */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "rtnstat.h"

/*---------------------------------------------------------------------
** A static local global used to give more detailed information on why
** BuildReturnStatusChain() could not do its work.
---------------------------------------------------------------------*/
static int ReturnStatusCode;


/* ----------------------------------------------------------------------
   procedure:  BuildReturnStatusChain_va_arg

   NOTE: Do NOT call this function directly.  You should use the shell functions
         BuildReturnStatus() or BuildReturnStatusChain().
         
   purpose:    allocates and initializes a ReturnStatus block. A ReturnStatus
               block is used to return meaningful status information to the
               caller of a routine.

   parameters: ReturnType:  Code used to define why the ReturnStatus block
                            was built. see "ReturnType - defines" in rtnstat.h
                            for list of reserved types. May be any valid int
               ReturnCode:  Integer return code.
               NextPtr:     Pointer to optional chain of return status structs
               Message1:    pointer to optional message to be returned to
                            caller.
               Message2:    pointer to another optional message which is to
                            be returned to caller. this message may contain
                            standard formatting expressions (ie. printf
                            recognizable).
               ap           pointer to a variable argument list of 0 or more 
                            data values which are to be formatted in Message2.

   returns:    pointer to the newly allocated ReturnStatus block.

               if any error occurs (either unable to allocate memory or
               vsprintf overflows) this routine will return NULL and
               set a code into a static variable which can be checked by
               calling GetReturnStatusCode().

               Note that the strings represented by Message1 and Message2
               are copied to buffers allocated by this routine, which means
               they need to be later freed by a call to FreeReturnStatus()
   ----------------------------------------------------------------------*/
ReturnStatus *BuildReturnStatusChain_va_arg (int ReturnType,
                                      int ReturnCode,
                                      ReturnStatus *NextPtr,
                                      char *Message1,
                                      char *Message2,
                                      va_list ap)
{
  ReturnStatus *RtStatus;

//  va_list ap;                              /* used to deal with variable   */
                                           /*    argument list             */

  char *FormatBuffer;
  int Length;

  ReturnStatusCode=0;

  /*
     allocate ReturnStatus block
  */
  RtStatus = (ReturnStatus *)malloc( sizeof(ReturnStatus) );
  if (RtStatus == NULL) {
    ReturnStatusCode=RSC_MALLOC0;
    return(NULL);
    }

  /*
     move return type and return code to newly allocated ReturnStatus
          block.
  */
  RtStatus->ReturnType = ReturnType;
  RtStatus->ReturnCode = ReturnCode;

  /*
    set pointer to the chain of ReturnStatus blocks, if any
  */
  if(NextPtr!=NULL)  RtStatus->NextPtr=NextPtr;
  else RtStatus->NextPtr=NULL;

  /*
     allocate a buffer for Message1 and copy original message to the new
          buffer
  */
  if (Message1 == NULL)
    RtStatus->Message1 = NULL;
  else
    {
    RtStatus->Message1 = (char *) malloc (strlen(Message1) + 1);
    if (RtStatus->Message1 == NULL) {
      ReturnStatusCode=RSC_MALLOC1;
      return(NULL);
      }
    strcpy(RtStatus->Message1, Message1);
    }

  /*
     format the message passed in Message2
  */
  if (Message2 == NULL)
    RtStatus->Message2 = NULL;
  else
    {
    /*
       allocate a huge temporary buffer for the formatting to hopefully
       make certain that the vsprintf will never overflow
    */
    Length = (int)(2*strlen(Message2) + 1);
    if(Length<16384) Length=16384;
    FormatBuffer = (char *) malloc(Length);
    if (FormatBuffer == NULL) {
      ReturnStatusCode=RSC_MALLOC2;
      return(NULL);
      }

//    va_start ( ap, Message2 );

    /*
       if the vsprintf overflows the allocated buffer then something
       might have gotten clobbered and there is no really good way
       to recover.  We'll notify the caller by setting the static
       variable ReturnStatusCode.
    */
    if (vsprintf ( FormatBuffer, Message2, ap ) > Length){
      free(FormatBuffer);
      va_end (ap);
      if(RtStatus->Message1!=NULL) free(RtStatus->Message1);
      free(RtStatus);
      ReturnStatusCode=RSC_VSPRINTF_OVERFLOW;
      return(NULL);
      }

//    va_end (ap);

    /*
       allocate a buffer for newly formatted Message2 and copy
                it to the new buffer.
    */
    RtStatus->Message2 = (char *) malloc (strlen(FormatBuffer) + 1);
    if (RtStatus->Message2 == NULL) {
      ReturnStatusCode=RSC_MALLOC3;
      return(NULL);
      }
    strcpy(RtStatus->Message2, FormatBuffer);
    free(FormatBuffer);
    }

  return(RtStatus);
}

/***********************************************************************
** BuildReturnStatus()
**
** This function is a shell function for calling BuildReturnStatusChain_va_arg()
** It is used most of the time (instead of BuildReturnStatusChain() ) as callers
** will rarely want to chain ReturnStatuses together.
** Why have this shell function?  Well, its a long story to do with how 
** variable argument lists are handled in C.
** >>>explain the details behind having the shell functions someday
************************************************************************/
ReturnStatus *BuildReturnStatus (int ReturnType,
                                 int ReturnCode,
                                 char *Message1,
                                 char *Message2,
                                 ... )
{
   va_list ap;
   ReturnStatus *RtStatus;

   va_start(ap,Message2);
   RtStatus=BuildReturnStatusChain_va_arg(ReturnType,
                                   ReturnCode,
                                   NULL,
                                   Message1,
                                   Message2,
                                   ap);
   va_end(ap);

   return(RtStatus);
   } /* end: BuildReturnStatus() */

/***********************************************************************
** BuildReturnStatusChain()
**
** This function is a shell function for calling BuildReturnStatusChain_va_arg()
** Why have this shell function?  Well, its a long story to do with how 
** variable argument lists are handled in C.
** >>>explain the details behind having the shell functions someday
************************************************************************/
ReturnStatus *BuildReturnStatusChain (int ReturnType,
                                 int ReturnCode,
                                 ReturnStatus *NextPtr,
                                 char *Message1,
                                 char *Message2,
                                 ... )
{
   va_list ap;
   ReturnStatus *RtStatus;

   va_start(ap,Message2);
   RtStatus=BuildReturnStatusChain_va_arg(ReturnType,
                                   ReturnCode,
                                   NextPtr,
                                   Message1,
                                   Message2,
                                   ap);
   va_end(ap);

   return(RtStatus);
   } /* end: BuildReturnStatusChain() */



/***********************************************************************
** FreeReturnStatus()
**
** This function frees all the space associated with a return status
** structure allocated by BuildReturnStatusChain().
************************************************************************/
void FreeReturnStatus(ReturnStatus *RSPtr)
{
   if(RSPtr->Message1!=NULL) free(RSPtr->Message1);
   if(RSPtr->Message2!=NULL) free(RSPtr->Message2);
   if(RSPtr->NextPtr!=NULL) FreeReturnStatus(RSPtr->NextPtr);
   free(RSPtr);

   } /* end: FreeReturnStatus() */

/***********************************************************************
** GetReturnStatusCode()
**
** This function simply returns the vlaue of the local static global.
************************************************************************/
int GetReturnStatusCode(void)
{
   return(ReturnStatusCode);
   } /* end: GetReturnStatusCode() */
