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
#define MAX_NUM1		24
#define MAX_NUM2		16
#define NUM_FETCH_LOOP	5
#define ROWS_INSERTED	50

PassFail TestSQLFetch(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	char				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	SQLUSMALLINT		i, j, k, fn, h;
	SWORD				col;
	CHAR				*CCharOutput1[MAX_NUM1], CCharOutput2[NAME_LEN];
	SQLLEN				OutputLen1[MAX_NUM1], OutputLen2;
	SQLSMALLINT			CType[] = {SQL_C_CHAR};
	CHAR				*ExecDirStr[5];
    char                datastr1[MAX_STRING_SIZE];
    char                datastr2[MAX_STRING_SIZE];
    char                datastr3[MAX_STRING_SIZE];
	CHAR				*CResults[] = 
						{
#ifndef _WM
							"--","--","1234.56789","1234.56789","1200","12000",
							"12345.0","123450.0","1234500.0","1993-07-01","09:45:30",
							"1993-08-02 08:44:31.001000","120000",
							"1234567890123456789",
							"1234567890123.456789",
							"1234567890123456789012345678901234567890",
							"0.12345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
							"1234567890.1234567890123456789012345678901234567890000000000000000000000000",
							"12345.56789",
							"1234567890123.56789",
							"12345678901234567890.0123456789",datastr1,datastr2,datastr3
#else
							"--","--","1234.56789","1234.56789","1200","12000",
							"12345.0","123450.0","1234500.0","93/07/01","09:45:30",
							"1993-08-02 08:44:31.001000","120000",
							"1234567890123456789",
							"1234567890123.456789",
							"1234567890123456789012345678901234567890",
							".12345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
							"1234567890.1234567890123456789012345678901234567890000000000000000000000000",
							"12345.56789",
							"1234567890123.56789",
							"12345678901234567890.0123456789",datastr1,datastr2,datastr3
#endif
								};

	CHAR				*FetchNStr[5];

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
	char *iso_level_cqd[] = {
		"control query default isolation_level 'READ_COMMITTED'",
		"control query default isolation_level 'READ_UNCOMMITTED'",
		"control query default isolation_level 'REPEATABLE_READ'",
		"control query default isolation_level 'SERIALIZABLE'",
		"endloop"
	};

	char *access_mode[] = {
		"default",
		"set transaction READ ONLY",
		"set transaction READ WRITE",
		"endloop"
	};

	CHAR *SQLString[4];	//"DROP TABLE YRWK_TY_POS_2";
						//"CREATE TABLE YRWK_TY_POS_2 ( C1 NUMERIC (9, 2) , C2 NUMERIC (9, 2)) NO PARTITION";
						//"INSERT INTO YRWK_TY_POS_2 VALUES (119.28, 6)";
						//"SELECT SUM(C1) + SUM(C2) FROM YRWK_TY_POS_2";

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLFetch", charset_file);
	if (var_list == NULL) return FAILED;

    ExecDirStr[1] = var_mapping("SQLFetch_ExecDirStr_2", var_list);
	ExecDirStr[2] = var_mapping("SQLFetch_ExecDirStr_3", var_list);

	ExecDirStr[0] = var_mapping("SQLFetch_ExecDirStr_1", var_list);
	ExecDirStr[3] = var_mapping("SQLFetch_ExecDirStr_4", var_list);
	ExecDirStr[4] = var_mapping("SQLFetch_ExecDirStr_5", var_list);

	CResults[0] = var_mapping("SQLFetch_CResults_1", var_list);
	CResults[1] = var_mapping("SQLFetch_CResults_2", var_list);

	FetchNStr[0] = var_mapping("SQLFetch_FetchNStr_1", var_list);
	FetchNStr[1] = var_mapping("SQLFetch_FetchNStr_2", var_list);
	FetchNStr[2] = var_mapping("SQLFetch_FetchNStr_3", var_list);
	FetchNStr[3] = var_mapping("SQLFetch_FetchNStr_4", var_list);
	FetchNStr[4] = var_mapping("SQLFetch_FetchNStr_5", var_list);

	SQLString[0] = var_mapping("SQLFetch_SQLString_0", var_list);
	SQLString[1] = var_mapping("SQLFetch_SQLString_1", var_list);
	SQLString[2] = var_mapping("SQLFetch_SQLString_2", var_list);
	SQLString[3] = var_mapping("SQLFetch_SQLString_3", var_list);

    strcpy(datastr1,var_mapping("SQLFetch_datastr1", var_list));
    strcpy(datastr2,var_mapping("SQLFetch_datastr2", var_list));
    strcpy(datastr3,var_mapping("SQLFetch_datastr3", var_list));

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLFetch | SQLFetch | fetch.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLFetch tests\n");

	if(!FullConnect(pTestInfo))
	{
		LogMsg(ERRMSG,"Unable to connect\n");
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

	SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; // end of setup

	for (i = 0; i < 1; i++)
	{ // begin of 1st for loop 
		sprintf(Heading,"Test 1.%d: Positive functionality of SQLFetch by doing SQLBindcol\n",i);
		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j=0; j<MAX_NUM1; j++)
		{
			CCharOutput1[j] = (char *)malloc(sizeof(char)*NAME_LEN);
			*(CCharOutput1[j])=(char)'\0';
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
				if (strcmp(CCharOutput1[j],CResults[j]) == 0)
				{
					//LogMsg(NONE,"expect: '%s' and actual: '%s' of column %d are matched\n",CResults[j],CCharOutput1[j],j+1);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: '%s' and actual: '%s' of column %d are not match, at line %d\n", CResults[j],CCharOutput1[j],j+1,__LINE__);
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
	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[4],SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;

	for (i = 0; i < 1; i++)
	{
		sprintf(Heading,"Test 2.%d: Positive functionality of SQLFetch by doing SQLGetData\n",i);
		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
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

				if (strcmp(CCharOutput2,CResults[j]) == 0)
				{
					//LogMsg(NONE,"expect: '%s' and actual: '%s' of column %d are matched\n", CResults[j],CCharOutput2,j+1);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: '%s' and actual: '%s' of column %d are not match, at line %d\n",CResults[j],CCharOutput2,j+1,__LINE__);
				}
			}
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		TESTCASE_END;
	} 
	
//============================================================================================

	for (fn = 0; fn < NUM_FETCH_LOOP; fn++)
	{
		sprintf(Heading,"Setup for Fetch %d tests\n",(ROWS_INSERTED*(fn+1)));
		TESTCASE_BEGIN(Heading);
		SQLFreeStmt(hstmt,SQL_DROP);
		SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
		SQLExecDirect(hstmt,(SQLCHAR*) FetchNStr[0],SQL_NTS); /* cleanup */
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)FetchNStr[1],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		for (i = 0; i < (ROWS_INSERTED*(fn+1)); i++)
		{ 
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)FetchNStr[2], SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
		TESTCASE_END; // end of setup

		sprintf(Heading,"Test Positive functionality of Fetch %d by doing SQLBindcol\n",(ROWS_INSERTED*(fn+1)));
		TESTCASE_BEGIN(Heading);
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
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)FetchNStr[3], SQL_NTS);
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
				CCharOutput1[j] = (char *)malloc(NAME_LEN);
				*(CCharOutput1[j])=(char)'\0';
				returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_CHAR,CCharOutput1[j],NAME_LEN,&OutputLen1[j]);
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
					    if (!FindError("00000",henv,hdbc,hstmt)) // SQLState should be "00000" when return code is SQL_NO_DATA_FOUND.
						{	
							TEST_FAILED;
							//assert(0);
							LogMsg(ERRMSG,"Rows #: %d : array %d suppose to be %d at line %d.\n",j,k, (ROWS_INSERTED*(fn+1)),__LINE__);
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
				//LogMsg(NONE,"Rows inserted Expected: %d and Actual: %d.\n",(ROWS_INSERTED*(fn+1)),j);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"Rows inserted Expected: %d and Actual: %d at line%d.\n",(ROWS_INSERTED*(fn+1)),j,__LINE__);
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
			LogMsg(NONE,"FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n",AccessTime[0],AccessTime[1]);
		}	
		else
		{
			TEST_FAILED;	
			LogMsg(ERRMSG,"FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n",AccessTime[0],AccessTime[1]);
		}
*/
		LogMsg(NONE,"FETCH ONE: %d millisecs and FETCH N: %d millisecs.\n",AccessTime[0],AccessTime[1]);
		TESTCASE_END;
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
		SQLSetConnectOption((SQLHANDLE)hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
		SQLExecDirect(hstmt,(SQLCHAR*) FetchNStr[0],SQL_NTS); /* cleanup */
	}
	SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */

//=====================================================================================================

	TESTCASE_BEGIN("Setup for SQLFetch isolation level tests\n");
	SQLFreeStmt(hstmt,SQL_DROP);
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS);/*clean up*/
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;

	i = 0; k = 0;
	while (_stricmp(iso_level_cqd[k],"endloop") != 0)
	{
		h = 0;
		while (_stricmp(access_mode[h],"endloop") != 0) {
			if (strstr(iso_level_cqd[k],"READ_UNCOMMITTED") != NULL && strstr(access_mode[h],"READ WRITE") != NULL) {
				h++;
				continue;
			}

			FullDisconnect(pTestInfo);

			sprintf(Heading, "Setup for SQLFetch with: %s\nAnd access-mode: %s\n", iso_level_cqd[k], access_mode[h]);
			TESTCASE_BEGIN(Heading);
			if(!FullConnect(pTestInfo))
			{
				LogMsg(ERRMSG,"Unable to connect\n");
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

			returncode = SQLExecDirect(hstmt,(SQLCHAR*)iso_level_cqd[k],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			if (_stricmp(access_mode[h],"default") != 0) {
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)access_mode[h],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
			}

			TESTCASE_END; // end of setup

			sprintf(Heading,"SQLFetch by doing SQLGetData\n");
			TESTCASE_BEGIN(Heading);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
                if(strstr(access_mode[h],"default") != NULL &&
                  (strstr(iso_level_cqd[k],"SERIALIZABLE") != NULL || strstr(iso_level_cqd[k],"REPEATABLE_READ") != NULL)) 
                    LogMsg(NONE,"No-fix scenario\n");
                else  
                    TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
            else 
            {
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

					    if (strcmp(CCharOutput2,CResults[j]) == 0)
					    {
						    //LogMsg(NONE,"expect: '%s' and actual: '%s' of column %d are matched\n",CResults[j],CCharOutput2,j+1);
					    }	
					    else
					    {
						    TEST_FAILED;	
						    LogMsg(ERRMSG,"expect: '%s' and actual: '%s' of column %d are not match, at line %d\n",CResults[j],CCharOutput2,j+1,__LINE__);
					    }
				    }
			    }
            }
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
			h++;
		}

		k++;
	}//End while

	SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */
	
//============================================================================================
	TESTCASE_BEGIN("Testcase for Mode_special_1\n");

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLString[0],SQL_NTS);

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLString[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLString[2],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLString[3],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLBindCol(hstmt,1,SQL_C_CHAR,CCharOutput2,300,NULL);
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
	if (strcmp(CCharOutput2,"125.2") == 0)
	{
		//LogMsg(NONE,"expect: '125.2' and actual: '%s' are matched\n",CCharOutput2);
	}	
	else
	{
		TEST_FAILED;	
		LogMsg(ERRMSG,"expect: '125.2' and actual: '%s' are not match, at line %d\n",CCharOutput2,__LINE__);
	}
#else
	if (strcmp(CCharOutput2,"125.28") == 0)
	{
		//LogMsg(NONE,"expect: '125.28' and actual: '%s' are matched\n",CCharOutput2);
	}	
	else
	{
		TEST_FAILED;	
		LogMsg(ERRMSG,"expect: '125.28' and actual: '%s' are not match, at line %d\n",CCharOutput2,__LINE__);
	}
#endif

//============================================================================================
	
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLFetch.\n");
	free_list(var_list);
	TEST_RETURN;
}
