#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	MAX_PARAMS		5
#define NUMROWS			200
#define	PREP_LEN		50
#define NAME_LEN		300
#define COLNAME_LEN		30
#define	RGB_MAX_LEN		50
#define MAX_COL			6
#define MAX_BUFFER		600
/*
------------------------------------------------------------------
   TestSQLSetConnectOption: Tests SQLSetConnectOption                      
------------------------------------------------------------------
*/
PassFail TestSQLSetConnectOption(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{   
	TEST_DECLARE;
	TCHAR		Heading[MAX_STRING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc, hdbc1;
 	SQLHANDLE	hstmt, hstmt1;
	int			i, j, qto;
	SQLUINTEGER		pvParamInt=0, rowsfetched;
//	TCHAR		pvParamChar[100];
	TCHAR				TempBuf1[MAX_STRING_SIZE];
	TCHAR				TempBuf2[MAX_STRING_SIZE];
	  
	struct {
		UWORD		fOption;
		BOOL		DoGetConnectOption;					// Since GetConnectOption doesn't return SetStmtoptions
		SQLULEN	vParamInt[MAX_PARAMS+1];
	} OptionInt[] = {			 
// connection options
		{SQL_ACCESS_MODE,TRUE,SQL_MODE_READ_WRITE,SQL_MODE_READ_ONLY,999,},
		{SQL_AUTOCOMMIT, TRUE,SQL_AUTOCOMMIT_OFF, SQL_AUTOCOMMIT_ON, 999,},
		{SQL_LOGIN_TIMEOUT,TRUE,60,0,999,},
//		{SQL_OPT_TRACE,TRUE,SQL_OPT_TRACE_OFF,SQL_OPT_TRACE_ON,999,},
//		{SQL_TRANSLATE_OPTION,TRUE,0,1,999},
		{SQL_TXN_ISOLATION,TRUE,SQL_TXN_READ_UNCOMMITTED,SQL_TXN_READ_COMMITTED,SQL_TXN_REPEATABLE_READ,SQL_TXN_SERIALIZABLE,/*SQL_TXN_VERSIONING,*/999},
//		{SQL_ODBC_CURSORS,TRUE,SQL_CUR_USE_IF_NEEDED,SQL_CUR_USE_ODBC,SQL_CUR_USE_DRIVER,999,},
//		{SQL_PACKET_SIZE,TRUE,0,512,1024,999,},

// statement option
		{SQL_MAX_ROWS,FALSE,0,1,10,50,100,999},
		{SQL_MAX_LENGTH,FALSE,0,10,50,100,200,999},
		{SQL_ASYNC_ENABLE,FALSE,SQL_ASYNC_ENABLE_ON,SQL_ASYNC_ENABLE_OFF,999,},
//		{SQL_QUERY_TIMEOUT,FALSE,0,1,999},
//		{SQL_NOSCAN,FALSE,SQL_NOSCAN_OFF,SQL_NOSCAN_ON,999,},
//		{SQL_BIND_TYPE,FALSE,SQL_BIND_BY_COLUMN,10,100,999,},
//		{SQL_CURSOR_TYPE,FALSE,SQL_CURSOR_FORWARD_ONLY,SQL_CURSOR_KEYSET_DRIVEN,SQL_CURSOR_DYNAMIC,SQL_CURSOR_STATIC,999,},
//		{SQL_CONCURRENCY,FALSE,SQL_CONCUR_READ_ONLY,SQL_CONCUR_LOCK,SQL_CONCUR_ROWVER,SQL_CONCUR_VALUES,999,},
//		{SQL_KEYSET_SIZE,FALSE,SQL_KEYSET_SIZE_DEFAULT,10,999,},
//		{SQL_ROWSET_SIZE,FALSE,SQL_ROWSET_SIZE_DEFAULT,10,999,},
//		{SQL_SIMULATE_CURSOR,FALSE,SQL_SC_NON_UNIQUE,SQL_SC_TRY_UNIQUE,SQL_SC_UNIQUE,999,},
//		{SQL_RETRIEVE_DATA,FALSE,SQL_RD_OFF,SQL_RD_ON,999,},
//		{SQL_USE_BOOKMARKS,FALSE,SQL_UB_OFF,SQL_UB_ON,999,}, 
		{999,}};
		
   	/* Set up some local variables to save on typing in longer ones */
	TCHAR		*colval[MAX_COL];
	SQLLEN		colvallen[MAX_COL];
	UWORD		k = 0,iatt = 0;
	SWORD		numcol,col;
	SWORD		param;
	TCHAR		cn[COLNAME_LEN];
	SWORD		cl;
	SWORD		st;
	SQLULEN 	cp;
	SWORD		cs, cnull;
	SQLLEN		cbInput = SQL_NTS;
	SWORD		totalatt = 18; /* should be 18 for 2.0 driver */
	TCHAR		rgbDesc[RGB_MAX_LEN];
	SWORD		pcbDesc;
	SQLLEN   	pfDesc;
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

	SQLSMALLINT	Type[] = {SQL_WCHAR,SQL_WVARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR};
	TCHAR		*szInput[] = {
								_T("--"),_T("--"),
								_T("1234.56789"),_T("5678.12345"),_T("1234"),      _T("12345"),
								_T("12340.0"),   _T("12300.0"),   _T("12345670.0"),_T("1993-12-30"),
								_T("11:45:23"),_T("1992-12-31 23:45:23.123456")
								#ifdef UNICODE
								,_T("--"),_T("--"),_T("--")
								#endif
							};

	SQLUINTEGER	ColPrec[] =  {254,254,10,10,5,10,7,15,15,10,8,26,254,254,254};
	SQLSMALLINT	ColScale[] = {0,0,5,5,0,0,0,0,0,0,0,0,0,0,0};

	struct {
		TCHAR *DrpTab;
		TCHAR *CrtTab;
		TCHAR *InsTab;
		TCHAR *SelTab;
	} ExecDirStr[] = {
		{_T("--"), _T("--"), _T("--"), _T("--")},
		{_T("--"), _T("--"), _T("--"), _T("--")},
		{_T("--"), _T("--"), _T("--"), _T("--")},
		{_T("--"), _T("--"), _T("--"), _T("--")}
	};

	TCHAR	*SelQuery[] = { _T("--"), _T("--") };
	TCHAR	*QryTimeOut[] = { _T("--"), _T("--"), _T("--") };
	TCHAR	*MXTimeOutQry[] = { _T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--") };
	TCHAR	*InsTmp,*InsCol,*TestAsync,*InsVal3;

	TCHAR buff[1024];
	int mySize = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLSetConnectOption"), charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0].DrpTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_DrpTab_0"), var_list);
	ExecDirStr[0].CrtTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_CrtTab_0"), var_list);
	ExecDirStr[0].InsTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_InsTab_0"), var_list);
	ExecDirStr[0].SelTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_SelTab_0"), var_list);

	ExecDirStr[1].DrpTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_DrpTab_1"), var_list);
	ExecDirStr[1].CrtTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_CrtTab_1"), var_list);
	ExecDirStr[1].InsTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_InsTab_1"), var_list);
	ExecDirStr[1].SelTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_SelTab_1"), var_list);

	ExecDirStr[2].DrpTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_DrpTab_2"), var_list);
	ExecDirStr[2].CrtTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_CrtTab_2"), var_list);
	ExecDirStr[2].InsTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_InsTab_2"), var_list);
	ExecDirStr[2].SelTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_SelTab_2"), var_list);

	ExecDirStr[3].DrpTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_DrpTab_3"), var_list);
	ExecDirStr[3].CrtTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_CrtTab_3"), var_list);
	ExecDirStr[3].InsTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_InsTab_3"), var_list);
	ExecDirStr[3].SelTab = var_mapping(_T("SQLSetConnectOption_ExecDirStr_SelTab_3"), var_list);

	SelQuery[0] = var_mapping(_T("SQLSetConnectOption_SelQuery_0"), var_list);
	SelQuery[1] = var_mapping(_T("SQLSetConnectOption_SelQuery_1"), var_list);

	InsVal3 = var_mapping(_T("SQLSetConnectOption_InsVal3"), var_list);

	szInput[0] = var_mapping(_T("SQLSetConnectOption_szInput_0"), var_list);
	szInput[1] = var_mapping(_T("SQLSetConnectOption_szInput_1"), var_list);

#ifdef UNICODE
	szInput[12] = var_mapping(_T("SQLSetConnectOption_szInput_12"), var_list);
	szInput[13] = var_mapping(_T("SQLSetConnectOption_szInput_13"), var_list);
	szInput[14] = var_mapping(_T("SQLSetConnectOption_szInput_14"), var_list);
#endif

	TestAsync = var_mapping(_T("SQLSetConnectOption_TestAsync"), var_list);

	MXTimeOutQry[0] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_0"), var_list);
	MXTimeOutQry[1] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_1"), var_list);
	MXTimeOutQry[2] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_2"), var_list);
	MXTimeOutQry[3] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_3"), var_list);
	MXTimeOutQry[4] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_4"), var_list);
	MXTimeOutQry[5] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_5"), var_list);
	MXTimeOutQry[6] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_6"), var_list);
	MXTimeOutQry[7] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_7"), var_list);
	MXTimeOutQry[8] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_8"), var_list);
	MXTimeOutQry[9] = var_mapping(_T("SQLSetConnectOption_MXTimeOutQry_9"), var_list);

	QryTimeOut[0] = var_mapping(_T("SQLSetConnectOption_QryTimeOut_0"), var_list);
	QryTimeOut[1] = var_mapping(_T("SQLSetConnectOption_QryTimeOut_1"), var_list);
	QryTimeOut[2] = var_mapping(_T("SQLSetConnectOption_QryTimeOut_2"), var_list);
	
//===========================================================================================================
		
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLSetConnection/GetConnection.\n"));

	TEST_INIT;

//==========================================================================================================

	TESTCASE_BEGIN("Setup for SQLSet/GetConnectionOption tests\n");
	returncode=FullConnect(pTestInfo);
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		LogMsg(ERRMSG,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	hstmt1 = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); 
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].CrtTab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLFreeStmt(hstmt,SQL_DROP);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END; // end of setup

//==========================================================================================================
	for (i = 0; OptionInt[i].fOption != 999; i++) 
	{
		for (j = 0; OptionInt[i].vParamInt[j] != 999; j++)
		{
			if (OptionInt[i].DoGetConnectOption == TRUE)
			{
				_stprintf(Heading,_T("Test Positive functionality of SQLSetConnectOptions for %s and ParamValue: %s\n"),
									ConnectionOptionToChar(OptionInt[i].fOption,TempBuf1),
									ConnectionParamToChar(OptionInt[i].fOption,OptionInt[i].vParamInt[j],TempBuf2));
			}
			else
			{
				_stprintf(Heading,_T("Test Positive functionality of SQLSetConnectOptions for %s and ParamValue: %s\n"),
									StatementOptionToChar(OptionInt[i].fOption,TempBuf1),
									StatementParamToChar(OptionInt[i].fOption,OptionInt[i].vParamInt[j],TempBuf2));
			}
			TESTCASE_BEGINW(Heading);

			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,OptionInt[i].fOption,OptionInt[i].vParamInt[j]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,(SQLHANDLE)NULL);
			}
			else
			{
				returncode = SQLGetConnectOption((SQLHANDLE)hdbc,OptionInt[i].fOption,&pvParamInt);
				if ((returncode != SQL_SUCCESS) && (OptionInt[i].DoGetConnectOption != FALSE))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,(SQLHANDLE)NULL);
				}
				else
				{
					returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
					{
						TEST_FAILED;
						TEST_RETURN;
					}
					if ((OptionInt[i].vParamInt[j] == pvParamInt) || (OptionInt[i].DoGetConnectOption == FALSE))
					{
						LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),OptionInt[i].vParamInt[j],pvParamInt);
						switch(OptionInt[i].fOption) 
						{
							case SQL_ACCESS_MODE :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_MODE_READ_WRITE :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_MODE_READ_ONLY :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
										{
											TEST_FAILED;
											LogAllErrors(henv,hdbc,hstmt);
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
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_COMMIT);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTransact"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLTransact((SQLHANDLE)henv,(SQLHANDLE)hdbc,SQL_ROLLBACK);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTransact"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
									case SQL_AUTOCOMMIT_ON :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].InsTab, SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										break;
								}
								break;
							case SQL_LOGIN_TIMEOUT :
								returncode = SQLAllocConnect((SQLHANDLE)henv,(SQLHANDLE *)&hdbc1);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
								{
									LogMsg(ERRMSG,_T("Unable to SQLAllocConnect\n"));
									TEST_FAILED;
								}
								switch(OptionInt[i].vParamInt[j]) 
								{
									case 0 :
										returncode = SQLSetConnectOption((SQLHANDLE)hdbc1,OptionInt[i].fOption,OptionInt[i].vParamInt[j]);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
										{
											LogAllErrors(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
										{
											LogAllErrors(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										break;
									case 1 :
										returncode = SQLSetConnectOption((SQLHANDLE)hdbc1,OptionInt[i].fOption,OptionInt[i].vParamInt[j]);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
										{
											LogAllErrors(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										returncode = SQLConnect((SQLHANDLE)hdbc1,(SQLTCHAR*)pTestInfo->DataSource,SQL_NTS,(SQLTCHAR*)pTestInfo->UserID,SQL_NTS,(SQLTCHAR*)pTestInfo->Password,SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
										{
											LogAllErrors(henv,hdbc1,hstmt1);
											TEST_FAILED;
										}
										break;
								}
								SQLDisconnect((SQLHANDLE)hdbc1);
								SQLFreeConnect((SQLHANDLE)hdbc1);
								break;

							// Statement options
							case SQL_QUERY_TIMEOUT :
								if (MX_MP_SPECIFIC == MP_SPECIFIC)
								{
									SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[2].DrpTab,SQL_NTS); 
									returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2].CrtTab,SQL_NTS);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									else
									{
										returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[2].InsTab, SQL_NTS);
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
											}
										}
										SQLExecDirect(hstmt,(SQLTCHAR*)QryTimeOut[0],SQL_NTS); 
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)QryTimeOut[1],SQL_NTS);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
									switch(OptionInt[i].vParamInt[j]) 
									{
										case 0 :
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)QryTimeOut[2], SQL_NTS);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;						
										case 1 :
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)QryTimeOut[2], SQL_NTS);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;
									}
									SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[2].DrpTab,SQL_NTS); 
									SQLExecDirect(hstmt,(SQLTCHAR*) QryTimeOut[0],SQL_NTS);
								}
								else
								{
									for (qto = 0; qto < 3; qto++)
									{
										SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[qto],SQL_NTS);	// cleanup
									}
									for (qto = 3; qto < 6; qto++)
									{
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[qto],SQL_NTS);	// create table
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
									returncode = SQLPrepare(hstmt,(SQLTCHAR*)MXTimeOutQry[6], SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									for (qto = 0; qto < 400; qto++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
									returncode = SQLPrepare(hstmt,(SQLTCHAR*)MXTimeOutQry[7], SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									for (qto = 0; qto < 100; qto++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
									switch(OptionInt[i].vParamInt[j]) 
									{
										case 0 :
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[8], SQL_NTS);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;						
										case 1 :
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[9], SQL_NTS);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}

											returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											do
											{
												returncode = SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[9], SQL_NTS);
											}
											while (returncode == SQL_STILL_EXECUTING);
											if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											do
											{
												returncode = SQLPrepare(hstmt,(SQLTCHAR*)MXTimeOutQry[9], SQL_NTS);
											}
											while (returncode == SQL_STILL_EXECUTING);
											if (returncode == SQL_SUCCESS)
											{
												do
												{
													returncode = SQLPrepare(hstmt,(SQLTCHAR*)MXTimeOutQry[9], SQL_NTS);
												}
												while (returncode == SQL_STILL_EXECUTING);
											}
											if(!CHECKRC(SQL_ERROR,returncode,"SQLPrepare/SQLExecute"))
											{
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
											}
											break;
									}
									for (qto = 0; qto < 3; qto++)
									{
										SQLExecDirect(hstmt,(SQLTCHAR*)MXTimeOutQry[qto],SQL_NTS);	// cleanup
									}
								}
								break;						
							case SQL_MAX_ROWS :
								SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[2].DrpTab,SQL_NTS); 
								returncode = SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[2].CrtTab,SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									TEST_RETURN;
								}
								else
								{
									returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[2].InsTab, SQL_NTS);
									if (returncode != SQL_SUCCESS)
									{
										TEST_FAILED;
										TEST_RETURN;
									}
									for (k = 0; k < NUMROWS; k++)
									{
										returncode = SQLExecute(hstmt);
										if (returncode != SQL_SUCCESS)
										{
											TEST_FAILED;
											TEST_RETURN;
										}
									}
									SQLFreeStmt(hstmt,SQL_CLOSE);
								}
								returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2].SelTab, SQL_NTS);
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
											LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),rowsfetched,NUMROWS);
										else
										{
											TEST_FAILED;
											LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),rowsfetched,NUMROWS);
										}
										break;						
									case 1 :
									case 10 :
									case 50 :
									case 100 :
										if (rowsfetched == OptionInt[i].vParamInt[j])
											LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),rowsfetched,OptionInt[i].vParamInt[j]);
										else
										{
											TEST_FAILED;
											LogMsg(ERRMSG,_T("expect: %d and actual: %d are matched\n"),rowsfetched,OptionInt[i].vParamInt[j]);
										}
										break;
								}
								SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[2].DrpTab,SQL_NTS); 
								break;						
							case SQL_NOSCAN :
								if (MX_MP_SPECIFIC == MX_SPECIFIC)
								{
									LogMsg(NONE,_T("This Statement option: SQL_NOSCAN is not supported in MX driver.\n"));
									break;
								}
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_NOSCAN_OFF :
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelQuery[0], SQL_NTS);
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
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelQuery[1], SQL_NTS);
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
								SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[3].DrpTab,SQL_NTS); 
								returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3].CrtTab,SQL_NTS);
								LogMsg(NONE,_T("%s (line: %d)\n"), ExecDirStr[3].CrtTab, __LINE__);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									InsTmp = (TCHAR *)malloc(MAX_NOS_SIZE*sizeof(TCHAR));
									InsCol = (TCHAR *)malloc(MAX_NOS_SIZE*sizeof(TCHAR));
									_tcscpy(InsCol,_T(""));
									_tcscat(InsCol,InsVal3);
									_tcscat(InsCol,InsVal3);
									_tcscat(InsCol,InsVal3);
									_tcscat(InsCol,InsVal3);
									_tcscat(InsCol,InsVal3);
									_tcscpy(InsTmp,_T(""));
									_tcscat(InsTmp,ExecDirStr[3].InsTab);
									_tcscat(InsTmp,_T("_iso88591'"));
									_tcscat(InsTmp,InsCol);
									_tcscat(InsTmp,_T("',_iso88591'"));
									_tcscat(InsTmp,InsCol);
									_tcscat(InsTmp,_T("',_iso88591'"));
									_tcscat(InsTmp,InsCol);
									// Modify + 6
								#ifndef UNICODE
									_tcscat(InsTmp,_T("','"));
									_tcscat(InsTmp,InsCol);
									_tcscat(InsTmp,_T("','"));
									_tcscat(InsTmp,InsCol);
									_tcscat(InsTmp,_T("','"));
									_tcscat(InsTmp,InsCol);
								#endif
									_tcscat(InsTmp,_T("')"));

									LogMsg(NONE,_T("%s\n"), InsTmp);
									returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTmp, SQL_NTS);
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
								LogMsg(NONE,_T("Test Bindcol Then Fetch.\n"));
								returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3].SelTab, SQL_NTS);
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
										colval[col] = (TCHAR *)malloc(MAX_BUFFER);
										returncode = SQLBindCol(hstmt,(SWORD)(col+1),SQL_C_TCHAR,colval[col],MAX_BUFFER,&colvallen[col]);
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
											if (_tcslen(colval[col]) == _tcslen(InsCol))
													LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),_tcslen(InsCol),_tcslen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched at: %d \n"),_tcslen(InsCol),_tcslen(colval[col]), __LINE__);
												}
												break;						
											case 10 :
											case 50 :
											case 100 :
											case 200 :
												if (col <= 2) mySize = mbs_truncate(InsCol, buff, OptionInt[i].vParamInt[j], 1);
												else mySize = mbs_truncate(InsCol, buff, OptionInt[i].vParamInt[j], 2);

												if ((mySize == _tcslen(colval[col])*sizeof(TCHAR)) && (_tcscmp(buff, colval[col]) == 0))
													LogMsg(NONE,_T("expect: %s, size %d and actual: %s, size %d are matched\n"), buff, mySize, colval[col], _tcslen(colval[col])*sizeof(TCHAR));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched at: %d\n"),buff,colval[col], __LINE__);
													LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched at: %d\n"), mySize, _tcslen(colval[col])*sizeof(TCHAR), __LINE__);
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
								LogMsg(NONE,_T("Test Fetch Then GetData.\n"));
								returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3].SelTab, SQL_NTS);
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
										colval[col] = (TCHAR *)malloc(MAX_BUFFER);
										returncode = SQLGetData(hstmt,(SWORD)(col+1),SQL_C_TCHAR,colval[col],MAX_BUFFER,&colvallen[col]);
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
												if (_tcslen(colval[col]) == _tcslen(InsCol))
													LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),_tcslen(InsCol),_tcslen(colval[col]));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched at: %d\n"),_tcslen(InsCol),_tcslen(colval[col]),__LINE__);
												}
												break;						
											case 10 :
											case 50 :
											case 100 :
											case 200 :
												if (col <= 2) mySize = mbs_truncate(InsCol, buff, OptionInt[i].vParamInt[j], 1);
												else mySize = mbs_truncate(InsCol, buff, OptionInt[i].vParamInt[j], 2);

												if ((mySize == _tcslen(colval[col])*sizeof(TCHAR)) && (_tcscmp(buff, colval[col]) == 0))
													LogMsg(NONE,_T("expect: %s, size %d and actual: %s, size %d are matched.\n"), buff, mySize, colval[col], _tcslen(colval[col])*sizeof(TCHAR));
												else
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched at: %d\n"),buff,colval[col], __LINE__);
													LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched at: %d\n"), mySize, _tcslen(colval[col])*sizeof(TCHAR), __LINE__);
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
								SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[3].DrpTab,SQL_NTS); 
								break;						
							case SQL_ASYNC_ENABLE :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_ASYNC_ENABLE_OFF :
										SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
										if( (!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect->Create Table"))  )
										{
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
										}
										returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS); // cleanup
										}
										SQLFreeStmt(hstmt,SQL_CLOSE);

										returncode = SQL_STILL_EXECUTING;
										while (returncode == SQL_STILL_EXECUTING)
										{
											returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[1].CrtTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for PREPARE stmt of create table.\n"));
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for EXECUTE stmt of create table.\n"));
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
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
												//Error: [Microsoft][ODBC Driver Manager] Driver does not support this function
												returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												//if (returncode != SQL_ERROR)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLTABLEPRIVILEGES.\n"));
													//LogMsg(ERRMSG,_T("Test succeeded while executing ASYNC call for SQLTABLEPRIVILEGES.\n"));
													LogAllErrors(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
											//if(!CHECKRC(SQL_ERROR,returncode,"SQLFreeStmt"))
											{
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
										}
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
												//Error: [Microsoft][ODBC Driver Manager] Driver does not support this function
												returncode = SQLColumnPrivileges(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS);
												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												//if (returncode != SQL_ERROR)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLCOLUMNPRIVILEGES.\n"));
													//LogMsg(ERRMSG,_T("Test succeeded while executing ASYNC call for SQLCOLUMNPRIVILEGES.\n"));
													LogAllErrors(henv,hdbc,hstmt);
												}
											}
											returncode = SQLFreeStmt(hstmt,SQL_CLOSE);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
											//if(!CHECKRC(SQL_ERROR,returncode,"SQLFreeStmt"))
											{
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
											}
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
											returncode = SQLSpecialColumns(hstmt,SQL_BEST_ROWID,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,SQL_SCOPE_CURROW,SQL_NULLABLE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLSPECIALCOLUMNS.\n"));
												LogAllErrors(henv,hdbc,hstmt);
											}
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
											returncode = SQLStatistics(hstmt,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR*)_T(""),SQL_NTS,(SQLTCHAR *)TestAsync,SQL_NTS,SQL_INDEX_UNIQUE,SQL_ENSURE);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLSTATISTICS.\n"));
												LogAllErrors(henv,hdbc,hstmt);
											}
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
											returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[1].InsTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLPREPARE of INSERT.\n"));
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
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
														LogAllErrors(henv,hdbc,hstmt);
													}
												}
											}
										}
										for (k = 0; k < param; k++)
										{
											returncode = SQL_STILL_EXECUTING;
											while (returncode == SQL_STILL_EXECUTING)
											{
												if (MX_MP_SPECIFIC == MX_SPECIFIC)
												{
													returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_TCHAR,Type[k],PREP_LEN,0,szInput[k],0,&cbInput);
												}
												else
												{
													returncode = SQLBindParameter(hstmt,(SWORD)(k+1),SQL_PARAM_INPUT,SQL_C_TCHAR,Type[k],ColPrec[k],ColScale[k],szInput[k],MAX_BUFFER,&cbInput);
												}

												if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
												{
													TEST_FAILED;
													LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLBINDPARAM of column : %d.\n"),k+1);
													LogAllErrors(henv,hdbc,hstmt);
												}
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
												LogAllErrors(henv,hdbc,hstmt);
											}
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].SelTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLEXECDIRECT of a select stmt.\n"));
												LogAllErrors(henv,hdbc,hstmt);
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
												LogAllErrors(henv,hdbc,hstmt);
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
													LogAllErrors(henv,hdbc,hstmt);
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
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLFETCH.\n"));
												LogAllErrors(henv,hdbc,hstmt);
											}
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
											returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1].DrpTab,SQL_NTS);
											if (returncode != SQL_STILL_EXECUTING && returncode != SQL_SUCCESS)
											{
												TEST_FAILED;
												LogMsg(ERRMSG,_T("Test failed while executing ASYNC call for SQLEXECDIRECT of drop stmt.\n"));
												LogAllErrors(henv,hdbc,hstmt);
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
						LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched at: %d\n"),OptionInt[i].vParamInt[j],pvParamInt,__LINE__);
					}
					returncode = SQLFreeStmt(hstmt,SQL_DROP);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}
			}
		}	
	}	

//======================================================================================================

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
	{
		TEST_FAILED;
		TEST_RETURN;
	}

/*	for (i = 0; OptionChar[i].fOption != 999; i++) 
	{
		for (j = 0; (_tcscmp(OptionChar[i].vParamChar[j], "end") != 0); j++)
		{
			_stprintf(Heading,_T("Test Positive functionality of SQLSetConnectOption/SQLGetConnectOption for option: %d and param: %d\n"),OptionChar[i].fOption,OptionChar[i].vParamChar[j]);
			TESTCASE_BEGINW(Heading);
			returncode = SQLSetConnectOption(hdbc,OptionChar[i].fOption,OptionChar[i].vParamChar[j]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOptions"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLGetConnectOption(hdbc,OptionChar[i].fOption,pvParamChar);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetConnectOptions"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					if (_tcsstr(pvParamChar,OptionChar[i].vParamChar[j]) != NULL)
					{
						LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),OptionChar[i].vParamChar[j],pvParamChar);
						TESTCASE_END;
					}
						// Success 
					else
					{
						TEST_FAILED;
						LogMsg(NONE,_T("expect: %s and actual: %s are not matched at: %d\n"),OptionChar[i].vParamChar[j],pvParamChar,__LINE__);
					}
				}
			}
		}	
	}																	 
*/

//=============================================================================================================

	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0].DrpTab,SQL_NTS); 
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLSetConnection/GetConnection.\n"));
	free_list(var_list);
	TEST_RETURN;
}
