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

#define DRVC_LEN 100
#define	NUM_PERFORM	30
#define	MAX_NUM_LOOP 4

//=========================================================//
//                                                         //
//                    TEST MX RESOURCE GOVERNING           //
//                                                         //
//=========================================================//

PassFail TestMXResourceGovern(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
 	//TCHAR		Heading[MAX_STRING_SIZE];	Never Used
  RETCODE	returncode;
	//HWND		Myhwnd;						Never Used
 	SQLHANDLE 	henv1;
 	SQLHANDLE 	hdbc1;
	SQLHANDLE	hstmt1;
	TCHAR		DataSource[50];
	int			i = 0;
	TCHAR		*StmtStr,	*tablename;

//======================================================================================================

 	LogMsg(SHORTTIMESTAMP+LINEBEFORE,_T("Begin testing => Resource Governing.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for Resource Governing tests\n");
	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	henv1 = pTestInfo->henv;
 	hdbc1 = pTestInfo->hdbc;
 	hstmt1 = (SQLHANDLE)pTestInfo->hstmt;
	_tcscpy(DataSource,_T(""));
	_tcscat(DataSource,pTestInfo->DataSource);
	returncode = SQLAllocStmt((SQLHANDLE)hdbc1, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv1,hdbc1,hstmt1);
		TEST_FAILED;
		TEST_RETURN;
	}
	StmtStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	tablename = (TCHAR *)malloc(MAX_TABLE_NAME);

	//CREATE
	_stprintf(tablename,_T("testresgovern"));
	SQLExecDirect(hstmt1,StmtQueries(DROP_TABLE,tablename,StmtStr),SQL_NTS);
	returncode = SQLExecDirect(hstmt1,StmtQueries(CREATE_TABLE,tablename,StmtStr),SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv1,hdbc1,hstmt1);
		SQLFreeStmt(hstmt1,SQL_DROP);
		free(StmtStr);
		free(tablename);
		TEST_RETURN;
	}
	//INSERT
	for (i = 0; i < 200; i++) // insert loop
	{
		returncode = SQLExecDirect(hstmt1,StmtQueries(INSERT_TABLE,tablename,StmtStr),SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv1,hdbc1,hstmt1);
			SQLFreeStmt(hstmt1,SQL_DROP);
			free(StmtStr);
			free(tablename);
			TEST_RETURN;
		}
	}
	TESTCASE_END;		// End setup

	SQLExecDirect(hstmt1,StmtQueries(DROP_TABLE,tablename,StmtStr),SQL_NTS);
	SQLFreeStmt(hstmt1,SQL_DROP);
	free(StmtStr);
	free(tablename);
	FullDisconnect(pTestInfo); 

//======================================================================================================

 	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => Resource Governing.\n"));
  TEST_RETURN;

}
