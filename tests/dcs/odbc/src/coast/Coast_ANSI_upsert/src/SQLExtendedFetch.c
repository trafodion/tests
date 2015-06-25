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
#define BUFFER_SIZE 6
#define ARRAY_SIZE 10


/*
---------------------------------------------------------
   TestSQLExtendedFetch
---------------------------------------------------------
*/
PassFail TestSQLExtendedFetch(TestInfo *pTestInfo)
{                  
   TEST_DECLARE;
   RETCODE retcode;
   char  Heading[MAX_STRING_SIZE];
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLHANDLE	hstmt;

//   SQLINTEGER StrLen_or_IndPtr;
	char buff[300];
	SQLLEN cbBuff;

	typedef struct _Row {
		CHAR       A[BUFFER_SIZE];
		SQLLEN AInd;
		CHAR       B[BUFFER_SIZE];
		SQLLEN BInd;
		CHAR       C[BUFFER_SIZE];
		SQLLEN CInd;
		CHAR       D[BUFFER_SIZE];
		SQLLEN DInd;
		CHAR       E[BUFFER_SIZE];
		SQLLEN EInd;
		CHAR       F[BUFFER_SIZE];
		SQLLEN FInd;
	} Row;

	Row RowArray[ARRAY_SIZE];
	CHAR *ExecDirStr[17];

	SQLUSMALLINT   FetchStatusArray[ARRAY_SIZE];
	SQLULEN FetchProcessed;
	int iend = 13;
	int i;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLExtendedFetch", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping("SQLExtendedFetch_ExecDirStr_0", var_list);
	ExecDirStr[1] = var_mapping("SQLExtendedFetch_ExecDirStr_1", var_list);
	ExecDirStr[2] = var_mapping("SQLExtendedFetch_ExecDirStr_2", var_list);
	ExecDirStr[3] = var_mapping("SQLExtendedFetch_ExecDirStr_3", var_list);
	ExecDirStr[4] = var_mapping("SQLExtendedFetch_ExecDirStr_4", var_list);
	ExecDirStr[5] = var_mapping("SQLExtendedFetch_ExecDirStr_5", var_list);
	ExecDirStr[6] = var_mapping("SQLExtendedFetch_ExecDirStr_6", var_list);
	ExecDirStr[7] = var_mapping("SQLExtendedFetch_ExecDirStr_7", var_list);
	ExecDirStr[8] = var_mapping("SQLExtendedFetch_ExecDirStr_8", var_list);
	ExecDirStr[9] = var_mapping("SQLExtendedFetch_ExecDirStr_9", var_list);
	ExecDirStr[10] = var_mapping("SQLExtendedFetch_ExecDirStr_10", var_list);
	ExecDirStr[11] = var_mapping("SQLExtendedFetch_ExecDirStr_11", var_list);
	ExecDirStr[12] = var_mapping("SQLExtendedFetch_ExecDirStr_12", var_list);
	ExecDirStr[13] = var_mapping("SQLExtendedFetch_ExecDirStr_13", var_list);
	ExecDirStr[14] = var_mapping("SQLExtendedFetch_ExecDirStr_14", var_list);
	ExecDirStr[15] = var_mapping("SQLExtendedFetch_ExecDirStr_15", var_list);
	ExecDirStr[16] = var_mapping("SQLExtendedFetch_ExecDirStr_16", var_list);

//===========================================================================================================
     
    LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLExtendedFetch | SQLExtendedFetch | SQLExtendedFetch.c\n");
 
    TEST_INIT;
	   
	TESTCASE_BEGIN("Initializing SQLExtendedFetch test environment\n");

	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	retcode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt);	

	
	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[13],SQL_NTS); /* CLEANUP */
	for (i = 0; i <= (iend-1); i++)
	{
		sprintf(Heading,"Creating database for SQLExtendedfetch and executing\n");
		strcat(Heading, ExecDirStr[i]);
		strcat(Heading, "\n");
		TESTCASE_BEGIN(Heading);
		
		retcode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,retcode,"SQLExecDirect"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
			goto terminate;
		}
	}

	SQLSetStmtOption(hstmt, SQL_CONCURRENCY, SQL_CONCUR_READ_ONLY);
	SQLSetStmtOption(hstmt, SQL_CURSOR_TYPE, SQL_CURSOR_FORWARD_ONLY);
	SQLSetStmtOption(hstmt, SQL_ROWSET_SIZE, ARRAY_SIZE);
	SQLSetStmtOption(hstmt, SQL_BIND_TYPE, sizeof(Row));

	// Bind the parameters in row-wise fashion.
	SQLBindCol(hstmt, 1, SQL_C_CHAR, &RowArray[0].A, BUFFER_SIZE, &RowArray[0].AInd);
	SQLBindCol(hstmt, 2, SQL_C_CHAR, &RowArray[0].B, BUFFER_SIZE, &RowArray[0].BInd);
	SQLBindCol(hstmt, 3, SQL_C_CHAR, &RowArray[0].C, BUFFER_SIZE, &RowArray[0].CInd);
	SQLBindCol(hstmt, 4, SQL_C_CHAR, &RowArray[0].D, BUFFER_SIZE, &RowArray[0].DInd);
	SQLBindCol(hstmt, 5, SQL_C_CHAR, &RowArray[0].E, BUFFER_SIZE, &RowArray[0].EInd);
	SQLBindCol(hstmt, 6, SQL_C_CHAR, &RowArray[0].F, BUFFER_SIZE, &RowArray[0].FInd);

	// Execute the select statement.
	retcode = SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[14], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLExecDirect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		goto terminate;
	}

	retcode = SQL_SUCCESS;

	while (retcode != SQL_NO_DATA_FOUND)
	{
		retcode = SQLExtendedFetch(hstmt, SQL_FETCH_NEXT, 1, &FetchProcessed, FetchStatusArray);
//		printf("Once Through %d \n", retcode);

		if (retcode == SQL_ERROR)
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
			goto terminate;
		}
		if (retcode == SQL_NO_DATA_FOUND) break;
	// Check to see which sets of parameters were processed successfully.
		for (i = 0; i < (int)FetchProcessed; i++) 
		{

			retcode = SQLSetPos(hstmt, i + 1, SQL_POSITION, SQL_LOCK_UNLOCK);
			if (retcode == SQL_ERROR)
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TEST_FAILED;
				goto terminate;
			}

			buff[0]=0;
//			LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Fetch Set  Status\n");
//			LogMsg(LINEBEFORE+SHORTTIMESTAMP,"------------- %d -------------\n",i);

			if (FetchStatusArray[i] == SQL_ROW_SUCCESS || 
				FetchStatusArray[i] == SQL_ROW_SUCCESS_WITH_INFO) 
			{
				int f = 0;
				TESTCASE_BEGIN("Checking the results\n");
				if (RowArray[i].AInd == SQL_NULL_DATA) {
					LogMsg(ERRMSG,"column 1: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 1, SQL_C_CHAR, buff, 300, &cbBuff);
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 1: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].A,buff) != 0) {
							LogMsg(ERRMSG,"column 1: expected: %s actual: %s\n",buff,RowArray[i].A);
							f = 1;
						}
				}

				if (RowArray[i].BInd == SQL_NULL_DATA) {
					LogMsg(ERRMSG,"column 2: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 2, SQL_C_CHAR, buff, 300, &cbBuff); 
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 2: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].B,buff) != 0) {
							LogMsg(ERRMSG,"column 2: expected: %s actual: %s\n",buff,RowArray[i].B);
							f = 1;
						}		
				}

				if (RowArray[i].CInd == SQL_NULL_DATA){
					LogMsg(ERRMSG,"column 3: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 3, SQL_C_CHAR, buff, 300, &cbBuff); 
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 3: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].C,buff) != 0) {
							LogMsg(ERRMSG,"column 3: expected: %s actual: %s\n",buff,RowArray[i].C);
							f = 1;
						}		
				}

				if (RowArray[i].DInd == SQL_NULL_DATA){
					LogMsg(ERRMSG,"column 4: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 4, SQL_C_CHAR, buff, 300, &cbBuff); 
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 4: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].D,buff) != 0) {
							LogMsg(ERRMSG,"column 4: expected: %s actual: %s\n",buff,RowArray[i].D);
							f = 1;
						}		
				}

				if (RowArray[i].EInd == SQL_NULL_DATA){
					LogMsg(ERRMSG,"column 5: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 5, SQL_C_CHAR, buff, 300, &cbBuff); 
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 5: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].E,buff) != 0) {
							LogMsg(ERRMSG,"column 5: expected: %s actual: %s\n",buff,RowArray[i].E);
							f = 1;
						}		
				}

				if (RowArray[i].FInd == SQL_NULL_DATA){
					LogMsg(ERRMSG,"column 6: expected: SQL_DATA_AT_EXEC, actual: SQL_NULL_DATA\n");
					f = 1;
				}
				else
				{
					retcode = SQLGetData(hstmt, 6, SQL_C_CHAR, buff, 300, &cbBuff); 
					if (retcode == SQL_NO_DATA) {
						LogMsg(ERRMSG,"column 6: expected: SQL_SUCCESS actual: SQL_NO_DATA\n");
						f = 1;
					}
					else
						if (strcmp(RowArray[i].F,buff) != 0) {
							LogMsg(ERRMSG,"column 6: expected: %s actual: %s\n",buff,RowArray[i].F);
							f = 1;
						}		
				}
				if (f == 1) {
					TEST_FAILED;
				}
				else {
					TESTCASE_END;
				}
			}
		}
	}
	TESTCASE_END;

//=============================================================================================
	// Test SQLExtendedFetch for empty data.
	for (i=0; i<2; i++) {
		SQLFreeStmt(hstmt, SQL_CLOSE);
		sprintf(Heading,"Select empty rows using SQLExtendedfetch\n");
		strcat(Heading, ExecDirStr[i+15]);
		strcat(Heading, "\n");
		TESTCASE_BEGIN(Heading);

		retcode = SQLPrepare(hstmt,(SQLCHAR*) ExecDirStr[i+15], SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,retcode,"SQLPrepare"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
			goto terminate;
		}

		retcode = SQLExecute(hstmt);
		if(!CHECKRC(SQL_SUCCESS,retcode,"SQLExecute"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
			goto terminate;
		}

		retcode = SQLExtendedFetch(hstmt, SQL_FETCH_NEXT, 1, &FetchProcessed, FetchStatusArray);
		if (retcode != SQL_NO_DATA_FOUND)
		{
			LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Return code %d, expected SQL_NO_DATA_FOUND\n", retcode);
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TEST_FAILED;
		}
	}

    TESTCASE_END;
   
//================================================================================================================
terminate:	
	SQLFreeStmt(hstmt, SQL_CLOSE);
	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[13],SQL_NTS); /* CLEANUP */
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLExtendedFetch.\n");
	FullDisconnect(pTestInfo);
	free_list(var_list);
	TEST_RETURN;
}
