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
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	SQL_MAX_MESSAGE_LEN 300

/*
---------------------------------------------------------
   TestSQLGetDiagRec 
---------------------------------------------------------
*/
PassFail TestMXSQLGetDiagRec(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	SQLCHAR			SqlState[STATE_SIZE];
	SQLINTEGER		NativeError;
	SQLCHAR			ErrorMsg[MAX_STRING_SIZE];
	SQLSMALLINT		ErrorMsglen;
	CHAR			*ExecDirStr[4];

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLGetDiagRec", charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecDirStr[0] = var_mapping("SQLGetDiagRec_ExecDirStr_1", var_list);
	ExecDirStr[1] = var_mapping("SQLGetDiagRec_ExecDirStr_2", var_list);
	ExecDirStr[2] = var_mapping("SQLGetDiagRec_ExecDirStr_3", var_list);
	ExecDirStr[3] = var_mapping("SQLGetDiagRec_ExecDirStr_4", var_list);
//=================================================================================================

 LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLGetDiagRec | SQLGetDiagRec | diagrec.c\n");
	
 TEST_INIT;

 if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
 {
	LogMsg(NONE,"Unable to connect\n");
	TEST_FAILED;
	TEST_RETURN;
 }

 henv = pTestInfo->henv;
 hdbc = pTestInfo->hdbc;
 hstmt = (SQLHANDLE)pTestInfo->hstmt;

 returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
 {
 	LogAllErrorsVer3(henv,hdbc,hstmt);
	FullDisconnect(pTestInfo);
	TEST_FAILED;
	TEST_RETURN;
 }
 
 TESTCASE_BEGIN("Test syntax while creating a table SQLError\n");
 returncode = SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)ExecDirStr[0],SQL_NTS);
 if (returncode == SQL_ERROR)
 {
	returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,1, SqlState, &NativeError, ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
	{
		TEST_FAILED;
		LogAllErrorsVer3(henv,hdbc,hstmt);
	}
	else
	{
		LogMsg(NONE,"SqlState: %s and ErrorMsg: %s\n",SqlState,ErrorMsg);
		TESTCASE_END;
	}
 }

 TESTCASE_BEGIN("Test syntax while inserting a table SQLError\n");
 SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)ExecDirStr[3],SQL_NTS);//clean
 returncode = SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)ExecDirStr[1],SQL_NTS);
 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
 {
 	TEST_FAILED;
	LogAllErrorsVer3(henv,hdbc,hstmt);
 }

 returncode = SQLExecDirect(hstmt,(SQLCHAR*)(SQLCHAR *)ExecDirStr[2],SQL_NTS);
 if (returncode == SQL_ERROR)
 {
	returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,1, SqlState, &NativeError, ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
	{
		TEST_FAILED;
		LogAllErrorsVer3(henv,hdbc,hstmt);
	}
	else
	{
		LogMsg(NONE,"SqlState: %s and ErrorMsg: %s\n",SqlState,ErrorMsg);
#ifndef _WM
		if(strcmp((char*)SqlState,"22001"))
			TEST_FAILED;
#else
		if(strcmp((char*)SqlState,"22003"))
			TEST_FAILED;
#endif
		TESTCASE_END;
	}
 }
 else {
	LogMsg(ERRMSG,"Expect: SQL_ERROR and Actual: %d, line=%d\n",returncode, __LINE__);
	TEST_FAILED;
	TESTCASE_END;
 }

 SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)ExecDirStr[3],SQL_NTS); // Cleanup
 SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
 
 LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLGetDiagRec.\n");
 
 FullDisconnect3(pTestInfo);
 free_list(var_list);
 TEST_RETURN;
}
