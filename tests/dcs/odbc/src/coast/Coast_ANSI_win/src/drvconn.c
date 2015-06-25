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
	char		szConnStrIn[DRVC_LEN], szConnStrOut[DRVC_LEN];
	char		connstr[DRVC_LEN], connstr1[DRVC_LEN];
	SWORD		cbConnStrOut;
	int i = 0;   
//==========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLDriverConnect | SQLDriverConnect | drvconn.c\n");

	TEST_INIT;

//  Myhwnd = GetTopWindow((HWND)NULL);
	strcpy(connstr,"");
	strcat(connstr,"DSN=");
	strcat(connstr,pTestInfo->DataSource);
	strcat(connstr,";");
	strcat(connstr,"UID=");
	strcat(connstr,pTestInfo->UserID);
	strcat(connstr,";");
	strcat(connstr,"PWD=");
	strcat(connstr,pTestInfo->Password);
	strcat(connstr,";");
	strcpy(szConnStrIn,"");
	strcat(szConnStrIn,connstr);

//==========================================================================================
  
	TESTCASE_BEGIN("Test Negative Functionality of SQLDriverConnect: Invalid CONN handle pointer\n");
	badhdbc = (SQLHANDLE)NULL;
	returncode = SQLDriverConnect(badhdbc,NULL,(SQLCHAR*)szConnStrIn,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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

	returncode = SQLDriverConnect(hdbc,NULL,NULL,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"DSN=");
	strcat(connstr,pTestInfo->DataSource);
	strcat(connstr,";");
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)connstr,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"UID=");
	strcat(connstr,pTestInfo->UserID);
	strcat(connstr,";");
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)connstr,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"PWD=");
	strcat(connstr,pTestInfo->Password);
	strcat(connstr,";");
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)connstr,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)szConnStrIn,(SWORD)(strlen(szConnStrIn)/2),(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)szConnStrIn,0,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"DSN=");
	strcat(connstr,"baddsn");
	strcat(connstr,";");
	strcat(connstr,"UID=");
	strcat(connstr,pTestInfo->UserID);
	strcat(connstr,";");
	strcat(connstr,"PWD=");
	strcat(connstr,pTestInfo->Password);
	strcat(connstr,";");

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)connstr,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"DSN=");
	strcat(connstr,pTestInfo->DataSource);
	strcat(connstr,";");
	strcat(connstr,"UID=");
	strcat(connstr,pTestInfo->UserID);
	strcat(connstr,";");
	strcat(connstr,"PWD=");
	strcat(connstr,"badpswd");
	strcat(connstr,";");

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)connstr,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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
	strcpy(connstr,"");
	strcat(connstr,"DSN=");
	strcat(connstr,pTestInfo->DataSource);
	strcat(connstr,";");
	strcat(connstr,"SERVER=");
	strcat(connstr,pTestInfo->Server);
	strcat(connstr,"/");
	strcat(connstr,pTestInfo->Port);
	strcat(connstr,";");
	strcat(connstr,"UID=");
	strcat(connstr,pTestInfo->UserID);
	strcat(connstr,";");
	strcat(connstr,"PWD=");
	strcat(connstr,pTestInfo->Password);
	strcat(connstr,";");
	strcat(connstr,"CATALOG=");
	if (strlen(pTestInfo->Catalog) == 0)
		strcat(connstr, "TRAFODION");
	else
		strcat(connstr,pTestInfo->Catalog);
	strcat(connstr,";");

        // connstr1 is to deal with the difference when the returned schema
        // name contains the catalog name.
        strcpy(connstr1, connstr);

	strcat(connstr,"SCHEMA=");
	strcat(connstr,pTestInfo->Schema);
	strcat(connstr,";");

        // connstr1 is to deal with the difference when the returned schema
        // name contains the catalog name.
        if (strstr(pTestInfo->Schema, ".") != NULL)
          // pTestInfo->Schema already has catalog name.  connstr1 will be
          // the same as connstr
          strcpy(connstr1, connstr);
        else
          {
            // added the catalog name to connstr1
            strcat(connstr1,"SCHEMA=");
            strcat(connstr1,pTestInfo->Catalog);
            strcat(connstr1,".");
            strcat(connstr1,pTestInfo->Schema);
            strcat(connstr1,";");
          }

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)szConnStrIn,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDriverConnect")){
		TEST_FAILED;
		LogAllErrors((SQLHANDLE)henv,(SQLHANDLE)hdbc,(SQLHANDLE)NULL);
		}

    if (strncmp(connstr,szConnStrOut,cbConnStrOut) != 0 &&
        strncmp(connstr1,szConnStrOut,cbConnStrOut) != 0)
	{
		TEST_FAILED;
		LogMsg(ERRMSG,"Connnection Strings expect: %s and actual: %s are not matched.\n",connstr,szConnStrOut);
	}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLDriverConnect with strlen\n");
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

	returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)szConnStrIn,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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

		returncode = SQLDriverConnect(hdbc1[i],NULL,(SQLCHAR*)szConnStrIn,SQL_NTS,(SQLCHAR*)szConnStrOut,DRVC_LEN,&cbConnStrOut,SQL_DRIVER_NOPROMPT);
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

 	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLDriverConnect.\n");
  TEST_RETURN;

}

