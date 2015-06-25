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

#ifndef __LOGH      /* this prevents multiple copies of this... */
#define __LOGH      /* ...include file from being #included... */
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
#define INFO			0x30	 /* Will print only if debugMode = on */
//#define	TESTSINIT				0x40		 /* initials the tests number to 0 */
//#define	TESTSCOUNT			0x50		 /* Keeps track of number of tests in each API */
#ifdef __cplusplus
extern "C" {
#endif

extern int isDebug;

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
			char *drive,
			char *dir
			);

extern short LogInit(
   char *   LogFileName,   
   int      RetryCount,
   char *   ErrorString);
   
extern short LogMsg(
   int      Options,
   char *   Format,
   ...);

extern short LogPrintf(
   char *   Format,
   ...);

extern short LogSetMark();

extern short LogSetEofAtMark();

extern char LgLogFileName[MAX_FILENAME_LENGTH];

/* older function left here because some programs still use it */
/* use LogPrintf() instead of LogMsgf() */
extern short LogMsgf(
   char *   Format,
   ...);

#ifdef __cplusplus
}
#endif

#endif
