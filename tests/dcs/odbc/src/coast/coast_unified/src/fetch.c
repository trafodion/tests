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
#define MAX_NUM1		27
#else
#define MAX_NUM1		25
#endif

PassFail TestSQLFetch(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	SQLUSMALLINT		i, j, k, fn, h;
	SWORD				col;
	TCHAR				*CCharOutput1[MAX_NUM1], CCharOutput2[NAME_LEN];
	SQLLEN				OutputLen1[MAX_NUM1], OutputLen2;
	SQLSMALLINT			CType[] = {SQL_C_TCHAR};
	//TCHAR					*TestCType[] = 
	//							{
	//								"SQL_C_TCHAR","SQL_C_BINARY","SQL_C_SSHORT","SQL_C_USHORT","SQL_C_SHORT","SQL_C_SLONG",
	//								"SQL_C_ULONG","SQL_C_FLOAT","SQL_C_DOUBLE","SQL_C_DATE","SQL_C_TIME","SQL_C_TIMESTAMP"
	//							};
	//TCHAR					*TestSQLType[] = 
	//							{
	//								"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL",
	//								"SQL_FLOAT","SQL_DOUBLE","SQL_DATE","SQL_TIME","SQL_TIMESTAMP","SQL_BIGINT",
	//								"SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL","SQL_DECIMAL"
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
									_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
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

	TCHAR					*FetchNStr[5];

	struct 
	{
		SQLULEN	AccessParam[2];
		SQLULEN	TransactParam[2];
	} ConnOption = {
			SQL_MODE_READ_WRITE,
			SQL_MODE_READ_ONLY,
			SQL_TXN_READ_COMMITTED,
			SQL_TXN_READ_UNCOMMITTED
		};

	struct _timeb	fetchstarttime;
	struct _timeb fetchendtime;
	long		AccessTime[2];

	//Added for transaction isolation problems
	TCHAR *iso_level_cqd[] = {
		_T("control query default isolation_level 'READ_COMMITTED'"),
		_T("control query default isolation_level 'READ_UNCOMMITTED'"),
		_T("control query default isolation_level 'REPEATABLE_READ'"),
		_T("control query default isolation_level 'SERIALIZABLE'"),
		_T("endloop")
	};

	TCHAR *access_mode[] = {
		_T("default"),
		_T("set transaction READ ONLY"),
		_T("set transaction READ WRITE"),
		_T("endloop")
	};

	SQLTCHAR *sqlstring0 = (SQLTCHAR*)_T("DROP TABLE YRWK_TY_POS_2");
	SQLTCHAR *sqlstring1 = (SQLTCHAR*)_T("CREATE TABLE YRWK_TY_POS_2 ( C1 NUMERIC (9, 2) , C2 NUMERIC (9, 2)) NO PARTITION");
	SQLTCHAR *sqlstring2 = (SQLTCHAR*)_T("INSERT INTO YRWK_TY_POS_2 VALUES (119.28, 6)");
	SQLTCHAR *sqlstring3 = (SQLTCHAR*)_T("SELECT SUM(C1) + SUM(C2) FROM YRWK_TY_POS_2");
	//SQLTCHAR sqlstring0[] = _T("DROP TABLE YRWK_TY_POS_2");
	//SQLTCHAR sqlstring1[] = _T("CREATE TABLE YRWK_TY_POS_2 ( C1 NUMERIC (9, 2) , C2 NUMERIC (9, 2)) NO PARTITION");
	//SQLTCHAR sqlstring2[] = _T("INSERT INTO YRWK_TY_POS_2 VALUES (119.28, 6)");
	//SQLTCHAR sqlstring3[] = _T("SELECT SUM(C1) + SUM(C2) FROM YRWK_TY_POS_2");

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLFetch"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecDirStr[0] = var_mapping(_T("SQLFetch_ExecDirStr_1"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLFetch_ExecDirStr_2"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLFetch_ExecDirStr_3"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLFetch_ExecDirStr_4"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLFetch_ExecDirStr_5"), var_list);

	CResults[0] = var_mapping(_T("SQLFetch_CResults_1"), var_list);
	CResults[1] = var_mapping(_T("SQLFetch_CResults_2"), var_list);

#ifdef UNICODE	
	CResults[21] = var_mapping(_T("SQLFetch_datastr1"), var_list);
	CResults[22] = var_mapping(_T("SQLFetch_datastr2"), var_list);
	CResults[23] = var_mapping(_T("SQLFetch_datastr3"), var_list);

	CResults[24] = var_mapping(_T("SQLFetch_CResults_24"), var_list);
	CResults[25] = var_mapping(_T("SQLFetch_CResults_25"), var_list);
	CResults[26] = var_mapping(_T("SQLFetch_CResults_26"), var_list);
#else
	CResults[21] = var_mapping(_T("SQLFetch_CResults_21"), var_list);
	CResults[22] = var_mapping(_T("SQLFetch_CResults_22"), var_list);
	CResults[23] = var_mapping(_T("SQLFetch_CResults_23"), var_list);
	CResults[24] = var_mapping(_T("SQLFetch_CResults_24"), var_list);
#endif

	FetchNStr[0] = var_mapping(_T("SQLFetch_FetchNStr_1"), var_list);
	FetchNStr[1] = var_mapping(_T("SQLFetch_FetchNStr_2"), var_list);
	FetchNStr[2] = var_mapping(_T("SQLFetch_FetchNStr_3"), var_list);
	FetchNStr[3] = var_mapping(_T("SQLFetch_FetchNStr_4"), var_list);
	FetchNStr[4] = var_mapping(_T("SQLFetch_FetchNStr_5"), var_list);

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLFetch.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLFetch tests\n");

	if(!FullConnect(pTestInfo))
	{
		LogMsg(ERRMSG,_T("Unable to connect\n"));
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
		_stprintf(Heading,_T("Test 1.%d: Positive functionality of SQLFetch by doing SQLBindcol\n"),i);
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

		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
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

	TESTCASE_BEGIN("Setup for more SQLFetch tests\n");
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
		_stprintf(Heading,_T("Test 2.%d: Positive functionality of SQLFetch by doing SQLGetData\n"),i);
		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
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

	for (fn = 0; fn < NUM_FETCH_LOOP; fn++)
	{
		_stprintf(Heading,_T("Setup for Fetch %d tests\n"),(ROWS_INSERTED*(fn+1)));
		TESTCASE_BEGINW(Heading);
		SQLFreeStmt(hstmt,SQL_DROP);
		SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
		SQLExecDirect(hstmt,(SQLTCHAR*) FetchNStr[0],SQL_NTS); /* cleanup */
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)FetchNStr[1],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		for (i = 0; i < (ROWS_INSERTED*(fn+1)); i++)
		{ 
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)FetchNStr[2], SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
		TESTCASE_END; // end of setup

		_stprintf(Heading,_T("Test Positive functionality of Fetch %d by doing SQLBindcol\n"),(ROWS_INSERTED*(fn+1)));
		TESTCASE_BEGINW(Heading);
		for (k = 0; k < 2; k++)
		{
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,ConnOption.AccessParam[k]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnection Access"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
				TEST_RETURN;
			}
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,ConnOption.TransactParam[k]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnection Transact"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
				TEST_RETURN;
			}
			returncode = SQLSetStmtOption(hstmt,SQL_ROWSET_SIZE,1);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
				TEST_RETURN;
			}
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)FetchNStr[3], SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLNumResultCols(hstmt, &col);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			for (j = 0; j < col; j++)
			{
				CCharOutput1[j] = (TCHAR *)malloc(NAME_LEN);
				*(CCharOutput1[j])=(TCHAR)'\0';
				returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_TCHAR,CCharOutput1[j],NAME_LEN,&OutputLen1[j]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
					TEST_RETURN;
				}
			} // end of 2nd for loop 

			returncode = SQL_SUCCESS;
			_ftime(&fetchstarttime);
			j = 0;
			while (returncode == SQL_SUCCESS)
			{
				returncode = SQLFetch(hstmt);
				if((returncode != SQL_SUCCESS) && (j < col)) // need to make sure we haven't fallen off the end of the table
				{
				   if (returncode == SQL_NO_DATA_FOUND)
				   {
					    if (!FindError(_T("00000"),henv,hdbc,hstmt)) // SQLState should be "00000" when return code is SQL_NO_DATA_FOUND.
						{	
							TEST_FAILED;
							//assert(0);
							LogMsg(NONE,_T("Rows #: %d : array %d suppose to be %d at line %d.\n"),j,k, (ROWS_INSERTED*(fn+1)),__LINE__);
							LogAllErrors(henv,hdbc,hstmt);
						}
				   }     
				   else
				   {
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				   }
				}
				if (returncode == SQL_SUCCESS)
					j++;
			}
			_ftime(&fetchendtime);
			if (j == (ROWS_INSERTED*(fn+1)))
			{
				LogMsg(NONE,_T("Rows inserted Expected: %d and Actual: %d.\n"),(ROWS_INSERTED*(fn+1)),j);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("Rows inserted Expected: %d and Actual: %d at line%d.\n"),(ROWS_INSERTED*(fn+1)),j,__LINE__);
			}

			AccessTime[k] = (long)(((fetchendtime.time - fetchstarttime.time) * 1000) + (fetchendtime.millitm - fetchstarttime.millitm));
			for (j = 0; j < col; j++)
			{
				free(CCharOutput1[j]);
			} // end of 3rd for loop 
			SQLFreeStmt(hstmt,SQL_CLOSE);
		}
/*
		if (AccessTime[0] >= 	AccessTime[1])
		{
			LogMsg(NONE,_T("FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n"),AccessTime[0],AccessTime[1]);
		}	
		else
		{
			TEST_FAILED;	
			LogMsg(ERRMSG,_T("FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n"),AccessTime[0],AccessTime[1]);
		}
*/
		LogMsg(NONE,_T("FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n"),AccessTime[0],AccessTime[1]);
		TESTCASE_END;
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
		SQLExecDirect(hstmt,(SQLTCHAR*) FetchNStr[0],SQL_NTS); /* cleanup */
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */

//=====================================================================================================

	TESTCASE_BEGIN("Setup for SQLFetch isolation level tests\n");
	SQLFreeStmt(hstmt,SQL_DROP);
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS);/*clean up*/
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1], SQL_NTS);
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
	TESTCASE_END;

	i = 0; k = 0;
	while (_tcsicmp(iso_level_cqd[k],_T("endloop")) != 0)
	{
		h = 0;
		while (_tcsicmp(access_mode[h],_T("endloop")) != 0) {
			if ((_tcsstr(iso_level_cqd[k],_T("READ_UNCOMMITTED")) != NULL && _tcsstr(access_mode[h],_T("READ WRITE")) != NULL) ||
				(_tcsstr(iso_level_cqd[k],_T("REPEATABLE_READ")) != NULL && _tcsstr(access_mode[h],_T("default")) != NULL) ||
				(_tcsstr(iso_level_cqd[k],_T("SERIALIZABLE")) != NULL && _tcsstr(access_mode[h],_T("default")) != NULL))
			{
				h++;
				continue;
			}

			FullDisconnect(pTestInfo);

			_stprintf(Heading, _T("Setup for SQLFetch with: %s\nAnd access-mode: %s\n"), iso_level_cqd[k], access_mode[h]);
			TESTCASE_BEGINW(Heading);
			if(!FullConnect(pTestInfo))
			{
				LogMsg(ERRMSG,_T("Unable to connect\n"));
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

			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)iso_level_cqd[k],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			if (_tcsicmp(access_mode[h],_T("default")) != 0) {
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)access_mode[h],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
			}

			TESTCASE_END; // end of setup

			_stprintf(Heading,_T("SQLFetch by doing SQLGetData\n"));
			TESTCASE_BEGINW(Heading);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				//TEST_RETURN;
			}
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
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
						LogMsg(NONE,_T("expect: '%s' and actual: '%s' of column %d are matched\n"),CResults[j],CCharOutput2,j+1);
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
			h++;
		}

		k++;
	}//End while

	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */
	
//============================================================================================
	TESTCASE_BEGIN("Testcase for Mode_special_1\n");

	returncode = SQLExecDirect(hstmt,sqlstring0,SQL_NTS);

	returncode = SQLExecDirect(hstmt,sqlstring1,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,sqlstring2,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLPrepare(hstmt,sqlstring3,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,CCharOutput2,300,NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecute(hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLFetch(hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

#ifndef _WM
	if (_tcscmp(CCharOutput2,_T("125.2")) == 0)
	{
		LogMsg(NONE,_T("expect: '125.2' and actual: '%s' are matched\n"),CCharOutput2);
	}	
	else
	{
		TEST_FAILED;	
		LogMsg(ERRMSG,_T("expect: '125.2' and actual: '%s' are not match, at line %d\n"),CCharOutput2,__LINE__);
	}
#else
	if (_tcscmp(CCharOutput2,"125.28") == 0)
	{
		LogMsg(NONE,_T("expect: '125.28' and actual: '%s' are matched\n"),CCharOutput2);
	}	
	else
	{
		TEST_FAILED;	
		LogMsg(ERRMSG,_T("expect: '125.28' and actual: '%s' are not match, at line %d\n"),CCharOutput2,__LINE__);
	}
#endif

//============================================================================================
	
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLFetch.\n"));
	free_list(var_list);
	TEST_RETURN;
}
