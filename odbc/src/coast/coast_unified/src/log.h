#ifndef __LOGH      /* this prevents multiple copies of this... */
#define __LOGH      /* ...include file from being #included... */

#ifdef unixcli
#include "utchar.h"
#else
#include <tchar.h>
#endif

/***********************************************************************
** log.h
** This include file contains the external declarations and any needed
** typedefs and defines for the functions in LOG.C.
** These functions provide a standard way to write to a log file and
** automatically flush all output to the file for each function call.
** This minimizes (and in most cases, eliminates) lost output when a 
** program hangs or halts the system it is running on.
***********************************************************************/
/******* CHANGES *******************************************************
** Andrea Reif 10/29 Added LogGetPath to return path of log file to allow
** other programs to use the same directory.
*/
/*************************
** defines and typedefs **
*************************/

/*
** Valid Values for LogMsg() <Options> parameter
** These can be easily used to make the LogMsg function display standard things
** like a time stamp and/or a standard error prefix like "***ERROR:" instead of
** you having to build those things.  More than one option may be used by
** ORing or adding options.  Example1: ERRMSG | TIME_STAMP   Example 2: ERRMSG + LINES
*/ 
#define NONE            0x00     /* Don't use any options.  Equivalent to using LogPrintf() */
#define ERRMSG          0x01     /* Prefix the <ErrorString> to the front of the message */
#define TIME_STAMP      0x02     /* Display a timestamp on the line before the message */
#define LINEBEFORE      0x04     /* Display separating lines before and after the message */
#define LINEAFTER       0x08     /* Display a separating line after the message */
#define ENDLINE         LINEAFTER/* Some older programs used to use ENDLINE instead of LINEAFTER */
#define INTERNALERRMSG  0x10     /* Prefix ***INTERNAL ERROR: to the fromt of the message */
#define SHORTTIMESTAMP  0x20     /* Prefix a shorter timestamp to the front of the message */
//#define	TESTSINIT				0x40		 /* initials the tests number to 0 */
//#define	TESTSCOUNT			0x50		 /* Keeps track of number of tests in each API */
#ifdef __cplusplus
extern "C" {
#endif

/**************************
** external declarations **
**************************/
/*
** LogInit() creates and sets up the log file.  This is the only
** place the log file name is specified.  Other Logxxxx functions
** will automatically write to the log file specified in the last
** call to LogInit().  
** NOTE: There is no LogClose() function.  It is not needed.
*/

/*******************************************************
** LogGetPath()
** Returns the drive and directory of the log file specified
** in LogInit.  This allows the functions in AuxLog.c to use
** the same directory for the log files of other programs.
** The buffers 'drive' and 'dir' must be of length _MAX_DRIVE
** and _MAX_DIR respectively.
**********************************************************
*/
extern void LogGetPath(
			TCHAR *drive,
			TCHAR *dir
			);

extern short LogInit(
   TCHAR *   LogFileName,   
   int      RetryCount,
   TCHAR *   ErrorString);
   
extern short LogMsg(
   int      Options,
   TCHAR *   Format,
   ...);

extern short LogPrintf(
   TCHAR *   Format,
   ...);

extern short LogSetMark();

extern short LogSetEofAtMark();

extern TCHAR LgLogFileName[MAX_FILENAME_LENGTH];

/* older function left here because some programs still use it */
/* use LogPrintf() instead of LogMsgf() */
extern short LogMsgf(
   TCHAR *   Format,
   ...);

#ifdef __cplusplus
}
#endif

#endif
