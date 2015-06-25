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
#include <time.h>
#include <sys/timeb.h>
#include <assert.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN		300
#define NUM_FETCH_LOOP	5
#define ROWS_INSERTED	50
#ifdef UNICODE
#define MAX_NUM1		26
#else
#define MAX_NUM1		25
#endif
PassFail TestMXSQLFetchScroll(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	int					i, j;
	TCHAR				*CCharOutput1[MAX_NUM1], CCharOutput2[NAME_LEN];
	SQLLEN				OutputLen1[MAX_NUM1], OutputLen2;
	SQLSMALLINT			CType[] = {SQL_C_TCHAR};
	//TCHAR					*TestCType[] = 
	//							{
	//								"SQL_C_TCHAR","SQL_C_BINARY","SQL_C_SSHORT","SQL_C_USHORT","SQL_C_SHORT","SQL_C_SLONG",
	//								"SQL_C_ULONG","SQL_C_FLOAT","SQL_C_DOUBLE","SQL_C_DATE","SQL_C_TIME","SQL_C_TIMESTAMP"
	//							};
	//
	//TCHAR					*TestSQLType[] = 
	//							{
	//								"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL",
	//								"SQL_FLOAT","SQL_DOUBLE","SQL_DATE","SQL_TIME","SQL_TIMESTAMP","SQL_BIGINT",
	//								"SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL",
	//								"SQL_LONGVARCHAR","SQL_WCHAR","SQL_WVARCHAR","SQL_WLONGVARCHAR"
	//							};
	TCHAR					*ExecDirStr[5];
	TCHAR					*CResults[] = 
								{
#ifndef _WM
									_T("--"),_T("--"),_T("1234.56789"),_T("1234.56789"),_T("1200"),_T("12000"),
									_T("12345.0"),_T("123450.0"),_T("1234500.0"),_T("1993-07-01"),_T("09:45:30"),
									_T("1993-08-02 08:44:31.001000"),_T("120000"),
									_T("1234567890123456789"),
									_T("1234567890123.456789"),
									_T("1234567890123456789012345678901234567890"),
									_T("0.12345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
									_T("1234567890.1234567890123456789012345678901234567890000000000000000000000000"),
									_T("12345.56789"),
									_T("1234567890123.56789"),
									_T("12345678901234567890.0123456789"),
									#ifdef UNICODE
									_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
									#else
									_T("--"),_T("--"),_T("--"),_T("--")
									#endif
#else
									_T("--"),_T("--"),_T("1234.56789"),_T("1234.56789"),_T("1200"),_T("12000"),
									_T("12345.0"),_T("123450.0"),_T("1234500.0"),_T("93/07/01"),_T("09:45:30"),
									_T("1993-08-02 08:44:31.001000"),_T("120000"),
									_T("1234567890123456789"),
									_T("1234567890123.456789"),
									_T("1234567890123456789012345678901234567890"),
									_T(".12345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
									_T("1234567890.1234567890123456789012345678901234567890000000000000000000000000"),
									_T("12345.56789"),
									_T("1234567890123.56789"),
									_T("12345678901234567890.0123456789"),
									_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
#endif
								};
	
	SQLSMALLINT	FetchOrientation[] = {SQL_FETCH_NEXT, SQL_FETCH_PRIOR, SQL_FETCH_FIRST, SQL_FETCH_LAST,
										SQL_FETCH_ABSOLUTE, SQL_FETCH_RELATIVE, SQL_FETCH_BOOKMARK, 999};

	TCHAR	*FetchOrientationText[] = {_T("SQL_FETCH_NEXT"), _T("SQL_FETCH_PRIOR"), _T("SQL_FETCH_FIRST"), _T("SQL_FETCH_LAST"),
										_T("SQL_FETCH_ABSOLUTE"), _T("SQL_FETCH_RELATIVE"), _T("SQL_FETCH_BOOKMARK")};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLFetchScroll"), charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping(_T("SQLFetchScroll_ExecDirStr_0"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLFetchScroll_ExecDirStr_1"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLFetchScroll_ExecDirStr_2"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLFetchScroll_ExecDirStr_3"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLFetchScroll_ExecDirStr_4"), var_list);

	CResults[0] = var_mapping(_T("SQLFetchScroll_CResults_1"), var_list);
	CResults[1] = var_mapping(_T("SQLFetchScroll_CResults_2"), var_list);

#ifdef UNICODE
	CResults[21] = var_mapping(_T("SQLFetchScroll_CResults_1"), var_list);
	CResults[22] = var_mapping(_T("SQLFetchScroll_CResults_2"), var_list);
	CResults[23] = var_mapping(_T("SQLFetchScroll_CResults_24"), var_list);
	CResults[24] = var_mapping(_T("SQLFetchScroll_CResults_25"), var_list);
	CResults[25] = var_mapping(_T("SQLFetchScroll_CResults_26"), var_list);
#else
	CResults[21] = var_mapping(_T("SQLFetchScroll_CResults_21"), var_list);
	CResults[22] = var_mapping(_T("SQLFetchScroll_CResults_22"), var_list);
	CResults[23] = var_mapping(_T("SQLFetchScroll_CResults_23"), var_list);
	CResults[24] = var_mapping(_T("SQLFetchScroll_CResults_24"), var_list);
#endif

//===========================================================================================================
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLFetchScroll.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLFetchScroll tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
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
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; // end of setup

	for (i = 0; i < 1; i++)
	{ // begin of 1st for loop 
		_stprintf(Heading,_T("Test 1.%d: Positive functionality of SQLFetchScroll by doing SQLBindcol\n"),i);
		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j=0; j<MAX_NUM1; j++)
		{
			CCharOutput1[j] = (TCHAR *)malloc(sizeof(TCHAR)*NAME_LEN);
			*(CCharOutput1[j])=(TCHAR)'\0';
			returncode = SQLBindCol(hstmt,(SWORD)(j+1),CType[i],CCharOutput1[j],NAME_LEN,&OutputLen1[j]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
				TEST_RETURN;
			}
		}

		returncode = SQLFetchScroll(hstmt, FetchOrientation[0], 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetchScroll"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			for (j=0; j<MAX_NUM1; j++)
			{
				if (_tcscmp(CCharOutput1[j],CResults[j]) == 0)
				{
					LogMsg(NONE,_T("expect: '%s' and actual: '%s' of column %d are matched\n"),CResults[j],CCharOutput1[j],j+1);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: '%s' and actual: '%s' of column %d are not match, at line %d\n"), CResults[j],CCharOutput1[j],j+1,__LINE__);
				}
				free(CCharOutput1[j]);
			} 
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		TESTCASE_END;
	} // end of 1st for loop 

//============================================================================================
 
	TESTCASE_BEGIN("Setup for more SQLFetchScroll tests\n");
	SQLFreeStmt(hstmt,SQL_DROP);
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[4],SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;

	for (i = 0; i < 1; i++)
	{
		_stprintf(Heading,_T("Test 2.%d: Positive functionality of SQLFetchScroll by doing SQLGetData\n"),i);
		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLFetchScroll(hstmt, FetchOrientation[0], 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetchScroll"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			for (j=0; j<MAX_NUM1; j++)
			{
				returncode = SQLGetData(hstmt,(SWORD)(j+1),CType[i],CCharOutput2,NAME_LEN,&OutputLen2);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}

				if (_tcscmp(CCharOutput2,CResults[j]) == 0)
				{
					LogMsg(NONE,_T("expect: '%s' and actual: '%s' of column %d are matched\n"), CResults[j],CCharOutput2,j+1);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: '%s' and actual: '%s' of column %d are not match, at line %d\n"),CResults[j],CCharOutput2,j+1,__LINE__);
				}
			}
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		TESTCASE_END;
	} 
 	
//============================================================================================

	TESTCASE_BEGIN("Setup for negative functionality of SQLFetchScroll \n");
	SQLFreeStmt(hstmt,SQL_DROP);
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[4],SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;

	i = 1;
	while (FetchOrientation[i] != 999)
	{
		_stprintf(Heading,_T("Test Negative functionality of SQLFetchScroll using %s\n"), FetchOrientationText[i]);
		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
				TEST_RETURN;
		}
		returncode = SQLFetchScroll(hstmt, FetchOrientation[i], 0);
		if(!CHECKRC(SQL_ERROR,returncode,"SQLFetchScroll"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		TESTCASE_END;
		i++;
	}
  
//=====================================================================================================
	
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); // cleanup  
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLFetchScroll.\n"));
	free_list(var_list);
	TEST_RETURN;
}
