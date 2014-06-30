#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include <sqlext.h>
#include <string.h>

/*
---------------------------------------------------------
   TestSQLMoreResults
---------------------------------------------------------
*/
PassFail TestSQLMoreResults(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
 	TCHAR			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	TCHAR			*SetupStr[] =  { _T("--"), _T("--"), _T("--"), _T("--"), _T("--"), _T("--"), _T("--"), _T("endloop") };
	TCHAR			*TestStr[] = { _T("--"), _T("--"), _T("--"), _T("--"), _T("--"),_T("endloop") };
	int				cnt, fail = 0;
//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLMoreResults"), charset_file);
	if (var_list == NULL) return FAILED;

	SetupStr[0] = var_mapping(_T("SQLMoreResults_SetupStr_0"), var_list);
	SetupStr[1] = var_mapping(_T("SQLMoreResults_SetupStr_1"), var_list);
	SetupStr[2] = var_mapping(_T("SQLMoreResults_SetupStr_2"), var_list);
	SetupStr[3] = var_mapping(_T("SQLMoreResults_SetupStr_3"), var_list);
	SetupStr[4] = var_mapping(_T("SQLMoreResults_SetupStr_4"), var_list);
	SetupStr[5] = var_mapping(_T("SQLMoreResults_SetupStr_5"), var_list);
	SetupStr[6] = var_mapping(_T("SQLMoreResults_SetupStr_6"), var_list);

	TestStr[0] = var_mapping(_T("SQLMoreResults_TestStr_0"), var_list);
	TestStr[1] = var_mapping(_T("SQLMoreResults_TestStr_1"), var_list);
	TestStr[2] = var_mapping(_T("SQLMoreResults_TestStr_2"), var_list);
	TestStr[3] = var_mapping(_T("SQLMoreResults_TestStr_3"), var_list);
	TestStr[4] = var_mapping(_T("SQLMoreResults_TestStr_4"), var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLMoreResults.\n"));

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
		cnt = 0;
		while (_tcsicmp(SetupStr[cnt],_T("endloop")) != 0)
		{
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*) SetupStr[cnt],SQL_NTS);
			if (returncode == SQL_ERROR)
				fail++;
			cnt++;
		}
		if (fail != cnt)
		{
			cnt = 0;
			while (_tcsicmp(TestStr[cnt],_T("endloop")) != 0)
			{
				_stprintf(Heading,_T("Positive Test SQLMoreResults for "));
				_tcscat(Heading,TestStr[cnt]);
				_tcscat(Heading,_T("\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TestStr[cnt],SQL_NTS);
				if (returncode == SQL_SUCCESS)
				{
					SQLFetch(hstmt);
					returncode=SQLMoreResults(hstmt);
					if(!CHECKRC(SQL_NO_DATA_FOUND,returncode,"SQLMoreResults"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				TESTCASE_END;
				cnt++;
			}
			SQLExecDirect(hstmt,(SQLTCHAR*)SetupStr[0],SQL_NTS); // CLEANUP 
			SQLExecDirect(hstmt,(SQLTCHAR*)SetupStr[1],SQL_NTS); // CLEANUP 
		}
	}

//==============================================================================*/

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLMoreResults.\n"));
	free_list(var_list);
	TEST_RETURN;
}
