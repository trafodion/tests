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
#include <windows.h>
#include <sqlext.h>
#include <stdio.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define T_SQLConnect				0
#define T_SQLDriverConnect			1
#define	OUT_CONN_STR				1024
/*---------------------------------------------------------
		TestSQLConnect
---------------------------------------------------------*/
PassFail TestSQLConnect(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv = (SQLHANDLE)NULL, henv1[NUM_ENV_HND];
	SQLHANDLE 		hdbc = (SQLHANDLE)NULL, hdbc1[NUM_ENV_HND * NUM_CONN_HND], badhdbc;
	SQLHANDLE		hstmt = (SQLHANDLE)NULL;
	TCHAR			*tempstr = _T("baddsn");
	int				i = 0, j = 0;
	TCHAR			*StmtHndlStr;
//	TCHAR			buffer[SQL_MAX_USER_NAME_LEN*3+2];
//	TCHAR			connstr[OUT_CONN_STR];
//	SQLTCHAR			OutConnStr[OUT_CONN_STR];
//	SQLSMALLINT		OutConn_tcslen;

	TCHAR		  *unUsedUserID[] = {_T("--"), _T("--"), _T("--"), _T("--"), _T("--") };
	TCHAR		  *invalidPWD[] =  {_T("--"), _T("--"), _T("--"), _T("--"), _T("--") };
	TCHAR		  *tabName = _T("--");

	struct testCases {
		RETCODE ret1;
		RETCODE ret2;
		TCHAR* newpwd;
		TCHAR* newpwdvalidation;
	} testMatrix[] = {
		//Positive tests
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("a"), _T("a")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("a1"), _T("a1")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("abcde12"), _T("abcde12")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("1234abcd"), _T("1234abcd")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("aaaa1111"), _T("aaaa1111")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("abcd12345"), _T("abcd12345")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("abc123456789012345678901234567890123456789012345678901234567890"), _T("abc123456789012345678901234567890123456789012345678901234567890")},
		{SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, _T("abcd123456789012345678901234567890123456789012345678901234567890"), _T("abcd123456789012345678901234567890123456789012345678901234567890")},

		//Negative tests
		{SQL_ERROR, SQL_ERROR, _T(""), _T("")},
		{SQL_ERROR, SQL_ERROR, _T(" "), _T(" ")},
		{SQL_ERROR, SQL_ERROR, _T("abcd"), _T("abc")},
		{SQL_ERROR, SQL_ERROR, _T("abc"), _T("abcd")},
		{SQL_ERROR, SQL_ERROR, _T("abc,d"), _T("abc,d")},
		{SQL_ERROR, SQL_ERROR, _T(","), _T(",")},
		{SQL_ERROR, SQL_ERROR, _T("a b"), _T("a b")},
		{SQL_ERROR, SQL_ERROR, _T(" cd e "), _T(" cd e ")},
		{SQL_ERROR, SQL_ERROR, _T("abcde123456789012345678901234567890123456789012345678901234567890"), _T("abcde123456789012345678901234567890123456789012345678901234567890")},
		{SQL_ERROR, SQL_ERROR, _T("abc 123456789012345678901234567890123456789012345678901234567890"), _T("abc 123456789012345678901234567890123456789012345678901234567890")},
		{SQL_ERROR, SQL_ERROR, _T("abcde123456789012345678901234567890123456789012345678901234567890"), _T("abcd123456789012345678901234567890123456789012345678901234567890")},
		{9999,}
	};
	
//==========================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLConnect"), charset_file);
	if (var_list == NULL) return FAILED;

	unUsedUserID[0] = var_mapping(_T("SQLConnect_unUsedUserID_0"), var_list);
	unUsedUserID[1] = var_mapping(_T("SQLConnect_unUsedUserID_1"), var_list);
	unUsedUserID[2] = var_mapping(_T("SQLConnect_unUsedUserID_2"), var_list);
	unUsedUserID[3] = var_mapping(_T("SQLConnect_unUsedUserID_3"), var_list);
	unUsedUserID[4] = var_mapping(_T("SQLConnect_unUsedUserID_4"), var_list);

	invalidPWD[0] = var_mapping(_T("SQLConnect_invalidPWD_0"), var_list);
	invalidPWD[1] = var_mapping(_T("SQLConnect_invalidPWD_1"), var_list);
	invalidPWD[2] = var_mapping(_T("SQLConnect_invalidPWD_2"), var_list);
	invalidPWD[3] = var_mapping(_T("SQLConnect_invalidPWD_3"), var_list);
	invalidPWD[4] = var_mapping(_T("SQLConnect_invalidPWD_4"), var_list);

	tabName = var_mapping(_T("SQLConnect_tabName"), var_list);

//==========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLConnect/SQLDisconnect.\n"));
  
	TEST_INIT;

	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: Invalid CONN handle pointer\n");
	badhdbc = (SQLHANDLE)NULL;
	returncode = SQLConnect(badhdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLConnect"))
	{
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)badhdbc,hstmt);
		TEST_FAILED;
	}
	SQLDisconnect(badhdbc);
	TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: NULL DSN\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLConnect(hdbc,NULL,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
    TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: Invalid DSN length\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,(SWORD)(_tcslen(pTestInfo->DataSource)/2),(SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),(SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password));
	if(!CHECKRC(SQL_ERROR,returncode,"SQLConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
	TESTCASE_END;

//==========================================================================================
  
	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: Invalid DSN\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLConnect(hdbc,(SQLTCHAR*)tempstr,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLConnect with SQL_NTS\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
  TESTCASE_END;

//==========================================================================================
  
	TESTCASE_BEGIN("Test Positive Functionality of SQLConnect with _tcslen\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),(SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),(SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
		TEST_FAILED;
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
	TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLConnect, SQLDisconnect then SQLConnect.\n");
	StmtHndlStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	for (i = 0; i < 3; i++)
	{
		returncode = SQLAllocEnv(&henv);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
		{
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
		{
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
		{
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
			TEST_FAILED;
		}
		switch (i)
		{
			case 0:
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
					TEST_FAILED;
				}
				returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
					TEST_FAILED;
				}
				returncode = SQLAllocStmt(hdbc, &hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				/* long table name
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,"testconnect",StmtHndlStr),SQL_NTS);
				*/
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,tabName,StmtHndlStr),SQL_NTS);

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}			
//				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				break;
			case 1:
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLFreeConnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
				{
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLAllocStmt(hdbc, &hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
/*				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,"testconnect",StmtHndlStr),SQL_NTS);
*/
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,tabName,StmtHndlStr),SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}			
//				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				break;
			case 2:
				if (hstmt != (SQLHANDLE)NULL) {
					returncode = SQLFreeStmt(hstmt, SQL_DROP);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
					{
						TEST_FAILED;
						LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
					}
				}
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLFreeConnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLFreeEnv(henv);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLAllocEnv(&henv);                 /* Environment handle */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
				{
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
				{
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
				returncode = SQLAllocStmt(hdbc, &hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}
/*				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,"testconnect",StmtHndlStr),SQL_NTS);
*/
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(CREATE_TABLE,tabName,StmtHndlStr),SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				}			
//				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,"testconnect",StmtHndlStr),SQL_NTS); 
				SQLExecDirect(hstmt,(SQLTCHAR*)StmtQueries(DROP_TABLE,tabName,StmtHndlStr),SQL_NTS); 
				break;
			default:
				// End
				break;
		}
		SQLFreeStmt(hstmt,SQL_DROP);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);

		// RS [1/22/05] need to cleanup handles or the function logic gets a memory error when testing a freed handle
		hstmt = (SQLHANDLE)NULL;
		hdbc =  (SQLHANDLE)NULL;
		henv =  (SQLHANDLE)NULL;

	}
	free(StmtHndlStr);
  TESTCASE_END;

//==========================================================================================
  
	TESTCASE_BEGIN("Test Positive Functionality of SQLConnect with different connection handles\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	for (i = 0; i < NUM_CONN_HND; i++){
		returncode = SQLAllocConnect(henv, &hdbc1[i]);    /* Connection handle  */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc1[i],hstmt);
			TEST_FAILED;
			TEST_RETURN;
			}
		returncode = SQLConnect(hdbc1[i],(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect")){
			TEST_FAILED;
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc1[i],hstmt);
			}
		}
	for (i = 0; i < NUM_CONN_HND; i++){
		SQLDisconnect(hdbc1[i]);
		SQLFreeConnect(hdbc1[i]);
		}
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLConnect with different env & conn handles\n");
	for (j = 0; j < NUM_ENV_HND / 5; j++)
	{
		returncode = SQLAllocEnv(&henv1[j]);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
		{
			TEST_FAILED;
			TEST_RETURN;
		}
		for (i = 0; i < NUM_CONN_HND / 2; i++)
		{
			returncode = SQLAllocConnect(henv1[j], &hdbc1[j * NUM_CONN_HND + i]);    /* Connection handle  */
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
			{
				LogAllErrors((SQLHANDLE)henv1[j],(SQLHANDLE)hdbc1[j * NUM_CONN_HND + i],hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLConnect(hdbc1[j * NUM_CONN_HND + i],(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
			{
				TEST_FAILED;
				LogAllErrors((SQLHANDLE)henv1[j],(SQLHANDLE)hdbc1[j * NUM_CONN_HND + i],hstmt);
			}
		}
	}
	for (j = 0; j < NUM_ENV_HND / 5; j++)
	{
		for (i = 0; i < NUM_CONN_HND / 2; i++)
		{
			SQLDisconnect(hdbc1[j * NUM_CONN_HND + i]);
			SQLFreeConnect(hdbc1[j * NUM_CONN_HND + i]);
		}
		SQLFreeEnv(henv1[j]);
	}
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: Invalid userid\n");
	for (i = 0; i < (int)(sizeof(unUsedUserID)/sizeof(TCHAR*)); i++)
	{
		LogMsg(NONE,_T("Connect with userid=\"%s\"\n"), unUsedUserID[i]);
		returncode = SQLAllocEnv(&henv);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
			TEST_FAILED;
			TEST_RETURN;
			}
		returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
			}
		returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,
									(SQLTCHAR*)unUsedUserID[i],SQL_NTS,
									(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
		if(!CHECKRC(SQL_ERROR,returncode,"SQLConnect")){
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
			SQLDisconnect(hdbc);
			TEST_FAILED;
			}
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
	TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Negative Functionality of SQLConnect: Valid userid and invalid password\n");
	for (i = 0; i < (int)(sizeof(invalidPWD)/sizeof(TCHAR*)); i++)
	{
		LogMsg(NONE,_T("Connect with pwd=\"%s\"\n"), invalidPWD[i]);
		returncode = SQLAllocEnv(&henv);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
			TEST_FAILED;
			TEST_RETURN;
			}
		returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
			}
		if (_tcscmp(pTestInfo->Password, invalidPWD[i]) != 0) {
			returncode = SQLConnect(hdbc,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,
										(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,
										(SQLTCHAR*)invalidPWD[i],SQL_NTS);
			if(!CHECKRC(SQL_ERROR,returncode,"SQLConnect")){
				LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
				SQLDisconnect(hdbc);
				TEST_FAILED;
				}
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
	TESTCASE_END;

//==========================================================================================
	
	/*Test a valid userid*/
	//TESTCASE_BEGIN("Test positive and negative function of change password for an active userid, valid password\n");
	//j=0;
	//while (j<2) {
	//	if (j==0) {
	//		type = T_SQLConnect;
	//		LogMsg(NONE,_T("Test positive and negative function of change password for an active userid, using SQlConnect\n"));
	//	}
	//	else if (j==1) {
	//		type = T_SQLDriverConnect;
	//		LogMsg(NONE,_T("Test positive and negative function of change password for an active userid, using SQLDriverConnect\n"));
	//	}

	//	i = 0;
	//	while (testMatrix[i].ret1 != 9999) {
	//		Sleep(2000);
	//		/**************Check current pwd***************************/
	//		if (!SQL_SUCCEEDED((returncode = SQLAllocEnv(&pTestInfo->henv)))){
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		if (!SQL_SUCCEEDED((returncode = SQLSetEnvAttr(pTestInfo->henv, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0))))
	//		{
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		if (!SQL_SUCCEEDED((returncode = SQLAllocConnect( pTestInfo->henv, &pTestInfo->hdbc)))){
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		if (type == T_SQLConnect) {
	//			returncode = SQLConnect( pTestInfo->hdbc,
	//							(SQLTCHAR*)pTestInfo->DataSource, SQL_NTS, 
	//							(SQLTCHAR*)pTestInfo->UserID, SQL_NTS, 
	//							(SQLTCHAR*)pTestInfo->Password, SQL_NTS );
	//		}
	//		else {
	//			_stprintf(connstr, "DSN=%s;UID=%s;PWD=%s", pTestInfo->DataSource,	pTestInfo->UserID, pTestInfo->Password);
	//			returncode = SQLDriverConnect(pTestInfo->hdbc, NULL, (SQLTCHAR*)connstr, _tcslen(connstr),
	//									OutConnStr,	OUT_CONN_STR, &OutConn_tcslen, SQL_DRIVER_NOPROMPT );          
	//		}

	//		if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO) {
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		returncode = SQLDisconnect(hdbc);
	//		if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO) {
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		/*******************Change new pwd****************************/
	//		_stprintf(buffer, "%s,%s,%s", pTestInfo->Password, testMatrix[i].newpwd, testMatrix[i].newpwdvalidation);
	//		LogMsg(NONE,_T("Password String :'%s'\n"), buffer);

	//		if (type == T_SQLConnect) {
	//			returncode = SQLConnect( pTestInfo->hdbc,
	//							(SQLTCHAR*)pTestInfo->DataSource, SQL_NTS, 
	//							(SQLTCHAR*)pTestInfo->UserID, SQL_NTS, 
	//							(SQLTCHAR*)buffer, SQL_NTS );
	//		}
	//		else {
	//			TCHAR connstr[OUT_CONN_STR];
	//			_stprintf(connstr, "DSN=%s;UID=%s;PWD=%s", pTestInfo->DataSource,	pTestInfo->UserID, buffer);
	//			returncode = SQLDriverConnect(pTestInfo->hdbc, NULL, (SQLTCHAR*)connstr, _tcslen(connstr),
	//									OutConnStr,	OUT_CONN_STR, &OutConn_tcslen, SQL_DRIVER_NOPROMPT );          
	//		}

	//		if (returncode != testMatrix[i].ret1 && returncode != testMatrix[i].ret2) {
	//			LogMsg(ERRMSG, "Test failed! Expected: %d or %d, return: %d\n",testMatrix[i].ret1,testMatrix[i].ret2,returncode);
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		returncode = SQLDisconnect(hdbc);
	//		if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO) {
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		/*******************Recheck new valid pwd**************************/
	//		if (type == T_SQLConnect) {
	//			returncode = SQLConnect( pTestInfo->hdbc,
	//							(SQLTCHAR*)pTestInfo->DataSource, SQL_NTS, 
	//							(SQLTCHAR*)pTestInfo->UserID, SQL_NTS, 
	//							(SQLTCHAR*)testMatrix[i].newpwd, SQL_NTS );
	//		}
	//		else {
	//			TCHAR connstr[OUT_CONN_STR];
	//			_stprintf(connstr, "DSN=%s;UID=%s;PWD=%s", pTestInfo->DataSource,	pTestInfo->UserID, testMatrix[i].newpwd);
	//			returncode = SQLDriverConnect(pTestInfo->hdbc, NULL, (SQLTCHAR*)connstr, _tcslen(connstr),
	//									OutConnStr,	OUT_CONN_STR, &OutConn_tcslen, SQL_DRIVER_NOPROMPT );          
	//		}

	//		if (returncode != testMatrix[i].ret1 && returncode != testMatrix[i].ret2) {
	//			LogMsg(ERRMSG, "Test failed! Expected: %d or %d, return: %d\n",testMatrix[i].ret1,testMatrix[i].ret2,returncode);
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		returncode = SQLDisconnect(hdbc);
	//		if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO) {
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		/**************Change back to original password for later tests***************/
	//		_stprintf(buffer, "%s,%s,%s", testMatrix[i].newpwd, pTestInfo->Password, pTestInfo->Password);
	//		LogMsg(NONE,_T("Password String :'%s'\n"), buffer);

	//		if (type == T_SQLConnect) {
	//			returncode = SQLConnect( pTestInfo->hdbc,
	//							(SQLTCHAR*)pTestInfo->DataSource, SQL_NTS, 
	//							(SQLTCHAR*)pTestInfo->UserID, SQL_NTS, 
	//							(SQLTCHAR*)buffer, SQL_NTS );
	//		}
	//		else {
	//			_stprintf(connstr, "DSN=%s;UID=%s;PWD=%s", pTestInfo->DataSource,	pTestInfo->UserID, buffer);
	//			returncode = SQLDriverConnect(pTestInfo->hdbc, NULL, (SQLTCHAR*)connstr, _tcslen(connstr),
	//									OutConnStr,	OUT_CONN_STR, &OutConn_tcslen, SQL_DRIVER_NOPROMPT );          
	//		}

	//		if (returncode != testMatrix[i].ret1 && returncode != testMatrix[i].ret2) {
	//			LogMsg(ERRMSG, "Test failed! Expected: %d or %d, return: %d\n",testMatrix[i].ret1,testMatrix[i].ret2,returncode);
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		returncode = SQLDisconnect(hdbc);
	//		if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO) {
	//			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,hstmt);
	//			TEST_FAILED;
	//			TEST_RETURN;
	//		}

	//		SQLFreeConnect(hdbc);
	//		SQLFreeEnv(henv);

	//		i++;
	//	}

	//	j++;
	//}//End while

	//TESTCASE_END;

/*===================================================================================================*/
	
   LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,_T("End of testing API ===> SQLConnect/SQLDisconnect.\n"));  
   free_list(var_list);
   TEST_RETURN;
}

