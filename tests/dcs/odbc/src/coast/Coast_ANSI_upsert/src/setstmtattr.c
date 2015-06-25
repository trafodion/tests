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
#include <sql.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	MAX_PARAMS		5
#define NUMROWS			200
#define	PREP_LEN		50
#define NAME_LEN		600
#define COLNAME_LEN		30
#define	RGB_MAX_LEN		50
#define MAX_COL			3

/*
------------------------------------------------------------------
   SQLSetStmtAttr: Tests SQLSet/GetStmtAttr                      
------------------------------------------------------------------
*/
PassFail TestMXSQLSetStmtAttr(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	char				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	int					i, j;
	SQLULEN 			pvParamInt64 = 235; 
	SQLUINTEGER			pvParamInt; 
	SQLUINTEGER			rowsfetched;
	char				TempBuf1[MAX_STRING_SIZE];
	char				TempBuf2[MAX_STRING_SIZE];
	CHAR				*colval[MAX_COL];
	void				*DescOut;
	SQLLEN	colvallen[MAX_COL];
	SQLINTEGER *StringLengthPtr;
    int MX_MP_SPECIFIC = MX_SPECIFIC;

struct {
		SQLINTEGER	fOption;
		SQLUINTEGER	vParamInt[MAX_PARAMS+1];
		} OptionInt[] = {
		{SQL_ATTR_MAX_ROWS,0,1,10,50,100,999},
		{SQL_ATTR_MAX_LENGTH,0,10,50,100,200,999},
/* sq: Since R2.5.1, if you set timeout smaller than 30 secs, the deafult
 * will be at least 30 secs.  Don't do 5 here, it will return 30 and cause a
 * mismatch. Do something at least bigger than 30.  Bug#3162
 */
		{SQL_ATTR_QUERY_TIMEOUT,/* sq 5 */ 40,0,999},
		{SQL_ATTR_CONCURRENCY,SQL_CONCUR_LOCK,/*SQL_CONCUR_ROWVER,SQL_CONCUR_VALUES,*/SQL_CONCUR_READ_ONLY,999},
		{SQL_ATTR_CURSOR_SCROLLABLE,/*SQL_SCROLLABLE,SQL_NONSCROLLABLE,*/999},
		{SQL_ATTR_CURSOR_SENSITIVITY,SQL_INSENSITIVE,SQL_SENSITIVE,SQL_UNSPECIFIED,999},
		{SQL_ATTR_CURSOR_TYPE,/*SQL_CURSOR_DYNAMIC,SQL_CURSOR_KEYSET_DRIVEN,SQL_CURSOR_STATIC,*/SQL_CURSOR_FORWARD_ONLY,999},
		{SQL_ATTR_ENABLE_AUTO_IPD,SQL_FALSE,SQL_TRUE,999},
		{SQL_ATTR_METADATA_ID,SQL_FALSE,SQL_TRUE,999},
		{SQL_ATTR_NOSCAN,SQL_NOSCAN_ON,SQL_NOSCAN_OFF,999},
		{SQL_ATTR_RETRIEVE_DATA,SQL_RD_OFF,SQL_RD_ON,999},
		{SQL_ATTR_SIMULATE_CURSOR,SQL_SC_UNIQUE,SQL_SC_TRY_UNIQUE,999},
		{SQL_ATTR_USE_BOOKMARKS,SQL_UB_VARIABLE,SQL_UB_OFF,999},
		{SQL_ATTR_ROW_ARRAY_SIZE,1,2,999},
		{SQL_ATTR_ROW_BIND_TYPE,SQL_BIND_BY_COLUMN,10,100,999},
		{SQL_ATTR_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON,SQL_ASYNC_ENABLE_OFF,999,},
//		{SQL_BIND_TYPE,SQL_BIND_BY_COLUMN,10,100,999,},
//		{SQL_KEYSET_SIZE,SQL_KEYSET_SIZE_DEFAULT,10,999,},
//		{SQL_ROWSET_SIZE,SQL_ROWSET_SIZE_DEFAULT,10,999,},
		{999,}};

	SQLINTEGER OptionDesc[] = {SQL_ATTR_APP_PARAM_DESC,SQL_ATTR_APP_ROW_DESC};

	UWORD		k = 0,iatt = 0;
	SWORD		numcol,col;
	SWORD		param;
	CHAR		cn[COLNAME_LEN];
	SWORD			cl;
	SWORD		st;
	SQLULEN 	cp;
	SWORD		cs, cnull;
	SQLLEN	cbInput = SQL_NTS;
	SQLLEN		InValue = SQL_DATA_AT_EXEC;
	SWORD		totalatt = 18; /* should be 18 for 2.0 driver */
	CHAR		rgbDesc[RGB_MAX_LEN];
	SWORD		pcbDesc;
	SQLLEN  	pfDesc;
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

	SQLSMALLINT	Type[] = {SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP};
	CHAR				*szInput[] = {"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","1993-12-30","11:45:23","1992-12-31 23:45:23.123456"};
	SQLUINTEGER	ColPrec[] = {254,254,10,10,5,10,7,15,15,10,8,26};
	SQLSMALLINT	ColScale[] = {0,0,5,5,0,0,0,0,0,0,0,0};

	struct {
		char *DrpTab;
		char *CrtTab;
		char *InsTab;
		char *SelTab;
	} ExecDirStr[3];

	char	*SelQuery[2];
	char	*QryTimeOut[3];
	int		qto;
	char	*MXTimeOutQry[10];
	char	*InsTmp,*InsCol,*InsVal3,*ParamDataValue,*TestAsync;
	char	*ParamDataQry[4]; 
	char	ParamDataCmp[NAME_LEN];
	CHAR		OutValue[NAME_LEN];
	SQLLEN   	OutValueLen;
	SQLPOINTER	pToken;
	SQLHDESC    hdesci,hdesce;
    SQLUINTEGER	DescInfoIntPtr;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLSetStmtAttr", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0].DrpTab = var_mapping("SQLSetStmtAttr_ExecDirStr_DrpTab_0", var_list);
	ExecDirStr[0].CrtTab = var_mapping("SQLSetStmtAttr_ExecDirStr_CrtTab_0", var_list);
	ExecDirStr[0].InsTab = var_mapping("SQLSetStmtAttr_ExecDirStr_InsTab_0", var_list);
	ExecDirStr[0].SelTab = var_mapping("SQLSetStmtAttr_ExecDirStr_SelTab_0", var_list);

	ExecDirStr[1].DrpTab = var_mapping("SQLSetStmtAttr_ExecDirStr_DrpTab_1", var_list);
	ExecDirStr[1].CrtTab = var_mapping("SQLSetStmtAttr_ExecDirStr_CrtTab_1", var_list);
	ExecDirStr[1].InsTab = var_mapping("SQLSetStmtAttr_ExecDirStr_InsTab_1", var_list);
	ExecDirStr[1].SelTab = var_mapping("SQLSetStmtAttr_ExecDirStr_SelTab_1", var_list);

	ExecDirStr[2].DrpTab = var_mapping("SQLSetStmtAttr_ExecDirStr_DrpTab_2", var_list);
	ExecDirStr[2].CrtTab = var_mapping("SQLSetStmtAttr_ExecDirStr_CrtTab_2", var_list);
	ExecDirStr[2].InsTab = var_mapping("SQLSetStmtAttr_ExecDirStr_InsTab_2", var_list);
	ExecDirStr[2].SelTab = var_mapping("SQLSetStmtAttr_ExecDirStr_SelTab_2", var_list);

	ParamDataQry[0] = var_mapping("SQLSetStmtAttr_ParamDataQry_0", var_list);
	ParamDataQry[1] = var_mapping("SQLSetStmtAttr_ParamDataQry_1", var_list);
	ParamDataQry[2] = var_mapping("SQLSetStmtAttr_ParamDataQry_2", var_list);
	ParamDataQry[3] = var_mapping("SQLSetStmtAttr_ParamDataQry_3", var_list);

	SelQuery[0] = var_mapping("SQLSetStmtAttr_SelQuery_0", var_list);
	SelQuery[1] = var_mapping("SQLSetStmtAttr_SelQuery_1", var_list);

	InsVal3 = var_mapping("SQLSetStmtAttr_InsVal3", var_list);

	szInput[0] = var_mapping("SQLSetStmtAttr_szInput_0", var_list);
	szInput[1] = var_mapping("SQLSetStmtAttr_szInput_1", var_list);

	ParamDataValue = var_mapping("SQLSetStmtAttr_ParamDataValue", var_list);
	TestAsync = var_mapping("SQLSetStmtAttr_TestAsync", var_list);

	MXTimeOutQry[0] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_0", var_list);
	MXTimeOutQry[1] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_1", var_list);
	MXTimeOutQry[2] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_2", var_list);
	MXTimeOutQry[3] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_3", var_list);
	MXTimeOutQry[4] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_4", var_list);
	MXTimeOutQry[5] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_5", var_list);
	MXTimeOutQry[6] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_6", var_list);
	MXTimeOutQry[7] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_7", var_list);
	MXTimeOutQry[8] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_8", var_list);
	MXTimeOutQry[9] = var_mapping("SQLSetStmtAttr_MXTimeOutQry_9", var_list);

	QryTimeOut[0] = var_mapping("SQLSetStmtAttr_QryTimeOut_0", var_list);
	QryTimeOut[1] = var_mapping("SQLSetStmtAttr_QryTimeOut_1", var_list);
	QryTimeOut[2] = var_mapping("SQLSetStmtAttr_QryTimeOut_2", var_list);
	
//===========================================================================================================
	/* Set up some local variables to save on typing in longer ones */
      
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLSetStatement/GetStatementAttr | SQLGetStmtAttr | setstmtattr.c\n");

	TEST_INIT;

//==========================================================================================================

	TESTCASE_BEGIN("Setup for SQLSet/GetStatementattribute tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	
	StringLengthPtr = (SQLINTEGER *)malloc(NAME_LEN);

//==============================================================================================================

	for (i = 0; OptionInt[i].fOption != 999; i++) 
	{
		for (j = 0; OptionInt[i].vParamInt[j] != 999; j++)
		{
			returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt);	
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
            strcpy(TempBuf1,(char*)"");
            strcpy(TempBuf2,(char*)"");
			sprintf(Heading,"Test Positive functionality of SQLSetStmtAttr "
									"for %s and ParamValue: %s\n",
									StatementOptionToChar(OptionInt[i].fOption,TempBuf1),
									StatementParamToChar(OptionInt[i].fOption,OptionInt[i].vParamInt[j],TempBuf2));
			TESTCASE_BEGIN(Heading);

			returncode = SQLSetStmtAttr(hstmt,OptionInt[i].fOption,(void *)OptionInt[i].vParamInt[j],0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOptions"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
#ifdef _LP64
               pvParamInt = 0;
			   pvParamInt64 = 0;
                if(OptionInt[i].fOption == SQL_MAX_ROWS ||
                   OptionInt[i].fOption == SQL_ATTR_ROW_ARRAY_SIZE ||
                   OptionInt[i].fOption == SQL_ATTR_MAX_LENGTH ||
                   OptionInt[i].fOption == SQL_MAX_LENGTH ||
                   OptionInt[i].fOption == SQL_ROWSET_SIZE ||
                  OptionInt[i].fOption == SQL_KEYSET_SIZE ||     // did not find this
                  OptionInt[i].fOption == SQL_ATTR_KEYSET_SIZE)
				   returncode = SQLGetStmtAttr(hstmt,OptionInt[i].fOption,&pvParamInt64,0,StringLengthPtr);
				else
				   returncode = SQLGetStmtAttr(hstmt,OptionInt[i].fOption,&pvParamInt,0,StringLengthPtr);
#else
				returncode = SQLGetStmtAttr(hstmt,OptionInt[i].fOption,&pvParamInt,0,StringLengthPtr);
#endif
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
#ifdef _LP64
                    if (pvParamInt != 0)
					   pvParamInt64 = pvParamInt;
					if (OptionInt[i].vParamInt[j] == pvParamInt64)
#else
					if (OptionInt[i].vParamInt[j] == pvParamInt)
#endif
					{					
						switch(OptionInt[i].fOption) 
						{
							case SQL_ATTR_CONCURRENCY :
							case SQL_ATTR_CURSOR_SCROLLABLE :
							case SQL_ATTR_CURSOR_SENSITIVITY :
							case SQL_ATTR_CURSOR_TYPE :
							case SQL_ATTR_ENABLE_AUTO_IPD :
							case SQL_ATTR_METADATA_ID :
							case SQL_ATTR_RETRIEVE_DATA :
							case SQL_ATTR_SIMULATE_CURSOR :
							case SQL_ATTR_USE_BOOKMARKS :
							case SQL_ATTR_ROW_ARRAY_SIZE :
								 break;
							case SQL_ATTR_ROW_BIND_TYPE :
								 returncode = SQLGetStmtAttr(hstmt,SQL_ATTR_APP_ROW_DESC,&hdesci,0,StringLengthPtr);
								 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
								 {
									TEST_FAILED;
									LogAllErrors(henv,hdbc,hstmt);
								 }
               			 		 returncode = SQLGetDescField(hdesci,0,SQL_DESC_BIND_TYPE,(SQLPOINTER)&DescInfoIntPtr,sizeof(DescInfoIntPtr),StringLengthPtr);
       							 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
								 {
									TEST_FAILED;
									LogAllErrors(henv,hdbc,hstmt);
								 }
								 if ( DescInfoIntPtr != OptionInt[i].vParamInt[j] )
   								 TEST_FAILED;
								 break;
							case SQL_QUERY_TIMEOUT :
								  if (MX_MP_SPECIFIC == MP_SPECIFIC)
								  {
									SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); 
									returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									else
									{
										returncode = SQLPrepare(hstmt,(SQLCHAR*)(SQLCHAR*)ExecDirStr[1].InsTab, SQL_NTS);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										for (k = 0; k < NUMROWS; k++)
										{
											returncode = SQLExecute(hstmt);
											if (returncode != SQL_SUCCESS)
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
												break;
											}
										}
										if (k < NUMROWS) break;

										SQLExecDirect(hstmt,(SQLCHAR*)QryTimeOut[0],SQL_NTS); 
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)QryTimeOut[1],SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
										}
									}
									switch(OptionInt[i].vParamInt[j]) 
									{
										case 0 :
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)QryTimeOut[2], SQL_NTS);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;						
										case 5 :
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)QryTimeOut[2], SQL_NTS);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;
									}
									SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); 
									SQLExecDirect(hstmt,(SQLCHAR*)QryTimeOut[0],SQL_NTS);
								}
								else
								{
									for (qto = 0; qto < 3; qto++)
									{
										SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[qto],SQL_NTS);	// cleanup
									}
									for (qto = 3; qto < 6; qto++)
									{
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[qto],SQL_NTS);	// create table
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
										}
									}
									if (qto < 6) break;

									returncode = SQLPrepare(hstmt,(SQLCHAR*)MXTimeOutQry[6], SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										break;
									}
									for (qto = 0; qto < 25; qto++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
										}
									}
									if (qto < 25) break;

									returncode = SQLPrepare(hstmt,(SQLCHAR*)MXTimeOutQry[7], SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										break;
									}
									for (qto = 0; qto < 10; qto++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
										}
									}
									if (qto < 10) break;

									switch(OptionInt[i].vParamInt[j]) 
									{
										case 0 :
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[8], SQL_NTS);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;						
										case 1 :
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[9], SQL_NTS);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}

											returncode = SQLSetStmtAttr(hstmt,SQL_ASYNC_ENABLE,(void *)SQL_ASYNC_ENABLE_ON,0);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											do
											{
												returncode = SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[9], SQL_NTS);
											}
											while (returncode == SQL_STILL_EXECUTING);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											/*do
											{
												returncode = SQLPrepare(hstmt,(SQLCHAR*)MXTimeOutQry[9], SQL_NTS);
											}
											while (returncode == SQL_STILL_EXECUTING);
											if (returncode == SQL_SUCCESS)
											{
												do
												{
													returncode = SQLPrepare(hstmt,(SQLCHAR*)MXTimeOutQry[9], SQL_NTS);
												}
												while (returncode == SQL_STILL_EXECUTING);
											}
											if(!CHECKRC(SQL_ERROR,returncode,"SQLPrepare/SQLExecute"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}*/
											returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_ASYNC_ENABLE,(void *)SQL_ASYNC_ENABLE_OFF,0);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
											{
												TEST_FAILED;
												LogAllErrors(henv,hdbc,hstmt);
											}
											break;
									}
									// Cleanup. Need to free the handle and allocate a new one to DROP the tables as the tables are in OPEN state.
									SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
									returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										TEST_RETURN;
									}
									for (qto = 0; qto < 3; qto++)
									{
										SQLExecDirect(hstmt,(SQLCHAR*)MXTimeOutQry[qto],SQL_NTS);	// cleanup
									}
								}
								break;						
							case SQL_MAX_ROWS :
								SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); 
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									TEST_RETURN;
								}
								else
								{
									returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[1].InsTab, SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										//TEST_RETURN;
									}
									for (k = 0; k < NUMROWS; k++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											TEST_RETURN;
										}
									}
									SQLFreeStmt(hstmt,SQL_CLOSE);
								}
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].SelTab, SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									rowsfetched = 0;
									while (returncode == SQL_SUCCESS)
									{
										returncode = SQLFetch(hstmt);
										if (returncode != SQL_SUCCESS && returncode != SQL_NO_DATA_FOUND)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										if (returncode == SQL_SUCCESS)
											rowsfetched = rowsfetched + 1;
									}
								}
								returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								switch(OptionInt[i].vParamInt[j]) 
								{
									case 0 :
										if (rowsfetched == NUMROWS)
											LogMsg(NONE,"expect: %d and actual: %d are matched\n",rowsfetched,NUMROWS);
										else
										{
											TEST_FAILED;
											LogMsg(NONE,"expect: %d and actual: %d are matched\n",rowsfetched,NUMROWS);
										}
										break;						
									case 1 :
									case 10 :
									case 50 :
									case 100 :
										if (rowsfetched == OptionInt[i].vParamInt[j])
											LogMsg(NONE,"expect: %d and actual: %d are matched\n",rowsfetched,OptionInt[i].vParamInt[j]);
										else
										{
											TEST_FAILED;
											LogMsg(ERRMSG,"expect: %d and actual: %d are matched\n",rowsfetched,OptionInt[i].vParamInt[j]);
										}
										break;
								}
								SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); 
								break;						
							case SQL_NOSCAN :
								if (MX_MP_SPECIFIC != MP_SPECIFIC)
								{
									LogMsg(NONE,"This Statement option: SQL_NOSCAN is not supported in MX driver.\n");
									break;
								}

								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_NOSCAN_OFF :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelQuery[0], SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;						
									case SQL_NOSCAN_ON :
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelQuery[1], SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
								}
								break;						
							case SQL_MAX_LENGTH :
								SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2].DrpTab,SQL_NTS); 
								LogMsg(NONE,"%s\n", ExecDirStr[2].CrtTab);
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2].CrtTab,SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									InsTmp = (char *)malloc(MAX_NOS_SIZE);
									InsCol = (char *)malloc(MAX_NOS_SIZE);
									strcpy(InsCol,"");
									strcat(InsCol,InsVal3);
									strcat(InsCol,InsVal3);
									strcat(InsCol,InsVal3);
									strcat(InsCol,InsVal3);
									strcat(InsCol,InsVal3);
									strcpy(InsTmp,"");
									strcat(InsTmp,ExecDirStr[2].InsTab);
									strcat(InsTmp,"'");
									strcat(InsTmp,InsCol);
									strcat(InsTmp,"','");
									strcat(InsTmp,InsCol);
									strcat(InsTmp,"','");
									strcat(InsTmp,InsCol);
									strcat(InsTmp,"')");
									LogMsg(NONE,"%s\n",InsTmp);
									returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTmp, SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLExecute(hstmt);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									SQLFreeStmt(hstmt,SQL_CLOSE);
								}
								// Tests Bindcol & Fetch
								LogMsg(NONE,"Test Bindcol Then Fetch.\n");
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2].SelTab, SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								numcol = 0;
								returncode = SQLNumResultCols(hstmt, &numcol);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									col = 0;
									while (col < numcol)
									{
										colval[col] = (char *)malloc(NAME_LEN);
										returncode = SQLBindCol(hstmt,(SWORD)(col+1),SQL_C_CHAR,colval[col],NAME_LEN,&colvallen[col]);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										col = col + 1;
									}
									col = 0;
									returncode = SQLFetch(hstmt);
									if ( returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									col = 0;
									while (col < numcol)
									{
										switch(OptionInt[i].vParamInt[j]) 
										{
											case 0 :
											if (strlen(colval[col]) == strlen(InsCol))
													LogMsg(NONE,"expect: %d and actual: %d are matched\n",strlen(InsCol),strlen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at: %d\n",strlen(InsCol),strlen(colval[col]),__LINE__);
												}
												break;						
											case 10 :
											case 50 :
											case 100 :
											case 200 :
												if (OptionInt[i].vParamInt[j] == strlen(colval[col]))
													LogMsg(NONE,"expect: %d and actual: %d are matched\n",OptionInt[i].vParamInt[j],strlen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at: %d\n",OptionInt[i].vParamInt[j],strlen(colval[col]),__LINE__);
													LogMsg(ERRMSG,"actual data: %s\n", colval[col]);
												}
												break;
										}
										free(colval[col]);
										col = col + 1;
									}
									returncode = SQLFreeStmt(hstmt,SQL_UNBIND);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}

								// Tests Fetch & GetData
								LogMsg(NONE,"Test Fetch Then GetData.\n");
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2].SelTab, SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								numcol = 0;
								returncode = SQLNumResultCols(hstmt, &numcol);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLFetch(hstmt);
									if ( returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									col = 0;
									while (col < numcol)
									{
										colval[col] = (char *)malloc(NAME_LEN);
										returncode = SQLGetData(hstmt,(SWORD)(col+1),SQL_C_CHAR,colval[col],NAME_LEN,&colvallen[col]);
										if( returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										col = col + 1;
									}
									col = 0;
									while (col < numcol)
									{
										switch(OptionInt[i].vParamInt[j]) 
										{
											case 0 :
												if (strlen(colval[col]) == strlen(InsCol))
													LogMsg(NONE,"expect: %d and actual: %d are matched\n",strlen(InsCol),strlen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at: %d\n",strlen(InsCol),strlen(colval[col]),__LINE__);
												}
												break;						
											case 10 :
											case 50 :
											case 100 :
											case 200 :
												if (OptionInt[i].vParamInt[j] == strlen(colval[col]))
													LogMsg(NONE,"expect: %d and actual: %d are matched\n",OptionInt[i].vParamInt[j],strlen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at: %d\n",OptionInt[i].vParamInt[j],strlen(colval[col]),__LINE__);
												}
												break;
										}
										free(colval[col]);
										col = col + 1;
									}
									returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}
								free(InsCol);
								free(InsTmp);
								SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2].DrpTab,SQL_NTS); 
								break;						
							case SQL_ASYNC_ENABLE :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_ASYNC_ENABLE_OFF :
										SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); // cleanup
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].CrtTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Create Table"))  )
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
										}
										returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].DrpTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Drop Table"))  )
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_ASYNC_ENABLE_ON :
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); // cleanup
										}
										SQLFreeStmt(hstmt,SQL_CLOSE);

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLCHAR*)(SQLCHAR*)ExecDirStr[0].CrtTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for PREPARE stmt of create table.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecute(hstmt);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for EXECUTE stmt of create table.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLTables(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,(SQLCHAR *)"TABLE",SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLTABLES.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											break;
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
													LogAllErrors(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
											{
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
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
													LogAllErrors(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
											{
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									/*	returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLSpecialColumns(hstmt,SQL_BEST_ROWID,"",SQL_NTS,"",SQL_NTS,TestAsync,SQL_NTS,SQL_SCOPE_CURROW,SQL_NULLABLE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLSPECIALCOLUMNS.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}*/
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLStatistics(hstmt,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)"",SQL_NTS,(SQLCHAR *)TestAsync,SQL_NTS,SQL_INDEX_UNIQUE,SQL_ENSURE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLSTATISTICS.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[0].InsTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPREPARE of INSERT.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLNumParams(hstmt, &param);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLNUMPARAMS.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										for (k = 0; k < param; k++)
										{
											if (MX_MP_SPECIFIC == MX_SPECIFIC)
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[k],PREP_LEN,0,szInput[k],0,&cbInput);
											}
											else
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[k],ColPrec[k],ColScale[k],szInput[k],NAME_LEN,&cbInput);
											}

											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLBINDPARAM of column : %d.\n",k+1);
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].SelTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of a select stmt.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										numcol = 0;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode=SQLNumResultCols(hstmt, &numcol); 
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLNUMRESULTCOLS.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

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
													LogAllErrors(henv,hdbc,hstmt);
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
														LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}

										// start of paramdata/putdata
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ParamDataQry[0],SQL_NTS); // cleanup
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ParamDataQry[1],SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for EXECDIRECT stmt of create table for paramdata/putdata.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLCHAR*)ParamDataQry[2],SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPREPARE of INSERT.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										InValue = SQL_DATA_AT_EXEC;
										if (MX_MP_SPECIFIC == MX_SPECIFIC)
										{
											returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,SQL_C_CHAR,SQL_LONGVARCHAR,NAME_LEN,0,NULL,0,&InValue);
										}
										else
										{
	//										returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,SQL_C_CHAR,Type[k],NAME_LEN,0,NULL,NAME_LEN,&InValue);
											returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,SQL_C_CHAR,SQL_LONGVARCHAR,NAME_LEN,0,NULL,NAME_LEN,&InValue);									
										}
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
										{
											TEST_FAILED;
											LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLBINDPARAM of column for ParamData/PutData.\n");
											LogAllErrors(henv,hdbc,hstmt);
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecute(hstmt);
											if (returncode != SQL_NEED_DATA)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECUTE insert stmt for ParamData/PutData.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_NEED_DATA) break;

										returncode = SQLParamData(hstmt,&pToken);
										if (returncode != SQL_NEED_DATA)
										{
											TEST_FAILED;
											LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPARAMDATA insert stmt for ParamData/PutData.\n");
											LogAllErrors(henv,hdbc,hstmt);
										}
										else
										{
											strcpy(ParamDataCmp,"");
											for (k = 0; k < 8; k++)
											{
												returncode = SQLPutData(hstmt,ParamDataValue,strlen(ParamDataValue));
												if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPUTDATA insert stmt for ParamData/PutData.\n");
													LogAllErrors(henv,hdbc,hstmt);
												}
												else
												{
													strcat(ParamDataCmp,ParamDataValue);
												}
											}
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												returncode = SQLParamData(hstmt,&pToken);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLPARAMDATA insert stmt for ParamData/PutData.\n");
													LogAllErrors(henv,hdbc,hstmt);
												}
											}
											if (returncode != SQL_SUCCESS) break;
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ParamDataQry[3],SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of a select stmt for ParamData/PutData.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLFetch(hstmt);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLFETCH after ParamData/PutData.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLGetData(hstmt,(SWORD)(1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLGetData after ParamData/PutData.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										if (_strnicmp(ParamDataCmp,OutValue,strlen(ParamDataCmp)) == 0)
										{
											LogMsg(NONE,"expect: %s and actual: %s are matched\n",ParamDataCmp,OutValue);
										}
										else
										{
											TEST_FAILED;	
											LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched at: %d\n",ParamDataCmp,OutValue,__LINE__);
										}
										returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ParamDataQry[0],SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of drop stmt.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;
									
										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0].DrpTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,"Test failed while executing ASYNC call for SQLEXECDIRECT of drop stmt.\n");
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
										if (returncode != SQL_SUCCESS) break;

										/*	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_ASYNC_ENABLE,(void *)SQL_ASYNC_ENABLE_OFF,0);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
										{
											TEST_FAILED;
											LogAllErrors(henv,hdbc,hstmt);
										}*/
										break;
								}
								break;						
						}
						LogMsg(NONE,"expect: %s and actual: %s are matched\n",
									StatementParamToChar(OptionInt[i].fOption,OptionInt[i].vParamInt[j],TempBuf1),
									StatementParamToChar(OptionInt[i].fOption,pvParamInt,TempBuf2));
						TESTCASE_END;
					}
					else
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at: %d\n",
									StatementParamToChar(OptionInt[i].fOption,OptionInt[i].vParamInt[j],TempBuf1),
									StatementParamToChar(OptionInt[i].fOption,pvParamInt,TempBuf2),__LINE__);
					}

				}
			}
			returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	}


//==============================================================================================================

	sprintf(Heading,"Test Positive functionality of SQLGetStmtAttr to test the descriptor attributes\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	for(i=0;i<2;i++)
	{
		returncode = SQLGetStmtAttr(hstmt,OptionDesc[i],&hdesci,0,StringLengthPtr);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
//		hdesci = pvParamInt;
		returncode = SQLAllocHandle(SQL_HANDLE_DESC, (SQLHANDLE)hdbc, &hdesce);	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLSetStmtAttr(hstmt,OptionDesc[i],(void *)hdesce,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOptions"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLGetStmtAttr(hstmt,OptionDesc[i],&DescOut,0,StringLengthPtr);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		if( DescOut != (void *)hdesce)
        TEST_FAILED;
		returncode = SQLSetStmtAttr(hstmt,OptionDesc[i],(void *)SQL_NULL_HANDLE,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOptions"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLGetStmtAttr(hstmt,OptionDesc[i],&DescOut,0,StringLengthPtr);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtOptions"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		if( DescOut != (void *)hdesci)
        TEST_FAILED;
	}
//==============================================================================================================
	
	sprintf(Heading,"Test Negative functionality of SQLSetStmtAttr for SQL_ASYNC_ENABLE with invalid param\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_ASYNC_ENABLE,(void *)3,0);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
		TESTCASE_END;
//==============================================================================================================

	sprintf(Heading,"Test Negative functionality of SQLSetStmtAttr for invalid option\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLSetStmtAttr(hstmt,50,0,0);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
		TESTCASE_END;

//==============================================================================================================

	sprintf(Heading,"Test Negative functionality of SQLSetStmtAttr with invalid stmt handle\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLSetStmtAttr((SQLHANDLE)NULL,OptionInt[0].fOption,0,0);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
		TESTCASE_END;

//==============================================================================================================

	sprintf(Heading,"Test Negative functionality of SQLGetStmtAttr for invalid option\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLGetStmtAttr(hstmt,50,&pvParamInt,0,StringLengthPtr);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLGetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
		TESTCASE_END;

//==============================================================================================================

	sprintf(Heading,"Test Negative functionality of SQLGetStmtAttr with invalid stmt handle\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLGetStmtAttr((SQLHANDLE)NULL,OptionInt[0].fOption,0,0,StringLengthPtr);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLGetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	TESTCASE_END;

//==============================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLSetStatement/GetStatement Attr.\n");
	free_list(var_list);
	TEST_RETURN;
}
