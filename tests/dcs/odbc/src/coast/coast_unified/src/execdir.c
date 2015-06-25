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
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

//---------------------------------------------------------
//   TestSQLExecDirect()
//---------------------------------------------------------
PassFail TestSQLExecDirect(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	TCHAR			Heading[MAX_STRING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	TCHAR			*ExecDirStr[10];
/*							= {
							"drop table testexecdir",
							"create table testexecdir(c1 char(10),c2 varchar(10),c3 decimal(10,5),c4 smallint,c5 integer,c6 real,c7 date,c8 time,c9 timestamp) NO PARTITION",
							"create table testexecdir(c1 char(10),c2 varchar(10) NO PARTITION",
							"drop table testexecdir1",
							"drop table testexecdir2",
							"create table testexecdir1(c1 int,c2 varchar(10)) NO PARTITION",
							"create table testexecdir2(c1 int,c2 varchar(10)) NO PARTITION",
							"insert into testexecdir1 values (1,'\"row1\"')",
							"insert into testexecdir1 values (2,'\"row2\"')",
							"insert into testexecdir2 select * from testexecdir1 order by c1"};
*/
//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLExecDirect"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecDirStr[0] = var_mapping(_T("SQLExecDirect_ExecDirStr_0"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLExecDirect_ExecDirStr_1"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLExecDirect_ExecDirStr_2"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLExecDirect_ExecDirStr_3"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLExecDirect_ExecDirStr_4"), var_list);
	ExecDirStr[5] = var_mapping(_T("SQLExecDirect_ExecDirStr_5"), var_list);
	ExecDirStr[6] = var_mapping(_T("SQLExecDirect_ExecDirStr_6"), var_list);
	ExecDirStr[7] = var_mapping(_T("SQLExecDirect_ExecDirStr_7"), var_list);
	ExecDirStr[8] = var_mapping(_T("SQLExecDirect_ExecDirStr_8"), var_list);
	ExecDirStr[9] = var_mapping(_T("SQLExecDirect_ExecDirStr_9"), var_list);
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLExecDirect.\n"));
	
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
	if((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	{
		DisplaySqlErr(hdbc, SQL_HANDLE_DBC);
	}
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	
	_stprintf(Heading,_T("Test Positive Functionality of SQLExecDirect\n"));
	TESTCASE_BEGINW(Heading);
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],_tcslen(ExecDirStr[1]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	TESTCASE_END;

	_stprintf(Heading,_T("Test Positive Functionality of SQLExecDirect with SQL_NTS\n"));
	TESTCASE_BEGINW(Heading);
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	TESTCASE_END;

	_stprintf(Heading,_T("Test negative Functionality of SQLExecDirect with _tcslen less than sqlstr\n"));
	TESTCASE_BEGINW(Heading);
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	//returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],_tcslen(ExecDirStr[1]));
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],(_tcslen(ExecDirStr[1])-5));
	if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* Clean up */
	TESTCASE_END;

	_stprintf(Heading,_T("Test negative Functionality of SQLExecDirect with invalid sqlstr\n"));
	TESTCASE_BEGINW(Heading);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2],_tcslen(ExecDirStr[2]));
	if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	_stprintf(Heading,_T("Test negative Functionality of SQLExecDirect with invalid handle\n"));
	TESTCASE_BEGINW(Heading);
	returncode = SQLExecDirect((SQLHANDLE)NULL,(SQLTCHAR*)ExecDirStr[2],_tcslen(ExecDirStr[2]));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	_stprintf(Heading,_T("Test +ve Func of SQLExecDirect for insert into...select * from..order by statement (Soln 10-990723-2800)\n"));
	TESTCASE_BEGINW(Heading);
	
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3],_tcslen(ExecDirStr[3])); /* Clean up */
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[4],_tcslen(ExecDirStr[4])); /* Clean up */
	
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[5],_tcslen(ExecDirStr[5]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[6],_tcslen(ExecDirStr[6]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[7],_tcslen(ExecDirStr[7]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[8],_tcslen(ExecDirStr[8]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[9],_tcslen(ExecDirStr[9]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}

	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3],_tcslen(ExecDirStr[3])); /* Clean up */
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[4],_tcslen(ExecDirStr[4])); /* Clean up */
	
	TESTCASE_END;


	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLExecDirect.\n"));

	free_list(var_list);

	TEST_RETURN;
}
