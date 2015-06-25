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


#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	SQLSTR_LEN	300
/*
---------------------------------------------------------
   TestSQLNativeSql
---------------------------------------------------------
*/
PassFail TestSQLNativeSql(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt;
	TCHAR		*szSqlStrIn[3];
	TCHAR		szSqlStrOut[SQLSTR_LEN];
	SDWORD	pcbSqlStr;
   
//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLNativeSql"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	szSqlStrIn[0] = var_mapping(_T("SQLNativeSql_szSqlStrIn_1"), var_list);
	szSqlStrIn[1] = var_mapping(_T("SQLNativeSql_szSqlStrIn_2"), var_list);
	szSqlStrIn[2] = var_mapping(_T("SQLNativeSql_szSqlStrIn_3"), var_list);
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLNativeSql.\n"));

	TEST_INIT;

	returncode=FullConnect(pTestInfo);
   if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if (returncode == SQL_SUCCESS)
	{
	//==================================================================================================

		TESTCASE_BEGIN("Test the positive functionality of SQLNativeSql with null terminated string\n");
		returncode = SQLNativeSql((SQLHANDLE)hdbc, (SQLTCHAR*)szSqlStrIn[0], SQL_NTS, (SQLTCHAR*)szSqlStrOut, SQLSTR_LEN, &pcbSqlStr); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNativeSql"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		if (_tcscmp(szSqlStrOut,szSqlStrIn[0]) == 0)
		{
			LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"), szSqlStrIn[0], szSqlStrOut);
		}	
		else
		{
			TEST_FAILED;	
			LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"), szSqlStrIn[0], szSqlStrOut);
		}
		TESTCASE_END;

		//==================================================================================================

		TESTCASE_BEGIN("Test the positive functionality of SQLNativeSql with string length as input\n");
		returncode = SQLNativeSql((SQLHANDLE)hdbc, (SQLTCHAR*)szSqlStrIn[1], _tcslen(szSqlStrIn[1]), (SQLTCHAR*)szSqlStrOut, SQLSTR_LEN, &pcbSqlStr); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNativeSql"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		if (_tcscmp(szSqlStrOut,szSqlStrIn[1]) == 0)
		{
			LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"), szSqlStrIn[1], szSqlStrOut);
		}	
		else
		{
			TEST_FAILED;	
			LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"), szSqlStrIn[1], szSqlStrOut);
		}
		TESTCASE_END;

		//==================================================================================================
		TESTCASE_BEGIN("Test the positive functionality of SQLNativeSql with max length same as string length\n");
		returncode = SQLNativeSql((SQLHANDLE)hdbc, (SQLTCHAR*)szSqlStrIn[2], _tcslen(szSqlStrIn[2]), (SQLTCHAR*)szSqlStrOut, _tcslen(szSqlStrIn[2])+1, &pcbSqlStr); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNativeSql"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		if (_tcscmp(szSqlStrOut,szSqlStrIn[2]) == 0)
		{
			LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"), szSqlStrIn[2], szSqlStrOut);
		}	
		else
		{
			TEST_FAILED;	
			LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"), szSqlStrIn[2], szSqlStrOut);
		}
		TESTCASE_END;
	}
//==================================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLNativeSql.\n"));
	free_list(var_list);
	TEST_RETURN;
}
