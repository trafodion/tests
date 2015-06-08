#include <stdlib.h>    
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <windows.h>
#include <time.h>
#include <fcntl.h>
#include "basedef.h"
#include "log.h"
#include "common.h"
#define NSK_PLATFORM
#if !defined(NSK_PLATFORM)
	#include <io.h>
#endif

/******************
** Local Globals
******************/
int		LgRetries;
TCHAR	LgLogFileName[MAX_FILENAME_LENGTH];
TCHAR	LgErrStr[255];
long	LgMark;

/***********************************************************************
** LogInit()
**
** This function initializes the log file name and number of retries.
** These values are set in local globals used by other Logxxxx() functions.
************************************************************************/
short LogInit(TCHAR *LogFileName,int RetryCount,TCHAR *ErrorString)
{
   short ReturnCode;
   
   /* if the caller wants to use STDOUT as logfile it must first be...*/
   /*...closed as C automatically opens it when programs start running */
   /* NOTE: this is commented out for now because on a PC the getenv("STDOUT") */
   /*       function call returns NULL, although it works on a Tandem system */
   //if(_tcscmp(LogFileName,getenv("STDOUT"))==0) _tfclose(stdout);

   /* set the local global values */
   _tcsncpy(LgLogFileName,LogFileName,sizeof(LgLogFileName)-1);
   _tcsncpy(LgErrStr,ErrorString,sizeof(LgErrStr)-1);
   
   LgRetries=RetryCount;

   /* write an initial message to the logfile just to make sure we can */
   ReturnCode=LogMsg(TIME_STAMP+ENDLINE,_T("Log file '%s' initialized.\n"),LogFileName);

   return(ReturnCode);
   } /* end: LogInit() */



/***********************************************************************
** LogOpen()
**
** This function will open the logfile specified in LogInit().  It will
** retry the open if an error occurs.
************************************************************************/
TFILE *LogOpen(void)
{
   TFILE *LogFilePtr;
   int i;

   /* loop retrying opens of the log file, if necessary */
   i=0;
   LogFilePtr=_tfopen(LgLogFileName,_T("a"));
   while((LogFilePtr==NULL)&&(i<LgRetries)){
      LogFilePtr=_tfopen(LgLogFileName,_T("a"));
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
//void LogGetPath( TCHAR *drive, TCHAR *dir )
//{
//	_splitpath( LgLogFileName, drive, dir, NULL, NULL );
//}


/***********************************************************************
** LogMsg()
**
** This function is a shell for _ftprintf().  It will open, _ftprintf to, and
** close the log file which was specified in the LogInit() function call.
** Several options can be specified like to have a time stamp written
** to the log file or an endline separation line printed to make it
** easier to read different error messages in the log file.
************************************************************************/
short LogMsg(int Options,TCHAR *Format, ...)
{
   va_list ArgumentList;
   TFILE *LogFilePtr;
   time_t TempTime;
   struct tm *TimeBlockPtr;

   va_start(ArgumentList,Format);

   LogFilePtr=NULL;
   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   // write out the beginning line separator if requested */
   if(Options&LINEBEFORE)
	 {
	   _ftprintf(LogFilePtr,_T("=======================================================================\n"));
	 }
	 // write out the test number
/*   if(Options&TESTSCOUNT)
	 {
			TestsPerAPI = TestsPerAPI + 1;
      _ftprintf(LogFilePtr,"Test Number ==> %d\n",TestsPerAPI);
	 }
	 // set the counter back to 0;
   if(Options&TESTSINIT)
	 {
			TestsPerAPI = 0;
	 } */
   // write out a long timestamp if requested 
   if(Options&TIME_STAMP){
      TempTime=time(NULL);
	  TCHAR* p_TimeStr = _tctime(&TempTime);
      _ftprintf(LogFilePtr,_T("%s\n"),p_TimeStr);
#ifdef UNICODE
	  free(p_TimeStr);
#endif
	  p_TimeStr = NULL;
      }

   // write out a shorter timestamp if requested */
   if(Options&SHORTTIMESTAMP){
      TempTime=time(NULL);
      TimeBlockPtr=localtime(&TempTime);
      _ftprintf(LogFilePtr,_T("%02d:%02d:%02d  "),TimeBlockPtr->tm_hour,
                                            TimeBlockPtr->tm_min,
                                            TimeBlockPtr->tm_sec);
      }

   /* prepend the internal error string if requested */
   if(Options&INTERNALERRMSG){
      _ftprintf(LogFilePtr,_T("%s (INTERNAL ERROR):"),LgErrStr);
      }

   /* prepend the error string if requested */
   if(Options&ERRMSG){
      _ftprintf(LogFilePtr,LgErrStr);
      }

   _vftprintf(LogFilePtr,Format,ArgumentList);

   /* write out the end line separator if requested */
   if(Options&LINEAFTER){
      _ftprintf(LogFilePtr,_T("=======================================================================\n"));
      }

#ifdef unixcli
   _tflush(LogFilePtr);
#else
   fflush(LogFilePtr);
#endif
   _tfclose(LogFilePtr);

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
#ifndef NSK_PLATFORM
	short FileHandle;
	TFILE *Logfile;
	int error;
#endif
   
  ReturnCode=0;

#ifdef NSK_PLATFORM
  {
/*	Logfile=fopen(LgLogFileName,"r+");
	error=fgetpos(Logfile, position);
    _tfclose(Logfile); */
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
#ifndef NSK_PLATFORM
	short FileHandle;
	TFILE *Logfile;
	int error;
#endif
   
   ReturnCode=0;

#ifdef NSK_PLATFORM
  {
/*	Logfile=fopen(LgLogFileName,"r+");
	error=fsetpos(Logfile, position);
    _tfclose(Logfile); */
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
** This function is a shell for _ftprintf().  It is basically the same as the
** function, LogMsg(), except that its argument list is compatible with
** _tprintf().
************************************************************************/
short LogPrintf(TCHAR *Format, ...)
{
   va_list ArgumentList;
   TFILE *LogFilePtr;

   va_start(ArgumentList,Format);

   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   _vftprintf(LogFilePtr,Format,ArgumentList);

   _tfclose(LogFilePtr);

   va_end(ArgumentList);

   return(SUCCESS);

} /* end: LogPrintf() */


/***********************************************************************
** LogMsgf)
**
** This function is a shell for _ftprintf().  It is basically the same as the
** previous function, LogMsg(), except that its argument list is compatible
** with _tprintf().
************************************************************************/
short LogMsgf(TCHAR *Format, ...)
{
   va_list ArgumentList;
   TFILE *LogFilePtr;

   va_start(ArgumentList,Format);

   LogFilePtr=LogOpen();
   if(LogFilePtr==NULL) return(FAILURE);

   _vftprintf(LogFilePtr,Format,ArgumentList);

   _tfclose(LogFilePtr);

   va_end(ArgumentList);

   return(SUCCESS);

   } /* end: LogMsgf() */

