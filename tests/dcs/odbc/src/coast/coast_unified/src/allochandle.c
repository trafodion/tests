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

#define NUM_STMT		20
#define NUM_ASYNC_STMT	10

//---------------------------------------------------------
//   TestMXSQLAllocHandle()
//---------------------------------------------------------
PassFail TestMXSQLAllocHandle(TestInfo *pTestInfo)
{
	TEST_DECLARE;

	TCHAR			*StmtHndlStr;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	RETCODE			returncode;
 	SQLHANDLE		hstmt[NUM_STMT];
 	TCHAR			Heading[MAX_STRING_SIZE];
	int				i = 0, j = 0, k = 0;
	int				AnyAsync;
	int				AsyncOper[] = {CREATE_TABLE,INSERT_TABLE,SELECT_TABLE,DROP_TABLE,999};

	struct AsyncStmt_struct {
		RETCODE	status;
		BOOL	checked;
	} AsyncStmt[NUM_ASYNC_STMT];

	TCHAR			*teststmthndl[21];

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLAllocateHandle"), charset_file);
	if (var_list == NULL) return FAILED;

	teststmthndl[0] = var_mapping(_T("TestStmtHndl_0"), var_list);
	teststmthndl[1] = var_mapping(_T("TestStmtHndl_1"), var_list);
	teststmthndl[2] = var_mapping(_T("TestStmtHndl_2"), var_list);
	teststmthndl[3] = var_mapping(_T("TestStmtHndl_3"), var_list);
	teststmthndl[4] = var_mapping(_T("TestStmtHndl_4"), var_list);
	teststmthndl[5] = var_mapping(_T("TestStmtHndl_5"), var_list);
	teststmthndl[6] = var_mapping(_T("TestStmtHndl_6"), var_list);
	teststmthndl[7] = var_mapping(_T("TestStmtHndl_7"), var_list);
	teststmthndl[8] = var_mapping(_T("TestStmtHndl_8"), var_list);
	teststmthndl[9] = var_mapping(_T("TestStmtHndl_9"), var_list);
	teststmthndl[10] = var_mapping(_T("TestStmtHndl_10"), var_list);
	teststmthndl[11] = var_mapping(_T("TestStmtHndl_11"), var_list);
	teststmthndl[12] = var_mapping(_T("TestStmtHndl_12"), var_list);
	teststmthndl[13] = var_mapping(_T("TestStmtHndl_13"), var_list);
	teststmthndl[14] = var_mapping(_T("TestStmtHndl_14"), var_list);
	teststmthndl[15] = var_mapping(_T("TestStmtHndl_15"), var_list);
	teststmthndl[16] = var_mapping(_T("TestStmtHndl_16"), var_list);
	teststmthndl[17] = var_mapping(_T("TestStmtHndl_17"), var_list);
	teststmthndl[18] = var_mapping(_T("TestStmtHndl_18"), var_list);
	teststmthndl[19] = var_mapping(_T("TestStmtHndl_19"), var_list);
	teststmthndl[20] = var_mapping(_T("TestStmtHndl_20"), var_list);
//======================================================================================
// Initialization Test Case

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX specific SQLAllocHandle.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLAllocStmt/SQLFreeStmt tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
	//set the connection attribute to SQL_AUTOCOMMIT_OFF to enable use of multiple stmt  without errors 
	SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);

	TESTCASE_END;  // end of setup

	StmtHndlStr = (TCHAR *)malloc(MAX_NOS_SIZE);

//====================================================================================================
// General statement handle exercise testcases.

	for (k = 0; k < 2; k++)
	{
		// ***************************
		// This section first does some pre-work cleanup. Next, it tests to
		// make sure that ODBC can create a series of test tables.
		for (i = 0; i < NUM_STMT; i++)
		{
			hstmt[i] = (SQLHANDLE)pTestInfo->hstmt;

			_stprintf(Heading,_T("SQLAllocHandle: Statement Handle Creation Test #%d\n"),i);
			TESTCASE_BEGINW(Heading);
			returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
			TESTCASE_END;
			
			if (returncode == SQL_SUCCESS)
			{
				//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DDLs ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
				// Pre-work clean-up. Making sure environment is clean
		 		if (i == 0)
				{
					for (j = 0; j < NUM_STMT; j++)
					{
						SQLExecDirect(hstmt[0],(SQLTCHAR*)StmtQueries(DROP_TABLE,teststmthndl[j],StmtHndlStr),SQL_NTS); 
					}
				}

				// Creating test tables.
				_stprintf(Heading,_T("SQLAllocHandle: create table teststmthndl%d\n"),i+1);
				TESTCASE_BEGINW(Heading);

				if (k == 0)	// prepare & execute 
				{
					returncode = SQLPrepare(hstmt[i],(SQLTCHAR*)StmtQueries(CREATE_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS); 
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
					else
					{
						returncode = SQLExecute(hstmt[i]);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
						{
							TEST_FAILED;
							LogAllErrorsVer3(henv,hdbc,hstmt[i]);
						}
					}
				}
				else	// execdirect 
				{
					returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(CREATE_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
				TESTCASE_END;
			}
		}

		//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF
		SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
		// ***************************
		// This section tests if inserts can be done on our test tables.
		for (i = 0; i < NUM_STMT; i++)
		{
			_stprintf(Heading,_T("SQLAllocHandle: inserts using Statement Handle[%d]\n"),i);
			TESTCASE_BEGINW(Heading);
			if (k == 0)	// prepare & execute 
			{
				returncode = SQLPrepare(hstmt[i],(SQLTCHAR*)StmtQueries(INSERT_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
				else
				{
					returncode = SQLExecute(hstmt[i]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
			}
			else	// execdirect 
			{
				returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(INSERT_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
			}
			TESTCASE_END;
		}

		// ***************************
		// This section tests if selects can be done on our test tables.
		for (i = 0; i < NUM_STMT; i++)
		{
			_stprintf(Heading,_T("SQLAllocHandle: selects using Statement Handle[%d]\n"),i);
			TESTCASE_BEGINW(Heading);
			if (k == 0)	// prepare & execute 
			{
				returncode = SQLPrepare(hstmt[i],(SQLTCHAR*)StmtQueries(SELECT_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
				else
				{
					returncode = SQLExecute(hstmt[i]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
			}
			else	// execdirect 
			{
				returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(SELECT_TABLE,teststmthndl[i],StmtHndlStr),SQL_NTS); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
			}
			TESTCASE_END;
		}

		// ***************************
		// This section tests if fetches can be done on our test tables.
		for (i = (NUM_STMT-1); i > -1; i--)
		{
			_stprintf(Heading,_T("SQLAllocStmt: fetches on selects using Statement Handle[%d]\n"),i);
			TESTCASE_BEGINW(Heading);
			returncode = SQLFetch(hstmt[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}			
			TESTCASE_END;
		}

		// ***************************
		// This section first tests if our statement handles can be closed.
		// Next, it cleans up the test tables now that we have finished with them.
		for (i = 0; i < NUM_STMT; i++)
		{
			_stprintf(Heading,_T("SQLAllocHandle: Running SQLFreeStmt on statement handle[%d] with SQL_CLOSE\n"),i);
			TESTCASE_BEGINW(Heading);
			returncode = SQLFreeStmt(hstmt[i],SQL_CLOSE);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
			TESTCASE_END;

			if (i == (NUM_STMT-1))					// cleanup 
			{
				//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DROP TABLE ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
				for (j = 0; j < NUM_STMT; j++)
				{
					SQLExecDirect(hstmt[0],(SQLTCHAR*)StmtQueries(DROP_TABLE,teststmthndl[j],StmtHndlStr),SQL_NTS); 
				}
				//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
			}
		}

		// ***************************
		// This section tests if the statement handles can be set free.
		for (i = 0; i < NUM_STMT; i++)
		{
			_stprintf(Heading,_T("SQLAllocHandle: Running SQLFreeHandle on statement handle[%d]\n"),i);
			TESTCASE_BEGINW(Heading);
			returncode = SQLFreeHandle(SQL_HANDLE_STMT, hstmt[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
			TESTCASE_END;
		}

		// ***************************
		// This section first performs some pre-work cleanup. Afterwards, it
		// performs creates, inserts, selects, and fetches. Then it closes
		// and frees the statement handles. All of the operations on each
		// handle is considered a single test case.
		_stprintf(Heading,_T("SLQAllocHandle: Performing SQL operations on statement handle[%d]\n"),i);
		TESTCASE_BEGINW(Heading);
 		
		// This loop drops, creates, inserts, selects, and fetches from the test table
		// from each statement handle.
		for (i = 0; i < NUM_STMT; i++)
		{
			hstmt[i] = (SQLHANDLE)pTestInfo->hstmt;
			returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
			if (returncode == SQL_SUCCESS)
			{
		 		if (i == 0)									// cleanup
				{
					//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DDLs TABLE ON TRAF
					SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
					SQLExecDirect(hstmt[0], (SQLTCHAR*)StmtQueries(DROP_TABLE, teststmthndl[20], StmtHndlStr), SQL_NTS);
						returncode = SQLExecDirect(hstmt[0],(SQLTCHAR*)StmtQueries(CREATE_TABLE,teststmthndl[20],StmtHndlStr),SQL_NTS); 
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[0]);
					}			
					//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF
					SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
				}
				if (k == 0)	// prepare & execute 
				{
					returncode = SQLPrepare(hstmt[i],(SQLTCHAR*)StmtQueries(INSERT_TABLE,teststmthndl[20],StmtHndlStr),SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}			
					returncode = SQLExecute(hstmt[i]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
				else	// execdirect
				{
					returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(INSERT_TABLE,teststmthndl[20],StmtHndlStr),SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
				if (k == 0)	// prepare & execute 
				{
					returncode = SQLPrepare(hstmt[i],(SQLTCHAR*)StmtQueries(SELECT_TABLE,teststmthndl[20],StmtHndlStr),SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}			
					returncode = SQLExecute(hstmt[i]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
				else
				{
					returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(SELECT_TABLE,teststmthndl[20],StmtHndlStr),SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt[i]);
					}
				}
				returncode = SQLFetch(hstmt[i]); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
			}
		}
 		for (i = 0; i < NUM_STMT; i++)
		{
			returncode = SQLFreeStmt(hstmt[i],SQL_CLOSE);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
			if (i == 0)
			{
				//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DDLs ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
				SQLExecDirect(hstmt[0], (SQLTCHAR*)StmtQueries(DROP_TABLE, teststmthndl[20], StmtHndlStr), SQL_NTS);
				//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF AFTER DROP TABLE ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
			}
			returncode = SQLFreeHandle(SQL_HANDLE_STMT, hstmt[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
		}
		TESTCASE_END;
	}

//====================================================================================================
// Asynchronus Testcases

	// ***************************
	// This section first performs some pre-work cleanup. Afterwards, it creates
	// the statement handles and sets them to run asynchronously.
	for (i = 0; i < NUM_ASYNC_STMT; i++)
	{
		hstmt[i] = (SQLHANDLE)pTestInfo->hstmt;
		// Creating statement handles
		_stprintf(Heading,_T("SQLAllocHandle: Test #%d and Enable the ASYNC MODE ON.\n"),i);
		TESTCASE_BEGINW(Heading);
		returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt[i]);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
		{
			TEST_FAILED;
			LogAllErrorsVer3(henv,hdbc,hstmt[i]);
		}
		else
		{
			if (i == 0)									// cleanup 
			{
				//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DDLs ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
				// Creating tables to be used by each of the stmt handles
				for (j = 0; j < NUM_ASYNC_STMT; j++)
				{
					SQLExecDirect(hstmt[0],(SQLTCHAR*)StmtQueries(DROP_TABLE,teststmthndl[j],StmtHndlStr),SQL_NTS); 
				}
				//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF FOR DROP TABLE ON TRAF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
			}
			// Putting each stmthandle into Asynchronus mode
			returncode = SQLSetStmtOption(hstmt[i],SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOptions"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt[i]);
			}
		}
		TESTCASE_END;
	}

	// Running the Asynchronus tests
	// WHAT IS GOING ON
	//   Two tests cases are being checked:
	//     1. That the status of an asynchronus stmt handle CAN be checked.
	//     2. That the stmt handle completes correctly.
	//
	// HOW IT'S BEING RUN
	//   Steps being performed until all handles are no longer executing:
	//     1. Prepare the async test data structure.
	//     2. Generate table name based on statement handle being used.
	//     3. If handle's status has not been checked already, check as test case 1.
	//        Else, check it's status NOT as a test case.
	//     4. Run the statement (also used to check the status of the handle).
	//     5. If the stmt completes, verify that it does so successfully. Test case 2.
	//
	//   Once all of the handles have completed, perform the next Async Operation
	//   until the terminating operation (a.k.a "999") is reached.
	k = 0;
	while (AsyncOper[k] != 999)
	{
		// 1. Preparing the async test data structure
		for (i = 0; i < NUM_ASYNC_STMT; i++)
		{
			AsyncStmt[i].status = SQL_STILL_EXECUTING;
			AsyncStmt[i].checked = FALSE;
		}
		AnyAsync = 1;
		// Testing begins
		while (AnyAsync > 0)
		{
			for (i = 0; i < NUM_ASYNC_STMT; i++)
			{
				if (AsyncOper[k] == CREATE_TABLE || AsyncOper[k] == DROP_TABLE)
					//May 9, 2014 - set the connection attribute to SQL_AUTOCOMMIT_ON FOR DDLs TABLE ON TRAF
					SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER);
				if (AsyncStmt[i].status == SQL_STILL_EXECUTING)
				{
					// 3. Has the handle been checked for its status?
					if (AsyncStmt[i].checked)
					{
						// 4. Run the statement.
						returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(AsyncOper[k],teststmthndl[i],StmtHndlStr),SQL_NTS);
						AsyncStmt[i].status = returncode;
						// 5. Result Test: Verifying that the statement completes correctly.
						if (returncode != SQL_STILL_EXECUTING)
						{
							_stprintf(Heading,_T("SQLAllocHandle: Result Test: %d; SQLStmt: %s.\n"),i,StmtQueries(AsyncOper[k],teststmthndl[i],StmtHndlStr));
							TESTCASE_BEGINW(Heading);
							if (returncode != SQL_SUCCESS)
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt[i]);
							}
							TESTCASE_END;
						}
					}
					else
					{
						// Status Test (Test case 1):
						// Only EXECUTING and SUCCESS are acceptable, others are errors.
						//   This test is only run once!
						_stprintf(Heading,_T("SQLAllocHandle: Status Test: %d; SQLStmt: %s.\n"),i,StmtQueries(AsyncOper[k],teststmthndl[i],StmtHndlStr));
						TESTCASE_BEGINW(Heading);
						
						// 4. Run the statement.
						returncode = SQLExecDirect(hstmt[i],(SQLTCHAR*)StmtQueries(AsyncOper[k],teststmthndl[i],StmtHndlStr),SQL_NTS);
						AsyncStmt[i].status = returncode;
						AsyncStmt[i].checked = TRUE;
						if ((returncode != SQL_STILL_EXECUTING) && (returncode != SQL_SUCCESS))
						{
							TEST_FAILED;
							LogAllErrorsVer3(henv,hdbc,hstmt[i]);
						}
						TESTCASE_END;
						
						// 5. If the stmt completes, verify that it does so successfully.
						if (returncode != SQL_STILL_EXECUTING)
						{
							// Result Test: Verifying that the stmt completes successfully.
							_stprintf(Heading,_T("SQLAllocHandle: Result Test: %d; SQLStmt: %s.\n"),i,StmtQueries(AsyncOper[k],teststmthndl[i],StmtHndlStr));
							TESTCASE_BEGINW(Heading);
							if (returncode != SQL_SUCCESS)
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt[i]);
							}
							TESTCASE_END;
						}
					}
				}
				//May 9, 2014 - set the connection attribute back to SQL_AUTOCOMMIT_OFF
				SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_ATTR_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
			}
			AnyAsync = 0;
			for (i = 0; i < NUM_ASYNC_STMT; i++)
			{
				if (AsyncStmt[i].status == SQL_STILL_EXECUTING)
				{
					AnyAsync = AnyAsync + 1;
				}
			}
		}

		// Special tests for Fetching after doing a SELECT
		// Steps are identical to the above steps.
		if (AsyncOper[k] == SELECT_TABLE)
		{
			// Preparing data structure
			for (i = 0; i < NUM_ASYNC_STMT; i++)
			{
				AsyncStmt[i].status = SQL_STILL_EXECUTING;
				AsyncStmt[i].checked = FALSE;
			}
			AnyAsync = 1;
			// Select testing begins
			while (AnyAsync > 0)
			{
				for (i = 0; i < NUM_ASYNC_STMT; i++)
				{
					if (AsyncStmt[i].status == SQL_STILL_EXECUTING)
					{
						if (AsyncStmt[i].checked)
						{
							returncode = SQLFetch(hstmt[i]);
							AsyncStmt[i].status = returncode;									
							if (returncode != SQL_STILL_EXECUTING)
							{
								// Result Test
								_stprintf(Heading,_T("SQLAllocStmt: Result Test:%d; performing SQLFetch.\n"),i);
								TESTCASE_BEGINW(Heading);
								if (returncode != SQL_SUCCESS)
								{
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt[i]);
								}
								TESTCASE_END;
							}
						}
						else
						{
							// Status Test
							_stprintf(Heading,_T("SQLAllocStmt: Status Test:%d; performing SQLFetch.\n"),i);
							TESTCASE_BEGINW(Heading);
							returncode = SQLFetch(hstmt[i]);
							AsyncStmt[i].status = returncode;
							AsyncStmt[i].checked = TRUE;
							if ((returncode != SQL_STILL_EXECUTING) && (returncode != SQL_SUCCESS))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt[i]);
							}
							TESTCASE_END;

							// Result Test
							if (returncode != SQL_STILL_EXECUTING)
							{
								_stprintf(Heading,_T("SQLAllocStmt: Result Test:%d; performing SQLFetch.\n"),i);
								TESTCASE_BEGINW(Heading);
								if (returncode != SQL_SUCCESS)
								{
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt[i]);
								}
								TESTCASE_END;
							}
						}
					}
				}
				AnyAsync = 0;
				for (i = 0; i < NUM_ASYNC_STMT; i++)
				{
					if (AsyncStmt[i].status == SQL_STILL_EXECUTING)
					{
						AnyAsync = AnyAsync + 1;
					}
				}
			}
			// Closing the cursor from the SELECT stmt result set.
			for (i = 0; i < NUM_ASYNC_STMT; i++)
			{
				_stprintf(Heading,_T("SQLFreeStmt: %d.\n"),i);
				TESTCASE_BEGINW(Heading);
				returncode = SQLFreeStmt(hstmt[i],SQL_CLOSE);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt[i]);
				}
				TESTCASE_END;
			}
		} // End of async SELECT test.

		// Resetting the checked status for the next operation.
		for (i = 0; i < NUM_ASYNC_STMT; i++)
		{
			AsyncStmt[i].checked = FALSE;
		}

		k++;
	}

//====================================================================================================
// Test Cleanup
	free(StmtHndlStr);

	returncode = SQLDisconnect((SQLHANDLE)hdbc);
    if(!CHECKRC(SQL_ERROR,returncode,"SQLDisconnect")) 
	{
		TEST_FAILED;	
		LogAllErrorsVer3(henv,hdbc,hstmt[0]);
	}	
	
	// Free the open transactions.
	returncode=SQLEndTran(SQL_HANDLE_DBC,(SQLHANDLE)hdbc,SQL_ROLLBACK);
	Sleep(2);	

	returncode=FullDisconnect3(pTestInfo);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFullDisconnect"))
	{
		TEST_FAILED;
		LogAllErrorsVer3(henv,hdbc,hstmt[0]);
	}
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLAllocHandle.\n"));

	free_list(var_list);
	TEST_RETURN;
}
