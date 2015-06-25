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

#define DRVC_LEN 1024
//=========================================================//
//                                                         //
//                    TESTSQLDRIVERCONNECT                 //
//                                                         //
//=========================================================//

PassFail TestSQLDriverConnect(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
//	HWND		Myhwnd;
	SQLHANDLE 	henv;
	SQLHANDLE 	hdbc, badhdbc, hdbc1[NUM_CONN_HND];
	TCHAR		szConnStrIn[DRVC_LEN], szConnStrOut[DRVC_LEN];
	TCHAR		connstr[DRVC_LEN], connstr1[DRVC_LEN];
	SWORD		cbConnStrOut;
	int i = 0; 
//==========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLDriverConnect.\n"));

	TEST_INIT;

//  Myhwnd = GetTopWindow((HWND)NULL);
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,pTestInfo->DataSource);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,pTestInfo->Password);
	_tcscat(connstr,_T(";"));
	_tcscpy(szConnStrIn,_T(""));
	_tcscat(szConnStrIn,connstr);

//==========================================================================================
  
	TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: Invalid CONN handle pointer\n");
	badhdbc = (SQLHANDLE)NULL;
	returncode = SQLDriverConnect(badhdbc,NULL,(SQLTCHAR*)szConnStrIn,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)NULL,(SQLHANDLE)badhdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(badhdbc);
    TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: NULL szConnStrIn\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,NULL,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
  TESTCASE_END;

//==========================================================================================
 
  TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: only DSN\n");
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,pTestInfo->DataSource);
	_tcscat(connstr,_T(";"));
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)connstr,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: only USER\n");
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	returncode = SQLAllocEnv(&henv);                 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)connstr,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END; 
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: only PASSWORD\n");
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,pTestInfo->Password);
	_tcscat(connstr,_T(";"));
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)connstr,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: Invalid szConnStrIn length\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)szConnStrIn,(SWORD)(_tcslen(szConnStrIn)/2),(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: zero length\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)szConnStrIn,0,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: Invalid DSN\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,_T("baddsn"));
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,pTestInfo->Password);
	_tcscat(connstr,_T(";"));

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)connstr,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: Invalid Password\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,pTestInfo->DataSource);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,_T("badpswd"));
	_tcscat(connstr,_T(";"));

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)connstr,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}

	LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLDriverConnect with SQL_NTS\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}
	//build expected DriverConnect string
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,pTestInfo->DataSource);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("SERVER="));
	_tcscat(connstr,pTestInfo->Server);
	_tcscat(connstr,_T("/"));
	_tcscat(connstr,pTestInfo->Port);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,pTestInfo->Password);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("CATALOG="));
	if (_tcslen(pTestInfo->Catalog) == 0)
		_tcscat(connstr, _T("TRAFODION"));
	else
		_tcscat(connstr,pTestInfo->Catalog);
	_tcscat(connstr,_T(";"));

        // connstr1 is to deal with the difference when the returned schema 
        // name contains the catalog name.
	_tcscpy(connstr1, connstr);

	_tcscat(connstr,_T("SCHEMA="));
	_tcscat(connstr,pTestInfo->Schema);
	_tcscat(connstr,_T(";"));

        // connstr1 is to deal with the difference when the returned schema
        // name contains the catalog name.
	if (_tcsstr(pTestInfo->Schema, _T(".")) != NULL)
	  // pTestInfo->Schema already has catalog name.  connstr1 will be
          // the same as connstr
	  _tcscpy(connstr1, connstr);
        else 	
	  {
            // added the catalog name to connstr1
            _tcscat(connstr1,_T("SCHEMA="));
            _tcscat(connstr1,pTestInfo->Catalog);
            _tcscat(connstr1,_T("."));
            _tcscat(connstr1,pTestInfo->Schema);
            _tcscat(connstr1,_T(";"));
          }

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)szConnStrIn,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}

    // connstr1 is to deal with the difference when the returned schema
    // name contains the catalog name.
    if (_tcsncmp(connstr,szConnStrOut,cbConnStrOut) != 0 &&
        _tcsncmp(connstr1,szConnStrOut,cbConnStrOut) != 0)
	{
		TEST_FAILED;
		LogMsg(ERRMSG,_T("Connnection Strings expect: %s and actual: %s are not matched.\n"),connstr,szConnStrOut);
	}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLDriverConnect with _tcslen\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)szConnStrIn,_tcslen(szConnStrIn),(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}
	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
	TESTCASE_END;

//==========================================================================================
  
	TESTCASE_BEGIN("Test Positive Functionality of SQLDriverConnect with different connection handles\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}
	for (i = 0; i < NUM_CONN_HND; i++){
		returncode = SQLAllocConnect(henv, &hdbc1[i]);    // Connection handle  
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc1[i],(SQLHANDLE)NULL);
			TEST_FAILED;
			TEST_RETURN;
			}

		returncode = SQLDriverConnect(hdbc1[i],NULL,(SQLTCHAR*)szConnStrIn,SQL_NTS,(SQLTCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDriverConnect")){
			TEST_FAILED;
			LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc1[i],(SQLHANDLE)NULL);
			}
		}
	for (i = 0; i < NUM_CONN_HND; i++){
		SQLDisconnect(hdbc1[i]);
		SQLFreeConnect(hdbc1[i]);
		}
	SQLFreeEnv(henv);
	TESTCASE_END;

//==========================================================================================

 	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLDriverConnect.\n"));
  TEST_RETURN;

}

