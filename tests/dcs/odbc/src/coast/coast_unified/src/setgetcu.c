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

#define MAX_CURLEN		300
#define NAME_LEN_CUR	50
#define PHONE_LEN		20
#define MAX_COLLEN		258


/*
------------------------------------------------------------------
   TestSQLSetCursorName: Tests SQLSetCursorName                      
------------------------------------------------------------------
*/
PassFail TestSQLSetCursorName(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{   
	TEST_DECLARE;
 	TCHAR            Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	TCHAR	*szCursor[] = {
		_T("C1"),
		_T("C12345678901234567"),
		_T("C1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"),
        _T("C12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678"),    // Soln    10-080501-2894
		_T("C123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"),   // Soln    10-080618-3937 
		_T("endloop")
	};

	TCHAR	*szCursorExp[] = {
		_T("C1"),
		_T("C12345678901234567"),
		_T("C1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"),
        _T("C1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"),
		_T("C1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"),
		_T("endloop")
	};

	TCHAR			*invalidCursor[] = {
							_T(""),
							_T("SQLCUR1"),
							_T("SQL_CUR1"),
							_T("endloop")
					};
	SQLTCHAR			CursorName[MAX_CURLEN];
	SQLSMALLINT		pcbCursor;
	int				i,ss,Sel;
	SQLHANDLE		hstmtSelect,hstmtUpdate,hstmtDelete,hstmt1;
	SQLTCHAR			*szName, *szPhone;
	SQLLEN  		cbName, cbPhone;
	TCHAR			*UpdateValue[] = {_T("999"),_T("890")};
	TCHAR			*InsStr,*InsVals; 
	TCHAR			*TableName,*TmpStr,*SelTab,*SelTabU,*DelTab,*DrpTab,*CrtTab;
	TCHAR			*ColName[2];
	TCHAR			cqdStmt[100];
	SQLHANDLE hstmtd;
    
//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLSetCursorName"), charset_file);
	if (var_list == NULL) return FAILED;

	TableName = var_mapping(_T("SQLSetCursorName_TableName"), var_list);
	ColName[0] = var_mapping(_T("SQLSetCursorName_ColName_0"), var_list);
	ColName[1] = var_mapping(_T("SQLSetCursorName_ColName_1"), var_list);

	DrpTab = var_mapping(_T("SQLSetCursorName_DrpTab"), var_list);
	CrtTab = var_mapping(_T("SQLSetCursorName_CrtTab"), var_list);
	DelTab = var_mapping(_T("SQLSetCursorName_DelTab"), var_list);
	SelTab = var_mapping(_T("SQLSetCursorName_SelTab"), var_list);
	SelTabU = var_mapping(_T("SQLSetCursorName_SelTabU"), var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLSetCursor/GetCursor.\n"));
	TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLSetCursor/GetCursor tests\n");

	TmpStr = (TCHAR*)malloc(1024);
	if (TmpStr == NULL) {
		LogMsg(NONE,_T("Unable to malloc, at line %d\n"), __LINE__);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode=FullConnect(pTestInfo);
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
	hdbc = pTestInfo->hdbc;
	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	//CQD to READ_COMMITTED
	_stprintf (cqdStmt, _T("control query default isolation_level 'read committed'"));
	SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmtd);
	SQLExecDirect (hstmtd, (SQLTCHAR*)cqdStmt, SQL_NTS);
	SQLFreeStmt (hstmtd, SQL_DROP);

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;  // end of setup

//===========================================================================================================

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt1);
		TEST_FAILED;
		TEST_RETURN;
	}

	i = 0;
	while (_tcscmp(szCursor[i],_T("endloop")) != 0)
	{
		_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName : %s\n"),szCursor[i]);
		TESTCASE_BEGINW(Heading);

		returncode = SQLSetCursorName(hstmt1,(SQLTCHAR*)szCursor[i],SQL_NTS);//(SQLSMALLINT)_tcslen(szCursor[i]));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			LogAllErrors(henv,hdbc,hstmt1);
			TEST_FAILED;
		}
		else
		{
			returncode = SQLGetCursorName(hstmt1,CursorName,sizeof(CursorName),NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmt1);
			}

			returncode = SQLGetCursorName(hstmt1,NULL,sizeof(CursorName),&pcbCursor);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmt1);
			}

			returncode = SQLGetCursorName(hstmt1,NULL,sizeof(CursorName),NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmt1);
			}

			returncode = SQLGetCursorName(hstmt1,CursorName,sizeof(CursorName),&pcbCursor);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmt1);
			}
			else
			{
				if (_tcsicmp(szCursorExp[i], (TCHAR*)CursorName) == 0)
				{
					LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),szCursorExp[i],CursorName);
					TESTCASE_END;
				}
				else
				{
					TEST_FAILED;
					LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),szCursorExp[i],CursorName);
				}
			}
		}
		i++;
	}	

	SQLFreeStmt(hstmt1,SQL_DROP);

//===========================================================================================================

for (Sel = 0; Sel < 2; Sel++) // Loop twice to test select statement FOR UPDATE OF and without FOR UPDATE OF.
{
	_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for update table.\n"));
	TESTCASE_BEGINW(Heading);
	
	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	returncode = SQLSetCursorName(hstmtSelect, (SQLTCHAR *)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	else
	{
		// cleanup
		SQLExecDirect(hstmtSelect,(SQLTCHAR *)DrpTab,SQL_NTS);
		// Setup the table and data.
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
			InsVals = (TCHAR *)malloc(MAX_COLLEN);
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			_stprintf(InsVals,_T("Testing Set/Get Cursors & this row is : "));

			ss = 0;
			for (i = 0; i < 10; i++)
			{
				_stprintf(InsStr, _T("INSERT INTO %s VALUES ('%s %d',%d)"),TableName, InsVals, i+1, i+1);
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)InsStr,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for insert"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
					ss++;
			}
			if (ss != i)
			{
				TEST_FAILED;
				LogMsg(NONE,_T("Insert failed"));
			}
			else
			{
				// SELECT the result set and bind its columns to local buffers. 
				if (Sel == 0)
					returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTab,SQL_NTS);
				else
					returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
				}

				// Read through the result set until the cursor is      
				// positioned on the middle row. 
				_stprintf(InsVals, _T("Testing Set/Get Cursors & this row is : %d"), (i+1)/2);
			
				do
					returncode = SQLFetch(hstmtSelect);
				while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));

				// Perform a positioned update on the middle row. 

				if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName, ColName[1], UpdateValue[0]);
					returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for update"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtUpdate);
					}
					else
					{
						if (MX_MP_SPECIFIC == MP_SPECIFIC)
						{
							returncode = SQLFetch(hstmtSelect);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch for second update"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtUpdate);
							}
							_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName,ColName[1],UpdateValue[1]);
							returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for update"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtUpdate);
							}
							else
							{
								SQLFreeStmt(hstmtSelect,SQL_CLOSE);
								returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTab,SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtSelect);
								}
								else
								{
									returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
									{
										TEST_FAILED;
										TESTCASE_LOG (Heading);
										LogAllErrors(henv,hdbc,hstmtSelect);
									}
									returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
									{
										TEST_FAILED;
										TESTCASE_LOG (Heading);
										LogAllErrors(henv,hdbc,hstmtSelect);
									}
									do
										returncode = SQLFetch(hstmtSelect);
									while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));
									if (_tcscmp((TCHAR*)szPhone,UpdateValue[0]) != 0)
									{
										TEST_FAILED;
										LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),UpdateValue[0],szPhone);
									}
									returncode = SQLFetch(hstmtSelect);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch for second update"))
									{
										TEST_FAILED;
										TESTCASE_LOG (Heading);
										LogAllErrors(henv,hdbc,hstmtUpdate);
									}
									if (_tcscmp((TCHAR*)szPhone,UpdateValue[1]) != 0)
									{
										TEST_FAILED;
										LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),UpdateValue[1],szPhone);
									}
								}
								SQLFreeStmt(hstmtSelect,SQL_CLOSE);
								TESTCASE_END;
							}
						}
						else
						{
							SQLFreeStmt(hstmtSelect,SQL_CLOSE); // Need to reset out cursor for the next select stmt.
							returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTab,SQL_NTS);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtSelect);
							}
							else
							{
								returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtSelect);
								}
								returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtSelect);
								}
								do
									returncode = SQLFetch(hstmtSelect);
								while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));
								if (_tcscmp((TCHAR*)szPhone,UpdateValue[0]) != 0)
								{
									TEST_FAILED;
									LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),UpdateValue[0],szPhone);
									LogAllErrors(henv,hdbc,hstmtSelect);									
								}
								SQLFreeStmt(hstmtSelect,SQL_CLOSE);
								TESTCASE_END;
							}
						}
					}
				}
			}
			free(InsStr);
			free(InsVals);
			free(szName);
			free(szPhone);
		}
		// cleanup
		SQLExecDirect(hstmtUpdate,(SQLTCHAR *)DrpTab,SQL_NTS);
	}
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);
}

//===========================================================================================================

for (Sel = 0; Sel < 2; Sel++) // Loop twice to test select statement FOR UPDATE OF and without FOR UPDATE OF.
{
	_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for delete table.\n"));
	TESTCASE_BEGINW(Heading);
	
	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}

	returncode = SQLSetCursorName(hstmtSelect, (SQLTCHAR *)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	else
	{
		// cleanup
		SQLExecDirect(hstmtSelect,(SQLTCHAR *)DrpTab,SQL_NTS);
		// Setup the table and data.					 
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
			InsVals = (TCHAR *)malloc(MAX_COLLEN);
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			_stprintf(InsVals,_T("Testing Set/Get Cursors & this row is : "));

			ss = 0;
			for (i = 0; i < 10; i++)
			{
				_stprintf(InsStr, _T("INSERT INTO %s VALUES ('%s %d',%d)"),TableName, InsVals, i+1, i+1);
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)InsStr,SQL_NTS);
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
					ss++;
			}
			if (ss != i)
			{
				TEST_FAILED;
				LogMsg(NONE,_T("Insert failed"));
			}
			else
			{
				// SELECT the result set and bind its columns to local buffers. 
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTabU,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
				}

				// Read through the result set until the cursor is      
				// positioned on the middle row. 
				_stprintf(InsVals, _T("Testing Set/Get Cursors & this row is : %d"), (i+1)/2);
			
				do
					returncode = SQLFetch(hstmtSelect);
				while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));

				// Perform a positioned update on the middle row. 

				if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR *)DelTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for DELETE"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtUpdate);
					}
					else
					{
						SQLFreeStmt(hstmtSelect,SQL_CLOSE);
						_stprintf(TmpStr,_T("SELECT %s, %s FROM %s WHERE %s = 5"),ColName[0],ColName[1],TableName,ColName[1]);
						returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
						{
							TEST_FAILED;
							TESTCASE_LOG (Heading);
							LogAllErrors(henv,hdbc,hstmtSelect);
						}
						else
						{
							SQLFreeStmt(hstmtSelect,SQL_CLOSE);
							TESTCASE_END;
						}
					}
				}
			}
			free(InsStr);
			free(InsVals);
			free(szName);
			free(szPhone);
		}
		// cleanup
		SQLExecDirect(hstmtUpdate,(SQLTCHAR *)DrpTab,SQL_NTS);
	}
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);
}

//===========================================================================================================

for (Sel = 0; Sel < 2; Sel++) // Loop twice to test select statement FOR UPDATE OF and without FOR UPDATE OF.
{
	_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for update table twice with AUTOCOMMIT OFF.\n"));
	TESTCASE_BEGINW(Heading);

	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	returncode = SQLSetCursorName(hstmtSelect, (SQLTCHAR *)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	else
	{
		// cleanup
		SQLExecDirect(hstmtSelect,(SQLTCHAR *)DrpTab,SQL_NTS);
		// Setup the table and data.
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
			InsVals = (TCHAR *)malloc(MAX_COLLEN);
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			_stprintf(InsVals,_T("Testing Set/Get Cursors & this row is : "));
			ss = 0;
			for (i = 0; i < 10; i++)
			{
				_tcscpy(InsStr,_T(""));
				_stprintf(InsStr, _T("INSERT INTO %s VALUES ('%s%d',%d)"),TableName, InsVals, i+1, i+1); 
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)InsStr,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for insert"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
					ss++;
			}
			if (ss != i)
			{
				TEST_FAILED;
				LogMsg(NONE,_T("Insert failed"));
			}
			else
			{
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
				if (returncode != SQL_SUCCESS)
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				} 
				// SELECT the result set and bind its columns to local buffers. 
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTabU,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
				}

				// Read through the result set until the cursor is      
				// positioned on the middle row. 
				_stprintf(InsVals, _T("Testing Set/Get Cursors & this row is : %d"), (i+1)/2);
			
				do
					returncode = SQLFetch(hstmtSelect);
				while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));

				// Perform a positioned update on the middle row. 

				if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName,ColName[1],UpdateValue[0]);
					returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for update"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtUpdate);
					}
					else
					{
						returncode = SQLFetch(hstmtSelect);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch for second update"))
						{
							TEST_FAILED;
							TESTCASE_LOG (Heading);
							LogAllErrors(henv,hdbc,hstmtUpdate);
						}
						_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName,ColName[1],UpdateValue[1]);
						returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for update"))
						{
							TEST_FAILED;
							TESTCASE_LOG (Heading);
							LogAllErrors(henv,hdbc,hstmtUpdate);
						}
						else
						{
							SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_COMMIT); 
							SQLFreeStmt(hstmtSelect,SQL_CLOSE);
							SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
							returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTab,SQL_NTS);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtSelect);
							}
							else
							{
								returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtSelect);
								}
								returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtSelect);
								}
								do
									returncode = SQLFetch(hstmtSelect);
								while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));
								if (_tcscmp((TCHAR*)szPhone,UpdateValue[0]) != 0)
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),UpdateValue[0],szPhone);
								}
								returncode = SQLFetch(hstmtSelect);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch for second update"))
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogAllErrors(henv,hdbc,hstmtUpdate);
								}
								if (_tcscmp((TCHAR*)szPhone,UpdateValue[1]) != 0)
								{
									TEST_FAILED;
									TESTCASE_LOG (Heading);
									LogMsg(NONE,_T("expect: %s and actual: %s are not matched\n"),UpdateValue[1],szPhone);
								}
							}
							SQLFreeStmt(hstmtSelect,SQL_CLOSE);
							TESTCASE_END;
						}
					}
				}
			}
			free(InsStr);
			free(InsVals);
			free(szName);
			free(szPhone);
		}
		// cleanup
		SQLExecDirect(hstmtUpdate,(SQLTCHAR *)DrpTab,SQL_NTS);
	}
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);
}

//===========================================================================================================

	for (i = 0; i < 10; i++)
	{
		_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for update table with auto_commit\n"));
		TESTCASE_BEGINW(Heading);

		// Allocate the statements and set the cursor name.
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
		{
			LogAllErrors(henv,hdbc,hstmtSelect);
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			TEST_RETURN;
		}
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
		{
			LogAllErrors(henv,hdbc,hstmtUpdate);
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			TEST_RETURN;
		}
		returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		} 
		SQLExecDirect(hstmtSelect,(SQLTCHAR *)DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			_tcscpy(TmpStr,_T(""));
			_stprintf(TmpStr,_T("INSERT INTO %s VALUES ('Rao Kakarlamudi',2856167)"),TableName);	
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			_stprintf(TmpStr,_T("INSERT INTO %s VALUES ('Dat Dang',2857149)"),TableName);
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if (returncode != SQL_SUCCESS)
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			_stprintf(TmpStr,_T("INSERT INTO %s VALUES ('Selva Ganesan',2855179)"),TableName);
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if (returncode != SQL_SUCCESS)
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			_stprintf(TmpStr,_T("INSERT INTO %s VALUES ('Neelam Moharil',2855128)"),TableName);
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if (returncode != SQL_SUCCESS)
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
		}
		SQLFreeStmt(hstmtSelect,SQL_DROP);
		TESTCASE_END;
		_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for update table.\n"));
		TESTCASE_BEGINW(Heading);
		returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		} 
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtDelete);	
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtDelete);
		}
		returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLSetCursorName(hstmtSelect,(SQLTCHAR *)szCursor[0], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			if (MX_MP_SPECIFIC == MP_SPECIFIC)
			{
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
				if (returncode != SQL_SUCCESS)
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				} 
			}
			_stprintf(TmpStr,_T("SELECT %s, %s FROM %s WHERE %s = 'Selva Ganesan' AND %s = 2855179 FOR UPDATE OF %s,%s"),ColName[0],ColName[1],TableName,ColName[0],ColName[1],ColName[0],ColName[1]);
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			if (MX_MP_SPECIFIC == MP_SPECIFIC)
			{
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_UNCOMMITTED);
				if (returncode != SQL_SUCCESS)
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				} 
			}
			returncode = SQLFetch(hstmtSelect);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			returncode = SQLGetData(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
			returncode = SQLGetData(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
			if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
			{
				returncode = SQLExecDirect(hstmtDelete,(SQLTCHAR *)DelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for DELETE"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtDelete);
				}
				else
					TESTCASE_END;
			}
			free(szName);
			free(szPhone);
		}
		SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_COMMIT); 
		SQLFreeStmt(hstmtSelect,SQL_DROP);
		SQLFreeStmt(hstmtDelete,SQL_DROP);

		_stprintf(Heading,_T("Test functionality of select twice using same cursor without going upto the end of table.\n"));
		TESTCASE_BEGINW(Heading);

		returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		} 
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLSetCursorName(hstmtSelect,(SQLTCHAR *)szCursor[0], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTab,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			returncode = SQLFetch(hstmtSelect);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			returncode = SQLGetData(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
			returncode = SQLGetData(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
			if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
			{
				returncode = SQLFreeStmt(hstmtSelect,SQL_CLOSE);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)SelTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLFetch(hstmtSelect);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					else
						TESTCASE_END;
				}
			}
			free(szName);
			free(szPhone);
		}
		SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_COMMIT); 
		SQLFreeStmt(hstmtSelect,SQL_DROP);

		_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for update table.\n"));
		TESTCASE_BEGINW(Heading);

		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtDelete);	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtDelete);
		}
		TESTCASE_END;

		_stprintf(Heading,_T("Test Positive functionality of SQLSetCursorName/SQLGetCursorName for delete table.\n"));
		TESTCASE_BEGINW(Heading);

		returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_LOCK,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		returncode = SQLSetCursorName(hstmtSelect, (SQLTCHAR *)szCursor[0], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			if (MX_MP_SPECIFIC == MP_SPECIFIC)
			{
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
				if (returncode != SQL_SUCCESS)
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				} 
			}
			_stprintf(TmpStr,_T("SELECT %s, %s FROM %s WHERE %s = 'Neelam Moharil' AND %s = 2855128 FOR UPDATE OF %s,%s"),ColName[0],ColName[1],TableName,ColName[0],ColName[1],ColName[0],ColName[1]);
			returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR *)TmpStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			if (MX_MP_SPECIFIC == MP_SPECIFIC)
			{
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_UNCOMMITTED);
				if (returncode != SQL_SUCCESS)
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				} 
			}
			returncode = SQLFetch(hstmtSelect);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			returncode = SQLGetData(hstmtSelect, 1, SQL_C_TCHAR, szName, NAME_LEN_CUR, &cbName);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			returncode = SQLGetData(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
			{
				TEST_FAILED;
				TESTCASE_LOG (Heading);
				LogAllErrors(henv,hdbc,hstmtSelect);
			}
			if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
			{
				returncode = SQLExecDirect(hstmtDelete,(SQLTCHAR *)DelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for update"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtDelete);
				}
				else
					TESTCASE_END;
			}
			free(szName);
			free(szPhone);
		}
		SQLExecDirect(hstmtUpdate,(SQLTCHAR *)DrpTab,SQL_NTS);

		SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_COMMIT); 
		SQLFreeStmt(hstmtSelect,SQL_DROP);
		SQLFreeStmt(hstmtUpdate,SQL_DROP);
		SQLFreeStmt(hstmtDelete,SQL_DROP);
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
	}

//===========================================================================================================

for (Sel = 0; Sel < 2; Sel++) // Loop twice to test select statement FOR UPDATE OF and without FOR UPDATE OF.
{
	_stprintf(Heading,_T("Test Negative functionality of SQLSetCursorName/SQLGetCursorName for update table with SQL_ATTR_CONCURRENCY attribute set to SQL_CONCUR_READ_ONLY.\n"));
	TESTCASE_BEGINW(Heading);
	
	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_READ_ONLY,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	returncode = SQLSetCursorName(hstmtSelect, (SQLTCHAR*)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	else
	{
		// cleanup
		SQLExecDirect(hstmtSelect,(SQLTCHAR*)DrpTab,SQL_NTS);
		// Setup the table and data.
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
			InsVals = (TCHAR *)malloc(MAX_COLLEN);
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			_stprintf(InsVals,_T("Testing Set/Get Cursors & this row is : "));
			ss = 0;
			for (i = 0; i < 10; i++)
			{
				_stprintf(InsStr, _T("INSERT INTO %s VALUES ('%s %d',%d)"),TableName, InsVals, i+1, i+1);
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)InsStr,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for insert"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
					ss++;
			}
			if (ss != i)
			{
				TEST_FAILED;
				LogMsg(NONE,_T("Insert failed"));
			}
			else
			{
				// SELECT the result set and bind its columns to local buffers. 
				if (Sel == 0)
					returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTabU,SQL_NTS);
				else
					returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
				}

				// Read through the result set until the cursor is      
				// positioned on the middle row. 
				_stprintf(InsVals, _T("Testing Set/Get Cursors & this row is : %d"), (i+1)/2);
			
				do
					returncode = SQLFetch(hstmtSelect);
				while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));

				// Perform a positioned update on the middle row. 

				if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName,ColName[1],UpdateValue[0]);
					returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
					if(!CHECKRC(SQL_ERROR,returncode,"SQLSetCursorName for update"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtUpdate);
					}
					else
					{
						if (MX_MP_SPECIFIC == MP_SPECIFIC)
						{
							returncode = SQLFetch(hstmtSelect);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch for second update"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtUpdate);
							}
							_stprintf(InsStr,_T("UPDATE %s SET %s = %s WHERE CURRENT OF C1"),TableName,ColName[1],UpdateValue[1]);
							returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)InsStr,SQL_NTS);
							if(!CHECKRC(SQL_ERROR,returncode,"SQLSetCursorName for update"))
							{
								TEST_FAILED;
								TESTCASE_LOG (Heading);
								LogAllErrors(henv,hdbc,hstmtUpdate);
							}
						}
						SQLFreeStmt(hstmtSelect,SQL_CLOSE); // Need to reset out cursor for the next select stmt.
					}
				}
			}
			free(InsStr);
			free(InsVals);
			free(szName);
			free(szPhone);
		}
		// cleanup
		SQLExecDirect(hstmtUpdate,(SQLTCHAR*)DrpTab,SQL_NTS);
	}
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);
}

//===================================================================================================================================

for (Sel = 0; Sel < 2; Sel++) // Loop twice to test select statement FOR UPDATE OF and without FOR UPDATE OF.
{
	_stprintf(Heading,_T("Test Negative functionality of SQLSetCursorName/SQLGetCursorName for delete table with SQL_ATTR_CONCURRENCY attribute set to SQL_CONCUR_READ_ONLY.\n"));
	TESTCASE_BEGINW(Heading);
		
	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetStmtAttr(hstmtSelect, SQL_ATTR_CONCURRENCY, (void *)SQL_CONCUR_READ_ONLY,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}

	returncode = SQLSetCursorName(hstmtSelect,(SQLTCHAR*)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	else
	{
		// cleanup
		SQLExecDirect(hstmtSelect,(SQLTCHAR*)_T("DROP TABLE TESTSETGETCURSOR1"),SQL_NTS);
		// Setup the table and data.
		returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)CrtTab,SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmtSelect);
		}
		else
		{
			InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
			InsVals = (TCHAR *)malloc(MAX_COLLEN);
			szName = (SQLTCHAR *)malloc(MAX_COLLEN);
			szPhone = (SQLTCHAR *)malloc(PHONE_LEN);
			_stprintf(InsVals,_T("Testing Set/Get Cursors & this row is : "));
			ss = 0;
			for (i = 0; i < 10; i++)
			{
				_stprintf(InsStr, _T("INSERT INTO %s VALUES ('%s %d',%d)"),TableName, InsVals, i+1, i+1);
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)InsStr,SQL_NTS);
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
					ss++;
			}
			if (ss != i)
			{
				TEST_FAILED;
				LogMsg(NONE,_T("Insert failed"));
			}
			else
			{
				// SELECT the result set and bind its columns to local buffers. 
				returncode = SQLExecDirect(hstmtSelect,(SQLTCHAR*)SelTabU,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
				{
					TEST_FAILED;
					TESTCASE_LOG (Heading);
					LogAllErrors(henv,hdbc,hstmtSelect);
				}
				else
				{
					returncode = SQLBindCol(hstmtSelect, 1, SQL_C_TCHAR, szName, MAX_COLLEN, &cbName);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
					returncode = SQLBindCol(hstmtSelect, 2, SQL_C_TCHAR, szPhone, PHONE_LEN, &cbPhone);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName for select"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtSelect);
					}
				}

				// Read through the result set until the cursor is      
				// positioned on the middle row. 
				_stprintf(InsVals, _T("Testing Set/Get Cursors & this row is : %d"), (i+1)/2);
			
				do
					returncode = SQLFetch(hstmtSelect);
				while ((returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO) && (_tcscmp((TCHAR*)szName, InsVals) != 0));

				// Perform a positioned update on the middle row. 

				if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					returncode = SQLExecDirect(hstmtUpdate,(SQLTCHAR*)DelTab,SQL_NTS);
					if(!CHECKRC(SQL_ERROR,returncode,"SQLSetCursorName for DELETE"))
					{
						TEST_FAILED;
						TESTCASE_LOG (Heading);
						LogAllErrors(henv,hdbc,hstmtUpdate);
					}
					SQLFreeStmt(hstmtSelect,SQL_CLOSE);
				}
			}
			free(InsStr);
			free(InsVals);
			free(szName);
			free(szPhone);
		}
		// cleanup
		SQLExecDirect(hstmtUpdate,(SQLTCHAR*)DrpTab,SQL_NTS);
	}
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);
}

//============================================================================================================================

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt1);
		TEST_FAILED;
		TEST_RETURN;
	}

	i = 0;
	while (_tcsicmp(invalidCursor[i],_T("endloop")) != 0)
	{
		_stprintf(Heading,_T("Test Negative functionality of SQLSetCursorName/SQLGetCursorName : %s\n"),invalidCursor[i]);
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLSetCursorName(hstmt,(SQLTCHAR*)invalidCursor[i],(SQLSMALLINT)_tcslen(invalidCursor[i]));
		if(!CHECKRC(SQL_ERROR,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
			TESTCASE_END;
		i++;

		SQLFreeStmt(hstmt, SQL_CLOSE);
	}

	SQLFreeStmt(hstmt1, SQL_DROP);

//===========================================================================================================

	_stprintf(Heading,_T("Test Negative functionality of SQLSetCursorName for duplicate cursor name by adding same cursor name to different statement handles.\n"));
	TESTCASE_BEGINW(Heading);
	
	
	// Allocate the statements and set the cursor name.
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtSelect);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtSelect);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmtUpdate);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmtUpdate);
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		TEST_RETURN;
	}
	returncode = SQLSetCursorName(hstmtSelect,(SQLTCHAR*)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtSelect);
	}
	returncode = SQLSetCursorName(hstmtUpdate,(SQLTCHAR*)szCursor[0], SQL_NTS);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmtUpdate);
	}
	else
		TESTCASE_END;
	SQLFreeStmt(hstmtSelect,SQL_DROP);
	SQLFreeStmt(hstmtUpdate,SQL_DROP);

//===========================================================================================================

	_stprintf(Heading,_T("Test Negative functionality of SQLSetCursorName with null hstmt\n"));
	TESTCASE_BEGINW(Heading);
	

	returncode = SQLSetCursorName((SQLHANDLE)NULL,(SQLTCHAR*)szCursor[0],(SQLSMALLINT)_tcslen(szCursor[0]));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
		TESTCASE_END;

//===========================================================================================================

	_stprintf(Heading,_T("Test Negative functionality of SQLGetCursorName with null hstmt\n"));
	TESTCASE_BEGINW(Heading);
	
	returncode = SQLSetCursorName(hstmt,(SQLTCHAR*)szCursor[0],(SQLSMALLINT)_tcslen(szCursor[0]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetCursorName"))
	{
		TEST_FAILED;
		TESTCASE_LOG (Heading);
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLGetCursorName((SQLHANDLE)NULL,CursorName,sizeof(CursorName),&pcbCursor);
		if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLSetCursorName"))
		{
			TEST_FAILED;
			TESTCASE_LOG (Heading);
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
			TESTCASE_END;
	}	
	SQLFreeStmt(hstmt, SQL_CLOSE);

//===========================================================================================================
	free(TmpStr);
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLSetCursor/GetCursor.\n"));
	free_list(var_list);
	TEST_RETURN;
}
