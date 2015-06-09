/***********************************************************************
** log.h
** This include file contains the external declarations and any needed
** typedefs and defines for the functions in LOG.C.
***********************************************************************/
#ifndef __LOGH      /* this prevents multiple copies of this... */
#define __LOGH      /* ...include file from being #included... */

#include "rtnstat.h"

/*************************
** defines and typedefs **
*************************/

/** Valid Values for LogMsg Options parameter **/
#define NONE				0x00
#define ERRMSG          0x01
#define TIMESTAMP       0x02
#define LINES           0x04
#define LINEAFTER       0x08
#define INTERNALERRMSG  0x10
#define INFOMSG         0x20
#define DEBUGMSG        0x40

/**************************
** external declarations **
**************************/
extern short LogInit(char *LogFileName,int RetryCount);
extern short LogMsg(int Options,char *Format, ...);
extern short LogPrintf(char *Format,...);
extern short LogReturnStatus(ReturnStatus *RSPtr);

#endif
