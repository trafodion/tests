#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	SQL_MAX_MESSAGE_LEN 300

/*
---------------------------------------------------------
   TestSQLError Minimum tests since this is tested all over the places
---------------------------------------------------------
*/
PassFail TestSQLError(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
	SQLHANDLE 	henv;
	SQLHANDLE 	hdbc;
	SQLHANDLE	hstmt;
	TCHAR		SqlState[STATE_SIZE];
	SDWORD		NativeError;
	TCHAR		ErrorMsg[MAX_STRING_SIZE];
	SWORD		ErrorMsglen;

	TCHAR		*CrtTab = _T("--");

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLError"), charset_file);
	if (var_list == NULL) return FAILED;

	CrtTab = var_mapping(_T("SQLError_CrtTab"), var_list);
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLError.\n"));
	
  TEST_INIT;

	returncode=FullConnect(pTestInfo);
  if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = pTestInfo->hstmt;

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
  if (returncode == SQL_SUCCESS)
	{
		TESTCASE_BEGIN("Test syntax while creating a table SQLError\n");
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab,SQL_NTS);
	  if (returncode == SQL_ERROR)
		{
			returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)hdbc, hstmt, (SQLTCHAR*)SqlState, &NativeError, (SQLTCHAR*)ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,_T("SqlState: %s and ErrorMsg: %s\n"),SqlState,ErrorMsg);
				TESTCASE_END;
			}
		}
	}
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLError.\n"));
	free_list(var_list);
	TEST_RETURN;
}
