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

