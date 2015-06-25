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
---------------------------------------------------------
   TestSQLAllocEnv: Test SQLAllocEnv and SQLFreeEnv
---------------------------------------------------------
*/

PassFail TestSQLAllocEnv(TestInfo *pTestInfo)

{ 
	
	TEST_DECLARE;
  RETCODE returncode;
  SQLHANDLE henv;
  SQLHANDLE OldHenv;
  SQLHANDLE BadHenv;       
   
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLAllocEnvirnoment | SQLAllocEnv | afenv.c\n");

	TEST_INIT;
	   
  TESTCASE_BEGIN("Test basic functionality of SQLAllocEnv\n");
  henv=(SQLHANDLE)NULL;
  returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
      /* Fatal error, no use running the remaining tests so, return */
		TEST_FAILED;
		TEST_RETURN;
  }
  TESTCASE_END;
   
  TESTCASE_BEGIN("Test non-NULL handle value\n");
  OldHenv=henv;
  returncode=SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
     SQLFreeEnv(OldHenv);
     LogMsg(ENDLINE,"Using a valid, non-NULL handle caused an error.\n");
    /* Fatal error, no use running the remaining tests so, return */
    TEST_FAILED;
		TEST_RETURN;
  }
  TESTCASE_END;
   
  TESTCASE_BEGIN("Negative test: Invalid handle pointer\n");
  BadHenv=(SQLHANDLE)NULL;
  returncode=SQLAllocEnv((SQLHANDLE *)BadHenv);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLAllocEnv"))
	{
	   LogMsg(ENDLINE,"Invalid handle pointer works, it shouldn't.\n");
	   TEST_FAILED;
	}
  TESTCASE_END;

  TESTCASE_BEGIN("Test basic functionality of SQLFreeEnv\n");
  returncode=SQLFreeEnv(OldHenv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv"))
	{
    LogAllErrors(OldHenv,(SQLHANDLE)NULL,(SQLHANDLE)NULL);
		TEST_FAILED;
	}
      
  returncode=SQLFreeEnv(henv);   
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv"))
	{
    LogAllErrors(henv,(SQLHANDLE)NULL,(SQLHANDLE)NULL);
	  TEST_FAILED;
	}
  TESTCASE_END;
   
/*	// this is a bug in driver manager we cannot free already freed   
	TESTCASE_BEGIN("Negative test: free an already freed handle\n");
	returncode=SQLFreeEnv(henv);   
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLFreeEnv"))
	{
		LogMsg(ENDLINE,"Invalid handle didn't produce proper error.");
    TEST_FAILED
	}

	TESTCASE_END;
*/

	LogMsg(SHORTTIMESTAMP+LINEBEFORE+LINEAFTER,"End testing API => SQLAllocEnvirnoment.\n");
  TEST_RETURN;

}
