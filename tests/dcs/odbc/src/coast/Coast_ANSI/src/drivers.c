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

#define DRVR_LEN 300

/*
---------------------------------------------------------
  TestSQLDrivers
	No negative tests since this functionality is done at
	driver manager level.
---------------------------------------------------------
*/
PassFail TestSQLDrivers(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
 	SQLHANDLE 	henv;
	char		szDRVDESC[DRVR_LEN], szDRVATTR[DRVR_LEN];
	SWORD		cbDRVDESC, pcbDRVATTR;

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLDrivers | SQLDrivers | drivers.c\n");

  TEST_INIT;

	//==========================================================================================
	   
  TESTCASE_BEGIN("Test the positive functionality of SQLDrivers\n");
 	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if (returncode == SQL_SUCCESS)
	{
		returncode = SQLDrivers(henv, SQL_FETCH_FIRST, (SQLCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,"Test SQLDrivers => SQL_FETCH_FIRST failed.\n");
		}
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLDrivers(henv, SQL_FETCH_NEXT, (SQLCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
			if((returncode != SQL_SUCCESS) && (returncode != SQL_NO_DATA_FOUND))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"Test SQLDrivers => SQL_FETCH_NEXT failed.\n");
			}
		}
		returncode = SQLDrivers(henv, SQL_FETCH_FIRST, (SQLCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,"Test SQLDrivers => SQL_FETCH_FIRST failed.\n");
		}
	}
	SQLFreeEnv(henv);
  TESTCASE_END;

	//==========================================================================================
      
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLDrivers.\n");
  TEST_RETURN;
}

