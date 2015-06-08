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
	TCHAR		Heading[MAX_STRING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc, hdbc1;
 	SQLHANDLE	hstmt, hstmt1;
	int			i, j;
	SQLINTEGER 	*StringLengthPtr = NULL;
	SQLUINTEGER pvParamInt = 0;
	TCHAR		TempBuf1[MAX_STRING_SIZE];
	TCHAR		TempBuf2[MAX_STRING_SIZE];
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
		{SQL_LOGIN_TIMEOUT,TRUE,60,0,999,},
		{999,}};
		
   	/* Set up some local variables to save on typing in longer ones */
	UWORD		k = 0,iatt = 0;
	SWORD		numcol = 0;
	SWORD		param = 0;
	TCHAR		cn[COLNAME_LEN];
	SWORD		cl;
	SWORD		st;
	SQLULEN		cp;
	SWORD		cs, cnull;
	SQLLEN   	cbInput = SQL_NTS;
	SWORD		totalatt = 18; /* should be 18 for 2.0 driver */
	TCHAR		rgbDesc[RGB_MAX_LEN];
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
		TCHAR *DrpTab;
		TCHAR *CrtTab;
		TCHAR *InsTab;
		TCHAR *SelTab;
	} ExecDirStr[] = {
		{_T("--"), _T("--"), _T("--"), _T("--")},
		{_T("--"), _T("--"), _T("--"), _T("--")}
	};

	TCHAR		*TestAsync = _T("--");
	SQLSMALLINT	Type[] = {SQL_WCHAR,SQL_WVARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR};
	TCHAR		*szInput[] = {_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("--"),_T("--")};
	SQLUINTEGER	ColPrec[] = {254,254,10,10,5,10,7,15,15,10,8,26,254,254,254};
	SQLSMALLINT	ColScale[] = {0,0,5,5,0,0,0,0,0,0,0,0,0,0,0};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLSetConnectAttr"), charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0].DrpTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_DrpTab_0"), var_list);
	ExecDirStr[0].CrtTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_CrtTab_0"), var_list);
	ExecDirStr[0].InsTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_InsTab_0"), var_list);
	ExecDirStr[0].SelTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_SelTab_0"), var_list);

	ExecDirStr[1].DrpTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_DrpTab_1"), var_list);
	ExecDirStr[1].CrtTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_CrtTab_1"), var_list);
	ExecDirStr[1].InsTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_InsTab_1"), var_list);
	ExecDirStr[1].SelTab = var_mapping(_T("SQLSetConnectAttr_ExecDirStr_SelTab_1"), var_list);

	szInput[0] = var_mapping(_T("SQLSetConnectAttr_szInput_0"), var_list);
	szInput[1] = var_mapping(_T("SQLSetConnectAttr_szInput_1"), var_list);
	szInput[12] = var_mapping(_T("SQLSetConnectAttr_szInput_12"), var_list);
	szInput[13] = var_mapping(_T("SQLSetConnectAttr_szInput_13"), var_list);
	szInput[14] = var_mapping(_T("SQLSetConnectAttr_szInput_14"), var_list);

	TestAsync = var_mapping(_T("SQLSetConnectAttr_TestAsync"), var_list);
	
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLSetConnection/GetConnection.\n"));

	TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLSet/GetConnectionOption tests\n");
  	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
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

	SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)ExecDirStr[0].DrpTab,SQL_NTS); 
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].CrtTab,SQL_NTS);
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
				_stprintf(Heading,_T("Test Positive functionality of SQLSetConnectAttr for %s and ParamValue: %s\n"),
									ConnectionOptionToChar(OptionInt[i].Attribute,TempBuf1),
									ConnectionParamToChar(OptionInt[i].Attribute,OptionInt[i].vParamInt[j],TempBuf2));
			}
			else
			{
				_stprintf(Heading,_T("Test Positive functionality of SQLSetConnectAttr for %s and ParamValue: %s\n"),
									StatementOptionToChar(OptionInt[i].Attribute,TempBuf1),
									StatementParamToChar(OptionInt[i].Attribute,OptionInt[i].vParamInt[j],TempBuf2));
			}
			TESTCASE_BEGINW(Heading);

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
						LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),OptionInt[i].vParamInt[j],pvParamInt);
						switch(OptionInt[i].Attribute) 
						{
							case SQL_ACCESS_MODE :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_MODE_READ_WRITE :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_MODE_READ_ONLY :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
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
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
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
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
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
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
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
									LogMsg(ERRMSG,_T("Unable to SQLAllocHandle\n"));
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
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
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
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
										{
											LogAllErrorsVer3(henv,hdbc1,hstmt1);
											TEST_FAILED;
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
										SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Create Table"))  )
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for PREPARE stmt of create table.\n"));
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}

										}*/
										SQLFreeStmt(hstmt,SQL_CLOSE);

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for PREPARE stmt of create table.\n"));
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for EXECUTE stmt of create table.\n"));
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLTables(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,(SQLTCHAR*)_T("TABLE"),SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLTABLES.\n"));
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
												returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLTABLEPRIVILEGES.\n"));
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
											returncode = SQLColumns(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLCOLUMNS.\n"));
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
												returncode = SQLColumnPrivileges(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLCOLUMNPRIVILEGES.\n"));
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
											returncode = SQLPrimaryKeys(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLPRIMARYKEYS.\n"));
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLSPECIALCOLUMNS.\n"));
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
											returncode = SQLStatistics(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,SQL_INDEX_UNIQUE,SQL_ENSURE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLSTATISTICS.\n"));
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
											returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[1].InsTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLPREPARE of INSERT.\n"));
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLNUMPARAMS.\n"));
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
														LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLDESCRIBEPARAM of column : %d.\n"),k+1);
														LogAllErrorsVer3(henv,hdbc,hstmt);
													}
												}
											}
										}
										for (k = 0; k < param; k++)
										{
											if (MX_MP_SPECIFIC == MX_SPECIFIC)
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_TCHAR,Type[k],PREP_LEN,0,szInput[k],0,&cbInput);
											}
											else
											{
												returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_TCHAR,Type[k],ColPrec[k],ColScale[k],szInput[k],300,&cbInput);
											}

											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLBINDPARAM of column : %d.\n"),k+1);
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLEXECUTE insert stmt.\n"));
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].SelTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLEXECDIRECT of a select stmt.\n"));
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLNUMRESULTCOLS.\n"));
												LogAllErrorsVer3(henv,hdbc,hstmt);
											}
										}
										for (k = 0; k < numcol; k++)
										{
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												returncode = SQLDescribeCol(hstmt,(SWORD)(k+1),(SQLTCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLDESCRIBECOL of column : %d.\n"),k+1);
													LogAllErrorsVer3(henv,hdbc,hstmt);
												}
											}
										}
										for (k = 0; k < numcol; k++)
										{
											for (iatt = 0; iatt <= totalatt; iatt++)
											{
		 										_tcscpy(rgbDesc,_T(""));
												pcbDesc = 0;
												pfDesc = 0;
												returncode = SQL_STILL_EXECUTING;
												while (returncode == SQL_STILL_EXECUTING)
												{
													returncode = SQLColAttributes(hstmt,(SWORD)(k+1),DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc);
													if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
													{
														TEST_FAILED;
														LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLCOLATTRIBUTES of column : %d.\n"),k+1);
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLFETCH.\n"));
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLEXECDIRECT of drop stmt.\n"));
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
						LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),OptionInt[i].vParamInt[j],pvParamInt);
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

	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); 
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLSetConnectionAttr/GetConnectionAttr.\n"));
	free_list(var_list);
	TEST_RETURN;
}
