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

#define	MAX_PARAMS		5
#define NUMROWS				200
#define	PREP_LEN			50
#define NAME_LEN			300
#define COLNAME_LEN		30
#define	RGB_MAX_LEN		50
#define MAX_COL				3
/*
------------------------------------------------------------------
   TestMXSQLSetConnectAttr: Tests SQLSetConnectAttr                     
------------------------------------------------------------------
*/
PassFail TestMXSQLSetConnectAttr(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
	char		Heading[MAX_STRING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc, hdbc1;
 	SQLHANDLE	hstmt, hstmt1;
	int			i, j;
	SQLINTEGER 	*StringLengthPtr = NULL;
	SQLUINTEGER pvParamInt = 0;
	char		TempBuf1[MAX_STRING_SIZE];
	char		TempBuf2[MAX_STRING_SIZE];
    int			MX_MP_SPECIFIC = MX_SPECIFIC;
	  
	struct {
		SQLUSMALLINT	Attribute;
		BOOL		DoGetConnectOption;					// Since GetConnectOption doesn't return SetStmtoptions
		SQLULEN	vParamInt[MAX_PARAMS+1];
	} OptionInt[] = {			 
// connection options
		{SQL_ACCESS_MODE,TRUE,SQL_MODE_READ_WRITE,SQL_MODE_READ_ONLY,999,},
		{SQL_AUTOCOMMIT,TRUE,SQL_AUTOCOMMIT_OFF,SQL_AUTOCOMMIT_ON,999,},
		{SQL_TXN_ISOLATION,TRUE,SQL_TXN_READ_UNCOMMITTED,SQL_TXN_READ_COMMITTED,SQL_TXN_REPEATABLE_READ,SQL_TXN_SERIALIZABLE,/*SQL_TXN_VERSIONING,*/999},
		{SQL_ASYNC_ENABLE,FALSE,SQL_ASYNC_ENABLE_ON,SQL_ASYNC_ENABLE_OFF,999,},
		{SQL_LOGIN_TIMEOUT,TRUE,1,0,999,},
		{999,}};
		
   	/* Set up some local variables to save on typing in longer ones */
	UWORD		k = 0,iatt = 0;
	SWORD		numcol = 0;
	SWORD		param = 0;
	CHAR		cn[COLNAME_LEN];
	SWORD		cl;
	SWORD		st;
	SQLULEN		cp;
	SWORD		cs, cnull;
	SQLLEN   	cbInput = SQL_NTS;
	SWORD		totalatt = 18; /* should be 18 for 2.0 driver */
	CHAR		rgbDesc[RGB_MAX_LEN];
	SWORD		pcbDesc;
	SQLLEN		pfDesc;
	UWORD		DescType[] = 
					{
						SQL_COLUMN_AUTO_INCREMENT,SQL_COLUMN_CASE_SENSITIVE,SQL_COLUMN_COUNT,
						SQL_COLUMN_DISPLAY_SIZE,SQL_COLUMN_LENGTH,SQL_COLUMN_MONEY,
						SQL_COLUMN_NULLABLE,SQL_COLUMN_PRECISION,SQL_COLUMN_SCALE,
						SQL_COLUMN_SEARCHABLE,SQL_COLUMN_TYPE,SQL_COLUMN_UNSIGNED,
						SQL_COLUMN_UPDATABLE,SQL_COLUMN_NAME,SQL_COLUMN_TYPE_NAME,
						SQL_COLUMN_OWNER_NAME,SQL_COLUMN_QUALIFIER_NAME,SQL_COLUMN_TABLE_NAME,
						SQL_COLUMN_LABEL
					};

	struct {
		char *DrpTab;
		char *CrtTab;
		char *InsTab;
		char *SelTab;
	} ExecDirStr[] = {
		{"--", "--", "--", "--"},
		{"--", "--", "--", "--"}
	};

	char		*TestAsync = "--";
	SQLSMALLINT	Type[] = {SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP};
	CHAR		*szInput[] = {"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","1993-12-30","11:45:23","1992-12-31 23:45:23.123456"};
	SQLUINTEGER	ColPrec[] = {254,254,10,10,5,10,7,15,15,10,8,26};
	SQLSMALLINT	ColScale[] = {0,0,5,5,0,0,0,0,0,0,0,0};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLSetConnectAttr", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0].DrpTab = var_mapping("SQLSetConnectAttr_ExecDirStr_DrpTab_0", var_list);
	ExecDirStr[0].CrtTab = var_mapping("SQLSetConnectAttr_ExecDirStr_CrtTab_0", var_list);
	ExecDirStr[0].InsTab = var_mapping("SQLSetConnectAttr_ExecDirStr_InsTab_0", var_list);
	ExecDirStr[0].SelTab = var_mapping("SQLSetConnectAttr_ExecDirStr_SelTab_0", var_list);

	ExecDirStr[1].DrpTab = var_mapping("SQLSetConnectAttr_ExecDirStr_DrpTab_1", var_list);
	ExecDirStr[1].CrtTab = var_mapping("SQLSetConnectAttr_ExecDirStr_CrtTab_1", var_list);
	ExecDirStr[1].InsTab = var_mapping("SQLSetConnectAttr_ExecDirStr_InsTab_1", var_list);
	ExecDirStr[1].SelTab = var_mapping("SQLSetConnectAttr_ExecDirStr_SelTab_1", var_list);

	szInput[0] = var_mapping("SQLSetConnectAttr_szInput_0", var_list);
	szInput[1] = var_mapping("SQLSetConnectAttr_szInput_1", var_list);

	TestAsync = var_mapping("SQLSetConnectAttr_TestAsync", var_list);
	
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLSetConnectionAttr/GetConnectionAttr | SQLGetConnectAttr | setgetconnattr.c\n");

	TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLSet/GetConnectionOption tests\n");
  	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	hstmt1 = (SQLHANDLE)pTestInfo->hstmt;
 
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)ExecDirStr[0].DrpTab,SQL_NTS); 
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].CrtTab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END; // end of setup

//==========================================================================================================
	for (i = 0; OptionInt[i].Attribute != 999; i++) 
	{
		for (j = 0; OptionInt[i].vParamInt[j] != 999; j++)
		{
			if (OptionInt[i].DoGetConnectOption == TRUE)
			{
				sprintf(Heading,"Test Positive functionality of SQLSetConnectAttr"
									" for %s and ParamValue: %s\n",
									ConnectionOptionToChar(OptionInt[i].Attribute,TempBuf1),
									ConnectionParamToChar(OptionInt[i].Attribute,OptionInt[i].vParamInt[j],TempBuf2));
			}
			else
			{
				sprintf(Heading,"Test Positive functionality of SQLSetConnectAttr"
									" for %s and ParamValue: %s\n",
									StatementOptionToChar(OptionInt[i].Attribute,TempBuf1),
									StatementParamToChar(OptionInt[i].Attribute,OptionInt[i].vParamInt[j],TempBuf2));
			}
			TESTCASE_BEGIN(Heading);

			returncode = SQLSetConnectAttr((SQLHANDLE)hdbc,OptionInt[i].Attribute,(void *)OptionInt[i].vParamInt[j],0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,(SQLHANDLE)NULL);
			}
			else
			{
				returncode = SQLGetConnectAttr((SQLHANDLE)hdbc,OptionInt[i].Attribute,&pvParamInt,0,StringLengthPtr);
				if ((returncode != SQL_SUCCESS) && (OptionInt[i].DoGetConnectOption != FALSE))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,(SQLHANDLE)NULL);
				}
				else
				{
					returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
					{
						TEST_FAILED;
						TEST_RETURN;
					}
					if ((OptionInt[i].vParamInt[j] == pvParamInt) || (OptionInt[i].DoGetConnectOption == FALSE))
					{
						LogMsg(NONE,"expect: %d and actual: %d are matched\n",OptionInt[i].vParamInt[j],pvParamInt);
						switch(OptionInt[i].Attribute) 
						{
							case SQL_ACCESS_MODE :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_MODE_READ_WRITE :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_MODE_READ_ONLY :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLSetConnectAttr((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE,0);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
										{
											TEST_FAILED;
											LogAllErrorsVer3(henv,hdbc,hstmt);
										}
										break;
								}
								break;
							case SQL_AUTOCOMMIT :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_AUTOCOMMIT_OFF :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLEndTran(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,SQL_COMMIT);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLEndTran"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLEndTran(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,SQL_ROLLBACK);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLEndTran"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_AUTOCOMMIT_ON :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
								}
								break;
							case SQL_LOGIN_TIMEOUT :
								returncode = SQLAllocHandle(SQL_HANDLE_DBC,(SQLHANDLE)henv,(SQLHANDLE *)&hdbc1);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
								{
									LogMsg(ERRMSG,"Unable to SQLAllocHandle\n");
									TEST_FAILED;
								}
								switch(OptionInt[i].vParamInt[j]) 
								{
									case 0 :
										returncode = SQLSetConnectAttr((SQLHANDLE)hdbc1,OptionInt[i].Attribute,(void *)OptionInt[i].vParamInt[j],0);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
										{
											LogAllErrorsVer3(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLCHAR*)pTestInfo->UserID,SQL_NTS,(SQLCHAR*)pTestInfo->Password,SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
										{
											LogAllErrorsVer3(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										break;
									case 1 :
										returncode = SQLSetConnectAttr((SQLHANDLE)hdbc1,OptionInt[i].Attribute,(void *)OptionInt[i].vParamInt[j],0);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr"))
										{
											LogAllErrorsVer3(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLCHAR*)pTestInfo->UserID,SQL_NTS,(SQLCHAR*)pTestInfo->Password,SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
										{
											LogAllErrorsVer3(henv,hdbc1,hstmt1);
/* sq: 1 sec is really short for SQL_LOGIN_TIMEOUT, often timeout error
 * IS seen here.  Let's not consider it as a test failure here.
 *
        TEST_FAILED;
 */
										}
										break;
								}
								SQLDisconnect((SQLHANDLE)hdbc1);
								SQLFreeHandle(SQL_HANDLE_DBC,(SQLHANDLE)hdbc1);
								break;

							// Statement options
		
							case SQL_ASYNC_ENABLE :
								
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_ASYNC_ENABLE_OFF :
										SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Create Table"))  )
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Drop Table"))  )
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_ASYNC_ENABLE_ON :
									/*	returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for PREPARE stmt of create table.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}

										}*/
										SQLFreeStmt(hstmt,SQL_CLOSE);

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for PREPARE stmt of create table.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecute(hstmt);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for EXECUTE stmt of create table.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLTables(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,(SQLCHAR *)"TABLE",SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLTABLES.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										if (MX_MP_SPECIFIC == MX_SPECIFIC)
										{
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												returncode = SQLTablePrivileges(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLTABLEPRIVILEGES.\n");
													LogAllErrorsVer3(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
											{
												LogAllErrorsVer3(henv,hdbc,hstmt);
												TEST_FAILED;
											}
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLColumns(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,(SQLCHAR *)"",SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLCOLUMNS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										if (MX_MP_SPECIFIC == MX_SPECIFIC)
										{
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												returncode = SQLColumnPrivileges(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,(SQLCHAR *)"",SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLCOLUMNPRIVILEGES.\n");
													LogAllErrorsVer3(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
											{
												LogAllErrorsVer3(henv,hdbc,hstmt);
												TEST_FAILED;
											}
										} 
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrimaryKeys(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPRIMARYKEYS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										/*returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLSpecialColumns(hstmt,SQL_BEST_ROWID,"",SQL_NTS,"",SQL_NTS,"TESTASYNC",SQL_NTS,SQL_SCOPE_CURROW,SQL_NULLABLE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLSPECIALCOLUMNS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										} */
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLStatistics(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,SQL_INDEX_UNIQUE,SQL_ENSURE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLSTATISTICS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										} 

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[1].InsTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPREPARE of INSERT.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLNumParams(hstmt, &param);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLNUMPARAMS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										if (MX_MP_SPECIFIC == MX_SPECIFIC)
										{
											for (k = 0; k < param; k++)
											{
												returncode = SQL_STILL_EXECUTING;
												while (returncode == SQL_STILL_EXECUTING)
												{
													returncode = SQLDescribeParam(hstmt,(SWORD)(k+1),&st,&cp,&cs,&cnull);
													if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
													{
														TEST_FAILED;
														LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLDESCRIBEPARAM of column : %d.\n",k+1);
														LogAllErrorsVer3(henv,hdbc,hstmt);
													}
												}
											}
										}
										for (k = 0; k < param; k++)
										{
											if (MX_MP_SPECIFIC == MX_SPECIFIC)
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[k],PREP_LEN,0,szInput[k],0,&cbInput);
											}
											else
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[k],ColPrec[k],ColScale[k],szInput[k],300,&cbInput);
											}

											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLBINDPARAM of column : %d.\n",k+1);
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecute(hstmt);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECUTE insert stmt.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].SelTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of a select stmt.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQL_STILL_EXECUTING;
										numcol = 0;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode=SQLNumResultCols(hstmt, &numcol); 
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLNUMRESULTCOLS.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										for (k = 0; k < numcol; k++)
										{
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												returncode = SQLDescribeCol(hstmt,(SWORD)(k+1),(SQLCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLDESCRIBECOL of column : %d.\n",k+1);
													LogAllErrorsVer3(henv,hdbc,hstmt);
												}
											}
										}
										for (k = 0; k < numcol; k++)
										{
											for (iatt = 0; iatt <= totalatt; iatt++)
											{
		 										strcpy(rgbDesc,"");
												pcbDesc = 0;
												pfDesc = 0;
												returncode = SQL_STILL_EXECUTING;
												while (returncode == SQL_STILL_EXECUTING)
												{
													returncode = SQLColAttributes(hstmt,(SWORD)(k+1),DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc);
													if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
													{
														TEST_FAILED;
														LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLCOLATTRIBUTES of column : %d.\n",k+1);
														LogAllErrorsVer3(henv,hdbc,hstmt);
													}
												}
											}
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLFetch(hstmt);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLFETCH.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of drop stmt.\n");
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										break; 
								}
								break;						
						}
						TESTCASE_END;
					}
					else
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",OptionInt[i].vParamInt[j],pvParamInt);
					}
					returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}
			}
		}	
	}	

	returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); 
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLSetConnectionAttr/GetConnectionAttr.\n");
	free_list(var_list);
	TEST_RETURN;
}
