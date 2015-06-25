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


#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define DSRC_LEN 300

/*
---------------------------------------------------------
   TestSQLDataSources
	No negative tests since this functionality is done at
	driver manager level.
---------------------------------------------------------
*/
PassFail TestSQLDataSources(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
 	SQLHANDLE 	henv;
	TCHAR		szDSN[DSRC_LEN], szDESC[DSRC_LEN];
	SWORD		cbDSN, pcbDESC;

 	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLDataSources.\n"));

  TEST_INIT;

	//==========================================================================================
	   
  TESTCASE_BEGIN("Test the positive functionality of SQLDataSources\n");
 	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if (returncode == SQL_SUCCESS)
	{
		returncode = SQLDataSources(henv, SQL_FETCH_FIRST, (SQLTCHAR*)szDSN, DSRC_LEN, &cbDSN, (SQLTCHAR*)szDESC, DSRC_LEN, &pcbDESC); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test SQLDataSources => SQL_FETCH_FIRST #1 failed.\n"));
		}
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLDataSources(henv, SQL_FETCH_NEXT, (SQLTCHAR*)szDSN, DSRC_LEN, &cbDSN, (SQLTCHAR*)szDESC, DSRC_LEN, &pcbDESC); 
			if((returncode != SQL_SUCCESS) && (returncode != SQL_NO_DATA_FOUND))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test SQLDataSources => SQL_FETCH_NEXT failed.\n"));
			}
		}
		returncode = SQLDataSources(henv, SQL_FETCH_FIRST, (SQLTCHAR*)szDSN, DSRC_LEN, &cbDSN, (SQLTCHAR*)szDESC, DSRC_LEN, &pcbDESC); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test SQLDataSources => SQL_FETCH_FIRST #2 failed.\n"));
		}
	}
	SQLFreeEnv(henv);
   TESTCASE_END;

	//==========================================================================================
      
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLDataSources.\n"));
   TEST_RETURN;
}

