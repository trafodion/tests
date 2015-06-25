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
#include <stdlib.h>
#include <windows.h>
//#include <winbase.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	NAME_LEN		300

/*
---------------------------------------------------------
   TestSQLCloseCursor
---------------------------------------------------------
*/
PassFail TestMXSQLCloseCursor(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
//  TCHAR			Heading[MAX_STRING_SIZE];
	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	TCHAR	*DrpTab1;
	TCHAR	*CrtTab1;
	TCHAR	*InsTab1;
	TCHAR	*SelTab1;
	TCHAR	*UpdTab1;
	TCHAR	*DelTab1;
	TCHAR	*Update;

	TCHAR	*Output;
	SQLLEN	OutputLen; 

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLCloseCursor"), charset_file);
	if (var_list == NULL) return FAILED;

	Update = var_mapping(_T("SQLCloseCursor_Update"), var_list);
	DrpTab1 = var_mapping(_T("SQLCloseCursor_Drptab1"), var_list);
	CrtTab1 = var_mapping(_T("SQLCloseCursor_CrtTab1"), var_list);
	InsTab1 = var_mapping(_T("SQLCloseCursor_InsTab1"), var_list);
	SelTab1 = var_mapping(_T("SQLCloseCursor_SelTab1"), var_list);
	UpdTab1 = var_mapping(_T("SQLCloseCursor_UpdTab1"), var_list);
	DelTab1 = var_mapping(_T("SQLCloseCursor_DelTab1"), var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLCloseCursor.\n"));
	TEST_INIT;

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	TESTCASE_BEGIN("Testing SQLCloseCursor with invalid handle\n");
	hstmt = (SQLHANDLE)NULL;
	returncode = SQLCloseCursor(hstmt);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLCloseCursor"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	TESTCASE_END;


	TESTCASE_BEGIN("Testing SQLCloseCursor Positive Functionality\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	returncode = SQLSetConnectAttr((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,(void *)SQL_AUTOCOMMIT_ON,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
	{
		 LogAllErrorsVer3(henv,hdbc,hstmt);
		 FullDisconnect(pTestInfo);
		 TEST_FAILED;
		 TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab1,SQL_NTS); /* CLEANUP */

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Creating table: %s\n"),CrtTab1);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab1,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Inserting into table: %s\n"),InsTab1);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab1,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Updating table: %s\n"),UpdTab1);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)UpdTab1,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	else
	{
		LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Select from table: %s\n"),SelTab1);
    	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab1,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
			LogAllErrorsVer3(henv,hdbc,hstmt);
		}
		else
		{
			if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
			{
				Output = (TCHAR *)malloc(NAME_LEN);
				returncode=SQLBindCol(hstmt,1,SQL_C_TCHAR,Output,NAME_LEN,&OutputLen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						if (returncode != SQL_NO_DATA_FOUND && returncode != SQL_ERROR)
						{
							if (_tcscspn(Update,Output) == 0)
							{
								LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),Output,Update);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),Output,Update);
							}
						}
					}
					free(Output);
				}
			}
		}
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTab1,SQL_NTS);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Nothing to worry we didn't close the cursor this error was expected\n"));
	LogAllErrorsVer3(henv,hdbc,hstmt);
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Now closing the cursor\n"));
	returncode = SQLCloseCursor(hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLCloseCursor"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	else
	{
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTab1,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrorsVer3(henv,hdbc,hstmt);
		}
	} 

	TESTCASE_END;

	TESTCASE_BEGIN("Testing SQLCloseCursor with cursor in invalid state\n");
	returncode = SQLCloseCursor(hstmt);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLCloseCursor"))
	{
		TEST_FAILED;
	}
	else
    {
		LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Nothing to worry cursor is in invalid state this error occured as expected\n"));
		LogAllErrorsVer3(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//========================================================================================================

	SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab1,SQL_NTS); /* CLEANUP */
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLCloseCursor.\n"));
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	TEST_RETURN;
}
