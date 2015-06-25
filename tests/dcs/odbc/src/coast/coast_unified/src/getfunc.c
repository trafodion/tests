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
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	MAX_FUNC	72

/*
------------------------------------------------------------------
   TestSQLGetFunction: Tests SQLGetFunction                      
------------------------------------------------------------------
*/
PassFail TestSQLGetFunctions(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
	TCHAR Heading[MAX_STRING_SIZE];
	RETCODE		returncode;
	SQLHANDLE 	henv;
	SQLHANDLE 	hdbc;
	SQLHANDLE	hstmt;
	UWORD	fFunction;
	UWORD	fExists;
	UWORD	fALLExists[MAX_FUNC];
	int i;
   
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLGetFunctions.\n"));

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
	for (fFunction = 1; fFunction <= MAX_FUNC; fFunction++) /* fFunction = 0 will get all functions */
	{
		if (fFunction < 24 || fFunction > 39)
		{
			_stprintf(Heading,_T("Test basic positive functionality of SQLGetFunctions for Function: %d\n"),fFunction);
			TESTCASE_BEGINW(Heading);
				
			if (fFunction == 0)
	       		returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,fALLExists);
			else			
       			returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,&fExists);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetFunctions"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				if (fFunction == 0)
				{
					for (i = 0; i <= MAX_FUNC; i++)
						LogMsg(SHORTTIMESTAMP,_T("%d\n"),fALLExists[i]);
				}
				else						
				{
					LogMsg(SHORTTIMESTAMP,_T("%d\n"),fExists);
				}
				TESTCASE_END;
			}
		}	
	}

	for (fFunction = 1; fFunction <= MAX_FUNC; fFunction++) /* fFunction = 0 will get all functions */
	{
		if (fFunction < 24 || fFunction > 39)
		{
			_stprintf(Heading,_T("Test Positive functionality of SQLGetFunctions for Function: %d\nwith output as NULL\n"),fFunction);
			TESTCASE_BEGINW(Heading);
			if (fFunction == 0)
				returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,fALLExists);
			else			
				returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetFunctions"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
				TESTCASE_END;
		}	
	}

	hdbc = (SQLHANDLE)NULL;
	for (fFunction = 1; fFunction <= MAX_FUNC; fFunction++) /* fFunction = 0 will get all functions */
	{
		if (fFunction < 24 || fFunction > 39)
		{
			_stprintf(Heading,_T("Test negative functionality of SQLGetFunctions for Function: %d\nwith hdbc as NULL\n"),fFunction);
			TESTCASE_BEGINW(Heading);
			if (fFunction == 0)
       		returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,fALLExists);
			else			
     			returncode = SQLGetFunctions((SQLHANDLE)hdbc,fFunction,&fExists);
			if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLGetFunctions"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
				TESTCASE_END;
		}	
	}

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLGetFunctions.\n"));
	TEST_RETURN;
}
