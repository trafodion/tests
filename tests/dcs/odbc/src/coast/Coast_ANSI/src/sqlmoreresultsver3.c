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

#include <stdio.h>
#include <windows.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

/*
---------------------------------------------------------
   TestSQLMoreResultsVer3
---------------------------------------------------------
*/
PassFail TestSQLMoreResultsVer3(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	char		Heading[MAX_STRING_SIZE];
	RETCODE		returncode;
	SQLHANDLE 	henv;
	SQLHANDLE 	hdbc;
	SQLHANDLE	hstmt;
	CHAR		*SetupStr[] = {"--","--","--","--","--","--","--","endloop"};
	CHAR		*TestStr[] = {"--","--","--","--","--","endloop"};
	int			cnt, fail = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLMoreResults30", charset_file);
	if (var_list == NULL) return FAILED;

	SetupStr[0] = var_mapping("SQLMoreResults30_SetupStr_0", var_list);
	SetupStr[1] = var_mapping("SQLMoreResults30_SetupStr_1", var_list);
	SetupStr[2] = var_mapping("SQLMoreResults30_SetupStr_2", var_list);
	SetupStr[3] = var_mapping("SQLMoreResults30_SetupStr_3", var_list);
	SetupStr[4] = var_mapping("SQLMoreResults30_SetupStr_4", var_list);
	SetupStr[5] = var_mapping("SQLMoreResults30_SetupStr_5", var_list);
	SetupStr[6] = var_mapping("SQLMoreResults30_SetupStr_6", var_list);

	TestStr[0] = var_mapping("SQLMoreResults30_TestStr_0", var_list);
	TestStr[1] = var_mapping("SQLMoreResults30_TestStr_1", var_list);
	TestStr[2] = var_mapping("SQLMoreResults30_TestStr_2", var_list);
	TestStr[3] = var_mapping("SQLMoreResults30_TestStr_3", var_list);
	TestStr[4] = var_mapping("SQLMoreResults30_TestStr_4", var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLMoreResults | SQLMoreResults30 | sqlmoreresultsver3.c\n");
	
	TEST_INIT;
	
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))	
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
	hdbc = pTestInfo->hdbc;
	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
	if (returncode == SQL_SUCCESS)
	{
		cnt = 0;
		while (_stricmp(SetupStr[cnt],"endloop") != 0)
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*) SetupStr[cnt],SQL_NTS);
			if (returncode == SQL_ERROR)
				fail++;
			cnt++;
		}
		if (fail != cnt)
		{
			cnt = 0;
			while (_stricmp(TestStr[cnt],"endloop") != 0)
			{
				sprintf(Heading,"Positive Test SQLMoreResults for ");
				strcat(Heading,TestStr[cnt]);
				strcat(Heading,"\n");
				TESTCASE_BEGIN(Heading);
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)TestStr[cnt],SQL_NTS);
				if (returncode == SQL_SUCCESS)
				{
					SQLFetch(hstmt);
					returncode=SQLMoreResults(hstmt);
					if(!CHECKRC(SQL_NO_DATA_FOUND,returncode,"SQLMoreResults"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
				}
				TESTCASE_END;
				cnt++;
			}
			SQLExecDirect(hstmt,(SQLCHAR*)SetupStr[0],SQL_NTS); // CLEANUP 
			SQLExecDirect(hstmt,(SQLCHAR*)SetupStr[1],SQL_NTS); // CLEANUP 
		}
	}

//==============================================================================*/

	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLMoreResults.\n");
	free_list(var_list);
	TEST_RETURN;
}
