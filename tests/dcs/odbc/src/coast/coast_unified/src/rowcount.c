#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

/*
---------------------------------------------------------
   TestSQLRowCount
---------------------------------------------------------
*/
PassFail TestSQLRowCount(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt;
	SQLLEN		row;
	static TCHAR *ExecDirStr[] = {_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")};
	int				cnt, fail = 0;
	int				effect = 3; /* change this if insert rows are changed */

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLRowCount"), charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping(_T("SQLRowCount_ExecDirStr_0"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLRowCount_ExecDirStr_1"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLRowCount_ExecDirStr_2"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLRowCount_ExecDirStr_3"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLRowCount_ExecDirStr_4"), var_list);
	ExecDirStr[5] = var_mapping(_T("SQLRowCount_ExecDirStr_5"), var_list);
	ExecDirStr[6] = var_mapping(_T("SQLRowCount_ExecDirStr_6"), var_list);
	ExecDirStr[7] = var_mapping(_T("SQLRowCount_ExecDirStr_7"), var_list);
	ExecDirStr[8] = var_mapping(_T("SQLRowCount_ExecDirStr_8"), var_list);
	ExecDirStr[9] = var_mapping(_T("SQLRowCount_ExecDirStr_9"), var_list);
	
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLRowcount.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLRowCount tests\n");

	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
 	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* CLEANUP */
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],SQL_NTS); /* CLEANUP */

	TESTCASE_END;  // end of setup

  for (cnt = 2; cnt <= 6; cnt++) 
	{
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[cnt],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			fail++;
		}
	}
	if (fail < 1)
	{
		TESTCASE_BEGIN("Test the positive functionality for SQLRowCount thru INSERT\n");
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[7],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			returncode=SQLRowCount(hstmt,&row);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLRowCount"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else if (row != effect)
			{
				LogMsg(ERRMSG,_T("SQLRowCount: actual row count %d, expected %d\n"),row,effect);
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		TESTCASE_END;
	
		TESTCASE_BEGIN("Test the positive functionality for SQLRowCount thru UPDATE\n");
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[8],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			returncode=SQLRowCount(hstmt,&row);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLRowCount"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else if (row != effect)
			{
				LogMsg(ERRMSG,_T("SQLRowCount: actual row count %d, expected %d\n"),row,effect);
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		TESTCASE_END;
		
		TESTCASE_BEGIN("Test the positive functionality for SQLRowCount thru DELETE\n");
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[9],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			returncode=SQLRowCount(hstmt,&row);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLRowCount"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else if (row != effect)
			{
				LogMsg(ERRMSG,_T("SQLRowCount: actual row count %d, expected %d\n"),row,effect);
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		TESTCASE_END;
	}

	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* CLEANUP */
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],SQL_NTS); /* CLEANUP */

//============================================================================================================	

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLRowcount.\n"));
	free_list(var_list);
	TEST_RETURN;
}
