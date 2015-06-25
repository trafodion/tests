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
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN		300
#define NUM_OUTPUTS		8
#define REM_LEN			254

/*
---------------------------------------------------------
   TestSQLProcedures
---------------------------------------------------------
*/
PassFail TestMXSQLProcedures(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
 	TCHAR			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
  	TCHAR			*ProcStr;
 	TCHAR           ProcName[NAME_LEN];
	SWORD			ProcType = SQL_PT_PROCEDURE;
	TCHAR			opqua[NAME_LEN],opowner[NAME_LEN],opname[NAME_LEN],oremark[REM_LEN];
	SWORD			onuminpar,onumoutpar,onumresset,optype;
	SQLLEN			opqualen,opownerlen,opnamelen,onuminparlen,onumoutparlen,onumressetlen,oremarklen,optypelen;

	char			tmpbuf[1024];
	TCHAR			*myTestSch;
	TCHAR			*createSchStr;
	TCHAR			*setSchStr;
	TCHAR			*dropSchStr;

	struct	
	{
		TCHAR		*DropProc;
		TCHAR		*CrtProc;
	} CreateProc[] = {
							{_T("DROP PROCEDURE N4210"),
							 _T("CREATE PROCEDURE N4210 (IN IN1 TIME) EXTERNAL NAME 'Procs.N4210' EXTERNAL PATH '/home/SQFQA/SPJRoot/spjrs/nci/spjrs.jar' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE")},
							{_T("DROP PROCEDURE N4260"),
							 _T("CREATE PROCEDURE N4260 (IN IN1 REAL, INOUT INOUT1 INTEGER) EXTERNAL NAME 'Procs.N4260' EXTERNAL PATH '/home/SQFQA/SPJRoot/spjrs/nci/spjrs.jar' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE")},
							{_T("DROP PROCEDURE N4261"),
 							 _T("CREATE PROCEDURE N4261 (IN IN1 NUMERIC, INOUT INOUT1 REAL) EXTERNAL NAME 'Procs.N4261' EXTERNAL PATH '/home/SQFQA/SPJRoot/spjrs/nci/spjrs.jar' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE")},
							{_T("DROP PROCEDURE N4264"),
 							 _T("CREATE PROCEDURE N4264 (IN IN1 VARCHAR(30), OUT OUT1 VARCHAR(45)) EXTERNAL NAME 'Procs.N4264' EXTERNAL PATH '/home/SQFQA/SPJRoot/spjrs/nci/spjrs.jar' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE")},	
							{_T("DROP PROCEDURE N4267"),
 							 _T("CREATE PROCEDURE N4267 (IN IN1 NUMERIC, INOUT INOUT1 REAL) EXTERNAL NAME 'Procs.N4267' EXTERNAL PATH '/home/SQFQA/SPJRoot/spjrs/nci/spjrs.jar' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE")},
							{_T("endloop"),_T("endloop")}
					};
	struct	
	{
		TCHAR		*ProcName;
		SDWORD	NumInParams;
		SDWORD	NumOutParams;
		SDWORD	NumResSet;
		TCHAR		*Remark;
	} Procedure[] = {
							{_T("N4210"),0,0,0,_T("")},
							{_T("N4260"),0,0,0,_T("")},
							{_T("N4261"),0,0,0,_T("")},
							{_T("N4264"),0,0,0,_T("")},
							{_T("N4267"),0,0,0,_T("")},
							{_T("endloop"),0,0,0,_T("")}
						};
	int	i = 0, k = 0;
	TCHAR	State[STATE_SIZE];
	SDWORD	NativeError;
	TCHAR	buf[MAX_STRING_SIZE];

//===========================================================================================================
// Initialization Test Case

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLProcedures.\n"));
	
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLProcedures tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
//		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
 	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect3(pTestInfo);
//		TEST_FAILED;
		TEST_RETURN;
	}
//	TESTCASE_END; 

	ProcStr = (TCHAR *)malloc(MAX_NOS_SIZE);

	myTestSch = (TCHAR *)malloc(MAX_NOS_SIZE);
	createSchStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	setSchStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	dropSchStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	_tcscpy (myTestSch, _T("ODBC_PROC_TEST"));
	_tcscpy (createSchStr, _T("create schema "));
	_tcscat (createSchStr, pTestInfo->Catalog);
	_tcscat (createSchStr, _T("."));
	_tcscat (createSchStr, myTestSch);
	_tcscpy (setSchStr, _T("set schema "));
	_tcscat (setSchStr, pTestInfo->Catalog);
	_tcscat (setSchStr, _T("."));
	_tcscat (setSchStr, myTestSch);
	_tcscpy (dropSchStr, _T("drop schema "));
	_tcscat (dropSchStr, pTestInfo->Catalog);
	_tcscat (dropSchStr, _T("."));
	_tcscat (dropSchStr, myTestSch);	
	_tcscat (dropSchStr, _T(" cascade"));
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) dropSchStr,SQL_NTS);
	// if(!CHECKRC(SQL_SUCCESS,returncode,"Drop Schema"))
	// {
	//	TEST_FAILED;
	//	LogAllErrors(henv,hdbc,hstmt);
	// }
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) createSchStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Create Schema"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) setSchStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Set Schema"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}

	while (_tcsicmp(CreateProc[i].DropProc,_T("endloop")) != 0)
	{
		_tcscpy(ProcStr,_T(""));
		_tcscat(ProcStr,CreateProc[i].DropProc);
		SQLExecDirect(hstmt,(SQLTCHAR*) ProcStr,SQL_NTS); // cleanup
		_tcscpy(ProcStr,_T(""));
		_tcscat(ProcStr,CreateProc[i].CrtProc);
		_stprintf(Heading,_T("Adding Procedure => "));
		_tcscat(Heading,ProcStr);
		_tcscat(Heading,_T("\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ProcStr,SQL_NTS);
		if(returncode != SQL_SUCCESS)
		{
			returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
			if (NativeError == -2013)
			{
				LogMsg(NONE, _T("Stored Procedures not supported\n"));
				_gTestCount--;
				free(ProcStr);
				FullDisconnect(pTestInfo);
				LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLProcedures.\n"));
				TEST_RETURN;
			}
			else
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		TESTCASE_END;
		i++;
	}
	
	_stprintf(Heading,_T("Test Positive Functionality of SQLProcedures \n"));
	TESTCASE_BEGINW(Heading);
	returncode = SQLProcedures(hstmt,(SQLTCHAR*)pTestInfo->Catalog,(SWORD)_tcslen(pTestInfo->Catalog),(SQLTCHAR*)/* SQ pTestInfo->Schema */ myTestSch,(SWORD)_tcslen(/* SQ pTestInfo->Schema */ myTestSch),(SQLTCHAR *)_T("%"),(SWORD)1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLProcedures"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	if (returncode == SQL_SUCCESS)
	{
		_tcscpy(opqua,_T(""));
		_tcscpy(opowner,_T(""));
		_tcscpy(opname,_T(""));
		onuminpar = 0;
		onumoutpar = 0;
		onumresset = 0;
		_tcscpy(oremark,_T(""));
		optype = 0;
		SQLBindCol(hstmt,1,SQL_C_TCHAR,opqua,NAME_LEN,&opqualen);
		SQLBindCol(hstmt,2,SQL_C_TCHAR,opowner,NAME_LEN,&opownerlen);
		SQLBindCol(hstmt,3,SQL_C_TCHAR,opname,NAME_LEN,&opnamelen);
		SQLBindCol(hstmt,4,SQL_C_SHORT,&onuminpar,0,&onuminparlen);
		SQLBindCol(hstmt,5,SQL_C_SHORT,&onumoutpar,0,&onumoutparlen);
		SQLBindCol(hstmt,6,SQL_C_SHORT,&onumresset,0,&onumressetlen);
		SQLBindCol(hstmt,7,SQL_C_TCHAR,oremark,NAME_LEN,&oremarklen);
		SQLBindCol(hstmt,8,SQL_C_SHORT,&optype,0,&optypelen);
		k = 0;
		i = 0;
		while (returncode == SQL_SUCCESS)
		{
			if(_tcscmp(Procedure[i].ProcName,_T("endloop")) == 0)
				break;
			returncode = SQLFetch(hstmt);
			if((returncode!=SQL_NO_DATA_FOUND) &&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				if (returncode == SQL_SUCCESS)
				{
					k++;
					_stprintf(Heading,_T("SQLProcedures: Comparing Results\n"));
					TESTCASE_BEGINW(Heading);
					if ((_tcsicmp(pTestInfo->Catalog,opqua) == 0) 
					&& (_tcsicmp(/* SQ pTestInfo->Schema */ myTestSch,opowner) == 0) 
					&& (_tcsicmp(Procedure[i].ProcName,opname) == 0) 
					&& (Procedure[i].NumInParams == onuminpar) 
					&& (Procedure[i].NumOutParams == onumoutpar) 
					&& (Procedure[i].NumResSet == onumresset) 
					&& (_tcsicmp(Procedure[i].Remark,oremark) == 0) 
					&& (ProcType == optype))
					{
						LogMsg(NONE,_T("Catalog Name expect: %s and actual: %s are matched\n"),pTestInfo->Catalog,opqua);
						LogMsg(NONE,_T("Schema Name expect: %s and actual: %s are matched\n"),/* SQ pTestInfo->Schema */ myTestSch,opowner);
						LogMsg(NONE,_T("ProcName expect: %s and actual: %s are matched\n"),Procedure[i].ProcName,opname);
						LogMsg(NONE,_T("NumInParams expect: %d and actual: %d are matched\n"),Procedure[i].NumInParams,onuminpar);
						LogMsg(NONE,_T("NumOutParams expect: %d and actual: %d are matched\n"),Procedure[i].NumOutParams,onumoutpar);
						LogMsg(NONE,_T("NumResSet expect: %d and actual: %d are matched\n"),Procedure[i].NumResSet, onumresset);
						LogMsg(NONE,_T("Remark expect: %s and actual: %s are matched\n"),Procedure[i].Remark,oremark);
						LogMsg(NONE,_T("ProcType expect: %d and actual: %d are matched\n"),ProcType,optype);
					}	
					else
					{
						TEST_FAILED;	
						if (_tcsicmp(pTestInfo->Catalog,opqua) != 0)
							LogMsg(ERRMSG,_T("Catalog Name expect: %s and actual: %s are not matched\n"),pTestInfo->Catalog,opqua);
						if (_tcsicmp(/* SQ pTestInfo->Schema */ myTestSch,opowner) != 0) 
							LogMsg(ERRMSG,_T("Schema Name expect: %s and actual: %s are not matched\n"),/* SQ pTestInfo->Schema */ myTestSch,opowner);
						if (_tcsicmp(Procedure[i].ProcName,opname) != 0) 
							LogMsg(ERRMSG,_T("ProcName expect: %s and actual: %s are not matched\n"),Procedure[i].ProcName,opname);
						if (Procedure[i].NumInParams != onuminpar) 
							LogMsg(ERRMSG,_T("NumInParams expect: %d and actual: %d are not matched\n"),Procedure[i].NumInParams,onuminpar);
						if (Procedure[i].NumOutParams != onumoutpar) 
							LogMsg(ERRMSG,_T("NumOutParams expect: %d and actual: %d are not matched\n"),Procedure[i].NumOutParams,onumoutpar);
						if (Procedure[i].NumResSet != onumresset) 
							LogMsg(ERRMSG,_T("NumResSet expect: %d and actual: %d are not matched\n"),Procedure[i].NumResSet, onumresset);
						if (_tcsicmp(Procedure[i].Remark,oremark) != 0) 
							LogMsg(ERRMSG,_T("Remark expect: %s and actual: %s are not matched\n"),Procedure[i].Remark,oremark);
						if (ProcType != optype)
							LogMsg(ERRMSG,_T("ProcType expect: %d and actual: %d are not matched\n"),ProcType,optype);
					}
				}
			}
			if(k == 0)
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
			}
			TESTCASE_END;
			i++;
		} // while
	}

	SQLFreeStmt(hstmt,SQL_UNBIND);
	SQLFreeStmt(hstmt,SQL_CLOSE);

	i=0;
	while (_tcsicmp(CreateProc[i].DropProc,_T("endloop")) != 0)
	{
		_tcscpy(ProcStr,_T(""));
		_tcscat(ProcStr,CreateProc[i].DropProc);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*) ProcStr,SQL_NTS); // cleanup	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		i++;
	}

	SQLFreeStmt(hstmt,SQL_UNBIND);
	SQLFreeStmt(hstmt,SQL_CLOSE);

	//========================================================================================================

	_stprintf(Heading,_T("SQLProcedures: Negative test with NULL handle\n"));
	TESTCASE_BEGINW(Heading);

	hstmt = (SQLHANDLE)NULL;
	_tcscpy(ProcName,_T("junkproc"));

	returncode = SQLProcedures(hstmt,(SQLTCHAR*)pTestInfo->Catalog,(SWORD)_tcslen(pTestInfo->Catalog),(SQLTCHAR*)/* SQ pTestInfo->Schema */ myTestSch,(SWORD)_tcslen(/* SQ pTestInfo->Schema */ myTestSch),(SQLTCHAR*)ProcName,(SWORD)_tcslen(ProcName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLProcedures"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	//========================================================================================================


	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) dropSchStr,SQL_NTS);

	free(ProcStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLProcedures.\n"));
	TEST_RETURN;
}
