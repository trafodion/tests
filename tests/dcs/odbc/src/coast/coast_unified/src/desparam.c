#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

/*
---------------------------------------------------------
   TestSQLDescribeParam for MX Specific
---------------------------------------------------------
*/

PassFail TestSQLDescribeParam(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{                  
	TEST_DECLARE;
 	TCHAR			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	SWORD			numparam;
	UWORD			icol;

	SWORD		st, SQLType[] = 
							{
								SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
								SQL_DOUBLE,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_BIGINT,SQL_VARCHAR,
								#ifndef UNICODE
								SQL_WCHAR,SQL_WVARCHAR,SQL_WVARCHAR,
								#endif
								SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC
								#ifdef UNICODE
								,SQL_WCHAR,SQL_WVARCHAR,SQL_WVARCHAR,SQL_CHAR,SQL_VARCHAR,SQL_VARCHAR
								#endif			
							};										// SQL_DOUBLE for SQL_FLOAT SQL/MX limitation
																	//SQL_BIGINT replaced by SQL_NUMERIC in SQL/MX
	SWORD		MPSQLType[] = 
							{
								SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
								SQL_FLOAT,SQL_FLOAT,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_BIGINT,SQL_VARCHAR,
								#ifndef UNICODE
								SQL_WCHAR,SQL_WVARCHAR,SQL_WVARCHAR,
								#endif
								SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC
								#ifdef UNICODE
								,SQL_WCHAR,SQL_WVARCHAR,SQL_WVARCHAR,SQL_CHAR,SQL_VARCHAR,SQL_VARCHAR
								#endif
							};						
    SQLULEN cp; // sushil
	SWORD		cs, cnull;
#ifdef UNICODE
	SQLULEN		ColPrec[] =   {10,10,10,10,5,10,7,15,15,10,8,26,19,2000,19,19,128,128,128,10,18,30,10,10,2000,40,40,2000};
    SQLULEN		MPColPrec[] = {10,10,10,10,5,10,7,15,15,10,8,26,19,10,  19,19,128,128,128,10,18,30,10,10,2000,10,10,2000};	
	SWORD		ColScale[] =  {0, 0, 5, 5, 0,0, 0,0, 0, 0, 0,6, 0, 0,   0, 6, 0,  128,64, 5,  5,10,0, 0, 0,   0, 0, 0};
#else 
	SQLULEN		ColPrec[] =   {10,10,10,10,5,10,7,15,15,10,8,26,19,2000,10,10,2000,19,19,128,128,128,10,18,30};
    SQLULEN		MPColPrec[] = {10,10,10,10,5,10,7,15,15,10,8,26,19,10,  10,10,10,  19,19,128,128,128,10,18,30};	
	SWORD		ColScale[] =  {0, 0, 5, 5, 0,0, 0,0, 0, 0, 0,6, 0, 0,   0, 0, 0,   0, 6, 0,  128,64, 5, 5, 10};
#endif

	TCHAR		*DropStr[] = {_T("--"),_T("--"),_T("endloop")};
	TCHAR		*CrtStr[] = {_T("--"), _T("--"), _T("endloop")};
	TCHAR		*MPCrtStr[] = {_T("--"), _T("--"), _T("endloop")};
	TCHAR		*ExecDirStr[] = {_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("endloop")};

	TCHAR		TempType1[50],TempType2[50];
	SWORD		ColNullable[] = {SQL_NULLABLE,SQL_NO_NULLS,SQL_NULLABLE,SQL_NO_NULLS,SQL_NULLABLE,SQL_NO_NULLS,SQL_NULLABLE,SQL_NO_NULLS,SQL_NULLABLE,SQL_NO_NULLS};

	TCHAR		*TestCase[] = 
						{
							_T("before preparing stmt "),
							_T("endloop")
						};

	SQLUSMALLINT i = 0, l = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLDescribeParam"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	DropStr[0] = var_mapping(_T("SQLDescribeParam_DropStr_1"), var_list);
	DropStr[1] = var_mapping(_T("SQLDescribeParam_DropStr_2"), var_list);

	CrtStr[0] = var_mapping(_T("SQLDescribeParam_CrtStr_1"), var_list);
	CrtStr[1] = var_mapping(_T("SQLDescribeParam_CrtStr_2"), var_list);

	MPCrtStr[0] = var_mapping(_T("SQLDescribeParam_MPCrtStr_1"), var_list);
	MPCrtStr[1] = var_mapping(_T("SQLDescribeParam_MPCrtStr_2"), var_list);

	ExecDirStr[0] = var_mapping(_T("SQLDescribeParam_ExecDirStr_1"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLDescribeParam_ExecDirStr_2"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLDescribeParam_ExecDirStr_3"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLDescribeParam_ExecDirStr_4"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLDescribeParam_ExecDirStr_5"), var_list);
	ExecDirStr[5] = var_mapping(_T("SQLDescribeParam_ExecDirStr_6"), var_list);
	ExecDirStr[6] = var_mapping(_T("SQLDescribeParam_ExecDirStr_7"), var_list);
	ExecDirStr[7] = var_mapping(_T("SQLDescribeParam_ExecDirStr_8"), var_list);
	ExecDirStr[8] = var_mapping(_T("SQLDescribeParam_ExecDirStr_9"), var_list);
	ExecDirStr[9] = var_mapping(_T("SQLDescribeParam_ExecDirStr_10"), var_list);

//=================================================================================================

	if(isUCS2) {
		LogMsg(NONE,_T("Setup for UCS2 mode testing: ColPrec has to be doubled\n"));

		l = sizeof(SQLType)/sizeof(SQLType[0]);
		while(i < l) {
			if(SQLType[i] == SQL_WCHAR) {
				SQLType[i] = SQL_WCHAR;
				//ColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else if (SQLType[i] == SQL_WVARCHAR) {
				SQLType[i] = SQL_WVARCHAR;
				//ColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else if (SQLType[i] == SQL_WLONGVARCHAR)	{
				SQLType[i] = SQL_WLONGVARCHAR;
				//ColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else {
			}

			i++;
		}
		i = 0;

		l = sizeof(MPSQLType)/sizeof(MPSQLType[0]);
		while(i < l) {
			if(MPSQLType[i] == SQL_WCHAR) {
				MPSQLType[i] = SQL_WCHAR;
				//MPColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else if (MPSQLType[i] == SQL_WVARCHAR) {
				MPSQLType[i] = SQL_WVARCHAR;
				//MPColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else if (MPSQLType[i] == SQL_WLONGVARCHAR)	{
				MPSQLType[i] = SQL_WLONGVARCHAR;
				//MPColPrec[i] *= 2;  --> This is in character, so no need to double
			}
			else {
			}

			i++;
		}
		i = 0;
		l = 0;
	}

//===========================================================================================================

	if (MX_MP_SPECIFIC == MX_SPECIFIC)
	   LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLDescribeParam.\n"));
	else
       LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MP Specific SQLDescribeParam.\n"));

	TEST_INIT;
	   
	TESTCASE_BEGIN("Setup for SQLDescribeParam tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	i = 0;
	while (_tcsicmp(DropStr[i],_T("endloop")) != 0)
	{
		SQLExecDirect(hstmt,(SQLTCHAR*)DropStr[i],SQL_NTS); /* cleanup */
		i++;
	}
	i = 0;
	if (MX_MP_SPECIFIC == MX_SPECIFIC)
	{
		while (_tcsicmp(CrtStr[i],_T("endloop")) != 0)
		{
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtStr[i],SQL_NTS); /* create table */
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			//LogMsg(NONE,_T("%s\n"),	CrtStr[i]);
			i++;
		}
	}
	else
	{
		while (_tcsicmp(MPCrtStr[i],_T("endloop")) != 0)
		{
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)MPCrtStr[i],SQL_NTS); /* create table */
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			//LogMsg(NONE,_T("%s\n"),	MPCrtStr[i]);
			i++;
		}
	}
	TESTCASE_END;  // end of setup

	l = 0;
	while (_tcsicmp(TestCase[l],_T("endloop")) != 0)
	{
		i = 0;
		while (_tcsicmp(ExecDirStr[i],_T("endloop")) != 0)
		{
			//==================================================================================
			_stprintf(Heading,_T("SQLDescribeParam: Test #%d.%d\n"),l,i);
			TESTCASE_BEGINW(Heading);
			returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[i], SQL_NTS);
			//LogMsg(NONE,_T("%s\n"), ExecDirStr[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				returncode=SQLNumParams(hstmt, &numparam);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				//LogMsg(NONE,_T("SQLNumParams returns %d\n"), numparam);
				for (icol = 1; icol <= numparam; icol++)
				{
					LogMsg(LINEBEFORE,_T("SQLDescribeParam: checking Column #%d\n"),icol);
					returncode = SQLDescribeParam(hstmt,icol,&st,&cp,&cs,&cnull);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeParam"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					if (MX_MP_SPECIFIC == MX_SPECIFIC)
					{
						if ((st==SQLType[icol-1]) && (cp==ColPrec[icol-1]) && (cs==ColScale[icol-1]) && (cnull==ColNullable[i]))
						{
							LogMsg(NONE,_T("SQLType expect: %s and actual: %s are matched\n"),
								SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
							LogMsg(NONE,_T("ColPrec expect: %d and actual: %d are matched\n"),ColPrec[icol-1],cp);
							LogMsg(NONE,_T("ColScale expect: %d and actual: %d are matched\n"),ColScale[icol-1],cs);
							LogMsg(NONE,_T("ColNullable expect: %s and actual: %s are matched\n\n"),
								SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
						}	
						else
						{
							TEST_FAILED;	
							if (st != SQLType[icol-1])
								LogMsg(ERRMSG,_T("SQLType expect: %s and actual: %s are not matched\n"),SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
							if (cp != ColPrec[icol-1])
								LogMsg(ERRMSG,_T("ColPrec expect: %d and actual: %d are not matched\n"),ColPrec[icol-1],cp);
							if (cs != ColScale[icol-1])
								LogMsg(ERRMSG,_T("ColScale expect: %d and actual: %d are not matched\n"),ColScale[icol-1],cs);
							if (cnull != ColNullable[i])
								LogMsg(ERRMSG,_T("ColNullable expect: %s and actual: %s are not matched\n\n"),SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
						}
					}
					else
					{
						if ((st==MPSQLType[icol-1]) && (cp==MPColPrec[icol-1]) && (cs==ColScale[icol-1]) && (cnull==ColNullable[i]))
						{
							LogMsg(NONE,_T("SQLType expect: %s and actual: %s are matched\n"),
								SQLTypeToChar(MPSQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
							LogMsg(NONE,_T("ColPrec expect: %d and actual: %d are matched\n"),MPColPrec[icol-1],cp);
							LogMsg(NONE,_T("ColScale expect: %d and actual: %d are matched\n"),ColScale[icol-1],cs);
							LogMsg(NONE,_T("ColNullable expect: %s and actual: %s are matched\n\n"),
								SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
						}	
						else
						{
							TEST_FAILED;	
							if (st != MPSQLType[icol-1])
								LogMsg(ERRMSG,_T("SQLType expect: %s and actual: %s are not matched\n"),SQLTypeToChar(MPSQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
							if (cp != MPColPrec[icol-1])
								LogMsg(ERRMSG,_T("ColPrec expect: %d and actual: %d are not matched\n"),MPColPrec[icol-1],cp);
							if (cs != ColScale[icol-1])
								LogMsg(ERRMSG,_T("ColScale expect: %d and actual: %d are not matched\n"),ColScale[icol-1],cs);
							if (cnull != ColNullable[i])
								LogMsg(ERRMSG,_T("ColNullable expect: %s and actual: %s are not matched\n\n"),SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
						}
					}
				} /* end icol loop */
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			i++;
			TESTCASE_END;
		}
		l++;
	}

	i = 0;
	while (_tcsicmp(DropStr[i],_T("endloop")) != 0)
	{
		SQLExecDirect(hstmt,(SQLTCHAR*)DropStr[i],SQL_NTS); /* cleanup */
		i++;
	}

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLDescribeParam.\n"));
	free_list(var_list);
	TEST_RETURN;
}
