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
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

#define SQL_START_NODE           4000
#define SQL_MODE_LOADER          4001
#define SQL_STREAMS_PER_SEG      4002
#define SQL_ATTR_SUG_ROWSET_SIZE 4003
#define SQL_LOADER_DELAYERROR    4004

#define ARRAY_SIZE 10

#define	SQLSTR_LEN	300

/*
---------------------------------------------------------
   TestHash2
---------------------------------------------------------
*/
PassFail TestHash2(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	SQLRETURN		returncode;      
	SQLHENV			henv = 0;
	SQLHDBC			hdbc = 0;
	SQLHSTMT		hstmt= 0;
	SQLUSMALLINT	ParamStatusArray[ARRAY_SIZE];
	SQLUSMALLINT	expParamStatusArray[ARRAY_SIZE];
	SQLUSMALLINT	lastExpParamStatusArray[ARRAY_SIZE];
	SQLULEN			lastParamsProcessed=ARRAY_SIZE, ParamsProcessed = 0;
	SQLLEN			rowcount = 0, expRowcount = 0, lastExpRowcount = 0;
	int				i,j,k,counter = 1, loopcount = 0;
	char			buffer[256];

	typedef struct {
    		char	num[15];	SQLLEN numLenOrInd;
    		char	val[15];	SQLLEN valLenOrInd;
	}nameStruct;
	nameStruct  nameArray1[ARRAY_SIZE];

	SQLUINTEGER mode = 1; 
	SQLUINTEGER startnode = 2;
	SQLUINTEGER streams_per_node = 4;
	SQLUINTEGER delay_error = 1;
	SQLUINTEGER suggested_rowset_size=0;

	char sqlDrvInsert[] = "PLANLOADTABLE HASH2_TABLE";
	SQLCHAR *dropTbl = (SQLCHAR *)"DROP TABLE HASH2_TABLE cascade";
	SQLCHAR *crtTbl = (SQLCHAR *)"CREATE TABLE HASH2_TABLE (A int NOT NULL NOT DROPPABLE, B varchar(10), PRIMARY KEY (A))";				
	SQLCHAR *insTbl = (SQLCHAR *)"INSERT INTO HASH2_TABLE values (?,?)";
//	SQLCHAR *selTbl = (SQLCHAR *)"SELECT * HASH2_TABLE";

	//==================================================================================================
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing feature => Hash2.\n");
	TEST_INIT;

	returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLAllocConnect( henv, &hdbc);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_ON,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	//==================================================================================================
	// Set Mode to Loader
	returncode = SQLSetConnectAttr(hdbc, SQL_MODE_LOADER, (void *) mode, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_MODE_LOADER"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Set Start mode
	returncode = SQLSetConnectAttr(hdbc,  SQL_START_NODE,  (void *) startnode,  0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_START_NODE"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Set Desired Streams Per Node
	returncode = SQLSetConnectAttr(hdbc,  SQL_STREAMS_PER_SEG,  (void *) streams_per_node,  0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_STREAMS_PER_SEG"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Set delay_error mode
	returncode = SQLSetConnectAttr(hdbc,  SQL_LOADER_DELAYERROR, (void *) delay_error, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_LOADER_DELAYERROR"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	//==================================================================================================

	returncode = SQLConnect(hdbc,
					   (SQLCHAR*)pTestInfo->DataSource,(SWORD)strlen(pTestInfo->DataSource),
					   (SQLCHAR*)pTestInfo->UserID,(SWORD)strlen(pTestInfo->UserID),
					   (SQLCHAR*)pTestInfo->Password,(SWORD)strlen(pTestInfo->Password)
					   );
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLAllocStmt(hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt, dropTbl, SQL_NTS);
	returncode = SQLExecDirect(hstmt, crtTbl, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLPrepare(hstmt, (SQLCHAR *) sqlDrvInsert, SQL_NTS);
	if (returncode != SQL_SUCCESS) {
		LogMsg(ERRMSG,"PLANLOADTABLE is expected to return SQL_SUCCESS, actual is %d\n", returncode);
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLGetConnectAttr(hdbc, SQL_ATTR_SUG_ROWSET_SIZE, &suggested_rowset_size, 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_SUG_ROWSET_SIZE"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	LogMsg(LINEAFTER,"suggested_rowset_size=%d\n", suggested_rowset_size);

	//==================================================================================================
	// Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use row-wise binding.
	returncode = SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, (void *)sizeof(nameStruct), 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_PARAM_BIND_TYPE"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	// Specify the number of elements in each parameter array.
	returncode = SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, (void *)ARRAY_SIZE, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_PARAMSET_SIZE"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	// Specify an array in which to return the status of each set of parameters.
	returncode = SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_PARAM_STATUS_PTR"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	// Specify an SQLUINTEGER value in which to return the number of sets of parameters processed.
	returncode = SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_PARAMS_PROCESSED_PTR"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLPrepare(hstmt, insTbl, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_INTEGER, 10, 0,
                 &nameArray1[0].num, 300, &nameArray1[0].numLenOrInd);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 10, 0,
                 &nameArray1[0].val, 300, &nameArray1[0].valLenOrInd);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	for (j=0; j<ARRAY_SIZE; j++) {
		lastExpParamStatusArray[j] = SQL_PARAM_SUCCESS;
		expParamStatusArray[j] = SQL_PARAM_SUCCESS;
	}

	//==================================================================================================
	TESTCASE_BEGIN("Test the positive functionality of Hash2, with delay_error mode ON.\n");
	loopcount = 4;
	k = 0;
	while ( k < (loopcount+1)) {
		expRowcount = 0;

		if (k==loopcount) { //Send a dummy rowsets to get the status array of the previous rowsets in delay-mode
			LogMsg(LINEAFTER,"Insert dummy rowsets with size=0\n");
			returncode = SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, (void *)0, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQL_ATTR_PARAMSET_SIZE"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
		else {
			sprintf(buffer, "Data inserted: ");
			for (j=0; j<ARRAY_SIZE; j++) {
				if ((j+1)%(3+2*k) == 0) {
					counter--;
					expParamStatusArray[j] = SQL_PARAM_ERROR;
				}
				else {
					expParamStatusArray[j] = SQL_PARAM_SUCCESS;
					expRowcount++;
				}
				sprintf(nameArray1[j].num,"%d",counter++);
				nameArray1[j].numLenOrInd = SQL_NTS;
				sprintf(nameArray1[j].val,"%s","chochet");
				nameArray1[j].valLenOrInd = SQL_NTS;
				strcat(buffer,nameArray1[j].num);
				strcat(buffer," ");
			}
			strcat(buffer,"\n");
		}
		LogMsg(NONE,"%s\n", buffer);

		returncode = SQLExecute(hstmt);
		if (delay_error == 1 && k != 0) {
			if(returncode != SQL_SUCCESS_WITH_INFO)
			{
				LogMsg(ERRMSG,"SQLExecute: returncode expected: SQL_SUCCESS_WITH_INFO, actual: %d at line=%d\n", returncode, __LINE__);
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
		else {
			if(returncode != SQL_SUCCESS)
			{
				LogMsg(ERRMSG,"SQLExecute: returncode expected: SQL_SUCCESS, actual: %d at line=%d\n", returncode, __LINE__);
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}

		if ((k == loopcount && ParamsProcessed != 0) || (k != loopcount && ParamsProcessed != ARRAY_SIZE)) {
			LogMsg(ERRMSG,"ParamsProcessed is not the same as rowset size from client, at line=%d\n", __LINE__);
			TEST_FAILED;
		}

		returncode = SQLRowCount(hstmt, &rowcount);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLRowCount"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		if (delay_error == 1) {
			if (lastExpRowcount != rowcount) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected Rowcount=%d, Actual Rowcount=%d\n", expRowcount, rowcount);
			}
			lastExpRowcount = expRowcount;

			LogMsg(NONE,"\n%d last rows processed, %d current rows processed, rowcount=%d\n", lastParamsProcessed, ParamsProcessed, rowcount);
			for (i = 0; i < (int)lastParamsProcessed; i++) {
   				LogMsg(NONE,"Parameter Set  Status\n");
				LogMsg(NONE,"-------------  -------------\n");
				if (ParamStatusArray[i] != lastExpParamStatusArray[i]) {
					TEST_FAILED;
					LogMsg(ERRMSG,"Param status array at row #%d is expected: %d, actual %d\n", i, lastExpParamStatusArray[i], ParamStatusArray[i]);
					continue;
				}
				switch (ParamStatusArray[i]) {
					case SQL_PARAM_SUCCESS:
					case SQL_PARAM_SUCCESS_WITH_INFO:
         					LogMsg(NONE,"%13d  Success\n", i);
         					break;

      					case SQL_PARAM_ERROR:
         					LogMsg(NONE,"%13d  Error  <-------\n", i);
         					break;

      					case SQL_PARAM_UNUSED:
        					LogMsg(NONE,"%13d  Not processed\n", i);
        					break;

     					case SQL_PARAM_DIAG_UNAVAILABLE:
         					LogMsg(NONE,"%13d  Unknown\n", i);
         					break;
   				}
			}
			LogMsg(NONE,"\n============================================================\n");
			lastParamsProcessed = ParamsProcessed;
			for (j=0; j<ARRAY_SIZE; j++) {
				lastExpParamStatusArray[j] = expParamStatusArray[j];
			}
		}
		else {
			if (expRowcount != rowcount) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected Rowcount=%d, Actual Rowcount=%d\n", expRowcount, rowcount);
			}

			LogMsg(NONE,"\n%d current rows processed, rowcount=%d\n", ParamsProcessed, rowcount);
			for (i = 0; i < (int)ParamsProcessed; i++) {
   				LogMsg(NONE,"Parameter Set  Status\n");
				LogMsg(NONE,"-------------  -------------\n");
				if (ParamStatusArray[i] != expParamStatusArray[i]) {
					TEST_FAILED;
					LogMsg(ERRMSG,"Param status array at row #%d is expected: %d, actual %d\n", i, expParamStatusArray[i], ParamStatusArray[i]);
					continue;
				}
				switch (ParamStatusArray[i]) {
					case SQL_PARAM_SUCCESS:
					case SQL_PARAM_SUCCESS_WITH_INFO:
         					LogMsg(NONE,"%13d  Success\n", i);
         					break;

      					case SQL_PARAM_ERROR:
         					LogMsg(NONE,"%13d  Error  <-------\n", i);
         					break;

      					case SQL_PARAM_UNUSED:
        					LogMsg(NONE,"%13d  Not processed\n", i);
        					break;

     					case SQL_PARAM_DIAG_UNAVAILABLE:
         					LogMsg(NONE,"%13d  Unknown\n", i);
         					break;
   				}
			}
			LogMsg(NONE,"\n============================================================\n");
		}
		k++;
	}
	TESTCASE_END;

	SQLFreeStmt( hstmt, SQL_CLOSE );
	SQLFreeStmt( hstmt, SQL_UNBIND );
	SQLDisconnect( hdbc );
	SQLFreeConnect( hdbc );
	SQLFreeEnv( henv );

	//==================================================================================================
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing feature => Hash2.\n");
	TEST_RETURN;
}
