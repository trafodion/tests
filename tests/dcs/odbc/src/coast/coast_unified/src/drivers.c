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
	TCHAR		szDRVDESC[DRVR_LEN], szDRVATTR[DRVR_LEN];
	SWORD		cbDRVDESC, pcbDRVATTR;

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLDrivers.\n"));

  TEST_INIT;

	//==========================================================================================
	   
  TESTCASE_BEGIN("Test the positive functionality of SQLDrivers\n");
 	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if (returncode == SQL_SUCCESS)
	{
		returncode = SQLDrivers(henv, SQL_FETCH_FIRST, (SQLTCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLTCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test SQLDrivers => SQL_FETCH_FIRST failed.\n"));
		}
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLDrivers(henv, SQL_FETCH_NEXT, (SQLTCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLTCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
			if((returncode != SQL_SUCCESS) && (returncode != SQL_NO_DATA_FOUND))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test SQLDrivers => SQL_FETCH_NEXT failed.\n"));
			}
		}
		returncode = SQLDrivers(henv, SQL_FETCH_FIRST, (SQLTCHAR*)szDRVDESC, DRVR_LEN, &cbDRVDESC, (SQLTCHAR*)szDRVATTR, DRVR_LEN, &pcbDRVATTR); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDataSources"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test SQLDrivers => SQL_FETCH_FIRST failed.\n"));
		}
	}
	SQLFreeEnv(henv);
  TESTCASE_END;

	//==========================================================================================
      
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLDrivers.\n"));
  TEST_RETURN;
}

