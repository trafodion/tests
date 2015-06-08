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
   
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLAllocConnect.\n"));

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

	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQAllocConnect.\n"));
	TEST_RETURN;
}
