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

/*
---------------------------------------------------------
   TestSQLNumParams
---------------------------------------------------------
*/
PassFail TestSQLNumParams(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	char			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	SWORD			param;
	CHAR			*ExecDirStr[] = {"--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"};
	char			*TestCase[] = {"after preparing stmt ",
									"after preparing & binding stmt ",
									"after preparing, binding & executing stmt ",
									"after preparing, binding, executing & fetching stmt "};

	int				lend = 4, iend = 6;
	SQLUSMALLINT	i = 0, j = 0, k = 0, l = 0;
	int				expparam[] = {1,3,6,9,2,4};
	SQLLEN			cbIn = SQL_NTS;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLNumparams", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping("SQLNumParams_ExecDirStr_0", var_list);
	ExecDirStr[1] = var_mapping("SQLNumParams_ExecDirStr_1", var_list);
	ExecDirStr[2] = var_mapping("SQLNumParams_ExecDirStr_2", var_list);
	ExecDirStr[3] = var_mapping("SQLNumParams_ExecDirStr_3", var_list);
	ExecDirStr[4] = var_mapping("SQLNumParams_ExecDirStr_4", var_list);
	ExecDirStr[5] = var_mapping("SQLNumParams_ExecDirStr_5", var_list);
	ExecDirStr[6] = var_mapping("SQLNumParams_ExecDirStr_6", var_list);
	ExecDirStr[7] = var_mapping("SQLNumParams_ExecDirStr_7", var_list);
	ExecDirStr[8] = var_mapping("SQLNumParams_ExecDirStr_8", var_list);
	ExecDirStr[9] = var_mapping("SQLNumParams_ExecDirStr_9", var_list);
	ExecDirStr[10] = var_mapping("SQLNumParams_ExecDirStr_10", var_list);
	ExecDirStr[11] = var_mapping("SQLNumParams_ExecDirStr_11", var_list);
	ExecDirStr[12] = var_mapping("SQLNumParams_ExecDirStr_12", var_list);
	ExecDirStr[13] = var_mapping("SQLNumParams_ExecDirStr_13", var_list);
	ExecDirStr[14] = var_mapping("SQLNumParams_ExecDirStr_14", var_list);
	ExecDirStr[15] = var_mapping("SQLNumParams_ExecDirStr_15", var_list);
	ExecDirStr[16] = var_mapping("SQLNumParams_ExecDirStr_16", var_list);
	ExecDirStr[17] = var_mapping("SQLNumParams_ExecDirStr_17", var_list);
	ExecDirStr[18] = var_mapping("SQLNumParams_ExecDirStr_18", var_list);
	ExecDirStr[19] = var_mapping("SQLNumParams_ExecDirStr_19", var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLNumParams | SQLNumParams | numpar.c\n");

	TEST_INIT;
	   
  returncode=FullConnect(pTestInfo);
  if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if (returncode == SQL_SUCCESS)
	{
		for (l = 0; l < lend; l++)
		{
			for (i = 0; i < iend; i++)
			{
				//==================================================================================
				SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend],SQL_NTS);
				if ((returncode == SQL_SUCCESS) && (i > 3))
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+2],SQL_NTS);
				if (returncode == SQL_SUCCESS)
				{
					sprintf(Heading,"Test Positive Functionality of SQLNumParams ");
					strcat(Heading, TestCase[l]);
					strcat(Heading, ExecDirStr[i+iend+iend]);
					strcat(Heading, "\n");
					TESTCASE_BEGIN(Heading);
					returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend], SQL_NTS);
					if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
					{
						if (returncode == SQL_SUCCESS_WITH_INFO) 
							LogAllErrors(henv,hdbc,hstmt);
						if ( l == 1)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQL_SUCCESS;
							else
								returncode = SQL_ERROR;
						}
						else if (l == 2)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQLExecute(hstmt);
							else
								returncode = SQL_ERROR;
						}
						else if (l == 3)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQLExecute(hstmt);
								if ((returncode == SQL_SUCCESS) && (i > 3))
									returncode = SQLFetch(hstmt);
						} 
						else
							returncode = SQL_SUCCESS;
						if (returncode == SQL_SUCCESS)
						{
							returncode = SQLNumParams(hstmt, &param);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumParams"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							if (param == expparam[i])
							{
								LogMsg(NONE,"expect: %d and actual: %d are matched\n",expparam[i], param);
								TESTCASE_END;
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(NONE,"expect: %d and actual: %d are not matched\n",expparam[i], param);
							}
						}
						else
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					else
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				else
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[i],SQL_NTS); /* cleanup */
				//==================================================================================
			} /* for i loop */
		} /* for l loop */
	}

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLNumParams.\n");
	free_list(var_list);
	TEST_RETURN;
}
