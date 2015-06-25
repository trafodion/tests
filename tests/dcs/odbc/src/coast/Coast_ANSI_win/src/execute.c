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
#define	EXEC_LEN			50
#define MAX_INSERTED_ROWS	50
#define MAX_SQLTYPES		13

/*
---------------------------------------------------------
   TestSQLExecute
---------------------------------------------------------
*/
PassFail TestSQLExecute(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{                  
	TEST_DECLARE;

 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			*ExecStr[15];
	CHAR			*szInput[] = {"Inst char","Inst vchar","1234.56789","1234.56789","1200","12000","123.45","123.45","123.45","1993-07-01","09:45:30","1993-08-02 08:44:31.001","120000","1234567890.56789","1234567890.456789","1234567890.456789","0.01234567890123456789","1234.56789","1234567890.56789","12345678901234567890.0123456789"};
	SQLLEN			cbInput = SQL_NTS;
	SQLUSMALLINT	i = 0;
	SQLSMALLINT		Type[] = {SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_BIGINT,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC};
	SQLUINTEGER		ColPrec[] = {254,254,10,10,5,10,7,15,15,10,8,26,19,19,19,128,128,10,18,30};
	SQLSMALLINT		ColScale[]= {0,0,5,5,0,0,0,0,0,0,0,0,0,0,6,0,128,5,5,10};
	short			CCharOutput1,CCharOutput2;
	SQLLEN			OutputLen1,OutputLen2;
	int				actual_insert=0,num_insert=0;
	SWORD			param = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLExecute", charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecStr[0] = var_mapping("SQLExecute_ExecStr_0", var_list);
	ExecStr[1] = var_mapping("SQLExecute_ExecStr_1", var_list);
	ExecStr[2] = var_mapping("SQLExecute_ExecStr_2", var_list);
	ExecStr[3] = var_mapping("SQLExecute_ExecStr_3", var_list);

	ExecStr[4] = var_mapping("SQLExecute_ExecStr_4", var_list);
	ExecStr[5] = var_mapping("SQLExecute_ExecStr_5", var_list);
	ExecStr[6] = var_mapping("SQLExecute_ExecStr_6", var_list); 
	ExecStr[7] = var_mapping("SQLExecute_ExecStr_7", var_list);
	ExecStr[8] = var_mapping("SQLExecute_ExecStr_8", var_list);
	ExecStr[9] = var_mapping("SQLExecute_ExecStr_9", var_list);
	ExecStr[10] = var_mapping("SQLExecute_ExecStr_10", var_list);
	ExecStr[11] = var_mapping("SQLExecute_ExecStr_11", var_list);
	ExecStr[12] = var_mapping("SQLExecute_ExecStr_12", var_list);
	ExecStr[13] = var_mapping("SQLExecute_ExecStr_13", var_list);
	ExecStr[14] = var_mapping("SQLExecute_ExecStr_14", var_list);

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLExecute | SQLExecute | execute.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLExecute tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode=SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[4],SQL_NTS);

	returncode=SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[5],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode=SQLExecDirect(hstmt,(SQLCHAR *)ExecStr[6],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode=SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[7],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode=SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[8],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	TESTCASE_END;  // end of setup

	TESTCASE_BEGIN("Test #1: Positive Functionality of SQLExecute\n");

	returncode = SQLPrepare(hstmt,(SQLCHAR *)ExecStr[9],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLBindCol(hstmt,1,SQL_C_SHORT,&CCharOutput1,0,&OutputLen1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLBindCol(hstmt,2,SQL_C_SHORT,&CCharOutput2,0,&OutputLen2);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	while (returncode != SQL_NO_DATA_FOUND)
	{
		returncode = SQLFetch(hstmt);
		if (returncode != SQL_NO_DATA_FOUND)
		{
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	}
	SQLFreeStmt(hstmt,SQL_CLOSE);
	returncode = SQLPrepare(hstmt,(SQLCHAR *)ExecStr[10],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	SQLFreeStmt(hstmt,SQL_CLOSE);
	SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[4],SQL_NTS); 
	TESTCASE_END;

	TESTCASE_BEGIN("Test #2: Positive Functionality of SQLExecute\n");
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[0],strlen(ExecStr[0])); /* cleanup */

	returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[1],strlen(ExecStr[1]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	TESTCASE_END;
	
	TESTCASE_BEGIN("Test #3: Positive Functionality of SQLExecute with SQL_NTS\n");
	returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[2],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	TESTCASE_END;

	TESTCASE_BEGIN("Test #4: Positive Functionality of SQLPrepare then SQLExecute twice\n");
	returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[2],strlen(ExecStr[2]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	returncode = SQLExecute(hstmt); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}

	TESTCASE_END;

	SQLFreeStmt(hstmt,SQL_CLOSE);
	SQLFreeStmt(hstmt,SQL_UNBIND);
	SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		
	TESTCASE_BEGIN("Test #5: Positive Functionality of SQLExecute with params\n");
	returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[3],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	else{
		for (i = 0; i <= 1; i++){
			    
			if (i==0) Type[0] = 1;	
			returncode = SQLBindParameter(hstmt,(SWORD)(i+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[i],EXEC_LEN,0,szInput[i],0,&cbInput);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter")){
				LogMsg(NONE,"Type[i]: %d  \n",Type[i]);
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				}
			
			}
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			}
		}
	TESTCASE_END;
		
	TESTCASE_BEGIN("Test #6: Negative Functionality of SQLExecute with less params\n");
	returncode = SQLFreeStmt(hstmt,SQL_DROP);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	else{
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")){
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			}
		else{
			returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[3],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				}
			else{
				returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,Type[0],EXEC_LEN,0,szInput[0],0,&cbInput);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter")){
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					}
				else{
					returncode = SQLExecute(hstmt); 
					if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
					}
				}	
			}
		}
	TESTCASE_END;

	TESTCASE_BEGIN("Test #7: Negative Functionality of SQLExecute with not prepared stmt\n");
	returncode = SQLFreeStmt(hstmt,SQL_DROP);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	else{
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")){
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			}
		else{
			returncode = SQLExecute(hstmt);
			if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute")){
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				}
			}
		}
	TESTCASE_END;

	TESTCASE_BEGIN("Test #8: Negative Functionality of SQLExecute with invalid handle\n");
	returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[2],strlen(ExecStr[2]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		}
	else{
		returncode = SQLExecute((SQLHANDLE)NULL); 
		if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLExecute")){
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			}
		}
	TESTCASE_END;

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[0],strlen(ExecStr[0])); /* cleanup */
 
	TESTCASE_BEGIN("Test #9: Stress Positive Functionality of SQLExecute.\n");
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[11],SQL_NTS);

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[12],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[13],SQL_NTS); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			actual_insert = 0;
			for (num_insert = 0; num_insert < MAX_INSERTED_ROWS; num_insert++)
			{
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
					actual_insert++;
			}
			if (actual_insert != MAX_INSERTED_ROWS)
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"failed to insert rows actual => %d & excepted => %d.\n",actual_insert,MAX_INSERTED_ROWS);
			}
		}
	}

	SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[11],SQL_NTS); 
	TESTCASE_END;
 
	TESTCASE_BEGIN("Test #10: Stress Positive Functionality of SQLExecute with Params.\n");
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[11],SQL_NTS); 

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[12],SQL_NTS); 
	//LogMsg(NONE,"ExecStr[12]: %s\n", ExecStr[12]);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[14],SQL_NTS); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			actual_insert = 0;
			returncode = SQLNumParams(hstmt, &param);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumParams"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			for (num_insert = 0; num_insert < MAX_INSERTED_ROWS; num_insert++)
			{
				for (i = 0; i < param; i++)
				{
					if (i==0) Type[0] = 1;

					if (MX_MP_SPECIFIC == MX_SPECIFIC)
					{
						returncode = SQLBindParameter(hstmt,(SWORD)(i+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[i],ColPrec[i],ColScale[i],szInput[i],0,&cbInput);
					}
					else
					{
						returncode = SQLBindParameter(hstmt,(SWORD)(i+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[i],ColPrec[i],ColScale[i],szInput[i],300,&cbInput);
					}
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
					actual_insert++;
			}
			if (actual_insert != MAX_INSERTED_ROWS)
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"failed to insert rows actual => %d & excepted => %d.\n",actual_insert,MAX_INSERTED_ROWS);
			}
		}
	}

	SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[11],SQL_NTS); 
	TESTCASE_END;

	TESTCASE_BEGIN("Test #11: Negative Functionality of SQLExecute with already existing table\n");
	returncode = SQLFreeStmt(hstmt,SQL_DROP);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	else
	{
		returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[0],strlen(ExecStr[0])); /* cleanup */
			returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecStr[1],strlen(ExecStr[1]));
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				returncode = SQLExecute(hstmt); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					returncode = SQLExecute(hstmt); 
					if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}
			}
			SQLExecDirect(hstmt,(SQLCHAR*)ExecStr[0],strlen(ExecStr[0])); /* cleanup */
		}
	}
	TESTCASE_END;

//=================================================================================================
	
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLExecute.\n");
	free_list(var_list);
	TEST_RETURN;
}
