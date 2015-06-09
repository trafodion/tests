#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <time.h>


#include "util.h"
#include "log.h"

extern long gDebug;

/******************
** Local Globals
******************/
int LgRetries;
char LgLogFileName[MAX_FILENAME_LEN];

/***********************************************************************
** LogInit()
**
** This function initializes the log file name and number of retries.
** These values are set in local globals used by other Logxxxx() functions.
************************************************************************/
short LogInit(char *LogFileName,int RetryCount)
{
   short ReturnCode;

   /* if the caller wants to use STDOUT as logfile it must first be...*/
   /*...closed as C automatically opens it when programs start running */
//>>> this doesn't seem to work under GCC and CYGWIN so skip it for now
//>>>   if(strcmp(LogFileName,getenv("STDOUT"))==0) fclose(stdout);

   /* set the local global values */
   strncpy(LgLogFileName,LogFileName,sizeof(LgLogFileName));
   LgRetries=RetryCount;

   /* write an initial message to the logfile just to make sure we can */
   ReturnCode=LogMsg(TIMESTAMP+LINEAFTER,"Log file '%s' initialized.\n",LogFileName);

   return(ReturnCode);
   } /* end: LogInit() */


/***********************************************************************
** LogOpen()
**
** This function will open the logfile specified in LogInit().  It will
** retry the open if an error occurs.
************************************************************************/
FILE *LogOpen(void)
{
   FILE *LogFilePtr;
   int i;

   /* loop retrying opens of the log file, if necessary */
   i=0;
   LogFilePtr=fopen(LgLogFileName,"a");
   while((LogFilePtr==NULL)&&(i<LgRetries)){
      LogFilePtr=fopen(LgLogFileName,"a");
      i++;
      }

   /* if our logfile can't be opened then just return a NULL pointer */
   /* otherwise return the log file pointer */
   return(LogFilePtr);

   } /* end: LogOpen() */


/***********************************************************************
** LogMsg()
**
** This function is a shell for fprintf().  It will open, fprintf to, and
** close the log file which was specified in the LogInit() function call.
** Several options can be specified like to have a time stamp written
** to the log file or an endling separation line printed to make it
** easier to read different error messages in the log file.
************************************************************************/
short LogMsg(int Options,char *Format, ...)
{
   va_list ArgumentList;
   FILE *LogFilePtr;
   time_t TempTime;
   struct tm *TimeBlockPtr;

   va_start(ArgumentList,Format);

   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   /* write out the beginning line separator if requested */
   if(Options&LINES){
      fprintf(LogFilePtr,"================================================="
                         "======================\n");
      }
   /* write out a timestamp if requested */
   if(Options&TIMESTAMP){
      TempTime=time(NULL);
      TimeBlockPtr=localtime(&TempTime);
      fprintf(LogFilePtr,"[%04d-%02d-%02d_%02d:%02d:%02d] ",
      		TimeBlockPtr->tm_year+1900,
            TimeBlockPtr->tm_mon+1,
            TimeBlockPtr->tm_mday,
            TimeBlockPtr->tm_hour,
            TimeBlockPtr->tm_min,
            TimeBlockPtr->tm_sec);
      }

   /* prepend the internal error string if requested */
   if(Options&INTERNALERRMSG){
      fprintf(LogFilePtr,"***INTERNAL ERROR: ");
      }

   /* prepend the error string if requested */
   if(Options&ERRMSG){
      fprintf(LogFilePtr,"***ERROR: ");
      }
   if(Options&INFOMSG){
      fprintf(LogFilePtr,"***INFO: ");
      }
   if(Options&DEBUGMSG){
      if(gDebug) fprintf(LogFilePtr,"***DEBUG: ");
      }

   vfprintf(LogFilePtr,Format,ArgumentList);

   /* write out the end line separator if requested */
   if((Options&LINES)||(Options&LINEAFTER)){
      fprintf(LogFilePtr,"================================================="
                         "======================\n");
      }

   fclose(LogFilePtr);

   va_end(ArgumentList);

   return(SUCCESS);

   } /* end: LogMsg() */


/***********************************************************************
** LogPrintf()
**
** This function is a shell for vfprintf().  It is basically the same as the
** previous function, LogMsg(), except that its argument list is compatible
** with printf().
************************************************************************/
short LogPrintf(char *Format, ...)
{
   va_list ArgumentList;
   FILE *LogFilePtr;

   va_start(ArgumentList,Format);

   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   vfprintf(LogFilePtr,Format,ArgumentList);

   fclose(LogFilePtr);

   va_end(ArgumentList);

   return(SUCCESS);

   } /* end: LogPrintf() */

/***********************************************************************
** LogReturnStatus()
**
** This function will format the information in a ReturnStatus structure
** and write it out to the log file.
************************************************************************/
short LogReturnStatus(ReturnStatus *RSPtr)
{
   short ReturnCode;

   ReturnCode=LogMsg(TIMESTAMP+ERRMSG,
                     "ReturnType=%d  ReturnCode=%d\n",
                     RSPtr->ReturnType,RSPtr->ReturnCode);
   if(ReturnCode!=SUCCESS) return(FAILURE);

   if(RSPtr->Message1!=NULL) {
      ReturnCode=LogMsg(0,"%s",RSPtr->Message1);
      if(ReturnCode!=SUCCESS) return(FAILURE);
      }

   if(RSPtr->Message2!=NULL) {
      ReturnCode=LogMsg(0,"%s",RSPtr->Message2);
      if(ReturnCode!=SUCCESS) return(FAILURE);
      }

   ReturnCode=LogMsg(LINEAFTER,"\n");
   if(ReturnCode!=SUCCESS) return(FAILURE);

   return(SUCCESS);

   } /* end: LogReturnStatus() */

