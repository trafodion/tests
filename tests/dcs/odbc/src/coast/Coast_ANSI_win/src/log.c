/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

#include <stdlib.h>    
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include "basedef.h"
#include "log.h"
#define PLATFORM
#if !defined(PLATFORM)
	#include <io.h>
#endif

/******************
** Local Globals
******************/
int		LgRetries;
char	LgLogFileName[MAX_FILENAME_LENGTH];
char	LgErrStr[255];
long	LgMark;
int		isDebug = 0;

/***********************************************************************
** LogInit()
**
** This function initializes the log file name and number of retries.
** These values are set in local globals used by other Logxxxx() functions.
************************************************************************/
short LogInit(char *LogFileName,int RetryCount,char *ErrorString)
{
   short ReturnCode;
   
   /* if the caller wants to use STDOUT as logfile it must first be...*/
   /*...closed as C automatically opens it when programs start running */
   /* NOTE: this is commented out for now because on a PC the getenv("STDOUT") */
   /*       function call returns NULL, although it works on certain system */
   //if(strcmp(LogFileName,getenv("STDOUT"))==0) fclose(stdout);

   /* set the local global values */
   strncpy(LgLogFileName,LogFileName,sizeof(LgLogFileName)-1);
   strncpy(LgErrStr,ErrorString,sizeof(LgErrStr)-1);
   
   LgRetries=RetryCount;

   /* write an initial message to the logfile just to make sure we can */
   ReturnCode=LogMsg(TIME_STAMP+ENDLINE,"Log file '%s' initialized.\n",LogFileName);

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
** LogGetPath()
** This function returns the drive and path of the main log file in buffers
** 'drive' and 'dir' (These buffers must be of size _MAX_DRIVE and _MAX_DIR
** respectively.  This allows the fxns in AuxLog.c 
** 
************************************************************************/
//void LogGetPath( char *drive, char *dir )
//{
//	_splitpath( LgLogFileName, drive, dir, NULL, NULL );
//}


/***********************************************************************
** LogMsg()
**
** This function is a shell for fprintf().  It will open, fprintf to, and
** close the log file which was specified in the LogInit() function call.
** Several options can be specified like to have a time stamp written
** to the log file or an endline separation line printed to make it
** easier to read different error messages in the log file.
************************************************************************/
short LogMsg(int Options,char *Format, ...)
{
   va_list ArgumentList;
   FILE *LogFilePtr;
   time_t TempTime;
   struct tm *TimeBlockPtr;

   if(Options&INFO && isDebug)
	   return (SUCCESS);

   va_start(ArgumentList,Format);

   LogFilePtr=NULL;
   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   // write out the beginning line separator if requested */
   if(Options&LINEBEFORE)
	 {
			fprintf(LogFilePtr,"================================================="
                         "======================\n");
	 }
	 // write out the test number
/*   if(Options&TESTSCOUNT)
	 {
			TestsPerAPI = TestsPerAPI + 1;
      fprintf(LogFilePtr,"Test Number ==> %d\n",TestsPerAPI);
	 }
	 // set the counter back to 0;
   if(Options&TESTSINIT)
	 {
			TestsPerAPI = 0;
	 } */
   // write out a long timestamp if requested 
   if(Options&TIME_STAMP){
      TempTime=time(NULL);
      fprintf(LogFilePtr,"%s\n",ctime(&TempTime));
      }

   // write out a shorter timestamp if requested */
   if(Options&SHORTTIMESTAMP){
      TempTime=time(NULL);
      TimeBlockPtr=localtime(&TempTime);
      fprintf(LogFilePtr,"%02d:%02d:%02d  ",TimeBlockPtr->tm_hour,
                                            TimeBlockPtr->tm_min,
                                            TimeBlockPtr->tm_sec);
      }

   /* prepend the internal error string if requested */
   if(Options&INTERNALERRMSG){
      fprintf(LogFilePtr,"%s (INTERNAL ERROR):",LgErrStr);
      }

   /* prepend the error string if requested */
   if(Options&ERRMSG){
      fprintf(LogFilePtr,LgErrStr);
      }

   vfprintf(LogFilePtr,Format,ArgumentList);

   /* write out the end line separator if requested */
   if(Options&LINEAFTER){
      fprintf(LogFilePtr,"================================================="
                         "======================\n");
      }

   fflush(LogFilePtr);
   fclose(LogFilePtr);

   va_end(ArgumentList);

   return(SUCCESS);

} /* end: LogMsg() */

/***********************************************************************
** LogSetMark()
**
** This function will set a marker (LgMark) to the current EOF of the 
** log file.  It is used, along with LogSetEofAtMark(), to allow test
** functions to backup and erase unessential data from the log file.
************************************************************************/
short LogSetMark()
{
	short ReturnCode;
#ifndef PLATFORM
	short FileHandle;
	FILE *Logfile;
	int error;
#endif
   
  ReturnCode=0;

#ifdef PLATFORM
  {
/*	Logfile=fopen(LgLogFileName,"r+");
	error=fgetpos(Logfile, position);
    fclose(Logfile); */
  }
#else
  {
	FileHandle=_open(LgLogFileName,_O_RDWR);
	LgMark=_filelength(FileHandle);
	_close(FileHandle);
  }	
#endif

	return(ReturnCode);
}

/***********************************************************************
** LogSetEofAtMark()
**
** This function will reset the EOF of the log file to the position of
** the mark (LgMark).  It is used, along with LogSetMark(), to allow test
** functions to backup and erase unessential data from the log file.
************************************************************************/
short LogSetEofAtMark()
{
	short ReturnCode;
#ifndef PLATFORM
	short FileHandle;
	FILE *Logfile;
	int error;
#endif
   
   ReturnCode=0;

#ifdef PLATFORM
  {
/*	Logfile=fopen(LgLogFileName,"r+");
	error=fsetpos(Logfile, position);
    fclose(Logfile); */
  }
#else
  {     
	   FileHandle=_open(LgLogFileName,_O_RDWR);
	  _chsize(FileHandle,LgMark);
	  _close(FileHandle);
  }
#endif

	return(ReturnCode);
   }

/***********************************************************************
** LogPrintf()
**
** This function is a shell for fprintf().  It is basically the same as the
** function, LogMsg(), except that its argument list is compatible with
** printf().
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
** LogMsgf)
**
** This function is a shell for fprintf().  It is basically the same as the
** previous function, LogMsg(), except that its argument list is compatible
** with printf().
************************************************************************/
short LogMsgf(char *Format, ...)
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

   } /* end: LogMsgf() */

