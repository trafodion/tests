/**************************************************************
** ODBCcommon.c
**
** This file contains common functions to support ODBC usage
**************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sqlext.h>
//#include <assert.h>
#include "ODBCcommon.h"
#include "log.h"

/****************************************************************
** ReturncodeToChar()
**
** This function will attempt to convert a returncode from an
** ODBC function call into a more user friendly character string.
** If the returncode isn't one of the standard errors then this
** function converts the returncode into a numeric string.
****************************************************************/
char *ReturncodeToChar(RETCODE retcode, char *buf)
{
   switch (retcode) {
      case SQL_SUCCESS:
         strcpy (buf, "SQL_SUCCESS");
         break;
      case SQL_ERROR:
         strcpy (buf, "SQL_ERROR");
         break;
      case SQL_SUCCESS_WITH_INFO:
         strcpy (buf, "SQL_SUCCESS_WITH_INFO");
         break;
      case SQL_NO_DATA_FOUND:
         strcpy (buf, "SQL_NO_DATA_FOUND");
         break;
      case SQL_NEED_DATA:
         strcpy (buf, "SQL_NEED_DATA");
         break;
      case SQL_INVALID_HANDLE:
         strcpy (buf, "SQL_INVALID_HANDLE");
         break;
      case SQL_STILL_EXECUTING:
         strcpy (buf, "SQL_STILL_EXECUTING");
         break;
      default:
         sprintf(buf,"%d",retcode);
	}
	return buf;
}

/**************************************************************
** CheckReturnCode()
**
** This function is used to compare an actual return code from
** a function to an expected value.  It will log a message
** if the expected return code was not correct. It should never
** be called directly.  It should always be invoked through the
** CHECKRC macro found in "ODBCcommon.h".
***************************************************************/
Boolean CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   char *FunctionName,
   char *SourceFile,
   short LineNum)
{
	char exp[30];
	char act[30];

	if(expected==actual) return(TRUE);
   LogMsg(NONE,"");
   LogMsg(ERRMSG+TIMESTAMP,"%s: Expected: %s(%d) Actual: %s(%d)\n",
		FunctionName,
		ReturncodeToChar(expected,exp),expected,
		ReturncodeToChar(actual,act),actual);
   LogMsg(NONE,"   File: %s   Line: %d\n",SourceFile,LineNum);
   return(FALSE);
}

/**************************************************************
** CheckReturnCodeString()
**
** This function is used to compare an actual return code from
** a function to an expected value.  It will return a pointer to
** a message if the expected return code was not correct. It
** should never be called directly.  It should always be invoked
** through the CHECKRC_STR macro found in "ODBCcommon.h".
***************************************************************/
char *CheckReturnCodeString(
   RETCODE expected,
   RETCODE actual,
   char *FunctionName,
   char *SourceFile,
   short LineNum)
{
	char exp[30];
	char act[30];
	char MessageBuf[1000];
	char *pMessage;

	if(expected==actual) return(NULL);
	sprintf(MessageBuf,"\n"
							 "***ERROR: %s: Expected: %s(%d) Actual: %s(%d)\n"
							 "   File: %s   Line: %d\n",
							FunctionName,ReturncodeToChar(expected,exp),expected,
							ReturncodeToChar(actual,act),actual,
							SourceFile,LineNum);
	pMessage=malloc(strlen(MessageBuf+1));
	strcpy(pMessage,MessageBuf);

   return(pMessage);
}

/**************************************************************
** FullConnect()
**
** This function will attempt to establish a full connection
** based upon the information within the structure passed in to it.
***************************************************************/
Boolean FullConnect(char *DataSource,
                    char *UserID, char *Password,
                    SQLHENV *henv_ptr, SQLHDBC *hdbc_ptr){
	RETCODE returncode;
	SQLHENV henv = 0;
	SQLHDBC hdbc = 0;

	returncode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle(SQL_HANDLE_ENV)")) {
		LogAllErrors(henv,NULL,NULL);
		return(FALSE);
	}

	// setup as an ODBC 3 connection, ODBC 2 is too old to worry about anymore
	returncode = SQLSetEnvAttr(henv,SQL_ATTR_ODBC_VERSION,(SQLPOINTER)SQL_OV_ODBC3,NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr(SQL_ATTR_ODBC_VERSION)")) {
		LogAllErrors(henv,NULL,NULL);
		SQLFreeHandle(SQL_HANDLE_ENV, henv);
		return(FALSE);
	}

	returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle(SQL_HANDLE_DBC)")){
		LogAllErrors(henv,hdbc,NULL);
		/* Cleanup. No need to check return code from SQLFreeHandle since we are already failing */
		SQLFreeHandle(SQL_HANDLE_ENV, henv);
		return(FALSE);
	}
	returncode = SQLConnect(hdbc,
                           DataSource,SQL_NTS,
                           UserID,SQL_NTS,
                           Password,SQL_NTS
                           );

	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO)){
		CHECKRC(SQL_SUCCESS,returncode,"SQLConnect");
		LogAllErrors(henv,hdbc,NULL);
		/* Cleanup.  No need to check return codes since we are already failing */
		SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
		SQLFreeHandle(SQL_HANDLE_ENV, henv);
		return(FALSE);
	}

	*henv_ptr = henv;
	*hdbc_ptr = hdbc;

	/* Connection established */
	return(TRUE);
}  /* FullConnect() */

/**************************************************************
** FullDisconnect()
**
** This function disconnects a single connection based upon the
** information passed in to it.  If this function returns FALSE
** it does not always mean the disconnect did not happen.  For
** FALSE, the disconnect might have happened and there might have
** been some other error.
***************************************************************/
Boolean FullDisconnect(SQLHENV henv, SQLHDBC hdbc)
{
  RETCODE returncode;
  Boolean Result;

  Result=TRUE;

  /* Disconnect from the data source.  If errors, still go on and */
  /* try to free the handles */
  returncode = SQLDisconnect(hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDisconnect")) {
		Result=FALSE;
		LogAllErrors(henv,hdbc,NULL);
	}

  /* Free up all handles used by this connection */
  returncode = SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle")) {
		Result=FALSE;
		LogAllErrors(henv,hdbc,NULL);
	}

  returncode = SQLFreeHandle(SQL_HANDLE_ENV, henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv")) {
		Result=FALSE;
		LogAllErrors(henv,NULL,NULL);
	}

  return(Result);
}  /* FullDisconnect() */

/**************************************************************
** LogAllErrors()
**
** A wrapper for GetAllErrors that will log the error string
** to the log file.
***************************************************************/
void LogAllErrors(SQLHENV henv,
                  SQLHDBC hdbc,
                  SQLHSTMT hstmt)
{
	char *pError;

	pError=GetAllErrors(henv,hdbc,hstmt);
	LogPrintf("%s\n",pError);
	free(pError);
}

/**************************************************************
** GetAllErrors()
**
** This function loops through calls to SQLGetDiagRec() building strings
** for all error messages that might be there and returns a buffer
** with any error messages.
***************************************************************/
char *GetAllErrors(SQLHENV henv,
                  SQLHDBC hdbc,
                  SQLHSTMT hstmt)
{
  SQLCHAR		buf[MAX_STRING_SIZE];
  SQLCHAR		State[STATE_SIZE];
  SQLINTEGER	NativeError;
  RETCODE returncode;
  Boolean MsgDisplayed;
  SQLSMALLINT	ErrorMsglen;
  SQLSMALLINT i =1;
  char ErrorBuf[MAX_STRING_SIZE];
  char *pErrorBuf;

  MsgDisplayed=FALSE;
  pErrorBuf=ErrorBuf;

   /* Get any hstmt error messages */
   if (hstmt != NULL) {
		i=1;
		returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
		while((returncode == SQL_SUCCESS) ||
		     (returncode == SQL_SUCCESS_WITH_INFO)){
			State[STATE_SIZE-1]=NULL;
			sprintf(pErrorBuf,"   State: %s\n"
						 "   Native Error: %ld\n"
						 "   Error: %s\n",State,NativeError,buf);
			MsgDisplayed=TRUE;
			pErrorBuf=ErrorBuf+strlen(ErrorBuf);
			i++;
			returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
		}
   }

   /* Log any hdbc error messages */
   if (hdbc != NULL) {
	   i=1;
	   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, hdbc,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
	   while((returncode == SQL_SUCCESS) ||
			 (returncode == SQL_SUCCESS_WITH_INFO)){
			State[STATE_SIZE-1]=NULL;
			sprintf(pErrorBuf,"   State: %s\n"
						 "   Native Error: %ld\n"
						 "   Error: %s\n",State,NativeError,buf);
			MsgDisplayed=TRUE;
			pErrorBuf=ErrorBuf+strlen(ErrorBuf);
			i++;
		   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, hdbc,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
		  }
   }

   /* Log any henv error messages */
   if (henv != NULL) {
	   i=1;
	   returncode = SQLGetDiagRec(SQL_HANDLE_ENV, henv,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
	   while((returncode == SQL_SUCCESS) ||
			 (returncode == SQL_SUCCESS_WITH_INFO)){
			State[STATE_SIZE-1]=NULL;
			sprintf(pErrorBuf,"   State: %s\n"
						 "   Native Error: %ld\n"
						 "   Error: %s\n",State,NativeError,buf);
    		MsgDisplayed=TRUE;
			pErrorBuf=ErrorBuf+strlen(ErrorBuf);
			i++;
			returncode = SQLGetDiagRec(SQL_HANDLE_ENV, henv,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
		  }
   }

   /* if no error messages were displayed then display a message */
	if(!MsgDisplayed){
		sprintf(ErrorBuf,"There were no error messages for SQLGetDiagRec() to display\n");
	}
	else {
		pErrorBuf=NULL;
	}

	// allocate space for the returned error buffer
	pErrorBuf=malloc(strlen(ErrorBuf)+1);
	strcpy(pErrorBuf,ErrorBuf);

	return(pErrorBuf);
	}
