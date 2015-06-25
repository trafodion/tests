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
   TestSQLEndTran
---------------------------------------------------------
*/
PassFail TestMXSQLEndTran(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	char			Heading[MAX_STRING_SIZE];
	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			*ExecDirStr[] = 
							{
								//"create table testtransact(c1 char(20),c2 integer)",
								//"create table testtransact(c1 char(20),c2 integer) NO PARTITION",
                                // The  NO PARTITION is to help speed up this test on TRAFODION/clustered systems with POS turned on.
								"--",
								"--",
								"--",
								"--",
								"--",
								"--"
							};
	UWORD			fType[] = { SQL_ROLLBACK, SQL_COMMIT };
	CHAR			*TypeDesc[] = { "SQL_ROLLBACK", "SQL_COMMIT" };
	CHAR			*Output;
	SQLLEN			OutputLen; 
	struct
	{
		SWORD	ExeRes[2];
		SWORD	FetchRes[2];
		CHAR	*DataRes[2];
	} CheckRes[] =	{
						{SQL_ERROR,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND,"",""},
						{SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_SUCCESS,"","--"},
						{SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,"--","--"},
						{SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND,"--",""},
						{SQL_SUCCESS,SQL_ERROR,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND,"",""}
					};
	int	i = 0, j = 0, iend = 5, jend = 1, commit_on_off = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLEndTran", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping("SQLEndTran_ExecDirStr_0", var_list);
	ExecDirStr[1] = var_mapping("SQLEndTran_ExecDirStr_1", var_list);
	ExecDirStr[2] = var_mapping("SQLEndTran_ExecDirStr_2", var_list);
	ExecDirStr[3] = var_mapping("SQLEndTran_ExecDirStr_3", var_list);
	ExecDirStr[4] = var_mapping("SQLEndTran_ExecDirStr_4", var_list);
	ExecDirStr[5] = var_mapping("SQLEndTran_ExecDirStr_5", var_list);

	CheckRes[1].DataRes[1] = var_mapping("SQLEndTran_Insert", var_list);
	CheckRes[2].DataRes[0] = var_mapping("SQLEndTran_Insert", var_list);
	CheckRes[2].DataRes[1] = var_mapping("SQLEndTran_Update", var_list);
	CheckRes[3].DataRes[0] = var_mapping("SQLEndTran_Update", var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLEndTran | SQLEndTran | endtran.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Initializing SQLEndTran test environment\n");
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
	//setting CQD to set POS OFF,as some tests fail otherwise. (to be fixed)
	//SQLExecDirect (hstmt,"CONTROL QUERY DEFAULT POS 'OFF'",SQL_NTS);

	for (commit_on_off = 0; commit_on_off < 10; commit_on_off++)
	{
		//LogMsg(NONE,">Loop commit_on_off=%d\n",commit_on_off);
		returncode = SQLSetConnectAttr((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,(void *)SQL_AUTOCOMMIT_ON,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
		for (i = 0; i <= (iend-1); i++)
		{
			sprintf(Heading,"Test Positive Functionality of SQLEndTran while Autocommit is ON and executing\n");
			strcat(Heading, ExecDirStr[i]);
			strcat(Heading, "\n");
			TESTCASE_BEGIN(Heading);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TEST_FAILED;
			}
		}
		SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
		returncode = SQLSetConnectAttr((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,(void *)SQL_AUTOCOMMIT_OFF,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		
		for (i = 0; i <= (iend-1); i++)
		{
			//LogMsg(NONE,">>Loop iend=%d\n",i);
			for (j = 0; j <= jend; j++)
			{
				//LogMsg(NONE,">>>Loop jend=%d\n",j);
				sprintf(Heading,"Test Positive Functionality of SQLEndTran while Autocommit is OFF and executing\n");
				strcat(Heading, ExecDirStr[i]);
				strcat(Heading, " & ");
				strcat(Heading, TypeDesc[j]);
				strcat(Heading, "\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					returncode=SQLEndTran(SQL_HANDLE_DBC,(SQLHANDLE)hdbc,fType[j]);
					//if(i==4) Sleep(20);																// tmf rollback is slower.
					Sleep(2);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTransact"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
					}

					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[iend],SQL_NTS);
					//LogMsg(NONE,"String to be executed: %s\n", ExecDirStr[iend]);
					if(!CHECKRC(CheckRes[i].ExeRes[j],returncode,"SQLExecDirect"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
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
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
							}
							else
							{
								returncode = SQLFetch(hstmt);
								if(!CHECKRC(CheckRes[i].FetchRes[j],returncode,"SQLFetch"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									if (returncode != SQL_NO_DATA_FOUND && returncode != SQL_ERROR)
									{
										if (strcspn(CheckRes[i].DataRes[j],Output) == 0)
										{
											//LogMsg(NONE,"expect: %s and actual: %s are matched\n",Output,CheckRes[i].DataRes[j]);
										}	
										else
										{
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d \n",Output,CheckRes[i].DataRes[j],__LINE__);
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
			//SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
			}/* end i loop */
		//SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
		}/* end j loop */
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
	returncode=SQLEndTran(SQL_HANDLE_DBC,(SQLHANDLE)hdbc,SQL_ROLLBACK);
	Sleep(2);	

	returncode=FullDisconnect3(pTestInfo);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFullDisconnect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
	}

	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLEndTran.\n");
	free_list(var_list);
	TEST_RETURN;
}