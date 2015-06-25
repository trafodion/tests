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

#define	NAME_LEN		300

/*
---------------------------------------------------------
   TestSQLTransact
---------------------------------------------------------
*/
PassFail TestSQLTransact(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	char			Heading[MAX_STRING_SIZE];
	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			*ExecDirStr[6];
	UWORD			fType[] = { SQL_ROLLBACK,SQL_COMMIT };
	CHAR			*TypeDesc[] = { "SQL_ROLLBACK","SQL_COMMIT" };
	CHAR			*Output;
	SQLLEN			OutputLen;
	struct
	{
		SWORD	ExeRes[2];
		SWORD	FetchRes[2];
		CHAR	*DataRes[2];
	} CheckRes[] =	
		{
			{SQL_ERROR,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND,"",""},
			{SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_SUCCESS,"","--"},
			{SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,"--","--"},
			{SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND,"--",""},
			{SQL_SUCCESS,SQL_ERROR,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND,"",""}
		};
	int	i = 0, j = 0, iend = 5, jend = 1, commit_on_off = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLTransact", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping("SQLTransact_ExecDirStr_0", var_list);
	ExecDirStr[1] = var_mapping("SQLTransact_ExecDirStr_1", var_list);
	ExecDirStr[2] = var_mapping("SQLTransact_ExecDirStr_2", var_list);
	ExecDirStr[3] = var_mapping("SQLTransact_ExecDirStr_3", var_list);
	ExecDirStr[4] = var_mapping("SQLTransact_ExecDirStr_4", var_list);
	ExecDirStr[5] = var_mapping("SQLTransact_ExecDirStr_5", var_list);

	CheckRes[1].DataRes[1] = var_mapping("SQLTransact_Insert", var_list);
	CheckRes[2].DataRes[0] = var_mapping("SQLTransact_Insert", var_list);
	CheckRes[2].DataRes[1] = var_mapping("SQLTransact_Update", var_list);
	CheckRes[3].DataRes[0] = var_mapping("SQLTransact_Update", var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLTransact | SQLTransact | transact.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Initializing SQLTransact test environment\n");
//	
	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,"Unable to connect\n");
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
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	for (commit_on_off = 0; commit_on_off < 10; commit_on_off++)
	{
		returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
		for (i = 0; i <= (iend-1); i++)
		{
			sprintf(Heading,"Test Positive Functionality of SQLTransact while Autocommit is ON and executing\n");
			strcat(Heading, ExecDirStr[i]);
			strcat(Heading, "\n");
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
		}
		SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
		returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		
		for (i = 0; i <= (iend-1); i++)
		{
			for (j = 0; j <= jend; j++)
			{
				sprintf(Heading,"Test Positive Functionality of SQLTransact while Autocommit is OFF and executing\n");
				strcat(Heading, ExecDirStr[i]);
				strcat(Heading, " & ");
				strcat(Heading, TypeDesc[j]);
				strcat(Heading, "\n");
				TESTCASE_BEGIN(Heading);
				
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					returncode=SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,fType[j]);
					Sleep(2);																// tmf rollback is slower.
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTransact"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}

					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[iend],SQL_NTS);
					if(!CHECKRC(CheckRes[i].ExeRes[j],returncode,"SQLExecDirect"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					else
					{
						if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
						{
							Output = (char *)malloc(NAME_LEN);
							returncode=SQLBindCol(hstmt,1,SQL_C_CHAR,Output,NAME_LEN,&OutputLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
							{
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
							}
							else
							{
								returncode = SQLFetch(hstmt);
								if(!CHECKRC(CheckRes[i].FetchRes[j],returncode,"SQLFetch"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									if (returncode != SQL_NO_DATA_FOUND && returncode != SQL_ERROR)
									{
										if (strcspn(CheckRes[i].DataRes[j],Output) == 0)
										{
											LogMsg(NONE,"expect: %s and actual: %s are matched\n",Output,CheckRes[i].DataRes[j]);
										}	
										else
										{
											LogMsg(NONE,"expect: %s and actual: %s are not matched\n",Output,CheckRes[i].DataRes[j]);
											TEST_FAILED;	
										}
									}
								}
								free(Output);
								SQLFreeStmt(hstmt,SQL_CLOSE);
							}
						}
					}
				}
				TESTCASE_END;
			}/* end j loop */
		}/* end i loop */
	}

//========================================================================================================

	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
	returncode = SQLDisconnect((SQLHANDLE)hdbc);
    if(!CHECKRC(SQL_ERROR,returncode,"SQLDisconnect")) 
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;	
	}	
	
	// Free the open transactions.
	returncode=SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_ROLLBACK);
	Sleep(2);	

	returncode=FullDisconnect(pTestInfo);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFullDisconnect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
	}

	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLTransact.\n");

	free_list(var_list);

	TEST_RETURN;
}
