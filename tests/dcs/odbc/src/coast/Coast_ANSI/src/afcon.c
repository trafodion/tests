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

/*
------------------------------------------------------------------
   TestSQLAllocConnect: Tests SQLAllocConnect and SQLFreeConnect                      
------------------------------------------------------------------
*/
PassFail TestSQLAllocConnect(TestInfo *pTestInfo)
{                  
   TEST_DECLARE;
   RETCODE returncode;
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLHANDLE Badhenv;
   SQLHANDLE Badhdbc;
   
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLAllocConnect | SQLAllocConnect | afcon.c\n");

  TEST_INIT;       


//===========================================================================   

  TESTCASE_BEGIN("Test basic functionality of SQLAllocConnect\n");
  henv=(SQLHANDLE)NULL;
  returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
      // Fatal error, no use running the remaining tests so, return 
		TEST_FAILED;
		TEST_RETURN;
  }
	
	returncode = SQLAllocConnect(henv,&hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
	{
      /* fatal error, no use continuing with tests */      
      TEST_FAILED;
      TEST_RETURN;
  }
  TESTCASE_END;

//===========================================================================   

  TESTCASE_BEGIN("Negative test: Invalid ENV handle pointer\n");
  Badhenv=(SQLHANDLE)NULL;
  returncode = SQLAllocConnect(Badhenv,&Badhdbc);
  if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLAllocConnect"))
	{
      TEST_FAILED;
	}
  TESTCASE_END;

//===========================================================================   

  TESTCASE_BEGIN("Negative test: Invalid ODBC handle pointer\n");
  Badhdbc=(SQLHANDLE)NULL;
  returncode = SQLAllocConnect(henv,(SQLHANDLE *)Badhdbc);
  if(!CHECKRC(SQL_ERROR,returncode,"SQLAllocConnect"))
	{
      TEST_FAILED;
	}                          
  TESTCASE_END;
     
//===========================================================================   

  TESTCASE_BEGIN("Test basic functionality of SQLFreeConnect\n");
  returncode = SQLFreeConnect(hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeConnect"))
	{
     TEST_FAILED;
     TEST_RETURN;
  }
  returncode = SQLFreeEnv(henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeConnect"))
	{
     TEST_FAILED;
     TEST_RETURN;
  }
  TESTCASE_END;

//===========================================================================   

/*		// this is a driver manager bug we cannot free already freed connect handle. 

  TESTCASE_BEGIN("Negative test: Free an already freed connection\n");
	returncode = SQLFreeConnect(hdbc);
  if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLFreeConnect"))
	{
      TEST_FAILED;
	}
  TESTCASE_END;
*/


//===========================================================================   

	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQAllocConnect.\n");
	TEST_RETURN;
}
