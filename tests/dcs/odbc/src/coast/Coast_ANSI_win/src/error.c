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
	CHAR		SqlState[STATE_SIZE];
	SDWORD		NativeError;
	CHAR		ErrorMsg[MAX_STRING_SIZE];
	SWORD		ErrorMsglen;

	CHAR		*CrtTab = "--";

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLError", charset_file);
	if (var_list == NULL) return FAILED;

	CrtTab = var_mapping("SQLError_CrtTab", var_list);
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLError | SQLError | error.c\n");
	
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
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab,SQL_NTS);
	  if (returncode == SQL_ERROR)
		{
			returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)hdbc, hstmt, (SQLCHAR*)SqlState, &NativeError, (SQLCHAR*)ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,"SqlState: %s and ErrorMsg: %s\n",SqlState,ErrorMsg);
				TESTCASE_END;
			}
		}
	}
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLError.\n");
	free_list(var_list);
	TEST_RETURN;
}
