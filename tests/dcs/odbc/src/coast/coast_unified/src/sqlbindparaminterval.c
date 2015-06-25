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
#include <time.h>
#include <windows.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN		300

#ifdef UNICODE
#define MAX_BINDPARAM1	15
#define MAX_BINDPARAM2	10
#else
#define MAX_BINDPARAM1	9
#define MAX_BINDPARAM2	4
#endif

#define MAX_BINDPARAM3	5
#define MAX_BINDPARAM4	8

void TestMXSQLBindParamaterInterval_Cleanup(SQLHANDLE hstmt, TCHAR* DrpTab, TCHAR* TempType, 
											 TCHAR* InsStr, TestInfo* pTestInfo);

PassFail TestMXSQLBindParameterInterval(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TCHAR		*InsStr;
	TCHAR		*TempType;

	TCHAR			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	int				i, j;
	int				loop_bindparam;
	SQLSMALLINT		ParamType = SQL_PARAM_INPUT;
	SQLLEN		InValue = SQL_NTS;
	TCHAR		OutValue[NAME_LEN];
	SQLLEN   	OutValueLen;

//****************************************
// Data structures for Testing Section #1 
 
	struct 
	{
		TCHAR				*TestSQLType[MAX_BINDPARAM1];
		SQLSMALLINT			SQLType[MAX_BINDPARAM1];
		SQLUINTEGER			ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT			ColScale[MAX_BINDPARAM1];
		TCHAR				*CrtTab;
	} CDataArgToSQL1[] = 
	{
#ifdef UNICODE
		{
		  _T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_YEAR"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_YEAR,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MONTH"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_MONTH,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_DAY"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_DAY,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{		
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_HOUR"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_HOUR,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MINUTE"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_MINUTE,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_SECOND"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_SECOND,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
#else
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_YEAR"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_YEAR,SQL_LONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,
			0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MONTH"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_MONTH,SQL_LONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,
			0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_DAY"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_DAY,SQL_LONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,
			0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_HOUR"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_HOUR,SQL_LONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,
			0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MINUTE"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_BIGINT,SQL_INTERVAL_MINUTE,SQL_LONGVARCHAR,
			254,254,0,0,0,0,0,0,2000,
			0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
#endif
		{_T("999"),}
	};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM1];
//		TCHAR		OutputValue[MAX_BINDPARAM1][35];
	} CDataValueTOSQL1[6] = {
#ifdef UNICODE
		{SQL_C_INTERVAL_YEAR,	_T("SQL_C_INTERVAL_YEAR"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
		{SQL_C_INTERVAL_MONTH,	_T("SQL_C_INTERVAL_MONTH"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
		{SQL_C_INTERVAL_DAY,	_T("SQL_C_INTERVAL_DAY"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("   1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
		{SQL_C_INTERVAL_HOUR,	_T("SQL_C_INTERVAL_HOUR"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
		{SQL_C_INTERVAL_MINUTE,	_T("SQL_C_INTERVAL_MINUTE"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
	//  {SQL_C_INTERVAL_SECOND,	_T("SQL_C_INTERVAL_SECOND"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1")},
#else		
		{SQL_C_INTERVAL_YEAR,	_T("SQL_C_INTERVAL_YEAR"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1")},
		{SQL_C_INTERVAL_MONTH,	_T("SQL_C_INTERVAL_MONTH"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1")},
		{SQL_C_INTERVAL_DAY,	_T("SQL_C_INTERVAL_DAY"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("   1"),	_T("1")},
		{SQL_C_INTERVAL_HOUR,	_T("SQL_C_INTERVAL_HOUR"),	_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1")},
		{SQL_C_INTERVAL_MINUTE,	_T("SQL_C_INTERVAL_MINUTE"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("1"),_T("  1"),	_T("1")},
#endif
		{999,}
	};

	TCHAR	*DrpTab1,*InsTab1,*SelTab1;

	SQL_INTERVAL_STRUCT CINTERVALTOSQL1;

	SQL_INTERVAL_STRUCT CINTERVALTOSQL2;

//****************************************
// Data structures for Testing Section #2 

	struct 
	{
		TCHAR				*TestSQLType[MAX_BINDPARAM2];
		SQLSMALLINT			SQLType[MAX_BINDPARAM2];
		SQLUINTEGER			ColPrec[MAX_BINDPARAM2];
		SQLSMALLINT			ColScale[MAX_BINDPARAM2];
		TCHAR				*CrtTab;
	} CDataArgToSQL2[] = 
	{
#ifdef UNICODE
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_SECOND"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_SECOND,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_YEAR_TO_MONTH"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_YEAR_TO_MONTH,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_HOUR"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_HOUR,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_MINUTE"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_MINUTE,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_SECOND"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_SECOND,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_HOUR_TO_MINUTE"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_HOUR_TO_MINUTE,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_HOUR_TO_SECOND"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_HOUR_TO_SECOND,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_MINUTE_TO_SECOND"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_MINUTE_TO_SECOND,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,2000,254,127,2000,254,127,2000,
			0,0,0,0,0,0,0,0,0,0,
			_T("--"),
		},
#else
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_SECOND"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_SECOND,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_YEAR_TO_MONTH"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_YEAR_TO_MONTH,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_HOUR"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_HOUR,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_MINUTE"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_MINUTE,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_DAY_TO_SECOND"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_DAY_TO_SECOND,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_HOUR_TO_MINUTE"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_HOUR_TO_MINUTE,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_HOUR_TO_SECOND"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_HOUR_TO_SECOND,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
		{
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_INTERVAL_MINUTE_TO_SECOND"),_T("SQL_LONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_INTERVAL_MINUTE_TO_SECOND,SQL_LONGVARCHAR,
			254,254,0,2000,
			0,0,0,0,
			_T("--"),
		},
#endif
		{_T("999"),}
	};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM2];
//		TCHAR		OutputValue[MAX_BINDPARAM2][35];
	} CDataValueTOSQL2[9] = {
#ifdef UNICODE
		{SQL_C_INTERVAL_SECOND,				_T("SQL_C_INTERVAL_SECOND"),			_T("1"),		_T("1"),		_T("  1"),			_T("1"),		_T("1"),		_T("1"),		_T("1"),		_T("1"),		_T("1"),		_T("1")},
		{SQL_C_INTERVAL_YEAR_TO_MONTH,		_T("SQL_C_INTERVAL_YEAR_TO_MONTH"),		_T("1-1"),		_T("1-1"),		_T("  1-01"),		_T("1-1"),		_T("1-1"),		_T("1-1"),		_T("1-1"),		_T("1-1"),		_T("1-1"),		_T("1-1")},
		{SQL_C_INTERVAL_DAY_TO_HOUR,		_T("SQL_C_INTERVAL_DAY_TO_HOUR"),		_T("1 1"),		_T("1 1"),		_T("   1 01"),		_T("1 1"),		_T("1 1"),		_T("1 1"),		_T("1 1"),		_T("1 1"),		_T("1 1"),		_T("1 1")},
		{SQL_C_INTERVAL_DAY_TO_MINUTE,		_T("SQL_C_INTERVAL_DAY_TO_MINUTE"),		_T("1 1:1"),	_T("1 1:1"),	_T("   1 01:01"),	_T("1 1:1"),	_T("1 1:1"),	_T("1 1:1"),	_T("1 1:1"),	_T("1 1:1"),	_T("1 1:1"),	_T("1 1:1")},
		{SQL_C_INTERVAL_DAY_TO_SECOND,		_T("SQL_C_INTERVAL_DAY_TO_SECOND"),		_T("1 1:1:1"),	_T("1 1:1:1"),	_T("   1 01:01:01"),_T("1 1:1:1"),	_T("1 1:1:1"),	_T("1 1:1:1"),	_T("1 1:1:1"),	_T("1 1:1:1"),	_T("1 1:1:1"),	_T("1 1:1:1")},
		{SQL_C_INTERVAL_HOUR_TO_MINUTE,		_T("SQL_C_INTERVAL_HOUR_TO_MINUTE"),	_T("1:1"),		_T("1:1"),		_T("  1:01"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1")},
		{SQL_C_INTERVAL_HOUR_TO_SECOND,		_T("SQL_C_INTERVAL_HOUR_TO_SECOND"),	_T("1:1:1"),	_T("1:1:1"),	_T("  1:01:01"),	_T("1:1:1"),	_T("1:1:1"),	_T("1:1:1"),	_T("1:1:1"),	_T("1:1:1"),	_T("1:1:1"),	_T("1:1:1")},
		{SQL_C_INTERVAL_MINUTE_TO_SECOND,	_T("SQL_C_INTERVAL_MINUTE_TO_SECOND"),	_T("1:1"),		_T("1:1"),		_T("  1:01"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1"),		_T("1:1")},
#else
		{SQL_C_INTERVAL_SECOND,				_T("SQL_C_INTERVAL_SECOND"),_T("1"),_T("1"),_T("  1"),_T("1")},
		{SQL_C_INTERVAL_YEAR_TO_MONTH,		_T("SQL_C_INTERVAL_YEAR_TO_MONTH"),_T("1-1"),_T("1-1"),_T("  1-01"),_T("1-1")},
		{SQL_C_INTERVAL_DAY_TO_HOUR,		_T("SQL_C_INTERVAL_DAY_TO_HOUR"),_T("1 1"),_T("1 1"),_T("   1 01"),_T("1 1")},
		{SQL_C_INTERVAL_DAY_TO_MINUTE,		_T("SQL_C_INTERVAL_DAY_TO_MINUTE"),_T("1 1:1"),_T("1 1:1"),_T("   1 01:01"),_T("1 1:1")},
		{SQL_C_INTERVAL_DAY_TO_SECOND,		_T("SQL_C_INTERVAL_DAY_TO_SECOND"),_T("1 1:1:1"),_T("1 1:1:1"),_T("   1 01:01:01"),_T("1 1:1:1")},
		{SQL_C_INTERVAL_HOUR_TO_MINUTE,		_T("SQL_C_INTERVAL_HOUR_TO_MINUTE"),_T("1:1"),_T("1:1"),_T("  1:01"),_T("1:1")},
		{SQL_C_INTERVAL_HOUR_TO_SECOND,		_T("SQL_C_INTERVAL_HOUR_TO_SECOND"),_T("1:1:1"),_T("1:1:1"),_T("  1:01:01"),_T("1:1:1")},
		{SQL_C_INTERVAL_MINUTE_TO_SECOND,	_T("SQL_C_INTERVAL_MINUTE_TO_SECOND"),_T("1:1"),_T("1:1"),_T("  1:01"),_T("1:1")},
#endif
		{999,}
		};

	TCHAR	*DrpTab2,*InsTab2,*SelTab2;

	SQL_INTERVAL_STRUCT CINTERVALTOSQL3;

	SQL_INTERVAL_STRUCT CINTERVALTOSQL4;

//************************************************
// Data structures for Testing Section #3
// SQL_C_INTERVAL(Single field) to SQL

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM1];
//		TCHAR		OutputValue[MAX_BINDPARAM1][35];
	} CDataValueTOSQL3[6] = {
#ifdef UNICODE
		{SQL_C_INTERVAL_YEAR,_T("SQL_C_INTERVAL_YEAR"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("  2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2")},
		{SQL_C_INTERVAL_MONTH,_T("SQL_C_INTERVAL_MONTH"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("  8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8")},
		{SQL_C_INTERVAL_DAY,_T("SQL_C_INTERVAL_DAY"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T(" 163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163")},
		{SQL_C_INTERVAL_HOUR,_T("SQL_C_INTERVAL_HOUR"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T(" 12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12")},
		{SQL_C_INTERVAL_MINUTE,_T("SQL_C_INTERVAL_MINUTE"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T(" 39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39")},
		// {SQL_C_INTERVAL_SECOND,_T("SQL_C_INTERVAL_SECOND"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T(" 59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59")},
#elif unixcli
#else
		{SQL_C_INTERVAL_YEAR,_T("SQL_C_INTERVAL_YEAR"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("2"),_T("  2"),_T("2")},
		{SQL_C_INTERVAL_MONTH,_T("SQL_C_INTERVAL_MONTH"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("8"),_T("  8"),_T("8")},
		{SQL_C_INTERVAL_DAY,_T("SQL_C_INTERVAL_DAY"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T("163"),_T(" 163"),_T("163")},
		{SQL_C_INTERVAL_HOUR,_T("SQL_C_INTERVAL_HOUR"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T("12"),_T(" 12"),_T("12")},
		{SQL_C_INTERVAL_MINUTE,_T("SQL_C_INTERVAL_MINUTE"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T("39"),_T(" 39"),_T("39")},
		// {SQL_C_INTERVAL_SECOND,_T("SQL_C_INTERVAL_SECOND"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T(" 59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59")},
#endif
		{999,}
		};

//************************************************
// Data structures for Testing Section #4
// SQL_C_INTERVAL(multiple fields) to SQL

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM2];
//		TCHAR		OutputValue[MAX_BINDPARAM2][35];
	} CDataValueTOSQL4[9] = {
#ifdef UNICODE
		{SQL_C_INTERVAL_SECOND,_T("SQL_C_INTERVAL_SECOND"),_T("59"),_T("59"),_T(" 59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59"),_T("59")},
		{SQL_C_INTERVAL_YEAR_TO_MONTH,_T("SQL_C_INTERVAL_YEAR_TO_MONTH"),_T("2-8"),_T("2-8"),_T("  2-08"),_T("2-8"),_T("2-8"),_T("2-8"),_T("2-8"),_T("2-8"),_T("2-8"),_T("2-8")},
		{SQL_C_INTERVAL_DAY_TO_HOUR,_T("SQL_C_INTERVAL_DAY_TO_HOUR"),_T("163 12"),_T("163 12"),_T(" 163 12"),_T("163 12"),_T("163 12"),_T("163 12"),_T("163 12"),_T("163 12"),_T("163 12"),_T("163 12")},
		{SQL_C_INTERVAL_DAY_TO_MINUTE,_T("SQL_C_INTERVAL_DAY_TO_MINUTE"),_T("163 12:39"),_T("163 12:39"),_T(" 163 12:39"),_T("163 12:39"),_T("163 12:39"),_T("163 12:39"),_T("163 12:39"),_T("163 12:39"),_T("163 12:39"),_T("163 12:39")},
		{SQL_C_INTERVAL_DAY_TO_SECOND,_T("SQL_C_INTERVAL_DAY_TO_SECOND"),_T("163 12:39:59"),_T("163 12:39:59"),_T(" 163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59"),_T("163 12:39:59")},
		{SQL_C_INTERVAL_HOUR_TO_MINUTE,_T("SQL_C_INTERVAL_HOUR_TO_MINUTE"),_T("12:39"),_T("12:39"),_T(" 12:39"),_T("12:39"),_T("12:39"),_T("12:39"),_T("12:39"),_T("12:39"),_T("12:39"),_T("12:39")},
		{SQL_C_INTERVAL_HOUR_TO_SECOND,_T("SQL_C_INTERVAL_HOUR_TO_SECOND"),_T("12:39:59"),_T("12:39:59"),_T(" 12:39:59"),_T("12:39:59"),_T("12:39:59"),_T("12:39:59"),_T("12:39:59"),_T("12:39:59"),_T("12:39:59"),_T("12:39:59")},
		{SQL_C_INTERVAL_MINUTE_TO_SECOND,_T("SQL_C_INTERVAL_MINUTE_TO_SECOND"),_T("39:59"),_T("39:59"),_T(" 39:59"),_T("39:59"),_T("39:59"),_T("39:59"),_T("39:59"),_T("39:59"),_T("39:59"),_T("39:59")},
#else
		{SQL_C_INTERVAL_SECOND,_T("SQL_C_INTERVAL_SECOND"),_T("59"),_T("59"),_T(" 59"),_T("59")},
		{SQL_C_INTERVAL_YEAR_TO_MONTH,_T("SQL_C_INTERVAL_YEAR_TO_MONTH"),_T("2-8"),_T("2-8"),_T("  2-08"),_T("2-8")},
		{SQL_C_INTERVAL_DAY_TO_HOUR,_T("SQL_C_INTERVAL_DAY_TO_HOUR"),_T("163 12"),_T("163 12"),_T(" 163 12"),_T("163 12")},
		{SQL_C_INTERVAL_DAY_TO_MINUTE,_T("SQL_C_INTERVAL_DAY_TO_MINUTE"),_T("163 12:39"),_T("163 12:39"),_T(" 163 12:39"),_T("163 12:39")},
		{SQL_C_INTERVAL_DAY_TO_SECOND,_T("SQL_C_INTERVAL_DAY_TO_SECOND"),_T("163 12:39:59"),_T("163 12:39:59"),_T(" 163 12:39:59"),_T("163 12:39:59")},
		{SQL_C_INTERVAL_HOUR_TO_MINUTE,_T("SQL_C_INTERVAL_HOUR_TO_MINUTE"),_T("12:39"),_T("12:39"),_T(" 12:39"),_T("12:39")},
		{SQL_C_INTERVAL_HOUR_TO_SECOND,_T("SQL_C_INTERVAL_HOUR_TO_SECOND"),_T("12:39:59"),_T("12:39:59"),_T(" 12:39:59"),_T("12:39:59")},
		{SQL_C_INTERVAL_MINUTE_TO_SECOND,_T("SQL_C_INTERVAL_MINUTE_TO_SECOND"),_T("39:59"),_T("39:59"),_T(" 39:59"),_T("39:59")},
#endif
		{999,}
		};
 
//************************************************
// Data structures for Testing Section #5
// SQL_C_DEFAULT to SQL (single field)

	struct 
	{
		TCHAR				*TestSQLType[MAX_BINDPARAM3];
		SQLSMALLINT			SQLType[MAX_BINDPARAM3];
		SQLUINTEGER			ColPrec[MAX_BINDPARAM3];
		SQLSMALLINT			ColScale[MAX_BINDPARAM3];
		TCHAR				*CrtTab;
	} CDataArgToSQL5[] = 
	{
		{
			_T("SQL_INTERVAL_YEAR"),_T("SQL_INTERVAL_MONTH"),_T("SQL_INTERVAL_DAY"),_T("SQL_INTERVAL_HOUR"),_T("SQL_INTERVAL_MINUTE"),
			SQL_INTERVAL_YEAR,SQL_INTERVAL_MONTH,SQL_INTERVAL_DAY,SQL_INTERVAL_HOUR,SQL_INTERVAL_MINUTE,
			0,0,0,0,0,
			0,0,0,0,0,
			_T("--"),
		},

		{_T("999"),}
	};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM3];
//		TCHAR		OutputValue[MAX_BINDPARAM3][35];
	} CDataValueTOSQL5[2] = {
		{SQL_C_DEFAULT,_T("SQL_C_DEFAULT"),_T(" 99"),_T(" 99"),_T(" 99"),_T(" 99"),_T(" 99")},
		{999,}
	};

	TCHAR	*DrpTab5,*InsTab5,*SelTab5;
 
	SQL_INTERVAL_STRUCT CINTERVALTOSQL5;
	
	SQL_INTERVAL_STRUCT CINTERVALTOSQL6;

//************************************************
// Data structures for Testing Section #6
// SQL_C_DEFAULT to SQL (multiple field)

	struct 
	{
		TCHAR				*TestSQLType[MAX_BINDPARAM4];
		SQLSMALLINT			SQLType[MAX_BINDPARAM4];
		SQLUINTEGER			ColPrec[MAX_BINDPARAM4];
		SQLSMALLINT			ColScale[MAX_BINDPARAM4];
		TCHAR				*CrtTab;
	} CDataArgToSQL6[] = 
	{
		{
			_T("SQL_INTERVAL_SECOND"),_T("SQL_INTERVAL_YEAR_TO_MONTH"),_T("SQL_INTERVAL_DAY_TO_HOUR"),_T("SQL_INTERVAL_DAY_TO_MINUTE"),_T("SQL_INTERVAL_DAY_TO_SECOND"),_T("SQL_INTERVAL_HOUR_TO_MINUTE"),_T("SQL_INTERVAL_HOUR_TO_SECOND"),_T("SQL_INTERVAL_MINUTE_TO_SECOND"),
			SQL_INTERVAL_SECOND,SQL_INTERVAL_YEAR_TO_MONTH,SQL_INTERVAL_DAY_TO_HOUR,SQL_INTERVAL_DAY_TO_MINUTE,SQL_INTERVAL_DAY_TO_SECOND,SQL_INTERVAL_HOUR_TO_MINUTE,SQL_INTERVAL_HOUR_TO_SECOND,SQL_INTERVAL_MINUTE_TO_SECOND,
			0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,
			_T("--"),
		},
		{_T("999"),}
	};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		*OutputValue[MAX_BINDPARAM4];
//		TCHAR		OutputValue[MAX_BINDPARAM4][35];
	} CDataValueTOSQL6[2] = {
		{SQL_C_DEFAULT,_T("SQL_C_DEFAULT"),_T(" 59"),_T(" 99-11"),_T(" 99 23"),_T(" 99 23:59"),_T(" 99 23:59:59"),_T(" 23:59"),_T(" 23:59:59"),_T(" 59:59")},
		{999,}
		};

	TCHAR	*DrpTab6,*InsTab6,*SelTab6;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLBindParameterInterval"), charset_file);
	if (var_list == NULL) return FAILED;

	CDataArgToSQL1[0].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_0"), var_list);
	CDataArgToSQL1[1].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_1"), var_list);
	CDataArgToSQL1[2].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_2"), var_list);
	CDataArgToSQL1[3].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_3"), var_list);
	CDataArgToSQL1[4].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_4"), var_list);

	CDataArgToSQL2[0].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_0"), var_list);
	CDataArgToSQL2[1].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_1"), var_list);
	CDataArgToSQL2[2].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_2"), var_list);
	CDataArgToSQL2[3].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_3"), var_list);
	CDataArgToSQL2[4].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_4"), var_list);
	CDataArgToSQL2[5].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_5"), var_list);
	CDataArgToSQL2[6].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_6"), var_list);
	CDataArgToSQL2[7].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL2_CrtTab_7"), var_list);

	CDataArgToSQL5[0].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL5_CrtTab_0"), var_list);
	CDataArgToSQL6[0].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL6_CrtTab_0"), var_list);

	DrpTab1 = var_mapping(_T("SQLBindParameterInterval_DrpTab1"), var_list);
	InsTab1 = var_mapping(_T("SQLBindParameterInterval_InsTab1"), var_list);
	SelTab1 = var_mapping(_T("SQLBindParameterInterval_SelTab1"), var_list);

	DrpTab2 = var_mapping(_T("SQLBindParameterInterval_DrpTab2"), var_list);
	InsTab2 = var_mapping(_T("SQLBindParameterInterval_InsTab2"), var_list);
	SelTab2 = var_mapping(_T("SQLBindParameterInterval_SelTab2"), var_list);

	DrpTab5 = var_mapping(_T("SQLBindParameterInterval_DrpTab5"), var_list);
	InsTab5 = var_mapping(_T("SQLBindParameterInterval_InsTab5"), var_list);
	SelTab5 = var_mapping(_T("SQLBindParameterInterval_SelTab5"), var_list);

	DrpTab6 = var_mapping(_T("SQLBindParameterInterval_DrpTab6"), var_list);
	InsTab6 = var_mapping(_T("SQLBindParameterInterval_InsTab6"), var_list);
	SelTab6 = var_mapping(_T("SQLBindParameterInterval_SelTab6"), var_list);

#ifdef UNICODE
	CDataArgToSQL1[5].CrtTab = var_mapping(_T("SQLBindParameterInterval_CDataArgToSQL1_CrtTab_5"), var_list);

#endif

//===========================================================================================================
// Initialization Test Case

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLBindParameter.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("SQLBindParameter Interval tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
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
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; 

	TempType = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(TempType,_T(""));
	InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);

//=================================================================================================================
// Testing Interval Section #1
// converting from cinterval to sql
// Uses data structures CDataArgToSQL1 & CDataValueTOSQL1
 
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL1[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL1[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL1[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL1[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab1,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab1,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM1; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL1[i].TestCType, SQLTypeToChar(CDataArgToSQL1[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataValueTOSQL1[i].CType == SQL_C_INTERVAL_YEAR || CDataValueTOSQL1[i].CType == SQL_C_INTERVAL_MONTH || CDataValueTOSQL1[i].CType == SQL_C_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL1.intval.year_month.year = 1;
					CINTERVALTOSQL1.intval.year_month.month = 1;
					CINTERVALTOSQL1.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL1[i].CType,
												CDataArgToSQL1[i].SQLType[j],
												CDataArgToSQL1[i].ColPrec[j],
												CDataArgToSQL1[i].ColScale[j],
												&CINTERVALTOSQL1,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL2.intval.day_second.day = 1;
					CINTERVALTOSQL2.intval.day_second.hour = 1;
					CINTERVALTOSQL2.intval.day_second.minute = 1;
					CINTERVALTOSQL2.intval.day_second.second = 1;
					CINTERVALTOSQL2.intval.day_second.fraction = 0;
					CINTERVALTOSQL2.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL1[i].CType,
												CDataArgToSQL1[i].SQLType[j],
												CDataArgToSQL1[i].ColPrec[j],
												CDataArgToSQL1[i].ColScale[j],
												&CINTERVALTOSQL2,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL1[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL1[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab1,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab1,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL1[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL1[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL1[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL1[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);

//=================================================================================================================
// Testing Interval Section #2
// converting from cinterval to sql
// Uses data structures CDataArgToSQL2 & CDataValueTOSQL2

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL2[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL2[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab2,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL2[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL2[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab2,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab2,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM2; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL2[i].TestCType, SQLTypeToChar(CDataArgToSQL2[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataValueTOSQL2[i].CType == SQL_C_INTERVAL_YEAR || CDataValueTOSQL2[i].CType == SQL_C_INTERVAL_MONTH || CDataValueTOSQL2[i].CType == SQL_C_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL3.intval.year_month.year = 1;
					CINTERVALTOSQL3.intval.year_month.month = 1;
					CINTERVALTOSQL3.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL2[i].CType,
												CDataArgToSQL2[i].SQLType[j],
												CDataArgToSQL2[i].ColPrec[j],
												CDataArgToSQL2[i].ColScale[j],
												&CINTERVALTOSQL3,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL4.intval.day_second.day = 1;
					CINTERVALTOSQL4.intval.day_second.hour = 1;
					CINTERVALTOSQL4.intval.day_second.minute = 1;
					CINTERVALTOSQL4.intval.day_second.second = 1;
					CINTERVALTOSQL4.intval.day_second.fraction = 0;
					CINTERVALTOSQL4.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL2[i].CType,
												CDataArgToSQL2[i].SQLType[j],
												CDataArgToSQL2[i].ColPrec[j],
												CDataArgToSQL2[i].ColScale[j],
												&CINTERVALTOSQL4,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL2[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL2[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab2,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab2,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM2; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL2[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL2[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL2[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL2[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab2,SQL_NTS);

//====================================================================================================
// Testing Interval Section #3
// converting from C(single fields) to sql
// Uses data structures CDataArgToSQL1 & CDataValueTOSQL3

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL3[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL3[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL1[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL3[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab1,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab1,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM1; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL3[i].TestCType, SQLTypeToChar(CDataArgToSQL1[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataValueTOSQL3[i].CType == SQL_C_INTERVAL_YEAR || CDataValueTOSQL3[i].CType == SQL_C_INTERVAL_MONTH || CDataValueTOSQL3[i].CType == SQL_C_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL1.intval.year_month.year = 02;
					CINTERVALTOSQL1.intval.year_month.month = 8;
					CINTERVALTOSQL1.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL3[i].CType,
												CDataArgToSQL1[i].SQLType[j],
												CDataArgToSQL1[i].ColPrec[j],
												CDataArgToSQL1[i].ColScale[j],
												&CINTERVALTOSQL1,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL2.intval.day_second.day = 163;
					CINTERVALTOSQL2.intval.day_second.hour = 12;
					CINTERVALTOSQL2.intval.day_second.minute = 39;
					CINTERVALTOSQL2.intval.day_second.second = 59;
					CINTERVALTOSQL2.intval.day_second.fraction = 0;
					CINTERVALTOSQL2.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL3[i].CType,
												CDataArgToSQL1[i].SQLType[j],
												CDataArgToSQL1[i].ColPrec[j],
												CDataArgToSQL1[i].ColScale[j],
												&CINTERVALTOSQL2,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL3[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL3[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab1,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab1,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL3[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL3[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL3[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);
	
//====================================================================================================
// Testing Interval Section #4
// converting from C(multiple fields) to sql
// Uses data structures CDataArgToSQL2 & CDataValueTOSQL4
 
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL4[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL4[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab2,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL2[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab2,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab2,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM2; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL4[i].TestCType, SQLTypeToChar(CDataArgToSQL2[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataValueTOSQL4[i].CType == SQL_C_INTERVAL_YEAR || CDataValueTOSQL4[i].CType == SQL_C_INTERVAL_MONTH || CDataValueTOSQL4[i].CType == SQL_C_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL3.intval.year_month.year = 02;
					CINTERVALTOSQL3.intval.year_month.month = 8;
					CINTERVALTOSQL3.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL4[i].CType,
												CDataArgToSQL2[i].SQLType[j],
												CDataArgToSQL2[i].ColPrec[j],
												CDataArgToSQL2[i].ColScale[j],
												&CINTERVALTOSQL3,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL4.intval.day_second.day = 163;
					CINTERVALTOSQL4.intval.day_second.hour = 12;
					CINTERVALTOSQL4.intval.day_second.minute = 39;
					CINTERVALTOSQL4.intval.day_second.second = 59;
					CINTERVALTOSQL4.intval.day_second.fraction = 0;
					CINTERVALTOSQL4.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL4[i].CType,
												CDataArgToSQL2[i].SQLType[j],
												CDataArgToSQL2[i].ColPrec[j],
												CDataArgToSQL2[i].ColScale[j],
												&CINTERVALTOSQL4,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab2,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab2,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM2; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL4[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL4[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL4[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL4[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab2,SQL_NTS);

//====================================================================================================
// Testing Interval Section #5
// converting from SQL_C_DEFAULT to sql (single interval fields)
// Uses data structures CDataArgToSQL5 & CDataValueTOSQL5
 
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL5[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL5[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab5,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL5[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL5[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab5,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab5,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM3; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL5[i].TestCType, SQLTypeToChar(CDataArgToSQL5[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataArgToSQL5[i].SQLType[j] == SQL_INTERVAL_YEAR || CDataArgToSQL5[i].SQLType[j] == SQL_INTERVAL_MONTH || CDataArgToSQL5[i].SQLType[j] == SQL_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL5.intval.year_month.year = 99;
					CINTERVALTOSQL5.intval.year_month.month = 99;
					CINTERVALTOSQL5.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL5[i].CType,
												CDataArgToSQL5[i].SQLType[j],
												CDataArgToSQL5[i].ColPrec[j],
												CDataArgToSQL5[i].ColScale[j],
												&CINTERVALTOSQL5,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL6.intval.day_second.day = 99;
					CINTERVALTOSQL6.intval.day_second.hour = 99;
					CINTERVALTOSQL6.intval.day_second.minute = 99;
					CINTERVALTOSQL6.intval.day_second.second = 99;
					CINTERVALTOSQL6.intval.day_second.fraction = 0;
					CINTERVALTOSQL6.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL5[i].CType,
												CDataArgToSQL5[i].SQLType[j],
												CDataArgToSQL5[i].ColPrec[j],
												CDataArgToSQL5[i].ColScale[j],
												&CINTERVALTOSQL6,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL5[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL5[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab5,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab5,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM3; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL5[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL5[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab5,SQL_NTS);
 
//====================================================================================================
// Testing Interval Section #6
// converting from SQL_C_DEFAULT to sql (multiple interval fields)
// Uses data structures CDataArgToSQL6 & CDataValueTOSQL6

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL6[i].CType != 999)
		{
			// Creating table
			_stprintf(Heading,_T("Setup for SQLBindParameter tests to create table for conversion from %s.\n"),CDataValueTOSQL6[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CDataArgToSQL6[i].CrtTab);
			LogMsg(NONE, _T("%s\n"), InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueTOSQL6[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)(SQLTCHAR*)InsTab6,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterInterval_Cleanup(hstmt,DrpTab6,TempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM4; j++)
			{
				_stprintf(Heading,_T("SQLBindParameter from %s to %s.\n"), CDataValueTOSQL6[i].TestCType, SQLTypeToChar(CDataArgToSQL6[i].SQLType[j],TempType));
				TESTCASE_BEGINW(Heading);
				if (CDataArgToSQL6[i].SQLType[j] == SQL_INTERVAL_YEAR || CDataArgToSQL6[i].SQLType[j] == SQL_INTERVAL_MONTH || CDataArgToSQL6[i].SQLType[j] == SQL_INTERVAL_YEAR_TO_MONTH)
				{
					CINTERVALTOSQL5.intval.year_month.year = 99;
					CINTERVALTOSQL5.intval.year_month.month = 11;
					CINTERVALTOSQL5.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL6[i].CType,
												CDataArgToSQL6[i].SQLType[j],
												CDataArgToSQL6[i].ColPrec[j],
												CDataArgToSQL6[i].ColScale[j],
												&CINTERVALTOSQL5,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				else
				{
					CINTERVALTOSQL6.intval.day_second.day = 99;
					CINTERVALTOSQL6.intval.day_second.hour = 23;
					CINTERVALTOSQL6.intval.day_second.minute = 59;
					CINTERVALTOSQL6.intval.day_second.second = 59;
					CINTERVALTOSQL6.intval.day_second.fraction = 0;
					CINTERVALTOSQL6.interval_sign = SQL_FALSE;
					returncode = SQLBindParameter(
												hstmt,
												(SWORD)(j+1),
												ParamType,
												CDataValueTOSQL6[i].CType,
												CDataArgToSQL6[i].SQLType[j],
												CDataArgToSQL6[i].ColPrec[j],
												CDataArgToSQL6[i].ColScale[j],
												&CINTERVALTOSQL6,
												sizeof(SQL_INTERVAL_STRUCT),
												&InValue
											);
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueTOSQL6[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueTOSQL6[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab6,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab6,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM4; j++)
						{
							LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL6[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL6[i].OutputValue[j])) == 0)
								{
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL6[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),CDataValueTOSQL6[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);

//=================================================================================================================

	TestMXSQLBindParamaterInterval_Cleanup(hstmt,_T(""),TempType,InsStr,pTestInfo);
	free_list(var_list);
	TEST_RETURN;
}

void TestMXSQLBindParamaterInterval_Cleanup(SQLHANDLE hstmt, TCHAR* DrpTab, TCHAR* TempType,
										TCHAR* InsStr, TestInfo* pTestInfo)
{
	if (_tcscmp(DrpTab,_T("")) != 0)
	{
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab,SQL_NTS);
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	free(TempType);
	free(InsStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLBindParameter.\n"));

}
