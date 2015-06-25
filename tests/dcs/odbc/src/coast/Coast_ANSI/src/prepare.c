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
#define	PREP_LEN	50

PassFail TestSQLPrepare(TestInfo *pTestInfo)
{   
	TEST_DECLARE;

 	char			Heading[MAX_STRING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			*PrepStr[6];

	CHAR			*szInput[] = {"Insert char","Insert varchar"};
	SQLLEN	cbInput = SQL_NTS;
	SQLUSMALLINT	i;
	SQLSMALLINT	Type[] = {SQL_CHAR,SQL_VARCHAR};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLPrepare", charset_file);
	if (var_list == NULL) return FAILED;

	PrepStr[0] = var_mapping("SQLPrepare_PrepStr_0", var_list);
	PrepStr[1] = var_mapping("SQLPrepare_PrepStr_1", var_list);
	PrepStr[2] = var_mapping("SQLPrepare_PrepStr_2", var_list);
	PrepStr[3] = var_mapping("SQLPrepare_PrepStr_3", var_list);
	PrepStr[4] = var_mapping("SQLPrepare_PrepStr_4", var_list);
	PrepStr[5] = var_mapping("SQLPrepare_PrepStr_5", var_list);
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLPrepare | SQLPrepare | prepare.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLPrepare tests\n");

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

	TESTCASE_END;  // end of setup

	TESTCASE_BEGIN("Test Positive Functionality of SQLPrepare/SQLExecute\n");
	returncode=SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[0],strlen(PrepStr[0])); /* cleanup */
	returncode = SQLPrepare(hstmt,(SQLCHAR*)PrepStr[1],strlen(PrepStr[1]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}	
	TESTCASE_END;

	sprintf(Heading,"Test Positive Functionality of SQLPrepare/SQLExecute with SQL_NTS\n");
	TESTCASE_BEGIN(Heading);
	returncode=SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[0],SQL_NTS);	/* cleanup */
	returncode = SQLPrepare(hstmt,(SQLCHAR*)PrepStr[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}	
	TESTCASE_END;

	sprintf(Heading,"Test Positive Functionality of SQLPrepare then SQLExecute twice\n");
	TESTCASE_BEGIN(Heading);
	returncode = SQLPrepare(hstmt,(SQLCHAR*)PrepStr[2],strlen(PrepStr[2]));
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}	
	SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[0],strlen(PrepStr[0])); /* cleanup */
	TESTCASE_END;
		
	sprintf(Heading,"Test Positive Functionality of SQLPrepare with params\n");
	TESTCASE_BEGIN(Heading);
	SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[3],SQL_NTS); /* cleanup */
	returncode = SQLPrepare(hstmt,(SQLCHAR*)PrepStr[4],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		for (i = 0; i <= 1; i++)
		{
			returncode = SQLBindParameter(hstmt,(SWORD)(i+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[i],PREP_LEN,0,szInput[i],0,&cbInput);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		returncode = SQLExecute(hstmt); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}	
	SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[3],SQL_NTS); /* cleanup */
	TESTCASE_END;

	sprintf(Heading,"Test negative Functionality of SQLPrepare with strlen less than sqlstr\n");
	TESTCASE_BEGIN(Heading);
	SQLExecDirect(hstmt,(SQLCHAR*)PrepStr[0],SQL_NTS); /* cleanup */
	returncode = SQLPrepare(hstmt,(SQLCHAR*)PrepStr[1],(strlen(PrepStr[1])-5));
	if(!CHECKRC(SQL_ERROR,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	sprintf(Heading,"Test negative Functionality of SQLPrepare with invalid sqlstr\n");
	TESTCASE_BEGIN(Heading);
	returncode = SQLPrepare(hstmt,NULL,strlen(PrepStr[2]));
	if(!CHECKRC(SQL_ERROR,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	sprintf(Heading,"Test negative Functionality of SQLPrepare with invalid handle\n");
	TESTCASE_BEGIN(Heading);
	returncode = SQLPrepare((SQLHANDLE)NULL,(SQLCHAR*)PrepStr[2],strlen(PrepStr[2]));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLPrepare"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLPrepare.\n");

	free_list(var_list);

	TEST_RETURN;
}
