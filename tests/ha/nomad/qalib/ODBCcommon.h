#ifndef __ODBCCOMMONH      /* this prevents multiple copies of this... */
#define __ODBCCOMMONH      /* ...include file from being #included... */

#include "util.h"
#include <sqlext.h>

/**************************************
** Constants, Structures, and Typedefs
**************************************/
#define STATE_SIZE				6
#define MAX_STRING_SIZE			5000


/*************************
** External declarations
*************************/
/* NOTE: Always use CHECKRC and never call CheckReturnCode directly */
#define CHECKRC(expected,actual,FunctionName) (CheckReturnCode((expected),(actual),(FunctionName),(char*)__FILE__,(short)__LINE__))

extern Boolean CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   char *comment,
   char *SourceFile,
   short LineNum);

/* NOTE: Always use CHECKRC_STR and never call CheckReturnCodeString directly */
#define CHECKRC_STR(expected,actual,FunctionName) (CheckReturnCodeString((expected),(actual),(FunctionName),(char*)__FILE__,(short)__LINE__))

char *CheckReturnCodeString(
   RETCODE expected,
   RETCODE actual,
   char *FunctionName,
   char *SourceFile,
   short LineNum);

// Function for converting ODBC values into more meaningful character strings
extern char *ReturncodeToChar(RETCODE returncode,char *buffer);

extern void LogAllErrors(SQLHENV henv,SQLHDBC hdbc,SQLHSTMT hstmt);
extern char *GetAllErrors(SQLHENV henv,SQLHDBC hdbc,SQLHSTMT hstmt);

extern Boolean FullConnect(char *DataSource, char *UID, char *PWD, SQLHENV *henv, SQLHDBC *hdbc);
extern Boolean FullDisconnect(SQLHENV henv,SQLHDBC hdbc);

#endif
